# Wave 7+8+9 Report: Negative Fixtures, Measurement Completeness, and Integration

**Date:** 2026-08-02
**Waves:** AUDIT-007, AUDIT-008, AUDIT-009
**Status:** ✅ COMPLETE — all proofs compile, `lake build` green (16534 jobs, 0 errors)
**Files:** `PfLean/AuditProtocol.lean`, `PfLean/MoneyResearchAudit.lean`

---

## Overview

These three waves complete the audit protocol:

- **Wave 7** — Negative fixtures: prove the audit catches each type of violation
- **Wave 8** — Measurement completeness: extend the iff to the full 10-check audit
- **Wave 9** — Integration: wire the verified iff into the Money-Research claim ledger

---

## Wave 7: Negative Fixtures (9 total)

Each fixture constructs a minimal violating ledger and proves the corresponding
`Check.X` predicate fails. This verifies the audit is not vacuously true — it
actively catches violations.

### Existing fixtures (Wave 3, verified in Wave 7a)

| # | Violation | Theorem |
|---|-----------|---------|
| 1 | Empty falsifier | `emptyFalsifierLedger_fails_falsifierCheck` |
| 2 | Self-dependency | `selfDepLedger_fails_selfDepCheck` |
| 3 | 2-cycle (A↔B) | `cyclicLedger_fails_cycleCheck` |
| 4 | Falsified measurement with OK status | `falsifiedOutcomeLedger_fails_measurementCheck` |
| 5 | 3-cycle passes 2-cycle check but fails acyclic | `cycle3Ledger_fails_acyclicCheck` |

### New fixtures (Wave 7b)

| # | Violation | Theorem | Strategy |
|---|-----------|---------|----------|
| 6 | Unresolved dependency | `unresolvedDepLedger_fails_depResolvedCheck` | Apply `h` to get `∃ e' ∈ entries, e'.name = "nonexistent"`, then `simp` shows no entry matches |
| 7 | Duplicate entry names | `dupNamesLedger_fails_uniqueNamesCheck` | Prove `map name = ["dup_test", "dup_test"]`, then `native_decide` on `¬Nodup` |
| 8 | Empty evidence | `emptyEvidenceLedger_fails_evidenceCheck` | Apply `h` to the entry, `simp` shows `evidence = ""` contradicts `≠ ""` |
| 9 | OK claim depends on HOLD claim | `gatedDepLedger_fails_statusGateCheck` | Apply `h` to get `e'.status = .OK`, contradict `e'.status = .HOLD` |

### Key technique for fixture 7 (duplicate names)

`Check.uniqueEntryNames` is a `Prop` (`Nodup`), not a `Bool`. The proof uses
definitional equality to convert `h : Check.uniqueEntryNames dupNamesLedger`
to `h_nodup : (dupNamesLedger.entries.map ClaimEntry.name).Nodup`, then
rewrites the map to `["dup_test", "dup_test"]` and uses `native_decide` to
prove `¬Nodup ["dup_test", "dup_test"]`.

---

## Wave 8: Measurement Completeness

### Theorems proven

1. **`runMeasurementOutcomeConsistent_complete`** — if
   `Check.measurementOutcomeConsistent cl contracts outcomes` holds, then
   `(runMeasurementOutcomeConsistent cl contracts outcomes).passed = true`.

   Strategy: prove the filter of violations is empty using
   `List.filter_eq_nil_iff`. For each contract `c`:
   - Case `outcomes c.claimName = none`: vacuously true (filter predicate is `false`)
   - Case `outcomes c.claimName = some o`: `by_contra` + `List.any_eq_true` extracts
     a violating entry `e` with `e.status ≠ expectedStatus o`, which contradicts
     the propositional hypothesis `h c hc e he h_name`.

2. **`auditPassesWithMeasurements_implies_runAuditWithMeasurements_allPassed`** —
   the capstone completeness theorem for the 10-check audit.

   Destructures `auditPassesWithMeasurements` into `auditPasses` (first 9 checks)
   and `measurementOutcomeConsistent` (10th check), applies the Wave 6 capstone
   for the first 9 and `runMeasurementOutcomeConsistent_complete` for the 10th,
   then combines via `List.all_append`.

3. **`runAuditWithMeasurements_allPassed_iff_auditPassesWithMeasurements`** —
   the full iff for the 10-check audit, combining soundness (Wave 5) and
   completeness (Wave 8).

### Key technique: reducing the match

The `runMeasurementOutcomeConsistent` definition uses a `match` on
`outcomes c.claimName` inside the filter predicate. After
`cases h_out : outcomes c.claimName with | some o =>`, the goal still
contains `match outcomes c.claimName with ...`. The fix: `simp only [h_out]`
rewrites `outcomes c.claimName` to `some o`, which reduces the match to its
`some o` branch. Then `by_contra` + `List.any_eq_true` extracts the violation.

---

## Wave 9: Integration

### Theorems proven in `MoneyResearchAudit.lean`

1. **`moneyResearch_runAudit_allPassed`** — the computable audit passes the
   Money-Research ledger.

   ```lean
   theorem moneyResearch_runAudit_allPassed :
       (runAudit moneyResearchLedger).allPassed = true := by
     rw [runAudit_allPassed_iff_auditPasses]
     exact moneyResearch_passes_full_audit
   ```

   This is the integration bridge: the propositional certificate
   (`moneyResearch_passes_full_audit`, proven in Wave 4) is transported to
   the computable side via the verified iff (`runAudit_allPassed_iff_auditPasses`,
   proven in Wave 5+6).

2. **`moneyResearch_audit_iff`** — the iff holds for the Money-Research ledger.

3. **`moneyResearch_passes_full_audit_with_measurements`** — the 10-check
   audit passes (with empty contracts, measurement check is vacuous).

4. **`moneyResearch_runAuditWithMeasurements_allPassed`** — the computable
   10-check audit passes.

5. **`moneyResearch_audit_with_measurements_iff`** — the full 10-check iff
   holds for the Money-Research ledger.

### Significance

This is the first **end-to-end verified audit pipeline**:

1. **Source data**: 26 claims from `Money-Research/CLAIMS/claims.ndjson`
2. **Lean port**: `moneyResearchLedger` with 26 `ClaimEntry` values
3. **Propositional certificate**: `auditPasses moneyResearchLedger` (Wave 4)
4. **Iff bridge**: `runAudit_allPassed ↔ auditPasses` (Waves 5+6)
5. **Computable pass**: `(runAudit moneyResearchLedger).allPassed = true` (Wave 9)

Every link in this chain is machine-verified by the Lean kernel. If any claim
is modified in a way that violates a structural invariant, the audit will fail
at compile time.

---

## Complete Audit Protocol Status

| Wave | Content | Status |
|------|---------|--------|
| 1 | ClaimLedger data structures | ✅ |
| 2 | AuditProtocol: 10 checks + runX functions | ✅ |
| 3 | MoneyResearchAudit: 26-claim port + propositional proofs | ✅ |
| 4 | Full propositional audit certificate | ✅ |
| 5 | Soundness bridge: runX passes → Check.X holds | ✅ |
| 6 | Completeness bridge: Check.X holds → runX passes | ✅ |
| 7 | Negative fixtures: audit catches violations (9 fixtures) | ✅ |
| 8 | Measurement completeness: full 10-check iff | ✅ |
| 9 | Integration: computable audit passes Money-Research ledger | ✅ |

**The audit protocol is complete.** Both the 9-check structural audit and the
10-check audit-with-measurements have verified iff bridges, negative fixtures
confirming violation detection, and integration with the Money-Research claim
ledger.

---

## Build Verification

```
$ lake build
Build completed successfully (16534 jobs).
```

Zero errors. Only linter warnings (unused simp arguments, unused variables).
