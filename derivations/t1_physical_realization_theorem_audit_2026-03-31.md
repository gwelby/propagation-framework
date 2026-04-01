# T1 Physical Realization Theorem — Codex Audit

**Audit ID**: HA-20260331-011  
**Claim**: T1 physical-realization closure for `(2,1)` topological weights  
**Audit Class**: Bounded theorem audit  
**Canonical Sources Before Audit**:
- `derivations/t1_physical_realization_theorem.md`
- `derivations/topological_weights_t1_audit_2026-03-28.md`
- `derivations/axiom3_coherence_functional_spec.md`
- `derivations/casimir_axiom3_functional_candidate_C.md`
- `CLAIMS.md`
**Status Before Audit**: `PARTIAL DERIVATION 0.85`  
**Auditor**: Codex  
**Date**: 2026-03-31

---

## Exact Claim Audited

The audited file attempts to close the remaining T1 numerator gap by formalizing Echo's Lemma C:

> if the weight-2 rotational branch is topologically available but unpopulated, the medium sits at a coherence deficit; therefore Axiom 3 should force physical population of that branch.

The file also attempts to cleanly separate the `SU(2)` lift step from the stronger physical-population claim.

---

## Audit Target 1

### Does `F_C = I(Phi_int; Phi_ext)` satisfy the acceptance tests in `axiom3_coherence_functional_spec.md` for this T1 use?

**Verdict**: **No sign-off.** `F_C` remains a candidate language, not an audit-accepted Axiom 3 functional for T1.

### What survives

1. **R1 / symmetry respect**: nothing in the revised T1 write-up visibly smuggles an axis choice or inserts a forbidden representation-dependent penalty term.
2. **R3 / no smuggled answer**: the revised T1 write-up no longer uses an illegal sectorwise decomposition and does not build in the desired answer through a term like `(J_z - J_theta)^2`.
3. The file now uses a mathematically valid information-theoretic identity (chain rule), which is an actual improvement over the prior draft.

### Why sign-off is still withheld

1. **R2 / threshold vs. selection remains unclosed**  
   The file posits an extremal principle for `F_C`, but does not derive from Axiom 3 why this exact functional orders coherent branch populations. The move from "coherent branches exist" to "the medium must populate all non-redundant branches" is still an extra bridge.

2. **Strict branch selection depends on an extra hypothesis**  
   After the correction, the file proves only

   `F_C^tot >= F_C^(1)`.

   The strict step requires an additional non-redundancy assumption:

   `A_NR: I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0`.

   That assumption is plausible, but it is not derived from Axioms 1-3 or from any previously closed lemma.

3. **R4 / Axiom 2 contact is not established as part of the T1 selector**  
   The T1 use of `F_C` does not yet show why the Axiom 3 selector should depend on the causal/kinematic structure imposed by Axiom 2, rather than functioning as a purely topological add-on.

4. **R5 / excited coherent alternatives are not classified**  
   The file does not yet classify whether partially populated or differently correlated branch configurations are forbidden, metastable, or merely lower-scoring.

### Target 1 conclusion

`F_C = I(Phi_int; Phi_ext)` is an admissible candidate language for T1, but it is **not** yet an audit-passing Axiom 3 functional. The acceptance-test gate remains open.

---

## Audit Target 2

### Is the coherence-deficit argument in Section 4 a strict proof or a heuristic?

**Verdict**: **Heuristic / argued bridge, not a strict proof.**

### Exact finding

The corrected Section 4 now proves a valid lower bound:

`F_C^tot >= F_C^(1)`.

That is all the chain rule gives automatically.

The stronger claim

`F_C^tot > F_C^(1)`

does **not** follow without the extra assumption `A_NR`.

So the strict coherence-deficit step remains unclosed. The theorem file has improved the situation by identifying the exact missing hypothesis instead of hiding it, but Proof Obligation 2 is still not derived from PF axioms alone.

### Target 2 conclusion

The repo should describe this step as:

> a sharpened conjectural bridge: the missing statement is that the available weight-2 branch contributes conditionally non-redundant coherent information, so leaving it empty is a strict coherence deficit.

That is progress, but it is not closure.

---

## Audit Target 3

### Does the `SU(2)` lift step in Section 5 import any hidden QFT structure?

**Verdict**: **No hidden QFT import detected, conditional step accepted.**

### Exact finding

The revised Section 5 uses only:

1. the closure-order definition,
2. the covering relation `SU(2) -> SO(3)`,
3. the fact that `pi_1(SO(3)) ~= Z_2`.

That is enough to justify the narrower statement:

> if a genuine weight-2 rotational mode is physically admitted, then it lives on the `SU(2)` lift rather than on `SO(3)` alone.

This is a correct covering-space statement. It does **not** by itself prove physical population of the branch, and it does **not** derive full fermion/boson identification or spin-statistics. But as a conditional topological step, it survives audit.

### Target 3 conclusion

Break 2 from the 2026-03-28 audit is now cleanly narrowed:

- the `SU(2)` lift statement is acceptable,
- the remaining live break is the Axiom 3 physical-population bridge.

---

## Overall Verdict

**Recommended status**: `PARTIAL DERIVATION`  
**Recommended confidence**: `0.85`

### Why the status does not upgrade

1. The exact topology remains derived.
2. The `SU(2)` lift step now survives as a clean conditional result.
3. But the physical-realization bridge still depends on two unclosed statements:
   - the Axiom 3 extremal principle for `F_C`
   - the conditional non-redundancy hypothesis `A_NR`

So T1 is sharper than it was on 2026-03-28, but it is still not closed.

---

## Board Wording

Use the following wording in status docs:

> Codex audit (2026-03-31): the revised T1 theorem file fixes the invalid mutual-information decomposition and cleanly isolates the `SU(2)` lift step, which survives as a conditional covering-space result. But the physical-realization bridge is still not derived: the chain rule gives only `F_C^tot >= F_C^(1)`, while strict coherence deficit requires an extra non-redundancy hypothesis `A_NR` not yet derived from Axioms 1-3. Therefore T1 remains `PARTIAL DERIVATION 0.85`.

---

## What Actually Closed

1. The information-theoretic algebra is now honest.
2. The hidden-step location is sharper.
3. The `SU(2)` lift branch is no longer the weak point.

## What Still Does Not Close

1. Why Axiom 3 chooses this exact extremal principle.
2. Why an available weight-2 branch must contribute conditionally non-redundant information.
3. Why physical population follows without adding a new axiom or corollary.

---

## Strongest Honest Statement After This Audit

> PF has a mathematically clean 3D closure-order bifurcation, and it now has a cleaner conditional statement linking genuine weight-2 modes to the `SU(2)` double cover. But the physical realization of the weight-2 branch is still an argued bridge, not a theorem: the current Family C route needs a derived extremal principle and a derived non-redundancy lemma before T1 can upgrade.
