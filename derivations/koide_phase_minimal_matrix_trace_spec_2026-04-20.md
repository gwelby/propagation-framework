# Koide Phase: Minimal Matrix Trace Spec

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Sharpen Lane B by writing the minimal abstract matrix / trace class that produces
`cos(9 delta)` exactly, and state why that still does not close the PF selector problem.

---

## 1. Why this note exists

The scalar audit and the existing-observable audit jointly showed:

- the scalar reduced variable is `f(delta) = -1/2 + cos(3 delta)/sqrt(2)`
- no existing concrete repo observable lands on the exact tuned cubic selector

That leaves the non-scalar lane:

> could a matrix / trace observable produce the right cancellation pattern before reduction to the
> scalar `f(delta)`?

This note writes the minimal abstract class.

---

## 2. The minimal phase matrix

Define the diagonal phase matrix

`U(delta) = diag(exp(i delta), exp(i(delta + 2*pi/3)), exp(i(delta + 4*pi/3)))`.

Equivalently,

`U(delta) = exp(i delta) * diag(1, omega, omega^2)`

with `omega = exp(2*pi*i/3)`.

This is the cleanest matrix object carrying the `Z_3` orbit as eigenphases.

---

## 3. First trace facts

Because `1 + omega + omega^2 = 0`, one gets immediately:

`Tr U = 0`

`Tr U^2 = 0`.

But

`U^3 = exp(i 3 delta) * I_3`

so

`Tr U^3 = 3 exp(i 3 delta)`.

### Theorem 1

In the minimal `3 x 3` phase matrix class above, the first nonzero trace invariant is exactly the
cubic trace:

`Tr U^3 = 3 exp(i 3 delta)`.

This is exact.

---

## 4. Exact `cos(9 delta)` from the trace class

Take the cubic trace and cube it:

`(Tr U^3)^3 = 27 exp(i 9 delta)`.

Therefore

`Re[(Tr U^3)^3] / 27 = cos(9 delta)`.

### Theorem 2

The minimal matrix trace class yields an exact `cos(9 delta)` selector through

`O_9(U) = Re[(Tr U^3)^3]`.

So, abstractly, a non-scalar matrix observable class that isolates the `n = 3` harmonic does
exist.

---

## 5. Why this does not yet close the repo problem

This construction is mathematically clean, but it still does **not** derive the Koide phase inside
the current PF repo.

The missing steps are:

### 5.1 No PF-native theorem object

The repo does not yet derive a canonical phase matrix `U(delta)` from Axioms 1-3 for the
charged-lepton Koide sector.

At present, `U(delta)` is an abstract representation-theoretic container, not a PF theorem object.

### 5.2 No selector principle on the trace algebra

Even if `U` were admitted, nothing in the current PF chain proves that the vacuum should extremize

`Re[(Tr U^3)^3]`

rather than:

- `Re[Tr U^3] ~ cos(3 delta)`
- `|Tr U^3|^2 = 9`
- a generic function of `Tr U^3`
- a mixed function involving other observables

So the existence of an exact matrix trace carrying `cos(9 delta)` is not yet a selector theorem.

### 5.3 No charged-lepton bridge

The phase matrix `U(delta)` carries the right harmonic structure, but the current repo still lacks
the bridge

`charged-lepton square-root mass triple -> canonical phase matrix U`.

Without that bridge, this remains a sharp abstract class, not a completed derivation.

---

## 6. Relation to the scalar cubic audit

This note does not contradict the scalar cubic result.

It complements it.

### Scalar lane

If everything is reduced first to the single scalar

`f(delta) = -1/2 + cos(3 delta)/sqrt(2)`,

then the first exact pure `cos(9 delta)` selector is the unique tuned cubic in `f`.

### Matrix lane

If the phase is carried instead by the matrix `U(delta)`, then the first clean trace invariant is
already cubic at the matrix level:

`Tr U^3 = 3 exp(i 3 delta)`.

Cubing that trace gives `cos(9 delta)` immediately.

So the two lanes say:

- scalar reduction first -> tuned Chebyshev cubic required
- matrix trace first -> exact `3 delta` carrier exists, but still needs a selector principle

---

## 7. What this buys us operationally

Lane B is now no longer handwave-shaped.

It has a concrete target:

1. derive a PF-native matrix object equivalent to `U(delta)`,
2. derive why the physical selector acts on `(Tr U^3)^3` or an equivalent class function,
3. connect that matrix object back to the charged-lepton Koide mass triple.

If none of those can be done, Lane B should be recorded as an abstract mathematical possibility,
not a PF derivation.

---

## 8. Final verdict

A minimal abstract matrix / trace class for exact `cos(9 delta)` does exist:

`U(delta) = diag(exp(i delta), exp(i(delta + 2*pi/3)), exp(i(delta + 4*pi/3)))`

with

`Re[(Tr U^3)^3] / 27 = cos(9 delta)`.

But this does **not** rescue the current repo state.

It only sharpens the non-scalar lane:

> PF still needs to derive the phase matrix, the trace-level selector principle, and the
> charged-lepton bridge.

Until then, this is a clean abstract target, not closure.
