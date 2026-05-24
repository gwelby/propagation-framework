"""TEST 2 — Neutrino Koide Universality.

Wraps the existing ``sandbox/neutrino_koide_scan.py`` via
:func:`verification.sandbox_runner.run_sandbox_script`. The sandbox
script scans the lightest neutrino mass over its cosmologically allowed
range and reports, for both orderings, the closest Koide-ratio value
``Q_ν`` it can achieve together with the best-fit Rivero phase ``δ``.

The falsification-lane mapping is intentionally narrow: this test
pressures the **universal-Koide hypothesis** — the claim that every
Standard-Model generation-triplet should satisfy ``Q = 2/3``. Under the
current CLAIMS.md framing, the positive local result is the scope
delimitation: charged leptons satisfy Koide, neutrinos do not. That is
the EMPIRICAL 0.95-confidence row for the neutrino scan; this
falsification-test record is a distinct artefact.

Readout policy
--------------

Let ``Q_best = min(|Q_NO - 2/3|, |Q_IO - 2/3|)`` where ``Q_NO`` and
``Q_IO`` are the closest-to-``2/3`` values the scan produced for the
normal and inverted orderings respectively.

* ``Q_best > 5%`` (fractional deviation) → ``UNDER_PRESSURE`` on the
  universal-Koide hypothesis. Supports the scope-delimiting result.
* ``Q_best ≤ 5%`` → ``PARTIAL_LOCAL``. This would be a tension with the
  scope-delimiting framing; it still cannot be a clean falsification
  from local data alone (real oscillation-parameter inputs vary).
* Parse failure with clean exit → ``PARTIAL_LOCAL`` with a caveat in
  ``details``.
* Broken harness → ``SCRIPT_BROKEN``.

See:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 5.3, Req. 5.6
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 3 (Falsification Pipeline)
- `papers/FALSIFICATION_PAPER_DRAFT.md` TEST 2
"""

from __future__ import annotations

import re
from pathlib import Path

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


TEST_ID = "TEST_2"
TEST_NAME = "Neutrino Koide Universality (Q_ν = 2/3?)"
SCRIPT_PATH = Path("sandbox/neutrino_koide_scan.py")

FRAMEWORK_PREDICTION = (
    "If the Koide relation is universal across generation triplets then "
    "Q_ν = 2/3 must hold for the neutrino mass triplet (some ordering, "
    "some lightest-mass choice within cosmological bounds)."
)
FALSIFICATION_CRITERION = (
    "Measurement showing Q_ν within 1% of 2/3 — this would contradict "
    "the electromagnetic-sector-specific interpretation recorded in "
    "CLAIMS.md. Conversely, a best-fit |Q_ν − 2/3| > 5% across the full "
    "allowed mass range supports the scope-delimiting result and puts "
    "the universal-Koide hypothesis UNDER_PRESSURE."
)

# Fractional tolerance on Q_nu relative to 2/3. 5% is the boundary the
# spec calls out: above it, the universal-Koide hypothesis is under
# pressure; at or below it, the scope-delimiting result would itself
# need revisiting.
Q_TARGET = 2.0 / 3.0
Q_REL_TOL = 0.05


# Best-effort regex over the script's stdout. The script prints:
#   Normal ordering — closest Q to 2/3:
#     m1 = 0.00010 eV,  Q = 0.549...  , δ = 0.1234 ...
# and likewise for the inverted ordering. We tolerate unicode dashes by
# matching any non-word character between "ordering" and "closest".
_Q_BLOCK_RE = re.compile(
    r"(Normal|Inverted)\s+ordering\W+closest\s+Q\s+to\s+2/3\s*:\s*"
    r"[^\n]*\n\s*[^Q\n]*Q\s*=\s*([0-9]*\.?[0-9]+)",
    re.IGNORECASE,
)


def run_test2(seed: int | None = None) -> FalsificationTest:
    """Run TEST 2 by wrapping the local neutrino Koide scan.

    Args:
        seed: Optional integer seed forwarded to the sandbox runner.

    Returns:
        A :class:`FalsificationTest` with ``current_readout`` set to
        one of ``UNDER_PRESSURE`` / ``PARTIAL_LOCAL`` / ``SCRIPT_BROKEN``
        according to the readout policy documented in the module
        docstring.
    """

    run = run_sandbox_script(SCRIPT_PATH, seed=seed)

    if not run.success:
        stderr_tail = _tail(run.stderr, max_chars=2000)
        return FalsificationTest(
            test_id=TEST_ID,
            name=TEST_NAME,
            locally_executable=True,
            framework_prediction=FRAMEWORK_PREDICTION,
            falsification_criterion=FALSIFICATION_CRITERION,
            current_readout=FalsificationReadout.SCRIPT_BROKEN,
            details=(
                f"Sandbox harness failed to execute {SCRIPT_PATH}. "
                f"error={run.error!r}, return_code={run.return_code}.\n"
                f"stderr (tail):\n{stderr_tail}"
            ),
        )

    q_no, q_io = _extract_q_values(run)
    q_values = {k: v for k, v in (("Q_NO", q_no), ("Q_IO", q_io)) if v is not None}

    if not q_values:
        stdout_tail = _tail(run.stdout, max_chars=1500)
        return FalsificationTest(
            test_id=TEST_ID,
            name=TEST_NAME,
            locally_executable=True,
            framework_prediction=FRAMEWORK_PREDICTION,
            falsification_criterion=FALSIFICATION_CRITERION,
            current_readout=FalsificationReadout.PARTIAL_LOCAL,
            details=(
                "Script exited cleanly but Q_ν values could not be "
                "parsed from stdout. Recording PARTIAL_LOCAL pending a "
                "structured output contract.\n"
                f"stdout (tail):\n{stdout_tail}"
            ),
        )

    # Smallest fractional deviation from 2/3 across both orderings.
    best_label, best_q = min(
        q_values.items(), key=lambda kv: abs(kv[1] - Q_TARGET)
    )
    best_abs_dev = abs(best_q - Q_TARGET)
    best_rel_dev = best_abs_dev / Q_TARGET

    parts = [
        f"Best Koide Q from {best_label}: {best_q:.6f}",
        f"Target: 2/3 = {Q_TARGET:.6f}",
        f"|Q - 2/3| = {best_abs_dev:.4e} ({best_rel_dev * 100:.2f}%)",
    ]
    for label, value in q_values.items():
        if label != best_label:
            dev = abs(value - Q_TARGET)
            parts.append(f"{label}: Q = {value:.6f}, |Q - 2/3| = {dev:.4e}")

    if best_rel_dev > Q_REL_TOL:
        readout = FalsificationReadout.UNDER_PRESSURE
        parts.append(
            "Universal-Koide hypothesis is UNDER_PRESSURE: best Q_ν lies "
            f"> {Q_REL_TOL * 100:.0f}% from 2/3 over the scanned mass "
            "range. Consistent with the electromagnetic-sector-specific "
            "interpretation recorded in CLAIMS.md."
        )
    else:
        readout = FalsificationReadout.PARTIAL_LOCAL
        parts.append(
            f"Best Q_ν lies within {Q_REL_TOL * 100:.0f}% of 2/3; this "
            "would challenge the scope-delimiting framing and warrants "
            "a careful re-examination of inputs and the CLAIMS.md row."
        )

    return FalsificationTest(
        test_id=TEST_ID,
        name=TEST_NAME,
        locally_executable=True,
        framework_prediction=FRAMEWORK_PREDICTION,
        falsification_criterion=FALSIFICATION_CRITERION,
        current_readout=readout,
        details="\n".join(parts),
    )


def _extract_q_values(
    run: SandboxRunResult,
) -> tuple[float | None, float | None]:
    """Return ``(Q_NO, Q_IO)`` parsed from the run result.

    Parsing strategy:

    1. If ``run.parsed_output`` contains numeric ``Q_NO`` / ``Q_IO``
       entries (or a ``q_nu`` fallback), prefer those. This is how unit
       tests inject mocked values.
    2. Otherwise, regex-scan ``run.stdout`` for the script's
       "closest Q to 2/3" blocks.

    Missing values are returned as ``None``.
    """

    parsed = run.parsed_output or {}
    q_no = _maybe_float(parsed.get("Q_NO"))
    q_io = _maybe_float(parsed.get("Q_IO"))
    if q_no is None and q_io is None:
        fallback = _maybe_float(parsed.get("q_nu") or parsed.get("Q_nu"))
        if fallback is not None:
            q_no = fallback

    if q_no is None and q_io is None:
        for match in _Q_BLOCK_RE.finditer(run.stdout):
            ordering = match.group(1).lower()
            value = _maybe_float(match.group(2))
            if value is None:
                continue
            if ordering.startswith("normal"):
                q_no = value
            elif ordering.startswith("inverted"):
                q_io = value

    return q_no, q_io


def _maybe_float(value: object) -> float | None:
    """Coerce ``value`` to ``float`` if possible, else return None."""

    if value is None:
        return None
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _tail(text: str, max_chars: int) -> str:
    """Return the last ``max_chars`` characters of ``text``."""

    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return "…" + text[-max_chars:]
