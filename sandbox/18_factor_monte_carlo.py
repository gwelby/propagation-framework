import numpy as np

def run_18_factor_audit():
    # 1. Physical Constants (PDG 2024)
    m_e = 0.51099895  # MeV
    alpha_inv = 137.035999  # 1/alpha
    m_t_pole = 172690.0  # MeV (Central)
    m_t_err = 300.0      # MeV

    # 2. The Target Formula
    # m_t = 18 * m_e * alpha_inv^2
    theoretical_mt = 18 * m_e * (alpha_inv**2)
    actual_error = abs(m_t_pole - theoretical_mt) / theoretical_mt

    print(f"--- T-008: The 18-Factor DOF Audit ---")
    print(f"Theoretical m_t (18 * m_e / alpha^2): {theoretical_mt/1000:.3f} GeV")
    print(f"Measured m_t (PDG 2024 Pole): {m_t_pole/1000:.3f} +/- 0.3 GeV")
    print(f"Precision Error: {actual_error:.4%}")

    # 3. Monte Carlo Significance Test
    # How often does m_t / (m_e * alpha_inv^2) land on a "meaningful" integer?
    # Meaningful integers = products of 2, 3, 4 (Symmetry counts)
    meaningful_ints = [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48, 54, 64, 72]
    
    # Generate 100,000 random "Top Masses" in a wide range (50 GeV to 500 GeV)
    # to see how often they hit ANY meaningful integer scaling of m_e/alpha^2.
    N = 100000
    hits = 0
    tolerance = 0.003 # 0.3%
    
    random_masses = np.random.uniform(50000, 500000, N)
    
    for rm in random_masses:
        scaling_factor = rm / (m_e * alpha_inv**2)
        for mi in meaningful_ints:
            if abs(scaling_factor - mi) / mi <= tolerance:
                hits += 1
                break

    p_value = hits / N
    print(f"\nResults:")
    print(f"Chance of hitting a DOF-related integer in mass-space: {p_value:.4%}")

    if p_value < 0.01:
        print("VERDICT: [STRUCTURAL SIGNAL] - The 18-factor coupling is highly significant.")
    else:
        print("VERDICT: [COINCIDENCE] - Small integers are dense enough to cause false hits.")

if __name__ == "__main__":
    run_18_factor_audit()
