# Koide Phase: Projective Invariant Audit

**Date**: 2026-04-20  
**Author**: Codex  
**Trigger**: Alejandro Rivero's clarification:

> "the rational is always tan theta, never theta"

**Purpose**: Reframe the Koide phase search from a literal-angle target to the natural
projective/slope variables of the Koide square-root mass geometry.

---

## 1. The corrected mathematical question

Rivero's sentence is the right filter.

If a rational is structurally natural, it should usually belong to a **projective / slope-like
variable**, not directly to a literal geometric angle.

So the bounded question becomes:

> what is the canonical reduced ratio variable of the Koide square-root triple, and does **that**
> variable land on a simple rational?

This is narrower and more honest than the earlier "why is `delta = 2/9` in radians?" framing.

---

## 2. Exact derivation of the canonical slope variable

Use the standard Koide parametrization in the repo convention `k=(0,1,2)`:

`sqrt(m_k) = A * (1 + sqrt(2) * cos(delta + 2*pi*k/3))`

Define the square-root mass vector

`s = (s_0, s_1, s_2) = (sqrt(m_0), sqrt(m_1), sqrt(m_2))`

and its centered version

`z = s - A*(1,1,1)`, where `A = (s_0 + s_1 + s_2)/3`.

The natural Koide plane is the 2D subspace orthogonal to `(1,1,1)`.  
Choose the orthogonal basis

- `u = (1, -1/2, -1/2)`
- `v = (0, -sqrt(3)/2, sqrt(3)/2)`

Then the centered Koide vector decomposes exactly as

`z = sqrt(2) * A * (cos(delta) * u + sin(delta) * v)`.

Therefore the canonical coordinates are

- `X = (2*s_0 - s_1 - s_2)/3 = sqrt(2) * A * cos(delta)`
- `Y = (s_2 - s_1)/sqrt(3)   = sqrt(2) * A * sin(delta)`

and the canonical projective invariant is

`Y / X = tan(delta)`.

Equivalently,

`tan(delta) = sqrt(3) * (s_2 - s_1) / (2*s_0 - s_1 - s_2)`.

This is the clean mathematical consequence of Rivero's distinction.

---

## 3. Charged-lepton evaluation

Using the repo convention for charged leptons:

- `m_0 = m_tau`
- `m_1 = m_e`
- `m_2 = m_mu`

with PDG 2024 values:

- `m_e = 0.51099895 MeV`
- `m_mu = 105.6583755 MeV`
- `m_tau = 1776.86 MeV`

the extracted quantities are:

- `delta_exact = 0.222229631490 rad`
- `2/9 = 0.222222222222 rad`
- `|delta - 2/9| = 7.409e-06 rad`

but the canonical projective invariant is

- `tan(delta_exact) = 0.225961718896`

which is **not** equal to `2/9`.

Relative gap:

`(tan(delta_exact) - 2/9) / (2/9) ≈ 1.68%`.

So the naive replacement

`"the true rational is tan(delta) = 2/9"`

does **not** survive contact with the charged-lepton data.

---

## 4. Rational approximation check

The earlier empirical anchor remains true:

- for denominators `q <= 36`, the angle `delta` is exceptionally well approximated by `2/9`

But for the canonical slope variable:

- the best small-denominator rational with `q <= 36` is `7/31 = 0.225806451613`
- error `|tan(delta) - 7/31| ≈ 1.55e-4`

This is a respectable approximation, but it is not the same kind of striking anchor as
`delta ≈ 2/9`.

So the projective reformulation does **not** preserve the exact same rational target automatically.

---

## 5. What survives from Rivero's sentence

Rivero's correction survives in a precise sense:

- the mathematically natural object is indeed a slope/projective variable
- in the canonical Koide plane that object is exactly `tan(delta)`

What does **not** survive is the stronger leap:

- that the measured charged-lepton phase therefore corresponds to `tan(delta) = 2/9`

That specific identification is false for the current data.

---

## 6. Updated interpretation of Issue #5

The issue should now be split conceptually into two layers:

### Layer A — empirical angle anchor

The measured charged-lepton phase still sits extremely close to `2/9 rad`.

This remains an empirical fact and should stay in `CLAIMS.md` as such.

### Layer B — mathematical selector class

Rivero's clarification says the selector should probably not act directly on the angle, but on a
reduced projective variable.

For the canonical Koide geometry, that variable is `tan(delta)`.

But since `tan(delta) != 2/9`, the search target changes:

> if a simple rational survives, it must likely appear in some **other** reduced invariant of the
> Koide geometry, not in the naive canonical slope itself.

---

## 7. What the repo should not say now

Do not say:

- "Rivero solved the issue"
- "the true invariant is `tan(delta)=2/9`"
- "the 2/9 anchor has been rederived projectively"

None of those are supported by this audit.

---

## 8. What the repo can say now

It is now defensible to say:

> The Koide phase search should be reformulated in projective terms. The canonical reduced
> invariant of the Koide square-root mass triangle is `tan(delta)`, not `delta` itself. On the
> charged-lepton data, `tan(delta)` is approximately `0.2259617`, so the naive equation
> `tan(delta)=2/9` fails. Rivero's distinction therefore sharpens the mathematical class of the
> problem, but does not close it.

---

## 9. Immediate next step

The next bounded pass should be:

1. enumerate the other natural projective invariants of the Koide geometry beyond the canonical
   slope `tan(delta)`
2. test whether any of them land near unusually simple rationals
3. keep the current empirical `delta ≈ 2/9` row unchanged until such an invariant is found

---

## 10. Reproducibility

See:

- [koide_projective_invariants.py](/mnt/d/Fundamentals/sandbox/koide_projective_invariants.py)

That script:

- derives the canonical Koide-plane coordinates
- verifies `Y/X = tan(delta)`
- evaluates the charged-lepton data
- compares rational approximants for `delta` and `tan(delta)`

