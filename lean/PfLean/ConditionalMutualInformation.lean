/-
  PfLean.ConditionalMutualInformation — finite-discrete conditional mutual
  information and the "CI → CMI = 0" bridge.

  Authors: Devin
  Started: 2026-08-20

  AXIOM POLICY: No project-specific axioms. Standard Lean foundations only.

  WHAT THIS FILE DOES (Stage 1):
    - Defines Shannon-style plog2, entropy, conditional entropy, and CMI for
      finite discrete spaces using a probability mass function `p : Ω → ℝ`.
    - Proves the algebraic core of the bridge:
      if the conditional masses factor as
        pXYZ(x,y,z) * pZ(z) = pXZ(x,z) * pYZ(y,z)
      for all x,y,z, then CMI(X;Y|Z) = 0.

  WHAT THIS FILE DOES NOT DO (Stage 2, future work):
    - Connect the mass-relation hypothesis to Mathlib's `CondIndepFun`.
      For finite discrete Z, `CondIndepFun (comap Z) X Y μ` should imply the
      above mass relation via conditional distribution disintegration. That
      equivalence is the remaining proof obligation.
    - Generalize to non-finite or non-discrete spaces.

  This is a concrete first step toward the unformalized
  `CI → CMI = 0` bridge noted in NullClassProofs.lean.
-/import Mathlib

open Real Finset

namespace ConditionalMutualInformation

noncomputable section

/- The Shannon term `-p log₂ p` with the 0·log 0 := 0 convention. -/
def plog2 (p : ℝ) : ℝ :=
  if 0 < p then - p * logb 2 p else 0

/- `plog2` is additive for an independent product of two finite probabilities. -/
lemma plog2_mul {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) :
    plog2 (a * b) = b * plog2 a + a * plog2 b := by
  unfold plog2
  by_cases ha0 : 0 < a
  · by_cases hb0 : 0 < b
    · have hab : 0 < a * b := mul_pos ha0 hb0
      have h : logb 2 (a * b) = logb 2 a + logb 2 b :=
        logb_mul (by linarith) (by linarith)
      simp [ha0, hb0, hab, h]
      ring
    · have hb0' : b = 0 := by linarith
      simp [hb0']
      try ring
  · have ha0' : a = 0 := by linarith
    by_cases hb0 : 0 < b
    · have h3 : (0 : ℝ) * b = 0 := by ring
      simp [ha0', h3]
      try ring
    · have hb0' : b = 0 := by linarith
      simp [ha0', hb0']
      try ring

/- Shannon entropy for a finite probability mass function. -/
def entropy {α : Type*} [Fintype α] (p : α → ℝ) : ℝ :=
  ∑ x, plog2 (p x)

lemma entropy_zero {α : Type*} [Fintype α] : entropy (fun _ : α => (0 : ℝ)) = 0 := by
  simp [entropy, plog2]

/- Entropy of an independent product is the sum of the entropies. -/
theorem entropy_pair_of_prod {α β : Type*} [Fintype α] [Fintype β]
    (pX : α → ℝ) (pY : β → ℝ)
    (hX : ∀ x, 0 ≤ pX x) (hY : ∀ y, 0 ≤ pY y)
    (hsumX : ∑ x, pX x = 1) (hsumY : ∑ y, pY y = 1) :
    entropy (fun (xy : α × β) => pX xy.1 * pY xy.2) = entropy pX + entropy pY := by
  have h1 : ∑ (x : α), ∑ (y : β), pY y * plog2 (pX x) =
            (∑ y, pY y) * (∑ x, plog2 (pX x)) := by
    calc
      ∑ (x : α), ∑ (y : β), pY y * plog2 (pX x)
          = ∑ (x : α), (∑ y, pY y) * plog2 (pX x) := by
            apply Finset.sum_congr rfl
            intro x _
            rw [Finset.sum_mul]
      _ = (∑ y, pY y) * ∑ (x : α), plog2 (pX x) := by
            rw [Finset.mul_sum]
  have h2 : ∑ (x : α), ∑ (y : β), pX x * plog2 (pY y) =
            (∑ x, pX x) * (∑ y, plog2 (pY y)) := by
    calc
      ∑ (x : α), ∑ (y : β), pX x * plog2 (pY y)
          = ∑ (x : α), pX x * (∑ y, plog2 (pY y)) := by
            apply Finset.sum_congr rfl
            intro x _
            rw [Finset.mul_sum]
      _ = (∑ x, pX x) * ∑ (y : β), plog2 (pY y) := by
            rw [Finset.sum_mul]
  simp only [entropy, plog2_mul (hX _) (hY _), ← Finset.univ_product_univ,
    Finset.sum_product, Finset.sum_add_distrib]
  rw [h1, h2, hsumX, hsumY]
  ring

section CMI

set_option linter.unusedSectionVars false

variable {Ω β γ S : Type*} [Fintype Ω] [Fintype β] [Fintype γ] [Fintype S]
  [DecidableEq Ω] [DecidableEq β] [DecidableEq γ] [DecidableEq S]

/- Marginal and conditional mass functions derived from a point mass function. -/
def pZ (p : Ω → ℝ) (Z : Ω → S) (z : S) : ℝ :=
  ∑ ω, if Z ω = z then p ω else 0

def pXZ (p : Ω → ℝ) (X : Ω → β) (Z : Ω → S) (x : β) (z : S) : ℝ :=
  ∑ ω, if X ω = x ∧ Z ω = z then p ω else 0

def pYZ (p : Ω → ℝ) (Y : Ω → γ) (Z : Ω → S) (y : γ) (z : S) : ℝ :=
  ∑ ω, if Y ω = y ∧ Z ω = z then p ω else 0

def pXYZ (p : Ω → ℝ) (X : Ω → β) (Y : Ω → γ) (Z : Ω → S) (x : β) (y : γ) (z : S) : ℝ :=
  ∑ ω, if X ω = x ∧ Y ω = y ∧ Z ω = z then p ω else 0

lemma pZ_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (Z : Ω → S) (z : S) : 0 ≤ pZ p Z z := by
  apply Finset.sum_nonneg
  intro ω _
  split_ifs
  · linarith [hp ω]
  · linarith

lemma pXZ_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (X : Ω → β) (Z : Ω → S) (x : β) (z : S) :
    0 ≤ pXZ p X Z x z := by
  apply Finset.sum_nonneg
  intro ω _
  split_ifs
  · linarith [hp ω]
  · linarith

lemma pYZ_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (Y : Ω → γ) (Z : Ω → S) (y : γ) (z : S) :
    0 ≤ pYZ p Y Z y z := by
  apply Finset.sum_nonneg
  intro ω _
  split_ifs
  · linarith [hp ω]
  · linarith

lemma pXYZ_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (X : Ω → β) (Y : Ω → γ) (Z : Ω → S)
    (x : β) (y : γ) (z : S) : 0 ≤ pXYZ p X Y Z x y z := by
  apply Finset.sum_nonneg
  intro ω _
  split_ifs
  · linarith [hp ω]
  · linarith

lemma sum_pXZ_eq_pZ {p : Ω → ℝ} (X : Ω → β) (Z : Ω → S) (z : S) :
    ∑ x, pXZ p X Z x z = pZ p Z z := by
  simp [pXZ, pZ]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro ω _
  by_cases h : Z ω = z
  · simp [h]
  · rw [if_neg h]
    apply Finset.sum_eq_zero
    intro x _
    split_ifs with h2
    · exfalso; exact h h2.2
    · rfl

lemma sum_pYZ_eq_pZ {p : Ω → ℝ} (Y : Ω → γ) (Z : Ω → S) (z : S) :
    ∑ y, pYZ p Y Z y z = pZ p Z z := by
  simp [pYZ, pZ]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro ω _
  by_cases h : Z ω = z
  · simp [h]
  · rw [if_neg h]
    apply Finset.sum_eq_zero
    intro y _
    split_ifs with h2
    · exfalso; exact h h2.2
    · rfl

/- pXYZ viewed as a pXZ over the paired value (Y,Z). -/
lemma pXYZ_eq_pXZ_pair {p : Ω → ℝ} (X : Ω → β) (Y : Ω → γ) (Z : Ω → S)
    (x : β) (y : γ) (z : S) :
    pXYZ p X Y Z x y z = pXZ p X (fun ω => (Y ω, Z ω)) x (y, z) := by
  simp [pXYZ, pXZ, Prod.ext_iff]

lemma pZ_pair_eq_pYZ {p : Ω → ℝ} (Y : Ω → γ) (Z : Ω → S) (y : γ) (z : S) :
    pZ p (fun ω => (Y ω, Z ω)) (y, z) = pYZ p Y Z y z := by
  simp [pZ, pYZ, Prod.ext_iff]

lemma sum_pXYZ_eq_pZ {p : Ω → ℝ} (X : Ω → β) (Y : Ω → γ) (Z : Ω → S) (z : S) :
    ∑ x, ∑ y, pXYZ p X Y Z x y z = pZ p Z z := by
  calc
    ∑ x, ∑ y, pXYZ p X Y Z x y z = ∑ y, ∑ x, pXYZ p X Y Z x y z := by rw [Finset.sum_comm]
    _ = ∑ y, pYZ p Y Z y z := by
      apply Finset.sum_congr rfl
      intro y _
      calc
        ∑ x, pXYZ p X Y Z x y z
          = ∑ x, pXZ p X (fun ω => (Y ω, Z ω)) x (y, z) := by
            apply Finset.sum_congr rfl
            intro x _
            rw [pXYZ_eq_pXZ_pair X Y Z x y z]
        _ = pZ p (fun ω => (Y ω, Z ω)) (y, z) := by
            apply sum_pXZ_eq_pZ X (fun ω => (Y ω, Z ω))
        _ = pYZ p Y Z y z := by
            apply pZ_pair_eq_pYZ Y Z y z
    _ = pZ p Z z := by
      apply sum_pYZ_eq_pZ Y Z

/- Conditional probability of X = x given Z = z. -/
def condProbX (p : Ω → ℝ) (X : Ω → β) (Z : Ω → S) (x : β) (z : S) : ℝ :=
  if 0 < pZ p Z z then pXZ p X Z x z / pZ p Z z else 0

def condProbY (p : Ω → ℝ) (Y : Ω → γ) (Z : Ω → S) (y : γ) (z : S) : ℝ :=
  if 0 < pZ p Z z then pYZ p Y Z y z / pZ p Z z else 0

def condProbXY (p : Ω → ℝ) (X : Ω → β) (Y : Ω → γ) (Z : Ω → S) (x : β) (y : γ) (z : S) : ℝ :=
  if 0 < pZ p Z z then pXYZ p X Y Z x y z / pZ p Z z else 0

lemma condProbX_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (X : Ω → β) (Z : Ω → S)
    (x : β) (z : S) : 0 ≤ condProbX p X Z x z := by
  unfold condProbX
  split_ifs with h
  · apply div_nonneg
    · exact pXZ_nonneg hp X Z x z
    · linarith [le_of_lt h]
  · linarith

lemma condProbY_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (Y : Ω → γ) (Z : Ω → S)
    (y : γ) (z : S) : 0 ≤ condProbY p Y Z y z := by
  unfold condProbY
  split_ifs with h
  · apply div_nonneg
    · exact pYZ_nonneg hp Y Z y z
    · linarith [le_of_lt h]
  · linarith

lemma condProbXY_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (X : Ω → β) (Y : Ω → γ) (Z : Ω → S)
    (x : β) (y : γ) (z : S) : 0 ≤ condProbXY p X Y Z x y z := by
  unfold condProbXY
  split_ifs with h
  · apply div_nonneg
    · exact pXYZ_nonneg hp X Y Z x y z
    · linarith [le_of_lt h]
  · linarith

lemma sum_condProbX_eq_one {p : Ω → ℝ} (X : Ω → β) (Z : Ω → S) {z : S} (hz : 0 < pZ p Z z) :
    ∑ x, condProbX p X Z x z = 1 := by
  have h : ∑ x, pXZ p X Z x z = pZ p Z z := sum_pXZ_eq_pZ X Z z
  calc
    ∑ x, condProbX p X Z x z
        = ∑ x, (pXZ p X Z x z / pZ p Z z) := by
          apply Finset.sum_congr rfl
          intro x _
          simp [condProbX, if_pos hz]
    _ = (∑ x, pXZ p X Z x z) / pZ p Z z := by rw [Finset.sum_div]
    _ = 1 := by rw [h]; field_simp [ne_of_gt hz]

lemma sum_condProbY_eq_one {p : Ω → ℝ} (Y : Ω → γ) (Z : Ω → S) {z : S} (hz : 0 < pZ p Z z) :
    ∑ y, condProbY p Y Z y z = 1 := by
  have h : ∑ y, pYZ p Y Z y z = pZ p Z z := sum_pYZ_eq_pZ Y Z z
  calc
    ∑ y, condProbY p Y Z y z
        = ∑ y, (pYZ p Y Z y z / pZ p Z z) := by
          apply Finset.sum_congr rfl
          intro y _
          simp [condProbY, if_pos hz]
    _ = (∑ y, pYZ p Y Z y z) / pZ p Z z := by rw [Finset.sum_div]
    _ = 1 := by rw [h]; field_simp [ne_of_gt hz]

/- Conditional entropy H(X|Z). -/
def condEntropyX (p : Ω → ℝ) (X : Ω → β) (Z : Ω → S) : ℝ :=
  ∑ z, pZ p Z z * entropy (fun x => condProbX p X Z x z)

def condEntropyY (p : Ω → ℝ) (Y : Ω → γ) (Z : Ω → S) : ℝ :=
  ∑ z, pZ p Z z * entropy (fun y => condProbY p Y Z y z)

def condEntropyXY (p : Ω → ℝ) (X : Ω → β) (Y : Ω → γ) (Z : Ω → S) : ℝ :=
  ∑ z, pZ p Z z * entropy (fun xy : β × γ => condProbXY p X Y Z xy.1 xy.2 z)

/- Conditional mutual information I(X;Y|Z). -/
def cmi (p : Ω → ℝ) (X : Ω → β) (Y : Ω → γ) (Z : Ω → S) : ℝ :=
  condEntropyX p X Z + condEntropyY p Y Z - condEntropyXY p X Y Z

/- The finite conditional-independence mass relation. -/
def condIndepMassRelation (p : Ω → ℝ) (X : Ω → β) (Y : Ω → γ) (Z : Ω → S) : Prop :=
  ∀ (x : β) (y : γ) (z : S),
    pXYZ p X Y Z x y z * pZ p Z z = pXZ p X Z x z * pYZ p Y Z y z

/- The core bridge: under the mass relation, CMI vanishes.
   This is stage 1; stage 2 connects the hypothesis to `CondIndepFun`. -/
theorem cmi_zero_of_mass_indep {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω)
    (X : Ω → β) (Y : Ω → γ) (Z : Ω → S)
    (h : condIndepMassRelation p X Y Z) :
    cmi p X Y Z = 0 := by
  have h2 : condEntropyXY p X Y Z = condEntropyX p X Z + condEntropyY p Y Z := by
    rw [condEntropyX, condEntropyY, condEntropyXY]
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro z _
    have hperz : entropy (fun (xy : β × γ) => condProbXY p X Y Z xy.1 xy.2 z) =
        entropy (fun x => condProbX p X Z x z) + entropy (fun y => condProbY p Y Z y z) := by
      by_cases hz : 0 < pZ p Z z
      · -- On a fiber with pZ z > 0 the conditional joint mass is the product of marginals.
        have hprod (x : β) (y : γ) :
            condProbXY p X Y Z x y z = condProbX p X Z x z * condProbY p Y Z y z := by
          simp [condProbXY, condProbX, condProbY, if_pos hz]
          have hxyz := h x y z
          field_simp [ne_of_gt hz]
          nlinarith
        rw [funext (fun (xy : β × γ) => hprod xy.1 xy.2)]
        exact entropy_pair_of_prod
          (fun x => condProbX p X Z x z)
          (fun y => condProbY p Y Z y z)
          (fun x => condProbX_nonneg hp X Z x z)
          (fun y => condProbY_nonneg hp Y Z y z)
          (sum_condProbX_eq_one X Z hz)
          (sum_condProbY_eq_one Y Z hz)
      · -- On a fiber with pZ z = 0 all conditional probabilities are zero, all entropies are zero.
        have hz' : pZ p Z z = 0 := by linarith [pZ_nonneg hp Z z, hz]
        have h0 (x : β) : condProbX p X Z x z = 0 := by
          simp [condProbX, if_neg (show ¬(0 < pZ p Z z) by linarith [hz'])]
        have h0' (y : γ) : condProbY p Y Z y z = 0 := by
          simp [condProbY, if_neg (show ¬(0 < pZ p Z z) by linarith [hz'])]
        have h0'' (xy : β × γ) : condProbXY p X Y Z xy.1 xy.2 z = 0 := by
          simp [condProbXY, if_neg (show ¬(0 < pZ p Z z) by linarith [hz'])]
        have hX0 : (fun x => condProbX p X Z x z) = (fun _ : β => (0 : ℝ)) := funext h0
        have hY0 : (fun y => condProbY p Y Z y z) = (fun _ : γ => (0 : ℝ)) := funext h0'
        have hXY0 : (fun (xy : β × γ) => condProbXY p X Y Z xy.1 xy.2 z) =
          (fun _ : β × γ => (0 : ℝ)) := funext h0''
        rw [hX0, hY0, hXY0]
        simp [entropy_zero]
    rw [hperz]
    ring
  rw [cmi, h2]
  ring

end CMI

end

end ConditionalMutualInformation
