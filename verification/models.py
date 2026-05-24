"""Claim data models for the Propagation Framework verification harness.

These dataclasses and enums are the structured records the parser and the
tier runners work with. They mirror the graded-outcome taxonomy from
`CLAIMS.md` and the verification design spec.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md` Req. 1
  (CLAIMS.md parsing into structured claim records)
- `.kiro/specs/propagation-framework-verification/requirements.md` Req. 3
  (graded verification outcomes: REPRODUCED, REGRESSION_OK,
  HYPOTHESIS_OPEN, SCRIPT_BROKEN, EXTERNAL_ONLY, UNDER_PRESSURE)

This module is read-only metadata; it does not modify `CLAIMS.md` or any
other board document.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class ClaimStatus(Enum):
    """Status tier of a claim, mirroring the grading scale in ``CLAIMS.md``.

    The enum name ``PARTIAL_DERIVATION`` uses an underscore, but the board
    displays it as ``PARTIAL DERIVATION`` (two words). The parser is
    responsible for mapping between the two spellings.
    """

    DERIVED = "DERIVED"
    CONDITIONAL = "CONDITIONAL"
    PARTIAL_DERIVATION = "PARTIAL_DERIVATION"
    ARGUED = "ARGUED"
    EMPIRICAL = "EMPIRICAL"
    INTUITION = "INTUITION"
    OPEN = "OPEN"
    NO_GO = "NO_GO"


@dataclass
class Claim:
    """One parsed row from the ``CLAIMS.md`` scoreboard.

    Attributes:
        id: Stable slugified identifier derived from ``name``.
        name: Row label as it appears in ``CLAIMS.md`` (bold markdown stripped).
        status: Tier from the grading scale.
        confidence: Reported confidence (0.0 to 1.0). Values outside the
            tier's stated range are a WARN signal, not a parse failure.
        evidence_summary: The full evidence cell, preserved as a single
            string for downstream runners.
        falsification_criterion: The "What Falsifies It" cell.
        derivation_files: Paths to ``derivations/*.md`` files referenced
            in the evidence cell.
        audited_derivation_refs: Subset of ``derivation_files`` that a
            Support_Manifest has marked as Codex-audit-qualified support.
            Populated by the parser only when a manifest is supplied.
        sandbox_scripts: Paths to ``sandbox/*.py`` scripts referenced in
            the evidence cell.
        named_hypotheses: Named open hypotheses (e.g. ``H_prod``, ``A_NR``)
            extracted from CONDITIONAL / PARTIAL_DERIVATION evidence.
        known_gaps: Short snippets describing stated gaps extracted from
            ARGUED evidence.
        source_row: Line number in the source ``CLAIMS.md`` (1-indexed).
    """

    id: str
    name: str
    status: ClaimStatus
    confidence: float
    evidence_summary: str
    falsification_criterion: str
    derivation_files: list[str] = field(default_factory=list)
    audited_derivation_refs: list[str] = field(default_factory=list)
    sandbox_scripts: list[str] = field(default_factory=list)
    named_hypotheses: list[str] = field(default_factory=list)
    known_gaps: list[str] = field(default_factory=list)
    source_row: int = 0


@dataclass
class DependencyEdge:
    """A single explicit dependency edge between two claim ids.

    Edges live in the read-only ``verification/dependency_overlay.yaml``
    file; they are never inferred from free-prose evidence text.
    """

    upstream: str
    downstream: str
    reason: str
    source: str  # e.g. "manual_overlay" or the path to an audited note


class VerificationOutcome(Enum):
    """Graded local-readout outcome for one claim verification run.

    Replaces binary PASS/FAIL. See Requirement 3 for the semantics of each
    value and the tier-to-outcome mapping rules.
    """

    REPRODUCED = "REPRODUCED"
    REGRESSION_OK = "REGRESSION_OK"
    HYPOTHESIS_OPEN = "HYPOTHESIS_OPEN"
    SCRIPT_BROKEN = "SCRIPT_BROKEN"
    EXTERNAL_ONLY = "EXTERNAL_ONLY"
    UNDER_PRESSURE = "UNDER_PRESSURE"


@dataclass
class VerificationResult:
    """The record a tier runner produces for one claim.

    ``dependency_state`` is a separate lane from the claim outcome and
    takes one of ``"CLEAR"``, ``"OPEN"``, ``"UNDER_PRESSURE"``, or
    ``"NOT_DECLARED"`` (no explicit upstream edges declared). It is never
    silently laundered into a boolean pass for downstream rows.
    """

    claim_id: str
    outcome: VerificationOutcome
    dependency_state: str  # "CLEAR", "OPEN", "UNDER_PRESSURE", "NOT_DECLARED"
    error_margin: float | None = None
    details: str = ""
    scripts_run: list[str] = field(default_factory=list)
    derivation_refs_checked: list[str] = field(default_factory=list)
    gaps_found: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
