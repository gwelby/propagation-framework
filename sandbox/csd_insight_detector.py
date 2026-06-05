#!/usr/bin/env python3
"""
CSD Insight Detector — T-007 Production Pipeline
=====================================================
Critical Slowing Down detector for Muse EEG insight experiments.
Implements the pre-registered protocol from:
  /mnt/d/Fundamentals/protocols/muse_insight_protocol.md

Usage modes:
  1. LIVE:  Stream from Muse OSC (python-osc required)
  2. BATCH: Process a recorded CSV of EEG + event timestamps

Pre-registered criteria (HONEST — locked before data collection):
  - Baseline window: 30 seconds of "Search" phase
  - Pre-event window: 5 seconds immediately before insight trigger
  - Success threshold: variance increase > 50% in pre-event window
  - Pass criterion: >= 7 out of 10 insight events show CSD signature

If < 7/10: the cross-scale phase-transition claim is falsified for brains.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Tuple

import numpy as np

# ─── Configuration ──────────────────────────────────────────────────

BASELINE_SEC: float = 30.0       # "Search" phase window
PRE_EVENT_SEC: float = 5.0      # Window before insight trigger
SUCCESS_RATIO: float = 0.50    # Variance must increase by > 50%
PASS_THRESHOLD: int = 7        # Need >= 7 out of 10 events
MUSE_SF: float = 256.0          # Muse sampling frequency (Hz)

# ─── Data structures ────────────────────────────────────────────────

@dataclass
class InsightEvent:
    """One insight event with baseline + pre-event windows."""
    event_id: int
    timestamp: float              # Seconds since start
    baseline: np.ndarray          # Shape: (n_baseline_samples, 4)
    pre_event: np.ndarray         # Shape: (n_pre_samples, 4)

@dataclass
class CSDResult:
    """Result for a single event."""
    event_id: int
    baseline_var: float           # Mean variance across 4 channels
    pre_event_var: float
    variance_ratio: float         # pre / baseline
    autocorr_trend: float         # Kendall tau for lag-1 autocorrelation
    csd_detected: bool            # variance_ratio > 1 + SUCCESS_RATIO

@dataclass
class SessionReport:
    """Full session results."""
    n_events: int
    n_csd_detected: int
    n_partial: int                # variance increases but < 50%
    n_none: int
    pass_pre_registered: bool     # n_csd_detected >= PASS_THRESHOLD
    events: List[CSDResult] = field(default_factory=list)

# ─── Core CSD analysis ────────────────────────────────────────────

def compute_variance(eeg_window: np.ndarray) -> float:
    """Mean variance across 4 EEG channels."""
    return float(np.mean(np.var(eeg_window, axis=0)))

def compute_autocorr_trend(eeg_window: np.ndarray) -> float:
    """
    Compute Kendall tau trend in lag-1 autocorrelation.
    Returns tau (positive = increasing autocorr = CSD signature).
    """
    from scipy import stats
    # Use first channel (AF7) as primary — could extend to multi-channel
    signal = eeg_window[:, 0]
    # Sliding window autocorrelation
    window_len = min(64, len(signal) // 4)
    if window_len < 8:
        return 0.0
    acs = []
    for i in range(0, len(signal) - window_len, window_len // 2):
        w = signal[i : i + window_len]
        w = w - np.mean(w)
        if np.std(w) < 1e-12:
            acs.append(0.0)
            continue
        acs.append(np.corrcoef(w[:-1], w[1:])[0, 1])
    if len(acs) < 3:
        return 0.0
    x = np.arange(len(acs))
    tau, _ = stats.kendalltau(x, acs)
    return float(tau)

def analyze_event(evt: InsightEvent) -> CSDResult:
    """Run CSD analysis on one insight event."""
    bvar = compute_variance(evt.baseline)
    pvar = compute_variance(evt.pre_event)
    ratio = pvar / bvar if bvar > 1e-12 else 1.0
    autocorr_tau = compute_autocorr_trend(evt.pre_event)

    return CSDResult(
        event_id=evt.event_id,
        baseline_var=bvar,
        pre_event_var=pvar,
        variance_ratio=ratio,
        autocorr_trend=autocorr_tau,
        csd_detected=ratio > (1.0 + SUCCESS_RATIO),
    )

def build_report(results: List[CSDResult]) -> SessionReport:
    """Aggregate session results."""
    n_csd = sum(1 for r in results if r.csd_detected)
    n_partial = sum(
        1 for r in results
        if not r.csd_detected and r.variance_ratio > 1.0
    )
    n_none = len(results) - n_csd - n_partial
    return SessionReport(
        n_events=len(results),
        n_csd_detected=n_csd,
        n_partial=n_partial,
        n_none=n_none,
        pass_pre_registered=(n_csd >= PASS_THRESHOLD),
        events=results,
    )

# ─── I/O: CSV batch mode ──────────────────────────────────────────

def load_csv_eeg(path: Path) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load EEG CSV. Expected columns:
      timestamp, tp9, af7, af8, tp10 [, event_flag]
    Returns (samples, events) where events is array of (index, timestamp).
    """
    timestamps: List[float] = []
    samples: List[List[float]] = []
    event_indices: List[int] = []
    event_timestamps: List[float] = []

    with path.open("r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        # Detect if there's an event_flag column
        has_event = header is not None and "event" in [h.lower() for h in header]
        if header is None:
            f.seek(0)
            reader = csv.reader(f)

        for i, row in enumerate(reader):
            if not row:
                continue
            try:
                ts = float(row[0])
                chans = [float(c) for c in row[1:5]]
                timestamps.append(ts)
                samples.append(chans)
                if has_event and len(row) > 5 and int(row[5]) == 1:
                    event_indices.append(i)
                    event_timestamps.append(ts)
            except (ValueError, IndexError):
                continue

    data = np.array(samples, dtype=np.float64)
    events = np.array(list(zip(event_indices, event_timestamps)), dtype=np.float64)
    return data, events

def extract_windows(
    data: np.ndarray,
    timestamps: np.ndarray,
    event_idx: int,
    sf: float = MUSE_SF,
) -> InsightEvent:
    """Extract baseline and pre-event windows around one event."""
    baseline_samples = int(BASELINE_SEC * sf)
    pre_samples = int(PRE_EVENT_SEC * sf)

    start_baseline = max(0, event_idx - baseline_samples - pre_samples)
    end_baseline = max(0, event_idx - pre_samples)
    start_pre = end_baseline
    end_pre = event_idx

    return InsightEvent(
        event_id=event_idx,
        timestamp=timestamps[event_idx],
        baseline=data[start_baseline:end_baseline],
        pre_event=data[start_pre:end_pre],
    )

def run_batch(csv_path: Path) -> SessionReport:
    """Run full batch analysis on a recorded EEG CSV."""
    data, events = load_csv_eeg(csv_path)
    if len(events) == 0:
        print("ERROR: No event flags found in CSV.")
        print("  Expected columns: timestamp, tp9, af7, af8, tp10, event_flag")
        sys.exit(1)

    # Build timestamps assuming uniform sampling
    timestamps = np.arange(len(data)) / MUSE_SF

    results: List[CSDResult] = []
    for evt_idx, evt_ts in events:
        evt = extract_windows(data, timestamps, int(evt_idx))
        if len(evt.baseline) < 10 or len(evt.pre_event) < 10:
            print(f"  Skipping event {int(evt_idx)}: insufficient data")
            continue
        results.append(analyze_event(evt))

    return build_report(results)

# ─── I/O: Live OSC mode ─────────────────────────────────────────────

class LiveCSDCollector:
    """
    Collects live EEG from Muse OSC and buffers for CSD analysis.
    Designed to run alongside problem-solving sessions.
    """

    def __init__(self, sf: float = MUSE_SF):
        self.sf = sf
        self.buffer: List[Tuple[float, List[float]]] = []  # (timestamp, [4 chans])
        self.events: List[Tuple[float, int]] = []          # (timestamp, event_id)
        self._running = False
        self._event_counter = 0

    def add_sample(self, timestamp: float, channels: List[float]) -> None:
        self.buffer.append((timestamp, channels))
        # Keep only last ~60 seconds to prevent unbounded growth
        cutoff = timestamp - (BASELINE_SEC + PRE_EVENT_SEC + 5.0)
        while self.buffer and self.buffer[0][0] < cutoff:
            self.buffer.pop(0)

    def trigger_event(self, timestamp: Optional[float] = None) -> int:
        """Call this when the subject hits the insight trigger (Spacebar)."""
        self._event_counter += 1
        ts = timestamp if timestamp is not None else time.time()
        self.events.append((ts, self._event_counter))
        print(f"  [EVENT {self._event_counter}] Insight trigger at t={ts:.3f}")
        return self._event_counter

    def analyze_all(self) -> SessionReport:
        """Analyze all recorded events after session ends."""
        if not self.buffer:
            print("ERROR: No EEG data collected.")
            sys.exit(1)

        # Reconstruct uniform array from buffer
        times = np.array([b[0] for b in self.buffer])
        data = np.array([b[1] for b in self.buffer])
        dt = np.median(np.diff(times))
        sf_est = 1.0 / dt if dt > 0 else self.sf

        results: List[CSDResult] = []
        for evt_ts, evt_id in self.events:
            # Find closest index
            idx = int(np.argmin(np.abs(times - evt_ts)))
            evt = extract_windows(data, times, idx, sf=sf_est)
            if len(evt.baseline) < 10 or len(evt.pre_event) < 10:
                print(f"  Skipping event {evt_id}: insufficient data")
                continue
            results.append(analyze_event(evt))

        return build_report(results)

def run_live(port: int = 5000) -> None:
    """Run live OSC collection. Requires python-osc."""
    try:
        from pythonosc import dispatcher, osc_server
    except ImportError:
        print("ERROR: python-osc not installed.")
        print("  pip install python-osc")
        sys.exit(1)

    collector = LiveCSDCollector()

    def on_eeg(address: str, *args) -> None:
        if len(args) >= 4:
            collector.add_sample(time.time(), list(args[:4]))

    disp = dispatcher.Dispatcher()
    disp.map("/muse/eeg", on_eeg)

    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", port), disp)
    print(f"Listening for Muse OSC on port {port}...")
    print("Commands:")
    print("  [SPACE] or 'e' + Enter → log insight event")
    print("  'q' + Enter → quit and analyze")

    import threading
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        while True:
            cmd = input().strip().lower()
            if cmd == "q":
                break
            elif cmd == "e" or cmd == "":
                collector.trigger_event()
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        server.shutdown()

    print(f"\nCollected {len(collector.events)} events.")
    report = collector.analyze_all()
    return report

# ─── Reporting ──────────────────────────────────────────────────────

def print_report(report: SessionReport) -> None:
    """Pretty-print session report."""
    print("\n" + "=" * 60)
    print("  T-007 CSD INSIGHT DETECTOR — SESSION REPORT")
    print("=" * 60)
    print(f"  Total insight events:      {report.n_events}")
    print(f"  Strong CSD (var > +50%):   {report.n_csd_detected}")
    print(f"  Partial CSD (var up, <50%): {report.n_partial}")
    print(f"  No CSD signal:             {report.n_none}")
    print()
    print("  Pre-registered pass criterion: >= 7/10 with >50% variance increase")
    print(f"  RESULT: {'✅ PASS' if report.pass_pre_registered else '❌ FAIL'}")
    print()
    if not report.pass_pre_registered:
        print("  INTERPRETATION (pre-registered, locked before data):")
        print("    If < 7/10, the cross-scale phase-transition claim is")
        print("    falsified for biological neural networks.")
        print("    The framework's scope is restricted to the quantum vacuum.")
    print()
    print("  Per-event breakdown:")
    print(f"  {'ID':>4} {'Baseline Var':>12} {'Pre-Event Var':>13} {'Ratio':>8} {'Auto τ':>8} {'CSD?':>5}")
    print("  " + "-" * 58)
    for r in report.events:
        flag = "YES" if r.csd_detected else ("partial" if r.variance_ratio > 1.0 else "no")
        print(
            f"  {r.event_id:>4} {r.baseline_var:>12.2f} {r.pre_event_var:>13.2f}"
            f" {r.variance_ratio:>8.2f} {r.autocorr_trend:>8.3f} {flag:>5}"
        )
    print("=" * 60 + "\n")

def save_json_report(report: SessionReport, path: Path) -> None:
    """Save machine-readable report."""
    payload = {
        "t007_version": "1.0.0",
        "pre_registered": True,
        "baseline_sec": BASELINE_SEC,
        "pre_event_sec": PRE_EVENT_SEC,
        "success_ratio": SUCCESS_RATIO,
        "pass_threshold": PASS_THRESHOLD,
        "n_events": report.n_events,
        "n_csd_detected": report.n_csd_detected,
        "n_partial": report.n_partial,
        "n_none": report.n_none,
        "pass_pre_registered": report.pass_pre_registered,
        "events": [
            {
                "event_id": r.event_id,
                "baseline_var": r.baseline_var,
                "pre_event_var": r.pre_event_var,
                "variance_ratio": r.variance_ratio,
                "autocorr_trend": r.autocorr_trend,
                "csd_detected": r.csd_detected,
            }
            for r in report.events
        ],
    }
    path.write_text(json.dumps(payload, indent=2))
    print(f"JSON report saved: {path}")

# ─── Main ───────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="T-007 CSD Insight Detector — prove phase transitions in the brain"
    )
    parser.add_argument(
        "--mode",
        choices=["batch", "live"],
        default="batch",
        help="batch = process recorded CSV; live = stream from Muse OSC",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="CSV file for batch mode (timestamp, tp9, af7, af8, tp10, [event_flag])",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="OSC listen port for live mode (default: 5000)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("csd_report.json"),
        help="JSON output path (default: csd_report.json)",
    )
    args = parser.parse_args()

    if args.mode == "batch":
        if args.input is None:
            print("ERROR: --input CSV required for batch mode.")
            sys.exit(1)
        if not args.input.exists():
            print(f"ERROR: File not found: {args.input}")
            sys.exit(1)
        report = run_batch(args.input)
    else:
        report = run_live(args.port)

    print_report(report)
    save_json_report(report, args.output)

    # Exit code signals result for CI/automation
    sys.exit(0 if report.pass_pre_registered else 2)

if __name__ == "__main__":
    main()
