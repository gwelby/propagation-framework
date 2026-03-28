# QCD Confinement Audit — 2026-03-27

**Audit ID**: HA-20260327-006
**Claim**: QCD Confinement from `λ_c`
**Audit Class**: Theorem Audit
**Canonical Source Before Audit**: [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md), [qcd_confinement_pf.md](/mnt/d/fundamentals/derivations/qcd_confinement_pf.md)
**Status Before Audit**: `DERIVED 0.85`
**Auditor**: Codex
**Date**: 2026-03-27

---

## Exact Statement

The repo currently presents the claim as:

> The confinement radius is derived from `λ_c` by QCD RG running, so no third fundamental coherence scale is required. The current `2.2 fm -> 0.9 fm` mismatch is just the standard 1-loop QCD error.

That statement is too strong.

The strongest statement that survives audit is:

> If one takes `λ_c` as the UV matter coherence scale and uses empirical QCD running from that scale, then the confinement radius is plausibly a **dynamically generated RG scale**, not a third independent PF coherence ceiling. The mechanism is structurally sound, but the current local chain is not a theorem from Axioms 1–3 and does not yet justify the stronger “known higher loops fix it” language.

---

## Allowed Inputs

- `λ_c` as the matter coherence ceiling used by the current PF scale stack
- Standard QCD running-coupling formulae
- Empirical UV input `α_s(λ_c)`
- The PF interpretation that confinement is an emergent medium response scale rather than a new fundamental ceiling

Not allowed as hidden steps:

- treating calibrated `λ_c` as a theorem of the axioms
- treating empirical `α_s(λ_c)` as a PF derivation
- claiming theorem-grade closure from a 1-loop estimate with factor-2.5 error
- asserting that 2-loop or threshold matching “fixes it” without showing the calculation locally
- treating the string-tension coefficient or full SU(3) dynamics as already derived from PF

---

## What Survives

### 1. The structural RG mechanism is real

[qcd_confinement_pf.md](/mnt/d/fundamentals/derivations/qcd_confinement_pf.md#L122) correctly identifies the basic scale-generation mechanism:

`r_conf = λ_c exp(2π / (b_0 α_s(λ_c)))`

That is the standard QCD statement that an infrared confinement scale can be generated exponentially from a shorter UV scale and a weak UV coupling.

Inside the current PF language, that supports a real structural claim:

> confinement need not be a third fundamental coherence ceiling if it can be generated dynamically from the matter ceiling plus QCD running.

That part survives.

### 2. The “no third fundamental scale” interpretation is plausible

[qcd_confinement_pf.md](/mnt/d/fundamentals/derivations/qcd_confinement_pf.md#L159) makes the right conceptual distinction:

- `l_P`: geometry coherence ceiling
- `λ_c`: matter coherence ceiling
- `r_conf`: dynamically generated trapping scale

That is a good framework distinction. It is not yet fully closed, but it is coherent and worth keeping.

### 3. The claim is already weaker in its own source note

The derivation note itself is materially more honest than the board:

- [qcd_confinement_pf.md](/mnt/d/fundamentals/derivations/qcd_confinement_pf.md#L6) says `ARGUED WITH NUMBERS`
- [qcd_confinement_pf.md](/mnt/d/fundamentals/derivations/qcd_confinement_pf.md#L33) gives confidence `0.72`

So the main problem is not that the idea is empty. The main problem is that the public status outran the source note.

---

## Hidden Step / Break

### Break 1. This is not derived from Axioms 1–3 alone

The current chain depends on:

- calibrated / externally anchored `λ_c`
- empirical `α_s(λ_c)`
- standard SU(3) beta-function input

So the claim is not “derived from the axioms” in the same sense as a topology or Casimir result.

At best it is:

> PF-scale interpretation + QCD RG mechanism + empirical UV boundary data.

That is useful, but it is not theorem-grade closure.

### Break 2. The 1-loop mismatch is too large for `DERIVED`

The headline number is:

- predicted `r_conf ≈ 2.2 fm`
- observed `r_conf ≈ 0.9 fm`

That is a factor `~2.5` miss. A mechanism can survive that kind of miss as an argued bridge. It does not survive it as a closed derivation.

### Break 3. The repo overstates the higher-loop rescue

The current board language says the factor-2.5 miss is “the known 1-loop QCD error” and that higher-loop corrections fix it.

The local repo does not actually show that.

Direct audit check using the standard 2-loop formula with the same UV boundary values gives:

- `Λ_QCD^(1-loop) ≈ 0.0882 GeV`, so `r_conf^(1-loop) ≈ 2.237 fm`
- `Λ_QCD^(2-loop) ≈ 0.5276 GeV`, so `r_conf^(2-loop) ≈ 0.374 fm`

So a naive 2-loop evaluation from the same top-scale boundary overshoots in the opposite direction rather than landing cleanly on `0.9 fm`.

This does **not** prove the mechanism is wrong. It does prove the stronger local slogan

> “factor 2.5 = standard 1-loop error, higher loops fix it”

is not established by the current repo.

### Break 4. The precise nonperturbative coefficient is not derived

[qcd_confinement_pf.md](/mnt/d/fundamentals/derivations/qcd_confinement_pf.md#L112) already admits the string-tension coefficient and full SU(3) group structure are not derived from PF.

That matters, because confinement is not just the existence of an RG-generated scale. It is also the actual nonperturbative dynamics at that scale.

So the current note identifies the right scale-generation mechanism, but not the full quantitative confinement theorem.

---

## Required Closure

To restore a stronger claim, the repo would need one of these:

### Option A — Honest argued bridge

Keep the claim as:

> QCD confinement is plausibly a dynamically generated infrared scale from `λ_c`, not a third PF coherence ceiling.

This supports `ARGUED`, not `DERIVED`.

### Option B — Stronger quantitative closure

Show all of the following locally:

1. a clean PF status for `λ_c` independent of calibration
2. a threshold-aware 2-loop or better QCD running calculation from the same UV boundary
3. a justified match from the perturbative running scale to the physical confinement radius / string tension
4. an honest account of what is imported from standard SU(3) gauge theory versus what PF itself adds

Only then would a theorem-grade or high-confidence conditional claim be justified.

---

## Sandbox Relation

This is not primarily a sandbox claim.

It is a **derivation-board / interpretation** claim that uses standard QCD running plus PF scale language.

So the risk is not “calculator pretending to be experiment.” The risk is:

- a structurally good bridge being promoted to theorem status before the quantitative chain is actually closed.

---

## Verdict

**Recommended status**: `ARGUED`

Reason:

- the RG mechanism survives
- the “no third coherence scale” interpretation plausibly survives
- but the theorem-grade wording does not
- and the current local repo does not justify the stronger 2-loop rescue language

Recommended confidence:

- `0.72`

This matches the source derivation note more closely than the current board.

---

## Board Action

1. Demote [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) from `DERIVED 0.85` to `ARGUED 0.72`.
2. Update [scale_stack_derivation_chain.md](/mnt/d/fundamentals/derivations/scale_stack_derivation_chain.md) so the matter-to-nuclear link is not presented as fully derived.
3. Update [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md) so the student/master summaries do not overclaim the QCD result.
4. Update [FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md) and any one-page outputs to the weaker status.

---

## Strongest Honest Statement After Audit

> PF has a plausible and mathematically recognizable mechanism by which the QCD confinement scale is generated from the matter coherence scale `λ_c` through RG amplification. That mechanism supports the claim that confinement need not introduce a third fundamental coherence ceiling. But the current repo does not yet have a theorem-grade or quantitatively closed derivation of the physical confinement radius from Axioms 1–3.
