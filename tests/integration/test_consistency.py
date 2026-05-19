"""Integration tests: pipeline consistency invariants (Task 10.2).

Each test asserts one cross-cutting invariant:

    * ``test_no_dependency_clear_when_upstream_open`` —
      :func:`summarize_dependency_state` never emits ``CLEAR`` for a
      downstream claim when any explicit upstream is HYPOTHESIS_OPEN.
    * ``test_all_five_falsification_tests_have_valid_readouts`` —
      :class:`FalsificationPipeline.run_all` always produces exactly
      five records (TEST_1..TEST_5) with readouts drawn from
      :class:`FalsificationReadout`. Sandbox runners are monkey-patched
      so the test does not depend on the real ``sandbox/`` scripts.
    * ``test_gap_report_includes_all_gaps`` — every unique ``gaps_found``
      entry produced across the pipeline run appears in the rendered
      gap report text.
    * ``test_cascade_report_includes_transitive_dependents`` — for an
      upstream claim with a multi-hop cascade, every transitive
      downstream id shows up in the rendered cascade report line.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md` Req. 7, 9.
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 10.2.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from verification.claim_graph import ClaimGraph
from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.falsification.pipeline import FalsificationPipeline
from verification.models import (
    Claim,
    ClaimStatus,
    DependencyEdge,
    VerificationOutcome,
    VerificationResult,
)
from verification.pipeline import (
    run_verification_pipeline,
    summarize_dependency_state,
)
from verification.report import (
    generate_cascade_report,
    generate_gap_report,
)
from verification.sandbox_runner import SandboxRunResult


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLAIMS_MD = REPO_ROOT / "CLAIMS.md"
OVERLAY = REPO_ROOT / "verification" / "dependency_overlay.yaml"
MANIFEST = REPO_ROOT / "verification" / "support_manifest.yaml"
AGENTS_MD = REPO_ROOT / "AGENTS.md"


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_claim(
    claim_id: str,
    *,
    status: ClaimStatus = ClaimStatus.DERIVED,
    confidence: float = 0.95,
) -> Claim:
    return Claim(
        id=claim_id,
        name=claim_id.replace("_", " ").title(),
        status=status,
        confidence=confidence,
        evidence_summary="(fixture)",
        falsification_criterion="(fixture)",
        derivation_files=[],
        audited_derivation_refs=[],
        sandbox_scripts=[],
        named_hypotheses=[],
        known_gaps=[],
        source_row=0,
    )


def _make_result(
    claim_id: str,
    outcome: VerificationOutcome,
    *,
    dependency_state: str = "NOT_DECLARED",
) -> VerificationResult:
    return VerificationResult(
        claim_id=claim_id,
        outcome=outcome,
        dependency_state=dependency_state,
        error_margin=None,
        details="fixture",
        scripts_run=[],
        derivation_refs_checked=[],
        gaps_found=[],
    )


def _graph(
    claims: list[Claim],
    edges: list[tuple[str, str]] | None = None,
) -> ClaimGraph:
    return ClaimGraph(
        claims={c.id: c for c in claims},
        dependency_edges=[
            DependencyEdge(
                upstream=u,
                downstream=d,
                reason="fixture",
                source="fixture",
            )
            for u, d in (edges or [])
        ],
    )


def _stub_falsification(monkeypatch) -> None:
    """Replace FalsificationPipeline.run_all with deterministic fake."""

    def fake_run_all(self, seed=None):
        return [
            FalsificationTest(
                test_id=f"TEST_{i}",
                name=f"Fake TEST {i}",
                locally_executable=i <= 2,
                framework_prediction="(fixture)",
                falsification_criterion="(fixture)",
                current_readout=(
                    FalsificationReadout.PARTIAL_LOCAL
                    if i == 1
                    else FalsificationReadout.UNDER_PRESSURE
                    if i == 2
                    else FalsificationReadout.EXTERNAL_ONLY
                ),
                details=f"fixture detail for TEST_{i}",
            )
            for i in range(1, 6)
        ]

    monkeypatch.setattr(
        "verification.pipeline.FalsificationPipeline.run_all", fake_run_all
    )


# ---------------------------------------------------------------------------
# Test 1: dependency propagation
# ---------------------------------------------------------------------------


def test_no_dependency_clear_when_upstream_open() -> None:
    """Any HYPOTHESIS_OPEN upstream must stop the downstream from being CLEAR.

    Build a small diamond graph ``A -> C``, ``B -> C``, ``C -> D``. Inject:
        * A: REPRODUCED
        * B: HYPOTHESIS_OPEN
        * C: REGRESSION_OK
    Then assert that ``summarize_dependency_state`` for every node below
    an explicit HYPOTHESIS_OPEN upstream is not ``CLEAR``.
    """

    graph = _graph(
        [
            _make_claim("A"),
            _make_claim("B", status=ClaimStatus.CONDITIONAL, confidence=0.85),
            _make_claim("C"),
            _make_claim("D"),
        ],
        edges=[("A", "C"), ("B", "C"), ("C", "D")],
    )
    results = [
        _make_result("A", VerificationOutcome.REPRODUCED),
        _make_result("B", VerificationOutcome.HYPOTHESIS_OPEN),
        _make_result(
            "C",
            VerificationOutcome.REGRESSION_OK,
            dependency_state="OPEN",
        ),
    ]

    # Directly-downstream-of-OPEN must be OPEN, not CLEAR.
    assert summarize_dependency_state("C", graph, results) == "OPEN"

    # For every claim in the graph, if any explicit upstream has
    # HYPOTHESIS_OPEN, the state must not be CLEAR.
    result_by_id = {r.claim_id: r for r in results}
    for cid in graph.claims:
        upstreams = graph.upstream_of(cid)
        if not upstreams:
            continue
        any_upstream_open = any(
            (r := result_by_id.get(up)) is not None
            and r.outcome is VerificationOutcome.HYPOTHESIS_OPEN
            for up in upstreams
        )
        state = summarize_dependency_state(cid, graph, results)
        if any_upstream_open:
            assert state != "CLEAR", (
                f"claim {cid}: at least one upstream is HYPOTHESIS_OPEN "
                f"but dependency_state == {state!r}"
            )


# ---------------------------------------------------------------------------
# Test 2: falsification lane
# ---------------------------------------------------------------------------


def test_all_five_falsification_tests_have_valid_readouts(monkeypatch) -> None:
    """The falsification pipeline always yields 5 records with valid readouts.

    We monkey-patch the sandbox subprocess so the locally executable
    tests (TEST 1, TEST 2) don't depend on the real ``sandbox/`` scripts
    or their optional dependencies. The external-only tests (TEST 3, 4,
    5) never invoke a subprocess by construction.
    """

    def fake_run(script_path, seed=None, timeout=None, cwd=None):
        return SandboxRunResult(
            script_path=str(script_path),
            success=True,
            stdout='{"Q_NO": 0.54, "Q_IO": 0.56}',
            stderr="",
            return_code=0,
            error="",
            parsed_output={"Q_NO": 0.54, "Q_IO": 0.56},
        )

    monkeypatch.setattr(
        "verification.falsification.test1_eeg_csd.run_sandbox_script", fake_run
    )
    monkeypatch.setattr(
        "verification.falsification.test2_neutrino_koide.run_sandbox_script",
        fake_run,
    )

    pipeline = FalsificationPipeline()
    tests = pipeline.run_all()

    assert len(tests) == 5

    expected_ids = {f"TEST_{i}" for i in range(1, 6)}
    assert {t.test_id for t in tests} == expected_ids

    valid = set(FalsificationReadout)
    for t in tests:
        assert t.current_readout in valid, (
            f"{t.test_id}: readout {t.current_readout!r} not in FalsificationReadout"
        )


# ---------------------------------------------------------------------------
# Test 3: gap report aggregates all gaps
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not CLAIMS_MD.is_file(),
    reason="CLAIMS.md not present in workspace",
)
def test_gap_report_includes_all_gaps(monkeypatch) -> None:
    """Every unique ``gaps_found`` entry appears in the rendered gap report."""

    _stub_falsification(monkeypatch)

    report = run_verification_pipeline(
        str(CLAIMS_MD),
        dependency_overlay=str(OVERLAY) if OVERLAY.is_file() else None,
        support_manifest=str(MANIFEST) if MANIFEST.is_file() else None,
        agents_md_path=str(AGENTS_MD) if AGENTS_MD.is_file() else None,
        quick=True,
    )

    gap_text = generate_gap_report(report.claims)

    # Collect the raw gap snippets from every claim that produced gaps.
    # Each should be findable as a substring in the rendered markdown.
    unique_snippets: set[str] = set()
    for r in report.claims:
        for gap in r.gaps_found:
            snippet = gap.strip().replace("\n", " ")
            if snippet:
                unique_snippets.add(snippet)

    missing = [s for s in unique_snippets if s not in gap_text]
    assert not missing, (
        f"gap report missing {len(missing)} gap snippets; "
        f"first few: {sorted(missing)[:3]}"
    )

    # Basic shape: if there were any gaps, the report should name
    # every claim that produced them by its claim id.
    claim_ids_with_gaps = {r.claim_id for r in report.claims if r.gaps_found}
    missing_ids = [cid for cid in claim_ids_with_gaps if cid not in gap_text]
    assert not missing_ids, (
        f"gap report missing claim ids: {missing_ids}"
    )


# ---------------------------------------------------------------------------
# Test 4: cascade report includes transitive dependents
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not CLAIMS_MD.is_file(),
    reason="CLAIMS.md not present in workspace",
)
def test_cascade_report_includes_transitive_dependents(monkeypatch) -> None:
    """For an upstream with a multi-hop cascade, every downstream id is listed.

    Iterates every claim in the graph that has a non-empty cascade and
    verifies the rendered cascade report mentions every transitive
    downstream id on the line for that upstream.
    """

    _stub_falsification(monkeypatch)

    report = run_verification_pipeline(
        str(CLAIMS_MD),
        dependency_overlay=str(OVERLAY) if OVERLAY.is_file() else None,
        support_manifest=str(MANIFEST) if MANIFEST.is_file() else None,
        agents_md_path=str(AGENTS_MD) if AGENTS_MD.is_file() else None,
        quick=True,
    )

    graph = ClaimGraph.from_markdown(
        str(CLAIMS_MD),
        dependency_overlay_path=str(OVERLAY) if OVERLAY.is_file() else None,
        support_manifest_path=str(MANIFEST) if MANIFEST.is_file() else None,
    )
    cascade_text = generate_cascade_report(graph, report.claims)

    # Pick every upstream with a non-trivial cascade; for each one,
    # confirm every transitive downstream id appears in the report.
    at_least_one_checked = False
    for cid in graph.claims:
        downstream = graph.cascade_impact(cid)
        if not downstream:
            continue
        at_least_one_checked = True

        # Pull the line that mentions this upstream (report has
        # backtick-quoted ids and a Unicode arrow).
        upstream_lines = [
            line
            for line in cascade_text.splitlines()
            if f"`{cid}`" in line and ("→" in line or "->" in line)
        ]
        assert upstream_lines, (
            f"cascade report has no line for upstream {cid}; "
            f"sample:\n{cascade_text[:500]}"
        )
        joined = " ".join(upstream_lines)
        missing = [d for d in downstream if d not in joined]
        assert not missing, (
            f"cascade report for upstream {cid} missing downstreams: {missing}"
        )

    assert at_least_one_checked, (
        "no upstream in the graph has a declared downstream cascade — "
        "unexpected for the real workspace (check dependency_overlay.yaml)"
    )
