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

-- ---------------------------------------------------------------------------
-- 7. Concrete positive instance: Koide claim is publication-ready
-- ---------------------------------------------------------------------------

/-- The Koide entry is in `pfClaimLedger`. -/
theorem koide_entry_in_ledger :
    koideQTwoThirdsEntry ∈ pfClaimLedger.entries := by
  simp [pfClaimLedger]

/-- The Koide contract's claimName matches the Koide entry's name. -/
theorem koide_contract_matches_entry :
    Koide_contract.claimName = koideQTwoThirdsEntry.name := by
  simp [Koide_contract, koideQTwoThirdsEntry]

/-- The Koide contract is in `pfMeasurementLedger_full`. -/
theorem koide_contract_in_ledger :
    Koide_contract ∈ pfMeasurementLedger_full.contracts := by
  simp [pfMeasurementLedger_full, MeasurementLedger.empty, MeasurementLedger.add]

/-- **Concrete publication-readiness theorem**: Applying the confirmed Koide
    measurement to the Koide claim in `pfClaimLedger` produces a public-ready
    entry.  This is the first specific, concrete instance of the capstone
    theorem — not "for any DERIVED claim" but "this specific Koide Q = 2/3
    claim, with this specific charged-lepton measurement, is public-ready." -/
theorem koide_claim_is_public_ready_after_confirmation :
    ∃ e' ∈ (pfClaimLedger.applyMeasurement
              koideQTwoThirdsEntry.name .Confirmed
              "PDG charged lepton masses: Q = 0.66666 ± 0.00001").entries,
      e'.name = koideQTwoThirdsEntry.name ∧ e'.record.isPublicReady := by
  apply confirmed_derived_claim_becomes_public_ready
    pfClaimLedger pfMeasurementLedger_full Koide_contract
    "PDG charged lepton masses: Q = 0.66666 ± 0.00001"
  · exact koide_contract_in_ledger
  · exact pfMeasurementLedger_full_resolved
  · exact koide_entry_in_ledger
  · exact koide_contract_matches_entry
  · exact koide_entry_is_derived

-- ---------------------------------------------------------------------------
-- 8. Concrete negative instance: Falsified claims are NOT public-ready
-- ---------------------------------------------------------------------------

/-- Applying a Falsified outcome to any entry makes it NOT public-ready.
    This is the core rejection theorem: a falsified claim cannot be
    public-ready because its status is NOGO, not OK. -/
theorem falsified_entry_is_not_public_ready (e : ClaimEntry) (note : String) :
    ¬ (ClaimEntry.applyOutcome e .Falsified note).record.isPublicReady := by
  intro h
  unfold ClaimRecord.isPublicReady at h
  have h_status := h.1
  have h_falsified : (MeasurementContract.applyOutcome e.record .Falsified note).status = .NOGO := by
    simp [MeasurementContract.applyOutcome]
  rw [ClaimEntry.applyOutcome_record] at h_status
  -- h_status : status = OK, h_falsified : status = NOGO, OK ≠ NOGO
  rw [h_status] at h_falsified
  exact absurd h_falsified (by decide)

/-- Applying an Inconclusive outcome to any entry makes it NOT public-ready.
    An inconclusive measurement cannot make a claim public-ready. -/
theorem inconclusive_entry_is_not_public_ready (e : ClaimEntry) (note : String) :
    ¬ (ClaimEntry.applyOutcome e .Inconclusive note).record.isPublicReady := by
  intro h
  unfold ClaimRecord.isPublicReady at h
  have h_status := h.1
  have h_inconclusive : (MeasurementContract.applyOutcome e.record .Inconclusive note).status = .HOLD := by
    simp [MeasurementContract.applyOutcome]
  rw [ClaimEntry.applyOutcome_record] at h_status
  rw [h_status] at h_inconclusive
  exact absurd h_inconclusive (by decide)

/-- **Concrete rejection theorem**: The PFEntropy T³ claim, after a falsifying
    measurement (0.20 ± 0.005, which falsifies the ratio = 1/8 prediction),
    is NOT public-ready.  This is the system rejecting its own claim —
    machine-proven. -/
theorem pfentropy_claim_not_public_ready_after_falsification :
    ¬ (ClaimEntry.applyOutcome PFEntropyDecreasesT3Entry .Falsified
        "sandbox/T3_entropy_ratio_hostile: 0.20 ± 0.005").record.isPublicReady := by
  exact falsified_entry_is_not_public_ready PFEntropyDecreasesT3Entry _

/-- **Concrete rejection theorem**: The gravity optics n(0) = 1 claim — which
    is DERIVED tier — after a falsifying Lorentz-violating measurement
    (n = 1.02 ± 0.001), is NOT public-ready.  Falsification overrides tier:
    a falsified DERIVED claim is still not publishable. -/
theorem gravity_claim_not_public_ready_after_falsification :
    ¬ (ClaimEntry.applyOutcome weakFieldIndexFlatEntry .Falsified
        "hypothetical Lorentz violation: n = 1.02 ± 0.001").record.isPublicReady := by
  exact falsified_entry_is_not_public_ready weakFieldIndexFlatEntry _

/-- **Concrete non-promotion theorem**: The Weinberg angle claim is ARGUED
    tier.  Even after a confirming measurement, it is NOT public-ready —
    because `isPublicReady` requires DERIVED or EMPIRICAL ≥ 0.90, and ARGUED
    does not qualify.  This is the system being honest: confirmation is
    necessary but not sufficient; the tier must also be high enough. -/
theorem weinberg_claim_not_public_ready_even_if_confirmed :
    ¬ (ClaimEntry.applyOutcome weinbergRatioEntry .Confirmed
        "PDG on-shell sin²θ_W: 0.22310 ± 0.00010").record.isPublicReady := by
  intro h
  unfold ClaimRecord.isPublicReady at h
  obtain ⟨h_status, h_tier⟩ := h
  -- tier is preserved as ARGUED
  rw [ClaimEntry.applyOutcome_record] at h_tier
  have h_preserve : (MeasurementContract.applyOutcome weinbergRatioEntry.record .Confirmed
                      "PDG on-shell sin²θ_W: 0.22310 ± 0.00010").tier
                    = weinbergRatioEntry.record.tier := by
    exact applyOutcome_preserves_tier _ _ _
  rw [h_preserve, weinberg_entry_is_argued] at h_tier
  -- h_tier : ARGUED = DERIVED ∨ (ARGUED = EMPIRICAL ∧ ...) — both impossible
  simp at h_tier

end PfLean
