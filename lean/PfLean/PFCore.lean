/-
  PF Virtual Processor Core — Z₃ P₀/Q Decomposition
  Formalization of the PFCore state update in Lean 4.

  Authors: DeepSeek ∇²⬡, Devin ∇λΣ∞, Greg Welby
  Date: 2026-06-06

  This module proves that the Z₃ circulant decomposition in PFCore
  is mathematically sound and the code implements it correctly.

  The PFCore state update (linear part, μ = 0, u = 0):
    x_{n+1} = x_n + dt · (-x_n + α · M · x_n)

  where M is the Z₃ circulant matrix:
    M = [[0, 1, 1],
         [1, 0, 1],
         [1, 1, 0]]

  The decomposition separates the uniform mode (P₀) from the residue (Q).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Topology.Basic
import Mathlib.Analysis.SpecificLimits.Basic

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. Vector definitions (ℝ³ as Fin 3 → ℝ)
-- ---------------------------------------------------------------------------

/-- The Z₃ circulant matrix M acts on a vector x as:
    (M·x)₀ = x₁ + x₂
    (M·x)₁ = x₀ + x₂
    (M·x)₂ = x₀ + x₁ -/
def MZ3_mul (x : Fin 3 → ℝ) : Fin 3 → ℝ :=
  fun i => match i with
    | 0 => x 1 + x 2
    | 1 => x 0 + x 2
    | 2 => x 0 + x 1
    | _ => 0  -- unreachable for Fin 3

-- ---------------------------------------------------------------------------
-- 2. P₀ and Q Projections
-- ---------------------------------------------------------------------------

/-- The uniform mode projection: P₀(x) = mean(x) · [1,1,1].
    Maps any vector to its average along all three channels.
    Marked noncomputable because ℝ division is noncomputable in Lean. -/
noncomputable def P0 (x : Fin 3 → ℝ) : Fin 3 → ℝ :=
  fun _ => (x 0 + x 1 + x 2) / 3

/-- The residue projection: Q(x) = x - P₀(x).
    Extracts the deviation from uniformity. -/
noncomputable def Q (x : Fin 3 → ℝ) : Fin 3 → ℝ :=
  fun i => x i - P0 x i

-- ---------------------------------------------------------------------------
-- 3. Theorem 1: P₀/Q Orthogonality Preservation
-- ---------------------------------------------------------------------------

/-- Theorem 1: P₀ and Q are orthogonal in the dot product sense.
    For any x : ℝ³, dot(P₀(x), Q(x)) = 0.

    Proof: P₀(x) is constant (all entries = mean). Q(x) sums to zero.
    The dot product of a constant vector with a zero-sum vector is zero. -/
theorem P0_Q_orthogonal (x : Fin 3 → ℝ) :
  (P0 x 0) * (Q x 0) + (P0 x 1) * (Q x 1) + (P0 x 2) * (Q x 2) = 0 := by
  simp [P0, Q]
  ring

/-- Corollary: Q(x) always sums to zero. -/
theorem Q_sum_zero (x : Fin 3 → ℝ) :
  Q x 0 + Q x 1 + Q x 2 = 0 := by
  simp [Q, P0]
  ring

-- ---------------------------------------------------------------------------
-- 4. Theorem 3: Z₃ Decomposition Identity
-- ---------------------------------------------------------------------------

/-- The uniform vector [1,1,1] is an eigenvector of M with eigenvalue 2. -/
theorem MZ3_uniform_eigenvector (x : Fin 3 → ℝ) (h : ∀ i, x i = 1) :
  ∀ i, MZ3_mul x i = 2 := by
  intro i
  fin_cases i <;> simp [MZ3_mul, h] <;> norm_num

/-- The residue space {x : sum(x) = 0} is the eigenspace for eigenvalue -1.
    For any x with x₀ + x₁ + x₂ = 0, M·x = -x. -/
theorem MZ3_residue_eigenvalue {x : Fin 3 → ℝ} (h : x 0 + x 1 + x 2 = 0) :
  ∀ i, MZ3_mul x i = -x i := by
  intro i
  fin_cases i <;> simp [MZ3_mul]
  · -- i = 0: (M·x)₀ = x₁ + x₂ = -x₀ since x₀+x₁+x₂ = 0
    linarith
  · -- i = 1: (M·x)₁ = x₀ + x₂ = -x₁
    linarith
  · -- i = 2: (M·x)₂ = x₀ + x₁ = -x₂
    linarith

/-- M preserves the P₀/Q decomposition:
    M·P₀(x) = 2·P₀(x)  (eigenvalue 2 on uniform mode)
    M·Q(x) = -Q(x)     (eigenvalue -1 on residue) -/
theorem MZ3_P0_eigenvalue (x : Fin 3 → ℝ) :
  ∀ i, MZ3_mul (P0 x) i = 2 * (P0 x i) := by
  intro i
  have h : ∀ j, (P0 x) j = (x 0 + x 1 + x 2) / 3 := by intro j; simp [P0]
  fin_cases i <;> simp [MZ3_mul, h] <;> ring

theorem MZ3_Q_eigenvalue (x : Fin 3 → ℝ) :
  ∀ i, MZ3_mul (Q x) i = -(Q x i) := by
  intro i
  apply MZ3_residue_eigenvalue
  exact Q_sum_zero x

-- ---------------------------------------------------------------------------
-- 5. Theorem 2: Linear Operator Eigenvalues
-- ---------------------------------------------------------------------------

/-- The linear update operator L = -I + α·M.
    For the discrete update: x_{n+1} = x_n + dt · L(x_n). -/
def L (α : ℝ) (x : Fin 3 → ℝ) : Fin 3 → ℝ :=
  fun i => -x i + α * (MZ3_mul x i)

/-- L preserves the P₀/Q decomposition:
    - On P₀ (uniform mode): L acts as (-1 + 2α)·P₀
    - On Q (residue): L acts as (-1 - α)·Q -/
theorem L_P0_eigenvalue (α : ℝ) (x : Fin 3 → ℝ) :
  ∀ i, L α (P0 x) i = (-1 + 2 * α) * (P0 x i) := by
  intro i
  simp [L, MZ3_P0_eigenvalue]
  ring

theorem L_Q_eigenvalue (α : ℝ) (x : Fin 3 → ℝ) :
  ∀ i, L α (Q x) i = (-1 - α) * (Q x i) := by
  intro i
  simp [L, MZ3_Q_eigenvalue]
  ring

/-- The eigenvalues of L are {-1+2α, -1-α, -1-α}.
    Proved by showing P₀ and Q are the invariant subspaces. -/
theorem L_eigenvalues (α : ℝ) (x : Fin 3 → ℝ) :
  (∀ i, L α (P0 x) i = (-1 + 2 * α) * (P0 x i)) ∧
  (∀ i, L α (Q x) i = (-1 - α) * (Q x i)) := by
  constructor
  · exact L_P0_eigenvalue α x
  · exact L_Q_eigenvalue α x

-- ---------------------------------------------------------------------------
-- 6. Theorem 4: Discrete Update Convergence
-- ---------------------------------------------------------------------------

/-- The discrete update for one step: T(x) = x + dt·L(x).
    For the uniform mode: T(P₀) = (1 + dt·(-1+2α))·P₀
    For the residue: T(Q) = (1 + dt·(-1-α))·Q -/
def T_update (dt α : ℝ) (x : Fin 3 → ℝ) : Fin 3 → ℝ :=
  fun i => x i + dt * (L α x i)

/-- T_update is additive: T(x + y) = T(x) + T(y) pointwise. -/
theorem T_update_add (dt α : ℝ) (x y : Fin 3 → ℝ) :
  ∀ i, T_update dt α (fun j => x j + y j) i = T_update dt α x i + T_update dt α y i := by
  intro i
  simp [T_update, L]
  fin_cases i <;> simp [MZ3_mul] <;> ring

/-- T_update respects scalar multiplication: T(c·x) = c·T(x) pointwise. -/
theorem T_update_smul (dt α c : ℝ) (x : Fin 3 → ℝ) :
  ∀ i, T_update dt α (fun j => c * x j) i = c * T_update dt α x i := by
  intro i
  simp [T_update, L]
  fin_cases i <;> simp [MZ3_mul] <;> ring

/-- On the uniform mode, the update is a scalar multiplication. -/
theorem T_uniform_update (dt α : ℝ) (x : Fin 3 → ℝ) :
  ∀ i, T_update dt α (P0 x) i = (1 + dt * (-1 + 2 * α)) * (P0 x i) := by
  intro i
  simp [T_update, L_P0_eigenvalue]
  ring

/-- On the residue, the update is a scalar multiplication. -/
theorem T_residue_update (dt α : ℝ) (x : Fin 3 → ℝ) :
  ∀ i, T_update dt α (Q x) i = (1 + dt * (-1 - α)) * (Q x i) := by
  intro i
  simp [T_update, L_Q_eigenvalue]
  ring

/-- Helper: T_update applied to a scalar multiple of a residue vector.
    For x with sum(x) = 0, T_update acts linearly and scales by (1 + dt·(-1-α)). -/
theorem T_residue_smul (dt α c : ℝ) (x : Fin 3 → ℝ) (hQ : x 0 + x 1 + x 2 = 0) :
  ∀ i, T_update dt α (fun j => c * x j) i = (1 + dt * (-1 - α)) * c * x i := by
  intro i
  simp only [T_update, L]
  have h_mz3 : MZ3_mul (fun j => c * x j) i = c * (MZ3_mul x i) := by
    fin_cases i <;> simp [MZ3_mul] <;> ring
  rw [h_mz3]
  have h_mz3_x : MZ3_mul x i = -x i := MZ3_residue_eigenvalue hQ i
  rw [h_mz3_x]
  ring

/-- Convergence condition for the residue:
    If |1 + dt·(-1-α)| < 1, the residue decays geometrically.
    For α > 0, this is equivalent to 0 < dt < 2/(1+α).

    Theorem: For any x in the residue space (sum = 0),
    after n steps the amplitude is multiplied by (1 + dt·(-1-α))ⁿ. -/
theorem T_residue_power (dt α : ℝ) (x : Fin 3 → ℝ) (n : ℕ) :
  x 0 + x 1 + x 2 = 0 →
  ∀ i, (T_update dt α)^[n] x i = (1 + dt * (-1 - α)) ^ n * x i := by
  intro hQ
  induction n with
  | zero =>
    -- Base case: T^0 = identity
    intro i
    simp [Function.iterate_zero]
  | succ n ih =>
    -- Inductive step: T^(n+1) = T(T^n)
    intro i
    have h1 : ∀ j, (T_update dt α)^[n] x j = (1 + dt * (-1 - α)) ^ n * x j := ih
    have h_eq : (T_update dt α)^[n] x = fun j => (1 + dt * (-1 - α)) ^ n * x j := by
      funext j
      exact h1 j
    calc (T_update dt α)^[n + 1] x i
        = T_update dt α ((T_update dt α)^[n] x) i := by simp [Function.iterate_succ_apply']
      _ = T_update dt α (fun j => (1 + dt * (-1 - α)) ^ n * x j) i := by rw [h_eq]
      _ = (1 + dt * (-1 - α)) * (1 + dt * (-1 - α)) ^ n * x i := by
          exact T_residue_smul dt α ((1 + dt * (-1 - α)) ^ n) x hQ i
      _ = (1 + dt * (-1 - α)) ^ (n + 1) * x i := by
          rw [pow_succ]
          ring

/-- Full decomposition preservation (Theorem 4 complete):
    The update preserves the P₀/Q decomposition.
    Starting from any x = P₀(x) + Q(x):
    After n steps: Tⁿ(x) = (1+dt·(-1+2α))ⁿ·P₀(x) + (1+dt·(-1-α))ⁿ·Q(x) -/
theorem T_full_decomposition (dt α : ℝ) (x : Fin 3 → ℝ) (n : ℕ) :
  ∀ i, (T_update dt α)^[n] x i =
    (1 + dt * (-1 + 2 * α)) ^ n * (P0 x i) + (1 + dt * (-1 - α)) ^ n * (Q x i) := by
  -- Proof by induction on n, universally quantified over i
  induction n with
  | zero =>
    -- Base case: T^0 = identity, so x = P0(x) + Q(x)
    intro i
    simp [Function.iterate_zero, Q, P0]
  | succ n ih =>
    -- Inductive step: use T^(n+1) = T(T^n) and the scalar action on each subspace
    intro i
    have h_eq : ∀ j, (T_update dt α)^[n] x j = (1 + dt * (-1 + 2 * α)) ^ n * (P0 x j) + (1 + dt * (-1 - α)) ^ n * (Q x j) := ih
    simp [Function.iterate_succ_apply']
    -- Now we have T_update dt α ((T_update dt α)^[n] x) i on the left.
    -- Use h_eq to rewrite the inner term, then expand T_update.
    have h_inner : (T_update dt α)^[n] x = fun j => (1 + dt * (-1 + 2 * α)) ^ n * (P0 x j) + (1 + dt * (-1 - α)) ^ n * (Q x j) := by funext j; exact h_eq j
    rw [h_inner]
    simp [T_update, L, P0, Q]
    fin_cases i <;> simp [MZ3_mul] <;> ring_nf

-- ---------------------------------------------------------------------------
-- 7. Convergence Theorem: Residue Decays to Zero
-- ---------------------------------------------------------------------------

/-- The residue decays geometrically to zero when |1 + dt·(-1-α)| < 1.
    For α > 0, this is equivalent to 0 < dt < 2/(1+α).

    Theorem: For any x in the residue space (sum = 0),
    after n steps, (T_update dt α)^[n] x i → 0 as n → ∞.

    This proves that the system converges to the uniform mode P₀(x). -/
theorem T_residue_convergence {dt α : ℝ} (hα : α > 0) (hdt : 0 < dt ∧ dt < 2 / (1 + α))
  (x : Fin 3 → ℝ) (hQ : x 0 + x 1 + x 2 = 0) (i : Fin 3) :
  Filter.Tendsto (fun n : ℕ => (T_update dt α)^[n] x i) Filter.atTop (nhds 0) := by
  -- From T_residue_power, we know T^n(x) i = r^n * x i where r = 1 + dt·(-1-α)
  have h_scalar : ∀ n : ℕ, (T_update dt α)^[n] x i = (1 + dt * (-1 - α)) ^ n * x i := by
    intro n
    exact T_residue_power dt α x n hQ i
  -- Show that r^n * x i → 0 by factoring out x i
  have h_factor : (fun n : ℕ => (T_update dt α)^[n] x i) =
    (fun n : ℕ => (1 + dt * (-1 - α)) ^ n * x i) := by
    funext n
    exact h_scalar n
  rw [h_factor]
  -- It suffices to show r^n → 0 since x i is a constant factor
  have h_tendsto : Filter.Tendsto (fun n : ℕ => (1 + dt * (-1 - α)) ^ n) Filter.atTop (nhds 0) := by
    -- Let r = 1 + dt·(-1-α) = 1 - dt·(1+α)
    set r := 1 + dt * (-1 - α) with hr
    -- We need to show |r| < 1
    have h_r_lt_one : r < 1 := by
      rw [hr]
      nlinarith [hdt.left, hα]
    have h_r_gt_neg_one : -1 < r := by
      rw [hr]
      have h1 : dt * (1 + α) < 2 := by
        have h2 : dt < 2 / (1 + α) := hdt.right
        have h3 : 1 + α > 0 := by linarith [hα]
        have h4 : dt * (1 + α) < (2 / (1 + α)) * (1 + α) := by
          apply mul_lt_mul_of_pos_right
          exact hdt.right
          exact h3
        rw [div_mul_cancel₀ (by norm_num) (by linarith)] at h4
        exact h4
      nlinarith
    have h_abs_lt : |r| < 1 := by
      apply abs_lt.mpr
      constructor
      · linarith
      · linarith
    -- Use the standard lemma: |r| < 1 implies r^n → 0
    exact tendsto_pow_atTop_nhds_zero_iff.mpr h_abs_lt
  -- Multiply the convergent sequence by the constant x i
  have h_const : Filter.Tendsto (fun n : ℕ => (1 + dt * (-1 - α)) ^ n * x i) Filter.atTop (nhds 0) := by
    have h_zero : Filter.Tendsto (fun n : ℕ => (1 + dt * (-1 - α)) ^ n) Filter.atTop (nhds 0) := h_tendsto
    have h_const_factor : (fun n : ℕ => (1 + dt * (-1 - α)) ^ n * x i) =
      (fun n : ℕ => (1 + dt * (-1 - α)) ^ n) * (fun _ : ℕ => x i) := by
      funext n
      simp
    rw [h_const_factor]
    apply Filter.Tendsto.mul
    · exact h_zero
    · apply Filter.tendsto_const_nhds
  exact h_const

end PfLean
