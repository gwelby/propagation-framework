import numpy as np

def run_gen2_audit():
    # 1. Fundamental Constants (PDG 2024 central values)
    masses = {
        "electron": 0.511,
        "up": 2.16,
        "muon": 105.66,
        "strange": 93.4,
        "charm": 1270,
        "tau": 1776.8,
        "bottom": 4180,
        "top": 172690
    }

    # 2. Ratios to test
    ratios = {
        "up/electron": masses["up"] / masses["electron"],
        "strange/muon": masses["strange"] / masses["muon"],
        "charm/muon": masses["charm"] / masses["muon"],
        "bottom/tau": masses["bottom"] / masses["tau"],
        "top/tau": masses["top"] / masses["tau"]
    }

    # 3. Geometric / Harmonic Targets
    phi = (1 + 5**0.5) / 2
    targets = {
        "phi^3": phi**3,
        "phi^5": phi**5,
        "sqrt(phi)": phi**0.5,
        "12": 12.0,
        "24": 24.0,
        "pi^2": np.pi**2,
        "e^pi": np.exp(np.pi),
        "sqrt(3)/2": 3**0.5 / 2,
        "cos(30)": np.cos(np.deg2rad(30))
    }

    print("--- T-008: Generation 2 & 3 Mass Ratio Audit ---")
    
    for label, ratio in ratios.items():
        print(f"\nRatio {label}: {ratio:.4f}")
        for t_label, t_val in targets.items():
            error = abs(ratio - t_val) / t_val
            if error < 0.05: # 5% threshold
                print(f" - HIT: {t_label} ({t_val:.4f}) | Error: {error:.4%}")

    # The Generation-over-Generation Shift (The "Refractive Index")
    # If Gen 1 is phi^3, what is the 'Index' for Gen 2?
    print(f"\n--- Refractive Index Shift Analysis ---")
    gen1_val = ratios["up/electron"]
    gen2_val_strange = ratios["strange/muon"]
    gen2_val_charm = ratios["charm/muon"]
    
    index_strange = gen2_val_strange / gen1_val
    index_charm = gen2_val_charm / gen1_val
    
    print(f"Gen 1 (up/electron) Index: 1.00 (Reference phi^3)")
    print(f"Gen 2 (strange/muon) Index: {index_strange:.4f} (Shift relative to phi^3)")
    print(f"Gen 2 (charm/muon) Index: {index_charm:.4f} (Shift relative to phi^3)")
    
    # 4. Charm/Muon Specific Check: 12.02
    print(f"\n--- Specific Signal: charm/muon ≈ 12 ---")
    error_12 = abs(ratios["charm/muon"] - 12.0) / 12.0
    print(f"Charm / Muon: 12.020 | Error from 12: {error_12:.4%}")

if __name__ == "__main__":
    run_gen2_audit()
