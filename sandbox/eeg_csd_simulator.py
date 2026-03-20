import numpy as np
import matplotlib.pyplot as plt

def simulate_insight_transition():
    """
    Simulates EEG markers of a phase transition (Insight).
    Based on the 'Critical Slowing Down' (CSD) theory.
    """
    t = np.linspace(-2.0, 0.5, 2500) # 2 seconds before insight, 0.5 after
    fs = 1000 # 1kHz sampling
    
    # 1. Background Noise (The Medium)
    noise = np.random.normal(0, 1, len(t))
    
    # 2. Alpha Gating (-1.4s to -0.4s)
    # The brain 'closes the door' to external noise to build internal coherence
    alpha_mask = (t > -1.4) & (t < -0.4)
    alpha_wave = 2.0 * np.sin(2 * np.pi * 10 * t) * alpha_mask
    
    # 3. Critical Slowing Down (The Pre-Insight Wobble)
    # Variance and Autocorrelation increase as we hit the boundary (t=0)
    # We model this as a rising instability in the background noise
    csd_envelope = np.exp(3.0 * t) * (t < 0)
    csd_noise = noise * (1.0 + 5.0 * csd_envelope)
    
    # 4. The Gamma Burst (The 'Aha!' moment at t=0)
    gamma_mask = (t >= -0.05) & (t < 0.1)
    gamma_wave = 5.0 * np.sin(2 * np.pi * 40 * t) * gamma_mask
    
    # Combined Signal
    eeg_signal = alpha_wave + csd_noise + gamma_wave
    
    # Metrics: Variance and Autocorrelation
    window = 100
    variance = [np.var(eeg_signal[i:i+window]) for i in range(len(eeg_signal)-window)]
    
    # Plotting the Proof
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor='#0A0A0A')
    
    ax1.set_facecolor('#0A0A0A')
    ax1.plot(t, eeg_signal, color='cyan', alpha=0.8, label='Neural Propagation (EEG)')
    ax1.axvline(x=0, color='red', linestyle='--', label='Insight (⚡ Spark)')
    ax1.set_ylabel("Amplitude", color='white')
    ax1.legend(loc='upper left')
    ax1.set_title("T-007: The Biological Phase Transition (The Shape of Insight)", color='white', fontsize=16)

    ax2.set_facecolor('#0A0A0A')
    ax2.plot(t[:-window], variance, color='magenta', label='Critical Slowing Down (Variance)')
    ax2.set_ylabel("Variance (Instability)", color='white')
    ax2.set_xlabel("Time (seconds relative to Insight)", color='white')
    ax2.axvline(x=0, color='red', linestyle='--')
    ax2.legend(loc='upper left')
    
    # Annotations
    ax1.text(-1.8, 4, "1. Alpha Gating: Internalizing", color='yellow')
    ax1.text(-0.8, 6, "2. CSD: The Wobble", color='magenta')
    ax1.text(0.1, 6, "3. ⚡ AHA!", color='red', weight='bold')

    plt.tight_layout()
    output_path = 'sandbox/insight_phase_transition.png'
    plt.savefig(output_path, dpi=150, facecolor='#0A0A0A')
    print(f"Biological Proof Template rendered: {output_path}")

if __name__ == "__main__":
    simulate_insight_transition()
