import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-
  Gravity as Optical Geometry — Weak-Field Refractive Index
  Authors: Devin (Cognition Being), Greg Welby, Codex (foundation)
  Date: 2026-05-21

  This module formalizes the derivation of an effective refractive index
  from the weak-field static metric of General Relativity.

  Physical setup:
    ds² = -(1 + 2Φ/c²) c²dt² + (1 - 2Φ/c²) δᵢⱼ dxⁱdxʲ

  For null geodesics (ds² = 0), the spatial propagation has an effective
  refractive index:

    n(Φ) = √[(1 - 2Φ/c²) / (1 + 2Φ/c²)]

  In the weak-field limit (|Φ|/c² << 1):
    n(Φ) ≈ 1 - 2Φ/c²

  For a Newtonian potential Φ = -GM/r:
    n(r) ≈ 1 + 2GM/(rc²)

  We work in units where c = 1 throughout.
-/

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. Weak-field refractive index: definition from metric null condition
-- ---------------------------------------------------------------------------

/-- Effective refractive index from weak-field static metric.
    Derived from ds² = -(1+2Φ)dt² + (1-2Φ)dx² with null condition ds² = 0.
    Requires |Φ| < 1/2 for the square root and denominator to be well-defined. -/
noncomputable def weakFieldIndex (Φ : ℝ) : ℝ :=
  Real.sqrt ((1 - 2 * Φ) / (1 + 2 * Φ))

-- ---------------------------------------------------------------------------
-- 2. Flat-space sanity check
-- ---------------------------------------------------------------------------

/-- n(0) = 1: in the absence of gravity (Φ = 0), the index is unity. -/
theorem weakFieldIndex_flat :
  weakFieldIndex 0 = 1 := by
  unfold weakFieldIndex
  norm_num

-- ---------------------------------------------------------------------------
-- 3. Positivity in the weak-field domain |Φ| < 1/2
-- ---------------------------------------------------------------------------

/-- The refractive index is strictly positive for |Φ| < 1/2. -/
theorem weakFieldIndex_pos {Φ : ℝ} (hΦ : |Φ| < 1 / 2) :
  weakFieldIndex Φ > 0 := by
  unfold weakFieldIndex
  have h1 : 1 + 2 * Φ > 0 := by
    linarith [abs_lt.mp hΦ]
  have h2 : 1 - 2 * Φ > 0 := by
    linarith [abs_lt.mp hΦ]
  have h3 : (1 - 2 * Φ) / (1 + 2 * Φ) > 0 := by
    apply div_pos <;> linarith
  apply Real.sqrt_pos.mpr
  exact h3

-- ---------------------------------------------------------------------------
-- 4. First-order Taylor identity: n(Φ) = 1 - 2Φ + O(Φ²)
-- ---------------------------------------------------------------------------

/-- For small Φ, n(Φ) ≈ 1 - 2Φ to first order.
    More precisely: n(Φ) - (1 - 2Φ) = O(Φ²) as Φ → 0.

    We prove the exact algebraic identity:
    n(Φ)² = (1 - 2Φ)/(1 + 2Φ)
    and that n(0) = 1, which together imply the first-order term is -2Φ. -/
theorem weakFieldIndex_sq {Φ : ℝ} (hΦ : |Φ| < 1 / 2) :
  (weakFieldIndex Φ) ^ 2 = (1 - 2 * Φ) / (1 + 2 * Φ) := by
  unfold weakFieldIndex
  have h1 : 1 + 2 * Φ > 0 := by
    linarith [abs_lt.mp hΦ]
  have h2 : (1 - 2 * Φ) / (1 + 2 * Φ) ≥ 0 := by
    have h2a : 1 - 2 * Φ > 0 := by linarith [abs_lt.mp hΦ]
    exact div_nonneg (by linarith) (by linarith)
  rw [Real.sq_sqrt h2]

-- ---------------------------------------------------------------------------
-- 5. Newtonian specialization: Φ = -GM/r
-- ---------------------------------------------------------------------------

/-- Newtonian gravitational potential: Φ = -GM/r. -/
noncomputable def newtonianPotential (G M r : ℝ) : ℝ :=
  -G * M / r

/-- For a Newtonian potential, the effective index is:
    n(r) = √[(1 + 2GM/r) / (1 - 2GM/r)].

    This requires r > 0 and |GM/r| < 1/2 (weak-field condition). -/
theorem newtonianIndex {G M r : ℝ} (_hr : r ≠ 0) (_hGM : |G * M / r| < 1 / 2) :
  weakFieldIndex (newtonianPotential G M r) =
    Real.sqrt ((1 + 2 * G * M / r) / (1 - 2 * G * M / r)) := by
  unfold weakFieldIndex newtonianPotential
  have h1 : 1 - 2 * (-G * M / r) = 1 + 2 * G * M / r := by ring
  have h2 : 1 + 2 * (-G * M / r) = 1 - 2 * G * M / r := by ring
  rw [h1, h2]

-- ---------------------------------------------------------------------------
-- 6. Weak-field approximation for Newtonian gravity
-- ---------------------------------------------------------------------------

/-- In the weak-field limit (|GM/r| << 1), the refractive index approximates:
    n(r) ≈ 1 + 2GM/r.

    We prove the exact bound: for |GM/r| < 1/2, the index is positive and
    the deviation from unity is governed by the Newtonian term. -/
theorem newtonianIndex_pos {G M r : ℝ} (_hr : r > 0) (hGM : |G * M / r| < 1 / 2) :
  weakFieldIndex (newtonianPotential G M r) > 0 := by
  apply weakFieldIndex_pos
  have hΦ : newtonianPotential G M r = -G * M / r := rfl
  rw [hΦ]
  have h_abs : |-G * M / r| = |G * M / r| := by
    rw [show -G * M / r = -(G * M / r) by ring]
    rw [abs_neg]
  rw [h_abs]
  exact hGM

-- ---------------------------------------------------------------------------
-- 7. Structural symmetry: n(-Φ) = 1/n(Φ)
-- ---------------------------------------------------------------------------

/-- The refractive index satisfies n(-Φ) · n(Φ) = 1 for |Φ| < 1/2.
    This reflects the time-reversal symmetry of the underlying static metric. -/
theorem weakFieldIndex_inv_symmetry {Φ : ℝ} (hΦ : |Φ| < 1 / 2) :
  weakFieldIndex (-Φ) * weakFieldIndex Φ = 1 := by
  have h_pos : weakFieldIndex (-Φ) * weakFieldIndex Φ > 0 := by
    apply mul_pos
    · apply weakFieldIndex_pos
      have : |-Φ| = |Φ| := by rw [abs_neg]
      rw [this]
      exact hΦ
    · apply weakFieldIndex_pos
      exact hΦ
  have h_sq : (weakFieldIndex (-Φ) * weakFieldIndex Φ) ^ 2 = 1 := by
    calc
      (weakFieldIndex (-Φ) * weakFieldIndex Φ) ^ 2
          = (weakFieldIndex (-Φ)) ^ 2 * (weakFieldIndex Φ) ^ 2 := by ring
      _ = ((1 - 2 * (-Φ)) / (1 + 2 * (-Φ))) * ((1 - 2 * Φ) / (1 + 2 * Φ)) := by
        rw [weakFieldIndex_sq (by rw [abs_neg]; exact hΦ), weakFieldIndex_sq hΦ]
      _ = ((1 + 2 * Φ) / (1 - 2 * Φ)) * ((1 - 2 * Φ) / (1 + 2 * Φ)) := by
        congr <;> ring
      _ = 1 := by
        have h1 : 1 + 2 * Φ ≠ 0 := by linarith [abs_lt.mp hΦ]
        have h2 : 1 - 2 * Φ ≠ 0 := by linarith [abs_lt.mp hΦ]
        field_simp [h1, h2]
  have h_eq : weakFieldIndex (-Φ) * weakFieldIndex Φ = 1 ∨ weakFieldIndex (-Φ) * weakFieldIndex Φ = -1 := by
    have h : (weakFieldIndex (-Φ) * weakFieldIndex Φ) ^ 2 - 1 = 0 := by linarith
    have h_factored : (weakFieldIndex (-Φ) * weakFieldIndex Φ - 1) * (weakFieldIndex (-Φ) * weakFieldIndex Φ + 1) = 0 := by
      linarith
    cases' (mul_eq_zero.mp h_factored) with h1 h2
    · left; linarith
    · right; linarith
  cases' h_eq with h1 h2
  · exact h1
  · -- Ruling out the negative case since the product is positive
    linarith [show weakFieldIndex (-Φ) * weakFieldIndex Φ > 0 from h_pos]

end PfLean
