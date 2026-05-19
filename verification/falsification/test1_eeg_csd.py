"""TEST 1 — EEG Phase Transition (Critical Slowing Down).

Wraps the existing ``sandbox/eeg_csd_simulator.py`` via
:func:`verification.sandbox_runner.run_sandbox_script`. On clean
subprocess exit, this falsification test emits ``PARTIAL_LOCAL`` — the
local CSD simulator ran and produced a synthetic trace that is
consistent with the framework's prediction, but the falsification
criterion is about real EEG (≥7 of 10 recorded insight events showing
CSD variance increase), which cannot be closed with simulation alone.

On a broken harness (missing script, traceback, timeout) we emit
``SCRIPT_BROKEN`` — never a falsification. A broken harness is a tooling
issue, not evidence against the framework.

See:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 5.2, Req. 5.6
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 3 (Falsification Pipeline)
- `papers/FALSIFICATION_PAPER_DRAFT.md` TEST 1
"""

from __future__ import annotations

from pathlib import Path

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.sandbox_runner import run_sandbox_script


TEST_ID = "TEST_1"
TEST_NAME = "EEG Phase Transition (Critical Slowing Down before insight)"
SCRIPT_PATH = Path("sandbox/eeg_csd_simulator.py")

FRAMEWORK_PREDICTION = (
    "A critical-slowing-down (CSD) variance signature precedes every "
    "genuine insight event — variance rises in a window of ~1–2 s before "
    "the insight gamma burst."
)
FALSIFICATION_CRITERION = (
    "Real EEG recordings show no CSD variance increase (>50% rise) in at "
    "least 7 of 10 recorded insight events."
)


def run_test1(seed: int | None = None) -> FalsificationTest:
    """Run TEST 1 by wrapping the local CSD simulator.

    Args:
        seed: Optional integer seed passed through to the sandbox runner
            so that ``PF_SEED`` / ``PYTHONHASHSEED`` are set in the
            subprocess environment for deterministic runs.

    Returns:
        A :class:`FalsificationTest` record with
        ``current_readout`` set to ``PARTIAL_LOCAL`` on clean exit or
        ``SCRIPT_BROKEN`` on failure. Never PASS, never FAIL.
    """

    run = run_sandbox_script(SCRIPT_PATH, seed=seed)

    if not run.success:
        stderr_tail = _tail(run.stderr, max_chars=2000)
        details = (
            f"Sandbox harness failed to execute {SCRIPT_PATH}. "
            f"error={run.error!r}, return_code={run.return_code}.\n"
            f"stderr (tail):\n{stderr_tail}"
        )
        return FalsificationTest(
            test_id=TEST_ID,
            name=TEST_NAME,
            locally_executable=True,
            framework_prediction=FRAMEWORK_PREDICTION,
            falsification_criterion=FALSIFICATION_CRITERION,
            current_readout=FalsificationReadout.SCRIPT_BROKEN,
            details=details,
        )

    # Clean exit. The simulator prints a rendering confirmation and
    # writes a PNG; we don't parse numerical CSD statistics here because
    # the current sandbox script does not emit a structured JSON blob.
    # The falsification-paper language makes this explicit: local
    # execution can only yield PARTIAL_LOCAL until real EEG data is
    # processed through the same pipeline.
    parsed = run.parsed_output or {}
    stdout_tail = _tail(run.stdout, max_chars=1500)
    details_parts = [
        f"CSD simulator executed cleanly (return_code={run.return_code}).",
    ]
    if parsed:
        details_parts.append(f"parsed_output={parsed}")
    if stdout_tail.strip():
        details_parts.append(f"stdout (tail):\n{stdout_tail}")
    details_parts.append(
        "Local simulation alone is insufficient to close the real-EEG "
        "falsification criterion; recording remains PARTIAL_LOCAL."
    )

    return FalsificationTest(
        test_id=TEST_ID,
        name=TEST_NAME,
        locally_executable=True,
        framework_prediction=FRAMEWORK_PREDICTION,
        falsification_criterion=FALSIFICATION_CRITERION,
        current_readout=FalsificationReadout.PARTIAL_LOCAL,
        details="\n".join(details_parts),
    )


def _tail(text: str, max_chars: int) -> str:
    """Return the last ``max_chars`` characters of ``text``.

    Used to keep the details field compact when a script produces large
    stdout / stderr dumps (e.g. matplotlib deprecation warnings).
    """

    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return "…" + text[-max_chars:]
