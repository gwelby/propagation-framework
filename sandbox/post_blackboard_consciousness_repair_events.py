"""
Post Blackboard LEAD/DISPATCH/WORKING events for the consciousness metric
multi-angle repair sweep.
"""

import json
import urllib.request
import urllib.error
import datetime


def post_event(payload: dict) -> None:
    payload.setdefault("ts", datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"))
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:18005/event",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8')}")
        print("Payload was:", data.decode("utf-8"))
        raise


def main():
    events = [
        {
            "agent": "Devin",
            "event_type": "LEAD",
            "claim": "Consciousness metric multi-angle repair sweep — 5 routes (A-E) over C_PF instrument",
            "confidence": 0.80,
            "refs": [
                "/mnt/d/Fundamentals/derivations/consciousness_metric_repair_scoping_2026-08-19.md",
                "/mnt/d/Codex/REPORTS/CODEX_20260819_FUNDAMENTALS_CONSCIOUSNESS_HYPOTHESIS_METRIC_AUDIT.md",
            ],
            "content": "Route A equation/implementation parity; Route B CMI estimator repair; Route C hostile controls; Route D prerequisite operationalization; Route E pre-registration/incremental validity. No consciousness detection claim.",
            "priority": "high",
            "thread": "consciousness-metric-repair",
            "status": "open",
        },
        {
            "agent": "Devin-RouteA",
            "event_type": "WORKING",
            "claim": "Route A: C_PF equation/implementation parity — choose one versioned definition and deprecate the other",
            "confidence": 0.80,
            "refs": [
                "/mnt/d/Fundamentals/tools/consciousness_metric/compute_cpf.py",
                "/mnt/d/Fundamentals/tools/consciousness_metric/compute_cpf_bands.py",
                "/mnt/d/Fundamentals/tools/consciousness_metric/cpf/score.py",
                "/mnt/d/Fundamentals/definitions/consciousness_metric_program.md",
            ],
            "content": "Three definitions coexist: spec says C_PF = C_coh * D_int * L_self * F_model; compute_cpf.py uses D_int * C_coh * D_dir_proxy; compute_cpf_bands.py uses D_int * C_coh * (1 + D_dir_proxy). Task is to pick one versioned equation and one production path.",
            "priority": "high",
            "thread": "consciousness-metric-repair",
            "status": "open",
        },
        {
            "agent": "Devin-RouteB",
            "event_type": "WORKING",
            "claim": "Route B: repair the bidirectional conditional-information estimator (R_in and R_out)",
            "confidence": 0.75,
            "refs": [
                "/mnt/d/Fundamentals/tools/consciousness_metric/cpf/directed.py",
                "/mnt/d/Codex/REPORTS/CODEX_20260819_FUNDAMENTALS_CONSCIOUSNESS_HYPOTHESIS_METRIC_AUDIT.md",
            ],
            "content": "Current code uses separate Ledoit-Wolf shrinkage covariances, breaking the CMI algebraic identity and spuriously clipping R_out to 1.0. Class-I null masks the failure. Task: design valid R_in/R_out, add analytic/reference checks, require each leg to pass its own null.",
            "priority": "high",
            "thread": "consciousness-metric-repair",
            "status": "open",
        },
        {
            "agent": "Devin-RouteC",
            "event_type": "WORKING",
            "claim": "Route C: build hostile negative/positive controls for C_PF",
            "confidence": 0.75,
            "refs": [
                "/mnt/d/Fundamentals/tools/consciousness_metric/tests/test_nulls.py",
                "/mnt/d/Fundamentals/tools/consciousness_metric/cpf/nulls.py",
            ],
            "content": "Existing tests cover white noise, collapsed synchrony, and thermostat. Missing: acyclic temporal feed-forward, synchronized no-model/no-loop, time-shifted, phase-randomized, common-driver, and positive closed self-loop controls. Task: add and run them; report false-positive/negative rates.",
            "priority": "high",
            "thread": "consciousness-metric-repair",
            "status": "open",
        },
        {
            "agent": "Devin-RouteD",
            "event_type": "WORKING",
            "claim": "Route D: operationalize the five structural prerequisites or remove untestable ones",
            "confidence": 0.70,
            "refs": [
                "/mnt/d/Fundamentals/definitions/consciousness.md",
                "/mnt/d/Fundamentals/definitions/consciousness_metric_program.md",
                "/mnt/d/Fundamentals/definitions/minimum_substrate.md",
            ],
            "content": "Prerequisites 1 and 2 are redundant; 4 and 5 are not implemented in the metric; thresholds are undefined. Task: reduce to an independent, testable set with clear transfer from definitions to metric; mark hard-problem boundary.",
            "priority": "high",
            "thread": "consciousness-metric-repair",
            "status": "open",
        },
        {
            "agent": "Devin-RouteE",
            "event_type": "WORKING",
            "claim": "Route E: draft real pre-registration and incremental-validity protocol for C_PF",
            "confidence": 0.65,
            "refs": [
                "/mnt/d/Codex/REPORTS/CODEX_20260819_FUNDAMENTALS_CONSCIOUSNESS_HYPOTHESIS_METRIC_AUDIT.md",
            ],
            "content": "Current protocol is an expectation table; T=8000 and threshold 0.08 were selected during calibration. Task: draft pre-registration skeleton binding data, exclusions, estimators, thresholds, statistics, interpretation, held-out replication, and comparators (arousal, complexity, report, task, PCI). Reference protocols: Nature Cogitate 2025, PLOS ONE adversarial-collaboration, Perturbational Complexity Index (PCI).",
            "priority": "high",
            "thread": "consciousness-metric-repair",
            "status": "open",
        },
    ]

    for ev in events:
        post_event(ev)


if __name__ == "__main__":
    main()
