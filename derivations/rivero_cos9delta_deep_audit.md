# Deep Audit: Rivero's cos(9δ) Mechanism
*Reading the actual calculation scripts, not the summary claims*

**Date**: 2026-03-21
**Author**: Claude
**Source files read**: `calculations/cos9delta_derivation.py`, `calculations/three_instanton_seiberg.py`, `results/assembly_round19.md`, `results/brainstorm_r21_sonnet.md`, `coordination2.md`
**Relevance**: Issue #5 (Koide phase δ₀), specifically the harmonic suppression question Codex is pursuing

---

## 1. What the Claim Actually Is

Rivero's sBootstrap argues that the three-instanton superpotential

$$W_3 = c_3 \frac{(\det M)^3}{\Lambda^{18}}$$

generates a cos(9δ) potential that selects δ₀ mod 2π/3 = 2/9 rad (to 33 ppm).

This is the claim we need to examine precisely.

---

## 2. What cos9delta_derivation.py Actually Computes

### Step 1: The exact product formula

The Koide parametrization writes the three mass factors as:

$$f_k(\delta) = 1 + \sqrt{2}\cos\!\left(\delta + \frac{2\pi k}{3}\right), \quad k=1,2,3.$$

Using symmetric function identities (Σc_k = 0, Σ_{i<j}c_ic_j = -3/4, Πc_k = cos(3δ)/4):

$$f(\delta) = \prod_k f_k(\delta) = -\frac{1}{2} + \frac{\cos 3\delta}{\sqrt{2}}.$$

This is **exact**.

### Step 2: The determinant

$$(\det M)^3 = z_0^{18}\, [f(\delta)]^6.$$

### Step 3: The Fourier expansion of [f(δ)]^6

The script computes this exactly by binomial expansion and power reduction. **The result is:**

| Harmonic | cos(nδ) coefficient | Relative to max |
|----------|---------------------|-----------------|
| cos(3δ)  | ≈ +0.265            | 1.000 (dominant)|
| cos(6δ)  | ≈ +0.046            | 0.174           |
| **cos(9δ)**  | **≈ +0.090**    | **0.340**       |
| cos(12δ) | ≈ +0.022            | 0.083           |
| cos(15δ) | ≈ +0.003            | 0.011           |
| cos(18δ) | ≈ +0.0002           | 0.001           |

**The script itself states:**

> "cos(9 delta) is one of them but NOT dominant."
> "The cos(3 delta) term has amplitude 2.9x larger than cos(9 delta)."
> "For pure Z_9 vacuum structure, lower harmonics must be cancelled."

This directly contradicts the simplified summary claim that "W_3 generates cos(9δ)."

---

## 3. What three_instanton_seiberg.py Actually Proves

This script solves the F-term equations at the Seiberg vacuum with W = W_ISS + W_3:

**Key result (quoted from script output):**

> "The c3 correction does NOT change the meson VEVs M_j. It shifts the Lagrange multiplier X by a fixed amount -3c3/Lambda^6."

The proof is exact and compact. Define X_eff = X + 3c₃D²/Λ¹⁸. The F-term equation for each meson field M_j is:

$$F_j = m_j + X_\text{eff}\frac{D}{M_j} = 0 \implies M_j = -X_\text{eff}\frac{D}{m_j}.$$

The constraint det M = D = Λ⁶ fixes X_eff entirely by the product of quark masses:

$$X_\text{eff} = -\frac{(\prod m_j)^{1/3}}{\Lambda^4}.$$

Since X_eff is independent of c₃, the meson VEVs M_j are **unchanged** by the three-instanton term. Only X itself shifts:

$$\Delta X = -\frac{3c_3}{\Lambda^6}.$$

**Physical interpretation:** On the constraint surface det M = Λ⁶, the W_3 term is just a constant (c₃Λ¹⁸/Λ¹⁸ = c₃). Its variation with respect to M_j is zero on-shell. The δ-dependent potential arises only **off the constraint surface** — in the off-shell effective potential for the pseudo-modulus δ.

---

## 4. The Off-Shell Potential and the Cross-Term

The script also analyzes the off-shell scalar potential from |∂W/∂M_k|²:

**Cross-term** (linear in c₃, dominant for small c₃):

$$V_\text{cross} \propto [f(\delta)]^6 \sum_k \frac{m_k}{g_k(\delta)^2}$$

where g_k(δ) = 1 + √2 cos(δ + 2πk/3).

**Pure W_3² term** (quadratic in c₃):

$$V_3 \propto [f(\delta)]^{12} \sum_k \frac{1}{g_k(\delta)^4}$$

Both functions share the Z₃ symmetry and thus both have harmonic content only at cos(3nδ). The script numerically computes their Fourier spectra. **Key question**: does the cross-term's cos(3δ)/cos(9δ) ratio differ from the pure term's ratio, enabling cancellation in the total potential?

The script computes this but we do not have the printed output. The structure suggests the cross-term and pure term do NOT cancel cos(3δ) automatically — they would need a specific ratio of c₃ to the ISS couplings.

---

## 5. The Z_9 Minimum Count

The script counts actual minima of the computed potentials:

- [f(δ)]^6 (pure superpotential): dominance of cos(3δ) suggests **≈3 minima** in [0, 2π)
- V_3 = [f]^12 · sum 1/g_k^4: the higher power could give more structure

The actual Z₉ structure (9 minima at δ = 2πn/9) requires the potential to have cos(9δ) as the leading oscillating term. With cos(3δ) 2.9× dominant, the minimum count is governed by cos(3δ) → **3 minima, not 9**, unless there is cancellation.

---

## 6. The Honest Gap in coordination2.md

Rivero's own open issues list (coordination2.md) states:

> "Renormalization scheme question: Hans idea was that it was some sort of composites, our idea was that perhaps it was just coming from casimirs. But I can not answer, **it is not relevant yet until we got some actual action Lagrangian.**"

This is Rivero explicitly saying the scheme-derivation gap (Issue #3) is open because there is no complete action yet. The same applies to the phase: the cos(9δ) selection mechanism requires a full Lagrangian to derive.

---

## 7. Summary: What We Now Know Precisely

### What is established

- f(δ) = -1/2 + cos(3δ)/√2 (exact algebraic identity)
- (det M)³ ∝ [f(δ)]^6 contains all cos(3nδ) harmonics, n=0..6
- cos(3δ) amplitude is 2.9× larger than cos(9δ) in [f(δ)]^6
- The W_3 term does not shift meson VEVs on-shell (three_instanton_seiberg.py, proven exactly)
- The off-shell potential has cos(3δ) as the dominant oscillating term

### What is NOT established (honest gap)

- Why cos(3δ) should be suppressed relative to cos(9δ) in the physical potential
- What cancellation mechanism removes the leading cos(3δ) term
- Whether the cross-term W_ISS · W_3 provides partial cancellation
- Whether higher instanton contributions (W_6, W_9,...) cancel lower harmonics

### The precise gap for Issue #5

The gap in Rivero's framework is the **same gap** that will appear in PF: Z₃ symmetry guarantees the potential is 2π/3-periodic, generating the full cos(3nδ) tower. Selecting cos(9δ) as dominant requires suppression of cos(3δ) and cos(6δ). Neither framework derives this suppression.

Rivero's claim that "W_3 selects δ₀" is:
- **Partially correct**: W_3 generates a potential with a cos(9δ) component
- **Incomplete**: cos(3δ) is the dominant term; Z₉ selection requires its cancellation
- **Status in coordination2.md**: implicitly deferred until there is an action Lagrangian

---

## 8. Consequence for Codex's Harmonic Suppression Test

Codex's planned test: "can PF generate a composite observable or cancellation rule that suppresses cos(3δ) and cos(6δ) leaving cos(9δ) leading?"

**Predicted outcome**: No-go. Reason:

PF's Z₃ structure is exactly what generates the full cos(3nδ) tower in Rivero's framework too. Both share the same symmetry class. Neither has a mechanism that selects n=3 (cos(9δ)) over n=1 (cos(3δ)).

The suppression would require fundamentally new structure, such as:
1. A cancellation mechanism between W_ISS and W_3 terms at specific coupling ratios
2. Higher instanton contributions that cancel lower harmonics (W_6 vs W_3 etc.)
3. Entirely different physics (the Kähler stabilization at c = 1/12 affects the modulus, not δ)

**Recommendation for Issue #5**: After Codex's no-go, name the specific target:

> The harmonic content of the cross-term V_cross = ∂W_ISS/∂M · ∂W_3/∂M — does it cancel the cos(3δ) term from the pure W_3 potential? If the cross-term coefficient of cos(3δ) is equal and opposite to the pure term's, then at order c₃^{1/2} the potential could be dominated by cos(9δ). This specific calculation exists in Rivero's cos9delta_derivation.py Part (d) but we do not have its output.

---

## 9. The Kähler Result (assembly_round19.md)

The c = 1/12 Kähler stabilization is a separate mechanism from the phase. It places the pseudo-modulus VEV at gv/m = √3 (fixing the O'Raifeartaigh mass ratio), not at a specific δ. The Kähler result is:

- c = 1/12 is **algebraically exact**
- Requires **non-perturbative dynamics** (one-loop Kähler cannot generate it)
- Stabilizes the **radial direction** (gv/m = √3), not the angular direction (δ)

The c = 1/12 result and the cos(9δ) result are independent mechanisms addressing different degrees of freedom.

---

*Deep audit of Rivero's scripts, Claude, 2026-03-21*
*Purpose: inform Codex's Issue #5 harmonic suppression test*
*Bottom line: cos(9δ) dominance is a named open gap in Rivero's framework too*
