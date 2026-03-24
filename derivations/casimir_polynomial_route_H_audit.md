# Casimir Polynomial — Codex Audit of Route H
*Does the action-resonance note derive the polynomial, or does it sharpen the helical coherence gap?*

**Date**: 2026-03-22
**Author**: Codex
**Scope**: Audit `casimir_polynomial_route_H.md` against the existing Casimir board
**Verdict**: C (strong gap reduction) — cleaner than Route F, but not yet an EBK derivation

---

## 1. What Survives Cleanly

Two pieces of Route H survive the audit without modification.

### Surviving result 1: the algebra for the drift advance is correct

Given the Route H setup:

- internal period `T = 2πr_C/c`
- drift distance per internal cycle `d = vT = 2πβr_C`
- drift momentum `p_z = γmβc`

the product

`p_z d = 2πγβ²ħ`

is algebraically and dimensionally correct after substituting `r_C = ħ/(mc)`.

This is a real gain over the earlier kinetic-power route, which had dimensional problems.

### Surviving result 2: Route H gives the cleanest phase-counting reformulation so far

The quantity

`N_dB = d / λ_dB = γβ²`

is the number of de Broglie wavelengths advanced by the drift during one internal circulation.

That is a legitimate phase-counting quantity.

So Route H does sharpen the problem to:

> why should the drift phase advance per internal cycle equal the angular phase content `√C₂`?

This is a better statement of Gap A/F than the older power-balance wording.

---

## 2. Main Audit Finding

Route H is **not** yet a standard EBK / action-angle derivation.

It takes a physically suggestive phase-counting construction and labels it as an action-resonance theorem. That overstates the current status.

The note should therefore be read as:

- a strong helical phase-matching ansatz
- not yet a canonical action-variable derivation

---

## 3. Specific Audit Objections

### Objection 1: `J_z = p_z d` is not yet a standard action variable

For an action variable in the Hamiltonian/EBK sense, the coordinate must run over a closed periodic cycle:

`J_i = ∮ p_i dq_i`

The angular piece satisfies this: `θ` is periodic, so `J_θ = ∮ p_θ dθ` is standard.

But the drift coordinate `z` is translational, not obviously periodic. Route H defines `J_z = p_z d` over one internal revolution, where `d` is the drift advance during that time. That is a perfectly good **action accumulated over one internal cycle**, or phase increment, but it is not automatically a canonical EBK action variable.

So the phrase "standard EBK action-resonance" is not yet earned.

### Objection 2: resonance is being imposed as equality of actions, not derived as a standard resonance condition

In standard Hamiltonian mechanics, resonance is usually stated as a commensurability of frequencies:

`n · ω = 0`

or equivalently rational relations among angle advances.

Route H instead imposes

`J_z = J_θ`

which is stronger and different. Equal actions are not the generic definition of 1:1 resonance.

This means the core condition is still an extra assumption, just in cleaner language than Route F.

### Objection 3: Route H does not yet close Gap G

Route H claims to answer Route G by identifying the coupling `√C₂` with the angular momentum magnitude.

That is a compatible interpretation, but it is not a derivation of the specific two-sector operator or its off-diagonal matrix element.

So Route H may illuminate Gap G, but it does not yet eliminate it.

### Objection 4: the appended "independent verification" is not independent enough to count as a separate route

The Claude section at the end of Route H restates the same core assumption in wave language:

`N_dB = √C₂`

That is useful corroboration, but not an independent closure of the gap. It also mixes multiple agents into one route note, which weakens the route-separation discipline of the Casimir board.

---

## 4. What Route H Actually Improves

Route H does improve the board in three real ways.

1. It replaces the dimensionally weak "kinetic power" story with a clean phase-counting quantity.
2. It avoids Route F's rigid-rotation and locking-radius machinery.
3. It suggests the right mathematical rescue path: build a **closed helical phase coordinate** so the drift sector becomes genuinely periodic.

That last point matters. If a periodic helical coordinate can be defined, then a true second action variable may emerge, and Route H could become much stronger.

---

## 5. The Sharpened Gap After Audit

The clean surviving question is:

> For a helical PF mode, why must the drift phase advance over one internal cycle satisfy
> `k_z d = 2π√C₂`
> or equivalently
> `N_dB = γβ² = √C₂`?

That is the real content beneath Route H.

This can be phrased three equivalent ways:

- phase-counting language: `N_dB = √C₂`
- action-per-cycle language: `p_z d = 2πL`
- relativistic language: `γβ² = √C₂`

What is still missing is the PF-native principle that forces that equality and excludes higher-order `m:n` relations.

---

## 6. Synthesis Impact

Route H should not currently be treated as:

- a derivation
- standard EBK quantization
- a full resolution of Gap G

It should be treated as:

- **strong gap reduction**
- the best current helical phase-matching reformulation of Gap A/F

The best next formal move is:

> derive a periodic helical coordinate or torus quotient for the drifting spinning mode, then state the coherence condition in terms of true angle variables rather than open drift distance.

If that can be done, Route H may become the right route.

If it cannot, Route H remains an elegant reformulation, not a closure.

---

## 7. Honest Verdict

Route H is the cleanest statement so far of what the extra-`β` wants to mean physically.

It is not yet a theorem.

Its strongest surviving contribution is:

`coherence of a helical mode = phase advance per internal cycle must match angular content`

That is a real improvement.

It is also still one decisive principle short of a derivation.
