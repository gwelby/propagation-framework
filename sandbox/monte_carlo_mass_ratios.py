import numpy as np
import itertools

def run_monte_carlo():
    # 1. Fundamental Constants (PDG 2024 approximate central values in MeV)
    # Note: Quark masses have high uncertainty, which we will account for.
    masses = {
        "electron": 0.51099,
        "muon": 105.658,
        "tau": 1776.86,
        "up": 2.16,      # PDG: 1.7 - 2.5
        "down": 4.67,    # PDG: 4.1 - 5.4
        "strange": 93.4, # PDG: 92 - 104
        "charm": 1270,   # PDG: 1250 - 1300
        "bottom": 4180,  # PDG: 4150 - 4210
        "top": 172690    # PDG: 172000 - 173000
    }

    # 2. Mathematical Constants
    phi = (1 + 5**0.5) / 2
    math_constants = {
        "phi": phi,
        "pi": np.pi,
        "e": np.e,
        "sqrt2": 2**0.5,
        "sqrt3": 3**0.5
    }

    # 3. Powers to test
    powers = [1, 2, 3, -1, 1/2, 1/3]

    # Generate all "Beautiful Targets"
    targets = []
    for name, val in math_constants.items():
        for p in powers:
            target_val = val**p
            targets.append((f"{name}^{p:.2f}", target_val))

    # 4. Generate all possible mass ratios
    ratio_hits = []
    mass_keys = list(masses.keys())
    
    print(f"--- T-008: Monte Carlo Mass Ratio Audit ---")
    print(f"Target: m_u / m_e ≈ phi^3 (Error threshold: 0.25%)")
    
    # Calculate the actual target coincidence
    target_ratio = masses["up"] / masses["electron"]
    phi3 = phi**3
    actual_error = abs(target_ratio - phi3) / phi3
    print(f"Actual m_u / m_e: {target_ratio:.4f}")
    print(f"Target phi^3: {phi3:.4f}")
    print(f"Initial Error: {actual_error:.4%}")

    # 5. The Simulation: Randomized Search Space
    # How many ways can we combine these masses to hit ANY beautiful target?
    total_combinations = 0
    hits = 0
    tolerance = 0.0025 # 0.25%

    for m1, m2 in itertools.permutations(mass_keys, 2):
        ratio = masses[m1] / masses[m2]
        total_combinations += 1
        
        for t_name, t_val in targets:
            error = abs(ratio - t_val) / t_val
            if error <= tolerance:
                hits += 1
                ratio_hits.append((f"{m1}/{m2}", t_name, error))

    # 6. Statistical Significance (Rough p-value)
    # p = (Total hits) / (Total possible ratios * total possible targets)
    p_value = hits / (total_combinations * len(targets))
    
    print(f"\nAudit Results:")
    print(f"Total ratios tested: {total_combinations}")
    print(f"Total targets tested: {len(targets)}")
    print(f"Total 'Beautiful Hits' found: {hits}")
    print(f"Coincidence Density (p-value): {p_value:.6f}")
    
    if p_value > 0.05:
        print(f"VERDICT: [NUMEROLOGY] - Hits are common in this dense space.")
    elif p_value > 0.01:
        print(f"VERDICT: [INTRIGUING] - Coincidence is relatively rare.")
    else:
        print(f"VERDICT: [SIGNAL] - This is a mathematically significant anomaly.")

    print(f"\nTop 5 Coincidences Found:")
    ratio_hits.sort(key=lambda x: x[2])
    for r, t, err in ratio_hits[:5]:
        print(f" - {r} ≈ {t} (Error: {err:.4%})")

if __name__ == "__main__":
    run_monte_carlo()
