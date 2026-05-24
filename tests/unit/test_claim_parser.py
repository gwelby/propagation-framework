"""Unit tests for the claim graph infrastructure.

Covers:
    * ``verification.claim_parser.parse_claims_md`` — parsing the live
      fixture, duplicate id rejection, unknown status, out-of-range
      confidence warning, and file / hypothesis / gap extraction.
    * ``verification.dependency_overlay`` — overlay loading, forbidden
      keys (``status``/``confidence``), self-loops, missing keys, and
      the shared :func:`resolve_claim_id` resolver.
    * ``verification.support_manifest`` — manifest loading and the
      "file must exist" and "no status key" rules.
    * ``verification.claim_graph.ClaimGraph`` — topological ordering
      (linear + diamond), cycle detection, cascade impact, and the
      validate() findings (WARN vs BLOCK).

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 1 (parsing), Req. 2 (graph + overlay), Req. 11 (validation).
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 2.7.

These tests use ``pytest``'s ``tmp_path`` fixture to synthesize minimal
CLAIMS.md / YAML inputs when needed; they never touch the real board.
"""

from __future__ import annotations

import textwrap
import warnings
from pathlib import Path

import pytest

from verification.claim_graph import ClaimGraph
from verification.claim_parser import CONFIDENCE_RANGES, parse_claims_md
from verification.dependency_overlay import (
    load_dependency_overlay,
    resolve_claim_id,
)
from verification.models import Claim, ClaimStatus, DependencyEdge
from verification.support_manifest import load_support_manifest


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "claims_fixture.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_minimal_claims_md(
    tmp_path: Path,
    rows: list[tuple[str, str, float, str]],
    *,
    filename: str = "claims_minimal.md",
    section: str = "### 1. Fundamental Physics",
    extra_grading_rows: bool = False,
) -> Path:
    """Write a minimal CLAIMS.md-format file containing only ``rows``.

    Args:
        tmp_path: pytest tmp_path fixture.
        rows: list of ``(name, status, confidence, evidence)`` tuples.
            ``status`` is the raw cell text (e.g. ``"DERIVED"`` or
            ``"PARTIAL DERIVATION"``); it is wrapped in ``**bold**``
            automatically. ``evidence`` is the full evidence cell; the
            falsification cell is a canned placeholder.
        filename: output filename inside ``tmp_path``.
        section: scoreboard section header to emit. The parser only
            reads rows under one of the two known section headers.

    Returns:
        Path to the written file.
    """

    lines: list[str] = [
        "# Minimal CLAIMS.md test fixture",
        "",
        "## ⦿ The Audit Scoreboard",
        "",
        section,
        "",
        "| Claim | Status | Evidence | What Falsifies It | Confidence |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for name, status, confidence, evidence in rows:
        # Rows must be a single line (the parser splits on newlines).
        one_line_evidence = " ".join(evidence.split())
        lines.append(
            f"| **{name}** | **{status}** | {one_line_evidence} | "
            f"Falsifier placeholder. | {confidence} |"
        )
    path = tmp_path / filename
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _claim(
    cid: str,
    status: ClaimStatus,
    *,
    confidence: float | None = None,
    named_hypotheses: list[str] | None = None,
) -> Claim:
    """Construct a :class:`Claim` with sensible defaults for graph tests.

    The confidence defaults to the midpoint of the tier's allowed range so
    the claim passes :meth:`ClaimGraph.validate` range checks unless the
    test overrides it.
    """

    if confidence is None:
        lo, hi = CONFIDENCE_RANGES[status]
        confidence = (lo + hi) / 2
    return Claim(
        id=cid,
        name=cid,
        status=status,
        confidence=confidence,
        evidence_summary="",
        falsification_criterion="",
        named_hypotheses=list(named_hypotheses or []),
    )


def _linear_graph(ids: list[str]) -> ClaimGraph:
    """Build a ClaimGraph with DERIVED claims for ``ids`` and no edges."""

    claims = {cid: _claim(cid, ClaimStatus.DERIVED) for cid in ids}
    return ClaimGraph(claims=claims, dependency_edges=[])


def _edge(upstream: str, downstream: str, *, reason: str = "test") -> DependencyEdge:
    return DependencyEdge(
        upstream=upstream,
        downstream=downstream,
        reason=reason,
        source="test_fixture",
    )


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


def test_parser_parses_all_tiers_from_fixture() -> None:
    """The shared fixture contains one row per status tier."""

    claims = parse_claims_md(FIXTURE_PATH)

    assert len(claims) == 8, f"expected 8 rows, got {sorted(claims)}"

    # Verify the slugified ids we rely on downstream.
    expected_ids = {
        "alpha_derived_from_x": (ClaimStatus.DERIVED, 0.95),
        "beta_conditional_on_h_foo": (ClaimStatus.CONDITIONAL, 0.85),
        "gamma_numerator_theorem": (ClaimStatus.PARTIAL_DERIVATION, 0.85),
        "delta_coupling_ratio": (ClaimStatus.ARGUED, 0.80),
        "epsilon_mass_coincidence": (ClaimStatus.EMPIRICAL, 0.70),
        "zeta_perpetual_motion_fixture": (ClaimStatus.NO_GO, 0.05),
        "eta_pattern_insight": (ClaimStatus.INTUITION, 0.45),
        "theta_frontier_gap": (ClaimStatus.OPEN, 0.10),
    }
    assert set(claims) == set(expected_ids)

    for cid, (status, confidence) in expected_ids.items():
        claim = claims[cid]
        assert claim.status is status, f"{cid}: {claim.status} != {status}"
        assert claim.confidence == pytest.approx(confidence)
        # Every parsed claim preserves its source line number.
        assert claim.source_row > 0


def test_parser_extracts_named_hypotheses_from_conditional() -> None:
    """The CONDITIONAL fixture row names at least one hypothesis."""

    claims = parse_claims_md(FIXTURE_PATH)
    beta = claims["beta_conditional_on_h_foo"]

    assert beta.status is ClaimStatus.CONDITIONAL
    assert beta.named_hypotheses, "expected at least one named hypothesis"
    # ``H_foo`` is the canonical name in the fixture prose.
    assert any("H_foo" in hyp for hyp in beta.named_hypotheses), (
        f"expected 'H_foo' token in {beta.named_hypotheses!r}"
    )


def test_parser_extracts_known_gaps_from_argued() -> None:
    """The ARGUED fixture row has at least one extracted gap snippet."""

    claims = parse_claims_md(FIXTURE_PATH)
    delta = claims["delta_coupling_ratio"]

    assert delta.status is ClaimStatus.ARGUED
    assert delta.known_gaps, "expected at least one gap snippet on ARGUED row"


def test_parser_extracts_file_refs() -> None:
    """Derivation and sandbox refs in the fixture land on the right fields."""

    claims = parse_claims_md(FIXTURE_PATH)
    alpha = claims["alpha_derived_from_x"]

    # Derivation references from the fixture's Alpha row.
    assert "derivations/fixture_alpha_derivation.md" in alpha.derivation_files
    assert "derivations/fixture_alpha_audit.md" in alpha.derivation_files
    # Sandbox script reference from the fixture's Alpha row.
    assert "sandbox/fixture_alpha_check.py" in alpha.sandbox_scripts


def test_parser_rejects_duplicate_slugified_ids(tmp_path: Path) -> None:
    """Two rows that slugify to the same id raise a ValueError."""

    path = _make_minimal_claims_md(
        tmp_path,
        rows=[
            (
                "Alpha Derived",
                "DERIVED",
                0.95,
                "First row. [ref](derivations/a.md)",
            ),
            (
                "alpha  derived",  # slugifies to the same id as the first row
                "DERIVED",
                0.93,
                "Second row that collides on id.",
            ),
        ],
    )

    with pytest.raises(ValueError) as excinfo:
        parse_claims_md(path)
    assert "collides" in str(excinfo.value) or "id" in str(excinfo.value).lower()


def test_parser_rejects_unknown_status(tmp_path: Path) -> None:
    """An unknown status tier raises with a line number in the message."""

    path = _make_minimal_claims_md(
        tmp_path,
        rows=[
            (
                "Mysterious Row",
                "MYTHICAL",
                0.5,
                "A row with a status the parser does not recognize.",
            ),
        ],
    )

    with pytest.raises(ValueError) as excinfo:
        parse_claims_md(path)
    message = str(excinfo.value)
    assert "MYTHICAL" in message
    # The parser's error messages include a line number for traceability.
    assert "line" in message.lower()


def test_parser_warns_on_out_of_range_confidence(tmp_path: Path) -> None:
    """A confidence outside the tier's stated range emits a UserWarning."""

    # DERIVED range is 0.90 - 1.00; 0.40 is far outside.
    path = _make_minimal_claims_md(
        tmp_path,
        rows=[
            (
                "Alpha Out Of Range",
                "DERIVED",
                0.40,
                "A DERIVED row with confidence well below its tier floor.",
            ),
        ],
    )

    with pytest.warns(UserWarning, match="outside the stated DERIVED range"):
        parse_claims_md(path)


# ---------------------------------------------------------------------------
# Dependency overlay tests
# ---------------------------------------------------------------------------


def test_overlay_loads_valid_edges(tmp_path: Path) -> None:
    """A well-formed overlay resolves its edges against parsed claim ids."""

    parsed = parse_claims_md(FIXTURE_PATH)
    overlay = tmp_path / "overlay.yaml"
    overlay.write_text(
        textwrap.dedent(
            """\
            edges:
              - upstream: alpha_derived_from_x
                downstream: beta_conditional_on_h_foo
                reason: "beta's ansatz rests on the alpha closure theorem"
                source: "test_fixture"
              - upstream: beta_conditional_on_h_foo
                downstream: gamma_numerator_theorem
                reason: "gamma's bridge uses the beta lemma"
                source: "test_fixture"
            """
        ),
        encoding="utf-8",
    )

    edges = load_dependency_overlay(overlay, parsed)
    assert len(edges) == 2
    assert edges[0].upstream == "alpha_derived_from_x"
    assert edges[0].downstream == "beta_conditional_on_h_foo"
    assert edges[1].upstream == "beta_conditional_on_h_foo"
    assert edges[1].downstream == "gamma_numerator_theorem"


def test_overlay_rejects_missing_claim_id(tmp_path: Path) -> None:
    """An edge referencing a non-existent id is a BLOCK-level error."""

    parsed = parse_claims_md(FIXTURE_PATH)
    overlay = tmp_path / "overlay.yaml"
    overlay.write_text(
        textwrap.dedent(
            """\
            edges:
              - upstream: alpha_derived_from_x
                downstream: nonexistent_claim
                reason: "references a claim that does not exist"
                source: "test_fixture"
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        load_dependency_overlay(overlay, parsed)
    assert "nonexistent_claim" in str(excinfo.value)


def test_overlay_rejects_status_key(tmp_path: Path) -> None:
    """A top-level ``status:`` key is forbidden by Req. 2.7."""

    parsed = parse_claims_md(FIXTURE_PATH)
    overlay = tmp_path / "overlay.yaml"
    overlay.write_text(
        textwrap.dedent(
            """\
            status: DERIVED
            edges: []
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        load_dependency_overlay(overlay, parsed)
    message = str(excinfo.value)
    assert "status" in message
    assert "2.7" in message  # loader advertises the requirement id


def test_overlay_rejects_confidence_key(tmp_path: Path) -> None:
    """A ``confidence:`` key on an edge is forbidden."""

    parsed = parse_claims_md(FIXTURE_PATH)
    overlay = tmp_path / "overlay.yaml"
    overlay.write_text(
        textwrap.dedent(
            """\
            edges:
              - upstream: alpha_derived_from_x
                downstream: beta_conditional_on_h_foo
                reason: "test"
                source: "test_fixture"
                confidence: 0.9
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        load_dependency_overlay(overlay, parsed)
    assert "confidence" in str(excinfo.value)


def test_overlay_rejects_self_loop(tmp_path: Path) -> None:
    """An edge whose upstream equals its downstream is rejected."""

    parsed = parse_claims_md(FIXTURE_PATH)
    overlay = tmp_path / "overlay.yaml"
    overlay.write_text(
        textwrap.dedent(
            """\
            edges:
              - upstream: alpha_derived_from_x
                downstream: alpha_derived_from_x
                reason: "self loop"
                source: "test_fixture"
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        load_dependency_overlay(overlay, parsed)
    assert "self-loop" in str(excinfo.value).lower()


def test_overlay_rejects_missing_required_key(tmp_path: Path) -> None:
    """An edge missing ``reason`` is rejected with a clear message."""

    parsed = parse_claims_md(FIXTURE_PATH)
    overlay = tmp_path / "overlay.yaml"
    overlay.write_text(
        textwrap.dedent(
            """\
            edges:
              - upstream: alpha_derived_from_x
                downstream: beta_conditional_on_h_foo
                source: "test_fixture"
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        load_dependency_overlay(overlay, parsed)
    assert "reason" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Support manifest tests
# ---------------------------------------------------------------------------


def test_manifest_loads_valid(tmp_path: Path) -> None:
    """A well-formed manifest resolves ids and captures file paths."""

    parsed = parse_claims_md(FIXTURE_PATH)
    # Create a real derivation file on disk so the manifest loader's
    # existence check passes.
    derivation_dir = tmp_path / "derivations"
    derivation_dir.mkdir()
    derivation_file = derivation_dir / "fixture_support.md"
    derivation_file.write_text("# stub derivation", encoding="utf-8")

    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        textwrap.dedent(
            f"""\
            support:
              alpha_derived_from_x:
                - path: {derivation_file.as_posix()}
                  audit_status: DERIVED
                  date: "2099-01-01"
            """
        ),
        encoding="utf-8",
    )

    loaded = load_support_manifest(manifest, parsed)
    assert "alpha_derived_from_x" in loaded
    entries = loaded["alpha_derived_from_x"]
    assert len(entries) == 1
    assert entries[0]["path"] == derivation_file.as_posix()
    assert entries[0]["audit_status"] == "DERIVED"


def test_manifest_rejects_missing_file(tmp_path: Path) -> None:
    """A manifest entry pointing at a non-existent file is a BLOCK error."""

    parsed = parse_claims_md(FIXTURE_PATH)
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        textwrap.dedent(
            """\
            support:
              alpha_derived_from_x:
                - path: derivations/does_not_exist.md
                  audit_status: DERIVED
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        load_support_manifest(manifest, parsed)
    assert "does_not_exist.md" in str(excinfo.value)


def test_manifest_rejects_status_key(tmp_path: Path) -> None:
    """A top-level ``status:`` key in the manifest is forbidden."""

    parsed = parse_claims_md(FIXTURE_PATH)
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        textwrap.dedent(
            """\
            status: DERIVED
            support: {}
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        load_support_manifest(manifest, parsed)
    assert "status" in str(excinfo.value)


# ---------------------------------------------------------------------------
# resolve_claim_id tests
# ---------------------------------------------------------------------------


def test_resolve_claim_id_exact() -> None:
    parsed = parse_claims_md(FIXTURE_PATH)
    resolved = resolve_claim_id("alpha_derived_from_x", parsed)
    assert resolved == "alpha_derived_from_x"


def test_resolve_claim_id_suffix() -> None:
    """A suffix-only ref resolves when the suffix is unique.

    The fixture has ``gamma_numerator_theorem``; ``numerator_theorem``
    is a unique suffix match.
    """

    parsed = parse_claims_md(FIXTURE_PATH)
    resolved = resolve_claim_id("numerator_theorem", parsed)
    assert resolved == "gamma_numerator_theorem"


def test_resolve_claim_id_token_superset() -> None:
    """A token-superset ref still resolves when no suffix match is possible.

    ``alpha_x`` is not a suffix of ``alpha_derived_from_x`` (the separator
    has other tokens between them), but its token set is a subset, and the
    fixture has no other candidate whose token set is a superset.
    """

    parsed = parse_claims_md(FIXTURE_PATH)
    resolved = resolve_claim_id("alpha_x", parsed)
    assert resolved == "alpha_derived_from_x"


def test_resolve_claim_id_unresolvable() -> None:
    """An id that matches nothing raises ValueError."""

    parsed = parse_claims_md(FIXTURE_PATH)
    with pytest.raises(ValueError) as excinfo:
        resolve_claim_id("totally_unknown_claim_xyz", parsed)
    assert "totally_unknown_claim_xyz" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Claim graph tests
# ---------------------------------------------------------------------------


def test_claim_graph_topological_sort_simple() -> None:
    """A → B → C yields an ordering with A before B before C."""

    graph = _linear_graph(["a", "b", "c"])
    graph.dependency_edges = [_edge("a", "b"), _edge("b", "c")]

    order = graph.topological_order()
    assert order.index("a") < order.index("b") < order.index("c")


def test_claim_graph_topological_sort_diamond() -> None:
    """Diamond A → B, A → C, B → D, C → D: A first, D last, B/C between."""

    graph = _linear_graph(["a", "b", "c", "d"])
    graph.dependency_edges = [
        _edge("a", "b"),
        _edge("a", "c"),
        _edge("b", "d"),
        _edge("c", "d"),
    ]

    order = graph.topological_order()
    assert order[0] == "a"
    assert order[-1] == "d"
    assert order.index("b") < order.index("d")
    assert order.index("c") < order.index("d")
    assert order.index("a") < order.index("b")
    assert order.index("a") < order.index("c")


def test_claim_graph_cycle_detection() -> None:
    """A cycle causes topological_order to raise and validate to emit BLOCK."""

    graph = _linear_graph(["a", "b"])
    graph.dependency_edges = [_edge("a", "b"), _edge("b", "a")]

    with pytest.raises(ValueError) as excinfo:
        graph.topological_order()
    assert "cycle" in str(excinfo.value).lower()

    findings = graph.validate()
    severities = [sev for sev, _ in findings]
    assert "BLOCK" in severities
    assert any("cycle" in message.lower() for _, message in findings)


def test_claim_graph_cascade_impact_multi_level() -> None:
    """A → B → C → D: cascade_impact('a') is [B, C, D] in BFS order."""

    graph = _linear_graph(["a", "b", "c", "d"])
    graph.dependency_edges = [
        _edge("a", "b"),
        _edge("b", "c"),
        _edge("c", "d"),
    ]

    impact = graph.cascade_impact("a")
    assert impact == ["b", "c", "d"]


def test_claim_graph_cascade_impact_no_downstream() -> None:
    """A claim with no declared downstream edges has an empty cascade."""

    graph = _linear_graph(["a", "b"])
    graph.dependency_edges = [_edge("a", "b")]

    # ``b`` has no downstream edges.
    assert graph.cascade_impact("b") == []


def test_claim_graph_validate_warn_on_out_of_range_confidence() -> None:
    """A claim whose confidence is outside its tier range is a WARN."""

    # DERIVED range is 0.90 - 1.00; 0.10 is far outside.
    claim = _claim("a", ClaimStatus.DERIVED, confidence=0.10)
    graph = ClaimGraph(claims={"a": claim}, dependency_edges=[])

    findings = graph.validate()
    matching = [
        (sev, msg)
        for sev, msg in findings
        if "outside stated range" in msg and "'a'" in msg
    ]
    assert matching, f"expected a range WARN, got {findings!r}"
    assert all(sev == "WARN" for sev, _ in matching)


def test_claim_graph_validate_warn_on_conditional_missing_hypothesis() -> None:
    """A CONDITIONAL claim with zero named hypotheses triggers a WARN."""

    claim = _claim("a", ClaimStatus.CONDITIONAL, named_hypotheses=[])
    graph = ClaimGraph(claims={"a": claim}, dependency_edges=[])

    findings = graph.validate()
    matching = [
        (sev, msg)
        for sev, msg in findings
        if "named hypotheses" in msg and "'a'" in msg
    ]
    assert matching, f"expected a hypothesis WARN, got {findings!r}"
    assert all(sev == "WARN" for sev, _ in matching)


def test_claim_graph_validate_block_on_no_go_language_in_reason() -> None:
    """An overlay edge whose reason uses no-go language is a BLOCK finding."""

    graph = _linear_graph(["a", "b"])
    graph.dependency_edges = [
        _edge("a", "b", reason="Rejected as failed approach in earlier audit"),
    ]

    findings = graph.validate()
    block_findings = [
        (sev, msg) for sev, msg in findings if sev == "BLOCK"
    ]
    assert block_findings, f"expected a BLOCK finding, got {findings!r}"
    assert any(
        "failed-approach" in msg or "no-go" in msg.lower()
        for _, msg in block_findings
    ), f"BLOCK message should mention no-go / failed-approach: {block_findings!r}"
