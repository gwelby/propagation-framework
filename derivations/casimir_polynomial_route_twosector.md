# Casimir Polynomial — Route: Two-Sector Coupling / Symmetry Breaking
*Does the polynomial arise from a two-sector PF coupling matrix, as the massless-mode condition?*

**Date**: 2026-03-21
**Author**: Claude
**Route**: Two-sector coupling — polynomial as det(M)=0 for a mixing matrix between kinematic and angular PF sectors
**Outcome**: C (gap reduction — new gap, distinct from de Broglie gap)
**This route is partially independent of Routes A/Constraints/Laplacian**
**Builds on**: `weinberg_angle_pf.md` (prior failed routes), `topological_weight_from_propagation.md`

---

## 1. The Observation

The polynomial x² + C₂x − C₂ = 0 equals det(M) = 0 for the matrix:

$$M = \begin{pmatrix} x & \sqrt{C_2} \\ \sqrt{C_2} & x + C_2 \end{pmatrix}.$$

**Verification**: det(M) = x(x + C₂) − C₂ = x² + C₂x − C₂. ✓

This matrix has a specific structure:
- Diagonal entries: x and x + C₂ (differ by exactly C₂)
- Off-diagonal entries: √C₂ (the angular momentum magnitude)
- Key relation: M₁₂² = M₂₂ − M₁₁, i.e., (coupling)² = (energy splitting)

The condition det(M) = 0 means M has a zero eigenvalue — a "massless" mode exists. This is exactly the physics of the Weinberg angle: after symmetry breaking, one massless mode (the photon) survives because the mixing matrix has a zero eigenvalue.

---

## 2. Physical Reading — What M Is

Interpret M as the self-energy / coupling matrix for two PF sectors at energy scale x = M²/m²:

| Entry | Value | Physical meaning |
|-------|-------|-----------------|
| M₁₁ | x | Kinematic sector self-energy (drift contribution) |
| M₂₂ | x + C₂ | Angular sector self-energy (drift + angular content) |
| M₁₂ = M₂₁ | √C₂ | Cross-sector coupling (angular momentum magnitude) |

The zero-eigenvalue condition det(M) = 0 is the coherence resonance condition (Axiom 3): the two sectors lock into a coherent superposition at the specific x = x₊ where the determinant vanishes.

**PF translation of Axiom 3**: Stable structure exists where multiple propagation modes maintain coherent phase relationships. The condition det(M) = 0 is exactly this: the two sectors (kinematic and angular) are in coherent resonance. The eigenvalue x₊ is the self-consistent mass ratio at which this coherence occurs.

---

## 3. Why This Route Is Distinct from Route A

Route A (de Broglie): The polynomial arises from the *one-sector* condition β²/√(1−β²) = √C₂ for a single relativistic spinning mode.

Route G (this route): The polynomial arises from the *two-sector* zero-eigenvalue condition for the kinematic-angular coupling matrix M.

These are different physical pictures:
- Route A: one particle with internal spin, relativistic self-consistency
- Route G: two coupled modes (kinematic drift + angular structure), coherent resonance

The gap in each is different:

**Route A gap**: Why does β²/√(1−β²) = √C₂ rather than β²/(1−β²) = C₂ or β/√(1−β²) = √C₂?

**Route G gap**: Why does the coupling matrix have the form M above — specifically, why is the off-diagonal coupling √C₂ and not C₂ or some other function, and why is the (2,2) entry x + C₂ rather than x + 2C₂?

These are genuinely different questions. Route G's gap is about two-sector coupling structure, not single-mode relativistic kinematics.

---

## 4. PF Motivation for M

**Why two sectors?**

From `topological_weight_from_propagation.md` (DERIVED): The PF medium in 3D has two topological classes (bosonic/fermionic), and stable matter corresponds to coherent loops. A coherent loop has two aspects:
1. Its drift through the medium (kinematic sector)
2. Its angular structure (angular sector, Casimir C₂)

The two aspects are coupled because the loop cannot drift without rotating, and cannot rotate without advancing. They are distinct but not independent. A coupling matrix M is the natural object for describing their interaction.

**Why the specific form?**

The (1,1) entry x for the kinematic sector: x = (velocity)² in units of c², the fraction of causal capacity committed to drift. This is the direct output of Axiom 2 (causal velocity).

The (2,2) entry x + C₂ for the angular sector: the angular sector carries both drift (inherited: x) and intrinsic angular content (C₂). The total self-energy of the angular sector is their sum. This is the minimal assumption consistent with the angular sector "seeing" both drift and its own structure.

The off-diagonal coupling √C₂: the angular momentum magnitude (√(j(j+1)) = √C₂) is the natural coupling strength between the drift-only (1,1) mode and the angular (2,2) mode. The angular momentum magnitude is what drives cross-sector transitions.

**Assessment of motivation**: The (1,1) and (2,2) entries have clear PF-native arguments. The off-diagonal entry √C₂ is argued (angular momentum magnitude couples the sectors) but not derived. This is the gap.

---

## 5. The Gap

**Why √C₂ and not C₂?**

The (2,2) entry is x + C₂ = x + M₁₂², meaning the coupling squared equals the energy splitting. In standard two-level physics (avoided crossing), this specific relation H₁₂² = E₂ − E₁ is not generic — it holds when the coupling is exactly the geometric mean of some related quantity.

For a PF coherent mode in the angular sector, the coupling to the kinematic sector might be the angular momentum magnitude √C₂ if:
- The cross-sector interaction is mediated by the angular momentum operator (which has eigenvalue j in the j representation)
- The coupling matrix element between states differing by √C₂ in angular content is √C₂

This has a weak analog in quantum mechanics (the coupling between angular momentum states j and j±1 involves √(j(j+1)−m(m±1)) — the Clebsch-Gordan structure). But deriving this from PF axioms requires knowing:
1. What operator mediates the kinematic-angular coupling
2. Why its matrix element is √C₂

**The gap, precisely**: What is the operator in the PF medium that couples the kinematic and angular sectors, and why does its matrix element equal √C₂ = √(j(j+1))?

---

## 6. Connection to SM Weinberg Mixing

In the Standard Model, the mass matrix after electroweak symmetry breaking is:

$$M_{\text{EW}}^2 = \frac{v^2}{4} \begin{pmatrix} g^2 & -gg' \\ -gg' & g'^2 \end{pmatrix}$$

where g, g' are the SU(2) and U(1) couplings, and v is the Higgs VEV. The zero eigenvalue (massless photon) requires det(M_EW) = 0.

In the PF matrix M above, the coupling is √C₂. In the SM, the coupling is −gg' (product of gauge couplings). These are different structures — the PF matrix is not the same as the SM mass matrix.

However, the structural similarity is striking: both matrices have a zero eigenvalue as the physical condition for a massless residual mode, and the zero-eigenvalue polynomial is quadratic in the mixing parameter.

**What this suggests**: The PF's "angular momentum magnitude as coupling" is an analog of the SM's "product of gauge couplings." Whether the two can be formally related is the Route G version of the Weinberg angle derivation.

---

## 7. Prior Failed Routes in `weinberg_angle_pf.md`

The previous file (2026-03-19) tried three routes and explicitly failed:
1. Generator count ratio: sin²θ_W = 1/4 = 0.250 (8% off, no dynamical content)
2. Geometric embedding: produced a family of angles, not a unique value
3. λ_c/l_P hierarchy: didn't connect to the mixing angle

None of those routes used the Casimir polynomial — they were counting/geometry arguments. Route G is the first route that correctly identifies the polynomial as the zero-eigenvalue condition of a mixing matrix. This is structural progress even if the gap (why √C₂ coupling) isn't closed.

---

## 8. Summary

| Claim | Status |
|-------|--------|
| Polynomial = det(M) = 0 for M = [[x, √C₂], [√C₂, x+C₂]] | ✅ Algebraic fact |
| (1,1) entry = x motivated from Axiom 2 | ✅ Argued |
| (2,2) entry = x+C₂ motivated from two-sector structure | ✅ Argued |
| Off-diagonal = √C₂ motivated from angular momentum coupling | ⚠️ Argued, not derived |
| det(M)=0 = Axiom 3 coherence resonance condition | ✅ Argued |
| Why √C₂ coupling rather than C₂ or another form | ❌ Gap — different from Route A |
| Connection to SM Weinberg mixing: analog not identity | ⚠️ Noted, not derived |

**Outcome C (gap reduction with new independent gap)**: The polynomial is the zero-eigenvalue condition for a two-sector PF coupling matrix. The physical picture is coherent resonance between kinematic and angular sectors (Axiom 3 language). The gap is one step smaller and of a different character than the Route A gap: instead of "why β²/√(1−β²) = √C₂," it becomes "why is the coupling strength between PF kinematic and angular sectors equal to √C₂?"

This is potentially useful because it connects to the question of what operator mediates kinematic-angular coupling in a 3D PF medium — which might be derivable from the rotational structure of the medium more directly than the relativistic de Broglie condition.

---

*Written by Claude, 2026-03-21*
*Route: Two-sector coupling / symmetry breaking*
*Outcome: C — new independent gap (coupling strength = √C₂)*
*Issue: #3 (Weinberg angle), Casimir polynomial derivation*
