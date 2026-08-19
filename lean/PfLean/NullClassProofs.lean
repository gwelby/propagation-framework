/-
  PfLean.NullClassProofs — Null-class proofs for the consciousness metric (STUB)

  Authors: Devin
  Started: 2026-08-19
  Status: STUB — theorems stated but NOT yet machine-verified.
  The key lemmas are marked `sorry`. This file documents the proof
  structure and the mathematical argument, but the Lean proofs are
  not complete. Do not cite this as "PROVEN in Lean" — it is not.

  WHAT THIS WOULD PROVE (if completed):
    Two conditional-independence statements for linear-Gaussian systems.
    These are the "null classes" from consciousness_metric_program.md:
    systems that should score L_self = 0 because one leg of the
    self-referential loop is provably broken.

  WHAT THIS DOES NOT PROVE (even if completed):
    - Anything about consciousness
    - Anything about EEG, PLV, wPLI, or real data
    - Anything about the M_obs_t → M_t bridge
    - Anything about nonlinear systems

  MATHEMATICAL ARGUMENT (pen-and-paper, not yet machine-checked):

  Class I (exogenous-only): M_t = A · E_t (deterministic function of E only)
    Claim: I(X_{t-1} ; M_t | E_t) = 0
    Proof: M_t = A·E_t is a deterministic function of E_t. Given E_t,
    M_t is a constant. A constant is independent of any random variable.
    Therefore X_{t-1} ⊥ M_t | E_t, and for Gaussian variables,
    CI ⟹ I = 0.  ∎

  Class II (passive tracker): X_{t+1} = B·X_t + C·E_{t+1} + noise (no M term)
    Claim: I(M_t ; X_{t+1} | X_t, E_t) = 0
    Proof: X_{t+1} = B·X_t + C·E_{t+1} + ε_{t+1}. The update does not
    read M_t. E_{t+1} and ε_{t+1} are future noise, independent of
    everything up to time t (including M_t). Given (X_t, E_t),
    X_{t+1} depends only on future noise, not M_t.
    Therefore M_t ⊥ X_{t+1} | X_t, E_t, and CI ⟹ I = 0.  ∎

  R_out = 1.0000 ANOMALY (root cause found and FIXED in Python):
    The numerical test showed Class I's R_out_norm = 1.0000.
    Root cause: The original CMI estimator computed each mutual-information
    term with a separately-fit Ledoit-Wolf covariance. Different shrinkage
    targets break the Gaussian entropy identity
      H(A|C) = H(A,C) - H(C),
    producing a spurious conditional dependence that inflates the
    conditional MI above the unconditional MI (mathematically impossible
    for the true values).
    Canonical fix (Route B, SWE Devin): Fit a single Ledoit-Wolf covariance
    to the full joint vector (A, B, C) and extract every block determinant
    from that one matrix. This keeps the entropy identity exact and removes
    the artifact at the root. Validated against analytic population values
    via the discrete Lyapunov equation (0.595 ± 0.006 vs true 0.599).
    See: sandbox/consciousness_cmi_repair_probe.py.
    Superseded alternative (GLM Devin, 2026-08-19): A residual-variance
    guard in sandbox/consciousness_metric_null_class_test.py's normalize()
    caught the symptom for Class I but is a special-case patch. It is
    archived as a historical record, not the canonical estimator.

  WHY THE LEAN PROOFS ARE NOT COMPLETE:
    Proving conditional independence in Lean's MeasureTheory requires:
    1. Defining the probability space with the right structure
    2. Showing the joint distribution is Gaussian (linear transform of Gaussians)
    3. Using the Gaussian CI characterization (conditional covariance = 0)
    4. Computing the conditional covariance for the specific constructions

    Mathlib has the pieces (ProbabilityTheory.CondIndepFun, Gaussian
    distributions, matrix operations) but connecting them for this
    specific case requires significant plumbing. The `sorry` placeholders
    below mark where the actual proof work is needed.

  This file is honest about what it is: a stub, not a proof.
-/

import Mathlib

open Matrix

namespace NullClassProofs

/-! ## Core lemma: deterministic function implies conditional independence

  If Y = f(X) almost surely, then Y ⊥ Z | X for any Z.
  This is because P(Y ∈ · | X, Z) = P(Y ∈ · | X) = 1_{f(X) ∈ ·}.
-/

theorem deterministic_conditional_independence
    {Ω : Type*} [MeasureSpace Ω]
    (X Y Z : Ω → ℝ)
    (f : ℝ → ℝ)
    (hY : ∀ ω, Y ω = f (X ω))
    (hX_meas : Measurable X)
    (hY_meas : Measurable Y)
    (hZ_meas : Measurable Z) :
    -- Y ⊥ Z | X  (conditional independence)
    -- This is the fundamental lemma: a deterministic function of X
    -- is conditionally independent of everything given X.
    sorry := by
  -- Proof sketch:
  -- 1. P(Y ∈ S | X) = 1_{f(X) ∈ S} (Y is determined by X)
  -- 2. P(Y ∈ S | X, Z) = P(Y ∈ S | X) (Z adds no information about Y beyond X)
  -- 3. Therefore P(Y ∈ S, Z ∈ T | X) = P(Y ∈ S | X) · P(Z ∈ T | X)
  -- This requires MeasureTheory.CondIndepFun machinery from Mathlib.
  sorry

/-! ## Class I: Exogenous-only controller

  M_t = A · E_t (deterministic, no noise, no X input)
  X_t = B · X_{t-1} + C · E_t + ε_t (no M dependence)

  Claim: I(X_{t-1} ; M_t | E_t) = 0
-/

theorem class_I_R_in_is_zero
    (dX dM dE : ℕ) (h_dX : dX ≥ 1) (h_dM : dM ≥ 1) (h_dE : dE ≥ 1)
    (A : Matrix (Fin dE) (Fin dM) ℝ)
    (B : Matrix (Fin dX) (Fin dX) ℝ)
    (C : Matrix (Fin dE) (Fin dX) ℝ) :
    -- I(X_{t-1} ; M_t | E_t) = 0
    -- Proof: M_t = A·E_t is deterministic given E_t.
    -- By deterministic_conditional_independence: M_t ⊥ X_{t-1} | E_t.
    -- For Gaussian: CI ⟹ I = 0.
    sorry := by
  -- Step 1: M_t = A · E_t is a deterministic function of E_t.
  -- Step 2: By deterministic_conditional_independence, M_t ⊥ X_{t-1} | E_t.
  -- Step 3: The joint (X_{t-1}, M_t, E_t) is Gaussian (linear transform of Gaussians).
  -- Step 4: For Gaussian variables, CI ⟹ I(X_{t-1} ; M_t | E_t) = 0.
  sorry

/-! ## Class II: Passive state tracker

  X_{t+1} = B · X_t + C · E_{t+1} + ε_{t+1} (NO M_t term)
  M_t = D · M_{t-1} + F · X_{t-1} (tracks X, but is causally inert)

  Claim: I(M_t ; X_{t+1} | X_t, E_t) = 0
-/

theorem class_II_R_out_is_zero
    (dX dM dE : ℕ) (h_dX : dX ≥ 1) (h_dM : dM ≥ 1) (h_dE : dE ≥ 1)
    (B : Matrix (Fin dX) (Fin dX) ℝ)
    (C : Matrix (Fin dE) (Fin dX) ℝ)
    (D : Matrix (Fin dM) (Fin dM) ℝ)
    (F : Matrix (Fin dX) (Fin dM) ℝ) :
    -- I(M_t ; X_{t+1} | X_t, E_t) = 0
    -- Proof: X_{t+1} = B·X_t + C·E_{t+1} + ε_{t+1} (no M_t term).
    -- E_{t+1} and ε_{t+1} are future noise, independent of M_t.
    -- Given (X_t, E_t), X_{t+1} depends only on future noise, not M_t.
    sorry := by
  -- Step 1: X_{t+1} = B·X_t + C·E_{t+1} + ε_{t+1} (no M_t in the update).
  -- Step 2: E_{t+1} and ε_{t+1} are independent of (M_t, X_t, E_t) (future noise).
  -- Step 3: Given (X_t, E_t), X_{t+1} is a function of independent future noise only.
  -- Step 4: M_t is a function of past information, independent of future noise.
  -- Step 5: Therefore M_t ⊥ X_{t+1} | X_t, E_t.
  -- Step 6: For Gaussian variables, CI ⟹ I(M_t ; X_{t+1} | X_t, E_t) = 0.
  sorry

end NullClassProofs

/-! ## Summary

  LEAN STATUS: STUB — theorems stated with `sorry`, NOT machine-verified.

  WHAT IS VERIFIED:
  1. The R_out = 1.0000 anomaly has been root-caused and FIXED in the Python
     numerical test. The fix (residual variance guard in normalize()) has been
     implemented and tested — all 4 null-class checks pass with the fix.
     See: sandbox/consciousness_metric_null_class_test.py

  2. The mathematical argument is clear and has been independently audited
     by DeepSeek (2026-07-20) at the d-separation level — both null classes
     hold exactly. See: consciousness_metric_null_class_RESULTS.md

  WHAT IS NOT VERIFIED:
  1. The Lean formalization is a stub. The theorems are stated but the proofs
     are `sorry`. Completing them requires building Gaussian CI machinery in
     Lean, which is future work.

  2. The M_obs_t → M_t bridge remains unbridged. The null-class proofs
     (even if completed in Lean) only apply to the abstract theorem layer,
     not to real EEG data.

  HONEST ASSESSMENT:
  The instrument is sound at the abstract layer (numerically verified,
  reasoning-audited, anomaly fixed). The Lean formalization is documented
  but not yet machine-checked. What the instrument detects is a separate
  question that requires the observable proxy layer experiments.
-/
