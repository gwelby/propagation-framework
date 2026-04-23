#!/usr/bin/env python3
"""Verify the Koide phase extraction using the EXACT formula from koide_phase_scan.py"""
import numpy as np

# PDG 2024
M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86

print("PDG 2024 masses:")
print(f"  m_e  = {M_E:.8f} MeV")
print(f"  m_mu = {M_MU:.8f} MeV")
print(f"  m_tau = {M_TAU:.8f} MeV")
print()

# The EXACT extraction formula from koide_phase_scan.py
def extract_A_delta(m_k0, m_k1, m_k2):
    """
    From sqrt(m_k) = A(1 + sqrt(2) cos(delta + 2pi*k/3)):
      A = mean(sqrt(m_k))
      exp(i*delta) is proportional to DFT at frequency 1
    """
    s = np.array([np.sqrt(m_k0), np.sqrt(m_k1), np.sqrt(m_k2)])
    A = s.mean()
    omega = np.exp(2j * np.pi / 3.0)
    # Fourier mode at k=1 uses exp(-i*2pi*k/3) = conj(omega)^k
    c = s[0] * 1.0 + s[1] * np.conj(omega) + s[2] * np.conj(omega) ** 2
    return A, float(np.angle(c)) % (2.0 * np.pi)

def reconstruct_masses(A, delta):
    """Reconstruct masses from A and delta."""
    k = np.array([0.0, 1.0, 2.0])
    sqm = A * (1.0 + np.sqrt(2.0) * np.cos(delta + 2.0 * np.pi * k / 3.0))
    return sqm ** 2

# Key assignment: k=(tau=0, e=1, mu=2)
# This is the Rivero/Brannen convention that gives delta ~ 0.2222 rad
print("=" * 70)
print("EXTRACTION WITH k=(tau=0, e=1, mu=2)")
print("=" * 70)

A, delta = extract_A_delta(M_TAU, M_E, M_MU)

print(f"\nExtracted parameters:")
print(f"  A     = {A:.12f} MeV^(1/2)")
print(f"  delta = {delta:.12f} rad  ({delta*180/np.pi:.4f} deg)")
print(f"  2/9   = {2/9:.12f} rad")
print(f"  |delta - 2/9| = {abs(delta - 2/9):.4e} rad  ({abs(delta-2/9)/(2/9)*100:.4f}%)")

# Reconstruction check
m_rec = reconstruct_masses(A, delta)
print(f"\nReconstruction check:")
print(f"  m_tau(rec) = {m_rec[0]:.8f}   PDG = {M_TAU:.8f}   diff = {m_rec[0]-M_TAU:+.3e}")
print(f"  m_e(rec)   = {m_rec[1]:.8f}   PDG = {M_E:.8f}     diff = {m_rec[1]-M_E:+.3e}")
print(f"  m_mu(rec)  = {m_rec[2]:.8f}   PDG = {M_MU:.8f}    diff = {m_rec[2]-M_MU:+.3e}")

# Koide Q check
def koide_Q(m0, m1, m2):
    ms = np.array([m0, m1, m2], dtype=float)
    return ms.sum() / np.sum(np.sqrt(np.abs(ms))) ** 2

Q_val = koide_Q(*m_rec)
print(f"\nKoide Q check:")
print(f"  Q(rec)    = {Q_val:.15f}")
print(f"  2/3       = {2/3:.15f}")
print(f"  |Q - 2/3| = {abs(Q_val - 2/3):.2e}")

import truth_audit_bridge
audit_result = truth_audit_bridge.audit_claim("Koide Q=2/3", Q_val)
print(audit_result)

# Now let's also check the sqrt(m) values directly
print("\n" + "=" * 70)
print("DIRECT sqrt(m) CHECK")
print("=" * 70)

sqrt_m_tau = np.sqrt(M_TAU)
sqrt_m_e = np.sqrt(M_E)
sqrt_m_mu = np.sqrt(M_MU)

print(f"\nsqrt(mass) values:")
print(f"  sqrt(m_tau) = {sqrt_m_tau:.8f}")
print(f"  sqrt(m_e)   = {sqrt_m_e:.8f}")
print(f"  sqrt(m_mu)  = {sqrt_m_mu:.8f}")

A_direct = (sqrt_m_tau + sqrt_m_e + sqrt_m_mu) / 3
print(f"\nA = (sqrt(m_tau) + sqrt(m_e) + sqrt(m_mu)) / 3 = {A_direct:.8f}")

# Now solve for delta from the parametrization
# sqrt(m_k) = A * (1 + sqrt(2) * cos(delta + 2*pi*k/3))
# For k=0: sqrt(m_tau) = A * (1 + sqrt(2) * cos(delta))
# => cos(delta) = (sqrt(m_tau)/A - 1) / sqrt(2)

cos_delta = (sqrt_m_tau / A_direct - 1) / np.sqrt(2)
print(f"\ncos(delta) from k=0 (tau):")
print(f"  cos(delta) = ({sqrt_m_tau:.8f} / {A_direct:.8f} - 1) / sqrt(2) = {cos_delta:.8f}")

# Check if cos_delta is in valid range
if abs(cos_delta) <= 1:
    delta_from_tau = np.arccos(cos_delta)
    print(f"  delta = arccos({cos_delta:.8f}) = {delta_from_tau:.8f} rad")
else:
    print(f"  ERROR: cos(delta) = {cos_delta:.8f} is outside [-1, 1]!")
    print(f"  This means the parametrization doesn't fit exactly!")

# Let's check all three equations
print("\n" + "=" * 70)
print("CONSISTENCY CHECK: All three k values")
print("=" * 70)

for k, mass, name in [(0, M_TAU, 'tau'), (1, M_E, 'e'), (2, M_MU, 'mu')]:
    sqrt_m = np.sqrt(mass)
    # sqrt(m_k) = A * (1 + sqrt(2) * cos(delta + 2*pi*k/3))
    # => cos(delta + 2*pi*k/3) = (sqrt(m_k)/A - 1) / sqrt(2)
    cos_arg = (sqrt_m / A_direct - 1) / np.sqrt(2)
    print(f"\nk={k} ({name}):")
    print(f"  sqrt(m) = {sqrt_m:.8f}")
    print(f"  cos(delta + 2*pi*{k}/3) = {cos_arg:.8f}")
    if abs(cos_arg) <= 1:
        arg = np.arccos(cos_arg)
        print(f"  delta + 2*pi*{k}/3 = +/- {arg:.8f} rad")
