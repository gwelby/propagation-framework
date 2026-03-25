import numpy as np

def scan_koide_phase():
    print("=======================================================")
    print("  EXPERIMENT 3: THE KOIDE PHASE HUNTER")
    print("  Scanning for the geometric meaning of δ_0 ≈ 2/9")
    print("=======================================================\n")

    # Rivero's empirical phase for charged leptons
    target_phase = 2.0 / 9.0
    print(f"Target Phase (δ_0) : {target_phase:.6f} rad")
    
    # We will scan the fundamental phase domain [0, 2pi/3]
    # because the generations are spaced by 2pi/3 (120 degrees)
    phases = np.linspace(0, 2 * np.pi / 3, 50000)
    
    # R/A = sqrt(2) is fixed by the Q=2/3 derivation
    sqrt2 = np.sqrt(2.0)
    
    # We want to find a functional F(phase) that is MINIMIZED at 2/9.
    # What does the medium "cost"? 
    # A mode with mass m has frequency proportional to m.
    # Total energy cost E_total ~ sum(m_n)
    # Total action cost A_total ~ sum(sqrt(m_n))
    # Let's calculate several geometric properties of the Koide triangle at each phase.
    
    # Arrays to store costs
    cost_variance = np.zeros_like(phases)
    cost_max_mass = np.zeros_like(phases)
    cost_min_mass = np.zeros_like(phases)
    cost_complexity = np.zeros_like(phases)
    
    best_phase_complexity = 0
    min_complexity = float('inf')

    for i, p in enumerate(phases):
        # The three roots (sqrt(mass) / A)
        r0 = 1.0 + sqrt2 * np.cos(p)
        r1 = 1.0 + sqrt2 * np.cos(p + 2*np.pi/3)
        r2 = 1.0 + sqrt2 * np.cos(p + 4*np.pi/3)
        
        # The three masses (normalized by A^2)
        m0, m1, m2 = r0**2, r1**2, r2**2
        
        cost_variance[i] = np.var([m0, m1, m2])
        cost_max_mass[i] = max(m0, m1, m2)
        cost_min_mass[i] = min(m0, m1, m2)
        
        # "Complexity Cost": The medium must maintain all three resonant frequencies simultaneously.
        # If the masses are vastly different, the required bandwidth is huge.
        # If one mass approaches zero, it becomes a long-range Goldstone-like mode, requiring infinite spatial coherence.
        # Let's define a cost function that penalizes both extreme mass hierarchies and near-zero masses.
        # Cost = Max_Mass / Min_Mass (Condition Number of the Mass Matrix)
        # To avoid divide by zero, we add a tiny epsilon
        cost_comp = max(m0, m1, m2) / (min(m0, m1, m2) + 1e-10)
        cost_complexity[i] = cost_comp
        
        if cost_comp < min_complexity:
            min_complexity = cost_comp
            best_phase_complexity = p

    print("\n--- Scanning Results ---")
    
    print("1. Minimum Variance (Most degenerate state):")
    idx_var = np.argmin(cost_variance)
    print(f"   Phase: {phases[idx_var]:.6f} rad")
    
    print("2. Maximum Hierarchy (Largest Top Mass):")
    idx_max = np.argmax(cost_max_mass)
    print(f"   Phase: {phases[idx_max]:.6f} rad")
    
    print("3. Minimum Complexity (Minimum Condition Number Max/Min):")
    print(f"   Phase: {best_phase_complexity:.6f} rad")
    
    # Check if the target phase (2/9) corresponds to any mathematical "golden" angle
    # 2/9 is exactly 0.2222... 
    
    # Is there a trigonometric identity near 2/9?
    # cos(2/9) = 0.9754
    # Let's check the derivative of the masses at 2/9
    target_idx = np.argmin(np.abs(phases - target_phase))
    
    print(f"\n--- Analyzing the Target Phase ({target_phase:.6f}) ---")
    m0_t = (1.0 + sqrt2 * np.cos(target_phase))**2
    m1_t = (1.0 + sqrt2 * np.cos(target_phase + 2*np.pi/3))**2
    m2_t = (1.0 + sqrt2 * np.cos(target_phase + 4*np.pi/3))**2
    
    print(f"Normalized Masses at 2/9 : {m0_t:.4f}, {m1_t:.4f}, {m2_t:.4f}")
    
    # Let's check the ratio of the two heaviest masses at 2/9
    sorted_m_t = sorted([m0_t, m1_t, m2_t])
    ratio_2_1 = sorted_m_t[2] / sorted_m_t[1]
    ratio_1_0 = sorted_m_t[1] / sorted_m_t[0]
    
    print(f"Ratio M_heavy / M_mid    : {ratio_2_1:.4f}")
    print(f"Ratio M_mid / M_light    : {ratio_1_0:.4f}")
    
    # Wait, the empirical tau/mu ratio is about 1776 / 105 = 16.9
    # The mu/e ratio is about 105 / 0.511 = 205
    print("\nThe 2/9 phase does not seem to minimize a simple geometric scalar like Variance or Max/Min.")
    print("If it is derived, it likely comes from a dynamic interaction with the other particle sectors.")

if __name__ == "__main__":
    scan_koide_phase()