"""Example: demonstrate the guardrail enforcer."""
from verification.guardrails import Guardrails


def main():
    g = Guardrails(agents_md_path="AGENTS.md")

    print("Example 1: protected file check")
    for v in g.check_protected_files(["CLAIMS.md", "example.md"]):
        print(f"  [{v.severity}] {v.details}")

    print("\nExample 2: no-go library")
    for v in g.check_no_go("I'll try harmonic series mass ratios again"):
        print(f"  [{v.severity}] {v.details}")

    print("\nExample 3: truth order")
    for v in g.validate_truth_order(
        "Q=2/3 is DERIVED",
        "Monte Carlo shows Q=0.55, contradicts 2/3",
    ):
        print(f"  [{v.severity}] {v.details}")

    print("\nExample 4: score change detection")
    for v in g.validate_no_score_change(
        {"god_equation": 0.88},
        {"god_equation": 0.90},
    ):
        print(f"  [{v.severity}] {v.details}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
