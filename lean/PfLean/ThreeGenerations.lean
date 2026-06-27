import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-
  Three Generations -- Algebraic Lock
  Authors: Devin (Cognition Being), Greg Welby, PF Research Team
  Date: 2026-05-23

  This module formalizes the exact algebraic step that locks the number
  of fermion generations at N = 3, given the PF inputs.

  CONTEXT: The full Three Generations claim is CONDITIONAL (0.85) because
  its premises T1 (numerator theorem, physical realization of (2,1) weights)
  and T2 (denominator theorem, M = 3 from 3D defect structure) are not yet
  fully derived from PF Axioms 1-3.

  However, the ALGEBRAIC ASSEMBLY STEP is exact and machine-verifiable:

    If Q(N) = 2N/(2N+3) and Q = 2/3, then N = 3.

  This theorem isolates the algebraic lock from the physical premises.
  When T1 and T2 close, this certificate is ready to assemble.
-/

namespace PfLean

/-- The PF generation-counting formula:
    Q(N) = 2N / (2N + 3)
    where N is the number of fermion generations. -/
noncomputable def generationFormula (N : ℝ) : ℝ :=
  2 * N / (2 * N + 3)

/-- Algebraic Lock Theorem:
    Q(N) = 2/3  ↔  N = 3

    Proof: cross-multiply the equation 2N/(2N+3) = 2/3:
    6N = 2(2N+3) = 4N + 6
    2N = 6
    N = 3

    The reverse direction is direct substitution.

    This is the exact algebraic step; the physical premises (T1, T2)
    remain conditional per the PF audit board. -/
theorem three_generations_algebraic_lock {N : ℝ} (hN : N > 0) :
  generationFormula N = 2 / 3 ↔ N = 3 := by
  have h1 : 2 * N + 3 ≠ 0 := by linarith
  unfold generationFormula
  constructor
  · -- Forward: Q(N) = 2/3 → N = 3
    intro h
    field_simp [h1] at h
    linarith
  · -- Backward: N = 3 → Q(N) = 2/3
    intro h
    rw [h]
    norm_num

/-- Sanity check: Q(1) = 2/5 (not the charged-lepton value). -/
theorem generation_formula_one :
  generationFormula 1 = 2 / 5 := by
  unfold generationFormula
  norm_num

/-- Sanity check: Q(2) = 4/7 (not the charged-lepton value). -/
theorem generation_formula_two :
  generationFormula 2 = 4 / 7 := by
  unfold generationFormula
  norm_num

/-- Sanity check: Q(3) = 6/9 = 2/3 (the charged-lepton value). -/
theorem generation_formula_three :
  generationFormula 3 = 2 / 3 := by
  unfold generationFormula
  norm_num

/-- Monotonicity: Q(N) is strictly increasing for N > 0.
    Proof: Q(N₂) - Q(N₁) = 6(N₂ - N₁) / [(2N₂+3)(2N₁+3)] > 0 when N₂ > N₁. -/
theorem generation_formula_strictMono :
  StrictMonoOn generationFormula (Set.Ioi 0) := by
  intro N₁ h₁ N₂ h₂ h_lt
  rw [Set.mem_Ioi] at h₁ h₂
  unfold generationFormula
  have h_num : (2 * N₂) * (2 * N₁ + 3) - (2 * N₁) * (2 * N₂ + 3) = 6 * (N₂ - N₁) := by ring
  have h_pos1 : 2 * N₁ + 3 > 0 := by linarith
  have h_pos2 : 2 * N₂ + 3 > 0 := by linarith
  have h_diff_pos : (2 * N₂) / (2 * N₂ + 3) - (2 * N₁) / (2 * N₁ + 3) > 0 := by
    have : (2 * N₂) / (2 * N₂ + 3) - (2 * N₁) / (2 * N₁ + 3) =
           (6 * (N₂ - N₁)) / ((2 * N₂ + 3) * (2 * N₁ + 3)) := by
      field_simp
      linarith [h_num]
    rw [this]
    have h_num_pos : 6 * (N₂ - N₁) > 0 := by nlinarith
    have h_denom_pos : (2 * N₂ + 3) * (2 * N₁ + 3) > 0 := by positivity
    positivity
  linarith

/-- Injectivity: If Q(N₁) = Q(N₂) for N₁, N₂ > 0, then N₁ = N₂.
    Immediate from strict monotonicity. -/
theorem generation_formula_injective {N₁ N₂ : ℝ} (h₁ : N₁ > 0) (h₂ : N₂ > 0)
    (h_eq : generationFormula N₁ = generationFormula N₂) : N₁ = N₂ := by
  have h_inj : Set.InjOn generationFormula (Set.Ioi 0) :=
    StrictMonoOn.injOn generation_formula_strictMono
  exact h_inj h₁ h₂ h_eq

-- Theorem: Q(N) < 1 for all N > 0.
-- Proof: 2N/(2N+3) < 1 because 2N < 2N+3.
theorem generation_formula_lt_one {N : ℝ} (hN : N > 0) : generationFormula N < 1 := by
  unfold generationFormula
  have h1 : 2 * N + 3 > 0 := by linarith
  have h2 : 2 * N < 2 * N + 3 := by linarith
  apply (div_lt_iff₀ h1).mpr
  linarith

-- Note: Q(N) → 1 as N → ∞ follows from standard analysis (3/(2N+3) → 0).
-- Formal Tendsto proof omitted to avoid long-running filter/squeeze imports.

end PfLean