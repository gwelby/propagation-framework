# Wave Report: AuditProtocol — Machine-Checked Audit of Claim Ledgers

**Wave ID:** AUDIT-001
**Date:** 2026-08-01
**Agent:** Devin (Cognition AI)
**Status:** GREEN — all proofs compile, full project builds clean

---

## What was built

Two new Lean 4 modules in `/mnt/d/Fundamentals/lean/PfLean/`:

### 1. `AuditProtocol.lean` (~500 lines)

The core audit infrastructure. Defines:

**Types:**
- `AuditCheck` — inductive type with 8 check identifiers
- `CheckResult` — pass/fail with detail strings
- `AuditResult` — list of check results with `allPassed`, `passCount`, `failCount`, `summary`

**8 propositional audit checks** (each a `Prop` predicate on `ClaimLedger`):
1. `tierConsistency` — confidence in tier's allowed range
2. `dependenciesResolved` — every dependency name exists in ledger
3. `uniqueEntryNames` — no two positions share a name
4. `falsifierNonEmpty` — every claim has a stated falsifier
5. `evidenceNonEmpty` — every claim has an evidence string
6. `statusGateConsistency` — no OK claim depends on HOLD/NOGO
7. `noSelfDependency` — no entry lists itself as dependency
8. `noCyclicDependencies` — no 2-cycles in dependency graph

**8 computable audit functions** (each returns `CheckResult`):
- `runTierConsistency`, `runDependenciesResolved`, `runUniqueEntryNames`,
  `runFalsifierNonEmpty`, `runEvidenceNonEmpty`, `runStatusGateConsistency`,
  `runNoSelfDependency`, `runNoCyclicDependencies`
- `runAudit` — runs all 8 and returns `AuditResult`

**Theorems:**
- `tierConsistency_holds` — holds for any well-typed ledger (by `tier_bound`)
- `statusGateConsistency_when_all_OK` — trivially satisfied when all OK
- `runTierConsistency_always_passes` — computable check always passes
- `runAudit_length` — audit always runs exactly 8 checks
- `runAudit_tierConsistency_sound` — soundness direction for tier check

**3 negative fixtures** (the audit catches violations):
- `emptyFalsifierLedger_fails_falsifierCheck` — empty falsifier caught
- `selfDepLedger_fails_selfDepCheck` — self-dependency caught
- `cyclicLedger_fails_cycleCheck` — 2-cycle caught

### 2. `AuditRegistry.lean` (~370 lines)

Runs the audit against the real `pfClaimLedger` (14 entries) and proves it passes.

**The audit certificate:**
- `pfClaimLedger_passes_tierConsistency`
- `pfClaimLedger_passes_dependenciesResolved`
- `pfClaimLedger_passes_uniqueEntryNames`
- `pfClaimLedger_passes_falsifierNonEmpty`
- `pfClaimLedger_passes_evidenceNonEmpty`
- `pfClaimLedger_passes_statusGateConsistency`
- `pfClaimLedger_passes_noSelfDependency`
- `pfClaimLedger_passes_noCyclicDependencies`
- **`pfClaimLedger_passes_full_audit`** — the capstone: all 8 checks pass

**Measurement ledger audit:**
- `pfMeasurementLedger_full_passes_contractsResolved`
- `pfMeasurementLedger_full_passes_uniqueContractNames`

---

## Build verification

```
lake build PfLean.AuditProtocol   → GREEN (226s)
lake build PfLean.AuditRegistry   → GREEN (197s)
lake build                        → GREEN (16534 jobs, full project)
```

Zero errors. Only pre-existing linter warnings from other modules (WeinbergAngle, PeriodOrbitRefactor, MeasurementLedger).

---

## What the certificate says

The Lean kernel has verified that the PF claim ledger (14 entries) is **structurally honest**:

| Check | What it verifies | Result |
|-------|-----------------|--------|
| TierConsistency | Confidence in tier's range | PASS (by construction) |
| DependenciesResolved | All deps name real entries | PASS (14/14) |
| UniqueEntryNames | No duplicate names | PASS (14/14) |
| FalsifierNonEmpty | Every claim has falsifier | PASS (14/14) |
| EvidenceNonEmpty | Every claim has evidence | PASS (14/14) |
| StatusGateConsistency | No OK→HOLD/NOGO deps | PASS (all OK) |
| NoSelfDependency | No entry deps on itself | PASS (14/14) |
| NoCyclicDependencies | No 2-cycles | PASS (14×14) |

---

## What the certificate does NOT say

This is the honest boundary. The Lean audit certifies **structural** honesty. It does NOT certify **semantic** honesty:

- ❌ Whether evidence strings semantically support the claims
- ❌ Whether the prose overclaims
- ❌ Whether the sources say what we attribute to them
- ❌ Whether the falsifiers are actually testable

Those require a human or LLM audit (Codex hostile review). Both are needed. The Lean audit is necessary but not sufficient.

This is the same distinction as the PhiFlow bug: tests checked the structure (coherence computation runs) but not the semantics (does CLI output match what the user sees?). The Lean audit catches structural issues. The semantic audit catches the rest.

---

## Why this is novel

The OpenAI Ten Proofs repo formalizes mathematical results. The ClaimLedger formalizes epistemic tiers. But **nobody has formalized the audit process itself in a proof assistant** — the act of checking whether a claim system is internally consistent.

That's because most people don't have a ClaimLedger. We do. The audit formalization is the natural next layer on top of it.

---

## Architecture

```
ClaimLedger (existing)          → what claims are, their tiers, dependencies
MeasurementContract (existing)  → how measurements confirm/falsify claims
MeasurementLedger (existing)     → linking contracts to claims
AuditProtocol (NEW)              → the process of checking the whole system
AuditRegistry (NEW)              → machine-checked certificate for PF claims
```

The audit doesn't care what the claims are about. It checks the structure. This means it can be run on any claim system that uses the ClaimLedger structure — PF, Money-Research, Gambling, any future workspace.

---

## Lines of code

| File | Lines | Theorems | Negative fixtures |
|------|-------|----------|-------------------|
| AuditProtocol.lean | ~500 | 5 | 3 |
| AuditRegistry.lean | ~370 | 13 | 0 |
| **Total** | **~870** | **18** | **3** |

Under the ~1,400-1,700 line estimate. The build was smaller than projected because the existing ClaimLedger infrastructure already provided most of the predicates — the audit reuses `dependenciesResolved`, `uniqueEntryNames`, and the `tier_bound` field directly.

---

## Next waves

**Wave 2: Port Money-Research claims to ClaimLedger format.**
The Money-Research `claims.ndjson` (26 claims) would be ported to Lean `ClaimEntry` values, and the audit run on them. This would give Money-Research the same structural audit certificate that PF now has.

**Wave 3: Port Gambling claims and formalize the 9-step Prediction Audit Protocol.**
The gambling `prediction-audit` skill's 9-step protocol would be formalized as a specialization of the general audit. Each step becomes a Lean function. The audit of a gambling system becomes a typed, machine-checked process.

**Wave 4: General acyclicity.**
The current `noCyclicDependencies` checks for 2-cycles only. General acyclicity (no cycles of any length) would use a topological sort or DFS-based check. This is a natural extension.

**Wave 5: Soundness bridge.**
The full soundness theorem (`runAudit_allPassed_implies_auditPasses`) would connect each computable check to its propositional form. The tier consistency direction is proven; the remaining 7 directions require unfolding the computable check functions and matching them to the propositional predicates.

---

## Files touched

- `PfLean/AuditProtocol.lean` — NEW (created)
- `PfLean/AuditRegistry.lean` — NEW (created)

No existing files were modified. The build is additive.

---

## Conclusion

The audit is built. The certificate is machine-checked. The PF claim ledger is structurally honest — verified by the Lean kernel, not by human assertion.

The next layer is ready to be built.
