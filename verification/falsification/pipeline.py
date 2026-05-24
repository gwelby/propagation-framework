"""Falsification pipeline orchestrator.

Runs the two local falsification tests (TEST 1 EEG-CSD, TEST 2 neutrino
Koide), records the three external-only watch entries (TEST 3 fourth
generation, TEST 4 tau g-2, TEST 5 GW dispersion), and produces a
human-readable pressure map.

The pressure map is explicitly NOT a binary survival theorem. It is a
tally of falsification-lane readouts plus per-test highlights, and it
names the external-only tests that remain open until an external
measurement lands.

See:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 5 (falsification pipeline), Req. 5.5 (pressure report shape)
- `.kiro/specs/propagation-framework-verification/design.md`
  Component 3 (Falsification Pipeline)
"""

from __future__ import annotations

from collections import Counter

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.falsification.test1_eeg_csd import run_test1
from verification.falsification.test2_neutrino_koide import run_test2
from verification.falsification.test3_fourth_gen import run_test3
from verification.falsification.test4_tau_g2 import run_test4
from verification.falsification.test5_gw_dispersion import run_test5


class FalsificationPipeline:
    """Orchestrate the five falsification-test records.

    The pipeline is stateless by design: each call re-runs the local
    tests and re-records the external-only entries. That keeps the
    falsification lane honest — nothing is cached across runs at this
    layer.
    """

    def run_local_tests(
        self, seed: int | None = None
    ) -> list[FalsificationTest]:
        """Run the two locally executable tests.

        Args:
            seed: Optional integer seed forwarded to the sandbox runner
                for deterministic execution.

        Returns:
            ``[test1_result, test2_result]`` — always two records in
            the stated order.
        """

        return [run_test1(seed=seed), run_test2(seed=seed)]

    def check_external_watch(self) -> list[FalsificationTest]:
        """Return the three external-only watch records.

        Each entry is ``EXTERNAL_ONLY`` by construction; no subprocess
        executes.
        """

        return [run_test3(), run_test4(), run_test5()]

    def run_all(self, seed: int | None = None) -> list[FalsificationTest]:
        """Run the local tests and append the external-watch records.

        Returns the five falsification records in TEST_1..TEST_5 order.
        """

        return [*self.run_local_tests(seed=seed), *self.check_external_watch()]

    def framework_pressure_report(
        self, tests: list[FalsificationTest]
    ) -> str:
        """Aggregate ``tests`` into a human-readable pressure map.

        The report intentionally does not emit PASS/FAIL language. It
        produces:

        * A tally of each :class:`FalsificationReadout` value.
        * A one-line highlight per test with readout and test name.
        * An explicit note that external-only tests remain open until
          an external measurement lands.
        """

        counts = Counter(t.current_readout for t in tests)
        lines: list[str] = []
        lines.append("Framework Pressure Map")
        lines.append("=" * 72)
        lines.append(f"Total falsification tests recorded: {len(tests)}")
        lines.append("")
        lines.append("Readout tally:")
        for readout in FalsificationReadout:
            lines.append(f"  - {readout.value}: {counts.get(readout, 0)}")
        lines.append("")
        lines.append("Per-test highlights:")
        if not tests:
            lines.append("  (no tests recorded)")
        for t in tests:
            lane = "local" if t.locally_executable else "external-only"
            lines.append(
                f"  - {t.test_id} [{t.current_readout.value}] ({lane}): {t.name}"
            )
            first_detail_line = (t.details or "").strip().splitlines()
            if first_detail_line:
                lines.append(f"      detail: {first_detail_line[0]}")
        lines.append("")
        lines.append(
            "Note: EXTERNAL_ONLY tests (TEST 3, 4, 5 when locally "
            "non-executable) remain open until an external measurement "
            "— LHC/HL-LHC data, a tau g-2 precision result, or a "
            "LIGO/Virgo/LISA dispersion analysis — resolves them. "
            "External-only entries are never recorded as supportive "
            "evidence by this pipeline; a non-discovery is not a "
            "confirmation."
        )
        lines.append(
            "Note: SCRIPT_BROKEN is a tooling failure, never a "
            "falsification. Fix the harness and re-run."
        )
        return "\n".join(lines)
