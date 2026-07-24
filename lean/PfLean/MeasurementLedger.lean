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

-- ---------------------------------------------------------------------------
-- 4. Entry-level measurement application
-- ---------------------------------------------------------------------------

/-- Apply a measurement outcome to a `ClaimEntry`, producing an updated entry
    with the same `P` and an updated record. -/
def ClaimEntry.applyOutcome (e : ClaimEntry) (o : MeasurementOutcome)
    (note : String) : ClaimEntry :=
  { name := e.name
    P := e.P
    record := MeasurementContract.applyOutcome e.record o note }

/-- The record field of `applyOutcome` is the applied record. -/
theorem ClaimEntry.applyOutcome_record (e : ClaimEntry) (o : MeasurementOutcome)
    (note : String) :
    (ClaimEntry.applyOutcome e o note).record =
      MeasurementContract.applyOutcome e.record o note := by
  rfl

/-- The name field of `applyOutcome` is preserved. -/
theorem ClaimEntry.applyOutcome_name (e : ClaimEntry) (o : MeasurementOutcome)
    (note : String) :
    (ClaimEntry.applyOutcome e o note).name = e.name := by
  rfl

/-- Applying a Confirmed outcome to a DERIVED entry makes it public-ready.

    This is the core publication-readiness theorem: a machine-confirmed
    measurement on a DERIVED claim yields a public-ready claim. -/
theorem confirmed_derived_entry_is_public_ready (e : ClaimEntry) (note : String)
    (h_derived : e.record.tier = .DERIVED) :
    (ClaimEntry.applyOutcome e .Confirmed note).record.isPublicReady := by
  unfold ClaimRecord.isPublicReady
  rw [ClaimEntry.applyOutcome_record]
  refine ⟨?_, ?_⟩
  · exact applyOutcome_confirmed_sets_OK e.record note
  · left
    have h := applyOutcome_preserves_tier e.record .Confirmed note
    rw [h]
    exact h_derived

/-- Applying a Confirmed outcome to an EMPIRICAL entry with confidence ≥ 0.90
    makes it public-ready. -/
theorem confirmed_empirical_entry_is_public_ready (e : ClaimEntry) (note : String)
    (h_empirical : e.record.tier = .EMPIRICAL)
    (h_conf : e.record.confidence.value ≥ 0.90) :
    (ClaimEntry.applyOutcome e .Confirmed note).record.isPublicReady := by
  unfold ClaimRecord.isPublicReady
  rw [ClaimEntry.applyOutcome_record]
  refine ⟨?_, ?_⟩
  · exact applyOutcome_confirmed_sets_OK e.record note
  · right
    refine ⟨?_, ?_⟩
    · have h := applyOutcome_preserves_tier e.record .Confirmed note
      rw [h]
      exact h_empirical
    · have h := applyOutcome_preserves_confidence e.record .Confirmed note
      rw [h]
      exact h_conf

-- ---------------------------------------------------------------------------
-- 5. Ledger-level measurement application
-- ---------------------------------------------------------------------------

/-- Apply a measurement outcome to the entry in a `ClaimLedger` matching a
    given claim name.  Entries that don't match are left unchanged. -/
def ClaimLedger.applyMeasurement (cl : ClaimLedger) (claimName : String)
    (o : MeasurementOutcome) (note : String) : ClaimLedger :=
  ⟨cl.entries.map (fun e =>
    if e.name = claimName then ClaimEntry.applyOutcome e o note else e)⟩

/-- The entries of `applyMeasurement` are the same length as the original. -/
theorem ClaimLedger.applyMeasurement_length (cl : ClaimLedger) (name : String)
    (o : MeasurementOutcome) (note : String) :
    (cl.applyMeasurement name o note).entries.length = cl.entries.length := by
  simp [ClaimLedger.applyMeasurement, List.length_map]

/-- A Confirmed measurement on a DERIVED claim in the ledger produces a
    public-ready entry in the updated ledger.

    This is the cross-ledger publication-readiness theorem: it composes
    `contractsResolved` (the measurement points at a real claim) with
    `confirmed_derived_entry_is_public_ready` (confirmation makes it
    publishable) to give the end-to-end guarantee. -/
theorem confirmed_derived_claim_becomes_public_ready
    (cl : ClaimLedger) (ml : MeasurementLedger)
    (c : MeasurementContract) (note : String)
    (h_c_in_ml : c ∈ ml.contracts)
    (h_resolved : ml.contractsResolved cl)
    (e : ClaimEntry) (h_e_in_cl : e ∈ cl.entries)
    (h_name_match : e.name = c.claimName)
    (h_derived : e.record.tier = .DERIVED) :
    ∃ e' ∈ (cl.applyMeasurement c.claimName .Confirmed note).entries,
      e'.name = e.name ∧ e'.record.isPublicReady := by
  refine ⟨ClaimEntry.applyOutcome e .Confirmed note, ?_, ?_⟩
  · -- The updated entry is in the mapped list
    simp [ClaimLedger.applyMeasurement]
    refine ⟨e, h_e_in_cl, ?_⟩
    rw [h_name_match]
    simp
  · -- The updated entry has the right name and is public-ready
    refine ⟨ClaimEntry.applyOutcome_name e .Confirmed note,
            confirmed_derived_entry_is_public_ready e note h_derived⟩

-- ---------------------------------------------------------------------------
-- 6. Concrete example: Koide claim is DERIVED and has a confirmed measurement
-- ---------------------------------------------------------------------------

/-- The Koide Q = 2/3 claim is DERIVED tier. -/
theorem koide_entry_is_derived :
    koideQTwoThirdsEntry.record.tier = .DERIVED := by
  rfl

/-- The gravity optics n(0) = 1 claim is DERIVED tier. -/
theorem gravityOptics_entry_is_derived :
    weakFieldIndexFlatEntry.record.tier = .DERIVED := by
  rfl

/-- The Weinberg angle claim is ARGUED tier (not DERIVED). -/
theorem weinberg_entry_is_argued :
    weinbergRatioEntry.record.tier = .ARGUED := by
  rfl

/-- The PFEntropy T³ claim is CONDITIONAL tier (not DERIVED). -/
theorem pfentropy_entry_is_conditional :
    PFEntropyDecreasesT3Entry.record.tier = .CONDITIONAL := by
  rfl

end PfLean
