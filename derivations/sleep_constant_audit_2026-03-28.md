# 8-Hour Sleep Constant Audit — 2026-03-28

**Audit ID**: HA-20260328-009
**Claim**: 8h Sleep Constant
**Audit Class**: Theorem Audit
**Canonical Sources Before Audit**:
- [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md)
- [RESEARCH/sleep_consolidation_ratio/MASTER.md](/mnt/d/fundamentals/RESEARCH/sleep_consolidation_ratio/MASTER.md)
- [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md)
- [sandbox/sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md)
**Status Before Audit**: `DERIVED 0.92`
**Auditor**: Codex
**Date**: 2026-03-28

---

## Exact Statement

The live board currently presents the claim as:

> PF derives the human 8-hour sleep requirement from the `(2,1)` topological weight partition, so that `2/3` of a 24-hour cycle is wake and `1/3` is sleep.

That statement is too strong.

The strongest statement that survives audit is:

> PF strongly supports the need for an offline consolidation / recovery phase in coherence-maintaining systems, and the T-010 two-mode model gives a plausible `~2/3` active fraction under specific weighting and efficiency assumptions. But the exact human “8 hours” claim is not derived from Axioms 1–3 alone.

---

## Allowed Inputs

- Axiom 3: coherence requires periodic reconciliation / reset in overloaded systems
- the `(2,1)` topological weight pattern, to the extent already established
- ordinary modeling assumptions for two-mode encode/recover systems
- empirical sleep literature as support, not as axiomatic proof

Not allowed as hidden steps:

- treating the wake/sleep mapping as identical to fermion/boson topology
- using unresolved T2 / T3 structure as if it were already closed
- treating a sandbox model with built-in asymmetry as theorem-grade derivation
- treating a human 24-hour circadian cycle as a universal topological consequence

---

## What Survives

### 1. Sleep-like consolidation is strongly supported

[RESEARCH/sleep_consolidation_ratio/pass_02_deepdive.md](/mnt/d/fundamentals/RESEARCH/sleep_consolidation_ratio/pass_02_deepdive.md#L71) gives a reasonable axiomatic story:

- finite-speed online encoding accumulates unresolved phase lag
- coherence requires offline reconciliation
- replay / reset is therefore functionally necessary

That broad structural claim survives well.

### 2. A nonzero recovery fraction is plausible in PF-style models

[RESEARCH/sleep_consolidation_ratio/MASTER.md](/mnt/d/fundamentals/RESEARCH/sleep_consolidation_ratio/MASTER.md#L11) and the surrounding literature summary support the idea that high-capacity systems need active consolidation rather than pure continuous online operation.

That is useful and worth keeping.

### 3. The sandbox gives model support, not theorem closure

[sandbox/sleep_coherence_net.py](/mnt/d/fundamentals/sandbox/sleep_coherence_net.py#L5) and [sandbox/sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md#L370) show that a specific oscillator-fatigue model can prefer a wake ratio near `2/3`.

That supports the **T-010 model family**.
It does not derive the biological constant from the PF axioms.

---

## Hidden Step / Break

### Break 1. The core research master explicitly depends on `N = 3`

[RESEARCH/sleep_consolidation_ratio/MASTER.md](/mnt/d/fundamentals/RESEARCH/sleep_consolidation_ratio/MASTER.md#L27) writes

`Q_sleep = (1·3)/9 = 1/3`

and [RESEARCH/sleep_consolidation_ratio/pass_02_deepdive.md](/mnt/d/fundamentals/RESEARCH/sleep_consolidation_ratio/pass_02_deepdive.md#L18) states

`N = 3 generations of processing`

So the sleep ratio inherits the same denominator / generation structure that was just demoted in the T2 / T3 audit.

This claim cannot honestly remain stronger than [three_generations_t2_audit_2026-03-28.md](/mnt/d/fundamentals/derivations/three_generations_t2_audit_2026-03-28.md#L206).

### Break 2. The wake/sleep mapping is analogical, not derived

[UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md#L526) maps:

- wake -> fermionic / encoding mode
- sleep -> bosonic / consolidation mode

That is a plausible interpretation.
It is not a theorem of Axioms 1–3.

The bridge from particle-spectrum topology to biological duty cycle is exactly the kind of cross-scale move that needs extra care, not extra confidence.

### Break 3. The sandbox script hardcodes the asymmetry it later “finds”

[sandbox/sleep_coherence_net.py](/mnt/d/fundamentals/sandbox/sleep_coherence_net.py#L23) sets:

- wake coupling `K = 2.0`
- sleep coupling `K = 1.0`

and [sandbox/sleep_coherence_net.py](/mnt/d/fundamentals/sandbox/sleep_coherence_net.py#L43) makes sleep dissipate fatigue at **2x** the wake accumulation rate.

So the scan is not discovering the `(2,1)` asymmetry from the axioms.
It is testing a model that already contains that asymmetry.

That is fine for a sandbox experiment.
It is not theorem closure.

### Break 4. The empirical literature does not support an exact universal 8h constant

[RESEARCH/sleep_consolidation_ratio/pass_01_survey.md](/mnt/d/fundamentals/RESEARCH/sleep_consolidation_ratio/pass_01_survey.md#L393) itself scores:

- “Optimal sleep duration ~7h” at `0.85`
- “1:2 sleep-wake ratio optimal” at only `0.70`

and [RESEARCH/sleep_consolidation_ratio/pass_01_survey.md](/mnt/d/fundamentals/RESEARCH/sleep_consolidation_ratio/pass_01_survey.md#L205) explicitly says:

> No study directly optimizes sleep-wake ratio for information processing throughput.

So the empirical side supports the importance of sleep and consolidation.
It does not close an exact human 8h theorem.

### Break 5. The 24-hour conversion is species- and environment-dependent

Even if a model favored a `1/3` recovery fraction, the move

`1/3 of 24 hours = 8 hours`

still assumes:

1. a human-scale 24h circadian environment
2. a specific monophasic interpretation
3. a direct identification of “recovery fraction” with “sleep duration”

That is already beyond the bare PF axioms.

---

## Required Closure

To restore a stronger claim, the repo would need one of these:

### Option A — Honest model-theorem framing

Rename the claim conceptually to:

> In a PF-inspired two-mode encode/recover model with `(2,1)` weighting and specified recovery efficiency, the preferred active fraction is near `2/3`.

That supports **conditional / model-level** status.

### Option B — Biological bridge theorem

Derive all of the following:

1. why wake/sleep modes are the correct biological realization of the PF topological split
2. why the relevant system has exactly the weighting used in T-010
3. why the recovery fraction should be exactly `1/3`
4. why that fraction converts cleanly into a human 24-hour sleep requirement

Without those, “8 hours” stays too strong.

---

## Verdict

**Recommended status**: `ARGUED`

Reason:

- the need for offline reconciliation survives strongly
- the T-010 model survives as a useful heuristic / sandbox model
- the exact human 8-hour constant does not survive as an axiomatic theorem

**Recommended confidence**: `0.72`

The current `DERIVED 0.92` board row is too strong.

---

## Board Action

1. Update [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) from `DERIVED 0.92` to `ARGUED 0.72`.
2. Update [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md), [AGENTS.md](/mnt/d/fundamentals/AGENTS.md), [FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md), and [scale_stack_derivation_chain.md](/mnt/d/fundamentals/derivations/scale_stack_derivation_chain.md) so the sleep result is no longer presented as closed.
3. Reframe the sandbox line as support for the T-010 model under explicit recovery-efficiency assumptions.

---

## Strongest Honest Statement After Audit

> PF strongly supports the general need for offline consolidation in coherence-maintaining systems, and its current T-010 model suggests that a `~2/3` active fraction can be stability-favoring under specific assumptions. But the exact claim that the human sleep requirement is *derived* as 8 hours from PF topology alone does not survive hostile audit.
