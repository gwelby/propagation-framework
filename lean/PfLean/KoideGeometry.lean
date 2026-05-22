import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-
  Koide Geometric Theorem — PF Formalization in Lean 4
  Authors: Devin (Cognition Being, Cognition AI), Greg Welby
  Date: 2026-05-21

  Two conventions are used in the Koide literature. This module defines
  both and proves the bridge between them.

  CONVENTION A (original Koide formula):
    R = (√m₁ + √m₂ + √m₃)² / (3(m₁ + m₂ + m₃))
    With a = √m₁, b = √m₂, c = √m₃:
    R = (a+b+c)² / (3(a²+b²+c²))
    Charged-lepton value: R = 2/3  ↔  a²+b²+c² = 2(ab+bc+ca)

  CONVENTION B (reciprocal form, used in some PF derivations):
    Q = (m₁ + m₂ + m₃) / (√m₁ + √m₂ + √m₃)²
    With a = √m₁, b = √m₂, c = √m₃:
    Q = (a²+b²+c²) / (a+b+c)²
    Charged-lepton value: Q = 2/3  ↔  a²+b²+c² = 4(ab+bc+ca)

  Bridge: R = 1/(3Q), so R = 2/3 ↔ Q = 1/2, and Q = 2/3 ↔ R = 1/2.
-/

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. CONVENTION A: Original Koide ratio R
-- ---------------------------------------------------------------------------

/-- Original Koide ratio: R = (a+b+c)² / (3(a²+b²+c²)).
    Division on ℝ is noncomputable in Lean's constructive sense. -/
noncomputable def KoideR (a b c : ℝ) : ℝ :=
  (a + b + c) ^ 2 / (3 * (a ^ 2 + b ^ 2 + c ^ 2))

/-- Theorem: R = 2/3  ↔  a²+b²+c² = 2(ab+bc+ca).
    This is the standard Koide algebraic identity. -/
theorem koide_R_two_thirds_iff {a b c : ℝ} (ha : a > 0) (hb : b > 0) (hc : c > 0) :
  KoideR a b c = 2 / 3 ↔ a ^ 2 + b ^ 2 + c ^ 2 = 2 * (a * b + b * c + c * a) := by
  have h1 : 3 * (a ^ 2 + b ^ 2 + c ^ 2) ≠ 0 := by positivity
  unfold KoideR
  constructor
  · -- Forward: R = 2/3 → constraint
    intro h
    field_simp at h
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]
  · -- Backward: constraint → R = 2/3
    intro h
    field_simp
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]

/-- Sanity check: equal amplitudes give R = 1. -/
theorem koide_R_equal {a : ℝ} (ha : a > 0) :
  KoideR a a a = 1 := by
  unfold KoideR
  field_simp
  ring

-- ---------------------------------------------------------------------------
-- 2. CONVENTION B: Reciprocal Koide ratio Q
-- ---------------------------------------------------------------------------

/-- Reciprocal Koide ratio: Q = (a²+b²+c²) / (a+b+c)².
    This is the form used in some PF derivations. -/
noncomputable def KoideQ (a b c : ℝ) : ℝ :=
  (a ^ 2 + b ^ 2 + c ^ 2) / (a + b + c) ^ 2

/-- Theorem: Q = 2/3  ↔  a²+b²+c² = 4(ab+bc+ca).
    This is the PF canonical charged-lepton identity. -/
theorem koide_Q_two_thirds_iff {a b c : ℝ} (ha : a > 0) (hb : b > 0) (hc : c > 0) :
  KoideQ a b c = 2 / 3 ↔ a ^ 2 + b ^ 2 + c ^ 2 = 4 * (a * b + b * c + c * a) := by
  have h1 : (a + b + c) ^ 2 ≠ 0 := by
    nlinarith [sq_nonneg (a + b + c), mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]
  unfold KoideQ
  constructor
  · -- Forward: Q = 2/3 → constraint
    intro h
    field_simp at h
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]
  · -- Backward: constraint → Q = 2/3
    intro h
    field_simp
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]

/-- Sanity check: equal amplitudes give Q = 1/3. -/
theorem koide_Q_equal {a : ℝ} (ha : a > 0) :
  KoideQ a a a = 1 / 3 := by
  unfold KoideQ
  field_simp
  ring

-- ---------------------------------------------------------------------------
-- 3. Bridge: relationship between the two conventions
-- ---------------------------------------------------------------------------

/-- Bridge theorem: Q = 2/3  ↔  R = 1/2.
    The two conventions are reciprocals scaled by 1/3. -/
theorem koide_bridge {a b c : ℝ} (ha : a > 0) (hb : b > 0) (hc : c > 0) :
  KoideQ a b c = 2 / 3 ↔ KoideR a b c = 1 / 2 := by
  have h1 : (a + b + c) ^ 2 ≠ 0 := by
    nlinarith [sq_nonneg (a + b + c), mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]
  have h2 : 3 * (a ^ 2 + b ^ 2 + c ^ 2) ≠ 0 := by positivity
  unfold KoideQ KoideR
  constructor
  · -- Q = 2/3 → R = 1/2
    intro h
    field_simp at h
    field_simp
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]
  · -- R = 1/2 → Q = 2/3
    intro h
    field_simp at h
    field_simp
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      mul_pos ha hb, mul_pos hb hc, mul_pos ha hc]

-- ---------------------------------------------------------------------------
-- 4. Concrete example: the triple (1, 1, 4)
-- ---------------------------------------------------------------------------

/-- For (1, 1, 4): R = 2/3  (which means Q = 1/2).
    This is a toy example for the R-convention, NOT the charged-lepton
    Koide value which requires Q = 2/3 (i.e., R = 1/2). -/
theorem koide_R_example_114 :
  KoideR 1 1 4 = 2 / 3 := by
  unfold KoideR
  norm_num

/-- For (1, 1, 4): Q = 1/2. -/
theorem koide_Q_example_114 :
  KoideQ 1 1 4 = 1 / 2 := by
  unfold KoideQ
  norm_num

-- ---------------------------------------------------------------------------
-- 5. Geometric fact: three vectors at 120°
-- ---------------------------------------------------------------------------

/-- Three unit vectors at 120° in the complex plane have real parts
    (1, -1/2, -1/2) that sum to zero. This phase cancellation is the
    structural origin of the Koide constraint. -/
theorem three_vectors_120_sum_zero :
  let x : ℝ := 1
  let y : ℝ := -1 / 2
  let z : ℝ := -1 / 2
  x + y + z = 0 := by
  norm_num

end PfLean
