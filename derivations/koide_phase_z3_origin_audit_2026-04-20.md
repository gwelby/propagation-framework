# Koide Phase: Z3-Origin Audit

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Audit the upstream question behind the matrix lane:

> does the current PF repo actually derive the `Z_3` structure used in the Koide phase discussion,
> or is the matrix lane only a rewrite of a `Z_3` already built into the Koide parametrization?

---

## 1. Short answer

The repo does derive a **real abstract `Z_3` orbit** in the internal generation-walk models.

It does **not** yet derive a **charged-lepton `Z_3` phase representation** strong enough to close
the Koide phase selector.

So the matrix lane is neither full closure nor pure nonsense:

- it is **not invented from nowhere**
- but it is **not yet PF-native enough** to count as a derivation of the charged-lepton phase law

That is the honest middle.

---

## 2. What PF really does derive

### 2.1 Exact abstract cycle

`phase_closure_exact_model.md` gives an exact lifted orbit

`Z_6`

with observable quotient

`Z_6 / Z_2 ~= Z_3`.

This is not metaphor. It is an explicit model choice with:

- lifted six-step orbit
- observable three-step quotient orbit
- exact cyclic closure

So PF does own a genuine abstract three-cycle structure.

### 2.2 Exact quotient characters

The earlier audit
[path_a_z6_z3_chirality_intertwiner_audit_2026-04-05.md](/mnt/d/Fundamentals/derivations/path_a_z6_z3_chirality_intertwiner_audit_2026-04-05.md)
states the key representation-theoretic fact:

the observable quotient keeps exactly the three characters

`1, omega, omega^2`

with `omega = exp(2*pi*i/3)`.

This matters because the minimal matrix lane

`U(delta) = exp(i delta) * diag(1, omega, omega^2)`

uses exactly that quotient character set.

So the matrix lane is not numerology. It is aligned with an actual abstract character structure
already present in the repo.

### 2.3 Exact 120-degree amplitude geometry

Separately, the Koide amplitude side already has a clean threefold geometry:

- three equal-strength resonances
- 120-degree spacing
- equilateral triangle / `Q = 2/3`

So the repo also owns a real threefold amplitude geometry.

---

## 3. What PF does not derive

### 3.1 No canonical orientation on the cycle

The same `Z_6 -> Z_3` audit already proved:

- the quotient cycle has no preferred generator
- `omega` and `omega^2` are not split by the bare lift
- the lift gives cycle existence, not orientation selection

This is load-bearing.

The minimal matrix lane needs not just the abstract character set, but a concrete ordered phase
structure

`diag(1, omega, omega^2)`.

The current repo does not yet derive why that ordering is physically selected in the charged-lepton
sector rather than its inverse or another equivalent basis.

### 3.2 No charged-lepton bridge

The repo does not currently contain a theorem object of the form

`charged-lepton square-root mass triple -> canonical Z_3 phase matrix / character basis`.

That is the actual bridge Claude is asking for.

The current matrix lane starts from an abstract phase matrix carrying the correct `Z_3` characters.
It does **not** yet show why the charged-lepton mass triple should be represented by that object.

### 3.3 One internal source is circular for this purpose

`g1_model_specification_brief.md` contains language such as:

- "the three fixed 120° intervals forced by the equiangular Koide construction"
- "the three 120° nodes of the Koide triangle"

That may be useful as heuristic model language, but it cannot be used as an *independent* origin
for the Koide `Z_3` structure.

If the goal is to derive the Koide phase law, one cannot cite "the Koide triangle" as the source of
the very `Z_3` one is trying to explain.

So for this audit:

> any G1 argument that takes the Koide triangle as primitive does not count as an upstream PF
> derivation of the Koide `Z_3` structure.

### 3.4 T1 physical realization is still not closed

Even the broader generation/topology lane is not fully closed.

The T1 audit still keeps physical realization at `PARTIAL DERIVATION 0.85`, because the Axiom 3
population / selector bridge remains open.

So the repo does not yet have full theorem-grade control even over the physical realization of the
three-branch structure, let alone over its charged-lepton phase representation.

---

## 4. Result for the matrix lane

This is the right way to read the current matrix construction:

### What survives

- PF does derive an abstract quotient character set `1, omega, omega^2`
- an abstract `3 x 3` phase matrix built from those characters is mathematically natural
- that matrix gives exact `cos(9 delta)` through the trace-class construction

### What does not survive

- PF has not yet derived that the charged-lepton Koide triple is canonically carried by that matrix
- PF has not yet derived a preferred orientation / generator on the quotient cycle
- PF has not yet derived the selector principle acting on the trace algebra

So the matrix lane is best described as:

> a mathematically clean realization of the **abstract quotient character structure** already
> present in PF, but not yet a PF-native derivation of the **charged-lepton Koide phase**.

---

## 5. Clean verdict on Claude's push

Claude's reordering is correct.

The real priority is:

1. **charged-lepton -> Z_3 bridge**
2. **PF-native phase-matrix theorem**
3. **selector principle on that object**

The tolerance-region pass is downstream of that.

Until step 1 exists, the matrix lane is structurally informative but not decisive.

---

## 6. Strongest honest statement

The current repo supports the following statement and no stronger one:

> PF contains a genuine abstract `Z_3` orbit and its quotient character set
> `1, omega, omega^2`. This is enough to make the minimal matrix lane mathematically natural.
> But the repo does not yet derive the charged-lepton mass triple as a canonical realization of that
> `Z_3` character structure, nor a preferred orientation on the cycle, nor the selector principle
> that would turn the matrix lane into a phase derivation.

That is the load-bearing state.

---

## 7. Next bounded move

The next honest bounded question is now very specific:

> is there any PF theorem object already in the repo that maps the charged-lepton square-root mass
> triple into the quotient-character basis `1, omega, omega^2` without importing the Koide
> parametrization itself?

If yes, the matrix lane becomes materially stronger.

If no, that absence should be recorded as the current frontier rather than blurred by selector
language.
