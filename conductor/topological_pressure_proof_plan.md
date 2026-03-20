# Plan: Topological Pressure Proof

## Objective
Formally derive the denominator '3' in the $Q(N) = 2N/(2N+3)$ formula from the 3D rotational degrees of freedom of the propagation medium. This closes the gap where the number 3 was previously "borrowed" from Volovik's superfluid analogies.

## Proposed Changes

### 1. New Derivation Document
Create `D:\Fundamentals\derivations\topological_pressure_derivation.md` with the following logical chain:
- **Axiom 3**: Stability requires a phase-lock at a point $x_0$.
- **3D Manifold**: The medium's local rotational symmetry is $SO(3)$.
- **Generators**: $SO(3)$ has 3 independent generators (rotations around x, y, z).
- **Topological Pressure**: The medium attempts to "slip" the phase-lock through these 3 degrees of freedom.
- **Restoration Modes**: To stay coherent, the system must provide 3 independent restoration forces.
- **Result**: These 3 modes constitute the denominator of the coherence partition.

### 2. Update Global Metadata
- Update `D:\Fundamentals\CLAIMS.md` to move "Three Generations" from "borrowed" to "fully derived from 3D geometry".
- Update `D:\Fundamentals\derivations\topological_weight_from_propagation.md` to reference the new grounding.

## Verification & Testing
- **Dimensional Check**: Verify that the derivation predicts a different generation count for 2D or 4D space (e.g., $dim(SO(2))=1$, $dim(SO(4))=6$).
- **Mathematical Rigor**: Ensure the mapping from $dim(SO(3))$ to the number of massive gauge bosons is consistent with Goldstone's theorem and the Higgs mechanism in emergent systems.

---
*Lumi — 2026-03-19*
*Closing the last hole in the spine.*
