import numpy as np

def generate_koide_masses(scale_A, phase_theta0):
    """
    Generates the three masses for a Koide family.
    Enforces the Q=2/3 geometric constraint (R/A = sqrt(2)).
    """
    R = scale_A * np.sqrt(2.0)
    masses = []
    for n in range(3):
        # m_n = (A + R * cos(theta0 + 2*pi*n/3))^2
        angle = phase_theta0 + (2.0 * np.pi * n / 3.0)
        sqrt_m = scale_A + R * np.cos(angle)
        masses.append(sqrt_m**2)
    # Return sorted (lightest to heaviest)
    return sorted(masses)

def top_tau_explorer():
    print("=======================================================")
    print("  EXPERIMENT 2: THE TOP/TAU MECHANISM")
    print("  Scanning Koide phase space for m_t / m_tau coupling")
    print("=======================================================\n")

    # Known empirical values (GeV)
    m_tau_empirical = 1.7768
    m_top_empirical = 172.69
    alpha_inv = 137.035999
    
    # Target relationship: m_t / m_tau = alpha^-1 / sqrt(2)
    target_ratio = alpha_inv / np.sqrt(2.0)
    empirical_ratio = m_top_empirical / m_tau_empirical
    
    print(f"Empirical m_t / m_tau      : {empirical_ratio:.4f}")
    print(f"Target α^-1 / sqrt(2)      : {target_ratio:.4f}")
    print(f"Current Error              : {abs(empirical_ratio - target_ratio) / target_ratio * 100:.3f}%\n")

    print("--- Scanning Koide Geometric Space ---")
    # Let's fix the Lepton scale so the heaviest mass is m_tau
    # And fix the Quark scale so the heaviest mass is m_top
    # We will scan the phase angle θ_0 to see how it affects the ratio
    
    phases_to_test = np.linspace(0, np.pi, 1000)
    
    # We want to find if a specific phase angle naturally produces the 1/sqrt(2) factor
    # independent of the scale A.
    
    # The heaviest mass in a Koide family occurs when cos(...) is maximized.
    # m_max = (A + A*sqrt(2)*cos(theta_max))^2
    # m_max = A^2 * (1 + sqrt(2)*cos(theta_max))^2
    
    print("Analyzing the scale-independent geometry:")
    print("If m_t and m_tau belong to two separate Koide triangles,")
    print("their ratio is (A_q / A_l)^2 * [ (1 + sqrt(2)*cos(θ_q)) / (1 + sqrt(2)*cos(θ_l)) ]^2\n")
    
    print("What if the scale ratio (A_q / A_l)^2 IS EXACTLY α^-1 ?")
    
    # Let's test the hypothesis: The fundamental scale difference between 
    # the quark medium and the lepton medium is exactly alpha^-1.
    scale_ratio_squared = alpha_inv
    
    # Then m_t / m_tau = α^-1 * [Geometry Factor]
    # We need the [Geometry Factor] to be exactly 1/sqrt(2) = 0.7071
    
    print(f"Hypothesis: The scale jump between domains is exactly α^-1 ({alpha_inv:.2f})")
    print(f"We need the Koide Geometry Factor to equal 1/sqrt(2) ≈ 0.7071\n")
    
    # Let's assume the lepton phase is the empirical 2/9
    theta_l = 2.0 / 9.0
    lepton_geo = (1.0 + np.sqrt(2.0) * np.cos(theta_l))**2
    
    best_error = float('inf')
    best_theta_q = 0
    
    for theta_q in phases_to_test:
        quark_geo = (1.0 + np.sqrt(2.0) * np.cos(theta_q))**2
        geo_ratio = quark_geo / lepton_geo
        
        error = abs(geo_ratio - (1.0 / np.sqrt(2.0)))
        if error < best_error:
            best_error = error
            best_theta_q = theta_q
            best_geo = geo_ratio

    print(f"Searching for Quark Phase (θ_q) that satisfies the geometry...")
    print(f"Found optimal Quark Phase : {best_theta_q:.6f} rad")
    print(f"Resulting Geometry Factor : {best_geo:.6f}")
    print(f"Target Geometry Factor    : {1.0 / np.sqrt(2.0):.6f}")
    
    # Is best_theta_q a "nice" fraction of pi?
    fraction = best_theta_q / np.pi
    print(f"Optimal phase as frac of π: {fraction:.5f} π")
    
    if abs(fraction - 0.5) < 0.05:
        print("\n[!] HIGH SIGNAL FOUND: The quark phase wants to be exactly π/2 (90 degrees).")
        print("    If Lepton phase = 2/9, and Quark phase = π/2, the geometry naturally yields the 1/sqrt(2) ratio.")
        
        # Verify
        q_geo_pi_2 = (1.0 + np.sqrt(2.0) * np.cos(np.pi/2))**2  # cos(pi/2) = 0, so this is 1.0
        l_geo_2_9 = (1.0 + np.sqrt(2.0) * np.cos(2.0/9.0))**2
        final_ratio = q_geo_pi_2 / l_geo_2_9
        print(f"\nExact Calculation with θ_q = π/2 and θ_l = 2/9:")
        print(f"Geometry Ratio = {final_ratio:.6f} (Target was 0.7071)")
        print(f"Total Theoretical m_t / m_tau = α^-1 * {final_ratio:.6f} = {alpha_inv * final_ratio:.2f}")
        print(f"Empirical m_t / m_tau       = {empirical_ratio:.2f}")

if __name__ == "__main__":
    top_tau_explorer()