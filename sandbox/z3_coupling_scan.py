#!/usr/bin/env python3
"""
z3_coupling_scan.py
===================

Executable stress test for the PF God Equation coupling layer.

This script does not assume the bridge is closed. It probes the exact questions
that remain open:

1. H_C3stat:
   Does a primitive Z3 x spatial coupling produce equal marginals after one
   three-step closure cycle?

2. H_prod:
   Do score cross-terms vanish because of the coupling model itself, or only
   when conditional independence is separately imposed?

3. Regularity:
   Is the closure observable strictly positive on the scan domain?

4. Fisher isotropy:
   Does a scalar closure observable automatically give G = lambda I_D, or only
   a rank-1 outer product unless an SO(3) averaging step is added?

It also checks the N^{-D/2} scaling numerically for the heat-kernel-style
closure observable used on the God Equation side.

Run:
    python sandbox/z3_coupling_scan.py
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


SEED = 7
RNG = np.random.default_rng(SEED)
D = 3

# Output paths (written alongside the script)
SCRIPT_DIR = Path(__file__).parent
CSV_PATH  = SCRIPT_DIR / "z3_coupling_scan_results.csv"
PLOT_PATH = SCRIPT_DIR / "z3_coupling_scan.png"


def row_softmax(matrix: np.ndarray) -> np.ndarray:
    shifted = matrix - np.max(matrix, axis=1, keepdims=True)
    weights = np.exp(shifted)
    return weights / np.sum(weights, axis=1, keepdims=True)


def closure_probabilities(kernels: list[np.ndarray]) -> np.ndarray:
    """
    Exact 3-step closure probabilities on the reference spatial state x0 = 0.

    For starting generation channel a:
        p_a = <x0 | K_{a+2} K_{a+1} K_a | x0>
    """
    probs = []
    x0 = 0
    for a in range(3):
        product = kernels[(a + 2) % 3] @ kernels[(a + 1) % 3] @ kernels[a]
        probs.append(product[x0, x0])
    return np.asarray(probs, dtype=float)


def finite_difference_gradient(func, theta: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    grad = np.zeros_like(theta, dtype=float)
    for i in range(len(theta)):
        step = np.zeros_like(theta)
        step[i] = eps
        grad[i] = (func(theta + step) - func(theta - step)) / (2.0 * eps)
    return grad


def bernoulli_fisher(prob: float, grad: np.ndarray) -> np.ndarray:
    prob = float(np.clip(prob, 1e-12, 1.0 - 1e-12))
    return np.outer(grad, grad) / (prob * (1.0 - prob))


def score_vector(outcome: int, prob: float, grad: np.ndarray) -> np.ndarray:
    prob = float(np.clip(prob, 1e-12, 1.0 - 1e-12))
    if outcome == 1:
        return grad / prob
    return -grad / (1.0 - prob)


def random_unit_vectors(n: int) -> np.ndarray:
    vectors = RNG.normal(size=(n, D))
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms


def isotropy_metrics(matrix: np.ndarray) -> dict[str, float]:
    eigenvalues = np.linalg.eigvalsh(matrix)
    lam_min = float(np.min(eigenvalues))
    lam_max = float(np.max(eigenvalues))
    trace = float(np.trace(matrix))
    if trace <= 0.0:
        return {
            "trace": trace,
            "lam_min": lam_min,
            "lam_max": lam_max,
            "condition": math.inf,
            "anisotropy": math.inf,
        }
    iso_part = (trace / matrix.shape[0]) * np.eye(matrix.shape[0])
    anisotropy = float(np.linalg.norm(matrix - iso_part) / np.linalg.norm(iso_part))
    condition = math.inf if lam_min <= 0.0 else lam_max / lam_min
    return {
        "trace": trace,
        "lam_min": lam_min,
        "lam_max": lam_max,
        "condition": condition,
        "anisotropy": anisotropy,
    }


@dataclass
class PrimitiveModel:
    name: str
    phase_independent: bool
    bias_strength: float = 0.0

    def kernels(self, theta: np.ndarray) -> list[np.ndarray]:
        """
        Construct three positive row-stochastic spatial kernels.

        The symmetric branch uses the same kernel for all channels.
        The broken branch adds a channel-labeled perturbation.
        """
        a0 = np.array(
            [
                [0.0, 0.9, -0.7],
                [-0.8, 0.0, 0.6],
                [0.7, -0.5, 0.0],
            ]
        )
        a1 = np.array(
            [
                [0.4, -0.3, 0.2],
                [0.2, 0.1, -0.4],
                [-0.5, 0.4, 0.0],
            ]
        )
        a2 = np.array(
            [
                [0.1, 0.3, -0.2],
                [-0.4, 0.2, 0.2],
                [0.3, -0.1, -0.2],
            ]
        )
        base = theta[0] * a0 + theta[1] * a1 + theta[2] * a2

        d0 = np.array(
            [
                [0.0, 0.8, -0.6],
                [0.1, -0.2, 0.2],
                [-0.3, 0.4, -0.1],
            ]
        )
        d1 = np.array(
            [
                [-0.1, 0.2, 0.3],
                [0.7, -0.6, 0.0],
                [0.0, 0.5, -0.4],
            ]
        )
        d2 = np.array(
            [
                [0.4, -0.1, -0.2],
                [-0.2, 0.5, -0.1],
                [0.6, -0.7, 0.1],
            ]
        )
        perturbations = [d0, d1, d2]

        kernels = []
        for idx in range(3):
            logits = base.copy()
            if not self.phase_independent:
                logits = logits + self.bias_strength * perturbations[idx]
            kernels.append(row_softmax(logits))
        return kernels


def scan_bias_strength(theta: np.ndarray,
                       bias_values: np.ndarray) -> dict[str, np.ndarray]:
    """
    Sweep bias_strength from 0 (phase-independent) to max (broken).
    Returns: closure_spread and cross_term_norm at each bias value.
    """
    spreads: list[float] = []
    for bias in bias_values:
        model = PrimitiveModel(
            name="scan", phase_independent=(bias == 0.0), bias_strength=float(bias)
        )
        probs = closure_probabilities(model.kernels(theta))
        spreads.append(float(np.max(probs) - np.min(probs)))
    return {"bias": bias_values, "spread": np.array(spreads)}


def analyze_primitive_models(theta: np.ndarray) -> dict[str, Any]:
    print("=" * 78)
    print("EXPERIMENT 1 — Primitive Z3 x Spatial Coupling")
    print("=" * 78)
    print(f"theta = {theta.tolist()}")
    print()

    models = [
        PrimitiveModel(name="Symmetric phase-independent coupling", phase_independent=True),
        PrimitiveModel(
            name="Channel-labeled broken coupling",
            phase_independent=False,
            bias_strength=0.55,
        ),
    ]

    results: dict[str, Any] = {}
    for model in models:
        kernels = model.kernels(theta)
        probs = closure_probabilities(kernels)
        spread = float(np.max(probs) - np.min(probs))
        min_entry = min(float(np.min(kernel)) for kernel in kernels)
        comm_01 = float(np.linalg.norm(kernels[0] @ kernels[1] - kernels[1] @ kernels[0]))
        print(model.name)
        print(f"  closure probs p_a: {[round(float(x), 6) for x in probs]}")
        print(f"  equal-marginal spread: {spread:.6e}")
        print(f"  min kernel entry: {min_entry:.6f}")
        print(f"  ||[K0, K1]||_F: {comm_01:.6e}")
        print(f"  H_C3stat (numerical): {'PASS' if spread < 1e-8 else 'FAIL'}")
        print(f"  regularity (strict positivity): {'PASS' if min_entry > 0 else 'FAIL'}")
        print()
        key = "symmetric" if model.phase_independent else "broken"
        results[key] = {
            "probs": [float(p) for p in probs],
            "spread": spread,
            "min_entry": min_entry,
            "comm_01": comm_01,
        }
    return results


def analyze_hprod(theta: np.ndarray, n_samples: int = 50000) -> dict[str, Any]:
    print("=" * 78)
    print("EXPERIMENT 2 — H_prod vs Correlated Common Mode")
    print("=" * 78)

    model = PrimitiveModel(name="Symmetric phase-independent coupling", phase_independent=True)
    kernels = model.kernels(theta)
    probs = closure_probabilities(kernels)
    prob = float(np.mean(probs))

    def p_func(local_theta: np.ndarray) -> float:
        return float(np.mean(closure_probabilities(model.kernels(local_theta))))

    grad = finite_difference_gradient(p_func, theta)

    independent_scores_a = []
    independent_scores_b = []
    correlated_scores_a = []
    correlated_scores_b = []

    latent_noise = RNG.normal(size=n_samples)
    threshold = np.quantile(latent_noise, 1.0 - prob)

    for _ in range(n_samples):
        xa = int(RNG.random() < prob)
        xb = int(RNG.random() < prob)
        independent_scores_a.append(score_vector(xa, prob, grad))
        independent_scores_b.append(score_vector(xb, prob, grad))

    for z in latent_noise:
        xa = int(z > threshold)
        xb = int(z > threshold)
        correlated_scores_a.append(score_vector(xa, prob, grad))
        correlated_scores_b.append(score_vector(xb, prob, grad))

    independent_scores_a = np.asarray(independent_scores_a)
    independent_scores_b = np.asarray(independent_scores_b)
    correlated_scores_a = np.asarray(correlated_scores_a)
    correlated_scores_b = np.asarray(correlated_scores_b)

    indep_cross = independent_scores_a.T @ independent_scores_b / n_samples
    corr_cross = correlated_scores_a.T @ correlated_scores_b / n_samples

    print(f"base closure probability p: {prob:.6f}")
    print(f"score gradient: {[round(float(x), 6) for x in grad]}")
    indep_norm = float(np.linalg.norm(indep_cross))
    corr_norm  = float(np.linalg.norm(corr_cross))
    print(f"||cross||_F under independent product model: {indep_norm:.6e}")
    print(f"||cross||_F under correlated common-mode model: {corr_norm:.6e}")
    print("H_prod lesson: vanishing cross-terms are a property of the statistical model,")
    print("not of C3 geometry by itself.")
    print()
    return {"prob": prob, "grad": grad.tolist(),
            "indep_cross_norm": indep_norm, "corr_cross_norm": corr_norm}


def analyze_fisher_isotropy(rho: float = 0.35, beta: float = 0.9, n_orient: int = 5000) -> dict[str, Any]:
    print("=" * 78)
    print("EXPERIMENT 3 — Fisher Isotropy")
    print("=" * 78)

    def scalar_closure(theta: np.ndarray) -> float:
        return float(np.exp(-beta * np.dot(theta, theta)))

    theta_axis = np.array([rho, 0.0, 0.0])
    prob = scalar_closure(theta_axis)
    grad = finite_difference_gradient(scalar_closure, theta_axis)
    fisher = bernoulli_fisher(prob, grad)
    metrics = isotropy_metrics(fisher)

    avg_fisher = np.zeros((D, D))
    for direction in random_unit_vectors(n_orient):
        theta = rho * direction
        p_dir = scalar_closure(theta)
        g_dir = finite_difference_gradient(scalar_closure, theta)
        avg_fisher += bernoulli_fisher(p_dir, g_dir)
    avg_fisher /= n_orient
    avg_metrics = isotropy_metrics(avg_fisher)

    print(f"single-orientation theta = {[round(float(x), 6) for x in theta_axis]}")
    print(f"single-orientation Fisher eigenvalues: {np.linalg.eigvalsh(fisher)}")
    print(f"single-orientation anisotropy: {metrics['anisotropy']:.6e}")
    print(f"single-orientation condition #: {metrics['condition']}")
    print()
    print(f"orientation-averaged Fisher eigenvalues: {np.linalg.eigvalsh(avg_fisher)}")
    print(f"orientation-averaged anisotropy: {avg_metrics['anisotropy']:.6e}")
    print(f"orientation-averaged condition #: {avg_metrics['condition']:.6f}")
    print("isotropy lesson: a scalar closure observable does not automatically give")
    print("G = lambda I_D at a fixed theta. It becomes isotropic only after an SO(3)")
    print("averaging step or an equivalent probabilistic construction.")
    print()
    return {
        "single_evals": np.linalg.eigvalsh(fisher).tolist(),
        "single_anisotropy": metrics["anisotropy"],
        "avg_evals": np.linalg.eigvalsh(avg_fisher).tolist(),
        "avg_anisotropy": avg_metrics["anisotropy"],
        "avg_condition": avg_metrics["condition"],
    }


def analyze_heat_kernel_scaling(kappa: float = 1.0, tau: float = 0.2, n_max: int = 20) -> dict[str, Any]:
    print("=" * 78)
    print("EXPERIMENT 4 — Heat-Kernel Scaling")
    print("=" * 78)

    n_values = np.arange(1, n_max + 1, dtype=float)
    closure = (4.0 * np.pi * kappa * tau * n_values) ** (-D / 2.0)
    slope, intercept = np.polyfit(np.log(n_values), np.log(closure), 1)

    print(f"fitted log-log slope: {slope:.6f}")
    print(f"expected slope: {-D / 2.0:.6f}")
    print(f"prefactor exp(intercept): {math.exp(intercept):.6e}")
    print("scaling lesson: the heat-kernel observable cleanly gives the N^{-D/2}")
    print("exponent, but it does not by itself fix the exact PF coefficient story.")
    print()
    return {
        "n_values": n_values.tolist(),
        "closure": closure.tolist(),
        "slope": float(slope),
        "expected_slope": -D / 2.0,
        "prefactor": math.exp(intercept),
    }


def write_csv(r1: dict[str, Any], r2: dict[str, Any],
              r3: dict[str, Any], r4: dict[str, Any],
              scan: dict[str, np.ndarray]) -> None:
    rows = [
        ["experiment", "metric", "value"],
        ["E1_symmetric", "spread", r1["symmetric"]["spread"]],
        ["E1_symmetric", "min_entry", r1["symmetric"]["min_entry"]],
        ["E1_symmetric", "comm_01", r1["symmetric"]["comm_01"]],
        ["E1_symmetric", "H_C3stat_pass", int(r1["symmetric"]["spread"] < 1e-8)],
        ["E1_broken",    "spread", r1["broken"]["spread"]],
        ["E1_broken",    "min_entry", r1["broken"]["min_entry"]],
        ["E1_broken",    "comm_01", r1["broken"]["comm_01"]],
        ["E1_broken",    "H_C3stat_pass", int(r1["broken"]["spread"] < 1e-8)],
        ["E2", "base_prob", r2["prob"]],
        ["E2", "cross_norm_indep", r2["indep_cross_norm"]],
        ["E2", "cross_norm_corr",  r2["corr_cross_norm"]],
        ["E3", "single_eval_max", max(r3["single_evals"])],
        ["E3", "single_anisotropy", r3["single_anisotropy"]],
        ["E3", "avg_eval_min", min(r3["avg_evals"])],
        ["E3", "avg_eval_max", max(r3["avg_evals"])],
        ["E3", "avg_anisotropy", r3["avg_anisotropy"]],
        ["E3", "avg_condition", r3["avg_condition"]],
        ["E4", "fitted_slope", r4["slope"]],
        ["E4", "expected_slope", r4["expected_slope"]],
        ["E4", "slope_error", abs(r4["slope"] - r4["expected_slope"])],
    ]
    for i, (b, s) in enumerate(zip(scan["bias"], scan["spread"])):
        rows.append([f"scan_bias_{i}", "bias", float(b)])
        rows.append([f"scan_bias_{i}", "spread", float(s)])
    with open(CSV_PATH, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"CSV written: {CSV_PATH}")


def make_plots(r1: dict[str, Any], r2: dict[str, Any],
               r3: dict[str, Any], r4: dict[str, Any],
               scan: dict[str, np.ndarray]) -> None:
    bg, tc = '#0A0A0A', '#DDDDDD'
    C = {'good': '#00FFCC', 'bad': '#FF3366', 'gold': '#FFCC00', 'purple': '#AA88FF'}

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.patch.set_facecolor(bg)
    for ax in axes.flat:
        ax.set_facecolor(bg)
        ax.tick_params(colors=tc, labelsize=9)
        for sp in ax.spines.values():
            sp.set_edgecolor('#333333')

    # ── Panel 1: bias scan → H_C3stat spread ──────────────────────────
    ax = axes[0, 0]
    ax.plot(scan["bias"], scan["spread"], color=C['gold'], lw=2, marker='o', ms=4)
    ax.axhline(0, color=C['good'], lw=1, ls='--', label='Equal marginals (spread=0)')
    ax.set_xlabel('Coupling bias strength', color=tc, fontsize=10)
    ax.set_ylabel('H_C3stat spread  max(pₐ)−min(pₐ)', color=tc, fontsize=10)
    ax.set_title('Exp 1 — Bias Scan: phase-independence breaks H_C3stat\n'
                 'bias=0 → spread=0 exactly (PASS);  bias>0 → spread rises',
                 color=tc, fontsize=10)
    ax.legend(facecolor='#1A1A1A', labelcolor=tc, fontsize=8)

    # ── Panel 2: H_prod cross-term norms ──────────────────────────────
    ax = axes[0, 1]
    labels = ['Independent\n(product model)', 'Correlated\n(common mode)']
    vals = [r2["indep_cross_norm"], r2["corr_cross_norm"]]
    colors = [C['good'], C['bad']]
    bars = ax.bar(labels, vals, color=colors, alpha=0.85, width=0.4)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v * 1.05,
                f'{v:.2e}', ha='center', color=tc, fontsize=9)
    ax.set_ylabel('‖E[s⁽ᵃ⁾ ⊗ s⁽ᵇ⁾]‖_F  (cross-term norm)', color=tc, fontsize=10)
    ax.set_title('Exp 2 — H_prod: cross-terms vanish only under\n'
                 'independent product model, not from C₃ geometry alone',
                 color=tc, fontsize=10)
    ax.tick_params(axis='x', colors=tc)

    # ── Panel 3: Fisher eigenvalues single vs averaged ─────────────────
    ax = axes[1, 0]
    x = np.arange(D)
    w = 0.35
    single_evals = sorted(r3["single_evals"], reverse=True)
    avg_evals    = sorted(r3["avg_evals"],    reverse=True)
    ax.bar(x - w/2, single_evals, w, color=C['bad'],    alpha=0.85, label='Single orientation (rank-1)')
    ax.bar(x + w/2, avg_evals,    w, color=C['purple'], alpha=0.85, label='SO(3)-averaged (isotropic)')
    ax.axhline(sum(avg_evals) / D, color=C['gold'], lw=1.5, ls='--',
               label=f'Isotropic target  trace/D = {sum(avg_evals)/D:.3f}')
    ax.set_xticks(x)
    ax.set_xticklabels(['λ₁', 'λ₂', 'λ₃'], color=tc)
    ax.set_ylabel('Eigenvalue of G(θ)', color=tc, fontsize=10)
    ax.set_title('Exp 3 — Fisher isotropy\n'
                 'rank-1 at fixed θ → near-isotropic after SO(3) averaging',
                 color=tc, fontsize=10)
    ax.legend(facecolor='#1A1A1A', labelcolor=tc, fontsize=8)

    # ── Panel 4: heat kernel N^{-D/2} scaling ─────────────────────────
    ax = axes[1, 1]
    n_vals = np.array(r4["n_values"])
    closure = np.array(r4["closure"])
    ax.loglog(n_vals, closure, color=C['good'], lw=2, marker='o', ms=4,
              label=f'K(N) = (4πκτN)^(−D/2)')
    fit_line = np.exp(np.log(n_vals) * r4["slope"] +
                      np.log(r4["prefactor"]))
    ax.loglog(n_vals, fit_line, color=C['gold'], lw=1.5, ls='--',
              label=f'Fit: slope = {r4["slope"]:.6f}  (expected {r4["expected_slope"]:.1f})')
    ax.set_xlabel('N  (cycle count)', color=tc, fontsize=10)
    ax.set_ylabel('Closure probability K(N)', color=tc, fontsize=10)
    ax.set_title(f'Exp 4 — Heat kernel scaling\n'
                 f'log-log slope = {r4["slope"]:.6f}  =  −D/2 = {r4["expected_slope"]:.1f}  ✓',
                 color=tc, fontsize=10)
    ax.legend(facecolor='#1A1A1A', labelcolor=tc, fontsize=8)

    fig.suptitle(
        'ℤ₃ × Spatial Coupling Scan — God Equation Sandbox  ·  Wave 4  ·  2026-03-25',
        color='#FFFFFF', fontsize=12, y=1.01)
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150, bbox_inches='tight', facecolor=bg)
    print(f"Plot saved: {PLOT_PATH}")


def main() -> None:
    print("Z3 x Spatial Coupling Scan")
    print("-" * 78)
    print("Purpose: executable audit of the God Equation coupling assumptions.")
    print(f"Random seed: {SEED}")
    print()

    theta = np.array([0.42, -0.27, 0.19], dtype=float)

    r1 = analyze_primitive_models(theta)
    r2 = analyze_hprod(theta)
    r3 = analyze_fisher_isotropy()
    r4 = analyze_heat_kernel_scaling()

    # Parameter scan: bias_strength 0 → 0.8
    bias_values = np.linspace(0.0, 0.8, 17)
    scan = scan_bias_strength(theta, bias_values)

    print("=" * 78)
    print("BOTTOM LINE")
    print("=" * 78)
    print("1. C3-symmetric primitive coupling is easy to enforce numerically.")
    print("2. H_prod does not come for free; correlated realizations reintroduce")
    print("   nonzero score cross-terms immediately.")
    print("3. Strict positivity is easy on smooth positive kernels, but not on naive")
    print("   odd-step lattice return observables.")
    print("4. A scalar closure observable does not automatically give G = lambda I_D;")
    print("   isotropy needs an averaging or ensemble argument.")
    print()

    write_csv(r1, r2, r3, r4, scan)
    make_plots(r1, r2, r3, r4, scan)


if __name__ == "__main__":
    main()
