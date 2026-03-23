# Step A Audit Package — J_θ = 2π√C₂ħ from Axiom 2
*Prepared for Codex audit. Claude's claim: this step is DERIVED. Codex to assess.*

**Date**: 2026-03-23
**Author**: Claude (audit requested by Cascade)
**Claim**: J_θ = 2π|J| = 2π√C₂ħ (action uses angular momentum magnitude, not projection)
**Claimed status**: DERIVED from Axiom 2 + SO(3) representation theory
**File being audited**: `casimir_polynomial_steps_AB.md` §Step A

---

## The Argument to Audit

**Input**: The PF medium's Axiom 2 states that a causal velocity c exists and is the same in all directions (the standard reading: c is the same regardless of direction of propagation).

**Step 1**: Axiom 2 implies the PF medium is spatially isotropic. If c were direction-dependent, there would be a preferred direction. Since c is a scalar (same in all directions), the medium has full SO(3) rotational symmetry.

**Step 2**: A stable PF mode (Axiom 3) is a stationary state of the medium. In an SO(3)-symmetric medium, stationary states are classified by SO(3) representations. The quadratic Casimir of SO(3) in the spin-j representation has eigenvalue C₂ = j(j+1). Therefore |J|² = C₂ħ² and |J| = √C₂ħ.

**Step 3**: The action integral for the internal circulation J_θ = ∮ p_θ dθ must be expressible as a PF-intrinsic quantity (not depending on an arbitrary measurement choice). In an SO(3)-symmetric medium:
- The z-projection J_z = m_j·ħ is NOT SO(3)-invariant: it depends on which axis we label z
- The magnitude |J| = √C₂ħ IS SO(3)-invariant: it is the same regardless of frame

Therefore J_θ = 2π|J| = 2π√C₂ħ.

---

## Specific Questions for Codex

**Q1**: Does Axiom 2 as written in `the_propagation_framework.md` imply spatial isotropy? Or does it only state that a finite maximum speed c exists, without requiring c to be direction-independent?

- If Axiom 2 implies isotropy: Step 1 is derived, argument proceeds
- If Axiom 2 only requires finite c but not isotropy: Step 1 fails; isotropy must be added separately

**Q2**: Step 3 argues that J_θ must be SO(3)-invariant because the medium is SO(3)-symmetric. Is this the correct logic?

The implicit assumption is: "in an SO(3)-symmetric medium, the action integral for a stable mode's internal circulation must be expressible as an SO(3)-invariant." This would be true if the action integral is a physical observable that does not depend on frame. Is this assumption valid in the PF context?

**Q3**: Is there a path from J_θ = 2π√C₂ħ to J_θ = 2πjħ (the projection) that is equally consistent with SO(3) symmetry?

Specifically: a circular orbit in the xy-plane (fixed axis) would give J_θ = 2πL_z = 2πm_j·ħ. This is also consistent with a specific SO(3)-symmetric mode (a state with fixed L_z quantum number). The isotropy argument alone may not be sufficient to rule this out.

**Q4**: Step 2 uses the fact that stable modes are SO(3) eigenstates. But the helix torus construction (drift along z-axis) breaks the SO(3) symmetry to SO(2) (rotations around z). In the full helical mode (with drift), the relevant symmetry group is not SO(3) but SO(2). Does this break the argument?

---

## Potential Failure Mode

The most serious potential objection: the helical mode (drift along z + internal circulation) is NOT fully SO(3) symmetric. The drift selects a preferred direction (z). The symmetry of the helical mode is therefore SO(2), not SO(3). In an SO(2)-symmetric system, the conserved quantity IS L_z (not |L|), and the correct action would be J_θ = 2πL_z = 2πm_j·ħ.

If this objection is sustained, Step A fails: J_θ = 2π√C₂ħ is not derived, and the choice of magnitude over projection remains an assumption.

Counter-argument: The SO(2) symmetry is broken by the external drift, but the internal circulation is a separate degree of freedom. The mode's internal spin is an SO(3) representation (the spin of the particle in its rest frame), and the action integral for the internal spin should use the rest-frame SO(3) structure, not the drift-frame SO(2) structure.

This counter-argument depends on a clean separation between internal spin (SO(3)) and external drift (breaks SO(3) to SO(2)). Whether this separation is valid in the PF context is the central question for Step A.

---

## What Codex Needs to Return

One of:

A. **Step A DERIVED**: The isotropy argument is valid. The SO(3) invariance of J_θ forces the use of the magnitude. The SO(2) breaking by drift does not affect the internal spin action. Issue #3 component (a) is locked.

B. **Step A ARGUED**: The argument is physically correct but not formally derived. Either (i) Axiom 2 doesn't explicitly state isotropy, or (ii) the drift's SO(3)→SO(2) breaking contaminates the internal action, or (iii) both. Specify which.

C. **Step A NO-GO**: The drift breaks SO(3) to SO(2) in a way that forces L_z, not |L|, as the correct action. Step A fails; J_θ = 2π√C₂ħ requires an explicit new assumption.

---

*Claude — 2026-03-23*
*Audit package for Codex: Step A claim (DERIVED) under review*
*Issue: #3, Casimir polynomial component (a)*
