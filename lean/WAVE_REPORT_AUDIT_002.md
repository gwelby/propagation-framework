# Wave Report: AUDIT-002 — Measurement Outcome Consistency + General Acyclicity

**Wave ID:** AUDIT-002
**Date:** 2026-08-01
**Agent:** Devin (Cognition AI)
**Status:** GREEN — all proofs compile, full project builds clean

---

## What was built

Two new checks added to `AuditProtocol.lean`, with proofs in `AuditRegistry.lean`:

### Check 9: MeasurementOutcomeConsistent (the genuinely new invariant)

**What it checks:** For every measurement contract with a known outcome, the corresponding claim's status matches: `Confirmed → OK`, `Inconclusive → HOLD`, `Falsified → NOGO`.

**Why it matters:** This is the Lean-native formalization of the "evidence_ready vs. resolved" distinction. A claim can have a measurement contract (the measurement is planned) without the outcome having been applied (the measurement hasn't been run). This check verifies that when the outcome IS known, the status reflects it.

**What it catches that the other checks don't:** A claim with a falsified measurement that's still in status `OK`. This is exactly the failure mode that Fundamentals has violated before by hand — multiple retracted claims in CLAIMS.md history had this pattern.

**Negative fixture:** `falsifiedOutcomeLedger_fails_measurementCheck` — a claim with a `Falsified` measurement outcome but status `OK` is caught.

**PF certificate:** `pfClaimLedger_passes_measurementOutcomeConsistent` — all 4 PF measurement contracts have `Confirmed` outcomes, and all 14 claims have status `OK`. The check passes.

### Check 10: Acyclic (general cycle detection)

**What it checks:** The dependency graph has no cycles of any length (not just 2-cycles).

**Why it matters:** The 2-cycle check (`noCyclicDependencies`) only catches A→B→A. A 3-cycle (A→B→C→A) passes the 2-cycle check but is still a circular foundation. The general acyclicity check uses bounded reachability: since the graph has N nodes, any cycle must have length ≤ N, so we check that no node reaches itself in 1..N steps.

**What it catches that the 2-cycle check doesn't:** Cycles of length 3, 4, 5, etc.

**Negative fixture:** `cycle3Ledger_fails_acyclicCheck` — a 3-cycle (A→B→C→A) passes the 2-cycle check but fails the general acyclicity check. Also `cycle3Ledger_passes_2cycleCheck` proves the 3-cycle passes the weaker check, demonstrating the gap.

**PF certificate:** `pfClaimLedger_passes_acyclic` — the 14-entry PF dependency graph is a DAG. Verified by `native_decide` on all 14 entries.

---

## Updated audit structure

The audit now has **10 checks** in two tiers:

**Structural audit (9 checks, ledger-only):**
1. TierConsistency — confidence in tier's range
2. DependenciesResolved — all deps name real entries
3. UniqueEntryNames — no duplicate names
4. FalsifierNonEmpty — every claim has a falsifier
5. EvidenceNonEmpty — every claim has an evidence string
6. StatusGateConsistency — no OK claim depends on HOLD/NOGO
7. NoSelfDependency — no entry lists itself
8. NoCyclicDependencies — no 2-cycles
9. Acyclic — no cycles of any length

**Full audit with measurements (10 checks):**
10. MeasurementOutcomeConsistent — claim status matches measurement outcome

The two-tier structure means a ledger can be audited structurally without measurements (`auditPasses`), and the measurement audit is an additional layer (`auditPassesWithMeasurements`).

---

## Updated certificates

- `pfClaimLedger_passes_full_audit` — 9 structural checks pass
- `pfClaimLedger_passes_full_audit_with_measurements` — all 10 checks pass
- `pfClaimLedger_runAudit_length` — structural audit runs 9 checks
- `pfClaimLedger_runAuditWithMeasurements_length` — full audit runs 10 checks

---

## Negative fixtures (5 total)

| Fixture | What it catches |
|---------|----------------|
| `emptyFalsifierLedger_fails_falsifierCheck` | Empty falsifier string |
| `selfDepLedger_fails_selfDepCheck` | Self-dependency |
| `cyclicLedger_fails_cycleCheck` | 2-cycle (A→B→A) |
| `falsifiedOutcomeLedger_fails_measurementCheck` | Falsified measurement but OK status |
| `cycle3Ledger_fails_acyclicCheck` | 3-cycle (passes 2-cycle check, fails acyclic) |

The 3-cycle fixture is particularly valuable: it proves the general acyclicity check is **strictly stronger** than the 2-cycle check, with a concrete example where the weaker check passes but the stronger one fails.

---

## Build verification

```
lake build PfLean.AuditProtocol   → GREEN (234s)
lake build PfLean.AuditRegistry   → GREEN (3226s — native_decide for 14-entry acyclicity)
lake build                        → GREEN (16534 jobs, full project)
```

The AuditRegistry build time is longer because `native_decide` evaluates the recursive `reachesIn` function for all 14 entries of the PF ledger. This is a one-time compilation cost; the proofs are cached in `.olean` files.

---

## Lines of code (cumulative)

| File | Lines | Theorems | Negative fixtures |
|------|-------|----------|-------------------|
| AuditProtocol.lean | ~780 | 7 | 5 |
| AuditRegistry.lean | ~470 | 17 | 0 |
| **Total** | **~1,250** | **24** | **5** |

---

## What's genuinely new vs. restated

Following the framing guidance from the review:

**Genuinely new (not provable from existing infrastructure):**
- Check 9 (MeasurementOutcomeConsistent) — connects measurement layer to claim status layer
- Check 10 (Acyclic) — catches cycles of any length, strictly stronger than 2-cycle check
- Check 6 (StatusGateConsistency) — cross-claim consistency, catches OK→HOLD/NOGO dependencies

**Restated from existing proofs (value is reusability, not new catching):**
- Check 1 (TierConsistency) — already enforced by `tier_bound` field
- Check 2 (DependenciesResolved) — reuses `pfClaimLedger_wellFormed`
- Check 3 (UniqueEntryNames) — reuses `pfClaimLedger_uniqueEntryNames`

**Simple structural checks:**
- Check 4 (FalsifierNonEmpty) — string non-empty check
- Check 5 (EvidenceNonEmpty) — string non-empty check
- Check 7 (NoSelfDependency) — list membership check
- Check 8 (NoCyclicDependencies) — 2-cycle check (subsumed by Check 10)

---

## Next wave

**Wave 3: Port Money-Research claims to ClaimLedger format and run audit.**

The Money-Research `claims.ndjson` (26 claims) would be ported to Lean `ClaimEntry` values, and the structural audit run on them. This would give Money-Research the same structural audit certificate that PF now has, and would be the first cross-workspace application of the audit protocol.
