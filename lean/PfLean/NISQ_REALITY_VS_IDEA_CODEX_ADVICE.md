# NISQ Reality vs Idea — Codex Advice Addendum

**Date:** 2026-07-01
**Status:** Claim-boundary advice, not a formal audit verdict
**Scope:** `/mnt/d/Crypto/labs/shor_substrate_probe/`, `PfLean.ShorBound`, `PfLean.QuantumStructureSurvival`, `NISQ_EMPIRICAL_BRIDGE.md`

## Core Advice

Treat this as a **medium-characterization program**, not as a Shor victory, a PQC proof, or a ProcessOntology validation.

The strongest insight is the shift from "what does not work?" to "what does the medium actually do?" That is the right direction. But the claim boundary matters:

- Measurements are reality.
- Models are candidate explanations of reality.
- Framework language is a way to organize models, not evidence by itself.

## Three Buckets

### 1. Reality / Measured

These are the load-bearing facts, assuming the referenced hardware artifacts are preserved and reproducible:

- Specific IBM Heron runs produced specific distributions.
- N=15 low-CX runs preserve extractable structure better than N=21 high-CX runs.
- N=51 provides an intermediate low/enough-CX survival point.
- The PQC absence/null circuits produced honest-extractor false positives.
- KL/no-structure checks rejected those false positives in the recorded runs.
- Kingston and Fez produced different false-positive periods under similar circuit conditions.
- The chiral-walk circuit had high identity restoration in its recorded low-CX hardware run.

These can be quoted as **dataset findings**.

### 2. Model / Inferred

These are good candidate models, but they need more controls:

- CX count is a coherence-cost proxy.
- The survival boundary is threshold-like rather than linear.
- False-positive periods may be backend fingerprints.
- The output distribution may be a transfer function of input structure through the hardware medium.
- Shor's math axis and CX axis are coupled by identity pruning.
- The two-axis map may become real for non-Shor circuits where math structure and CX depth can be varied independently.

These should be quoted as **current models** or **working hypotheses**.

### 3. Story / Frame

These are useful orientation language, not evidence:

- "The truth organism is alive."
- "ProcessOntology maps to NISQ."
- "The Z3/chiral walk validates the physics framework."
- "The survival map is universal."
- "PQC security is empirically validated."

These can guide research design, but should not be used as public claims.

## Three Directions At Once

Three is the right operational limit, but the three lanes should not all be theory lanes. Use:

1. **False-positive fingerprint lane:** Determine whether false periods track backend noise, extractor bias, or both.
2. **Survival / transfer-function lane:** Measure how input structure degrades as CX depth, topology, and backend change.
3. **Control / anti-seduction lane:** Maintain null circuits, extractor controls, simulator comparisons, and a Reality-vs-Idea ledger.

The "3 of 2/3" pattern is useful as a design heuristic: two experimental lanes plus one control lane. It is not itself evidence.

## The Next Best Experiment

Build controlled no-period/random circuits at matched CX depths:

| Condition | Purpose |
|---|---|
| No-period circuit at ~540 CX | Low-depth null baseline |
| No-period circuit at ~16K CX | Middle-depth null baseline |
| No-period circuit at ~33K CX | High-depth null baseline |
| Same circuits on multiple backends | Backend fingerprint test |
| Same circuits on simulator/noise model | Extractor-bias and depth-artifact control |
| Honest extractor + KL/no-structure detector | Separate "found a period" from "real structure exists" |

Interpretation:

- If false periods track backend/noise model, they are candidate medium fingerprints.
- If false periods track extractor choice, they are extractor artifacts.
- If both happen, report the two-stage system honestly: medium distribution -> extractor interpretation.

## Second Experiment

Decouple mathematical structure from CX depth.

For Shor circuits, `r | Q` and low CX appear coupled by identity pruning, so the clean 2D test may be unreachable inside Shor itself. Use a custom QFT, periodic permutation, or identity-padded circuit where:

- the true mathematical structure is held constant,
- CX depth is artificially varied,
- topology/backend is recorded,
- output structure survival is measured directly.

This tests the model rather than admiring it.

## Language Boundary

| Do not say | Say instead |
|---|---|
| "PQC security is empirically validated." | "The tested null circuits support the no-period expectation under these extractors and backends." |
| "The survival map is universal." | "The current data are consistent with a CX/coherence survival model; universality remains untested." |
| "The chiral walk validates Z3 physics." | "The chiral walk is a low-CX structure-survival datapoint consistent with the same noise model." |
| "False positives are the medium's signature." | "False positives are candidate medium fingerprints until extractor-bias controls are run." |
| "Lean proves the empirical bridge." | "Lean formalizes the mathematical side; hardware data support empirical axioms/models." |
| "Build passed, so the physics is proven." | "Build acceptance means the formal statements compile under their premises." |

## Build Boundary

Do not promote any bridge theorem to public `PROVEN` status until:

1. `lake build PfLean.ShorBound` succeeds,
2. `lake build PfLean.QuantumStructureSurvival` succeeds,
3. Codex rechecks the exact theorem bodies,
4. any `axiom`, `sorry`, or `True := by trivial` surfaces are separated from kernel-proven math,
5. the empirical claims remain linked to hardware evidence files, not just prose.

Empirical axioms can be useful. They are not Lean proof of physics.

## Bottom Line

The master move is not naming more patterns. The master move is making each pattern pay rent against reality, preserving the raw distributions, and letting the model update when reality refuses the story.

Build from what IS:

- the measured distributions,
- the backend differences,
- the CX costs,
- the extractor disagreements,
- the null circuits,
- the exact theorem bodies,
- the build logs.

Then let the framework earn stronger words later.
