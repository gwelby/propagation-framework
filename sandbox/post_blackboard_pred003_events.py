#!/usr/bin/env python3
"""One-off helper to post multi-angle PRED-003 no-go/conditional events to the Blackboard.

The canonical CLI (blackboard_claim.py) supports WORKING/CLOSE/BLOCKED/DISPATCH but
not generic STATE/AUDIT events. This script uses the /event endpoint directly.
"""

import json
import urllib.request
import urllib.error
import datetime


def post_event(payload: dict) -> None:
    payload.setdefault("ts", datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"))
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:18005/event",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(json.dumps(json.loads(resp.read().decode()), indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}")
        print(f"Payload was: {data.decode()}")
        raise


def main() -> None:
    events = [
        {
            "agent": "Devin-RouteA",
            "event_type": "AUDIT",
            "claim": "PRED-003 Route A NO-GO: God Equation scale bridge cannot produce r_nu",
            "confidence": 0.95,
            "refs": [
                "/mnt/d/Fundamentals/PREDICTIONS/PRED-003-route-A-probe.md",
                "/mnt/d/Fundamentals/sandbox/pred003_route_A_toy.py",
            ],
            "content": "Single residue -1/8 cannot serve two splittings. lambda_c top-Compton scale is 1e24-1e25 too small. Full 1,-1/8,-1/8 spectrum gives r_nu=0.",
            "priority": "normal",
            "thread": "pred003-multi-angle",
            "status": "watch",
        },
        {
            "agent": "Devin-RouteB",
            "event_type": "AUDIT",
            "claim": "PRED-003 Route B CONDITIONAL/FIT: Koide ansatz can match r_nu but no PF anchor selects the point",
            "confidence": 0.82,
            "refs": [
                "/mnt/d/Fundamentals/PREDICTIONS/PRED-003-route-B-probe.md",
                "/mnt/d/Fundamentals/sandbox/pred003_route_B_toy.py",
            ],
            "content": "2146 (beta,delta) points within 3 sigma of 0.02951. Charged-lepton Q=2/3 and PF delta=2/9 anchors miss by 20-26 sigma. Best fit at beta=1.154, delta=0.398 rad is unprincipled.",
            "priority": "normal",
            "thread": "pred003-multi-angle",
            "status": "watch",
        },
        {
            "agent": "Devin-RouteD",
            "event_type": "AUDIT",
            "claim": "PRED-003 Route D NO-GO: D=3/N=3 fixes cardinality and degenerate residue, not mass-squared splitting",
            "confidence": 0.95,
            "refs": [
                "/mnt/d/Fundamentals/PREDICTIONS/PRED-003-route-D-probe.md",
                "/mnt/d/Fundamentals/derivations/god_eq_q_sector_basis_selection_2026-04-02.md",
            ],
            "content": "Q-sector degeneracy protected by C3 symmetry. Toy perturbation magnitude rho=0.0588 (47 pct of 1/8) required for target; no PF rule selects it.",
            "priority": "normal",
            "thread": "pred003-multi-angle",
            "status": "watch",
        },
        {
            "agent": "Devin-RouteU",
            "event_type": "AUDIT",
            "claim": "PRED-003 Route U: UGP 0.02936 is a valid external benchmark, not derivable in PF",
            "confidence": 0.85,
            "refs": [
                "/mnt/d/Fundamentals/PREDICTIONS/PRED-003-ugp-reverse.md",
                "/tmp/neutrino_masses_from_braid_atlas.pdf",
            ],
            "content": "UGP formula r = (11^(58/9) - 5^(58/9)) / (19^(58/9) - 5^(58/9)) = 0.02936 verified. PF lacks Braid-Atlas, GF(7)/GTE, Froggatt-Nielsen, and GUT-representation substrate. PF has no competing native number.",
            "priority": "normal",
            "thread": "pred003-multi-angle",
            "status": "watch",
        },
        {
            "agent": "Devin",
            "event_type": "STATE",
            "claim": "PRED-003 multi-angle sweep: A/C/D no-go, B conditional/fit, U external benchmark",
            "confidence": 0.88,
            "refs": ["/mnt/d/Fundamentals/PREDICTIONS/PRED-003-neutrino-mass-squared-ratio.md"],
            "content": "Five routes converge on missing mass-squared-difference generator, flavor/PMNS bridge, scale/closure, and degeneracy-breaking rule. PRED-003 remains NOT YET BUILT.",
            "priority": "normal",
            "thread": "pred003-multi-angle",
            "status": "open",
        },
    ]

    for ev in events:
        post_event(ev)


if __name__ == "__main__":
    main()
