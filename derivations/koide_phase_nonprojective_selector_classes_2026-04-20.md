# Koide Phase: Non-Projective Selector Classes

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Map the live search space after the projective lane has been fenced by
[koide_projective_mobius_lemma_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_projective_mobius_lemma_2026-04-20.md).

---

## 1. What changed

The projective pass closed one class of search:

- canonical slope `tan(delta)`
- edge ratios of the square-root mass triple
- any affine/projective coordinate on the Koide line

These are all the same one-dimensional object up to Möbius transformation.

So the next live question is stricter:

> if a selector exists, what **non-projective** mathematical object could sit upstream of the
> observed Koide phase?

This note classifies the candidate classes.

---

## 2. Required properties of any serious candidate

A usable selector class has to do more than merely rename the problem.

It must satisfy all of:

1. **Upstream rational label**  
   There must be a naturally rational parameter before any angle is introduced.

2. **Non-projective content**  
   It cannot be just a Möbius transform of `tan(delta)` or an equivalent slope coordinate.

3. **Trigonometric embedding path**  
   There must be a clear map from the rational label to the Koide cosine parametrization.

4. **Selection, not allowance**  
   The class must explain why the chosen value is selected, not just why it is algebraically
   permitted.

5. **Charged-lepton relevance**  
   It must have a plausible route to the charged-lepton square-root mass triple specifically, not
   only to an abstract phase variable.

If one of these is missing, the class is analogy, not closure.

---

## 3. Candidate class A — Rotation numbers / winding labels

### Form

Rational rotation numbers of the form

`rho = p/q`

arise naturally in circle dynamics and maps on `R/Z`.

### Strength

- exact rational label upstream of the angle
- mathematically clean
- directly supports Rivero's statement that the rational may belong to a reduced quantity rather
  than to the literal angle

### Weakness

- the physical angle is recovered only after a `2*pi*rho`-type embedding
- so this class does **not** explain a bare rational literal angle
- more importantly, there is currently no natural map from the charged-lepton Koide geometry to a
  rotation-number dynamical system

### Verdict

Useful as a **conceptual analogy**, not currently a live derivation route.

---

## 4. Candidate class B — Conformal weights / topological spins

### Form

Representation-theoretic labels such as

`h in Q`

occur naturally in conformal field theory and modular tensor categories.

The physical phase is then typically

`exp(2*pi*i*h)`.

### Strength

- exact rational labels are native to the theory
- this is the cleanest known mathematical class where a rational sits upstream of a phase
- unlike the projective lane, this is genuinely non-projective

### Weakness

- the standard phase is still `2*pi*h`, not `h`
- so the class explains rational **labels**, not bare rational geometric angles
- the missing bridge is severe: the repo does not currently identify the Koide `delta` with a
  conformal weight, topological spin, or any equivalent representation-theoretic label
- the earlier WZW lane did not close the selector problem

### Verdict

This is the **strongest external mathematical class** currently visible, but still only as a
candidate loophole class, not a derived mechanism.

---

## 5. Candidate class C — Modular / level-k representation data

### Form

Affine and modular theories often produce rational labels from level data, Casimir ratios, and
representation combinatorics.

### Strength

- exact rational values arise naturally
- close in spirit to earlier WZW audits
- can generate finite discrete allowed values rather than a continuum

### Weakness

- by itself this class usually produces a discrete **menu**, not a selector for one specific
  charged-lepton phase
- unless tied to a specific representation-theoretic map, it just moves the problem:
  “why this level / representation?”
- the repo already has experience here: a k-based story can fit the target without deriving the
  selector principle

### Verdict

Potentially useful only if coupled to a genuine independent selection rule. On its own, too easy to
turn into post-hoc matching.

---

## 6. Candidate class D — Trace / character variables

### Form

Instead of treating `delta` itself as fundamental, treat observables like

- `cos(delta)`
- `cos(3 delta)`
- `trace U(delta)`

as the true invariants.

### Strength

- much closer to the actual Koide parametrization, which is already written in cosine form
- naturally non-projective
- can convert the question from “which angle?” to “which trace value?”
- compatible with group/representation viewpoints without requiring the angle itself to be primary

### Weakness

- by itself, this still does not select a rational value
- current local audits already show that the natural nonlinear composite

  `f(delta) = -1/2 + cos(3 delta)/sqrt(2)`

  does not automatically produce `cos(9 delta)` dominance
- without a new nonlinear or representation-theoretic ingredient, trace variables remain a
  reformulation, not a selector

### Verdict

This is the **cleanest bridge class** between abstract mathematics and the actual Koide formula,
but it still needs a real selector mechanism.

---

## 7. Candidate class E — Nonlinear 3-cycle composite observables

### Form

Composite objects built from the entire three-step Koide / PF cycle, such as:

- determinant-like products
- cubic 3-cycle observables
- effective actions whose Fourier content lives in the `cos(3n delta)` tower

### Strength

- this is the most direct route to `n=3` / `9 delta` structure
- genuinely non-projective
- already aligned with both sides of the bridge:
  - PF gives the `cos(3n delta)` tower
  - Rivero gives a determinant-like nonlinear candidate

### Weakness

- all current audits say the same thing:
  `cos(9 delta)` appears, but lower harmonics dominate unless additional cancellation occurs
- so the missing step is not “invent a nonlinear observable”; it is “derive the cancellation or
  suppression rule”

### Verdict

This is the **strongest PF-native class** currently on the board.

If the selector is going to be derived inside PF rather than imported from a new external theory,
it is most likely to come from this class.

---

## 8. Candidate class F — General reparameterization tricks

### Form

Any move of the form:

- rename `delta`
- take another rational approximation
- compose with a simple invertible scalar function

without introducing new structure

### Verdict

Dead lane.

This is exactly what the Möbius lemma was written to prevent.

---

## 9. Ranked live lanes

From strongest to weakest:

### Lane 1 — PF-native nonlinear 3-cycle observables

Why first:

- directly relevant to the actual Koide phase problem
- already partially constrained by local audits
- could in principle derive a selector without importing an external ontology

### Lane 2 — Trace / character variables with a genuine selector rule

Why second:

- closest to the cosine structure of the Koide parametrization
- broad enough to include group-theoretic and geometric reformulations
- narrow enough to avoid pure analogy

### Lane 3 — Conformal weights / topological spins / modular data

Why third:

- mathematically real class of upstream rational labels
- strongest external analogy
- but currently lacks a clean bridge to the charged-lepton mass geometry

### Dead lane — projective reparameterizations of the Koide line

Already fenced.

---

## 10. Best honest summary

After the projective classification, the remaining selector problem is no longer:

> which ratio of the square-root masses is the “right” rational?

It is now:

> what genuinely non-projective object sits upstream of the Koide cosine parametrization and could
> carry a selected rational label?

The best current answers are:

- **inside PF**: nonlinear 3-cycle composite observables
- **outside PF / analogy class**: conformal weights, topological spins, modular labels

Neither is closed.

---

## 11. Recommendation

The next bounded pass should not scan more rational approximants.

It should do one of the following:

1. **PF-native pass**  
   Specify the minimal nonlinear 3-cycle observable class that is not equivalent to the already
   audited `f(delta)^n` dead ends, and state exactly what suppression theorem would be required.

2. **External-structure pass**  
   Write a narrow bridge note asking whether any conformal-weight / modular-label class can be
   mapped to the charged-lepton Koide cone without simply reasserting `delta = h`.

If forced to choose one, the better next move is **(1)**, because it attacks the selector in the
same mathematical language the repo already uses.

