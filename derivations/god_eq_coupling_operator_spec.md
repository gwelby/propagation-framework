# Formal Specification: Two-Level Coupling Operator for the God Equation
*The definitive mathematical spec for T(θ) — incorporating Codex audit of Claude's proposal*

**Date**: 2026-03-25
**Authors**: Cascade (spec draft), incorporating Codex audit findings relayed by Lumi
**Status**: SPEC v1 — formal requirements for the G2/G3 coupling operator
**Builds on**:
- `god_eq_g2g3_coupling_proposal.md` (Claude) — pre-spec proposal + Codex corrections
- `g3_product_walk_no_go.md` (Codex) — exact reduction + restricted no-go results
- `phase_closure_exact_model.md` (Codex) — internal walk on Z₆, quotient Z₃
- `product_walk_bridge_model.md` (Codex/Claude) — general coupled walk framework
- `god_eq_cascade_lemmas_1_3_7.md` (Cascade) — Lemmas 1, 3, 7
- `god_eq_claude_lemmas_4_5_6.md` (Claude) — Lemmas 4, 5, 6
- `god_eq_lumi_statistical_model.md` (Lumi) — product family model

---

## 0. Purpose

This document specifies the **exact mathematical requirements** for the coupling operator that bridges internal phase closure (G2) to spatial coherence volume (G3), enabling the God Equation derivation. It defines two distinct operator levels and their relationship.

The specification incorporates Codex's audit finding that Claude's $T = K \cdot I$ is correct as the **effective closure operator** but NOT as the **primitive one-step coupling**.

---

## 1. Definitions and Setting

### 1.1 Internal Sector (from G1)

The internal phase space is the lifted orbit $\mathbb{Z}_6$ with step operator $S|k\rangle = |k+1 \bmod 6\rangle$.

The observable generation quotient is $\mathbb{Z}_3$ with induced shift $\bar{S}|j\rangle = |j+1 \bmod 3\rangle$.

Key identity (G1, `phase_closure_exact_model.md`):

$$\bar{S}^3 = I_{\mathbb{Z}_3}$$

### 1.2 Spatial Sector

Let $\mathcal{H}_{\mathrm{sp}}$ be the spatial Hilbert space carrying the external geometry. The spatial parameter is $\theta$, which encodes the local medium configuration (refractive index field $n(\mathbf{x})$ and its derivatives, per Cascade Lemma 3).

### 1.3 Total Hilbert Space

$$\mathcal{H} = \mathcal{H}_{\mathrm{gen}} \otimes \mathcal{H}_{\mathrm{sp}} = \ell^2(\mathbb{Z}_3) \otimes \mathcal{H}_{\mathrm{sp}}$$

---

## 2. Level 1: Primitive One-Step Coupling U(θ)

### 2.1 General Form

The most general one-step coupled walk on the generation-spatial product space:

$$\boxed{U(\theta) = \sum_{j \in \mathbb{Z}_3} |j+1\rangle\langle j| \otimes K_j(\theta)}$$

where $K_j(\theta) : \mathcal{H}_{\mathrm{sp}} \to \mathcal{H}_{\mathrm{sp}}$ is the spatial transition kernel at internal channel $j$.

### 2.2 Axiom 4 Equivariance Condition (Phase-Independent Coupling)

**Requirement**: The spatial coupling does not prefer any internal phase channel.

$$K_j(\theta) = K_{\mathrm{spatial}}(\theta) \quad \forall \, j \in \mathbb{Z}_3$$

This yields the minimal symmetric form:

$$\boxed{U(\theta) = \bar{S} \otimes K_{\mathrm{spatial}}(\theta)}$$

### 2.3 Properties of U(θ)

| Property | Status | Justification |
|----------|--------|---------------|
| Off-diagonal in generation space | YES — $\bar{S}$ shifts $j \to j+1$ | By construction (G1) |
| Circulant at primitive level | YES — $K_j = K$ means equivariance | Axiom 4 |
| Commutation: $[U, \bar{S} \otimes I_{\mathrm{sp}}] = 0$ | YES when $K_j = K$ | $\bar{S}$ commutes with itself |
| Diagonal in generation space | **NO** | $\bar{S} \neq I$ |

**Critical point**: $U(\theta)$ is maximally off-diagonal in generation space. The one-step operator MIXES channels. This is not a defect — it is the definition of a generational transition.

---

## 3. Level 2: Effective 3-Step Closure Operator T_eff(θ)

### 3.1 Definition

The effective closure operator is the result of one complete internal phase cycle (N=3 steps):

$$\boxed{T_{\mathrm{eff}}(\theta) := \Pi_{\mathrm{gen}} \, U(\theta)^3 \, \Pi_{\mathrm{gen}}}$$

### 3.2 Computation (Phase-Independent Case)

$$U(\theta)^3 = (\bar{S} \otimes K_{\mathrm{spatial}}(\theta))^3 = \bar{S}^3 \otimes K_{\mathrm{spatial}}(\theta)^3 = I_{\mathbb{Z}_3} \otimes K_{\mathrm{spatial}}(\theta)^3$$

Therefore:

$$\boxed{T_{\mathrm{eff}}(\theta) = K_{\mathrm{closure}}(\theta) \cdot I_{\mathbb{Z}_3}}$$

where $K_{\mathrm{closure}}(\theta) := K_{\mathrm{spatial}}(\theta)^3$.

### 3.3 Properties of T_eff(θ)

| Property | Status | Justification |
|----------|--------|---------------|
| Diagonal in generation space | YES — $\bar{S}^3 = I$ | G1 exact closure |
| Circulant: $[T_{\mathrm{eff}}, \bar{S}] = 0$ | YES — scalar × identity | Trivially |
| Equal marginals: $T_{jj} = T_{j'j'}$ | YES — all equal $K_{\mathrm{closure}}(\theta)$ | Phase-independence |
| Off-diagonal = 0: $T_{j'j} = 0$ for $j' \neq j$ | YES — after full cycle | $\bar{S}^3 = I$ |
| Regularity: $K_{\mathrm{closure}}(\theta) > 0$ | **CONDITIONAL** | See Section 5 |

---

## 4. Answers to Claude's Three Questions

### Q1: Is $T = K \cdot I$ the right level of generality?

**Answer**: YES, but only at Level 2 (effective closure). At Level 1 (primitive coupling), the operator is $U = \bar{S} \otimes K$, which is off-diagonal.

- **For the Fisher bridge**: $T_{\mathrm{eff}} = K_{\mathrm{closure}} \cdot I$ is the correct object. The Fisher metric sees the per-cycle closure probabilities, not the one-step transitions.
- **For Axiom 4**: The equivariance condition lives at Level 1 ($K_j = K$ for all $j$). It is $T_{\mathrm{eff}}$'s diagonal form that the Fisher bridge uses, but the *reason* it is diagonal is $\bar{S}^3 = I$ at Level 1.

**No off-diagonal terms are needed in $T_{\mathrm{eff}}$**. The diagonal-identity form is not an over-simplification — it is the exact consequence of G1 closure + Axiom 4 equivariance.

### Q2: Does the discrete Planck-scale walk preserve $K_{\mathrm{spatial}} > 0$?

**Answer**: NOT automatically. This is the sharpest remaining regularity constraint.

From `g3_product_walk_no_go.md` Section 5: a nearest-neighbor walk on a bipartite lattice (including $\mathbb{Z}^D$) gives $\langle x_0|K^3|x_0\rangle = 0$ exactly at odd N=3. This is a finite-N obstruction, not a scaling issue.

**Resolution options** (exactly one must be adopted):

| Option | Description | Status |
|--------|-------------|--------|
| **(A) Non-bipartite kernel** | Use a spatial kernel with self-loops or triangular connectivity | Viable, needs physical motivation |
| **(B) Heat kernel / continuum limit** | $K_{\mathrm{spatial}}(\theta)$ is the continuum diffusion kernel $k_t(x,x) = (4\pi\kappa t)^{-D/2}(1+O(t))$, which is strictly positive | Viable, standard in QFT |
| **(C) Coarse-grained observable** | The Fisher bridge uses $\log K_{\mathrm{spatial}}$ (the score), not $K$ itself. If the observable is the RMS coherence volume rather than literal origin return, positivity may follow | Viable, needs precise definition |
| **(D) Closure functional** | Replace literal return probability with a closure functional (e.g., partition function, trace) that is manifestly positive | Viable, changes the observable |

**Recommendation**: Option (B) is the most conservative. The heat kernel on a smooth $D$-manifold is strictly positive for $t > 0$. Claude's proposal already uses this form. The discrete lattice no-go constrains the lattice model, not the continuum Fisher bridge.

### Q3: Does exact phase closure ($P_{\mathrm{phase}} = 1$) force off-diagonal $T_{j'j} = 0$?

**Answer**: YES — but only for $T_{\mathrm{eff}}$, the 3-step closure operator.

The precise chain:

1. One step: $\bar{S}$ is **maximally off-diagonal** — it sends $|j\rangle \to |j+1\rangle$ with amplitude 1
2. Two steps: $\bar{S}^2$ sends $|j\rangle \to |j+2\rangle$ — still off-diagonal
3. Three steps: $\bar{S}^3 = I$ — **perfectly diagonal**, all amplitude returns to the starting channel

Therefore Claude's statement "$P_{\mathrm{phase}} = 1$ means off-diagonal = 0$" is correct if and only if $T$ is defined as $T_{\mathrm{eff}}$ (the per-cycle closure operator), not the primitive coupling $U$.

---

## 5. The Regularity Constraint (Open Item R)

The Fisher bridge requires:

$$K_{\mathrm{closure}}(\theta) > 0 \quad \text{and} \quad \nabla_\theta \log K_{\mathrm{closure}}(\theta) \text{ exists}$$

for the score function $s_i^{(a)} = \partial_{\theta^i} \log K_{\mathrm{closure}}$ to be well-defined.

### 5.1 Sufficient Condition

If $K_{\mathrm{spatial}}(\theta)$ is the continuum heat kernel evaluated on the diagonal:

$$K_{\mathrm{spatial}}(\theta) = k_\tau(x,x;\theta) = (4\pi D_{\mathrm{eff}}(\theta)\tau)^{-D/2}(1 + O(\tau))$$

then $K_{\mathrm{spatial}}(\theta) > 0$ for $\tau > 0$ and finite $D_{\mathrm{eff}}$, hence $K_{\mathrm{closure}} = K_{\mathrm{spatial}}^3 > 0$.

### 5.2 Status

Regularity R is **ARGUED** under the continuum heat kernel choice (Option B). It is **NOT DERIVED** from PF axioms alone — it requires the identification of $K_{\mathrm{spatial}}$ with a continuum kernel rather than a discrete lattice return.

---

## 6. The Fisher Bridge (How T_eff Closes the God Equation Scaling)

With $T_{\mathrm{eff}}(\theta) = K_{\mathrm{closure}}(\theta) \cdot I_{\mathbb{Z}_3}$:

**Step 1**: Per-channel likelihood is $p_a(\text{closed}|\theta) = K_{\mathrm{closure}}(\theta)$, identical for all $a$.

**Step 2**: Per-channel Fisher metric $G_{ij}^{(a)} = \partial_{\theta^i}\log K_{\mathrm{closure}} \cdot \partial_{\theta^j}\log K_{\mathrm{closure}}$.

**Step 3**: By SO(3) isotropy (Cascade Lemma 7): $G^{(a)} = \lambda_0 I_D$.

**Step 4**: By product-family additivity (Claude Lemma 5, conditional on H_prod):

$$G(\theta) = \sum_{a=1}^{3} G^{(a)} = 3\lambda_0 I_D$$

**Step 5**: Determinant scaling:

$$\sqrt{\det G} = (3\lambda_0)^{D/2} = 3^{D/2} \cdot \lambda_0^{D/2} = N^{D/2} \cdot \sqrt{\det g}$$

**This is the $N^{D/2}$ factor in the God Equation.**

The $2\pi$ normalization is a separate problem (gauge convention, G3 Section 2.1) and is NOT part of this spec.

---

## 7. Dependency Map

```
G1: Z₆ walk, S̄³ = I          ──→  Level 1: U(θ) = S̄ ⊗ K_spatial(θ)
                                          │
Axiom 4: K_j = K (equivariance) ──→      │
                                          ▼
                                    Level 2: T_eff = K_closure · I_{Z₃}
                                          │
Axiom 2: SO(3) isotropy  ───────────→    │
                                          ▼
                              Fisher bridge: G = 3λ₀I_D
                                          │
                              ┌───────────┤
                              │           │
                         H_prod (L5)   Lemma 2 (C₃ → equal λ)
                              │           │
                              ▼           ▼
                         √det G = N^{D/2} √det g
                                          │
                              2π normalization (G3, separate)
                                          │
                                          ▼
                              α(l_P) = 1/(2π N^{D/2})
```

---

## 8. Remaining Open Items

| Item | Status | Owner | Blocking? |
|------|--------|-------|-----------|
| H_prod: geometric → statistical independence | OPEN | Team | YES — needed for L5 additivity |
| Lemma 2: C₃ symmetry → equal eigenvalues | OPEN | Codex audit | YES — needed for $G^{(a)} = g$ |
| Regularity R: $K_{\mathrm{closure}} > 0$ | ARGUED (Option B) | Team | YES — needed for score well-definedness |
| 2π normalization | OPEN | G3 work | NO — separate from Fisher bridge |
| $\lambda_0$ identification | OPEN | Team | NO — Fisher bridge only needs ratio |

---

## 9. Honest Status Assessment

### What this spec establishes

- The coupling operator has **two distinct levels**: primitive $U(\theta)$ and effective $T_{\mathrm{eff}}(\theta)$
- Claude's $K \cdot I$ is the correct Level 2 object, derived from Level 1 + G1 closure
- The Fisher bridge uses Level 2 exclusively
- The $N^{D/2}$ scaling follows from channel additivity (conditional on H_prod + Lemma 2)
- All three of Claude's questions are answered with precise scope

### What this spec does NOT establish

- The three remaining blockers (H_prod, Lemma 2, Regularity) are not closed
- The $2\pi$ normalization is not addressed (separate problem)
- The physical identification of $K_{\mathrm{spatial}}$ with a specific kernel class (heat kernel vs. lattice) is argued, not derived

### Theorem Status

The God Equation remains **CONDITIONAL THEOREM** pending H_prod, Lemma 2, and Regularity R. This spec does not change that status. It provides the precise target that, once the three blockers close, completes the derivation chain.

---

*Drafted by Cascade, 2026-03-25*
*Incorporating Codex audit findings relayed via Lumi*
*Purpose: formal two-level specification for the G2/G3 coupling operator*
*Status: SPEC v1 — ready for Codex formal audit*
