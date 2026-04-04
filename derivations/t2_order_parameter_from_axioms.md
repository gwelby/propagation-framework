# T2 Order Parameter From Axioms

**File ID**: T2-OPAX-001  
**Purpose**: Answer the Agent 3 brief directly: derive the PF order parameter from Axioms 1-3, or show that this cannot be done from the current axioms alone. [CITATION NEEDED]  
**Status**: NO-GO (axioms alone) - the current axioms do not derive a unique PF order parameter, a nonzero condensate, or the translation-invariant structure needed for the T2 co-dimension route; T2 remains `PARTIAL DERIVATION 0.85`. [CITATION NEEDED]  
**Author**: Codex (2026-04-04)  
**Primary inputs**:
- `FIVE_AGENT_COORDINATION.md`, Agent 3 brief. [CITATION NEEDED]
- `derivations/t2_denominator_theorem_audit_2026-03-31.md`. [CITATION NEEDED]
- `derivations/axiom3_coherence_functional_spec.md`. [CITATION NEEDED]
- `CLAIMS.md`. [CITATION NEEDED]
- `the_propagation_framework.md`. [CITATION NEEDED]

---

## 0. Ingest Note

Per `AGENTS.md`, a WARP query was attempted before writing. [CITATION NEEDED] The local ingest requirement was followed, but the query tool could not complete because the environment is offline and `warp_query.py` attempted to fetch Hugging Face assets. This file therefore uses local-source ingest only.

---

## 1. Exact Question

The 2026-03-31 T2 audit isolates Break 1 cleanly:

> the PF order parameter is still an ansatz, not a derivation. [CITATION NEEDED]

Agent 3 asks five narrower questions: whether Axiom 3 alone can force a condensate, whether a Landau-type broken-symmetry argument is available, whether the coherence functional can define the order parameter, whether a three-mode Goldstone route can be derived without assuming a scalar field, and whether translation invariance follows from Axiom 1. [CITATION NEEDED]

This file answers those questions at the current audit standard. It does not upgrade T2 and does not reuse the older `ARGUED (0.72)` companion as a closure claim. [CITATION NEEDED]

---

## 2. What Axioms 1-3 Actually Force

Using only the canonical three axioms, one can justify the following minimal statements. [CITATION NEEDED]

### 2.1 Axiom 1 forces a local state-carrying medium

If propagation is fundamental, the medium must carry some local state:

`s(x,t) in S`

for some state space `S`.

This is a structural requirement only. Axiom 1 does not specify:

- the dimension of `S`,
- whether `S` is real, complex, spinorial, tensorial, or nonlinear,
- whether the vacuum value of `s` vanishes,
- whether the relevant order parameter is `s` itself or some coarse-grained function of `s`.

### 2.2 Axiom 2 forces finite-speed phase-capable dynamics

Finite causal velocity requires propagating modes with finite-speed signal transport. A wave-like description therefore needs at least a cyclic or phase-like local degree of freedom in addition to magnitude.

That supports a minimal amplitude-plus-phase description, but it does not uniquely select:

- `C` over `R^2`,
- a scalar over a multi-component field,
- a field over a matrix-valued order parameter,
- a momentum-space description over a purely configuration-space description.

So Axiom 2 supports "phase-capable local structure" but not a unique order-parameter manifold.

### 2.3 Axiom 3 gives a threshold, not an ordering theorem

The current Axiom 3 formulation distinguishes coherent structure from incoherent dispersion, but the current formal state of the framework does not yet provide a selector over multiple coherent candidates. The coherence-functional specification says this explicitly: PF still lacks the mathematical object that orders coherent states and picks the fundamental one. [CITATION NEEDED]

That matters here because a nonzero condensate is not just a threshold statement. It is a selection statement:

- why one vacuum manifold is chosen rather than another,
- why the selected vacuum is nonzero rather than zero,
- why the selected field should be scalar rather than spinor or tensor.

Current Axiom 3 does not yet answer those questions. [CITATION NEEDED]

---

## 3. Exact No-Go

### Theorem 3.1

From Axioms 1-3 alone, one cannot derive all of the following:

1. a unique PF order-parameter type,
2. a field of the form `Psi : R^3 x R -> C`,
3. a nonzero vacuum expectation value `|Psi_vac| = rho_0 > 0`,
4. a Landau-style broken-symmetry pattern `G -> H`,
5. the translation-invariant momentum-space condition `C_mom`.

### Proof

**Step 1: representation underdetermination**

Axiom 1 requires only that the medium carry local state. Axiom 2 requires only that the state admit finite-speed phase-capable propagation. Neither axiom fixes the representation type of that state.

So the following are all compatible extensions of the axioms:

- a scalar amplitude-phase field,
- a two-component complex branch field,
- a phase-invariant coherence tensor,
- other higher-component coherent state spaces.

The axioms do not contain a rule selecting one of these state spaces over the others.

**Step 2: no condensate theorem from current Axiom 3**

To prove `|Psi_vac| > 0`, one needs a principle that excludes a zero-background medium with coherent excitations around it. Current Axiom 3 does not do that. The March 31 audit states that a nonzero condensate vacuum was assumed rather than derived, and the coherence-functional specification states that PF still lacks the ordering object needed to choose among coherent states. [CITATION NEEDED]

So a nonzero condensate is not presently derivable from the axioms alone.

**Step 3: no Landau theorem**

A Landau-style route requires, at minimum:

- an explicit continuous symmetry group `G`,
- an order-parameter representation on which `G` acts,
- a functional or dynamics whose minima define the vacuum,
- a proof that the vacuum lies on a nontrivial orbit `G/H`.

The current axioms provide none of these objects explicitly. Therefore they do not yield a broken-symmetry theorem, Goldstone count, or Higgs-style restoration count by themselves. [CITATION NEEDED]

**Step 4: no translation-invariance theorem**

Propagation everywhere does not imply a homogeneous medium. A heterogeneous medium can propagate signals while lacking global translation invariance. Therefore Axiom 1 does not imply momentum conservation or Fourier labeling of modes, and `C_mom` remains extra structure. The March 31 audit names this directly. [CITATION NEEDED]

Since Steps 1-4 block each item in the claim list above, the order parameter is underdetermined by the current axioms. QED.

### Corollary 3.2

The strongest honest conclusion is not "the scalar order parameter is derived but bounded." The stronger honest conclusion is narrower:

> the current axioms justify only phase-capable coherent medium states in some local state space; they do not yet derive the order-parameter manifold, its vacuum value, or the symmetry structure needed for T2. [CITATION NEEDED]

---

## 4. Consequences For The Five Agent 3 Questions

### Q1. Can Axiom 3 alone force a nonzero condensate expectation value?

No.

Current Axiom 3 says coherent structures persist and incoherent ones disperse. That is not enough to prove that the vacuum must satisfy `|Psi_vac| > 0`. A zero-background medium can still support coherent propagating excitations unless an additional selector principle forbids it. The current framework does not yet contain that selector. [CITATION NEEDED]

### Q2. Is there a Landau-type argument from coherence to broken symmetry to order parameter?

Not from the current axioms alone.

Such an argument needs a symmetry group, an order-parameter representation, and a vacuum-selection functional. Those are not yet derived from Axioms 1-3. So the Landau route is available only as an extra model layer, not as an axiomatic theorem. [CITATION NEEDED]

### Q3. Can the coherence functional `F_C` itself define the order parameter?

Not yet.

The coherence-functional specification states that this is exactly the missing mathematical object PF still needs. Until `F_C` is actually constructed and shown to select a unique nonzero vacuum, it cannot be used as evidence that the order parameter has been derived. [CITATION NEEDED]

### Q4. Can the denominator `M = 3` come from three Goldstone modes without assuming a scalar field?

Not at the current stage.

Even if one avoids a scalar-field ansatz, the same missing pieces remain:

- what the order parameter is,
- what symmetry acts on it,
- what subgroup remains unbroken,
- why the resulting broken directions are the relevant massive restoration modes.

So the Goldstone route is not closed by replacing the scalar with more abstract coherence language. It still needs a real `G -> H` theorem and dynamics. [CITATION NEEDED]

### Q5. Can translation invariance be derived from Axiom 1?

No.

Axiom 1 says the medium carries propagation. It does not say the medium is homogeneous. Therefore translation invariance, conserved momentum, and the `H(k)` framing remain conditional inputs. [CITATION NEEDED]

---

## 5. Minimal Extra Structure Needed

If later work wants an actual PF order parameter rather than an honest no-go, the minimal additional structure should be named explicitly.

### 5.1 Minimal scalar-route assumptions

To obtain a scalar order parameter of the form

`Psi : R^3 x R -> C`

one must add at least:

**OP-1**: a representation choice stating that the minimal coherent local state is a complex line field rather than `R^2`, `C^2`, or a tensor field.

**OP-2**: an Axiom-3 selector functional `F[Psi]` or equivalent dynamics whose stable vacuum satisfies `|Psi_vac| = rho_0 > 0`.

**OP-3**: a homogeneity assumption sufficient to justify translation invariance and `C_mom` when the T2 route moves to momentum space.

Without all three, the scalar route is still model choice, not theorem.

### 5.2 Minimal T1-aware route

If one grants the conditional T1 statement that the physical weight-2 branch is locally two-component, then the natural phase-invariant local object is not obviously a scalar. The April 1 follow-up note argues that the cleaner candidate is the traceless coherence tensor

`Q in Herm_0(2) ~= R^3`

rather than a single complex scalar. [CITATION NEEDED]

That route still needs:

**OP-T1**: the T1 physical-realization bridge.

**OP-T2**: a selector functional for the local coherence tensor.

**OP-T3**: a theorem connecting that tensor dynamics to the defect or momentum-space structure used in T2.

So even the stronger tensor route is conditional, not axiomatic.

---

## 6. Strongest Honest Statement For T2

Use the following wording if this file is cited elsewhere:

> Codex note (2026-04-04): Axioms 1-3 do not yet derive a unique PF order parameter. They justify only that the medium must carry phase-capable local states and that stable structure requires coherent dynamics. They do not yet prove a scalar field `Psi`, a nonzero condensate vacuum, a Landau symmetry-breaking pattern, or the translation-invariant momentum-space assumption `C_mom`. Therefore the PF order parameter remains an extra model layer, and T2 stays `PARTIAL DERIVATION 0.85`. [CITATION NEEDED]

---

## 7. Bottom Line

The order-parameter question is presently underivable from the three axioms alone.

What survives:

- PF needs a local state space that can carry coherent phase-capable propagation.
- PF still needs an Axiom-3 selector functional.
- T2 still needs named extra structure before the co-dimension route can close.

What does not survive:

- "Axioms 1-3 derive `Psi : R^3 x R -> C`."
- "Axiom 3 alone forces `|Psi_vac| > 0`."
- "Translation invariance follows from propagation."
- "The Goldstone count is already axiomatic."

That is the honest boundary as of 2026-04-04. [CITATION NEEDED]
