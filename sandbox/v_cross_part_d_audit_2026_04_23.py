#!/usr/bin/env python3
"""
Reconstruct Rivero cos9delta_derivation.py Part (d) from local audited formulas.

Server source was unavailable during this pass. The formulas used here are the
ones already preserved in:
  derivations/koide_phase_existing_observable_audit_2026-04-20.md

Let theta = 3*delta and x = cos(theta).
  f(delta) = -1/2 + cos(3*delta)/sqrt(2)

Cross term:
  V_cross = f^6 * sum_k 1/g_k^2 = -6 f^5 + (9/4) f^4

Pure W3^2 term:
  V_pure = f^12 * sum_k 1/g_k^4 = 24 f^10 - 27 f^9 + (81/16) f^8

The script expands both as Chebyshev/Fourier series:
  V(delta) = sum_m a_m cos(3*m*delta)

It then tests whether one relative coupling rho in:
  V_total = V_cross + rho * V_pure
can cancel lower harmonics and leave cos(9*delta) dominant.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as s


X = s.symbols("x")
SQRT2 = s.sqrt(2)


@dataclass(frozen=True)
class Spectrum:
    name: str
    coeffs: dict[int, s.Expr]

    def coeff(self, m: int) -> s.Expr:
        return self.coeffs.get(m, s.Integer(0))


def chebyshev_coefficients(poly: s.Expr) -> dict[int, s.Expr]:
    """Return coefficients a_m for poly(cos theta) = sum a_m cos(m theta)."""

    poly = s.expand(poly)
    degree = s.Poly(poly, X).degree()
    symbols = s.symbols(f"a0:{degree + 1}")
    basis = sum(symbols[m] * s.chebyshevt(m, X) for m in range(degree + 1))
    residual = s.Poly(s.expand(basis - poly), X)
    solution = s.solve(residual.all_coeffs(), symbols, dict=True)[0]
    return {
        m: s.simplify(solution[symbols[m]])
        for m in range(degree + 1)
        if s.simplify(solution[symbols[m]]) != 0
    }


def total_coeff(cross: Spectrum, pure: Spectrum, rho: s.Expr, m: int) -> s.Expr:
    return s.simplify(cross.coeff(m) + rho * pure.coeff(m))


def print_spectrum_table(cross: Spectrum, pure: Spectrum) -> None:
    all_m = sorted(set(cross.coeffs) | set(pure.coeffs))
    print("Fourier/Chebyshev coefficients")
    print("V(delta) = sum_m a_m cos(3*m*delta)")
    print()
    print(f"{'m':>2} {'harmonic':>10} {'V_cross':>28} {'V_cross_float':>16} {'V_pure':>30} {'V_pure_float':>16}")
    print("-" * 112)
    for m in all_m:
        c = cross.coeff(m)
        p = pure.coeff(m)
        print(
            f"{m:>2d} {3*m:>10d} "
            f"{str(s.factor(c)):>28} {float(s.N(c)):>16.9f} "
            f"{str(s.factor(p)):>30} {float(s.N(p)):>16.9f}"
        )


def print_key_ratios(cross: Spectrum, pure: Spectrum) -> None:
    print()
    print("Raw lower-harmonic ratios")
    print()
    for spec in (cross, pure):
        c3 = spec.coeff(1)
        c6 = spec.coeff(2)
        c9 = spec.coeff(3)
        print(f"{spec.name}:")
        print(f"  cos(3d)/cos(9d) = {s.N(c3 / c9, 12)}")
        print(f"  cos(6d)/cos(9d) = {s.N(c6 / c9, 12)}")
        print(f"  signs c3,c6,c9   = {math.copysign(1, float(c3)):+.0f}, {math.copysign(1, float(c6)):+.0f}, {math.copysign(1, float(c9)):+.0f}")


def print_cancellation_case(cross: Spectrum, pure: Spectrum, rho: s.Expr, label: str) -> None:
    print()
    print(label)
    print(f"rho = {s.factor(rho)} = {float(s.N(rho)):.12f}")
    print(f"{'harmonic':>10} {'total_coeff':>28} {'float':>16} {'rel_to_abs_cos9':>18}")
    print("-" * 76)
    cos9_abs = abs(float(s.N(total_coeff(cross, pure, rho, 3))))
    for m in range(1, max(pure.coeffs) + 1):
        coeff = total_coeff(cross, pure, rho, m)
        if coeff == 0:
            rel = 0.0
        elif cos9_abs:
            rel = abs(float(s.N(coeff))) / cos9_abs
        else:
            rel = float("inf")
        print(f"{3*m:>10d} {str(s.factor(coeff)):>28} {float(s.N(coeff)):>16.9f} {rel:>18.9f}")


def scan_cos9_dominance(cross: Spectrum, pure: Spectrum) -> tuple[float, float] | None:
    """Numerically find a rho interval where |cos9| is the largest harmonic."""

    max_m = max(pure.coeffs)
    cross_float = {
        m: float(s.N(cross.coeff(m)))
        for m in range(1, max_m + 1)
    }
    pure_float = {
        m: float(s.N(pure.coeff(m)))
        for m in range(1, max_m + 1)
    }

    def dominant_is_cos9(rho: float) -> bool:
        values = {
            m: abs(cross_float[m] + rho * pure_float[m])
            for m in range(1, max_m + 1)
        }
        return max(values, key=values.get) == 3

    step = 1e-6
    lo = -0.2
    hi = 0.1
    start = None
    last_true = None
    count = int(round((hi - lo) / step))
    for idx in range(count + 1):
        rho = lo + idx * step
        if dominant_is_cos9(rho):
            if start is None:
                start = rho
            last_true = rho
        elif start is not None:
            break
    if start is None or last_true is None:
        return None
    return start, last_true


def main() -> None:
    f = -s.Rational(1, 2) + X / SQRT2
    v_cross = s.expand(-6 * f**5 + s.Rational(9, 4) * f**4)
    v_pure = s.expand(24 * f**10 - 27 * f**9 + s.Rational(81, 16) * f**8)

    cross = Spectrum("V_cross", chebyshev_coefficients(v_cross))
    pure = Spectrum("V_pure", chebyshev_coefficients(v_pure))

    print("Reconstructed Rivero Part (d) harmonic audit")
    print()
    print("Source status: original server script was unavailable; using locally preserved exact reductions.")
    print("x = cos(3*delta)")
    print(f"V_cross(x) = {s.factor(v_cross)}")
    print(f"V_pure(x)  = {s.factor(v_pure)}")
    print()

    print_spectrum_table(cross, pure)
    print_key_ratios(cross, pure)

    rho_cancel_c3 = s.simplify(-cross.coeff(1) / pure.coeff(1))
    rho_cancel_c6 = s.simplify(-cross.coeff(2) / pure.coeff(2))
    rho_least_squares = s.simplify(
        -(
            cross.coeff(1) * pure.coeff(1)
            + cross.coeff(2) * pure.coeff(2)
        )
        / (pure.coeff(1) ** 2 + pure.coeff(2) ** 2)
    )

    print()
    print("Cancellation ratios")
    print(f"rho to cancel cos(3*delta): {s.factor(rho_cancel_c3)} = {float(s.N(rho_cancel_c3)):.12f}")
    print(f"rho to cancel cos(6*delta): {s.factor(rho_cancel_c6)} = {float(s.N(rho_cancel_c6)):.12f}")
    print(f"rho least-squares for cos3/cos6 lower pair: {s.N(rho_least_squares, 12)}")
    print("Same-sign addition (rho > 0) does not cancel the cos(3*delta) term; cancellation requires a negative relative sign.")

    print_cancellation_case(cross, pure, rho_cancel_c3, "Case A: exact cos(3*delta) cancellation")
    print_cancellation_case(cross, pure, rho_cancel_c6, "Case B: exact cos(6*delta) cancellation")
    print_cancellation_case(cross, pure, rho_least_squares, "Case C: least-squares lower-harmonic suppression")

    dominance = scan_cos9_dominance(cross, pure)
    print()
    print("Dominance scan")
    if dominance is None:
        print("No rho in [-0.2, 0.1] made cos(9*delta) the largest oscillating harmonic.")
    else:
        print(
            "Numerical interval where cos(9*delta) is the largest oscillating harmonic: "
            f"rho in [{dominance[0]:.6f}, {dominance[1]:.6f}]"
        )

    print()
    print("Verdict")
    print("- Raw V_cross and V_pure both carry same-sign cos(3*delta), so they do not cancel under same-sign addition.")
    print("- A negative relative coupling can cancel cos(3*delta), and in a finite interval makes cos(9*delta) the largest harmonic.")
    print("- One relative coupling cannot exactly cancel both cos(3*delta) and cos(6*delta); rho_3 != rho_6.")
    print("- This is a conditional structural lead, not a PF-native selector for delta = 2/9.")


if __name__ == "__main__":
    main()
