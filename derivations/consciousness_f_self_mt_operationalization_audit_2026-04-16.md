# F_self v2 — M_t Operationalization Audit

**Date**: 2026-04-16  
**Author**: Codex  
**Status**: Hostile audit / calibration note  
**Builds on**:
- `consciousness_f_self_v2_spec_2026-04-15.md`
- `consciousness_f_self_mt_operationalization_2026-04-16.md`
- `consciousness_f_self_null_theorem_target_2026-04-15.md`

---

## 1. What Survives

The delay-embedding proposal survives in a narrower form.

What is real:
- delay embedding is a valid **observable surrogate candidate** for the hidden state of a dynamical system,
- it is cheap, deterministic, and compatible with the existing P1 data stream,
- it gives a plausible first coordinate system for differentiation and coherence proxies,
- and it is a reasonable first benchmark object.

That is enough to keep it.

---

## 2. What Fails If Stated Too Strongly

The note overstates one critical step:

> delay-embedded observable history is **the** internal model state `M_t`.

That identification is too strong.

### Break 1 — Conflict with Null Class I

The null-class theorem for exogenous-only controllers says that a candidate model state may satisfy:

\[
M_t \perp X_{t-L:t-1} \mid E_{t-L:t}.
\]

But if `M_t` is *defined* as a delay embedding of the observable internal trace, then it is built from recent internal history by construction.

So the Class I null can no longer be represented except in degenerate cases.

That means the current operationalization cannot be identified with the theorem object without breaking the null program.

### Break 2 — Takens Gives a State Reconstruction, Not a Self-Model Variable

Delay embedding can reconstruct a state manifold under suitable assumptions.
It does **not** prove that the reconstructed coordinate is the part of the system functioning as an endogenous self-model.

It may instead represent:
- generic recurrent state,
- generic memory,
- or a mixed state that carries no special self-model role.

So it is a good observable reconstruction, but not yet the exact PF `M_t` by theorem.

### Break 3 — Proxy Inflation Risk

If the delay-embedded observable is treated as the theorem object too early, then:
- generic recurrence can be misread as self-modeling,
- null-class proofs become incoherent,
- and benchmark success would look stronger than it really is.

That is the exact failure mode the hostile audit is supposed to block.

---

## 3. The Correct Split

Use two layers.

### 3.1 Abstract theorem object

\[
M_t
\]

This remains the **theorem-grade internal model state** appearing in the v2 spec and the null-class derivations.

### 3.2 Observable surrogate

\[
\widehat M_t^{\mathrm{obs}}
\]

This is the **delay-embedded observable surrogate** built from sensor history.

It is legitimate to estimate proxy quantities from this surrogate:

- \(L_{\mathrm{self}}^{\mathrm{proxy}}\)
- \(D_{\mathrm{int}}^{\mathrm{proxy}}\)
- \(C_{\mathrm{coh}}^{\mathrm{proxy}}\)
- \(C_{\mathrm{PF}}^{\mathrm{proxy}}\)

But those are still proxy quantities until the bridge from
\(\widehat M_t^{\mathrm{obs}}\) to theorem-grade \(M_t\) is justified.

---

## 4. Operational Consequence

The right workflow is now:

1. keep the null-class derivations stated at the abstract `M_t` level,
2. keep the delay-embedding note as the first **observable surrogate** for implementation,
3. label sandbox and benchmark quantities as proxies when they use observable surrogates,
4. do not promote the delay-embedding choice as a theorem closure.

This is narrower, but it is honest.

---

## 5. Coherence Gate Read

The PLV proposal is acceptable as a **first coherence proxy candidate**.

It does not yet deserve theorem status.

What survives:
- PLV is a real, standard synchronization statistic,
- it can separate fragmented versus phase-locked recurrent structure,
- it is easy to compute on delay embeddings or channel stacks.

What remains open:
- whether PLV is the right PF coherence object,
- whether it suppresses seizure-like synchrony strongly enough when combined with differentiation,
- and whether a recurrence-specific coherence object would do better.

So the right label is:

> `C_coh_proxy`, not final `C_coh`.

---

## 6. Status Table

| Item | Status | Codex read |
|------|--------|------------|
| Abstract `M_t` in theorem notes | KEEP | Correct level of abstraction |
| Delay-embedded state as direct identity with `M_t` | REJECT | Too strong |
| Delay-embedded state as `M_obs_t` / observable surrogate | KEEP | Right first implementation choice |
| PLV as final PF coherence gate | OPEN | Candidate only |
| PLV as coherence proxy | KEEP | Good enough for sandbox / benchmark pass |

---

## Final Codex Read

The useful move here is not to throw out the delay-embedding work.
It is to **bound it correctly**.

The delay-embedded state is a real implementation bridge.
It is not yet the theorem object.

That distinction keeps the null theorem coherent and keeps the benchmark lane honest.
