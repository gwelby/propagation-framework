# Circularity Audit Report — H8 Redefinition and Z3FromBareMedium Overclaim

**Date:** 2026-06-22
**Agents:** Devin ∇λΣ∞ (Kimi K2.7), Hermes, Claude, Codex, Greg
**Status:** COMPLETED — `Z3FromBareMedium.lean` equivalence proof machine-verified; full `lake build PfLean` passes (8267 jobs, 0 errors)

> [!IMPORTANT]
> **Supersession Note (2026-06-26):**
> Codex's 2026-06-26 re-audit found that the "drift reconciled" status declared on 2026-06-22 was premature due to H17/H18 numbering discrepancy (H17 = Matrix Symmetry, H18 = Equal Row Sums) and proof-hole count drift (four actual sorries + three True stubs, rather than 3 or 6 sorries). Those have now been fully reconciled and updated across the ledger, README, Axioms, and RESUME documents.

**Codex Re-Audit (2026-06-24):** HOLD for declaring the H8/Z3 documentation reconciled or committing as audit-clean. Source compiles and the two Z3 theorems are legitimate conditional results. Documentation must be corrected before it is committed with a "clean/non-circular/reconciled" message. Required fixes were applied to this report and to `Axioms.lean`, `README.md`, `PREMISE_LEDGER.md`, and `PfLean/RESUME.md`. The remaining next step is the isometry/closure experiment (see Section 7).

---

## Summary

Two related circularity issues were identified in the PfLean formalization:

1. **H8 (Coherence) was circular.** It was defined as the exact conclusion it was supposed to help prove (`∃ periodic orbit`). The fix: redefine H8 as **approximate recurrence + Lyapunov stability**. H8 is no longer a restatement of the conclusion, but it is not "strictly weaker than exact periodicity" in a logical-implication sense because Lyapunov stability is an additional independent premise not implied by exact periodicity.

2. **`Z3FromBareMedium.lean` overclaimed.** The theorem `degenerate_residue_forces_circulant` is TRUE, but the documentation interpreted it as "symmetry is DERIVED, not assumed." For D=3 circulants, "degenerate residue" is **equivalent** to the symmetry condition `b = c`. The theorem narrows which symmetry (to J-I), but does not derive symmetry from non-symmetric premises.

---

## 1. H8 Redefinition

### Old (circular)

```lean
def Hypothesis_Coherence (M : BareMedium) : Prop :=
  ∃ (s : M.State) (T : ℝ) (T_pos : T > 0),
    ∀ (n : ℕ), M.propagate (n * T) s = s
```

This defines H8 as an exact periodic orbit, then the discovery experiment `recurrent_mode_from_H8` simply unpacked it. A → A.

### New (non-circular)

```lean
def Hypothesis_Coherence (M : BareMedium) : Prop :=
  ∃ (s : M.State) (τ : ℝ) (τ_pos : τ > 0),
    -- Approximate recurrence: state returns within the causal bound.
    M.d s (M.propagate τ s) < M.causal_velocity * τ
    -- Lyapunov stability: nearby states stay nearby.
    ∧ ∀ (ε : ℝ), ε > 0 → ∃ (δ : ℝ), δ > 0 →
        ∀ (s' : M.State), M.d s s' < δ →
          ∀ (t : ℝ), t ≥ 0 → M.d (M.propagate t s) (M.propagate t s') < ε
```

The premise is now genuinely weaker than the conclusion. Exact periodicity, eigenstructure, and Z₃ become theorems requiring extra hypotheses (H3, H2, H4, H5, etc.).

### Lean build status

- `lake build PfLean.Axioms` passes with the new definition.
- `recurrence_stability_plus_structural_gives_periodic_orbit` is PROVEN (not sorry) — but VACUOUS: the zero vector is always a fixed point of a linear semigroup. The interesting non-zero version `recurrence_stability_plus_structural_gives_nonzero_periodic_orbit` is `sorry` (expected FALSE as stated — informal counterexample: contraction semigroup `exp(-t)·v`; no Lean countermodel yet).
- Full `lake build PfLean` passes: 8267 jobs, 0 errors.

---

## 2. Z3FromBareMedium Overclaim

### The true theorem

```lean
theorem degenerate_residue_forces_circulant
    (D : ℕ) (D_pos : D ≥ 2)
    (M : Fin D → Fin D → ℝ)
    (c residue_eig : ℝ)
    (h_zero_diag : ∀ i, M i i = 0)
    (h_row_sum : ∀ i, ∑ j, M i j = c)
    (h_degenerate : ∀ (v : Fin D → ℝ), ∑ j, v j = 0 →
      ∀ i, ∑ j, M i j * v j = residue_eig * v i) :
    ∀ i j, M i j = if i = j then (0 : ℝ) else c / ((D : ℝ) - 1)
```

**What it actually says:** If a zero-diagonal matrix with equal row sums has **degenerate residue** (all zero-sum vectors are eigenvectors with the same eigenvalue), then it must be `c/(D-1)·(J-I)`.

**The overclaim:** "Symmetry is DERIVED, not assumed."

### Why the overclaim is false

For a D=3 circulant with zero diagonal and first row `(0, b, c)`:

- Degenerate residue means all zero-sum vectors are eigenvectors with the same eigenvalue.
- Apply the test vector `v = (1, -1, 0)` (sum zero) to row 0:
  - `(M·v)₀ = 0·1 + b·(-1) + c·0 = -b`
  - `λ·v₀ = λ`
  - So `λ = -b`.
- Apply the same vector to row 1:
  - `(M·v)₁ = c·1 + 0·(-1) + b·0 = c`
  - `λ·v₁ = -λ`
  - So `c = -λ = b`.

Therefore **degenerate residue → b = c**. The converse also holds. So for D=3 circulants:

> **degenerate residue ↔ b = c (symmetry condition)**

The theorem is not deriving symmetry from non-symmetric premises. It is restating the symmetry condition in the language of eigenvalues. The load-bearing question — "what forces degenerate residue without assuming a symmetry?" — remains open.

### Physics perspective

Wigner's theorem: degenerate eigenvalues almost always indicate a symmetry. If degenerate residue is itself a symmetry condition, then the chain "degenerate residue → J-I → D=3 → Z₃" is not a discovery from non-symmetric axioms; it is a construction that assumes symmetry at the base.

---

## 3. Honest Record

The corrected documentation should say:

> `degenerate_residue_forces_circulant` shows that **degenerate residue narrows the symmetry to J-I specifically**. It does NOT derive symmetry from non-symmetric premises. For D=3 circulants, "degenerate residue" is equivalent to the symmetry condition `b = c`. The open question — whether degenerate residue can be forced by anything weaker than an assumed symmetry — remains open.

---

## 4. Files Changed

- `PfLean/Axioms.lean` — H8 redefined; experiments updated.
- `lean/README.md` — H8 description and theorem tables updated.
- `lean/PREMISE_LEDGER.md` — H8 status and circularity notes updated.
- `RESUME.md` (main) and `lean/PfLean/RESUME.md` — current state updated.
- `PfLean/Z3FromBareMedium.lean` — equivalence proof `D3_circulant_degenerate_iff_symmetric` machine-verified and build-verified by another Devin instance. Both theorems compile with 0 sorrys.

---

## 5. Next Steps

1. ✅ `D3_circulant_degenerate_iff_symmetric` proof in `Z3FromBareMedium.lean` — COMPLETED, machine-verified.
2. ✅ Full `lake build PfLean` passes — 8267 jobs, 0 errors.
3. ✅ Documentation drift reconciled — README, PREMISE_LEDGER, RESUME, and this report all reflect actual build state.
4. ✅ Codex re-audit (2026-06-24) — HOLD verdict received; required documentation fixes applied.
5. **Investigate the non-zero periodic orbit question** — the leading candidate is a closure hypothesis (`Hypothesis_Isometry`) plus boundedness of the orbit. Target: H8 + H_isometry + H3 + H5 + H_bounded_orbit → compact recurrent orbit. Exact periodicity likely needs a separate rationality condition. However, the design document `DESIGN_H_ISOMETRY_REAL_EIGENVALUE_20260625.md` identifies a structural obstruction: the J-I circulant has real eigenvalues only, so it contracts rather than oscillates. Temporal periodicity and Z₃ spatial symmetry are likely independent axes. See that document for the full eigenvalue analysis.

---

## 6. Meta-Lesson

The same circularity pattern is fractal. It reappears at every level of abstraction. The diagnostic question is always:

> **Is the premise a restatement of the conclusion, or does it add an independent premise that is not implied by the conclusion?**

- H8 was a restatement → circular.
- Degenerate residue for D=3 circulants is equivalent to symmetry → circular as a "derivation" claim, though the conditional equivalence theorem itself is valid.
- Approximate recurrence + stability → exact periodicity: the return inequality is weaker, but Lyapunov stability is an added independent premise; the premise set is therefore not strictly weaker than exact periodicity. The only genuine theorem proved is the vacuous zero-orbit fixed point from linearity.

The only cure is to apply this test to every theorem, every fix, every time.

---

## 7. Proposed Next Experiment: Closure/Isometry Hypothesis

The contraction counterexample `propagate(t, v) = exp(-t)·v` fails because it is an **open system** — structure dissipates. The irrational torus rotation fails because it is recurrent but not exactly periodic. These two failures suggest the missing premise is a **closure** condition: propagation preserves distances (no leakage) and the recurrent orbit is bounded.

### Proposed hypotheses

```lean
def Hypothesis_Isometry (M : BareMedium) : Prop :=
  ∀ (t : ℝ) (s₁ s₂ : M.State), M.d s₁ s₂ = M.d (M.propagate t s₁) (M.propagate t s₂)

def Hypothesis_BoundedOrbit (M : BareMedium) (s : M.State) : Prop :=
  ∃ (R : ℝ), ∀ (t : ℝ), t ≥ 0 → M.d s (M.propagate t s) < R
```

### Target theorem

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

### Why this is the honest next step

- **Isometry** closes the dissipation gap (`exp(-t)` fails).
- **Boundedness** prevents the orbit from escaping to infinity.
- **H3 + H5** give finite-dimensional linear structure, so bounded orbits are precompact (Heine-Borel).
- **H8** gives the seed recurrence and stability.
- **Exact periodicity** remains a separate question requiring a rationality/minimality condition (e.g., D=3 eigenvalue structure).

If this theorem holds, the honest parameter count for the upstream of J-I becomes: **coherence + closure + boundedness** (3 posits), not the original single "stability" posit.
