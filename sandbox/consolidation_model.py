import numpy as np
import matplotlib.pyplot as plt

def simulate_consolidation(wake_ratio, total_steps=3000, N=1000):
    """
    Final T-010 Model: Implements Axiom 3 Stability Criterion.
    """
    wake_steps = int(total_steps * wake_ratio)
    sleep_steps = total_steps - wake_steps
    
    # Topological Weights from T-002
    # The 2:1 ratio is the core 'impedance' of the system.
    w_enc = 2.0  # Encoding cost
    w_cons = 1.0 # Consolidation capacity
    
    info_gain = 0.0
    noise = 0.0
    
    # 1. Wake Phase (Encoding)
    for _ in range(wake_steps):
        info_gain += 1.0
        noise += (w_enc / N) # Accumulate phase lag
        
    # 2. Sleep Phase (Consolidation)
    # This represents the 'Return to Identity' (4pi -> 2pi)
    for _ in range(sleep_steps):
        # Consolidation is linear but capped by total time
        noise = max(0, noise - (w_cons / N))
        
    # 3. Axiom 3: Stability Check
    # Final structure is only stable if noise is reduced below a critical threshold.
    # We model this as a coherence function: C = exp(-noise^2)
    coherence = np.exp(-(noise * 5.0)**2)
    
    # Effective IQ = Total Info * Coherence
    return info_gain * coherence

def run_t010_model():
    print("--- T-010: Optimal Consolidation Ratio Model (Axiom 3 Final) ---")
    
    ratios = np.linspace(0.01, 0.99, 200)
    final_scores = []
    
    for r in ratios:
        score = simulate_consolidation(r)
        final_scores.append(score)
        
    optimal_ratio = ratios[np.argmax(final_scores)]
    
    print(f"Optimal Wake Ratio: {optimal_ratio:.4f}")
    print(f"Theoretical Target (2/3): 0.6667")
    print(f"Error: {abs(optimal_ratio - 0.6667) / 0.6667:.4%}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(ratios, final_scores, label='System Stability (Integrated Coherence)')
    plt.axvline(x=0.6667, color='r', linestyle='--', label='PF Prediction (2/3)')
    plt.xlabel('Wake Ratio (Encoding Time)')
    plt.ylabel('Stable Information Mass')
    plt.title('T-010: Universal Ratio of Encoding to Consolidation')
    plt.legend()
    plt.grid(True)
    plt.savefig('sandbox/consolidation_axiom3_final.png')
    print("Final plot saved to sandbox/consolidation_axiom3_final.png")

if __name__ == "__main__":
    run_t010_model()
