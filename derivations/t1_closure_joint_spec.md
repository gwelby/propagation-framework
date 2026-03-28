# T1 Closure Joint Specification
*Decomposing the (2,1) Topological Weights gap into attackable Lemmas*

**Date**: 2026-03-28
**Authors**: Joint Agent Synthesis (Codex, Claude, Qwen, Lumi)
**Target**: Close the T1 physical-realization gap identified in `HA-20260328-010`.

---

## 1. The Core Missing Theorem
**Current Status:** PF has proven that 3D rotation topology $\pi_1(SO(3)) \cong \mathbb{Z}_2$ yields exactly two closure orders: 1 and 2. 
**The Gap:** PF has *not* proven that a coherence-seeking medium (Axiom 3) *must* physically realize the weight-2 spinorial branch as a stable mode.

**Theorem to Prove:** 
Given Axiom 3 (coherence necessary for stable structure) and a 3D rotational configuration space, stable self-referential propagation modes must admit realization on the nontrivial $SU(2)$ lift, and a purely weight-1 (tensor/scalar) medium is dynamically incomplete or unstable.

## 2. Decomposition into Proof Obligations (Lemmas)

To prevent "lump" theorem attempts that smuggle in the Standard Model, the proof is decomposed into three strictly bounded Lemmas.

### Lemma A: Completeness under Rotation (The Mathematical Necessity)
*Assigned to: Claude*
* **Hypothesis:** A medium restricted entirely to weight-1 (contractible) modes fails the Axiom 3 phase-closure condition for at least one physically mandated rotational configuration.
* **Proof Obligation:** Define the PF stable mode as a *section* over the 3D rotational configuration space, not just a loop. Prove that a purely tensor/scalar section acquires an unresolvable phase defect under a $2\pi$ rotation boundary condition that only a lifted spinorial representation can absorb.

### Lemma B: Weight-2 is the Unique Nontrivial Completion (The Topological Lock)
*Assigned to: Codex*
* **Hypothesis:** Given 3D space and $\pi_1(SO(3)) \cong \mathbb{Z}_2$, the $SU(2)$ lift (which has minimal closure order 2) is the *only* mathematically valid way to extend the state space to cover non-contractible loops while preserving local coherence.
* **Proof Obligation:** Formalize the covering space theorem in PF language to show no intermediate or higher-order fraction closure options exist. (Likely already closed by standard topology, needs strict translation).

### Lemma C: Dynamical Stability Selects Both Branches (The Physical Necessity)
*Assigned to: Qwen / Sandbox*
* **Hypothesis:** The weight-2 branch is not merely topologically available; it is energetically or dynamically necessary for a stable self-referential mode to exist in 3D space.
* **Proof Obligation:** Search the literature (geometric quantization, projective representations in superfluids/media, topological phases of matter) for existing proofs that coherent media force spinorial structure. Alternatively, build a sandbox simulation showing a pure weight-1 medium suffers catastrophic instability under coherence pressure, forcing the spawning of a weight-2 defect to regain stability.

## 3. Execution Plan
1. **Qwen:** Execute research pass on Lemma C (Projective/spinorial necessity in coherent media).
2. **Claude:** Draft formal theorem attempt for Lemma A (PF-to-SU(2) lift via sections).
3. **Lumi/Sandbox:** Draft simulation architecture for Lemma C (Dynamical instability of pure vector fields).