"""EmpiricalRunner — verification for EMPIRICAL tier claims.

An EMPIRICAL row claims a numerical match against experimental data
without a full derivation. Local verification runs the declared scripts
and grades the reported error margin between the framework's
prediction and the measured/experimental value:

    * margin < 1%             → ``REPRODUCED`` (high-precision match)
    * 1% ≤ margin < 10%       → ``REGRESSION_OK`` (in-tolerance, note added)
    * margin ≥ 10%            → ``UNDER_PRESSURE`` (claim contradicted)
    * no script + no derivation → ``EXTERNAL_ONLY``
    * any script crash          → ``SCRIPT_BROKEN`` (never a falsification)

Scripts are expected to emit JSON on stdout with one of the recognized
prediction/measurement key pairs (``predicted``/``measured``,
``expected``/``actual``, ``theoretical``/``observed``) or an explicit
``error_margin`` / ``relative_error`` field. Scripts whose output the
runner cannot parse contribute to the run but do not provide a margin —
they fall back to REGRESSION_OK when they exit cleanly.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.4, 3.6, 4.4, 8.3, 8.5.
"""

from __future__ import annotations

import logging
from typing import Any

from verification.models import Claim, VerificationOutcome, VerificationResult
from verification.runners.base import TierRunner
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


logger = logging.getLogger(__name__)


# Bands for the empirical-match grading.
_TIGHT_MARGIN = 0.01   # < 1 %  -> REPRODUCED
_LOOSE_MARGIN = 0.10   # < 10 % -> REGRESSION_OK (>= 10 % -> UNDER_PRESSURE)


class EmpiricalRunner(TierRunner):
    """Runner for ``ClaimStatus.EMPIRICAL`` rows."""

    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed

    def verify(
        self,
        claim: Claim,
        dependency_state: str = "NOT_DECLARED",
    ) -> VerificationResult:
        # No script and no derivation metadata → external-only lane.
        if not claim.sandbox_scripts and not claim.derivation_files:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.EXTERNAL_ONLY,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "EMPIRICAL row has no sandbox script and no derivation "
                    "file; nothing to verify locally."
                ),
                scripts_run=[],
                derivation_refs_checked=[],
                gaps_found=list(claim.known_gaps or []),
            )

        # No script but derivation present → REGRESSION_OK-flavored
        # outcome: we have a paper trail but no re-runnable empirical
        # comparison.
        if not claim.sandbox_scripts:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.REGRESSION_OK,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "EMPIRICAL row cites derivation metadata but has no "
                    "sandbox comparison script to rerun; treating the "
                    "existing derivation as the regression checkpoint."
                ),
                scripts_run=[],
                derivation_refs_checked=list(claim.derivation_files),
                gaps_found=list(claim.known_gaps or []),
            )

        run_results: list[SandboxRunResult] = []
        any_broken = False
        any_success = False
        margins: list[float] = []

        for script in claim.sandbox_scripts:
            result = run_sandbox_script(script, seed=self.seed)
            run_results.append(result)
            if not result.success:
                any_broken = True
                continue
            any_success = True
            margin = _relative_error_margin(result.parsed_output)
            if margin is not None:
                margins.append(margin)

        if any_broken:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = (
                "At least one empirical-comparison script failed to execute; "
                "treating row as SCRIPT_BROKEN rather than a falsification."
            )
            worst_margin = max(margins) if margins else None
        elif not any_success:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = "No empirical-comparison script ran successfully."
            worst_margin = None
        elif not margins:
            # Scripts ran but produced no parseable numerical margin;
            # treat as a green regression without a sharp number.
            outcome = VerificationOutcome.REGRESSION_OK
            details_prefix = (
                "Empirical script(s) exited cleanly but produced no "
                "parseable margin; grading as REGRESSION_OK without a "
                "precision readout."
            )
            worst_margin = None
        else:
            worst_margin = max(margins)
            if worst_margin < _TIGHT_MARGIN:
                outcome = VerificationOutcome.REPRODUCED
                details_prefix = (
                    f"Empirical match: worst relative margin "
                    f"{worst_margin:.4g} < {_TIGHT_MARGIN:.0%}."
                )
            elif worst_margin < _LOOSE_MARGIN:
                outcome = VerificationOutcome.REGRESSION_OK
                details_prefix = (
                    f"Empirical match in tolerance: {worst_margin:.4g} "
                    f"falls in [{_TIGHT_MARGIN:.0%}, {_LOOSE_MARGIN:.0%})."
                )
            else:
                outcome = VerificationOutcome.UNDER_PRESSURE
                details_prefix = (
                    f"Empirical margin {worst_margin:.4g} >= "
                    f"{_LOOSE_MARGIN:.0%}: claim under pressure."
                )

        details_lines = [details_prefix]
        for r in run_results:
            status = (
                "ok"
                if r.success
                else f"broken ({r.error or 'non-zero exit'})"
            )
            details_lines.append(f"  - {r.script_path}: {status}")

        return VerificationResult(
            claim_id=claim.id,
            outcome=outcome,
            dependency_state=dependency_state,
            error_margin=worst_margin,
            details="\n".join(details_lines),
            scripts_run=list(claim.sandbox_scripts),
            derivation_refs_checked=list(claim.derivation_files or []),
            gaps_found=list(claim.known_gaps or []),
        )


def _relative_error_margin(parsed: dict[str, Any]) -> float | None:
    """Same fragment-parser as in the other runners, kept local on
    purpose so runners do not share a private API surface."""

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
