#!/usr/bin/env python3
"""
Explorer Truth Layer V3 — Fixtures

V3 requirement 6: Fixtures run the command-line gate against an isolated
temp candidate directory. They NEVER write to live files.

Each fixture:
  1. Creates a temp directory
  2. Copies the explorer tree
  3. Applies a mutation (drift, missing field, etc.)
  4. Runs the gate against the temp copy
  5. Asserts the gate FAILS (for negative fixtures) or PASSES (for positive)
  6. Cleans up the temp directory
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent
GATE_SCRIPT = EXPLORER_DIR / "check_truth_drift_v3.py"
GENERATOR_SCRIPT = EXPLORER_DIR / "generate_claims_data_v3.py"
CLAIMS_MD = Path("/mnt/d/fundamentals/CLAIMS.md")


def setup_temp_explorer() -> tuple[Path, Path]:
    """Create a temp directory with a copy of the explorer tree."""
    tmpdir = Path(tempfile.mkdtemp(prefix="explorer_v3_fixture_"))
    tmp_explorer = tmpdir / "explorer"
    # Copy the explorer directory (excluding heavy vendor files)
    shutil.copytree(EXPLORER_DIR, tmp_explorer,
                    ignore=shutil.ignore_patterns("vendor", "__pycache__", "*.pyc", "node_modules"))
    # Create a minimal vendor dir so HTML doesn't break
    (tmp_explorer / "vendor").mkdir(exist_ok=True)
    return tmpdir, tmp_explorer


def run_gate(explorer_dir: Path) -> tuple[int, str]:
    """Run the V3 gate against the given explorer directory."""
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), "--explorer-dir", str(explorer_dir)],
        cwd=explorer_dir,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout + result.stderr


def run_generator(explorer_dir: Path) -> tuple[int, str]:
    """Run the V3 generator against the given explorer directory."""
    result = subprocess.run(
        [sys.executable, str(GENERATOR_SCRIPT)],
        cwd=explorer_dir,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout + result.stderr


# ============================================================================
# FIXTURES
# ============================================================================

def fixture_positive_clean_tree() -> bool:
    """POSITIVE: Clean tree should pass the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        rc, output = run_gate(tmp_explorer)
        if rc != 0:
            print(f"  FAIL: Expected PASS, got FAIL")
            print(f"  Output: {output[:500]}")
            return False
        print("  PASS: Clean tree passes gate")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_status_drift() -> bool:
    """NEGATIVE: Changing a status in data.claims.js should fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Mutate data.claims.js: change a status
        claims_js = tmp_explorer / "data.claims.js"
        text = claims_js.read_text()
        # Change bohr-spectrum from DERIVED to ARGUED
        mutated = text.replace('"status": "DERIVED"', '"status": "ARGUED"', 1)
        claims_js.write_text(mutated)

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (status drift), got PASS")
            return False
        if "STATUS_DRIFT" not in output and "does not match fresh generation" not in output:
            print(f"  FAIL: Gate failed but didn't detect status drift")
            print(f"  Output: {output[:500]}")
            return False
        print("  PASS: Status drift detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_confidence_drift() -> bool:
    """NEGATIVE: Changing a confidence value should fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        claims_js = tmp_explorer / "data.claims.js"
        text = claims_js.read_text()
        # Change a confidence value
        mutated = text.replace('"confidence": 0.9,', '"confidence": 0.95,', 1)
        claims_js.write_text(mutated)

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (confidence drift), got PASS")
            return False
        print("  PASS: Confidence drift detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_stale_data_js() -> bool:
    """NEGATIVE: Stale data.js (not regenerated) should fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Mutate data.js: change a status
        data_js = tmp_explorer / "data.js"
        text = data_js.read_text()
        mutated = text.replace('"status": "DERIVED"', '"status": "ARGUED"', 1)
        data_js.write_text(mutated)

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (stale data.js), got PASS")
            return False
        if "data.js does not match" not in output and "RESULT_STATUS_DRIFT" not in output:
            print(f"  FAIL: Gate failed but didn't detect stale data.js")
            print(f"  Output: {output[:500]}")
            return False
        print("  PASS: Stale data.js detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_missing_premise() -> bool:
    """NEGATIVE: Empty premise field should fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Mutate snapshot: clear a premise field
        snapshot_path = tmp_explorer / "_authority_snapshot.json"
        snapshot = json.loads(snapshot_path.read_text())
        first_claim = list(snapshot["claims"].keys())[0]
        snapshot["claims"][first_claim]["premise"] = ""
        snapshot_path.write_text(json.dumps(snapshot, indent=2))

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (empty premise), got PASS")
            return False
        if "EMPTY_PREMISE" not in output:
            print(f"  FAIL: Gate failed but didn't detect empty premise")
            return False
        print("  PASS: Empty premise detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_std_math_as_derived() -> bool:
    """NEGATIVE: Standard math showing as DERIVED should fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Mutate data.claims.js: change a standard math badge to DERIVED
        claims_js = tmp_explorer / "data.claims.js"
        text = claims_js.read_text()
        # Find pythagorean-decomposition and change its badge
        if "STANDARD MATH" in text:
            mutated = text.replace('"badge": "STANDARD MATH', '"badge": "DERIVED', 1)
            claims_js.write_text(mutated)

            rc, output = run_gate(tmp_explorer)
            if rc == 0:
                print("  FAIL: Expected FAIL (std math as DERIVED), got PASS")
                return False
            print("  PASS: Standard math as DERIVED detected")
            return True
        else:
            print("  SKIP: No STANDARD MATH badge found in data.claims.js")
            return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_positive_generator_regenerates() -> bool:
    """POSITIVE: Running the generator should produce identical output."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Read original files
        orig_claims = (tmp_explorer / "data.claims.js").read_text()
        orig_data = (tmp_explorer / "data.js").read_text()

        # Run generator
        rc, output = run_generator(tmp_explorer)
        if rc != 0:
            print(f"  FAIL: Generator failed: {output[:300]}")
            return False

        # Compare
        new_claims = (tmp_explorer / "data.claims.js").read_text()
        new_data = (tmp_explorer / "data.js").read_text()

        if new_claims != orig_claims:
            print("  FAIL: Generator produced different data.claims.js")
            return False
        if new_data != orig_data:
            print("  FAIL: Generator produced different data.js")
            return False

        print("  PASS: Generator produces identical output")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_hardcoded_badge() -> bool:
    """NEGATIVE: Adding a hardcoded status badge should fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Add a hardcoded badge to a panel file
        panel_js = tmp_explorer / "panels" / "foundations.js"
        text = panel_js.read_text()
        # Insert a hardcoded status badge
        mutated = text + '\n// V3 fixture injection\nvar _test = \'<span class="status-pill status-derived">DERIVED</span>\';\n'
        panel_js.write_text(mutated)

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (hardcoded badge), got PASS")
            return False
        if "UNMAPPED_BADGE" not in output:
            print(f"  FAIL: Gate failed but didn't detect hardcoded badge")
            return False
        print("  PASS: Hardcoded badge detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_snapshot_tampering() -> bool:
    """NEGATIVE: Tampering both snapshot and public data while keeping CLAIMS.md
    hash unchanged must fail the gate (Codex V2 finding #3)."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        import hashlib
        # Read current snapshot and data.claims.js
        snapshot = json.loads((tmp_explorer / "_authority_snapshot.json").read_text())
        claims_js = (tmp_explorer / "data.claims.js").read_text()

        # Forge: change Weinberg from ARGUED 0.65 to DERIVED 0.90 in snapshot
        if "weinberg-angle" in snapshot["claims"]:
            snapshot["claims"]["weinberg-angle"]["primary_status"] = "DERIVED"
            snapshot["claims"]["weinberg-angle"]["primary_confidence"] = 0.90
        # Also forge in data.claims.js
        forged_claims = claims_js.replace(
            '"status": "ARGUED", "confidence": 0.65',
            '"status": "DERIVED", "confidence": 0.90'
        )
        # Write forged files (but keep CLAIMS.md unchanged)
        (tmp_explorer / "_authority_snapshot.json").write_text(json.dumps(snapshot, indent=2))
        (tmp_explorer / "data.claims.js").write_text(forged_claims)

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (snapshot tampering), got PASS")
            return False
        # Gate should detect either drift or hash mismatch
        if "FAIL" not in output and "drift" not in output.lower() and "mismatch" not in output.lower():
            print(f"  FAIL: Gate failed but didn't report tampering")
            return False
        print("  PASS: Snapshot+public tampering detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_standalone_injection() -> bool:
    """NEGATIVE: A standalone HTML page with a hardcoded status badge should
    fail the gate (Codex V2 finding #2 — journey.html had Status: CONDITIONAL)."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Create a standalone HTML page with a hardcoded status
        fake_page = tmp_explorer / "test-injection.html"
        fake_page.write_text("""<!DOCTYPE html>
<html><head><title>Test</title></head>
<body>
<div class="result-highlight">Status: DERIVED 0.99 • fake claim</div>
</body></html>""")

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (standalone injection), got PASS")
            return False
        if "UNMAPPED_BADGE" not in output or "test-injection" not in output:
            print(f"  FAIL: Gate failed but didn't detect standalone injection")
            return False
        print("  PASS: Standalone page injection detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_unmapped_panel_id() -> bool:
    """NEGATIVE: A runtime result with an authorityClaimIds reference to a
    non-existent claim should fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Forge data.js to include a result with an unmapped panel ID
        data_js = (tmp_explorer / "data.js").read_text()
        # Add a fake result with an unmapped authority claim ID
        if '"results":' in data_js:
            forged = data_js.replace(
                '"results":',
                '"results": [{"id": "fake-claim", "title": "Fake", "status": "DERIVED", "confidence": 0.99, "authorityClaimIds": ["nonexistent-id"]},'
            )
            (tmp_explorer / "data.js").write_text(forged)

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (unmapped panel ID), got PASS")
            return False
        if "FAIL" not in output:
            print(f"  FAIL: Gate failed but didn't report unmapped ID")
            return False
        print("  PASS: Unmapped panel ID detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ============================================================================
# MAIN
# ============================================================================

FIXTURES = [
    ("positive_clean_tree", fixture_positive_clean_tree),
    ("positive_generator_regenerates", fixture_positive_generator_regenerates),
    ("negative_status_drift", fixture_negative_status_drift),
    ("negative_confidence_drift", fixture_negative_confidence_drift),
    ("negative_stale_data_js", fixture_negative_stale_data_js),
    ("negative_missing_premise", fixture_negative_missing_premise),
    ("negative_std_math_as_derived", fixture_negative_std_math_as_derived),
    ("negative_hardcoded_badge", fixture_negative_hardcoded_badge),
    ("negative_snapshot_tampering", fixture_negative_snapshot_tampering),
    ("negative_standalone_injection", fixture_negative_standalone_injection),
    ("negative_unmapped_panel_id", fixture_negative_unmapped_panel_id),
]


def main() -> int:
    print("=" * 70)
    print("Explorer Truth Layer V3 — Fixtures")
    print("(Isolated temp candidates — never writes live files)")
    print("=" * 70)
    print()

    passed = 0
    failed = 0

    for name, fn in FIXTURES:
        print(f"[{name}]")
        try:
            if fn():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
        print()

    print("=" * 70)
    print(f"Fixtures: {passed} passed, {failed} failed, {len(FIXTURES)} total")
    print("=" * 70)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
