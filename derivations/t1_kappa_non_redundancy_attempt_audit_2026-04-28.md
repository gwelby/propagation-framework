# T1 Kappa Non-Redundancy Attempt — Codex Audit

**Date:** 2026-04-28  
**Auditor:** Codex  
**Target:** proposed section "Lemma: Axiom 3 Non-Redundancy (Physical Realization)" for `derivations/three_generations_t1_proof.md`  
**Verdict:** NO-GO as a derivation. Useful as a named failed route / proof obligation.  
**Status impact:** T1 remains `PARTIAL DERIVATION 0.85`; T3 remains `CONDITIONAL 0.85`.

---

## 1. Exact Proposed Move

The proposal attempts to close T1 by adding a topological term to a coherence functional:

```text
C[psi] = integral |psi|^2 dmu + kappa * (topological winding)
```

with `kappa` described as a PF-derived coupling, not a free parameter.

It then argues:

1. `pi_1(SO(3)) = Z_2` gives two closure classes.
2. The coherence functional is sensitive to holonomy class.
3. `kappa > 0` favors the nontrivial branch.
4. The trivial branch remains a local maximum by minimal energy.
5. Therefore both classes are physically realized.

---

## 2. What Survives

The topological classification survives:

```text
pi_1(SO(3)) ~= Z_2
```

still gives exactly two loop classes, and the closure-order theorem still gives possible lifted closure orders `1` and `2`.

The proposed route also correctly identifies the load-bearing missing object:

```text
kappa = topological-coherence coupling
```

If a PF-native theorem derived this coupling with the right sign and showed that both branches are stable extrema, it could become a serious T1 route.

---

## 3. Hidden Steps

### H1: The topological term is inserted, not derived

The proposed term

```text
kappa * (topological winding)
```

does exactly the work the proof needs. But no existing PF axiom derives this additive functional form, its normalization, or its sign.

This is structurally the same error prior audits rejected: it converts topological availability into physical selection by adding a selector term.

### H2: `kappa > 0` is an assumption

The proof requires `kappa > 0` to make the nontrivial branch favorable. Axiom 3 says stable structure requires coherence; it does not currently say winding increases coherence, decreases coherence, or splits into a local-maxima pair.

The opposite sign or zero coupling is not ruled out by Axioms 1-3 as currently stated.

### H3: "Both classes maximize" is not shown

Even granting a winding-sensitive functional, the proposal does not prove two local maxima. It asserts:

- class `[1]` gains from winding,
- class `[0]` gains from no winding cost.

That is plausible variational language, but it is not a proof without:

1. an explicit cost term,
2. an explicit topology term,
3. a domain for admissible modes,
4. a Hessian or stability argument at both candidate extrema.

### H4: This does not derive `A_NR`

The existing missing T1 hypothesis is:

```text
A_NR: I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0
```

The proposed `kappa` term does not prove that the weight-2 branch contributes conditionally non-redundant internal/external phase information. It bypasses the information-theoretic gap by switching to a new unproven energy/coherence functional.

---

## 4. Countermodel

The existing no-go in `t1_non_redundancy_lemma.md` still applies.

Construct a PF-admissible model with:

```text
kappa = 0
```

or a model where the nontrivial branch is topologically available but unpopulated:

```text
X_2 = x_0
Y_2 = y_0
```

Then:

```text
I(X_2; Y_2 | X_1, Y_1) = 0
```

and the proposed strict physical-realization conclusion fails.

Nothing in Axioms 1-3 currently excludes this countermodel. Therefore the proposal is not a theorem of the present framework.

---

## 5. Verdict

Do **not** add the proposed section as a proof.

Allowed wording:

> A possible future T1 route is to derive a PF-native topological-coherence coupling `kappa` whose variational structure forces both `Z_2` closure classes to be stable extrema. This route is currently open because the coupling, sign, and stability analysis are not derived from Axioms 1-3.

Forbidden wording:

> Axiom 3 Non-Redundancy derives that both `Z_2` classes are physically realized.

That statement is not supported.

---

## 6. Exact Next Proof Obligation

The smallest valid next target is not "add the lemma." It is:

```text
Derive kappa from Axioms 1-3, including:
1. the functional form C[psi],
2. the sign of kappa,
3. the winding normalization,
4. proof that both closure classes are local maxima,
5. proof that the result implies A_NR or replaces A_NR with an audited equivalent.
```

Until this is done, T1 remains `PARTIAL DERIVATION 0.85`.

