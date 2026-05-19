"""Example: run the full verification pipeline and print the dashboard."""
from verification.pipeline import run_verification_pipeline
from verification.report import generate_dashboard
from verification.claim_graph import ClaimGraph


def main():
    report = run_verification_pipeline(
        "CLAIMS.md",
        dependency_overlay="verification/dependency_overlay.yaml",
        support_manifest="verification/support_manifest.yaml",
        agents_md_path="AGENTS.md",
        quick=True,
    )
    # The pipeline already parsed the graph; re-parse here for the dashboard.
    graph = ClaimGraph.from_markdown(
        "CLAIMS.md",
        dependency_overlay_path="verification/dependency_overlay.yaml",
        support_manifest_path="verification/support_manifest.yaml",
    )
    print(generate_dashboard(graph, report.claims, report.falsification))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
