"""Unit tests for the tier verification runners (Task 4.9).

Each runner is tested with synthetic inputs assembled in-process:
sandbox scripts are written into ``tmp_path`` with deterministic
stdout (JSON blobs) so we exercise the full subprocess path in
:mod:`verification.sandbox_runner` without depending on the real
``sandbox/`` directory or on network/data files.

Covered cases:

    * DerivedRunner
        - audited refs, no script → REGRESSION_OK
        - script succeeds         → REPRODUCED
        - script crashes          → SCRIPT_BROKEN (never a falsification)
        - script reports >5 %     → UNDER_PRESSURE
    * ConditionalRunner
        - open hypothesis         → HYPOTHESIS_OPEN
        - all hypotheses closed   → REGRESSION_OK
        - open hypothesis + passing script → still HYPOTHESIS_OPEN
    * ArguedRunner
        - contradiction script    → UNDER_PRESSURE
        - clean pressure tests    → REGRESSION_OK
        - no scripts              → EXTERNAL_ONLY
    * EmpiricalRunner
        - <1 %                    → REPRODUCED
        - 15 %                    → UNDER_PRESSURE
    * FrontierRunner
        - INTUITION clean script  → REGRESSION_OK
        - OPEN no script          → EXTERNAL_ONLY
        - NO_GO no script         → REGRESSION_OK
        - NO_GO script without confirmation → UNDER_PRESSURE

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3 (graded outcomes), Req. 4 (tier runners), Req. 8 (sandbox
  safety).
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 4.9.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from verification.models import (
    Claim,
    ClaimStatus,
    VerificationOutcome,
)
from verification.runners.argued import ArguedRunner
from verification.runners.base import get_runner_for_tier
from verification.runners.conditional import ConditionalRunner
from verification.runners.derived import DerivedRunner
from verification.runners.empirical import EmpiricalRunner
from verification.runners.frontier import FrontierRunner


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_script(tmp_path: Path, name: str, body: str) -> Path:
    """Write a Python script into ``tmp_path`` and return its path."""

    script = tmp_path / name
    script.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")
    return script


def _make_claim(
    claim_id: str,
    status: ClaimStatus,
    *,
    confidence: float = 0.9,
    derivation_files: list[str] | None = None,
    audited_derivation_refs: list[str] | None = None,
    sandbox_scripts: list[str] | None = None,
    named_hypotheses: list[str] | None = None,
    known_gaps: list[str] | None = None,
) -> Claim:
    return Claim(
        id=claim_id,
        name=claim_id.replace("_", " ").title(),
        status=status,
        confidence=confidence,
        evidence_summary="(synthetic test claim)",
        falsification_criterion="(synthetic)",
        derivation_files=list(derivation_files or []),
        audited_derivation_refs=list(audited_derivation_refs or []),
        sandbox_scripts=list(sandbox_scripts or []),
        named_hypotheses=list(named_hypotheses or []),
        known_gaps=list(known_gaps or []),
        source_row=0,
    )


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def test_factory_returns_runner_for_every_tier() -> None:
    """``get_runner_for_tier`` must cover all eight status tiers."""

    expected = {
        ClaimStatus.DERIVED: DerivedRunner,
        ClaimStatus.CONDITIONAL: ConditionalRunner,
        ClaimStatus.PARTIAL_DERIVATION: ConditionalRunner,
        ClaimStatus.ARGUED: ArguedRunner,
        ClaimStatus.EMPIRICAL: EmpiricalRunner,
        ClaimStatus.INTUITION: FrontierRunner,
        ClaimStatus.OPEN: FrontierRunner,
        ClaimStatus.NO_GO: FrontierRunner,
    }
    for status, cls in expected.items():
        runner = get_runner_for_tier(status)
        assert isinstance(runner, cls), (
            f"status={status} should map to {cls.__name__}, got "
            f"{type(runner).__name__}"
        )


# ---------------------------------------------------------------------------
# DerivedRunner
# ---------------------------------------------------------------------------


def test_derived_runner_audited_refs_without_script_is_regression_ok() -> None:
    """Theorem island: audited ref + no script → REGRESSION_OK."""

    claim = _make_claim(
        "alpha_theorem",
        ClaimStatus.DERIVED,
        audited_derivation_refs=["derivations/alpha_audit.md"],
    )
    result = DerivedRunner().verify(claim)
    assert result.outcome is VerificationOutcome.REGRESSION_OK
    assert result.scripts_run == []
    assert "audited derivation" in result.details.lower()


def test_derived_runner_clean_script_is_reproduced(tmp_path: Path) -> None:
    """A clean sandbox run with a JSON match → REPRODUCED."""

    script = _write_script(
        tmp_path,
        "alpha_ok.py",
        """
        import json
        print(json.dumps({"predicted": 1.0, "measured": 1.0}))
        """,
    )
    claim = _make_claim(
        "alpha_reproduced",
        ClaimStatus.DERIVED,
        sandbox_scripts=[str(script)],
        audited_derivation_refs=["derivations/alpha_audit.md"],
    )
    result = DerivedRunner().verify(claim)
    assert result.outcome is VerificationOutcome.REPRODUCED
    assert result.scripts_run == [str(script)]


def test_derived_runner_broken_script_is_script_broken(
    tmp_path: Path,
) -> None:
    """Any crash → SCRIPT_BROKEN; never a falsification."""

    script = _write_script(
        tmp_path,
        "alpha_crash.py",
        """
        raise RuntimeError("simulated crash")
        """,
    )
    claim = _make_claim(
        "alpha_broken",
        ClaimStatus.DERIVED,
        sandbox_scripts=[str(script)],
    )
    result = DerivedRunner().verify(claim)
    assert result.outcome is VerificationOutcome.SCRIPT_BROKEN
    # The runner must never emit UNDER_PRESSURE for a broken script.
    assert result.outcome is not VerificationOutcome.UNDER_PRESSURE


def test_derived_runner_out_of_tolerance_is_under_pressure(
    tmp_path: Path,
) -> None:
    """A script reporting a >5 % margin → UNDER_PRESSURE."""

    script = _write_script(
        tmp_path,
        "alpha_drift.py",
        """
        import json
        print(json.dumps({"predicted": 1.0, "measured": 1.2}))
        """,
    )
    claim = _make_claim(
        "alpha_drift",
        ClaimStatus.DERIVED,
        sandbox_scripts=[str(script)],
    )
    result = DerivedRunner().verify(claim)
    assert result.outcome is VerificationOutcome.UNDER_PRESSURE
    assert result.error_margin is not None
    assert result.error_margin > 0.05


# ---------------------------------------------------------------------------
# ConditionalRunner
# ---------------------------------------------------------------------------


def test_conditional_runner_open_hypothesis_is_hypothesis_open(
    tmp_path: Path,
) -> None:
    """A CONDITIONAL claim with an undocumented hypothesis → HYPOTHESIS_OPEN."""

    # Derivation file exists but is not audited (no ``_audit`` in name).
    deriv = tmp_path / "beta_draft.md"
    deriv.write_text(
        "# Beta draft\nH_foo remains open pending further work.\n",
        encoding="utf-8",
    )
    claim = _make_claim(
        "beta_open",
        ClaimStatus.CONDITIONAL,
        confidence=0.85,
        derivation_files=[str(deriv)],
        named_hypotheses=["H_foo"],
    )
    result = ConditionalRunner(workspace_root=tmp_path).verify(claim)
    assert result.outcome is VerificationOutcome.HYPOTHESIS_OPEN
    assert "H_foo" in result.gaps_found


def test_conditional_runner_closed_hypothesis_is_regression_ok(
    tmp_path: Path,
) -> None:
    """Audited derivation with explicit closure → REGRESSION_OK."""

    audited = tmp_path / "beta_audit.md"
    audited.write_text(
        "# Beta Codex audit\nH_foo: CLOSED\nCodex audit H_foo: passed.\n",
        encoding="utf-8",
    )
    claim = _make_claim(
        "beta_closed",
        ClaimStatus.CONDITIONAL,
        confidence=0.85,
        derivation_files=[str(audited)],
        named_hypotheses=["H_foo"],
    )
    result = ConditionalRunner(workspace_root=tmp_path).verify(claim)
    assert result.outcome is VerificationOutcome.REGRESSION_OK
    assert result.gaps_found == []


def test_conditional_runner_passing_script_does_not_override_open_hypothesis(
    tmp_path: Path,
) -> None:
    """A passing support script must NOT upgrade HYPOTHESIS_OPEN."""

    deriv = tmp_path / "beta_draft.md"
    deriv.write_text("# Beta draft\nH_foo pending.\n", encoding="utf-8")

    script = _write_script(
        tmp_path,
        "beta_support.py",
        """
        import json
        print(json.dumps({"predicted": 0.5, "measured": 0.5}))
        """,
    )
    claim = _make_claim(
        "beta_mixed",
        ClaimStatus.CONDITIONAL,
        confidence=0.85,
        derivation_files=[str(deriv)],
        named_hypotheses=["H_foo"],
        sandbox_scripts=[str(script)],
    )
    result = ConditionalRunner(workspace_root=tmp_path).verify(claim)
    assert result.outcome is VerificationOutcome.HYPOTHESIS_OPEN


# ---------------------------------------------------------------------------
# ArguedRunner
# ---------------------------------------------------------------------------


def test_argued_runner_contradiction_is_under_pressure(
    tmp_path: Path,
) -> None:
    """A pressure-test script reporting drift → UNDER_PRESSURE."""

    script = _write_script(
        tmp_path,
        "delta_pressure.py",
        """
        import json
        print(json.dumps({"predicted": 1.0, "measured": 1.3}))
        """,
    )
    claim = _make_claim(
        "delta_pressure",
        ClaimStatus.ARGUED,
        confidence=0.8,
        sandbox_scripts=[str(script)],
        known_gaps=["medium-geometry step not yet derived"],
    )
    result = ArguedRunner().verify(claim)
    assert result.outcome is VerificationOutcome.UNDER_PRESSURE
    # known_gaps plus script-level contradictions must survive.
    assert any("medium-geometry" in g for g in result.gaps_found)


def test_argued_runner_clean_pressure_is_regression_ok(tmp_path: Path) -> None:
    script = _write_script(
        tmp_path,
        "delta_clean.py",
        """
        import json
        print(json.dumps({"predicted": 0.577, "measured": 0.577}))
        """,
    )
    claim = _make_claim(
        "delta_clean",
        ClaimStatus.ARGUED,
        confidence=0.8,
        sandbox_scripts=[str(script)],
    )
    result = ArguedRunner().verify(claim)
    assert result.outcome is VerificationOutcome.REGRESSION_OK


def test_argued_runner_no_scripts_is_external_only() -> None:
    claim = _make_claim(
        "delta_external",
        ClaimStatus.ARGUED,
        confidence=0.8,
    )
    result = ArguedRunner().verify(claim)
    assert result.outcome is VerificationOutcome.EXTERNAL_ONLY


# ---------------------------------------------------------------------------
# EmpiricalRunner
# ---------------------------------------------------------------------------


def test_empirical_runner_tight_margin_is_reproduced(tmp_path: Path) -> None:
    """Error margin < 1 % → REPRODUCED."""

    script = _write_script(
        tmp_path,
        "epsilon_tight.py",
        """
        import json
        print(json.dumps({"predicted": 1.0, "measured": 1.005}))
        """,
    )
    claim = _make_claim(
        "epsilon_tight",
        ClaimStatus.EMPIRICAL,
        confidence=0.7,
        sandbox_scripts=[str(script)],
    )
    result = EmpiricalRunner().verify(claim)
    assert result.outcome is VerificationOutcome.REPRODUCED
    assert result.error_margin is not None
    assert result.error_margin < 0.01


def test_empirical_runner_large_margin_is_under_pressure(
    tmp_path: Path,
) -> None:
    """Error margin >= 10 % → UNDER_PRESSURE."""

    script = _write_script(
        tmp_path,
        "epsilon_drift.py",
        """
        import json
        print(json.dumps({"predicted": 1.0, "measured": 1.15}))
        """,
    )
    claim = _make_claim(
        "epsilon_drift",
        ClaimStatus.EMPIRICAL,
        confidence=0.7,
        sandbox_scripts=[str(script)],
    )
    result = EmpiricalRunner().verify(claim)
    assert result.outcome is VerificationOutcome.UNDER_PRESSURE
    assert result.error_margin is not None
    assert result.error_margin >= 0.10


# ---------------------------------------------------------------------------
# FrontierRunner
# ---------------------------------------------------------------------------


def test_frontier_intuition_clean_script_is_regression_ok(
    tmp_path: Path,
) -> None:
    script = _write_script(
        tmp_path,
        "eta_pattern.py",
        """
        import json
        print(json.dumps({"predicted": 0.66, "measured": 0.66}))
        """,
    )
    claim = _make_claim(
        "eta_pattern",
        ClaimStatus.INTUITION,
        confidence=0.45,
        sandbox_scripts=[str(script)],
    )
    result = FrontierRunner().verify(claim)
    assert result.outcome is VerificationOutcome.REGRESSION_OK


def test_frontier_intuition_broken_pattern_is_under_pressure(
    tmp_path: Path,
) -> None:
    script = _write_script(
        tmp_path,
        "eta_broken.py",
        """
        import json
        print(json.dumps({"predicted": 0.66, "measured": 0.80}))
        """,
    )
    claim = _make_claim(
        "eta_broken",
        ClaimStatus.INTUITION,
        confidence=0.45,
        sandbox_scripts=[str(script)],
    )
    result = FrontierRunner().verify(claim)
    assert result.outcome is VerificationOutcome.UNDER_PRESSURE


def test_frontier_open_row_without_script_is_external_only() -> None:
    claim = _make_claim(
        "theta_open",
        ClaimStatus.OPEN,
        confidence=0.1,
    )
    result = FrontierRunner().verify(claim)
    assert result.outcome is VerificationOutcome.EXTERNAL_ONLY


def test_frontier_no_go_without_script_is_regression_ok() -> None:
    """A NO_GO row with no re-attempt script → no-go confirmed → REGRESSION_OK."""

    claim = _make_claim(
        "zeta_no_go",
        ClaimStatus.NO_GO,
        confidence=0.05,
    )
    result = FrontierRunner().verify(claim)
    assert result.outcome is VerificationOutcome.REGRESSION_OK


def test_frontier_no_go_with_unconfirmed_script_is_under_pressure(
    tmp_path: Path,
) -> None:
    """A NO_GO row whose script runs cleanly without emitting
    ``no_go_confirmed`` → UNDER_PRESSURE (the no-go is being challenged)."""

    script = _write_script(
        tmp_path,
        "zeta_challenge.py",
        """
        import json
        print(json.dumps({"predicted": 1.0, "measured": 1.0}))
        """,
    )
    claim = _make_claim(
        "zeta_challenge",
        ClaimStatus.NO_GO,
        confidence=0.05,
        sandbox_scripts=[str(script)],
    )
    result = FrontierRunner().verify(claim)
    assert result.outcome is VerificationOutcome.UNDER_PRESSURE


def test_frontier_no_go_with_confirmation_is_regression_ok(
    tmp_path: Path,
) -> None:
    """An explicit ``no_go_confirmed`` signal keeps the row REGRESSION_OK."""

    script = _write_script(
        tmp_path,
        "zeta_confirm.py",
        """
        import json
        print(json.dumps({"no_go_confirmed": True}))
        """,
    )
    claim = _make_claim(
        "zeta_confirmed",
        ClaimStatus.NO_GO,
        confidence=0.05,
        sandbox_scripts=[str(script)],
    )
    result = FrontierRunner().verify(claim)
    assert result.outcome is VerificationOutcome.REGRESSION_OK
