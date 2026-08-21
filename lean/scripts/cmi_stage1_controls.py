#!/usr/bin/env python3
"""Finite semantic controls for PfLean.ConditionalMutualInformation (Stage 1).

These exact Fraction-valued tables complement the Lean proof.  They do not
formalize probability theory; they test the finite-discrete mass relation
hypothesis and the conditional mutual information formula in two directions:

1. Positive control: when pXYZ(x,y,z) * pZ(z) = pXZ(x,z) * pYZ(y,z) for all
   (x,y,z), the CMI formula vanishes.
2. Negative controls: when the relation fails, the CMI formula is strictly
   positive.

The script exits 0 only if the positive control passes and all negative
controls fail (i.e. CMI > 0 in each non-independent case).
"""

from __future__ import annotations

from fractions import Fraction
from math import log2
from typing import Iterable, TypeVar

T = TypeVar("T")


def plog2(a: Fraction) -> float:
    """a * log2(a) with the convention 0 * log2(0) = 0."""
    if a == 0:
        return 0.0
    return float(a) * log2(float(a))


def entropy(mass: dict[T, Fraction]) -> float:
    """Shannon entropy H in bits, ignoring zero masses."""
    return -sum(plog2(a) for a in mass.values() if a != 0)


def conditional_mutual_information(
    dist: dict[tuple[int, int, int], Fraction]
) -> tuple[float, bool]:
    """Compute CMI(X;Y|Z) and whether the mass relation holds everywhere.

    Returns (cmi, relation_holds).
    """
    pZ: dict[int, Fraction] = {}
    pXZ: dict[tuple[int, int], Fraction] = {}
    pYZ: dict[tuple[int, int], Fraction] = {}
    pXYZ: dict[tuple[int, int, int], Fraction] = {}

    for (x, y, z), m in dist.items():
        pZ[z] = pZ.get(z, Fraction(0)) + m
        pXZ[(x, z)] = pXZ.get((x, z), Fraction(0)) + m
        pYZ[(y, z)] = pYZ.get((y, z), Fraction(0)) + m
        pXYZ[(x, y, z)] = pXYZ.get((x, y, z), Fraction(0)) + m

    # Fill in any missing triples with zero mass for the relation test.
    all_x = sorted({x for (x, _, _) in dist})
    all_y = sorted({y for (_, y, _) in dist})
    all_z = sorted({z for (_, _, z) in dist})

    relation_holds = True
    for x in all_x:
        for y in all_y:
            for z in all_z:
                xyz = pXYZ.get((x, y, z), Fraction(0))
                z_mass = pZ.get(z, Fraction(0))
                xz = pXZ.get((x, z), Fraction(0))
                yz = pYZ.get((y, z), Fraction(0))
                if xyz * z_mass != xz * yz:
                    relation_holds = False

    cond_entropy_x = Fraction(0)
    cond_entropy_y = Fraction(0)
    cond_entropy_xy = Fraction(0)

    for z, z_mass in pZ.items():
        if z_mass == 0:
            continue
        cond_x = {x: pXZ.get((x, z), Fraction(0)) / z_mass for x in all_x}
        cond_y = {y: pYZ.get((y, z), Fraction(0)) / z_mass for y in all_y}
        cond_xy = {
            (x, y): pXYZ.get((x, y, z), Fraction(0)) / z_mass
            for x in all_x
            for y in all_y
        }

        cond_entropy_x += z_mass * Fraction(entropy(cond_x)).limit_denominator(10**12)
        cond_entropy_y += z_mass * Fraction(entropy(cond_y)).limit_denominator(10**12)
        cond_entropy_xy += z_mass * Fraction(entropy(cond_xy)).limit_denominator(10**12)

    cmi = float(cond_entropy_x + cond_entropy_y - cond_entropy_xy)
    return cmi, relation_holds


def product_distribution() -> dict[tuple[int, int, int], Fraction]:
    """Positive control: X, Y, Z fully independent."""
    pX = {0: Fraction(1, 2), 1: Fraction(1, 2)}
    pY = {0: Fraction(1, 3), 1: Fraction(2, 3)}
    pZ = {0: Fraction(1, 4), 1: Fraction(3, 4)}
    dist: dict[tuple[int, int, int], Fraction] = {}
    for x, mx in pX.items():
        for y, my in pY.items():
            for z, mz in pZ.items():
                dist[(x, y, z)] = mx * my * mz
    return dist


def conditional_independent_distribution() -> dict[tuple[int, int, int], Fraction]:
    """Positive control: X and Y independent conditional on Z."""
    # pZ
    pZ = {0: Fraction(1, 3), 1: Fraction(2, 3)}
    # conditional pX|z and pY|z
    cond_x = {
        0: {0: Fraction(2, 3), 1: Fraction(1, 3)},
        1: {0: Fraction(1, 4), 1: Fraction(3, 4)},
    }
    cond_y = {
        0: {0: Fraction(1, 5), 1: Fraction(4, 5)},
        1: {0: Fraction(3, 4), 1: Fraction(1, 4)},
    }
    dist: dict[tuple[int, int, int], Fraction] = {}
    for z, mz in pZ.items():
        for x, mx in cond_x[z].items():
            for y, my in cond_y[z].items():
                dist[(x, y, z)] = mz * mx * my
    return dist


def negative_common_cause() -> dict[tuple[int, int, int], Fraction]:
    """Negative control: Z is a common cause but X and Y are coupled within Z."""
    return {
        (0, 0, 0): Fraction(1, 4),
        (0, 1, 0): Fraction(1, 4),
        (1, 0, 0): Fraction(1, 4),
        (1, 1, 1): Fraction(1, 4),
    }


def negative_direct_link() -> dict[tuple[int, int, int], Fraction]:
    """Negative control: X directly influences Y even after conditioning on Z."""
    return {
        (0, 0, 0): Fraction(1, 6),
        (0, 1, 0): Fraction(1, 12),
        (1, 0, 0): Fraction(1, 12),
        (1, 1, 0): Fraction(1, 6),
        (0, 0, 1): Fraction(1, 6),
        (0, 1, 1): Fraction(1, 12),
        (1, 0, 1): Fraction(1, 12),
        (1, 1, 1): Fraction(1, 6),
    }


def main() -> None:
    checks = {
        "positive_full_independence": (product_distribution(), True, 0.0),
        "positive_conditional_independence": (conditional_independent_distribution(), True, 0.0),
        "negative_common_cause": (negative_common_cause(), False, None),
        "negative_direct_link": (negative_direct_link(), False, None),
    }

    all_pass = True
    for name, (dist, expect_relation, expect_cmi) in checks.items():
        cmi, relation = conditional_mutual_information(dist)
        if relation != expect_relation:
            print(f"{name}: FAIL (relation={relation}, expected={expect_relation})")
            all_pass = False
            continue
        if expect_cmi is not None and abs(cmi - expect_cmi) > 1e-12:
            print(f"{name}: FAIL (cmi={cmi}, expected={expect_cmi})")
            all_pass = False
            continue
        if expect_cmi is None and cmi <= 0:
            print(f"{name}: FAIL (cmi={cmi}, expected > 0)")
            all_pass = False
            continue
        print(f"{name}: PASS (cmi={cmi}, relation={relation})")

    if all_pass:
        print("All finite controls passed.")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
