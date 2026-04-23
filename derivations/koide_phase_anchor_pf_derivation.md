# Koide Phase Anchor: Can PF Derive δ₀ ≈ 2/9 Natively?
**Agent 4 — Claude WSL**  
**Date**: 2026-04-04  
**Target question**: Can the Propagation Framework derive δ₀ ≈ 2/9 without borrowing Rivero's cos(9δ) mechanism?  
**Reads**: `koide_phase_rivero_bridge_audit.md`, `koide_phase_delta_0_gap.md`, `koide_geometric_equivalence.md`, `g3_casimir_weinberg_angle.md`

---

## 1. What I Am Actually Trying to Derive

The Koide parameterization: √m_n = A + R·cos(2πn/3 + δ₀), n = 0,1,2

PF already explains why R/A = √2 (the amplitude). The open question: why does the vacuum sit at δ₀ ≈ 2/9 ≈ 0.22222 rad?

This is NOT the same as asking why the potential has period 2π/9. The phase δ₀ is the **global rotation** of the whole lepton triple on the Koide cone. Z₃ symmetry is preserved — all three masses are related by 120° rotation around δ₀. So spontaneous Z₃ breaking is NOT the right mechanism here.

---

## 2. Correcting a Common Confusion

The FIVE_AGENT_COORDINATION brief asks whether "Z₃ chiral structure spontaneously selects a preferred phase." This needs careful unpacking.

**The Koide formula IS Z₃-symmetric.** The parameterization √m_n = A + R·cos(2πn/3 + δ₀) assigns mass√ values that differ by 120° rotations — the triple is Z₃-invariant by construction. δ₀ is not a Z₃ asymmetry; it is the **orientation** of the Z₃-symmetric triple within the larger phase space.

Therefore:
- Spontaneous Z₃ breaking → selects WHICH of 3 symmetric vacua → NOT what we need
- We need a mechanism that pins the orientation of an already Z₃-symmetric structure to δ₀ = 2/9

The correct question is: **does PF's coherence functional F_C have a preferred orientation at δ₀ = 2/9 for Z₃-symmetric mass triples?**

---

## 3. What PF Currently Gives (Exact Results from Prior Audits)

From `koide_phase_rivero_bridge_audit.md` (Codex, 2026-03-21):

**Theorem 1 (exact)**: Any PF-compatible reduced phase potential must have the form:
$$V(\delta) = a_0 + \sum_{n \geq 1} \left(a_n \cos(3n\delta) + b_n \sin(3n\delta)\right)$$

With reflection symmetry V(δ) = V(-δ): the sine terms vanish.

**Theorem 2 (exact)**: PF determines the periodicity class (cos(3nδ) tower) but NOT which harmonic n dominates. The n=3 selection (cos(9δ)) is not yet PF-native.

**From Wave 5 numerical audit** (`koide_phase_delta_0_gap.md`, Section 7):

| Quantity | Value |
|----------|-------|
| δ_Koide (PDG 2024) | 0.222229631... |
| 2/9 exact | 0.222222222... |
| gap (δ_Koide − 2/9) | 7.41 × 10⁻⁶ |
| m_τ measurement uncertainty contribution | 2.58 × 10⁻⁴ rad |
| gap / uncertainty | **0.029** |

**Conclusion**: δ_Koide = 2/9 is consistent within 0.029σ of m_τ measurement precision. This is effectively an identity for the purposes of PF derivation.

**sin²θ_W ≠ 2/9 algebraically**:
- sin²θ_W (Casimir) = (√19-3)(√19-√3)/16 ≈ 0.22310
- Test: 56√3 − 9√57 = 29.046... ≠ 29.000
- These are algebraically distinct.

---

## 4. The 2/9 Cluster: Are These Three Manifestations of One Root?

The numbers δ_Koide ≈ 2/9, sin²θ_W ≈ 0.22310, 2/9 = 0.22222 cluster within 0.4%.

**Sharp result from Wave 5**: The gap B = sin²θ_W − δ_Koide = 8.72 × 10⁻⁴ satisfies:
$$\text{gap B} \approx \alpha \cdot (1 - x_{+}(3/2)) \cdot x_{+}(3/2)^2 \quad \text{(0.317% error)}$$

where x_+(3/2) is the Casimir root at spin j=3/2.

**Interpretation**: If this α-correction formula is real, then:
$$\sin^2\theta_W = \frac{2}{9} + O(\alpha)$$

i.e., **2/9 is the tree-level PF prediction, and the Casimir polynomial gives the one-loop correction at O(α)**.

This would mean δ_Koide and sin²θ_W share a common origin at x* = 2/9, with sin²θ_W shifted by a small radiative correction.

**Status of this interpretation**: Numerically compelling, not yet derived. The identification of the α correction with specific Casimir roots is an observation from a numerical scan, not a proof. This is the **sharpest formal target for this issue**.

---

## 5. The n=3 Problem: Where Does "9" Come From?

The gap between what PF has (cos(3nδ) for any n) and what's needed (n=3 specifically) can be stated as: **PF gives one factor of 3; the 9 needs a second factor of 3.**

**The PF structure that might provide the second factor:**

The 3-step walk closure is 3-periodic: the internal phase cycle is 0→1→2→0. This is the source of the first factor of 3 (the Z₃ periodicity, Theorem 1).

**New observation**: A natural PF observable that is invariant under single walk steps but sensitive to the complete 3-cycle would be a **product over all three steps of the cycle**. If such a product observable is defined, its Fourier content would involve cos(3δ) composed three times, yielding cos(9δ).

Concretely: if the single-step phase factor is e^{iδ}, then the 3-step return amplitude is ∑_{k} e^{i(δ + 2πk/3)} for k=0,1,2, which is proportional to e^{i3δ} (up to the Z₃ sum). A three-fold product of such 3-step observables would give:

$$\left(\sum_{k=0}^2 e^{i(3\delta + 2\pi k)}\right)^3 \sim e^{i9\delta}$$

This is qualitatively the same as Rivero's det(M)³ mechanism: Rivero uses a CUBIC power of a 3×3 determinant; PF has a CUBIC product of a 3-step walk return. Both mechanisms produce the factor 3×3 = 9 from a double application of the Z₃ structure.

**Key comparison:**

| Mechanism | Source of first "3" | Source of second "3" |
|-----------|---------------------|----------------------|
| Rivero W₃ | SU(3) matrix det(M) | Power ³ in superpotential |
| PF (proposed) | Z₃ walk periodicity | Product over 3-cycle |
| Connection | Same? | Same? |

If the PF 3-cycle product and Rivero's det³ are the same physics in different language, then PF and Rivero are deriving the same selection rule from different axioms.

**Status**: Not yet a derivation. The qualitative match is there. The precise PF observable needs to be specified.

---

## 6. The Coherence Functional Angle

Can F_C (PF coherence functional) penalize phases away from δ₀ = 2/9?

From the literature in the repo, F_C maximizes mutual information across the propagation channels. For the phase sector, a phase potential derived from F_C would take the form:

$$V_{F_C}(\delta) = -F_C[\text{mass triple at phase } \delta]$$

For this to select δ₀ = 2/9, we need F_C to have a unique maximum at δ = 2/9 mod 2π/3.

**What would give this**: If F_C is monotonically related to the overlap between the mass-space vector and the fundamental domain of the PF walk lattice, and if the fundamental domain has a natural orientation at 2/9 relative to the equal-mass axis, then F_C would peak at δ₀ = 2/9.

**The challenge**: PF currently does not have a specific prediction for the orientation of the fundamental domain relative to the Koide cone. The coherence functional is defined up to the symmetry class, which gives cos(3nδ) but not the constant.

**The gap**: Specifying F_C precisely enough to derive a phase orientation requires pinning the "zero of the phase" in the PF internal sector. This is equivalent to the scheme-dependence problem in the Weinberg angle: PF derives dimensionless ratios, but the overall phase orientation is like choosing a reference angle.

---

## 7. The α Connection: Most Promising Near-Term Target

The numerical observation from Wave 5:
$$\text{gap B} = \sin^2\theta_W - \delta_{\text{Koide}} \approx \alpha \cdot (1 - x_+(3/2)) \cdot x_+(3/2)^2$$

requires careful interpretation before declaring it a derivation.

**What x_+(3/2) is**: The Casimir eigenvalue root at spin j = 3/2:
$$x_+(3/2) = \frac{-C_2(3/2) + \sqrt{C_2(3/2)^2 + 4C_2(3/2)}}{2}, \quad C_2(3/2) = \frac{15}{4}$$

$$= \frac{-15/4 + \sqrt{(15/4)^2 + 15}}{2} = \frac{-15 + \sqrt{465}}{8} \approx \frac{-15 + 21.587}{8} \approx 0.823$$

**The scan result**: gap B ≈ α × 0.823² × (1 - 0.823) ≈ α × 0.677 × 0.177 ≈ α × 0.120 ≈ 8.74 × 10⁻⁴

vs actual gap B = 8.72 × 10⁻⁴. Remarkably close (0.23% error).

**What this means physically**: The Casimir root at j=3/2 appears in the correction. Spin 3/2 is the next half-integer spin after the spin-1 and spin-1/2 used in the Weinberg angle derivation. In PF terms, the 3-step walk has an effective representation content that includes j = 3/2 as a composite of three j = 1/2 steps.

**Updated interpretation after T-021**: the earlier RG sentence does not survive the convention audit. No legitimate Standard Model definition in this pass supports a crossing near μ ≈ 98 GeV, so this gap-B lead cannot currently be framed as running from a "Koide scale." If the α-correction structure is real, it will need a different PF-native explanation.

**Status**: This α-correction formula is the strongest numerical bridge between the two quantities. Whether it has a PF-native derivation is the key open question. It merits a dedicated bounded pass.

---

## 8. Formal Status Summary

Answering each question from FIVE_AGENT_COORDINATION.md:

| Question | Answer | Status |
|----------|--------|--------|
| Does Z₃ SSB select δ₀? | No — Koide formula IS Z₃-symmetric, SSB wrong mechanism | ESTABLISHED NO-GO |
| Is δ_Koide = 2/9 derivable? | δ_Koide = 2/9 to 0.029σ, effectively exact | EMPIRICAL TARGET |
| Do δ_Koide, sin²θ_W, 2/9 share one PF root? | Probably — connected via O(α) correction | CONJECTURAL (0.60) |
| Can F_C select δ₀? | PF gives cos(3nδ) tower but not orientation | GAP PERSISTS |
| Can cos(9δ) be replaced by PF-native suppression? | Qualitative match via 3-cycle product; not derived | PROMISING DIRECTION |
| Can Rivero's W₃ and PF 3-cycle be identified? | Structural match; not proven | BOUNDED QUESTION |

---

## 9. What Would Actually Close This Gap

**Route 1 (cleanest)**: Prove that 2/9 is a natural output of the Casimir polynomial framework at the leading approximation, and that Rivero's cos(9δ) mechanism and the α-correction formula are the same thing. This requires:
1. Show that the Koide phase δ₀ = 2/9 is the "tree level" value before loop corrections
2. Show that the Casimir polynomial gives sin²θ_W = 2/9 + O(α) when spin-3/2 contributions are included
3. This would make both quantities derivable from a single x* = 2/9

**Route 2 (PF-native)**: Define a precise PF 3-cycle product observable analogous to Rivero's det(M)³. If the 3-step walk amplitude at a fixed phase δ, when taken as a 3-fold product, generates a cos(9δ) term that dominates over cos(3δ) (via cancellation of lower harmonics), this would be a PF-native derivation. The required structure is:
- A PF observable O(δ) ∝ (-1/2 + cos(3δ)/√2) [this is f(δ) from Rivero, already PF-native]
- Show O(δ)³ in the coherence functional generates the dominant cos(9δ) minimum
- AntiGravity's question (from freeze record): "Can Z₆ lifted-spinorial closure produce effective inverse-weight structure analogous to Rivero's Σ 1/g_k²?" — this is the most concrete bounded question

**Route 3 (admit the boundary)**: Axioms 1-3 fix the Koide amplitude Q = 2/3 and the cos(3nδ) symmetry class. The phase anchor δ₀ = 2/9 requires additional dynamics — specifically, either Rivero's superpotential structure or a yet-specified PF-native nonlinear 3-cycle observable. This additional structure is not contained in Axioms 1-3 alone.

---

## 10. Recommendation

**Do not attempt to derive cos(9δ) from bare Z₃ symmetry.** The bare Z₃ gives only the tower. The second factor of 3 needs a nonlinear composite mechanism.

**Do not use the naive `f(δ)^3` test as the next step.** Since the cube is monotone on the real line, `f(δ)^3` has the same extrema as `f(δ)`, so it cannot move the minimum from the `cos(3δ)` locations to `δ₀ = 2/9`.

**The bounded question to assign next** is narrower and honest:
- can a PF-native 3-cycle observable produce an effective `cos(9δ)` selector after lower-harmonic cancellations, rather than by the trivial cube of `f(δ)`?
- or can the `α`-scale correction candidate be upgraded from scan observation to an actual symbolic derivation?

**The α-correction target is independently valuable**: Even without cos(9δ), the observation gap B ≈ α · x_+(3/2)² · (1 − x_+(3/2)) deserves a dedicated verification pass using symbolic computation. If confirmed, it directly connects the Koide phase to the Weinberg angle via a one-loop correction — a significant structural result regardless of the underlying mechanism.

---

## 11. What I Cannot Derive Here

- A first-principles derivation of δ₀ = 2/9 from Axioms 1-3 alone: **not available, honest no-go**
- A proof that the PF 3-cycle product and Rivero's det³ are identical: **would require spelling out both mechanisms in the same mathematical language**
- A proof that F_C has a unique maximum at δ₀ = 2/9: **requires a specific model for F_C in the phase sector**

---

*Written by Claude WSL, 2026-04-04*  
*Role: Agent 4 — Koide Phase Anchor*  
*Status: ANALYSIS COMPLETE — No new derivation, significant gap clarification*  
*Key contribution: SSB no-go, 2/9 precision established, α-correction route identified, nonlinear 3-cycle structure isolated as the right class of missing ingredient*  
*Repo confidence unchanged; this file does not alter the live `CLAIMS.md` / `ACTIVE_ISSUES.md` status language for Issue #5.*
