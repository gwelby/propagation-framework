# Step B Lemma — Minimum-Energy Coherent State from Axiom 3
*The bounded question Cascade identified. For Codex to evaluate.*

**Date**: 2026-03-23
**Author**: Claude
**The Question** (Cascade's formulation, 2026-03-22):
> Does Axiom 3 ("coherence is necessary for stable structure") imply that the stable coherent state is the minimum-energy coherent state?

**If yes**: k=1 follows → polynomial derived from Axioms 1-3
**If no**: k=1 requires an explicit additional principle → state it cleanly and honestly

---

## 1. Setup

A helical PF mode with spin j and mass m can be in any of a family of coherent states parametrized by k > 0 (real):

$$J_z = k \cdot J_\theta \implies \gamma\beta^2 = k\sqrt{C_2}$$

Each k-value gives a different drift velocity β_k (satisfying γ_k β_k² = k√C₂) and a different energy:

$$E_k = \gamma_k mc^2 = \frac{mc^2}{\sqrt{1-\beta_k^2}}$$

Since β_k increases with k (higher k requires larger drift), E_k is a strictly increasing function of k. The minimum-energy coherent state is k=1.

All these states satisfy Axioms 1 and 2 (each is a propagating mode at β_k c < c). All satisfy Axiom 3 in the sense of maintaining individual coherence (each loop on the helix torus is individually coherent). The question is whether Axiom 3 selects one k over others.

---

## 2. The Minimum-Energy Claim

**Candidate Lemma** (to be evaluated):

> **Lemma B**: Among all k > 0 coherent helical modes with spin j and mass m (satisfying Axioms 1-3), the unique stable state is the one with minimum energy: k = 1.

**Motivation**: In physics, when multiple quantum states satisfy the coherence/stability conditions, the ground state (minimum energy) is the one that is stable against perturbations. Excited states decay to the ground state by emitting energy. If the PF medium allows any energy loss (even infinitesimal dissipation), higher-k modes are unstable and will decay toward k=1.

---

## 3. Arguments For

### Argument F1: Dissipative medium

Axiom 3 says coherence is the "necessary condition for structure." Implicit in this: incoherent propagation is the background, and coherent modes are stable islands in an incoherent background.

In a dissipative medium (incoherent propagation removes energy from coherent modes), the equilibrium coherent state is the one with minimum energy consistent with the coherence condition. Higher-k modes (higher energy for the same j) would lose energy to the incoherent background until they reach k=1.

**Gap**: Axiom 3 does not explicitly state that the PF medium is dissipative. It says coherence is necessary for structure, but not that incoherent propagation actively drains energy from coherent modes.

### Argument F2: Variational stability

The coherent ground state (k=1) is a local minimum of the energy functional for fixed spin j. A perturbation of the drift velocity away from β_1 moves the mode to k ≠ 1, which has higher energy. The mode returns to k=1 by lowering its kinetic energy.

This is a Lyapunov stability argument: k=1 is stable because any perturbation increases energy, and the mode relaxes back.

**Gap**: This requires that the mode CAN lose kinetic energy — i.e., that β is not fixed by initial conditions but dynamically selected. If β is fixed by initial conditions (a free parameter), then k is also a free parameter and k=1 is not selected.

### Argument F3: Thermodynamic dominance

In a statistical ensemble of helical modes, the Boltzmann weight for energy E_k is e^{-E_k/T}. At any finite temperature, the k=1 state has the highest Boltzmann weight and dominates the ensemble.

**Gap**: This is a statistical argument, not a derivation from axioms. It requires the concept of temperature and a thermal ensemble, which are not directly stated in the PF axioms (though temperature as "average incoherent frequency" is Derived Quantity 2 in the PF document).

---

## 4. Arguments Against

### Argument A1: k is a free parameter, not a dynamical variable

The velocity β of a mode is a free parameter — it depends on how the mode was created (what initial conditions were imposed). Nothing in Axioms 1-3 selects a specific β. A mode with any β < 1 is equally valid. Therefore k = γβ²/√C₂ is a free continuous parameter, and no single k is selected.

**The challenge**: If this argument holds, the Casimir polynomial γβ² = √C₂ is not a constraint at all — it's just a definition of what we CALL the "coherent mode." The polynomial would not be a physical prediction but a definitional choice.

**Response**: The polynomial IS a physical prediction — it predicts the mass-to-velocity relationship for stable particles, and this prediction matches experimental data (Weinberg angle, to 0.13σ). So something must select the specific k=1 velocity. The question is whether that "something" comes from Axioms 1-3 or requires additional input.

### Argument A2: Excited states can also be stable

In quantum mechanics, excited states are stable when they cannot decay (e.g., conservation laws prevent the decay). For helical PF modes:
- Can a k=2 mode decay to a k=1 mode? Only if there is a mechanism to dissipate kinetic energy.
- If the PF medium conserves energy (no dissipation), all k-values are equally stable.

**Response**: The PF medium does have incoherent propagation (Axiom 3's "noise = zero coherence" end of the spectrum). If the medium can absorb kinetic energy into incoherent modes, then k=2 is unstable against decay to k=1. But this requires the medium to be at least partially dissipative for coherent modes.

---

## 5. The Honest Assessment

The minimum-energy argument (Lemma B) is physically compelling but depends on an implicit assumption about the PF medium:

**Assumption B**: The PF medium provides a dissipative environment for coherent modes — incoherent propagation can absorb excess kinetic energy from a k>1 mode, driving it toward the k=1 ground state.

This assumption is CONSISTENT with Axiom 3 ("incoherent propagation = noise = background") but is NOT explicitly stated in Axiom 3. Axiom 3 says coherence is necessary for structure; it does not say incoherent modes actively drain excess energy from coherent modes.

**Two possible outcomes**:

**Outcome 1**: Codex finds that Assumption B follows from Axiom 3's structure (e.g., from the spectrum of coherence levels described in the axiom — "zero coherence: thermal noise, maximum entropy" implies the medium tends toward noise, meaning coherent modes lose energy to noise unless at minimum-energy configuration). If so, Lemma B is derived and Step B is closed.

**Outcome 2**: Codex finds that Assumption B is an independent principle not derivable from Axiom 3. Then k=1 requires an explicit additional axiom (call it **Axiom 3b**: "Among multiple coherent states satisfying Axioms 1-3, the stable state is the one that minimizes energy for given mass and spin"). The polynomial is then derived from Axioms 1-3 + Axiom 3b, and Issue #3 status would be: ARGUED (0.75) with one explicit additional principle.

---

## 6. The Clean Statement for Codex

**Question**: Does the following statement follow from Axiom 3 as written in `the_propagation_framework.md`?

> "When multiple coherent states are possible for a given mass m and spin j (parametrized by k > 0), the state that is stable against perturbations by the incoherent background (thermal noise) is the one with minimum energy — i.e., k = 1."

**Context from Axiom 3**: "Zero coherence: thermal noise, maximum entropy, no extractable information." This establishes that the background is entropy-maximizing. The question is whether a high-entropy background selects minimum-energy coherent states, or whether it is neutral between all coherent k-values.

**If yes**: Minimum-energy → k=1 → Step B DERIVED.
**If no**: State what additional principle is needed. Draft it as a sub-axiom for team consideration.

---

## 7. What Codex Needs to Return

One of:

A. **Step B DERIVED**: Axiom 3's maximum-entropy background implies energy minimization for coherent modes. Lemma B follows. Specify the logical chain.

B. **Step B requires Axiom 3b**: Minimum energy is not a consequence of Axiom 3. A clean statement of Axiom 3b (or a corollary) is needed. Draft the statement.

C. **Step B NO-GO**: The velocity β is a free parameter not constrained by Axioms 1-3 alone. The polynomial is not derivable from these three axioms. Additional structure (a 4th axiom, or a physical selection mechanism) is required.

---

*Claude — 2026-03-23*
*Lemma B: the bounded question Cascade identified. For Codex to evaluate.*
*Do not update CLAIMS.md or ACTIVE_ISSUES.md pending Codex response.*
*Issue: #3, Casimir polynomial component (c)*
