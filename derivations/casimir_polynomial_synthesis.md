# Casimir Polynomial Synthesis
*Cross-route comparison board for the parallel attack*

**Date**: 2026-03-21
**Purpose**: Keep the multi-route attack broad without blending assumptions
**Authority**: `casimir_polynomial_brief.md` and `casimir_polynomial_route_matrix.md`

---

## 1. Current Rule

Each route must stay separate.

For each route record:
- starting assumptions
- result type: derivation / no-go / smaller lemma
- exact unresolved step

Only after that do we synthesize.

---

## 2. Route Board

| Route | Owner | Status | Result type | Key output |
|---|---|---|---|---|
| A — Relativistic standing-wave / de Broglie | Cascade | complete | **gap reduction** | `derivations/casimir_polynomial_route_A.md` |
| B — Propagation Lagrangian / variational | Claude | complete | **no-go** | `derivations/casimir_polynomial_route_lagrangian.md` |
| C — Medium-Laplacian eigenvalue | Claude | complete | **gap reduction** | `derivations/casimir_polynomial_route_laplacian.md` |
| Constraints — algebraic uniqueness route | Claude | complete | **gap reduction** | `derivations/casimir_polynomial_route_constraints.md` |
| D — Holonomy / monodromy | Claude | complete | **partial no-go / gap reduction** | `derivations/casimir_polynomial_route_holonomy.md` |
| E — Refractive stress / virial balance | Codex | complete | **gap reduction** | `derivations/casimir_polynomial_route_refractive.md` |
| F — Coherence functional / drift-rotation locking | Claude | complete | **B+ (closest to derivation)** | `derivations/casimir_polynomial_route_F.md` |
| G — Two-sector coupling / symmetry-breaking | Claude | complete | **gap reduction** | `derivations/casimir_polynomial_route_twosector.md` |

---

## 3. Confirmed Across Completed Routes

What the tracked Lagrangian route now rules out:

- the current single-scalar PF Lagrangian does not by itself yield the polynomial
- the current scalar fluctuation operator is affine in the spectral variable
- \(C_2\) does not enter unless PF first derives an internal angular sector

What the algebraic-constraints route establishes:

- the three coefficient constraints reduce to two real gaps, not three
- `f₀ = 0` and `g₀ = 0` both collapse to the same PF claim: mass from angular coherence only
- the antisymmetry constraint `g₁ = −f₁` reduces to the same core issue as Route A

What the Laplacian route establishes:

- the polynomial reads cleanly as a PF resonance condition
- but the specific squaring in `x²/(1-x) = C₂` is not fixed by medium language alone
- this route converges back to the same relativistic self-consistency gap as Route A

What the holonomy route establishes:

- a transfer-matrix formulation can reproduce the polynomial algebraically
- but the actual PF phase walk only yields scalar holonomies on fixed spin sectors
- any successful holonomy route still needs a real cross-sector coupling map

What the two-sector route establishes:

- the polynomial is exactly the zero-eigenvalue condition of a specific `2 × 2` kinematic-angular coupling matrix
- this gives a second physical picture that is not identical to the one-sector de Broglie route
- the new sharp gap is: why is the off-diagonal coupling exactly `√C₂`?

What the refractive route establishes:

- PF refraction naturally gives a drift-versus-structure balance law
- the Casimir naturally sits on the structural side as an angular barrier / stress term
- but refraction still does not force the specific nonlinear form `x²/(1-x) = C₂`

What Route F establishes:

- A PF mode has two simultaneous motions: internal circulation at $c$ (Axioms 1+2) and external drift at $\beta c$
- Axiom 3 (coherence) applied to both motions gives a **drift-rotation locking** condition: the mode is self-reinforcing at radius $r_{\text{lock}} = \beta r_C$ where tangential velocity = drift velocity
- This directly derives Cascade's Lemma 1 ($r = \beta r_C$) from Axiom 3 — NOT from the de Broglie orbit condition
- At $r_{\text{lock}}$: $L = \gamma\beta^2\hbar = \sqrt{C_2}\hbar$ → Casimir polynomial ✓
- This is the coherence locking picture, not the circular orbit picture — confirming Cascade's Lemma 3
- One argued step remains: drift-rotation locking as the specific Axiom 3 condition for a spinning+drifting mode
- Note: Codex's "Lemma 1 NO-GO" was based on the de Broglie orbit. Route F does NOT use the de Broglie orbit. The two are different physical pictures and there is no contradiction.

What Route A now establishes (updated with extra-β gap analysis):

- standard relativistic circular-orbit mechanics gives `γβ = √C₂`, hence `u/(1-u) = C₂`
- the Casimir polynomial instead requires `γβ² = √C₂`, hence `u²/(1-u) = C₂`
- the entire discrepancy is exactly one extra factor of `β`
- the de Broglie route therefore does not currently derive the polynomial; it isolates a sharper missing ingredient
- Route A's three candidate lemmas have been evaluated:
  - **Lemma 1 (radius scaling r = β·r_C)**: NO-GO - contradicts de Broglie wavelength
  - **Lemma 2 (kinetic power balance)**: GAP REDUCTION - reduces to eliminating -β² term from power balance
  - **Lemma 3 (propagator pole)**: NO-GO - requires field theory beyond axioms
- The extra-β gap is now reduced to: "Why does the -β² term vanish in the kinetic power balance?"
- Possible resolution paths for Lemma 2:
  1. High-velocity approximation (β → 1)
  2. Quantum correction to energy density
  3. Different energy partition (total vs kinetic energy in power definition)

This means any successful future route must explain at least one of:

1. where the angular operator comes from
2. why the effective mode problem is multi-sector rather than single-scalar
3. what exact reduced consistency relation generates the quadratic
4. why the de Broglie self-consistency relation takes the specific form `β²/√(1-β²) = √C₂`
5. or why the two-sector coupling strength is exactly `√C₂`

---

## 4. Intersection Tracker

Use this section only for steps that appear independently in at least two routes.

| Candidate step | Routes supporting it | Status |
|---|---|---|
| Matter must be treated as a structured mode, not a point excitation | A, B | weak intersection |
| A single scalar mode equation is insufficient | B | current |
| A two-sector reduction is structurally natural | D, G | stronger |
| The missing structure must carry \(C_2\) explicitly | B, D, G | stronger |
| The polynomial’s specific form is not fixed by medium language alone | A, Constraints, C | stronger |
| The polynomial is naturally interpretable as a balance law | C, E | stronger |
| The Casimir belongs on the structural side of the balance | C, E, G | stronger |
| The de Broglie route is missing exactly one extra factor of `β` | A | current |
| Drift-rotation locking (Axiom 3) gives $r = \beta r_C$ → correct polynomial | F | new — strongest route |
| The extra β comes from a coherence condition, not orbit mechanics | A, F | convergent |
| The de Broglie squaring step is the convergent gap for several routes | A, Constraints, C | strong convergence |
| Cross-sector coupling is required somewhere in the story | D, G | stronger |

---

## 5. Gap Tracker

This section records the deepest unresolved step that survives route comparison.

Current leading gaps (updated after Route F):

> **Gap F (leading gap)**: Formally derive from Axiom 3 that a PF mode with internal angular velocity ω and external drift velocity v achieves coherent self-reinforcement at locking radius $r = v/\omega = \beta r_C$, rather than at $r_C$ or another radius. This is the drift-rotation locking condition. If it follows from Axiom 3, the Casimir polynomial is derived.

> **Gap A (refined)**: Why does the -β² term vanish in the kinetic power balance equation
> ` (γ - 1)β·mc²/r = γβ²·√C₂ `
> leaving ` γβ² = √C₂ ` as required by the Casimir polynomial?

This is the refined version of the original extra-β gap, now reduced from "why γβ² instead of γβ?" to the specific question of energy partition in coherent modes.

Route A analysis shows three possible resolution paths:
1. High-velocity approximation (β → 1) making β² ≈ 1
2. Quantum correction to kinetic energy density in coherent modes
3. Different definition of power (total vs kinetic energy) in coherence conditions

and

> **Gap G**: What PF operator couples the kinematic and angular sectors with matrix element
> `√C₂`
> so that the polynomial appears as a zero-eigenvalue condition?

These may still turn out to be two descriptions of the same deeper mechanism.
That is now the main synthesis question.

Route E strengthens that interpretation:

> the eventual answer is likely either a relativistic balance law in one-mode language,
> or the same mechanism written as kinematic-versus-angular stress coupling in two-sector language.

Below both of them sits a still-deeper structural requirement:

> PF needs a derived internal angular / representation sector that can carry
> `C₂ = j(j+1)` into either a one-mode relativistic balance law or a pre-mass-matrix two-sector operator.

> **Gap A (alternate formulation)**: What is the correct energy partition function for coherent PF modes?
> The gap suggests that Axiom 3 (coherence) may imply a specific way of counting energy flow between kinetic and structural reservoirs that differs from standard relativistic mechanics.

---

## 6. Synthesis Discipline

Do not promote an overlap into a theorem unless:

1. it appears independently in multiple routes
2. the routes do not share the same hidden extra assumption
3. Codex can state the common step in PF-native language

Breadth is good.
Blending is bad.
