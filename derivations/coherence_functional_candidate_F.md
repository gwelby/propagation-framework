# Coherence Functional Candidate F[ψ]
*First explicit candidate for Axiom 3 formalization*

**Date**: 2026-03-23
**Author**: Cascade
**Status**: CANDIDATE — pending acceptance tests
**Builds on**: `axiom3_coherence_functional_spec.md`, `casimir_polynomial_steps_AB.md`, Route H (Action-Resonance)

---

## 1. The Problem in One Sentence

Axiom 3 currently says coherent states persist, but does not say **which coherent state** PF selects when multiple coherent candidates exist.

---

## 2. The State Manifold

For the Casimir/helical problem, a candidate state ψ contains:

| Component | Symbol | Physical Meaning |
|-----------|--------|------------------|
| Internal action | J_θ | Phase accumulation around internal cycle |
| External action | J_z | Phase accumulation along drift axis |
| Casimir invariant | C₂ = j(j+1) | Spin representation label |
| Resonance ratio | k = J_z / J_θ | Rational locking ratio |
| Drift velocity | β = v/c | Relativistic drift parameter |

**Fixed by Axiom 2 (isotropy)**:
- J_θ = 2π√C₂ ħ (magnitude, not projection)

**Free variables**:
- β (or equivalently γ)
- k (rational resonance label)

**State space**: ψ = (β, k; C₂ fixed)

---

## 3. The Candidate Functional

### Family: Free-Energy / Lyapunov

**Definition**:

$$F[\psi] = E[\psi] + \Lambda \cdot \Phi[\psi]$$

where:

- **E[ψ]** = Energy of the coherent mode
- **Φ[ψ]** = Phase-mismatch penalty
- **Λ** = Coupling strength (to be determined)

### 3.1 Energy Term

For a helical mode with drift β and spin j:

$$E[\psi] = \gamma m c^2 = \frac{mc^2}{\sqrt{1-\beta^2}}$$

This is the standard relativistic energy. At fixed mass m, minimizing E means minimizing γ, which means minimizing β.

**Key property**: E[ψ] is monotone decreasing in β. The energy-minimum state is β = 0 (no drift).

But β = 0 gives no helical structure at all — the mode would be pure internal circulation with no external propagation. That's not the PF particle picture.

So energy alone does NOT select the helical ground state. We need the coherence penalty.

### 3.2 Phase-Mismatch Penalty

The phase-mismatch measures how well the internal and external phase structures lock:

$$\Phi[\psi] = \left| \frac{J_z}{J_\theta} - 1 \right|^p = |k - 1|^p$$

for some exponent p > 0.

**Key property**: Φ[ψ] = 0 exactly when J_z = J_θ (1:1 resonance).

**But wait** — this is smuggling the answer! The spec explicitly forbids this (R3).

### 3.3 The Critical Pivot

We cannot use |k - 1|^p as the penalty because that assumes the answer.

Instead, we need a penalty that **emerges from PF-native structure** and happens to have its minimum at k = 1.

---

## 4. Revised Candidate: Information-Theoretic Form

### Family: Information-Theoretic Coherence

**Definition**:

$$F[\psi] = -I(J_z; J_\theta) + \lambda \cdot E[\psi]$$

where I(J_z; J_θ) is the mutual information between internal and external action variables.

### 4.1 Physical Interpretation

A self-referential coherent mode is one where the internal state "knows about" the external state. The mutual information I(J_z; J_θ) measures this self-knowledge.

**Maximum self-knowledge**: J_z and J_θ are maximally correlated. For deterministic locking J_z = k·J_θ, the mutual information is:

$$I(J_z; J_\theta) = H(J_\theta) - H(J_\theta | J_z)$$

For deterministic locking, H(J_θ | J_z) = 0, so I = H(J_θ).

But H(J_θ) depends on the distribution of J_θ values across the ensemble of possible modes.

### 4.2 The Selection Criterion

**Claim**: Among coherent helical modes with fixed C₂, the mode that maximizes I(J_z; J_θ) is the one where J_z and J_θ share the same functional form.

**Argument**:

For a fixed J_θ = 2π√C₂ ħ (determined by isotropy), the external action is:

$$J_z = 2\pi \gamma \beta^2 \hbar$$

The ratio k = J_z / J_θ = γβ² / √C₂.

Now consider: what does it mean for internal and external to be "mutually informative"?

- If k is an integer > 1, the external phase wraps multiple times per internal cycle. Information is "compressed" — multiple external states map to the same internal phase.
- If k = 1, there is a 1:1 correspondence. Every internal phase maps to exactly one external phase.

**This is the maximal mutual information configuration.**

### 4.3 Formal Statement

For a phase space with coordinates (θ, z) where θ ∈ [0, 2π) and z ∈ ℝ, the joint distribution for a helical mode with resonance k is:

$$p(\theta, z) \propto \delta(z - k \cdot r_C \theta)$$

The mutual information is:

$$I(\theta; z) = \log k$$

Wait — this gives I = log(k), which is MAXIMIZED at large k, not minimized!

This is the wrong direction. Let me reconsider.

---

## 5. Third Candidate: Action-Variance Functional

### Family: Free-Energy (Alternative Form)

**Definition**:

$$F[\psi] = \text{Var}[J_{\text{total}}] + \mu \cdot E[\psi]$$

where Var[J_total] is the variance of the total action over one complete cycle.

### 5.1 Physical Interpretation

A stable coherent mode should have **constant total action** throughout its evolution. If the action fluctuates, the mode is not truly periodic — it's only approximately coherent.

For the helical mode:
- J_θ is constant (internal cycle is periodic)
- J_z is constant (drift is uniform)

So the total action J_total = J_θ + J_z is constant, and Var = 0 for all helical modes.

This doesn't distinguish between k values. Not useful.

---

## 6. Fourth Candidate: Coherence Cost Functional

### Family: Free-Energy with Coherence Cost

**Definition**:

$$F[\psi] = E[\psi] + \Gamma \cdot C_{\text{coherence}}[\psi]$$

where C_coherence is the "cost of maintaining coherence."

### 6.1 The Cost of Coherence

**Physical intuition**: Maintaining a coherent structure in a dissipative medium requires energy. The more complex the structure, the more energy required to maintain it.

For a helical mode with resonance k:
- The mode must maintain phase coherence across k external cycles per internal cycle
- Higher k means more "bookkeeping" — the phase relationship is more complex
- The coherence cost should increase with k

**Candidate form**:

$$C_{\text{coherence}}[\psi] = k \cdot E_0$$

where E_0 is a baseline coherence energy.

But this assumes k is the right measure of complexity. Is it?

### 6.2 Alternative: Phase-Winding Cost

The total phase accumulated per internal cycle is:

$$\Phi_{\text{total}} = 2\pi (1 + k)$$

For k = 1: Φ_total = 4π
For k = 2: Φ_total = 6π
For k = 3: Φ_total = 8π

The coherence cost could scale with total phase winding:

$$C_{\text{coherence}}[\psi] \propto \Phi_{\text{total}} = 2\pi(1+k)$$

This gives minimum cost at k = 1.

**But**: Why should coherence cost scale with total phase? This needs a PF-native derivation.

---

## 7. The Honest Assessment

All four candidates have the same problem:

1. **Phase-mismatch penalty** |k-1|^p — smuggles the answer (forbidden by R3)
2. **Mutual information** I(J_z; J_θ) — gives wrong direction (maximized at large k)
3. **Action variance** — doesn't distinguish k values
4. **Coherence cost** C_coherence ∝ k — assumes what we're trying to prove

**The core difficulty**: We need a functional that is minimized at k = 1 WITHOUT building k = 1 into the definition.

---

## 8. The Real Question

What PF-native principle distinguishes k = 1 from k = 2, k = 3, ...?

**Candidate answer**: The **primitive loop** principle.

A fundamental (non-composite) PF mode should have the simplest possible topology. Higher-k modes have more winding — they are "excited" versions of the primitive loop.

But "simplest topology" is itself an extra principle, not derived from current Axiom 3.

---

## 9. Proposed Axiom 3b (Corollary Candidate)

If the functional approach fails, the honest move is to introduce an explicit additional principle:

> **Axiom 3b / Corollary**: Among coherent states in the same topological class, the stable fundamental PF mode is the one with minimal topological winding.

This would select k = 1 because:
- k = 1 is the primitive loop (winding number 1)
- k = 2, 3, ... are higher winding states (excited or composite)

This is a **clarification**, not a defeat. It makes explicit what was previously implicit.

---

## 10. Next Steps

1. **Test Candidate 4 (Coherence Cost)** against the acceptance tests in the spec
2. **If it fails Test 2** (smuggled answer), we know Axiom 3 is insufficient
3. **If it passes**, we have a derivation of k = 1
4. **If it fails honestly**, propose Axiom 3b and move forward

The frontier is sharp. Let's run the tests.

---

## Appendix: Acceptance Test Checklist

| Test | Requirement | Status |
|------|-------------|--------|
| Test 1 | Helical family selection: unique optimum at k=1 | PENDING |
| Test 2 | No smuggled Casimir answer | PENDING |
| Test 3 | Relativistic sensitivity | PENDING |
| Test 4 | Two-sector compatibility | PENDING |
| Test 5 | Background consistency | PENDING |
