/-
  PfLean.MeasurementLedger — Linking Measurement Contracts to the Claim Ledger
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-07-24

  A `MeasurementLedger` is a list of `MeasurementContract`s.  Its key
  consistency property is `contractsResolved`: every contract's `claimName`
  must name an existing entry in a given `ClaimLedger`.

  This module defines the structure, the consistency predicate, a concrete
  `pfMeasurementLedger` (the single contract that currently resolves), and
  a `pfMeasurementLedger_full` (all 4 contracts) whose resolution gap
  exposes the 3 claim names not yet in `pfClaimLedger`.
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

/-- The minimal measurement ledger: just the PFEntropy T³ contract.
    This is the only contract whose `claimName` (`PFEntropy_decreases_T3`)
    currently exists in `pfClaimLedger`. -/
noncomputable def pfMeasurementLedger : MeasurementLedger :=
  MeasurementLedger.empty.add PFEntropy_T3_contract

/-- The minimal ledger resolves against `pfClaimLedger`. -/
theorem pfMeasurementLedger_resolved :
    MeasurementLedger.contractsResolved pfMeasurementLedger pfClaimLedger := by
  rw [MeasurementLedger.contractsResolved, pfMeasurementLedger,
      MeasurementLedger.empty, MeasurementLedger.add]
  simp [PFEntropy_T3_contract]
  -- The PFEntropy_decreases_T3 entry exists in pfClaimLedger
  native_decide

/-- The full measurement ledger: all 4 contracts.
    NOTE: `weinberg_ratio`, `koide_Q_two_thirds`, and `weakFieldIndex_flat`
    are NOT yet in `pfClaimLedger`.  This ledger does NOT resolve until
    those entries are added to `ClaimLedgerRegistry`. -/
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

/-- The full ledger references 4 claim names, one of which is not yet in
    `pfClaimLedger`.  This theorem documents the gap: the `weinberg_ratio`
    claim name does not appear in `pfClaimLedger.entries`. -/
theorem pfMeasurementLedger_full_gap :
    ∃ c ∈ pfMeasurementLedger_full.contracts,
      ∀ e ∈ pfClaimLedger.entries, e.name ≠ c.claimName := by
  decide

end PfLean
