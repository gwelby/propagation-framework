# Koide Phase Filter: Bare Rational in Radians vs Reduced Parameter

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: State the exact filter prompted by Alejandro Rivero's reply and prevent future
category errors in the Koide phase discussion.

---

## 1. The challenge

Rivero's objection is:

> if a mechanism produces an exact rational **in radian units**, that is surprising

That objection is technically correct for ordinary geometric-angle mechanisms.

---

## 2. What the filter says

### Case A — ordinary geometric angle

If `delta` is an ordinary phase angle on a circle, then finite-order quantization gives values of
the form

`delta = 2*pi*k/n`

or related rational multiples of `pi`.

Therefore:

- exact bare rationals like `2/9` are **not** natural outputs of ordinary angle quantization
- the question "where did the `pi` go?" is mandatory

This is the default hostile filter.

### Case B — reduced dimensionless parameter

If the object called `delta` is **not** fundamentally an angle, but a reduced parameter later
inserted into a trigonometric parametrization, then a bare rational is no longer automatically
pathological.

Examples of this general class include:

- conformal weights
- scaling dimensions
- topological labels that only generate a physical phase after multiplication by `2*pi`

But then the burden shifts:

- one must show that the Koide `delta` belongs to this class
- one must not silently rename a parameter and call the problem solved

---

## 3. What the repo currently supports

The repo currently supports:

1. `Q = 2/3` is derived for charged leptons.
2. `delta ≈ 2/9` is a strong empirical anchor.
3. T-022 and T-021 failed as selector bridges.
4. PF naturally allows a `2*pi/3`-periodic harmonic tower `cos(3n delta)`.
5. PF does **not** currently derive why `n=3` should dominate.

The repo does **not** currently support:

1. "delta is proven to be a conformal weight"
2. "the WZW route solves the bare-rational problem"
3. "Rivero's `cos(9 delta)` mechanism is fully closed"

---

## 4. Practical interpretation

When evaluating a candidate selector for the Koide phase, ask:

### Filter 1

Is the proposed object fundamentally an angle?

If yes, then any exact rational-in-radians claim must explain the missing `pi`.

### Filter 2

Is the proposed object fundamentally a reduced parameter that only later appears inside a cosine?

If yes, then the model must explicitly state that, and must show why the Koide parametrization is
using that reduced parameter rather than a geometric angle.

### Filter 3

Does the mechanism actually select `2/9`, or does it merely make `2/9` algebraically allowable?

Allowance is weaker than selection.

### Filter 4

Does the mechanism suppress lower harmonics?

For the Rivero/PF overlap, this is the real load-bearing question:

- `cos(9 delta)` being present is not enough
- `cos(3 delta)` and `cos(6 delta)` must fail to dominate

---

## 5. Working conclusion

The current strongest honest statement is:

> A bare exact `delta = 2/9` in radian units remains unnatural for an ordinary geometric-angle
> mechanism. A loophole exists only if the Koide `delta` is not fundamentally an angle but a
> reduced dimensionless parameter. That loophole class is plausible, but it is **not yet derived**
> in the repo.

### Rivero sharpening — 2026-04-20

Rivero's later formulation makes the filter stricter and clearer:

> "the rational is always tan theta, never theta"

Interpreted mathematically:

- the natural rational object is a **projective / slope-like invariant**
- the angle is secondary

This means the better hostile filter is:

1. do not ask first whether `theta` is rational
2. ask whether some **reduced ratio variable** attached to the geometry is rational
3. only then ask how that ratio is embedded into the trigonometric parametrization

Numerical caution:

- for the measured charged-lepton Koide phase, `tan(delta_exact) = 0.225961718896`
- this is **not** equal to `2/9 = 0.222222222222`

So Rivero's sharpening does not rescue the exact claim `tan(delta)=2/9`.
It instead redirects the search toward a different reduced invariant.

---

## 6. Immediate use

This note should govern:

- any reply to Rivero
- any manuscript sentence about `delta = 2/9`
- any future WZW / conformal-weight / topological-spin route

Terminology rule:

- `Q = 2/3` → derived
- `delta = 2/9` → empirical anchor
- selector mechanism → open
- conformal-weight reinterpretation → candidate loophole, not closure
