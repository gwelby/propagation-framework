# Report: PfLean.ClaimLedger + Registry — 2026-07-23

**Agent:** Devin (Cognition AI)  
**Workspace:** `/mnt/d/Fundamentals/lean`  
**Files touched:** `PfLean/ClaimLedger.lean`, `PfLean/ClaimLedgerRegistry.lean`, `PfLean.lean`

## What was built

### `PfLean/ClaimLedger.lean`
Formalizes the `CLAIMS.md` epistemic architecture:
- `EpistemicTier` — `DERIVED`, `CONDITIONAL`, `ARGUED`, `EMPIRICAL`, `INTUITION`, `OPEN`.
- `ClaimStatus` — gating overlays `OK`, `HOLD`, `NOGO`.
- `Confidence` — real number in `[0, 1]`.
- `ClaimRecord P` — proof of `P` plus tier, status, confidence, evidence, falsifier, dependencies. `tier_bound` is kernel-enforced.
- `ClaimEntry` and `ClaimLedger` with `lookup`, `allDependencies`, `dependenciesResolved`.
- Tier constructors `derived`, `conditional`, `argued`, `empirical`, `intuition`, `openClaim` plus `hold`/`noGo`.

### `PfLean/ClaimLedgerRegistry.lean`
Wires 10 real PF theorems into the ledger:
- **Double cover / topological weights:**
  - `quatToSO3_ker` — DERIVED 0.95
  - `at_most_two_closure_orders` — DERIVED 0.95
  - `kernel_closure_orders` — DERIVED 0.95, depends on `quatToSO3_ker` + `at_most_two_closure_orders`
  - `topological_availability` — DERIVED 0.95, depends on `kernel_closure_orders`
- **PFCore state-update:**
  - `T_full_decomposition` — DERIVED 0.95
  - `Q_sum_zero` — DERIVED 0.95
- **PF Entropy:**
  - `P0_Q_dot_zero` — DERIVED 0.95
  - `full_norm_Pythagorean` — DERIVED 0.95, depends on `P0_Q_dot_zero` + `Q_sum_zero`
  - `PFEntropy_decreases_T3` — CONDITIONAL 0.85, depends on `T_full_decomposition` + `Q_sum_zero`
  - `full_norm_T3_strictly_decreases` — CONDITIONAL 0.85, depends on `full_norm_Pythagorean` + `PFEntropy_decreases_T3`

`pfClaimLedger` is a concrete `ClaimLedger`; `pfClaimLedger_wellFormed` proves every dependency resolves.

## Verification

- `lake build PfLean.ClaimLedger` — green, 3285 jobs.
- `lake build PfLean.ClaimLedgerRegistry` — green, 8256 jobs.
- `lake build` (full project including executable) — green, 16530 jobs.
- Zero `sorry`s in `ClaimLedger.lean` and `ClaimLedgerRegistry.lean`.

## Next

1. Extend `ClaimLedgerRegistry` with more PF theorems (e.g. `isometry_linear_semigroup_gives_nonzero_periodic_orbit`, `ThreeGenerations`, `ShorBound`).
2. Build `PfLean.MeasurementContract` as the bridge between sandbox scanners and formal theorems.
