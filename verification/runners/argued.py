"""ArguedRunner — verification for ARGUED tier claims.

An ARGUED row has a mechanism identified and plausible reasoning, but
no formal proof. The local harness contribution is pressure testing:
we run the declared sandbox scripts (which typically either reproduce
the argued numerical signal or localize a gap) and surface their
readout, along with any ``known_gaps`` the parser extracted from the
row's evidence cell.

Outcome mapping:

    * Any declared script crashes  → ``SCRIPT_BROKEN`` (never a
      falsification — Req. 3.4).
    * Any declared script reports a numerical contradiction outside
      the stated tolerance → ``UNDER_PRESSURE`` (Req. 4.3 / 8.5).
    * All scripts pass with in-tolerance numerics → ``REGRESSION_OK``.
    * No scripts available → ``EXTERNAL_ONLY`` with an explanatory
      note that no local pressure tests exist.

The runner never mutates the claim status or confidence.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.4, 3.6, 4.3, 8.3, 8.5.
"""

from __future__ import annotations

import logging
from typing import Any

from verification.models import Claim, VerificationOutcome, VerificationResult
from verification.runners.base import TierRunner
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


logger = logging.getLogger(__name__)


# Relative tolerance used to classify a script-reported value as
# contradicting the claim. Scripts may override via a ``tolerance`` key
# in their JSON output. See derived.py for the same constant; kept
# local here so the two runners can drift independently if needed.
_DEFAULT_RELATIVE_TOLERANCE = 0.05


class ArguedRunner(TierRunner):
    """Runner for ``ClaimStatus.ARGUED`` rows."""

    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed

    def verify(
        self,
        claim: Claim,
        dependency_state: str = "NOT_DECLARED",
    ) -> VerificationResult:
        if not claim.sandbox_scripts:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.EXTERNAL_ONLY,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "ARGUED row has no local pressure tests available; "
                    "no sandbox scripts declared."
                ),
                scripts_run=[],
                derivation_refs_checked=list(claim.derivation_files or []),
                gaps_found=list(claim.known_gaps or []),
            )

        run_results: list[SandboxRunResult] = []
        any_broken = False
        any_pressure = False
        any_success = False
        contradictions: list[str] = []
        error_margins: list[float] = []

        for script in claim.sandbox_scripts:
            result = run_sandbox_script(script, seed=self.seed)
            run_results.append(result)
            if not result.success:
                any_broken = True
                continue
            any_success = True
            margin = _relative_error_margin(result.parsed_output)
            if margin is not None:
                error_margins.append(margin)
                tolerance = _tolerance_from(result.parsed_output)
                if margin > tolerance:
                    any_pressure = True
                    contradictions.append(
                        f"{script}: relative margin {margin:.4g} "
                        f"exceeds tolerance {tolerance:.4g}"
                    )

        if any_broken:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = (
                "At least one pressure-test script failed to execute; "
                "treating row as SCRIPT_BROKEN rather than a falsification."
            )
        elif any_pressure:
            outcome = VerificationOutcome.UNDER_PRESSURE
            details_prefix = "; ".join(contradictions)
        elif any_success:
            outcome = VerificationOutcome.REGRESSION_OK
            details_prefix = (
                f"All {len(claim.sandbox_scripts)} pressure-test script(s) "
                f"passed within tolerance."
            )
        else:
            # Shouldn't happen: we had scripts, none were broken, none
            # were successful. Defensive fallback.
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = (
                "No successful script run observed despite declared scripts."
            )

        # Aggregate known_gaps from the parser with any script-level
        # contradictions the runner noticed.
        gaps = list(claim.known_gaps or [])
        gaps.extend(contradictions)

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
            error_margin=max(error_margins) if error_margins else None,
            details="\n".join(details_lines),
            scripts_run=list(claim.sandbox_scripts),
            derivation_refs_checked=list(claim.derivation_files or []),
            gaps_found=gaps,
        )


def _relative_error_margin(parsed: dict[str, Any]) -> float | None:
    """Extract a relative-error fraction from parsed script output.

    Mirrors :func:`verification.runners.derived._relative_error_margin`;
    duplicated locally so the two runners do not couple to each other
    through private helpers. See the derived-runner docstring for the
    recognized key conventions.
    """

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
