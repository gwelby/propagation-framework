# The Axiom 3 Formalization Wall — Consolidated State
*Written 2026-07-31 by Devin, deferred to post-paper per standing decision.*

**Purpose:** One document that captures the full state of the Axiom 3 formalization gap so it doesn't need re-discovering from scratch when picked back up. Carried forward, not dropped.

**Status:** DEFERRED. The falsification paper (v0.5) is the priority. Return to this after the paper ships.

---

## The Gap in One Sentence

Axiom 3 as currently stated ("coherent propagation persists; incoherent propagation disperses") is compatible with `γβⁿ = √C₂` for any integer n. It cannot select n=2 (the correct Casimir polynomial) over n=1 (wrong). Every formalization attempt has converged on this same wall.

---

## What the Polynomial Is

The Casimir polynomial: `x² + C₂x - C₂ = 0` where `x = β² = v²/c²`.

- Gives the Weinberg angle: `sin²θ_W ≈ 0.22310` (matches PDG to 0.13σ)
- Empirically correct. The question is whether it can be **derived from the PF axioms**, not whether it's right.
- Axiom 2 is essential (Route E proved this — non-relativistic limit is 3× wrong)
- The extra β is specifically the relativistic contribution
- The gap is: why does relativistic coherence select `γβ²` rather than `γβ`?

---

## H8 in Lean — The Current Formalization

**File:** `/mnt/d/Fundamentals/lean/PfLean/Axioms.lean`, line 115

**Definition (`Hypothesis_Coherence`):**
- (a) Approximate recurrence: `∃ s τ > 0, d(s, propagate(τ, s)) < causal_velocity · τ`
- (b) Lyapunov stability: small perturbations stay small under propagation

**What H8 gives you:** Recurrence + stability. This is enough for the compact-orbit theorem (H3+H2+H14+H5+H21+H22+IP → nonzero periodic orbit, PROVEN with 0 sorrys via `PeriodOrbitRefactor.lean`).

**What H8 does NOT give you:** A selection principle. H8 says "some propagations are special" but does not say which ones, or why n=2 over n=1. The compact-orbit theorem proves existence of periodic orbits under isometry + finite-dim + continuity; it does not select among coherent candidates.

**Honest limit:** H8 is neither strictly weaker nor strictly stronger than exact periodicity (stability is an added premise). The real question — "what MORE do we need to select the correct coherence condition?" — is open.

---

## All 8+ Routes and Why Each Failed

### Routes that sharpen but don't close

| Route | Approach | What it proved | Where it fails |
|-------|----------|----------------|----------------|
| **A** (de Broglie) | Relativistic standing-wave kinematics | Standard mechanics gives `γβ = √C₂` → wrong form | Why does the self-consistency variable become `γβ²` instead of `γβ`? |
| **C** (Laplacian) | Medium eigenvalue equation | Polynomial reads cleanly as PF resonance condition | Why `x²/(1-x) = C₂` rather than `x/(1-x) = C₂`? Same gap as Route A. |
| **E** (Virial) | Refractive stress balance | **Axiom 2 is essential.** Non-relativistic gives R ≈ 0.643 (3× wrong). Relativistic gives R ≈ 0.223 (correct). α=2 forced by relativistic dispersion. | Why does a relativistic spinning mode satisfy `β²/√(1-β²) = √C₂` specifically? |
| **Constraints** | Algebraic uniqueness | Three constraints uniquely select the polynomial. Two have PF-native arguments. | The third (g₁=−f₁) is algebraically equivalent to Route A's gap. |
| **F** (Coherence functional) | Drift-rotation locking | IF `r_lock = βr_C`, THEN `L = γβ²ℏ` and polynomial follows. Cleanest geometric ansatz. | Why does Axiom 3 → `ωr = v`? The functional `Φ(r) = ωr - v` has units of velocity, not phase. |
| **G** (Two-sector) | 2×2 coupling matrix | `det(M) = 0` gives the polynomial algebraically. | Why is the off-diagonal coupling exactly `√C₂`? What operator mediates it? |
| **H** (Helical phase-matching) | Action resonance | **Cleanest reformulation.** `J_z = 2πγβ²ℏ` (algebra correct). IF `J_z = J_θ` THEN polynomial follows. | Why does Axiom 3 → 1:1 action resonance? Standard resonance is frequency commensurability, not action equality. |

### Routes that are no-go

| Route | Why it's no-go |
|-------|----------------|
| **B** (Lagrangian) | Current PF Lagrangian is scalar. No spin structure. C₂ does not appear. Would need spinning-field extension derived from PF axioms. |
| **D** (Holonomy) | N=3 phase walk holonomy is scalar on each spin sector. Cross-sector coupling required but absent from current PF. |
| **Lemma 1** (radius scaling) | Contradicts de Broglie wavelength relation. Double-counts velocity dependence. |
| **Lemma 3** (propagator pole) | Requires field-theoretic machinery beyond current PF axioms. |

### Closure paths ruled out

| Path | Why ruled out |
|------|---------------|
| Wigner rotation | Coaxial helical geometry → trivial Wigner rotation. Thomas precession contributes nothing. |
| Cross-loop coherence | Individual quantization of J_θ and J_z already ensures all loops coherent. J_θ = J_z is NOT required by Axiom 3 alone. |

---

## Three Recent Formalization Attempts (All Failed)

### 1. Family C — Mutual Information (DIED 2026-07-29)

**File:** `derivations/casimir_axiom3_mutual_information_correction_2026-07-29.md`

**Approach:** Formalize Axiom 3 as mutual information maximization `I(Φ_int; Φ_ext)`. Two-part argument: periodicity eliminates k<1, MI maximization eliminates k>1.

**What killed it:** The penalty is **partition-dependent**. A half-bin offset on the external grid collapses the k=1/2 penalty from 0.693 to 0.00006 — four orders of magnitude. The k=1 advantage over k=1/2 was entirely a bin-alignment artifact.

**What survives:** Under aligned bins, k=1 has the highest MI (numerical observation, not proof). The companion script (`sandbox/casimir_mi_bin_offset_control.py`) exists for testing further perturbations.

**Status:** Gap 1 NOT closed. Gap 2 (Axiom 3 = MI maximization) remains open. The MI approach may be measuring partition structure, not physical selection.

### 2. Axiom 3 → QFT (DIED 2026-07-30, overclaim)

**File:** `audit/crypto_axiom3_qft_overclaim_audit_2026-07-30.md`

**Approach:** Crypto Devin claimed Axiom 3 derives the QFT success probability (C-063, ARGUED 0.65).

**What killed it:** Five defects:
1. Uses the same Axiom 3 we just proved is underdetermined
2. Standard Fourier analysis with Axiom 3 labels attached (relabeling, not derivation)
3. The "iff" claim is false — the peak is algebraic, exists in pure math with no coherence
4. QEM "confirmation" doesn't discriminate Axiom 3 from any noise model
5. "Original research" is misleading — strip the labels, get Nielsen & Chuang §5.3

**Status:** C-063 demoted to ARGUED 0.45 (physical interpretation, not derivation). C-062 (QEM monotonic improvement, EMPIRICAL 0.80) stands.

### 3. Coherence Budget Pre-Registration (H1 DIED 2026-07-30)

**File:** `/mnt/d/Crypto/derivations/coherence_budget_pre_registration_2026-07-30.md`

**Approach:** Pre-registered hypothesis: does `(1-p)^depth` predict extraction success across the 3,201-row leaderboard? Salvaged from killed C-063 as pure empirics.

**What killed H1:** The leaderboard was a negative — the coherence budget model did not predict success_rate better than a constant or backend-only model on the held-out test split.

**What survives:** C-062 (single-circuit QEM monotonic improvement, EMPIRICAL 0.80). The bridge to Fundamentals is NOT ARGUED 0.45 — it's weaker, maybe ARGUED 0.30 or "within-condition only, doesn't generalize across circuits."

### 4. O2bis Correlation Functional (CLASSICAL RESULT ONLY, 2026-07-29)

**File:** `derivations/o2bis_analytic_kickstart_2026-07-29.md`

**Approach:** OU-Markov correlation functional `G(a)` for the 3-cycle transition matrix. For positive exponential OU noise, `dG/da > 0`, so a=0 is the unique minimum.

**What limits it:** The CPTP no-selection negative control shows no selection in the natural open-system completion. The result is **PROVEN (classical)** / **EMPIRICAL (postselection)** / **UNDERDETERMINED (physical selection)**. It's a Python-sandbox result, not a Lean theorem, and does not bridge to Axiom 3 formalization.

---

## The Two Foundational Sub-Audits (Codex-Demoted)

### Step A: Why `J_θ = 2π√C₂ħ` (magnitude, not projection)

**Claim:** Axiom 2 → isotropy → SO(3) symmetry → J_θ uses |J| = √C₂ħ (magnitude), not m_j ħ (projection).

**Codex verdict: ARGUED (strong), not DERIVED.** Three objections:
1. Axiom 2 does not explicitly state isotropy
2. Isotropy of medium ≠ isotropy of internal motion
3. The action integral's cycle is not specified

**What's missing:** Derivation that the internal cycle of a fundamental mode is itself SO(3)-invariant.

### Step B: Why `k = 1` (1:1 resonance, not k:1)

**Claim:** Axiom 3 + Axiom 1 → k=1 (primitive loop, not k-fold composite).

**Codex verdict: ARGUED, not DERIVED.** Four objections:
1. Axiom 3 requires coherence, not energy minimization
2. Coherence alone underdetermines selection
3. The argument smuggles in a coherence cost functional not yet defined
4. Axiom 1 does not define "fundamental" in a way that uniquely selects 1:1

**What's missing:** A formal principle that, among coherent helical resonances, selects k=1.

---

## The Pattern — Why Defer Now

Three independently-designed approaches failed in three different ways, converging on the same wall:
- Family C: partition-dependence (subtle numerical flaw)
- C-063: overclaim (standard math with axiom labels)
- Coherence budget: negative leaderboard (empirical falsification)

This is the same shape as a KNOW Graph pattern: real effort, real attempts, not converging. The difference is this one doesn't even have a shrinking-residual number to point to.

The standing decision ("after paper") was written before these three failures. Watching them fail in the meantime is evidence that reinforces the earlier call, not undermines it. The paper is what unblocks publishing and physicist conversations — the stated destination. Chasing an actively-resistant foundational gap ahead of shipping that is the wrong trade right now.

---

## What Option A Would Require (When Picked Back Up)

A mathematical object that:
1. Is a plausible formalization of "coherence" (not circular, not smuggled)
2. Can be evaluated on candidate propagation modes
3. Selects the correct mode (n=2, k=1) from alternatives
4. Is partition-invariant (unlike Family C MI)
5. Does not reduce to standard math with axiom labels (unlike C-063)

### Candidate approaches (ranked by promise, not by effort)

1. **New coherence functional (partition-invariant).** The Family C failure is specific to MI under binning. A topological invariant (winding number, linking number) or group-theoretic functional (representation-theoretic) might be partition-invariant by construction. Start from the requirement: must select n=2.

2. **Step A first (SO(3) invariance).** Close Step A: prove the internal cycle of a fundamental mode is SO(3)-invariant. Doesn't close the extra-β gap but removes one of two foundational uncertainties. Smallest, most bounded option.

3. **Lean-native H8 strengthening.** Add a selection principle as a named hypothesis in `Axioms.lean`, then test what it implies. The honest-parameter-count approach: see what minimal additional structure forces n=2. Methodologically clean but still the same open question in different clothes.

4. **Poincaré group route.** Formalize Axiom 3 in group-theoretic language for a Lorentz-covariant PF medium. Check whether "coherent in the medium frame" forces `γβ² = √C₂` from ISO(3,1) representations. Requires significant new mathematical machinery.

### What NOT to do

- Do NOT attempt another Casimir route. Another route would converge on the same gap. The routes have done their job: they've located the gap precisely.
- Do NOT promote the Casimir polynomial to DERIVED. It remains ARGUED 0.65.
- Do NOT relabel standard math as "Axiom 3" (the C-063 disease).
- Do NOT use partition-dependent functionals without testing bin offsets.

---

## Cross-Links

- **State-of-play (full):** `derivations/casimir_extra_beta_state_of_play_2026-07-28.md`
- **Family C failure:** `derivations/casimir_axiom3_mutual_information_correction_2026-07-29.md`
- **C-063 overclaim audit:** `audit/crypto_axiom3_qft_overclaim_audit_2026-07-30.md`
- **Coherence budget pre-registration:** `/mnt/d/Crypto/derivations/coherence_budget_pre_registration_2026-07-30.md`
- **O2bis correlation functional:** `derivations/o2bis_analytic_kickstart_2026-07-29.md`
- **α from axioms (Option A original):** `derivations/alpha_from_axioms.md` §10
- **Lean formalization:** `lean/PfLean/Axioms.lean` (H8 at line 115, periodic orbit theorem at line 1379, compact-orbit theorem at line 2402)
- **Physics synthesis map:** `PHYSICS_SYNTHESIS_MAP_2026-07-30.md`
- **Falsification paper:** `papers/FALSIFICATION_PAPER_DRAFT.md` (v0.5)

---

## Claim Tier Impact

**Nothing changes.** The Casimir polynomial remains ARGUED 0.65. Axiom 3 remains underdetermined. No PUBLIC HOLD, release, activation, legal, or Greg boundary moves. This document is internal preparation for a deferred research question, not a claim change.

---

*Written by Devin — 2026-07-31*
*Deferred to post-paper per standing decision, reinforced by three independent failures (Family C, C-063, coherence budget).*
*Carried forward, not dropped.*
