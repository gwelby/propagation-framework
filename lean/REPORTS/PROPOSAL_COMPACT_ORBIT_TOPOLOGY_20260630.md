# Proposal: Topology Scaffolding for `isometry_finite_dim_gives_compact_orbit`

> **Date:** 2026-06-30
> **Author:** Devin (GLM-5.2) with topology research from Mathlib source audit
> **Status:** Draft — awaiting build verification of H19/H20/counterexample/obstruction first
> **Depends on:** Edge 25 (dependency graph v10), `lake build PfLean.Axioms` exiting 0

---

## The Theorem

```lean
theorem isometry_finite_dim_gives_compact_orbit
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    (s : M.State)
    (hIso : Hypothesis_Isometry M)       -- H14
    (hBdd : Hypothesis_BoundedOrbit M s) -- H19
    (hFin : Hypothesis_FiniteDimensional M) : -- H5
    IsCompact (closure (Set.range (fun t => M.propagate t s)))
```

## Mathematical Argument

1. H5 (finite-dim) + NormedSpace ℝ → `FiniteDimensional.proper_real` instance → `ProperSpace M.State`
2. ProperSpace → Heine-Borel: `IsCompact s ↔ IsClosed s ∧ IsBounded s`
3. H19 (bounded orbit) → orbit set is bounded
4. `IsBounded.isCompact_closure` → closure of bounded set is compact
5. QED

## Required Mathlib Imports

```lean
import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.Normed.Module.FiniteDimension  -- FiniteDimensional.proper_real
import Mathlib.Topology.MetricSpace.Bounded             -- Heine-Borel, IsBounded.isCompact_closure
import Mathlib.Topology.MetricSpace.Defs                -- closedBall
import Mathlib.Data.Set.Operations                      -- Set.range
import Mathlib.Topology.Defs.Basic                      -- closure
import Mathlib.Topology.Compactness.Compact             -- IsCompact
```

## Key Mathlib Theorems

| Theorem | Location | What it gives |
|---------|----------|---------------|
| `FiniteDimensional.proper_real` | FiniteDimension.lean:575-577 | Finite-dim real normed space → ProperSpace |
| `isCompact_iff_isClosed_bounded` | Bounded.lean:325-327 | Heine-Borel: compact ↔ closed ∧ bounded (needs ProperSpace) |
| `IsBounded.isCompact_closure` | Bounded.lean:318-320 | Closure of bounded set is compact (needs ProperSpace) |
| `isBounded_iff_subset_closedBall` | Bounded.lean:87-89 | Bounded ↔ subset of some closed ball |
| `NormedAddCommGroup` | Group/Defs.lean:217-220 | Extends MetricSpace with dist x y = ‖-x + y‖ |

## Required Type Class Changes

Current signature: `[AddCommGroup M.State] [Module ℝ M.State]`
New signature: `[NormedAddCommGroup M.State] [NormedSpace ℝ M.State]`

This is a **stronger requirement** — it adds a norm to the state space. The cost:
- NormedAddCommGroup extends AddCommGroup + MetricSpace (dist from norm)
- NormedSpace ℝ extends Module ℝ (norm compatible with scalar multiplication)
- Together with FiniteDimensional ℝ → triggers `proper_real` → Heine-Borel

## Critical Gap: Connecting M.d to the Norm

The proof needs `M.d` (BareMedium's bare pseudometric) to be the same as the norm-induced metric `dist`. Three options:

### Option A: New hypothesis H21 (MetricFromNorm)
```lean
def Hypothesis_MetricFromNorm (M : BareMedium) [NormedAddCommGroup M.State] : Prop :=
  ∀ (s₁ s₂ : M.State), M.d s₁ s₂ = dist s₁ s₂
```
**Cost:** 1 hypothesis. Cleanest separation. H19 boundedness in M.d transfers to dist.

### Option B: Define norm from M.d
```lean
instance (M : BareMedium) [MetricSpace M.State] : Norm M.State where
  norm x := M.d x 0
```
**Problem:** Need to prove norm axioms from metric axioms on M.d. Requires H15 + H16 + triangle inequality (not currently assumed).

### Option C: Pseudometric Heine-Borel
Work entirely with M.d and prove a pseudometric version of Heine-Borel.
**Problem:** Mathlib's Heine-Borel is for MetricSpace + ProperSpace, not pseudometric.

**Recommendation:** Option A (H21). It's the honest parameter count — the theorem needs H14 + H19 + H3 + H5 + H21 + topology scaffolding.

## Draft Proof

```lean
theorem isometry_finite_dim_gives_compact_orbit
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    (s : M.State)
    (hIso : Hypothesis_Isometry M)
    (hBdd : Hypothesis_BoundedOrbit M s)
    (hFin : Hypothesis_FiniteDimensional M)
    (hMetric : Hypothesis_MetricFromNorm M) :
    IsCompact (closure (Set.range (fun t => M.propagate t s))) := by
  -- Step 1: Extract boundedness from H19
  obtain ⟨R, hR⟩ := hBdd
  -- Step 2: Show the orbit is bounded in the norm metric
  have h_orbit_bounded : IsBounded (Set.range (fun t => M.propagate t s)) := by
    rw [isBounded_iff_subset_closedBall s]
    use R
    intro x hx
    obtain ⟨t, ht⟩ := Set.mem_range.mp hx
    rw [← ht, hMetric]
    -- H19 gives M.d s (M.propagate t s) < R, which equals dist s (M.propagate t s) < R
    -- Need to convert to dist s x ≤ R (closedBall uses ≤, H19 uses <)
    exact (hR t (by omega)).le  -- may need adjustment for t ≥ 0
  -- Step 3: Apply Heine-Borel via IsBounded.isCompact_closure
  -- FiniteDimensional.proper_real gives ProperSpace, which is the precondition
  exact h_orbit_bounded.isCompact_closure
```

## Honest Parameter Count

| Hypothesis | What it gives | Cost |
|-----------|---------------|------|
| H3 (linear) | propagate(t,0) = 0, matrix structure | 15+ transitive |
| H5 (finite-dim) | FiniteDimensional ℝ → proper_real → Heine-Borel | 1 |
| H14 (isometry) | d preserved under propagation | 1 |
| H19 (bounded orbit) | Orbit stays within finite distance | 1 |
| H21 (metric from norm) | M.d = dist (bridge to normed space) | 1 |
| Topology scaffolding | NormedAddCommGroup + NormedSpace instances | ~20 axioms |

**Total new cost:** H19 + H21 + topology = 2 explicit + scaffolding

## Next Steps

1. **Wait for build verification** of H19/H20/counterexample/obstruction (Greg running it now)
2. **Add H21 (Hypothesis_MetricFromNorm)** to Axioms.lean
3. **Change theorem signature** from AddCommGroup/Module to NormedAddCommGroup/NormedSpace
4. **Replace `True := by trivial`** with the actual proof
5. **Build and verify** — this will need the topology imports which may increase build time
6. **Update dependency graph v10→v11** with edge 25 upgraded from OPEN to VERIFIED

## Note on H14 (Isometry) Role

H14 (isometry) is actually NOT needed for the compactness proof itself — H19 (bounded orbit)
alone gives boundedness, and finite-dim gives Heine-Borel. H14 is needed for the broader
argument that isometry + bounded orbit is a meaningful combination (e.g., in the context
of the real eigenvalue obstruction, edges 26-27). The compact-orbit theorem is really
H19 + H5 + topology → compact closure, with H14 as context.

This is a discovery: the compact-orbit theorem doesn't actually need isometry. It needs
boundedness (H19) and finite-dimensionality (H5). Isometry is a sufficient condition for
boundedness in some contexts, but H19 is the honest premise.
