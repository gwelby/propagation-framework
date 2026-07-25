/-
  PfLean.ClaimLedgerRegistry — Real PF Theorems in the Claim Ledger
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-07-23

  This module wires selected machine-verified PF theorems into the
  `PfLean.ClaimLedger` infrastructure.  It is the first real registry of
  claims with epistemic tiers, confidence intervals, evidence strings,
  falsifiers, and dependency links.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.ClaimLedger
import PfLean.PFCore
import PfLean.SO3DoubleCover
import PfLean.TopologicalWeights
import PfLean.Entropy
import PfLean.WeinbergAngle
import PfLean.KoideGeometry
import PfLean.GravityOptics

namespace PfLean

-- ---------------------------------------------------------------------------
-- 1. Topological / double-cover claims
-- ---------------------------------------------------------------------------

def quatToSO3KerEntry : ClaimEntry :=
  let P : Prop := ∀ q : UnitQuaternion, quatToSO3 q = 1 ↔ q = 1 ∨ q = -1
  let h : P := quatToSO3_ker
  ClaimEntry.mk "quatToSO3_ker" P
    (ClaimRecord.derived h
      "SO3DoubleCover.lean: quaternion-to-SO(3) kernel is exactly {±1}"
      "antipodal quaternions do not map to the same rotation")

def atMostTwoClosureOrdersEntry : ClaimEntry :=
  let P : Prop := ∀ (g : UnitQuaternion), g = 1 ∨ g = -1 →
    closureOrder g = 1 ∨ closureOrder g = 2
  let h : P := at_most_two_closure_orders
  ClaimEntry.mk "at_most_two_closure_orders" P
    (ClaimRecord.derived h
      "TopologicalWeights.lean: only closure orders 1 and 2 are forced by the kernel"
      "unit-quaternion kernel contains an element of order other than 1 or 2")

def kernelClosureOrdersEntry : ClaimEntry :=
  let P : Prop := ∀ g : UnitQuaternion, quatToSO3 g = 1 →
    closureOrder g = 1 ∨ closureOrder g = 2
  let h : P := kernel_closure_orders
  ClaimEntry.mk "kernel_closure_orders" P
    (ClaimRecord.derived h
      "TopologicalWeights.lean: kernel elements have closure order 1 or 2"
      "trivial action on SO(3) does not imply closure order in {1,2}"
      ["quatToSO3_ker", "at_most_two_closure_orders"])

def topologicalAvailabilityEntry : ClaimEntry :=
  let P : Prop := ∀ g : UnitQuaternion, quatToSO3 g = 1 →
    closureOrder g = 1 ∨ closureOrder g = 2
  let h : P := topological_availability
  ClaimEntry.mk "topological_availability" P
    (ClaimRecord.derived h
      "TopologicalWeights.lean: topological availability theorem for (2,1) weights"
      "SO(3) kernel admits a closure order outside {1,2}"
      ["kernel_closure_orders"])

-- ---------------------------------------------------------------------------
-- 2. PFCore / state-update claims
-- ---------------------------------------------------------------------------

def TFullDecompositionEntry : ClaimEntry :=
  let P : Prop := ∀ (dt α : ℝ) (x : Fin 3 → ℝ) (n : ℕ) (i : Fin 3),
    (T_update dt α)^[n] x i =
      (1 + dt * (-1 + 2 * α)) ^ n * (P0 x i) +
      (1 + dt * (-1 - α)) ^ n * (Q x i)
  let h : P := T_full_decomposition
  ClaimEntry.mk "T_full_decomposition" P
    (ClaimRecord.derived h
      "PFCore.lean: T^n preserves the P₀/Q decomposition for arbitrary dt, α, n"
      "state update does not split into uniform and residue eigenmodes")

def QSumZeroEntry : ClaimEntry :=
  let P : Prop := ∀ x : Fin 3 → ℝ, Q x 0 + Q x 1 + Q x 2 = 0
  let h : P := Q_sum_zero
  ClaimEntry.mk "Q_sum_zero" P
    (ClaimRecord.derived h
      "PFCore.lean: the residue projection Q(x) always sums to zero"
      "residue vectors have non-zero total sum")

-- ---------------------------------------------------------------------------
-- 3. PF Entropy claims
-- ---------------------------------------------------------------------------

def P0QDotZeroEntry : ClaimEntry :=
  let P : Prop := ∀ x : Fin 3 → ℝ,
    (P0 x 0) * (Q x 0) + (P0 x 1) * (Q x 1) + (P0 x 2) * (Q x 2) = 0
  let h : P := P0_Q_dot_zero
  ClaimEntry.mk "P0_Q_dot_zero" P
    (ClaimRecord.derived h
      "Entropy.lean: P₀ and Q are orthogonal in the Euclidean inner product"
      "uniform and residue components are not orthogonal")

def fullNormPythagoreanEntry : ClaimEntry :=
  let P : Prop := ∀ x : Fin 3 → ℝ,
    (full_norm x) ^ 2 = (P0 x 0) ^ 2 + (P0 x 1) ^ 2 + (P0 x 2) ^ 2
                       + (PFEntropy x) ^ 2
  let h : P := full_norm_Pythagorean
  ClaimEntry.mk "full_norm_Pythagorean" P
    (ClaimRecord.derived h
      "Entropy.lean: full norm² = P₀ norm² + PF Entropy²"
      "orthogonal decomposition of state space fails"
      ["P0_Q_dot_zero", "Q_sum_zero"])

/-- The kernel-level algebraic identity for the defined `T3` operator.  This
    entry deliberately makes no physical-transfer assertion. -/
def PFEntropyT3FormalIdentityEntry : ClaimEntry :=
  let P : Prop := ∀ x : Fin 3 → ℝ, PFEntropy (T3 x) = (1 / 8) * PFEntropy x
  let h : P := PFEntropy_decreases_T3
  ClaimEntry.mk "PFEntropy_T3_formal_identity" P
    (ClaimRecord.derived h
      "Entropy.lean: formal T³ algebraic identity only; no physical transfer is asserted"
      "the formal Entropy.lean identity fails"
      ["P0_Q_dot_zero", "Q_sum_zero"])

/-- A named, intentionally unproven bridge from the formal `T3` model to a
    selected physical observation.  No inhabitant is supplied in PfLean. -/
opaque PFEntropyT3PhysicalTransferPremise : Prop

/-- The physical reading is conditional on an explicit transfer premise; the
    formal identity alone does not establish that premise. -/
def PFEntropyT3PhysicalReading : Prop :=
  PFEntropyT3PhysicalTransferPremise →
    ∀ x : Fin 3 → ℝ, PFEntropy (T3 x) = (1 / 8) * PFEntropy x

theorem pfentropy_t3_physical_reading : PFEntropyT3PhysicalReading := by
  intro _ x
  exact PFEntropy_decreases_T3 x

/-- The physical interpretation of the T³ identity.  The named transfer
    premise is part of the proposition, so this CONDITIONAL row is distinct
    from `PFEntropyT3FormalIdentityEntry`. -/
def PFEntropyDecreasesT3Entry : ClaimEntry :=
  let P : Prop := PFEntropyT3PhysicalReading
  let h : P := pfentropy_t3_physical_reading
  ClaimEntry.mk "PFEntropy_decreases_T3" P
    (ClaimRecord.conditional h
      "Conditional physical reading: if PFEntropyT3PhysicalTransferPremise holds, the formal T³ identity applies"
      "the named physical-transfer premise or formal T³ identity fails"
      ["PFEntropy_T3_formal_identity"])

def fullNormT3StrictlyDecreasesEntry : ClaimEntry :=
  let P : Prop := ∀ x : Fin 3 → ℝ, PFEntropy x > 0 →
    full_norm (T3 x) < full_norm x
  let h : P := full_norm_T3_strictly_decreases
  ClaimEntry.mk "full_norm_T3_strictly_decreases" P
    (ClaimRecord.conditional h
      "Entropy.lean: J-I dynamics strictly decreases full Euclidean norm"
      "a non-uniform state has its full norm preserved under T³"
      ["full_norm_Pythagorean", "PFEntropy_decreases_T3"])

-- ---------------------------------------------------------------------------
-- 4. Weinberg / Koide / Gravity claims
-- ---------------------------------------------------------------------------

def weinbergRatioEntry : ClaimEntry :=
  let P : Prop := 22309 / 100000 < WeinbergRatio ∧ WeinbergRatio < 22311 / 100000
  let h : P := weinberg_ratio_bounds
  ClaimEntry.mk "weinberg_ratio" P
    (ClaimRecord.argued h
      "WeinbergAngle.lean: de Vries identity gives sin²θ_W ≈ 0.22310 (0.13σ PDG match)"
      "the Casimir root ratio does not match the measured Weinberg angle")

def koideQTwoThirdsEntry : ClaimEntry :=
  { name := "koide_Q_two_thirds"
    P := ∀ (a b c : ℝ), a > 0 → b > 0 → c > 0 →
      (KoideQ a b c = 2 / 3 ↔ a ^ 2 + b ^ 2 + c ^ 2 = 4 * (a * b + b * c + c * a))
    record := ClaimRecord.derived
      (fun a b c ha hb hc => @koide_Q_two_thirds_iff a b c ha hb hc)
      "KoideGeometry.lean: Q = 2/3 ↔ equal-strength geometric identity (exact, physical selection OPEN)"
      "three positive amplitudes satisfying the constraint do not yield Q = 2/3" }

def weakFieldIndexFlatEntry : ClaimEntry :=
  let P : Prop := weakFieldIndex 0 = 1
  let h : P := weakFieldIndex_flat
  ClaimEntry.mk "weakFieldIndex_flat" P
    (ClaimRecord.derived h
      "GravityOptics.lean: n(0) = 1 — flat-space refractive index is unity"
      "the weak-field metric null condition does not give n = 1 at Φ = 0")

-- ---------------------------------------------------------------------------
-- 5. The real PF claim ledger
-- ---------------------------------------------------------------------------

def pfClaimLedger : ClaimLedger :=
  ⟨[ fullNormT3StrictlyDecreasesEntry
   , PFEntropyT3FormalIdentityEntry
   , PFEntropyDecreasesT3Entry
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

theorem pfClaimLedger_wellFormed :
    pfClaimLedger.dependenciesResolved := by
  simp [pfClaimLedger, ClaimLedger.dependenciesResolved, ClaimEntry.dependencies,
        ClaimRecord.derived, ClaimRecord.conditional,
        fullNormT3StrictlyDecreasesEntry, PFEntropyT3FormalIdentityEntry,
        PFEntropyDecreasesT3Entry, fullNormPythagoreanEntry,
        P0QDotZeroEntry, QSumZeroEntry, TFullDecompositionEntry,
        topologicalAvailabilityEntry, kernelClosureOrdersEntry, atMostTwoClosureOrdersEntry,
        quatToSO3KerEntry, weinbergRatioEntry, koideQTwoThirdsEntry, weakFieldIndexFlatEntry]
  decide

end PfLean
