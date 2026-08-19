# C_PF Structural-Correlate Benchmark — Pre-registration and Incremental-Validity Protocol (Route E)

**Status:** PRE-REGISTRATION SKELETON / DESIGN-ONLY.  
**Authority tier:** advisory — instrument repair and boundary audit only.  
**Public hold:** PUBLIC HOLD on Fundamentals remains in effect. No promotion.  
**Scope:** a design document for a prospective structural-correlate benchmark. No real data are used, no claim of consciousness detection is made, and the protocol is not ready for execution until the missing estimator is frozen.  
**Procedural templates consulted:** Cogitate (Mudrik et al. 2025; OSF preregistration v4/v5); PLOS ONE adversarial-collaboration protocol (Mudrik et al. 2023); Perturbational Complexity Index / PCI (Massimini et al. 2013; Sarasso et al. 2024). These are used only as procedural templates for pre-registration, adversarial interpretation, and comparator design, not as evidence for the PF metric.

---

## 1. Pre-registration skeleton

### 1.1 Research question

In a multivariate, delay-embedded sensor time series, does the composite score `C_PF_reduced_wpli` — the product of effective manifold rank (`D_int`), lag-aware phase coherence (`C_coh_wpli`), and lagged self-prediction gain (`D_dir_proxy`) — show a pre-registered pattern across synthetic and physiological dynamical states, and does it add predictive information beyond simpler structural correlates (arousal, complexity, report, task, signal quality, PCI) on a held-out replication set?

This is a test of a **candidate structural-correlate instrument**, not a test of phenomenal consciousness. The labels "wakeful rest," "NREM," "REM," "sedation-like," "seizure-like," and "psychedelic-like" refer to experimental conditions and signal properties, not to the presence or absence of experience.

### 1.2 Datasets and inclusion/exclusion criteria

Because this is a design document, the target dataset is not yet bound. The following criteria must be written into the protocol *before* any `C_PF` value is computed on the target data.

**Intended source (to be locked):**
A multi-condition, non-clinical, multichannel EEG corpus with at least `N = 40` independent recordings per condition (session or participant), sampled at a fixed rate and with a stable channel layout. Conditions:

1. Eyes-closed wakeful rest (high-differentiation, high-self-prediction candidate).
2. NREM sleep stage 2 or 3 (low-differentiation, low-self-prediction candidate).
3. REM sleep (moderate-differentiation, moderate-coherence candidate).
4. Pharmacologically induced low-arousal state (e.g. propofol or zolpidem sedation in healthy volunteers; low-differentiation, low-coherence candidate).
5. Pharmacologically altered wakeful state (e.g. ketamine or psilocybin; high-differentiation, altered-coherence candidate) — *only if* approved for non-clinical volunteer research.
6. High-synchrony, low-differentiation synthetic/in-vitro seizure-like dynamics.
7. In-silico negative and positive controls (see §1.8).

**Inclusion criteria:**
- Recording has at least 4 EEG channels and a fixed sampling rate `fs ≥ 256 Hz`.
- Each included session yields at least 20 clean 2-s epochs after artifact rejection.
- Channel labels contain or can be mapped to `TP9/AF7/AF8/TP10` (Muse-style) or a documented 10-20 montage.
- Recording has a metadata field binding it to one of the pre-registered conditions.

**Exclusion criteria:**
- More than 50% of epochs are rejected by the pre-registered artifact rule.
- Known hardware dropout, flat line, or saturated amplifier in any channel.
- Missing or ambiguous condition label.
- Any recording used to select thresholds, tune parameters, or define post-hoc comparisons.

**Data binding lock:** the exact dataset DOI, download/access date, condition table, and channel mapping must be added to this document and committed before analysis. Until then the dataset field is incomplete.

### 1.3 Epoching and artifact-rejection rules

These rules are locked to the current `compute_cpf.py` defaults. Any deviation becomes a protocol amendment.

- **Bandpass filter:** zero-phase 4th-order Butterworth bandpass, `1.0–45.0 Hz`, applied with `scipy.signal.butter` + `filtfilt` along the sample axis.
- **Epoching:** non-overlapping 2.0-s windows. At `fs = 256 Hz` this is 512 samples per epoch.
- **Artifact rejection:** an epoch is rejected if the absolute amplitude in any channel exceeds `100 µV` at any sample. This is a fixed threshold and is not re-tuned on target data.
- **Minimum epoch count:** a session is excluded if fewer than 20 clean epochs remain after rejection.
- **No re-referencing, ICA, or additional denoising** is applied beyond the locked bandpass and artifact rejection.

### 1.4 Exact estimator and parameter choices

Two estimator tracks are described below because the documented self-model conditional-information (`CMI`) gate is not yet implemented. Track A is the only track that is currently executable. Track B is the intended target and can replace Track A only through a numbered pre-registration amendment after Route B closes.

#### 1.4.1 Track A — Phase 0 production pipeline (currently executable)

This is the exact pipeline in `tools/consciousness_metric/compute_cpf.py` and `tools/consciousness_metric/cpf/score.py`.

| Component | Exact choice |
|-----------|--------------|
| Input | 4-channel EEG, `n_channels × n_samples` array (Muse `RAW_TP9/AF7/AF8/TP10` or first 4 numeric non-timestamp columns) |
| Sampling rate | `fs = 256 Hz` (locked). If the source is not 256 Hz, resample before analysis and record the resampling method. |
| Delay embedding | `d = 3`, `τ = 2` samples (~7.8 ms). `M_obs_t` is the concatenation of channel samples at lags `0, τ, 2τ` (channel-major order). Edge samples shorter than `(d-1)τ` are discarded. |
| Differentiation | PCA on the embedded matrix. `D_int` is the normalized Shannon entropy of the explained-variance eigenvalues: `H = -∑ p_i log2 p_i / log2(min(n_samples, n_features))`, with `p_i = λ_i / ∑λ_i`. `D_int ∈ [0,1]`. Zero-variance inputs return 0. |
| Coherence | Analytic signal via `scipy.signal.hilbert` (axis=1). `C_coh_wpli` is the mean weighted phase-lag index over all unique channel pairs: `wPLI_ij = |mean(Im(z_i · conj(z_j)))| / mean(|Im(z_i · conj(z_j))|)`. PLV is computed for diagnostics only. |
| Directed proxy | One-lag linear Granger prediction gain. For each target channel `c`, regress `X_c[t]` on `X_c[t-1]` (self model) and on all `X[:, t-1]` (full model). `gain_c = max(0, (var_self - var_all) / var_self)` with `var_*` the residual variances. `D_dir_proxy = mean_c gain_c`. `LinearRegression` includes an intercept (default). |
| Composite | `C_PF_reduced_wpli = D_int × C_coh_wpli × D_dir_proxy` (product, **not** `1 + D_dir_proxy`). |

**Important caveat:** `D_dir_proxy` is a generic cross-lag prediction-gain proxy, *not* the documented `L_self = min(R_in, R_out)` self-model CMI gate. Track A therefore does **not** test the self-model loop; it tests a "differentiation × lag-aware coherence × lagged self-prediction" structural proxy. Track A is falsified if it yields high scores on an acyclic feed-forward chain or a synchronized no-loop system.

#### 1.4.2 Track B — target self-model CMI gate (must be frozen by Route B)

If Route B produces a validated estimator and Route C confirms it passes the hostile controls, the pre-registration will be amended to:

| Component | Exact choice (to be specified by the amendment) |
|-----------|--------------------------------------------------|
| Self-model variable | `M_obs_t` as above, or a formally justified surrogate `M_t`. |
| Inbound leg | `R_in = I(X_{t-L:t-1} → M_t | E_{t-L:t})` estimated by a single-joint-covariance Gaussian CMI or by a k-NN CMI with a fixed `k`. `E` is an environment proxy to be specified (e.g. time-shifted surrogate or a held-out channel set). |
| Outbound leg | `R_out = I(M_t → X_{t+1:t+L} | X_t, E_t)` estimated by the same CMI method. |
| Normalization | Each leg is normalized against `n = 1000` conditional-independent surrogate samples of the same dimensions and autocorrelation. The exact surrogate method (e.g. AAFT) and clipping rule are fixed. |
| Gate | `L_self = min(R_in_norm, R_out_norm)`, `L_self ∈ [0,1]`. |
| Composite | `C_PF = C_coh_wpli × D_int × L_self`. |

Until Track B is frozen, Track A is the only executable pre-registered pipeline, and the interpretation is restricted to the Phase 0 proxy.

### 1.5 Primary and secondary outcomes

**Primary outcome:**  
On the held-out set, the area under the ROC curve (`AUC`) for discriminating a *high-differentiation, high-self-prediction* condition (eyes-closed wakeful rest) from a *low-differentiation, low-self-prediction* condition (NREM sleep or pharmacologically induced low-arousal state) using `C_PF_reduced_wpli`. The primary test is one-sided against `AUC = 0.5`.

**Secondary outcomes:**
1. Median `C_PF_reduced_wpli` across all seven pre-registered conditions.
2. Separate contributions of `D_int`, `C_coh_wpli`, and `D_dir_proxy` across conditions.
3. Pass/fail of all synthetic null classes at the pre-registered thresholds.
4. Incremental validity over the six comparator baselines on held-out data.
5. Test-retest / split-half reliability of `C_PF_reduced_wpli` within a condition.
6. Confound checks: correlation of `C_PF_reduced_wpli` with signal-quality metrics and arousal proxies.

No outcome is reframed as evidence for or against consciousness.

### 1.6 A priori thresholds for null/positive classification

These thresholds are fixed **before** target data are inspected and are based on the existing null-class test suite, not on the target dataset.

| Class | Threshold rule |
|-------|----------------|
| White noise | Median `C_PF_reduced_wpli` across 1000 instantiations `C_null < 0.05`; no more than 5% of individual instances exceed `0.10`. |
| Collapsed synchrony | Median `C_PF_reduced_wpli` `C_null < 0.05`; `C_coh_plv` may be high, but `C_coh_wpli` and `D_int` must suppress the composite. |
| Thermostat / 1-D recurrent controller | Median `C_PF_reduced_wpli` `C_null < 0.05`; `D_int` must be below `0.25`. |
| Acyclic feed-forward chain | Median `C_PF_reduced_wpli` `C_null < 0.05`; failure labels `D_dir_proxy` as a generic cross-lag confound. |
| Synchronized no-loop / common-driver | Median `C_PF_reduced_wpli` `C_null < 0.05`; failure labels `C_coh_wpli` and/or the `(1 + proxy)` bug as uncontrolled. |
| Phase-randomized surrogate | `C_PF_reduced_wpli` for the surrogate must not exceed the empirical 95th percentile of an AAFT null distribution. |
| Positive closed self-model loop | Median `C_PF_reduced_wpli` must exceed `C_null` (i.e. the instrument must be sensitive to a true loop). |

**Condition-discrimination threshold:**
- Primary AUC: positive if the lower bound of a 95% bootstrap confidence interval is above `0.5` and the one-sided `p` from DeLong's test is `< 0.05`.
- Pairwise condition comparisons: one-sided Mann-Whitney U with `α = 0.0125` (Bonferroni across the 4 pre-registered contrasts) or FDR `q = 0.05` if the family is expanded.

**Incremental-validity threshold:**
Adding `C_PF_reduced_wpli` to the full baseline model must produce a significant likelihood-ratio test (`p < 0.05`) and a held-out `ΔAUC ≥ 0.03` against the same model without `C_PF`.

### 1.7 Statistical tests and correction for multiple comparisons

- **Distribution:** condition scores are expected to be non-normal, so non-parametric tests are pre-registered: Kruskal-Wallis across conditions, Mann-Whitney U for pairwise contrasts, Cliff's `d` for effect size.
- **Classification:** logistic regression with stratified 5-fold cross-validation on the development set; final evaluation on the held-out set. Classifier uses `C_PF_reduced_wpli` and, in nested models, the comparator baselines.
- **AUC:** DeLong's test for comparing `C_PF` AUC against chance and against comparator AUCs; 2000-stratified bootstrap for the 95% CI.
- **Incremental validity:** nested logistic regression (baseline set only vs. baseline set + `C_PF`); likelihood-ratio test; permutation test (`n = 1000` permutations) for feature importance.
- **Surrogate nulls:** for each empirical epoch, generate `1000` amplitude-adjusted Fourier-transform (AAFT) surrogates preserving the power spectrum and amplitude distribution. `p` is the proportion of surrogates with `C_PF` greater than or equal to the observed value. Use FDR `q = 0.05` across epochs.
- **Multiple comparison correction:** condition contrasts use FDR `q = 0.05`; the null-class battery uses a family-wise error rule — failure of **any** null class halts interpretation (so no `p`-value correction is needed; each null is a go/no-go gate).

### 1.8 Interpretation rules and error labels

| Result pattern | Interpretation / error label |
|----------------|------------------------------|
| Any synthetic null class exceeds its threshold | **INSTRUMENT-FAIL / PROXY-CONFOUND**. All condition claims are suspended. |
| Feed-forward chain scores `C_PF > 0.05` | **FEED-FORWARD-FALSE-POSITIVE**: `D_dir_proxy` measures generic temporal prediction, not a self-model loop. |
| Synchronized no-loop / common-driver scores `C_PF > 0.05` | **SYNC-OR-COMMON-DRIVER-FALSE-POSITIVE**: wPLI or `D_int` is failing to penalize common-mode / zero-lag structure. |
| Positive self-loop does not exceed null | **GATE-INSENSITIVE**: the estimator cannot detect a known closed loop. |
| Seizure-like synchrony scores in the wake range | **DIFFERENTIATION-GATE-FAILURE**: `D_int` is not suppressing high-coherence / low-rank dynamics. |
| `C_PF` correlates more strongly with signal-quality metrics than with condition | **QUALITY-CONFOUND**: the score is artifact-driven. |
| `C_PF` is not incremental over the baseline model | **REDUNDANT**: the composite adds no information beyond simpler correlates. |
| Conditions order as predicted on held-out data | **RANKING-HOLD**: the structural-correlate hypothesis is supported for the tested signals. Not a consciousness claim. |
| Conditions do not order as predicted | **HYPOTHESIS-FAIL / INSTRUMENT-INSUFFICIENT**: the proxy is wrong for the tested states or the construct is not captured. |
| `C_PF` classifies wake vs. NREM/SED above chance, but comparator AUC is comparable | **WEAK-INCREMENTAL-VALIDITY**: the score works, but not better than existing proxies. |

### 1.9 Held-out replication set

- **Development / held-out split:** at the moment of data binding, 70% of sessions are designated as the **development set** and 30% as the **held-out set**, stratified by condition and with a locked random seed. The split is recorded in the protocol and the held-out set is not used for any threshold selection, parameter tuning, feature selection, outlier-rule revision, or model fitting.
- **Internal cross-validation:** 5-fold stratified CV is allowed on the development set for estimating variance and training nested models. Final reported statistics are always from the held-out set.
- **External replication:** at least one independent dataset collected by a separate lab or with a different device is locked as **replication-2**. It is not inspected until the primary and secondary analyses are frozen.
- **Replication success criterion:** the primary effect (held-out AUC for wake vs. low-arousal) is significant in the same direction at `p < 0.05`, and the point estimate of the held-out AUC lies within the 95% CI of the development-set AUC. The null-class battery must also pass on the replication set.

---

## 2. Comparator / incremental-validity plan

### 2.1 Baselines to compare

All baselines are computed on the same 2-s clean epochs as `C_PF`.

1. **Arousal**
   - log-ratio `(alpha + beta) / (delta + theta)` bandpower.
   - Total log-bandpower (1–45 Hz).
   - Zero-crossing rate / Higuchi fractal dimension of the broadband signal.

2. **Complexity**
   - Normalized Lempel-Ziv complexity (binary median-split, LZ77) per channel, averaged.
   - Sample entropy: `m = 2`, `r = 0.2 × SD`.
   - Spectral entropy of the 1–45 Hz power spectrum.
   - Higuchi fractal dimension (standard `k_max = 10`).

3. **Report**
   - Objective behavioral report, when available (detection accuracy, `d′` from a simple visual/auditory detection task).
   - If no report is collected, the condition label is used as a group-level proxy and this limitation is reported.

4. **Task**
   - Task accuracy and reaction time, if a concurrent task was performed.

5. **Signal quality**
   - Percentage of rejected epochs per session.
   - Mean absolute amplitude and broadband variance.
   - Channel-by-channel covariance and dropout count.
   - 50/60 Hz residual after bandpass.

6. **PCI (Perturbational Complexity Index)**
   - If TMS-EEG is available, a pre-registered fast-PCI or PCI surrogate.
   - If TMS-EEG is unavailable, a published PCI-style Lempel-Ziv spatiotemporal complexity index is computed on the same source as a *proxy* comparator, not as the clinical PCI.

### 2.2 How `C_PF` will be compared

- **Pairwise AUC comparison:** each baseline and `C_PF` is used separately to classify the primary contrast. AUCs are compared with DeLong's test.
- **Nested model test:** a logistic model with the full baseline set is compared to a model that adds `C_PF`. The likelihood-ratio test and the change in held-out `AUC` (`ΔAUC`) are reported.
- **Partial correlation:** Spearman correlation between `C_PF` and condition, controlling for each baseline in turn. If the partial correlation vanishes, `C_PF` is redundant with that baseline.
- **Permutation importance:** in a random-forest / gradient-boosting classifier, the drop in held-out AUC when `C_PF` is permuted is compared to the drop when each baseline is permuted.
- **Confound-specific tests:** if `C_PF` is significant only when low-quality epochs are included, or only when an arousal proxy is not controlled for, the result is flagged as **AROUSAL-CONFOUNDED** or **QUALITY-CONFOUNDED**.

### 2.3 Incremental-validity decision rule

`C_PF` has incremental validity on the held-out set only if **all** of the following hold:

1. The baseline-only model is better than chance (AUC `> 0.5` for the primary contrast).
2. The baseline + `C_PF` model has a significantly better fit (likelihood-ratio `p < 0.05`).
3. The held-out `ΔAUC` is at least `0.03`.
4. `C_PF` remains a significant predictor in a multivariate model that includes all baselines.

If `C_PF` is no better than the best single baseline, the label is **NO-INCREMENTAL-VALIDITY**, even if the raw AUC is above chance.

---

## 3. What must be frozen before data inspection: a checklist

- [ ] **One versioned equation and one production path.** `compute_cpf.py` and `compute_cpf_bands.py` cannot remain as simultaneous active alternatives for the same analysis.
- [ ] Exact Git commit hash of the registered code and the protocol version (e.g. `pre-registration v1.0-RouteE`).
- [ ] Dataset identifier, DOI, access date, condition table, and channel mapping.
- [ ] Inclusion and exclusion rules, including the minimum-epoch rule.
- [ ] Hardware and acquisition details (device, sampling rate, montage, reference).
- [ ] Preprocessing script: filter type, order, cutoffs, padding, resampling rule.
- [ ] Epoching: length, overlap, artifact threshold, minimum retained epochs.
- [ ] Delay-embedding parameters: `d`, `τ`, variable construction, edge handling.
- [ ] Differentiation method: PCA, entropy normalization, rank handling.
- [ ] Coherence formula: wPLI and PLV definitions, channel-pair set.
- [ ] Directed / self-model estimator: exact formula, lags, conditioning, normalization, surrogate null, and source file.
- [ ] Composite formula and any clipping/flooring.
- [ ] Random seeds for data split, null generation, surrogate generation, and cross-validation.
- [ ] All synthetic null and positive control generators and their parameters.
- [ ] Comparator formulas, code, and parameter values (bands, `m`, `r`, `k_max`, etc.).
- [ ] Primary and secondary outcomes, including exact condition contrasts.
- [ ] Statistical tests, significance thresholds, and multiple-comparison correction.
- [ ] Interpretation rules and error-label definitions.
- [ ] Development / held-out split and external replication dataset.
- [ ] Pre-registration timestamp, version URL, and repository commit.
- [ ] Analysis code committed and frozen.

Nothing on this list may be changed after the first `C_PF` value is computed on the target data. Any post-hoc change is an explicit protocol amendment and must be registered with a new version number and a reason.

---

## 4. Boundary statement: what the protocol can and cannot establish

### What this protocol can, in principle, establish

- Whether a specific multivariate-signal composite (`C_PF_reduced_wpli` in Track A, or `C_PF` in Track B) shows systematic variation across the pre-registered physiological and synthetic conditions on held-out data.
- Whether the composite is robust against the pre-registered synthetic null confounds.
- Whether the composite adds predictive information beyond the pre-registered arousal, complexity, report, task, signal-quality, and PCI baselines on held-out data.
- Whether the *structural-correlate* hypothesis (a closed, differentiated, lag-aware self-referential signal structure covaries with certain states) is consistent with the data, or whether the instrument is confounded.

### What this protocol cannot establish

- **Consciousness detection, measurement, or proof.** The protocol tests a signal-processing composite, not phenomenal experience.
- **Necessity or sufficiency.** A positive result would not show that the structure is necessary or sufficient for consciousness; a negative result would not show that consciousness is absent.
- **Generalization to other substrates.** The protocol is bound to the registered EEG channel layout, frequency band, and estimator; it does not apply to animals, AI systems, quantum computers, or other physical substrates without a separate transfer argument.
- **The `M_obs → M_t` bridge.** Delay embedding reconstructs a manifold; it does not prove that the reconstructed coordinates function as an endogenous self-model.
- **Clinical, medical, diagnostic, welfare, legal, or AI-personhood use.** The protocol is non-clinical research; no participant or system is classified as conscious or not conscious for any practical purpose.
- **PUBLIC HOLD lift.** No canonical promotion, public release, or claim-tier change follows from this design document.

---

## 5. Single most important pre-registration element currently missing

The **single most important missing element** is a **single, versioned, and independently validated self-model conditional-information estimator (`L_self`) that is frozen before any data are inspected**.

Why this is the critical gap:
- The current `compute_cpf.py` uses `D_dir_proxy`, a linear Granger prediction-gain proxy. It is **not** the documented `L_self = min(R_in, R_out)` gate, and it produces positive scores on acyclic feed-forward chains.
- The current `compute_cpf_bands.py` uses a different, incompatible composite (`D_int × C_coh × (1 + D_dir_proxy)`), which cannot force the metric to zero when directed structure is absent.
- The documented `L_self` cannot be pre-registered because the CMI estimator that implements it has not been repaired and independently checked (Route B), and the hostile controls that must validate each leg have not been run (Route C).

Until Route B delivers a valid `R_in` / `R_out` estimator, Route A confirms the exact parameter table, and Route C confirms each leg passes its own null and the positive self-loop control, the pre-registration cannot be locked to a *defensible structural-correlate* instrument. All other items — thresholds, held-out set, comparators, and statistics — depend on first knowing what is being measured.

### 5.1 Cross-route correction (2026-08-20)

Routes B and C are now complete. **Track A must not be frozen as the final pre-registered pipeline.** `D_dir_proxy` was shown to produce 25–40% FPR on the hostile control battery and cannot discriminate a positive closed self-model loop from an acyclic feed-forward chain or common-driver confound. The pre-registration should be **amended to Track B** (`C_PF = D_int × C_coh_wpli × L_self` with `L_self` from the single-joint-covariance CMI estimator) as soon as the Route B estimator is integrated into the production path and re-run through the Route C battery.
