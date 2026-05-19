"""Dependency overlay loader for the verification harness.

The overlay is a small read-only YAML file
(``verification/dependency_overlay.yaml``) that declares explicit
structural dependency edges between claims already present in
``CLAIMS.md``. This loader parses the file, validates its shape, and
resolves the human-friendly short ids it contains against the real
slugified claim ids produced by :mod:`verification.claim_parser`.

The overlay is *metadata only*: it must never redefine a claim's
status or confidence score. Any top-level or per-edge ``status:`` /
``confidence:`` key is rejected with a BLOCK-level :class:`ValueError`
(Requirement 2.7).

Id resolution strategy for every ``upstream`` / ``downstream`` ref:

    1. Exact match against ``parsed_claims``.
    2. Suffix match: the parsed id equals the ref or ends with
       ``"_" + ref``. ``topological_weights`` matches
       ``2_1_topological_weights`` this way.
    3. Token-superset match: the ref's underscore-delimited tokens are
       a subset of the parsed id's tokens, and exactly one parsed id
       wins (shortest winner when multiple tie). ``koide_q`` matches
       ``koide_law_for_charged_leptons_q_2_3`` this way. This lane is
       a last-resort fallback and emits a WARN via :mod:`logging`.
    4. If nothing resolves, raise :class:`ValueError` with the list of
       candidate ids so the operator can fix the overlay.

Run ``python -m verification.dependency_overlay`` as a self-check; the
``__main__`` block loads the real overlay against the real CLAIMS.md
and prints the resolved edges.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 2.1, 2.2, 2.3, 2.7
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import yaml

from verification.claim_parser import parse_claims_md
from verification.models import Claim, DependencyEdge


logger = logging.getLogger(__name__)


# Keys that are forbidden at the top level of the overlay or inside an
# individual edge. The overlay is a dependency annotation file; it must
# not carry claim status or confidence overrides. See Req. 2.7.
_FORBIDDEN_KEYS: frozenset[str] = frozenset({"status", "confidence"})


# ---------------------------------------------------------------------------
# Shared id resolution helper (used by support_manifest.py as well)
# ---------------------------------------------------------------------------


def resolve_claim_id(
    ref_id: str,
    parsed_claims: dict[str, Claim],
    *,
    source_hint: str = "",
) -> str:
    """Resolve ``ref_id`` to a key in ``parsed_claims``.

    The strategy (first hit wins):

        1. Exact match.
        2. Suffix match (``cid == ref_id`` or ``cid.endswith("_" + ref_id)``).
           If unique, returns it. If ambiguous, raises with the tie set.
        3. Token-superset fallback: ``set(ref_id.split("_")) <=
           set(cid.split("_"))``. A unique winner is returned; ties are
           broken by fewest tokens and only resolved when exactly one id
           ties for the minimum. Falling through to this lane logs a
           WARN so the operator knows the overlay uses a fuzzy match.

    Args:
        ref_id: The id as written in the YAML (e.g. ``"koide_q"``).
        parsed_claims: Dict of :class:`Claim` records keyed by parsed id.
        source_hint: Short string appended to error/warn messages
            identifying where ``ref_id`` was encountered.

    Raises:
        ValueError: when no candidate resolves or a fallback lane is
            ambiguous. The message lists the available claim ids.
    """

    if not isinstance(ref_id, str) or not ref_id:
        raise ValueError(
            f"claim id reference must be a non-empty string "
            f"(got {ref_id!r}){_hint(source_hint)}"
        )

    # 1. Exact.
    if ref_id in parsed_claims:
        return ref_id

    # 2. Suffix.
    suffix_matches = [
        cid
        for cid in parsed_claims
        if cid == ref_id or cid.endswith("_" + ref_id)
    ]
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    if len(suffix_matches) > 1:
        raise ValueError(
            f"ambiguous suffix match for claim id {ref_id!r}"
            f"{_hint(source_hint)}: candidates {sorted(suffix_matches)}. "
            f"Rewrite the overlay/manifest to use a longer id."
        )

    # 3. Token-superset fallback.
    ref_tokens = set(ref_id.split("_"))
    token_matches = [
        cid
        for cid in parsed_claims
        if ref_tokens.issubset(set(cid.split("_")))
    ]
    if token_matches:
        # Prefer the candidate with the fewest extra tokens; only accept
        # if that shortest candidate is unique.
        token_matches.sort(key=lambda c: (len(c.split("_")), c))
        shortest_len = len(token_matches[0].split("_"))
        shortest = [c for c in token_matches if len(c.split("_")) == shortest_len]
        if len(shortest) == 1:
            logger.warning(
                "resolve_claim_id: using token-superset fallback for %r -> %r"
                "%s",
                ref_id,
                shortest[0],
                _hint(source_hint),
            )
            return shortest[0]
        raise ValueError(
            f"ambiguous token-superset match for claim id {ref_id!r}"
            f"{_hint(source_hint)}: tied at {shortest_len} tokens between "
            f"{shortest}"
        )

    raise ValueError(
        f"could not resolve claim id {ref_id!r}{_hint(source_hint)}. "
        f"No parsed claim matches exactly, by suffix, or by token-superset. "
        f"Known claim ids: {sorted(parsed_claims)}"
    )


def _hint(source_hint: str) -> str:
    return f" (at {source_hint})" if source_hint else ""


# ---------------------------------------------------------------------------
# Overlay loader
# ---------------------------------------------------------------------------


def load_dependency_overlay(
    path: str | Path | None,
    parsed_claims: dict[str, Claim],
) -> list[DependencyEdge]:
    """Load ``path`` as a dependency overlay YAML.

    Args:
        path: Filesystem path to the overlay file, or ``None``. When
            ``None`` or the file does not exist, an empty list is
            returned (an overlay is optional by design).
        parsed_claims: The claim dict produced by
            :func:`verification.claim_parser.parse_claims_md`; used to
            resolve human-friendly ids into the real slugified ids.

    Returns:
        List of :class:`DependencyEdge` records whose ``upstream`` and
        ``downstream`` fields are keys into ``parsed_claims``.

    Raises:
        ValueError: with severity BLOCK when the YAML redefines claim
            statuses/confidence, has missing required fields, or
            contains unresolvable claim ids.
    """

    if path is None:
        return []
    overlay_path = Path(path)
    if not overlay_path.is_file():
        logger.info(
            "load_dependency_overlay: %s not found; continuing with no edges",
            overlay_path,
        )
        return []

    with overlay_path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    if raw is None:
        return []
    if not isinstance(raw, dict):
        raise ValueError(
            f"dependency overlay {overlay_path}: top-level document must be a "
            f"mapping with an 'edges' list (got {type(raw).__name__})"
        )

    _reject_forbidden_keys(raw, context=f"{overlay_path} top-level")

    edges_raw = raw.get("edges")
    if edges_raw is None:
        # An overlay with no edges is valid — the file may be a stub.
        return []
    if not isinstance(edges_raw, list):
        raise ValueError(
            f"dependency overlay {overlay_path}: 'edges' must be a list "
            f"(got {type(edges_raw).__name__})"
        )

    resolved: list[DependencyEdge] = []
    for index, edge_raw in enumerate(edges_raw):
        if not isinstance(edge_raw, dict):
            raise ValueError(
                f"dependency overlay {overlay_path}: edge #{index} must be a "
                f"mapping (got {type(edge_raw).__name__})"
            )
        _reject_forbidden_keys(
            edge_raw, context=f"{overlay_path} edge #{index}"
        )

        for required in ("upstream", "downstream", "reason", "source"):
            if required not in edge_raw:
                raise ValueError(
                    f"dependency overlay {overlay_path}: edge #{index} "
                    f"missing required key {required!r}"
                )

        upstream_raw = edge_raw["upstream"]
        downstream_raw = edge_raw["downstream"]
        reason = edge_raw["reason"]
        source = edge_raw["source"]

        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(
                f"dependency overlay {overlay_path}: edge #{index} 'reason' "
                f"must be a non-empty string"
            )
        if not isinstance(source, str) or not source.strip():
            raise ValueError(
                f"dependency overlay {overlay_path}: edge #{index} 'source' "
                f"must be a non-empty string"
            )

        upstream = resolve_claim_id(
            upstream_raw,
            parsed_claims,
            source_hint=f"{overlay_path} edge #{index} upstream",
        )
        downstream = resolve_claim_id(
            downstream_raw,
            parsed_claims,
            source_hint=f"{overlay_path} edge #{index} downstream",
        )

        if upstream == downstream:
            raise ValueError(
                f"dependency overlay {overlay_path}: edge #{index} is a "
                f"self-loop on {upstream!r}"
            )

        resolved.append(
            DependencyEdge(
                upstream=upstream,
                downstream=downstream,
                reason=reason,
                source=source,
            )
        )

    return resolved


def _reject_forbidden_keys(mapping: dict[str, Any], *, context: str) -> None:
    """Raise if ``mapping`` contains any key in :data:`_FORBIDDEN_KEYS`."""

    for key in mapping:
        if key in _FORBIDDEN_KEYS:
            raise ValueError(
                f"{context}: key {key!r} is forbidden. The dependency "
                f"overlay must not redefine claim statuses or confidence "
                f"scores (Req. 2.7)."
            )


# ---------------------------------------------------------------------------
# Self-check entry point
# ---------------------------------------------------------------------------


def _main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    repo_root = Path(__file__).resolve().parent.parent
    claims_path = repo_root / "CLAIMS.md"
    overlay_path = repo_root / "verification" / "dependency_overlay.yaml"

    if not claims_path.exists():
        print(f"[skip] CLAIMS.md not found at {claims_path}", file=sys.stderr)
        return 1
    if not overlay_path.exists():
        print(f"[skip] overlay not found at {overlay_path}", file=sys.stderr)
        return 1

    parsed = parse_claims_md(claims_path)
    edges = load_dependency_overlay(overlay_path, parsed)

    print(f"=== dependency overlay self-check ===")
    print(f"  claims parsed: {len(parsed)}")
    print(f"  edges loaded:  {len(edges)}")
    for edge in edges:
        print(
            f"    {edge.upstream} -> {edge.downstream}"
            f"  (source={edge.source})"
        )
        print(f"      reason: {edge.reason}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
