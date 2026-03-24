# Casimir Polynomial — Codex Audit of Step B
*Does Axiom 3 imply that the stable coherent state is the minimum-energy coherent state, and therefore select `k = 1`?*

**Date**: 2026-03-23
**Author**: Codex
**Scope**: Audit `casimir_polynomial_steps_AB.md` Step B against the canonical PF docs and current Casimir synthesis
**Verdict**: ARGUED, precisely located — the minimum-energy principle is not currently derivable from Axiom 3 as written

---

## 1. The Claim Being Audited

Step B isolates the remaining selection problem:

> On the helix torus, coherence and single-valuedness allow rational resonances `J_z/J_θ = p/q`.
> Why does the PF select the fundamental `1:1` state, i.e. `k = 1` and `J_z = J_θ`?

The strongest proposed closure path is:

> the stable coherent state is the minimum-energy coherent state for fixed spin content,
> therefore the `k = 1` member of the helical family is the PF ground state.

This is the right question.
It is also stronger than what the current axiom text actually guarantees.

---

## 2. What Survives the Audit

Two parts are solid.

### Surviving part 1: the energy ordering is real

Within the helical family used in `casimir_polynomial_steps_AB.md`, larger `k` means larger `γβ² = k√C₂`, hence larger `β`, hence larger total energy

`E = γmc²`.

So for fixed `m` and `j`, the `k = 1` branch is the lowest-energy branch in that family.

That ordering is a genuine structural observation.

### Surviving part 2: Axiom 3 makes a ground-state style principle plausible

Axiom 3 says stable structure exists where coherence persists against incoherent background.
That strongly suggests that coherent structures should have preferred stable states and excited states.

So the proposed closure path is physically natural:

- `k = 1` as the ground coherent mode
- `k > 1` as excited coherent modes

This is good PF language.
It is not yet a theorem.

---

## 3. Why Step B Does Not Yet Count as DERIVED

### Objection 1: Axiom 3 requires coherence, not energy minimization

The canonical axiom says:

> coherent propagation persists; incoherent propagation disperses.

It does **not** say:

- among multiple coherent states, the lowest-energy one is uniquely stable
- the fundamental mode is defined by minimum energy
- excited coherent states are excluded from "structure"

Those are reasonable physical additions, but they are additions.

### Objection 2: coherence and minimum energy are not equivalent

The present Step B argument shows that several rational resonances can be coherent on the torus.

That means coherence alone underdetermines the selection.

To go from

`many coherent resonant states exist`

to

`the PF selects the minimum-energy one`

requires an extra ordering principle.

That principle is not contained in the current English statement of Axiom 3.

### Objection 3: the argument smuggles in a coherence cost functional

`casimir_polynomial_steps_AB.md` already states the real hidden ingredient correctly:

> maintaining coherence requires energy above incoherent background
> and the stable state is the minimum-energy coherent one.

That is effectively a coherence functional or free-energy principle.

But the framework has **not yet defined** such a functional mathematically.

So the current Step B closure path is:

- not derived from Axiom 3 alone
- not ruled out
- a candidate new principle waiting to be formalized

### Objection 4: Axiom 1 does not rescue the argument by itself

Path 2 also tries the wording:

> fundamental mode = primitive helix loop, not a `k`-fold composite.

This is suggestive, but not sufficient.

Why not:

- a primitive `(1,2)` or `(2,1)` loop
- or a distinct low-order rational state still counted as fundamental?

Axiom 1 says matter is a self-reinforcing propagation pattern.
It does **not** yet define "fundamental" in a way that uniquely selects `1:1` over other primitive rational windings.

So the topological wording rephrases the gap.
It does not close it.

---

## 4. Correct Audited Status

The honest Step B status is:

> **ARGUED, precisely located**: If PF is supplemented by a principle that, among coherent helical resonances with fixed angular content, the stable fundamental mode is the minimum-energy one, then `k = 1` follows cleanly.

That principle may be:

1. a corollary of Axiom 3 after Axiom 3 is formalized as a coherence/free-energy functional
2. a new sub-axiom or explicitly named corollary
3. or false, in which case Step B does not close from the present framework

Right now, the repo does not justify choosing option 1 over 2.

---

## 5. What Would Close Step B

Any one of the following would likely close it:

1. A PF-native coherence functional `F` whose stationary coherent states exist at multiple rational resonances but whose minimum selects `k = 1`.
2. A formal theorem from Axiom 3 showing that "stable structure" means the energetically lowest coherent state in a resonant family.
3. A precise definition of "fundamental mode" in Axiom 1 that excludes all non-`1:1` primitive windings on the helix torus.

Until one of these exists, the honest statement is:

- `k = 1` is the best-motivated closure path
- not a theorem of Axioms 1–3 as currently written

---

## 6. Bottom Line

Step B is the real remaining barrier.

The current formalism supports:

- a genuine energy ordering of the helical family
- a plausible ground-state interpretation
- a sharply bounded question

It does **not** yet support:

> Axiom 3 implies that the stable coherent state is the minimum-energy coherent state.

So the right repo-level conclusion is:

> the minimum-energy principle is currently a candidate additional principle, not a derived consequence of the canonical PF axioms.
