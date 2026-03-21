# G3: Restricted No-Go for Naive Product-Walk Bridges
*Exact reduction for the coupled walk, and what the cleanest spatial models cannot do*

**Date**: 2026-03-21  
**Author**: Codex  
**Task**: Attack G3 by proving the strongest honest restricted statement available from the exact model  
**Status**: EXACT REDUCTION + RESTRICTED NO-GO — narrows the frontier without closing G3  
**Builds on**: `phase_closure_exact_model.md`, `product_walk_bridge_model.md`, `exact_return_N3_D3.md`, `g3_coupling_bridge.md`, `g3_theorem_audit.md`  
**Current claim status**: Keeps the God Equation at **ARGUED (0.75)** and G3 at **PARTIAL / ARGUED (0.60)**  

---

## 1. Why This File Exists

The current G3 frontier is no longer vague.

The exact internal model is fixed:

- the observable generational walk is a 3-cycle on \(\mathbb Z_3\)
- the lifted spinorial walk is a 6-cycle on \(\mathbb Z_6\)
- the bare internal return object is periodic, not diffusive

The remaining question is therefore specific:

> Can a coupled internal-phase/spatial product walk produce the exact boundary object needed for
> \[
> \alpha(l_P)=\frac{1}{2\pi N^{D/2}}?
> \]

This file proves two restricted facts:

1. in the exact coupled model, the 3-step closure amplitude reduces to an ordered product of spatial kernels
2. the cleanest naive spatial models do not close the bridge exactly

That does not solve G3. It removes a class of bad candidate closures.

---

## 2. Exact Coupled-Walk Setup

Work directly on the observable generation quotient

\[
\mathcal H_{\mathrm{gen}} = \ell^2(\mathbb Z_3),
\]

with basis \(\{|j\rangle : j \in \mathbb Z_3\}\) and cyclic shift

\[
\bar S |j\rangle = |j+1 \bmod 3\rangle.
\]

Let the spatial sector be a Hilbert space \(\mathcal H_{\mathrm{sp}}\) with kernels \(K_j\) acting on it.

The most honest one-step coupled walk is

\[
U = \sum_{j \in \mathbb Z_3} |j+1\rangle\langle j| \otimes K_j.
\]

This is the quotient version of the more general `product_walk_bridge_model.md` ansatz. It is the
right place to study the \(N=3\) closure problem because the observable cycle is exactly length 3.

Fix a reference spatial state \(|x_0\rangle\). Define the literal 3-step closure amplitude

\[
\mathcal C_3(x_0) = \langle 0, x_0 | U^3 | 0, x_0 \rangle.
\]

---

## 3. Exact Reduction Theorem

### Theorem 1

For the coupled walk above,

\[
U^3 = \sum_{j \in \mathbb Z_3} |j\rangle\langle j| \otimes K_{j+2}K_{j+1}K_j.
\]

Therefore

\[
\mathcal C_3(x_0) = \langle x_0 | K_2 K_1 K_0 | x_0 \rangle.
\]

### Proof

Apply one step:

\[
U(|j\rangle \otimes |\psi\rangle) = |j+1\rangle \otimes K_j |\psi\rangle.
\]

Apply a second step:

\[
U^2(|j\rangle \otimes |\psi\rangle) = |j+2\rangle \otimes K_{j+1}K_j |\psi\rangle.
\]

Apply a third step:

\[
U^3(|j\rangle \otimes |\psi\rangle) = |j\rangle \otimes K_{j+2}K_{j+1}K_j |\psi\rangle.
\]

Since this holds on the basis, the operator identity follows. Evaluating at \(|0,x_0\rangle\)
gives the stated closure amplitude.

\[
\square
\]

### Corollary 1

If the spatial kernel is phase-independent, \(K_0 = K_1 = K_2 = K\), then

\[
\mathcal C_3(x_0) = \langle x_0 | K^3 | x_0 \rangle.
\]

In that restricted model, the internal sector contributes only the cycle length \(N=3\). All
nontrivial G3 content moves into the spatial return object.

### Corollary 2

For any exact derivation of G3 inside this coupled framework, the only possible source of a
nontrivial coefficient beyond the bare period is:

- the ordered product \(K_2 K_1 K_0\), or
- the map from \(\mathcal C_3\) to the coupling \(\alpha(l_P)\)

The internal quotient walk by itself cannot supply the needed coefficient once the closure
observable is written exactly.

---

## 4. Restricted No-Go A: Smooth Diffusion Does Not Give the Exact Bare Coefficient

Now restrict further to the phase-independent case:

\[
K_0 = K_1 = K_2 = K_t,
\]

where \(K_t\) is the time-\(t\) kernel of an isotropic diffusion semigroup on a smooth
\(D\)-dimensional manifold \(M\).

For any such smooth diffusion with local diffusivity \(\kappa\), the on-diagonal heat kernel has the
standard short-time form

\[
k_t(x,x) = (4\pi \kappa t)^{-D/2}\Big(1 + a_1(x)t + O(t^2)\Big).
\]

Taking the 3-step cycle time to be \(t = N\tau\) gives

\[
k_{N\tau}(x,x) = (4\pi \kappa \tau)^{-D/2} N^{-D/2}\Big(1 + a_1(x)N\tau + O((N\tau)^2)\Big).
\]

### Consequence

The literal smooth return density naturally gives the **right exponent** \(N^{-D/2}\), but its
coefficient is fixed by the diffusion generator, not canonically by the cycle count alone. It comes
with a kernel prefactor

\[
c_D(\kappa,\tau) = (4\pi \kappa \tau)^{-D/2},
\]

plus curvature corrections on a non-flat manifold.

So:

- **scaling** can come from smooth diffusion
- the **exact coefficient** needed for \(1/(2\pi N^{D/2})\) is not derived from the literal return density alone

Any successful derivation must therefore add one of:

- a canonical normalization of the return object into a mode count
- a different coherence observable than the literal on-diagonal kernel
- a non-smooth or nonstandard spatial model

### Honest reading

This does **not** prove that smooth diffusion can never participate in G3.
It proves the narrower statement that:

> the exact God Equation coefficient is not obtained from the bare smooth return density without an
> extra normalization story.

That is enough to rule out the naive closure.

---

## 5. Restricted No-Go B: Nearest-Neighbor Bipartite Lattices Fail Exactly at N = 3

Now take the spatial sector to be a nearest-neighbor walk on a bipartite graph \(G = A \sqcup B\),
with no stay-put term.

This includes the standard simple cubic lattice \(\mathbb Z^D\).

Let \(x_0 \in A\). One nearest-neighbor step moves every amplitude from \(A\) into \(B\), and from
\(B\) into \(A\). Therefore:

- \(K\) swaps the two parity sectors
- \(K^{2m}\) preserves them
- \(K^{2m+1}\) flips them

So for every odd step count,

\[
\langle x_0 | K^{2m+1} | x_0 \rangle = 0.
\]

In particular,

\[
\langle x_0 | K^3 | x_0 \rangle = 0.
\]

Combining this with Corollary 1 gives:

\[
\mathcal C_3(x_0) = 0
\]

for any phase-independent coupled walk whose spatial factor is a nearest-neighbor bipartite lattice
kernel.

### Consequence

The literal origin-return probability at \(N=3\) cannot be the G3 coherence observable on a simple
cubic Planck lattice.

This is stronger than a scaling objection. It is an exact finite-\(N\) obstruction.

---

## 6. What Survives These No-Go Results

The product-walk program is still alive, but the naive version is not.

Any successful G3 bridge must now break at least one of the following assumptions:

1. **Phase-independent spatial kernel**  
   The ordered product \(K_2 K_1 K_0\) must matter, not just \(K^3\).

2. **Literal origin return as the coherence observable**  
   A coarse-grained volume, RMS horizon, or another closure functional may be required.

3. **Standard smooth-diffusion normalization**  
   The exact coefficient \(1\) in \(N^{D/2}\) must come from a canonical mode-count map, not the raw
   heat kernel.

4. **Nearest-neighbor bipartite spatial graph**  
   A simple cubic return kernel cannot work at odd \(N=3\).

This narrows the remaining viable frontier to:

- phase-dependent kernels \(K_0, K_1, K_2\)
- a nontrivial closure observable built from their ordered product
- an exact map from that observable to \(\alpha(l_P)\), including the \(2\pi\) normalization

---

## 7. Practical Impact on G3

Before this note, the product-walk idea was a broad frontier.

After this note, the honest statement is sharper:

> A factorized, phase-independent product walk cannot close G3 by itself.
> The internal sector fixes the period. The spatial sector supplies any diffusion exponent.
> Smooth diffusion gives the right scaling but not the exact coefficient.
> Simple cubic return fails exactly at \(N=3\).

That is real progress because it removes two tempting but inadequate closures:

- "just use the smooth return density"
- "just use a cubic Planck lattice return probability"

Neither is enough.

---

## 8. Updated Honest Status

**What this file establishes exactly**

- the 3-step coupled closure amplitude reduces to \(K_2 K_1 K_0\)
- the phase-independent case reduces further to a pure spatial return object
- smooth diffusion alone gives scaling, not the exact coefficient
- nearest-neighbor bipartite return gives zero at \(N=3\)

**What this file does not establish**

- a successful phase-dependent kernel family \(\{K_j\}\)
- the correct closure observable
- the exact map to \(\alpha(l_P)\)
- the \(2\pi\) normalization

So G3 does **not** upgrade from this note alone.

**Status after this note**:

- **G3** stays **PARTIAL / ARGUED at 0.60**
- **God Equation** stays **ARGUED at 0.75**

The frontier is simply narrower than before.

---

## 9. The Next Mathematical Move

The next legitimate theorem attempt is now specific:

1. Choose a genuinely phase-dependent family \(K_0, K_1, K_2\)
2. Define a closure observable that is not naive origin return
3. Prove why that observable is the physically correct Planck-boundary coherence measure
4. Derive the exact normalization that turns it into \(\alpha(l_P)\)

That is the only remaining path inside the product-walk framework.

---

*Written by Codex, 2026-03-21*  
*Purpose: narrow G3 by proving what the simplest product-walk bridges cannot do*  
