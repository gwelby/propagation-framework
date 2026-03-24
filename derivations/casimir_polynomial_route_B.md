# Casimir Polynomial Route B
*Propagation Lagrangian / variational route*

**Date**: 2026-03-21
**Owner**: Codex
**Question**: Can the existing Propagation Lagrangian produce the Casimir polynomial
`x² + C₂x - C₂ = 0`
as a stationarity condition or pole condition?
**Primary inputs**: `propagation_lagrangian.md`, `g3_casimir_weinberg_angle.md`, `casimir_polynomial_brief.md`
**Outcome**: **B — bounded no-go for the current Lagrangian**

---

## 1. Target

Test whether the existing PF variational structure

\[
\mathcal L_{\text{prop}} = \frac12 (\partial \chi)^2 - V(\chi) + \lambda \chi T
\]

can generate, from Axioms 1–3 and no extra hidden assumptions, the polynomial

\[
x^2 + C_2 x - C_2 = 0
\]

where `C₂ = j(j+1)`.

The question is not whether one can invent an effective reduced model that reproduces the polynomial. The question is whether the **current** PF Lagrangian already forces it.

---

## 2. What The Existing Lagrangian Actually Gives

From `propagation_lagrangian.md`, the Euler-Lagrange equation is

\[
\Box \chi + V'(\chi) = \lambda T .
\]

Linearizing around a background \(\chi = \bar\chi + \delta\chi\) with constant \(\bar\chi\):

\[
(\Box + m_{\text{eff}}^2)\,\delta\chi = \lambda\,\delta T,
\qquad
m_{\text{eff}}^2 := V''(\bar\chi).
\]

In momentum space:

\[
(-k^2 + m_{\text{eff}}^2)\,\tilde\chi(k) = \lambda\,\widetilde{\delta T}(k).
\]

So the tree-level propagator denominator is

\[
D(k^2) = -k^2 + m_{\text{eff}}^2
\]

up to convention signs.

This is affine in \(k^2\), not quadratic.

---

## 3. Why The Polynomial Does Not Appear At Tree Level

The Casimir polynomial requires three structural ingredients:

1. a quadratic relation in a spectral variable \(x\)
2. coefficients controlled by \(C_2\)
3. the specific antisymmetric pattern \(x^2 + C_2 x - C_2\)

The present Lagrangian provides none of these by itself.

### 3.1 No internal `SU(2)` label

The field \(\chi\) is a single real scalar. The derivation in `propagation_lagrangian.md` explicitly chose a scalar because it is the minimal isotropic medium variable.

A scalar field carries no built-in representation label \(j\), hence no built-in quadratic Casimir \(C_2 = j(j+1)\).

So the current Lagrangian has no native object from which \(C_2\) can arise.

### 3.2 No quadratic spectral equation

For a single local scalar with canonical kinetic term and local potential, the fluctuation operator is linear in \(k^2\):

\[
D(k^2) = Z\,k^2 + M^2
\]

after linearization, even if a background-dependent wavefunction factor \(Z\) is allowed.

That gives a first-degree pole condition in the spectral variable, not

\[
x^2 + C_2 x - C_2 = 0.
\]

### 3.3 The matter coupling does not fix it either

The interaction term \(\lambda \chi T\) introduces sourcing and, after integrating out matter loops, a self-energy:

\[
D(k^2) = Zk^2 + M^2 + \Pi(k^2).
\]

But Axioms 1–3 do not determine \(\Pi(k^2)\) uniquely, and the existing PF Lagrangian does not specify a loop structure that would force

\[
D \propto x^2 + C_2 x - C_2.
\]

Without an explicitly derived \(\Pi(k^2)\), using loop corrections here would be importing extra QFT structure rather than deriving from PF axioms.

---

## 4. Stronger No-Go Statement

### Claim

The current single-scalar Propagation Lagrangian cannot, by itself, derive the Casimir polynomial as a tree-level variational or pole condition.

### Reason

Any local quadratic fluctuation operator obtained from the current Lagrangian has the form

\[
\mathcal O = Z(\bar\chi)\,\Box + M^2(\bar\chi)
\]

acting on a single scalar mode.

After Fourier transform this becomes

\[
D(k^2) = Z(\bar\chi)\,k^2 + M^2(\bar\chi),
\]

which is affine in \(k^2\).

To get a quadratic polynomial in a dimensionless spectral variable \(x\), one needs at least one of:

- an additional coupled field or sector
- a matrix-valued fluctuation operator
- a nonlocal self-energy / memory kernel
- an explicit internal angular operator with eigenvalue \(C_2\)
- a reduced collective-coordinate constraint not contained in the current Lagrangian

None of these are present in the current derivation of `propagation_lagrangian.md`.

Therefore Route B, in its current strict form, is a no-go.

---

## 5. What This Does Not Prove

This note does **not** prove that no future PF variational route can derive the polynomial.

It proves only this narrower statement:

> the currently derived single-scalar PF Lagrangian is insufficient on its own.

That is still useful. It sharply narrows where the missing structure must enter.

---

## 6. The Smallest Remaining Variational Gap

The smallest plausible lemma now looks like this:

> PF must derive an internal angular sector for coherent matter modes, with operator eigenvalues \(C_2 = j(j+1)\), and show that the effective reduced mode equation is a **two-sector** or **matrix** consistency problem rather than a single scalar pole condition.

Why this is the right scale of gap:

- \(C_2\) cannot appear until an angular operator exists
- a quadratic polynomial in \(x\) naturally suggests a two-branch or two-sector reduction
- the specific sign pattern \(x^2 + C_2 x - C_2\) suggests a Schur-complement or self-consistency equation, not a bare Klein-Gordon pole

One concrete future target would be a reduced \(2 \times 2\) mode system whose determinant is

\[
\det
\begin{pmatrix}
x & -1 \\
C_2 & x + C_2
\end{pmatrix}

= x^2 + C_2 x - C_2.
\]

This matrix is **not** derived here. It is only an example of the kind of extra structure required.

---

## 7. Honest Verdict

Route B does not close the Casimir polynomial from the existing PF Lagrangian.

What it establishes is more precise:

- the current Lagrangian yields a scalar Klein-Gordon-type pole condition
- that structure is too weak to produce the Casimir polynomial
- therefore the missing ingredient is not “more algebra” on the same scalar field
- the missing ingredient is additional internal structure: angular, matrix, or collective-coordinate

So this route ends as:

\[
\boxed{\text{Outcome B: no-go for the current single-scalar variational route}}
\]

with one sharpened next lemma:

\[
\boxed{\text{derive the internal angular sector that could carry } C_2 \text{ into an effective mode equation}}
\]
