# PFLean Hypothesis / Premise Ledger

> **Purpose:** One place to record what each named hypothesis (H1–H18) actually
> buys, what it does *not* buy, and how the Z₃ circulant result depends on explicit
> premises. This ledger is documentation only; Lean source is the binding truth.
> **Last updated:** 2026-06-26 (Devin: H18 added, isometry-JI incompatibility proven, D3/D4 theorems verified)
> **Bound:** This file does not modify `CLAIMS.md`, PRED files, public surfaces,
> or the Fundamentals PUBLIC HOLD.

---

## Hypothesis Roster (matching `PfLean.Axioms.lean`)

| ID | Name | Lean definition | What it actually asserts |
|----|------|-------------------|--------------------------|
| H1 | Reversibility | `Hypothesis_Reversible` | `propagate t` is injective for all `t > 0`. Injectivity alone does not imply periodicity. |
| H2 | Semigroup | `Hypothesis_Semigroup` | `propagate (t + s) = propagate t ∘ propagate s`. |
| H3 | Linear | `Hypothesis_Linear` | `propagate t` is `ℝ`-linear for all `t`. |
| H4 | Complex | `Hypothesis_Complex` | State is a complex vector space and propagation is complex-linear. |
| H5 | Finite-dimensional | `Hypothesis_FiniteDimensional` | State is a finite-dimensional `ℝ`-vector space. |
| H6 | Dimension = 3 | `Hypothesis_DimensionThree` | `State` is 3-dimensional. |
| H7 | Postulate D | `Hypothesis_PostulateD` | Coupling matrix has zero diagonal (`M i i = 0`). Formalized, not `True`. |
| H8 | Coherence | `Hypothesis_Coherence` | **Two independent premises** combined under one name: (a) approximate return to a state within `d(s, propagate τ s) < causal_velocity * τ`, and (b) Lyapunov-style stability of nearby orbits. It is **not** exact periodicity, and it is **not ordered by implication** with exact periodicity (stability is an added premise, not implied by periodicity). |
| H9 | Causal velocity | `Hypothesis_CausalVelocity` | `causal_velocity > 0` and `d(s, propagate t s) ≤ causal_velocity * t` for all `t ≥ 0`. This is what makes `d` and `causal_velocity` a meaningful pair; H8 does not assume it. |
| H10 | Scale invariance | `Hypothesis_ScaleInvariance` | Strong self-similarity under rescaling. Not assumed by any other axiom. |
| H11 | Stability | `Hypothesis_Stability` | Uniform eigenvalue `c ≥ 0` and residue eigenvalue `λ < 0`. Used with `ArbitraryD` to select D=3. |
| **H12** | **Permutation symmetry** | `Hypothesis_PermutationSymmetry` | Coupling matrix invariant under **all** permutations `S_D`. This forces the 2-parameter form `a` on-diagonal, `b` off-diagonal. |
| **H13** | **Cyclic symmetry** | `Hypothesis_CyclicSymmetry` | Coupling matrix invariant under **cyclic** permutations `Z_D`. Weaker than H12. For D=3 this is the Z₃ circulant structure. |
| H14 | Isometry | `Hypothesis_Isometry` | `propagate(t,·)` preserves the bare distance `d` for all `t`. Does NOT imply periodicity (irrational torus rotation is a counterexample). Structurally incompatible with J-I contraction: `full_norm_T3_strictly_decreases` proves T³ decreases the full Euclidean norm for non-uniform states. |
| H15 | Metric identity | `Hypothesis_MetricIdentity` | `d(s₁,s₂) = 0 → s₁ = s₂`. Minimal metric axiom needed to connect H14 to reversibility (H1). |
| H16 | Metric reflexivity | `Hypothesis_MetricReflexivity` | `d(s,s) = 0` for all `s`. Minimal metric axiom needed to connect H14 + H15 to reversibility (H1). |
| H17 | Matrix symmetry | `Hypothesis_MatrixSymmetry` | `M(i,j) = M(j,i)` for all `i,j`. Named and formalized in `Axioms.lean`. Distinguish from H12 (permutation symmetry of propagation) and H13 (cyclic symmetry). H17 is a property of the coupling matrix itself. |
| H18 | Equal row sums | `Hypothesis_EqualRowSums` | `∑ⱼ M i j = c` for all `i`. Named and formalized in `Axioms.lean`. Used in `Z3FromBareMedium` D3 uniqueness and in the Entropy counterexample. |

> **Note:** `Axioms.lean` defines H12 as full permutation symmetry and H13 as cyclic
> symmetry. This ledger follows the source. Any older document that reverses them is
> stale. H14/H15/H16 are the isometry/metric axioms introduced in the H8 closure
> experiments (2026-06-25). H17/H18 are the previously-hidden equal-row-sums and
> matrix-symmetry premises, now formalized (2026-06-26).

---

## What H8 is and is not

H8 is a **named pair of premises**: approximate recurrence + Lyapunov stability.

- It is **not** exact periodicity.
- It is **not** "strictly weaker than exact periodicity" in a logical-implication sense,
  because the stability half is an additional premise not implied by exact periodicity.
- The phrase "light-cone distance" is informal. `d` is only a bare function
  `State → State → ℝ` in `BareMedium`; pseudometric/causal laws are H9, and H8's
  recurrence clause is meaningful even without them.
- H8 + H3 + H2 + H5 proves **only the trivial zero fixed point** from linearity.
  H8's hypotheses are unused in that proof.

---

## H14 → H1 chain: honest cost

`isometry_implies_reversible` in `Axioms.lean` is **proven** (machine-verified,
no `sorry`). It shows:

| Required premise | Cost | Why it is needed |
|------------------|------|------------------|
| H14 (Isometry) | 1 | Distance preservation under propagation |
| H15 (Metric identity) | 1 | `d(s₁,s₂)=0 → s₁=s₂`; without it `d` could be zero everywhere |
| H16 (Metric reflexivity) | 1 | `d(s,s)=0`; needed for the base case `d(s,s)=0` |
| **Total** | **3** | **H14+H15+H16 → H1 (Reversibility)** |

This is an honest result: isometry plus two minimal metric axioms gives
injectivity. It does **not** give periodicity (irrational torus rotation is
isometric and recurrent but never exactly periodic). Closing the gap from
reversibility to symmetry / J-I requires additional premises.

---

## H17 / H18: Equal row sums and matrix symmetry — now formalized

Both conditions are now named hypotheses in `Axioms.lean` (2026-06-26).

| Property | Lean name | Status | Cost |
|----------|-----------|--------|------|
| Matrix symmetry | `Hypothesis_MatrixSymmetry` | **Formalized as H17** | 1 if independent of H7/H12/H13 |
| Equal row sums | `Hypothesis_EqualRowSums` | **Formalized as H18** | 1 if independent of H7/H12/H13 |

Where they appear:
- `degenerate_residue_forces_circulant` (H7 + equal row sums + degenerate residue)
- `D3_symmetric_zero_diag_equal_rows_forces_JI` (H7 + H17 + H18)
- `D4_symmetric_zero_diag_equal_rows_not_unique_JI` (H7 + H17 + H18 at D=4)
- `non_symmetric_cooling_counterexample` (H7 + H17, without H18)

Physical origin: **Unresolved**. Both are structural regularities of the coupling matrix, not derived from `BareMedium`.

---

## Zero-Orbit Theorem (vacuous)

`recurrence_stability_plus_structural_gives_periodic_orbit` in `Axioms.lean` is
**proven** but **vacuous**: the zero vector is always a fixed point of a linear
semigroup. The Lean proof uses H3 (linearity/typeclass structure) only.

- **H8, H2, and H5 are unused** in the proof (the compiler reports `hCoh`, `hSemi`,
  and `hFin` as unused).
- The theorem establishes **only** that the zero orbit is periodic from H3 plus
  algebraic typeclass structure.
- The non-zero version `recurrence_stability_plus_structural_gives_nonzero_periodic_orbit`
  is a `sorry` frontier theorem. It is expected to be **false as stated** (informal
  counterexample; no Lean countermodel yet): `propagate(t, v) = exp(-t)·v` on `ℝ²` is linear, semigroup,
  finite-dimensional, Lyapunov stable, but has no non-zero periodic orbit. The
  counterexample is **not formalized in Lean**.

---

## Z₃ Circulant Derivation Chain (honest)

The four machine-verified theorems in `PfLean.Z3FromBareMedium.lean` are:

1. `degenerate_residue_forces_circulant`:
   - **Premises:** zero diagonal (H7) + equal row sums + degenerate residue.
   - **Conclusion:** `M = c/(D-1) · (J-I)`.
   - **Status:** Proven, no `sorry`.

2. `D3_circulant_degenerate_iff_symmetric`:
   - **Premises:** D=3, zero diagonal, circulant.
   - **Conclusion:** degenerate residue ↔ `b = c` (symmetry condition).
   - **Status:** Proven, no `sorry`.

3. `D3_symmetric_zero_diag_equal_rows_forces_JI`:
   - **Premises:** D=3, zero diagonal (H7), matrix symmetry (H17), equal row sums (H18).
   - **Conclusion:** `M = (c/2) · (J-I)`.
   - **Status:** Proven, no `sorry`.

4. `D4_symmetric_zero_diag_equal_rows_not_unique_JI`:
   - **Premises:** D=4, zero diagonal (H7), matrix symmetry (H17), equal row sums (H18).
   - **Conclusion:** there exists a non-J-I matrix satisfying all three premises.
   - **Status:** Proven, no `sorry`. D=3 uniqueness is dimension-dependent.

5. `D_selection_principle`:
   - **Premises:** D ≥ 2, plus the two conditions below.
   - **Conclusion:** D=3 is the unique dimension where (1) symmetric + zero-diagonal + equal-row-sum matrices collapse to J-I, and (2) the J-I God Equation has a frozen uniform mode and decaying residue modes.
   - **Status:** Proven, no `sorry`. This is the D-selection principle: H11 (Stability) selects D=3.

### What is NOT established

- Neither theorem derives **degenerate residue** from non-symmetric premises.
- The theorem narrows *which* symmetry (J-I) follows from the degenerate-residue
  premise, but it does **not** derive symmetry from non-symmetric physics.
- The load-bearing question — **what physical condition forces degenerate residue?** —
  remains **OPEN**.

### Honest parameter count for Z₃ circulant structure

To reach the J-I form at least:
- H3 (linearity) + H5 (finite-dim) + H7 (zero diagonal) + **degenerate residue**.
- Degenerate residue is the premise whose physical origin is unresolved.
- If one assumes H12 (permutation symmetry), then equal row sums + zero diagonal
  give the symmetric form, but that is a **symmetry-for-symmetry** route, not a
  derivation of symmetry from BareMedium.

### D≥4 gap: D=3 is special

For D=3, the combination of **symmetry + zero diagonal + equal row sums**
forces the J-I form. For D≥4, it does **not**.

Counterexample (machine-verified in `D4_symmetric_zero_diag_equal_rows_not_unique_JI`):
```
M = [[0,2,0,1],
     [2,0,1,0],
     [0,1,0,2],
     [1,0,2,0]]
```
- Zero diagonal (H7)
- Symmetric (H17)
- Equal row sums = 3
- **NOT J-I**: off-diagonals are 1 and 2, not all equal.

This means the D=3 uniqueness result is **dimension-dependent**. The honest
question is not "why is the matrix J-I?" but "why is D=3 the relevant
dimension?" The answer is now machine-verified as `D_selection_principle`:
- H11 (stability) + H7 + H17 + H18 selects D=3 uniquely.
- D=3 is the only dimension where the symmetric zero-diagonal equal-row-sum
  family collapses to J-I AND the J-I God Equation is stable.
- H6 (Dimension = 3) can now be seen as a consequence of H11 + H7 + H17 + H18,
  not an independent posit. The D-selection principle is closed.

---

## Intentional `sorry` boundaries (epistemic markers)

| Theorem | Why it is `sorry` |
|---------|-------------------|
| `recurrent_mode_bare` | BareMedium does not supply the H8 content. |
| `recurrent_mode_from_H3_H2` | Real linear semigroups need complex structure for periodicity; the real-semigroup argument is informal. |
| `recurrent_mode_from_H1` | Reversibility/injectivity does not imply periodicity; the translation example is informal. |
| `recurrence_stability_plus_structural_gives_nonzero_periodic_orbit` | Frontier theorem; informal contraction evidence suggests it is expected false as stated. No Lean countermodel yet. |

---

## `PfLean.Entropy` — PF Entropy as Residue Tension

`PfLean/Entropy.lean` is a **downstream** module. It does not derive J-I; it measures what J-I does.

### Theorem results (all machine-verified, no sorry)

| Theorem | What it says |
|---------|--------------|
| `PFEntropy` | Euclidean norm of residue component `Q(x)` — distance from uniform mode |
| `uniform_state_zero_entropy` | Uniform states have zero PF Entropy |
| `uniform_state_unique_min_entropy` | Uniform state is the unique minimizer |
| `PFEntropy_decreases_T3` | T³ scales residue by `-1/8`, so PF Entropy decreases by factor `1/8` |
| `PFEntropy_T3_decreases` | PF Entropy is non-increasing under stable discrete dynamics |
| `PFEntropy_residue_dimension` | At D=3, residue subspace is 2/3 of state space |
| `P0_Q_dot_zero` | Uniform and residue components are orthogonal in Euclidean inner product |
| `full_norm_Pythagorean` | Full norm² = P₀ norm² + PF Entropy² |
| `full_norm_T3_strictly_decreases` | T³ strictly decreases full Euclidean norm for non-uniform states — J-I + isometry is inconsistent |

### Honest parameter cost

PF Entropy is derived, not primitive. It requires:

| Premise | Cost | Why it is needed |
|---------|------|------------------|
| H3 (Linearity) | 1 | Residue subspace is a linear complement |
| H5 (Finite-dimensional) | 1 | Norms exist; eigenvalue structure is finite |
| H7 (Postulate D) | 1 | Zero diagonal, part of J-I definition |
| H11 (Stability) | 1 | Negative residue eigenvalue guarantees decrease |
| J-I coupling matrix | 1 | Specific structure from `ArbitraryD` / `Z3FromBareMedium` |
| **Total** | **5** | **Downstream theorem, not upstream premise** |

### Boundary

- PF Entropy is **not** thermodynamic entropy or Shannon entropy.
- It measures the **cooling** half of PF dynamics only.
- It does **not** address the oscillatory/standing-wave component.
- It does **not** solve the upstream question of why the coupling matrix is J-I.
- **PF Entropy is a DOWNSTREAM property of J-I, not an upstream selector.** Entropy decrease + H7 (zero diagonal) + H18 (equal row sums) is **insufficient** to force J-I (proven via the non-symmetric circulant counterexample in `Entropy.lean`).
- **Isometry-JI incompatibility:** `full_norm_T3_strictly_decreases` proves J-I dynamics + H14 (isometry) is inconsistent. T³ preserves P₀ and scales Q by -1/8, so the full Euclidean norm strictly decreases for non-uniform states. Isometry does not bridge to J-I.
- Entropy documents cooling dynamics; the open question of what forces J-I is addressed by the H17/H18 symmetry posits and the D-selection principle.

### Phase 2: Selection principle (frontier)

| Theorem | Status | What it says |
|---------|--------|--------------|
| `non_symmetric_cooling_counterexample` | **PROVEN** | A non-symmetric circulant with zero diagonal + equal row sums is not J-I but still has decaying residue modes. Kills "entropy decrease + zero diagonal + equal row sums → J-I". |
| `entropy_decrease_constrains_residue` | **FRONTIER** | If PF Entropy decreases for all states, residue eigenvalues are non-positive. `True` stub; needs spectral theory scaffolding to make rigorous. |

**Honest conclusion from Phase 2:** Entropy decrease is **necessary but not sufficient** for J-I. The gap is "uniform cooling" (degenerate residue), which is an independent posit. The selection principle "what matrix minimizes PF Entropy?" has a unique answer only after adding symmetry or uniform-cooling premises.

---

## What is not claimed here

- This is not a proof of H8, periodicity, non-zero recurrence, Z₃ emergence, or
  symmetry from PF axioms alone.
- It is not a physics-claim upgrade or a globally `sorry`-free certification.
- Fundamentals PUBLIC HOLD remains unchanged.
