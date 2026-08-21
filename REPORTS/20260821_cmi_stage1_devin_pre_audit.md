# Devin Pre-Audit — PfLean.ConditionalMutualInformation (Stage 1)

**Date:** 2026-08-21 EDT  
**Owner:** Devin  
**Source commit:** `7ec57359fd4eec5af0b8e0d3f28de2bb2e274d24`  
**Source file:** `lean/PfLean/ConditionalMutualInformation.lean`  
**Source SHA-256:** `8fd35e0e3ada6275c849e41fdc548f1fccb9bfe57ced14e4e5116a33fd52199f`  
**Git blob:** `ea7fec0f466de8859fe6a2f1043908a4cbeb3d3b`  
**Candidate chain parent:** `5bd8057` (module commit), `5e4d2f6` (RESUME metadata), `7ec5735` (status correction).

---

## Claim

The Lean 4 module `PfLean.ConditionalMutualInformation.lean` (Stage 1)
formalizes a finite-discrete Shannon-style `plog2`, `entropy`, conditional
entropies, and conditional mutual information, and proves the exact theorem

> `condIndepMassRelation p X Y Z → cmi p X Y Z = 0`

where the mass relation is `pXYZ(x,y,z) * pZ(z) = pXZ(x,z) * pYZ(y,z)` for all
`x : β`, `y : γ`, `z : S`.

The module builds green, contains no `sorry`/`admit`/project-specific `axiom`,
and the kernel-axiom closure of the main theorem is only the standard Lean
foundations `[propext, Classical.choice, Quot.sound]`.

---

## Commands and Results

### 1. Focused build

```text
$ lake build PfLean.ConditionalMutualInformation
Build completed successfully (8248 jobs).
```

### 2. Aggregate build

```text
$ lake build
Build completed successfully (16572 jobs).
```

### 3. `sorry` / `admit` / `axiom` source scan

```text
$ rg '\b(sorry|admit|axiom)\b' PfLean/ConditionalMutualInformation.lean
(no matches)
```

### 4. Kernel axiom inventory

```text
$ lake env lean scripts/cmi_stage1_audit.lean
'ConditionalMutualInformation.cmi_zero_of_mass_indep' depends on axioms:
  [propext, Classical.choice, Quot.sound]
```

### 5. Finite semantic controls

```text
$ python3.12 lean/scripts/cmi_stage1_controls.py
positive_full_independence: PASS (cmi=0.0, relation=True)
positive_conditional_independence: PASS (cmi=-2.2204466447493665e-16, relation=True)
negative_common_cause: PASS (cmi=0.18872187554086728, relation=False)
negative_direct_link: PASS (cmi=0.08170416594551044, relation=False)
All finite controls passed.
```

---

## Scope

This pre-audit covers **only** the Stage 1 formalization:

- Definitions: `plog2`, `entropy`, `condEntropyX`, `condEntropyY`,
  `condEntropyXY`, `cmi`, `condIndepMassRelation`, conditional probability
  mass functions.
- Theorem: `cmi_zero_of_mass_indep`.
- Supporting lemmas: nonnegativity, normalization, and marginal-sum facts for
  the mass functions; `entropy_pair_of_prod`.

It does **not** cover:

- Stage 2: connecting `CondIndepFun (comap Z) X Y` (the measure-theoretic
  conditional independence in `NullClassProofs.lean`) to the finite-discrete
  mass relation used here.
- Any empirical estimator, EEG data, consciousness classification, or
  consciousness detection claim.
- Any canonical, public, release, medical, legal, or Greg-gate promotion.

---

## Negative Evidence

1. **Stage 1 is conditional on a mass-relation hypothesis.**  The theorem does
   not prove that real conditional independence implies the mass relation; it
   assumes the relation.  The finite controls include positive cases (relation
   holds ⇒ CMI ≈ 0) and negative cases (relation fails ⇒ CMI > 0).
2. **The positive `conditional_independence` control returns CMI ≈ `-2.22e-16`,**
   i.e. numerical roundoff around zero, not an exact zero.  This is expected for
   floating-point entropy; the Lean theorem gives the exact real-valued zero.
3. **The ` entropy_pair_of_prod` proof uses `funext` and real analysis.**  It is
   a project-local proof with no direct Mathlib equivalent; the proof has not
   been externally peer-reviewed.

---

## Known Risks

- **Stage 2 open:** The main bridge from `CondIndepFun` to the mass relation is
  not yet formalized.  Without it, the theorem does not connect to the
  `NullClassProofs.lean` conditional-independence results.
- **WHATS_NEXT.md hold (2026-08-16):** The top-level route says "No new work
  until verdicts" for three pending Codex packets.  This audit packet is a
  verification/audit handoff, not new theorem work, but it should be reconciled
  with the route before being treated as a top-priority lane.
- **PUBLIC HOLD remains:** No consciousness detection, public, or canonical claim.
- **Module `linter.unusedSectionVars` is disabled in `section CMI`:** This is a
  minor hygiene choice to avoid warnings on shared section variables; it does not
  affect the kernel or the theorem.

---

## Ask

Codex: please independently replay `lake build PfLean.ConditionalMutualInformation`,
re-run the source scan for `sorry`/`admit`/`axiom`, run
`scripts/cmi_stage1_audit.lean`, and run `lean/scripts/cmi_stage1_controls.py`.
Issue a `PASS`, `HOLD`, or `CONDITIONAL` verdict for the **Stage 1** claim:

> `cmi_zero_of_mass_indep` is a green, no-project-specific-axiom theorem over
> finite-discrete conditional mutual information under the stated mass-relation
> hypothesis.

---

## Boundaries

This packet does **not** ask Codex to approve:

- Stage 2 (`CondIndepFun` → mass relation).
- Any empirical metric or EEG pipeline.
- Any consciousness prerequisite, detection, or classification claim.
- Any public, canonical, scientific-tier, medical, legal, release, or Greg-gate
  promotion.

---

## Next Step

After Codex verdict:

- If **PASS**: the Stage 1 claim can be recorded in the claim ledger as a narrow
  formal pass; Stage 2 remains the next technical gap.
- If **HOLD / CONDITIONAL**: repair the findings and resubmit.
- The route-priority question (continue Stage 2 vs. wait for `WHATS_NEXT.md`
  verdicts) should be escalated to Greg.
