# Casimir Polynomial — Route: Algebraic Constraints from PF Axioms
*Can the three structural constraints that pin x² + C₂x - C₂ = 0 be derived from PF Axioms 1–3?*

**Date**: 2026-03-21
**Author**: Claude
**Route**: Algebraic constraints — derive f₀=0, g₀=0, g₁=−f₁ from PF axioms, then invoke uniqueness
**Outcome**: C (gap reduction) — two of three constraints have PF-native derivations; one reduces to the same gap as Route A
**Builds on**: `g3_casimir_weinberg_angle.md` §2.2, `the_propagation_framework.md`, `topological_weight_from_propagation.md`

---

## 1. The Setup

The most general degree-2 polynomial in x with Casimir-type coefficients is:

$$x^2 + (f_0 + f_1 C_2)\,x + (g_0 + g_1 C_2) = 0.$$

Three constraints uniquely select x² + C₂x − C₂ = 0:

| Constraint | Condition | Result |
|-----------|-----------|--------|
| No spin-independent mass | f₀ = 0 | Linear term purely from angular structure |
| Massless at s=0 | g₀ = 0 | Scalar mode (j=0) has zero mass eigenvalue |
| Coefficient antisymmetry | g₁ = −f₁ | Equal and opposite angular contributions |

Plus normalization: f₁ = 1 (the leading coefficient of C₂ in the linear term equals 1).

Each constraint is tested separately against PF axioms. No constraint is assumed. Each either derives, argues, or fails.

---

## 2. Constraint 1: f₀ = 0 (no spin-independent mass)

**What it says**: The coefficient of x in the polynomial has no spin-independent part. The only coupling to x comes through C₂ (angular structure).

**PF-native argument**:

In the Propagation Framework, rest mass arises from stable self-reinforcing propagation (Axiom 3). A mode is massive if and only if it forms a coherent closed loop — a standing wave pattern that self-reinforces without dispersing. The angular structure of the mode (its Casimir C₂ = j(j+1)) is the organizing content of that loop.

A spin-independent mass term f₀ ≠ 0 would mean: even a mode with zero angular structure (C₂ = 0, j = 0) has a non-zero coupling in the mass eigenvalue equation. But a j=0 mode has no rotational degrees of freedom — there is no angular coherence loop. If mass were present for j=0, it would have to come from somewhere other than angular self-reinforcement.

**Axiom 1** (propagation is fundamental) says there is no pre-existing mass parameter — mass is a derived quantity emerging from propagation structure. A spin-independent f₀ would be exactly such a pre-existing parameter.

**Verdict**: f₀ = 0 **argued** from Axiom 1 + Axiom 3. The argument is: mass from angular coherence only → no spin-independent mass term.

**Gap**: The argument treats "angular coherence" as the only source of mass, which is a specific claim about PF mass generation not yet formally derived from the axioms alone. The claim is PF-shaped and consistent with the three axioms, but "mass from angular coherence only" is a specific sub-principle that still needs a derivation path.

---

## 3. Constraint 2: g₀ = 0 (massless eigenstate at s=0)

**What it says**: The constant term in the polynomial has no spin-independent part. At C₂ = 0, the equation reduces to x² = 0, forcing x = 0 (zero mass eigenvalue).

**PF-native argument**:

This is the same content as Constraint 1, stated as a condition on the eigenvalue rather than the coefficient. If mass arises only from angular structure, then the mass eigenvalue must vanish when C₂ = 0. The j=0 mode has no angular content and therefore no mass.

Physical check: In the Standard Model, the only fundamental j=0 particle is the Higgs boson, which is massive — but through a spontaneous symmetry breaking mechanism, not an intrinsic mass from its spin content. All massless particles in the SM are j=1 (photon, gluon) or j=2 (graviton). The Standard Model is consistent with g₀=0 as the "intrinsic" condition before symmetry breaking.

**Verdict**: g₀ = 0 **argued** from the same chain as f₀ = 0. Same strength, same gap.

**Note**: g₀=0 and f₀=0 are not independent — they are both manifestations of the same PF principle (mass from angular coherence). If one is derived, the other follows. So these two constraints together count as **one independent gap**, not two.

---

## 4. Constraint 3: g₁ = −f₁ (coefficient antisymmetry)

**What it says**: The coefficient of C₂ in the constant term is minus the coefficient of C₂ in the linear term. In the polynomial x² + f₁C₂·x − f₁C₂ = 0, the C₂ appears with equal weight and opposite sign in the two non-leading terms.

**Equivalently**: the polynomial factors as x² = f₁C₂(1 − x), i.e.:

$$\frac{x^2}{1-x} = f_1 C_2.$$

With f₁ = 1 (normalization), this is x²/(1−x) = C₂.

**Physical reading**: The squared kinematic parameter (x²) divided by the structural complement (1−x) equals the angular complexity (C₂). This is not an external condition — it is a self-consistency relation where the kinematic and angular content of the mode are in balance.

**Where this constraint comes from — the de Broglie route (Section 6 of g3_casimir_weinberg_angle.md)**:

The relativistic de Broglie standing-wave condition for spin j is:

$$\frac{\beta^2}{\sqrt{1-\beta^2}} = \sqrt{j(j+1)} = \sqrt{C_2}.$$

Squaring: β⁴/(1−β²) = C₂. With u = β²: u²/(1−u) = C₂. This IS the antisymmetry condition g₁=−f₁ with f₁=1.

**Verdict**: g₁ = −f₁ does NOT have a PF-native derivation independent of Route A. It is algebraically equivalent to the squaring of the de Broglie self-consistency condition. Deriving g₁=−f₁ from PF axioms requires first deriving β²/√(1−β²) = √C₂ from PF axioms — which is precisely what Cascade's Route A is attempting.

**This constraint is the critical one. The other two (f₀=0, g₀=0) are argued but plausibly PF-native. This one directly imports Route A's gap.**

---

## 5. Normalization: f₁ = 1

After applying the three constraints, the polynomial is x² + f₁C₂x − f₁C₂ = 0. The remaining free parameter f₁ sets the overall scale of the angular coupling.

**Is f₁ = 1 a normalization or a physical constraint?**

In the de Broglie route, f₁ = 1 is not a free choice — it is forced by the specific form β²/√(1−β²) = √C₂. Squaring gives exactly u²/(1−u) = C₂, i.e., f₁ = 1. Any other value of f₁ would require a different de Broglie condition (e.g., β²/√(1−β²) = λ√C₂ for some λ ≠ 1).

**Verdict**: f₁ = 1 is not an independent constraint — it is included in Constraint 3 when that constraint is derived from the de Broglie condition rather than assumed separately. The same gap applies.

---

## 6. What This Route Establishes

| Constraint | PF status | Gap |
|-----------|-----------|-----|
| f₀ = 0 | Argued | "Mass from angular coherence only" needs formal derivation |
| g₀ = 0 | Argued (same chain) | Same gap as f₀=0 |
| g₁ = −f₁ | Reduces to Route A | Requires β²/√(1−β²) = √C₂ from PF axioms |
| f₁ = 1 | Included in g₁=−f₁ | Same gap |

**The key finding**: The three constraints are not three independent gaps. They reduce to **two independent gaps**:

1. **Mass from angular coherence only** (argued, one formal derivation step away)
2. **The de Broglie self-consistency condition** β²/√(1−β²) = √C₂ (not yet argued from PF — shared with Route A)

Gap 1 is smaller and more targeted than it looks. If PF can formally state "mass = angular coherence = closed propagation loop," then f₀=0 and g₀=0 both follow.

Gap 2 is the same gap that appears in Route A, Route C (Laplacian eigenvalue), and likely several other routes. **This convergence is itself a result**: the polynomial's structure is mostly constrained by the mass-from-angular-coherence principle; the specific form comes from the relativistic standing-wave condition, which is the one genuine new input needed.

---

## 7. The Gap, Precisely Stated

The Casimir polynomial x² + C₂x − C₂ = 0 requires:

**Needed (Gap 1, plausibly PF-native)**: A formal statement from Axioms 1+3 that rest mass arises only from angular self-reinforcement. This gives f₀=g₀=0. The principle is present informally in the PF narrative but has not been derived as a theorem.

**Needed (Gap 2, same as Route A)**: A derivation of β²/√(1−β²) = √C₂ for a coherent relativistic spinning PF mode. This gives g₁=−f₁=−1 and pins the polynomial completely.

If both gaps close, the polynomial is derived. If Gap 2 cannot close from Axioms 1–3 alone, the polynomial requires additional structure beyond the three axioms.

---

## 8. Outcome Classification

**Outcome C (gap reduction)**: This route does not derive the polynomial, but it reduces the question from "why this specific polynomial?" to two sharply stated gaps, one of which (mass from angular coherence) is likely much closer to PF-derivable than the original question. The two gaps also converge with Route A, which strengthens the case that the real work is in one place: the de Broglie self-consistency condition.

---

*Written by Claude, 2026-03-21*
*Route: Algebraic constraints from PF axioms*
*Outcome: C — gap reduction, two gaps identified, convergence with Route A established*
*Issue: #3 (Weinberg angle), Casimir polynomial derivation*
