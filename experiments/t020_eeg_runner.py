#!/usr/bin/env python3
"""
T-020 EEG Experiment Runner — Critical Slowing Down before insight.

Records Muse EEG via BrainFlow, listens for spacebar to mark insight events,
computes CSD indicators in real-time, and saves to CSV for analysis.

Usage:
    python t020_eeg_runner.py [--output DIR] [--session-name NAME]

Controls:
    SPACEBAR  — mark insight event (sets insight_flag=1 for that sample)
    Ctrl+C    — stop recording and save

Output CSV format matches existing session files in P1/data/csd_sessions/
for compatibility with analyze_real_eeg.py and eeg_csd_analysis.py.

Protocol: /mnt/d/Fundamentals/protocols/muse_insight_protocol.md
"""

import argparse
import csv
import os
import sys
import time
import threading
import numpy as np
from pathlib import Path
from datetime import datetime

# BrainFlow
try:
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
    from brainflow.data_filter import DataFilter
    BRAINFLOW_AVAILABLE = True
except ImportError:
    BRAINFLOW_AVAILABLE = False
    print("ERROR: brainflow not installed. Run: pip install brainflow")
    sys.exit(1)

# Keyboard listener (cross-platform)
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("WARNING: 'keyboard' not installed. Insight marking via keyboard will not work.")
    print("  Install: pip install keyboard")
    print("  Running without insight trigger — you'll need to add markers manually.")
    print()


# ─── Constants ───────────────────────────────────────────────────────

SAMPLING_RATE = 256          # Muse 2 default
CHANNEL_NAMES = ['TP9', 'AF7', 'AF8', 'TP10']
BAND_NAMES = ['delta', 'theta', 'alpha', 'beta', 'gamma']
CSD_WINDOW_SEC = 1.0         # 1-second sliding window for variance
BASELINE_WINDOW_SEC = 30.0   # 30-second rolling baseline for contrast
SAVE_INTERVAL_SEC = 10.0     # save checkpoint every 10 seconds

CSV_COLUMNS = [
    'timestamp', 'elapsed_sec',
    'delta', 'theta', 'alpha', 'beta', 'gamma',
    'alpha_variance', 'gamma_variance',
    'alpha_vs_baseline', 'gamma_vs_baseline',
    'csd_signal', 'insight_flag'
]


# ─── CSD Computation ─────────────────────────────────────────────────

class CSDTracker:
    """Tracks Critical Slowing Down indicators in real-time."""

    def __init__(self, sampling_rate=SAMPLING_RATE):
        self.fs = sampling_rate
        self.window_samples = int(CSD_WINDOW_SEC * sampling_rate)
        self.baseline_samples = int(BASELINE_WINDOW_SEC * sampling_rate)

        # Rolling buffers for band powers
        self.alpha_history = []
        self.gamma_history = []
        self.variance_history = []

        # Baseline tracking
        self.alpha_baseline = []
        self.gamma_baseline = []

        # Current values
        self.alpha_var = 0.0
        self.gamma_var = 0.0
        self.alpha_baseline_val = 1.0
        self.gamma_baseline_val = 1.0
        self.alpha_vs_baseline = 1.0
        self.gamma_vs_baseline = 1.0
        self.csd_signal = 0.0

    def update(self, alpha_power, gamma_power):
        """Update with new band power sample. Returns current CSD state."""
        self.alpha_history.append(alpha_power)
        self.gamma_history.append(gamma_power)

        # Keep buffer bounded (5 minutes max)
        max_buf = self.fs * 300
        if len(self.alpha_history) > max_buf:
            self.alpha_history = self.alpha_history[-max_buf:]
            self.gamma_history = self.gamma_history[-max_buf:]

        # Compute variance over sliding window
        if len(self.alpha_history) >= self.window_samples:
            alpha_window = np.array(self.alpha_history[-self.window_samples:])
            gamma_window = np.array(self.gamma_history[-self.window_samples:])

            self.alpha_var = float(np.var(alpha_window))
            self.gamma_var = float(np.var(gamma_window))

            # Lag-1 autocorrelation (CSD indicator)
            if len(alpha_window) > 1 and np.var(alpha_window) > 0:
                ac = np.corrcoef(alpha_window[:-1], alpha_window[1:])[0, 1]
                self.csd_signal = ac if not np.isnan(ac) else 0.0

        # Rolling baseline
        self.alpha_baseline.append(alpha_power)
        self.gamma_baseline.append(gamma_power)
        if len(self.alpha_baseline) > self.baseline_samples:
            self.alpha_baseline = self.alpha_baseline[-self.baseline_samples:]
            self.gamma_baseline = self.gamma_baseline[-self.baseline_samples:]

        if len(self.alpha_baseline) >= self.baseline_samples:
            self.alpha_baseline_val = max(float(np.mean(self.alpha_baseline)), 0.001)
            self.gamma_baseline_val = max(float(np.mean(self.gamma_baseline)), 0.001)
            self.alpha_vs_baseline = alpha_power / self.alpha_baseline_val
            self.gamma_vs_baseline = gamma_power / self.gamma_baseline_val

        return {
            'alpha_variance': self.alpha_var,
            'gamma_variance': self.gamma_var,
            'alpha_vs_baseline': self.alpha_vs_baseline,
            'gamma_vs_baseline': self.gamma_vs_baseline,
            'csd_signal': self.csd_signal,
        }


# ─── Insight Trigger ─────────────────────────────────────────────────

class InsightTrigger:
    """Thread-safe insight event marker."""

    def __init__(self):
        self.flagged = False
        self.event_count = 0
        self._lock = threading.Lock()

    def mark(self):
        with self._lock:
            self.flagged = True
            self.event_count += 1
            print(f"\n  ⚡ INSIGHT EVENT #{self.event_count} marked at {time.time():.2f}")

    def consume(self):
        """Return and reset the flag."""
        with self._lock:
            if self.flagged:
                self.flagged = False
                return 1
            return 0


# ─── Main Recorder ───────────────────────────────────────────────────

def run_experiment(output_dir, session_name=None):
    """Main experiment loop."""

    # Output path
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if session_name is None:
        session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    csv_path = output_dir / f"{session_name}.csv"
    print(f"T-020 EEG Experiment Runner")
    print(f"{'='*60}")
    print(f"  Output: {csv_path}")
    print(f"  Sampling rate: {SAMPLING_RATE} Hz")
    print(f"  Insight trigger: {'SPACEBAR (hold left hand ready)' if KEYBOARD_AVAILABLE else 'NOT AVAILABLE — keyboard not installed'}")
    print(f"  CSD window: {CSD_WINDOW_SEC}s")
    print(f"  Baseline window: {BASELINE_WINDOW_SEC}s")
    print(f"{'='*60}")

    # Connect to Muse
    print("\nConnecting to Muse...")
    try:
        params = BrainFlowInputParams()
        board = BoardShim(BoardIds.MUSE_2_BOARD, params)
        board.prepare_session()
        board.start_stream(450000)  # buffer 450k samples (~30 min)
        print("  ✅ Muse connected and streaming")
    except Exception as e:
        print(f"  ❌ Connection failed: {e}")
        print("  Make sure Muse is powered on and paired via Bluetooth")
        return

    # Set up channels
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.MUSE_2_BOARD)
    actual_sr = BoardShim.get_sampling_rate(BoardIds.MUSE_2_BOARD)
    print(f"  Actual sampling rate: {actual_sr} Hz")

    # Set up CSD tracker
    tracker = CSDTracker(actual_sr)

    # Set up insight trigger
    trigger = InsightTrigger()

    # Set up keyboard listener
    if KEYBOARD_AVAILABLE:
        keyboard.on_press_key("space", lambda _: trigger.mark())
        print("  ⌨️  SPACEBAR listener active — press space when you have an insight")

    # Open CSV for writing
    csv_file = open(csv_path, 'w', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
    writer.writeheader()

    # State
    start_time = time.time()
    last_save = start_time
    sample_count = 0
    running = True

    print(f"\n🔴 RECORDING — solve problems, press SPACEBAR on insight moments")
    print(f"   Ctrl+C to stop\n")

    try:
        while running:
            try:
                data = board.get_board_data(actual_sr)  # 1 second of data
            except Exception:
                time.sleep(0.01)
                continue

            if data.shape[1] < 1:
                time.sleep(0.01)
                continue

            # Process each sample
            num_samples = data.shape[1]
            for i in range(num_samples):
                elapsed = time.time() - start_time
                timestamp = time.time()

                # Extract band powers for this sample
                bands = {}
                try:
                    # Get single-sample band powers via average of buffer
                    if i >= actual_sr - 1:
                        # Use last 1 second for band power calculation
                        chunk = data[:, max(0, i - actual_sr + 1):i + 1]
                        band_result = DataFilter.get_avg_band_powers(
                            chunk, eeg_channels[:4], actual_sr, True
                        )
                        if len(band_result) >= 2 and len(band_result[0]) >= 5:
                            for j, name in enumerate(BAND_NAMES):
                                bands[name] = float(band_result[0][j])
                except Exception:
                    pass

                # Fallback if band powers couldn't be computed
                for name in BAND_NAMES:
                    if name not in bands:
                        bands[name] = 0.0

                # Update CSD tracker
                csd = tracker.update(bands['alpha'], bands['gamma'])

                # Consume insight flag
                insight = trigger.consume()

                # Write row
                row = {
                    'timestamp': timestamp,
                    'elapsed_sec': round(elapsed, 3),
                    'delta': round(bands['delta'], 6),
                    'theta': round(bands['theta'], 6),
                    'alpha': round(bands['alpha'], 6),
                    'beta': round(bands['beta'], 6),
                    'gamma': round(bands['gamma'], 6),
                    'alpha_variance': round(csd['alpha_variance'], 6),
                    'gamma_variance': round(csd['gamma_variance'], 6),
                    'alpha_vs_baseline': round(csd['alpha_vs_baseline'], 4),
                    'gamma_vs_baseline': round(csd['gamma_vs_baseline'], 4),
                    'csd_signal': round(csd['csd_signal'], 6),
                    'insight_flag': insight,
                }
                writer.writerow(row)
                sample_count += 1

            # Periodic status
            now = time.time()
            if now - last_save >= SAVE_INTERVAL_SEC:
                csv_file.flush()
                last_save = now

                mins = elapsed / 60 if (elapsed := now - start_time) else 0
                events = trigger.event_count
                print(f"  [{mins:.1f}min] {sample_count} samples | "
                      f"α_var={csd['alpha_variance']:.4f} | "
                      f"csd={csd['csd_signal']:.4f} | "
                      f"insights: {events}", end='\r')

            # Small sleep to avoid busy-wait
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    finally:
        # Cleanup
        try:
            board.stop_stream()
            board.release_session()
        except Exception:
            pass

        csv_file.close()

        elapsed_total = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"SESSION COMPLETE")
        print(f"  File: {csv_path}")
        print(f"  Duration: {elapsed_total/60:.1f} minutes")
        print(f"  Samples: {sample_count}")
        print(f"  Insight events: {trigger.event_count}")
        print(f"{'='*60}")

        if trigger.event_count == 0:
            print("\n⚠️  No insight events recorded. For T-020 you need ≥10 events.")
            print("   Press SPACEBAR immediately when you feel an 'Aha!' moment.")
        elif trigger.event_count < 10:
            print(f"\n⚠️  Only {trigger.event_count}/10 events. Keep recording sessions.")
        else:
            print(f"\n✅ {trigger.event_count} events — ready for analysis!")

        print(f"\nTo analyze: python3.12 {Path(__file__).parent.parent}/Fundamentals/sandbox/analyze_real_eeg.py '{csv_path}'")


# ─── Entry Point ─────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='T-020 EEG Experiment Runner')
    parser.add_argument('--output', '-o',
                        default='/mnt/d/P1/data/csd_sessions',
                        help='Output directory for session CSVs')
    parser.add_argument('--session-name', '-n',
                        default=None,
                        help='Session name (default: auto-timestamped)')
    args = parser.parse_args()

    run_experiment(args.output, args.session_name)
