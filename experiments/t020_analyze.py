#!/usr/bin/env python3
"""
T-020 Insight Event Analyzer — evaluates CSD against pre-registered criteria.

Reads a session CSV from t020_eeg_runner.py, finds insight events,
computes variance increase in the 5-second pre-insight window vs 30-second baseline,
and reports PASS/FAIL against the protocol threshold.

Protocol: /mnt/d/Fundamentals/protocols/muse_insight_protocol.md
Criteria: >50% variance increase in 5s pre-insight window vs 30s baseline

Usage:
    python t020_analyze.py SESSION.csv
    python t020_analyze.py --all  (analyze all sessions in csd_sessions/)
"""

import csv
import sys
import numpy as np
from pathlib import Path

# Pre-registered thresholds (DO NOT CHANGE after data collection starts)
VARIANCE_INCREASE_THRESHOLD = 0.50   # >50% increase = CSD detected
SUCCESS_RATE_THRESHOLD = 0.70        # ≥7/10 events must show CSD
PRE_INSIGHT_WINDOW_SEC = 5.0
BASELINE_WINDOW_SEC = 30.0


def analyze_session(csv_path):
    """Analyze a single session for CSD before insight events."""
    csv_path = Path(csv_path)

    # Load data
    rows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                'elapsed_sec': float(row['elapsed_sec']),
                'alpha': float(row['alpha']),
                'gamma': float(row['gamma']),
                'alpha_variance': float(row['alpha_variance']),
                'gamma_variance': float(row['gamma_variance']),
                'csd_signal': float(row['csd_signal']),
                'insight_flag': int(row['insight_flag']),
            })

    if not rows:
        return None

    # Find insight events
    insight_times = [r['elapsed_sec'] for r in rows if r['insight_flag'] == 1]

    if not insight_times:
        print(f"  No insight events found in {csv_path.name}")
        return None

    print(f"\n{'='*60}")
    print(f"SESSION: {csv_path.name}")
    print(f"Duration: {rows[-1]['elapsed_sec']:.1f}s | Insight events: {len(insight_times)}")
    print(f"{'='*60}")

    results = []

    for idx, insight_t in enumerate(insight_times):
        # Extract 5-second pre-insight window
        pre_start = insight_t - PRE_INSIGHT_WINDOW_SEC
        pre_data = [r for r in rows if pre_start <= r['elapsed_sec'] <= insight_t]

        # Extract 30-second baseline (before pre-insight window)
        baseline_start = max(0, pre_start - BASELINE_WINDOW_SEC)
        baseline_data = [r for r in rows
                        if baseline_start <= r['elapsed_sec'] < pre_start]

        if len(pre_data) < 10 or len(baseline_data) < 30:
            print(f"  Event #{idx+1}: insufficient data window (pre={len(pre_data)}, base={len(baseline_data)})")
            continue

        # Compute gamma variance in both windows (gamma is the insight band)
        pre_gamma = np.array([r['gamma'] for r in pre_data])
        base_gamma = np.array([r['gamma'] for r in baseline_data])

        pre_var = np.var(pre_gamma)
        base_var = np.var(base_gamma)

        if base_var < 1e-10:
            variance_ratio = float('inf') if pre_var > 1e-10 else 1.0
        else:
            variance_ratio = (pre_var - base_var) / base_var

        # Also check alpha variance (secondary indicator)
        pre_alpha = np.array([r['alpha'] for r in pre_data])
        base_alpha = np.array([r['alpha'] for r in baseline_data])
        alpha_pre_var = np.var(pre_alpha)
        alpha_base_var = np.var(base_alpha)

        if alpha_base_var < 1e-10:
            alpha_ratio = float('inf') if alpha_pre_var > 1e-10 else 1.0
        else:
            alpha_ratio = (alpha_pre_var - alpha_base_var) / alpha_base_var

        # Mean CSD signal (lag-1 autocorrelation) in pre-insight window
        pre_csd = np.mean([r['csd_signal'] for r in pre_data])

        # CSD detected?
        csd_detected = variance_ratio > VARIANCE_INCREASE_THRESHOLD

        result = {
            'event': idx + 1,
            'insight_time': insight_t,
            'gamma_pre_var': pre_var,
            'gamma_base_var': base_var,
            'gamma_increase_pct': variance_ratio * 100,
            'alpha_increase_pct': alpha_ratio * 100,
            'mean_csd_signal': pre_csd,
            'csd_detected': csd_detected,
        }
        results.append(result)

        status = "✅ CSD" if csd_detected else "❌ NO CSD"
        print(f"\n  Event #{idx+1} @ T={insight_t:.1f}s")
        print(f"    γ variance: {pre_var:.6f} (pre) vs {base_var:.6f} (baseline)")
        print(f"    γ increase: {variance_ratio*100:+.1f}% {status}")
        print(f"    α increase: {alpha_ratio*100:+.1f}%")
        print(f"    CSD signal (autocorr): {pre_csd:.4f}")

    if not results:
        return None

    # Summary
    n_events = len(results)
    n_csd = sum(1 for r in results if r['csd_detected'])
    success_rate = n_csd / n_events if n_events > 0 else 0
    passed = success_rate >= SUCCESS_RATE_THRESHOLD and n_events >= 10

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"  Events analyzed: {n_events}")
    print(f"  CSD detected: {n_csd}/{n_events} ({success_rate*100:.0f}%)")
    print(f"  Threshold: ≥{SUCCESS_RATE_THRESHOLD*100:.0f}% ({int(SUCCESS_RATE_THRESHOLD*10)}/10)")
    print(f"  Result: {'✅ PASS — CSD confirmed' if passed else '❌ FAIL — CSD not confirmed' if n_events >= 10 else '⏳ INCOMPLETE — need more events'}")
    print(f"{'='*60}")

    return {
        'session': csv_path.name,
        'n_events': n_events,
        'n_csd': n_csd,
        'success_rate': success_rate,
        'passed': passed,
        'details': results,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python t020_analyze.py SESSION.csv")
        print("       python t020_analyze.py --all")
        sys.exit(1)

    if sys.argv[1] == '--all':
        session_dir = Path('/mnt/d/P1/data/csd_sessions')
        csv_files = sorted(session_dir.glob('session_*.csv'))
        if not csv_files:
            print("No session files found.")
            sys.exit(1)

        all_results = []
        for csv_file in csv_files:
            result = analyze_session(csv_file)
            if result:
                all_results.append(result)

        if all_results:
            total_events = sum(r['n_events'] for r in all_results)
            total_csd = sum(r['n_csd'] for r in all_results)
            print(f"\n{'='*60}")
            print(f"GRAND TOTAL ACROSS ALL SESSIONS")
            print(f"  Sessions: {len(all_results)}")
            print(f"  Total events: {total_events}")
            print(f"  Total CSD: {total_csd}/{total_events}")
            print(f"  Overall rate: {total_csd/total_events*100:.0f}%" if total_events > 0 else "  No events")
            print(f"  Protocol requirement: ≥10 events with ≥7 showing CSD")
            print(f"{'='*60}")
    else:
        analyze_session(sys.argv[1])


if __name__ == '__main__':
    main()
