# Route D — Operationalizing the Five Structural Prerequisites

**Status:** repair probe / advisory — instrument boundary audit only.  
**Scope:** `definitions/consciousness.md` five structural prerequisites vs. the current Phase 0 metric.  
**Authority tier:** advisory. Does **not** detect, measure, or classify consciousness.  
**Public hold:** PUBLIC HOLD on Fundamentals remains in effect. No promotion of `consciousness.md`, `consciousness_metric_program.md`, or the metric as a consciousness test.

---

## 1. Current metric variables (for reference)

The production code does **not** implement the theorem-grade variables in `consciousness_metric_program.md`.  The actual variables are:

- `D_int` — PCA entropy of a delay-embedded manifold (`cpf/differentiation.py:54`; called from `cpf/score.py:23`).
- `C_coh_plv` / `C_coh_wpli` — mean phase-locking value and weighted phase-lag index (`cpf/coherence.py:27`, `:58`; called from `cpf/score.py:28-29`).
- `D_dir_proxy` — one-step linear VAR / Granger prediction-gain proxy (`cpf/directed.py:4-55`; called from `cpf/score.py:32` and `compute_cpf_bands.py:143`).
- `C_PF_reduced_plv` / `C_PF_reduced_wpli` — `D_int * C_coh * D_dir_proxy` (`cpf/score.py:35-36`).
- `C_PF_reduced` in the band entry point — `D_int * C_coh * (1 + D_dir_proxy)` (`compute_cpf_bands.py:146`).

The theorem-grade model variable `M_t`, the bidirectional conditional-information legs `R_in` / `R_out`, the self-model gate `L_self = min(R_in, R_out)`, and the Fisher sensitivity `F_model` are **not present in any production file**.

---

## 2. Prerequisite-by-prerequisite audit

### 2.1 Prerequisite 1 — Type 4 observer

*Statement in `consciousness.md`:* “The system's internal dynamics are modified by its own records. The record of past observations feeds back into the system's future state changes.”

| Criterion | Verdict |
|---|---|
| Currently implemented in the metric? | **Partially / ambiguously.** `D_dir_proxy` uses the past of all channels to predict the present of each channel, but it is a generic cross-lag prediction gain, not a record-to-future observer mechanism.  No record variable is extracted. |
| Independent of the others? | **No.** Prerequisite 2 (self-referential coherence / closed self-model loop) is a *stricter* form of the same idea: a model that is written by past state and that writes future state.  A Type-4 observer with a self-model is already covered by `L_self > 0`.  Keeping #1 as a separate prerequisite therefore double-counts the loop. |
| Proposed operational measure | Remove as an independent metric-tested prerequisite.  If a separate label is required, make it an *interpretive* consequence of `L_self > 0`: any system whose `M_t` is both written by `X` history and writes future `X` is a Type-4 observer by construction.  No new code variable is needed. |
| Threshold / calibration rule | None required once `L_self` is operational.  The Type-4 label follows from `L_self > θ_L` (see 2.2). |

**Recommendation:** remove #1 from the independent metric-tested prerequisite set; fold it into the self-model loop gate.

---

### 2.2 Prerequisite 2 — Self-referential coherence

*Statement in `consciousness.md`:* “Part of the system's internal state functions as a model of its own future propagation — and that model causally matters for the system's own dynamics. This is the loop gate `L_self > 0` from the consciousness metric program.”

| Criterion | Verdict |
|---|---|
| Currently implemented in the metric? | **No.** `cpf/score.py:35-36` multiplies by `D_dir_proxy`, not `L_self`.  `cpf/directed.py:4-55` is a linear Granger prediction-gain proxy; it does not construct `M_t`, does not condition on `E_t`, and does not have separate `R_in` / `R_out` legs.  The two production entry points even disagree on whether the directed term is multiplied or added (`cpf/score.py:35` vs. `compute_cpf_bands.py:146`). |
| Independent of the others? | **Yes, in intent.** It captures a directed, causal feedback relation that `D_int` (rank) and `C_coh` (phase stability) do not.  It is distinct from #3, #4, and #5. |
| Proposed operational measure | Implement the spec variables in `consciousness_metric_program.md:40-57` using the Route B single-joint-covariance CMI estimator:
  - `R_in` — `I( X_{t-L:t-1} ; M_t | E_{t-L:t} )`
  - `R_out` — `I( M_t ; X_{t+1:t+L} | X_t, E_t )`
  - `L_self = min( normalize(R_in), normalize(R_out) )`
  - `M_obs_t` remains the delay-embedded observable surrogate (`consciousness_metric_program.md:96-100`).  The bridge `M_obs_t → M_t` is still open and must be reported as an assumption. |
| Threshold / calibration rule | Each leg must pass its own null before the `min` gate is reported:
  - Class I (exogenous-only): `R_in ≈ 0` → `L_self = 0`.
  - Class II (passive tracker): `R_out ≈ 0` → `L_self = 0`.
  - Feed-forward / synchronized no-model: `L_self < 0.08` (Route B sandbox sanity bound).
  - Positive closed self-model loop: `L_self ≈ 0.595` (Route B population value), sample `0.529–0.595`.
  - Candidate pass/fail threshold: `θ_L = 0.08` against the construction set; a final held-out threshold must be frozen in the Route E pre-registration before the target dataset is inspected. |

**Recommendation:** keep as a core prerequisite, rename the code path to `R_in`, `R_out`, `L_self`, and deprecate `D_dir_proxy`.  Requires Route A (one versioned equation) and Route B (estimator repair) to land first.

---

### 2.3 Prerequisite 3 — Differentiation and coherence lifetime

*Statement in `consciousness.md`:* “The internal model manifold has effective rank above the trivial-loop threshold (`D_int`). The recurrent phase relations are stable enough to maintain a unified self-model over the relevant timescale (`C_coh`).”

| Criterion | Verdict |
|---|---|
| Currently implemented in the metric? | **Yes, but with overlap risk.** `D_int` is implemented in `cpf/differentiation.py:54` (PCA entropy of the delay-embedded covariance).  `C_coh_plv` and `C_coh_wpli` are implemented in `cpf/coherence.py:27` and `:58`. |
| Independent of the others? | **Mostly independent, but need a separation rule.** `D_int` measures effective rank / manifold complexity.  `C_coh` measures stable phase-lag structure.  They are conceptually distinct, but a common-mode oscillator can produce high `C_coh` and low `D_int`, and a high-rank noise process can produce high `D_int` and low `C_coh`.  The product `D_int * C_coh` is the intended separation rule: neither alone is sufficient. |
| Proposed operational measure | Keep the existing variables but make `C_coh_wpli` the primary coherence scalar and `C_coh_plv` a diagnostics-only scalar:
  - `D_int` from `cpf/differentiation.py:54`.
  - `C_coh_proxy` = `C_coh_wpli` from `cpf/coherence.py:58`. |
| Threshold / calibration rule | Use the existing null tests as initial sanity bounds, then calibrate on held-out data:
  - `D_int < 0.25` rejects the 1D thermostat null (`tests/test_nulls.py:45`); require `D_int > θ_D` with `θ_D ≥ 0.25` for a non-trivial manifold.
  - `C_coh_wpli < 0.1` for white noise and collapsed synchrony (`tests/test_nulls.py:18-19`, `:31`); require `C_coh_wpli > θ_C` with `θ_C ≥ 0.1` for phase-lag structure.
  - Final thresholds must be frozen in a pre-registration (Route E) before the held-out dataset is scored. |

**Recommendation:** keep as two independent components of the reduced prerequisite set, with a documented rule that `C_coh` alone must not dominate (seizure / synchrony suppression: high `C_coh`, low `D_int` → low composite).

---

### 2.4 Prerequisite 4 — Extended local substrate

*Statement in `consciousness.md`:* “A single isolated Hilbert space cannot be conscious. Consciousness requires a distributed substrate — tensor-product quantum system with finite-speed update, local coherence, and no-signaling entanglement between separated regions.”

| Criterion | Verdict |
|---|---|
| Currently implemented in the metric? | **No.** The Phase 0 metric processes EEG-like time series.  It has no variable that tests local Hilbert spaces, tensor-product structure, finite-speed update rules, or spacelike separation. |
| Independent of the others? | Conceptually independent, but **not testable** by the metric.  It belongs to a substrate-layer claim, not to the time-series structural-correlate instrument. |
| Proposed operational measure | **Remove from the metric-tested prerequisite set.**  If it is ever tested, it would require new instrumentation (e.g., spatially resolved quantum-substrate models, local-algebra tests, or causal-velocity bounds) that is outside the EEG metric. |
| Threshold / calibration rule | Not applicable.  Do not assign an EEG proxy to this prerequisite. |

**Recommendation:** remove as a metric-tested prerequisite.  It may remain as a speculative interpretive statement, but it cannot be operationalized by the current program.

---

### 2.5 Prerequisite 5 — Integrated self-information

*Statement in `consciousness.md`:* “The mutual information between the self-model modes and the sensory/processing modes exceeds the threshold above which the self-model is functionally autonomous from the immediate sensory stream.”

| Criterion | Verdict |
|---|---|
| Currently implemented in the metric? | **No.** There is no partition of the data into `M_t` (self-model) and `S_t` (sensory/processing) modes, and no conditional / directed / unique-information estimator.  `D_dir_proxy` treats all channels symmetrically; high cross-channel prediction gain can indicate dependence on a common driver, not autonomy. |
| Independent of the others? | **No — it overlaps with #2 and #3 without a separation rule.**  The self-model loop (`L_self`) already measures directed information between model and dynamics.  Raw mutual information with sensory modes can mean dependence as easily as autonomy; the stated threshold is not calibrated.  It is not independent of the loop / differentiation / coherence triad. |
| Proposed operational measure | **Remove from the metric-tested prerequisite set** as currently phrased.  If retained as a research target, it must be redefined as a *conditional* or *unique* information quantity with an explicit model/sensory partition:
  - Candidate new variable: `I_ms_unique` from partial information decomposition, or `I( M_t ; S_t | X_t, E_t )` if `M_t` and `S_t` can be identified.
  - Until the `M_obs_t → M_t` bridge closes and a mode partition is justified, this quantity cannot be computed from the current pipeline. |
| Threshold / calibration rule | None can be set because the variable is undefined.  If reintroduced later, the threshold must distinguish autonomy from common-driver confounding on held-out controls. |

**Recommendation:** remove as an independent metric-tested prerequisite.  The relevant autonomy idea is better captured by the bidirectional `L_self` gate (the model is not merely driven by sensory history) and by the `D_int` requirement (the model has non-trivial structure).

---

## 3. Reduced independent prerequisite set

The defensible, metric-testable structural-prerequisite set is:

| # | Prerequisite | Operational variable | Source file (current or proposed) | Role |
|---|---|---|---|---|
| 1 | **Differentiation of the internal manifold** | `D_int` | `cpf/differentiation.py:54` (`compute_pca_entropy`) | Suppresses trivial one-parameter / thermostat-like loops. |
| 2 | **Coherence lifetime of recurrent phase relations** | `C_coh_proxy` = `C_coh_wpli` (primary); `C_coh_plv` (diagnostic) | `cpf/coherence.py:58` (`compute_wpli`) | Measures stable, lag-aware phase structure; penalizes zero-lag common mode. |
| 3 | **Closed self-model feedback loop** | `R_in`, `R_out`, `L_self = min(R_in_norm, R_out_norm)` | New; spec in `consciousness_metric_program.md:40-57`; Route B prototype in `sandbox/consciousness_cmi_repair_probe.py` | Tests that an identified model is written by past state and causally shapes future state. |

The composite then becomes `C_PF = D_int * C_coh_proxy * L_self` (with `F_model` deferred; see note below).  This collapses the original five prerequisites into three independent, falsifiable conditions.

**Removed from the metric-tested set:**

- **Type 4 observer** — folded into the self-model loop (`L_self`).
- **Extended local substrate** — not testable by the EEG metric; requires an unsupported transfer from `minimum_substrate.md`.
- **Integrated self-information / autonomy** — cannot be computed without an identified `M_t`/sensory partition and a conditional/unique-information estimator; overlaps with the loop and differentiation tests.

**Note on `F_model`:** the full spec uses `F_self* = L_self * F_model` (`consciousness_metric_program.md:60-65`).  `F_model` (Fisher information of future trajectory with respect to `M_t`) is not implemented.  For the reduced prerequisite set, `F_model` is deferred; adding it would require a new variable and its own hostile controls.

---

## 4. Hard-problem boundary and what the metric can and cannot claim

This route, like the whole multi-angle repair, is a **structural-correlate instrument audit**, not a consciousness-detection result.

**What the reduced metric can claim:**

- It can test whether the three reduced structural prerequisites (`D_int`, `C_coh`, `L_self`) show a predicted pattern across neural/physiological states or synthetic controls.
- It can act as a candidate *structural-correlate* index, provided the hostile control battery, the pre-registration, and the `M_obs_t → M_t` bridge are addressed.
- It can be falsified: if the reduced prerequisites fail on known conscious-state data, or if negative controls systematically score high, the hypothesis is wrong.

**What it cannot claim:**

- It cannot detect, measure, prove, or falsify phenomenal consciousness.
- It cannot establish that the reduced prerequisites are necessary or sufficient for consciousness.
- It cannot classify any human, animal, AI, or quantum system as conscious or non-conscious.
- It does not cross the hard-problem boundary: the “something it is like” question remains outside the PF scope.

**Boundary preservation:**

- The `M_obs_t → M_t` bridge is still open (`consciousness_metric_program.md:159-177`).  Any score derived from delay-embedded data is an observable proxy, not a theorem-grade self-model.
- `PUBLIC HOLD` on Fundamentals remains in effect.
- No medical, clinical, welfare, AI personhood, public-release, or consciousness-classification claims are made.

---

## 5. Required transfer from `minimum_substrate.md` and whether it is defensible

`minimum_substrate.md` is a **canonical** definition of the physical Medium that supports PF observers.  It establishes that a single isolated Hilbert space cannot serve as the PF Medium because it lacks locality, causal order, propagation paths, and separated subsystems.  It does **not** establish sufficiency for consciousness.

To use `minimum_substrate.md` as a consciousness prerequisite, one would need a separate transfer argument:

> “The minimum substrate for PF observers is also a necessary substrate for consciousness.”

**This transfer is not defensible for the current metric:**

1. The metric data (EEG / band-power time series) do not encode local Hilbert-space structure, tensor-product factorization, finite-speed update rules, or spacelike separations.  It is therefore impossible to test the substrate claim from the score.
2. The phrase “a single isolated Hilbert space cannot be conscious” is not a well-formed empirical discriminator, as the Codex audit (F5) notes: a tensor product of local Hilbert spaces is itself a Hilbert space.  The relevant properties are *factorization*, *local observable algebras*, *interaction structure*, and *update dynamics* — none of which the Phase 0 metric measures.
3. `minimum_substrate.md` is silent on the hard problem and on the extra structures (self-model loop, differentiation, coherence lifetime) that `consciousness.md` adds.  It cannot carry those properties by itself.

**Conclusion:** the transfer from `minimum_substrate.md` to the consciousness metric is **not defensible** at this stage.  The extended-substrate prerequisite should be **removed from the metric-tested list**.  It may be retained only as an interpretive, non-metric statement about the kind of physical system that could host the reduced prerequisites, pending a separate derivation.

---

## 6. Synthesis and next-step dependencies

For the reduced prerequisite set to become production-ready, the following routes must land:

1. **Route A** — choose one versioned equation and one production path, deprecating `compute_cpf.py` vs. `compute_cpf_bands.py` and the `(1 + D_dir_proxy)` form.
2. **Route B** — replace `D_dir_proxy` with the `R_in`/`R_out`/`L_self` CMI estimator and add leg-specific null assertions.
3. **Route C** — run the hostile controls on the new `D_int * C_coh * L_self` composite and report false-positive rates.
4. **Route E** — freeze a real pre-registration with held-out data, thresholds, exclusions, and interpretation rules.

Only after those steps can the reduced three-prerequisite set be honestly described as a **candidate structural-correlate instrument**.  It still does not detect consciousness.

---

**Reduced prerequisite set (one-sentence form):** the defensible metric-tested set is `{ D_int, C_coh_proxy (wPLI-primary), L_self = min(R_in_norm, R_out_norm) }`, with the Type-4 observer label folded into `L_self`, the extended-substrate claim removed as untestable, and the raw integrated-self-information claim removed as unmeasured and overlapping.

---

*Report produced at `/mnt/d/Fundamentals/derivations/consciousness_metric_route_D_prerequisites.md`.*
