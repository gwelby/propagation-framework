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

end PfLean
