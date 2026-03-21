# Product-Walk Bridge Model — Exact Frontier for G3

**Date**: 2026-03-21  
**Author**: Codex  
**Task**: Formulate the cleanest exact candidate bridge between internal phase closure and spatial coherence volume  
**Status**: MODEL FORMULATED — bridge specified, not derived  
**Builds on**: `phase_closure_exact_model.md`, `exact_return_N3_D3.md`, `g3_coupling_bridge.md`, `phase_closure_meaning.md`  
**Current claim status**: Supports keeping the God Equation at **ARGUED (0.75)** while isolating one remaining bridge theorem  

---

## 1. Why This File Exists

The repo has already established:

- the exact internal phase walk (`phase_closure_exact_model.md`)
- the exact failure of the internal walk by itself to generate the needed \(N^{D/2}\) scaling
- the fact that Euclidean spatial diffusion has the right exponent but lives on the wrong state space

So the natural next move is a **product-walk model**:

\[
\text{internal phase dynamics} \times \text{spatial diffusion}.
\]

This file states that model as cleanly as possible, and it marks exactly which steps are known and
which remain open.

---

## 2. Internal Factor: Exact and Already Fixed

From `phase_closure_exact_model.md`, the internal walk is:

\[
\mathcal H_{\mathrm{int}} = \ell^2(\mathbb Z_6),
\]

with basis \(\{|k\rangle : k \in \mathbb Z_6\}\) and shift operator

\[
S_{\mathrm{int}} |k\rangle = |k+1 \bmod 6\rangle.
\]

Observable generations live on the quotient

\[
\mathbb Z_6 / \mathbb Z_2 \cong \mathbb Z_3,
\]

so three quotient steps close the observable orbit and six lifted steps close the full spinorial
orbit.

This part is not open.

---

## 3. Spatial Factor: Candidate Diffusion Sector

Take the spatial factor to be either:

\[
\mathcal H_{\mathrm{sp}} = \ell^2(\mathbb Z^D)
\]

for a lattice walk, or its continuum diffusion limit on \(L^2(\mathbb R^D)\).

The corresponding isotropic spatial kernel is denoted \(K_D\). In the continuum Gaussian limit,
the return density has the standard scaling

\[
P_{\mathrm{sp}}(0,N) \propto N^{-D/2}.
\]

Equivalently, the RMS spatial extent scales as

\[
R_{\mathrm{rms}}(N)\sim \sqrt{N}\,l_P,
\]

and the associated coarse-grained volume scale is

\[
V_{\mathrm{rms}}(N)\sim N^{D/2} l_P^D.
\]

This part is standard diffusion theory. The open problem is not the diffusion exponent itself.

---

## 4. Candidate Product Walk

The minimal synchronized product model is

\[
\mathcal H = \mathcal H_{\mathrm{int}} \otimes \mathcal H_{\mathrm{sp}}.
\]

At the most schematic level, one time step is represented by

\[
U = S_{\mathrm{int}} \otimes K_D.
\]

This means:

- one internal phase increment is paired with one spatial diffusion increment
- after \(N\) internal steps, the spatial sector has also evolved for \(N\) increments

This is the simplest model that can possibly produce both:

- exact \(N=3\) phase closure from the internal factor
- \(N^{-D/2}\) spatial scaling from the spatial factor

But this synchronization is still a **model choice**, not a theorem.

---

## 5. More General Coupled Form

The more honest general form is not a pure tensor product but a phase-dependent spatial kernel:

\[
U = \sum_{k \in \mathbb Z_6} |k+1\rangle\langle k| \otimes K_k,
\]

where each \(K_k\) is a spatial transition kernel associated with internal phase state \(k\).

This formulation makes the real bridge explicit:

- if all \(K_k\) collapse to the same isotropic kernel \(K_D\), one gets the synchronized product walk
- if the \(K_k\) differ, the internal walk can bias or constrain spatial diffusion

The theorem we need is effectively a statement about the family \(\{K_k\}\).

An exact quotient-cycle reduction is now available in `g3_product_walk_no_go.md`. On the
observable \(N=3\) cycle, the coupled closure amplitude reduces to an ordered spatial-kernel
product:

\[
\mathcal C_3(x_0)=\langle x_0|K_2K_1K_0|x_0\rangle.
\]

So the product-walk frontier is no longer abstract. The only remaining room for nontrivial G3
content is in the ordered spatial kernels and in the map from that closure object to
\(\alpha(l_P)\).

---

## 6. What the Product Walk Would Need to Prove

To close G3, the product-walk framework must establish four things.

### 6.1 Step Synchronization

It must derive, not assume, that the physically relevant spatial evolution time for one coherence
cycle is exactly \(N\) increments when the internal walk traverses \(N\) phase nodes.

This is the missing statement:

\[
N_{\mathrm{spatial}} = N_{\mathrm{internal}} = N_{\mathrm{gen}}.
\]

### 6.2 The Correct Spatial Observable

It must choose the exact coherence object. Several inequivalent candidates exist:

- exact return probability on a lattice
- continuum return density
- heat kernel at the origin
- RMS radius or coarse-grained coherence volume

These are not interchangeable at small \(N\), especially at \(N=3\).

### 6.3 Canonical Normalization

It must derive one exact normalization instead of switching among:

- return-density normalization
- volume normalization
- phase-space mode counting
- gauge-coupling convention

Right now the exponent candidate is cleaner than the prefactor. The prefactor problem is real.

### 6.4 Bridge to the Gauge Coupling

Even once a spatial coherence object is fixed, the map

\[
\text{coherence object} \longrightarrow \alpha(l_P)
\]

must still be proven, including the \(2\pi\) factor.

---

## 7. What This Model Already Explains

Even before the missing theorem is proven, the product-walk picture explains the current tension:

### Internal walk alone

The internal \(SU(2)\)/\(\mathbb Z_6\) structure fixes the cycle length \(N=3\), but by itself it
does not produce the desired spatial diffusion exponent.

### Spatial diffusion alone

The spatial walk naturally produces \(N^{-D/2}\) scaling, but by itself it does not know why
\(N\) should equal the generation count.

### Product walk

The product-walk idea is exactly the place where those two structures could meet.

That is why it is the correct current frontier.

---

## 8. What This Model Does Not Yet Prove

This file does **not** prove:

\[
\alpha(l_P)=\frac{1}{2\pi N^{D/2}}.
\]

It also does **not** prove:

\[
\text{one internal phase step} \Rightarrow \text{one Planck-scale spatial diffusion increment}.
\]

Those are still the two core missing bridge statements.

`g3_product_walk_no_go.md` also now rules out the cleanest naive closure:

- if \(K_0=K_1=K_2\), the internal sector only fixes the period
- smooth diffusion gives the right \(N^{-D/2}\) scaling but still carries a geometric/diffusive
  prefactor
- nearest-neighbor bipartite lattice return is exactly zero at odd \(N=3\)

And `g3_triangular_gaussian_family.md` rules out the first natural phase-dependent refinement:

- the obvious \(120^\circ\)-locked triangular Gaussian family still collapses to a commutative,
  \(C_3\)-averaged Gaussian
- its coefficient depends on continuous covariance data rather than being fixed by the phase cycle

And `g3_wilson_loop_toy_model.md` constrains the next holonomy-style refinement:

- the same-axis \(120^\circ\) SU(2) Wilson loop is rigid but trivial, giving only the central
  \(\mathbb Z_2\) lift
- the first genuinely noncommuting \(C_3\)-symmetric cone family still leaves a free cone angle
  \(\beta\)

---

## 9. Precise Theorem Target

The missing theorem can now be stated in model language:

> For the coupled walk
>
> \[
> U = \sum_{k \in \mathbb Z_6} |k+1\rangle\langle k| \otimes K_k,
> \]
>
> the effective coherence observable after one quotient cycle satisfies
>
> \[
> \mathcal C(N,D) \propto N^{-D/2},
> \]
>
> and the induced marginal-coherence coupling is
>
> \[
> \alpha(l_P)=\frac{1}{2\pi N^{D/2}}.
> \]

To prove this, one must show:

1. why the relevant cycle length is the quotient closure \(N=3\)
2. why the coupled spatial evolution is diffusive with exactly \(N\) increments
3. why the chosen coherence observable is the physically correct one
4. why its normalization maps to the gauge coupling with a single \(2\pi\) factor

---

## 10. Current Honest Status

The product-walk model is the right next mathematical object, but it is still only a frontier
model.

What is now honest to say is:

- the internal walk is exact
- the spatial diffusion exponent is standard
- the bridge between them is isolated to one coupled-walk theorem
- the phase-independent product-walk closure is no longer a live exact candidate
- the first natural phase-dependent Gaussian family is no longer a live exact candidate
- the first natural Wilson-loop holonomy family is no longer a live exact closure candidate

That sharpens the God Equation without overselling it.

---

*This file is not a closure. It is the cleanest exact statement of the frontier that remains.*
