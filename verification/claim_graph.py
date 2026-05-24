"""Claim graph builder for the Propagation Framework verification harness.

The :class:`ClaimGraph` packages together:

    * the parsed CLAIMS.md rows (from :mod:`verification.claim_parser`),
    * the optional explicit dependency overlay
      (from :mod:`verification.dependency_overlay`),
    * the optional support manifest
      (from :mod:`verification.support_manifest`),

and exposes a small, read-only API the rest of the harness uses to walk
the graph (topological order, upstream / downstream, cascade impact) and
to surface structural problems (``validate()``).

The graph is never a second scoreboard. ``claims`` is a structured view
of CLAIMS.md; statuses and confidence scores come from the board and are
never mutated here.

Run ``python -m verification.claim_graph`` as a self-check; the
``__main__`` block builds the graph from the real workspace files and
prints counts, topological order, validation findings, and cascade
impact for a couple of anchor claims.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 2 (graph construction), Req. 7 (cascade impact), Req. 11
  (validation).
"""

from __future__ import annotations

import logging
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path

from verification.claim_parser import CONFIDENCE_RANGES, parse_claims_md
from verification.dependency_overlay import load_dependency_overlay
from verification.models import Claim, ClaimStatus, DependencyEdge
from verification.support_manifest import load_support_manifest


logger = logging.getLogger(__name__)


# Patterns we treat as "this edge references a no-go-style justification"
# in the reason string. This is the conservative scaffold for Req. 6.2 /
# Req. 11.6 — the full no-go library enforcement lives in the guardrails
# module (Section 5/6 of the spec). The patterns below are a defensive
# check: if an overlay edge's reason text itself advertises a no-go or a
# failed approach, it cannot legitimately serve as positive support.
_NO_GO_REASON_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bno[-_\s]?go\b", re.IGNORECASE),
    re.compile(r"\brejected as\b", re.IGNORECASE),
    re.compile(r"\bfailed approach\b", re.IGNORECASE),
)


@dataclass
class ClaimGraph:
    """Structured view of CLAIMS.md plus explicit dependency edges."""

    claims: dict[str, Claim]
    dependency_edges: list[DependencyEdge] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_markdown(
        cls,
        claims_md_path: str | Path,
        dependency_overlay_path: str | Path | None = None,
        support_manifest_path: str | Path | None = None,
    ) -> "ClaimGraph":
        """Parse CLAIMS.md and optionally attach overlay + manifest.

        The manifest is loaded first so its entries can seed the parser's
        ``audited_derivation_refs`` field. The overlay is loaded last so
        it sees the final claim id set.

        Args:
            claims_md_path: Path to the live CLAIMS.md scoreboard.
            dependency_overlay_path: Optional path to the overlay YAML.
            support_manifest_path: Optional path to the manifest YAML.

        Raises:
            ValueError: propagated from the loaders on BLOCK-level
                errors (unresolvable ids, missing files, forbidden keys).
        """

        # Parse once without a manifest to obtain the full set of ids,
        # then feed that through the manifest loader's id resolver, and
        # finally re-parse so the manifest populates
        # ``audited_derivation_refs``.
        initial_claims = parse_claims_md(claims_md_path)

        manifest: dict | None = None
        if support_manifest_path is not None:
            manifest = load_support_manifest(
                support_manifest_path, initial_claims
            )

        if manifest:
            claims = parse_claims_md(
                claims_md_path, support_manifest=manifest
            )
        else:
            claims = initial_claims

        edges: list[DependencyEdge] = []
        if dependency_overlay_path is not None:
            edges = load_dependency_overlay(dependency_overlay_path, claims)

        return cls(claims=claims, dependency_edges=edges)

    # ------------------------------------------------------------------
    # Graph queries
    # ------------------------------------------------------------------

    def topological_order(self) -> list[str]:
        """Return a topological order over the explicit dependency edges.

        Uses Kahn's algorithm. Claims that participate in no edges are
        included in the result; their relative order follows the
        iteration order of ``self.claims`` so the output is deterministic
        for a given input dict.

        Raises:
            ValueError: when the dependency graph contains a cycle. The
                exception message enumerates the claim ids that could
                not be linearized.
        """

        adjacency: dict[str, list[str]] = defaultdict(list)
        indegree: dict[str, int] = {cid: 0 for cid in self.claims}

        for edge in self.dependency_edges:
            if edge.upstream not in self.claims or edge.downstream not in self.claims:
                # Defensive: the loader should have caught this, but we
                # never want to crash inside Kahn's for a missing key.
                continue
            adjacency[edge.upstream].append(edge.downstream)
            indegree[edge.downstream] += 1

        queue: deque[str] = deque(
            cid for cid in self.claims if indegree[cid] == 0
        )
        ordered: list[str] = []
        while queue:
            current = queue.popleft()
            ordered.append(current)
            for neighbour in adjacency[current]:
                indegree[neighbour] -= 1
                if indegree[neighbour] == 0:
                    queue.append(neighbour)

        if len(ordered) != len(self.claims):
            stuck = sorted(
                cid for cid in self.claims if cid not in ordered
            )
            raise ValueError(
                f"dependency graph has a cycle; could not linearize: {stuck}"
            )
        return ordered

    def get_tier(self, status: ClaimStatus) -> list[Claim]:
        """Return all claims currently at ``status``.

        The relative order follows the iteration order of ``self.claims``.
        """

        return [claim for claim in self.claims.values() if claim.status == status]

    def upstream_of(self, claim_id: str) -> list[str]:
        """Direct explicit upstream ids for ``claim_id`` (no transitive)."""

        return [
            edge.upstream
            for edge in self.dependency_edges
            if edge.downstream == claim_id
        ]

    def downstream_of(self, claim_id: str) -> list[str]:
        """Direct explicit downstream ids for ``claim_id`` (no transitive)."""

        return [
            edge.downstream
            for edge in self.dependency_edges
            if edge.upstream == claim_id
        ]

    def cascade_impact(self, claim_id: str) -> list[str]:
        """Transitive closure of explicit downstream edges from ``claim_id``.

        Uses BFS over ``downstream_of``. The starting claim is never
        included in the result. Ids are returned in BFS visitation order
        so the output is deterministic for a given graph.
        """

        if claim_id not in self.claims:
            return []
        visited: set[str] = {claim_id}
        queue: deque[str] = deque([claim_id])
        result: list[str] = []
        while queue:
            current = queue.popleft()
            for neighbour in self.downstream_of(current):
                if neighbour in visited:
                    continue
                visited.add(neighbour)
                result.append(neighbour)
                queue.append(neighbour)
        return result

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[tuple[str, str]]:
        """Return structural findings as a list of ``(severity, message)``.

        Severity is ``"BLOCK"`` or ``"WARN"``. BLOCK-level findings stop
        the verification pipeline; WARN-level findings are advisory.
        Checks performed:

            1. Cycle detection (BLOCK).
            2. Confidence range per tier (WARN); mirrors
               :data:`verification.claim_parser.CONFIDENCE_RANGES`.
            3. Overlay edge id validation (BLOCK, defensive).
            4. Support manifest validation (placeholder; the manifest
               loader is the authoritative check).
            5. CONDITIONAL / PARTIAL_DERIVATION hypothesis presence
               (WARN).
            6. No-go plan scaffold (BLOCK): an overlay edge whose reason
               text uses no-go language cannot be used as positive
               support.
        """

        findings: list[tuple[str, str]] = []

        # 1. Cycle detection.
        try:
            self.topological_order()
        except ValueError as exc:
            findings.append(("BLOCK", f"cycle detection: {exc}"))

        # 2. Confidence range per tier.
        for claim in self.claims.values():
            lo, hi = CONFIDENCE_RANGES.get(claim.status, (0.0, 1.0))
            if not (lo <= claim.confidence <= hi):
                findings.append(
                    (
                        "WARN",
                        f"claim {claim.id!r} ({claim.status.value}) confidence "
                        f"{claim.confidence:.3f} outside stated range "
                        f"[{lo:.2f}, {hi:.2f}]",
                    )
                )

        # 3. Overlay edge id validation (defensive).
        for edge in self.dependency_edges:
            if edge.upstream not in self.claims:
                findings.append(
                    (
                        "BLOCK",
                        f"overlay edge references missing upstream "
                        f"claim {edge.upstream!r}",
                    )
                )
            if edge.downstream not in self.claims:
                findings.append(
                    (
                        "BLOCK",
                        f"overlay edge references missing downstream "
                        f"claim {edge.downstream!r}",
                    )
                )

        # 4. Support manifest validation: authoritative check lives in
        # the loader, which raises BLOCK ValueError at load time. This
        # block is a placeholder so the numbering in the spec lines up.

        # 5. CONDITIONAL / PARTIAL_DERIVATION hypothesis check.
        for claim in self.claims.values():
            if claim.status in (
                ClaimStatus.CONDITIONAL,
                ClaimStatus.PARTIAL_DERIVATION,
            ):
                if not claim.named_hypotheses:
                    findings.append(
                        (
                            "WARN",
                            f"claim {claim.id!r} is {claim.status.value} but "
                            f"no named hypotheses were extracted from its "
                            f"evidence",
                        )
                    )

        # 6. No-go plan scaffold: overlay edges whose reason text uses
        # no-go language cannot serve as positive support.
        for edge in self.dependency_edges:
            reason = edge.reason or ""
            for pattern in _NO_GO_REASON_PATTERNS:
                if pattern.search(reason):
                    findings.append(
                        (
                            "BLOCK",
                            f"overlay edge {edge.upstream!r} -> "
                            f"{edge.downstream!r} cites no-go / failed-"
                            f"approach language as positive support: "
                            f"{reason!r}",
                        )
                    )
                    break

        return findings


# ---------------------------------------------------------------------------
# Self-check entry point
# ---------------------------------------------------------------------------


def _tier_breakdown(claims: dict[str, Claim]) -> dict[ClaimStatus, int]:
    counts: dict[ClaimStatus, int] = defaultdict(int)
    for claim in claims.values():
        counts[claim.status] += 1
    return counts


def _main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    repo_root = Path(__file__).resolve().parent.parent
    claims_path = repo_root / "CLAIMS.md"
    overlay_path = repo_root / "verification" / "dependency_overlay.yaml"
    manifest_path = repo_root / "verification" / "support_manifest.yaml"

    if not claims_path.exists():
        print(f"[skip] CLAIMS.md not found at {claims_path}", file=sys.stderr)
        return 1

    # Try to build the full graph. If the manifest is unresolvable, fall
    # back to overlay-only so the self-check still reports something
    # useful against the live board.
    manifest_status = "loaded"
    try:
        graph = ClaimGraph.from_markdown(
            claims_path,
            dependency_overlay_path=overlay_path if overlay_path.is_file() else None,
            support_manifest_path=manifest_path if manifest_path.is_file() else None,
        )
    except ValueError as exc:
        print(f"[manifest] BLOCK: {exc}")
        manifest_status = "skipped (BLOCK above)"
        graph = ClaimGraph.from_markdown(
            claims_path,
            dependency_overlay_path=overlay_path if overlay_path.is_file() else None,
            support_manifest_path=None,
        )

    print(f"=== claim graph self-check ===")
    print(f"  manifest:   {manifest_status}")
    print(f"  claim count: {len(graph.claims)}")
    print(f"  tier breakdown:")
    for status, count in sorted(
        _tier_breakdown(graph.claims).items(), key=lambda kv: kv[0].value
    ):
        print(f"    {status.value:20s} {count}")

    print(f"  edge count: {len(graph.dependency_edges)}")
    for edge in graph.dependency_edges:
        print(f"    {edge.upstream}  ->  {edge.downstream}")
        print(f"      reason: {edge.reason}")
        print(f"      source: {edge.source}")

    # Topological order.
    print(f"\n=== topological order ===")
    try:
        order = graph.topological_order()
        for idx, cid in enumerate(order):
            print(f"  {idx:2d}. {cid}")
    except ValueError as exc:
        print(f"  ERROR: {exc}")

    # Validation findings.
    print(f"\n=== validation findings ===")
    findings = graph.validate()
    if not findings:
        print("  (no findings)")
    for severity, message in findings:
        print(f"  [{severity}] {message}")

    # Cascade impact for the live "three generations" and the
    # slugified "god equation" row.
    print(f"\n=== cascade impact ===")
    anchors = [
        "three_generations",
        "c_from_l_p_the_god_equation",
        "god_equation",  # short alias; only hits if present
    ]
    for anchor in anchors:
        if anchor not in graph.claims:
            print(f"  {anchor}: (not in claims — skipping)")
            continue
        impact = graph.cascade_impact(anchor)
        print(f"  {anchor} -> {impact}")

    return 0


if __name__ == "__main__":
    sys.exit(_main())
