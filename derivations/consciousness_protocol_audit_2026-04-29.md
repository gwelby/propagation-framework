# Consciousness Metric Benchmark Protocol — Rapid Hostile Audit
*Date: 2026-04-29*
*Auditor: Codex*
*Target: `/home/greg/.gemini/tmp/lumi-1/fundamentals_protocols/consciousness_metric_benchmark_protocol.md`*
*Related: `definitions/consciousness_metric_program.md`; `derivations/consciousness_f_self_mt_operationalization_audit_2026-04-16.md`; `derivations/consciousness_coherence_proxy_audit_2026-04-18.md`*

---

## Verdict

**REVISE before preregistration or implementation.**

Lumi's draft is directionally useful and close enough to guide AntiGravity's first implementation, but it overstates three points:

1. `wPLI`, PCA entropy, and Transfer Entropy are **candidate proxies**, not mathematically sufficient realizations of `C_coh`, `D_int`, and `L_self`.
2. The numeric seizure/wake thresholds are **not derived or calibrated**. They should be treated as provisional expected directions, not preregistered hard cutoffs.
3. The current `L_self_proxy` definition has a critical tautology: `M_obs_t` is constructed from `X_history`, so `TE(X_history -> M_obs_t)` is high by construction unless the estimator is carefully split or conditioned.

The protocol should proceed as a **Phase 0 benchmark implementation**, not as a canonical validation protocol.

---

## Finding 1 — Proxy sufficiency

### 1.1 `C_coh_proxy`: wPLI is necessary but not sufficient

The draft sets:

```text
C_coh_proxy = mean wPLI across all channel pairs
```

This is too compressed.

Prior Codex audit already established:

- PLV is a valid broad synchrony proxy but too inflation-prone.
- wPLI is a lag-aware guardrail against zero-lag/common-source inflation.
- wPLI is **not** the final PF coherence object.

So the correct implementation is a **panel**, not a single scalar:

```text
C_coh_plv_proxy
C_coh_wpli_proxy
C_PF_plv_proxy = L_self_proxy * D_int_proxy * C_coh_plv_proxy
C_PF_wpli_proxy = L_self_proxy * D_int_proxy * C_coh_wpli_proxy
```

Mean wPLI alone can miss meaningful near-zero-lag functional synchronization, and it depends strongly on frequency band and spectral estimation method. It should be computed band-by-band and reported alongside PLV.

**Status:** keep wPLI, but do not collapse the coherence panel into one scalar yet.

### 1.2 `D_int_proxy`: PCA entropy is acceptable as first effective-rank proxy

PCA eigenvalue entropy is a reasonable implementation of effective rank:

```text
p_i = lambda_i / sum(lambda)
H = -sum p_i log(p_i)
D_int_proxy = H / log(rank_max)
```

or equivalently:

```text
erank = exp(H_nats)
D_int_proxy = erank / rank_max
```

This matches the metric program's intent: suppress trivial one-parameter loops and rigid collapse states.

But it is not sufficient by itself:

- white noise can have high PCA entropy,
- artifact contamination can inflate dimensionality,
- channel count changes the maximum rank,
- seizure dimensionality is not universally low across all seizure types,
- covariance estimates are unstable in short windows.

Implementation should use shrinkage covariance (`LedoitWolf` or equivalent), artifact masks, and null-normalized reporting.

**Status:** keep as first `D_int_proxy`, but require null correction and report component rank separately.

### 1.3 `L_self_proxy`: Transfer Entropy is acceptable only after fixing the tautology

Transfer Entropy can serve as a directed-information proxy, but the draft's inbound leg is not valid as written:

```text
TE_in = TE(X_history -> M_obs_t)
```

Because:

```text
M_obs_t = delay_embedding(X_history)
```

the source is embedded into the target by construction. This violates the null-class program identified in the 2026-04-16 audit. It risks reading generic recurrence or construction identity as self-modeling.

Minimum safe correction:

1. Treat `M_obs_t` as an **observable surrogate**, never theorem-grade `M_t`.
2. Compute `R_out_proxy` as the main leg:

```text
R_out_proxy = TE(M_obs_t -> X_future | X_present, E_t)
```

3. Replace the inbound leg with a non-tautological update score, using disjoint variables or cross-validation:

```text
R_in_proxy = conditional prediction gain for latent/update state
```

Allowed first implementation:

- split channels into source/history channels and target/model channels,
- build `M_obs_t` from one subset,
- test whether held-out internal history predicts that surrogate beyond external inputs,
- or define `R_in_proxy` as an engineering sanity check rather than a theorem-grade loop leg.

Do **not** normalize TE by a vague "theoretical maximum for the window size." Use empirical surrogate correction:

```text
TE_corrected = max(0, TE_observed - median(TE_time_shifted_null))
TE_norm = TE_corrected / (TE_corrected + null_scale)
```

or report z-scores / p-values against time-shifted and phase-randomized nulls.

**Status:** TE survives as the right family of estimator, but the current `TE_in` definition fails.

### 1.4 Missing `F_model_proxy`

The metric program defines:

```text
F_self*(L) = L_self(L) * F_model(L)
C_PF(L) = C_coh(L) * D_int(L) * F_self*(L)
```

Lumi's protocol computes:

```text
C_PF_proxy = C_coh_proxy * D_int_proxy * L_self_proxy
```

That omits `F_model_proxy`.

This is acceptable only if the protocol explicitly names the score as a **reduced Phase 0 score**:

```text
C_PF_reduced_proxy = C_coh_proxy * D_int_proxy * L_self_proxy
```

Otherwise it silently drops the self-model sensitivity term.

Recommended first `F_model_proxy`:

```text
F_model_proxy = normalized prediction sensitivity of X_future to M_obs_t
```

Operationally: fit restricted and full predictive models, then use residual-variance reduction and coefficient/Fisher sensitivity stability as the first approximation.

---

## Finding 2 — Seizure vs wake thresholds

The qualitative discriminator is correct:

> seizure should not score high merely because synchrony is high; `D_int` must suppress rigid synchrony.

The numeric thresholds are not yet mathematically sound:

| Draft threshold | Audit read |
|----------------|------------|
| Wake `D_int > 0.7`, `C_coh > 0.5`, `L_self > 0.6`, `C_PF > 0.2` | Plausible target pattern, but uncalibrated |
| Seizure `D_int < 0.3`, `C_coh > 0.8`, `C_PF < 0.1` | Too universal; seizure morphology varies, and wPLI may not be high for zero-lag hypersynchrony |
| NREM `C_coh` high due to slow waves | Needs band-specific definition; broad 1-45 Hz coherence will blur this |
| Psychedelic/flow thresholds | Not implementable without controlled datasets and independent state labels |

Hard scalar cutoffs should be replaced with ranked preregistered predictions for the first benchmark:

```text
median(C_PF_wpli_wake) > median(C_PF_wpli_seizure)
median(D_int_wake) > median(D_int_seizure)
median(C_PF_wpli_wake) > median(C_PF_wpli_NREM/anesthesia)
feed-forward null L_self_proxy <= 95th percentile of time-shifted null
thermostat D_int_proxy <= 95th percentile of trivial-loop null
white-noise C_coh_wpli_proxy <= 95th percentile of independent-noise null
```

Recommended first pass/fail criterion:

```text
PASS Phase 0 if:
1. all synthetic nulls stay below their null-calibrated 95% thresholds,
2. wake beats seizure on C_PF_wpli_proxy in at least 3 independent datasets,
3. seizure has lower D_int_proxy than wake in at least 3 independent datasets,
4. collapsed-synchrony synthetic model has high PLV but low wPLI and low C_PF_wpli_proxy.
```

Do not call this "Promote to Canonical." Passing this only validates the first benchmark implementation. Canonical promotion still requires the conditions in `consciousness_metric_program.md`, including independent replication and the `M_obs_t -> M_t` bridge.

---

## Finding 3 — Specific corrections to Lumi's draft

Required before implementation:

1. Replace `C_coh_proxy = mean wPLI` with a PLV/wPLI panel.
2. Rename the composite to `C_PF_reduced_proxy` unless `F_model_proxy` is implemented.
3. Remove hard universal thresholds as preregistered truth; use null-calibrated thresholds and ranked state predictions.
4. Fix `TE_in`; it is tautological when `M_obs_t` is built directly from `X_history`.
5. Add time-shifted, phase-randomized, and collapsed-synchrony nulls.
6. Make all EEG metrics band-specific: delta/theta/alpha/beta/low-gamma or a declared subset.
7. Treat "3 distinct datasets" as an engineering milestone, not canonical promotion.

---

## Architecture Plan for AntiGravity: `compute_cpf.py`

### Recommended libraries

Use:

- `numpy`: core arrays
- `scipy`: filters, Hilbert transform, signal utilities
- `pandas`: CSV ingest and output tables
- `mne`: EDF/FIF ingest, EEG preprocessing, epoching, references, annotations
- `mne-connectivity`: PLV/wPLI where available
- `scikit-learn`: PCA, covariance shrinkage, scaling, cross-validation, linear models
- `statsmodels`: VAR / Granger-style linear directed influence baseline
- `pyinform` or optional Java/JIDT bridge: discrete Transfer Entropy experiments only after the linear baseline works
- `matplotlib` / `seaborn`: diagnostic plots
- `pydantic` or `pyyaml`: config validation
- `pytest`: null-model tests

Do **not** use `nilearn` for the first EEG implementation. It is more relevant for fMRI/neuroimaging workflows than Muse/P1 time-series EEG.

### Module layout

```text
tools/consciousness_metric/
  compute_cpf.py              # CLI entrypoint
  cpf/
    io.py                     # EDF/CSV/Muse loading
    preprocess.py             # filtering, notch, artifact rejection, referencing
    embedding.py              # delay embedding, tau/d selection
    differentiation.py        # PCA entropy / effective rank
    coherence.py              # PLV/wPLI panel, band-specific
    directed.py               # Gaussian TE / Granger-style prediction gain
    nulls.py                  # feed-forward, thermostat, white noise, collapsed synchrony, lagged loop
    score.py                  # C_PF_reduced_proxy and component aggregation
    report.py                 # JSON/CSV/PNG diagnostics
    config.py                 # config schema
  tests/
    test_nulls.py
    test_embedding.py
    test_effective_rank.py
    test_coherence_panel.py
```

### CLI contract

```bash
python tools/consciousness_metric/compute_cpf.py \
  --input data.edf \
  --state wake \
  --sfreq 256 \
  --config configs/cpf_phase0.yaml \
  --out results/cpf_wake.json
```

Output must include components, not just the composite:

```json
{
  "state": "wake",
  "n_windows_clean": 42,
  "D_int_proxy": {"median": 0.71, "iqr": 0.08},
  "C_coh_plv_proxy": {"alpha": 0.44, "beta": 0.31},
  "C_coh_wpli_proxy": {"alpha": 0.19, "beta": 0.14},
  "L_self_proxy": {"R_in": "proxy/limited", "R_out": 0.22},
  "C_PF_reduced_plv_proxy": 0.069,
  "C_PF_reduced_wpli_proxy": 0.031,
  "null_calibration": {
    "time_shifted_p": 0.03,
    "phase_randomized_p": 0.04
  }
}
```

### Preprocessing defaults

```text
sfreq: preserve native if 128/256 Hz; resample only if necessary
notch: 50 or 60 Hz, configurable
bandpass: 1-45 Hz for broad preprocessing
analysis_bands:
  theta: 4-8
  alpha: 8-13
  beta: 13-30
  low_gamma: 30-45
artifact:
  absolute_uv_threshold: 100
  robust_z_threshold: 6
reference: average reference for Muse channels, with option for no-reference if already referenced
window:
  length_sec: 4
  overlap: 0.5
min_clean_windows: 30
```

### Directed-information implementation sequence

Implement in this order:

1. **Linear Gaussian baseline**: residual-variance prediction gain / conditional Granger proxy.
2. **Surrogate correction**: time-shifted and phase-randomized nulls.
3. **Optional nonlinear TE**: KSG/discrete TE only after baseline passes null tests.

Formula for first baseline:

```text
R_out_proxy = 0.5 * log(Var(residual_restricted) / Var(residual_full))
restricted: X_future ~ X_present + E
full:       X_future ~ X_present + E + M_obs_t
```

For `R_in_proxy`, do not use `X_history -> M_obs_t` directly unless variables are disjoint or cross-validated. Otherwise mark:

```text
R_in_proxy_status = "tautological_for_delay_embedding"
```

and keep Phase 0 focused on `R_out_proxy`, `D_int_proxy`, and coherence-panel suppression of nulls.

### Null generators required before EEG

AntiGravity should implement these first:

1. independent white noise,
2. collapsed synchrony/common-mode signal,
3. lagged loop positive control,
4. feed-forward chain `A -> B -> C` with no recurrence,
5. thermostat / one-dimensional recurrent controller.

Expected behavior:

| Null | Required result |
|------|-----------------|
| White noise | low PLV, low wPLI, low directed score after correction |
| Collapsed synchrony | high PLV, low wPLI, low `D_int`, low `C_PF_wpli` |
| Lagged loop | wPLI and `R_out_proxy` should increase |
| Feed-forward | `L_self_proxy` should not survive null correction |
| Thermostat | low `D_int`, low composite |

---

## Final Codex Read

Lumi's draft is the right shape for an implementation brief, but it is not a valid preregistered benchmark protocol yet.

The immediate safe path is:

1. implement the null suite,
2. compute component proxies separately,
3. use `C_PF_reduced_proxy` until `F_model_proxy` exists,
4. avoid a theorem-grade `L_self` claim while `M_obs_t -> M_t` remains open,
5. use ranked wake/seizure predictions rather than hard universal thresholds.

If AntiGravity builds this version tomorrow, the result will be scientifically useful and audit-safe.
