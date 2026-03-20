import math

def calculate_varma_r(masses, k):
    sum_numerator = sum(m**(1/k) for m in masses)
    sum_denominator = sum(m**(1/(2*k)) for m in masses)
    return (sum_numerator**k) / (sum_denominator**(2*k))

# PDG 2024 MS-bar masses at MZ scale (91.18 GeV) in GeV
# Source: Common literature values for MS-bar running masses at MZ
masses_mz = {
    "u": 0.00127,
    "d": 0.00259,
    "s": 0.0538,
    "c": 0.624,
    "b": 2.82,
    "t": 172.0 # pole mass
}

# Quarks: Sum of all 6, k=2
quarks_all = [masses_mz[q] for q in "udscbt"]
R_q = calculate_varma_r(quarks_all, 2)

# Quarks: with t_msbar ~ 163 GeV
quarks_all_msbar = [0.00127, 0.00259, 0.0538, 0.624, 2.82, 163.0]
R_q_msbar = calculate_varma_r(quarks_all_msbar, 2)

# Leptons: Sum of 3, k=1
leptons = [0.000510999, 0.105658, 1.77686]
R_l = calculate_varma_r(leptons, 1)

print(f"--- Varma Unified Fermion Mass Ratio Audit ---")
print(f"Leptons (k=1, n=3): {R_l:.6f} (Target: 0.666667)")
print(f"Quarks (k=2, n=6, t_pole): {R_q:.6f} (Target: 0.500000)")
print(f"Quarks (k=2, n=6, t_msbar=163): {R_q_msbar:.6f} (Target: 0.500000)")

# Let's check sensitivity to top mass
for mt in range(150, 181, 5):
    q_list = [0.00127, 0.00259, 0.0538, 0.624, 2.82, float(mt)]
    res = calculate_varma_r(q_list, 2)
    print(f" mt={mt:3}: R_q = {res:.6f}")

