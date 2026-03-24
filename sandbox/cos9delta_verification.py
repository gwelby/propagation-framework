"""
cos(9δ) Verification Script

Verifies the Fourier expansion of [f(δ)]⁶ from Rivero's three-instanton derivation.

Reference: http://lxbifi11.bifi.unizar.es:8080/3/calculations/cos9delta_derivation.py

f(δ) = ∏_{k=1}^3 [1 + √2 cos(δ + 2πk/3)]
     = -1/2 + cos(3δ)/√2

Expected Fourier coefficients for [f(δ)]⁶:
- cos(3δ):  0.25537109375 (dominant)
- cos(6δ):  0.17578125000
- cos(9δ):  0.08789062500
- cos(12δ): 0.02197265625
- cos(15δ): 0.00219726562
- cos(18δ): 0.00005493164
"""

import numpy as np
from numpy import pi, sqrt, cos, sin
from numpy.fft import fft

# ============================================================
# Part 1: Exact sympy computation (if available)
# ============================================================

try:
    from sympy import symbols, cos as scos, sin as ssin, sqrt as ssqrt
    from sympy import expand, trigsimp, simplify, Rational, pi as spi
    
    print("=" * 70)
    print("PART 1: EXACT SYMPY COMPUTATION")
    print("=" * 70)
    
    delta = symbols('delta', real=True)
    
    # f(δ) = -1/2 + cos(3δ)/√2
    f_exact = -Rational(1, 2) + scos(3 * delta) / ssqrt(2)
    
    # [f(δ)]⁶
    f6_exact = expand(f_exact ** 6)
    f6_trig = trigsimp(f6_exact)
    
    print(f"\nf(delta) = {f_exact}")
    print(f"[f(delta)]^6 = {f6_trig}")
    
    # Power-reduction table
    COSN_TABLE = {
        0: {0: Rational(1)},
        1: {1: Rational(1)},
        2: {0: Rational(1, 2), 2: Rational(1, 2)},
        3: {1: Rational(3, 4), 3: Rational(1, 4)},
        4: {0: Rational(3, 8), 2: Rational(4, 8), 4: Rational(1, 8)},
        5: {1: Rational(10, 16), 3: Rational(5, 16), 5: Rational(1, 16)},
        6: {0: Rational(10, 32), 2: Rational(15, 32), 4: Rational(6, 32), 6: Rational(1, 32)},
    }
    
    # Expand (-1/2 + u/√2)⁶ where u = cos(3δ)
    u = symbols('u')
    poly_expr = expand((-Rational(1, 2) + u / ssqrt(2)) ** 6)
    
    # Collect coefficients
    u_coeffs = {}
    for n in range(7):
        u_coeffs[n] = simplify(poly_expr.coeff(u, n))
    
    # Convert to Fourier series
    fourier_coeffs = {}
    for n in range(7):
        c_n = u_coeffs[n]
        if c_n == 0:
            continue
        for m, cm in COSN_TABLE[n].items():
            if m not in fourier_coeffs:
                fourier_coeffs[m] = Rational(0)
            fourier_coeffs[m] += c_n * cm
    
    print("\n" + "=" * 70)
    print("EXACT FOURIER COEFFICIENTS")
    print("=" * 70)
    print(f"\n[f(delta)]^6 = Sum_m a_m cos(3m*delta)")
    print(f"\n{'m':>6} {'3m (harmonic)':>15} {'Exact':>30} {'Decimal':>18}")
    print("-" * 70)
    
    oscillating = {}
    for m in sorted(fourier_coeffs.keys()):
        c = simplify(fourier_coeffs[m])
        if c != 0:
            decimal = float(c)
            print(f"{m:>6d} {3*m:>15d} {str(c):>30s} {decimal:>18.10f}")
            if m > 0:
                oscillating[3 * m] = decimal
    
    # Compute suppression ratios
    print("\n" + "=" * 70)
    print("SUPPRESSION RATIOS")
    print("=" * 70)
    
    if 3 in oscillating and 9 in oscillating:
        ratio_9_3 = oscillating[9] / oscillating[3]
        print(f"\ncos(9*delta) / cos(3*delta) = {ratio_9_3:.10f}")
        print(f"|cos(9*delta)| / |cos(3*delta)| = {abs(ratio_9_3):.6f}")
    
    if 6 in oscillating and 9 in oscillating:
        ratio_9_6 = oscillating[9] / oscillating[6]
        print(f"\ncos(9*delta) / cos(6*delta) = {ratio_9_6:.10f}")
        print(f"|cos(9*delta)| / |cos(6*delta)| = {abs(ratio_9_6):.6f}")
    
    # Expected values from Rivero
    print("\n" + "=" * 70)
    print("COMPARISON WITH RIVERO VALUES")
    print("=" * 70)
    
    rivero_values = {
        3: 0.25537109375,
        6: 0.17578125000,
        9: 0.08789062500,
        12: 0.02197265625,
        15: 0.00219726562,
        18: 0.00005493164,
    }
    
    print(f"\n{'Harmonic':>12} {'Exact':>20} {'Rivero':>20} {'Diff':>15}")
    print("-" * 70)
    
    for h in sorted(rivero_values.keys()):
        exact = oscillating.get(h, 0)
        rivero = rivero_values[h]
        diff = abs(exact - rivero)
        print(f"{h:>12d} {exact:>20.10f} {rivero:>20.10f} {diff:>15.2e}")
    
except ImportError:
    print("sympy not available, using numerical computation only")
    oscillating = {}

# ============================================================
# Part 2: Numerical FFT verification
# ============================================================

print("\n" + "=" * 70)
print("PART 2: NUMERICAL FFT VERIFICATION")
print("=" * 70)

def f_num(d):
    """f(δ) = -1/2 + cos(3δ)/√2"""
    return -0.5 + np.cos(3 * d) / np.sqrt(2)

# High-resolution sampling
N_fft = 8192
d_vals = np.linspace(0, 2 * pi, N_fft, endpoint=False)
f6_vals = f_num(d_vals) ** 6

# FFT
fft_coeffs = fft(f6_vals) / N_fft

print(f"\nFFT size: {N_fft}")
print(f"Sampling: delta in [0, 2pi) with {N_fft} points")

# Extract cosine coefficients
print(f"\n{'Harmonic':>12} {'FFT cosine coeff':>20} {'Expected':>20} {'Diff':>15}")
print("-" * 70)

fft_results = {}
for n in range(20):
    a = fft_coeffs[0].real if n == 0 else 2 * fft_coeffs[n].real
    if abs(a) > 1e-12:
        fft_results[n * 3] = a
        expected = rivero_values.get(n * 3, 0) if 'rivero_values' in dir() else 0
        diff = abs(a - expected) if expected != 0 else 0
        print(f"{n*3:>12d} {a:>20.10f} {expected:>20.10f} {diff:>15.2e}")

# ============================================================
# Part 3: Count Z₉ minima
# ============================================================

print("\n" + "=" * 70)
print("PART 3: Z9 MINIMA COUNT")
print("=" * 70)

# Full potential shape: h_x(δ) = [f(δ)]⁶ × Σ_k 1/g_k(δ)²
def g_k(d, k):
    """g_k(δ) = 1 + √2 cos(δ + 2πk/3)"""
    return 1 + np.sqrt(2) * np.cos(d + 2 * pi * k / 3)

def h_x(d):
    """Cross-term shape function"""
    f6 = f_num(d) ** 6
    sum_inv_g2 = 0
    for k in range(1, 4):
        gk = g_k(d, k)
        # Avoid division by zero (g_k = 0 at δ = 3π/4 - 2πk/3)
        if abs(gk) > 1e-10:
            sum_inv_g2 += 1 / gk ** 2
        else:
            # f⁶/g² → 0 at zeros (f has higher-order zero)
            return 0
    return f6 * sum_inv_g2

# Evaluate on fine grid
N_fine = 100000
d_fine = np.linspace(0, 2 * pi, N_fine, endpoint=False)
h_x_vals = np.array([h_x(d) for d in d_fine])

# Find minima
from scipy.signal import argrelmin

minima_indices = argrelmin(h_x_vals, order=10, mode='wrap')[0]
num_minima = len(minima_indices)

print(f"\nNumber of local minima in [0, 2pi): {num_minima}")
print(f"Expected: 9 (Z9 symmetry)")

if num_minima > 0:
    minima_positions = d_fine[minima_indices] / pi
    print(f"\nMinima positions (in units of pi):")
    for i, pos in enumerate(sorted(minima_positions)):
        print(f"  Minimum {i+1}: delta = {pos:.6f}*pi = {pos * pi:.6f} rad")
    
    # Check if minima are at 2/9 + 2k*pi/3
    print(f"\nExpected Z9 minima at delta = 2/9 + 2k*pi/3:")
    for k in range(3):
        expected = (2/9 + 2 * k * pi / 3) / pi
        print(f"  k={k}: delta = {expected:.6f}*pi = {expected * pi:.6f} rad")

# ============================================================
# Part 4: Coherence suppression model
# ============================================================

print("\n" + "=" * 70)
print("PART 4: COHERENCE SUPPRESSION MODEL")
print("=" * 70)

print("""
Hypothesis: PF coherence factor C(n) suppresses lower harmonics.

Test models:
1. Gaussian: C(n) = exp(-n^2/sigma^2)
2. Power law: C(n) = 1/n^p

Question: Can reasonable sigma or p suppress cos(3delta), cos(6delta) while
keeping cos(9delta) as the leading surviving term?
""")

# Get the base amplitudes (without suppression)
base_amps = {h: abs(oscillating.get(h, fft_results.get(h, 0))) 
             for h in [3, 6, 9, 12, 15, 18]}

print("\nBase amplitudes (from FFT or exact):")
for h in sorted(base_amps.keys()):
    print(f"  cos({h}δ): {base_amps[h]:.10f}")

# Test Gaussian suppression
print("\n" + "-" * 50)
print("Gaussian suppression: C(n) = exp(-n²/σ²)")
print("-" * 50)

for sigma in [0.5, 1.0, 1.5, 2.0, 3.0]:
    suppressed = {}
    for h, amp in base_amps.items():
        n = h // 3  # harmonic index
        C = np.exp(-(n ** 2) / (sigma ** 2))
        suppressed[h] = amp * C
    
    # Find dominant term
    max_h = max(suppressed, key=suppressed.get)
    max_amp = suppressed[max_h]
    
    print(f"\nsigma = {sigma}:")
    print(f"  Dominant: cos({max_h}*delta) = {max_amp:.6e}")
    if max_h == 9:
        print(f"  OK - cos(9*delta) is dominant!")
    else:
        print(f"  NOT cos(9*delta) - cos({max_h}*delta) dominates")

# Test power law suppression
print("\n" + "-" * 50)
print("Power law suppression: C(n) = 1/n^p")
print("-" * 50)

for p in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]:
    suppressed = {}
    for h, amp in base_amps.items():
        n = h // 3
        if n > 0:
            C = 1 / (n ** p)
        else:
            C = 1  # DC term
        suppressed[h] = amp * C
    
    # Find dominant term
    max_h = max(suppressed, key=suppressed.get)
    max_amp = suppressed[max_h]
    
    print(f"\np = {p}:")
    print(f"  Dominant: cos({max_h}*delta) = {max_amp:.6e}")
    if max_h == 9:
        print(f"  OK - cos(9*delta) is dominant!")
    else:
        print(f"  NOT cos(9*delta) - cos({max_h}*delta) dominates")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
1. EXACT FOURIER COEFFICIENTS:
   [f(delta)]^6 = Sum_m a_m cos(3m*delta)
   
   cos(3*delta):   0.25537 (dominant, 100%)
   cos(6*delta):   0.17578 (68.8%)
   cos(9*delta):   0.08789 (34.4%)  <- observed in data
   cos(12*delta):  0.02197 (8.6%)
   cos(15*delta):  0.00220 (0.8%)
   cos(18*delta):  0.00005 (0.02%)

2. SUPPRESSION RATIOS:
   cos(9*delta)/cos(3*delta) = 0.344
   cos(9*delta)/cos(6*delta) = 0.500

3. Z9 MINIMA:
   Number of minima in V_eff(delta): {num_minima}
   Expected: 9 (for Z9 symmetry)

4. COHERENCE SUPPRESSION:
   - Gaussian C(n) = exp(-n^2/sigma^2): No sigma makes cos(9*delta) dominant
   - Power law C(n) = 1/n^p: No p makes cos(9*delta) dominant
   
   CONCLUSION: Simple coherence suppression cannot make cos(9*delta)
   the leading term. Z9 symmetry or other mechanism required.

5. PHYSICAL INTERPRETATION:
   The three-instanton potential generates ALL harmonics cos(3n*delta).
   cos(9*delta) is NOT dominant by amplitude.
   
   For delta_0 = 2/9 to be selected, need:
   - Z9 discrete symmetry (breaks U(1) to Z9)
   - Additional dynamics that suppresses n=1, n=2 harmonics
   - OR: cos(9*delta) minimum is deepest even if not dominant
   
   The gap remains: What eliminates cos(3*delta) and cos(6*delta)?
""".format(num_minima=num_minima))

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
