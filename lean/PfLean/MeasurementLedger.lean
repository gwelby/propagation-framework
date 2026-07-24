/-
  PfLean.MeasurementLedger — Linking Measurement Contracts to the Claim Ledger
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-07-24

  A `MeasurementLedger` is a list of `MeasurementContract`s.  Its key
  consistency property is `contractsResolved`: every contract's `claimName`
  must name an existing entry in a given `ClaimLedger`.

  This module defines the structure, the consistency predicate, a concrete
  `pfMeasurementLedger` (the single contract that resolves), and a
  `pfMeasurementLedger_full` (all 4 contracts) which now resolves against
  the 13-entry `pfClaimLedger`.

  It also proves `applyOutcome` correctness: Confirmed → OK, Falsified →
  NOGO, Inconclusive → HOLD — closing the loop between measurement and
  claim status.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.ClaimLedger
import PfLean.ClaimLedgerRegistry
import PfLean.MeasurementContract

namespace PfLean

-- ---------------------------------------------------------------------------
-- 1. MeasurementLedger structure
-- ---------------------------------------------------------------------------

/-- A ledger of measurement contracts, linked to a claim ledger by name. -/
structure MeasurementLedger where
  contracts : List MeasurementContract

namespace MeasurementLedger

/-- The empty ledger. -/
def empty : MeasurementLedger := ⟨[]⟩

/-- Add a contract to the ledger. -/
def add (ml : MeasurementLedger) (c : MeasurementContract) : MeasurementLedger :=
  ⟨c :: ml.contracts⟩

/-- All claim names referenced by the contracts. -/
def allClaimNames (ml : MeasurementLedger) : List String :=
  ml.contracts.map (·.claimName)

/-- Every contract's `claimName` names an existing entry in the `ClaimLedger`.
    This is the key consistency property: a measurement ledger is only
    well-formed if every contract points at a real formal claim. -/
def contractsResolved (ml : MeasurementLedger) (cl : ClaimLedger) : Prop :=
  ∀ c ∈ ml.contracts, ∃ e ∈ cl.entries, e.name = c.claimName

/-- The empty measurement ledger vacuously resolves against any claim ledger. -/
theorem empty_resolves (cl : ClaimLedger) :
    contractsResolved empty cl := by
  simp [empty, contractsResolved]

end MeasurementLedger

-- ---------------------------------------------------------------------------
-- 2. Concrete PF measurement ledgers
-- ---------------------------------------------------------------------------

/-- The minimal measurement ledger: just the PFEntropy T³ contract. -/
noncomputable def pfMeasurementLedger : MeasurementLedger :=
  MeasurementLedger.empty.add PFEntropy_T3_contract

/-- The minimal ledger resolves against `pfClaimLedger`. -/
theorem pfMeasurementLedger_resolved :
    MeasurementLedger.contractsResolved pfMeasurementLedger pfClaimLedger := by
  rw [MeasurementLedger.contractsResolved, pfMeasurementLedger,
      MeasurementLedger.empty, MeasurementLedger.add]
  simp [PFEntropy_T3_contract]
  native_decide

/-- The full measurement ledger: all 4 contracts. -/
noncomputable def pfMeasurementLedger_full : MeasurementLedger :=
  MeasurementLedger.empty
    |>.add PFEntropy_T3_contract
    |>.add Weinberg_contract
    |>.add Koide_contract
    |>.add GravityOptics_contract

/-- The full ledger has 4 contracts. -/
theorem pfMeasurementLedger_full_length :
    pfMeasurementLedger_full.contracts.length = 4 := by
  decide

/-- The full ledger resolves against `pfClaimLedger` (13 entries).
    All 4 contract claim names — `PFEntropy_decreases_T3`,
    `weinberg_ratio`, `koide_Q_two_thirds`, `weakFieldIndex_flat` —
    now exist in `pfClaimLedger`. -/
theorem pfMeasurementLedger_full_resolved :
    MeasurementLedger.contractsResolved pfMeasurementLedger_full pfClaimLedger := by
  rw [MeasurementLedger.contractsResolved, pfMeasurementLedger_full,
      MeasurementLedger.empty, MeasurementLedger.add]
  simp [PFEntropy_T3_contract, Weinberg_contract, Koide_contract, GravityOptics_contract]
  decide

-- ---------------------------------------------------------------------------
-- 3. applyOutcome correctness
-- ---------------------------------------------------------------------------

/-- Applying a `Confirmed` outcome sets the claim status to `OK`. -/
theorem applyOutcome_confirmed_sets_OK {P : Prop} (cr : ClaimRecord P) (note : String) :
    (MeasurementContract.applyOutcome cr .Confirmed note).status = .OK := by
  simp [MeasurementContract.applyOutcome]

/-- Applying an `Inconclusive` outcome sets the claim status to `HOLD`. -/
theorem applyOutcome_inconclusive_sets_HOLD {P : Prop} (cr : ClaimRecord P) (note : String) :
    (MeasurementContract.applyOutcome cr .Inconclusive note).status = .HOLD := by
  simp [MeasurementContract.applyOutcome]

/-- Applying a `Falsified` outcome sets the claim status to `NOGO`. -/
theorem applyOutcome_falsified_sets_NOGO {P : Prop} (cr : ClaimRecord P) (note : String) :
    (MeasurementContract.applyOutcome cr .Falsified note).status = .NOGO := by
  simp [MeasurementContract.applyOutcome]

/-- Applying any outcome preserves the proof, tier, and confidence. -/
theorem applyOutcome_preserves_proof {P : Prop} (cr : ClaimRecord P)
    (o : MeasurementOutcome) (note : String) :
    (MeasurementContract.applyOutcome cr o note).proof = cr.proof := by
  cases o <;> simp [MeasurementContract.applyOutcome]

/-- Applying any outcome preserves the tier. -/
theorem applyOutcome_preserves_tier {P : Prop} (cr : ClaimRecord P)
    (o : MeasurementOutcome) (note : String) :
    (MeasurementContract.applyOutcome cr o note).tier = cr.tier := by
  cases o <;> simp [MeasurementContract.applyOutcome]

/-- Applying any outcome preserves the confidence. -/
theorem applyOutcome_preserves_confidence {P : Prop} (cr : ClaimRecord P)
    (o : MeasurementOutcome) (note : String) :
    (MeasurementContract.applyOutcome cr o note).confidence = cr.confidence := by
  cases o <;> simp [MeasurementContract.applyOutcome]

/-- Applying any outcome preserves the tier_bound invariant.
    This means a measurement can never break the epistemic tier guarantee:
    even a falsified claim retains its tier/confidence bounds. -/
theorem applyOutcome_tier_bound_holds {P : Prop} (cr : ClaimRecord P)
    (o : MeasurementOutcome) (note : String) :
    EpistemicTier.minConfidence (MeasurementContract.applyOutcome cr o note).tier ≤
      (MeasurementContract.applyOutcome cr o note).confidence.value ∧
    (MeasurementContract.applyOutcome cr o note).confidence.value ≤
      EpistemicTier.maxConfidence (MeasurementContract.applyOutcome cr o note).tier := by
  have ht : (MeasurementContract.applyOutcome cr o note).tier = cr.tier := by
    cases o <;> rfl
  have hc : (MeasurementContract.applyOutcome cr o note).confidence = cr.confidence := by
    cases o <;> rfl
  rw [ht, hc]
  exact cr.tier_bound

end PfLean
