"""TEST 5 — Gravitational Wave Dispersion (external watch).

The framework predicts gravitational-wave propagation consistent with
standard general relativity: no frequency-dependent GW dispersion at the
scales accessible to LIGO / Virgo / LISA. A detection of
frequency-dependent dispersion at the Propagation-Framework-predicted
scale would falsify that position.

No local sandbox script can detect a gravitational wave. This test
always emits ``EXTERNAL_ONLY`` and never ``PASS``.

See:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.7, Req. 5.4
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 3 (Falsification Pipeline)
- `papers/FALSIFICATION_PAPER_DRAFT.md` TEST 5
"""

from __future__ import annotations

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)


TEST_ID = "TEST_5"
TEST_NAME = "Gravitational Wave Dispersion"

FRAMEWORK_PREDICTION = (
    "Gravitational-wave dispersion is consistent with standard general "
    "relativity — no measurable frequency-dependent travel-time shift "
    "at accessible GW detector sensitivities."
)
FALSIFICATION_CRITERION = (
    "LIGO / Virgo / LISA detection of frequency-dependent GW dispersion "
    "at the Propagation-Framework-predicted scale."
)


def run_test5() -> FalsificationTest:
    """Return the external-watch record for TEST 5.

    No subprocess is executed. The current readout is ``EXTERNAL_ONLY``
    unconditionally.
    """

    return FalsificationTest(
        test_id=TEST_ID,
        name=TEST_NAME,
        locally_executable=False,
        framework_prediction=FRAMEWORK_PREDICTION,
        falsification_criterion=FALSIFICATION_CRITERION,
        current_readout=FalsificationReadout.EXTERNAL_ONLY,
        details=(
            "No locally executable harness exists for this test. "
            "Resolution depends on external GW-detector observations "
            "(LIGO, Virgo, LISA)."
        ),
    )
