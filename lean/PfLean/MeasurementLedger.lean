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
  the 14-entry `pfClaimLedger`.

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

/-- The measurement ledger has occurrence-unique contract claim names: no
    two **positions** in `contracts` have the same `claimName`.  This is
    the occurrence-level invariant for one-to-one contract-to-entry binding.

    Codex re-audit (2026-07-30, `clg_1b946d7211000490825d6aa6`, PFU-03)
    identified that `contractsResolved` is existential and does not check
    for duplicate contracts.  This predicate closes that gap. -/
def uniqueContractNames (ml : MeasurementLedger) : Prop :=
  (ml.contracts.map (·.claimName)).Nodup

/-- The empty measurement ledger vacuously resolves against any claim ledger. -/
theorem empty_resolves (cl : ClaimLedger) :
    contractsResolved empty cl := by
  simp [empty, contractsResolved]

/-- The empty measurement ledger vacuously satisfies `uniqueContractNames`. -/
theorem empty_unique_contract_names :
    uniqueContractNames empty := by
  simp [empty, uniqueContractNames]

/-- Under `uniqueContractNames`, if a contract with the given claim name
    exists, the filter of contracts matching that name has length exactly 1.
    This is the contract-level analog of `ClaimLedger.exactly_one_matching_entry`. -/
theorem exactly_one_matching_contract
    (ml : MeasurementLedger) (hUnique : ml.uniqueContractNames)
    (name : String) (h_exists : ∃ c ∈ ml.contracts, c.claimName = name) :
    (ml.contracts.filter (fun c => c.claimName = name)).length = 1 := by
  have helper : ∀ (l : List MeasurementContract) (target : String),
      (l.map (·.claimName)).Nodup →
      (∃ c ∈ l, c.claimName = target) →
      (l.filter (fun c => c.claimName = target)).length = 1 := by
    intro l target
    induction l with
    | nil => intro _ h; exact absurd h (by simp)
    | cons x xs ih =>
      intro hnodup hexists
      rw [List.map_cons, List.nodup_cons] at hnodup
      obtain ⟨hfx_notin, hxs_nodup⟩ := hnodup
      by_cases hxeq : x.claimName = target
      · have hno_match : ∀ c ∈ xs, c.claimName ≠ target := by
          intro c hc hcname
          have hmem : target ∈ xs.map (·.claimName) := by
            rw [List.mem_map]; exact ⟨c, hc, hcname⟩
          rw [← hxeq] at hmem
          exact absurd hmem hfx_notin
        have hfilter_nil : (xs.filter (fun c => c.claimName = target)) = [] := by
          clear ih hexists hfx_notin hxs_nodup
          induction xs with
          | nil => rfl
          | cons y ys ih_filter =>
            by_cases hyeq : y.claimName = target
            · exact absurd hyeq (hno_match y (by simp))
            · simp [hyeq]
              intro e he hename
              exact hno_match e (List.mem_cons_of_mem _ he) hename
        simp [hxeq, List.filter_cons, hfilter_nil]
      · have hexists_xs : ∃ c ∈ xs, c.claimName = target := by
          obtain ⟨c, hc, hcname⟩ := hexists
          simp only [List.mem_cons] at hc
          rcases hc with rfl | hc
          · simp [hxeq] at hcname
          · exact ⟨c, hc, hcname⟩
        simp [hxeq, List.filter_cons]
        exact ih hxs_nodup hexists_xs
  exact helper ml.contracts name hUnique h_exists

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

/-- The minimal ledger has occurrence-unique contract names (single contract,
    trivially Nodup). -/
theorem pfMeasurementLedger_unique_contract_names :
    pfMeasurementLedger.uniqueContractNames := by
  rw [MeasurementLedger.uniqueContractNames, pfMeasurementLedger,
      MeasurementLedger.empty, MeasurementLedger.add]
  simp [PFEntropy_T3_contract]

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

/-- The full ledger resolves against `pfClaimLedger` (14 entries).
    All 4 contract claim names — `PFEntropy_decreases_T3`,
    `weinberg_ratio`, `koide_Q_two_thirds`, `weakFieldIndex_flat` —
    now exist in `pfClaimLedger`. -/
theorem pfMeasurementLedger_full_resolved :
    MeasurementLedger.contractsResolved pfMeasurementLedger_full pfClaimLedger := by
  rw [MeasurementLedger.contractsResolved, pfMeasurementLedger_full,
      MeasurementLedger.empty, MeasurementLedger.add]
  simp [PFEntropy_T3_contract, Weinberg_contract, Koide_contract, GravityOptics_contract]
  decide

/-- The full ledger has occurrence-unique contract names: the four claim
    names `PFEntropy_decreases_T3`, `weinberg_ratio`, `koide_Q_two_thirds`,
    `weakFieldIndex_flat` are all distinct, so the name list is Nodup. -/
theorem pfMeasurementLedger_full_unique_contract_names :
    pfMeasurementLedger_full.uniqueContractNames := by
  rw [MeasurementLedger.uniqueContractNames, pfMeasurementLedger_full,
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

/-- Applying a Confirmed outcome to a DERIVED entry makes it meet the tier gate.

    This is the core tier-gate theorem: a machine-confirmed
    measurement on a DERIVED claim yields a meets the tier gate claim. -/
theorem confirmed_derived_entry_meets_tier_gate (e : ClaimEntry) (note : String)
    (h_derived : e.record.tier = .DERIVED) :
    (ClaimEntry.applyOutcome e .Confirmed note).record.meetsPublicationTierGate := by
  unfold ClaimRecord.meetsPublicationTierGate
  rw [ClaimEntry.applyOutcome_record]
  refine ⟨?_, ?_⟩
  · exact applyOutcome_confirmed_sets_OK e.record note
  · left
    have h := applyOutcome_preserves_tier e.record .Confirmed note
    rw [h]
    exact h_derived

/-- Applying a Confirmed outcome to an EMPIRICAL entry with confidence ≥ 0.90
    makes it meet the tier gate. -/
theorem confirmed_empirical_entry_meets_tier_gate (e : ClaimEntry) (note : String)
    (h_empirical : e.record.tier = .EMPIRICAL)
    (h_conf : e.record.confidence.value ≥ 0.90) :
    (ClaimEntry.applyOutcome e .Confirmed note).record.meetsPublicationTierGate := by
  unfold ClaimRecord.meetsPublicationTierGate
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

/-- Select the claim entry named by a contract using the ledger-resolution
    witness.  The selected entry is defined from both membership in the
    measurement ledger and `contractsResolved`; it is not caller-supplied. -/
noncomputable def MeasurementLedger.resolvedEntry (ml : MeasurementLedger)
    (cl : ClaimLedger) (c : MeasurementContract)
    (h_c_in_ml : c ∈ ml.contracts) (h_resolved : ml.contractsResolved cl) :
    ClaimEntry :=
  Classical.choose (h_resolved c h_c_in_ml)

/-- The resolver returns an entry actually present in the claim ledger. -/
theorem MeasurementLedger.resolvedEntry_mem (ml : MeasurementLedger)
    (cl : ClaimLedger) (c : MeasurementContract)
    (h_c_in_ml : c ∈ ml.contracts) (h_resolved : ml.contractsResolved cl) :
    ml.resolvedEntry cl c h_c_in_ml h_resolved ∈ cl.entries := by
  exact (Classical.choose_spec (h_resolved c h_c_in_ml)).1

/-- The resolver's entry has exactly the contract's claim name. -/
theorem MeasurementLedger.resolvedEntry_name (ml : MeasurementLedger)
    (cl : ClaimLedger) (c : MeasurementContract)
    (h_c_in_ml : c ∈ ml.contracts) (h_resolved : ml.contractsResolved cl) :
    (ml.resolvedEntry cl c h_c_in_ml h_resolved).name = c.claimName := by
  exact (Classical.choose_spec (h_resolved c h_c_in_ml)).2

/-- **Bridge theorem (computed outcome, derived entry, consumed premises)**:
    Given a measurement `m`, a contract `c` in measurement ledger `ml` that
    resolves against claim ledger `cl`, if the `outcome` function computes
    `.Confirmed` for `m` against `c`, and every entry in `cl` matching
    `c.claimName` is `DERIVED` tier, then applying that computed outcome to
    the resolved entry in the ledger yields an entry that meets the
    publication tier gate.

    This theorem **genuinely consumes** all its premises:
    - `h_c_in_ml : c ∈ ml.contracts` — used to instantiate `h_resolved`
    - `h_resolved : ml.contractsResolved cl` — applied to `h_c_in_ml` to
      **derive** the entry `e` from the bridge (not caller-supplied)
    - `h_outcome : outcome m c = .Confirmed` — the computed outcome, rewritten
      into the `applyMeasurement` call
    - `h_tier : ∀ e ∈ cl.entries, e.name = c.claimName → e.record.tier = .DERIVED`
      — applied to the derived entry to obtain the tier proof

    The entry used in the result is the named `resolvedEntry` selected from
    `h_resolved` + `h_c_in_ml`, not a caller-supplied witness. -/
theorem confirmed_derived_claim_meets_tier_gate
    (cl : ClaimLedger) (ml : MeasurementLedger)
    (m : Measurement) (c : MeasurementContract) (note : String)
    (h_c_in_ml : c ∈ ml.contracts)
    (h_resolved : ml.contractsResolved cl)
    (h_outcome : MeasurementContract.outcome m c = .Confirmed)
    (h_tier : ∀ e ∈ cl.entries, e.name = c.claimName → e.record.tier = .DERIVED) :
    ∃ e' ∈ (cl.applyMeasurement c.claimName
              (MeasurementContract.outcome m c) note).entries,
      e'.name = c.claimName ∧ e'.record.meetsPublicationTierGate := by
  -- Select the entry FROM the bridge; it cannot be named without both
  -- contract membership and a `contractsResolved` witness.
  let e := ml.resolvedEntry cl c h_c_in_ml h_resolved
  have h_e_in : e ∈ cl.entries :=
    MeasurementLedger.resolvedEntry_mem ml cl c h_c_in_ml h_resolved
  have h_e_name : e.name = c.claimName :=
    MeasurementLedger.resolvedEntry_name ml cl c h_c_in_ml h_resolved
  -- Obtain the tier proof from h_tier, applied to the derived entry
  have h_derived : e.record.tier = .DERIVED := h_tier e h_e_in h_e_name
  -- Rewrite the computed outcome
  rw [h_outcome]
  -- Build the witness: the derived entry, updated with the computed Confirmed
  refine ⟨ClaimEntry.applyOutcome e .Confirmed note, ?_, ?_⟩
  · -- The updated entry is in the mapped list (uses h_e_in, h_e_name)
    simp [ClaimLedger.applyMeasurement]
    refine ⟨e, h_e_in, ?_⟩
    rw [h_e_name]
    simp
  · -- The updated entry has name = c.claimName (via h_e_name) and meets the tier gate
    have h_name' : (ClaimEntry.applyOutcome e .Confirmed note).name = c.claimName := by
      rw [ClaimEntry.applyOutcome_name, h_e_name]
    refine ⟨h_name',
            confirmed_derived_entry_meets_tier_gate e note h_derived⟩

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

/-- The kernel-only PFEntropy T³ identity is DERIVED.  This is deliberately
    distinct from `PFEntropyDecreasesT3Entry`, whose physical reading remains
    conditional on `PFEntropyT3PhysicalTransferPremise`. -/
theorem pfentropy_formal_identity_entry_is_derived :
    PFEntropyT3FormalIdentityEntry.record.tier = .DERIVED := by
  rfl

-- ---------------------------------------------------------------------------
-- 7. Concrete positive instance: Koide claim is tier-gate
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

/-- **Concrete tier-gate theorem (computed outcome, derived entry)**: Running
    the charged-lepton measurement through the Koide contract, the `outcome`
    function computes `.Confirmed`.  The bridge theorem derives the matching
    entry from `pfClaimLedger` via `contractsResolved`, obtains its DERIVED
    tier from the tier hypothesis, and concludes the updated entry meets the
    publication tier gate.

    This is the first concrete instance of the bridge theorem.  The entry is
    NOT caller-supplied — it is derived from the measurement ledger's
    resolution property.  The outcome is *computed* (not assumed).  The
    measurement value is a typed literal, not a provenance-validated datum. -/
theorem koide_claim_meets_tier_gate_after_computed_confirmation :
    ∃ e' ∈ (pfClaimLedger.applyMeasurement
              Koide_contract.claimName
              (MeasurementContract.outcome chargedLepton_Koide_measurement Koide_contract)
              "PDG charged lepton masses: Q = 0.66666 ± 0.00001").entries,
      e'.name = Koide_contract.claimName ∧ e'.record.meetsPublicationTierGate := by
  apply confirmed_derived_claim_meets_tier_gate
    pfClaimLedger pfMeasurementLedger_full
    chargedLepton_Koide_measurement Koide_contract
    "PDG charged lepton masses: Q = 0.66666 ± 0.00001"
  · exact koide_contract_in_ledger
  · exact pfMeasurementLedger_full_resolved
  · exact chargedLepton_Koide_confirmed
  · -- h_tier: every entry in pfClaimLedger with name = Koide_contract.claimName is DERIVED
    -- The pfClaimLedger is a concrete list of 14 entries.
    -- The only entry with name "koide_Q_two_thirds" is koideQTwoThirdsEntry, which is DERIVED.
    intro e h_e_in h_name
    -- Unfold Koide_contract to get the literal claim name
    unfold Koide_contract at h_name
    -- Unfold the concrete ledger
    unfold pfClaimLedger at h_e_in
    simp only [List.mem_cons, List.not_mem_nil, or_false] at h_e_in
    -- Case-analyze all 14 entries
    rcases h_e_in with
      rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    all_goals first
      | exact koide_entry_is_derived
      | simp [fullNormT3StrictlyDecreasesEntry, PFEntropyT3FormalIdentityEntry,
          PFEntropyDecreasesT3Entry, fullNormPythagoreanEntry, P0QDotZeroEntry,
          QSumZeroEntry, TFullDecompositionEntry, topologicalAvailabilityEntry,
          kernelClosureOrdersEntry, atMostTwoClosureOrdersEntry, quatToSO3KerEntry,
          weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry] at h_name

-- ---------------------------------------------------------------------------
-- 8. Concrete negative instance: Falsified claims are NOT meet the tier gate
-- ---------------------------------------------------------------------------

/-- Applying a Falsified outcome to any entry makes it NOT meet the tier gate.
    This is the core rejection theorem: a falsified claim cannot be
    meets the tier gate because its status is NOGO, not OK. -/
theorem falsified_entry_does_not_meet_tier_gate (e : ClaimEntry) (note : String) :
    ¬ (ClaimEntry.applyOutcome e .Falsified note).record.meetsPublicationTierGate := by
  intro h
  unfold ClaimRecord.meetsPublicationTierGate at h
  have h_status := h.1
  have h_falsified : (MeasurementContract.applyOutcome e.record .Falsified note).status = .NOGO := by
    simp [MeasurementContract.applyOutcome]
  rw [ClaimEntry.applyOutcome_record] at h_status
  -- h_status : status = OK, h_falsified : status = NOGO, OK ≠ NOGO
  rw [h_status] at h_falsified
  exact absurd h_falsified (by decide)

/-- Applying an Inconclusive outcome to any entry makes it NOT meet the tier gate.
    An inconclusive measurement cannot make a claim meets the tier gate. -/
theorem inconclusive_entry_does_not_meet_tier_gate (e : ClaimEntry) (note : String) :
    ¬ (ClaimEntry.applyOutcome e .Inconclusive note).record.meetsPublicationTierGate := by
  intro h
  unfold ClaimRecord.meetsPublicationTierGate at h
  have h_status := h.1
  have h_inconclusive : (MeasurementContract.applyOutcome e.record .Inconclusive note).status = .HOLD := by
    simp [MeasurementContract.applyOutcome]
  rw [ClaimEntry.applyOutcome_record] at h_status
  rw [h_status] at h_inconclusive
  exact absurd h_inconclusive (by decide)

/-- **Concrete rejection theorem**: The PFEntropy T³ claim, after a falsifying
    measurement (0.20 ± 0.005, which falsifies the ratio = 1/8 prediction),
    is NOT meet the tier gate.  This is the system rejecting its own claim —
    machine-proven. -/
theorem pfentropy_claim_fails_tier_gate_after_falsification :
    ¬ (ClaimEntry.applyOutcome PFEntropyDecreasesT3Entry .Falsified
        "sandbox/T3_entropy_ratio_hostile: 0.20 ± 0.005").record.meetsPublicationTierGate := by
  exact falsified_entry_does_not_meet_tier_gate PFEntropyDecreasesT3Entry _

/-- **Concrete rejection theorem**: The gravity optics n(0) = 1 claim — which
    is DERIVED tier — after a falsifying Lorentz-violating measurement
    (n = 1.02 ± 0.001), is NOT meet the tier gate.  Falsification overrides tier:
    a falsified DERIVED claim does not meet the tier gate. -/
theorem gravity_claim_fails_tier_gate_after_falsification :
    ¬ (ClaimEntry.applyOutcome weakFieldIndexFlatEntry .Falsified
        "hypothetical Lorentz violation: n = 1.02 ± 0.001").record.meetsPublicationTierGate := by
  exact falsified_entry_does_not_meet_tier_gate weakFieldIndexFlatEntry _

/-- **Concrete non-promotion theorem**: The Weinberg angle claim is ARGUED
    tier.  Even after a confirming measurement, it is NOT meet the tier gate —
    because `meetsPublicationTierGate` requires DERIVED or EMPIRICAL ≥ 0.90, and ARGUED
    does not qualify.  This is the system being honest: confirmation is
    necessary but not sufficient; the tier must also be high enough. -/
theorem weinberg_claim_fails_tier_gate_even_if_confirmed :
    ¬ (ClaimEntry.applyOutcome weinbergRatioEntry .Confirmed
        "PDG on-shell sin²θ_W: 0.22310 ± 0.00010").record.meetsPublicationTierGate := by
  intro h
  unfold ClaimRecord.meetsPublicationTierGate at h
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

-- ---------------------------------------------------------------------------
-- 9. Composition theorems — the actual measurement pipeline
-- ---------------------------------------------------------------------------

/-- **Falsification pipeline (generic)**: If a measurement's outcome against
    a contract is `Falsified`, then applying that computed outcome to the
    claim entry makes it NOT meet the tier gate.

    This composes the computed outcome (`h_outcome`) with
    `falsified_entry_does_not_meet_tier_gate`.  The outcome is *computed*,
    not assumed.  The caller is responsible for ensuring `e` is the entry
    targeted by `c` (see `confirmed_derived_claim_meets_tier_gate` for the
    bridge theorem that checks this via `contractsResolved`). -/
theorem falsification_pipeline
    (m : Measurement) (c : MeasurementContract) (e : ClaimEntry) (note : String)
    (h_outcome : MeasurementContract.outcome m c = .Falsified) :
    ¬ (ClaimEntry.applyOutcome e
        (MeasurementContract.outcome m c) note).record.meetsPublicationTierGate := by
  rw [h_outcome]
  exact falsified_entry_does_not_meet_tier_gate e note

/-- **Confirmation pipeline (generic, DERIVED)**: If a measurement's outcome
    against a contract is `Confirmed`, and the claim entry is DERIVED tier,
    then applying that computed outcome makes it meet the tier gate.

    This composes the computed outcome (`h_outcome`) with
    `confirmed_derived_entry_meets_tier_gate`.  The outcome is *computed*,
    not assumed.  The caller is responsible for ensuring `e` is the entry
    targeted by `c` (see `confirmed_derived_claim_meets_tier_gate` for the
    bridge theorem that checks this via `contractsResolved`). -/
theorem confirmation_pipeline_derived
    (m : Measurement) (c : MeasurementContract) (e : ClaimEntry) (note : String)
    (h_outcome : MeasurementContract.outcome m c = .Confirmed)
    (h_derived : e.record.tier = .DERIVED) :
    (ClaimEntry.applyOutcome e
        (MeasurementContract.outcome m c) note).record.meetsPublicationTierGate := by
  rw [h_outcome]
  exact confirmed_derived_entry_meets_tier_gate e note h_derived

/-- **Inconclusive pipeline (generic)**: If a measurement's outcome is
    `Inconclusive`, then applying it makes the entry NOT meet the tier gate.
    An inconclusive measurement cannot promote a claim.  The caller is
    responsible for ensuring `e` is the entry targeted by `c`. -/
theorem inconclusive_pipeline
    (m : Measurement) (c : MeasurementContract) (e : ClaimEntry) (note : String)
    (h_outcome : MeasurementContract.outcome m c = .Inconclusive) :
    ¬ (ClaimEntry.applyOutcome e
        (MeasurementContract.outcome m c) note).record.meetsPublicationTierGate := by
  rw [h_outcome]
  exact inconclusive_entry_does_not_meet_tier_gate e note

-- ---------------------------------------------------------------------------
-- 10. Concrete pipelines — computed outcomes, not assumed
-- ---------------------------------------------------------------------------

/-- **Full falsification pipeline (PFEntropy)**: The hostile PFEntropy
    measurement (0.20 ± 0.005) is run through the PFEntropy T³ contract.
    The `outcome` function computes `Falsified`.  Applying that computed
    outcome to the PFEntropy claim entry makes it NOT meet the tier gate.

    This is the computed falsification: measurement → outcome computation →
    claim update → rejection.  Nothing is assumed — the outcome is computed
    by `hostile_PFEntropy_falsified` and the rejection follows by
    `falsification_pipeline`. -/
theorem pfentropy_full_falsification_pipeline :
    ¬ (ClaimEntry.applyOutcome PFEntropyDecreasesT3Entry
        (MeasurementContract.outcome hostile_PFEntropy_measurement PFEntropy_T3_contract)
        "sandbox/T3_entropy_ratio_hostile: 0.20 ± 0.005").record.meetsPublicationTierGate := by
  apply falsification_pipeline hostile_PFEntropy_measurement PFEntropy_T3_contract
    PFEntropyDecreasesT3Entry
    "sandbox/T3_entropy_ratio_hostile: 0.20 ± 0.005"
  · exact hostile_PFEntropy_falsified

/-- **Full falsification pipeline (Gravity)**: The Lorentz-violating
    measurement (n = 1.02 ± 0.001) is run through the gravity optics
    contract.  The `outcome` function computes `Falsified`.  Applying that
    computed outcome to the gravity optics DERIVED claim entry makes it NOT
    meets the tier gate — even though the claim is DERIVED tier.

    Falsification overrides tier: a falsified DERIVED claim is still
    rejected.  Nothing is assumed — the outcome is computed by
    `lorentz_violating_n_falsified` and the rejection follows. -/
theorem gravity_full_falsification_pipeline :
    ¬ (ClaimEntry.applyOutcome weakFieldIndexFlatEntry
        (MeasurementContract.outcome lorentz_violating_n_measurement GravityOptics_contract)
        "hypothetical Lorentz violation: n = 1.02 ± 0.001").record.meetsPublicationTierGate := by
  apply falsification_pipeline lorentz_violating_n_measurement GravityOptics_contract
    weakFieldIndexFlatEntry
    "hypothetical Lorentz violation: n = 1.02 ± 0.001"
  · exact lorentz_violating_n_falsified

/-- **Full confirmation pipeline (Koide)**: The charged-lepton measurement
    (Q ≈ 0.66666 ± 0.00001) is run through the Koide contract.  The `outcome`
    function computes `Confirmed`.  Applying that computed outcome to the
    Koide DERIVED claim entry makes it meet the tier gate.

    This is the computed confirmation: measurement → outcome computation →
    claim update → promotion.  Nothing is assumed — the outcome is computed
    by `chargedLepton_Koide_confirmed` and the promotion follows by
    `confirmation_pipeline_derived`. -/
theorem koide_full_confirmation_pipeline :
    (ClaimEntry.applyOutcome koideQTwoThirdsEntry
        (MeasurementContract.outcome chargedLepton_Koide_measurement Koide_contract)
        "PDG charged lepton masses: Q = 0.66666 ± 0.00001").record.meetsPublicationTierGate := by
  apply confirmation_pipeline_derived chargedLepton_Koide_measurement Koide_contract
    koideQTwoThirdsEntry
    "PDG charged lepton masses: Q = 0.66666 ± 0.00001"
  · exact chargedLepton_Koide_confirmed
  · exact koide_entry_is_derived

/-- **Full confirmation pipeline (PFEntropy — confirming measurement)**: The
    example PFEntropy measurement (0.124 ± 0.005) is run through the
    PFEntropy T³ contract.  The `outcome` function computes `Confirmed`.
    However, the PFEntropy claim is CONDITIONAL tier, so even after
    confirmation it is NOT meet the tier gate — because `meetsPublicationTierGate` requires
    DERIVED or EMPIRICAL ≥ 0.90.

    This demonstrates the tier gate: a confirmed CONDITIONAL claim is still
    does not meet the tier gate.  The outcome is computed, the tier is checked, and the
    gate holds. -/
theorem pfentropy_confirmed_but_fails_tier_gate :
    ¬ (ClaimEntry.applyOutcome PFEntropyDecreasesT3Entry
        (MeasurementContract.outcome example_PFEntropy_measurement PFEntropy_T3_contract)
        "sandbox/T3_entropy_ratio_scan: 0.124 ± 0.005").record.meetsPublicationTierGate := by
  intro h
  unfold ClaimRecord.meetsPublicationTierGate at h
  obtain ⟨h_status, h_tier⟩ := h
  -- The outcome is Confirmed, so status = OK (this part is fine)
  -- But tier is CONDITIONAL, preserved by applyOutcome
  rw [ClaimEntry.applyOutcome_record] at h_tier
  rw [example_PFEntropy_confirmed] at h_tier
  -- After Confirmed, tier is preserved as CONDITIONAL
  have h_preserve : (MeasurementContract.applyOutcome PFEntropyDecreasesT3Entry.record
                      .Confirmed
                      "sandbox/T3_entropy_ratio_scan: 0.124 ± 0.005").tier
                    = PFEntropyDecreasesT3Entry.record.tier := by
    exact applyOutcome_preserves_tier _ _ _
  rw [h_preserve, pfentropy_entry_is_conditional] at h_tier
  -- h_tier : CONDITIONAL = DERIVED ∨ (CONDITIONAL = EMPIRICAL ∧ ...) — impossible
  simp at h_tier

-- ---------------------------------------------------------------------------
-- 11. Negative tests — premises are necessary, not decorative
-- ---------------------------------------------------------------------------

/-- **Negative test 1**: A `Measurement` whose `source` string claims PDG
    provenance does NOT gain any special status from the string.  The
    `meetsPublicationTierGate` predicate examines only `status` and `tier`,
    not the `source` field.  A free-form source string alone cannot create
    a tier-gate-passing entry.

    This test constructs a measurement with a convincing source string but
    applies a `.Falsified` outcome.  Despite the source saying "PDG
    confirmed", the entry does not meet the tier gate.  The source string
    is explanatory metadata, not provenance. -/
theorem source_string_alone_does_not_meet_tier_gate :
    ¬ (ClaimEntry.applyOutcome koideQTwoThirdsEntry .Falsified
        "PDG confirmed: Q = 0.66666 ± 0.00001 (fake source)").record.meetsPublicationTierGate := by
  exact falsified_entry_does_not_meet_tier_gate koideQTwoThirdsEntry
    "PDG confirmed: Q = 0.66666 ± 0.00001 (fake source)"

/-- **Negative provenance test**: changing only a measurement's free-form
    source label leaves its computed numeric outcome unchanged.  A source
    string is therefore neither a validation receipt nor a substitute for the
    `MeasurementProvenance` required by `ValidatedMeasurement`. -/
theorem koide_outcome_is_invariant_under_source_replacement :
    MeasurementContract.outcome
        (Measurement.withSource chargedLepton_Koide_measurement
          "forged external source")
        Koide_contract =
      MeasurementContract.outcome chargedLepton_Koide_measurement Koide_contract := by
  exact MeasurementContract.outcome_invariant_under_source_change
    chargedLepton_Koide_measurement "forged external source" Koide_contract

/-- **Negative test 2**: An `ARGUED` tier claim, even after a `.Confirmed`
    outcome with a PDG source string, does NOT meet the tier gate.  The tier
    gate requires `DERIVED` or `EMPIRICAL ≥ 0.90`.  No source string or
    confirmation can override the tier requirement. -/
theorem argued_tier_with_confirmed_and_source_does_not_meet_tier_gate :
    ¬ (ClaimEntry.applyOutcome weinbergRatioEntry .Confirmed
        "PDG on-shell sin²θ_W: 0.22310 ± 0.00010").record.meetsPublicationTierGate := by
  exact weinberg_claim_fails_tier_gate_even_if_confirmed

/-- **Negative test 3**: A `CONDITIONAL` tier claim, even after a computed
    `.Confirmed` outcome, does NOT meet the tier gate.  This is the
    PFEntropy case: the measurement confirms, the outcome is computed, but
    the tier gate holds because CONDITIONAL ≠ DERIVED. -/
theorem conditional_tier_with_computed_confirmation_does_not_meet_tier_gate :
    ¬ (ClaimEntry.applyOutcome PFEntropyDecreasesT3Entry
        (MeasurementContract.outcome example_PFEntropy_measurement PFEntropy_T3_contract)
        "sandbox/T3_entropy_ratio_scan: 0.124 ± 0.005").record.meetsPublicationTierGate := by
  exact pfentropy_confirmed_but_fails_tier_gate

/-- **Negative test 4**: A DERIVED claim with a computed `.Falsified` outcome
    does NOT meet the tier gate.  Falsification overrides tier: even a
    DERIVED claim is rejected when the measurement falsifies it.  The
    outcome is computed (not assumed), and the tier gate checks status first. -/
theorem derived_tier_with_computed_falsification_does_not_meet_tier_gate :
    ¬ (ClaimEntry.applyOutcome weakFieldIndexFlatEntry
        (MeasurementContract.outcome lorentz_violating_n_measurement GravityOptics_contract)
        "hypothetical Lorentz violation: n = 1.02 ± 0.001").record.meetsPublicationTierGate := by
  exact gravity_full_falsification_pipeline

/-- **Negative test 5**: The `contractsResolved` predicate is NOT vacuously
    true for a non-empty ledger with a missing claim.  If a contract
    references a claim name that doesn't exist in the ledger, the ledger
    does NOT resolve.  This is a structural test: the bridge matters. -/
theorem unresolved_contract_does_not_resolve :
    ¬ MeasurementLedger.contractsResolved
        (MeasurementLedger.empty.add
          { claimName := "nonexistent_claim"
            predictedValue := 0
            tolerance := 0
            tolerance_nonneg := by norm_num
            falsificationThreshold := 1
            falsification_nonneg := by norm_num
            tolerance_le_falsification := by norm_num })
        pfClaimLedger := by
  rw [MeasurementLedger.contractsResolved, MeasurementLedger.empty,
      MeasurementLedger.add]
  simp
  -- The ledger has no entry named "nonexistent_claim"
  -- Check all 13 entry names — none is "nonexistent_claim"
  decide

-- ---------------------------------------------------------------------------
-- 12. Unique-name invariant: value-level results (legacy, weak)
-- ---------------------------------------------------------------------------
--
-- Codex re-audit (2026-07-25, ledger `clg_5e44d7c916c6a0ee00978b73`)
-- flagged two remaining holds on the discarded-premise repair:
--
--   1. `contractsResolved` is existential and no unique-name invariant
--      exists.  `applyMeasurement` updates every same-named entry, so the
--      capstone is a name-level theorem rather than a one-to-one
--      contract-to-entry binding.
--   2. `ValidatedMeasurement` is caller-supplied local metadata but is not
--      a capstone input.  Hard-coded values and source text remain
--      externally unvalidated.
--
-- ⚠️ This section provides VALUE-LEVEL results only.  The `uniqueNames`
--    predicate checks value equality, which is satisfied by `[entry, entry]`.
--    These theorems do NOT close hold #1 / PFU-01.  The occurrence-level
--    repair is in §13 below, using the stronger `uniqueEntryNames`
--    (Nodup on the name list) and `uniqueContractNames` (Nodup on the
--    contract claim-name list).
--
-- Hold #2 (ValidatedMeasurement provenance) is NOT addressed here; it
-- requires structured provenance in the actual measurement pipeline and
-- remains open.

/-- **Value-level (legacy, weak)**: Under the `uniqueNames` invariant, any
    two entries sharing a name are equal **by value**.  This does NOT imply
    occurrence-level uniqueness: `[entry, entry]` satisfies `uniqueNames`
    because both quantified values are the same, yet the name appears at two
    positions.  Use `uniqueEntryNames` for occurrence-level results. -/
theorem ClaimLedger.uniqueNames_at_most_one
    (cl : ClaimLedger) (hUnique : cl.uniqueNames) (name : String)
    (e₁ e₂ : ClaimEntry) (h₁ : e₁ ∈ cl.entries) (h₂ : e₂ ∈ cl.entries)
    (hName : e₁.name = name) (hName' : e₂.name = name) : e₁ = e₂ := by
  have h := hUnique e₁ h₁ e₂ h₂
  exact h (by rw [hName, hName'])

/-- **Value-level (legacy, weak)**: Under `uniqueNames`, the entry selected
    by `contractsResolved` is equal by value to any other entry matching the
    contract's claim name.  This does NOT prove occurrence-level uniqueness;
    `[entry, entry]` satisfies `uniqueNames` but has two positions with the
    same name.  Use `uniqueEntryNames` for occurrence-level results. -/
theorem MeasurementLedger.resolvedEntry_unique
    (ml : MeasurementLedger) (cl : ClaimLedger) (c : MeasurementContract)
    (h_c_in_ml : c ∈ ml.contracts) (h_resolved : ml.contractsResolved cl)
    (hUnique : cl.uniqueNames)
    (e : ClaimEntry) (h_e_in : e ∈ cl.entries) (h_e_name : e.name = c.claimName) :
    e = ml.resolvedEntry cl c h_c_in_ml h_resolved := by
  let res := ml.resolvedEntry cl c h_c_in_ml h_resolved
  have h_res_in : res ∈ cl.entries :=
    MeasurementLedger.resolvedEntry_mem ml cl c h_c_in_ml h_resolved
  have h_res_name : res.name = c.claimName :=
    MeasurementLedger.resolvedEntry_name ml cl c h_c_in_ml h_resolved
  exact hUnique e h_e_in res h_res_in (by rw [h_e_name, h_res_name])

/-- `applyMeasurement` preserves entry names: every entry in the updated
    ledger has the same name as its pre-image in the original ledger.
    This is because `applyOutcome` preserves the name field. -/
theorem ClaimLedger.applyMeasurement_preserves_names
    (cl : ClaimLedger) (claimName : String) (o : MeasurementOutcome) (note : String)
    (e' : ClaimEntry) (h_e' : e' ∈ (cl.applyMeasurement claimName o note).entries) :
    ∃ e ∈ cl.entries, e'.name = e.name ∧
      (e.name = claimName → e' = ClaimEntry.applyOutcome e o note) ∧
      (e.name ≠ claimName → e' = e) := by
  -- applyMeasurement is entries.map (fun e => if e.name = claimName then ... else e)
  simp only [ClaimLedger.applyMeasurement, List.mem_map] at h_e'
  obtain ⟨e, h_e_in, h_eq⟩ := h_e'
  refine ⟨e, h_e_in, ?_, ?_, ?_⟩
  · -- e'.name = e.name in both branches
    by_cases heq : e.name = claimName
    · -- matched branch: e' = applyOutcome e o note, name preserved
      simp [heq] at h_eq
      rw [← h_eq, ClaimEntry.applyOutcome_name]
    · -- non-matched branch: e' = e
      simp [heq] at h_eq
      rw [← h_eq]
  · intro h_match
    simp [h_match] at h_eq
    rw [← h_eq]
  · intro h_nomatch
    simp [h_nomatch] at h_eq
    rw [← h_eq]

/-- **Value-level uniqueness (legacy, weak)**: Under the `uniqueNames`
    invariant (value equality, NOT occurrence uniqueness), applying a
    measurement outcome to the ledger produces a ledger in which *at most
    one* entry has any given name **by value**.

    ⚠️ **This is a value-level compatibility result, NOT a one-to-one
    binding theorem.** The `uniqueNames` predicate checks value equality,
    which is satisfied by `[entry, entry]` (two occurrences of the same
    value).  The occurrence-level repair is
    `applyMeasurement_preserves_names_and_updates_one`, which uses the
    stronger `uniqueEntryNames` (Nodup on the name list) and proves
    index-level update semantics.

    This theorem is retained for backward compatibility with existing
    proofs that only need value-level uniqueness.  It does NOT close
    Codex hold PFU-01; the occurrence-level capstone
    `confirmed_derived_claim_occurrence_unique_tier_gate_pass` addresses
    that hold, subject to final revision-bound audit. -/
theorem ClaimLedger.applyMeasurement_unique_names
    (cl : ClaimLedger) (claimName : String) (o : MeasurementOutcome) (note : String)
    (hUnique : cl.uniqueNames) :
    (cl.applyMeasurement claimName o note).uniqueNames := by
  intro e₁' h₁' e₂' h₂' h_name_eq
  -- Both e₁' and e₂' come from pre-images in cl.entries with the same name.
  obtain ⟨e₁, h_e₁_in, h_e₁_name, h_e₁_match, h_e₁_nomatch⟩ :=
    ClaimLedger.applyMeasurement_preserves_names cl claimName o note e₁' h₁'
  obtain ⟨e₂, h_e₂_in, h_e₂_name, h_e₂_match, h_e₂_nomatch⟩ :=
    ClaimLedger.applyMeasurement_preserves_names cl claimName o note e₂' h₂'
  -- e₁'.name = e₁.name and e₂'.name = e₂.name, and e₁'.name = e₂'.name
  -- so e₁.name = e₂.name.  By uniqueNames, e₁ = e₂.
  have h_names : e₁.name = e₂.name := by
    rw [← h_e₁_name, ← h_e₂_name, h_name_eq]
  have h_e₁_eq_e₂ : e₁ = e₂ := hUnique e₁ h_e₁_in e₂ h_e₂_in h_names
  -- Now e₁' and e₂' are both derived from the same pre-image e₁ = e₂.
  subst h_e₁_eq_e₂
  by_cases heq : e₁.name = claimName
  · -- Both e₁' and e₂' are applyOutcome e₁ o note, so they're equal.
    rw [h_e₁_match heq, h_e₂_match heq]
  · -- Both e₁' and e₂' are e₁ itself, so they're equal.
    rw [h_e₁_nomatch heq, h_e₂_nomatch heq]

/-- **Value-level capstone (legacy, weak)**: Under the `uniqueNames`
    invariant (value equality), applying a computed `.Confirmed` outcome
    to a `DERIVED` claim produces a ledger in which there is *at most one*
    entry with the contract's claim name that meets the publication tier
    gate **by value**.

    ⚠️ **This is a value-level compatibility result, NOT the occurrence-level
    capstone.**  The `uniqueNames` predicate is satisfied by `[entry, entry]`,
    so this theorem does not prove occurrence-level one-to-one binding.

    The occurrence-level capstone that addresses Codex hold PFU-01 is
    `confirmed_derived_claim_occurrence_unique_tier_gate_pass`, which
    requires the stronger `uniqueEntryNames` and `uniqueContractNames`
    premises and proves exact-one entry count, exact-one contract count,
    and pairwise uniqueness.  Closure of PFU-01 is subject to final
    revision-bound audit.

    - **Existence** follows from the original bridge theorem
      `confirmed_derived_claim_meets_tier_gate` (which does not require
      `uniqueNames`).
    - **Uniqueness** follows from `applyMeasurement_unique_names`: the
      updated ledger has unique names, so at most one entry has name =
      `c.claimName`, hence at most one can meet the gate. -/
theorem confirmed_derived_claim_unique_tier_gate_pass
    (cl : ClaimLedger) (ml : MeasurementLedger)
    (m : Measurement) (c : MeasurementContract) (note : String)
    (h_c_in_ml : c ∈ ml.contracts)
    (h_resolved : ml.contractsResolved cl)
    (h_unique : cl.uniqueNames)
    (h_outcome : MeasurementContract.outcome m c = .Confirmed)
    (h_tier : ∀ e ∈ cl.entries, e.name = c.claimName → e.record.tier = .DERIVED) :
    -- Existence: at least one entry passes.
    (∃ e' ∈ (cl.applyMeasurement c.claimName
               (MeasurementContract.outcome m c) note).entries,
       e'.name = c.claimName ∧ e'.record.meetsPublicationTierGate) ∧
    -- Uniqueness: no two distinct entries both pass.
    (∀ e₁ ∈ (cl.applyMeasurement c.claimName
               (MeasurementContract.outcome m c) note).entries,
     ∀ e₂ ∈ (cl.applyMeasurement c.claimName
               (MeasurementContract.outcome m c) note).entries,
       e₁.name = c.claimName → e₂.name = c.claimName →
       e₁.record.meetsPublicationTierGate → e₂.record.meetsPublicationTierGate →
       e₁ = e₂) := by
  refine ⟨?_, ?_⟩
  · -- Existence: from the original bridge theorem (no uniqueNames needed)
    exact confirmed_derived_claim_meets_tier_gate cl ml m c note
      h_c_in_ml h_resolved h_outcome h_tier
  · -- Uniqueness: the updated ledger has unique names, so any two entries
    -- with the same name are equal.
    have h_unique' :
        (cl.applyMeasurement c.claimName
           (MeasurementContract.outcome m c) note).uniqueNames := by
      apply ClaimLedger.applyMeasurement_unique_names
      · exact h_unique
    intro e₁ h₁ e₂ h₂ h_name₁ h_name₂ h_gate₁ h_gate₂
    exact h_unique' e₁ h₁ e₂ h₂
      (by rw [h_name₁, h_name₂])

-- ---------------------------------------------------------------------------
-- 13. Occurrence-level repair (Codex PFU-01..PFU-04, 2026-07-30)
-- ---------------------------------------------------------------------------
--
-- Codex re-audit `clg_1b946d7211000490825d6aa6` identified that the old
-- `uniqueNames` predicate checks value equality, not occurrence uniqueness.
-- `[entry, entry]` satisfies it because both quantified values are the same.
-- The repair uses `uniqueEntryNames` (Nodup on the name list) which is
-- occurrence-level: no two positions share a name.
--
-- This section adds:
--   - exactly-one-count for resolved contracts (PFU-02)
--   - applyMeasurement applies the outcome at exactly one matching occurrence (PFU-02/PFU-03)
--   - the capstone restated with `uniqueEntryNames` (PFU-01)
--   - negative fixtures for [entry, entry], two distinct same-name entries,
--     and duplicate contract occurrences (PFU-05)

/-- Under `uniqueEntryNames`, if an entry with the given name exists, the
    filter of entries matching that name has length exactly 1.  This is the
    occurrence-level count theorem: not just "all matching values are equal"
    but "there is exactly one matching position."  Proved by induction. -/
theorem ClaimLedger.exactly_one_matching_entry
    (cl : ClaimLedger) (hUnique : cl.uniqueEntryNames)
    (name : String) (h_exists : ∃ e ∈ cl.entries, e.name = name) :
    (cl.entries.filter (fun e => e.name = name)).length = 1 := by
  -- General helper by induction on the list
  have helper : ∀ (l : List ClaimEntry) (target : String),
      (l.map ClaimEntry.name).Nodup →
      (∃ e ∈ l, e.name = target) →
      (l.filter (fun e => e.name = target)).length = 1 := by
    intro l target
    induction l with
    | nil => intro _ h; exact absurd h (by simp)
    | cons x xs ih =>
      intro hnodup hexists
      rw [List.map_cons, List.nodup_cons] at hnodup
      obtain ⟨hfx_notin, hxs_nodup⟩ := hnodup
      by_cases hxeq : x.name = target
      · -- x matches. No element in xs matches (from Nodup: x.name ∉ xs.map name).
        have hno_match : ∀ e ∈ xs, e.name ≠ target := by
          intro e he hename
          have hmem : target ∈ xs.map ClaimEntry.name := by
            rw [List.mem_map]; exact ⟨e, he, hename⟩
          rw [← hxeq] at hmem
          exact absurd hmem hfx_notin
        have hfilter_nil : (xs.filter (fun e => e.name = target)) = [] := by
          clear ih hexists hfx_notin hxs_nodup
          induction xs with
          | nil => rfl
          | cons y ys ih_filter =>
            by_cases hyeq : y.name = target
            · exact absurd hyeq (hno_match y (by simp))
            · simp [hyeq]
              intro e he hename
              exact hno_match e (List.mem_cons_of_mem _ he) hename
        simp [hxeq, List.filter_cons, hfilter_nil]
      · -- x doesn't match. The matching entry is in xs.
        have hexists_xs : ∃ e ∈ xs, e.name = target := by
          obtain ⟨e, he, hename⟩ := hexists
          simp only [List.mem_cons] at he
          rcases he with rfl | he
          · simp [hxeq] at hename
          · exact ⟨e, he, hename⟩
        simp [hxeq, List.filter_cons]
        exact ih hxs_nodup hexists_xs
  exact helper cl.entries name hUnique h_exists

/-- Under `uniqueEntryNames`, `applyMeasurement` preserves the name list
    (so `uniqueEntryNames` is preserved) and updates exactly the matching
    position while leaving every other position unchanged.

    This is the occurrence-level update theorem.  It states three things:
    1. Exactly one entry in the original ledger matches `claimName`
       (filter length = 1).
    2. The updated ledger also has `uniqueEntryNames` (names are preserved).
    3. **Index-level update semantics**: for every index `i` into the
       entry list, if the original entry at `i` matches `claimName` then
       the updated entry at `i` is `applyOutcome` of it (and its name is
       preserved); if not, the updated entry at `i` is identical to the
       original.  Combined with (1), exactly one index is updated. -/
theorem ClaimLedger.applyMeasurement_preserves_names_and_updates_one
    (cl : ClaimLedger) (claimName : String) (o : MeasurementOutcome) (note : String)
    (hUnique : cl.uniqueEntryNames)
    (h_exists : ∃ e ∈ cl.entries, e.name = claimName) :
    -- Exactly one entry matches the claim name
    (cl.entries.filter (fun e => e.name = claimName)).length = 1 ∧
    -- The updated ledger also has unique entry names (names preserved)
    (cl.applyMeasurement claimName o note).uniqueEntryNames ∧
    -- Index-level: every position is either updated (name matches) or unchanged.
    -- The updated list has the same length (applyMeasurement_length), so
    -- indices are shared.
    ∀ (i : Nat) (h_i : i < cl.entries.length),
      (cl.entries.get ⟨i, h_i⟩).name = claimName ∧
        (cl.applyMeasurement claimName o note).entries.get ⟨i, cl.applyMeasurement_length claimName o note ▸ h_i⟩ =
          ClaimEntry.applyOutcome (cl.entries.get ⟨i, h_i⟩) o note ∧
        ((cl.applyMeasurement claimName o note).entries.get ⟨i, cl.applyMeasurement_length claimName o note ▸ h_i⟩).name = claimName
      ∨
      (cl.entries.get ⟨i, h_i⟩).name ≠ claimName ∧
        (cl.applyMeasurement claimName o note).entries.get ⟨i, cl.applyMeasurement_length claimName o note ▸ h_i⟩ =
          cl.entries.get ⟨i, h_i⟩ := by
  refine ⟨?_, ?_, ?_⟩
  · exact cl.exactly_one_matching_entry hUnique claimName h_exists
  · -- applyMeasurement preserves names, so Nodup is preserved
    -- The name list of the updated ledger equals the name list of the original
    have h_names_preserved :
        (cl.applyMeasurement claimName o note).entries.map ClaimEntry.name =
        cl.entries.map ClaimEntry.name := by
      simp only [ClaimLedger.applyMeasurement, List.map_map]
      rw [show (ClaimEntry.name ∘ fun e => if e.name = claimName then ClaimEntry.applyOutcome e o note else e) = ClaimEntry.name from by
        funext e
        by_cases heq : e.name = claimName
        · simp [heq, ClaimEntry.applyOutcome_name, Function.comp]
        · simp [heq, Function.comp]]
    rw [uniqueEntryNames, h_names_preserved]
    exact hUnique
  · -- Index-level update semantics: applyMeasurement is List.map, so
    -- updated[i] = if orig[i].name = claimName then applyOutcome else orig[i]
    intro i h_i
    have h_len : (cl.applyMeasurement claimName o note).entries.length = cl.entries.length := by
      exact cl.applyMeasurement_length claimName o note
    by_cases heq : (cl.entries.get ⟨i, h_i⟩).name = claimName
    · -- Name matches: updated[i] = applyOutcome orig[i], name preserved
      left
      have h_get : (cl.applyMeasurement claimName o note).entries.get ⟨i, h_len ▸ h_i⟩ =
                   (cl.entries.get ⟨i, h_i⟩).applyOutcome o note := by
        unfold ClaimLedger.applyMeasurement
        -- Convert heq to getElem form
        have heq_elem : cl.entries[i].name = claimName := by
          have : cl.entries.get ⟨i, h_i⟩ = cl.entries[i] := by simp
          rw [← this]; exact heq
        simp [h_len, heq_elem]
      refine ⟨heq, h_get, ?_⟩
      rw [h_get, ClaimEntry.applyOutcome_name, heq]
    · -- Name doesn't match: updated[i] = orig[i]
      right
      have h_get : (cl.applyMeasurement claimName o note).entries.get ⟨i, h_len ▸ h_i⟩ =
                   cl.entries.get ⟨i, h_i⟩ := by
        unfold ClaimLedger.applyMeasurement
        have heq_elem : ¬ cl.entries[i].name = claimName := by
          have : cl.entries.get ⟨i, h_i⟩ = cl.entries[i] := by simp
          rw [← this]; exact heq
        simp [h_len, heq_elem]
      refine ⟨heq, h_get⟩

/-- **Capstone (occurrence-level)**: Under `uniqueEntryNames`,
    `contractsResolved`, and `uniqueContractNames`, applying a computed
    `.Confirmed` outcome to a `DERIVED` claim produces a ledger in which
    there is *exactly one* entry with the contract's claim name that meets
    the publication tier gate, the matching-entry count is exactly 1, and
    the matching-contract count is exactly 1.

    This replaces the value-level capstone
    `confirmed_derived_claim_unique_tier_gate_pass` with the
    occurrence-level version.  The existence proof reuses the original
    bridge theorem.  The entry count and uniqueness use `uniqueEntryNames`
    (Nodup on the name list), which is strictly stronger than
    `uniqueNames`.  The contract count uses `uniqueContractNames`
    (Nodup on the contract claim-name list), which is consumed here as a
    material premise — not merely named in documentation. -/
theorem confirmed_derived_claim_occurrence_unique_tier_gate_pass
    (cl : ClaimLedger) (ml : MeasurementLedger)
    (m : Measurement) (c : MeasurementContract) (note : String)
    (h_c_in_ml : c ∈ ml.contracts)
    (h_resolved : ml.contractsResolved cl)
    (h_unique : cl.uniqueEntryNames)
    (h_contract_unique : ml.uniqueContractNames)
    (h_outcome : MeasurementContract.outcome m c = .Confirmed)
    (h_tier : ∀ e ∈ cl.entries, e.name = c.claimName → e.record.tier = .DERIVED) :
    -- Existence: at least one entry passes.
    (∃ e' ∈ (cl.applyMeasurement c.claimName
               (MeasurementContract.outcome m c) note).entries,
       e'.name = c.claimName ∧ e'.record.meetsPublicationTierGate) ∧
    -- Entry count: exactly one entry in the original ledger matches the claim name.
    (cl.entries.filter (fun e => e.name = c.claimName)).length = 1 ∧
    -- Contract count: exactly one contract in the measurement ledger has this claim name.
    (ml.contracts.filter (fun c' => c'.claimName = c.claimName)).length = 1 ∧
    -- Uniqueness: no two distinct entries both pass.
    (∀ e₁ ∈ (cl.applyMeasurement c.claimName
               (MeasurementContract.outcome m c) note).entries,
     ∀ e₂ ∈ (cl.applyMeasurement c.claimName
               (MeasurementContract.outcome m c) note).entries,
       e₁.name = c.claimName → e₂.name = c.claimName →
       e₁.record.meetsPublicationTierGate → e₂.record.meetsPublicationTierGate →
       e₁ = e₂) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- Existence: from the original bridge theorem (no uniqueNames needed)
    exact confirmed_derived_claim_meets_tier_gate cl ml m c note
      h_c_in_ml h_resolved h_outcome h_tier
  · -- Entry count: exactly one matching entry (from uniqueEntryNames + contractsResolved)
    have h_exists : ∃ e ∈ cl.entries, e.name = c.claimName := by
      obtain ⟨e, h_e_in, h_e_name⟩ := h_resolved c h_c_in_ml
      exact ⟨e, h_e_in, h_e_name⟩
    exact cl.exactly_one_matching_entry h_unique c.claimName h_exists
  · -- Contract count: exactly one matching contract (from uniqueContractNames + h_c_in_ml)
    have h_contract_exists : ∃ c' ∈ ml.contracts, c'.claimName = c.claimName := by
      exact ⟨c, h_c_in_ml, rfl⟩
    exact MeasurementLedger.exactly_one_matching_contract
      ml h_contract_unique c.claimName h_contract_exists
  · -- Uniqueness: the updated ledger has uniqueEntryNames (names preserved)
    have h_unique' :
        (cl.applyMeasurement c.claimName
           (MeasurementContract.outcome m c) note).uniqueEntryNames := by
      have h_exists : ∃ e ∈ cl.entries, e.name = c.claimName := by
        obtain ⟨e, h_e_in, h_e_name⟩ := h_resolved c h_c_in_ml
        exact ⟨e, h_e_in, h_e_name⟩
      exact (cl.applyMeasurement_preserves_names_and_updates_one c.claimName
        (MeasurementContract.outcome m c) note h_unique h_exists).2.1
    -- uniqueEntryNames → uniqueNames (bridge lemma, applied to updated ledger)
    let cl' := cl.applyMeasurement c.claimName (MeasurementContract.outcome m c) note
    have h_weak := cl'.uniqueEntryNames_implies_uniqueNames h_unique'
    intro e₁ h₁ e₂ h₂ h_name₁ h_name₂ h_gate₁ h_gate₂
    exact h_weak e₁ h₁ e₂ h₂ (by rw [h_name₁, h_name₂])

-- ---------------------------------------------------------------------------
-- 14. Negative fixtures (Codex PFU-05)
-- ---------------------------------------------------------------------------

/-- **Negative fixture 1**: A ledger `[entry, entry]` (same value at two
    positions) does NOT satisfy `uniqueEntryNames`.  This is the core
    defect: the weak `uniqueNames` passes but the strong
    `uniqueEntryNames` correctly rejects it. -/
theorem duplicate_entry_ledger_fails_uniqueEntryNames :
    ¬ ({ entries := [onePlusOneEntry, onePlusOneEntry] } : ClaimLedger).uniqueEntryNames := by
  intro h
  simp only [ClaimLedger.uniqueEntryNames, onePlusOneEntry,
             List.map_cons, List.map_nil] at h
  exact absurd h (by decide)

/-- **Negative fixture 2**: Two distinct entries with the same name do NOT
    satisfy `uniqueEntryNames`.  We construct two entries with the same
    name `"dup"` but different propositions/proofs. -/
theorem two_distinct_same_name_entries_fail_uniqueEntryNames :
    ¬ ({ entries := [ClaimEntry.mk "dup" (1 + 1 = 2 : Prop)
                       (ClaimRecord.derived one_plus_one_eq_two "evidence1" "falsifier1"),
                     ClaimEntry.mk "dup" (0 ≤ 1 : Prop)
                       (ClaimRecord.derived zero_le_one "evidence2" "falsifier2")] } : ClaimLedger).uniqueEntryNames := by
  intro h
  simp only [ClaimLedger.uniqueEntryNames, List.map_cons, List.map_nil] at h
  -- The name list is ["dup", "dup"] which is not Nodup
  exact absurd h (by decide)

/-- **Negative fixture 3**: A measurement ledger with duplicate contracts
    (same `claimName` at two positions) does NOT satisfy
    `uniqueContractNames`.  This is the contract-level analog of the
    entry-level defect. -/
theorem duplicate_contract_ledger_fails_uniqueContractNames :
    ¬ (MeasurementLedger.empty.add
        { claimName := "koide_Q_two_thirds"
          predictedValue := 2/3
          tolerance := 0.001
          tolerance_nonneg := by norm_num
          falsificationThreshold := 0.01
          falsification_nonneg := by norm_num
          tolerance_le_falsification := by norm_num } |>.add
        { claimName := "koide_Q_two_thirds"
          predictedValue := 2/3
          tolerance := 0.001
          tolerance_nonneg := by norm_num
          falsificationThreshold := 0.01
          falsification_nonneg := by norm_num
          tolerance_le_falsification := by norm_num }).uniqueContractNames := by
  intro h
  simp only [MeasurementLedger.uniqueContractNames, MeasurementLedger.empty,
             MeasurementLedger.add, List.map_cons, List.map_nil] at h
  -- The claim name list is ["koide_Q_two_thirds", "koide_Q_two_thirds"]
  -- which is not Nodup
  exact absurd h (by decide)

/-- **Negative fixture 4**: `contractsResolved` does NOT imply
    `uniqueContractNames`.  A ledger with two contracts pointing at the
    same claim resolves (both find the entry) but has duplicate contract
    names.  This shows the two predicates are independent. -/
theorem contractsResolved_does_not_imply_uniqueContractNames :
    ∃ (ml : MeasurementLedger) (cl : ClaimLedger),
      ml.contractsResolved cl ∧ ¬ ml.uniqueContractNames := by
  let dupContract : MeasurementContract :=
    { claimName := "koide_Q_two_thirds"
      predictedValue := 2/3
      tolerance := 0.001
      tolerance_nonneg := by norm_num
      falsificationThreshold := 0.01
      falsification_nonneg := by norm_num
      tolerance_le_falsification := by norm_num }
  refine ⟨MeasurementLedger.empty.add dupContract |>.add dupContract,
          pfClaimLedger, ?_, ?_⟩
  · -- Both contracts resolve (both find koideQTwoThirdsEntry)
    rw [MeasurementLedger.contractsResolved, MeasurementLedger.empty,
        MeasurementLedger.add]
    intro c hc
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
    -- hc : c = dupContract ∨ c ∈ ({ contracts := [] }.add dupContract).contracts
    have hc' : c = dupContract := by
      cases hc with
      | inl h => exact h
      | inr h =>
        simp only [MeasurementLedger.empty, MeasurementLedger.add] at h
        cases h with
        | head _ => rfl
        | tail _ h' => nomatch h'
    rw [hc']
    exact ⟨koideQTwoThirdsEntry, koide_entry_in_ledger, rfl⟩
  · -- But uniqueContractNames fails
    intro h
    simp only [MeasurementLedger.uniqueContractNames, MeasurementLedger.empty,
               MeasurementLedger.add, List.map_cons, List.map_nil] at h
    exact absurd h (by decide)

end PfLean
