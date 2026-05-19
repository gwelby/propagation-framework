"""Abstract base class and factory for per-tier verification runners.

Each status tier in ``CLAIMS.md`` gets its own runner implementation:

    * :class:`verification.runners.derived.DerivedRunner`       — DERIVED
    * :class:`verification.runners.conditional.ConditionalRunner`
      — CONDITIONAL and PARTIAL_DERIVATION
    * :class:`verification.runners.argued.ArguedRunner`         — ARGUED
    * :class:`verification.runners.empirical.EmpiricalRunner`   — EMPIRICAL
    * :class:`verification.runners.frontier.FrontierRunner`     — INTUITION,
      OPEN, NO_GO

Runners are pure functions over a :class:`Claim` plus a small
``dependency_state`` string. They read sandbox scripts and derivation
metadata; they never mutate :class:`Claim` records, they never write to
``CLAIMS.md`` / ``ACTIVE_ISSUES.md`` / ``WHATS_NEXT.md`` / ``derivations/``,
and they never upgrade confidence scores (Req. 6).

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3 (graded outcomes), Req. 4 (tier-appropriate runners).
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 2 (Verification Runners).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from verification.models import Claim, ClaimStatus, VerificationResult


class TierRunner(ABC):
    """Abstract base class for per-tier verification runners.

    Subclasses must implement :meth:`verify`. The ``dependency_state``
    argument is a short string — one of ``"CLEAR"``, ``"OPEN"``,
    ``"UNDER_PRESSURE"``, or ``"NOT_DECLARED"`` — summarizing upstream
    results. Runners use it as context (e.g. to distinguish a clean
    REGRESSION_OK from one whose upstream is already under pressure),
    but they must never silently promote it into a graded outcome.
    """

    @abstractmethod
    def verify(
        self,
        claim: Claim,
        dependency_state: str = "NOT_DECLARED",
    ) -> VerificationResult:
        """Run tier-appropriate verification and return a graded result.

        Implementations must return a :class:`VerificationResult` whose
        ``outcome`` is one of the six :class:`VerificationOutcome`
        values. Broken scripts must map to ``SCRIPT_BROKEN``; they must
        never be treated as a falsification.
        """


def get_runner_for_tier(status: ClaimStatus) -> TierRunner:
    """Factory: map each claim status tier to its runner instance.

    The mapping is:

        * ``DERIVED``              -> :class:`DerivedRunner`
        * ``CONDITIONAL``,
          ``PARTIAL_DERIVATION``  -> :class:`ConditionalRunner`
        * ``ARGUED``               -> :class:`ArguedRunner`
        * ``EMPIRICAL``            -> :class:`EmpiricalRunner`
        * ``INTUITION``,
          ``OPEN``,
          ``NO_GO``               -> :class:`FrontierRunner`

    Raises:
        ValueError: if ``status`` is not a member of
            :class:`ClaimStatus` (defensive; should never fire for a
            parser-produced :class:`Claim`).
    """

    # Imports are local to avoid a circular-import spider at module load
    # time (the concrete runners import from this module).
    from verification.runners.argued import ArguedRunner
    from verification.runners.conditional import ConditionalRunner
    from verification.runners.derived import DerivedRunner
    from verification.runners.empirical import EmpiricalRunner
    from verification.runners.frontier import FrontierRunner

    if status is ClaimStatus.DERIVED:
        return DerivedRunner()
    if status in (ClaimStatus.CONDITIONAL, ClaimStatus.PARTIAL_DERIVATION):
        return ConditionalRunner()
    if status is ClaimStatus.ARGUED:
        return ArguedRunner()
    if status is ClaimStatus.EMPIRICAL:
        return EmpiricalRunner()
    if status in (ClaimStatus.INTUITION, ClaimStatus.OPEN, ClaimStatus.NO_GO):
        return FrontierRunner()

    raise ValueError(f"no runner registered for status {status!r}")
