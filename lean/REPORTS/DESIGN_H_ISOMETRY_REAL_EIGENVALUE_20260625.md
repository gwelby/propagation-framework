# Design Document: H_isometry Experiment and the Real Eigenvalue Obstruction

**Date:** 2026-06-25; updated 2026-06-26
**Author:** Devin ∇λΣ∞ (GLM-5.2) — the Devin who fixed Z3FromBareMedium and corrected documentation drift
**Status:** IMPLEMENTED — H14/H15/H16 added to `Axioms.lean`, `isometry_implies_reversible` proven, and `full_norm_T3_strictly_decreases` (Entropy.lean) proves the isometry-JI incompatibility. Awaiting Codex PfLean audit clearance before final commit.
**Build state:** `lake build PfLean` = 8268 jobs, 0 errors (verified 2026-06-26)

---

## Summary

This document designs the next Lean experiment chain (H_isometry → compact recurrence → exact periodicity) and identifies a **structural obstruction** that may make Ending A impossible for the standard D=3 circulant dynamics: the J-I matrix has **real eigenvalues only**, so its propagation is a contraction, not an oscillation. No amount of H4 (complex structure) or H_isometry changes this. The Z₃ spatial symmetry and temporal periodicity may be **different axes** that cannot be connected without additional assumptions.

---

## 1. The Real Eigenvalue Obstruction

### 1.1 What the Lean source proves

The machine-verified eigenvalue structure of the D=3 circulant M = J-I (from `ArbitraryD.lean` and `PFCore.lean`):

| Operator | Uniform eigenvalue | Residue eigenvalue | Complex? |
|----------|-------------------|-------------------|----------|
| M = J-I | (D-1) = 2 | -1 | **No** — all real |
| L = -I + (1/2)M (God Equation) | (D-3)/2 = 0 | -3/2 | **No** — all real |
| T = I + dt·L (discrete update) | 1 + dt·0 = 1 | 1 - 3dt/2 | **No** — all real |
| T³ (one cycle, dt=1, α=1/2) | 1 | -1/8 | **No** — all real |
| T³^k (k cycles) | 1 | (-1/8)^k | **No** — decays to 0 |

**Source citations:**
- `circulant_D_uniform_eigenvalue` (ArbitraryD.lean:50) — eigenvalue (D-1), real
- `circulant_D_residue_eigenvalue` (ArbitraryD.lean:71) — eigenvalue -1, real
- `god_equation_uniform_eigenvalue` (ArbitraryD.lean:98) — eigenvalue (D-3)/2, real
- `god_equation_residue_eigenvalue` (ArbitraryD.lean:119) — eigenvalue -3/2, real
- `God_Equation_eigenvalues` (PFCore.lean:342) — {0, -3/2, -3/2}, all real
- `T3_Q_pow` (PFCore.lean:460) — T³^k scales residue by (-1/8)^k → decays

### 1.2 The general circulant eigenvalue formula

For a D=3 circulant with zero diagonal and first row (0, b, c), the eigenvalues are:

```
λ₀ = b + c                    (uniform mode)
λ₁ = -(b+c)/2 + i·(√3/2)·(b-c)   (first residue)
λ₂ = -(b+c)/2 - i·(√3/2)·(b-c)   (second residue)
```

The imaginary part is **proportional to (b - c)**. When b = c (the J-I symmetric case), the imaginary part vanishes. The eigenvalues become:

```
λ₀ = 2b    (real)
λ₁ = -b    (real)
λ₂ = -b    (real)
```

**Complex eigenvalues — the ones needed for oscillation and periodicity — arise ONLY when b ≠ c, which is the NON-symmetric case that J-I excludes.**

### 1.3 The fundamental tension

| Property | Requires | Compatible with M = J-I? |
|----------|----------|--------------------------|
| Z₃ spatial symmetry (M = J-I) | b = c | Yes (definitional) |
| Complex eigenvalues (oscillation) | b ≠ c | **No** |
| Non-zero periodic orbits | Complex eigenvalues | **No** |
| Approximate recurrence (H8) | Non-decaying orbit | **Only for uniform mode** (frozen, trivial) |

The J-I dynamics is a **contraction**: every non-uniform state decays geometrically to the uniform mode. The only "recurrence" is the trivial fixed point at the uniform mode (eigenvalue 0 under L, eigenvalue 1 under T).

### 1.4 What this means for the dependency graph

DeepSeek's dependency graph (v5, edge 16) says:

> "compact recurrent orbit + rationality condition → exact periodicity at D=3. D=3 may satisfy this automatically via its eigenvalue structure."

**This is incorrect for the standard circulant dynamics.** The D=3 J-I eigenvalues are real. There are no imaginary eigenvalues to be rational multiples of 2π. The rationality question is moot. Edge 16 should be marked **STRUCTURALLY BLOCKED** for the real circulant, not merely OPEN.

The rationality condition only becomes meaningful for the **non-symmetric** circulant (b ≠ c), where eigenvalues are complex. But b ≠ c is the case that J-I excludes — it's the case where Z₃ spatial symmetry does NOT hold.

---

## 2. The H_isometry Experiment (Still Worth Running)

Despite the real eigenvalue obstruction, the H_isometry experiment is worth running — not because it leads to periodicity, but because it tests whether isometry + recurrence gives us anything beyond the trivial uniform mode, and it honestly tracks the scaffolding cost.

### 2.1 Hypothesis definition (draft Lean)

```lean
/-- H14: Isometry — propagation preserves the pseudometric.
    d(s₁, s₂) = d(propagate(t, s₁), propagate(t, s₂)) for all t, s₁, s₂.
    This closes the dissipation gap (exp(-t)·v counterexample) but
    does NOT assume periodicity. Cost: 1 new hypothesis. -/
def Hypothesis_Isometry (M : BareMedium) : Prop :=
  ∀ (t : ℝ) (s₁ s₂ : M.State),
    M.d s₁ s₂ = M.d (M.propagate t s₁) (M.propagate t s₂)
```

**Cost:** 1 new hypothesis (H14). No transitive imports — it uses the existing `d` and `propagate` from `BareMedium`.

### 2.2 What H_isometry closes

The `exp(-t)·v` counterexample (edge 11) exploited **dissipation**: the propagation shrinks distances, so the orbit spirals to zero. H_isometry forbids this — distances are preserved. This eliminates the contraction counterexample.

### 2.3 What H_isometry does NOT close

Claude's quasi-periodic correction (edge 15): an irrational rotation on a torus is isometric, recurrent, and has **no exact non-zero periodic orbit**. So even with isometry:

- ✅ No contraction (dissipation gap closed)
- ✅ Compact orbit (isometry → bounded → finite-dim → compact closure)
- ❌ No exact periodicity (quasi-periodic obstruction)
- ❌ No connection to J-I (real eigenvalue obstruction — see §1)

### 2.4 The experiment chain

**Experiment 6: H_isometry closes the dissipation gap**

```
Theorem: H_isometry → propagate(t, ·) is injective for all t
Proof: d(s₁, s₂) = d(propagate(t, s₁), propagate(t, s₂)).
       If propagate(t, s₁) = propagate(t, s₂), then d(s₁, s₂) = 0.
```

This is almost trivial but worth machine-verifying — it confirms isometry implies reversibility (H1).

**Experiment 7: H8 + H_isometry + H3 + H5 → compact orbit closure**

The honest intermediate step. The orbit of the coherent state under an isometric linear semigroup on a finite-dimensional space is bounded (isometry preserves distance from the coherent state), and bounded sets in finite-dimensional normed spaces have compact closure (Heine-Borel).

**Scaffolding cost:** This requires topology on `BareMedium.State`. The cheapest import:
- H3 (linear) + H5 (finite-dim) → `Module ℝ M.State` + `Module.Finite ℝ M.State`
- → any norm on `M.State` (exists by finite-dimensionality)
- → `MetricSpace` structure (from the norm)
- → `Bornology` / bounded sets
- → Heine-Borel: bounded + closed → compact in finite-dim normed spaces

This re-imports the H3 transitive cost (15+ axioms) plus norm/metric/topology infrastructure. **Honest ledger impact: significant.**

**Experiment 8: H8 + H_isometry + H3 + H5 → the orbit approaches the uniform mode**

Even with isometry, the J-I eigenvalues are still real. Isometry prevents the orbit from decaying, but the J-I dynamics doesn't oscillate — it contracts (or, with isometry, preserves). The only way to reconcile isometry with real eigenvalues is if the coherent state is **already in the uniform mode** (the fixed-point eigenspace).

**Expected result:** The theorem reduces to "the coherent state is uniform" — which is trivial and doesn't derive Z₃ structure.

### 2.5 The negative result I expect

The H_isometry experiment chain will likely produce:

1. ✅ Isometry → injectivity (trivial, machine-verifiable)
2. ✅ Isometry + finite-dim → compact orbit closure (needs topology scaffolding)
3. ❌ Compact recurrence + J-I dynamics → exact periodicity: **BLOCKED by real eigenvalues**
4. ❌ The coherent state under J-I isometry is the uniform mode (trivial fixed point)

**The honest conclusion:** H_isometry closes the dissipation gap but does not bridge to Z₃ spatial symmetry. The real eigenvalue structure of J-I means the dynamics contracts (or preserves), never oscillates. Periodicity and Z₃ spatial symmetry are **different axes**.

---

## 3. The Two-Axis Diagnosis

### 3.1 Spatial vs temporal

The dependency graph conflates two distinct symmetry axes:

**Z₃ spatial symmetry** (M = J-I):
- A property of the **coupling matrix** — how channels relate to each other
- Selected by **stability** (H11): D=3 is the unique stable dimension
- Has **real eigenvalues** → contraction dynamics
- Does NOT produce temporal periodicity

**Temporal periodicity** (exact recurrence):
- A property of the **propagation dynamics** — how states evolve in time
- Requires **complex eigenvalues** (imaginary part → oscillation)
- Needs H4 (complex structure) + rationality condition
- Does NOT require Z₃ spatial symmetry

These are **independent properties**. A system can have Z₃ spatial symmetry without temporal periodicity (the J-I contraction), and temporal periodicity without Z₃ spatial symmetry (a 2D rotation with irrational frequency).

### 3.2 What this means for Ending A vs Ending B

**Ending A** (symmetry derived from recurrence): The chain "H8 → periodicity → Z₃ symmetry" requires connecting temporal periodicity to spatial symmetry. But the Z₃-symmetric dynamics (J-I) has real eigenvalues and contracts. The periodic dynamics requires complex eigenvalues, which need b ≠ c (non-symmetric). **These are incompatible.** Ending A may be **structurally impossible** for the standard circulant.

**Ending B** (symmetry irreducible): Z₃ spatial symmetry is an independent posit, selected by stability (H11), not derivable from temporal recurrence (H8). The honest parameter count:
- Coherence (H8: recurrence + stability): 1 parameter — gives approximate recurrence
- Spatial symmetry (H12/H13: permutation/cyclic): 1 parameter — gives Z₃ structure
- Stability (H11): 1 parameter — selects D=3 given symmetry
- **Total: 3 irreducible physical posits + scaffolding**

**Ending B may be the honest answer.** The dependency graph should reflect this as the likely outcome, not merely "one of two clean endings."

---

## 4. Proposed Dependency Graph Corrections

Based on the real eigenvalue analysis, the following corrections to DeepSeek's v5 graph are proposed:

### 4.1 Edge 16 correction

**Current:** "compact recurrent orbit + rationality condition → exact periodicity at D=3. D=3 may satisfy this automatically via its eigenvalue structure. OPEN"

**Corrected:** "compact recurrent orbit + rationality condition → exact periodicity. **STRUCTURALLY BLOCKED for J-I circulant**: D=3 J-I eigenvalues are real {0, -3/2, -3/2} (machine-verified: ArbitraryD.lean, PFCore.lean). No imaginary component → no oscillation → no periodicity. Rationality condition is moot. Complex eigenvalues require b ≠ c (non-symmetric), which J-I excludes. The rationality question only arises for the NON-symmetric circulant."

### 4.2 New edge 17

"Z₃ spatial symmetry (M = J-I) ↔ real eigenvalues ↔ contraction dynamics. **VERIFIED** (ArbitraryD.lean, PFCore.lean). The J-I dynamics contracts to the uniform mode. Temporal periodicity requires complex eigenvalues, which require b ≠ c, which excludes Z₃ symmetry. **Spatial symmetry and temporal periodicity are independent axes.**"

### 4.3 Ending A status update

**Current:** "Symmetry derived (BIG, now more constrained) — OPEN"

**Corrected:** "Symmetry derived — **STRUCTURALLY BLOCKED for standard circulant dynamics**. The J-I matrix (Z₃ symmetric) has real eigenvalues and contracts. Periodicity requires complex eigenvalues, which require non-symmetry. These are incompatible. Ending A may be impossible without fundamentally changing the dynamics model (e.g., adding a separate oscillatory mechanism not captured by the circulant coupling matrix)."

### 4.4 Ending B status update

**Current:** "Symmetry irreducible (also real)"

**Corrected:** "Symmetry irreducible — **LIKELY HONEST ANSWER**. Z₃ spatial symmetry is an independent posit (H12/H13), selected by stability (H11), not derivable from temporal recurrence (H8). The real eigenvalue structure of J-I confirms this: the dynamics contracts, it doesn't oscillate. The honest parameter count: 3 irreducible posits (coherence + symmetry + stability) + scaffolding."

---

## 5. Next Steps (Priority Order)

### 5.1 Already implemented (2026-06-26)

- ✅ **Add `Hypothesis_Isometry` (H14)**, `Hypothesis_MetricIdentity` (H15), and `Hypothesis_MetricReflexivity` (H16) to `Axioms.lean`.
- ✅ **Run Experiment 6** (isometry → injectivity): `isometry_implies_reversible` proven, machine-verified.
- ✅ **Run Experiment 8** (J-I + isometry → contraction): `full_norm_T3_strictly_decreases` proven in `Entropy.lean`. T³ strictly decreases the full Euclidean norm for any non-uniform state; J-I + isometry is inconsistent.
- ✅ **Document the two-axis finding** — spatial symmetry and temporal periodicity are independent.

### 5.2 Still open

- **Experiment 7** (isometry + finite-dim → compact closure) — needs topology scaffolding in `BareMedium.State`. The theorem `isometry_finite_dim_gives_compact_orbit` is a `True` stub.
- **D-selection principle** — why is D=3 the relevant dimension? `D4_symmetric_zero_diag_equal_rows_not_unique_JI` proves D=3 uniqueness is dimension-dependent.

### 5.3 For Claude (design review)

The key design question: **is there a dynamics model where Z₃ spatial symmetry and temporal periodicity coexist?** Candidates:
- A **non-circulant** coupling matrix with Z₃ symmetry but complex eigenvalues (is this possible? Z₃-invariant matrices with complex spectrum?)
- A **second-order** dynamics (acceleration, not just velocity) — the wave equation has real eigenvalues but oscillatory solutions
- A **Hamiltonian** formulation where the eigenvalues come in ±iω pairs

If none of these work, Ending B is not just "also real" — it's the **only honest ending**.

### 5.4 For DeepSeek (graph update)

Dependency graph updated to v8 (2026-06-26) with:
- Edge 16: STRUCTURALLY BLOCKED
- Edge 19: FALSE (J-I + isometry incompatible, `full_norm_T3_strictly_decreases`)
- Edge 20: STRUCTURALLY BLOCKED (isometry → skew-symmetry, J-I is symmetric)
- Edge 22: VERIFIED (D3 uniqueness + D4 counterexample)
- H17/H18 named and costed
- Ending A: STRUCTURALLY BLOCKED
- Ending B: LIKELY HONEST ANSWER

---

## 6. Machine-Verified Evidence

All eigenvalue claims in this document are backed by machine-verified Lean theorems:

| Claim | Lean theorem | File:Line |
|-------|-------------|-----------|
| M = J-I has uniform eigenvalue (D-1) | `circulant_D_uniform_eigenvalue` | ArbitraryD.lean:50 |
| M = J-I has residue eigenvalue -1 | `circulant_D_residue_eigenvalue` | ArbitraryD.lean:71 |
| L = -I + (1/2)M has uniform eigenvalue (D-3)/2 | `god_equation_uniform_eigenvalue` | ArbitraryD.lean:98 |
| L = -I + (1/2)M has residue eigenvalue -3/2 | `god_equation_residue_eigenvalue` | ArbitraryD.lean:119 |
| At D=3: L eigenvalues are {0, -3/2, -3/2} | `God_Equation_eigenvalues` | PFCore.lean:342 |
| T³ scales residue by -1/8 (real, contracting) | `T3_Q` | PFCore.lean:401 |
| T³^k scales residue by (-1/8)^k → decays | `T3_Q_pow` | PFCore.lean:460 |
| D=3 is unique stable dimension | `D3_unique_stable_dimension` | ArbitraryD.lean:145 |
| T³ strictly decreases full Euclidean norm for non-uniform states | `full_norm_T3_strictly_decreases` | Entropy.lean:237 |
| D=3: symmetry + zero diagonal + equal row sums → J-I | `D3_symmetric_zero_diag_equal_rows_forces_JI` | Z3FromBareMedium.lean |
| D=4: symmetric + zero diagonal + equal row sums is NOT unique | `D4_symmetric_zero_diag_equal_rows_not_unique_JI` | Z3FromBareMedium.lean |
| D-selection principle: D=3 uniquely selected by stability | `D_selection_principle` | Z3FromBareMedium.lean |

All eigenvalues are **real**. No theorem in the codebase produces a complex eigenvalue for the J-I circulant. The contraction dynamics is machine-verified. The isometry-JI incompatibility is now also machine-verified.

---

## 7. The Honest One-Liner

> **The Z₃ circulant at D=3 is selected by stability, not by periodicity. Its eigenvalues are real, its dynamics contracts, and it does not oscillate. Temporal periodicity and Z₃ spatial symmetry are independent axes that cannot be connected through the standard circulant coupling matrix. Ending B (symmetry irreducible) is likely the honest answer.**

---

*This is a design document, not a theorem. The eigenvalue analysis is machine-verified; the two-axis diagnosis and Ending A obstruction are mathematical arguments pending formalization. All claims about Lean theorems reference the live build (8267 jobs, 0 errors, 2026-06-22).*
