/-
  PfLean.MeasurementLedgerAudit — Audit Protocol Applied to the Measurement Ledger
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-08-02

  This module applies the machine-verified audit protocol to the PfLean
  measurement ledger (`pfMeasurementLedger` and `pfMeasurementLedger_full`
  from `MeasurementLedger.lean`).

  The measurement ledger has three structural checks that are distinct from
  the claim-ledger checks:

  1. **contractsResolved** — every contract's `claimName` names an existing
     entry in `pfClaimLedger`.  This is the one-to-one binding between
     measurement contracts and formal claims.
  2. **uniqueContractNames** — no two positions in the contract list share
     the same `claimName` (occurrence-level uniqueness, `Nodup`).
  3. **measurementOutcomeConsistent** (AuditProtocol Check 9) — for every
     contract with a known outcome, the corresponding claim's status matches
     the expected status: `Confirmed → OK`, `Inconclusive → HOLD`,
     `Falsified → NOGO`.

  Together with the 9 claim-ledger checks (proven in `FundamentalsAudit.lean`),
  these form the complete 10-check audit certificate
  `auditPassesWithMeasurements`.

  This module proves all three measurement-ledger checks for both the minimal
  ledger (`pfMeasurementLedger`, 1 contract) and the full ledger
  (`pfMeasurementLedger_full`, 4 contracts), and combines them with the
  claim-ledger audit to produce the full 10-check certificate.

  **Result: 0 violations found. All checks PASS for both the ungated and
  gated configurations.**
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.ClaimLedger
import PfLean.ClaimLedgerRegistry
import PfLean.MeasurementContract
import PfLean.MeasurementLedger
import PfLean.AuditProtocol
import PfLean.FundamentalsAudit

namespace PfLean

open ClaimLedger ClaimEntry ClaimRecord Check MeasurementLedger

-- ---------------------------------------------------------------------------
-- 1. Measurement-ledger audit predicate
-- ---------------------------------------------------------------------------

/-- A measurement ledger passes its structural audit when:
    1. Every contract's `claimName` resolves to an entry in the claim ledger.
    2. Contract claim names are occurrence-unique (no duplicate positions).
    3. Measurement outcomes are consistent with claim statuses.

    This is the measurement-ledger analog of `auditPasses` for claim ledgers.
    It does NOT duplicate the 9 claim-ledger checks; those are in
    `auditPasses`.  The full 10-check certificate is
    `auditPassesWithMeasurements`. -/
def measurementLedgerAuditPasses (ml : MeasurementLedger)
    (cl : ClaimLedger)
    (outcomes : String → Option MeasurementOutcome) : Prop :=
  ml.contractsResolved cl ∧
  ml.uniqueContractNames ∧
  Check.measurementOutcomeConsistent cl ml.contracts outcomes

-- ---------------------------------------------------------------------------
-- 2. Minimal ledger audit (pfMeasurementLedger — 1 contract)
-- ---------------------------------------------------------------------------

/-- Outcome map for the minimal ledger: PFEntropy_decreases_T3 → Confirmed.

    The sandbox measurement (0.124 ± 0.005) confirms the 1/8 ratio prediction.
    The claim `PFEntropy_decreases_T3` is `.OK` in `pfClaimLedger` (ungated),
    so `Confirmed → OK` is consistent. -/
def pfMeasurementOutcomes_minimal : String → Option MeasurementOutcome
  | "PFEntropy_decreases_T3" => some .Confirmed
  | _ => none

/-- `pfMeasurementOutcomes_minimal` never returns `Inconclusive`. -/
theorem pfMeasurementOutcomes_minimal_never_Inconclusive (s : String) :
    pfMeasurementOutcomes_minimal s ≠ some .Inconclusive := by
  intro h
  unfold pfMeasurementOutcomes_minimal at h
  split at h <;> simp at h

/-- `pfMeasurementOutcomes_minimal` never returns `Falsified`. -/
theorem pfMeasurementOutcomes_minimal_never_Falsified (s : String) :
    pfMeasurementOutcomes_minimal s ≠ some .Falsified := by
  intro h
  unfold pfMeasurementOutcomes_minimal at h
  split at h <;> simp at h

/-- The minimal ledger's single contract is `PFEntropy_T3_contract`. -/
theorem pfMeasurementLedger_contracts_eq :
    pfMeasurementLedger.contracts = [PFEntropy_T3_contract] := by
  rw [pfMeasurementLedger, MeasurementLedger.add, MeasurementLedger.empty]

/-- **Check 1 (minimal)**: The minimal ledger resolves against `pfClaimLedger`.
    Reuses `pfMeasurementLedger_resolved` from `MeasurementLedger.lean`. -/
theorem pfMeasurementLedger_passes_contractsResolved :
    pfMeasurementLedger.contractsResolved pfClaimLedger :=
  pfMeasurementLedger_resolved

/-- **Check 2 (minimal)**: The minimal ledger has unique contract names.
    Reuses `pfMeasurementLedger_unique_contract_names` from `MeasurementLedger.lean`. -/
theorem pfMeasurementLedger_passes_uniqueContractNames :
    pfMeasurementLedger.uniqueContractNames :=
  pfMeasurementLedger_unique_contract_names

/-- **Check 3 (minimal)**: Measurement outcomes are consistent with claim
    statuses.  The single contract (`PFEntropy_decreases_T3`) has outcome
    `Confirmed`, and the corresponding claim is `.OK` in `pfClaimLedger`. -/
theorem pfMeasurementLedger_passes_measurementOutcomeConsistent :
    Check.measurementOutcomeConsistent pfClaimLedger
      pfMeasurementLedger.contracts pfMeasurementOutcomes_minimal := by
  intro c hc e he h_name
  -- Unfold the minimal ledger's contract list to get the single contract
  rw [pfMeasurementLedger_contracts_eq] at hc
  simp only [List.mem_singleton] at hc
  -- c = PFEntropy_T3_contract, so c.claimName = "PFEntropy_decreases_T3"
  rw [hc]
  -- Case-split on the outcome map (same expression as in the goal)
  cases h_out : pfMeasurementOutcomes_minimal PFEntropy_T3_contract.claimName with
  | none => trivial
  | some o =>
    cases o with
    | Confirmed =>
      -- The outcome is Confirmed → claim must be .OK
      -- All entries in pfClaimLedger are .OK (from FundamentalsAudit)
      exact pfClaimLedger_all_entries_OK e he
    | Inconclusive =>
      exact absurd h_out (pfMeasurementOutcomes_minimal_never_Inconclusive PFEntropy_T3_contract.claimName)
    | Falsified =>
      exact absurd h_out (pfMeasurementOutcomes_minimal_never_Falsified PFEntropy_T3_contract.claimName)

/-- **The minimal measurement ledger passes all 3 structural checks.** -/
theorem pfMeasurementLedger_passes_measurementLedgerAudit :
    measurementLedgerAuditPasses pfMeasurementLedger pfClaimLedger
      pfMeasurementOutcomes_minimal :=
  ⟨pfMeasurementLedger_passes_contractsResolved,
    pfMeasurementLedger_passes_uniqueContractNames,
    pfMeasurementLedger_passes_measurementOutcomeConsistent⟩

-- ---------------------------------------------------------------------------
-- 3. Full ledger audit (pfMeasurementLedger_full — 4 contracts)
-- ---------------------------------------------------------------------------

/-- The full ledger's 4 contracts as an explicit list. -/
theorem pfMeasurementLedger_full_contracts_eq :
    pfMeasurementLedger_full.contracts =
      [GravityOptics_contract, Koide_contract, Weinberg_contract, PFEntropy_T3_contract] := by
  rw [pfMeasurementLedger_full, MeasurementLedger.add, MeasurementLedger.add,
      MeasurementLedger.add, MeasurementLedger.add, MeasurementLedger.empty]

/-- **Check 1 (full)**: The full ledger resolves against `pfClaimLedger`.
    Reuses `pfMeasurementLedger_full_resolved` from `MeasurementLedger.lean`. -/
theorem pfMeasurementLedger_full_passes_contractsResolved :
    pfMeasurementLedger_full.contractsResolved pfClaimLedger :=
  pfMeasurementLedger_full_resolved

/-- **Check 2 (full)**: The full ledger has unique contract names.
    Reuses `pfMeasurementLedger_full_unique_contract_names` from `MeasurementLedger.lean`. -/
theorem pfMeasurementLedger_full_passes_uniqueContractNames :
    pfMeasurementLedger_full.uniqueContractNames :=
  pfMeasurementLedger_full_unique_contract_names

/-- **Check 3 (full)**: All 4 Confirmed measurements have status `.OK`.

    The 4 contracts are `GravityOptics_contract`, `Koide_contract`,
    `Weinberg_contract`, `PFEntropy_T3_contract`.  All 4 have outcome
    `Confirmed` (via `pfMeasurementOutcomes` from `FundamentalsAudit.lean`),
    and all 4 corresponding claims are `.OK` in `pfClaimLedger` (ungated). -/
theorem pfMeasurementLedger_full_passes_measurementOutcomeConsistent :
    Check.measurementOutcomeConsistent pfClaimLedger
      pfMeasurementLedger_full.contracts pfMeasurementOutcomes := by
  intro c hc e he h_name
  -- Unfold the full ledger's contract list
  rw [pfMeasurementLedger_full_contracts_eq] at hc
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
  -- Case-split on the 4 contracts
  rcases hc with rfl | rfl | rfl | rfl
  · -- GravityOptics_contract: claimName = "weakFieldIndex_flat"
    cases h_out : pfMeasurementOutcomes GravityOptics_contract.claimName with
    | none => trivial
    | some o =>
      cases o with
      | Confirmed => exact pfClaimLedger_all_entries_OK e he
      | Inconclusive => exact absurd h_out (pfMeasurementOutcomes_never_Inconclusive GravityOptics_contract.claimName)
      | Falsified => exact absurd h_out (pfMeasurementOutcomes_never_Falsified GravityOptics_contract.claimName)
  · -- Koide_contract: claimName = "koide_Q_two_thirds"
    cases h_out : pfMeasurementOutcomes Koide_contract.claimName with
    | none => trivial
    | some o =>
      cases o with
      | Confirmed => exact pfClaimLedger_all_entries_OK e he
      | Inconclusive => exact absurd h_out (pfMeasurementOutcomes_never_Inconclusive Koide_contract.claimName)
      | Falsified => exact absurd h_out (pfMeasurementOutcomes_never_Falsified Koide_contract.claimName)
  · -- Weinberg_contract: claimName = "weinberg_ratio"
    cases h_out : pfMeasurementOutcomes Weinberg_contract.claimName with
    | none => trivial
    | some o =>
      cases o with
      | Confirmed => exact pfClaimLedger_all_entries_OK e he
      | Inconclusive => exact absurd h_out (pfMeasurementOutcomes_never_Inconclusive Weinberg_contract.claimName)
      | Falsified => exact absurd h_out (pfMeasurementOutcomes_never_Falsified Weinberg_contract.claimName)
  · -- PFEntropy_T3_contract: claimName = "PFEntropy_decreases_T3"
    cases h_out : pfMeasurementOutcomes PFEntropy_T3_contract.claimName with
    | none => trivial
    | some o =>
      cases o with
      | Confirmed => exact pfClaimLedger_all_entries_OK e he
      | Inconclusive => exact absurd h_out (pfMeasurementOutcomes_never_Inconclusive PFEntropy_T3_contract.claimName)
      | Falsified => exact absurd h_out (pfMeasurementOutcomes_never_Falsified PFEntropy_T3_contract.claimName)

/-- **The full measurement ledger passes all 3 structural checks.** -/
theorem pfMeasurementLedger_full_passes_measurementLedgerAudit :
    measurementLedgerAuditPasses pfMeasurementLedger_full pfClaimLedger
      pfMeasurementOutcomes :=
  ⟨pfMeasurementLedger_full_passes_contractsResolved,
    pfMeasurementLedger_full_passes_uniqueContractNames,
    pfMeasurementLedger_full_passes_measurementOutcomeConsistent⟩

-- ---------------------------------------------------------------------------
-- 4. Full 10-check audit: claim ledger + measurement ledger
-- ---------------------------------------------------------------------------

/-- **The full 10-check audit passes for the ungated claim ledger + full
    measurement ledger.**

    This combines:
    - The 9 claim-ledger checks (`pfClaimLedger_passes_full_audit` from
      `FundamentalsAudit.lean`)
    - The measurement-outcome consistency check (Check 10), proven above
      via `pfMeasurementLedger_full_passes_measurementOutcomeConsistent`.

    `pfMeasurementContracts` (from `FundamentalsAudit.lean`) is definitionally
    equal to `pfMeasurementLedger_full.contracts`, so we reuse the existing
    `auditPassesWithMeasurements` proof directly. -/
theorem pfMeasurementLedger_full_passes_auditWithMeasurements :
    auditPassesWithMeasurements pfClaimLedger
      pfMeasurementLedger_full.contracts pfMeasurementOutcomes :=
  pfClaimLedger_passes_full_audit_with_measurements

/-- **The computable 10-check audit returns all-passed.** -/
theorem pfMeasurementLedger_full_runAuditWithMeasurements_allPassed :
    (runAuditWithMeasurements pfClaimLedger
      pfMeasurementLedger_full.contracts pfMeasurementOutcomes).allPassed = true := by
  rw [runAuditWithMeasurements_allPassed_iff_auditPassesWithMeasurements]
  exact pfMeasurementLedger_full_passes_auditWithMeasurements

-- ---------------------------------------------------------------------------
-- 5. Gated ledger + measurement ledger (10-check, non-vacuous status gate)
-- ---------------------------------------------------------------------------
/-
  The gated outcome map (`pfMeasurementOutcomes_gated`) and the gated
  measurement-outcome consistency proof are already defined and proven in
  `FundamentalsAudit.lean` (section 8).  We reuse them directly here.

  The gated map: PFEntropy_decreases_T3 → `none` (premise open), the other
  3 → `Confirmed`.  The 3 Confirmed claims are `.OK` in the gated ledger;
  the `none` case is vacuous.
-/

/-- **Check 1 (gated)**: The full ledger resolves against `pfClaimLedger_gated`.

    The gated ledger has the same entry names as the ungated ledger (only
    statuses changed from `.OK` to `.HOLD` for two entries).  So every
    contract's `claimName` still names an existing entry. -/
theorem pfMeasurementLedger_full_passes_contractsResolved_gated :
    pfMeasurementLedger_full.contractsResolved pfClaimLedger_gated := by
  rw [MeasurementLedger.contractsResolved, pfMeasurementLedger_full,
      MeasurementLedger.empty, MeasurementLedger.add]
  simp [PFEntropy_T3_contract, Weinberg_contract, Koide_contract, GravityOptics_contract,
        pfClaimLedger_gated, fullNormT3StrictlyDecreasesEntry_gated,
        PFEntropyDecreasesT3Entry_gated]
  decide

/-- **The gated measurement ledger passes all 3 structural checks.**

    - `contractsResolved`: proven above against `pfClaimLedger_gated`
    - `uniqueContractNames`: unchanged by gating (property of the measurement
      ledger, not the claim ledger)
    - `measurementOutcomeConsistent`: already proven in `FundamentalsAudit.lean`
      as `pfClaimLedger_gated_passes_measurementOutcomeConsistent` -/
theorem pfMeasurementLedger_full_passes_measurementLedgerAudit_gated :
    measurementLedgerAuditPasses pfMeasurementLedger_full pfClaimLedger_gated
      pfMeasurementOutcomes_gated :=
  ⟨pfMeasurementLedger_full_passes_contractsResolved_gated,
    pfMeasurementLedger_full_passes_uniqueContractNames,
    pfClaimLedger_gated_passes_measurementOutcomeConsistent⟩

/-- **The full 10-check audit passes for the gated claim ledger + full
    measurement ledger.**

    Reuses `pfClaimLedger_gated_passes_full_audit_with_measurements` from
    `FundamentalsAudit.lean`, which combines the 9 gated claim-ledger
    checks with the gated measurement-outcome consistency check. -/
theorem pfMeasurementLedger_full_passes_auditWithMeasurements_gated :
    auditPassesWithMeasurements pfClaimLedger_gated
      pfMeasurementLedger_full.contracts pfMeasurementOutcomes_gated :=
  pfClaimLedger_gated_passes_full_audit_with_measurements

/-- **The computable 10-check audit returns all-passed (gated).** -/
theorem pfMeasurementLedger_full_runAuditWithMeasurements_allPassed_gated :
    (runAuditWithMeasurements pfClaimLedger_gated
      pfMeasurementLedger_full.contracts pfMeasurementOutcomes_gated).allPassed = true := by
  rw [runAuditWithMeasurements_allPassed_iff_auditPassesWithMeasurements]
  exact pfMeasurementLedger_full_passes_auditWithMeasurements_gated

-- ---------------------------------------------------------------------------
-- 6. Summary theorems
-- ---------------------------------------------------------------------------

/-- **The minimal measurement ledger (1 contract) passes its structural audit.**

    - `contractsResolved`: PFEntropy_T3_contract → PFEntropy_decreases_T3 ✓
    - `uniqueContractNames`: single contract, trivially Nodup ✓
    - `measurementOutcomeConsistent`: Confirmed → .OK ✓ -/
theorem pfMeasurementLedger_audit_summary :
    measurementLedgerAuditPasses pfMeasurementLedger pfClaimLedger
      pfMeasurementOutcomes_minimal :=
  pfMeasurementLedger_passes_measurementLedgerAudit

/-- **The full measurement ledger (4 contracts) passes its structural audit.**

    - `contractsResolved`: all 4 claim names exist in pfClaimLedger ✓
    - `uniqueContractNames`: 4 distinct claim names, Nodup ✓
    - `measurementOutcomeConsistent`: all 4 Confirmed → all 4 .OK ✓ -/
theorem pfMeasurementLedger_full_audit_summary :
    measurementLedgerAuditPasses pfMeasurementLedger_full pfClaimLedger
      pfMeasurementOutcomes :=
  pfMeasurementLedger_full_passes_measurementLedgerAudit

/-- **The complete 10-check audit passes (ungated).**

    9 claim-ledger checks + 1 measurement-outcome check = 10/10 PASS. -/
theorem pfMeasurementLedger_full_complete_audit_passes :
    auditPasses pfClaimLedger ∧
    measurementLedgerAuditPasses pfMeasurementLedger_full pfClaimLedger
      pfMeasurementOutcomes :=
  ⟨pfClaimLedger_passes_full_audit,
    pfMeasurementLedger_full_passes_measurementLedgerAudit⟩

/-- **The complete 10-check audit passes (gated).**

    9 claim-ledger checks (gated, non-vacuous status gate) +
    1 measurement-outcome check (3 Confirmed + 1 none) = 10/10 PASS. -/
theorem pfMeasurementLedger_full_complete_audit_passes_gated :
    auditPasses pfClaimLedger_gated ∧
    measurementLedgerAuditPasses pfMeasurementLedger_full pfClaimLedger_gated
      pfMeasurementOutcomes_gated :=
  ⟨pfClaimLedger_gated_passes_full_audit,
    pfMeasurementLedger_full_passes_measurementLedgerAudit_gated⟩

end PfLean
