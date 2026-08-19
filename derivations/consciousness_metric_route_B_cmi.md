# Route B — CMI Estimator Repair for `L_self = min(R_in, R_out)`

**Status:** Repair probe / sandbox result. **NOT a claim of consciousness detection.**  
**Scope:** `cpf/directed.py` (production self-loop proxy) and the separate-Ledoit-Wolf CMI construction used in the July null-class sandbox.  
**Public hold:** PUBLIC HOLD on Fundamentals remains in effect. No promotion of `consciousness.md` or `consciousness_metric_program.md`.

---

## 1. What is being repaired

The written metric in `definitions/consciousness_metric_program.md` (§ Self-reference loop gate, lines 40-57) defines

```
R_in(L)  = I_dir( X_{t-L:t-1} → M_t | E_{t-L:t} )
R_out(L) = I_dir( M_t → X_{t+1:t+L} | X_t, E_t )
L_self(L) = min( R_in_normalized, R_out_normalized )
```

Two implementations currently fail:

1. **Production `cpf/directed.py`** (`tools/consciousness_metric/cpf/directed.py:4-55`) is a one-step linear VAR / Granger prediction-gain, not a conditional-mutual-information estimator.  It never constructs `R_in` or `R_out`, never conditions on `E`, and has no notion of the model variable `M`.  It is used as `D_dir_proxy` in `cpf/score.py:31-36`.

2. **The July null-class CMI sandbox** (`sandbox/consciousness_metric_null_class_test.py:61-94`) does compute `R_in` and `R_out`, but it estimates each mutual-information term with a *separately* fit Ledoit-Wolf covariance.  Separate shrinkage targets destroy the Gaussian identity

```
H(A|C) = H(A,C) - H(C)
```

because the determinants are no longer taken from the same matrix.  That produces a large spurious residual and, under the old `min(1, cmi/ceiling)` normalization, can clip `R_out` to `1.0` on a Class-I null (Codex audit P3).

---

## 2. Quantitative evidence that the current proxy fails

The prototype at `sandbox/consciousness_cmi_repair_probe.py` runs the production `cpf.directed.compute_prediction_gain` on the same synthetic `X/M/E` traces that the new CMI estimator scores.

| System | True `L_self` (population) | `D_dir_proxy` from `cpf/directed.py` | What the proxy is actually measuring |
|---|---:|---:|---|
| White noise | 0.00000 | 0.00101 ± 0.00012 | Low by construction; no dynamics to exploit. |
| Class I — exogenous-only | 0.00000 | 0.00102 ± 0.00030 | M has no dynamics, so the VAR cannot extract gain. |
| Class II — passive tracker | **0.00000** | **0.21286 ± 0.00092** | M has its own AR and tracks X; the proxy cannot tell that M does **not** drive X. |
| Feed-forward chain | 0.00000 | 0.42358 ± 0.00127 | Pure acyclic temporal chain gives high cross-lag prediction gain. |
| Synchrony, no model | 0.05225 | 0.39619 ± 0.00447 | Common-mode phase relations produce cross-channel prediction gain. |
| Positive linear loop | **0.59850** | 0.43454 ± 0.00378 | Similar magnitude to the no-loop cases. |

The proxy has **no leg-specific gating**.  It fires on any cross-lag predictability, so it cannot play the role of `L_self = min(R_in, R_out)`.

The Codex audit P4 (acyclic feed-forward chain) already reported `D_dir_proxy = 0.81`; the new probe reproduces the same failure mode (feed-forward chain → 0.42) and extends it to a Class-II system, where the proxy is 0.21 on a system with a **proven zero outbound leg**.

---

## 3. Proposed single-joint-covariance estimator

### 3.1 Design

For jointly Gaussian `(A, B, C)` with covariance `Σ`, use the entropy identity

```
I(A;B|C) = H(A,C) + H(B,C) - H(C) - H(A,B,C)
         = 0.5 * log( det(Σ_AC) · det(Σ_BC)
                      / (det(Σ_C) · det(Σ_ABC)) )
```

The repair is: **fit one Ledoit-Wolf covariance to the full concatenated vector `[A; B; C]`, then extract every block determinant from that single matrix.**  This makes the identity exact at the chosen regularization level.  No second, separately-shrunk covariance is used for `(A,C)` or `(A,BC)`.

Implementation: `sandbox/consciousness_cmi_repair_probe.py:82-180` (`fit_joint_cov`, `gaussian_cmi_from_cov`, `single_cov_cmi`).

### 3.2 `R_in` and `R_out` alignment

```
R_in  = I( X_{t-1} ; M_t | E_t )
R_out = I( M_t ; X_{t+1} | X_t, E_t )
L_self = min( normalize(R_in), normalize(R_out) )
```

Code: `estimate_R_in_R_out` at `sandbox/consciousness_cmi_repair_probe.py:182-212`.

### 3.3 Normalization

We normalize by the monotonic map `R_norm = 1 - exp(-R_nats)`.  It is in `[0,1)`, stable near zero, and does **not** require a second (separately estimated) unconditional-MI ceiling.  The old `min(1, cmi/ceiling)` ratio is included as `broken_R_in_R_out` for comparison and is shown to over-estimate the positive loop.

### 3.4 Analytic / population reference

For linear-Gaussian state-space models `Y_t = A Y_{t-1} + B E_t + W_t` with `Y = [X; M]`, the stationary covariance `Σ_Y` is obtained from the discrete Lyapunov equation.  From `Σ_Y` and the one-step cross-covariances `Σ_Y A^T` and `A Σ_Y`, the exact population covariance of `(X_{t-1}, M_t, E_t)` and `(M_t, X_{t+1}, X_t, E_t)` is built algebraically.  This gives the **true** `R_in` and `R_out` for the linear nulls and the linear positive loop.

Code: `population_R_in_R_out` at `sandbox/consciousness_cmi_repair_probe.py:456-519`.

---

## 4. Results

Settings: `dX = dM = dE = 3`, `T = 8000`, `12` independent trials.  Values are means ± std from the sample estimator; population values are exact for the linear-Gaussian cases.

### 4.1 (a) White noise / Class-I null

| Quantity | White noise (population) | White noise (sample) | Class I (population) | Class I (sample) |
|---|---|---|---|---|
| `R_in` nats | 0.00000 | 0.00001 ± 0.00003 | 0.00000 | 0.00046 ± 0.00021 |
| `R_out` nats | 0.00000 | 0.00001 ± 0.00002 | 0.00000 | 0.00060 ± 0.00020 |
| `L_self` | 0.00000 | 0.00000 ± 0.00000 | 0.00000 | 0.00000 ± 0.00000 |

Both nulls are recovered to well below the `0.08` sanity threshold.  The non-zero but tiny `R_in/R_out` nats in Class-I are finite-sample residual; the normalized `L_self` is rounded to zero by the noise floor.

### 4.2 (b) Class-II null

| Quantity | Population (true) | Sample estimator | Broken separate-LW CMI | `cpf/directed.py` proxy |
|---|---:|---:|---:|---:|
| `R_in` nats | **0.87962** | 0.87070 ± 0.01048 | — | — |
| `R_out` nats | **0.00000** | 0.00066 ± 0.00036 | — | — |
| `R_out` norm | 0.00000 | 0.00066 | **0.03064** | — |
| `L_self` | **0.00000** | 0.00000 ± 0.00000 | 0.03064 | 0.21286 |

The new estimator respects the analytic fact that `R_out = 0`.  The `min` gate therefore gives `L_self = 0`.  The broken estimator leaks 0.03, and the production directed proxy leaks 0.21 — it cannot distinguish the inbound leg from the outbound leg.

### 4.3 (c) Positive closed self-model loop

**Linear positive loop (constructed, with analytic reference):**

| Quantity | Population (true) | Sample estimator | Broken CMI | `cpf/directed.py` proxy |
|---|---:|---:|---:|---:|
| `R_in` nats | 1.76620 | 1.73540 ± 0.02849 | — | — |
| `R_out` nats | 0.91254 | 0.90337 ± 0.01416 | — | — |
| `L_self` | **0.59850** | **0.59476 ± 0.00573** | 0.74047 | 0.43454 |

`R_in` and `R_out` are both positive, the gate opens, and the sample estimate is within ~1% of the population value.  This is a positive control that does **not** fire vacuously.

**Bounded non-linear positive loop (tanh):**

| Quantity | Sample estimator |
|---|---|
| `R_in` nats | 2.47284 ± 0.63743 |
| `R_out` nats | 0.87885 ± 0.47004 |
| `L_self` | **0.52942 ± 0.26112** |

The tanh loop is not analytically tractable, but the sample `L_self = 0.53` is well above the null threshold and comparable to the linear positive control.  The higher variance is expected for a strongly non-linear system and is acceptable for a sandbox positive control.

### 4.4 Additional hostile checks

| System | True `L_self` | New `L_self` | `cpf/directed.py` | Verdict |
|---|---:|---:|---:|---|
| Feed-forward chain | 0.00000 | 0.00000 ± 0.00000 | 0.42358 | `L_self` correctly zero; proxy false-positive. |
| Synchrony, no loop | — | 0.05225 ± 0.00332 | 0.39619 | `L_self` below 0.08; proxy false-positive. |

---

## 5. Why the broken construction fails in detail

The old CMI in `sandbox/consciousness_metric_null_class_test.py:85-94` calls

```python
mi_xy(a, bc) - mi_xy(a, c)
```

with a **new** `LedoitWolf().fit(...)` for each `mi_xy` call.  Because each fit shrinks toward a different target, the two resulting determinants do not satisfy `H(A|C) = H(A,C) - H(C)`.  The Codex audit P3 found that this produced

```
conditional-MI estimate: 0.2445 nats
unconditional-MI ceiling: 0.0505 nats
ratio: 4.84
reported normalized outbound: 1.0
regression-residual Gaussian CMI check: 0.0002 nats
```

The new `single_cov_cmi` eliminates this by construction: all four determinants (`Σ_AC`, `Σ_BC`, `Σ_C`, `Σ_ABC`) are sub-blocks of **one** Ledoit-Wolf matrix.

---

## 6. Remaining assumptions and PF-native status

| Assumption | Status |
|---|---|
| The model variable `M_t` is observable / recoverable. | **NOT PF-native.** The `M_obs_t → M_t` bridge in `consciousness_metric_program.md:159-177` is still open.  Delay embedding is only a candidate surrogate. |
| Gaussian generative model for CMI. | **PF-native for the linear nulls**, because the analytic CMI is exact.  For real (non-Gaussian, non-stationary) data, a non-parametric KSG/k-NN CMI would be required. |
| Single-joint Ledoit-Wolf covariance. | **PF-native instrument repair.**  It is a standard high-dimensional covariance estimator and closes the algebraic identity bug. |
| `L_self = min(R_in, R_out)` gate. | **PF-native by definition.**  The spec defines this; the prototype implements it exactly. |
| Coherence (`C_coh`) and differentiation (`D_int`) components. | **Out of scope for this route.**  They are orthogonal and still have their own hostile controls. |
| `F_model` (Fisher information of future with respect to `M_t`). | **Not implemented.**  The current production scorer (`cpf/score.py`) uses `D_dir_proxy` directly, not `L_self × F_model`.  This is a Route A / equation-parity issue. |
| Threshold `0.08` and `T = 8000`. | **Calibration, not pre-registration.**  As noted in the Codex audit F4 and the repair scoping doc, the window/threshold were chosen during development.  A real held-out protocol is still required (Route E). |

The CMI repair is therefore a **valid structural-correlate instrument step**, not a consciousness-detection result.

---

## 7. Conclusion and next steps

- **Repair achieved:** A single-joint-covariance Gaussian CMI estimator correctly computes `R_in`, `R_out`, and `L_self = min(R_in, R_out)`.  It passes Class-I, Class-II, feed-forward, and synchrony nulls, and it opens on a constructed positive closed self-model loop.  Sample estimates agree with analytic population CMIs for the linear cases.
- **Production still broken:** `cpf/directed.py` and `cpf/score.py` remain unchanged and still return a generic Granger prediction gain, not `L_self`.  Route A must deprecate the two production entry points (`compute_cpf.py` and `compute_cpf_bands.py`) and choose one equation + one implementation.
- **No promotion:** This work does **not** detect or measure consciousness.  The PUBLIC HOLD on Fundamentals is preserved.

**Files produced / changed (new only):**

- `sandbox/consciousness_cmi_repair_probe.py`
- `sandbox/consciousness_cmi_repair_probe_results.json` (auto-generated by the probe)
- `derivations/consciousness_metric_route_B_cmi.md`

No existing source files were modified.
