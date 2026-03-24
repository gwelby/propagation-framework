# Casimir Polynomial — Codex Audit of Route F
*Does drift-rotation locking actually derive the extra factor of `β`, or does it restate the gap geometrically?*

**Date**: 2026-03-21
**Author**: Codex
**Scope**: Audit `casimir_polynomial_route_F.md` against `casimir_polynomial_route_A.md` and the PF axioms
**Verdict**: C (strong gap reduction) — Route F is the clearest geometric ansatz so far, but not yet a derivation

---

## 1. What Route F Gets Right

Route F identifies the right target.

Route A showed the exact discrepancy:

- standard relativistic circular mechanics gives `γβ = √C₂`
- the Casimir polynomial requires `γβ² = √C₂`

Route F provides a clean geometric way to generate the extra factor:

- replace the fixed radius `r_C` with a locking radius `r_lock = β r_C`
- then `L = γ m v r_lock = γβ² ħ`

That is a real structural gain. It says the extra `β` can be read as a radius-selection issue rather than as an arbitrary algebraic correction.

---

## 2. Main Audit Finding

As written, Route F does **not** derive `r_lock = β r_C` from Axiom 3.

It introduces that result through a new, model-specific locking ansatz:

1. assume an internal circulation with angular velocity `ω = c / r_C`
2. assume a tangential profile `v_tang(r) = ω r`
3. define a "coherence functional" by velocity mismatch
   `Φ(r) = ω r - v`
4. declare coherence at `Φ = 0`

This is physically suggestive, but it is not yet a PF derivation.

The route therefore converts the gap into a sharper geometric question:

> why should Axiom 3 select `r = v / ω` as the characteristic coherence radius of a drifting spinning mode?

That is valuable, but it is still a gap.

---

## 3. Specific Audit Objections

### Objection 1: The "coherence functional" is not yet a phase functional

Route F calls

`Φ(r) = ω r - v`

a phase mismatch, but this quantity has units of velocity, not phase.

That does not make the idea wrong, but it means the decisive step is not yet derived from the PF statement that stable structure requires coherent **phase** relationships.

To close this, Route F would need one of:

- an actual phase-closure condition over a loop with internal circulation and drift
- an action or stationarity principle whose extremum gives `ω r = v`
- a bona fide coherence functional built from dimensionless phase data

Without that, the locking condition is an ansatz.

### Objection 2: Hidden rigid-rotation assumption

Route F starts from a loop of natural radius `r_C` and angular velocity `ω = c / r_C`, then evaluates tangential velocity at an arbitrary interior radius via

`v_tang(r) = ω r`.

That is a rigid-rotation profile. It is not supplied by Axioms 1-3, and it is not a consequence of Route A.

This matters because the derivation of `r_lock = β r_C` depends entirely on being allowed to slide to a smaller radius while keeping the same `ω`.

### Objection 3: The route identifies the lock radius with the angular-momentum radius

After obtaining `r_lock = β r_C`, Route F uses

`L = γ m v r_lock`

as the angular momentum of the mode.

But the physical loop that originally defined `ω = c / r_C` lives at `r_C`, not obviously at `r_lock`.

So the route still owes a derivation of why the radius selected by its locking ansatz is also the radius that enters the relativistic angular momentum of the coherent mode.

This is exactly where the extra factor of `β` enters. The route has localized the gap, but not removed it.

---

## 4. What Survives the Audit

Three claims survive cleanly:

1. The extra-`β` problem is geometrically expressible as a radius-selection problem.
2. The most promising geometric candidate is a drift-rotation locking condition.
3. Route F is best read as a reformulation of Gap A, not as closure of Gap A.

Equivalently:

- Route A phrased the gap as `γβ²` versus `γβ`
- Route F phrases the same gap as `r = β r_C` versus `r = r_C`

Those are two languages for the same unresolved step.

---

## 5. Synthesis Impact

Route F should not currently be treated as:

- a derivation
- "B+" in the sense of nearly closed

It should be treated as:

- **strong gap reduction**
- the best current geometric ansatz for the extra-`β` factor

The leading gap after this audit is:

> Derive from a genuine PF coherence principle why a spinning mode with internal circulation and external drift selects the locking condition `r = v / ω = β r_C`, or equivalently why PF privileges the variable `pv/(mc²) = γβ²` rather than `p/(mc) = γβ`.

This leaves Gap G intact:

> what PF operator couples kinematic and angular sectors with strength `√C₂`?

The two gaps may still be the same mechanism in one-mode and two-sector language.

---

## 6. Honest Verdict

Route F is promising.

It is also not closed.

Its real contribution is that it sharpens the extra-`β` discrepancy into a specific geometric ansatz that future work can now attack directly:

`coherence → locking radius → extra β`

That is progress. It is not yet a derivation.
