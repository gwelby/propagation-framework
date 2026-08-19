#!/usr/bin/env python3
"""
PRED-003 Route B toy probe — Koide ansatz mass-squared-ratio sweep.

This is NOT a PF derivation. It tests whether the standard Koide ansatz
    √m_k = √m̄ · (1 + β·cos(δ + 2πk/3)),   k = 0,1,2
with only the algebraic machinery that PF has in KoideGeometry/KoideSelection/KoideUnlocked,
can produce the measured neutrino mass-squared ratio
    r_ν = Δm²₂₁ / Δm²₃₁ ≈ 0.02951 (NuFIT 6.0, normal ordering)
at a point selected by a known PF principle.

The ratio is independent of the absolute scale m̄, so we set m̄ = 1 for the
dimensionless pattern and, for matching points, compute the m̄ that would
reproduce the absolute solar splitting.

The test points we single out are:
  1. The charged-lepton anchor:  β = √2  (Q = 2/3) and δ = 2/9.
  2. The charged-lepton Q = 2/3 line with the best-fit δ for r_ν.
  3. The Koide phase δ = 2/9 with the best-fit β for r_ν.
  4. The measured neutrino Q values (NO/IO) with δ = 2/9.

Expected outcome: r_ν is a one-parameter family of fits in (β,δ)-space.
The PF-known selectors (δ=2/9, Q=2/3) do not land on the r_ν = 0.02951 curve,
so the match is a fit, not a derivation.
"""

import math
import sys

# NuFIT 6.0 normal ordering (eV²)
TARGET_R = 0.02951
TARGET_R_ERR = 0.00098
TARGET_DM21 = 7.49e-5
TARGET_DM31 = 2.534e-3

# Known PF / empirical anchors
DELTA_KOIDE = 2.0 / 9.0                # the charged-lepton phase, radians
BETA_CHARGED = math.sqrt(2.0)          # Q = 2/3 amplitude
Q_NO = 0.550
Q_IO = 0.479


def amplitudes(beta: float, delta: float, mbar: float = 1.0) -> list[float]:
    """The three ansatz amplitudes a_k = √m̄·(1 + β·cos(δ + 2πk/3))."""
    sqrt_mbar = math.sqrt(mbar)
    return [
        sqrt_mbar * (1.0 + beta * math.cos(delta + 2.0 * math.pi * k / 3.0))
        for k in range(3)
    ]


def domain_ok(beta: float, delta: float) -> bool:
    """All three branches must be non-negative to be genuine square roots."""
    for k in range(3):
        if 1.0 + beta * math.cos(delta + 2.0 * math.pi * k / 3.0) < -1e-12:
            return False
    return True


def koide_Q(beta: float) -> float:
    """Algebraic Q(β) = (1 + β²/2)/3 from KoideUnlocked.lean."""
    return (1.0 + beta * beta / 2.0) / 3.0


def beta_for_Q(Q: float) -> float | None:
    """β = √(2(3Q − 1)), valid for Q ≥ 1/3."""
    arg = 2.0 * (3.0 * Q - 1.0)
    return math.sqrt(arg) if arg >= 0 else None


def sorted_mass_splittings(beta: float, delta: float, mbar: float = 1.0) -> tuple[float, float, float] | None:
    """
    Returns (Δm²₂₁, Δm²₃₁, r) for normal ordering (sorted by mass).
    The masses are m_k = a_k²; the mass-squared differences are a_k^4 differences.
    If the point is outside the physical domain or the splittings vanish, return None.
    """
    if not domain_ok(beta, delta):
        return None

    amps = amplitudes(beta, delta, mbar)
    # physical masses are amp², so the mass-squared values are amp⁴.
    # Sort by the physical mass = amp², same order as sorting by amp.
    amps.sort()
    msq = [a ** 4 for a in amps]

    dm21 = msq[1] - msq[0]
    dm31 = msq[2] - msq[0]
    if dm31 <= 1e-15:
        return None

    return dm21, dm31, dm21 / dm31


def inverted_ratio(beta: float, delta: float, mbar: float = 1.0) -> float | None:
    """IO variant: (m₂² − m₃²)/(m₁² − m₃²), using sorted-by-descending convention."""
    if not domain_ok(beta, delta):
        return None
    amps = sorted(amplitudes(beta, delta, mbar))
    msq = [a ** 4 for a in amps]
    # IO: m3 lightest, m1 heaviest
    return (msq[1] - msq[0]) / (msq[2] - msq[0])


def evaluate_point(beta: float, delta: float, mbar: float = 1.0, label: str = "") -> dict | None:
    """Return a summary dictionary for a given (β,δ), or None if invalid."""
    res = sorted_mass_splittings(beta, delta, mbar)
    if res is None:
        return None
    dm21, dm31, r = res
    amps = amplitudes(beta, delta, mbar)
    amps_sorted = sorted(amps)
    m_total = sum(a * a for a in amps)
    return {
        "label": label,
        "beta": beta,
        "delta": delta,
        "Q": koide_Q(beta),
        "r": r,
        "dr": abs(r - TARGET_R),
        "sigma": abs(r - TARGET_R) / TARGET_R_ERR,
        "dm21": dm21,
        "dm31": dm31,
        "m_total": m_total,
        "a_sorted": amps_sorted,
    }


def grid_scan(n_beta: int = 300, n_delta: int = 300) -> dict:
    """Brute-force scan over the physical (β,δ) domain."""
    best = None
    best_dr = float("inf")
    best_io = None
    best_io_dr = float("inf")

    # δ ∈ [0, 2π/3) is a fundamental domain because the mass set is invariant
    # under δ → δ + 2π/3 (cyclic permutation of k).
    # β ≥ 0; the physical upper bound is roughly β ≤ 2.
    beta_vals = [0.001 + 2.0 * i / (n_beta - 1) for i in range(n_beta)]
    delta_vals = [2.0 * math.pi / 3.0 * i / n_delta for i in range(n_delta)]

    hits = []  # all points within 3σ of the target

    for beta in beta_vals:
        for delta in delta_vals:
            res = sorted_mass_splittings(beta, delta)
            if res is None:
                continue
            dm21, dm31, r = res
            dr = abs(r - TARGET_R)
            if dr < best_dr:
                best_dr = dr
                best = (beta, delta, r, dm21, dm31)
            if dr < 3.0 * TARGET_R_ERR:
                hits.append((beta, delta, r, dr, koide_Q(beta)))

    return {
        "best": best,
        "best_dr": best_dr,
        "hits": hits,
    }


def find_nearest_on_delta(delta: float, n_beta: int = 10000) -> dict | None:
    """Find the β that best reproduces the target at a fixed δ."""
    best = None
    best_dr = float("inf")
    # physical β upper bound: the worst branch is the most negative cos.
    for beta in [0.001 + 2.0 * i / (n_beta - 1) for i in range(n_beta)]:
        res = sorted_mass_splittings(beta, delta)
        if res is None:
            continue
        dm21, dm31, r = res
        dr = abs(r - TARGET_R)
        if dr < best_dr:
            best_dr = dr
            best = (beta, r, dr)
    if best is None:
        return None
    beta, r, dr = best
    return {
        "beta": beta,
        "Q": koide_Q(beta),
        "r": r,
        "dr": dr,
        "sigma": dr / TARGET_R_ERR,
    }


def find_nearest_on_beta(beta: float, n_delta: int = 10000) -> dict | None:
    """Find the δ that best reproduces the target at a fixed β."""
    best = None
    best_dr = float("inf")
    for i in range(n_delta):
        delta = 2.0 * math.pi / 3.0 * i / n_delta
        res = sorted_mass_splittings(beta, delta)
        if res is None:
            continue
        dm21, dm31, r = res
        dr = abs(r - TARGET_R)
        if dr < best_dr:
            best_dr = dr
            best = (delta, r, dr)
    if best is None:
        return None
    delta, r, dr = best
    return {
        "delta": delta,
        "r": r,
        "dr": dr,
        "sigma": dr / TARGET_R_ERR,
    }


def print_report():
    print("=" * 78)
    print("PRED-003 Route B toy probe — Koide ansatz → neutrino mass-squared ratio")
    print(f"Target r_ν = {TARGET_R} ± {TARGET_R_ERR}")
    print("=" * 78)

    print("\n--- 1. Specific PF / empirical anchors -------------------------------")
    anchors = [
        (BETA_CHARGED, DELTA_KOIDE, "charged-lepton anchor: β=√2, δ=2/9"),
        (beta_for_Q(Q_NO) if beta_for_Q(Q_NO) else 0.0, DELTA_KOIDE, f"measured Q_NO={Q_NO} with δ=2/9"),
        (beta_for_Q(Q_IO) if beta_for_Q(Q_IO) else 0.0, DELTA_KOIDE, f"measured Q_IO={Q_IO} with δ=2/9"),
    ]
    for beta, delta, label in anchors:
        ev = evaluate_point(beta, delta, label=label)
        if ev is None:
            print(f"  {label:50s} -> OUTSIDE DOMAIN")
            continue
        print(f"  {ev['label']:50s} β={ev['beta']:.5f}  δ={ev['delta']:.6f}  Q={ev['Q']:.5f}  r={ev['r']:.6f}  "
              f"|r−r_ν|={ev['dr']:.5f} ({ev['sigma']:.1f}σ)")

    print("\n--- 2. Best fit on the charged-lepton Q=2/3 line (β=√2) --------------")
    nearest_on_Q = find_nearest_on_beta(BETA_CHARGED)
    if nearest_on_Q:
        d = nearest_on_Q["delta"]
        print(f"  Best δ for r_ν at β=√2: δ = {d:.6f} rad ({d / (math.pi / 9):.4f}·(π/9))")
        print(f"  r = {nearest_on_Q['r']:.6f}, distance = {nearest_on_Q['dr']:.5f} "
              f"({nearest_on_Q['sigma']:.1f}σ)")
        print(f"  Compare with PF phase anchor δ = 2/9 = {DELTA_KOIDE:.6f} rad.")
    else:
        print("  No valid point found on β=√2 line.")

    print("\n--- 2a. Best-fit phase for the measured neutrino Q values ------------")
    for q, name in [(Q_NO, "NO"), (Q_IO, "IO")]:
        beta = beta_for_Q(q)
        if beta is None:
            continue
        nearest = find_nearest_on_beta(beta)
        if nearest:
            d = nearest["delta"]
            print(f"  Measured Q_{name}={q} (β={beta:.5f}):")
            print(f"    Best δ for r_ν: δ = {d:.6f} rad ({d / (math.pi / 9):.4f}·(π/9))")
            print(f"    r = {nearest['r']:.6f}, distance = {nearest['dr']:.5f} "
                  f"({nearest['sigma']:.1f}σ)")
            print(f"    Distance from PF phase anchor δ=2/9: {abs(d - DELTA_KOIDE):.6f} rad "
                  f"({abs(d - DELTA_KOIDE) / DELTA_KOIDE * 100:.1f}%)")

    print("\n--- 3. Best fit on the PF phase line (δ = 2/9) -----------------------")
    nearest_on_phase = find_nearest_on_delta(DELTA_KOIDE)
    if nearest_on_phase:
        b = nearest_on_phase["beta"]
        print(f"  Best β for r_ν at δ=2/9: β = {b:.6f}")
        print(f"  Q(β) = {nearest_on_phase['Q']:.5f}")
        print(f"  r = {nearest_on_phase['r']:.6f}, distance = {nearest_on_phase['dr']:.5f} "
              f"({nearest_on_phase['sigma']:.1f}σ)")
        print(f"  Compare with charged-lepton Q=2/3 anchor β=√2={BETA_CHARGED:.6f}.")
    else:
        print("  No valid point found on δ=2/9 line.")

    print("\n--- 4. Full (β,δ) grid scan ------------------------------------------")
    scan = grid_scan(n_beta=400, n_delta=400)
    best = scan["best"]
    if best:
        beta, delta, r, dm21, dm31 = best
        print(f"  Best-fit grid point: β={beta:.5f}, δ={delta:.6f} rad, r={r:.6f}")
        print(f"  Distance from target: {abs(r - TARGET_R):.5f} ({abs(r - TARGET_R) / TARGET_R_ERR:.2f}σ)")
        print(f"  Q at this point: {koide_Q(beta):.5f}")
        # absolute scale from solar splitting
        # dm21 is dimensionless (computed with mbar=1). Actual Δm²₂₁ = mbar²·dm21.
        mbar = math.sqrt(TARGET_DM21 / dm21)  # ansatz scale parameter, units eV
        amps = amplitudes(beta, delta, mbar)
        masses = sorted([a * a for a in amps])
        total = sum(masses)
        dm21_actual = masses[1] ** 2 - masses[0] ** 2
        dm31_actual = masses[2] ** 2 - masses[0] ** 2
        print(f"  Scale m̄ = {mbar:.6f} eV (chosen to match Δm²₂₁)")
        print(f"  Implied masses (eV): m1={masses[0]:.6f}, m2={masses[1]:.6f}, m3={masses[2]:.6f}")
        print(f"  Implied Δm²₂₁ = {dm21_actual:.6e} eV², Δm²₃₁ = {dm31_actual:.6e} eV²")
        print(f"  Implied Σmν = {total:.6f} eV")
    print(f"  Points within 3σ of target: {len(scan['hits'])}")

    print("\n--- 5. Inverted ordering (IO) sanity check ---------------------------")
    io = find_best_io()
    if io:
        print(f"  Best IO point: β={io['beta']:.5f}, δ={io['delta']:.6f} rad, r_IO={io['r']:.6f}, "
              f"distance={io['dr']:.5f} ({io['sigma']:.1f}σ)")
    else:
        print("  No valid IO point found.")

    print("\n" + "=" * 78)
    print("Interpretation:")
    print("- The ratio r_ν is a continuous function of (β,δ). A match can always be")
    print("  obtained by fitting one of these two free parameters once the other is fixed.")
    print("- The PF-known fixed points (δ=2/9, β=√2) do not reproduce r_ν.")
    print("- Therefore the Koide ansatz, as PF currently has it, does not DERIVE the")
    print("  neutrino mass-squared ratio; it can only FIT it with an additional selector")
    print("  for β or δ that PF does not possess.")
    print("=" * 78)


def find_best_io(n_beta: int = 400, n_delta: int = 400) -> dict | None:
    best = None
    best_dr = float("inf")
    for beta in [0.001 + 2.0 * i / (n_beta - 1) for i in range(n_beta)]:
        for i in range(n_delta):
            delta = 2.0 * math.pi / 3.0 * i / n_delta
            r = inverted_ratio(beta, delta)
            if r is None:
                continue
            dr = abs(r - TARGET_R)
            if dr < best_dr:
                best_dr = dr
                best = {"beta": beta, "delta": delta, "r": r, "dr": dr,
                        "sigma": dr / TARGET_R_ERR}
    return best


if __name__ == "__main__":
    print_report()
