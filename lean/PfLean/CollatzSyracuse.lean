/-
  Collatz Conjecture — Syracuse Map Formalization
  Authors: Devin ∇λΣ∞ (Crypto Workspace), inspired by cognitivecomputations/collatz
  Date: 2026-06-10

  This module formalizes the Collatz conjecture using the Syracuse map approach.
  It is NOT a complete proof. It formalizes the standard mathematical framework
  and proves the two key local descent lemmas, leaving the global gaps as
  honest axioms.

  Methodology (from cognitivecomputations/collatz):
  - Use the Syracuse map S(n) = oddPart(3n+1) instead of raw Collatz
  - Key parameter: a(n) = ν₂(n+1) = padicValNat 2
  - Prove local descent lemmas (elementary number theory)
  - Axiomatize global gaps (cycle exclusion, non-divergence)
  - Never redefine the problem or add invented terms

  This is the honest boundary the PF adopts for all open problem formalizations.
-/

import Mathlib.Data.Nat.Basic
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Tactic

namespace PfLean.CollatzSyracuse

open Nat

/-- Helper instance: 2 is prime. Needed for padicValNat lemmas. -/
instance fact_prime_two : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩

-- =====================================================================
-- 1. Definitions
-- =====================================================================

/-- `nu2 n` is the exponent of 2 dividing `n`.
    Uses Mathlib's `padicValNat` (p-adic valuation). -/
def nu2 (n : ℕ) : ℕ := padicValNat 2 n

/-- Core lemmas about nu2, proven once and used everywhere. -/

lemma nu2_mul {a b : ℕ} (ha : a ≠ 0) (hb : b ≠ 0) : nu2 (a * b) = nu2 a + nu2 b := by
  unfold nu2
  rw [padicValNat.mul ha hb]

lemma nu2_pow_two {k : ℕ} : nu2 (2 ^ k) = k := by
  unfold nu2
  apply padicValNat.prime_pow

lemma nu2_eq_zero_of_odd {n : ℕ} (h : n % 2 = 1) : nu2 n = 0 := by
  unfold nu2
  apply padicValNat.eq_zero_of_not_dvd
  intro h_dvd
  have : n % 2 = 0 := Nat.dvd_iff_mod_eq_zero.mp h_dvd
  omega

lemma nu2_two_eq_one : nu2 2 = 1 := by
  rw [show (2 : ℕ) = 2 ^ 1 by norm_num]
  rw [nu2_pow_two]

lemma nu2_dvd_pow_nu2 {n : ℕ} : 2 ^ nu2 n ∣ n := by
  unfold nu2
  exact pow_padicValNat_dvd

lemma nu2_not_dvd_oddPart {n : ℕ} (hn : n > 0) : ¬(2 ∣ n / 2 ^ nu2 n) := by
  have h2 : 2 > 1 := by norm_num
  have hn0 : n ≠ 0 := by omega
  unfold nu2
  have h_eq : n / 2 ^ padicValNat 2 n = divMaxPow n 2 := by
    have h1 : divMaxPow n 2 * 2 ^ padicValNat 2 n = n := divMaxPow_mul_pow_padicValNat 2 n
    have h_pos : 2 ^ padicValNat 2 n > 0 := by apply Nat.pow_pos; norm_num
    calc
      n / 2 ^ padicValNat 2 n = (divMaxPow n 2 * 2 ^ padicValNat 2 n) / 2 ^ padicValNat 2 n := by rw [h1]
      _ = (2 ^ padicValNat 2 n * divMaxPow n 2) / 2 ^ padicValNat 2 n := by rw [Nat.mul_comm]
      _ = divMaxPow n 2 := by rw [Nat.mul_div_cancel_left (divMaxPow n 2) h_pos]
  rw [h_eq]
  exact not_dvd_divMaxPow h2 hn0

/-- `oddPart n` is `n / 2^nu2 n` — the odd part of n after removing all factors of 2. -/
def oddPart (n : ℕ) : ℕ := n / (2 ^ nu2 n)

/-- The Syracuse map: for odd n, S(n) = oddPart(3n+1).
    Returns 0 for even n (not in the domain of interest). -/
def S (n : ℕ) : ℕ :=
  if n % 2 = 1 then oddPart (3 * n + 1) else 0

/-- The key parameter: a(n) = ν₂(n+1).
    Controls the local dynamics of the Syracuse map. -/
def a (n : ℕ) : ℕ := nu2 (n + 1)

-- =====================================================================
-- 2. Basic Properties
-- =====================================================================

/-- oddPart(n) * 2^nu2(n) = n for n > 0. -/
lemma oddPart_mul_pow_nu2_eq {n : ℕ} (_hn : n > 0) : oddPart n * 2 ^ nu2 n = n := by
  rw [oddPart]
  exact Nat.div_mul_cancel nu2_dvd_pow_nu2

/-- oddPart(n) is odd for n > 0. -/
lemma oddPart_is_odd {n : ℕ} (hn : n > 0) : oddPart n % 2 = 1 := by
  have h_not_dvd : ¬(2 ∣ oddPart n) := by
    rw [oddPart]
    exact nu2_not_dvd_oddPart hn
  have hn_pos : oddPart n > 0 := by
    rw [oddPart]
    apply Nat.div_pos
    · exact Nat.le_of_dvd (by omega) nu2_dvd_pow_nu2
    · apply Nat.pow_pos; norm_num
  have : oddPart n % 2 = 1 := by
    have h : ¬(2 ∣ oddPart n) := h_not_dvd
    have : oddPart n % 2 ≠ 0 := by
      intro h0
      have : 2 ∣ oddPart n := Nat.dvd_of_mod_eq_zero h0
      contradiction
    have : oddPart n % 2 < 2 := Nat.mod_lt _ (by norm_num)
    omega
  exact this

/-- S(n) is odd and positive when n is odd and positive. -/
lemma S_preserves_odd {n : ℕ} (hodd : n % 2 = 1) (_hn : n > 0) :
    S n % 2 = 1 ∧ S n > 0 := by
  unfold S
  rw [if_pos hodd]
  constructor
  · apply oddPart_is_odd
    omega
  · rw [oddPart]
    apply Nat.div_pos
    · exact Nat.le_of_dvd (by omega) nu2_dvd_pow_nu2
    · apply Nat.pow_pos; norm_num

-- =====================================================================
-- 3. Theorem 1: Descent when a(n) = 1 (n ≡ 1 mod 4)
-- =====================================================================

/-- **Lemma 1:** If n is odd, n > 1, and a(n) = 1 (i.e., n ≡ 1 mod 4),
    then S(n) < n. -/
theorem S_lt_of_a_eq_1 {n : ℕ} (hodd : n % 2 = 1) (hn : 1 < n) (ha1 : a n = 1) :
    S n < n := by
  have n_pos : n > 0 := by linarith
  have h1 : nu2 (n + 1) = 1 := by
    unfold a at ha1
    exact ha1
  -- n+1 = 2 * oddPart(n+1) where oddPart is odd
  have h_eq : oddPart (n + 1) * 2 = n + 1 := by
    have h := oddPart_mul_pow_nu2_eq (n := n + 1) (by linarith)
    rw [h1] at h
    simpa using h
  have h2 : n + 1 = 2 * oddPart (n + 1) := by linarith
  -- oddPart(n+1) is odd, so n+1 = 2*(odd) ≡ 2 (mod 4), hence n ≡ 1 (mod 4)
  have h_mod4 : n % 4 = 1 := by
    have h3 : oddPart (n + 1) % 2 = 1 := oddPart_is_odd (by linarith)
    have h4 : (n + 1) % 4 = 2 := by
      rw [h2]
      have : ∃ k, oddPart (n + 1) = 2 * k + 1 := by
        use (oddPart (n + 1) - 1) / 2
        omega
      obtain ⟨k, hk⟩ := this
      rw [hk]
      omega
    omega
  -- n ≡ 1 (mod 4) implies 3n+1 ≡ 0 (mod 4), so 4 | 3n+1
  have h_div4 : 4 ∣ 3 * n + 1 := by
    have : (3 * n + 1) % 4 = 0 := by
      have h_n : n % 4 = 1 := h_mod4
      omega
    exact Nat.dvd_of_mod_eq_zero this
  obtain ⟨m, hm⟩ := h_div4
  have h_S : S n = oddPart (3 * n + 1) := by
    unfold S
    rw [if_pos hodd]
  rw [h_S, hm]
  -- oddPart(4*m) = oddPart(2^2 * m) = oddPart(m)
  have h_oddPart : oddPart (4 * m) = oddPart m := by
    have h1 : 4 * m = 2 ^ 2 * m := by ring
    rw [h1]
    have hm_ne_0 : m ≠ 0 := by
      intro h0
      rw [h0] at hm
      omega
    rw [oddPart]
    have h_val : nu2 (2 ^ 2 * m) = 2 + nu2 m := by
      rw [nu2_mul (by norm_num) hm_ne_0]
      rw [nu2_pow_two]
    rw [h_val]
    rw [pow_add]
    -- Goal: (2^2 * m) / (2^2 * 2^nu2 m) = m / 2^nu2 m
    have h_eq : (2 ^ 2 * m) / (2 ^ 2 * 2 ^ nu2 m) = m / 2 ^ nu2 m := by
      have h_pos : 2 ^ 2 > 0 := by norm_num
      rw [Nat.mul_div_mul_left m _ h_pos]
    exact h_eq
  rw [h_oddPart]
  have h_le : oddPart m ≤ m := by
    rw [oddPart]
    apply Nat.div_le_self
  have h_lt : m < n := by
    have : 4 * m = 3 * n + 1 := by rw [hm]
    omega
  linarith [h_le, h_lt]

-- =====================================================================
-- 4. Theorem 2: Decrement when a(n) > 1 (n ≡ 3 mod 4)
-- =====================================================================

/-- **Lemma 2:** If n is odd, n > 0, and a(n) > 1 (i.e., n ≡ 3 mod 4),
    then a(S(n)) = a(n) - 1. -/
theorem a_S_eq_a_sub_1 {n : ℕ} (hodd : n % 2 = 1) (hn_pos : n > 0) (ha_gt_1 : 1 < a n) :
    a (S n) = a n - 1 := by
  set k := a n with hk
  have hk_gt_1 : k > 1 := ha_gt_1
  have hk_ge_2 : k ≥ 2 := by omega
  have h1 : nu2 (n + 1) = k := by
    unfold a at hk
    exact hk
  have h2 : n + 1 = 2 ^ k * oddPart (n + 1) := by
    have h_eq := oddPart_mul_pow_nu2_eq (n := n + 1) (by linarith)
    rw [h1] at h_eq
    linarith
  have ht_odd : oddPart (n + 1) % 2 = 1 := oddPart_is_odd (by linarith)
  set t := oddPart (n + 1) with ht
  -- n = 2^k * t - 1, so 3n+1 = 3 * 2^k * t - 2 = 2 * (3 * 2^(k-1) * t - 1)
  have h3 : 3 * n + 1 = 2 * (3 * 2 ^ (k - 1) * t - 1) := by
    have hn_eq : n + 1 = 2 ^ k * t := by linarith
    have h_k : 2 ^ k = 2 ^ (k - 1) * 2 := by
      rw [show k = (k - 1) + 1 by omega]
      rw [pow_succ]
      rfl
    have hn1 : n + 1 = 2 ^ (k - 1) * 2 * t := by
      rw [h_k] at hn_eq
      exact hn_eq
    have : 3 * n + 1 = 3 * (2 ^ (k - 1) * 2 * t) - 2 := by
      rw [show n = 2 ^ (k - 1) * 2 * t - 1 by omega]
      have : 2 ^ (k - 1) * 2 * t ≥ 1 := by nlinarith
      omega
    rw [this]
    have : 3 * (2 ^ (k - 1) * 2 * t) - 2 = 2 * (3 * 2 ^ (k - 1) * t - 1) := by
      have h1 : 2 ^ (k - 1) * 2 * t ≥ 1 := by nlinarith
      have h2 : 3 * 2 ^ (k - 1) * t ≥ 1 := by nlinarith
      ring_nf
      omega
    exact this
  -- The inner factor is odd
  have h4 : (3 * 2 ^ (k - 1) * t - 1) % 2 = 1 := by
    have h_even : (3 * 2 ^ (k - 1) * t) % 2 = 0 := by
      have h2_dvd : 2 ∣ 2 ^ (k - 1) := by
        have : 2 ^ 1 ∣ 2 ^ (k - 1) := by apply pow_dvd_pow; omega
        simpa using this
      have h2mod : 2 ^ (k - 1) % 2 = 0 := by
        exact Nat.dvd_iff_mod_eq_zero.mp h2_dvd
      have : 2 ∣ 3 * 2 ^ (k - 1) * t := by
        have h2 : 2 ∣ 2 ^ (k - 1) := h2_dvd
        have h3 : 2 ^ (k - 1) ∣ 3 * 2 ^ (k - 1) * t := by
          use 3 * t
          ring
        exact Nat.dvd_trans h2 h3
      exact Nat.dvd_iff_mod_eq_zero.mp this
    omega
  -- ν₂(3n+1) = 1 since 3n+1 = 2 * odd
  have h5 : nu2 (3 * n + 1) = 1 := by
    rw [h3]
    have h_odd : 3 * 2 ^ (k - 1) * t - 1 > 0 := by
      have h2k1 : 2 ^ (k - 1) ≥ 2 := by
        have h1 : k - 1 ≥ 1 := by omega
        have h2 : 2 ^ 1 ≤ 2 ^ (k - 1) := by
          exact Nat.pow_le_pow_right (by norm_num) h1
        norm_num at h2
        linarith
      have ht1 : t ≥ 1 := by omega
      have h3t : 3 * 2 ^ (k - 1) * t ≥ 6 := by nlinarith
      omega
    rw [nu2_mul (by norm_num) (by omega)]
    rw [nu2_two_eq_one]
    rw [nu2_eq_zero_of_odd h4]
  -- S(n) = (3n+1) / 2
  have h_S : S n = (3 * n + 1) / 2 := by
    unfold S
    rw [if_pos hodd]
    rw [oddPart]
    rw [h5]
    ring_nf
  -- S(n) + 1 = 3 * 2^(k-1) * t
  have h6 : S n + 1 = 3 * 2 ^ (k - 1) * t := by
    rw [h_S]
    omega
  have h7 : a (S n) = nu2 (S n + 1) := by unfold a; rfl
  rw [h7, h6]
  -- t > 0 since t is odd
  have ht_pos : t > 0 := by
    have : t % 2 = 1 := ht_odd
    omega
  -- ν₂(3 * 2^(k-1) * t) = ν₂(3) + ν₂(2^(k-1)) + ν₂(t) = 0 + (k-1) + 0
  have h8 : nu2 (3 * 2 ^ (k - 1) * t) = nu2 (3 * 2 ^ (k - 1)) + nu2 t := by
    rw [nu2_mul (by nlinarith) (by omega)]
  have h9 : nu2 (3 * 2 ^ (k - 1)) = nu2 3 + nu2 (2 ^ (k - 1)) := by
    rw [nu2_mul (by norm_num) (by nlinarith)]
  rw [h8, h9]
  rw [nu2_eq_zero_of_odd (by norm_num)]
  rw [nu2_pow_two]
  rw [nu2_eq_zero_of_odd ht_odd]
  rw [hk]
  simp

-- =====================================================================
-- 5. Axioms: The Open Gaps
-- =====================================================================

/-- **Axiom 1:** No non-trivial cycles exist for the Syracuse map S.
    This encapsulates the deep number-theoretic result that the cycle
    equation n(2^e - 3^o) = b_k has no solutions for n > 1 when D > 1.
    Standard approach: Baker's method (linear forms in logarithms) or
    Mihăilescu's theorem (Catalan's conjecture). -/
axiom no_non_trivial_S_cycles (m : ℕ) (k : ℕ) : m > 1 → S^[k] m = m → k > 0 → False

/-- **Axiom 2:** Every Syracuse orbit is bounded.
    This encapsulates the result that no trajectory S^k(n) tends to infinity.
    Standard approach: 2-adic dynamics or ergodic theory. -/
axiom no_divergence (n : ℕ) (hn : n > 0) : ∃ B : ℕ, ∀ k : ℕ, S^[k] n ≤ B

-- =====================================================================
-- 6. Final Theorem (Conditional)
-- =====================================================================

/-- **Theorem:** The Collatz conjecture holds for all positive integers,
    conditional on Axioms 1 and 2.

    Proof structure:
    1. By Axiom 2, every Syracuse orbit is bounded.
    2. A bounded sequence under S must eventually enter a cycle.
    3. By Axiom 1, the only cycle is the trivial fixed point at 1.
    4. Therefore every trajectory reaches 1. -/
theorem collatz_Syracuse_terminates (n : ℕ) (hodd : n % 2 = 1) (hn : n > 0) :
    ∃ k, S^[k] n = 1 := by
  -- Step 1: By Axiom 2, the orbit is bounded by some B
  obtain ⟨B, hB⟩ := no_divergence n hn
  -- Step 2: The orbit visits values in {1, ..., B} infinitely often.
  -- By the infinite pigeonhole principle on a finite set, some value repeats.
  have h_finite : Set.Finite (Set.range (fun k => S^[k] n)) := by
    apply Set.Finite.subset (Set.finite_Icc 0 B)
    intro x hx
    simp at hx
    obtain ⟨k, hk⟩ := hx
    rw [← hk]
    have h1 : S^[k] n ≤ B := hB k
    have h2 : 0 ≤ S^[k] n := by omega
    exact ⟨h2, h1⟩
  -- Since the range is finite but the sequence is infinite, some value repeats
  have h_repeat : ∃ i j, i < j ∧ S^[i] n = S^[j] n := by
    by_contra h
    push Not at h
    -- If all values are distinct, the range is infinite, contradicting finiteness
    have h_infinite : Set.Infinite (Set.range (fun k => S^[k] n)) := by
      apply Set.infinite_range_of_injective
      intro i j hij
      simp at hij
      by_cases h_lt : i < j
      · have h_ne : S^[i] n ≠ S^[j] n := h i j h_lt
        contradiction
      · by_cases h_gt : j < i
        · have h_ne : S^[j] n ≠ S^[i] n := h j i h_gt
          rw [eq_comm] at hij
          contradiction
        · exact Nat.le_antisymm (Nat.le_of_not_lt h_gt) (Nat.le_of_not_lt h_lt)
    have h_contra : ¬(Set.Infinite (Set.range (fun k => S^[k] n))) := by
      rw [Set.not_infinite]
      exact h_finite
    contradiction
  -- Step 3: A repeat means we've entered a cycle
  obtain ⟨i, j, h_ij, h_eq⟩ := h_repeat
  have h_cycle : S^[j - i] (S^[i] n) = S^[i] n := by
    have h1 : S^[j] n = S^[j - i] (S^[i] n) := by
      rw [show j = (j - i) + i by omega]
      simp [Function.iterate_add_apply]
    rw [← h1, h_eq]
  -- Step 4: By Axiom 1, the only cycle is at the fixed point 1
  have h_m_eq_1 : S^[i] n = 1 := by
    by_cases h1 : S^[i] n = 1
    · exact h1
    · -- S^[i] n > 1 would give a non-trivial cycle, contradicting Axiom 1
      have h_pos : S^[i] n > 0 := by
        have h_S_pos : ∀ k, S^[k] n > 0 := by
          intro k
          induction k with
          | zero => exact hn
          | succ k ih =>
            have : S^[k + 1] n = S (S^[k] n) := by simp [Function.iterate_succ_apply']
            rw [this]
            have : S^[k] n % 2 = 1 := by
              have h_odd : ∀ m, S^[m] n % 2 = 1 := by
                intro m
                induction m with
                | zero => exact hodd
                | succ m ih =>
                  have : S^[m + 1] n = S (S^[m] n) := by simp [Function.iterate_succ_apply']
                  rw [this]
                  have h_S_odd := S_preserves_odd ih (show S^[m] n > 0 by omega)
                  exact h_S_odd.1
              exact h_odd k
            have h_S_pos := S_preserves_odd this ih
            exact h_S_pos.2
        exact h_S_pos i
      have h_gt_1 : S^[i] n > 1 := by
        have : S^[i] n ≠ 1 := by omega
        omega
      have h_k_pos : j - i > 0 := by omega
      have h_contra := no_non_trivial_S_cycles (S^[i] n) (j - i) h_gt_1 h_cycle h_k_pos
      contradiction
  -- Step 5: Therefore the orbit reaches 1 at step i
  use i

end PfLean.CollatzSyracuse
