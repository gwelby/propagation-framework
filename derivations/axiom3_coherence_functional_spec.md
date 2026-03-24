# Axiom 3 Coherence Functional — Minimal Specification
*What exact mathematical object the PF now needs, and what it must do before anyone claims Axiom 3 is formalized*

**Date**: 2026-03-23
**Author**: Codex
**Status**: Design target / research specification
**Purpose**: Replace vague appeals to "coherence" with an audit-ready mathematical target
**Builds on**: `the_propagation_framework.md`, `derivations/casimir_polynomial_synthesis.md`, `derivations/casimir_polynomial_step_A_audit.md`, `derivations/casimir_polynomial_step_B_audit.md`

---

## 1. Why This File Exists

The Casimir-polynomial program has now done its job.

It did **not** derive the polynomial from the current axioms.
It did isolate the missing object with high precision:

> PF needs a mathematical selection principle over coherent states.

The present wording of Axiom 3 gives a **threshold**:

- incoherent propagation disperses
- coherent propagation persists

What it does **not** yet give is an **ordering**:

- if several states are coherent, which one does PF select?
- why that one rather than another coherent state?

That is the exact frontier.

The missing object can be written in either of two equivalent ways:

1. a **coherence score** `C[ψ]` to be maximized
2. a **coherence cost / free energy** `F[ψ]` to be minimized

These are equivalent up to monotone transformation.
This file uses `F[ψ]` because the current Step B language is already close to a ground-state / variational problem.

---

## 2. The Minimal Job of the Functional

The functional must do two logically distinct things:

### Job A — Threshold

Distinguish coherent structure from incoherent background.

This is the current Axiom 3 content:

- incoherent states should not be stable minima
- coherent states should be stationary or metastable states

### Job B — Selection

Among multiple coherent states in the same topological / representation family, select the PF-fundamental one.

This is the currently missing content:

- why `k = 1` over `k = 2`, `3`, ...
- why `1:1` helical locking over other rational resonances
- more generally, why one coherent branch is fundamental while others are excited, composite, or excluded

If a proposed functional does Job A but not Job B, it has **not** yet formalized the missing part of Axiom 3.

---

## 3. Minimal Domain of Definition

The functional must be defined on candidate PF mode configurations `ψ`.

At minimum, `ψ` must contain:

1. **Closed-loop phase data**
   - phase accumulation around each independent coherent cycle
   - or equivalent action variables

2. **Topology / winding data**
   - primitive loop vs higher winding
   - rational resonance labels `p:q` where relevant

3. **Representation / angular data**
   - at least the relevant invariant such as `C₂ = j(j+1)` where spin structure matters

4. **Kinematic data**
   - causal-velocity constrained drift / internal motion data
   - enough structure to distinguish relativistic from non-relativistic candidates

5. **Energetic data**
   - a scalar energy or effective action at fixed conserved labels
   - enough to test "ground state" claims without handwaving

For the current Casimir target, the minimal state is effectively:

`ψ = (J_θ, J_z, C₂, k, β; constraints from Axioms 1–2)`

where `k` labels the resonance family and `J_z/J_θ = k` in the simplest branch language.

---

## 4. Non-Negotiable Requirements

Any candidate `F[ψ]` must satisfy all of these.

### R1. Symmetry respect

The functional must be invariant under the symmetries the PF already claims for the relevant medium.

Examples:

- vacuum / isotropic sector: no arbitrary preferred spatial axis
- torus/helical representation: no dependence on coordinate labels rather than invariants

For Casimir work, this means no hidden axis-fixing term that simply inserts `j` or `√C₂` by hand.

### R2. Threshold + ordering must be separated

The functional must distinguish:

- incoherent states vs coherent states
- coherent states vs the **selected** coherent state

This is critical.
The recent failures came from smuggling the second into the first.

Example of a bad move:

- proving that several rational torus states are coherent
- then silently calling the simplest one "the" coherent state

That is not a derivation.

### R3. The target cannot be built in by definition

A candidate functional fails immediately if it contains any term equivalent to:

- `(J_z - J_θ)^2`
- `(k - 1)^2`
- `(\gamma\beta² - √C₂)^2`

unless that term is itself derived from a prior PF-native principle.

Those forms may appear **after** derivation as consequences.
They may not appear as starting assumptions disguised as "coherence."

### R4. The functional must make contact with Axiom 2

The Casimir work already established that Axiom 2 is essential.

A coherence functional that ignores causal-velocity / relativistic structure and still claims to derive the Weinberg angle is almost certainly wrong.

At minimum, it must explain why the relativistic variable survives:

- `γβ²` rather than `γβ`
- equivalently the helical phase count `N_dB = γβ²`

### R5. Excited coherent states must be representable

If the functional selects a ground state, it should also allow the possibility of excited coherent states or explain why they are forbidden.

Otherwise it is only renaming the answer.

For the helical family, this means `k > 1` should appear as:

- local extrema
- metastable states
- unstable saddles
- or be excluded by a genuine theorem

but not simply vanish by fiat.

### R6. The functional must be portable across route languages

The same object should admit at least two equivalent readings:

- one-mode / helical / phase-counting language
- two-sector / coupling / matrix language

If it only works in one route's notation, it is probably an artifact of that route.

---

## 5. Minimal Acceptance Tests

Before any claim that "Axiom 3 has been formalized," the candidate functional must pass these tests.

### Test 1 — Helical family selection

Input:

- fixed `C₂`
- coherent helical family labeled by rational `k = p/q`

Required output:

- either a unique optimum at `k = 1`
- or a proof that no unique optimum follows from the current axioms

Anything else is inconclusive.

### Test 2 — No smuggled Casimir answer

Audit the functional's primitive terms.

Required output:

- no term whose minimum is visibly equivalent to `J_z = J_θ` unless derived upstream

If this fails, the functional is invalid as evidence.

### Test 3 — Relativistic sensitivity

Take the non-relativistic limit.

Required output:

- either the functional degenerates to the known wrong non-relativistic branch
- or it explicitly shows why the relativistic correction is essential

This is necessary because the repo already established that Axiom 3 alone, without Axiom 2, does not give the right Weinberg-angle structure.

### Test 4 — Two-sector compatibility

Translate the selected state into the Route G language.

Required output:

- the same selected condition should look like a kinematic-angular locking or zero-mode condition
- not a contradictory or unrelated criterion

### Test 5 — Background consistency

The incoherent background should not outrank coherent structure.

Required output:

- coherent states must appear as structured extrema against incoherent background
- not merely as arbitrary local labels

---

## 6. Three Smallest Viable Functional Families

These are the three most reasonable families to try.

### Family A — Phase-mismatch functional

Prototype:

`F_phase = mismatch(closed-loop phases, cross-loop phases, representation content)`

Good:

- closest to the current Axiom 3 wording
- directly tied to stable phase relationships

Risk:

- pure phase closure alone typically admits many rational resonances
- it may solve threshold but not selection

So if this route works, it must contain a PF-native reason why the simplest locked state is preferred.

### Family B — Free-energy / Lyapunov functional

Prototype:

`F = E + coherence_penalty`

or

`F = E - coherence_benefit`

Good:

- most natural home for Step B
- makes "ground coherent state" a mathematical statement

Risk:

- easy to smuggle the answer by inventing a penalty minimized at `k = 1`
- must derive the coherence term, not guess it

### Family C — Information-theoretic coherence functional

Prototype:

`F = -I(internal; external) + energetic / causal constraints`

Good:

- matches the "self-referential coherence" language already present in Axiom 3
- naturally expresses "selected state" as maximal mutual constraint between internal and external structure

Risk:

- can become too abstract unless connected back to phase and action data

---

## 7. What Definitely Does NOT Count

The following do **not** count as formalizing Axiom 3:

1. Rephrasing the desired answer in prettier language
   - "single structure means 1:1"
   - "fundamental means primitive"
   - "coherence means locking"

2. Pure threshold conditions
   - individual quantization of each loop
   - rationality of action ratios

3. Unmotivated minimum-energy claims
   - "ground states are lower energy, therefore selected"
   - without a PF-native relaxation / Lyapunov / coherence-cost principle

4. Route-specific ansatzes
   - any argument that only works in one notation and does not survive translation into another route

---

## 8. The Smallest Honest Deliverable

The next real milestone is **not**:

- a final bridge file
- a confidence upgrade
- another Casimir route

The next real milestone is:

> a candidate `F[ψ]` written explicitly enough that Codex can run the five acceptance tests above.

That candidate may fail.
Failure is still progress if it localizes the remaining missing ingredient.

---

## 9. Immediate Work Order

If the team wants the shortest path forward, do this:

1. **Define the state manifold for the current problem**
   - exactly what counts as a candidate helical coherent state
   - what is fixed and what is varied

2. **Write one candidate functional only**
   - smallest viable form
   - probably Free-energy / Lyapunov or Information-theoretic

3. **Run the acceptance tests**
   - especially Test 1 and Test 2

4. **Classify the outcome honestly**
   - derives `k = 1`
   - narrows the gap
   - or proves that Axiom 3 as written is insufficient

If it proves insufficient, the honest next move is not embarrassment.
It is to introduce an explicit additional principle, e.g.:

> **Axiom 3b / Corollary candidate**:  
> Among coherent states in the same topological class, the stable fundamental PF mode is the one minimizing the coherence free energy.

That would be a real scientific clarification, not a defeat.

---

## 10. Bottom Line

The missing mathematical object is now clear:

> PF needs a coherence functional that does not merely distinguish coherent from incoherent states, but selects the fundamental state among coherent candidates without smuggling in the answer.

For the current Casimir problem, that means:

- not just proving rational resonance
- not just proving phase closure
- but explaining why PF selects the `1:1` coherent helical state

Until that object exists, Axiom 3 remains conceptually powerful but mathematically underdetermined at exactly the point where the hardest derivations bottleneck.

That is not failure.
That is the frontier.
