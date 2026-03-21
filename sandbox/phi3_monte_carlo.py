"""
Phi^3 Monte Carlo Test - Electron/Up Quark Mass Ratio

Testing: m_e / m_u approx 1/phi^3

PDG 2024 values:
- m_e = 0.51099895 MeV (exact, well-measured)
- m_u = 2.16 MeV central value, range 1.7-2.7 MeV (large uncertainty)
- phi = 1.6180339887... (golden ratio)
- 1/phi^3 = 0.2360679775...

Question: Is the observed ratio statistically significant, or expected by chance?
"""

import numpy as np

# Constants
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
INV_PHI3 = 1 / (PHI ** 3)   # 1/phi^3

# PDG 2024 values
M_E = 0.51099895  # MeV (exact)
M_U_CENTRAL = 2.16  # MeV
M_U_MIN = 1.7  # MeV
M_U_MAX = 2.7  # MeV

# Calculate observed ratio
RATIO_OBSERVED = M_E / M_U_CENTRAL
RATIO_TARGET = INV_PHI3
PERCENT_ERROR = abs(RATIO_OBSERVED - RATIO_TARGET) / RATIO_TARGET * 100

print("=" * 60)
print("PHI^3 MONTE CARLO TEST - ELECTRON/UP QUARK MASS RATIO")
print("=" * 60)
print(f"\nConstants:")
print(f"  phi (golden ratio)   = {PHI:.10f}")
print(f"  1/phi^3              = {INV_PHI3:.10f}")
print(f"\nPDG 2024 Values:")
print(f"  m_e                  = {M_E} MeV")
print(f"  m_u (central)        = {M_U_CENTRAL} MeV")
print(f"  m_u (range)          = {M_U_MIN} - {M_U_MAX} MeV")
print(f"\nObserved Ratio:")
print(f"  m_e / m_u            = {RATIO_OBSERVED:.10f}")
print(f"  Target (1/phi^3)     = {RATIO_TARGET:.10f}")
print(f"  Percent error        = {PERCENT_ERROR:.4f}%")

# Monte Carlo simulation
# Sample m_u uniformly from its PDG uncertainty range
N_SAMPLES = 100_000
np.random.seed(42)  # Reproducibility

m_u_samples = np.random.uniform(M_U_MIN, M_U_MAX, N_SAMPLES)
ratio_samples = M_E / m_u_samples

# How many samples land within the same % error of 1/phi^3?
tolerance = PERCENT_ERROR / 100 * RATIO_TARGET
hits = np.sum(np.abs(ratio_samples - RATIO_TARGET) <= tolerance)
p_value = hits / N_SAMPLES

print(f"\n{'=' * 60}")
print("MONTE CARLO RESULTS")
print("=" * 60)
print(f"  Samples              = {N_SAMPLES:,}")
print(f"  Hits (within +/-{PERCENT_ERROR:.4f}%)  = {hits:,}")
print(f"  p-value              = {p_value:.6f}")
print(f"  Significance         = {1 - p_value:.4f}")

# Statistical interpretation
print(f"\n{'=' * 60}")
print("INTERPRETATION")
print("=" * 60)

if p_value < 0.001:
    print("  VERDICT: HIGHLY SIGNIFICANT (p < 0.001)")
    print("  The electron/up ratio is NOT expected by chance.")
    print("  This is a real signal requiring explanation.")
elif p_value < 0.01:
    print("  VERDICT: SIGNIFICANT (p < 0.01)")
    print("  The ratio is unlikely to be coincidence.")
    print("  Suggests underlying structure.")
elif p_value < 0.05:
    print("  VERDICT: MARGINALLY SIGNIFICANT (p < 0.05)")
    print("  The ratio may be real, but more analysis needed.")
else:
    print("  VERDICT: NOT SIGNIFICANT (p >= 0.05)")
    print("  The ratio is consistent with random chance.")
    print("  Likely coincidence.")

# Compare to simple integer ratios
print(f"\n{'=' * 60}")
print("INTEGER RATIO COMPARISON")
print("=" * 60)

# Test simple ratios p/q where p, q are small integers
simple_ratios = []
for q in range(1, 20):
    for p in range(1, 20):
        ratio = p / q
        error = abs(ratio - RATIO_TARGET) / RATIO_TARGET
        simple_ratios.append((p, q, ratio, error))

# Sort by error
simple_ratios.sort(key=lambda x: x[3])

print("  Best simple integer ratios to 1/phi^3:")
for i, (p, q, ratio, error) in enumerate(simple_ratios[:5]):
    print(f"    {p}/{q} = {ratio:.10f} (error: {error*100:.4f}%)")

# Where does 1/phi^3 rank?
observed_error = PERCENT_ERROR / 100
better_ratios = [r for r in simple_ratios if r[3] < observed_error]
print(f"\n  1/phi^3 ranks better than {len(better_ratios)} simple ratios")
print(f"  Rank: #{len(better_ratios) + 1} out of {len(simple_ratios)}")

# Additional analysis: distribution of ratio samples
print(f"\n{'=' * 60}")
print("DISTRIBUTION ANALYSIS")
print("=" * 60)
print(f"  Mean of sampled ratios    = {np.mean(ratio_samples):.10f}")
print(f"  Std dev of sampled ratios = {np.std(ratio_samples):.10f}")
print(f"  Median                    = {np.median(ratio_samples):.10f}")
print(f"  95% CI                    = [{np.percentile(ratio_samples, 2.5):.10f}, {np.percentile(ratio_samples, 97.5):.10f}]")

# Z-score of observed ratio
z_score = (RATIO_OBSERVED - np.mean(ratio_samples)) / np.std(ratio_samples)
print(f"  Z-score of observed       = {z_score:.4f}")

# Trials factor correction
# We're testing multiple phi powers, not just phi^3
# Apply Bonferroni correction for ~25 tests (phi^1 through phi^25)
N_TESTS = 25
p_value_corrected = min(1.0, p_value * N_TESTS)

print(f"\n{'=' * 60}")
print("TRIALS FACTOR CORRECTION")
print("=" * 60)
print(f"  Tests performed         = ~{N_TESTS} (phi^1 through phi^25)")
print(f"  Uncorrected p-value     = {p_value:.6f}")
print(f"  Corrected p-value       = {p_value_corrected:.6f} (Bonferroni)")

if p_value_corrected < 0.05:
    print("  VERDICT: Still significant after correction")
else:
    print("  VERDICT: Not significant after trials factor")

print(f"\n{'=' * 60}")
print("CLAIMS.MD UPDATE RECOMMENDATION")
print("=" * 60)

if p_value < 0.01 and p_value_corrected < 0.05:
    print("  Current status: EMPIRICAL (0.65)")
    print("  Recommendation: INCREASE to 0.70-0.75")
    print("  Rationale: Statistically significant signal, survives trials correction")
elif p_value < 0.05:
    print("  Current status: EMPIRICAL (0.65)")
    print("  Recommendation: MAINTAIN at 0.65")
    print("  Rationale: Marginal significance, needs more data")
else:
    print("  Current status: EMPIRICAL (0.65)")
    print("  Recommendation: DECREASE to 0.40-0.50 (INTUITION)")
    print("  Rationale: Not statistically significant, likely coincidence")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
