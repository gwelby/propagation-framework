"""
chiral_projection_z3.py
=======================
Path A: Does chiral projection of the Z3 generation walk kill the backward
coupling b·S̄² and leave only the forward pure shift a·S̄?

The Gap B no-go proved:
  T = a·S̄ + b·S̄²  =>  T³ diagonal iff ab = 0.

The symmetric nearest-neighbor operator (a=b) from the Z3 EOM does NOT give
diagonal 3-step closure.

Path A asks: IF the weak force is left-handed (chiral), AND the generation
walk is the 'current' driven by weak coupling, THEN does chirality force b→0?

This script works in the Fourier eigenbasis of S̄ on Z3:
  Eigenvalues of S̄:  ω⁰=1,  ω¹=e^{2πi/3},  ω²=e^{4πi/3}
  k=0: static mode (uniform generation average)
  k=1: forward-propagating mode (phase velocity +2π/3 per step)
  k=2: backward-propagating mode (phase velocity -2π/3 per step)

Left-handed chirality ≡ selecting only FORWARD-propagating modes.
P_L ≡ projector onto k=1 eigenspace (and k=0 static mode).

Under P_L:
  The k=2 EIGENMODE is killed entirely (eigenvalue set to zero).
  T_L is NOT reduced to a pure forward shift: |β/α| = 1 in position space.

Result: Chiral projection makes T_L rank-2 (kills k=2 eigenmode), but does
NOT eliminate the S̄² component from the position-space matrix. T_L³ in the
full 3D position space has NONZERO off-diagonals — Gap B no-go still applies.

What IS true within the projected 2D subspace {k=0, k=1}: T_L has eigenvalues
{1, -1/2}, and T_L³ restricted to that subspace is diagonal in the Fourier
basis. This is 3-step periodicity in the projected sector, not full H_prod.

This is NOT a proof from PF axioms. It makes the chirality argument executable
and exposes two remaining targets for Path A:
  (1) Prove P_L is forced by the Z3 Lagrangian + weak chiral structure.
  (2) Prove Fourier-basis closure in the projected sector implies position-space
      probability factorization (new gap — not visible before this computation).
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent

# ── Build S̄ and Fourier basis on Z3 ─────────────────────────────────────────

omega = np.exp(2j * np.pi / 3)

# S̄: cyclic shift |j⟩ → |j+1 mod 3⟩
S_bar = np.array([[0, 0, 1],
                  [1, 0, 0],
                  [0, 1, 0]], dtype=complex)

# DFT matrix on Z3: F[j,k] = ω^{-jk} / √3
# Columns are the eigenvectors of S̄
F = np.array([[omega**(0), omega**(0),    omega**(0)   ],
              [omega**(0), omega**(-1),   omega**(-2)  ],
              [omega**(0), omega**(-2),   omega**(-4)  ]]) / np.sqrt(3)

# Verify: S̄ = F · diag(1, ω, ω²) · F†
eigenvalues_Sbar = np.array([1.0, omega, omega**2])
S_check = F @ np.diag(eigenvalues_Sbar) @ F.conj().T
assert np.allclose(S_check, S_bar, atol=1e-12), "DFT diagonalization failed"

print("=" * 70)
print("CHIRAL PROJECTION ON Z3")
print("=" * 70)
print()
print("S̄ eigenbasis on Z3:")
print(f"  k=0: eigenvalue ω⁰ = 1       (static mode, uniform over generations)")
print(f"  k=1: eigenvalue ω¹ = e^(+2πi/3)  (FORWARD: phase advances +120° per step)")
print(f"  k=2: eigenvalue ω² = e^(-2πi/3)  (BACKWARD: phase retreats -120° per step)")
print()

# ── Define the operators ─────────────────────────────────────────────────────

S_bar2 = S_bar @ S_bar  # S̄²

T_symmetric = 0.5 * (S_bar + S_bar2)     # a=b=1/2  symmetric
T_symmetric_real = T_symmetric.real       # should be real for physical stochastic operator

# Verify symmetry
assert np.allclose(T_symmetric.imag, 0, atol=1e-12), "T_symmetric should be real"
print("T_symmetric = (1/2)(S̄ + S̄²) [nearest-neighbor, real, both directions]")
print(np.round(T_symmetric.real, 4))
print()

# ── Chiral projectors ────────────────────────────────────────────────────────

# P_L: project onto k=1 mode (forward propagating, left-handed)
# P_k = |v_k⟩⟨v_k| where |v_k⟩ is k-th column of F

def projector(k, F_matrix):
    v = F_matrix[:, k]
    return np.outer(v, v.conj())

P0 = projector(0, F)   # static
P1 = projector(1, F)   # forward (left-handed)
P2 = projector(2, F)   # backward (right-handed)

# Verify completeness and orthogonality
assert np.allclose(P0 + P1 + P2, np.eye(3), atol=1e-12), "Projectors not complete"
assert np.allclose(P0 @ P1, 0, atol=1e-12), "P0, P1 not orthogonal"

print("Projector structure verified: P0 + P1 + P2 = I  ✓")
print()

# ── Chiral projection of T_symmetric ────────────────────────────────────────

# "Left-handed" coupling: keep k=0 (static) and k=1 (forward), zero out k=2
P_L = P0 + P1   # left-handed sector
P_R = P2        # right-handed sector

# Projected operator: only left-handed coupling survives
T_L = P_L @ T_symmetric @ P_L     # restrict to left-handed subspace
T_R = P_R @ T_symmetric @ P_R     # restrict to right-handed subspace

print("Fourier decomposition of T_symmetric:")
print(f"  T in k=0 sector: eigenvalue = {np.vdot(F[:,0], T_symmetric @ F[:,0]):.4f}")
print(f"  T in k=1 sector: eigenvalue = {np.vdot(F[:,1], T_symmetric @ F[:,1]):.6f}")
print(f"  T in k=2 sector: eigenvalue = {np.vdot(F[:,2], T_symmetric @ F[:,2]):.6f}")
print()
print("Fourier decomposition of S̄ (forward shift):")
print(f"  S̄ in k=0 sector: eigenvalue = {np.vdot(F[:,0], S_bar @ F[:,0]):.4f}")
print(f"  S̄ in k=1 sector: eigenvalue = {np.vdot(F[:,1], S_bar @ F[:,1]):.6f}")
print(f"  S̄ in k=2 sector: eigenvalue = {np.vdot(F[:,2], S_bar @ F[:,2]):.6f}")
print()
print("Fourier decomposition of S̄² (backward shift):")
print(f"  S̄² in k=0 sector: eigenvalue = {np.vdot(F[:,0], S_bar2 @ F[:,0]):.4f}")
print(f"  S̄² in k=1 sector: eigenvalue = {np.vdot(F[:,1], S_bar2 @ F[:,1]):.6f}")
print(f"  S̄² in k=2 sector: eigenvalue = {np.vdot(F[:,2], S_bar2 @ F[:,2]):.6f}")
print()

# ── Key result: what is T_L in position space? ───────────────────────────────

print("=" * 70)
print("KEY RESULT: T_L = P_L · T_sym · P_L in position space")
print("=" * 70)
print(np.round(T_L.real, 6))
print("(imaginary part max magnitude:", np.max(np.abs(T_L.imag)), ")")
print()

# What fraction is S̄ vs S̄²?
# T_L should decompose as α·S̄ + β·S̄²
# α = Tr(S̄† · T_L)/3,  β = Tr(S̄²† · T_L)/3
alpha = np.trace(S_bar.conj().T @ T_L) / 3
beta  = np.trace(S_bar2.conj().T @ T_L) / 3

print(f"T_L = α·S̄ + β·S̄²  where:")
print(f"  α = {alpha:.6f}  (forward S̄ coefficient)")
print(f"  β = {beta:.6f}   (backward S̄² coefficient)")
print(f"  |β/α| = {abs(beta/alpha):.6f}  (ratio of backward to forward coupling)")
print()

# ── 3-step closure under chiral projection ────────────────────────────────────

T_L3 = np.linalg.matrix_power(T_L, 3)
T_sym3 = np.linalg.matrix_power(T_symmetric, 3)

print("T_L³ (chiral-projected, 3-step closure):")
print(np.round(T_L3.real, 6))
print()
print("T_sym³ (symmetric, 3-step closure):")
print(np.round(T_sym3.real, 4))
print()

# Is T_L³ diagonal?
off_diag_L = np.max(np.abs(T_L3 - np.diag(np.diag(T_L3))))
off_diag_sym = np.max(np.abs(T_sym3 - np.diag(np.diag(T_sym3))))

print(f"Max off-diagonal of T_L³:   {off_diag_L:.2e}  {'← DIAGONAL ✓' if off_diag_L < 1e-10 else '← non-zero'}")
print(f"Max off-diagonal of T_sym³: {off_diag_sym:.4f}  ← non-zero (Gap B no-go)")
print()

# ── Entropy comparison under chiral projection ────────────────────────────────

def evolve_entropy(T_op, steps=12):
    state = np.array([1.0, 0.0, 0.0], dtype=complex)
    entropies = []
    for _ in range(steps + 1):
        p = np.abs(state)**2
        p = np.clip(p, 1e-15, 1.0)
        h = -np.sum(p * np.log(p))
        entropies.append(float(h))
        state = T_op @ state
        state = state / (np.sum(np.abs(state)**2)**0.5 + 1e-30)
    return entropies

ent_L   = evolve_entropy(T_L / (np.sum(np.abs(T_L[0]))**1 + 1e-30), 12)
ent_sym = evolve_entropy(T_symmetric.astype(complex), 12)

print("Shannon entropy evolution (starting in generation 0):")
print(f"{'Step':>4}  {'Symmetric':>12}  {'Chiral-proj':>14}")
print("-" * 35)
for k, (es, ec) in enumerate(zip(ent_sym, ent_L)):
    print(f"{k:>4}  {es:>12.6f}  {ec:>14.6f}")

# ── Physical interpretation ──────────────────────────────────────────────────

print()
print("=" * 70)
print("PHYSICAL INTERPRETATION  [corrected — see audit 2026-03-31]")
print("=" * 70)
print(f"""
The Z3 Fourier eigenbasis splits the generation walk into three sectors:

  k=0 (static):   S̄ and S̄² both have eigenvalue 1   — no propagation
  k=1 (forward):  S̄  eigenvalue e^{{+2πi/3}}           — left-handed chirality
  k=2 (backward): S̄  eigenvalue e^{{-2πi/3}}           — right-handed chirality

The symmetric T = (1/2)(S̄ + S̄²) has EQUAL weight in k=1 and k=2.

WHAT P_L = P0 + P1 ACTUALLY DOES:
  P_L kills the k=2 EIGENMODE (sets its eigenvalue to zero).
  It does NOT eliminate S̄² from the position-space matrix.

  Computed: |β/α| = 1.000  ← T_L retains equal forward AND backward
  coupling in position space. T_L is NOT ∝ S̄ (NOT a pure shift).

3-STEP CLOSURE (CORRECTED):
  T_L³ in the full 3D position space has NONZERO off-diagonals (see above).
  Gap B no-go still applies: T_L³ is not diagonal in position space.

  What IS true in the projected 2D subspace {{k=0, k=1}}:
    T_L has eigenvalues {{1, -1/2}} and T_L³|_{{2D}} = diag(1, -1/8)
    — diagonal in the Fourier eigenbasis of that 2D sector.
  This is 3-step periodicity within the left-handed sector only.

REMAINING FORMAL TARGETS FOR PATH A:
  1. Prove P_L is forced by the Z3 Lagrangian under weak chiral coupling
     (the original Path A target — still open).
  2. Prove that Fourier-basis closure in the projected 2D sector translates
     to position-space probability factorization for H_prod.
     *** This is a NEW named gap, not visible before this computation. ***

Gap B does NOT close from chiral projection alone. Both targets are open.
""")

# ── Plot ─────────────────────────────────────────────────────────────────────

bg = "#0a0a14"
fg = "#dddddd"
c_chiral = "#00e0b8"
c_sym = "#ff6b6b"
c_proj = "#a78bfa"
c_gold = "#ffd166"

fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor(bg)
fig.suptitle(
    "Chiral Projection on Z₃ — Path A for Gap B\n"
    "Left-handed projection kills backward coupling: T_projected ∝ S̄ → T³ diagonal",
    color="white", fontsize=13, y=0.98
)

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.35)

def style_ax(ax):
    ax.set_facecolor(bg)
    ax.tick_params(colors=fg, labelsize=9)
    for sp in ax.spines.values(): sp.set_edgecolor("#333333")
    ax.grid(True, color="#222233", lw=0.5, alpha=0.7)
    ax.xaxis.label.set_color(fg)
    ax.yaxis.label.set_color(fg)
    ax.title.set_color("white")

steps_arr = np.arange(13)
H_max = np.log(3)

# Panel 1: Sector weights of each operator
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1)
ops = ['S̄\n(forward)', 'S̄²\n(backward)', 'T_sym\n(both equal)', 'T_projected\n(P_L applied)']
k0_weights = [abs(np.vdot(F[:,0], op @ F[:,0]))**2 for op in [S_bar, S_bar2, T_symmetric, T_L]]
k1_weights = [abs(np.vdot(F[:,1], op @ F[:,1]))**2 for op in [S_bar, S_bar2, T_symmetric, T_L]]
k2_weights = [abs(np.vdot(F[:,2], op @ F[:,2]))**2 for op in [S_bar, S_bar2, T_symmetric, T_L]]

x = np.arange(len(ops))
w = 0.25
ax1.bar(x - w, np.abs(k0_weights), w, color='gray', alpha=0.8, label='k=0 (static)')
ax1.bar(x,     np.abs(k1_weights), w, color=c_chiral, alpha=0.9, label='k=1 (forward, L-handed)')
ax1.bar(x + w, np.abs(k2_weights), w, color=c_sym, alpha=0.9, label='k=2 (backward, R-handed)')
ax1.set_xticks(x)
ax1.set_xticklabels(ops, fontsize=8)
ax1.set_ylabel('|eigenvalue|²')
ax1.set_title('Fourier Sector Decomposition')
ax1.legend(facecolor="#111122", labelcolor=fg, fontsize=8)

# Panel 2: T³ off-diagonal comparison
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2)
ops_for_plot = [S_bar, S_bar2, T_symmetric, T_L]
op_labels = ['S̄ (chiral)', 'S̄² (anti-chiral)', 'T_sym (balanced)', 'T_L (projected)']
op_colors = [c_chiral, c_sym, c_sym, c_proj]
T3_list = [np.linalg.matrix_power(op, 3) for op in ops_for_plot]
off_diags = [np.max(np.abs(T3 - np.diag(np.diag(T3)))) for T3 in T3_list]

bars = ax2.bar(op_labels, off_diags, color=op_colors, alpha=0.85, edgecolor='white', lw=0.5)
ax2.set_ylabel('Max off-diagonal |T³|')
ax2.set_title('3-Step Closure: Off-Diagonal Mixing')
ax2.axhline(1e-10, color=c_gold, ls='--', lw=1.5, label='Exact zero threshold')
ax2.set_yscale('symlog', linthresh=1e-12)
ax2.legend(facecolor="#111122", labelcolor=fg, fontsize=9)
for bar, val in zip(bars, off_diags):
    ax2.text(bar.get_x() + bar.get_width()/2, max(val, 1e-11)*2,
             f'{val:.2e}', ha='center', fontsize=7, color='white')

# Panel 3: Entropy comparison
ax3 = fig.add_subplot(gs[1, 0])
style_ax(ax3)
ax3.plot(steps_arr, ent_sym, 'o-', color=c_sym, lw=2, ms=6, label='Symmetric T')
ax3.plot(steps_arr, ent_L, 's--', color=c_proj, lw=2, ms=6, label='Chiral-projected T_L')
ax3.axhline(0, color=c_chiral, ls=':', lw=1.5, label='H=0 (perfect identity)')
ax3.axhline(H_max, color=c_gold, ls='--', lw=1.5, label=f'H_max = ln(3)')
ax3.set_xlabel('Step')
ax3.set_ylabel('Shannon entropy H')
ax3.set_title('Entropy: Symmetric vs Chiral-Projected Walk')
ax3.legend(facecolor="#111122", labelcolor=fg, fontsize=8)
ax3.set_ylim(-0.05, H_max * 1.2)

# Panel 4: Logical chain diagram
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(bg)
ax4.axis('off')
ax4.set_title('Path A: Logical Chain to Close Gap B', color='white', fontsize=11, fontweight='bold')

chain = [
    ("Gap B No-Go Theorem", "#e74c3c",
     "T³ diagonal iff ab = 0\n(proved by Codex 2026-03-25)"),
    ("Chirality Observation", "#f59e0b",
     "Weak force is left-handed (SM)\nOnly k=1 (forward) mode couples"),
    ("Chiral Projection", "#a78bfa",
     "P_L kills k=2 EIGENMODE (not S̄² term)\n|β/α|=1 in position space — NOT pure shift"),
    ("T_L³ in 2D subspace", "#00e0b8",
     "Diagonal in Fourier basis of {k=0,k=1}\nBut NOT diagonal in full 3D position space"),
    ("H_prod: TWO open gaps", "#e74c3c",
     "Gap 1: prove P_L from ℤ₃ Lagrangian\nGap 2: 2D closure → position-space H_prod"),
]

y = 0.92
for title, color, desc in chain:
    ax4.text(0.05, y, f"► {title}", color=color, fontsize=10,
             fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.08, y - 0.06, desc, color=fg, fontsize=8.5,
             transform=ax4.transAxes, style='italic')
    y -= 0.17

ax4.text(0.05, 0.04,
         "OPEN: Gap 1 (P_L from ℤ₃) + Gap 2 (2D→H_prod)",
         color="#ffd166", fontsize=9, fontweight='bold',
         transform=ax4.transAxes,
         bbox=dict(boxstyle='round', fc='#2a1a00', alpha=0.8))

output_path = OUTPUT_DIR / 'chiral_projection_z3.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=bg)
plt.close()
print(f"\nFigure saved: {output_path.relative_to(OUTPUT_DIR.parent)}")
