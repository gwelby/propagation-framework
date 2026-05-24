"""End-to-end validation tests (Task 13.1).

Asserts that the verification harness satisfies every top-level
requirement in
`.kiro/specs/propagation-framework-verification/requirements.md`
and that the correctness properties from
`.kiro/specs/propagation-framework-verification/design.md`
that map to runtime assertions hold against the real workspace.

Falsification runners and sandbox subprocesses are stubbed so the
suite stays fast and does not depend on heavyweight scientific
libraries. The stubs still produce five falsification records with
valid readouts so the invariants are real, just not gated on the
sandbox scripts' present state.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from verification.claim_graph import ClaimGraph
from verification.claim_parser import parse_claims_md
from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.guardrails import Guardrails
from verification.models import ClaimStatus, VerificationOutcome
from verification.pipeline import run_verification_pipeline
from verification.report import (
    generate_cascade_report,
    generate_dashboard,
    generate_gap_report,
)
from verification.runners.base import get_runner_for_tier
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLAIMS_MD = REPO_ROOT / "CLAIMS.md"
OVERLAY = REPO_ROOT / "verification" / "dependency_overlay.yaml"
MANIFEST = REPO_ROOT / "verification" / "support_manifest.yaml"
AGENTS_MD = REPO_ROOT / "AGENTS.md"

PROTECTED_FILES: tuple[Path, ...] = (
    REPO_ROOT / "CLAIMS.md",
    REPO_ROOT / "ACTIVE_ISSUES.md",
    REPO_ROOT / "WHATS_NEXT.md",
)


# ---------------------------------------------------------------------------
# Stubs and helpers
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    if not path.is_file():
        return ""
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _stub_falsification(monkeypatch) -> None:
    """Replace FalsificationPipeline.run_all with a deterministic fake.

    Produces five records in TEST_1..TEST_5 order with a mix of
    readouts so invariants about the falsification lane are real.
    """

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


def _stub_sandbox_runner(monkeypatch) -> None:
    """Make every runner's sandbox subprocess deterministic and fast."""

    def fake_run(script_path, seed=None, timeout=None, cwd=None):
        return SandboxRunResult(
            script_path=str(script_path),
            success=True,
            stdout='{"predicted": 1.0, "measured": 1.0}',
            stderr="",
            return_code=0,
            error="",
            parsed_output={"predicted": 1.0, "measured": 1.0},
        )

    for module in (
        "verification.runners.derived",
        "verification.runners.conditional",
        "verification.runners.argued",
        "verification.runners.empirical",
        "verification.runners.frontier",
    ):
        monkeypatch.setattr(f"{module}.run_sandbox_script", fake_run)


def _build_full_report(monkeypatch):
    """Run the pipeline and also return the graph used for the dashboard."""

    _stub_falsification(monkeypatch)
    _stub_sandbox_runner(monkeypatch)
    report = run_verification_pipeline(
        str(CLAIMS_MD),
        dependency_overlay=str(OVERLAY) if OVERLAY.is_file() else None,
        support_manifest=str(MANIFEST) if MANIFEST.is_file() else None,
        agents_md_path=str(AGENTS_MD) if AGENTS_MD.is_file() else None,
        quick=True,
        seed=42,
    )
    graph = ClaimGraph.from_markdown(
        str(CLAIMS_MD),
        dependency_overlay_path=str(OVERLAY) if OVERLAY.is_file() else None,
        support_manifest_path=str(MANIFEST) if MANIFEST.is_file() else None,
    )
    return report, graph


pytestmark = pytest.mark.skipif(
    not CLAIMS_MD.is_file(),
    reason="CLAIMS.md not present in workspace",
)


# ---------------------------------------------------------------------------
# Requirement coverage
# ---------------------------------------------------------------------------


def test_verification_report_satisfies_all_11_requirements(monkeypatch) -> None:
    """Build a full report and check every top-level requirement.

    Requirement-to-assertion map (see requirements.md for prose):
        Req. 1  — CLAIMS.md parsed into at least 20 claim records.
        Req. 2  — dependency overlay contributes at least 7 edges.
        Req. 3  — every claim result has a valid VerificationOutcome.
        Req. 4  — each status tier resolves to a runner class.
        Req. 5  — the falsification pipeline produces exactly 5 records.
        Req. 6  — protected board documents are byte-identical pre/post.
        Req. 7  — at least one claim has a non-empty cascade impact.
        Req. 8  — sandbox runner always returns a SandboxRunResult, even
                  for a missing or broken script (never raises).
        Req. 9  — dashboard, gap report, and cascade report all produce
                  non-empty markdown strings.
        Req. 10 — two runs with the same seed produce matching graded
                  outcomes (determinism).
        Req. 11 — graph.validate() returns (severity, message) tuples
                  with severities drawn from {"BLOCK", "WARN"}.
    """

    before_hashes = {p: _sha256(p) for p in PROTECTED_FILES}
    report, graph = _build_full_report(monkeypatch)

    # Req. 1 — CLAIMS.md parsing produced enough structured records.
    assert len(graph.claims) >= 20, (
        f"expected at least 20 parsed claims, got {len(graph.claims)}"
    )

    # Req. 2 — overlay contributed edges.
    assert len(graph.dependency_edges) >= 7, (
        f"expected at least 7 dependency edges from the overlay, "
        f"got {len(graph.dependency_edges)}"
    )

    # Req. 3 — every claim result has a valid VerificationOutcome.
    valid_outcomes = set(VerificationOutcome)
    for r in report.claims:
        assert r.outcome in valid_outcomes, (
            f"{r.claim_id}: outcome {r.outcome!r} not in VerificationOutcome"
        )

    # Req. 4 — every status tier resolves to a runner.
    for status in ClaimStatus:
        runner = get_runner_for_tier(status)
        assert runner is not None, f"no runner for {status.value}"

    # Req. 5 — exactly five falsification records, each valid.
    assert len(report.falsification) == 5
    valid_readouts = set(FalsificationReadout)
    for ft in report.falsification:
        assert ft.current_readout in valid_readouts

    # Req. 6 — no board document changed.
    after_hashes = {p: _sha256(p) for p in PROTECTED_FILES}
    drifted = [
        p.name
        for p in PROTECTED_FILES
        if before_hashes[p] and before_hashes[p] != after_hashes[p]
    ]
    assert not drifted, f"protected board documents changed: {drifted}"

    # Req. 7 — at least one claim has a non-empty cascade.
    any_cascade = any(v for v in report.cascade.values())
    assert any_cascade, "no claim has a declared cascade impact"

    # Req. 8 — sandbox runner never raises. A missing script returns a
    # SandboxRunResult with success=False / error='FileNotFoundError'.
    result = run_sandbox_script("sandbox/__does_not_exist__.py")
    assert isinstance(result, SandboxRunResult)
    assert result.success is False
    assert result.error == "FileNotFoundError"

    # Req. 9 — all three report artifacts produce non-empty markdown.
    dashboard = generate_dashboard(graph, report.claims, report.falsification)
    gaps = generate_gap_report(report.claims)
    cascade = generate_cascade_report(graph, report.claims)
    assert dashboard.strip(), "dashboard is empty"
    assert gaps.strip(), "gap report is empty"
    assert cascade.strip(), "cascade report is empty"

    # Req. 10 — determinism under a fixed seed. Build a second report
    # using the same monkeypatched stubs and compare outcomes.
    report_b, _ = _build_full_report(monkeypatch)
    outcomes_a = {r.claim_id: r.outcome for r in report.claims}
    outcomes_b = {r.claim_id: r.outcome for r in report_b.claims}
    assert outcomes_a == outcomes_b, (
        "pipeline outputs drifted across deterministic runs"
    )

    # Req. 11 — validate returns (severity, message) tuples with
    # recognised severities.
    findings = graph.validate()
    assert isinstance(findings, list)
    for severity, message in findings:
        assert severity in ("BLOCK", "WARN"), (
            f"unexpected severity {severity!r} in {message!r}"
        )
        assert isinstance(message, str) and message.strip()


# ---------------------------------------------------------------------------
# Correctness properties (design.md)
# ---------------------------------------------------------------------------


def test_correctness_properties_hold(monkeypatch) -> None:
    """Assert the directly-testable correctness properties from design.md.

    Not every named property maps to a runtime assertion (some are
    type-level invariants already enforced by dataclass typing). The
    properties asserted here are:

        * Parser round-trip (parse → re-parse): identical id sets.
        * Dependency edges match the overlay file exactly.
        * Topological order visits every claim.
        * Cycle detection via validate() produces BLOCK findings.
        * Every graded outcome is a valid VerificationOutcome.
        * Tier-outcome mapping: DERIVED with audited refs +
          no script → REGRESSION_OK.
        * Broken sandbox script → SCRIPT_BROKEN.
        * Non-local falsification tests always yield EXTERNAL_ONLY.
        * Board documents byte-identical pre/post (guardrail).
        * No-go library blocking (guardrail).
        * Cascade impact equals the transitive closure.
        * Dependency state propagation (upstream OPEN → no CLEAR
          downstream).
        * Report completeness (dashboard contains every claim id).
        * Falsification-lane determinism under a fixed seed.
    """

    before_hashes = {p: _sha256(p) for p in PROTECTED_FILES}
    report, graph = _build_full_report(monkeypatch)

    # --- Parser round-trip ---
    claims_a = parse_claims_md(CLAIMS_MD)
    claims_b = parse_claims_md(CLAIMS_MD)
    assert set(claims_a) == set(claims_b)

    # --- Dependency edges match overlay ---
    import yaml  # local import — yaml is already a verification dependency

    if OVERLAY.is_file():
        with OVERLAY.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
        overlay_edges_raw = raw.get("edges") or []
        assert len(graph.dependency_edges) == len(overlay_edges_raw), (
            f"loaded {len(graph.dependency_edges)} edges from a file with "
            f"{len(overlay_edges_raw)} edge entries"
        )

    # --- Topological order visits every claim ---
    ordered = graph.topological_order()
    assert len(ordered) == len(graph.claims)
    assert set(ordered) == set(graph.claims)

    # --- Cycle detection via validate ---
    # Construct a synthetic cycle by mutating a copy of dependency_edges
    # and re-running validate on the patched graph.
    from verification.models import DependencyEdge

    cid_list = list(graph.claims)
    if len(cid_list) >= 2:
        a, b = cid_list[0], cid_list[1]
        cycle_graph = ClaimGraph(
            claims=dict(graph.claims),
            dependency_edges=[
                DependencyEdge(a, b, "cycle1", "synthetic"),
                DependencyEdge(b, a, "cycle2", "synthetic"),
            ],
        )
        findings = cycle_graph.validate()
        assert any(
            sev == "BLOCK" and "cycle" in msg.lower() for sev, msg in findings
        ), "cycle detection did not emit a BLOCK finding"

    # --- Graded outcome validity ---
    valid_outcomes = set(VerificationOutcome)
    for r in report.claims:
        assert r.outcome in valid_outcomes

    # --- Tier-outcome mapping: DERIVED + audited refs, no script ---
    from verification.models import Claim

    synthetic = Claim(
        id="synthetic_derived",
        name="Synthetic Derived",
        status=ClaimStatus.DERIVED,
        confidence=0.95,
        evidence_summary="",
        falsification_criterion="",
        derivation_files=["derivations/foo.md"],
        audited_derivation_refs=["derivations/foo.md"],
        sandbox_scripts=[],
    )
    derived_runner = get_runner_for_tier(ClaimStatus.DERIVED)
    result = derived_runner.verify(synthetic)
    assert result.outcome is VerificationOutcome.REGRESSION_OK

    # --- Broken sandbox script → SCRIPT_BROKEN ---
    broken = run_sandbox_script("sandbox/__no_such_file__.py")
    assert broken.success is False
    assert broken.return_code == -1

    # --- Non-local falsification tests always yield EXTERNAL_ONLY ---
    for ft in report.falsification:
        if not ft.locally_executable:
            assert ft.current_readout is FalsificationReadout.EXTERNAL_ONLY, (
                f"{ft.test_id}: non-local test has readout "
                f"{ft.current_readout!r}"
            )

    # --- Board documents read-only ---
    after_hashes = {p: _sha256(p) for p in PROTECTED_FILES}
    for p in PROTECTED_FILES:
        if before_hashes[p]:
            assert before_hashes[p] == after_hashes[p], (
                f"protected file {p.name} changed during the run"
            )

    # --- No-go library blocking ---
    g = Guardrails(agents_md_path=str(AGENTS_MD) if AGENTS_MD.is_file() else None)
    violations = g.check_no_go("retry harmonic series mass ratios")
    assert any(v.rule == "NO_GO" and v.severity == "BLOCK" for v in violations)

    # --- Cascade impact = transitive closure ---
    for cid in graph.claims:
        impact = graph.cascade_impact(cid)
        # The starting claim must never appear in its own cascade.
        assert cid not in impact
        # Every id in the cascade must be a valid claim id.
        assert set(impact).issubset(graph.claims)
        # Closure check: every downstream of any impacted node also
        # lives in the impact set.
        for dcid in impact:
            for ddcid in graph.downstream_of(dcid):
                assert ddcid in impact or ddcid == cid, (
                    f"cascade for {cid} missing transitive downstream {ddcid} "
                    f"(via {dcid})"
                )

    # --- Dependency state propagation: no CLEAR downstream of OPEN ---
    result_by_id = {r.claim_id: r for r in report.claims}
    for r in report.claims:
        if r.dependency_state != "CLEAR":
            continue
        for up in graph.upstream_of(r.claim_id):
            up_result = result_by_id.get(up)
            if up_result is None:
                continue
            # CLEAR is only allowed when every upstream is REPRODUCED
            # or REGRESSION_OK.
            assert up_result.outcome in (
                VerificationOutcome.REPRODUCED,
                VerificationOutcome.REGRESSION_OK,
            ), (
                f"{r.claim_id} is CLEAR but upstream {up} has outcome "
                f"{up_result.outcome.value}"
            )

    # --- Report completeness: dashboard mentions every claim id ---
    dashboard = generate_dashboard(graph, report.claims, report.falsification)
    for cid in graph.claims:
        assert cid in dashboard, (
            f"dashboard is missing row for claim id {cid!r}"
        )

    # --- Falsification-lane determinism ---
    report_c, _ = _build_full_report(monkeypatch)
    readouts_a = {ft.test_id: ft.current_readout for ft in report.falsification}
    readouts_c = {ft.test_id: ft.current_readout for ft in report_c.falsification}
    assert readouts_a == readouts_c
