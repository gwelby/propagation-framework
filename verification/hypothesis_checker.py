"""Hypothesis closure checker for the verification harness.

A CONDITIONAL or PARTIAL_DERIVATION claim lists one or more *named
hypotheses* — short tokens like ``H_prod``, ``H_foo``, ``H_nr`` that
name the missing bridge between its local lemma and its full claim.
This module decides, for a given hypothesis token and a set of
candidate derivation files, whether the hypothesis has been *explicitly
closed in a Codex-audited derivation*. Anything weaker (a draft note,
an unaudited sketch, the hypothesis appearing only as "still open" or
"pending") is treated as not-closed.

The rule the harness enforces is intentionally conservative:

    A hypothesis is CLOSED iff some derivation file whose path looks
    like a Codex audit (contains ``_audit`` or begins with ``audit_``
    in its filename) contains a closure pattern for the hypothesis
    (``CLOSED``, ``DERIVED``, ``audit ... passed``, etc.).

Non-audited drafts are allowed to *mention* the hypothesis without
counting as a closure. This mirrors the spec's "only Codex-audited
closures count" language (Req. 4.2) and the AGENTS.md truth order
rule that sandbox/audit files dominate draft notes.

The text-matching heuristics below are deliberately simple and
documented; future work may replace them with a structured audit
manifest once one exists.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 3.5, Req. 4.2 (HYPOTHESIS_OPEN while any named hypothesis stays
  open; only audited closures count).
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 4.8.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path


logger = logging.getLogger(__name__)


# Patterns that count as an explicit closure signal when they appear in
# an audited file. ``{hyp}`` is substituted with the escaped hypothesis
# token per call; the compiled patterns live inside
# :func:`_closure_patterns_for`.
_CLOSURE_PATTERN_TEMPLATES: tuple[str, ...] = (
    # "H_prod: CLOSED" / "H_prod status: DERIVED"
    r"{hyp}\s*(?:status)?\s*[:\-]\s*(?:closed|derived|proven|proved)\b",
    # "H_prod is now CLOSED" / "H_prod has been derived"
    r"{hyp}\s+(?:is|has\s+been)\s+(?:now\s+)?(?:closed|derived|proven|proved)\b",
    # "Codex audit: H_prod passed" / "audit H_prod: passed"
    r"(?:codex\s+)?audit[:\-\s]+{hyp}[:\-\s]+(?:passed|closed|derived)\b",
    r"{hyp}\s+audit(?:ed)?[:\-\s]+(?:passed|closed|derived)\b",
    # Explicit "CLOSURE" / "DERIVED" headline near the hypothesis
    r"{hyp}\s*(?:--|—|->)\s*(?:closed|derived|proven|proved)\b",
)


# Patterns that, when they appear in the same file, *cancel* a closure —
# even in an audited file the operator may have explicitly marked the
# hypothesis as still open.
_STILL_OPEN_PATTERNS: tuple[str, ...] = (
    r"{hyp}\s*(?:status)?\s*[:\-]\s*(?:open|partial|pending|not\s+closed)\b",
    r"{hyp}\s+(?:remains|is\s+still|stays)\s+(?:open|partial|pending)\b",
    r"{hyp}\s+not\s+yet\s+(?:closed|derived|proven)\b",
)


def check_hypothesis_closure(
    hypothesis: str,
    derivation_files: list[str],
    workspace_root: Path | None = None,
) -> bool:
    """Return True iff ``hypothesis`` is explicitly closed in an audited file.

    Args:
        hypothesis: The hypothesis token (e.g. ``"H_prod"``). Leading
            and trailing whitespace is stripped. Matching is
            case-insensitive and uses the exact token with a word
            boundary on the right-hand side so ``H_prod`` does not
            match ``H_product``.
        derivation_files: Candidate derivation file paths. Paths may be
            absolute or relative; relative paths are resolved against
            ``workspace_root`` when given.
        workspace_root: Optional base directory for resolving relative
            paths. Defaults to the repository root (three parents above
            this file).

    Returns:
        True iff at least one audited file contains a closure pattern
        for ``hypothesis`` and no "still open" pattern overrides it in
        the same file. False for any of:

            * hypothesis is empty after stripping,
            * no candidate file is audited,
            * no audited file mentions the hypothesis,
            * the only audited mentions are as OPEN / PARTIAL / PENDING,
            * an audited file lists a closure but the same file also
              lists a still-open note for the same hypothesis (the
              still-open note wins — conservative by design).
    """

    hyp = (hypothesis or "").strip()
    if not hyp:
        return False

    resolved_paths = _resolve_paths(derivation_files, workspace_root)
    audited_paths = [p for p in resolved_paths if _is_audited_path(p)]
    if not audited_paths:
        logger.debug(
            "check_hypothesis_closure: no audited files among %d candidates "
            "for %r",
            len(resolved_paths),
            hyp,
        )
        return False

    closure_patterns = _closure_patterns_for(hyp)
    still_open_patterns = _still_open_patterns_for(hyp)

    any_closure = False
    for path in audited_paths:
        text = _safe_read(path)
        if not text:
            continue
        has_closure = any(pat.search(text) for pat in closure_patterns)
        has_still_open = any(pat.search(text) for pat in still_open_patterns)
        if has_closure and not has_still_open:
            logger.debug(
                "check_hypothesis_closure: %r closed by %s",
                hyp,
                path,
            )
            return True
        if has_closure and has_still_open:
            logger.info(
                "check_hypothesis_closure: %r flagged both closed and still "
                "open in %s; treating as still open",
                hyp,
                path,
            )
            any_closure = True  # for logging only

    if any_closure:
        return False
    return False


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _closure_patterns_for(hypothesis: str) -> list[re.Pattern[str]]:
    escaped = re.escape(hypothesis)
    return [
        re.compile(tmpl.format(hyp=escaped), re.IGNORECASE)
        for tmpl in _CLOSURE_PATTERN_TEMPLATES
    ]


def _still_open_patterns_for(hypothesis: str) -> list[re.Pattern[str]]:
    escaped = re.escape(hypothesis)
    return [
        re.compile(tmpl.format(hyp=escaped), re.IGNORECASE)
        for tmpl in _STILL_OPEN_PATTERNS
    ]


def _is_audited_path(path: Path) -> bool:
    """Heuristic: does ``path``'s filename look like a Codex audit?

    Returns True when the filename contains ``_audit`` (``_audit.md``,
    ``_audit_2026-04-01.md``, ``step_A_audit.md``) or begins with
    ``audit_`` / ``audit-``. Case-insensitive.
    """

    name = path.name.lower()
    if name.startswith(("audit_", "audit-")):
        return True
    stem = path.stem.lower()
    if "_audit" in stem or stem.endswith("audit"):
        return True
    return False


def _resolve_paths(
    derivation_files: list[str],
    workspace_root: Path | None,
) -> list[Path]:
    base = workspace_root or Path(__file__).resolve().parent.parent
    out: list[Path] = []
    for raw in derivation_files or []:
        if not raw:
            continue
        p = Path(raw)
        if not p.is_absolute():
            p = base / p
        out.append(p)
    return out


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, PermissionError, OSError) as exc:
        logger.debug("_safe_read: could not read %s: %s", path, exc)
        return ""
