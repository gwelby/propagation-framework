"""
Phi vs Sampling Period — Chord Postulate Test
==============================================
Tests the Propagation Framework's Chord Postulate prediction:

    Integrated information (Phi) peaks when the observation lag matches
    the cortical round-trip propagation time.

Predicted peak zone (from MASTER.md, time_emergent):
    L ≈ 0.15 m        (human cortex diameter)
    v ≈ 1.5–2.0 m/s   (myelinated propagation, long-range association fibers)
    v_eff = √(1.5 × 2.0) ≈ 1.73 m/s
    θ_eff = L / v_eff = 0.15 / 1.73 ≈ 88 ms
    2θ_eff ≈ 176 ms
    PREDICTION: Phi proxy peaks in [88, 176] ms

Signal model:
    Each cortical area i has an independent broadband noise source s_i(t).
    Observed activity at node j:
        x_j(t) = η * s_j(t) + w * Σᵢ∈in(j) s_i(t − δᵢⱼ) / deg(j)

    Bandpass: 1–50 Hz (cortical LFP range).
    This is numerically stable, biologically motivated (Honey et al. 2007),
    and creates a sharp cross-correlation peak at lag δᵢⱼ for connected pairs.

Phi proxy — MEAN BASELINE-SUBTRACTED CROSS-CORRELATION at lag τ:
    For each pair (i,j):
        r_ij(τ) = Pearson corr(x_i(t), x_j(t+τ))

    We subtract the mean over the full lag range (removes common baseline
    from indirect connections and filter autocorr artifacts), then average:
        Phi(τ) = mean_{i≠j} [ r_ij(τ) − mean_τ(r_ij) ]

    This captures: at which lag does information flow peak ABOVE the baseline?
    Answer: at τ ≈ mean(δᵢⱼ) — the propagation delay.

    For Gaussian signals, MI(X_i;X_j|τ) = −½ log(1−r²), so the baseline-
    subtracted peak in |r| directly identifies the integration timescale.

Network:
    N = 16 nodes, small-world topology, 2 runs:
      Run A: delay_mean = 100 ms  (inside 88–176ms zone — should peak YES)
      Run B: delay_mean =  40 ms  (outside zone — should peak NO)
    This double-run design tests both prediction AND falsifiability.

Output:
    - phi_vs_delay.png
    - Prints: PEAK IN PREDICTED RANGE? YES/NO
    - Appends result to sandbox_results.md

References:
    - Chord Postulate: MASTER.md (time_emergent), 2026-03-16
    - Honey CJ et al (2007). PNAS 104:10240. (structural delays → functional lags)
    - Barnett L et al (2009). PRL 103:238701. (TE ≡ Granger causality)
    - Tononi G (2004). BMC Neuroscience 5:42. (Phi definition)
    - Buzsáki G (2006). Rhythms of the Brain. (propagation speeds)
"""

import numpy as np
from scipy.signal import butter, sosfilt
from scipy.ndimage import gaussian_filter1d
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ─── Reproducibility ──────────────────────────────────────────────────────────
RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

# ─── Simulation Parameters ────────────────────────────────────────────────────
N_NODES        = 16
DURATION_S     = 60.0          # seconds
FS_HZ          = 1000.0        # Hz (1 ms resolution)
N_SAMPLES      = int(DURATION_S * FS_HZ)
BP_LOW_HZ      = 1.0
BP_HIGH_HZ     = 50.0
LOCAL_NOISE    = 0.6           # local source amplitude
COUPLING_W     = 0.8           # coupling weight (per neighbour, degree-normalised)
N_LONG_RANGE   = 12

# ─── Chord Postulate Predicted Peak Zone ─────────────────────────────────────
PEAK_LOW_MS    = 88.0
PEAK_HIGH_MS   = 176.0

# ─── Lags to scan ─────────────────────────────────────────────────────────────
LAGS_MS = np.array([
    10, 15, 20, 30, 40, 50, 60, 70, 80, 88, 95,
    100, 110, 120, 130, 140, 150, 160, 176,
    190, 210, 240, 270, 300, 350, 400, 450, 500
], dtype=float)


# ─── Build network ────────────────────────────────────────────────────────────

def build_network(n, n_lr, delay_mean_ms, delay_std_ms=15.0, delay_min_ms=20.0):
    adj = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for d in [1, 2]:
            j = (i + d) % n
            adj[i, j] = True
            adj[j, i] = True
    added, attempts = 0, 0
    while added < n_lr and attempts < 10_000:
        i, j = rng.integers(0, n, size=2)
        if i != j and not adj[i, j]:
            adj[i, j] = True
            adj[j, i] = True
            added += 1
        attempts += 1
    delay_ms = np.zeros((n, n))
    rows, cols = np.where(adj)
    raw = rng.normal(delay_mean_ms, delay_std_ms, len(rows))
    raw = np.clip(raw, delay_min_ms, None)
    delay_ms[rows, cols] = raw
    return adj, delay_ms


# ─── Generate signals ─────────────────────────────────────────────────────────

def generate_signals(adj, delay_ms):
    """
    x_j(t) = LOCAL_NOISE * s_j(t) + COUPLING_W/deg(j) * Σᵢ s_i(t − δᵢⱼ)

    Numerically stable: linear superposition of filtered noise.
    Cross-correlation r(x_i, x_j) peaks at lag δᵢⱼ for connected pairs.
    """
    n = adj.shape[0]
    max_d_samp = int(np.max(delay_ms) * FS_HZ / 1000.0) + 10
    total = N_SAMPLES + max_d_samp

    sos = butter(4, [BP_LOW_HZ, BP_HIGH_HZ], btype="bandpass", fs=FS_HZ, output="sos")
    sources = np.array([sosfilt(sos, rng.standard_normal(total)) for _ in range(n)])
    # sources: (n, total)

    observed = np.zeros((N_SAMPLES, n))
    for j in range(n):
        sig = LOCAL_NOISE * sources[j, max_d_samp:]
        in_nb = np.where(adj[:, j])[0]
        deg = max(len(in_nb), 1)
        for i in in_nb:
            d_samp = int(round(delay_ms[i, j] * FS_HZ / 1000.0))
            start = max_d_samp - d_samp
            sig += (COUPLING_W / deg) * sources[i, start:start + N_SAMPLES]
        m, s = sig.mean(), sig.std()
        observed[:, j] = (sig - m) / s if s > 1e-12 else sig

    return observed


# ─── Phi proxy: baseline-subtracted cross-correlation at lag τ ─────────────

def compute_phi_profile(signal):
    """
    Compute r_ij(τ) for all pairs (i,j), all lags in LAGS_MS.
    Returns: (n_lags, n_pairs) array of Pearson r values.
    """
    T, n = signal.shape
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    n_lags = len(LAGS_MS)
    n_pairs = len(pairs)

    R = np.zeros((n_lags, n_pairs))
    for li, lag_ms in enumerate(LAGS_MS):
        lag_s = max(1, int(round(lag_ms * FS_HZ / 1000.0)))
        if T - lag_s < 100:
            continue
        for pi, (i, j) in enumerate(pairs):
            xp = signal[:T - lag_s, i]
            yf = signal[lag_s:, j]
            sx, sy = xp.std(), yf.std()
            if sx > 1e-12 and sy > 1e-12:
                R[li, pi] = np.mean((xp - xp.mean()) * (yf - yf.mean())) / (sx * sy)

    return R, pairs


def phi_proxy_from_profile(R):
    """
    Phi proxy = mean over pairs of (r_ij(τ) − mean_τ(r_ij)).

    Subtracting the per-pair lag-mean removes the common baseline (indirect
    connections, filter pedestal) and isolates lag-specific structure.
    The result is positive where r is ABOVE baseline, negative below.
    Taking the mean gives the lag at which the WHOLE NETWORK is maximally
    integrated above its own baseline.

    Returns: (n_lags,) array — the Phi proxy curve.
    """
    # Per-pair baseline: mean over lags
    pair_mean = R.mean(axis=0, keepdims=True)   # (1, n_pairs)
    R_demeaned = R - pair_mean                   # (n_lags, n_pairs)
    return R_demeaned.mean(axis=1)               # (n_lags,)


# ─── Run a single test ────────────────────────────────────────────────────────

def run_test(delay_mean_ms, label):
    print(f"\n{'='*64}")
    print(f"Test: {label}")
    print(f"Predicted peak zone: {PEAK_LOW_MS:.0f}–{PEAK_HIGH_MS:.0f} ms")
    print(f"{'='*64}")

    adj, delay_ms = build_network(N_NODES, N_LONG_RANGE, delay_mean_ms)
    actual_delays = delay_ms[adj]
    print(f"  Edges (directed): {adj.sum()}")
    print(f"  Delays: {actual_delays.mean():.1f} ± {actual_delays.std():.1f} ms  "
          f"[{actual_delays.min():.1f}–{actual_delays.max():.1f} ms]")

    print(f"  Generating {DURATION_S:.0f}s of bandpass-filtered signals...")
    signal = generate_signals(adj, delay_ms)
    print(f"  Signal shape: {signal.shape}")

    print(f"  Computing cross-correlation profiles ({N_NODES*(N_NODES-1)} pairs × {len(LAGS_MS)} lags)...")
    R, pairs = compute_phi_profile(signal)
    phi_values = phi_proxy_from_profile(R)

    print(f"\n  Phi proxy (baseline-subtracted mean cross-corr):")
    for li, lag_ms in enumerate(LAGS_MS):
        zone = "  *** IN ZONE ***" if PEAK_LOW_MS <= lag_ms <= PEAK_HIGH_MS else ""
        print(f"    {lag_ms:6.0f} ms  →  Phi = {phi_values[li]:+.5f}{zone}")

    phi_smooth = gaussian_filter1d(phi_values, sigma=1.5)
    peak_idx    = int(np.argmax(phi_smooth))
    peak_ms_val = LAGS_MS[peak_idx]
    raw_peak_ms = LAGS_MS[int(np.argmax(phi_values))]
    in_range    = PEAK_LOW_MS <= peak_ms_val <= PEAK_HIGH_MS
    verdict     = "YES" if in_range else "NO"

    print(f"\n  RAW PEAK:       {raw_peak_ms:.0f} ms")
    print(f"  SMOOTHED PEAK:  {peak_ms_val:.0f} ms  (Phi = {phi_smooth[peak_idx]:+.5f})")
    print(f"  MEAN DELAY:     {actual_delays.mean():.1f} ms")
    print(f"  PEAK IN PREDICTED RANGE [{PEAK_LOW_MS:.0f}–{PEAK_HIGH_MS:.0f} ms]? {verdict}")

    return dict(
        label=label,
        delay_mean_ms=delay_mean_ms,
        actual_delays=actual_delays,
        n_edges=int(adj.sum()),
        phi_values=phi_values,
        phi_smooth=phi_smooth,
        peak_ms=peak_ms_val,
        raw_peak_ms=raw_peak_ms,
        verdict=verdict,
        in_range=in_range,
    )


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plot_path  = os.path.join(script_dir, "phi_vs_delay.png")

    result_A = run_test(100.0, "Run A: delay=100ms (inside 88–176ms zone)")
    result_B = run_test(40.0,  "Run B: delay=40ms  (outside zone — falsification)")

    primary_verdict = result_A["verdict"]
    mechanism_works = (result_A["verdict"] == "YES" and result_B["verdict"] == "NO")

    print(f"\n{'='*64}")
    print("SUMMARY")
    print(f"  Run A (delay 100ms, inside zone):  peak = {result_A['peak_ms']:.0f} ms → {result_A['verdict']}")
    print(f"  Run B (delay  40ms, outside zone): peak = {result_B['peak_ms']:.0f} ms → {result_B['verdict']}")
    print(f"  Mechanism discriminates correctly? {'YES' if mechanism_works else 'PARTIAL/NO'}")
    print(f"\n  PRIMARY RESULT (Run A): PEAK IN PREDICTED RANGE? {primary_verdict}")
    print(f"{'='*64}")

    # ─── Plot ─────────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        "Chord Postulate Test: Baseline-Subtracted Cross-Node MI vs Lag\n"
        "Propagation Framework — Biological Phase Transition",
        fontsize=12, fontweight="bold"
    )

    for col_idx, result in enumerate([result_A, result_B]):
        ax_phi  = axes[0, col_idx]
        ax_hist = axes[1, col_idx]

        phi_v   = result["phi_values"]
        phi_s   = result["phi_smooth"]
        peak_ms = result["peak_ms"]
        verdict = result["verdict"]
        adm     = result["actual_delays"].mean()
        ads     = result["actual_delays"].std()
        label   = result["label"]

        ax_phi.axhline(0, color="grey", linewidth=0.8, linestyle=":", alpha=0.6)
        ax_phi.plot(LAGS_MS, phi_v, "o--", color="steelblue",
                    alpha=0.45, markersize=5, label="Phi proxy (raw)")
        ax_phi.plot(LAGS_MS, phi_s, "-", color="steelblue",
                    linewidth=2.5, label="Phi proxy (smoothed)")
        ax_phi.axvspan(PEAK_LOW_MS, PEAK_HIGH_MS, alpha=0.15, color="orange",
                       label=f"Predicted zone ({PEAK_LOW_MS:.0f}–{PEAK_HIGH_MS:.0f} ms)")
        ax_phi.axvline(peak_ms, color="red", linestyle="--", linewidth=1.8,
                       label=f"Peak = {peak_ms:.0f} ms")
        ax_phi.scatter([peak_ms], [phi_s[int(np.argmax(phi_s))]],
                       color="red", zorder=5, s=80)
        ax_phi.axvline(adm, color="green", linestyle="-.", linewidth=1.3,
                       alpha=0.7, label=f"Mean delay = {adm:.0f} ms")

        verdict_color = "green" if result["in_range"] else "crimson"
        ax_phi.text(0.97, 0.96, f"IN ZONE? {verdict}",
                    transform=ax_phi.transAxes, ha="right", va="top",
                    fontsize=11, fontweight="bold", color=verdict_color,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                              edgecolor=verdict_color, alpha=0.9))

        mtext = (f"Delays: {adm:.0f} ± {ads:.0f} ms\n"
                 f"LOCAL={LOCAL_NOISE}, COUP={COUPLING_W}\n"
                 "Phi = mean(r_ij(τ) − mean_τ(r_ij))")
        ax_phi.text(0.02, 0.04, mtext, transform=ax_phi.transAxes, fontsize=8,
                    va="bottom", ha="left",
                    bbox=dict(boxstyle="round", facecolor="lightyellow",
                              edgecolor="grey", alpha=0.85))

        ax_phi.set_title(label, fontsize=9, fontweight="bold")
        ax_phi.set_xlabel("Lag (ms)", fontsize=10)
        ax_phi.set_ylabel("Phi Proxy (baseline-subtracted |r|)", fontsize=10)
        ax_phi.set_xscale("log")
        ax_phi.set_xlim(LAGS_MS[0] * 0.85, LAGS_MS[-1] * 1.15)
        ax_phi.legend(fontsize=8, loc="upper right")
        ax_phi.grid(True, alpha=0.3)

        # Delay distribution
        ad = result["actual_delays"]
        ax_hist.hist(ad, bins=20, color="steelblue", alpha=0.7, edgecolor="white")
        ax_hist.axvspan(PEAK_LOW_MS, PEAK_HIGH_MS, alpha=0.2, color="orange",
                        label="Predicted zone")
        ax_hist.axvline(ad.mean(), color="red", linestyle="--",
                        label=f"Mean = {ad.mean():.0f} ms")
        ax_hist.set_xlabel("Connection Delay (ms)", fontsize=9)
        ax_hist.set_ylabel("Edge count", fontsize=9)
        ax_hist.set_title("Delay Distribution", fontsize=9)
        ax_hist.legend(fontsize=8)
        ax_hist.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    print(f"\nPlot saved: {plot_path}")

    # ─── Append to sandbox_results.md ─────────────────────────────────────────
    now = datetime.now().strftime("%Y-%m-%d")
    A  = result_A
    B  = result_B

    result_block = f"""
---

## {now} — phi_vs_delay.py — Chord Postulate Test (v5: baseline-subtracted cross-corr)

**Prediction tested**: Phi proxy peaks at lag = 88–176 ms
(Chord Postulate: L=0.15m, v_eff=1.73 m/s → one-way 88ms, round-trip 176ms)

**Method**: Bandpass-filtered broadband signals (1–50Hz), linear delay mixing.
Phi(τ) = mean_{{pairs}} [ r_ij(τ) − mean_τ(r_ij) ].
Baseline subtraction removes indirect-path and filter artifacts.
This isolates the lag-specific cross-node information flow peak.

**Signal**: LOCAL_NOISE={LOCAL_NOISE}, COUPLING_W={COUPLING_W}, {DURATION_S:.0f}s at {FS_HZ:.0f}Hz.
**Network**: N={N_NODES} nodes, small-world, {A['n_edges']} directed edges.

**Run A (delay 100ms — inside zone)**:
  - Actual delays: {A['actual_delays'].mean():.1f} ± {A['actual_delays'].std():.1f} ms
  - Raw peak: {A['raw_peak_ms']:.0f} ms | Smoothed peak: {A['peak_ms']:.0f} ms
  - PEAK IN PREDICTED RANGE [{PEAK_LOW_MS:.0f}–{PEAK_HIGH_MS:.0f} ms]? **{A['verdict']}**

**Run B (delay 40ms — outside zone, falsification)**:
  - Actual delays: {B['actual_delays'].mean():.1f} ± {B['actual_delays'].std():.1f} ms
  - Raw peak: {B['raw_peak_ms']:.0f} ms | Smoothed peak: {B['peak_ms']:.0f} ms
  - PEAK IN PREDICTED RANGE? **{B['verdict']}**

**Mechanism discriminates? {'YES' if mechanism_works else 'PARTIAL/NO'}**

**PRIMARY RESULT (Run A)**: PEAK IN PREDICTED RANGE? **{primary_verdict}**

**Honest verdict**: {"SUPPORTS Chord Postulate. MI proxy peaks within 88–176ms when delays are centred at 100ms. Run B correctly falls outside. Delay-resonance mechanism confirmed: cross-node information integration peaks at the propagation delay timescale. CAVEAT: delays were set to 100ms (inside zone). True biological test = EEG cross-correlation analysis with empirical inter-area lags." if mechanism_works else f"Partial confirmation. Run A peak={A['peak_ms']:.0f}ms ({A['verdict']}), Run B peak={B['peak_ms']:.0f}ms ({B['verdict']}). Mechanism may work but proxy or parameters need refinement."}

**Plot**: sandbox/phi_vs_delay.png
**Next step**: EEG CSD recorder data → empirical cross-correlation lags → compare to 88–176ms prediction.
"""

    results_file = os.path.join(script_dir, "sandbox_results.md")
    with open(results_file, "a") as f:
        f.write(result_block)
    print(f"Result appended to: {results_file}")

    return primary_verdict


if __name__ == "__main__":
    verdict = main()
    exit(0 if verdict == "YES" else 1)
