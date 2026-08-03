# Wave 6 Report: Completeness Bridge

**Date:** 2026-08-02
**Wave:** AUDIT-006
**Status:** ✅ COMPLETE — all proofs compile, `lake build` green (16534 jobs, 0 errors)
**File:** `PfLean/AuditProtocol.lean`

---

## Goal

Prove the **completeness** direction of the audit correspondence:

> If the propositional audit predicate `auditPasses cl` holds, then the computable
> `runAudit cl` produces a result where `allPassed = true`.

This is the converse of Wave 5 (soundness), and together they establish the
exact iff:

```
(runAudit cl).allPassed = true ↔ auditPasses cl
```

---

## Theorems Proven

### Individual completeness theorems

Each theorem has the form `Check.X cl → (runX cl).passed = true`:

| # | Theorem | Strategy |
|---|---------|----------|
| 1 | `runFalsifierNonEmpty_complete` | `List.all_eq_true` + `decide_eq_true_iff.mpr` |
| 2 | `runEvidenceNonEmpty_complete` | `List.all_eq_true` + `decide_eq_true_iff.mpr` |
| 3 | `runNoSelfDependency_complete` | `List.filter_eq_nil_iff` + contradiction |
| 4 | `runUniqueEntryNames_complete` | `split` on `if Nodup`; false branch contradicts `h` |
| 5 | `runDependenciesResolved_complete` | Nested `List.all_eq_true` + `List.any_eq_true` |
| 6 | `runStatusGateConsistency_complete` | `List.filter_eq_nil_iff` + nested `any_eq_true` extraction |
| 7 | `runNoCyclicDependencies_complete` | `List.filter_eq_nil_iff` + `h_name ▸ hd` transport |
| 8 | `runAcyclic_complete` | `List.filter_eq_nil_iff` + `rw [h e he]` + `simp` |
| 9 | `runTierConsistency_complete` | Trivial (check always passes) |

### Capstone theorem

```
theorem auditPasses_implies_runAudit_allPassed (cl : ClaimLedger)
    (h : auditPasses cl) :
    (runAudit cl).allPassed = true
```

Destructures `auditPasses` into 9 component hypotheses, applies each
`runX_complete` theorem, then reduces `List.all_cons` / `List.all_nil`.

### Iff theorem (Wave 5 + Wave 6 capstone)

```
theorem runAudit_allPassed_iff_auditPasses (cl : ClaimLedger) :
    (runAudit cl).allPassed = true ↔ auditPasses cl
```

Combines `runAudit_allPassed_implies_auditPasses` (Wave 5 soundness) with
`auditPasses_implies_runAudit_allPassed` (Wave 6 completeness) into a single
`⟨_, _⟩` proof.

---

## Key Proof Techniques

1. **`List.filter_eq_nil_iff`** — the workhorse for filter-based checks.
   Instead of trying to rewrite the `if violations.isEmpty = true` condition
   directly (which fails because `unfold` produces a `let`/`have` binding that
   blocks `rw` and `split`), we prove the filter equals `[]` first, then
   derive `isEmpty = true` by `rfl`, then `simp only [h_cond, if_true, ...]`.

2. **`List.all_eq_true` + `decide_eq_true_iff.mpr`** — for `all`-based checks
   (falsifier/evidence non-empty, dependencies resolved). The propositional
   hypothesis gives `p x` (a Prop); `decide_eq_true_iff.mpr` converts it to
   `decide (p x) = true` (the Bool the computable check expects).

3. **`h_name ▸ hd`** — term transport in `runNoCyclicDependencies_complete`.
   From `e₂.name = d` and `d ∈ e₁.dependencies`, we get `e₂.name ∈ e₁.dependencies`,
   which contradicts the `noCyclicDependencies` hypothesis.

4. **Avoiding `split` on `let`-bound `if`** — several `runX` definitions use
   `have violations := ...; if violations.isEmpty then ...`. The `split` tactic
   cannot see through the `have` binding. The fix: prove the condition
   (`isEmpty = true`) as a separate `have`, then `simp only [h_cond, if_true]`.

---

## Build Verification

```
$ lake build
Build completed successfully (16534 jobs).
```

Zero errors. Only linter warnings (unused simp arguments, unused variables) —
all pre-existing from earlier waves.

---

## Significance

With Wave 5 (soundness) and Wave 6 (completeness) both complete, the audit
protocol now has a **machine-verified exact correspondence**:

```
(runAudit cl).allPassed = true ↔ auditPasses cl
```

This means:
- The computable audit function `runAudit` is **faithful** to the propositional
  specification `auditPasses` — it neither misses violations (soundness) nor
  reports false failures (completeness).
- Any future change to `runX` or `Check.X` that breaks this correspondence will
  fail at compile time.
- The audit protocol is a **verified bridge** between executable code and
  formal specification — the same property that makes CompCert and seL4
  trustworthy.

---

## Next Steps

- Wave 7: Negative fixtures (verify the audit catches constructed violations)
  — already partially present in the file (lines 1094+).
- Measurement completeness: extend the iff to `runAuditWithMeasurements`.
- Integration: wire the verified audit into the Money-Research claim ledger.
