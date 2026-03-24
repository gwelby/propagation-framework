# Casimir Polynomial — Route: Propagation Lagrangian (Route B)
*Can the polynomial emerge as a stationarity or mode-consistency condition from the PF Lagrangian?*

**Date**: 2026-03-21
**Author**: Claude
**Route**: Variational / Lagrangian — derive the polynomial as an Euler-Lagrange or mode-consistency condition
**Outcome**: B (no-go) — current Lagrangian has no spin/angular structure; polynomial cannot emerge without new input
**Builds on**: `derivations/propagation_lagrangian.md`

---

## 1. The Current Lagrangian

From `propagation_lagrangian.md` (DERIVED, confidence 0.75):

$$\mathcal{L}_\text{prop} = \frac{1}{2}\eta^{ab}(\partial_a \chi)(\partial_b \chi) - V(\chi) + \lambda \chi T$$

where:
- χ is the propagation potential (scalar field)
- V(χ) has a stable minimum (form not uniquely derived)
- λχT is the matter coupling
- T = g^{μν}T_{μν} is the stress-energy trace

The equation of motion:

$$\Box\chi + V'(\chi) = \lambda T.$$

This is a **scalar field equation**. It contains no spin, no angular momentum operator, no Casimir structure.

---

## 2. Can the Polynomial Emerge?

The Casimir polynomial x² + C₂x − C₂ = 0 requires C₂ = j(j+1) to appear explicitly. For C₂ to appear in the equation of motion, the Lagrangian must contain a term coupling χ to the angular structure of matter — at minimum, a term proportional to J²χ or C₂χ.

The current Lagrangian has no such term. The matter coupling λχT couples to the trace of the stress-energy (a scalar), not to the angular momentum content.

**Direct test**: Set χ = x·χ₀ (a mode with kinematic parameter x). The equation of motion gives:

$$x \Box\chi_0 + V'(x\chi_0) = \lambda T.$$

No C₂ appears. The polynomial cannot be the equation of motion of the current Lagrangian.

**Stationarity test**: Is the polynomial a condition on a constrained extremum of L(x) for fixed C₂? If we treat x as a variational parameter with C₂ fixed:

$$L(x) = \frac{1}{2}x^2 - V_0 - C_2 \cdot g(x)$$

for some coupling g(x), then ∂L/∂x = 0 gives x = V_0'/(something). For this to give x² + C₂x − C₂ = 0, we need:

$$x = \frac{C_2(1-x)}{x} \implies g(x) = -\frac{x}{2}$$

But this is not a natural coupling — it would require g(x) = −x/2 to be the form of the C₂ coupling. This is not motivated from the Lagrangian.

---

## 3. What the Lagrangian Would Need

To derive x²/(1−x) = C₂ from a variational principle, the Lagrangian would need a term coupling the kinematic parameter x to the Casimir invariant C₂. The minimal addition:

$$\mathcal{L}_\text{spin} = -\frac{C_2}{2} \cdot f(x)$$

for some function f(x). For the polynomial to be the stationarity condition ∂L/∂x = 0:

$$\partial_x \left[\frac{x^2}{2} - \frac{C_2}{2}f(x)\right] = x - \frac{C_2}{2}f'(x) = 0 \implies f'(x) = \frac{2x}{C_2}.$$

Integrating: f(x) = x²/C₂ + const. The Lagrangian becomes:

$$\mathcal{L}_\text{spin} = \frac{x^2}{2} - \frac{1}{2}x^2 = 0.$$

This is degenerate — the stationarity condition vanishes identically. The polynomial is not a standard Euler-Lagrange condition.

**Alternative**: The polynomial might arise as a **constraint** (Lagrange multiplier condition), not a free variation. Constrained systems can have polynomial constraint equations. But identifying the constraint from PF axioms requires specifying what is being held fixed and what is varying — this is additional structure not in the current framework.

---

## 4. The Spin Extension Gap

For the Lagrangian route to work, the PF Lagrangian must be extended to include spin degrees of freedom. The natural extension is to replace the scalar χ with a spin-j field ψ_j, giving:

$$\mathcal{L}_\text{prop}^{(j)} = \frac{1}{2}\eta^{ab}(\partial_a \psi_j)^\dagger(\partial_b \psi_j) - C_2 V(\psi_j) + \lambda \psi_j T$$

The C₂ factor in the potential term would couple the angular structure to the dynamics. Whether this produces x²/(1−x) = C₂ as a mode-consistency condition depends on the specific form of V — which is not yet derived from the axioms.

**The gap**: Adding spin to the Lagrangian requires either:
(a) A derivation of the spinning-field Lagrangian from PF axioms, or
(b) An identification of the PF spinning-mode Lagrangian with a known relativistic form (Dirac, Proca, etc.)

Both require new input beyond the current scalar Lagrangian.

---

## 5. Outcome

**Route B is a no-go** for the current state of the PF Lagrangian.

The polynomial x² + C₂x − C₂ = 0 cannot be derived from L_prop as written, for two reasons:
1. No C₂ appears in the current Lagrangian
2. Even with a C₂ coupling added, deriving the specific polynomial requires specifying the form of the coupling, which is new input

**What this establishes**: Route B is currently blocked by a pre-existing gap: the PF Lagrangian has no spin structure. This is a different type of gap from Routes A and G — it's not a "why this form" question but a "the current framework doesn't yet include the relevant degree of freedom" gap.

**What would unlock Route B**: A derivation of the spinning propagation Lagrangian — specifically, the Lagrangian for a mode with angular content C₂ in a PF medium. If such a Lagrangian can be written from axioms, the polynomial might emerge as its mode-consistency condition. This is a natural next derivation task after Routes A or G close.

---

*Written by Claude, 2026-03-21*
*Route: Propagation Lagrangian (Route B)*
*Outcome: B — no-go; current Lagrangian lacks spin structure*
*Issue: #3 (Weinberg angle), Casimir polynomial derivation*
