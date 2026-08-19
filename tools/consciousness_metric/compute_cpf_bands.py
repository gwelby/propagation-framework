"""
compute_cpf_bands.py
Run C_PF_reduced_proxy on CSD band-power session files.

DEPRECATION WARNING (2026-08-20):
This script uses the legacy C_PF_reduced = D_int × C_coh_plv × (1 + D_dir_proxy)
formula. The canonical v1.0 consciousness-metric candidate is
    C_PF = D_int × C_coh_wpli × L_self
where L_self is the single-joint-covariance conditional-MI self-loop gate
implemented in cpf.self_model. This script is retained only for historical
session reprocessing and should not be used for new work without a migration
plan.

Input format: CSD session CSV with columns:
  timestamp, elapsed_sec, delta, theta, alpha, beta, gamma, ...

These are relative band-power time series at ~9Hz.
We adapt the C_PF pipeline: delay embedding on band time series,
PLV coherence between band pairs, transfer entropy proxy.

Usage:
    python3 compute_cpf_bands.py /path/to/session_XXXXXXXX.csv
    python3 compute_cpf_bands.py /path/to/session.csv --window_min 5 --step_min 5
"""

import argparse
import numpy as np
import sys
import os

def load_csd_session(filepath):
    """Load CSD band-power CSV. Returns (bands_array, fs_approx)."""
    import csv
    rows = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows.append([
                    float(row['timestamp']),
                    float(row['delta']),
                    float(row['theta']),
                    float(row['alpha']),
                    float(row['beta']),
                    float(row['gamma']),
                ])
            except (ValueError, KeyError):
                continue

    data = np.array(rows)
    timestamps = data[:, 0]
    bands = data[:, 1:].T  # shape: (5, n_samples) — delta, theta, alpha, beta, gamma

    # Estimate sampling rate
    dt_median = np.median(np.diff(timestamps))
    fs = 1.0 / dt_median

    return bands, fs, timestamps

def bandnames():
    return ['delta', 'theta', 'alpha', 'beta', 'gamma']

def reject_artifacts_bands(bands, threshold_std=4.0, window_sec=10.0, fs=9.3):
    """Epoch band-power data and reject windows with extreme values."""
    n_channels, n_samples = bands.shape
    window_samples = int(window_sec * fs)
    if window_samples < 10:
        window_samples = 10

    epochs = []
    for start in range(0, n_samples - window_samples, window_samples):
        epoch = bands[:, start:start + window_samples]
        # Reject if any band has extreme z-score (artifact or dropout)
        z = np.abs((epoch - epoch.mean(axis=1, keepdims=True)) /
                   (epoch.std(axis=1, keepdims=True) + 1e-9))
        if z.max() < threshold_std and np.all(epoch.std(axis=1) > 1e-6):
            epochs.append(epoch)

    return epochs

def compute_plv_bands(epoch):
    """PLV between band pairs using Hilbert analytic signal."""
    from scipy.signal import hilbert
    n_bands, n_samples = epoch.shape
    plv_matrix = np.zeros((n_bands, n_bands))

    phases = []
    for i in range(n_bands):
        analytic = hilbert(epoch[i] - epoch[i].mean())
        phases.append(np.angle(analytic))

    for i in range(n_bands):
        for j in range(i + 1, n_bands):
            phase_diff = phases[i] - phases[j]
            plv = np.abs(np.mean(np.exp(1j * phase_diff)))
            plv_matrix[i, j] = plv
            plv_matrix[j, i] = plv

    return plv_matrix

def compute_d_int_bands(epoch):
    """Effective dimensionality of band-power manifold (PCA entropy)."""
    n_bands, n_samples = epoch.shape
    # Normalize
    centered = epoch - epoch.mean(axis=1, keepdims=True)
    cov = np.cov(centered)
    eigenvalues = np.linalg.eigvalsh(cov)
    eigenvalues = eigenvalues[eigenvalues > 0]
    if len(eigenvalues) == 0:
        return 0.0

    # Normalized entropy
    p = eigenvalues / eigenvalues.sum()
    p = p[p > 1e-12]
    entropy = -np.sum(p * np.log(p))
    max_entropy = np.log(len(eigenvalues))
    d_int = entropy / max_entropy if max_entropy > 0 else 0.0
    return float(d_int)

def compute_dir_proxy_bands(epoch, tau=2):
    """Transfer entropy proxy: cross-lagged MI between alpha and gamma."""
    alpha = epoch[2]  # alpha
    gamma = epoch[4]  # gamma

    if len(alpha) <= tau + 1:
        return 0.0

    # Lagged correlation as proxy for directed information
    from scipy.stats import pearsonr
    try:
        r_forward, _ = pearsonr(alpha[:-tau], gamma[tau:])
        r_backward, _ = pearsonr(gamma[:-tau], alpha[tau:])
        # Asymmetry = directed information proxy
        dir_proxy = max(0.0, abs(r_forward) - abs(r_backward))
        return float(dir_proxy)
    except Exception:
        return 0.0

def compute_cpf_epoch(epoch, tau=2):
    """Compute C_PF_reduced_proxy for one band-power epoch."""
    d_int = compute_d_int_bands(epoch)
    plv_matrix = compute_plv_bands(epoch)

    # Mean off-diagonal PLV as C_coh proxy
    n = plv_matrix.shape[0]
    off_diag = plv_matrix[np.triu_indices(n, k=1)]
    c_coh_plv = float(np.mean(off_diag))

    # Alpha-gamma PLV specifically (cross-frequency coupling — consciousness correlate)
    c_coh_alpha_gamma = float(plv_matrix[2, 4])

    dir_proxy = compute_dir_proxy_bands(epoch, tau=tau)

    # C_PF_reduced_proxy = D_int × C_coh × (1 + dir_proxy)
    c_pf = d_int * c_coh_plv * (1.0 + dir_proxy)

    return {
        'D_int': d_int,
        'C_coh_plv': c_coh_plv,
        'C_coh_alpha_gamma': c_coh_alpha_gamma,
        'D_dir_proxy': dir_proxy,
        'C_PF_reduced': c_pf,
    }

def main():
    parser = argparse.ArgumentParser(
        description="C_PF_reduced_proxy on CSD band-power session files."
    )
    parser.add_argument("csv_path", type=str)
    parser.add_argument("--window_min", type=float, default=5.0,
                        help="Analysis window in minutes (default: 5)")
    parser.add_argument("--step_min", type=float, default=5.0,
                        help="Step between windows in minutes (default: 5)")
    parser.add_argument("--tau", type=int, default=2,
                        help="Transfer entropy lag in samples (default: 2)")
    args = parser.parse_args()

    if not os.path.exists(args.csv_path):
        print(f"Error: {args.csv_path} not found")
        sys.exit(1)

    print(f"Loading {args.csv_path}...")
    bands, fs, timestamps = load_csd_session(args.csv_path)

    duration_min = (timestamps[-1] - timestamps[0]) / 60
    print(f"  Channels: {bands.shape[0]} bands × {bands.shape[1]} samples")
    print(f"  Duration: {duration_min:.1f} min at {fs:.1f} Hz")
    print(f"  Bands: {bandnames()}")

    window_samples = int(args.window_min * 60 * fs)
    step_samples = int(args.step_min * 60 * fs)

    print(f"\nEpoching: {args.window_min:.0f}-min windows, {args.step_min:.0f}-min steps...")

    all_scores = []
    n_samples = bands.shape[1]
    window_num = 0

    for start in range(0, n_samples - window_samples, step_samples):
        window = bands[:, start:start + window_samples]
        t_offset_min = (timestamps[start] - timestamps[0]) / 60

        # Reject artifact windows
        sub_epochs = reject_artifacts_bands(window, fs=fs, window_sec=10.0)
        if len(sub_epochs) < 3:
            window_num += 1
            continue

        # Compute score for each sub-epoch, average
        epoch_scores = [compute_cpf_epoch(ep, tau=args.tau) for ep in sub_epochs]
        avg = {k: float(np.mean([s[k] for s in epoch_scores])) for k in epoch_scores[0]}
        avg['t_min'] = t_offset_min
        avg['n_epochs'] = len(sub_epochs)
        all_scores.append(avg)

        window_num += 1
        if window_num <= 3 or window_num % 10 == 0:
            print(f"  t={t_offset_min:.0f}min | D_int={avg['D_int']:.3f} "
                  f"C_coh={avg['C_coh_plv']:.3f} "
                  f"α-γ={avg['C_coh_alpha_gamma']:.3f} "
                  f"Dir={avg['D_dir_proxy']:.3f} "
                  f"C_PF={avg['C_PF_reduced']:.4f}")

    if not all_scores:
        print("No valid windows. Check data quality.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"SESSION SUMMARY — {os.path.basename(args.csv_path)}")
    print(f"{'='*60}")
    for key in ['D_int', 'C_coh_plv', 'C_coh_alpha_gamma', 'D_dir_proxy', 'C_PF_reduced']:
        vals = [s[key] for s in all_scores]
        print(f"  {key:22s}: mean={np.mean(vals):.4f}  std={np.std(vals):.4f}  "
              f"min={np.min(vals):.4f}  max={np.max(vals):.4f}")

    print(f"\n  Windows scored: {len(all_scores)}")

    # Null comparison baseline (white noise on same shape)
    noise = np.random.randn(*bands[:, :window_samples].shape)
    noise_sub = reject_artifacts_bands(noise, fs=fs, window_sec=10.0)
    if noise_sub:
        ns = compute_cpf_epoch(noise_sub[0])
        print(f"\n  Null (white noise) C_PF_reduced ≈ {ns['C_PF_reduced']:.4f}")

    print(f"{'='*60}")

if __name__ == "__main__":
    main()
