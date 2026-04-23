# F_self Null Class II — Passive State Trackers

**Date**: 2026-04-16  
**Author**: Codex  
**Status**: Restricted null-class derivation note  
**Builds on**:
- `consciousness_f_self_v2_spec_2026-04-15.md`
- `consciousness_f_self_null_theorem_target_2026-04-15.md`

---

## 1. Scope

This note proves the second restricted null class for the `F_self` v2 program:

> if the candidate model state tracks internal history but does not causally shape the system's own future internal dynamics once the present state and environment are fixed, then the self-reference loop gate vanishes.

This is not the full null theorem.
It closes the outbound-broken subclass.

---

## 2. Setup

On a window of length \(L\), let:

\[
Z_t=(X_t,M_t,E_t)
\]

with the outbound loop leg defined as:

\[
R_{\mathrm{out}}(L):=
I_{\mathrm{dir}}\!\big(M_t\to X_{t+1:t+L} \,\|\, X_t,E_t\big).
\]

The v2 loop gate is:

\[
\mathcal L_{\mathrm{self}}(L)=
\min\!\big(\widetilde R_{\mathrm{in}}(L),\widetilde R_{\mathrm{out}}(L)\big).
\]

And:

\[
F_{\mathrm{self}}^{*}(L)=
\mathcal L_{\mathrm{self}}(L)\cdot \mathcal F_{\mathrm{model}}(L).
\]

---

## 3. Null-Class Assumption

Assume the architecture is a **passive state tracker** in the following sense:

\[
M_t = g(X_{t-L:t-1}, E_{t-L:t}, U_t)
\]

for some measurable function \(g\), but the future internal trajectory is conditionally independent of \(M_t\) once the present internal state and environment are fixed:

\[
X_{t+1:t+L} \perp M_t \mid X_t,E_t.
\]

This says:

- the candidate model state may summarize past internal dynamics,
- it may retain useful memory,
- but it does **not** act back on the future propagation of the system once the live state is given.

So it is a tracker, not an endogenous self-model loop.

---

## 4. Proposition

Under the passive-tracker assumption,

\[
R_{\mathrm{out}}(L)=0.
\]

### Proof

By assumption,

\[
P\!\big(X_{t+1:t+L}\mid M_t,X_t,E_t\big)
=
P\!\big(X_{t+1:t+L}\mid X_t,E_t\big).
\]

Directed information from \(M_t\) into the future internal trajectory conditioned on \((X_t,E_t)\) reduces to the corresponding conditional mutual-information content over the same sigma-algebra.

But conditional mutual information vanishes exactly when conditioning on the source variable does not change the conditional law of the target.

Therefore:

\[
I_{\mathrm{dir}}\!\big(M_t\to X_{t+1:t+L} \,\|\, X_t,E_t\big)=0.
\]

Hence:

\[
R_{\mathrm{out}}(L)=0.
\]

\(\square\)

---

## 5. Corollary

Since:

\[
\mathcal L_{\mathrm{self}}(L)=
\min(\widetilde R_{\mathrm{in}}(L),\widetilde R_{\mathrm{out}}(L)),
\]

we immediately get:

\[
\mathcal L_{\mathrm{self}}(L)=0.
\]

Therefore:

\[
F_{\mathrm{self}}^{*}(L)=0.
\]

This holds regardless of the value of:

- \(\mathcal F_{\mathrm{model}}\),
- \(\mathcal C_{\mathrm{coh}}\),
- or \(\mathcal D_{\mathrm{int}}\),

because the self-reference loop is already broken at the outbound leg.

---

## 6. Interpretation

This closes the second null class demanded by the hostile audit:

- the system may remember its own past,
- it may build a compact internal tracker,
- but if that tracker does not causally matter for future internal evolution once present state is fixed, then PF should not count it as self-referential.

So mere internal memory is not enough.
The model must close a loop.

---

## 7. What This Does Not Show

This note does **not** show:

1. that every memory system is a passive tracker,
2. that every unconscious system falls into this class,
3. that nonzero loop gate implies consciousness.

It proves only one restricted class:

> passive internal trackers do not satisfy the PF self-reference loop when their state has no outbound causal role.

That is the correct level of claim.

---

## 8. Sandbox Alignment

The corresponding toy-model check is the `passive_state_tracker` case in:

`sandbox/f_self_null_toy_models.py`

That harness shows the expected numerical pattern:

- \(R_{\mathrm{out}} \approx 0\)
- loop gate \(\approx 0\)

Again: the sandbox is not the proof.
It is the implementation sanity check.

---

## Final Codex Read

Class II now closes as cleanly as Class I.

That matters because the null theorem is no longer a slogan.
It is becoming a union of exact restricted subclasses.
