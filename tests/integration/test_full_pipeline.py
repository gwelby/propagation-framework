"""Integration test: full pipeline against the real ``CLAIMS.md`` (Task 10.1).

Runs :func:`verification.pipeline.run_verification_pipeline` end-to-end
against the live workspace artifacts (``CLAIMS.md``,
``verification/dependency_overlay.yaml``,
``verification/support_manifest.yaml``, ``AGENTS.md``) with
``quick=True`` so the run stays fast. The test asserts the invariants
that are advertised in the spec:

    * Every parsed claim has a matching result with a valid
      :class:`VerificationOutcome`.
    * No ``Board_Documents`` (``CLAIMS.md``, ``ACTIVE_ISSUES.md``,
      ``WHATS_NEXT.md``) change during the run — byte-exact SHA-256
      comparison before vs. after.
    * No confidence score drifts — the parser is re-run after the
      pipeline and per-claim confidences are compared for equality.
    * The falsification lane always produces exactly five records,
      each with a value in :class:`FalsificationReadout`.

Falsification runners are monkey-patched to avoid invoking the real
``sandbox/`` scripts (which can be slow or depend on optional libs).
The test still validates the lane shape and record count.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md` — Req. all
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 10.1
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from verification.claim_parser import parse_claims_md
from verification.falsification.models import (
    FalsificationReadout,
    FalsificationTest,
)
from verification.models import VerificationOutcome
from verification.pipeline import run_verification_pipeline
from verification.report import VerificationReport


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLAIMS_MD = REPO_ROOT / "CLAIMS.md"
OVERLAY = REPO_ROOT / "verification" / "dependency_overlay.yaml"
MANIFEST = REPO_ROOT / "verification" / "support_manifest.yaml"
AGENTS_MD = REPO_ROOT / "AGENTS.md"

PROTECTED_FILES: tuple[Path, ...] = (
    REPO_ROOT / "CLAIMS.md",
    REPO_ROOT / "ACTIVE_ISSUES.md",
    REPO_ROOT / "WHATS_NEXT.md",
)


def _sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of ``path`` contents (or empty string)."""

    if not path.is_file():
        return ""
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _stub_falsification(monkeypatch) -> None:
    """Replace the falsification runners with deterministic fakes.

    We do NOT want the integration test invoking the real local
    sandbox scripts (``sandbox/eeg_csd_simulator.py`` etc.) because
    those pull optional scientific libraries and write artifacts.
    The fakes still return five records with valid readouts so the
    pipeline's falsification-lane invariants can be asserted.
    """

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


@pytest.mark.skipif(
    not CLAIMS_MD.is_file(),
    reason="CLAIMS.md not present in workspace",
)
def test_full_pipeline_runs_on_real_claims(monkeypatch) -> None:
    """End-to-end run: real CLAIMS.md, stubbed falsification, quick mode.

    Asserts, in order:
        1. Every parsed claim has a matching result with a valid
           :class:`VerificationOutcome`.
        2. The result count matches the parsed claim count.
        3. No board document was modified (byte-identical SHA-256
           before vs. after).
        4. No confidence score drifted (per-claim compare).
        5. Five falsification records, each with a valid readout.
    """

    _stub_falsification(monkeypatch)

    # Snapshot: SHA-256 of every board doc, plus the parsed confidence
    # dict, taken BEFORE the run.
    before_hashes = {p: _sha256(p) for p in PROTECTED_FILES}
    claims_before = parse_claims_md(CLAIMS_MD)
    confidence_before = {cid: c.confidence for cid, c in claims_before.items()}

    report = run_verification_pipeline(
        str(CLAIMS_MD),
        dependency_overlay=str(OVERLAY) if OVERLAY.is_file() else None,
        support_manifest=str(MANIFEST) if MANIFEST.is_file() else None,
        agents_md_path=str(AGENTS_MD) if AGENTS_MD.is_file() else None,
        quick=True,
    )

    # 1. every claim -> a result with a valid outcome
    assert isinstance(report, VerificationReport)
    valid_outcomes = set(VerificationOutcome)
    result_by_id = {r.claim_id: r for r in report.claims}
    missing_results = set(claims_before) - set(result_by_id)
    assert not missing_results, (
        f"pipeline did not produce a result for claims: {sorted(missing_results)}"
    )
    for cid, result in result_by_id.items():
        assert result.outcome in valid_outcomes, (
            f"claim {cid}: outcome {result.outcome!r} is not a VerificationOutcome"
        )

    # 2. claim count matches parsed claims
    assert len(report.claims) == len(claims_before), (
        f"expected {len(claims_before)} results, got {len(report.claims)}"
    )

    # 3. no board document was modified
    after_hashes = {p: _sha256(p) for p in PROTECTED_FILES}
    drifted = [
        p.name
        for p in PROTECTED_FILES
        if before_hashes[p] and before_hashes[p] != after_hashes[p]
    ]
    assert not drifted, f"protected board documents changed: {drifted}"

    # 4. no confidence score changed
    claims_after = parse_claims_md(CLAIMS_MD)
    confidence_after = {cid: c.confidence for cid, c in claims_after.items()}
    assert confidence_before == confidence_after, (
        f"confidence scores drifted: before={confidence_before}, "
        f"after={confidence_after}"
    )

    # 5. falsification: exactly five records, each with a valid readout
    assert len(report.falsification) == 5, (
        f"expected 5 falsification records, got {len(report.falsification)}"
    )
    valid_readouts = set(FalsificationReadout)
    for ft in report.falsification:
        assert ft.current_readout in valid_readouts, (
            f"{ft.test_id}: readout {ft.current_readout!r} not a "
            f"FalsificationReadout"
        )
