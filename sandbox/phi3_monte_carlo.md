# φ³ Monte Carlo Test — Electron/Up Quark Mass Ratio

**Test Date**: 2026-03-20  
**Test Agent**: Qwen Code  
**Reference**: CLAIMS.md — "Electron/Up ≈ 1/φ³" entry (EMPIRICAL, 0.65)  
**Script**: `sandbox/phi3_monte_carlo.py`

---

## The Claim

The electron to up quark mass ratio approximates 1/φ³ (where φ is the golden ratio):

$$\frac{m_e}{m_u} \approx \frac{1}{\phi^3}$$

---

## Input Values (PDG 2024)

| Constant | Value | Uncertainty |
|----------|-------|-------------|
| m_e (electron mass) | 0.51099895 MeV | ±0.00000000031 MeV (negligible) |
| m_u (up quark mass) | 2.16 MeV | 1.7 – 2.7 MeV (large uncertainty) |
| φ (golden ratio) | 1.6180339887... | Exact (mathematical constant) |
| 1/φ³ | 0.2360679775... | Exact |

---

## Observed Values

| Quantity | Value |
|----------|-------|
| m_e / m_u (observed) | 0.2365735880 |
| 1/φ³ (target) | 0.2360679775 |
| **Percent error** | **0.2142%** |

---

## Monte Carlo Method

**Question**: Given the large uncertainty in m_u (1.7–2.7 MeV), how likely is it that a random mass value in this range would produce a ratio within 0.2142% of 1/φ³?

**Procedure**:
1. Sample m_u uniformly from [1.7, 2.7] MeV
2. Calculate m_e / m_u for each sample
3. Count how many samples land within ±0.2142% of 1/φ³
4. Compute p-value = (hits) / (total samples)

**Samples**: 100,000  
**Seed**: 42 (reproducible)

---

## Results

| Metric | Value |
|--------|-------|
| Total samples | 100,000 |
| Hits (within ±0.2142%) | 920 |
| **p-value** | **0.009200** |
| Significance | 0.9908 |

---

## Statistical Interpretation

### Uncorrected Significance

**VERDICT: SIGNIFICANT (p < 0.01)**

The uncorrected p-value of 0.0092 means that only ~0.92% of random mass values in the allowed range would produce a ratio this close to 1/φ³. This is below the standard 0.01 threshold for statistical significance.

### Integer Ratio Comparison

The test also compared 1/φ³ to all simple integer ratios p/q where p,q ∈ [1,19]:

| Rank | Ratio | Value | Error |
|------|-------|-------|-------|
| 1 | **1/φ³** | 0.2360679775 | **0.2142%** |
| 2 | 4/17 | 0.2352941176 | 0.3278% |
| 3 | 3/13 | 0.2307692308 | 2.2446% |
| 4 | 2/9 | 0.2222222222 | 5.8652% |
| 5 | 1/4 | 0.2500000000 | 5.9017% |

**1/φ³ ranks #1 out of 361 tested ratios** — it is a better fit than any simple integer ratio.

### Distribution Analysis

| Statistic | Value |
|-----------|-------|
| Mean of sampled ratios | 0.2364476514 |
| Std dev of sampled ratios | 0.0316621332 |
| Median | 0.2322057777 |
| 95% CI | [0.191, 0.296] |
| Z-score of observed | 0.0040 |

The observed ratio sits almost exactly at the mean of the distribution (z-score ≈ 0), meaning it is not an outlier in the sampled range.

---

## Trials Factor Correction

**Critical Issue**: This test is not isolated. The framework tests multiple φ powers (φ¹ through φ²⁵) against particle mass ratios. This is a classic "look-elsewhere effect" — if you test enough hypotheses, some will appear significant by chance.

**Bonferroni Correction** (conservative):
- Tests performed: ~25 (φ¹ through φ²⁵)
- Uncorrected p-value: 0.0092
- **Corrected p-value: 0.230**

**VERDICT AFTER CORRECTION: NOT SIGNIFICANT**

After accounting for the trials factor, the result is consistent with random chance. The correction is conservative (assumes all tests are independent, which they are not), but even so, p = 0.23 is well above the 0.05 threshold.

---

## Comparison to Harmonic Series Test

The harmonic series test (sandbox_results.md, March 2026) found:
- Coefficient of variation = 0.94 (essentially random)
- **VERDICT: FAILED** — particle masses do not follow harmonic spacing

The φ³ test performs better than the harmonic series test, but:
- Harmonic series: CV = 0.94 → clearly noise
- φ³ ratio: p = 0.009 (uncorrected), p = 0.23 (corrected) → ambiguous

---

## Verdict

### What This Test Shows

1. **The 0.2142% error is real** — the electron/up ratio is genuinely close to 1/φ³
2. **Uncorrected significance is strong** (p < 0.01) — closer than expected by chance
3. **After trials correction, significance disappears** (p = 0.23) — consistent with coincidence

### What This Does NOT Show

1. This does NOT prove the ratio is coincidence — only that it's not statistically distinguishable from coincidence given current uncertainties
2. This does NOT falsify the claim — a future reduction in m_u uncertainty could shift the p-value dramatically

### Key Limiting Factor

The up quark mass uncertainty (1.7–2.7 MeV) is the dominant source of uncertainty. If future lattice QCD calculations or experimental measurements narrow this to, say, 2.16 ± 0.05 MeV, the test would become much more powerful.

---

## CLAIMS.md Update Recommendation

**Current Status**: EMPIRICAL (0.65)

**Recommendation**: **MAINTAIN at 0.65**

**Rationale**:
- The uncorrected p-value (0.0092) is significant, suggesting a real signal
- The corrected p-value (0.23) is not significant, preventing a confidence increase
- The result is "intriguing but not conclusive" — exactly what 0.65 represents
- Future m_u precision improvements could revise this either direction

**What Would Increase Confidence**:
- m_u measurement converging toward 2.16 MeV with <5% uncertainty
- Independent φ-based predictions confirmed in other mass ratios
- A theoretical mechanism deriving φ from propagation axioms

**What Would Decrease Confidence**:
- m_u measurement shifting toward 2.3 MeV or higher
- A posteriori analysis showing many equally-good φ^n fits exist

---

## Epistemic Status

**The numbers are real. The interpretation is unproven.**

The electron mass is known to 9 significant figures. The up quark mass is known to ~20% uncertainty. The golden ratio is a mathematical exact constant. The 0.2142% error between m_e/m_u and 1/φ³ is a factual statement about current PDG values.

Whether this is:
- (A) A deep structural feature of the propagation medium
- (B) A remarkable coincidence
- (C) An artifact of a posteriori pattern matching

...remains open. This Monte Carlo test shows it is not statistically significant after trials correction, but also not ruled out.

---

## Code Availability

**Script**: `d:\Fundamentals\sandbox\phi3_monte_carlo.py`

**Reproducibility**: Set `np.random.seed(42)` for identical results.

**Dependencies**: numpy (no scipy required)

---

*Test completed: 2026-03-20*  
*Agent: Qwen Code*  
*Status: Inconclusive — maintain current confidence*
