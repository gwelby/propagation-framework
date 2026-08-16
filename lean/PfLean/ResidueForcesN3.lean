/-
ResidueForcesN3.lean — DeepSeek sandbox proposal, 2026-08-12.

The forcing direction: the God Equation residue value −1/8 pins the cycle
length.  Given the N-cycle structure and the Euler discretization
(T = I + L, L = −I + ½M, T³ residue = cos³(2π/N)), the exact value
cos³(2π/N) = −1/8 forces N = 3.

This COMPLETES the selection statement of GodEquationSelection.lean:
  - there:  N=3 gives −1/8, and N≠3 is never contracting (uniqueness of the
            contracting cycle)
  - here:   IF the residue equals −1/8 THEN N = 3 (the value forces the cycle)

The honest boundary is unchanged: the residue value itself stays conditional
on the T3/Euler discretization (documented non-theorem in
GodEquationSelection.lean).  What is new is the bi-implication:
    residue = −1/8  ⟺  N = 3.
-/
import PfLean.GodEquationSelection

open Real
open PfLean

namespace ResidueForcesN3

/-- The God Equation residue −1/8 forces the 3-cycle.

    Case split on N: N=2 gives −1 (contradiction), N=3 gives the value,
    N=4 gives 0 (contradiction), N≥5 gives a positive residue (contradiction). -/
theorem residue_minus_eighth_forces_n3 (n : ℕ) (hn : 2 ≤ n) :
    (cos (2 * Real.pi / n)) ^ 3 = (-1 : ℝ) / 8 → n = 3 := by
  intro h
  by_cases hn2 : n = 2
  · subst n
    change (cos (2 * Real.pi / (2 : ℝ))) ^ 3 = (-1 : ℝ) / 8 at h
    rw [n2_gives_minus_one] at h
    norm_num at h
  by_cases hn3 : n = 3
  · exact hn3
  by_cases hn4 : n = 4
  · subst n
    have h4val : (cos (2 * Real.pi / (4 : ℝ))) ^ 3 = 0 := by
      rw [show (2 * Real.pi : ℝ) / (4 : ℝ) = Real.pi / (2 : ℝ) by
        field_simp
        norm_num]
      rw [Real.cos_pi_div_two]
      norm_num
    change (cos (2 * Real.pi / (4 : ℝ))) ^ 3 = (-1 : ℝ) / 8 at h
    rw [h4val] at h
    norm_num at h
  · have hn5 : 5 ≤ n := by omega
    have hpos : 0 < (cos (2 * Real.pi / n)) ^ 3 :=
      cos_cubed_pos_for_n_ge_5 n hn5
    have hneg : (cos (2 * Real.pi / n)) ^ 3 < 0 := by
      rw [h]
      norm_num
    linarith

/-- The bi-implication: residue = −1/8  ⟺  N = 3. -/
theorem minus_eighth_residue_iff_n3 (n : ℕ) (hn : 2 ≤ n) :
    (cos (2 * Real.pi / n)) ^ 3 = (-1 : ℝ) / 8 ↔ n = 3 := by
  constructor
  · exact residue_minus_eighth_forces_n3 n hn
  · intro hn3
    subst n
    exact n3_gives_minus_eighth

end ResidueForcesN3
