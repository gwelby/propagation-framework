#!/usr/bin/env python3.12
"""n3_spectrum_controls.py — finite numerical controls for GodEquationSpectrum.lean

Verifies the residue spectrum `cos^3(2πk / N)` for small N.
The module claims:
  - N = 3 is the unique N >= 2 whose ENTIRE residue spectrum (k = 1..N-1) is -1/8.
  - N = 6 is a control: its spectrum contains +1/8, -1/8 and -1.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction


def residue_cubed(n: int, k: int) -> Fraction:
    """Compute cos^3(2πk / N) as an exact Fraction (approx)."""
    if n <= 0 or k <= 0 or k >= n:
        raise ValueError(f"invalid residue mode n={n}, k={k}")
    # Use exact known cosines where possible; otherwise numeric and limit.
    angle = 2 * math.pi * k / n
    c = math.cos(angle)
    # Rational approximation with small denominator for clean values.
    return Fraction(c ** 3).limit_denominator(1000)


def spectrum(n: int) -> list[tuple[int, Fraction]]:
    return [(k, residue_cubed(n, k)) for k in range(1, n)]


def main() -> int:
    tests = [2, 3, 4, 5, 6, 9]
    all_minus_eighth: set[int] = set()
    for n in tests:
        spec = spectrum(n)
        values = [v for _, v in spec]
        is_all_minus_eighth = all(v == Fraction(-1, 8) for v in values)
        print(f"N={n}: k=1..{n-1} -> {[(k, str(v)) for k, v in spec]}")
        print(f"  all residues -1/8: {is_all_minus_eighth}")
        if is_all_minus_eighth:
            all_minus_eighth.add(n)

    print(f"\nN with entire spectrum -1/8: {all_minus_eighth}")
    if all_minus_eighth == {3}:
        print("PASS: N=3 is unique among tested values.")
        return 0
    else:
        print("FAIL: unexpected N with all -1/8 spectrum.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
