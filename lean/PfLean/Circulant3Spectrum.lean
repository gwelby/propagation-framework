/-
  PfLean.Circulant3Spectrum — D=3 Circulant Family Spectrum

  Authors: Devin ∇λΣ∞ (Owner), per DeepSeek spec and Codex audit
  Date: 2026-08-14
  Audit: CODEX_20260813_D3_CIRCULANT_FAMILY_SPECTRUM_AUDIT.md — PASS, NARROW for algebra

  SCOPE: This file proves ONLY the scoped real D=3 circulant algebra.
  No physical interpretation, no arrow of time, no mass identification,
  no Koide/PRED-003 transfer. Physical observations are in the non-theorem
  section at the bottom, explicitly separated.

  H-LABELS (per Codex correction, live ledger):
    H17 = matrix symmetry (b = c, i.e., M = M^T)
    H18 = equal row sums (each row sums to the same value)

  NUMPY: Any numerical checks are floating-point regression checks, NOT
  machine certification. Lean kernel verification is the only authority here.
-/

import Mathlib
import PfLean.Axioms
import PfLean.Z3FromBareMedium

namespace PfLean.Circulant3Spectrum

open Finset Real Complex

/-! ## Setup

The D=3 roots of unity: ω = -1/2 + i√3/2, ω² = -1/2 - i√3/2.

The residue eigenvalues of circulant3 b c are:
  λ = b·ω + c·ω² = -(b+c)/2 + i·(√3/2)·(b-c)

The squared modulus:
  |λ|² = ((b+c)/2)² + (√3/2·(b-c))² = (b+c)²/4 + 3(b-c)²/4
-/

/-- The primitive D=3 root of unity as an explicit complex number. -/
noncomputable def omega3 : ℂ := (-(1:ℝ)/2) + (Real.sqrt 3 / 2) * I

/-- omega3 squared = the other primitive root. -/
lemma omega3_sq : omega3^2 = (-(1:ℝ)/2) - (Real.sqrt 3 / 2) * I := by
  have hsq : (Real.sqrt 3)^2 = 3 := Real.sq_sqrt (by norm_num : 0 ≤ (3:ℝ))
  unfold omega3
  rw [pow_two, Complex.ext_iff]
  constructor
  · -- Real part: (-1/2)^2 - (√3/2)^2 = 1/4 - 3/4 = -1/2
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im,
          Complex.neg_re, Complex.neg_im]
    nlinarith [hsq]
  · -- Imaginary part: 2*(-1/2)*(√3/2) = -√3/2
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im,
          Complex.neg_re, Complex.neg_im]
    ring

/-! ## Theorem 1: circulant3_spectrum_formula -/

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

/-! ## Theorem 2: circulant3_residue_real_iff_symmetric -/

/-- THEOREM 2: For real b, c, the residue eigenvalue is real iff b = c. -/
theorem circulant3_residue_real_iff_symmetric (b c : ℝ) :
    (b * omega3 + c * omega3^2).im = 0 ↔ b = c := by
  rw [circulant3_spectrum_formula]
  have h_sqrt_pos : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have h_sqrt_half_ne : Real.sqrt 3 / 2 ≠ 0 := by
    have : Real.sqrt 3 ≠ 0 := ne_of_gt h_sqrt_pos
    linarith
  -- Compute imaginary part: Im(↑a + ↑x * I) = x
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

/-! ## Theorem 3: circulant3_fixed_sum_residue_norm_minimized_at_symmetric -/

/-- THEOREM 3: The squared residue modulus is (b+c)²/4 + 3(b-c)²/4,
    which is ≥ (b+c)²/4, with equality iff b = c. -/
theorem circulant3_fixed_sum_residue_norm_minimized_at_symmetric (b c : ℝ) :
    (b + c)^2 / 4 + 3 * (b - c)^2 / 4 ≥ (b + c)^2 / 4 := by
  have h_nonneg : 0 ≤ 3 * (b - c)^2 / 4 := by
    have : 0 ≤ (b - c)^2 := sq_nonneg (b - c)
    linarith
  linarith

/-- COROLLARY: Equality holds iff b = c. -/
theorem circulant3_fixed_sum_residue_norm_minimized_iff_symmetric (b c : ℝ) :
    ((b + c)^2 / 4 + 3 * (b - c)^2 / 4 = (b + c)^2 / 4) ↔ b = c := by
  constructor
  · intro h
    have h1 : 3 * (b - c)^2 / 4 = 0 := by linarith
    have h2 : (b - c)^2 = 0 := by linarith
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp h2)
  · intro h
    simp [h]

/-! ## Theorem 4: normalized_circulant3_residue_norm_lt_one_iff -/

/-- THEOREM 4: On the normalized slice (p=b, q=1-b), the squared residue
    modulus is 3b² - 3b + 1, which is < 1 iff b is in the open interval (0,1). -/
theorem normalized_circulant3_residue_norm_lt_one_iff (b : ℝ) :
    (3 * b^2 - 3 * b + 1 < 1) ↔ (0 < b ∧ b < 1) := by
  constructor
  · intro h
    have h1 : 3 * b^2 - 3 * b < 0 := by linarith
    have h2 : 3 * b * (b - 1) < 0 := by linarith [show 3 * b * (b - 1) = 3 * b^2 - 3 * b from by ring]
    have h3pos : (3:ℝ) > 0 := by norm_num
    have h3 : b * (b - 1) < 0 := by
      have : b * (b - 1) = (3 * b * (b - 1)) / 3 := by field_simp
      rw [this]
      exact div_neg_of_neg_of_pos h2 h3pos
    -- From b * (b - 1) < 0, we get 0 < b and b < 1
    -- If b ≤ 0: b ≤ 0 and b-1 ≤ -1 < 0, so b*(b-1) ≥ 0, contradiction
    -- If b ≥ 1: b ≥ 1 and b-1 ≥ 0, so b*(b-1) ≥ 0, contradiction
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
    b = 0 ∨ b = 1 → 3 * b^2 - 3 * b + 1 = 1 := by
  rintro (rfl | rfl)
  · norm_num
  · norm_num

/-- COROLLARY: At b = 1/2 (H17, symmetry), |λ|² = 1/4 (minimum). -/
theorem normalized_circulant3_residue_norm_min_at_half :
    3 * ((1:ℝ)/2)^2 - 3 * ((1:ℝ)/2) + 1 = 1/4 := by
  norm_num

/-! ## Negative Controls (per Codex spec) -/

/-- NEGATIVE CONTROL 1: Symmetry (b = c) does NOT always give contraction.
    b = c = 2: |λ|² = 4 > 1. Symmetry alone is insufficient. -/
theorem symmetric_circulant3_not_always_contracting :
    (4 : ℝ)^2 / 4 + 3 * ((2:ℝ) - 2)^2 / 4 > 1 := by
  norm_num

/-- NEGATIVE CONTROL 2: Nonsymmetric can still contract on the normalized slice.
    b = 1/4, c = 3/4: |λ|² = 7/16 < 1. Symmetry is not necessary. -/
theorem nonsymmetric_normalized_circulant3_contracts :
    (3 * ((1:ℝ)/4)^2 - 3 * ((1:ℝ)/4) + 1) < 1 := by
  norm_num

/-- NEGATIVE CONTROL 3: Zero diagonal + equal row sums does NOT imply circulant.
    M = [[0, 1, 2], [3, 0, 0], [0, 3, 0]] has zero diag, row sums = 3,
    but is not circulant3 for any b, c (M(0,1)=1 ≠ M(1,2)=0, but circulant requires both = b). -/
theorem zero_diag_equal_rows_not_circulant :
    ∃ (M : Fin 3 → Fin 3 → ℝ),
      (∀ i, M i i = 0) ∧
      (∀ i, ∑ j, M i j = 3) ∧
      (∀ b c, ∃ i j, M i j ≠ PfLean.Z3FromBareMedium.circulant3 b c i j) := by
  -- M = [[0, 1, 2], [3, 0, 0], [0, 3, 0]]
  -- Row sums: 3, 3, 3. Zero diagonal.
  -- Not circulant: circulant3 b c has M(0,1) = b and M(1,2) = b.
  -- Here M(0,1) = 1 but M(1,2) = 0, so no single b works.
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
  · -- Zero diagonal
    intro i
    fin_cases i <;> simp [M]
  · -- Equal row sums = 3
    intro i
    fin_cases i <;> simp [M, Fin.sum_univ_three] <;> ring
  · -- Not circulant: for any b c, M(0,1) ≠ circulant3 b c 0 1 or M(1,2) ≠ circulant3 b c 1 2
    intro b c
    by_cases hb : b = 1
    · -- b = 1: use i=1, j=2. M(1,2) = 0, circulant3 1 c 1 2 = 1
      use 1, 2
      have h_M12 : M 1 2 = 0 := by simp [M]
      have h_circ : PfLean.Z3FromBareMedium.circulant3 b c 1 2 = b := by
        unfold PfLean.Z3FromBareMedium.circulant3
        rw [if_neg (by simp : ¬((2:Fin 3) = (1:Fin 3))),
            if_pos (by simp : (2:Fin 3) = (1:Fin 3) + 1)]
      rw [h_M12, h_circ, hb]
      norm_num
    · -- b ≠ 1: use i=0, j=1. M(0,1) = 1 ≠ b = circulant3
      use 0, 1
      have h_M01 : M 0 1 = 1 := by simp [M]
      have h_circ : PfLean.Z3FromBareMedium.circulant3 b c 0 1 = b := by
        unfold PfLean.Z3FromBareMedium.circulant3
        rw [if_neg (by simp : ¬((1:Fin 3) = (0:Fin 3))),
            if_pos (by simp : (1:Fin 3) = (0:Fin 3) + 1)]
      rw [h_M01, h_circ]
      exact ne_comm.mp hb

/-! ## Non-Theorem Section: Physical Observations (NOT claims)

The following are observations about what the algebra MEANS, not theorems.
They do not appear in CLAIMS.md and are not machine-verified.

OBSERVATION 1 (from Devin's grove reflection, 2026-08-13):
  The Wall v4: "Why stable structure?"
  - Re(λ) = -s/2 is forced by H7 (zero diagonal) + H18 (equal row sums) + real matrix
  - Im(λ) = 0 is NOT forced — it requires H17 (symmetry, b = c)
  - Real eigenvalue ↔ stable (in QFT language: real mass ↔ stable particle)
  - The axioms give the mass parameter for free; stability is the independent posit

OBSERVATION 2:
  The number -1/2 (in normalized form) appears in every circulant.
  Its meaning changes with |λ|:
    - |λ| = 1: rotation component (cos(2π/3))
    - |λ| < 1: decay rate (paired with oscillation)
    - |λ| = 1/2 (H17): pure eigenvalue (no imaginary partner)

  Same signal, different media, different meanings.
  This connects to MEDIUM_TRANSFER_LAYER but is NOT a formal transfer contract.

OBSERVATION 3:
  The damped oscillator regime (0 < b < 1, b ≠ 1/2) corresponds to
  complex eigenvalues — analogous to unstable particles in QFT (complex mass).
  The God Equation (H17, b = 1/2) sits at the unique point of stability.
  This is an analogy, not a derivation. A transfer contract would be needed
  to promote it to a claim.

These observations are kept as thoughts, not claims. They guide where to look
next, not what to assert.
-/

end PfLean.Circulant3Spectrum
