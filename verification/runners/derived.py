"""DerivedRunner — verification for DERIVED tier claims.

Per Requirement 3 and 4, a DERIVED claim is either:

    * A **theorem island** supported by one or more audit-qualified
      derivation files and no local sandbox script. Running the
      harness against such a row should emit ``REGRESSION_OK`` with a
      note that no local reproduction script exists (Req. 4.7).
    * A **script-backed** result with at least one sandbox regression
      script. Running those scripts is the direct reproduction; all
      green → ``REPRODUCED`` (Req. 3.2). Any crash → ``SCRIPT_BROKEN``
      (Req. 3.4) — *never* a falsification. A script whose numerical
      output contradicts the claim (more than 5 % off the expected
      value declared in the script output) → ``UNDER_PRESSURE``
      (Req. 3.6 / 8.5). Contradiction detection here is scaffolded:
      the full guardrail enforcer in Section 5/6 of the spec handles
      the richer truth-order checks.
    * A mix of the two — we run whatever scripts exist and require an
      audited ref to fall back to ``REGRESSION_OK`` when no script
      reproduces the core result.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.2-3.4, 4.1, 4.7, 8.3, 8.5.
- `.kiro/specs/propagation-framework-verification/design.md`
  Algorithm 2 (Derived Claim Numerical Verification).
"""

from __future__ import annotations

import logging
from typing import Any

from verification.models import Claim, VerificationOutcome, VerificationResult
from verification.runners.base import TierRunner
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


logger = logging.getLogger(__name__)


# Relative tolerance used to flag a script-reported value as
# contradicting the claim (Req. 8.5). Scripts that want to override the
# default may emit their own ``tolerance`` field in the JSON output.
_DEFAULT_RELATIVE_TOLERANCE = 0.05


class DerivedRunner(TierRunner):
    """Runner for ``ClaimStatus.DERIVED`` rows."""

    def __init__(
        self,
        support_manifest: dict[str, Any] | None = None,
        seed: int | None = None,
    ) -> None:
        """Args:
            support_manifest: Optional dict of manifest metadata keyed
                by claim id. The runner itself only reads the claim's
                ``audited_derivation_refs`` list that the parser
                populated from the manifest; the full dict is kept for
                future annotations (e.g. per-ref audit dates).
            seed: Fixed seed forwarded to :func:`run_sandbox_script`
                for deterministic runs.
        """

        self.support_manifest = support_manifest or {}
        self.seed = seed

    def verify(
        self,
        claim: Claim,
        dependency_state: str = "NOT_DECLARED",
    ) -> VerificationResult:
        # Case 1: audit-qualified derivation refs with no local script.
        # We cannot locally reproduce the core result, but the audited
        # derivation stands; emit REGRESSION_OK per Req. 4.7.
        if claim.audited_derivation_refs and not claim.sandbox_scripts:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.REGRESSION_OK,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "Theorem-backed DERIVED claim: audited derivation refs "
                    "present; no local reproduction script to rerun."
                ),
                scripts_run=[],
                derivation_refs_checked=list(claim.audited_derivation_refs),
                gaps_found=[],
            )

        # Case 2: no script and no audited refs — we have nothing to run
        # and nothing to cite. That is a structural gap on this row;
        # surface it as EXTERNAL_ONLY so the dashboard flags it without
        # ever mutating the board.
        if not claim.sandbox_scripts:
            return VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.EXTERNAL_ONLY,
                dependency_state=dependency_state,
                error_margin=None,
                details=(
                    "DERIVED row has neither audited derivation refs nor "
                    "sandbox scripts; nothing to reproduce locally."
                ),
                scripts_run=[],
                derivation_refs_checked=[],
                gaps_found=[],
            )

        # Case 3: run whatever scripts are declared.
        run_results: list[SandboxRunResult] = []
        any_broken = False
        any_pressure = False
        any_success = False
        error_margins: list[float] = []
        contradictions: list[str] = []

        for script in claim.sandbox_scripts:
            try:
                result = run_sandbox_script(script, seed=self.seed)
            except Exception as exc:  # defensive — run_sandbox_script should not raise
                logger.warning(
                    "DerivedRunner: unexpected exception from run_sandbox_script"
                    " on %s: %s",
                    script,
                    exc,
                )
                any_broken = True
                run_results.append(
                    SandboxRunResult(
                        script_path=script,
                        success=False,
                        stdout="",
                        stderr=f"{type(exc).__name__}: {exc}",
                        return_code=-1,
                        error=type(exc).__name__,
                    )
                )
                continue

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
                        f"{script}: relative margin {margin:.4g} exceeds "
                        f"tolerance {tolerance:.4g}"
                    )

        # Outcome precedence: SCRIPT_BROKEN > UNDER_PRESSURE > REPRODUCED
        # > REGRESSION_OK. A broken script is never a falsification.
        if any_broken and not any_success:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details = "All sandbox scripts failed to execute cleanly."
        elif any_broken:
            # Some scripts ran, some broke. Per Req. 3.4 we treat the
            # row as SCRIPT_BROKEN because the harness cannot fully
            # execute the claim's declared support.
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details = "At least one sandbox script failed to execute cleanly."
        elif any_pressure:
            outcome = VerificationOutcome.UNDER_PRESSURE
            details = "; ".join(contradictions)
        elif claim.audited_derivation_refs:
            # Scripts passed and the row has audited derivation backing
            # — direct reproduction is available; emit REPRODUCED.
            outcome = VerificationOutcome.REPRODUCED
            details = (
                f"All {len(claim.sandbox_scripts)} sandbox script(s) "
                f"succeeded; audited derivation refs present."
            )
        else:
            outcome = VerificationOutcome.REPRODUCED
            details = (
                f"All {len(claim.sandbox_scripts)} sandbox script(s) "
                f"succeeded; no audited derivation ref cited."
            )

        return VerificationResult(
            claim_id=claim.id,
            outcome=outcome,
            dependency_state=dependency_state,
            error_margin=max(error_margins) if error_margins else None,
            details=_compose_details(details, run_results),
            scripts_run=list(claim.sandbox_scripts),
            derivation_refs_checked=list(claim.audited_derivation_refs),
            gaps_found=contradictions,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _relative_error_margin(parsed: dict[str, Any]) -> float | None:
    """Best-effort "relative error" extraction from a parsed JSON dict.

    Recognizes several common key conventions:

        * Explicit margin: ``error_margin``, ``relative_error``,
          ``rel_err`` — used directly (absolute value, treated as
          fractional, i.e. 0.03 == 3%).
        * Predicted vs. measured pair: ``predicted`` + ``measured``.
          Margin = |predicted - measured| / max(|measured|, eps).
        * Expected vs. actual pair: ``expected`` + ``actual``.

    Returns ``None`` when no recognizable numerical pair is found.
    Percentage values are assumed to already be fractional
    (``error_margin: 0.03`` means 3 %), not percent-scaled.
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
    """Per-script tolerance override, or the module default."""

    val = parsed.get("tolerance")
    if isinstance(val, (int, float)) and val > 0:
        return float(val)
    return _DEFAULT_RELATIVE_TOLERANCE


def _compose_details(prefix: str, results: list[SandboxRunResult]) -> str:
    """Human-readable details: prefix + per-script status."""

    lines = [prefix]
    for r in results:
        status = (
            "ok"
            if r.success
            else f"broken ({r.error or 'non-zero exit'})"
        )
        lines.append(f"  - {r.script_path}: {status}")
    return "\n".join(lines)
