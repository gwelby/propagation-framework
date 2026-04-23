# F_self v2 — Coherence Proxy Audit (PLV vs wPLI)

**Date**: 2026-04-18  
**Author**: Codex  
**Status**: Hostile audit / calibration note  
**Builds on**:
- `consciousness_f_self_v2_spec_2026-04-15.md`
- `consciousness_f_self_mt_operationalization_audit_2026-04-16.md`
- `sandbox/f_self_null_toy_models.py`

---

## 1. The Question

The live proxy chain is now:

\[
C_{PF}^{proxy} = L_{self}^{proxy} \cdot D_{int}^{proxy} \cdot C_{coh}^{proxy}
\]

The weakest factor is still the coherence term.

The candidate on the table was:

> `C_coh_proxy = mean PLV across observable-channel pairs`

The right audit question is not whether PLV is a real statistic.
It is.

The real question is:

> Does PLV reward the kind of coherence PF wants, or does it over-reward trivial/common-mode synchrony?

---

## 2. What PLV Actually Measures

Phase-Locking Value (PLV):

\[
PLV_{jk} = \left|\left\langle e^{i(\phi_j - \phi_k)} \right\rangle\right|
\in [0,1].
\]

PLV is high whenever the phase difference between two signals is stable.
That includes:
- meaningful recurrent phase-locking,
- externally imposed synchrony,
- and zero-lag common-mode collapse.

So PLV is a **broad synchrony statistic**, not a specific self-model coherence object.

This is not a bug in PLV.
It is a scope issue.

---

## 3. Comparison Proxy: wPLI

Weighted Phase Lag Index (wPLI) uses the imaginary part of the cross-spectrum:

\[
wPLI = \frac{\left|\mathbb E\left[ |\Im(S_{xy})|\,\mathrm{sign}(\Im(S_{xy})) \right]\right|}{\mathbb E\left[|\Im(S_{xy})|\right]}.
\]

What that buys:
- near-zero-lag coupling is strongly suppressed,
- common-source / volume-conduction style synchrony is suppressed,
- genuinely lagged directional coupling can survive.

So wPLI is not a replacement for PLV in every context.
It is a **lag-aware guardrail** against zero-lag inflation.

---

## 4. Sandbox Result

Toy comparison on the current four-channel sandbox plus one added lagged-loop positive control:

| Model | PLV mean | wPLI mean | Codex read |
|------|---------:|----------:|------------|
| exogenous-only controller | 0.4676 | 0.0064 | PLV sees broad correlation; wPLI correctly says no meaningful lagged coupling |
| passive state tracker | 0.7187 | 0.0102 | same issue: PLV high, wPLI near zero |
| positive loop (current zero-lag toy) | 0.7515 | 0.0101 | PLV high, but mostly zero-lag/shared synchrony |
| collapsed sync | 0.9974 | 0.0045 | this is the critical failure mode for raw PLV |
| lagged loop | 0.1448 | 0.2963 | wPLI finally lights up where lagged structure is real |

This is the decisive pattern.

---

## 5. What Survives

### 5.1 PLV survives as a broad coherence proxy

PLV is still useful when the question is:
- how phase-locked are these channels,
- how stable is the pairwise phase relationship,
- how synchronized is the observable state.

So PLV can remain in the sandbox.

### 5.2 PLV fails as a standalone PF coherence gate

Raw PLV by itself is too permissive for the PF lane.

Why:
- it gives the collapsed synchrony toy an almost perfect coherence score,
- it does not distinguish phase-locked collapse from meaningful lagged organization,
- and it rewards exactly the seizure/common-mode failure mode we are trying to suppress.

That means:

> `C_coh_proxy = PLV mean` is too strong as a standalone choice.

### 5.3 wPLI survives as the right comparison guardrail

wPLI is valuable precisely because it kills the easy false positive.

It does **not** mean PF coherence must equal wPLI.
It means any usable coherence gate should at least be tested against the wPLI contrast.

---

## 6. Recommendation

Use a two-proxy coherence panel for now:

- `C_coh_plv_proxy`
- `C_coh_wpli_proxy`

and keep the full proxy score explicit rather than hidden:

- `C_PF_plv_proxy = L_self_proxy * D_int_proxy * C_coh_plv_proxy`
- `C_PF_wpli_proxy = L_self_proxy * D_int_proxy * C_coh_wpli_proxy`

Why this is the right next step:
- it preserves information instead of collapsing too early,
- it makes the zero-lag inflation problem visible,
- and it tells us what kind of coherence the benchmark battery is actually rewarding.

Do **not** compress these into one final coherence scalar yet.

---

## 7. Final Codex Read

PLV is not wrong.
It is just too generous.

wPLI is not the final answer either.
It is a necessary hostile comparison because it punishes the exact failure mode PLV over-rewards.

So the honest status is:

| Item | Status |
|------|--------|
| PLV as broad synchrony proxy | KEEP |
| PLV as standalone PF coherence gate | REJECT |
| wPLI as lag-aware comparison proxy | KEEP |
| Final PF coherence object | OPEN |

That is the right place to stand tonight.
