"""TEST 3 — Fourth Generation Absolute Exclusion (external watch).

The Propagation Framework predicts that no fourth fermion generation is
stable at accessible energies — the three-generations theorem is meant
to be absolute, not a tuning that could shift with future data. A
discovery of a fourth-generation fermion at the LHC or a future
collider would falsify that prediction.

This test is **not locally executable**. There is no Python script in
``sandbox/`` that could produce or refute a fourth-generation discovery
on its own. The test therefore always emits ``EXTERNAL_ONLY`` and
**never** emits ``PASS``: a non-discovery so far is not a confirmation,
it is simply the current external-watch state.

See:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.7, Req. 5.4
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 3 (Falsification Pipeline)
- `papers/FALSIFICATION_PAPER_DRAFT.md` TEST 3
"""

from __future__ import annotations

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)


TEST_ID = "TEST_3"
TEST_NAME = "Fourth Generation Absolute Exclusion"

FRAMEWORK_PREDICTION = (
    "No fourth fermion generation is stable at accessible energies; the "
    "three-generation structure is absolute under Axiom 3 (Minimal "
    "Winding) / the N=3 bridge."
)
FALSIFICATION_CRITERION = (
    "Discovery of a fourth-generation fermion (quark or lepton) at the "
    "LHC or a future collider at any mass, any coupling."
)


def run_test3() -> FalsificationTest:
    """Return the external-watch record for TEST 3.

    No subprocess is executed. The current readout is ``EXTERNAL_ONLY``
    unconditionally: only an external measurement can move this test.
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
            "Resolution depends on external collider data (LHC Run 3+, "
            "HL-LHC, future colliders). Non-discovery is tracked, not "
            "marked as a pass."
        ),
    )
