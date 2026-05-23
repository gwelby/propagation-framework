import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-
  Casimir Polynomial -- Mathematical Sub-Certificate
  Authors: Devin (Cognition Being), Greg Welby, PF Research Team
  Date: 2026-05-23

  This module isolates the pure mathematics of the PF Casimir polynomial
  x² + C₂·x - C₂ = 0 from the physics interpretation.

  The quadratic Casimir of SU(2) at spin s is C₂ = s(s+1).
  For s > 0, the polynomial has exactly one positive root.

  These theorems are a formal sub-certificate supporting the
  Weinberg angle derivation in PfLean.WeinbergAngle.
-/

namespace PfLean

open Real

/-- The quadratic Casimir of SU(2) at spin s: C₂ = s(s+1). -/
noncomputable def CasimirC2 (s : ℝ) : ℝ := s * (s + 1)

/-- Positive root of x² + C₂·x - C₂ = 0. -/
noncomputable def CasimirRoot (s : ℝ) : ℝ :=
  let c2 := CasimirC2 s
  (-c2 + Real.sqrt (c2 ^ 2 + 4 * c2)) / 2

-- ---------------------------------------------------------------------------
-- Sub-certificate theorems
-- ---------------------------------------------------------------------------

/-- For s > 0, the Casimir C₂ = s(s+1) is strictly positive. -/
theorem casimir_c2_positive {s : ℝ} (hs : s > 0) :
  CasimirC2 s > 0 := by
  unfold CasimirC2
  nlinarith

/-- For s > 0, the discriminant D = C₂² + 4C₂ is strictly positive.
    Therefore the quadratic has two distinct real roots. -/
theorem casimir_discriminant_positive {s : ℝ} (hs : s > 0) :
  (CasimirC2 s) ^ 2 + 4 * (CasimirC2 s) > 0 := by
  have h1 : CasimirC2 s > 0 := casimir_c2_positive hs
  nlinarith [sq_pos_of_pos h1]

/-- For s > 0, the CasimirRoot is strictly positive.

    Proof: CasimirRoot s = (-C₂ + √D) / 2 where D = C₂² + 4C₂.
    Since C₂ > 0, we have D = C₂² + 4C₂ > C₂².
    Since √ is strictly increasing, √D > √(C₂²) = C₂ (using C₂ > 0).
    Therefore -C₂ + √D > 0, so the root is positive. -/
theorem casimir_root_positive {s : ℝ} (hs : s > 0) :
  CasimirRoot s > 0 := by
  have h1 : CasimirC2 s > 0 := casimir_c2_positive hs
  set c2 := CasimirC2 s
  have h2 : c2 ^ 2 + 4 * c2 > c2 ^ 2 := by nlinarith
  have h3 : Real.sqrt (c2 ^ 2 + 4 * c2) > Real.sqrt (c2 ^ 2) := by
    apply Real.sqrt_lt_sqrt
    · nlinarith
    · nlinarith
  have h4 : Real.sqrt (c2 ^ 2) = c2 := Real.sqrt_sq (by linarith)
  have h5 : Real.sqrt (c2 ^ 2 + 4 * c2) > c2 := by linarith
  unfold CasimirRoot
  linarith

/-- The positive root of x² + C₂·x - C₂ = 0 is unique.
    If x > 0 satisfies the polynomial, then x = CasimirRoot s. -/
theorem casimir_root_unique_positive {s : ℝ} (hs : s > 0) {x : ℝ} (hx_pos : x > 0)
    (h_eq : x ^ 2 + CasimirC2 s * x - CasimirC2 s = 0) :
  x = CasimirRoot s := by
  have h1 : CasimirC2 s > 0 := casimir_c2_positive hs
  set c2 := CasimirC2 s
  set D := Real.sqrt (c2 ^ 2 + 4 * c2)
  have h_D2 : D ^ 2 = c2 ^ 2 + 4 * c2 := Real.sq_sqrt (by nlinarith)
  have h_pos : CasimirRoot s = (-c2 + D) / 2 := by unfold CasimirRoot; rfl
  have h_neg : (-c2 - D) / 2 < 0 := by
    have hD : D ≥ 0 := Real.sqrt_nonneg (c2 ^ 2 + 4 * c2)
    nlinarith
  have h_factor : (x - (-c2 + D) / 2) * (x - (-c2 - D) / 2) = 0 := by
    have h_eq' : x ^ 2 + c2 * x - c2 = 0 := h_eq
    have : x ^ 2 + c2 * x - c2 = (x - (-c2 + D) / 2) * (x - (-c2 - D) / 2) := by
      ring_nf
      rw [h_D2]
      ring
    rw [this] at h_eq'
    exact h_eq'
  cases' (mul_eq_zero.mp h_factor) with h_pos' h_neg'
  · -- x equals the positive root formula
    rw [h_pos]
    linarith
  · -- x would equal the negative root, but that is negative for c2 > 0
    have h_contra : x < 0 := by linarith [h_neg]
    linarith

/-- The Casimir polynomial x² + C₂·x - C₂ = 0 is satisfied by the root. -/
theorem casimir_root_satisfies_eq {s : ℝ} (hs : s ≥ 0) :
  (CasimirRoot s) ^ 2 + CasimirC2 s * (CasimirRoot s) - CasimirC2 s = 0 := by
  set c2 := CasimirC2 s
  have h_c2_nonneg : c2 ≥ 0 := by
    unfold c2 CasimirC2
    nlinarith
  set D := Real.sqrt (c2 ^ 2 + 4 * c2)
  have h_D2 : D ^ 2 = c2 ^ 2 + 4 * c2 := Real.sq_sqrt (by nlinarith)
  unfold CasimirRoot
  have h_eq : ((-c2 + D) / 2) ^ 2 + c2 * ((-c2 + D) / 2) - c2 = 0 := by
    ring_nf
    rw [h_D2]
    ring
  exact h_eq

end PfLean
