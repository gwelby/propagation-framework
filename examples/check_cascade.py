"""Example: show the cascade impact for a specific claim."""
import sys

from verification.claim_graph import ClaimGraph


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "god_equation"
    graph = ClaimGraph.from_markdown(
        "CLAIMS.md",
        dependency_overlay_path="verification/dependency_overlay.yaml",
        support_manifest_path="verification/support_manifest.yaml",
    )
    # Use token-superset resolver to handle short ids too.
    from verification.dependency_overlay import resolve_claim_id

    try:
        resolved = resolve_claim_id(target, graph.claims)
    except ValueError as exc:
        print(f"Could not resolve claim '{target}': {exc}", file=sys.stderr)
        return 1
    cascade = graph.cascade_impact(resolved)
    print(f"Cascade impact for '{resolved}' ({len(cascade)} downstream):")
    for cid in cascade:
        print(f"  - {cid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
