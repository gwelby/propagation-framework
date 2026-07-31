#!/usr/bin/env python3
"""
Explorer Truth Layer V5 — Browser DOM Runtime Proof

V5 fixes V4 defects:
  1. Rendered authority binding: each status badge on a claim route must
     carry a machine-readable claim ID and be compared against the generated
     status and confidence.
  2. A visible bare tier, unknown claim ID, or mismatched status/confidence
     must FAIL.
  3. Counting pills is not proof.

Uses Playwright to:
  1. Start the Explorer's serve.py (V5 allowlist-enforced)
  2. Load each HTML route in a headless browser
  3. For claim routes: verify rendered badges match authority data
  4. For non-claim routes: verify no status badges appear
  5. Report DOM evidence with claim IDs and expected/actual comparison
"""

from __future__ import annotations

import datetime
import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent
SERVE_SCRIPT = EXPLORER_DIR / "serve.py"
REGISTRY_PATH = EXPLORER_DIR / "release_tree_registry.json"
EVIDENCE_PATH = EXPLORER_DIR / "_browser_dom_evidence.json"

# V5.6: Closed vocabulary of accepted non-authority reasons.
# Only 'axiom' and 'intermediate-ui' are semantically eligible non-authority
# classifications produced by resolveNodeAuthority() in timeline.js.
# Any other reason value is treated as a potential authority-bypass.
CLOSED_REASON_VOCABULARY = {"axiom", "intermediate-ui"}


def _find_free_port() -> int:
    """Find an isolated free port on loopback."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server() -> tuple[subprocess.Popen, int]:
    """Start the Explorer's V5 serve.py on an isolated free test port.

    V5.2: The proof must own its server. We pick a fresh free port, start the
    candidate serve.py with that port, and fail if the child exits or an
    unrelated process already owns the port.
    """
    port = _find_free_port()
    proc = subprocess.Popen(
        [sys.executable, str(SERVE_SCRIPT), str(port)],
        cwd=str(EXPLORER_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid if sys.platform != "win32" else None,
    )
    url = f"http://127.0.0.1:{port}/index.html"
    for _ in range(30):
        time.sleep(0.5)
        if proc.poll() is not None:
            stdout = proc.stdout.read().decode("utf-8", errors="ignore")[:500] if proc.stdout else ""
            stderr = proc.stderr.read().decode("utf-8", errors="ignore")[:500] if proc.stderr else ""
            raise RuntimeError(
                f"serve.py exited before binding to port {port} (rc={proc.returncode}). "
                f"stdout={stdout!r} stderr={stderr!r}"
            )
        try:
            with urllib.request.urlopen(url, timeout=3) as resp:
                if resp.status == 200:
                    return proc, port
        except Exception:
            pass
    raise RuntimeError(f"serve.py did not become ready on isolated port {port} within 15s")


def stop_server(proc: subprocess.Popen):
    try:
        if sys.platform != "win32":
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        else:
            proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def _extract_js_object(text: str, var_name: str) -> dict:
    """Extract a JS object assignment like `window.X = {...};` and parse as JSON."""
    import re
    m = re.search(rf'window\.{re.escape(var_name)}\s*=\s*(\{{.*?\n\}});\s*\n', text, re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}


def load_authority_data() -> dict:
    """Load the generated authority data for comparison."""
    claims_js = EXPLORER_DIR / "data.claims.js"
    explorer_data_js = EXPLORER_DIR / "data.js"
    import re
    text = claims_js.read_text(encoding="utf-8")
    m = re.search(r'window\.PFClaimsData\s*=\s*(\{.*?\});', text, re.DOTALL)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    claims = {}
    for c in data.get("claims", []):
        status = c.get("status") or "UNAVAILABLE"
        badge = c.get("badge", status)
        # V5.4: For STANDARD MATH claims, the rendered status label comes from the
        # badge (e.g. "STANDARD MATH 0.85"), not from the authority status field.
        display_status = status
        if c.get("isStandardMath"):
            m = re.match(r"^([A-Za-z\s\-]+?)(?=\s*\d|\/|\()", badge)
            if m:
                display_status = m.group(1).strip()
        claims[c["id"]] = {
            "status": display_status,
            "raw_status": status,
            "confidence": c.get("confidence"),
            "badge": badge,
            "isSplit": c.get("isSplit", False),
            "isStandardMath": c.get("isStandardMath", False),
        }
    for d in data.get("definitions", []):
        # Definitions carry canonical status but no confidence score.
        claims[d["id"]] = {
            "status": d.get("status"),
            "confidence": None,
            "badge": d.get("auditLine", d.get("status", "")),
            "isSplit": False,
            "isStandardMath": False,
        }

    # V5.4: Also index PFExplorerData.results by result id, so dynamic surfaces
    # (scale-ladder, journey fallback, etc.) that expose a result id can be
    # verified against authority.
    if explorer_data_js.is_file():
        explorer_data = _extract_js_object(explorer_data_js.read_text(encoding="utf-8"), "PFExplorerData")
        for r in explorer_data.get("results", []):
            rid = r.get("id")
            if rid and rid not in claims:
                claims[rid] = {
                    "status": r.get("status"),
                    "confidence": r.get("confidence"),
                    "badge": r.get("badge", r.get("status", "")),
                    "isSplit": r.get("isSplit", False),
                    "isStandardMath": r.get("isStandardMath", False),
                }
    return claims


class MappingParseError(Exception):
    """V5.8: Raised when the mapping parser encounters a hard failure."""


class InventoryError(Exception):
    """V5.8: Raised when the expected inventory is missing, empty, or invalid."""


def load_node_authority_mapping() -> tuple[dict[str, str], list[str]]:
    """V5.8: Load the NODE_TO_AUTHORITY mapping from timeline.js.

    V5.8 hardening (Codex V57-02):
    - Handles both single-quoted and double-quoted entries
    - HARD-FAILS on malformed entries (returns them in the malformed list)
    - Detects duplicate keys before dictionary collapse
    - Returns (mapping, malformed) tuple so the caller can hard-fail

    Returns:
        (mapping, malformed) where mapping is the parsed dict and malformed
        is a list of entries that could not be parsed. The caller MUST
        check malformed and fail if non-empty.

    Raises:
        MappingParseError: if the file is missing, the NODE_TO_AUTHORITY block
        is missing, or duplicate keys are detected.
    """
    import re
    timeline_js = EXPLORER_DIR / "timeline.js"
    if not timeline_js.is_file():
        raise MappingParseError(f"timeline.js not found: {timeline_js}")
    text = timeline_js.read_text(encoding="utf-8")
    m = re.search(r"var\s+NODE_TO_AUTHORITY\s*=\s*\{(.*?)\};", text, re.DOTALL)
    if not m:
        raise MappingParseError("NODE_TO_AUTHORITY block not found in timeline.js")
    mapping: dict[str, str] = {}
    seen_keys: set[str] = set()
    malformed: list[str] = []
    duplicates: list[str] = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        # V5.9: Normalize one allowed trailing comma, then require full match.
        # This catches same-line duplicates and same-line unexpected properties
        # that are valid JavaScript but outside the accepted one-entry-per-line
        # grammar. (Codex V58-01: re.match was prefix-only.)
        if line.endswith(","):
            line = line[:-1].rstrip()
        # V5.9: Use fullmatch so trailing tokens after a valid prefix are rejected
        m2 = re.fullmatch(r"""['"]([^'"]+)['"]:\s*['"]([^'"]+)['"]""", line)
        if m2:
            key = m2.group(1)
            # V5.8: Detect duplicate keys before dictionary collapse
            if key in seen_keys:
                duplicates.append(key)
                continue
            seen_keys.add(key)
            mapping[key] = m2.group(2)
        else:
            # V5.8: Collect malformed entries for caller to hard-fail on
            malformed.append(line)
    if duplicates:
        raise MappingParseError(f"Duplicate mapping keys detected: {duplicates}")
    return mapping, malformed


def load_expected_mapping_inventory() -> dict[str, str]:
    """V5.10: Load the expected mapping inventory for exact-snapshot comparison.

    V5.10 hardening (Codex V59-01/V59-02):
    - HARD-FAILS (raises InventoryError) if the file is missing
    - HARD-FAILS if the file is empty or has no mappings
    - HARD-FAILS if mappings is not a dict
    - _version is MANDATORY: must be present, must be a string, must start with "V"
    - _expected_count is MANDATORY: must be present, must be an integer,
      and must equal len(mappings)
    - _source_hash is not used and not present in the inventory

    Scope: This is an exact-snapshot comparison guard. The inventory file
    lives in the same candidate revision as timeline.js. It detects
    one-sided mapping deletion but cannot detect coordinated deletion
    from both files. It is NOT an independent, frozen, or drift-resistant
    root of trust.

    Raises:
        InventoryError: if the inventory is missing, empty, malformed,
        missing _version, missing _expected_count, or has a count mismatch.
    """
    inventory_path = EXPLORER_DIR / "expected_node_authority_mapping.json"
    if not inventory_path.is_file():
        raise InventoryError(f"Expected mapping inventory not found: {inventory_path}")
    try:
        data = json.loads(inventory_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise InventoryError(f"Expected mapping inventory is not valid JSON: {e}")
    mappings = data.get("mappings")
    if not isinstance(mappings, dict):
        raise InventoryError("Expected mapping inventory 'mappings' must be a non-empty object")
    if len(mappings) == 0:
        raise InventoryError("Expected mapping inventory 'mappings' is empty")
    # V5.10: _version is MANDATORY (Codex V59-01)
    if "_version" not in data:
        raise InventoryError("Expected mapping inventory is missing required '_version' field")
    version = data["_version"]
    if not isinstance(version, str):
        raise InventoryError(f"_version must be a string, got {type(version).__name__}")
    if not version.startswith("V"):
        raise InventoryError(f"_version must start with 'V', got '{version}'")
    # V5.9: _expected_count is MANDATORY
    if "_expected_count" not in data:
        raise InventoryError("Expected mapping inventory is missing required '_expected_count' field")
    expected_count = data["_expected_count"]
    if not isinstance(expected_count, int):
        raise InventoryError(f"_expected_count must be an integer, got {type(expected_count).__name__}")
    if expected_count != len(mappings):
        raise InventoryError(f"_expected_count={expected_count} but mappings has {len(mappings)} entries")
    return mappings


def verify_mapping_completeness(
    parsed: dict[str, str], expected: dict[str, str]
) -> list[dict]:
    """V5.8: Verify parsed mapping matches expected inventory.

    Returns a list of failure dicts (empty if mapping is complete and correct).
    Checks:
    - Every expected entry is present in parsed mapping
    - No extra entries in parsed mapping
    - Values match for every key
    """
    failures: list[dict] = []
    for key, expected_val in expected.items():
        if key not in parsed:
            failures.append({
                "error": f"Missing mapping entry: '{key}' -> '{expected_val}'",
                "type": "missing_entry",
                "key": key,
                "expected": expected_val,
            })
        elif parsed[key] != expected_val:
            failures.append({
                "error": f"Mapping value mismatch for '{key}': expected '{expected_val}', got '{parsed[key]}'",
                "type": "value_mismatch",
                "key": key,
                "expected": expected_val,
                "observed": parsed[key],
            })
    for key in parsed:
        if key not in expected:
            failures.append({
                "error": f"Unexpected mapping entry: '{key}' -> '{parsed[key]}'",
                "type": "extra_entry",
                "key": key,
                "observed": parsed[key],
            })
    return failures


STATUS_ELEMENT_SELECTORS = (
    ".status-pill, .status-badge, [data-status-note], .result-card-status, .eb-status-pill, .result-status, "
    ".detail-confidence, .node-status-label, .node-conf-value, .detail-status, .conf-value"
)


def _collect_status_elements(page, selector: str = STATUS_ELEMENT_SELECTORS) -> list:
    """V5.5: Collect all authority-bearing status elements in the current DOM.

    Each authority-bearing element must carry its own data-claim-id binding.
    Non-authority UI must carry data-status-reason with a source-backed reason.
    Parent inheritance is intentionally disabled so that removing a binding
    from a Journey result-card or Experiment Bench pill is detected.
    """
    return page.evaluate(
        """
        (selector) => {
            const pills = document.querySelectorAll(selector);
            return Array.from(pills).map(p => {
                return {
                    text: p.textContent.trim(),
                    class: p.className,
                    claimId: p.dataset.claimId || null,
                    statusReason: p.dataset.statusReason || null,
                    tagName: p.tagName,
                    parentTag: p.parentElement ? p.parentElement.tagName : null,
                    parentClass: p.parentElement ? p.parentElement.className : null,
                };
            });
        }
        """,
        selector,
    )


def _verify_mapped_nodes(page, node_mapping: dict[str, str], authority_claims: dict) -> list[dict]:
    """V5.7: Verify that each mapped timeline node renders with the correct
    data-claim-id binding on its status and confidence elements.

    V5.7 hardening (Codex V56-02):
    - Hard-fails when a mapped DOM node is absent (was: silently skipped)
    - Hard-fails when .node-status-label or .node-conf-value is absent
    - Does NOT skip any mapped node — all must be present and correct

    For each entry in NODE_TO_AUTHORITY, query the DOM for the node's
    .node-status-label and .node-conf-value elements and verify they carry
    the expected data-claim-id. A mapped node that renders with
    data-status-reason instead of data-claim-id is an authority bypass.

    Returns a list of failure dicts (empty if all mapped nodes are correct).
    """
    failures: list[dict] = []
    for node_id, expected_claim_id in node_mapping.items():
        # Query the timeline node's status label and confidence value
        result = page.evaluate(
            """
            ([nodeId, expectedClaimId]) => {
                var nodeG = document.querySelector('[data-id="' + nodeId + '"]');
                if (!nodeG) return { found: false };
                var statusLabel = nodeG.querySelector('.node-status-label');
                var confValue = nodeG.querySelector('.node-conf-value');
                return {
                    found: true,
                    statusLabel: statusLabel ? {
                        text: statusLabel.textContent.trim(),
                        claimId: statusLabel.getAttribute('data-claim-id'),
                        statusReason: statusLabel.getAttribute('data-status-reason'),
                    } : null,
                    confValue: confValue ? {
                        text: confValue.textContent.trim(),
                        claimId: confValue.getAttribute('data-claim-id'),
                        statusReason: confValue.getAttribute('data-status-reason'),
                    } : null,
                };
            }
            """,
            [node_id, expected_claim_id],
        )
        # V5.7: Hard-fail on missing DOM node (was: silently skipped)
        if not result.get("found"):
            failures.append({
                "node_id": node_id,
                "element": "node",
                "expected_claim_id": expected_claim_id,
                "observed_claim_id": None,
                "observed_status_reason": None,
                "error": f"Mapped node '{node_id}' not found in DOM (data-id='{node_id}')",
            })
            continue

        # V5.7: Hard-fail on missing status label or confidence value
        for elem_name in ("statusLabel", "confValue"):
            elem = result.get(elem_name)
            if not elem:
                failures.append({
                    "node_id": node_id,
                    "element": elem_name,
                    "expected_claim_id": expected_claim_id,
                    "observed_claim_id": None,
                    "observed_status_reason": None,
                    "error": f"Mapped node '{node_id}' missing .{elem_name} element",
                })
                continue
            claim_id = elem.get("claimId")
            status_reason = elem.get("statusReason")
            if claim_id != expected_claim_id:
                failures.append({
                    "node_id": node_id,
                    "element": elem_name,
                    "expected_claim_id": expected_claim_id,
                    "observed_claim_id": claim_id,
                    "observed_status_reason": status_reason,
                    "error": f"Mapped node '{node_id}' {elem_name} has claim-id={claim_id!r}, expected {expected_claim_id!r}"
                        + (f" (carries status-reason={status_reason!r} instead)" if status_reason else ""),
                })
    return failures


def _verify_inventory_entry(page, entry: dict, authority_claims: dict) -> dict:
    """V5.2/V5.4: Activate and verify one static or dynamic status inventory entry.

    Returns a dict with ok, claimId, selector, observed, and error if failed.
    """
    import re as _re
    claim_id = entry["claimId"]
    selector = entry["selector"]
    activation = entry.get("activation")
    expected_status = entry.get("expectedStatus", "").upper()
    expected_conf = entry.get("expectedConfidence")
    non_authority = entry.get("nonAuthority", False) or claim_id == ""
    is_dynamic = entry.get("dynamic", False) or claim_id == "*"
    result = {
        "claimId": claim_id,
        "selector": selector,
        "activation": activation,
        "ok": False,
    }

    try:
        if activation:
            try:
                # V5.5: Activation may be a CSS selector (click) or a JS expression (evaluate).
                if activation.startswith("window.") or "(" in activation:
                    page.evaluate("() => { " + activation + "; }")
                    page.wait_for_timeout(800)
                else:
                    el = page.query_selector(activation)
                    if el:
                        el.click()
                        page.wait_for_timeout(800)
            except Exception as e:
                result["error"] = f"activation failed: {e}"
                return result

        # V5.4/V5.5: Dynamic inventory entries verify every matching element.
        if is_dynamic:
            elements = page.query_selector_all(selector)
            if not elements:
                result["error"] = f"dynamic selector returned no elements: {selector}"
                return result
            observed = []
            errors = []
            for el in elements:
                obs_id = el.get_attribute("data-claim-id")
                if not obs_id:
                    obs_id = el.evaluate("(node) => { var p = node.closest('[data-claim-id]'); return p ? p.getAttribute('data-claim-id') : null; }")
                text = (el.text_content() or "").strip()
                observed.append({"claimId": obs_id, "text": text})
                if non_authority:
                    reason = el.get_attribute("data-status-reason")
                    if not reason:
                        errors.append(f"non-authority element missing data-status-reason in {selector}: '{text}'")
                        continue
                    # V5.6: Enforce closed reason vocabulary
                    if reason not in CLOSED_REASON_VOCABULARY:
                        errors.append(f"unrecognized non-authority reason {reason!r} in {selector} (not in closed vocabulary)")
                        continue
                    if expected_status and expected_status not in text.upper():
                        errors.append(f"non-authority status mismatch in {selector}: expected {expected_status} in '{text}'")
                    continue
                if not obs_id:
                    errors.append(f"missing data-claim-id in {selector}: '{text}'")
                    continue
                if obs_id not in authority_claims:
                    errors.append(f"unknown claim ID in {selector}: {obs_id}")
                    continue
                auth = authority_claims[obs_id]
                auth_status = (auth.get("status") or "").upper()
                text_u = text.upper()
                has_status_word = any(w in text_u for w in
                    ["DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
                     "INTUITION", "OPEN", "EXACT IDENTITY", "CANONICAL",
                     "STANDARD MATH", "NO-GO", "PARTIAL DERIVATION"])
                conf_match = _re.search(r'(\d+\.\d+)', text)
                is_confidence_only = (not has_status_word) and bool(conf_match)
                if not is_confidence_only:
                    if auth_status and auth_status not in text_u and text_u not in auth_status:
                        errors.append(f"status mismatch for {obs_id}: text='{text}' vs authority={auth['status']}")
                        continue
                if expected_conf is not None:
                    if conf_match:
                        pill_conf = float(conf_match.group(1))
                        if abs(pill_conf - expected_conf) > 0.01:
                            errors.append(f"confidence mismatch for {obs_id}: text='{text}' vs expected={expected_conf}")
                    else:
                        errors.append(f"expected confidence {expected_conf} but no numeric confidence in '{text}'")
                elif conf_match and auth.get("confidence") is not None:
                    pill_conf = float(conf_match.group(1))
                    if abs(pill_conf - auth["confidence"]) > 0.01:
                        errors.append(f"confidence mismatch for {obs_id}: text='{text}' vs authority={auth['confidence']}")
            result["observed"] = observed[:5]
            result["observed_count"] = len(elements)
            if errors:
                result["error"] = "; ".join(errors[:3])
                return result
            result["ok"] = True
            return result

        el = page.query_selector(selector)
        if not el:
            result["error"] = "expected status element not found"
            return result

        if non_authority:
            reason = el.get_attribute("data-status-reason")
            result["observed_reason"] = reason
            if not reason:
                result["error"] = f"non-authority element missing data-status-reason: {selector}"
                return result
            # V5.6: Enforce closed reason vocabulary
            if reason not in CLOSED_REASON_VOCABULARY:
                result["error"] = f"unrecognized non-authority reason: {reason!r} (not in closed vocabulary)"
                return result
            text = (el.text_content() or "").strip()
            result["observed_text"] = text
            if expected_status and expected_status not in text.upper():
                result["error"] = f"non-authority status mismatch: expected {expected_status} in '{text}'"
                return result
            result["ok"] = True
            return result

        observed_id = el.get_attribute("data-claim-id")
        if not observed_id:
            # Check closest parent with data-claim-id for sidebar notes
            observed_id = el.evaluate("(node) => { var p = node.closest('[data-claim-id]'); return p ? p.getAttribute('data-claim-id') : null; }")
        result["observed_claimId"] = observed_id
        if observed_id != claim_id:
            result["error"] = f"data-claim-id mismatch: expected {claim_id}, got {observed_id}"
            return result

        text = (el.text_content() or "").strip()
        result["observed_text"] = text
        if expected_status and expected_status not in text.upper():
            result["error"] = f"status mismatch: expected {expected_status} in '{text}'"
            return result

        if expected_conf is not None:
            m = _re.search(r'(\d+\.\d+)', text)
            if not m:
                result["error"] = f"expected confidence {expected_conf} but no numeric confidence in '{text}'"
                return result
            obs_conf = float(m.group(1))
            result["observed_confidence"] = obs_conf
            if abs(obs_conf - expected_conf) > 0.01:
                result["error"] = f"confidence mismatch: expected {expected_conf}, got {obs_conf}"
                return result

        if claim_id not in authority_claims:
            result["error"] = f"unknown claim ID in authority: {claim_id}"
            return result

        result["ok"] = True
    except Exception as e:
        result["error"] = f"exception: {e}"
    return result


def run_browser_proof(port: int, proc: subprocess.Popen) -> dict:
    """V5/V5.2: Run browser DOM proof with authority binding."""
    from playwright.sync_api import sync_playwright

    registry = json.loads(REGISTRY_PATH.read_text())
    served_routes = registry.get("servedRoutes", [])
    route_filter = os.environ.get("PF_RUNTIME_ROUTE")
    if route_filter:
        served_routes = [r for r in served_routes if r.get("path") == route_filter]
    authority_claims = load_authority_data()

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1440, "height": 900})

        for route in served_routes:
            path = route["path"]
            route_type = route.get("type", "unknown")
            url = f"http://127.0.0.1:{port}/{path}"

            page = context.new_page()
            js_errors = []
            page.on("pageerror", lambda err: js_errors.append(str(err)))

            try:
                wait_until = "domcontentloaded" if "journey_live" in path else "networkidle"
                response = page.goto(url, wait_until=wait_until, timeout=30000)
                if response is None or response.status != 200:
                    results[path] = {
                        "status": "FAIL",
                        "reason": f"HTTP {response.status if response else 'no response'}",
                        "route_type": route_type,
                    }
                    continue

                page.wait_for_timeout(3000)

                dom_evidence = {}

                # 1. Check authority data loaded
                has_claims_data = page.evaluate(
                    "() => typeof window.PFClaimsData !== 'undefined' && window.PFClaimsData !== null"
                )
                dom_evidence["PFClaimsData_loaded"] = has_claims_data

                has_explorer_data = page.evaluate(
                    "() => typeof window.PFExplorerData !== 'undefined' && window.PFExplorerData !== null"
                )
                dom_evidence["PFExplorerData_loaded"] = has_explorer_data

                # V5.4: Activate status-bearing surfaces and collect all authority-bearing
                # status elements. index.html has multiple panel routes; walk them so
                # dynamic lists (Experiment Bench, etc.) are mounted and scanned.
                status_pills = []
                panel_activations = []
                if path == "index.html":
                    route_buttons = page.evaluate(
                        "() => Array.from(document.querySelectorAll('[data-route]')).map(b => b.getAttribute('data-route'))"
                    )
                    for route in route_buttons:
                        try:
                            page.evaluate(
                                "(route) => { var b = document.querySelector('[data-route=\"' + route + '\"]'); if (b) b.click(); }",
                                route,
                            )
                            page.wait_for_timeout(500)
                            status_pills.extend(_collect_status_elements(page))
                            panel_activations.append(route)
                        except Exception as _e:
                            panel_activations.append(f"{route}:error")
                    page.wait_for_timeout(1000)
                elif path == "derivation.html":
                    # V5.5: Exercise the derivation graph and timeline interactions
                    # before scanning so dynamically-rendered status elements are mounted.
                    for _ in range(20):
                        if page.evaluate(
                            "() => typeof window.DerivationRoute !== 'undefined' && window.DerivationRoute.isReady()"
                        ):
                            break
                        page.wait_for_timeout(250)
                    page.evaluate("() => { if(window.DerivationRoute) window.DerivationRoute.selectNodeById('weinberg-angle'); }")
                    page.wait_for_timeout(500)
                    page.evaluate("() => { if(window.DerivationTimeline) window.DerivationTimeline.open(); }")
                    for _ in range(20):
                        if page.evaluate(
                            "() => typeof window.DerivationTimeline !== 'undefined' && window.DerivationTimeline.isReady()"
                        ):
                            break
                        page.wait_for_timeout(250)
                    page.evaluate(
                        "() => { if(window.DerivationTimeline) { window.DerivationTimeline.selectNodeById('bohr-quantization'); } }"
                    )
                    page.wait_for_timeout(500)
                    page.evaluate(
                        "() => { if(window.DerivationTimeline) { window.DerivationTimeline.selectNodeById('casimir-poly'); } }"
                    )
                    page.wait_for_timeout(500)
                    status_pills = _collect_status_elements(page)
                    panel_activations = ["graph:weinberg-angle", "timeline:bohr-quantization", "timeline:casimir-poly"]
                else:
                    # Journey result cards, scale-ladder result statuses, and static
                    # route cells render after a short wait.
                    page.wait_for_timeout(2000)
                    status_pills = _collect_status_elements(page)
                dom_evidence["panel_activations"] = panel_activations
                dom_evidence["status_pills"] = status_pills

                # V5.10: Verify mapped timeline nodes render with correct
                # data-claim-id. This catches authority-bypass where a mapped
                # node is rendered with data-status-reason instead of
                # data-claim-id. Only applies to derivation.html (timeline).
                #
                # V5.10 changes (Codex V59-01/V59-02/V59-03):
                # - _version is mandatory (was: unvalidated in V5.9)
                # - All independent/frozen wording removed from inventory
                # - Scope is exact-snapshot comparison (not drift-resistant)
                mapped_node_failures: list[dict] = []
                if path == "derivation.html":
                    # V5.8: Load expected inventory — hard-fail on any error
                    try:
                        expected_mapping = load_expected_mapping_inventory()
                    except InventoryError as e:
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Expected mapping inventory error: {e}",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                        }
                        continue

                    # V5.8: Load parsed mapping — hard-fail on parse error
                    try:
                        parsed_mapping, malformed_entries = load_node_authority_mapping()
                    except MappingParseError as e:
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Mapping parse error: {e}",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                        }
                        continue

                    # V5.8: Hard-fail on malformed entries (was: warn only)
                    if malformed_entries:
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Malformed NODE_TO_AUTHORITY entries: {len(malformed_entries)} entries could not be parsed: {malformed_entries[:3]}",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                            "malformed_entries": malformed_entries[:5],
                        }
                        continue

                    # V5.10: Check mapping completeness against expected inventory
                    mapping_failures = verify_mapping_completeness(parsed_mapping, expected_mapping)
                    if mapping_failures:
                        dom_evidence["mapping_completeness_failures"] = mapping_failures
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Mapping completeness check failed: {len(mapping_failures)} discrepancies",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                            "mapping_failures": mapping_failures[:5],
                        }
                        continue

                    # V5.8: Use the EXPECTED mapping (not parsed) for DOM verification
                    # so that a deleted mapping entry is still checked
                    mapped_node_failures = _verify_mapped_nodes(page, expected_mapping, authority_claims)
                    dom_evidence["mapped_node_failures"] = mapped_node_failures
                    if mapped_node_failures:
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Mapped authority node bypass: {len(mapped_node_failures)} failures",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                            "mapped_node_failures": mapped_node_failures[:5],
                        }
                        continue

                # V5.2: Activate and verify every expected status inventory entry
                # for this route. Missing element, missing data-claim-id, unknown
                # ID, or status/confidence mismatch must fail.
                inventory = registry.get("statusInventory", [])
                route_inventory = [e for e in inventory if e.get("route") == path]
                inventory_results = []
                for entry in route_inventory:
                    inv_res = _verify_inventory_entry(page, entry, authority_claims)
                    inventory_results.append(inv_res)
                dom_evidence["inventory_results"] = inventory_results
                inventory_failures = [r for r in inventory_results if not r.get("ok")]

                # 3. Check for JS errors
                dom_evidence["js_errors"] = js_errors[:5]

                # 4. Page title
                dom_evidence["title"] = page.title()

                # 5. V5: Authority binding verification for claim routes
                authority_binding = []
                if route_type == "claim":
                    dom_evidence["claim_route"] = True

                    if not has_claims_data and not has_explorer_data:
                        results[path] = {
                            "status": "FAIL",
                            "reason": "Claim route did not load authority data",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                        }
                        continue

                    # V5.5: For each status element, verify authority binding or
                    # explicit non-authority classification.
                    import re as _re
                    for pill in status_pills:
                        pill_text = pill.get("text", "")
                        pill_class = pill.get("class", "")
                        claim_id = pill.get("claimId")
                        status_reason = pill.get("statusReason")

                        # Skip empty pills
                        if not pill_text:
                            continue

                        has_status_word = any(w in pill_text.upper() for w in
                            ["DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
                             "INTUITION", "OPEN", "EXACT IDENTITY", "CANONICAL",
                             "STANDARD MATH", "NO-GO", "PARTIAL DERIVATION"])
                        conf_match = _re.search(r'(\d+\.\d+)', pill_text)
                        is_confidence_only = (not has_status_word) and bool(conf_match)

                        binding = {
                            "pill_text": pill_text,
                            "pill_class": pill_class,
                            "claim_id": claim_id,
                            "status_reason": status_reason,
                            "has_status_word": has_status_word,
                        }

                        # V5.6: Explicit non-authority classification — only
                        # accept reasons from the closed vocabulary. Arbitrary
                        # reason text (e.g. 'bogus-bypass') is a potential
                        # authority-bypass on a mapped node and must FAIL.
                        if status_reason:
                            if status_reason not in CLOSED_REASON_VOCABULARY:
                                binding["error"] = (
                                    f"Unrecognized non-authority reason: {status_reason!r} "
                                    f"(not in closed vocabulary {sorted(CLOSED_REASON_VOCABULARY)})"
                                )
                                authority_binding.append(binding)
                                continue
                            binding["non_authority"] = True
                            authority_binding.append(binding)
                            continue

                        # Authority-bearing elements must have a claim ID.
                        if claim_id and claim_id in authority_claims:
                            auth = authority_claims[claim_id]
                            auth_status = auth["status"]
                            auth_conf = auth["confidence"]

                            binding["auth_status"] = auth_status
                            binding["auth_confidence"] = auth_conf

                            # Sentinel for missing/null confidence displayed as em-dash
                            is_missing_conf = pill_text == "\u2014"

                            if is_confidence_only:
                                # Confidence-only element (e.g. .conf-value, .node-conf-value)
                                binding["matches_status"] = True
                                if is_missing_conf:
                                    if auth_conf is None:
                                        binding["matches_confidence"] = True
                                    else:
                                        binding["matches_confidence"] = False
                                        binding["error"] = f"Missing confidence: pill={pill_text} vs authority={auth_conf}"
                                else:
                                    pill_conf = float(conf_match.group(1))
                                    binding["pill_confidence"] = pill_conf
                                    if auth_conf is not None:
                                        binding["matches_confidence"] = abs(pill_conf - auth_conf) < 0.01
                                    else:
                                        binding["matches_confidence"] = False
                                        binding["error"] = f"Unexpected confidence: pill={pill_text} vs authority confidence null"
                                if not binding.get("error") and not binding["matches_confidence"]:
                                    binding["error"] = f"Confidence mismatch: pill={pill_conf} vs authority={auth_conf}"
                            elif is_missing_conf:
                                # Missing confidence marker for an authority-bearing element; skip status check.
                                binding["matches_status"] = True
                                binding["matches_confidence"] = (auth_conf is None)
                                if binding["matches_confidence"] is False:
                                    binding["error"] = f"Missing confidence: pill={pill_text} vs authority={auth_conf}"
                            else:
                                binding["matches_status"] = (
                                    auth_status.upper() in pill_text.upper()
                                    or pill_text.upper() in auth_status.upper()
                                )
                                if conf_match and auth_conf is not None:
                                    pill_conf = float(conf_match.group(1))
                                    binding["pill_confidence"] = pill_conf
                                    binding["matches_confidence"] = abs(pill_conf - auth_conf) < 0.01
                                else:
                                    binding["matches_confidence"] = True

                                if not binding["matches_status"]:
                                    binding["error"] = f"Status mismatch: pill={pill_text} vs authority={auth_status}"
                                elif not binding["matches_confidence"]:
                                    binding["error"] = f"Confidence mismatch: pill={pill_conf} vs authority={auth_conf}"

                        elif claim_id and claim_id not in authority_claims:
                            binding["error"] = f"Unknown claim ID: {claim_id}"
                        elif is_confidence_only:
                            # Confidence number with no claim binding is suspicious
                            binding["error"] = "Confidence value without claim ID binding"
                        elif has_status_word:
                            # Status word with no claim binding is an injection risk
                            binding["error"] = "Status pill without claim ID binding"
                        else:
                            # No status word, no claim id, no reason: ignore
                            continue

                        authority_binding.append(binding)

                    dom_evidence["authority_binding"] = authority_binding

                    # V5: Check for binding errors
                    binding_errors = [b for b in authority_binding if b.get("error")]
                    if binding_errors:
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Authority binding errors: {len(binding_errors)}",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                            "binding_errors": binding_errors[:5],
                        }
                        continue

                # V5.2: Any inventory failure is a runtime proof failure
                if inventory_failures:
                    results[path] = {
                        "status": "FAIL",
                        "reason": f"Status inventory failures: {len(inventory_failures)}",
                        "route_type": route_type,
                        "dom_evidence": dom_evidence,
                        "inventory_failures": inventory_failures[:5],
                    }
                    continue

                if route_type == "non-claim":
                    dom_evidence["non_claim_route"] = True
                    # V5: Non-claim routes must not have status pills
                    if status_pills:
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Non-claim route has {len(status_pills)} status pills",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                        }
                        continue

                # Check for JS errors
                # V5: Distinguish truth-layer errors from visual library errors.
                # CDN libraries (THREE.js, d3.js) may not load in headless mode;
                # these are visual rendering issues, not truth-layer violations.
                # Truth-layer errors are: missing authority data, status pill
                # binding failures, unmapped badges, claim ID mismatches.
                VISUAL_LIB_ERRORS = {"THREE is not defined", "d3 is not defined",
                                     "THREE is not defined", "d3 is not defined"}
                truth_layer_errors = [e for e in js_errors
                                      if not any(vl in e for vl in VISUAL_LIB_ERRORS)]
                visual_errors = [e for e in js_errors
                                 if any(vl in e for vl in VISUAL_LIB_ERRORS)]
                dom_evidence["js_errors"] = js_errors[:5]
                dom_evidence["visual_lib_errors"] = visual_errors[:3]
                dom_evidence["truth_layer_errors"] = truth_layer_errors[:3]

                if truth_layer_errors:
                    results[path] = {
                        "status": "FAIL",
                        "reason": f"Truth-layer JS errors: {truth_layer_errors[:3]}",
                        "route_type": route_type,
                        "dom_evidence": dom_evidence,
                    }
                    continue

                results[path] = {
                    "status": "PASS",
                    "route_type": route_type,
                    "dom_evidence": dom_evidence,
                }

            except Exception as e:
                results[path] = {
                    "status": "ERROR",
                    "reason": str(e),
                    "route_type": route_type,
                }
            finally:
                page.close()

        browser.close()

    return results


def main() -> int:
    print("=" * 70)
    print("Explorer Truth Layer V5/V5.2 — Browser DOM Runtime Proof")
    print("=" * 70)
    print()

    # Start server on an isolated free port
    print("Starting V5/V5.2 release server on an isolated free port...")
    proc, port = start_server()
    print(f"  Candidate server pid={proc.pid} port={port}")

    try:
        # V5: Verify quarantine paths return 404
        print("Verifying quarantine/dev paths return 404...")
        for test_path in ["quarantine/test-d3.html", "dev/test-d3.html", "_blocked.html"]:
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/{test_path}", timeout=5)
                print(f"  FAIL: {test_path} returned 200 (expected 404)")
                return 1
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"  PASS: {test_path} -> 404")
                else:
                    print(f"  FAIL: {test_path} returned {e.code} (expected 404)")
                    return 1
            except Exception:
                print(f"  PASS: {test_path} -> blocked")

        # Run browser proof
        print("\nRunning browser DOM proof with authority binding...")
        results = run_browser_proof(port, proc)

        # V5.2: Evidence includes inventory result, activations, observed
        # comparisons, candidate port/process identity, and run timestamp.
        evidence = {
            "schema_version": "5.2",
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "candidate_server": {
                "pid": proc.pid,
                "port": port,
                "command": [sys.executable, str(SERVE_SCRIPT), str(port)],
                "cwd": str(EXPLORER_DIR),
            },
            "route_results": results,
        }
        EVIDENCE_PATH.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
        print(f"Evidence saved to {EVIDENCE_PATH}")

        # Report results
        passed = sum(1 for r in results.values() if r["status"] == "PASS")
        failed = sum(1 for r in results.values() if r["status"] == "FAIL")
        errors = sum(1 for r in results.values() if r["status"] == "ERROR")

        print()
        for path, result in sorted(results.items()):
            status = result["status"]
            route_type = result.get("route_type", "unknown")
            if status == "PASS":
                dom = result.get("dom_evidence", {})
                pills = len(dom.get("status_pills", []))
                bindings = len(dom.get("authority_binding", []))
                print(f"  PASS: {path} ({route_type}) - pills={pills}, bindings={bindings}")
            elif status == "FAIL":
                print(f"  FAIL: {path} ({route_type}) - {result.get('reason', 'unknown')}")
                if "binding_errors" in result:
                    for be in result["binding_errors"][:3]:
                        print(f"    binding error: {be.get('error', be)}")
            else:
                print(f"  ERROR: {path} ({route_type}) - {result.get('reason', 'unknown')}")

        print()
        print("=" * 70)
        print(f"Browser DOM Proof V5.2: {passed} passed, {failed} failed, {errors} errors")
        print("=" * 70)
        return 0 if failed == 0 and errors == 0 else 1

    finally:
        stop_server(proc)


if __name__ == "__main__":
    raise SystemExit(main())
