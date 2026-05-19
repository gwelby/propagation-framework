# Selection Boundary Synthesis
*Cross-front pattern behind G3, T1/T2, and Koide*

**Date**: 2026-05-08  
**Status**: SYNTHESIS / RESEARCH DIRECTION — not a theorem, not a claim upgrade  
**Inputs**: `CLAIMS.md`, `ACTIVE_ISSUES.md`, `WHATS_NEXT.md`, `derivations/axiom3_selector_note_2026-04-01.md`, `derivations/generation_closure_cards_2026-04-01.md`, `derivations/g3_closure_card_2026-04-01.md`, `derivations/h_prod_joint_model_obligation.md`, DeepSeek survey `D:\DeepSeek\REPORTS\DEEPSEEK_20260508_PROPAGATION_FRAMEWORK_SURVEY.md`, DeepSeek response `D:\DeepSeek\REPORTS\DEEPSEEK_20260508_SELECTION_BOUNDARY_RESPONSE.md`

---

## 1. The Pattern

The current open physics fronts share the same structural form:

> PF topology/geometry identifies an arena of admissible coherent structures, but Axioms 1-3 do not yet always supply the dynamical selection rule that says which admissible structure is physically realized, populated, basis-fixed, independent, or phase-selected.

This is not a failure of the existing audits. It is the thing the audits have made visible.

| Front | Arena Derived | Missing Selector / Realization Bridge |
|-------|---------------|----------------------------------------|
| **T1** | `pi_1(SO(3)) ~= Z_2`; closure orders `1` and `2`; SU(2) lift for the nontrivial branch | `A_NR`: why the available weight-2 branch carries non-redundant coherent information and must be physically populated |
| **T2** | local `2x2` Fermi-point ansatz gives codimension `3` and three Pauli gap directions | `C_mom`, `C_FP`, `C_bridge`: why PF has that momentum/Fermi-point realization and why three perturbation directions are three massive restoration modes |
| **G3 / H_prod** | genuine `Z_3` internal sector and circulant closure operators | Markov/minimal-state bridge, primitive operator selection, and a one-medium joint probability model with actual factorization |
| **Koide phase** | charged-lepton Koide amplitude geometry and `Z_3` phase arena | PF-native selector for `delta = 2/9`; all audited Casimir/RG/character/Chebyshev/proxy routes have failed |

The signature is consistent: topology gives **availability**; the missing theorem gives **realization**.

---

## 2. What This Does Not Mean

This does **not** justify adding a broad new axiom like "the universe selects the simplest option."

The repo already learned the correct discipline from Axiom 3b:

- A selector can be accepted when it is bounded.
- It must name its domain.
- It must say what is varied and what is fixed.
- It must define the ordering object.
- It must state falsifiers.
- It must survive Codex-style hostile audit.

So the next step is not "Axiom 4."  
The next step is a **selector contract**.

---

## 3. Selector Contract

Any proposed selector should be forced into this form:

```text
Selector S = (D, F, R, V, X)

D = domain of admissible PF candidates
F = PF-native functional, score, or partial order
R = realization rule: selected / excited / metastable / forbidden / unpopulated
V = verification gate: analytical check or script showing F on D actually produces R
X = falsifier: what result kills this selector
```

Minimum requirements:

1. **Domain**: fixed labels, topology, symmetry, and admissible candidate family.
2. **Functional**: not target-loaded; not equivalent to the desired answer by definition.
3. **Realization rule**: says what happens to candidates that are coherent but not selected.
4. **Verification gate**: a small check, preferably analytical or scripted, that tests whether the proposed `F` on the stated `D` produces the claimed `R` before Codex audit.
5. **Falsifier**: one counterexample or numerical result that would kill the route.

If a proposal cannot fill these five slots, it should not modify theorem language.

`V` is not a replacement for hostile audit. It is a local self-audit step. The historical proxy potential and Chebyshev cubic routes would have failed faster if they had been forced to state, before interpretation, what verification result would count as success.

---

## 4. Three Candidate Selector Classes

These are research targets, not accepted principles.

### S1. Extremal Coherence Selector

Candidate form:

> Stable PF realizations are local maxima of a PF-native coherence functional under fixed topology and causal constraints.

Where it may help:

- T1: decide whether `F_C = I(Phi_int; Phi_ext)` is a real PF selector, and whether unpopulated weight-2 is a strict coherence deficit.
- G3 Obligation 1: support a minimal full-state / Markov argument if extremal coherence forces all relevant coherent variables into the local state.

Risk:

- `F_C` may be a useful model language but not derivable from Axiom 3.
- Local maxima may exist that do not populate the desired branch.

Falsifier:

- A stable PF-consistent weight-1-only medium with no strict coherence deficit despite an available weight-2 branch.

Verification gate:

- Write a toy or analytical model of the two-sector state space and compute whether the proposed `F_C` strictly increases when the weight-2 branch carries independent phase data, while also checking whether any coherent weight-1-only local maximum survives.

### S2. Minimal Sufficient State Selector

Candidate form:

> The physically realized local state is the minimal sufficient statistic for future coherent evolution. Hidden memory variables must either be included in the state or shown dynamically irrelevant.

Where it may help:

- G3/H_prod Markov obligation: turns "Axiom 2 gives locality" into a sharper state-completeness question.
- T2: can test whether the Fermi-point state variables are PF-native or merely ansatz variables.
- T1 fallback: if S1 cannot derive an ordering functional from Axiom 3, S2 may still prove a weaker state-completeness result without claiming that one branch is "better" than another.

Risk:

- This may close state completeness but still not produce independence or phase selection.
- This may be too weak for `A_NR`, because `A_NR` needs non-redundant coherent content, not merely a complete state vector.

Falsifier:

- A PF evolution where hidden memory affects future closure events while all proposed local variables remain fixed.

Verification gate:

- Construct two local-state encodings with identical proposed coarse variables and different hidden histories. If future closure probabilities differ, the coarse state is not sufficient and the selector fails in that domain.

### S3. Degeneracy-Breaking Vacuum Selector

Candidate form:

> When topology leaves a degenerate coherent subspace, the physical vacuum or lowest-order PF interaction term selects a basis, phase, or branch by breaking the degeneracy.

Where it may help:

- G3 noncanonical Family C: `H_basis` asks why one basis inside the degenerate `Q` sector is selected.
- Koide phase: the missing selector is likely a vacuum/interaction term that picks `delta = 2/9` inside the already-derived `Z_3` phase arena.
- Path A: any real `b/a -> 0` route must derive an interaction that distinguishes `S` from `S^2`.

Risk:

- The required term may be new physics beyond Axioms 1-3.
- If inserted by hand, it repeats the failed `kappa * winding` problem.

Falsifier:

- The lowest-order PF-native interaction remains fully symmetric in the target subspace, or selects a value different from the claimed physical one.

Verification gate:

- Compute the lowest-order allowed interaction on the stated degenerate subspace and verify that its extrema select the claimed basis, branch, or phase without inserting that target into the interaction.

---

## 5. The Correct Work Order

The cross-front insight changes the work order:

1. Do not chase all four fronts independently.
2. Do not add a general selector axiom.
3. Write one selector contract for one bounded domain.
4. Run it through Codex audit.
5. Only then apply the surviving contract to a load-bearing front.

Primary track:

> T1 / `A_NR`, because it is the cleanest expression of the availability-versus-realization gap and does not require the full G3 probability model.

Parallel fallback track:

> S2 / minimal-sufficient-state on G3 Obligation 1, because it can sharpen the Markov step without requiring a global ordering functional. This is the fallback if S1 cannot derive `F` from Axiom 3 in a way that survives audit.

Do **not** start with Koide unless a genuinely new PF-native phase selector is proposed. The obvious scalar/matrix/character/Casimir/RG routes are already fenced.

---

## 6. Strongest Honest Summary

The Propagation Framework is not blocked because it lacks topology.

It is blocked because topology tells us what can exist, while the open fronts require a theorem saying what the medium actually realizes.

That theorem cannot be vague. It must be a bounded selector contract:

```text
domain -> PF-native functional -> realization rule -> verification gate -> falsifier
```

If that contract closes for one front, the same pattern can be tested elsewhere.
If it fails, the framework still becomes sharper because the boundary is now named.

No confidence score changes from this note.
