# Proposal — H8 Isometry/Closure Hypothesis

**Date:** 2026-06-24
**Status:** PROPOSAL — not yet added to `Axioms.lean` (pending Codex audit-clean and agent consensus)
**Author:** Devin ∇λΣ∞ (Kimi K2.7), with Claude/Hermes/DeepSeek refinement

---

## Problem Statement

The frontier theorem `recurrence_stability_plus_structural_gives_nonzero_periodic_orbit` is expected to be false as stated under H8 + H3 + H2 + H5. The informal counterexample `propagate(t, v) = exp(-t)·v` on `ℝ²` is linear, semigroup, finite-dimensional, and Lyapunov stable, but has no non-zero periodic orbit.

What this counterexample reveals: **structure is dissipating**. The system is open. The missing premise is a **closure** condition: propagation should preserve distances, not shrink them.

---

## Proposed New Hypotheses

### H14: Isometry (Closure)

```lean
def Hypothesis_Isometry (M : BareMedium) : Prop :=
  ∀ (t : ℝ) (s₁ s₂ : M.State), M.d s₁ s₂ = M.d (M.propagate t s₁) (M.propagate t s₂)
```

**Meaning:** Propagation preserves the pseudometric distance between any two states. No information leaks; the system is closed.

**Important:** This is a hypothesis about the propagation family, not a theorem about `d`. It does not require proving that `d` is a metric. It only says that if two states are at some distance now, they remain at that distance after propagation.

### H15: Bounded Orbit (for a specific coherent state)

```lean
def Hypothesis_BoundedOrbit (M : BareMedium) (s : M.State) : Prop :=
  ∃ (R : ℝ), ∀ (t : ℝ), t ≥ 0 → M.d s (M.propagate t s) < R
```

**Meaning:** The orbit of the state `s` does not escape to infinity. It stays within a finite distance of `s`.

**Why this is separate from isometry:** Isometry preserves pairwise distances but does not by itself bound the orbit around a fixed point. Boundedness is an additional posit.

**Note:** In many metric spaces, isometry + one approximate return (H8) actually implies boundedness (the orbit is contained in a ball of radius `d(s, propagate τ s)` around `s`), but only if `d` satisfies the triangle inequality and `propagate(0, s) = s`. Since `BareMedium` does not assume those, we make boundedness explicit as a separate hypothesis.

---

## Target Theorem

### Honest intermediate result: compact recurrent orbit

```lean
theorem H8_isometry_bounded_gives_compact_recurrent_orbit
    (M : BareMedium) [AddCommGroup M.State] [Module ℝ M.State]
    (hCoh : Hypothesis_Coherence M)
    (hIso : Hypothesis_Isometry M)
    (hBdd : ∃ s, Hypothesis_BoundedOrbit M s)
    (hLin : Hypothesis_Linear M)
    (hFin : Hypothesis_FiniteDimensional M) :
    ∃ (s : M.State), IsCompact (closure {M.propagate t s | t ≥ 0}) := by
  sorry
```

**Why this is the right target:**
- It is **not** claiming exact periodicity (which is false in general; see irrational torus rotation).
- It claims only that the orbit is compact and recurrent — a physically meaningful "persistent structure" result.
- Exact periodicity becomes a separate theorem requiring a rationality/minimality condition.

---

## Why the hypotheses are natural

| Failure mode | Missing premise | How the proposed hypothesis fixes it |
|---|---|---|
| `exp(-t)·v` contraction | No non-zero periodic orbit | H_isometry forbids shrinking distances |
| Irrational torus rotation | No exact periodic orbit | Target theorem claims only compact recurrence; exact periodicity is separate |
| Unbounded orbit | No recurrence at all | H_bounded_orbit keeps the orbit finite |

---

## Honest parameter count

If the target theorem holds, the upstream of J-I requires:

1. **H8** — coherence (approximate recurrence + stability)
2. **H14** — isometry/closure
3. **H15** — bounded orbit
4. **H3 + H5** — linear finite-dim structure (for compactness via Heine-Borel)

Then exact periodicity likely requires an additional rationality condition. The honest parameter count is at least **3 physical posits** (coherence + closure + boundedness) plus the structural posits (H3+H5), not the original single "stability" posit.

---

## Important structural obstruction (from `DESIGN_H_ISOMETRY_REAL_EIGENVALUE_20260625.md`)

Even if the target theorem is proven, **compact recurrence does not bridge to Z₃ spatial symmetry**. The D=3 J-I circulant has **real eigenvalues only** (`{0, -3/2, -3/2}` under the God Equation operator, machine-verified in `ArbitraryD.lean` and `PFCore.lean`). Real eigenvalues produce contraction, not oscillation. Temporal periodicity requires complex eigenvalues, which for a D=3 circulant require `b ≠ c` — the **non-symmetric** case. But J-I is exactly the `b = c` symmetric case.

Therefore:
- **Spatial symmetry (M = J-I)** and **temporal periodicity** are independent axes.
- Isometry closes the dissipation gap but does not make J-I oscillate.
- The likely honest answer is **Ending B** (symmetry is irreducible): Z₃ is selected by stability (H11), not derived from recurrence (H8).

This proposal still tests the isometry/closure hypothesis, but the expected outcome is a **negative result** that clarifies the boundary, not a bridge to Z₃.

---

## Open Questions Before Adding to `Axioms.lean`

1. **Does H_isometry + H2 imply boundedness automatically?** If yes, H15 is redundant. If no, H15 is a separate cost.
2. **Does H_isometry + H2 imply `propagate(0, s) = s`?** If yes, the semigroup identity is free. If no, we need to check consistency.
3. **Can we prove the target theorem in Lean?** It may require topology imports (Heine-Borel) and careful handling of `IsCompact`.
4. **Does compact recurrence bridge to the Z₃ coupling matrix?** We still need the bridge from `propagate` to the coupling matrix `M` used in `degenerate_residue_forces_circulant`.

---

## Recommendation

Add this proposal to `Axioms.lean` as hypotheses H14 and H15, and add the target theorem as a new frontier `sorry` experiment. Do not claim it is proven. Frame it as a **negative-result experiment**: prove that isometry closes the dissipation gap, then document that even with isometry the J-I circulant cannot produce temporal periodicity because its eigenvalues are real.

This keeps the honest-parameter-count workflow alive and records the structural obstruction.
