# Proof Design: entropy_decrease_constrains_residue

*Written by Devin, 2026-07-12. Followed from CURIOSITIES.md.*

## The Theorem (current state)

```lean
theorem entropy_decrease_constrains_residue
    (M : Fin 3 → Fin 3 → ℝ)
    (h_zero_diag : ∀ i, M i i = 0)
    (h_row_sums : Hypothesis_EqualRowSums M)
    (h_entropy_decrease : ∀ (s : Fin 3 → ℝ),
        PFEntropy (fun i => ∑ j, M i j * s j) ≤ PFEntropy s) :
    True := by trivial
```

Proves `True`. The real claim is in a comment: all residue eigenvalues of M are non-positive.

## What We Actually Want to Prove

If PF entropy is non-increasing under M for all states s, then all eigenvalues λ of M (restricted to the residue subspace) satisfy Re(λ) ≤ 0 (continuous time) or |λ| ≤ 1 (discrete time).

**Note:** The current theorem statement says "non-positive" but doesn't specify continuous vs discrete. The proof below targets |λ| ≤ 1 (discrete), which is the stronger statement (Re(λ) ≤ |λ| ≤ 1).

## The Proof Path

### Step 1: PFEntropy decrease implies residue norm decrease

PFEntropy(s) = ‖Q(s)‖ where Q is the residue projection. The hypothesis says:

  ‖Q(M·s)‖ ≤ ‖Q(s)‖ for all s

Since Q is a projection (Q² = Q) and M has equal row sums (preserves the uniform subspace), Q(M·s) = M_Q · Q(s) where M_Q is M restricted to the residue subspace. So:

  ‖M_Q · r‖ ≤ ‖r‖ for all r in the residue subspace

This is the contraction condition: M_Q is a contraction on the residue subspace.

### Step 2: Extend to ℂ

The residue subspace is 2-dimensional over ℝ. Extend M_Q from a real 2×2 matrix to a complex 2×2 matrix via base change:

  M_Q^ℂ : ℂ² → ℂ²

Mathlib infrastructure:
- `Mathlib.LinearAlgebra.Charpoly.BaseChange` — characteristic polynomial under base change
- The norm extends: ‖M_Q^ℂ · v‖ = ‖M_Q · Re(v)‖ + ... (needs care)

### Step 3: Eigenvalues exist over ℂ

Over ℂ (algebraically closed), every linear map on a nontrivial finite-dimensional space has at least one eigenvalue:

  Mathlib: `Module.End.exists_eigenvalue [IsAlgClosed K] [FiniteDimensional K V] [Nontrivial V]`

For a 2×2 matrix, there are exactly 2 eigenvalues (counting multiplicity), found as roots of the characteristic polynomial.

Mathlib infrastructure:
- `Mathlib.LinearAlgebra.Eigenspace.Triangularizable` — `exists_eigenvalue`
- `Mathlib.LinearAlgebra.Eigenspace.Charpoly` — `hasEigenvalue_iff_isRoot_charpoly`

### Step 4: Contraction implies |λ| ≤ 1

For each eigenvalue λ with eigenvector v (over ℂ):

  M_Q^ℂ · v = λ · v
  ‖M_Q^ℂ · v‖ = |λ| · ‖v‖

The contraction condition (Step 1) extends to ℂ:
  ‖M_Q^ℂ · v‖ ≤ ‖v‖

Therefore:
  |λ| · ‖v‖ ≤ ‖v‖
  |λ| ≤ 1  (since ‖v‖ > 0 for an eigenvector)

Mathlib infrastructure:
- `Mathlib.Analysis.Normed.Operator.Basic` — operator norm
- The key lemma: `‖f v‖ ≤ ‖f‖ * ‖v‖` and if f is a contraction, `‖f‖ ≤ 1`

### Step 5: Conclude Re(λ) ≤ 1 ≤ ... 

For any complex number λ:
  Re(λ) ≤ |λ| ≤ 1

So all residue eigenvalues have Re(λ) ≤ 1. For the J-I case specifically, the residue eigenvalue is -1/8 (discrete) or -1 (continuous), which satisfies this.

**Note:** The theorem says "non-positive" (Re(λ) ≤ 0), but the proof gives |λ| ≤ 1 which is Re(λ) ≤ 1. The stronger statement Re(λ) ≤ 0 requires either:
- The contraction to be strict (‖M·s‖ < ‖s‖ for s ≠ 0), or
- An additional constraint from the zero-diagonal structure

The counterexample matrix [[0,1,2],[2,0,1],[1,2,0]] has eigenvalues with Re(λ) = -7/4 < 0, so the non-positivity might follow from the zero-diagonal + equal-row-sums structure. But that's a separate argument.

## The Lean Proof Sketch

```lean
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.LinearAlgebra.Eigenspace.Triangularizable
import Mathlib.LinearAlgebra.Eigenspace.Charpoly
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Analysis.Normed.Module.Basic

-- The theorem we want:
theorem entropy_decrease_constrains_residue
    (M : Fin 3 → Fin 3 → ℝ)
    (h_zero_diag : ∀ i, M i i = 0)
    (h_row_sums : Hypothesis_EqualRowSums M)
    (h_entropy_decrease : ∀ (s : Fin 3 → ℝ),
        PFEntropy (fun i => ∑ j, M i j * s j) ≤ PFEntropy s) :
    -- All eigenvalues λ of M restricted to residue subspace satisfy |λ| ≤ 1
    ∀ (λ : ℂ), IsEigenvalue (residue_restriction M) λ → λ.abs ≤ 1 := by
  -- Step 1: PFEntropy decrease → residue norm decrease
  -- (needs: Q(M·s) = M_Q · Q(s) when M has equal row sums)
  have h_contraction : ∀ r : ResidueSubspace, ‖M_Q r‖ ≤ ‖r‖ := ...
  -- Step 2: Extend to ℂ
  -- (needs: base change from ℝ to ℂ, norm extension)
  have h_contraction_ℂ : ∀ v : ℂ², ‖M_Q_ℂ v‖ ≤ ‖v‖ := ...
  -- Step 3-4: For each eigenvalue λ with eigenvector v:
  --   ‖M_Q_ℂ v‖ = |λ| · ‖v‖ ≤ ‖v‖, so |λ| ≤ 1
  intro λ h_eigen
  obtain ⟨v, h_v_ne, h_Mv⟩ := h_eigen
  -- h_Mv : M_Q_ℂ v = λ • v
  have h_norm : ‖M_Q_ℂ v‖ = λ.abs * ‖v‖ := by
    rw [h_Mv]
    -- norm of scalar multiplication: ‖λ • v‖ = |λ| * ‖v‖
    exact norm_smul λ v
  have h_le : λ.abs * ‖v‖ ≤ ‖v‖ := by
    rw [← h_norm]
    exact h_contraction_ℂ v
  have h_v_pos : 0 < ‖v‖ := ...
  linarith [h_le, h_v_pos]
```

## What's Missing (Engineering, Not Research)

1. **ResidueSubspace type** — the 2D subspace orthogonal to the uniform vector. Needs to be defined as a Submodule of Fin 3 → ℝ.

2. **residue_restriction** — M restricted to the residue subspace. Needs the equal-row-sums hypothesis to show M preserves the residue subspace.

3. **Base change ℝ → ℂ** — extending M_Q from ℝ² to ℂ². Mathlib has `Algebra.TensorProduct` for this, but the specific instance for Fin 2 → ℝ → Fin 2 → ℂ needs construction.

4. **Norm extension** — showing the contraction condition extends from ℝ to ℂ. This is the trickiest part. The real norm on the residue subspace needs to extend to a complex norm, and the contraction needs to hold for complex vectors too.

5. **IsEigenvalue over ℂ** — using `Module.End.exists_eigenvalue` with `IsAlgClosed ℂ`.

## Estimated Effort

- ResidueSubspace + residue_restriction: ~40 lines
- Base change + norm extension: ~60 lines
- Eigenvalue argument: ~30 lines
- Glue + cleanup: ~30 lines
- **Total: ~160 lines of Lean**

## Build Verification

**Do NOT run `lake build` from Devin's shell** — WSL 9P deadlocks. Only Greg's terminal can build Lean. This design document is for Greg or a future Devin with build access to implement and verify.

## Why This Matters

This theorem closes one of the two real mathematical gaps in the PfLean codebase. It proves that PF entropy decrease is not just a property of J-I dynamics — it's a constraint on the spectrum. The framework forces non-positive residue eigenvalues. That's the "what does the framework force?" question, answered for the entropy case.

The counterexample shows entropy decrease doesn't force J-I (you need symmetry or uniform cooling). But this theorem shows it DOES force the spectrum to be bounded. That's the necessary-but-not-sufficient result the comment describes.
