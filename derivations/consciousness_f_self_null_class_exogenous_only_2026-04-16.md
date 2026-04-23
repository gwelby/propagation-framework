# F_self Null Class I — Exogenous-Only Controllers

**Date**: 2026-04-16  
**Author**: Codex  
**Status**: Restricted null-class derivation note  
**Builds on**:
- `consciousness_f_self_v2_spec_2026-04-15.md`
- `consciousness_f_self_null_theorem_target_2026-04-15.md`

---

## 1. Scope

This note proves the easiest restricted null class for the `F_self` v2 program:

> if the candidate model state is driven only by exogenous input and not by the system's own recent internal history, then the self-reference loop gate vanishes.

This is not the full null theorem.
It is the first closed subclass.

---

## 2. Setup

On a window of length \(L\), let:

\[
Z_t=(X_t,M_t,E_t)
\]

with the inbound loop leg defined as:

\[
R_{\mathrm{in}}(L):=
I_{\mathrm{dir}}\!\big(X_{t-L:t-1}\to M_t \,\|\, E_{t-L:t}\big).
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

Assume the architecture is **exogenous-only** in the following sense:

\[
M_t = f(E_{t-L:t}, U_t)
\]

for some measurable function \(f\) and exogenous noise \(U_t\) independent of
\(X_{t-L:t-1}\) conditional on \(E_{t-L:t}\).

Equivalently:

\[
M_t \perp X_{t-L:t-1}\mid E_{t-L:t}.
\]

This says:

- the candidate model state may be adaptive,
- it may be memoryful with respect to the environment,
- but it is **not** updated by the system's own recent internal history.

So it is not an endogenous self-model in the PF sense.

---

## 4. Proposition

Under the exogenous-only assumption,

\[
R_{\mathrm{in}}(L)=0.
\]

### Proof

By the conditional-independence assumption,

\[
P\!\big(M_t \mid X_{t-L:t-1}, E_{t-L:t}\big)
=
P\!\big(M_t \mid E_{t-L:t}\big).
\]

Directed information from \(X_{t-L:t-1}\) into \(M_t\) conditioned on
\(E_{t-L:t}\) reduces to a conditional mutual-information term over the same sigma-algebra.

But conditional mutual information vanishes exactly when the conditional distribution is unchanged by the source variable.

Therefore:

\[
I_{\mathrm{dir}}\!\big(X_{t-L:t-1}\to M_t \,\|\, E_{t-L:t}\big)=0.
\]

Hence:

\[
R_{\mathrm{in}}(L)=0.
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

because the self-reference loop is already broken at the inbound leg.

---

## 6. Interpretation

This is exactly the kind of architecture the hostile audit said must be separated from genuine self-reference:

- the system may have internal state,
- the state may respond to the environment,
- the controller may be sophisticated,
- but if the candidate model state does not incorporate the system's own recent internal history, the PF self-reference gate must read zero.

So this class is a real null.

---

## 7. What This Does Not Show

This note does **not** show:

1. that every feed-forward architecture is exogenous-only,
2. that every non-conscious system falls into this class,
3. that nonzero loop gate implies consciousness.

It proves only one restricted class:

> exogenous-only candidate model states do not satisfy the PF self-reference loop.

That is enough to count as real progress.

---

## 8. Sandbox Alignment

The corresponding toy-model check is the `exogenous_only_controller` case in:

`sandbox/f_self_null_toy_models.py`

That harness shows the expected numerical pattern:

- \(R_{\mathrm{in}} \approx 0\)
- loop gate \(\approx 0\)

The sandbox is not the proof.
It is the sanity check that the toy implementation matches the theorem target.

---

## Final Codex Read

This is the first real formula closure in the `F_self` lane after the hostile audit.

It is narrow.
It is honest.
And it is the correct kind of narrow.
