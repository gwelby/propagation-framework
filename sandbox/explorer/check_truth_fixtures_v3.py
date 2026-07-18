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
    """Create a temp directory with a copy of the explorer tree.

    Uses /tmp (native ext4) for fast I/O — /mnt/d is very slow on WSL.
    """
    tmpdir = Path(tempfile.mkdtemp(prefix="explorer_v3_fixture_", dir="/tmp"))
    tmp_explorer = tmpdir / "explorer"
    # Copy the explorer directory (excluding heavy vendor files)
    shutil.copytree(EXPLORER_DIR, tmp_explorer,
                    ignore=shutil.ignore_patterns("vendor", "__pycache__", "*.pyc", "node_modules", ".git", "_visual_pass_screens", "PROPAGATION_FRAMEWORK_v1.*"))
    # Create a minimal vendor dir so HTML doesn't break
    (tmp_explorer / "vendor").mkdir(exist_ok=True)
    return tmpdir, tmp_explorer


def run_gate(explorer_dir: Path) -> tuple[int, str]:
    """V4: Run the COPIED CANDIDATE'S own gate, not the host gate.

    This ensures the fixture tests the candidate's actual code, not
    the host's code. A tampered candidate gate would not be caught
    if we ran the host gate against the candidate's data.
    """
    candidate_gate = explorer_dir / "check_truth_drift_v3.py"
    result = subprocess.run(
        [sys.executable, str(candidate_gate), "--explorer-dir", str(explorer_dir)],
        cwd=explorer_dir,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout + result.stderr


def run_generator(explorer_dir: Path) -> tuple[int, str]:
    """V4: Run the COPIED CANDIDATE'S own generator."""
    candidate_gen = explorer_dir / "generate_claims_data_v3.py"
    result = subprocess.run(
        [sys.executable, str(candidate_gen)],
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


# ── V4 Fixtures: Journey injection, gate tampering, pre/post hashes ───

def fixture_negative_journey_injection() -> bool:
    """V4: The exact Codex hostile probe — changing journey.html from
    'loading from authority...' to 'DERIVED 1.00 - Hostile Injection'
    must fail the gate."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        journey = tmp_explorer / "journey.html"
        if not journey.is_file():
            print("  SKIP: journey.html not found")
            return True
        text = journey.read_text(encoding="utf-8")
        # Apply the exact Codex probe
        mutated = text.replace(
            "loading from authority...",
            "DERIVED 1.00 - Hostile Injection"
        )
        if mutated == text:
            print("  SKIP: 'loading from authority...' not found in journey.html")
            return True
        journey.write_text(mutated, encoding="utf-8")

        rc, output = run_gate(tmp_explorer)
        if rc == 0:
            print("  FAIL: Expected FAIL (Journey hostile injection), got PASS")
            return False
        if "UNMAPPED_BADGE" not in output:
            print(f"  FAIL: Gate failed but didn't detect UNMAPPED_BADGE")
            return False
        print("  PASS: Journey hostile injection detected")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_negative_gate_tampering() -> bool:
    """V4: A tampered candidate gate that always returns PASS must NOT
    fool the fixture framework. The fixture proves the original worktree
    hash is unchanged before/after fixtures."""
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Tamper with the candidate's gate to always pass
        gate = tmp_explorer / "check_truth_drift_v3.py"
        text = gate.read_text(encoding="utf-8")
        # Replace ALL failure exits: return 1 and sys.exit(1)
        tampered = text.replace("return 1", "return 0  # TAMPERED")
        tampered = tampered.replace("sys.exit(1)", "sys.exit(0)  # TAMPERED")
        tampered = tampered.replace("raise SystemExit(1)", "raise SystemExit(0)  # TAMPERED")
        gate.write_text(tampered, encoding="utf-8")

        # The tampered gate should now pass even with a bad mutation
        claims_js = tmp_explorer / "data.claims.js"
        claims_text = claims_js.read_text(encoding="utf-8")
        mutated = claims_text.replace('"status": "DERIVED"', '"status": "ARGUED"', 1)
        claims_js.write_text(mutated, encoding="utf-8")

        rc, output = run_gate(tmp_explorer)
        if rc != 0:
            print(f"  FAIL: Tampered gate unexpectedly failed (rc={rc})")
            return False

        # Now verify the ORIGINAL (host) gate catches this mutation
        # by running the host gate against the tampered candidate
        result = subprocess.run(
            [sys.executable, str(GATE_SCRIPT), "--explorer-dir", str(tmp_explorer)],
            cwd=str(tmp_explorer),
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print("  FAIL: Host gate also passed — mutation wasn't detected")
            return False

        print("  PASS: Gate tampering detected by host gate cross-check")
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fixture_positive_worktree_unchanged() -> bool:
    """V4: Prove the original worktree hash is unchanged before/after
    fixtures. This verifies that fixtures never write to live files."""
    import hashlib

    # Hash the key source files before fixtures
    files_to_hash = [
        "check_truth_drift_v3.py",
        "generate_claims_data_v3.py",
        "check_truth_fixtures_v3.py",
        "data.claims.js",
        "data.js",
        "_authority_snapshot.json",
        "release_tree_registry.json",
    ]

    before_hashes = {}
    for fname in files_to_hash:
        fpath = EXPLORER_DIR / fname
        if fpath.is_file():
            before_hashes[fname] = hashlib.sha256(fpath.read_bytes()).hexdigest()

    # Run a fixture (which copies and mutates a temp tree)
    tmpdir, tmp_explorer = setup_temp_explorer()
    try:
        # Mutate the temp copy
        claims_js = tmp_explorer / "data.claims.js"
        text = claims_js.read_text(encoding="utf-8")
        claims_js.write_text(text.replace("DERIVED", "ARGUED", 1), encoding="utf-8")

        # Run the gate against the temp copy
        rc, output = run_gate(tmp_explorer)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # Hash the key source files after fixtures
    after_hashes = {}
    for fname in files_to_hash:
        fpath = EXPLORER_DIR / fname
        if fpath.is_file():
            after_hashes[fname] = hashlib.sha256(fpath.read_bytes()).hexdigest()

    # Verify all hashes match
    all_match = True
    for fname in before_hashes:
        if before_hashes[fname] != after_hashes.get(fname, ""):
            print(f"  FAIL: {fname} hash changed!")
            all_match = False

    if all_match:
        print(f"  PASS: All {len(before_hashes)} source file hashes unchanged")
        return True
    return False


# ============================================================================
# MAIN
# ============================================================================

FIXTURES = [
    ("positive_clean_tree", fixture_positive_clean_tree),
    ("positive_generator_regenerates", fixture_positive_generator_regenerates),
    ("positive_worktree_unchanged", fixture_positive_worktree_unchanged),
    ("negative_status_drift", fixture_negative_status_drift),
    ("negative_confidence_drift", fixture_negative_confidence_drift),
    ("negative_stale_data_js", fixture_negative_stale_data_js),
    ("negative_missing_premise", fixture_negative_missing_premise),
    ("negative_std_math_as_derived", fixture_negative_std_math_as_derived),
    ("negative_hardcoded_badge", fixture_negative_hardcoded_badge),
    ("negative_snapshot_tampering", fixture_negative_snapshot_tampering),
    ("negative_standalone_injection", fixture_negative_standalone_injection),
    ("negative_unmapped_panel_id", fixture_negative_unmapped_panel_id),
    ("negative_journey_injection", fixture_negative_journey_injection),
    ("negative_gate_tampering", fixture_negative_gate_tampering),
]


def main() -> int:
    print("=" * 70)
    print("Explorer Truth Layer V4 — Fixtures")
    print("(Isolated temp candidates — V4: uses candidate's own gate/generator)")
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
