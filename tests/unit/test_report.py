"""Unit tests for :mod:`verification.report` (Task 7.5).

Covers:

    * :func:`generate_dashboard` — every claim id present, color-code
      markers applied per outcome, falsification section rendered as a
      separate table (not mixed into the claim-level table),
      timestamps present per row, confidence values echoed without
      drift.
    * :func:`generate_gap_report` — aggregates gaps across multiple
      claims, reports total count, groups by claim id.
    * :func:`generate_cascade_report` — transitive cascade correct on
      a small A→B→C graph; flags stressed downstream when results are
      provided.
    * Property-ish invariants (Property 14): every claim id is a row
      in the dashboard; every identified gap appears in the gap
      report; every claim-level row has a timestamp.

Tests build :class:`Claim`, :class:`VerificationResult`, and
:class:`FalsificationTest` fixtures directly (no disk I/O, no live
CLAIMS.md).

References:
- `.kiro/specs/propagation-framework-verification/requirements.md` Req. 9.
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 7.5.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

import pytest

from verification.claim_graph import ClaimGraph
from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.models import (
    Claim,
    ClaimStatus,
    DependencyEdge,
    VerificationOutcome,
    VerificationResult,
)
from verification.report import (
    VerificationReport,
    generate_cascade_report,
    generate_dashboard,
    generate_gap_report,
)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def _make_claim(
    claim_id: str,
    *,
    status: ClaimStatus = ClaimStatus.DERIVED,
    confidence: float = 0.95,
    name: str | None = None,
) -> Claim:
    return Claim(
        id=claim_id,
        name=name or claim_id.replace("_", " ").title(),
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
    dependency_state: str = "CLEAR",
    gaps: list[str] | None = None,
    timestamp: datetime | None = None,
) -> VerificationResult:
    return VerificationResult(
        claim_id=claim_id,
        outcome=outcome,
        dependency_state=dependency_state,
        error_margin=None,
        details="(fixture result)",
        scripts_run=[],
        derivation_refs_checked=[],
        gaps_found=list(gaps or []),
        timestamp=timestamp or datetime(2026, 4, 2, 12, 0, 0, tzinfo=timezone.utc),
    )


def _make_falsification(
    test_id: str,
    readout: FalsificationReadout,
    *,
    locally_executable: bool = True,
    name: str | None = None,
) -> FalsificationTest:
    return FalsificationTest(
        test_id=test_id,
        name=name or f"{test_id} name",
        locally_executable=locally_executable,
        framework_prediction="(fixture prediction)",
        falsification_criterion="(fixture criterion)",
        current_readout=readout,
        details="first-line detail\nsecond line",
    )


def _build_graph(claims: list[Claim], edges: list[tuple[str, str]] | None = None) -> ClaimGraph:
    claim_map = {c.id: c for c in claims}
    dependency_edges = [
        DependencyEdge(upstream=u, downstream=d, reason="fixture", source="fixture")
        for u, d in (edges or [])
    ]
    return ClaimGraph(claims=claim_map, dependency_edges=dependency_edges)


# ---------------------------------------------------------------------------
# VerificationReport dataclass
# ---------------------------------------------------------------------------


def test_verification_report_defaults_populate_timestamp_and_collections():
    """Default constructor fills timestamp + empty gaps/cascade."""

    report = VerificationReport(claims=[], falsification=[])

    assert isinstance(report.timestamp, datetime)
    assert report.timestamp.tzinfo is not None
    assert report.gaps == []
    assert report.cascade == {}


# ---------------------------------------------------------------------------
# generate_dashboard
# ---------------------------------------------------------------------------


def test_generate_dashboard_all_claims_present():
    """Every claim id in the graph must appear in the dashboard."""

    claims = [
        _make_claim("alpha", status=ClaimStatus.DERIVED, confidence=0.95),
        _make_claim("beta", status=ClaimStatus.CONDITIONAL, confidence=0.85),
        _make_claim("gamma", status=ClaimStatus.ARGUED, confidence=0.80),
    ]
    graph = _build_graph(claims)
    results = [
        _make_result("alpha", VerificationOutcome.REPRODUCED),
        _make_result("beta", VerificationOutcome.HYPOTHESIS_OPEN),
        _make_result("gamma", VerificationOutcome.UNDER_PRESSURE),
    ]

    output = generate_dashboard(graph, results, [])

    for cid in ("alpha", "beta", "gamma"):
        assert f"`{cid}`" in output, f"claim id {cid} missing from dashboard"


def test_generate_dashboard_falsification_section_separate():
    """Falsification rows must be in their own section, not in the claim table."""

    claims = [_make_claim("alpha")]
    graph = _build_graph(claims)
    results = [_make_result("alpha", VerificationOutcome.REPRODUCED)]
    falsification = [
        _make_falsification("TEST_1", FalsificationReadout.PARTIAL_LOCAL),
        _make_falsification(
            "TEST_3",
            FalsificationReadout.EXTERNAL_ONLY,
            locally_executable=False,
        ),
    ]

    output = generate_dashboard(graph, results, falsification)

    # A clear section header for falsification.
    assert "## Falsification tests" in output
    # Split the document and make sure the falsification test IDs
    # appear after the falsification heading, not in the claim table.
    before_fals, _, after_fals = output.partition("## Falsification tests")
    assert "TEST_1" not in before_fals
    assert "TEST_3" not in before_fals
    assert "TEST_1" in after_fals
    assert "TEST_3" in after_fals
    # And the claim row is still in the section above.
    assert "`alpha`" in before_fals


def test_generate_dashboard_color_coding_markers():
    """Each outcome gets the documented marker glyph."""

    claims = [
        _make_claim("a_reproduced"),
        _make_claim("a_regression"),
        _make_claim("a_hyp_open"),
        _make_claim("a_external"),
        _make_claim("a_pressure"),
        _make_claim("a_broken"),
    ]
    graph = _build_graph(claims)
    results = [
        _make_result("a_reproduced", VerificationOutcome.REPRODUCED),
        _make_result("a_regression", VerificationOutcome.REGRESSION_OK),
        _make_result("a_hyp_open", VerificationOutcome.HYPOTHESIS_OPEN),
        _make_result("a_external", VerificationOutcome.EXTERNAL_ONLY),
        _make_result("a_pressure", VerificationOutcome.UNDER_PRESSURE),
        _make_result("a_broken", VerificationOutcome.SCRIPT_BROKEN),
    ]

    output = generate_dashboard(graph, results, [])
    lines = output.splitlines()

    def _row_for(cid: str) -> str:
        matches = [ln for ln in lines if f"`{cid}`" in ln]
        assert matches, f"no dashboard row for {cid!r}"
        return matches[0]

    # supportive ✓
    assert "✓" in _row_for("a_reproduced")
    assert "✓" in _row_for("a_regression")
    # neutral ○
    assert "○" in _row_for("a_hyp_open")
    assert "○" in _row_for("a_external")
    # flagged ⚠
    assert "⚠" in _row_for("a_pressure")
    assert "⚠" in _row_for("a_broken")

    # And the marker must match the outcome classification — no ⚠ on a
    # supportive row.
    assert "⚠" not in _row_for("a_reproduced")
    assert "⚠" not in _row_for("a_regression")


def test_generate_dashboard_no_score_drift():
    """Confidence values in the output must match the input exactly."""

    claims = [
        _make_claim("alpha", confidence=0.91),
        _make_claim("beta", confidence=0.77),
    ]
    graph = _build_graph(claims)
    results = [
        _make_result("alpha", VerificationOutcome.REPRODUCED),
        _make_result("beta", VerificationOutcome.HYPOTHESIS_OPEN),
    ]

    output = generate_dashboard(graph, results, [])

    # Confidences are formatted to 2 decimal places in the dashboard.
    assert "0.91" in output
    assert "0.77" in output
    # None of the other outcomes should have moved the values.
    assert re.search(r"\|\s*0\.91\s*\|", output) is not None
    assert re.search(r"\|\s*0\.77\s*\|", output) is not None


def test_report_timestamps_present_every_row():
    """Every claim row must carry a timestamp cell."""

    ts = datetime(2026, 4, 2, 15, 30, 0, tzinfo=timezone.utc)
    claims = [_make_claim("alpha"), _make_claim("beta")]
    graph = _build_graph(claims)
    results = [
        _make_result("alpha", VerificationOutcome.REPRODUCED, timestamp=ts),
        _make_result("beta", VerificationOutcome.REGRESSION_OK, timestamp=ts),
    ]

    output = generate_dashboard(graph, results, [])

    expected_iso = ts.isoformat()
    # Every claim row is a line containing the claim id; that line must
    # also contain the ISO timestamp.
    for cid in ("alpha", "beta"):
        matching_rows = [
            line for line in output.splitlines() if f"`{cid}`" in line
        ]
        assert matching_rows, f"no dashboard row for {cid!r}"
        for row in matching_rows:
            assert expected_iso in row, f"timestamp missing from row: {row}"


def test_generate_dashboard_status_tier_preserved_verbatim():
    """The Status column is echoed from CLAIMS.md, never recomputed."""

    claims = [
        _make_claim("alpha", status=ClaimStatus.DERIVED, confidence=0.95),
        _make_claim("beta", status=ClaimStatus.CONDITIONAL, confidence=0.80),
        _make_claim("gamma", status=ClaimStatus.PARTIAL_DERIVATION, confidence=0.80),
    ]
    graph = _build_graph(claims)
    # The graded outcome disagrees with the tier — the tier text in the
    # dashboard must NOT be changed to reflect the outcome.
    results = [
        _make_result("alpha", VerificationOutcome.UNDER_PRESSURE),
        _make_result("beta", VerificationOutcome.HYPOTHESIS_OPEN),
        _make_result("gamma", VerificationOutcome.HYPOTHESIS_OPEN),
    ]

    output = generate_dashboard(graph, results, [])

    # Tier values come straight from the ClaimStatus enum values.
    assert "DERIVED" in output
    assert "CONDITIONAL" in output
    assert "PARTIAL_DERIVATION" in output


def test_generate_dashboard_property_every_claim_has_a_row():
    """Property 14 equivalent: dashboard contains one row per claim id."""

    claims = [_make_claim(f"claim_{i}") for i in range(7)]
    graph = _build_graph(claims)
    results = [
        _make_result(f"claim_{i}", VerificationOutcome.REGRESSION_OK)
        for i in range(7)
    ]

    output = generate_dashboard(graph, results, [])

    for c in claims:
        assert f"`{c.id}`" in output


# ---------------------------------------------------------------------------
# generate_gap_report
# ---------------------------------------------------------------------------


def test_generate_gap_report_aggregates_across_claims():
    """Every gap across every claim must appear in the gap report."""

    results = [
        _make_result(
            "alpha",
            VerificationOutcome.HYPOTHESIS_OPEN,
            gaps=["H_foo open", "H_bar open"],
        ),
        _make_result(
            "beta",
            VerificationOutcome.UNDER_PRESSURE,
            gaps=["scheme selection not yet closed"],
        ),
        _make_result(
            "gamma",
            VerificationOutcome.REGRESSION_OK,
            gaps=[],
        ),
    ]

    output = generate_gap_report(results)

    # Total count is 3 (2 from alpha, 1 from beta).
    assert "**3**" in output
    # Each gap snippet present.
    assert "H_foo open" in output
    assert "H_bar open" in output
    assert "scheme selection not yet closed" in output
    # gamma has no gaps → it must not get a subsection.
    assert "gamma" not in output
    # Each claim id that has gaps gets a subsection header.
    assert "alpha" in output
    assert "beta" in output


def test_generate_gap_report_shows_status_tier_and_hypotheses():
    """Subsection headers surface the outcome and dependency state."""

    results = [
        _make_result(
            "alpha",
            VerificationOutcome.HYPOTHESIS_OPEN,
            dependency_state="OPEN",
            gaps=["H_foo"],
        ),
    ]

    output = generate_gap_report(results)

    assert "HYPOTHESIS_OPEN" in output
    assert "OPEN" in output


def test_generate_gap_report_handles_empty_results():
    """An empty gap report is still a structured markdown doc."""

    output = generate_gap_report([])

    assert "# Gap Report" in output
    assert "Total gaps / open hypotheses: **0**" in output
    assert "No gaps recorded" in output


def test_gap_report_property_every_gap_appears():
    """Property 14: every identified gap appears verbatim in the gap report."""

    results = [
        _make_result(
            "alpha",
            VerificationOutcome.HYPOTHESIS_OPEN,
            gaps=[f"gap_alpha_{i}" for i in range(4)],
        ),
        _make_result(
            "beta",
            VerificationOutcome.UNDER_PRESSURE,
            gaps=[f"gap_beta_{i}" for i in range(3)],
        ),
    ]

    output = generate_gap_report(results)

    for r in results:
        for gap in r.gaps_found:
            assert gap in output


# ---------------------------------------------------------------------------
# generate_cascade_report
# ---------------------------------------------------------------------------


def test_generate_cascade_report_transitive_closure():
    """A→B→C: cascade of A must include both B and C."""

    claims = [_make_claim("A"), _make_claim("B"), _make_claim("C")]
    graph = _build_graph(claims, edges=[("A", "B"), ("B", "C")])

    output = generate_cascade_report(graph)

    # Pull out just the line for A so we check its cascade list only.
    lines = [ln for ln in output.splitlines() if "`A`" in ln]
    assert lines, "no cascade line for A"
    line = lines[0]
    assert "B" in line
    assert "C" in line


def test_generate_cascade_report_omits_leaves():
    """Claims with no declared downstream are left out of the report."""

    claims = [_make_claim("A"), _make_claim("B")]
    graph = _build_graph(claims, edges=[("A", "B")])

    output = generate_cascade_report(graph)

    # A has downstream B so A should appear.
    assert "`A`" in output
    # B is a leaf and should not appear as a cascade source.
    lines = [ln for ln in output.splitlines() if ln.startswith("- ")]
    assert all("`B`" not in ln for ln in lines), (
        f"leaf B appeared as a cascade source: {lines}"
    )


def test_generate_cascade_report_flags_stressed_downstream():
    """Results with HYPOTHESIS_OPEN or UNDER_PRESSURE flag the upstream cascade."""

    claims = [_make_claim("A"), _make_claim("B"), _make_claim("C")]
    graph = _build_graph(claims, edges=[("A", "B"), ("B", "C")])
    results = [
        _make_result("A", VerificationOutcome.REGRESSION_OK),
        _make_result("B", VerificationOutcome.HYPOTHESIS_OPEN),
        _make_result("C", VerificationOutcome.REGRESSION_OK),
    ]

    output = generate_cascade_report(graph, results=results)

    # Line for A should note stressed downstream.
    a_section = [ln for ln in output.splitlines() if "`A`" in ln or "stressed" in ln]
    joined = "\n".join(a_section)
    assert "⚠" in joined
    assert "HYPOTHESIS_OPEN" in output


def test_generate_cascade_report_empty_graph_still_renders():
    """Even with no edges the cascade report returns a structured doc."""

    claims = [_make_claim("solo")]
    graph = _build_graph(claims)

    output = generate_cascade_report(graph)

    assert "# Cascade Report" in output
    assert "No declared cascade edges" in output
