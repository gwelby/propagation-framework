#!/usr/bin/env python3
"""
O2bis: CPTP Channel — No-Selection Control

Kraus completion: U(a) has eigenvalues {1, λ, λ}, λ=(3a-1)/2.
K(a) = √(1-λ²)·Q guarantees U†U + K†K = I.

Result: Φ_a(P₀) = P₀ and Φ_a(Q) = Q for all a. The channel preserves
the P₀ population identically across all a. Under symmetric dephasing,
the exact fidelity is constant (~0.9518 for noise=0.05, 30 steps).
This is a no-selection control — no a=0 advantage exists in this model.

2026-07-29 — DeepSeek ∇²⬡ — corrected per Fundamentals audit
"""

import numpy as np

I3 = np.eye(3, dtype=complex)
v0 = np.ones(3, dtype=complex) / np.sqrt(3)
P0 = np.outer(v0, v0.conj())
Q = I3 - P0

def step_operator(a):
    M = np.array([[0,1,1],[1,0,1],[1,1,0]], dtype=complex)
    b = (1 - a) / 2
    return a * I3 + b * M

def kraus_k(a):
    """Analytic K(a) = √(1-λ²)·Q, with λ = (3a-1)/2."""
    lam = (3*a - 1) / 2
    k_norm = np.sqrt(max(0.0, 1.0 - lam**2))
    return k_norm * Q

def dephasing(rho, noise_std):
    """Exact symmetric dephasing: off-diagonals decay by exp(-sigma²)."""
    if noise_std == 0:
        return rho.copy()
    decay = np.exp(-noise_std**2)
    result = rho.copy() * decay
    for i in range(3):
        result[i, i] = rho[i, i]
    return result

def channel_step(rho, a, noise_std):
    rho_d = dephasing(rho, noise_std)
    U = step_operator(a)
    K = kraus_k(a)
    return U @ rho_d @ U.conj().T + K @ rho_d @ K.conj().T

def fidelity(rho):
    return np.real(v0.conj() @ rho @ v0)

def simulate(a, n_steps=30, noise_std=0.05):
    """Exact deterministic channel propagation, no sampling."""
    rho = P0.copy()
    for _ in range(n_steps):
        rho = channel_step(rho, a, noise_std)
        rho = (rho + rho.conj().T) / 2
    return fidelity(rho)

if __name__ == "__main__":
    print("=" * 64)
    print("O2bis: CPTP CHANNEL — No-Selection Control")
    print("=" * 64)

    print("\nChannel verification (||U†U + K†K - I||):")
    for a in [0.0, 0.3, 0.5, 0.8, 1.0]:
        U = step_operator(a)
        K = kraus_k(a)
        r = np.linalg.norm(U.conj().T @ U + K.conj().T @ K - I3)
        print(f"  a={a:.1f}: {r:.2e}")

    print(f"\n  Algebra: Φ_a(P₀)=P₀, Φ_a(Q)=Q for all a.")
    print(f"  Channel damps P₀-Q coherence but preserves populations.")
    print(f"  Under symmetric dephasing, fidelity is constant across a.\n")

    print(f"Probe (30 steps, exact symmetric dephasing, noise=0.05):")
    print(f"  {'a':>6} {'F_N':>10}")
    print(f"  {'-'*6} {'-'*10}")

    fids = []
    for a in np.linspace(0, 1, 11):
        fid = simulate(a, n_steps=30, noise_std=0.05)
        fids.append(fid)
        print(f"  {a:>6.1f} {fid:>10.4f}")

    spread = max(fids) - min(fids)
    print(f"\n  Spread across a: {spread:.3e}")
    print(f"  All values cluster near ~0.9518 (analytic constant).")
    print(f"  Differences are numerical round-off, not physical selection.")

    # Noise sweep
    print(f"\nNoise sweep (confirms no selection at any noise level):")
    for ns in [0.01, 0.03, 0.05, 0.1]:
        f0 = simulate(0.0, n_steps=30, noise_std=ns)
        f05 = simulate(0.5, n_steps=30, noise_std=ns)
        print(f"  ns={ns:.2f}  a0={f0:.4f}  a05={f05:.4f}  Δ={abs(f0-f05):.4f}")

    print(f"\n{'='*64}")
    print("CONCLUSION: No selection of a=0 in the CPTP channel model.")
    print("  This is a negative control — strong evidence against the")
    print("  simplest open-system completion producing an a=0 preference.")
    print("  ")
    print("  The 52.7× postselection ratio (May 29 v2 probe) remains a")
    print("  model-internal statistic. A physical selection mechanism")
    print("  has not been established.")
    print("=" * 64)
