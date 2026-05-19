"""Integration tests: pipeline determinism (Task 10.3).

Asserts that re-running the pipeline on the same inputs with the same
``seed`` produces identical outputs:

    * ``test_same_inputs_produce_same_outcomes`` — two full runs
      against the real ``CLAIMS.md`` with ``seed=42`` must produce:

        - the same :class:`VerificationOutcome` for every claim,
        - the same :class:`FalsificationReadout` for every test,
        - the same dashboard markdown after stripping ISO timestamps.

    * ``test_cache_key_stable`` — :func:`get_script_cache_key` returns
      the same SHA-256 hex digest on repeated reads of an unchanged
      file.

Sandbox-script subprocesses are monkey-patched to a deterministic
stub so the test does not depend on the real ``sandbox/`` scripts.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 10.1, Req. 10.2.
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 10.3.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.pipeline import (
    get_script_cache_key,
    run_verification_pipeline,
)
from verification.report import generate_dashboard
from verification.claim_graph import ClaimGraph
from verification.sandbox_runner import SandboxRunResult


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLAIMS_MD = REPO_ROOT / "CLAIMS.md"
OVERLAY = REPO_ROOT / "verification" / "dependency_overlay.yaml"
MANIFEST = REPO_ROOT / "verification" / "support_manifest.yaml"
AGENTS_MD = REPO_ROOT / "AGENTS.md"


# ISO 8601 UTC timestamp pattern, e.g. "2026-05-07T12:34:56.789012+00:00".
# We also need to match the shorter flavor without fractional seconds.
_ISO_TIMESTAMP_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:\+\d{2}:\d{2}|Z)?"
)


def _strip_timestamps(text: str) -> str:
    """Replace every ISO-8601 timestamp in ``text`` with ``<TS>``.

    Dashboard and report generators embed ``datetime.now(timezone.utc)``
    in their headers and per-row fields; those differ between runs and
    must be stripped before we compare byte-for-byte.
    """

    return _ISO_TIMESTAMP_RE.sub("<TS>", text)


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
                current_readout=(
                    FalsificationReadout.PARTIAL_LOCAL
                    if i == 1
                    else FalsificationReadout.UNDER_PRESSURE
                    if i == 2
                    else FalsificationReadout.EXTERNAL_ONLY
                ),
                details=f"fixture detail for TEST_{i}",
            )
            for i in range(1, 6)
        ]

    monkeypatch.setattr(
        "verification.pipeline.FalsificationPipeline.run_all", fake_run_all
    )


def _stub_sandbox_runner(monkeypatch) -> None:
    """Make every sandbox subprocess return a deterministic success.

    Touches the four runners that import :func:`run_sandbox_script`
    directly. Each gets the same stub so any runner that fires during a
    pipeline pass produces the same output.
    """

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


@pytest.mark.skipif(
    not CLAIMS_MD.is_file(),
    reason="CLAIMS.md not present in workspace",
)
def test_same_inputs_produce_same_outcomes(monkeypatch) -> None:
    """Two runs with the same seed must produce identical outputs."""

    _stub_falsification(monkeypatch)
    _stub_sandbox_runner(monkeypatch)

    def single_run():
        report = run_verification_pipeline(
            str(CLAIMS_MD),
            dependency_overlay=str(OVERLAY) if OVERLAY.is_file() else None,
            support_manifest=str(MANIFEST) if MANIFEST.is_file() else None,
            agents_md_path=str(AGENTS_MD) if AGENTS_MD.is_file() else None,
            quick=True,
            seed=42,
        )
        graph = ClaimGraph.from_markdown(
            str(CLAIMS_MD),
            dependency_overlay_path=str(OVERLAY) if OVERLAY.is_file() else None,
            support_manifest_path=str(MANIFEST) if MANIFEST.is_file() else None,
        )
        dashboard = generate_dashboard(
            graph, report.claims, report.falsification
        )
        return report, dashboard

    report_a, dash_a = single_run()
    report_b, dash_b = single_run()

    # Outcomes per claim id.
    outcomes_a = {r.claim_id: r.outcome for r in report_a.claims}
    outcomes_b = {r.claim_id: r.outcome for r in report_b.claims}
    assert outcomes_a == outcomes_b, (
        "VerificationOutcomes differ across deterministic runs"
    )

    # Falsification readouts per test id.
    readouts_a = {t.test_id: t.current_readout for t in report_a.falsification}
    readouts_b = {t.test_id: t.current_readout for t in report_b.falsification}
    assert readouts_a == readouts_b, (
        "FalsificationReadouts differ across deterministic runs"
    )

    # Dashboard text is identical once timestamps are redacted.
    assert _strip_timestamps(dash_a) == _strip_timestamps(dash_b), (
        "dashboard content (excluding timestamps) drifted between runs"
    )


def test_cache_key_stable(tmp_path: Path) -> None:
    """Hashing an unchanged script twice returns the same cache key."""

    script = tmp_path / "fixed_script.py"
    script.write_text(
        "import json\n"
        "print(json.dumps({'predicted': 1.0, 'measured': 1.0}))\n",
        encoding="utf-8",
    )

    key_a = get_script_cache_key(script)
    key_b = get_script_cache_key(script)

    assert key_a == key_b
    assert len(key_a) == 64  # SHA-256 hex
