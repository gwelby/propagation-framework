#!/usr/bin/env python3
"""Debug: What is the actual Koide phase for charged leptons?"""
import numpy as np
from scipy.optimize import minimize_scalar

# PDG 2024
M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86

print("PDG 2024 masses:")
print(f"  m_e  = {M_E:.6f} MeV")
print(f"  m_mu = {M_MU:.6f} MeV")
print(f"  m_tau = {M_TAU:.2f} MeV")
print()

# The Brannen/Rivero parametrization has AMBIGUITY in which k maps to which particle
# Standard assignment (k=0 -> tau, k=1 -> e, k=2 -> mu) gives delta ~ 0.2222 rad
# Let's verify this explicitly

def reconstruct_masses(A, delta, assignment='standard'):
    """
    sqrt(m_k) = A * (1 + sqrt(2) * cos(delta + 2*pi*k/3))
    
    Assignments:
      'standard': k=0->tau, k=1->e, k=2->mu (Rivero/Brannen convention)
      'reverse':  k=0->e, k=1->mu, k=2->tau
    """
    k = np.array([0.0, 1.0, 2.0])
    sqrt_m = A * (1.0 + np.sqrt(2.0) * np.cos(delta + 2.0 * np.pi * k / 3.0))
    
    if assignment == 'standard':
        # Returns [m_tau, m_e, m_mu]
        return sqrt_m**2
    elif assignment == 'reverse':
        # Returns [m_e, m_mu, m_tau]
        return sqrt_m**2
    else:
        raise ValueError(f"Unknown assignment: {assignment}")

def residual(delta, A, masses_target, assignment):
    """Residual sum of squares between reconstructed and target masses."""
    m_pred = reconstruct_masses(A, delta, assignment)
    return np.sum((np.array(masses_target) - m_pred)**2)

# The key: A is determined by the average mass
# m_bar = (m1 + m2 + m3) / 3
# A = sqrt(m_bar) approximately (but not exactly due to the cos terms)

# Let's scan delta and find the best fit for DIFFERENT assignments
print("=" * 70)
print("SCANNING DELTA FOR DIFFERENT ASSIGNMENTS")
print("=" * 70)

# Standard: [m_tau, m_e, m_mu]
masses_standard = [M_TAU, M_E, M_MU]
A_std = np.sqrt(np.mean(masses_standard))

print(f"\nStandard assignment (k=0->tau, k=1->e, k=2->mu):")
print(f"  Target: [{M_TAU:.2f}, {M_E:.6f}, {M_MU:.6f}]")
print(f"  A = {A_std:.2f}")

result = minimize_scalar(
    lambda d: residual(d, A_std, masses_standard, 'standard'),
    bounds=(0, 2*np.pi),
    method='bounded'
)
delta_std = result.x
m_pred = reconstruct_masses(A_std, delta_std, 'standard')
print(f"  Best delta = {delta_std:.8f} rad ({delta_std*180/np.pi:.2f} deg)")
print(f"  Predicted: [{m_pred[0]:.2f}, {m_pred[1]:.6f}, {m_pred[2]:.6f}]")
print(f"  Residual = {result.fun:.2e}")

# Check 2/9
delta_2_9 = 2.0/9.0
res_2_9 = residual(delta_2_9, A_std, masses_standard, 'standard')
print(f"  At delta=2/9: residual = {res_2_9:.2e}")
print(f"  |delta_std - 2/9| = {abs(delta_std - 2/9):.2e} rad")

# Reverse: [m_e, m_mu, m_tau]
masses_reverse = [M_E, M_MU, M_TAU]
A_rev = np.sqrt(np.mean(masses_reverse))

print(f"\nReverse assignment (k=0->e, k=1->mu, k=2->tau):")
print(f"  Target: [{M_E:.6f}, {M_MU:.6f}, {M_TAU:.2f}]")

result = minimize_scalar(
    lambda d: residual(d, A_rev, masses_reverse, 'reverse'),
    bounds=(0, 2*np.pi),
    method='bounded'
)
delta_rev = result.x
m_pred = reconstruct_masses(A_rev, delta_rev, 'reverse')
print(f"  Best delta = {delta_rev:.8f} rad ({delta_rev*180/np.pi:.2f} deg)")
print(f"  Predicted: [{m_pred[0]:.6f}, {m_pred[1]:.6f}, {m_pred[2]:.2f}]")
print(f"  Residual = {result.fun:.2e}")

# Try cyclic permutations
print("\n" + "=" * 70)
print("TRYING ALL 6 PERMUTATIONS")
print("=" * 70)

from itertools import permutations

base_masses = [M_E, M_MU, M_TAU]
best_overall = None
best_perm = None
best_delta = None

for i, perm in enumerate(permutations([0, 1, 2])):
    masses_perm = [base_masses[perm[0]], base_masses[perm[1]], base_masses[perm[2]]]
    A_perm = np.sqrt(np.mean(masses_perm))
    
    result = minimize_scalar(
        lambda d: residual(d, A_perm, masses_perm, 'standard'),
        bounds=(0, 2*np.pi),
        method='bounded'
    )
    
    print(f"\nPermutation {i}: k=0->perm[{perm[0]}], k=1->perm[{perm[1]}], k=2->perm[{perm[2]}]")
    print(f"  Target: [{masses_perm[0]:.6f}, {masses_perm[1]:.6f}, {masses_perm[2]:.2f}]")
    print(f"  Best delta = {result.x:.8f} rad")
    print(f"  Residual = {result.fun:.2e}")
    
    if best_overall is None or result.fun < best_overall:
        best_overall = result.fun
        best_perm = perm
        best_delta = result.x

print(f"\nBEST PERMUTATION: {best_perm}")
print(f"  delta = {best_delta:.8f} rad")
print(f"  residual = {best_overall:.2e}")

# The Foot parametrization uses a DIFFERENT convention
print("\n" + "=" * 70)
print("FOOT PARAMETRIZATION (standard in literature)")
print("=" * 70)

# Foot (1994): sqrt(m_k) = A * (1 + sqrt(2) * cos(2*pi*k/3 + delta))
# with k=0->e, k=1->mu, k=2->tau
# This is equivalent to delta_Foot = -delta_Rivero (mod 2pi/3)

def foot_masses(A, delta):
    """Foot parametrization: k=0->e, k=1->mu, k=2->tau"""
    k = np.array([0.0, 1.0, 2.0])
    sqrt_m = A * (1.0 + np.sqrt(2.0) * np.cos(2.0 * np.pi * k / 3.0 + delta))
    return sqrt_m**2

def foot_residual(delta, A):
    m_pred = foot_masses(A, delta)
    target = np.array([M_E, M_MU, M_TAU])
    return np.sum((target - m_pred)**2)

A_foot = np.sqrt(np.mean([M_E, M_MU, M_TAU]))

result = minimize_scalar(
    lambda d: foot_residual(d, A_foot),
    bounds=(0, 2*np.pi),
    method='bounded'
)
delta_foot = result.x
m_pred = foot_masses(A_foot, delta_foot)

print(f"  Best delta_Foot = {delta_foot:.8f} rad ({delta_foot*180/np.pi:.2f} deg)")
print(f"  Predicted: m_e={m_pred[0]:.6f}, m_mu={m_pred[1]:.6f}, m_tau={m_pred[2]:.2f}")
print(f"  Residual = {result.fun:.2e}")
print(f"  |delta_Foot - 2/9| = {abs(delta_foot - 2/9):.2e} rad")

# Check if delta_foot is close to pi - 2/9 or similar
print(f"\n  delta_Foot relations:")
print(f"    2*pi - delta_Foot = {2*np.pi - delta_foot:.8f} rad")
print(f"    pi - delta_Foot   = {np.pi - delta_foot:.8f} rad")
print(f"    pi/2 - delta_Foot = {np.pi/2 - delta_foot:.8f} rad")
