#!/usr/bin/env python3
"""
pf_phase_world_model_experiments.py
===================================

Bounded experiment driver for the complex Z3 phase world model.

Goal:
- sweep the chirality family eta in [0, 1]
- compare a phase-bearing amplitude operator against the existing stochastic
  chirality / entropy baseline
- report endpoint information-style quantities plus phase-world diagnostics

Important scope limit:
- This script compares endpoint distributions after 1 and 3 steps.
- It does NOT define a full intermediate measurement / trajectory law for the
  complex amplitude model.
- Therefore it does NOT settle the Fisher/trajectory question from the derivation
  notes. It is an architecture comparison tool only.

Run:
  python3 sandbox/pf_phase_world_model_experiments.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from pf_phase_world_model import (
    I3,
    S,
    S2,
    mean_intensity_entropy,
    pairwise_phase_coherence,
    recurrence_score,
    sample_complex_states,
)


SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR / "pf_phase_world_model_experiments.csv"


def shannon_entropy_bits(prob: np.ndarray) -> float:
    prob = np.asarray(prob, dtype=float)
    mask = prob > 0.0
    return float(-np.sum(prob[mask] * np.log2(prob[mask])))


def mutual_information_bits(transition: np.ndarray) -> float:
    n = transition.shape[0]
    px = np.full(n, 1.0 / n)
    joint = px[:, None] * transition
    py = np.sum(joint, axis=0)
    info = 0.0
    for i in range(n):
        for j in range(n):
            if joint[i, j] > 0.0:
                info += joint[i, j] * math.log2(joint[i, j] / (px[i] * py[j]))
    return float(info)


def offdiag_frobenius(matrix: np.ndarray) -> float:
    offdiag = matrix - np.diag(np.diag(matrix))
    return float(np.linalg.norm(offdiag))


def chirality_probabilities(eta: float) -> tuple[float, float]:
    if not 0.0 <= eta <= 1.0:
        raise ValueError("eta must lie in [0, 1]")
    p_fwd = 0.5 * (1.0 + eta)
    p_bwd = 0.5 * (1.0 - eta)
    return p_fwd, p_bwd


def markov_chirality_matrix(eta: float) -> np.ndarray:
    p_fwd, p_bwd = chirality_probabilities(eta)
    # Return row-conditional transition probabilities, consistent with the
    # amplitude endpoint transition builder below.
    return (p_fwd * S + p_bwd * S2).T.real


def phase_chirality_operator(eta: float, phase: float) -> np.ndarray:
    """
    Build an amplitude operator whose one-step intensities from basis states
    match the Markov chirality family exactly:

      T_amp = sqrt(p_fwd) e^{+i phi} S + sqrt(p_bwd) e^{-i phi} S^2

    Because amplitudes are squared at readout, the basis-state one-step endpoint
    distribution matches the stochastic walk, while multi-step endpoint behavior
    can differ due to interference.
    """
    p_fwd, p_bwd = chirality_probabilities(eta)
    b = math.sqrt(p_fwd) * np.exp(1j * phase)
    c = math.sqrt(p_bwd) * np.exp(-1j * phase)
    return b * S + c * S2


def intensity_transition(operator: np.ndarray, steps: int) -> np.ndarray:
    """
    Effective endpoint transition from basis-state preparations under amplitude
    evolution. Rows are normalized intensity readouts after `steps`.
    """
    op_n = np.linalg.matrix_power(operator, steps)
    basis = I3.copy()
    amplitudes = basis @ op_n.T
    probs = np.abs(amplitudes) ** 2
    row_sums = probs.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums < 1e-12, 1.0, row_sums)
    return probs / row_sums


def random_state_diagnostics(
    operator: np.ndarray,
    rng: np.random.Generator,
    batch_size: int = 256,
) -> dict[str, float]:
    x_t = sample_complex_states(batch_size=batch_size, rng=rng)
    x_1 = x_t @ operator.T
    x_3 = x_t @ np.linalg.matrix_power(operator, 3).T
    return {
        "recurrence_t1": recurrence_score(x_t, x_1),
        "recurrence_t3": recurrence_score(x_t, x_3),
        "phase_coh_t1": pairwise_phase_coherence(x_1),
        "phase_coh_t3": pairwise_phase_coherence(x_3),
        "entropy_t1_random": mean_intensity_entropy(x_1),
        "entropy_t3_random": mean_intensity_entropy(x_3),
    }


def sweep_family(family: str, phase: float, n_eta: int = 21) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    rng = np.random.default_rng(42)

    for eta in np.linspace(0.0, 1.0, n_eta):
        eta = float(np.round(eta, 10))
        p_fwd, p_bwd = chirality_probabilities(eta)
        markov = markov_chirality_matrix(eta)
        operator = phase_chirality_operator(eta, phase=phase)

        P1_markov = markov
        P3_markov = np.linalg.matrix_power(markov, 3)
        P1_phase = intensity_transition(operator, steps=1)
        P3_phase = intensity_transition(operator, steps=3)

        max_abs_diff_p1 = float(np.max(np.abs(P1_phase - P1_markov)))
        if max_abs_diff_p1 > 1e-10:
            raise RuntimeError(
                f"one-step endpoint mismatch too large for eta={eta:.6f}, "
                f"phase={phase:.6f}: {max_abs_diff_p1:.3e}"
            )

        diag = random_state_diagnostics(operator, rng=rng)
        T3 = np.linalg.matrix_power(operator, 3)

        row = {
            "family": family,
            "phase_rad": phase,
            "eta": eta,
            "p_forward": p_fwd,
            "p_backward": p_bwd,
            "mi_t1_markov": mutual_information_bits(P1_markov),
            "mi_t1_phase": mutual_information_bits(P1_phase),
            "mi_t3_markov": mutual_information_bits(P3_markov),
            "mi_t3_phase": mutual_information_bits(P3_phase),
            "delta_mi_t3": mutual_information_bits(P3_phase) - mutual_information_bits(P3_markov),
            "entropy_t3_markov": shannon_entropy_bits(P3_markov[0]),
            "entropy_t3_phase": shannon_entropy_bits(P3_phase[0]),
            "return_t3_markov": float(P3_markov[0, 0]),
            "return_t3_phase": float(P3_phase[0, 0]),
            "max_abs_diff_p1": max_abs_diff_p1,
            "max_abs_diff_p3": float(np.max(np.abs(P3_phase - P3_markov))),
            "offdiag_t3_amp": offdiag_frobenius(T3),
            "offdiag_p3_phase": offdiag_frobenius(P3_phase),
            "offdiag_p3_markov": offdiag_frobenius(P3_markov),
            **diag,
        }
        rows.append(row)

    return rows


def save_csv(rows: list[dict[str, float | str]]) -> None:
    fieldnames = list(rows[0].keys())
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_selected_rows(rows: list[dict[str, float | str]], title: str) -> None:
    print(title)
    print(
        "  eta   mi3_markov  mi3_phase  d_mi3   ret3_phase  "
        "||offdiag(T^3)||  rec_t1  phase_coh_t1"
    )
    print("  " + "-" * 86)
    for row in rows:
        eta = float(row["eta"])
        if eta in {0.0, 0.5, 1.0}:
            print(
                f"  {eta:>3.1f}   "
                f"{float(row['mi_t3_markov']):>10.4f}  "
                f"{float(row['mi_t3_phase']):>9.4f}  "
                f"{float(row['delta_mi_t3']):>+6.4f}  "
                f"{float(row['return_t3_phase']):>10.4f}  "
                f"{float(row['offdiag_t3_amp']):>15.4f}  "
                f"{float(row['recurrence_t1']):>6.4f}  "
                f"{float(row['phase_coh_t1']):>12.4f}"
            )
    print()


def print_summary(rows: list[dict[str, float | str]], title: str) -> None:
    etas_zero = [
        float(row["eta"])
        for row in rows
        if float(row["offdiag_t3_amp"]) < 1e-8
    ]
    max_delta = max(rows, key=lambda row: abs(float(row["delta_mi_t3"])))
    print(title)
    if etas_zero:
        print(f"  first eta with diagonal T^3: {etas_zero[0]:.3f}")
    else:
        print("  no eta in sweep produced diagonal T^3")
    print(
        "  largest endpoint-MI deviation at "
        f"eta={float(max_delta['eta']):.3f}: "
        f"delta_mi_t3={float(max_delta['delta_mi_t3']):+.4f}, "
        f"max_abs_diff_p3={float(max_delta['max_abs_diff_p3']):.4f}"
    )
    print()


def main() -> None:
    print("==============================================================")
    print(" PF PHASE WORLD MODEL EXPERIMENTS - CHIRALITY SWEEP")
    print("==============================================================")
    print("Comparing:")
    print("- Markov chirality family from the existing entropy sandbox")
    print("- Complex amplitude endpoint readout from the phase world model")
    print()
    print("Scope note:")
    print("- one-step and three-step endpoint distributions only")
    print("- no intermediate measurement law")
    print("- no claim about full Fisher/trajectory closure")
    print()

    real_rows = sweep_family(family="phase0", phase=0.0)
    twisted_rows = sweep_family(family="phase_pi_over_9", phase=math.pi / 9.0)
    all_rows = real_rows + twisted_rows
    save_csv(all_rows)

    print_selected_rows(real_rows, "Real-amplitude family (phase = 0)")
    print_summary(real_rows, "Real-amplitude family summary")

    print_selected_rows(twisted_rows, "Phase-twisted family (phase = pi/9)")
    print_summary(twisted_rows, "Phase-twisted family summary")

    print(f"CSV written to: {CSV_PATH}")


if __name__ == "__main__":
    main()
