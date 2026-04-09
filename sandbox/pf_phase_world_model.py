#!/usr/bin/env python3
"""
pf_phase_world_model.py
=======================

Phase 1b scaffold for a PF-style world model with a complex Z3 latent.

This file extends the probability-walk toy into the layer PF actually needs:
complex amplitudes, local phase-bearing propagation, and phase-sensitive
observables.

What it does:
- represents latent state as complex amplitudes on three Z3 channels
- uses a local operator T = a I + b S + c S^2
- fits the propagator coefficients from synthetic teacher trajectories
- separates latent dynamics from a phase-sensitive observation head
- reports bounded diagnostics (recurrence, 3-step closure, entropy, T^3 structure)

What it does NOT do:
- derive the Axiom 3 selector
- prove H_prod
- identify the final PF probability law
- upgrade any repo claim status

This is an architecture pressure-test harness, not an evidentiary artifact.

Run:
  python3 sandbox/pf_phase_world_model.py
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


I3 = np.eye(3, dtype=np.complex128)
S = np.array(
    [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=np.complex128,
)
S2 = S @ S


def format_complex(z: complex) -> str:
    """Compact complex-number formatter for terminal output."""
    return f"{z.real:+.4f}{z.imag:+.4f}i"


def normalize_rows(x: np.ndarray) -> np.ndarray:
    """Normalize each complex state to unit norm."""
    denom = np.linalg.norm(x, axis=1, keepdims=True)
    denom = np.where(denom < 1e-12, 1.0, denom)
    return x / denom


def sample_complex_states(batch_size: int, rng: np.random.Generator) -> np.ndarray:
    """Random unit-norm complex states on C^3."""
    x = rng.standard_normal((batch_size, 3)) + 1j * rng.standard_normal((batch_size, 3))
    return normalize_rows(x)


def spectral_radius(matrix: np.ndarray) -> float:
    return float(np.max(np.abs(np.linalg.eigvals(matrix))))


def rescale_coeffs_to_radius(coeffs: np.ndarray, target_radius: float = 1.0) -> np.ndarray:
    """Rescale coefficients so the induced operator has the requested spectral radius."""
    matrix = coeffs[0] * I3 + coeffs[1] * S + coeffs[2] * S2
    radius = spectral_radius(matrix)
    if radius < 1e-12:
        return coeffs.copy()
    return coeffs * (target_radius / radius)


@dataclass
class OperatorSpec:
    name: str
    coeffs: np.ndarray

    def matrix(self) -> np.ndarray:
        return self.coeffs[0] * I3 + self.coeffs[1] * S + self.coeffs[2] * S2


class PFPhaseWorldModel:
    """
    Minimal phase-bearing world model:
    - local complex propagator on Z3
    - phase-sensitive observation head on gauge-invariant features
    """

    def __init__(self, coeffs: np.ndarray | None = None, obs_dim: int = 4):
        self.coeffs = (
            np.array([0.0 + 0.0j, 0.4 + 0.0j, 0.4 + 0.0j], dtype=np.complex128)
            if coeffs is None
            else np.asarray(coeffs, dtype=np.complex128)
        )
        self.obs_dim = obs_dim
        self.obs_weights = np.zeros((obs_dim, 9), dtype=np.float64)
        self.obs_bias = np.zeros(obs_dim, dtype=np.float64)

    def operator_matrix(self) -> np.ndarray:
        return self.coeffs[0] * I3 + self.coeffs[1] * S + self.coeffs[2] * S2

    def propagate(self, x_t: np.ndarray) -> np.ndarray:
        """One-step complex propagation for row-batched states."""
        return x_t @ self.operator_matrix().T

    def feature_map(self, x_t: np.ndarray) -> np.ndarray:
        """
        Gauge-invariant, phase-sensitive features:
        - per-channel intensities |x_i|^2
        - real and imaginary parts of pairwise coherences x_i * conj(x_j)
        """
        x_n = normalize_rows(x_t)
        intensities = np.abs(x_n) ** 2

        coh_01 = x_n[:, 0] * np.conj(x_n[:, 1])
        coh_12 = x_n[:, 1] * np.conj(x_n[:, 2])
        coh_20 = x_n[:, 2] * np.conj(x_n[:, 0])

        return np.column_stack(
            [
                intensities[:, 0],
                intensities[:, 1],
                intensities[:, 2],
                coh_01.real,
                coh_12.real,
                coh_20.real,
                coh_01.imag,
                coh_12.imag,
                coh_20.imag,
            ]
        )

    def observe(self, x_t: np.ndarray) -> np.ndarray:
        features = self.feature_map(x_t)
        return features @ self.obs_weights.T + self.obs_bias

    def fit_propagator(self, x_t: np.ndarray, x_next: np.ndarray) -> np.ndarray:
        """
        Fit a, b, c in x_(t+1) = (a I + b S + c S^2) x_t by complex least squares.
        """
        basis_0 = x_t
        basis_1 = x_t @ S.T
        basis_2 = x_t @ S2.T

        design = np.column_stack(
            [
                basis_0.reshape(-1),
                basis_1.reshape(-1),
                basis_2.reshape(-1),
            ]
        )
        target = x_next.reshape(-1)
        coeffs, _, _, _ = np.linalg.lstsq(design, target, rcond=None)
        self.coeffs = coeffs.astype(np.complex128)
        return self.coeffs

    def fit_observation_head(self, x_t: np.ndarray, y_target: np.ndarray) -> None:
        features = self.feature_map(x_t)
        features_aug = np.column_stack([features, np.ones(features.shape[0])])
        solved, _, _, _ = np.linalg.lstsq(features_aug, y_target, rcond=None)
        self.obs_weights = solved[:-1, :].T
        self.obs_bias = solved[-1, :]


def rollout_pairs(
    operator: np.ndarray,
    batch_size: int,
    steps: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Collect one-step trajectory pairs from random initial complex states."""
    x_t = sample_complex_states(batch_size, rng)
    x_curr = x_t.copy()

    current_states: list[np.ndarray] = []
    next_states: list[np.ndarray] = []

    for _ in range(steps):
        x_next = x_curr @ operator.T
        current_states.append(x_curr.copy())
        next_states.append(x_next.copy())
        x_curr = x_next

    return np.vstack(current_states), np.vstack(next_states)


def make_teacher_observations(x_t: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fixed synthetic teacher observation head on phase-sensitive features.
    This keeps the observable bridge separate from the latent dynamics.
    """
    model = PFPhaseWorldModel(obs_dim=4)
    features = model.feature_map(x_t)
    weights = np.array(
        [
            [0.90, -0.20, -0.70, 0.60, 0.00, -0.40, 0.30, 0.10, -0.20],
            [-0.25, 0.80, -0.55, -0.15, 0.45, 0.25, 0.60, -0.35, 0.10],
            [0.00, -0.50, 0.50, 0.40, -0.40, 0.55, -0.20, 0.15, 0.35],
            [0.30, 0.30, 0.30, -0.50, 0.50, 0.00, 0.10, 0.25, -0.25],
        ],
        dtype=np.float64,
    )
    bias = np.array([0.10, -0.05, 0.00, 0.20], dtype=np.float64)
    y_target = features @ weights.T + bias
    return y_target, weights, bias


def mean_intensity_entropy(x_t: np.ndarray) -> float:
    intensities = np.abs(normalize_rows(x_t)) ** 2
    safe = np.clip(intensities, 1e-15, 1.0)
    return float(np.mean(-np.sum(safe * np.log2(safe), axis=1)))


def recurrence_score(x_t: np.ndarray, x_next: np.ndarray) -> float:
    x_n = normalize_rows(x_t)
    y_n = normalize_rows(x_next)
    overlaps = np.sum(np.conj(x_n) * y_n, axis=1)
    return float(np.mean(np.abs(overlaps)))


def pairwise_phase_coherence(x_t: np.ndarray) -> float:
    x_n = normalize_rows(x_t)
    coh_01 = np.abs(x_n[:, 0] * np.conj(x_n[:, 1]))
    coh_12 = np.abs(x_n[:, 1] * np.conj(x_n[:, 2]))
    coh_20 = np.abs(x_n[:, 2] * np.conj(x_n[:, 0]))
    return float(np.mean((coh_01 + coh_12 + coh_20) / 3.0))


def closure_report(operator: np.ndarray) -> dict[str, float]:
    t3 = operator @ operator @ operator
    off_diag = t3 - np.diag(np.diag(t3))
    return {
        "spectral_radius": spectral_radius(operator),
        "t3_offdiag_frob": float(np.linalg.norm(off_diag)),
        "t3_diag_frob": float(np.linalg.norm(np.diag(np.diag(t3)))),
    }


def evaluate_rollout(
    teacher: np.ndarray,
    student: np.ndarray,
    batch_size: int,
    steps: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    x_teacher = sample_complex_states(batch_size, rng)
    x_student = x_teacher.copy()

    mse_per_step: list[float] = []
    teacher_entropy: list[float] = []
    student_entropy: list[float] = []

    for _ in range(steps):
        x_teacher = x_teacher @ teacher.T
        x_student = x_student @ student.T
        mse_per_step.append(float(np.mean(np.abs(x_teacher - x_student) ** 2)))
        teacher_entropy.append(mean_intensity_entropy(x_teacher))
        student_entropy.append(mean_intensity_entropy(x_student))

    return {
        "rollout_mse": float(np.mean(mse_per_step)),
        "teacher_entropy": float(np.mean(teacher_entropy)),
        "student_entropy": float(np.mean(student_entropy)),
    }


def canonical_teachers() -> list[OperatorSpec]:
    symmetric = OperatorSpec(
        name="symmetric_real",
        coeffs=np.array([0.0 + 0.0j, 0.5 + 0.0j, 0.5 + 0.0j], dtype=np.complex128),
    )
    chiral = OperatorSpec(
        name="chiral_phase",
        coeffs=np.array([0.0 + 0.0j, np.exp(1j * np.pi / 9), 0.0 + 0.0j], dtype=np.complex128),
    )
    phase_skew_raw = np.array(
        [
            0.20 * np.exp(1j * np.pi / 10),
            0.60 * np.exp(1j * np.pi / 7),
            0.25 * np.exp(-1j * np.pi / 5),
        ],
        dtype=np.complex128,
    )
    phase_skew = OperatorSpec(
        name="phase_skew",
        coeffs=rescale_coeffs_to_radius(phase_skew_raw, target_radius=0.98),
    )
    return [symmetric, chiral, phase_skew]


def print_operator_summary(spec: OperatorSpec) -> None:
    print(f"Scenario: {spec.name}")
    print("  coefficients:")
    print(f"    a = {format_complex(spec.coeffs[0])}")
    print(f"    b = {format_complex(spec.coeffs[1])}")
    print(f"    c = {format_complex(spec.coeffs[2])}")

    report = closure_report(spec.matrix())
    print(
        "  operator diagnostics: "
        f"spectral_radius={report['spectral_radius']:.4f}, "
        f"||offdiag(T^3)||_F={report['t3_offdiag_frob']:.4f}, "
        f"||diag(T^3)||_F={report['t3_diag_frob']:.4f}"
    )


def run_scenario(spec: OperatorSpec, seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    teacher_matrix = spec.matrix()

    x_train, x_next_train = rollout_pairs(teacher_matrix, batch_size=128, steps=5, rng=rng)
    y_train, _, _ = make_teacher_observations(x_next_train)

    model = PFPhaseWorldModel(obs_dim=y_train.shape[1])
    learned = model.fit_propagator(x_train, x_next_train)
    model.fit_observation_head(x_next_train, y_train)

    latent_mse = float(np.mean(np.abs(model.propagate(x_train) - x_next_train) ** 2))
    obs_mse = float(np.mean((model.observe(x_next_train) - y_train) ** 2))

    teacher_rec = recurrence_score(x_train, x_next_train)
    student_rec = recurrence_score(x_train, model.propagate(x_train))

    teacher_phase_coh = pairwise_phase_coherence(x_next_train)
    student_phase_coh = pairwise_phase_coherence(model.propagate(x_train))

    rollout = evaluate_rollout(
        teacher=teacher_matrix,
        student=model.operator_matrix(),
        batch_size=96,
        steps=6,
        rng=np.random.default_rng(seed + 100),
    )

    print_operator_summary(spec)
    print("  learned coefficients:")
    print(f"    a_hat = {format_complex(learned[0])}")
    print(f"    b_hat = {format_complex(learned[1])}")
    print(f"    c_hat = {format_complex(learned[2])}")
    print(
        "  fit errors: "
        f"latent_mse={latent_mse:.6e}, "
        f"obs_mse={obs_mse:.6e}, "
        f"rollout_mse={rollout['rollout_mse']:.6e}"
    )
    print(
        "  diagnostics: "
        f"teacher_recurrence={teacher_rec:.4f}, "
        f"student_recurrence={student_rec:.4f}, "
        f"teacher_phase_coh={teacher_phase_coh:.4f}, "
        f"student_phase_coh={student_phase_coh:.4f}"
    )
    print(
        "  entropy: "
        f"teacher_mean={rollout['teacher_entropy']:.4f}, "
        f"student_mean={rollout['student_entropy']:.4f}"
    )
    print()


def main() -> None:
    print("==============================================================")
    print(" PF PHASE WORLD MODEL - COMPLEX Z3 LATENT")
    print("==============================================================")
    print("This is a bounded architecture harness, not a derivation engine.")
    print("It fits local complex propagation and a separate observation head.")
    print()

    for index, spec in enumerate(canonical_teachers()):
        run_scenario(spec, seed=42 + 17 * index)

    print("Interpretation:")
    print("- The probability toy was useful for structure, but PF needs phase-bearing state.")
    print("- A local operator T = a I + b S + c S^2 is the minimal complex Z3 latent.")
    print("- Gauge-invariant phase/coherence observables should stay separate from")
    print("  the latent propagation rule.")
    print("- This script pressure-tests that split without pretending to close Axiom 3 or H_prod.")


if __name__ == "__main__":
    main()
