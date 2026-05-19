"""
Automated guardrail scanner for the God Equation Path B / Family C
deliverables.

Role
----
This module implements task 12.1 of
.kiro/specs/god-eq-path-b-family-c/tasks.md and Requirement 9 of
.kiro/specs/god-eq-path-b-family-c/requirements.md.

Two bounded derivation notes are the live deliverables of the work
package:

  * Family_C_Draft ->
    derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md
  * Vacuum_Note   ->
    derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md

Neither deliverable is allowed to

  1. overclaim H_prod (for example, "H_prod is proved"),
  2. upgrade a confidence score (for example, "0.88 -> 0.9",
     "upgrade to DERIVED", "now DERIVED"),
  3. silently import a killed shortcut as if it were an active
     assumption (for example, an unqualified "T = S_bar", a revived
     "b = 0" closure claim, a recycled Path-A "projected {k=0, k=1}
     sector is forced", or a QFT import presented as a derivation
     step),
  4. edit CLAIMS.md, ACTIVE_ISSUES.md, or WHATS_NEXT.md (the
     Board_Documents),
  5. (Vacuum_Note) claim that PF "fully forbids every escape
     ensemble" or equivalent, or
  6. (Vacuum_Note) broaden from the free linearized vacuum to the full
     nonlinear PF without an explicit bridge derivation in the note.

The scanner is deliberately conservative. Mere mentions of a forbidden
object inside a negation / scope-limit / "dead shortcut" context are
NOT flagged as violations; only unqualified usages are. This lets the
deliverables keep doing the right thing -- naming every dead shortcut
by name and explaining why it is dead -- without tripping the scanner.

Scanner design
--------------

Three categories of pattern are scanned, plus two structural checks:

  * FORBIDDEN_STRINGS (dict[category, tuple[regex]]):
      H_prod_overclaim   -- "H_prod is proved", etc. (both files)
      escape_overclaim   -- "fully forbids every escape ensemble",
                            "rules out all escape ensembles", etc.
                            (Vacuum_Note only)
      nonlinear_pf_overclaim -- "full nonlinear PF", etc. Tagged as
                            WARNING rather than FAIL if a bridge
                            derivation or explicit "free linearized"
                            scope qualifier appears in the same
                            paragraph (Vacuum_Note only).

  * SCORE_UPGRADE_PATTERNS (tuple[regex]):
      confidence score transitions (0.88 -> 0.9, etc.), promotion
      verbs ("upgrade to DERIVED"), and "now DERIVED" status changes.
      WARNING if the same sentence also contains a scope-limit
      qualifier ("does not upgrade", "no score change"), FAIL
      otherwise.

  * FORBIDDEN_SHORTCUTS (tuple[tuple[category, regex]]):
      dead_pure_shift   -- unqualified T = S_bar / T = S-bar.
      revived_b_eq_0    -- b = 0 asserted positively (not a revived
                            no-go reference).
      path_a_projection -- the exact Path-A "projected {k=0, k=1}
                            sector is forced" phrase.
      qft_imported_step -- "from standard QFT, ..." presented as a
                            derivation step (as opposed to a citation
                            or a named assumption).
      A match upgrades to FAIL only if no qualifier from
      QUALIFIER_WORDS appears in the same sentence; otherwise it is
      recorded as WARNING (context suggests the forbidden object is
      being discussed as killed, not imported).

  * Protected-path check:
      the two deliverable paths MUST NOT be CLAIMS.md, ACTIVE_ISSUES.md,
      or WHATS_NEXT.md (Requirement 9.1, 9.2). The helper
      `assert_no_protected_file_writes(paths)` lets a caller feed a
      list of paths-to-be-written through the same check.

Severity semantics
------------------
Every flagged item carries a severity:

  * FAIL     -- hard violation, causes the scan to fail.
  * WARNING  -- context looks like a valid mention (negation, scope
                limit, explicit "dead" tag), but a human reviewer
                should confirm.

The `passed` flag on a FileScanResult is True iff it has NO FAIL
matches AND no protected-path violation. Warnings do not flip passed.

Public API
----------
- `Severity`                    string alias constants "FAIL" / "WARNING"
- `Match`                       dataclass for a single flagged line
- `FileScanResult`              dataclass for a single-file scan report
- `GuardrailReport`             dataclass aggregating both deliverables
- `scan_file(path, is_vacuum_note=False)`     -> FileScanResult
- `run_guardrail_check(family_c_path=..., vacuum_note_path=...)`
                                              -> GuardrailReport
- `assert_no_protected_file_writes(paths)`    -> None (raises on violation)
- `FAMILY_C_PATH`, `VACUUM_NOTE_PATH`         module-level default paths
- `PROTECTED_PATHS`                           frozenset of forbidden write targets

Guardrails on this file
-----------------------
This module lives under `verification/` only. It does not edit
CLAIMS.md, ACTIVE_ISSUES.md, WHATS_NEXT.md, requirements.md, design.md,
or any derivation note. Its sole function is to SCAN the two
deliverables and report findings -- it never rewrites them. If a scan
surfaces a real violation, the fix is the caller's decision, not this
module's.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from typing import Iterable


# ----------------------------------------------------------------------
# Module-level constants
# ----------------------------------------------------------------------

FAMILY_C_PATH: str = (
    "derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md"
)
VACUUM_NOTE_PATH: str = (
    "derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md"
)

# Files that no deliverable may write to. Match on basename so that
# "CLAIMS.md" and "./CLAIMS.md" and "/repo/CLAIMS.md" all trigger.
PROTECTED_BASENAMES: frozenset[str] = frozenset(
    {"CLAIMS.md", "ACTIVE_ISSUES.md", "WHATS_NEXT.md"}
)

# Backward-compat alias: some callers may want the full set of
# conventional paths. We match on basename, so both spellings work.
PROTECTED_PATHS: frozenset[str] = PROTECTED_BASENAMES


# Severity tags. Kept as plain strings for trivial serialisation.
FAIL: str = "FAIL"
WARNING: str = "WARNING"
Severity = str


# Words that, if present in the same sentence as a flagged pattern,
# demote a FAIL to a WARNING. The guardrail scanner treats these as
# evidence that the forbidden object is being MENTIONED (as a dead
# shortcut, a no-go reference, or a scope limit) rather than imported.
QUALIFIER_WORDS: tuple[str, ...] = (
    "dead",
    "shortcut",
    "forbidden",
    "no-go",
    "no go",
    "not",
    "never",
    "fails",
    "fail",
    "failed",
    "contradicts",
    "rejected",
    "reject",
    "kill",
    "killed",
    "restricted",
    "does not",
    "do not",
    "cannot",
    "without",
    "dropped",
    "drop",
    "abandon",
    "abandoned",
    "ruled out",
    "ruled-out",
    "wrong",
    "refute",
    "refuted",
    "disproved",
    "mention",
    "mentions",
    "mentioned",
)

# Words that, if present in the same paragraph as a "nonlinear PF" /
# bridge-derivation warning, demote it to a WARNING of the "probably
# fine, reviewer please confirm" kind rather than a full FAIL.
BRIDGE_QUALIFIER_WORDS: tuple[str, ...] = (
    "free linearized",
    "free-linearized",
    "linearized",
    "linearised",
    "linear sector",
    "linear regime",
    "bridge",
    "bridge derivation",
    "not proved",
    "not claim",
    "does not claim",
    "not prove",
    "does not prove",
    "bounded",
    "scope",
    "out of scope",
    "restricted to",
    "bounded to",
    "does not broaden",
    "no bridge",
    "without a bridge",
    "without bridge",
)


# ----------------------------------------------------------------------
# Forbidden-string catalogue
# ----------------------------------------------------------------------

# A "category -> tuple of compiled regex" mapping. All regexes run
# case-INsensitive unless explicitly stated otherwise.

_H_PROD_OVERCLAIM_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, flags=re.IGNORECASE)
    for p in (
        r"H[_\s]*prod\s+is\s+proved\b",
        r"H[_\s]*prod\s+is\s+proven\b",
        r"fully\s+proves\s+H[_\s]*prod\b",
        r"H[_\s]*prod\s+is\s+closed\b",
        r"H[_\s]*prod\s+has\s+been\s+proved\b",
        r"H[_\s]*prod\s+has\s+been\s+proven\b",
        r"proof\s+of\s+H[_\s]*prod\s+is\s+complete\b",
        r"completes?\s+the\s+proof\s+of\s+H[_\s]*prod\b",
    )
)

_ESCAPE_OVERCLAIM_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, flags=re.IGNORECASE)
    for p in (
        r"fully\s+forbids\s+every\s+escape\s+ensemble",
        r"rules?\s+out\s+all\s+escape\s+ensembles?",
        r"rules?\s+out\s+every\s+escape\s+ensemble",
        r"forbids?\s+every\s+escape\s+ensemble",
        r"forbids?\s+all\s+escape\s+ensembles?",
        r"every\s+escape\s+ensemble\s+is\s+forbidden",
        r"all\s+escape\s+ensembles?\s+are\s+forbidden",
        r"PF\s+fully\s+forbids?\s+(?:the\s+)?escape",
        r"escape\s+(?:covariance|hatch)\s+is\s+physically\s+closed\s+in\s+full\s+generality",
    )
)

_NONLINEAR_PF_OVERCLAIM_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, flags=re.IGNORECASE)
    for p in (
        r"full\s+nonlinear\s+PF\b",
        r"full\s+non-linear\s+PF\b",
        r"nonlinear\s+Propagation\s+Framework",
        r"non-linear\s+Propagation\s+Framework",
        r"nonlinear\s+PF\s+vacuum\s+is\s+(?:proved|equal|fixed)",
        r"non-linear\s+PF\s+vacuum\s+is\s+(?:proved|equal|fixed)",
    )
)

FORBIDDEN_STRINGS: dict[str, tuple[re.Pattern[str], ...]] = {
    "H_prod_overclaim": _H_PROD_OVERCLAIM_PATTERNS,
    "escape_overclaim": _ESCAPE_OVERCLAIM_PATTERNS,
    "nonlinear_pf_overclaim": _NONLINEAR_PF_OVERCLAIM_PATTERNS,
}

# Which categories apply to which deliverable. Escape and nonlinear-PF
# overclaims are Vacuum_Note concerns; H_prod overclaims apply to both.
_VACUUM_ONLY_CATEGORIES: frozenset[str] = frozenset(
    {"escape_overclaim", "nonlinear_pf_overclaim"}
)


# ----------------------------------------------------------------------
# Score-upgrade patterns
# ----------------------------------------------------------------------

SCORE_UPGRADE_PATTERNS: tuple[re.Pattern[str], ...] = (
    # 0.88 -> 0.9 / 0.88 => 0.9 / 0.88 to 0.9 / 0.88 → 0.9
    re.compile(r"0\.\d{1,3}\s*(?:->|=>|\u2192|\bto\b)\s*0\.\d{1,3}"),
    # "upgrade to DERIVED", "upgraded to CONDITIONAL", etc.
    re.compile(
        r"\bupgrade[sd]?\s+to\s+(?:DERIVED|CONDITIONAL|PROVEN|CLOSED|PROVED)\b",
        flags=re.IGNORECASE,
    ),
    # "now DERIVED", "now PROVEN", etc.
    re.compile(
        r"\bnow\s+(?:DERIVED|PROVEN|PROVED|CLOSED|CONDITIONAL)\b",
        flags=re.IGNORECASE,
    ),
    # "promoted to DERIVED", "promote to CONDITIONAL"
    re.compile(
        r"\bpromot(?:e|es|ed|ing)\s+to\s+(?:DERIVED|CONDITIONAL|PROVEN|CLOSED|PROVED)\b",
        flags=re.IGNORECASE,
    ),
    # "confidence score ... <number>" transitions with arrow / "to"
    re.compile(
        r"\bconfidence\s+(?:score|level)\b[^.\n]*?(?:->|=>|\u2192|\bto\b)\s*0?\.?\d+",
        flags=re.IGNORECASE,
    ),
)


# Qualifiers that turn a score-upgrade match into a WARNING (or drop
# it entirely). These signal the sentence is explicitly disclaiming an
# upgrade rather than performing one.
_SCORE_UPGRADE_QUALIFIERS: tuple[str, ...] = (
    "does not upgrade",
    "do not upgrade",
    "no score change",
    "without upgrade",
    "without upgrading",
    "no upgrade",
    "not upgrade",
    "not promoted",
    "not promote",
    "no promotion",
    "without promoting",
    "no confidence change",
    "does not change",
    "do not change",
    "not a score",
    "not a confidence",
    "not score",
    "pending Codex audit",
    "pending audit",
    "recommendation",
    "recommend",
    "suggested",
    "tentative",
    "conditional on",
    "pending",
)


# ----------------------------------------------------------------------
# Forbidden-shortcut patterns
# ----------------------------------------------------------------------

# Each entry is (category_name, regex). The scanner runs every pattern
# against every line and then applies the qualifier-word downgrade.
_FORBIDDEN_SHORTCUT_SPECS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # Unqualified T = S̄ / T = S_bar / T = \bar S
    (
        "dead_pure_shift",
        re.compile(
            r"\bT\s*=\s*(?:S\u0305|S_bar|\\bar\s*S|S-bar)\b",
            flags=re.IGNORECASE,
        ),
    ),
    # b = 0 as a positive assumption. Bare "b = 0" occurrences will
    # still often appear in dead-shortcut references; the qualifier
    # downgrade handles that. Also match "b=0 closure", "set b to 0".
    (
        "revived_b_eq_0",
        re.compile(
            r"\bb\s*=\s*0\b(?!\s*(?:\.|,|\)))",
        ),
    ),
    (
        "revived_b_eq_0",
        re.compile(
            r"\bset\s+b\s*(?:=|to)\s*0\b",
            flags=re.IGNORECASE,
        ),
    ),
    # Path-A "projected {k=0, k=1} sector is forced"
    (
        "path_a_projection",
        re.compile(
            r"projected\s*\{?\s*k\s*=\s*0\s*,?\s*k\s*=\s*1\s*\}?\s+sector"
            r"\s+is\s+forced",
            flags=re.IGNORECASE,
        ),
    ),
    # QFT import presented as a derivation step. We look for
    # "from standard QFT" / "standard QFT gives" / "by QFT" followed by
    # an equation-looking tail on the same line.
    (
        "qft_imported_step",
        re.compile(
            r"\b(?:from\s+standard\s+QFT|standard\s+QFT\s+gives|"
            r"by\s+QFT|by\s+standard\s+QFT|QFT\s+tells\s+us)\b"
            r"[^.\n]*?(?:=|\\Box|\\partial|\\phi|\\chi|m\^?2|\bm\^2\b)",
            flags=re.IGNORECASE,
        ),
    ),
)


# ----------------------------------------------------------------------
# Result dataclasses
# ----------------------------------------------------------------------


@dataclass
class Match:
    """A single flagged item from a file scan.

    Attributes
    ----------
    category : str
        Short category tag (for example "H_prod_overclaim",
        "score_upgrade", "dead_pure_shift").
    pattern : str
        The literal regex source that triggered the match.
    line : int
        1-indexed line number in the scanned file.
    snippet : str
        The matched line, stripped of trailing whitespace and
        truncated to a reasonable display length.
    severity : str
        Either FAIL or WARNING. See module docstring.
    reason : str
        One-line diagnostic explaining the severity choice.
    """

    category: str
    pattern: str
    line: int
    snippet: str
    severity: Severity
    reason: str = ""


@dataclass
class FileScanResult:
    """Full scan report for a single file.

    Attributes
    ----------
    path : str
        The file path as given to `scan_file`.
    exists : bool
        True iff the file could be opened and read.
    is_deliverable : bool
        True iff the file path is FAMILY_C_PATH or VACUUM_NOTE_PATH
        (basename match). Deliverables are scanned; other files can be
        scanned too but are reported as non-deliverables.
    protected_path_violation : bool
        True iff the path's basename is in PROTECTED_BASENAMES. Any
        TRUE value here makes `passed` False regardless of matches.
    forbidden_matches : list[Match]
        Every match (FAIL or WARNING) found in the file.
    passed : bool
        True iff there are NO FAIL matches AND `protected_path_violation`
        is False AND the file exists.
    error : str
        Empty string on success; otherwise the string representation
        of the exception that stopped the scan.
    """

    path: str
    exists: bool
    is_deliverable: bool
    protected_path_violation: bool
    forbidden_matches: list[Match] = field(default_factory=list)
    passed: bool = True
    error: str = ""


@dataclass
class GuardrailReport:
    """Aggregate scan over both deliverables.

    Attributes
    ----------
    family_c_result : FileScanResult
        Scan result for the Family_C_Draft.
    vacuum_note_result : FileScanResult
        Scan result for the Vacuum_Note.
    passed : bool
        True iff both FileScanResult.passed are True AND no protected
        path is targeted by either deliverable AND at least one FAIL
        match did not occur.
    warnings : int
        Number of WARNING-severity matches across both files.
    fails : int
        Number of FAIL-severity matches across both files.
    """

    family_c_result: FileScanResult
    vacuum_note_result: FileScanResult
    passed: bool
    warnings: int
    fails: int


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _basename(path: str) -> str:
    """Return the basename of `path`, safely handling POSIX / Windows."""
    return os.path.basename(path.replace("\\", "/"))


def _split_into_sentences(line: str) -> list[str]:
    """Break a line into sentences for qualifier scanning.

    Markdown / prose sentences are separated mostly by periods,
    question marks, semicolons, and hard dashes. We keep this loose on
    purpose so that "T = S_bar. This shortcut is dead." is treated as
    two sentences, but "T = S_bar; this is a shortcut" still sees the
    qualifier in the same unit.
    """
    if not line:
        return [""]
    pieces = re.split(r"(?<=[.!?;])\s+", line)
    return [p for p in pieces if p.strip()] or [line]


def _has_qualifier(text: str, qualifiers: Iterable[str]) -> bool:
    """True iff any qualifier appears in `text`, case-insensitively."""
    lower = text.lower()
    return any(q.lower() in lower for q in qualifiers)


_LIST_MARKER_RE: re.Pattern[str] = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")


def _paragraph_of(lines: list[str], idx: int) -> str:
    """Return the paragraph surrounding `lines[idx]`.

    A paragraph is a block of consecutive non-blank lines. If the
    current paragraph is a bulleted / numbered list and the nearest
    preceding non-blank paragraph ends with a colon (the common
    markdown "intro: bullets" pattern), we extend the returned context
    to include that intro paragraph as well. This is what lets the
    scanner correctly treat

        This note does **not** claim:

        - that the full nonlinear PF vacuum is proved to equal this free vacuum

    as a qualified mention rather than an import: the "does **not**
    claim" intro lives in a different whitespace paragraph from the
    bullet, but it is semantically part of the same statement.

    `idx` is 0-indexed.
    """
    n = len(lines)
    if not (0 <= idx < n):
        return ""
    start = idx
    while start > 0 and lines[start - 1].strip():
        start -= 1
    end = idx
    while end + 1 < n and lines[end + 1].strip():
        end += 1
    current = lines[start : end + 1]

    # Intro-paragraph extension. If the current paragraph begins with
    # a list marker, walk back past the blank line(s) to find the
    # nearest preceding non-blank block and, if its last line ends with
    # ":", prepend that block to the context.
    if current and _LIST_MARKER_RE.match(current[0]):
        # Skip blank lines preceding the current paragraph.
        intro_end = start - 1
        while intro_end >= 0 and not lines[intro_end].strip():
            intro_end -= 1
        if intro_end >= 0 and lines[intro_end].rstrip().endswith(":"):
            intro_start = intro_end
            while (
                intro_start > 0 and lines[intro_start - 1].strip()
            ):
                intro_start -= 1
            intro = lines[intro_start : intro_end + 1]
            return "\n".join(intro + [""] + current)

    return "\n".join(current)


def _truncate(line: str, limit: int = 240) -> str:
    """Truncate a line for display, stripping trailing whitespace."""
    stripped = line.rstrip()
    if len(stripped) <= limit:
        return stripped
    return stripped[:limit] + "..."


def _severity_for_match(
    sentence: str,
    paragraph: str,
    qualifiers: Iterable[str],
    *,
    fail_default: bool = True,
) -> tuple[Severity, str]:
    """Return (severity, reason) given sentence/paragraph context."""
    if _has_qualifier(sentence, qualifiers):
        return (
            WARNING,
            "qualifier word(s) present in the same sentence; "
            "treating match as mention, not import",
        )
    if _has_qualifier(paragraph, qualifiers):
        return (
            WARNING,
            "qualifier word(s) present in the same paragraph; "
            "reviewer should confirm the match is a mention, not an import",
        )
    if fail_default:
        return (FAIL, "no qualifier found in sentence or paragraph")
    return (
        WARNING,
        "no qualifier found; flagged as warning for reviewer to confirm",
    )


# ----------------------------------------------------------------------
# Core scan loop
# ----------------------------------------------------------------------


def _scan_category_patterns(
    lines: list[str],
    category: str,
    patterns: tuple[re.Pattern[str], ...],
    qualifiers: Iterable[str],
    *,
    fail_default: bool = True,
) -> list[Match]:
    """Scan `lines` for every `pattern` in `patterns` under `category`."""
    matches: list[Match] = []
    for line_idx, line in enumerate(lines):
        for pat in patterns:
            if not pat.search(line):
                continue
            # Determine sentence context first (tighter), then paragraph.
            sentences = _split_into_sentences(line)
            hit_sentence = next(
                (s for s in sentences if pat.search(s)), line
            )
            paragraph = _paragraph_of(lines, line_idx)
            severity, reason = _severity_for_match(
                hit_sentence,
                paragraph,
                qualifiers,
                fail_default=fail_default,
            )
            matches.append(
                Match(
                    category=category,
                    pattern=pat.pattern,
                    line=line_idx + 1,
                    snippet=_truncate(line),
                    severity=severity,
                    reason=reason,
                )
            )
    return matches


def _scan_score_upgrades(lines: list[str]) -> list[Match]:
    """Run the SCORE_UPGRADE_PATTERNS sweep with the upgrade qualifiers."""
    qualifiers = _SCORE_UPGRADE_QUALIFIERS + QUALIFIER_WORDS
    return _scan_category_patterns(
        lines,
        category="score_upgrade",
        patterns=SCORE_UPGRADE_PATTERNS,
        qualifiers=qualifiers,
        fail_default=True,
    )


def _scan_forbidden_shortcuts(lines: list[str]) -> list[Match]:
    """Run the FORBIDDEN_SHORTCUTS sweep, grouped by category."""
    matches: list[Match] = []
    for category, pat in _FORBIDDEN_SHORTCUT_SPECS:
        matches.extend(
            _scan_category_patterns(
                lines,
                category=category,
                patterns=(pat,),
                qualifiers=QUALIFIER_WORDS,
                fail_default=True,
            )
        )
    return matches


def _scan_forbidden_strings(
    lines: list[str], is_vacuum_note: bool
) -> list[Match]:
    """Run FORBIDDEN_STRINGS sweeps. Some categories are vacuum-only."""
    matches: list[Match] = []
    for category, patterns in FORBIDDEN_STRINGS.items():
        if category in _VACUUM_ONLY_CATEGORIES and not is_vacuum_note:
            continue
        if category == "nonlinear_pf_overclaim":
            # Nonlinear-PF patterns are judged against a DIFFERENT
            # qualifier list (bridge-derivation qualifiers). They fail
            # only when NO bridge qualifier is present in the same
            # paragraph.
            matches.extend(
                _scan_category_patterns(
                    lines,
                    category=category,
                    patterns=patterns,
                    qualifiers=BRIDGE_QUALIFIER_WORDS + QUALIFIER_WORDS,
                    fail_default=True,
                )
            )
        else:
            matches.extend(
                _scan_category_patterns(
                    lines,
                    category=category,
                    patterns=patterns,
                    qualifiers=QUALIFIER_WORDS,
                    fail_default=True,
                )
            )
    return matches


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------


def assert_no_protected_file_writes(paths: Iterable[str]) -> None:
    """Raise `RuntimeError` if any path in `paths` is a protected file.

    The check is basename-based so relative ("./CLAIMS.md"), absolute
    ("/repo/CLAIMS.md"), and bare ("CLAIMS.md") references all trigger.
    This helper lets a caller route a list of intended write targets
    through the same rule the scanner uses.
    """
    bad: list[str] = []
    for p in paths:
        if p is None:
            continue
        base = _basename(str(p))
        if base in PROTECTED_BASENAMES:
            bad.append(str(p))
    if bad:
        raise RuntimeError(
            "Attempted write to protected Board_Documents: "
            + ", ".join(bad)
            + ". These files are read-only truth sources "
            + f"(see Requirement 9.1-9.2): {sorted(PROTECTED_BASENAMES)}"
        )


def scan_file(
    path: str, *, is_vacuum_note: bool | None = None
) -> FileScanResult:
    """Scan a single file for guardrail violations.

    Parameters
    ----------
    path : str
        Path to the file to scan, relative or absolute.
    is_vacuum_note : bool | None
        If None (default), auto-detected from the path basename. Pass
        True to force the vacuum-only category scans on, or False to
        force them off (for example, to test the scanner against the
        Family_C_Draft only).

    Returns
    -------
    FileScanResult
        See dataclass docstring. On IOError / read failure, returns a
        FileScanResult with exists=False, passed=False, and `error`
        set to the exception repr.
    """
    base = _basename(path)
    protected = base in PROTECTED_BASENAMES
    is_deliverable = base in {
        _basename(FAMILY_C_PATH),
        _basename(VACUUM_NOTE_PATH),
    }

    if is_vacuum_note is None:
        is_vacuum_note = base == _basename(VACUUM_NOTE_PATH)

    # Short-circuit if the path itself is a protected file. We do NOT
    # scan it (we do not want to load CLAIMS.md etc. into this
    # process's scan space), and the scanner returns an immediate
    # violation so callers cannot silently feed a forbidden target.
    if protected:
        return FileScanResult(
            path=path,
            exists=False,
            is_deliverable=False,
            protected_path_violation=True,
            forbidden_matches=[],
            passed=False,
            error=(
                f"refusing to scan protected Board_Document {base!r}; "
                "deliverables must never be these files"
            ),
        )

    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError as exc:
        return FileScanResult(
            path=path,
            exists=False,
            is_deliverable=is_deliverable,
            protected_path_violation=False,
            forbidden_matches=[],
            passed=False,
            error=f"file not found: {exc!r}",
        )
    except OSError as exc:
        return FileScanResult(
            path=path,
            exists=False,
            is_deliverable=is_deliverable,
            protected_path_violation=False,
            forbidden_matches=[],
            passed=False,
            error=f"OS error: {exc!r}",
        )

    lines = text.splitlines()
    matches: list[Match] = []
    matches.extend(_scan_forbidden_strings(lines, is_vacuum_note))
    matches.extend(_scan_score_upgrades(lines))
    matches.extend(_scan_forbidden_shortcuts(lines))

    fails = [m for m in matches if m.severity == FAIL]
    passed = (not fails) and (not protected)

    return FileScanResult(
        path=path,
        exists=True,
        is_deliverable=is_deliverable,
        protected_path_violation=False,
        forbidden_matches=matches,
        passed=passed,
        error="",
    )


def run_guardrail_check(
    family_c_path: str = FAMILY_C_PATH,
    vacuum_note_path: str = VACUUM_NOTE_PATH,
) -> GuardrailReport:
    """Scan both deliverables and aggregate the results.

    Neither path is allowed to be a protected Board_Document. If either
    caller-supplied path matches, the corresponding FileScanResult
    comes back with `protected_path_violation=True` and the overall
    report is marked failed.
    """
    # Trivial but spec-mandated: confirm the configured deliverable
    # paths themselves are not protected (Requirement 9.1, 9.2).
    assert _basename(family_c_path) not in PROTECTED_BASENAMES, (
        f"family_c_path {family_c_path!r} resolves to a protected "
        f"Board_Document basename"
    )
    assert _basename(vacuum_note_path) not in PROTECTED_BASENAMES, (
        f"vacuum_note_path {vacuum_note_path!r} resolves to a protected "
        f"Board_Document basename"
    )

    family_c = scan_file(family_c_path, is_vacuum_note=False)
    vacuum = scan_file(vacuum_note_path, is_vacuum_note=True)

    fails = sum(
        1
        for r in (family_c, vacuum)
        for m in r.forbidden_matches
        if m.severity == FAIL
    )
    warnings = sum(
        1
        for r in (family_c, vacuum)
        for m in r.forbidden_matches
        if m.severity == WARNING
    )
    overall_passed = family_c.passed and vacuum.passed

    return GuardrailReport(
        family_c_result=family_c,
        vacuum_note_result=vacuum,
        passed=overall_passed,
        warnings=warnings,
        fails=fails,
    )


__all__ = [
    "FAMILY_C_PATH",
    "VACUUM_NOTE_PATH",
    "PROTECTED_BASENAMES",
    "PROTECTED_PATHS",
    "FAIL",
    "WARNING",
    "Severity",
    "FORBIDDEN_STRINGS",
    "SCORE_UPGRADE_PATTERNS",
    "Match",
    "FileScanResult",
    "GuardrailReport",
    "scan_file",
    "run_guardrail_check",
    "assert_no_protected_file_writes",
]


# ----------------------------------------------------------------------
# CLI summary
# ----------------------------------------------------------------------


def _print_file_result(result: FileScanResult) -> None:
    header = f"{result.path}"
    print(header)
    print("-" * min(len(header), 70))
    if not result.exists:
        print(f"  [ERROR] {result.error}")
        print(f"  passed = {result.passed}")
        return
    print(
        f"  is_deliverable           = {result.is_deliverable}"
    )
    print(
        f"  protected_path_violation = {result.protected_path_violation}"
    )
    if not result.forbidden_matches:
        print("  no matches")
    else:
        by_cat: dict[str, list[Match]] = {}
        for m in result.forbidden_matches:
            by_cat.setdefault(m.category, []).append(m)
        for cat, ms in sorted(by_cat.items()):
            n_fail = sum(1 for m in ms if m.severity == FAIL)
            n_warn = sum(1 for m in ms if m.severity == WARNING)
            print(
                f"  [{cat}] {len(ms)} match(es)  "
                f"FAIL={n_fail} WARNING={n_warn}"
            )
            for m in ms:
                flag = "FAIL" if m.severity == FAIL else "WARN"
                print(
                    f"    ({flag}) line {m.line}: "
                    f"{m.snippet}"
                )
                if m.reason:
                    print(f"          -> {m.reason}")
    print(f"  passed = {result.passed}")


def _print_report(report: GuardrailReport) -> None:
    print("verification.guardrail_check")
    print("=" * 70)
    _print_file_result(report.family_c_result)
    print()
    _print_file_result(report.vacuum_note_result)
    print()
    print("-" * 70)
    print(f"total FAILs    = {report.fails}")
    print(f"total WARNINGs = {report.warnings}")
    print(f"overall passed = {report.passed}")


def main() -> int:
    """Run the guardrail check on the two configured deliverables."""
    # First verify the two configured deliverable paths exist on disk.
    # A missing deliverable is a configuration error, not a guardrail
    # violation, and we want a clear message.
    missing: list[str] = []
    for p in (FAMILY_C_PATH, VACUUM_NOTE_PATH):
        if not os.path.isfile(p):
            missing.append(p)
    if missing:
        print(
            "ERROR: deliverable path(s) do not exist on disk: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "This scanner expects the two deliverables at their "
            "canonical locations:",
            file=sys.stderr,
        )
        print(f"  FAMILY_C_PATH    = {FAMILY_C_PATH}", file=sys.stderr)
        print(f"  VACUUM_NOTE_PATH = {VACUUM_NOTE_PATH}", file=sys.stderr)
        return 2

    report = run_guardrail_check()
    _print_report(report)

    # Hard invariants: the configured deliverable paths themselves are
    # NOT protected files. (Trivial but the spec asks for it.)
    assert (
        _basename(FAMILY_C_PATH) not in PROTECTED_BASENAMES
    ), f"FAMILY_C_PATH {FAMILY_C_PATH!r} is a Board_Document!"
    assert (
        _basename(VACUUM_NOTE_PATH) not in PROTECTED_BASENAMES
    ), f"VACUUM_NOTE_PATH {VACUUM_NOTE_PATH!r} is a Board_Document!"

    # And the overall scan must pass (no FAIL matches, no protected
    # path violations on either deliverable).
    assert report.passed, (
        "guardrail_check: scan surfaced FAIL-severity matches or a "
        "protected-path violation; see the report above. This module "
        "does NOT rewrite the deliverables -- the caller must decide "
        "how to address each finding."
    )

    print()
    print("guardrail_check: all invariants satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
