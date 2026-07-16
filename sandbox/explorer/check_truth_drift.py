#!/usr/bin/env python3
"""Truth drift gate: verify data.claims.js matches the authority snapshot.

This gate FAILS when:
1. Any claim in data.claims.js has a status or confidence that doesn't match AUTHORITY_CLAIMS
2. Any forbidden overclaim pattern appears in public-facing files
3. The God Equation operator algebra and λ_c scale formula are conflated
4. Required scope fields (standard_physics, pf_result, pf_open) are missing

Usage:
    python3 check_truth_drift.py

Exit code 0 = PASS (no drift detected)
Exit code 1 = FAIL (drift detected — see output for details)

This gate is part of the Explorer release process. It must pass before
any visual or release gate can clear.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Fix for Windows CLI UnicodeEncodeError
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
SNAPSHOT_PATH = ROOT / "_authority_snapshot.json"
DATA_CLAIMS_PATH = ROOT / "data.claims.js"
INDEX_HTML_PATH = ROOT / "index.html"


def load_snapshot() -> dict:
    if not SNAPSHOT_PATH.exists():
        print(f"FAIL: Authority snapshot not found at {SNAPSHOT_PATH}")
        print("  Run: python3 generate_claims_data.py")
        sys.exit(1)
    return json.loads(SNAPSHOT_PATH.read_text())


def extract_claims_from_js(path: Path) -> dict:
    """Parse data.claims.js and extract claim id → {status, confidence} mapping.

    Uses regex to find claim objects in the CLAIMS array.
    Only searches within the CLAIMS array (not DEFINITIONS).
    """
    content = path.read_text()

    # Extract just the CLAIMS array section to avoid matching definitions
    claims_start = content.find("const CLAIMS = [")
    claims_end = content.find("];", claims_start + 1)
    if claims_start == -1 or claims_end == -1:
        print("FAIL: Could not locate CLAIMS array in data.claims.js")
        return {}

    claims_section = content[claims_start:claims_end]

    # Find all claim objects with id, status, and confidence
    # Pattern: id: "...", ... status: STATUS.XXX, ... confidence: 0.XX
    claims = {}

    # Match claim blocks in the CLAIMS array
    claim_pattern = re.compile(
        r'id:\s*"([^"]+)".*?status:\s*STATUS\.(\w+).*?confidence:\s*([\d.]+)',
        re.DOTALL
    )

    for match in claim_pattern.finditer(claims_section):
        claim_id = match.group(1)
        status = match.group(2)
        confidence = float(match.group(3))
        claims[claim_id] = {
            "status": status,
            "confidence": confidence,
        }

    return claims


def check_claim_drift(snapshot: dict, js_claims: dict) -> list[str]:
    """Check that every claim in data.claims.js matches the authority snapshot."""
    failures = []
    authority = snapshot["claims"]

    for claim_id, js_data in js_claims.items():
        if claim_id not in authority:
            # Unknown claim — not necessarily a failure, but worth noting
            # Only fail if it looks like a status-bearing claim
            continue

        auth = authority[claim_id]
        auth_status = auth["status"]
        auth_confidence = auth["confidence"]

        if js_data["status"] != auth_status:
            failures.append(
                f"  CLAIM '{claim_id}': status DRIFTED\n"
                f"    data.claims.js: {js_data['status']}\n"
                f"    CLAIMS.md:      {auth_status}"
            )

        # Allow confidence to differ by at most 0.01 for float comparison
        if abs(js_data["confidence"] - auth_confidence) > 0.01:
            failures.append(
                f"  CLAIM '{claim_id}': confidence DRIFTED\n"
                f"    data.claims.js: {js_data['confidence']}\n"
                f"    CLAIMS.md:      {auth_confidence}"
            )

    # Check for missing claims (in authority but not in JS)
    for claim_id in authority:
        if claim_id not in js_claims:
            failures.append(
                f"  CLAIM '{claim_id}': MISSING from data.claims.js"
            )

    return failures


def check_forbidden_patterns(snapshot: dict) -> list[str]:
    """Check that no forbidden overclaim patterns appear in public files."""
    failures = []

    for pattern_info in snapshot["forbidden_patterns"]:
        pattern = pattern_info["pattern"]
        reason = pattern_info["reason"]
        files_to_check = pattern_info["files"]

        for file_glob in files_to_check:
            # Handle glob patterns like "panels/*.js"
            if "*" in file_glob:
                paths = list(ROOT.glob(file_glob))
            else:
                paths = [ROOT / file_glob]

            for path in paths:
                if not path.exists():
                    continue

                content = path.read_text()
                matches = re.findall(pattern, content, re.IGNORECASE)

                if matches:
                    failures.append(
                        f"  FORBIDDEN PATTERN '{pattern_info['id']}' in {path.relative_to(ROOT)}\n"
                        f"    Matched: {matches[:3]}\n"
                        f"    Reason: {reason}"
                    )

    return failures


def check_god_equation_split(snapshot: dict) -> list[str]:
    """Verify the God Equation operator algebra and λ_c scale are separate claims."""
    failures = []
    content = DATA_CLAIMS_PATH.read_text()

    # The God Equation entry must NOT contain the λ_c scale formula as part of its claim
    # It should be split into two entries: god-equation (operator algebra) and god-equation-scale
    god_eq_block = re.search(
        r'id:\s*"god-equation".*?(?=id:\s*"|\];|\Z)',
        content,
        re.DOTALL
    )

    if god_eq_block:
        block = god_eq_block.group(0)
        # Check if the λ_c scale formula is in the god-equation block
        if "λ_c" in block or "lambda_c" in block or "1.157" in block or "1.140" in block:
            # It's OK to reference it in openBridge, but the claim field should not conflate
            claim_match = re.search(r'claim:\s*"(.*?)"', block, re.DOTALL)
            if claim_match:
                claim_text = claim_match.group(1)
                if "1.157" in claim_text or "1.140" in claim_text or "1.48%" in claim_text:
                    failures.append(
                        "  GOD EQUATION CONFLATION: The λ_c scale formula (ARGUED 0.60) is mixed into the\n"
                        "  operator algebra claim (CONDITIONAL 0.88). These must be separate entries."
                    )

    # Check that god-equation-scale entry exists
    if 'id: "god-equation-scale"' not in content and "id: 'god-equation-scale'" not in content:
        # Check if the scale formula is at least mentioned somewhere separate
        has_scale = "1.48%" in content or "1.157" in content
        if has_scale:
            # It's mentioned but not as a separate claim — check if it's in the god-equation block
            if god_eq_block:
                block = god_eq_block.group(0)
                if "1.48%" in block or "1.157" in block:
                    failures.append(
                        "  GOD EQUATION SPLIT: The λ_c scale formula (ARGUED 0.60, 1.48% error) appears\n"
                        "  inside the god-equation entry but should be a separate 'god-equation-scale' claim\n"
                        "  with status ARGUED and confidence 0.60."
                    )

    return failures


def check_scope_fields(snapshot: dict, js_claims: dict) -> list[str]:
    """Verify that claims have the three required scope fields."""
    failures = []
    content = DATA_CLAIMS_PATH.read_text()

    # Check for the presence of scope-like fields in the audit objects
    # The current data.claims.js uses audit.standardBoundary, audit.derivedPart, audit.openBridge
    # We need to verify these exist and map to the three required fields

    for claim_id in snapshot["claims"]:
        # Find the claim block
        pattern = re.compile(
            rf'id:\s*"{re.escape(claim_id)}".*?(?=id:\s*"|\];|\Z)',
            re.DOTALL
        )
        match = pattern.search(content)
        if not match:
            continue

        block = match.group(0)

        # Check for required scope fields
        has_standard = "standardBoundary" in block or "standard_physics" in block
        has_pf_result = "derivedPart" in block or "pf_result" in block
        has_pf_open = "openBridge" in block or "pf_open" in block

        if not (has_standard and has_pf_result and has_pf_open):
            missing = []
            if not has_standard:
                missing.append("standard_physics/standardBoundary")
            if not has_pf_result:
                missing.append("pf_result/derivedPart")
            if not has_pf_open:
                missing.append("pf_open/openBridge")
            failures.append(
                f"  CLAIM '{claim_id}': missing scope fields: {', '.join(missing)}"
            )

    return failures


def main():
    print("=== Explorer Truth Drift Gate ===")
    print()

    snapshot = load_snapshot()
    all_failures = []

    # 1. Check data.claims.js exists
    if not DATA_CLAIMS_PATH.exists():
        print(f"FAIL: {DATA_CLAIMS_PATH} not found")
        sys.exit(1)

    # 2. Extract claims from data.claims.js
    js_claims = extract_claims_from_js(DATA_CLAIMS_PATH)
    print(f"Found {len(js_claims)} claims in data.claims.js")
    print(f"Authority snapshot has {len(snapshot['claims'])} claims")
    print()

    # 3. Check claim drift (status + confidence)
    print("--- Claim Status/Confidence Drift ---")
    drift_failures = check_claim_drift(snapshot, js_claims)
    if drift_failures:
        print(f"FAIL: {len(drift_failures)} drift(s) detected:")
        for f in drift_failures:
            print(f)
        all_failures.extend(drift_failures)
    else:
        print("PASS: All claim statuses and confidences match authority")
    print()

    # 4. Check forbidden patterns
    print("--- Forbidden Overclaim Patterns ---")
    pattern_failures = check_forbidden_patterns(snapshot)
    if pattern_failures:
        print(f"FAIL: {len(pattern_failures)} forbidden pattern(s) found:")
        for f in pattern_failures:
            print(f)
        all_failures.extend(pattern_failures)
    else:
        print("PASS: No forbidden overclaim patterns detected")
    print()

    # 5. Check God Equation split
    print("--- God Equation Operator/Scale Split ---")
    split_failures = check_god_equation_split(snapshot)
    if split_failures:
        print(f"FAIL: {len(split_failures)} conflation issue(s):")
        for f in split_failures:
            print(f)
        all_failures.extend(split_failures)
    else:
        print("PASS: God Equation operator algebra and λ_c scale are properly separated")
    print()

    # 6. Check scope fields
    print("--- Required Scope Fields ---")
    scope_failures = check_scope_fields(snapshot, js_claims)
    if scope_failures:
        print(f"FAIL: {len(scope_failures)} missing scope field(s):")
        for f in scope_failures:
            print(f)
        all_failures.extend(scope_failures)
    else:
        print("PASS: All claims have required scope fields")
    print()

    # Summary
    print("=== Summary ===")
    if all_failures:
        print(f"FAIL: {len(all_failures)} total issue(s) detected")
        print()
        print("Fix these in data.claims.js and re-run this gate.")
        print("Do NOT deploy Explorer until this gate passes.")
        sys.exit(1)
    else:
        print("PASS: No truth drift detected. data.claims.js matches authority.")
        sys.exit(0)


if __name__ == "__main__":
    main()
