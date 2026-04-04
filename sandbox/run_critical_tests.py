#!/usr/bin/env python3
"""
Critical Tests Runner — Windows Console Safe

Convenience wrapper for a small local falsification pass.
This file is not a truth source and should not outrank the underlying
canonical scripts or the board docs:
  - koide_phase_scan.py
  - neutrino_koide_scan.py
  - spin_pair_classification.py
  - chiral_projection_z3.py

Use it for a compact console summary only.
"""
import numpy as np
from pathlib import Path

# Suppress matplotlib for now
import os
os.environ['MPLBACKEND'] = 'Agg'

print("=" * 70)
print("CRITICAL FALSIFICATION TESTS")
print("=" * 70)
print()

# ======================================================================
# TEST 1: Koide Phase delta = 2/9
# ======================================================================
print("TEST 1: Koide Phase Selection (delta_0 = 2/9?)")
print("-" * 70)

# PDG 2024 lepton masses (MeV)
M_E   = 0.51099895
M_MU  = 105.6583755
M_TAU = 1776.86

def reconstruct_masses(A, delta):
    k = np.array([0.0, 1.0, 2.0])
    sqm = A * (1.0 + np.sqrt(2.0) * np.cos(delta + 2.0 * np.pi * k / 3.0))
    return sqm ** 2

def rivero_phase(masses):
    """Find best-fit Rivero phase for mass triplet."""
    m = np.array(masses)
    m_bar = np.mean(m)
    
    def residual(delta):
        phases_k = 2.0 * np.pi * k / 3.0
        sm = np.sqrt(m_bar) * (1 + np.sqrt(2) * np.cos(phases_k + delta))
        m_pred = sm**2
        return np.sum((m - m_pred)**2)
    
    k = np.array([0.0, 1.0, 2.0])
    from scipy.optimize import minimize_scalar
    result = minimize_scalar(residual, bounds=(0, 2*np.pi), method='bounded')
    return result.x

# Calculate exact delta from PDG masses
lepton_masses = [M_E, M_MU, M_TAU]
delta_exact = rivero_phase(lepton_masses)
delta_2_9 = 2.0 / 9.0
delta_diff = abs(delta_exact - delta_2_9)
delta_pct = delta_diff / delta_2_9 * 100

print(f"  PDG 2024 charged leptons:")
print(f"    m_e  = {M_E:.6f} MeV")
print(f"    m_mu = {M_MU:.6f} MeV")
print(f"    m_tau = {M_TAU:.2f} MeV")
print()
print(f"  Results:")
print(f"    delta_exact = {delta_exact:.8f} rad")
print(f"    2/9         = {delta_2_9:.8f} rad")
print(f"    |delta - 2/9| = {delta_diff:.4e} rad ({delta_pct:.4f}%)")
print()

# Monte Carlo test: how special is this closeness?
rng = np.random.default_rng(42)
A_ref = np.sqrt(np.mean(lepton_masses))
mc_samples = []
batch = rng.uniform(0.0, 2.0 * np.pi, 2_000_000)
for s in batch:
    m = reconstruct_masses(A_ref, s)
    if m[0] > m[2] > m[1] > 0.0:  # m_tau > m_mu > m_e
        mc_samples.append(s)
    if len(mc_samples) >= 100_000:
        break

mc = np.array(mc_samples)
mc_d29 = np.abs(mc - 2.0 / 9.0)
frac_ref = float(np.mean(mc_d29 < delta_diff))

print(f"  Monte Carlo (100k valid samples):")
print(f"    Fraction as close to 2/9: {frac_ref:.4f}")
if frac_ref < 0.01:
    print(f"    -> SIGNIFICANT: delta is unusually close to 2/9 (p = {frac_ref:.4f})")
else:
    print(f"    -> delta is close to 2/9 at p={frac_ref:.4f}")
print()

# ======================================================================
# TEST 2: Neutrino Koide Universality
# ======================================================================
print("TEST 2: Neutrino Koide Universality")
print("-" * 70)

# PDG 2024 neutrino mass-squared differences
DM2_21 = 7.53e-5      # eV^2 solar
DM2_31_NO = 2.453e-3  # eV^2 atmospheric NO
DM2_32_IO = -2.546e-3 # eV^2 atmospheric IO
COSMO_BOUND = 0.12    # eV

def neutrino_masses_NO(m1_eV):
    m2 = np.sqrt(np.maximum(m1_eV**2 + DM2_21, 0.0))
    m3 = np.sqrt(np.maximum(m1_eV**2 + DM2_31_NO, 0.0))
    return m1_eV, m2, m3

def neutrino_masses_IO(m3_eV):
    m1 = np.sqrt(np.maximum(m3_eV**2 - DM2_32_IO, 0.0))
    m2 = np.sqrt(np.maximum(m3_eV**2 - DM2_32_IO + DM2_21, 0.0))
    return m1, m2, m3_eV

def koide_Q(masses):
    m = np.array(masses)
    if np.any(m < 0):
        return np.nan
    denom = np.sum(np.sqrt(m))**2
    if denom < 1e-30:
        return np.nan
    return np.sum(m) / denom

# Scan normal ordering
m1_scan = np.linspace(1e-4, 0.04, 2000)
Q_NO = []
for m1 in m1_scan:
    masses = neutrino_masses_NO(m1)
    if sum(masses) > COSMO_BOUND:
        break
    Q_NO.append(koide_Q(masses))

m1_scan = m1_scan[:len(Q_NO)]
Q_NO = np.array(Q_NO)

# Scan inverted ordering
m3_scan = np.linspace(1e-4, 0.04, 2000)
Q_IO = []
for m3 in m3_scan:
    masses = neutrino_masses_IO(m3)
    if sum(masses) > COSMO_BOUND:
        break
    Q_IO.append(koide_Q(masses))

m3_scan = m3_scan[:len(Q_IO)]
Q_IO = np.array(Q_IO)

print(f"  Normal Ordering (best Q):")
if len(Q_NO) > 0:
    idx_best_NO = np.argmin(np.abs(Q_NO - 2/3))
    print(f"    m1 = {m1_scan[idx_best_NO]:.5f} eV")
    print(f"    Q  = {Q_NO[idx_best_NO]:.6f}")
    print(f"    |Q - 2/3| = {abs(Q_NO[idx_best_NO] - 2/3):.2e}")
    print(f"    note: use neutrino_koide_scan.py for canonical phase / scan details")
    
    # Falsification check
    if abs(Q_NO[idx_best_NO] - 2/3) > 0.05:
        print(f"    -> FALSIFIED: |Q - 2/3| > 5% (neutrino Koide universality fails)")
    else:
        print(f"    -> CONSISTENT: |Q - 2/3| < 5%")
print()

print(f"  Inverted Ordering (best Q):")
if len(Q_IO) > 0:
    idx_best_IO = np.argmin(np.abs(Q_IO - 2/3))
    print(f"    m3 = {m3_scan[idx_best_IO]:.5f} eV")
    print(f"    Q  = {Q_IO[idx_best_IO]:.6f}")
    print(f"    |Q - 2/3| = {abs(Q_IO[idx_best_IO] - 2/3):.2e}")
    print(f"    note: use neutrino_koide_scan.py for canonical phase / scan details")
    
    if abs(Q_IO[idx_best_IO] - 2/3) > 0.05:
        print(f"    -> FALSIFIED: |Q - 2/3| > 5% (neutrino Koide universality fails)")
    else:
        print(f"    -> CONSISTENT: |Q - 2/3| < 5%")
print()

# ======================================================================
# TEST 3: Topological Weights (2,1) — Spin Classification
# ======================================================================
print("TEST 3: Topological Weights (2,1) - Spin Classification")
print("-" * 70)

def chi_at_z3_step(j):
    theta = 2.0 * np.pi / 3.0
    numerator = np.sin((2.0 * j + 1.0) * theta / 2.0)
    denominator = np.sin(theta / 2.0)
    value = numerator / denominator
    if abs(value) < 1e-12:
        return 0.0
    if abs(value - 1.0) < 1e-12:
        return 1.0
    if abs(value + 1.0) < 1e-12:
        return -1.0
    return value

print(f"  Low-spin classification at theta = 2pi/3:")
print(f"  {'j':>5}  {'C2=j(j+1)':>12}  {'chi_j(2pi/3)':>13}  {'class':>12}")
print("  " + "-" * 50)

survivors = []
annihilated = []

for n in range(17):
    j = n / 2.0
    c2 = j * (j + 1.0)
    chi = chi_at_z3_step(j)
    label = "annihilated" if chi == 0.0 else "survivor"
    print(f"  {str(j):>5}  {c2:12.2f}  {chi:13.1f}  {label:>12}")
    
    if chi == 0.0:
        annihilated.append(str(j))
    else:
        survivors.append(str(j))

print()
print(f"  Survivors: {', '.join(survivors[:8])}...")
print(f"  Annihilated: {', '.join(annihilated)}")
print()

# Key finding: j=0 survives, j=1 annihilated
print(f"  CRITICAL FINDING:")
print(f"    j=0 (scalar):     chi={chi_at_z3_step(0.0):.1f} -> SURVIVOR")
print(f"    j=0.5 (fermion):  chi={chi_at_z3_step(0.5):.1f} -> SURVIVOR")
print(f"    j=1 (boson):      chi={chi_at_z3_step(1.0):.1f} -> ANNIHILATED")
print()
print(f"    -> This contradicts the simple 'j=1 survives, j=0.5 annihilated' story")
print(f"    -> The chi=-1 sector (j=1.5, 2, etc.) is uninterpreted")
print()

# ======================================================================
# TEST 4: Chiral Projection Z3 — Path A Gap B
# ======================================================================
print("TEST 4: Chiral Projection Z3 - Path A Gap B")
print("-" * 70)

omega = np.exp(2j * np.pi / 3)

# S_bar: cyclic shift on Z3
S_bar = np.array([[0, 0, 1],
                  [1, 0, 0],
                  [0, 1, 0]], dtype=complex)

S_bar2 = S_bar @ S_bar

# Symmetric nearest-neighbor operator
T_symmetric = 0.5 * (S_bar + S_bar2)

print(f"  T_symmetric = (1/2)(S_bar + S_bar^2):")
print(np.round(T_symmetric.real, 4))
print()

# Compute T^3
T3_sym = T_symmetric @ T_symmetric @ T_symmetric
print(f"  T_symmetric^3:")
print(np.round(T3_sym.real, 4))
print()

# Check if diagonal
is_diagonal = np.allclose(T3_sym.imag, 0, atol=1e-12) and np.allclose(T3_sym.real - np.diag(np.diag(T3_sym.real)), 0, atol=1e-12)
print(f"  Is T^3 diagonal? {is_diagonal}")
if not is_diagonal:
    print(f"  -> GAP B NO-GO CONFIRMED: symmetric operator does NOT give diagonal T^3")
print()

# Chiral projection: kill k=2 mode
# DFT matrix
F = np.array([[omega**0, omega**0, omega**0],
              [omega**0, omega**(-1), omega**(-2)],
              [omega**0, omega**(-2), omega**(-4)]]) / np.sqrt(3)

# Projector onto k=0 and k=1
P_k0 = np.outer(F[:, 0], F[:, 0].conj())
P_k1 = np.outer(F[:, 1], F[:, 1].conj())
P_L = P_k0 + P_k1  # Left-handed projector

# Apply chiral projection
T_chiral = P_L @ T_symmetric @ P_L

# Compute T_chiral^3
T3_chiral = T_chiral @ T_chiral @ T_chiral

print(f"  T_chiral (projected onto k=0,1):")
print(np.round(T_chiral, 4))
print()

print(f"  T_chiral^3:")
print(np.round(T3_chiral, 4))
print()

# Check rank
rank = np.linalg.matrix_rank(T_chiral)
print(f"  Rank of T_chiral: {rank}")
print(f"  -> Chiral projection reduces rank from 3 to {rank}")
print()

# Check if T_chiral^3 is diagonal in the full space
is_diag_chiral = np.allclose(T3_chiral.imag, 0, atol=1e-12) and np.allclose(T3_chiral.real - np.diag(np.diag(T3_chiral.real)), 0, atol=1e-12)
print(f"  Is T_chiral^3 diagonal in full 3D space? {is_diag_chiral}")
if not is_diag_chiral:
    print(f"  -> PATH A GAP: Chiral projection does NOT close the Gap B no-go")
print()

# ======================================================================
# SUMMARY
# ======================================================================
print("=" * 70)
print("SUMMARY OF CRITICAL TESTS")
print("=" * 70)
print()
print(f"  TEST 1 (Koide Phase): delta = {delta_exact:.6f} rad")
print(f"    |delta - 2/9| = {delta_diff:.2e} ({delta_pct:.4f}%)")
print(f"    Monte Carlo p-value: {frac_ref:.4f}")
if frac_ref < 0.01:
    print(f"    -> delta is UNUSUALLY close to 2/9")
else:
    print(f"    -> delta is marginally close to 2/9")
print()

print(f"  TEST 2 (Neutrino Koide):")
if len(Q_NO) > 0:
    print(f"    Normal:  Q = {Q_NO[idx_best_NO]:.6f}, |Q-2/3| = {abs(Q_NO[idx_best_NO]-2/3):.2e}")
if len(Q_IO) > 0:
    print(f"    Inverted: Q = {Q_IO[idx_best_IO]:.6f}, |Q-2/3| = {abs(Q_IO[idx_best_IO]-2/3):.2e}")
print(f"    -> NEUTRINO KOIDE UNIVERSALITY: FALSIFIED (|Q-2/3| >> 5%)")
print()

print(f"  TEST 3 (Topological Weights):")
print(f"    j=0 -> SURVIVOR (chi=+1)")
print(f"    j=0.5 -> SURVIVOR (chi=+1)")
print(f"    j=1 -> ANNIHILATED (chi=0)")
print(f"    -> Simple 'fermion=boson' story NOT derived")
print(f"    -> chi=-1 sector uninterpreted")
print()

print(f"  TEST 4 (Chiral Projection):")
print(f"    T_symmetric^3 is NOT diagonal -> Gap B no-go holds")
print(f"    T_chiral has rank {rank} (not full rank)")
print(f"    T_chiral^3 is NOT diagonal in 3D space")
print(f"    -> Path A still needs Fourier-to-position-space bridge")
print()

print("=" * 70)
print("END OF CRITICAL TESTS")
print("=" * 70)
