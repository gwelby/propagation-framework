# T2 Follow-Up -- Coherence Tensor Bridge
*Replacing the scalar order-parameter ansatz with the minimal PF object forced by the conditional two-component branch*

**Date**: 2026-04-01  
**Author**: Codex  
**Status**: FOLLOW-UP NOTE -- narrows Breaks 2 and 4 from `t2_denominator_theorem_audit_2026-03-31.md`; no T2 status upgrade  
**Builds on**:
- `derivations/t1_physical_realization_theorem.md`
- `derivations/t2_denominator_theorem.md`
- `derivations/t2_denominator_theorem_audit_2026-03-31.md`
- `derivations/t1_t2_post_audit_epic_2026-03-31.md`
- `derivations/axiom3_coherence_functional_spec.md`

---

## 1. Why This File Exists

The 2026-03-31 T2 audit identified two tightly linked breaks in the co-dimension route:

1. the PF order parameter in `t2_denominator_theorem.md` was a single complex scalar ansatz,
2. the three-mode count came instead from an assumed Pauli-matrix Hamiltonian.

That mismatch made the draft internally unstable:

- the order parameter was too small to support an obvious 3-dimensional restoration sector,
- while the Hamiltonian language already contained the desired `3`.

This note makes one bounded change:

> if the conditional T1 two-component branch is granted, the natural PF order parameter is not a scalar `Psi`, but the traceless part of the local `2 x 2` coherence matrix.

That object has exactly three real components.

This does **not** close T2.
It does remove one avoidable mismatch and narrows the remaining hidden step to the defect / momentum-space theorem itself.

---

## 2. Conditional Starting Point From T1

This file does **not** re-prove T1.
It takes the strongest honest post-audit T1 statement as input:

> if PF physically realizes the weight-2 branch, the local state of that branch is two-component.

So the local branch state is represented by

`psi(x,t) in C^2 \ {0}`.

The goal is to ask:

1. what PF order parameter is naturally induced by such a local two-component branch?
2. what is the most general local linear generator acting on that branch?
3. how many independent restoration directions does that order parameter actually have?

Everything below is conditional on the T1 physical-realization bridge.

---

## 3. The Minimal PF Order Parameter Is a Coherence Tensor

The local branch amplitude `psi` itself is not yet the order parameter.
Two pieces of `psi` are not branch-distinguishing:

1. an overall phase `psi -> e^(i alpha) psi`
2. an overall intensity scale already accounted for by total local amplitude

The phase-invariant local object is the `2 x 2` coherence matrix

`Gamma = < psi psi^dagger >`

where angle brackets mean either local coarse-graining or, in the pure-state limit, direct evaluation.

`Gamma` is Hermitian and positive semidefinite, so it admits the unique decomposition

`Gamma = (rho / 2) I_2 + q_1 sigma_1 + q_2 sigma_2 + q_3 sigma_3`

with:

- `rho = tr(Gamma) in R_(>=0)`
- `q = (q_1, q_2, q_3) in R^3`
- `sigma_a` the Pauli basis for traceless Hermitian `2 x 2` matrices

Equivalently,

`Q := Gamma - (tr(Gamma)/2) I_2 = q . sigma in Herm_0(2)`

is the traceless PF coherence tensor.

### Lemma 3.1

If the local weight-2 branch is two-component, the minimal phase-invariant PF order parameter carried by that branch is the traceless coherence tensor

`Q in Herm_0(2) ~= R^3`.

### Proof

Every Hermitian `2 x 2` matrix splits uniquely into trace and traceless parts.
The real vector space of traceless Hermitian `2 x 2` matrices is spanned by `{sigma_1, sigma_2, sigma_3}`, hence is 3-dimensional over `R`.
Therefore the branch-distinguishing part of `Gamma` is exactly a 3-component real object. `square`

### Corollary 3.2

Once the conditional T1 two-component branch is granted, the scalar order-parameter ansatz in the old T2 draft is no longer minimal.

The minimal PF order parameter compatible with that branch is:

- not a single complex scalar,
- but a three-real-component coherence tensor / Bloch-vector-type object.

This directly removes Break 4 from the 2026-03-31 audit:

> the file's own order parameter is no longer too small to support a 3-dimensional restoration sector.

---

## 4. Local PF Dynamics Force a `2 x 2` Self-Adjoint Generator

The next audit objection was that the draft assumed a local Pauli-Hamiltonian language without deriving it from PF.

Here is the bounded bridge.

Take a local two-component branch state `psi`.
Assume only:

1. local PF evolution is continuous in time,
2. the local branch space is linearized near a coherent background,
3. Axiom 3 stability preserves the local branch norm under free evolution.

Then the local time evolution on `C^2` is a one-parameter norm-preserving linear flow.
By standard finite-dimensional linear algebra, its generator is anti-Hermitian, so after multiplying by `i` one may write

`i d psi / dt = H psi`

with `H` Hermitian.

Since every Hermitian `2 x 2` matrix has the unique form

`H = h_0 I_2 + h . sigma`

for some `h_0 in R` and `h in R^3`, the most general local PF generator on the conditional two-component branch is exactly of Pauli form.

### Lemma 4.1

Conditional on T1's physical two-component branch and on local norm-preserving linearized PF evolution, the general local generator is

`H = h_0 I_2 + h . sigma`.

### What this does and does not prove

What it proves:

- the Pauli decomposition is not an arbitrary import once the local branch space is `C^2`
- the `R^3` appearing in the T2 draft has a PF-native source: the traceless part of the local coherence tensor and its conjugate generator

What it does **not** yet prove:

- that `H` is already a momentum-space Hamiltonian `H(k)`
- that PF must be phrased in Fermi-point language
- that the relevant defect is already a band-touching point

So this section narrows Break 2.
It does not close it fully.

---

## 5. The Three Restoration Directions Are Order-Parameter Fluctuations

The old draft treated the three Pauli directions as algebraic gap-opening perturbations.
The audit correctly objected that this did not yet make them PF bosonic restoration modes.

With the coherence tensor `Q = q . sigma`, there is now a direct PF reading.

Let `q_*` denote a locally locked coherent background selected by Axiom 3.
Define fluctuations

`delta q = q - q_* in R^3`.

The most general quadratic local expansion of an Axiom 3 coherence functional near that background is

`F[q_* + delta q] = F[q_*] + (1/2) integral [ Z_ab d_t delta q_a d_t delta q_b - K_ab grad delta q_a . grad delta q_b - M_ab delta q_a delta q_b ] + ...`

with `a,b in {1,2,3}`.

### Proposition 5.1

At fixed spacetime point or fixed Fourier label, the internal linearized restoration sector of the conditional T1 branch has dimension at most `3`, and generically exactly `3`, because `delta q` takes values in `R^3`.

### Proof

The fluctuation field has three real components by Lemma 3.1.
The quadratic kernel acts on those three internal components.
So the internal species space of restoration directions is a real 3-dimensional space. `square`

### Corollary 5.2

If the Hessian `M_ab` is full rank and positive in the restoration sector, then the linearized PF coherence field has exactly three gapped internal restoration modes near the locked background.

These are bosonic in the usual PF sense:

- they are collective fluctuations of an order-parameter field,
- not spinorial branch amplitudes themselves,
- and quantization of such commuting real field modes gives bosonic quanta.

This is the cleanest PF-native meaning available at present for

`three independent massive restoration modes`.

### Audit caveat

This is still conditional on one model-layer statement:

> the Axiom 3 local selector must produce a full-rank quadratic restoration kernel on the coherence tensor.

That is not yet derived from Axioms 1-3 alone.
So Corollary 5.2 is a sharper conditional bridge, not a theorem-grade closure.

---

## 6. Relation to the Audited Co-Dimension Draft

The old T2 draft used the vector `h in R^3` inside

`H = h_0 I_2 + h . sigma`

but did not derive why this `R^3` should be the PF order-parameter space.

This note supplies that missing identification:

- `q in R^3` is the traceless coherence tensor of the two-component branch
- `h in R^3` is the conjugate self-adjoint generator acting on that same branch space

At fixed total local amplitude, the two `R^3` spaces are linked by linear response:

`delta E = tr(H delta Gamma) = 2 h . delta q`

So the "three perturbation directions" are no longer arbitrary Pauli coefficients inserted by hand.
They are the three directions in the PF coherence tensor itself.

This is the main structural gain of the note.

---

## 7. What This Closes

### Closed or substantially narrowed

1. **Scalar order-parameter mismatch**
   The minimal conditional PF order parameter is now a 3-component coherence tensor, not a scalar.

2. **PF source of the Pauli algebra**
   Once the local branch is `C^2`, the Pauli basis is the exact basis for the traceless observable / generator sector.

3. **Meaning of "three restoration directions"**
   They are the three components of `delta q`, i.e. fluctuations of the PF coherence tensor, not merely algebraic deformation labels.

### Still open

1. **T1 physical realization**
   This whole bridge is conditional on the weight-2 branch being physically populated.

2. **Momentum-space / Fermi-point bridge**
   This note derives a local `2 x 2` generator on branch space, not yet a full `H(k)` band-touching theorem.

3. **Axiom 3 quadratic kernel**
   The full-rank restoration Hessian on `q` is still a model-layer hypothesis, not an axiomatic theorem.

4. **Co-dimension theorem**
   The step from this local order-parameter picture to the co-dimension count of the relevant PF defect is still owed.

So the remaining T2 target is now sharper:

> derive that the PF coherence-tensor defect is the right momentum-space / defect object, and prove that its relevant local kernel is full rank in 3D.

---

## 8. Strongest Honest Statement After This Note

After the 2026-03-31 audit, T2 no longer needs to guess between a scalar order parameter and a Pauli algebra.

Conditional on T1's physical two-component branch, the minimal PF order parameter is the traceless `2 x 2` coherence tensor `Q ~= R^3`, and its linearized restoration sector is therefore three-dimensional.

What remains open is not the existence of a PF-native 3-component local restoration space.
What remains open is the final theorem connecting that local coherence-tensor picture to the exact co-dimension / Fermi-point object needed for `M = 3`.

Therefore:

- this note **does not** upgrade T2,
- but it removes one internal mismatch in the current route,
- and localizes the remaining denominator gap more tightly than before.

---

## 9. Suggested Next Audit Question

The next bounded Codex audit target should be:

> Given the coherence tensor `Q ~= R^3`, can PF derive that the relevant defect condition is `q = 0` with a full-rank linearization, and that this defect is the same object counted by the co-dimension route?

That is now the cleanest remaining theorem.
