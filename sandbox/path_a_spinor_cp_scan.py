#!/usr/bin/env python3
"""
path_a_spinor_cp_scan.py
========================

Bounded executable attack on God Equation Path A.

Question:
Can left-chiral weak coupling, by itself or with a minimal CP-odd phase
deformation, drive the generation-walk operator

    T = alpha * S_bar + beta * S_bar^2

toward the pure forward shift beta/alpha -> 0?

This script checks three things:

1. Chirality-only factorization:
   P_L acts on spinor space, not generation space. Does tensoring with P_L change
   the generation coefficients alpha, beta? Expected answer: no.

2. Minimal CP-odd phase deformation:
   Starting from symmetric amplitudes a(S_bar + S_bar^2), add an antisymmetric
   imaginary term i * eps * (S_bar - S_bar^2). This changes phases, but does it
   suppress |beta/alpha|? Expected answer: no.

3. Genuine amplitude asymmetry:
   Add a real directional asymmetry delta so that
     T = (a + delta + i eps) S_bar + (a - delta - i eps) S_bar^2.
   This is the first family that can actually move |beta/alpha| away from 1.

Scope:
- no claim that any surviving asymmetry term is derived from PF axioms
- no claim that H_prod is closed
- this is a structural scan for what Path A would need
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR / "path_a_spinor_cp_scan.csv"

S_BAR = np.array(
    [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=np.complex128,
)
S_BAR2 = S_BAR @ S_BAR


def ratio(alpha: complex, beta: complex) -> float:
    if abs(alpha) < 1e-14:
        return np.inf
    return float(abs(beta / alpha))


def is_diagonal_after_three_steps(alpha: complex, beta: complex, tol: float = 1e-10) -> bool:
    t = alpha * S_BAR + beta * S_BAR2
    t3 = np.linalg.matrix_power(t, 3)
    offdiag = t3 - np.diag(np.diag(t3))
    return bool(np.max(np.abs(offdiag)) < tol)


def chiral_factorization_check(alpha: complex, beta: complex) -> dict[str, float]:
    """
    Use a minimal 2x2 chiral space:
      P_L = [[1,0],[0,0]]
    and generation operator M_gen = alpha S + beta S^2.

    Restricting to the left-handed block leaves M_gen unchanged.
    """
    p_l = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)
    m_gen = alpha * S_BAR + beta * S_BAR2
    full_op = np.kron(p_l, m_gen)

    # Extract the surviving left-handed generation block.
    left_block = full_op[:3, :3]

    return {
        "block_residual": float(np.max(np.abs(left_block - m_gen))),
        "ratio_before": ratio(alpha, beta),
        "ratio_after": ratio(
            np.trace(S_BAR.conj().T @ left_block) / 3.0,
            np.trace(S_BAR2.conj().T @ left_block) / 3.0,
        ),
    }


def cp_phase_only_family(a: float, eps: float) -> tuple[complex, complex]:
    alpha = a + 1j * eps
    beta = a - 1j * eps
    return alpha, beta


def directional_family(a: float, delta: float, eps: float) -> tuple[complex, complex]:
    alpha = (a + delta) + 1j * eps
    beta = (a - delta) - 1j * eps
    return alpha, beta


def run_scan() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []

    # Baseline chirality-only check on the symmetric nearest-neighbor coefficients.
    base_alpha = 0.5 + 0.0j
    base_beta = 0.5 + 0.0j
    chirality = chiral_factorization_check(base_alpha, base_beta)
    rows.append(
        {
            "family": "chirality_only",
            "a": 0.5,
            "delta": 0.0,
            "eps": 0.0,
            "alpha_abs": abs(base_alpha),
            "beta_abs": abs(base_beta),
            "beta_over_alpha_abs": chirality["ratio_after"],
            "diagonal_t3": float(is_diagonal_after_three_steps(base_alpha, base_beta)),
            "block_residual": chirality["block_residual"],
        }
    )

    # CP-odd phase only: cannot change magnitude ratio from 1.
    for eps in np.linspace(0.0, 1.0, 11):
        alpha, beta = cp_phase_only_family(a=0.5, eps=float(eps))
        rows.append(
            {
                "family": "cp_phase_only",
                "a": 0.5,
                "delta": 0.0,
                "eps": float(eps),
                "alpha_abs": abs(alpha),
                "beta_abs": abs(beta),
                "beta_over_alpha_abs": ratio(alpha, beta),
                "diagonal_t3": float(is_diagonal_after_three_steps(alpha, beta)),
                "block_residual": 0.0,
            }
        )

    # Directional asymmetry: first family that can actually suppress beta/alpha.
    for delta in np.linspace(0.0, 0.5, 11):
        alpha, beta = directional_family(a=0.5, delta=float(delta), eps=0.0)
        rows.append(
            {
                "family": "directional_asymmetry",
                "a": 0.5,
                "delta": float(delta),
                "eps": 0.0,
                "alpha_abs": abs(alpha),
                "beta_abs": abs(beta),
                "beta_over_alpha_abs": ratio(alpha, beta),
                "diagonal_t3": float(is_diagonal_after_three_steps(alpha, beta)),
                "block_residual": 0.0,
            }
        )

    # Mixed directional + CP-odd deformation.
    for delta in np.linspace(0.0, 0.5, 6):
        for eps in np.linspace(0.0, 0.5, 6):
            alpha, beta = directional_family(a=0.5, delta=float(delta), eps=float(eps))
            rows.append(
                {
                    "family": "directional_plus_cp",
                    "a": 0.5,
                    "delta": float(delta),
                    "eps": float(eps),
                    "alpha_abs": abs(alpha),
                    "beta_abs": abs(beta),
                    "beta_over_alpha_abs": ratio(alpha, beta),
                    "diagonal_t3": float(is_diagonal_after_three_steps(alpha, beta)),
                    "block_residual": 0.0,
                }
            )

    return rows


def save_csv(rows: list[dict[str, float | str]]) -> None:
    fieldnames = list(rows[0].keys())
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def first_threshold(rows: list[dict[str, float | str]], family: str, threshold: float) -> dict[str, float | str] | None:
    candidates = [
        row for row in rows
        if row["family"] == family and float(row["beta_over_alpha_abs"]) <= threshold
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda row: (float(row["delta"]), float(row["eps"])))


def main() -> None:
    rows = run_scan()
    save_csv(rows)

    chirality = next(row for row in rows if row["family"] == "chirality_only")
    cp_rows = [row for row in rows if row["family"] == "cp_phase_only"]
    asym_rows = [row for row in rows if row["family"] == "directional_asymmetry"]
    mixed_rows = [row for row in rows if row["family"] == "directional_plus_cp"]

    print("=" * 70)
    print("PATH A SPINOR / CP SCAN")
    print("=" * 70)
    print()
    print("1. Chirality-only factorization")
    print(f"   left-block residual: {float(chirality['block_residual']):.2e}")
    print(f"   |beta/alpha| before: {float(chirality['alpha_abs']) and 1.0:.4f}")
    print(f"   |beta/alpha| after : {float(chirality['beta_over_alpha_abs']):.4f}")
    print("   verdict: P_L acts on spinor space only; generation coefficients are unchanged.")
    print()

    print("2. CP-odd phase-only deformation  T = (a+i eps) S + (a-i eps) S^2")
    cp_ratios = sorted({round(float(row["beta_over_alpha_abs"]), 10) for row in cp_rows})
    print(f"   unique |beta/alpha| values across eps in [0,1]: {cp_ratios}")
    print("   verdict: pure phase deformation changes phases, not the magnitude ratio.")
    print()

    print("3. Directional asymmetry  T = (a+delta) S + (a-delta) S^2")
    for target in (0.5, 0.1, 0.01):
        hit = first_threshold(asym_rows, "directional_asymmetry", target)
        if hit is None:
            print(f"   threshold |beta/alpha| <= {target:.2f}: not reached in scan")
        else:
            print(
                f"   threshold |beta/alpha| <= {target:.2f}: "
                f"delta={float(hit['delta']):.3f}, ratio={float(hit['beta_over_alpha_abs']):.4f}"
            )
    print()

    print("4. Mixed directional + CP deformation")
    mixed_hit = first_threshold(mixed_rows, "directional_plus_cp", 0.1)
    if mixed_hit is None:
        print("   threshold |beta/alpha| <= 0.10: not reached in mixed scan")
    else:
        print(
            "   first threshold |beta/alpha| <= 0.10: "
            f"delta={float(mixed_hit['delta']):.3f}, eps={float(mixed_hit['eps']):.3f}, "
            f"ratio={float(mixed_hit['beta_over_alpha_abs']):.4f}"
        )
    print()

    print("5. Structural conclusion")
    print("   - chirality alone does not move beta/alpha")
    print("   - a pure CP-odd phase term does not move |beta/alpha| away from 1")
    print("   - only a genuine directional amplitude asymmetry suppresses beta/alpha")
    print("   - therefore Path A needs a generation-directional asymmetry mechanism,")
    print("     not just P_L and not just a pure phase")
    print()
    print(f"CSV written to: {CSV_PATH}")


if __name__ == "__main__":
    main()
