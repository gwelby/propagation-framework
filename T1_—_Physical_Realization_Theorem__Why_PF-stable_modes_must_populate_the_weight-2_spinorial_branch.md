# T1 — Physical Realization Theorem: Why PF-stable modes must populate the weight-2 spinorial branch

## What This Is

**Frontier**: Topological Weights `(2,1)` — `PARTIAL DERIVATION 0.85`  
**Blocking**: Three Generations (Ticket 3), and ultimately the God Equation  
**Source audit**: file:derivations/topological_weights_t1_audit_2026-03-28.md

The topology of `SO(3)` gives two loop classes with closure orders `1` and `2`. That part is a theorem. What is **not yet proved** is why physical stable propagation modes in the PF must realize the weight-2 spinorial branch — rather than simply existing as a topological possibility that nature ignores.

---

## The Exact Gap (from Codex audit)

> "The topology tells you there are two loop classes. It does not by itself prove that stable PF propagation modes must realize both as physical sectors."

Three hidden steps were identified:

1. `π₁(SO(3)) = ℤ₂` does not force physical realization of the nontrivial branch
2. The move from loop topology to `ψ → -ψ` requires the mode to transform on the `SU(2)` lift — not derived from Axiom 3 alone
3. The fermion/boson distinction is overclaimed; what is actually derived is a two-class closure-order structure

---

## The Candidate Argument (Echo's Lemma C — Codex audited: NO SIGN-OFF)

**Codex update, 2026-06-09:** this thread is not lost. The hostile audit exists at
`derivations/lemma_c_audit_2026-04-14.md` and returns **NO SIGN-OFF / no T1 upgrade**. T1 remains
`PARTIAL DERIVATION 0.85`. Lemma C still needs two unclosed inputs: a derived selector/extremal
principle and a branch-faithfulness / non-redundancy theorem strong enough to turn
`F_C^tot >= F_C^(1)` into a strict deficit.

From file:derivations/topological_weights_t1_audit_2026-03-28.md (Post-Audit Addendum, 2026-03-29):

> A coherence-maximizing medium cannot be in stable equilibrium with an available rotational mode empty, because populating it strictly increases phase closure. Therefore, by the extremal principle from Axiom 3, the medium must populate all available rotational branches.

**Structure:**

1. `π₁(SO(3)) ≅ ℤ₂` guarantees the weight-2 spinorial branch is *available*
2. Axiom 3 + extremal principle: the medium fills available branches (an unpopulated available branch is a strict coherence deficit — unstable)
3. Therefore stable PF modes must realize the weight-2 branch

---

## Proof Obligations

Write a formal derivation file `derivations/t1_physical_realization_theorem.md` that:

1. **States the extremal principle precisely** — what exactly does "coherence-maximizing" mean as a mathematical condition? Is it a variational principle on the coherence functional? Name the functional.
2. **Proves "available but unpopulated = strict coherence deficit"** — this is the hinge. Show that leaving the weight-2 branch empty is not a local minimum of the coherence functional, using only Axioms 1–3.
3. **Closes the `SU(2)` lift step** — show that the relevant mode must transform on the double cover, not just on `SO(3)` itself. This requires showing that the phase closure condition under Axiom 3 forces the lifted representation.
4. **States the theorem cleanly**: "In a 3D PF medium satisfying Axioms 1–3, stable propagation modes must realize both closure-order classes, with weights `(2,1)`."

---

## Acceptance Criteria

- [ ] The extremal principle is stated as a mathematical condition, not an English intuition
- [ ] The "coherence deficit" claim is proved, not asserted — the functional is named and the deficit is computed
- [ ] The `SU(2)` lift step is explicit and does not import spinor behavior from QFT
- [x] Codex audits the file and either signs off or names the remaining hidden step
- [ ] If signed off: `CLAIMS.md` updates T1 from `PARTIAL DERIVATION 0.85` → `DERIVED 0.93`
  - **Current result:** not signed off; no `CLAIMS.md` update.

**Assigned to**: Claude (draft) → Codex (audit)  
**Do not promote** without Codex sign-off.
