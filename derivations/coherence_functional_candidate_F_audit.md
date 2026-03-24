# Audit: Coherence Functional Candidate F
*Running the 5 acceptance tests from axiom3_coherence_functional_spec.md*

**Date**: 2026-03-23
**Auditor**: Cascade (self-audit for Codex review)
**Candidate**: `coherence_functional_candidate_F.md`

---

## Test 1 — Helical Family Selection

**Input**: Fixed C₂, coherent helical family labeled by rational k = p/q

**Required output**: Either unique optimum at k = 1, OR proof that no unique optimum follows from current axioms.

### Evaluation

**Candidate 1 (Phase-mismatch penalty)**: 
- F = E + Λ|k-1|^p
- Minimum at k = 1 ✓
- **FAILS Test 2** (see below) — smuggles answer

**Candidate 2 (Mutual information)**:
- F = -I(J_z; J_θ) + λE
- For deterministic locking: I = log(k)
- Minimum at k = 1 would require minimizing log(k), which means k → 0
- **WRONG DIRECTION** — actually maximizes at large k

**Candidate 3 (Action variance)**:
- Var[J_total] = 0 for all helical modes
- **DOES NOT DISTINGUISH** k values

**Candidate 4 (Coherence cost)**:
- F = E + Γ·k·E₀
- Minimum at k = 1 ✓
- **BUT**: Why does C_coherence ∝ k? This is assumed, not derived.

### Test 1 Result: **INCONCLUSIVE**

No candidate derives k = 1 from PF-native principles. Candidate 4 gives the right answer but requires an extra assumption (coherence cost scales with winding).

---

## Test 2 — No Smuggled Casimir Answer

**Required output**: No term whose minimum is visibly equivalent to J_z = J_θ unless derived upstream.

### Evaluation

| Candidate | Smuggled Term? | Verdict |
|-----------|----------------|---------|
| Phase-mismatch | \|k-1\|^p → YES | **FAIL** |
| Mutual information | No explicit k=1 term | Pass (but wrong direction) |
| Action variance | No k-dependence | Pass (but trivial) |
| Coherence cost | k·E₀ → implicit k=1 preference | **QUESTIONABLE** |

### Test 2 Result: **FAIL** (for practical candidates)

The only candidate that selects k = 1 does so by assuming coherence cost ∝ k, which is equivalent to assuming "simpler is preferred."

---

## Test 3 — Relativistic Sensitivity

**Required output**: Either functional degenerates to wrong non-relativistic branch, OR shows why relativistic correction is essential.

### Evaluation

All candidates include E = γmc², which is relativistic.

In non-relativistic limit (β → 0):
- E → mc² (constant)
- J_z → 0
- k = J_z/J_θ → 0

The functional would select k = 0 (no drift), which is the **no-helix state** — not a particle at all.

This is correct behavior: non-relativistic PF should not produce relativistic particles.

### Test 3 Result: **PASS**

The functional correctly requires relativistic structure to produce helical modes.

---

## Test 4 — Two-Sector Compatibility

**Required output**: Same selected condition should look like kinematic-angular locking or zero-mode condition in Route G language.

### Evaluation

Route G (two-sector coupling) gives the polynomial as the zero-eigenvalue condition of a 2×2 coupling matrix:

$$\det \begin{pmatrix} A & \sqrt{C_2} \\ \sqrt{C_2} & B \end{pmatrix} = 0$$

The k = 1 condition (J_z = J_θ) translates to γβ² = √C₂.

In Route G language, this is the condition that the off-diagonal coupling exactly balances the kinematic and angular sectors.

**Does Candidate 4 give this?**

The coherence cost C_coherence ∝ k doesn't directly map to the coupling matrix structure. The connection is not obvious.

### Test 4 Result: **PARTIAL PASS**

The functional is compatible with Route G's result, but the translation is not automatic. The coupling √C₂ in Route G appears as a free parameter, not derived from the functional.

---

## Test 5 — Background Consistency

**Required output**: Coherent states must appear as structured extrema against incoherent background, not merely as arbitrary local labels.

### Evaluation

The functional F = E + Γ·C_coherence treats coherent states as minima of a free energy.

Incoherent states (no phase locking) would have:
- No well-defined J_z or J_θ
- Undefined k
- Effectively infinite coherence cost (cannot maintain phase relationship)

So coherent states are indeed structured minima against a high-cost incoherent background.

### Test 5 Result: **PASS**

---

## Summary

| Test | Result | Notes |
|------|--------|-------|
| Test 1 (Selection) | INCONCLUSIVE | No derivation of k=1 without extra assumption |
| Test 2 (No smuggling) | FAIL | Practical candidates smuggle or assume |
| Test 3 (Relativistic) | PASS | Correct β-dependence |
| Test 4 (Two-sector) | PARTIAL | Compatible but not automatic |
| Test 5 (Background) | PASS | Coherent states are structured minima |

---

## Honest Conclusion

**The candidate functional does NOT pass acceptance tests.**

The core problem: selecting k = 1 requires an extra principle that is NOT contained in Axioms 1-3 as currently written.

**This is not failure. This is clarification.**

The frontier is now precisely located:

> Axiom 3 needs an explicit selection principle among coherent states.

---

## Proposed Resolution

Introduce **Axiom 3b** (or a corollary):

> **Among coherent states in the same topological class, the stable fundamental PF mode is the one with minimal topological winding.**

This principle:
- Selects k = 1 (primitive loop)
- Is physically motivated (simplicity/Occam's razor)
- Is NOT derived from current axioms (honest about gap)
- Closes the Casimir polynomial derivation

**This is the smallest honest deliverable.**

---

## What This Means for the Weinberg Angle

With Axiom 3b:
- k = 1 is selected
- γβ² = √C₂ follows
- Casimir polynomial derived
- sin²θ_W = 1/4 at unification scale

The Weinberg angle would move from **ARGUED (0.65)** to **DERIVED** — but with an explicit extra axiom.

---

## Next Action

Present this audit to the team. Decision required:

1. **Accept Axiom 3b** → Weinberg angle derived, gap closed
2. **Reject Axiom 3b** → Weinberg angle remains argued, continue search
3. **Reformulate Axiom 3b** → Find alternative selection principle

The team decides. The math is honest.
