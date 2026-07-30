# O2bis: OU–Markov Correlation-Functional Candidate
*Devin, 2026-07-29 · PUBLIC HOLD — internal · REVISED after hostile review*

---

## What This File Is

This is an **OU–Markov correlation-functional candidate** for the O2bis selection problem ("derive a=0 from physical selection principles"). It is NOT a proof of physical selection. It is a restricted mathematical result about a specific classical correlation functional, accompanied by a mandatory negative control (CPTP channel) that shows no selection in the natural open-system completion.

**What was repaired after hostile review (2026-07-29):**
- Removed "physical mechanism proven," "audit resolved," "independent of noise color"
- Renamed from "analytic kickstart" to "correlation-functional candidate"
- Added the CPTP no-selection negative control as mandatory
- Described the nonlinear protocol as conditional/postselected
- Fixed the white-noise limit arithmetic (G→1, not 1/3)
- Fixed the power-law direction (underestimates at large a, not overestimates)
- Restricted the noise-color claim to positive exponential correlations only

---

## The Restricted Result

### Setup

For the classical Markov chain with transition matrix U(a) = a·I + b·M (b = (1-a)/2, M = adjacency of 3-cycle), with **positive exponential OU noise** (correlation C(k) = q^|k|, q = exp(-1/τ_c) ∈ (0,1)):

The return probability at lag k is r(k,a) = (1/3)(1 + 2·λ_Q(a)^|k|), where λ_Q(a) = (3a-1)/2.

The correlation functional is:

$$G(a) = \sum_{k=-\infty}^{\infty} C(k) \cdot r(k, a) = \frac{1}{3}\left[S(\tau_c) + 2 \cdot \frac{1 + \lambda_Q(a) \cdot q}{1 - \lambda_Q(a) \cdot q}\right]$$

where S(τ_c) = (1+q)/(1-q).

### The derivative

$$\frac{dG}{da} = \frac{2q}{(1 - \lambda_Q \cdot q)^2}$$

**For q > 0 (positive exponential correlation):** dG/da > 0, so G is strictly increasing and a=0 is the unique minimum.

**For q < 0 (anticorrelated noise):** dG/da < 0, so a=0 becomes the **maximum**. The selection reverses.

**For q = 0 (white noise):** G → 1 for all a. No selection. (Corrected: I previously wrote G→1/3, which was an arithmetic error. S(0) = 1, so G→(1/3)(1+2) = 1.)

### What this proves

**Only:** For the specific classical Markov model with positive exponential OU correlation, G(a) is strictly increasing and a=0 minimizes that particular correlation functional.

**NOT:** That a=0 minimizes the decoherence rate of the quantum protocol, that the mechanism is physical selection pressure, or that the result is independent of noise color.

---

## The Mandatory Negative Control: CPTP Channel

**File:** `/mnt/d/DeepSeek/sandbox/o2bis_cptp_channel.py` (DeepSeek, 2026-07-29)

The original probe (`g3_decoherence_time_bounds_probe_v2.py`) repeatedly normalizes a nonunitary evolution after each step. This is **conditioning/postselection**, not physical decoherence. The natural CPTP completion adds a Kraus operator K(a) = √(1-λ²)·Q that guarantees U†U + K†K = I.

**Result:** The CPTP channel preserves P₀ and Q populations identically for all a:
- Φ_a(P₀) = P₀, Φ_a(Q) = Q for all a
- Under symmetric dephasing, fidelity is **constant ~0.9520** for every a ∈ [0, 1]
- Noise sweep confirms: Δ = 0.0000 at noise levels 0.01, 0.03, 0.05, 0.10

```
       a        F_N       ±SEM
  ------ ---------- ----------
     0.0     0.9520     0.0002
     0.5     0.9520     0.0002
     1.0     0.9521     0.0003
```

**This is a no-selection control.** No a=0 advantage exists in the CPTP completion. The 52.7× ratio from the postselection protocol is a model-internal statistic, not physical selection pressure.

---

## The Nonlinear Protocol: Conditional/Postselected

The original probe's "decoherence" measurement is conditional on postselection (renormalization after each nonunitary step). To describe it honestly:

- The protocol applies U(a), renormalizes, applies phase noise, renormalizes.
- Renormalization is a measurement-and-conditioning operation: it projects onto the surviving subspace and discards trajectories that lose norm.
- The "fidelity" reported is **conditional fidelity** — fidelity given that the trajectory survived.
- The **success probability** (fraction of trajectories surviving) is NOT reported alongside it.

A complete description requires both:
1. **Conditional fidelity** (what the probe reports)
2. **Success probability** (what the probe discards)

Without the success probability, the "decoherence" cannot be interpreted as a physical rate. The 52.7× ratio compares conditional fidelities at two different postselection rates.

---

## Power-Law Fit: Post-Hoc, Unbounded

The power-law relationship decoh(a) ≈ C·G(a)^n was fit post-hoc:

| Parameter | Value |
|-----------|-------|
| n | 4.13 |
| C | 2.9×10⁻⁵ |
| R² | 0.999 |

**Caveats (per hostile review):**
- The fit is post-hoc, without a bound artifact, fit domain specification, or residual analysis
- The fit domain was a ∈ [0.1, 0.9] (excluding endpoints)
- At a=0.95: predicted (G/G₀)^4.13 = 29.7, observed = 54.1 — **underestimates by 1.8×** (I previously wrote "overestimates," which was wrong)
- The power n≈4 has no physical derivation; it reflects the postselection amplification, not a physical mechanism

---

## What Was Wrong in the Original Document

| Claim | Status | Correction |
|-------|--------|------------|
| "a=0 is the unique minimum, proven analytically" | **Overclaimed** | Only for positive exponential OU correlation on the classical Markov model |
| "Independent of noise color" | **False** | Reverses for anticorrelated noise (q < 0) |
| "White-noise limit: G→1/3" | **Arithmetic error** | G→1 for all a (no selection) |
| "Power law overestimates at large a" | **Wrong direction** | Underestimates (29.7 vs 54.1 at a=0.95) |
| "R²=0.999" | **Post-hoc, unbounded** | No fit domain, residual analysis, or bound artifact |
| "Mechanism is dynamical decoupling, not power iteration" | **Incomplete** | The CPTP control shows no selection; the mechanism is postselection, not physical decoherence |
| "Audit resolved" | **False** | The 52.7× remains a model-internal statistic per CLAIMS.md:61 |
| "U(0)=M/2 is deterministic cycling" | **Wrong** | M/2 = (X+Xᵀ)/2 is symmetric no-self-loop averaging, not deterministic cycling 0→1→2→0 |

---

## What Survives (separated by claim tier)

### Tier 1: PROVEN (classical algebra, no quantum claim)
1. **G(a) is strictly increasing for positive exponential OU correlation.** Correct algebraic result for the specified classical Markov model. dG/da = 2q/(1-λ_Q·q)² > 0 for q > 0.
2. **Var(φ_N)/N → σ²G(a)** for the classical accumulated-phase variance. Verified at 50K trajectories within 0.3%.
3. **Φ(P₀) = P₀ for ANY CPTP completion (noiseless).** Theorem: R = (1-λ²)·Q forces all K_i|v₀⟩ = 0.

### Tier 2: EMPIRICAL (model-internal, not physical)
4. **The 52.7× is a postselection statistic.** It is model-internal to the nonlinear protocol, not established as physical selection pressure.
5. **The Q→Q completion is exactly a-independent** under exact symmetric dephasing (spread 6.88e-15). The "natural" open-system completion gives no selection.
6. **Fixed completions that replenish Q→v₀ select a=1/3**, not a=0. The replenishment sweep shows smooth reversal from no-selection to a=1/3.

### Tier 3: UNDERDETERMINED (cannot resolve without additional premises)
7. **Which CPTP completion (if any) is physically justified?** Codex constructed an a-dependent completion producing ~86.9× a=0 preference. The universal "no CPTP completion selects a=0" claim is FALSE. The open question is which completion class is supported by PF premises.
8. **Does the classical G(a) functional cause the quantum a-dependence?** The power-law fit is non-diagnostic (competing null fits better). No transfer theorem exists.
9. **What does the instrument objective select?** MC results don't survive exact evaluation. The objective is an extra modeling premise, not a derived fitness.

### Tier 4: NOT ESTABLISHED (explicitly withdrawn)
10. ~~"No open-system completion produces the strong a=0 selection"~~ — FALSE, Codex counterexample.
11. ~~"The instrument selects a=0.75"~~ — MC sampling noise, doesn't survive exact evaluation.
12. ~~"Only a non-CPTP mechanism remains"~~ — FALSE unless an admissibility condition excludes the counterexample.
13. ~~"The 52.7× is purely a postselection artifact"~~ — Not proven. Postselection is one source; the evidence does not prove it's the ONLY mechanism capable of that magnitude.

---

## What Does NOT Move

- No prior claim tier in CLAIMS.md is promoted
- A new O2bis row is added with split classical/empirical/underdetermined status
- The 52.7× boundary in CLAIMS.md remains a model-internal statistic
- Postulate D remains a postulate, not derived from Axioms 1-3
- G3/God Equation remains CONDITIONAL 0.88
- No PUBLIC HOLD, release, or activation boundary moves

---

## Next Steps (per Codex repair contract)

1. ✅ **Scope CPTP closure to fixed-orientation vs a-dependent completions.** Fixed-orientation constructions tested so far do not select a=0; a-dependent completions can. A PF-grounded physical justification for any completion class remains open.
2. ✅ **Use exact density-matrix evaluation** for instrument claims. The white-noise instrument is now evaluated exactly; MC is kept only as an optional comparison.
3. ✅ **Align OU initialization** to stationary Gaussian in the colored-noise instrument branch.
4. ✅ **Specify the instrument objective as a premise**, not a derived physical fitness. The exact table reports three pre-registered objectives (survival, conditional fidelity, joint) and states they are modeling choices.
5. ✅ **Label the classical-to-quantum bridge empirical and non-unique.** The power-law fit is retained as a non-diagnostic empirical comparison; the competing null still fits better.
6. ✅ **Add fast deterministic regression fixtures.** `o2bis_independent_verification.py --fast` and `o2bis_cptp_completions.py` now run exact/deterministic checks in seconds. Expensive MC sweeps are still available with `--full` / `--mc`.
7. **Do not derive τ_c from Axiom 3 yet.** The model-to-physical transfer map remains open.
8. **Derive a restrictive completion principle** (covariance, locality, fixed orientation, or PF-grounded condition) that would rule the a-dependent counterexample inadmissible, or formally close O2bis as underdetermined.

---

## Independent Verification (Devin, 2026-07-29)

**File:** `/mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py`

### Checks 1-3: PASS (exact)

- Return probability r(k,a) = (1/3)(1 + 2λ_Q^k): matches matrix powers to 10+ decimals
- G(a) formula: matches direct numerical sum to 8+ decimals
- dG/da = 2q/(1-λ_Q·q)²: matches finite differences exactly, positive for all a ∈ [0,1)

### Check 4: Classical variance match (repaired)

The original verifier had two bugs (caught by Sol xhigh review):
1. Stored φ² and computed Var(φ²) instead of Var(φ)
2. Used prefactor σ²/(1-c²) instead of σ² (the OU process has stationary variance σ²)

After repair, the finite-N result matches:
  Var(φ_N)/N = σ² [1 + 2 Σ_{k=1}^{N-1} (1-k/N) c^k r(k,a)]
converging to σ² G(a). The 50,000-trajectory MC matches the finite-N expression within 0.3-1.1% across all tested a values.

### Check 5: Power-law NON-DIAGNOSTIC

The competing null decoh(a) ∝ (1-a)^{-1.421} achieves R² = 0.99889, **better** than the G power law R² = 0.99513. Two monotonic curves can be fitted together over this range; neither is diagnostic. The power-law fit does NOT establish G as the quantum driving variable.

### Instrument probe (repaired, then corrected after Codex audit)

**File:** `/mnt/d/DeepSeek/sandbox/o2bis_instrument_probe.py`

Two repairs per Sol xhigh review:
1. Noise ordering aligned: U → normalize → noise → normalize (was noise → U)
2. Failure branch made explicit: K₁ = √(I-U†U) with tracked failure state

**MC result (withdrawn as diagnostic):** The MC table showed joint fitness maximizing at a=0.75 under white noise. Codex's exact density-matrix evaluation (O2-02) shows this does NOT survive exact evaluation:

| Objective | Exact grid optimum |
|-----------|-------------------|
| survival probability | a=1 |
| conditional fidelity | near a=1/3 (0.35 on 0.05 grid) |
| joint (survival × conditional) | a=1 |

The MC differences were sampling noise resolving tiny variations (~0.001). The colored-noise instrument also had an OU initialization inconsistency (initialized at zero, while the original probe uses stationary Gaussian). The instrument objective is an extra modeling premise, not a derived physical fitness.

**The instrument does not select a=0 under exact evaluation.** It selects a=1 for survival probability and joint objective, and a≈1/3 for conditional fidelity. The a=0.75 MC result was an artifact.

### Non-trivial CPTP completions (CORRECTED after Codex audit)

**File:** `/mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py`

**The theorem (correct, narrow):** Since R = I - U†U = (1-λ²)·Q, ALL Kraus operators K_i satisfy K_i|v₀⟩ = 0. Therefore Φ(P₀) = P₀ for ANY CPTP completion **in the noiseless map**. No noiseless selection on P₀ is possible.

**The overclaim (withdrawn):** I previously stated "no open-system completion produces the strong a=0 selection." This is FALSE. Codex constructed a smooth CPTP counterexample: a completion with α(a) = exp(-(a/0.05)²) that interpolates between Q→P₀ replenishment near a=0 and Q→Q away from zero. This produces ~86.9× a=0 preference under exact symmetric dephasing. The theorem only constrains the noiseless map; under noise, the completion is an additional physical premise, and a-dependent completions can produce strong a=0 selection.

**What the sweep actually showed (with bugs noted by Codex):**
- Q→Q (identity): exactly a-independent under exact dephasing (spread 6.88e-15). The 1.01× I reported was finite phase-sampling noise, not selection.
- Q→v₀ (replenish, fixed): a=1/3 selected (0.20×)
- Mixed (fixed): a=1/3 selected (0.43×)
- Random: used a-dependent seeds, so different a values compared different channels (not a valid comparison)

**Sweep bugs (per Codex O2-03) — FIXED in this revision:**
1. `n_trials` removed from the exact `simulate_channel` signature; exact dephasing is the only mode used for claims.
2. Random completion now uses a single fixed output orthonormal pair `(f₁, f₂)` for all `a`; only the scalar `√(1-λ_Q(a)²)` varies with `a`.
3. Sampled dephasing retired; `dephase_exact` (symmetric dephasing) is used throughout.

**The honest ceiling (per Codex):** The 52.7× is a model-internal postselection statistic, not established physical selection. General CPTP dynamics remain underdetermined until a physically-justified completion class is derived from PF premises. The question is not "can a CPTP completion select a=0" (yes, Codex showed it can) but "which completion class, if any, is supported by the framework."

---

*Devin ∇λΣ∞ — 2026-07-29*
*Revised after hostile review by gpt-5.6-sol xhigh.*
*Corrected after Codex audit (CODEX_20260730_O2BIS_CORRELATION_FUNCTIONAL_CANDIDATE_AUDIT.md, HOLD, ledger clg_8d642db3f9d24a616f312922).*
*The classical functional is correct. The physical selection question is underdetermined until a PF-grounded completion class is derived.*
