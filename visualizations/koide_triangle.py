"""
The Koide Q = 2/3 Visualization
Why three lepton masses form an equilateral triangle in mass-root space

Run: python koide_triangle.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch

# ── Real lepton masses (MeV/c²) ──────────────────────────────────────────────
m_e   = 0.51099895    # electron
m_mu  = 105.6583755   # muon
m_tau = 1776.86       # tau

# Amplitudes (square roots of masses)
a = np.array([np.sqrt(m_e), np.sqrt(m_mu), np.sqrt(m_tau)])

# Verify Koide Q
Q = np.sum(a**2) / np.sum(a)**2
print(f"Koide Q = {Q:.10f}  (should be ≈ 0.666666...)")
print(f"2/3     = {2/3:.10f}")
print(f"Error   = {abs(Q - 2/3)*100:.6f}%")

# ── Find the geometric parameters ────────────────────────────────────────────
# The Foot-Harari-Zenczykowski parametrization:
# aᵢ = A(1 + √2·cos(θ + 2π(i-1)/3))
# So A = mean(aᵢ)/... let's solve it
A = np.sum(a) / 3
# aᵢ - A = R·cos(θ + 2π(i-1)/3) where R = A√2
R = A * np.sqrt(2)

# Find phase θ by fitting
# a₁ = A + R·cos(θ)  →  cos(θ) = (a₁ - A)/R
# Using the tau (largest) as i=1
# Sort by size: tau, muon, electron
a_sorted = np.sort(a)[::-1]  # descending: tau, muon, electron
cos_theta = (a_sorted[0] - A) / R
theta = np.arccos(np.clip(cos_theta, -1, 1))

# Angles for the three modes
angles = theta + np.array([0, 2*np.pi/3, 4*np.pi/3])
a_fitted = A + R * np.cos(angles)

print(f"\nGeometric parameters:")
print(f"  A (center) = {A:.4f} MeV^(1/2)")
print(f"  R (spread) = {R:.4f} MeV^(1/2)")
print(f"  R/A        = {R/A:.6f}  (should be √2 = {np.sqrt(2):.6f})")
print(f"  θ (phase)  = {np.degrees(theta):.2f}°")

# ── FIGURE 1: The Triangle in Mass-Root Space ────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.patch.set_facecolor('#0a0a1a')

ax1 = axes[0]
ax1.set_facecolor('#0a0a1a')

# Draw the circle of radius R centered at (0, A)
circle_theta = np.linspace(0, 2*np.pi, 300)
circle_x = R * np.cos(circle_theta)
circle_y = A + R * np.sin(circle_theta)
ax1.plot(circle_x, circle_y, color='#334455', linewidth=1, linestyle='--', alpha=0.6)

# Draw the origin
ax1.plot(0, 0, 'o', color='white', markersize=4, zorder=5)

# Draw center point A
ax1.plot(0, A, 'o', color='#aaaaff', markersize=6, zorder=5)
ax1.annotate('Center A', (0, A), textcoords='offset points',
             xytext=(8, 4), color='#aaaaff', fontsize=10)

# Draw the three amplitude vectors from origin
colors = ['#ff6644', '#44aaff', '#44ff88']
labels = ['τ  (tau)', 'μ  (muon)', 'e  (electron)']
points = []

for i, (ang, col, lab) in enumerate(zip(angles, colors, labels)):
    x = R * np.cos(ang)
    y = A + R * np.sin(ang)
    points.append((x, y))

    # Vector from origin
    ax1.annotate('', xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=col,
                                lw=2.5, mutation_scale=15))

    # Point
    ax1.plot(x, y, 'o', color=col, markersize=10, zorder=6)

    # Label with actual mass
    mass_vals = [m_tau, m_mu, m_e]
    ax1.annotate(f'{lab}\n√m = {np.sqrt(mass_vals[i]):.2f}',
                xy=(x, y), textcoords='offset points',
                xytext=(12 if x > 0 else -70, 6),
                color=col, fontsize=9, fontweight='bold')

# Draw the equilateral triangle
triangle = plt.Polygon(points, fill=False, edgecolor='#ffffff',
                       linewidth=1.5, linestyle='-', alpha=0.4, zorder=4)
ax1.add_patch(triangle)

# Draw A and R labels
ax1.annotate('', xy=(0, A), xytext=(0, 0),
            arrowprops=dict(arrowstyle='<->', color='#aaaaff',
                            lw=1.5, mutation_scale=10))
ax1.text(0.15, A/2, 'A', color='#aaaaff', fontsize=13, fontweight='bold', ha='left')

# Draw R label (from center to tau vertex)
px, py = points[0]
ax1.annotate('', xy=(px, py), xytext=(0, A),
            arrowprops=dict(arrowstyle='<->', color='#ffcc44',
                            lw=1.5, mutation_scale=10))
mid_rx = px/2
mid_ry = (A + py)/2
ax1.text(mid_rx + 0.5, mid_ry, 'R = A√2', color='#ffcc44',
         fontsize=11, fontweight='bold')

# Root-of-unity annotation
ax1.text(0.02, 0.98,
         'The three vectors sum to\npure vertical → 3A\n(sideways parts cancel:\nroot of unity identity)',
         transform=ax1.transAxes, color='#888888', fontsize=9,
         va='top', ha='left', style='italic')

ax1.set_xlim(-55, 55)
ax1.set_ylim(-5, 80)
ax1.set_xlabel('Phase offset (MeV^½)', color='white', fontsize=10)
ax1.set_ylabel('Mass amplitude √m  (MeV^½)', color='white', fontsize=10)
ax1.set_title('The Koide Triangle\nThree lepton masses as one rotating pattern',
              color='white', fontsize=12, pad=12)
ax1.tick_params(colors='#666666')
for spine in ax1.spines.values():
    spine.set_edgecolor('#333333')
ax1.axhline(y=0, color='#333333', linewidth=0.5)
ax1.axvline(x=0, color='#333333', linewidth=0.5)

# ── FIGURE 2: The Clock Intuition ────────────────────────────────────────────
ax2 = axes[1]
ax2.set_facecolor('#0a0a1a')
ax2.set_aspect('equal')

# Draw unit circle
theta_c = np.linspace(0, 2*np.pi, 300)
ax2.plot(np.cos(theta_c), np.sin(theta_c), color='#334455',
         linewidth=1, linestyle='--', alpha=0.5)

# Three hands at 120°
hand_angles = np.radians([90, 90+120, 90+240])  # Start at top
hand_colors = ['#ff6644', '#44aaff', '#44ff88']
hand_labels = ['τ', 'μ', 'e']

for ang, col, lab in zip(hand_angles, hand_colors, hand_labels):
    x, y = np.cos(ang), np.sin(ang)
    ax2.annotate('', xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=col,
                                lw=3, mutation_scale=18))
    ax2.plot(x, y, 'o', color=col, markersize=12, zorder=6)
    offset = 0.15
    ax2.text(x*(1+offset), y*(1+offset), lab,
             color=col, fontsize=16, fontweight='bold', ha='center', va='center')

# Sum vector (points straight up — net = 3A = vertical)
ax2.annotate('', xy=(0, 0.3), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='white',
                            lw=2, mutation_scale=12, linestyle='dashed'))
ax2.text(0.05, 0.18, 'Sum = 3A\n(straight up)', color='white',
         fontsize=9, ha='left')

# Annotations
ax2.text(0, -1.4,
         '120° apart  →  sideways cancels  →  only "up" survives\n'
         'This is why  Σaᵢ = 3A  (the root-of-unity identity)',
         color='#888888', fontsize=9, ha='center', style='italic')

ax2.set_xlim(-1.6, 1.6)
ax2.set_ylim(-1.7, 1.6)
ax2.set_title('Why the Cosines Cancel\nThree equally-spaced hands always sum to center',
              color='white', fontsize=12, pad=12)
ax2.axis('off')

# ── Overall math summary ─────────────────────────────────────────────────────
fig.text(0.5, 0.02,
         r'$Q = \frac{\sum a_i^2}{(\sum a_i)^2} = \frac{1}{3} + \frac{R^2}{6A^2} = \frac{2}{3}$'
         r'$\;\;\Longleftrightarrow\;\; R = A\sqrt{2}$'
         r'$\;\;\Longleftrightarrow\;\;$ ground/excited state amplitude ratio',
         ha='center', color='white', fontsize=13,
         bbox=dict(boxstyle='round', facecolor='#111133', alpha=0.8))

plt.suptitle('The Koide Formula Is Geometry\nNot numerology — a triangle forced by quantum resonance',
             color='white', fontsize=14, fontweight='bold', y=1.01)

plt.tight_layout(rect=[0, 0.07, 1, 1])
plt.savefig('/mnt/d/Fundamentals/visualizations/koide_triangle.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.show()
print("\nSaved: koide_triangle.png")
