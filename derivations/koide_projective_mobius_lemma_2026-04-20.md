# Koide Projective Möbius Lemma

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Close the bounded projective-classification task triggered by Alejandro Rivero's
`"the rational is always tan theta, never theta"` correction.

---

## 1. Why this lemma exists

After Rivero's correction, the natural move was to reformulate the Koide phase problem in
projective terms.

The immediate danger in that lane is obvious:

- keep forming new ratios from the square-root mass triple
- find more small-denominator rational approximants
- mistake reparameterizations of the same object for new structure

This lemma closes that loophole.

---

## 2. Setup

Work in the standard Koide parametrization

`sqrt(m_k) = A * (1 + sqrt(2) * cos(delta + 2*pi*k/3))`,  `k = 0,1,2`.

Let

- `s = (s_0, s_1, s_2) = (sqrt(m_0), sqrt(m_1), sqrt(m_2))`
- `A = (s_0 + s_1 + s_2)/3`
- `z = s - A*(1,1,1)`

Then `z` lies in the 2D Koide plane orthogonal to `(1,1,1)`.

Choose the standard orthogonal basis

- `u = (1, -1/2, -1/2)`
- `v = (0, -sqrt(3)/2, sqrt(3)/2)`

so that

`z = sqrt(2) * A * (cos(delta) * u + sin(delta) * v)`.

Define the canonical projective coordinate

`t := tan(delta)`.

---

## 3. Lemma

### Lemma

Any nonconstant projective coordinate on the Koide line obtained as the ratio of two affine-linear
functions of the square-root masses is a Möbius transform of `t = tan(delta)`.

Equivalently: if

`R(s) = (alpha_0 s_0 + alpha_1 s_1 + alpha_2 s_2 + alpha_3) / (beta_0 s_0 + beta_1 s_1 + beta_2 s_2 + beta_3)`

and the restriction of `R` to the Koide one-parameter family is nonconstant, then on that family
it has the form

`R(delta) = (a t + b) / (c t + d)`

for constants `a,b,c,d` not all zero, with `ad - bc != 0` in the nondegenerate case.

---

## 4. Proof

On the Koide family,

`s_k = A + z_k`

with `z_k` linear in `cos(delta)` and `sin(delta)`.

So any affine-linear form in `s`

`L(s) = gamma_0 s_0 + gamma_1 s_1 + gamma_2 s_2 + gamma_3`

restricts to a function of the form

`L(delta) = p * cos(delta) + q * sin(delta) + r`

for constants `p,q,r`.

Now divide numerator and denominator by `cos(delta)` on any chart where `cos(delta) != 0`. Since

- `tan(delta) = t`
- `1 = cos(delta) / cos(delta)`
- `sin(delta) / cos(delta) = t`

the ratio of two such linear forms becomes

`R(delta) = (a t + b) / (c t + d)`

for suitable constants `a,b,c,d`.

This is exactly a Möbius transformation of `t`.

Since the Koide family is one-dimensional in projective terms, there is only one independent
projective degree of freedom. Therefore no new ratio built this way can produce an independent
selector variable; it can only reparameterize `t`.

QED.

---

## 5. Concrete examples

From the charged-lepton square-root triple:

- canonical slope:
  `t = tan(delta) = Y/X`

with

- `X = (2*s_0 - s_1 - s_2)/3`
- `Y = (s_2 - s_1)/sqrt(3)`

Natural edge-ratio variables are:

- `R12/01 = (s_2 - s_1)/(s_0 - s_1) = 2t / (t + sqrt(3))`
- `R12/02 = (s_2 - s_1)/(s_0 - s_2) = -2t / (t - sqrt(3))`
- `R01/02 = (s_0 - s_1)/(s_0 - s_2) = -(t + sqrt(3)) / (t - sqrt(3))`

These are exact Möbius transforms of the same single invariant `t`.

So:

- `3/13`
- `3/10`
- `13/10`

may be cleaner rational approximants numerically, but they do not represent new independent
geometric structure.

---

## 6. What this closes

This lemma closes the bounded question:

> are we learning anything fundamentally new by generating more ratios from the square-root mass
> triple?

Answer:

> not if those ratios are affine/projective coordinates on the same Koide line.

They are all ghosts of the same slope.

That is why the lemma is short: the projective space is only one-dimensional, so the classification
collapses quickly.

---

## 7. What this does NOT close

This lemma does **not** say:

- that `delta` itself is unimportant
- that `tan(delta)` is the selector
- that the Koide phase problem is solved

It only says:

- the **projective reparameterization lane is now fenced**

So the next live lane must be outside this class:

- non-projective upstream labels
- nonlinear observables not reducible to affine ratios of the square-root triple
- PF-native selectors acting on something other than the single Koide slope coordinate

---

## 8. Best honest summary

The bounded projective search is now classified:

> any natural affine/projective coordinate of the Koide square-root mass triple is a Möbius
> transform of `tan(delta)`. Therefore chasing new rational approximants in such coordinates cannot
> by itself reveal a new selector mechanism.

That is a real closure. It is not the solution to Issue #5, but it prevents us from burning time
inside a lane that cannot produce independent structure.

---

## 9. Companion artifacts

- [koide_phase_projective_invariant_audit_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_projective_invariant_audit_2026-04-20.md)
- [koide_phase_edge_ratio_audit_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_edge_ratio_audit_2026-04-20.md)
- [koide_projective_invariants.py](/mnt/d/Fundamentals/sandbox/koide_projective_invariants.py)

