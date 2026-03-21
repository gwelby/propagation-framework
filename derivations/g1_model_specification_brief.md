# G1: Exact Model Specification Brief
*For Codex — integrating G4 (AntiGravity) and G5 (Lumi)*
*2026-03-20*

---

## What G4 and G5 Tell G1

AntiGravity completed the literature survey on G4. Result:

**No external theorem bridges generations to walk steps.**
The bridge is definitional within the Propagation Framework.

AntiGravity's conclusion: *"Generations are physically defined as the three distinct 120° phase orientations required to complete a stable rotational closure cycle."* The walk length is N=3 because exactly 3 sequential phase steps close the SO(3) loop. Not "equal to" — the same object.

Lumi's G5 physical picture:
- Phase closure = topological knot completion, not spatial return to R=0
- The wave's internal phase must complete a 4π cycle (π₁(SO(3))≅ℤ₂ requires double winding)
- The medium is the constraint, not Euclidean space

---

## What G1 Must Now Specify

The model that Codex formalizes must have these properties:

**State space:**
Not R^D (Euclidean). The walk is on the internal phase manifold of SO(3) — likely S² (the 2-sphere, the coset SO(3)/U(1)) or the full group manifold SO(3) ≅ RP³.

**Step operator:**
A step is a 120° rotation in the internal phase space — one generational transition. The three steps are not random directions; they are the three fixed 120° intervals forced by the equiangular Koide construction.

**"Closure":**
Not return to Euclidean origin. Completion of a full 4π internal phase cycle (double winding, required by π₁(SO(3))≅ℤ₂). In the SO(3) manifold, this means the path lifts to a closed loop in the double cover SU(2) ≅ S³.

**Walk length:**
N = 3, not because we set it equal to generation count, but because the state space has exactly 3 distinct phase positions (the three 120° nodes of the Koide triangle). The walk has 3 steps because there are 3 nodes. The 3 nodes are the 3 generations.

**The return object:**
Not a probability density P(0,N) in R^D. The relevant object is the return amplitude for a walk on S² or SO(3) — a spectral quantity derived from the Laplacian on the group manifold.

---

## The Key Question for Codex

If the state space is SO(3) and each step is a 120° phase rotation:

1. What is the exact return amplitude after N=3 steps?
2. Does this amplitude, when inverted and normalized by 2π angular phase space, give α = 1/(2πN^(D/2))?
3. If D enters through the dimension of the SO(3) orbit (the coherent state manifold in D spatial dimensions), does the counting naturally produce N^(D/2)?

The Borel-Weil theorem failed on the CP^1 orbit (gave k+1, not N^(D/2)).
The question for G1 is: does the correct state space (SO(3) group manifold, not CP^1) give the right count?

---

## Why N^(D/2) Might Be Correct on SO(3)

Hint from AntiGravity's finding:
- Each generation = one 120° phase step
- In D=3 spatial dimensions, there are D independent planes of rotation
- To close in ALL D planes, you need N steps that collectively cover D-dimensional phase space
- If each step covers 2 dimensions (a rotation in a plane), D=3 dimensions require... N^(D/2) coverings?

This is not yet a proof. It is the geometric intuition that G1 needs to formalize.

The specific claim: in D spatial dimensions, the phase volume of a coherent state orbit for N equal-strength resonances scales as N^(D/2). This is what the boundary condition α = 1/(2πN^(D/2)) requires. If the SO(3) group manifold calculation gives this scaling exactly for D=3, N=3, the gap closes.

---

## For Codex: The Path Forward

Two options for the G1 model:

**Option A: Geometric (preferred)**
State space = S² (the coherent state manifold for SU(2) in 3D)
Steps = three 120° rotations (the three Koide nodes)
Closure = return to starting point on S² after traversing all three nodes
Return object = exact Green's function of the Laplacian on S²
Question: does the exact Green's function give N^(D/2) scaling at the Planck boundary?

**Option B: Algebraic**
State space = representation theory of SO(3) restricted to N=3 dimensional representations
Steps = matrix multiplication by the generators
Closure = trace condition (return to identity in representation space)
Return object = character of the N=3 representation evaluated at the identity
Question: does the character give the right normalization?

Option A is more physical. Option B is more tractable.

Both should be attempted. If neither gives α = 1/(2πN^(D/2)) exactly, the scaling argument fails and the God Equation stays ARGUED on solid grounds rather than optimistic ones.

---

*Brief written by Claude, integrating G4 (AntiGravity) and G5 (Lumi) for Codex G1 specification.*
*The house is in order. The proof attempt can now be focused.*
