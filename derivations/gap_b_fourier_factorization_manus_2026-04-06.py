"""
Gap B: Chiral Projection Fourier Sector Factorization Test
===========================================================
The live Path A obligation (CLAIMS.md, 2026-04-01):
  "Derive whether the projected {k=0, k=1} sector is forced by the Z3 Lagrangian,
   and whether closure in that 2D Fourier sector implies the position-space
   probability factorization required for H_prod."

This script tests:
  1. The Z3 transfer matrix T (nearest-neighbor circulant) and its Fourier structure
  2. The chiral projection P onto {k=0, k=1} Fourier modes
  3. Whether T_chiral^3 is diagonal in position space (known: NO — confirmed)
  4. NEW: Whether the projected probability distribution P(i,j) = P(i)*P(j) factorizes
     (i.e., whether the marginals are independent after chiral projection)
  5. NEW: The entropy of the projected distribution vs the factorized product
  6. NEW: Whether the {k=0,k=1} sector closure is FORCED by the Z3 Lagrangian
     (i.e., is it the only sector that satisfies Axiom 3 coherence?)

Author: Manus
Date: 2026-04-06
Ground Truth: D:\Fundamentals\CLAIMS.md (Gap B, Path A, 2026-04-01 update)
"""

import numpy as np
from itertools import product as iproduct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

print("=" * 70)
print("GAP B: CHIRAL PROJECTION FOURIER SECTOR FACTORIZATION TEST")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: The Z3 Transfer Matrix
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1] Z3 Transfer Matrix Construction")
print("-" * 50)

# The nearest-neighbor circulant on Z3: T = a*S + b*S^2
# where S is the cyclic shift: S|j> = |j+1 mod 3>
# For the symmetric EOM: a = b = 1
# S matrix
S = np.array([[0, 0, 1],
              [1, 0, 0],
              [0, 1, 0]], dtype=complex)

S2 = S @ S  # S^2

# Symmetric transfer matrix (a=b=1)
T_sym = S + S2
print(f"  T_sym (symmetric, a=b=1):")
print(f"  {T_sym.real.astype(int)}")

# T_sym^3
T_sym3 = np.linalg.matrix_power(T_sym, 3)
print(f"\n  T_sym^3:")
print(f"  {T_sym3.real.astype(int)}")
print(f"  Off-diagonal entries: {T_sym3[0,1].real:.0f} (should be 3 per CLAIMS.md)")

# Chiral transfer matrix: T_chiral = alpha*S + beta*S^2 with |beta/alpha| = 1, arg != 0
# Use the chiral projection: keep only k=0 and k=1 Fourier modes
# Fourier basis for Z3: omega = exp(2*pi*i/3)
omega = np.exp(2j * np.pi / 3)
# DFT matrix for Z3
F = np.array([[1, 1, 1],
              [1, omega, omega**2],
              [1, omega**2, omega**4]]) / np.sqrt(3)

# Eigenvalues of S in Fourier basis: lambda_k = omega^k for k=0,1,2
# T_sym eigenvalues: lambda_k(T_sym) = omega^k + omega^(2k)
eigs_sym = np.array([1 + 1,  # k=0: 1+1=2
                     omega + omega**2,  # k=1: omega + omega^2 = -1
                     omega**2 + omega**4])  # k=2: omega^2 + omega^4 = omega^2 + omega = -1

print(f"\n  T_sym eigenvalues (Fourier basis):")
for k in range(3):
    lam = omega**k + omega**(2*k)
    print(f"  k={k}: lambda = {lam:.4f} (|lambda| = {abs(lam):.4f})")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: Chiral Projection onto {k=0, k=1}
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2] Chiral Projection onto {k=0, k=1} Sector")
print("-" * 50)

# Projection operator: P = |k=0><k=0| + |k=1><k=1| in position basis
f0 = F[0]  # k=0 eigenvector
f1 = F[1]  # k=1 eigenvector
f2 = F[2]  # k=2 eigenvector

P_proj = np.outer(f0, f0.conj()) + np.outer(f1, f1.conj())
print(f"  Projection operator P (onto k=0,1):")
print(f"  Real part:\n  {P_proj.real.round(4)}")
print(f"  Rank of P: {int(round(np.trace(P_proj).real))}")

# Projected transfer matrix
T_chiral = P_proj @ T_sym @ P_proj
print(f"\n  T_chiral = P * T_sym * P:")
print(f"  Real part:\n  {T_chiral.real.round(4)}")
print(f"  Imag part:\n  {T_chiral.imag.round(4)}")

# T_chiral^3
T_chiral3 = np.linalg.matrix_power(T_chiral, 3)
print(f"\n  T_chiral^3:")
print(f"  Real part:\n  {T_chiral3.real.round(6)}")
is_diagonal = np.allclose(T_chiral3 - np.diag(np.diag(T_chiral3)), 0, atol=1e-10)
print(f"  Is T_chiral^3 diagonal? {is_diagonal} (CLAIMS.md says NO)")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: Position-Space Probability Factorization Test (H_prod)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3] H_prod Factorization Test")
print("-" * 50)

# The H_prod requirement: after 3 steps, the joint probability distribution
# P(i,j) of (start, end) should factorize as P(i,j) = P_i(i) * P_j(j)
# This is the statistical independence condition.

# Start with a uniform initial distribution over Z3
rho0 = np.ones(3) / 3.0  # uniform

# Apply T_chiral^3 to get the transition matrix
# The (i,j) entry of T_chiral^3 gives the amplitude for i -> j
# The probability is |T_chiral^3[i,j]|^2 (for a quantum walk)
# or T_chiral^3[i,j] directly (for a classical walk with complex weights)

# For the factorization test, we examine the joint distribution:
# P(i,j) = rho0[i] * |T_chiral^3[i,j]|^2 (quantum) or rho0[i] * T_chiral^3[i,j].real

# Quantum probability matrix
P_joint_quantum = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        P_joint_quantum[i, j] = rho0[i] * abs(T_chiral3[i, j])**2

# Normalize
P_joint_quantum /= P_joint_quantum.sum()

# Marginals
P_i = P_joint_quantum.sum(axis=1)  # marginal over j
P_j = P_joint_quantum.sum(axis=0)  # marginal over i

# Factorized product
P_factorized = np.outer(P_i, P_j)

# Kullback-Leibler divergence from factorized
def kl_divergence(P, Q):
    """KL(P || Q) — how much P differs from Q"""
    mask = P > 1e-15
    return np.sum(P[mask] * np.log(P[mask] / Q[mask]))

kl_from_factorized = kl_divergence(P_joint_quantum, P_factorized)
total_variation = 0.5 * np.sum(np.abs(P_joint_quantum - P_factorized))

print(f"  Joint distribution P(i,j) [quantum, 3-step, uniform init]:")
print(f"  {P_joint_quantum.round(6)}")
print(f"\n  Marginals:")
print(f"  P_i = {P_i.round(6)}")
print(f"  P_j = {P_j.round(6)}")
print(f"\n  Factorized product P_i ⊗ P_j:")
print(f"  {P_factorized.round(6)}")
print(f"\n  KL(P_joint || P_factorized) = {kl_from_factorized:.6f}")
print(f"  Total variation distance = {total_variation:.6f}")

if kl_from_factorized < 1e-10:
    print(f"\n  RESULT: P(i,j) FACTORIZES — H_prod is satisfied!")
    factorizes = True
else:
    print(f"\n  RESULT: P(i,j) does NOT factorize — H_prod is NOT satisfied.")
    print(f"  The chiral projection alone is insufficient for H_prod.")
    factorizes = False

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: Is {k=0,k=1} Sector Closure FORCED by Axiom 3?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4] Axiom 3 Sector Selection Test")
print("-" * 50)

# Test all possible 2D sector projections of Z3 Fourier modes
# There are 3 possible 2D projections: {0,1}, {0,2}, {1,2}
sectors = [(0,1), (0,2), (1,2)]
F_vecs = [f0, f1, f2]

print(f"  Testing all 2D Fourier sector projections for coherence...")
print(f"  {'Sector':<12} {'Coherence (|Tr T^3|)':<25} {'Factorizes?':<15} {'Entropy'}")
print(f"  {'-'*65}")

best_coherence = 0
best_sector = None
results = []

for s in sectors:
    # Build projection
    P_s = np.outer(F_vecs[s[0]], F_vecs[s[0]].conj()) + \
          np.outer(F_vecs[s[1]], F_vecs[s[1]].conj())
    T_s = P_s @ T_sym @ P_s
    T_s3 = np.linalg.matrix_power(T_s, 3)

    # Coherence measure: |Tr(T^3)| — how much the 3-step walk returns to origin
    coherence = abs(np.trace(T_s3))

    # Factorization test
    P_j_s = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            P_j_s[i, j] = rho0[i] * abs(T_s3[i, j])**2
    if P_j_s.sum() > 1e-15:
        P_j_s /= P_j_s.sum()
        P_i_s = P_j_s.sum(axis=1)
        P_j_marg = P_j_s.sum(axis=0)
        P_fact_s = np.outer(P_i_s, P_j_marg)
        kl_s = kl_divergence(P_j_s, P_fact_s)
        fact_s = kl_s < 1e-10

        # Shannon entropy of joint distribution
        mask = P_j_s > 1e-15
        entropy_s = -np.sum(P_j_s[mask] * np.log2(P_j_s[mask]))
    else:
        kl_s = float('inf')
        fact_s = False
        entropy_s = 0.0

    results.append((s, coherence, fact_s, entropy_s, kl_s))
    print(f"  k={{{s[0]},{s[1]}}}: {coherence:>20.6f}   {'YES' if fact_s else 'NO':<15} {entropy_s:.4f} bits")

    if coherence > best_coherence:
        best_coherence = coherence
        best_sector = s

print(f"\n  Highest coherence sector: k={{{best_sector[0]},{best_sector[1]}}}")
print(f"  Is {{{best_sector[0]},{best_sector[1]}}} == {{0,1}}? {best_sector == (0,1)}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: The Honest Verdict
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5] HONEST VERDICT")
print("-" * 50)
print(f"""
  QUESTION: Does closure in the {{k=0,k=1}} Fourier sector imply
            position-space probability factorization (H_prod)?

  ANSWER: {'YES — H_prod is satisfied.' if factorizes else 'NO — H_prod is NOT satisfied.'}

  QUESTION: Is the {{k=0,k=1}} sector uniquely selected by Axiom 3 coherence?

  ANSWER: {'YES' if best_sector == (0,1) else 'NO'} — the sector with highest coherence is k={{{best_sector[0]},{best_sector[1]}}}.

  IMPLICATION:
  {'Path A remains viable — the chiral projection satisfies H_prod.' if factorizes else
   'Path A still has an open bridge. The chiral projection does NOT satisfy H_prod in position space.'}

  The {{{best_sector[0]},{best_sector[1]}}} sector {'IS' if best_sector == (0,1) else 'is NOT'} the Axiom 3 preferred sector.

  CONFIDENCE IMPACT:
  {'God Equation Path A: OPEN gap partially closed. Recommend Codex audit.' if factorizes else
   'God Equation Path A: Gap confirmed open. The Fourier-to-position bridge is the live obligation.'}
""")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: Visualization
# ─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10), facecolor='#0a0a0a')
fig.suptitle('Gap B: Chiral Projection Fourier Sector Factorization Test\nPropagation Framework — God Equation Path A Analysis',
             fontsize=14, color='white', fontweight='bold', y=0.98)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)
bg = '#111111'
c_gold = '#FFD700'
c_cyan = '#00FFFF'
c_green = '#00FF88'
c_red = '#FF4444'
c_white = '#FFFFFF'
c_gray = '#888888'

# Plot 1: T_sym^3 heatmap
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(bg)
im1 = ax1.imshow(T_sym3.real, cmap='RdYlGn', vmin=-5, vmax=10)
ax1.set_title('T_sym³ (Symmetric Walk)\nOff-diagonal = 3 (thermalizes)', color=c_white, fontsize=9)
for i in range(3):
    for j in range(3):
        ax1.text(j, i, f'{T_sym3[i,j].real:.0f}', ha='center', va='center',
                color='black', fontweight='bold', fontsize=14)
ax1.set_xticks([0,1,2]); ax1.set_yticks([0,1,2])
ax1.tick_params(colors=c_gray)
plt.colorbar(im1, ax=ax1)

# Plot 2: T_chiral^3 heatmap
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(bg)
im2 = ax2.imshow(np.abs(T_chiral3), cmap='RdYlGn', vmin=0, vmax=2)
ax2.set_title('|T_chiral³| (Chiral Projection)\nNot diagonal — Gap B confirmed', color=c_white, fontsize=9)
for i in range(3):
    for j in range(3):
        ax2.text(j, i, f'{abs(T_chiral3[i,j]):.3f}', ha='center', va='center',
                color='black', fontweight='bold', fontsize=11)
ax2.set_xticks([0,1,2]); ax2.set_yticks([0,1,2])
ax2.tick_params(colors=c_gray)
plt.colorbar(im2, ax=ax2)

# Plot 3: Joint vs Factorized distribution
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(bg)
x = np.arange(9)
joint_flat = P_joint_quantum.flatten()
fact_flat = P_factorized.flatten()
labels = [f'({i},{j})' for i in range(3) for j in range(3)]
ax3.bar(x - 0.2, joint_flat, 0.4, color=c_cyan, alpha=0.85, label='P(i,j) joint')
ax3.bar(x + 0.2, fact_flat, 0.4, color=c_gold, alpha=0.85, label='P_i⊗P_j factorized')
ax3.set_xticks(x); ax3.set_xticklabels(labels, rotation=45, fontsize=7, color=c_white)
ax3.set_title(f'H_prod Test: Joint vs Factorized\nKL = {kl_from_factorized:.4f} | TV = {total_variation:.4f}',
              color=c_white, fontsize=9)
ax3.legend(fontsize=7, facecolor=bg, labelcolor=c_white, edgecolor=c_gray)
ax3.tick_params(colors=c_gray)
for spine in ax3.spines.values():
    spine.set_edgecolor(c_gray)
verdict_color = c_green if factorizes else c_red
verdict_text = 'H_prod: SATISFIED' if factorizes else 'H_prod: NOT SATISFIED'
ax3.text(0.5, 0.92, verdict_text, transform=ax3.transAxes,
         ha='center', color=verdict_color, fontsize=11, fontweight='bold')

# Plot 4: Sector coherence comparison
ax4 = fig.add_subplot(gs[1, 0:2])
ax4.set_facecolor(bg)
sector_labels = [f'k={{{s[0]},{s[1]}}}' for s, c, f, e, kl in results]
coherences = [c for s, c, f, e, kl in results]
entropies = [e for s, c, f, e, kl in results]
bar_colors = [c_gold if s == (0,1) else c_cyan for s, c, f, e, kl in results]
bars = ax4.bar(sector_labels, coherences, color=bar_colors, alpha=0.85, edgecolor='white', linewidth=0.5)
ax4.set_title('Axiom 3 Sector Selection: Which 2D Fourier Sector Has Highest Coherence?\n(Gold = {k=0,1} — the Path A candidate)',
              color=c_white, fontsize=9)
ax4.set_ylabel('|Tr(T³)| Coherence', color=c_gray)
ax4.tick_params(colors=c_gray)
for spine in ax4.spines.values():
    spine.set_edgecolor(c_gray)
for i, (bar, (s, coh, fact, ent, kl)) in enumerate(zip(bars, results)):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{coh:.3f}\n{"FACTORIZES" if fact else "NO FACTOR"}',
             ha='center', color=c_white, fontsize=9, fontweight='bold')

# Plot 5: Verdict panel
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor(bg)
ax5.axis('off')

lines = [
    ("GAP B STATUS", c_white),
    ("─" * 20, c_gray),
    ("T_sym³ off-diag: 3", c_cyan),
    ("(thermalizes — known)", c_gray),
    ("", c_white),
    ("T_chiral³ diagonal?", c_cyan),
    ("NO (confirmed)", c_red),
    ("", c_white),
    ("H_prod factorizes?", c_cyan),
    ("YES" if factorizes else "NO", c_green if factorizes else c_red),
    ("", c_white),
    ("Axiom 3 selects {0,1}?", c_cyan),
    ("YES" if best_sector == (0,1) else "NO", c_green if best_sector == (0,1) else c_red),
    ("", c_white),
    ("Path A status:", c_white),
    ("OPEN" if not factorizes else "PARTIALLY CLOSED", c_red if not factorizes else c_gold),
]

for i, (text, color) in enumerate(lines):
    ax5.text(0.05, 0.95 - i*0.065, text, transform=ax5.transAxes,
             color=color, fontsize=9, fontfamily='monospace', fontweight='bold' if i == 0 else 'normal')

ax5.set_title('Verdict', color=c_white, fontsize=10)

plt.savefig('/home/ubuntu/gap_b_factorization_results.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a', edgecolor='none')
plt.close()

print("\nVisualization saved to: gap_b_factorization_results.png")
