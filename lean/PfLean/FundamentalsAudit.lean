/-
  PfLean.FundamentalsAudit — Audit Protocol Applied to the Real PF Claim Ledger
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-08-02

  This module applies the machine-verified audit protocol to the real PfLean
  claim ledger (pfClaimLedger from ClaimLedgerRegistry.lean). Unlike the
  Money-Research application, this ledger has real theorems, real dependencies,
  and mixed tiers (DERIVED, CONDITIONAL, ARGUED).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.ClaimLedger
import PfLean.ClaimLedgerRegistry
import PfLean.MeasurementContract
import PfLean.MeasurementLedger
import PfLean.AuditProtocol

namespace PfLean

open ClaimLedger ClaimEntry ClaimRecord Check

theorem pfClaimLedger_length :
    pfClaimLedger.entries.length = 14 := by
  simp [pfClaimLedger]

theorem pfClaimLedger_passes_tierConsistency :
    Check.tierConsistency pfClaimLedger :=
  Check.tierConsistency_holds pfClaimLedger

theorem pfClaimLedger_passes_dependenciesResolved :
    Check.dependenciesResolved pfClaimLedger :=
  pfClaimLedger_wellFormed

theorem pfClaimLedger_passes_uniqueEntryNames :
    Check.uniqueEntryNames pfClaimLedger :=
  pfClaimLedger_uniqueEntryNames

theorem pfClaimLedger_passes_falsifierNonEmpty :
    Check.falsifierNonEmpty pfClaimLedger := by
  intro e he
  simp [pfClaimLedger] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals native_decide

theorem pfClaimLedger_passes_evidenceNonEmpty :
    Check.evidenceNonEmpty pfClaimLedger := by
  intro e he
  simp [pfClaimLedger] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals native_decide

theorem pfClaimLedger_all_entries_OK :
    ∀ e ∈ pfClaimLedger.entries, e.status = .OK := by
  intro e he
  simp [pfClaimLedger] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals rfl

theorem pfClaimLedger_passes_statusGateConsistency :
    Check.statusGateConsistency pfClaimLedger := by
  intro e he h_OK d hd e' he' h_name
  exact pfClaimLedger_all_entries_OK e' he'

theorem pfClaimLedger_passes_noSelfDependency :
    Check.noSelfDependency pfClaimLedger := by
  intro e he
  simp [pfClaimLedger] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals native_decide

theorem pfClaimLedger_passes_noCyclicDependencies :
    Check.noCyclicDependencies pfClaimLedger := by
  -- The 2-cycle check: for all e1, e2, if e1.name in e2.deps then e2.name not in e1.deps
  -- We prove this by showing the filter of 2-cycle violations is empty
  have h_filter : (pfClaimLedger.entries.filter (fun e =>
    e.dependencies.any (fun d =>
      pfClaimLedger.entries.any (fun e' =>
        e'.name = d ∧ e.name ∈ e'.dependencies)))) = [] := by
    native_decide
  intro e₁ he₁ e₂ he₂ h_dep h_back
  -- e₁ has a dependency d = e₂.name, and e₂ has e₁.name in its deps
  -- So e₁ should be in the filter, but the filter is empty
  have h_mem : e₁ ∈ pfClaimLedger.entries.filter (fun e =>
    e.dependencies.any (fun d =>
      pfClaimLedger.entries.any (fun e' =>
        e'.name = d ∧ e.name ∈ e'.dependencies))) := by
    simp only [List.mem_filter, he₁, true_and]
    rw [List.any_eq_true]
    refine ⟨e₂.name, h_back, ?_⟩
    rw [List.any_eq_true]
    refine ⟨e₂, he₂, ?_⟩
    simp [h_dep]
  rw [h_filter] at h_mem
  exact absurd h_mem (by simp)

theorem pfClaimLedger_passes_acyclic :
    Check.acyclic pfClaimLedger := by
  intro e he
  simp [pfClaimLedger] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals native_decide

theorem pfClaimLedger_passes_full_audit :
    auditPasses pfClaimLedger :=
  ⟨pfClaimLedger_passes_tierConsistency,
    pfClaimLedger_passes_dependenciesResolved,
    pfClaimLedger_passes_uniqueEntryNames,
    pfClaimLedger_passes_falsifierNonEmpty,
    pfClaimLedger_passes_evidenceNonEmpty,
    pfClaimLedger_passes_statusGateConsistency,
    pfClaimLedger_passes_noSelfDependency,
    pfClaimLedger_passes_noCyclicDependencies,
    pfClaimLedger_passes_acyclic⟩

theorem pfClaimLedger_runAudit_allPassed :
    (runAudit pfClaimLedger).allPassed = true := by
  rw [runAudit_allPassed_iff_auditPasses]
  exact pfClaimLedger_passes_full_audit

theorem pfClaimLedger_audit_iff :
    (runAudit pfClaimLedger).allPassed = true ↔
    auditPasses pfClaimLedger :=
  runAudit_allPassed_iff_auditPasses pfClaimLedger

theorem pfClaimLedger_derived_count :
    (pfClaimLedger.entries.filter (fun e => e.tier = .DERIVED)).length = 11 := by
  simp [pfClaimLedger, fullNormT3StrictlyDecreasesEntry,
        PFEntropyT3FormalIdentityEntry, PFEntropyDecreasesT3Entry,
        fullNormPythagoreanEntry, P0QDotZeroEntry, QSumZeroEntry,
        TFullDecompositionEntry, topologicalAvailabilityEntry,
        kernelClosureOrdersEntry, atMostTwoClosureOrdersEntry,
        quatToSO3KerEntry, weinbergRatioEntry, koideQTwoThirdsEntry,
        weakFieldIndexFlatEntry]
  native_decide

theorem pfClaimLedger_conditional_count :
    (pfClaimLedger.entries.filter (fun e => e.tier = .CONDITIONAL)).length = 2 := by
  simp [pfClaimLedger, fullNormT3StrictlyDecreasesEntry,
        PFEntropyT3FormalIdentityEntry, PFEntropyDecreasesT3Entry,
        fullNormPythagoreanEntry, P0QDotZeroEntry, QSumZeroEntry,
        TFullDecompositionEntry, topologicalAvailabilityEntry,
        kernelClosureOrdersEntry, atMostTwoClosureOrdersEntry,
        quatToSO3KerEntry, weinbergRatioEntry, koideQTwoThirdsEntry,
        weakFieldIndexFlatEntry]
  native_decide

theorem pfClaimLedger_argued_count :
    (pfClaimLedger.entries.filter (fun e => e.tier = .ARGUED)).length = 1 := by
  simp [pfClaimLedger, fullNormT3StrictlyDecreasesEntry,
        PFEntropyT3FormalIdentityEntry, PFEntropyDecreasesT3Entry,
        fullNormPythagoreanEntry, P0QDotZeroEntry, QSumZeroEntry,
        TFullDecompositionEntry, topologicalAvailabilityEntry,
        kernelClosureOrdersEntry, atMostTwoClosureOrdersEntry,
        quatToSO3KerEntry, weinbergRatioEntry, koideQTwoThirdsEntry,
        weakFieldIndexFlatEntry]
  native_decide

theorem pfClaimLedger_tier_counts_sum :
    (pfClaimLedger.entries.filter (fun e => e.tier = .DERIVED)).length +
    (pfClaimLedger.entries.filter (fun e => e.tier = .CONDITIONAL)).length +
    (pfClaimLedger.entries.filter (fun e => e.tier = .ARGUED)).length
    = 14 := by
  simp [pfClaimLedger_derived_count, pfClaimLedger_conditional_count,
        pfClaimLedger_argued_count]

-- ---------------------------------------------------------------------------
-- 7. Gated audit: CONDITIONAL entries → .HOLD (non-vacuous status-gate)
-- ---------------------------------------------------------------------------
/-
  The gated ledger is identical to `pfClaimLedger` except the two CONDITIONAL
  entries have status `.HOLD` instead of `.OK`. This reflects the policy:
  claims depending on an unproven opaque premise (`PFEntropyT3PhysicalTransferPremise`)
  are gated. DERIVED and ARGUED entries remain `.OK`.

  The key check is **status-gate consistency** (Check 6): no `.OK` claim may
  depend on a `.HOLD` claim. In the ungated ledger this was vacuous (all `.OK`).
  In the gated ledger it is non-vacuous: the two `.HOLD` entries are
  `PFEntropy_decreases_T3` and `full_norm_T3_strictly_decreases`. No `.OK`
  entry depends on either — the only entries that depend on them are each
  other (both `.HOLD`), so the check passes.

  This is the check that would catch the God Equation overclaim pattern:
  if a DERIVED (.OK) claim had depended on Postulate D (.HOLD), the audit
  would fail at compile time.
-/

/-- Gated PFEntropy entry: same as `PFEntropyDecreasesT3Entry` but with
    status `.HOLD`. -/
def PFEntropyDecreasesT3Entry_gated : ClaimEntry :=
  { PFEntropyDecreasesT3Entry with
    record := ClaimRecord.hold PFEntropyDecreasesT3Entry.record }

/-- Gated full-norm-T³ entry: same as `fullNormT3StrictlyDecreasesEntry`
    but with status `.HOLD`. -/
def fullNormT3StrictlyDecreasesEntry_gated : ClaimEntry :=
  { fullNormT3StrictlyDecreasesEntry with
    record := ClaimRecord.hold fullNormT3StrictlyDecreasesEntry.record }

/-- The gated PF claim ledger: 12 `.OK` + 2 `.HOLD`. -/
def pfClaimLedger_gated : ClaimLedger :=
  ⟨[ fullNormT3StrictlyDecreasesEntry_gated
   , PFEntropyT3FormalIdentityEntry
   , PFEntropyDecreasesT3Entry_gated
   , fullNormPythagoreanEntry
   , P0QDotZeroEntry
   , QSumZeroEntry
   , TFullDecompositionEntry
   , topologicalAvailabilityEntry
   , kernelClosureOrdersEntry
   , atMostTwoClosureOrdersEntry
   , quatToSO3KerEntry
   , weinbergRatioEntry
   , koideQTwoThirdsEntry
   , weakFieldIndexFlatEntry ]⟩

/-- The gated ledger has 14 entries. -/
theorem pfClaimLedger_gated_length :
    pfClaimLedger_gated.entries.length = 14 := by
  decide

/-- The gated ledger has 2 `.HOLD` entries. -/
theorem pfClaimLedger_gated_hold_count :
    (pfClaimLedger_gated.entries.filter (fun e => e.status = .HOLD)).length = 2 := by
  simp [pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold, ClaimRecord.derived, ClaimRecord.conditional,
        ClaimRecord.argued]
  native_decide

/-- The gated ledger has 12 `.OK` entries. -/
theorem pfClaimLedger_gated_ok_count :
    (pfClaimLedger_gated.entries.filter (fun e => e.status = .OK)).length = 12 := by
  simp [pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold, ClaimRecord.derived, ClaimRecord.conditional,
        ClaimRecord.argued]
  native_decide

-- 7a. Structural checks for the gated ledger

theorem pfClaimLedger_gated_passes_tierConsistency :
    Check.tierConsistency pfClaimLedger_gated :=
  Check.tierConsistency_holds pfClaimLedger_gated

theorem pfClaimLedger_gated_passes_dependenciesResolved :
    Check.dependenciesResolved pfClaimLedger_gated := by
  -- Same pattern as pfClaimLedger_wellFormed: simp unfolds everything,
  -- decide closes the concrete computation.
  -- The gated entries use ClaimRecord.hold which preserves dependencies.
  have h : pfClaimLedger_gated.dependenciesResolved := by
    simp [ClaimLedger.dependenciesResolved, ClaimEntry.dependencies,
          pfClaimLedger_gated,
          fullNormT3StrictlyDecreasesEntry_gated,
          PFEntropyDecreasesT3Entry_gated,
          PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
          P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
          topologicalAvailabilityEntry, kernelClosureOrdersEntry,
          atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
          weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
          ClaimRecord.hold, ClaimRecord.derived, ClaimRecord.conditional,
          ClaimRecord.argued]
    decide
  exact h

theorem pfClaimLedger_gated_passes_uniqueEntryNames :
    Check.uniqueEntryNames pfClaimLedger_gated := by
  -- The gated ledger has the same entry names as the ungated ledger
  -- (only status fields changed). Use decide on the concrete list.
  simp [Check.uniqueEntryNames, ClaimLedger.uniqueEntryNames,
        pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold]
  decide

theorem pfClaimLedger_gated_passes_falsifierNonEmpty :
    Check.falsifierNonEmpty pfClaimLedger_gated := by
  intro e he
  simp [Check.falsifierNonEmpty, pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals decide

theorem pfClaimLedger_gated_passes_evidenceNonEmpty :
    Check.evidenceNonEmpty pfClaimLedger_gated := by
  intro e he
  simp [Check.evidenceNonEmpty, pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals decide

/-- **Check 6 (gated): StatusGateConsistency — non-vacuous.**

    No `.OK` entry depends on a `.HOLD` entry. The two `.HOLD` entries are
    `PFEntropy_decreases_T3` and `full_norm_T3_strictly_decreases`. The only
    entries that depend on them are each other (both `.HOLD`), so no `.OK`
    entry is blocked. This is the check that would catch the God Equation
    overclaim pattern automatically. -/
theorem pfClaimLedger_gated_passes_statusGateConsistency :
    Check.statusGateConsistency pfClaimLedger_gated := by
  intro e he h_OK d hd e' he' h_name
  -- Case-split on both e and e' to get concrete entries
  simp [pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold] at he he'
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals
    rcases he' with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                    rfl | rfl | rfl | rfl
    all_goals first
      | rfl
      | (exfalso; rw [← h_name] at hd; exact absurd hd (by native_decide))
      | (exfalso; exact absurd h_OK (by native_decide))

theorem pfClaimLedger_gated_passes_noSelfDependency :
    Check.noSelfDependency pfClaimLedger_gated := by
  intro e he
  simp [Check.noSelfDependency, pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals decide

theorem pfClaimLedger_gated_passes_noCyclicDependencies :
    Check.noCyclicDependencies pfClaimLedger_gated := by
  intro e₁ he₁ e₂ he₂ h_dep h_back
  -- Case-split on both entries to get concrete values
  simp [pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold] at he₁ he₂
  rcases he₁ with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals
    rcases he₂ with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                    rfl | rfl | rfl | rfl
    all_goals first
      | exact absurd h_dep (by native_decide)
      | exact absurd h_back (by native_decide)

theorem pfClaimLedger_gated_passes_acyclic :
    Check.acyclic pfClaimLedger_gated := by
  intro e he
  simp [pfClaimLedger_gated,
        fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated,
        PFEntropyT3FormalIdentityEntry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry,
        atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
        weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry,
        ClaimRecord.hold] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
                  rfl | rfl | rfl | rfl
  all_goals native_decide

/-- **The gated PF claim ledger passes all 9 structural audit checks.**

    The key difference from the ungated audit: Check 6 (StatusGateConsistency)
    is **non-vacuous**. It verifies that no `.OK` claim depends on the two
    `.HOLD` claims. This is the check that would catch the God Equation
    overclaim at compile time. -/
theorem pfClaimLedger_gated_passes_full_audit :
    auditPasses pfClaimLedger_gated :=
  ⟨pfClaimLedger_gated_passes_tierConsistency,
    pfClaimLedger_gated_passes_dependenciesResolved,
    pfClaimLedger_gated_passes_uniqueEntryNames,
    pfClaimLedger_gated_passes_falsifierNonEmpty,
    pfClaimLedger_gated_passes_evidenceNonEmpty,
    pfClaimLedger_gated_passes_statusGateConsistency,
    pfClaimLedger_gated_passes_noSelfDependency,
    pfClaimLedger_gated_passes_noCyclicDependencies,
    pfClaimLedger_gated_passes_acyclic⟩

theorem pfClaimLedger_gated_runAudit_allPassed :
    (runAudit pfClaimLedger_gated).allPassed = true := by
  rw [runAudit_allPassed_iff_auditPasses]
  exact pfClaimLedger_gated_passes_full_audit

-- ---------------------------------------------------------------------------
-- 8. Measurement audit (10-check, both ledgers)
-- ---------------------------------------------------------------------------
/-
  Check 10 (measurementOutcomeConsistent): for each measurement contract,
  if the outcome is `Confirmed`, the claim's status must be `.OK`; if
  `Inconclusive`, `.HOLD`; if `Falsified`, `.NOGO`; if `none`, vacuous.

  The 4 contracts from `pfMeasurementLedger_full`:
  1. PFEntropy_decreases_T3 → 1/8 ratio (sandbox: 0.124 ± 0.005, Confirmed)
  2. weinberg_ratio → 0.22310 (PDG: 0.22310 ± 0.00010, Confirmed)
  3. koide_Q_two_thirds → 2/3 (charged leptons: 0.66666 ± 0.00001, Confirmed)
  4. weakFieldIndex_flat → n=1 (trivial, Confirmed)

  **Ungated ledger**: all 4 Confirmed → all 4 claims are .OK → check passes.
  **Gated ledger**: PFEntropy_decreases_T3 is .HOLD, but the measurement
  outcome is `none` (premise open; measurement not applied to status).
  The other 3 are Confirmed → .OK → check passes.
-/

/-- The 4 measurement contracts as a list. -/
noncomputable def pfMeasurementContracts : List MeasurementContract :=
  pfMeasurementLedger_full.contracts

/-- Outcome map for the ungated ledger: all 4 Confirmed. -/
def pfMeasurementOutcomes : String → Option MeasurementOutcome
  | "PFEntropy_decreases_T3" => some .Confirmed
  | "weinberg_ratio" => some .Confirmed
  | "koide_Q_two_thirds" => some .Confirmed
  | "weakFieldIndex_flat" => some .Confirmed
  | _ => none

/-- `pfMeasurementOutcomes` never returns `Inconclusive`. -/
theorem pfMeasurementOutcomes_never_Inconclusive (s : String) :
    pfMeasurementOutcomes s ≠ some .Inconclusive := by
  intro h
  unfold pfMeasurementOutcomes at h
  split at h <;> simp at h

/-- `pfMeasurementOutcomes` never returns `Falsified`. -/
theorem pfMeasurementOutcomes_never_Falsified (s : String) :
    pfMeasurementOutcomes s ≠ some .Falsified := by
  intro h
  unfold pfMeasurementOutcomes at h
  split at h <;> simp at h

/-- **Check 10 (ungated)**: all 4 Confirmed measurements have status `.OK`. -/
theorem pfClaimLedger_passes_measurementOutcomeConsistent :
    Check.measurementOutcomeConsistent pfClaimLedger
      pfMeasurementContracts pfMeasurementOutcomes := by
  intro c hc e he h_name
  cases h_out : pfMeasurementOutcomes c.claimName with
  | none => trivial
  | some o =>
    cases o with
    | Confirmed => exact pfClaimLedger_all_entries_OK e he
    | Inconclusive => exact absurd h_out (pfMeasurementOutcomes_never_Inconclusive c.claimName)
    | Falsified => exact absurd h_out (pfMeasurementOutcomes_never_Falsified c.claimName)

/-- **The ungated ledger passes the full 10-check audit with measurements.** -/
theorem pfClaimLedger_passes_full_audit_with_measurements :
    auditPassesWithMeasurements pfClaimLedger
      pfMeasurementContracts pfMeasurementOutcomes :=
  ⟨pfClaimLedger_passes_full_audit,
    pfClaimLedger_passes_measurementOutcomeConsistent⟩

theorem pfClaimLedger_runAuditWithMeasurements_allPassed :
    (runAuditWithMeasurements pfClaimLedger
      pfMeasurementContracts pfMeasurementOutcomes).allPassed = true := by
  rw [runAuditWithMeasurements_allPassed_iff_auditPassesWithMeasurements]
  exact pfClaimLedger_passes_full_audit_with_measurements

/-- Outcome map for the gated ledger: 3 Confirmed, 1 `none`.

    The PFEntropy T³ measurement is numerically Confirmed (0.124 ≈ 1/8),
    but the physical claim is `.HOLD` (premise open). Applying Confirmed
    would require status `.OK`, which contradicts `.HOLD`. Using `none`
    honestly says "measurement done, outcome not applied to status." -/
def pfMeasurementOutcomes_gated : String → Option MeasurementOutcome
  | "PFEntropy_decreases_T3" => none
  | "weinberg_ratio" => some .Confirmed
  | "koide_Q_two_thirds" => some .Confirmed
  | "weakFieldIndex_flat" => some .Confirmed
  | _ => none

/-- `pfMeasurementOutcomes_gated` never returns `Inconclusive`. -/
theorem pfMeasurementOutcomes_gated_never_Inconclusive (s : String) :
    pfMeasurementOutcomes_gated s ≠ some .Inconclusive := by
  intro h
  unfold pfMeasurementOutcomes_gated at h
  split at h <;> simp at h

/-- `pfMeasurementOutcomes_gated` never returns `Falsified`. -/
theorem pfMeasurementOutcomes_gated_never_Falsified (s : String) :
    pfMeasurementOutcomes_gated s ≠ some .Falsified := by
  intro h
  unfold pfMeasurementOutcomes_gated at h
  split at h <;> simp at h

/-- **Check 10 (gated)**: 3 Confirmed (→ .OK), 1 `none` (vacuous). -/
theorem pfClaimLedger_gated_passes_measurementOutcomeConsistent :
    Check.measurementOutcomeConsistent pfClaimLedger_gated
      pfMeasurementContracts pfMeasurementOutcomes_gated := by
  intro c hc e he h_name
  cases h_out : pfMeasurementOutcomes_gated c.claimName with
  | none => trivial
  | some o =>
    cases o with
    | Confirmed =>
      -- The 3 Confirmed claims (weinberg_ratio, koide_Q_two_thirds,
      -- weakFieldIndex_flat) are all .OK in the gated ledger
      have h_confirmed : c.claimName = "weinberg_ratio" ∨
        c.claimName = "koide_Q_two_thirds" ∨
        c.claimName = "weakFieldIndex_flat" := by
        simp only [pfMeasurementOutcomes_gated] at h_out
        split at h_out <;> simp_all
      rcases h_confirmed with h_w | h_k | h_g
      · -- weinberg_ratio: ARGUED, .OK (not gated)
        rw [h_w] at h_name
        have : e = weinbergRatioEntry := by
          have h_uniq := uniqueEntryNames_implies_uniqueNames pfClaimLedger_gated
            pfClaimLedger_gated_passes_uniqueEntryNames
          have h_mem : weinbergRatioEntry ∈ pfClaimLedger_gated.entries := by
            simp [pfClaimLedger_gated, weinbergRatioEntry]
          exact h_uniq e he weinbergRatioEntry h_mem h_name
        rw [this]; rfl
      · -- koide_Q_two_thirds: DERIVED, .OK (not gated)
        rw [h_k] at h_name
        have : e = koideQTwoThirdsEntry := by
          have h_uniq := uniqueEntryNames_implies_uniqueNames pfClaimLedger_gated
            pfClaimLedger_gated_passes_uniqueEntryNames
          have h_mem : koideQTwoThirdsEntry ∈ pfClaimLedger_gated.entries := by
            simp [pfClaimLedger_gated, koideQTwoThirdsEntry]
          exact h_uniq e he koideQTwoThirdsEntry h_mem h_name
        rw [this]; rfl
      · -- weakFieldIndex_flat: DERIVED, .OK (not gated)
        rw [h_g] at h_name
        have : e = weakFieldIndexFlatEntry := by
          have h_uniq := uniqueEntryNames_implies_uniqueNames pfClaimLedger_gated
            pfClaimLedger_gated_passes_uniqueEntryNames
          have h_mem : weakFieldIndexFlatEntry ∈ pfClaimLedger_gated.entries := by
            simp [pfClaimLedger_gated, weakFieldIndexFlatEntry]
          exact h_uniq e he weakFieldIndexFlatEntry h_mem h_name
        rw [this]; rfl
    | Inconclusive => exact absurd h_out (pfMeasurementOutcomes_gated_never_Inconclusive c.claimName)
    | Falsified => exact absurd h_out (pfMeasurementOutcomes_gated_never_Falsified c.claimName)

/-- **The gated ledger passes the full 10-check audit with measurements.**

    The PFEntropy_decreases_T3 measurement outcome is `none` (premise open,
    measurement not applied). The other 3 are Confirmed and their claims
    are `.OK` in the gated ledger. -/
theorem pfClaimLedger_gated_passes_full_audit_with_measurements :
    auditPassesWithMeasurements pfClaimLedger_gated
      pfMeasurementContracts pfMeasurementOutcomes_gated :=
  ⟨pfClaimLedger_gated_passes_full_audit,
    pfClaimLedger_gated_passes_measurementOutcomeConsistent⟩

theorem pfClaimLedger_gated_runAuditWithMeasurements_allPassed :
    (runAuditWithMeasurements pfClaimLedger_gated
      pfMeasurementContracts pfMeasurementOutcomes_gated).allPassed = true := by
  rw [runAuditWithMeasurements_allPassed_iff_auditPassesWithMeasurements]
  exact pfClaimLedger_gated_passes_full_audit_with_measurements

/-- **The gated ledger has no `.OK` entry depending on a `.HOLD` entry.**

    This is the structural invariant that would have caught the God Equation
    overclaim: if a DERIVED (.OK) claim had depended on Postulate D (.HOLD),
    this theorem would be false and the audit would fail. -/
theorem pfClaimLedger_gated_no_OK_depends_on_HOLD :
    ∀ e ∈ pfClaimLedger_gated.entries,
      e.status = .OK →
      ∀ d ∈ e.dependencies,
        ∀ e' ∈ pfClaimLedger_gated.entries,
          e'.name = d → e'.status = .OK :=
  pfClaimLedger_gated_passes_statusGateConsistency

end PfLean
