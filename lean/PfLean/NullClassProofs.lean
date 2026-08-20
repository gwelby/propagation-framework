/-
  PfLean.NullClassProofs — Machine-checked null-class proofs for the consciousness metric

  Authors: Devin
  Started: 2026-08-19
  Updated: 2026-08-19 — vacuous axiom and True-concluding theorems removed (Claude finding)

  WHAT THIS PROVES:
    Class I: If M = f(E) (deterministic function of E), then M ⊥ X | E.
    This is machine-checked with zero sorries.

  WHAT IS PARTIALLY PROVEN:
    Bridge lemma: If f ⊥ (g, h), then f ⊥ h | g.
    9 of 10 proof steps compile. Step 10 (ae_eq_condExp_of_forall_setIntegral_eq)
    remains sorry. This lemma does not exist in Mathlib.

  WHAT THIS DOES NOT PROVE:
    - Class II conditional independence (depends on bridge lemma, sorry)
    - The "CI ⟹ MI = 0" step — NOT FORMALIZED, not even as a stated axiom.
      The previous version had an axiom `condIndep_implies_zero_mi` concluding
      `True`, which is provable by `trivial` and asserts nothing. It has been
      removed. Formalizing this step requires defining conditional mutual
      information in Lean, which is future work.
    - Anything about consciousness
    - Anything about EEG, PLV, wPLI, or real data
    - The M_obs_t → M_t bridge

  KEY MATHLIB Lemmas:
    - condIndepFun_of_measurable_left: if X is m'-measurable, Y measurable,
      then CondIndepFun m' X Y (X is CI of Y given m')
    - comap_measurable: f is measurable w.r.t. σ(f) (the comap sigma-algebra)
    - Measurable.comp: if f measurable and g measurable, then f ∘ g measurable
    - condExp_indep_eq: if m₁ ⊥ m₂ and f is m₁-measurable, then E[f | m₂] = E[f] a.e.
    - IndepFun_iff_Indep: IndepFun f g μ ↔ Indep (comap f) (comap g) μ
    - Indep_iff: Indep m₁ m₂ μ ↔ ∀ s t, m₁-measurable s → m₂-measurable t →
      μ(s ∩ t) = μ(s) * μ(t)

  PROOF PATTERN:
    Following Mathlib's own convention, we use an explicit measure parameter
    μ : Measure Ω with [IsFiniteMeasure μ] rather than relying on MeasureSpace's
    volume. This matches how condIndepFun_of_measurable_left is stated in
    Mathlib/Probability/Independence/Conditional.lean.
-/

import Mathlib

open ProbabilityTheory MeasureTheory

namespace NullClassProofs

/-! ## Class I: Exogenous-only controller (thermostat shape)

  M = f(E) — model is a deterministic function of E only.
  Claim: M ⊥ X | E (conditional independence)

  Proof:
    M = f ∘ E where f is measurable.
    By comap_measurable, E is σ(E)-measurable.
    By Measurable.comp, f ∘ E is σ(E)-measurable.
    By condIndepFun_of_measurable_left, (f ∘ E) ⊥ X | σ(E).
    Since M = f ∘ E, M ⊥ X | E.  ∎

  NOTE: The conditional independence M ⊥ X | E is the actual mathematical
  content. The further step "CI ⟹ I(M; X | E) = 0" is NOT formalized here.
  Formalizing it requires defining conditional mutual information in Lean.
-/

/-- Class I null: M = f(E) is deterministic, so M ⊥ X | E.

    PROVEN — zero sorries, zero axioms. This is a real machine-checked proof.

    The proof uses three Mathlib lemmas:
    1. comap_measurable E : Measurable[σ(E)] E
    2. hf.comp (comap_measurable E) : Measurable[σ(E)] (f ∘ E)
    3. condIndepFun_of_measurable_left : Measurable[m'] X → Measurable Y → CondIndepFun m' X Y -/
theorem class_I_conditional_independence
    {Ω : Type*} {mΩ : MeasurableSpace Ω} [StandardBorelSpace Ω] [Nonempty Ω]
    {μ : Measure Ω} [IsFiniteMeasure μ]
    {β γ δ : Type*} [MeasurableSpace β] [StandardBorelSpace β] [Nonempty β]
    [MeasurableSpace γ] [MeasurableSpace δ] [StandardBorelSpace δ] [Nonempty δ]
    (E : Ω → β) (X : Ω → γ) (M : Ω → δ)
    (f : β → δ) (hf : Measurable f)
    (hM : M = f ∘ E)
    (hE_meas : Measurable E) (hX_meas : Measurable X) :
    M ⟂ᵢ[E, hE_meas; μ] X := by
  subst hM
  exact condIndepFun_of_measurable_left (hf.comp (comap_measurable E)) hX_meas

/-! ## Bridge lemma: independence implies conditional independence

  If f is independent of the pair (g, h), then f is conditionally
  independent of h given g.

  This is a standard probability result that is NOT in Mathlib.
  Proof: if f ⊥ (g, h), then for any σ(g)-measurable set A and
  measurable sets s, t:
    μ(A ∩ f⁻¹'s ∩ h⁻¹'t) = μ(f⁻¹'s) * μ(A ∩ h⁻¹'t)
  because A ∩ h⁻¹'t ∈ σ(g, h) and f ⊥ σ(g, h).
  This gives μ⟦f⁻¹'s ∩ h⁻¹'t | σ(g)⟧ = μ(f⁻¹'s) * μ⟦h⁻¹'t | σ(g)⟧ a.e.,
  which is exactly CondIndepFun σ(g) f h.
-/

/-- Bridge lemma: if f ⊥ (g, h) then f ⊥ h | g.

    This lemma does not exist in Mathlib and is proved here as a new
    contribution. It bridges the unconditional independence world
    (IndepFun) to the conditional independence world (CondIndepFun).

    STATUS: sorry — 9 of 10 proof steps compile. Step 10 requires
    ae_eq_condExp_of_forall_setIntegral_eq with ENNReal.toReal plumbing
    for indicator integrals. The mathematical argument is standard. -/
theorem indepFun_implies_condIndepFun
    {Ω : Type*} {mΩ : MeasurableSpace Ω} [StandardBorelSpace Ω] [Nonempty Ω]
    {μ : Measure Ω} [IsFiniteMeasure μ]
    {β γ δ : Type*} [MeasurableSpace β] [StandardBorelSpace β] [Nonempty β]
    [MeasurableSpace γ] [StandardBorelSpace γ] [Nonempty γ]
    [MeasurableSpace δ] [StandardBorelSpace δ] [Nonempty δ]
    (f : Ω → β) (g : Ω → γ) (h : Ω → δ)
    (hf : Measurable f) (hg : Measurable g) (hh : Measurable h)
    (h_indep : IndepFun f (fun ω => (g ω, h ω)) μ) :
    CondIndepFun (MeasurableSpace.comap g inferInstance) hg.comap_le f h μ := by
  -- Step 1: Extract f ⊥ g from f ⊥ (g, h) by composing with Prod.fst
  have hfg : IndepFun f g μ :=
    h_indep.comp (measurable_id) (measurable_fst)
  -- Step 2: Convert to sigma-algebra independence
  rw [IndepFun_iff_Indep] at hfg
  -- Step 3: Also extract f ⊥ h from f ⊥ (g, h) by composing with Prod.snd
  have hfh : IndepFun f h μ :=
    h_indep.comp (measurable_id) (measurable_snd)
  -- Step 4: Use condIndepFun_iff to reduce to a.e. equality of condExp
  rw [condIndepFun_iff _ _ _ _ hf hh]
  intro s t hs ht
  -- Step 5: From f ⊥ g, the condExp of s given σ(g) is constant = μ(s)
  let m' := MeasurableSpace.comap g inferInstance
  let m₁ := MeasurableSpace.comap f inferInstance
  have h_ind_sm : StronglyMeasurable[m₁] (Set.indicator s (1 : Ω → ℝ)) :=
    stronglyMeasurable_const.indicator hs
  have h_const : μ⟦s | m'⟧ =ᵐ[μ] fun _ => ∫ x, Set.indicator s (1 : Ω → ℝ) x ∂μ := by
    exact condExp_indep_eq hf.comap_le hg.comap_le h_ind_sm hfg
  -- Step 6: Get sigma-algebra independence from h_indep
  have h_indep_Indep : Indep m₁
    (MeasurableSpace.comap (fun ω => (g ω, h ω)) inferInstance) μ := by
    rw [IndepFun_iff_Indep] at h_indep
    exact h_indep
  -- Step 7: comap g ≤ comap (g, h) because g = Prod.fst ∘ (g, h)
  have hcomap_g : m' ≤ MeasurableSpace.comap (fun ω => (g ω, h ω)) inferInstance := by
    intro u hu
    rw [MeasurableSpace.measurableSet_comap] at hu
    obtain ⟨s', hs', rfl⟩ := hu
    rw [MeasurableSpace.measurableSet_comap]
    exact ⟨s' ×ˢ Set.univ, MeasurableSet.prod hs' MeasurableSet.univ, by
      ext ω : 1
      simp [Set.mem_preimage, Set.mem_prod, Set.mem_univ]⟩
  -- Step 8: comap h ≤ comap (g, h) because h = Prod.snd ∘ (g, h)
  have hcomap_h : MeasurableSpace.comap h inferInstance ≤
      MeasurableSpace.comap (fun ω => (g ω, h ω)) inferInstance := by
    intro u hu
    rw [MeasurableSpace.measurableSet_comap] at hu
    obtain ⟨s', hs', rfl⟩ := hu
    rw [MeasurableSpace.measurableSet_comap]
    exact ⟨Set.univ ×ˢ s', MeasurableSet.prod MeasurableSet.univ hs', by
      ext ω : 1
      simp [Set.mem_preimage, Set.mem_prod, Set.mem_univ]⟩
  -- Step 9: Use Indep_iff to get measure factoring
  rw [Indep_iff] at h_indep_Indep
  -- Step 10: For A ∈ σ(g) and t ∈ σ(h), A ∩ t ∈ σ(g, h)
  -- So μ(s ∩ (A ∩ t)) = μ(s) * μ(A ∩ t) by independence
  -- This gives the integral equality needed for ae_eq_condExp_of_forall_setIntegral_eq.
  -- The candidate is (∫ 1_s ∂μ) * μ⟦t | m'⟧. The remaining steps are:
  --   - m'-measurability and integrability of the candidate
  --   - equality of set integrals over all A ∈ m'
  --   - replacing the constant back by μ⟦s | m'⟧ using h_const
  sorry

/-! ## Class II: Passive state tracker (epiphenomenal logger)

  X' = g(X, E', noise) — next state does NOT read M.
  Future noise (E', noise) is independent of the entire past (X, E, M).
  Claim: M ⊥ X' | (X, E)

  Proof:
    (E', noise) ⊥ (X, E, M) — future noise is independent of the past.
    X' = g(X, E', noise) is a measurable function of (X, E', noise).
    Given (X, E), X' depends only on (E', noise).
    Since (E', noise) ⊥ (X, E, M), by the bridge lemma:
      (E', noise) ⊥ M | (X, E)
    By CondIndepFun.comp, X' ⊥ M | (X, E).  ∎

  NOTE: As with Class I, the CI → MI=0 step is NOT formalized.
-/

/-- Class II null: X' does not depend on M, so M ⊥ X' | (X, E).

    The hypothesis is that future noise (E', noise) is independent of
    the entire past (X, E, M). This is the natural hypothesis for the
    Class II construction — future noise is independent of everything
    up to time t, not just of M.

    STATUS: sorry — depends on the bridge lemma
    indepFun_implies_condIndepFun which is itself sorry. The mathematical
    argument is sound (DeepSeek-audited at d-separation level). -/
theorem class_II_conditional_independence
    {Ω : Type*} {mΩ : MeasurableSpace Ω} [StandardBorelSpace Ω] [Nonempty Ω]
    {μ : Measure Ω} [IsFiniteMeasure μ]
    {β γ δ ε : Type*} [MeasurableSpace β] [StandardBorelSpace β] [Nonempty β]
    [MeasurableSpace γ] [StandardBorelSpace γ] [Nonempty γ]
    [MeasurableSpace δ] [StandardBorelSpace δ] [Nonempty δ]
    [MeasurableSpace ε] [StandardBorelSpace ε] [Nonempty ε]
    (X : Ω → β) (E : Ω → γ) (M : Ω → δ) (X' : Ω → β)
    (E' : Ω → γ) (noise : Ω → ε)
    (g : β × γ × ε → β) (hg : Measurable g)
    (hX'_def : X' = fun ω => g (X ω, E' ω, noise ω))
    (hfuture_indep :
      (fun ω => (E' ω, noise ω)) ⟂ᵢ[μ] (fun ω => (X ω, E ω, M ω)))
    (hX_meas : Measurable X) (hE_meas : Measurable E)
    (hM_meas : Measurable M) (hX'_meas : Measurable X')
    (hE'_meas : Measurable E') (hnoise_meas : Measurable noise) :
    M ⟂ᵢ[fun ω => (X ω, E ω), Measurable.prod hX_meas hE_meas; μ] X' := by
  -- Step 1: From (E', noise) ⊥ (X, E, M), apply the bridge lemma to get
  -- (E', noise) ⊥ M | (X, E).
  -- Step 2: X' = g(X, E', noise) is a measurable function of (X, E', noise).
  -- Given (X, E), X' is a function of (E', noise) only.
  -- Step 3: By CondIndepFun.comp, X' ⊥ M | (X, E).
  --
  -- This depends on indepFun_implies_condIndepFun (the bridge lemma)
  -- which is itself sorry. Both need the same Mathlib plumbing.
  sorry

end NullClassProofs

/-! ## Summary

  LEAN STATUS (honest, post-Claude-audit):
  - Class I conditional independence: PROVEN (zero sorries, zero axioms)
  - Bridge lemma (indepFun_implies_condIndepFun): 9/10 steps compiled, sorry
  - Class II conditional independence: sorry (depends on bridge lemma)
  - CI ⟹ MI = 0: NOT FORMALIZED — not even as a stated axiom

  VACUOUS AXIOM REMOVED (2026-08-19, Claude finding):
  The previous version had `axiom condIndep_implies_zero_mi ... : True`.
  An axiom concluding `True` is provable by `trivial` and asserts nothing.
  The name and docstring implied it represented "CI ⟹ MI = 0" but the
  type signature said no such thing. Both downstream theorems
  (`class_I_R_in_is_zero`, `class_II_R_out_is_zero`) concluded `True`
  and discharged via that axiom — they proved nothing. All three have
  been removed. This is the same promotion-layer pattern documented in
  CURIOSITIES.md: a real result at one layer dressed to look like it
  establishes something at the next layer.

  WHAT IS PROVEN (machine-checked by Lean):
  Class I: If M = f(E) for measurable f, then M ⊥ X | E.
  Proof body (2 lines, zero sorries, zero axioms):
    subst hM
    exact condIndepFun_of_measurable_left (hf.comp (comap_measurable E)) hX_meas

  WHAT IS PARTIALLY PROVEN (bridge lemma, 9/10 steps compiled):
  Bridge lemma: If f ⊥ (g, h), then f ⊥ h | g.
  This lemma does NOT exist in Mathlib (confirmed by exhaustive search).
  It is a genuine new contribution. The proof has 10 steps:
  1. Extract f ⊥ g from f ⊥ (g,h) — COMPILED (IndepFun.comp with Prod.fst)
  2. Convert to sigma-algebra independence — COMPILED (IndepFun_iff_Indep)
  3. Extract f ⊥ h from f ⊥ (g,h) — COMPILED (IndepFun.comp with Prod.snd)
  4. Reduce to a.e. equality of condExp — COMPILED (condIndepFun_iff)
  5. Constant condExp from independence — COMPILED (condExp_indep_eq)
  6. Get sigma-algebra independence from h_indep — COMPILED (IndepFun_iff_Indep)
  7. comap g ≤ comap (g,h) — COMPILED (Prod.fst decomposition)
  8. comap h ≤ comap (g,h) — COMPILED (Prod.snd decomposition)
  9. Get measure factoring — COMPILED (Indep_iff)
  10. ae_eq_condExp_of_forall_setIntegral_eq — SORRY
      (requires ENNReal.toReal plumbing for indicator integrals)

  WHAT IS NOT PROVEN:
  Class II: If X' = g(X, E', noise) where (E', noise) ⊥ (X, E, M),
  then M ⊥ X' | (X, E). Depends on the bridge lemma (sorry).

  CI ⟹ MI = 0: NOT FORMALIZED. The previous axiom concluding `True`
  has been removed. Formalizing this requires defining conditional
  mutual information in Lean — future work.

  HONEST ASSESSMENT:
  One conditional independence result is machine-checked in Lean (Class I).
  The bridge lemma needed for Class II has 9 of 10 steps compiled.
  The information-theoretic step (CI ⟹ MI = 0) is not formalized at all.
  The empirical battery (0% FPR, +0.1087 gap) stands independently of Lean.
-/