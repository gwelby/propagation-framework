# Audit Protocol Handoff — Apply to PfLean MeasurementLedger

**From:** Devin (Money-Research workspace, audit protocol builder)
**To:** Devin (Fundamentals workspace)
**Date:** 2026-08-02
**Status:** Framework complete and committed (`51e49d1`), ready for real application

---

## What I Built

A machine-verified audit protocol in `PfLean/AuditProtocol.lean` that checks
claim ledgers for structural integrity. It has two iff bridges proven in the
Lean kernel:

```
(runAudit cl).allPassed = true ↔ auditPasses cl                    (9-check)
(runAuditWithMeasurements cl contracts outcomes).allPassed = true
  ↔ auditPassesWithMeasurements cl contracts outcomes              (10-check)
```

Both directions (soundness + completeness) are proven. 9 negative fixtures
verify the audit catches violations. `lake build` is green (16534 jobs, 0 errors).

**The framework is real. The first application (Money-Research) was trivial.**
The Money-Research ledger has `P := True` for all entries, empty dependencies,
and all-OK status — so most checks pass vacuously. The framework needs a ledger
with real structure to be meaningful.

**Your MeasurementLedger has that structure.** Real math, real dependencies,
real tier distinctions, real measurement outcomes. That's where this matters.

---

## Why You Should Do This (Not Me)

The hard part isn't the Lean — I can do that. The hard part is the **physics
dependency graph and tier assignments**. Getting those right requires knowing:

- Does ThreeGenerations depend on KoideGeometry, or just reference it?
- Is TopologicalWeights DERIVED or ARGUED? (Codex demotion audit changed language)
- Which claims depend on Postulate D (the unproven premise)?
- What are the real measurement contracts and outcomes?

If I guess wrong on the dependency graph, the audit passes but didn't check
what matters. That's worse than no audit. You know the physics. I don't.

---

## The 10 Checks (What the Audit Verifies)

| # | Check | What it catches | Prop predicate |
|---|-------|-----------------|----------------|
| 1 | Tier consistency | Confidence outside tier range | `Check.tierConsistency` |
| 2 | Dependencies resolved | Dependency on non-existent entry | `Check.dependenciesResolved` |
| 3 | Unique entry names | Duplicate claim IDs | `Check.uniqueEntryNames` |
| 4 | Falsifier non-empty | Claim with no falsifier (unfalsifiable) | `Check.falsifierNonEmpty` |
| 5 | Evidence non-empty | Claim with no evidence string | `Check.evidenceNonEmpty` |
| 6 | Status gate consistency | OK claim depending on HOLD/NOGO claim | `Check.statusGateConsistency` |
| 7 | No self-dependency | Claim depending on itself | `Check.noSelfDependency` |
| 8 | No 2-cycles | A↔B mutual dependency | `Check.noCyclicDependencies` |
| 9 | Acyclic | Any-length cycle (A→B→C→A) | `Check.acyclic` |
| 10 | Measurement outcome consistent | Falsified measurement but status still OK | `Check.measurementOutcomeConsistent` |

**Check 6 is the one that would have caught the God Equation overclaim
automatically.** When "seven approaches converged" was DERIVED (OK) but
Postulate D was an unproven premise (should be HOLD), that's a status-gate
violation. The Codex audit found that manually in June. This check finds it
at compile time.

---

## The API (How to Use It)

### Data structures

```lean
-- A single claim entry
ClaimEntry.mk (name : String) (P : Prop) (record : ClaimRecord)

-- The record holds the metadata
ClaimRecord.mk (proof : P) (tier : EpistemicTier) (status : ClaimStatus)
  (confidence : Confidence) (evidence : String) (falsifier : String)
  (dependencies : List String) (tier_bound : proof tier confidence)

-- EpistemicTier: .EMPIRICAL | .ARGUED | .INTUITION | .OPEN | .DERIVED
-- ClaimStatus:  .OK | .HOLD | .NOGO

-- A ledger is just a list of entries
ClaimLedger := ⟨ List ClaimEntry ⟩

-- Measurement contracts (for check 10)
MeasurementContract := { claimName : String, predictedValue : ℝ,
  tolerance : ℝ, falsificationThreshold : ℝ, ... }

-- Measurement outcomes
MeasurementOutcome := .Confirmed | .Inconclusive | .Falsified
-- expectedStatus: Confirmed → OK, Inconclusive → HOLD, Falsified → NOGO
```

### Running the audit

```lean
-- Propositional: does the ledger pass? (9 checks)
auditPasses cl : Prop

-- Computable: run the audit function (9 checks)
runAudit cl : AuditResult
(runAudit cl).allPassed : Bool

-- With measurements (10 checks)
auditPassesWithMeasurements cl contracts outcomes : Prop
runAuditWithMeasurements cl contracts outcomes : AuditResult

-- The iff bridges (already proven)
runAudit_allPassed_iff_auditPasses cl
runAuditWithMeasurements_allPassed_iff_auditPassesWithMeasurements cl contracts outcomes
```

### Helper constructors

```lean
-- In MoneyResearchAudit.lean, I defined helpers for each tier:
def mrEmpirical (id text source falsifier : String) : ClaimEntry
def mrArgued (id text source falsifier : String) : ClaimEntry
-- etc.

-- You'll want similar helpers for your tiers:
def pfDerived (id : String) (P : Prop) (h : P)
    (evidence falsifier : String) (deps : List String) : ClaimEntry
def pfArgued (id : String) (P : Prop) (h : P)
    (evidence falsifier : String) (deps : List String) : ClaimEntry
```

---

## Step-by-Step Plan

### Step 1: Read your existing MeasurementLedger

Read `PfLean/MeasurementLedger.lean` and `PfLean/ClaimLedgerRegistry.lean`.
Identify:
- Which entries are actual theorems (have real `P : Prop` with a proof)
- What tier each entry is (DERIVED, ARGUED, CONDITIONAL, etc.)
- What status each should have (OK, HOLD, NOGO)
- What the real dependencies are

### Step 2: Build the ClaimLedger

Create `PfLean/FundamentalsAudit.lean` with:
- One `ClaimEntry` per measurement ledger entry
- Use the REAL `P : Prop` from each theorem (not `True`)
- Set `dependencies` to the actual conceptual dependencies
- Set `status` based on current claim status (DERIVED→OK, ARGUED→OK or HOLD, CONDITIONAL→HOLD, demoted→NOGO)
- Set `falsifier` to a meaningful falsification condition

### Step 3: Prove the propositional audit

For each of the 9 checks, prove `Check.X fundamentalsLedger`:
- Tier consistency: usually `Check.tierConsistency_holds` (automatic)
- Dependencies resolved: prove each dep resolves to an entry
- Unique names: `native_decide` if the list is concrete
- Falsifier/evidence non-empty: `native_decide` per entry
- Status gate: prove no OK claim depends on a non-OK claim
- No self-dep: prove no entry lists itself
- No 2-cycles: prove no A↔B pairs
- Acyclic: `native_decide` if the graph is concrete and small

### Step 4: Apply the iff bridge

```lean
theorem fundamentals_runAudit_allPassed :
    (runAudit fundamentalsLedger).allPassed = true := by
  rw [runAudit_allPassed_iff_auditPasses]
  exact fundamentals_passes_full_audit
```

### Step 5: Add measurement contracts (optional but high-value)

For claims with numerical predictions (Weinberg angle, Koide Q=2/3, etc.):
- Define `MeasurementContract` with predicted value and tolerance
- Define outcomes map: `falsifiedOutcomes : String → Option MeasurementOutcome`
- Prove `Check.measurementOutcomeConsistent`
- Apply the 10-check iff bridge

### Step 6: Wire into build

Add `import PfLean.FundamentalsAudit` to `PfLean.lean` so the build checks it.

---

## Proof Patterns That Work (and Gotchas I Hit)

### Pattern 1: Filter-based checks (checks 3, 6, 7, 8, 9)

The `runX` functions use `have violations := List.filter ...; if violations.isEmpty then`.

**Problem:** `split` can't see through the `have` binding. `rw` fails on the `if`.

**Solution:** Prove the condition as a separate `have`, then `simp only [h_cond, if_true]`:

```lean
have h_filter : (cl.entries.filter (fun e => e.name ∈ e.dependencies)) = [] := by
  rw [List.filter_eq_nil_iff]
  intro e he
  rw [decide_eq_true_iff]
  intro h_self
  exact absurd h_self (h e he)
have h_cond : (cl.entries.filter ...).isEmpty = true := by
  rw [h_filter]; rfl
simp only [h_cond, if_true, CheckResult.passed]
```

### Pattern 2: All-based checks (checks 2, 4, 5)

```lean
have h_cond : cl.entries.all (fun e => e.falsifier ≠ "") = true := by
  rw [List.all_eq_true]
  intro e he
  exact decide_eq_true_iff.mpr (h e he)
simp only [h_cond, if_true, CheckResult.passed]
```

### Pattern 3: Nodup (check 3)

`Check.uniqueEntryNames` is a `Prop` (`Nodup`), not a `Bool`. The `runX` uses
`if (map name).Nodup then`. For completeness:

```lean
unfold runUniqueEntryNames
split
· simp [CheckResult.passed]  -- true branch
· exact absurd h ‹¬(map name).Nodup›  -- false branch contradicts h
```

For soundness, the false branch needs `if_neg`:
```lean
simp only [runUniqueEntryNames, h_cond, if_neg, CheckResult.passed] at h
```

### Pattern 4: Measurement outcome match reduction

The `runMeasurementOutcomeConsistent` has a `match` on `outcomes c.claimName`
inside the filter. After `cases h_out : outcomes c.claimName with | some o =>`,
the goal still has the match. Fix: `simp only [h_out]` to reduce the match,
then `by_contra` + `List.any_eq_true` to extract the violation.

### Pattern 5: native_decide for concrete lists

For `Nodup` and `hasCycleThrough` on concrete ledgers, `native_decide` works
when `decide` fails (decidability synthesis issues). Use it for:
- `Check.uniqueEntryNames` on a concrete ledger
- `Check.acyclic` on a concrete ledger with small graph
- `¬Nodup ["dup_test", "dup_test"]` in negative fixtures

### Gotcha: List.isEmpty_eq_true_iff does NOT exist

I wasted time on this. The lemma is `List.isEmpty_eq_false_iff` (for the
non-empty direction). For the empty direction, use `List.filter_eq_nil_iff`
to prove the filter is `[]`, then `rfl` for `isEmpty = true`.

### Gotcha: unfold on dot notation

`unfold Check.uniqueEntryNames at h` may produce `dupNamesLedger.uniqueEntryNames`
(dot notation) instead of the expanded form. Use `simp only [Check.uniqueEntryNames]`
or `have h_nodup : (cl.entries.map ClaimEntry.name).Nodup := h` (definitional
equality) instead.

---

## What the Physics-Critical Decisions Are

These are the decisions I can't make for you. Getting them wrong makes the
audit useless (passes when it shouldn't, or fails for wrong reasons).

### 1. Dependency graph

For each entry, what are its REAL conceptual dependencies?

Examples I'd guess but am not sure about:
- `ThreeGenerations` depends on `KoideGeometry`? Or just uses the same convention?
- `TopologicalWeights` depends on `SO3DoubleCover`?
- `Z3FromBareMedium` depends on `Entropy`? Or independent?
- Everything in `Axioms.lean` depends on which hypotheses?

**Wrong guess = false confidence.** If you mark a real dependency as empty,
the cycle check passes vacuously but didn't check the actual conceptual structure.

### 2. Status assignments

Map current claim status to `ClaimStatus`:
- DERIVED 0.95 → `.OK`
- ARGUED 0.65 → `.OK` or `.HOLD`? (It's argued, not proven — is that OK?)
- CONDITIONAL 0.88 → `.HOLD` (depends on an explicit premise)
- Demoted claims → `.NOGO`
- PUBLIC HOLD → `.HOLD`

**The key question:** should ARGUED claims be `.OK` or `.HOLD`? If ARGUED is
`.OK`, then an ARGUED claim can be depended on by other OK claims. If it's
`.HOLD`, the status-gate check catches any DERIVED claim that quietly depends
on an ARGUED one. This is a policy decision, not a math decision.

### 3. Measurement contracts

Which claims have actual numerical predictions?
- Weinberg angle: predicted value vs measured 0.2312 — Confirmed? Inconclusive?
- Koide Q=2/3: exact identity — Confirmed?
- Gravity optics n(Φ): predicted vs measured — Confirmed?
- God Equation eigenvalues: conditional on Postulate D — Inconclusive? Falsified?

---

## Where Everything Lives

```
/mnt/d/Fundamentals/lean/
├── PfLean/
│   ├── AuditProtocol.lean       # The framework (10 checks, iff bridges, fixtures)
│   ├── AuditRegistry.lean       # Audit check registry
│   ├── ClaimLedger.lean         # ClaimEntry, ClaimRecord, ClaimLedger definitions
│   ├── ClaimLedgerRegistry.lean # The PfLean measurement ledger entries
│   ├── MeasurementLedger.lean   # Measurement contracts and outcomes
│   ├── MoneyResearchAudit.lean  # Example application (trivial — 26 True claims)
│   └── FundamentalsAudit.lean   # ← YOU CREATE THIS (the real application)
├── WAVE_REPORT_AUDIT_001.md     # Wave 1: data structures
├── WAVE_REPORT_AUDIT_002.md     # Wave 2: audit protocol
├── WAVE_REPORT_AUDIT_003.md     # Wave 3: Money-Research port
├── WAVE_REPORT_AUDIT_005.md     # Wave 5: soundness
├── WAVE_REPORT_AUDIT_006.md     # Wave 6: completeness
└── WAVE_REPORT_AUDIT_007_008_009.md  # Wave 7+8+9: fixtures, measurement, integration
```

---

## If the Audit FAILS

That's the point. If `fundamentals_runAudit_allPassed` doesn't compile, it
means there's a structural problem in the claim ledger. The error message
will tell you which check failed. Common failures:

- **Status gate failure:** an OK (DERIVED) claim depends on a HOLD (CONDITIONAL)
  claim. This is the God Equation pattern. Fix: either downgrade the dependent
  claim to HOLD, or upgrade the dependency to OK (if it's actually proven).
- **Cyclic dependency:** A→B→A. This means two claims depend on each other
  circularly. Fix: break the cycle by removing one dependency.
- **Unresolved dependency:** a claim depends on a name that doesn't exist in
  the ledger. Fix: add the missing entry or remove the dependency.

**Do NOT silence a failing audit by weakening the checks.** The checks are
the value. If the audit fails, the ledger has a real problem.

---

## Contact

I'm in the Money-Research workspace. If you hit Lean issues with the audit
framework (not physics issues), the patterns above should cover it. If you
find a framework bug or need a new check type, the audit protocol is in
`PfLean/AuditProtocol.lean` — it's ~1600 lines, well-commented, and the
proof techniques are documented in the wave reports.

The framework is committed at `51e49d1`. Build is green. Good luck.
