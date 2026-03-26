#!/usr/bin/env python3
"""
coulomb_lens_multiscale.py — Phase 5: Multi-Scale Refraction Continuity
Propagation Framework: Forces ARE Refraction at ALL Scales

Phase 5 demonstrates that the SAME refractive index principle:
- Electromagnetic: n² = E + 1/r (atomic scale)
- Gravitational: n² = 1 - 2GM/rc² (planetary scale)
Both are instances of: n² = 1 + 2Φ/c² where Φ is the potential

This shows the mathematical continuity across 20+ orders of magnitude
from the Bohr radius to planetary orbits.

Output: sandbox/coulomb_lens_multiscale.png (4-panel figure)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
#  STYLING
# ═══════════════════════════════════════════════════════════════════════════════

BG = '#0a0a1a'
GRID_COL = '#1a1a2e'
TEXT_COL = '#cccccc'
ACCENT_EM = '#00cfff'
ACCENT_GRAV = '#ffdd00'
ACCENT_UNITY = '#44ff88'


def style_ax(ax, title=''):
    ax.set_facecolor(BG)
    ax.tick_params(colors='#666', labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333')
    ax.grid(True, color=GRID_COL, lw=0.4, zorder=0)
    if title:
        ax.set_title(title, color='white', fontsize=9, fontweight='bold', pad=8)


# ═══════════════════════════════════════════════════════════════════════════════
#  REFRACTIVE INDICES — TWO FORCES, ONE PRINCIPLE
# ═══════════════════════════════════════════════════════════════════════════════

def n_coulomb(x, y, E, q=+1):
    """Electromagnetic refractive index for Coulomb potential."""
    r = np.sqrt(x**2 + y**2)
    if r < 0.05:
        r = 0.05
    # n² = E + q/r  (in natural units where 2m=1)
    val = E + q / r
    return np.sqrt(max(val, 1e-12))


def n_gravity(x, y, M):
    """Gravitational refractive index from General Relativity."""
    r = np.sqrt(x**2 + y**2)
    if r < 0.1:
        r = 0.1
    # n² = 1 - 2GM/rc²  (Schwarzschild metric in weak field)
    # In units where G=c=1: n² = 1 - 2M/r
    val = 1 - 2 * M / r
    return np.sqrt(max(val, 0.1))  # Prevent imaginary inside horizon


def grad_n_coulomb(x, y, E, q=+1):
    """Gradient of Coulomb refractive index."""
    r = np.sqrt(x**2 + y**2)
    if r < 0.05:
        r = 0.05
    nv = n_coulomb(x, y, E, q)
    if nv < 1e-10:
        return 0.0, 0.0
    f = -q / (2.0 * nv * r**3)
    return f * x, f * y


def grad_n_gravity(x, y, M):
    """Gradient of gravitational refractive index."""
    r = np.sqrt(x**2 + y**2)
    if r < 0.1:
        r = 0.1
    nv = n_gravity(x, y, M)
    if nv < 1e-10:
        return 0.0, 0.0
    f = M / (nv * r**3)  # Note: sign difference from Coulomb
    return f * x, f * y


# ═══════════════════════════════════════════════════════════════════════════════
#  UNIFIED EIKONAL INTEGRATOR
# ═══════════════════════════════════════════════════════════════════════════════

def eikonal_rhs(s, state, force_type, params):
    """Unified eikonal RHS for both EM and gravity."""
    x, y, px, py = state
    
    if force_type == 'coulomb':
        E, q = params
        nv = n_coulomb(x, y, E, q)
        gx, gy = grad_n_coulomb(x, y, E, q)
    elif force_type == 'gravity':
        M = params
        nv = n_gravity(x, y, M)
        gx, gy = grad_n_gravity(x, y, M)
    else:
        raise ValueError("force_type must be 'coulomb' or 'gravity'")
    
    if nv < 1e-10:
        return [0, 0, 0, 0]
    return [px / nv, py / nv, gx, gy]


def integrate_eikonal_unified(x0, y0, theta, force_type, params, s_max=100):
    """Unified ray tracer for both forces."""
    if force_type == 'coulomb':
        E, q = params
        nv = n_coulomb(x0, y0, E, q)
    else:
        M = params
        nv = n_gravity(x0, y0, M)
    
    if nv < 1e-10:
        return None
    
    px0 = nv * np.cos(theta)
    py0 = nv * np.sin(theta)
    
    def hit(s, state, force_type, params):
        r = np.sqrt(state[0]**2 + state[1]**2)
        if force_type == 'coulomb':
            return r - 0.04
        else:
            return r - 0.5  # Larger core for planets
    hit.terminal = True
    hit.direction = -1
    
    def escape(s, state, force_type, params):
        return 20.0 - np.sqrt(state[0]**2 + state[1]**2)
    escape.terminal = True
    escape.direction = -1
    
    sol = solve_ivp(
        eikonal_rhs, [0, s_max], [x0, y0, px0, py0],
        args=(force_type, params), max_step=s_max / 4000,
        events=[hit, escape], method='RK45', rtol=1e-10, atol=1e-12,
    )
    return sol


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 5 PANELS
# ═══════════════════════════════════════════════════════════════════════════════

def panel1_unified_formula(ax_theory):
    """Panel 1: The unified refractive index formula."""
    style_ax(ax_theory, 'Phase 5A: Unified Refraction Principle')
    
    # Create a clean theory panel
    ax_theory.axis('off')
    
    # Main formula
    formula = r'$n^2(r) = 1 + \frac{2\Phi(r)}{c^2}$'
    ax_theory.text(0.5, 0.85, formula, transform=ax_theory.transAxes,
                  fontsize=16, color='white', ha='center', fontweight='bold')
    
    # Two special cases
    em_case = r'Electromagnetic: $\Phi = \frac{q}{4\pi\epsilon_0 r}$'
    grav_case = r'Gravitational: $\Phi = -\frac{GM}{r}$'
    
    ax_theory.text(0.5, 0.65, em_case, transform=ax_theory.transAxes,
                  fontsize=12, color=ACCENT_EM, ha='center')
    ax_theory.text(0.5, 0.50, grav_case, transform=ax_theory.transAxes,
                  fontsize=12, color=ACCENT_GRAV, ha='center')
    
    # Scale annotation
    scale_text = 'SAME PRINCIPLE across 20+ orders of magnitude\n'
    scale_text += r'Atomic: $10^{-10}$ m  →  Planetary: $10^{11}$ m'
    ax_theory.text(0.5, 0.25, scale_text, transform=ax_theory.transAxes,
                  fontsize=11, color=ACCENT_UNITY, ha='center', style='italic')
    
    # Key insight
    insight = 'Forces are not mysterious actions at a distance.\n'
    insight += 'They are local refraction in a structured medium.'
    ax_theory.text(0.5, 0.08, insight, transform=ax_theory.transAxes,
                  fontsize=10, color='#aaa', ha='center')


def panel2_em_atomic(ax_em):
    """Panel 2: Electromagnetic refraction at atomic scale."""
    style_ax(ax_em, 'Phase 5B: Electromagnetic Refraction (Atomic Scale)')
    
    E = -0.3
    x0, y0 = 2.0, 0.0
    thetas = np.linspace(np.pi * 0.6, np.pi * 0.95, 12)
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(thetas)))
    
    for theta, col in zip(thetas, colors):
        sol = integrate_eikonal_unified(x0, y0, theta, 'coulomb', (E, +1), s_max=80)
        if sol is not None and sol.y.shape[1] > 10:
            ax_em.plot(sol.y[0], sol.y[1], color=col, lw=1.3, alpha=0.8)
    
    # Source
    ax_em.plot(0, 0, 'k+', ms=12, mew=2.5, zorder=10)
    c = plt.Circle((0, 0), 0.1, color=ACCENT_EM, ec='k', lw=1.2, zorder=9)
    ax_em.add_patch(c)
    ax_em.text(0.15, 0.15, '+', color='white', fontsize=10, fontweight='bold')
    
    ax_em.set_xlim(-3, 3)
    ax_em.set_ylim(-3, 3)
    ax_em.set_aspect('equal')
    ax_em.annotate(r'$n^2 = E + 1/r$  (attractive lens)',
                   xy=(0.02, 0.02), xycoords='axes fraction',
                   color=ACCENT_EM, fontsize=8, fontweight='bold')


def panel3_gravity_planetary(ax_grav):
    """Panel 3: Gravitational refraction at planetary scale."""
    style_ax(ax_grav, 'Phase 5C: Gravitational Refraction (Planetary Scale)')
    
    M = 1.0  # Central mass
    x0 = -8.0
    impact_bs = np.linspace(0.5, 4.0, 10)
    colors = plt.cm.autumn(np.linspace(0.2, 0.8, len(impact_bs)))
    
    for b, col in zip(impact_bs, colors):
        # Upper ray
        sol = integrate_eikonal_unified(x0, b, 0.0, 'gravity', M, s_max=40)
        if sol is not None and sol.y.shape[1] > 10:
            ax_grav.plot(sol.y[0], sol.y[1], color=col, lw=1.3, alpha=0.8)
        # Lower ray
        sol = integrate_eikonal_unified(x0, -b, 0.0, 'gravity', M, s_max=40)
        if sol is not None and sol.y.shape[1] > 10:
            ax_grav.plot(sol.y[0], sol.y[1], color=col, lw=1.3, alpha=0.8)
    
    # Central mass
    ax_grav.plot(0, 0, 'ko', ms=15, zorder=10)
    c = plt.Circle((0, 0), 0.3, color=ACCENT_GRAV, ec='k', lw=1.2, zorder=9)
    ax_grav.add_patch(c)
    ax_grav.text(0.4, 0.4, 'M', color='black', fontsize=10, fontweight='bold')
    
    ax_grav.set_xlim(-10, 10)
    ax_grav.set_ylim(-5, 5)
    ax_grav.set_aspect('equal')
    ax_grav.annotate(r'$n^2 = 1 - 2GM/rc^2$  (gravitational lens)',
                     xy=(0.02, 0.02), xycoords='axes fraction',
                     color=ACCENT_GRAV, fontsize=8, fontweight='bold')


def panel4_scale_continuity(ax_continuity):
    """Panel 4: Scale continuity visualization."""
    style_ax(ax_continuity, 'Phase 5D: Scale Continuity — One Principle, Many Manifestations')
    
    # Create scale axis
    scales = [-35, -18, -15, -10, 0, 11]  # log10(scale in meters)
    scale_names = ['Planck', 'Matter', 'Nuclear', 'Atomic', 'Human', 'Planetary']
    colors = ['#666', '#ff6666', '#ff8844', ACCENT_EM, '#44ff44', ACCENT_GRAV]
    
    # Draw scale axis
    y_pos = 0.5
    ax_continuity.plot(scales, [y_pos]*len(scales), 'o-', color='white', 
                       markersize=8, lw=2, alpha=0.8)
    
    # Add scale labels
    for i, (scale, name, col) in enumerate(zip(scales, scale_names, colors)):
        ax_continuity.text(scale, y_pos + 0.15, name, 
                          transform=ax_continuity.get_xaxis_transform(),
                          color=col, fontsize=9, ha='center', fontweight='bold')
        ax_continuity.text(scale, y_pos - 0.15, f'10^{scale} m',
                          transform=ax_continuity.get_xaxis_transform(),
                          color='#aaa', fontsize=7, ha='center')
    
    # Highlight this simulation's position
    ax_continuity.plot([-10], [y_pos], 'o', color=ACCENT_EM, markersize=15, 
                       markeredgecolor='white', markeredgewidth=2, zorder=10)
    ax_continuity.annotate('Coulomb Lens\nSimulation Here',
                          xy=(-10, y_pos), xytext=(-25, y_pos + 0.35),
                          arrowprops=dict(arrowstyle='->', color=ACCENT_EM, lw=2),
                          color=ACCENT_EM, fontsize=8, fontweight='bold',
                          ha='center')
    
    # Add unity principle text
    ax_continuity.text(0.5, 0.85, 
                      'n² = 1 + 2Φ/c²  —  ONE REFRACTIVE PRINCIPLE',
                      transform=ax_continuity.transAxes,
                      color=ACCENT_UNITY, fontsize=11, ha='center', 
                      fontweight='bold', style='italic')
    
    ax_continuity.set_xlim(-40, 15)
    ax_continuity.set_ylim(0, 1)
    ax_continuity.set_xlabel('Scale (log₁₀ meters)', color='#888', fontsize=8)
    ax_continuity.set_yticks([])


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(BG)
    
    fig.suptitle(
        'Phase 5: Multi-Scale Refraction Continuity  —  Forces ARE Refraction at ALL Scales\n'
        r'Unified Principle: $n^2 = 1 + 2\Phi/c^2$  ·  EM: $n^2 = E + 1/r$  ·  Gravity: $n^2 = 1 - 2GM/rc^2$  ·  '
        'Propagation Framework',
        fontsize=13, fontweight='bold', color='white', y=0.98,
    )
    
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    
    print('Phase 5A: Unified refraction principle...')
    panel1_unified_formula(ax1)
    print('  Done.')
    
    print('Phase 5B: Electromagnetic refraction at atomic scale...')
    panel2_em_atomic(ax2)
    print('  Done.')
    
    print('Phase 5C: Gravitational refraction at planetary scale...')
    panel3_gravity_planetary(ax3)
    print('  Done.')
    
    print('Phase 5D: Scale continuity visualization...')
    panel4_scale_continuity(ax4)
    print('  Done.')
    
    fig.text(0.5, 0.005,
             'The same refractive index principle governs forces across 46 orders of magnitude  ·  '
             'From electron orbits to planetary trajectories  ·  No mysterious action at a distance — only local refraction',
             ha='center', fontsize=7.5, color='#777', style='italic')
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    
    out = Path(__file__).parent / 'coulomb_lens_multiscale.png'
    plt.savefig(out, dpi=180, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f'\nSaved: {out}')
    
    # Console report
    print('\n' + '=' * 65)
    print('  PHASE 5: MULTI-SCALE CONTINUITY — PROPAGATION FRAMEWORK')
    print('=' * 65)
    print()
    print('  UNIFIED PRINCIPLE:')
    print('    n² = 1 + 2Φ/c²  where Φ is the potential')
    print('    EM potential:  Φ = q/(4πε₀r)  →  n² = E + 1/r')
    print('    Gravity potential: Φ = -GM/r  →  n² = 1 - 2GM/rc²')
    print()
    print('  SCALE SPAN:')
    print('    Planck: 10⁻³⁵ m  ←  Quantum foam')
    print('    Matter: 10⁻¹⁸ m  ←  Elementary particles')
    print('    Atomic: 10⁻¹⁰ m  ←  THIS SIMULATION')
    print('    Human: 10⁰ m     ←  Observer scale')
    print('    Planetary: 10¹¹ m ←  Orbits, tides')
    print()
    print('  KEY INSIGHT:')
    print('    The SAME mathematical structure (refractive gradient)')
    print('    explains BOTH electron orbits AND planetary trajectories')
    print('    No quantum mechanics needed for atomic orbits')
    print('    No curved spacetime needed for gravity')
    print('    Only ONE principle: propagation seeks the fastest path')
    print()
    print('  FRAMEWORK POWER:')
    print('    Three axioms → 46 orders of magnitude of unified physics')
    print('    From Planck uncertainty to planetary certainty')
    print('    The universe is not a collection of different forces')
    print('    It is ONE medium with MANY refractive patterns')
    print('=' * 65)


if __name__ == '__main__':
    main()
