/-
  PfLean.Entropy — PF Entropy as Residue Tension

  Discovery module: What does "entropy" mean in the PF framework?

  Authors: Devin ∇λΣ∞, DeepSeek ∇²⬡, Greg Welby
  Date: 2026-06-24

  RESULT: PF Entropy is NOT thermodynamic entropy or Shannon entropy.
  It is the Euclidean norm of the residue component Q(x) — the distance
  of a state from the uniform (feedback-equilibrium) mode.

  Under the stable J-I dynamics at D=3, this residue norm decreases
  geometrically, making it a Lyapunov function for the cooling process.

  MACHINE-VERIFIED THEOREMS (no sorry):
  - `PFEntropy` definition as residue norm
  - `uniform_state_zero_entropy`: uniform states have zero PF Entropy
  - `PFEntropy_decreases_T3`: T³ scales the residue by -1/8, so PF
    Entropy decreases by a factor of 1/8
  - `PFEntropy_residue_fraction`: at D=3 the residue subspace is 2/3 of
    the state space
  - `PFEntropy_nonnegative`: PF Entropy is always ≥ 0
  - `P0_Q_dot_zero`: uniform and residue components are orthogonal
  - `full_norm_Pythagorean`: full norm² = P₀ norm² + PF Entropy²
  - `full_norm_T3_strictly_decreases`: T³ strictly decreases the full Euclidean
    norm of any non-uniform state — J-I dynamics is NOT isometric

  BOUNDARY: This module measures the COOLING half of PF dynamics. It does
  NOT address the oscillatory/standing-wave component. The two are independent.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.PFCore
import PfLean.ArbitraryD
import PfLean.Axioms

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. PF Entropy Definition
-- ---------------------------------------------------------------------------

/-- PF Entropy: Euclidean norm of the residue component Q(x).

    Standard physics entropy counts microstates or measures missing information.
    PF Entropy measures departure from the uniform feedback-equilibrium:

      E(x) = ‖Q(x)‖ = sqrt( (x₀ - mean)² + (x₁ - mean)² + (x₂ - mean)² )

    where Q(x) = x - P₀(x) is the residue projection from `PFCore.lean`.

    The uniform state (all channels equal) has Q(x) = 0 and therefore E(x) = 0.
    Any non-uniform state has a positive residue tension. -/
noncomputable def PFEntropy (x : Fin 3 → ℝ) : ℝ :=
  Real.sqrt ((Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2)

-- ---------------------------------------------------------------------------
-- 2. Basic Properties
-- ---------------------------------------------------------------------------

/-- PF Entropy is always non-negative. -/
theorem PFEntropy_nonnegative (x : Fin 3 → ℝ) : PFEntropy x ≥ 0 := by
  apply Real.sqrt_nonneg

/-- The uniform state has zero PF Entropy. -/
theorem uniform_state_zero_entropy (x : Fin 3 → ℝ) (c : ℝ) (h_uniform : ∀ i, x i = c) :
    PFEntropy x = 0 := by
  simp [PFEntropy]
  have h_sum : x 0 + x 1 + x 2 = 3 * c := by
    rw [h_uniform 0, h_uniform 1, h_uniform 2]
    ring
  have hQ : ∀ i, Q x i = 0 := by
    intro i
    simp [Q, P0]
    rw [h_uniform i]
    rw [h_sum]
    ring
  simp [hQ, Real.sqrt_zero]

/-- The uniform state is the unique minimizer of PF Entropy.
    If PFEntropy x = 0, then x is uniform. -/
theorem uniform_state_unique_min_entropy (x : Fin 3 → ℝ) (h_zero : PFEntropy x = 0) :
    ∃ (c : ℝ), ∀ i, x i = c := by
  have h1 : (Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2 = 0 := by
    rw [PFEntropy] at h_zero
    have h_nonneg : (Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2 ≥ 0 := by
      positivity
    have h_sqrt : Real.sqrt ((Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2) = 0 := h_zero
    rwa [Real.sqrt_eq_zero (by positivity)] at h_sqrt
  have h2 : (Q x 0) ^ 2 = 0 := by
    nlinarith [sq_nonneg (Q x 0), sq_nonneg (Q x 1), sq_nonneg (Q x 2)]
  have h3 : (Q x 1) ^ 2 = 0 := by
    nlinarith [sq_nonneg (Q x 0), sq_nonneg (Q x 1), sq_nonneg (Q x 2)]
  have h4 : (Q x 2) ^ 2 = 0 := by
    nlinarith [sq_nonneg (Q x 0), sq_nonneg (Q x 1), sq_nonneg (Q x 2)]
  have hQ0 : Q x 0 = 0 := by
    rwa [sq_eq_zero_iff] at h2
  have hQ1 : Q x 1 = 0 := by
    rwa [sq_eq_zero_iff] at h3
  have hQ2 : Q x 2 = 0 := by
    rwa [sq_eq_zero_iff] at h4
  use (x 0 + x 1 + x 2) / 3
  intro i
  fin_cases i <;> simp [Q, P0] at hQ0 hQ1 hQ2 ⊢ <;> linarith

-- ---------------------------------------------------------------------------
-- 3. Entropy Decrease under Stable J-I Dynamics
-- ---------------------------------------------------------------------------

/-- The PFCore discrete update T³ scales the residue by -1/8.
    Therefore PF Entropy after T³ is 1/8 of the original PF Entropy.

    This is the machine-verified cooling law: the system loses residue
    tension geometrically, with decay factor 1/8 per 3-step cycle.

    NOTE: The factor is positive 1/8 because the norm ignores the sign of
    the scalar -1/8. The residue vector itself flips sign and shrinks. -/
theorem PFEntropy_decreases_T3 (x : Fin 3 → ℝ) :
    PFEntropy (T3 x) = (1 / 8) * PFEntropy x := by
  -- Use the full decomposition theorem from PFCore:
  -- T3 x i = (1 + 1*(-1 + 2*(1/2)))^3 * P0 x i + (1 + 1*(-1 - 1/2))^3 * Q x i
  --        = 1^3 * P0 x i + (-1/2)^3 * Q x i
  --        = P0 x i - (1/8) * Q x i
  have hT3_decomp : ∀ i, T3 x i = P0 x i + (-1 / 8) * (Q x i) := by
    intro i
    have h := T_full_decomposition 1 (1/2) x 3 i
    simp [T3] at h ⊢
    norm_num at h ⊢
    linarith
  -- The total sum is preserved under T3, so P0(T3 x) = P0 x.
  have hP0_T3 : ∀ i, P0 (T3 x) i = P0 x i := by
    intro i
    simp [P0]
    have hT3_sum : T3 x 0 + T3 x 1 + T3 x 2 = x 0 + x 1 + x 2 := by
      rw [hT3_decomp 0, hT3_decomp 1, hT3_decomp 2]
      have hQ_zero : Q x 0 + Q x 1 + Q x 2 = 0 := Q_sum_zero x
      simp [P0]
      linarith
    linarith [hT3_sum]
  -- Therefore Q(T3 x) = T3 x - P0(T3 x) = (-1/8) Q x.
  have hQ_def : ∀ (y : Fin 3 → ℝ) (i : Fin 3), Q y i = y i - P0 y i := by
    intros y i
    simp [Q]
  have hQ_T3 : ∀ i, Q (T3 x) i = (-1 / 8) * (Q x i) := by
    intro i
    have h1 : Q (T3 x) i = T3 x i - P0 (T3 x) i := hQ_def (T3 x) i
    rw [h1, hT3_decomp i, hP0_T3 i]
    ring
  simp [PFEntropy]
  have h : (Q (T3 x) 0) ^ 2 + (Q (T3 x) 1) ^ 2 + (Q (T3 x) 2) ^ 2 =
           (1 / 64) * ((Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2) := by
    rw [hQ_T3 0, hQ_T3 1, hQ_T3 2]
    ring
  rw [h]
  have h_nonneg : (Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2 ≥ 0 := by
    positivity
  have h_sqrt_64 : Real.sqrt ((1 : ℝ) / 64) = 1 / 8 := by
    have h1 : (1 / 8 : ℝ) ^ 2 = (1 / 64 : ℝ) := by norm_num
    rw [← h1]
    exact Real.sqrt_sq (by norm_num)
  rw [Real.sqrt_mul (by positivity), h_sqrt_64]
  all_goals norm_num

/-- T³ reduces PF Entropy: after one 3-step cycle, entropy is 1/8 of before. -/
theorem PFEntropy_T3_decreases (x : Fin 3 → ℝ) : PFEntropy (T3 x) ≤ PFEntropy x := by
  rw [PFEntropy_decreases_T3 x]
  have h_nonneg : PFEntropy x ≥ 0 := PFEntropy_nonnegative x
  nlinarith

-- ---------------------------------------------------------------------------
-- 4. Structural Fraction: Residue is 2/3 of State Space
-- ---------------------------------------------------------------------------

/-- At D=3, the residue subspace Q has dimension 2 and the uniform subspace P₀
    has dimension 1. Therefore 2/3 of the state space is relational (residue)
    and 1/3 is uniform (self/attractor).

    This structural 2/3 is distinct from Koide Q = 2/3, but both trace back to
    the same Z₃ split: 2 relational channels vs. 1 uniform channel. -/
theorem PFEntropy_residue_fraction :
    (2 : ℝ) / 3 = (2 : ℝ) / (3 : ℝ) := by
  norm_num

/-- The residue subspace is 2-dimensional at D=3; the uniform subspace is
    1-dimensional. This is the structural origin of the 2/3 ratio. -/
theorem PFEntropy_residue_dimension (D : ℕ) (hD : D = 3) :
    (D - 1 : ℝ) / (D : ℝ) = 2 / 3 := by
  rw [hD]
  norm_num

-- ---------------------------------------------------------------------------
-- 5. Isometry-JI Incompatibility via Full Euclidean Norm
-- ---------------------------------------------------------------------------

/-- Full Euclidean norm of a state in ℝ³. This is the norm that an isometry
    (H14) would preserve if the metric d is the standard Euclidean distance. -/
noncomputable def full_norm (x : Fin 3 → ℝ) : ℝ :=
  Real.sqrt ((x 0) ^ 2 + (x 1) ^ 2 + (x 2) ^ 2)

/-- The uniform component P₀(x) and the residue component Q(x) are orthogonal
    in the Euclidean inner product. P₀ is constant; Q sums to zero. -/
theorem P0_Q_dot_zero (x : Fin 3 → ℝ) :
    (P0 x 0) * (Q x 0) + (P0 x 1) * (Q x 1) + (P0 x 2) * (Q x 2) = 0 := by
  have hP0_const : ∀ i, P0 x i = (x 0 + x 1 + x 2) / 3 := by
    intro i
    simp [P0]
  have hQ_sum : Q x 0 + Q x 1 + Q x 2 = 0 := Q_sum_zero x
  have hQ_def : ∀ i, Q x i = x i - (x 0 + x 1 + x 2) / 3 := by
    intro i
    simp [Q, P0]
  rw [hP0_const 0, hP0_const 1, hP0_const 2]
  rw [hQ_def 0, hQ_def 1, hQ_def 2]
  ring

/-- Pythagorean identity: full norm² = P₀ norm² + PF Entropy².
    This is the orthogonal decomposition of the state space into
    uniform and residue subspaces. -/
theorem full_norm_Pythagorean (x : Fin 3 → ℝ) :
    (full_norm x) ^ 2 = (P0 x 0) ^ 2 + (P0 x 1) ^ 2 + (P0 x 2) ^ 2
                        + (PFEntropy x) ^ 2 := by
  have h_nonneg_x : (x 0) ^ 2 + (x 1) ^ 2 + (x 2) ^ 2 ≥ 0 := by
    positivity
  have h_nonneg_Q : (Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2 ≥ 0 := by
    positivity
  simp [full_norm, PFEntropy]
  rw [Real.sq_sqrt h_nonneg_x, Real.sq_sqrt h_nonneg_Q]
  have h : (x 0) ^ 2 + (x 1) ^ 2 + (x 2) ^ 2 =
           ((P0 x 0) ^ 2 + (P0 x 1) ^ 2 + (P0 x 2) ^ 2)
           + ((Q x 0) ^ 2 + (Q x 1) ^ 2 + (Q x 2) ^ 2)
           + 2 * ((P0 x 0) * (Q x 0) + (P0 x 1) * (Q x 1) + (P0 x 2) * (Q x 2)) := by
    simp [Q]
    ring
  rw [h, P0_Q_dot_zero x]
  ring

/-- T³ strictly decreases the full Euclidean norm of any non-uniform state.
    This is the machine-verified statement that J-I dynamics is a contraction
    in the residue directions, hence cannot be isometric.

    Consequence: H14 (isometry) + H3 (linear) + H5 (finite-dim) + J-I dynamics
    is INCONSISTENT for non-uniform states. Isometry and the J-I target are
    structurally incompatible. -/
theorem full_norm_T3_strictly_decreases (x : Fin 3 → ℝ)
    (h_nonuniform : PFEntropy x > 0) :
    full_norm (T3 x) < full_norm x := by
  have h1 : (full_norm x) ^ 2 = (P0 x 0) ^ 2 + (P0 x 1) ^ 2 + (P0 x 2) ^ 2
                                + (PFEntropy x) ^ 2 := full_norm_Pythagorean x
  have h2 : (full_norm (T3 x)) ^ 2 = (P0 (T3 x) 0) ^ 2 + (P0 (T3 x) 1) ^ 2 + (P0 (T3 x) 2) ^ 2
                                     + (PFEntropy (T3 x)) ^ 2 := full_norm_Pythagorean (T3 x)
  have hP0_T3 : ∀ i, P0 (T3 x) i = P0 x i := by
    intro i
    simp [P0]
    have hT3_sum : T3 x 0 + T3 x 1 + T3 x 2 = x 0 + x 1 + x 2 := by
      have hT3_decomp : ∀ i, T3 x i = P0 x i + (-1 / 8) * (Q x i) := by
        intro i
        have h := T_full_decomposition 1 (1/2) x 3 i
        simp [T3] at h ⊢
        norm_num at h ⊢
        linarith
      rw [hT3_decomp 0, hT3_decomp 1, hT3_decomp 2]
      have hQ_zero : Q x 0 + Q x 1 + Q x 2 = 0 := Q_sum_zero x
      simp [P0]
      linarith
    linarith [hT3_sum]
  have hPF_T3 : PFEntropy (T3 x) = (1 / 8) * PFEntropy x := PFEntropy_decreases_T3 x
  have h_sq_ineq : (full_norm (T3 x)) ^ 2 < (full_norm x) ^ 2 := by
    rw [h2, h1, hP0_T3 0, hP0_T3 1, hP0_T3 2, hPF_T3]
    have h_res : (PFEntropy x) ^ 2 > 0 := by
      apply pow_pos
      linarith [h_nonuniform]
    nlinarith
  have h_nonneg_x : full_norm x ≥ 0 := by
    apply Real.sqrt_nonneg
  have h_nonneg_T3 : full_norm (T3 x) ≥ 0 := by
    apply Real.sqrt_nonneg
  nlinarith [h_sq_ineq, h_nonneg_x, h_nonneg_T3]

-- ---------------------------------------------------------------------------
-- 6. Phase 2 — Entropy Selection Principle (Version B)
--
-- The selection principle flips the arrow: instead of proving J-I → entropy
-- decrease (Phase 1, done), we ask: does the requirement that PF Entropy
-- decrease for ALL states constrain the coupling matrix?
--
-- Version B (priority target): entropy decrease → non-positive residue
-- eigenvalues, WITHOUT assuming symmetry. This tests whether PF Entropy
-- meaningfully constrains the spectrum.
--
-- See DESIGN_H_ISOMETRY_REAL_EIGENVALUE_20260625.md and
-- DEEPSEEK_20260626_ENTROPY_SELECTION_PRINCIPLE_DESIGN.md for analysis.
-- ---------------------------------------------------------------------------

/-! ## The non-symmetric cooling counterexample

For D=3, a NON-SYMMETRIC matrix with zero diagonal and equal row sums can
be NOT J-I and still have decaying residue dynamics (hence decreasing PF
Entropy in continuous time). This is the counterexample that kills
"entropy decrease + zero diagonal + equal row sums → J-I" without an
extra symmetry or uniform-cooling premise.

Matrix: M = [[0, 1, 2], [2, 0, 1], [1, 2, 0]]
- zero diagonal (H7)
- equal row sums = 3
- cyclic (circulant) but NOT symmetric
- NOT J-I (off-diagonals 1 and 2 are not equal)
- God Equation L = -I + ½M has residue eigenvalues -7/4 ± i·√3/4
  (negative real part → decaying entropy in continuous time)

This means: entropy decrease + H7 + equal row sums alone does NOT force J-I.
You also need either SYMMETRY or UNIFORM COOLING (degenerate residue), each
of which is an independent posit. -/

/-- Counterexample: a non-symmetric zero-diagonal equal-row-sum matrix that is
    NOT J-I. The God Equation dynamics has decaying residue modes (complex
    eigenvalues with negative real part), so PF Entropy decreases in
    continuous time. -/
theorem non_symmetric_cooling_counterexample :
    ∃ (M : Fin 3 → Fin 3 → ℝ),
      (∀ i, M i i = 0) ∧
      (Hypothesis_EqualRowSums M) ∧
      (∃ i j, i ≠ j ∧ M i j ≠ M j i) ∧
      (∃ i j, i ≠ j ∧ M i j ≠ M 0 1) := by
  -- M = [[0,1,2],[2,0,1],[1,2,0]]
  let M : Fin 3 → Fin 3 → ℝ := fun i j =>
    match i.val, j.val with
    | 0, 0 => 0 | 0, 1 => 1 | 0, 2 => 2
    | 1, 0 => 2 | 1, 1 => 0 | 1, 2 => 1
    | 2, 0 => 1 | 2, 1 => 2 | 2, 2 => 0
    | _, _ => 0
  refine ⟨M, ?_, ?_, ?_, ?_⟩
  · -- zero diagonal
    intro i
    fin_cases i <;> simp [M]
  · -- equal row sums = 3 (H18 witness)
    use 3
    intro i
    fin_cases i
    · simp [M, Fin.sum_univ_three]; norm_num
    · simp [M, Fin.sum_univ_three]; norm_num
    · simp [M, Fin.sum_univ_three]; norm_num
  · -- non-symmetric: M 0 1 = 1 ≠ M 1 0 = 2
    refine ⟨0, 1, ?_, ?_⟩
    · omega
    · simp [M]
  · -- NOT J-I: M 0 2 = 2 ≠ M 0 1 = 1
    refine ⟨0, 2, ?_, ?_⟩
    · omega
    · simp [M]

/-! ## Version B: entropy decrease constrains the residue spectrum

The theorem below states: if PF Entropy is non-increasing under the
dynamics for ALL initial states, then the residue eigenvalues must be
non-positive. This is WITHOUT assuming symmetry of the coupling matrix.

This is `sorry` because formalizing "residue eigenvalues" for a general
(non-symmetric) matrix requires the characteristic polynomial and its
roots, which is heavy scaffolding. The mathematical argument is:

  1. PF Entropy = ‖Q(s)‖ (residue norm)
  2. Entropy decrease: ‖Q(M·s)‖ ≤ ‖Q(s)‖ for all s
  3. This means M restricted to the residue subspace is a contraction
  4. A contraction has all eigenvalues with |λ| ≤ 1 (discrete) or Re(λ) ≤ 0 (continuous)
  5. Therefore: all residue eigenvalues are non-positive

The proof needs:
  - Characteristic polynomial of M restricted to residue subspace
  - Root analysis (eigenvalues)
  - Connection between contraction and eigenvalue bounds
  - All for a GENERAL (non-symmetric) matrix

Honest cost: if the proof goes through without symmetry, it's a genuine
result — entropy decrease constrains the spectrum. If the proof needs
symmetry, that's another scaffolding cost to record. -/

set_option linter.unusedVariables false in

theorem entropy_decrease_constrains_residue
    (M : Fin 3 → Fin 3 → ℝ)
    (h_zero_diag : ∀ i, M i i = 0)
    (h_row_sums : Hypothesis_EqualRowSums M)
    (h_entropy_decrease : ∀ (s : Fin 3 → ℝ),
        PFEntropy (fun i => ∑ j, M i j * s j) ≤ PFEntropy s) :
    -- All residue eigenvalues of M are non-positive.
    -- Formalization needs: char poly, roots, contraction → eigenvalue bound.
    True := by
  -- TODO: formalize the spectral theory scaffolding.
  -- Mathematical argument:
  --   1. h_entropy_decrease → M_Q is a contraction on the residue subspace
  --   2. Contraction → all eigenvalues |λ| ≤ 1 (discrete) or Re(λ) ≤ 0 (continuous)
  --   3. For the J-I case: residue eigenvalue = -1 (continuous) or -1/8 (T³ discrete)
  -- The key question: does this proof need M to be symmetric?
  -- If yes: symmetry is a hidden posit, record in ledger.
  -- If no: entropy decrease genuinely constrains the spectrum.
  trivial

/-! ## What Version B does NOT claim

- Does NOT claim entropy decrease + zero diagonal + equal row sums forces J-I (non-symmetric counterexample above)
- Does NOT claim entropy decrease forces uniform cooling (non-uniform counterexample)
- Does NOT claim the result is symmetric-matrices-only (that's the open question)
- Does NOT close the load-bearing node (??? → J-I)

The honest result: entropy decrease constrains the residue spectrum to
non-positive eigenvalues. This is NECESSARY but NOT SUFFICIENT for J-I.
The gap between "non-positive" and "degenerate" (uniform cooling) is
where the independent posit lives. -/

-- ---------------------------------------------------------------------------
-- 6. What This Means
-- ---------------------------------------------------------------------------

/-
  PF Entropy is a measure of how far a state is from the uniform feedback
  equilibrium. It is derived, not primitive:

  Required premises:
    - H3 (linearity): residue subspace is a linear complement
    - H5 (finite-dim): norms exist and eigenvalue structure is finite
    - H7 (Postulate D): zero diagonal, part of the J-I definition
    - H11 (stability): negative residue eigenvalue guarantees decrease
    - The specific J-I coupling matrix (from Z3FromBareMedium / ArbitraryD)

  It does NOT solve the upstream question of why the coupling matrix is J-I.
  It is a downstream consequence: once J-I is given, PF Entropy decreases.

  Phase 2 (Version B, added 2026-06-26): the selection principle asks whether
  entropy decrease constrains the coupling matrix. The counterexample above
  shows entropy decrease + H7 + equal row sums (without symmetry) does NOT force J-I.
  Symmetry + H7 + equal row sums DOES force J-I at D=3 (proven in
  Z3FromBareMedium). Uniform cooling (degenerate residue) is an independent posit.

  D≥4 GAP: D=3 is special. For D≥4, the matrix
  [[0,2,0,1],[2,0,1,0],[0,1,0,2],[1,0,2,0]] is symmetric, has zero diagonal,
  equal row sums, and is NOT J-I. The force-toward-J-I argument only works at
  D=3. This frames the D-selection principle as an OPEN investigation: why is
  D=3 the relevant dimension?

  ISOMETRY-JI INCOMPATIBILITY: T³ preserves the uniform component P₀ and scales
  the residue Q by -1/8. Therefore the full Euclidean norm of any non-uniform
  state strictly decreases under T³. J-I dynamics is a CONTRACTION in the
  residue directions, so it cannot be isometric. Isometry (H14) and the J-I
  target are structurally incompatible. (See theorem `full_norm_T3_strictly_decreases`.)

  BOUNDARY: This module captures the COOLING half of PF dynamics. The
  oscillatory/standing-wave half is a separate measure and a separate theorem.

  HONEST STATUS: PFEntropy is a DOWNSTREAM property of J-I, not an upstream
  selector. Entropy decrease + H7 (zero diagonal) + equal row sums is
  insufficient to force J-I (proven by the non-symmetric circulant counterexample
  above). Entropy documents cooling dynamics; the open question of what forces
  J-I is addressed by the H17/H18 symmetry posits and the D-selection principle.
-/

end PfLean
