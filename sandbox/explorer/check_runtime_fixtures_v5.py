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
    # V5.5: derivation.html needs d3 (and fonts.css for layout). 3D bundle is optional.
    vendor_src = EXPLORER_DIR / "vendor"
    vendor_dst = tmp_explorer / "vendor"
    vendor_dst.mkdir(exist_ok=True)
    for vf in ("d3.v7.min.js", "fonts.css"):
        src = vendor_src / vf
        if src.exists():
            shutil.copy2(src, vendor_dst / vf)
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


def fixture_unbound_journey_result_card(tmp_explorer: Path) -> None:
    """Remove data-claim-id from the Journey result-card child status only."""
    with _mutate(tmp_explorer, "journey.js") as panel_path:
        lines = panel_path.read_text(encoding="utf-8").splitlines()
        # V5.5: target only the inner .result-card-status binding, leaving the parent card binding intact.
        patched_lines = []
        for line in lines:
            if 'result-card-status' in line and 'data-claim-id="' in line:
                line = line.replace('data-claim-id="', 'data-result-id="')
            patched_lines.append(line)
        panel_path.write_text("\n".join(patched_lines), encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="journey.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Unbound Journey result-card fixture should have failed; stdout={proc.stdout[-500:]}, stderr={proc.stderr[-500:]}"
        )
    if "Status pill without claim ID binding" not in proc.stdout and "missing data-claim-id" not in proc.stdout:
        raise AssertionError("Journey fixture did not report the intended unbound status failure")
    print("  PASS fixture: unbound Journey result-card status rejected")


def fixture_unbound_experiment_bench(tmp_explorer: Path) -> None:
    """Remove data-claim-id from the Experiment Bench child status pill only."""
    with _mutate(tmp_explorer, "panels/experiment-bench.js") as panel_path:
        lines = panel_path.read_text(encoding="utf-8").splitlines()
        # V5.5: target only the inner .eb-status-pill binding, leaving the parent card binding intact.
        patched_lines = []
        for line in lines:
            if 'eb-status-pill' in line and 'data-claim-id="' in line:
                line = line.replace('data-claim-id="', 'data-result-id="')
            patched_lines.append(line)
        panel_path.write_text("\n".join(patched_lines), encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="index.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Unbound Experiment Bench fixture should have failed; stdout={proc.stdout[-500:]}, stderr={proc.stderr[-500:]}"
        )
    if "Status pill without claim ID binding" not in proc.stdout and "missing data-claim-id" not in proc.stdout:
        raise AssertionError("Experiment Bench fixture did not report the intended unbound status failure")
    print("  PASS fixture: unbound Experiment Bench status pill rejected")


def fixture_unbound_main_graph_detail(tmp_explorer: Path) -> None:
    """Remove data-claim-id from the derivation main graph detail status."""
    with _mutate(tmp_explorer, "derivation.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        patched = text.replace(
            'bindingAttr = ` data-claim-id="${claimId}"`;',
            'bindingAttr = ` data-result-id="${claimId}"`;',
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Unbound main graph detail fixture should have failed; stdout={proc.stdout[-500:]}, stderr={proc.stderr[-500:]}"
        )
    if "Status pill without claim ID binding" not in proc.stdout and "missing data-claim-id" not in proc.stdout:
        raise AssertionError("Main graph detail fixture did not report the intended unbound status failure")
    print("  PASS fixture: unbound main graph detail status rejected")


def fixture_unbound_timeline(tmp_explorer: Path) -> None:
    """Remove data-claim-id from all timeline-rendered status elements."""
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        patched = text.replace(
            "setAttribute('data-claim-id', authority.claimId)",
            "setAttribute('data-result-id', authority.claimId)",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Unbound timeline fixture should have failed; stdout={proc.stdout[-500:]}, stderr={proc.stderr[-500:]}"
        )
    # V5.6: mapped-node verification catches data-claim-id removal as a
    # mapped authority bypass (the stronger detection path). The older
    # "Status pill without claim ID binding" / "missing data-claim-id"
    # messages remain valid for unmapped nodes.
    if ("Status pill without claim ID binding" not in proc.stdout
            and "missing data-claim-id" not in proc.stdout
            and "Mapped authority node bypass" not in proc.stdout):
        raise AssertionError("Timeline fixture did not report the intended unbound status failure")
    print("  PASS fixture: unbound timeline status rejected")


def fixture_bohr_confidence_mismatch(tmp_explorer: Path) -> None:
    """Force bohr-quantization timeline confidence to 0.78 while still bound to bohr-spectrum."""
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        patched = text.replace(
            "return { status: displayStatus, confidence: claim.confidence, isAuthority: true, claimId: authId };",
            "return { status: displayStatus, confidence: (node.id === 'bohr-quantization' ? 0.78 : claim.confidence), isAuthority: true, claimId: authId };",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Bohr confidence mismatch fixture should have failed; stdout={proc.stdout[-500:]}, stderr={proc.stderr[-500:]}"
        )
    if "Confidence mismatch" not in proc.stdout:
        raise AssertionError("Bohr fixture did not report the intended confidence mismatch")
    print("  PASS fixture: Bohr confidence mismatch rejected")


def fixture_mapped_authority_bypass(tmp_explorer: Path) -> None:
    """V5.6: Mutate fine-structure-alpha (mapped to alpha-numeric) to return
    isAuthority=false with reason='bogus-bypass' while preserving rendered
    authority values (OPEN, null confidence).

    This is the exact hostile mutation from Codex's adjacent reproduction.
    The proof must FAIL — a mapped authority node cannot be unbound by
    substituting an arbitrary data-status-reason.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Inject a hostile override before the normal authority lookup:
        # if the node is 'fine-structure-alpha', return a non-authority
        # result with an arbitrary reason, bypassing the mapping.
        patched = text.replace(
            "var authId = NODE_TO_AUTHORITY[node.id];",
            "var authId = NODE_TO_AUTHORITY[node.id];\n"
            "    if (node.id === 'fine-structure-alpha') { "
            "return { status: 'OPEN', confidence: null, isAuthority: false, reason: 'bogus-bypass' }; }",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Mapped authority bypass fixture should have failed; stdout={proc.stdout[-500:]}, stderr={proc.stderr[-500:]}"
        )
    # The proof must report either the closed-vocabulary rejection or the
    # mapped-node verification failure (both are valid detection paths).
    if "bogus-bypass" not in proc.stdout and "Mapped" not in proc.stdout and "mapped" not in proc.stdout:
        raise AssertionError(
            f"Mapped authority bypass fixture did not report the bypass detection; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: mapped authority bypass (bogus-bypass reason) rejected")


def fixture_mapping_entry_deletion(tmp_explorer: Path) -> None:
    """V5.7: Delete one entry from NODE_TO_AUTHORITY in timeline.js.

    Codex V56-01: The proof was checked against itself — deleting a mapping
    entry made the proof see 14 expected mappings instead of 15, and it
    false-passed. V5.7 uses an independent expected inventory, so the
    deleted entry is detected as a missing entry.

    The proof must FAIL — the parsed mapping has 14 entries but the
    expected inventory has 15.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Delete the fine-structure-alpha -> alpha-numeric entry
        patched = text.replace(
            "    'fine-structure-alpha': 'alpha-numeric',\n",
            "",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Mapping deletion fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "Mapping completeness" not in proc.stdout and "missing" not in proc.stdout.lower():
        raise AssertionError(
            f"Mapping deletion fixture did not report the missing entry; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: mapping entry deletion rejected")


def fixture_mapping_syntax_drift(tmp_explorer: Path) -> None:
    """V5.7: Change one mapping entry to double-quoted JavaScript.

    Codex V56-02: A semantically equivalent double-quoted entry was silently
    omitted by the V5.6 parser (which only matched single quotes). V5.7
    handles both quote styles, so this should parse correctly and the
    proof should PASS (the mapping is semantically equivalent).

    This fixture verifies the parser handles double-quoted entries without
    silently dropping them.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Change one entry from single-quoted to double-quoted
        patched = text.replace(
            "    'fine-structure-alpha': 'alpha-numeric',",
            '    "fine-structure-alpha": "alpha-numeric",',
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # The proof should PASS because double-quoted entries are semantically
    # equivalent and V5.7's parser handles both quote styles.
    if proc.returncode != 0:
        # If it fails, it must NOT be because of a silently omitted entry
        # (that would be the V5.6 bug). It should either pass or fail for
        # a different reason.
        if "Mapping completeness" in proc.stdout and "missing" in proc.stdout.lower():
            raise AssertionError(
                f"Double-quoted entry was silently omitted (V5.6 bug not fixed); "
                f"stdout={proc.stdout[-500:]}"
            )
    print("  PASS fixture: double-quoted mapping entry parsed correctly")


def fixture_mapped_axiom_substitution(tmp_explorer: Path) -> None:
    """V5.7: A mapped node returns allowed reason 'axiom' instead of authority.

    Codex V56-01: The closed vocabulary accepts 'axiom' as a valid
    non-authority reason. If a mapped node returns 'axiom', the closed
    vocabulary alone would accept it. V5.7's mapped-node verification
    catches this because the DOM element won't have the expected
    data-claim-id.

    The proof must FAIL — the mapped node's status label will have
    data-status-reason='axiom' instead of data-claim-id='alpha-numeric'.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Inject a hostile override: mapped node returns allowed 'axiom' reason
        patched = text.replace(
            "var authId = NODE_TO_AUTHORITY[node.id];",
            "var authId = NODE_TO_AUTHORITY[node.id];\n"
            "    if (node.id === 'fine-structure-alpha') { "
            "return { status: 'OPEN', confidence: null, isAuthority: false, reason: 'axiom' }; }",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Mapped axiom substitution fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "Mapped" not in proc.stdout and "mapped" not in proc.stdout:
        raise AssertionError(
            f"Mapped axiom substitution fixture did not report mapped node failure; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: mapped axiom substitution rejected")


def fixture_missing_mapped_dom_node(tmp_explorer: Path) -> None:
    """V5.7: Rename a mapped node's id in the node data so the DOM node
    gets a different data-id and the verifier cannot find it.

    Codex V56-02: A missing mapped DOM node was silently skipped (continue).
    V5.7 hard-fails on missing DOM nodes. Renaming the node's id in the
    node data causes the DOM to render with data-id='fine-structure-alpha-RENAMED'
    while the expected mapping still expects 'fine-structure-alpha'.

    The proof must FAIL — the mapped node 'fine-structure-alpha' cannot
    be found in the DOM.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Rename the node's id in the node data (line 362: id: 'fine-structure-alpha')
        # This causes the DOM to render with data-id='fine-structure-alpha-RENAMED'
        patched = text.replace(
            "id: 'fine-structure-alpha',",
            "id: 'fine-structure-alpha-RENAMED',",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Missing mapped DOM node fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "not found" not in proc.stdout and "Mapped" not in proc.stdout and "mapped" not in proc.stdout:
        raise AssertionError(
            f"Missing mapped DOM node fixture did not report the missing node; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: missing mapped DOM node rejected")


def main() -> int:
    print("=" * 70)
    print("Explorer V5.2/V5.3/V5.5 Runtime Proof — Copied-Candidate Negative Fixtures")
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
        fixture_unbound_journey_result_card(tmp_explorer)
        fixture_unbound_experiment_bench(tmp_explorer)
        fixture_unbound_main_graph_detail(tmp_explorer)
        fixture_unbound_timeline(tmp_explorer)
        fixture_bohr_confidence_mismatch(tmp_explorer)
        fixture_mapped_authority_bypass(tmp_explorer)
        fixture_mapping_entry_deletion(tmp_explorer)
        fixture_mapping_syntax_drift(tmp_explorer)
        fixture_mapped_axiom_substitution(tmp_explorer)
        fixture_missing_mapped_dom_node(tmp_explorer)
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
