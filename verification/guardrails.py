"""Central guardrail enforcer for the Propagation Framework verification pipeline.

This module implements the guardrail layer described in
`.kiro/specs/propagation-framework-verification/design.md` (Component 4).
It checks four kinds of integrity violation and never mutates any file:

1. **Protected-files check** — ``CLAIMS.md``, ``ACTIVE_ISSUES.md``,
   ``WHATS_NEXT.md`` are never allowed to be modified by the pipeline
   (see AGENTS.md TRUTH ORDER).
2. **No-go library check** — re-attempts of documented failed approaches
   are blocked. The library is loaded from AGENTS.md / AGENTS_FULL.md and
   supplemented by filenames in ``derivations/*_no_go*.md``.
3. **Truth-order check** — if sandbox results contradict framework
   framing and the claim isn't explicitly framed as pending/open, emit
   an ``UNDER_PRESSURE`` warning (sandbox > framework).
4. **No-score-change check** — confidence scores in ``CLAIMS.md`` are
   read-only; any drift is a BLOCK.

Related to but distinct from ``verification/guardrail_check.py``, which is
the Family-C-specific deliverable scanner. Both coexist.

References:
- AGENTS_FULL.md Part IV ("THE NO-GO LIBRARY").
- `.kiro/specs/propagation-framework-verification/design.md`
  §"Component 4: Guardrail Enforcer".
- `.kiro/specs/propagation-framework-verification/requirements.md` Req. 6.
- `.kiro/specs/propagation-framework-verification/tasks.md` Tasks 6.1-6.5.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


__all__ = [
    "GuardrailViolation",
    "Guardrails",
    "load_no_go_library",
    "HARDCODED_NO_GO_FALLBACK",
    "DEFAULT_PROTECTED_FILES",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_PROTECTED_FILES: tuple[str, ...] = (
    "CLAIMS.md",
    "ACTIVE_ISSUES.md",
    "WHATS_NEXT.md",
)

# Hardcoded fallback entries — used when AGENTS.md / AGENTS_FULL.md is
# missing or not parseable. Sourced from the real AGENTS_FULL.md
# "THE NO-GO LIBRARY" table and from ACTIVE_ISSUES.md entries flagged as
# no-gos in audited derivations. This is a CACHE, not a second truth source;
# the parseable markdown in the repo always wins when present.
HARDCODED_NO_GO_FALLBACK: dict[str, str] = {
    "harmonic series mass ratios":
        "sandbox_results.md — CV=0.94, essentially random",
    "pure-shift T = S_bar closure":
        "god_eq_path_b family audits",
    "b = 0 chiral closure":
        "path_a_chiral_b_to_zero.md NO-GO",
    "Wigner rotation W=1 from coaxial helix":
        "path3 no-go (casimir_polynomial_path2_poincare.md)",
    "single-scalar PF Lagrangian for Casimir polynomial":
        "route B no-go (casimir_polynomial_route_lagrangian.md)",
    "Route A radius scaling lemma":
        "route A lemma 1 no-go (casimir_polynomial_route_A.md)",
    "projected {k=0, k=1} sector is forced by G1 kinematics alone":
        "path a z6 z3 chirality audit 2026-04-05",
    "canonical operator-native Family C closure":
        "god_eq_path_b_family_c_counterexample_search_2026-04-02.md",
}

# Section headers we'll recognise in AGENTS.md / AGENTS_FULL.md as marking
# a no-go block. Matched case-insensitively, anchored to markdown headers.
_NO_GO_HEADER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^#{1,6}\s*(?:the\s+)?no[-\s_]?go(?:\s+library)?\b", re.IGNORECASE),
    re.compile(r"^#{1,6}\s*failed\s+approaches\b", re.IGNORECASE),
    re.compile(r"^#{1,6}\s*what\s+we\s+got\s+wrong\b", re.IGNORECASE),
)

# Hedging words that let a framework claim coexist with a sandbox-negative
# result without tripping the truth-order check.
_TRUTH_ORDER_HEDGE_WORDS: tuple[str, ...] = (
    "pending",
    "open",
    "argued",
    "conditional",
    "partial",
    "under pressure",
    "under_pressure",
    "hypothesis_open",
    "not yet",
    "awaiting",
    "tbd",
)

# Signals in sandbox results that something went the wrong way.
_SANDBOX_NEGATIVE_SIGNALS: tuple[str, ...] = (
    "fails",
    "failed",
    "contradicts",
    "contradict",
    "violates",
    "violated",
    "exceeds tolerance",
    "outside tolerance",
    "outside the tolerance",
    "no-go",
    "no go",
)

# Float comparison tolerance for confidence-score drift.
_SCORE_EPSILON = 1e-9


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class GuardrailViolation:
    """A single integrity violation flagged by the guardrail enforcer.

    Attributes:
        rule: Short rule identifier. Known values include
            ``"PROTECTED_FILE"``, ``"NO_GO"``, ``"TRUTH_ORDER"``,
            ``"SCORE_CHANGE"``.
        details: Human-readable explanation, including the offending
            input and, when available, the documented reason / source.
        severity: Either ``"BLOCK"`` (stop the run) or ``"WARN"`` (record
            in the report, do not stop). UNDER_PRESSURE truth-order hits
            are surfaced as ``"WARN"`` here because the claim-level
            pipeline re-emits them as ``UNDER_PRESSURE`` outcomes.
    """

    rule: str
    details: str
    severity: str  # "BLOCK" or "WARN"


# ---------------------------------------------------------------------------
# No-go library loader
# ---------------------------------------------------------------------------


def _read_text_safely(path: Path) -> str | None:
    """Read ``path`` as UTF-8, returning ``None`` on any IO failure."""

    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _scan_no_go_sections(text: str, source: str) -> dict[str, str]:
    """Extract no-go entries from the first no-go section in ``text``.

    The parser is deliberately simple: it finds a header that matches one
    of :data:`_NO_GO_HEADER_PATTERNS`, then collects rows until the next
    ``#``-level header. From each collected block it pulls:

    * markdown table rows (``| approach | file | why |``), using the
      ``approach`` cell as the key and ``why`` / ``file`` as the value;
    * bullet lines of the form ``- approach — reason`` or
      ``- approach: reason``.

    Keep parsing simple. False negatives just fall back to the hardcoded
    cache; we don't try to build a complete ontology.
    """

    entries: dict[str, str] = {}
    lines = text.splitlines()

    in_section = False
    section_end = False
    for line in lines:
        stripped = line.strip()

        # Start / end section detection.
        if stripped.startswith("#"):
            matched_start = any(p.match(stripped) for p in _NO_GO_HEADER_PATTERNS)
            if matched_start:
                in_section = True
                section_end = False
                continue
            if in_section:
                # Next top-of-tree header ends the current block. Bail.
                section_end = True
                in_section = False
                continue

        if not in_section or section_end:
            continue

        # Table row: "| approach | file | why |"
        if stripped.startswith("|") and "|" in stripped[1:]:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Skip separator rows ("|---|---|") and header rows.
            if all(set(c) <= set("-: ") for c in cells if c):
                continue
            header_like = {c.lower() for c in cells}
            if {"approach"} & header_like or {"why it failed"} & header_like:
                continue
            if len(cells) >= 2:
                approach = cells[0].strip("` ")
                # Prefer "why" (3rd cell), fall back to 2nd cell.
                reason = cells[2] if len(cells) >= 3 and cells[2] else cells[1]
                reason = reason.strip("` ")
                if approach and reason:
                    entries[approach] = f"{reason} (source: {source})"
            continue

        # Bullet: "- approach — reason" or "- approach: reason"
        if stripped.startswith(("-", "*")):
            body = stripped[1:].strip()
            for sep in (" — ", " -- ", " - ", ": ", " -> "):
                if sep in body:
                    approach, reason = body.split(sep, 1)
                    approach = approach.strip("` ")
                    reason = reason.strip("` ")
                    if approach and reason:
                        entries[approach] = f"{reason} (source: {source})"
                    break

    return entries


def _scan_no_go_filenames(derivations_dir: Path) -> dict[str, str]:
    """Extract no-go entries from filenames in ``derivations/``.

    Any markdown file whose name contains ``_no_go`` or ``no_go_`` is
    treated as a documented failed approach. The filename stem
    (minus the marker) becomes the approach key; the file path is the
    source. Keeps parsing simple — we cache the title text rather than
    parsing abstracts.
    """

    entries: dict[str, str] = {}
    if not derivations_dir.is_dir():
        return entries

    for path in sorted(derivations_dir.glob("*.md")):
        name = path.name.lower()
        if "_no_go" not in name and "no_go_" not in name:
            continue
        stem = path.stem
        # Humanise: drop the marker, replace underscores, trim dates.
        approach = stem.replace("_no_go", "").replace("no_go_", "")
        approach = re.sub(r"_?\d{4}-\d{2}-\d{2}$", "", approach)
        approach = approach.replace("_", " ").strip()
        if not approach:
            continue
        entries[approach] = f"documented in {path.as_posix()}"

    return entries


def load_no_go_library(
    agents_md_path: str | Path | None = None,
    *,
    derivations_dir: str | Path | None = None,
) -> dict[str, str]:
    """Load documented no-go entries, with a hardcoded fallback.

    Parsing strategy (simple, best-effort, deliberately conservative):

    1. Start from :data:`HARDCODED_NO_GO_FALLBACK`.
    2. If ``agents_md_path`` is given and readable, scan it for sections
       whose header matches ``No-Go``, ``NO_GO``, ``Failed Approaches``,
       or ``What We Got Wrong`` and pull table rows / bullets out of
       them. Also, if a sibling ``AGENTS_FULL.md`` exists, scan it too.
    3. Scan ``derivations/`` (or the provided ``derivations_dir``) for
       markdown files whose names contain ``_no_go`` or ``no_go_`` and
       add them as entries with the path as source.

    When AGENTS.md is missing or not parseable, step 1's hardcoded cache
    alone still returns the expected entries. That is a documented,
    intentional fallback — not a silent failure mode.

    Returns:
        A dict mapping no-go approach description → reason / source.
    """

    library: dict[str, str] = dict(HARDCODED_NO_GO_FALLBACK)

    # Step 2 — scan AGENTS.md and, if present, AGENTS_FULL.md.
    if agents_md_path is not None:
        agents_path = Path(agents_md_path)
        for candidate in (agents_path, agents_path.with_name("AGENTS_FULL.md")):
            if candidate.is_file():
                text = _read_text_safely(candidate)
                if text:
                    library.update(_scan_no_go_sections(text, candidate.name))

    # Step 3 — scan derivations/ filenames.
    if derivations_dir is not None:
        library.update(_scan_no_go_filenames(Path(derivations_dir)))
    else:
        # Best-effort: look for a ``derivations/`` directory next to
        # AGENTS.md (usually the repo root).
        if agents_md_path is not None:
            default_derivations = Path(agents_md_path).resolve().parent / "derivations"
            library.update(_scan_no_go_filenames(default_derivations))

    return library


# ---------------------------------------------------------------------------
# Guardrails class
# ---------------------------------------------------------------------------


class Guardrails:
    """Central enforcer for the verification pipeline.

    Loads the no-go library and protected-file list, checks for each
    kind of violation. Never mutates any file.

    Example:
        >>> g = Guardrails()
        >>> g.check_protected_files(["CLAIMS.md"])
        [GuardrailViolation(rule='PROTECTED_FILE', ...)]
    """

    def __init__(
        self,
        agents_md_path: str | Path | None = None,
        *,
        protected_files: tuple[str, ...] = DEFAULT_PROTECTED_FILES,
        derivations_dir: str | Path | None = None,
    ) -> None:
        self.no_go_library: dict[str, str] = load_no_go_library(
            agents_md_path, derivations_dir=derivations_dir
        )
        self.protected_files: set[str] = set(protected_files)

    # ------------------------------------------------------------------
    # 6.2 — Protected files
    # ------------------------------------------------------------------

    def check_protected_files(
        self, modified_files: list[str]
    ) -> list[GuardrailViolation]:
        """Emit BLOCK if any modified file is a protected Board_Document.

        Matches by basename so that both ``CLAIMS.md`` and
        ``/abs/path/to/CLAIMS.md`` trip the rule.
        """

        violations: list[GuardrailViolation] = []
        for raw in modified_files:
            # Use PurePath for cross-platform basename extraction without
            # touching the filesystem.
            basename = Path(raw).name
            if basename in self.protected_files:
                violations.append(
                    GuardrailViolation(
                        rule="PROTECTED_FILE",
                        details=(
                            f"Protected board document '{basename}' was modified "
                            f"(path: {raw}). Board documents are read-only per "
                            f"AGENTS.md TRUTH ORDER."
                        ),
                        severity="BLOCK",
                    )
                )
        return violations

    # ------------------------------------------------------------------
    # 6.3 — No-go enforcement
    # ------------------------------------------------------------------

    def check_no_go(self, approach: str) -> list[GuardrailViolation]:
        """Emit BLOCK if ``approach`` matches a documented no-go.

        Matching is a case-insensitive substring test against the
        no-go library keys. We also try a mildly normalised form where
        ``T = S̄`` / ``T = S_bar`` are treated as equivalent.

        We don't attempt semantic matching — "vaguely resembles a no-go"
        is the reviewer's job, not the guardrail's.
        """

        if not approach:
            return []

        violations: list[GuardrailViolation] = []
        normalised_input = _normalise_for_no_go(approach)

        for key, reason in self.no_go_library.items():
            normalised_key = _normalise_for_no_go(key)
            if not normalised_key:
                continue
            if normalised_key in normalised_input:
                violations.append(
                    GuardrailViolation(
                        rule="NO_GO",
                        details=(
                            f"Approach references documented no-go: '{key}'. "
                            f"Documented failure: {reason}. Do not re-attempt "
                            f"without reading the source."
                        ),
                        severity="BLOCK",
                    )
                )
        return violations

    # ------------------------------------------------------------------
    # 6.4 — Truth order
    # ------------------------------------------------------------------

    def validate_truth_order(
        self,
        claim_framing: str,
        sandbox_result_summary: str,
    ) -> list[GuardrailViolation]:
        """Emit an UNDER_PRESSURE WARN if sandbox contradicts framing.

        Simple keyword-overlap heuristic, deliberately conservative:
        if the sandbox summary contains a negative signal word
        (``fails``, ``contradicts``, ``violates``, ``exceeds tolerance``,
        ...) AND the claim framing does NOT hedge (``pending``,
        ``open``, ``ARGUED``, ``conditional``, ...), emit a warning.

        False positives are acceptable as reviewer flags; false
        negatives (silently letting framework outrun sandbox) are the
        actual failure mode we're protecting against.
        """

        sandbox_lower = (sandbox_result_summary or "").lower()
        framing_lower = (claim_framing or "").lower()

        has_negative = any(sig in sandbox_lower for sig in _SANDBOX_NEGATIVE_SIGNALS)
        has_hedge = any(hedge in framing_lower for hedge in _TRUTH_ORDER_HEDGE_WORDS)

        if has_negative and not has_hedge:
            return [
                GuardrailViolation(
                    rule="TRUTH_ORDER",
                    details=(
                        "Sandbox result contradicts framework framing without "
                        "hedging. Per AGENTS.md TRUTH ORDER (sandbox_results.md > "
                        "CLAIMS.md > the_propagation_framework.md), the framing "
                        "should be downgraded or marked UNDER_PRESSURE. "
                        f"Framing: {claim_framing!r}. Sandbox: "
                        f"{sandbox_result_summary!r}."
                    ),
                    severity="WARN",
                )
            ]
        return []

    # ------------------------------------------------------------------
    # 6.5 — No score changes
    # ------------------------------------------------------------------

    def validate_no_score_change(
        self,
        before_scores: dict[str, float],
        after_scores: dict[str, float],
    ) -> list[GuardrailViolation]:
        """Emit BLOCK for every confidence score that drifted.

        Also emits BLOCK for any claim that appears in ``after_scores``
        but not ``before_scores`` (new claim injected without audit) or
        that disappeared from ``before_scores`` (claim silently dropped).
        """

        violations: list[GuardrailViolation] = []

        before_keys = set(before_scores)
        after_keys = set(after_scores)

        for claim_id in before_keys & after_keys:
            before = before_scores[claim_id]
            after = after_scores[claim_id]
            if abs(before - after) > _SCORE_EPSILON:
                violations.append(
                    GuardrailViolation(
                        rule="SCORE_CHANGE",
                        details=(
                            f"Confidence score for '{claim_id}' changed "
                            f"{before} -> {after}. The verification pipeline "
                            f"MUST NOT modify CLAIMS.md scores. Only a Codex "
                            f"audit can move a score."
                        ),
                        severity="BLOCK",
                    )
                )

        for claim_id in after_keys - before_keys:
            violations.append(
                GuardrailViolation(
                    rule="SCORE_CHANGE",
                    details=(
                        f"New confidence score injected for '{claim_id}' "
                        f"(after={after_scores[claim_id]}) with no pre-image "
                        f"in CLAIMS.md. Only a Codex audit can introduce a claim."
                    ),
                    severity="BLOCK",
                )
            )

        for claim_id in before_keys - after_keys:
            violations.append(
                GuardrailViolation(
                    rule="SCORE_CHANGE",
                    details=(
                        f"Confidence score for '{claim_id}' was dropped "
                        f"(before={before_scores[claim_id]}). The pipeline "
                        f"MUST NOT remove claims from CLAIMS.md."
                    ),
                    severity="BLOCK",
                )
            )

        return violations


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalise_for_no_go(text: str) -> str:
    """Lightweight normalisation for no-go substring matching.

    Lowercase, collapse whitespace, and fold a few unicode / ASCII
    variants (``S̄`` ↔ ``S_bar``) so that approach descriptions
    written in either form still match.
    """

    if not text:
        return ""
    s = text.lower()
    s = s.replace("s̄", "s_bar").replace("s\u0304", "s_bar")
    s = re.sub(r"\s+", " ", s).strip()
    return s
