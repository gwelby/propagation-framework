# Route C — Hostile Control Battery for the C_PF Reduced Metric

**Status:** Route C repair probe — measurement and boundary report.  
**Authority tier:** advisory / internal.  
**PUBLIC HOLD:** Remains in effect. No claim that this instrument detects, measures, or proves consciousness.  
**Scope:** Add and run hostile negative and positive controls; report the false-positive/negative landscape.  

This report does **not** lift the Fundamentals PUBLIC HOLD, does **not** authorize promotion of any consciousness claim, and does **not** assert that the C_PF score is a valid correlate of consciousness.

---

## 1. What was done

1. Added a new pytest file at `/mnt/d/Fundamentals/sandbox/test_consciousness_hostile_controls.py`.
2. Implemented the six requested hostile controls:
   1. Acyclic temporal feed-forward chain.
   2. Synchronized no-model / no-loop system.
   3. Time-shifted surrogate.
   4. Phase-randomized surrogate.
   5. Common-driver confound.
   6. Positive closed self-model loop.
3. Also included the three existing nulls (`white_noise`, `collapsed_synchrony`, `thermostat`) as a baseline battery.
4. Ran the battery through `cpf.score.compute_cpf_components` with `tau=2`, `d=3`, `n_samples=1500`, `seed=42`.
5. Collected `D_int`, `C_coh_plv`, `C_coh_wpli`, `D_dir_proxy`, and `C_PF_reduced_wpli` for each control.

**Command run:**

```text
python3.12 -m pytest -q -s /mnt/d/Fundamentals/sandbox/test_consciousness_hostile_controls.py
```

Result: `10 passed in 21.92s`.

---

## 2. Metric reminder

The tested production path (`cpf/score.py`) implements:

\[ C_{PF,reduced,wpli} = D_{int} \times C_{coh,wpli} \times D_{dir,proxy} \]

with `D_dir_proxy` a one-lag linear Granger prediction-gain proxy (`cpf/directed.py`).  This is **not** the documented self-model gate `L_self = min(R_in, R_out)` and is not a consciousness-detection instrument.

---

## 3. Control outcomes

| Control | Kind | Expected `C_PF` | `D_int` | `C_coh_plv` | `C_coh_wpli` | `D_dir_proxy` | `C_PF_reduced_wpli` | Verdict at threshold 0.05 |
|---|---|---|---:|---:|---:|---:|---:|---|
| white_noise | negative | ≈ 0 | 0.9986 | 0.0280 | 0.0278 | 0.0013 | 0.0000 | PASS |
| collapsed_synchrony | negative | ≈ 0 | 0.1869 | 0.9900 | 0.0371 | 0.1776 | 0.0012 | PASS |
| thermostat | negative | ≈ 0 | 0.2373 | 1.0000 | 0.1090 | 0.0000 | 0.0000 | PASS |
| acyclic_feedforward_chain | negative | ≈ 0 | 0.2782 | 0.9423 | 0.9976 | 0.9240 | **0.2564** | **FALSE POSITIVE** |
| synchronized_no_model | negative | ≈ 0 | 0.2125 | 0.9975 | 0.0319 | 0.0352 | 0.0002 | PASS |
| time_shifted_surrogate | negative | ≈ 0 | 0.9841 | 0.0370 | 0.0495 | 0.0010 | 0.0001 | PASS |
| phase_randomized_surrogate | negative | ≈ 0 | 0.6780 | 0.1592 | 0.1920 | 0.0558 | 0.0073 | PASS |
| common_driver_confound | negative | ≈ 0 | 0.3245 | 0.9077 | 0.9728 | 0.6897 | **0.2177** | **FALSE POSITIVE** |
| closed_self_model_loop | positive | > 0 | 0.7066 | 0.4403 | 0.4019 | 0.4539 | 0.1289 | Non-zero, but **not discriminated** |

*Values are rounded to 4 decimal places.  The threshold 0.05 is the same order of magnitude used by the existing `tools/consciousness_metric/tests/test_nulls.py` battery.*

---

## 4. False-positive / false-negative landscape

### 4.1 Negative controls

- **Total negative controls:** 8 (3 existing + 5 new).
- **False positives** (`C_PF_reduced_wpli >= 0.05`): 2
  - `acyclic_feedforward_chain`: 0.2564
  - `common_driver_confound`: 0.2177
- **False-positive rate (FPR) at threshold 0.05:** 2 / 8 = **25%**.
- **FPR on the 5 new hostile negatives only:** 2 / 5 = **40%**.

The two failing controls are exactly the failure modes the audit flagged:

- **Acyclic feed-forward chains** satisfy `D_dir_proxy` because a one-lag linear VAR treats cross-lag prediction gain as directed structure, even when no feedback or model variable exists.
- **Common-driver confounds** satisfy both `C_coh_wpli` (different delays create non-zero phase lag) and `D_dir_proxy` (the lagged driver can be predicted from other channels), even though the observed channels are only driven by a hidden source and are not a self-model.

### 4.2 Positive control

- **Closed self-model loop `C_PF_reduced_wpli`:** 0.1289.
- **Max negative `C_PF_reduced_wpli`:** 0.2564 (acyclic feed-forward).
- **Discrimination gap:** 0.1289 − 0.2564 = **−0.1275**.

**Verdict:** The positive control is **non-zero**, so the metric is not completely blind to closed loops.  However, it is **not discriminated**: its score sits below the strongest negative controls.  Any threshold chosen to reject the acyclic feed-forward and common-driver false positives would also reject the genuine positive loop.

At the 0.05 threshold, the false-negative rate is 0 / 1 = **0%**, but this is misleading because the positive is not the highest-scoring condition.

---

## 5. Gaps in the test battery and the metric

1. **No self-model variable `M_t`.** The metric has no explicit model variable or bidirectional conditional-information gate (`R_in`, `R_out`, `L_self`). `D_dir_proxy` is a generic Granger gain, so any directed temporal structure scores.

2. **No causal-direction asymmetry test.** The one-lag linear regression cannot distinguish feed-forward (X → Y) from feedback (X ↔ M) or from common-driver with delays. A valid self-model gate needs inbound and outbound conditional-information estimators that pass their own nulls.

3. **`C_coh_wpli` is not specific enough.** Non-zero phase lag can be produced by delayed common drivers, delayed feed-forward chains, or genuine feedback loops. wPLI alone cannot separate these cases.

4. **`D_int` is a PCA-entropy proxy, not a self-loop gate.** It rewards high-dimensional manifolds but does not test whether the dimensionality is sustained by a closed model.

5. **The band implementation (`compute_cpf_bands.py`) uses a different equation.** `C_PF = D_int × C_coh × (1 + D_dir_proxy)` means a no-loop synchronized system can still produce a positive score, as the audit demonstrated (`C_PF_reduced = 0.3200827`). The new test battery was run against `cpf/score.py`; the band path still needs an equivalent hostile battery.

6. **No signal-quality / arousal / artifact controls.** The battery does not yet include amplitude normalization, dropout, pink noise, or eye-blink/muscle confounds.

7. **No held-out real data or pre-registered threshold.** The 0.05 threshold is ad hoc; the battery was calibrated here, not locked before inspection.

8. **No comparator metrics.** There is no comparison against perturbational complexity, simple complexity, report, task, or signal-quality baselines.

---

## 6. Boundary and next step

The hostile control battery reproduces and extends the 2026-08-19 Codex audit finding: the current C_PF reduced scorer is **not a specific self-model detector**. It fails on the two structural false-positive patterns it most needs to reject (acyclic feed-forward and common-driver confounds) and it fails to make the positive closed self-model loop the highest-scoring condition.

**Next:** Route B (repair the bidirectional conditional-information estimator) and Route A (choose one versioned equation and one production path) are prerequisites for any further control work. Without a valid `L_self` and a single operational definition, additional controls will continue to find the same class of false positives.

**PUBLIC HOLD remains.** This report does not approve promotion, public release, medical/clinical use, human/animal/AI/quantum classification, or canonical status for any consciousness metric.
