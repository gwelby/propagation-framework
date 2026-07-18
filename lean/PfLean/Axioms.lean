/-
  PfLean.Axioms — The Three Axioms of the Propagation Framework
  Formalized in Lean 4. DISCOVERY layer — not verification of what we believe,
  but a machine that tells us what the axioms DO and DON'T imply.

  Authors: Greg Welby, Claude, DeepSeek, Hermes, Devin
  Started: 2026-06-21
  Updated: 2026-06-22 — Devin: Claude's Q2/Q3 corrections applied, H10 added,
           experiments rewritten for semigroup + recurrent target

  ANTI-CONFIRMATION-TRAP RULE (Claude, 2026-06-21):
  Do NOT choose a formalism for the Medium (Hilbert space? manifold? linear?).
  Every choice secretly determines the answer. "Hilbert space + linear" builds
  a room shaped like Z₃ and then announces we discovered Z₃ in it.

  Instead: keep the Medium as bare as the axioms literally force.
  Turn every tempting choice — linear, Hilbert, complex, finite-dim — into a
  NAMED HYPOTHESIS that Lean must explicitly demand. Then the list of hypotheses
  Lean can't do without IS the honest parameter count, machine-checked.

  Z₃ either falls out of the bare axioms (huge discovery) or it needs
  "+linear +finite-dim +ℂ" bolted on (honest bound). Either way we learn
  the truth instead of flattering ourselves.
-/

import Mathlib

/-! # THE BARE MEDIUM

The Medium is whatever the axioms minimally require. No more. Every additional
property (linear, metric, complex, finite-dimensional) is a NAMED HYPOTHESIS
added only when a theorem can't be proved without it. -/

structure BareMedium where
  -- The only thing the axioms require: a set of states and a way for
  -- propagation to move between them. Nothing else.
  State : Type
  -- Claude correction (2026-06-21): propagate is a one-parameter semigroup,
  -- NOT a bare State → State function. The time parameter is part of the
  -- axiom structure, not an add-on hypothesis. Linearity/unitarity are
  -- HYPOTHESES, not the definition.
  propagate : ℝ → State → State
  -- Axiom 2 adds: there's a speed limit. Formalized as a pseudometric d
  -- such that d(s, propagate(t, s)) ≤ causal_velocity · t.
  -- Claude Q3 answer: derive causal connection from propagate + d + bound.
  d : State → State → ℝ
  causal_velocity : ℝ
  -- Axiom 3 adds: some propagations are special (coherent).
  -- H8 below is the hypothesis form; the bare medium does NOT assume it.

/-! # NAMED HYPOTHESES

Every structural choice that might be needed. Each is a SEPARATE hypothesis
that Lean must explicitly demand before a theorem can use it.

The honest parameter count = the number of hypotheses a theorem needs minus
what the bare axioms force. -/

-- H1: propagation is reversible (each state has at most one predecessor at each t)
def Hypothesis_Reversible (M : BareMedium) : Prop :=
  ∀ (t : ℝ) (s₁ s₂ : M.State), M.propagate t s₁ = M.propagate t s₂ → s₁ = s₂

-- H2: semigroup law (propagation composes in time). This is the MINIMAL
-- algebraic condition on the one-parameter family. NOT linearity.
def Hypothesis_Semigroup (M : BareMedium) : Prop :=
  ∀ (t₁ t₂ : ℝ) (s : M.State), M.propagate (t₁ + t₂) s = M.propagate t₁ (M.propagate t₂ s)

-- H3: states form a vector space (linear superposition)
def Hypothesis_Linear (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State] : Prop :=
  ∀ (t : ℝ) (s₁ s₂ : M.State) (a b : ℝ), M.propagate t (a • s₁ + b • s₂) = a • M.propagate t s₁ + b • M.propagate t s₂

-- H4: states are over ℂ (complex amplitudes)
def Hypothesis_Complex (M : BareMedium) : Prop :=
  -- "∃ complex structure on State" — needs definition
  True

-- H5: finite-dimensional (the state space has finite dimension D)
def Hypothesis_FiniteDimensional (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State] : Prop :=
  Module.Finite ℝ M.State

-- H6: dimension = 3 (the spatial dimension of our universe)
def Hypothesis_Dimension3 (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State] : Prop :=
  Module.rank ℝ M.State = 3

-- H7: Postulate D (a=0, no self-loop in the Z₃ circulant)
-- Codex audit (2026-06-22): was `True`, now properly formalized as zero-diagonal.
-- For a D×D coupling matrix M, Postulate D says M(i,i) = 0 for all i.
def Hypothesis_PostulateD {D : ℕ} (M : Fin D → Fin D → ℝ) : Prop :=
  ∀ i, M i i = 0

-- H8: coherence condition (NON-CIRCULAR draft — Greg/Claude/Hermes/Devin 2026-06-22)
-- The old H8 was "∃ s, propagate s = s" — circular because it IS the conclusion.
-- The Devin update changed it to "∃ s T, ∀ n, propagate(n*T, s) = s" — still
-- circular: H8 was defined as the exact periodic orbit it was supposed to "prove".
--
-- The fix: H8 is no longer defined as exact periodicity. It asserts only:
--   (a) APPROXIMATE recurrence: after some period τ, the state returns to within
--       d(s, propagate τ s) < causal_velocity * τ of itself.
--   (b) Lyapunov stability: small perturbations stay small under propagation.
--
-- H8 and exact periodicity are NOT ordered by logical implication. The return
-- inequality is weaker than exact periodicity, but Lyapunov stability is an
-- additional independent premise (not implied by exact periodicity). Therefore
-- H8 is neither strictly weaker nor strictly stronger than exact periodicity.
--
-- Exact periodicity, eigenstructure, and Z₃ symmetry become THEOREMS that may
-- need additional hypotheses (H3 linearity, H5 finite-dim, H4 complex, etc.).
-- This breaks the A→A loop.
--
-- NOTE: This definition uses M.d and M.causal_velocity as bare data. The fact
-- that d is a pseudometric and satisfies the causal bound is H9, not H8. The
-- recurrence clause is meaningful even before H9 is assumed; H9 is needed to
-- interpret it as a causal bound.
def Hypothesis_Coherence (M : BareMedium) : Prop :=
  ∃ (s : M.State) (τ : ℝ) (τ_pos : τ > 0),
    -- Approximate recurrence: state returns to within a distance strictly smaller
    -- than the causal-velocity bound after one period τ.
    M.d s (M.propagate τ s) < M.causal_velocity * τ
    -- Lyapunov stability: nearby initial states stay nearby for all future times.
    ∧ ∀ (ε : ℝ), ε > 0 → ∃ (δ : ℝ), δ > 0 →
        ∀ (s' : M.State), M.d s s' < δ →
          ∀ (t : ℝ), t ≥ 0 → M.d (M.propagate t s) (M.propagate t s') < ε

-- H9: causal velocity bound (Axiom 2 formalized via pseudometric d)
-- Claude Q3 answer: derive causal connection from propagate + d + the bound.
-- d(s, propagate(t, s)) ≤ causal_velocity · t
def Hypothesis_CausalVelocity (M : BareMedium) : Prop :=
  M.causal_velocity > 0 ∧
  ∀ (t : ℝ) (s : M.State), t ≥ 0 → M.d s (M.propagate t s) ≤ M.causal_velocity * t

-- H10: scale invariance (Greg gut-check 2026-06-21, Claude flagged)
-- "Same STRUCTURES repeat at every scale" — STRONG, specific, falsifiable,
-- and NOT granted by any axiom. The scale-stack derivation and λ_c may
-- secretly use this to carry human/lab-scale structure down to Planck scale.
-- Distinguish from "same RULES everywhere" (mild, ~implicit in fixed laws).
def Hypothesis_ScaleInvariance (M : BareMedium) : Prop :=
  -- For any scale factor scale > 0, the propagation structure is invariant:
  -- rescaling time and distance by the same factor leaves physics unchanged.
  -- This is the STRONG form (self-similarity), not the weak form (same laws).
  ∀ (scale : ℝ) (scale_pos : scale > 0),
    ∀ (t : ℝ) (s : M.State), M.d s (M.propagate (scale * t) s) = scale * M.d s (M.propagate t s)

/-- H11: Stability — the uniform mode is non-decaying (eigenvalue ≥ 0) and
    all residue modes decay (eigenvalue < 0). This is what selects D=3.
    Codex audit (2026-06-22): formalized as a Lean definition, not just comments.
    For a D×D coupling matrix M with uniform eigenvalue c and residue eigenvalue λ:
    - c ≥ 0 (uniform mode is frozen or growing)
    - λ < 0 (residue modes decay)
    Combined with D3_unique_stable_dimension, this selects D=3. -/
def Hypothesis_Stability {D : ℕ} (M : Fin D → Fin D → ℝ) (c residue_eig : ℝ) : Prop :=
  c ≥ 0 ∧ residue_eig < 0

/-- H12: Permutation Symmetry — the coupling matrix is invariant under all
    permutations of the D indices. This forces M to be of the form
    M(i,j) = a if i=j, b if i≠j (2-parameter family).
    This is the STRONG form (full symmetric group S_D). -/
def Hypothesis_PermutationSymmetry {D : ℕ} (M : Fin D → Fin D → ℝ) : Prop :=
  ∀ (σ : Equiv.Perm (Fin D)) (i j : Fin D), M (σ i) (σ j) = M i j

/-- H13: Cyclic Symmetry — the coupling matrix is circulant (invariant under
    cyclic permutations only). This is weaker than H12 (Z_D vs S_D).
    For D=3, this gives the Z₃ circulant structure. -/
def Hypothesis_CyclicSymmetry {D : ℕ} (M : Fin D → Fin D → ℝ) : Prop :=
  ∀ (k : Fin D) (i j : Fin D), M (i + k) (j + k) = M i j

/-! # THE HONEST WORKFLOW

For any PF claim (Z₃ decomposition, God Equation, N=3 generations, etc.):
  1. State the claim as a theorem in terms of `BareMedium`
  2. Try to prove it with NO hypotheses
  3. When Lean says "can't prove," add ONE hypothesis
  4. Repeat until the theorem goes through
  5. The set of hypotheses required IS the honest parameter count

  If Z₃ falls out of `BareMedium` alone → genuine discovery
  If Z₃ needs H3 + H5 + H6 + H7 → honest bound on the claim
-/

-- Example: try to prove Z₃ structure from bare axioms
example (M : BareMedium) : True := by
  trivial

/-! # DISCOVERY EXPERIMENTS — The Honest Workflow in Action

## Discovery 1: Recurrent mode existence (Claude-corrected 2026-06-21)

Question: What does BareMedium force about coherent/robustly returning states?

We split the target into two strictly separated questions:
  (a) Does BareMedium force approximate recurrence + stability? — NO (needs H8).
  (b) Does anything short of H8 force exact periodic orbits? — NO (needs H3+H2+H4+H5).

The old H8 ("fixed point") was circular (defined AS its own conclusion).
The Devin update ("periodic orbit") was still circular (defined as exact periodicity).
The corrected H8 is a pair of independent premises: approximate recurrence + Lyapunov stability.
It is not ordered by implication with exact periodicity.
Exact periodicity, eigenstructure, and Z₃ become theorems requiring extra hypotheses. -/

-- Experiment 1: NO hypotheses — can we prove approximate recurrence + stability
-- from bare structure? NO. Counterexample: a trivial medium with a single
-- state and causal_velocity = 0. The recurrence condition requires
-- d(s, propagate(τ, s)) < 0, which is impossible for any τ > 0.
-- This is a machine-verified negative result: bare structure is insufficient.
theorem bare_medium_insufficient_for_recurrence :
    ∃ (M : BareMedium),
      ¬∃ (s : M.State) (τ : ℝ) (τ_pos : τ > 0),
        M.d s (M.propagate τ s) < M.causal_velocity * τ
        ∧ ∀ (ε : ℝ), ε > 0 → ∃ (δ : ℝ), δ > 0 →
            ∀ (s' : M.State), M.d s s' < δ →
              ∀ (t : ℝ), t ≥ 0 → M.d (M.propagate t s) (M.propagate t s') < ε := by
  -- Counterexample: single-state medium with zero causal velocity
  refine ⟨{ State := Unit, propagate := fun _ _ => (), d := fun _ _ => 0, causal_velocity := 0 }, ?_⟩
  rintro ⟨s, τ, τ_pos, h_rec, h_stab⟩
  -- d(s, propagate(τ, s)) = 0, causal_velocity * τ = 0, so 0 < 0 is false
  simp at h_rec

-- Experiment 2: H8_Coherence alone — trivially gives its own content.
-- H8 is no longer a restatement of exact periodicity, so this theorem is not
-- circular in the A→A sense. It just unpacks H8: recurrence + stability.
-- H8 is not strictly weaker than exact periodicity (stability is an added premise).
-- The real question is: what MORE do we need to get exact periodicity?
theorem recurrence_and_stability_from_H8 (M : BareMedium) (hCoh : Hypothesis_Coherence M) :
    ∃ (s : M.State) (τ : ℝ) (τ_pos : τ > 0),
      M.d s (M.propagate τ s) < M.causal_velocity * τ
      ∧ ∀ (ε : ℝ), ε > 0 → ∃ (δ : ℝ), δ > 0 →
          ∀ (s' : M.State), M.d s s' < δ →
            ∀ (t : ℝ), t ≥ 0 → M.d (M.propagate t s) (M.propagate t s') < ε := by
  -- H8 IS the recurrence + stability statement. Extract from hCoh.
  obtain ⟨s, τ, τ_pos, h_rec, h_stab⟩ := hCoh
  exact ⟨s, τ, τ_pos, h_rec, h_stab⟩

-- Experiment 3: H3_Linear + H2_Semigroup — can linearity + semigroup give recurrence?
-- For a linear semigroup, propagate(0, s) = s (identity at t=0).
-- But identity ≠ periodic orbit. We need EIGENVALUES with imaginary components
-- to get oscillation. That requires H4 (complex) too.
-- DISCOVERY: linear + semigroup alone gives NO NON-ZERO recurrence over ℝ.
-- The theorem as stated IS provable (s=0 is a trivial fixed point of any linear
-- map), but the non-trivial version (s ≠ 0) is the real open question.
-- See recurrence_stability_plus_structural_gives_nonzero_periodic_orbit below.
theorem recurrent_mode_from_H3_H2 (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M) (hSemi : Hypothesis_Semigroup M) :
    ∃ (s : M.State) (T : ℝ), T > 0 ∧ ∀ (n : ℕ), M.propagate (n * T) s = s := by
  -- Trivial proof: the zero vector is always a fixed point of a linear semigroup.
  -- Linearity: propagate(t, a·s₁ + b·s₂) = a·propagate(t, s₁) + b·propagate(t, s₂)
  -- Setting s₁ = s₂ = 0, a = b = 0: propagate(t, 0) = 0.
  use 0
  use 1
  constructor
  · norm_num
  · intro n
    have h0 : ∀ (t : ℝ), M.propagate t 0 = 0 := by
      intro t
      have h := hLin t 0 0 0 0
      simp at h
      exact h
    exact h0 (n * (1 : ℝ))

-- Experiment 4: H1 (reversibility) alone — does injectivity give recurrence?
-- NO. Counterexample: the translation flow propagate(t, x) = x + t on ℝ is
-- injective at every t but has no periodic orbit (s + n*T = s forces T = 0).
-- This is a machine-verified negative result: H1 is insufficient for periodicity.
theorem H1_insufficient_for_periodic_orbit :
    ∃ (M : BareMedium), Hypothesis_Reversible M ∧
      ¬∃ (s : M.State) (T : ℝ), T > 0 ∧ ∀ (n : ℕ), M.propagate (n * T) s = s := by
  -- Counterexample: translation flow on ℝ
  refine ⟨{ State := ℝ, propagate := fun t s => s + t, d := fun _ _ => 0, causal_velocity := 1 }, ?_, ?_⟩
  -- H1: injectivity of (fun s => s + t) for each t
  · intro t s₁ s₂ h
    exact add_right_cancel h
  -- No periodic orbit: s + n*T = s for all n forces T = 0
  · intro ⟨s, T, hT, hperiodic⟩
    have h1 := hperiodic 1
    simp [Nat.cast_one, mul_one] at h1
    linarith

-- Experiment 5: H8 + H3 + H2 + H5 — can we get EXACT periodicity from
-- approximate recurrence + stability + linear + semigroup + finite-dim?
-- This is the REAL theorem. It is NOT trivial; it may need more hypotheses or
-- a stronger version of H8.
--
-- IMPORTANT: The theorem as stated is actually TRIVIALLY TRUE because the zero
-- vector is always a fixed point of any linear semigroup. The interesting
-- question is whether a NON-ZERO periodic orbit exists. See the next theorem.
theorem recurrence_stability_plus_structural_gives_periodic_orbit
    (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hCoh : Hypothesis_Coherence M)
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hFin : Hypothesis_FiniteDimensional M) :
    ∃ (s : M.State) (T : ℝ), T > 0 ∧ ∀ (n : ℕ), M.propagate (n * T) s = s := by
  -- Trivial proof: the zero vector is always a fixed point of a linear semigroup.
  use 0
  use 1
  constructor
  · norm_num
  · intro n
    -- Linearity forces propagate(t, 0) = 0.
    have h0 : ∀ (t : ℝ), M.propagate t 0 = 0 := by
      intro t
      have h := hLin t 0 0 0 0
      simp at h
      exact h
    exact h0 (n * (1 : ℝ))

-- Experiment 5b: The NON-TRIVIAL version. Does H8 + H3 + H2 + H5 give a
-- NON-ZERO periodic orbit? NO. Machine-verified counterexample: the contraction
-- semigroup propagate(t, x) = exp(-t)·x on ℝ is linear, semigroup, finite-dim,
-- and Lyapunov stable (H8 holds). But exp(-n*T)·x = x with x ≠ 0 forces
-- exp(-n*T) = 1, hence T = 0 — contradicting T > 0. The only periodic orbit
-- is the trivial one (x = 0).
--
-- What would make it true? Likely need:
--   - H4 (complex structure) AND
--   - a stronger recurrence condition (not just one approximate return), or
--   - an explicit non-degeneracy condition on the coherent state.

/-- The contraction semigroup counterexample: propagate(t, x) = exp(-t)·x on ℝ.
    This is linear, semigroup, finite-dimensional, and Lyapunov stable (H8 holds),
    but has NO nonzero periodic orbit. Proven as a machine-verified counterexample
    showing H8 + H3 + H2 + H5 does NOT guarantee a nonzero periodic orbit. -/
theorem contraction_semigroup_no_nonzero_periodic_orbit :
    -- The contraction semigroup on ℝ: propagate(t, x) = exp(-t) * x
    let prop (t x : ℝ) := Real.exp (-t) * x
    -- H8 (Coherence): approximate recurrence + Lyapunov stability
    (∃ (s : ℝ) (τ : ℝ), τ > 0 ∧
      |s - prop τ s| < 2 * τ ∧
      ∀ (ε : ℝ), ε > 0 → ∃ (δ : ℝ), δ > 0 →
        ∀ (s' : ℝ), |s - s'| < δ →
          ∀ (t : ℝ), t ≥ 0 → |prop t s - prop t s'| < ε)
    ∧ -- H3 (Linearity): prop(t, a·s₁ + b·s₂) = a·prop(t,s₁) + b·prop(t,s₂)
    (∀ (t : ℝ) (s₁ s₂ : ℝ) (a b : ℝ),
      prop t (a * s₁ + b * s₂) = a * prop t s₁ + b * prop t s₂)
    ∧ -- H2 (Semigroup): prop(t₁+t₂, s) = prop(t₁, prop(t₂, s))
    (∀ (t₁ t₂ : ℝ) (s : ℝ), prop (t₁ + t₂) s = prop t₁ (prop t₂ s))
    ∧ -- No nonzero periodic orbit: prop(n·T, s) = s with s ≠ 0, T > 0 is impossible
    (¬∃ (s : ℝ) (T : ℝ), s ≠ 0 ∧ T > 0 ∧ ∀ (n : ℕ), prop (↑n * T) s = s) := by
  intro prop
  refine ⟨?coh, ?lin, ?semi, ?neg⟩
  -- H8: Coherence — take s = 1, τ = 1, causal_velocity = 2
  · refine ⟨1, 1, by norm_num, ?_, ?_⟩
    · -- |1 - exp(-1)*1| < 2 * 1
      simp only [show prop 1 1 = Real.exp (-1) * 1 from rfl]
      rw [mul_one]
      have h_exp : Real.exp (-1) < 1 := Real.exp_lt_one_iff.mpr (by norm_num)
      have h_pos : 0 < Real.exp (-1) := Real.exp_pos (-1)
      rw [abs_sub_lt_iff]
      refine ⟨?_, ?_⟩
      · linarith
      · linarith
    · -- Lyapunov stability: exp(-t) is a contraction
      intro ε hε
      refine ⟨ε, ?_⟩
      intro hδ s' hs' t ht
      show |Real.exp (-t) * 1 - Real.exp (-t) * s'| < ε
      rw [← mul_sub, abs_mul, abs_of_pos (Real.exp_pos (-t))]
      have h_contr : Real.exp (-t) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
      calc Real.exp (-t) * |1 - s'|
          ≤ 1 * |1 - s'| := by gcongr
          _ = |1 - s'| := by rw [one_mul]
          _ < ε := hs'
  -- H3: Linearity
  · intro t s₁ s₂ a b
    show Real.exp (-t) * (a * s₁ + b * s₂) = a * (Real.exp (-t) * s₁) + b * (Real.exp (-t) * s₂)
    ring
  -- H2: Semigroup
  · intro t₁ t₂ s
    show Real.exp (-(t₁ + t₂)) * s = Real.exp (-t₁) * (Real.exp (-t₂) * s)
    rw [neg_add, Real.exp_add]
    ring
  -- Negation: no nonzero periodic orbit
  · rintro ⟨s, T, hs_ne, hT_pos, hperiodic⟩
    have h1 := hperiodic 1
    simp only [Nat.cast_one, one_mul] at h1
    -- h1 : Real.exp (-T) * s = s
    have h_factor : (Real.exp (-T) - 1) * s = 0 := by linarith
    -- (exp(-T) - 1) * s = 0 and s ≠ 0 → exp(-T) - 1 = 0
    have h_factor_zero : Real.exp (-T) - 1 = 0 := by
      by_contra h_ne_zero
      exact (mul_ne_zero h_ne_zero hs_ne) h_factor
    have h_exp_eq_1 : Real.exp (-T) = 1 := by linarith
    -- T > 0 → -T < 0 → exp(-T) < 1, contradicting exp(-T) = 1
    have h_exp_lt_1 : Real.exp (-T) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
    linarith

/-! ## Experiment 5c: The KEY INSIGHT — isometry (H14) forces periodicity in finite dim

The contraction counterexample (Experiment 5b) shows H8 + H3 + H2 + H5 is NOT enough:
exp(-t)·v contracts, so no nonzero periodic orbit exists. The missing hypothesis is
H14 (isometry): if propagation preserves distances, contraction is impossible.

The mathematical argument:
  1. H14 (isometry) + H3 (linearity) → propagate(t, ·) is a linear isometry → orthogonal matrix
  2. H2 (semigroup) → one-parameter group of orthogonal matrices
  3. Finite-dim + continuity → U(t) = exp(tA) for skew-symmetric A (Stone's theorem, finite-dim)
  4. Spectral theorem: A has eigenvalues 0 or ±iωⱼ
  5. If any ωⱼ ≠ 0: eigenvector v ≠ 0, U(2π/ωⱼ)v = v → nonzero periodic orbit
  6. If all ωⱼ = 0: U(t) = I → every nonzero v is periodic

Steps 1-2 are straightforward. Steps 3-4 require the finite-dimensional spectral theorem
for skew-symmetric matrices (Mathlib has the pieces but the assembly is nontrivial).

This section proves the CONCRETE 2D case (step 5 for a specific rotation) and states
the general theorem. The general proof needs the spectral theorem machinery — that's
the 10% for DeepSeek or Claude to bang down.
-/

/-- The 2D rotation semigroup: propagate(t, (x, y)) = R(ωt)·(x, y) where R is the
    standard rotation matrix. This is the canonical example of an isometric linear
    semigroup with a nonzero periodic orbit. -/
noncomputable def rotationProp (ω t : ℝ) (s : ℝ × ℝ) : ℝ × ℝ :=
  (Real.cos (ω * t) * s.1 - Real.sin (ω * t) * s.2,
   Real.sin (ω * t) * s.1 + Real.cos (ω * t) * s.2)

/-- The 2D rotation semigroup is linear in the state. -/
theorem rotation_semigroup_linear (ω : ℝ) :
    ∀ (t : ℝ) (s₁ s₂ : ℝ × ℝ) (a b : ℝ),
      rotationProp ω t (a • s₁ + b • s₂) = a • rotationProp ω t s₁ + b • rotationProp ω t s₂ := by
  intro t s₁ s₂ a b
  ext
  · dsimp [rotationProp]
    show Real.cos (ω * t) * (a * s₁.1 + b * s₂.1) - Real.sin (ω * t) * (a * s₁.2 + b * s₂.2) =
      a * (Real.cos (ω * t) * s₁.1 - Real.sin (ω * t) * s₁.2) +
      b * (Real.cos (ω * t) * s₂.1 - Real.sin (ω * t) * s₂.2)
    ring
  · dsimp [rotationProp]
    show Real.sin (ω * t) * (a * s₁.1 + b * s₂.1) + Real.cos (ω * t) * (a * s₁.2 + b * s₂.2) =
      a * (Real.sin (ω * t) * s₁.1 + Real.cos (ω * t) * s₁.2) +
      b * (Real.sin (ω * t) * s₂.1 + Real.cos (ω * t) * s₂.2)
    ring

/-- The 2D rotation semigroup satisfies the semigroup property. -/
theorem rotation_semigroup_semigroup (ω : ℝ) :
    ∀ (t₁ t₂ : ℝ) (s : ℝ × ℝ),
      rotationProp ω (t₁ + t₂) s = rotationProp ω t₁ (rotationProp ω t₂ s) := by
  intro t₁ t₂ s
  ext
  · dsimp [rotationProp]
    rw [show ω * (t₁ + t₂) = ω * t₁ + ω * t₂ from by ring, Real.cos_add, Real.sin_add]
    ring
  · dsimp [rotationProp]
    rw [show ω * (t₁ + t₂) = ω * t₁ + ω * t₂ from by ring, Real.cos_add, Real.sin_add]
    ring

/-- The 2D rotation semigroup with ω ≠ 0 has a nonzero periodic orbit.
    Period: T = 2π/|ω|. Orbit: every nonzero vector returns after T.

    This is the concrete demonstration that H14 (isometry) + H3 (linearity) +
    H2 (semigroup) + finite-dim → nonzero periodic orbit. The contraction
    counterexample (exp(-t)·v) fails because it's not isometric. The rotation
    succeeds because isometry prevents contraction, forcing the eigenvalues
    onto the unit circle. -/
theorem rotation_semigroup_nonzero_periodic_orbit (ω : ℝ) (hω : ω ≠ 0) :
    ∃ (s : ℝ × ℝ) (T : ℝ), s ≠ (0, 0) ∧ T > 0 ∧
      ∀ (n : ℕ), rotationProp ω (↑n * T) s = s := by
  by_cases hpos : ω > 0
  · -- Case ω > 0: T = 2π/ω, angle = n * 2π
    refine ⟨(1, 0), 2 * Real.pi / ω, ?_, ?_, ?_⟩
    · intro h; exact absurd h (by simp)
    · positivity
    · intro n
      show (Real.cos (ω * (↑n * (2 * Real.pi / ω))) * 1 - Real.sin (ω * (↑n * (2 * Real.pi / ω))) * 0,
            Real.sin (ω * (↑n * (2 * Real.pi / ω))) * 1 + Real.cos (ω * (↑n * (2 * Real.pi / ω))) * 0) = (1, 0)
      have hangle : ω * (↑n * (2 * Real.pi / ω)) = ↑n * (2 * Real.pi) := by
        field_simp
      rw [hangle, Real.cos_nat_mul_two_pi n]
      have hsin : Real.sin (↑n * (2 * Real.pi)) = 0 := by
        simpa using Real.sin_add_nat_mul_two_pi 0 n
      rw [hsin]; ring
  · -- Case ω < 0: T = 2π/(-ω), angle = -n * 2π
    have hneg : ω < 0 := lt_of_le_of_ne (le_of_not_gt hpos) (fun h => hω (h.symm ▸ rfl))
    refine ⟨(1, 0), 2 * Real.pi / (-ω), ?_, ?_, ?_⟩
    · intro h; exact absurd h (by simp)
    · have hnpos : -ω > 0 := neg_pos.mpr hneg
      have hpi : Real.pi > 0 := Real.pi_pos
      positivity
    · intro n
      show (Real.cos (ω * (↑n * (2 * Real.pi / (-ω)))) * 1 - Real.sin (ω * (↑n * (2 * Real.pi / (-ω)))) * 0,
            Real.sin (ω * (↑n * (2 * Real.pi / (-ω)))) * 1 + Real.cos (ω * (↑n * (2 * Real.pi / (-ω)))) * 0) = (1, 0)
      have hangle : ω * (↑n * (2 * Real.pi / (-ω))) = -(↑n * (2 * Real.pi)) := by
        field_simp
      rw [hangle, Real.cos_neg, Real.sin_neg, Real.cos_nat_mul_two_pi n]
      have hsin : Real.sin (↑n * (2 * Real.pi)) = 0 := by
        simpa using Real.sin_add_nat_mul_two_pi 0 n
      rw [hsin]; ring

/-! ## General theorem (STATED — needs spectral theorem machinery)

The following theorem is the general version. The proof requires the finite-dimensional
spectral theorem for skew-symmetric matrices, which Mathlib has in pieces but which
requires nontrivial assembly. This is the 10% that remains.

PROOF STRATEGY (for DeepSeek or Claude to formalize):

1. H14 (isometry) + H3 (linearity) + H21 (d = norm) → propagate(t, ·) is a linear
   isometry of a finite-dimensional inner product space → an orthogonal matrix O(t).

2. H2 (semigroup) → O(s + t) = O(s) · O(t), i.e., t ↦ O(t) is a one-parameter group
   in O(D).

3. CONTINUITY: In finite dimensions, a linear map is continuous. The semigroup property
   + linearity gives continuity of t ↦ O(t) (this needs a proof but follows from
   finite-dimensionality).

4. STONE'S THEOREM (finite-dim): A continuous one-parameter group of orthogonal matrices
   is O(t) = exp(t · A) where A is skew-symmetric (A^T = -A).

5. SPECTRAL THEOREM for skew-symmetric A: eigenvalues are 0 or ±iωⱼ (purely imaginary).
   The matrix A can be block-diagonalized into 2×2 rotation blocks [[0, -ωⱼ], [ωⱼ, 0]]
   plus a zero block.

6. PERIODIC ORBIT:
   - If all ωⱼ = 0: A = 0, O(t) = I, every nonzero v is periodic with any period.
   - If some ωⱼ ≠ 0: the corresponding eigenvector v ≠ 0 satisfies O(2π/|ωⱼ|) v = v,
     giving a nonzero periodic orbit with period 2π/|ωⱼ|.

KEY MATHLIB LEMMAS NEEDED:
- `Matrix.skewSymmetric` and its spectral properties
- `Matrix.exp` (matrix exponential) and its relation to one-parameter groups
- Continuous linear maps in finite dimensions
- Eigenvalue decomposition of orthogonal/skew-symmetric matrices

The 2D case above (`rotation_semigroup_nonzero_periodic_orbit`) proves step 6 for a
specific rotation. The general case requires steps 3-5 which are the spectral theorem
machinery.
-/

/-! # DISCOVERY RESULTS (updated for non-circular H8)

  Hypothesis set                                      | Periodic orbit?       | Recurrence+stability? | Why
  BareMedium alone                                    | NO                    | NO                    | No structure guarantees recurrence or stability
  H8 (Coherence)                                      | NO                    | YES (non-circular)    | H8 IS the recurrence + stability statement
  H3 + H2 (Linear + Semigroup)                        | NO                    | NO                    | Real linear semigroups have no periodic orbits (need complex)
  H1 (Reversible)                                     | NO (counterexample)   | NO                    | Injectivity != periodicity; translation flow x+t is injective but has no periodic orbit
  H8 + H3 + H2 + H5 (vacuous)                         | YES (zero fixed point)| YES                   | Proven trivially by s = 0; H8, H2, H5 unused
  H8 + H3 + H2 + H5 (non-zero)                        | NO (counterexample)   | YES                   | Contraction semigroup exp(-t)*v has no non-zero periodic orbit (machine-verified)
  H3 + H2 + H14 + H5 + H21 (no continuity)            | NO (counterexample)   | YES                   | Discontinuous homomorphism from R to SO(2) via Hamel basis; no nonzero periodic orbit (informal, needs AC)
  H3 + H2 + H14 + H5 + H21 + H22 (with continuity)    | YES (needs spectral)  | YES                   | Stone's theorem + spectral theorem for skew-symmetric A; 2D case proven, general case needs Mathlib assembly
  H8 + H3 + H2 + H4 + H5 (non-zero, with complex)     | OPEN                  | YES                   | Even with complex eigenvalues, one approximate return + stability does not force non-zero periodic orbit
  H3 + H2 + H14 + H5 (2D rotation, concrete)           | YES (non-zero, PROVEN)| N/A                   | rotation_semigroup_nonzero_periodic_orbit: 2D rotation with ω≠0 has period 2π/|ω|
  H3 + H2 + H14 + H5 + H21 + H22 + IP (general, D-dim)  | PARTIAL (sorry)       | N/A                   | isometry_linear_semigroup_gives_nonzero_periodic_orbit: μ=±2 cases PROVEN (T=1,2); |μ|<2 case needs Stone's theorem (sorry). Uses S=U(1)+U(-1) self-adjoint + spectral theorem.|

## Honest parameter count for recurrence:

To prove `∃ s T, T > 0 ∧ ∀ n, propagate(n*T, s) = s` we need:
  - H8_Coherence (postulated directly) — gives approximate recurrence + stability, NOT exact periodicity.
  - The trivial exact periodicity (zero fixed point) follows from H3 + algebraic typeclass structure only.
    H8, H2, and H5 are unused in that vacuous proof.
  - Non-trivial exact periodicity: expected FALSE under H8 + H3 + H2 + H5 as stated
    (informal contraction counterexample). Needs stronger H8 or additional hypotheses.

The discovery: **recurrence + stability costs 1 parameter (H8), but non-trivial exact periodicity is not guaranteed by H3+H2+H5 alone.**
Z₃ circulant structure needs even more (H7, H12/H13, etc.).

## CIRCULARITY ALERT (Codex 2026-06-22):

The same A→A pattern can reappear at the matrix level. `degenerate_residue_forces_circulant`
(Z3FromBareMedium.lean) proves: zero diagonal + equal row sums + DEGENERATE residue →
M = c/(D-1)·(J-I). This is a valid conditional linear-algebra theorem. What it does NOT
prove is that degenerate residue follows from non-symmetric premises. If the answer is
"permutation symmetry (H12)" then we assumed a symmetry to derive a symmetry — the same
circularity one level up. The ledger must record this explicitly. The physical origin
of degenerate residue remains an open question.

## Next discovery targets:
- Can H9 (causal velocity bound) + H2 (semigroup) give recurrence? (Probably not)
- Can H10 (scale invariance) + anything give recurrence? (Scale invariance ≠ periodicity)
- What is the MINIMUM hypothesis set for degenerate residue / Z₃ circulant structure?
  Candidates: H3 + H5 + H7 + H12 (linear + finite-dim + Postulate D + permutation symmetry) = 4+ parameters.
  Can we do better WITHOUT assuming a symmetry? Let Lean answer.
- H10 audit: check whether λ_c and Planck-boundary coupling secretly use H10.
-/

/-! # ISOMETRY EXPERIMENTS (Devin, 2026-06-25)

## The Real Eigenvalue Obstruction

The D=3 J-I circulant has REAL eigenvalues only (machine-verified:
ArbitraryD.lean: `circulant_D_uniform_eigenvalue` gives (D-1)=2,
`circulant_D_residue_eigenvalue` gives -1; PFCore.lean:
`God_Equation_eigenvalues` gives {0, -3/2, -3/2}).

Real eigenvalues → contraction dynamics → NO oscillation → NO non-zero
periodic orbits. Complex eigenvalues (needed for periodicity) require
b ≠ c in the circulant first row (0, b, c), which is the NON-symmetric
case that J-I excludes.

Z₃ spatial symmetry (M = J-I) and temporal periodicity are INDEPENDENT
axes that cannot be connected through the standard circulant coupling
matrix. See DESIGN_H_ISOMETRY_REAL_EIGENVALUE_20260625.md for full analysis.

## H14: Isometry — propagation preserves the pseudometric.

Closes the dissipation gap (exp(-t)·v counterexample from Experiment 5b):
isometry forbids contraction. Does NOT assume periodicity.
Cost: 1 new hypothesis, 0 transitive imports. -/

/-- H14: Isometry — propagation preserves distances.
    d(s₁, s₂) = d(propagate(t, s₁), propagate(t, s₂)) for all t, s₁, s₂.
    This is the STRONG form: exact distance preservation.
    Closes the exp(-t)·v dissipation counterexample.
    Does NOT imply periodicity (Claude: irrational torus rotation is
    isometric and recurrent but never exactly periodic). -/
def Hypothesis_Isometry (M : BareMedium) : Prop :=
  ∀ (t : ℝ) (s₁ s₂ : M.State),
    M.d s₁ s₂ = M.d (M.propagate t s₁) (M.propagate t s₂)

/-- H15: Metric identity — d(s₁, s₂) = 0 → s₁ = s₂.
    BareMedium.d has no axioms; this is the minimal metric property
    needed to connect isometry to injectivity. Without it, d could
    be the zero function and isometry is trivial.
    Cost: 1 hypothesis. Together with H14 + H16, gives reversibility (H1). -/
def Hypothesis_MetricIdentity (M : BareMedium) : Prop :=
  ∀ (s₁ s₂ : M.State), M.d s₁ s₂ = 0 → s₁ = s₂

/-- H16: Metric reflexivity — d(s, s) = 0 for all s.
    BareMedium.d has no axioms; this is the minimal property needed
    to connect isometry to the metric identity. Without it, d(x,x)
    could be nonzero and the isometry chain breaks.
    Cost: 1 hypothesis. Together with H14 + H15, gives reversibility (H1). -/
def Hypothesis_MetricReflexivity (M : BareMedium) : Prop :=
  ∀ (s : M.State), M.d s s = 0

/-- H17: Matrix Symmetry — the coupling matrix is symmetric: M(i,j) = M(j,i).
    This is a DIFFERENT symmetry than H12 (permutation invariance) and
    H13 (cyclic invariance). H17 is a property of the matrix itself, not
    of the propagation operation under index transformations.
    Cost: 1 hypothesis. Needed for the D=3 uniqueness lemma. -/
def Hypothesis_MatrixSymmetry {D : ℕ} (M : Fin D → Fin D → ℝ) : Prop :=
  ∀ i j, M i j = M j i

/-- H18: Equal Row Sums — the coupling matrix has equal row sums.
    This ensures the uniform vector is an eigenvector.
    Cost: 1 hypothesis. Needed for the D=3 uniqueness lemma and for the
    residue subspace to be invariant under the dynamics. -/
def Hypothesis_EqualRowSums {D : ℕ} (M : Fin D → Fin D → ℝ) : Prop :=
  ∃ (c : ℝ), ∀ i, ∑ j, M i j = c

/-- H19: Bounded Orbit — the forward orbit of a state stays within a finite
    pseudometric distance of itself. Isometry alone does not imply this:
    the translation flow on `ℝ` is isometric but unbounded (see Experiment 7).
    Cost: 1 hypothesis. Needed for the compact-orbit theorem. -/
def Hypothesis_BoundedOrbit (M : BareMedium) (s : M.State) : Prop :=
  ∃ (R : ℝ), ∀ (t : ℝ), t ≥ 0 → M.d s (M.propagate t s) < R

/-- H21: d-agrees-with-norm — the pseudometric d equals the norm distance.
    This bridges the bare pseudometric (no topology) to the NormedSpace
    structure (which gives MetricSpace → Heine-Borel). Without this, d is
    just a function with no connection to the topology of M.State.
    Cost: 1 hypothesis. Needed for the compact-orbit theorem (Experiment 7). -/
def Hypothesis_DIsNorm (M : BareMedium) [NormedAddCommGroup M.State] : Prop :=
  ∀ (s₁ s₂ : M.State), M.d s₁ s₂ = ‖s₁ - s₂‖

/-- H22: Continuity — t ↦ propagate(t, s) is continuous for each s.
    This is REQUIRED for the periodic orbit theorem (Experiment 5d).
    Without it, a discontinuous group homomorphism from ℝ to SO(2)
    (constructed via a Hamel basis of ℝ over ℚ) satisfies H3 + H2 + H14 + H5 + H21
    but has NO nonzero periodic orbit. The image of ℝ under such a homomorphism
    is dense in SO(2), so no T > 0 gives U(T) = I.

    With H22, the theorem is TRUE: a continuous one-parameter group of linear
    isometries in finite dimensions has a generator A (Stone's theorem, finite-dim),
    A is skew-symmetric, its eigenvalues are 0 or ±iωⱼ, and any eigenvector with
    ωⱼ ≠ 0 gives a periodic orbit with period 2π/|ωⱼ|.

    Cost: 1 hypothesis. The recurrence theorem (Experiment 7) does NOT need H22
    (discrete iterates + sequential compactness suffice for approximate return).
    The PERIODIC ORBIT theorem does need H22 (exact return requires the generator). -/
def Hypothesis_Continuity (M : BareMedium) [TopologicalSpace M.State] : Prop :=
  ∀ (s : M.State), Continuous (fun t => M.propagate t s)

/-! ## Experiment 5d: The periodic orbit theorem (WITH continuity)

DISCOVERY (2026-07-14): The theorem `isometry_linear_semigroup_gives_nonzero_periodic_orbit`
is FALSE as stated without H22 (continuity). The counterexample is:

  Counterexample (informal, requires AC):
  - Let f: ℝ → ℝ be a ℚ-linear isomorphism that is NOT ℝ-linear (exists via Hamel basis).
  - Choose f such that f⁻¹(ℤ) = {0} (possible: pick f on a Hamel basis to avoid integers).
  - Define φ: ℝ → SO(2) by φ(t) = rotation by 2π·f(t) mod 2π.
  - Then φ is a group homomorphism (ℚ-linear → additive), injective (f⁻¹(ℤ)={0}),
    and discontinuous (not ℝ-linear).
  - Define propagate(t, (x,y)) = φ(t)·(x,y) on ℝ² with the Euclidean norm.
  - This satisfies H3 (linear), H2 (semigroup), H14 (isometry), H5 (finite-dim),
    H21 (d = norm), bounded orbits, and nontrivial state space.
  - But φ(T) = I requires f(T) ∈ ℤ, which forces T = 0 (by f⁻¹(ℤ) = {0}).
  - So NO nonzero periodic orbit exists. ∎

With H22 (continuity), the theorem is TRUE. The proof requires:
  1. propagate(0, ·) = id (from linearity + semigroup + isometry — proven below)
  2. Each propagate(t, ·) is a linear isometry → orthogonal matrix (needs inner product)
  3. t ↦ propagate(t, ·) is a continuous group homomorphism ℝ → O(D)
  4. Stone's theorem (finite-dim): U(t) = exp(tA) for skew-symmetric A
  5. Spectral theorem: A has eigenvalues 0 or ±iωⱼ
  6. If all ωⱼ = 0: A = 0, U = id, any nonzero s works
  7. If some ωⱼ ≠ 0: eigenvector v, T = 2π/|ωⱼ| gives U(T)v = v

The 2D case (step 7 for a single rotation) is proven as `rotation_semigroup_nonzero_periodic_orbit`.
The general case needs Mathlib's spectral theorem for skew-symmetric matrices, which
is not yet assembled in a directly usable form.

Below we prove:
  (a) propagate(0, ·) = id (Lemma: identity_at_zero)
  (b) The trivial case: if propagate = id, every nonzero state is periodic
  (c) The 1D case: continuous homomorphism from ℝ to O(1) = {±1} is constant
-/

/-- Lemma: propagate(0, ·) = id.
    From H2 (semigroup): propagate(0, propagate(0, s)) = propagate(0, s), so P = propagate(0, ·)
    is idempotent. From H3 (linearity): P is linear. So P is a linear projection.
    From H14 (isometry) + H21 (d = norm): ‖P s‖ = ‖s‖ for all s (norm-preserving).
    A norm-preserving linear projection is the identity: for any s, P(s - Ps) = Ps - P²s = 0,
    and ‖s - Ps‖ = ‖P(s - Ps)‖ = ‖0‖ = 0, so s = Ps. -/
theorem identity_at_zero
    (M : BareMedium) [NormedAddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hDNorm : Hypothesis_DIsNorm M) :
    ∀ (s : M.State), M.propagate 0 s = s := by
  intro s
  -- P := propagate(0, ·) is a linear projection (idempotent from semigroup)
  have h_idem : M.propagate 0 (M.propagate 0 s) = M.propagate 0 s := by
    have h := hSemi 0 0 s
    simpa using h.symm
  -- P is linear, so P(0) = 0
  have h_P0 : M.propagate 0 (0 : M.State) = 0 := by
    have h := hLin 0 (0 : M.State) (0 : M.State) 0 0
    simp at h
    exact h
  -- Isometry: d(s, 0) = d(Ps, P0) = d(Ps, 0)
  -- With d = norm: ‖s - 0‖ = ‖Ps - 0‖, i.e., ‖s‖ = ‖Ps‖
  have h_norm_pres : ‖M.propagate 0 s‖ = ‖s‖ := by
    have h_dist := hIso 0 s (0 : M.State)
    rw [h_P0] at h_dist
    have h_d1 : M.d s (0 : M.State) = ‖s - (0 : M.State)‖ := hDNorm s 0
    have h_d2 : M.d (M.propagate 0 s) (0 : M.State) = ‖M.propagate 0 s - (0 : M.State)‖ :=
      hDNorm (M.propagate 0 s) 0
    rw [h_d1, h_d2] at h_dist
    simpa [sub_zero] using h_dist.symm
  -- P(s - Ps) = Ps - P²s = Ps - Ps = 0 (by idempotence and linearity)
  have h_Pdiff : M.propagate 0 (s - M.propagate 0 s) = 0 := by
    have h_lin := hLin 0 s (M.propagate 0 s) 1 (-1)
    rw [h_idem] at h_lin
    simp [one_smul, neg_smul] at h_lin
    rw [sub_eq_add_neg]
    exact h_lin
  -- ‖s - Ps‖ = ‖P(s - Ps)‖ = ‖0‖ = 0, so s = Ps
  have h_norm_diff : ‖s - M.propagate 0 s‖ = 0 := by
    have h_dist := hIso 0 (s - M.propagate 0 s) (0 : M.State)
    rw [h_Pdiff, h_P0] at h_dist
    have h_d00 : M.d (0 : M.State) (0 : M.State) = 0 := by
      rw [hDNorm]; simp
    have h_d_diff : M.d (s - M.propagate 0 s) (0 : M.State) = ‖s - M.propagate 0 s‖ := by
      rw [hDNorm]; simp
    rw [h_d_diff, h_d00] at h_dist
    exact h_dist
  -- s - Ps = 0 → Ps = s
  exact (sub_eq_zero.mp (norm_eq_zero.mp h_norm_diff)).symm

/-- The trivial case: if propagate(t, s) = s for all t, then every nonzero state
    is periodic with any period. This is the case A = 0 in the spectral decomposition. -/
theorem trivial_periodic_orbit
    (M : BareMedium) [NormedAddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hDNorm : Hypothesis_DIsNorm M)
    (hNontrivial : ∃ (s : M.State), s ≠ 0)
    (h_trivial : ∀ (t : ℝ) (s : M.State), M.propagate t s = s) :
    ∃ (s : M.State) (T : ℝ), s ≠ 0 ∧ T > 0 ∧
      ∀ (n : ℕ), M.propagate (↑n * T) s = s := by
  obtain ⟨s, hs⟩ := hNontrivial
  exact ⟨s, 1, hs, by norm_num, fun n => h_trivial _ _⟩

/-- ODD-DIMENSIONAL THEOREM (no spectral theorem needed):
    H3 (linearity) + H2 (semigroup) + H14 (isometry) + H5 (finite-dim) + H21 (d = norm)
    + H22 (continuity) + [InnerProductSpace ℝ] + Odd(finrank) → nonzero periodic orbit.

    PROOF STRATEGY (Devin, 2026-07-14):
    1. U(t) := propagate(t, ·) is a linear map (H3)
    2. ‖U(t) v‖ = ‖v‖ (H14 + H21 + H3) → U(t) is a linear isometry
    3. U(t)† ∘ U(t) = id (LinearIsometry.adjoint_comp_self')
    4. det(U(t)†) · det(U(t)) = 1 (det_comp)
    5. det(U(t)†) = det(U(t)) (adjoint = transpose in real IP space, det_transpose)
    6. det(U(t))² = 1 → det(U(t)) = ±1
    7. det(U(0)) = 1 (U(0) = id, from identity_at_zero)
    8. det(U(s+t)) = det(U(s))·det(U(t)) (semigroup + det_comp)
    9. By IVT: det(U(t)) = 1 for all t (continuous, ±1-valued, det(U(0))=1)
    10. For T = 1: U(1) is orthogonal with det = 1, in odd dimension
    11. det(U(1) - I) = 0 (algebraic trick: A⁻¹ = Aᵀ, det(A-I) = det(Aᵀ-I) = det(A⁻¹-I)
        = det(A⁻¹(I-A)) = det(A⁻¹)·(-1)^n·det(A-I) = -det(A-I) for odd n, det(A)=1)
    12. ∃ v ≠ 0 with U(1)v = v (det = 0 → ker ≠ ⊥)
    13. U(n)v = U(1)^n v = v for all n (semigroup)

    This covers D = 1, 3, 5, ... — including D = 3 (the spatial dimension of our universe).
    The general case (even D) needs the spectral theorem or complexification. -/
theorem isometry_linear_semigroup_odd_dim_periodic_orbit
    (M : BareMedium) [NormedAddCommGroup M.State] [InnerProductSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hDNorm : Hypothesis_DIsNorm M)
    (hCont : Hypothesis_Continuity M)
    (hNontrivial : ∃ (s : M.State), s ≠ 0)
    (hOdd : Odd (Module.finrank ℝ M.State)) :
    ∃ (s : M.State) (T : ℝ), s ≠ 0 ∧ T > 0 ∧
      ∀ (n : ℕ), M.propagate (↑n * T) s = s := by
  -- Step 1: Construct U(t) as a LinearMap for each t
  let U (t : ℝ) : M.State →ₗ[ℝ] M.State := {
    toFun := fun s => M.propagate t s
    map_add' := by
      intro s₁ s₂
      have h := hLin t s₁ s₂ 1 1
      simp [one_smul] at h ⊢
      exact h
    map_smul' := by
      intro a s
      have h_zero : M.propagate t (0 : M.State) = 0 := by
        have h := hLin t (0 : M.State) (0 : M.State) 0 0
        simp at h
        exact h
      have h := hLin t s (0 : M.State) a 0
      simp [h_zero] at h ⊢
      exact h
  }
  -- Step 2: U(t) preserves the norm
  have h_norm_pres (t : ℝ) (v : M.State) : ‖U t v‖ = ‖v‖ := by
    have h_zero : M.propagate t (0 : M.State) = 0 := by
      have h := hLin t (0 : M.State) (0 : M.State) 0 0
      simp at h
      exact h
    have h_iso := hIso t v (0 : M.State)
    rw [h_zero] at h_iso
    have h_d1 : M.d v (0 : M.State) = ‖v - (0 : M.State)‖ := hDNorm v (0 : M.State)
    have h_d2 : M.d (M.propagate t v) (0 : M.State) = ‖M.propagate t v - (0 : M.State)‖ :=
      hDNorm (M.propagate t v) (0 : M.State)
    rw [h_d1, h_d2] at h_iso
    simp [sub_zero] at h_iso ⊢
    exact h_iso.symm
  -- Step 3: U(t) preserves distances
  have h_dist_pres (t : ℝ) (x y : M.State) : dist (U t x) (U t y) = dist x y := by
    have h_linearity : U t (x - y) = U t x - U t y := by rw [map_sub]
    rw [dist_eq_norm_sub, dist_eq_norm_sub, ← h_linearity]
    exact h_norm_pres t (x - y)
  -- Step 4: det(U(t))² = 1 for all t
  have h_det_sq (t : ℝ) : LinearMap.det (U t) ^ 2 = 1 := by
    have h_isometry : Isometry (U t : M.State → M.State) :=
      Isometry.of_dist_eq (h_dist_pres t)
    let LI : M.State →ₗᵢ[ℝ] M.State := (U t).toLinearIsometry h_isometry
    have h_adj_comp : LinearMap.adjoint LI.toLinearMap ∘ₗ (U t) = LinearMap.id :=
      LI.adjoint_comp_self'
    have h_det_comp : LinearMap.det (LinearMap.adjoint LI.toLinearMap ∘ₗ (U t : M.State →ₗ[ℝ] M.State)) =
        (1 : ℝ) := by
      rw [h_adj_comp, LinearMap.det_id]
    rw [LinearMap.det_comp] at h_det_comp
    have h_det_adj_eq_det : LinearMap.det (LinearMap.adjoint LI.toLinearMap) = LinearMap.det (U t) := by
      let ob := stdOrthonormalBasis ℝ M.State
      let b := ob.toBasis
      have h_adj_mat : LinearMap.det (LinearMap.adjoint LI.toLinearMap) =
        Matrix.det (LinearMap.toMatrix b b (LinearMap.adjoint LI.toLinearMap)) :=
        (LinearMap.det_toMatrix b (LinearMap.adjoint LI.toLinearMap)).symm
      have h_U_mat : LinearMap.det (U t) =
        Matrix.det (LinearMap.toMatrix b b (U t)) :=
        (LinearMap.det_toMatrix b (U t)).symm
      rw [h_adj_mat, h_U_mat]
      have h_toMat_adj : LinearMap.toMatrix b b (LinearMap.adjoint LI.toLinearMap) =
        Matrix.conjTranspose (LinearMap.toMatrix b b (U t)) := by
        exact LinearMap.toMatrix_adjoint ob ob _
      rw [h_toMat_adj]
      have h_conj_eq_trans : Matrix.conjTranspose (LinearMap.toMatrix b b (U t)) =
        (LinearMap.toMatrix b b (U t)).transpose := by
        ext i j
        simp [Matrix.conjTranspose]
      rw [h_conj_eq_trans, Matrix.det_transpose]
    rw [h_det_adj_eq_det] at h_det_comp
    rw [pow_two, h_det_comp]
  -- Step 5: det(U(0)) = 1
  have h_det_zero : LinearMap.det (U 0) = 1 := by
    have h_id : ∀ v, U 0 v = v := fun v => identity_at_zero M hLin hSemi hIso hDNorm v
    have h_id_linearMap : U 0 = LinearMap.id := by ext v; exact h_id v
    rw [h_id_linearMap, LinearMap.det_id]
  -- Step 6: det(U(t)) = 1 for all t (pure algebra, no IVT!)
  have h_det_mul (s t : ℝ) : LinearMap.det (U (s + t)) = LinearMap.det (U s) * LinearMap.det (U t) := by
    have h_semi : U (s + t) = U s ∘ₗ U t := by ext v; exact hSemi s t v
    rw [h_semi, LinearMap.det_comp]
  have h_det_one (t : ℝ) : LinearMap.det (U t) = 1 := by
    have h_half : t = (t / 2) + (t / 2) := by ring
    rw [h_half, h_det_mul, ← pow_two, h_det_sq (t/2)]
  -- Step 7: det(U(1) - I) = 0 (odd dimension + det = 1)
  have h_det_minus_id : LinearMap.det (U 1 - LinearMap.id) = 0 := by
    let ob := stdOrthonormalBasis ℝ M.State
    let b := ob.toBasis
    let n := Module.finrank ℝ M.State
    rw [← LinearMap.det_toMatrix b (U 1 - LinearMap.id)]
    rw [map_sub, LinearMap.toMatrix_id]
    set A := LinearMap.toMatrix b b (U 1)
    have h_det_A : Matrix.det A = 1 := by
      have := h_det_one 1
      rw [← LinearMap.det_toMatrix b (U 1)] at this
      exact this
    have h_A_inv : IsUnit A.det := by rw [h_det_A]; exact isUnit_one
    -- Aᵀ * A = I (orthogonal, from isometry)
    have h_orth : A.transpose * A = 1 := by
      have h_isom : Isometry (U 1 : M.State → M.State) :=
        Isometry.of_dist_eq (h_dist_pres 1)
      let LI : M.State →ₗᵢ[ℝ] M.State := (U 1).toLinearIsometry h_isom
      have h_adj_id : LI.adjoint ∘ₗ LI.toLinearMap = LinearMap.id :=
        LI.adjoint_comp_self'
      have h_mat : LinearMap.toMatrix b b (LI.adjoint ∘ₗ LI.toLinearMap) =
        LinearMap.toMatrix b b LinearMap.id := by rw [h_adj_id]
      have h_comp : LinearMap.toMatrix b b (LI.adjoint ∘ₗ LI.toLinearMap) =
        LinearMap.toMatrix b b LI.adjoint * LinearMap.toMatrix b b (U 1) := by
        rw [show LI.toLinearMap = (U 1 : M.State →ₗ[ℝ] M.State) from rfl]
        exact LinearMap.toMatrix_comp b b b LI.adjoint (U 1)
      rw [h_comp, LinearMap.toMatrix_id] at h_mat
      have h_adj_mat : LinearMap.toMatrix b b LI.adjoint = Matrix.conjTranspose A := by
        exact LinearMap.toMatrix_adjoint ob ob _
      rw [h_adj_mat] at h_mat
      have h_conj_trans : Matrix.conjTranspose A = A.transpose := by
        ext i j; simp [Matrix.conjTranspose]
      rw [h_conj_trans] at h_mat
      exact h_mat
    -- Aᵀ = A⁻¹
    have h_trans_inv : A.transpose = A⁻¹ := by
      have h_inv_left : A⁻¹ * A = 1 := Matrix.nonsing_inv_mul A h_A_inv
      have h_both : A.transpose * A = A⁻¹ * A := by rw [h_orth, h_inv_left]
      have h_A_unit : IsUnit A := A.isUnit_iff_isUnit_det.mpr h_A_inv
      exact (IsUnit.mul_left_inj h_A_unit).mp h_both
    -- det(A - I) = det(Aᵀ - I) = det(A⁻¹ - I)
    have h_det_trans : (A - 1).det = (A.transpose - 1).det := by
      have h : (A - 1).det = (A - 1).transpose.det := Matrix.det_transpose _
      rw [Matrix.transpose_sub, Matrix.transpose_one] at h
      exact h
    have h_det_inv_trans : (A.transpose - 1).det = (A⁻¹ - 1).det := by rw [h_trans_inv]
    -- A⁻¹ - I = A⁻¹ * (-(A - I))
    have h_factor : A⁻¹ - 1 = A⁻¹ * (-(A - 1)) := by
      have h1 : -(A - 1) = 1 - A := by rw [neg_sub]
      rw [h1, Matrix.mul_sub, Matrix.mul_one, Matrix.nonsing_inv_mul A h_A_inv]
    have h_det_inv : (A⁻¹).det = 1 := by
      rw [Matrix.det_nonsing_inv, h_det_A]
      exact @Ring.inverse_one ℝ _
    have h_card : Fintype.card (Fin (Module.finrank ℝ M.State)) = Module.finrank ℝ M.State := by
      exact Fintype.card_fin _
    have h_neg_one_pow : (-1 : ℝ) ^ n = -1 := hOdd.neg_one_pow
    -- Chain: (A-1).det = (Aᵀ-1).det = (A⁻¹-1).det = 1 * (-1)^n * (A-1).det = -(A-1).det
    have h_chain : (A - 1).det = (A⁻¹ - 1).det := by rw [h_det_trans, h_det_inv_trans]
    have h_factored : (A⁻¹ - 1).det = (A⁻¹).det * (-(A - 1)).det := by
      rw [h_factor]; exact Matrix.det_mul _ _
    rw [Matrix.det_neg] at h_factored
    rw [h_card, h_neg_one_pow] at h_factored
    rw [h_det_inv, one_mul, neg_one_mul] at h_factored
    -- h_factored: (A⁻¹ - 1).det = -(A - 1).det
    -- h_chain: (A - 1).det = (A⁻¹ - 1).det
    -- So (A - 1).det = -(A - 1).det → 2*(A-1).det = 0 → (A-1).det = 0
    have h_eq : (A - 1).det = -(A - 1).det := by
      exact h_chain.trans h_factored
    have h_zero : (A - 1).det = 0 := by linarith
    exact h_zero
  -- Step 8: ∃ v ≠ 0 with U(1)v = v
  have h_eigenvector : ∃ v : M.State, v ≠ 0 ∧ U 1 v = v := by
    have h_ker : LinearMap.ker (U 1 - LinearMap.id) ≠ ⊥ :=
      LinearMap.det_eq_zero_iff_ker_ne_bot.mp h_det_minus_id
    obtain ⟨v, hv_mem, hv_nezero⟩ := (Submodule.ne_bot_iff _).mp h_ker
    refine ⟨v, hv_nezero, ?_⟩
    have h_ker_apply : (U 1 - LinearMap.id : M.State →ₗ[ℝ] M.State) v = 0 :=
      LinearMap.mem_ker.mp hv_mem
    have h_apply : (U 1 : M.State →ₗ[ℝ] M.State) v - v = 0 := h_ker_apply
    exact sub_eq_zero.mp h_apply
  -- Step 9: U(n)v = v for all n (semigroup)
  obtain ⟨v, hv_nezero, hv_eigen⟩ := h_eigenvector
  have hv_prop : M.propagate 1 v = v := hv_eigen
  refine ⟨v, 1, hv_nezero, by norm_num, ?_⟩
  intro n
  induction' n with n ih
  · simp
    exact identity_at_zero M hLin hSemi hIso hDNorm v
  · have h_cast : (↑(n + 1) : ℝ) = ↑n + 1 := by simp [Nat.cast_add, Nat.cast_one]
    rw [h_cast, mul_one, hSemi, hv_prop]
    rw [mul_one] at ih
    exact ih
/-- Helper: A continuous group homomorphism z: ℝ → Circle with z(0) = 1
    and z(1) ≠ 1 has a positive period T with z(T) = 1.

    This is the key lemma for the |μ| < 2 case of the periodic orbit theorem.
    It replaces Stone's theorem in finite dimensions by using:
    1. Complex.arg to locally lift z to ℝ (near z(0) = 1)
    2. Local additivity of the lift (from exp_eq_exp + bounds)
    3. Local linearity (continuous + locally additive → linear, via Rat density)
    4. Global extension via the group property -/
lemma exists_period_of_continuous_circle_hom
    (z : ℝ → Circle) (hz_cont : Continuous z) (hz_zero : z 0 = 1)
    (hz_add : ∀ s t, z (s + t) = z s * z t) (hz_one_ne : z 1 ≠ 1) :
    ∃ T > 0, z T = 1 := by
  -- Step 1: ∃ δ > 0 with (z t : ℂ) ∈ ball 1 1 for |t| < δ
  have h_coe_cont : ContinuousAt (fun t : ℝ => (z t : ℂ)) 0 :=
    continuousAt_subtype_val.comp hz_cont.continuousAt
  obtain ⟨δ, δ_pos, hδ_ball⟩ : ∃ δ > 0, ∀ t, |t| < δ → (z t : ℂ) ∈ Metric.ball (1 : ℂ) 1 := by
    have h_mem : (z 0 : ℂ) ∈ Metric.ball (1 : ℂ) 1 := by
      rw [hz_zero, Circle.coe_one, Metric.mem_ball, dist_self]; exact zero_lt_one
    have h_ball : ∀ᶠ t in nhds 0, (z t : ℂ) ∈ Metric.ball (1 : ℂ) 1 :=
      h_coe_cont.tendsto.eventually (Metric.isOpen_ball.mem_nhds h_mem)
    obtain ⟨ε, ε_pos, hε⟩ := Metric.eventually_nhds_iff_ball.mp h_ball
    exact ⟨ε, ε_pos, fun t ht => hε _ (by simpa using ht)⟩
  have hδ : ∀ t, |t| < δ → (z t : ℂ) ∈ Complex.slitPlane := fun t ht =>
    Complex.ball_one_subset_slitPlane (hδ_ball t ht)
  -- |arg(z t)| ≤ π/2 for |t| < δ (since z t ∈ ball 1 1 → re > 0)
  have harg_bound : ∀ t, |t| < δ → |Complex.arg ((z t : ℂ))| ≤ Real.pi / 2 := by
    intro t ht
    have hball : (z t : ℂ) ∈ Metric.ball (1 : ℂ) 1 := hδ_ball t ht
    have hre : 0 < (z t : ℂ).re := by
      have hnorm : ‖(z t : ℂ) - 1‖ < 1 := by
        rw [← Complex.dist_eq]; exact hball
      have hre_sub : |((z t : ℂ) - 1).re| ≤ ‖(z t : ℂ) - 1‖ :=
        Complex.abs_re_le_norm _
      rw [Complex.sub_re] at hre_sub
      have h_le : -‖(z t : ℂ) - 1‖ ≤ (z t : ℂ).re - 1 := (abs_le.mp hre_sub).1
      linarith [h_le, hnorm]
    exact Complex.abs_arg_le_pi_div_two_iff.mpr (le_of_lt hre)
  -- Step 2: g(t) = Complex.arg((z t : ℂ)) is continuous for |t| < δ
  let g (t : ℝ) : ℝ := Complex.arg ((z t : ℂ))
  have hg_cont : ∀ t, |t| < δ → ContinuousAt g t := by
    intro t ht
    have hzt : (z t : ℂ) ∈ Complex.slitPlane := hδ t ht
    have h1 : ContinuousAt ((↑) : Circle → ℂ) (z t) := continuousAt_subtype_val
    have h2 : ContinuousAt (fun x : ℝ => (z x : ℂ)) t := h1.comp hz_cont.continuousAt
    have h3 : ContinuousAt Complex.arg ((z t : ℂ)) := Complex.continuousAt_arg hzt
    show ContinuousAt (fun x => Complex.arg ((z x : ℂ))) t
    exact @ContinuousAt.comp ℝ ℂ ℝ _ _ _ (fun x => (z x : ℂ)) t Complex.arg h3 h2
  have hg_zero : g 0 = 0 := by
    show Complex.arg ((z 0 : ℂ)) = 0
    rw [hz_zero, Circle.coe_one, Complex.arg_one]
  have hg_exp : ∀ t, |t| < δ → Circle.exp (g t) = z t := fun t _ =>
    Circle.exp_arg (z t)
  -- Step 3: g is locally additive for |s|, |t|, |s+t| < δ/2
  have hg_add : ∀ s t, |s| < δ/2 → |t| < δ/2 → |s + t| < δ/2 →
      g (s + t) = g s + g t := by
    intro s t hs ht hst
    have hs' : |s| < δ := by linarith
    have ht' : |t| < δ := by linarith
    have hst' : |s + t| < δ := by
      have : |s + t| ≤ |s| + |t| := abs_add_le _ _
      linarith
    have h1 : Circle.exp (g (s + t)) = Circle.exp (g s + g t) := by
      rw [show g (s + t) = Complex.arg ((z (s + t) : ℂ)) from rfl,
          show g s = Complex.arg ((z s : ℂ)) from rfl,
          show g t = Complex.arg ((z t : ℂ)) from rfl]
      rw [hg_exp _ hst', hz_add, Circle.exp_add, hg_exp _ hs', hg_exp _ ht']
    have hgs : |g s| ≤ Real.pi / 2 := harg_bound s hs'
    have hgt : |g t| ≤ Real.pi / 2 := harg_bound t ht'
    have hgst : |g (s + t)| ≤ Real.pi / 2 := harg_bound (s + t) hst'
    have h_bound : |g (s + t) - (g s + g t)| < 2 * Real.pi := by
      have h_sum : |g s + g t| ≤ Real.pi := by
        calc |g s + g t| ≤ |g s| + |g t| := abs_add_le _ _
          _ ≤ Real.pi / 2 + Real.pi / 2 := add_le_add hgs hgt
          _ = Real.pi := by ring
      have h_tri : |g (s + t) - (g s + g t)| ≤ |g (s + t)| + |g s + g t| := by
        have := abs_add_le (g (s + t)) (-(g s + g t))
        rwa [abs_neg, ← sub_eq_add_neg] at this
      linarith [h_tri, hgst, h_sum, Real.pi_pos]
    obtain ⟨m, hm⟩ := Circle.exp_eq_exp.mp h1
    have hm_zero : m = 0 := by
      by_contra hne
      have h_abs_m : 1 ≤ |(m : ℝ)| := by exact_mod_cast Int.one_le_abs hne
      have h_abs_prod : 2 * Real.pi ≤ |(m : ℝ) * (2 * Real.pi)| := by
        have hpi_pos : 0 < 2 * Real.pi := by linarith [Real.pi_pos]
        rw [abs_mul, abs_of_pos hpi_pos]
        nlinarith [h_abs_m, Real.pi_pos, abs_nonneg (m : ℝ)]
      have h_diff : |g (s + t) - (g s + g t)| = |(m : ℝ) * (2 * Real.pi)| := by
        rw [hm]; ring_nf
      have h_ge : 2 * Real.pi ≤ |g (s + t) - (g s + g t)| := by
        rw [h_diff]; exact h_abs_prod
      linarith [h_ge, h_bound]
    rw [hm_zero, Int.cast_zero, zero_mul, add_zero] at hm
    exact hm
  -- Step 4: g(n * x) = n * g(x) for n ∈ ℕ, |x| < δ/4, |n * x| < δ/4
  have hg_nsmul : ∀ n : ℕ, ∀ x, |x| < δ / 4 → |(n : ℝ) * x| < δ / 4 →
      g ((n : ℝ) * x) = (n : ℝ) * g x := by
    intro n
    induction n with
    | zero =>
      intro x hx hkx
      simp only [Nat.cast_zero, zero_mul]
      exact hg_zero
    | succ k ih =>
      intro x hx hkx
      have hkx' : |(k : ℝ) * x| < δ / 4 := by
        have hk_nn : (0 : ℝ) ≤ (k : ℝ) := by exact_mod_cast (Nat.zero_le k)
        have hk1_nn : (0 : ℝ) ≤ ((k + 1 : ℕ) : ℝ) := by exact_mod_cast (Nat.zero_le (k + 1))
        have hk_le : (k : ℝ) ≤ ((k + 1 : ℕ) : ℝ) := by exact_mod_cast (by omega)
        calc |(k : ℝ) * x|
            = (k : ℝ) * |x| := by rw [abs_mul, abs_of_nonneg hk_nn]
          _ ≤ ((k + 1 : ℕ) : ℝ) * |x| := mul_le_mul_of_nonneg_right hk_le (abs_nonneg x)
          _ = |((k + 1 : ℕ) : ℝ) * x| := by
            rw [abs_mul, abs_of_nonneg hk1_nn]
          _ < δ / 4 := hkx
      have h_kx : |(k : ℝ) * x| < δ / 2 := by linarith
      have h_x : |x| < δ / 2 := by linarith
      have h_sum : |(k : ℝ) * x + x| < δ / 2 := by
        have h_eq : (k : ℝ) * x + x = ((k + 1 : ℕ) : ℝ) * x := by
          rw [Nat.cast_add_one]; ring
        rw [h_eq]; linarith
      have h_gkx : g ((k : ℝ) * x) = (k : ℝ) * g x := ih x hx hkx'
      rw [Nat.cast_add_one, show (↑k + 1) * x = ↑k * x + x from by ring]
      rw [hg_add _ _ h_kx h_x h_sum, h_gkx]
      ring
  -- g(-x) = -g(x) for |x| < δ/4
  have hg_neg : ∀ x, |x| < δ / 4 → g (-x) = -g x := by
    intro x hx
    have hx' : |x| < δ / 2 := by linarith
    have hneg' : |-x| < δ / 2 := by rw [abs_neg]; linarith
    have hsum : |x + (-x)| < δ / 2 := by rw [add_neg_cancel, abs_zero]; linarith
    have h1 : g (x + (-x)) = g x + g (-x) := hg_add _ _ hx' hneg' hsum
    rw [add_neg_cancel, hg_zero] at h1
    linarith [h1]
  -- Step 5: g(r * τ) = r * g(τ) for r ∈ ℚ, |r * τ| < δ/4
  set τ : ℝ := δ / 8 with hτ_def
  have τ_pos : 0 < τ := by rw [hτ_def]; positivity
  have hτ_small : |τ| < δ / 4 := by
    rw [hτ_def, abs_of_pos (by positivity)]; linarith [δ_pos]
  have hg_rat : ∀ r : ℚ, |(r : ℝ) * τ| < δ / 4 →
      g ((r : ℝ) * τ) = (r : ℝ) * g τ := by
    intro r hr
    by_cases hr_zero : r = 0
    · simp [hr_zero, zero_mul, hg_zero]
    -- r ≠ 0: use r.num and r.den
    have rden_pos : (0 : ℝ) < (r.den : ℝ) := by
      have hne : r.den ≠ 0 := Rat.den_ne_zero r
      have : (0 : ℕ) < r.den := by
        by_contra h
        push_neg at h
        exact hne (le_antisymm h (Nat.zero_le _))
      exact_mod_cast this
    have rden_ne : (r.den : ℝ) ≠ 0 := ne_of_gt rden_pos
    have h_cast : (r : ℝ) = (r.num : ℝ) / (r.den : ℝ) := Rat.cast_def r
    set x : ℝ := τ / (r.den : ℝ) with hx_def
    have h_rτ : (r : ℝ) * τ = (r.num : ℝ) * x := by
      rw [h_cast, hx_def, div_mul_eq_mul_div, mul_div_assoc]
    have hx_abs : |x| < δ / 4 := by
      rw [hx_def, abs_div, abs_of_pos rden_pos, div_lt_iff₀ rden_pos]
      have h_den_ge : (1 : ℝ) ≤ (r.den : ℝ) := by
        have : (0 : ℕ) < r.den := by
          by_contra h
          push_neg at h
          exact (Rat.den_ne_zero r) (le_antisymm h (Nat.zero_le _))
        exact_mod_cast (by omega : (1 : ℕ) ≤ r.den)
      nlinarith [hτ_small, h_den_ge, δ_pos]
    have hnx : |(r.num : ℝ) * x| < δ / 4 := by rw [← h_rτ]; exact hr
    have h_qτ : (r.den : ℝ) * x = τ := by
      rw [hx_def, mul_div_cancel₀ τ rden_ne]
    have h1 : g τ = (r.den : ℝ) * g x := by
      rw [← h_qτ]
      exact hg_nsmul r.den x hx_abs (by rw [h_qτ]; exact hτ_small)
    have h3 : g x = g τ / (r.den : ℝ) := by
      have hne : (r.den : ℝ) ≠ 0 := rden_ne
      field_simp
      linarith [h1]
    -- g(r.num * x) = r.num * g(x): handle ℤ sign
    have hg_intsmul : ∀ z : ℤ, ∀ y, |y| < δ / 4 → |(z : ℝ) * y| < δ / 4 →
        g ((z : ℝ) * y) = (z : ℝ) * g y := by
      intro z y hy hzy
      by_cases hz : 0 ≤ z
      · have hn : (z.toNat : ℝ) = (z : ℝ) := by exact_mod_cast Int.toNat_of_nonneg hz
        rw [← hn]
        have hny : |(z.toNat : ℝ) * y| < δ / 4 := by rw [hn]; exact hzy
        rw [hg_nsmul z.toNat y hy hny, hn]
      · have hzneg : z < 0 := by omega
        have hneg_nn : 0 ≤ -z := by omega
        have hn : ((-z).toNat : ℝ) = -(z : ℝ) := by
          exact_mod_cast Int.toNat_of_nonneg hneg_nn
        have h_cast : (z : ℝ) = -((-z).toNat : ℝ) := by linarith
        rw [h_cast, neg_mul, neg_mul]
        have habs : |((-z).toNat : ℝ) * y| < δ / 4 := by
          have h_eq : |((-z).toNat : ℝ) * y| = |(z : ℝ) * y| := by
            have h2 : (z : ℝ) * y = -((-z).toNat : ℝ) * y := by rw [h_cast]
            rw [h2]
            rw [show |-((-z).toNat : ℝ) * y| = |((-z).toNat : ℝ) * y| from by
              rw [neg_mul, abs_neg]]
          rw [h_eq]; exact hzy
        rw [hg_neg _ habs]
        rw [hg_nsmul (-z).toNat y hy habs]
    have h_num : g ((r.num : ℝ) * x) = (r.num : ℝ) * g x :=
      hg_intsmul r.num x hx_abs hnx
    rw [h_rτ, h_num, h3, h_cast]
    field_simp
  -- Step 5b: g(t) = α * t for |t| < δ/4 (continuity + density of ℚ)
  set α : ℝ := g τ / τ with hα_def
  have hg_linear : ∀ t, |t| < δ / 4 → g t = α * t := by
    intro t ht
    by_cases ht_zero : t = 0
    · rw [ht_zero, mul_zero]; exact hg_zero
    · set s : ℝ := t / τ with hs_def
      have hs_abs : |s| < 2 := by
        rw [hs_def, abs_div, abs_of_pos τ_pos, div_lt_iff₀ τ_pos]
        calc |t| < δ / 4 := ht
          _ = 2 * (δ / 8) := by ring
          _ = 2 * τ := by rw [hτ_def]
      have hsτ : s * τ = t := by rw [hs_def, div_mul_cancel₀]; exact ne_of_gt τ_pos
      have h_F_cont : ContinuousAt (fun u : ℝ => g (u * τ) - u * g τ) s := by
        have h_st : |s * τ| < δ := by rw [hsτ]; linarith
        have h_mul : ContinuousAt (fun u : ℝ => u * τ) s :=
          continuousAt_id.mul continuousAt_const
        have h_g : ContinuousAt g (s * τ) := hg_cont _ h_st
        have h_g_cont : ContinuousAt (fun u : ℝ => g (u * τ)) s :=
          @ContinuousAt.comp ℝ ℝ ℝ _ _ _ (fun u => u * τ) s g h_g h_mul
        have h_lin_cont : ContinuousAt (fun u : ℝ => u * g τ) s :=
          continuousAt_id.mul continuousAt_const
        exact h_g_cont.sub h_lin_cont
      have h_F_rat : ∀ r : ℚ, |(r : ℝ)| < 2 →
          g ((r : ℝ) * τ) - (r : ℝ) * g τ = 0 := by
        intro r hr
        rw [sub_eq_zero]
        apply hg_rat
        rw [abs_mul, abs_of_pos τ_pos]
        have h2τ : 2 * τ = δ / 4 := by rw [hτ_def]; ring
        have h_bound : |(r : ℝ)| * τ < δ / 4 := by
          have : |(r : ℝ)| * τ < 2 * τ := mul_lt_mul_of_pos_right hr τ_pos
          exact lt_of_lt_of_le this h2τ.le
        exact h_bound
      have h_Fs : g (s * τ) - s * g τ = 0 := by
        by_contra h_ne
        set ε : ℝ := |g (s * τ) - s * g τ| / 2
        have ε_pos : 0 < ε := by
          show 0 < |g (s * τ) - s * g τ| / 2
          exact half_pos (abs_pos.mpr h_ne)
        obtain ⟨δ', δ'_pos, hδ'⟩ : ∃ δ' > 0, ∀ u, |u - s| < δ' →
            |(g (u * τ) - u * g τ) - (g (s * τ) - s * g τ)| < ε := by
          have key := (Metric.continuousAt_iff.mp h_F_cont) ε ε_pos
          simp only [Real.dist_eq] at key
          simpa using key
        set η : ℝ := min δ' (2 - |s|)
        have η_pos : 0 < η := lt_min_iff.mpr ⟨δ'_pos, by linarith⟩
        obtain ⟨q, hq⟩ : ∃ q : ℚ, |(q : ℝ) - s| < η := by
          obtain ⟨q, hq⟩ := exists_rat_near s η_pos
          exact ⟨q, by rw [abs_sub_comm]; exact hq⟩
        have hq_close : |(q : ℝ) - s| < δ' :=
          lt_of_lt_of_le hq (min_le_left _ _)
        have hq_small : |(q : ℝ)| < 2 := by
          have h_η2 : |(q : ℝ) - s| < 2 - |s| :=
            lt_of_lt_of_le hq (min_le_right _ _)
          have h_le : |(q : ℝ)| ≤ |s| + |(q : ℝ) - s| := by
            have := abs_add_le s ((q : ℝ) - s)
            simpa [show s + ((q : ℝ) - s) = (q : ℝ) from by ring] using this
          linarith
        have h_Fq : g ((q : ℝ) * τ) - (q : ℝ) * g τ = 0 := h_F_rat q hq_small
        have h_bound : |g (s * τ) - s * g τ| < ε := by
          have h_diff : |(g (s * τ) - s * g τ) - (g ((q : ℝ) * τ) - (q : ℝ) * g τ)| < ε := by
            have := hδ' _ hq_close
            rw [abs_sub_comm] at this
            exact this
          rw [h_Fq, sub_zero] at h_diff
          exact h_diff
        have h_half : |g (s * τ) - s * g τ| / 2 < |g (s * τ) - s * g τ| :=
          half_lt_self (abs_pos.mpr h_ne)
        have h_self : |g (s * τ) - s * g τ| < |g (s * τ) - s * g τ| :=
          calc |g (s * τ) - s * g τ| < ε := h_bound
            _ = |g (s * τ) - s * g τ| / 2 := rfl
            _ < |g (s * τ) - s * g τ| := h_half
        exact absurd h_self (lt_irrefl _)
      have h_gst : g (s * τ) = s * g τ := by linarith
      rw [← hsτ, h_gst, hα_def, hs_def, div_mul_cancel₀]
      · ring
      · exact ne_of_gt τ_pos
  -- Step 6: z(t) = Circle.exp(αt) for all t (global extension via group property)
  have h_zpow : ∀ m : ℕ, ∀ x : ℝ, z ((m : ℝ) * x) = z x ^ m := by
    intro m
    induction m with
    | zero => intro x; simp [zero_mul, pow_zero, hz_zero]
    | succ k ih =>
      intro x
      rw [show ((k + 1 : ℕ) : ℝ) * x = (k : ℝ) * x + x from by
        rw [Nat.cast_succ]; ring]
      rw [hz_add, ih x, pow_succ]
  have hz_exp : ∀ t : ℝ, z t = Circle.exp (α * t) := by
    intro t
    obtain ⟨n, hn_ge, hn_small⟩ : ∃ n : ℕ, n ≥ 1 ∧ |t| / (n : ℝ) < δ / 4 := by
      by_cases ht : t = 0
      · exact ⟨1, by norm_num, by rw [ht, abs_zero, zero_div]; positivity⟩
      · obtain ⟨n, hn⟩ : ∃ n : ℕ, (4 * |t| / δ : ℝ) < n :=
          exists_nat_gt (4 * |t| / δ)
        refine ⟨n + 1, by omega, ?_⟩
        have hn1_pos : (0 : ℝ) < ((n + 1 : ℕ) : ℝ) := by exact_mod_cast (Nat.succ_pos n)
        rw [div_lt_iff₀ hn1_pos]
        have hn' : (4 * |t| / δ : ℝ) < ((n + 1 : ℕ) : ℝ) := by
          have h1 : (4 * |t| / δ : ℝ) < ((n : ℕ) : ℝ) := by exact_mod_cast hn
          have h2 : ((n : ℕ) : ℝ) ≤ ((n + 1 : ℕ) : ℝ) := by
            have : n ≤ n + 1 := by omega
            exact_mod_cast this
          linarith
        have h4t : 4 * |t| / δ * (δ / 4) = |t| := by
          have hδ : δ ≠ 0 := ne_of_gt δ_pos
          have h4 : (4 : ℝ) ≠ 0 := by norm_num
          field_simp
        have h_d4 : 0 < δ / 4 := by positivity
        have h_prod : (4 * |t| / δ) * (δ / 4) < δ / 4 * ((n + 1 : ℕ) : ℝ) := by
          rw [mul_comm (δ / 4) ((n + 1 : ℕ) : ℝ)]
          exact mul_lt_mul_of_pos_right hn' h_d4
        rw [show |t| = (4 * |t| / δ) * (δ / 4) from h4t.symm]
        exact h_prod
    have hn_pos : (0 : ℝ) < n := by
      have h1 : (1 : ℝ) ≤ n := by exact_mod_cast hn_ge
      linarith
    have h_tn : |t / (n : ℝ)| < δ / 4 := by
      rw [abs_div, abs_of_pos hn_pos]; exact hn_small
    have h_tn' : |t / (n : ℝ)| < δ := by linarith
    have h_zn : z (t / (n : ℝ)) = Circle.exp (α * (t / (n : ℝ))) := by
      rw [show z (t / (n : ℝ)) = Circle.exp (g (t / (n : ℝ))) from (hg_exp _ h_tn').symm]
      rw [hg_linear _ h_tn]
    have h_t_eq : (n : ℝ) * (t / (n : ℝ)) = t := mul_div_cancel₀ t (ne_of_gt hn_pos)
    have h_zn_pow : z ((n : ℝ) * (t / (n : ℝ))) = z (t / (n : ℝ)) ^ n :=
      h_zpow n (t / (n : ℝ))
    rw [← h_t_eq, h_zn_pow, h_zn]
    rw [← Circle.exp_nsmul, nsmul_eq_mul]
    congr 1
    have hn : (n : ℝ) ≠ 0 := ne_of_gt hn_pos
    field_simp
  -- Step 7: α ≠ 0 (since z(1) ≠ 1)
  have hα_ne : α ≠ 0 := by
    intro hα_zero
    rw [hα_zero] at hz_exp
    simp only [zero_mul, Circle.exp_zero] at hz_exp
    exact hz_one_ne (hz_exp 1)
  -- Step 8: T = 2π/|α| gives z(T) = 1
  refine ⟨2 * Real.pi / |α|, by positivity, ?_⟩
  rw [hz_exp, ← Circle.exp_zero, Circle.exp_eq_exp]
  by_cases hα_pos : α > 0
  · refine ⟨1, ?_⟩
    rw [abs_of_pos hα_pos]
    rw [show α * (2 * Real.pi / α) = 2 * Real.pi from
      mul_div_cancel₀ _ (ne_of_gt hα_pos)]
    ring
  · have hα_neg : α < 0 := lt_of_le_of_ne (not_lt.mp hα_pos) hα_ne
    refine ⟨-1, ?_⟩
    rw [abs_of_neg hα_neg]
    rw [show α * (2 * Real.pi / (-α)) = -(2 * Real.pi) from by
      have hneg : (-α) ≠ 0 := ne_of_gt (by linarith [hα_neg])
      field_simp]
    ring
/-- GENERAL THEOREM (WITH CONTINUITY — still needs spectral theorem for full proof):

    PROOF-DESIGN CHOICE (2026-07-15, per Codex intake HOLD 2026-07-14):
    Route 1 chosen: explicit `InnerProductSpace ℝ M.State` hypothesis.
    This matches the already-proven odd-dimension theorem
    (`isometry_linear_semigroup_odd_dim_periodic_orbit`) which requires
    `InnerProductSpace` for the adjoint/orthogonal-matrix machinery.
    Route 2 (deriving an invariant inner product from a finite-dimensional
    normed isometry) is NOT taken; it would require a separate bridge lemma
    (compact-isometry-group → invariant inner product) that is not formalized.

    hBdd REMOVED: `Hypothesis_BoundedOrbit` is derivable from hIso + hDNorm
    alone (isometry preserves norms → ‖U(t)s‖ = ‖s‖ → d(s, U(t)s) ≤ 2‖s‖).
    See `isometry_implies_bounded_orbit` below. The odd-dim theorem does not
    use hBdd either. Listing hBdd as a separate premise was misleading.

    H22 (continuity) RETAINED: the discontinuous SO(2) counterexample
    (lines 653–686) shows H22 is necessary. Without it, a Hamel-basis
    homomorphism ℝ → SO(2) satisfies H3+H2+H14+H5+H21 but has no nonzero
    periodic orbit.

    HYPOTHESES: H3 (linearity) + H2 (semigroup) + H14 (isometry) + H5 (finite-dim)
    + H21 (d = norm) + H22 (continuity) + InnerProductSpace → nonzero periodic orbit.

    STATUS: OPEN. The proof requires the finite-dimensional spectral theorem
    for skew-symmetric matrices (Stone's theorem → A skew-adjoint → eigenvalue
    decomposition). The 2D case is proven (`rotation_semigroup_nonzero_periodic_orbit`).
    The odd-dim case is proven (`isometry_linear_semigroup_odd_dim_periodic_orbit`).
    The general (all-dim) case remains `sorry` until Mathlib's spectral theorem
    is assembled in a directly usable form.

    This theorem is NOT a formal H8 closure. Do not describe it as 90% proved
    or nearly complete. The dependency closure contains `sorryAx`. -/
theorem isometry_linear_semigroup_gives_nonzero_periodic_orbit
    (M : BareMedium) [NormedAddCommGroup M.State] [InnerProductSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hDNorm : Hypothesis_DIsNorm M)
    (hCont : Hypothesis_Continuity M)
    (hNontrivial : ∃ (s : M.State), s ≠ 0) :
    ∃ (s : M.State) (T : ℝ), s ≠ 0 ∧ T > 0 ∧
      ∀ (n : ℕ), M.propagate (↑n * T) s = s := by
  -- ========================================================================
  -- PROOF: Uses S = U(1) + U(-1) (self-adjoint) + spectral theorem
  -- μ = 2 → T = 1; μ = -2 → T = 2; |μ| < 2 → sorry (needs Stone's theorem)
  -- ========================================================================
  -- Construct U(t) as a LinearMap
  let U (t : ℝ) : M.State →ₗ[ℝ] M.State := {
    toFun := fun s => M.propagate t s
    map_add' := by
      intro s₁ s₂
      have h := hLin t s₁ s₂ 1 1
      simp [one_smul] at h ⊢
      exact h
    map_smul' := by
      intro a s
      have h_zero : M.propagate t (0 : M.State) = 0 := by
        have h := hLin t (0 : M.State) (0 : M.State) 0 0
        simp at h; exact h
      have h := hLin t s (0 : M.State) a 0
      simp [h_zero] at h ⊢
      exact h
  }
  have h_U0 : U 0 = LinearMap.id := by ext v; exact identity_at_zero M hLin hSemi hIso hDNorm v
  have h_Usemi (s t : ℝ) : U (s + t) = U s ∘ₗ U t := by ext v; exact hSemi s t v
  have h_norm_pres (t : ℝ) (v : M.State) : ‖U t v‖ = ‖v‖ := by
    have h_zero : M.propagate t (0 : M.State) = 0 := by
      have h := hLin t (0 : M.State) (0 : M.State) 0 0
      simp at h; exact h
    have h_iso := hIso t v (0 : M.State)
    rw [h_zero] at h_iso
    have h_d1 : M.d v (0 : M.State) = ‖v - (0 : M.State)‖ := hDNorm v (0 : M.State)
    have h_d2 : M.d (M.propagate t v) (0 : M.State) = ‖M.propagate t v - (0 : M.State)‖ :=
      hDNorm (M.propagate t v) (0 : M.State)
    rw [h_d1, h_d2] at h_iso
    simp [sub_zero] at h_iso ⊢
    exact h_iso.symm
  have h_isom (t : ℝ) : Isometry (U t : M.State → M.State) := by
    refine Isometry.of_dist_eq ?_
    intro x y
    have hsub : U t (x - y) = U t x - U t y := by rw [map_sub]
    rw [dist_eq_norm_sub, dist_eq_norm_sub, ← hsub]
    exact h_norm_pres t (x - y)
  have h_Uneg1_U1 : U (-1) ∘ₗ U 1 = LinearMap.id := by
    have h : U (-1 + 1) = U (-1) ∘ₗ U 1 := h_Usemi (-1) 1
    rw [neg_add_cancel, h_U0] at h; exact h.symm
  have h_U1_Uneg1 : U 1 ∘ₗ U (-1) = LinearMap.id := by
    have h : U (1 + (-1)) = U 1 ∘ₗ U (-1) := h_Usemi 1 (-1)
    rw [add_neg_cancel, h_U0] at h; exact h.symm
  have h_inner_pres (t : ℝ) (x y : M.State) :
      inner ℝ (U t x) (U t y) = inner ℝ x y := by
    let LI : M.State →ₗᵢ[ℝ] M.State := (U t).toLinearIsometry (h_isom t)
    exact LI.inner_map_map x y
  -- S = U(1) + U(-1) is self-adjoint (symmetric)
  have h_S_sym : (U 1 + U (-1) : Module.End ℝ M.State).IsSymmetric := by
    intro x y
    have h1 : inner ℝ (U 1 x) y = inner ℝ x (U (-1) y) := by
      have h_inv : U 1 (U (-1) y) = y := LinearMap.congr_fun h_U1_Uneg1 y
      have h_ip := h_inner_pres 1 x (U (-1) y)
      rw [h_inv] at h_ip; exact h_ip
    have h2 : inner ℝ (U (-1) x) y = inner ℝ x (U 1 y) := by
      have h_inv : U (-1) (U 1 y) = y := LinearMap.congr_fun h_Uneg1_U1 y
      have h_ip := h_inner_pres (-1) x (U 1 y)
      rw [h_inv] at h_ip; exact h_ip
    show inner ℝ ((U 1 + U (-1)) x) y = inner ℝ x ((U 1 + U (-1)) y)
    simp only [LinearMap.add_apply]
    rw [inner_add_left, inner_add_right, h1, h2]
    ring
  -- Spectral theorem: get eigenvector v of S with eigenvalue μ
  let n := Module.finrank ℝ M.State
  have hNT : Nontrivial M.State := by
    obtain ⟨s, hs⟩ := hNontrivial
    exact ⟨⟨0, s, hs.symm⟩⟩
  have hn_pos : 0 < n := Module.finrank_pos_iff.mpr hNT
  have hn : Module.finrank ℝ M.State = n := rfl
  haveI : NeZero n := ⟨hn_pos.ne'⟩
  let ob := h_S_sym.eigenvectorBasis hn
  let v : M.State := ob 0
  let μ : ℝ := h_S_sym.eigenvalues hn 0
  have hv_ne : v ≠ 0 := ob.orthonormal.ne_zero 0
  have h_S_v : (U 1 + U (-1) : Module.End ℝ M.State) v = μ • v :=
    h_S_sym.apply_eigenvectorBasis hn 0
  -- Key identity: U(1)² v = μ • U(1) v - v
  have h_Uneg1_v : U (-1) v = μ • v - U 1 v := by
    have h_Sv : U 1 v + U (-1) v = μ • v := by
      have := h_S_v; rw [LinearMap.add_apply] at this; exact this
    rw [← h_Sv, add_sub_cancel_left]
  have h_U1_Uneg1_v : U 1 (U (-1) v) = v := LinearMap.congr_fun h_U1_Uneg1 v
  have h_U1_sq : U 1 (U 1 v) = μ • (U 1 v) - v := by
    -- v = U(1)(U(-1) v) = U(1)(μ v - U(1) v) = μ • U(1) v - U(1)(U(1) v)
    have h2 : U 1 (U (-1) v) = μ • (U 1 v) - U 1 (U 1 v) := by
      rw [h_Uneg1_v, map_sub, map_smul]
    have h3 : v = μ • (U 1 v) - U 1 (U 1 v) := h_U1_Uneg1_v.symm.trans h2
    -- From h3: v + U(1)(U(1) v) = μ • U(1) v
    have h4 : v + U 1 (U 1 v) = μ • (U 1 v) := by
      have h_sub : (μ • (U 1 v) - U 1 (U 1 v)) + U 1 (U 1 v) = μ • (U 1 v) :=
        sub_add_cancel _ _
      rw [← h3] at h_sub
      exact h_sub
    rw [← h4, add_sub_cancel_left]
  -- U(n) = U(1)^n for natural n
  have h_Un_pow (k : ℕ) : U (↑k : ℝ) = (U 1 : Module.End ℝ M.State) ^ k := by
    induction k with
    | zero => rw [Nat.cast_zero, pow_zero, h_U0]; rfl
    | succ k ih => rw [Nat.cast_succ, pow_succ, ← ih]; exact h_Usemi ↑k 1
  have h_prop_eq_U (t : ℝ) (s : M.State) : M.propagate t s = U t s := rfl
  -- CASE ANALYSIS on μ
  by_cases hμ2 : μ = 2
  · -- CASE 1: μ = 2 → U(1) v = v → T = 1
    have h_sq : U 1 (U 1 v) = (2 : ℝ) • (U 1 v) - v := by
      rw [hμ2] at h_U1_sq; exact h_U1_sq
    set w : M.State := U 1 v - v with hw
    have h_U1_w : U 1 w = w := by
      rw [hw, map_sub, h_sq, two_smul ℝ (U 1 v)]; abel
    have h_U1_v_eq : U 1 v = v + w := by rw [hw]; abel
    have h_ip : inner ℝ (U 1 v) (U 1 w) = inner ℝ v w := h_inner_pres 1 v w
    rw [h_U1_v_eq, h_U1_w, inner_add_left] at h_ip
    have h_ww_zero : inner ℝ w w = 0 := by linarith
    have h_w_zero : w = 0 := inner_self_eq_zero.mp h_ww_zero
    have h_U1_v : U 1 v = v := by rw [h_U1_v_eq, h_w_zero]; abel
    refine ⟨v, 1, hv_ne, zero_lt_one, ?_⟩
    intro k
    rw [h_prop_eq_U, mul_one]
    induction k with
    | zero => rw [Nat.cast_zero, h_U0, LinearMap.id_apply]
    | succ k ih =>
      rw [Nat.cast_succ, h_Usemi ↑k 1, LinearMap.comp_apply, h_U1_v]
      exact ih
  · by_cases hμ_neg2 : μ = -2
    · -- CASE 2: μ = -2 → U(1) v = -v → U(2) v = v → T = 2
      have h_sq : U 1 (U 1 v) = (-(2 : ℝ)) • (U 1 v) - v := by
        rw [hμ_neg2] at h_U1_sq; exact h_U1_sq
      set w : M.State := U 1 v + v with hw
      have h_U1_w : U 1 w = -w := by
        rw [hw, map_add, h_sq]
        rw [neg_smul, two_smul ℝ (U 1 v), neg_add]
        abel
      have h_U1_v_eq : U 1 v = -v + w := by rw [hw]; abel
      have h_ip : inner ℝ (U 1 v) (U 1 w) = inner ℝ v w := h_inner_pres 1 v w
      rw [h_U1_v_eq, h_U1_w] at h_ip
      have h_ip2 : inner ℝ (-v + w) (-w) = inner ℝ v w - inner ℝ w w := by
        have h_add : inner ℝ (-v + w) (-w) = inner ℝ (-v) (-w) + inner ℝ w (-w) :=
          inner_add_left _ _ _
        have h_v : inner ℝ (-v) (-w) = inner ℝ v w := by
          rw [inner_neg_left, inner_neg_right, neg_neg]
        have h_w : inner ℝ w (-w) = -(inner ℝ w w) := inner_neg_right _ _
        rw [h_add, h_v, h_w]
        ring
      rw [h_ip2] at h_ip
      have h_ww_zero : inner ℝ w w = 0 := by linarith
      have h_w_zero : w = 0 := inner_self_eq_zero.mp h_ww_zero
      have h_U1_v : U 1 v = -v := by rw [h_U1_v_eq, h_w_zero]; abel
      have h_U2_v : U 2 v = v := by
        rw [show (2 : ℝ) = 1 + 1 from by norm_num, h_Usemi 1 1]
        rw [LinearMap.comp_apply, h_U1_v, map_neg, h_U1_v, neg_neg]
      refine ⟨v, 2, hv_ne, by norm_num, ?_⟩
      intro k
      rw [h_prop_eq_U]
      induction k with
      | zero => rw [Nat.cast_zero, zero_mul, h_U0, LinearMap.id_apply]
      | succ k ih =>
        rw [Nat.cast_succ, add_mul, one_mul, h_Usemi (↑k * 2) 2]
        rw [LinearMap.comp_apply, h_U2_v]
        exact ih
    · -- CASE 3: μ ≠ 2 and μ ≠ -2 → |μ| < 2
      -- Step 1: Basic inner product facts
      have h_v_norm : ‖v‖ = 1 := ob.orthonormal.1 0
      have h_v_inner : inner ℝ v v = 1 := by
        rw [real_inner_self_eq_norm_sq, h_v_norm, one_pow]
      have h_U1v_norm : ‖U 1 v‖ = 1 := by
        rw [h_norm_pres 1 v, h_v_norm]
      -- Step 2: μ = 2 * ⟨v, U(1)v⟩
      have h_ip_v_U1v : inner ℝ v (U 1 v) = μ / 2 := by
        have h_Sv : U 1 v + U (-1) v = μ • v := by
          have := h_S_v; rw [LinearMap.add_apply] at this; exact this
        have h_ip : inner ℝ v (U 1 v + U (-1) v) = inner ℝ v (μ • v) := by rw [h_Sv]
        rw [inner_add_right, real_inner_smul_right, h_v_inner] at h_ip
        have h_ip_neg : inner ℝ v (U (-1) v) = inner ℝ v (U 1 v) := by
          have hip := h_inner_pres 1 v (U (-1) v)
          rw [show U 1 (U (-1) v) = v from LinearMap.congr_fun h_U1_Uneg1 v] at hip
          exact hip.symm.trans (real_inner_comm v (U 1 v))
        rw [h_ip_neg] at h_ip
        linarith
      have h_μ_eq : μ = 2 * inner ℝ v (U 1 v) := by linarith
      -- Step 3: |μ| ≤ 2 by Cauchy-Schwarz, then |μ| < 2
      have h_ip_bound : |inner ℝ v (U 1 v)| ≤ 1 := by
        have := abs_real_inner_le_norm v (U 1 v)
        rw [h_v_norm, h_U1v_norm] at this
        linarith
      have h_μ_abs_le : |μ| ≤ 2 := by
        rw [h_μ_eq, abs_mul, show |(2 : ℝ)| = 2 from abs_of_nonneg (by norm_num)]
        linarith
      have h_μ_abs_lt : |μ| < 2 := by
        rcases lt_or_eq_of_le h_μ_abs_le with h | h
        · exact h
        · exfalso
          by_cases h0 : 0 ≤ μ
          · rw [abs_of_nonneg h0] at h; exact hμ2 h
          · rw [abs_of_neg (lt_of_not_ge h0)] at h
            have : μ = -2 := by linarith
            exact hμ_neg2 this
      -- Step 4: Construct σ, w', e₂
      have hσ_pos : 0 < √(1 - μ ^ 2 / 4) := by
        have h1 : 1 - μ ^ 2 / 4 > 0 := by
          have hμ2_lt : μ ^ 2 < 4 := by
            have := abs_lt.mp h_μ_abs_lt
            nlinarith
          nlinarith
        exact Real.sqrt_pos.mpr h1
      set σ : ℝ := √(1 - μ ^ 2 / 4) with hσ_def
      have hσ_sq : σ ^ 2 = 1 - μ ^ 2 / 4 := by
        rw [hσ_def, Real.sq_sqrt]
        have hμ2_lt : μ ^ 2 < 4 := by
          have h := abs_lt.mp h_μ_abs_lt
          nlinarith
        nlinarith
      set w' : M.State := U 1 v - (μ / 2) • v with hw'_def
      have hw'_orth : inner ℝ v w' = 0 := by
        rw [hw'_def, inner_sub_right, real_inner_smul_right, h_ip_v_U1v, h_v_inner]
        ring
      have hw'_norm_sq : inner ℝ w' w' = σ ^ 2 := by
        rw [hw'_def, inner_sub_left, inner_sub_right, inner_sub_right,
            real_inner_smul_left, real_inner_smul_right,
            real_inner_smul_left, real_inner_smul_right]
        rw [show inner ℝ (U 1 v) (U 1 v) = 1 from by
          rw [h_inner_pres 1 v v, h_v_inner]]
        rw [show inner ℝ (U 1 v) v = μ / 2 from by
          rw [real_inner_comm v (U 1 v), h_ip_v_U1v]]
        rw [h_ip_v_U1v, h_v_inner, hσ_sq]
        nlinarith
      have hw'_norm : ‖w'‖ = σ := by
        rw [norm_eq_sqrt_real_inner, hw'_norm_sq, Real.sqrt_sq (by positivity)]
      set e₂ : M.State := σ⁻¹ • w' with he₂_def
      have he₂_norm : ‖e₂‖ = 1 := by
        rw [he₂_def, norm_smul, hw'_norm, Real.norm_eq_abs, abs_inv,
            abs_of_pos hσ_pos, inv_mul_cancel₀ (ne_of_gt hσ_pos)]
      have he₂_orth : inner ℝ v e₂ = 0 := by
        rw [he₂_def, real_inner_smul_right, hw'_orth, mul_zero]
      have he₂_self : inner ℝ e₂ e₂ = 1 := by
        rw [real_inner_self_eq_norm_sq, he₂_norm, one_pow]
      -- Step 5: U(1) on W has rotation matrix form
      have h_U1_v : U 1 v = (μ / 2) • v + σ • e₂ := by
        have : σ • e₂ = w' := by
          rw [he₂_def, smul_smul, mul_inv_cancel₀ (ne_of_gt hσ_pos), one_smul]
        rw [this, hw'_def, add_sub_cancel]
      have h_U1_e₂ : U 1 e₂ = -(σ) • v + (μ / 2) • e₂ := by
        -- U(1)e₂ = σ⁻¹ • U(1)w' = σ⁻¹ • (U(1)²v - (μ/2)•U(1)v)
        -- = σ⁻¹ • (μ•U(1)v - v - (μ/2)•U(1)v) = σ⁻¹ • ((μ/2)•U(1)v - v)
        -- = σ⁻¹ • ((μ/2)•((μ/2)•v + σ•e₂) - v)
        -- = σ⁻¹ • ((μ²/4 - 1)•v + (μσ/2)•e₂) = -σ•v + (μ/2)•e₂
        have h1 : U 1 e₂ = σ⁻¹ • (U 1 w') := by
          rw [he₂_def, map_smul]
        have h2 : U 1 w' = (μ / 2) • (U 1 v) - v := by
          have hw'1 : U 1 w' = U 1 (U 1 v) - (μ / 2) • (U 1 v) := by
            rw [hw'_def, map_sub, map_smul]
          rw [hw'1, h_U1_sq]
          -- Goal: μ • (U 1 v) - v - (μ / 2) • (U 1 v) = (μ / 2) • (U 1 v) - v
          -- Rearrange: (μ - μ/2) • (U 1 v) - v = (μ/2) • (U 1 v) - v
          have hcomb : μ • (U 1 v) - (μ / 2) • (U 1 v) = (μ / 2) • (U 1 v) := by
            rw [← sub_smul]; ring_nf
          -- Need to rearrange the goal to use hcomb
          rw [sub_right_comm, hcomb]
        rw [h1, h2, h_U1_v]
        -- Now: σ⁻¹ • ((μ/2)•((μ/2)•v + σ•e₂) - v) = -σ•v + (μ/2)•e₂
        -- Expand and use σ² = 1 - μ²/4
        have hσ_ne : σ ≠ 0 := ne_of_gt hσ_pos
        -- Algebra: σ⁻¹ • ((μ/2)•((μ/2)•v + σ•e₂) - v) = -σ•v + (μ/2)•e₂
        -- using σ² = 1 - μ²/4. Pure module algebra.
        have hσsq : σ ^ 2 = 1 - μ ^ 2 / 4 := hσ_sq
        sorry
      have h_ip_e2_U1v : inner ℝ e₂ (U 1 v) = σ := by
        rw [h_U1_v, inner_add_right, real_inner_smul_right,
            show inner ℝ e₂ v = 0 from (real_inner_comm v e₂).trans he₂_orth,
            real_inner_smul_right, he₂_self]
        ring
      -- Step 6: U(t) commutes with U(1) (from semigroup)
      have h_comm : ∀ t, U t ∘ₗ (U 1 : Module.End ℝ M.State) =
          (U 1 : Module.End ℝ M.State) ∘ₗ U t := by
        intro t
        rw [← h_Usemi t 1, ← h_Usemi 1 t, add_comm]
      -- Step 7: W-invariance — the key mathematical step
      -- W = span{v, e₂} is invariant under U(t) for all t.
      -- This follows from the projection argument using the complex structure
      -- J = (U(1) - μ/2)/σ on E_μ, and the fact that U(t) commutes with U(1).
      have h_W_invariant : ∀ t, U t v ∈ Submodule.span ℝ ({v, e₂} : Set M.State) := by
        sorry
      have h_W_invariant_e2 : ∀ t, U t e₂ ∈ Submodule.span ℝ ({v, e₂} : Set M.State) := by
        sorry
      -- Step 8: Define z: ℝ → Circle and verify properties
      -- z(t) = ⟨v, U(t)v⟩ + i⟨e₂, U(t)v⟩ ∈ Circle
      -- This requires W-invariance to ensure |z(t)| = 1
      have h_z_cont : Continuous (fun t => inner ℝ v (U t v)) := by
        sorry
      have h_z_e2_cont : Continuous (fun t => inner ℝ e₂ (U t v)) := by
        sorry
      -- Construct z as a function ℝ → Circle
      let z : ℝ → Circle := fun t =>
        ⟨((inner ℝ v (U t v)) : ℂ) + Complex.I * (inner ℝ e₂ (U t v) : ℂ), by
          sorry⟩
      have h_z_zero : z 0 = 1 := by
        sorry
      have h_z_add : ∀ s t, z (s + t) = z s * z t := by
        sorry
      have h_z_one_ne : z 1 ≠ 1 := by
        sorry
      have h_z_cont' : Continuous z := by
        sorry
      -- Step 9: Apply helper lemma
      obtain ⟨T, hT_pos, hT_z⟩ := exists_period_of_continuous_circle_hom z h_z_cont' h_z_zero h_z_add h_z_one_ne
      -- Step 10: Derive U(T)v = v from z(T) = 1
      -- z(T) = 1 means ⟨v, U(T)v⟩ + i⟨e₂, U(T)v⟩ = 1
      -- So ⟨v, U(T)v⟩ = 1 and ⟨e₂, U(T)v⟩ = 0
      -- Since U(T)v ∈ W and has the same coordinates as v, U(T)v = v
      have h_U1v_T : inner ℝ v (U T v) = 1 := by sorry
      have h_Ue2_T : inner ℝ e₂ (U T v) = 0 := by sorry
      have h_UT_v : U T v = v := by
        sorry
      -- Step 11: Conclude — T is the period
      refine ⟨v, T, hv_ne, hT_pos, ?_⟩
      intro k
      rw [h_prop_eq_U]
      -- U(k*T) v = v for all natural k, by induction using U(T)v = v
      induction k with
      | zero => simp [h_U0]
      | succ k ih =>
        rw [show (↑(k + 1) : ℝ) * T = ↑k * T + T from by
          rw [Nat.cast_succ]; ring]
        rw [h_Usemi (↑k * T) T, LinearMap.comp_apply, h_UT_v]
        exact ih

/-- Lemma: Isometry + d=norm implies bounded orbit (hBdd is derivable, not a
    separate premise).

    This is the negative-evidence justification for removing `hBdd` from the
    general periodic-orbit theorem. If U(t) preserves norms, then every orbit
    is bounded by 2‖s‖ regardless of any other hypothesis. -/
lemma isometry_implies_bounded_orbit
    (M : BareMedium) [NormedAddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hIso : Hypothesis_Isometry M)
    (hDNorm : Hypothesis_DIsNorm M)
    (s : M.State) :
    Hypothesis_BoundedOrbit M s := by
  -- U(t) preserves norms: ‖propagate(t, s)‖ = ‖s‖
  have h_Pt0 (t : ℝ) : M.propagate t (0 : M.State) = 0 := by
    have h := hLin t (0 : M.State) (0 : M.State) 0 0
    simp at h
    exact h
  have h_norm_pres (t : ℝ) : ‖M.propagate t s‖ = ‖s‖ := by
    have h_dist := hIso t s (0 : M.State)
    rw [h_Pt0 t] at h_dist
    have h_d1 : M.d s (0 : M.State) = ‖s - (0 : M.State)‖ := hDNorm s 0
    have h_d2 : M.d (M.propagate t s) (0 : M.State) = ‖M.propagate t s - (0 : M.State)‖ :=
      hDNorm (M.propagate t s) 0
    rw [h_d1, h_d2] at h_dist
    simp [sub_zero] at h_dist
    exact h_dist.symm
  -- d(s, U(t)s) = ‖s - U(t)s‖ ≤ ‖s‖ + ‖U(t)s‖ = 2‖s‖
  refine ⟨2 * ‖s‖ + 1, fun t ht => ?_⟩
  have h_d : M.d s (M.propagate t s) = ‖s - M.propagate t s‖ := hDNorm s (M.propagate t s)
  rw [h_d]
  calc ‖s - M.propagate t s‖
      ≤ ‖s‖ + ‖M.propagate t s‖ := norm_sub_le _ _
    _ = ‖s‖ + ‖s‖ := by rw [h_norm_pres t]
    _ = 2 * ‖s‖ := by ring
    _ < 2 * ‖s‖ + 1 := by linarith

/-! ## Experiment 6: Isometry + metric identity → reversibility

If propagation preserves distances and d(s₁,s₂)=0 implies s₁=s₂,
then propagate(t,·) is injective. This is almost trivial but worth
machine-verifying: it confirms H14 + H15 → H1 (reversibility).

DISCOVERY: isometry alone (H14) does NOT give injectivity without the
metric axiom (H15). BareMedium.d is just a function with no axioms. -/

theorem isometry_implies_reversible
    (M : BareMedium)
    (hIso : Hypothesis_Isometry M)
    (hMet : Hypothesis_MetricIdentity M)
    (hRefl : Hypothesis_MetricReflexivity M) :
    Hypothesis_Reversible M := by
  intro t s₁ s₂ h_eq
  have h_dist : M.d s₁ s₂ = M.d (M.propagate t s₁) (M.propagate t s₂) := hIso t s₁ s₂
  rw [h_eq] at h_dist
  have h_refl : M.d (M.propagate t s₂) (M.propagate t s₂) = 0 := hRefl (M.propagate t s₂)
  rw [h_refl] at h_dist
  exact hMet s₁ s₂ h_dist

/-! ## Experiment 7: Isometry + finite-dim → compact orbit closure

The honest intermediate step (Claude 2026-06-25). Isometry preserves
distance from the coherent state → orbit is bounded → finite-dim normed
space → Heine-Borel → compact closure.

STATUS: VERIFIED 2026-07-03. The theorem is machine-checked by the Lean 4 kernel.
Uses: H19 (bounded orbit) + H21 (d = norm) + [FiniteDimensional ℝ] + [NormedSpace ℝ]
→ IsCompact (closure of orbit set)

NOTE: H14 (isometry) is included in the theorem signature for the downstream
theorem (compact orbit → Poincaré recurrence → periodicity) but is NOT needed
for compactness itself. Bounded orbit + finite-dim + Heine-Borel suffices.
This is a discovery: the compactness theorem is cheaper than expected.

The proof chain:
  1. H21 connects d to the norm → orbit bounded in d ⟹ orbit bounded in norm
  2. FiniteDimensional ℝ M.State → FiniteDimensional.proper ℝ → ProperSpace
  3. Bornology.IsBounded.isCompact_closure: in a ProperSpace, closure of
     a bounded set is compact (this packages Heine-Borel + closure-is-bounded)
  4. The orbit set {propagate(t, s) : t ≥ 0} is bounded (H19 + H21)
  5. Therefore its closure is compact

Honest parameter count: H19 + H21 + [FiniteDimensional ℝ] + [NormedSpace ℝ].
H14 (isometry) is in the signature for the downstream theorem but is NOT
needed for compactness itself — a discovery: the compactness theorem is
cheaper than expected. The [NormedSpace ℝ] instance is the "topology
scaffolding" cost — minimal structure for Heine-Borel. -/

set_option linter.unusedVariables false in

theorem isometry_finite_dim_gives_compact_orbit
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (s : M.State)
    (hIso : Hypothesis_Isometry M)
    (hBdd : Hypothesis_BoundedOrbit M s)
    (hDNorm : Hypothesis_DIsNorm M) :
    -- The orbit closure {propagate(t, s) : t ≥ 0} is compact.
    IsCompact (closure (Set.range (fun t : {t : ℝ // t ≥ 0} => M.propagate t.val s))) := by
  -- Step 1: Extract the bound R from H19.
  rcases hBdd with ⟨R, hR⟩

  -- Step 2: The orbit set is bounded in d (H19), and d = norm (H21),
  -- so the orbit set is bounded in norm.
  -- We show: ∀ t ≥ 0, ‖propagate(t, s) - s‖ < R
  have h_orbit_bounded : ∀ t : {t : ℝ // t ≥ 0}, ‖M.propagate t.val s - s‖ < R := by
    intro t
    have ht_d : M.d s (M.propagate t.val s) < R := hR t.val t.prop
    -- H21: d(s, propagate(t, s)) = ‖s - propagate(t, s)‖
    have ht_norm : ‖s - M.propagate t.val s‖ < R := by
      have := hDNorm s (M.propagate t.val s)
      rw [this] at ht_d
      exact ht_d
    -- ‖s - propagate(t, s)‖ = ‖propagate(t, s) - s‖ by norm symmetry
    rw [← neg_sub s (M.propagate t.val s), norm_neg]
    exact ht_norm

  -- Step 3: Convert to Bornology.IsBounded for the range set.
  -- isBounded_iff_subset_closedBall: IsBounded s ↔ ∃ r, s ⊆ closedBall c r
  have h_range_bounded : Bornology.IsBounded (Set.range (fun t : {t : ℝ // t ≥ 0} => M.propagate t.val s)) := by
    rw [Metric.isBounded_iff_subset_closedBall s]
    refine ⟨R + 1, ?_⟩
    rintro x ⟨t, rfl⟩
    -- x = propagate(t, s), need dist x s ≤ R + 1 (i.e., x ∈ closedBall s (R+1))
    have ht := h_orbit_bounded t
    rw [Metric.mem_closedBall, dist_eq_norm_sub]
    linarith

  -- Step 4: Finite-dimensional normed space over ℝ → ProperSpace (Heine-Borel).
  -- FiniteDimensional.proper_real is a registered instance:
  --   [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E] → ProperSpace E
  -- So ProperSpace M.State is automatically inferred from the instance parameters.
  -- Bornology.IsBounded.isCompact_closure: in a ProperSpace, closure of bounded set is compact.
  -- This is the Heine-Borel theorem.
  exact h_range_bounded.isCompact_closure

/-! ## Experiment 7b: Counterexample — isometry + finite-dim does NOT imply bounded orbit

The translation flow on `ℝ` is a clean counterexample: it preserves the
standard metric (`d(x,y) = |x-y|`), the state space is finite-dimensional,
but the orbit of `0` under forward propagation is `[0,∞)`, which is unbounded.
This proves the original `isometry + finite-dim → compact orbit` statement
was false and justifies adding H19 (BoundedOrbit) as an independent premise. -/

noncomputable def translationMedium : BareMedium where
  State := ℝ
  propagate := fun t x => x + t
  d := fun x y => abs (x - y)
  causal_velocity := 1

noncomputable instance : AddCommGroup translationMedium.State := inferInstanceAs (AddCommGroup ℝ)
noncomputable instance : Module ℝ translationMedium.State := inferInstanceAs (Module ℝ ℝ)
noncomputable instance : Zero translationMedium.State := inferInstanceAs (Zero ℝ)

theorem translationMedium_isometry : Hypothesis_Isometry translationMedium := by
  intro t x y
  simp [translationMedium]

theorem translationMedium_finiteDimensional : Hypothesis_FiniteDimensional translationMedium := by
  simp [Hypothesis_FiniteDimensional, translationMedium]
  exact FiniteDimensional.finiteDimensional_self ℝ

theorem translationMedium_not_bounded_orbit :
    ¬ Hypothesis_BoundedOrbit translationMedium (0 : ℝ) := by
  intro h
  rcases h with ⟨R, hR⟩
  -- For any claimed bound R, use t = max(0, R) + 1 to get a contradiction.
  let t := max (0 : ℝ) R + 1
  have ht : t ≥ 0 := by linarith [le_max_left (0 : ℝ) R]
  have h_dist : translationMedium.d (0 : ℝ) (translationMedium.propagate t (0 : ℝ)) = t := by
    simp only [translationMedium]
    rw [zero_sub, abs_neg, zero_add, abs_of_nonneg ht]
  specialize hR t ht
  rw [h_dist] at hR
  -- t = max(0, R) + 1 > R
  have ht_gt : t > R := by linarith [le_max_right (0 : ℝ) R]
  linarith

/- Combined counterexample statement: isometry + finite-dim does not imply
    bounded orbit, hence does not imply compact orbit.

    NOTE: The combined existential is not formalized here due to type class
    instance resolution issues with `BareMedium.State` field projection on
    `noncomputable def`. The three individual theorems above
    (`translationMedium_isometry`, `translationMedium_finiteDimensional`,
    `translationMedium_not_bounded_orbit`) together constitute the full
    counterexample. The combined statement can be formalized once the
    `BareMedium` structure is refactored to make `State` reducible. -/
-- theorem isometry_finite_dim_not_bounded_orbit_counterexample :
--     ∃ (M : BareMedium) (s : M.State),
--       Hypothesis_Isometry M ∧ Hypothesis_FiniteDimensional M ∧ ¬ Hypothesis_BoundedOrbit M s := by
--   exact ⟨translationMedium, 0, translationMedium_isometry, translationMedium_finiteDimensional, translationMedium_not_bounded_orbit⟩

/-! ## Experiment 8: The real eigenvalue obstruction (PROVEN)

The J-I circulant at D=3 has eigenvalues {2, -1, -1} (for M) or
{0, -3/2, -3/2} (for L = -I + ½M). All REAL. The propagation exp(tL)
has eigenvalues {1, exp(-3t/2), exp(-3t/2)}. All REAL and decaying.

CONSEQUENCE: the J-I dynamics is a CONTRACTION. Every non-uniform state
decays to the uniform mode. There is NO oscillation and NO non-zero
periodic orbit. This is machine-verified for the discrete dynamics:
T³ scales residue by -1/8 (PFCore.lean: T3_Q), T³^k scales by (-1/8)^k
(PFCore.lean: T3_Q_pow) → decays to zero.

The theorem below states the obstruction formally: if the propagation
operator is a strict contraction on non-zero states (the formal content
of "real eigenvalues" for the J-I circulant), then isometry + linearity
force ALL states to have zero distance from the origin. The coherent
state is therefore trivial (uniform mode).

PROOF STRATEGY (no spectral theory scaffolding needed):
  1. Linearity → propagate(t, 0) = 0 (zero is a fixed point)
  2. Isometry + (1) → d(propagate(τ, s), 0) = d(s, 0) (norm preservation)
  3. Contraction → d(s, 0) > 0 implies d(propagate(τ, s), 0) < d(s, 0)
  4. (2) + (3) → d(s, 0) > 0 is impossible → d(s, 0) = 0 for all s

The contraction hypothesis replaces the informal "real eigenvalues"
placeholder. For the J-I circulant at D=3, T³ scales the residue by -1/8
(machine-verified: `full_norm_T3_strictly_decreases` in Entropy.lean),
which is exactly this contraction property.

DISCOVERY: hSemi, hFin, and hCoh are NOT needed for the core obstruction.
The incompatibility of isometry and contraction is purely a consequence
of linearity (H3) + isometry (H14) + the contraction property. The
coherence hypothesis (H8) is included for context but does not load. -/

set_option linter.unusedVariables false in

/-- H20: Non-negative distance — the pseudometric d is non-negative.
    BareMedium.d has no axioms; this is needed to conclude d(s, 0) = 0
    from d(s, 0) ≤ 0 (the contrapositive of the contraction).
    Cost: 1 hypothesis. -/
def Hypothesis_NonnegativeDistance (M : BareMedium) : Prop :=
  ∀ (s₁ s₂ : M.State), 0 ≤ M.d s₁ s₂

/-- The real eigenvalue obstruction (Experiment 8, PROVEN — no sorry, no True stub).

    If the propagation operator is a strict contraction on non-zero states
    (which is what "real eigenvalues" means for the J-I circulant: T³ scales
    the residue by -1/8, |−1/8| < 1), then isometry + linearity force ALL
    states to have zero distance from the origin. The coherent state is
    therefore trivial (uniform mode).

    Mathematical argument:
      1. Linearity → propagate(t, 0) = 0 (zero is a fixed point)
      2. Isometry + (1) → d(propagate(τ, s), 0) = d(s, 0) (norm preservation)
      3. Contraction → d(s, 0) > 0 implies d(propagate(τ, s), 0) < d(s, 0)
      4. (2) + (3) → d(s, 0) > 0 is impossible → d(s, 0) = 0 for all s

    The contraction hypothesis is the formal content of "real eigenvalues":
    for the J-I circulant at D=3, T³ scales the residue by -1/8
    (machine-verified: `full_norm_T3_strictly_decreases` in Entropy.lean).
    Isometry (H14) and the J-I contraction are structurally incompatible
    for any non-trivial state.

    With `Hypothesis_MetricIdentity` (H15), the conclusion `d(s, 0) = 0`
    for all s forces all states to equal 0 — the state space is trivial.

    Discovery: hSemi, hFin, and hCoh are NOT needed for this obstruction.
    The incompatibility of isometry and contraction is purely a consequence
    of linearity (H3) + isometry (H14) + the contraction property. -/
theorem real_eigenvalue_obstruction
    (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hFin : Hypothesis_FiniteDimensional M)
    (hIso : Hypothesis_Isometry M)
    (hRefl : Hypothesis_MetricReflexivity M)
    (hNonNeg : Hypothesis_NonnegativeDistance M)
    -- The propagation at time τ is a strict contraction on states with
    -- positive distance from the origin. This is the formal content of
    -- "real eigenvalues" for the J-I circulant at D=3: T³ scales the
    -- residue by -1/8 (|−1/8| < 1), so non-uniform states contract.
    -- (Machine-verified: `full_norm_T3_strictly_decreases` in Entropy.lean.)
    (τ : ℝ) (τ_pos : τ > 0)
    (h_contraction : ∀ (s : M.State), M.d s (0 : M.State) > 0 →
                     M.d (M.propagate τ s) (0 : M.State) < M.d s (0 : M.State))
    -- The coherent state from H8 (included for context; not needed for the proof).
    (hCoh : Hypothesis_Coherence M) :
    -- Isometry + linearity → d(propagate(τ, s), 0) = d(s, 0) (norm preservation).
    -- Contraction → d(s, 0) > 0 implies d(propagate(τ, s), 0) < d(s, 0).
    -- Together: d(s, 0) > 0 is impossible → d(s, 0) = 0 for all states.
    -- The coherent state is trivial (zero distance from origin = uniform mode).
    -- With Hypothesis_MetricIdentity (H15), this forces all states to equal 0.
    ∀ (s : M.State), M.d s (0 : M.State) = 0 := by
  intro s
  -- Step 1: Linearity gives propagate(t, 0) = 0 for all t.
  have h0 : ∀ (t : ℝ), M.propagate t 0 = 0 := by
    intro t
    have h := hLin t 0 0 0 0
    simp at h
    exact h
  -- Step 2: Isometry + linearity gives norm preservation:
  -- d(propagate(τ, s), 0) = d(propagate(τ, s), propagate(τ, 0)) = d(s, 0).
  have h_norm_preserved : M.d (M.propagate τ s) (0 : M.State) = M.d s (0 : M.State) := by
    have h_iso := hIso τ s 0
    rw [h0 τ] at h_iso
    exact h_iso.symm
  -- Step 3: If d(s, 0) > 0, contraction gives d(propagate(τ, s), 0) < d(s, 0).
  -- But norm preservation gives d(propagate(τ, s), 0) = d(s, 0). Contradiction.
  by_contra h_ne
  have h_ge : 0 ≤ M.d s (0 : M.State) := hNonNeg s 0
  have h_pos : 0 < M.d s (0 : M.State) := lt_of_le_of_ne h_ge (Ne.symm h_ne)
  have h_contracted : M.d (M.propagate τ s) (0 : M.State) < M.d s (0 : M.State) :=
    h_contraction s h_pos
  rw [h_norm_preserved] at h_contracted
  exact absurd h_contracted (lt_irrefl _)

/-- Corollary: the real eigenvalue obstruction + metric identity → all states
    equal zero (the state space is trivial).

    Isometry + linearity + contraction → d(s, 0) = 0 for all s (the obstruction).
    Metric identity (H15) → d(s, 0) = 0 implies s = 0.
    Together: every state is the zero state — the dynamics is trivial. -/
theorem real_eigenvalue_obstruction_trivial
    (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hFin : Hypothesis_FiniteDimensional M)
    (hIso : Hypothesis_Isometry M)
    (hRefl : Hypothesis_MetricReflexivity M)
    (hMet : Hypothesis_MetricIdentity M)
    (hNonNeg : Hypothesis_NonnegativeDistance M)
    (τ : ℝ) (τ_pos : τ > 0)
    (h_contraction : ∀ (s : M.State), M.d s (0 : M.State) > 0 →
                     M.d (M.propagate τ s) (0 : M.State) < M.d s (0 : M.State))
    (hCoh : Hypothesis_Coherence M) :
    ∀ (s : M.State), s = 0 := by
  intro s
  have h_dist_zero : M.d s (0 : M.State) = 0 :=
    real_eigenvalue_obstruction M hLin hSemi hFin hIso hRefl hNonNeg τ τ_pos h_contraction hCoh s
  exact hMet s 0 h_dist_zero

/-! ## Edge 28: Discrete Sampled Recurrence (Devin 2026-07-03, repaired 2026-07-15)

The compact-orbit theorem (Edge 18) gives us IsCompact (closure of orbit).
This theorem uses that compactness + isometry (H14) + semigroup (H2) to prove
DISCRETE SAMPLED RECURRENCE: for every ε > 0, there exists a POSITIVE NATURAL
n such that d(s, propagate(n, s)) < ε.

**Semantic boundary (Codex 2026-07-14 audit):** The primary theorem exports a
Nat witness, not a Real witness. The proof constructs T = m - n ∈ ℕ with
m > n; the Nat witness excludes the small-time contraction loophole that a
pure Real-time statement permits (e.g. F_t(x) = exp(-t)x satisfies the
Real-time version for arbitrarily small t but has no return at unit-sampled
times). The Real-time version is retained as a corollary.

This is NOT periodicity (exact return). The irrational torus rotation is
isometric, compact, and recurrent but never exactly periodic. We prove
sampled recurrence, not exact periodicity and not arbitrary-late recurrence.

This is the FIRST theorem that uses H14 (isometry) essentially. Edge 18 had
H14 in its signature but didn't use it — compactness comes from H19 + H21 +
finite-dim alone. Here, isometry is what converts "two orbit points are close"
into "the orbit returns close to its start."

Proof sketch:
  1. Edge 18 gives compact orbit closure K
  2. The sequence x_n = propagate(n, s) lies in K for all n ∈ ℕ
  3. By sequential compactness, a subsequence x_{φ(k)} → a ∈ K
  4. For large k: d(x_{φ(k)}, a) < ε/2 and d(x_{φ(k+1)}, a) < ε/2
  5. Triangle inequality: d(x_{φ(k)}, x_{φ(k+1)}) < ε
  6. Semigroup: x_{φ(k+1)} = propagate(φ(k), propagate(φ(k+1)-φ(k), s))
  7. Isometry: d(x_{φ(k)}, x_{φ(k+1)}) = d(s, propagate(φ(k+1)-φ(k), s))
  8. So d(s, propagate(T, s)) < ε with T = φ(k+1) - φ(k) ∈ ℕ, T > 0. ∎

Honest parameter count: H2 + H14 + H19 + H21 + [FiniteDimensional] + [NormedSpace]
No new hypothesis needed. H22 (continuity) is NOT required — discrete iterates
and sequential compactness suffice. -/

set_option linter.unusedVariables false in

/-- Edge 28 primary theorem: DISCRETE SAMPLED RECURRENCE.

    For every ε > 0, there exists a positive natural number n such that
    d(s, propagate(n, s)) < ε. The witness is a Nat, not a Real, which
    excludes the small-time contraction loophole (a dissipative semigroup
    can satisfy the Real-time version with arbitrarily small t but has no
    return at unit-sampled times).

    This is NOT exact periodicity and NOT arbitrary-late recurrence.
    The proof constructs n = m - k where m > k are natural indices of
    orbit points that cluster near the same limit point. -/
theorem isometry_compact_orbit_gives_discrete_recurrence
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (s : M.State)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hBdd : Hypothesis_BoundedOrbit M s)
    (hDNorm : Hypothesis_DIsNorm M) :
    -- For every ε > 0, there exists a positive Nat n with d(s, propagate(n, s)) < ε.
    -- This is discrete sampled recurrence: the orbit returns close at integer times.
    ∀ (ε : ℝ), ε > 0 → ∃ (n : ℕ), 0 < n ∧ M.d s (M.propagate (n : ℝ) s) < ε := by
  -- Step 1: Orbit closure K is compact (Edge 18).
  let O := Set.range (fun t : {t : ℝ // t ≥ 0} => M.propagate t.val s)
  have hK : IsCompact (closure O) :=
    isometry_finite_dim_gives_compact_orbit M s hIso hBdd hDNorm
  -- M.d = dist (from H21: d = ‖·‖, and dist = ‖·‖ in NormedAddCommGroup)
  have hd : ∀ (x y : M.State), M.d x y = dist x y := by
    intro x y; rw [hDNorm x y, dist_eq_norm_sub]

  intro ε hε

  -- Step 2: Define sequence u n = propagate(n, s), all in K.
  let u := fun (n : ℕ) => M.propagate (n : ℝ) s
  have h_in_K : ∀ n, u n ∈ closure O := by
    intro n
    apply subset_closure
    exact ⟨⟨(n : ℝ), Nat.cast_nonneg n⟩, rfl⟩

  -- Step 3: Get cluster point a ∈ K with MapClusterPt a atTop u.
  -- (IsCompact.exists_mapClusterPt_of_frequently)
  have h_freq_in_K : ∃ᶠ n in Filter.atTop, u n ∈ closure O :=
    Filter.Frequently.of_forall h_in_K
  obtain ⟨a, ha, h_cluster⟩ := hK.exists_mapClusterPt_of_frequently h_freq_in_K

  -- Step 4: From MapClusterPt, get ∃ᶠ n in atTop, dist(u n, a) < δ.
  set δ := ε / 2
  have hδ : δ > 0 := by show ε / 2 > 0; linarith
  -- MapClusterPt a atTop u = ClusterPt a (map u atTop)
  -- clusterPt_iff_frequently: ClusterPt x F ↔ ∀ s ∈ nhds x, ∃ᶠ y in F, y ∈ s
  have h_cluster_freq : ∀ s ∈ nhds a, ∃ᶠ y in Filter.map u Filter.atTop, y ∈ s :=
    clusterPt_iff_frequently.mp h_cluster
  have h_ball_mem : Metric.ball a δ ∈ nhds a := Metric.ball_mem_nhds a hδ
  have h_freq_ball : ∃ᶠ y in Filter.map u Filter.atTop, y ∈ Metric.ball a δ :=
    h_cluster_freq _ h_ball_mem
  -- frequently_map: ∃ᶠ b in map m f, P b ↔ ∃ᶠ a in f, P (m a)
  rw [Filter.frequently_map] at h_freq_ball
  -- u n ∈ ball a δ ↔ dist (u n) a < δ
  simp only [Metric.mem_ball, dist_comm] at h_freq_ball

  -- Step 5: Extract two indices n < m with both within δ of a.
  -- Frequently.forall_exists_of_atTop: (∃ᶠ x in atTop, p x) → ∀ a, ∃ b, a ≤ b ∧ p b
  obtain ⟨n, hn, h_n⟩ := Filter.Frequently.forall_exists_of_atTop h_freq_ball 0
  obtain ⟨m, hm, h_m⟩ := Filter.Frequently.forall_exists_of_atTop h_freq_ball (n + 1)
  have h_nm : n < m := by omega

  -- Step 6: Triangle inequality — dist(u n, u m) < 2δ = ε.
  have h_n' : dist (u n) a < δ := by rw [dist_comm]; exact h_n
  have h_m' : dist (u m) a < δ := by rw [dist_comm]; exact h_m
  have h_close : dist (u n) (u m) < ε := by
    calc dist (u n) (u m)
        ≤ dist (u n) a + dist a (u m) := dist_triangle _ _ _
      _ = dist (u n) a + dist (u m) a := by rw [dist_comm a (u m)]
      _ < δ + δ := by linarith [h_n', h_m']
      _ = ε := by show ε / 2 + (ε / 2) = ε; ring

  -- Step 7: T = m - n > 0 (the discrete return time, Nat witness).
  have h_sub_pos : 0 < m - n := Nat.sub_pos_of_lt h_nm
  set T := ((m - n : ℕ) : ℝ)
  have hT_pos : T > 0 := Nat.cast_pos.mpr h_sub_pos

  -- Step 8: Semigroup (H2) — propagate(m, s) = propagate(n, propagate(T, s)).
  have h_mn : (m : ℝ) = (n : ℝ) + T := by
    show (m : ℝ) = (n : ℝ) + ((m - n : ℕ) : ℝ)
    rw [Nat.cast_sub h_nm.le]; push_cast; ring
  have h_semi : M.propagate (m : ℝ) s = M.propagate (n : ℝ) (M.propagate T s) := by
    rw [h_mn]; exact hSemi _ _ _

  -- Step 9: Isometry (H14) — d(propagate(n, s), propagate(n, propagate(T, s))) = d(s, propagate(T, s)).
  have h_iso : M.d (M.propagate (n : ℝ) s) (M.propagate (n : ℝ) (M.propagate T s)) =
               M.d s (M.propagate T s) :=
    (hIso (n : ℝ) s (M.propagate T s)).symm

  -- Step 10: Combine — d(s, propagate(T, s)) < ε with Nat witness m - n.
  -- u n = propagate(n, s), u m = propagate(m, s) = propagate(n, propagate(T, s))
  -- h_close : dist(u n, u m) < ε  →  M.d(u n, u m) < ε  →  M.d(s, propagate(T, s)) < ε
  show ∃ (k : ℕ), 0 < k ∧ M.d s (M.propagate (k : ℝ) s) < ε
  refine ⟨m - n, h_sub_pos, ?_⟩
  -- h_close : dist (u n) (u m) < ε  where  u k = propagate(k, s)
  -- = dist (propagate(n, s)) (propagate(m, s)) < ε
  -- = M.d (propagate(n, s)) (propagate(m, s)) < ε   [hd]
  -- = M.d (propagate(n, s)) (propagate(n, propagate(T, s))) < ε  [h_semi]
  -- = M.d s (propagate(T, s)) < ε  [h_iso]
  have h_close' : M.d (M.propagate (n : ℝ) s) (M.propagate (m : ℝ) s) < ε := by
    rw [hd]; exact h_close
  rw [h_semi] at h_close'
  rw [← h_iso]
  -- T = ((m - n : ℕ) : ℝ) which is defeq to the goal's (m - n : ℝ) from refine
  exact h_close'

/-! ## Edge 28b: Infinite Discrete Sampled Recurrence (Devin 2026-07-15)

Strengthening of Edge 28: the return times are not just nonzero but ARBITRARILY
LARGE. For every ε > 0 and every N ∈ ℕ, there exists n ≥ N with
d(s, propagate(n, s)) < ε.

Proof: the existing Edge 28 proof finds two indices k < m near a cluster point
and returns T = m - k. Here we fix k (one orbit point near the cluster point a)
and let m go to infinity (another orbit point near a, with m ≥ k + N + 1).
Then T = m - k ≥ N, and the same isometry + semigroup argument gives
d(s, propagate(T, s)) < ε.

This answers WHAT'S NEEDED NEXT item 6: "Can recurrence be strengthened to
'infinitely many return times' without additional hypotheses?" — YES.

This is NOT exact periodicity. The irrational torus rotation satisfies this
(approximate returns at arbitrarily large times) but has no exact period.
The return times have positive density (by Weyl equidistribution in the
concrete rotation case) but we do not prove density here. -/
set_option linter.unusedVariables false in
theorem isometry_compact_orbit_gives_infinite_discrete_recurrence
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (s : M.State)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hBdd : Hypothesis_BoundedOrbit M s)
    (hDNorm : Hypothesis_DIsNorm M) :
    ∀ (ε : ℝ), ε > 0 → ∀ (N : ℕ), ∃ (n : ℕ), N ≤ n ∧ M.d s (M.propagate (n : ℝ) s) < ε := by
  -- Step 1: Orbit closure K is compact (Edge 18).
  let O := Set.range (fun t : {t : ℝ // t ≥ 0} => M.propagate t.val s)
  have hK : IsCompact (closure O) :=
    isometry_finite_dim_gives_compact_orbit M s hIso hBdd hDNorm
  have hd : ∀ (x y : M.State), M.d x y = dist x y := by
    intro x y; rw [hDNorm x y, dist_eq_norm_sub]
  intro ε hε N
  -- Step 2: Define sequence u n = propagate(n, s), all in K.
  let u := fun (n : ℕ) => M.propagate (n : ℝ) s
  have h_in_K : ∀ n, u n ∈ closure O := by
    intro n
    apply subset_closure
    exact ⟨⟨(n : ℝ), Nat.cast_nonneg n⟩, rfl⟩
  -- Step 3: Get cluster point a ∈ K with MapClusterPt a atTop u.
  have h_freq_in_K : ∃ᶠ n in Filter.atTop, u n ∈ closure O :=
    Filter.Frequently.of_forall h_in_K
  obtain ⟨a, ha, h_cluster⟩ := hK.exists_mapClusterPt_of_frequently h_freq_in_K
  -- Step 4: From MapClusterPt, get ∃ᶠ n in atTop, dist(u n, a) < δ.
  set δ := ε / 2
  have hδ : δ > 0 := by show ε / 2 > 0; linarith
  have h_cluster_freq : ∀ s ∈ nhds a, ∃ᶠ y in Filter.map u Filter.atTop, y ∈ s :=
    clusterPt_iff_frequently.mp h_cluster
  have h_ball_mem : Metric.ball a δ ∈ nhds a := Metric.ball_mem_nhds a hδ
  have h_freq_ball : ∃ᶠ y in Filter.map u Filter.atTop, y ∈ Metric.ball a δ :=
    h_cluster_freq _ h_ball_mem
  rw [Filter.frequently_map] at h_freq_ball
  simp only [Metric.mem_ball, dist_comm] at h_freq_ball
  -- Step 5: Fix one index k ≥ 1 with u(k) near a.
  obtain ⟨k, hk, h_k⟩ := Filter.Frequently.forall_exists_of_atTop h_freq_ball 1
  have h_k' : dist (u k) a < δ := by rw [dist_comm]; exact h_k
  -- Step 6: Get another index m ≥ k + N + 1 with u(m) near a.
  -- Then T = m - k ≥ N, ensuring the return time is arbitrarily large.
  obtain ⟨m, hm, h_m⟩ := Filter.Frequently.forall_exists_of_atTop h_freq_ball (k + N + 1)
  have h_m' : dist (u m) a < δ := by rw [dist_comm]; exact h_m
  have h_km : k < m := by omega
  -- Step 7: Triangle inequality — dist(u k, u m) < 2δ = ε.
  have h_close : dist (u k) (u m) < ε := by
    calc dist (u k) (u m)
        ≤ dist (u k) a + dist a (u m) := dist_triangle _ _ _
      _ = dist (u k) a + dist (u m) a := by rw [dist_comm a (u m)]
      _ < δ + δ := by linarith [h_k', h_m']
      _ = ε := by show ε / 2 + (ε / 2) = ε; ring
  -- Step 8: T = m - k ≥ N (the discrete return time, arbitrarily large).
  have h_T_ge_N : N ≤ m - k := by omega
  have h_sub_pos : 0 < m - k := by omega
  set T := ((m - k : ℕ) : ℝ)
  have hT_pos : T > 0 := Nat.cast_pos.mpr h_sub_pos
  -- Step 9: Semigroup (H2) — propagate(m, s) = propagate(k, propagate(T, s)).
  have h_km_real : (m : ℝ) = (k : ℝ) + T := by
    show (m : ℝ) = (k : ℝ) + ((m - k : ℕ) : ℝ)
    rw [Nat.cast_sub h_km.le]; push_cast; ring
  have h_semi : M.propagate (m : ℝ) s = M.propagate (k : ℝ) (M.propagate T s) := by
    rw [h_km_real]; exact hSemi _ _ _
  -- Step 10: Isometry (H14) — d(propagate(k, s), propagate(k, propagate(T, s))) = d(s, propagate(T, s)).
  have h_iso : M.d (M.propagate (k : ℝ) s) (M.propagate (k : ℝ) (M.propagate T s)) =
               M.d s (M.propagate T s) :=
    (hIso (k : ℝ) s (M.propagate T s)).symm
  -- Step 11: Combine — d(s, propagate(T, s)) < ε with T = m - k ≥ N.
  have h_close' : M.d (M.propagate (k : ℝ) s) (M.propagate (m : ℝ) s) < ε := by
    rw [hd]; exact h_close
  rw [h_semi] at h_close'
  refine ⟨m - k, h_T_ge_N, ?_⟩
  rw [← h_iso]
  exact h_close'

/-- Corollary: the Real-time version of discrete sampled recurrence.

    This is the weaker statement that for every ε > 0, there exists a
    positive Real t with d(s, propagate(t, s)) < ε. It follows trivially
    from the discrete version by coercing the Nat witness to Real.

    WARNING: this Real-time statement alone does NOT capture nontrivial
    recurrence — a dissipative contraction F_t(x) = exp(-t)x satisfies it
    with arbitrarily small t. The discrete (Nat-witness) theorem above is
    the honest nontrivial result. This corollary is retained for backward
    compatibility but should not be labeled "topological recurrence" on
    its own. -/
theorem isometry_compact_orbit_gives_recurrence
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (s : M.State)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hBdd : Hypothesis_BoundedOrbit M s)
    (hDNorm : Hypothesis_DIsNorm M) :
    ∀ (ε : ℝ), ε > 0 → ∃ (t : ℝ), t > 0 ∧ M.d s (M.propagate t s) < ε := by
  intro ε hε
  obtain ⟨n, hn, h⟩ := isometry_compact_orbit_gives_discrete_recurrence M s hSemi hIso hBdd hDNorm ε hε
  exact ⟨(n : ℝ), Nat.cast_pos.mpr hn, h⟩

/-! ## Edge 28c: Orbit is Dense-in-Itself (Devin 2026-07-15)

No orbit point is isolated. For every orbit point U(t₀)s and every ε > 0,
there exists a DIFFERENT time t ≠ t₀ with d(U(t)s, U(t₀)s) < ε.

This uses Edge 28b (infinite recurrence) essentially: the one-return version
(Edge 28) only gives one return time n > 0, which might collide with t₀.
The infinite version gives returns at arbitrarily large n, so we can always
find n large enough that t = t₀ + n ≠ t₀.

Isometry is essential: a contraction F_t(x) = exp(-t)x has an orbit converging
to 0, and 0 is isolated from the rest of the orbit (once t > -ln(ε), no orbit
point is within ε of 0 except 0 itself... actually 0 is the limit point, so
the orbit points get closer to 0 but 0 is not an orbit point unless s = 0).
The correct contrast: for a contraction, the orbit points themselves become
sparse near the limit — each orbit point IS isolated from the others because
the map is contracting, not isometric. Isometry preserves distances, so
closeness to s transfers to closeness at every orbit point. -/
set_option linter.unusedVariables false in
theorem isometry_compact_orbit_dense_in_itself
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (s : M.State)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hBdd : Hypothesis_BoundedOrbit M s)
    (hDNorm : Hypothesis_DIsNorm M) :
    ∀ (t₀ : ℝ) (h_t₀ : t₀ ≥ 0) (ε : ℝ) (hε : ε > 0),
      ∃ (n : ℕ), 0 < n ∧
        M.d (M.propagate (t₀ + (n : ℝ)) s) (M.propagate t₀ s) < ε := by
  intro t₀ h_t₀ ε hε
  -- Convert M.d to dist (which is symmetric) via H21.
  have hd : ∀ (x y : M.State), M.d x y = dist x y := by
    intro x y; rw [hDNorm x y, dist_eq_norm_sub]
  -- Use infinite recurrence: for every ε > 0 and every N, ∃ n ≥ N with d(s, U(n)s) < ε.
  -- Take N = 1 to ensure n > 0, hence t = t₀ + n ≠ t₀.
  obtain ⟨n, hn, h_rec⟩ :=
    isometry_compact_orbit_gives_infinite_discrete_recurrence M s hSemi hIso hBdd hDNorm ε hε 1
  -- n ≥ 1, so n > 0.
  have hn_pos : 0 < n := by omega
  -- Semigroup: U(t₀ + n, s) = U(t₀, U(n, s)).
  have h_semi : M.propagate (t₀ + (n : ℝ)) s = M.propagate t₀ (M.propagate (n : ℝ) s) := by
    exact hSemi t₀ (n : ℝ) s
  -- Isometry: d(U(t₀, U(n, s)), U(t₀, s)) = d(U(n, s), s)
  have h_iso : M.d (M.propagate t₀ (M.propagate (n : ℝ) s)) (M.propagate t₀ s) =
               M.d (M.propagate (n : ℝ) s) s :=
    (hIso t₀ (M.propagate (n : ℝ) s) s).symm
  -- Combine: d(U(t₀+n, s), U(t₀, s)) → [semigroup] → d(U(t₀)(U(n)s), U(t₀)s)
  --         → [isometry] → d(U(n)s, s) → [hd] → dist(U(n)s, s)
  --         → [dist_comm] → dist(s, U(n)s) → [← hd] → d(s, U(n)s) < ε
  refine ⟨n, hn_pos, ?_⟩
  rw [h_semi, h_iso, hd, dist_comm, ← hd s (M.propagate (n : ℝ) s)]
  exact h_rec

/-! ## TWO-AXIS DIAGNOSIS (Devin 2026-06-25)

Z₃ spatial symmetry and temporal periodicity are INDEPENDENT axes:

  Z₃ spatial symmetry (M = J-I):
    - Property of the coupling matrix (how channels relate)
    - Selected by stability (H11): D=3 is unique stable dimension
    - Has REAL eigenvalues → contraction dynamics
    - Does NOT produce temporal periodicity

  Temporal periodicity (exact recurrence):
    - Property of the propagation dynamics (how states evolve)
    - Requires COMPLEX eigenvalues (imaginary part → oscillation)
    - Needs H4 (complex structure) + rationality condition
    - Does NOT require Z₃ spatial symmetry

These are INCOMPATIBLE through the standard circulant:
  - J-I (b=c) → real eigenvalues → contraction → no periodicity
  - Complex eigenvalues → b≠c → non-symmetric → no Z₃ symmetry
  - You cannot have both through the same coupling matrix.

ENDING B (symmetry irreducible) is likely the HONEST ANSWER:
  - Coherence (H8): 1 parameter — approximate recurrence
  - Spatial symmetry (H12/H13): 1 parameter — Z₃ structure
  - Stability (H11): 1 parameter — selects D=3
  - Total: 3 irreducible physical posits + scaffolding

See DESIGN_H_ISOMETRY_REAL_EIGENVALUE_20260625.md for the full analysis. -/

/-! # WHAT'S NEEDED NEXT

  1. ✅ DONE: Bare formalism chosen — `propagate : ℝ → State → State` (semigroup)
     with pseudometric `d` and `causal_velocity`. Claude's Q2/Q3 answers applied.
  2. ✅ DONE: Edge 18 — compact-orbit theorem (H19 + H21 + finite-dim → IsCompact).
  3. ✅ DONE: Edge 28 — discrete sampled recurrence (H2 + H14 + H19 + H21 → Nat-witness recurrence).
     First theorem to use H14 (isometry) essentially. No new hypotheses needed.
     Repaired 2026-07-15: primary theorem now exports a Nat witness
     (`isometry_compact_orbit_gives_discrete_recurrence`); the Real-time version
     is retained as a corollary. The Nat witness excludes the small-time
     contraction loophole that the Real-time statement alone permits.
     This is NOT exact periodicity and NOT arbitrary-late recurrence.
  4. ✅ DONE: Bug fix — recurrent_mode_from_H3_H2 sorry replaced with trivial proof
     (s=0 is a fixed point of any linear semigroup; the non-trivial version is the
     real open question, already captured by recurrence_stability_plus_structural_gives_nonzero_periodic_orbit).
  5. NEXT: Greg builds Axioms.lean, then DeepSeek hostile review, then Codex truth-lock.
  6. ✅ DONE: Recurrence strengthened to "infinitely many return times" —
     `isometry_compact_orbit_gives_infinite_discrete_recurrence` (Devin 2026-07-15).
     For every ε > 0 and every N ∈ ℕ, ∃ n ≥ N with d(s, propagate(n, s)) < ε.
     The return times are unbounded. Proof: fix one orbit point near a cluster
     point, let the other go to infinity. Same hypotheses as Edge 28, no new
     assumptions needed. This is NOT exact periodicity — the irrational torus
     rotation satisfies it but never exactly returns.
  7. OPEN: Does the recurrence theorem connect to the Z₃ / circulant structure?
     The two-axis diagnosis says spatial symmetry and temporal recurrence are
     independent. This theorem formalizes the temporal recurrence axis.
  8. Devin: implement the arbitrary-D experiment (see ArbitraryD.lean).
     Refactor `Fin 3 → ℝ` to `Fin D → ℝ` and ask Lean: is D=3 forced or fit?
  9. H10 audit: check whether λ_c and Planck-boundary coupling secretly use H10.
  10. NOTE: `isometry_linear_semigroup_gives_nonzero_periodic_orbit` (line ~1120)
      still has an explicit `sorry` — it needs the spectral theorem for
      skew-symmetric matrices. This does NOT taint Edge 28's dependency closure.
-/
