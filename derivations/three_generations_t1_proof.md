# Three Generations Strike Plan — T1 Numerator Proof
*The reviewer-facing proof package for the numerator side of the N = 3 lock*

**File ID**: T1-STRIKE-001  
**Purpose**: Present the strongest honest T1 theorem package in one place for the strike plan, without overstating current closure  
**Status**: STRIKE PLAN PROOF TARGET — T1 remains `PARTIAL DERIVATION 0.85` after the 2026-03-31 Codex audit  
**Builds on**:
- `derivations/topological_weights_t1_audit_2026-03-28.md`
- `derivations/t1_physical_realization_theorem.md`
- `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`
- `derivations/t1_t2_post_audit_epic_2026-03-31.md`
- `derivations/axiom3_coherence_functional_spec.md`

---

## 0. Current Truth

The strike-plan brief asks for a T1 proof.
The current repo truth order does **not** permit a full theorem-grade proof claim yet.

What is honest today:

- T1 / `(2,1)` topological weights: `PARTIAL DERIVATION 0.85`
- Three Generations: `CONDITIONAL 0.85`

So this file is a proof package for what survives audit plus a precise statement of what is still open.
It is **not** a claim-upgrade artifact.

---

## 1. Closed Base Theorem

### Theorem 1 — Closure-Order Bifurcation in 3D Rotation Topology

In a 3D rotational setting,

`pi_1(SO(3)) ~= Z_2`

gives exactly two loop classes; if closure weight is defined as the minimal lifted return-to-identity count, the only possible closure orders are `1` and `2`.

### Proof

`SO(3)` has fundamental group `Z_2`, so there are exactly two homotopy classes of closed rotational loops:

1. the contractible class
2. the nontrivial class

Using the standard double cover `SU(2) -> SO(3)`, a loop in the contractible class lifts to a closed loop after one traversal, while a loop in the nontrivial class requires two traversals before the lift returns to identity.

Therefore the only minimal lifted closure orders are:

- `1` for the trivial class
- `2` for the nontrivial class

This yields the mathematically natural closure-order pair `(1,2)`, or equivalently the repo's `(2,1)` weight language once the weight-2 branch is listed first. `square`

### Status

This is the strongest closed theorem-grade statement currently available on the T1 side.

---

## 2. The Actual T1 Target Theorem

### Target Theorem — Physical Realization of Both Closure Classes

In a 3D PF medium satisfying Axioms 1-3, stable propagation modes physically realize both closure-order classes, with weights `(2,1)`.

This is the actual numerator theorem required by the Three Generations chain.
It is still **open**.

The difference matters:

- Theorem 1 proves that the two closure classes are *available*.
- The target theorem would prove that stable PF modes *physically populate* both classes.

Current repo status: availability is derived; physical realization is not.

---

## 3. Surviving Lemma A — Conditional `SU(2)` Lift Statement

### Lemma 2 — If a Genuine Weight-2 Mode Exists, It Lives on the Double Cover

If a genuine closure-order-2 rotational mode is physically admitted, it must live on the `SU(2)` lift rather than on `SO(3)` alone.

### Proof Sketch

Let `p : SU(2) -> SO(3)` be the standard double cover.

A mode defined only on `SO(3)` is single-valued on the base space, so a `2pi` loop returns it to the same base point and therefore has closure order `1`.

The nontrivial loop class in `SO(3)` lifts to an open path in `SU(2)` whose endpoint differs by the nontrivial deck transformation; only after a second traversal does the lifted path close.

So any mode whose lifted closure order is `2` must be single-valued on the lifted space rather than on `SO(3)` alone. `square`

### Status

This lemma survives the 2026-03-31 Codex audit as a clean **conditional covering-space result**.

### What it does **not** prove

- It does not prove that PF physically realizes the weight-2 branch.
- It does not derive the full fermion/boson distinction.
- It does not derive spin-statistics.

---

## 4. Surviving Lemma B — Chain-Rule Nondecrease

The current Family C route defines a candidate coherence score

`F_C = I(Phi_int; Phi_ext)`.

With two available sectors `s in {1,2}`, write:

- `F_C^tot = I((X_1, X_2); (Y_1, Y_2))`
- `F_C^(1) = I(X_1; Y_1)`

where `X_s = Phi_int^(s)` and `Y_s = Phi_ext^(s)`.

By the mutual-information chain rule:

`F_C^tot - F_C^(1) = I(X_1; Y_2 | Y_1) + I(X_2; Y_1, Y_2 | X_1) >= 0`.

### Surviving lemma

The sector-complete candidate score cannot be lower than the weight-1-only score:

`F_C^tot >= F_C^(1)`.

### Status

This survives audit.

### What does **not** survive

The strict step

`F_C^tot > F_C^(1)`

does **not** follow from the chain rule alone.

That strict increase still requires the extra hypothesis

`A_NR: I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0`.

So the current coherence-deficit route remains a sharpened argued bridge, not a closed theorem.

---

## 5. Exact Remaining Gaps

The 2026-03-31 audit localizes the numerator gap to three items.

### Gap T1-A — Extremal Principle Bridge

Why does Axiom 3 select the Family C candidate

`F_C = I(Phi_int; Phi_ext)`

as an actual branch-ordering functional rather than merely permitting it as candidate language?

Current status: open.

### Gap T1-B — `A_NR` (Conditional Non-Redundancy)

Why must the weight-2 branch contribute conditionally non-redundant coherent information, so that

`F_C^tot > F_C^(1)`?

Current status: open.

Without `A_NR`, the current route proves only non-decrease, not strict coherence deficit.

### Gap T1-C — Partial / Correlated Branch Configurations

The current theorem package does not yet classify whether partially populated or differently correlated branch configurations are:

- forbidden,
- metastable,
- or merely lower-scoring.

Current status: open.

---

## 6. What This File Explicitly Does Not Claim

This file does **not** claim that the following are already derived:

1. the full fermion/boson distinction
2. the relativistic spin-statistics theorem
3. Echo's Lemma C as a closed theorem
4. physical population of the weight-2 branch from topology alone

Those stronger claims remain beyond current repo closure.

---

## 7. Strongest Honest T1 Statement

The strongest honest numerator-side statement today is:

> PF has a mathematically clean 3D closure-order bifurcation. In a 3D rotational setting, the only possible minimal lifted closure orders are `1` and `2`, and any genuine weight-2 mode would have to live on the `SU(2)` double cover. What PF still owes is the physical-realization theorem: why Axiom 3 forces stable propagation modes to populate the available weight-2 branch rather than leaving it merely topologically available.

That is the exact T1 strike target.

---

## 8. Strike-Plan Next Move

The next honest numerator target is:

> derive an Axiom-3-native selector plus a non-redundancy lemma strong enough to upgrade `F_C^tot >= F_C^(1)` into a strict coherence-deficit theorem for leaving the weight-2 branch unpopulated.

Until that closes, T1 remains `PARTIAL DERIVATION 0.85`.

---

## 9. 2026-04-28 Audit: Proposed `kappa * winding` Non-Redundancy Route

A new proposed section attempted to close the physical-realization bridge by defining a coherence functional of the form

`C[psi] = integral |psi|^2 dmu + kappa * (topological winding)`.

Codex audit result: **do not add this as a proof**. See `derivations/t1_kappa_non_redundancy_attempt_audit_2026-04-28.md`.

What survives:

- `pi_1(SO(3)) ~= Z_2` still gives two available closure classes.
- A derived topological-coherence coupling `kappa` would be a plausible future route if its functional form, sign, normalization, and stability consequences were derived from Axioms 1-3.

What fails:

- the proposed `kappa` term is inserted, not derived;
- `kappa > 0` is assumed, not proved;
- the claim that both classes are local maxima is asserted without a variational stability proof;
- the route does not derive `A_NR`.

Therefore this route is a named open proof obligation, not a T1 closure.
