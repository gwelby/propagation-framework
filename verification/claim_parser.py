"""CLAIMS.md parser for the Propagation Framework verification harness.

This module implements a read-only parser that turns the live
``CLAIMS.md`` scoreboard into structured :class:`Claim` records keyed by
slugified claim id. It does NOT modify ``CLAIMS.md`` and it does NOT
create a second canonical scoreboard; the returned dict is a structured
view of the single source of truth.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md` Req. 1
  (CLAIMS.md parsing: all tiers, unique ids, named hypotheses and known
  gaps preserved, format errors surfaced with line numbers).

Run ``python -m verification.claim_parser`` as a quick self-check; the
``__main__`` block parses the fixture and the real board and prints a
summary of each claim's status, confidence, and extracted metadata.
"""

from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path
from typing import Iterable

from verification.models import Claim, ClaimStatus


# ---------------------------------------------------------------------------
# Tier definitions and helpers
# ---------------------------------------------------------------------------

# Valid confidence ranges per tier as stated in the CLAIMS.md grading scale.
# Values outside these ranges are a WARN signal (not a parse failure).
CONFIDENCE_RANGES: dict[ClaimStatus, tuple[float, float]] = {
    ClaimStatus.DERIVED: (0.90, 1.00),
    ClaimStatus.CONDITIONAL: (0.75, 0.89),
    ClaimStatus.PARTIAL_DERIVATION: (0.75, 0.89),
    ClaimStatus.ARGUED: (0.70, 0.89),
    ClaimStatus.EMPIRICAL: (0.60, 0.95),
    ClaimStatus.INTUITION: (0.30, 0.59),
    ClaimStatus.OPEN: (0.00, 0.29),
    ClaimStatus.NO_GO: (0.00, 0.29),
}

# Section headers we want to scope table parsing to.
_SCOREBOARD_SECTIONS: tuple[str, ...] = (
    "### 1. Fundamental Physics",
    "### 2. Biological & Cognitive Systems",
)

# Header signatures we recognize as scoreboard row headers. The foundational
# definitions table starts with "| Definition |" and is intentionally skipped.
_CLAIM_HEADER_PREFIX = "| Claim |"


# ---------------------------------------------------------------------------
# Small text utilities
# ---------------------------------------------------------------------------


_BOLD_RE = re.compile(r"\*\*(.*?)\*\*", re.DOTALL)
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def _strip_bold(value: str) -> str:
    """Strip ``**bold**`` markdown wrappers, preserving inner content."""

    # Replace **x** with x. Leave lone ** sequences alone (they are rare
    # inside evidence but should not corrupt the text if present).
    return _BOLD_RE.sub(r"\1", value)


def _slugify(name: str) -> str:
    """Turn a claim row label into a stable lowercase identifier.

    The rules match the design spec:
      * strip surrounding ``**bold**`` markdown
      * lowercase
      * replace non-alphanumeric sequences with ``_``
      * collapse repeated underscores
      * strip leading/trailing underscores
    """

    text = _strip_bold(name).strip().lower()
    slug = _NON_ALNUM_RE.sub("_", text)
    slug = re.sub(r"_+", "_", slug)
    return slug.strip("_")


def _split_table_row(line: str) -> list[str]:
    """Split a pipe-delimited markdown table row into its cells.

    The leading and trailing pipes are consumed, so a row like
    ``| a | b | c |`` returns ``["a", "b", "c"]``. Cell values are
    stripped of surrounding whitespace.

    CLAIMS.md uses unescaped pipes in three places that must NOT be
    treated as column separators:

      * inside backtick-quoted inline code
        (e.g. ``C[psi] = integral |psi|^2 dmu``)
      * in bare double-pipe math norms outside backticks
        (e.g. ``||U(1)||^2``)
      * in bare absolute-value notation
        (e.g. ``|δ − 2/9|``)

    The splitter handles all three by treating a ``|`` as a column
    separator only when it is surrounded by whitespace (or at the row
    edge). Escaped pipes (``\\|``) are preserved defensively.
    """

    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []

    cells: list[str] = []
    current: list[str] = []
    in_code = False
    inner = stripped[1:-1]
    n = len(inner)
    i = 0
    while i < n:
        ch = inner[i]
        if ch == "\\" and i + 1 < n and inner[i + 1] == "|":
            # Escaped pipe: preserve literally.
            current.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
            current.append(ch)
            i += 1
            continue
        if ch == "|" and not in_code:
            prev_char = inner[i - 1] if i > 0 else ""
            next_char = inner[i + 1] if i + 1 < n else ""
            # Column separator: preceded by whitespace (or at the start of
            # the stripped inner) AND followed by whitespace (or at the
            # end of the stripped inner). Otherwise it is a math token.
            prev_is_sep = (prev_char == "" or prev_char.isspace())
            next_is_sep = (next_char == "" or next_char.isspace())
            if prev_is_sep and next_is_sep:
                cells.append("".join(current).strip())
                current = []
                i += 1
                continue
        current.append(ch)
        i += 1

    # Flush final cell.
    cells.append("".join(current).strip())
    return cells


def _is_alignment_row(cells: list[str]) -> bool:
    """Return True if the cells look like a markdown alignment row.

    Alignment rows contain only ``:``, ``-``, and whitespace (e.g.
    ``| :--- | :--- |``).
    """

    if not cells:
        return False
    return all(re.fullmatch(r":?-+:?", cell.strip() or "-") for cell in cells)


def _normalize_status(raw: str) -> ClaimStatus | None:
    """Normalize a raw status cell to a :class:`ClaimStatus`.

    Handles ``**bold**`` wrappers and the two-word ``PARTIAL DERIVATION``
    spelling used on the board. Returns ``None`` when the value does not
    match any known tier.
    """

    text = _strip_bold(raw).strip().upper()
    # Collapse inner whitespace so "PARTIAL   DERIVATION" still works.
    text = re.sub(r"\s+", " ", text)
    if text == "PARTIAL DERIVATION":
        return ClaimStatus.PARTIAL_DERIVATION
    # Try a few common spellings. The enum values already use the canonical
    # form (DERIVED, CONDITIONAL, etc.).
    candidate = text.replace(" ", "_")
    try:
        return ClaimStatus(candidate)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Confidence parsing
# ---------------------------------------------------------------------------


_FLOAT_RE = re.compile(r"-?\d+(?:\.\d+)?")


def _parse_confidence(raw: str, line_num: int) -> float:
    """Parse the first float from a confidence cell.

    Some rows carry decorated values such as
    ``0.35 (as derivation); 0.60 (as structural identification)``. We use
    the first float in the cell, which matches the board's primary
    confidence for that row.
    """

    match = _FLOAT_RE.search(raw)
    if not match:
        raise ValueError(
            f"CLAIMS.md line {line_num}: could not find a numeric confidence "
            f"value in cell {raw!r}"
        )
    try:
        return float(match.group(0))
    except ValueError as exc:  # pragma: no cover - defensive
        raise ValueError(
            f"CLAIMS.md line {line_num}: confidence value {match.group(0)!r} "
            f"is not a valid float"
        ) from exc


def _warn_confidence_out_of_range(
    claim_id: str, status: ClaimStatus, confidence: float, line_num: int
) -> None:
    """Emit a WARN (as a ``warnings.warn``) if confidence is outside range."""

    lo, hi = CONFIDENCE_RANGES[status]
    if not (lo <= confidence <= hi):
        warnings.warn(
            f"CLAIMS.md line {line_num}: claim {claim_id!r} has confidence "
            f"{confidence:.3f} outside the stated {status.value} range "
            f"[{lo:.2f}, {hi:.2f}].",
            stacklevel=2,
        )


# ---------------------------------------------------------------------------
# Evidence text extraction helpers
# ---------------------------------------------------------------------------


# Capture markdown links of the form [label](derivations/foo.md) and plain
# or backticked path references to derivations/... and sandbox/....
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_PATH_TOKEN_RE = re.compile(
    r"`?(?P<path>(?:[A-Za-z0-9_./-]+/)?(?:derivations|sandbox)/[A-Za-z0-9_./-]+\.(?:md|py))`?"
)


def _extract_file_refs(evidence: str) -> tuple[list[str], list[str]]:
    """Pull ``derivations/*.md`` and ``sandbox/*.py`` refs out of evidence.

    Matches markdown links, backticked inline paths, and bare path tokens.
    The returned lists are deduplicated while preserving first-seen order.
    """

    derivation_refs: list[str] = []
    sandbox_refs: list[str] = []

    def _add(path: str) -> None:
        # Strip any leading "/mnt/d/fundamentals/" style workspace prefix
        # so the relative path lives alongside the repo layout.
        norm = path.strip()
        # Anchor the relative portion to the first "derivations/" or
        # "sandbox/" token found in the path, dropping anything before it.
        for anchor in ("derivations/", "sandbox/"):
            idx = norm.find(anchor)
            if idx >= 0:
                norm = norm[idx:]
                break
        if norm.startswith("derivations/") and norm.endswith(".md"):
            if norm not in derivation_refs:
                derivation_refs.append(norm)
        elif norm.startswith("sandbox/") and (
            norm.endswith(".py") or norm.endswith(".md")
        ):
            if norm not in sandbox_refs:
                sandbox_refs.append(norm)

    for match in _MD_LINK_RE.finditer(evidence):
        _add(match.group(1))

    for match in _PATH_TOKEN_RE.finditer(evidence):
        _add(match.group("path"))

    return derivation_refs, sandbox_refs


# Named hypothesis patterns. We stay conservative: include explicit
# ``H_foo``/``A_NR`` tokens, and any backticked token that starts with
# ``H_``. We also record short snippets around "pending closure of ..."
# and "named hypothesis ..." phrasings so the runner has context.
_HYP_TOKEN_RE = re.compile(r"`([HA]_[A-Za-z_][A-Za-z0-9_]*)`|\b([HA]_[A-Za-z_][A-Za-z0-9_]*)\b")
_HYP_PHRASE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"pending closure of\s+`?([^`.;,\n]+?)`?(?=[.;,\n])", re.IGNORECASE),
    re.compile(r"named hypothesis\s+`?([^`.;,\n]+?)`?(?=[.;,\n])", re.IGNORECASE),
    re.compile(r"resting on\s+(?:a\s+)?named hypothesis\s+`?([^`.;,\n]+?)`?(?=[.;,\n])", re.IGNORECASE),
    re.compile(r"until\s+`?([HA]_[A-Za-z0-9_]+)`?\s+is\s+(?:closed|derived)", re.IGNORECASE),
)


def _extract_named_hypotheses(evidence: str) -> list[str]:
    """Extract named hypotheses from evidence text.

    Looks for ``H_foo``/``A_NR``-style tokens and short phrasings like
    ``pending closure of X``. Returned as a deduplicated list preserving
    first-seen order.
    """

    found: list[str] = []

    def _add(value: str) -> None:
        cleaned = value.strip().strip("`").strip()
        if cleaned and cleaned not in found:
            found.append(cleaned)

    # Token-level matches (H_prod, A_NR, etc.).
    for match in _HYP_TOKEN_RE.finditer(evidence):
        token = match.group(1) or match.group(2)
        if token:
            _add(token)

    # Phrase-level matches: keep the whole matched snippet so the runner
    # has context when the hypothesis is not a single H_ token.
    for pattern in _HYP_PHRASE_PATTERNS:
        for match in pattern.finditer(evidence):
            _add(match.group(1))

    return found


# Known-gap extraction for ARGUED claims.
_GAP_SENTENCE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?:^|[.;])\s*([^.;]*\bgap:[^.;]*)", re.IGNORECASE),
    re.compile(r"([^.;]*\bis not yet derived\b[^.;]*)", re.IGNORECASE),
    re.compile(r"([^.;]*\bis still pending\b[^.;]*)", re.IGNORECASE),
    re.compile(r"([^.;]*\bremaining gap\b[^.;]*)", re.IGNORECASE),
    re.compile(r"([^.;]*\bnot yet shown locally\b[^.;]*)", re.IGNORECASE),
    re.compile(r"([^.;]*\bnot yet closed\b[^.;]*)", re.IGNORECASE),
)


def _extract_known_gaps(evidence: str) -> list[str]:
    """Extract short gap snippets from ARGUED-tier evidence text."""

    found: list[str] = []

    def _add(snippet: str) -> None:
        cleaned = " ".join(snippet.split()).strip(" .;")
        if not cleaned:
            return
        # Hard-cap length so we record a snippet, not a whole paragraph.
        if len(cleaned) > 240:
            cleaned = cleaned[:237].rstrip() + "..."
        if cleaned and cleaned not in found:
            found.append(cleaned)

    for pattern in _GAP_SENTENCE_PATTERNS:
        for match in pattern.finditer(evidence):
            _add(match.group(1))

    return found


# ---------------------------------------------------------------------------
# Row -> Claim translation
# ---------------------------------------------------------------------------


def _row_to_claim(
    cells: list[str],
    line_num: int,
) -> Claim:
    """Translate a 5-cell scoreboard row into a :class:`Claim`.

    The expected column layout is:
        ``| Claim | Status | Evidence | What Falsifies It | Confidence |``

    Raises :class:`ValueError` if required fields cannot be parsed.
    """

    if len(cells) != 5:
        raise ValueError(
            f"CLAIMS.md line {line_num}: expected a 5-column scoreboard row, "
            f"got {len(cells)} columns: {cells!r}"
        )

    raw_name, raw_status, raw_evidence, raw_falsification, raw_confidence = cells

    name = _strip_bold(raw_name).strip()
    if not name:
        raise ValueError(
            f"CLAIMS.md line {line_num}: claim name cell is empty"
        )

    status = _normalize_status(raw_status)
    if status is None:
        raise ValueError(
            f"CLAIMS.md line {line_num}: unrecognized status value "
            f"{raw_status!r}"
        )

    confidence = _parse_confidence(raw_confidence, line_num)
    claim_id = _slugify(name)

    _warn_confidence_out_of_range(claim_id, status, confidence, line_num)

    evidence_summary = raw_evidence.strip()
    falsification = raw_falsification.strip()

    derivation_files, sandbox_scripts = _extract_file_refs(evidence_summary)

    named_hypotheses: list[str] = []
    if status in (ClaimStatus.CONDITIONAL, ClaimStatus.PARTIAL_DERIVATION):
        named_hypotheses = _extract_named_hypotheses(evidence_summary)

    known_gaps: list[str] = []
    if status is ClaimStatus.ARGUED:
        known_gaps = _extract_known_gaps(evidence_summary)

    return Claim(
        id=claim_id,
        name=name,
        status=status,
        confidence=confidence,
        evidence_summary=evidence_summary,
        falsification_criterion=falsification,
        derivation_files=derivation_files,
        audited_derivation_refs=[],  # populated below from support_manifest
        sandbox_scripts=sandbox_scripts,
        named_hypotheses=named_hypotheses,
        known_gaps=known_gaps,
        source_row=line_num,
    )


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------


def _iter_scoreboard_rows(lines: Iterable[str]) -> Iterable[tuple[int, str]]:
    """Yield (line_num, raw_line) pairs that are candidate scoreboard data rows.

    Scoping rules:
      * only emit rows inside one of the configured scoreboard sections
      * require the most recent header row in the active section to be a
        ``| Claim | Status | ...`` header (skips the foundational
        ``| Definition |`` table and the grading scale)
      * skip alignment rows (``| :--- |``) and blank rows
    """

    section_active = False
    header_active = False

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")

        # Detect section boundaries.
        if line.startswith("## ") or line.startswith("### "):
            # Entering a new section or subsection resets header tracking.
            header_active = False
            section_active = any(
                line.startswith(header) for header in _SCOREBOARD_SECTIONS
            )
            continue

        if not section_active:
            continue

        stripped = line.strip()
        if not stripped.startswith("|"):
            # A non-table line ends the current header context but does not
            # leave the section (prose lines between tables are allowed).
            continue

        cells = _split_table_row(line)
        if not cells:
            continue

        if _is_alignment_row(cells):
            # Alignment row only matters if we just saw a Claim header.
            continue

        # Recognize the Claim header that prefaces each scoreboard table.
        if stripped.startswith(_CLAIM_HEADER_PREFIX):
            header_active = True
            continue

        # Any other header (e.g. "| Definition |") deactivates our claim
        # context for this section.
        if any(
            stripped.startswith(prefix)
            for prefix in ("| Definition |", "| Status |")
        ):
            header_active = False
            continue

        if not header_active:
            continue

        yield idx, line


def parse_claims_md(
    path: str | Path,
    support_manifest: dict | None = None,
) -> dict[str, Claim]:
    """Parse ``CLAIMS.md`` into a dict keyed by slugified claim id.

    Args:
        path: Filesystem path to a CLAIMS.md-format file.
        support_manifest: Optional already-loaded support manifest. When
            provided, the parser populates each claim's
            ``audited_derivation_refs`` with matching file paths from the
            manifest. The expected layout is
            ``{"claim_id": [{"path": "derivations/...", ...}, ...]}``.

    Returns:
        A dict of :class:`Claim` records keyed by slugified id.

    Raises:
        ValueError: on unrecognized row formats or duplicate claim ids.
            The message includes the offending line number.
    """

    source_path = Path(path)
    text = source_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    claims: dict[str, Claim] = {}

    for line_num, line in _iter_scoreboard_rows(lines):
        cells = _split_table_row(line)
        claim = _row_to_claim(cells, line_num)

        if claim.id in claims:
            other = claims[claim.id]
            raise ValueError(
                f"CLAIMS.md line {line_num}: claim id {claim.id!r} collides "
                f"with earlier row on line {other.source_row} "
                f"({other.name!r} vs {claim.name!r}). Rename one of the rows "
                f"or adjust the slugifier."
            )

        claims[claim.id] = claim

    # Populate audited_derivation_refs from the support manifest, if any.
    if support_manifest:
        _apply_support_manifest(claims, support_manifest)

    return claims


def _apply_support_manifest(
    claims: dict[str, Claim], support_manifest: dict
) -> None:
    """Attach audit-qualified derivation refs to matching claims.

    The manifest is expected in the shape loaded from
    ``verification/support_manifest.yaml``:

        {
            "support": {
                "claim_id": [
                    {"path": "derivations/foo.md", "audit_status": "DERIVED", ...},
                    ...
                ],
                ...
            }
        }

    The top-level ``"support"`` wrapper is optional; if it is missing,
    the manifest is treated as already being the inner mapping.
    """

    mapping = support_manifest.get("support", support_manifest)
    if not isinstance(mapping, dict):
        return

    for claim_id, entries in mapping.items():
        claim = claims.get(claim_id)
        if claim is None or not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            path_value = entry.get("path")
            if isinstance(path_value, str) and path_value not in claim.audited_derivation_refs:
                claim.audited_derivation_refs.append(path_value)


# ---------------------------------------------------------------------------
# Self-check entry point
# ---------------------------------------------------------------------------


def _summary_line(claim: Claim) -> str:
    return (
        f"  {claim.id:40s}  {claim.status.value:20s}  "
        f"conf={claim.confidence:.2f}  "
        f"hyp={len(claim.named_hypotheses):2d}  "
        f"gaps={len(claim.known_gaps):2d}  "
        f"derivs={len(claim.derivation_files):2d}  "
        f"sandbox={len(claim.sandbox_scripts):2d}"
    )


def _print_report(label: str, claims: dict[str, Claim]) -> None:
    print(f"=== {label} ===")
    print(f"  parsed {len(claims)} claims")
    print("  ids:")
    for cid in claims:
        print(f"    - {cid}")
    print("  summary:")
    for claim in claims.values():
        print(_summary_line(claim))
    print()


def _main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    fixture_path = repo_root / "tests" / "fixtures" / "claims_fixture.md"
    real_path = repo_root / "CLAIMS.md"

    exit_code = 0

    for label, path in (("FIXTURE", fixture_path), ("REAL CLAIMS.md", real_path)):
        if not path.exists():
            print(f"[skip] {label}: {path} not found", file=sys.stderr)
            continue
        try:
            claims = parse_claims_md(path)
        except ValueError as exc:
            print(f"[FAIL] {label}: {exc}", file=sys.stderr)
            exit_code = 1
            continue
        _print_report(f"{label} ({path})", claims)

    return exit_code


if __name__ == "__main__":
    sys.exit(_main())
