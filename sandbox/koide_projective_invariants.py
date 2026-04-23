#!/usr/bin/env python3
"""
koide_projective_invariants.py
------------------------------
Bounded audit prompted by Alejandro Rivero's April 20, 2026 clarification:

    "the rational is always tan theta, never theta"

Goal:
1. Derive the natural projective / slope invariant of the Koide square-root
   mass triple.
2. Evaluate it on the charged-lepton data using the repo convention
   k=(tau=0, e=1, mu=2).
3. Compare simple rational approximants for the angle delta itself and for the
   canonical slope tan(delta).

This script does not change CLAIMS.md. It is a geometry audit only.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Iterable

import numpy as np

# PDG 2024 charged leptons, MeV
M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86


def extract_A_delta(m_k0: float, m_k1: float, m_k2: float) -> tuple[float, float]:
    """
    Koide/Rivero/Brannen convention:
        sqrt(m_k) = A * (1 + sqrt(2) * cos(delta + 2*pi*k/3))

    Returns:
        A, delta  with delta in [0, 2*pi)
    """
    s = np.array([math.sqrt(m_k0), math.sqrt(m_k1), math.sqrt(m_k2)], dtype=float)
    A = float(s.mean())
    omega = np.exp(2j * np.pi / 3.0)
    c = s[0] + s[1] * np.conj(omega) + s[2] * np.conj(omega) ** 2
    return A, float(np.angle(c)) % (2.0 * np.pi)


def canonical_projective_coordinates(s0: float, s1: float, s2: float) -> tuple[float, float]:
    """
    For the centered square-root vector z = s - A*(1,1,1), with
        s = (s0, s1, s2),
        A = (s0 + s1 + s2)/3,

    the canonical orthogonal coordinates in the Koide plane are

        X = (2*s0 - s1 - s2)/3
        Y = (s2 - s1)/sqrt(3)

    In the exact Koide parametrization these satisfy

        X = sqrt(2) * A * cos(delta)
        Y = sqrt(2) * A * sin(delta)

    so the canonical projective invariant is Y/X = tan(delta).
    """
    x = (2.0 * s0 - s1 - s2) / 3.0
    y = (s2 - s1) / math.sqrt(3.0)
    return x, y


def best_rationals(x: float, max_denom: int) -> list[tuple[float, int, int, float]]:
    rows: list[tuple[float, int, int, float]] = []
    for q in range(1, max_denom + 1):
        p = round(x * q)
        val = p / q
        err = abs(x - val)
        rows.append((err, p, q, val))
    return sorted(rows)


def print_best(name: str, x: float, max_denom: int = 36, top_n: int = 8) -> None:
    print(f"\nBest rational approximants for {name} with q <= {max_denom}:")
    for err, p, q, val in best_rationals(x, max_denom)[:top_n]:
        rel = err / abs(x) * 100.0 if x else math.inf
        print(f"  {p:>3d}/{q:<2d} = {val:.12f}   err={err:.6e}   rel={rel:.6f}%")


def print_fraction(name: str, x: float, p: int, q: int) -> None:
    val = p / q
    err = abs(x - val)
    rel = err / abs(x) * 100.0 if x else math.inf
    print(f"{name:<18s} target={x:.12f}   {p}/{q}={val:.12f}   err={err:.6e}   rel={rel:.6f}%")


def main() -> None:
    # Repo convention: k=(tau=0, e=1, mu=2)
    s_tau = math.sqrt(M_TAU)
    s_e = math.sqrt(M_E)
    s_mu = math.sqrt(M_MU)

    A, delta = extract_A_delta(M_TAU, M_E, M_MU)
    x, y = canonical_projective_coordinates(s_tau, s_e, s_mu)
    tan_delta = y / x
    edge01 = s_tau - s_e
    edge12 = s_mu - s_e
    edge02 = s_tau - s_mu

    r12_01 = edge12 / edge01
    r12_02 = edge12 / edge02
    r01_02 = edge01 / edge02
    r_edge12_sum = edge12 / (s_tau + s_e + s_mu)
    r_edge20_sum = edge02 / (s_tau + s_e + s_mu)
    r_edge01_sum = edge01 / (s_tau + s_e + s_mu)

    print("=" * 72)
    print("KOIDE PROJECTIVE INVARIANT AUDIT")
    print("=" * 72)
    print("\nCharged-lepton convention: k=(tau=0, e=1, mu=2)")
    print(f"sqrt masses: s_tau={s_tau:.12f}, s_e={s_e:.12f}, s_mu={s_mu:.12f}")
    print(f"A = mean(sqrt masses) = {A:.12f}")

    print("\nCanonical Koide-plane coordinates:")
    print(f"X = (2*s_tau - s_e - s_mu)/3 = {x:.12f}")
    print(f"Y = (s_mu - s_e)/sqrt(3)     = {y:.12f}")

    print("\nExtracted phase:")
    print(f"delta     = {delta:.12f} rad")
    print(f"2/9       = {2/9:.12f} rad")
    print(f"|delta-2/9| = {abs(delta - 2/9):.6e} rad")

    print("\nProjective invariant:")
    print(f"tan(delta) = Y/X = {tan_delta:.12f}")
    print(f"atan(Y/X)  = {math.atan2(y, x):.12f} rad")

    print("\nNatural edge ratios of the square-root triangle:")
    print(f"R12/01 = (s_mu - s_e)/(s_tau - s_e)   = {r12_01:.12f}")
    print(f"R12/02 = (s_mu - s_e)/(s_tau - s_mu)  = {r12_02:.12f}")
    print(f"R01/02 = (s_tau - s_e)/(s_tau - s_mu) = {r01_02:.12f}")
    print(f"edge12/sum = {r_edge12_sum:.12f}")
    print(f"edge20/sum = {r_edge20_sum:.12f}")
    print(f"edge01/sum = {r_edge01_sum:.12f}")

    print("\nExact dependency checks (single projective degree of freedom):")
    print(f"R01/02 - (1 + R12/02) = {r01_02 - (1.0 + r12_02):+.6e}")
    print(f"R12/01 - (R12/02)/(R01/02) = {r12_01 - (r12_02 / r01_02):+.6e}")

    print("\nNamed checks:")
    print_fraction("delta", delta, 2, 9)
    print_fraction("tan(delta)", tan_delta, 2, 9)
    print_fraction("R12/01", r12_01, 3, 13)
    print_fraction("R12/02", r12_02, 3, 10)
    print_fraction("R01/02", r01_02, 13, 10)

    print_best("delta", delta, max_denom=36, top_n=8)
    print_best("tan(delta)", tan_delta, max_denom=36, top_n=8)
    print_best("R12/01", r12_01, max_denom=36, top_n=5)
    print_best("R12/02", r12_02, max_denom=36, top_n=5)
    print_best("R01/02", r01_02, max_denom=36, top_n=5)

    best_delta = best_rationals(delta, 36)[0]
    best_tan = best_rationals(tan_delta, 36)[0]
    best_r12_01 = best_rationals(r12_01, 36)[0]
    best_r12_02 = best_rationals(r12_02, 36)[0]
    best_r01_02 = best_rationals(r01_02, 36)[0]

    print("\nSummary:")
    print(f"  delta best q<=36     -> {best_delta[1]}/{best_delta[2]}  (err={best_delta[0]:.6e})")
    print(f"  tan(delta) best q<=36-> {best_tan[1]}/{best_tan[2]}  (err={best_tan[0]:.6e})")
    print(f"  R12/01 best q<=36    -> {best_r12_01[1]}/{best_r12_01[2]}  (err={best_r12_01[0]:.6e})")
    print(f"  R12/02 best q<=36    -> {best_r12_02[1]}/{best_r12_02[2]}  (err={best_r12_02[0]:.6e})")
    print(f"  R01/02 best q<=36    -> {best_r01_02[1]}/{best_r01_02[2]}  (err={best_r01_02[0]:.6e})")
    print("  Canonical projective invariant is tan(delta), not delta itself.")
    print("  For charged leptons, the naive identification tan(delta) = 2/9 fails.")
    print("  The edge-ratio rationals are cleaner than tan(delta), but they are Möbius")
    print("  transforms of the same single invariant, not independent extra structure.")


if __name__ == "__main__":
    main()
