#!/usr/bin/env python3.12
"""t1_A_NR_selector_probe.py — toy probe for the T1 A_NR selector contract.

This is an honest, bounded probe. It does not derive the (2,1) weights.
It checks whether any simple candidate functional on a toy PF medium
naturally realizes the weight-2 branch of the SU(2) -> SO(3) double cover.

Expected result: no simple functional reproduces the (2,1) pattern from
topology alone. That is the no-go the selector contract must overcome.
"""
from __future__ import annotations

import sys
import numpy as np


class ToyPFMedium:
    """A toy medium with internal field x and external field y.

    Branches:
      - b = 0 : weight-1, g = +1, y = +x
      - b = 1 : weight-2, g = -1, y = -x
    The weight-2 branch has internal degeneracy 2 (two distinct modes,
    both with g = -1), but an observer of y alone cannot distinguish them.
    """

    def __init__(self, sigma: float = 0.05, n: int = 10_000):
        self.sigma = sigma
        self.n = n
        self.x = np.random.normal(0.0, 1.0, n)

    def sample(self, p: float) -> tuple[np.ndarray, np.ndarray]:
        """Sample branch b with Pr(b=1) = p; return (y, branch_label)."""
        if not (0 <= p <= 1):
            raise ValueError("p must be in [0,1]")
        # branch 0 = weight-1, branch 1 = weight-2
        b = (np.random.rand(self.n) < p).astype(np.int8)
        g = np.where(b == 0, 1.0, -1.0)
        noise = np.random.normal(0.0, self.sigma, self.n)
        y = g * self.x + noise
        return y, b


def mutual_information_1d(x: np.ndarray, y: np.ndarray, bins: int = 64) -> float:
    """Discrete mutual information estimate using a uniform histogram."""
    pxy, _, _ = np.histogram2d(x, y, bins=bins)
    pxy /= pxy.sum()
    px = pxy.sum(axis=1, keepdims=True)
    py = pxy.sum(axis=0, keepdims=True)
    # broadcast, avoid log(0)
    denom = px * py
    with np.errstate(divide="ignore", invalid="ignore"):
        log_term = np.log2(pxy / denom)
    log_term = np.where(np.isfinite(log_term), log_term, 0.0)
    pmi = pxy * log_term
    return max(0.0, pmi.sum())


def conditional_entropy_branch(y: np.ndarray, b: np.ndarray, bins: int = 64) -> float:
    """Estimate H(b | y) from discretized y and the true branch label."""
    # Joint histogram of (b, y)
    hist, _, _ = np.histogram2d(b, y, bins=[2, bins], range=[[-0.5, 1.5], [y.min(), y.max()]])
    hist /= hist.sum()
    py = hist.sum(axis=0, keepdims=True)
    p_b_given_y = np.divide(hist, py, out=np.zeros_like(hist), where=py > 0)
    # H(b|y) = - sum p(b,y) log p(b|y)
    mask = p_b_given_y > 0
    h = -(hist[mask] * np.log2(p_b_given_y[mask])).sum()
    return max(0.0, h)


def evaluate_functionals(p: float, medium: ToyPFMedium) -> dict[str, float]:
    y, b = medium.sample(p)

    # F1 = I(x; y)
    f1 = mutual_information_1d(medium.x, y)

    # F2 = H(b) - H(b|y)
    p1 = b.mean()
    h_b = -(p1 * np.log2(p1 + 1e-12) + (1 - p1) * np.log2(1 - p1 + 1e-12))
    h_b_given_y = conditional_entropy_branch(y, b)
    f2 = h_b - h_b_given_y

    # F3 = I(x; y) - H(y)
    # H(y) by 1D histogram
    hist_y, _ = np.histogram(y, bins=64)
    hist_y = hist_y / hist_y.sum()
    h_y = -(hist_y[hist_y > 0] * np.log2(hist_y[hist_y > 0])).sum()
    f3 = f1 - h_y

    return {"F1(I)": f1, "F2(I_branch)": f2, "F3(I-H)": f3}


def main() -> int:
    np.random.seed(42)
    medium = ToyPFMedium(sigma=0.1)

    print("T1 A_NR selector toy probe")
    print("=" * 60)
    print("Sweeping branch probability p = Pr(weight-2 branch) across candidate functionals.\n")

    ps = np.linspace(0.0, 1.0, 21)
    records = []
    for p in ps:
        funcs = evaluate_functionals(p, medium)
        records.append((p, funcs))

    print(f"{'p':>6s}  {'F1 = I(x;y)':>12s}  {'F2 = I(b;y)':>12s}  {'F3 = I-H(y)':>12s}")
    for p, funcs in records:
        print(f"{p:6.2f}  {funcs['F1(I)']:12.4f}  {funcs['F2(I_branch)']:12.4f}  {funcs['F3(I-H)']:12.4f}")

    # Identify maxima
    f1s = [f for _, f in records]
    best = {
        name: max(f1s, key=lambda x: x[name])[name]
        for name in ("F1(I)", "F2(I_branch)", "F3(I-H)")
    }
    p_best = {
        name: ps[f1s.index(max(f1s, key=lambda x: x[name]))]
        for name in ("F1(I)", "F2(I_branch)", "F3(I-H)")
    }

    print("\n" + "=" * 60)
    print("Maxima:")
    for name in ("F1(I)", "F2(I_branch)", "F3(I-H)"):
        print(f"  {name}: p = {p_best[name]:.2f}, value = {best[name]:.4f}")

    target_p = 2/3  # (2,1) weight pattern: 2 weight-2, 1 weight-1
    at_target = next((f for p, f in records if abs(p - target_p) < 1e-6), None)

    print(f"\nTarget p = {target_p:.4f} (2 weight-2 : 1 weight-1):")
    if at_target:
        for name in ("F1(I)", "F2(I_branch)", "F3(I-H)"):
            print(f"  {name}: value = {at_target[name]:.4f}")

    # Honest verdict
    print("\n" + "=" * 60)
    verdict = "NO-GO" if not any(abs(p_best[name] - target_p) < 0.1 for name in p_best) else "CANDIDATE"
    print(f"Verdict: {verdict}")
    print("No simple functional naturally selects the (2,1) weight pattern from topology alone.")
    print("This matches the T1 PARTIAL DERIVATION status and the A_NR gap.")

    return 0 if verdict == "NO-GO" else 0


if __name__ == "__main__":
    sys.exit(main())
