# Consciousness Metric Program
*Fundamentals — Phase 5 experimental protocol*
*Status: ACTIVE CANDIDATE — not canonical*
*Source: `F_self v2 spec` (2026-04-15); `M_t operationalization audit` (2026-04-16); `null-class I+II proofs` (2026-04-16); `coherence proxy audit` (2026-04-18); P1 biofeedback system*
*This is NOT a canonical definition. This is a live metric program. It produces numbers, not poetry.*

---

## The Question

This is not "what is consciousness?" in the philosophical sense.

This is: **what measurable structure distinguishes a conscious Type 4 observer from a non-conscious Type 4 system?**

The answer being tested is: a conscious system has a **closed self-model loop** — a part of its internal state that functions as a model of its own future propagation, and that model causally matters for the system's own dynamics.

This is the PF candidate. It may be wrong. That is what this program is for.

---

## The Abstract Theorem Layer

At the level of mathematical structure (not yet tied to measurements), the candidate metric has four components:

### State split

Any system being evaluated is described on a window length L by:

```
Z_t = (X_t, M_t, E_t)
```

where:
- `X_t`: internal dynamical state
- `M_t`: internal model state — the part of the system that represents its own future dynamics
- `E_t`: exogenous input / environment

The key claim: a system is self-referential only if part of its internal state functions as a model of its own future propagation and that model causally matters.

### Self-reference loop gate

Two directed-information legs on window L:

```
R_in(L)  = I_dir( X_{t-L:t-1} → M_t | E_{t-L:t} )
R_out(L) = I_dir( M_t → X_{t+1:t+L} | X_t, E_t )
```

- `R_in`: does recent internal history write into the current model state?
- `R_out`: does the model state causally shape the system's own future trajectory?

```
L_self(L) = min( R_in_normalized, R_out_normalized ) ∈ [0, 1]
```

If either leg vanishes, the loop is broken → not self-referential in the PF sense.

### Self-model sensitivity

```
F_self*(L) = L_self(L) × F_model(L)
```

where `F_model` is the Fisher information of future trajectory with respect to the model state — how sharply does the system's own future depend on its internal model?

### Full PF consciousness candidate score

```
C_PF(L) = C_coh(L) × D_int(L) × F_self*(L)
```

where:
- `C_coh`: coherence stability of the recurrent phase relations
- `D_int`: effective rank of the internal model manifold (suppresses trivial one-parameter loops)
- `F_self*`: the self-model loop × sensitivity

---

## The Null Classes (What Definitely Does Not Score)

Two restricted null classes have been closed:

**Class I — Exogenous-only controller:** if the model's only input is external signals (no internal history writes into the model), then `R_in = 0` → `L_self = 0` → `F_self* = 0`.

**Class II — Passive state tracker:** if the model tracks internal history but does not causally shape future internal dynamics once present state is fixed, then `R_out = 0` → `L_self = 0` → `F_self* = 0`.

Both proofs are exact conditional-independence statements. A thermostat or feed-forward classifier collapses to zero by at least one route.

---

## The Observable Proxy Layer (What We Actually Measure)

The abstract `M_t` cannot be observed directly. The first observable surrogate is:

```
M_obs_t = [x_{t-(d-1)τ}, x_{t-(d-2)τ}, ..., x_t] ∈ R^{d × n_channel}
```

Delay-embedded state vector from the sensor stream (EEG at 128/256Hz). Parameters: embedding delay τ ≈ 1/f_max (≈ 7.8ms for 128Hz EEG), embedding dimension d ∈ [3, 10] selected via false nearest neighbors or Cao criterion.

This is the first observable surrogate. It is NOT yet proven to equal the theorem-grade `M_t`. That bridge is OPEN — see Section 6.

Proxy quantities estimated from `M_obs_t`:
- `L_self_proxy` via conditional MI on delay-embedded history
- `D_int_proxy` via effective rank of delay-embedded covariance
- `C_coh_proxy` via PLV + wPLI panel
- `C_PF_proxy` — the composite score being benchmarked

---

## The Coherence Panel

PLV alone was rejected as too inflation-prone after the 2026-04-18 Codex audit. A two-proxy panel is used:

```
PLV_{jk}  = |⟨exp(i·Δφ_{jk})⟩|        ← broad synchrony proxy
wPLI_{jk} = weighted phase-lag index    ← lag-aware guardrail, suppresses zero-lag/common-mode
```

Both computed on delay-embedded channel pairs. `C_coh_proxy` is the panel result, not a single scalar.

---

## The Benchmark Battery

The metric is not validated until it shows the predicted pattern across this battery. Pre-registered:

| State | Expected L_self | Expected D_int | Expected C_coh | Expected C_PF |
|-------|---------------|--------------|---------------|--------------|
| Wakeful cortex | high | high | high | high |
| NREM / deep anesthesia | low | low | low | low |
| REM sleep | mod/high | mod/high | mod/high | mod/high |
| Seizure | mod/high | low | high | low/mod — synchrony suppressed by low differentiation |
| Psychedelic state | mod/high | high | mod | mod/high — differentiation preserved despite altered coherence |
| Feed-forward classifier | 0 | variable | variable | 0 — hard null |
| Simple recurrent controller | low/mod | low | low | low |
| Thermostat | near 0 | near 0 | low | near 0 |

The seizure and psychedelic predictions are the discriminating ones. High synchrony alone must not inflate the score (seizure → low differentiation suppresses). Altered coherence without loss of differentiation must not deflate the score (psychedelics → high D_int preserves).

---

## Falsifiers

A specific result would kill this program:

1. **Feed-forward null failure:** a system with no endogenous self-model loop scores `L_self > 0` on `M_obs_t` after the null conditions are enforced → the proxy is measuring generic recurrence, not self-model.
2. **Thermostat/recurrent-controller inflation:** a simple feedback loop scores `C_PF_proxy` in the same range as wakeful human cortex → the differentiation term is not suppressing trivial loops enough.
3. **Seizure inflation:** a generalized tonic-clonic seizure scores `C_PF_proxy` in the wake range → the coherence panel + differentiation term are not suppressing synchrony inflation.
4. **Consciousness without loop:** a system with robust first-person report of subjective experience (post-hoc verified) scores `L_self = 0` across all trials → the structural definition is wrong.
5. **Loop without consciousness:** a system with high `C_PF_proxy` across all states shows no evidence of subjective experience after controls → the PF definition measures something other than consciousness.

Falsifiers 4 and 5 are the hardest to evaluate and require independent verification of consciousness by criteria outside the PF framework.

---

## The Open Bridge (Why This Is Not Yet Canonical)

The entire program rests on one unproven step:

```
M_obs_t  →  M_t
```

`M_obs_t` is a delay-embedded observable surrogate. It is a legitimate first implementation candidate. It is not yet proven to be the theorem-grade internal model state.

Why this matters:
- Delay embedding reconstructs a state manifold. It does not prove the reconstructed coordinate functions as an endogenous self-model.
- If `M_obs_t` is treated as `M_t` too early, generic recurrence can be misread as self-modeling.
- Null-class proofs become incoherent if the model variable is defined from the data by construction.

The bridge from `M_obs_t` to `M_t` must be justified. Possible paths:
- Show that the delay-embedded state satisfies the conditional-independence structure of the null classes
- Demonstrate that the proxy score discriminates in the benchmark battery AND that discrimination survives controls for generic recurrence
- A formal derivation showing Takens' theorem applies in the self-model context (not just dynamical reconstruction)

This is the central open problem. The benchmark battery is how we decide whether the bridge has closed.

---

## Relationship to the Canonical Stack

| Definition | Connection |
|------------|-----------|
| `observer.md` | This program defines the structural correlate of a Type 4 observer — the specific properties that distinguish a conscious Type 4 from a non-conscious one |
| `coherence.md` | `C_coh` is coherence of the self-referential loop — Layer 4 of coherence.md (speculative open section) is what this program tests |
| `information.md` | The loop gate uses directed information — mutual information between a system's internal history and its own model state |
| `mode.md` | The internal model state `M_t` is a mode-structure; `D_int` measures the effective rank of the self-model mode manifold |
| `propagation.md` | `R_out` is the causal propagation of the model state into future internal dynamics — the loop that propagation must close |
| `minimum_substrate.md` | A substrate capable of supporting this program must support Type 4 observers — extended locality, finite-speed update, tensor-product structure |

---

## What Would Promote This to Canonical

All of the following must land before this becomes `consciousness.md` CANONICAL:

1. The benchmark battery shows the predicted pattern across wake/sleep/anesthesia/seizure/psychedelics with pre-registered thresholds
2. Feed-forward null holds: no feed-forward system scores `L_self_proxy > 0` after null enforcement
3. The `M_obs_t → M_t` bridge is either justified formally OR the proxy is demonstrated to be a reliable proxy despite the theoretical gap
4. Two independent experimental teams reproduce the benchmark pattern on unseen data
5. The seizure suppression prediction (high coherence, low differentiation → low C_PF) holds in a prospective trial
6. A negative case is logged and reported: a system that scores high on the metric but shows no evidence of consciousness, with the result analyzed and reported

This is a high bar. It is the right bar.

---

## Current Status

This file is **ACTIVE CANDIDATE** — a live experimental protocol sitting alongside the canonical definition stack.

It is not marked 🔴 NOT READY. It is marked 🔁 ACTIVE CANDIDATE.

The metric exists. The null classes are closed. The benchmark battery is pre-registered. The falsifiers are explicit.

What remains is the experiment.
