# Three Generations Strike Plan — T2 Denominator Proof
*The reviewer-facing proof package for the denominator side of the N = 3 lock*

**File ID**: T2-STRIKE-001  
**Purpose**: Present the strongest honest T2 theorem package in one place for the strike plan, without overstating current closure  
**Status**: STRIKE PLAN PROOF TARGET — T2 remains `PARTIAL DERIVATION 0.85` after the 2026-03-31 Codex audit  
**Builds on**:
- `derivations/three_generations_t2_audit_2026-03-28.md`
- `derivations/t2_denominator_theorem.md`
- `derivations/t2_denominator_theorem_audit_2026-03-31.md`
- `derivations/t2_order_parameter_derivation.md`
- `derivations/t2_fermi_point_bridge.md`
- `derivations/t2_coherence_tensor_bridge.md`
- `derivations/t1_t2_post_audit_epic_2026-03-31.md`

---

## 0. Current Truth

The strike-plan brief asks for a T2 proof.
The current repo truth order does **not** permit a theorem-grade `M = 3` claim yet.

What is honest today:

- T2 / denominator theorem: `PARTIAL DERIVATION 0.85`
- Three Generations: `CONDITIONAL 0.85`

So this file is a proof package for the surviving denominator-side lemmas plus the exact open gaps.
It is **not** a claim-upgrade artifact.

---

## 1. Closed Conditional Algebra

### Theorem 1 — Exact N = 3 Lock Once T1 and T2 Are Granted

If the numerator theorem supplies the physical `(2,1)` closure-weight branch and the denominator theorem supplies `M = 3`, then the Koide counting law

`Q(N) = 2N / (2N + 3)`

together with the empirical target `Q = 2/3` yields `N = 3` uniquely.

### Proof

Set

`2/3 = 2N / (2N + 3)`.

Then

`2(2N + 3) = 3(2N)`

which simplifies to

`4N + 6 = 6N`,

so

`N = 3`.

For positive integers, the solution is unique. `square`

### Status

This algebra is exact.
It is **conditional** on both T1 and T2.

---

## 2. The Actual T2 Target Theorem

### Target Theorem — Denominator `M = 3` from PF Axioms

Derive the denominator

`M = 3`

from PF axioms alone via the co-dimension route, without importing observed weak-boson counting or collapsing unrelated counting arguments into one proof.

This is the actual denominator theorem required by the Three Generations chain.
It is still **open**.

---

## 3. Strongest Audited Surviving Lemma

### Theorem 2 — Conditional Local `2 x 2` Fermi-Point Lemma

If PF admits a local two-band Fermi-point description with

`H(k) = h_0(k) I + h(k) . sigma`,

then in `d = 3` the codimension of a generic band-touching point and the dimension of the gap-opening perturbation space are both `3`.

### Status

This is the strongest honest ceiling established by the March 31 T2 audit.

It is useful and real.
It is not yet the full denominator theorem.

---

## 4. Surviving Lemma A — Pauli Decomposition

### Lemma 3

Every Hermitian `2 x 2` matrix has a unique decomposition

`H = h_0 I + h . sigma`

with `h_0 in R` and `h in R^3`.

### Why it matters

This is the exact linear-algebra source of the `3`-component local perturbation space inside the two-band ansatz.

### Status

Derived inside the conditional `C^2` / `2 x 2` setting.

---

## 5. Surviving Lemma B — Conditional Co-Dimension Count

### Lemma 4

For a generic smooth map

`h : R^3 -> R^3`,

the degeneracy condition

`h(k_F) = 0`

is three scalar equations in three variables, so a generic solution is isolated and has codimension `3`.

### Why it matters

This is the local geometric source of the denominator-side `3`.

### Status

Derived as a conditional implicit-function-theorem statement.

### Named condition

This depends on Jacobian genericity at the actual PF defect; see `C_gen` below.

---

## 6. Surviving Lemma C — Mass-Space Dimension

### Lemma 5

At a Fermi point, the gap-opening perturbations are the traceless Hermitian `2 x 2` matrices

`delta H = m . sigma`,

so the perturbation space is

`P = { m . sigma : m in R^3 } ~= R^3`.

Therefore the local gap-opening perturbation space is `3`-dimensional.

### Status

Derived inside the same two-band ansatz as Lemma 3.

---

## 7. Follow-Up Scaffold — Coherence Tensor Note

The April 1 follow-up note adds one useful narrowing:

> conditional on T1's physical two-component branch, the minimal local phase-invariant order parameter is the traceless coherence tensor
>
> `Q in Herm_0(2) ~= R^3`.

This is helpful because it removes the old mismatch between:

- a scalar order-parameter ansatz, and
- a three-direction Pauli perturbation space.

### Status

This is a **follow-up scaffold**, not an audited closure.
It narrows the route but does not upgrade T2.

---

## 8. Exact Open Gaps

The denominator theorem is currently blocked by named, localized gaps.

### Gap T2-A — `d = 3` Is Still an Explicit Input

The co-dimension route uses physical three-dimensional momentum space as input.

Current status: explicit premise, not PF-derived theorem.

### Gap T2-B — `OP-1`

The single-complex-scalar order-parameter minimality claim remains only argued, not uniquely forced from Axioms 1-3.

Current status: open / argued model-layer assumption.

### Gap T2-C — `C_FP`

The PF weight-2 sector must actually possess Fermi points / band-touching points.

Current status: open.

Without `C_FP`, the local Fermi-point route may be structurally elegant but physically mis-targeted.

### Gap T2-D — `C_gen`

The Jacobian at the actual PF defect must be nonsingular enough for the generic codimension count to apply.

Current status: open.

### Gap T2-E — `C_bridge`

The three gap-opening perturbation directions must be proved to be PF massive bosonic restoration modes, not merely algebraic deformation directions of the local Hamiltonian.

Current status: open.

This is the core denominator-side hidden step named by the audits.

### Gap T2-F — `C_local`

The current mode count is local to one Fermi point.
The global PF mode count may depend on multiple defects and their topological charges.

Current status: open.

---

## 9. What This File Explicitly Does Not Claim

This file does **not** claim that the following are already derived:

1. `M = 3` from PF axioms alone
2. equivalence of co-dimension count, `SO(3)` generator count, Goldstone counting, and observed `(W+, W-, Z)` counting
3. existence of PF Fermi points from topology alone
4. restoration-mode identification from Pauli algebra alone

Those stronger claims remain beyond current repo closure.

---

## 10. Strongest Honest T2 Statement

The strongest honest denominator-side statement today is:

> If PF admits a local two-band Fermi-point description with `H(k) = h_0 I + h . sigma`, then in `d = 3` the codimension of a generic band-touching point and the dimension of the local gap-opening perturbation space are both `3`. What PF still owes is the theorem that this is the correct native defect language for the coherence field, that such Fermi points actually exist in the weight-2 sector, and that the three perturbation directions are the three massive bosonic restoration modes.

That is the exact T2 strike target.

---

## 11. Strike-Plan Next Move

The clean next denominator target is:

> derive that the relevant PF defect condition is `q = 0` with full-rank linearization, and prove that this is the same object counted by the co-dimension route.

Until that closes, T2 remains `PARTIAL DERIVATION 0.85`, and Three Generations remains `CONDITIONAL 0.85`.
