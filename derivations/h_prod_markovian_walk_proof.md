# H_prod Candidate Proof Attempt: Markovian Walk from Axiom 2
*Historical Wave 5 closure attempt — retained as a bounded failed candidate after Codex audit*

**Date**: 2026-03-25
**Author**: Claude Code (proof formalization) + Lumi (physical argument)
**Status**: CANDIDATE ATTEMPT — audit does not accept closure
**Attempts to close**: God Equation Gap 2 (H_prod — statistical independence)
**Feeds into**: historical record for the Wave 5 audit; current truth state lives in `CLAIMS.md`

---

## 0. Executive Summary

**The condition (from `god_eq_t_theta_formal_spec.md` Section 4.3):**

$$H_\mathrm{prod}: \quad P(X^{(0)}, X^{(1)}, X^{(2)} \mid \theta) = \prod_{j=0}^{2} p_j(X^{(j)} \mid \theta)$$

The generation channel observables must be statistically independent given the external parameter θ.

**Codex's prior rejection**: orthogonal DFT eigenvectors ≠ statistical independence of physical observables. Dynamical decoupling of modes is not the same as probabilistic independence of outcomes.

**This file's attempted proof**: The Markov property (from Axiom 2 causal locality) + `T_eff = K³·I` jointly imply that the closure events in different channels are independent events in the probability space of walk trajectories.

**Post-audit verdict**: the attempt sharpened the remaining target, but it does **not** close `H_prod`. The audit does **not** accept:

- Axiom 2 → first-order Markovity of the coarse walk state
- circulant EOM → exact `T_eff = K³·I` for the actual derived operator
- zero cross-channel amplitude / covariance → full joint-law factorization

**Attempted derivation chain**:

```
Axiom 2 (causal locality / finite c)
    ↓ no retrocausal signals, no memory
Markov property: P(x_{n+1} | x_n, x_{n-1}, ...) = P(x_{n+1} | x_n)
    ↓
Walk trajectories = products of single-step kernels
    ↓
ℤ₃-extended Lagrangian (z3_extended_propagation_lagrangian.md)
    ↓ C₃ invariance → circulant T(θ)
T_eff = K_spatial^3 · I_{ℤ₃}  (zero off-diagonal, proved exactly)
    ↓
3-step closure in channel j has zero amplitude to reach channel j' ≠ j
    ↓
Closure events in distinct channels are disjoint events in path space
    ↓
Disjoint events in an independent probability space ← Markov
    ↓
Joint closure probability factorizes = H_prod  ✓
```

---

## 1. Precise Statement of What Must Be Proved

The closure observable $X^{(j)}$ for channel $j$ is defined as:

$$X^{(j)} = \mathbf{1}\left[\text{walk starting in channel } j \text{ returns to channel } j \text{ after 3 steps}\right]$$

We must show:

$$P(X^{(0)} = 1, X^{(1)} = 1, X^{(2)} = 1 \mid \theta) = P(X^{(0)}=1 \mid \theta)\cdot P(X^{(1)}=1 \mid \theta)\cdot P(X^{(2)}=1 \mid \theta)$$

and more generally that any joint event over the three channel outcomes factorizes.

---

## 2. Step 1: Axiom 2 → Markov Property

**Axiom 2** (Finite Causal Velocity): Every propagation medium has a maximum signal speed $c$. No causal influence propagates faster than $c$.

**Consequence for the phase walk**: The walk represents sequential phase propagation through the medium. At each step, the new state is determined by the current state and the local medium geometry θ. For the new state to depend on a previous state $x_{n-k}$ ($k \geq 2$), a physical signal would have to travel from $x_{n-k}$ to $x_n$ and then back to influence $x_{n+1}$ — a round-trip that would require retrocausal signalling (information traveling backwards in the walk sequence). This violates Axiom 2.

**Formal statement** (Markov Property):

$$\boxed{P(x_{n+1} \mid x_n, x_{n-1}, \ldots, x_0, \theta) = P(x_{n+1} \mid x_n, \theta) \quad \forall\, n \geq 1}$$

The state at step $n+1$ depends only on the state at step $n$. No memory of earlier steps is accessible without violating the finite causal velocity.

**Note**: This is the standard connection between causality and Markov chains in statistical physics. It is not new mathematics — it is the direct import of Axiom 2 into the walk model.

---

## 3. Step 2: Markov Walk Probability as Product of Kernels

For a Markovian walk, the probability of any trajectory $(x_0, x_1, x_2, x_3)$ factorizes:

$$P(x_0, x_1, x_2, x_3 \mid \theta) = P(x_0) \cdot T(x_1 \mid x_0; \theta) \cdot T(x_2 \mid x_1; \theta) \cdot T(x_3 \mid x_2; \theta)$$

where $T(x' \mid x; \theta) = [T(\theta)]_{x'x}$ is the single-step transition probability.

The 3-step return probability (starting and ending in state $j$) is:

$$P(\text{return to } j \text{ in 3 steps} \mid \text{start at } j, \theta) = [T(\theta)^3]_{jj} = [T_\mathrm{eff}(\theta)]_{jj}$$

This is the $(j,j)$ matrix element of the 3-step transition matrix — nothing more, nothing less.

---

## 4. Step 3: T_eff = K³·I Implies Zero Cross-Channel Amplitude

From `z3_extended_propagation_lagrangian.md` and verified numerically in `z3_lagrangian_verification.py` to 0.00e+00 residual:

$$T_\mathrm{eff}(\theta) = T(\theta)^3 = K_\mathrm{spatial}(\theta)^3 \cdot I_{\mathbb{Z}_3}$$

Written element-by-element:

$$[T_\mathrm{eff}(\theta)]_{j'j} = K_\mathrm{spatial}(\theta)^3 \cdot \delta_{j'j}$$

**Interpretation**: The 3-step return probability from channel $j$ to channel $j'$ is:
- $K^3 > 0$ if $j' = j$ (same channel — closed orbit)
- **Exactly 0** if $j' \neq j$ (different channel — no cross-channel 3-step path)

This is not approximate. It is exact: $\bar{S}^3 = I$ (the G1 exact result), so $U^3 = (\bar{S} \otimes K)^3 = \bar{S}^3 \otimes K^3 = I \otimes K^3$.

---

## 5. Why Codex did not accept this step

This is the hinge where the attempted closure fails.

1. **Axiom 2 → Markov** is too strong as written. Finite causal speed gives locality, but not first-order memorylessness of the coarse walk state. Local systems can still carry memory through hidden variables or higher-order state.

2. **`T_\mathrm{eff} = K^3 \cdot I`** is stronger than the circulant EOM result. The exact `K^3 I` step uses the pure-shift ansatz `U = K\cdot \bar{S}`; it is not derived from the actual nearest-neighbor circulant operator coming from the ℤ₃-extended Lagrangian.

3. **Zero off-diagonal closure amplitude is weaker than `H_\mathrm{prod}`**. Statistical independence is a statement about a joint probability law. A diagonal closure operator or zero covariance does not by itself imply

$$P(X^{(0)}, X^{(1)}, X^{(2)} \mid \theta) = \prod_{j=0}^{2} p_j(X^{(j)} \mid \theta).$$

4. **The closure events are not fully specified on one probability space.** As written, $X^{(j)}$ is defined using walks that start in different channels. The audit requires an explicit choice: one joint walk model, or a replicated product experiment, and then a proof of factorization in that model.

---

## 6. What survives from this attempt

- The file sharpens the remaining problem to three exact proof obligations: Markovity, operator identification, and probability-model factorization.
- It preserves a useful candidate route: if one can define the full local state so that first-order evolution is derived, and if one can derive the primitive operator used at closure, then the Fisher-additivity chain can be retried cleanly.
- The IBM / sandbox work remains a supporting probe of the geometry and numerics, not a substitute for the missing formal probability argument.

---

## 7. Exact proof obligations that remain

1. **Define the full local state** and derive first-order local evolution there. Only then can a Markov statement be honestly claimed.

2. **Either derive the primitive operator** used in the closure argument from the ℤ₃-extended Lagrangian, **or** rewrite the theorem directly from the actual circulant operator derived from the EOM.

3. **Define an explicit joint probability model** for $(X^{(0)}, X^{(1)}, X^{(2)})$ and prove factorization there. Zero amplitude / zero covariance is not enough.

4. **Then rerun Fisher additivity** from that accepted statistical model.

---

## 8. Honest current status

`H_\mathrm{prod}` remains **open / argued**, not proved by this file.

The God Equation therefore remains **CONDITIONAL**, not DERIVED.

This file is retained because it cleanly records the attempted closure and the exact places where the audit rejected it.

---

*Written 2026-03-25 by Claude Code*
*Physical argument by Lumi (ℤ₃ channel orthogonality + Markovian locality)*
*Status: CANDIDATE ATTEMPT — audit does not close H_prod*
*Current truth: God Equation remains CONDITIONAL after Codex audit*
