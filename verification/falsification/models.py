"""Falsification-lane data models.

The falsification pipeline is a separate lane from the claim-level
verification outcomes. A falsification test asks a different question:
"is there, right now, a local experiment whose result would contradict
the Propagation Framework's prediction?" The answer is one of four
readouts — PARTIAL_LOCAL, UNDER_PRESSURE, EXTERNAL_ONLY, or
SCRIPT_BROKEN — and never a binary PASS/FAIL.

See:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.7 and Req. 5 (falsification pipeline)
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 3 (Falsification Pipeline)
- `papers/FALSIFICATION_PAPER_DRAFT.md` (the five tests)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class FalsificationReadout(Enum):
    """The four falsification-lane readouts.

    Intentionally distinct from :class:`verification.models.VerificationOutcome`
    so that downstream tooling (dashboards, reports) cannot accidentally
    collapse a falsification readout into a claim-level pass.

    Values:
        PARTIAL_LOCAL: A local harness ran cleanly and produced evidence
            that is consistent with the Propagation Framework prediction,
            but local evidence alone cannot fully close the falsification
            criterion.
        UNDER_PRESSURE: A local harness ran cleanly and produced evidence
            that tensions the Propagation Framework prediction — the test
            is pointing at a candidate falsification.
        EXTERNAL_ONLY: The test is not locally executable. Its resolution
            depends on an external measurement (LHC, JUNO, LISA, etc.).
            Explicitly NOT a pass: a non-discovery so far is not a
            confirmation.
        SCRIPT_BROKEN: The local harness failed to execute (missing
            dependency, traceback, timeout). Never promoted to a
            falsification — broken infrastructure is a tooling issue.
    """

    PARTIAL_LOCAL = "PARTIAL_LOCAL"
    UNDER_PRESSURE = "UNDER_PRESSURE"
    EXTERNAL_ONLY = "EXTERNAL_ONLY"
    SCRIPT_BROKEN = "SCRIPT_BROKEN"


@dataclass
class FalsificationTest:
    """Record of one falsification-test run.

    Attributes:
        test_id: Stable identifier like ``"TEST_1"`` through ``"TEST_5"``.
        name: Human-readable test name.
        locally_executable: True for tests that wrap a local sandbox
            script (TEST 1, TEST 2). False for external-watch entries
            (TEST 3, 4, 5) which never emit PASS.
        framework_prediction: One-sentence statement of what the
            Propagation Framework predicts for this test.
        falsification_criterion: One-sentence statement of what
            measurement would falsify the prediction.
        current_readout: The :class:`FalsificationReadout` produced by
            the latest run (or the current external-watch state).
        details: Free-text summary of what happened — numerical result,
            traceback snippet, JSON snapshot, etc.
        timestamp: When the record was produced. Defaults to UTC now.
    """

    test_id: str
    name: str
    locally_executable: bool
    framework_prediction: str
    falsification_criterion: str
    current_readout: FalsificationReadout
    details: str = ""
    timestamp: datetime | None = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
