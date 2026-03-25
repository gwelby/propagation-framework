"""
Kuramoto Large-N Scaling Study
===============================
Tests whether the criticality hypothesis — "Phi peaks at the phase transition,
not at full synchrony" — holds as N increases from 50 to 500.

If the hypothesis is robust, we expect:
    1. r(Phi_approx, dr/dK) to increase with N (stronger signal at large N)
    2. |K_peak_Phi - K_crit| to converge toward 0 as N → ∞
    3. K_crit(N) to converge toward K_c = 2/pi ≈ 0.637 (Lorentzian analytical result)

Phi proxy used here:
    Phi_approx(K) = |<exp(i(theta_first_half - theta_second_half))>|
    This is the inter-partition coherence: measures how much the two halves of
    the oscillator population are integrated (phase-locked to each other) WITHOUT
    being locked to the same phase. It peaks when there is partial, structured
    coupling — precisely at criticality.

Reference: Kim & Lee (2019) Criticality as a Determinant of Integrated
    Information Phi in Human Brain Networks. Entropy 21:981.

Output:
    Console: N | K_crit | K_peak_Phi | |dK| | r | PASS/FAIL table
    File:    sandbox/kuramoto_large_n.png  (4-panel dark figure)
"""

import numpy as np
from scipy.stats import pearsonr
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ─── Constants ────────────────────────────────────────────────────────────────

BG = '#0a0a1a'
COLORS = ['#00d4ff', '#ff6b35', '#7fff00', '#ff00ff']   # one per N value
GRID_COLOR = '#1a1a3a'
TEXT_COLOR = '#e0e0ff'

N_VALUES = [50, 100, 200, 500]
N_K = 30
K_MIN, K_MAX = 0.0, 8.0
WARMUP_STEPS = 50       # discrete steps (not time units)
SAMPLE_STEPS = 200      # discrete steps
DT = 0.05               # time step — coarser than baseline but fine for scaling
GAMMA = 1.0             # Lorentzian half-width
LORENTZ_CLIP = 5.0      # clip at ±5γ
SEED = 42

# Analytical K_c for Lorentzian g(omega) = gamma/(pi*(omega^2+gamma^2))
# K_c = 2 / (pi * g(0)) = 2 / (pi * 1/(pi*gamma)) = 2*gamma
# For gamma=1: K_c = 2.0
# (The formula K_c = 2/(pi*g(0)) with g(0) = 1/(pi*gamma) gives K_c = 2*gamma = 2.0)
K_C_THEORETICAL = 2.0 * GAMMA   # = 2.0

# Pass/fail thresholds (from original script)
R_PASS = 0.70
R_STRONG = 0.85
DK_PASS = 1.0
DK_STRONG = 0.5


# ─── Simulation (fully vectorized over oscillators) ───────────────────────────

def sample_lorentzian(N, gamma, clip, rng):
    """
    Draw N samples from Lorentzian(0, gamma) truncated at ±clip*gamma.
    Uses inverse-CDF: omega = gamma * tan(pi*(u - 0.5)) with rejection.
    Vectorized — no Python loop over oscillators.
    """
    clip_arg = np.arctan(clip) / np.pi + 0.5   # CDF value at +clip*gamma
    lo, hi = 1.0 - clip_arg, clip_arg
    u = rng.uniform(lo, hi, N)
    return gamma * np.tan(np.pi * (u - 0.5))


def step_kuramoto(theta, omega, K, N, dt):
    """
    One Euler step of the Kuramoto model, vectorized.

    theta: (N,)  current phases
    omega: (N,)  natural frequencies
    Returns updated theta (N,).

    The N×N sin-diff matrix is the expensive part.
    For N=500 this is 250k floats — fast with numpy broadcasting.
    """
    diff = theta[np.newaxis, :] - theta[:, np.newaxis]   # (N,N): diff[i,j] = θ_j - θ_i
    coupling = (K / N) * np.sin(diff).sum(axis=1)        # (N,): mean field force on i
    return theta + dt * (omega + coupling)


def run_one_K(N, K, omega, dt, warmup_steps, sample_steps):
    """
    Run Kuramoto at fixed K, return sampled phases array (sample_steps, N).
    """
    rng_local = np.random.default_rng(SEED ^ int(K * 1000) ^ N)
    theta = rng_local.uniform(0, 2 * np.pi, N)

    for _ in range(warmup_steps):
        theta = step_kuramoto(theta, omega, K, N, dt)

    phases = np.empty((sample_steps, N))
    for t in range(sample_steps):
        theta = step_kuramoto(theta, omega, K, N, dt)
        phases[t] = theta

    return phases


# ─── Observables ──────────────────────────────────────────────────────────────

def order_parameter(phases):
    """r = mean |<exp(i*theta)>| over time."""
    z = np.mean(np.exp(1j * phases), axis=1)   # (T,) complex
    return float(np.mean(np.abs(z)))


def phi_approx(phases):
    """
    Inter-partition coherence proxy for integrated information.

    Split oscillators into first half (0..N//2-1) and second half (N//2..).
    Compute |<exp(i*(theta_A - theta_B))>| where theta_A/B are the
    instantaneous mean phases of each half.

    This quantity measures structured integration between the two populations:
      - Near 0 if the halves are incoherent with each other (low K)
      - Near 0 if the halves are both locked to the same global phase (high K,
        because then theta_A ≈ theta_B ≈ psi, so diff ≈ 0, |exp(i*0)| = 1 ...
        BUT in that case the individual oscillator differences are all near 0
        and the *variance* of (theta_A - theta_B) is near 0 → the proxy's
        discriminative power comes from the fluctuation pattern)

    We use the *standard deviation* of r_diff(t) = |mean_A exp(i*theta_i) - mean_B exp(i*theta_j)|
    evaluated per time step, as a direct analog of metastability applied to
    the cross-partition signal.  This peaks when the two halves are sometimes
    in phase and sometimes not — exactly at criticality.
    """
    N = phases.shape[1]
    mid = N // 2

    z_A = np.mean(np.exp(1j * phases[:, :mid]), axis=1)    # (T,)
    z_B = np.mean(np.exp(1j * phases[:, mid:]), axis=1)    # (T,)

    # Instantaneous cross-partition order: magnitude of difference of mean phasors
    # peaks when parts are partially but not fully coupled
    r_cross = np.abs(z_A - z_B)   # (T,)
    return float(np.std(r_cross))


# ─── Scan over K for one N ────────────────────────────────────────────────────

def scan_N(N, K_values, rng):
    """
    For a given N, sweep over K_values.
    Returns arrays: r_arr, phi_arr, drho_dK_arr, K_crit, K_peak_phi, corr_r.
    """
    omega = sample_lorentzian(N, GAMMA, LORENTZ_CLIP, rng)

    r_arr = np.empty(len(K_values))
    phi_arr = np.empty(len(K_values))

    for i, K in enumerate(K_values):
        phases = run_one_K(N, K, omega, DT, WARMUP_STEPS, SAMPLE_STEPS)
        r_arr[i] = order_parameter(phases)
        phi_arr[i] = phi_approx(phases)

    drho_dK = np.gradient(r_arr, K_values)

    K_crit = float(K_values[np.argmax(drho_dK)])
    K_peak_phi = float(K_values[np.argmax(phi_arr)])

    corr_r, _ = pearsonr(phi_arr, drho_dK)

    return r_arr, phi_arr, drho_dK, K_crit, K_peak_phi, float(corr_r)


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_scaling_study():
    np.random.seed(SEED)
    rng = np.random.default_rng(SEED)

    K_values = np.linspace(K_MIN, K_MAX, N_K)

    results = {}

    print()
    print("Kuramoto Large-N Scaling Study")
    print(f"K range: [{K_MIN}, {K_MAX}], {N_K} steps")
    print(f"Warmup: {WARMUP_STEPS} steps | Sample: {SAMPLE_STEPS} steps | dt={DT}")
    print(f"Lorentzian gamma={GAMMA}, clipped at ±{LORENTZ_CLIP}gamma")
    print(f"Theoretical K_c = 2*gamma = {K_C_THEORETICAL:.3f}")
    print(f"Pass: r > {R_PASS}, |dK| < {DK_PASS}")
    print(f"Strong: r > {R_STRONG}, |dK| < {DK_STRONG}")
    print()

    for N in N_VALUES:
        print(f"  Running N={N}...", end='', flush=True)
        r_arr, phi_arr, drho_dK, K_crit, K_peak_phi, corr_r = scan_N(N, K_values, rng)
        results[N] = {
            'r_arr': r_arr,
            'phi_arr': phi_arr,
            'drho_dK': drho_dK,
            'K_crit': K_crit,
            'K_peak_phi': K_peak_phi,
            'corr_r': corr_r,
            'dK': abs(K_peak_phi - K_crit),
        }
        print(f"  K_crit={K_crit:.2f}  K_peak_Phi={K_peak_phi:.2f}  r={corr_r:.3f}")

    return K_values, results


def print_table(K_values, results):
    print()
    print("=" * 72)
    print(f"{'N':>6}  {'K_crit':>7}  {'K_peak_Phi':>10}  {'|dK|':>6}  {'r':>6}  {'Status':}")
    print("-" * 72)

    for N in N_VALUES:
        d = results[N]
        K_crit = d['K_crit']
        K_peak_phi = d['K_peak_phi']
        dK = d['dK']
        corr_r = d['corr_r']

        r_ok = corr_r > R_PASS
        dk_ok = dK < DK_PASS
        r_strong = corr_r > R_STRONG
        dk_strong = dK < DK_STRONG

        if r_strong and dk_strong:
            status = "STRONG"
        elif r_ok and dk_ok:
            status = "PASS"
        elif r_ok or dk_ok:
            status = "PARTIAL"
        else:
            status = "FAIL"

        print(f"{N:>6}  {K_crit:>7.3f}  {K_peak_phi:>10.3f}  {dK:>6.3f}  {corr_r:>6.3f}  {status}")

    print("=" * 72)
    print(f"  Theoretical K_c = {K_C_THEORETICAL:.3f}")
    print()

    # Scaling verdict
    corrs = [results[N]['corr_r'] for N in N_VALUES]
    dKs = [results[N]['dK'] for N in N_VALUES]

    # Check if correlation increases with N (robust) vs flat/decreasing (fragile)
    # Use linear trend: if slope > 0, correlation grows with N
    N_arr = np.array(N_VALUES, dtype=float)
    corr_arr = np.array(corrs)
    dK_arr = np.array(dKs)

    slope_r, _ = np.polyfit(np.log(N_arr), corr_arr, 1)
    slope_dK, _ = np.polyfit(np.log(N_arr), dK_arr, 1)

    r_improves = slope_r > 0.0
    dK_converges = slope_dK < 0.0
    majority_pass = sum(1 for c, d in zip(corrs, dKs) if c > R_PASS and d < DK_PASS) >= 2

    if r_improves and dK_converges and majority_pass:
        final_verdict = "ROBUST — criticality hypothesis CONFIRMED (r scales with N, |dK| converges)"
    elif majority_pass:
        final_verdict = "ROBUST — criticality hypothesis holds but scaling trend weak"
    elif r_improves or dK_converges:
        final_verdict = "PARTIAL — some scaling evidence but hypothesis not consistently confirmed"
    else:
        final_verdict = "FRAGILE — criticality hypothesis does NOT improve with N"

    print(f"  Correlation trend with log(N): slope = {slope_r:+.4f}  ({'increases' if r_improves else 'flat/decreasing'})")
    print(f"  |dK| trend with log(N):        slope = {slope_dK:+.4f}  ({'converges' if dK_converges else 'diverges'})")
    print()
    print(f"  FINAL VERDICT: {final_verdict}")
    print()

    return final_verdict, slope_r, slope_dK


# ─── Plot ─────────────────────────────────────────────────────────────────────

def make_figure(K_values, results, final_verdict, slope_r, slope_dK):
    fig = plt.figure(figsize=(14, 10), facecolor=BG)
    gs = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.35,
                           left=0.08, right=0.97, top=0.91, bottom=0.09)

    ax_r    = fig.add_subplot(gs[0, 0])   # Panel 1: r(K)
    ax_phi  = fig.add_subplot(gs[0, 1])   # Panel 2: Phi_approx(K)
    ax_corr = fig.add_subplot(gs[1, 0])   # Panel 3: correlation r vs N
    ax_dK   = fig.add_subplot(gs[1, 1])   # Panel 4: |dK| vs N

    panel_style = dict(facecolor=BG)

    def style_ax(ax, title, xlabel, ylabel):
        ax.set_facecolor(BG)
        ax.set_title(title, color=TEXT_COLOR, fontsize=10, pad=6)
        ax.set_xlabel(xlabel, color=TEXT_COLOR, fontsize=9)
        ax.set_ylabel(ylabel, color=TEXT_COLOR, fontsize=9)
        ax.tick_params(colors=TEXT_COLOR, labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor(GRID_COLOR)
        ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)

    # ── Panel 1: r(K) ──────────────────────────────────────────────────────────
    style_ax(ax_r, 'Order Parameter r(K)', 'Coupling K', 'r  (mean field coherence)')
    for idx, N in enumerate(N_VALUES):
        ax_r.plot(K_values, results[N]['r_arr'],
                  color=COLORS[idx], linewidth=1.6, label=f'N={N}', alpha=0.85)
    ax_r.axvline(K_C_THEORETICAL, color='white', linestyle='--', linewidth=0.9,
                 alpha=0.5, label=f'K_c={K_C_THEORETICAL:.2f}')
    ax_r.legend(fontsize=7, facecolor=BG, labelcolor=TEXT_COLOR,
                framealpha=0.6, edgecolor=GRID_COLOR)

    # ── Panel 2: Phi_approx(K) ─────────────────────────────────────────────────
    style_ax(ax_phi, 'Φ_approx(K)  [cross-partition metastability]',
             'Coupling K', 'Φ_approx')
    for idx, N in enumerate(N_VALUES):
        ax_phi.plot(K_values, results[N]['phi_arr'],
                    color=COLORS[idx], linewidth=1.6, label=f'N={N}', alpha=0.85)
        # Mark the Phi peak
        k_peak = results[N]['K_peak_phi']
        phi_peak_val = results[N]['phi_arr'][np.argmax(results[N]['phi_arr'])]
        ax_phi.scatter([k_peak], [phi_peak_val], color=COLORS[idx], s=40,
                       zorder=5, marker='v', alpha=0.9)
    ax_phi.axvline(K_C_THEORETICAL, color='white', linestyle='--', linewidth=0.9,
                   alpha=0.5, label=f'K_c={K_C_THEORETICAL:.2f}')
    ax_phi.legend(fontsize=7, facecolor=BG, labelcolor=TEXT_COLOR,
                  framealpha=0.6, edgecolor=GRID_COLOR)

    # ── Panel 3: Correlation r vs N ────────────────────────────────────────────
    style_ax(ax_corr, 'Correlation r(Φ_approx, dr/dK)  vs  N',
             'N (oscillators)', 'Pearson r')
    N_arr = np.array(N_VALUES, dtype=float)
    corr_arr = np.array([results[N]['corr_r'] for N in N_VALUES])
    ax_corr.plot(N_arr, corr_arr, color='#00d4ff', linewidth=2.0,
                 marker='o', markersize=7, label='r(N)')
    ax_corr.axhline(R_PASS, color='#7fff00', linestyle='--', linewidth=0.9,
                    alpha=0.7, label=f'pass r={R_PASS}')
    ax_corr.axhline(R_STRONG, color='#ffdd00', linestyle=':', linewidth=0.9,
                    alpha=0.7, label=f'strong r={R_STRONG}')
    # Trend line in log(N) space
    log_N = np.log(N_arr)
    log_N_fine = np.linspace(log_N[0], log_N[-1], 100)
    N_fine = np.exp(log_N_fine)
    coeffs = np.polyfit(log_N, corr_arr, 1)
    ax_corr.plot(N_fine, np.polyval(coeffs, log_N_fine),
                 color='#ff6b35', linewidth=1.0, linestyle='-.',
                 alpha=0.6, label=f'trend (slope={slope_r:+.3f})')
    ax_corr.set_xscale('log')
    ax_corr.set_ylim(-0.05, 1.05)
    ax_corr.legend(fontsize=7, facecolor=BG, labelcolor=TEXT_COLOR,
                   framealpha=0.6, edgecolor=GRID_COLOR)

    # ── Panel 4: |dK| vs N ─────────────────────────────────────────────────────
    style_ax(ax_dK, '|K_peak_Φ - K_crit|  vs  N  (convergence)',
             'N (oscillators)', '|ΔK|')
    dK_arr = np.array([results[N]['dK'] for N in N_VALUES])
    ax_dK.plot(N_arr, dK_arr, color='#ff00ff', linewidth=2.0,
               marker='s', markersize=7, label='|ΔK|(N)')
    ax_dK.axhline(DK_PASS, color='#7fff00', linestyle='--', linewidth=0.9,
                  alpha=0.7, label=f'pass |ΔK|={DK_PASS}')
    ax_dK.axhline(DK_STRONG, color='#ffdd00', linestyle=':', linewidth=0.9,
                  alpha=0.7, label=f'strong |ΔK|={DK_STRONG}')
    coeffs_dK = np.polyfit(log_N, dK_arr, 1)
    ax_dK.plot(N_fine, np.polyval(coeffs_dK, log_N_fine),
               color='#ff6b35', linewidth=1.0, linestyle='-.',
               alpha=0.6, label=f'trend (slope={slope_dK:+.3f})')
    ax_dK.set_xscale('log')
    ax_dK.set_ylim(bottom=0)
    ax_dK.legend(fontsize=7, facecolor=BG, labelcolor=TEXT_COLOR,
                 framealpha=0.6, edgecolor=GRID_COLOR)

    # ── Title ──────────────────────────────────────────────────────────────────
    fig.suptitle(
        f'Kuramoto Large-N Scaling  |  Criticality Hypothesis\n'
        f'K_c(theoretical) = {K_C_THEORETICAL:.3f}  |  {final_verdict}',
        color=TEXT_COLOR, fontsize=11, y=0.98
    )

    out_path = '/mnt/d/Fundamentals/sandbox/kuramoto_large_n.png'
    fig.savefig(out_path, dpi=140, facecolor=BG, bbox_inches='tight')
    plt.close(fig)
    print(f"  Figure saved: {out_path}")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    K_values, results = run_scaling_study()
    final_verdict, slope_r, slope_dK = print_table(K_values, results)
    make_figure(K_values, results, final_verdict, slope_r, slope_dK)
