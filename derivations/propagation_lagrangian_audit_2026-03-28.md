# Propagation Lagrangian Audit — 2026-03-28

**Audit ID**: HA-20260328-007
**Claim**: Propagation Lagrangian
**Audit Class**: Theorem Audit
**Canonical Source Before Audit**: [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md), [propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md)
**Status Before Audit**: `DERIVED 0.72`
**Auditor**: Codex
**Date**: 2026-03-28

---

## Exact Statement

The live board currently presents the claim as:

> `ℒ_prop = ½(∂χ)² − V(χ) + λχT` is derived from Axioms 1–3 and maps to Brans-Dicke scalar-tensor gravity in the linearized limit.

That statement is too strong as written.

The strongest statement that survives audit is:

> Axioms 1–3 strongly motivate a **scalar-tensor effective field theory class** for the propagation medium. Within that class,  
> `ℒ_prop = ½(∂χ)² − V(χ) + λχT` is a clean **minimal scalar ansatz** whose Euler-Lagrange equation and linearized Brans-Dicke mapping are mathematically correct.  
> But the scalar field assumption, the specific coupling branch `λχT`, and the form of `V(χ)` are not uniquely forced by the axioms alone.

---

## Allowed Inputs

- Axiom 1: propagation is fundamental
- Axiom 2: finite causal velocity and isotropy
- Axiom 3: stability requires a coherence-supporting mechanism
- Standard effective-field-theory reasoning at lowest order
- Standard scalar-tensor / Brans-Dicke comparison machinery

Not allowed as hidden steps:

- treating the scalar-field choice as identical to the axioms
- treating “minimal lowest-order ansatz” as “uniquely derived”
- treating the Brans-Dicke map as proof that the PF picked the only correct Lagrangian
- treating the Euler-Lagrange equation of the chosen ansatz as proof that the ansatz itself is axiomatically forced

---

## What Survives

### 1. The scalar-tensor EFT direction is well motivated

[propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L48) is already honest that the scalar field is a **working assumption**, not an axiom.

That matters, but it does not kill the whole program.

What does survive is:

> if the propagation medium admits a long-wavelength scalar effective description, then the axioms strongly push toward a scalar-tensor EFT family with a causal kinetic term, a coherence-supporting potential, and matter coupling.

That is a real result.

### 2. The kinetic term is solid once the scalar branch is chosen

[propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L81) gives the standard lowest-order hyperbolic kinetic term

`½(∂χ)^2`

and that is defensible.

Once one accepts a scalar low-energy field, Axiom 2 plus Lorentz/local EFT structure really does point there.

### 3. The Euler-Lagrange calculation is correct

[propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L168) correctly derives

`□χ + V'(χ) = λT`

from the chosen Lagrangian.

There is no issue there.

### 4. The Brans-Dicke connection is structurally real

[propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L357) does support a meaningful linearized scalar-tensor comparison.

The honest surviving statement is:

> the PF ansatz lives in the scalar-tensor / Brans-Dicke neighborhood.

That is useful and should be kept.

---

## Hidden Step / Break

### Break 1. The scalar field is a branch choice, not an axiom-level consequence

[propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L48) explicitly says:

> “Working assumption (not an axiom): the medium supports a long-wavelength effective description in terms of a scalar field `χ`.”

That is already enough to block the strongest board wording “derived from Axioms 1–3” if taken literally.

The scalar branch is plausible.
It is not identical to the axioms.

### Break 2. The coupling `λχT` is motivated, not uniquely forced

The weakest part of the chain is in [propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L122):

- scalar coupling to matter
- linear in `χ`
- linear in `T`

This is a good **minimal scalar-tensor choice**.
It is not a unique theorem of the axioms.

The file itself gives only `0.70` confidence for the coupling form at [line 139](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L139).

That is not theorem-grade closure.

### Break 3. The potential is only specified at the class level

[propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L111) openly says the specific form of `V(χ)` is not uniquely determined.

Again, this is honest and acceptable for an EFT note.

But it means the current board row should not present a single fully derived Lagrangian as if the axioms singled it out exactly.

### Break 4. “Derived Lagrangian” and “derived field theory family” are being conflated

The document’s actual content is closer to:

- scalar EFT family identified
- minimal ansatz selected by simplicity / lowest order / scalar-tensor analogy
- standard consequences computed from that ansatz

That is valuable.

But it is not the same as:

> Axioms 1–3 uniquely derive `ℒ_prop = ½(∂χ)^2 − V(χ) + λχT`.

### Break 5. The variable-`c` consequence is explicitly weaker

[propagation_lagrangian.md](/mnt/d/fundamentals/derivations/propagation_lagrangian.md#L289) already gives only `0.65` confidence to

`c_local = 1 / sqrt(1 + λχ)`

and calls it argued rather than forced.

That reinforces the same general conclusion:

the file is stronger as a disciplined EFT note than as an axiomatic theorem.

---

## Required Closure

To restore a stronger claim, the repo would need one of these:

### Option A — Honest EFT-family claim

Rename the row conceptually to:

> Axioms 1–3 motivate a scalar-tensor effective field theory class; `ℒ_prop` is the minimal scalar representative.

This supports a **conditional / model-theorem** status.

### Option B — Stronger uniqueness theorem

Show all of the following:

1. why the long-wavelength medium variable must be scalar rather than scalar-plus-vector or a more general multiplet
2. why the matter coupling must be `χT` rather than another allowed lowest-order scalar coupling
3. why the effective potential must fall into a uniquely selected class

Without those, the exact single-ansatz wording is too strong.

---

## Verdict

**Recommended status**: `CONDITIONAL`

Reason:

- the scalar-tensor EFT direction survives strongly
- the minimal ansatz survives as a disciplined branch choice
- the exact single Lagrangian does not survive as uniquely derived from the axioms alone

Recommended confidence:

- `0.72`

So the confidence can stay roughly where it is.
The status should not.

---

## Board Action

1. Update [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) from `DERIVED 0.72` to `CONDITIONAL 0.72`, with wording narrowed to the scalar-tensor EFT family plus minimal ansatz.
2. Update [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md) so the Propagation Lagrangian row is no longer presented as a fully derived theorem.
3. Keep the Brans-Dicke map, but describe it as the nearest established parent theory rather than proof of uniqueness.

---

## Strongest Honest Statement After Audit

> The Propagation Framework strongly supports a scalar-tensor effective field theory description of the medium. Within that family, `ℒ_prop = ½(∂χ)² − V(χ) + λχT` is a coherent minimal ansatz whose field equation and Brans-Dicke correspondence are mathematically sound. But the present axioms do not uniquely force that exact Lagrangian without the added scalar-medium assumption and lowest-order EFT selection rules.
