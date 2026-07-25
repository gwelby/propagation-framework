/-
  PfLean.MeasurementContract — Bridge Between Sandbox Measurements and Formal Claims
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-07-23

  This module provides the minimal machinery for a measurement to interact
  with a `ClaimRecord`:

  - `Measurement` carries a real value, a non-negative uncertainty, and a
    source string.
  - `MeasurementContract` links a claim name to a predicted observable value
    and two bands: a *tolerance* (inside = measurement confirms the claim)
    and a *falsification threshold* (outside = measurement falsifies the
    claim).  The inconclusive region lies between the two.
  - `MeasurementOutcome` is `Confirmed`, `Inconclusive`, or `Falsified`.
  - `MeasurementContract.applyOutcome` returns a new `ClaimRecord` with the
    status updated and the evidence string annotated.

  The design is intentionally two-sided and numeric for the first pass.
  One-sided (inequality) contracts and covariance-aware multi-dimensional
  contracts are natural extensions.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.ClaimLedger

namespace PfLean
open Classical

-- ---------------------------------------------------------------------------
-- 1. Measurement and contract types
-- ---------------------------------------------------------------------------

/-- A sandbox or experimental measurement. -/
structure Measurement where
  value : ℝ
  uncertainty : ℝ
  uncertainty_nonneg : 0 ≤ uncertainty
  source : String

/-- A contract between a formal claim and an observable. -/
structure MeasurementContract where
  claimName : String
  predictedValue : ℝ
  tolerance : ℝ
  tolerance_nonneg : 0 ≤ tolerance
  falsificationThreshold : ℝ
  falsification_nonneg : 0 ≤ falsificationThreshold
  tolerance_le_falsification : tolerance ≤ falsificationThreshold

-- ---------------------------------------------------------------------------
-- 2. Outcome and claim update
-- ---------------------------------------------------------------------------

/-- The result of comparing a measurement against a contract. -/
inductive MeasurementOutcome
  | Confirmed
  | Inconclusive
  | Falsified
  deriving DecidableEq, BEq, Repr

namespace MeasurementContract

/-- The measurement agrees with the prediction within tolerance + uncertainty. -/
def compatible (m : Measurement) (c : MeasurementContract) : Prop :=
  |m.value - c.predictedValue| ≤ m.uncertainty + c.tolerance

/-- The measurement deviates by more than falsificationThreshold + uncertainty. -/
def falsified (m : Measurement) (c : MeasurementContract) : Prop :=
  |m.value - c.predictedValue| > m.uncertainty + c.falsificationThreshold

/-- Decide the outcome, with falsification taking priority over confirmation. -/
noncomputable def outcome (m : Measurement) (c : MeasurementContract) : MeasurementOutcome :=
  if falsified m c then .Falsified
  else if compatible m c then .Confirmed
  else .Inconclusive

/-- Update a `ClaimRecord` according to the measurement outcome. -/
def applyOutcome {P : Prop} (cr : ClaimRecord P) (o : MeasurementOutcome)
    (measurementNote : String) : ClaimRecord P :=
  match o with
  | .Confirmed =>
      { proof := cr.proof
        tier := cr.tier
        status := .OK
        confidence := cr.confidence
        evidence := cr.evidence ++ " | measurement confirmed: " ++ measurementNote
        falsifier := cr.falsifier
        dependencies := cr.dependencies
        tier_bound := cr.tier_bound }
  | .Inconclusive =>
      { proof := cr.proof
        tier := cr.tier
        status := .HOLD
        confidence := cr.confidence
        evidence := cr.evidence ++ " | measurement inconclusive: " ++ measurementNote
        falsifier := cr.falsifier
        dependencies := cr.dependencies
        tier_bound := cr.tier_bound }
  | .Falsified =>
      { proof := cr.proof
        tier := cr.tier
        status := .NOGO
        confidence := cr.confidence
        evidence := cr.evidence ++ " | measurement falsified: " ++ measurementNote
        falsifier := cr.falsifier
        dependencies := cr.dependencies
        tier_bound := cr.tier_bound }

end MeasurementContract

-- ---------------------------------------------------------------------------
-- 2b. Outcome correctness — the outcome function computes what it claims
-- ---------------------------------------------------------------------------

/-- The outcome is `Falsified` if and only if the measurement falsifies the
    contract.  This is the correctness theorem for the falsification branch:
    it says `outcome` correctly identifies falsification. -/
theorem outcome_iff_falsified (m : Measurement) (c : MeasurementContract) :
    MeasurementContract.outcome m c = .Falsified ↔ MeasurementContract.falsified m c := by
  unfold MeasurementContract.outcome
  split_ifs with h_falsified h_compatible
  · exact ⟨fun _ => h_falsified, fun _ => rfl⟩
  · exact ⟨fun h => absurd h (by decide), fun hf => absurd hf h_falsified⟩
  · exact ⟨fun h => absurd h (by decide), fun hf => absurd hf h_falsified⟩

/-- The outcome is `Confirmed` if and only if the measurement is compatible
    and NOT falsified.  This is the correctness theorem for the confirmation
    branch: it says `outcome` correctly identifies confirmation, while
    respecting falsification priority. -/
theorem outcome_iff_confirmed (m : Measurement) (c : MeasurementContract) :
    MeasurementContract.outcome m c = .Confirmed ↔
    MeasurementContract.compatible m c ∧ ¬ MeasurementContract.falsified m c := by
  unfold MeasurementContract.outcome
  split_ifs with h_falsified h_compatible
  · exact ⟨fun h => absurd h (by decide), fun ⟨_, hf⟩ => absurd h_falsified hf⟩
  · exact ⟨fun _ => ⟨h_compatible, h_falsified⟩, fun _ => rfl⟩
  · exact ⟨fun h => absurd h (by decide), fun ⟨hc, _⟩ => absurd hc h_compatible⟩

/-- The outcome is `Inconclusive` if and only if the measurement is neither
    compatible nor falsified — it falls in the gap between tolerance and
    falsification threshold. -/
theorem outcome_iff_inconclusive (m : Measurement) (c : MeasurementContract) :
    MeasurementContract.outcome m c = .Inconclusive ↔
    ¬ MeasurementContract.compatible m c ∧ ¬ MeasurementContract.falsified m c := by
  unfold MeasurementContract.outcome
  split_ifs with h_falsified h_compatible
  · exact ⟨fun h => absurd h (by decide), fun ⟨_, hf⟩ => absurd h_falsified hf⟩
  · exact ⟨fun h => absurd h (by decide), fun ⟨hnc, _⟩ => absurd h_compatible hnc⟩
  · exact ⟨fun _ => ⟨h_compatible, h_falsified⟩, fun _ => rfl⟩

/-- If the outcome is `Confirmed`, then the measurement is not falsified.
    This is a direct corollary of `outcome_iff_confirmed`. -/
theorem confirmed_implies_not_falsified (m : Measurement) (c : MeasurementContract) :
    MeasurementContract.outcome m c = .Confirmed →
    ¬ MeasurementContract.falsified m c := by
  rw [outcome_iff_confirmed]
  exact fun ⟨_, hf⟩ => hf

/-- If the outcome is `Falsified`, then the measurement is not compatible.
    Falsification and confirmation are mutually exclusive: the falsification
    threshold is ≥ the tolerance, so any measurement within the compatible
    band cannot be in the falsification band. -/
theorem falsified_implies_not_compatible (m : Measurement) (c : MeasurementContract) :
    MeasurementContract.outcome m c = .Falsified →
    ¬ MeasurementContract.compatible m c := by
  rw [outcome_iff_falsified]
  intro hf hc
  -- falsified: |diff| > u + falsThreshold
  -- compatible: |diff| ≤ u + tolerance
  -- tolerance ≤ falsThreshold, so u + tolerance ≤ u + falsThreshold
  -- therefore |diff| ≤ u + falsThreshold, contradicting |diff| > u + falsThreshold
  have h_le : m.uncertainty + c.tolerance ≤ m.uncertainty + c.falsificationThreshold := by
    linarith [c.tolerance_le_falsification]
  have h_comp_abs : |m.value - c.predictedValue| ≤ m.uncertainty + c.falsificationThreshold :=
    le_trans hc h_le
  exact absurd hf (not_lt_of_ge h_comp_abs)

-- ---------------------------------------------------------------------------
-- 3. Example: PF entropy T³ ratio
-- ---------------------------------------------------------------------------

/-- The formal claim `PFEntropy_decreases_T3` predicts the ratio
    `PFEntropy(T3 x) / PFEntropy(x)` equals `1/8`. -/
noncomputable def PFEntropy_T3_contract : MeasurementContract :=
  { claimName := "PFEntropy_decreases_T3"
    predictedValue := (1 / 8 : ℝ)
    tolerance := (0.01 : ℝ)
    tolerance_nonneg := by norm_num
    falsificationThreshold := (0.05 : ℝ)
    falsification_nonneg := by norm_num
    tolerance_le_falsification := by norm_num }

/-- A sandbox scan observing the ratio `0.124 ± 0.005`. -/
noncomputable def example_PFEntropy_measurement : Measurement :=
  { value := (0.124 : ℝ)
    uncertainty := (0.005 : ℝ)
    uncertainty_nonneg := by norm_num
    source := "sandbox/T3_entropy_ratio_scan" }

/-- The example measurement confirms the contract. -/
theorem example_PFEntropy_confirmed :
    (MeasurementContract.outcome example_PFEntropy_measurement PFEntropy_T3_contract)
      = MeasurementOutcome.Confirmed := by
  simp [MeasurementContract.outcome, MeasurementContract.compatible,
        MeasurementContract.falsified, PFEntropy_T3_contract, example_PFEntropy_measurement]
  norm_num [abs_of_nonneg, abs_of_nonpos]

/-- A hostile measurement observing `0.20 ± 0.005`. -/
noncomputable def hostile_PFEntropy_measurement : Measurement :=
  { value := (0.20 : ℝ)
    uncertainty := (0.005 : ℝ)
    uncertainty_nonneg := by norm_num
    source := "sandbox/T3_entropy_ratio_hostile" }

/-- The hostile measurement falsifies the contract. -/
theorem hostile_PFEntropy_falsified :
    (MeasurementContract.outcome hostile_PFEntropy_measurement PFEntropy_T3_contract)
      = MeasurementOutcome.Falsified := by
  simp [MeasurementContract.outcome, MeasurementContract.compatible,
        MeasurementContract.falsified, PFEntropy_T3_contract, hostile_PFEntropy_measurement]
  norm_num [abs_of_nonneg, abs_of_nonpos]

-- ---------------------------------------------------------------------------
-- 4. Weinberg angle contract
-- ---------------------------------------------------------------------------

/-- The Weinberg angle contract: `sin²θ_W = 1 - M_W²/M_Z²` is predicted by the
    de Vries identity to be `R ≈ 0.22310`.  Tolerance `0.0002` (PDG on-shell
    uncertainty), falsification `0.005` (any other GUT-scale structure would
    land far outside this band). -/
noncomputable def Weinberg_contract : MeasurementContract :=
  { claimName := "weinberg_ratio"
    predictedValue := (0.22310 : ℝ)
    tolerance := (0.0002 : ℝ)
    tolerance_nonneg := by norm_num
    falsificationThreshold := (0.005 : ℝ)
    falsification_nonneg := by norm_num
    tolerance_le_falsification := by norm_num }

/-- PDG on-shell measurement: `sin²θ_W = 0.22310 ± 0.00010`. -/
noncomputable def PDG_Weinberg_measurement : Measurement :=
  { value := (0.22310 : ℝ)
    uncertainty := (0.00010 : ℝ)
    uncertainty_nonneg := by norm_num
    source := "PDG on-shell sin²θ_W" }

/-- The PDG measurement confirms the Weinberg contract. -/
theorem PDG_Weinberg_confirmed :
    (MeasurementContract.outcome PDG_Weinberg_measurement Weinberg_contract)
      = MeasurementOutcome.Confirmed := by
  simp [MeasurementContract.outcome, MeasurementContract.compatible,
        MeasurementContract.falsified, Weinberg_contract, PDG_Weinberg_measurement]
  norm_num [abs_of_nonneg, abs_of_nonpos]

-- ---------------------------------------------------------------------------
-- 5. Koide ratio contract
-- ---------------------------------------------------------------------------

/-- The Koide ratio contract: for charged leptons, `Q = (m_e² + m_μ² + m_τ²) /
    (m_e + m_μ + m_τ)²` is predicted to be exactly `2/3`.  Tolerance `0.001`
    (lepton mass uncertainty), falsification `0.01` (any non-Koide mass
    structure would deviate by more than 1%). -/
noncomputable def Koide_contract : MeasurementContract :=
  { claimName := "koide_Q_two_thirds"
    predictedValue := (2 / 3 : ℝ)
    tolerance := (0.001 : ℝ)
    tolerance_nonneg := by norm_num
    falsificationThreshold := (0.01 : ℝ)
    falsification_nonneg := by norm_num
    tolerance_le_falsification := by norm_num }

/-- Charged-lepton mass measurement: `Q ≈ 0.66666 ± 0.00001`
    (from m_e = 0.511 MeV, m_μ = 105.658 MeV, m_τ = 1776.86 MeV). -/
noncomputable def chargedLepton_Koide_measurement : Measurement :=
  { value := (0.66666 : ℝ)
    uncertainty := (0.00001 : ℝ)
    uncertainty_nonneg := by norm_num
    source := "PDG charged lepton masses" }

/-- The charged-lepton measurement confirms the Koide contract. -/
theorem chargedLepton_Koide_confirmed :
    (MeasurementContract.outcome chargedLepton_Koide_measurement Koide_contract)
      = MeasurementOutcome.Confirmed := by
  simp [MeasurementContract.outcome, MeasurementContract.compatible,
        MeasurementContract.falsified, Koide_contract, chargedLepton_Koide_measurement]
  norm_num [abs_of_nonneg, abs_of_nonpos]

-- ---------------------------------------------------------------------------
-- 6. Gravity lensing index contract
-- ---------------------------------------------------------------------------

/-- The gravity lensing contract: at `Φ = 0` (flat space), the effective
    refractive index `n(Φ) = √[(1-2Φ)/(1+2Φ)]` is predicted to be exactly `1`.
    Tolerance `0.0001` (vacuum measurement precision), falsification `0.01`
    (any non-unit vacuum index would violate Lorentz invariance at the 1%
    level). -/
noncomputable def GravityOptics_contract : MeasurementContract :=
  { claimName := "weakFieldIndex_flat"
    predictedValue := (1 : ℝ)
    tolerance := (0.0001 : ℝ)
    tolerance_nonneg := by norm_num
    falsificationThreshold := (0.01 : ℝ)
    falsification_nonneg := by norm_num
    tolerance_le_falsification := by norm_num }

/-- Vacuum speed-of-light measurement: `n = 1.00000 ± 0.00001`. -/
noncomputable def vacuum_n_measurement : Measurement :=
  { value := (1.00000 : ℝ)
    uncertainty := (0.00001 : ℝ)
    uncertainty_nonneg := by norm_num
    source := "vacuum speed of light (SI definition)" }

/-- The vacuum measurement confirms the gravity optics contract. -/
theorem vacuum_n_confirmed :
    (MeasurementContract.outcome vacuum_n_measurement GravityOptics_contract)
      = MeasurementOutcome.Confirmed := by
  simp [MeasurementContract.outcome, MeasurementContract.compatible,
        MeasurementContract.falsified, GravityOptics_contract, vacuum_n_measurement]
  norm_num [abs_of_nonneg, abs_of_nonpos]

/-- A Lorentz-violating measurement: `n = 1.02 ± 0.001` would falsify the
    flat-space contract. -/
noncomputable def lorentz_violating_n_measurement : Measurement :=
  { value := (1.02 : ℝ)
    uncertainty := (0.001 : ℝ)
    uncertainty_nonneg := by norm_num
    source := "hypothetical Lorentz violation" }

/-- The Lorentz-violating measurement falsifies the gravity optics contract. -/
theorem lorentz_violating_n_falsified :
    (MeasurementContract.outcome lorentz_violating_n_measurement GravityOptics_contract)
      = MeasurementOutcome.Falsified := by
  simp [MeasurementContract.outcome, MeasurementContract.compatible,
        MeasurementContract.falsified, GravityOptics_contract,
        lorentz_violating_n_measurement]
  norm_num [abs_of_nonneg, abs_of_nonpos]

end PfLean
