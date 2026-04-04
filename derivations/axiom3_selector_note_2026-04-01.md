# Axiom 3 Selector Note (2026-04-01)
*Turning "coherence selects structure" into a bounded mathematical target*

**Status**: Open design target. This note does not upgrade Axiom 3, T1, or T2.  
**Purpose**: Make the selector problem explicit enough that it can either close or fail cleanly.  
**Truth sources**: `AGENTS.md`, `CLAIMS.md`, `ACTIVE_ISSUES.md`, `the_propagation_framework.md`, `derivations/axiom3_coherence_functional_spec.md`, `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`

---

## 1. What Is Already True

Axiom 3 already does real work at the threshold level:

- incoherent propagation disperses
- coherent propagation can persist
- stable structure requires phase closure and self-reinforcement

The repo also has one accepted local selector corollary:

- **Axiom 3b / Minimal Winding** selects `k = 1` inside the bounded helical family used for the Weinberg-angle closure

That is important, but it is not yet a general selector theorem for the whole framework.

The live unresolved question is broader:

> when multiple coherent candidates are available, what mathematical rule selects the fundamental PF structure rather than merely permitting several coherent options?

---

## 2. The Exact Gap

Right now the framework has a threshold principle more clearly than it has an ordering principle.

That means the repo can often say:

- which configurations are coherent enough to exist

but cannot yet always say:

- why one coherent branch is fundamental
- why another coherent branch is excited, composite, metastable, or forbidden

This matters immediately for:

- **T1**, where the missing step is why Axiom 3 should force physical population of the available weight-2 branch
- parts of **T2**, where selector language can otherwise get smuggled in through model choices

It also explains why some sentences in the repo still drift from theorem language into interpretation.

---

## 3. Strongest Honest Current Statement

The strongest honest current statement is:

> PF has an accepted local selector corollary in the bounded minimal-winding setting, but it does not yet have a general selector theorem that orders coherent PF candidates across the broader frontier.

Until that changes, any broader sentence of the form

- "coherence always selects the simplest structure"
- "the medium prefers the fundamental branch"
- "the available coherent branch must be populated"

is interpretation unless a specific selector object is written down and survives audit.

---

## 4. The Minimal Deliverable

The next deliverable is not a grand new axiom.
It is one bounded selector target.

That target must specify all four pieces:

1. **Domain**
   A named family of PF-admissible candidates `psi` with fixed conserved labels and stated topology.

2. **Ordering object**
   Either:
   - a selector functional `F[psi]`
   - a selector score `Sigma[psi]`
   - or an explicit corollary stating a partial order over coherent candidates

3. **Classification rule**
   A way to say what happens to non-selected coherent states:
   - excited
   - composite
   - metastable
   - forbidden

4. **Falsifier**
   A concrete condition under which the selector would fail.

If any one of those is missing, the selector is still English-heavy.

---

## 5. Acceptance Tests

Any proposed selector should pass these tests before it is allowed to steer theorem language.

### Test 1. Recover the local Axiom 3b result without hiding it in the definition

Inside the helical family, the selector should recover the accepted `k = 1` result or make clear that Axiom 3b remains an additional bounded corollary.

What does not count:

- building in a term like `(k - 1)^2`
- calling "primitive" the winner by definition

### Test 2. Separate threshold from selection

The selector must do more than restate phase closure.

It must distinguish:

- incoherent vs coherent
- coherent vs fundamental

If it only does the first, it does not solve the live gap.

### Test 3. State whether T1's Family C language is actually justified

For T1, the selector must either:

- justify why `F_C = I(Phi_int; Phi_ext)` is a PF-native ordering object
- or reject it and force a different route

What does not count:

- assuming the Family C functional is "obviously what Axiom 3 means"

### Test 4. Keep contact with Axiom 2 when kinematics matter

Where the candidate family depends on causal or relativistic structure, the selector cannot float free of Axiom 2.

Otherwise the repo risks reintroducing exactly the "beautiful English, missing mechanism" pattern it is trying to remove.

### Test 5. Name the failure mode

The selector must say what would break it.

Examples:

- a higher-winding coherent state outranks the claimed fundamental state under the same rule
- a stable weight-1-only PF model exists with no coherence deficit despite an available weight-2 branch
- the ordering depends on a route-specific ansatz rather than a PF-native invariant

---

## 6. Two Honest Ways This Can Close

### Route A. Derived selector object

Write one explicit selector object and show that it survives the tests above.

This is the strongest route, but it is also the hardest.

### Route B. Explicit bounded corollary

State an additional bounded principle in the style of Axiom 3b:

> within a named PF family, the stable fundamental mode is the one minimizing a specific derived instability count, winding count, or coherence cost

This is weaker than a general selector theorem, but still scientific if the scope is explicit.

What does not count is using a bounded corollary in one route and then pretending the whole framework now has a general selector.

---

## 7. Immediate Work Order

1. Pick one family only.
   Start with the family that actually blocks theorem closure.

2. State the candidate domain exactly.
   What is varied, what is fixed, and what counts as an admissible coherent candidate?

3. Write one selector object or one bounded corollary only.
   No competing selector zoo.

4. Run the acceptance tests.
   Especially Test 2 and Test 3.

5. Record the failure honestly if it fails.
   A failed selector note is still progress if it rules out a tempting but invalid bridge.

---

## 8. What This Means For The Current Queue

This note places the work order in a clearer upstream-to-downstream sequence:

- selector note first
- T1 physical-population bridge second
- T2 denominator theorem third
- G3 closure after that, on its exact remaining operator/probability bridge

The point is not that every open theorem depends on one universal selector.
The point is that the selector ambiguity is currently the cleanest upstream source of category blur.

---

## 9. Bottom Line

PF does not currently lack ideas.
It lacks a general mathematical way to say why one coherent candidate is fundamental rather than merely allowed.

The bounded next step is:

> write one selector object or one bounded selector corollary clearly enough that Codex can either sign it off or reject it.

That is how Axiom 3 stops being "strong in English, weaker in mathematics" at the exact place where T1 still stalls.
