"""
neutrino_koide_scan.py
======================
Scan over the lightest neutrino mass (m1 in normal ordering, m3 in inverted)
and ask: does the Koide relation Q = 2/3 hold for neutrinos? And if so, at
what phase δ does it lock — the same as charged leptons (δ_lepton), the quark
anchor (π/4), the 2/9 candidate, or something distinct?

PDG 2024 mass-squared differences (normal ordering):
  Δm²_21 =  7.53 × 10⁻⁵ eV²  (solar)
  Δm²_31 =  2.453 × 10⁻³ eV²  (atmospheric)

Inverted ordering:
  Δm²_32 = -2.546 × 10⁻³ eV²  (atmospheric IH)

Cosmological bound: Σ mν < 0.12 eV (Planck 2018)

Rivero–Gsponer parameterisation:
  √m_k = √m̄ · (1 + √2 · cos(2πk/3 + δ))  for k = 0, 1, 2
  Q = 2/3 is automatic if and only if the masses fit this ansatz.
  We scan δ over [0, π] for each m1 and find the best-fit phase.

Outputs: neutrino_koide_scan.png
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import minimize_scalar, brentq

# ── PDG 2024 values ──────────────────────────────────────────────────────────

DM2_21 = 7.53e-5     # eV²  solar
DM2_31_NO = 2.453e-3  # eV²  atmospheric, normal ordering  (m3 > m1)
DM2_32_IO = -2.546e-3 # eV²  atmospheric, inverted ordering (m3 < m1)

COSMO_SUM_BOUND = 0.12  # eV

# Known Koide phases from the charged sector
DELTA_CHARGED_LEPTON = 0.2223   # rad — from PDG e/mu/tau masses
DELTA_DOWN_QUARK     = np.pi/4  # rad — Rivero anchor for down-type quarks
DELTA_2_OVER_9       = 2.0/9.0  # rad — the 2/9 candidate

# ── Build mass triplets ──────────────────────────────────────────────────────

def neutrino_masses_NO(m1_eV):
    """Normal ordering: m1 < m2 < m3."""
    m2 = np.sqrt(np.maximum(m1_eV**2 + DM2_21, 0.0))
    m3 = np.sqrt(np.maximum(m1_eV**2 + DM2_31_NO, 0.0))
    return m1_eV, m2, m3

def neutrino_masses_IO(m3_eV):
    """Inverted ordering: m3 < m1 < m2."""
    m1 = np.sqrt(np.maximum(m3_eV**2 - DM2_32_IO, 0.0))
    m2 = np.sqrt(np.maximum(m3_eV**2 - DM2_32_IO + DM2_21, 0.0))
    return m1, m2, m3_eV

# ── Koide quantities ─────────────────────────────────────────────────────────

def koide_Q(masses):
    m = np.array(masses)
    if np.any(m < 0):
        return np.nan
    denom = np.sum(np.sqrt(m))**2
    if denom < 1e-30:
        return np.nan
    return np.sum(m) / denom

def rivero_phase(masses):
    """
    Best-fit Rivero phase δ for a mass triplet.
    Solves: √m_k = √m̄ · (1 + √2 cos(2πk/3 + δ))
    Returns δ ∈ [0, π] that minimises residual sum-of-squares.
    """
    m = np.asarray(masses, dtype=float)
    if np.any(m < 0):
        return np.nan
    sm = np.sqrt(m)
    sm_bar = np.mean(sm)
    if sm_bar < 1e-20:
        return np.nan
    x = (sm - sm_bar) / (np.sqrt(2) * sm_bar)   # should be cos(2πk/3 + δ)

    phases_k = np.array([0.0, 2*np.pi/3, 4*np.pi/3])

    def residual(delta):
        return np.sum((x - np.cos(phases_k + delta))**2)

    res = minimize_scalar(residual, bounds=(0.0, np.pi), method='bounded')
    return float(res.x)

def koide_Q_from_rivero(delta, m_bar=1.0):
    """Koide Q given Rivero phase δ (should always be 2/3 by construction)."""
    phases_k = np.array([0.0, 2*np.pi/3, 4*np.pi/3])
    sm = np.sqrt(m_bar) * (1 + np.sqrt(2) * np.cos(phases_k + delta))
    m = sm**2
    if np.any(m < 0):
        return np.nan
    return koide_Q(m)

# ── Scan ─────────────────────────────────────────────────────────────────────

# Normal ordering: m1 from ~0 to cosmological-bound-limited
# Σmν = m1 + m2 + m3 < 0.12 eV → find max m1
def sum_masses_NO(m1):
    return sum(neutrino_masses_NO(m1))

# Find m1 such that sum = 0.12 eV
m1_max = 0.04   # conservative upper bound

m1_scan = np.linspace(1e-4, m1_max, 2000)
Q_NO, delta_NO, sum_NO = [], [], []

for m1 in m1_scan:
    masses = neutrino_masses_NO(m1)
    s = sum(masses)
    if s > COSMO_SUM_BOUND:
        break
    Q_NO.append(koide_Q(masses))
    delta_NO.append(rivero_phase(masses))
    sum_NO.append(s)

m1_scan = m1_scan[:len(Q_NO)]
Q_NO = np.array(Q_NO)
delta_NO = np.array(delta_NO)
sum_NO = np.array(sum_NO)

# Inverted ordering: lightest is m3
m3_scan = np.linspace(1e-4, m1_max, 2000)
Q_IO, delta_IO, sum_IO = [], [], []

for m3 in m3_scan:
    masses = neutrino_masses_IO(m3)
    s = sum(masses)
    if s > COSMO_SUM_BOUND:
        break
    Q_IO.append(koide_Q(masses))
    delta_IO.append(rivero_phase(masses))
    sum_IO.append(s)

m3_scan = m3_scan[:len(Q_IO)]
Q_IO = np.array(Q_IO)
delta_IO = np.array(delta_IO)
sum_IO = np.array(sum_IO)

# ── Charged leptons for comparison ───────────────────────────────────────────

M_E  = 0.51099895e-3   # eV
M_MU = 105.6583755e-3  # eV
M_TAU = 1776.86e-3     # eV

Q_lepton = koide_Q([M_E, M_MU, M_TAU])
delta_lepton = rivero_phase([M_E, M_MU, M_TAU])

# ── Print results ─────────────────────────────────────────────────────────────

print("=" * 70)
print("NEUTRINO KOIDE SCAN")
print("=" * 70)
print()
print(f"Charged leptons:  Q = {Q_lepton:.6f},  δ = {delta_lepton:.4f} rad  ({delta_lepton*180/np.pi:.2f}°)")
print(f"Reference phases: 2/9 = {2/9:.4f},  π/4 = {np.pi/4:.4f},  δ_lepton = {delta_lepton:.4f}")
print()
print("Normal Ordering scan (first 5 m1 values):")
print(f"{'m1 (eV)':>10} {'Q':>10} {'δ (rad)':>10} {'δ (deg)':>10} {'Σmν (eV)':>10}")
print("-" * 55)
for i in range(0, min(5, len(m1_scan))):
    print(f"{m1_scan[i]:>10.5f} {Q_NO[i]:>10.6f} {delta_NO[i]:>10.4f} {delta_NO[i]*180/np.pi:>10.2f} {sum_NO[i]:>10.5f}")
print("  ...")
print()

# Find where Q is closest to 2/3
if len(Q_NO) > 0:
    idx_best_NO = np.argmin(np.abs(Q_NO - 2/3))
    print(f"Normal ordering — closest Q to 2/3:")
    print(f"  m1 = {m1_scan[idx_best_NO]:.5f} eV,  Q = {Q_NO[idx_best_NO]:.6f},  δ = {delta_NO[idx_best_NO]:.4f} rad ({delta_NO[idx_best_NO]*180/np.pi:.2f}°)")
    print(f"  |Q - 2/3| = {abs(Q_NO[idx_best_NO] - 2/3):.2e}")
    print()

if len(Q_IO) > 0:
    idx_best_IO = np.argmin(np.abs(Q_IO - 2/3))
    print(f"Inverted ordering — closest Q to 2/3:")
    print(f"  m3 = {m3_scan[idx_best_IO]:.5f} eV,  Q = {Q_IO[idx_best_IO]:.6f},  δ = {delta_IO[idx_best_IO]:.4f} rad ({delta_IO[idx_best_IO]*180/np.pi:.2f}°)")
    print(f"  |Q - 2/3| = {abs(Q_IO[idx_best_IO] - 2/3):.2e}")
    print()

# Check anchor proximity
anchors = {"2/9": 2/9, "π/4": np.pi/4, "δ_lepton": delta_lepton}
print("Phase anchor distances (Normal Ordering, best-Q point):")
for name, anchor in anchors.items():
    if len(delta_NO) > 0:
        dist = abs(delta_NO[idx_best_NO] - anchor)
        print(f"  |δ_NO - {name}| = {dist:.4f} rad  ({dist*180/np.pi:.2f}°)")

print()
print("Phase anchor distances (Inverted Ordering, best-Q point):")
for name, anchor in anchors.items():
    if len(delta_IO) > 0:
        dist = abs(delta_IO[idx_best_IO] - anchor)
        print(f"  |δ_IO - {name}| = {dist:.4f} rad  ({dist*180/np.pi:.2f}°)")

# ── Plot ─────────────────────────────────────────────────────────────────────

bg = "#0a0a14"
fg = "#dddddd"
c_NO = "#00e0b8"
c_IO = "#ff6b6b"
c_gold = "#ffd166"
c_lepton = "#a78bfa"

fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor(bg)
fig.suptitle(
    "Neutrino Koide Phase Scan\n"
    "Does the weak sector lock to the same geometric anchors as charged leptons?",
    color="white", fontsize=13, y=0.98
)

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.35)

def style_ax(ax):
    ax.set_facecolor(bg)
    ax.tick_params(colors=fg, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")
    ax.grid(True, color="#222233", lw=0.5, alpha=0.7)
    ax.xaxis.label.set_color(fg)
    ax.yaxis.label.set_color(fg)
    ax.title.set_color("white")

# Panel 1: Q vs m_lightest
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1)
if len(Q_NO) > 0:
    ax1.plot(m1_scan * 1000, Q_NO, color=c_NO, lw=2, label='NO (m₁ lightest)')
if len(Q_IO) > 0:
    ax1.plot(m3_scan * 1000, Q_IO, color=c_IO, lw=2, label='IO (m₃ lightest)')
ax1.axhline(2/3, color=c_gold, ls='--', lw=1.8, label='Q = 2/3 (Koide)')
ax1.axhline(Q_lepton, color=c_lepton, ls=':', lw=1.5, label=f'Q charged leptons = {Q_lepton:.4f}')
ax1.set_xlabel('Lightest neutrino mass (meV)')
ax1.set_ylabel('Koide Q')
ax1.set_title('Koide Q vs Lightest Neutrino Mass')
ax1.legend(facecolor="#111122", labelcolor=fg, fontsize=8)

# Panel 2: δ vs m_lightest
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2)
if len(delta_NO) > 0:
    ax2.plot(m1_scan * 1000, delta_NO, color=c_NO, lw=2, label='NO Rivero phase δ')
if len(delta_IO) > 0:
    ax2.plot(m3_scan * 1000, delta_IO, color=c_IO, lw=2, label='IO Rivero phase δ')
ax2.axhline(DELTA_2_OVER_9, color=c_gold, ls='--', lw=1.5, label=f'2/9 = {2/9:.3f} rad')
ax2.axhline(DELTA_DOWN_QUARK, color='#f59e0b', ls='-.', lw=1.5, label=f'π/4 = {np.pi/4:.3f} rad')
ax2.axhline(delta_lepton, color=c_lepton, ls=':', lw=1.5, label=f'δ_lepton = {delta_lepton:.3f} rad')
ax2.set_xlabel('Lightest neutrino mass (meV)')
ax2.set_ylabel('Rivero phase δ (rad)')
ax2.set_title('Koide Phase δ vs Lightest Neutrino Mass')
ax2.legend(facecolor="#111122", labelcolor=fg, fontsize=8)

# Panel 3: Q - 2/3 deviation
ax3 = fig.add_subplot(gs[1, 0])
style_ax(ax3)
if len(Q_NO) > 0:
    ax3.semilogy(m1_scan * 1000, np.abs(Q_NO - 2/3) + 1e-10, color=c_NO, lw=2, label='|Q_NO - 2/3|')
if len(Q_IO) > 0:
    ax3.semilogy(m3_scan * 1000, np.abs(Q_IO - 2/3) + 1e-10, color=c_IO, lw=2, label='|Q_IO - 2/3|')
ax3.set_xlabel('Lightest neutrino mass (meV)')
ax3.set_ylabel('|Q - 2/3| (log scale)')
ax3.set_title('Deviation from Koide Relation Q = 2/3')
ax3.legend(facecolor="#111122", labelcolor=fg, fontsize=8)

# Panel 4: phase comparison to charged lepton sector
ax4 = fig.add_subplot(gs[1, 1])
style_ax(ax4)
if len(delta_NO) > 0 and len(delta_IO) > 0:
    ax4.scatter([delta_lepton], [delta_lepton], s=120, color=c_lepton, zorder=5, label=f'Charged leptons δ={delta_lepton:.3f}')
    ax4.scatter(delta_NO[::20], delta_IO[:len(delta_NO[::20])], s=15, color=c_NO, alpha=0.5, label='NO vs IO phases')
ax4.axhline(DELTA_2_OVER_9, color=c_gold, ls='--', lw=1.2, label='2/9')
ax4.axhline(DELTA_DOWN_QUARK, color='#f59e0b', ls='-.', lw=1.2, label='π/4')
ax4.plot([0, 1], [0, 1], color='gray', ls=':', alpha=0.3)
ax4.set_xlabel('δ_NO (rad)')
ax4.set_ylabel('δ_IO (rad)')
ax4.set_title('Normal vs Inverted Ordering Phases')
ax4.legend(facecolor="#111122", labelcolor=fg, fontsize=8)

plt.savefig('/mnt/d/Fundamentals/sandbox/neutrino_koide_scan.png',
            dpi=150, bbox_inches='tight', facecolor=bg)
plt.close()
print("\nFigure saved: sandbox/neutrino_koide_scan.png")
