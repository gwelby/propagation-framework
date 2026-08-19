# Consciousness Metric Multi-Angle Repair — Scoping

**Status:** REPAIR SCOPING — NOT A CLAIM OF CONSCIOUSNESS DETECTION.  
**Authority tier:** advisory — instrument repair and boundary audit only.  
**Public hold:** PUBLIC HOLD on Fundamentals remains in effect. No promotion of `consciousness.md`, `consciousness_metric_program.md`, or the metric as detecting/measuring consciousness.

---

## 1. The question

The 2026-08-19 Codex hostile audit (`CODEX_20260819_FUNDAMENTALS_CONSCIOUSNESS_HYPOTHESIS_METRIC_AUDIT.md`) returned **HOLD / REVISE — NOT PROMOTION-READY** for the consciousness hypothesis and metric program. The audit identified ten required repairs and a clear boundary: the hard-problem boundary is well placed, but the instrument does not implement the documented self-model gate, the conditional-information estimator is broken, and the benchmark is not pre-registered.

The multi-angle repair question is:

> **What would it take to repair the C_PF metric program to a defensible *structural-correlate* instrument, and which repairs are feasible in the current PF substrate?**

This is not a claim that the resulting instrument detects consciousness. The word "consciousness" is kept as a candidate label only.

---

## 2. Honest starting state

From the audit and direct code inspection:

- **Two production entry points disagree:**
  - `compute_cpf.py` / `cpf/score.py`: `C_PF = D_int × C_coh × D_dir_proxy`
  - `compute_cpf_bands.py`: `C_PF = D_int × C_coh × (1 + D_dir_proxy)`
  - The spec in `consciousness_metric_program.md`: `C_PF = C_coh × D_int × L_self × F_model`, where `L_self = min(R_in, R_out)` with bidirectional conditional information.

- **No implementation contains the documented self-model variable `M_t` or the bidirectional conditional-information gate.** The current `D_dir_proxy` is a linear Granger prediction-gain proxy, not `L_self`.

- **The Class-I null masks a broken CMI estimator.** `R_out` is spuriously clipped to 1 because separate Ledoit-Wolf shrinkage targets break the algebraic identity `H(X|Y) = H(X,Y) − H(Y)`. An independent Gaussian residual check gives `0.0002 nats`; the code reports `0.2445 nats` and normalizes to `1.0`.

- **Hostile controls are missing.** The existing tests cover white noise, collapsed synchrony, and a thermostat. They do not cover:
  - acyclic temporal feed-forward chains,
  - synchronized no-model / no-loop systems,
  - time-shifted / phase-randomized surrogates,
  - common-driver / common-input confounds,
  - positive closed self-model loops.

- **Prerequisites are not operationalized.** `consciousness.md` lists five structural prerequisites. The metric does not implement items 4 (extended local substrate) or 5 (integrated self-information / autonomy threshold). Items 1 and 2 are redundant. No thresholds are calibrated.

- **"Pre-registered" is unsupported.** The protocol is an expectation table. Sample size `T=8000` and threshold `0.08` were selected during calibration, not locked before data inspection.

- **Incremental validity is untested.** No comparison against arousal, complexity, report, task, signal-quality, or perturbational-complexity baselines.

- **Lean formalization is narrow and correctly placed.** It can check conditional-independence null classes and gate algebra (`min(0,x)=0`), not the estimator, the empirical model variable, or the transfer to consciousness.

---

## 3. Repair transfer contract

A defensible structural-correlate instrument requires at least these transfer pieces:

| # | Transfer piece | What it means | Current state |
|---|----------------|---------------|---------------|
| T1 | One versioned equation + one production path | A single operational definition, one executable implementation, deprecated or versioned alternates | FAIL — three definitions, two entry points |
| T2 | Valid conditional-information estimator | Both `R_in` and `R_out` computed correctly; each leg passes its own null; no `min` masking | FAIL — `R_out` is broken and masked |
| T3 | Hostile control suite | A test battery that includes the known false-positive patterns and a positive self-loop control | FAIL — only 3 nulls, no feed-forward / sync / common-driver controls |
| T4 | Operationalized prerequisites | Remove redundant prerequisites, define thresholds, supply transfer for substrate/integrated-self-info or remove them from the metric-tested list | FAIL — 5 items not independently tested |
| T5 | Real pre-registration / held-out benchmark | Bind data, exclusions, estimators, thresholds, stats, interpretation, and a held-out replication set before looking at results | FAIL — calibration table, not pre-registration |
| T6 | Incremental validity vs baselines | Demonstrate added value over simpler arousal/complexity/report/task/PCI metrics on held-out data | NOT TESTED |
| T7 | Lean at the exact mathematical layer | Formalize generative nulls → conditional independence and gate algebra; do not claim consciousness | PARTIAL — null classes are provable in principle |

---

## 4. Multi-angle route map

| Route | Question | Owner | Expected output |
|---|---|---|---|
| A — Equation/implementation parity | Choose one versioned equation and one production path; document the gap between spec and code | Devin-RouteA | Route A repair probe: which implementation is closest, what deprecation/versioning is needed |
| B — CMI estimator repair | Repair the bidirectional conditional-information gate `L_self = min(R_in, R_out)`; make each leg pass its own null with analytic/reference checks | Devin-RouteB | Route B repair probe: working estimator design and remaining assumptions |
| C — Hostile controls | Add and run acyclic feed-forward, synchronized no-model, time-shifted, phase-randomized, common-driver, and positive self-loop controls; report false-positive rates | Devin-RouteC | Route C repair probe: control results and a minimum discriminating battery |
| D — Prerequisite operationalization | Distinguish and operationalize the five prerequisites; decide whether 4 and 5 stay, are removed, or get their own transfer | Devin-RouteD | Route D repair probe: reduced and operationalized prerequisite set |
| E — Pre-registration / incremental validity | Draft a real held-out protocol and list the comparators/baselines needed; do not calibrate to data | Devin-RouteE | Route E repair probe: pre-registration skeleton and comparator map |

---

## 5. Deliverables and sign-off

Each route will produce a short report file:

- `derivations/consciousness_metric_route_A_parity.md`
- `derivations/consciousness_metric_route_B_cmi.md`
- `derivations/consciousness_metric_route_C_controls.md`
- `derivations/consciousness_metric_route_D_prerequisites.md`
- `derivations/consciousness_metric_route_E_preregistration.md`

The synthesis will update this scoping doc's transfer contract and produce:

- A ranked repair order
- A **do not promote** boundary
- The next concrete step

No claim of consciousness detection, no canonical promotion, no PUBLIC HOLD lift.

---

## 6. Cross-route synthesis (2026-08-20)

All five route subagents completed. The results converge on one candidate v1.0 instrument.

### 6.1 Route verdicts

| Route | Question | Verdict | Key output |
|---|---|---|---|
| A | Equation/implementation parity | **PARITY FINDING + CORRECTED RECOMMENDATION** | `derivations/consciousness_metric_route_A_parity.md` — `compute_cpf_bands.py`'s `(1 + D_dir_proxy)` factor is structurally broken; `cpf/score.py` has the correct multiplicative shape. **However, `D_dir_proxy` was falsified by Route C (25–40% FPR) and Route B, so v1.0 must use `L_self`, not `D_dir_proxy`.** |
| B | CMI estimator repair | **REPAIR FOUND** | `derivations/consciousness_metric_route_B_cmi.md` + `sandbox/consciousness_cmi_repair_probe.py` — single-joint-covariance Ledoit-Wolf CMI correctly gates `L_self` to 0 on Class I/II/feed-forward/synchrony and opens to ~0.6 on a positive closed self-model loop |
| C | Hostile controls | **REPAIRED (PARTIAL)** | `derivations/consciousness_metric_route_C_controls.md` + `sandbox/test_consciousness_hostile_controls.py` — new `C_PF_lself_wpli` gives FPR 12.5% and discrimination gap −0.0106 vs legacy 25.0% FPR / −0.1275 gap; only `common_driver_confound` remains false-positive because no exogenous `E_t` is observed |
| D | Prerequisite operationalization | **REDUCE SET** | `derivations/consciousness_metric_route_D_prerequisites.md` — reduce to `{D_int, C_coh_wpli, L_self}`; remove Type-4 observer (fold into L_self), extended substrate, and integrated self-information |
| E | Pre-registration/incremental validity | **DESIGN-ONLY** | `derivations/consciousness_metric_route_E_preregistration.md` — full pre-registration skeleton with Track A (current pipeline) and Track B ( awaits validated `L_self`) |

### 6.2 Convergent candidate instrument

All five routes point to the same reduced instrument:

```
C_PF^v1.0 = D_int × C_coh_wpli × L_self
```

where

- `D_int` = PCA entropy of delay-embedded manifold (from `cpf/differentiation.py`)
- `C_coh_wpli` = weighted phase-lag index (from `cpf/coherence.py`)
- `L_self = min(R_in_norm, R_out_norm)` with `R_in`/`R_out` estimated by the single-joint-covariance CMI repair from Route B.

This is **not** the spec's `C_PF = C_coh × D_int × L_self × F_model` because `F_model` is not yet implemented and may not be needed for a structural-correlate instrument. The `M_obs_t → M_t` bridge remains open.

### 6.3 What is now closed

- **T1 implementation parity:** Route A identifies the exact path to one versioned equation and one production entry point.
- **T2 CMI estimator:** Route B provides the canonical single-joint-covariance `L_self` design with population-analytic checks. The GLM Devin `Guard 2` residual-variance patch in `sandbox/consciousness_metric_null_class_test.py` is a symptom patch and is archived/superseded; the root-cause fix is in `sandbox/consciousness_cmi_repair_probe.py`.
- **T3 hostile controls:** Route C battery run with new `L_self` in `cpf/score.py`. New composite `C_PF_lself_wpli` improves FPR from 25.0% to 12.5% and discrimination gap from −0.1275 to −0.0106; only `common_driver_confound` still false-positives.
- **T4 prerequisite operationalization:** Route D reduces the set to three independent, testable components.
- **T5 pre-registration:** Route E provides the design; it is ready to be frozen once `L_self` is integrated.
- **T7 Lean gate algebra:** Route B's analytic null checks and the `min(0, x) = 0` gate are mathematically exact for the constructed linear-Gaussian systems.

### 6.4 What remains open

- **Exogenous-channel proxy for EEG:** the only remaining hostile false positive (`common_driver_confound`) requires conditioning on an observed `E_t`; no general EEG proxy exists yet.
- **Full hostile-control validation:** the common-driver confound must be added to the battery with explicit `E_t` channels.
- **Threshold calibration:** `θ_L` and the final `C_PF` pass/fail threshold must be set on a construction set and frozen before target data inspection.
- **Held-out dataset and incremental validity:** the Route E pre-registration is design-only; real data and comparators are pending.
- **F_model and M_obs_t → M_t bridge:** not addressed; keep as open assumptions.
- **T6 incremental validity:** design only, no data.

### 6.5 Honest boundary

- The repaired `L_self` is a **candidate structural-correlate instrument**, not a consciousness detector.
- The hard-problem boundary remains intact.
- `PUBLIC HOLD` on Fundamentals is not lifted.
- No medical, clinical, welfare, human/animal/AI/quantum classification, public, release, or Greg authority is moved.

### 6.6 Next concrete steps

1. **Design an exogenous-channel proxy for EEG** (or add explicit `E_t` channels to the battery) to collapse the remaining `common_driver_confound` false positive.
2. **Verify confound removal:** run the battery with explicit `model_channels` and `exog_channels` per control.
3. **Update Route E pre-registration:** freeze `C_PF_lself_wpli` thresholds and the held-out split.
4. **Return for Codex re-audit** with exact hashes.

