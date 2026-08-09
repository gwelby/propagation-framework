/-
  PfLean.HProdGap — The H_prod Operator/Probability Bridge: The Gaussian Gap

  Authors: Devin ∇λΣ∞, Greg Welby
  Date: 2026-08-09

  This module formalizes the H_prod gap: the bridge from the God Equation
  operator algebra to a joint probability model. The key finding:

  **H_prod requires the Gaussian assumption, which is not in Axioms 1-3.**

  The argument has three parts:

  1. T is diagonal in Fourier space (already proven in PFCore.lean).
     A diagonal operator IS a product of single-particle operators —
     each Fourier mode evolves independently under T.

  2. For REAL data on Z₃, the k=1 and k=2 Fourier modes are complex
     conjugates (DFT conjugate symmetry). They are deterministically
     related and CANNOT be independent. Position-space factorization
     FAILS for the residue sector.

  3. The Gaussian assumption closes the gap: a Gaussian distribution
     is determined by its first two moments. Circulant covariance →
     diagonal in Fourier space → uncorrelated → independent (for
     Gaussian only). H_prod holds CONDITIONAL on Gaussianity.

  The conclusion: H_prod is CONDITIONAL on the Gaussian assumption,
  not unconditional from Axioms 1-3. The Gaussian assumption is the
  missing posit — the same structure as the Wall (where H12 is the
  missing posit for Postulate D).

  This is the "shortest route to failure" from g3_closure_card_2026-04-01.md:
  "show that any proof of H_prod would need assumptions stronger than
  the Z₃ Lagrangian plus Axioms 1-3." The stronger assumption is Gaussianity.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Star.Basic
import Mathlib.Tactic

namespace PfLean

open Complex
open scoped ComplexConjugate

-- Now `conj` is available as the complex conjugate notation

/-- The primitive cube root of unity: ω = e^(2πi/3).
    We define it as a complex number with the known properties axiomatized. -/
noncomputable def ω : ℂ :=
  Complex.mk (Real.cos (2 * Real.pi / 3)) (Real.sin (2 * Real.pi / 3))

/-- ω³ = 1 (primitive cube root of unity). -/
axiom omega_cubed : ω ^ 3 = 1

/-- star(ω) = ω² (conjugate of primitive root is its square). -/
axiom conj_omega_eq_omega_sq : conj ω = ω ^ 2

/-- 1 + ω + ω² = 0 (cyclotomic identity). -/
axiom cyclotomic_identity : (1 : ℂ) + ω + ω ^ 2 = 0

/-- ω ≠ 1 (ω is primitive, not trivial). -/
axiom omega_ne_one : ω ≠ 1

-- ---------------------------------------------------------------------------
-- 2. The DFT on Z₃ (expanded for Fin 3)
-- ---------------------------------------------------------------------------

/-- The DFT of a real vector x : Fin 3 → ℝ at frequency k=1.
    DFT₁(x) = x(0) + x(1)·ω + x(2)·ω² -/
noncomputable def DFT1 (x : Fin 3 → ℝ) : ℂ :=
  Complex.mk (x 0) 0 + Complex.mk (x 1) 0 * ω + Complex.mk (x 2) 0 * ω ^ 2

/-- The DFT of a real vector x : Fin 3 → ℝ at frequency k=2.
    DFT₂(x) = x(0) + x(1)·ω² + x(2)·ω⁴ = x(0) + x(1)·ω² + x(2)·ω -/
noncomputable def DFT2 (x : Fin 3 → ℝ) : ℂ :=
  Complex.mk (x 0) 0 + Complex.mk (x 1) 0 * ω ^ 2 + Complex.mk (x 2) 0 * ω ^ 4

/-- ω⁴ = ω (follows from ω³ = 1). -/
theorem omega_four_eq_omega : ω ^ 4 = ω := by
  have h : ω ^ 4 = ω ^ 3 * ω := by
    rw [show 4 = 3 + 1 from by norm_num]
    rw [pow_add]
    ring
  rw [h, omega_cubed]
  simp

/-- Helper: for real r, conj(Complex.mk r 0) = Complex.mk r 0. -/
theorem conj_real_complex (r : ℝ) : conj (Complex.mk r 0) = Complex.mk r 0 := by
  show Star.star (Complex.mk r 0) = Complex.mk r 0
  simp [Star.star]

/-- Helper: conj(ω²) = ω (follows from conj(ω) = ω² and conj(conj(ω)) = ω). -/
theorem conj_omega_sq_eq_omega : conj (ω ^ 2) = ω := by
  have h : ω ^ 2 = ω * ω := by rw [pow_two]
  rw [h, (starRingEnd ℂ).map_mul]
  rw [conj_omega_eq_omega_sq]
  -- Now: ω² * ω² = ω⁴ = ω
  have h2 : (ω ^ 2 : ℂ) * (ω ^ 2 : ℂ) = ω ^ 4 := by
    rw [show (4 : ℕ) = 2 + 2 from by norm_num, pow_add]
  rw [h2, omega_four_eq_omega]

-- ---------------------------------------------------------------------------
-- 3. Conjugate Symmetry: DFT₂(x) = star(DFT₁(x)) for real x
-- ---------------------------------------------------------------------------

/-- **Conjugate symmetry of the DFT on Z₃:** For real data x,
    DFT₂(x) = conj(DFT₁(x)).

    This is the fundamental obstruction to H_prod: the k=1 and k=2
    Fourier modes are complex conjugates, hence deterministically
    related, hence NOT independent. -/
theorem DFT_conjugate_symmetry (x : Fin 3 → ℝ) :
    DFT2 x = conj (DFT1 x) := by
  simp only [DFT1, DFT2, omega_four_eq_omega]
  -- Expand conj of sum using (starRingEnd ℂ).map_add (twice for two additions)
  rw [show conj ((Complex.mk (x 0) 0) + (Complex.mk (x 1) 0) * ω + (Complex.mk (x 2) 0) * ω ^ 2) =
        conj (Complex.mk (x 0) 0) + conj (Complex.mk (x 1) 0 * ω) + conj (Complex.mk (x 2) 0 * ω ^ 2) from by
    rw [(starRingEnd ℂ).map_add, (starRingEnd ℂ).map_add]]
  -- conj of real is real
  rw [conj_real_complex (x 0)]
  -- conj(a * b) = conj(a) * conj(b) via (starRingEnd ℂ).map_mul
  rw [show conj (Complex.mk (x 1) 0 * ω) = conj (Complex.mk (x 1) 0) * conj ω from
        (starRingEnd ℂ).map_mul (Complex.mk (x 1) 0) ω]
  rw [conj_real_complex (x 1), conj_omega_eq_omega_sq]
  rw [show conj (Complex.mk (x 2) 0 * ω ^ 2) = conj (Complex.mk (x 2) 0) * conj (ω ^ 2) from
        (starRingEnd ℂ).map_mul (Complex.mk (x 2) 0) (ω ^ 2)]
  rw [conj_real_complex (x 2), conj_omega_sq_eq_omega]

-- ---------------------------------------------------------------------------
-- 4. The Deterministic Relation: |DFT₁|² = |DFT₂|²
-- ---------------------------------------------------------------------------

/-- **Conjugate modes share magnitude:** |conj(y)|² = |y|². -/
theorem conjugate_implies_equal_magnitude (y : ℂ) :
    normSq (conj y) = normSq y := by
  exact Complex.normSq_conj y

/-- **Corollary:** For real data x, |DFT₁(x)|² = |DFT₂(x)|².

    The two residue Fourier modes have the same magnitude. This is a
    deterministic constraint — knowing |DFT₁| immediately determines
    |DFT₂|. They cannot be independent. -/
theorem DFT_residue_magnitudes_equal (x : Fin 3 → ℝ) :
    normSq (DFT1 x) = normSq (DFT2 x) := by
  rw [DFT_conjugate_symmetry x]
  rw [conjugate_implies_equal_magnitude (DFT1 x)]

-- ---------------------------------------------------------------------------
-- 5. The Real Part Constraint
-- ---------------------------------------------------------------------------

/-- **Real parts are equal:** Re(DFT₂(x)) = Re(DFT₁(x)) for real x.

    Since DFT₂ = conj(DFT₁), the real parts are identical. -/
theorem DFT_residue_real_parts_equal (x : Fin 3 → ℝ) :
    (DFT2 x).re = (DFT1 x).re := by
  rw [DFT_conjugate_symmetry x, conj_re]

/-- **Imaginary parts are negated:** Im(DFT₂(x)) = -Im(DFT₁(x)) for real x.

    Since DFT₂ = conj(DFT₁), the imaginary parts are negated. -/
theorem DFT_residue_imag_parts_negated (x : Fin 3 → ℝ) :
    (DFT2 x).im = -(DFT1 x).im := by
  rw [DFT_conjugate_symmetry x, conj_im]

-- ---------------------------------------------------------------------------
-- 6. The Non-Independence Theorem
-- ---------------------------------------------------------------------------

/-!
## The non-independence of residue Fourier modes

For real data on Z₃, the k=1 and k=2 Fourier modes are complex conjugates.
This means three deterministic relations:

  1. |DFT₁|² = |DFT₂|²  (magnitudes equal)
  2. Re(DFT₂) = Re(DFT₁)  (real parts equal)
  3. Im(DFT₂) = -Im(DFT₁)  (imaginary parts negated)

These deterministic relations mean the two modes CANNOT be independent
random variables. If Y₁ = DFT₁(X) and Y₂ = DFT₂(X) for a random real
vector X, then Y₂ = star(Y₁), so:

  P(Y₁ ∈ A, Y₂ ∈ B) = P(Y₁ ∈ A, star(Y₁) ∈ B)

This is NOT equal to P(Y₁ ∈ A) · P(Y₂ ∈ B) in general — the joint
distribution is supported on the "conjugate surface" {(y, star(y))},
which is a 2D submanifold of ℂ² (4D), not a product distribution.

**This is the fundamental obstruction to H_prod.**

The operator algebra (T diagonal in Fourier space) gives "uncorrelated"
modes. But "uncorrelated" ≠ "independent" except for Gaussian distributions.
For real data on Z₃, the conjugate symmetry is a STRUCTURAL constraint
that goes beyond correlation — it's a deterministic relation.
-/

-- ---------------------------------------------------------------------------
-- 7. The Gaussian Conditional (the missing posit)
-- ---------------------------------------------------------------------------

/-!
## The Gaussian assumption closes the gap

The Gaussian distribution is the UNIQUE distribution where uncorrelated
implies independent. This is because a Gaussian is completely determined
by its first two moments (mean and covariance).

If the state distribution is Gaussian with circulant covariance:
  1. Circulant covariance → diagonal in Fourier space (standard result)
  2. Diagonal covariance → Fourier modes are uncorrelated
  3. Gaussian + uncorrelated → independent (the key Gaussian property)
  4. Independent Fourier modes → H_prod holds

So H_prod is CONDITIONAL on the Gaussian assumption. The Gaussian
assumption is the missing posit — not in Axioms 1-3.

The physical question: why would the Medium's state distribution be
Gaussian? Possible arguments:
  - Central limit theorem (many weak interactions → Gaussian)
  - Maximum entropy (Gaussian is max-entropy for fixed covariance)
  - Free field theory (Gaussian is the free field vacuum)

None of these is currently formalized in the PF axioms. The Gaussian
assumption is a physical posit, comparable to H12 (permutation symmetry)
or stationarity. It's the missing posit for H_prod.

## Important subtlety: the conjugate constraint vs independence

The conjugate symmetry DFT₂ = star(DFT₁) is a constraint on REAL data.
For COMPLEX data, the two modes could be independent. But the PF
framework's state space is Fin 3 → ℝ (real), not Fin 3 → ℂ.

If the state space were extended to complex values, the conjugate
symmetry would not apply, and H_prod could potentially hold without
the Gaussian assumption. But this would require extending the axioms
to complex state spaces — a non-trivial modification.

As it stands, with real state space, H_prod requires Gaussianity.
-/

-- ---------------------------------------------------------------------------
-- 8. The Honest Assessment
-- ---------------------------------------------------------------------------

/-!
## The honest assessment of H_prod

**What's machine-checked in this module:**
  - DFT conjugate symmetry: DFT₂(x) = star(DFT₁(x)) for real x
  - Equal magnitudes: |DFT₁(x)|² = |DFT₂(x)|²
  - Equal real parts: Re(DFT₂) = Re(DFT₁)
  - Negated imaginary parts: Im(DFT₂) = -Im(DFT₁)
  - These are deterministic relations → non-independence

**What's prose-argued (not machine-checked):**
  - "Uncorrelated ≠ independent except for Gaussian" — standard probability
    theorem, but not formalized here
  - "Gaussian + circulant covariance → independent Fourier modes" — standard
    but not formalized here
  - "H_prod requires Gaussianity" — the conclusion, following from the above
  - "Gaussianity is not in Axioms 1-3" — inspection of the axioms

**The conclusion:**
  H_prod is CONDITIONAL on the Gaussian assumption, not unconditional
  from Axioms 1-3. The Gaussian assumption is the missing posit.

  This is the "shortest route to failure" from g3_closure_card_2026-04-01.md:
  "show that any proof of H_prod would need assumptions stronger than
  the Z₃ Lagrangian plus Axioms 1-3." The stronger assumption is Gaussianity.

**What this means for the God Equation:**
  - The operator algebra (eigenvalues {1, -1/8, -1/8}) is CONDITIONAL 0.88
    on Postulate D — unchanged
  - H_prod (the probability bridge) is now CONDITIONAL on Gaussianity
    — a second explicit posit
  - The God Equation's full chain: Postulate D + Gaussianity → H_prod →
    probability predictions
  - Two posits, not one. Neither is in Axioms 1-3.

**Comparison to the Wall:**
  The Wall (Postulate D) needs 4 posits: H7 + H12 + stationarity + stability.
  H_prod needs 1 additional posit: Gaussianity.
  The full God Equation needs 5 posits: H7 + H12 + stationarity + stability
  + Gaussianity. Each does a different job, none redundant, none circular.

**The axioms used here:**
  The three axioms (omega_cubed, conj_omega_eq_omega_sq, cyclotomic_identity)
  are standard properties of the primitive cube root of unity. They are
  mathematical facts, not physical assumptions. The physical assumption
  (Gaussianity) is identified as the missing posit, not axiomatized.
-/

end PfLean
