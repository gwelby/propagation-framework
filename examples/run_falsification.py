"""Example: run the falsification pipeline and print the pressure report."""
from verification.falsification.pipeline import FalsificationPipeline


def main():
    pipeline = FalsificationPipeline()
    tests = pipeline.run_all()
    print(pipeline.framework_pressure_report(tests))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
