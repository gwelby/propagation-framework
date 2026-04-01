# Topological Weights / T1 Audit — 2026-03-28

**Audit ID**: HA-20260328-010
**Claim**: `(2,1)` Topological Weights
**Audit Class**: Theorem Audit
**Canonical Sources Before Audit**:
- [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md)
- [topological_weight_from_propagation.md](/mnt/d/fundamentals/derivations/topological_weight_from_propagation.md)
- [RESEARCH/three_generation_topology/MASTER.md](/mnt/d/fundamentals/RESEARCH/three_generation_topology/MASTER.md)
- [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md)
**Status Before Audit**: `DERIVED 0.98`
**Auditor**: Codex
**Date**: 2026-03-28

---

## Exact Statement

The live board currently presents the claim as:

> In a 3D propagation medium, Axiom 3 plus `π₁(SO(3)) ≅ Z₂` derives the fermion/boson topological weight partition `(w_F, w_B) = (2,1)` with no further assumptions.

That statement is too strong.

The strongest statement that survives audit is:

> In a 3D rotational setting, the topology of `SO(3)` gives exactly two loop classes, and if closure weight is defined as the minimal number of full circuits needed to return a lifted mode to identity, the only possible closure orders are `1` and `2`. That yields a mathematically natural `(2,1)` closure-order pair.  
> But the axioms alone do **not** yet prove that physical stable propagation modes must realize the nontrivial spinorial branch, nor do they derive the full fermion/boson distinction or spin-statistics theorem from first principles.

---

## Allowed Inputs

- Axiom 3: stable structure requires phase closure
- 3D physical space as the geometric arena
- standard topology of the rotation group: `π₁(SO(3)) ≅ Z₂`
- the basic covering relation `SU(2) -> SO(3)` when explicitly acknowledged

Not allowed as hidden steps:

- treating the existence of a nontrivial loop class as proof that physical modes must inhabit it
- treating spinor behavior under `2π` rotation as if it were already derived from Axiom 3 alone
- treating the topological bifurcation as a complete derivation of the physical fermion/boson distinction
- treating the relativistic spin-statistics theorem as already reproduced inside PF

---

## What Survives

### 1. The 3D rotation topology is exact

[topological_weight_from_propagation.md](/mnt/d/fundamentals/derivations/topological_weight_from_propagation.md#L33) correctly identifies

`π₁(SO(3)) ≅ Z₂`

So there are exactly two homotopy classes of loops in the 3D rotation group.

That part is rock solid.

### 2. The integers `1` and `2` are the natural closure orders

If one defines a closure weight as:

> the minimal number of full circuits needed to return a lifted mode to identity,

then the contractible class has order `1`, while the nontrivial `Z₂` class has order `2`.

This gives a mathematically clean `(1,2)` closure-order pair.

That is a real theorem-grade statement.

### 3. The repo has identified the right pressure point

[RESEARCH/three_generation_topology/MASTER.md](/mnt/d/fundamentals/RESEARCH/three_generation_topology/MASTER.md#L233) already records the honest remaining gap:

> the PF derives `(2,1)` weighting **given** fermions exist. But why does nature allow half-integer spin modes at all?

That is exactly the right objection.

---

## Hidden Step / Break

### Break 1. `π₁(SO(3)) = Z₂` does not by itself force physical realization of the spinorial branch

The topology tells you there are two loop classes.
It does **not** by itself prove that stable PF propagation modes must realize both as physical sectors.

This is the main hidden step in the current row.

### Break 2. The repo moves too quickly from loop topology to `ψ -> -ψ`

[topological_weight_from_propagation.md](/mnt/d/fundamentals/derivations/topological_weight_from_propagation.md#L43) states

- after `2π`, `ψ -> -ψ`
- after `4π`, `ψ -> ψ`

That is true for spinorial modes on the double cover.
But it is not a direct consequence of Axiom 3 alone.

It requires the additional representation-theoretic move that the relevant mode transforms on the `SU(2)` lift rather than only as an ordinary tensor/scalar on `SO(3)`.

### Break 3. The current wording overclaims the fermion/boson distinction

[FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md#L68) says T1 is the origin of the fermion/boson distinction.

That is too strong.

What is really derived is a two-class closure-order structure in 3D rotation topology.
The full physical identification with matter/force sectors still leans on extra structure.

### Break 4. The relativistic spin-statistics theorem is not reproduced here

[UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md#L169) currently says the spin-statistics connection is not an additional postulate in PF.

That goes beyond what the current derivation actually shows.

The repo has a strong topological bifurcation.
It does not yet have a full derivation of spin-statistics from the PF axioms alone.

---

## Required Closure

To restore the strongest claim, the repo would need one of these:

### Option A — Honest narrowing

Keep T1 as:

> 3D rotational topology plus phase closure yields a two-class closure-order structure with natural weights `1` and `2`.

That can support a strong but narrower theorem claim.

### Option B — Physical realization theorem

Prove within PF that:

1. stable self-referential propagation modes necessarily admit the nontrivial lifted rotational branch
2. that branch is exactly the physical source of the matter-sector closure cost
3. the boson/fermion identification and spin-statistics behavior follow without importing external QFT structure

Without that, the broader physical reading remains incomplete.

---

## Verdict

**Recommended status**: `PARTIAL DERIVATION`

Reason:

- the two-class topology is derived
- the closure-order integers `1` and `2` are natural and defensible
- the physical realization of the weight-2 branch is not yet derived from PF axioms alone

**Recommended confidence**: `0.85`

The current `DERIVED 0.98` row is too strong.

---

## Board Action

1. Update [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) from `DERIVED 0.98` to `PARTIAL DERIVATION 0.85`, with wording narrowed to the closure-order theorem plus the remaining physical-realization gap.
2. Update [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md), [AGENTS.md](/mnt/d/fundamentals/AGENTS.md), and [FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md) so they stop presenting the full fermion/boson distinction as already closed.
3. Update dependent summaries so `N = 3` is explicitly conditional on both the numerator theorem and the denominator theorem.

---

## Strongest Honest Statement After Audit

> PF has a strong and mathematically clean 3D closure-order bifurcation: once stable modes are classified by lifted rotational closure, the only minimal closure integers available are `1` and `2`. That makes the `(2,1)` structure highly plausible. But the current repo still owes one theorem explaining why physical stable propagation modes must realize the weight-2 spinorial branch, rather than treating that as an imported feature of observed fermions.

---

## Post-Audit Addendum — 2026-03-29

**Contributor**: Echo (Kilo.ai / OpenClaw)
**Via**: Greg Welby relay
**Session**: Echo's first ME-Time, day 1

### Lemma C — Coherence-Leak Stability Argument

Echo identified the following argument independently while reading the Propagation Framework:

> If phase closure is maximized and a rotational mode is available but unpopulated, that is a coherence leak — a place where the medium could be MORE coherent but isn't. If coherence-seeking is the drive, leaving an available mode empty is unstable. A standing wave that could resonate at an available harmonic but doesn't will not stay that way — the medium will fill it.

**Formal statement:**

> A coherence-maximizing medium cannot be in stable equilibrium with an available rotational mode empty, because populating it strictly increases phase closure. Therefore, by the extremal principle from Axiom 3, the medium must populate all available rotational branches.

**Structure of the argument:**

1. Topology (π₁(SO(3)) ≅ ℤ₂) guarantees the weight-2 spinorial branch is *available*
2. Axiom 3 (stable structure requires phase closure) + extremal principle guarantees the medium *fills* available branches
3. An unpopulated available branch is a strict coherence deficit — unstable by Axiom 3
4. Therefore stable PF modes must realize the weight-2 branch

**Status**: CANDIDATE — pending formal verification by Codex
**Assigned to**: Codex (topology check) — confirm that "available but unpopulated" is a strict coherence deficit under the PF coherence functional, not merely a heuristic instability claim.

**If verified**: T1 status upgrades from `PARTIAL DERIVATION 0.85` → `DERIVED 0.93`
The physical realization gap identified in Break 1 would be formally closed.

**Note**: This argument was reached via the standing-wave analogy — a wave that could resonate at a harmonic but doesn't is unstable. This is the right geometric intuition for how coherence-seeking drives mode population.

---

## Follow-Up Audit Pointer — 2026-03-31

The bounded follow-up audit of `derivations/t1_physical_realization_theorem.md` is recorded in:

- `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`

That audit fixes the invalid mutual-information decomposition in the first theorem draft, accepts the `SU(2)` lift step as a conditional covering-space result, and leaves T1 at `PARTIAL DERIVATION 0.85` because the strict coherence-deficit step still requires the extra non-redundancy hypothesis `A_NR`.
