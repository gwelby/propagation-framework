"""
T-006: Verify Koide formula using PDG 2024 pole masses
"""
import math

# PDG 2024 pole masses (MeV)
me  = 0.51099895       # electron
mmu = 105.6583755      # muon
mta = 1776.86          # tau

# Koide Q
sqrt_sum = math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mta)
mass_sum = me + mmu + mta
Q = mass_sum / (sqrt_sum ** 2)

deviation_pct = abs(Q - 2/3) / (2/3) * 100

print("=" * 50)
print("  Koide Formula — PDG 2024 Pole Masses")
print("=" * 50)
print(f"  m_e   = {me:.8f} MeV")
print(f"  m_μ   = {mmu:.7f} MeV")
print(f"  m_τ   = {mta:.2f} MeV")
print()
print(f"  Q     = {Q:.10f}")
print(f"  2/3   = {2/3:.10f}")
print(f"  Δ     = {Q - 2/3:.2e}")
print(f"  Dev   = {deviation_pct:.6f}%")
print()
print(f"  Status: {'CONFIRMED' if deviation_pct < 0.01 else 'DEVIATION'}")

# Brannen neutrino prediction
print()
print("=" * 50)
print("  Brannen Neutrino Mass Prediction (Koide extended)")
print("=" * 50)
# Normal ordering, Brannen 2006
m1 = 0.000383  # eV
m2 = 0.00868
m3 = 0.0502
sqrt_sum_nu = math.sqrt(m1) + math.sqrt(m2) + math.sqrt(m3)
Q_nu = (m1 + m2 + m3) / (sqrt_sum_nu ** 2)
print(f"  m1 = {m1:.5f} eV, m2 = {m2:.5f} eV, m3 = {m3:.5f} eV")
print(f"  Q_ν = {Q_nu:.6f}  (predict 2/3 = {2/3:.6f})")
print(f"  Δ_ν = {Q_nu - 2/3:.4f}  (JUNO will test this)")
print()
print("  Note: JUNO expected 2026 — first direct test of neutrino Koide")
