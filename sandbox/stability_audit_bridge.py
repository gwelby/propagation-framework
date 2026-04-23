import numpy as np

# Stability Audit: Weinberg Angle Casimir Polynomial
# Target: x^2 + C2*x - C2 = 0
# j=1/2, C2 = 0.75

def solve_casimir(c2, noise_level=0.0):
    # Add noise to C2
    c2_n = c2 + np.random.normal(0, noise_level)
    # Solve: x^2 + c2_n*x - c2_n = 0
    # Roots: [-c2_n ± sqrt(c2_n^2 + 4*c2_n)] / 2
    discriminant = c2_n**2 + 4*c2_n
    x_plus = (-c2_n + np.sqrt(discriminant)) / 2
    return x_plus

c2_target = 0.75
trials = 1000
noise = 1e-6
results = [solve_casimir(c2_target, noise) for _ in range(trials)]

mean_val = np.mean(results)
std_dev = np.std(results)

print(f"Weinberg Casimir Stability Scan")
print(f"  Target C2: {c2_target}")
print(f"  Noise: {noise}")
print(f"  Mean result: {mean_val:.8f}")
print(f"  Standard Deviation: {std_dev:.8e}")
print(f"  Stability Factor (Mean/Std): {mean_val/std_dev:.2f}")
