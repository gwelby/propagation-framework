# Codex Hostile Audit of Axiom 3 Candidate Functional F1
*Is `F₁` a real PF coherence functional, or just the first neat scalar that picks `1:1`?*

**Date**: 2026-03-23
**Author**: Codex
**Scope**: Audit `axiom3_candidate_functional_F1.md` against `axiom3_coherence_functional_spec.md`, current Casimir audits, and the canonical PF axioms
**Verdict**: Promising reduced candidate for Step B; not yet an acceptable formalization of Axiom 3

---

## 1. What Survives the Audit

Three things are genuinely good.

### Surviving part 1: `F₁` is explicit

This matters.

The team now has a concrete scalar object:

`F₁(p,q; C₂) = E_{p:q} T_prim(p,q)/(2πħ)`

instead of vague language about coherence, simplicity, or fundamentality.

That is real progress.

### Surviving part 2: `F₁` does not directly hard-code the answer

It does **not** start with:

- `(J_z - J_θ)^2`
- `(k - 1)^2`
- `(\gammaβ² - √C₂)^2`

So it passes the most basic anti-smuggling check.

### Surviving part 3: it unifies two prior intuitions

`F₁` combines:

- energy ordering of the helical family
- primitive closure complexity

That is better than pure minimum energy or pure primitive-loop language taken separately.

If a real Step B functional exists, it may well look qualitatively like this.

---

## 2. Main Audit Finding

`F₁` is a plausible **reduced Step B candidate**.

It is **not yet** a credible full Axiom 3 functional.

The reason is simple:

> the minimization result is mathematically clean, but the choice of what is being minimized is still an ansatz.

That is the whole problem.

---

## 3. Specific Audit Objections

### Objection 1: `F₁` lives only on the already-coherent resonance family

The spec required the missing object to do two jobs:

1. threshold: coherent vs incoherent
2. selection: which coherent state is fundamental

`F₁` only does Job 2.

It is defined on the family of already-admitted helical resonances `(p,q)`.
It does not distinguish:

- incoherent states
- non-resonant states
- generic field configurations

So `F₁` cannot yet be "the Axiom 3 functional."

Best reading:

> `F₁` is an effective selection functional on the reduced Step B state space.

That is useful.
It is narrower than the full claim.

### Objection 2: the primitive cell choice is the hidden decisive move

The candidate defines:

`T_prim = q T₀`.

This is where most of the selection power comes from.

Why this is not innocent:

- it chooses the internal period `T₀` as the privileged clock
- it treats the first primitive self-return as the relevant coherent cell
- it penalizes larger `q` directly

But why should PF minimize **action per primitive self-return** rather than, for example:

- action per unit time
- action per closed loop of a different basis
- action per independent phase-closure event
- action per information bit
- energy alone
- or some other monotone complexity score?

Right now, the proof that `(1,1)` minimizes `F₁` is less important than the unproved choice of `T_prim`.

That is the main hidden assumption.

### Objection 3: the functional is asymmetric in the two torus cycles

The Step B problem lives on a torus with two cycles.

Yet `F₁` is built from:

- one energy scalar
- one closure time measured in units of the internal cycle

This privileges the internal cycle over the drift cycle.

Yes, one can say `T_prim = q T₀ = p T_drift`.
But the candidate is still constructed from the internal cycle as the natural clock.

That may be right.
It is not yet derived.

Until this asymmetry is justified, `F₁` remains a shaped ansatz rather than a canonical torus functional.

### Objection 4: the rest-energy term may be doing too much of the work

Because `m` is fixed, the energy entering `F₁` is:

`E = γ mc²`.

The large rest-energy piece is always present.

So a lot of the minimization is effectively:

- penalize large `q`
- mildly correct by `γ`

That means `F₁` may be selecting topological simplicity with a relativistic garnish, rather than capturing a genuinely PF-native coherence law.

This is not fatal.
But it weakens the claim that `F₁` has already found the real physics.

### Objection 5: many other monotone functionals would also pick `(1,1)`

This is the harshest point.

Once the domain is positive integers `(p,q)`, many candidates would choose `(1,1)`:

- `p + q`
- `pq`
- `qγ`
- `pγ`
- `p + √(p² + q²)`
- and so on

So the fact that `F₁` picks `(1,1)` is not strong evidence by itself.

The real question is:

> why this scalar, and not another one from the same broad monotone family?

Until that is answered, `F₁` is a good candidate, not a privileged one.

### Objection 6: no relaxation mechanism is supplied

Calling `F₁` "free-energy / Lyapunov-like" is suggestive.

To make that real, one needs a dynamical statement such as:

- the coherent mode relaxes downhill in `F₁`
- incoherent background absorbs excess closure action
- or perturbations increase `F₁` and the system returns to the minimum

None of that is currently derived.

Without a downhill flow, `F₁` is an ordering functional, not yet a Lyapunov functional.

### Objection 7: portability to the two-sector route is missing

The spec required portability across route languages.

`F₁` has not yet been translated into:

- Route G matrix language
- a broader Hamiltonian
- or an information-theoretic form

So it is still route-local.

That is not disqualifying.
It is incomplete.

### Objection 8: Step A is still only strong argued

`F₁` depends on `√C₂`.

That means `F₁` inherits the current Step A conditionality.

So even a perfect Step B closure via `F₁` would still leave the full Casimir chain one audit step short.

---

## 4. What `F₁` Is Best Read As

The honest reading is:

> `F₁` is the first serious reduced candidate for the missing Step B selection principle.

That is already worthwhile.

It is **not** yet:

- the Axiom 3 functional
- a proof of Step B
- or something the team should emotionally trust

`F₁` earns the right to be attacked further.
It does not earn the right to be believed yet.

---

## 5. What Would Strengthen `F₁`

Any one of the following would materially improve it:

1. Derive `T_prim` as the unique PF coherent cell from torus geometry rather than choosing it.
2. Show that a broader field-level or Hamiltonian coherence functional reduces to `F₁` on the helical family.
3. Produce a monotone-equivalent form of `F₁` from the two-sector Route G language.
4. Derive a genuine Lyapunov or dissipative relaxation law with `dF₁/dt ≤ 0`.

Any one of those would move `F₁` from "clever candidate" toward "real principle."

---

## 6. Fastest Falsification Tests

If the team wants to kill `F₁` quickly, these are the right attacks.

1. **Primitive-cell attack**
   - Show that a different equally natural choice of coherent cell gives a different selector than `(1,1)`.

2. **Symmetry attack**
   - Show that `F₁` depends on a chosen torus basis rather than an invariant torus quantity.

3. **Route-G attack**
   - Show that no monotone-equivalent scalar arises in the two-sector coupling picture.

4. **Dynamics attack**
   - Show that there is no plausible PF relaxation law under which `F₁` decreases.

If `F₁` survives those four, it becomes genuinely interesting.

---

## 7. Bottom Line

Hostile verdict:

> `F₁` is the best reduced Step B candidate so far, but it is still an ansatz centered on one unproved choice: that PF should minimize action cost per primitive self-return.

That means:

- worth keeping
- worth attacking
- not yet safe

This is exactly the right stage to be in before the team gets attached to it.
