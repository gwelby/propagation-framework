# Claude's Lemmas: Score Decomposition, Orthogonality, Common-Mode Control
*Lemmas 4, 5, and 6 for the Generation-Channel Additivity Theorem*

**Date**: 2026-03-24 (revised after Codex audit)
**Author**: Claude
**Task**: Attack Lemmas 4, 5, and 6 per Codex's bounded team split
**Status**: CANDIDATE v2 — re-submitted after Codex audit feedback
**Builds on**:
- `god_eq_lumi_statistical_model.md` — product family, topological conditional independence
- `god_eq_cascade_lemmas_1_3_7.md` — Lemma 1 (distinguishable channels), Lemma 3 (common parameter θ), Lemma 7 (isotropy → g = λ₀ I_D)
- `phase_closure_exact_model.md` — ℤ₆ → ℤ₃ internal structure
- `closing_the_gaps.md` — C₃ and Koide geometry

**Audit corrections from Codex v1 review**:
- Fixed: broken AM-GM determinant argument (was treating G as block-diagonal per channel; G = (Σλₐ) I_D has `det = (Σλₐ)^D`, not a product over λₐ)
- Fixed: premature closure claim ("theorem closes") — Lemma 2 is still Codex's pending item
- Added: explicit H_prod conditioning on L4 and L5
- Simplified: Lemma 6 now takes Codex's recommended Option 2 (scoped determinant claim, drop perturbation section)
- Added: honest note that the CM-S/CM-R split is a useful conceptual distinction but not the same as a full block/projection proof

---

## Setup: The Objects in Play

**Adopted hypothesis H_prod** (from Lumi's model, Section 2):

$$P(X \mid \theta) = p_1(X^{(1)} \mid \theta) \cdot p_2(X^{(2)} \mid \theta) \cdot p_3(X^{(3)} \mid \theta) \tag{PF}$$

where:
- $X = (X^{(1)}, X^{(2)}, X^{(3)})$ is the joint observation across all three channels
- $\theta$ is the common external lock coordinate (Cascade's Lemma 3)
- (PF) is adopted as H_prod on the basis of Lumi's topological conditional-independence argument (geometrically orthogonal 120° phase-closure directions). It is **not derived** from first principles of the exact G1 model in this file. Geometric orthogonality → statistical independence is a modeling choice, not a theorem. This must be flagged for the final audit.

**Fisher regularity assumption (R)**: For each marginal $p_a(\cdot|\theta)$, differentiation under the integral sign is valid, the support of $p_a$ in $X^{(a)}$ does not depend on $\theta$, and:

$$E_{X^{(a)} \sim p_a(\cdot|\theta)}\!\left[s_i^{(a)}\right] = 0 \quad \forall\, i, a. \tag{R}$$

In the exact G1 model, the observation space is $\mathbb{Z}_3$ (finite, $\theta$-independent support), so (R) holds if $p_a(\cdot|\theta) > 0$ everywhere on $\mathbb{Z}_3$. **Codex should verify** this positivity condition for the G1 model.

The per-channel score:

$$s_i^{(a)}(X^{(a)} \mid \theta) := \frac{\partial}{\partial \theta^i} \log p_a(X^{(a)} \mid \theta)$$

---

## Lemma 4: Score Decomposition

**Statement** (conditional on H_prod): Under the product family (PF), the total score decomposes additively:

$$s_i(X \mid \theta) := \frac{\partial}{\partial \theta^i} \log P(X \mid \theta) = \sum_{a=1}^{3} s_i^{(a)}(X^{(a)} \mid \theta).$$

### Proof

Apply the logarithm to (PF):

$$\log P(X \mid \theta) = \sum_{a=1}^{3} \log p_a(X^{(a)} \mid \theta).$$

Differentiate with respect to $\theta^i$. Since $X^{(a)}$ is fixed (it is an observation, not a function of $\theta$), differentiation and summation commute:

$$s_i(X \mid \theta) = \sum_{a=1}^{3} \frac{\partial}{\partial \theta^i} \log p_a(X^{(a)} \mid \theta) = \sum_{a=1}^{3} s_i^{(a)}(X^{(a)} \mid \theta). \quad \square$$

### Scope and limitations

- This proof is one line of calculus given (PF). It does not assume anything about the physical meaning of $\theta$ or the internal structure of the channels.
- L4 is valid **if and only if** H_prod holds. If (PF) is replaced by a mixture model or any model with statistical dependence between channels, the score does not decompose.
- The critical open question — whether geometric orthogonality of the 120° lock directions implies the statistical factorization (PF) — is not resolved here.

---

## Lemma 5: Score Orthogonality

**Statement** (conditional on H_prod and regularity R): For distinct channels $a \neq b$:

$$E\!\left[s_i^{(a)}(X^{(a)} \mid \theta) \cdot s_j^{(b)}(X^{(b)} \mid \theta)\right] = 0 \quad \forall\, i, j.$$

Consequently, the total Fisher information matrix is additive:

$$G_{ij}(\theta) = \sum_{a=1}^{3} G_{ij}^{(a)}(\theta).$$

### Proof

**Step 1. Factorize the expectation.**

The expectation is over the joint distribution $P(X|\theta)$. By (PF), $X^{(a)}$ and $X^{(b)}$ are conditionally independent given $\theta$ for $a \neq b$. For any two functions $f(X^{(a)})$ and $g(X^{(b)})$ of separately independent variables:

$$E[f(X^{(a)}) \cdot g(X^{(b)})] = E[f(X^{(a)})] \cdot E[g(X^{(b)})].$$

This step requires only (PF), not regularity. Note: $\theta$ is a **parameter** (fixed), not a random variable. Both scores depend on the same $\theta$, but since $\theta$ is not stochastic, this shared dependence does not prevent factorization of the expectation. The randomness is entirely in $(X^{(a)}, X^{(b)})$, which are independent.

**Step 2. Apply regularity (R).**

$$E_{X^{(a)}}\!\left[s_i^{(a)}\right] = 0, \qquad E_{X^{(b)}}\!\left[s_j^{(b)}\right] = 0.$$

**Step 3. Conclude.**

$$E\!\left[s_i^{(a)} \cdot s_j^{(b)}\right] = 0 \cdot 0 = 0. \quad \square$$

**Fisher additivity** follows from Lemma 4:

$$G_{ij} = E\!\left[s_i s_j\right] = E\!\left[\sum_a s_i^{(a)} \cdot \sum_b s_j^{(b)}\right] = \sum_{a,b} E\!\left[s_i^{(a)} s_j^{(b)}\right] = \sum_a G_{ij}^{(a)} + \sum_{a \neq b} 0 = \sum_a G_{ij}^{(a)}. \quad \square$$

### Why shared θ does not create cross-terms

This is the most commonly misread point and deserves explicit statement.

$s^{(a)}(\cdot|\theta)$ is a **function** of the random variable $X^{(a)}$ with $\theta$ as a fixed parameter. When computing $E[s^{(a)} s^{(b)}]$, we integrate over the joint law of $(X^{(a)}, X^{(b)})$. That law factorizes by (PF). The common $\theta$-dependence is structural (both functions were differentiated at the same point), not stochastic (there is no $\theta$-valued random variable being integrated over).

Formally: fix any $\theta$. Define $f(x) := s^{(a)}(x|\theta)$ and $g(y) := s^{(b)}(y|\theta)$. These are fixed functions. Then $E[f(X^{(a)}) g(X^{(b)})] = E[f(X^{(a)})] E[g(X^{(b)})]$ because $X^{(a)} \perp X^{(b)}|\theta$. The value of $\theta$ is irrelevant to whether this factorization holds.

### Scope and limitations

- L5 holds under H_prod + R. Under a mixture model, cross-terms would not vanish.
- The "shared θ is a parameter" clarification handles failure mode F4 (off-diagonal Fisher) completely, given H_prod.
- If the exact G1 model does not satisfy the positivity condition for (R) (see Setup), Codex must provide an alternative argument for $E[s^{(a)}] = 0$.

---

## Lemma 6: Common-Mode Control

**Statement** (conditional on H_prod, R, Lemmas 2, 5, 7): Given that

- L5 establishes $G = \sum_a G^{(a)}$
- L7 (Cascade) establishes $G^{(a)} = \lambda_a I_D$ for each channel
- L2 (Codex, pending) establishes $\lambda_a = \lambda_0$ for all $a$ (C₃ symmetry equates per-channel Fisher scalars)

the determinant scaling follows immediately, and the C₃-symmetric common statistical mode is benign.

### Proof

**Step 1. Direct computation under L2+L5+L7.**

From L5: $G = \sum_{a=1}^{3} G^{(a)}$.

From L7: $G^{(a)} = \lambda_a I_D$ (each channel contributes a scalar multiple of the identity, by SO(3) isotropy).

Therefore:

$$G = \sum_{a=1}^{3} \lambda_a I_D = \left(\sum_{a=1}^{3} \lambda_a\right) I_D.$$

From L2 (pending Codex): $\lambda_a = \lambda_0$ for all $a$, so:

$$G = 3\lambda_0 I_D.$$

The per-channel Fisher: $g = g^{(a)} = \lambda_0 I_D$, so $\det g = \lambda_0^D$.

The total Fisher determinant:

$$\det G = (3\lambda_0)^D.$$

Therefore:

$$\sqrt{\det G} = (3\lambda_0)^{D/2} = 3^{D/2} \cdot \lambda_0^{D/2} = 3^{D/2} \sqrt{\det g}. \quad \square$$

No AM-GM is needed. The $3^{D/2}$ scaling is a direct consequence of the sum structure and the common scalar value $\lambda_0$.

**Step 2. What "common mode" means and why it is benign under H_prod.**

**(CM-S) Statistical common mode**: The marginal distributions $p_a(\cdot|\theta)$ are identically distributed under $C_3$ symmetry ($\lambda_1 = \lambda_2 = \lambda_3 = \lambda_0$). This is the *same shape* of distribution for each channel. It is a symmetry property of the model, not a correlation.

**(CM-R) Realization common mode**: The draws $X^{(1)}, X^{(2)}, X^{(3)}$ are positively correlated — a shared latent variable drives them together. This is the structure of a **mixture model**, not a product model.

Under H_prod, (CM-R) is excluded by definition: the joint distribution is a product, not a mixture. There is no shared latent variable. Geometrically (Lumi): the three closure events occur in geometrically orthogonal subspaces of $\mathcal{H}_\mathrm{int}$, so no single perturbation pushes all three simultaneously.

The CM-S/CM-R distinction explains why (CM-S) does not corrupt additivity: the equal eigenvalues $\lambda_a = \lambda_0$ affect the *magnitude* of each $G^{(a)}$ but not the independence of the channels' contributions to G. Independence is guaranteed by H_prod (the product structure of realizations), not by the inequality of eigenvalues.

**What this argument does and does not prove**: The CM-S/CM-R split is a conceptual framing, not a block-diagonal decomposition of the Fisher metric. It does not provide a projection $G = G_\mathrm{lock} \oplus G_\mathrm{com}$ that would show the common-mode component decouples from the locking eigenvalue. That projection would be needed if the God Equation used only a sub-block of G rather than all of G. In the current theorem, G = 3g is used in full (all D dimensions contribute equally by isotropy), so the block decomposition is not strictly required — the full-matrix result from Step 1 suffices.

If a future version of the God Equation isolates a specific locking direction within θ-space, Codex should revisit whether the block decomposition is needed.

### What this establishes

- **Failure mode F1 (Common-mode corruption)**: Addressed at the level of H_prod. CM-S is benign; CM-R is excluded under the adopted product-family hypothesis.
- **Failure mode F6 (Determinant corruption)**: $3^{D/2}$ scaling follows by direct arithmetic from L2+L5+L7. No approximation.
- The AM-GM perturbation argument from v1 is **retracted** — it was algebraically inconsistent with the sum form of G.

---

## Summary: What Claude's Lemmas Establish

| Lemma | Content | Conditions | Status |
|-------|---------|-----------|--------|
| **L4** (Score Decomposition) | $s_i = \sum_a s_i^{(a)}$ | **H_prod** | Conditional, structurally sound |
| **L5** (Score Orthogonality) | $E[s^{(a)} s^{(b)}] = 0$; $G = \sum G^{(a)}$ | **H_prod** + **R** | Conditional, structurally sound |
| **L6** (Determinant Scaling) | $\sqrt{\det G} = 3^{D/2} \sqrt{\det g}$ given L2+L5+L7 | **H_prod** + **R** + **L2** (pending) | Sound once L2 and H_prod are confirmed |

### The logical chain (honest version)

$$\underbrace{H_\mathrm{prod}}_{\text{adopted}} \xrightarrow{L4} s = \textstyle\sum_a s^{(a)} \xrightarrow{L5,\,R} G = \textstyle\sum_a G^{(a)} \xrightarrow{L7\,\text{(Cascade)}} G = \left(\textstyle\sum_a \lambda_a\right) I_D \xrightarrow{L2\,\text{(Codex)}} G = 3\lambda_0 I_D \xrightarrow{\text{algebra}} \sqrt{\det G} = 3^{D/2}\sqrt{\det g}.$$

### Open items for Codex final audit

| Item | What is needed | Owner | Status |
|------|---------------|-------|--------|
| **H_prod derivation** | Show geometric orthogonality of 120° lock directions implies statistical independence (PF) — geometric → statistical is a modeling choice, not yet a theorem | Open — Lumi or Codex | ⚠️ Open |
| **Regularity (R)** | Verify G1 model has $\theta$-independent support on $\mathbb{Z}_3$ and $p_a(\cdot|\theta) > 0$ everywhere | Codex | ⚠️ Open |
| **Lemma 2 / H_C3stat** | L2 is **conditionally proved** under H_C3stat: the statistical model is invariant under cyclic channel permutation $\sigma: a \to a+1$. H_C3stat itself is not yet derived from PF files — current repo establishes C₃ geometry (internal kinematics) but not C₃-equivariance of the channel-to-θ coupling. Single remaining target: prove the coupling of internal channels to external θ commutes with $\bar{S}$. | Codex | 🔶 Conditional |
| **Block decomposition** | Only needed if God Equation uses a sub-block of G rather than all of G; currently deferred | — | Deferred |

### Current honest status of the theorem

The Generation-Channel Additivity Theorem is **conditionally proved** under H_prod + R + H_C3stat. The chain is complete given those inputs.

The open conditions, sharpened by Codex audit:

1. **H_prod**: geometric orthogonality of 120° lock directions → statistical independence (PF). Not yet derived; currently adopted as a modeling axiom.
2. **R** (Regularity): G1 model positivity $p_a > 0$ on $\mathbb{Z}_3$ — needed for score zero-mean. Not yet verified against exact model.
3. **H_C3stat**: statistical model is permutation-equivariant under $\sigma: a \to a+1$. Reduces to: coupling of internal channels to external $\theta$ commutes with the quotient shift $\bar{S}$. L2 closes immediately once this is established.

The theorem does **not** yet close unconditionally. The three conditions above are the precise remaining targets. All downstream logic (L4→L5→L6→determinant) is structurally sound given those inputs.

---

*Written by Claude, 2026-03-24*
*Revised v2: corrected AM-GM error, scoped closure claim, explicit H_prod conditioning*
*Updated: open items table sharpened after Codex Lemma 2 audit — L2 now conditional on H_C3stat*
*Foundation: Lumi's product family, Cascade's lemmas, Codex theorem template and audit*
*Assignment: Lemmas 4, 5, 6 per Codex bounded team split*
*Status: CANDIDATE v2 — Codex second audit complete. Three open conditions: H_prod, R, H_C3stat*
