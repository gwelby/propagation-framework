# T1 Non-Redundancy Lemma
*Can the missing hypothesis `A_NR` be derived from Axioms 1-3 alone?*

**Date**: 2026-04-04  
**Author**: Codex  
**Status**: HONEST NO-GO for derivation from current Axioms 1-3 alone; names the minimal extra inputs; no confidence change  
**Builds on**:
- `FIVE_AGENT_COORDINATION.md` Agent 1 brief [CITATION NEEDED]
- `derivations/t1_physical_realization_theorem_audit_2026-03-31.md` [CITATION NEEDED]
- `derivations/t1_physical_realization_theorem.md` [CITATION NEEDED]
- `derivations/axiom3_coherence_functional_spec.md` [CITATION NEEDED]
- `derivations/t1_closure_joint_spec.md` [CITATION NEEDED]
- `derivations/three_generations_t1_proof.md` [CITATION NEEDED]
- `derivations/g3_faithfulness_bridge_challenge.md` [CITATION NEEDED]
- `CLAIMS.md` [CITATION NEEDED]
- `RESEARCH/three_generation_topology/MASTER.md` [CITATION NEEDED]

---

## 1. Exact Target

The missing T1 step is the strict inequality

`A_NR: I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0`.

The March 31 audit is explicit: the current theorem proves only

`F_C^tot >= F_C^(1)`

by the chain rule, and the strict coherence-deficit step still requires `A_NR`. [CITATION NEEDED]

Write

- `X_1 = Phi_int^(1)`
- `Y_1 = Phi_ext^(1)`
- `X_2 = Phi_int^(2)`
- `Y_2 = Phi_ext^(2)`

Then the missing statement is

`I(X_2; Y_2 | X_1, Y_1) > 0`.

Using the conditional-KL identity,

`I(X_2; Y_2 | X_1, Y_1) = E[D_KL(p(Y_2 | X_1, Y_1, X_2) || p(Y_2 | X_1, Y_1))]`.

So the exact content of `A_NR` is:

> after conditioning on the weight-1 branch, the weight-2 branch still changes the conditional external phase law on a set of positive measure.

That is an information-faithfulness claim, not a topology claim by itself.

---

## 2. Main Result

### Theorem

`A_NR` is **not derivable** from the current PF axioms alone, even granting:

1. Axioms 1-3,
2. `pi_1(SO(3)) ~= Z_2`,
3. topological availability of the weight-2 branch,
4. the Family C candidate language `F_C = I(Phi_int; Phi_ext)`.

### Proof

The proof is by admissible countermodel.

#### Countermodel A: available but unpopulated branch

Assume `(X_1, Y_1)` is any coherent weight-1 stable mode.
Let the weight-2 branch be topologically available but physically unpopulated, represented in the state description by constants:

`X_2 = x_0`, `Y_2 = y_0`.

Then

`p(Y_2 | X_1, Y_1, X_2) = p(Y_2 | X_1, Y_1)`

almost surely, so

`I(X_2; Y_2 | X_1, Y_1) = 0`.

This does not violate Axioms 1-3. It only says the medium realizes one coherent branch and leaves the other merely available. The current axiom set does not yet contain a selector saying every available topological branch must carry irreducible coherent information. [CITATION NEEDED]

#### Countermodel B: populated but conditionally redundant branch

Even if the weight-2 branch is populated, `A_NR` still need not follow.
Choose

`X_2 = f(X_1, Y_1)`,

`Y_2 = g(X_1, Y_1)`

for measurable functions `f, g`.

Then `(X_2, Y_2)` may label a distinct topological branch in the state description, but they add no conditional information beyond `(X_1, Y_1)`. Again

`p(Y_2 | X_1, Y_1, X_2) = p(Y_2 | X_1, Y_1)`

almost surely, hence

`I(X_2; Y_2 | X_1, Y_1) = 0`.

So topological distinctness does **not** imply information-theoretic non-redundancy.

#### Why the countermodels are enough

To derive `A_NR` from Axioms 1-3, every admissible model satisfying those axioms would have to force `I(X_2; Y_2 | X_1, Y_1) > 0`.
But the two constructions above satisfy the current logical boundary while giving equality instead of strict positivity.
Therefore `A_NR` is not a theorem of the present axioms.

`QED`

---

## 3. Consequences for the Five Agent-1 Questions

### 3.1 Can `A_NR > 0` be derived from Axiom 3 alone?

No.

The coherence-functional spec already isolates the reason: Axiom 3 currently gives a **threshold** for structure, not an **ordering** among multiple coherent candidates. [CITATION NEEDED]
`A_NR` is stronger than threshold coherence. It says a particular branch remains conditionally informative after other branches are conditioned out.
That is extra structure.

### 3.2 If T1 uses an extremal principle, is that derivable?

Not from the current axioms.

The March 31 audit already withholds sign-off on the claim that Axiom 3 selects the Family C functional as an actual branch-ordering principle. [CITATION NEEDED]
Even if one **adds** the selector

`A_Sel: stable PF equilibria locally maximize the accepted coherence functional over admissible branch populations`,

that still does not force T1 unless the improvement is strict.
In Countermodels A and B,

`F_C^tot - F_C^(1) = 0`,

so a selector alone is insufficient.

### 3.3 Can non-redundancy be reframed as a no-simplification condition?

Yes, but only as a renamed extra assumption.

A clean formulation is:

> `A_NS` (No-Simplification / Branch Dispensability Ban): a stable PF equilibrium may not contain a topologically distinct realized branch whose internal-external phase law is conditionally recoverable from the already-populated branches.

Formally, for the weight-2 branch this means:

`p(Y_2 | X_1, Y_1, X_2) != p(Y_2 | X_1, Y_1)`

on a set of positive measure.

This is just the conditional-dependence form of `A_NR`.
So the reframing is legitimate, but it does **not** derive the statement from existing axioms.

### 3.4 Does Fisher information geometry close the gap?

Not by itself.

There is a conditional route:

1. define a branch-local parameter `theta_2` for the conditional family `p_theta(Y_2 | X_1, Y_1, X_2)`,
2. derive a nonzero conditional Fisher block for `theta_2`,
3. show the realized distribution over `X_2` explores that branch-local direction.

Then the local conditional KL divergence is quadratic in the perturbation,

`D_KL(p_theta || p_theta0) = (1/2) delta(theta)^T G_(2|1) delta(theta) + o(||delta(theta)||^2)`,

so positive conditional Fisher curvature would witness local distinguishability of branch-2 phase data.

But the current PF theorem package does **not** derive:

1. the statistical family for the T1 branches,
2. the branch-local parameter `theta_2`,
3. positivity of the relevant conditional Fisher block.

So Fisher geometry is a possible later bridge, not a present derivation.

### 3.5 What is the weakest additional assumption that closes T1?

This splits into two levels.

For the **strict inequality alone**, the weakest extra input is:

> `A_BF` (Conditional Branch Faithfulness):  
> `p(Y_2 | X_1, Y_1, X_2) != p(Y_2 | X_1, Y_1)` on a set of positive measure.

By the conditional-KL identity, `A_BF` is equivalent to `A_NR > 0`.
It is weaker than demanding full independence of sectors, weaker than saying "all available branches are populated," and weaker than any global complexity-minimization principle.

For the **full T1 physical-realization step**, the weakest closure package is:

1. `A_BF` / `A_NR` for strict gain,
2. `A_Sel` for why the medium must move to the higher-coherence configuration.

Without `A_BF`, there may be no gain to select.
Without `A_Sel`, there is no reason the medium must realize the gain.

---

## 4. The Precise No-Go

The no-go can be stated sharply:

> Topological availability of a branch is not enough to prove information-theoretic necessity of that branch.

What topology gives is:

1. a second loop class exists,
2. a genuine weight-2 mode would live on the `SU(2)` lift rather than on `SO(3)` alone. [CITATION NEEDED]

What topology does **not** give is:

1. a branch selector,
2. a faithful branch-to-observable map,
3. a proof that the weight-2 branch carries conditionally irreducible phase information.

That is the exact logical break.

---

## 5. Strongest Honest Statement After This Lemma

The strongest honest T1 statement remains:

> PF derives the `(1,2)` closure-order bifurcation and conditionally localizes the weight-2 branch to the `SU(2)` double cover, but it does not yet derive that the weight-2 branch contributes non-redundant coherent information. Therefore the physical-realization bridge remains open. [CITATION NEEDED]

No confidence upgrade follows from this file. [CITATION NEEDED]

---

## 6. Next Bounded Step

The next honest move is **not** another generic appeal to "coherence wants completeness."
It is to derive one of the following, explicitly:

1. a PF-native **branch-faithfulness theorem**: a realized nontrivial rotational branch must alter the conditional external phase law,
2. or a concrete **branch-local statistical model** whose conditional Fisher block is strictly positive and whose observables are PF-native,
3. or an honest statement that PF needs a new axiom/corollary beyond the current Axiom 3 threshold language.

This aligns T1 with the same structural issue already identified elsewhere in the repo: coherence language without a derived faithfulness/selection bridge does not by itself close a branch-choice theorem. [CITATION NEEDED]

