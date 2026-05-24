"""Main verification pipeline orchestrator.

:func:`run_verification_pipeline` is the top-level entry point for the
Propagation Framework verification harness. It wires the claim graph
parser, the per-tier runners, the falsification pipeline, the guardrail
enforcer, and the report generator into a single read-only run that
produces a :class:`verification.report.VerificationReport`.

Key invariants (enforced here by behaviour, not just documentation):

    * ``CLAIMS.md`` is read-only. The pipeline never writes to any
      board document.
    * Confidence scores parsed from ``CLAIMS.md`` are never mutated.
      The results the runners return are stored alongside the
      :class:`Claim` records but do not edit them.
    * BLOCK-level validation findings stop the run before any runner
      executes, so a bad graph never causes speculative work.
    * Long-running sandbox scripts are optionally skipped when
      ``quick=True``; the claim is recorded as ``EXTERNAL_ONLY`` with
      a "skipped: long-running" note in ``details`` so the dashboard
      surfaces the skip rather than burying it.
    * Sandbox scripts are content-hashed. A second run over the same
      script contents reuses the cached :class:`SandboxRunResult` so
      incremental reruns are cheap; edits to the script invalidate
      the cache automatically.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 7 (dependency state summarization), Req. 10 (caching /
  quick mode), plus Req. 1-6 wiring.
- `.kiro/specs/propagation-framework-verification/design.md`
  "Algorithm 1: Bottom-Up Verification Pipeline".
- `.kiro/specs/propagation-framework-verification/tasks.md`
  Tasks 8.1-8.4.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from verification.claim_graph import ClaimGraph
from verification.falsification.pipeline import FalsificationPipeline
from verification.guardrails import Guardrails
from verification.models import (
    Claim,
    ClaimStatus,
    VerificationOutcome,
    VerificationResult,
)
from verification.report import (
    VerificationReport,
    generate_cascade_report,
    generate_dashboard,
    generate_gap_report,
)
from verification.runners.base import get_runner_for_tier
from verification.sandbox_runner import SandboxRunResult


logger = logging.getLogger(__name__)


__all__ = [
    "run_verification_pipeline",
    "summarize_dependency_state",
    "get_script_cache_key",
    "load_cached_result",
    "save_cached_result",
    "DEFAULT_CACHE_DIR",
    "LONG_RUNNING_PATTERNS",
]


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------


# Cache directory for content-hashed sandbox run results. Already
# gitignored (see .gitignore section "Verification harness cache").
DEFAULT_CACHE_DIR: Path = Path(__file__).resolve().parent / ".cache"


# Sandbox scripts whose path contains any of these substrings are
# treated as "long-running" for the purposes of ``quick=True``. The list
# is intentionally conservative — erring toward skipping is safer than
# timing out a quick run.
LONG_RUNNING_PATTERNS: tuple[str, ...] = (
    "monte_carlo",
    "kuramoto_large",
    "z3_product_walk",
    "_mc.py",
)


# Priority order for the dependency-state summariser. Higher number
# wins when multiple upstream signals are present.
_DEPENDENCY_PRIORITY: dict[str, int] = {
    "NOT_DECLARED": 0,
    "CLEAR": 1,
    "OPEN": 2,
    "UNDER_PRESSURE": 3,
}


# ---------------------------------------------------------------------------
# Dependency state summariser (Task 8.2)
# ---------------------------------------------------------------------------


def summarize_dependency_state(
    claim_id: str,
    graph: ClaimGraph,
    results: Iterable[VerificationResult],
) -> str:
    """Return a single string summarising a claim's upstream state.

    The priority order is ``UNDER_PRESSURE > OPEN > CLEAR > NOT_DECLARED``.
    This matters when a row has multiple upstream edges: a single
    pressured upstream is enough to surface the downstream as
    ``UNDER_PRESSURE`` even if every other upstream is clean.

    Rules:

        * ``NOT_DECLARED`` — the claim has no explicit upstream edges
          in the overlay. Nothing to summarize.
        * ``CLEAR`` — every explicit upstream has a matching result
          with outcome ``REPRODUCED`` or ``REGRESSION_OK``.
        * ``OPEN`` — any explicit upstream has outcome
          ``HYPOTHESIS_OPEN``.
        * ``UNDER_PRESSURE`` — any explicit upstream has outcome
          ``UNDER_PRESSURE``.

    Upstream claims that have no matching result yet (the pipeline
    hasn't gotten to them, or they were skipped) do not vote
    ``CLEAR``. They leave the summary at its prior state so we never
    launder a missing upstream into a green downstream.

    Args:
        claim_id: Claim id whose upstream should be summarised.
        graph: The parsed claim graph.
        results: Any iterable of :class:`VerificationResult`. The
            summariser only reads ``claim_id`` and ``outcome``.
    """

    upstreams = graph.upstream_of(claim_id)
    if not upstreams:
        return "NOT_DECLARED"

    result_by_id: dict[str, VerificationResult] = {
        r.claim_id: r for r in results
    }

    # Two independent signals we track as we walk the upstream set:
    #   * ``highest`` — the highest-priority explicit pressure signal
    #     we've seen (UNDER_PRESSURE > OPEN). Stays at "" when no
    #     upstream has voted pressure or open.
    #   * ``all_clear`` — true iff every upstream has a result whose
    #     outcome is REPRODUCED or REGRESSION_OK. A missing result, or
    #     a SCRIPT_BROKEN / EXTERNAL_ONLY outcome, flips this to
    #     False because it means we cannot honestly claim CLEAR for
    #     the downstream row.
    highest: str = ""
    highest_priority = 0
    all_clear = True

    def _promote(candidate: str) -> None:
        nonlocal highest, highest_priority
        priority = _DEPENDENCY_PRIORITY[candidate]
        if priority > highest_priority:
            highest = candidate
            highest_priority = priority

    for up in upstreams:
        r = result_by_id.get(up)
        if r is None:
            # No result for this upstream yet. We cannot vote CLEAR
            # on its behalf.
            all_clear = False
            continue
        if r.outcome is VerificationOutcome.UNDER_PRESSURE:
            all_clear = False
            _promote("UNDER_PRESSURE")
        elif r.outcome is VerificationOutcome.HYPOTHESIS_OPEN:
            all_clear = False
            _promote("OPEN")
        elif r.outcome in (
            VerificationOutcome.REPRODUCED,
            VerificationOutcome.REGRESSION_OK,
        ):
            # CLEAR-worthy contribution; do not disturb ``all_clear``.
            pass
        else:
            # SCRIPT_BROKEN / EXTERNAL_ONLY — cannot claim CLEAR and
            # is not an explicit OPEN / UNDER_PRESSURE signal either.
            # Fall back to OPEN so the downstream is not silently
            # laundered to green.
            all_clear = False
            _promote("OPEN")

    if highest:
        return highest
    if all_clear:
        return "CLEAR"
    return "OPEN"


# ---------------------------------------------------------------------------
# Content-hash caching (Task 8.3)
# ---------------------------------------------------------------------------


def get_script_cache_key(script_path: str | Path) -> str:
    """Return a SHA-256 content hash of ``script_path``.

    The returned string is a hex digest suitable for use as a cache
    filename. If the file does not exist, a sentinel ``"missing:..."``
    key is returned so callers can still identify the absence.
    """

    path = Path(script_path)
    if not path.is_file():
        # Include the path text so two missing scripts hash to different
        # sentinel keys.
        return "missing:" + hashlib.sha256(str(path).encode("utf-8")).hexdigest()

    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _cache_file(cache_key: str, cache_dir: Path | None) -> Path:
    target_dir = cache_dir or DEFAULT_CACHE_DIR
    return target_dir / f"{cache_key}.json"


def load_cached_result(
    cache_key: str,
    cache_dir: Path | None = None,
) -> SandboxRunResult | None:
    """Return a previously cached :class:`SandboxRunResult`, or None.

    The cache is JSON on disk, keyed by the script's content hash.
    Missing cache files and malformed cache contents both return
    ``None`` so callers always get a safe fallback.
    """

    path = _cache_file(cache_key, cache_dir)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.info("load_cached_result: %s unreadable (%s); ignoring", path, exc)
        return None
    if not isinstance(data, dict):
        return None

    try:
        return SandboxRunResult(
            script_path=str(data.get("script_path", "")),
            success=bool(data.get("success", False)),
            stdout=str(data.get("stdout", "")),
            stderr=str(data.get("stderr", "")),
            return_code=int(data.get("return_code", -1)),
            error=str(data.get("error", "")),
            parsed_output=dict(data.get("parsed_output") or {}),
        )
    except (TypeError, ValueError) as exc:
        logger.info(
            "load_cached_result: %s not a valid SandboxRunResult (%s); ignoring",
            path,
            exc,
        )
        return None


def save_cached_result(
    cache_key: str,
    result: SandboxRunResult,
    cache_dir: Path | None = None,
) -> None:
    """Persist ``result`` to ``{cache_dir}/{cache_key}.json``.

    Silently creates the cache directory if it does not exist.
    Serialization failures are logged but not raised — the cache is
    an optimisation, never a correctness requirement.
    """

    target_dir = cache_dir or DEFAULT_CACHE_DIR
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.info("save_cached_result: could not create %s (%s)", target_dir, exc)
        return

    path = target_dir / f"{cache_key}.json"
    payload = dataclasses.asdict(result)
    try:
        path.write_text(
            json.dumps(payload, sort_keys=True, default=_json_default),
            encoding="utf-8",
        )
    except OSError as exc:
        logger.info("save_cached_result: could not write %s (%s)", path, exc)


def _json_default(obj: Any) -> Any:
    """JSON default encoder for objects the cache may encounter."""

    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"object of type {type(obj).__name__} is not JSON serialisable")


# ---------------------------------------------------------------------------
# Helpers for the main pipeline
# ---------------------------------------------------------------------------


def _is_long_running(script_path: str) -> bool:
    """Heuristic: does ``script_path`` look like a long-running sandbox script?

    Returns True when any of :data:`LONG_RUNNING_PATTERNS` appears in
    the path. Case-insensitive so ``Monte_Carlo_foo.py`` still matches.
    """

    lowered = script_path.lower()
    return any(pat in lowered for pat in LONG_RUNNING_PATTERNS)


def _skipped_result(claim: Claim, dependency_state: str) -> VerificationResult:
    """Build an EXTERNAL_ONLY skip result for a long-running row in quick mode."""

    return VerificationResult(
        claim_id=claim.id,
        outcome=VerificationOutcome.EXTERNAL_ONLY,
        dependency_state=dependency_state,
        error_margin=None,
        details=(
            "skipped: long-running sandbox script(s) not executed in "
            "quick mode. Re-run without --quick to verify this row."
        ),
        scripts_run=[],
        derivation_refs_checked=list(claim.audited_derivation_refs or []),
        gaps_found=list(claim.known_gaps or []),
    )


def _aggregate_gaps(results: list[VerificationResult]) -> list[str]:
    """Flatten every ``gaps_found`` list into a deduped ``claim_id:`` list."""

    aggregated: list[str] = []
    seen: set[str] = set()
    for r in results:
        for gap in r.gaps_found:
            entry = f"{r.claim_id}: {gap}".strip()
            if entry not in seen:
                seen.add(entry)
                aggregated.append(entry)
    return aggregated


def _build_cascade_map(graph: ClaimGraph) -> dict[str, list[str]]:
    """Per-claim transitive downstream map, omitting empty cascades."""

    cascade: dict[str, list[str]] = {}
    for cid in graph.claims:
        downstream = graph.cascade_impact(cid)
        if downstream:
            cascade[cid] = downstream
    return cascade


# ---------------------------------------------------------------------------
# Main entry point (Task 8.1)
# ---------------------------------------------------------------------------


def run_verification_pipeline(
    claims_md_path: str | Path,
    dependency_overlay: str | Path | None = None,
    support_manifest: str | Path | None = None,
    agents_md_path: str | Path | None = None,
    quick: bool = False,
    seed: int | None = None,
) -> VerificationReport:
    """End-to-end verification run.

    Execution order:

        1. Parse ``CLAIMS.md`` via :meth:`ClaimGraph.from_markdown`.
        2. Instantiate :class:`Guardrails` against ``AGENTS.md`` so the
           no-go library is loaded. (The enforcer is not called here in
           blocking mode; its role at this layer is to be available to
           runners and the report layer. Protected-file checks run
           against the pipeline's own write set — which is empty.)
        3. Run ``graph.validate()``. BLOCK findings raise :class:`ValueError`
           so the pipeline does not do any speculative work on a bad graph.
        4. Compute topological order.
        5. For each claim in order, summarise dependency state, pick
           the tier-appropriate runner, and run it. Long-running
           scripts are skipped when ``quick=True``.
        6. Run the falsification pipeline (local + external watch).
        7. Wrap results, falsification, aggregated gaps, and the
           per-claim cascade into a :class:`VerificationReport`.

    The function never writes to any board document and never mutates
    the parsed :class:`Claim` records.

    Args:
        claims_md_path: Path to ``CLAIMS.md``.
        dependency_overlay: Optional path to the YAML dependency overlay.
        support_manifest: Optional path to the YAML support manifest.
        agents_md_path: Optional path to ``AGENTS.md`` so the
            guardrail enforcer can parse the no-go library. When
            omitted, the hardcoded fallback library is used.
        quick: When True, skip sandbox scripts matching
            :data:`LONG_RUNNING_PATTERNS`.
        seed: Optional integer seed forwarded to every runner and the
            falsification pipeline for deterministic runs.

    Returns:
        A :class:`VerificationReport` with one entry per claim plus the
        five falsification records.

    Raises:
        ValueError: if ``graph.validate()`` reports BLOCK-level issues.
            The message enumerates the blocking findings.
    """

    now = datetime.now(timezone.utc)
    logger.info("run_verification_pipeline: starting at %s", now.isoformat())

    # --- Step 1: parse the claim graph ---
    graph = ClaimGraph.from_markdown(
        claims_md_path,
        dependency_overlay_path=dependency_overlay,
        support_manifest_path=support_manifest,
    )

    # --- Step 2: guardrails (no-go library etc.) ---
    # We construct Guardrails so the no-go library loads and is
    # available to any runner that wants it later. The enforcer is
    # deliberately not used to mutate anything here.
    _guardrails = Guardrails(agents_md_path=agents_md_path)

    # --- Step 3: validate; BLOCK findings stop the run ---
    findings = graph.validate()
    blocks = [msg for severity, msg in findings if severity == "BLOCK"]
    warns = [msg for severity, msg in findings if severity == "WARN"]
    for msg in warns:
        logger.warning("graph.validate: %s", msg)
    if blocks:
        joined = "; ".join(blocks)
        raise ValueError(
            f"graph.validate() returned {len(blocks)} BLOCK finding(s); "
            f"aborting before any runner: {joined}"
        )

    # --- Step 4: topological order ---
    try:
        ordered = graph.topological_order()
    except ValueError as exc:
        # Should not happen: cycle detection is already in validate().
        raise ValueError(f"topological_order failed after validate: {exc}") from exc

    # --- Step 5: per-claim verification ---
    results: list[VerificationResult] = []
    for claim_id in ordered:
        claim = graph.claims[claim_id]
        dep_state = summarize_dependency_state(claim_id, graph, results)

        # Quick mode: skip rows whose only declared scripts are
        # long-running. A row with a mix of short + long scripts still
        # runs — we only trim the long ones by passing a filtered clone
        # to the runner.
        if quick and claim.sandbox_scripts:
            long_running = [
                s for s in claim.sandbox_scripts if _is_long_running(s)
            ]
            if long_running and len(long_running) == len(claim.sandbox_scripts):
                logger.info(
                    "quick mode: skipping all %d long-running script(s) for %s",
                    len(long_running),
                    claim_id,
                )
                results.append(_skipped_result(claim, dep_state))
                continue
            if long_running:
                filtered = [
                    s for s in claim.sandbox_scripts if not _is_long_running(s)
                ]
                logger.info(
                    "quick mode: dropping %d long-running script(s) from %s; "
                    "running %d remaining",
                    len(long_running),
                    claim_id,
                    len(filtered),
                )
                claim = dataclasses.replace(claim, sandbox_scripts=filtered)

        runner = get_runner_for_tier(claim.status)
        # Not every runner exposes ``seed`` as an attribute (base class
        # is abstract), but the concrete runners do. Setting the attr
        # defensively keeps the API simple without a per-tier switch.
        if seed is not None:
            try:
                runner.seed = seed  # type: ignore[attr-defined]
            except Exception:  # pragma: no cover - defensive
                pass
        try:
            result = runner.verify(claim, dependency_state=dep_state)
        except Exception as exc:
            logger.exception(
                "runner for claim %s raised %s; recording SCRIPT_BROKEN",
                claim_id,
                exc,
            )
            result = VerificationResult(
                claim_id=claim.id,
                outcome=VerificationOutcome.SCRIPT_BROKEN,
                dependency_state=dep_state,
                error_margin=None,
                details=f"runner raised {type(exc).__name__}: {exc}",
                scripts_run=list(claim.sandbox_scripts or []),
                derivation_refs_checked=list(claim.audited_derivation_refs or []),
                gaps_found=list(claim.known_gaps or []),
            )
        results.append(result)

    # --- Step 6: falsification pipeline ---
    fpipe = FalsificationPipeline()
    falsification = fpipe.run_all(seed=seed)

    # --- Step 7: build the report ---
    report = VerificationReport(
        claims=results,
        falsification=falsification,
        gaps=_aggregate_gaps(results),
        cascade=_build_cascade_map(graph),
        timestamp=now,
    )
    logger.info(
        "run_verification_pipeline: finished with %d claim result(s) and "
        "%d falsification record(s)",
        len(report.claims),
        len(report.falsification),
    )
    return report


# ---------------------------------------------------------------------------
# Dashboard convenience rendering
# ---------------------------------------------------------------------------


def render_reports(
    graph: ClaimGraph,
    report: VerificationReport,
) -> dict[str, str]:
    """Render the three standard markdown artifacts for a report.

    Small convenience used by the CLI example and integration tests;
    not part of the required task surface. Kept here so the report
    generator does not need to import the pipeline module.
    """

    return {
        "dashboard": generate_dashboard(graph, report.claims, report.falsification),
        "gaps": generate_gap_report(report.claims),
        "cascade": generate_cascade_report(graph, report.claims),
    }


# ---------------------------------------------------------------------------
# CLI entry point (Task 11.2 — quick mode)
# ---------------------------------------------------------------------------


def _main(argv: list[str] | None = None) -> int:
    """CLI entry point: run the pipeline and print the dashboard.

    Flags:
        --claims      Path to the live CLAIMS.md scoreboard.
                      Default: CLAIMS.md.
        --overlay     Optional YAML dependency overlay.
                      Default: verification/dependency_overlay.yaml.
        --manifest    Optional YAML support manifest.
                      Default: verification/support_manifest.yaml.
        --agents      Path to AGENTS.md for the no-go library.
                      Default: AGENTS.md.
        --quick       Skip long-running sandbox scripts. A script is
                      treated as long-running when its path contains any
                      of: ``monte_carlo``, ``kuramoto_large``,
                      ``z3_product_walk``, or ``_mc.py``. Claims whose
                      only declared scripts match these patterns are
                      recorded as EXTERNAL_ONLY with a "skipped:
                      long-running" note. Quick mode still runs all
                      other scripts and all falsification tests.
        --seed        Optional integer seed forwarded to every runner
                      and the falsification pipeline for deterministic
                      runs.

    Exit codes:
        0 on a successful run (report generated, dashboard printed).
        2 on BLOCK-level validation findings (graph cycle, missing
          claim id, etc.).

    This CLI never writes to any board document. It only prints the
    dashboard to stdout.
    """

    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m verification.pipeline",
        description=(
            "Propagation Framework verification pipeline. Parses "
            "CLAIMS.md, runs tier-appropriate runners and the "
            "falsification pipeline, and prints a markdown dashboard to "
            "stdout. Never modifies board documents, never changes "
            "confidence scores."
        ),
    )
    parser.add_argument(
        "--claims",
        default="CLAIMS.md",
        help="Path to CLAIMS.md (default: CLAIMS.md).",
    )
    parser.add_argument(
        "--overlay",
        default="verification/dependency_overlay.yaml",
        help=(
            "Path to the YAML dependency overlay (default: "
            "verification/dependency_overlay.yaml). Pass an empty "
            "string to disable."
        ),
    )
    parser.add_argument(
        "--manifest",
        default="verification/support_manifest.yaml",
        help=(
            "Path to the YAML support manifest (default: "
            "verification/support_manifest.yaml). Pass an empty "
            "string to disable."
        ),
    )
    parser.add_argument(
        "--agents",
        default="AGENTS.md",
        help="Path to AGENTS.md for the no-go library (default: AGENTS.md).",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help=(
            "Skip long-running sandbox scripts. A script is treated as "
            "long-running when its path contains any of: 'monte_carlo', "
            "'kuramoto_large', 'z3_product_walk', or '_mc.py'. Quick "
            "mode still runs all other scripts and all falsification "
            "tests."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help=(
            "Optional integer seed forwarded to every runner and the "
            "falsification pipeline for deterministic runs."
        ),
    )

    args = parser.parse_args(argv)

    overlay_arg: str | None = args.overlay if args.overlay else None
    manifest_arg: str | None = args.manifest if args.manifest else None
    agents_arg: str | None = args.agents if args.agents else None

    try:
        report = run_verification_pipeline(
            args.claims,
            dependency_overlay=overlay_arg,
            support_manifest=manifest_arg,
            agents_md_path=agents_arg,
            quick=args.quick,
            seed=args.seed,
        )
    except ValueError as exc:
        # BLOCK-level validation findings surface here.
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2

    graph = ClaimGraph.from_markdown(
        args.claims,
        dependency_overlay_path=overlay_arg,
        support_manifest_path=manifest_arg,
    )
    print(generate_dashboard(graph, report.claims, report.falsification))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
