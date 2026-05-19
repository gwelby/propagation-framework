"""Integration tests: error-handling behavior (Task 10.4).

Each test validates one failure mode of the verification pipeline:

    * ``test_broken_sandbox_script_maps_to_script_broken`` — a sandbox
      script that raises on import/execution must surface as
      :attr:`VerificationOutcome.SCRIPT_BROKEN`, never
      :attr:`UNDER_PRESSURE`. Broken harness is tooling, not evidence.
    * ``test_upstream_hypothesis_open_never_becomes_dependency_clear`` —
      a DERIVED downstream whose only explicit upstream is
      HYPOTHESIS_OPEN must never see ``dependency_state == "CLEAR"``.
    * ``test_numerical_result_outside_tolerance_flags_under_pressure`` —
      a synthetic EMPIRICAL script reporting a 50% relative error must
      grade to :attr:`UNDER_PRESSURE` (not REPRODUCED, not SCRIPT_BROKEN).
    * ``test_no_go_approach_blocks_verification_plan`` —
      :meth:`Guardrails.check_no_go` must produce a BLOCK violation on
      a text that references a documented no-go approach.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3, Req. 6, Req. 7, Req. 8.
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 10.4.
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

import pytest

from verification.claim_graph import ClaimGraph
from verification.guardrails import Guardrails, GuardrailViolation
from verification.models import (
    Claim,
    ClaimStatus,
    DependencyEdge,
    VerificationOutcome,
    VerificationResult,
)
from verification.pipeline import summarize_dependency_state
from verification.runners.derived import DerivedRunner
from verification.runners.empirical import EmpiricalRunner


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_claim(
    claim_id: str,
    *,
    status: ClaimStatus,
    sandbox_scripts: list[str] | None = None,
    confidence: float = 0.85,
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


# ---------------------------------------------------------------------------
# Test 1: broken sandbox script
# ---------------------------------------------------------------------------


def test_broken_sandbox_script_maps_to_script_broken(tmp_path: Path) -> None:
    """A script that raises must yield SCRIPT_BROKEN, not UNDER_PRESSURE.

    Creates a synthetic sandbox script that raises a RuntimeError at
    module load time (which also covers import-time failures). Builds a
    DERIVED claim pointing at it and dispatches via DerivedRunner; the
    outcome must be SCRIPT_BROKEN.
    """

    script = tmp_path / "broken_sandbox.py"
    script.write_text(
        textwrap.dedent(
            """
            raise RuntimeError("intentional failure for SCRIPT_BROKEN coverage")
            """
        ).lstrip("\n"),
        encoding="utf-8",
    )

    claim = _make_claim(
        "broken",
        status=ClaimStatus.DERIVED,
        confidence=0.92,
        sandbox_scripts=[str(script)],
    )

    runner = DerivedRunner(seed=42)
    result = runner.verify(claim, dependency_state="NOT_DECLARED")

    assert result.outcome is VerificationOutcome.SCRIPT_BROKEN, (
        f"expected SCRIPT_BROKEN, got {result.outcome}"
    )
    # Belt-and-braces: must NOT be mapped to UNDER_PRESSURE (broken
    # tooling is not a falsification).
    assert result.outcome is not VerificationOutcome.UNDER_PRESSURE
    assert str(script) in result.scripts_run


# ---------------------------------------------------------------------------
# Test 2: upstream HYPOTHESIS_OPEN → downstream not CLEAR
# ---------------------------------------------------------------------------


def test_upstream_hypothesis_open_never_becomes_dependency_clear() -> None:
    """A DERIVED downstream must never be CLEAR when upstream is HYPOTHESIS_OPEN.

    Builds a two-node graph, injects a HYPOTHESIS_OPEN result for the
    upstream, and asserts the summariser never emits CLEAR for the
    downstream — regardless of the downstream's own status.
    """

    upstream = _make_claim(
        "up", status=ClaimStatus.CONDITIONAL, confidence=0.85
    )
    downstream = _make_claim(
        "down",
        status=ClaimStatus.DERIVED,
        confidence=0.92,
        audited_derivation_refs=["derivations/fake.md"],
    )
    graph = ClaimGraph(
        claims={"up": upstream, "down": downstream},
        dependency_edges=[
            DependencyEdge(
                upstream="up",
                downstream="down",
                reason="fixture",
                source="fixture",
            ),
        ],
    )
    upstream_result = VerificationResult(
        claim_id="up",
        outcome=VerificationOutcome.HYPOTHESIS_OPEN,
        dependency_state="NOT_DECLARED",
        error_margin=None,
        details="fixture: upstream hypothesis is open",
        scripts_run=[],
        derivation_refs_checked=[],
        gaps_found=["fixture_hyp"],
    )

    state = summarize_dependency_state("down", graph, [upstream_result])
    assert state != "CLEAR", (
        f"downstream must not be CLEAR when upstream is HYPOTHESIS_OPEN; "
        f"got {state!r}"
    )
    assert state == "OPEN"


# ---------------------------------------------------------------------------
# Test 3: numerical result outside tolerance → UNDER_PRESSURE
# ---------------------------------------------------------------------------


def test_numerical_result_outside_tolerance_flags_under_pressure(
    tmp_path: Path,
) -> None:
    """An EMPIRICAL script with 50% error must grade to UNDER_PRESSURE.

    The EmpiricalRunner thresholds are:
        * margin < 1 %             → REPRODUCED
        * 1 % ≤ margin < 10 %      → REGRESSION_OK
        * margin ≥ 10 %            → UNDER_PRESSURE

    This script reports ``predicted=1.0, measured=1.5`` → ~33% error
    (|1.0 - 1.5| / 1.5 = 0.3333...), well above the 10% band.
    """

    script = tmp_path / "empirical_pressure.py"
    script.write_text(
        textwrap.dedent(
            """
            import json
            print(json.dumps({"predicted": 1.0, "measured": 1.5}))
            """
        ).lstrip("\n"),
        encoding="utf-8",
    )

    claim = _make_claim(
        "empirical_under_pressure",
        status=ClaimStatus.EMPIRICAL,
        confidence=0.80,
        sandbox_scripts=[str(script)],
    )

    runner = EmpiricalRunner(seed=42)
    result = runner.verify(claim, dependency_state="NOT_DECLARED")

    assert result.outcome is VerificationOutcome.UNDER_PRESSURE, (
        f"expected UNDER_PRESSURE, got {result.outcome} "
        f"(error_margin={result.error_margin})"
    )
    assert result.error_margin is not None
    assert result.error_margin > 0.10, (
        f"error margin {result.error_margin} unexpectedly within tolerance"
    )


# ---------------------------------------------------------------------------
# Test 4: no-go approach → BLOCK
# ---------------------------------------------------------------------------


def test_no_go_approach_blocks_verification_plan() -> None:
    """A plan that re-attempts a documented no-go must yield a BLOCK.

    Uses the hardcoded ``HARDCODED_NO_GO_FALLBACK`` entry
    ``"harmonic series mass ratios"`` (which is baked in and doesn't
    require AGENTS.md parsing). The Guardrails instance is built with
    no AGENTS.md path so the fallback alone drives the check.
    """

    guardrails = Guardrails(agents_md_path=None)

    approach = "I'll try harmonic series mass ratios again this week."
    violations = guardrails.check_no_go(approach)

    assert violations, "no BLOCK emitted for a documented no-go approach"
    assert all(isinstance(v, GuardrailViolation) for v in violations)
    assert any(v.severity == "BLOCK" for v in violations), (
        f"no BLOCK-severity violation emitted: {violations}"
    )
    matched = [v for v in violations if "harmonic series mass ratios" in v.details]
    assert matched, (
        f"BLOCK did not cite 'harmonic series mass ratios'; violations: "
        f"{[v.details for v in violations]}"
    )

    # Sanity: an innocuous approach yields no violation.
    assert guardrails.check_no_go("compute the one-loop vacuum propagator") == []
