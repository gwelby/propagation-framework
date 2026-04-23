# Koide Phase: Edge-Ratio Audit

**Date**: 2026-04-20  
**Author**: Codex  
**Builds on**: [koide_phase_projective_invariant_audit_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_projective_invariant_audit_2026-04-20.md)

---

## 1. Why this pass exists

After the projective-invariant audit, the next bounded question was:

> beyond the canonical slope `tan(delta)`, what other **natural** ratio variables are attached to
> the Koide square-root triangle, and do any of them land unusually close to simple rationals?

The motivation is straightforward:

- `tan(delta)` is mathematically canonical
- but on the charged-lepton data it is **not** especially close to `2/9`

So perhaps some other geometrically natural ratio is cleaner.

---

## 2. The natural edge ratios

Let

- `s0 = sqrt(m_tau)`
- `s1 = sqrt(m_e)`
- `s2 = sqrt(m_mu)`

in the standard repo convention `k=(tau=0, e=1, mu=2)`.

The most natural basis-free ratios built directly from the square-root triple are the edge
differences:

- `e01 = s0 - s1`
- `e12 = s2 - s1`
- `e02 = s0 - s2`

and the corresponding edge ratios:

- `R12/01 = e12 / e01`
- `R12/02 = e12 / e02`
- `R01/02 = e01 / e02`

These are more geometric than an arbitrary basis change because they use only the square-root mass
differences themselves.

---

## 3. Exact dependence on the projective variable

Let `t = tan(delta)`.

Using the Koide parametrization and trig identities, these edge ratios reduce exactly to:

- `R12/01 = 2 t / (t + sqrt(3))`
- `R12/02 = -2 t / (t - sqrt(3))`
- `R01/02 = -(t + sqrt(3)) / (t - sqrt(3))`

So:

1. all three edge ratios are exact Möbius transforms of the single invariant `t = tan(delta)`
2. there is still only **one** projective degree of freedom

Indeed, the ratios satisfy exact identities:

- `R01/02 = 1 + R12/02`
- `R12/01 = (R12/02) / (R01/02)`

This is the crucial caution:

> the edge ratios may look cleaner numerically, but they are not independent new structure.

---

## 4. Charged-lepton values

With PDG 2024 charged-lepton masses:

- `R12/01 = 0.230807225022`
- `R12/02 = 0.300064213458`
- `R01/02 = 1.300064213458`

These are strikingly close to small rationals:

- `R12/01 ≈ 3/13 = 0.230769230769`  (relative error `0.0165%`)
- `R12/02 ≈ 3/10 = 0.300000000000`  (relative error `0.0214%`)
- `R01/02 ≈ 13/10 = 1.300000000000` (relative error `0.00494%`)

The three approximants are mutually consistent:

- `13/10 = 1 + 3/10`
- `3/13 = (3/10) / (13/10)`

That consistency is not surprising, because the exact quantities obey the same algebraic
relations.

---

## 5. What this means

This pass produces one real refinement:

> the projective reformulation does uncover a geometrically natural family of low-denominator
> rational approximants built from edge ratios of the square-root mass triangle.

But it also produces the main warning:

> these do **not** count as three new signals. They are all reparameterizations of the same single
> projective invariant `tan(delta)`.

So the correct interpretation is:

- the rational structure survives the projective reformulation in a cleaner geometric language
- but it does not yet become theorem-like evidence for a selector

---

## 6. Comparison with the original 2/9 angle anchor

The original empirical angle result remains stronger in one specific sense:

- `delta ≈ 2/9` has relative error `0.00333%`

The edge-ratio approximants are weaker numerically:

- `R01/02 ≈ 13/10` has relative error `0.00494%`
- `R12/01 ≈ 3/13` has relative error `0.0165%`
- `R12/02 ≈ 3/10` has relative error `0.0214%`

So the edge-ratio reformulation is useful, but it does **not** beat the original 2/9 empirical
anchor on numerical sharpness.

---

## 7. Honest status

What survives:

- The Koide phase problem should now be thought about in projective terms.
- The canonical invariant is `tan(delta)`.
- The natural edge-ratio coordinates produce clean low-denominator rational approximants.

What does not survive:

- the naive claim `tan(delta)=2/9`
- any suggestion that the edge-ratio rationals are independent evidence beyond the single
  projective degree of freedom

---

## 8. Best current sentence

The best honest sentence after this pass is:

> The charged-lepton Koide geometry has one natural projective degree of freedom. In canonical
> coordinates that invariant is `tan(delta)`, and in edge coordinates it appears as the Möbius
> family `R12/01`, `R12/02`, `R01/02`. Those edge ratios land near simple rationals such as
> `3/13`, `3/10`, and `13/10`, but because they are exact transforms of the same `tan(delta)`
> variable, they sharpen the geometry without yet closing the selector problem.

---

## 9. Reproducibility

See:

- [koide_projective_invariants.py](/mnt/d/Fundamentals/sandbox/koide_projective_invariants.py)

The updated script now prints:

- `delta`
- `tan(delta)`
- the natural edge ratios
- their exact dependency relations
- best small-denominator rational approximants for each

