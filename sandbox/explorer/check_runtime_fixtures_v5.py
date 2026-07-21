#!/usr/bin/env python3
"""
Explorer Truth Layer V5.2/V5.3 — Runtime Proof Copied-Candidate Negative Fixtures

Per Codex 2026-07-20 V5.2/V5.3 repair contract:
1. Occupied/wrong server port
2. Missing expected rendered state
3. Unbound God Equation primary pill
4. Mismatched claim ID or displayed status (God Equation)
5. Unbound primary Weinberg or Bohr pill
6. Unbound Consciousness audit badge
7. Rendered status that reads UNAVAILABLE / missing
8. Status/confidence mismatch on a non-God-Equation claim

Each fixture reuses one temp copy of the explorer tree, applies a mutation,
runs the copied candidate's own `check_runtime_proof_v5.py`, and asserts it
fails. Mutated files are restored between fixtures. The original worktree hash
is verified before and after.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent


def _hash_tree(root: Path) -> str:
    """Fast hash of covered files: registry, gate scripts, panels, data, html."""
    from check_truth_fixtures_v5 import hash_explorer_tree
    return hash_explorer_tree(root)


def _copy_tree() -> Path:
    tmpdir = Path(tempfile.mkdtemp(prefix="explorer_v52_fixture_", dir="/tmp"))
    tmp_explorer = tmpdir / "explorer"
    shutil.copytree(
        EXPLORER_DIR,
        tmp_explorer,
        ignore=shutil.ignore_patterns(
            "vendor", "__pycache__", "*.pyc", "node_modules", ".git",
            "_visual_pass_screens", "_browser_dom_evidence.json",
        ),
    )
    (tmp_explorer / "vendor").mkdir(exist_ok=True)
    return tmp_explorer


@contextlib.contextmanager
def _mutate(tmp_explorer: Path, rel_path: str):
    """Context manager: mutate a file and restore it on exit."""
    p = tmp_explorer / rel_path
    original = p.read_text(encoding="utf-8")
    try:
        yield p
    finally:
        p.write_text(original, encoding="utf-8")


def _run_runtime_proof(tmp_explorer: Path, route: str = "index.html") -> subprocess.CompletedProcess:
    env = {
        "PYTHONPATH": str(tmp_explorer) + ":" + sys.path[0],
        "PF_RUNTIME_ROUTE": route,
    }
    return subprocess.run(
        [sys.executable, str(tmp_explorer / "check_runtime_proof_v5.py")],
        cwd=str(tmp_explorer),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )


def fixture_occupied_port(tmp_explorer: Path) -> None:
    """Start a server on a fixed port, then run proof with that port occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to all interfaces because serve.py binds to ("", PORT)
        s.bind(("0.0.0.0", 0))
        occupied_port = s.getsockname()[1]
        s.listen(1)

        with _mutate(tmp_explorer, "check_runtime_proof_v5.py") as script:
            text = script.read_text(encoding="utf-8")
            patched = text.replace(
                "def _find_free_port() -> int:",
                "def _find_free_port() -> int:\n    return " + str(occupied_port),
            )
            script.write_text(patched, encoding="utf-8")
            result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Occupied port fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: occupied port rejected")


def fixture_missing_state(tmp_explorer: Path) -> None:
    """Add an inventory entry for a selector that does not exist."""
    with _mutate(tmp_explorer, "release_tree_registry.json") as registry_path:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry.setdefault("statusInventory", []).append({
            "route": "index.html",
            "activation": "[data-route='nonexistent']",
            "selector": ".nonexistent-state-element",
            "claimId": "nonexistent-claim",
            "splitPart": None,
            "expectedStatus": "DERIVED",
            "expectedConfidence": 0.95,
        })
        registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Missing state fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: missing expected rendered state rejected")


def fixture_unbound_god_equation(tmp_explorer: Path) -> None:
    """Remove data-claim-id from the God Equation primary pill."""
    with _mutate(tmp_explorer, "panels/god-equation.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        patched = text.replace(
            'data-claim-id="god-equation-operator">',
            '>',
        )
        panel_path.write_text(patched, encoding="utf-8")
        result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Unbound God Equation fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: unbound God Equation primary pill rejected")


def fixture_mismatched_status(tmp_explorer: Path) -> None:
    """Set inventory expected status to a value that does not match authority."""
    with _mutate(tmp_explorer, "release_tree_registry.json") as registry_path:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for entry in registry.get("statusInventory", []):
            if entry.get("claimId") == "god-equation-operator" and entry.get("splitPart") is None:
                entry["expectedStatus"] = "DERIVED"  # authority is CONDITIONAL
                entry["expectedConfidence"] = 0.99   # authority is 0.88
        registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Mismatched status fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: mismatched status/confidence rejected")


def fixture_unbound_weinberg(tmp_explorer: Path) -> None:
    """Remove data-claim-id from the Weinberg primary pill."""
    with _mutate(tmp_explorer, "panels/weinberg.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Source uses double-quoted JS strings, so the HTML attribute is escaped.
        patched = text.replace(
            'data-claim-id=\\"weinberg-angle\\">',
            '>',
        )
        panel_path.write_text(patched, encoding="utf-8")
        result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Unbound Weinberg fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: unbound Weinberg primary pill rejected")


def fixture_unbound_consciousness_audit(tmp_explorer: Path) -> None:
    """Remove data-claim-id from a Consciousness audit badge."""
    with _mutate(tmp_explorer, "panels/consciousness.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Target the audit note badge, not the primary pill.
        patched = text.replace(
            """The consciousness claim remains <span class="status-badge ' + (consciousness.statusClass || statusToClass(consciousness.status)) + '" data-claim-id="consciousness-claim">""",
            """The consciousness claim remains <span class="status-badge ' + (consciousness.statusClass || statusToClass(consciousness.status)) + '">""",
        )
        panel_path.write_text(patched, encoding="utf-8")
        result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Unbound Consciousness audit fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: unbound Consciousness audit badge rejected")


def fixture_unavailable_status(tmp_explorer: Path) -> None:
    """Force a primary status pill to render as UNAVAILABLE / missing."""
    with _mutate(tmp_explorer, "panels/bohr.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Replace the badge expression so the pill text becomes UNAVAILABLE
        patched = text.replace(
            "var badge = claim ? (claim.badge || claim.status) : 'UNAVAILABLE';",
            "var badge = 'UNAVAILABLE';",
        )
        panel_path.write_text(patched, encoding="utf-8")
        result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Unavailable status fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: rendered UNAVAILABLE status rejected")


def fixture_mismatched_non_god_equation(tmp_explorer: Path) -> None:
    """Set inventory expected status to a value that does not match a non-God-Equation claim."""
    with _mutate(tmp_explorer, "release_tree_registry.json") as registry_path:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for entry in registry.get("statusInventory", []):
            if entry.get("claimId") == "weinberg-angle":
                entry["expectedStatus"] = "DERIVED"  # authority is ARGUED
                entry["expectedConfidence"] = 0.95   # authority is 0.65
        registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        result = _run_runtime_proof(tmp_explorer)

    if result.returncode == 0:
        raise AssertionError(
            f"Mismatched non-God-Equation fixture should have failed; stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"
        )
    print("  PASS fixture: mismatched non-God-Equation status/confidence rejected")


def main() -> int:
    print("=" * 70)
    print("Explorer V5.2/V5.3 Runtime Proof — Copied-Candidate Negative Fixtures")
    print("=" * 70)
    print()

    print("Hashing original explorer worktree...")
    original_hash = _hash_tree(EXPLORER_DIR)
    print(f"  original hash: {original_hash[:16]}...")

    print("Copying explorer tree to temp candidate...")
    tmp_explorer = _copy_tree()
    print(f"  temp: {tmp_explorer}")

    try:
        fixture_occupied_port(tmp_explorer)
        fixture_missing_state(tmp_explorer)
        fixture_unbound_god_equation(tmp_explorer)
        fixture_mismatched_status(tmp_explorer)
        fixture_unbound_weinberg(tmp_explorer)
        fixture_unbound_consciousness_audit(tmp_explorer)
        fixture_unavailable_status(tmp_explorer)
        fixture_mismatched_non_god_equation(tmp_explorer)
    finally:
        shutil.rmtree(tmp_explorer.parent, ignore_errors=True)

    print("Re-hashing original explorer worktree...")
    after_hash = _hash_tree(EXPLORER_DIR)
    if after_hash != original_hash:
        raise AssertionError("Original explorer worktree changed during fixture run")
    print(f"  original hash unchanged: {after_hash[:16]}...")

    print()
    print("All V5.2/V5.3 runtime negative fixtures passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
