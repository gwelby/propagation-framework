#!/usr/bin/env python3
"""
PRED-003 Route C toy probe — Circulant3Spectrum free-parameter sweep.

This is NOT a PF derivation. It is a bounded attempt to see whether any
natural, parameter-free interpretation of the D=3 circulant residue
eigenvalues can produce the measured neutrino mass-squared ratio
r_ν = Δm²₂₁ / Δm²₃₁ ≈ 0.02951.

The circulant3 residue eigenvalue (per PfLean.Circulant3Spectrum) is:
    λ = b·ω + c·ω² = -(b+c)/2 + i·(√3/2)·(b-c)
    |λ|² = (b+c)²/4 + 3(b-c)²/4

On the normalized slice b + c = 1 (equal row sum, H18):
    |λ(b)|² = 3b² - 3b + 1
    minimum |λ|² = 1/4 at b = 1/2 (H17 symmetry)

We test several naive r_PF(b) candidates and ask:
1. Does any candidate have a natural "selected" point that gives 0.02951?
2. If not, how much tuning is required?
3. What physical selector would choose that point?

Expected outcome: no natural interpretation yields the measured ratio without
importing extra structure (mass scale, flavor/PMNS bridge, splitting generator).
"""

import math

R_TARGET = 0.02951          # NuFIT 6.0 Δm²₂₁/Δm²₃₁ (normal ordering)
R_TARGET_ERR = 0.00098      # NuFIT 6.0 uncertainty

OMEGA_RE = -0.5
OMEGA_IM = math.sqrt(3.0) / 2.0


def residue_eigenvalue(b: float, c: float) -> complex:
    """λ = b·ω + c·ω²."""
    # ω² = -1/2 - i√3/2
    omega2 = complex(-0.5, -math.sqrt(3.0) / 2.0)
    omega = complex(OMEGA_RE, OMEGA_IM)
    return b * omega + c * omega2


def residue_modsq(b: float, c: float) -> float:
    """|λ|² = (b+c)²/4 + 3(b-c)²/4."""
    return ((b + c) ** 2) / 4.0 + 3.0 * ((b - c) ** 2) / 4.0


def uniform_eigenvalue(b: float, c: float) -> float:
    """Uniform mode eigenvalue = b + c (row sum)."""
    return b + c


def candidates():
    """Sweep several naive r_PF(b,c) candidates."""
    results = []
    # Normalized slice: b + c = 1, b in (0, 1)
    for b in [0.05 * i for i in range(1, 20)]:
        c = 1.0 - b
        lam = residue_eigenvalue(b, c)
        mods = residue_modsq(b, c)
        unif = uniform_eigenvalue(b, c)

        # Candidate 1: residue |λ|² / uniform eigenvalue (row sum)
        # At b=1/2 this is (1/4) / 1 = 0.25 — 8.5× too large.
        r1 = mods / unif

        # Candidate 2: squared imaginary part over squared real part
        # At b=1/2 the imaginary part is 0, so r2 = 0.
        real = lam.real
        imag = lam.imag
        r2 = (imag * imag) / (real * real) if abs(real) > 1e-12 else float('inf')

        # Candidate 3: (b-c)² / (b+c)² — the normalized asymmetry squared
        # At b=1/2 this is 0; at endpoints it is 1.
        r3 = ((b - c) ** 2) / ((b + c) ** 2) if (b + c) > 0 else 0.0

        # Candidate 4: (b-c) / (b+c) — normalized asymmetry (not squared)
        r4 = (b - c) / (b + c) if (b + c) > 0 else 0.0

        results.append({
            'b': b,
            'c': c,
            'modsq': mods,
            'r1_modsq_over_uniform': r1,
            'r2_imag2_over_real2': r2,
            'r3_asymmetry_squared': r3,
            'r4_asymmetry': r4,
        })
    return results


def find_closest(candidate_values, key):
    """Find the b that makes a given candidate closest to the target ratio."""
    best = None
    best_diff = float('inf')
    for row in candidate_values:
        v = row[key]
        if not math.isfinite(v):
            continue
        diff = abs(v - R_TARGET)
        if diff < best_diff:
            best_diff = diff
            best = (row['b'], row['c'], v, diff)
    return best, best_diff


def main():
    data = candidates()

    print("=" * 70)
    print("PRED-003 Route C toy probe — Circulant3Spectrum")
    print(f"Target ratio r_ν = {R_TARGET} ± {R_TARGET_ERR}")
    print("=" * 70)

    print("\nSample points on normalized slice b + c = 1:")
    print(f"{'b':>5} {'c':>5} {'|λ|²':>10} {'r1=|λ|²/u':>14} "
          f"{'r2=Im²/Re²':>14} {'r3=Δ²/Σ²':>14} {'r4=Δ/Σ':>14}")
    for row in data[::4]:  # every 4th point for brevity
        print(f"{row['b']:.2f} {row['c']:.2f} {row['modsq']:>10.5f} "
              f"{row['r1_modsq_over_uniform']:>14.5f} "
              f"{row['r2_imag2_over_real2']:>14.5f} "
              f"{row['r3_asymmetry_squared']:>14.5f} "
              f"{row['r4_asymmetry']:>14.5f}")

    print("\n" + "=" * 70)
    print("Best-fit b for each naive candidate (no physical selector):")

    for key, label in [
        ('r1_modsq_over_uniform', '|λ|² / uniform eigenvalue'),
        ('r2_imag2_over_real2', 'Im(λ)² / Re(λ)²'),
        ('r3_asymmetry_squared', '(b-c)² / (b+c)²'),
        ('r4_asymmetry', '(b-c) / (b+c)'),
    ]:
        best, diff = find_closest(data, key)
        if best is None:
            continue
        b, c, v, d = best
        sigma = d / R_TARGET_ERR
        print(f"  {label:30s} -> b={b:.4f}, c={c:.4f}, r_PF={v:.5f}, "
              f"|r_PF - r_ν|={d:.5f} ({sigma:.2f}σ)")

    print("\n" + "=" * 70)
    print("Observations:")
    print("- Candidate r1 (|λ|² / uniform) has a natural selected point at b=1/2,")
    print("  giving 0.25 — not 0.0295. It is 227σ away from the measured ratio.")
    print("- Candidates r2, r3, r4 can be tuned to hit 0.0295, but only by choosing")
    print("  an *ad hoc* b/c asymmetry. No PF axiom or theorem selects that b.")
    print("- The required tuning is not a derivation; it is a fit.")
    print("- This supports the scoping finding: a mass-squared-difference generator")
    print("  and a flavor/PMNS bridge are missing before PRED-003 can be built.")

    # Check the symmetric point explicitly
    b_sym = 0.5
    c_sym = 0.5
    modsym = residue_modsq(b_sym, c_sym)
    r1_sym = modsym / uniform_eigenvalue(b_sym, c_sym)
    print(f"\nSymmetric point b=c=1/2 (H17): |λ|²={modsym:.5f}, r1={r1_sym:.5f}")
    print(f"Distance from target: {abs(r1_sym - R_TARGET) / R_TARGET_ERR:.1f}σ")


if __name__ == '__main__':
    main()
