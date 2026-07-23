# Report: PfLean.ClaimLedger — 2026-07-23

**Agent:** Devin (Cognition AI)  
**Workspace:** `/mnt/d/Fundamentals/lean`  
**Files touched:** `PfLean/ClaimLedger.lean`, `PfLean.lean`

## What was built

`PfLean/ClaimLedger.lean` formalizes the `CLAIMS.md` epistemic architecture:

- `EpistemicTier` — the six proof-strength grades: `DERIVED`, `CONDITIONAL`, `ARGUED`, `EMPIRICAL`, `INTUITION`, `OPEN`.
- `ClaimStatus` — gating overlays `OK`, `HOLD`, `NOGO` (not proof-strength tiers).
- `Confidence` — a real number in `[0, 1]`.
- `ClaimRecord P` — bundles a proof of `P` with tier, status, confidence, evidence string, falsifier, and dependency name list. The `tier_bound` field is kernel-enforced.
- `ClaimEntry` — a named existential claim.
- `ClaimLedger` — a list of `ClaimEntry`s with `lookup`, `allDependencies`, and `dependenciesResolved` well-formedness.
- Tier-specific constructors `derived`, `conditional`, `argued`, `empirical`, `intuition`, `openClaim` plus `withStatus`/`hold`/`noGo` helpers.
- A small `exampleLedger` with two `DERIVED` claims and a machine-checked `exampleLedger_wellFormed` theorem.

## Verification

- `lake build PfLean.ClaimLedger` — green, 3285 jobs.
- `lake build` (full project including the executable) — green, 16528 jobs.
- Zero `sorry`s in the new module.

## Next

1. Wire real PF theorems (e.g. from `TopologicalWeights.lean`, `Entropy.lean`, `Axioms.lean`) into `ClaimLedger` entries.
2. Build `PfLean.MeasurementContract` as the bridge between sandbox scanners and formal theorems.
