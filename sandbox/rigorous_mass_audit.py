import numpy as np
import itertools

def run_rigorous_audit():
    # 1. PDG 2024 Data with Uncertainty (MeV)
    mass_data = {
        "electron": (0.51099, 0.00001),
        "muon": (105.658, 0.00001),
        "tau": (1776.86, 0.12),
        "up": (2.16, 0.4),
        "down": (4.67, 0.5),
        "strange": (93.4, 6.0),
        "charm_msbar": (1270, 20),
        "charm_pole": (1670, 70),
        "bottom_msbar": (4180, 30),
        "bottom_pole": (4780, 60),
        "top_pole": (172690, 300)
    }

    # 2. Pre-defined Constant Bucket
    phi = (1 + 5**0.5) / 2
    alpha_inv = 137.036
    base_constants = {
        "phi": phi,
        "pi": np.pi,
        "e": np.e,
        "alpha_inv": alpha_inv,
        "sqrt2": 2**0.5,
        "sqrt3": 3**0.5,
        "sqrt5": 5**0.5
    }
    for i in range(1, 13):
        base_constants[str(i)] = float(i)

    powers = [1, 2, 3, -1, 1/2, 1/3]
    targets = []
    for name, val in base_constants.items():
        for p in powers:
            targets.append((f"{name}^{p:.2f}", val**p))

    # 3. The Monte Carlo Simulation
    N = 100000
    hits = 0
    tolerance = 0.003
    
    claim_hits = {
        "top_pole/tau ~ alpha_inv/sqrt2": 0,
        "charm_msbar/muon ~ 12": 0,
        "charm_pole/muon ~ 5*pi": 0,
        "bottom_pole/tau ~ e": 0,
        "up/electron ~ phi^3": 0
    }

    print(f"--- T-008: Rigorous Monte Carlo Audit (Corrected) ---")
    print(f"N Samples: {N} | Target Tolerance: {tolerance*100}%")

    for _ in range(N):
        sampled = {k: np.random.normal(v[0], v[1]) for k, v in mass_data.items()}
        
        # Test general density
        mass_keys = ["electron", "muon", "tau", "up", "down", "strange", "charm_msbar", "bottom_msbar", "top_pole"]
        for m1, m2 in itertools.permutations(mass_keys, 2):
            ratio = sampled[m1] / sampled[m2]
            for _, t_val in targets:
                if abs(ratio - t_val) / t_val <= tolerance:
                    hits += 1
                    break
        
        # Test specific claims
        if abs((sampled["top_pole"]/sampled["tau"]) - (alpha_inv/2**0.5)) / (alpha_inv/2**0.5) <= tolerance:
            claim_hits["top_pole/tau ~ alpha_inv/sqrt2"] += 1
        if abs((sampled["charm_msbar"]/sampled["muon"]) - 12.0) / 12.0 <= tolerance:
            claim_hits["charm_msbar/muon ~ 12"] += 1
        if abs((sampled["charm_pole"]/sampled["muon"]) - (5*np.pi)) / (5*np.pi) <= tolerance:
            claim_hits["charm_pole/muon ~ 5*pi"] += 1
        if abs((sampled["bottom_pole"]/sampled["tau"]) - np.e) / np.e <= tolerance:
            claim_hits["bottom_pole/tau ~ e"] += 1
        if abs((sampled["up"]/sampled["electron"]) - phi**3) / phi**3 <= tolerance:
            claim_hits["up/electron ~ phi^3"] += 1

    # 4. Statistical Analysis
    total_possible_pair_checks = N * 72
    p_value_general = hits / total_possible_pair_checks
    
    print(f"\nResults:")
    print(f"General Coincidence Probability (p): {p_value_general:.6f}")
    
    print(f"\nSpecific Claim Robustness (Given uncertainty):")
    for claim, count in claim_hits.items():
        print(f" - {claim}: {count/N*100:.2f}% robustness")

    print(f"\n--- LUMI VERDICT ---")
    if p_value_general > 0.05:
        print("STATUS: [NUMEROLOGY] - The space is too noisy.")
    elif p_value_general < 0.01:
        print("STATUS: [SIGNAL] - The spectrum is mathematically constrained.")
    else:
        print("STATUS: [INTRIGUING] - Borderline significance.")

if __name__ == "__main__":
    run_rigorous_audit()
