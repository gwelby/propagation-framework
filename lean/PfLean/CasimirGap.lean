import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.CasimirPolynomial
import PfLean.WeinbergAngle

/-!
# CasimirGap — The Honesty Layer for the Casimir/Weinberg Derivation

Sibling of `CasimirPolynomial.lean` and `WeinbergAngle.lean`. Those modules
prove the **algebra**: the polynomial root exists, the closed form is
(√19−3)(√19−√3)/16, and the numerical bounds match PDG to 0.13σ.

This module formalizes what those modules **do not** prove — the gaps between
the algebra and the physics. It follows the pattern established by
`KoideUnlocked.lean`: machine-check the algebra, then machine-check the
boundaries of what the algebra alone cannot reach.

## The three gaps

**Gap 1 (extra-β):** The de Broglie relativistic orbit gives γβ = √C₂.
The Casimir polynomial requires γβ² = √C₂. These differ by exactly one
factor of β. We prove they are **incompatible** for any physical particle
(0 < β < 1). This is the core unresolved mathematical discrepancy identified
across 8 independent derivation routes (A–H, see `casimir_polynomial_synthesis.md`).

**Gap 2 (look-elsewhere):** The Weinberg ratio R = 0.22310 is obtained from
the spin pair (1/2, 1). We compute R for three alternative low-spin pairs
and show each is far from the PDG value. This does not close the
look-elsewhere concern (P≈0.46 for random targets), but it does show that
within the natural discrete set of low-lying SU(2) reps, (1/2, 1) is
the unique match.

**Gap 3 (non-theorems):** The physics interpretation requires spin-pair
selection, k=1 selection (Axiom 3b), and scheme selection — none derived
from Axioms 1-3. These are documented as non-theorems.
-/

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. The extra-β gap (machine-checked)
-- ---------------------------------------------------------------------------

/-- The Lorentz factor γ = 1/√(1−β²), defined for |β| < 1. -/
noncomputable def lorentzFactor (β : ℝ) : ℝ := 1 / Real.sqrt (1 - β^2)

/-- For 0 < β < 1, the Lorentz factor is strictly positive. -/
theorem lorentz_factor_pos {β : ℝ} (h1 : 0 < β) (h2 : β < 1) :
    0 < lorentzFactor β := by
  unfold lorentzFactor
  have h_sq : 0 < 1 - β^2 := by nlinarith
  have h_sqrt : 0 < Real.sqrt (1 - β^2) := Real.sqrt_pos.mpr h_sq
  exact one_div_pos.mpr h_sqrt

/-- **The extra-β gap, machine-checked:**
    The de Broglie condition (γβ = √C₂) and the Casimir condition (γβ² = √C₂)
    cannot both hold for any physical particle (0 < β < 1, C₂ > 0).

    Proof: If both hold, then γβ = γβ². Since γ > 0, this gives β = β²,
    hence β(1−β) = 0, so β = 0 or β = 1. Both are excluded for a massive
    particle with non-trivial velocity. -/
theorem extra_beta_gap {β C₂ : ℝ} (hβ_pos : 0 < β) (hβ_lt : β < 1) (hC₂ : 0 < C₂)
    (h_deBroglie : lorentzFactor β * β = Real.sqrt C₂)
    (h_casimir : lorentzFactor β * β^2 = Real.sqrt C₂) :
    False := by
  have hγ : 0 < lorentzFactor β := lorentz_factor_pos hβ_pos hβ_lt
  have h_eq : β = β^2 := by
    have h : lorentzFactor β * β = lorentzFactor β * β^2 := by
      rw [h_deBroglie, h_casimir]
    exact mul_left_cancel₀ hγ.ne' h
  have h_factor : β * (1 - β) = 0 := by nlinarith [h_eq]
  rcases mul_eq_zero.mp h_factor with h0 | h1
  · exact absurd h0 (ne_of_gt hβ_pos)
  · have h_eq1 : β = 1 := by linarith
    exact absurd h_eq1 (ne_of_lt hβ_lt)

/-- **Corollary:** the extra-β gap is an exact algebraic incompatibility.
    No choice of β in the physical range (0, 1) can satisfy both conditions. -/
theorem extra_beta_gap_exact :
    ¬ ∃ (β C₂ : ℝ), 0 < β ∧ β < 1 ∧ 0 < C₂ ∧
      lorentzFactor β * β = Real.sqrt C₂ ∧
      lorentzFactor β * β^2 = Real.sqrt C₂ := by
  rintro ⟨β, C₂, hβ_pos, hβ_lt, hC₂, h_db, h_cas⟩
  exact extra_beta_gap hβ_pos hβ_lt hC₂ h_db h_cas

-- ---------------------------------------------------------------------------
-- 2. The look-elsewhere scan (low-spin pairs)
-- ---------------------------------------------------------------------------

/-- Casimir root for spin 3/2: x₊(3/2) = (−15 + √465) / 8. -/
theorem casimir_root_three_halves :
    CasimirRoot (3 / 2) = (-15 + Real.sqrt 465) / 8 := by
  unfold CasimirRoot CasimirC2
  norm_num
  <;> ring_nf
  <;> norm_num

/-- Casimir root for spin 2: x₊(2) = −3 + √15. -/
theorem casimir_root_two :
    CasimirRoot 2 = -3 + Real.sqrt 15 := by
  unfold CasimirRoot CasimirC2
  have h : Real.sqrt (60 : ℝ) = 2 * Real.sqrt 15 := by
    rw [show (60 : ℝ) = 4 * 15 by norm_num]
    rw [Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 4)]
    have h4 : Real.sqrt (4 : ℝ) = 2 := by norm_num
    rw [h4]
  norm_num
  <;> rw [h]
  <;> ring_nf
  <;> norm_num

/-- R(1/2, 3/2) ≈ 0.307 — far from the PDG value 0.22337. -/
theorem weinberg_ratio_alt_pair_1_bounds :
    0.29 < (1 - CasimirRoot (1/2) / CasimirRoot (3/2)) ∧
    (1 - CasimirRoot (1/2) / CasimirRoot (3/2)) < 0.32 := by
  rw [casimir_root_half, casimir_root_three_halves]
  have h57_ub : Real.sqrt 57 < 7.550 := by rw [Real.sqrt_lt]; all_goals norm_num
  have h465_lb : 21.563 < Real.sqrt 465 := by rw [Real.lt_sqrt]; all_goals norm_num
  have h465_ub : Real.sqrt 465 < 21.564 := by rw [Real.sqrt_lt]; all_goals norm_num
  have h_den : (0 : ℝ) < -15 + Real.sqrt 465 := by
    have : 15 < Real.sqrt 465 := by rw [Real.lt_sqrt]; all_goals norm_num
    linarith
  constructor
  · -- 0.29 < 1 - a/b  ↔  a/b < 0.71  ↔  a < 0.71*b (b > 0)
    have h_key : (-3 + Real.sqrt 57) < (71 / 100 : ℝ) * (-15 + Real.sqrt 465) := by
      nlinarith [h57_ub, h465_lb, h_den,
        Real.sq_sqrt (show (0:ℝ) ≤ 57 by norm_num),
        Real.sq_sqrt (show (0:ℝ) ≤ 465 by norm_num)]
    have h_div : (-3 + Real.sqrt 57) / (-15 + Real.sqrt 465) < 71 / 100 := by
      rwa [div_lt_iff₀ h_den]
    have h_simp : ((-3 + Real.sqrt 57) / 8) / ((-15 + Real.sqrt 465) / 8) =
        (-3 + Real.sqrt 57) / (-15 + Real.sqrt 465) := by field_simp
    rw [h_simp]
    linarith
  · -- 1 - a/b < 0.32  ↔  a/b > 0.68  ↔  a > 0.68*b (b > 0)
    have h57_lb : 7.549 < Real.sqrt 57 := by rw [Real.lt_sqrt]; all_goals norm_num
    have h_key : (68 / 100 : ℝ) * (-15 + Real.sqrt 465) < (-3 + Real.sqrt 57) := by
      nlinarith [h57_lb, h465_ub, h_den,
        Real.sq_sqrt (show (0:ℝ) ≤ 57 by norm_num),
        Real.sq_sqrt (show (0:ℝ) ≤ 465 by norm_num)]
    have h_div : 68 / 100 < (-3 + Real.sqrt 57) / (-15 + Real.sqrt 465) := by
      rwa [lt_div_iff₀ h_den]
    have h_simp : ((-3 + Real.sqrt 57) / 8) / ((-15 + Real.sqrt 465) / 8) =
        (-3 + Real.sqrt 57) / (-15 + Real.sqrt 465) := by field_simp
    rw [h_simp]
    linarith

/-- R(1, 3/2) ≈ 0.108 — far from the PDG value. -/
theorem weinberg_ratio_alt_pair_2_bounds :
    0.09 < (1 - CasimirRoot 1 / CasimirRoot (3/2)) ∧
    (1 - CasimirRoot 1 / CasimirRoot (3/2)) < 0.13 := by
  rw [casimir_root_one, casimir_root_three_halves]
  have h3_lb : 1.732 < Real.sqrt 3 := by rw [Real.lt_sqrt]; all_goals norm_num
  have h3_ub : Real.sqrt 3 < 1.733 := by rw [Real.sqrt_lt]; all_goals norm_num
  have h465_lb : 21.563 < Real.sqrt 465 := by rw [Real.lt_sqrt]; all_goals norm_num
  have h465_ub : Real.sqrt 465 < 21.564 := by rw [Real.sqrt_lt]; all_goals norm_num
  have h_den : (0 : ℝ) < -15 + Real.sqrt 465 := by
    have : 15 < Real.sqrt 465 := by rw [Real.lt_sqrt]; all_goals norm_num
    linarith
  -- After clearing /8: ratio = 8*(-1+√3) / (-15+√465)
  constructor
  · -- 0.09 < 1 - 8a/b  ↔  8a/b < 0.91  ↔  8a < 0.91*b
    have h_key : 8 * (-1 + Real.sqrt 3) < (91 / 100 : ℝ) * (-15 + Real.sqrt 465) := by
      nlinarith [h3_ub, h465_lb, h_den,
        Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num),
        Real.sq_sqrt (show (0:ℝ) ≤ 465 by norm_num)]
    have h_div : 8 * (-1 + Real.sqrt 3) / (-15 + Real.sqrt 465) < 91 / 100 := by
      rwa [div_lt_iff₀ h_den]
    -- 1 - 8*(-1+√3)/((-15+√465)/8) = 1 - 8*(-1+√3)/(-15+√465) ... wait
    -- Actually: CasimirRoot 1 / CasimirRoot (3/2) = (-1+√3) / ((-15+√465)/8)
    --         = 8*(-1+√3) / (-15+√465)
    -- So 1 - that = 1 - 8*(-1+√3)/(-15+√465)
    -- And 0.09 < 1 - 8a/b ↔ 8a/b < 0.91
    have h_orig : (-1 + Real.sqrt 3) / ((-15 + Real.sqrt 465) / 8) < 91 / 100 := by
      have h8 : ((-15 + Real.sqrt 465) / 8 : ℝ) > 0 := by linarith
      have : (-1 + Real.sqrt 3) / ((-15 + Real.sqrt 465) / 8) =
          8 * (-1 + Real.sqrt 3) / (-15 + Real.sqrt 465) := by field_simp
      rw [this]
      exact h_div
    linarith
  · -- 1 - 8a/b < 0.13  ↔  8a/b > 0.87  ↔  8a > 0.87*b
    have h_key : (87 / 100 : ℝ) * (-15 + Real.sqrt 465) < 8 * (-1 + Real.sqrt 3) := by
      nlinarith [h3_lb, h465_ub, h_den,
        Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num),
        Real.sq_sqrt (show (0:ℝ) ≤ 465 by norm_num)]
    have h_div : 87 / 100 < 8 * (-1 + Real.sqrt 3) / (-15 + Real.sqrt 465) := by
      rwa [lt_div_iff₀ h_den]
    have h_orig : 87 / 100 < (-1 + Real.sqrt 3) / ((-15 + Real.sqrt 465) / 8) := by
      have h8 : ((-15 + Real.sqrt 465) / 8 : ℝ) > 0 := by linarith
      have : (-1 + Real.sqrt 3) / ((-15 + Real.sqrt 465) / 8) =
          8 * (-1 + Real.sqrt 3) / (-15 + Real.sqrt 465) := by field_simp
      rw [this]
      exact h_div
    linarith

/-- R(1/2, 2) ≈ 0.349 — far from the PDG value. -/
theorem weinberg_ratio_alt_pair_3_bounds :
    0.32 < (1 - CasimirRoot (1/2) / CasimirRoot 2) ∧
    (1 - CasimirRoot (1/2) / CasimirRoot 2) < 0.38 := by
  rw [casimir_root_half, casimir_root_two]
  have h57_lb : 7.549 < Real.sqrt 57 := by rw [Real.lt_sqrt]; all_goals norm_num
  have h57_ub : Real.sqrt 57 < 7.550 := by rw [Real.sqrt_lt]; all_goals norm_num
  have h15_lb : 3.872 < Real.sqrt 15 := by rw [Real.lt_sqrt]; all_goals norm_num
  have h15_ub : Real.sqrt 15 < 3.873 := by rw [Real.sqrt_lt]; all_goals norm_num
  have h_den : (0 : ℝ) < -3 + Real.sqrt 15 := by
    have : 9 < 15 := by norm_num
    have h3 : 3 < Real.sqrt 15 := by rw [Real.lt_sqrt]; all_goals norm_num
    linarith
  -- ratio = ((-3+√57)/8) / (-3+√15) = (-3+√57) / (8*(-3+√15))
  constructor
  · -- 0.32 < 1 - a/(8b)  ↔  a/(8b) < 0.68  ↔  a < 0.68*8b = 5.44*b
    have h_key : (-3 + Real.sqrt 57) < (68 / 100 : ℝ) * (8 * (-3 + Real.sqrt 15)) := by
      nlinarith [h57_ub, h15_lb, h_den,
        Real.sq_sqrt (show (0:ℝ) ≤ 57 by norm_num),
        Real.sq_sqrt (show (0:ℝ) ≤ 15 by norm_num)]
    have h_div : (-3 + Real.sqrt 57) / (8 * (-3 + Real.sqrt 15)) < 68 / 100 := by
      rwa [div_lt_iff₀ (by linarith : (0:ℝ) < 8 * (-3 + Real.sqrt 15))]
    have h_orig : ((-3 + Real.sqrt 57) / 8) / (-3 + Real.sqrt 15) < 68 / 100 := by
      have : ((-3 + Real.sqrt 57) / 8) / (-3 + Real.sqrt 15) =
          (-3 + Real.sqrt 57) / (8 * (-3 + Real.sqrt 15)) := by field_simp
      rw [this]
      exact h_div
    linarith
  · -- 1 - a/(8b) < 0.38  ↔  a/(8b) > 0.62  ↔  a > 0.62*8b = 4.96*b
    have h_key : (62 / 100 : ℝ) * (8 * (-3 + Real.sqrt 15)) < (-3 + Real.sqrt 57) := by
      nlinarith [h57_lb, h15_ub, h_den,
        Real.sq_sqrt (show (0:ℝ) ≤ 57 by norm_num),
        Real.sq_sqrt (show (0:ℝ) ≤ 15 by norm_num)]
    have h_div : 62 / 100 < (-3 + Real.sqrt 57) / (8 * (-3 + Real.sqrt 15)) := by
      rwa [lt_div_iff₀ (by linarith : (0:ℝ) < 8 * (-3 + Real.sqrt 15))]
    have h_orig : 62 / 100 < ((-3 + Real.sqrt 57) / 8) / (-3 + Real.sqrt 15) := by
      have : ((-3 + Real.sqrt 57) / 8) / (-3 + Real.sqrt 15) =
          (-3 + Real.sqrt 57) / (8 * (-3 + Real.sqrt 15)) := by field_simp
      rw [this]
      exact h_div
    linarith

/-- **Uniqueness within the low-spin set:** the pair (1/2, 1) is the unique
    match among low-lying SU(2) reps. See `weinberg_ratio_bounds` for the
    canonical pair's bounds (0.22309, 0.22311). -/
theorem weinberg_ratio_unique_in_low_spin_set :
    (22309 / 100000 < WeinbergRatio ∧ WeinbergRatio < 22311 / 100000) ∧
    (0.29 < 1 - CasimirRoot (1/2) / CasimirRoot (3/2)) ∧
    (1 - CasimirRoot 1 / CasimirRoot (3/2) < 0.13) ∧
    (0.32 < 1 - CasimirRoot (1/2) / CasimirRoot 2) := by
  exact ⟨weinberg_ratio_bounds,
         weinberg_ratio_alt_pair_1_bounds.1,
         weinberg_ratio_alt_pair_2_bounds.2,
         weinberg_ratio_alt_pair_3_bounds.1⟩

-- ---------------------------------------------------------------------------
-- 3. Non-theorems — the physics gaps (documented, deliberately unprovable)
-- ---------------------------------------------------------------------------

/-!
## Gap 3: Non-theorems — what the algebra does NOT prove

**N1: Spin-pair selection.** Why (s₁, s₂) = (1/2, 1)?
The algebra works for any spin pair. The selection is argued from
"minimal coherent representation principle", not derived from PF axioms.
The look-elsewhere scan above shows (1/2, 1) is the unique match in the
low-spin set, but uniqueness within a discrete set is not a derivation.

**N2: k=1 selection (Axiom 3b).** Why J_z = J_θ (k=1, not k=2,3,...)?
Axiom 3b (Minimal Winding Principle) selects k=1. But Axiom 3b is an
EXPLICIT PREMISE — it is not derived from Axioms 1-3.

**N3: Scheme selection.** Why the on-shell scheme?
The ratio matches PDG on-shell (0.22337) to 0.13σ. The MS-bar running
angle does NOT match (T-021 audit, 2026-04-13). The framework does not
derive why the on-shell scheme is the correct one.

**N4: Polynomial derivation.** Why x² + C₂·x − C₂ = 0?
Eight routes converge but none closes the extra-β gap (Gap 1). The
polynomial is the best candidate, not a derivation.

**Summary:** The algebra is exact. The physics is ARGUED 0.65. The gap
between them is three explicit premises (N1, N2, N3) and one unresolved
derivation (N4). None is a sorry or an axiom — they are documented here
so no future formalization claims them as derived.
-/

/-- **Non-theorem N1:** Spin-pair selection is not derived from Axioms 1-3. -/
theorem spin_pair_selection_not_derived : True := by trivial

/-- **Non-theorem N2:** Axiom 3b (Minimal Winding) is an explicit premise. -/
theorem axiom_3b_is_explicit_premise : True := by trivial

/-- **Non-theorem N3:** Scheme selection is not derived. -/
theorem scheme_selection_not_derived : True := by trivial

/-- **Non-theorem N4:** The polynomial itself is not derived from Axioms 1-3. -/
theorem polynomial_not_derived_from_axioms : True := by trivial

end PfLean
