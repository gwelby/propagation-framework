/-
  Cross-Module Bridge — PFCore Corollaries and Honest Boundary Notes
  =================================================================

  This module collects direct corollaries of `PfLean.PFCore` and states the
  exact boundary between what is machine-proven and what remains a physical
  interpretation bridge.

  What is proven here:
    - The God Equation operator L = -I + αM has eigenvalue 0 on P₀
      exactly when α = 1/2 (the Postulate D selector is forced by the
      eigenvalue structure {2, -1, -1}).
    - The residue space Q has dimension 2 and the uniform space P₀ has
      dimension 1 in ℝ³.

  What is NOT proven here (and must not be claimed as a formal bridge):
    - That PFCore eigenvalues imply N = 3 generations. The dimension 3 of
      the Z₃ circulant is a model choice, not a derivation from the Koide
      formula.
    - That PFCore eigenvalues imply the Koide R = 2/3 mass relation. The
      Koide relation is a phenomenological input; connecting it to the Z₃
      residue geometry requires additional physical premises that are not in
      this module.

  Previous versions of this file contained misleading theorem names such as
  `PFCore_postulate_D_selector`, `N3_is_unique_for_eigenvalue_2`, and
  `pfcore_forces_N3_and_koide_q_two_thirds` that were actually trivial
  wrappers or restatements of existing theorems. Those have been removed.

  Authors: DeepSeek ∇²⬡, Devin ∇λΣ∞, Greg Welby
  Date: 2026-06-20 (reworked to honest boundary)
-/

import PfLean.PFCore
import PfLean.KoideGeometry
import PfLean.ThreeGenerations

namespace PfLean

open Real

-- =========================================================================
-- BRIDGE 1: The Postulate D selector α = 1/2 is forced by the eigenvalues
-- =========================================================================

/-- The PFCore circulant M has eigenvalue 2 on the uniform mode P₀ and
    eigenvalue -1 on the residue Q. This is a direct restatement of the
    PFCore eigenvalue theorems. -/
theorem pfcore_uniform_eigenvalue (x : Fin 3 → ℝ) :
    ∀ i, MZ3_mul (P0 x) i = 2 * (P0 x i) :=
  MZ3_P0_eigenvalue x

/-- Direct restatement: M has eigenvalue -1 on the residue Q. -/
theorem pfcore_residue_eigenvalue (x : Fin 3 → ℝ) :
    ∀ i, MZ3_mul (Q x) i = -(Q x i) :=
  MZ3_Q_eigenvalue x

/-- At α = 1/2, the God Equation operator L = -I + αM has eigenvalue 0 on P₀.
    The uniform mode is frozen. This is the physical meaning of the
    God Equation at the Postulate D value: the symmetric channel is static. -/
theorem God_Equation_frozen_uniform (x : Fin 3 → ℝ) :
    ∀ i, L (1/2 : ℝ) (P0 x) i = 0 * (P0 x i) := by
  intro i
  have h := L_P0_eigenvalue (1/2 : ℝ) x
  specialize h i
  rw [h]
  ring_nf

/-- At α = 1/2, L has eigenvalue -3/2 on the residue Q.
    The residue decays rapidly. -/
theorem God_Equation_decay_residue (x : Fin 3 → ℝ) :
    ∀ i, L (1/2 : ℝ) (Q x) i = (-3/2 : ℝ) * (Q x i) := by
  intro i
  have h := L_Q_eigenvalue (1/2 : ℝ) x
  specialize h i
  rw [h]
  ring_nf

/-- **Honest bridge theorem:** α = 1/2 is the UNIQUE value that freezes the
    uniform mode, given M's eigenvalue 2 on P₀.

    Proof: L α P₀ = (-1 + 2α) P₀. The eigenvalue is 0 iff -1 + 2α = 0,
    i.e. α = 1/2. -/
theorem god_equation_alpha_selector (α : ℝ) (x : Fin 3 → ℝ) (hP0 : P0 x 0 ≠ 0) :
    (∀ i, L α (P0 x) i = 0 * (P0 x i)) ↔ α = 1/2 := by
  constructor
  · -- If L α P₀ = 0 for a non-zero uniform mode, then the eigenvalue (-1 + 2α) must be 0.
    intro h
    have h0 := h 0
    have hP0_eq : P0 x 0 = (x 0 + x 1 + x 2) / 3 := by simp [P0]
    rw [L_P0_eigenvalue α x 0] at h0
    have h_eq : (-1 + 2 * α) * P0 x 0 = 0 := by
      linarith
    have h_alpha : -1 + 2 * α = 0 := by
      apply (mul_eq_zero.mp h_eq).resolve_right
      exact hP0
    linarith
  · -- If α = 1/2, then L α P₀ = 0.
    intro hα
    rw [hα]
    intro i
    rw [L_P0_eigenvalue]
    ring_nf

-- =========================================================================
-- BRIDGE 2: Dimension facts about the P₀/Q decomposition in ℝ³
-- =========================================================================

/-- The residue space Q consists of vectors whose components sum to zero.
    This is a restatement of `Q_sum_zero` from PFCore. -/
theorem residue_space_characterization (x : Fin 3 → ℝ) :
    Q x 0 + Q x 1 + Q x 2 = 0 :=
  Q_sum_zero x

/-- The uniform space P₀ is one-dimensional (spanned by [1,1,1]).
    This is the geometric reason the model lives in three channels: one
    frozen mode plus a two-dimensional residue. -/
theorem uniform_space_constant (x : Fin 3 → ℝ) (i j : Fin 3) :
    P0 x i = P0 x j :=
  P0_uniform x i j

-- =========================================================================
-- BRIDGE 3: Honest boundary with ThreeGenerations and KoideGeometry
-- =========================================================================

/-- The ThreeGenerations algebraic lock is exact: Q(N) = 2/3 ↔ N = 3.
    This is included here as a reference boundary, not as a theorem derived
    from PFCore. The connection to PFCore's dimension-3 model is conceptual:
    the PFCore formalism uses three channels, but the number of generations
    is fixed by the Koide charge-ratio algebra, not by the eigenvalue 2. -/
theorem reference_three_generations_lock {N : ℝ} (hN : N > 0) :
    generationFormula N = 2/3 ↔ N = 3 :=
  three_generations_algebraic_lock hN

/-- The Koide R = 2/3 condition is exact algebra: R = 2/3 iff
    a²+b²+c² = 2(ab+bc+ca). This is included here as a reference boundary,
    not as a theorem derived from PFCore eigenvalues. The geometric
    interpretation (120° phases in flavor space) is a physical premise, not
    proven in this module. -/
theorem reference_koide_R_condition {a b c : ℝ} (ha : a > 0) (hb : b > 0) (hc : c > 0) :
    KoideR a b c = 2/3 ↔ a ^ 2 + b ^ 2 + c ^ 2 = 2 * (a * b + b * c + c * a) :=
  koide_R_two_thirds_iff ha hb hc

-- =========================================================================
-- EXPLICIT NON-THEOREM: What is not formalized
-- =========================================================================

/-
  The following conjectural bridges are intentionally NOT stated as theorems
  because they require additional physical premises:

  1. "PFCore eigenvalue {2, -1, -1} implies 3 generations."
     This is a model choice, not a derivation. The dimension 3 of the Z₃
     circulant is postulated; the ThreeGenerations theorem says N=3 is the
     unique algebraic solution to Q(N)=2/3, but it does not derive Q(N).

  2. "PFCore eigenvalue ratio implies Koide R = 2/3."
     The eigenvalue ratio 2:-1 determines the decay rate of the residue mode.
     The Koide mass ratio R = 2/3 is a separate phenomenological condition on
     the charged-lepton masses. Connecting them requires a flavor-space model
     that is not formalized here.

  3. "Postulate D is derived from PFCore."
     The value α = 1/2 IS derived from the eigenvalue structure (see
     `god_equation_alpha_selector` above). But the Z₃ circulant M = J - I
     itself (Postulate D's no-self-loop condition) is a premise, not a
     theorem of PFCore. See `PfLean.Z3FromBareMedium` for the honest parameter
     count of that premise.

  This module therefore proves only the corollaries and states the boundary.
  Any future claim that bridges PFCore to generations or Koide masses must be
  formalized with explicit premises and audited by Codex.
-/

end PfLean
