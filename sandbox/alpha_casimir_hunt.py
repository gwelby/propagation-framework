"""
alpha_casimir_hunt.py — Comprehensive hunt for the fine structure constant
from the Propagation Framework's Casimir polynomial machinery.

Framework anchors:
  φ = 1.618033988749895   (golden ratio)
  N = 3                   (generations)
  D = 3                   (spatial dimensions)
  b₀ = 16/3               (one-loop beta coefficient)
  N^{D/2} = 3^{3/2} = 5.196...
  sin²θ_W = 0.22310       DERIVED from x²+C₂x-C₂=0  ← the anchor

PDG target:
  α    = 1 / 137.035999084
  α⁻¹  = 137.035999084
  α(M_Z)⁻¹ = 128.9          (running value at Z mass)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import numpy as np
import itertools
from math import gamma, sqrt, pi, log, exp

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = '#0a0a1a'
FG      = '#e0e0f0'
ACCENT  = '#00ffe0'
GOLD    = '#ffd700'
RED     = '#ff4466'
GREEN   = '#44ff88'
BLUE    = '#4488ff'
PURPLE  = '#cc66ff'
ORANGE  = '#ff8844'

# ── Fundamental constants ─────────────────────────────────────────────────────
PHI     = 1.618033988749895
N_GEN   = 3
D_SPACE = 3
B0      = 16.0 / 3.0                     # 5.3333...
N_D2    = N_GEN ** (D_SPACE / 2.0)       # 3^{3/2} = 5.19615...
ALPHA_PDG     = 1.0 / 137.035999084      # PDG 2022
ALPHA_INV_PDG = 137.035999084
ALPHA_MZ_INV  = 128.9                    # α⁻¹ at M_Z (running)
ALPHA_MZ      = 1.0 / ALPHA_MZ_INV
SIN2_TW_PDG   = 0.23122                  # PDG on-shell
SIN2_TW_FW    = 0.22310                  # Framework derived value


def pct_error(val, target):
    """Percentage error relative to target."""
    return abs(val - target) / abs(target) * 100.0


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — CASIMIR ROOT ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════

def casimir_root(j):
    """Positive root of x² + C₂·x - C₂ = 0, where C₂ = j(j+1)."""
    C2 = j * (j + 1.0)
    if C2 == 0.0:
        return 0.0
    return (-C2 + sqrt(C2 * C2 + 4.0 * C2)) / 2.0


def section1_casimir_roots():
    print("\n" + "=" * 68)
    print("  SECTION 1 — CASIMIR ROOT ANALYSIS")
    print("=" * 68)

    spins = [0.0, 0.5, 1.0, 1.5, 2.0]
    roots = {}
    for j in spins:
        roots[j] = casimir_root(j)

    print(f"\n{'j':>5}  {'C₂=j(j+1)':>12}  {'x₊(j)':>12}  {'(1-x₊)':>12}  {'x₊²':>12}  {'x₊³':>12}")
    print("-" * 72)
    for j in spins:
        C2 = j * (j + 1.0)
        x  = roots[j]
        print(f"{j:>5.1f}  {C2:>12.6f}  {x:>12.8f}  {1-x:>12.8f}  {x**2:>12.8f}  {x**3:>12.8f}")

    # Weinberg sanity check
    x_half = roots[0.5]
    x_one  = roots[1.0]
    # Framework derivation: sin²θ_W = 1 - x_{1/2}/x_1
    sin2_fw = 1.0 - (x_half / x_one)
    err_fw  = pct_error(sin2_fw, SIN2_TW_FW)
    err_pdg = pct_error(sin2_fw, SIN2_TW_PDG)

    print(f"\n  WEINBERG SANITY CHECK")
    print(f"  sin²θ_W = 1 - x(1/2)/x(1) = 1 - {x_half:.8f}/{x_one:.8f}")
    print(f"           = {sin2_fw:.8f}")
    print(f"  vs Framework target {SIN2_TW_FW}  → error {err_fw:.4f}%  ✓" if err_fw < 0.01 else
          f"  vs Framework target {SIN2_TW_FW}  → error {err_fw:.4f}%")
    print(f"  vs PDG on-shell     {SIN2_TW_PDG} → error {err_pdg:.4f}%")

    return roots


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — ALGEBRAIC COMBINATION SCAN
# ═════════════════════════════════════════════════════════════════════════════

def section2_algebraic_scan(roots):
    print("\n" + "=" * 68)
    print("  SECTION 2 — ALGEBRAIC COMBINATION SCAN")
    print("=" * 68)

    THRESHOLD = 5.0   # percent

    # Build variable pool
    pool = {}
    for j, x in roots.items():
        if x <= 0:
            continue
        label = f"x({j})"
        pool[label]         = x
        pool[f"(1-x({j}))"] = 1.0 - x if (1.0 - x) > 0 else None
        pool[f"x({j})²"]    = x ** 2
        pool[f"x({j})³"]    = x ** 3

    # Add framework constants
    pool["φ"]            = PHI
    pool["π"]            = pi
    pool["√2"]           = sqrt(2.0)
    pool["N=3"]          = float(N_GEN)
    pool["D=3"]          = float(D_SPACE)
    pool["b₀"]           = B0
    pool["N^{D/2}"]      = N_D2
    pool["φ²"]           = PHI ** 2
    pool["φ³"]           = PHI ** 3
    pool["1/π"]          = 1.0 / pi
    pool["1/π²"]         = 1.0 / (pi ** 2)
    pool["sin²θ_W(fw)"]  = SIN2_TW_FW

    # Remove None entries
    pool = {k: v for k, v in pool.items() if v is not None and np.isfinite(v) and v > 0}

    names  = list(pool.keys())
    values = list(pool.values())
    n      = len(names)

    hits = []   # (error_pct, label, computed_alpha, computed_alpha_inv)

    def record(label, val):
        """Record if val looks like α or 1/α is within threshold of α_inv."""
        if val <= 0 or not np.isfinite(val):
            return
        # Direct alpha
        err = pct_error(val, ALPHA_PDG)
        if err < THRESHOLD:
            hits.append((err, label, val, 1.0/val))
        # Inverse
        inv = 1.0 / val
        err2 = pct_error(inv, ALPHA_PDG)
        if err2 < THRESHOLD and label != "1/val":
            hits.append((err2, f"1/({label})", inv, val))

    print(f"\n  Pool size: {n} variables. Scanning pairs, triples, quads...")
    print(f"  Threshold: {THRESHOLD}% of α = {ALPHA_PDG:.6e}\n")

    # ── single values ──
    for i in range(n):
        record(names[i], values[i])

    # ── pairs: multiply ──
    for i, j in itertools.combinations(range(n), 2):
        record(f"{names[i]}·{names[j]}", values[i] * values[j])

    # ── pairs: divide ──
    for i in range(n):
        for j in range(n):
            if i != j and values[j] > 0:
                record(f"{names[i]}/{names[j]}", values[i] / values[j])

    # ── triples: multiply ──
    for i, j, k in itertools.combinations(range(n), 3):
        record(f"{names[i]}·{names[j]}·{names[k]}",
               values[i] * values[j] * values[k])

    # ── triples: A*B/C ──
    for i, j, k in itertools.permutations(range(n), 3):
        if values[k] > 0:
            record(f"{names[i]}·{names[j]}/{names[k]}",
                   values[i] * values[j] / values[k])

    # ── quads: multiply (limited combos to keep speed reasonable) ──
    for i, j, k, l in itertools.combinations(range(n), 4):
        record(f"{names[i]}·{names[j]}·{names[k]}·{names[l]}",
               values[i] * values[j] * values[k] * values[l])

    # ── quads: A*B*C/D ──
    quad_pool = list(range(min(n, 12)))   # keep tractable
    for i, j, k in itertools.combinations(quad_pool, 3):
        for l in quad_pool:
            if l not in (i, j, k) and values[l] > 0:
                record(f"{names[i]}·{names[j]}·{names[k]}/{names[l]}",
                       values[i] * values[j] * values[k] / values[l])

    # Deduplicate by label
    seen = set()
    unique_hits = []
    for h in hits:
        if h[1] not in seen:
            seen.add(h[1])
            unique_hits.append(h)

    unique_hits.sort(key=lambda h: h[0])

    print(f"  {'Expression':<45} {'α value':>14} {'1/α':>10} {'Error%':>8}")
    print("  " + "-" * 82)
    for err, label, val, inv_val in unique_hits[:20]:
        marker = "  <<<< <1%" if err < 1.0 else ("  << <3%" if err < 3.0 else "")
        print(f"  {label:<45} {val:>14.8f} {inv_val:>10.4f} {err:>7.3f}%{marker}")

    if unique_hits:
        best = unique_hits[0]
        if best[0] < 1.0:
            print(f"\n  [!!] SUB-1% HIT: {best[1]}")
            print(f"       α = {best[2]:.10f}  (PDG: {ALPHA_PDG:.10f})")
            print(f"       error = {best[0]:.4f}%")
        else:
            print(f"\n  Best algebraic hit: {best[1]}")
            print(f"  α = {best[2]:.8f}  error = {best[0]:.3f}%")

    return unique_hits


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — VOLUME / WYLER APPROACH
# ═════════════════════════════════════════════════════════════════════════════

def vol_sphere(n):
    """Volume of unit n-sphere S^n (surface of (n+1)-ball)."""
    return 2.0 * pi**((n + 1) / 2.0) / gamma((n + 1) / 2.0)


def section3_volume_wyler():
    print("\n" + "=" * 68)
    print("  SECTION 3 — VOLUME / WYLER APPROACH")
    print("=" * 68)

    # Standard sphere volumes
    vols = {1: 2.0 * pi,
            2: 4.0 * pi,
            3: 2.0 * pi ** 2,
            4: (8.0 / 3.0) * pi ** 2}

    print("\n  Sphere volumes (cross-check):")
    for n, v in vols.items():
        print(f"  vol(S^{n}) = {v:.8f}  (formula: {vol_sphere(n):.8f})")

    wyler_hits = []

    def check_wyler(label, val):
        if val <= 0 or not np.isfinite(val):
            return
        err = pct_error(val, ALPHA_PDG)
        print(f"  {label:<55} = {val:.10f}  (1/α={1/val:.4f})  err={err:.4f}%"
              + ("  <<<<" if err < 1.0 else ("  <<" if err < 3.0 else "")))
        wyler_hits.append((err, label, val))

    print(f"\n  Target α = {ALPHA_PDG:.10f}  (1/α = {ALPHA_INV_PDG:.6f})")
    print()

    # ── Wyler's original formula ──
    # α_Wyler = 9 / (8π⁴) × [π/Γ(5)]^(1/4)
    # Γ(5) = 4! = 24
    wyler_classic = (9.0 / (8.0 * pi**4)) * (pi / gamma(5)) ** (1.0/4.0)
    check_wyler("Wyler:  9/(8π⁴)·(π/Γ(5))^{1/4}", wyler_classic)

    # ── Variations on Wyler ──
    # Using vol(S^n) explicitly
    w2 = vol_sphere(2) / (8.0 * pi**3) * (vol_sphere(1) / vol_sphere(4)) ** (1.0/4.0)
    check_wyler("Wyler-v2: vol(S²)/(8π³)·(vol(S¹)/vol(S⁴))^{1/4}", w2)

    # ── N^{D/2} combinations with Wyler ──
    # 1/α ~ N^{D/2} × (something from volumes)?
    w3 = wyler_classic * N_D2
    check_wyler(f"Wyler × N^{{D/2}} ({N_D2:.4f})", w3)

    w4 = wyler_classic / N_D2
    check_wyler(f"Wyler / N^{{D/2}}", w4)

    # ── φ³ = 4.236 combinations ──
    phi3 = PHI ** 3
    w5 = wyler_classic * phi3
    check_wyler(f"Wyler × φ³ ({phi3:.4f})", w5)

    w6 = wyler_classic / phi3
    check_wyler(f"Wyler / φ³", w6)

    # ── 1/(4π) natural unification coupling ──
    alpha_gut = 1.0 / (4.0 * pi)
    check_wyler("α_GUT = 1/(4π)", alpha_gut)

    # ── Koide-inspired: α = sin²θ_W / π ──
    okun = SIN2_TW_FW / pi
    check_wyler("Okun-approx: sin²θ_W(fw)/π", okun)

    okun2 = SIN2_TW_PDG / pi
    check_wyler("Okun-approx: sin²θ_W(PDG)/π", okun2)

    # ── vol(S³)/vol(S⁴) × 1/N² ──
    combo1 = vols[3] / vols[4] / (N_GEN ** 2)
    check_wyler("vol(S³)/vol(S⁴)/N²", combo1)

    # ── vol(S²)/(4π² × N_D2 × φ³) ──
    combo2 = vols[2] / (4.0 * pi**2 * N_D2 * phi3)
    check_wyler("vol(S²)/(4π²·N^{D/2}·φ³)", combo2)

    # ── Pure geometric: 1/(4π) × (vol(S²)/vol(S⁴))^(1/3) ──
    combo3 = (1.0/(4.0*pi)) * (vols[2] / vols[4]) ** (1.0/3.0)
    check_wyler("(1/4π)·(vol(S²)/vol(S⁴))^{1/3}", combo3)

    # ── Charge-sum-squared Wyler variant ──
    # sum Q² for SM quarks+leptons (one generation): 3×(4/9+1/9+1/9) + 1 = 2+1=3
    sum_Q2 = 3.0 * (4.0/9.0 + 1.0/9.0 + 1.0/9.0) + 1.0  # = 3
    w7 = wyler_classic * sum_Q2
    check_wyler(f"Wyler × ΣQ² ({sum_Q2:.3f})", w7)

    # ── Explicit Wyler domain volume formula ──
    # Wyler's D₄ domain:  vol = π^10 / (3·2^15·5!)
    vol_D4 = pi**10 / (3.0 * 2**15 * 120.0)
    # α = (9/8) × (vol_D4 / vol_S4)^(1/5)
    w8 = (9.0/8.0) * (vol_D4 / vols[4]) ** (1.0/5.0)
    check_wyler("Wyler D₄: (9/8)·(vol_D4/vol_S4)^{1/5}", w8)

    wyler_hits.sort(key=lambda h: h[0])
    print(f"\n  Best volume approach: {wyler_hits[0][1]}")
    print(f"  α = {wyler_hits[0][2]:.10f}  error = {wyler_hits[0][0]:.4f}%")

    return wyler_hits


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — RG RUNNING HYPOTHESIS
# ═════════════════════════════════════════════════════════════════════════════

def section4_rg_running():
    print("\n" + "=" * 68)
    print("  SECTION 4 — RG RUNNING HYPOTHESIS")
    print("=" * 68)

    # ── Framework GUT scale from God Equation exponent ──
    # ln(M_GUT/M_Z) = 4π²·N^{D/2} / b₀
    log_ratio = 4.0 * pi**2 * N_D2 / B0
    M_Z     = 91.1876   # GeV
    M_GUT   = M_Z * exp(log_ratio)

    print(f"\n  Framework constants:")
    print(f"  b₀ = 16/3 = {B0:.6f}")
    print(f"  N^{{D/2}} = 3^{{3/2}} = {N_D2:.6f}")
    print(f"  God Eq exponent: ln(M_GUT/M_Z) = 4π²·N^{{D/2}}/b₀ = {log_ratio:.6f}")
    print(f"  → M_GUT = {M_Z:.4f} × exp({log_ratio:.3f}) = {M_GUT:.4e} GeV")

    # ── Natural unification coupling ──
    alpha_gut_nat = 1.0 / (4.0 * pi)
    print(f"\n  Natural GUT coupling: α_GUT = 1/(4π) = {alpha_gut_nat:.8f}")
    print(f"  → 1/α_GUT = 4π = {4.0*pi:.6f}")

    # ── EM beta coefficient from SM ──
    # b_em = (4/3) × ΣQ² × N_f  (one-loop, N_f active flavors)
    # At full SM: ΣQ² per generation = 3×(4/9+1/9+1/9) + 1 = 2+1 = 3
    # For N_gen generations: b_em = (4/3) × 3 × N_gen = 4 × N_gen
    b_em = (4.0 / 3.0) * 3.0 * N_GEN   # = 4 × 3 = 12  (but conventional is different)
    # More standard: b_em(SM, above top) = 4/3 × (3×(4/9+1/9+1/9) + 1 + ...) × N_gen
    # Simpler standard form: b_em = 41/6 ≈ 6.833 for the SM hypercharge
    b_em_std = 41.0 / 6.0

    print(f"\n  EM running: 1/α(μ) = 1/α_GUT + (b_em/2π)·ln(μ/M_GUT)  [runs up from GUT]")
    print(f"  Or:         1/α(μ) = 1/α_GUT - (b_em/2π)·ln(M_GUT/μ)")
    print(f"  NOTE: α_GUT=1/(4π) ≈ 0.0796 is far too large for a GUT coupling;")
    print(f"  standard SU(5) gives α_GUT ≈ 1/25=0.04.  Both are tested below.")

    m_e   = 0.511e-3   # GeV
    b_qed = 2.0 / 3.0  # |b_QED| one-loop, one charged lepton

    rg_hits = []

    def run_alpha(alpha_gut, b_em_val, log_mg_mz, label):
        """Run coupling from GUT to M_Z, then continue to low energy."""
        inv_alpha_mz = (1.0/alpha_gut) - (b_em_val / (2.0*pi)) * log_mg_mz
        alpha_mz     = 1.0 / inv_alpha_mz if inv_alpha_mz > 0 else float('inf')

        # Continue M_Z → m_e with QED one-loop (b_qed = 2/3 per charged lepton)
        log_mz_me   = log(M_Z / m_e)
        delta_low   = (b_qed / (2.0*pi)) * log_mz_me   # ≈ 2.3

        inv_alpha_0 = inv_alpha_mz + delta_low if inv_alpha_mz > 0 else float('inf')
        alpha_0     = 1.0 / inv_alpha_0 if inv_alpha_0 > 0 else float('inf')

        err_mz  = pct_error(1.0/inv_alpha_mz, ALPHA_MZ)  if inv_alpha_mz > 0 and np.isfinite(1.0/inv_alpha_mz)  else 999.0
        err_low = pct_error(alpha_0, ALPHA_PDG)            if inv_alpha_0 > 0 and np.isfinite(alpha_0)            else 999.0

        print(f"\n  [{label}]")
        print(f"    1/α_GUT = {1.0/alpha_gut:.4f},  b_em = {b_em_val:.4f},  ln(M_GUT/M_Z) = {log_mg_mz:.4f}")
        print(f"    → 1/α(M_Z) = {inv_alpha_mz:.4f}   (PDG: {ALPHA_MZ_INV:.3f})   err={err_mz:.3f}%")
        print(f"    → 1/α(0)  ≈ {inv_alpha_0:.4f}  (PDG: {ALPHA_INV_PDG:.3f})   err={err_low:.3f}%")

        rg_hits.append({
            'label': label,
            'alpha_gut': alpha_gut,
            'b_em': b_em_val,
            'log_ratio': log_mg_mz,
            'inv_alpha_mz': inv_alpha_mz,
            'inv_alpha_0': inv_alpha_0,
            'err_mz': err_mz,
            'err_low': err_low,
        })
        return inv_alpha_mz, inv_alpha_0

    # ── Standard GUT coupling ──
    alpha_gut_su5 = 1.0 / 25.0   # SU(5) unification value
    # Also compute what log ratio gives α→1/137 if we trust α_GUT=1/25
    # 1/α₀ = 1/α_GUT - (b_em/2π)·log_ratio + δ_low
    # → log_ratio = (1/α_GUT - 1/α₀ + δ_low) × (2π/b_em)
    delta_low_ref = (b_qed / (2.0*pi)) * log(M_Z / m_e)
    log_needed_std = (1.0/alpha_gut_su5 - ALPHA_INV_PDG + delta_low_ref) * (2.0*pi / b_em_std)
    print(f"\n  [Info] SU(5) α_GUT=1/25: log needed to reach α₀=1/137 = {log_needed_std:.4f}")
    print(f"         FW log = {log_ratio:.4f}  (ratio = {log_needed_std/log_ratio:.4f})")

    # Run several scenarios
    run_alpha(alpha_gut_nat,  b_em_std, log_ratio,         "α_GUT=1/4π,  b_em=41/6 (SM hyper), FW log")
    run_alpha(alpha_gut_nat,  b_em,     log_ratio,         "α_GUT=1/4π,  b_em=4N_gen=12, FW log")
    run_alpha(alpha_gut_nat,  B0,       log_ratio,         "α_GUT=1/4π,  b_em=b₀=16/3, FW log")
    run_alpha(alpha_gut_su5,  b_em_std, log_ratio,         "α_GUT=1/25,  b_em=41/6 (SM hyper), FW log")
    run_alpha(alpha_gut_su5,  B0,       log_ratio,         "α_GUT=1/25,  b_em=b₀=16/3, FW log")
    run_alpha(alpha_gut_su5,  b_em_std, log_needed_std,    "α_GUT=1/25,  b_em=41/6, log→1/137 (back-calc)")
    run_alpha(1.0/(2.0*pi*PHI), b_em_std, log_ratio,       "α_GUT=1/(2πφ),b_em=41/6, FW log")

    # ── RG curve data for plotting ──
    # Use a physically reasonable GUT coupling α_GUT ≈ 1/25 at M_GUT
    # (standard SU(5)/SO(10) unification value)
    m_e          = 0.511e-3  # GeV (also needed for low-energy running below)
    alpha_gut_plot = 1.0 / 25.0
    mu_range     = np.logspace(log(m_e)/log(10), log(M_GUT)/log(10), 500)
    alpha_run_fw = []

    for mu in mu_range:
        if mu < M_Z:
            # Run from GUT to M_Z with SM b_em, then M_Z to mu with QED b_qed
            inv_mz  = (1.0/alpha_gut_plot) - (b_em_std/(2.0*pi)) * log(M_GUT/M_Z)
            inv_mu  = inv_mz + (b_qed/(2.0*pi)) * log(M_Z/max(mu, m_e))
            alpha_run_fw.append(1.0/inv_mu if inv_mu > 0 else 0)
        else:
            inv = (1.0/alpha_gut_plot) - (b_em_std/(2.0*pi)) * log(M_GUT/mu)
            alpha_run_fw.append(1.0/inv if inv > 0 else 0)

    # Sort hits
    rg_hits.sort(key=lambda h: h['err_low'])
    best = rg_hits[0]
    print(f"\n  Best RG scenario: {best['label']}")
    print(f"  Low-energy α error: {best['err_low']:.3f}%")

    return rg_hits, mu_range, alpha_run_fw, M_GUT


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5 — CROSS-CHECK WITH KNOWN IDENTITIES
# ═════════════════════════════════════════════════════════════════════════════

def section5_known_identities():
    print("\n" + "=" * 68)
    print("  SECTION 5 — CROSS-CHECK WITH KNOWN IDENTITIES")
    print("=" * 68)

    identity_hits = []

    def check(label, val, note=""):
        if val <= 0 or not np.isfinite(val):
            print(f"  {label:<55} = INVALID")
            return
        err = pct_error(val, ALPHA_PDG)
        star = ""
        if err < 1.0:
            star = "  <<<< <1% !!"
        elif err < 3.0:
            star = "  << <3%"
        elif err < 5.0:
            star = "  < <5%"
        print(f"  {label:<55} α={val:.8f}  1/α={1/val:.4f}  err={err:.4f}%{star}")
        if note:
            print(f"    ({note})")
        identity_hits.append((err, label, val))

    print()

    # ── Koide phase ──
    # Standard: δ₀ ≈ 2/9 rad, but from Koide formula δ = π/12 for charged leptons
    delta_koide = 2.0/9.0         # "2/9 phase"
    delta_pi12  = pi/12.0         # Koide exact

    alpha_koide1 = (2.0/9.0) * SIN2_TW_FW * np.sin(3.0 * delta_koide)
    check("(2/9)·sin²θ_W(fw)·sin(3δ₀), δ₀=2/9",  alpha_koide1, "Koide-inspired")

    alpha_koide2 = (2.0/9.0) * SIN2_TW_PDG * np.sin(3.0 * delta_koide)
    check("(2/9)·sin²θ_W(PDG)·sin(3δ₀), δ₀=2/9", alpha_koide2, "Koide-inspired PDG")

    alpha_koide3 = (2.0/9.0) * SIN2_TW_FW * np.sin(3.0 * delta_pi12)
    check("(2/9)·sin²θ_W(fw)·sin(3δ₀), δ₀=π/12", alpha_koide3, "Koide exact phase")

    # ── Okun formula: α ≈ sin²θ_W / π ──
    alpha_okun_fw  = SIN2_TW_FW  / pi
    alpha_okun_pdg = SIN2_TW_PDG / pi
    check("Okun: sin²θ_W(fw)/π",  alpha_okun_fw,  "Okun approximate")
    check("Okun: sin²θ_W(PDG)/π", alpha_okun_pdg, "Okun approximate PDG")

    # ── Alternative Okun-like ──
    check("sin²θ_W(fw)/(4π)",     SIN2_TW_FW  / (4.0*pi))
    check("sin²θ_W(PDG)/(4π)",    SIN2_TW_PDG / (4.0*pi))

    # ── Rosen-Cabibbo type ──
    # α = (g²/4π) at unification, g² = sin²θ_W × (4π/α) → circular. Instead:
    # Try α = sin⁴θ_W / (something)
    check("sin⁴θ_W(fw)/(2π)",     SIN2_TW_FW**2 / (2.0*pi))
    check("sin²θ_W(fw)·sin²θ_W(fw)/π", SIN2_TW_FW * SIN2_TW_FW / pi)

    # ── Freeman Dyson / MIT bag ──
    # α ≈ 1/(6π) × cos²θ_W style
    cos2_fw  = 1.0 - SIN2_TW_FW
    check("sin²θ_W(fw)·cos²θ_W(fw)/π",  SIN2_TW_FW * cos2_fw / pi)
    check("sin²θ_W·cos²θ_W/(2π)",        SIN2_TW_FW * cos2_fw / (2.0*pi))

    # ── Dirac large number / simple π formulas ──
    check("1/(137)",                     1.0/137.0,              "integer approx")
    check("1/(137+1/(2π))",              1.0/(137.0+1.0/(2.0*pi)), "naive correction")
    check("1/(4π × φ²)",                 1.0/(4.0*pi*PHI**2))
    check("1/(4π × N^{D/2} × φ)",        1.0/(4.0*pi*N_D2*PHI))
    check("1/(4π × N^{D/2})",            1.0/(4.0*pi*N_D2))
    check("(1-sin²θ_W(fw))/(4π·N^{D/2})", cos2_fw/(4.0*pi*N_D2))

    # ── Framework: exponent from God Eq ──
    log_ratio = 4.0 * pi**2 * N_D2 / B0
    check("b₀/(4π²·N^{D/2})  [1/log_ratio]",   B0/(4.0*pi**2*N_D2))
    check("1/(4π·log_ratio)",                   1.0/(4.0*pi*log_ratio))
    check("sin²θ_W(fw)/log_ratio",              SIN2_TW_FW/log_ratio)

    # ── Explicit 1/137 derivations attempted in literature ──
    # Atiyah's formula: α = exp(-2/3) × (Γ(2/3))²
    try:
        atiyah = exp(-2.0/3.0) * gamma(2.0/3.0)**2
        check("Atiyah: exp(-2/3)·Γ(2/3)²",        atiyah, "Atiyah 2018 (approximate)")
    except Exception:
        pass

    # ── Sort and summarize ──
    identity_hits.sort(key=lambda h: h[0])
    print(f"\n  {'Rank':<5} {'Error%':>8}  Expression")
    print("  " + "-" * 60)
    for rank, (err, label, val) in enumerate(identity_hits[:10], 1):
        print(f"  {rank:<5} {err:>7.4f}%  {label}")

    return identity_hits


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE — 4-panel plot
# ═════════════════════════════════════════════════════════════════════════════

def make_figure(roots, alg_hits, wyler_hits, rg_data, identity_hits, save_path):
    rg_hits_list, mu_range, alpha_run_fw, M_GUT = rg_data

    fig = plt.figure(figsize=(18, 14), facecolor=BG)
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.38,
                            left=0.07, right=0.97, top=0.93, bottom=0.07)
    axes = [fig.add_subplot(gs[r, c]) for r, c in [(0,0),(0,1),(1,0),(1,1)]]

    for ax in axes:
        ax.set_facecolor(BG)
        ax.tick_params(colors=FG, labelsize=9)
        for sp in ax.spines.values():
            sp.set_color(ACCENT)
            sp.set_linewidth(0.8)

    fig.suptitle("α Hunt — Casimir / Propagation Framework", color=GOLD,
                 fontsize=15, fontweight='bold', y=0.97)

    # ── Panel 1: Casimir roots vs spin ──
    ax1 = axes[0]
    spins = [0.0, 0.5, 1.0, 1.5, 2.0]
    x_vals   = [roots[j]       for j in spins]
    mx_vals  = [1.0 - roots[j] for j in spins]
    x2_vals  = [roots[j]**2    for j in spins]
    x3_vals  = [roots[j]**3    for j in spins]

    bar_w = 0.18
    xs    = np.arange(len(spins))
    ax1.bar(xs - 1.5*bar_w, x_vals,  bar_w, color=ACCENT,  alpha=0.85, label='x₊(j)')
    ax1.bar(xs - 0.5*bar_w, mx_vals, bar_w, color=GOLD,    alpha=0.85, label='1-x₊(j)')
    ax1.bar(xs + 0.5*bar_w, x2_vals, bar_w, color=BLUE,    alpha=0.85, label='x₊(j)²')
    ax1.bar(xs + 1.5*bar_w, x3_vals, bar_w, color=PURPLE,  alpha=0.85, label='x₊(j)³')

    ax1.set_xticks(xs)
    ax1.set_xticklabels([f'j={s}' for s in spins], color=FG, fontsize=8)
    ax1.set_ylabel('Value', color=FG, fontsize=9)
    ax1.set_title('Panel 1: Casimir Roots x₊(j)', color=ACCENT, fontsize=10, pad=8)
    ax1.legend(facecolor='#15152a', edgecolor=ACCENT, labelcolor=FG, fontsize=7)
    ax1.yaxis.label.set_color(FG)

    # Mark Weinberg anchor
    x05 = roots[0.5]; x10 = roots[1.0]
    sin2 = 1.0 - x05/x10
    ax1.annotate(f'sin²θ_W={sin2:.5f}', xy=(2, x10), xytext=(1.5, 0.85),
                 color=GREEN, fontsize=7.5,
                 arrowprops=dict(arrowstyle='->', color=GREEN, lw=0.8))

    # ── Panel 2: Best algebraic hits ──
    ax2 = axes[1]
    # Normalise alg_hits (4-tuple) to 3-tuple for combining
    alg3 = [(h[0], h[1], h[2]) for h in alg_hits[:12]]
    all_hits = alg3 + [(h[0], h[1], h[2]) for h in wyler_hits[:6]] + \
               [(h[0], h[1], h[2]) for h in identity_hits[:6]]
    all_hits.sort(key=lambda h: h[0])
    top_hits = all_hits[:15]

    errors  = [h[0] for h in top_hits]
    labels  = [h[1][:38] for h in top_hits]
    colors2 = [GREEN if e < 1.0 else (ACCENT if e < 3.0 else ORANGE) for e in errors]

    ypos = np.arange(len(top_hits))
    ax2.barh(ypos, errors, color=colors2, alpha=0.85, height=0.65)
    ax2.axvline(1.0, color=GREEN, lw=1.0, ls='--', alpha=0.6, label='1% threshold')
    ax2.axvline(5.0, color=RED,   lw=0.8, ls='--', alpha=0.5, label='5% threshold')
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(labels, color=FG, fontsize=6.5)
    ax2.set_xlabel('Error % vs PDG α', color=FG, fontsize=9)
    ax2.set_title('Panel 2: Best Algebraic/Volume Combinations', color=ACCENT,
                  fontsize=10, pad=8)
    ax2.legend(facecolor='#15152a', edgecolor=ACCENT, labelcolor=FG, fontsize=7)
    ax2.invert_yaxis()

    # ── Panel 3: RG running ──
    ax3 = axes[2]
    alpha_run = np.array(alpha_run_fw)
    mu_gev    = mu_range

    valid = alpha_run > 0
    ax3.semilogx(mu_gev[valid], 1.0/alpha_run[valid],
                 color=ACCENT, lw=1.8, label=r'1/α(μ) Framework RG')

    # Reference lines
    ax3.axhline(ALPHA_INV_PDG,  color=GREEN, lw=1.0, ls='--', alpha=0.7,
                label=f'PDG α⁻¹={ALPHA_INV_PDG:.1f}')
    ax3.axhline(ALPHA_MZ_INV,   color=GOLD,  lw=1.0, ls=':',  alpha=0.7,
                label=f'α(M_Z)⁻¹={ALPHA_MZ_INV:.1f}')
    ax3.axhline(4.0*pi,         color=PURPLE,lw=0.8, ls='-.',  alpha=0.7,
                label=f'4π (GUT)={4*pi:.3f}')

    ax3.set_xlabel('μ (GeV)', color=FG, fontsize=9)
    ax3.set_ylabel('1/α(μ)', color=FG, fontsize=9)
    ax3.set_title('Panel 3: RG Running α_GUT=1/(4π) → low energy', color=ACCENT,
                  fontsize=10, pad=8)
    ax3.legend(facecolor='#15152a', edgecolor=ACCENT, labelcolor=FG, fontsize=7,
               loc='upper left')
    ax3.set_ylim(0, 200)
    M_Z_val = 91.1876
    ax3.axvline(M_Z_val, color=BLUE, lw=0.7, ls='--', alpha=0.5)
    ax3.text(M_Z_val*1.1, 10, 'M_Z', color=BLUE, fontsize=7)
    ax3.axvline(M_GUT, color=RED, lw=0.7, ls='--', alpha=0.5)
    ax3.text(M_GUT*0.1, 10, 'M_GUT', color=RED, fontsize=7)

    # ── Panel 4: Summary table ──
    ax4 = axes[3]
    ax4.axis('off')

    # Gather top 3 from each section
    def top3(hits, key_fn):
        s = sorted(hits, key=key_fn)
        return s[:3]

    table_rows = []

    for h in top3(alg_hits, lambda h: h[0]):
        err, label, val = h[0], h[1], h[2]
        table_rows.append(('Algebraic', f"{err:.3f}%", label[:32], f"{1/val:.3f}"))

    for err, label, val in top3(wyler_hits, lambda h: h[0]):
        table_rows.append(('Volume/Wyler', f"{err:.3f}%", label[:32], f"{1/val:.3f}"))

    for rh in top3(rg_hits_list, lambda h: h['err_low']):
        table_rows.append(('RG Running', f"{rh['err_low']:.3f}%",
                           rh['label'][:32], f"{rh['inv_alpha_0']:.3f}"))

    for err, label, val in top3(identity_hits, lambda h: h[0]):
        table_rows.append(('Known Identity', f"{err:.3f}%", label[:32], f"{1/val:.3f}"))

    col_labels = ['Section', 'Error', 'Expression', '1/α']
    col_widths = [0.18, 0.10, 0.50, 0.12]

    y_top = 0.95
    row_h = 0.056
    font_h = 8.5

    # Header
    x_pos = 0.01
    for ci, (clabel, cw) in enumerate(zip(col_labels, col_widths)):
        ax4.text(x_pos, y_top, clabel, color=GOLD, fontsize=9,
                 fontweight='bold', transform=ax4.transAxes, va='top')
        x_pos += cw

    ax4.plot([0.0, 1.0], [y_top - 0.03, y_top - 0.03],
             color=ACCENT, lw=0.8, transform=ax4.transAxes, clip_on=False)

    prev_section = None
    row_i = 0
    for row in table_rows:
        y = y_top - 0.06 - row_i * row_h
        x_pos = 0.01
        section = row[0]
        row_color = FG
        if row[1].replace('%', '').strip():
            try:
                err_val = float(row[1].replace('%', ''))
                if err_val < 1.0:
                    row_color = GREEN
                elif err_val < 3.0:
                    row_color = ACCENT
            except Exception:
                pass

        for ci, (cell, cw) in enumerate(zip(row, col_widths)):
            display = cell if (ci != 0 or section != prev_section) else ''
            ax4.text(x_pos, y, display, color=row_color, fontsize=font_h,
                     transform=ax4.transAxes, va='top')
            x_pos += cw

        if section != prev_section:
            prev_section = section
        row_i += 1

    ax4.set_title('Panel 4: Summary — All Approaches', color=ACCENT, fontsize=10, pad=8)

    plt.savefig(save_path, dpi=140, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"\n  Figure saved → {save_path}")


# ═════════════════════════════════════════════════════════════════════════════
# CONCLUSION
# ═════════════════════════════════════════════════════════════════════════════

def print_conclusion(alg_hits, wyler_hits, rg_hits_list, identity_hits):
    print("\n" + "=" * 68)
    print("  CONCLUSION")
    print("=" * 68)

    # Gather overall best across all sections
    # alg_hits tuples: (err, label, val, inv_val)
    # wyler/identity tuples: (err, label, val)
    candidates = []
    for h in alg_hits[:5]:
        err, label, val = h[0], h[1], h[2]
        candidates.append((err, f"[Algebraic] {label}", val))
    for h in wyler_hits[:5]:
        err, label, val = h[0], h[1], h[2]
        candidates.append((err, f"[Volume] {label}", val))
    for rh in rg_hits_list[:3]:
        if rh['inv_alpha_0'] > 0 and np.isfinite(rh['inv_alpha_0']):
            candidates.append((rh['err_low'], f"[RG] {rh['label']} → low-energy",
                                1.0/rh['inv_alpha_0']))
    for h in identity_hits[:5]:
        err, label, val = h[0], h[1], h[2]
        candidates.append((err, f"[Identity] {label}", val))

    candidates.sort(key=lambda c: c[0])

    print()
    print(f"  PDG α    = {ALPHA_PDG:.10f}  (1/α = {ALPHA_INV_PDG:.6f})")
    print(f"  FW sin²θ = {SIN2_TW_FW}  (DERIVED, sub-0.01% from Casimir polynomial)")
    print()

    best_err, best_label, best_val = candidates[0]

    if best_err < 1.0:
        print(f"  STATUS: POSSIBLE α SIGNAL FOUND")
        print(f"  Best:   {best_label}")
        print(f"          α = {best_val:.10f}  error = {best_err:.4f}%")
        print()
        print("  NEXT STEP: verify whether this combination has geometric meaning")
        print("             within the Propagation Framework's topology.")
    else:
        print(f"  STATUS: α derivation remains OPEN")
        print(f"  Closest approach: {best_label}")
        print(f"  Value: α ≈ {best_val:.8f}  (1/α ≈ {1.0/best_val:.4f})")
        print(f"  Error: {best_err:.3f}%  vs PDG 1/α = {ALPHA_INV_PDG:.3f}")
        print()
        print("  INTERPRETATION:")
        print("  The Casimir polynomial roots do not directly yield α to <1%.")
        print("  The RG running from α_GUT=1/(4π) with SM b_em approaches")
        print("  the correct order of magnitude but requires the full threshold")
        print("  correction from the framework's topology to land on 1/137.")
        print("  The Wyler-type volume formula provides the closest geometric")
        print("  proxy but is not derivable from the Casimir roots alone.")

    print()
    print("  Top 5 candidates across all methods:")
    print(f"  {'Rank':<5} {'Error%':>8}  {'1/α':>8}  Approach")
    print("  " + "-" * 65)
    for rank, (err, label, val) in enumerate(candidates[:5], 1):
        print(f"  {rank:<5} {err:>7.3f}%  {1.0/val:>8.4f}  {label[:50]}")
    print()


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os

    print("\n" + "█" * 68)
    print("  ALPHA (α) CASIMIR HUNT — Propagation Framework")
    print(f"  PDG α⁻¹ = {ALPHA_INV_PDG}  |  sin²θ_W anchor = {SIN2_TW_FW}")
    print("█" * 68)

    roots       = section1_casimir_roots()
    alg_hits    = section2_algebraic_scan(roots)
    wyler_hits  = section3_volume_wyler()
    rg_data     = section4_rg_running()
    id_hits     = section5_known_identities()

    print_conclusion(alg_hits, wyler_hits, rg_data[0], id_hits)

    # Save figure
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    save_path   = os.path.join(script_dir, "alpha_casimir_hunt.png")
    make_figure(roots, alg_hits, wyler_hits, rg_data, id_hits, save_path)

    print("\n" + "█" * 68)
    print("  HUNT COMPLETE")
    print("█" * 68 + "\n")
