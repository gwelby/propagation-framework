# Axiom 3 Candidate Functional F1 — Primitive Closure Action
*First explicit free-energy / Lyapunov-style candidate for selecting the fundamental helical PF mode*

**Date**: 2026-03-23
**Author**: Codex
**Status**: Candidate only — not yet audited, not integrated into `CLAIMS.md` or `ACTIVE_ISSUES.md`
**Purpose**: Provide one explicit mathematical object for the team to attack, instead of another loose route
**Builds on**: `axiom3_coherence_functional_spec.md`, `casimir_polynomial_step_B_audit.md`, `casimir_polynomial_synthesis.md`, `casimir_polynomial_claude_independent_pass.md`

---

## 1. What This Candidate Is Trying to Do

The Step B gap is:

> among coherent helical resonances, why does PF select `k = 1` rather than another rational resonance?

The strongest current ideas are:

- minimum energy for fixed angular content
- primitive (non-multiple-winding) loop

These have been treated as two separate stories.
This candidate tries to unify them.

The proposed principle is:

> **A PF coherent structure is selected by minimizing the action cost required for one primitive self-return of the mode.**

This is not yet derived from Axiom 3.
It is a clean candidate formalization of the missing Step B selection rule.

---

## 2. Domain: the Helical Resonance Family

Fix:

- mass `m`
- angular content `C₂ = j(j+1) > 0`

Consider coherent helical resonances labeled by coprime positive integers `(p, q)`:

- `p` = number of drift-action units
- `q` = number of internal cycles in the primitive closure

Write:

`k = p/q`

so that the resonance condition family is

`J_z = k J_θ`.

Using the current helical language:

- `J_θ = 2π√C₂ ħ`  (Step A target; still strong argued)
- `J_z = 2πγβ² ħ`  (substantially resolved on the helix torus)

So the `(p, q)` family satisfies

`γβ² = (p/q) √C₂`.

This file does **not** derive that family.
It assumes the family as the candidate coherent branch on which Step B must choose.

---

## 3. Primitive Closure Time

Let the internal fundamental period be

`T₀ = 2π r_C / c = 2πħ / (m c²)`

using `r_C = ħ/(mc)`.

For a `p:q` resonance, the first primitive self-return occurs after `q` internal cycles:

`T_prim(p,q) = q T₀`.

This is the smallest time after which the composite helical pattern closes back on itself as a primitive loop.

This is the topological piece:

- larger `q` means a longer primitive closure cell
- even if the state is coherent, it takes longer to complete one irreducible self-return

---

## 4. Candidate Functional

Define the dimensionless closure-action cost:

`F₁(p,q; C₂) = E_{p:q} T_prim(p,q) / (2πħ)`

where

`E_{p:q} = γ_{p:q} m c²`.

Substitute `T_prim = q (2πħ)/(mc²)`:

`F₁(p,q; C₂) = q γ_{p:q}`.

Interpretation:

> `F₁` is the number of action quanta spent to carry the helical mode through one primitive self-return.

This is a genuine free-energy / Lyapunov-style candidate because it combines:

- energetic cost (`γ mc²`)
- topological / temporal complexity of primitive closure (`q T₀`)

It does **not** contain:

- `(J_z - J_θ)²`
- `(k - 1)²`
- `(\gammaβ² - √C₂)²`

So it does not build in the target answer directly.

---

## 5. Explicit Formula

Let

`s = √C₂`

and

`a = (p/q) s`.

From the resonance-family condition:

`γβ² = a`

and using `β² = 1 - 1/γ²`,

`γ - 1/γ = a`

so

`γ² - aγ - 1 = 0`.

Taking the positive root:

`γ(a) = (a + √(a² + 4)) / 2`.

Therefore:

`F₁(p,q; C₂) = q γ((p/q)s)`

which simplifies to

`F₁(p,q; C₂) = (p s + √(p² s² + 4 q²)) / 2`.

This is the closed-form candidate functional on the helical resonance family.

---

## 6. Key Result: F₁ Selects the 1:1 Primitive Resonance

### Proposition

For fixed `C₂ > 0` and positive coprime integers `(p, q)`, the functional

`F₁(p,q; C₂) = (p s + √(p² s² + 4 q²)) / 2`

is uniquely minimized at

`(p, q) = (1, 1)`.

### Proof

Let `s = √C₂ > 0`.

Then:

- the first term `(p s)/2` is strictly increasing in `p`
- the second term `√(p² s² + 4 q²)/2` is strictly increasing in both `p` and `q`

Hence `F₁` is strictly increasing in `p` for fixed `q`, and strictly increasing in `q` for fixed `p`.

Since the allowed domain is positive integers `p ≥ 1`, `q ≥ 1`, the unique global minimum occurs at the smallest allowed pair:

`(p, q) = (1, 1)`.

Therefore:

`arg min F₁ = (1,1)`

which is exactly the `1:1` resonance, i.e. `k = p/q = 1`.

QED.

---

## 7. What This Would Give If Accepted

If Axiom 3 is formalized as:

> the stable fundamental helical mode minimizes the primitive closure-action cost `F₁`

then:

1. `F₁` selects `(p,q) = (1,1)`
2. so `k = 1`
3. so `J_z = J_θ`
4. so `γβ² = √C₂`
5. and therefore the Casimir polynomial follows

`u² + C₂ u - C₂ = 0`

with `u = β²`.

This would close Step B.

It would **not** by itself close Step A.

---

## 8. Why This Candidate Is Better Than "Minimum Energy" Alone

Pure minimum energy by itself is too loose:

- it does not distinguish primitive closure complexity
- it leaves ambiguity about whether lower-energy but more weakly matched states should count as equally fundamental

Pure primitive-loop language by itself is also too loose:

- it does not explain why primitive closure should dominate dynamically
- it can sound topological but not variational

`F₁` unifies the two:

- **energy** says how expensive the state is to sustain
- **primitive closure time** says how long it takes to complete one irreducible self-return

So `F₁` is exactly:

> action cost per primitive coherent cell

This is the cleanest single scalar I currently see for Step B.

---

## 9. Why This Still Might Fail

This candidate is promising.
It is not yet a derivation.

Three real risks remain.

### Risk 1: The variational principle itself is not yet derived

The proposition above proves:

- **if** PF minimizes `F₁`
- **then** PF selects `k = 1`

What it does **not** prove is:

- why Axiom 3 should minimize `F₁` specifically

That is still the core conceptual step.

### Risk 2: The candidate lives on the resonance family, not on all field configurations

`F₁` is defined on the helical resonance family `(p,q)`.

A deeper PF functional should ideally live on a broader configuration space and reduce to `F₁` on this family.

So `F₁` may be:

- the effective reduced functional on the Casimir sector
- not yet the full Axiom 3 functional

### Risk 3: Step A is still only strong argued

This candidate assumes the relevant angular quantity is `√C₂`.

If Step A later changes, `F₁` would have to be rebuilt.

So `F₁` is best understood as:

> a candidate Step B functional conditional on the current Step A language

---

## 10. Anti-Smuggling Check

Against `axiom3_coherence_functional_spec.md`, `F₁` does reasonably well:

- it separates threshold/selection better than prior route language
- it does not contain an explicit `(k-1)²` or `(J_z - J_θ)²` penalty
- it uses relativistic data through `γ`
- it naturally represents higher resonances rather than banning them by fiat

What it does **not** yet pass:

- a derivation that Axiom 3 should minimize closure action cost
- a translation into the two-sector Route G language
- a field-level definition beyond the reduced helical family

So `F₁` should be treated as:

- a serious candidate
- not a proof

---

## 11. Best Next Audit Questions

This candidate gives the team a much better bounded target.

The next questions should be:

1. **Codex audit question**
   - Is `F₁` genuinely non-smuggled, or does the primitive closure definition secretly force `1:1`?

2. **Claude question**
   - Can `F₁` be derived from a broader Hamiltonian / free-energy picture rather than proposed directly on the resonance family?

3. **Cascade question**
   - Can the information-theoretic route produce the same reduced scalar `F₁` or a monotone equivalent?

4. **Qwen question**
   - Numerically scan `F₁(p,q; C₂)` over relevant low-spin sectors and compare with any alternative candidate functionals.

5. **AntiGravity question**
   - Is the primitive closure time `q T₀` the right irreducible cell, or is that where the answer is being smuggled in?

---

## 12. Honest Verdict

This is the first candidate functional I would actually want the team to attack.

It is valuable because it converts the vague Step B question into a clear statement:

> PF may be selecting the coherent state that minimizes the action required for one primitive self-return.

That is mathematically crisp.
It selects `1:1` cleanly.
And it is still honest about what remains unproved.

That makes it a good next object for the team, regardless of whether it survives audit.
