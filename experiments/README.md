# T-020 EEG Experiment — Critical Slowing Down Before Insight

## Protocol
- **Pre-registered:** `/mnt/d/Fundamentals/protocols/muse_insight_protocol.md`
- **Hypothesis:** Genuine cognitive insight produces Critical Slowing Down (variance spike >50% in 5s pre-insight window)
- **Falsification:** <7/10 insight events show CSD → framework scope restricted to quantum vacuum
- **Threshold:** >50% variance increase, ≥7/10 hit rate

## Quick Start

### 1. Connect Muse
- Power on Muse headband, pair via Bluetooth
- Verify BrainFlow sees it: `python -c "from brainflow.board_shim import BoardShim, BoardIds; b=BoardShim(BoardIds.MUSE_2_BOARD, __import__('brainflow.board_shim', fromlist=['BrainFlowInputParams']).BrainFlowInputParams()); b.prepare_session(); print('OK'); b.release_session()"`

### 2. Run Experiment
```bash
# Start recording — press SPACEBAR on insight moments
python3.12 /mnt/d/Fundamentals/experiments/t020_eeg_runner.py

# With custom output dir
python3.12 /mnt/d/Fundamentals/experiments/t020_eeg_runner.py -o /mnt/d/P1/data/csd_sessions
```

**During recording:**
- Solve problems (math derivation, spatial puzzle, coding architecture)
- When you feel a genuine "Aha!" moment → press SPACEBAR
- Continue recording for a few seconds after the insight
- Run multiple sessions until ≥10 insight events collected

### 3. Analyze Results
```bash
# Analyze one session
python3.12 /mnt/d/Fundamentals/experiments/t020_analyze.py /mnt/d/P1/data/csd_sessions/session_YYYYMMDD_HHMMSS.csv

# Analyze all sessions
python3.12 /mnt/d/Fundamentals/experiments/t020_analyze.py --all
```

## Files
| File | Purpose |
|------|---------|
| `t020_eeg_runner.py` | Records EEG + insight triggers → CSV |
| `t020_analyze.py` | Evaluates CSD against pre-registered threshold |
| `../protocols/muse_insight_protocol.md` | Full protocol with sign-off |

## Dependencies
```bash
# Install in whatever Python you use to run (Windows PowerShell recommended — needs Bluetooth)
pip install brainflow numpy keyboard
```

**Note:** Run from Windows PowerShell (not WSL) — BrainFlow needs Bluetooth access for Muse connection.
The scripts are in `/mnt/d/Fundamentals/experiments/` but execute from `D:\Fundamentals\experiments\` on the Windows side.
