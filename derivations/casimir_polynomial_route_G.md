# Casimir Polynomial Route G
*Representation / symmetry-breaking route*

**Date**: 2026-03-21
**Owner**: Codex
**Question**: Can PF symmetry breaking from `SO(3) × U(1)` to the residual electromagnetic `U(1)` force the Casimir polynomial
`x² + C₂x - C₂ = 0`?
**Primary inputs**: `topological_pressure_derivation.md`, `weinberg_angle_pf.md`, `g3_scheme_selection_argument.md`, `casimir_polynomial_brief.md`
**Outcome**: **C — gap reduction, with a restricted no-go**

---

## 1. Target

Test whether the symmetry-breaking structure already present in PF can generate the Casimir polynomial directly, before any separate spin-pair selection argument is invoked.

The hoped-for logic would be:

\[
\text{PF gauge structure} \;\Rightarrow\; \text{neutral-sector mixing operator} \;\Rightarrow\; x^2 + C_2x - C_2 = 0 .
\]

If this fails, identify exactly what part of the symmetry-breaking story is real progress and what part remains missing.

---

## 2. What PF Already Supplies

From `topological_pressure_derivation.md` and `weinberg_angle_pf.md`, PF already gives:

- an `SO(3)` rotational sector
- a `U(1)` phase sector
- spontaneous symmetry breaking with 3 Goldstone modes absorbed
- one surviving massless `U(1)` direction after breaking

So PF genuinely has a **two-sector neutral mixing problem** in the basis

\[
(B,\;W^3)
\]

where `B` is the `U(1)` phase gauge field and `W^3` is the neutral `SO(3)` gauge field.

This is important because a two-sector operator naturally leads to a quadratic characteristic equation.

---

## 3. The Most General Neutral-Sector Matrix PF Allows At This Stage

Before fixing any detailed normalization, the neutral-sector mass/stiffness operator has the generic symmetric form

\[
\mathcal M^2_{\text{neutral}} = m_*^2
\begin{pmatrix}
a & -b \\
-b & d
\end{pmatrix},
\]

with dimensionless coefficients \(a,d,b\) encoding:

- the relative `U(1)` stiffness
- the relative `SO(3)` stiffness
- the off-diagonal mixing induced by the broken phase

This is the most general two-sector quadratic form compatible with:

- a real neutral basis
- no explicit CP breaking in the mass matrix
- a single symmetry-breaking scale \(m_*\)

Its characteristic polynomial in the dimensionless eigenvalue \(x = \lambda/m_*^2\) is

\[
x^2 - (a+d)x + (ad-b^2) = 0.
\]

So **quadraticity itself** is not mysterious. Any two-sector neutral mixing problem gives a quadratic.

That is the first real result of Route G.

---

## 4. The Restricted No-Go

PF symmetry breaking requires one residual massless electromagnetic direction.

That means the neutral-sector operator must have one zero eigenvalue:

\[
\det \mathcal M^2_{\text{neutral}} = 0.
\]

For the generic matrix above:

\[
ad - b^2 = 0.
\]

So the characteristic polynomial collapses to

\[
x^2 - (a+d)x = x\bigl(x-(a+d)\bigr)=0.
\]

This has:

- one massless mode
- one massive neutral mode

and nothing else.

Now compare with the Casimir polynomial:

\[
x^2 + C_2x - C_2 = 0.
\]

For nonzero \(C_2\), its constant term is

\[
-C_2 \neq 0.
\]

Therefore:

\[
\boxed{
\text{the bare neutral symmetry-breaking mass matrix cannot be the Casimir polynomial}
}
\]

because gauge invariance forces the constant term to vanish, while the Casimir polynomial requires a nonzero constant term.

This is a clean restricted no-go.

---

## 5. What Route G Actually Establishes

Route G gives two precise statements.

### Statement 1 — Why a quadratic is natural

The PF symmetry-breaking story naturally produces a **two-sector** neutral problem, and two-sector problems generically produce quadratic characteristic equations.

So the presence of a quadratic in the Casimir story is not arbitrary. It fits the existence of two neutral sectors.

### Statement 2 — Why the bare gauge-boson mass matrix is not enough

The exact Casimir polynomial cannot be the characteristic equation of the final neutral gauge-boson mass matrix, because the residual massless photon forces zero determinant.

So the Casimir polynomial must belong to a **different operator** than the final neutral mass matrix.

That is the sharpened gap.

---

## 6. Where `C₂` Could Enter, If This Route Is Ever Completed

The route does not die completely. It redirects.

If Route G is to succeed later, `C₂ = j(j+1)` must enter **before** the final neutral mass-matrix stage, through something like:

- a representation-dependent stiffness metric
- an internal angular operator for coherent medium modes
- a pre-diagonalization self-consistency map on structured modes
- a two-sector reduced operator acting on representation-labeled states rather than directly on the final gauge fields

In other words:

\[
\text{symmetry breaking gives the two-sector skeleton,}
\]
\[
\text{but not yet the Casimir-labeled coefficients.}
\]

---

## 7. The Smallest Lemma Route G Leaves Behind

Route G reduces the original question to a smaller one:

> What is the **pre-mass-matrix** two-sector operator in PF whose coefficients are representation-dependent and can therefore carry \(C_2\)?

That is smaller than the original polynomial problem because it isolates exactly what symmetry breaking does and does not provide.

The final neutral gauge-boson matrix is too late in the chain. By that stage the zero mode is already enforced.

So if the Casimir polynomial is real PF structure, it must arise at an earlier reduction stage.

---

## 8. Honest Verdict

Route G does not derive the Casimir polynomial from PF symmetry breaking alone.

But it does produce a useful structural result:

- PF symmetry breaking explains why a quadratic spectral problem is plausible
- PF symmetry breaking rules out identifying the Casimir polynomial with the final neutral gauge-boson mass matrix
- therefore the Casimir polynomial must come from an earlier or different two-sector operator carrying explicit representation data

So this route ends as:

\[
\boxed{
\text{Outcome C: gap reduction via a restricted no-go}
}
\]

The sharpened remaining question is:

\[
\boxed{
\text{where does the representation-labeled pre-mass-matrix two-sector operator come from?}
}
\]
