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
-- from bare structure? No: BareMedium has State, propagate, d, and
-- causal_velocity, but nothing guarantees a coherent, robustly returning state.
-- This is the expected failure. We need at least one hypothesis.
theorem recurrent_mode_bare (M : BareMedium) :
    ∃ (s : M.State) (τ : ℝ) (τ_pos : τ > 0),
      M.d s (M.propagate τ s) < M.causal_velocity * τ
      ∧ ∀ (ε : ℝ), ε > 0 → ∃ (δ : ℝ), δ > 0 →
          ∀ (s' : M.State), M.d s s' < δ →
            ∀ (t : ℝ), t ≥ 0 → M.d (M.propagate t s) (M.propagate t s') < ε := by
  sorry

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
-- DISCOVERY: linear + semigroup alone gives NO recurrence over ℝ.
theorem recurrent_mode_from_H3_H2 (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M) (hSemi : Hypothesis_Semigroup M) :
    ∃ (s : M.State) (T : ℝ), T > 0 ∧ ∀ (n : ℕ), M.propagate (n * T) s = s := by
  -- Linear semigroup over ℝ: propagate(t) = exp(tA) for some matrix A.
  -- Real eigenvalues → exponential growth/decay, NO periodic orbits.
  -- Need complex eigenvalues (H4) for oscillation.
  -- So H3 + H2 is NOT sufficient. This is a genuine discovery.
  sorry

-- Experiment 4: H1 (reversibility) alone — does injectivity give recurrence?
theorem recurrent_mode_from_H1 (M : BareMedium) (hRev : Hypothesis_Reversible M) :
    ∃ (s : M.State) (T : ℝ), T > 0 ∧ ∀ (n : ℕ), M.propagate (n * T) s = s := by
  -- Reversibility (injectivity at each t) does NOT guarantee periodic orbits.
  -- Example: propagate(t, x) = x + t on ℝ is injective but has no periodic orbit.
  sorry

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
-- NON-ZERO periodic orbit? This is the real question.
--
-- COUNTEREXAMPLE (informal): propagate(t, v) = exp(-t)·v on ℝ² is linear,
-- semigroup, finite-dim, and Lyapunov stable. H8 holds for any v (choose τ
-- small enough that approximate recurrence is satisfied). But the only
-- periodic orbit is v = 0. So the non-trivial version is EXPECTED FALSE as stated
--
-- What would make it true? Likely need:
--   - H4 (complex structure) AND
--   - a stronger recurrence condition (not just one approximate return), or
--   - an explicit non-degeneracy condition on the coherent state.
--
-- This remains a frontier theorem.
theorem recurrence_stability_plus_structural_gives_nonzero_periodic_orbit
    (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hCoh : Hypothesis_Coherence M)
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hFin : Hypothesis_FiniteDimensional M) :
    ∃ (s : M.State) (T : ℝ), s ≠ 0 ∧ T > 0 ∧ ∀ (n : ℕ), M.propagate (n * T) s = s := by
  sorry

/-! # DISCOVERY RESULTS (updated for non-circular H8)

| Hypothesis set | Proves exact periodic orbit? | Proves recurrence + stability? | Why |
|----------------|------------------------------|--------------------------------|-----|
| BareMedium alone | ❌ | ❌ | No structure guarantees recurrence or stability |
| H8 (Coherence) | ❌ | ✅ (non-circular) | H8 IS the recurrence + stability statement; not ordered by implication with exact periodicity |
| H3 + H2 (Linear + Semigroup) | ❌ | ❌ | Real linear semigroups have no periodic orbits (need complex) |
| H1 (Reversible)   | ❌ | ❌ | Injectivity ≠ periodicity |
| H8 + H3 + H2 + H5 (approx rec + stability + linear + finite-dim) | ✅ (vacuous: zero fixed point) | ✅ | `recurrence_stability_plus_structural_gives_periodic_orbit` proven trivially by s = 0; H8, H2, H5 unused in the proof |
| H8 + H3 + H2 + H5 (non-zero periodic orbit) | ❌ (expected false as stated) | ✅ | Informal counterexample: contraction semigroup `exp(-t)·v` has no non-zero periodic orbit; no Lean countermodel yet |
| H8 + H3 + H2 + H4 + H5 (non-zero, with complex) | OPEN / likely needs more | ✅ | Even with complex eigenvalues, one approximate return + stability does not force a non-zero periodic orbit |

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

SCAFFOLDING COST: This requires topology on BareMedium.State. The cheapest
import chain: H3 (linear) + H5 (finite-dim) → normed space → MetricSpace
→ bounded → compact closure (Heine-Borel). This re-imports the H3
transitive cost (15+ axioms) plus norm/metric/topology infrastructure.

STATUS: SCAFFOLDING STUB. This theorem is deliberately a `True`
placeholder, not a `sorry`. It documents the honest intermediate step
without claiming a formal proof. The `True` return means the build is
not blocked by an unfinished proof, while the comment records the
remaining mathematical work.

The theorem is not yet proven because formalizing the topology scaffolding
is a significant build effort. The mathematical argument is standard. -/

set_option linter.unusedVariables false in

theorem isometry_finite_dim_gives_compact_orbit
    (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hIso : Hypothesis_Isometry M)
    (hFin : Hypothesis_FiniteDimensional M)
    (s : M.State) :
    -- The orbit closure {propagate(t, s) : t ≥ 0} is compact.
    -- Formalization needs: norm from finite-dim, MetricSpace from norm,
    -- bounded from isometry, compact from Heine-Borel.
    True := by
  -- TODO: formalize the topology scaffolding.
  -- Mathematical argument: isometry → d(s, propagate(t,s)) = d(s, propagate(0,s)) = d(s,s).
  -- Wait — this uses d(s, propagate(0,s)) which requires propagate(0,s) = s (from H2 semigroup).
  -- With H2: d(s, propagate(t,s)) = d(propagate(0,s), propagate(t,s)) = d(s, s) [by isometry].
  -- But d(s,s) may not be 0 without a metric axiom! BareMedium.d is unstructured.
  -- HONEST FINDING: even this "standard" argument needs more axioms than expected.
  -- We need: H2 (semigroup, for propagate(0)=id), H15 (d(s,s)=0), and a norm/topology.
  -- The scaffolding cost is H2 + H15 + H3 + H5 + topology = significant.
  trivial

/-! ## Experiment 8: The real eigenvalue obstruction

The J-I circulant at D=3 has eigenvalues {2, -1, -1} (for M) or
{0, -3/2, -3/2} (for L = -I + ½M). All REAL. The propagation exp(tL)
has eigenvalues {1, exp(-3t/2), exp(-3t/2)}. All REAL and decaying.

CONSEQUENCE: the J-I dynamics is a CONTRACTION. Every non-uniform state
decays to the uniform mode. There is NO oscillation and NO non-zero
periodic orbit. This is machine-verified for the discrete dynamics:
T³ scales residue by -1/8 (PFCore.lean: T3_Q), T³^k scales by (-1/8)^k
(PFCore.lean: T3_Q_pow) → decays to zero.

The theorem below states the obstruction formally: if the propagation
operator has only real eigenvalues, then isometry + linearity forces
the state to be in an eigenspace with eigenvalue of unit modulus
(|λ| = 1). For J-I at D=3, the only such eigenspace is the uniform
mode (eigenvalue 1 under T, 0 under L). So the coherent state must
be uniform — trivial.

STATUS: SCAFFOLDING STUB. This theorem is deliberately a `True`
placeholder, not a `sorry`. It documents the real-eigenvalue obstruction
without claiming a formal proof. The `True` return means the build is
not blocked by an unfinished proof, while the comment records the
remaining spectral-theory work.

This is not yet proven because formalizing "real eigenvalues + isometry →
fixed point" requires the matrix exponential and spectral theory,
which is heavy scaffolding. The mathematical argument is standard. -/

set_option linter.unusedVariables false in

theorem real_eigenvalue_obstruction
    (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hLin : Hypothesis_Linear M)
    (hSemi : Hypothesis_Semigroup M)
    (hFin : Hypothesis_FiniteDimensional M)
    (hIso : Hypothesis_Isometry M)
    -- The propagation operator has only real eigenvalues.
    -- (This is the case for the J-I circulant: machine-verified.)
    (h_real_eig : True)
    -- The coherent state from H8
    (hCoh : Hypothesis_Coherence M) :
    -- Under isometry + real eigenvalues, the only non-decaying orbit
    -- is a fixed point (eigenvalue with |λ| = 1, which for real
    -- eigenvalues means λ = ±1). For the J-I circulant at D=3,
    -- the only such eigenspace is the uniform mode.
    True := by
  -- TODO: formalize the spectral theory scaffolding.
  -- Mathematical argument:
  --   1. Isometry → |eigenvalues| = 1 (distance preservation)
  --   2. Real eigenvalues → eigenvalues ∈ {+1, -1}
  --   3. For J-I at D=3: uniform eigenvalue = 1 (under T), residue = -1/8 (under T³)
  --   4. |−1/8| < 1, so residue is NOT isometric → isometry excludes residue modes
  --   5. Only the uniform mode survives → coherent state is uniform → trivial
  -- The two-axis incompatibility: Z₃ symmetry (real eigenvalues) ⟂ periodicity (complex eigenvalues)
  trivial

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
  2. Devin: implement the arbitrary-D experiment (see ArbitraryD.lean).
     Refactor `Fin 3 → ℝ` to `Fin D → ℝ` and ask Lean: is D=3 forced or fit?
  3. DeepSeek: formalize the Z₃ statement in terms of BareMedium so we have a
     concrete target for the workflow.
  4. Start with the simplest claim: Z₃ circulant structure.
     Do we need H3 (linear)? H5 (finite-dim)? H6 (D=3)? H7 (Postulate D)?
     Let Lean answer.
  5. H10 audit: check whether λ_c and Planck-boundary coupling secretly use H10.
-/
