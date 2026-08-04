import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import PfLean.BekensteinBound

/-
  Chain Rule Formalization — Conditional Black-Hole Thermodynamic Identity
  Authors: Devin (Cognition AI), Greg Welby
  Date: 2026-08-03

  This module formalizes a CONDITIONAL algebraic identity, NOT a PF derivation.

  Imported premises (not derived here):
    1. Schwarzschild relation R = 2GE/c⁴ (from General Relativity)
    2. Entropy S = 2πkRE/ℏc (from assumed Bekenstein bound)
    3. Thermodynamic relation 1/T = dS/dE (from thermodynamics)

  The factor-of-2 resolution is correct mathematics along the Schwarzschild
  family: the total derivative dS/dE = ∂S/∂E|_R + ∂S/∂R|_E · dR/dE yields
  8πkGE/(ℏc⁵), giving T = ℏc⁵/(8πkGE) = ℏc³/(8πkGM) = T_Hawking.

  This reproduces the known Hawking formula from known black-hole relations;
  it is not an independent PF explanation.
-/

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. Functions
-- ---------------------------------------------------------------------------

/-- S(E, R) = 2πkRE/ℏc as a function of E, with R held fixed.
    Entropy formula from assumed Bekenstein bound (imported premise). -/
noncomputable def cr_satEntropyE (k R c ℏ : ℝ) (E : ℝ) : ℝ :=
  2 * Real.pi * k * R * E / (ℏ * c)

/-- R(E) = 2GE/c⁴ — Schwarzschild radius as a function of E.
    Schwarzschild relation from General Relativity (imported premise). -/
noncomputable def cr_schwarzschildR (G c : ℝ) (E : ℝ) : ℝ :=
  2 * G * E / c^4

/-- S(E) = S(E, R(E)) — entropy with R depending on E.
    Combines the Bekenstein-bound entropy S = 2πkRE/ℏc with the Schwarzschild
    relation R = 2GE/c⁴ (both imported premises).
    S(E) = 2πk × (2GE/c⁴) × E / (ℏc) = 4πkGE²/(ℏc⁵). -/
noncomputable def cr_satEntropyTotal (k G c ℏ : ℝ) (E : ℝ) : ℝ :=
  cr_satEntropyE k (cr_schwarzschildR G c E) c ℏ E

-- ---------------------------------------------------------------------------
-- 2. Derivatives via Mathlib
-- ---------------------------------------------------------------------------

/-- ∂S/∂E|_R = 2πkR/ℏc. Pure algebraic derivative; no positivity needed. -/
theorem cr_deriv_satEntropyE (k R c ℏ E : ℝ) :
  deriv (cr_satEntropyE k R c ℏ) E = 2 * Real.pi * k * R / (ℏ * c) := by
  unfold cr_satEntropyE
  have h_eq : (fun E => 2 * Real.pi * k * R * E / (ℏ * c)) =
              (fun E => (2 * Real.pi * k * R / (ℏ * c)) * E) := by
    funext E; ring
  rw [h_eq, deriv_const_mul_field]
  simp [deriv_id]

/-- dR/dE = 2G/c⁴. Pure algebraic derivative; no positivity needed. -/
theorem cr_deriv_schwarzschildR (G c E : ℝ) :
  deriv (cr_schwarzschildR G c) E = 2 * G / c^4 := by
  unfold cr_schwarzschildR
  have h_eq : (fun E => 2 * G * E / c^4) =
              (fun E => (2 * G / c^4) * E) := by
    funext E; ring
  rw [h_eq, deriv_const_mul_field]
  simp [deriv_id]

-- ---------------------------------------------------------------------------
-- 3. The chain rule computation
-- ---------------------------------------------------------------------------

/-- The total derivative dS/dE = 8πkGE/(ℏc⁵).
    S(E) = 4πkGE²/(ℏc⁵), so dS/dE = 8πkGE/(ℏc⁵).
    Pure algebraic derivative; no positivity needed. -/
theorem cr_total_deriv (k G c ℏ E : ℝ) :
  deriv (cr_satEntropyTotal k G c ℏ) E = 8 * Real.pi * k * G * E / (ℏ * c^5) := by
  unfold cr_satEntropyTotal cr_satEntropyE cr_schwarzschildR
  have h_eq : (fun E => 2 * Real.pi * k * (2 * G * E / c^4) * E / (ℏ * c)) =
              (fun E => (4 * Real.pi * k * G / (ℏ * c^5)) * E^2) := by
    funext E; ring
  rw [h_eq, deriv_const_mul_field]
  have h_d : deriv (fun E => E^2) E = 2 * E := by
    simp [pow_two, deriv_mul, deriv_id]
    ring
  rw [h_d]
  ring

/-- The chain rule decomposition: dS/dE = ∂S/∂E|_R + ∂S/∂R|_E × dR/dE.
    Pure algebraic identity; no positivity needed. -/
theorem cr_chain_rule_decomposition (k G c ℏ E : ℝ) :
  deriv (cr_satEntropyTotal k G c ℏ) E =
  2 * Real.pi * k * cr_schwarzschildR G c E / (ℏ * c) +
  (2 * Real.pi * k * E / (ℏ * c)) * (2 * G / c^4) := by
  rw [cr_total_deriv k G c ℏ E]
  unfold cr_schwarzschildR
  ring

/-- Both chain-rule terms are equal when R = 2GE/c⁴.
    Pure algebraic identity; no positivity needed. -/
theorem cr_chain_rule_terms_equal (k G c ℏ E : ℝ) :
  2 * Real.pi * k * cr_schwarzschildR G c E / (ℏ * c) =
  (2 * Real.pi * k * E / (ℏ * c)) * (2 * G / c^4) := by
  unfold cr_schwarzschildR
  ring

/-- Conditional black-hole thermodynamic identity: T_total = 1/(dS/dE) = ℏc⁵/(8πkGE).
    Uses the thermodynamic relation 1/T = dS/dE (imported premise).
    Positivity hypotheses needed for `field_simp` to clear denominators. -/
theorem cr_total_temperature_conditional (k G c ℏ E : ℝ)
    (hk : k > 0) (hG : G > 0) (hc : c > 0) (hℏ : ℏ > 0) (hE : E > 0) :
  1 / deriv (cr_satEntropyTotal k G c ℏ) E = ℏ * c^5 / (8 * Real.pi * k * G * E) := by
  rw [cr_total_deriv k G c ℏ E]
  field_simp

/-- Conditional black-hole thermodynamic identity: T_partial = 1/(∂S/∂E|_R) = ℏc/(2πkR).
    Uses the thermodynamic relation 1/T = dS/dE (imported premise).
    Positivity hypotheses needed for `field_simp` to clear denominators. -/
theorem cr_partial_temperature_conditional (k R c ℏ E : ℝ)
    (hk : k > 0) (hR : R > 0) (hc : c > 0) (hℏ : ℏ > 0) :
  1 / deriv (cr_satEntropyE k R c ℏ) E = ℏ * c / (2 * Real.pi * k * R) := by
  rw [cr_deriv_satEntropyE k R c ℏ E]
  field_simp

/-- Conditional black-hole thermodynamic identity: T_total = T_partial / 2 when R = R_s.
    Uses the Schwarzschild relation R = 2GE/c⁴ (imported premise from GR).
    Positivity hypotheses needed for `field_simp` to clear denominators. -/
theorem cr_total_is_half_partial (k G c ℏ E : ℝ)
    (hk : k > 0) (hG : G > 0) (hc : c > 0) (hℏ : ℏ > 0) (hE : E > 0) :
  ℏ * c^5 / (8 * Real.pi * k * G * E) =
  ℏ * c / (2 * Real.pi * k * cr_schwarzschildR G c E) / 2 := by
  unfold cr_schwarzschildR
  field_simp
  ring

/-- Conditional black-hole thermodynamic identity: T_H = ℏc³/(8πkGM) with E = Mc².
    Reproduces the known Hawking temperature from the imported premises
    (Schwarzschild R = 2GE/c⁴ from GR, entropy S = 2πkRE/ℏc from assumed
    Bekenstein bound, thermodynamic 1/T = dS/dE). Not an independent PF explanation.
    Positivity hypotheses needed for `field_simp` to clear denominators. -/
theorem cr_hawking_temperature_conditional (k G M c ℏ : ℝ)
    (hk : k > 0) (hG : G > 0) (hM : M > 0) (hc : c > 0) (hℏ : ℏ > 0) :
  1 / deriv (cr_satEntropyTotal k G c ℏ) (M * c^2) =
  ℏ * c^3 / (8 * Real.pi * k * G * M) := by
  rw [cr_total_deriv k G c ℏ (M * c^2)]
  field_simp

end PfLean
