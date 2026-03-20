import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyze_session(file_path):
    print(f"Loading session data from: {file_path}")
    df = pd.read_csv(file_path)
    
    # Find the insight marker
    insight_idx = df.index[df['insight_flag'] == 1].tolist()
    
    if not insight_idx:
        print("No insight marker (spacebar) found in the data.")
        insight_time = df['elapsed_sec'].iloc[-1]
    else:
        insight_time = df['elapsed_sec'].iloc[insight_idx[-1]]
        print(f"Insight marker found at T = {insight_time:.2f}s")

    # Filter data to a window around the insight (e.g., -30s to +10s)
    window_start = max(0, insight_time - 30)
    window_end = min(df['elapsed_sec'].iloc[-1], insight_time + 10)
    
    mask = (df['elapsed_sec'] >= window_start) & (df['elapsed_sec'] <= window_end)
    df_window = df[mask]
    
    t = df_window['elapsed_sec'] - insight_time  # Relative time to insight
    
    # Plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True, facecolor='#0A0A0A')
    
    # 1. Raw Band Powers
    ax1.set_facecolor('#0A0A0A')
    ax1.plot(t, df_window['theta'], color='#FFCC00', label='Theta (4-8 Hz)', alpha=0.8)
    ax1.plot(t, df_window['alpha'], color='#00FFCC', label='Alpha (8-12 Hz)', alpha=0.8)
    ax1.plot(t, df_window['gamma'], color='#FF3366', label='Gamma (30-44 Hz)', alpha=0.8)
    ax1.axvline(x=0, color='white', linestyle='--', label='Void/Source Mark')
    ax1.set_ylabel("Absolute Power", color='white')
    ax1.legend(loc='upper left', facecolor='#1A1A1A', labelcolor='white')
    ax1.set_title("Live Muse EEG: The 'Void/Source' Transition", color='white', fontsize=14)
    ax1.tick_params(colors='white')

    # 2. Gamma vs Baseline (The Spark?)
    ax2.set_facecolor('#0A0A0A')
    ax2.plot(t, df_window['gamma_vs_baseline'], color='#FF3366', label='Gamma vs Baseline')
    ax2.axvline(x=0, color='white', linestyle='--')
    ax2.set_ylabel("Gamma Ratio", color='white')
    ax2.legend(loc='upper left', facecolor='#1A1A1A', labelcolor='white')
    ax2.tick_params(colors='white')

    # 3. Variance / CSD Signal (The Wobble?)
    ax3.set_facecolor('#0A0A0A')
    ax3.plot(t, df_window['csd_signal'], color='magenta', label='CSD Signal (Variance Indicator)')
    ax3.axvline(x=0, color='white', linestyle='--')
    ax3.set_ylabel("Variance", color='white')
    ax3.set_xlabel("Time (seconds relative to mark)", color='white')
    ax3.legend(loc='upper left', facecolor='#1A1A1A', labelcolor='white')
    ax3.tick_params(colors='white')

    plt.tight_layout()
    output_path = 'D:/Fundamentals/sandbox/real_eeg_analysis.png'
    plt.savefig(output_path, dpi=150, facecolor='#0A0A0A')
    print(f"Analysis plot saved to {output_path}")

if __name__ == "__main__":
    analyze_session('D:/P1/data/csd_sessions/session_20260319_153348.csv')
