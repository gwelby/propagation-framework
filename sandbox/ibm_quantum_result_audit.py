#!/usr/bin/env python3
"""
ibm_quantum_result_audit.py
===========================

Minimal audit tool for the overnight IBM chirality/mixing jobs.

It accepts raw counts for the 2-qubit qutrit encoding:
  |00> -> channel 0
  |01> -> channel 1
  |10> -> channel 2
  |11> -> leakage / unused state

Outputs:
- normalized channel probabilities
- leakage
- Shannon entropy over the physical 3-channel sector
- return probability to |00>
- total-variation distance to the expected target distribution

Examples:
  python sandbox/ibm_quantum_result_audit.py --mode chiral --counts '{"00": 8100, "01": 40, "10": 30, "11": 22}'
  python sandbox/ibm_quantum_result_audit.py --mode symmetric --counts '{"00": 2700, "01": 2660, "10": 2725, "11": 107}'
"""

from __future__ import annotations

import argparse
import ast
import json
import math
from pathlib import Path


PHYSICAL_STATES = ("00", "01", "10")
LEAK_STATE = "11"


def parse_counts(text: str) -> dict[str, int]:
    text = text.strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = ast.literal_eval(text)
    if not isinstance(data, dict):
        raise ValueError("Counts must parse to a dictionary")
    out: dict[str, int] = {}
    for key, value in data.items():
        out[str(key)] = int(value)
    return out


def shannon_entropy(probabilities: list[float]) -> float:
    return -sum(p * math.log2(p) for p in probabilities if p > 0.0)


def total_variation(p: list[float], q: list[float]) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def classify(mode: str, physical_probs: list[float], leakage: float) -> str:
    if mode == "chiral":
        if physical_probs[0] > 0.9 and leakage < 0.05:
            return "supports chiral identity preservation"
        if physical_probs[0] > physical_probs[1] and physical_probs[0] > physical_probs[2]:
            return "partial support for chiral identity preservation"
        return "does not support chiral identity preservation"

    if mode == "symmetric":
        spread = max(physical_probs) - min(physical_probs)
        if spread < 0.1 and leakage < 0.1:
            return "supports symmetric mixing prediction"
        if spread < 0.2:
            return "partial support for symmetric mixing prediction"
        return "does not support symmetric mixing prediction"

    return "unclassified"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("chiral", "symmetric"), required=True)
    parser.add_argument("--counts", help="Raw counts dict literal or JSON string")
    parser.add_argument("--counts-file", help="Path to file containing raw counts dict/JSON")
    args = parser.parse_args()

    if bool(args.counts) == bool(args.counts_file):
        raise SystemExit("Provide exactly one of --counts or --counts-file")

    if args.counts_file:
        raw = Path(args.counts_file).read_text(encoding="utf-8")
    else:
        raw = args.counts

    counts = parse_counts(raw)
    total = sum(counts.values())
    if total <= 0:
        raise SystemExit("Total counts must be positive")

    physical_counts = [counts.get(state, 0) for state in PHYSICAL_STATES]
    leakage_count = counts.get(LEAK_STATE, 0)
    physical_total = sum(physical_counts)

    probs_all = [value / total for value in physical_counts]
    leakage = leakage_count / total

    if physical_total > 0:
        probs_physical_norm = [value / physical_total for value in physical_counts]
    else:
        probs_physical_norm = [0.0, 0.0, 0.0]

    expected = {
        "chiral": [1.0, 0.0, 0.0],
        "symmetric": [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0],
    }[args.mode]

    entropy = shannon_entropy(probs_physical_norm)
    tv = total_variation(probs_physical_norm, expected)
    verdict = classify(args.mode, probs_all, leakage)

    print("=" * 72)
    print(f"IBM QUANTUM RESULT AUDIT — {args.mode.upper()}")
    print("=" * 72)
    print(f"Total shots: {total}")
    print(f"Counts: {counts}")
    print()
    print("Physical-sector probabilities (of all shots):")
    for state, prob in zip(PHYSICAL_STATES, probs_all):
        print(f"  P({state}) = {prob:.6f}")
    print(f"  Leakage P(11) = {leakage:.6f}")
    print()
    print("Physical-sector probabilities (renormalized over 00/01/10):")
    for state, prob in zip(PHYSICAL_STATES, probs_physical_norm):
        print(f"  P({state} | physical) = {prob:.6f}")
    print()
    print(f"Return probability to |00>: {probs_all[0]:.6f}")
    print(f"Entropy H(physical): {entropy:.6f} bits")
    print(f"TV distance to expected {args.mode} target: {tv:.6f}")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    main()
