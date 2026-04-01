# T1 Physical Realization Theorem
*Formalizing the remaining numerator gap for the `(2,1)` topological weights*

**Date**: 2026-03-31
**Author**: Codex
**Status**: CANDIDATE DERIVATION -- audited 2026-03-31; Proof Obligation 2 remains an argued bridge, not a closed proof
**Builds on**:
- `derivations/topological_weights_t1_audit_2026-03-28.md`
- `derivations/t1_closure_joint_spec.md`
- `derivations/axiom3_coherence_functional_spec.md`
- `derivations/g3_lowest_wins_skeptic_audit.md`
- `derivations/g3_faithfulness_bridge_challenge.md`
- `derivations/g3_spin_selection_final_status.md`
- `derivations/casimir_axiom3_functional_candidate_C.md`

---

## 1. Theorem Statement

**Target theorem.**

> In a 3D PF medium satisfying Axioms 1-3, stable propagation modes must realize both closure-order classes, with weights `(2,1)`.

More explicitly: the contractible rotational branch of closure order `1` and the nontrivial lifted branch of closure order `2` must both occur as physically populated stable sectors of the medium.

---

## 2. Allowed Inputs

### Allowed

1. **Axioms 1-3**
   - propagation is fundamental
   - causal propagation has finite maximal speed
   - stable structure requires coherent phase closure

2. **3D rotation topology**
   - `pi_1(SO(3)) ~= Z_2`
   - therefore exactly two loop classes exist in the rotational configuration space

3. **Covering-space structure**
   - the double cover `SU(2) -> SO(3)` may be used when explicitly acknowledged
   - the closure order of a lifted mode is the minimal number of full circuits needed to return that lifted mode to identity

4. **Candidate Axiom 3 functional language**
   - the Family C information-theoretic coherence functional
   - `F_C = I(Phi_int; Phi_ext)`
   - stable PF modes are to be tested as extrema of this functional, not assumed by analogy

### Forbidden

1. Importing spinor behavior from external QFT as a premise.
2. Treating topological availability as physical realization by fiat.
3. Starting from any term equivalent to `(J_z - J_theta)^2`.
4. Reusing a generic "lowest wins" or minimal-Casimir argument.
5. Reusing the falsified faithfulness bridge.
6. Claiming the full fermion/boson distinction or the spin-statistics theorem in advance.

---

## 3. The Extremal Principle (Proof Obligation 1)

The hinge of the theorem is not topology alone. It is topology plus an Axiom 3 selection rule.

Take the PF-native Family C candidate:

`F_C[psi] = I(Phi_int; Phi_ext)`

where:

- `Phi_int` is the internal phase structure of the mode,
- `Phi_ext` is the external phase structure of the same mode,
- `I` is mutual information.

### Extremal principle

> A stable PF mode is a stationary point of `F_C` subject to the topological and causal constraints from Axioms 1-2.  
> A PF medium is in stable equilibrium only at a local maximum of `F_C`.

This is the exact mathematical form of the claim Echo's Lemma C needs. It separates the two jobs identified in `axiom3_coherence_functional_spec.md`:

1. **Threshold**: incoherent states do not produce stationary coherent structure.
2. **Selection**: among coherent states allowed by topology, the stable medium selects a local maximizer of `F_C`.

This avoids the banned shortcut of encoding the desired answer through a penalty term minimized at `k=1` or at `J_z = J_theta`.

---

## 4. "Available but Unpopulated = Strict Coherence Deficit" (Proof Obligation 2)

This section formalizes Echo's Lemma C in the Family C language.

### Step 1. Availability is topological

Because `pi_1(SO(3)) ~= Z_2`, the rotational configuration space has exactly two loop classes:

- the contractible class (`w = 1`)
- the nontrivial class whose lifted closure order is `w = 2`

So the weight-2 branch is **available** as a genuine topological sector of the PF configuration space.

### Step 2. Define the candidate deficit precisely

Let `s in {1,2}` label the two available closure-order sectors.  
For each available sector, let:

- `Phi_int^(s)` be the internal phase data on sector `s`
- `Phi_ext^(s)` be the external phase data on sector `s`

Encode the full medium by the direct-sum phase variables

`Phi_int^tot = (Phi_int^(1), Phi_int^(2))`

`Phi_ext^tot = (Phi_ext^(1), Phi_ext^(2))`

and define the sector-complete coherence score

`F_C^tot = I(Phi_int^tot; Phi_ext^tot)`.

If the medium populates only the weight-1 sector, then the score collapses to

`F_C^(1) = I(Phi_int^(1); Phi_ext^(1))`.

**Definition.**
A configuration is at a **strict coherence deficit** if its coherence score is strictly below the global maximum of `F_C^tot` over the available topological sectors.

### Step 3. Chain-rule lower bound and the extra hypothesis needed for strict increase

The two sector labels are not redundant copies of the same topology. They correspond to distinct loop classes in `SO(3)`: contractible versus non-contractible. In the Family C encoding, this means the full phase space contains an additional topologically independent phase sector when `s = 2` is populated.

Write

- `X_1 = Phi_int^(1)`
- `X_2 = Phi_int^(2)`
- `Y_1 = Phi_ext^(1)`
- `Y_2 = Phi_ext^(2)`

Then

`F_C^tot = I((X_1, X_2); (Y_1, Y_2))`

and

`F_C^(1) = I(X_1; Y_1)`.

By the mutual-information chain rule,

`I((X_1, X_2); (Y_1, Y_2)) = I(X_1; Y_1, Y_2) + I(X_2; Y_1, Y_2 | X_1)`

`= I(X_1; Y_1) + I(X_1; Y_2 | Y_1) + I(X_2; Y_1, Y_2 | X_1)`.

Therefore

`F_C^tot - F_C^(1) = I(X_1; Y_2 | Y_1) + I(X_2; Y_1, Y_2 | X_1) >= 0`

since conditional mutual information is always non-negative.

This is the mathematically valid information-theoretic statement that the sector-complete candidate score cannot be lower than the weight-1-only score once the state space is enlarged in this way.

To get a **strict** increase, an additional hypothesis is needed. A sufficient condition is:

> **A_NR (conditional non-redundancy of the weight-2 branch):**  
> `I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0`.

Using the chain rule once more,

`I(X_2; Y_1, Y_2 | X_1) = I(X_2; Y_1 | X_1) + I(X_2; Y_2 | X_1, Y_1)`.

So under `A_NR`,

`F_C^tot - F_C^(1) > 0`.

### Step 4. What is proved, and what is only bridged

The chain rule proves only the non-decrease

`F_C^tot >= F_C^(1)`.

It does **not** by itself prove a strict coherence deficit.

The strict statement

`F_C^tot > F_C^(1)`

requires an extra non-redundancy assumption such as `A_NR`. Topological distinctness of the two loop classes makes `A_NR` plausible, but this file does **not** derive `A_NR` from Axioms 1-3 alone or from any previously closed lemma.

So the correct status of Echo's Lemma C is now:

> **conjectural variational bridge**: if the available weight-2 branch carries coherent phase information not already fixed by the populated weight-1 branch, then leaving it empty is a strict coherence deficit in the Family C language.

### Step 5. Weight-1-only is therefore not proved to be maximal

What is proved:

- a weight-1-only configuration is not better than the sector-complete candidate under the direct-sum Family C encoding
- strict inferiority follows only if `A_NR` is true

What is **not** proved from the current axioms:

- that `A_NR` follows from topology plus Axioms 1-3
- that every available rotational branch must contribute non-redundant mutual information

So Proof Obligation 2 is sharpened but not closed.

### Step 6. Apply the extremal principle conditionally

By Section 3, stable PF media occur only at local maxima of `F_C` if the Family C extremal principle is the correct Axiom 3 selector.

Therefore the physical-realization bridge is conditional on **two** argued inputs:

1. the Axiom 3 extremal principle
2. the non-redundancy hypothesis `A_NR`

Under those extra assumptions:

> availability + strict coherence deficit + extremal principle => physical population of the weight-2 branch.

Without them, this section does not yet prove physical population.

No term of the form `(J_z - J_theta)^2` appears anywhere in this argument. The entire step is driven by topological sector distinctness plus the candidate Axiom 3 functional.

---

## 5. The `SU(2)` Lift Step (Proof Obligation 3)

This closes Break 2 from the 2026-03-28 Codex audit.

Let `p: SU(2) -> SO(3)` be the standard double cover.

### Step 1. What weight 2 means

A weight-2 mode is, by definition, a mode whose lifted rotational closure requires `4pi` rather than `2pi`.

Equivalently:

- after one `2pi` loop in `SO(3)`, the lifted mode has not yet returned to identity
- after two such loops (`4pi` total), it does

That is exactly the closure-order definition.

### Step 2. Why an `SO(3)`-only mode cannot do this

A mode defined only as an ordinary scalar/tensor field on `SO(3)` itself is single-valued on the base space. Traversing a `2pi` loop returns it to the same point of the base, so its closure order is `1`.

So an `SO(3)`-only mode cannot realize closure order `2`.

### Step 3. Why the weight-2 branch is the double-cover branch

The nontrivial loop in `SO(3)` lifts to an open path on `SU(2)` whose endpoint differs by the nontrivial deck transformation. Only after a second traversal does the lifted path close.

So any PF mode with closure order `2` must be single-valued on the lifted space, not on `SO(3)` alone. In that precise sense, it transforms on the `SU(2)` double cover.

Because `pi_1(SO(3)) ~= Z_2`, there is no third intermediate closure option. The only possibilities are:

1. trivial monodromy / closure order `1`
2. nontrivial lifted monodromy / closure order `2`

Hence:

> the weight-2 branch is exactly the `SU(2)`-lift branch.

This step uses only the closure-order definition plus standard covering-space structure. It does **not** derive the full relativistic spin-statistics theorem, and it does **not** import QFT spinors as a premise.

---

## 6. Formal Conditional Statement

**Formal conditional proposition.**

> In a 3D PF medium satisfying Axioms 1-3, with candidate coherence functional `F_C = I(Phi_int; Phi_ext)`:
>
> 1. `pi_1(SO(3)) ~= Z_2` guarantees two available closure-order classes with weights `1` and `2`.
> 2. The chain rule gives `F_C^tot >= F_C^(1)` for the direct-sum sector encoding.
> 3. If the Axiom 3 extremal principle holds **and** the weight-2 branch satisfies the conditional non-redundancy hypothesis `A_NR`, then `F_C^tot > F_C^(1)`.
> 4. Under those additional assumptions, a weight-1-only configuration is unstable and the weight-2 branch must be physically populated.
> 5. Any genuinely populated weight-2 mode necessarily transforms on the `SU(2)` double cover.
> 6. Therefore the full physical realization of `(2,1)` would follow once the extremal-principle bridge and `A_NR` are derived.

---

## 7. Honest Assessment and Remaining Gaps

| Step | Status | Notes |
|------|--------|-------|
| Two topological classes from `pi_1(SO(3)) ~= Z_2` | Derived | Standard topology |
| Extremal principle from Axiom 3 | Argued | `F_C` is a candidate functional, not yet Codex-audited against the acceptance tests |
| Coherence deficit of a weight-1-only medium | Argued | Chain rule gives only non-decrease; strict increase requires the extra hypothesis `A_NR` |
| `SU(2)` lift step | Derived (conditional) | Follows from closure-order definition plus covering-space structure once a weight-2 mode is admitted |
| Full fermion/boson distinction | Not claimed | Downstream identification still requires extra structure |
| Spin-statistics theorem | Not claimed | Requires additional relativistic / field-theoretic structure |

**Strongest honest statement after this file:**

PF now has a bounded theorem attempt for the physical-realization gap. The topology is exact, the `SU(2)` lift step is clean once closure order `2` is admitted, and Echo's Lemma C has been sharpened to a precise missing bridge. What remains open is exact: Axiom 3 must supply both the extremal principle and a derivation of the conditional non-redundancy hypothesis `A_NR`. Without those, Section 4 is heuristic/argued rather than theorem-grade.

---

## 8. Codex Audit Result

**Audit artifact**: `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`

**Verdict summary**:
1. `F_C = I(Phi_int; Phi_ext)` is **not signed off** as an accepted Axiom 3 functional for T1; it remains a candidate language.
2. The coherence-deficit step is **not** a strict proof. After the Section 4 correction, the chain rule proves only non-decrease; strict increase still depends on the extra hypothesis `A_NR`.
3. The `SU(2)` lift step **does survive audit** as a conditional covering-space statement and does not import hidden QFT structure.

**Board result**: T1 remains `PARTIAL DERIVATION 0.85`. The new file sharpens the missing bridge but does not close it.
