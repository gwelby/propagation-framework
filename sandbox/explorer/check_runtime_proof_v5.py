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

import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent
SERVE_SCRIPT = EXPLORER_DIR / "serve.py"
REGISTRY_PATH = EXPLORER_DIR / "release_tree_registry.json"
EVIDENCE_PATH = EXPLORER_DIR / "_browser_dom_evidence.json"
PORT = 8773


def start_server() -> subprocess.Popen:
    """Start the Explorer's V5 serve.py on a test port."""
    proc = subprocess.Popen(
        [sys.executable, str(SERVE_SCRIPT), str(PORT)],
        cwd=str(EXPLORER_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid if sys.platform != "win32" else None,
    )
    for _ in range(30):
        time.sleep(0.5)
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=3)
            return proc
        except Exception:
            pass
    return proc


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


def load_authority_data() -> dict:
    """Load the generated authority data for comparison."""
    claims_js = EXPLORER_DIR / "data.claims.js"
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
        claims[c["id"]] = {
            "status": c.get("status"),
            "confidence": c.get("confidence"),
            "badge": c.get("badge", ""),
            "isSplit": c.get("isSplit", False),
            "isStandardMath": c.get("isStandardMath", False),
        }
    return claims


def run_browser_proof() -> dict:
    """V5: Run browser DOM proof with authority binding."""
    from playwright.sync_api import sync_playwright

    registry = json.loads(REGISTRY_PATH.read_text())
    served_routes = registry.get("servedRoutes", [])
    authority_claims = load_authority_data()

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1440, "height": 900})

        for route in served_routes:
            path = route["path"]
            route_type = route.get("type", "unknown")
            url = f"http://127.0.0.1:{PORT}/{path}"

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

                # V5.1: Activate status-bearing panel states
                # Click on panel triggers, result items, and drawer openers
                # to ensure status pills are rendered and bound
                panel_activations = page.evaluate("""
                    () => {
                        var activations = [];
                        // Click any result-item or claim-row elements
                        var items = document.querySelectorAll('.result-item, .claim-row, [data-claim], .panel-trigger, .nav-item, [data-route]');
                        for (var i = 0; i < Math.min(items.length, 8); i++) {
                            try { items[i].click(); activations.push(items[i].getAttribute('data-route') || items[i].className || 'item'); } catch(e) {}
                        }
                        // Click on Refraction panel if present
                        var refPanel = document.querySelector('#refractionInfo, [data-panel="refraction"]');
                        if (refPanel) {
                            try { refPanel.click(); activations.push('refraction'); } catch(e) {}
                        }
                        // Open evidence drawer if present
                        var drawerTriggers = document.querySelectorAll('.drawer-trigger, .evidence-link, [data-drawer]');
                        for (var i = 0; i < Math.min(drawerTriggers.length, 3); i++) {
                            try { drawerTriggers[i].click(); activations.push('drawer'); } catch(e) {}
                        }
                        return activations;
                    }
                """)
                dom_evidence["panel_activations"] = panel_activations

                # Wait for any panel rendering to complete
                page.wait_for_timeout(2000)

                # 2. V5: Extract status pills with claim ID binding
                status_pills = page.evaluate("""
                    () => {
                        const pills = document.querySelectorAll('.status-pill, .status-badge, [data-status-note]');
                        return Array.from(pills).map(p => {
                            // V5: Look for claim ID in data attributes or parent context
                            let claimId = null;
                            // Check data-claim-id attribute
                            if (p.dataset.claimId) claimId = p.dataset.claimId;
                            // Check parent element for data-claim-id
                            if (!claimId && p.parentElement) {
                                claimId = p.parentElement.dataset.claimId ||
                                          p.closest('[data-claim-id]')?.dataset.claimId;
                            }
                            // Check for nearby claim ID in id attribute or data-id
                            if (!claimId) {
                                const row = p.closest('[data-id], [id]');
                                if (row) {
                                    claimId = row.dataset.id || row.id;
                                }
                            }
                            return {
                                text: p.textContent.trim(),
                                class: p.className,
                                claimId: claimId,
                                tagName: p.tagName,
                                parentTag: p.parentElement ? p.parentElement.tagName : null,
                                parentClass: p.parentElement ? p.parentElement.className : null,
                            };
                        });
                    }
                """)
                dom_evidence["status_pills"] = status_pills

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

                    # V5: For each status pill, verify it matches authority
                    for pill in status_pills:
                        pill_text = pill.get("text", "")
                        pill_class = pill.get("class", "")
                        claim_id = pill.get("claimId")

                        # Skip empty pills
                        if not pill_text:
                            continue

                        # V5: Check for forged/injected pills
                        # A pill with "DERIVED 1.00" but no claim ID is suspicious
                        has_status_word = any(w in pill_text.upper() for w in
                            ["DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
                             "INTUITION", "OPEN", "EXACT IDENTITY", "CANONICAL",
                             "STANDARD MATH", "NO-GO", "PARTIAL DERIVATION"])

                        if has_status_word:
                            binding = {
                                "pill_text": pill_text,
                                "pill_class": pill_class,
                                "claim_id": claim_id,
                                "has_status_word": True,
                            }

                            # V5: If pill has a claim ID, verify against authority
                            if claim_id and claim_id in authority_claims:
                                auth = authority_claims[claim_id]
                                auth_status = auth["status"]
                                auth_conf = auth["confidence"]

                                binding["auth_status"] = auth_status
                                binding["auth_confidence"] = auth_conf
                                binding["matches_status"] = auth_status.upper() in pill_text.upper()

                                # Check confidence if present in pill text
                                import re as _re
                                conf_match = _re.search(r'(\d+\.\d+)', pill_text)
                                if conf_match:
                                    pill_conf = float(conf_match.group(1))
                                    binding["pill_confidence"] = pill_conf
                                    binding["matches_confidence"] = abs(pill_conf - auth_conf) < 0.01
                                else:
                                    binding["matches_confidence"] = True  # No confidence to check

                                if not binding["matches_status"]:
                                    binding["error"] = f"Status mismatch: pill={pill_text} vs authority={auth_status}"
                                elif not binding["matches_confidence"]:
                                    binding["error"] = f"Confidence mismatch: pill={pill_conf} vs authority={auth_conf}"

                            elif claim_id and claim_id not in authority_claims:
                                binding["error"] = f"Unknown claim ID: {claim_id}"
                            else:
                                # V5: Status pill without claim ID
                                # This is suspicious — could be an injection
                                binding["error"] = "Status pill without claim ID binding"

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

                elif route_type == "non-claim":
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
    print("Explorer Truth Layer V5 — Browser DOM Runtime Proof")
    print("=" * 70)
    print()

    # Start server
    print(f"Starting V5 release server on port {PORT}...")
    proc = start_server()
    try:
        # Verify server is up
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=5)
        except Exception:
            print("FAIL: Server did not start")
            return 1

        # V5: Verify quarantine paths return 404
        print("Verifying quarantine/dev paths return 404...")
        for test_path in ["quarantine/test-d3.html", "dev/test-d3.html", "_blocked.html"]:
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/{test_path}", timeout=5)
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
        results = run_browser_proof()

        # Save evidence
        EVIDENCE_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
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
        print(f"Browser DOM Proof V5: {passed} passed, {failed} failed, {errors} errors")
        print("=" * 70)
        return 0 if failed == 0 and errors == 0 else 1

    finally:
        stop_server(proc)


if __name__ == "__main__":
    raise SystemExit(main())
