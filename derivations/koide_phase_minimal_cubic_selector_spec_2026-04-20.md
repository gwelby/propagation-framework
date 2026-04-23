# Koide Phase: Minimal Cubic Selector Spec

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Tighten the PF-native nonlinear 3-cycle lane from a vague "maybe some cubic observable"
to an exact algebraic target.

---

## 1. Why this note exists

The previous audits already established:

- PF naturally gives the `cos(3 n delta)` harmonic tower
- natural symmetric three-body composites reduce to the single scalar

  `f(delta) = -1/2 + cos(3 delta)/sqrt(2)`

- simple powers `f^k` do not make `cos(9 delta)` dominant

That still leaves too much slack. "Some nonlinear observable" is not precise enough.

The sharper question is:

> inside the scalar reduced variable `f(delta)`, what is the **lowest-degree polynomial class**
> that can isolate the `n = 3` harmonic exactly?

This note answers that question.

---

## 2. Setup

Write

`x = cos(3 delta)`.

Then the PF / Koide scalar from the earlier reduction is

`f(delta) = -1/2 + x/sqrt(2)`.

So any scalar selector built only from the symmetric reduced phase variable is a function

`Q(f(delta)) = R(x)`

for some scalar function `R`.

The target harmonic is

`cos(9 delta) = T_3(x) = 4 x^3 - 3 x`,

where `T_3` is the third Chebyshev polynomial.

---

## 3. Degree barrier

### Theorem 1

No polynomial selector `Q(f)` of degree `< 3` can isolate `cos(9 delta)`.

### Proof

Because `f` is affine-linear in `x`, a polynomial `Q(f)` of degree `d` becomes a polynomial
`R(x)` of degree `d`.

But `cos(9 delta) = T_3(x) = 4 x^3 - 3 x` is cubic in `x`.

Therefore:

- degree `0` gives only a constant
- degree `1` gives only constant + `cos(3 delta)`
- degree `2` gives only constant + `cos(3 delta)` + `cos(6 delta)`

So degree `< 3` cannot produce pure `cos(9 delta)`.

This is exact.

---

## 4. Minimal cubic class

Take the most general cubic polynomial in the reduced scalar:

`Q(f) = A + B f + C f^2 + D f^3`.

Substitute `f = -1/2 + x/sqrt(2)`. After expansion,

`Q(f(delta)) = q_0 + q_1 x + q_2 x^2 + q_3 x^3`

with coefficients

`q_3 = (sqrt(2)/4) D`

`q_2 = (1/2) C - (3/4) D`

`q_1 = (sqrt(2)/2) B - (sqrt(2)/2) C + (3 sqrt(2)/8) D`

`q_0 = A - B/2 + C/4 - D/8`.

To get a pure `cos(9 delta)` selector up to scale and additive constant, we require

`Q(f(delta)) = c + k (4 x^3 - 3 x)`.

Matching coefficients gives a unique cubic family:

`D = 8 sqrt(2) k`

`C = 12 sqrt(2) k`

`B = 3 sqrt(2) k`

`A = c - (sqrt(2)/2) k`.

### Theorem 2

Inside the scalar reduced variable `f(delta)`, the exact pure-`cos(9 delta)` cubic selector is
unique up to overall scale and additive constant.

Equivalently,

`Q_*(f) = c + sqrt(2) k (8 f^3 + 12 f^2 + 3 f - 1/2)`

and

`Q_*(f(delta)) = c + k cos(9 delta)`.

This is exact.

---

## 5. Minimal exact selector in normalized form

Dropping the irrelevant additive constant and overall scale, the minimal cubic content is

`8 f^3 + 12 f^2 + 3 f`.

Indeed,

`sqrt(2) (8 f^3 + 12 f^2 + 3 f - 1/2) = cos(9 delta)`.

So the scalar problem is now completely sharp:

> if a PF-native scalar selector exists in the reduced phase variable, then the first exact
> candidate is not "some cubic". It is this Chebyshev-tuned cubic.

---

## 6. What this changes

### 6.1 Simple nonlinear language is no longer enough

Saying "the selector is cubic" is too weak.

Most cubic choices

`A + B f + C f^2 + D f^3`

still contain a mixture of:

- `cos(3 delta)`
- `cos(6 delta)`
- `cos(9 delta)`

The lower harmonics disappear only on the tuned coefficient locus above.

### 6.2 The physical burden is now explicit

The missing step is no longer:

> invent a nonlinear observable.

It is now:

> derive why PF would choose the specific coefficient ratio
>
> `B : C : D = 3 : 12 : 8`
>
> in the reduced scalar basis.

That is a much narrower and more auditable demand.

### 6.3 This is a real filter on future claims

Any future selector claim that reduces to a scalar polynomial in `f` must answer:

1. does it reach degree `>= 3`?
2. if cubic, does it land on the tuned Chebyshev locus?
3. if not, what dynamical or nonlocal structure cancels the lower harmonics instead?

If it does not answer these, it is not closing the `delta = 2/9` selector problem.

---

## 7. What this does not prove

This note does **not** derive the Koide phase selector.

It also does **not** show that PF prefers the cubic Chebyshev combination.

It only proves:

- the exact minimal scalar degree
- the exact tuned cubic family
- the precise algebraic burden any PF-native scalar selector must satisfy

So this is a boundary-setting result, not a closure result.

---

## 8. Consequences for the live search

The remaining serious PF-native lane is now even narrower:

### Lane A — derive the tuned cubic

Find a PF-native three-cycle observable, coherence functional, or effective action whose reduced
scalar form is exactly the Chebyshev-tuned cubic above.

### Lane B — leave the scalar lane entirely

Show that the physical selector is not a scalar polynomial in `f`, but a matrix / trace / nonlocal
observable whose reduction produces the same coefficient cancellation after integrating out extra
structure.

### Dead lane

Keep trying:

- powers `f^k`
- generic "more nonlinear" slogans
- new rational approximants of slopes or edge ratios

These no longer move the problem.

---

## 9. Final verdict

The projective lane is fenced, and the scalar nonlinear lane is now sharply bounded.

Inside the PF-reduced scalar variable `f(delta)`, the first exact `cos(9 delta)` selector is the
unique Chebyshev-tuned cubic

`Q_*(f) = c + sqrt(2) k (8 f^3 + 12 f^2 + 3 f - 1/2)`.

Therefore the real open problem is not "could some cubic do it?" but:

> what physical principle, if any, forces PF to choose that cubic rather than a generic mixture?

That is the next honest question.
