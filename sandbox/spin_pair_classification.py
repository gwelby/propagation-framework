#!/usr/bin/env python3
"""Low-spin classification for the Weinberg spin-pair audit.

Prints raw tables only:
- spin j
- Casimir C2 = j(j+1)
- SU(2) character at the PF Z3 step angle theta = 2pi/3
- survivor / annihilated classification

This script is intentionally non-interpretive. It exists to support the
bounded numerical pass described in ACTIVE_ISSUES.md.
"""

from __future__ import annotations

import math


def chi_at_z3_step(j: float) -> float:
    """Character chi_j(theta) at theta = 2pi/3."""
    theta = 2.0 * math.pi / 3.0
    numerator = math.sin((2.0 * j + 1.0) * theta / 2.0)
    denominator = math.sin(theta / 2.0)
    value = numerator / denominator
    # Clean tiny floating-point noise around 0 and +-1.
    if abs(value) < 1e-12:
        return 0.0
    if abs(value - 1.0) < 1e-12:
        return 1.0
    if abs(value + 1.0) < 1e-12:
        return -1.0
    return value


def fmt_j(j: float) -> str:
    return str(int(j)) if j.is_integer() else str(j)


def main() -> None:
    print("Low-spin classification at theta = 2pi/3")
    print()
    print(f"{'j':>5}  {'C2=j(j+1)':>12}  {'chi_j(2pi/3)':>13}  {'class':>12}")
    print("-" * 50)

    survivors = []
    annihilated = []

    for n in range(17):
        j = n / 2.0
        c2 = j * (j + 1.0)
        chi = chi_at_z3_step(j)
        label = "annihilated" if chi == 0.0 else "survivor"
        row = f"{fmt_j(j):>5}  {c2:12.2f}  {chi:13.1f}  {label:>12}"
        print(row)

        if chi == 0.0:
            annihilated.append(fmt_j(j))
        else:
            survivors.append(fmt_j(j))

    print()
    print("Survivors:", ", ".join(survivors))
    print("Annihilated:", ", ".join(annihilated))


if __name__ == "__main__":
    main()
