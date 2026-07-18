# Reading Order: The Propagation Framework

**Last updated:** 2026-06-29

This repository is active research, not a finished public release. Some results
are machine-checked or derived, several are conditional, and some older
enthusiastic summaries are now superseded. Start with the live truth surfaces
before reading narrative derivations.

## 0. Current Truth First

1. **[CLAIMS.md](./CLAIMS.md)** - the live claim scoreboard, confidence tiers,
   falsifiers, and June 29 PfLean alignment patch. This file governs public or
   release-facing claim status.
2. **[ACTIVE_ISSUES.md](./ACTIVE_ISSUES.md)** - current blockers, public-HOLD
   state, and next allowed work.
3. **[RESUME.md](./RESUME.md)** - latest handoff for this workspace. Read this
   before editing or auditing.

Use this rule: if a derivation, manuscript, README, or generated artifact
conflicts with these files, treat the derivation or artifact as stale until it
is reconciled.

## 1. Plain-Language Entry

1. **[EXPLAINER.md](./EXPLAINER.md)** - conceptual entry point.
2. **[UNDERSTAND.md](./UNDERSTAND.md)** - the framework told at multiple levels.
   Read the 2026-06-29 current-truth note at the top before relying on older
   sections.
3. **[README.md](./README.md)** - repository overview and headline status.

## 2. Canonical Foundations

1. **[the_propagation_framework.md](./the_propagation_framework.md)** - the
   three core axioms.
2. **[theory_of_propagation.md](./theory_of_propagation.md)** - expanded
   conceptual framework.
3. **[definitions/README.md](./definitions/README.md)** - canonical definition
   index.

## 3. Formal And Audited Mathematics

1. **[lean/README.md](./lean/README.md)** - current Lean module map and proof
   boundary notes.
2. **[lean/PREMISE_LEDGER.md](./lean/PREMISE_LEDGER.md)** - H1-H18 premise
   accounting, including H17 matrix symmetry and H18 equal row sums.
3. **[lean/PfLean/Axioms.lean](./lean/PfLean/Axioms.lean)** - source truth for
   named hypotheses and real `sorry` versus `True := by trivial` scaffolding.
4. **[lean/PfLean/Z3FromBareMedium.lean](./lean/PfLean/Z3FromBareMedium.lean)**
   - D=3 uniqueness, D>=4 counterexample, degenerate-residue boundary, and the
   D-selection principle.
5. **[lean/PfLean/Entropy.lean](./lean/PfLean/Entropy.lean)** - PFEntropy as
   downstream J-I cooling evidence, not an upstream selector.

## 4. Core Derivations And Audits

1. **[derivations/koide_geometric_equivalence.md](./derivations/koide_geometric_equivalence.md)**
   - Koide geometric identity; physical vacuum selection remains separate.
2. **[derivations/topological_weight_from_propagation.md](./derivations/topological_weight_from_propagation.md)**
   - topology route; physical realization remains conditional.
3. **[derivations/g3_coupling_bridge.md](./derivations/g3_coupling_bridge.md)**
   - historical God Equation bridge context. Check `CLAIMS.md` first because
   the live status is split: Postulate-D operator algebra is conditional and the
   lambda scale formula is argued.
4. **[papers/FALSIFICATION_PAPER_DRAFT.md](./papers/FALSIFICATION_PAPER_DRAFT.md)**
   - falsification framing.

## 5. Empirical And Executable Checks

1. **[sandbox_results.md](./sandbox_results.md)** - empirical and executable
   results log.
2. **[sandbox/](./sandbox/)** - local verification scripts and exploratory
   probes.
3. **[verification/README.md](./verification/README.md)** - verification index.

## Current High-Risk Reading Rules

- Do not call the Weinberg angle `DERIVED`; live status is `ARGUED 0.65`.
- Do not call the God Equation scale formula `DERIVED`; live status is split:
  Postulate-D Z3 operator algebra is `CONDITIONAL 0.88`, and the lambda scale
  formula is `ARGUED 0.60`.
- Do not say symmetry is derived from bare propagation. H17 matrix symmetry and
  H18 equal row sums are explicit premises in the current Lean stack.
- Treat PFEntropy as downstream evidence of J-I cooling, not proof that entropy
  alone forces J-I.
- Fundamentals PUBLIC HOLD remains active until Codex explicitly lifts it.
