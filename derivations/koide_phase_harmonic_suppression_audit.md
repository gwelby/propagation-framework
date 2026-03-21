# Koide Phase: Harmonic Suppression Audit
*Why PF symmetry alone does not make \(\cos(9\delta)\) the leading harmonic*

**Date**: 2026-03-21  
**Author**: Codex  
**Status**: AUDIT COMPLETE — natural symmetric PF composites reduce to one variable \(f(\delta)\); lower harmonics are generically present  
**Builds on**: `koide_phase_rivero_bridge_audit.md`, `koide_phase_delta_0_gap.md`, Rivero's `cos9delta_derivation.py`

---

## 1. The Narrow Question

The previous bridge audit established:

- PF naturally gives a \(2\pi/3\)-periodic phase tower \(\cos(3n\delta)\)
- Rivero's \(\cos(9\delta)\) lies inside that allowed tower
- PF does not yet single out \(n=3\)

The next precise question is:

> can a **natural composite observable** of the three Koide phase factors suppress
> \(\cos(3\delta)\) and \(\cos(6\delta)\), leaving \(\cos(9\delta)\) as the first leading term?

This note answers that for the most natural class of PF observables: symmetric composites of the
three phase-shifted Koide factors.

---

## 2. The Three Koide Factors

Define

\[
g_k(\delta) = 1 + \sqrt{2}\cos\!\left(\delta + \frac{2\pi k}{3}\right),
\qquad k=0,1,2.
\]

These are exactly the three dimensionless factors in the Koide angular parametrization

\[
\sqrt{m_k}=\sqrt{M_0}\,g_k(\delta).
\]

Rivero's script introduces the product

\[
f(\delta)=g_0(\delta)\,g_1(\delta)\,g_2(\delta).
\]

The key point is that the lower symmetric data are actually constant.

### Theorem 1

The elementary symmetric polynomials of the three Koide factors are

\[
e_1 = g_0+g_1+g_2 = 3,
\]

\[
e_2 = g_0g_1+g_0g_2+g_1g_2 = \frac32,
\]

\[
e_3 = g_0g_1g_2 = -\frac12 + \frac{\cos(3\delta)}{\sqrt{2}}.
\]

### Proof

Let

\[
c_k=\cos\!\left(\delta + \frac{2\pi k}{3}\right).
\]

Standard \(120^\circ\) identities give

\[
\sum_k c_k = 0,
\qquad
\sum_{i<j} c_i c_j = -\frac34,
\qquad
\prod_k c_k = \frac{\cos(3\delta)}{4}.
\]

Then

\[
e_1 = \sum_k (1+\sqrt2\,c_k) = 3 + \sqrt2\sum_k c_k = 3,
\]

and

\[
e_2 = \sum_{i<j}(1+\sqrt2 c_i)(1+\sqrt2 c_j)
    = 3 + 2\sqrt2\sum_k c_k + 2\sum_{i<j}c_i c_j
    = 3 - \frac32 = \frac32.
\]

Finally,

\[
e_3
=
\prod_k (1+\sqrt2\,c_k)
=
1 + 2\sum_{i<j}c_i c_j + 2\sqrt2\prod_k c_k
=
1 - \frac32 + \frac{\cos(3\delta)}{\sqrt2}.
\]

So

\[
\boxed{
e_3=f(\delta)= -\frac12 + \frac{\cos(3\delta)}{\sqrt2}
}
\]

This is exactly the function appearing in Rivero's script.

---

## 3. Immediate Consequence: Only One Phase Variable Survives

By the fundamental theorem of symmetric polynomials:

> any symmetric polynomial observable built from \((g_0,g_1,g_2)\) can be written as a polynomial
> in \((e_1,e_2,e_3)\).

But here \(e_1\) and \(e_2\) are constants.

So:

\[
\mathcal O(g_0,g_1,g_2) = P(e_1,e_2,e_3) = Q(e_3) = Q(f(\delta)).
\]

This is the exact reduction.

### Theorem 2

Every natural symmetric polynomial three-body observable of the Koide factors reduces to a function
of the single variable

\[
f(\delta)= -\frac12 + \frac{\cos(3\delta)}{\sqrt2}.
\]

So the harmonic-suppression problem is not arbitrary. It is exactly the problem of whether some
natural \(Q(f)\) kills the lower \(\cos(3\delta)\) and \(\cos(6\delta)\) terms.

---

## 4. What Natural Powers Actually Do

Rivero's determinant route uses powers of \(f\), in particular \(f^6\).

The low harmonics of \(f^k\) for small \(k\) are:

| \(k\) | \(\cos(3\delta)\) | \(\cos(6\delta)\) | \(\cos(9\delta)\) |
|---|---:|---:|---:|
| 1 | \(+0.7071\) | \(0\) | \(0\) |
| 2 | \(-0.7071\) | \(+0.2500\) | \(0\) |
| 3 | \(+0.7955\) | \(-0.3750\) | \(+0.0884\) |
| 4 | \(-0.8839\) | \(+0.5000\) | \(-0.1768\) |
| 5 | \(+0.9944\) | \(-0.6250\) | \(+0.2762\) |
| 6 | \(-1.1270\) | \(+0.7617\) | \(-0.3867\) |

For the key case \(k=6\):

- \(|\cos(3\delta)| \approx 1.1270\)
- \(|\cos(6\delta)| \approx 0.7617\)
- \(|\cos(9\delta)| \approx 0.3867\)

So \(\cos(9\delta)\) is present, but it is not dominant. This matches Rivero's own script.

### Corollary

Natural monomials \(f^k\) do **not** automatically suppress the lower harmonics.

So the hoped-for “threefold composite observable \(\Rightarrow\) automatic \(9\delta\)” does not
happen by itself.

---

## 5. What Would Be Needed to Isolate \(\cos(9\delta)\)

Write

\[
x=\cos(3\delta),
\qquad
f = -\frac12 + \frac{x}{\sqrt2}.
\]

Then any symmetric polynomial observable becomes a polynomial \(R(x)\).

Pure \(\cos(9\delta)\) is the Chebyshev combination

\[
\cos(9\delta)=T_3(x)=4x^3-3x.
\]

So isolating the \(n=3\) harmonic requires a very specific tuned combination of cubic and linear
terms in \(x\), equivalently a very specific combination of cubic and lower powers of \(f\).

### Theorem 3

To make \(\cos(9\delta)\) the leading harmonic from the single-variable reduction
\(\mathcal O=Q(f)\), one must impose specific coefficient relations that cancel the lower
\(\cos(3\delta)\) and \(\cos(6\delta)\) pieces.

That cancellation is **not** implied by:

- \(Z_3\) symmetry alone
- the Koide amplitude geometry alone
- the existence of the symmetric product \(f=g_0g_1g_2\) alone

It requires additional dynamical structure.

---

## 6. Strongest Honest No-Go

The most precise version of the no-go is:

> PF symmetry plus natural symmetric three-body composition does not force \(\cos(9\delta)\) to
> lead. It collapses the phase dependence to the single variable \(f(\delta)\), but generic
> functions of \(f\) retain lower harmonics.

This is stronger than the earlier bridge audit.

The earlier note said:

- PF gives the \(\cos(3n\delta)\) tower
- Rivero adds the \(n=3\) dynamics

This note adds:

- even the most natural PF composite observable \(f=g_0g_1g_2\) does **not** fix that
- powers of \(f\) keep the lower harmonics alive
- pure \(9\delta\) needs tuned cancellation or extra dynamics

---

## 7. What This Means for PF vs Rivero

There are now three clean layers:

1. **PF symmetry layer**  
   \(Z_3\) cycle \(\Rightarrow\) allowed Fourier tower \(\cos(3n\delta)\)

2. **PF composite layer**  
   natural symmetric three-body observables \(\Rightarrow\) functions of
   \(f(\delta)=-1/2+\cos(3\delta)/\sqrt2\)

3. **Rivero dynamical layer**  
   special nonlinear / instanton dynamics needed to make \(n=3\) physically selected

So Rivero is not just adding “another observable.” He is adding the specific dynamics needed to
pick one member of the PF-allowed tower.

---

## 8. Final Verdict

| Question | Answer |
|----------|--------|
| Do symmetric three-body PF observables reduce to one phase function? | **Yes** — to \(Q(f(\delta))\) |
| Is \(f(\delta)\) exactly Rivero's determinant-like factor? | **Yes** |
| Do natural powers \(f^k\) suppress \(\cos(3\delta)\) and \(\cos(6\delta)\)? | **No** |
| Does PF currently derive the \(n=3\) selection? | **No** |
| What is required? | Tuned cancellation or additional dynamics |

**Net outcome**:

The harmonic-suppression pass points toward a no-go, not a derivation. PF naturally reproduces the
right phase variable and the right symmetry tower, but not the specific suppression pattern needed
for \(\cos(9\delta)\) dominance.

That makes Rivero's instanton dynamics genuinely additional structure, unless a future PF derivation
finds an internal cancellation principle that has not yet been identified.

---

*Written by Codex, 2026-03-21*  
*Purpose: decide whether natural PF composite observables can make \(\cos(9\delta)\) lead without extra dynamics*
