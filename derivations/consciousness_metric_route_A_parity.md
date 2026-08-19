# Consciousness Metric — Route A: Equation/Implementation Parity

**Status:** REPAIR SCOPING — NOT A CLAIM OF CONSCIOUSNESS DETECTION OR MEASUREMENT.  
**Authority tier:** advisory — instrument repair and boundary audit only.  
**Public hold:** PUBLIC HOLD on the consciousness metric and `consciousness_metric_program.md` remains in effect. No canonical promotion.  
**Scope:** audit the three coexisting definitions of `C_PF` and recommend one versioned operational equation plus one production path.  
**Constraint:** no source files were modified in producing this report.  

---

## Executive summary

- The spec in `definitions/consciousness_metric_program.md` defines `C_PF = C_coh × D_int × L_self × F_model` with `L_self = min(R_in, R_out)`; neither production entry point implements `M_t`, `R_in`, `R_out`, `L_self`, or `F_model`.
- `compute_cpf.py` / `cpf/score.py` computes `C_PF_reduced = D_int × C_coh × D_dir_proxy` for both PLV and wPLI. The wPLI variant is the one enforced by the existing test suite and is the only production composite with the correct multiplicative null-gate shape.
- `compute_cpf_bands.py` computes `C_PF_reduced = D_int × C_coh × (1 + D_dir_proxy)`, using a band-specific alpha–gamma cross-correlation asymmetry. The `(1 + D_dir_proxy)` factor makes the score non-zero even when the directed proxy is zero, directly contradicting the documented null logic.
- **Recommendation (parity only):** the `C_PF_reduced_wpli` line in `cpf/score.py` has the correct *multiplicative* shape and should be the production path, but `D_dir_proxy` is a placeholder, not `L_self`. Routes B and C falsified `D_dir_proxy` as a self-loop gate (25–40% FPR; 0.21 on Class II, 0.42 on feed-forward). The actual v1.0 operational equation is therefore `C_PF^v1.0 = D_int × C_coh_wpli × L_self` using the repaired CMI estimator from Route B. Deprecate `compute_cpf_bands.py` because its formula is structurally incompatible.

---

## 1. Exact current state of the three `C_PF` paths

### 1.1 Spec / theoretical definition

File: `definitions/consciousness_metric_program.md`

- State split: `Z_t = (X_t, M_t, E_t)` (line 30), with `M_t` the internal model state.
- Inbound / outbound directed information legs:
  - `R_in(L)  = I_dir( X_{t-L:t-1} → M_t | E_{t-L:t} )` (line 45)
  - `R_out(L) = I_dir( M_t → X_{t+1:t+L} | X_t, E_t )` (line 47)
- Self-reference loop gate: `L_self(L) = min(R_in_normalized, R_out_normalized)` (line 53).
- Self-model sensitivity: `F_self*(L) = L_self(L) × F_model(L)` (line 61), where `F_model` is the Fisher information of the future trajectory with respect to the model state.
- Full candidate score: `C_PF(L) = C_coh(L) × D_int(L) × F_self*(L)` (line 69).
- Observable surrogate: `M_obs_t` is a delay-embedded sensor vector (lines 95–98); the proxy quantities `L_self_proxy`, `D_int_proxy`, `C_coh_proxy`, and `C_PF_proxy` are declared (lines 103–108) but the document does not give an explicit `C_PF_proxy` formula. The coherence panel is stated to be a two-proxy panel (PLV + wPLI, lines 116–118) and explicitly “not a single scalar” (line 120).

This path is the only one that contains the theorem-grade state split and the bidirectional conditional-information gate. It is **not implemented** in code.

### 1.2 Production A — `compute_cpf.py` → `cpf/score.py`

Files: `tools/consciousness_metric/compute_cpf.py`, `tools/consciousness_metric/cpf/score.py`, `tools/consciousness_metric/cpf/embedding.py`, `tools/consciousness_metric/cpf/differentiation.py`, `tools/consciousness_metric/cpf/coherence.py`, `tools/consciousness_metric/cpf/directed.py`

- `compute_cpf.py` is a CLI that loads a Muse CSV, bandpass-filters 1–45 Hz, epochs the data, rejects artifacts, and calls `compute_cpf_components` for each epoch (lines 28–58).
- `cpf/score.py::compute_cpf_components` (lines 7–45):
  - `embedded_data = delay_embed(data, tau, d)` (line 22)
  - `D_int = compute_pca_entropy(embedded_data)` (lines 23–25)
  - `C_coh_plv = compute_plv(data)` (line 28)
  - `C_coh_wpli = compute_wpli(data)` (line 29)
  - `D_dir_proxy = compute_prediction_gain(data)` (line 32)
  - `C_PF_reduced_plv = D_int * C_coh_plv * D_dir_proxy` (line 35)
  - `C_PF_reduced_wpli = D_int * C_coh_wpli * D_dir_proxy` (line 36)
- `cpf/embedding.py::delay_embed` (lines 3–31): stacks lagged samples `(d-1)*tau` back, producing shape `(n_samples - (d-1)*tau, n_channels * d)`.
- `cpf/differentiation.py::compute_pca_entropy` (lines 4–55): fits `sklearn.decomposition.PCA`, computes Shannon entropy of the normalized explained-variance distribution using `log2`, and normalizes by `log2(max_rank)` where `max_rank = min(n_samples, n_features)`.
- `cpf/coherence.py`:
  - `compute_plv` (lines 4–30): Hilbert transform per channel, mean over pairs of `|⟨exp(i·Δφ)⟩|`.
  - `compute_wpli` (lines 32–64): mean over pairs of `|⟨Im(cross_spectra)⟩| / ⟨|Im(cross_spectra)|⟩`.
- `cpf/directed.py::compute_prediction_gain` (lines 4–55): for each target channel, predicts `data[target, 1:]` from `data[target, :-1]` (self model) and from `data[:, :-1].T` (all-channel model). The per-channel gain is `max(0, (var_self - var_all) / var_self)`, and `D_dir_proxy` is the mean gain across channels (lines 46–53).

The existing test suite (`tools/consciousness_metric/tests/test_nulls.py`, lines 12–47) asserts `C_PF_reduced_wpli < 0.05` on the white-noise, collapsed-synchrony, and thermostat nulls.

### 1.3 Production B — `compute_cpf_bands.py`

File: `tools/consciousness_metric/compute_cpf_bands.py`

- Input is a CSD band-power CSV with columns `timestamp, delta, theta, alpha, beta, gamma` at approximately 9 Hz (lines 22–49).
- Windows are 5 minutes by default, stepped 5 minutes; each window is broken into 10-second sub-epochs and artifact-rejected (lines 54–69, 156–205).
- `compute_d_int_bands` (lines 92–109): covariance of the 5 band time series, eigenvalue entropy normalized by `log(len(eigenvalues))` (natural log).
- `compute_plv_bands` (lines 72–90): Hilbert transform of each band, mean off-diagonal pairwise PLV.
- `compute_dir_proxy_bands` (lines 111–128): alpha → gamma and gamma → alpha cross-lagged Pearson correlation asymmetry, `max(0, |r_forward| - |r_backward|)` (line 125).
- `compute_cpf_epoch` (lines 130–154) returns:
  - `C_coh_alpha_gamma = plv_matrix[2, 4]` (alpha-gamma PLV, line 141)
  - `C_PF_reduced = d_int * c_coh_plv * (1.0 + dir_proxy)` (lines 145–146)

There is no wPLI, no `F_model`, no `L_self`, and the directed proxy is hardcoded to alpha–gamma only.

---

## 2. Diff / alignment table: spec vs `compute_cpf.py` vs `compute_cpf_bands.py`

| Dimension | Spec (`definitions/consciousness_metric_program.md`) | `compute_cpf.py` / `cpf/score.py` | `compute_cpf_bands.py` | Verdict |
|---|---|---|---|---|
| **Final `C_PF` formula** | `C_PF = C_coh × D_int × L_self × F_model` (line 69), `L_self = min(R_in, R_out)` (line 53) | `C_PF_reduced_plv = D_int × C_coh_plv × D_dir_proxy` (line 35) and `C_PF_reduced_wpli = D_int × C_coh_wpli × D_dir_proxy` (line 36) | `C_PF_reduced = D_int × C_coh_plv × (1 + D_dir_proxy)` (lines 145–146) | `compute_cpf.py` is closer in algebraic shape; `compute_cpf_bands.py` is structurally incompatible. |
| **State / model variable** | Explicit split `Z_t = (X_t, M_t, E_t)` (line 30); `M_t` is a model of the system’s own future (lines 35–36) | No `M_t`; delay-embedding of all channels is used for both `D_int` and `D_dir_proxy` | No `M_t`; operates on five band-power time series | Neither implements the spec state split. |
| **Differentiation `D_int`** | Effective rank of the internal model manifold (line 73) | PCA entropy of delay-embedded all-channel covariance (`cpf/differentiation.py` lines 4–55, `cpf/embedding.py` lines 3–31) | PCA entropy of 5-band covariance (`compute_cpf_bands.py` lines 92–109) | Both are PCA-entropy proxies but on different input spaces and with different log normalization. |
| **Coherence `C_coh`** | Panel of PLV + wPLI, “not a single scalar” (lines 116–120) | Two separate scalars: `C_coh_plv` and `C_coh_wpli` (`cpf/coherence.py`); no panel combination rule | PLV only (`compute_plv_bands` lines 72–90); also reports `C_coh_alpha_gamma` (line 141) | `compute_cpf.py` provides both proxies; `compute_cpf_bands.py` is PLV-only. Tests enforce the wPLI composite (`tests/test_nulls.py` line 21). |
| **Self-model / directed term** | `L_self = min(R_in, R_out)`, conditional directed information (lines 45–53) | `D_dir_proxy` = unidirectional linear Granger prediction gain (`cpf/directed.py` lines 4–55) | `D_dir_proxy` = alpha–gamma cross-lagged correlation asymmetry (`compute_cpf_bands.py` lines 111–128) | Both are placeholders; neither is the spec’s bidirectional CMI. |
| **Sensitivity `F_model`** | Fisher information of future trajectory wrt model state (lines 61, 64–65) | Not implemented | Not implemented | Missing in both paths. |
| **Null-gate property** | If either `R_in` or `R_out` is zero, `L_self = 0` ⇒ `C_PF = 0` (lines 83–86) | Product form is zero if `D_dir_proxy = 0`, but `D_dir_proxy` can be positive for acyclic feed-forward chains (Codex P4) | `C_PF` remains `D_int × C_coh` when `D_dir_proxy = 0` because of `(1 + D_dir_proxy)` (Codex P5) | `compute_cpf.py` has the right algebraic shape; the bands path fails the documented null logic. |
| **Data domain** | EEG / time-series; delay-embedding parameters (lines 95–99) | Muse EEG, 256 Hz, 1–45 Hz bandpass, 2 s epochs | CSD band-power CSV, ~9 Hz, 5-min windows, delta/theta/alpha/beta/gamma | Different input surfaces; not interchangeable. |
| **Output variants** | Single `C_PF` | Two composites (`plv`, `wpli`) plus diagnostics | Single `C_PF_reduced` plus `C_coh_alpha_gamma` | `compute_cpf.py` has redundant variants; v1.0 should pick one. |
| **Known hostile false positives** | Feed-forward and passive tracker collapse to zero by construction (lines 83–87) | Acyclic temporal feed-forward chain scored `C_PF_reduced_wpli ≈ 0.15` (Codex P4, audit lines 153–167) | Five phase-locked oscillators with no loop/model scored `C_PF_reduced ≈ 0.32` (Codex P5, audit lines 170–188) | Both produce false positives; the bands path is worse. |

---

## 3. Recommendation: versioned v1.0 operational equation and production path

### 3.1 v1.0 equation

Adopt the `C_PF_reduced_wpli` line from `cpf/score.py` as the *shape* of `C_PF^v1.0`:

```
C_PF^v1.0 = D_int × C_coh_wpli × D_dir_proxy   [interim placeholder]
C_PF^v1.0 = D_int × C_coh_wpli × L_self        [target after Route B lands]
```

Source reference for the interim shape: `tools/consciousness_metric/cpf/score.py`, line 36.

**Correction after Routes B and C (2026-08-20):** `D_dir_proxy` is empirically unsound as a self-loop gate. It scores 0.21 on a Class-II null (proven `R_out = 0`) and 0.42 on an acyclic feed-forward chain, so it cannot serve as `L_self`. The validated v1.0 equation is `C_PF = D_int × C_coh_wpli × L_self` with `L_self` from the single-joint-covariance CMI repair.

`C_coh_wpli` is the default coherence factor because:
- The 2026-04-18 Codex audit concluded that PLV alone is “too inflation-prone” and the program switched to a PLV + wPLI panel (`consciousness_metric_program.md` lines 113–118).
- wPLI suppresses zero-lag / common-mode / volume-conduction artifacts (`cpf/coherence.py::compute_wpli`, lines 32–64).
- The existing null tests assert `C_coh_wpli < 0.1` and `C_PF_reduced_wpli < 0.05` on the white-noise and collapsed-synchrony nulls (`tests/test_nulls.py`, lines 17–21 and 30–36).

`D_dir_proxy` in v1.0 is explicitly a **placeholder**: it is a linear Granger gain, not the spec’s `L_self = min(R_in, R_out)`. The v1.0 equation is therefore a **reduced operational proxy**, not the full spec. Once Route B repairs the CMI estimator, `D_dir_proxy` should be replaced by `L_self` (and `F_model` still must be addressed).

### 3.2 Production path

Make `tools/consciousness_metric/compute_cpf.py` the single production CLI. It is the only entry point that:
- uses the modular `cpf/` library (`cpf/score.py`, `cpf/directed.py`, `cpf/coherence.py`, `cpf/differentiation.py`, `cpf/embedding.py`);
- offers both PLV and wPLI and can naturally carry a default wPLI variant;
- has the correct multiplicative null-gate shape;
- operates on the raw EEG pipeline described in the spec (bandpass, epoch, artifact rejection, delay embedding).

`compute_cpf.py` should also be the substrate for Route B: once the single-joint-covariance `L_self` estimator is placed in `cpf/self_model.py`, `cpf/score.py` can swap `D_dir_proxy` for `L_self` without touching the CLI surface.

### 3.3 Why not the other candidates

- **Spec equation as v1.0:** `M_t`, `R_in`, `R_out`, `L_self`, and `F_model` are not implemented. Choosing the spec as v1.0 would leave the codebase without a runnable reference.
- **`C_PF_reduced_plv` as v1.0:** PLV is inflation-prone and wPLI is the operational guardrail. The existing tests already treat wPLI as the gating coherence measure.
- **`compute_cpf_bands.py` as a production path:** its `(1 + D_dir_proxy)` factor violates the documented zero-null logic, it is PLV-only, it hardcodes an alpha–gamma directed proxy, and it is a standalone monolith rather than a reusable module.

---

## 4. Deprecation plan for the alternate entry point

The alternate entry point is `tools/consciousness_metric/compute_cpf_bands.py` and its incompatible `C_PF_reduced` formula.

### Immediate steps (no source edits)
1. Stop treating `compute_cpf_bands.py` output as comparable to `C_PF`. In all prose, dashboards, and reports, label it `C_PF_bands_legacy` or `C_PF_pre_v1.0_bands` and note the formula divergence.
2. Freeze any new band-based session analysis: do not use `compute_cpf_bands.py` for new data until it is migrated or deleted.

### Source-edit steps
3. Add a runtime deprecation warning to `compute_cpf_bands.py` (in the module docstring and on `--help` output) stating that the script is not aligned with `C_PF^v1.0` and is kept only for historical comparison.
4. Remove `compute_cpf_bands.py` from the benchmark battery, README, and any pre-registration protocol; redirect users to `compute_cpf.py`.
5. If band-power input remains a requirement, build a `cpf/bands.py` loader that converts the CSD CSV into a multi-channel array and calls `cpf/score.py::compute_cpf_components` with the v1.0 equation. This reuses the same `D_int`, `C_coh_wpli`, and `D_dir_proxy` machinery and removes the standalone `(1 + D_dir_proxy)` logic.
6. After Route B (CMI estimator) and Route C (hostile controls) land and the new band loader is validated, delete or archive `compute_cpf_bands.py`.

---

## 5. Gaps that cannot be closed without source edits

The following gaps are **not** fixable by documentation or versioning alone. They require source-code changes, and in some cases also theoretical work.

1. **No `M_t` variable.** The spec requires an explicit split `Z_t = (X_t, M_t, E_t)` (`consciousness_metric_program.md` line 30). No source file estimates or validates a model state. Source edits must add an `M_t` operationalization module or a validation that the delay-embedded surrogate `M_obs_t` functions as an endogenous self-model.

2. **No bidirectional conditional-information gate `L_self = min(R_in, R_out)`.** The spec defines `R_in` and `R_out` as conditional directed-information legs (lines 45–47). `cpf/directed.py` computes a unidirectional Granger gain, and `compute_cpf_bands.py` uses a cross-correlation asymmetry. Source edits must implement a CMI/directed-information estimator with separately tested `R_in` and `R_out` and replace `D_dir_proxy`.

3. **Broken outbound CMI estimator (Class-I).** The 2026-08-19 audit showed the current conditional-MI estimate is computed by subtracting MI terms from separately fitted Ledoit-Wolf covariances, which breaks the identity `H(X|Y) = H(X,Y) − H(Y)` and produces a spurious residual (Codex P3, audit lines 136–150). A regression-residual, single-covariance, or analytic CMI estimator must replace it.

4. **No `F_model` (Fisher sensitivity).** The spec multiplies `L_self` by `F_model` (`F_self* = L_self × F_model`, line 61). No code implements Fisher information of the future trajectory with respect to the model state. Source edits must add it or formally decide that v1.0 omits it.

5. **No `C_coh` panel combination rule.** The spec states the coherence panel is “not a single scalar” (line 120), but `cpf/score.py` returns separate `C_coh_plv` and `C_coh_wpli` (lines 28–29). A v1.x source edit must define a panel combination or keep `wpli` as the default scalar.

6. **`compute_cpf_bands.py` formula and directed proxy.** Its `(1 + D_dir_proxy)` factor and band-specific alpha–gamma cross-correlation asymmetry cannot be aligned with v1.0 without rewriting the script.

7. **Thresholds and pre-registration are not encoded.** The `0.08` threshold and `T=8000` sample size are calibration results, not a frozen protocol. Source / protocol edits must lock a pre-registration schema, exclusion rules, and threshold logic.

8. **No hostile control suite.** `tests/test_nulls.py` only covers white noise, collapsed synchrony, and a thermostat (lines 12–47). Source edits must add and assert acyclic temporal feed-forward, synchronized no-model, time-shifted/phase-randomized surrogates, common-driver, and positive closed self-loop controls.

9. **`M_obs_t → M_t` bridge remains open.** The spec acknowledges this as the central open problem (lines 159–177). It cannot be closed by source edits alone; it also needs a theoretical transfer argument or benchmark validation. Source edits can add validation checks but cannot prove the bridge.

10. **Falsifiers 4/5 and incremental validity not operational.** The spec lists falsifiers that require independent evidence of subjective experience and comparison with arousal/complexity/PCI baselines (`consciousness_metric_program.md` lines 143–153; Codex F7, audit lines 247–257). These need experimental and protocol infrastructure, not just metric code.

---

## 6. Boundary and next-step statement

- This report does **not** claim that any version of the score detects, measures, proves, or falsifies consciousness.
- It does **not** lift the PUBLIC HOLD on `consciousness_metric_program.md` or the `C_PF` metric.
- It does **not** approve medical, clinical, welfare, AI personhood, or public-release use.
- The next concrete step is Route B: repair the bidirectional conditional-information estimator so that `L_self` can replace `D_dir_proxy` in the chosen v1.0 production path (`compute_cpf.py` → `cpf/score.py`).

---

## 7. Verification

- Ran the existing null suite to confirm the wPLI composite is the tested path:
  `python3.12 -m pytest -q tools/consciousness_metric/tests/test_nulls.py`
  → `3 passed in 9.77s`.
- No source files were modified during verification.
