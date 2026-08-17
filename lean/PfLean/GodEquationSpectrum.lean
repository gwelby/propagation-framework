import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic
import PfLean.GodEquationSelection

/-!
# GodEquationSpectrum — N=3 selection at the level of the FULL residue spectrum

Companion to `GodEquationSelection.lean`, written to repair a scoping gap
found in cross-audit (Claude, 2026-08-12; formalized 2026-08-14).

## The gap

Every theorem in `GodEquationSelection` evaluates `cos³(2πk/N)` at the
**fundamental mode k = 1** only. But the cycle graph `C_N` has `N−1`
residue modes, `k = 1 … N−1`, with residues `cos(2πk/N)`. The theorems
there are all TRUE; the *narrative* around them ("−1/8 CARRIES the
generation count: it is N=3-specific") is not, read at spectrum level:

    every N divisible by 3 has a mode with residue exactly −1/8,
    namely k = N/3, since cos(2π·(N/3)/N) = cos(2π/3) = −1/2.

Numerically: N=6 (k=2), N=9 (k=3), N=12 (k=4), N=15 (k=5) all contain a
−1/8 residue. So "N=6 flips the sign" is true of the *fundamental* mode
and false of the 6-cycle's spectrum, which contains +1/8, −1/8 and −1.
A discriminator that depends on which mode you look at is fragile.

## The repair (strictly stronger, and mode-choice-independent)

    N = 3 is the unique N ≥ 2 whose ENTIRE residue spectrum is −1/8.

That is exactly the God Equation spectrum {1, −1/8, −1/8}: uniform mode 1,
and *all* residue modes at −1/8. The degeneracy — both residues coinciding
— is itself the Z₃ signature, and it is what no other cycle has.

The proof is short: for N ≥ 4 the fundamental mode already fails, because
0 < 2π/N ≤ π/2 forces cos(2π/N) ≥ 0, so its cube cannot be negative;
and N = 2 gives −1. No case analysis beyond that is needed.

**Honest boundary (inherited, unchanged):** this sharpens the structural
statement. It does NOT derive N=3 from Axioms 1-3. The generation-count
derivation remains the conditional T3 theorem.

Author: Claude — 2026-08-14. Cross-audit dispatch:
`/mnt/d/Claude/outbox/2026-08-12-claude-n3-selection-cross-audit.md`.
Original module and the k=1 results: DeepSeek ∇²⬡ (2026-08-09), Devin (2026-08-10).
-/

namespace PfLean

open Real

/-- The Euler-discretized T³ residue of mode `k` of the N-cycle:
    `cos³(2πk/N)`. Mode `k = 0` is the uniform sector (eigenvalue 1) and is
    excluded from the residue spectrum; the residue modes are `1 ≤ k < N`. -/
noncomputable def residueCubed (n k : ℕ) : ℝ := (cos (2 * Real.pi * k / n)) ^ 3

/-- Mode 1 of the N-cycle is the fundamental mode `GodEquationSelection`
    studies: `residueCubed n 1 = cos³(2π/n)`. -/
theorem residueCubed_one (n : ℕ) :
    residueCubed n 1 = (cos (2 * Real.pi / n)) ^ 3 := by
  unfold residueCubed
  norm_num

/-- **For N ≥ 4: `cos(2π/N) ≥ 0`.** The angle `2π/N` lies in `(0, π/2]`,
    where cosine is non-negative. This is the `N ≥ 4` companion to
    `cos_pos_for_n_ge_5` (which is strict, but excludes N = 4 where the
    cosine is exactly 0). -/
theorem cos_nonneg_for_n_ge_4 (n : ℕ) (hn : 4 ≤ n) :
    0 ≤ cos (2 * Real.pi / n) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hn4 : (4 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hn_pos : (0 : ℝ) < (n : ℝ) := by linarith
  have h_upper : 2 * Real.pi / n ≤ Real.pi / 2 := by
    rw [div_le_iff₀ hn_pos]
    nlinarith [hpi, hn4]
  have h_lower : 0 < 2 * Real.pi / n := div_pos (by linarith) hn_pos
  exact Real.cos_nonneg_of_mem_Icc ⟨by linarith, h_upper⟩

/-- **For N ≥ 4 the fundamental residue is not −1/8.** Its cube is
    non-negative, and −1/8 is negative. -/
theorem residueCubed_one_ne_of_n_ge_4 (n : ℕ) (hn : 4 ≤ n) :
    residueCubed n 1 ≠ (-1 : ℝ) / 8 := by
  rw [residueCubed_one]
  have h : 0 ≤ (cos (2 * Real.pi / n)) ^ 3 :=
    pow_nonneg (cos_nonneg_for_n_ge_4 n hn) 3
  intro hcontra
  rw [hcontra] at h
  norm_num at h

/-- **N = 2: the single residue mode is −1, not −1/8.** -/
theorem residueCubed_two_one : residueCubed 2 1 = (-1 : ℝ) := by
  unfold residueCubed
  push_cast
  have h : (2 * Real.pi * 1 / 2 : ℝ) = Real.pi := by ring
  rw [h, Real.cos_pi]
  norm_num

/-- **N = 3: both residue modes equal −1/8.**

    `k = 1` gives `cos(2π/3) = −1/2`; `k = 2` gives `cos(4π/3) = −1/2` as
    well. The 3-cycle's residue spectrum is `{−1/8, −1/8}` — degenerate,
    which is precisely the Z₃ signature. -/
theorem n3_all_residues_minus_eighth :
    ∀ k : ℕ, 1 ≤ k → k < 3 → residueCubed 3 k = (-1 : ℝ) / 8 := by
  intro k hk1 hk3
  interval_cases k
  · -- k = 1 : cos(2π/3)
    rw [residueCubed_one]
    exact n3_gives_minus_eighth
  · -- k = 2 : cos(4π/3) = cos(2π − 2π/3) = cos(2π/3)
    unfold residueCubed
    push_cast
    have h : (2 * Real.pi * 2 / 3 : ℝ) = 2 * Real.pi - 2 * Real.pi / 3 := by ring
    rw [h, Real.cos_sub, Real.cos_two_pi, Real.sin_two_pi]
    simp only [one_mul, zero_mul, add_zero]
    exact n3_gives_minus_eighth

/-- **MAIN — N = 3 is the unique cycle whose entire residue spectrum is −1/8.**

    For `n ≥ 2`:  (every residue mode of the n-cycle equals −1/8) ↔ n = 3.

    This is the mode-choice-independent form of the N=3 selection. Unlike the
    k = 1 statements in `GodEquationSelection`, it cannot be weakened by
    pointing at a different mode: N = 6, 9, 12, … each *contain* a −1/8
    residue (see `residueCubed_minus_eighth_at_multiples_of_three`), but only
    N = 3 has nothing else. -/
theorem n3_unique_full_residue_spectrum (n : ℕ) (hn : 2 ≤ n) :
    (∀ k : ℕ, 1 ≤ k → k < n → residueCubed n k = (-1 : ℝ) / 8) ↔ n = 3 := by
  constructor
  · intro hall
    by_contra hne
    -- n ≥ 2 and n ≠ 3, so n = 2 or n ≥ 4; both fail at the fundamental mode.
    rcases lt_or_ge n 4 with hlt | hge
    · -- n = 2 or n = 3; n ≠ 3 leaves n = 2
      interval_cases n
      · have := hall 1 (le_refl 1) (by norm_num)
        rw [residueCubed_two_one] at this
        norm_num at this
      · exact hne rfl
    · exact residueCubed_one_ne_of_n_ge_4 n hge
        (hall 1 (le_refl 1) (by omega))
  · rintro rfl
    exact n3_all_residues_minus_eighth

/-- **Why the k = 1 framing was fragile: every multiple of 3 contains −1/8.**

    For `m ≥ 1`, the `(3m)`-cycle has mode `k = m` with residue exactly
    −1/8, because `2π·m/(3m) = 2π/3`. So `N = 6, 9, 12, …` all carry a
    God-Equation-valued residue mode; what distinguishes N = 3 is that it
    carries *nothing else*. -/
theorem residueCubed_minus_eighth_at_multiples_of_three (m : ℕ) (hm : 1 ≤ m) :
    residueCubed (3 * m) m = (-1 : ℝ) / 8 := by
  unfold residueCubed
  push_cast
  have hm0 : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
  have h : (2 * Real.pi * (m : ℝ) / (3 * (m : ℝ))) = 2 * Real.pi / 3 := by
    field_simp
  rw [h]
  exact n3_gives_minus_eighth

/-- **The corrected reading of `n6_sign_flip`.**

    `n6_sign_flip` proves cos³(π/3) = +1/8 — true, and it is the 6-cycle's
    *fundamental* mode. But the 6-cycle's mode k = 2 is −1/8 (this theorem,
    at m = 2). Both are facts about C₆; the sign flip is therefore a
    property of a chosen mode, not of the 6-cycle. Recorded so the
    discriminator is never cited mode-blind. -/
theorem n6_contains_minus_eighth : residueCubed 6 2 = (-1 : ℝ) / 8 := by
  have h := residueCubed_minus_eighth_at_multiples_of_three 2 (by norm_num)
  norm_num at h
  linarith [h]

end PfLean
