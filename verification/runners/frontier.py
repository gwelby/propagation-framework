"""FrontierRunner — verification for INTUITION, OPEN, and NO_GO rows.

Frontier rows are the ones most at risk of being dropped on the floor:
they are low-confidence by design and have no obvious tier-appropriate
verification verb. Following Req. 3.8 / 4.5, the runner still emits a
valid :class:`VerificationOutcome` for every one of them and never
mutates the board status.

Behavior by tier:

    * ``INTUITION``: pattern-observation rows. Run whatever scripts
      the row declares. If they pass → ``REGRESSION_OK`` (pattern still
      holds). If they report numerical contradiction → ``UNDER_PRESSURE``
      (pattern broken). If they crash → ``SCRIPT_BROKEN``. If no script
      is declared → ``EXTERNAL_ONLY`` ("pattern is observed but not yet
      dissociated locally").

    * ``OPEN``: unresolved frontier gap. Default emission is
      ``EXTERNAL_ONLY`` (nothing to do locally). If the row declares a
      sandbox script — which would be unusual for a true OPEN row —
      we still run it and surface its graded outcome so the operator
      sees the result.

    * ``NO_GO``: documented failure retained as a negative signpost.
      Default emission is ``REGRESSION_OK`` ("no-go confirmed: we are
      intentionally not re-attempting this"). If the row declares a
      sandbox script that *does* run cleanly and does not emit an
      explicit ``"no_go_confirmed": true`` signal, we raise
      ``UNDER_PRESSURE`` because the no-go status is being challenged
      and a human should look.

The runner never calls the guardrail enforcer to block a no-go row —
that is the pipeline orchestrator's job. Here we only classify what
we saw.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.8, 4.5.
"""

from __future__ import annotations

import logging
from typing import Any

from verification.models import (
    Claim,
    ClaimStatus,
    VerificationOutcome,
    VerificationResult,
)
from verification.runners.base import TierRunner
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


logger = logging.getLogger(__name__)


_DEFAULT_RELATIVE_TOLERANCE = 0.05


class FrontierRunner(TierRunner):
    """Runner for ``INTUITION``, ``OPEN``, and ``NO_GO`` rows."""

    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed

    def verify(
        self,
        claim: Claim,
        dependency_state: str = "NOT_DECLARED",
    ) -> VerificationResult:
        if claim.status is ClaimStatus.INTUITION:
            return self._verify_intuition(claim, dependency_state)
        if claim.status is ClaimStatus.OPEN:
            return self._verify_open(claim, dependency_state)
        if claim.status is ClaimStatus.NO_GO:
            return self._verify_no_go(claim, dependency_state)

        # Defensive fallback; should never fire because the factory
        # only sends INTUITION/OPEN/NO_GO here.
        raise ValueError(
            f"FrontierRunner received unsupported status {claim.status!r} "
            f"for claim {claim.id!r}"
        )

    # ------------------------------------------------------------------
    # INTUITION
    # ------------------------------------------------------------------

    def _verify_intuition(
        self,
        claim: Claim,
        dependency_state: str,
    ) -> VerificationResult:
        if not claim.sandbox_scripts:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.EXTERNAL_ONLY,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "INTUITION row has no local sandbox script; pattern is "
                    "noted but not locally exercised."
                ),
                scripts_run=[],
                derivation_refs_checked=list(claim.derivation_files or []),
                gaps_found=list(claim.known_gaps or []),
            )

        run_results, any_broken, any_pressure, contradictions, margins = (
            _run_all(claim.sandbox_scripts, self.seed)
        )
        if any_broken:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = (
                "At least one exploratory script failed to execute; "
                "treating row as SCRIPT_BROKEN."
            )
        elif any_pressure:
            outcome = VerificationOutcome.UNDER_PRESSURE
            details_prefix = (
                "Exploratory script reports the intuition pattern is "
                "broken: " + "; ".join(contradictions)
            )
        else:
            outcome = VerificationOutcome.REGRESSION_OK
            details_prefix = (
                f"Intuition pattern still observed across "
                f"{len(claim.sandbox_scripts)} exploratory script(s)."
            )

        return _make_result(
            claim,
            outcome,
            dependency_state,
            details_prefix,
            run_results,
            margins,
            contradictions,
        )

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------

    def _verify_open(
        self,
        claim: Claim,
        dependency_state: str,
    ) -> VerificationResult:
        if not claim.sandbox_scripts:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.EXTERNAL_ONLY,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "OPEN row: no local script; unresolved frontier gap."
                ),
                scripts_run=[],
                derivation_refs_checked=list(claim.derivation_files or []),
                gaps_found=list(claim.known_gaps or []),
            )

        # Unusual — an OPEN row declaring a script. Run it and report
        # whatever it produces so we don't silently drop it.
        run_results, any_broken, any_pressure, contradictions, margins = (
            _run_all(claim.sandbox_scripts, self.seed)
        )
        if any_broken:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = "OPEN row's exploratory script failed to execute."
        elif any_pressure:
            outcome = VerificationOutcome.UNDER_PRESSURE
            details_prefix = (
                "OPEN row's exploratory script reports a contradiction: "
                + "; ".join(contradictions)
            )
        else:
            outcome = VerificationOutcome.REGRESSION_OK
            details_prefix = (
                "OPEN row's exploratory script ran cleanly; row remains "
                "OPEN on the board."
            )
        return _make_result(
            claim,
            outcome,
            dependency_state,
            details_prefix,
            run_results,
            margins,
            contradictions,
        )

    # ------------------------------------------------------------------
    # NO_GO
    # ------------------------------------------------------------------

    def _verify_no_go(
        self,
        claim: Claim,
        dependency_state: str,
    ) -> VerificationResult:
        if not claim.sandbox_scripts:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.REGRESSION_OK,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "NO_GO row confirmed: no local script re-attempts the "
                    "documented failed approach."
                ),
                scripts_run=[],
                derivation_refs_checked=list(claim.derivation_files or []),
                gaps_found=list(claim.known_gaps or []),
            )

        run_results, any_broken, any_pressure, contradictions, margins = (
            _run_all(claim.sandbox_scripts, self.seed)
        )

        if any_broken:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = (
                "NO_GO row's attached script failed to execute; treating "
                "as SCRIPT_BROKEN rather than a no-go confirmation."
            )
        else:
            # A script that ran cleanly on a NO_GO row is suspicious
            # unless it explicitly confirms the no-go.
            explicitly_confirmed = _all_results_confirm_no_go(run_results)
            if explicitly_confirmed:
                outcome = VerificationOutcome.REGRESSION_OK
                details_prefix = (
                    "NO_GO row's script ran cleanly and reports explicit "
                    '"no_go_confirmed": true; no-go status holds.'
                )
            else:
                outcome = VerificationOutcome.UNDER_PRESSURE
                details_prefix = (
                    "NO_GO row's script ran cleanly without an explicit "
                    "no-go confirmation signal; a human should review — "
                    "the documented failure mode may be being "
                    "re-challenged."
                )

        return _make_result(
            claim,
            outcome,
            dependency_state,
            details_prefix,
            run_results,
            margins,
            contradictions,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_all(
    scripts: list[str],
    seed: int | None,
) -> tuple[list[SandboxRunResult], bool, bool, list[str], list[float]]:
    """Run every script and aggregate status flags."""

    run_results: list[SandboxRunResult] = []
    any_broken = False
    any_pressure = False
    contradictions: list[str] = []
    margins: list[float] = []
    for script in scripts:
        result = run_sandbox_script(script, seed=seed)
        run_results.append(result)
        if not result.success:
            any_broken = True
            continue
        margin = _relative_error_margin(result.parsed_output)
        if margin is not None:
            margins.append(margin)
            tolerance = _tolerance_from(result.parsed_output)
            if margin > tolerance:
                any_pressure = True
                contradictions.append(
                    f"{script}: relative margin {margin:.4g} "
                    f"exceeds tolerance {tolerance:.4g}"
                )
    return run_results, any_broken, any_pressure, contradictions, margins


def _all_results_confirm_no_go(results: list[SandboxRunResult]) -> bool:
    """True iff every successful result advertises ``no_go_confirmed``."""

    if not results:
        return False
    for r in results:
        if not r.success:
            return False
        val = r.parsed_output.get("no_go_confirmed")
        if not isinstance(val, bool) or not val:
            return False
    return True


def _make_result(
    claim: Claim,
    outcome: VerificationOutcome,
    dependency_state: str,
    prefix: str,
    run_results: list[SandboxRunResult],
    margins: list[float],
    contradictions: list[str],
) -> VerificationResult:
    details_lines = [prefix]
    for r in run_results:
        status = (
            "ok"
            if r.success
            else f"broken ({r.error or 'non-zero exit'})"
        )
        details_lines.append(f"  - {r.script_path}: {status}")
    gaps = list(claim.known_gaps or [])
    gaps.extend(contradictions)
    return VerificationResult(
        claim_id=claim.id,
        outcome=outcome,
        dependency_state=dependency_state,
        error_margin=max(margins) if margins else None,
        details="\n".join(details_lines),
        scripts_run=[r.script_path for r in run_results],
        derivation_refs_checked=list(claim.derivation_files or []),
        gaps_found=gaps,
    )


def _relative_error_margin(parsed: dict[str, Any]) -> float | None:
    if not parsed:
        return None
    for key in ("error_margin", "relative_error", "rel_err"):
        val = parsed.get(key)
        if isinstance(val, (int, float)):
            return abs(float(val))
    for pred_key, meas_key in (
        ("predicted", "measured"),
        ("expected", "actual"),
        ("theoretical", "observed"),
    ):
        pred = parsed.get(pred_key)
        meas = parsed.get(meas_key)
        if isinstance(pred, (int, float)) and isinstance(meas, (int, float)):
            denom = max(abs(float(meas)), 1e-30)
            return abs(float(pred) - float(meas)) / denom
    return None


def _tolerance_from(parsed: dict[str, Any]) -> float:
    val = parsed.get("tolerance")
    if isinstance(val, (int, float)) and val > 0:
        return float(val)
    return _DEFAULT_RELATIVE_TOLERANCE
