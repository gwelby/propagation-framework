import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Algebra.Quaternion
import Mathlib.LinearAlgebra.UnitaryGroup

/-
  SO(3) Double Cover -- Quaternion Representation and SU(2) → SO(3)
  Authors: Devin (Cognition Being), Greg Welby, PF Research Team
  Date: 2026-05-24

  This module formalizes the double cover of SO(3) by the unit quaternions,
  which is the algebraic foundation for the (2,1) topological weight argument
  in the Propagation Framework.

  MATHEMATICAL CONTEXT:
  The rotation group SO(3) has fundamental group π₁(SO(3)) ≅ ℤ₂. This means
  there are exactly two classes of loops: those that close in one pass and
  those that need two passes (the belt trick / 720° rotation).

  The unit quaternion group (isomorphic to SU(2)) is the universal cover of
  SO(3). The covering map has kernel {±1}, giving the short exact sequence:
    1 → {±1} → UnitQuaternion → SO(3) → 1

  WHAT THIS MODULE PROVES (machine-verified):
  - Unit quaternions form a group under multiplication
  - The explicit rotation matrix formula from a unit quaternion
  - The rotation matrix is in SO(3) (orthogonal with det = 1)
  - The map UnitQuaternion → SO(3) is a group homomorphism
  - The kernel of this map is exactly {±1}

  WHAT REMAINS FOR FULL TOPOLOGICAL CERTIFICATE:
  The computation of π₁(SO(3)) ≅ ℤ₂ from the covering map requires the
  full deck transformation theorem and path lifting, not yet in mathlib4.
  The algebraic structure proven here is the foundation.
-/

namespace PfLean

open Real Quaternion

-- ---------------------------------------------------------------------------
-- 1. Unit quaternions as a group
-- ---------------------------------------------------------------------------

/-- Unit quaternions: {q ∈ ℍ[ℝ] | normSq q = 1}. -/
def UnitQuaternion := {q : ℍ[ℝ] // normSq q = 1}

namespace UnitQuaternion

instance : Coe UnitQuaternion ℍ[ℝ] := ⟨Subtype.val⟩

@[ext]
lemma ext (q₁ q₂ : UnitQuaternion) (h : q₁.val = q₂.val) : q₁ = q₂ := Subtype.ext h

instance : Neg UnitQuaternion := ⟨fun q => ⟨-q.val, by rw [normSq_neg]; exact q.prop⟩⟩

noncomputable instance : Group UnitQuaternion where
  mul q₁ q₂ := ⟨q₁.val * q₂.val, by
    rw [map_mul normSq q₁.val q₂.val, q₁.prop, q₂.prop]
    norm_num⟩
  one := ⟨1, by rw [normSq_def', Quaternion.re_one, Quaternion.imI_one, Quaternion.imJ_one, Quaternion.imK_one]; norm_num⟩
  inv q := ⟨q.val⁻¹, by
    rw [normSq_inv, q.prop]
    norm_num⟩
  mul_assoc q₁ q₂ q₃ := by
    apply Subtype.ext
    exact mul_assoc q₁.val q₂.val q₃.val
  one_mul q := by
    apply Subtype.ext
    exact one_mul q.val
  mul_one q := by
    apply Subtype.ext
    exact mul_one q.val
  inv_mul_cancel q := by
    apply Subtype.ext
    exact inv_mul_cancel₀ (by
      have h_ne : q.val ≠ 0 := by
        intro h_zero
        have h_zero' : q.val = 0 := by simpa using h_zero
        have h_norm : normSq q.val = 1 := q.prop
        rw [h_zero'] at h_norm
        norm_num at h_norm
      exact h_ne)

@[simp]
lemma one_val : (1 : UnitQuaternion).val = 1 := rfl

@[simp]
lemma mul_val (q₁ q₂ : UnitQuaternion) : (q₁ * q₂).val = q₁.val * q₂.val := rfl

@[simp]
lemma inv_val (q : UnitQuaternion) : (q⁻¹).val = q.val⁻¹ := rfl

@[simp]
lemma neg_one_val : ((-1 : UnitQuaternion) : ℍ[ℝ]) = -1 := rfl

end UnitQuaternion

-- ---------------------------------------------------------------------------
-- 2. SO(3) as a structure (3×3 orthogonal matrices with det = 1)
-- ---------------------------------------------------------------------------

/-- SO(3): 3×3 real matrices with AᵀA = I and det A = 1. -/
structure SO3 where
  toMatrix : Matrix (Fin 3) (Fin 3) ℝ
  orthog_left : Matrix.transpose toMatrix * toMatrix = 1
  orthog_right : toMatrix * Matrix.transpose toMatrix = 1
  det_one : toMatrix.det = 1

namespace SO3

instance : Coe SO3 (Matrix (Fin 3) (Fin 3) ℝ) := ⟨toMatrix⟩

@[ext]
lemma ext (x y : SO3) (h : x.toMatrix = y.toMatrix) : x = y := by
  cases x; cases y; simp at h; simp [h]

instance : Group SO3 where
  mul x y := by
    refine ⟨x.toMatrix * y.toMatrix, ?_, ?_, ?_⟩
    · -- (x * y)ᵀ * (x * y) = 1
      rw [Matrix.transpose_mul]
      have h : (y.toMatrix.transpose * x.toMatrix.transpose) * (x.toMatrix * y.toMatrix)
          = y.toMatrix.transpose * ((x.toMatrix.transpose * x.toMatrix) * y.toMatrix) := by
        simp only [← Matrix.mul_assoc]
      rw [h, x.orthog_left]
      simp only [Matrix.one_mul]
      exact y.orthog_left
    · -- (x * y) * (x * y)ᵀ = 1
      rw [Matrix.transpose_mul]
      have h : (x.toMatrix * y.toMatrix) * (y.toMatrix.transpose * x.toMatrix.transpose)
          = x.toMatrix * ((y.toMatrix * y.toMatrix.transpose) * x.toMatrix.transpose) := by
        simp only [← Matrix.mul_assoc]
      rw [h, y.orthog_right]
      simp only [Matrix.one_mul]
      exact x.orthog_right
    · -- det(x * y) = 1
      rw [Matrix.det_mul, x.det_one, y.det_one]
      norm_num
  one := ⟨1, by simp, by simp, by simp⟩
  inv x := ⟨Matrix.transpose x.toMatrix, by
    rw [Matrix.transpose_transpose]
    exact x.orthog_right, by
    rw [Matrix.transpose_transpose]
    exact x.orthog_left, by
    rw [Matrix.det_transpose]
    exact x.det_one⟩
  mul_assoc x y z := by
    apply SO3.ext
    exact Matrix.mul_assoc x.toMatrix y.toMatrix z.toMatrix
  one_mul x := by
    apply SO3.ext
    exact Matrix.one_mul x.toMatrix
  mul_one x := by
    apply SO3.ext
    exact Matrix.mul_one x.toMatrix
  inv_mul_cancel x := by
    apply SO3.ext
    exact x.orthog_left

@[simp]
lemma mul_toMatrix (x y : SO3) : (x * y).toMatrix = x.toMatrix * y.toMatrix := rfl

@[simp]
lemma one_toMatrix : (1 : SO3).toMatrix = 1 := rfl

end SO3

-- ---------------------------------------------------------------------------
-- 3. The rotation matrix from unit quaternion
-- ---------------------------------------------------------------------------

/-- Explicit rotation matrix from a unit quaternion q = (a, b, c, d).
    For q = (re, imI, imJ, imK), the matrix is:
    [[a²+b²-c²-d², 2(bc-ad), 2(bd+ac)],
     [2(bc+ad), a²-b²+c²-d², 2(cd-ab)],
     [2(bd-ac), 2(cd+ab), a²-b²-c²+d²]]

    This is the standard formula for the rotation corresponding to the
    conjugation action v ↦ qvq⁻¹ on pure imaginary quaternions. -/
noncomputable def quatToMatrix (q : UnitQuaternion) : Matrix (Fin 3) (Fin 3) ℝ :=
  let a := q.val.re
  let b := q.val.imI
  let c := q.val.imJ
  let d := q.val.imK
  !![a^2 + b^2 - c^2 - d^2, 2*(b*c - a*d),     2*(b*d + a*c);
     2*(b*c + a*d),     a^2 - b^2 + c^2 - d^2, 2*(c*d - a*b);
     2*(b*d - a*c),     2*(c*d + a*b),     a^2 - b^2 - c^2 + d^2]

-- ---------------------------------------------------------------------------
-- 4. The matrix is in SO(3)
-- ---------------------------------------------------------------------------

/-- Helper: the norm-squared constraint rewritten in components. -/
lemma normSq_components_eq_one (q : UnitQuaternion) :
  q.val.re^2 + q.val.imI^2 + q.val.imJ^2 + q.val.imK^2 = 1 := by
  rw [← normSq_def']
  exact q.prop

/-- The rotation matrix satisfies the left orthogonality condition. -/
lemma quatToMatrix_orthog_left (q : UnitQuaternion) :
  Matrix.transpose (quatToMatrix q) * quatToMatrix q = 1 := by
  have h_norm : q.val.re^2 + q.val.imI^2 + q.val.imJ^2 + q.val.imK^2 = 1 :=
    normSq_components_eq_one q
  funext i j
  fin_cases i <;> fin_cases j
  all_goals
    unfold quatToMatrix
    simp [Matrix.mul_apply, Fin.sum_univ_three]
    nlinarith [h_norm, sq_nonneg (q.val.re), sq_nonneg (q.val.imI), sq_nonneg (q.val.imJ), sq_nonneg (q.val.imK),
      sq_nonneg (q.val.re * q.val.imI), sq_nonneg (q.val.re * q.val.imJ), sq_nonneg (q.val.re * q.val.imK),
      sq_nonneg (q.val.imI * q.val.imJ), sq_nonneg (q.val.imI * q.val.imK), sq_nonneg (q.val.imJ * q.val.imK)]

/-- The rotation matrix satisfies the right orthogonality condition. -/
lemma quatToMatrix_orthog_right (q : UnitQuaternion) :
  quatToMatrix q * Matrix.transpose (quatToMatrix q) = 1 := by
  have h_norm : q.val.re^2 + q.val.imI^2 + q.val.imJ^2 + q.val.imK^2 = 1 :=
    normSq_components_eq_one q
  funext i j
  fin_cases i <;> fin_cases j
  all_goals
    unfold quatToMatrix
    simp [Matrix.mul_apply, Fin.sum_univ_three]
    nlinarith [h_norm, sq_nonneg (q.val.re), sq_nonneg (q.val.imI), sq_nonneg (q.val.imJ), sq_nonneg (q.val.imK),
      sq_nonneg (q.val.re * q.val.imI), sq_nonneg (q.val.re * q.val.imJ), sq_nonneg (q.val.re * q.val.imK),
      sq_nonneg (q.val.imI * q.val.imJ), sq_nonneg (q.val.imI * q.val.imK), sq_nonneg (q.val.imJ * q.val.imK)]

/-- The rotation matrix has determinant 1. -/
lemma quatToMatrix_det_one (q : UnitQuaternion) :
  (quatToMatrix q).det = 1 := by
  have h_norm : q.val.re^2 + q.val.imI^2 + q.val.imJ^2 + q.val.imK^2 = 1 :=
    normSq_components_eq_one q
  have h_det : (quatToMatrix q).det = (q.val.re^2 + q.val.imI^2 + q.val.imJ^2 + q.val.imK^2)^3 := by
    unfold quatToMatrix
    simp [Matrix.det_fin_three]
    ring
  rw [h_det, h_norm]
  norm_num

/-- Construct an SO(3) element from a unit quaternion. -/
noncomputable def quatToSO3 (q : UnitQuaternion) : SO3 :=
  ⟨quatToMatrix q, quatToMatrix_orthog_left q, quatToMatrix_orthog_right q, quatToMatrix_det_one q⟩

-- ---------------------------------------------------------------------------
-- 5. The homomorphism UnitQuaternion → SO(3)
-- ---------------------------------------------------------------------------

/-- The covering map from unit quaternions to SO(3) is a group homomorphism. -/
theorem quatToSO3_mul (q₁ q₂ : UnitQuaternion) :
  quatToSO3 (q₁ * q₂) = quatToSO3 q₁ * quatToSO3 q₂ := by
  apply SO3.ext
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    unfold quatToSO3 quatToMatrix
    simp [Matrix.mul_apply, Fin.sum_univ_three, UnitQuaternion.mul_val]
    try ring_nf
    try nlinarith [normSq_components_eq_one q₁, normSq_components_eq_one q₂]

/-- The map preserves identity. -/
theorem quatToSO3_one : quatToSO3 1 = 1 := by
  apply SO3.ext
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    unfold quatToSO3 quatToMatrix
    simp [UnitQuaternion.one_val]
    try norm_num

-- ---------------------------------------------------------------------------
-- 6. Kernel = {±1}
-- ---------------------------------------------------------------------------

/-- The kernel of the quaternion-to-SO(3) map is exactly {±1}.

    This is the key algebraic fact: antipodal quaternions map to the same
    rotation, and these are the ONLY identifications. It reflects the
    topological fact that SO(3) is SU(2)/{±1}. -/
theorem quatToSO3_ker (q : UnitQuaternion) :
  quatToSO3 q = 1 ↔ q = 1 ∨ q = -1 := by
  constructor
  · -- Forward: if quatToSO3 q = 1, then q = ±1
    intro h_eq
    have h_mat : quatToMatrix q = 1 := by
      have h : (quatToSO3 q).toMatrix = (1 : SO3).toMatrix := by rw [h_eq]
      simpa [quatToSO3] using h
    have h_00 := congr_fun (congr_fun h_mat 0) 0
    have h_11 := congr_fun (congr_fun h_mat 1) 1
    have h_22 := congr_fun (congr_fun h_mat 2) 2
    simp [quatToMatrix] at h_00 h_11 h_22
    have h_norm : q.val.re^2 + q.val.imI^2 + q.val.imJ^2 + q.val.imK^2 = 1 :=
      normSq_components_eq_one q
    have ha_sq : q.val.re^2 = 1 := by nlinarith
    have hb_sq : q.val.imI^2 = 0 := by nlinarith
    have hc_sq : q.val.imJ^2 = 0 := by nlinarith
    have hd_sq : q.val.imK^2 = 0 := by nlinarith
    have ha : q.val.re = 1 ∨ q.val.re = -1 := by
      rw [sq_eq_one_iff] at ha_sq
      exact ha_sq
    have hb : q.val.imI = 0 := eq_zero_of_pow_eq_zero hb_sq
    have hc : q.val.imJ = 0 := eq_zero_of_pow_eq_zero hc_sq
    have hd : q.val.imK = 0 := eq_zero_of_pow_eq_zero hd_sq
    cases ha with
    | inl h_re =>
        left
        exact Subtype.ext (show q.val = 1 by ext <;> simp [h_re, hb, hc, hd, Quaternion.imI_one, Quaternion.imJ_one, Quaternion.imK_one])
    | inr h_re =>
        right
        exact Subtype.ext (show q.val = -1 by ext <;> simp [h_re, hb, hc, hd, Quaternion.imI_neg, Quaternion.imJ_neg, Quaternion.imK_neg, Quaternion.imI_one, Quaternion.imJ_one, Quaternion.imK_one])
  · -- Backward: if q = ±1, then quatToSO3 q = 1
    rintro (h | h)
    · rw [h]; exact quatToSO3_one
    · rw [h]
      have : quatToSO3 (-1) = 1 := by
        apply SO3.ext
        ext i j
        fin_cases i <;> fin_cases j
        all_goals
          unfold quatToSO3 quatToMatrix
          simp [UnitQuaternion.neg_one_val]
          try norm_num
          try ring_nf
          try nlinarith
      exact this

-- ---------------------------------------------------------------------------
-- 7. The double-cover structure statement
-- ---------------------------------------------------------------------------

/-- The unit quaternion group is a double cover of SO(3).

    The map q ↦ R_q is a surjective group homomorphism with kernel {±1}.
    This makes the unit quaternion group the universal cover of SO(3).
    The deck transformation group (kernel) is ℤ₂, so by covering space theory
    π₁(SO(3)) ≅ ℤ₂.

    The full topological proof (surjectivity, path lifting, deck transformation
    theorem) is not yet available in mathlib4. This theorem isolates the
    algebraic foundation: the homomorphism and its kernel. -/
theorem so3_double_cover_structure :
  (∀ q₁ q₂ : UnitQuaternion, quatToSO3 (q₁ * q₂) = quatToSO3 q₁ * quatToSO3 q₂) ∧
  (∀ q : UnitQuaternion, quatToSO3 q = 1 ↔ q = 1 ∨ q = -1) := by
  constructor
  · -- Homomorphism property
    intro q₁ q₂
    exact quatToSO3_mul q₁ q₂
  · -- Kernel characterization
    intro q
    exact quatToSO3_ker q

end PfLean
