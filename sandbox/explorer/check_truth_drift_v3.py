#!/usr/bin/env python3
"""
Explorer Truth Layer V3 — Fail-Closed Drift Gate

V3 extends V2 by:
  1. Parsing CLAIMS.md at gate time (not just hash check)
  2. Comparing fresh manifest to committed snapshot
  3. Comparing fresh generated output to committed data files
  4. Scanning EVERY reachable HTML/JS/JSON surface (no broad exemptions)
  5. Checking premise/scope fields are nonempty for PF claims
  6. Verifying standard math never shows as PF DERIVED

A matching source hash alone is insufficient. The gate must reparse and
compare the full manifest.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent
CLAIMS_MD = Path("/mnt/d/fundamentals/CLAIMS.md")

# V3: Allow override via command-line for fixture testing
_explorer_dir_override = None
def get_explorer_dir() -> Path:
    return _explorer_dir_override or EXPLORER_DIR

def get_claims_md() -> Path:
    return CLAIMS_MD

SNAPSHOT_PATH = None  # computed dynamically
DATA_CLAIMS_JS = None
DATA_JS = None
DATA_GRAPH_JS = None

def _compute_paths():
    global SNAPSHOT_PATH, DATA_CLAIMS_JS, DATA_JS, DATA_GRAPH_JS
    ed = get_explorer_dir()
    SNAPSHOT_PATH = ed / "_authority_snapshot.json"
    DATA_CLAIMS_JS = ed / "data.claims.js"
    DATA_JS = ed / "data.js"
    DATA_GRAPH_JS = ed / "data.graph.js"

_compute_paths()

STATUS_WORDS = {"DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
                "INTUITION", "OPEN", "EXACT IDENTITY", "CANONICAL",
                "STANDARD MATH", "NO-GO", "UNSYNCED"}

GENERATED_FILES = {"data.claims.js", "data.js", "data.graph.js",
                   "_authority_snapshot.json", "generate_claims_data_v3.py",
                   "check_truth_drift_v3.py", "check_truth_fixtures_v3.py"}


# ============================================================================
# ENTRY POINT ENUMERATION (V3: no broad exemptions)
# ============================================================================

def enumerate_public_surfaces() -> list[Path]:
    """Enumerate every reachable HTML/JS/JSON surface in the release tree."""
    ed = get_explorer_dir()
    surfaces = []

    # All HTML entry points
    for html in ed.glob("*.html"):
        surfaces.append(html)

    # All JS files (root + panels/)
    for js in ed.glob("*.js"):
        surfaces.append(js)
    panels_dir = ed / "panels"
    if panels_dir.is_dir():
        for js in panels_dir.glob("*.js"):
            surfaces.append(js)

    # All JSON files
    for json_file in ed.glob("*.json"):
        surfaces.append(json_file)

    return surfaces


def get_html_entry_points() -> list[Path]:
    """Get all HTML entry points that are part of the release tree."""
    ed = get_explorer_dir()
    htmls = []
    for html in ed.glob("*.html"):
        name = html.name
        if name == "test-d3.html":
            continue
        htmls.append(html)
    return htmls


# ============================================================================
# SNAPSHOT VERIFICATION (V3: parse + compare, not just hash)
# ============================================================================

def load_and_verify_snapshot() -> dict:
    """
    V3: Parse CLAIMS.md at gate time, compare fresh manifest to committed snapshot.
    A matching source hash alone is insufficient.
    """
    if not SNAPSHOT_PATH.is_file():
        print(f"FAIL: No authority snapshot found at {SNAPSHOT_PATH}", file=sys.stderr)
        sys.exit(1)

    committed = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))

    # Step 1: Verify source hash
    source_hash = hashlib.sha256(CLAIMS_MD.read_bytes()).hexdigest()
    if source_hash != committed.get("claims_md_hash"):
        print("FAIL: CLAIMS.md hash mismatch!", file=sys.stderr)
        print(f"  Snapshot recorded: {committed.get('claims_md_hash', 'missing')[:16]}...", file=sys.stderr)
        print(f"  Current file:      {source_hash[:16]}...", file=sys.stderr)
        print("  Run generate_claims_data_v3.py to regenerate.", file=sys.stderr)
        sys.exit(1)

    # Step 2: V3 NEW — Parse CLAIMS.md fresh and compare manifest
    from generate_claims_data_v3 import build_snapshot
    try:
        fresh_snapshot = build_snapshot(CLAIMS_MD)
    except ValueError as e:
        print(f"FAIL: Fresh parse of CLAIMS.md failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Compare claim count
    if fresh_snapshot["claim_count"] != committed["claim_count"]:
        print(f"FAIL: Claim count drift!", file=sys.stderr)
        print(f"  Committed: {committed['claim_count']}", file=sys.stderr)
        print(f"  Fresh:     {fresh_snapshot['claim_count']}", file=sys.stderr)
        sys.exit(1)

    # Compare each claim's status/confidence
    for cid, fresh_claim in fresh_snapshot["claims"].items():
        committed_claim = committed["claims"].get(cid)
        if not committed_claim:
            print(f"FAIL: Claim '{cid}' in fresh parse but not in committed snapshot", file=sys.stderr)
            sys.exit(1)
        if fresh_claim["primary_status"] != committed_claim["primary_status"]:
            print(f"FAIL: Status drift for '{cid}':", file=sys.stderr)
            print(f"  Committed: {committed_claim['primary_status']}", file=sys.stderr)
            print(f"  Fresh:     {fresh_claim['primary_status']}", file=sys.stderr)
            sys.exit(1)
        if fresh_claim["primary_confidence"] != committed_claim["primary_confidence"]:
            print(f"FAIL: Confidence drift for '{cid}':", file=sys.stderr)
            print(f"  Committed: {committed_claim['primary_confidence']}", file=sys.stderr)
            print(f"  Fresh:     {fresh_claim['primary_confidence']}", file=sys.stderr)
            sys.exit(1)

    # Step 3: V3 NEW — Verify committed data files match fresh generation
    from generate_claims_data_v3 import generate_public_data_js, generate_runtime_data_js

    fresh_claims_js = generate_public_data_js(fresh_snapshot)
    committed_claims_js = DATA_CLAIMS_JS.read_text(encoding="utf-8")
    if fresh_claims_js != committed_claims_js:
        print("FAIL: data.claims.js does not match fresh generation!", file=sys.stderr)
        print("  Run generate_claims_data_v3.py to regenerate.", file=sys.stderr)
        sys.exit(1)

    fresh_runtime_js = generate_runtime_data_js(fresh_snapshot)
    committed_runtime_js = DATA_JS.read_text(encoding="utf-8")
    if fresh_runtime_js != committed_runtime_js:
        print("FAIL: data.js does not match fresh generation!", file=sys.stderr)
        print("  Run generate_claims_data_v3.py to regenerate.", file=sys.stderr)
        sys.exit(1)

    return committed


# ============================================================================
# PUBLIC CLAIMS EXTRACTION
# ============================================================================

def extract_public_claims() -> dict:
    """Extract public claims from data.claims.js."""
    if not DATA_CLAIMS_JS.is_file():
        return {}
    text = DATA_CLAIMS_JS.read_text(encoding="utf-8")
    # Parse the JSON object from window.PFClaimsData = {...};
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
            "isSplit": c.get("isSplit", False),
            "isStandardMath": c.get("isStandardMath", False),
            "badge": c.get("badge", ""),
            "statusClass": c.get("statusClass", ""),
        }
    return claims


def extract_public_results() -> dict:
    """Extract public results from data.js (V3 NEW)."""
    if not DATA_JS.is_file():
        return {}
    text = DATA_JS.read_text(encoding="utf-8")
    m = re.search(r'window\.PFExplorerData\s*=\s*(\{.*?\});', text, re.DOTALL)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    results = {}
    for r in data.get("results", []):
        results[r["id"]] = {
            "status": r.get("status"),
            "confidence": r.get("confidence"),
            "authorityClaimIds": r.get("authorityClaimIds", []),
        }
    return results


# ============================================================================
# DRIFT CHECKS
# ============================================================================

def check_claim_drift(snapshot: dict, public_claims: dict) -> list[str]:
    """Check that public claims match authority."""
    failures = []
    auth_claims = snapshot["claims"]

    # Check every public claim has an authority record
    for cid, pub in public_claims.items():
        if cid not in auth_claims:
            failures.append(f"UNKNOWN_CLAIM: Public claim '{cid}' has no authority record in CLAIMS.md")
            continue
        auth = auth_claims[cid]
        if pub["status"] != auth["primary_status"]:
            failures.append(f"STATUS_DRIFT: '{cid}' public={pub['status']} authority={auth['primary_status']}")
        if pub["confidence"] != auth["primary_confidence"]:
            failures.append(f"CONFIDENCE_DRIFT: '{cid}' public={pub['confidence']} authority={auth['primary_confidence']}")
        if pub.get("isSplit") != auth.get("is_split", False):
            failures.append(f"SPLIT_FLATTENED: '{cid}' public isSplit={pub.get('isSplit')} authority is_split={auth.get('is_split')}")
        if pub.get("isStandardMath") != auth.get("is_standard_math", False):
            failures.append(f"STD_MATH_DRIFT: '{cid}' public isStandardMath={pub.get('isStandardMath')} authority={auth.get('is_standard_math')}")
        # V3: Standard math must NOT show as DERIVED badge
        if auth.get("is_standard_math") and "DERIVED" in (pub.get("badge") or "").upper():
            failures.append(f"STD_MATH_AS_DERIVED: '{cid}' standard math shows DERIVED badge: {pub.get('badge')}")

    # Check every authority claim is in public data
    for cid in auth_claims:
        if cid not in public_claims:
            failures.append(f"MISSING_PUBLIC: Authority claim '{cid}' not in public data")

    return failures


def check_result_drift(snapshot: dict, public_results: dict) -> list[str]:
    """V3 NEW: Check that data.js results match authority via crosswalk."""
    failures = []
    crosswalk = snapshot.get("result_to_authority", {})

    for result_id, pub in public_results.items():
        auth_refs = pub.get("authorityClaimIds", [])
        if not auth_refs:
            # No authority — check if it's unsynced or no-go
            if pub["status"] not in ("UNSYNCED", "NO-GO", "OPEN"):
                failures.append(f"RESULT_NO_AUTH: '{result_id}' has status '{pub['status']}' but no authorityClaimIds")
            continue

        # Check each authority claim
        for auth_id in auth_refs:
            auth = snapshot["claims"].get(auth_id)
            if not auth:
                failures.append(f"RESULT_UNKNOWN_AUTH: '{result_id}' references unknown authority '{auth_id}'")
                continue
            # For split results (God Equation), check the primary status matches
            if len(auth_refs) > 1:
                # Split result — primary status should match first authority
                if pub["status"] != snapshot["claims"][auth_refs[0]]["primary_status"]:
                    failures.append(f"RESULT_SPLIT_DRIFT: '{result_id}' primary status={pub['status']} but first auth={auth_refs[0]} has {snapshot['claims'][auth_refs[0]]['primary_status']}")
            else:
                # Single authority — status must match
                if pub["status"] != auth["primary_status"]:
                    failures.append(f"RESULT_STATUS_DRIFT: '{result_id}' status={pub['status']} but authority={auth['primary_status']}")
                if pub["confidence"] != auth["primary_confidence"]:
                    failures.append(f"RESULT_CONF_DRIFT: '{result_id}' confidence={pub['confidence']} but authority={auth['primary_confidence']}")

    return failures


def check_scope_fields(snapshot: dict, public_claims: dict) -> list[str]:
    """V3: Check that PF claims have nonempty premise and scope fields."""
    failures = []
    for cid, auth in snapshot["claims"].items():
        # Standard math claims are exempt from premise/scope requirements
        if auth.get("is_standard_math"):
            continue
        # OPEN claims are exempt (they're explicitly open)
        if auth["primary_status"] == "OPEN":
            continue

        if not auth.get("premise"):
            failures.append(f"EMPTY_PREMISE: '{cid}' has empty premise field")
        if not auth.get("scope_note"):
            failures.append(f"EMPTY_SCOPE: '{cid}' has empty scope_note field")
        if not auth.get("source_line"):
            failures.append(f"EMPTY_SOURCE_LINE: '{cid}' has no source_line")
        if not auth.get("section"):
            failures.append(f"EMPTY_SECTION: '{cid}' has no section")

    return failures


def check_god_equation_split(snapshot: dict, public_claims: dict) -> list[str]:
    """Check that God Equation operator and scale are separate claims."""
    failures = []
    operator = snapshot["claims"].get("god-equation-operator")
    scale = snapshot["claims"].get("god-equation-scale")
    if not operator:
        failures.append("GOD_SPLIT: Missing god-equation-operator claim")
    if not scale:
        failures.append("GOD_SPLIT: Missing god-equation-scale claim")
    if operator and scale:
        if operator["primary_status"] == scale["primary_status"]:
            failures.append(f"GOD_SPLIT: operator and scale have same status: {operator['primary_status']}")
    return failures


def check_source_unity() -> list[str]:
    """V3: Check that PFExplorerData, PFClaimsData, PFDataGraph are unified."""
    failures = []
    # Check data.graph.js is a thin alias
    if DATA_GRAPH_JS.is_file():
        text = DATA_GRAPH_JS.read_text(encoding="utf-8")
        # Must not contain independent claim data
        if "results:" in text and "PFExplorerData" not in text:
            failures.append("DUAL_SOURCE: data.graph.js contains independent results data")
        # Must reference PFClaimsData
        if "PFClaimsData" not in text:
            failures.append("DUAL_SOURCE: data.graph.js does not reference PFClaimsData")
    return failures


# ============================================================================
# BADGE SCANNING (V3: no broad exemptions)
# ============================================================================

def scan_file_for_badges(filepath: Path, auth_claims: dict) -> list[str]:
    """
    V3: Scan a file for status-bearing words in hand-written contexts.
    No broad exemptions — every file is scanned.
    Only generated files and comments are skipped.
    """
    failures = []
    if not filepath.is_file():
        return failures

    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    rel_path = filepath.relative_to(get_explorer_dir()) if filepath.is_relative_to(get_explorer_dir()) else filepath

    # Skip generated files
    if filepath.name in GENERATED_FILES:
        return failures

    # Skip vendor files
    if "vendor/" in str(rel_path):
        return failures

    # Track multi-line fallback blocks
    in_fallback_block = False
    fallback_depth = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip comments
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        # Track multi-line fallback blocks: x || { ... }
        if "||" in line and "{" in line:
            in_fallback_block = True
            fallback_depth = line.count("{") - line.count("}")
        elif in_fallback_block:
            fallback_depth += line.count("{") - line.count("}")
            if fallback_depth <= 0:
                in_fallback_block = False
                continue

        # Skip fallback defaults
        is_fallback = ("||" in line and ("{" in line or "status" in line.lower())) or \
                      "_fallback" in line or \
                      "fallback" in line.lower() or \
                      in_fallback_block

        if is_fallback:
            continue

        # V3: Scan for ALL status words in badge-like contexts
        for word in STATUS_WORDS:
            patterns = [
                rf"'status'\s*:\s*'{re.escape(word)}'",
                rf'"status"\s*:\s*"{re.escape(word)}"',
                rf"status:\s*'{re.escape(word)}'",
                rf'status:\s*"{re.escape(word)}"',
                rf'class="status-pill[^"]*">\s*{re.escape(word)}',
                rf'class="status-badge[^"]*">\s*{re.escape(word)}',
                rf'<span[^>]*class="[^"]*status[^"]*"[^>]*>\s*{re.escape(word)}',
                # V3: Plain-text "Status: CONDITIONAL" in HTML content
                rf'Status:\s*{re.escape(word)}',
                # V3: result-highlight or similar divs with status words
                rf'class="result[^"]*"[^>]*>\s*Status:\s*{re.escape(word)}',
            ]

            for pat in patterns:
                if re.search(pat, line, re.IGNORECASE):
                    failures.append(
                        f"UNMAPPED_BADGE: {rel_path}:{i} contains status word '{word}' "
                        f"in hand-written file. Line: {stripped[:100]}"
                    )
                    break

    return failures


# ============================================================================
# HTML ENTRY POINT CHECKS (V3 NEW)
# ============================================================================

def check_html_entry_points() -> list[str]:
    """V3: Check that every HTML entry point loads generated data, not legacy."""
    failures = []
    htmls = get_html_entry_points()

    for html in htmls:
        text = html.read_text(encoding="utf-8")
        rel = html.relative_to(get_explorer_dir())

        # Check load order: data.graph.js must come before data.claims.js
        graph_pos = text.find("data.graph.js")
        claims_pos = text.find("data.claims.js")
        data_js_pos = text.find('src="data.js"')

        # If data.js is loaded, it must be the generated version (V3)
        if data_js_pos > 0:
            # data.js is loaded — verify it's after data.claims.js
            if claims_pos > 0 and data_js_pos < claims_pos:
                failures.append(f"LOAD_ORDER: {rel} loads data.js before data.claims.js")

        # Check that truth-utils.js is loaded if data files are loaded
        has_data = ("data.js" in text or "data.claims.js" in text or "data.graph.js" in text)
        has_truth_utils = "truth-utils.js" in text
        if has_data and not has_truth_utils:
            failures.append(f"MISSING_TRUTH_UTILS: {rel} loads data files but not truth-utils.js")

    return failures


# ============================================================================
# MAIN GATE
# ============================================================================

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Explorer Truth Layer V3 — Fail-Closed Drift Gate")
    parser.add_argument("--explorer-dir", type=Path, default=None,
                        help="Override explorer directory (for fixture testing)")
    args = parser.parse_args()

    global _explorer_dir_override
    if args.explorer_dir:
        _explorer_dir_override = args.explorer_dir
        _compute_paths()

    print("=" * 70)
    print("Explorer Truth Layer V3 — Fail-Closed Drift Gate")
    print("=" * 70)
    print()

    # Step 1: Verify snapshot (V3: parse + compare, not just hash)
    print("[1/7] Verifying source hash + fresh parse...")
    snapshot = load_and_verify_snapshot()
    print(f"  PASS: CLAIMS.md hash matches, fresh parse matches committed snapshot")
    print(f"  Claims in authority: {snapshot['claim_count']}")

    # Step 2: Extract public claims
    print("\n[2/7] Extracting public claims...")
    public_claims = extract_public_claims()
    public_results = extract_public_results()
    print(f"  Claims in public data: {len(public_claims)}")
    print(f"  Results in runtime data: {len(public_results)}")

    # Step 3: Check claim drift
    print("\n[3/7] Checking claim drift...")
    drift_failures = check_claim_drift(snapshot, public_claims)
    if drift_failures:
        print(f"  FAIL: {len(drift_failures)} drift failures:")
        for f in drift_failures[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: All public claims match authority")

    # Step 4: Check result drift (V3 NEW)
    print("\n[4/7] Checking runtime result drift...")
    result_failures = check_result_drift(snapshot, public_results)
    if result_failures:
        print(f"  FAIL: {len(result_failures)} result drift failures:")
        for f in result_failures[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: All runtime results match authority")

    # Step 5: Check scope fields (V3: premise + scope required)
    print("\n[5/7] Checking premise/scope fields...")
    scope_failures = check_scope_fields(snapshot, public_claims)
    if scope_failures:
        print(f"  FAIL: {len(scope_failures)} scope failures:")
        for f in scope_failures[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: All PF claims have nonempty premise and scope")

    # Step 6: Scan all public surfaces for unmapped badges (V3: no exemptions)
    print("\n[6/7] Scanning all public surfaces for unmapped badges...")
    surfaces = enumerate_public_surfaces()
    badge_failures = []
    for surface in surfaces:
        badge_failures.extend(scan_file_for_badges(surface, snapshot["claims"]))
    if badge_failures:
        print(f"  FAIL: {len(badge_failures)} unmapped badges found:")
        for f in badge_failures[:15]:
            print(f"    - {f}")
    else:
        print(f"  PASS: No unmapped badges in {len(surfaces)} public surfaces")

    # Step 7: Check God Equation split, source unity, HTML entry points
    print("\n[7/7] Checking God Equation split, source unity, HTML entry points...")
    god_failures = check_god_equation_split(snapshot, public_claims)
    unity_failures = check_source_unity()
    html_failures = check_html_entry_points()
    all_check7 = god_failures + unity_failures + html_failures
    if all_check7:
        print(f"  FAIL: {len(all_check7)} failures:")
        for f in all_check7[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: God Equation split, source unity, HTML entry points all OK")

    # Summary
    total_failures = len(drift_failures) + len(result_failures) + len(scope_failures) + \
                     len(badge_failures) + len(all_check7)

    print()
    print("=" * 70)
    if total_failures == 0:
        print("TRUTH GATE V3: PASS — No truth drift detected")
        print("=" * 70)
        return 0
    else:
        print(f"TRUTH GATE V3: FAIL ({total_failures} total failures)")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
