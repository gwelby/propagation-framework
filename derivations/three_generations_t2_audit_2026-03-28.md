# Three Generations / T2 Audit — 2026-03-28

**Audit ID**: HA-20260328-008
**Claim**: Three Generations (`N = 3`) and the denominator theorem `M = 3`
**Audit Class**: Theorem Audit
**Canonical Sources Before Audit**:
- [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md)
- [FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md)
- [closing_the_gaps.md](/mnt/d/fundamentals/derivations/closing_the_gaps.md)
- [topological_pressure_derivation.md](/mnt/d/fundamentals/derivations/topological_pressure_derivation.md)
- [topological_weight_from_propagation.md](/mnt/d/fundamentals/derivations/topological_weight_from_propagation.md)
**Status Before Audit**: `DERIVED 0.98`
**Auditor**: Codex
**Date**: 2026-03-28

---

## Exact Statement

The live board currently presents the claim as:

> The number of fermion generations is uniquely fixed at `N = 3` because  
> `Q(N) = 2N / (2N + 3) = 2/3`, where the numerator comes from the `(2,1)` topological weights and the denominator `3` follows from the generators of `SO(3)` / Goldstone / co-dimension.

That statement is too strong.

The strongest statement that survives audit is:

> If one accepts the denominator theorem `M = 3`, then the algebraic step  
> `Q(N) = 2N / (2N + 3) = 2/3 -> N = 3` is exact and unique.  
> But the current repo does **not** yet have a single clean theorem proving that the denominator `3` follows from PF axioms alone. The denominator is still supported by a **convergent but not fully unified** set of arguments: co-dimension, `SO(3)` generator counting, and broken-symmetry / Goldstone language.

So the real issue is not the algebra.
It is the denominator proof.

---

## Allowed Inputs

- T1: the `(2,1)` topological weights from `π₁(SO(3)) ≅ Z₂`
- the observed empirical Koide target `Q = 2/3`
- ordinary algebra once `Q(N) = 2N / (2N + M)` is fixed
- dimensional facts about `SO(3)` and point defects in 3D

Not allowed as hidden steps:

- importing the observed electroweak triplet `(W+, W-, Z)` as if that itself were the denominator proof
- treating co-dimension, Lie-group dimension, and massive gauge-boson count as automatically identical
- invoking Goldstone or Higgs language without an explicit broken-symmetry setup and order parameter

---

## What Survives

### 1. The numerator is solid

The `(2,1)` topological weight partition is still the strongest part of this chain:

- bosonic closure weight `1`
- fermionic closure weight `2`

That survives independently of T2.

### 2. The algebraic uniqueness of `N = 3` survives once `M = 3` is granted

Given

`Q(N) = 2N / (2N + 3)`

and empirical `Q = 2/3`, the algebra is exact:

`2/3 = 2N / (2N + 3) -> N = 3`

No problem there.

### 3. The denominator arguments are converging on the same number

The repo is not inventing the number `3` from nowhere.
It has three distinct structural routes all pointing at it:

1. co-dimension of a point defect in 3D
2. dimension / generator count of `SO(3)`
3. broken-symmetry language with three slip directions

That convergence is real and valuable.

But convergence is not the same as one closed theorem.

---

## Hidden Step / Break

### Break 1. The repo is internally inconsistent about T2 status

The same repo currently says:

- [FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md#L80) — `Claim T2 (DERIVED)`
- [FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md#L314) — `T2: PARTIAL DERIVATION`
- [closing_the_gaps.md](/mnt/d/fundamentals/derivations/closing_the_gaps.md#L160) — `PARTIAL DERIVATION`
- [AGENTS.md](/mnt/d/fundamentals/AGENTS.md#L252) — “DERIVED (conditional on T2 formal proof)”

That is not one theorem state.
It is a split-brain indicator.

### Break 2. Co-dimension -> number of massive perturbation modes is not actually proved

[closing_the_gaps.md](/mnt/d/fundamentals/derivations/closing_the_gaps.md#L168) states:

> point defect in 3D -> co-dimension 3 -> three independent perturbation modes -> denominator 3

The first arrow is trivial geometry.
The second arrow is the nontrivial theorem.

The repo does not yet prove, from PF axioms alone, that:

`co-dim(point defect) = number of massive bosonic restoration modes`

That is exactly why the paper’s own honesty log still keeps T2 only partial.

### Break 3. The Goldstone / Higgs route smuggles more structure than advertised

[topological_pressure_derivation.md](/mnt/d/fundamentals/derivations/topological_pressure_derivation.md#L37) is the clearest overreach.

It moves:

- local `SO(3)` rotational structure
- spontaneous symmetry breaking
- 3 Goldstone bosons
- Higgs absorption
- 3 massive gauge bosons `(W+, W-, Z)`

This is far beyond what the PF axioms by themselves currently establish.

Specific problems:

1. no explicit PF order parameter is defined
2. no full symmetry-breaking pattern is derived
3. no gauge structure is derived from the axioms at this stage
4. the electroweak triplet appears too close to the observed answer

So this route is a strong heuristic bridge, not a theorem.

### Break 4. An older derivation still counts observed bosons directly

[topological_weight_from_propagation.md](/mnt/d/fundamentals/derivations/topological_weight_from_propagation.md#L107) writes the denominator as:

- “massive gauge boson triplet `(W+, W-, Z)`”

That is explicitly not an axiomatic denominator proof.
That is using the observed triplet.

So this file cannot support the strongest current claim row.

### Break 5. T3 cannot be stronger than unresolved T2

The live board gives:

- `Three Generations` = `DERIVED 0.98`

but the paper still gives:

- `T2` = `PARTIAL DERIVATION 0.85`

That is not coherent.

If `T3` depends on `T2`, then `T3` cannot honestly sit above an unresolved `T2`.

---

## Required Closure

To restore theorem-grade status for `N = 3`, the repo needs one of these:

### Option A — Formal co-dimension theorem

Prove within PF that:

`number of independent massive restoration modes = co-dim(point defect)`

for the relevant phase-lock defect.

This is the cleanest closure target.

### Option B — Formal broken-symmetry theorem

Specify:

1. the PF order parameter
2. the symmetry group before locking
3. the unbroken subgroup after locking
4. the exact count of broken generators
5. why these produce the relevant massive bosonic denominator

Without smuggling the Standard Model answer.

### Option C — Explicitly conditional theorem

Keep the result in this form:

> If the denominator theorem `M = 3` holds, then `N = 3` follows uniquely from `Q = 2/3`.

This is still useful and honest.

---

## Verdict

**Recommended status for T2**: `PARTIAL DERIVATION`

**Recommended status for Three Generations (`T3`)**: `CONDITIONAL`

Reason:

- the numerator survives
- the algebra survives
- the denominator proof does not yet survive as a single closed theorem

Recommended confidence:

- `T2`: keep around `0.85` as a bounded partial derivation if desired
- `T3`: reduce to `0.85` as a conditional theorem resting on T2

The current `DERIVED 0.98` board row is too strong.

---

## Board Action

1. Update [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) so `Three Generations` is no longer presented as fully derived.
2. Update [FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md) so Section 3.2 and the honesty table agree on T2/T3 status.
3. Update [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md), [AGENTS.md](/mnt/d/fundamentals/AGENTS.md), and [scale_stack_derivation_chain.md](/mnt/d/fundamentals/derivations/scale_stack_derivation_chain.md) to remove the fully locked wording.

---

## Strongest Honest Statement After Audit

> PF strongly supports the structure in which fermions carry topological weight `2` and the Koide target `Q = 2/3` uniquely selects `N = 3` once the denominator `M = 3` is fixed. But the current repo still owes one formal theorem for why the denominator is exactly `3` from PF axioms alone. Until that theorem is closed, `N = 3` is best treated as a conditional theorem rather than a fully settled derivation.

---

## Follow-Up Audit Pointer — 2026-03-31

The bounded follow-up audit of `derivations/t2_denominator_theorem.md` is recorded in:

- `derivations/t2_denominator_theorem_audit_2026-03-31.md`

That audit accepts the local `2×2` linear-algebra / co-dimension lemma inside the Fermi-point ansatz, but leaves T2 at `PARTIAL DERIVATION 0.85` because the PF order-parameter bridge, the PF -> `2×2` Fermi-point Hamiltonian bridge, and the identification of perturbation directions with massive bosonic restoration modes are still not derived from PF axioms alone.
