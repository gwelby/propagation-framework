"""Report generator for the Propagation Framework verification harness.

This module turns the three kinds of records the harness produces —
parsed :class:`Claim` rows, graded :class:`VerificationResult` records,
and :class:`FalsificationTest` records — into three human-readable
markdown artifacts:

    * :func:`generate_dashboard`     — the top-level audit dashboard
    * :func:`generate_gap_report`    — every gap and open hypothesis
    * :func:`generate_cascade_report` — transitive downstream impact

The :class:`VerificationReport` dataclass bundles everything the
pipeline wants to hand back to a caller (or a CLI) in one place.

Design constraints worth repeating in code so nobody fixes it out:

    * The dashboard is a snapshot. Confidence scores come from
      ``CLAIMS.md``. This module never computes, adjusts, or rewrites
      them — it only echoes what the parser already extracted. The
      dashboard is intentionally labelled as a snapshot so nobody
      mistakes it for a new scoreboard.
    * Claim-level ``Graded_Outcome`` values and falsification-lane
      ``Falsification_Readout`` values live in different tables.
      Mixing them would collapse two different questions into one
      column; :func:`generate_dashboard` keeps them separate.
    * Rows are emitted in dependency-topological order when the graph
      allows it. If the graph has a cycle, we fall back to the
      iteration order of ``graph.claims`` and add a caveat line so the
      operator sees what happened.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 9 (report generation), Req. 9.5/9.6 (no score drift, falsification
  lane separate).
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 5 (Report Generator).
- `.kiro/specs/propagation-framework-verification/tasks.md`
  Tasks 7.1-7.5.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from verification.claim_graph import ClaimGraph
from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.models import (
    Claim,
    VerificationOutcome,
    VerificationResult,
)


__all__ = [
    "VerificationReport",
    "generate_dashboard",
    "generate_gap_report",
    "generate_cascade_report",
]


# ---------------------------------------------------------------------------
# Visual coding
# ---------------------------------------------------------------------------

# Color / marker coding for the dashboard's Graded_Outcome column.
#   supportive (green-ish): REPRODUCED, REGRESSION_OK   -> "✓"
#   neutral    (open-ish):  HYPOTHESIS_OPEN, EXTERNAL_ONLY -> "○"
#   flagged    (pressure):  UNDER_PRESSURE, SCRIPT_BROKEN -> "⚠"
#
# The coded marker is meant for at-a-glance scanning, not for
# classification logic. The enum value itself remains the source of
# truth.
_OUTCOME_MARKERS: dict[VerificationOutcome, str] = {
    VerificationOutcome.REPRODUCED: "✓",
    VerificationOutcome.REGRESSION_OK: "✓",
    VerificationOutcome.HYPOTHESIS_OPEN: "○",
    VerificationOutcome.EXTERNAL_ONLY: "○",
    VerificationOutcome.UNDER_PRESSURE: "⚠",
    VerificationOutcome.SCRIPT_BROKEN: "⚠",
}


def _outcome_marker(outcome: VerificationOutcome) -> str:
    """Marker glyph for a graded outcome (``✓`` / ``○`` / ``⚠``)."""

    return _OUTCOME_MARKERS.get(outcome, "·")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class VerificationReport:
    """All the artifacts the pipeline produced, bundled in one place.

    Attributes:
        claims: Graded verification results, one per claim the pipeline
            ran over. Ordering follows the pipeline's dependency-topological
            traversal when available.
        falsification: Records for TEST 1..5. Always five entries in
            TEST_1..TEST_5 order when produced by the falsification
            pipeline, but the dataclass accepts any list so partial
            reports can be constructed in tests.
        gaps: Aggregated short descriptions of every gap or open
            hypothesis surfaced during the run. Deduplicated and
            prefixed by ``claim_id:`` so the operator can trace each
            entry back to its origin.
        cascade: Mapping of ``claim_id -> [transitive downstream ids]``
            computed from the dependency graph. Claims with no declared
            downstream edges are omitted from the mapping.
        timestamp: When the report was generated (UTC).
    """

    claims: list[VerificationResult]
    falsification: list[FalsificationTest]
    gaps: list[str] = field(default_factory=list)
    cascade: dict[str, list[str]] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


def generate_dashboard(
    graph: ClaimGraph,
    results: list[VerificationResult],
    falsification: list[FalsificationTest],
) -> str:
    """Render the top-level audit dashboard as markdown.

    The dashboard has three sections:

        1. Header with UTC timestamp and a snapshot caveat.
        2. Claim-level table, one row per claim in ``graph.claims``.
           Columns: id, Status tier (from CLAIMS.md — *unchanged*),
           Graded Outcome (with color-code marker), Dependency state,
           Gaps found, Confidence (echoed from CLAIMS.md), Timestamp.
        3. Falsification section with its own table. Columns:
           test_id, name, locally_executable, current_readout, details
           (first line).

    Rows are emitted in topological order over the dependency graph.
    If the graph has a cycle we fall back to ``graph.claims`` iteration
    order and add a note so the operator is not mis-led.

    Args:
        graph: The parsed claim graph. ``graph.claims`` is used as
            the source of status/confidence; no scores are ever
            recomputed here.
        results: Graded verification results. Results without a
            matching entry in ``graph.claims`` are still rendered in a
            trailing "Unmapped results" row so nothing is silently
            dropped.
        falsification: Falsification records. Rendered in their own
            section — never mixed into the claim-level table.

    Returns:
        A markdown string suitable for printing or writing to disk.
    """

    now = datetime.now(timezone.utc)
    results_by_id: dict[str, VerificationResult] = {r.claim_id: r for r in results}

    try:
        ordered = graph.topological_order()
        order_note = None
    except ValueError as exc:
        ordered = list(graph.claims.keys())
        order_note = (
            f"NOTE: dependency graph has a cycle; claim rows are listed "
            f"in parse order instead of topological order ({exc})."
        )

    lines: list[str] = []
    lines.append("# Propagation Framework Verification Dashboard")
    lines.append("")
    lines.append(f"Generated: {now.isoformat()}")
    lines.append("")
    lines.append(
        "> **Snapshot only.** The confidence scores below are echoed "
        "verbatim from `CLAIMS.md`. This dashboard does not and cannot "
        "change them — only an audited update to `CLAIMS.md` can move "
        "a score. See AGENTS.md TRUTH ORDER."
    )
    lines.append("")
    if order_note:
        lines.append(f"> {order_note}")
        lines.append("")

    # ------------------ Claim-level table ------------------
    lines.append("## Claim-level verification")
    lines.append("")
    lines.append(
        "| Claim ID | Status (CLAIMS.md) | Graded Outcome | "
        "Dependency | Gaps | Confidence | Timestamp |"
    )
    lines.append(
        "| :--- | :--- | :--- | :--- | :--- | ---: | :--- |"
    )

    for cid in ordered:
        claim = graph.claims.get(cid)
        if claim is None:
            continue
        result = results_by_id.get(cid)
        lines.append(_claim_row(claim, result))

    # Surface any results for claim ids not in the graph, so they are
    # never silently dropped from the audit view.
    orphan_ids = [r.claim_id for r in results if r.claim_id not in graph.claims]
    if orphan_ids:
        lines.append("")
        lines.append(
            "> NOTE: the following result rows reference claim ids that "
            f"are not in the parsed graph and are listed separately: "
            f"{sorted(orphan_ids)}"
        )
        lines.append("")
        lines.append(
            "| Claim ID (unmapped) | Graded Outcome | Dependency | Gaps | Timestamp |"
        )
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for cid in orphan_ids:
            result = results_by_id[cid]
            lines.append(_orphan_row(cid, result))

    # ------------------ Falsification section ------------------
    lines.append("")
    lines.append("## Falsification tests (separate lane)")
    lines.append("")
    lines.append(
        "Falsification readouts are a distinct lane from claim-level "
        "graded outcomes. `EXTERNAL_ONLY` is explicitly not a pass — a "
        "non-discovery so far is not a confirmation. `SCRIPT_BROKEN` is "
        "a tooling failure, never a falsification."
    )
    lines.append("")
    lines.append(
        "| Test ID | Name | Locally Executable | Current Readout | Detail |"
    )
    lines.append("| :--- | :--- | :---: | :--- | :--- |")
    if not falsification:
        lines.append("| (none) | — | — | — | — |")
    for ft in falsification:
        lines.append(_falsification_row(ft))

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "_Confidence values above are echoed from `CLAIMS.md`. Graded "
        "outcomes and falsification readouts come from this run only; "
        "they never update `CLAIMS.md`._"
    )

    return "\n".join(lines)


def _claim_row(claim: Claim, result: VerificationResult | None) -> str:
    """Build one row of the claim-level table."""

    status_text = claim.status.value
    confidence = f"{claim.confidence:.2f}"
    if result is None:
        outcome_cell = "—"
        dep_cell = "—"
        gaps_cell = "—"
        timestamp_cell = "—"
    else:
        marker = _outcome_marker(result.outcome)
        outcome_cell = f"{marker} {result.outcome.value}"
        dep_cell = result.dependency_state or "NOT_DECLARED"
        gaps_cell = _format_gaps_cell(result.gaps_found)
        timestamp_cell = result.timestamp.isoformat()
    return (
        f"| `{claim.id}` | {status_text} | {outcome_cell} | "
        f"{dep_cell} | {gaps_cell} | {confidence} | {timestamp_cell} |"
    )


def _orphan_row(claim_id: str, result: VerificationResult) -> str:
    """Row for a result whose ``claim_id`` is not in the graph."""

    marker = _outcome_marker(result.outcome)
    return (
        f"| `{claim_id}` | {marker} {result.outcome.value} | "
        f"{result.dependency_state or 'NOT_DECLARED'} | "
        f"{_format_gaps_cell(result.gaps_found)} | "
        f"{result.timestamp.isoformat()} |"
    )


def _falsification_row(ft: FalsificationTest) -> str:
    """Build one row of the falsification table."""

    first_line = ""
    if ft.details:
        for line in ft.details.splitlines():
            if line.strip():
                first_line = line.strip()
                break
    local = "yes" if ft.locally_executable else "no"
    return (
        f"| `{ft.test_id}` | {_escape_cell(ft.name)} | {local} | "
        f"{ft.current_readout.value} | {_escape_cell(first_line)} |"
    )


def _format_gaps_cell(gaps: list[str]) -> str:
    """Compact gap summary: count + first short snippet, if any."""

    if not gaps:
        return "0"
    snippet = gaps[0].strip().replace("\n", " ")
    if len(snippet) > 60:
        snippet = snippet[:57].rstrip() + "..."
    return f"{len(gaps)} — {_escape_cell(snippet)}"


def _escape_cell(text: str) -> str:
    """Escape pipe characters inside markdown table cells."""

    if not text:
        return ""
    return text.replace("|", "\\|").replace("\n", " ")


# ---------------------------------------------------------------------------
# Gap report
# ---------------------------------------------------------------------------


def generate_gap_report(results: list[VerificationResult]) -> str:
    """Aggregate every gap and open hypothesis across all claims.

    Output shape:

        * Header with total gap count (sum across claims).
        * One bullet-list subsection per claim that produced at least
          one gap. Each subsection shows the claim id, the graded
          outcome (so the operator sees whether the gaps came from a
          HYPOTHESIS_OPEN, UNDER_PRESSURE, or SCRIPT_BROKEN row), and
          a bulleted list of the short gap snippets.

    Claims with no gaps are omitted so the report stays scannable.
    """

    now = datetime.now(timezone.utc)

    # Preserve input order so the gap report follows the topological
    # order used by the caller's dashboard.
    claims_with_gaps: list[VerificationResult] = [
        r for r in results if r.gaps_found
    ]
    total = sum(len(r.gaps_found) for r in claims_with_gaps)

    lines: list[str] = []
    lines.append("# Gap Report")
    lines.append("")
    lines.append(f"Generated: {now.isoformat()}")
    lines.append("")
    lines.append(f"Total gaps / open hypotheses: **{total}**")
    lines.append("")
    if not claims_with_gaps:
        lines.append("_No gaps recorded in this run._")
        return "\n".join(lines)

    for r in claims_with_gaps:
        lines.append(
            f"## `{r.claim_id}` — {r.outcome.value} ({r.dependency_state or 'NOT_DECLARED'})"
        )
        for gap in r.gaps_found:
            snippet = gap.strip().replace("\n", " ")
            lines.append(f"- {snippet}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Cascade report
# ---------------------------------------------------------------------------


def generate_cascade_report(
    graph: ClaimGraph,
    results: list[VerificationResult] | None = None,
) -> str:
    """Render the transitive-downstream cascade for every declared edge.

    Only claims whose cascade set is non-empty appear in the report. If
    ``results`` is provided, any claim whose cascade includes a row
    currently at HYPOTHESIS_OPEN or UNDER_PRESSURE is flagged with a
    ``⚠`` marker and a note listing the stressed downstream ids so the
    operator can see which parts of the graph inherit risk.

    Args:
        graph: The parsed claim graph.
        results: Optional list of :class:`VerificationResult`. When
            provided, the cascade highlight uses the graded outcomes
            from this run; when ``None``, the report still emits the
            structural cascade without flagging.

    Returns:
        A markdown string. Always non-empty (header + timestamp) even
        when the graph has no declared edges.
    """

    now = datetime.now(timezone.utc)
    result_map: dict[str, VerificationResult] = {}
    if results:
        result_map = {r.claim_id: r for r in results}

    stressed_outcomes = {
        VerificationOutcome.HYPOTHESIS_OPEN,
        VerificationOutcome.UNDER_PRESSURE,
    }

    lines: list[str] = []
    lines.append("# Cascade Report")
    lines.append("")
    lines.append(f"Generated: {now.isoformat()}")
    lines.append("")
    lines.append(
        "For each claim with at least one declared downstream edge, "
        "the list below enumerates the transitive downstream closure "
        "over the explicit dependency overlay."
    )
    lines.append("")

    any_rows = False
    for cid in graph.claims:
        downstream = graph.cascade_impact(cid)
        if not downstream:
            continue
        any_rows = True

        stressed: list[str] = []
        if result_map:
            for dcid in downstream:
                r = result_map.get(dcid)
                if r is not None and r.outcome in stressed_outcomes:
                    stressed.append(f"{dcid} ({r.outcome.value})")

        marker = "⚠" if stressed else "·"
        lines.append(
            f"- {marker} `{cid}` → [{', '.join(downstream)}]"
        )
        if stressed:
            lines.append(
                f"    - stressed downstream: {', '.join(stressed)}"
            )

    if not any_rows:
        lines.append("_No declared cascade edges in this graph._")

    return "\n".join(lines).rstrip() + "\n"
