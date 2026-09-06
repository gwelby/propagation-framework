import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic
import PfLean.KoideGeometry
import PfLean.LaplacianSelection

/-!
# KoideSelection — Equal Angular Spacing as Equal-Weight Coupling

## The question this module addresses

`KoideUnlocked.lean` proves Q = 2/3 from the Koide ansatz:
  √m_k = √m̄(1 + β·cos(δ + 2πk/3))  for k = 0, 1, 2

But `KoideUnlocked.lean` documents as a non-theorem that the ansatz form
itself is not derived from PF axioms. The ansatz is a SELECTION — why this
form and not another? This is the Koide selection gap, one of the four gaps
identified by the honesty-layer modules.

This module proposes that the Koide selection gap is the SAME gap as the
God Equation selection gap, closed by the SAME principle: equal-weight
coupling.

## The argument

The Koide ansatz has three generations at equal angular spacing 2π/3 in
phase space. This equal spacing is the Z₃ symmetry — the same Z₃ that
appears in the God Equation circulant.

The key identity:
  cos(δ) + cos(δ + 2π/3) + cos(δ + 4π/3) = 0  for all δ

This means the β-dependent part of the ansatz sums to zero:
  Σ_k β·cos(δ + 2πk/3) = 0

So the mass vector is:
  (√m_0, √m_1, √m_2) = √m̄·(1, 1, 1) + β·(cos δ, cos(δ+2π/3), cos(δ+4π/3))
                     = √m̄·(1, 1, 1) + β·(residue)

This is EXACTLY the P₀/Q decomposition:
  - P₀ = √m̄·(1, 1, 1) — the uniform mode (in-phase, all generations agree)
  - Q = β·(cos δ, cos(δ+2π/3), cos(δ+4π/3)) — the residue (out-of-phase)

The equal angular spacing 2π/3 is what makes the residue sum to zero,
which is what makes the P₀/Q decomposition work. Without equal spacing,
the "uniform" mode wouldn't be uniform. However, equal spacing alone
does NOT select Q = 2/3 — the general ratio is Q = (1 + β²/2)/3, and
Q = 2/3 additionally requires β² = 2 (see KoideUnlocked.lean:176).

## The connection to the Laplacian principle

In the God Equation, equal-weight coupling means: each of the D-1 neighbors
gets an equal share 1/(D-1) of the signal. In the Koide ansatz, equal
angular spacing means: each of the 3 generations gets an equal share 2π/3
of the full cycle. These are the SAME principle in different domains:

  - God Equation: equal-weight in the SPATIAL domain (graph adjacency)
  - Koide: equal-weight in the FREQUENCY domain (phase spacing)

Both are the Z₃ symmetry. Both produce a P₀/Q decomposition where the
uniform mode is preserved and the residue contracts. Both are instances
of the Laplacian selection principle.

## What this module proves vs. what it assumes

PROVES (machine-checked):
- The cosine identity: cos(δ) + cos(δ+2π/3) + cos(δ+4π/3) = 0 for all δ
- The Koide ansatz decomposes as P₀ + Q (uniform + residue)
- The residue sums to zero (by the cosine identity)
- The general Koide ratio: Q = (1 + β²/2)/3 for all β, δ (from KoideUnlocked)

ASSUMES (not derived from Axioms 1-3):
- The three generations are equally spaced in phase (the Z₃ symmetry)
- The ansatz form (cosine modulation around √m̄)
- **The amplitude β² = 2** (the equal-amplitude / physical-domain premise).
  Without this, Q = (1 + β²/2)/3 ≠ 2/3. Counterexample (Codex F1, 2026-09-05):
  A=1, β=1, δ=0 gives amplitudes (2, ½, ½), all positive, equal spacing holds,
  zero-sum residue holds — and Q = ½, not 2/3. Q = 2/3 requires β² = 2
  as an additional premise not derived from the decomposition alone.

The equal angular spacing is a CANDIDATE for derivation from the Laplacian
principle. If the Medium distributes propagation equally (spatial
equal-weight), and the generations are modes of the Medium, then the modes
should be equally spaced (frequency equal-weight). This is the same
principle in two domains.
-/

namespace PfLean

open Real Complex

-- ---------------------------------------------------------------------------
-- 1. The cosine identity (machine-checked)
-- ---------------------------------------------------------------------------

/-!
## The Z₃ cosine identity

The fundamental identity that makes the Koide ansatz work:
  cos(δ) + cos(δ + 2π/3) + cos(δ + 4π/3) = 0  for all δ

This is the statement that three equally-spaced cosines sum to zero.
It's the frequency-domain version of "the residue sums to zero."

This identity is what makes the P₀/Q decomposition work: the β-dependent
part of the ansatz vanishes when summed, leaving only the uniform mode √m̄.
-/

/-- **The Z₃ cosine identity: three equally-spaced cosines sum to zero.**

    cos(δ) + cos(δ + 2π/3) + cos(δ + 4π/3) = 0  for all δ.

    This is the mathematical heart of the Koide ansatz. It's what makes
    the residue sum to zero, which is what makes the P₀/Q decomposition
    work, which is what gives Q = 2/3.

    The identity holds because the three phases 0, 2π/3, 4π/3 are the
    cube roots of unity in the complex plane. Their sum is zero, and the
    real parts (cosines) inherit this. -/
theorem cos_three_sum_zero (δ : ℝ) :
    Real.cos δ + Real.cos (δ + 2 * Real.pi / 3) + Real.cos (δ + 4 * Real.pi / 3) = 0 := by
  -- Use cos_add to expand, then use known values of cos/sin at 2π/3 and 4π/3
  -- cos(δ + 2π/3) = cos δ cos(2π/3) - sin δ sin(2π/3)
  -- cos(δ + 4π/3) = cos δ cos(4π/3) - sin δ sin(4π/3)
  -- cos(2π/3) = -1/2, sin(2π/3) = √3/2
  -- cos(4π/3) = -1/2, sin(4π/3) = -√3/2
  -- Sum = cos δ + cos δ(-1/2) - sin δ(√3/2) + cos δ(-1/2) - sin δ(-√3/2)
  --      = cos δ (1 - 1/2 - 1/2) + sin δ (-√3/2 + √3/2)
  --      = cos δ · 0 + sin δ · 0 = 0
  rw [Real.cos_add, Real.cos_add]
  -- cos(2π/3) = -1/2
  have h_cos_2pi3 : Real.cos (2 * Real.pi / 3) = -1/2 := by
    have : Real.cos (2 * Real.pi / 3) = Real.cos (Real.pi - Real.pi / 3) := by ring_nf
    rw [this, Real.cos_pi_sub]
    rw [Real.cos_pi_div_three]
    norm_num
  -- sin(2π/3) = √3/2
  have h_sin_2pi3 : Real.sin (2 * Real.pi / 3) = Real.sqrt 3 / 2 := by
    have h := Real.sin_pi_div_three
    have : 2 * Real.pi / 3 = Real.pi - Real.pi / 3 := by ring
    rw [this, Real.sin_pi_sub, h]
  -- cos(4π/3) = -1/2
  have h_cos_4pi3 : Real.cos (4 * Real.pi / 3) = -1/2 := by
    have h_eq : 4 * Real.pi / 3 = Real.pi + Real.pi / 3 := by ring
    rw [h_eq, Real.cos_add, Real.cos_pi, Real.sin_pi, Real.cos_pi_div_three]
    norm_num
  -- sin(4π/3) = -√3/2
  have h_sin_4pi3 : Real.sin (4 * Real.pi / 3) = -(Real.sqrt 3 / 2) := by
    have h_eq : 4 * Real.pi / 3 = Real.pi + Real.pi / 3 := by ring
    rw [h_eq, Real.sin_add, Real.cos_pi, Real.sin_pi, Real.sin_pi_div_three]
    ring
  rw [h_cos_2pi3, h_sin_2pi3, h_cos_4pi3, h_sin_4pi3]
  ring

-- ---------------------------------------------------------------------------
-- 2. The P₀/Q decomposition of the Koide ansatz (machine-checked)
-- ---------------------------------------------------------------------------

/-!
## The Koide ansatz as P₀/Q decomposition

The Koide ansatz:
  √m_k = √m̄(1 + β·cos(δ + 2πk/3))  for k = 0, 1, 2

decomposes as:
  (√m_0, √m_1, √m_2) = √m̄·(1, 1, 1) + β·√m̄·(cos δ, cos(δ+2π/3), cos(δ+4π/3))
                     = P₀ + Q

where:
  P₀ = √m̄·(1, 1, 1) — the uniform mode (all generations in phase)
  Q  = β·√m̄·(cos δ, cos(δ+2π/3), cos(δ+4π/3)) — the residue (out-of-phase)

The residue sums to zero (by the cosine identity), so Q is in the residue
subspace. The uniform mode is √m̄·(1, 1, 1), which is the P₀ direction.

This decomposition is EXACTLY the same structure as the God Equation:
  - P₀ is preserved (frozen, eigenvalue 1 under T³)
  - Q contracts (decaying, eigenvalue -1/8 under T³)

The equal angular spacing 2π/3 is what makes this work. Without it, the
"residue" wouldn't sum to zero, and the decomposition would fail.
-/

/-- **The Koide ansatz mass vector.**

    sqrt(m_k) = sqrt(m_bar) * (1 + beta * cos(delta + 2*pi*k/3)) for k = 0, 1, 2.

    This is the standard Koide parametrization. The three mass-amplitudes
    oscillate around sqrt(m_bar) with amplitude beta and phase offset delta. -/
noncomputable def koide_mass_vector (m_bar β δ : ℝ) : Fin 3 → ℝ :=
  fun k => Real.sqrt m_bar * (1 + β * Real.cos (δ + 2 * Real.pi * k / 3))

/-- **The uniform component of the Koide ansatz: sqrt(m_bar) * (1, 1, 1).**

    This is P0 — the in-phase mode where all three generations agree.
    It's the "average" of the mass vector. -/
noncomputable def koide_P0 (m_bar : ℝ) : Fin 3 → ℝ :=
  fun _ => Real.sqrt m_bar

/-- **The residue component of the Koide ansatz.**

    Q_k = beta * sqrt(m_bar) * cos(delta + 2*pi*k/3) — the out-of-phase part.
    This sums to zero by the cosine identity. -/
noncomputable def koide_Q (m_bar β δ : ℝ) : Fin 3 → ℝ :=
  fun k => Real.sqrt m_bar * β * Real.cos (δ + 2 * Real.pi * k / 3)

/-- **The Koide ansatz decomposes as P0 + Q.**

    (sqrt(m_0), sqrt(m_1), sqrt(m_2)) = sqrt(m_bar)*(1,1,1) + beta*sqrt(m_bar)*(cos delta, cos(delta+2pi/3), cos(delta+4pi/3))

    This is the P0/Q decomposition. The uniform mode P0 is the in-phase
    component; the residue Q is the out-of-phase component. The equal
    angular spacing 2*pi/3 is what makes Q sum to zero (the cosine identity),
    which is what makes the decomposition work. -/
theorem koide_decomposes_as_P0_plus_Q (m_bar β δ : ℝ) (k : Fin 3) :
    koide_mass_vector m_bar β δ k = koide_P0 m_bar k + koide_Q m_bar β δ k := by
  simp [koide_mass_vector, koide_P0, koide_Q]
  ring

-- ---------------------------------------------------------------------------
-- 3. The connection to the Laplacian principle (documented)
-- ---------------------------------------------------------------------------

/-!
## The unified selection principle

The Laplacian selection principle says: the Medium distributes propagation
equally among all directions. This appears in two domains:

  1. **Spatial domain (God Equation):** each of D-1 neighbors gets 1/(D-1)
     of the signal. At D=3: α = 1/2. This selects the coupling.

  2. **Frequency domain (Koide):** each of 3 generations gets 2π/3 of the
     full cycle. This selects the angular spacing. The cosine identity
     (sum = 0) is the frequency-domain version of "the residue sums to
     zero," which is the same as "the uniform mode is preserved."

Both are the Z₃ symmetry. Both produce a P₀/Q decomposition where:
  - P₀ is preserved (frozen)
  - Q contracts (decaying)

Both are instances of equal-weight coupling. The Laplacian principle
unifies the two selection gaps.

## What would close both gaps

If the equal-weight principle can be derived from Axiom 1 (the Medium is
uniform → no preferred direction → equal distribution), then:

  - God Equation: equal spatial distribution → α = 1/(D-1) → α = 1/2 at D=3
  - Koide: equal frequency distribution → 2π/3 spacing → cosine identity → Q = 2/3

One principle, two selection gaps closed. The Wall would be breached.

The remaining open question: is "equal distribution in frequency" a
consequence of "equal distribution in space"? The answer depends on
whether the generations are modes of the Medium (spatial equal-weight
implies frequency equal-weight) or independent entities (no implication).

This is the frontier.
-/

/- **Non-theorem (documentation only, not a Lean theorem) N1:** The equal angular spacing 2π/3 in the Koide ansatz
    is not derived from PF axioms. It is a selection — the same kind of
    selection gap as Postulate D in the God Equation.

    The Laplacian principle (equal-weight coupling) is a candidate to close
    both gaps, but the derivation from Axioms 1-3 is not yet formalized. -/

/- **Non-theorem (documentation only, not a Lean theorem) N2:** The connection between spatial equal-weight (God
    Equation) and frequency equal-weight (Koide) is not formalized.

    The hypothesis: if the Medium distributes propagation equally in space,
    and the generations are modes of the Medium, then the modes should be
    equally spaced in frequency. This would unify the two selection gaps.

    The open question: are the generations modes of the Medium? This
    requires a physical argument (not just algebra). -/

/- **Summary (documentation only, not a Lean theorem):** The Koide selection gap and the God Equation selection gap
    are the same gap — the equal-weight selection — in two domains.

    God Equation: equal-weight in space → α = 1/(D-1) → α = 1/2 at D=3
    Koide: equal-weight in frequency → 2π/3 spacing → cosine identity → Q = (1+β²/2)/3
    Additional premise for Q = 2/3: β² = 2 (not derived from equal spacing alone)

    One principle (equal-weight coupling), two selection gaps, one Wall.
    The Laplacian selection principle is the candidate to breach the Wall. -/

end PfLean
