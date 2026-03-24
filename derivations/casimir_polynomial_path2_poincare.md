# Casimir Polynomial — Path 2: Poincaré Group Formalization of Axiom 3
*Can the medium-frame coherence condition select the spin-orbit locking state from ISO(3,1) representations?*

**Date**: 2026-03-22
**Author**: Claude
**Status**: Attempt — not a route file; formal follow-on to `casimir_polynomial_claude_independent_pass.md`
**Goal**: Formalize Axiom 3 in group-theoretic language; check whether "coherent in the medium frame" forces γβ² = √C₂
**Verdict**: Gap not closed. Path 2 repositions the gap and reveals convergence with Routes F and H. A minimality principle is identified as the remaining decisive step.

---

## 1. Setup: Poincaré Group Structure for PF Modes

### The Symmetry Groups in Play

The PF involves two symmetry groups that must be distinguished:

**Group 1 — The medium's symmetry group G_medium:**
The PF medium (Axiom 1) is isotropic and homogeneous in space, but has a preferred rest frame (Axiom 2: there is a causal velocity c, and the medium is the thing through which propagation occurs). The medium's symmetry group is therefore:

$$G_{\rm medium} = SE(3) \times \mathbb{R} = (\mathbb{R}^3 \rtimes SO(3)) \times \mathbb{R}$$

(Euclidean group in 3D, plus time translations). Crucially: **Lorentz boosts are NOT symmetries of the medium** — they change the observer's relationship to the medium's preferred frame. The medium breaks Lorentz invariance by providing a preferred frame.

**Group 2 — The mode's internal symmetry group G_mode:**
A stable PF mode propagates internally at c (Axioms 1+2). Its internal structure is governed by the full Poincaré group ISO(3,1), because the internal propagation at c is relativistic. The mode's quantum numbers (mass m, spin j) are Poincaré invariants.

The tension between G_medium (breaks Lorentz) and G_mode (full Poincaré) is where the constraint must come from.

### Wigner Classification in the Medium Context

For a massive mode (mass m, spin j), Wigner's classification gives:
- Rest-frame states: |j, σ⟩ with little group SO(3), σ = −j, …, j
- Moving states at momentum **p**: |**p**, σ⟩ = U(L(**p**)) |k, σ⟩ where L(**p**) is the standard boost

In the **medium frame** specifically, the mode has momentum **p** = (γmc, **p**) with |**p**| = γmβc. The mode is a Wigner representation evaluated at a specific boost parameter (γ, β) — the parameters of the mode's drift through the medium.

The question is: does the medium's preferred frame impose a constraint on (γ, β) beyond simply labeling which state we're describing?

---

## 2. The Wigner Rotation Approach

### Thomas Precession for a Helical Mode

When a spin-j mode drifts at βc through the medium while circulating internally, there is a Wigner rotation associated with each internal revolution. Compute this explicitly.

**Setup**: Mode drifts along z at βc. Internal circulation is in the x-y plane at speed c, radius r_C. After one internal revolution (time T = 2πr_C/c), the center has moved to z = d = 2πβr_C.

The trajectory of the mode's center-of-mass is helical. The Wigner rotation W associated with the sequence:
1. Boost from rest to drift velocity βc (boost B_z(η), rapidity η = arctanh β)
2. Internal revolution in the x-y plane (rotation R_z(2π) = identity!)
3. Inverse boost back to rest frame

For step 2: A rotation by 2π around the z-axis (the drift direction) is the identity on the center of mass. The Wigner rotation in this case is:

$$W = L^{-1}(\text{final}) \cdot R_z(2\pi) \cdot L(\text{initial}) = L^{-1} \cdot \mathbf{1} \cdot L = \mathbf{1}$$

**Finding**: For a helical mode where the internal rotation axis is the same as the drift axis (z), the Wigner rotation after one full revolution is the identity. This means Thomas precession contributes nothing in this geometry.

### What Wigner Rotation Gives

The Wigner rotation is trivial for coaxial helical motion. This tells us:

- The mode's spin axis does not precess due to Thomas precession
- The Wigner rotation cannot be the mechanism that selects γβ² = √C₂
- Path 3 (Wigner rotation → zero angle) cannot work in this coaxial geometry

**Conclusion from Wigner rotation approach**: The coaxial helical geometry makes the Wigner rotation trivial. Path 3 is a no-go for coaxial helices. The constraint must come from somewhere else.

---

## 3. The Frame-Adapted Representation Approach

### What "Coherent in the Medium Frame" Could Mean

In the medium frame, the mode is described by a specific Wigner state:
$$|\text{mode}\rangle = \sum_\sigma c_\sigma |\mathbf{p}, \sigma\rangle$$

For this to be a "coherent" state in the PF sense (Axiom 3), it must maintain stable phase relationships. There are several possible formalizations:

**Version A — Helicity eigenstate:**
The mode is in a definite helicity state (spin projection along drift direction = ±j). In the drift frame, the mode is a helicity eigenstate with helicity ±j.

For a helicity eigenstate, L_z = j·ħ (taking helicity +j for definiteness). The angular action is:
$$J_\theta = 2\pi L_z = 2\pi j \hbar$$

The coherence condition J_z = J_θ then gives:
$$\gamma\beta^2\hbar = j\hbar \implies \gamma\beta^2 = j$$

This gives the Casimir polynomial as x²/(1−x) = j² (NOT j(j+1)). This is **not** the correct polynomial.

**Version B — Maximum weight state (|m| = j):**
Same as Version A. Gives j, not √(j(j+1)).

**Version C — Angular momentum magnitude state:**
The mode's "effective" angular momentum is the magnitude |**L**| = √(j(j+1))·ħ. This is the eigenvalue of L² not L_z. Using J_θ = 2π|**L**| = 2π√C₂ħ (as Route H does) and J_z = J_θ gives:
$$\gamma\beta^2 = \sqrt{C_2} = \sqrt{j(j+1)}$$

This is the correct polynomial. But using the angular momentum **magnitude** (not projection) in the action integral is non-standard Bohr-Sommerfeld.

**Why the magnitude and not the projection?**

The key question is: which action integral is the right one for a PF mode?

For a mode that circulates in 3D (not just 2D), the angular momentum vector precesses around the drift axis. The trajectory in angular momentum space is a circle of radius |**L**_perp| = √(L² - L_z²) centered on the z-axis. The full action integral over one precession is:

$$J_\theta^{\rm 3D} = \oint_{\rm precession} p_\theta d\theta = |\mathbf{L}| \cdot 2\pi = 2\pi\sqrt{C_2}\hbar$$

This is the angular momentum magnitude, traced around the full precession circle. It equals 2π|**L**| regardless of L_z.

**Physical interpretation**: The PF mode's angular momentum is not fixed in direction — it precesses around the drift axis. The action integral uses the magnitude because the circulation explores all directions equally (isotropic 3D internal structure). This is the correct action for an isotropically-precessing spin, not just an azimuthally-rotating one.

This is a real distinction between a 2D orbit (uses L_z = projection) and a 3D isotropic mode (uses |L| = magnitude). The PF medium has causal velocity c in all directions (Axiom 2 → isotropy), which means stable modes have no preferred orientation. A mode with no preferred spin direction is isotropically precessing in 3D, and its action integral uses the magnitude |**L**| = √C₂ħ. Therefore J_θ = 2π√C₂ħ is correct for isotropic PF modes, derived from medium isotropy (Axiom 2), not from N=3 generations.

[Note: D=3 spatial dimensions is currently assumed, not derived, in the PF framework — see `closing_the_gaps.md`. The isotropy argument above uses only the isotropic character of the medium, not the specific value D=3.]

**Assessment of Version C**: This explains WHY √C₂ (not j) appears in the action. It does NOT yet explain why J_z = J_θ.

---

## 4. The Self-Referential Coherence Condition

### Axiom 3 at Maximum Coherence

The PF document (Axiom 3) defines coherence on a spectrum, with the highest level being:

> "Self-referential coherence: systems whose coherent patterns include models of their own coherence."

For a fundamental mode, self-referential coherence has a precise interpretation:

**A mode is self-referentially coherent if its internal state (characterized by J_θ) contains complete information about its external state (characterized by J_z).**

If J_z ≠ J_θ: the mode's internal action does not fully specify its external action. The external dynamics carries more (or less) information than the internal dynamics. This is an internal-external asymmetry.

If J_z = J_θ: the mode's internal action exactly matches its external action. Internal and external are in perfect correspondence. The mode "knows about itself" completely — knowing J_θ tells you J_z, and vice versa.

This is the group-theoretic reading of drift-rotation locking: the mode achieves self-referential coherence precisely when J_z = J_θ.

### Can This Be Derived from Axiom 3?

The question becomes: does Axiom 3 ("coherence is the necessary condition for structure") force self-referential coherence as the condition for a FUNDAMENTAL stable mode?

**Argument**:
- Axiom 3 says stable structure requires coherence.
- A mode with J_z ≠ J_θ has an internal-external mismatch: each revolution, the internal phase accumulates by 2π√C₂ but the external phase accumulates by 2πγβ². These two phase rates differ.
- The mismatch means the mode's phase structure is incoherent between its internal and external degrees of freedom.
- A mode with internal-external phase mismatch cannot be in full self-referential coherence (Axiom 3, highest level).
- Therefore: the fundamental stable modes of the PF are those with J_z = J_θ.

**The Gap in This Argument**:

The argument says "full self-referential coherence requires J_z = J_θ," but it doesn't show that fundamental modes MUST achieve full self-referential coherence rather than some weaker level of coherence.

Axiom 3 says coherence is necessary for structure, but it does not say fundamental modes must achieve the maximum possible coherence. A mode with J_z ≠ J_θ still has partial coherence — both internal and external loops are individually coherent (J_θ is quantized by the internal circulation, J_z is quantized by the helix torus). The mismatch is between the two separately-coherent systems.

**What's Missing**: A principle that states fundamental modes must achieve not just individual coherence (each loop coherent separately) but joint coherence (both loops coherent with each other). Call this the **Cross-Loop Coherence Principle**.

---

## 5. The Cross-Loop Coherence Principle

### Statement

> **Cross-Loop Coherence (CLC)**: For a fundamental PF mode on a torus T² with two independent coherence loops (A: internal, B: external), the mode is stable only if the phase accumulation around Loop A equals the phase accumulation around Loop B:
> $$J_A = J_B$$
> i.e., the torus's two independent cycles carry equal action.

### Why This Follows from Axiom 3

Axiom 3 for a multi-loop system: "coherent phase relationships around closed loops." For a system with TWO loops, there are three types of phase coherence to enforce:

1. **Loop A coherence**: phase returns to itself around Loop A → J_A = integer × h ✓ (quantization)
2. **Loop B coherence**: phase returns to itself around Loop B → J_B = integer × h ✓ (quantization)
3. **Cross-loop coherence**: the phase structure is consistent between the two loops → J_A = J_B

Conditions 1 and 2 are individually satisfied by EBK quantization. Condition 3 is the additional constraint.

**Physical meaning of condition 3**: If J_A ≠ J_B, then a path that goes around Loop A once and Loop B once in opposite senses picks up a net phase of J_A − J_B per cycle. This is a non-trivial holonomy on the torus. A mode with non-trivial cross-loop holonomy is not fully coherent on the torus — different paths on the torus give different phases.

**Fully coherent mode on T²**: A mode is coherent on the full torus if and only if the action is the same around all closed loops. For T², all loops are linear combinations of Loop A and Loop B: a loop going m times around A and n times around B accumulates phase m·J_A + n·J_B. For this to be consistent (equal to an integer multiple of h for all m, n), we need J_A = J_B.

This is the condition that the torus action is "flat" — no non-trivial holonomy. A flat torus action means J_A = J_B.

### The Derivation

Under the Cross-Loop Coherence Principle (which follows from Axiom 3 applied to a two-loop system):

$$J_\theta = J_z$$
$$2\pi\sqrt{C_2}\hbar = 2\pi\gamma\beta^2\hbar$$
$$\gamma\beta^2 = \sqrt{C_2}$$

Setting u = β²:
$$\frac{u}{\sqrt{1-u}} = \sqrt{C_2} \implies \frac{u^2}{1-u} = C_2 \implies u^2 + C_2 u - C_2 = 0$$

**This is the Casimir polynomial.** ✓

---

## 6. Checking the Argument's Chain

Let me state the full chain and identify which steps are derived vs. argued:

| Step | Source | Status |
|------|--------|--------|
| PF mode has internal circulation at c | Axioms 1+2 (internal propagation speed = c) | ARGUED (well-established in Route A chain) |
| Internal action J_θ = 2π√C₂ħ uses angular momentum magnitude | PF medium is 3D (N=3), mode precesses isotropically | ARGUED — needs N=3 derivation as input |
| Drift action J_z = 2πγβ²ħ is canonical (helix torus) | Torus construction from `claude_independent_pass.md` | ESTABLISHED (substantially resolved Objection 1) |
| Cross-Loop Coherence: J_A = J_B on T² | Axiom 3 applied to two-loop system → flat torus action | **KEY STEP — see below** |
| J_z = J_θ → γβ² = √C₂ → Casimir polynomial | Algebra | DERIVED |

### Is Cross-Loop Coherence Derived from Axiom 3?

The argument is:

Axiom 3: coherent phase relationships around closed loops.

For a torus T², there are infinitely many closed loops: general (m, n) loops. The phase around the (m, n) loop is m·J_θ + n·J_z.

For EVERY closed loop to have coherent phase (integer × h), we need both J_θ/h and J_z/h to be rational, AND their ratio to be rational. But the weakest full-torus coherence condition is:

**The action 1-form p dq restricted to the torus must be exact** — its integral around every loop is zero mod h.

This is the condition that the torus is a Lagrangian torus with equal actions in both directions: J_θ = J_z.

Wait — that's not right. The condition "integral is integer × h around every loop" for T² with J_θ and J_z both quantized (J_θ = n_θ · h, J_z = n_z · h) requires n_θ and n_z to be integers. The general (m, n) loop gives m·n_θ + n·n_z which is automatically an integer if n_θ, n_z are integers. So just having J_θ and J_z both quantized is sufficient for all loops.

The condition J_θ = J_z is NOT automatically required by Axiom 3 alone. You can have J_θ = h and J_z = 2h (a 1:2 resonance) and all loops are still coherent. The (1, 1) loop gives 3h (coherent), the (1, -1) loop gives -h (coherent), etc.

**The Cross-Loop Coherence Principle as stated above is WRONG.** It conflates "all loops coherent" with "J_A = J_B," but these are not the same. Individual quantization of J_A and J_B already ensures all loops are coherent. The additional condition J_A = J_B is NOT required by Axiom 3 applied to the torus.

---

## 7. The Gap, Re-Located

The argument of Section 5 breaks down. Cross-Loop Coherence does not follow from Axiom 3 for the reasons given. Let me re-examine what IS true:

**What follows from Axiom 3 (torus version)**:
- J_θ = n_θ · h for some positive integer n_θ
- J_z = n_z · h for some positive integer n_z
- ALL closed loops on T² are coherent automatically once these are satisfied

**What requires an additional principle**:
- The selection of n_z = n_θ (the 1:1 resonance condition)
- Excluding n_z = 2n_θ, n_z = 3n_θ, etc.

**Why is k=1 (n_z = n_θ) special?**

On a resonant torus where J_θ/J_z = p/q (rational), there is always a single loop (the (q, -p) loop) that is trivial — the phase is zero. This is the resonance direction. For k=1 (p=q=1), the resonance direction is the (1, -1) loop, which is the difference of the two fundamental cycles.

The 1:1 resonance is special because:
- It is the **unique resonance where the torus quotient under the resonance direction collapses to a circle** (not a torus with rational winding)
- The resonant loop on a 1:1 torus is topologically the most natural one: it is the diagonal of the fundamental domain
- In the language of flat connections on T²: a 1:1 resonant torus is the unique torus where the two actions are equal

But NONE of this automatically follows from Axiom 3 without an additional minimality or uniqueness principle.

**The precise gap**:

> **Gap, re-located by Path 2**: On the helix torus T², Axiom 3 requires J_θ and J_z to each be individually quantized (integer multiples of h). This does not force J_z = J_θ. An additional principle — call it the **Minimal Resonance Principle** — is needed: among all resonant states n_z/n_θ = p/q (with p, q positive integers), the PF selects the lowest-order resonance p = q = 1.

---

## 8. Three Formulations of the Minimal Resonance Principle

These are all equivalent ways of stating the missing step:

| Language | Statement |
|----------|-----------|
| Action | n_z = n_θ = 1 is the minimum-action 1:1 resonant state on the helix torus |
| Topology | The helix torus with k:1 resonance for k > 1 is k-fold covered; the fundamental mode has no covering (k=1) |
| Group theory | The 1:1 resonant loop is the generator of the first homology H₁(T²) with the shortest period |
| Quantum | The helix torus ground state has n_θ = n_z = 1; excited states have higher k |

The **Topological Formulation** is most promising for a PF derivation:

A k:1 resonant helical mode visits each point in z-space k times per j-cycle. The mode is a k-fold "winding" of the basic helical pattern. For k > 1, the mode is not a fundamental loop on the torus but a k-fold cover.

**Axiom 3 (coherence as the condition for stable FUNDAMENTAL modes) selects the k=1 unwound loop** — the mode that traces each helix cycle exactly once. Higher-k modes (k > 1) are k-th "harmonics" of the fundamental and are excluded as non-fundamental.

This is the PF-native statement: the fundamental mode is the k=1 helix, not a k-fold harmonic. Excited states in this direction would be k-fold harmonics, but these are compound modes, not fundamental ones.

### Is This Derivable or Another Assumption?

This is a genuine PF principle: the distinction between fundamental modes (k=1) and composite modes (k > 1) is a consequence of the mode being a "self-reinforcing propagation pattern" (Axiom 1's description of matter). A k > 1 mode would reinforce k copies of the fundamental pattern per revolution — it is a compound mode, not a fundamental one.

**The Minimal Resonance Principle follows from Axiom 1** (propagation is fundamental; matter = fundamental self-reinforcing modes) combined with the helix torus structure: **the fundamental mode is the mode that traces the helix once per period, not k times**.

---

## 9. The Reconstructed Derivation Chain

With the Minimal Resonance Principle now grounded in Axiom 1:

**Step 1**: PF mode has internal circulation at c and external drift at βc (Axioms 1+2).

**Step 2**: The helical trajectory defines a torus T² via the screw quotient σ. The two canonical actions are J_θ and J_z (Codex Objection 1, resolved by helix torus construction).

**Step 3**: J_θ = 2π√C₂ħ because the PF medium is isotropic (Axiom 2: causal velocity c in all directions) and a stable mode in an isotropic medium has no preferred spin orientation. An isotropically-precessing spin uses the angular momentum magnitude |**L**| = √C₂ħ in the action integral, not the z-projection L_z = jħ.

**Step 4**: Axiom 3 requires J_θ = n_θ · h and J_z = n_z · h (individual quantization of both loops).

**Step 5**: Axiom 1 (fundamental modes, not composites) requires n_z/n_θ = 1 — the mode traces the helix exactly once per internal revolution (not k > 1 times).

**Step 6**: Therefore J_z = J_θ → 2πγβ²ħ = 2π√C₂ħ → γβ² = √C₂ → **Casimir polynomial**. ✓

---

## 10. Honest Assessment of the Chain

### What is clean

- Steps 1, 2 (helix torus): established or substantially resolved
- Step 6 (algebra): derived
- Step 5 (n_z/n_θ = 1 from Axiom 1): a genuine consequence of "fundamental mode," not obviously circular

### What remains argued

**Step 3** (J_θ uses magnitude not projection): This requires the N=3 derivation as input. If the medium is 3D and the internal angular momentum precesses isotropically around the drift axis, the action integral around the internal cycle uses |**L**| not L_z. This is well-motivated but requires the N=3 result explicitly.

**Step 4-5 interface**: The argument that Axiom 3 requires individual quantization (standard Bohr-Sommerfeld) combined with Axiom 1 requiring the fundamental (n=1) mode is clean, but it assumes that J_θ and J_z must be separately quantized to integer multiples of h (not just that their ratio is 1). This is the standard EBK condition, which applies when the torus is a Lagrangian torus with two independent canonical cycles.

### The Residual Gap

After Path 2, the gap is:

> **Gap (after Path 2)**: The derivation of the Casimir polynomial requires three components:
> (a) J_θ = 2π√C₂ħ — angular momentum magnitude in 3D PF (needs N=3 result explicitly)
> (b) J_z = 2πγβ²ħ — canonical drift action on helix torus (substantially resolved)
> (c) n_z = n_θ — fundamental mode condition from Axiom 1 (argued, not formally derived)
>
> If (a) and (c) are both accepted as argued, the polynomial follows. The remaining formal gap is the derivation of (a) from N=3 structure — which may already be available from the existing N=3 derivation.

---

## 11. Connection to N=3 Derivation

The claim that J_θ = 2π√C₂ħ (magnitude, not projection) rests on the mode being isotropically circulating in a 3D medium. The N=3 derivation (which established that the PF medium has exactly 3 spatial dimensions from Axiom 3's coherence structure) might already imply isotropic 3D internal circulation.

**Specific check needed**: Does the N=3 derivation establish that PF modes have isotropic internal angular momentum distributions (rather than fixed-axis rotation)? If yes, Step 3 is derived from N=3.

If the N=3 result gives isotropy, then the chain is:

$$\underbrace{N=3}_{\text{from Axiom 3}} \implies \underbrace{J_\theta = 2\pi\sqrt{C_2}\hbar}_{\text{magnitude, not projection}} \xrightarrow{+ \text{helix torus}} \underbrace{J_z = 2\pi\gamma\beta^2\hbar}_{\text{canonical}} \xrightarrow{+ \text{Axiom 1: fundamental}} \underbrace{J_z = J_\theta}_{\text{spin-orbit locking}} \implies \text{Casimir polynomial}$$

This would be a complete chain from PF axioms to polynomial.

---

## 12. Synthesis: What Path 2 Contributes

Path 2 did not close the gap, but it did:

1. **Ruled out Path 3 (Wigner rotation)**: Coaxial helical motion has trivial Wigner rotation. This is a genuine no-go for one candidate path.

2. **Identified why √C₂ not j**: The 3D internal structure of PF modes (precessing angular momentum) explains why the action uses the magnitude |**L**| = √C₂ħ rather than the projection L_z = jħ. This resolves a sub-question about Route H.

3. **Identified the Minimal Resonance Principle**: The k=1 selection follows from Axiom 1 (fundamental modes are not k-fold composites). This is a new argument not present in Routes F or H.

4. **Reduced the gap to N=3 + isotropy**: If the N=3 derivation gives isotropic angular momentum distributions, and if Axiom 1's "fundamental" constraint gives n=1, the Casimir polynomial follows.

5. **Located convergence**: Routes F, H, and Path 2 all point to the same core principle — the mode's internal and external phases must be in 1:1 correspondence. Path 2 identifies this as the combination of isotropic 3D internal structure (N=3) and fundamental mode selection (Axiom 1).

---

## 13. Recommended Next Steps

**Step A (bounded, near-term)**: Verify that Axiom 2 (isotropic causal velocity c in all directions) implies that stable PF modes have isotropic angular momentum distributions (no preferred spin direction). If so, Step 3 above (J_θ = 2π√C₂ħ from magnitude not projection) is derived from Axiom 2 alone. This is a short argument, not requiring the N=3 or God Equation derivations.

**Step B (bounded, near-term)**: Formalize the "fundamental mode" condition from Axiom 1 → n_z/n_θ = 1. This requires stating precisely what "fundamental" means for a mode with two independent action variables.

**Step C (if A and B complete)**: Write the full derivation chain as a proper derivation file, have Codex audit.

**Do NOT update CLAIMS.md** until Step C is complete and audited.

---

## 14. New Gap Status

| Gap | Pre-Path 2 | Post-Path 2 |
|-----|------------|-------------|
| Why J_θ = 2π√C₂ħ (not 2πjħ)? | Unstated | **Identified**: 3D isotropic internal structure (N=3 medium) |
| Why J_z is canonical? | Objection 1 (Codex) | Substantially resolved: helix torus |
| Why J_z = J_θ? | Assumed (Objection 2) | **Repositioned**: Minimal Resonance (Axiom 1, n=1) + isotropy (N=3) |
| Path 3 (Wigner rotation) viable? | Unknown | **No-go**: coaxial Wigner rotation is trivial |

The gap is smaller than before. The residual requires checking two things that may already be derivable from existing results.

---

*Claude — 2026-03-22*
*Path 2: Poincaré group attempt — gap not closed but substantially repositioned*
*Key outputs: Wigner rotation no-go (coaxial); √C₂ from 3D isotropy (N=3 input); k=1 from Axiom 1 (fundamental mode)*
*Remaining: verify N=3 → isotropy; formalize Axiom 1 → n=1*
*Issue: #3 (Weinberg angle), Casimir polynomial derivation*
