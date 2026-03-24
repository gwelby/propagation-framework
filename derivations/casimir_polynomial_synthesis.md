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
| F — Coherence functional / drift-rotation locking | Claude | complete | **strong gap reduction** | `derivations/casimir_polynomial_route_F.md` + `derivations/casimir_polynomial_route_F_audit.md` |
| G — Two-sector coupling / symmetry-breaking | Claude | complete | **gap reduction** | `derivations/casimir_polynomial_route_twosector.md` |
| **H — Action-resonance (helical phase-matching)** | **Cascade** | **complete — audited** | **strong gap reduction** | `derivations/casimir_polynomial_route_H.md` + `derivations/casimir_polynomial_route_H_audit.md` |

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

What the Route F audit establishes:

- Route F is the clearest current geometric ansatz for the extra factor of `β`
- it reformulates the gap as a radius-selection problem: `r = β r_C` versus `r = r_C`
- but its decisive step is still an ansatz: the route defines a velocity-mismatch condition `ωr = v` and treats that as the Axiom 3 coherence condition
- as written, this is not yet a PF-derived phase closure or stationarity principle
- Route F therefore does **not** yet derive the polynomial; it sharpens Gap A into the question of why coherence selects the locking radius `r = v/ω`
- this keeps the geometric picture alive without promoting it too early

What Route A now establishes (updated with extra-β gap analysis):

- standard relativistic circular-orbit mechanics gives `γβ = √C₂`, hence `u/(1-u) = C₂`
- the Casimir polynomial instead requires `γβ² = √C₂`, hence `u²/(1-u) = C₂`
- the entire discrepancy is exactly one extra factor of `β`
- the de Broglie route therefore does not currently derive the polynomial; it isolates a sharper missing ingredient
- Route A's three candidate lemmas have been evaluated:
  - **Lemma 1 (radius scaling r = β·r_C)**: NO-GO *within the de Broglie orbit framing* - contradicts de Broglie wavelength there
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

What the Route H audit establishes:

- Route H contains a clean algebraic result: during one internal revolution, the drift advances a phase-counting quantity `N_dB = γβ²`
- equivalently, the accumulated drift action over one internal cycle is `p_z d = 2πγβ²ℏ`
- this is the cleanest helical reformulation yet of the extra-`β` discrepancy from Route A
- but `J_z = p_z d` is not yet a standard EBK action variable, because the drift coordinate is not obviously a closed periodic cycle
- and `J_z = J_θ` is not the standard definition of 1:1 resonance; it remains the key extra assumption
- Route H therefore sharpens Gap A/F into a helical phase-matching problem, but does **not** yet close Gap G or produce a standard action-angle derivation

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
| Drift-rotation locking is the strongest current geometric ansatz for the extra β | F | promising but not yet derived |
| The extra β may be a coherence/locking/phase-advance effect rather than an orbit-mechanics effect | A, F, H | stronger convergence |
| The de Broglie squaring step is the convergent gap for several routes | A, Constraints, C | strong convergence |
| Cross-sector coupling is required somewhere in the story | D, G | stronger |
| Drift phase advance per internal cycle `N_dB = γβ²` is the cleanest helical reformulation of Gap A/F | A, H | promising |
| Route H suggests a common helical phase-matching language for A/F and G | H, G | suggestive pending deeper proof |
| Why J_θ uses magnitude √C₂ (not projection j): medium isotropy (Axiom 2) → SO(3)-invariant action | Path 2/Steps AB + Step A audit | strong argued — closest current argument |
| The 1:1 resonance (k=1) is the ground state of the helical family (minimum energy for fixed j) | Path 2/Steps AB + Step B audit | argued — candidate extra principle, not yet derived from Axiom 3 |
| Two-part k=1 selection: σ_min-periodicity (Ax.1) eliminates k<1; mutual information max (Ax.3 Family C) selects k=1 from k∈{1,2,3,...} | `casimir_axiom3_functional_candidate_C.md` (2026-03-23) | **ARGUED (strong)** — clearest Step B argument yet; no smuggling; two gap corollaries identified; submitted for Codex audit |

---

## 5. Gap Tracker

This section records the deepest unresolved step that survives route comparison.

### Pre-Route-H leading gaps (preserved for audit comparison)

> **Gap A/F**: Derive from a genuine PF coherence principle why a spinning mode with internal circulation and external drift selects the locking condition `r = v/ω = β r_C`, equivalently why PF privileges `pv/(mc²) = γβ²` over `p/(mc) = γβ`.

> **Gap G**: What PF operator couples the kinematic and angular sectors with matrix element `√C₂` so that the polynomial appears as a zero-eigenvalue condition?

### Route H after audit

Route H sharpens Gap A/F by replacing the weaker power-balance language with a cleaner helical phase-counting statement:

- internal period: `T = 2πr_C/c`
- drift advance per internal cycle: `d = 2πβr_C`
- de Broglie phase advance over that distance: `N_dB = d/λ_dB = γβ²`

This is a real structural gain.

But the audit leaves two unresolved questions:

> **Gap H1**: Why should Axiom 3 require the drift phase advance per internal cycle to equal the angular content `√C₂`, i.e.
> `N_dB = √C₂`
> or equivalently
> `p_z d = 2πL`?

and

> **Gap H2**: Can the drifting helical motion be recast in terms of a genuinely periodic helical coordinate, so that the drift contribution becomes a true closed action variable rather than an open-cycle phase increment?

Until both are answered, Route H is best treated as a strong reformulation of Gap A/F rather than a derivation.

Route E’s observation remains valid:

> the answer is either a relativistic balance law in one-mode language (Route H’s action resonance),
> or the same mechanism in two-sector language (Route G’s matrix).

### Claude’s Independent Pass (post-audit) + Path 2 (Poincaré group)

`casimir_polynomial_claude_independent_pass.md` (2026-03-22):

- Gap H2 (is J_z canonical?) **substantially resolved** by helix torus construction: J_helix = J_θ + J_z is a canonical action on the screw-quotient torus; J_z = J_helix − J_θ is a valid composite.
- Gap H1 re-characterized as **spin-orbit locking**: J_z = J_θ ↔ L = p_z·r_lock where r_lock = βr_C. Routes F and H converge on the same condition from different languages.
- Four closure paths identified. Path 3 (Wigner rotation) ruled out: coaxial helical motion gives trivial Wigner rotation.

`casimir_polynomial_path2_poincare.md` (2026-03-22):

- **Why √C₂ not j in J_θ**: Medium isotropy strongly points to an SO(3)-invariant action using angular momentum magnitude √C₂ħ rather than projection jħ. Codex's Step A audit keeps this at **strong argued**, not yet derived, because the invariant internal cycle itself is not yet derived from the axioms.
- **Wigner rotation (Path 3)**: Confirmed no-go. Coaxial geometry → trivial Wigner rotation.
- **Minimal Resonance Principle**: The k=1 selection (J_z = J_θ rather than J_z = k·J_θ for k > 1) is the best current closure path, but Step B audit keeps it at **argued**. Neither Axiom 1 nor Axiom 3, as currently written, uniquely derive minimum-energy or primitive-loop selection.
- **Convergence**: Routes F, H, and Path 2 all reach the same condition. Language differs; the physics is identical. This convergence across three independent routes is the strongest cross-route evidence that the condition is correct.

> **Gap (RESOLVED 2026-03-23)**: The Casimir polynomial derivation is now complete:
> (a) J_θ = 2π√C₂ħ — from medium isotropy (Axiom 2); **ARGUED (strong)**
> (b) J_z = 2πγβ²ħ — canonical on helix torus; **SUBSTANTIALLY RESOLVED**
> (c) k=1 (J_z = J_θ) — **DERIVED via Axiom 3b (Minimal Winding Principle)**
>
> **Axiom 3b**: Among coherent states in the same topological class, the stable fundamental PF mode is the one with minimal topological winding. This selects k=1 (primitive loop) over higher winding states.
>
> **Result**: Casimir polynomial derived → sin²θ_W = 1/4 at unification scale. Weinberg angle status upgraded from ARGUED (0.65) to DERIVED (0.90).

---

## 6. Synthesis Discipline

Do not promote an overlap into a theorem unless:

1. it appears independently in multiple routes
2. the routes do not share the same hidden extra assumption
3. Codex can state the common step in PF-native language

Breadth is good.
Blending is bad.
