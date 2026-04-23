# F_self Null Theorem Target — No Endogenous Self-Model Loop

**Date**: 2026-04-15  
**Author**: Codex  
**Status**: Conditional theorem target  
**Builds on**:
- `consciousness_f_self_v2_spec_2026-04-15.md`
- `consciousness_fisher_metric_audit_2026-04-15.md`

---

## 1. Purpose

The first instinct was:

> if the system is feed-forward / acyclic, then \(F_{\text{self}}^{*}=0\)

That wording is too loose.

Why:

- any causal dynamical system becomes a DAG after time-unrolling,
- so DAG-ness alone does not distinguish recurrence from feed-forward processing,
- and a generic recurrent controller can still show nonzero loop information without being conscious.

The correct theorem target is narrower:

> \(F_{\text{self}}^{*}\) should vanish when there is **no endogenous self-model loop**.

---

## 2. Setup

On a window of length \(L\), define:

\[
Z_t=(X_t,M_t,E_t)
\]

with:

- \(X_t\): internal dynamical state,
- \(M_t\): candidate internal model state,
- \(E_t\): exogenous input.

Define the two loop legs:

\[
R_{\text{in}}(L) :=
I_{\mathrm{dir}}\!\big(X_{t-L:t-1}\to M_t \,\|\, E_{t-L:t}\big)
\]

\[
R_{\text{out}}(L) :=
I_{\mathrm{dir}}\!\big(M_t\to X_{t+1:t+L} \,\|\, X_t,E_t\big)
\]

and the loop gate:

\[
\mathcal L_{\text{self}}(L)
:=
\min(\widetilde R_{\text{in}}(L),\widetilde R_{\text{out}}(L)).
\]

Finally define:

\[
F_{\text{self}}^{*}(L)
:=
\mathcal L_{\text{self}}(L)\cdot \mathcal F_{\text{model}}(L).
\]

---

## 3. Exact Null Lemmas

### Lemma A — No inbound model update

If

\[
M_t \perp X_{t-L:t-1}\mid E_{t-L:t},
\]

then

\[
R_{\text{in}}(L)=0.
\]

**Reason:** directed information and conditional mutual information vanish under the relevant conditional-independence relation.

---

### Lemma B — No outbound model control

If

\[
X_{t+1:t+L} \perp M_t \mid X_t,E_t,
\]

then

\[
R_{\text{out}}(L)=0.
\]

**Reason:** once future internal evolution is conditionally independent of the candidate model state, the model contributes no directed information to future internal dynamics.

---

### Corollary — Broken loop implies zero self-reference gate

If either Lemma A or Lemma B holds, then

\[
\mathcal L_{\text{self}}(L)=0.
\]

Therefore

\[
F_{\text{self}}^{*}(L)=0.
\]

This is the exact mathematical core of the null target.

---

## 4. Structural Theorem Target

The next real theorem is not "all DAGs give zero."

It is:

> For the class of architectures with **no endogenous self-model loop**, every admissible candidate model variable \(M_t\) must satisfy either Lemma A or Lemma B.

If that structural statement is proved for a chosen architecture class, then the null theorem follows immediately.

---

## 5. Candidate Null Classes

The theorem should be attempted first on these restricted classes:

### Class 1 — Pure feed-forward mappings

No persistent internal state intended to represent the system's own future propagation.

Expected result:

- every candidate \(M_t\) fails the inbound or outbound leg,
- so \(\mathcal L_{\text{self}}=0\).

### Class 2 — Exogenous-only controllers

Internal control state depends only on external input and not on the system's own recent internal history.

Expected result:

- Lemma A null holds.

### Class 3 — Passive state trackers

Internal memory tracks past state but has no causal influence on future internal dynamics once \(X_t,E_t\) are fixed.

Expected result:

- Lemma B null holds.

---

## 6. What This Does Not Prove

This null theorem does **not** prove:

1. that nonzero \(\mathcal L_{\text{self}}\) implies consciousness,
2. that all recurrent systems with loop closure are conscious,
3. that thermostat-like loops should score zero.

That is deliberate.

The null theorem only separates:

- systems with no endogenous self-model loop
- from systems with at least one such loop candidate.

The richer consciousness discrimination still depends on:

- coherence gate \(\mathcal C_{\text{coh}}\),
- differentiation term \(\mathcal D_{\text{int}}\),
- and eventually a benchmark battery.

---

## 7. Executable Test Path

The theorem target should be paired with toy-model checks:

1. no-inbound model update => \(R_{\text{in}}\approx 0\)
2. no-outbound model control => \(R_{\text{out}}\approx 0\)
3. positive-control recurrent self-model => both legs \(>0\)

This is not proof, but it catches implementation drift before formal claims are made.

---

## 8. Final Codex Read

This is the right next proof target because it is:

- narrow,
- falsifiable,
- mathematically legible,
- and directly responsive to the hostile audit.

The wrong target was:

> prove consciousness from Fisher

The right target is:

> prove when the self-reference loop is absent, the self-reference metric must vanish.
