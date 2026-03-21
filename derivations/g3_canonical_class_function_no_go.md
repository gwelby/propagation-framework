# G3: Canonical Class-Function No-Go
*Why a gauge-invariant scalar built only from the total SU(2) holonomy cannot fix the G3 coefficient*

**Date**: 2026-03-21  
**Author**: Codex  
**Task**: Test the narrowest remaining holonomy route: can a canonical gauge-invariant observable of the total 3-step SU(2) holonomy close G3?  
**Status**: EXACT RESTRICTION — holonomy-only class functions are underdetermined; extra structure is required  
**Builds on**: `g3_wilson_loop_toy_model.md`, `g3_beta_lock_audit.md`, `g3_closure_via_imperfect_holonomy.md`  
**Current claim status**: Keeps G3 at **PARTIAL / ARGUED (0.60)**  

---

## 1. The Narrow Question

After the Wilson-loop and beta-lock passes, the cleanest remaining idea is:

> maybe there exists a **canonical** gauge-invariant scalar of the total 3-step holonomy
> \(U = K_2 K_1 K_0 \in SU(2)\) that fixes the Planck-boundary coefficient.

This is narrower than the earlier G3 attempts:

- not a random-walk return density
- not a tunable Gaussian family
- not an ad hoc function fitted after seeing the answer

The question here is purely structural:

> if one uses only the total holonomy \(U\), what scalar data are actually available?

---

## 2. Exact Reduction to One Class Parameter

Every element \(U \in SU(2)\) is conjugate to

\[
U \sim \exp\!\big(i\phi\, \hat n \cdot \sigma\big),
\qquad \phi \in [0,\pi].
\]

So conjugacy classes in \(SU(2)\) are parameterized by a single angle \(\phi\).

The normalized fundamental trace is

\[
W \equiv \frac{1}{2}\operatorname{Tr}(U) = \cos \phi.
\]

Therefore:

> **Theorem 1.** Any continuous gauge-invariant scalar observable built only from the total holonomy
> \(U\) is a function of the single variable \(\phi\), equivalently a function of \(W\).

Write it as

\[
\mathcal O(U) = f(\phi) = F(W).
\]

This is exact. There is no additional scalar information in the conjugacy class.

### Corollary: higher-spin characters add no new scalar invariant

The spin-\(j\) character is

\[
\chi_j(U) = \frac{\sin\big((2j+1)\phi\big)}{\sin\phi},
\]

which is a Chebyshev polynomial in \(W = \cos\phi\).

So even moving to higher representations does not create a new independent gauge-invariant scalar.
It only replaces \(W\) by another fixed function of \(W\).

---

## 3. Immediate Consequence for the Cone Family

From `g3_wilson_loop_toy_model.md`, the first noncommuting \(C_3\)-symmetric cone family gives

\[
W\!\left(\frac{2\pi}{3},\beta\right)
=
\frac{11 - 27\cos^2\beta + 27\cos\beta\,\sin^2\beta}{16}.
\]

Hence any gauge-invariant scalar built only from the total holonomy has the form

\[
\mathcal O(\beta) = F\!\left(W\!\left(\frac{2\pi}{3},\beta\right)\right).
\]

So:

> **Theorem 2.** If \(\beta\) is not fixed independently, then no holonomy-only class function can
> remove the free geometric parameter. It can only repackage it.

This means the “canonical observable” problem splits cleanly into two subproblems:

1. fix \(\beta\) from the framework, or
2. use more data than the conjugacy class of the total holonomy

Without one of those, the coefficient remains underdetermined.

---

## 4. Why the Imperfect-Holonomy Near-Miss Was Not Selective

The exploratory note `g3_closure_via_imperfect_holonomy.md` found that

\[
\alpha_{\mathrm{trial}} = \frac{1-|W|^2}{4\pi}
\]

at the heuristic angle \(\beta = \arccos(1/\sqrt{3})\) lands within about 4% of the target coupling.

At that angle,

\[
W = \frac{1+3\sqrt{3}}{8} \approx 0.774519,
\qquad
\phi = \arccos(W) \approx 0.684842.
\]

Then

\[
1-W \approx 0.225481,
\qquad
\phi^2 \approx 0.469008,
\qquad
2(1-W) \approx 0.450962.
\]

So

\[
\frac{\phi^2}{2(1-W)} \approx 1.04002.
\]

That is the key structural point: near this angle, several natural class functions are already close:

- \(1-W\)
- \(1-|W|^2\)
- \(\phi^2\)
- higher-character deviations \(1-\chi_j/\dim(j)\)

They differ by order-one factors, not by a canonical theorem.

So the previous near-miss was not evidence that one specific observable had been selected. It was
evidence that many quadratic class functions of the same conjugacy angle sit in the same numerical
neighborhood.

---

## 5. Small-Holonomy Normalization Still Has a Free Constant

Suppose one asks for a physically reasonable canonical observable \(\mathcal O(U)\) with:

1. gauge invariance
2. \(\mathcal O(I)=0\)
3. positivity near the identity
4. symmetry under \(U \leftrightarrow U^{-1}\)
5. analyticity near \(U=I\)

Then \(\mathcal O\) must be an even analytic function of \(\phi\), so

\[
\mathcal O(U) = c\,\phi^2 + O(\phi^4)
\]

for some constant \(c>0\).

Since

\[
W = \cos\phi = 1 - \frac{\phi^2}{2} + O(\phi^4),
\]

this is equivalently

\[
\mathcal O(U) = 2c(1-W) + O\big((1-W)^2\big).
\]

So even after imposing the standard regularity conditions, the leading observable still carries a
free multiplicative constant \(c\).

> **Theorem 3.** A holonomy-only class function cannot produce the exact G3 coefficient from
> regularity and gauge invariance alone. The normalization remains free.

This is the canonical-observable version of the prefactor problem already seen in the product-walk
and Gaussian notes.

---

## 6. What Would Actually Escape This No-Go

There are only three honest exits.

### 6.1 Framework-fixed geometry

If the PF axioms uniquely determine \(\beta\), then the class angle \(\phi\) becomes fixed.
That still would not by itself fix the normalization constant, but it would eliminate one major
ambiguity.

### 6.2 More than the conjugacy class

Use data not captured by \(U\) alone, for example:

- the ordered triple \((K_0,K_1,K_2)\) itself
- a path-dependent connection functional
- a Chern-Simons / bundle-topological quantity
- a coupled spatial-holonomy observable in the product-walk model

These are not reducible to a class function of the total holonomy.

### 6.3 Independent coupling normalization

Derive the \(2\pi\) normalization and amplitude scale from a separate first-principles argument.
Then the holonomy observable would only need to supply the dimensionless geometric part.

---

## 7. Honest Outcome

This note does **not** prove that the holonomy route is wrong.

It proves something narrower and cleaner:

> a canonical gauge-invariant scalar built only from the total 3-step \(SU(2)\) holonomy cannot, by
> itself, close G3 under the current framework.

Why not?

- it contains only one class parameter \(\phi\) (equivalently \(W\))
- any candidate observable is just a function of that one parameter
- if \(\beta\) is free, the observable remains \(\beta\)-dependent
- even if \(\beta\) is fixed, the normalization constant is still not selected

So the “one narrow future return” to G3 lands on a precise boundary:

**holonomy-only class functions are exhausted as a closure mechanism.**

The next viable G3 move, if it ever resumes, must use either:

- extra geometric/topological data beyond the conjugacy class, or
- an independently derived connection-geometry principle plus an independent normalization argument

---

## 8. Final Status

| Question | Result |
|----------|--------|
| Does a holonomy-only class function give a unique scalar invariant? | **No** — it reduces to \(F(W)\) |
| Does changing representation help? | **No** — higher characters are functions of \(W\) |
| Does this close G3? | **No** |
| What did it accomplish? | It sharply rules out one more class of “canonical observable” hopes |

**Net effect on G3**: no confidence upgrade, but a cleaner frontier.

---

*Written by Codex, 2026-03-21*  
*Purpose: make the holonomy-observable question exact enough to stop coefficient hunting*
