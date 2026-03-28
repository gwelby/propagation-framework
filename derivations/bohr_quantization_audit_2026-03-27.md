# Bohr Quantization Audit — 2026-03-27

**Audit ID**: HA-20260327-002
**Claim**: Axiom 3 -> Bohr-like Quantization
**Audit Class**: Theorem Audit
**Canonical Source Before Audit**: [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md), [coulomb_lens_ultimate.py](/mnt/d/fundamentals/sandbox/coulomb_lens_ultimate.py), [sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md)
**Status Before Audit**: `DERIVED 0.95`
**Auditor**: Codex
**Date**: 2026-03-27

---

## Exact Statement

The repo currently presents the claim as:

> Axiom 3 alone forces atomic quantization in the Coulomb field, yielding the Bohr-like spectrum `r_k = 2k^2`, `E_k = -1/(4k^2)`.

That statement is too strong.

The strongest statement that survives audit is:

> In the **circular eikonal Coulomb model**, if stable circular orbits satisfy the phase-closure rule `∮ n ds = 2πk`, then the allowed circular orbit radii and energies are `r_k = 2k^2`, `E_k = -1/(4k^2)`, i.e. a Bohr-like `1/k^2` spectrum.

---

## Allowed Inputs

- Axiom 1: matter mode propagates in a Coulomb field
- Axiom 3: stable mode requires phase closure
- Eikonal ray equations used in [coulomb_lens_ultimate.py](/mnt/d/fundamentals/sandbox/coulomb_lens_ultimate.py)
- Circular-orbit ansatz

Not allowed as hidden steps:

- exact validity of the eikonal / semiclassical approximation at atomic scale
- “Axiom 3 alone” wording that omits the Coulomb/eikonal model
- internal identity checks being treated as external experimental confirmation

---

## What Survives

### 1. The circular-orbit condition is mathematically recoverable

The script states the condition

`n^2(r0) = 1/(2r0)`

without proving it. But it does follow from the eikonal equations for a radial index profile.

Sketch:

- The script evolves
  - `dx/ds = p_x / n`
  - `dy/ds = p_y / n`
  - `dp/ds = ∇n`
- For a circular orbit of radius `r0`, the momentum is tangential with magnitude `|p| = n(r0)`.
- Along a circle, curvature is `1/r0`, so
  - `dp/ds = -(n/r0) r_hat`
- For a radial medium, `∇n = n'(r0) r_hat`
- Therefore circular balance requires
  - `n'(r0) = -n(r0)/r0`
- For `n(r) = sqrt(E + 1/r)`, this gives
  - `n'(r) = -1 / (2 n r^2)`
- Hence
  - `1 / (2 n r0^2) = n / r0`
  - so `n^2(r0) = 1 / (2r0)`

So the core circular-balance relation is valid in the script’s model.

### 2. The Bohr-like `1/k^2` spectrum follows inside that model

Using:

- circular balance: `n^2(r0) = 1/(2r0)`
- phase closure: `∮ n ds = n(r_k) 2π r_k = 2πk`

one gets:

- `n(r_k) r_k = k`
- `n^2(r_k) = 1/(2r_k)`

Combining them:

- `k^2 / r_k^2 = 1/(2r_k)`
- `r_k = 2k^2`
- `n(r_k) = 1/(2k)`

Then from `n^2 = E + 1/r`:

- `1/(4k^2) = E_k + 1/(2k^2)`
- `E_k = -1/(4k^2)`

So the algebraic model theorem holds.

### 3. The sandbox numerics are a good internal consistency check

The `0.0000%` values in [sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md#L291) show that the numerical orbit integration is consistent with the same formulas used to generate the circular orbit and closure target.

That is useful.

But it is an **internal identity check**, not an independent experimental test of hydrogen.

---

## Hidden Step / Break

### Break 1. “Axiom 3 alone” is false

The derivation uses:

- Axiom 1
- a Coulomb refractive model
- the eikonal equations
- the circular-orbit ansatz

So the repo wording “Axiom 3 alone” overstates the claim.

### Break 2. The model statement is inconsistent across files

[coulomb_lens_ultimate.py](/mnt/d/fundamentals/sandbox/coulomb_lens_ultimate.py#L394) uses:

- `n^2 = E + 1/r`

But [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md#L585) and [scale_stack_derivation_chain.md](/mnt/d/fundamentals/derivations/scale_stack_derivation_chain.md#L132) state:

- `n(r) = sqrt(1 + 1/(2r))`
- or `n^2(r) = 1 + 1/(2r)`

Those are not the same model.

That means the public derivation chain is not yet written in a single exact form.

### Break 3. The claim only covers circular semiclassical orbits

What is actually shown:

- circular orbit family
- principal `1/k^2` scaling

What is **not** shown:

- full hydrogen eigenproblem
- angular momentum quantum numbers `l, m`
- degeneracy structure
- transition amplitudes
- exact atomic-scale validity of the eikonal approximation

So the result is Bohr-like, not full atomic quantization.

### Break 4. The “0.0000% error” language is misleading

It sounds like a match to independent experiment.

What it really is:

- numerical confirmation that the script’s orbit integrator reproduces the same closure formulas used to define `r_k` and `E_k`

That is not fraud, but it is stronger-sounding than it should be.

---

## Required Closure

To restore a theorem-grade claim, the repo would need one of these:

### Option A — Honest model theorem

Rename the claim to something like:

> Circular Coulomb eikonal + phase closure yields a Bohr-like `1/k^2` spectrum.

This can be kept as a **conditional/model theorem**.

### Option B — Stronger physical theorem

Show that:

1. the eikonal / semiclassical model is derivable or valid at the atomic scale in PF
2. the Coulomb refractive model is the correct matter-wave medium for the electron
3. the phase-closure rule selects the physically relevant bound states beyond the circular subset

Only then should “atomic quantization from the axioms” be used without qualification.

---

## Sandbox Relation

This is a strong **model-support / internal-consistency** sandbox result.

It is not yet:

- a direct experimental confirmation
- or a full theorem of the axioms alone

---

## Verdict

**Recommended status**: `CONDITIONAL`

Reason:

- the circular-model derivation is real
- but it rests on named extra structure:
  - Coulomb eikonal model
  - circular-orbit ansatz
  - semiclassical validity at atomic scale

The current `DERIVED 0.95` status is too strong.

Recommended confidence:

- `0.82` as a conditional/model theorem

---

## Board Action

1. Demote the claim in [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) from `DERIVED` to `CONDITIONAL`.
2. Update [sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md) so the verdict reads as a model theorem, not an axiom-only closure.
3. Clean the teaching language in [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md) and [scale_stack_derivation_chain.md](/mnt/d/fundamentals/derivations/scale_stack_derivation_chain.md) to match the audited statement.

---

## One-Line Summary

The Bohr-like `1/k^2` result survives as a real circular-eikonal model theorem, but the repo currently overstates it as “Axiom 3 alone derives atomic quantization.” That stronger claim does not pass hostile audit.
