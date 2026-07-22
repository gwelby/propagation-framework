import Mathlib

/-- The 2x2 companion relation on E_μ: U(1) is like rotation by angle θ with cos θ = μ/2.
    Define J_E x = σ⁻¹ (U(1) x - (μ/2) x).  Then J_E^2 = -I on E_μ. -/

noncomputable def σ (μ : ℝ) : ℝ := Real.sqrt (1 - μ ^ 2 / 4)

lemma σ_nonneg (μ : ℝ) : 0 ≤ σ μ := Real.sqrt_nonneg _

lemma σ_pos (μ : ℝ) (hμ : |μ| < 2) : 0 < σ μ := by
  have h1 : 0 < 1 - μ ^ 2 / 4 := by
    have h2 : μ ^ 2 < 4 := by nlinarith [abs_lt.mp hμ]
    nlinarith
  apply Real.sqrt_pos.mpr
  nlinarith

lemma σ_sq (μ : ℝ) (hμ : |μ| < 2) : σ μ ^ 2 = 1 - μ ^ 2 / 4 := Real.sq_sqrt (by
  have h1 : μ ^ 2 < 4 := by nlinarith [abs_lt.mp hμ]
  nlinarith)

section JConstruction

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]
variable (U : ℝ → E →ₗ[ℝ] E)
variable (hU0 : U 0 = LinearMap.id)
variable (hUadd : ∀ s t, U (s + t) = U s ∘ₗ U t)
variable (hUnorm : ∀ t (x : E), ‖U t x‖ = ‖x‖)
variable (μ : ℝ) (hμ : |μ| < 2)
variable (Eμ : Submodule ℝ E)
variable (hEμ : Eμ = LinearMap.ker ((U 1 + U (-1) : E →ₗ[ℝ] E) - μ • LinearMap.id))
variable (hEinvar : ∀ t, ∀ x ∈ Eμ, U t x ∈ Eμ)
variable (hU1sqE : ∀ x ∈ Eμ, U 1 (U 1 x) = μ • U 1 x - x)

-- The 2x2 companion relation on E_μ: U(1) is like rotation by angle θ with cos θ = μ/2.
-- Define J_E x = σ⁻¹ (U(1) x - (μ/2) x).  Then J_E^2 = -I on E_μ.

noncomputable def J_fun (x : ↥Eμ) : ↥Eμ :=
  ⟨ (1 / (σ μ)) • (U 1 x.1 - (μ / 2) • x.1),
    by
      have h1 : U 1 x.1 ∈ Eμ := hEinvar 1 x.1 x.2
      have h2 : (μ / 2) • x.1 ∈ Eμ := Submodule.smul_mem _ _ x.2
      have h3 : U 1 x.1 - (μ / 2) • x.1 ∈ Eμ := Submodule.sub_mem _ h1 h2
      exact Submodule.smul_mem _ (1 / (σ μ)) h3 ⟩

lemma J_fun_coe (x : ↥Eμ) : (J_fun U μ Eμ hEinvar x : E) = (1 / (σ μ)) • (U 1 x.1 - (μ / 2) • x.1) := by
  rfl

noncomputable def J_E : ↥Eμ →ₗ[ℝ] ↥Eμ := {
  toFun := J_fun U μ Eμ hEinvar,
  map_add' := by
    intro x y
    ext
    simp only [J_fun_coe, Submodule.coe_add]
    have h1 : (U 1 : E →ₗ[ℝ] E) (x.1 + y.1) - (μ / 2 : ℝ) • (x.1 + y.1) =
              ((U 1) x.1 - (μ / 2 : ℝ) • x.1) + ((U 1) y.1 - (μ / 2 : ℝ) • y.1) := by
      rw [map_add, smul_add]
      abel
    rw [h1, smul_add]
  map_smul' := by
    intro c x
    ext
    simp only [J_fun_coe, Submodule.coe_smul]
    have h1 : (U 1 : E →ₗ[ℝ] E) (c • x.1) - (μ / 2 : ℝ) • (c • x.1) =
              c • ((U 1) x.1 - (μ / 2 : ℝ) • x.1) := by
      rw [map_smul]
      rw [show (μ / 2 : ℝ) • (c • x.1) = c • ((μ / 2 : ℝ) • x.1) by
            rw [smul_smul, mul_comm (μ / 2 : ℝ) c, ← smul_smul]]
      rw [← smul_sub]
    rw [h1]
    rw [smul_smul, mul_comm (1 / (σ μ) : ℝ) c, ← smul_smul]
    simp
}

lemma J_E_coe (x : ↥Eμ) : (J_E U μ Eμ hEinvar x : E) = (1 / (σ μ)) • (U 1 x.1 - (μ / 2) • x.1) := by
  rfl

include hμ hU1sqE in
lemma J_E_sq (x : ↥Eμ) : J_E U μ Eμ hEinvar (J_E U μ Eμ hEinvar x) = -x := by
  ext
  have hσ_pos : 0 < σ μ := σ_pos μ hμ
  have hσ_ne : σ μ ≠ 0 := ne_of_gt hσ_pos
  -- Compute U(1) acting on J_E x
  have hU1Jx : (U 1 : E →ₗ[ℝ] E) ((J_E U μ Eμ hEinvar x : E)) =
               (1 / (σ μ)) • ((μ / 2 : ℝ) • (U 1) x.1 - x.1) := by
    rw [J_E_coe]
    rw [map_smul]
    have hU1sq : (U 1) ((U 1) x.1) = μ • (U 1) x.1 - x.1 := hU1sqE x.1 x.2
    rw [map_sub, hU1sq]
    rw [map_smul]
    have h3 : μ • (U 1) x.1 - x.1 - (μ / 2 : ℝ) • (U 1) x.1 = (μ / 2 : ℝ) • (U 1) x.1 - x.1 := by
      have h4 : μ • (U 1) x.1 - (μ / 2 : ℝ) • (U 1) x.1 = (μ / 2 : ℝ) • (U 1) x.1 := by
        rw [← sub_smul]
        ring_nf
      have h5 : μ • (U 1) x.1 - x.1 - (μ / 2 : ℝ) • (U 1) x.1 =
                (μ • (U 1) x.1 - (μ / 2 : ℝ) • (U 1) x.1) - x.1 := by abel
      rw [h5, h4]
    rw [h3]
  -- Compute (μ/2) acting on J_E x
  have hsmulJx : (μ / 2 : ℝ) • (J_E U μ Eμ hEinvar x : E) =
                 (1 / (σ μ)) • ((μ / 2 : ℝ) • (U 1) x.1 - (μ / 2 : ℝ) ^ 2 • x.1) := by
    rw [J_E_coe]
    have h3 : (μ / 2 : ℝ) • (1 / (σ μ)) • (U 1 x.1 - (μ / 2 : ℝ) • x.1) =
              (1 / (σ μ)) • ((μ / 2 : ℝ) • (U 1 x.1 - (μ / 2 : ℝ) • x.1)) := by
      rw [smul_smul, mul_comm (μ / 2 : ℝ) (1 / (σ μ) : ℝ), ← smul_smul]
    rw [h3, smul_sub, smul_smul]
    rw [show (μ / 2 : ℝ) * (μ / 2 : ℝ) = (μ / 2 : ℝ) ^ 2 by ring]
  -- Combine to get U(1)(J_E x) - (μ/2)(J_E x) = (1/σ) • (-(σ^2 • x))
  have hinner : (U 1) (J_E U μ Eμ hEinvar x : E) - (μ / 2 : ℝ) • (J_E U μ Eμ hEinvar x : E) =
                (1 / (σ μ)) • (-(σ μ ^ 2 • x.1)) := by
    rw [hU1Jx, hsmulJx]
    have h5 : (σ μ) ^ 2 = 1 - μ ^ 2 / 4 := σ_sq μ hμ
    have h6 : (μ / 2 : ℝ) • (U 1) x.1 - x.1 - ((μ / 2 : ℝ) • (U 1) x.1 - (μ / 2 : ℝ) ^ 2 • x.1) =
              -(σ μ ^ 2 • x.1) := by
      rw [show (μ / 2 : ℝ) ^ 2 = μ ^ 2 / 4 by ring]
      have h7 : (μ ^ 2 / 4 : ℝ) • x.1 - x.1 = (-(σ μ ^ 2) : ℝ) • x.1 := by
        nth_rewrite 2 [show x.1 = (1 : ℝ) • x.1 by rw [one_smul]]
        rw [← sub_smul]
        have h8 : (μ ^ 2 / 4 : ℝ) - (1 : ℝ) = -(σ μ ^ 2) := by
          have h9 : (σ μ) ^ 2 = 1 - μ ^ 2 / 4 := h5
          linarith
        rw [h8]
      have h8 : (μ / 2 : ℝ) • (U 1) x.1 - x.1 - ((μ / 2 : ℝ) • (U 1) x.1 - (μ ^ 2 / 4 : ℝ) • x.1) =
                (μ ^ 2 / 4 : ℝ) • x.1 - x.1 := by abel
      rw [h8, h7]
      rw [← neg_smul]
    rw [← smul_sub]
    rw [h6]
  -- Now J_E(J_E x) = (1/σ) • (U(1)(J_E x) - (μ/2)(J_E x)) = (1/σ) • (1/σ) • (-(σ^2 • x)) = -x
  have hJ2 : (1 / (σ μ)) • ((1 / (σ μ)) • (-(σ μ ^ 2 • x.1))) = - x.1 := by
    have h9 : (1 / (σ μ) : ℝ) * (1 / (σ μ) : ℝ) * (σ μ ^ 2 : ℝ) = 1 := by
      field_simp [hσ_ne]
    have h10 : (1 / (σ μ)) • ((1 / (σ μ)) • (-(σ μ ^ 2 • x.1))) =
               -(((1 / (σ μ) : ℝ) * (1 / (σ μ) : ℝ) * (σ μ ^ 2 : ℝ)) • x.1) := by
      rw [smul_smul]
      rw [smul_neg]
      rw [smul_smul]
    rw [h10, h9]
    simp [one_smul]
  rw [J_E_coe, hinner]
  exact hJ2

@[reducible] noncomputable def complexSMul : SMul ℂ ↥Eμ :=
  ⟨fun z x => z.re • x + z.im • (J_E U μ Eμ hEinvar x)⟩

@[reducible] noncomputable def complexModule : Module ℂ ↥Eμ := by
  letI : SMul ℂ ↥Eμ := complexSMul U μ Eμ hEinvar
  have hsmul : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
  have hJ2 : ∀ (x : ↥Eμ), (J_E U μ Eμ hEinvar) ((J_E U μ Eμ hEinvar) x) = -x := fun x => J_E_sq U μ hμ Eμ hEinvar hU1sqE x
  refine Module.ofMinimalAxioms ?_ ?_ ?_ ?_
  · -- smul_add
    intro z x y
    simp [hsmul, smul_add]
    abel
  · -- add_smul
    intro z w x
    simp [hsmul, Complex.add_re, Complex.add_im, add_smul]
    abel
  · -- mul_smul
    intro z w x
    simp [hsmul, Complex.mul_re, Complex.mul_im, smul_add, smul_smul, add_smul, hJ2, smul_neg, neg_smul, neg_one_smul]
    try abel
    module
  · -- one_smul
    intro x
    simp [hsmul, Complex.one_re, Complex.one_im, one_smul, zero_smul]

/-- The restriction of `U(t)` to `E_μ`. -/
def U_E_real (t : ℝ) : ↥Eμ →ₗ[ℝ] ↥Eμ where
  toFun := fun x => ⟨U t x.1, hEinvar t x.1 x.2⟩
  map_add' := by
    intro x y
    ext
    simp [map_add]
  map_smul' := by
    intro c x
    ext
    simp [map_smul]

lemma U_E_real_coe (t : ℝ) (x : ↥Eμ) : (U_E_real U Eμ hEinvar t x : E) = U t x.1 := rfl

include hUadd in
lemma U_E_commutes_J (t : ℝ) (x : ↥Eμ) : U_E_real U Eμ hEinvar t (J_E U μ Eμ hEinvar x) = J_E U μ Eμ hEinvar (U_E_real U Eμ hEinvar t x) := by
  ext
  simp [U_E_real_coe, J_E_coe, map_smul, map_sub]
  have h1 : (U t) ((U 1) x.1) = (U 1) ((U t) x.1) := by
    have h2 : (U t) ((U 1) x.1) = U (t + 1) x.1 := by
      rw [← LinearMap.comp_apply, hUadd t 1]
    have h3 : (U 1) ((U t) x.1) = U (1 + t) x.1 := by
      rw [← LinearMap.comp_apply, hUadd 1 t]
    have h4 : t + 1 = 1 + t := by ring
    rw [h2, h3, h4]
  rw [h1]

include hUadd in
lemma U_E_smul_explicit (t : ℝ) (z : ℂ) (x : ↥Eμ) :
  U_E_real U Eμ hEinvar t (z.re • x + z.im • J_E U μ Eμ hEinvar x) =
  z.re • U_E_real U Eμ hEinvar t x + z.im • J_E U μ Eμ hEinvar (U_E_real U Eμ hEinvar t x) := by
  rw [map_add, map_smul, map_smul]
  have h := U_E_commutes_J U hUadd μ Eμ hEinvar t x
  rw [h]


include U hUadd μ hμ Eμ hEinvar hU1sqE in
theorem exists_common_generalized_eigenvector (hEμne : Eμ ≠ ⊥) :
  ∃ (v : ↥Eμ) (χ : ℝ → ℂ), v ≠ 0 ∧
    ∀ (t : ℝ), ∃ (k : ℕ),
      ((U_E_real U Eμ hEinvar t - ((χ t).re • (LinearMap.id : ↥Eμ →ₗ[ℝ] ↥Eμ)) - (χ t).im • (J_E U μ Eμ hEinvar : ↥Eμ →ₗ[ℝ] ↥Eμ)) ^ k) v = 0 := by
  -- Build the ℂ-module structure on E_μ.
  letI hmod : Module ℂ ↥Eμ := complexModule U μ hμ Eμ hEinvar hU1sqE
  -- Restrict scalars from ℂ to ℝ gives back the real module.
  letI hst : IsScalarTower ℝ ℂ ↥Eμ := {
    smul_assoc := by
      intro r z x
      have hsmul : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
      simp only [hsmul]
      simp [Complex.mul_re, Complex.mul_im, smul_add, smul_smul]
  }
  letI hfin : FiniteDimensional ℂ ↥Eμ := by
    have hfin : FiniteDimensional ℝ ↥Eμ := by infer_instance
    exact Module.Finite.of_restrictScalars_finite ℝ ℂ ↥Eμ
  -- Lift U(t) to a ℂ-linear endomorphism.
  let f (t : ℝ) : Module.End ℂ ↥Eμ := {
    toFun := U_E_real U Eμ hEinvar t,
    map_add' := fun x y => map_add (U_E_real U Eμ hEinvar t) x y,
    map_smul' := by
      intro z x
      have hsmul : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
      rw [hsmul z x]
      have h1 := U_E_smul_explicit U hUadd μ Eμ hEinvar t z x
      rw [h1]
      have h2 : z.re • U_E_real U Eμ hEinvar t x + z.im • J_E U μ Eμ hEinvar (U_E_real U Eμ hEinvar t x) = z • U_E_real U Eμ hEinvar t x := by
        rw [hsmul z (U_E_real U Eμ hEinvar t x)]
      rw [h2]
      simp [RingHom.id_apply]
  }
  -- The family commutes because U is a one-parameter group.
  have hf_commute : ∀ (s t : ℝ), Commute (f s) (f t) := by
    intro s t
    ext x
    simp [f, U_E_real_coe]
    have h1 : (U s) ((U t) x.1) = (U (s + t)) x.1 := by
      rw [← LinearMap.comp_apply, hUadd s t]
    have h2 : (U t) ((U s) x.1) = (U (t + s)) x.1 := by
      rw [← LinearMap.comp_apply, hUadd t s]
    rw [h1, h2]
    rw [show s + t = t + s by ring]
  have hf_pair : Pairwise (fun s t => Commute (f s) (f t)) := by
    intro s t _
    exact hf_commute s t
  -- Each individual endomorphism has spanning generalized eigenspaces over ℂ.
  have hf_iSup : ∀ (t : ℝ), ⨆ (μ : ℂ), (f t).maxGenEigenspace μ = ⊤ := by
    intro t
    apply Module.End.iSup_maxGenEigenspace_eq_top (f t)
  -- Apply simultaneous generalized eigenspaces.
  have h_iSup_iInf : ⨆ (χ : ℝ → ℂ), ⨅ (t : ℝ), (f t).maxGenEigenspace (χ t) = ⊤ := by
    apply Module.End.iSup_iInf_maxGenEigenspace_eq_top_of_iSup_maxGenEigenspace_eq_top_of_commute f hf_pair hf_iSup
  -- The top submodule is nontrivial because E_μ is nonzero.
  have h_top_ne_bot : (⊤ : Submodule ℂ ↥Eμ) ≠ ⊥ := by
    have hne : Nontrivial ↥Eμ := by
      rw [Submodule.nontrivial_iff_ne_bot]
      exact hEμne
    intro h
    have h1 : Subsingleton (⊤ : Submodule ℂ ↥Eμ) := by
      rw [h]
      infer_instance
    have h2 : Subsingleton ↥Eμ := by
      have he : (⊤ : Submodule ℂ ↥Eμ) ≃ₗ[ℂ] ↥Eμ := Submodule.topEquiv
      exact he.toEquiv.subsingleton_congr.mp h1
    have h3 : Nontrivial ↥Eμ := hne
    have h4 : ¬Nontrivial ↥Eμ := by
      haveI := h2
      exact not_nontrivial ↥Eμ
    contradiction
  -- Therefore some simultaneous generalized eigenspace is nonzero.
  have hχ : ∃ (χ : ℝ → ℂ), ⨅ (t : ℝ), (f t).maxGenEigenspace (χ t) ≠ ⊥ := by
    by_contra h
    push_neg at h
    have hbot : ⨆ (χ : ℝ → ℂ), ⨅ (t : ℝ), (f t).maxGenEigenspace (χ t) = ⊥ := by
      rw [iSup_eq_bot]
      intro χ
      exact h χ
    rw [h_iSup_iInf] at hbot
    contradiction
  rcases hχ with ⟨χ, hχ⟩
  obtain ⟨v, hv_mem, hv_ne⟩ := (Submodule.ne_bot_iff _).mp hχ
  refine ⟨v, χ, hv_ne, ?_⟩
  intro t
  have hvt : v ∈ (f t).maxGenEigenspace (χ t) := by
    exact (Submodule.mem_iInf _).mp hv_mem t
  rw [Module.End.mem_maxGenEigenspace] at hvt
  rcases hvt with ⟨k, hk⟩
  use k
  let g_t := f t - χ t • (LinearMap.id : ↥Eμ →ₗ[ℂ] ↥Eμ)
  let L_t := U_E_real U Eμ hEinvar t - ((χ t).re • (LinearMap.id : ↥Eμ →ₗ[ℝ] ↥Eμ)) - (χ t).im • (J_E U μ Eμ hEinvar : ↥Eμ →ₗ[ℝ] ↥Eμ)
  have hL : (g_t : ↥Eμ → ↥Eμ) = (L_t : ↥Eμ → ↥Eμ) := by
    funext x
    simp [f, U_E_real_coe, g_t, L_t]
    have hsmul : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
    rw [hsmul (χ t) x]
    abel
  have hpow : ∀ (k : ℕ), (g_t ^ k) v = (L_t ^ k) v := by
    intro k
    induction k with
    | zero => simp
    | succ k ih =>
      rw [pow_succ', pow_succ']
      rw [Module.End.mul_apply, Module.End.mul_apply]
      rw [ih]
      rw [hL]
  rw [← hpow k]
  exact hk

include U hUnorm in
lemma U_t_preserves_inner (t : ℝ) (x y : E) : inner ℝ (U t x) (U t y) = inner ℝ x y := by
  have h := (LinearMap.norm_map_iff_inner_map_map (U t : E →ₗ[ℝ] E)).mp (hUnorm t)
  exact h x y

include U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE in
lemma U_one_eq (x : ↥Eμ) : (U 1 x.1 : E) = (μ / 2 : ℝ) • (x : E) + (σ μ : ℝ) • (J_E U μ Eμ hEinvar x : E) := by
  have h := J_E_coe U μ Eμ hEinvar x
  have hσ : σ μ ≠ 0 := ne_of_gt (σ_pos μ hμ)
  have h' : (σ μ : ℝ) • (J_E U μ Eμ hEinvar x : E) = (U 1 x.1 : E) - (μ / 2 : ℝ) • (x : E) := by
    rw [h]
    rw [smul_smul]
    have hσ1 : (σ μ : ℝ) * (1 / σ μ) = 1 := by field_simp [hσ]
    rw [hσ1]
    rw [one_smul]
  calc
    (U 1 x.1 : E) = (U 1 x.1 : E) - (μ / 2 : ℝ) • (x : E) + (μ / 2 : ℝ) • (x : E) := by rw [sub_add_cancel]
    _ = (σ μ : ℝ) • (J_E U μ Eμ hEinvar x : E) + (μ / 2 : ℝ) • (x : E) := by rw [h']
    _ = (μ / 2 : ℝ) • (x : E) + (σ μ : ℝ) • (J_E U μ Eμ hEinvar x : E) := by rw [add_comm]

include U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE in
lemma U_E_one_eq (x : ↥Eμ) : U_E_real U Eμ hEinvar 1 x = (μ / 2 : ℝ) • x + (σ μ : ℝ) • J_E U μ Eμ hEinvar x := by
  apply Subtype.ext
  rw [U_E_real_coe]
  exact U_one_eq U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE x

include U hUnorm Eμ hEinvar in
lemma U_E_real_preserves_inner (t : ℝ) (x y : ↥Eμ) : inner ℝ (U_E_real U Eμ hEinvar t x) (U_E_real U Eμ hEinvar t y) = inner ℝ x y := by
  simp [U_E_real_coe, U_t_preserves_inner U hUnorm t x.1 y.1]

include U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE in
set_option maxHeartbeats 800000 in
lemma J_E_inner_zero (x : ↥Eμ) : inner ℝ x (J_E U μ Eμ hEinvar x) = 0 := by
  let Jx := J_E U μ Eμ hEinvar x
  let a := (μ / 2 : ℝ)
  let b := (σ μ : ℝ)
  have h1 : U_E_real U Eμ hEinvar 1 x = a • x + b • Jx := U_E_one_eq U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE x
  have h2 : U_E_real U Eμ hEinvar 1 Jx = a • Jx - b • x := by
    have h2' := U_E_one_eq U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE Jx
    have hJ : J_E U μ Eμ hEinvar Jx = - x := by
      rw [show Jx = J_E U μ Eμ hEinvar x by rfl]
      rw [J_E_sq U μ hμ Eμ hEinvar hU1sqE x]
      all_goals norm_num
    rw [hJ] at h2'
    have hneg1 : b • (- x) = - (b • x) := by rw [smul_neg]
    rw [hneg1] at h2'
    have ha : a = (μ / 2 : ℝ) := by rfl
    rw [ha]
    rw [← sub_eq_add_neg] at h2'
    exact h2'
  have h3 : inner ℝ (U_E_real U Eμ hEinvar 1 x) (U_E_real U Eμ hEinvar 1 x) = inner ℝ x x := U_E_real_preserves_inner U hUnorm Eμ hEinvar 1 x x
  have h4 : inner ℝ (U_E_real U Eμ hEinvar 1 Jx) (U_E_real U Eμ hEinvar 1 Jx) = inner ℝ Jx Jx := U_E_real_preserves_inner U hUnorm Eμ hEinvar 1 Jx Jx
  have h5 : inner ℝ (U_E_real U Eμ hEinvar 1 x) (U_E_real U Eμ hEinvar 1 Jx) = inner ℝ x Jx := U_E_real_preserves_inner U hUnorm Eμ hEinvar 1 x Jx
  rw [real_inner_self_eq_norm_sq (U_E_real U Eμ hEinvar 1 x), real_inner_self_eq_norm_sq x, h1] at h3
  rw [real_inner_self_eq_norm_sq (U_E_real U Eμ hEinvar 1 Jx), real_inner_self_eq_norm_sq Jx, h2] at h4
  rw [h1, h2] at h5
  have hax : ‖a • x‖ ^ 2 = a ^ 2 * ‖x‖ ^ 2 := by
    have h' : ‖a • x‖ = |a| * ‖x‖ := by
      rw [norm_smul a x, Real.norm_eq_abs]
    calc
      ‖a • x‖ ^ 2 = (|a| * ‖x‖) ^ 2 := by rw [h']
      _ = a ^ 2 * ‖x‖ ^ 2 := by rw [mul_pow, sq_abs]
  have haj : ‖a • Jx‖ ^ 2 = a ^ 2 * ‖Jx‖ ^ 2 := by
    have h' : ‖a • Jx‖ = |a| * ‖Jx‖ := by
      rw [norm_smul a Jx, Real.norm_eq_abs]
    calc
      ‖a • Jx‖ ^ 2 = (|a| * ‖Jx‖) ^ 2 := by rw [h']
      _ = a ^ 2 * ‖Jx‖ ^ 2 := by rw [mul_pow, sq_abs]
  have hbx : ‖b • x‖ ^ 2 = b ^ 2 * ‖x‖ ^ 2 := by
    have h' : ‖b • x‖ = |b| * ‖x‖ := by
      rw [norm_smul b x, Real.norm_eq_abs]
    calc
      ‖b • x‖ ^ 2 = (|b| * ‖x‖) ^ 2 := by rw [h']
      _ = b ^ 2 * ‖x‖ ^ 2 := by rw [mul_pow, sq_abs]
  have hbj : ‖b • Jx‖ ^ 2 = b ^ 2 * ‖Jx‖ ^ 2 := by
    have h' : ‖b • Jx‖ = |b| * ‖Jx‖ := by
      rw [norm_smul b Jx, Real.norm_eq_abs]
    calc
      ‖b • Jx‖ ^ 2 = (|b| * ‖Jx‖) ^ 2 := by rw [h']
      _ = b ^ 2 * ‖Jx‖ ^ 2 := by rw [mul_pow, sq_abs]
  have hinner1 : inner ℝ (a • x) (b • Jx) = a * b * inner ℝ x Jx := by
    rw [inner_smul_left x (b • Jx) a, inner_smul_right x Jx b]
    norm_num
    ring
  have hinner2 : inner ℝ (a • Jx) (b • x) = a * b * inner ℝ x Jx := by
    rw [inner_smul_left Jx (b • x) a, inner_smul_right Jx x b]
    rw [real_inner_comm x Jx]
    norm_num [real_inner_comm Jx x]
    ring
  have hinner3 : inner ℝ (a • x + b • Jx) (a • Jx - b • x) =
      (a ^ 2 - b ^ 2) * inner ℝ x Jx + a * b * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) := by
    rw [inner_add_left]
    rw [inner_sub_right, inner_sub_right]
    simp only [inner_smul_left, inner_smul_right, real_inner_comm, real_inner_self_eq_norm_sq]
    norm_num [real_inner_comm x Jx]
    ring
  have h3' := norm_add_sq_real (a • x) (b • Jx)
  have h4' := norm_sub_sq_real (a • Jx) (b • x)
  rw [h3'] at h3
  rw [hax, hbj, hinner1] at h3
  rw [h4'] at h4
  rw [haj, hbx, hinner2] at h4
  rw [hinner3] at h5
  have ha2 : a ^ 2 = μ ^ 2 / 4 := by
    unfold a
    ring
  have hb2 : b ^ 2 = 1 - μ ^ 2 / 4 := by
    unfold b
    rw [σ_sq μ hμ]
  have hab : a ^ 2 + b ^ 2 = 1 := by nlinarith [ha2, hb2]
  have h_eq : a ^ 2 = 1 - b ^ 2 := by nlinarith [hab]
  have hb_pos : 0 < b := σ_pos μ hμ
  have hne : b ≠ 0 := ne_of_gt hb_pos
  have h6 : b ^ 2 * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) + 2 * (a * b) * inner ℝ x Jx = 0 := by
    nlinarith [h3, h4, h_eq]
  have h7 : (a * b) * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) - 2 * b ^ 2 * inner ℝ x Jx = 0 := by
    rw [h_eq] at h5
    nlinarith
  have h8 : b * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) + 2 * a * inner ℝ x Jx = 0 := by
    apply (mul_left_inj' hne).mp
    linarith [h6]
  have h9 : a * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) - 2 * b * inner ℝ x Jx = 0 := by
    apply (mul_left_inj' hne).mp
    linarith [h7]
  have hI : inner ℝ x Jx = 0 := by
    have h10 : a * (b * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) + 2 * a * inner ℝ x Jx) = 0 := by
      rw [h8]
      ring
    have h11 : b * (a * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) - 2 * b * inner ℝ x Jx) = 0 := by
      rw [h9]
      ring
    have h12 : -2 * (a ^ 2 + b ^ 2) * inner ℝ x Jx = 0 := by
      nlinarith [h10, h11]
    rw [hab] at h12
    linarith [h12]
  exact hI

include U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE in
set_option maxHeartbeats 400000 in
lemma J_E_norm (x : ↥Eμ) : ‖J_E U μ Eμ hEinvar x‖ = ‖x‖ := by
  have h_pos : 0 ≤ ‖J_E U μ Eμ hEinvar x‖ := norm_nonneg _
  have h_pos' : 0 ≤ ‖x‖ := norm_nonneg _
  have hI := J_E_inner_zero U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE x
  let Jx := J_E U μ Eμ hEinvar x
  let a := (μ / 2 : ℝ)
  let b := (σ μ : ℝ)
  have h1 : U_E_real U Eμ hEinvar 1 x = a • x + b • Jx := U_E_one_eq U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE x
  have h3 : inner ℝ (U_E_real U Eμ hEinvar 1 x) (U_E_real U Eμ hEinvar 1 x) = inner ℝ x x := U_E_real_preserves_inner U hUnorm Eμ hEinvar 1 x x
  rw [real_inner_self_eq_norm_sq (U_E_real U Eμ hEinvar 1 x), real_inner_self_eq_norm_sq x, h1] at h3
  have h3' := norm_add_sq_real (a • x) (b • Jx)
  rw [h3'] at h3
  have hax : ‖a • x‖ ^ 2 = a ^ 2 * ‖x‖ ^ 2 := by
    have h' : ‖a • x‖ = |a| * ‖x‖ := by
      rw [norm_smul a x, Real.norm_eq_abs]
    calc
      ‖a • x‖ ^ 2 = (|a| * ‖x‖) ^ 2 := by rw [h']
      _ = a ^ 2 * ‖x‖ ^ 2 := by rw [mul_pow, sq_abs]
  have hbj : ‖b • Jx‖ ^ 2 = b ^ 2 * ‖Jx‖ ^ 2 := by
    have h' : ‖b • Jx‖ = |b| * ‖Jx‖ := by
      rw [norm_smul b Jx, Real.norm_eq_abs]
    calc
      ‖b • Jx‖ ^ 2 = (|b| * ‖Jx‖) ^ 2 := by rw [h']
      _ = b ^ 2 * ‖Jx‖ ^ 2 := by rw [mul_pow, sq_abs]
  have hinner1 : inner ℝ (a • x) (b • Jx) = a * b * inner ℝ x Jx := by
    rw [inner_smul_left x (b • Jx) a, inner_smul_right x Jx b]
    norm_num
    ring
  rw [hax, hbj, hinner1, hI] at h3
  have ha2 : a ^ 2 = μ ^ 2 / 4 := by
    unfold a
    ring
  have hb2 : b ^ 2 = 1 - μ ^ 2 / 4 := by
    unfold b
    rw [σ_sq μ hμ]
  have hab : a ^ 2 + b ^ 2 = 1 := by nlinarith [ha2, hb2]
  have hb_pos : 0 < b := σ_pos μ hμ
  have hb2_pos : 0 < b ^ 2 := sq_pos_of_pos hb_pos
  have h_eq : b ^ 2 * (‖Jx‖ ^ 2 - ‖x‖ ^ 2) = 0 := by nlinarith [h3, hab]
  have h_cancel : ‖Jx‖ ^ 2 - ‖x‖ ^ 2 = 0 := by nlinarith [h_eq, hb2_pos]
  have h_eq2 : ‖Jx‖ ^ 2 = ‖x‖ ^ 2 := by linarith
  nlinarith [h_eq2, h_pos, h_pos']

include U hU0 hUadd hUnorm μ hμ Eμ hEinvar hU1sqE in
set_option maxHeartbeats 400000 in
theorem exists_common_eigenvector (hEμne : Eμ ≠ ⊥) :
  ∃ (v : ↥Eμ) (χ : ℝ → ℂ), v ≠ 0 ∧
    ∀ (t : ℝ), U_E_real U Eμ hEinvar t v = (χ t).re • v + (χ t).im • J_E U μ Eμ hEinvar v ∧
    ‖χ t‖ = 1 := by
  rcases exists_common_generalized_eigenvector U hUadd μ hμ Eμ hEinvar hU1sqE hEμne with ⟨v, χ, hv_ne, hgen⟩
  use v, χ
  constructor
  · exact hv_ne
  · intro t
    rcases hgen t with ⟨k, hk⟩
    letI hmod : Module ℂ ↥Eμ := complexModule U μ hμ Eμ hEinvar hU1sqE
    have hnorm_smul : ∀ (c : ℂ) (x : ↥Eμ), ‖c • x‖ = ‖c‖ * ‖x‖ := by
      intro c x
      let Jx := J_E U μ Eμ hEinvar x
      have hsmul : c • x = c.re • x + c.im • Jx := by
        have h : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
        rw [h c x]
      rw [hsmul]
      have hI : inner ℝ (c.re • x) (c.im • Jx) = 0 := by
        rw [inner_smul_left x (c.im • Jx) (c.re), inner_smul_right x Jx (c.im)]
        rw [J_E_inner_zero U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE x]
        norm_num
      have hpyt : ‖c.re • x + c.im • Jx‖ ^ 2 = (c.re ^ 2 + c.im ^ 2) * ‖x‖ ^ 2 := by
        have h' := norm_add_sq_real (c.re • x) (c.im • Jx)
        rw [h']
        have hre : ‖c.re • x‖ ^ 2 = c.re ^ 2 * ‖x‖ ^ 2 := by
          have h'' : ‖c.re • x‖ = |c.re| * ‖x‖ := by
            rw [norm_smul (c.re : ℝ) x, Real.norm_eq_abs]
          calc
            ‖c.re • x‖ ^ 2 = (|c.re| * ‖x‖) ^ 2 := by rw [h'']
            _ = c.re ^ 2 * ‖x‖ ^ 2 := by rw [mul_pow, sq_abs]
        have him : ‖c.im • Jx‖ ^ 2 = c.im ^ 2 * ‖Jx‖ ^ 2 := by
          have h'' : ‖c.im • Jx‖ = |c.im| * ‖Jx‖ := by
            rw [norm_smul (c.im : ℝ) Jx, Real.norm_eq_abs]
          calc
            ‖c.im • Jx‖ ^ 2 = (|c.im| * ‖Jx‖) ^ 2 := by rw [h'']
            _ = c.im ^ 2 * ‖Jx‖ ^ 2 := by rw [mul_pow, sq_abs]
        have hJnorm : ‖Jx‖ = ‖x‖ := J_E_norm U hUadd hUnorm μ hμ Eμ hEinvar hU1sqE x
        rw [hre, him, hI, hJnorm]
        ring
      have hc2 : ‖c‖ ^ 2 = c.re ^ 2 + c.im ^ 2 := by
        rw [← Complex.normSq_eq_norm_sq c]
        simp [Complex.normSq_apply]
        ring
      have hnonneg : 0 ≤ ‖c.re • x + c.im • Jx‖ := norm_nonneg _
      have hpos : 0 ≤ ‖c‖ * ‖x‖ := mul_nonneg (norm_nonneg _) (norm_nonneg _)
      nlinarith [hpyt, hc2, hnonneg, hpos]
    let f (t : ℝ) : Module.End ℂ ↥Eμ := {
      toFun := U_E_real U Eμ hEinvar t,
      map_add' := by
        intro x y
        exact map_add (U_E_real U Eμ hEinvar t) x y,
      map_smul' := by
        intro z x
        have h1 := U_E_smul_explicit U hUadd μ Eμ hEinvar t z x
        have hsmul : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
        rw [hsmul z x]
        rw [h1]
        have h2 : z.re • U_E_real U Eμ hEinvar t x + z.im • J_E U μ Eμ hEinvar (U_E_real U Eμ hEinvar t x) = z • U_E_real U Eμ hEinvar t x := by
          rw [hsmul z (U_E_real U Eμ hEinvar t x)]
        rw [h2]
        simp [RingHom.id_apply]
    }
    have hf_pow : ∀ (n : ℕ) (t : ℝ), f (n * t) = (f t) ^ n := by
      intro n s
      induction n with
      | zero =>
        ext x
        simp [f, U_E_real_coe, hU0]
      | succ n ih =>
        rw [show (↑(n + 1 : ℕ) : ℝ) * s = (n : ℝ) * s + s by simp; ring]
        have hadd : f ((n * s) + s) = f (n * s) * f s := by
          ext x
          simp [f, U_E_real_coe]
          rw [hUadd (↑n * s) s]
          rfl
        rw [hadd, ih]
        rw [pow_succ]
    have hf_isom : ∀ (s : ℝ) (x : ↥Eμ), ‖f s x‖ = ‖x‖ := by
      intro s x
      simp [f, U_E_real_coe, hUnorm]
    let lam := χ t
    let g_t := f t - lam • (LinearMap.id : ↥Eμ →ₗ[ℂ] ↥Eμ)
    let L_t := U_E_real U Eμ hEinvar t - (lam.re • (LinearMap.id : ↥Eμ →ₗ[ℝ] ↥Eμ)) - lam.im • (J_E U μ Eμ hEinvar : ↥Eμ →ₗ[ℝ] ↥Eμ)
    have hL : (g_t : ↥Eμ → ↥Eμ) = (L_t : ↥Eμ → ↥Eμ) := by
      funext x
      simp [f, U_E_real_coe, g_t, L_t]
      have hsmul : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
      rw [hsmul lam x]
      abel
    have hpow : ∀ (k : ℕ), (g_t ^ k) v = (L_t ^ k) v := by
      intro k
      induction k with
      | zero => simp
      | succ k ih =>
        rw [pow_succ', pow_succ']
        rw [Module.End.mul_apply, Module.End.mul_apply]
        rw [ih]
        rw [hL]
    have hgk : (g_t ^ k) v = 0 := by
      rw [hpow k]
      exact hk
    let p := fun (m : ℕ) => (g_t ^ m) v = 0
    haveI : DecidablePred p := by classical exact inferInstance
    have hex : ∃ m, p m := ⟨k, hgk⟩
    let k0 := Nat.find hex
    have h_k0_min : (g_t ^ k0) v = 0 := Nat.find_spec hex
    have hk1 : k0 = 1 := by
      by_contra h
      push_neg at h
      have hk0_pos : k0 > 0 := by
        by_contra h'
        push_neg at h'
        have : k0 = 0 := by linarith
        rw [this] at h_k0_min
        simp at h_k0_min
        contradiction
      have hk0_gt : k0 > 1 := by omega
      let m := k0 - 1
      have hm1 : m ≥ 1 := by omega
      have h_lt : m < k0 := by omega
      have hgm_ne : (g_t ^ m) v ≠ 0 := by
        have := Nat.find_min ⟨k, hgk⟩ h_lt
        simpa using this
      let w := (g_t ^ m) v
      have hw_ne : w ≠ 0 := hgm_ne
      have hw_eig : f t w = lam • w := by
        have h0 : g_t w = 0 := by
          rw [show g_t w = (g_t ^ (m + 1)) v by rw [pow_succ']; rfl]
          rw [show m + 1 = k0 by omega]
          exact h_k0_min
        have h' : f t w = g_t w + lam • w := by
          have hfeq : f t = g_t + lam • (LinearMap.id : ↥Eμ →ₗ[ℂ] ↥Eμ) := by
            simp [g_t]
          rw [hfeq]
          simp
        rw [h'] 
        rw [h0]
        simp
      have hlam_mod : ‖lam‖ = 1 := by
        have hw_norm : ‖w‖ = ‖f t w‖ := by rw [hf_isom]
        rw [hw_eig] at hw_norm
        have hnorm_smul_w := hnorm_smul lam w
        rw [hnorm_smul_w] at hw_norm
        have hw_pos : 0 < ‖w‖ := by
          rwa [norm_pos_iff]
        have : ‖lam‖ = 1 := by nlinarith
        exact this
      -- polynomial growth contradiction: a nilpotent perturbation of an isometry cannot have index > 1
      let r := k0 - 2
      have hr : k0 = r + 2 := by omega
      let u := (g_t ^ r) v
      have hgu : g_t u = w := by
        rw [show u = (g_t ^ r) v by rfl]
        rw [show w = (g_t ^ m) v by rfl]
        rw [show m = r + 1 by omega]
        rw [← Module.End.mul_apply]
        rw [pow_succ']
      have hgu2 : (g_t ^ 2) u = 0 := by
        rw [show u = (g_t ^ r) v by rfl]
        rw [← Module.End.mul_apply]
        rw [← pow_add]
        rw [show 2 + r = k0 by omega]
        exact h_k0_min
      have hu_ne : u ≠ 0 := by
        by_contra hu0
        have hw0 : w = 0 := by
          rw [← hgu, hu0]
          simp
        contradiction
      have hw_pos : 0 < ‖w‖ := by rwa [norm_pos_iff]
      have hu_pos : 0 < ‖u‖ := by rwa [norm_pos_iff]
      have hftu : (f t) u = lam • u + w := by
        have h' : (f t) u = g_t u + lam • u := by
          have hfeq : f t = g_t + lam • (LinearMap.id : ↥Eμ →ₗ[ℂ] ↥Eμ) := by
            simp [g_t]
          rw [hfeq]
          simp
        rw [h', hgu]
        abel
      have hftn : ∀ (n : ℕ), n ≥ 1 → ((f t) ^ n) u = (lam ^ n) • u + ((n : ℂ) * lam ^ (n - 1)) • w := by
        intro n hn
        refine Nat.le_induction ?_ (fun n _ ih => ?_) n hn
        · -- n = 1
          simp
          rw [hftu]
          <;> ring_nf
          <;> abel
        · -- n → n + 1
          have h1 : ((f t) ^ (n + 1)) u = (f t) (((f t) ^ n) u) := by
            rw [pow_succ']
            simp
          rw [h1, ih]
          have h2 : (f t) ((lam ^ n) • u) = (lam ^ (n + 1)) • u + (lam ^ n) • w := by
            rw [map_smul, hftu, smul_add]
            have h7 : (lam ^ n : ℂ) • (lam • u) = (lam ^ (n + 1)) • u := by
              rw [smul_smul]
              rw [mul_comm]
              rw [← pow_succ']
            rw [h7]
          have h3 : (f t) (((n : ℂ) * lam ^ (n - 1)) • w) = ((n : ℂ) * lam ^ n) • w := by
            rw [map_smul, hw_eig, smul_smul]
            have h8 : ((n : ℂ) * lam ^ (n - 1)) * lam = (n : ℂ) * lam ^ n := by
              have h9 : (lam ^ (n - 1) : ℂ) * lam = lam ^ n := by
                rw [mul_comm]
                rw [← pow_succ']
                rw [show (n - 1 : ℕ) + 1 = n by omega]
              calc
                ((n : ℂ) * lam ^ (n - 1)) * lam = (n : ℂ) * ((lam ^ (n - 1)) * lam) := by ring
                _ = (n : ℂ) * lam ^ n := by rw [h9]
            rw [h8]
          rw [map_add, h2, h3]
          have h10 : (lam ^ n : ℂ) • w + ((n : ℂ) * (lam ^ n : ℂ)) • w = (((n + 1 : ℕ) : ℂ) * (lam ^ n : ℂ)) • w := by
            rw [← add_smul]
            have h11 : (lam ^ n : ℂ) + ((n : ℂ) * (lam ^ n : ℂ)) = (((n + 1 : ℕ) : ℂ) * (lam ^ n : ℂ)) := by
              rw [Nat.cast_succ]
              ring
            rw [h11]
          rw [add_assoc]
          rw [h10]
          have h12 : n + 1 - 1 = n := by omega
          simp [h12]
          <;> ring_nf
          <;> abel
      have h_norm_lam : ∀ (n : ℕ), ‖lam ^ n‖ = 1 := by
        intro n
        rw [norm_pow]
        rw [hlam_mod]
        norm_num
      have h_norm_smul_n : ∀ (n : ℕ), ‖(n : ℂ)‖ = (n : ℝ) := by
        intro n
        simp [RCLike.norm_natCast]
      have h_lower : ∀ (n : ℕ), n ≥ 1 → ‖((f t) ^ n) u‖ ≥ |((↑n : ℝ) * ‖w‖ - ‖u‖ : ℝ)| := by
        intro n hn
        have h_eq : ((f t) ^ n) u = (lam ^ n) • u + ((n : ℂ) * lam ^ (n - 1)) • w := hftn n hn
        rw [h_eq]
        let A := (lam ^ n) • u
        let B := ((n : ℂ) * lam ^ (n - 1)) • w
        have hA : ‖A‖ = ‖u‖ := by
          simp [A, hnorm_smul, h_norm_lam n]
          all_goals norm_num
        have hB : ‖B‖ = ((n : ℝ) * ‖w‖) := by
          rw [show B = ((n : ℂ) * lam ^ (n - 1)) • w by rfl]
          rw [hnorm_smul]
          have h1 : ‖(n : ℂ) * lam ^ (n - 1)‖ = (n : ℝ) := by
            rw [norm_mul]
            rw [h_norm_lam (n - 1)]
            rw [h_norm_smul_n n]
            all_goals norm_num
          rw [h1]
          <;> ring_nf
          <;> norm_num
        have h_pos := norm_sub_norm_le B (-A)
        have h_neg := norm_sub_norm_le (-A) B
        have hneg1 : ‖-A‖ = ‖A‖ := by rw [norm_neg]
        have hsum_pos : B - -A = A + B := by
          simp [sub_neg_eq_add, A, B]
          <;> ring_nf
          <;> abel
        have hsum_neg : -A - B = -(A + B) := by
          simp [A, B]
          <;> ring_nf
          <;> abel
        rw [hneg1, hA, hB, hsum_pos] at h_pos
        rw [hneg1, hA, hB, hsum_neg, norm_neg] at h_neg
        cases' abs_cases ((↑n : ℝ) * ‖w‖ - ‖u‖ : ℝ) with h h <;> linarith [h_pos, h_neg]
      have h_isom_n : ∀ (n : ℕ), ‖((f t) ^ n) u‖ = ‖u‖ := by
        intro n
        have h_eq : (f t) ^ n = f (n * t : ℝ) := by
          rw [hf_pow n t]
        rw [h_eq]
        rw [hf_isom]
      obtain ⟨N, hN⟩ := exists_nat_gt ((2 * ‖u‖ / ‖w‖) : ℝ)
      have hN1 : N ≥ 1 := by
        by_contra h
        push_neg at h
        have hN0 : N = 0 := by linarith
        rw [hN0] at hN
        have : 0 > 2 * ‖u‖ / ‖w‖ := by nlinarith
        have : 2 * ‖u‖ / ‖w‖ ≥ 0 := by positivity
        linarith
      have hN_lower := h_lower N hN1
      have hN_isom := h_isom_n N
      have hN_gt : (↑N * ‖w‖ - ‖u‖ : ℝ) > ‖u‖ := by
        have h1 : (↑N : ℝ) * ‖w‖ > 2 * ‖u‖ := by
          have h2 : 2 * ‖u‖ / ‖w‖ < (↑N : ℝ) := hN
          have hw' : 0 < ‖w‖ := hw_pos
          rw [div_lt_iff₀ hw'] at h2
          linarith
        linarith
      have hN_abs_pos : 0 < (↑N * ‖w‖ - ‖u‖ : ℝ) := by linarith [hN_gt]
      have hN_abs : |((↑N : ℝ) * ‖w‖ - ‖u‖ : ℝ)| = (↑N * ‖w‖ - ‖u‖ : ℝ) := by
        apply abs_of_pos hN_abs_pos
      linarith [hN_lower, hN_isom, hN_gt, hN_abs]
    have hgv0 : g_t v = 0 := by
      rw [← pow_one g_t]
      rw [hk1] at h_k0_min
      exact h_k0_min
    have hlam_mod : ‖lam‖ = 1 := by
      have hv_pos : 0 < ‖v‖ := by
        rwa [norm_pos_iff]
      have h_eig : f t v = lam • v := by
        have h' : f t v = g_t v + lam • v := by
          have hfeq : f t = g_t + lam • (LinearMap.id : ↥Eμ →ₗ[ℂ] ↥Eμ) := by
            simp [g_t]
          rw [hfeq]
          simp
        rw [h', hgv0]
        simp
      have h_norm : ‖v‖ = ‖f t v‖ := by rw [hf_isom]
      rw [h_eig] at h_norm
      have hnorm_smul_v := hnorm_smul lam v
      rw [hnorm_smul_v] at h_norm
      have : ‖lam‖ = 1 := by nlinarith
      exact this
    have h_eig : f t v = lam • v := by
      have h' : f t v = g_t v + lam • v := by
        have hfeq : f t = g_t + lam • (LinearMap.id : ↥Eμ →ₗ[ℂ] ↥Eμ) := by
          simp [g_t]
        rw [hfeq]
        simp
      rw [h', hgv0]
      simp
    -- convert f t v = lam v to real expression
    have h_re : U_E_real U Eμ hEinvar t v = lam.re • v + lam.im • J_E U μ Eμ hEinvar v := by
      have h1 : U_E_real U Eμ hEinvar t v = f t v := by simp [f]
      rw [h1, h_eig]
      have hsmul : ∀ (z : ℂ) (x : ↥Eμ), z • x = z.re • x + z.im • (J_E U μ Eμ hEinvar x) := fun _ _ => rfl
      rw [hsmul lam v]
    constructor
    · exact h_re
    · exact hlam_mod

end JConstruction
