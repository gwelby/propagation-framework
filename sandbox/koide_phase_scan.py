"""
koide_phase_scan.py
-------------------
Systematic scan for what physical constraint selects the Koide phase δ₀ ≈ 2/9 rad.

Parametrization (Brannen 2006):
  √m_k = A(1 + √2 cos(δ + 2πk/3))   k=0,1,2
  Q = 2/3 is satisfied by construction (cos terms sum to zero).

Mass assignment: k=0→τ, k=1→e, k=2→μ  →  δ_exact ≈ 2/9 ≈ 0.2222 rad.

PDG 2024 lepton masses (MeV):
  m_e = 0.51099895,  m_μ = 105.6583755,  m_τ = 1776.86

PDG 2024 quark masses (MeV):
  u=2.16, d=4.67, s=93.4, c=1270, b=4180, t=172690

OUTPUT:
  Console: step-by-step report for all five sections.
  File:    sandbox/koide_phase_scan.png  (4-panel dark figure)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# PHYSICAL CONSTANTS
# ─────────────────────────────────────────────────────────────
M_E   = 0.51099895      # MeV
M_MU  = 105.6583755     # MeV
M_TAU = 1776.86         # MeV

M_U = 2.16
M_D = 4.67
M_S = 93.4
M_C = 1270.0
M_B = 4180.0
M_T = 172690.0

SIN2_THETA_W = 0.22310   # Weinberg angle (Casimir-derived value)
V_EW         = 246000.0  # electroweak vev in MeV

# Plot colours
BG      = '#0a0a1a'
C_K0    = '#ffcc00'    # k=0 (heavy)
C_K1    = '#00ffcc'    # k=1 (light)
C_K2    = '#ff6688'    # k=2 (mid)
C_MARK  = '#ffffff'
C_REF   = '#ff88ff'
C_SHADE = '#88aaff'


# ═══════════════════════════════════════════════════════════════
# CORE PARAMETRIZATION
# ═══════════════════════════════════════════════════════════════

def reconstruct_masses(A, delta):
    """
    k=0→m[0], k=1→m[1], k=2→m[2].
    Returns array [m_k0, m_k1, m_k2].
    With k=(τ=0, e=1, μ=2): returns [m_τ, m_e, m_μ].
    """
    k = np.array([0.0, 1.0, 2.0])
    sqm = A * (1.0 + np.sqrt(2.0) * np.cos(delta + 2.0 * np.pi * k / 3.0))
    return sqm ** 2


def koide_Q(m0, m1, m2):
    """Koide Q ratio from three masses (order irrelevant)."""
    ms = np.array([m0, m1, m2], dtype=float)
    return ms.sum() / np.sum(np.sqrt(np.abs(ms))) ** 2


def extract_A_delta(m_k0, m_k1, m_k2):
    """
    Analytical extraction of A and δ from three masses in k=(0,1,2) order.

    From √m_k = A(1 + √2 cos(δ + 2πk/3)):
      A     = mean(√m_k)
      exp(iδ) ∝ Σ_k √m_k exp(−i2πk/3)    [DFT at frequency 1]

    Returns (A, delta) with delta ∈ [0, 2π).
    """
    s = np.array([np.sqrt(m_k0), np.sqrt(m_k1), np.sqrt(m_k2)])
    A = s.mean()
    omega = np.exp(2j * np.pi / 3.0)
    # Fourier mode at k=1 uses exp(−i2πk/3) = conj(omega)^k
    c = s[0] * 1.0 + s[1] * np.conj(omega) + s[2] * np.conj(omega) ** 2
    return A, float(np.angle(c)) % (2.0 * np.pi)


# ═══════════════════════════════════════════════════════════════
# RATIONAL APPROXIMATION UTILITIES
# ═══════════════════════════════════════════════════════════════

def continued_fraction(x, max_terms=14, max_denom=1000):
    """Convergents of the continued fraction for x."""
    terms, convergents = [], []
    h0, k0 = 1, 0
    h1, k1 = 0, 1
    val = float(x)
    for _ in range(max_terms):
        a = int(val)
        terms.append(a)
        h2 = a * h1 + h0
        k2 = a * k1 + k0
        convergents.append((h2, k2))
        h0, k0 = h1, k1
        h1, k1 = h2, k2
        rem = val - a
        if abs(rem) < 1e-13 or k2 > max_denom:
            break
        val = 1.0 / rem
    return terms, convergents


def best_rational(x, max_denom=100):
    """Best p/q with 0 < q <= max_denom minimising |x - p/q|."""
    best_err, best_p, best_q = np.inf, 0, 1
    for q in range(1, max_denom + 1):
        p = round(x * q)
        err = abs(x - p / q)
        if err < best_err:
            best_err, best_p, best_q = err, p, q
    return best_p, best_q, best_err


# ═══════════════════════════════════════════════════════════════
# SECTION 1 — EMPIRICAL CALIBRATION
# ═══════════════════════════════════════════════════════════════

def section1():
    print("=" * 70)
    print("SECTION 1: EMPIRICAL CALIBRATION")
    print("=" * 70)

    # k=(τ=0, e=1, μ=2): extract δ using DFT formula with exp(-i2πk/3)
    A, delta = extract_A_delta(M_TAU, M_E, M_MU)

    m_rec = reconstruct_masses(A, delta)
    Q_val = koide_Q(*m_rec)

    print(f"\nPDG 2024:  m_e={M_E}, m_μ={M_MU}, m_τ={M_TAU}  (MeV)")
    print(f"\nExtraction with k=(τ=0, e=1, μ=2):")
    print(f"  A     = {A:.12f}  MeV^(1/2)")
    print(f"  δ     = {delta:.12f}  rad")
    print(f"\nReconstruction check (m_rec = reconstruct_masses(A, δ)):")
    print(f"  m_τ(rec) = {m_rec[0]:.8f}   PDG = {M_TAU:.8f}   Δ = {m_rec[0]-M_TAU:+.3e}")
    print(f"  m_e(rec) = {m_rec[1]:.8f}   PDG = {M_E:.8f}   Δ = {m_rec[1]-M_E:+.3e}")
    print(f"  m_μ(rec) = {m_rec[2]:.8f}   PDG = {M_MU:.8f}   Δ = {m_rec[2]-M_MU:+.3e}")
    print(f"  Q        = {Q_val:.15f}   (2/3 = {2/3:.15f})")
    print(f"  |Q-2/3|  = {abs(Q_val - 2/3):.2e}")

    # Note: small reconstruction error is because m_τ PDG is the less precise value
    # The formula gives Q=2/3 exactly but each mass individually has a small residual.

    dref  = 2.0 / 9.0                   # 2/9 rad (not fraction of 2π)
    d2pi  = delta / (2.0 * np.pi)       # delta as fraction of 2π
    dpi   = delta / np.pi               # delta as fraction of π

    print(f"\nPhase forms:")
    print(f"  δ          = {delta:.12f}  rad")
    print(f"  2/9 rad    = {dref:.12f}  rad  (reference)")
    print(f"  |δ - 2/9|  = {abs(delta - dref):.4e}  rad  ({abs(delta - dref)/dref*100:.6f}%)")
    print(f"  δ/(2π)     = {d2pi:.12f}")
    print(f"  δ/π        = {dpi:.12f}")
    print(f"  cos δ      = {np.cos(delta):.12f}")
    print(f"  sin δ      = {np.sin(delta):.12f}")
    print(f"  cos 3δ     = {np.cos(3*delta):.12f}")
    print(f"  sin 3δ     = {np.sin(3*delta):.12f}")

    # Continued fractions — δ itself (in rad)
    print(f"\nContinued fraction for δ = {delta:.12f} rad:")
    terms, convs = continued_fraction(delta, max_terms=14, max_denom=500)
    print(f"  CF terms: {terms}")
    for i, (p, q) in enumerate(convs[:10]):
        if q <= 0:
            continue
        val = p / q
        err = abs(delta - val)
        rel = err / delta * 100.0
        tag = "  <── 2/9" if (p == 2 and q == 9) else ""
        print(f"  [{i}] {p}/{q:<8} = {val:.10f}   err={err:.2e}  ({rel:.4f}%){tag}")

    print(f"\nBest rational approximations for δ (rad):")
    for md in [9, 12, 18, 24, 36]:
        p, q, err = best_rational(delta, max_denom=md)
        rel = err / delta * 100.0
        tag = "  <── 2/9" if (p == 2 and q == 9) else ""
        print(f"  q≤{md:2d}:  {p}/{q} = {p/q:.10f}   err={err:.2e}  ({rel:.4f}%){tag}")

    # Also for δ/π
    print(f"\nContinued fraction for δ/π = {dpi:.12f}:")
    terms2, convs2 = continued_fraction(dpi, max_terms=10, max_denom=200)
    print(f"  CF terms: {terms2}")
    for i, (p, q) in enumerate(convs2[:7]):
        if q <= 0:
            continue
        val = p / q
        err = abs(dpi - val)
        print(f"  [{i}] {p}/{q:<8} = {val:.10f}   err={err:.2e}")

    return A, delta


# ═══════════════════════════════════════════════════════════════
# SECTION 2 — MASS-ORDERING CONSTRAINT
# ═══════════════════════════════════════════════════════════════

def section2(A_ref, delta_exact):
    print("\n" + "=" * 70)
    print("SECTION 2: MASS-ORDERING CONSTRAINT")
    print("=" * 70)
    print("\nk=(τ=0, e=1, μ=2). Scan δ ∈ [0,2π). Mark where m_τ > m_μ > m_e > 0.")

    N = 10000
    dscan = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
    ms    = np.array([reconstruct_masses(A_ref, d) for d in dscan])   # (N, 3): [τ, e, μ]

    m_tau = ms[:, 0]
    m_e   = ms[:, 1]
    m_mu  = ms[:, 2]

    valid = (m_tau > m_mu) & (m_mu > m_e) & (m_e > 0.0)

    vd = dscan[valid]
    print(f"\nδ regions where m_τ > m_μ > m_e > 0:")
    if len(vd) > 0:
        # Find contiguous regions
        breaks = np.where(np.diff(valid.astype(int)) != 0)[0]
        start = 0
        regions = []
        in_region = valid[0]
        for brk in breaks:
            if in_region:
                regions.append((dscan[start], dscan[brk]))
            in_region = not in_region
            start = brk + 1
        if in_region:
            regions.append((dscan[start], dscan[-1]))
        for lo, hi in regions:
            print(f"  [{lo:.6f}, {hi:.6f}] rad  =  [{lo/(2*np.pi):.4f}, {hi/(2*np.pi):.4f}] × 2π")
        frac = len(vd) / N
        print(f"  Total valid fraction: {frac:.4f}  ({frac*100:.2f}%)")
        print(f"  → Ordering is a necessary but insufficient constraint ({frac*100:.1f}% of phase space).")
    else:
        print("  [None found — check convention]")

    idx = int(np.argmin(np.abs(dscan - delta_exact)))
    print(f"\n  δ_exact = {delta_exact:.6f} rad  ({delta_exact/(2*np.pi):.6f} × 2π)")
    print(f"  In valid region? {bool(valid[idx])}")
    print(f"  m_τ(δ_exact)={m_tau[idx]:.4f},  m_μ(δ_exact)={m_mu[idx]:.4f},  m_e(δ_exact)={m_e[idx]:.6f}  (MeV)")

    return dscan, ms, valid


# ═══════════════════════════════════════════════════════════════
# SECTION 3 — TOP-YUKAWA COUPLING TEST
# ═══════════════════════════════════════════════════════════════

def section3(delta_lepton):
    print("\n" + "=" * 70)
    print("SECTION 3: TOP-YUKAWA COUPLING TEST")
    print("=" * 70)

    y_t = M_T * np.sqrt(2.0) / V_EW
    print(f"\nm_t = {M_T} MeV,  v = {V_EW} MeV")
    print(f"y_t = m_t√2/v = {y_t:.10f}   (natural coupling = 1.0)")
    print(f"|y_t - 1| = {abs(y_t - 1):.4e}")

    # Up-type quarks: k=(t=0, u=1, c=2)
    A_uct, d_uct = extract_A_delta(M_T, M_U, M_C)
    Q_uct = koide_Q(M_U, M_C, M_T)
    print(f"\nUp-type Koide (t,u,c) — k=(t=0, u=1, c=2):")
    print(f"  Q    = {Q_uct:.8f}   (2/3 = {2/3:.8f})")
    print(f"  δ_uct = {d_uct:.8f} rad  (2/9={2/9:.8f})")

    # Down-type quarks: k=(b=0, d=1, s=2)
    A_dsb, d_dsb = extract_A_delta(M_B, M_D, M_S)
    Q_dsb = koide_Q(M_D, M_S, M_B)
    print(f"\nDown-type Koide (b,d,s) — k=(b=0, d=1, s=2):")
    print(f"  Q    = {Q_dsb:.8f}   (2/3 = {2/3:.8f})")
    print(f"  δ_dsb = {d_dsb:.8f} rad  (2/9={2/9:.8f})")

    diffs = {
        'δ_L - δ_uct':   delta_lepton - d_uct,
        'δ_L - δ_dsb':   delta_lepton - d_dsb,
        'δ_uct - δ_dsb': d_uct - d_dsb,
    }
    print(f"\nPhase differences:")
    print(f"  δ_lepton = {delta_lepton:.8f} rad")
    for name, diff in diffs.items():
        print(f"  {name} = {diff:+.8f} rad  = {diff/np.pi:+.8f} π")

    print(f"\nRational approximations for |difference| (rad):")
    for name, diff in diffs.items():
        ad = abs(diff)
        p, q, err = best_rational(ad, max_denom=24)
        print(f"  |{name}| = {ad:.6f} rad  ≈  {p}/{q}  (err={err:.2e})")

    # y_t = 1 exact scenario
    m_t_nat = V_EW / np.sqrt(2.0)
    _, d_nat = extract_A_delta(m_t_nat, M_U, M_C)
    diff_nat = delta_lepton - d_nat
    print(f"\nIf y_t=1 exactly:  m_t = v/√2 = {m_t_nat:.2f} MeV = {m_t_nat/1000:.4f} GeV")
    print(f"  δ_uct(y_t=1) = {d_nat:.8f} rad")
    print(f"  δ_lepton - δ_uct(y_t=1) = {diff_nat:+.8f} rad  = {diff_nat/np.pi:+.8f} π")
    ad2 = abs(diff_nat)
    p2, q2, e2 = best_rational(ad2, max_denom=18)
    print(f"  Best rational (q≤18): |diff|≈{p2}/{q2}  (err={e2:.2e})")

    return d_uct, d_dsb


# ═══════════════════════════════════════════════════════════════
# SECTION 4 — WEINBERG ANGLE LINK
# ═══════════════════════════════════════════════════════════════

def section4(delta_exact):
    print("\n" + "=" * 70)
    print("SECTION 4: WEINBERG ANGLE LINK")
    print("=" * 70)

    sw2 = SIN2_THETA_W
    d   = delta_exact
    d9  = 2.0 / 9.0   # δ reference in rad

    print(f"\nsin²θ_W = {sw2:.5f}  (Casimir-derived)")
    print(f"δ_exact  = {d:.8f} rad  (≈ 2/9 = {2/9:.8f} rad)")

    cands = {
        'sin(3δ)':              np.sin(3*d),
        'cos(3δ)':              np.cos(3*d),
        'sin(δ)':               np.sin(d),
        'cos(δ)':               np.cos(d),
        'δ/(π)':                d/np.pi,
        'δ/(2π)':               d/(2*np.pi),
        '3δ':                   3*d,
        '9δ':                   9*d,
        '9δ/(2π)':              9*d/(2*np.pi),
        'sin²(δ)':              np.sin(d)**2,
        'cos²(δ)':              np.cos(d)**2,
        'sin²(3δ)':             np.sin(3*d)**2,
        'cos²(3δ)':             np.cos(3*d)**2,
        '(1+cos(3δ))/2':        (1+np.cos(3*d))/2,
        '1-sin²(3δ)':           1-np.sin(3*d)**2,
        '2/9':                  2/9,
        'δ':                    d,
        'δ²':                   d**2,
        'δ/sin²θ_W':            d/sw2,
        '9δ-2π':                9*d - 2*np.pi,
        '1/(1+9δ)':             1/(1+9*d),
        'sin(9δ)':              np.sin(9*d),
        'cos(9δ)':              np.cos(9*d),
    }

    print(f"\n{'Expression':<24}  {'Value':>12}  {'|Δ|':>12}  {'% err':>9}  Match?")
    print(f"  {'-'*24}  {'-'*12}  {'-'*12}  {'-'*9}  {'-'*7}")
    matches = []
    for name, val in cands.items():
        if not np.isfinite(val):
            continue
        diff = abs(val - sw2)
        rel  = diff / sw2 * 100.0
        flag = "YES <──" if rel < 1.0 else ""
        print(f"  {name:<24}  {val:>12.7f}  {diff:>12.4e}  {rel:>9.4f}%  {flag}")
        if rel < 1.0:
            matches.append((name, val, diff, rel))

    if matches:
        print(f"\n  MATCHES WITHIN 1%:")
        for name, val, diff, rel in matches:
            print(f"    {name} = {val:.10f}   err = {rel:.4f}%")
    else:
        sc = sorted([(n, v) for n, v in cands.items() if np.isfinite(v)],
                    key=lambda kv: abs(kv[1] - sw2))
        print(f"\n  No match within 1%. Closest:")
        for name, val in sc[:5]:
            print(f"    {name} = {val:.8f}   err = {abs(val-sw2)/sw2*100:.4f}%")


# ═══════════════════════════════════════════════════════════════
# SECTION 5 — BOOTSTRAP SIGNIFICANCE
# ═══════════════════════════════════════════════════════════════

def section5(delta_exact, A_ref):
    print("\n" + "=" * 70)
    print("SECTION 5: BOOTSTRAP SIGNIFICANCE")
    print("=" * 70)

    # Simple angles
    simple = {}
    for denom in [3, 4, 6, 9, 12, 18, 24, 36]:
        for num in range(0, 2 * denom + 1):
            a = 2.0 * np.pi * num / denom
            if 0.0 <= a <= 2.0 * np.pi:
                key = f"2π×{num}/{denom}"
                if not any(abs(a - v) < 1e-10 for v in simple.values()):
                    simple[key] = a
    # Also add simple fractions of 1 rad
    for denom in [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 15, 18]:
        for num in range(0, denom + 1):
            a = float(num) / denom
            if 0.0 < a < 2.0 * np.pi:
                key = f"{num}/{denom} rad"
                if not any(abs(a - v) < 1e-10 for v in simple.values()):
                    simple[key] = a

    avals = np.array(list(simple.values()))

    dists_sorted = sorted(
        ((k, v, abs(delta_exact - v)) for k, v in simple.items()),
        key=lambda x: x[2]
    )
    print(f"\nδ_exact = {delta_exact:.8f} rad")
    print(f"  2/9   = {2/9:.8f} rad  (reference)")
    print(f"  |δ - 2/9| = {abs(delta_exact - 2/9):.4e} rad  ({abs(delta_exact-2/9)/(2/9)*100:.4f}%)")
    print(f"\nDistance to nearby simple angles (top 12):")
    for k, v, dist in dists_sorted[:12]:
        print(f"  {k:<18} = {v:.8f}   |δ-a| = {dist:.4e}  ({dist/delta_exact*100:.4f}%)")

    # Monte Carlo
    print(f"\nMonte Carlo: 100 000 δ ∈ [0,2π) with m_τ > m_μ > m_e > 0 ...")
    N_mc  = 100_000
    rng   = np.random.default_rng(42)
    batch = rng.uniform(0.0, 2.0 * np.pi, 2_000_000)
    buf   = []
    for s in batch:
        m = reconstruct_masses(A_ref, s)
        if m[0] > m[2] > m[1] > 0.0:    # m_tau > m_mu > m_e
            buf.append(s)
        if len(buf) >= N_mc:
            break

    mc = np.array(buf)
    n  = len(mc)
    if n < N_mc:
        print(f"  [Warning: only {n} valid samples found]")
    else:
        print(f"  Collected {n} valid samples.")

    mc_min_dist = np.min(np.abs(mc[:, None] - avals[None, :]), axis=1)

    nearest_k, nearest_v, nearest_dist = dists_sorted[0]
    frac_closer = float(np.mean(mc_min_dist < nearest_dist))
    print(f"\n  Nearest simple angle to δ_exact: {nearest_k} = {nearest_v:.8f}  (dist={nearest_dist:.4e})")
    print(f"  Fraction of MC closer to any simple angle: {frac_closer:.4f}")
    print(f"  → δ_exact is at the {frac_closer*100:.1f}th percentile")
    print(f"    (0 = maximally special, 100 = typical random)")

    # Density near δ_exact
    win = 0.01   # ±0.01 rad — tight window because δ ≈ 0.22
    n_near = int(np.sum(np.abs(mc - delta_exact) < win))
    exp_uni = n * (2.0 * win) / (2.0 * np.pi)
    print(f"\n  Density near δ_exact (±{win} rad): {n_near} samples  (expected uniform: {exp_uni:.1f})")
    print(f"  Density ratio: {n_near/exp_uni:.4f}")

    # p-value: how special is |δ - 2/9| compared to random?
    d29 = abs(delta_exact - 2.0 / 9.0)
    mc_d29 = np.abs(mc - 2.0 / 9.0)
    frac_ref = float(np.mean(mc_d29 < d29))
    print(f"\n  |δ_exact - 2/9| = {d29:.4e} rad")
    print(f"  Fraction of MC samples as close to 2/9 rad: {frac_ref:.4f}")
    if frac_ref < 0.05:
        print(f"  → SIGNIFICANT: δ_exact is unusually close to 2/9 rad (p ≈ {frac_ref:.4f})")
    else:
        print(f"  → δ is close to 2/9 at level p={frac_ref:.4f} — marginal / not extreme")

    return mc, 2.0 / 9.0


# ═══════════════════════════════════════════════════════════════
# PLOTTING — 4-PANEL DARK FIGURE
# ═══════════════════════════════════════════════════════════════

def make_figure(delta_exact, dscan, ms_scan, valid, d_uct, d_dsb,
                mc_samples, delta_ref, A_ref):
    print("\n" + "=" * 70)
    print("GENERATING 4-PANEL FIGURE")
    print("=" * 70)

    fig = plt.figure(figsize=(18, 14), facecolor=BG)
    fig.patch.set_facecolor(BG)
    gs  = gridspec.GridSpec(2, 2, figure=fig,
                            hspace=0.44, wspace=0.36,
                            left=0.07, right=0.96,
                            top=0.93, bottom=0.07)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    all_axes = [ax1, ax2, ax3, ax4]

    for ax in all_axes:
        ax.set_facecolor(BG)
        for sp in ax.spines.values():
            sp.set_color('#334455')
        ax.tick_params(colors='#aabbcc', which='both')
        ax.xaxis.label.set_color('#aabbcc')
        ax.yaxis.label.set_color('#aabbcc')
        ax.title.set_color('#eef4ff')

    x = dscan         # x-axis in rad (not scaled by 2π, since δ ≈ 0.22 is in a small range)
    m_tau = ms_scan[:, 0]
    m_e   = ms_scan[:, 1]
    m_mu  = ms_scan[:, 2]

    # ── Panel 1: three mass curves vs δ (full range) ──────────
    ax1.plot(x, m_tau, color=C_K0, lw=1.8, label='m_τ  (k=0)')
    ax1.plot(x, m_e,   color=C_K1, lw=1.8, label='m_e  (k=1)')
    ax1.plot(x, m_mu,  color=C_K2, lw=1.8, label='m_μ  (k=2)')

    ax1.axvline(delta_exact, color=C_MARK, lw=2.0, ls='--', alpha=0.9,
                label=f'δ_exact = {delta_exact:.4f} rad')
    ax1.axvline(delta_ref,   color=C_REF,  lw=1.4, ls=':',  alpha=0.85,
                label=f'2/9 = {2/9:.4f} rad')

    # Shade valid ordering region
    for i in range(len(dscan) - 1):
        if valid[i]:
            ax1.axvspan(x[i], x[i+1], alpha=0.08, color=C_SHADE, lw=0)

    ax1.set_yscale('log')
    ax1.set_xlabel('δ (rad)', fontsize=11)
    ax1.set_ylabel('Mass (MeV)', fontsize=11)
    ax1.set_title('Panel 1: Mass Hierarchy vs δ\n(blue shading = valid ordering m_τ>m_μ>m_e)',
                  fontsize=11, fontweight='bold')
    ax1.legend(fontsize=8, loc='upper right',
               facecolor='#111122', edgecolor='#334455', labelcolor='#ccddee')
    ax1.set_xlim(0, 2*np.pi)
    ax1.grid(alpha=0.15, color='#334455')

    # ── Panel 2: Koide Q vs δ — sanity check ─────────────────
    Qv = np.array([koide_Q(*ms_scan[i]) for i in range(len(dscan))])
    ax2.plot(x, Qv, color=C_K1, lw=1.5, label='Q(δ)')
    ax2.axhline(2/3, color=C_K0, lw=2.2, ls='--', label='2/3 (exact)')
    ax2.axvline(delta_exact, color=C_MARK, lw=2.0, ls='--', alpha=0.9,
                label='δ_exact')
    ax2.axvline(delta_ref, color=C_REF, lw=1.4, ls=':', alpha=0.8,
                label='2/9 rad')

    fin = Qv[np.isfinite(Qv) & (Qv > 0) & (Qv < 5)]
    if len(fin):
        lo = max(0.0, float(np.percentile(fin, 2)) * 0.95)
        hi = min(3.0, float(np.percentile(fin, 98)) * 1.05)
        ax2.set_ylim(lo, hi)

    Q_pdg = koide_Q(M_TAU, M_E, M_MU)
    ax2.text(0.04, 0.12, f'Q(PDG) = {Q_pdg:.14f}',
             transform=ax2.transAxes, color=C_K0, fontsize=8.5,
             bbox=dict(facecolor='#0d0d2b', edgecolor='#334455', alpha=0.85, boxstyle='round'))
    ax2.set_xlabel('δ (rad)', fontsize=11)
    ax2.set_ylabel('Koide Q', fontsize=11)
    ax2.set_title('Panel 2: Koide Q vs δ\n(Q = 2/3 everywhere — not a hint for δ selection)',
                  fontsize=11, fontweight='bold')
    ax2.legend(fontsize=8.5, facecolor='#111122', edgecolor='#334455', labelcolor='#ccddee')
    ax2.set_xlim(0, 2*np.pi)
    ax2.grid(alpha=0.15, color='#334455')

    # ── Panel 3: Continued fraction text panel ────────────────
    ax3.axis('off')
    terms, convs = continued_fraction(delta_exact, max_terms=14, max_denom=500)
    rows = []
    rows.append(f"δ_exact = {delta_exact:.12f} rad")
    rows.append(f"2/9     = {2/9:.12f} rad  (reference)")
    rows.append(f"|δ - 2/9| = {abs(delta_exact - 2/9):.4e} rad")
    rows.append(f"  = {abs(delta_exact-2/9)/(2/9)*100:.6f}% of 2/9")
    rows.append("")
    rows.append(f"CF expansion of δ: [{'; '.join(str(t) for t in terms[:10])}; ...]")
    rows.append("")
    rows.append(f"{'n':<4} {'p/q':<10} {'value':>16} {'error':>14} {'% err':>10}")
    rows.append("─" * 58)
    for i, (p, q) in enumerate(convs[:12]):
        if q <= 0:
            continue
        val = p / q
        err = abs(delta_exact - val)
        rel = err / delta_exact * 100.0
        tag = "  ← 2/9" if (p == 2 and q == 9) else ""
        rows.append(f"{i:<4} {p}/{q:<8} {val:>16.10f} {err:>14.4e} {rel:>10.4f}%{tag}")
    rows.append("")
    rows.append("Best rational p/q approximations for δ (rad):")
    for md in [9, 12, 18, 24, 36]:
        p, q, err = best_rational(delta_exact, max_denom=md)
        rel = err / delta_exact * 100.0
        tag = "  ← 2/9" if (p == 2 and q == 9) else ""
        rows.append(f"  q≤{md:2d}: {p}/{q:<5d} = {p/q:.10f}   err={err:.2e}  ({rel:.4f}%){tag}")

    ax3.text(0.02, 0.97, '\n'.join(rows),
             transform=ax3.transAxes, va='top', ha='left',
             fontfamily='monospace', fontsize=8.5, color='#ccddee',
             bbox=dict(facecolor='#080818', edgecolor='#334455', alpha=0.9, boxstyle='round'))
    ax3.set_title('Panel 3: Continued Fraction for δ_exact',
                  fontsize=11, fontweight='bold')

    # ── Panel 4: Quark vs Lepton phase comparison ─────────────
    ax4.axis('off')
    Q_L = koide_Q(M_TAU, M_E, M_MU)
    Q_U = koide_Q(M_U, M_C, M_T)
    Q_D = koide_Q(M_D, M_S, M_B)

    dL = delta_exact
    dU = d_uct
    dD = d_dsb
    d_LU = dL - dU
    d_LD = dL - dD
    d_UD = dU - dD

    r4 = []
    r4.append("LEPTON vs QUARK KOIDE PHASES")
    r4.append("k=(heavy=0, light=1, mid=2) convention")
    r4.append("─" * 48)
    r4.append("")
    r4.append(f"Leptons (τ,e,μ):    Q = {Q_L:.8f}  (2/3={2/3:.8f})")
    r4.append(f"  δ_L = {dL:.8f} rad")
    r4.append(f"  2/9 = {2/9:.8f} rad")
    r4.append(f"  δ_L - 2/9 = {dL-2/9:+.6e} rad  ({(dL-2/9)/(2/9)*100:+.4f}%)")
    r4.append("")
    r4.append(f"Up quarks (t,u,c):  Q = {Q_U:.8f}")
    r4.append(f"  δ_U = {dU:.8f} rad")
    r4.append(f"  δ_U - 2/9 = {dU-2/9:+.6e} rad")
    r4.append("")
    r4.append(f"Down quarks (b,d,s):  Q = {Q_D:.8f}")
    r4.append(f"  δ_D = {dD:.8f} rad")
    r4.append(f"  δ_D - 2/9 = {dD-2/9:+.6e} rad")
    r4.append("")
    r4.append("Phase differences:")
    r4.append(f"  δ_L-δ_U = {d_LU:+.6f} rad  = {d_LU/np.pi:+.6f}π")
    r4.append(f"  δ_L-δ_D = {d_LD:+.6f} rad  = {d_LD/np.pi:+.6f}π")
    r4.append(f"  δ_U-δ_D = {d_UD:+.6f} rad  = {d_UD/np.pi:+.6f}π")
    r4.append("")
    r4.append("Rational approx for |difference| (rad):")
    for lbl, diff in [("δ_L-δ_U", d_LU), ("δ_L-δ_D", d_LD), ("δ_U-δ_D", d_UD)]:
        ad = abs(diff)
        p, q, err = best_rational(ad, max_denom=18)
        r4.append(f"  |{lbl}| = {ad:.5f}  ≈  {p}/{q}  (err={err:.2e})")
    r4.append("")
    r4.append(f"Top Yukawa:  y_t = {M_T*np.sqrt(2)/V_EW:.6f}  (natural=1)")
    r4.append(f"sin²θ_W = {SIN2_THETA_W:.5f}")
    r4.append(f"Note: sin²θ_W / δ_L = {SIN2_THETA_W/dL:.6f}")

    ax4.text(0.02, 0.97, '\n'.join(r4),
             transform=ax4.transAxes, va='top', ha='left',
             fontfamily='monospace', fontsize=8.5, color='#ccddee',
             bbox=dict(facecolor='#080818', edgecolor='#334455', alpha=0.9, boxstyle='round'))
    ax4.set_title('Panel 4: Quark vs Lepton Koide Phase Comparison',
                  fontsize=11, fontweight='bold')

    fig.suptitle('Koide Phase Scan — What Selects δ₀ ≈ 2/9 rad?',
                 fontsize=15, fontweight='bold', color='#eef4ff', y=0.97)

    outpath = '/mnt/d/Fundamentals/sandbox/koide_phase_scan.png'
    plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f"Figure saved: {outpath}")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n" + "█" * 70)
    print("  KOIDE PHASE SCAN")
    print("  Parametrization: √m_k = A(1+√2 cos(δ+2πk/3)), k=0→τ, k=1→e, k=2→μ")
    print("  Q=2/3 by construction. Searching for constraint that fixes δ≈2/9 rad.")
    print("█" * 70)

    A_ref, delta_exact = section1()
    dscan, ms_scan, valid = section2(A_ref, delta_exact)
    d_uct, d_dsb = section3(delta_exact)
    section4(delta_exact)
    mc, delta_ref = section5(delta_exact, A_ref)
    make_figure(delta_exact, dscan, ms_scan, valid,
                d_uct, d_dsb, mc, delta_ref, A_ref)

    print("\n" + "█" * 70)
    print("  DONE")
    print("█" * 70)
    print(f"\n  δ_exact   = {delta_exact:.12f} rad")
    print(f"  2/9 rad   = {2/9:.12f} rad  (reference)")
    print(f"  |δ - 2/9| = {abs(delta_exact - 2/9):.4e}  ({abs(delta_exact-2/9)/(2/9)*100:.6f}%)")
    print(f"\n  Output: /mnt/d/Fundamentals/sandbox/koide_phase_scan.png")


if __name__ == '__main__':
    main()
