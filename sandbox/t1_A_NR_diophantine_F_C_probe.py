#!/usr/bin/env python3.12
"""t1_A_NR_diophantine_F_C_probe.py

Probe the Diophantine closure-weight functional candidate for T1 A_NR.

F_C[n_B, n_F] = - |n_B * 1 + n_F * 2 - M|

Under the non-redundancy constraint n_B > 0 and n_F > 0 (the double cover
has two sheets; a complete rotational medium must realize both loop classes),
M = 3 selects the unique pair (n_B, n_F) = (1, 1).

The fermionic class has topological weight 2; the bosonic class has weight 1.
The realized pair is therefore (fermion weight, boson weight) = (2, 1).
"""
from __future__ import annotations

import sys


def F_C(n_B: int, n_F: int, M: int) -> float:
    """Closure-weight deficit functional."""
    return -abs(n_B * 1 + n_F * 2 - M)


def main() -> int:
    M = 3
    max_n = 4

    print(f"T1 A_NR Diophantine F_C probe (M = {M})")
    print("=" * 60)
    print(f"F_C[n_B, n_F] = - |n_B*1 + n_F*2 - {M}|\n")
    print(f"{'n_B':>4s}  {'n_F':>4s}  {'n_B + 2*n_F':>13s}  {'F_C':>6s}  {'non-redundant?':>15s}  {'selected?':>10s}")

    best_score = -float("inf")
    best_pairs = []

    rows = []
    for n_B in range(max_n + 1):
        for n_F in range(max_n + 1):
            score = F_C(n_B, n_F, M)
            redundant = n_B > 0 and n_F > 0
            rows.append((n_B, n_F, n_B + 2 * n_F, score, redundant))
            if redundant and score > best_score:
                best_score = score
                best_pairs = [(n_B, n_F)]
            elif redundant and score == best_score:
                best_pairs.append((n_B, n_F))

    for n_B, n_F, total, score, redundant in rows:
        selected = (n_B, n_F) in best_pairs
        print(f"{n_B:4d}  {n_F:4d}  {total:13d}  {score:6.1f}  {'yes' if redundant else 'no':>15s}  {'YES' if selected else '':>10s}")

    print("\n" + "=" * 60)
    print(f"Best non-redundant pair(s): {best_pairs} with F_C = {best_score}")

    if best_pairs == [(1, 1)]:
        print("PASS: M = 3 and F_C uniquely select one bosonic (order 1) and one fermionic (order 2) mode.")
        print("Realized topological weights: (fermion=2, boson=1) -> (2,1).")
        return 0
    else:
        print("FAIL or non-unique: F_C did not select (1,1).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
