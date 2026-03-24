# Casimir Polynomial — Codex Audit of Step A
*Does Axiom 2 really derive `J_θ = 2π√C₂ħ`, or only motivate it strongly?*

**Date**: 2026-03-22
**Author**: Codex
**Scope**: Audit `casimir_polynomial_steps_AB.md` Step A against the canonical PF docs
**Verdict**: ARGUED (strong) — not yet fully derived

---

## 1. The Claim Being Audited

Step A claims:

> Axiom 2 (causal velocity) implies spatial isotropy of the PF medium.
> Therefore stable PF modes are SO(3)-stationary, and the internal action must use the
> angular momentum magnitude `|J| = √C₂ħ`, not a projection `m_j ħ`.
> Hence `J_θ = 2π√C₂ħ`.

This is the right target.
It is also slightly stronger than what the current formal chain supports.

---

## 2. What Survives the Audit

Two parts are solid.

### Surviving part 1: PF strongly reads the vacuum medium as isotropic

The canonical framework treats vacuum propagation using scalar `c`, spherical wavefronts, and no preferred spatial direction; see [the_propagation_framework.md](/mnt/d/Fundamentals/the_propagation_framework.md#L33) and [the_propagation_framework.md](/mnt/d/Fundamentals/the_propagation_framework.md#L79).

The broader repo also repeatedly treats the local causal velocity as a scalar rather than a vector field; see [propagation_lagrangian.md](/mnt/d/Fundamentals/derivations/propagation_lagrangian.md#L75).

So "PF medium is isotropic" is a strong internal reading of the framework.

### Surviving part 2: `√C₂` is the unique SO(3)-invariant angular scale

If the relevant quantity must be SO(3)-invariant, then the magnitude

`|J| = √(j(j+1)) ħ = √C₂ ħ`

is the natural invariant, whereas `m_j ħ` is axis-dependent.

That part is standard representation theory and is fine.

---

## 3. Why Step A Does Not Yet Count as DERIVED

### Objection 1: Axiom 2 does not explicitly state isotropy

Axiom 2 says every medium has a finite causal velocity. It does **not** explicitly say that this velocity is the same in all directions.

The repo often reads it that way, and likely correctly for vacuum, but the isotropy statement is still an interpretive strengthening, not a literal line-by-line consequence of the axiom text alone.

### Objection 2: isotropy of the medium does not by itself force isotropic internal motion

Even in an isotropic medium, a particular stable mode can carry a definite oriented angular momentum state.

SO(3) symmetry guarantees degeneracy structure and invariant labels like `J²`; it does **not** by itself prove that the mode's internal action cycle explores all orientations equally or "precesses freely over all directions."

That is the key hidden step in Step A.

### Objection 3: the action integral still needs its cycle specified

To conclude

`J_θ = 2π|J|`

one must specify what loop the internal action is taken around.

If the cycle is a full invariant precession orbit in angular-momentum space, then the magnitude is natural.
If the cycle is an azimuthal orbit around a chosen axis, then a projection-like quantity is natural.

Step A currently chooses the first interpretation without deriving why that is the correct internal cycle for a PF fundamental mode.

That is a dynamical claim, not just a symmetry claim.

---

## 4. Correct Audited Status

The honest audited status is:

> **ARGUED (strong)**: If the PF fundamental mode's internal cycle is itself SO(3)-invariant — equivalently, if the mode does not pick a preferred spin axis in the medium — then `J_θ = 2π√C₂ħ` follows cleanly.

That is a very good argument.
It is not yet a completed derivation from the canonical axioms alone.

---

## 5. What Would Close Step A

Any one of the following would likely close it:

1. A direct derivation that the internal circulation of a PF fundamental mode is an SO(3)-invariant orbit rather than an axis-fixed one.
2. A PF-native definition of the internal action as an invariant functional on the SO(3) orbit of the mode.
3. A cleaner statement in the canonical framework that vacuum causal propagation is isotropic and fundamental stable modes inherit that isotropy at the level of their internal coherence cycle.

Until then, the correct board status is:

- not `DERIVED`
- not weak speculation
- **strong argued**

---

## 6. Bottom Line

Step A is closer than Step B.

But it is not closed yet.

The precise surviving statement is:

> The PF strongly suggests that the relevant angular action should use the SO(3)-invariant magnitude `√C₂ħ`; what is still missing is the derivation that the internal cycle of a fundamental mode is itself the invariant one.
