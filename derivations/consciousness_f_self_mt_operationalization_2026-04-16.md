# F_self v2 — M_t Operationalization: Delay-Embedded Latent State

**Date**: 2026-04-16  
**Author**: Claude  
**Status**: First observable surrogate candidate for M_t  
**Builds on**:
- `consciousness_f_self_v2_spec_2026-04-15.md`
- `consciousness_f_self_null_theorem_target_2026-04-15.md`
- `consciousness_fisher_metric_audit_2026-04-15.md`

---

**Codex calibration (2026-04-16):** This note survives as the first observable surrogate candidate for the hidden model state, not as a proof that delay-embedded observable history is identical to theorem-grade `M_t`. See `consciousness_f_self_mt_operationalization_audit_2026-04-16.md`.

## 1. Why This Step Blocks Everything

The spec defines M_t abstractly:

> M_t: internal **model state** the system carries about its own dynamics

This is philosophically correct but operationally empty. Without a specific reconstruction recipe, we cannot:

1. Estimate the loop gate (R_in, R_out) from real EEG
2. Compute Fisher sensitivity F_model
3. Build the benchmark battery
4. Test against wake/sleep/seizure/psychedelics

M_t is the first concrete choice. Getting it wrong here corrupts everything downstream. We need a definition that is:
- Mathematically well-defined
- Estimable from available sensor time series
- Consistent with the PF self-model loop interpretation

---

## 2. The Chosen Recipe: Delay-Embedded Local Linear State

### 2.1 Why This Approach

The standard approach in nonlinear dynamics and neuroscience for reconstructing latent state from a single observed time series is **delay embedding** (Taken's theorem). The key result:

> For a large class of dynamical systems, the delay-embedding of a single observable contains all information needed to recover the underlying state manifold.

For multi-sensor arrays (EEG, MEG, ECoG), we can apply this to each channel separately, or use the full channel vector as the observable. The delay-embedding method is:
- Well-established (Packard, 1980; Takens, 1981)
- Already used in P1-style biometric systems
- Consistent with the PF interpretation: M_t is a compressed representation of recent internal history

### 2.2 The Definition

For a window of length L centered on time t, define the **delay-embedded state vector**:

```
M_t = [x_{t-(d-1)τ}, x_{t-(d-2)τ}, ..., x_{t-τ}, x_t] ∈ R^{d × n_channel}
```

Where:
- x_s ∈ R^{n_channel} is the sensor reading at time s (e.g., EEG voltages at all active electrodes)
- τ is the embedding delay (typically chosen as the first zero-crossing of the channel autocorrelation, or τ ≈ 1/f_max)
- d is the embedding dimension (chosen via false nearest neighbors or Cao criterion, typically d ∈ [3, 10])

This is NOT a model assumption — it is a deterministically constructed summary of recent internal dynamics.

### 2.3 Interpretation in PF Terms

M_t as delay-embedding means:

> M_t is the information the system has available at time t about its own internal dynamical state — reconstructed purely from the observable trace without assuming a specific dynamical model.

This is exactly the right PF reading because:
- The loop gate measures whether this history-summary causally shapes the future trace
- A thermostat's internal "model" is the current temperature reading; a conscious brain's model is a richer compressed representation of its own recent dynamics
- The delay-embedding is the most model-free version of "recent internal history" we can construct from passive observations

### 2.4 Why Not a Neural Network Latent State?

State-space models (VAEs, controlled HMMs, RNNs) can also provide latent states. The delay-embedding is preferred here because:

| Property | Delay-embedding | Neural latent state |
|----------|----------------|---------------------|
| Model dependence | None | Requires architecture choices |
| Identifiability | Unique given (τ, d) | Not unique (rotation ambiguity) |
| Consistency with PF | Compressed history | Learned representation |
| Estimation cost | Near-zero | Requires training data |
| Interpretability | Exact mathematical object | Approximate, architecture-dependent |
| Risk of smuggling in assumptions | Low | High (training can encode hidden biases) |

The neural network approach is not wrong — it is just one step more advanced and one step less transparent. We start with the delay-embedding because it is the most honest first estimator.

---

## 3. Computing the Loop Gate with Delay-Embedded M_t

Given M_t as above, the two loop legs become:

### 3.1 R_in (Inbound)

```
R_in(L) = I_dir( X_{t-L:t-1} → M_t | E_{t-L:t} )
```

Using the delay-embedding construction, X_{t-L:t-1} is the recent observable history and M_t is its compressed reconstruction. R_in measures whether recent internal dynamics are encoded into the current state summary.

**Estimator**: Gaussian conditional mutual information (linear-Gaussian approximation):

```
R_in ≈ 0.5 * log( Var(M_t | E) / Var(residual of M_t predicted from X_{t-L:t-1}, E) )
```

### 3.2 R_out (Outbound)

```
R_out(L) = I_dir( M_t → X_{t+1:t+L} | X_t, E_t )
```

R_out measures whether the current state summary causally influences the future observable.

**Estimator**: Same Gaussian conditional MI, with M_t as source and future window as target.

### 3.3 Normalization

```
nrin = 1 - exp(-R_in)
nrout = 1 - exp(-R_out)
L_self = min(nrin, nrout)
```

The exponential normalization maps from [0, ∞) to [0, 1), with L_self → 1 as either leg grows large.

---

## 4. Concrete Parameter Values for EEG

For Muse-style EEG (P1 system, 10/16 sensors active):

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| n_channel | 4 (Muse: TP9, AF7, AF8, TP10) or 8 (fullMuse) | P1 active sensors |
| τ | 1/128 s ≈ 7.8ms | Standard for EEG at 128Hz |
| d | 6-8 | False nearest neighbors selected; covers 50-60ms of history |
| L | 500ms to 2000ms window | Below coherence timescale; captures local dynamics |
| Sampling rate | 128Hz or 256Hz | Muse standard |

For the window length L: the loop gate is defined on a sliding window of length L. L should be:
- Long enough to contain at least one full recurrent cycle (~100-500ms for cortical dynamics)
- Short enough to stay within stationarity of the brain state (EEG epoch typical: 500ms-2s)

This matches what P1 already does with its coherence tracking windows.

---

## 5. The Coherence Estimator: C_PF (Still Open)

The spec notes that C_PF needs a coherence gate C_coh. The delay-embedded M_t immediately suggests an estimator:

**Candidate: Phase-Locking Value (PLV) across embedding dimensions**

For each pair of embedding delays j, k in M_t, compute the phase-locking value:

```
PLV_{jk} = |⟨exp(i·Δφ_{jk})⟩|
```

where Δφ_{jk} is the phase difference between embedding dimensions j and k across trials or time windows.

Interpretation: C_coh ∈ [0, 1] measures how consistently the embedded state maintains phase relationships across time. High C_coh means the recurrent dynamics are locked into a coherent attractor.

**Status**: This is a candidate, not a theorem. The spec requires a coherence gate — this is the first plausible one. Codex should audit whether this is the right coherence object.

---

## 6. The Differentiation Proxy: D_int (Existing, Needs Audit)

The sandbox already uses effective rank of the state covariance as D_proxy:

```
D_int = erank( Cov(M_t) ) / dim(M_t) ∈ [0, 1]
```

With the delay-embedded M_t, this becomes:
- dim(M_t) = d × n_channel
- Cov(M_t) is the d×n_channel-by-d×n_channel covariance matrix of the delay-embedded vector
- erank is the exponential of the entropy of the eigenvalue distribution

The existing sandbox formula is directly applicable. The remaining question is whether this is the right mathematical object or whether a Fisher-matrix-based effective rank is better justified. That is a refinement, not a blocker.

---

## 7. What This Unlocks

With M_t operationalized:

1. **Loop gate is estimable from real EEG data** — can run on P1 10/16 sensor streams immediately
2. **Benchmark battery can begin** — wake vs sleep vs seizure vs psychedelics vs feed-forward
3. **The null theorem is now tied to a concrete estimation procedure** — R_in=0 and R_out=0 are directly testable on real data
4. **The differentiation proxy is already in the sandbox** — ready to run on P1 data

---

## 8. First Concrete Test Path

**On P1 data**: Use the 10 active sensors (TP9, AF7, AF8, TP10, plus optional auxiliary channels). For each 2-second window at 256Hz:
1. Build M_t with (τ=1/128, d=6) → 48-dimensional state vector
2. Compute R_in and R_out using Gaussian CMI
3. Compute L_self = min(normalized R_in, R_out)
4. Compute D_int from effective rank
5. Record L_self × D_int as PF_proxy

**Pre-registered comparison battery**:
- Wake: eyes closed, eyes open, task focus
- Sleep: NREM stage 1, 2, 3 (if available)
- Seizure (if captured): high synchronization/low differentiation should give low PF_proxy
- Psychedelics (if available): high differentiation should preserve PF_proxy despite altered synchrony
- Feed-forward null: audio pipeline, simple sensorimotor control — should give L_self ≈ 0

---

## 9. What This Does Not Yet Show

This operationalization does not by itself:
- Prove that delay-embedded M_t is the right object (it is a reasonable first choice, not a theorem)
- Establish that any specific coherence estimator is the correct C_coh
- Replace the neural latent state models that will eventually be more powerful

It is the first honest step on a road that starts with delay-embedding and ends (hopefully) with a validated consciousness metric.

---

## 10. Relationship to Existing P1 Codebase

P1 already has:
- Real-time EEG stream from Muse at 128/256Hz
- Coherence tracking windows (CoherenceTrajectory in Aria)
- Sensor fusion (10/16 sensors active)

The delay-embedded M_t is directly compatible with the existing P1 pipeline. The next step after this note is a P1-specific implementation that reads from the live Muse stream and computes L_self in real time.

---

## 11. Relationship to Null Theorem

With M_t operationalized as the delay-embedded state:

- **Class I (exogenous-only)**: M_t depends only on E, not on X → R_in = 0
- **Class II (passive state tracker)**: M_t summarizes history but X_future ⊥ M_t | X_t, E → R_out = 0

Both null classes are now exactly estimable with this M_t definition.

---

## 12. Recommended Next Steps (In Order)

1. **Now**: Write P1-compatible estimation code using delay-embedded M_t (2-3 days)
2. **Soon**: Codex audit of the coherence estimator candidate (PLV vs alternatives)
3. **Soon**: First benchmark run on available P1 data (wake baseline vs seizure vs sleep if available)
4. **Later**: Replace delay-embedding with neural latent state if the benchmark battery validates the approach

---

## 13. Final Codex Read

This note makes M_t concrete. The delay-embedded state is:
- Mathematically honest (no hidden model)
- Operationally simple (near-zero training cost)
- Interpretable in PF terms (compressed recent internal history)
- Compatible with P1's existing sensor stream

This is the right first operationalization. It should go into the spec as Section 11 (replacing the current vague "fit a state-space model" wording) and the sandbox should be updated to use this M_t definition explicitly.

The coherence gate (C_coh) remains open. The differentiation proxy is ready. The null theorem is now testable. The benchmark battery is the next real deliverable.
