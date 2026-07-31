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
    false-passed. V5.7 uses a separate expected inventory file, so the
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
    """V5.8: Change one mapping entry to double-quoted JavaScript.

    Codex V57-04: The V5.7 fixture did not assert returncode == 0, so it
    could false-pass on an unrelated failure. V5.8 requires the proof to
    exit 0 and report 45/45 success.

    The proof must PASS because double-quoted entries are semantically
    equivalent and V5.8's parser handles both quote styles.
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

    # V5.8: The proof MUST exit 0 and report 45/45 success
    if proc.returncode != 0:
        raise AssertionError(
            f"Double-quoted entry should parse correctly and proof should PASS; "
            f"got returncode={proc.returncode}, stdout={proc.stdout[-500:]}"
        )
    if "pills=45" not in proc.stdout or "bindings=45" not in proc.stdout:
        raise AssertionError(
            f"Double-quoted entry proof should report 45/45; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: double-quoted mapping entry parsed correctly (exit 0, 45/45)")


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


def fixture_missing_inventory_plus_axiom(tmp_explorer: Path) -> None:
    """V5.8: Delete the expected inventory file AND apply axiom substitution.

    Codex V57-01: With the inventory absent, load_expected_mapping_inventory()
    returned {} and all checks were skipped (if expected_mapping). A mapped
    node returning allowed 'axiom' reason false-passed 45/45.

    V5.8: load_expected_mapping_inventory() raises InventoryError on missing
    file, which is a top-level proof failure before any browser verdict.

    The proof must FAIL — the missing inventory is detected before the
    axiom substitution is even checked.
    """
    inventory_path = tmp_explorer / "expected_node_authority_mapping.json"
    # Delete the inventory file
    if inventory_path.exists():
        inventory_path.unlink()

    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        patched = text.replace(
            "var authId = NODE_TO_AUTHORITY[node.id];",
            "var authId = NODE_TO_AUTHORITY[node.id];\n"
            "    if (node.id === 'fine-structure-alpha') { "
            "return { status: 'OPEN', confidence: null, isAuthority: false, reason: 'axiom' }; }",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # Restore inventory file for subsequent fixtures
    _restore_inventory(tmp_explorer)

    if proc.returncode == 0:
        raise AssertionError(
            f"Missing inventory + axiom fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "inventory" not in proc.stdout.lower():
        raise AssertionError(
            f"Missing inventory fixture did not report inventory error; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: missing inventory + axiom substitution rejected")


def fixture_empty_inventory_plus_axiom(tmp_explorer: Path) -> None:
    """V5.8: Empty the expected inventory AND apply axiom substitution.

    Codex V57-01: With an empty inventory (mappings: {}), all checks were
    skipped. V5.8 raises InventoryError on empty mappings.

    The proof must FAIL.
    """
    inventory_path = tmp_explorer / "expected_node_authority_mapping.json"
    original = inventory_path.read_text(encoding="utf-8")
    # Write an empty inventory
    inventory_path.write_text(json.dumps({"mappings": {}}), encoding="utf-8")

    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        patched = text.replace(
            "var authId = NODE_TO_AUTHORITY[node.id];",
            "var authId = NODE_TO_AUTHORITY[node.id];\n"
            "    if (node.id === 'fine-structure-alpha') { "
            "return { status: 'OPEN', confidence: null, isAuthority: false, reason: 'axiom' }; }",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # Restore inventory
    inventory_path.write_text(original, encoding="utf-8")

    if proc.returncode == 0:
        raise AssertionError(
            f"Empty inventory + axiom fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "inventory" not in proc.stdout.lower() and "empty" not in proc.stdout.lower():
        raise AssertionError(
            f"Empty inventory fixture did not report inventory error; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: empty inventory + axiom substitution rejected")


def fixture_duplicate_mapping_key(tmp_explorer: Path) -> None:
    """V5.8: Add a duplicate mapping key to NODE_TO_AUTHORITY.

    Codex V57-02: Duplicate keys silently collapsed in a Python dict.
    V5.8 detects duplicates and raises MappingParseError.

    The proof must FAIL — the duplicate key is detected.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Add a duplicate of the fine-structure-alpha entry
        patched = text.replace(
            "    'fine-structure-alpha': 'alpha-numeric',",
            "    'fine-structure-alpha': 'alpha-numeric',\n"
            "    'fine-structure-alpha': 'alpha-numeric',",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Duplicate mapping key fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "duplicate" not in proc.stdout.lower() and "Duplicate" not in proc.stdout:
        raise AssertionError(
            f"Duplicate mapping fixture did not report duplicate; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: duplicate mapping key rejected")


def fixture_malformed_mapping_entry(tmp_explorer: Path) -> None:
    """V5.8: Add an unquoted (valid JavaScript but outside accepted grammar)
    mapping entry to NODE_TO_AUTHORITY.

    Codex V57-02: An unquoted JavaScript key is valid in the live renderer
    but was only a parser warning. V5.8 hard-fails on malformed entries.

    The proof must FAIL — the malformed entry is detected.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Add an unquoted key (valid JS but outside our accepted grammar)
        patched = text.replace(
            "    'fine-structure-alpha': 'alpha-numeric',",
            "    'fine-structure-alpha': 'alpha-numeric',\n"
            "    unquoted-key: 'some-claim',",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Malformed mapping entry fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "malformed" not in proc.stdout.lower() and "Malformed" not in proc.stdout:
        raise AssertionError(
            f"Malformed mapping fixture did not report malformed entry; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: malformed mapping entry rejected")


def fixture_same_line_duplicate(tmp_explorer: Path) -> None:
    """V5.9: Add a second identical property on the same JavaScript line.

    Codex V58-01: The V5.8 parser used re.match (prefix), so a valid JS
    line like `'fine-structure-alpha': 'alpha-numeric', 'fine-structure-alpha': 'alpha-numeric'`
    matched the prefix and ignored the trailing duplicate. V5.9 uses
    re.fullmatch after normalizing one trailing comma, so the trailing
    duplicate token causes the line to be classified as malformed.

    The proof must FAIL — the same-line duplicate is detected as malformed.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Add a second identical property on the same line
        patched = text.replace(
            "    'fine-structure-alpha': 'alpha-numeric',",
            "    'fine-structure-alpha': 'alpha-numeric', 'fine-structure-alpha': 'alpha-numeric',",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Same-line duplicate fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "malformed" not in proc.stdout.lower() and "Malformed" not in proc.stdout:
        raise AssertionError(
            f"Same-line duplicate fixture did not report malformed entry; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: same-line duplicate mapping rejected")


def fixture_same_line_unexpected(tmp_explorer: Path) -> None:
    """V5.9: Add an unexpected property on the same JavaScript line.

    Codex V58-01: The V5.8 parser used re.match (prefix), so a valid JS
    line like `'fine-structure-alpha': 'alpha-numeric', 'codex-extra': 'bogus'`
    matched the prefix and ignored the trailing unexpected property.
    V5.9 uses re.fullmatch, so the trailing token causes malformed.

    The proof must FAIL — the same-line unexpected property is detected.
    """
    with _mutate(tmp_explorer, "timeline.js") as panel_path:
        text = panel_path.read_text(encoding="utf-8")
        # Add an unexpected property on the same line
        patched = text.replace(
            "    'fine-structure-alpha': 'alpha-numeric',",
            "    'fine-structure-alpha': 'alpha-numeric', 'codex-extra-node': 'bogus-claim',",
        )
        panel_path.write_text(patched, encoding="utf-8")
        proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    if proc.returncode == 0:
        raise AssertionError(
            f"Same-line unexpected property fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "malformed" not in proc.stdout.lower() and "Malformed" not in proc.stdout:
        raise AssertionError(
            f"Same-line unexpected property fixture did not report malformed; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: same-line unexpected property rejected")


def fixture_missing_expected_count(tmp_explorer: Path) -> None:
    """V5.9: Delete _expected_count from the inventory.

    Codex V58-02: _expected_count was optional (checked only if present).
    Deleting it disabled the count check. V5.9 makes _expected_count
    mandatory — its absence is a hard failure.

    The proof must FAIL — the missing _expected_count is detected.
    """
    inventory_path = tmp_explorer / "expected_node_authority_mapping.json"
    original = inventory_path.read_text(encoding="utf-8")
    data = json.loads(original)
    del data["_expected_count"]
    inventory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # Restore inventory
    inventory_path.write_text(original, encoding="utf-8")

    if proc.returncode == 0:
        raise AssertionError(
            f"Missing _expected_count fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "_expected_count" not in proc.stdout and "expected_count" not in proc.stdout.lower():
        raise AssertionError(
            f"Missing _expected_count fixture did not report the missing field; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: missing _expected_count rejected")


def fixture_missing_version(tmp_explorer: Path) -> None:
    """V5.10: Delete _version from the inventory.

    Codex V59-01: _version was not validated. Deleting it false-passed 45/45.
    V5.10 makes _version mandatory — its absence is a hard failure.

    The proof must FAIL — the missing _version is detected.
    """
    inventory_path = tmp_explorer / "expected_node_authority_mapping.json"
    original = inventory_path.read_text(encoding="utf-8")
    data = json.loads(original)
    del data["_version"]
    inventory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # Restore inventory
    inventory_path.write_text(original, encoding="utf-8")

    if proc.returncode == 0:
        raise AssertionError(
            f"Missing _version fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "_version" not in proc.stdout and "version" not in proc.stdout.lower():
        raise AssertionError(
            f"Missing _version fixture did not report the missing field; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: missing _version rejected")


def fixture_unsupported_version(tmp_explorer: Path) -> None:
    """V5.11: Set _version to an invented V-prefixed value (V99).

    Codex V510-01: The V5.10 check only required a 'V' prefix, so V99
    (an invented version-shaped value) false-passed. V5.11 uses a closed
    supported set, so V99 is rejected.

    The proof must FAIL — V99 is not in the supported set.
    """
    inventory_path = tmp_explorer / "expected_node_authority_mapping.json"
    original = inventory_path.read_text(encoding="utf-8")
    data = json.loads(original)
    data["_version"] = "V99"
    inventory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # Restore inventory
    inventory_path.write_text(original, encoding="utf-8")

    if proc.returncode == 0:
        raise AssertionError(
            f"V99 _version fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "supported" not in proc.stdout.lower() and "version" not in proc.stdout.lower():
        raise AssertionError(
            f"V99 _version fixture did not report unsupported version; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: invented V99 _version rejected")


def fixture_prior_version(tmp_explorer: Path) -> None:
    """V5.11: Set _version to a prior supported version (V5.9).

    Codex V510-01: The V5.10 check only required a 'V' prefix, so V5.9
    (a prior version) false-passed. V5.11 uses a closed supported set
    that does not include V5.9, so it is rejected.

    The proof must FAIL — V5.9 is not in the current supported set.
    """
    inventory_path = tmp_explorer / "expected_node_authority_mapping.json"
    original = inventory_path.read_text(encoding="utf-8")
    data = json.loads(original)
    data["_version"] = "V5.9"
    inventory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # Restore inventory
    inventory_path.write_text(original, encoding="utf-8")

    if proc.returncode == 0:
        raise AssertionError(
            f"V5.9 _version fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "supported" not in proc.stdout.lower() and "version" not in proc.stdout.lower():
        raise AssertionError(
            f"V5.9 _version fixture did not report unsupported version; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: prior V5.9 _version rejected")


def fixture_metadata_tampering(tmp_explorer: Path) -> None:
    """V5.8: Corrupt _expected_count in the inventory.

    Codex V57-03: _expected_count was decorative (never enforced). V5.8
    enforces it. Setting _expected_count=999 must fail.

    _source_hash was removed per the repair contract (it tied the inventory
    to specific timeline.js bytes, preventing legitimate mutation testing).

    The proof must FAIL — the count mismatch is detected.
    """
    inventory_path = tmp_explorer / "expected_node_authority_mapping.json"
    original = inventory_path.read_text(encoding="utf-8")
    # Corrupt _expected_count
    data = json.loads(original)
    data["_expected_count"] = 999
    inventory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    proc = _run_runtime_proof(tmp_explorer, route="derivation.html")

    # Restore inventory
    inventory_path.write_text(original, encoding="utf-8")

    if proc.returncode == 0:
        raise AssertionError(
            f"Metadata tampering fixture should have failed; stdout={proc.stdout[-500:]}"
        )
    if "count" not in proc.stdout.lower() and "mismatch" not in proc.stdout.lower():
        raise AssertionError(
            f"Metadata tampering fixture did not report the count mismatch; stdout={proc.stdout[-500:]}"
        )
    print("  PASS fixture: metadata tampering (_expected_count) rejected")


def _restore_inventory(tmp_explorer: Path) -> None:
    """Restore the expected inventory from the original explorer dir."""
    src = EXPLORER_DIR / "expected_node_authority_mapping.json"
    dst = tmp_explorer / "expected_node_authority_mapping.json"
    if src.exists():
        shutil.copy2(src, dst)


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
        fixture_missing_inventory_plus_axiom(tmp_explorer)
        fixture_empty_inventory_plus_axiom(tmp_explorer)
        fixture_duplicate_mapping_key(tmp_explorer)
        fixture_malformed_mapping_entry(tmp_explorer)
        fixture_same_line_duplicate(tmp_explorer)
        fixture_same_line_unexpected(tmp_explorer)
        fixture_missing_expected_count(tmp_explorer)
        fixture_missing_version(tmp_explorer)
        fixture_unsupported_version(tmp_explorer)
        fixture_prior_version(tmp_explorer)
        fixture_metadata_tampering(tmp_explorer)
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
