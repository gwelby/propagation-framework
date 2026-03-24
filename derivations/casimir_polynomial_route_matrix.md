# Casimir Polynomial Route Matrix
*Why we should test all plausible derivation routes, but not blend them into one proof*

**Date**: 2026-03-21
**Question**: Why does PF produce `x² + C₂x - C₂ = 0`?
**Authority**: `ACTIVE_ISSUES.md` and `derivations/casimir_polynomial_brief.md`

---

## 1. Why Not Just One Route?

We should not restrict the work to a single favorite route.

But we also should not collapse all routes into one blended argument.

Reason:
- if multiple viewpoints are mixed together, we cannot tell which assumption actually did the work
- if the proof fails, we do not know which step failed
- hidden extra assumptions can slip across route boundaries and masquerade as derivation

So the honest method is:

> pursue all plausible routes, but keep them independent and auditable

Each route should end in one of three outcomes:
- derivation
- no-go
- smaller lemma

That is how we get breadth without losing rigor.

---

## 2. The Route Families

### Route A — Relativistic Standing-Wave / de Broglie Route

Core idea:
- the polynomial already appears from relativistic standing-wave kinematics
- try to ground that kinematic argument directly in PF axioms

PF-native input:
- Axiom 1: propagation is fundamental
- Axiom 2: internal propagation limited by causal velocity
- Axiom 3: stable matter is coherent self-reinforcing propagation

Target:
- derive `u²/(1-u) = C₂` with `u = v²/c²`

Main risk:
- may require a specific relativistic spinning-mode model not yet derived from PF

Status:
- best immediate route because it already reproduces the exact polynomial

---

### Route B — Propagation Lagrangian / Variational Route

Core idea:
- start from the existing propagation Lagrangian and ask whether the polynomial arises as a stationarity or self-consistency condition

PF-native input:
- `derivations/propagation_lagrangian.md`

Target:
- derive the polynomial as an Euler-Lagrange, constrained extremum, or mode-consistency condition

Main risk:
- the current Lagrangian may not yet contain the representation-theoretic structure needed to produce `C₂`

Status:
- important because it would be more first-principles than the de Broglie route if it closes

---

### Route C — Casimir as Medium-Laplacian Eigenvalue Route

Core idea:
- interpret `C₂ = j(j+1)` as an eigenvalue of angular structure in the propagation medium
- ask whether the polynomial arises from a mode equation on that medium

PF-native input:
- matter as standing wave
- rotational structure in 3D
- `SO(3)` / `SU(2)` representation content already present in the framework

Target:
- derive a mode equation whose spectral parameter satisfies `x² + C₂x - C₂ = 0`

Main risk:
- may need a concrete medium operator that PF has not yet defined

Status:
- mathematically natural

---

### Route D — Holonomy / Monodromy Route

Core idea:
- ask whether the polynomial is the characteristic equation of a closure map, transport map, or holonomy constraint on a coherent loop

PF-native input:
- phase closure
- coherent loops
- transport around closed paths

Target:
- show the polynomial emerges as a closure condition on a two-state or two-sector transport relation

Main risk:
- recent G3 work already showed holonomy-only observables can fail to fix key coefficients

Status:
- worth testing, but must avoid repeating the holonomy-only dead ends from G3

---

### Route E — Refractive Stress / Virial-Balance Route

Core idea:
- if forces are refractive and matter is a stable propagation knot, then the polynomial might encode a balance between translational drive and angular structural stress

PF-native input:
- forces as refraction
- matter as stable coherent pattern
- coherence as balance against dispersion

Target:
- derive the polynomial as a balance law between drift, confinement, and angular content

Main risk:
- easy to become a physical analogy unless written as an exact balance equation

Status:
- physically intuitive, audit-sensitive

---

### Route F — Information / Coherence Functional Route

Core idea:
- derive the polynomial from extremizing a coherence functional, information measure, or stability functional over structured modes

PF-native input:
- Axiom 3
- existing PF language around coherence thresholds and stable structure

Target:
- produce the polynomial as the stationarity condition of a concrete functional

Main risk:
- this route will fail unless the functional itself is PF-derived, not invented ad hoc

Status:
- high risk, high value

---

### Route G — Representation / Symmetry-Breaking Route

Core idea:
- derive the polynomial from the structure of symmetry breaking before asking which specific spins realize it

PF-native input:
- `SO(3) × U(1)` medium structure
- Goldstone / broken-generator picture already used elsewhere in the framework

Target:
- show the quadratic is forced by the coupling geometry of the two sectors

Main risk:
- may secretly depend on the same un-derived coupling-ratio structure that already blocks the Weinberg-angle derivation

Status:
- strategically important because it attacks the problem upstream of spin selection

---

### Route H — Helical Phase-Matching / Action-Per-Cycle Route (NEW — 2026-03-22)

Core idea:
- a helical PF mode (internal circulation + external drift) has two action variables
- Axiom 3 (coherence) requires 1:1 action commensurability between them
- this directly yields γβ² = √C₂, hence the Casimir polynomial

PF-native input:
- Axiom 1+2: internal circulation at causal velocity c
- SO(3) on 3D medium: angular momentum L = √C₂ ℏ
- Axiom 3: coherence = action commensurability (1:1 resonance)

Target:
- derive the polynomial from J_z = J_θ where J_z = 2πγβ²ℏ and J_θ = 2π√C₂ℏ

Main risk:
- the drift quantity `p_z d` is not yet a standard closed EBK action variable
- the 1:1 resonance condition is argued, not formally derived from Axiom 3
- must exclude higher-order resonances (2:1, 3:2, etc.)
- may be a phase-counting reformulation rather than a full action-angle derivation

Status:
- strong gap reduction
- formalizes Route F's geometric ansatz in cleaner helical phase language
- survives algebraically, but not yet as a standard EBK theorem
- illuminates Route G without yet deriving the two-sector coupling operator
- audited in `derivations/casimir_polynomial_route_H_audit.md`

---

## 3. Recommended Rule

Do all of them.

But do them as separate derivation notes, not as one merged argument.

That means:
- one route per note
- each note names its exact starting assumptions
- each note ends as derivation, no-go, or reduced lemma
- no cross-borrowing of unstated assumptions

---

## 4. Recommended Order

1. Route A — fastest because the exact polynomial is already known there
2. Route B — strongest first-principles route if it closes
3. Route C — clean mathematical route from spectral structure
4. Route G — upstream symmetry-breaking route
5. Route D / E / F — only if written as exact equations, not narratives

This is an order of attack, not an exclusion list.

---

## 5. Operational Summary

The right question is not:

> which single route do we believe?

The right question is:

> which routes survive honest contact with the axioms?

For this problem, breadth is good.
Blending is bad.
