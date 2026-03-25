import numpy as np
import itertools
from dataclasses import dataclass

def get_casimir_root(j):
    """Returns the positive root of the Casimir polynomial x^2 + C2*x - C2 = 0"""
    C2 = j * (j + 1)
    if C2 == 0:
        return 0.0
    return (-C2 + np.sqrt(C2**2 + 4*C2)) / 2.0

def hunt_for_alpha():
    print("=======================================================")
    print("  EXPERIMENT 1: THE ALPHA (α) HUNT")
    print("  Scanning Casimir polynomial roots for 1/137.036")
    print("=======================================================\n")

    # Target
    target_alpha = 1.0 / 137.035999
    target_alpha_inv = 137.035999
    print(f"Target α     : {target_alpha:.8f}")
    print(f"Target 1/α   : {target_alpha_inv:.8f}\n")

    # The fundamental roots
    spins = [0.5, 1.0, 1.5, 2.0] # 0 is trivial
    roots = {j: get_casimir_root(j) for j in spins}
    
    print("--- Fundamental Casimir Roots (x_j) ---")
    for j, r in roots.items():
        print(f"j={j:<3}: x = {r:.6f}, (1-x) = {1-r:.6f}")
    print()

    # The Weinberg angle ratio we just proved
    weinberg = 1.0 - (roots[0.5] / roots[1.0])
    print(f"Known Anchor (Weinberg): sin^2(θ_W) = 1 - (x_0.5 / x_1.0) = {weinberg:.6f}\n")

    results = []

    # 1. Simple Ratios & Products (x_a * x_b) / x_c etc.
    print("--- Scanning Algebraic Combinations ---")
    
    # We will build a small search space of expressions
    # Variables: x_0.5, x_1.0, x_1.5, x_2.0
    # Operations: *, /, +, -, **2, **3, (1-x)
    
    components = []
    for j, r in roots.items():
        components.append((f"x_{j}", r))
        components.append((f"(1-x_{j})", 1.0 - r))
        components.append((f"x_{j}^2", r**2))
        components.append((f"(1-x_{j})^2", (1.0 - r)**2))
        components.append((f"x_{j}^3", r**3))

    # Test all pairs: A * B
    for (n1, v1), (n2, v2) in itertools.combinations(components, 2):
        val = v1 * v2
        if val > 0:
            error = abs(val - target_alpha) / target_alpha
            if error < 0.05: # Within 5%
                results.append((error, f"{n1} * {n2}", val))
            
            # Check inverse
            inv_val = 1.0 / val
            error_inv = abs(inv_val - target_alpha_inv) / target_alpha_inv
            if error_inv < 0.05:
                results.append((error_inv, f"1 / ({n1} * {n2})", val))

    # Test all pairs: A / B
    for (n1, v1), (n2, v2) in itertools.permutations(components, 2):
        if v2 > 0:
            val = v1 / v2
            if val > 0:
                error = abs(val - target_alpha) / target_alpha
                if error < 0.05:
                    results.append((error, f"{n1} / {n2}", val))

    # Test triplets: A * B * C
    for (n1, v1), (n2, v2), (n3, v3) in itertools.combinations(components, 3):
        val = v1 * v2 * v3
        if val > 0:
            error = abs(val - target_alpha) / target_alpha
            if error < 0.05:
                results.append((error, f"{n1} * {n2} * {n3}", val))

    # Test geometric/topological constructs
    # Weinberg angle is intimately related to Alpha
    val = (weinberg ** 3) / roots[1.0] # Just throwing a dart
    error = abs(val - target_alpha) / target_alpha
    # results.append((error, "weinberg^3 / x_1.0", val))

    # Sort by error
    results.sort(key=lambda x: x[0])

    print(f"{'Expression':<40} | {'Value (α)':<10} | {'Error':<10}")
    print("-" * 65)
    for error, expr, val in results[:15]:
        print(f"{expr:<40} | {val:.6f}   | {error*100:.2f}%")

    if not results:
         print("No combinations found within 5% error. The relationship is deeper.")
    else:
        best_error, best_expr, best_val = results[0]
        if best_error < 0.01:
            print(f"\n[!] HIGH SIGNAL FOUND: {best_expr} matches α to {best_error*100:.3f}%")
        else:
            print(f"\nClosest match is {best_error*100:.2f}% off. Likely not the true geometric mechanism.")

if __name__ == "__main__":
    hunt_for_alpha()