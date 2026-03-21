# Issue #3: Candidate Minimal Coherent Representation Principle
*Attempting to derive the spin-pair selection from Axiom 3*

**Date**: 2026-03-21
**Author**: Claude (for Codex audit)
**Task**: Derive the principle from PF Axiom 3 that singles out the lowest half-integer Z₃-survivor and lowest integer Z₃-annihilated sector, completing the spin-pair identification
**Status**: CANDIDATE DERIVATION — one step closes cleanly, one remains a gap
**Builds on**: `g3_spin_pair_identification.md`, `topological_weight_from_propagation.md`

---

## 1. The Target

From `g3_spin_pair_identification.md` (Codex audit, cef9043):

> Derive a principle of minimal coherent representation content from PF Axiom 3 that singles out the lowest half-integer survivor and lowest integer annihilated sector under the Z₃ step action.

If this principle exists and follows from Axiom 3, the spin pair $(s=1/2, s=1)$ is derived from PF, closing the last gap in the spin identification step of Issue #3.

---

## 2. Setup: What Axiom 3 Gives

From `topological_weight_from_propagation.md` (DERIVED, Axiom 3 + 3D topology):

Axiom 3 requires **phase closure**: a stable structure's propagation mode must return to its initial state after one cycle. In a 3D medium ($\pi_1(\text{SO}(3)) \cong \mathbb{Z}_2$), this gives exactly two closure classes:

- **Bosonic class** (w=1): $2\pi$ rotation closes the phase. All integer-spin representations belong here: $j = 0, 1, 2, 3, \ldots$
- **Fermionic class** (w=2): $4\pi$ rotation closes the phase. All half-integer-spin representations belong here: $j = 1/2, 3/2, 5/2, \ldots$

Within each class, every value of $j$ satisfies the topological closure condition. Axiom 3's phase closure constraint partitions representations into two classes but **does not yet single out a specific $j$ within each class**.

The Casimir eigenvalue for spin $j$ is $C_2(j) = j(j+1)$. This grows with $j$: it is the "phase content" or "rotational complexity" of the representation.

---

## 3. The j=0 Exclusion — A Clean Formal Step

Before deriving the minimality principle, there is one exclusion that follows **formally** from the structure of the Casimir equation:

The eigenvalue equation $x^2 + C_2 x - C_2 = 0$ at $j=0$ gives $C_2 = 0$:

$$x^2 = 0 \implies x_+ = 0.$$

Setting $x_+(j=0) = M_Z^2/m^2$ would give $M_Z = 0$ — a massless state. The Weinberg angle ratio is:

$$R = 1 - \frac{x_+(\text{fermion})}{x_+(\text{boson})},$$

and if $x_+(\text{boson}) = 0$, the ratio is undefined ($R = -\infty$).

**Therefore**: $j=0$ is **excluded from the bosonic Casimir sector by the self-consistency of the derivation** — not by an external physical input, but because it makes $R$ undefined. The bosonic spin must be $j \geq 1$.

This step requires no Axiom 3 argument. It is a formal exclusion from within the Casimir derivation itself.

---

## 4. The Minimality Argument — Phase Complexity and Axiom 3

Having excluded $j=0$ from the bosonic sector, the remaining question is: why take $j=1$ (not $j=2, 3, \ldots$) for bosons, and why take $j=1/2$ (not $j=3/2, 5/2, \ldots$) for fermions?

### 4.1 A Candidate Principle

**Candidate (Minimal Phase Content)**: Among all representations in a topological class satisfying the closure constraint, Axiom 3 selects the one with the **minimum Casimir eigenvalue $C_2$**.

Axiom 3 says: stable structures are self-reinforcing coherent loops. A loop with higher Casimir eigenvalue carries more angular-momentum phase content. In a dispersive medium (implied by Axiom 1: propagation can fail), higher phase content requires more precise phase alignment to close coherently — it is less robust, more easily dispersed.

The minimum-$C_2$ representation in each class is the most robust against dispersion: it needs the least precise phase alignment to maintain coherent closure.

Under this principle:
- Fermionic class: minimum $C_2$ is at $j=1/2$ with $C_2 = 3/4$.
- Bosonic class: minimum non-trivial $C_2$ (with $j \geq 1$, after $j=0$ exclusion) is at $j=1$ with $C_2 = 2$.

This gives the unique pair $(j=1/2, j=1)$.

### 4.2 The Casimir Eigenvalues

$$C_2(1/2) = \frac{3}{4}, \quad C_2(1) = 2, \quad C_2(3/2) = \frac{15}{4}, \quad C_2(2) = 6, \ldots$$

Each step up in $j$ increases $C_2$ by $j + (j+1) = 2j+1$ (the next increment). The gap grows. The lowest representatives are the minimum-phase-complexity states in their class.

### 4.3 Why "Minimum Phase Content = Maximum Coherence"

In a propagation medium, a stable mode closes a loop in phase space. The probability of completing the loop coherently decreases with the amount of phase that must be accumulated. High-$j$ representations accumulate more phase per rotation.

Formally: if the probability of maintaining phase coherence per unit rotation is $p < 1$ (from Axiom 1: propagation is not perfect), then the probability of completing a $j=1/2$ loop is $p^{4\pi/\Omega_0}$ and the probability of completing a $j=3/2$ loop requires more precise alignment per rotation, generically $p^{4\pi/\Omega_0}$ for the topological closure but with more stringent phase requirements between turns.

This argument captures the physical intuition but is not yet a formal derivation: the "phase alignment per rotation" is not precisely defined from the PF axioms.

---

## 5. Honest Assessment

### What is formally closed

1. **j=0 exclusion** (Section 3): $j=0$ makes $R$ undefined. Excluded by internal consistency of the Casimir derivation. This is a derivation.

2. **Topological class partition** (from prior work): bosonic ($j$ integer) and fermionic ($j$ half-integer) from $\pi_1(\text{SO}(3)) \cong \mathbb{Z}_2$. This is derived.

### What is still a gap

3. **Minimality principle** (Section 4): the argument that Axiom 3 selects minimum-$C_2$ within each class is **physically motivated but not formally derived**. The specific gap:

> Show formally from Axiom 3 that coherent stable structures correspond to the minimum Casimir eigenvalue in their topological class.

The physical picture (minimum phase content = maximum stability against dispersion) is correct but needs to be derived from the axiom text, not just motivated by it.

### The remaining missing piece is small but precise

The entire spin identification reduces to one formal step:

$$\text{Axiom 3 + dispersion} \;\Rightarrow\; \text{minimum-}C_2 \text{ selection within each class.}$$

If this can be derived (even as a stability bound on the coherence condition), the full chain becomes:

$$\underbrace{\text{Axiom 3 + 3D}}_{\text{derived}} \;\Rightarrow\; (w=2, w=1) \;\Rightarrow\; \underbrace{j=0 \text{ excluded}}_{\text{derived}} \;\Rightarrow\; \underbrace{\text{min-}C_2}_{\text{candidate}} \;\Rightarrow\; (j=1/2, j=1) \;\Rightarrow\; R = 0.22310.$$

---

## 6. What Would Constitute a Derivation

A formal derivation of the minimum-$C_2$ principle would take one of these forms:

**Form 1 (Stability argument):** Show that in the PF propagation medium, the amplitude for a spin-$j$ mode to complete a closed loop decreases with $j$ for $j > j_{\min}$ in each class, so the minimum-$j$ mode is the only one that can form a stable (non-dispersive) structure.

**Form 2 (Entropy/information argument):** Show that Axiom 3's coherence condition, applied to the representation content, minimizes a free energy or information measure, and that this is minimized at $j=j_{\min}$.

**Form 3 (Uniqueness argument):** Show that there is a unique self-consistent solution to the Casimir equation in each topological class when the equation is combined with the PF's N=3 phase-walk constraint, and that self-consistency forces $j=1/2$ and $j=1$.

Form 3 is the most PF-native and would be the tightest derivation. It would require showing that the N=3 3-step walk, when composed with the Casimir self-consistency, uniquely selects the lowest-$j$ modes.

---

## 7. Summary

| Step | Status | Notes |
|------|--------|-------|
| Two topological classes (bosonic/fermionic) | ✅ Derived | Axiom 3 + 3D topology |
| j=0 excluded from bosonic Casimir sector | ✅ **Derived** | R undefined if x₊(boson)=0 |
| Minimum-C₂ selects j=1/2 (fermionic) | ⚠️ **Argued** | Physical motivation from "min phase = max stability" |
| Minimum-C₂ selects j=1 (bosonic, j≥1) | ⚠️ **Argued** | Same principle |
| Full chain: Axiom 3 → (1/2, 1) → R=0.22310 | ❌ Not yet closed | Missing: formal minimum-C₂ derivation |

**New formal result**: the $j=0$ exclusion is clean and is a derivation.
**Remaining gap**: minimum-$C_2$ principle from Axiom 3 — physically motivated, not yet formal.

---

*Written by Claude, 2026-03-21*
*For Codex audit: assess the j=0 exclusion as a formal result, and evaluate whether Form 3 (N=3 walk self-consistency) is the right route for the minimality principle*
*Issue: #3 (Weinberg angle), spin-pair minimality step*
