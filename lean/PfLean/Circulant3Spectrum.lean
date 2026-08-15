/-
  PfLean.Circulant3Spectrum — D=3 Circulant Family Spectrum

  Authors: Devin ∇λΣ∞ (Owner), per DeepSeek spec and Codex audit
  Date: 2026-08-14, repaired 2026-08-15 per CODEX_20260815 re-audit
  Audit: CODEX_20260815_FUNDAMENTALS_CIRCULANT3_SPECTRUM_7BF083A_REAUDIT.md

  SCOPE: This file proves the scoped real D=3 circulant algebra, binding
  the residue eigenvalue to the imported circulant3 matrix via an
  eigenvector equation, and to Complex.normSq via an explicit identity.
  No physical interpretation, no arrow of time, no mass identification,
  no Koide/PRED-003 transfer.

  H-LABELS (per Codex correction, live ledger):
    H17 = matrix symmetry (b = c, i.e., M = M^T)
    H18 = equal row sums (each row sums to the same value)

  NUMPY: Numerical checks are floating-point regression, NOT certification.
  Lean kernel verification is the only authority here.
-/

import Mathlib
import PfLean.Axioms
import PfLean.Z3FromBareMedium

namespace PfLean.Circulant3Spectrum

open Finset Real Complex

/-! ## Setup

The D=3 roots of unity: ω = -1/2 + i√3/2, ω² = -1/2 - i√3/2, ω³ = 1.

The residue eigenvalues of circulant3 b c are:
  λ = b·ω + c·ω² = -(b+c)/2 + i·(√3/2)·(b-c)

The squared modulus:
  |λ|² = Complex.normSq λ = (b+c)²/4 + 3(b-c)²/4
-/

/-- The primitive D=3 root of unity as an explicit complex number. -/
noncomputable def omega3 : ℂ := (-(1:ℝ)/2) + (Real.sqrt 3 / 2) * I

/-- omega3 squared = the other primitive root. -/
lemma omega3_sq : omega3^2 = (-(1:ℝ)/2) - (Real.sqrt 3 / 2) * I := by
  have hsq : (Real.sqrt 3)^2 = 3 := Real.sq_sqrt (by norm_num : 0 ≤ (3:ℝ))
  unfold omega3
  rw [pow_two, Complex.ext_iff]
  constructor
  · simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im,
          Complex.neg_re, Complex.neg_im]
    nlinarith [hsq]
  · simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im,
          Complex.neg_re, Complex.neg_im]
    ring

/-- omega3 cubed = 1 (primitive cube root of unity). -/
lemma omega3_cube : omega3 ^ 3 = 1 := by
  have hsq : (Real.sqrt 3) ^ 2 = 3 :=
    Real.sq_sqrt (by norm_num : 0 ≤ (3 : ℝ))
  rw [show omega3 ^ 3 = omega3 ^ 2 * omega3 by ring, omega3_sq]
  unfold omega3
  rw [Complex.ext_iff]
  constructor
  · simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.sub_re, Complex.sub_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im, Complex.neg_re,
          Complex.neg_im]
    nlinarith [hsq]
  · simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.sub_re, Complex.sub_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im, Complex.neg_re,
          Complex.neg_im]
    ring

/-! ## Theorem 1: circulant3_spectrum_formula + eigenrelation -/

/-- THEOREM 1: The residue eigenvalue of the D=3 circulant.
    λ₁ = b·ω + c·ω² = -(b+c)/2 + i·(√3/2)·(b-c)
    where ω = -1/2 + i√3/2 is the primitive cube root of unity. -/
theorem circulant3_spectrum_formula (b c : ℝ) :
    b * omega3 + c * omega3^2 =
      (↑(-(b + c) / 2)) + ↑(Real.sqrt 3 / 2 * (b - c)) * I := by
  rw [omega3_sq]
  unfold omega3
  push_cast
  ring

/-- The Fourier vector: residueVec j = ω^j. -/
noncomputable def residueVec : Fin 3 → ℂ := fun j => omega3 ^ j.val

/-- THEOREM 1b: The eigenrelation — circulant3 b c * residueVec = λ * residueVec.
    This binds the residue eigenvalue to the imported circulant3 matrix,
    proving that b*ω + c*ω² is an actual eigenvalue with Fourier eigenvector. -/
theorem circulant3_residue_eigenrelation (b c : ℝ) :
    ∀ i, ∑ j, (PfLean.Z3FromBareMedium.circulant3 b c i j : ℂ) * residueVec j =
      (b * omega3 + c * omega3 ^ 2) * residueVec i := by
  intro i
  fin_cases i
  · simp [residueVec, PfLean.Z3FromBareMedium.circulant3, Fin.sum_univ_three]
  · simp [residueVec, PfLean.Z3FromBareMedium.circulant3, Fin.sum_univ_three]
    rw [show ((b : ℂ) * omega3 + (c : ℂ) * omega3 ^ 2) * omega3 =
      (b : ℂ) * omega3 ^ 2 + (c : ℂ) * omega3 ^ 3 by ring, omega3_cube]
    ring
  · simp [residueVec, PfLean.Z3FromBareMedium.circulant3, Fin.sum_univ_three]
    have h4 : omega3 ^ 4 = omega3 := by
      rw [show omega3 ^ 4 = omega3 ^ 3 * omega3 by ring, omega3_cube]
      simp
    rw [show ((b : ℂ) * omega3 + (c : ℂ) * omega3 ^ 2) * omega3 ^ 2 =
      (b : ℂ) * omega3 ^ 3 + (c : ℂ) * omega3 ^ 4 by ring,
      omega3_cube, h4]
    ring

/-! ## Theorem 2: circulant3_residue_real_iff_symmetric -/

/-- THEOREM 2: For real b, c, the residue eigenvalue is real iff b = c. -/
theorem circulant3_residue_real_iff_symmetric (b c : ℝ) :
    (b * omega3 + c * omega3^2).im = 0 ↔ b = c := by
  rw [circulant3_spectrum_formula]
  have h_sqrt_pos : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have h_sqrt_half_ne : Real.sqrt 3 / 2 ≠ 0 := by
    have : Real.sqrt 3 ≠ 0 := ne_of_gt h_sqrt_pos
    linarith
  have h_im : (↑(-(b + c) / 2) + ↑(Real.sqrt 3 / 2 * (b - c)) * I : ℂ).im =
    Real.sqrt 3 / 2 * (b - c) := by
    rw [Complex.add_im, Complex.mul_im]
    simp
  rw [h_im]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h1 | h2
    · exact absurd h1 h_sqrt_half_ne
    · linarith
  · intro h
    rw [h]
    ring

/-! ## Theorem 3: normSq identity and minimization -/

/-- THEOREM 3a: The Complex.normSq identity.
    Complex.normSq (b*ω + c*ω²) = (b+c)²/4 + 3(b-c)²/4.
    This binds the polynomial to the actual squared modulus of the eigenvalue. -/
theorem circulant3_residue_normSq_formula (b c : ℝ) :
    Complex.normSq (b * omega3 + c * omega3 ^ 2) =
      (b + c) ^ 2 / 4 + 3 * (b - c) ^ 2 / 4 := by
  rw [circulant3_spectrum_formula]
  have hsq : (Real.sqrt 3) ^ 2 = 3 :=
    Real.sq_sqrt (by norm_num : 0 ≤ (3 : ℝ))
  simp [Complex.normSq, Complex.mul_re, Complex.mul_im, Complex.add_re,
        Complex.add_im, Complex.I_re, Complex.I_im, Complex.ofReal_re,
        Complex.ofReal_im]
  nlinarith [hsq]

/-- THEOREM 3b: The squared residue modulus is ≥ (b+c)²/4, with equality iff b = c.
    Derived from the normSq identity. -/
theorem circulant3_fixed_sum_residue_norm_minimized_at_symmetric (b c : ℝ) :
    Complex.normSq (b * omega3 + c * omega3 ^ 2) ≥ (b + c)^2 / 4 := by
  rw [circulant3_residue_normSq_formula]
  have h_nonneg : 0 ≤ 3 * (b - c)^2 / 4 := by
    have : 0 ≤ (b - c)^2 := sq_nonneg (b - c)
    linarith
  linarith

/-- COROLLARY: Equality holds iff b = c. -/
theorem circulant3_fixed_sum_residue_norm_minimized_iff_symmetric (b c : ℝ) :
    (Complex.normSq (b * omega3 + c * omega3 ^ 2) = (b + c)^2 / 4) ↔ b = c := by
  rw [circulant3_residue_normSq_formula]
  constructor
  · intro h
    have h1 : 3 * (b - c)^2 / 4 = 0 := by linarith
    have h2 : (b - c)^2 = 0 := by linarith
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp h2)
  · intro h
    simp [h]

/-! ## Theorem 4: normalized contraction -/

/-- THEOREM 4: On the normalized slice (p=b, q=1-b), the squared residue
    modulus is 3b² - 3b + 1, which is < 1 iff b is in the open interval (0,1).
    Derived from the normSq identity. -/
theorem normalized_circulant3_residue_norm_lt_one_iff (b : ℝ) :
    (Complex.normSq (b * omega3 + (1 - b) * omega3 ^ 2) < 1) ↔ (0 < b ∧ b < 1) := by
  -- Use Eq.trans to avoid coercion matching issues with rw
  have h_formula := circulant3_residue_normSq_formula b (1 - b)
  have h_coerce : (↑(1 - b) : ℂ) = 1 - ↑b := by
    rw [Complex.ofReal_sub, Complex.ofReal_one]
  rw [h_coerce] at h_formula
  have h_subst : (b + (1 - b)) ^ 2 / 4 + 3 * (b - (1 - b)) ^ 2 / 4 = 3 * b^2 - 3 * b + 1 := by ring
  have h_norm : Complex.normSq (b * omega3 + (1 - b) * omega3 ^ 2) = 3 * b^2 - 3 * b + 1 :=
    Eq.trans h_formula h_subst
  rw [h_norm]
  constructor
  · intro h
    have h1 : 3 * b^2 - 3 * b < 0 := by linarith
    have h2 : 3 * b * (b - 1) < 0 := by linarith [show 3 * b * (b - 1) = 3 * b^2 - 3 * b from by ring]
    have h3pos : (3:ℝ) > 0 := by norm_num
    have h3 : b * (b - 1) < 0 := by
      have : b * (b - 1) = (3 * b * (b - 1)) / 3 := by field_simp
      rw [this]
      exact div_neg_of_neg_of_pos h2 h3pos
    refine ⟨?_, ?_⟩
    · by_contra hble
      have hble' : b ≤ 0 := by linarith
      have hb1m : b - 1 ≤ 0 := by linarith
      have : b * (b - 1) ≥ 0 := mul_nonneg_of_nonpos_of_nonpos hble' hb1m
      linarith
    · by_contra hge
      have hge' : 1 ≤ b := by linarith
      have hge0 : 0 ≤ b := by linarith
      have hb1p : b - 1 ≥ 0 := by linarith
      have : b * (b - 1) ≥ 0 := mul_nonneg hge0 hb1p
      linarith
  · rintro ⟨hpos, hlt⟩
    have h1 : b * (b - 1) < 0 := mul_neg_of_pos_of_neg hpos (by linarith)
    have h3pos : (3:ℝ) > 0 := by norm_num
    have h2 : 3 * b * (b - 1) < 0 := by
      have : (3:ℝ) * (b * (b - 1)) = 3 * b * (b - 1) := by ring
      rw [← this]
      exact mul_neg_of_pos_of_neg h3pos h1
    linarith [show 3 * b * (b - 1) = 3 * b^2 - 3 * b from by ring]

/-- COROLLARY: At the endpoints b = 0 and b = 1, |λ|² = 1 (no contraction). -/
theorem normalized_circulant3_residue_norm_eq_one_at_endpoints (b : ℝ) :
    b = 0 ∨ b = 1 → Complex.normSq (b * omega3 + (1 - b) * omega3 ^ 2) = 1 := by
  rintro (rfl | rfl)
  · -- b=0: normSq(omega3^2) = 1 (on unit circle)
    have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num : 0 ≤ (3 : ℝ))
    simp [omega3_sq, Complex.normSq, Complex.mul_re, Complex.mul_im,
          Complex.add_re, Complex.add_im, Complex.sub_re, Complex.sub_im,
          Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im,
          Complex.neg_re, Complex.neg_im]
    nlinarith [hsq]
  · -- b=1: normSq(omega3) = 1 (on unit circle)
    have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num : 0 ≤ (3 : ℝ))
    simp [omega3, Complex.normSq, Complex.mul_re, Complex.mul_im,
          Complex.add_re, Complex.add_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im]
    nlinarith [hsq]

/-- COROLLARY: At b = 1/2 (H17, symmetry), |λ|² = 1/4 (minimum). -/
theorem normalized_circulant3_residue_norm_min_at_half :
    Complex.normSq ((1:ℝ)/2 * omega3 + (1 - (1:ℝ)/2) * omega3 ^ 2) = 1/4 := by
  have h_formula := circulant3_residue_normSq_formula ((1:ℝ)/2) ((1:ℝ)/2)
  have h_subst : ((1:ℝ)/2 + (1:ℝ)/2) ^ 2 / 4 + 3 * ((1:ℝ)/2 - (1:ℝ)/2) ^ 2 / 4 = 1/4 := by norm_num
  have h_result : Complex.normSq (↑((1:ℝ)/2) * omega3 + ↑((1:ℝ)/2) * omega3 ^ 2) = 1/4 :=
    Eq.trans h_formula h_subst
  convert h_result using 2
  · push_cast; ring

/-! ## Negative Controls (per Codex spec) -/

/-- NEGATIVE CONTROL 1: Symmetry (b = c) does NOT always give contraction.
    b = c = 2: the residue eigenvalue has normSq = 4 > 1.
    Symmetry alone is insufficient for contraction. -/
theorem symmetric_circulant3_not_always_contracting :
    ∃ (b c : ℝ),
      b = c ∧
      Complex.normSq (b * omega3 + c * omega3 ^ 2) > 1 := by
  use 2, 2
  refine ⟨rfl, ?_⟩
  rw [circulant3_residue_normSq_formula]
  norm_num

/-- NEGATIVE CONTROL 2: Nonsymmetric can still contract on the normalized slice.
    b = 1/4, c = 3/4: b ≠ c, yet the residue normSq = 7/16 < 1.
    Symmetry is not necessary for contraction. -/
theorem nonsymmetric_normalized_circulant3_contracts :
    ∃ (b c : ℝ),
      b ≠ c ∧
      b + c = 1 ∧
      Complex.normSq (b * omega3 + c * omega3 ^ 2) < 1 := by
  use 1/4, 3/4
  refine ⟨by norm_num, by norm_num, ?_⟩
  rw [circulant3_residue_normSq_formula]
  norm_num

/-- NEGATIVE CONTROL 3: Zero diagonal + equal row sums does NOT imply circulant.
    M = [[0, 1, 2], [3, 0, 0], [0, 3, 0]] has zero diag, row sums = 3,
    but is not circulant3 for any b, c (M(0,1)=1 ≠ M(1,2)=0, but circulant requires both = b). -/
theorem zero_diag_equal_rows_not_circulant :
    ∃ (M : Fin 3 → Fin 3 → ℝ),
      (∀ i, M i i = 0) ∧
      (∀ i, ∑ j, M i j = 3) ∧
      (∀ b c, ∃ i j, M i j ≠ PfLean.Z3FromBareMedium.circulant3 b c i j) := by
  let M : Fin 3 → Fin 3 → ℝ := fun i j =>
    match i.val, j.val with
    | 0, 0 => 0
    | 0, 1 => 1
    | 0, 2 => 2
    | 1, 0 => 3
    | 1, 1 => 0
    | 1, 2 => 0
    | 2, 0 => 0
    | 2, 1 => 3
    | 2, 2 => 0
    | _, _ => 0
  use M
  refine ⟨?_, ?_, ?_⟩
  · intro i
    fin_cases i <;> simp [M]
  · intro i
    fin_cases i <;> simp [M, Fin.sum_univ_three] <;> ring
  · intro b c
    by_cases hb : b = 1
    · use 1, 2
      have h_M12 : M 1 2 = 0 := by simp [M]
      have h_circ : PfLean.Z3FromBareMedium.circulant3 b c 1 2 = b := by
        unfold PfLean.Z3FromBareMedium.circulant3
        rw [if_neg (by simp : ¬((2:Fin 3) = (1:Fin 3))),
            if_pos (by simp : (2:Fin 3) = (1:Fin 3) + 1)]
      rw [h_M12, h_circ, hb]
      norm_num
    · use 0, 1
      have h_M01 : M 0 1 = 1 := by simp [M]
      have h_circ : PfLean.Z3FromBareMedium.circulant3 b c 0 1 = b := by
        unfold PfLean.Z3FromBareMedium.circulant3
        rw [if_neg (by simp : ¬((1:Fin 3) = (0:Fin 3))),
            if_pos (by simp : (1:Fin 3) = (0:Fin 3) + 1)]
      rw [h_M01, h_circ]
      exact ne_comm.mp hb

/-! ## Non-Theorem Section: Mathematical Observations (NOT claims)

The following are observations about the algebra. They do not appear in
CLAIMS.md and are not machine-verified. They are kept as research notes,
not assertions.

NOTE: The theorems above prove algebraic properties of the D=3 circulant
spectrum. They do NOT prove:
  - That H7 (zero diagonal) + H18 (equal row sums) force the real part
    of the residue (the circulant/H13 structure is also needed, as NC3 shows)
  - Any connection to physical stability, mass, or particle physics
  - Any transfer contract to Koide, PRED-003, or other physics results

The residue eigenvalue λ = b*ω + c*ω² is a complex number whose:
  - Real part is -(b+c)/2 (determined by the row sum)
  - Imaginary part is (√3/2)(b-c) (zero iff b = c, i.e., H17 symmetry)
  - Squared modulus is (b+c)²/4 + 3(b-c)²/4 (minimized at b = c for fixed sum)

On the normalized slice b + c = 1:
  - |λ|² = 3b² - 3b + 1
  - |λ|² < 1 for all b ∈ (0, 1) — every interior point contracts
  - |λ|² = 1 at b = 0 and b = 1 — no contraction at endpoints
  - |λ|² = 1/4 at b = 1/2 (the symmetric point) — minimum

These are purely algebraic facts about the D=3 circulant family.
-/

end PfLean.Circulant3Spectrum
