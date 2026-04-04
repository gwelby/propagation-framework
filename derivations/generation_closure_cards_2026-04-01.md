# Generation Closure Cards (2026-04-01)
*Hostile-compression cards for the T1 and T2 load-bearing bridges*

**Status**: Planning / closure map  
**Purpose**: Force the generation front into short-form theorem language that can close or fail cleanly.  
**Truth sources**: `CLAIMS.md`, `ACTIVE_ISSUES.md`, `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`, `derivations/t2_denominator_theorem_audit_2026-03-31.md`, `derivations/t1_t2_post_audit_epic_2026-03-31.md`

---

## How To Use These Cards

Each card should answer, in a few lines:

- what the theorem claim is
- what the live status is
- what survives right now
- what exact bridge is still missing
- what the shortest route to closure is
- what the shortest route to failure is

If a future draft cannot improve one of those lines, it is probably not real progress.

---

## Card T1

### Claim

PF must physically realize the available weight-2 branch, not merely allow it topologically.

### Live Status

`PARTIAL DERIVATION 0.85`

### What Survives

- `pi_1(SO(3)) ~= Z_2` gives a real two-class closure-order structure
- the minimal closure orders are `1` and `2`
- if a genuine weight-2 rotational mode is physically admitted, it lives on the `SU(2)` lift rather than on `SO(3)` alone

### Exact Missing Bridge

- why Axiom 3 selects the candidate Family C ordering language at all
- why the available weight-2 branch contributes conditionally non-redundant coherent content
- why leaving that branch empty is a strict coherence deficit rather than merely a lower bound

In present notation, the chain rule gives only:

`F_C^tot >= F_C^(1)`

The strict step still depends on the extra hypothesis:

`A_NR: I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0`

### Why It Matters

Without T1, the numerator theorem for the three-generation lock never becomes physical.
The algebra may still be elegant, but the medium has not been shown to realize the required branch.

### Shortest Route To Closure

1. Use the selector note to decide whether Family C is a PF-native selector or just a suggestive model language.
2. If Family C survives, derive the extremal principle rather than assuming it.
3. Derive `A_NR` or replace it with a stronger PF-native lemma that yields strict deficit without smuggling.
4. Classify alternative branch-population patterns as forbidden, metastable, composite, or merely lower-scoring.

### Shortest Route To Failure

- exhibit a stable PF-consistent weight-1-only medium with an available weight-2 branch and no strict coherence deficit
- or show that any T1 selector strong enough to force branch population must add information not present in Axioms 1-3

### Do Not Say Yet

- "fermion/boson distinction is fully derived"
- "spin-statistics is derived"
- "the weight-2 branch is forced by topology alone"

---

## Card T2

### Claim

PF fixes the denominator theorem `M = 3` from its own coherence-field dynamics rather than from imported condensed-matter structure.

### Live Status

`PARTIAL DERIVATION 0.85`

### What Survives

Inside the local `2x2` Fermi-point Hamiltonian ansatz,

`H(k) = h_0(k) I_2 + h(k) · sigma`

the following are exact:

- a generic band-touching point in `R^3` has codimension `3`
- the gap-opening perturbation space is the real span of `{sigma_1, sigma_2, sigma_3}`
- that perturbation space has dimension `3`

This is a useful conditional lemma.
It is not yet the PF denominator theorem.

### Exact Missing Bridges

The live bridge list is now explicit:

- **OP-1a**: `C` is natural packaging for the order parameter, but not uniquely forced over `R^2`
- **OP-2**: nonzero coherent mean field is a plausible Axiom 3 reading, not yet a strict consequence
- **C_mom**: the PF medium must admit a translation-invariant momentum-space description
- **C_FP**: the PF weight-2 sector must actually contain Fermi points
- **C_bridge**: the three Pauli gap directions must be proved to be the three massive bosonic restoration modes of the PF coherence field

### Why It Matters

Without T2, the denominator in the generation lock remains model-dependent.
That keeps the `N = 3` result conditional even if the algebra after numerator-plus-denominator is exact.

### Shortest Route To Closure

There are only two serious options.

**Option A: stay in the Fermi-point language**

- derive or explicitly adopt the PF order parameter with honest scope
- derive `C_mom` and `C_FP` from PF dynamics rather than importing them
- give the PF coherence field a native local dynamics that makes `C_bridge` an actual theorem

**Option B: abandon the Fermi-point language**

- stop trying to inherit `M = 3` from the Volovik template
- derive a PF-native denominator count directly from coherence-field structure
- only return to `M = 3` once the count is native to PF rather than to the ansatz

### Shortest Route To Failure

- prove that the PF weight-2 sector need not admit the momentum-space / Fermi-point description at all
- or prove that the three algebraic gap directions do not map to three independent physical restoration modes

Either result would kill this route honestly and prevent more analogy-driven overreach.

### Do Not Say Yet

- "`M = 3` is derived"
- "three generations follow from topology" without naming the T1 and T2 blockers
- "the Volovik analogy closes the theorem"

---

## Order Between The Cards

The clean order is:

1. selector work
2. T1 closure
3. T2 closure

T2 may still advance locally in parallel, but the repo should not pretend the broader generation stack is downstream-complete while T1 still lacks a physical-population theorem.

---

## Strongest Honest Summary

The generation front is not blocked by vague mystery anymore.
It is blocked by named bridges.

That is progress.

The next gain will not come from finding more beautiful language for `N = 3`.
It will come from either closing these cards or killing one of them cleanly.
