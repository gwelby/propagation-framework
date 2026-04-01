# T2 Denominator Theorem — Codex Audit

**Audit ID**: HA-20260331-012  
**Claim**: T2 denominator theorem `M = 3` from PF axioms (co-dimension route)  
**Audit Class**: Bounded theorem audit  
**Canonical Sources Before Audit**:
- `derivations/t2_denominator_theorem.md`
- `derivations/three_generations_t2_audit_2026-03-28.md`
- `CLAIMS.md`
- `papers/FALSIFICATION_PAPER_DRAFT.md`
**Status Before Audit**: `PARTIAL DERIVATION 0.85`  
**Auditor**: Codex  
**Date**: 2026-03-31

---

## Exact Claim Audited

The draft claims to close the denominator gap by proving:

> in a 3D PF medium, the denominator `M` in `Q(N) = 2N/(2N+M)` is `3`, because a point-like Fermi defect has co-dimension `3` and the corresponding mass-restoration space is also `3`-dimensional.

The file is careful about not importing `(W+, W-, Z)` directly. That is good.

The question is whether it proves the PF theorem, or whether it proves only a useful lemma inside an extra Hamiltonian ansatz.

---

## What Survives

### 1. The local `2×2` linear-algebra statement is exact

If one grants a local `2×2` Hermitian Hamiltonian

`H(k) = h_0(k) I_2 + h(k) · sigma`

then:

1. the degeneracy condition is `h(k_F) = 0`,
2. a generic solution in `k ∈ ℝ^3` is isolated,
3. the gap-opening perturbation space inside this ansatz is the real span of `{sigma_1, sigma_2, sigma_3}`,
4. that space has dimension `3`.

That mathematical package is sound.

### 2. The Volovik use is disciplined

The draft uses ³He-A as a structural template rather than as a substitute proof. That is acceptable.

### 3. The exact hidden-step location is sharper than before

The 2026-03-28 audit asked for a proof of:

`co-dim(point defect) = number of massive bosonic restoration modes`.

The new draft shows where a plausible `3` comes from in the local two-band language. That is a real narrowing of the gap.

---

## Hidden Steps / Breaks

### Break 1. The PF order parameter is still an ansatz, not a derivation

Section 2 defines the PF order parameter as a single complex scalar field

`Psi : ℝ^3 × ℝ -> ℂ`

with `|Psi_vac| = rho_0 > 0`.

That is a plausible minimal coherence-field ansatz.
It is **not** derived from Axioms 1-3 alone.

Axiom 3 requires coherent phase structure, but it does not by itself prove:

1. a single complex scalar order parameter,
2. a nonzero condensate vacuum expectation value,
3. that this is the right order-parameter manifold for the denominator theorem.

So the order parameter is better described as a candidate PF model layer, not an axiomatic theorem.

### Break 2. T1 does not yet derive the local `2×2` Fermi-point Hamiltonian

The draft moves:

`T1 closure-weight 2 -> two-component spinorial structure -> local 2×2 Hermitian Hamiltonian in momentum space -> Fermi point`

That chain is not currently closed.

What T1 gives, at best, is a partial closure-order theorem plus a conditional `SU(2)` lift statement.
It does **not** yet prove:

1. that the relevant PF excitation is a local two-band quasiparticle,
2. that its dynamics are exhausted by a Hermitian `2×2` Hamiltonian over momentum space,
3. that the PF denominator problem should be phrased in Fermi-point language at all.

So the Pauli-matrix decomposition is exact **once** the `2×2` Hamiltonian is granted, but the bridge from PF to that Hamiltonian is the first major hidden step.

### Break 3. Corollary 5.2 shifts, rather than closes, the named gap

Corollary 5.2 states:

> three independent gap-opening perturbation directions imply three independent massive restoration modes.

That equivalence is not proved.

What the draft actually establishes is:

- the dimension of the gap-opening perturbation space of a local `2×2` Hamiltonian is `3`.

What the draft does **not** establish is:

- that these perturbation directions are the three **bosonic** normal modes of the PF coherence field,
- that they are dynamical restoration modes rather than algebraic deformation parameters,
- that the PF order parameter has a linearized excitation spectrum whose massive sector is exactly this `ℝ^3`.

That is exactly the 2026-03-28 hidden step, just relocated into the sentence "Each such direction corresponds to one independent massive restoration mode."

### Break 4. The file's own order parameter is too small to justify three bosonic restoration modes

The draft defines the PF order parameter as a single complex scalar.
A single complex scalar has two real local components.

Without extra internal structure, one does not get an obvious three-dimensional massive restoration sector from that order parameter alone.

But the draft's three-mode count comes from the Pauli-matrix structure of the **assumed** `2×2` Hamiltonian, not from the fluctuation spectrum of the defined PF order parameter.

So the file currently contains two different structures:

1. a scalar coherence-field ansatz in Section 2,
2. a two-band Pauli-Hamiltonian ansatz in Sections 3-6.

The theorem would need a derived bridge between them.
That bridge is missing.

### Break 5. The co-dimension theorem is conditional on a non-PF genericity assumption

Section 4 correctly applies the implicit function theorem to a generic map `h : ℝ^3 -> ℝ^3`.

That is mathematically fine.

But the PF theorem needs more than a generic map in the abstract.
It needs a derivation that the actual PF map is of that form and is generic enough for the nonsingular-Jacobian argument to apply.

So Section 4 survives as a conditional mathematical lemma, not as the closed PF denominator theorem.

---

## Audit Item Verdicts

### Item A — PF order parameter definition

**Verdict**: **Not signed off as axiomatic.**

The order parameter is explicit, which is an improvement over the older Goldstone route.
But it is still a model ansatz, not a theorem from Axioms 1-3 alone.

### Item B — Derivation of `H(k) = h_0 I + h·sigma` from T1

**Verdict**: **Not signed off.**

This is the largest remaining hidden step.
The Pauli decomposition is correct once the `2×2` Hamiltonian is assumed, but T1 does not currently derive that Hamiltonian or the Fermi-point framing.

### Item C — Implicit function theorem application

**Verdict**: **Accepted as a conditional lemma.**

For a generic smooth `h : ℝ^3 -> ℝ^3`, the argument is correct.
The remaining issue is not the theorem itself; it is whether PF derives the required `h`.

### Item D — Does Corollary 5.2 close the 2026-03-28 gap?

**Verdict**: **No.**

It proves the dimension of the gap-opening perturbation space inside the assumed `2×2` Hamiltonian ansatz.
It does not yet prove that these are the massive bosonic restoration modes of the PF coherence field.

### Item E — Does `d = 3` need to be explicit?

**Verdict**: **Yes.**

This route uses `d = 3` as an input. That must remain explicit in the owning docs if this draft is cited.

---

## Overall Verdict

**Recommended status for T2**: `PARTIAL DERIVATION`  
**Recommended confidence**: `0.85`

### Why no upgrade

The draft does **not** yet prove `M = 3` from PF axioms alone.

What it does prove is narrower:

> if PF admits a local two-band Fermi-point description with Hamiltonian `H(k) = h_0 I + h·sigma`, then both the codimension of the generic band-touching point and the dimension of the gap-opening perturbation space are `3`.

That is a useful conditional lemma.
It is not yet the denominator theorem.

So the strongest honest classification remains:

- `T2`: `PARTIAL DERIVATION 0.85`
- `T3`: stays `CONDITIONAL 0.85`

---

## Board Wording

Use the following wording in status docs:

> Codex audit (2026-03-31): the new T2 denominator draft proves a useful conditional lemma inside a local `2×2` Fermi-point Hamiltonian ansatz: in 3D, the codimension of a generic band-touching point and the dimension of the gap-opening perturbation space are both `3`. But the PF theorem is not yet closed. The draft still assumes, rather than derives, the PF order parameter and the local `2×2` Fermi-point Hamiltonian, and Corollary 5.2 does not yet prove that these three perturbation directions are the three massive bosonic restoration modes of the PF coherence field. Therefore T2 remains `PARTIAL DERIVATION 0.85`.

---

## What Actually Improved

1. The co-dimension route is now much sharper.
2. The local linear-algebraic core is explicit and correct.
3. The remaining gap is no longer "somewhere in the convergence"; it is now:
   - PF -> local `2×2` Fermi-point Hamiltonian
   - perturbation directions -> bosonic restoration modes of the coherence field

---

## Strongest Honest Statement After Audit

> PF still owes one theorem connecting its coherence-field dynamics to the local two-band Fermi-point structure used in the Volovik-style co-dimension route. Until that bridge is derived, the number `3` remains strongly supported and structurally localized, but not yet proved from PF axioms alone.
