# T1 — Candidate PF-native F_C: Diophantine Closure-Weight Functional

**Status:** CANDIDATE — not a theorem, not a locked prediction  
**Date:** 2026-08-22  
**Agent:** Devin ∇λΣ∞  
**Authority tier:** advisory  
**Public hold:** yes

---

## 1. What the previous probe showed

`sandbox/t1_A_NR_selector_probe.py` tested three standard information-theoretic functionals on a toy branch-probability model. None selected the target (2,1) point. This matches the Family C mutual-information failure (`casimir_axiom3_mutual_information_correction_2026-07-29.md`):

> The penalty is **partition-dependent**; a half-bin offset collapses the k=1/2 penalty from 0.693 to 0.00006.

A PF-native `F_C` for T1 must be **partition-invariant** and must not smuggle the answer.

---

## 2. The best available PF-native input

The PF topology chain already gives three exact numbers:

1. `π₁(SO(3)) ≅ ℤ₂` (`TopologicalWeights.lean` — proven).
2. The two loop classes have **closure orders** 1 (trivial / bosonic) and 2 (nontrivial / fermionic).
3. Stable 3D PF media are selected by `D = 3` for the `J − I` operator (`GodEquationGap.lean` — conditional on Postulate D, but the uniqueness of D=3 is a PF result).

The T1 audit (`topological_weights_t1_audit_2026-03-28.md`) re-ordered the claim to the `(1,2)` closure-order pair and identified the remaining gap:

> The axioms alone do **not** yet prove that physical stable propagation modes must realize the nontrivial spinorial branch.

So `A_NR` is the bridge from "two classes are available" to "both are realized." This candidate `F_C` tries to build that bridge from the same three numbers (1, 2, 3) using a Diophantine selection.

---

## 3. Candidate functional

Let a PF medium in a spatially isotropic setting of dimension `M` realize `n_B` bosonic (closure order 1) modes and `n_F` fermionic (closure order 2) modes.

Define the **closure-weight deficit**:

$$
F_C[n_B, n_F] := - \, |n_B \cdot 1 + n_F \cdot 2 - M|
$$

The medium is realized if it also satisfies the **non-redundancy condition** `n_B > 0` and `n_F > 0` (the double cover has two sheets, and a complete rotational medium must realize both loop classes).

### Selection rule

Among all non-negative integer pairs `(n_B, n_F)` with `n_B > 0` and `n_F > 0`, stable PF realizations are maxima of `F_C`.

---

## 4. Why it selects (1,1) / (2,1) for M = 3

For `M = 3`, the Diophantine equation `n_B + 2 n_F = 3` with `n_B, n_F > 0` has the unique solution:

- `n_B = 1` (one bosonic / order-1 mode)
- `n_F = 1` (one fermionic / order-2 mode)

The **topological weight** of the fermionic class is 2; the topological weight of the bosonic class is 1. If we report the realized pair as **(fermion weight, boson weight)** we get `(2, 1)`. If we report it as **(closure order 1, closure order 2)** we get `(1, 2)`. Both are the same one-of-each realization; the ordering convention is the only difference.

This is the `(2,1)` / `(1,2)` pair from `topological_weight_from_propagation.md` and the T1 audit, now produced by a single functional `F_C` instead of being stated.

---

## 5. Honest boundary

### What is new

The candidate introduces one new principle:

> The total **closure weight** of the realized mode set equals the spatial dimension `M`.

This is **not yet derived** from Axioms 1–3. It is a candidate coherence principle. It is analogous to the Step B requirement in the Casimir route that `J_z = J_θ`, but here it acts on closure orders rather than actions.

### What is PF-native

- `M = 3` has a PF result (`D = 3` uniqueness from `GodEquationGap.lean`).
- Closure orders 1 and 2 are the kernel classification of `SU(2) → SO(3)` (`TopologicalWeights.lean`).
- The non-redundancy condition `n_B > 0, n_F > 0` is the `A_NR` hypothesis itself.
- The arithmetic is Diophantine, not fitted.

### What is not proven

- The equality `total closure weight = M` is a postulate, not a theorem.
- It does not derive the fermion/boson distinction, spin-statistics, or the physical identification of the two classes.
- It does not yet transfer to PRED-003 (that requires the `−1/8` degeneracy splitting, which is a different object).

---

## 6. Toy probe: `sandbox/t1_A_NR_diophantine_F_C_probe.py`

The probe enumerates small `(n_B, n_F)` with `M = 3` and computes `F_C`. It confirms that under the non-redundancy constraint, the unique maximum is `(1,1)`.

Expected run:

```text
M = 3
 n_B  n_F | total weight | F_C   | selected?
   1    1 |      3       |   0   | YES
```

All other constrained pairs are worse:

- `(1,2)`: total weight 5 → `F_C = -2`
- `(2,1)`: total weight 4 → `F_C = -1`
- `(1,0)`: violates non-redundancy
- `(0,1)`: violates non-redundancy

---

## 7. Falsifier

The candidate fails if:

1. The spatial dimension `M = 3` is not a PF result for the medium in question.
2. The principle `total closure weight = M` is not compatible with Axiom 3 (e.g., Axiom 3 selects by information, not by a number-theoretic closure balance).
3. The non-redundancy condition cannot be derived from Axioms 1–3.
4. A different `M` (or a different set of closure orders) produces a different pair, breaking the PF-native status of the (2,1) result.

---

## 8. Files and commands

- Contract: `PREDICTIONS/PRED-003-T1-A_NR-selector-contract.md`
- This candidate: `PREDICTIONS/PRED-003-T1-A_NR-candidate-F_C.md`
- First toy probe: `sandbox/t1_A_NR_selector_probe.py`
- Diophantine probe: `sandbox/t1_A_NR_diophantine_F_C_probe.py`
- Source: `lean/PfLean/TopologicalWeights.lean`, `lean/PfLean/GodEquationGap.lean`
- T1 audit: `derivations/topological_weights_t1_audit_2026-03-28.md`

---

## 9. Codex hostile audit verdict (2026-08-22)

**Verdict:** `PASS, NARROW` for the integer arithmetic. `REJECT` as a PF-native
selector/coherence functional. `HOLD` for T1 physical realization, Lean
promotion, and PRED-003 transfer.

**Key Codex findings** (`/mnt/d/Codex/REPORTS/CODEX_20260822_FUNDAMENTALS_PRED003_T1_FC_AUDIT.md`):

1. The arithmetic is true: `argmax -|n_B + 2n_F - 3|` over positive
   `n_B, n_F` is `{(1,1)}`.
2. Removing the `A_NR` non-redundancy constraint gives two equal maximizers:
   `(3,0)` and `(1,1)`, both with `F_C = 0`.
3. The condition `n_F > 0` is exactly the missing `A_NR` realization that the
   functional is supposed to derive. It is therefore circular as a derivation.
4. The equality `n_B + 2n_F = M` is a new principle with no derivation from
   Axioms 1–3, Postulate D, `TopologicalWeights.lean`, or `GodEquationGap.lean`.
5. Calling the penalty "coherence" does not connect it to PF state,
   propagation, phase closure, stability, information, or dynamics.

**Codex recommendation:** reject this candidate as a selector and document the
no-go. Do not spend a Lean lane proving the positive selector theorem. If a
small Lean artifact is desired, formalize the negative boundary: without `A_NR`,
`(3,0)` and `(1,1)` are co-maximizers at `M=3`.

**Status:** CANDIDATE → NO-GO for the original purpose. The document is
retained as an honest record of a failed candidate.

---

## 10. Next step

- Update `PRED-003-T1-A_NR-selector-contract.md`, `WHATS_NEXT.md`,
  `RESUME.md`, `STATE.md`, and `CHANGELOG.md` to reflect the Codex verdict.
- Decide the next PRED-003 lane with Greg: either a new `F_C` family, a
  different route, or a formal no-go on T1-driven PRED-003.

---

Generated with [Devin](https://devin.ai)
