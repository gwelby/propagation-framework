# Casimir Polynomial — Route: Medium-Laplacian Eigenvalue
*Does the polynomial arise as the spectral condition of a rotation-group Laplacian on the PF medium?*

**Date**: 2026-03-21
**Author**: Claude
**Route**: Casimir as medium-Laplacian eigenvalue — the polynomial emerges from a mode equation whose spectral parameter satisfies x² + C₂x − C₂ = 0
**Outcome**: C (gap reduction with convergence finding)
**Builds on**: `topological_weight_from_propagation.md`, `the_propagation_framework.md`, `casimir_polynomial_route_constraints.md`

---

## 1. The Idea

In a 3D propagation medium with SO(3) rotational symmetry, coherent modes can be labeled by their angular structure. The angular Laplacian (quadratic Casimir of SO(3)) has eigenvalue C₂ = j(j+1) for the spin-j representation.

The question: is the polynomial x² + C₂x − C₂ = 0 the **spectral condition** for coherent modes in this medium? That is, does a mode equation of the form

$$\hat{L}\,\psi = \lambda\,\psi$$

produce exactly this polynomial when the spectral parameter x is related to the Casimir eigenvalue C₂ by a self-consistency requirement?

---

## 2. The PF Medium Structure

From `topological_weight_from_propagation.md` (DERIVED):

- 3D medium → SO(3) symmetry group
- Coherent modes labeled by spin j → Casimir C₂ = j(j+1)
- Two topological classes: bosonic (integer j, contractible loops) and fermionic (half-integer j, non-contractible loops)
- The Casimir operator commutes with all rotations and acts as a scalar on each irreducible representation

The PF medium has a well-defined angular Laplacian: the quadratic Casimir $\hat{C}_2 = \hat{J}^2$ with eigenvalue C₂ = j(j+1) on the spin-j sector.

---

## 3. Candidate Mode Equation

A coherent mode ψ with angular label j and kinematic parameter x = β² (velocity-squared ratio to c²) satisfies some mode equation in the PF medium. In the simplest case consistent with the SO(3) structure:

$$x \cdot \hat{C}_2\,\psi = f(x)\,\hat{C}_2\,\psi$$

This is trivial. The non-trivial content comes from a self-consistency condition.

**The self-consistency ansatz**: A coherent standing-wave mode with kinematic parameter x and angular content C₂ is self-consistent if and only if its "squared propagation ratio" is balanced by its angular content:

$$x^2 = C_2\,(1-x).$$

This gives x² + C₂x − C₂ = 0 directly.

**What this says physically**: The fraction of the mode's "propagation capacity" that is committed to squared kinematic content (x²) equals the angular complexity C₂ times the remaining non-kinematic fraction (1−x). The mode is self-reinforcing exactly at the balance point.

---

## 4. Is This Derived or Assumed?

The ansatz x² = C₂(1−x) is the polynomial itself, written as a balance law. Stating it as an ansatz is not a derivation — it is circular unless the balance law can be independently motivated.

**Attempt to ground it in the medium structure**:

The quadratic Casimir C₂ measures the "angular complexity" of the mode — how many rotational degrees of freedom it occupies. The kinematic parameter x = β² measures how much of the causal velocity the mode's drift occupies.

In a relativistic medium (Axiom 2: causal velocity), the total "capacity" is partitioned between drift (x) and structure (1−x). The structural partition carries angular content C₂. The self-reinforcing condition (Axiom 3) requires:

$$\frac{\text{kinematic fraction}^2}{\text{structural fraction}} = \text{angular complexity},$$

i.e., x²/(1−x) = C₂.

The squaring of the kinematic fraction (x² rather than x) is the key step. **This squaring needs justification.**

---

## 5. Why x² and Not x?

The equation x/(1−x) = C₂ would give a different polynomial: x = C₂(1−x) → x(1+C₂) = C₂ → x = C₂/(1+C₂). This has a unique solution for each j and does NOT give the Weinberg angle to sub-percent accuracy.

The equation x²/(1−x) = C₂ is not a generic balance law. The squaring is the specific content that matches observation. Where does it come from?

**Three possible sources — all reduce to the same gap:**

**Source 1 (de Broglie)**: β²/√(1−β²) = √C₂ → squaring gives β⁴/(1−β²) = C₂. With x = β²: x²/(1−x) = C₂. The squaring comes from the relativistic de Broglie velocity-momentum relation.

**Source 2 (propagator pole)**: In a relativistic dispersion relation ω² = k² + m², the ratio of momentum squared to frequency squared gives a squared quantity. The polynomial x²/(1−x) = C₂ could be the on-shell condition for a spinning mode propagator.

**Source 3 (phase coherence)**: If the self-consistency condition involves the phase of the mode (which is intrinsically a complex quantity), then the self-reinforcing condition on the amplitude involves squaring the phase contribution. This is heuristic.

**All three sources require additional structure beyond Axioms 1–3.** Source 1 is Route A (Cascade). Source 2 is Route B (Codex's propagation Lagrangian). Source 3 needs formalization.

---

## 6. The Laplacian Eigenvalue Interpretation — What It Gives

Rewrite the polynomial as a fixed-point condition:

$$x = \frac{C_2\,(1-x)}{x} = \frac{C_2}{x} - C_2.$$

This is not a useful form. Try the other direction:

$$x + C_2 = \frac{C_2}{x}.$$

The fixed-point map f(x) = C₂/(x + C₂) was already shown (in `g3_form3_attempt.md` §8) to recover the polynomial under 3-fold composition — but without adding new information.

**Alternative**: interpret x as the eigenvalue of an operator that acts on the mode. If the medium Laplacian ∇² in the angular directions has eigenvalue −C₂/r² for a mode at radius r, and the kinematic part has eigenvalue −x/r², then the total eigenvalue condition for a standing wave:

$$\frac{x^2}{1-x} = C_2$$

might arise from requiring the standing wave to close at the medium's coherence length. But this requires a specific geometric model of the PF medium with a defined coherence radius — not yet present in the framework.

---

## 7. Where This Route Leads

**The Laplacian eigenvalue route is not independent of Route A.** The mode equation x² = C₂(1−x) is the polynomial itself. Motivating it from the medium's Laplacian structure either:

(a) Reduces to the de Broglie balance condition (Route A gap), or
(b) Requires a specific geometric model of the PF medium with coherence length and angular momentum coupling (new structure beyond Axioms 1–3)

**What this route adds that is new**: The interpretation is clarified. The polynomial x²/(1−x) = C₂ reads as:

> The squared ratio of kinematic-to-structural content equals the angular Casimir of the mode.

This is a **resonance condition** in the PF medium: the mode is at the balance point where its kinematic and structural components are in exact resonance defined by the angular complexity. This language is natural in PF (Axiom 3: coherence as the condition for stable structure).

But the specific form — why squared, why this ratio — is not derivable from the language alone. It requires the mechanism behind the squaring, which is the same gap as Route A.

---

## 8. Cross-Route Convergence Finding

This route, the algebraic constraints route, and Route A (Cascade's de Broglie route) all converge on the same gap:

$$\text{Why does } \frac{x^2}{1-x} = C_2 \text{ rather than } \frac{x}{1-x} = C_2 \text{ or } \frac{x^2}{1-x^2} = C_2 \text{ or any other form?}$$

The answer in all cases traces back to the relativistic standing-wave squaring: β²/√(1−β²) = √C₂ → β⁴/(1−β²) = C₂. This is one gap expressed in three different route languages.

**Implication for the parallel attack**: Routes A, Algebraic Constraints, and Laplacian Eigenvalue are not three independent attacks. They triangulate to the same point. Codex's synthesis should register this as: **the polynomial's specific form is entirely contained in one question** — why does a coherent relativistic spinning PF mode satisfy β²/√(1−β²) = √C₂?

Routes B, D, E, F, G may genuinely be independent if they approach from non-relativistic-kinematic directions (Lagrangian, holonomy, refractive balance, symmetry breaking). Those should be executed to check.

---

## 9. Outcome

**Outcome C (gap reduction with convergence)**:

- The polynomial is a resonance condition in the PF medium (argued cleanly)
- The specific form x²/(1−x) requires a derivation of the relativistic squaring step
- Three routes (A, Constraints, Laplacian) converge on the same gap
- Routes B, D, E, F, G remain independent and should be checked

**The gap, maximally reduced**: Derive from PF Axioms 1–3 why a coherent relativistic spinning mode with angular content √C₂ satisfies β²/√(1−β²) = √C₂, rather than any other form of velocity-angular-content balance.

---

*Written by Claude, 2026-03-21*
*Route: Casimir as medium-Laplacian eigenvalue*
*Outcome: C — gap reduction, convergence with Routes A and Algebraic Constraints*
*Issue: #3 (Weinberg angle), Casimir polynomial derivation*
