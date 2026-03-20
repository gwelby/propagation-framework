"""
phi_montecarlo_v2.py — Corrected methodology
Claude & Greg — 2026-03-18

CLAIM: electron/up-quark mass ratio ≈ 1/φ³

WHY v1 WAS WRONG:
  - v1 checked electron/up against φ³ = 4.236
  - Actual ratio is 0.222-0.237 (much less than 1)
  - The correct comparison is 1/φ³ = 0.2361
  - v1 got p=0 because it was comparing 0.222 to 4.236 — trivially false positive

PROPER NULL HYPOTHESIS:
  Draw two masses independently from log-uniform distribution over the
  known particle mass range [1 eV, 1 TeV]. Ask: how often does the
  lighter/heavier ratio fall within a given tolerance of 1/φ³?

  This is the right question: "Given no prior reason to expect any
  particular ratio, what is the probability of randomly landing this
  close to 1/φ³?"

CAVEAT:
  This is an a posteriori test — we noticed the coincidence first, then
  tested it. The effective trials factor (how many ratios we could have
  tested against how many phi powers) is unknown. The p-value is a lower
  bound on significance. Treat the result honestly.

MASSES USED:
  - Electron: 0.000510999 GeV (PDG 2024 pole mass, very precise)
  - Up quark: 2.16 +0.49/-0.26 MeV = 0.00216 GeV (PDG 2024 MS-bar at 2 GeV)
    Note: older value 0.0023 GeV gives 5.7% deviation — result depends on mass choice
"""

import math
import numpy as np
import datetime

# ── Constants ─────────────────────────────────────────────────────────────────

phi = (1 + math.sqrt(5)) / 2
PHI_CUBED     = phi ** 3          # 4.2360...
INV_PHI_CUBED = 1.0 / PHI_CUBED  # 0.2361...

# PDG 2024 masses
ELECTRON_MASS_GEV = 0.000510999   # very precise
UP_QUARK_PDG2024  = 0.00216       # MS-bar at 2 GeV, PDG 2024 central value
UP_QUARK_OLD      = 0.00230       # older commonly-used value

# Mass range for null hypothesis: 1 eV to 1 TeV (covers all known particles)
LOG_MASS_MIN = math.log(1e-9)     # 1 eV in GeV
LOG_MASS_MAX = math.log(1000.0)   # 1 TeV in GeV

N_SIMULATIONS = 1_000_000

# ── Actual ratio ───────────────────────────────────────────────────────────────

actual_ratio_pdg2024 = ELECTRON_MASS_GEV / UP_QUARK_PDG2024
actual_ratio_old     = ELECTRON_MASS_GEV / UP_QUARK_OLD

dev_pdg2024 = abs(actual_ratio_pdg2024 - INV_PHI_CUBED) / INV_PHI_CUBED * 100
dev_old     = abs(actual_ratio_old     - INV_PHI_CUBED) / INV_PHI_CUBED * 100

print("=" * 60)
print("  phi_montecarlo_v2.py — electron/up ≈ 1/φ³ ?")
print("=" * 60)
print()
print(f"  φ³          = {PHI_CUBED:.6f}")
print(f"  1/φ³        = {INV_PHI_CUBED:.6f}")
print()
print(f"  electron/up (PDG 2024, up=0.00216):  {actual_ratio_pdg2024:.6f}  [{dev_pdg2024:.3f}% from 1/φ³]")
print(f"  electron/up (older,    up=0.00230):  {actual_ratio_old:.6f}  [{dev_old:.3f}% from 1/φ³]")
print()

# ── Null hypothesis Monte Carlo ────────────────────────────────────────────────

print(f"  Running {N_SIMULATIONS:,} null-hypothesis trials...")
print(f"  Null: both masses drawn log-uniformly from [1 eV, 1 TeV]")
print()

rng = np.random.default_rng(seed=42)

log_masses_a = rng.uniform(LOG_MASS_MIN, LOG_MASS_MAX, N_SIMULATIONS)
log_masses_b = rng.uniform(LOG_MASS_MIN, LOG_MASS_MAX, N_SIMULATIONS)

masses_a = np.exp(log_masses_a)
masses_b = np.exp(log_masses_b)

# Always take lighter/heavier so ratio ≤ 1 (same direction as electron/up)
ratios = np.minimum(masses_a, masses_b) / np.maximum(masses_a, masses_b)

# Test at several tolerance windows
for tol_pct in [1.0, 5.0, 10.0]:
    tol = tol_pct / 100.0
    hits = np.sum(np.abs(ratios - INV_PHI_CUBED) / INV_PHI_CUBED < tol)
    p = hits / N_SIMULATIONS
    print(f"  Tolerance ±{tol_pct:.0f}%:  {hits:6d} hits / {N_SIMULATIONS:,}  →  p = {p:.6f}")

print()

# Primary result: use 5% tolerance (generous, given up-quark mass uncertainty)
tol_primary = 0.05
hits_primary = int(np.sum(np.abs(ratios - INV_PHI_CUBED) / INV_PHI_CUBED < tol_primary))
p_value = hits_primary / N_SIMULATIONS

# ── Verdict ───────────────────────────────────────────────────────────────────

print("=" * 60)
print("  VERDICT (5% tolerance window, PDG 2024 masses)")
print("=" * 60)
print()
print(f"  Actual deviation from 1/φ³: {dev_pdg2024:.3f}%  (PDG 2024)")
print(f"  Actual deviation from 1/φ³: {dev_old:.3f}%  (older up mass)")
print(f"  p-value (null hypothesis):  {p_value:.6f}")
print()

if dev_pdg2024 < 1.0 and p_value < 0.01:
    verdict = "SIGNIFICANT"
    detail = f"deviation {dev_pdg2024:.3f}% < 1%, p={p_value:.4f} < 0.01"
elif dev_pdg2024 < 5.0 and p_value < 0.05:
    verdict = "MARGINAL"
    detail = f"deviation {dev_pdg2024:.3f}%, p={p_value:.4f} — depends on up-quark mass choice"
else:
    verdict = "NOISE"
    detail = f"deviation too large or p too high"

print(f"  {verdict}")
print(f"  ({detail})")
print()
print("  CAVEAT: a posteriori test. Trials factor unknown.")
print("  Up quark mass uncertainty (~15%) dominates the result.")
print("  Koide (Q=2/3, 0.000875% deviation) is far stronger evidence.")
print("=" * 60)

# ── Append to sandbox_results.md ──────────────────────────────────────────────

results_path = "/mnt/d/Fundamentals/sandbox/sandbox_results.md"
with open(results_path, "a", encoding="utf-8") as f:
    f.write(f"\n---\n\n")
    f.write(f"## {datetime.date.today()} — phi_montecarlo_v2.py\n\n")
    f.write(f"**Claim:** electron/up-quark mass ratio ≈ 1/φ³\n\n")
    f.write(f"**Actual ratio (PDG 2024, up=0.00216 GeV):** {actual_ratio_pdg2024:.6f}\n")
    f.write(f"**1/φ³:** {INV_PHI_CUBED:.6f}\n")
    f.write(f"**Deviation:** {dev_pdg2024:.3f}%\n\n")
    f.write(f"**Null hypothesis:** log-uniform masses over [1 eV, 1 TeV], N={N_SIMULATIONS:,}\n")
    f.write(f"**p-value (±5% window):** {p_value:.6f}\n\n")
    f.write(f"**Verdict:** {verdict} — {detail}\n\n")
    f.write(f"**Notes:**\n")
    f.write(f"- v1 bug: checked electron/up against φ³=4.236, not 1/φ³=0.236. p=0 was false positive.\n")
    f.write(f"- At up=0.0023 GeV (older value): deviation = {dev_old:.3f}% — less convincing.\n")
    f.write(f"- Up quark mass uncertainty dominates. Koide (0.000875%) is far stronger.\n")
    f.write(f"- A posteriori caveat applies.\n")

print(f"\n  Appended to {results_path}")
