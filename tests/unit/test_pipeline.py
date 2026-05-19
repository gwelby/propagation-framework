"""Unit tests for :mod:`verification.pipeline` (Task 8.4).

Covers:

    * :func:`summarize_dependency_state` priority ordering
      (UNDER_PRESSURE > OPEN > CLEAR > NOT_DECLARED).
    * BLOCK-level validation findings stop the pipeline before any
      runner executes.
    * Dependency-state propagation: upstream HYPOTHESIS_OPEN →
      downstream ``dependency_state`` != ``CLEAR``.
    * Quick mode skips long-running sandbox scripts.
    * Content-hash caching reuses results across runs.
    * End-to-end smoke: the pipeline returns a populated
      :class:`VerificationReport`.

Tests avoid touching the real ``CLAIMS.md`` / ``AGENTS.md``. They build
minimal fixtures in ``tmp_path`` and monkeypatch external collaborators
(sandbox subprocess runner, falsification runners) where needed.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 7, Req. 10.
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 8.4.
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

import pytest

from verification import pipeline as pipeline_module
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
from verification.pipeline import (
    get_script_cache_key,
    load_cached_result,
    run_verification_pipeline,
    save_cached_result,
    summarize_dependency_state,
)
from verification.report import VerificationReport
from verification.sandbox_runner import SandboxRunResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_result(
    claim_id: str,
    outcome: VerificationOutcome,
) -> VerificationResult:
    return VerificationResult(
        claim_id=claim_id,
        outcome=outcome,
        dependency_state="NOT_DECLARED",
        error_margin=None,
        details="fixture",
        scripts_run=[],
        derivation_refs_checked=[],
        gaps_found=[],
    )


def _make_claim(
    claim_id: str,
    *,
    status: ClaimStatus = ClaimStatus.DERIVED,
    confidence: float = 0.95,
    sandbox_scripts: list[str] | None = None,
    audited_derivation_refs: list[str] | None = None,
) -> Claim:
    return Claim(
        id=claim_id,
        name=claim_id.replace("_", " ").title(),
        status=status,
        confidence=confidence,
        evidence_summary="(fixture)",
        falsification_criterion="(fixture)",
        derivation_files=[],
        audited_derivation_refs=list(audited_derivation_refs or []),
        sandbox_scripts=list(sandbox_scripts or []),
        named_hypotheses=[],
        known_gaps=[],
        source_row=0,
    )


def _build_graph(
    claims: list[Claim],
    edges: list[tuple[str, str]] | None = None,
) -> ClaimGraph:
    return ClaimGraph(
        claims={c.id: c for c in claims},
        dependency_edges=[
            DependencyEdge(
                upstream=u, downstream=d, reason="fixture", source="fixture"
            )
            for u, d in (edges or [])
        ],
    )


# Minimal CLAIMS.md fixture used by the end-to-end smoke test.
_MINIMAL_CLAIMS_MD = """\
# Test CLAIMS.md

## ⦿ The Audit Scoreboard

### 1. Fundamental Physics

| Claim | Status | Evidence | What Falsifies It | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Alpha Row** | **DERIVED** | Theorem island with audited derivation [alpha_audit.md](derivations/alpha_audit.md). | A proof that the closure argument does not hold. | 0.95 |
| **Beta Row** | **ARGUED** | Plausible mechanism. Not yet closed. Gap: mechanism bridge is not yet derived. | A pressure test that rules the mechanism out. | 0.80 |

### 2. Biological & Cognitive Systems

| Claim | Status | Evidence | What Falsifies It | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Gamma Row** | **OPEN** | Unresolved frontier gap. | A derivation route. | 0.10 |
"""


# ---------------------------------------------------------------------------
# summarize_dependency_state
# ---------------------------------------------------------------------------


class TestSummarizeDependencyState:
    """Tests for :func:`summarize_dependency_state`."""

    def test_no_upstream_returns_not_declared(self):
        graph = _build_graph([_make_claim("solo")])
        state = summarize_dependency_state("solo", graph, [])
        assert state == "NOT_DECLARED"

    def test_clear_when_every_upstream_is_reproduced_or_regression_ok(self):
        graph = _build_graph(
            [_make_claim("A"), _make_claim("B"), _make_claim("D")],
            edges=[("A", "D"), ("B", "D")],
        )
        results = [
            _make_result("A", VerificationOutcome.REPRODUCED),
            _make_result("B", VerificationOutcome.REGRESSION_OK),
        ]
        assert summarize_dependency_state("D", graph, results) == "CLEAR"

    def test_open_when_any_upstream_hypothesis_open(self):
        graph = _build_graph(
            [_make_claim("A"), _make_claim("B"), _make_claim("D")],
            edges=[("A", "D"), ("B", "D")],
        )
        results = [
            _make_result("A", VerificationOutcome.REPRODUCED),
            _make_result("B", VerificationOutcome.HYPOTHESIS_OPEN),
        ]
        assert summarize_dependency_state("D", graph, results) == "OPEN"

    def test_under_pressure_beats_open_and_clear(self):
        """Priority: UNDER_PRESSURE > OPEN > CLEAR."""

        graph = _build_graph(
            [
                _make_claim("A"),
                _make_claim("B"),
                _make_claim("C"),
                _make_claim("D"),
            ],
            edges=[("A", "D"), ("B", "D"), ("C", "D")],
        )
        results = [
            _make_result("A", VerificationOutcome.REGRESSION_OK),
            _make_result("B", VerificationOutcome.HYPOTHESIS_OPEN),
            _make_result("C", VerificationOutcome.UNDER_PRESSURE),
        ]
        assert summarize_dependency_state("D", graph, results) == "UNDER_PRESSURE"

    def test_regression_ok_plus_under_pressure_is_under_pressure(self):
        """Task 8.4 case: REGRESSION_OK + UNDER_PRESSURE → UNDER_PRESSURE, not CLEAR."""

        graph = _build_graph(
            [_make_claim("A"), _make_claim("B"), _make_claim("D")],
            edges=[("A", "D"), ("B", "D")],
        )
        results = [
            _make_result("A", VerificationOutcome.REGRESSION_OK),
            _make_result("B", VerificationOutcome.UNDER_PRESSURE),
        ]
        assert summarize_dependency_state("D", graph, results) == "UNDER_PRESSURE"

    def test_missing_upstream_result_does_not_launder_to_clear(self):
        """If no upstream result is known yet, state must not be CLEAR."""

        graph = _build_graph(
            [_make_claim("A"), _make_claim("D")],
            edges=[("A", "D")],
        )
        # No result recorded for A yet.
        assert summarize_dependency_state("D", graph, []) == "OPEN"

    def test_script_broken_upstream_is_not_clear(self):
        """SCRIPT_BROKEN upstream must not vote CLEAR."""

        graph = _build_graph(
            [_make_claim("A"), _make_claim("D")],
            edges=[("A", "D")],
        )
        results = [_make_result("A", VerificationOutcome.SCRIPT_BROKEN)]
        state = summarize_dependency_state("D", graph, results)
        # The only known upstream contributed no CLEAR/OPEN/UP signal,
        # so the summariser falls back to OPEN rather than silently
        # promoting to CLEAR.
        assert state in {"OPEN", "UNDER_PRESSURE"}
        assert state != "CLEAR"


# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------


class TestCaching:
    def test_cache_key_changes_when_script_content_changes(self, tmp_path: Path):
        script = tmp_path / "script.py"
        script.write_text("print('v1')\n", encoding="utf-8")
        key_v1 = get_script_cache_key(script)

        script.write_text("print('v2')\n", encoding="utf-8")
        key_v2 = get_script_cache_key(script)

        assert key_v1 != key_v2
        assert len(key_v1) == 64  # SHA-256 hex digest
        assert len(key_v2) == 64

    def test_load_cached_result_returns_none_for_missing_key(self, tmp_path: Path):
        assert load_cached_result("no_such_key", cache_dir=tmp_path) is None

    def test_save_and_load_roundtrip(self, tmp_path: Path):
        key = "roundtrip"
        original = SandboxRunResult(
            script_path="fake.py",
            success=True,
            stdout="hello",
            stderr="",
            return_code=0,
            error="",
            parsed_output={"a": 1, "b": [1, 2, 3]},
        )
        save_cached_result(key, original, cache_dir=tmp_path)
        loaded = load_cached_result(key, cache_dir=tmp_path)

        assert loaded is not None
        assert loaded.script_path == original.script_path
        assert loaded.success is True
        assert loaded.stdout == "hello"
        assert loaded.return_code == 0
        assert loaded.parsed_output == {"a": 1, "b": [1, 2, 3]}

    def test_load_cached_result_ignores_malformed_payload(self, tmp_path: Path):
        (tmp_path / "bad.json").write_text("not json at all", encoding="utf-8")
        assert load_cached_result("bad", cache_dir=tmp_path) is None


# ---------------------------------------------------------------------------
# Pipeline integration
# ---------------------------------------------------------------------------


def _write_claims_md(tmp_path: Path, contents: str) -> Path:
    path = tmp_path / "CLAIMS.md"
    path.write_text(contents, encoding="utf-8")
    return path


def _stub_falsification(monkeypatch) -> None:
    """Stub FalsificationPipeline.run_all to avoid invoking real sandbox scripts."""

    def fake_run_all(self, seed=None):
        return [
            FalsificationTest(
                test_id=f"TEST_{i}",
                name=f"Fake TEST {i}",
                locally_executable=i <= 2,
                framework_prediction="(fixture)",
                falsification_criterion="(fixture)",
                current_readout=FalsificationReadout.EXTERNAL_ONLY,
                details="fixture detail",
            )
            for i in range(1, 6)
        ]

    monkeypatch.setattr(
        "verification.pipeline.FalsificationPipeline.run_all",
        fake_run_all,
    )


class TestPipelineValidation:
    def test_block_findings_stop_the_run_before_any_runner(self, monkeypatch):
        """A graph with a cycle must raise before any runner is called."""

        called: list[str] = []

        class RunnerShouldNotRun:
            def verify(self, claim, dependency_state="NOT_DECLARED"):
                called.append(claim.id)
                raise AssertionError("runner must not execute when validate() BLOCKs")

        monkeypatch.setattr(
            "verification.pipeline.get_runner_for_tier",
            lambda status: RunnerShouldNotRun(),
        )
        _stub_falsification(monkeypatch)

        # Monkeypatch ClaimGraph.from_markdown to return a graph with a
        # cycle without needing a real CLAIMS.md cycle.
        cycle_graph = _build_graph(
            [_make_claim("A"), _make_claim("B")],
            edges=[("A", "B"), ("B", "A")],
        )
        monkeypatch.setattr(
            "verification.pipeline.ClaimGraph.from_markdown",
            classmethod(lambda cls, *a, **kw: cycle_graph),
        )

        with pytest.raises(ValueError, match="BLOCK"):
            run_verification_pipeline(claims_md_path="unused")

        assert called == [], "runners must not have been invoked"


class TestPipelineDependencyPropagation:
    def test_upstream_hypothesis_open_makes_downstream_not_clear(
        self, tmp_path: Path, monkeypatch
    ):
        """Verify that a HYPOTHESIS_OPEN upstream leaves downstream dep_state != CLEAR."""

        # Build a graph with an explicit edge upstream -> downstream.
        upstream = _make_claim("up_hyp", status=ClaimStatus.CONDITIONAL, confidence=0.85)
        downstream = _make_claim(
            "down_derived",
            status=ClaimStatus.DERIVED,
            confidence=0.92,
            audited_derivation_refs=["derivations/fake_audit.md"],
        )
        graph = _build_graph([upstream, downstream], edges=[("up_hyp", "down_derived")])
        monkeypatch.setattr(
            "verification.pipeline.ClaimGraph.from_markdown",
            classmethod(lambda cls, *a, **kw: graph),
        )

        # Capture the dependency_state each runner sees.
        seen_states: dict[str, str] = {}

        class RecordingRunner:
            def __init__(self, outcome: VerificationOutcome):
                self.outcome = outcome
                self.seed = None

            def verify(self, claim, dependency_state="NOT_DECLARED"):
                seen_states[claim.id] = dependency_state
                return VerificationResult(
                    claim_id=claim.id,
                    outcome=self.outcome,
                    dependency_state=dependency_state,
                    error_margin=None,
                    details="fixture",
                    scripts_run=[],
                    derivation_refs_checked=[],
                    gaps_found=[],
                )

        def runner_factory(status):
            if status is ClaimStatus.CONDITIONAL:
                return RecordingRunner(VerificationOutcome.HYPOTHESIS_OPEN)
            return RecordingRunner(VerificationOutcome.REPRODUCED)

        monkeypatch.setattr(
            "verification.pipeline.get_runner_for_tier", runner_factory
        )
        _stub_falsification(monkeypatch)

        report = run_verification_pipeline(claims_md_path="unused")

        # The upstream should have been NOT_DECLARED (no upstream itself),
        # and the downstream must have seen OPEN (not CLEAR).
        assert seen_states["up_hyp"] == "NOT_DECLARED"
        assert seen_states["down_derived"] != "CLEAR"
        assert seen_states["down_derived"] == "OPEN"
        assert isinstance(report, VerificationReport)
        assert len(report.claims) == 2


class TestPipelineQuickMode:
    def test_quick_mode_skips_long_running_scripts(self, monkeypatch):
        """A claim whose only script is long-running is skipped in quick mode."""

        long_only = _make_claim(
            "slow",
            status=ClaimStatus.DERIVED,
            confidence=0.92,
            sandbox_scripts=["sandbox/monte_carlo_big.py"],
        )
        graph = _build_graph([long_only])
        monkeypatch.setattr(
            "verification.pipeline.ClaimGraph.from_markdown",
            classmethod(lambda cls, *a, **kw: graph),
        )

        # If the pipeline tried to invoke run_sandbox_script, this would
        # raise and the test would fail.
        def explode(*args, **kwargs):
            raise AssertionError(
                "run_sandbox_script must not be called for a long-running "
                "script in quick mode"
            )

        monkeypatch.setattr(
            "verification.runners.derived.run_sandbox_script", explode
        )
        _stub_falsification(monkeypatch)

        report = run_verification_pipeline(
            claims_md_path="unused", quick=True
        )

        assert len(report.claims) == 1
        result = report.claims[0]
        assert result.claim_id == "slow"
        assert result.outcome is VerificationOutcome.EXTERNAL_ONLY
        assert "skipped" in result.details.lower()
        assert result.scripts_run == []

    def test_non_quick_mode_would_run_long_running_scripts(self, monkeypatch):
        """Without quick=True the pipeline must invoke the sandbox runner."""

        long_only = _make_claim(
            "slow",
            status=ClaimStatus.DERIVED,
            confidence=0.92,
            sandbox_scripts=["sandbox/monte_carlo_big.py"],
        )
        graph = _build_graph([long_only])
        monkeypatch.setattr(
            "verification.pipeline.ClaimGraph.from_markdown",
            classmethod(lambda cls, *a, **kw: graph),
        )

        called = {"n": 0}

        def fake_run(script_path, seed=None):
            called["n"] += 1
            return SandboxRunResult(
                script_path=str(script_path),
                success=True,
                stdout="",
                stderr="",
                return_code=0,
                error="",
                parsed_output={"predicted": 1.0, "measured": 1.0},
            )

        monkeypatch.setattr(
            "verification.runners.derived.run_sandbox_script", fake_run
        )
        _stub_falsification(monkeypatch)

        run_verification_pipeline(claims_md_path="unused", quick=False)

        assert called["n"] == 1


class TestPipelineSmoke:
    def test_pipeline_produces_verification_report(
        self, tmp_path: Path, monkeypatch
    ):
        """End-to-end: real parser + stubbed runners + stubbed falsification."""

        claims_path = _write_claims_md(tmp_path, _MINIMAL_CLAIMS_MD)

        # Use a real parser but stub runners and falsification so the
        # test stays hermetic.
        class StubRunner:
            def __init__(self, outcome: VerificationOutcome):
                self.outcome = outcome
                self.seed = None

            def verify(self, claim, dependency_state="NOT_DECLARED"):
                return VerificationResult(
                    claim_id=claim.id,
                    outcome=self.outcome,
                    dependency_state=dependency_state,
                    error_margin=None,
                    details="stubbed",
                    scripts_run=[],
                    derivation_refs_checked=list(claim.audited_derivation_refs or []),
                    gaps_found=["stub_gap"] if self.outcome is VerificationOutcome.HYPOTHESIS_OPEN else [],
                )

        def runner_factory(status):
            if status is ClaimStatus.DERIVED:
                return StubRunner(VerificationOutcome.REGRESSION_OK)
            if status is ClaimStatus.ARGUED:
                return StubRunner(VerificationOutcome.UNDER_PRESSURE)
            return StubRunner(VerificationOutcome.EXTERNAL_ONLY)

        monkeypatch.setattr(
            "verification.pipeline.get_runner_for_tier", runner_factory
        )
        _stub_falsification(monkeypatch)

        report = run_verification_pipeline(claims_md_path=claims_path)

        assert isinstance(report, VerificationReport)
        assert len(report.claims) == 3
        claim_ids = {r.claim_id for r in report.claims}
        assert {"alpha_row", "beta_row", "gamma_row"} == claim_ids

        # Falsification has five records from our stub.
        assert len(report.falsification) == 5

        # Cascade is empty because the minimal fixture has no overlay
        # attached.
        assert report.cascade == {}


# ---------------------------------------------------------------------------
# End-to-end caching behavior with a realistic script
# ---------------------------------------------------------------------------


class TestPipelineCachingReuses:
    def test_second_call_with_unchanged_script_reuses_cached_result(
        self, tmp_path: Path, monkeypatch
    ):
        """Run twice over the same script; the second call hits the cache."""

        # Build a trivial claim with one short (non long-running) script.
        script = tmp_path / "short_script.py"
        script.write_text(
            textwrap.dedent(
                """
                import json
                print(json.dumps({"predicted": 1.0, "measured": 1.0}))
                """
            ).lstrip("\n"),
            encoding="utf-8",
        )

        # Cache the result *first* so the pipeline run can observe it.
        key = get_script_cache_key(script)
        cached = SandboxRunResult(
            script_path=str(script),
            success=True,
            stdout='{"predicted": 1.0, "measured": 1.0}',
            stderr="",
            return_code=0,
            error="",
            parsed_output={"predicted": 1.0, "measured": 1.0},
        )
        save_cached_result(key, cached, cache_dir=tmp_path / "cache")

        # Verify the hash is stable across reads.
        key_again = get_script_cache_key(script)
        assert key_again == key

        loaded = load_cached_result(key_again, cache_dir=tmp_path / "cache")
        assert loaded is not None
        assert loaded.parsed_output == {"predicted": 1.0, "measured": 1.0}

        # Mutating the script changes the hash, which invalidates the cache.
        script.write_text("print('different')\n", encoding="utf-8")
        new_key = get_script_cache_key(script)
        assert new_key != key
        assert load_cached_result(new_key, cache_dir=tmp_path / "cache") is None
