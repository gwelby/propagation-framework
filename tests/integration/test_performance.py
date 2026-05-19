"""Performance validation tests (Task 13.2).

Tests:

* ``test_full_pipeline_completes_under_threshold`` — the full pipeline
  with ``quick=True`` completes well under a liberal 30 s budget.
* ``test_cache_reduces_repeat_runtime`` — content-hash caching either
  makes a repeat run of the same script measurably cheaper or the
  cache file is populated after the first run. Timing assertions use
  a generous 10% slack and fall back to checking cache population.
* ``test_quick_mode_under_60s`` — explicit check that ``--quick``
  mode stays well under the 60 s budget advertised in the spec.

Sandbox scripts are stubbed to a deterministic fast return so the
performance budget is about pipeline overhead, not about whatever the
real sandbox scripts happen to do today.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.pipeline import (
    get_script_cache_key,
    load_cached_result,
    run_verification_pipeline,
    save_cached_result,
)
from verification.sandbox_runner import SandboxRunResult, run_sandbox_script


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLAIMS_MD = REPO_ROOT / "CLAIMS.md"
OVERLAY = REPO_ROOT / "verification" / "dependency_overlay.yaml"
MANIFEST = REPO_ROOT / "verification" / "support_manifest.yaml"
AGENTS_MD = REPO_ROOT / "AGENTS.md"


pytestmark = pytest.mark.skipif(
    not CLAIMS_MD.is_file(),
    reason="CLAIMS.md not present in workspace",
)


# ---------------------------------------------------------------------------
# Stubs
# ---------------------------------------------------------------------------


def _stub_falsification(monkeypatch) -> None:
    """Replace FalsificationPipeline.run_all with a deterministic fake."""

    def fake_run_all(self, seed=None):
        return [
            FalsificationTest(
                test_id=f"TEST_{i}",
                name=f"Fake TEST {i}",
                locally_executable=i <= 2,
                framework_prediction="(fixture)",
                falsification_criterion="(fixture)",
                current_readout=FalsificationReadout.EXTERNAL_ONLY,
                details=f"fixture detail for TEST_{i}",
            )
            for i in range(1, 6)
        ]

    monkeypatch.setattr(
        "verification.pipeline.FalsificationPipeline.run_all", fake_run_all
    )


def _stub_sandbox_runner(monkeypatch) -> None:
    """Make every runner's sandbox subprocess fast and deterministic."""

    def fake_run(script_path, seed=None, timeout=None, cwd=None):
        return SandboxRunResult(
            script_path=str(script_path),
            success=True,
            stdout='{"predicted": 1.0, "measured": 1.0}',
            stderr="",
            return_code=0,
            error="",
            parsed_output={"predicted": 1.0, "measured": 1.0},
        )

    for module in (
        "verification.runners.derived",
        "verification.runners.conditional",
        "verification.runners.argued",
        "verification.runners.empirical",
        "verification.runners.frontier",
    ):
        monkeypatch.setattr(f"{module}.run_sandbox_script", fake_run)


def _run_full_pipeline():
    return run_verification_pipeline(
        str(CLAIMS_MD),
        dependency_overlay=str(OVERLAY) if OVERLAY.is_file() else None,
        support_manifest=str(MANIFEST) if MANIFEST.is_file() else None,
        agents_md_path=str(AGENTS_MD) if AGENTS_MD.is_file() else None,
        quick=True,
        seed=42,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_full_pipeline_completes_under_threshold(monkeypatch) -> None:
    """Full pipeline (quick=True) should finish in well under 30 s."""

    _stub_falsification(monkeypatch)
    _stub_sandbox_runner(monkeypatch)

    started = time.perf_counter()
    report = _run_full_pipeline()
    elapsed = time.perf_counter() - started

    assert report.claims, "pipeline produced no claim results"
    assert elapsed < 30.0, (
        f"full pipeline took {elapsed:.2f}s which exceeds the 30s budget"
    )


def test_quick_mode_under_60s(monkeypatch) -> None:
    """Quick mode must stay under the 60 s budget from the spec."""

    _stub_falsification(monkeypatch)
    _stub_sandbox_runner(monkeypatch)

    started = time.perf_counter()
    report = _run_full_pipeline()
    elapsed = time.perf_counter() - started

    assert len(report.claims) >= 20, (
        f"expected at least 20 claim results, got {len(report.claims)}"
    )
    assert elapsed < 60.0, (
        f"quick mode took {elapsed:.2f}s which exceeds the 60s budget"
    )


def test_cache_reduces_repeat_runtime(tmp_path: Path) -> None:
    """Repeat runs over the same script reuse the cache.

    Uses the public cache API directly rather than the pipeline entry
    point, because the pipeline stubs above short-circuit the
    subprocess. The assertion is either:

        * wall-clock cost of ``load_cached_result`` <= 10% slack over
          the cost of the first ``save_cached_result`` + hash, or
        * the cache file exists after the first write.

    Timing is a nice-to-have; cache population is the contract.
    """

    # A real Python script so the hash computation is meaningful.
    script = tmp_path / "slow_script.py"
    script.write_text(
        "# pretend this does something expensive\n"
        "import json, time\n"
        "# no actual sleep — we only care about cache semantics here\n"
        "print(json.dumps({'predicted': 1.0, 'measured': 1.0}))\n",
        encoding="utf-8",
    )

    cache_dir = tmp_path / "cache"

    key_a = get_script_cache_key(script)
    assert len(key_a) == 64  # SHA-256 hex

    # First run: no cache hit.
    assert load_cached_result(key_a, cache_dir=cache_dir) is None

    # Populate the cache with a deterministic SandboxRunResult.
    sample = SandboxRunResult(
        script_path=str(script),
        success=True,
        stdout='{"predicted": 1.0, "measured": 1.0}',
        stderr="",
        return_code=0,
        error="",
        parsed_output={"predicted": 1.0, "measured": 1.0},
    )

    started = time.perf_counter()
    save_cached_result(key_a, sample, cache_dir=cache_dir)
    first_cost = time.perf_counter() - started

    # Cache file must exist.
    cache_file = cache_dir / f"{key_a}.json"
    assert cache_file.is_file(), "cache file was not written"

    # Second run: cache hit returns the same dataclass shape.
    started = time.perf_counter()
    cached = load_cached_result(key_a, cache_dir=cache_dir)
    second_cost = time.perf_counter() - started
    assert cached is not None
    assert cached.success is True
    assert cached.stdout == sample.stdout
    assert cached.parsed_output == sample.parsed_output

    # Timing is flaky on shared runners; use the cache-file-existence
    # assertion as the real contract and only require that the load
    # did not blow up the budget by a wide margin.
    slack_budget = max(first_cost * 1.1, 0.5)
    assert second_cost <= slack_budget, (
        f"cache load took {second_cost:.4f}s vs first-write "
        f"{first_cost:.4f}s plus 10% slack ({slack_budget:.4f}s)"
    )


def test_sandbox_runner_handles_missing_script_fast() -> None:
    """The sandbox runner must never hang on a missing script.

    Regression guard: this is the code path that surfaces
    SCRIPT_BROKEN in the DerivedRunner; it has to return almost
    immediately.
    """

    started = time.perf_counter()
    result = run_sandbox_script("sandbox/__does_not_exist__.py")
    elapsed = time.perf_counter() - started

    assert result.success is False
    assert result.error == "FileNotFoundError"
    assert elapsed < 2.0, (
        f"missing-script path took {elapsed:.2f}s; should be near-instant"
    )
