# GR and Fermat: Exact Equivalence, Precise Limits

**Date**: 2026-03-20  
**Author**: Codex  
**Task**: Formalize the "gravity = refraction" claim  
**Status**: VERIFIED WITH DOMAIN RESTRICTIONS

---

## 1. Executive Verdict

The statement "gravity is refraction" is:

- **exact** for **null geodesics** in **static spacetimes** when written in terms of the
  optical metric
- **exact** for **null geodesics** in **stationary spacetimes** when extended from a scalar
  refractive index to a **Randers/Finsler optical geometry**
- **approximate** if one insists on a single scalar \(n(x)\) for all gravitational situations
- **not exact as stated** for the full content of GR, because a general metric has tensor structure
  beyond a scalar refractive index

So the strong version of the PF claim is defensible only in the form:

> gravitational propagation is optical geometry; scalar refraction is the static/isotropic limit,
> and Randers/Finsler optics is the minimum extension for the stationary case.

---

## 2. The GR Side

The spacetime geodesic equation is

\[
\frac{d^2 x^\mu}{d\lambda^2}
+
\Gamma^\mu_{\alpha\beta}
\frac{dx^\alpha}{d\lambda}
\frac{dx^\beta}{d\lambda}
=0.
\]

In the weak-field limit, write

\[
g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu},
\qquad |h_{\mu\nu}|\ll 1.
\]

For a static Newtonian potential \(\Phi(\mathbf x)\),

\[
ds^2
\simeq
-(1+2\Phi/c^2)c^2dt^2
+
(1-2\Phi/c^2)\,\delta_{ij}\,dx^i dx^j.
\]

For slow timelike motion, the spatial geodesic equation reduces to

\[
\frac{d^2 x^i}{dt^2} \simeq -\partial_i \Phi,
\]

which is the Newtonian limit.

For light, one imposes \(ds^2=0\), and the spatial path is governed not by the Newtonian limit
but by the optical metric discussed below.

---

## 3. Fermat's Principle

In an ordinary isotropic medium with refractive index \(n(\mathbf x)\), travel time is

\[
T[\gamma] = \frac{1}{c}\int_\gamma n(\mathbf x)\, dl,
\]

and Fermat's principle states

\[
\delta T[\gamma]=0.
\]

The Euler-Lagrange equation for this functional is the ray equation

\[
\frac{d}{dl}\big(n\,\mathbf t\big)=\nabla n,
\]

where \(\mathbf t\) is the unit tangent to the ray.

Equivalently,

\[
\frac{d\mathbf t}{dl}
=
\nabla_\perp \ln n,
\]

so rays bend where \(n\) has a transverse gradient.

---

## 4. Exact Mapping in Static Spacetimes

Consider a static spacetime written as

\[
ds^2 = -V(\mathbf x)^2 c^2 dt^2 + h_{ij}(\mathbf x)\,dx^i dx^j.
\]

For a null curve \(ds^2=0\),

\[
dt = \frac{1}{c}\sqrt{\frac{h_{ij}\,dx^i dx^j}{V^2}}.
\]

Hence the arrival-time functional is

\[
T[\gamma]
=
\frac{1}{c}\int_\gamma \sqrt{\hat h_{ij}\,dx^i dx^j},
\qquad
\hat h_{ij} := V^{-2} h_{ij}.
\]

So projected light rays are geodesics of the **optical metric**

\[
\hat h_{ij}=V^{-2}h_{ij}.
\]

This is an exact equivalence:

- 4D null geodesics in the static spacetime
- 3D geodesics of the optical metric
- stationary points of arrival time

are the same paths.

If, in addition, \(\hat h_{ij}\) is conformally flat,

\[
\hat h_{ij} = n(\mathbf x)^2 \delta_{ij},
\]

then one recovers the ordinary scalar-index Fermat form

\[
T[\gamma]=\frac{1}{c}\int n(\mathbf x)\,dl.
\]

So the scalar refractive-index picture is exact only after this extra simplification.

---

## 5. Weak-Field Scalar Index

For the weak-field static metric

\[
ds^2
\simeq
-(1+2\Phi/c^2)c^2dt^2
+
(1-2\Phi/c^2)\delta_{ij}dx^i dx^j,
\]

the effective optical index is

\[
n(\mathbf x)
=
\sqrt{\frac{1-2\Phi/c^2}{1+2\Phi/c^2}}
\simeq
1-\frac{2\Phi}{c^2}.
\]

For \(\Phi=-GM/r\),

\[
n(r) \simeq 1+\frac{2GM}{rc^2}.
\]

Then Fermat's ray equation gives the same weak-field bending as null geodesics.

This is the clean mathematical core of the slogan
"gravity is refraction."

---

## 6. Where Scalar \(n(x)\) Breaks

A general GR metric has ten independent components. A scalar refractive index carries only one.

Therefore a scalar \(n(\mathbf x)\) cannot encode generic:

- anisotropy
- frame dragging
- gravitomagnetic effects
- non-static structure

The scalar-index language is exact only in special cases:

1. static spacetime
2. null propagation
3. coordinates where the optical metric is conformally Euclidean

Outside that regime, the claim must be upgraded from scalar optics to geometric optics on a
nontrivial spatial geometry.

---

## 7. Minimum Exact Extension: Randers / Finsler Geometry

For a stationary spacetime one may write

\[
ds^2 =
-V^2 (dt-\theta_i dx^i)^2
+
\gamma_{ij}dx^i dx^j.
\]

Then the arrival-time functional for null curves becomes

\[
T[\gamma]
=
\frac{1}{c}
\int
\left(
\sqrt{a_{ij}\dot x^i\dot x^j}
+
b_i \dot x^i
\right)d\lambda,
\]

which is a **Randers metric**

\[
F(x,\dot x)=\sqrt{a_{ij}\dot x^i\dot x^j}+b_i\dot x^i.
\]

Here:

\[
a_{ij}=V^{-2}\gamma_{ij},
\qquad
b_i=\theta_i
\]

up to the standard stationary-spacetime convention.

This is the exact stationary generalization of Fermat's principle:

- the Riemannian part \(\sqrt{a_{ij}\dot x^i\dot x^j}\) gives the refractive slowing
- the one-form \(b_i dx^i\) gives a magnetic/Coriolis-like drift term

This term is exactly what scalar optics misses in rotating geometries such as Kerr.

So the local PF statement in `CLAIMS.md` that the bridge is a Randers metric is the correct one.

---

## 8. Beyond Stationary Spacetimes

In a general non-stationary spacetime there is still a general-relativistic Fermat principle:
actual light rays make the arrival time stationary among nearby null curves connecting an observer
event to a source worldline.

That statement remains exact.

However, there is generally no global reduction to:

- a time-independent scalar refractive index, or
- even a time-independent spatial Randers metric.

So the full statement "GR = scalar refraction" is false, while
"GR light propagation = generalized Fermat optics" is true.

---

## 9. What About Massive Particles?

Massive particles do not obey the null optical metric directly.

In static backgrounds one can still rewrite their spatial motion using a Jacobi/Maupertuis metric,
which is the mechanical analog of Fermat's principle:

\[
\delta \int p_i\,dx^i = 0.
\]

So there is a broader optical-mechanical analogy, but it is not literally the same as the null
Fermat principle of GR.

This matters for the PF slogan:

- **lightlike propagation**: exact optical/refraction language
- **massive particle motion**: analogous, but via Jacobi/Maupertuis geometry

---

## 10. Final Status of the Claim

### Exact

- Null geodesics in static GR are geodesics of the optical metric.
- Null geodesics in stationary GR are geodesics of a Randers/Finsler optical metric.
- Weak-field static gravity is exactly representable as propagation through an effective
  refractive index \(n(\mathbf x)\) for light.

### Approximate

- "gravity is a scalar refractive index gradient" is a weak-field/static/isotropic simplification.

### Not exact

- A single scalar \(n(\mathbf x)\) does not capture full GR.
- Full GR contains tensor and shift data that require at least optical metric + one-form,
  and in the stationary case this is naturally Randers/Finsler geometry.

---

## 11. Recommended CLAIMS.md Interpretation

The current claim can stay strong if phrased carefully:

> Forces as Refraction: **DERIVED in the optical-geometry sense**, exact for null propagation in
> static/stationary spacetimes, with scalar \(n(x)\) as the weak-field limit and Randers/Finsler
> geometry as the minimum exact stationary extension.

That wording is earned.

If the intended claim is instead:

> every gravitational effect is exactly a scalar refractive index field,

then 0.95 is too high.

---

## 12. Conclusion

The formal equivalence is real, but it is more precise than the slogan.

The mathematically correct chain is:

\[
\text{null GR geodesics}
\Longleftrightarrow
\text{stationary arrival-time extremals}
\Longleftrightarrow
\text{optical metric / Randers geodesics}.
\]

So "forces are refraction" is best read as:

> gravity is optical geometry, with ordinary scalar refraction as its weak-field static limit.

That is rigorous.

---

## References

1. Perlick, V. *Gravitational Lensing from a Spacetime Perspective* (Living Reviews, 2004): https://eprints.lancs.ac.uk/id/eprint/34484/1/livrev.pdf
2. Gordon, W. "Zur Lichtfortpflanzung nach der Relativitätstheorie" (1923).
