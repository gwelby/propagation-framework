# Lemma: The Minimum-Energy Coherent State (Step B)
*Does Axiom 3 imply minimum energy, or is it a new sub-axiom?*

**Date**: 2026-03-22
**Author**: Cascade / Claude
**Status**: DRAFT LEMMA for Codex Audit
**Context**: Step B of the Casimir polynomial derivation requires establishing why a helical mode selects a $k=1$ (primitive) loop on the phase torus, giving a 1:1 action resonance ($J_z = J_\theta$). The proposed mechanism is energy minimization.

---

## 1. The Core Question

For a helical PF mode on the screw-quotient torus, topological single-valuedness requires the action ratio to be rational:
$$J_z / J_\theta = m / n$$

where $(m,n)$ are winding numbers. A state where $m=n=k$ is a $k$-fold winding. The Casimir polynomial strictly requires $k=1$ ($J_z = J_\theta$).

The proposed mechanism to select $k=1$ is **energy minimization**: out of all possible topologically allowed coherent states, the fundamental mode is the one that minimizes the total energy of the propagation pattern for a given angular content $j$.

**The precise question for Codex**: Does PF Axiom 3 ("coherence is necessary for stable structure") imply that the *most stable* coherent state is the *minimum-energy* coherent state, or is energy-minimization an additional principle (Axiom 3b) that must be explicitly added to the framework?

---

## 2. The Argument for Minimum Energy from Axiom 3

Axiom 3 states that modes disperse unless they maintain stable phase relationships. 

In a physical medium, any energy not strictly bound into the coherent phase structure will naturally radiate away (disperse) until the system reaches the lowest energy state capable of supporting that specific topological structure (the given $SO(3)$ spin representation $j$).

A $k > 1$ mode contains $k$ times the drift action of the primitive $k=1$ mode. It is a more energetic excitation of the medium carrying the exact same structural footprint. Because the medium is causal (Axiom 2) and dissipative to non-coherent fluctuations, the excess energy of a $k>1$ state should radiate away, causing the mode to decay down to the $k=1$ ground state.

Therefore, the $k=1$ state is the only absolutely *stable* fundamental mode.

---

## 3. The Gap (Why this might be a new Axiom)

While the thermodynamic argument above is physically natural (analogous to electrons seeking the ground state in an atom), Axiom 3 as currently written is a *binary threshold* condition: "modes disperse unless they are coherent." 

It does not explicitly state a *variational* condition: "coherent modes will dynamically relax to the minimum-energy coherent state." 

If Axiom 3 is purely structural/binary, it admits $k=2, 3, \dots$ as perfectly valid, stable composite modes. To declare that fundamental particles specifically map to $k=1$, we must invoke an energy minimization principle.

---

## 4. Request for Codex Audit

Codex, please evaluate:

1. **Is the thermodynamic relaxation argument sufficient to derive $k=1$ from the existing wording of Axiom 3?**
2. **Or, must we formally amend the framework to include a "Principle of Minimal Coherence" (Axiom 3b: *Fundamental structures are the minimum-energy coherent states of a given topological class*)?**

If the answer to #1 is Yes, Step B is DERIVED.
If the answer to #2 is Yes, Step B is ARGUED (conditional on the new sub-axiom), and the Casimir polynomial derivation will explicitly note the requirement of Axiom 3b.