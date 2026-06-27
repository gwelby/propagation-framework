# TopologicalWeights.lean — Path B Analysis
**Lane 3: Devin CLI 2** | **Date:** 2026-06-14

---

## The Gap (Lines 119-128)

```lean
theorem topological_availability_conditional
  (path_lifting : ∀ (γ : ℝ → SO3), Continuous γ ∧ γ 0 = γ 1 →
    ∃ (gamma_tilde : ℝ → UnitQuaternion), Continuous gamma_tilde ∧
      quatToSO3 (gamma_tilde 0) = γ 0 ∧ ∀ t, quatToSO3 (gamma_tilde t) = γ t) :
  ∀ (w : ℕ), w ∈ closureOrders UnitQuaternion → w = 1 ∨ w = 2 := by
  sorry
```

**Claimed blocker:** mathlib4 has no `CoveringMap`, `DeckTransformation`, or path-lifting APIs.

**Actual blocker:** The theorem statement itself is problematic. It claims ALL elements of `UnitQuaternion` have order 1 or 2. This is **false** — `UnitQuaternion` (SU(2) ≅ S³) contains elements of all finite orders (e.g., a rotation by 120° has order 3).

---

## Path B: Reframe Without Covering Spaces

### The Core Insight

The "topological availability" claim in the PF context is NOT about all elements of SU(2). It's about the **kernel of the covering map** SU(2) → SO(3), which is exactly {±1}.

The kernel {±1} has:
- `1` with order 1
- `-1` with order 2

That's it. No other elements act trivially on SO(3).

### What We Already Proved (No Covering Spaces Needed)

**`kernel_closure_orders` (lines 94-102):**
```lean
∀ g : UnitQuaternion, quatToSO3 g = 1 → closureOrder g = 1 ∨ closureOrder g = 2
```

This is already proven using `quatToSO3_ker` from `SO3DoubleCover.lean`. It says: "If g acts trivially on SO(3), then g has order 1 or 2."

**`at_most_two_closure_orders` (lines 159-188):**
```lean
∀ (g : UnitQuaternion), g = 1 ∨ g = -1 → closureOrder g = 1 ∨ closureOrder g = 2
```

This is also proven by direct computation.

### Path B Theorem (Reframed)

We don't need path lifting or covering spaces. The topological availability is already captured by the kernel:

```lean
-- The topological availability theorem, WITHOUT covering spaces:
-- The only elements of SU(2) that act trivially on SO(3) are {±1},
-- which have orders {1, 2}. This is the full topological obstruction.

theorem topological_availability_kernel_only :
  ∀ g : UnitQuaternion, quatToSO3 g = 1 → closureOrder g = 1 ∨ closureOrder g = 2 :=
  kernel_closure_orders
```

This is **already proven** (line 94). It requires no covering-space theory.

### Why This is Sufficient for PF

The PF "(2,1) weights claim" has two parts:
1. **Topological availability:** Only closure orders {1, 2} are possible
2. **Physical realization:** Both must be populated

Part 1 follows from: "The only loops in SO(3) that lift to closed loops in SU(2) are those whose lifts are in {±1}." This is equivalent to `kernel_closure_orders`.

The standard covering-space proof goes:
```
π₁(SO(3)) ≅ DeckTransformations ≅ Kernel ≅ {±1} ≅ ℤ₂
```

But for the PF claim, we only need:
```
Kernel = {±1} → orders are {1, 2}
```

The isomorphism with π₁ is extra structure we don't need.

---

## The Fix

### Option 1: Remove the sorry entirely

Replace `topological_availability_conditional` with a corollary of `kernel_closure_orders`:

```lean
/-- **Topological Availability (PROVEN):** The kernel of the covering map
    SU(2) → SO(3) is {±1}, with closure orders {1, 2} exactly.

    This is the honest topological foundation for the (2,1) weights claim.
    No path-lifting or covering-space theory is needed — the kernel
    obstruction is purely algebraic and already proven. -/
theorem topological_availability :
  ∀ g : UnitQuaternion, quatToSO3 g = 1 → closureOrder g = 1 ∨ closureOrder g = 2 :=
  kernel_closure_orders
```

### Option 2: Keep the conditional form but fix the statement

If we want to keep a "conditional" theorem for future covering-space formalization:

```lean
/-- **Conditional form (for future covering-space stack):**
    Assuming path lifting, the deck transformation group of the cover
    SU(2) → SO(3) has exactly closure orders {1, 2}.

    NOTE: The unconditional version (kernel_closure_orders) is already
    proven without path lifting. This conditional form is kept for
    pedagogical alignment with standard topology textbooks. -/
theorem topological_availability_conditional_refactored
  (path_lifting : ∀ (γ : ℝ → SO3), Continuous γ ∧ γ 0 = γ 1 →
    ∃ (gamma_tilde : ℝ → UnitQuaternion), Continuous gamma_tilde ∧
      quatToSO3 (gamma_tilde 0) = γ 0 ∧ ∀ t, quatToSO3 (gamma_tilde t) = γ t) :
  ∀ g : UnitQuaternion, quatToSO3 g = 1 → closureOrder g = 1 ∨ closureOrder g = 2 := by
  intro g h
  exact kernel_closure_orders g h
```

The proof is trivial because `kernel_closure_orders` already proved it unconditionally.

---

## Why This Works

| Standard Topology Approach | Path B (Kernel-Only) |
|---------------------------|----------------------|
| Build `CoveringMap` API in mathlib4 (~200 lines) | Use existing `SO3DoubleCover.lean` |
| Prove path lifting (~100 lines) | Already have `quatToSO3_ker` |
| Prove `π₁(SO(3)) ≅ DeckTransformations` (~150 lines) | Not needed for PF claim |
| Prove `DeckTransformations ≅ Kernel` (~50 lines) | Not needed — we use kernel directly |
| **Total:** ~500 lines of new Lean | **Total:** 0 lines — already proven |

The PF claim only needs: "The topology of SO(3) permits at most two closure orders." This follows from `|Kernel| = 2`, which is `quatToSO3_ker`.

---

## Honest Boundary

This Path B does NOT prove:
- `π₁(SO(3)) ≅ ℤ₂` (requires covering spaces)
- The deck transformation theorem (requires covering spaces)
- Path lifting (requires covering spaces)

It DOES prove:
- The kernel of SU(2) → SO(3) is {±1} ✅
- Kernel elements have orders {1, 2} ✅
- This is the topological obstruction for PF ✅

If the PF community later wants the full `π₁(SO(3)) ≅ ℤ₂` theorem, that requires Path A (building covering spaces in mathlib4). But for the (2,1) weights claim, the kernel-only theorem is sufficient.

---

*∇λΣ∞ — The cathedral gets its keystone from what we already have, not from what mathlib4 hasn't shipped.*
