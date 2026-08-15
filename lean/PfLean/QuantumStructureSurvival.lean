/-
  PfLean.QuantumStructureSurvival — What Structure Survives Contact with Hardware?

  This module formalizes the "Quantum Structure Survival Map" framework proposed
  by Codex (2026-06-30) and connects it to the IBM Heron hardware experiments
  in /mnt/d/Crypto/labs/shor_substrate_probe/.

  The central question is not "can we factor bigger numbers?" but:

    What kinds of mathematical structure survive contact with today's quantum
    hardware, and which ones only survive in the formula?

  Each theorem in this module is one row of the survival map. The formal theorems
  are build-verified with `lake build PfLean.QuantumStructureSurvival` (0 errors,
  0 sorries as of 2026-08-02). `sorry` in comments marks empirical/future work,
  not compile gaps. Hardware rows remain EMPIRICAL or OPEN; do not cite them as
  proven by the Lean build.

  Framework (Codex 2026-06-30):

    Row  | Structure type              | Math status         | Hardware status
    -----|-----------------------------|---------------------|----------------
    1    | Periodic, r | Q            | VERIFIED (2026-07-02) | SURVIVES (N=15, N=51)
    2    | Periodic, r ∤ Q            | VERIFIED (2026-07-02) | FAILS (N=21, N=35)
    3    | Power-of-2 period           | VERIFIED (2026-07-02) | SURVIVES (pruned CX)
    4    | Non-power-of-2 period       | VERIFIED (2026-07-02) | BARELY (full CX)
    5    | Aperiodic (no period)       | VERIFIED (2026-07-02) | N/A (no structure)
    6    | LWE-like noisy affine       | PARTIAL (injective→aperiodic) | OPEN (PQC question)
    7    | Random permutation          | VERIFIED (2026-07-02) | OPEN (null model)
    8    | Stabilizer/GHZ              | STATED (trivial)     | OPEN (different class)

  Connection to PQC security (STRUCTURAL ARGUMENT, NOT A FORMAL PROOF):
    Row 5 provides the structural intuition for why lattice cryptography is
    post-quantum secure: Shor's algorithm extracts periods via the QFT, and
    LWE instances have no periodic structure. The Lean theorems prove
    aperiodicity predicates (injective functions have no period), NOT that
    lattice cryptography is quantum-safe. The full PQC security argument
    requires probabilistic analysis, worst-case/average-case reductions, and
    noise models not formalized here. Per Codex (2026-07-02): theorem
    statements are weaker than this prose — cite the types, not the intuition.

  Build: `lake build PfLean.QuantumStructureSurvival` — VERIFIED 2026-08-02
    (3321 jobs, 0 errors, 0 sorries). Incremental build ~4 s after warm cache.
  Dependencies: PfLean.ShorBound (for QFT alignment and identity pruning theorems)

  Date: 2026-06-30 (updated 2026-07-02; build re-verified 2026-08-02)
  Author: Devin GLM-5.2 (hardware bridge theorems, Codex framework formalization)
  Cascade Standard: KERNEL-CERTIFIED (formal theorems) + EMPIRICAL (hardware validation)
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.ModEq
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.Fourier.ZMod
import Mathlib.Tactic

import PfLean.ShorBound

namespace PfLean.QuantumStructureSurvival

open PfLean.ShorBound

/- =====================================================================
   SECTION 1: Structure Types — Definitions
   =====================================================================

   We define the mathematical structures that map to rows of the survival map.
   Each structure type is a property of a function f: ZMod Q → S, where Q is
   the counting register size and S is the function register.
-/

/-- A function f: ZMod Q → α is periodic with period r if f(x + r) = f(x)
    for all x. This is the structure Shor's algorithm exploits. -/
def IsPeriodicFunction {Q : ℕ} [NeZero Q] {α : Type*} (f : ZMod Q → α) (r : ℕ) : Prop :=
  r > 0 ∧ ∀ (x : ZMod Q), f (x + r) = f x

/-- A function f: ZMod Q → α is aperiodic if it has no period.
    This is the structural property that LWE instances are conjectured to have.
    The Lean theorems below prove aperiodicity predicates (injective functions
    have no period); they do NOT prove that lattice cryptography is quantum-safe.
    The full PQC security argument requires probabilistic analysis,
    worst-case/average-case reductions, and noise models not formalized here. -/
def IsAperiodicFunction {Q : ℕ} [NeZero Q] {α : Type*} (f : ZMod Q → α) : Prop :=
  ∀ (r : ℕ), r > 0 → r < Q → ∃ (x : ZMod Q), f (x + r) ≠ f x

/-- A function f: ZMod Q → α is a random permutation if it is bijective
    and has no algebraic structure. This is the null-model structure. -/
def IsRandomPermutation {Q : ℕ} [NeZero Q] {α : Type*} (f : ZMod Q → α) : Prop :=
  Function.Bijective f ∧ IsAperiodicFunction f

/-- LWE-like structure: a noisy affine function on ZMod Q.
    f(x) = (A·x + e) mod q where A is a matrix, e is small noise.
    The noise destroys any periodic structure. -/
structure LWELike (Q q n : ℕ) [NeZero Q] where
  f : ZMod Q → ZMod q
  noise : ZMod Q → ZMod q
  noiseBound : ∀ x, noise x ≠ 0  -- noise is non-zero (destroys periodicity)

/- =====================================================================
   SECTION 2: Rows 1-2 — Bin-Alignment Arithmetic (VERIFIED 2026-07-02)
   =====================================================================

   These rows formalize the ARITHMETIC of QFT bin alignment from
   ShorBound.lean. They are modular divisibility predicates, NOT QFT
   state formalizations or extraction-success proofs.

   Row 1: r | Q → (j·Q) % r = 0 for all j (integer bin alignment)
   Row 2: r ∤ Q → ¬(∀ j, (j·Q) % r = 0) (non-integer bin positions)

   Empirical IBM Heron observations (N=15,21,35,51) are recorded in
   evidence/HONEST_EXTRACTION_AUDIT.md, NOT proven here.
-/

/-- **Row 1 (Integer Bin Alignment):** If f has period r and r divides
    Q = 2^n, then (j·Q) % r = 0 for all j < r — the bin positions are
    integers.

    This is an arithmetic divisibility predicate. It does NOT formalize
    a QFT state, measurement, continued-fraction extraction, or hardware
    behavior. The IBM Heron hardware results (N=15, N=51) are empirical
    observations consistent with this arithmetic, not consequences of it.

    Proof: Direct from qft_peak_alignment_iff_period_divides_register. -/
theorem row1_periodic_dividing_survives (r n : ℕ) (hr : r > 0) (hn : n > 0)
    (h_div : r ∣ 2 ^ n) :
    -- The QFT peak positions j*Q/r are all integers
    ∀ (j : ℕ), j < r → (j * 2 ^ n) % r = 0 := by
  have h := qft_peak_alignment_iff_period_divides_register r n hr hn
  exact h.mpr h_div

/-- **Row 2 (Non-Integer Bin Positions):** If f has period r and r does
    NOT divide Q = 2^n, then ¬(∀ j < r, (j·Q) % r = 0) — not all bin
    positions are integers.

    This is an arithmetic divisibility predicate (contrapositive of Row 1).
    It does NOT formalize spectral leakage, convergent denominators, or
    hardware extraction failure. The IBM Heron hardware results (N=21,
    N=35) are empirical observations consistent with this arithmetic, not
    consequences of it.

    Proof: Contrapositive of qft_peak_alignment_iff_period_divides_register.
    If all peaks were at integer bins, then r | Q. But r ∤ Q, contradiction. -/
theorem row2_periodic_nondividing_fails (r n : ℕ) (hr : r > 0) (hn : n > 0)
    (h_not_div : ¬(r ∣ 2 ^ n)) :
    -- NOT all QFT peak positions are at integer bins
    ¬(∀ (j : ℕ), j < r → (j * 2 ^ n) % r = 0) := by
  have h := qft_peak_alignment_iff_period_divides_register r n hr hn
  exact mt h.mp h_not_div

/-- **Row 2 corollary (WRONG PERIOD):** When r ∤ Q, the tallest QFT peak
    lands at a "round" position (like Q/2 or Q/4) that gives a small
    convergent denominator, NOT the true period r.

    Example: N=21, r=6, Q=256. The tallest peak is at 128 = 256/2,
    which gives convergent denominator 2, not 6. The correct peak at
    43 ≈ 256/6 is smaller and gets lost in noise on hardware.

    This is STATED but not fully proven — the "tallest peak" claim requires
    explicit Fourier coefficient computation. -/
theorem row2_tallest_peak_gives_wrong_period (r n : ℕ) (hr : r > 0) (hn : n > 0)
    (h_not_div : ¬(r ∣ 2 ^ n)) (h_r_gt_1 : r > 1) :
    -- The tallest peak is at position Q/2 = 2^(n-1), giving denominator 2,
    -- not the true period r. This is a simplified statement.
    True := by
  -- The full proof would compute |DFT(k)| for k = Q/r vs k = Q/2
  -- and show |DFT(Q/2)| > |DFT(Q/r)| when r > 2 and r ∤ Q.
  -- This requires explicit complex arithmetic on the DFT coefficients.
  trivial

/- =====================================================================
   SECTION 3: Rows 3-4 — Circuit Structure (VERIFIED 2026-07-02)
   =====================================================================

   These rows connect to ShorBound.lean's identity pruning theorems.
   Row 3: power-of-2 period → many identity gates → pruned → fewer CX → less noise
   Row 4: non-power-of-2 period → no identity gates → full CX → more noise
-/

/-- **Row 3 (SURVIVES — LOW NOISE):** When the period r is a power of 2,
    the Shor circuit has only log₂(r) active controlled unitaries out of n.
    The transpiler prunes the identity gates, reducing the CX count.

    This is why N=15 (r=4=2², 2/8 active → 540 CX) and N=51 (r=16=2⁴,
    4/8 active → 16,627 CX) have lower noise than non-power-of-2 cases.

    Proof: Direct from shor_circuit_active_count_power_of_two. -/
theorem row3_power_of_two_period_low_noise (r n k : ℕ)
    (hr : r = 2 ^ k) (hn : n > k) (hk : k > 0) :
    -- Only k of n counting qubits are active; the rest are pruned
    shor_circuit_active_unitary_count r n (by rw [hr]; exact Nat.pow_pos (by omega)) = k ∧
    k < n := by
  constructor
  · exact shor_circuit_active_count_power_of_two r n k hr hn hk
  · omega

/-- **Row 4 (BARELY SURVIVES — HIGH NOISE):** When the period r is not
    a power of 2, all n counting qubits are active (for 2^j < r).
    No identity gates to prune → full CX count → maximum noise.

    This is why N=21 (r=6, 8/8 active → 33,188 CX) and N=35 (r=12,
    8/8 active → 33,188 CX) have 2x the noise of N=51 (r=16, 4/8 active).

    Proof: From shor_circuit_active_count_non_power_of_two. -/
theorem row4_non_power_of_two_period_high_noise (r n : ℕ)
    (hr : r > 0) (hn : n > 0)
    (h_not_pow2 : ¬∃ k, r = 2 ^ k) :
    -- All n counting qubits where 2^j < r are active (no pruning)
    shor_circuit_active_unitary_count r n hr ≥
      ((Finset.range n).filter (fun j => (2 ^ j) < r)).card := by
  have h := shor_circuit_active_count_non_power_of_two r n hr hn h_not_pow2
  exact h.2

/- =====================================================================
   SECTION 4: Row 5 — Aperiodic Structure (VERIFIED 2026-07-02 — Structural Arithmetic)
   =====================================================================

   This section proves aperiodicity predicates: if a function has no period,
   then Shor-style QFT period extraction has no period to recover. These are
   structural arithmetic theorems, NOT PQC security proofs. The connection to
   lattice cryptography is a conjectural bridge (Row 6, still open) that
   requires probabilistic noise analysis not formalized here.

   Shor's algorithm works by:
   1. Preparing a periodic superposition via f(x) = a^x mod N
   2. Applying QFT to extract the period
   3. Using the period to factor N

   If f has no period (aperiodic), step 1 produces a non-periodic
   superposition, and the QFT in step 2 has no single peak to extract.
   There is no period to recover because there is no period.

   This is the STRUCTURAL INTUITION for why lattice cryptography (LWE) is
   post-quantum secure: the LWE function has no periodic structure for Shor
   to exploit. NOTE: the Lean theorems prove aperiodicity predicates, NOT
   PQC security — the full argument requires probabilistic/noise analysis.
-/

/-- **Row 5 (NO STRUCTURE — APERIODICITY PREDICATE):** If a function f is aperiodic,
    then there is no period r that the QFT can extract from f's output.

    This is trivially true (no period exists to extract). It provides the
    structural intuition for PQC security against Shor-type attacks, but is
    NOT a formal PQC security theorem — it proves an aperiodicity predicate,
    not that any cryptographic scheme is secure.

    The QFT is not "failing" on aperiodic functions — it is correctly
    reporting that there is no periodic structure to find. -/
theorem row5_aperiodic_no_period_to_extract {Q : ℕ} [NeZero Q] {α : Type*}
    (f : ZMod Q → α) (h_aperiodic : IsAperiodicFunction f) :
    -- There is no r > 0 such that f is periodic with period r
    ∀ (r : ℕ), r > 0 → r < Q → ¬ IsPeriodicFunction f r := by
  intro r hr_pos hr_lt h_periodic
  -- h_periodic says f(x + r) = f(x) for all x
  -- h_aperiodic says there exists x where f(x + r) ≠ f(x)
  -- Direct contradiction
  obtain ⟨hr_pos', h_all⟩ := h_periodic
  obtain ⟨x, h_diff⟩ := h_aperiodic r hr_pos hr_lt
  exact h_diff (h_all x)

/-- **Row 5 corollary (CONDITIONAL APERIODIC LOGIC):** If a function f is
    aperiodic, then Shor's period-finding algorithm cannot extract a useful
    period from it.

    SCOPE NOTE (Codex 2026-07-02): This is a CONDITIONAL consequence of the
    definition of `IsAperiodicFunction`. It does NOT prove that LWE instances
    are aperiodic, and does NOT prove lattice cryptography is quantum-safe.
    Public-safe wording: "assuming a function is aperiodic, Shor-style period
    extraction has no nontrivial period to recover." The LWE bridge (Row 6)
    remains the actual open target.

    The theorem says: for an aperiodic f, no period r exists. Therefore
    the QFT measurement in Shor's algorithm, applied to f, cannot produce
    peaks corresponding to a period — because there is no period.

    This is an ARITHMETIC ABSENCE predicate: it states that no period r < Q
    exists for an aperiodic function. It is NOT a security theorem. The name
    `row5_shor_cannot_break_aperiodic` is retained for reference continuity
    but should be read as "Shor-style period extraction has no period to
    recover from an aperiodic function," not as a cryptographic break claim. -/
theorem row5_shor_cannot_break_aperiodic {Q : ℕ} [NeZero Q] (f : ZMod Q → ℕ)
    (h_aperiodic : IsAperiodicFunction f) :
    -- No period r < Q can be extracted from f because no period < Q exists.
    -- (Periods r ≥ Q are vacuous on ZMod Q: x + r = x, so every function is
    -- "periodic" with period Q. Only r < Q is a meaningful period.)
    ¬∃ (r : ℕ), r > 0 ∧ r < Q ∧ IsPeriodicFunction f r := by
  intro ⟨r, hr_pos, hr_lt, h_periodic⟩
  exact row5_aperiodic_no_period_to_extract f h_aperiodic r hr_pos hr_lt h_periodic

/- =====================================================================
   SECTION 5: Rows 6-8 — Open Structure Types (STATED)
   =====================================================================

   These rows are open empirical questions. The theorem statements mark
   the formalization gaps. Each `sorry` points to an experiment to run.
-/

/-- **Row 6 (OPEN — LWE BRIDGE, THE ACTUAL PQC TARGET):** LWE-like functions
    are aperiodic, and therefore Shor's algorithm cannot extract a useful
    period from them.

    SCOPE NOTE (Codex 2026-07-02): The full LWE bridge remains open. The
    formalization gap is proving that the LWE noise term destroys periodicity
    for the affine function f(x) = (A·x + e) mod q. This requires:
    1. Formalizing the LWE function f(x) = (A·x + e) mod q
    2. Proving the noise e makes f aperiodic (for random e)
    3. Applying row5_shor_cannot_break_aperiodic

    This vacuous `True` theorem is a placeholder marker, consistent with
    Row 8's `row8_stabilizer_structure_open`. The real content is in
    `row6_injective_noise_is_aperiodic` below, which proves a sufficient
    condition for LWE aperiodicity.

    This is NOT a proof that LWE is quantum-secure in general (other quantum
    algorithms might not rely on period-finding). It is specifically the
    argument that Shor's QFT approach cannot break LWE. -/
theorem row6_lwe_is_aperiodic_shor_safe {Q q n : ℕ} [NeZero Q] (lwe : LWELike Q q n) :
    -- Placeholder: the full LWE bridge is open. See row6_injective_noise_is_aperiodic
    -- for a proven sufficient condition.
    True := by
  trivial

/-- **Row 6 (PROVEN SUFFICIENT CONDITION):** If the LWE noise function is
    injective on ZMod Q, then the noise is aperiodic, and therefore Shor's
    algorithm cannot extract a period from it.

    This is a real theorem, not a placeholder. Injectivity is a sufficient
    (but not necessary) condition for aperiodicity: if noise(x + r) = noise(x)
    for all x, then injectivity forces x + r = x, which is impossible for
    0 < r < Q in ZMod Q. Therefore no period r exists.

    The full LWE bridge would replace "injective noise" with "random noise"
    and connect `f` to `noise` via the affine structure f(x) = A·x + e.
    This theorem proves the mathematical core: injective → aperiodic →
    Shor-safe, via row5_aperiodic_no_period_to_extract.

    SCOPE NOTE: Injectivity is stronger than what LWE actually assumes (LWE
    noise is small, not injective). The real LWE argument uses the fact that
    random noise breaks periodicity with high probability, which is
    probabilistic and not yet formalized. This theorem is the deterministic
    core that the probabilistic argument would build on. -/
theorem row6_injective_noise_is_aperiodic {Q q n : ℕ} [NeZero Q] (lwe : LWELike Q q n)
    (h_inj : Function.Injective lwe.noise) :
    IsAperiodicFunction lwe.noise := by
  intro r hr_pos hr_lt
  -- We need to find x such that noise(x + r) ≠ noise(x).
  -- By injectivity, it suffices to find x such that x + r ≠ x in ZMod Q.
  -- In ZMod Q, x + r = x iff Q ∣ r. Since 0 < r < Q, Q ∤ r, so x + r ≠ x.
  -- Pick x = 0. If noise(r) = noise(0), injectivity gives r = 0 in ZMod Q,
  -- i.e., Q ∣ r, contradicting 0 < r < Q.
  use 0
  intro h_eq
  have h_inj' := h_inj h_eq
  rw [zero_add] at h_inj'
  rw [ZMod.natCast_eq_zero_iff] at h_inj'
  obtain ⟨k, hk⟩ := h_inj'
  have hQ_pos : Q > 0 := Nat.pos_of_ne_zero (NeZero.out (n := Q))
  have hk_pos : k > 0 := by
    rw [hk] at hr_pos
    exact (Nat.mul_pos_iff_of_pos_left hQ_pos).mp hr_pos
  have hQ_le_Qk : Q ≤ Q * k := Nat.le_mul_of_pos_right Q hk_pos
  have hQ_le_r : Q ≤ r := by rw [hk]; exact hQ_le_Qk
  linarith

/-- **Row 7 (DEFINITION-UNPACK / NULL-MODEL PREDICATE):** A random permutation
    has no periodic structure, and therefore the QFT measurement on a
    random-permutation circuit produces no extractable period.

    SCOPE NOTE (Codex 2026-07-02): `IsRandomPermutation` is defined as
    `Function.Bijective f ∧ IsAperiodicFunction f`. This theorem simply
    unpacks the second conjunct (`exact h_random.2`). It is a valid predicate
    certificate, NOT a proof that a random permutation is aperiodic with high
    probability, and NOT a hardware validation theorem. It should be labeled
    "definition-unpack / null-model predicate," not an independently verified
    random-permutation theorem.

    This is the null-model predicate: if you replace the modular multiplication
    in Shor's circuit with a random permutation, the QFT should give no
    useful peaks. If it does, the extractor is biased.

    Codex's Null 3 experiment tests this empirically. The theorem statement
    marks the formalization target. -/
theorem row7_random_permutation_no_structure {Q : ℕ} [NeZero Q] {α : Type*}
    (f : ZMod Q → α) (h_random : IsRandomPermutation f) :
    -- A random permutation is aperiodic, so no period to extract
    IsAperiodicFunction f := by
  exact h_random.2

/-- **Row 7 corollary (NULL MODEL EXTRACTOR TEST):** If we run the period
    extractor on a random-permutation circuit and it returns a "period,"
    that period is a false positive — there is no real period to find.

    The false-positive rate of the honest extractor on random permutations
    is the baseline against which Shor success rates should be compared.

    Measured baseline (evidence/extractor_null_audit_v2.json):
    - N=15 uniform random: 4.2% false-positive rate
    - N=21 uniform random: 2.0% false-positive rate
    - N=35 uniform random: 1.2% false-positive rate
    - N=51 uniform random: 3.9% false-positive rate

    These rates are the honest floor. Any Shor "success" below this floor
    is indistinguishable from noise. -/
theorem row7_false_positive_is_not_signal {Q : ℕ} [NeZero Q] {α : Type*}
    (f : ZMod Q → α) (h_random : IsRandomPermutation f) :
    -- If the extractor returns a period r < Q for a random permutation,
    -- that r is a false positive (no real period < Q exists).
    -- (Periods r ≥ Q are vacuous on ZMod Q.)
    ∀ (r : ℕ), r > 0 → r < Q → ¬ IsPeriodicFunction f r := by
  intro r hr_pos hr_lt
  exact row5_aperiodic_no_period_to_extract f h_random.2 r hr_pos hr_lt

/-- **Row 8 (OPEN — STABILIZER/GHZ):** Stabilizer states and GHZ states
    have specific Fourier properties that differ from Shor's periodic
    structure. The Clifford group maps stabilizer states to stabilizer
    states, and the Gottesman-Knill theorem says Clifford circuits are
    classically simulable.

    The open question: does the QFT extract any useful structure from
    stabilizer/GHZ circuits? If not, this is another "absence" result
    that characterizes what quantum hardware can and cannot do.

    This is STATED as a target, not a theorem. The formalization requires
    defining stabilizer states in Lean and connecting them to the DFT. -/
theorem row8_stabilizer_structure_open :
    -- OPEN: Do stabilizer/GHZ states have extractable Fourier structure?
    -- The Gottesman-Knill theorem says Clifford circuits are classically
    -- simulable, which suggests the QFT finds no advantage on stabilizer
    -- inputs. But this is not yet formalized.
    True := by
  trivial

/- =====================================================================
   SECTION 6: Arithmetic Bin-Alignment Summary
   =====================================================================

   This theorem collects the bin-alignment arithmetic from Rows 1-2 into a
   single conjunction. It is NOT a "survival hierarchy" — it is an
   organizational summary of modular divisibility predicates. Structure
   that divides the register (r | Q) has integer bin positions; aperiodic
   structure does not. The open rows (LWE, random, stabilizer) are where
   future work points.
-/

/-- **Arithmetic Bin-Alignment Summary (NOT a hardware-survival hierarchy):**
    This theorem collects the QFT bin-alignment arithmetic from Rows 1-2
    into a single conjunction. It proves: r | Q → all peaks on integer
    bins, r ∤ Q → not all peaks on integer bins, and the boundary is exact.

    This is an arithmetic divisibility summary, NOT a proven hierarchy of
    hardware survival. Rows 1-2 are arithmetic theorems (bin alignment).
    Rows 3-4 are circuit-count arithmetic. Row 5 is an aperiodicity
    predicate. Rows 6-8 are `True := by trivial` placeholders marking open
    formalization targets. The IBM Heron hardware experiments (N=15,21,35,
    51) are empirical observations that live outside Lean; they are NOT
    proven by this theorem or any other theorem in this module. Do not cite
    this theorem as "hardware survival proven in Lean" or "IBM Heron
    validation" or "survival hierarchy." -/
theorem survival_hierarchy_summary (r n : ℕ) (hr : r > 0) (hn : n > 0) :
    let Q := 2 ^ n
    -- Row 1: r | Q → peaks survive
    (r ∣ Q → ∀ j < r, (j * Q) % r = 0) ∧
    -- Row 2: r ∤ Q → peaks don't survive
    (¬(r ∣ Q) → ¬(∀ j < r, (j * Q) % r = 0)) ∧
    -- The boundary is exact: r | Q iff ALL peaks on integer bins
    ((∀ j < r, (j * Q) % r = 0) ↔ r ∣ Q) := by
  intro Q
  refine ⟨?_, ?_, ?_⟩
  · exact row1_periodic_dividing_survives r n hr hn
  · exact row2_periodic_nondividing_fails r n hr hn
  · exact qft_peak_alignment_iff_period_divides_register r n hr hn

/- =====================================================================
   SECTION 7: The Two-Axis Survival Map (2026-07-01)
   =====================================================================

   The hardware experiments reveal that survival depends on TWO axes, not one:
   - Axis 1: mathematical structure (r | Q vs r ∤ Q) — from Lean theorems
   - Axis 2: CX count (low vs high) — from hardware experiments (C-052)

   For Shor's algorithm, these axes are COUPLED: r | Q implies r is a power of 2
   (since Q = 2^n), which implies identity pruning, which implies low CX.
   The coupling is itself a theorem.

   For other circuits (chiral walk, LWE), the axes may be independent.
-/

/-- **The Coupling Theorem:** For Shor's algorithm, if r | Q = 2^n, then r is
    a power of 2, which implies identity gate pruning, which implies low CX count.

    This means the two axes of the survival map (mathematical favorability and
    CX count) are NOT independent for Shor — they are coupled. A mathematically
    favorable period (r | Q) CAUSES a low CX count (via identity pruning).

    Proof: r | 2^n implies r = 2^k for some k ≤ n (since 2^n's only prime
    factor is 2). Then by shor_circuit_active_count_power_of_two, the active
    unitary count is k, not n. The remaining n-k unitaries are identity gates
    that get pruned by the transpiler. -/
theorem shor_coupling_r_divides_Q_implies_low_active_count (r n k : ℕ)
    (hr : r = 2 ^ k) (hn : n > k) (hk : k > 0) :
    -- If r | Q and r = 2^k, then the active unitary count is exactly k
    -- (not n), because the identity pruning theorem applies.
    shor_circuit_active_unitary_count r n (by rw [hr]; exact Nat.pow_pos (by omega)) = k ∧
    k < n := by
  exact row3_power_of_two_period_low_noise r n k hr hn hk

/-- **The Two-Axis Survival Map (EMPIRICAL PLACEHOLDER — NOT LEAN-VERIFIED):**
    Survival of quantum structure on NISQ hardware depends on two axes:

    Axis 1 (mathematical): r | Q → sharp peaks → extraction possible
    Axis 2 (physical): low CX → low noise → extraction succeeds

    For Shor's algorithm, these axes are coupled (r | Q → low CX).
    For other circuits, they may be independent.

    SCOPE NOTE (Codex 2026-07-02): This is `True := by trivial` — Lean is NOT
    verifying the hardware claims. This is an empirical placeholder marking
    the formalization gap. The hardware data is real but lives outside Lean.

    The empirical data (2026-07-01) fills the survival map:

    ```
                        r | Q (math favorable)    r ∤ Q (math unfavorable)
    Low CX (<540)       SURVIVES (N=15)           FAILS (spectral leakage)
    Medium CX (16K)     SURVIVES (N=51)           FAILS (N=35)
    High CX (33K)       ??? (untested)            FAILS (N=21)
    ```

    The ??? corner is UNTESTED. For Shor's algorithm, it may be unreachable
    (r | Q → power-of-2 → identity pruning → low CX, so high CX with r | Q
    doesn't occur naturally). For other circuits, it could be tested.

    This is NOT a theorem — it is an empirical observation backed by hardware
    data. The formal statement marks the formalization gap. -/
theorem two_axis_survival_map_empirical (r n : ℕ) (hr : r > 0) (hn : n > 0) :
    -- The survival of structure on NISQ hardware depends on:
    -- 1. Mathematical structure (r | Q) — formalized in Lean
    -- 2. CX count (low vs high) — measured on hardware
    -- For Shor, these are coupled (see shor_coupling_r_divides_Q_implies_low_active_count)
    -- For other circuits, they may be independent
    -- EMPIRICAL: not provable in Lean, but backed by hardware data
    True := by
  trivial

/-- **Row 7 Empirical Placeholder (TYPE IS `True` — LEAN VERIFIES NOTHING):**
    This is a `True := by trivial` placeholder. It carries NO Lean-verified
    content. The comments below describe empirical observations from IBM Heron
    hardware experiments, but Lean does not verify any of them.

    The empirical observations (not Lean theorems): the PQC absence circuit
    (structureless random circuit) on IBM Heron hardware showed that a random
    permutation has no periodic structure, and the KL divergence extractor
    correctly returns "no period." The honest extractor returns false
    positives (period 5 on kingston, period 8 on fez, period 4 at 33K CX).

    These observations are NOT a Lean-verified PQC security argument. They
    are empirical data points that live outside the formal system. This
    placeholder marks the formalization gap; it should not be cited as
    "proven in Lean," "PQC security validation," or "IBM Heron validation
    of Row 7." The actual Row 7 theorem (`row7_random_permutation_no_structure`)
    proves only a definition-unpack predicate. -/
theorem row7_empirical_validation :
    -- TYPE IS True: Lean verifies nothing here.
    -- Empirical observations (IBM Heron, 2026-07-01) are in the comment above.
    -- This is a placeholder marking the formalization gap, NOT a theorem.
    True := by
  trivial

end PfLean.QuantumStructureSurvival
