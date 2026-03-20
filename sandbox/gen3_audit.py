import numpy as np

def run_gen3_audit():
    # 1. Fundamental Constants (PDG 2024 central values)
    masses = {
        "tau": 1776.86,
        "bottom": 4180,
        "top": 172690
    }

    # 2. Ratios to test
    ratios = {
        "bottom/tau": masses["bottom"] / masses["tau"],
        "top/tau": masses["top"] / masses["tau"]
    }

    # 3. Geometric / Transcendental Targets
    phi = (1 + 5**0.5) / 2
    alpha_inv = 137.036
    targets = {
        "e": np.e,
        "pi": np.pi,
        "pi^2": np.pi**2,
        "10*pi": 10 * np.pi,
        "10*pi^2": 10 * np.pi**2,
        "alpha_inv/sqrt(2)": alpha_inv / (2**0.5),
        "alpha_inv / phi": alpha_inv / phi,
        "alpha_inv * (2/3)": alpha_inv * (2/3),
        "phi^5": phi**5,
        "sqrt(5)": 5**0.5,
        "sqrt(6)": 6**0.5
    }

    print("--- T-008: Generation 3 Mass Ratio Audit ---")
    
    for label, ratio in ratios.items():
        print(f"\nRatio {label}: {ratio:.4f}")
        for t_label, t_val in targets.items():
            error = abs(ratio - t_val) / t_val
            if error < 0.05: # 5% threshold
                print(f" - HIT: {t_label} ({t_val:.4f}) | Error: {error:.4%}")

    # The Final Scaling Index (The "Top-Tau" Peak)
    print(f"\n--- The Ultimate Scaling Check: top/tau ---")
    target_val = alpha_inv / (2**0.5)
    error_alpha = abs(ratios["top/tau"] - target_val) / target_val
    print(f"Top / Tau: {ratios['top/tau']:.4f}")
    print(f"Target alpha_inv / sqrt(2): {target_val:.4f}")
    print(f"Error from alpha_inv / sqrt(2): {error_alpha:.4%}")

    # The Bottom / Tau Ratio (2.35)
    print(f"\n--- Specific Signal: bottom/tau ≈ sqrt(5.5)? ---")
    target_val_b = (5.5)**0.5
    error_b = abs(ratios["bottom/tau"] - target_val_b) / target_val_b
    print(f"Bottom / Tau: {ratios['bottom/tau']:.4f}")
    print(f"Target sqrt(5.5): {target_val_b:.4f}")
    print(f"Error: {error_b:.4%}")

if __name__ == "__main__":
    run_gen3_audit()
