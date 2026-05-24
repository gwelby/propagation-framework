"""Unit tests for the falsification pipeline (Task 5.6).

Covers:

    * TEST 1 (EEG CSD)
        - mocked clean-exit subprocess → PARTIAL_LOCAL
        - mocked crashing subprocess   → SCRIPT_BROKEN
    * TEST 2 (neutrino Koide)
        - mocked Q_ν ≈ 0.55            → UNDER_PRESSURE
        - mocked Q_ν ≈ 0.667           → PARTIAL_LOCAL
    * TEST 3, 4, 5 (external watch)
        - Always emit EXTERNAL_ONLY and run no subprocess.
    * FalsificationPipeline.framework_pressure_report
        - Aggregates all five readouts into a non-empty summary with
          the expected labels visible.

All tests mock :func:`verification.sandbox_runner.run_sandbox_script`
so the real ``sandbox/`` scripts are never executed here.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 5 (falsification pipeline).
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 5.6.
"""

from __future__ import annotations

from verification.falsification import (
    test1_eeg_csd,
    test2_neutrino_koide,
)
from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.falsification.pipeline import FalsificationPipeline
from verification.falsification.test3_fourth_gen import run_test3
from verification.falsification.test4_tau_g2 import run_test4
from verification.falsification.test5_gw_dispersion import run_test5
from verification.sandbox_runner import SandboxRunResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fake_success(stdout: str = "", parsed: dict | None = None) -> SandboxRunResult:
    """Build a clean-exit SandboxRunResult for monkeypatching."""

    return SandboxRunResult(
        script_path="<mock>",
        success=True,
        stdout=stdout,
        stderr="",
        return_code=0,
        error="",
        parsed_output=parsed or {},
    )


def _fake_crash(stderr: str = "Traceback (most recent call last):\nBoom") -> SandboxRunResult:
    """Build a crashing SandboxRunResult for monkeypatching."""

    return SandboxRunResult(
        script_path="<mock>",
        success=False,
        stdout="",
        stderr=stderr,
        return_code=1,
        error="NonZeroExit",
        parsed_output={},
    )


# ---------------------------------------------------------------------------
# TEST 1 — EEG CSD
# ---------------------------------------------------------------------------


def test_test1_clean_exit_emits_partial_local(monkeypatch):
    """Clean subprocess → PARTIAL_LOCAL, never PASS."""

    calls: list[tuple] = []

    def fake(script_path, seed=None):
        calls.append((script_path, seed))
        return _fake_success(stdout="Biological Proof Template rendered: ok\n")

    monkeypatch.setattr(test1_eeg_csd, "run_sandbox_script", fake)

    result = test1_eeg_csd.run_test1(seed=42)

    assert isinstance(result, FalsificationTest)
    assert result.test_id == "TEST_1"
    assert result.locally_executable is True
    assert result.current_readout is FalsificationReadout.PARTIAL_LOCAL
    # seed must be forwarded to the sandbox runner
    assert calls and calls[0][1] == 42
    # details summarize what happened
    assert "executed cleanly" in result.details
    assert "PARTIAL_LOCAL" in result.details


def test_test1_broken_script_emits_script_broken(monkeypatch):
    """Crashing subprocess → SCRIPT_BROKEN, never a falsification."""

    stderr = "Traceback (most recent call last):\nModuleNotFoundError: No module named 'foo'"
    monkeypatch.setattr(
        test1_eeg_csd,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_crash(stderr=stderr),
    )

    result = test1_eeg_csd.run_test1()

    assert result.current_readout is FalsificationReadout.SCRIPT_BROKEN
    assert "Traceback" in result.details or "failed to execute" in result.details


# ---------------------------------------------------------------------------
# TEST 2 — Neutrino Koide
# ---------------------------------------------------------------------------


def test_test2_q_nu_far_from_two_thirds_emits_under_pressure(monkeypatch):
    """Q_ν ≈ 0.55 ⇒ UNDER_PRESSURE on the universal-Koide hypothesis."""

    monkeypatch.setattr(
        test2_neutrino_koide,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_success(
            parsed={"Q_NO": 0.55, "Q_IO": 0.56},
        ),
    )

    result = test2_neutrino_koide.run_test2()

    assert result.test_id == "TEST_2"
    assert result.locally_executable is True
    assert result.current_readout is FalsificationReadout.UNDER_PRESSURE
    assert "2/3" in result.details
    assert "UNDER_PRESSURE" in result.details


def test_test2_q_nu_near_two_thirds_emits_partial_local(monkeypatch):
    """Q_ν within 5% of 2/3 ⇒ PARTIAL_LOCAL (not automatic pass)."""

    monkeypatch.setattr(
        test2_neutrino_koide,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_success(
            parsed={"Q_NO": 0.667, "Q_IO": 0.68},
        ),
    )

    result = test2_neutrino_koide.run_test2()

    assert result.current_readout is FalsificationReadout.PARTIAL_LOCAL
    assert "0.667" in result.details or "0.6670" in result.details


def test_test2_parses_q_values_from_stdout(monkeypatch):
    """When parsed_output is empty, fall back to scanning stdout."""

    stdout = (
        "==========================================================\n"
        "NEUTRINO KOIDE SCAN\n"
        "==========================================================\n"
        "Normal ordering — closest Q to 2/3:\n"
        "  m1 = 0.00010 eV,  Q = 0.549123,  delta = 0.1234\n"
        "  |Q - 2/3| = 1.17e-01\n"
        "\n"
        "Inverted ordering — closest Q to 2/3:\n"
        "  m3 = 0.00010 eV,  Q = 0.552345,  delta = 0.2345\n"
        "  |Q - 2/3| = 1.14e-01\n"
    )
    monkeypatch.setattr(
        test2_neutrino_koide,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_success(stdout=stdout),
    )

    result = test2_neutrino_koide.run_test2()

    assert result.current_readout is FalsificationReadout.UNDER_PRESSURE
    assert "0.549" in result.details or "0.552" in result.details


def test_test2_broken_script_emits_script_broken(monkeypatch):
    """Crashing subprocess → SCRIPT_BROKEN."""

    monkeypatch.setattr(
        test2_neutrino_koide,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_crash(),
    )

    result = test2_neutrino_koide.run_test2()

    assert result.current_readout is FalsificationReadout.SCRIPT_BROKEN


# ---------------------------------------------------------------------------
# TEST 3, 4, 5 — External watch entries
# ---------------------------------------------------------------------------


def test_external_tests_always_external_only():
    """TEST 3, 4, 5 emit EXTERNAL_ONLY and never run any script."""

    for test_id, runner in (("TEST_3", run_test3), ("TEST_4", run_test4), ("TEST_5", run_test5)):
        result = runner()
        assert result.test_id == test_id
        assert result.locally_executable is False
        assert result.current_readout is FalsificationReadout.EXTERNAL_ONLY


def test_external_tests_do_not_invoke_sandbox_runner(monkeypatch):
    """Even if run_sandbox_script is replaced to raise, T3/T4/T5 must not touch it."""

    def explode(*args, **kwargs):
        raise AssertionError("external-only tests must not call the sandbox runner")

    # Defensive: patch the module-level symbol on each test module.
    monkeypatch.setattr(test1_eeg_csd, "run_sandbox_script", explode)
    monkeypatch.setattr(test2_neutrino_koide, "run_sandbox_script", explode)

    for runner in (run_test3, run_test4, run_test5):
        result = runner()
        assert result.current_readout is FalsificationReadout.EXTERNAL_ONLY


# ---------------------------------------------------------------------------
# FalsificationPipeline
# ---------------------------------------------------------------------------


def test_pipeline_run_all_returns_five_tests_with_valid_readouts(monkeypatch):
    """run_all produces five records, each with a valid FalsificationReadout."""

    monkeypatch.setattr(
        test1_eeg_csd,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_success(stdout="ok"),
    )
    monkeypatch.setattr(
        test2_neutrino_koide,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_success(parsed={"Q_NO": 0.55}),
    )

    results = FalsificationPipeline().run_all(seed=7)

    assert len(results) == 5
    ids = [r.test_id for r in results]
    assert ids == ["TEST_1", "TEST_2", "TEST_3", "TEST_4", "TEST_5"]
    for r in results:
        assert isinstance(r.current_readout, FalsificationReadout)
    # TEST_1 and TEST_2 are local; TEST_3..5 external.
    assert results[0].locally_executable is True
    assert results[1].locally_executable is True
    for r in results[2:]:
        assert r.locally_executable is False
        assert r.current_readout is FalsificationReadout.EXTERNAL_ONLY


def test_framework_pressure_report_non_empty_and_lists_all_readouts(monkeypatch):
    """The pressure report names every test and every readout value."""

    monkeypatch.setattr(
        test1_eeg_csd,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_success(stdout="ok"),
    )
    monkeypatch.setattr(
        test2_neutrino_koide,
        "run_sandbox_script",
        lambda script_path, seed=None: _fake_success(parsed={"Q_NO": 0.55}),
    )

    pipeline = FalsificationPipeline()
    results = pipeline.run_all(seed=1)
    report = pipeline.framework_pressure_report(results)

    assert isinstance(report, str)
    assert report.strip(), "pressure report must not be empty"
    # every readout name appears at least once (in the tally section)
    for readout in FalsificationReadout:
        assert readout.value in report
    # every test_id appears in per-test highlights
    for test_id in ("TEST_1", "TEST_2", "TEST_3", "TEST_4", "TEST_5"):
        assert test_id in report
    # no binary survival / PASS / FAIL language
    assert "PASS" not in report
    assert "SURVIVED" not in report.upper()
    # explicit note about external-only open status
    assert "EXTERNAL_ONLY" in report
    assert "external" in report.lower()


def test_framework_pressure_report_handles_empty_list():
    """An empty tests list still produces a structured non-empty report."""

    report = FalsificationPipeline().framework_pressure_report([])

    assert "Framework Pressure Map" in report
    assert "Total falsification tests recorded: 0" in report
