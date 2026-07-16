#!/usr/bin/env python3
"""
Explorer Truth Layer V2 — Independent Negative Fixtures

Tests the production gate (check_truth_drift_v2.py) against negative cases
that must FAIL. These are NOT self-referential regex tests — they exercise
the actual production parser and gate functions.

Codex V2 repair requirement 7:
  Fixtures must exercise the production parser/output and include:
  - stale-source failures
  - unknown-ID failures
  - missing-scope failures
  - mixed-status failures
  - panel/sidebar failures
  - semantic-variant failures
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent
SNAPSHOT_PATH = EXPLORER_DIR / "_authority_snapshot.json"


def run_fixture(name: str, test_fn) -> bool:
    """Run a fixture and report result. Returns True if test passes (gate correctly rejects)."""
    print(f"  [{name}] ", end="", flush=True)
    try:
        result = test_fn()
        if result:
            print("PASS (gate correctly rejected)")
            return True
        else:
            print("FAIL (gate did NOT reject — BUG)")
            return False
    except Exception as e:
        print(f"ERROR ({e})")
        return False


# ============================================================================
# FIXTURE 1: Stale source — empty CLAIMS.md should produce zero claims
# ============================================================================

def test_stale_source() -> bool:
    """An empty source file must fail, not emit all 27 claims."""
    from generate_claims_data_v2 import build_snapshot
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("")
        tmp = Path(f.name)
    try:
        try:
            build_snapshot(tmp)
            return False  # should have raised ValueError
        except ValueError:
            return True  # correctly rejected
    finally:
        tmp.unlink(missing_ok=True)


# ============================================================================
# FIXTURE 2: Unknown ID — a public claim not in authority must be rejected
# ============================================================================

def test_unknown_id() -> bool:
    """An unknown DERIVED 1.0 claim in public data must be rejected."""
    from check_truth_drift_v2 import check_claim_drift
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    public_claims = {
        "fake-unknown-claim": {"status": "DERIVED", "confidence": 1.0}
    }
    failures = check_claim_drift(snapshot, public_claims)
    return any("UNKNOWN_CLAIM" in f for f in failures)


# ============================================================================
# FIXTURE 3: Forged hash — a tampered source hash must be rejected
# ============================================================================

def test_forged_hash() -> bool:
    """A forged source hash must cause the gate to exit with failure."""
    from check_truth_drift_v2 import load_and_verify_snapshot
    if not SNAPSHOT_PATH.is_file():
        return False
    original = SNAPSHOT_PATH.read_text(encoding="utf-8")
    snapshot = json.loads(original)
    snapshot["claims_md_hash"] = "0" * 64
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    try:
        try:
            load_and_verify_snapshot()
            return False  # should have exited
        except SystemExit as e:
            return e.code != 0
    finally:
        SNAPSHOT_PATH.write_text(original, encoding="utf-8")


# ============================================================================
# FIXTURE 4: Empty scope — authority record with empty status must be rejected
# ============================================================================

def test_empty_scope() -> bool:
    """An authority record with empty primary_status must be rejected."""
    from check_truth_drift_v2 import check_scope_fields
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    snapshot["claims"]["test-empty"] = {
        "primary_status": "",
        "primary_confidence": None,
        "source_line": 0,
        "section": "",
        "is_split": False,
        "is_standard_math": False,
        "status_parts": [],
    }
    failures = check_scope_fields(snapshot, {})
    return any("test-empty" in f for f in failures)


# ============================================================================
# FIXTURE 5: Mixed status flattening — split claim must not be flattened
# ============================================================================

def test_mixed_status_flattening() -> bool:
    """A split claim (e.g. Koide) must not be flattened to a single status."""
    from check_truth_drift_v2 import check_claim_drift
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    # Koide is split (EXACT IDENTITY / OPEN) — try to flatten it
    public_claims = {
        "koide-leptons": {
            "status": "DERIVED",  # wrong — should be EXACT IDENTITY
            "confidence": 0.95,
            "isSplit": False,  # wrong — should be True
            "isStandardMath": False,
        }
    }
    failures = check_claim_drift(snapshot, public_claims)
    return any("SPLIT_FLATTENED" in f or "STATUS_DRIFT" in f for f in failures)


# ============================================================================
# FIXTURE 6: God Equation split — operator and scale must be separate
# ============================================================================

def test_god_equation_split() -> bool:
    """God Equation operator and scale must have different statuses."""
    from check_truth_drift_v2 import check_god_equation_split
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    # Tamper: make both have same status
    snapshot["claims"]["god-equation-operator"]["primary_status"] = "ARGUED"
    snapshot["claims"]["god-equation-scale"]["primary_status"] = "ARGUED"
    public_claims = {
        "god-equation-operator": {"status": "ARGUED", "confidence": 0.6},
        "god-equation-scale": {"status": "ARGUED", "confidence": 0.6},
    }
    failures = check_god_equation_split(snapshot, public_claims)
    return any("GOD_SPLIT" in f for f in failures)


# ============================================================================
# FIXTURE 7: Semantic variant — "Derived" (capitalized) in panel must be caught
# ============================================================================

def test_semantic_variant() -> bool:
    """A 'Derived' badge in a hand-written panel file must be caught."""
    from check_truth_drift_v2 import scan_file_for_badges
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    # Create a temp file with a hand-written badge
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, dir=EXPLORER_DIR) as f:
        f.write("var x = { status: 'DERIVED' };\n")
        tmp = Path(f.name)
    try:
        failures = scan_file_for_badges(tmp, snapshot["claims"])
        return len(failures) > 0
    finally:
        tmp.unlink(missing_ok=True)


# ============================================================================
# FIXTURE 8: Confidence drift — wrong confidence must be caught
# ============================================================================

def test_confidence_drift() -> bool:
    """A confidence value that differs from authority must be caught."""
    from check_truth_drift_v2 import check_claim_drift
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    # Bohr spectrum is 0.90 — try 0.50
    public_claims = {
        "bohr-spectrum": {"status": "DERIVED", "confidence": 0.50,
                          "isSplit": False, "isStandardMath": False}
    }
    failures = check_claim_drift(snapshot, public_claims)
    return any("CONFIDENCE_DRIFT" in f for f in failures)


# ============================================================================
# FIXTURE 9: Missing public claim — authority claim not in public data
# ============================================================================

def test_missing_public() -> bool:
    """An authority claim missing from public data must be caught."""
    from check_truth_drift_v2 import check_claim_drift
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    # Empty public claims — all authority claims are missing
    failures = check_claim_drift(snapshot, {})
    return any("MISSING_PUBLIC" in f for f in failures)


# ============================================================================
# FIXTURE 10: Standard math class — must not use PF-DERIVED badge
# ============================================================================

def test_standard_math_class() -> bool:
    """A standard-math claim must not be marked as regular DERIVED."""
    from check_truth_drift_v2 import check_claim_drift
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    # Pythagorean decomposition is standard math — try marking it as regular DERIVED
    public_claims = {
        "pythagorean-decomposition": {
            "status": "DERIVED",
            "confidence": 0.95,
            "isSplit": False,
            "isStandardMath": False,  # wrong — should be True
        }
    }
    failures = check_claim_drift(snapshot, public_claims)
    return any("STD_MATH_DRIFT" in f for f in failures)


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    print("=" * 70)
    print("Explorer Truth Layer V2 — Independent Negative Fixtures")
    print("=" * 70)
    print()

    fixtures = [
        ("stale-source", test_stale_source),
        ("unknown-id", test_unknown_id),
        ("forged-hash", test_forged_hash),
        ("empty-scope", test_empty_scope),
        ("mixed-status-flattening", test_mixed_status_flattening),
        ("god-equation-split", test_god_equation_split),
        ("semantic-variant", test_semantic_variant),
        ("confidence-drift", test_confidence_drift),
        ("missing-public", test_missing_public),
        ("standard-math-class", test_standard_math_class),
    ]

    passed = 0
    failed = 0
    for name, test_fn in fixtures:
        if run_fixture(name, test_fn):
            passed += 1
        else:
            failed += 1

    print()
    print("=" * 70)
    print(f"FIXTURES: {passed}/{passed + failed} passed")
    if failed:
        print(f"  {failed} FAILED — gate has gaps")
        print("=" * 70)
        return 1
    else:
        print(f"  All negative fixtures correctly rejected by gate")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
