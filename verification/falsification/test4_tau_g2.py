"""TEST 4 — Tau Anomalous Magnetic Moment (external watch).

The framework predicts that the tau g-2 anomaly ``a_τ = (g_τ − 2) / 2``
remains consistent with the Standard Model augmented by the
Propagation-Framework coherence-ceiling corrections. A future precision
measurement of ``a_τ`` that deviates from the Standard-Model prediction
by more than 3σ in a direction the framework cannot accommodate would
falsify that position.

No local sandbox script can measure ``a_τ``. This test always emits
``EXTERNAL_ONLY`` and never ``PASS``.

See:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.7, Req. 5.4
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 3 (Falsification Pipeline)
- `papers/FALSIFICATION_PAPER_DRAFT.md` TEST 4
"""

from __future__ import annotations

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)


TEST_ID = "TEST_4"
TEST_NAME = "Tau Anomalous Magnetic Moment (a_τ)"

FRAMEWORK_PREDICTION = (
    "Tau g-2 is consistent with the Standard Model plus Propagation "
    "Framework corrections from the coherence-ceiling torsion sector."
)
FALSIFICATION_CRITERION = (
    "Precision measurement of a_τ deviating > 3σ from the SM prediction "
    "in a direction inconsistent with the Propagation Framework's "
    "coherence-ceiling correction."
)


def run_test4() -> FalsificationTest:
    """Return the external-watch record for TEST 4.

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
            "Resolution depends on an external precision measurement of "
            "the tau anomalous magnetic moment."
        ),
    )
