"""
Koide phase tolerance scan

Purpose:
1. quantify how far the Chebyshev cubic selector locus is from making the empirical Koide phase
   a stationary point,
2. identify whether a nearby cubic coefficient region can still place a minimum near the empirical
   phase,
3. audit the historical proxy potential V_proxy(delta) = f(delta)^6 * sum_k 1/g_k(delta)^2.

This is a bounded audit tool. It does not derive a selector.
"""

import math
from typing import Iterable

import numpy as np
from scipy.signal import argrelmin


DELTA_EMP = 0.22222963149
DELTA_TWO_NINTHS = 2.0 / 9.0
M_TAU_DELTA_UNCERTAINTY = 2.58e-4


def f(delta: float) -> float:
    return -0.5 + math.cos(3.0 * delta) / math.sqrt(2.0)


def g(delta: float, k: int) -> float:
    return 1.0 + math.sqrt(2.0) * math.cos(delta + 2.0 * math.pi * k / 3.0)


def cubic_value(delta: float, b: float, c: float, d: float) -> float:
    x = f(delta)
    return b * x + c * x * x + d * x * x * x


def cubic_stationary_deltas(b: float, c: float, d: float) -> list[float]:
    vals = [0.0, math.pi / 3.0, 2.0 * math.pi / 3.0]

    if abs(d) < 1e-15:
        roots: Iterable[float] = []
        if abs(c) > 1e-15:
            roots = [-b / (2.0 * c)]
    else:
        disc = 4.0 * c * c - 12.0 * d * b
        roots = []
        if disc >= -1e-12:
            disc = max(disc, 0.0)
            s = math.sqrt(disc)
            roots = [(-2.0 * c + s) / (6.0 * d), (-2.0 * c - s) / (6.0 * d)]

    for root in roots:
        x = (root + 0.5) * math.sqrt(2.0)
        if -1.0 - 1e-12 <= x <= 1.0 + 1e-12:
            x = min(1.0, max(-1.0, x))
            angle = math.acos(x)
            for theta in (angle, 2.0 * math.pi - angle):
                delta = theta / 3.0
                if 0.0 <= delta <= 2.0 * math.pi / 3.0:
                    vals.append(delta)

    return sorted(set(round(v, 12) for v in vals))


def cubic_global_minimum(b: float, c: float, d: float) -> tuple[float, float]:
    pts = cubic_stationary_deltas(b, c, d)
    scored = [(cubic_value(p, b, c, d), p) for p in pts]
    return min(scored)


def proxy_value(delta: float) -> float:
    ff = f(delta) ** 6
    s = 0.0
    for k in (1, 2, 3):
        gk = g(delta, k)
        if abs(gk) < 1e-12:
            return 0.0
        s += 1.0 / (gk * gk)
    return ff * s


def main() -> None:
    f_emp = f(DELTA_EMP)
    center = np.array([3.0, 12.0, 8.0])
    target_plane_normal = np.array([1.0, 2.0 * f_emp, 3.0 * f_emp * f_emp])
    plane_eval = float(center @ target_plane_normal)
    plane_dist = abs(plane_eval) / float(np.linalg.norm(target_plane_normal))
    plane_rel = plane_dist / float(np.linalg.norm(center))
    nearest_plane_point = center - plane_eval / float(target_plane_normal @ target_plane_normal) * target_plane_normal

    print("== Empirical target data ==")
    print(f"delta_emp               = {DELTA_EMP:.12f}")
    print(f"2/9                     = {DELTA_TWO_NINTHS:.12f}")
    print(f"|delta_emp - 2/9|       = {abs(DELTA_EMP - DELTA_TWO_NINTHS):.12e}")
    print(f"f(delta_emp)            = {f_emp:.12f}")
    print()

    print("== Target-critical plane for cubic family ==")
    print("Condition for delta_emp to be an interior stationary point:")
    print("b + 2 f_emp c + 3 f_emp^2 d = 0")
    print(f"plane eval at (3,12,8)  = {plane_eval:.12f}")
    print(f"distance to plane       = {plane_dist:.12f}")
    print(f"relative distance       = {plane_rel:.12f}")
    print(f"nearest point on plane  = {nearest_plane_point}")
    print(f"nearest ratio (d=1)     = {nearest_plane_point / nearest_plane_point[2]}")
    print()

    print("== Representative cubic minima ==")
    samples = [
        (3.0, 12.0, 8.0),
        (-1.356728845233823, 11.514690973260247, 7.959454984496095),
        (-1.35, 11.45, 8.0),
        (-1.30, 11.00, 8.0),
    ]
    for coeffs in samples:
        stationary = cubic_stationary_deltas(*coeffs)
        value, delta_min = cubic_global_minimum(*coeffs)
        print(f"coeffs={coeffs} -> stationary deltas={stationary}")
        print(
            f"  global min delta={delta_min:.12f}, "
            f"|delta-delta_emp|={abs(delta_min - DELTA_EMP):.12e}, value={value:.12f}"
        )
    print()

    print("== Local scan around Chebyshev point with d fixed at 8 ==")
    best: list[tuple[float, float, float, float, float]] = []
    count_within_mass = 0
    count_within_emp = 0
    for db in np.linspace(-6.0, 6.0, 241):
        for dc in np.linspace(-12.0, 12.0, 481):
            b = 3.0 + db
            c = 12.0 + dc
            d = 8.0
            _, delta_min = cubic_global_minimum(b, c, d)
            diff = abs(delta_min - DELTA_EMP)
            if diff <= M_TAU_DELTA_UNCERTAINTY:
                count_within_mass += 1
            if diff <= abs(DELTA_EMP - DELTA_TWO_NINTHS):
                count_within_emp += 1
            if len(best) < 10 or diff < best[-1][0]:
                best.append((diff, b, c, d, delta_min))
                best = sorted(best)[:10]
    print(f"count within m_tau uncertainty   = {count_within_mass}")
    print(f"count within empirical 2/9 gap   = {count_within_emp}")
    print("best nearby coefficient sets:")
    for row in best:
        print(
            f"  diff={row[0]:.12e}, coeffs=({row[1]:.6f}, {row[2]:.6f}, {row[3]:.6f}), "
            f"delta_min={row[4]:.12f}"
        )
    print()

    print("== Historical proxy potential audit ==")
    xs = np.linspace(0.0, 2.0 * math.pi, 400000, endpoint=False)
    vals = np.array([proxy_value(x) for x in xs])
    minima_indices = argrelmin(vals, order=30, mode="wrap")[0]
    minima = sorted(float(xs[i]) for i in minima_indices)
    print(f"number of minima on [0, 2pi) = {len(minima)}")
    for idx, delta_min in enumerate(minima):
        print(
            f"  min {idx}: delta={delta_min:.12f}, "
            f"|delta-delta_emp|={abs(delta_min - DELTA_EMP):.12e}"
        )
    closest = min(minima, key=lambda x: abs(x - DELTA_EMP))
    print(f"closest proxy minimum     = {closest:.12f}")
    print(f"closest gap to delta_emp  = {abs(closest - DELTA_EMP):.12e}")
    print(f"gap / m_tau uncertainty   = {abs(closest - DELTA_EMP) / M_TAU_DELTA_UNCERTAINTY:.6f}")
    print(
        f"gap / empirical 2/9 gap   = "
        f"{abs(closest - DELTA_EMP) / abs(DELTA_EMP - DELTA_TWO_NINTHS):.6f}"
    )

    h = 1e-7
    vp = (proxy_value(DELTA_EMP + h) - proxy_value(DELTA_EMP - h)) / (2.0 * h)
    vpp = (
        proxy_value(DELTA_EMP + h)
        - 2.0 * proxy_value(DELTA_EMP)
        + proxy_value(DELTA_EMP - h)
    ) / (h * h)
    print(f"proxy value at delta_emp  = {proxy_value(DELTA_EMP):.12e}")
    print(f"proxy derivative there    = {vp:.12e}")
    print(f"proxy 2nd derivative      = {vpp:.12e}")


if __name__ == "__main__":
    main()
