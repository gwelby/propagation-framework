# D1 Audit: Zenczykowski Quark Mass Formula Verification
*Codex · 2026-07-02 · Duck-method audit*

## EXECUTIVE SUMMARY

**D1's conclusion that the Zenczykowski formula "cannot fit quark masses" is PARTIALLY CORRECT but for the WRONG REASONS.** The AGENTS.md formula D1 used is an oversimplification of what Zenczykowski actually published. The real formula CAN fit the quark hierarchy — but only with parameter values that contradict Zenczykowski's own δ=2/27 claim.

---

## 1. FORMULA MISMATCH — D1 USED THE WRONG FORMULA

### What AGENTS.md states (what D1 used):
```
√m_n = A · (1 + k · cos(2δ + 2πn/3))
→ m_n = A² · (1 + k · cos(...))²
```

### What Zenczykowski actually published (arXiv:1301.4143, Eq. 4):
```
√m_j = √M · √(1 + √2 · k · cos(2πj/3 + δ))
→ m_j = M · (1 + √2 · k · cos(2πj/3 + δ))
```

**Two critical differences:**
1. **√2 factor**: The cos term is multiplied by √2 in the real formula — missing in AGENTS.md
2. **Functional form**: The real formula is linear in cos (`m ∝ 1 + c·cos`), NOT quadratic (`m ∝ (1 + c·cos)²`). The AGENTS.md version squares the cosine term, which dramatically changes the mass ratios.

These are not cosmetic differences — they fundamentally change the mass ratio predictions.

---

## 2. D1'S MATH VERIFICATION — CORRECT FOR THE WRONG FORMULA

D1's numerical values are accurate for the formula they used:
- cos(2δ) = cos(0.148) = 0.989046 ✓
- cos(2δ + 2π/3) = -0.622354 ✓
- cos(2δ + 4π/3) = -0.366692 ✓
- sqrt ratio (k→1): (1+0.989)/(1-0.622) = 5.267 → mass ratio = 27.7× ✓

**But D1's key claim that "k→1 gives max ratio" is FALSE.** The ratio grows as k increases:
- At k = 1.0: 27.7×
- At k = 1.25: 101× 
- At k = 1.5: 1,396×
- At k = 1.592: 79,861× (matches actual up-type hierarchy!)
- Pole at k = 1.607: ratio → ∞

The formula can produce any mass ratio by tuning k near the pole, where the up-quark denominator (1+k·cos₁) → 0.

---

## 3. CORRECT FORMULA ANALYSIS

Using Zenczykowski's published formula `m = M·(1 + √2·k·cos(2δ + 2πn/3))`:

### With δ = 2/27 (fixed):
| k | t/c ratio | c/u ratio | t/u ratio |
|---|-----------|-----------|-----------|
| 0.5 | 2.3 | 1.3 | 3.0 |
| 1.0 | 5.0 | 4.0 | 20.0 |
| 1.1 | 5.9 | 13.5 | 79.7 |
| 1.135 | 6.3 | 396 | 2,491 |
| 1.136 | 6.3 | 2,588 | 16,305 |

**Key problem at δ=2/27**: The top/charm ratio maxes out at ~6.3× while actual is 136×. The charm/up ratio can be made arbitrarily large by approaching the pole at k=1.136, but the top/charm ratio is structurally limited to ~6.3× at this δ.

The formula at δ=2/27 is OVERCONSTRAINED: with only k as a free parameter, it cannot simultaneously satisfy t/c=136 and c/u=588.

### Positivity constraint:
Masses must be positive: 1 + √2·k·cos_n > 0 for all n. At δ=2/27, cos_min=-0.622, giving k_max = 1/(√2·0.622) = 1.136. At k=1.136, the up quark mass → 0 (the pole). For the required t/u=79,861, k must be within 0.003% of the pole — extreme fine-tuning.

---

## 4. CAN THE FORMULA FIT WITH FREE δ?

**Yes — with a very different δ.** The formula `m = M·(1 + √2·k·cos(2δ + 2πn/3))` has 3 parameters (M, k, δ) for 3 observables (m_t, m_c, m_u). A perfect fit is mathematically guaranteed if a geometrically consistent solution exists.

I verified the geometric identities: the required cos values satisfy all 120°-spacing constraints (sum=0, sum of squares=1.5, cross sum=-0.75). **A perfect fit exists.**

Required parameters:
| Parameter | Value for exact fit | Zenczykowski's value |
|-----------|--------------------|--------------------|
| δ | 0.00320 rad (0.18°) | 0.07407 rad (4.24°) |
| k | 1.3987 | ~1.25 (at μ=2 GeV) |
| M | scale factor | — |

**δ differs by a factor of 23× (or 96%)** from Zenczykowski's claimed δ_U = δ_L/3 = 2/27.

---

## 5. DOES THE ZENCZYKOWSKI PAPER USE DIFFERENT PARAMETERS?

From the actual paper (arXiv:1301.4143):

> "Experiment suggests that at the low-energy scale the relevant phase parameters δ_f take on possibly exact values of δ_L = 3δ_D/2 = 3δ_U = 2/9."

So δ_U = 2/27 ≈ 0.074 rad — exactly what D1 tested. The paper also states:

> "Using quark mass values appropriate at μ = 2 GeV, one obtains k_D ≈ 1.08 (k_U ≈ 1.25). If a higher energy scale μ = M_Z is taken, even larger values are obtained, i.e. k_D = 1.12 and k_U = 1.29."

The paper's values (δ_U=2/27, k_U≈1.25) give t/c≈6.3, t/u≈101 — far from actual quark hierarchy.

The paper also notes:
> "Going from μ=2 GeV towards the low energy scale leads to smaller values of k_D and k_U."

But smaller k makes the fit WORSE for the mass hierarchy. The paper's δ=2/27 claim is for the "low-energy scale" — the same scale where quark masses have their largest hierarchy. The δ that actually fits quark masses (~0.003 rad) is near zero, not 2/27.

### Running masses at M_Z scale:
The hierarchy is slightly different at M_Z (t/c≈277, c/u≈487), but this changes δ requirements only marginally. The fundamental mismatch (δ≈0 vs δ=2/27) persists at any scale.

---

## 6. IS THE AGENTS.MD FORMULA AN OVERSIMPLIFICATION?

**Yes, severely.** The AGENTS.md formula (and Claude's hierarchy analysis) both omit:
1. The √2 factor in the cosine term
2. The correct functional form (linear vs quadratic in cos)

Claude's analysis states the formula as `√m_n = A + R·cos(δ + 2πn/3)` and as `m_n = μ·(1 + 2k·cos(2δ + 2πn/3))` — neither matches Eq.(4) from the actual paper.

However, Claude's analysis correctly notes "k = R/A, and Q=2/3 requires k = √2 (not k = 1 as in Zenczykowski's convention)" — showing awareness that the parametrization conventions differ.

**The AGENTS.md file itself doesn't actually contain the formula** — it just references the missing external preprint. The formula appears only in D1's analysis and Claude's analysis, both with errors.

---

## 7. THE DUCK METHOD VERDICT

| Claim | Assessment |
|-------|-----------|
| "Formula cannot fit quark masses" | FALSE (can fit with free δ) |
| "Max mass ratio ~28× at k=1" | TRUE for D1's wrong formula |
| "Ratio can't reach 79,861×" | FALSE (can reach with k near pole) |
| "δ_U=2/27 is wrong" | CORRECT — required δ≈0.0032 |
| "Formula needs additional parameter" | FALSE — 3 params fit 3 masses |

### Bottom line:
D1 is **80% correct** in spirit but used the wrong formula and oversimplified the parameter space. The Zenczykowski formula CAN fit quark masses, but only by abandoning Zenczykowski's own δ=2/27 claim. The required δ is near zero (0.0032 rad), not 2/27 (0.074 rad). The formula at δ=2/27 is geometrically unable to reproduce the top/charm ratio of 136× — it maxes out at ~6.3× regardless of k.

The real problem is not that the Z3 parametrization fails — it's that **Zenczykowski's specific delta values are wrong for quarks**. The geometric structure (Z3 120° spacing) can accommodate quark masses with different parameters.

---

## 8. IMPLICATIONS FOR PF

1. **The Z3 geometry is sound** — it can mathematically accommodate quark masses. The 120° resonance spacing is flexible enough.

2. **Zenczykowski's δ hierarchy (1:2:3) is empirically wrong for quarks.** The required δ_U ≈ 0.0032 is ~23× smaller than δ_L/3 = 0.074. This challenges the "exact rational phase hierarchy" claim.

3. **The formula is a fit, not a prediction.** With 3 free parameters for 3 masses, any fit is exact. The interesting question is whether PF can REDUCE the degrees of freedom — e.g., deriving k from gauge couplings, or δ from symmetry principles.

4. **The AGENTS.md and Claude analysis need correction** — the formula should be updated to match Zenczykowski's Eq.(4) with the √2 factor.

5. **Recommendation**: If exploring quark masses through Z3 resonance, treat δ and k as free parameters to be derived, not as fixed values. The PF derivation pathway (Claude analysis §3.2) should target the actual best-fit values (δ≈0.003, k≈1.40), not Zenczykowski's claimed values.

---

*Methodology: Verified against Zenczykowski arXiv:1301.4143v2 (retrieved from arxiv.org). Full PDF downloaded and text-extracted via pdftotext. All numerical computations performed in Python with double precision. Duck method applied throughout — every claim tested against actual paper and numerical computation.*
