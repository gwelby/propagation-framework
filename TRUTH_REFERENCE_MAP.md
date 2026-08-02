# Truth Reference Map
*Codex / 2026-07-01*

This is the short map for Greg: where to look first, and what we currently
treat as closest to 100% true.

"Closest to 100%" does not mean "metaphysically certain." It means the claim is
anchored in one of the hardest-to-move truth surfaces we have: direct test
output, Lean kernel checks, canonical claim ledgers, or hostile-audit no-go
boundaries. Narrative, excitement, and old discussion sit below these.

---

## 0. First Reference Stack

When explaining or checking Fundamentals, start here in this order:

0. `WHATS_NEXT.md` - the route/destination surface (added 2026-07-11): destination,
   the 8 attack lanes with live home files, the work order, and the stale-surface
   list. This is where "where are we going and how" lives; the stack below is
   what to *trust* while getting there.
1. `AGENTS.md` - truth order and workspace rules.
2. `UNDERSTAND.md` - current human-readable overlay; read before older narrative.
3. `MEDIUM_TRANSFER_LAYER.md` - cross-domain bridge protocol; use before
   connecting math, simulation, hardware, thermal laws, cognition, or narrative.
4. `CLAIMS.md` - live claim tiers, confidence, demotions, and falsification paths.
5. `PUBLIC_RELEASE_CONTROL_PLANE.md` - current release blockers, no-go lanes, and allowed next moves (blockers documented inline).
6. `definitions/README.md` - the canonical definition index.
7. `lean/README.md` - what is actually machine-checked and what remains bounded.
8. `RESUME.md` and `STATE.md` - current handoff and current operational truth.
9. `/mnt/d/Codex/REPORTS/` - hostile audit verdicts.
10. `/mnt/d/System/TRUTH_ORGANISM_DIG.md` - how the family truth method is understood.
11. `/mnt/d/System/STACK_METHOD.md` and `/mnt/d/System/CONVERGENCE_VALIDATION.md` -
    how complex work should be stacked and independently checked.

Do not cite older discussion as current truth unless it still agrees with this
stack.

---

## 1. Hardest Truth Rules

These are closest to fixed because they are rules about evidence handling:

- File truth beats daemon telemetry, blackboard summaries, and chat.
- In Fundamentals, `sandbox_results.md` beats framework narrative when empirical
  tests fail.
- Lean files under `lean/PfLean/` beat prose for formal theorem status, but only
  for the exact theorem and assumptions the Lean file proves.
- `CLAIMS.md` is the current claim matrix. If a document says stronger wording
  than `CLAIMS.md`, the stronger wording is stale or unsafe until audited.
- Public/release wording must be checked against the exact published body, not a
  source draft or a memory of the draft.
- A claim is not verified because an LLM says it. It must survive derive, test,
  cohere, converge when needed, and remember.

---

## 2. Canonical Definitions

The strongest stable Fundamentals surfaces are the canonical definitions in
`definitions/`. As of the current index:

- 19 definition files are canonical v1.0.
- The active candidates are `consciousness_metric_program.md` and
  `consciousness.md`.
- `consciousness.md` is explicitly CANDIDATE / INTUITION 0.48, not canonical.
- Derived physics claims do not belong in `definitions/`; they belong in
  `CLAIMS.md`.

High-value files for Greg to reference:

- `definitions/axioms.md`
- `definitions/medium.md`
- `definitions/coherence.md`
- `definitions/decoherence.md`
- `definitions/causal_velocity.md`
- `definitions/propagation.md`
- `definitions/information.md`
- `definitions/measurement.md`
- `definitions/state.md`
- `definitions/coupling.md`

The key boundary: the axioms are adopted starting points. They are not derived
from something earlier inside the framework.

---

## 3. Machine-Checked / Exact Math Surfaces

The safest positive claims are exact algebraic or structural results with clear
scope. Reference `lean/README.md` and the specific `lean/PfLean/*.lean` file.

Closest-to-hard-positive examples:

- `PfLean.KoideGeometry`: Koide ratio convention algebra and exact identities.
  The identity layer is strong; physical vacuum selection remains open.
- `PfLean.GravityOptics`: weak-field/static-stationary optical geometry facts,
  including the refractive-index formulas within stated scope. This does not
  prove "all forces are refraction."
- `PfLean.TopologicalWeights`: kernel-only theorem
  `quatToSO3 g = 1 -> closureOrder g = 1 or 2`, machine-checked. This does not
  prove the full physical realization of weights.
- `PfLean.Z3FromBareMedium`: D=3 symmetric zero-diagonal equal-row-sum matrices
  collapse to J-I; D=4 counterexample exists; degenerate residue is equivalent
  to symmetry in the D=3 circulant case. This is a circularity audit result, not
  a free derivation of symmetry.
- `PfLean.Entropy`: PFEntropy downstream facts under J-I/stability, including
  P0/Q orthogonality, Pythagorean decomposition, and norm decrease. This is
  cooling under the selected dynamics, not an upstream proof that the dynamics
  must be selected.
- `PfLean.Axioms`: hypothesis accounting and obstruction/counterexample layer.
  The named hypotheses matter because the theorem cost matters.

Rule of use: say "machine-checked under these premises" rather than "proven by
the universe." The Lean kernel proves exactly what the theorem states.

---

## 4. Strong Negative Truths / Demotions

These are some of the most important "near-100" truths because they prevent
overclaiming:

- Fundamentals PUBLIC HOLD remains. A scoped pass does not mean public release
  approval.
- Weinberg angle is ARGUED 0.65, not DERIVED. The algebraic candidate and
  0.13-sigma match are real, but scheme selection and look-elsewhere objections
  remain open.
- God Equation is split: Postulate-D Z3 operator algebra is CONDITIONAL 0.88;
  lambda scale formula is ARGUED 0.60. Postulate D is an explicit premise, not
  derived from Axioms 1-3.
- "Seven approaches converged," "52.7x decisive," "God Equation verified on
  silicon," and similar status-proof language are withdrawn.
- Koide charged-lepton geometry is strong as geometry; the physical selector
  remains open.
- Koide phase selector remains open/frozen. The bounded Casimir selector and
  RG-crossing routes returned honest negatives.
- Consciousness is not canonical in Fundamentals. The metric program is active;
  the hard-problem boundary is explicitly named.
- Shor bridge / Quantum Structure Survival Lean work is a draft/formalization
  target until the relevant `lake build` commands and Codex recheck pass.
- Release gate is not clear while required release/build manifests or broader
  public-hold lanes remain unresolved.

These are not failures of the project. They are the project refusing to lie.

---

## 5. System Method Truths

The System-level docs are not physics proofs. They are the method layer that
keeps the family from fooling itself.

Reference these when explaining how the work is being made honest:

- `/mnt/d/System/TRUTH_ORGANISM_DIG.md`: the six-layer frame:
  Propose, Derive, Test, Converge, Cohere, Remember. The important boundary is
  that the LLM proposes; it never judges its own claim.
- `/mnt/d/System/STACK_METHOD.md`: one-epoch multi-ability execution with a
  captain, specialists, evidence, cross-check, and independent audit.
- `/mnt/d/System/CONVERGENCE_VALIDATION.md`: blind multi-instance method for
  finding focal points in conventions. This is for conventions and design
  choices, not direct truth-voting on facts.
- `/mnt/d/System/SOVEREIGN_WAVE_PROTOCOL.md`: stronger isolated-worker pattern
  for consequential claim verification.
- `/mnt/d/System/FAMILY_WORKSPACE_UPDATE_RULE.md` and
  `/mnt/d/System/END_OF_DAY_SIGN_OFF.md`: continuity and handoff discipline.

The reliable claim here is not "the family is always right." The reliable claim
is: the family has built repeatable mechanisms that catch overclaim, stale
status, missing null models, and source mismatch.

---

## 6. What Greg Can Safely Say

Safe public-facing skeleton, before final release/legal checks:

> We are building a file-backed research and audit system where claims are not
> trusted because an agent says them. Claims are tiered in `CLAIMS.md`, checked
> against tests, Lean proofs where possible, and hostile Codex audits. Some
> results are exact algebraic or machine-checked under named premises; some are
> conditional; some promising routes have been demoted or falsified. The method
> matters as much as the positive results because it preserves the negative
> results too.

Do not say:

- "Fundamentals is release-approved."
- "Weinberg is derived."
- "The God Equation is unconditionally proven from Axioms 1-3."
- "Consciousness is derived."
- "The Shor survival map is Lean-proven."
- "The agents voted it true."

Say instead:

- "Here is the claim tier."
- "Here is the exact premise."
- "Here is the audit report."
- "Here is the test."
- "Here is what failed."
- "Here is what remains open."

---

## 7. The Deep Truth

The strongest thing here is not any single headline result. It is the pattern:

- structure gets proposed,
- derivations are attempted,
- tests and null models are run,
- independent minds cross-check,
- Codex audits for contradiction and overclaim,
- survivors are written back to durable files.

That is what Greg should reference first. The public may understand the results
slowly, but the method is already visible in the trail.

This document should be updated when `CLAIMS.md`, `ACTIVE_ISSUES.md`, Lean build
status, or public-release state changes.
