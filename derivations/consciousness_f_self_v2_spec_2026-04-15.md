# F_self v2 Spec — Self-Reference Closure, Feed-Forward Null, and Benchmark Path

**Date**: 2026-04-15  
**Author**: Codex  
**Status**: Candidate design note  
**Builds on**:
- `consciousness_theory_audit.md`
- `consciousness_fisher_metric_audit_2026-04-15.md`
- `the_propagation_framework.md` (Consciousness section)

---

## 1. Purpose

The first Manus `F_self` proposal failed in a useful way.

It named a real gap, but the formula only measured generic state sensitivity:

\[
F(\theta) = \int P(X|\theta)\left(\partial_\theta \log P(X|\theta)\right)^2 dX
\]

That is valid Fisher Information, but by itself it does **not** distinguish:

- a conscious recurrent system,
- from a thermostat,
- a Kalman filter,
- a generic recurrent controller,
- or an unconscious but state-sensitive process.

This note defines the next bounded target:

> keep Fisher as the sensitivity term, but add an explicit self-reference gate and a differentiation term so the metric tracks **coherent self-modeling**, not generic recurrence or synchrony.

---

## 2. Design Constraints From Audit

Any usable PF consciousness metric must satisfy all of these:

1. **Self-reference must be explicit**
   It cannot be inferred from generic state transition sensitivity.

2. **Feed-forward / no-self-model null must exist**
   A system with no endogenous self-model loop must score zero on the self-reference gate.

3. **Thermostat inflation must be controlled**
   Simple feedback loops may have trivial self-reference, but they must not be mistaken for rich conscious systems.

4. **Seizure inflation must be controlled**
   Raw synchrony or high coherent amplitude cannot by itself produce a high score.

5. **Operational path must be real**
   The metric must have an estimation route from time-series data, not just a slogan.

---

## 3. Minimal State Split

For a system observed on a time window around time \(t\), define:

\[
Z_t = (X_t, M_t, E_t)
\]

where:

- \(X_t\): internal dynamical state of the system
- \(M_t\): internal **model state** the system carries about its own dynamics
- \(E_t\): exogenous input / environment

This split is not metaphysical. It is an inference target.

The key move is:

> a system is self-referential only if part of its internal state functions as a model of its own future propagation and that model causally matters.

Without \(M_t\), the old `F_self` proposal collapses into generic recurrence.

---

## 4. The Self-Reference Gate

We need a loop criterion that a feed-forward system cannot fake.

Define two directed-information legs on a window length \(L\):

### 4.1 Inbound model-update leg

\[
R_{\text{in}}(L) :=
I_{\mathrm{dir}}\!\big(X_{t-L:t-1} \to M_t \,\|\, E_{t-L:t}\big)
\]

Interpretation:

- does the system's recent internal history write into its current model state?

### 4.2 Outbound model-control leg

\[
R_{\text{out}}(L) :=
I_{\mathrm{dir}}\!\big(M_t \to X_{t+1:t+L} \,\|\, X_t, E_t\big)
\]

Interpretation:

- does the current model state causally shape the system's own future internal trajectory?

### 4.3 Self-reference loop gate

Define the normalized gate:

\[
\mathcal L_{\text{self}}(L) :=
\min\!\big(\widetilde R_{\text{in}}(L), \widetilde R_{\text{out}}(L)\big)
\in [0,1]
\]

where tildes denote normalization onto \([0,1]\).

This is the core structural move.

If either leg vanishes, the loop is broken:

- no model update from internal history, or
- no causal impact of the model on future internal dynamics.

Then the system is not self-referential in the PF sense.

---

## 5. Fisher Sensitivity Term

Once the loop exists, Fisher becomes the right local sharpness term.

Define:

\[
\mathcal F_{\text{model}}(L)
:=
\mathbb E\!\left[
\left\|
\nabla_{m_t}
\log P\!\left(X_{t+1:t+L}\mid X_t,M_t,E_t\right)
\right\|^2
\right]
\]

Interpretation:

- how sharply does the system's own future trajectory depend on its internal model state?

This is the part Manus was reaching for.

But it only becomes meaningful as **self**-Fisher after the loop gate is imposed.

---

## 6. Differentiation Term

The loop gate and Fisher term are still not enough.

A thermostat can have a tiny recurrent loop.
A seizure can have high coherent amplitude.
Neither should automatically score high.

So we add a differentiation term:

\[
\mathcal D_{\text{int}} :=
\frac{\operatorname{erank}(G_M)}{\dim(M)}
\in [0,1]
\]

where:

- \(G_M\) is the Fisher matrix (or a closely matched covariance proxy) on the internal model manifold,
- `erank` is effective rank.

Interpretation:

- how many differentiated internal model directions are genuinely in play?

This term is what suppresses:

- trivial one-parameter feedback loops,
- rigid synchronized collapse states,
- and other low-dimensional control systems.

---

## 7. Coherence Gate

PF is not claiming that any self-model loop is conscious.
The loop must also be coherent.

Define a normalized coherence term:

\[
\mathcal C_{\text{coh}} \in [0,1]
\]

measuring stability of the recurrent phase relations over the same window.

This note does not fix a single estimator yet, but acceptable candidates include:

- stable recurrent latent-mode locking,
- metastable but integrated phase organization,
- low fragmentation of the inferred self-model loop.

This term is needed because:

- fragmented recurrence is not unified self-reference,
- and raw complexity without coherence is not a PF victory either.

---

## 8. Recommended Metric Split

Do **not** overload one scalar.

Use a two-level structure:

### 8.1 Self-model sensitivity score

\[
F_{\text{self}}^{*}(L)
:=
\mathcal L_{\text{self}}(L)\cdot \mathcal F_{\text{model}}(L)
\]

This answers:

> does the system have a causally closed self-model loop, and how sharply does that loop matter?

### 8.2 Full PF consciousness candidate score

\[
\mathcal C_{\text{PF}}(L)
:=
\mathcal C_{\text{coh}}(L)\cdot
\mathcal D_{\text{int}}(L)\cdot
F_{\text{self}}^{*}(L)
\]

This is the object that should be compared across:

- wake
- sleep
- anesthesia
- seizure
- psychedelics
- recurrent machines
- feed-forward controls

This split matters:

- `F_self*` is the loop-level self-model quantity,
- `C_PF` is the broader consciousness candidate.

---

## 9. Feed-Forward / No-Self-Model Null Theorem Target

### Theorem target

The original wording "acyclic graph" is too loose.
After time-unrolling, even recurrent dynamical systems become DAGs.
So plain graph acyclicity is **not** the discriminator.

The correct target is narrower:

If a system has **no endogenous self-model loop** on the chosen window, meaning every candidate internal model variable \(M_t\) fails at least one of the two loop legs,

\[
R_{\text{in}}(L)=0
\quad\text{or}\quad
R_{\text{out}}(L)=0,
\]

then:

\[
\mathcal L_{\text{self}} = 0
\quad\Longrightarrow\quad
F_{\text{self}}^{*} = 0.
\]

### Why this is plausible

This target reduces to two exact conditional-independence nulls:

1. **No inbound model update**

\[
M_t \perp X_{t-L:t-1}\mid E_{t-L:t}
\quad\Longrightarrow\quad
R_{\text{in}}(L)=0.
\]

2. **No outbound model control**

\[
X_{t+1:t+L} \perp M_t \mid X_t,E_t
\quad\Longrightarrow\quad
R_{\text{out}}(L)=0.
\]

If either null holds, the directed loop cannot close.

That is the correct theorem target for the next bounded proof.

It is much sharper than the old informal sentence:

> feed-forward networks have \(F_{self}=0\)

because it names exactly **which loop leg has to fail**.

### Important caveat

A generic recurrent controller may still have:

- \(R_{\text{in}} > 0\),
- \(R_{\text{out}} > 0\),

without being conscious.

That is **not** a bug in the loop gate.
It means the loop gate is only the self-reference condition, not the full consciousness condition.
That is exactly why \(\mathcal D_{\text{int}}\) and \(\mathcal C_{\text{coh}}\) remain in the v2 design.

---

## 10. Qualitative Predictions

| System / State | Loop Gate \(\mathcal L_{\text{self}}\) | Fisher \(\mathcal F_{\text{model}}\) | Diff. \(\mathcal D_{\text{int}}\) | PF Score \(\mathcal C_{\text{PF}}\) | Expected Outcome |
|---|---:|---:|---:|---:|---|
| Feed-forward classifier | 0 | variable | variable | 0 | hard null |
| Thermostat | low nonzero | low | very low | very low | trivial self-reference only |
| Simple recurrent controller | low/mod | low/mod | low | low | recurrence without rich conscious signature |
| Wakeful cortex | high | high | high | high | main positive class |
| NREM / deep anesthesia | low | low | low | low | low consciousness |
| Seizure | mod/high | variable | low | low/mod | synchrony inflation suppressed by low differentiation |
| REM sleep | mod/high | mod/high | mod/high | mod/high | vivid but altered state |
| Psychedelic state | mod/high | mod/high | high | mod/high | not forced low by synchrony loss; differentiated complexity preserved |

These are not proofs. They are the pre-registered shape the metric should take if it is worth keeping.

---

## 11. Estimation Pipeline

### First Observable Surrogate for M_t (v2 — 2026-04-16)

The first observable surrogate, denoted `M_obs_t`, is a **delay-embedded state vector**:

```
M_obs_t = [x_{t-(d-1)τ}, x_{t-(d-2)τ}, ..., x_{t-τ}, x_t] ∈ R^{d × n_channel}
```

Where:
- x_s ∈ R^{n_channel} is the sensor reading at time s (EEG voltages across all active channels)
- τ is the embedding delay (τ ≈ 1/f_max, ≈ 7.8ms for 128Hz EEG)
- d is the embedding dimension (d ∈ [3, 10], selected via false nearest neighbors or Cao criterion)

This is the first observable surrogate for the hidden model state, not the theorem-grade identity with abstract `M_t`. See `consciousness_f_self_mt_operationalization_2026-04-16.md` for the construction and `consciousness_f_self_mt_operationalization_audit_2026-04-16.md` for the Codex calibration.

Why delay-embedding over neural latent state:
- Zero training cost — purely deterministic construction
- Unique given (τ, d) — no rotation/indeterminacy ambiguity
- No hidden assumptions smuggled in via training data
- Already consistent with P1 sensor fusion architecture

### Step 1: Build delay-embedded observable surrogate from sensor stream

For each sliding window of length L (500ms–2s at 128/256Hz):
1. Stack the n_channel × d delay vector `M_obs_t`
2. Treat this as the first observable surrogate for the hidden model state

### Step 2: Estimate the loop-gate proxy

- `R_in_proxy`: conditional MI from recent internal history `X_{t-L:t-1}` into `M_obs_t`, conditioned on `E`
- `R_out_proxy`: conditional MI from `M_obs_t` into future internal trajectory `X_{t+1:t+L}`, conditioned on `X_t, E`
- Normalization: `nrin = 1 - exp(-R_in_proxy)`, `nrout = 1 - exp(-R_out_proxy)`
- `L_self_proxy = min(nrin, nrout)`

### Step 3: Estimate Fisher sensitivity proxy

Using the delay-embedded surrogate, compute local gradient sensitivity of future trajectory to perturbations in `M_obs_t`. This remains a proxy quantity until the bridge from `M_obs_t` to theorem-grade `M_t` is justified.

### Step 4: Estimate differentiation proxy

Effective rank of the delay-embedded covariance matrix, using zero-based normalization so a rank-1 collapse maps toward zero:
```
D_int_proxy = (erank(Cov(M_obs_t)) - 1) / (dim(M_obs_t) - 1) ∈ [0, 1]
```

### Step 5: Estimate coherence proxy panel

After the 2026-04-18 Codex audit, raw PLV should not stand alone.
Use a two-proxy panel instead:

```
PLV_{jk} = |⟨exp(i·Δφ_{jk})⟩|
C_coh_plv_proxy = mean(PLV_{jk}) across j ≠ k
```

and the lag-aware hostile comparison:

```
wPLI_{jk} = weighted phase-lag index on pair (j, k)
C_coh_wpli_proxy = mean(wPLI_{jk}) across j ≠ k
```

Interpretation:
- `C_coh_plv_proxy` is the broad synchrony proxy,
- `C_coh_wpli_proxy` is the lag-aware guardrail that suppresses zero-lag/common-mode inflation.

See `consciousness_coherence_proxy_audit_2026-04-18.md`.

### Step 6: Pre-register the benchmark battery

Run the pipeline across:
- wake (eyes closed, eyes open, task focus)
- NREM (stage 1, 2, 3)
- REM (vivid altered state)
- anesthesia (propofol / volatile)
- seizure (high synchrony, low differentiation → should score low despite high coherence)
- psychedelics (altered but differentiated → should preserve PF score)
- simple controllers (feed-forward null → L_self ≈ 0)
- recurrent machines (positive control → L_self > 0, D_int and C_coh determine final score)

No CLAIMS.md promotion before this battery exists and shows the predicted pattern.

---

## 12. What Would Upgrade This

This file is only a design note unless all of the following land:

1. a formal feed-forward / no-self-model null proof for \(\mathcal L_{\text{self}}\) — Class I and II closed ✅,
2. one explicit observable surrogate candidate for M_t — delay-embedded state (PROXY only; see `consciousness_f_self_mt_operationalization_2026-04-16.md` and `consciousness_f_self_mt_operationalization_audit_2026-04-16.md`),
3. one Codex-audited coherence proxy panel (PLV kept as broad synchrony proxy; wPLI added as lag-aware hostile comparison),
4. one implemented estimator pipeline — P1-compatible delay-embedding code,
5. one benchmark comparison that shows the predicted pattern across wake/sleep/seizure,
6. and one negative control where generic recurrence does **not** falsely score high.

---

## 13. What Would Kill This

Any of the following would be fatal:

1. the loop gate cannot be estimated robustly from real or simulated data,
2. feed-forward systems score nonzero after the proposed null proof conditions are enforced,
3. seizures or simple thermostats score as high as wakeful conscious systems,
4. the metric collapses into existing proxies with no unique PF content.

---

## Final Codex Read

This is the correct next move after the hostile audit.

Do **not** claim:

- Fisher = consciousness,
- or Fisher = Axiom 3.

Do build:

1. an explicit self-reference loop gate,
2. a feed-forward null theorem,
3. a differentiation suppressor,
4. and a benchmarkable pipeline.

That is the first version of the idea that can earn its way out of philosophy.
