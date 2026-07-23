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
      { cr with
        status := .OK,
        evidence := cr.evidence ++ " | measurement confirmed: " ++ measurementNote }
  | .Inconclusive =>
      { cr with
        status := .HOLD,
        evidence := cr.evidence ++ " | measurement inconclusive: " ++ measurementNote }
  | .Falsified =>
      { cr with
        status := .NOGO,
        evidence := cr.evidence ++ " | measurement falsified: " ++ measurementNote }

end MeasurementContract

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

end PfLean
