# Three Generations - Conditional Assembly Proof
*The honest T3 assembly theorem while T1 and T2 remain open*

**Status**: CONDITIONAL ASSEMBLY THEOREM - T3 remains `CONDITIONAL 0.85`  
**Purpose**: record the exact algebraic lock that upgrades immediately once T1 and T2 are both derived, without overstating present closure  
**Builds on**:
- `derivations/three_generations_t2_audit_2026-03-28.md`
- `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`
- `derivations/t2_denominator_theorem_audit_2026-03-31.md`
- `derivations/three_generations_t1_proof.md`
- `derivations/three_generations_t2_proof.md`
- `CLAIMS.md`

---

## 0. Current Truth

The algebraic T3 lock is exact.
The repo still does **not** permit a theorem-grade upgrade.

What is honest today:

- T1 / numerator route: `PARTIAL DERIVATION 0.85`
- T2 / denominator route: `PARTIAL DERIVATION 0.85`
- T3 / Three Generations: `CONDITIONAL 0.85`

So this file is an assembly theorem for the part that already closes exactly.
It is **not** a claim-upgrade artifact.

---

## 1. Conditional Input Package

The T3 algebra needs three inputs.

### Input A - T1 numerator input

PF must physically realize the closure-weight pair `(2,1)` across the relevant stable branches, so the fermionic contribution to the Koide counting law is `2N`.

Current status: **not yet fully derived**.

The live T1 blocker is not the `SU(2)` lift itself.
The live blocker is the Axiom 3 physical-population bridge: why stable PF modes must actually populate the available weight-2 branch.

### Input B - T2 denominator input

PF must supply the denominator

`M = 3`

from the native 3D defect / restoration-mode structure.

Current status: **not yet fully derived**.

The live T2 blocker is not the local Pauli count inside the conditional `2x2` Hamiltonian ansatz.
The live blocker is the PF-native bridge to that ansatz plus the proof that the three gap-opening directions are the three massive restoration modes of the PF coherence field.

### Input C - Koide target

The charged-lepton Koide ratio is exactly

`Q = 2/3`.

Current status: **DERIVED 0.95** via the geometric theorem.

---

## 2. Conditional Assembly Theorem

### Theorem

If:

1. T1 closes to the physical closure-weight input `(w_F, w_B) = (2,1)`,
2. T2 closes to the denominator theorem `M = 3`,
3. and the Koide target remains `Q = 2/3`,

then the number of fermion generations is uniquely fixed at

`N = 3`.

### Proof

Under Inputs A and B, the counting law is

`Q(N) = 2N / (2N + 3)`.

Under Input C, this must equal `2/3`, so

`2/3 = 2N / (2N + 3)`.

Cross-multiplying gives

`2(2N + 3) = 3(2N)`,

hence

`4N + 6 = 6N`.

Therefore

`N = 3`.

For positive integers, the solution is unique. `square`

---

## 3. What This File Does And Does Not Add

### What it adds

This file makes one exact point explicit:

> once the T1 numerator input and T2 denominator input are both granted, there is no further hidden step in the T3 algebra.

The T3 assembly itself is exact and trivial to audit.

### What it does not add

This file does **not** close either prerequisite theorem.

It does not prove:

1. the T1 physical-population bridge,
2. the T2 denominator theorem `M = 3`,
3. or any stronger claim about generation physics beyond the exact algebraic lock.

So the remaining uncertainty in T3 is inherited entirely from T1 and T2.

---

## 4. Exact Open Gates

### T1 gate

T1 can upgrade only if PF derives why Axiom 3 forces stable propagation modes to populate the available weight-2 branch.

The March 31 audit localizes this to:

- the extremal-principle bridge for the Family C selector, and
- a strict non-redundancy theorem strong enough to replace the external `A_NR` hypothesis.

### T2 gate

T2 can upgrade only if PF derives the denominator route rather than assuming it.

The March 31 audit localizes this to:

- the PF -> local `2x2` Fermi-point Hamiltonian bridge,
- the existence of the relevant band-touching structure in the PF weight-2 sector,
- and the proof that the three perturbation directions are the three massive bosonic restoration modes of the PF coherence field.

---

## 5. Promotion Rule

This file may be promoted from conditional assembly theorem to theorem-grade T3 proof only after:

1. `derivations/t1_physical_realization_theorem_audit_2026-03-31.md` is superseded by a Codex sign-off that upgrades T1,
2. `derivations/t2_denominator_theorem_audit_2026-03-31.md` is superseded by a Codex sign-off that upgrades T2,
3. and the owning status docs are updated in truth order.

Until then, the correct classification remains:

- T1: `PARTIAL DERIVATION 0.85`
- T2: `PARTIAL DERIVATION 0.85`
- T3: `CONDITIONAL 0.85`

---

## 6. Strongest Honest Statement

The strongest honest T3 statement today is:

> PF already has the exact algebraic lock from `Q(N) = 2N / (2N + 3)` and `Q = 2/3` to the unique solution `N = 3`. What it still lacks are the two load-bearing input theorems: why stable PF modes must physically realize the weight-2 branch, and why the PF denominator is exactly `3` from native 3D coherence dynamics. Until those two bridges close, Three Generations remains a conditional theorem rather than a derived one.
