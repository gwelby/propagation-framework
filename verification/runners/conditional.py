"""ConditionalRunner — verification for CONDITIONAL and PARTIAL_DERIVATION tiers.

A CONDITIONAL / PARTIAL_DERIVATION row declares one or more *named
hypotheses* that block the row from being promoted to DERIVED. The
runner's job is to:

    1. Check, for every named hypothesis, whether it has been
       explicitly closed in a Codex-audited derivation file (via
       :func:`verification.hypothesis_checker.check_hypothesis_closure`).
    2. Optionally run any supporting sandbox scripts the row declares
       so regressions against the local lemma stay visible.
    3. Emit ``HYPOTHESIS_OPEN`` while any hypothesis remains open —
       even if every script passes (Req. 3.5, 4.2). A passing script
       never promotes an open-hypothesis row to ``REGRESSION_OK``.
    4. Emit ``REGRESSION_OK`` only when *every* hypothesis is closed
       and scripts either pass or are absent.
    5. Emit ``SCRIPT_BROKEN`` when scripts fail to execute, so the
       harness never silently swallows a broken support script.

The runner never mutates the claim status or confidence.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.5, Req. 4.2.
- `.kiro/specs/propagation-framework-verification/design.md`
  Algorithm 3 (Conditional Claim Gap Tracker).
"""

from __future__ import annotations

import logging
from pathlib import Path

from verification.hypothesis_checker import check_hypothesis_closure
from verification.models import Claim, VerificationOutcome, VerificationResult
from verification.runners.base import TierRunner
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


logger = logging.getLogger(__name__)


class ConditionalRunner(TierRunner):
    """Runner for ``ClaimStatus.CONDITIONAL`` and ``PARTIAL_DERIVATION``."""

    def __init__(
        self,
        workspace_root: Path | None = None,
        seed: int | None = None,
    ) -> None:
        """Args:
            workspace_root: Optional base directory forwarded to
                :func:`check_hypothesis_closure` so relative derivation
                paths resolve against the caller's repo root.
            seed: Fixed seed forwarded to :func:`run_sandbox_script`.
        """

        self.workspace_root = workspace_root
        self.seed = seed

    def verify(
        self,
        claim: Claim,
        dependency_state: str = "NOT_DECLARED",
    ) -> VerificationResult:
        # Step 1: hypothesis closure check.
        hypothesis_status: dict[str, str] = {}
        for hyp in claim.named_hypotheses or []:
            closed = check_hypothesis_closure(
                hyp,
                claim.derivation_files,
                workspace_root=self.workspace_root,
            )
            hypothesis_status[hyp] = "CLOSED" if closed else "OPEN"

        open_hypotheses = [
            h for h, s in hypothesis_status.items() if s == "OPEN"
        ]

        # Step 2: run any supporting scripts.
        run_results: list[SandboxRunResult] = []
        any_broken = False
        any_success = False
        for script in claim.sandbox_scripts or []:
            result = run_sandbox_script(script, seed=self.seed)
            run_results.append(result)
            if not result.success:
                any_broken = True
            else:
                any_success = True

        # Step 3: decide the outcome.
        #
        # Precedence, top-down:
        #
        #   * SCRIPT_BROKEN when every declared script failed (we need
        #     at least one green run to treat the support layer as
        #     "available"; partial-broken with any-green still returns
        #     SCRIPT_BROKEN per Req. 3.4 "any fails with runtime error").
        #   * HYPOTHESIS_OPEN when any hypothesis is still open, even if
        #     scripts pass (Req. 3.5, 4.2). The "supporting evidence"
        #     never overrides an open hypothesis.
        #   * REGRESSION_OK when every hypothesis is closed *and*
        #     scripts pass (or are absent).
        if claim.sandbox_scripts and any_broken:
            outcome = VerificationOutcome.SCRIPT_BROKEN
            details_prefix = (
                "At least one supporting sandbox script failed to execute; "
                "treating row as SCRIPT_BROKEN rather than a hypothesis or "
                "falsification signal."
            )
        elif open_hypotheses:
            outcome = VerificationOutcome.HYPOTHESIS_OPEN
            details_prefix = (
                f"Open hypotheses: {', '.join(open_hypotheses)}. "
                f"Supporting scripts do not promote the row past an open "
                f"hypothesis."
            )
        elif hypothesis_status:
            # Every named hypothesis resolved to CLOSED.
            outcome = VerificationOutcome.REGRESSION_OK
            details_prefix = (
                f"All {len(hypothesis_status)} named hypotheses CLOSED in "
                f"audited files; support layer holds."
            )
        else:
            # No named hypotheses declared. That is a data gap on the
            # row (the parser / validator WARNs on it). The harness
            # cannot emit HYPOTHESIS_OPEN with an empty hypothesis set,
            # so emit REGRESSION_OK when scripts pass, EXTERNAL_ONLY
            # when we have neither hypotheses nor scripts.
            if not run_results:
                outcome = VerificationOutcome.EXTERNAL_ONLY
                details_prefix = (
                    "CONDITIONAL row declares no named hypotheses and no "
                    "sandbox scripts; nothing to verify locally."
                )
            elif any_success:
                outcome = VerificationOutcome.REGRESSION_OK
                details_prefix = (
                    "No named hypotheses declared; supporting scripts passed."
                )
            else:
                outcome = VerificationOutcome.SCRIPT_BROKEN
                details_prefix = (
                    "No named hypotheses declared and supporting scripts "
                    "failed."
                )

        details_lines = [details_prefix]
        if hypothesis_status:
            details_lines.append(
                "Hypothesis closure: "
                + ", ".join(
                    f"{h}={s}" for h, s in hypothesis_status.items()
                )
            )
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
            error_margin=None,
            details="\n".join(details_lines),
            scripts_run=list(claim.sandbox_scripts or []),
            derivation_refs_checked=list(claim.derivation_files or []),
            gaps_found=list(open_hypotheses),
        )
