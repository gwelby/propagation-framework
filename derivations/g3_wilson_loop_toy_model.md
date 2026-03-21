# G3: SU(2) Wilson-Loop Toy Model
*A 3-step holonomy test for the internal phase bridge*

**Date**: 2026-03-21  
**Author**: Codex  
**Task**: Test whether a minimal 3-step SU(2) holonomy can supply the rigid coefficient missing from G3  
**Status**: EXACTLY COMPUTED — same-axis holonomy is trivial; the first honest noncommuting family still leaves free geometry  
**Builds on**: `phase_closure_exact_model.md`, `g3_product_walk_no_go.md`, `g3_triangular_gaussian_family.md`, `g3_coupling_bridge.md`  
**Current claim status**: Keeps G3 at **PARTIAL / ARGUED (0.60)**  

---

## 1. Why This File Exists

The product-walk and Gaussian-triangle notes narrowed G3 to a precise question:

> can a genuinely noncommuting 3-step SU(2) holonomy produce a rigid dimensionless coefficient,
> rather than a tunable diffusion prefactor?

This note tests the cleanest Wilson-loop version of that idea.

The observable is the normalized trace of the ordered product:

\[
W = \frac{1}{2}\,\operatorname{Tr}(K_2 K_1 K_0),
\]

with each \(K_j \in SU(2)\).

If this route is going to close G3, the coefficient has to come from group theory itself, not from a
free geometric parameter.

---

## 2. Minimal SU(2) Transport Model

Write each step as a standard SU(2) rotation:

\[
K_j = c\,I + i s\,\hat n_j \cdot \sigma,
\qquad
c = \cos\frac{\theta}{2}, \quad s = \sin\frac{\theta}{2}.
\]

Here \(\theta\) is the step angle and \(\hat n_j\) is the unit axis for the \(j\)-th transport.

The cleanest 3-step holonomy test should respect the \(C_3\) symmetry already present in the
framework, so the natural symmetric choice is:

\[
\hat n_j = \big(\sin\beta\cos\tfrac{2\pi j}{3},\; \sin\beta\sin\tfrac{2\pi j}{3},\; \cos\beta\big),
\qquad j=0,1,2.
\]

This is a common cone of half-angle \(\beta\) around the \(z\)-axis, with the three axes separated
by \(120^\circ\) in azimuth.

That is the simplest genuinely noncommuting \(C_3\)-symmetric family available here.

---

## 3. Same-Axis Check

First test the degenerate case where all three steps share the same axis:

\[
\hat n_0 = \hat n_1 = \hat n_2 = \hat n.
\]

Then the steps commute, and

\[
K_2 K_1 K_0 = \big(cI + i s\,\hat n\cdot\sigma\big)^3.
\]

Using the Pauli algebra, the normalized Wilson loop is

\[
W_{\mathrm{same}} = \cos\frac{3\theta}{2}.
\]

For the \(120^\circ\) step used throughout the framework,
\[
\theta = \frac{2\pi}{3}
\]
so
\[
W_{\mathrm{same}} = \cos\pi = -1.
\]

Thus
\[
|W_{\mathrm{same}}|^2 = 1.
\]

### Verdict on the same-axis model

This is rigid, but it is trivial.

It only sees the central SU(2) lift \(K_2K_1K_0 = -I\), i.e. the \(\mathbb Z_2\) sheet flip.
It does not produce a nontrivial geometric coefficient, and it does not encode any extra structure
beyond the already-known 3-step closure.

So the same-axis 120-degree model is insufficient for G3.

---

## 4. Exact Wilson Loop for the Cone Family

Now take the genuinely noncommuting \(C_3\)-symmetric cone family from Section 2.

The normalized trace of the ordered product can be computed directly from

\[
(\mathbf a \cdot \sigma)(\mathbf b \cdot \sigma)
=
(\mathbf a \cdot \mathbf b)\,I + i(\mathbf a \times \mathbf b)\cdot \sigma.
\]

The exact result is:

\[
W(\theta,\beta)
=
c^3
- c s^2 \sum_{i<j}\hat n_i \cdot \hat n_j
- s^3 (\hat n_2 \times \hat n_1)\cdot \hat n_0.
\]

For the cone axes defined above,

\[
\sum_{i<j}\hat n_i\cdot \hat n_j = \frac{3}{2}\big(3\cos^2\beta - 1\big),
\]

and

\[
(\hat n_2 \times \hat n_1)\cdot \hat n_0
=
-\frac{3\sqrt{3}}{2}\sin^2\beta\cos\beta.
\]

So the Wilson loop becomes

\[
W(\theta,\beta)
=
c^3
- \frac{3}{2} c s^2 \big(3\cos^2\beta - 1\big)
+ \frac{3\sqrt{3}}{2} s^3 \sin^2\beta\cos\beta.
\]

This is exact.

### Check at the framework step angle

For \(\theta = 2\pi/3\), so \(c = 1/2\) and \(s = \sqrt{3}/2\),

\[
W\!\left(\frac{2\pi}{3},\beta\right)
=
\frac{11 - 27\cos^2\beta + 27\cos\beta\,\sin^2\beta}{16}.
\]

That depends continuously on \(\beta\).

Two useful limits:

\[
W\!\left(\frac{2\pi}{3},0\right) = -1,
\qquad
W\!\left(\frac{2\pi}{3},\frac{\pi}{2}\right) = \frac{11}{16}.
\]

So the same \(120^\circ\) phase step gives different Wilson loops depending on the cone angle.

---

## 5. Interpretation

This is the key point.

The same-axis model is rigid only because it is central and effectively Abelian.
Once the holonomy is genuinely noncommuting, the ordered product does remember the sequence, but
it still does not collapse to a unique coefficient.

The surviving parameter is the cone angle \(\beta\).

That means the Wilson loop is not yet the missing G3 bridge by itself. It gives a family of
dimensionless values, not a single group-theoretic constant.

The ordered product is sensitive to ordering, but the geometry is still underdetermined.

---

## 6. What This Does and Does Not Prove

### Established exactly

- A same-axis 3-step SU(2) holonomy gives \(W = \cos(3\theta/2)\).
- At \(\theta = 2\pi/3\), the same-axis loop gives \(W=-1\) and \(|W|^2=1\).
- That case is rigid but trivial: it only captures the central \(\mathbb Z_2\) lift.
- The simplest noncommuting \(C_3\)-symmetric cone family has an exact Wilson loop
  \(W(\theta,\beta)\) that depends on the free cone angle \(\beta\).

### Not established

- a rigid coefficient fixed by group theory alone
- a canonical choice of \(\beta\) from the framework axioms
- a direct map from \(W\) to \(\alpha(l_P)=1/(2\pi N^{D/2})\)

So the Wilson-loop toy model does **not** close G3.

It does sharpen the target:

> if G3 is to close via holonomy, the theory must fix the connection geometry itself, not merely
> the ordered product of SU(2) transports.

---

## 7. The Surviving Gap

The new frontier is now precise:

1. Find a noncommuting transport family where the framework fixes the analogue of \(\beta\).
2. Or replace the trace with a genuinely topological/holonomy observable that eliminates the free
   cone parameter.
3. Then show how that observable maps to the Planck-boundary coupling with the required \(2\pi\)
   normalization.

Until then, the Wilson loop is a useful restriction, not a derivation.

---

## 8. Final Status

**Honest outcome**:

- same-axis SU(2) holonomy is rigid but trivial
- the simplest noncommuting \(C_3\)-symmetric holonomy is exact but still parameterized
- G3 is still **PARTIAL / ARGUED (0.60)**

The Wilson-loop route does not close the God Equation yet.

---

*Written by Codex, 2026-03-21*  
*Purpose: test whether a 3-step SU(2) holonomy can supply a rigid coefficient for G3*  
