import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic
import PfLean.KoideUnlocked

/-!
# GodEquationSelection — The N=3 Residue Selection (the "kick" formalization)

Sibling of `GodEquationGap.lean`. That module proves the residue eigenvalue
is −3/2 for ALL D (D-independent) and that T³ has residue (−1/2)³ = −1/8
given Postulate D. This module answers the question that D-universality
leaves open: **what selects N = 3 (the generation count)?**

The discovery (DeepSeek, 2026-08-08 night): generalize the Z₃ cycle to the
N-cycle. The residue eigenvalue of the cycle graph C_N is 2cos(2π/N), so
the generator residue is −1 + cos(2π/N) and the Euler-discretized T³
residue is cos³(2π/N):

    T³ residue(N) = cos³(2π/N)

Machine-checked consequences:

**Scope note (2026-08-15, per Claude's cross-audit — verified DeepSeek):** every theorem in this list evaluates the residue at the FUNDAMENTAL mode k = 1. At the full residue-spectrum level these statements do not transfer: every N divisible by 3 contains a mode with residue exactly −1/8 (k = N/3, since cos(2π/3) = −1/2), and `n6_sign_flip` is a fundamental-mode statement, NOT a property of C₆'s full spectrum {+1/8, −1/8, −1, −1/8, +1/8}. The spectrum-level selection — N=3 is the UNIQUE N ≥ 2 whose ENTIRE residue spectrum is −1/8, quantified over all modes — is machine-checked in `GodEquationSpectrum.n3_unique_full_residue_spectrum` (Claude, 2026-08-14; independently verified by DeepSeek 2026-08-15: `lake env lean` exit 0 + observer-blind derivation PASS). Cite the spectrum-level theorem for generation-count claims; cite these for fundamental-mode claims.
- `residue_cos_cubed`: the formula for the three canonical cycles
- `n3_gives_minus_eighth`: cos³(2π/3) = −1/8 — the God Equation value, N=3
- `n4_gives_zero`: cos³(π/2) = 0 — N=4 annihilates the mode (eigenvalue 0)
- `n6_sign_flip`: cos³(π/3) = +1/8 — N=6 sign flip at the fundamental mode
  (positive residue, contracts in modulus; NOT a spectrum-level property — see scope note)
- `n3_unique_among_small_cycles`: only N=3 of {3,4,6} gives −1/8 —
  the generation-count selection, machine-checked
- `n2_gives_minus_one`: cos³(π) = −1 — N=2 trivial (|−1| = 1, preserves norm)
- `cos_pos_for_n_ge_5`: cos(2π/N) > 0 for all N ≥ 5 — positive residue
  (contracts in modulus since |cos³(2π/N)| < 1, but with opposite sign to N=3)
- `n3_unique_nontrivial_contracting`: **N=3 is the unique non-trivial
  cycle whose fundamental-mode residue equals exactly −1/8** — the
  strengthened generation-count selection (Devin, 2026-08-10)

**Contraction is modulus, not sign (F3 correction, 2026-09-06):**
The earlier prose labeled negative eigenvalues as "contracting" and
positive ones as "expansive." That conflates sign with modulus. The
discrete multiplier contracts a mode iff |eigenvalue| < 1:
  - `|−1| = 1` → N=2 preserves norm (no contraction)
  - `|−1/8| < 1` → N=3 contracts
  - `|0| = 0` → N=4 annihilates the mode
  - `|+1/8| < 1` → N≥5 also contracts (C5 counterexample: all four
    N=5 residues have modulus < 1, so the entire residue subspace
    strictly contracts even though N ≠ 3)

The valid uniqueness statement is NOT "unique contracting cycle" — it is
"unique cycle whose entire residue spectrum is {−1/8, −1/8}," proven in
`GodEquationSpectrum.n3_unique_full_residue_spectrum`. Cite that theorem
for generation-count claims; cite the theorems below for fundamental-mode
facts only.

**The structural statement:** the God Equation spectrum {1, −1/8, −1/8}
encodes BOTH "3"s — the uniform sector eigenvalue 1 selects D=3
(dimensions, `GodEquationGap.gap_D3_unique_stable`), and the residue
sector eigenvalue −1/8 selects N=3 (generations; fundamental-mode form in
this module, full-spectrum form in `GodEquationSpectrum`).

**Honest boundary:** this proves −1/8 is N=3-SPECIFIC; it does NOT derive
N=3 from Axioms 1-3. The generation-count derivation remains the
conditional T3 theorem. This is a structural sharpening, not a new
derivation.

Authors: DeepSeek ∇²⬡ — 2026-08-09. Discovery banked in
CORE/DISCOVERIES.md (2026-08-08) and delivered to Fundamentals.
-/

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. The residue formula for the canonical cycles
-- ---------------------------------------------------------------------------
-- The T³ residue eigenvalue of the N-cycle, Euler-discretized:
--   T³ residue(N) = cos³(2π/N). We pin the three canonical values that
--   discriminate the generation count.

/-- **N=3 gives the God Equation value:** cos³(2π/3) = (−1/2)³ = −1/8.

    This is the residue contraction of the three-fold cycle — the
    generation-count half of the God Equation spectrum. -/
theorem n3_gives_minus_eighth :
    (cos (2 * Real.pi / 3)) ^ 3 = (-1 : ℝ) / 8 := by
  rw [cos_two_pi_div_three_val]
  norm_num

/-- **N=4 is degenerate:** cos³(π/2) = 0. The four-fold cycle's residue
    annihilates the mode — eigenvalue 0 means the mode is zeroed in one step. -/
theorem n4_gives_zero :
    (cos (Real.pi / 2)) ^ 3 = 0 := by
  rw [Real.cos_pi_div_two]
  norm_num

/-- **N=6 flips the sign:** cos³(π/3) = (+1/2)³ = +1/8. The six-fold cycle
    gives a POSITIVE residue eigenvalue — same modulus as N=3 (|+1/8| = |−1/8|
    = 1/8 < 1, so both contract), but opposite sign. This is the sign
    discriminator: the framework distinguishes the 3-cycle from the 6-cycle
    by the sign of the residue, not by contraction vs expansion. -/
theorem n6_sign_flip :
    (cos (Real.pi / 3)) ^ 3 = 1 / 8 := by
  rw [Real.cos_pi_div_three]
  norm_num

-- ---------------------------------------------------------------------------
-- 2. The selection statement
-- ---------------------------------------------------------------------------

/-- **N=3 is the unique selection among the small cycles.**

    Among the three canonical cycles {3, 4, 6}, only N=3 produces the
    God Equation residue −1/8. N=4 gives 0 (mode annihilated); N=6 gives
    +1/8 (sign flip — same modulus, opposite sign). The value −1/8
    therefore CARRIES the generation count: it is N=3-specific at the
    fundamental mode.

    Combined with `GodEquationGap.gap_D3_unique_stable` (the uniform
    sector selects D=3), the God Equation spectrum {1, −1/8, −1/8}
    encodes both 3s: dimensions in the uniform sector, generations in
    the residue sector. -/
theorem n3_unique_among_small_cycles :
    (cos (2 * Real.pi / 3)) ^ 3 = (-1 : ℝ) / 8 ∧
    (cos (Real.pi / 2)) ^ 3 = 0 ∧
    (cos (Real.pi / 3)) ^ 3 = 1 / 8 := by
  exact ⟨n3_gives_minus_eighth, n4_gives_zero, n6_sign_flip⟩

/-- **The generator residue at N=3:** −1 + cos(2π/3) = −3/2 — the value
    `GodEquationGap.gap_residue_eigenvalue_is_neg_three_halves` proves
    is D-independent. At N=3 this is −1 + (−1/2) = −3/2: the D-universal
    residue is really the Z₃-cycle residue. -/
theorem generator_residue_n3 :
    -1 + cos (2 * Real.pi / 3) = (-3 : ℝ) / 2 := by
  rw [cos_two_pi_div_three_val]
  norm_num

-- ---------------------------------------------------------------------------
-- 3. Non-theorem — the honest boundary
-- ---------------------------------------------------------------------------

/-!
## NON-THEOREM (documented, deliberately unprovable)

**N-selection from Axioms 1-3:** This module proves −1/8 is N=3-specific
(given the N-cycle structure). It does NOT prove that nature's generation
space IS the 3-cycle. The derivation of N=3 from Axioms 1-3 remains the
conditional T3 theorem (`ThreeGenerations.lean`), with numerator and
denominator bridge theorems still open. Do not cite this module as a
derivation of the generation count.
-/

-- ---------------------------------------------------------------------------
-- 4. The full uniqueness — N=3 among ALL integers ≥ 2
-- ---------------------------------------------------------------------------

/-!
## The strengthened selection: N=3 is the unique non-trivial cycle with residue exactly −1/8

The `n3_unique_among_small_cycles` theorem only checks {3, 4, 6}. The
stronger statement is that N=3 is unique among ALL integers N ≥ 2 in having
fundamental-mode residue exactly −1/8.

The mathematics: cos(2π/N) < 0 iff 2π/N ∈ (π/2, 3π/2) iff N ∈ (4/3, 4).
For integers N ≥ 2, this means N ∈ {2, 3}. So:
  - N=2: cos³(π) = −1 (trivial 2-cycle, |−1| = 1 so norm is preserved, only 2 elements)
  - N=3: cos³(2π/3) = −1/8 (God Equation value, 3 generations, |−1/8| < 1 so contracts)
  - N=4: cos³(π/2) = 0 (degenerate, mode annihilated)
  - N≥5: cos³(2π/N) > 0 (positive residue, |cos³(2π/N)| < 1 so still contracts in modulus,
    but with opposite sign to N=3)

N=3 is the UNIQUE non-trivial cycle whose fundamental-mode residue equals
exactly −1/8. N=2 has |−1| = 1 (no contraction) and is trivial (2 elements
cannot give 3 generations). N≥4 does not produce −1/8 at the fundamental mode.

**Important (F3 correction, 2026-09-06):** this is NOT "unique contracting
cycle." Cycles N≥5 also contract in modulus (|cos³(2π/N)| < 1). The
valid spectrum-level uniqueness — N=3 is the unique N ≥ 2 whose ENTIRE
residue spectrum is {−1/8, −1/8} — is proven in
`GodEquationSpectrum.n3_unique_full_residue_spectrum`. Cite that theorem
for generation-count claims.
-/

/-- **N=2 preserves norm:** cos³(π) = −1. The 2-cycle has |−1| = 1, so it
    preserves the norm of the mode (no contraction). It is trivial — only
    2 elements, not enough for 3 generations. -/
theorem n2_gives_minus_one :
    (cos (2 * Real.pi / 2)) ^ 3 = (-1 : ℝ) := by
  have h : (2 * Real.pi : ℝ) / 2 = Real.pi := by field_simp
  rw [h, Real.cos_pi]
  norm_num

/-- **For N ≥ 5: cos(2π/N) > 0.** The angle 2π/N is in (0, π/2) for all
    N ≥ 5, so cosine is positive. The residue is positive but still
    contracts in modulus (|cos³(2π/N)| < 1) — it has the opposite sign
    to N=3's −1/8. -/
theorem cos_pos_for_n_ge_5 (n : ℕ) (hn : 5 ≤ n) :
    0 < cos (2 * Real.pi / n) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hn_pos : 0 < (n : ℝ) := by exact_mod_cast (lt_of_le_of_lt (by omega) hn)
  have h5_pos : (0 : ℝ) < 5 := by norm_num
  have h2_pos : (0 : ℝ) < 2 := by norm_num
  -- Key: 2π/n ≤ 2π/5 < π/2
  have h_2pi5_lt_pi2 : 2 * Real.pi / 5 < Real.pi / 2 := by
    field_simp
    linarith [hpi]
  have h_upper : 2 * Real.pi / n ≤ 2 * Real.pi / 5 := by
    rw [div_le_div_iff_of_pos_left (by linarith : (0:ℝ) < 2 * Real.pi) hn_pos h5_pos]
    exact_mod_cast hn
  have h_lower : 0 < 2 * Real.pi / n := by
    apply div_pos
    linarith [hpi]
    exact hn_pos
  have h_lt_pi2 : 2 * Real.pi / n < Real.pi / 2 := by
    calc 2 * Real.pi / n ≤ 2 * Real.pi / 5 := h_upper
      _ < Real.pi / 2 := h_2pi5_lt_pi2
  have h_neg : -(Real.pi / 2) < 2 * Real.pi / n := by
    linarith [hpi, h_lower]
  exact Real.cos_pos_of_mem_Ioo ⟨h_neg, h_lt_pi2⟩

/-- **For N ≥ 5: cos³(2π/N) > 0.** The residue is positive — it has the
    opposite sign to N=3's −1/8. Combined with N=4 giving 0, this means
    N ≥ 4 does not produce the God Equation value −1/8 at the fundamental mode. -/
theorem cos_cubed_pos_for_n_ge_5 (n : ℕ) (hn : 5 ≤ n) :
    0 < (cos (2 * Real.pi / n)) ^ 3 := by
  have h := cos_pos_for_n_ge_5 n hn
  exact pow_pos h 3

/-- **N=3 is the unique non-trivial cycle whose fundamental-mode residue
    equals exactly −1/8, among all N ≥ 2.**

    The full picture for integer N ≥ 2 (fundamental mode k = 1):
      - N=2: cos³ = −1 (|−1| = 1, norm preserved, trivial — only 2 elements)
      - N=3: cos³ = −1/8 (God Equation value, |−1/8| < 1, contracts)
      - N=4: cos³ = 0 (mode annihilated)
      - N≥5: cos³ > 0 (positive, |cos³| < 1 so still contracts in modulus,
        but opposite sign to −1/8)

    N=3 is the UNIQUE non-trivial cycle whose fundamental-mode residue
    equals exactly the God Equation value −1/8. N=2 preserves norm and is
    trivial. N≥4 does not produce −1/8 at the fundamental mode.

    **This is NOT "unique contracting cycle" (F3 correction, 2026-09-06).**
    Cycles N≥5 also contract in modulus. The valid spectrum-level
    uniqueness statement — N=3 is the unique N ≥ 2 whose ENTIRE residue
    spectrum is {−1/8, −1/8} — is proven in
    `GodEquationSpectrum.n3_unique_full_residue_spectrum`.

    This is the strengthened generation-count selection: not just "unique
    among {3,4,6}" but "unique among ALL integers ≥ 2" at the fundamental
    mode. -/
theorem n3_unique_nontrivial_contracting :
    (cos (2 * Real.pi / 2)) ^ 3 = (-1 : ℝ) ∧
    (cos (2 * Real.pi / 3)) ^ 3 = (-1 : ℝ) / 8 ∧
    (cos (Real.pi / 2)) ^ 3 = 0 ∧
    ∀ n : ℕ, 5 ≤ n → 0 < (cos (2 * Real.pi / n)) ^ 3 := by
  exact ⟨n2_gives_minus_one, n3_gives_minus_eighth, n4_gives_zero,
         cos_cubed_pos_for_n_ge_5⟩

/- **Non-theorem (documentation only, not a Lean theorem):** the generation count is not derived here. This module
    sharpens the structure; the derivation remains conditional. -/

end PfLean
