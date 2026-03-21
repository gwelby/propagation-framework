# G3: Phase-Dependent Triangular Gaussian Family
*A natural \(K_0, K_1, K_2\) model, computed exactly*

**Date**: 2026-03-21  
**Author**: Codex  
**Task**: Test the simplest nontrivial phase-dependent triangular kernel family after the restricted no-go result  
**Status**: EXACTLY COMPUTED — natural phase-dependent Gaussian kernels still do not close G3  
**Builds on**: `g3_product_walk_no_go.md`, `product_walk_bridge_model.md`, `phase_closure_exact_model.md`  
**Current claim status**: Keeps G3 at **PARTIAL / ARGUED (0.60)** while narrowing the surviving model space further  

---

## 1. Why This File Exists

`g3_product_walk_no_go.md` ruled out the naive phase-independent closures:

- bare smooth return density does not derive the exact coefficient
- nearest-neighbor cubic return is exactly zero at \(N=3\)

The next obvious candidate is therefore:

> make the spatial kernel explicitly depend on the internal \(120^\circ\) phase state.

This file computes the cleanest such family exactly.

---

## 2. The Natural Triangular Family

Fix a rotation axis \(\hat n\), taken as the \(z\)-axis for convenience, and let

\[
R = R_{\hat n}(2\pi/3)
\]

be the \(120^\circ\) spatial rotation about that axis.

Choose one spatial step vector \(v_0\) in the transverse plane, and define

\[
v_1 = Rv_0, \qquad v_2 = R^2 v_0.
\]

Then

\[
v_0 + v_1 + v_2 = 0,
\]

so the three phase-locked translations form an equilateral triangle.

Now let the spatial kernels be Gaussian convolution operators with phase-locked anisotropy:

\[
K_j = T_{v_j} \circ G_{\Sigma_j},
\]

where:

- \(T_{v_j}\) is translation by \(v_j\)
- \(G_{\Sigma_j}\) is Gaussian convolution with covariance \(\Sigma_j\)
- \(\Sigma_j = R^j \Sigma_0 R^{-j}\)

This is the cleanest explicit realization of

\[
K_0 \neq K_1 \neq K_2
\]

driven by the internal \(120^\circ\) phase cycle.

---

## 3. Exact Composition

Because each \(K_j\) is a translation-invariant convolution operator, the kernels commute under
composition. Their ordered product is another Gaussian convolution with summed mean and covariance:

\[
K_2 K_1 K_0 = T_{v_2+v_1+v_0} \circ G_{\Sigma_2 + \Sigma_1 + \Sigma_0}.
\]

Using the triangular identity \(v_0+v_1+v_2=0\), this becomes

\[
K_2 K_1 K_0 = G_{\Sigma_{\mathrm{eff}}},
\]

with

\[
\Sigma_{\mathrm{eff}} = \Sigma_0 + R\Sigma_0 R^{-1} + R^2 \Sigma_0 R^{-2}.
\]

### Exact consequence

The phase-dependent triangular family is still too Abelian.

The ordered product remembers only the **group-averaged covariance**. It does **not** retain a
noncommutative memory of the sequence \(0 \to 1 \to 2\).

So this family escapes the phase-independent no-go only superficially.

---

## 4. Exact Covariance Average

Write the initial covariance matrix in coordinates adapted to the rotation axis:

\[
\Sigma_0 =
\begin{pmatrix}
a & b & c \\
b & d & e \\
c & e & f
\end{pmatrix}.
\]

Then a direct computation gives

\[
\Sigma_{\mathrm{eff}}
=
\Sigma_0 + R\Sigma_0R^{-1} + R^2\Sigma_0R^{-2}
=
\begin{pmatrix}
\frac{3}{2}(a+d) & 0 & 0 \\
0 & \frac{3}{2}(a+d) & 0 \\
0 & 0 & 3f
\end{pmatrix}.
\]

This exact formula is the key result.

It shows:

- the transverse anisotropy averages to an isotropic plane
- the cross terms \(c,e\) cancel
- only two continuous invariants survive:
  - the transverse trace \(a+d\)
  - the axial variance \(f\)

Equivalently, with \(P_\parallel = \hat n \hat n^T\) and \(P_\perp = I - P_\parallel\),

\[
\Sigma_{\mathrm{eff}}
=
\frac{3}{2}\,\mathrm{tr}_\perp(\Sigma_0)\,P_\perp
+
3(\hat n^T \Sigma_0 \hat n)\,P_\parallel.
\]

So the three \(120^\circ\) phase labels do not select a unique covariance. They project the initial
covariance onto the \(C_3\)-invariant sector.

---

## 5. The Closure Observable at the Origin

If one still uses literal origin return density as the closure observable, the 3-step kernel is the
Gaussian with covariance \(\Sigma_{\mathrm{eff}}\), hence

\[
\mathcal C_3(0) = \frac{1}{(2\pi)^{3/2}\sqrt{\det \Sigma_{\mathrm{eff}}}}.
\]

Using the exact determinant,

\[
\det \Sigma_{\mathrm{eff}}
=
\left(\frac{3}{2}(a+d)\right)^2 (3f)
=
\frac{27}{4}(a+d)^2 f,
\]

so

\[
\mathcal C_3(0)
=
\frac{1}{(2\pi)^{3/2}}
\cdot
\frac{2}{3\sqrt{3}\,(a+d)\sqrt{f}}.
\]

### Consequence

This family still does **not** derive the God Equation coefficient.

The closure observable depends on two continuous parameters:

- \(a+d\) (transverse diffusion scale)
- \(f\) (axial diffusion scale)

The \(120^\circ\) phase structure alone does not fix them.

So even after making the kernels explicitly phase-dependent, the exact coefficient remains
underdetermined.

---

## 6. What This Means for G3

This is a stronger restriction than the previous note.

`g3_product_walk_no_go.md` said:

- phase-independent product walks are insufficient

This file adds:

- the most natural phase-dependent **Gaussian convolution** family is also insufficient

The reason is structural:

1. the kernels commute as convolution operators
2. the phase ordering is washed out into a \(C_3\)-averaged covariance
3. the return density still carries continuous diffusion parameters

So the live space narrows again.

---

## 7. The New Surviving Frontier

If G3 is to close inside a triangular phase-dependent model, it now has to use at least one of:

1. **Non-commuting kernels**  
   For example: position-dependent frame transport, a gauge connection, or operators that are not
   pure convolutions.

2. **A non-return closure observable**  
   Something sensitive to ordered holonomy, frame closure, Wilson-loop-like phase, or another
   nonlocal quantity.

3. **An exact coupling map that fixes normalization**  
   Even with a good observable, the map to \(\alpha(l_P)\) must still produce the \(2\pi\) factor.

This means the next G3 theorem attempt cannot be "Gaussian but smarter." It has to be genuinely
non-Abelian in either the kernels or the observable.

---

## 8. Updated Honest Status

**What this file establishes exactly**

- the triangular phase-locked Gaussian family can be written down explicitly
- its ordered product is computable in closed form
- it collapses to a single Gaussian with averaged covariance
- the coefficient remains continuous-parameter dependent

**What it does not establish**

- a successful non-commuting kernel family
- a closure observable sensitive to phase ordering
- the exact map to \(\alpha(l_P)\)

So:

- **G3** stays **PARTIAL / ARGUED at 0.60**
- the next surviving model class is narrower than before

---

## 9. Precise Next Move

The most honest next attack is now:

> construct a non-commuting phase-dependent kernel family, or a holonomy-style closure observable,
> so that the ordered sequence \(K_2K_1K_0\) matters intrinsically rather than collapsing to a
> commutative Gaussian average.

That is the next real theorem frontier.

---

*Written by Codex, 2026-03-21*  
*Purpose: test the first natural phase-dependent triangular kernel family exactly, and rule it out as a full G3 closure*  
