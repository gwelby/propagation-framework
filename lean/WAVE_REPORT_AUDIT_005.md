# WAVE REPORT: AUDIT-005 — Soundness Bridge

**Date:** 2026-08-01
**Status:** GREEN — all proofs machine-verified by the Lean kernel
**Build:** `lake build` — 16534 jobs, 0 errors, 0 sorries

---

## Goal

Prove that the computable audit checks (`runX`) are **sound**: if a computable
check passes (returns `passed = true`), then the corresponding propositional
predicate (`Check.X`) holds. This bridges the gap between the executable audit
function and the mathematical specification, establishing that a passing audit
certificate is a genuine proof of audit-worthiness.

---

## Theorems Proven

### Individual check soundness (9 theorems)

| Theorem | Computable Check | Propositional Predicate |
|---------|-----------------|------------------------|
| `runTierConsistency_sound` | `runTierConsistency` | `Check.tierConsistency` |
| `runFalsifierNonEmpty_sound` | `runFalsifierNonEmpty` | `Check.falsifierNonEmpty` |
| `runEvidenceNonEmpty_sound` | `runEvidenceNonEmpty` | `Check.evidenceNonEmpty` |
| `runNoSelfDependency_sound` | `runNoSelfDependency` | `Check.noSelfDependency` |
| `runUniqueEntryNames_sound` | `runUniqueEntryNames` | `Check.uniqueEntryNames` |
| `runDependenciesResolved_sound` | `runDependenciesResolved` | `Check.dependenciesResolved` |
| `runStatusGateConsistency_sound` | `runStatusGateConsistency` | `Check.statusGateConsistency` |
| `runNoCyclicDependencies_sound` | `runNoCyclicDependencies` | `Check.noCyclicDependencies` |
| `runAcyclic_sound` | `runAcyclic` | `Check.acyclic` |

### Capstone theorems (2 theorems)

| Theorem | Statement |
|---------|-----------|
| `runAudit_allPassed_implies_auditPasses` | If all 9 computable checks pass, then `auditPasses cl` holds |
| `runAuditWithMeasurements_allPassed_implies_auditPasses` | If all 10 computable checks (including measurement) pass, then `auditPassesWithMeasurements` holds |

### Helper theorem

| Theorem | Purpose |
|---------|---------|
| `allPassed_get` (private) | Extract the i-th check's `passed = true` from `allPassed = true` |

---

## Proof Strategy

Each soundness proof follows one of two patterns:

### Pattern 1: `List.all`-based checks (falsifier, evidence)

1. `unfold runX at h` to expose the `if` expression
2. `split at h` to case-split on the condition
3. In the `true` branch: use `List.all_eq_true` to convert `all p = true` to `∀ x ∈ l, p x = true`, then extract the specific entry
4. In the `false` branch: `simp [CheckResult.passed] at h` derives a contradiction (fail.passed = false ≠ true)

### Pattern 2: `List.filter`-based checks (self-dep, cyclic, status gate, acyclic)

1. Assume the negation of the propositional predicate (`by_contra`)
2. Show the violating entry is in the filter (`List.mem_filter`)
3. Case 1: filter is empty → contradiction (entry in `[]`)
4. Case 2: filter is non-empty → `runX` produces a fail → `passed = false` → contradiction

### Capstone theorem

The `allPassed_get` helper extracts individual check results from the
`allPassed = true` hypothesis by converting `List.all` to a universal
quantifier (`List.all_eq_true`) and accessing the i-th element via
`List.get_mem`. Each of the 9 individual soundness theorems is then applied
to produce the full `auditPasses` conjunction.

The measurement soundness theorem case-splits on `MeasurementOutcome`
(`Confirmed`, `Inconclusive`, `Falsified`) to reduce the match expression
in the propositional predicate, then uses the same filter-emptiness
contradiction pattern.

---

## Key Lean Lemmas Used

- `List.all_eq_true : l.all p = true ↔ ∀ x ∈ l, p x = true`
- `List.any_eq_true : l.any p = true ↔ ∃ x, x ∈ l ∧ p x = true`
- `List.isEmpty_eq_false_iff : l.isEmpty = false ↔ l ≠ []`
- `List.mem_filter : x ∈ l.filter p ↔ x ∈ l ∧ p x = true`
- `decide_eq_true_iff : decide p = true ↔ p`
- `List.get_mem : l.get n ∈ l`

---

## What This Means

The soundness bridge establishes that the `ClaimLedger` audit infrastructure
is **trustworthy**: a passing audit certificate (`allPassed = true`) is not
just a computational artifact — it is a mathematical proof that the ledger
satisfies all structural well-formedness predicates. No `sorry` or axioms
are used; every step is checked by the Lean kernel.

Combined with the source-fidelity bridge (Wave 3.1) and the negative fixtures
(Wave 2), the audit pipeline now has:

1. **Source fidelity:** The Lean representation matches the source data (Wave 3.1)
2. **Soundness:** Computable checks imply propositional predicates (Wave 5)
3. **Completeness (negative fixtures):** Violations are caught (Wave 2)

---

## Files Modified

- `PfLean/AuditProtocol.lean` — all soundness theorems added (lines 509–903)

---

## Next Steps

- Wave 4: Gambling specialization (applying the audit framework to gambling claims)
- Wave 6: Completeness bridge (proving the converse — if predicates hold, checks pass)
- Wave 7: Audit certificate extraction (producing a standalone certificate from a passing audit)
