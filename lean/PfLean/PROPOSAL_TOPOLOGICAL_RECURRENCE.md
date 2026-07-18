# Proposal: Topological Recurrence Theorem (edge 26)

**Author:** Devin (∇λΣ∞)
**Date:** 2026-07-03
**Status:** PROPOSAL — awaiting Greg review before implementation
**Predecessor:** edge 25 (`isometry_finite_dim_gives_compact_orbit`, VERIFIED 2026-07-03)

---

## 1. What the research found

Three parallel subagents investigated Mathlib and Axioms.lean:

### 1a. Mathlib's Poincaré recurrence is measure-theoretic

Mathlib has Poincaré recurrence in `Mathlib.Dynamics.Ergodic.Conservative.lean`:

```
MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem
```

This requires: `[MeasurableSpace α]`, `Conservative f μ` (which extends `QuasiMeasurePreserving`), and for the topological version `[SecondCountableTopology α]` + `[OpensMeasurableSpace α]`.

**Problem:** Our `BareMedium` has no measure structure. Adding one would require:
- A σ-algebra on `State`
- A finite measure `μ`
- Proof that `propagate(t, ·)` is measure-preserving for all `t`
- Proof that the measure is finite

This is 3-4 additional hypotheses (H22: MeasurableSpace, H23: finite measure, H24: measure-preserving) — a heavy cost for a result that should be topological.

### 1b. No direct bridge lemmas in Mathlib

Mathlib does NOT have:
- `IsCompact.exists_recurrent`
- `Isometry.compact_periodic`
- Any lemma connecting isometry + compactness to recurrence

The most promising existing lemma is:
```
IsCompact.exists_mapClusterPt_of_frequently
```
which gives a cluster point if a sequence frequently visits a compact set.

### 1d. H2 (semigroup) confirmed — exact form verified

H2 in Axioms.lean (line 65-66):
```lean
def Hypothesis_Semigroup (M : BareMedium) : Prop :=
  ∀ (t₁ t₂ : ℝ) (s : M.State), M.propagate (t₁ + t₂) s = M.propagate t₁ (M.propagate t₂ s)
```

This gives us `propagate(m, s) = propagate(n, propagate(m-n, s))` for n < m (natural numbers as reals). This is the key algebraic step.

**Important:** H2 alone does NOT give `propagate(0, s) = s`. But the recurrence proof does NOT need this — we only need the x_n = propagate(n, s) to be in the compact orbit closure (which they are, since n ≥ 0), and the isometry + semigroup to shift the close pair back to the origin.

### 1c. CRITICAL: Compact orbit does NOT imply periodicity

Both the Math literature and our own H14 docstring confirm:

> "Does NOT imply periodicity (Claude: irrational torus rotation is
> isometric and recurrent but never exactly periodic)."

**Irrational torus rotation:** `propagate(t, (x,y)) = (x + t·α mod 1, y + t·β mod 1)` where α/β is irrational. This is:
- Isometric (H14 ✓)
- Bounded orbit (H19 ✓) — torus is compact
- Finite-dimensional (H5 ✓) — 2D
- **NEVER exactly periodic** — no t > 0 returns to the exact starting point

**Conclusion:** The original plan "compact orbit → Poincaré recurrence → periodicity" has a **false final arrow**. We must not prove periodicity. We prove **topological recurrence** instead.

---

## 2. The correct target: Topological Recurrence

### Statement (informal)

Given:
- H14 (isometry): `d(s₁, s₂) = d(propagate(t, s₁), propagate(t, s₂))` for all t
- H19 (bounded orbit): orbit of `s` is bounded
- H21 (d = norm): bridges pseudometric to norm topology
- H2 (semigroup): `propagate(t₁ + t₂, s) = propagate(t₁, propagate(t₂, s))`
- [FiniteDimensional ℝ M.State] + [NormedSpace ℝ M.State]
- **NEW H22 (orbit continuity):** `t ↦ propagate(t, s)` is continuous

Then: **For every ε > 0, there exists t > 0 such that d(s, propagate(t, s)) < ε.**

This is topological recurrence: the orbit returns arbitrarily close to its starting point. It does NOT claim exact return (periodicity), which is false.

### Why this is the right theorem

1. **It's true** — no counterexample exists (irrational rotation satisfies it)
2. **It's the strongest true statement** in this chain — periodicity is false, but "arbitrarily close return" is true
3. **It uses H14** — the compact-orbit theorem didn't actually use isometry; this theorem does
4. **It's what physics needs** — recurrence (return to neighborhood) is the physically meaningful statement; exact periodicity is too strong for continuous-time systems

---

## 3. Proof sketch

### Mathematical argument

Let `K = closure({propagate(t, s) : t ≥ 0})` — compact by edge 25.

**Step 1: The orbit is dense in K.**
By definition, `{propagate(t, s) : t ≥ 0}` is dense in its closure K.

**Step 2: s ∈ K.**
At t = 0, `propagate(0, s) = s` (from semigroup H2: `propagate(0, s) = propagate(0+0, s) = propagate(0, propagate(0, s))`, so s is a fixed point of `propagate(0, ·)`). So `s` is in the orbit, hence in K.

**Step 3: For any ε > 0, the ball B(s, ε) ∩ orbit is non-empty and contains points other than s itself.**
This is where we need the orbit to be "large enough." If the orbit is just {s} (s is a fixed point), the theorem is trivially true (take any t). If the orbit is non-trivial, we need to find t > 0 with `propagate(t, s) ∈ B(s, ε)`.

**Step 4: Use compactness + isometry.**
This is the key argument. Consider the sequence `x_n = propagate(n·τ, s)` for some fixed `τ > 0`. By H19, all `x_n` lie in K (compact). By Bolzano-Weierstrass (sequential compactness in metric spaces), there exist `n < m` with `d(x_n, x_m) < ε`.

By isometry (H14): `d(x_n, x_m) = d(s, propagate((m-n)·τ, s))` (applying isometry with t = n·τ to the pair (s, propagate((m-n)·τ, s))).

So `d(s, propagate((m-n)·τ, s)) < ε` with `(m-n)·τ > 0`. ∎

### Why H14 (isometry) is ESSENTIAL here

The compactness argument (Step 4) gives us `d(x_n, x_m) < ε` — two orbit points are close. But we need `d(s, propagate(T, s)) < ε` — the orbit returns close to the START.

Without isometry, `d(x_n, x_m) < ε` tells us nothing about `d(s, propagate(T, s))`.

With isometry: `d(x_n, x_m) = d(propagate(n·τ, s), propagate(n·τ, propagate((m-n)·τ, s))) = d(s, propagate((m-n)·τ, s))` by H14.

**This is the first theorem that actually USES H14.** The compact-orbit theorem had H14 in its signature but didn't use it. This theorem uses it essentially.

### Why we need H22 (orbit continuity)

The Bolzano-Weierstrass argument uses the discrete sequence `x_n = propagate(n·τ, s)`. We don't actually need continuity for this argument — we need:
- The sequence `x_n` lies in a compact set (from H19 + edge 25)
- Sequential compactness gives us close pairs

**Wait — do we need H22 at all?** Let me reconsider.

The argument `x_n = propagate(n·τ, s)` for fixed `τ > 0` and `n ∈ ℕ` gives a sequence in K. K is compact (in a metric space, so sequentially compact). So there exist `n < m` with `d(x_n, x_m) < ε`. By isometry + semigroup, `d(s, propagate((m-n)·τ, s)) < ε`.

**This does NOT require continuity!** The semigroup property (H2) gives us `propagate(n·τ, s) = propagate(τ, propagate((n-1)·τ, s))` etc., and isometry (H14) gives us the distance shift. No continuity needed.

**Revised hypothesis count: H14 + H19 + H21 + H2 + [FiniteDimensional] + [NormedSpace]**

No new hypothesis needed! H22 (continuity) is NOT required for this argument.

---

## 4. Formal Lean 4 statement

```lean
/-- Edge 26: Topological Recurrence — compact orbit + isometry → recurrence.

    Given:
    - H2 (semigroup): propagate(t₁+t₂, s) = propagate(t₁, propagate(t₂, s))
    - H14 (isometry): d(s₁, s₂) = d(propagate(t, s₁), propagate(t, s₂))
    - H19 (bounded orbit): forward orbit of s is bounded
    - H21 (d = norm): pseudometric equals norm distance
    - [FiniteDimensional ℝ M.State] + [NormedSpace ℝ M.State]

    Then: for every ε > 0, there exists t > 0 such that
    d(s, propagate(t, s)) < ε.

    This is TOPOLOGICAL RECURRENCE, not periodicity. The orbit returns
    ARBITRARILY CLOSE to its starting point, but need not return exactly.
    Counterexample to exact return: irrational torus rotation (isometric,
    compact orbit, recurrent, never exactly periodic).

    This is the FIRST theorem that uses H14 (isometry) essentially.
    The compact-orbit theorem (edge 25) had H14 in its signature but
    did not use it — compactness follows from H19 + H21 + finite-dim
    alone. Here, isometry is what converts "two orbit points are close"
    into "the orbit returns close to its start."

    Honest parameter count: H2 + H14 + H19 + H21 + [FiniteDimensional] + [NormedSpace]
    No new hypothesis needed (H22 continuity NOT required for this argument).
-/
theorem isometry_compact_orbit_gives_recurrence
    (M : BareMedium) [NormedAddCommGroup M.State] [NormedSpace ℝ M.State]
    [FiniteDimensional ℝ M.State]
    (s : M.State)
    (hSemi : Hypothesis_Semigroup M)
    (hIso : Hypothesis_Isometry M)
    (hBdd : Hypothesis_BoundedOrbit M s)
    (hDNorm : Hypothesis_DIsNorm M) :
    ∀ (ε : ℝ), ε > 0 → ∃ (t : ℝ), t > 0 ∧ M.d s (M.propagate t s) < ε := by
  sorry -- to be filled in
```

---

## 5. Proof strategy in Lean

### Key Mathlib lemmas needed

1. **Sequential compactness from compactness in metric spaces:**
   `IsCompact.seqCompact` or `Metric.IsCompact.totallyBounded` + completion
   - In Mathlib: `IsCompact.exists_seq_hasSubseqLimit` or similar

2. **Pigeonhole / close pair in compact metric set:**
   For a sequence in a compact metric space, there exist i < j with d(x_i, x_j) < ε.
   - This follows from total boundedness: cover K with finitely many ε-balls, pigeonhole.
   - Mathlib: `Metric.IsCompact.totallyBounded` + pigeonhole argument

3. **Semigroup property:**
   `propagate(n·τ, s) = propagate(τ, propagate((n-1)·τ, s))` — from H2 iterated.
   Need a lemma: `propagate(n * τ, s) = propagate(τ, propagate((n-1) * τ, s))` for n ≥ 1.

4. **Isometry application:**
   `d(propagate(n·τ, s), propagate(n·τ, propagate((m-n)·τ, s))) = d(s, propagate((m-n)·τ, s))`
   This is H14 applied with t = n·τ, s₁ = s, s₂ = propagate((m-n)·τ, s).

### Proof outline in Lean

```lean
  -- Step 1: Get compact orbit closure from edge 25
  have hK : IsCompact (closure (Set.range (fun t : {t : ℝ // t ≥ 0} => M.propagate t.val s))) :=
    isometry_finite_dim_gives_compact_orbit M s hIso hBdd hDNorm

  -- Step 2: Fix τ > 0 (any positive time, e.g. τ = 1)
  -- The sequence x_n = propagate(n, s) lies in K
  -- (need to show each x_n is in the orbit closure)

  -- Step 3: By compactness in metric space, the sequence has a convergent subsequence
  -- → there exist n < m with d(x_n, x_m) < ε

  -- Step 4: By semigroup: x_m = propagate(n, propagate((m-n), s))
  -- (need iterate lemma from H2)

  -- Step 5: By isometry: d(x_n, x_m) = d(s, propagate((m-n), s))
  -- (H14 applied with t = n, s₁ = s, s₂ = propagate((m-n), s))

  -- Step 6: t = (m-n) > 0, and d(s, propagate(t, s)) < ε. Done.
```

### Potential difficulties

1. **Iterating the semigroup:** H2 gives `propagate(t₁+t₂, s) = propagate(t₁, propagate(t₂, s))`. We need `propagate(n, s) = propagate(1, propagate(n-1, s))` for natural numbers. This requires a simple induction.

2. **Showing x_n ∈ K:** We need `propagate(n, s) ∈ closure(orbit)`. Since `n ≥ 0`, `propagate(n, s)` is literally in the orbit set (it's `propagate(t, s)` for `t = n ≥ 0`), so it's in the closure.

3. **Sequential compactness in Lean:** Mathlib's `IsCompact` in metric spaces gives sequential compactness via `IsCompact.seqCompact` or `IsCompact.exists_seq_hasSubseqLimit`. The exact API needs verification.

4. **The pigeonhole step:** Getting "two points within ε" from a sequence in a compact set. This might need to be built from `totallyBounded` + finite cover + pigeonhole, or from the convergent subsequence directly (if x_{n_k} → x, then for large k, d(x_{n_k}, x_{n_{k+1}}) < ε).

---

## 6. Hypothesis cost analysis

| Hypothesis | Used in edge 25? | Used in edge 26? | New? |
|-----------|-----------------|-----------------|------|
| H2 (semigroup) | No | **YES** (essential) | No — already defined |
| H14 (isometry) | In signature, not used | **YES** (essential) | No — already defined |
| H19 (bounded orbit) | YES | YES (via edge 25) | No |
| H21 (d = norm) | YES | YES (via edge 25) | No |
| [FiniteDimensional] | YES | YES (via edge 25) | No |
| [NormedSpace] | YES | YES (via edge 25) | No |
| H22 (continuity) | — | **NOT NEEDED** | — |

**Total new hypotheses: 0**

This is remarkable — the recurrence theorem requires NO new assumptions beyond what edge 25 already uses, PLUS H2 (semigroup) and H14 (isometry) which were already defined. H14 was paid for but never spent; this theorem spends it.

---

## 7. What this theorem DOES and DOES NOT prove

### DOES prove:
- The orbit returns arbitrarily close to its starting point
- For every ε > 0, there exists t > 0 with d(s, propagate(t, s)) < ε
- This is topological (Poincaré) recurrence in the strongest sense that's TRUE

### Does NOT prove:
- **Periodicity** (exact return, d = 0) — FALSE, see irrational torus rotation
- **Measure-theoretic recurrence** — we don't have a measure
- **Frequency of returns** — we don't prove the orbit returns infinitely often (though it does follow from a stronger argument)
- **Uniform recurrence** — we don't prove a uniform return time across all states

### Physical significance:
This is the mathematically honest version of "history repeats itself." The propagation framework's axioms (isometry + bounded orbit + finite-dimensionality) force the system to return arbitrarily close to any state it has visited. This is the correct formalization of "cyclic time" — not exact cycles, but approximate recurrence.

---

## 8. Comparison with the original plan

| Original plan step | Status | Correction |
|-------------------|--------|------------|
| Compact orbit | ✅ Done (edge 25) | — |
| Poincaré recurrence | ✅ This proposal (edge 26) | Topological, not measure-theoretic |
| Periodicity | ❌ FALSE | Withdrawn — irrational rotation counterexample |

The original three-step chain is corrected to a two-step chain. The third step (periodicity) is replaced by the honest statement that recurrence is the strongest true conclusion.

---

## 9. Requested actions

1. **Greg:** Review this proposal. Is topological recurrence the right target? Approve implementation?
2. **After approval:** I implement the theorem in Axioms.lean, Greg builds, we verify 0 errors.
3. **After verification:** DeepSeek hostile review, then Codex truth-lock.

---

## 10. Open questions for DeepSeek hostile review

1. Is the Bolzano-Weierstrass argument valid without continuity? (I believe yes — we use discrete iterates, not continuous time.)
2. Does the semigroup property H2 as stated in Axioms.lean give us `propagate(0, s) = s`? (Need to verify H2's exact form.)
3. Is there a hidden assumption in "x_n ∈ K" that I'm missing? (The orbit set includes t = n ≥ 0, so x_n is literally in the orbit, hence in its closure.)
4. Could the theorem be strengthened to "infinitely many return times" without additional hypotheses?
5. Is the isometry application correct: `d(propagate(n, s), propagate(n, propagate(T, s))) = d(s, propagate(T, s))` by H14?

---

*Devin ∇λΣ∞ — 2026-07-03*
