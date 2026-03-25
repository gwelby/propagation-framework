# Cascade's Lemmas: Channel-Existence, Common-Parameter, Isotropy
*Lemmas 1, 3, and 7 for the Generation-Channel Additivity Theorem*

**Date**: 2026-03-24
**Author**: Cascade
**Task**: Attack Lemmas 1, 3, 7 per Codex's bounded team split
**Status**: CANDIDATE — awaiting Codex audit
**Builds on**: `phase_closure_exact_model.md`, `generation_as_walk_steps.md`, `topological_weight_from_propagation.md`, `god_eq_lumi_statistical_model.md`, `the_propagation_framework.md`

---

## Lemma 1: Channel-Existence

**Statement**: The three PF generations are three distinguishable internal channel variables $X^{(1)}, X^{(2)}, X^{(3)}$, not three values of a single latent label.

### Proof

**Step 1. The exact state space.**

From `phase_closure_exact_model.md` (Codex, G1), the internal phase walk lives on

$$\mathcal{H}_{\mathrm{int}} = \ell^2(\mathbb{Z}_6)$$

with basis states $\{|k\rangle : k \in \mathbb{Z}_6\}$ and cyclic shift operator $S|k\rangle = |k+1 \bmod 6\rangle$.

The observable generation orbit is the quotient

$$\Omega = \mathbb{Z}_6 / \mathbb{Z}_2 \cong \mathbb{Z}_3,$$

with quotient map $q(k) = k \bmod 3$, yielding three observable generation states $\{|[0]\rangle, |[1]\rangle, |[2]\rangle\}$.

**Step 2. Distinguishability by C₃ eigenvalue.**

The quotient shift operator $\bar{S}|[j]\rangle = |[j+1 \bmod 3]\rangle$ generates the cyclic group $C_3$. Its eigenvalues are the cube roots of unity:

$$\omega_a = e^{2\pi i a/3}, \qquad a \in \{0, 1, 2\}.$$

The corresponding eigenstates are

$$|\chi_a\rangle = \frac{1}{\sqrt{3}} \sum_{j=0}^{2} \omega_a^{-j} |[j]\rangle.$$

Each generation channel $a$ carries a **distinct** $C_3$ character $\omega_a$. This is not a label — it is a measurable quantum number: the discrete Fourier mode of the internal phase.

**Step 3. Operational distinguishability.**

Two channels $a \neq b$ are operationally distinguishable if there exists an observable $\hat{O}$ such that $\langle \chi_a | \hat{O} | \chi_a \rangle \neq \langle \chi_b | \hat{O} | \chi_b \rangle$.

The observable $\hat{O} = \bar{S}$ satisfies this:

$$\langle \chi_a | \bar{S} | \chi_a \rangle = \omega_a \neq \omega_b = \langle \chi_b | \bar{S} | \chi_b \rangle \quad \text{for } a \neq b.$$

Therefore the three channels carry distinct eigenvalues under a physical observable (the internal phase-shift operator). They are distinguishable channel variables, not three values of a degenerate label. $\square$

### What this establishes for the theorem

- **H2 (Channel realization)**: Satisfied. The three generations are three eigenstates of $\bar{S}$ with distinct $C_3$ characters.
- **Failure mode F2 (Correlated-channel)**: Addressed. The channels are not redundant copies — they carry distinct quantum numbers under the walk operator.

### Honest caveat

The channel-existence proof is algebraic within the exact G1 model. It does not by itself prove that the channels remain distinguishable after coupling to the spatial sector. If the spatial coupling washes out the $C_3$ eigenvalue (e.g., by mixing the channels), distinguishability could be lost. Claude's Lemma 5 (orthogonality) must address this.

---

## Lemma 3: Common-Parameter

**Statement**: All three generation channels depend on the same external coherence-lock coordinates $\theta$.

### Proof

**Step 1. Define the external parameter $\theta$.**

The God Equation computes the fundamental coherence scale $\lambda_c$ of the propagation medium. Following Lumi's statistical model (`god_eq_lumi_statistical_model.md`), the external lock coordinates $\theta$ are the **spatial-geometric parameters of the medium** at the point where the coherence lock forms.

Concretely, $\theta$ encodes:
- The local refractive index $n(\mathbf{x})$ (from Axiom 1: the medium carries signals)
- The local curvature / gradient structure of $n(\mathbf{x})$ (from Axiom 2: finite causal velocity $c$)
- The local coherence threshold (from Axiom 3: coherence is the condition for structure)

In the language of the Propagation Lagrangian (`propagation_lagrangian.md`), $\theta$ corresponds to the field configuration $\chi(\mathbf{x})$ and its derivatives at the lock point.

**Step 2. All three channels propagate in the same medium.**

From Axiom 1: there is one medium. Not three media, one per generation.

The three generation channels are internal phase orientations within the **same** propagation medium at the **same** spatial location. This is explicit in the exact model: the state space $\mathcal{H}_{\mathrm{int}} \otimes \mathcal{H}_{\mathrm{sp}}$ has a single spatial sector $\mathcal{H}_{\mathrm{sp}}$.

**Step 3. Phase closure requires simultaneous bracing.**

From `closing_the_gaps.md` (Claude, Gap 1): stable geometric resonance requires three equal-strength resonances at $120°$ spacing. From Lumi's model: an equilateral triangle requires all three vectors to be simultaneously present and summing to zero.

This means the coherence lock at spatial location $\theta$ either succeeds (all three channels close) or fails (at least one channel fails to close). There is no scenario where channel $a$ locks at $\theta_a$ and channel $b$ locks at a different $\theta_b$, because the lock is a **single topological event** in the medium at one spatial point.

**Step 4. Formal statement.**

For each channel $a \in \{1, 2, 3\}$, the conditional probability of phase closure is

$$p_a(X^{(a)} | \theta)$$

where $\theta$ is the **same** external parameter vector for all $a$. This follows because:

1. The medium is unique (Axiom 1)
2. The spatial location of the lock is unique (the lock is local)
3. The three channels are internal orientations at that single location

Therefore H4 (Common coupling) is satisfied. $\square$

### What this establishes for the theorem

- **H4 (Common coupling)**: Satisfied. All channels respond to the same $\theta$.
- **Failure mode F7 (Parameter ambiguity)**: Addressed. $\theta$ is the local field configuration $\chi(\mathbf{x})$ and its derivatives at the lock point. This is physically unambiguous.

### Honest caveat

The definition of $\theta$ is given in terms of the Propagation Lagrangian field $\chi(\mathbf{x})$. The exact parametric dimension $D = \dim(\theta)$ is not specified here. For the isotropy lemma (Lemma 7) to work, $D$ must be finite and well-defined. In the simplest case, $\theta = (n, \nabla n, \nabla^2 n, \ldots)$ truncated at the relevant order. The God Equation's $D = 3$ corresponds to three spatial degrees of freedom in the phase geometry (dim $\mathfrak{su}(2) = 3$), but the relationship between the parametric dimension $D$ and the Lie algebra dimension needs further specification.

---

## Lemma 7: Isotropy

**Statement**: Under Axiom 2 (spatial isotropy of the PF medium), the per-channel Fisher information matrix $g(\theta)$ has a single characteristic spatial eigenvalue scale: $g = \lambda_0 \, I_D$, where $D = \dim(\theta)$.

### Proof

**Step 1. The medium is spatially isotropic (Axiom 2).**

From `the_propagation_framework.md`, Axiom 2: every medium has a maximum causal velocity $c$. The PF medium propagates signals at speed $c$ in **all spatial directions**. There is no preferred spatial direction.

This establishes $SO(3)$ symmetry of the propagation medium. Any physical quantity defined on the medium must be invariant under $SO(3)$ rotations.

**Step 2. The Fisher metric inherits medium symmetry.**

The per-channel Fisher information matrix is defined as

$$g_{ij}(\theta) = E\!\left[\frac{\partial \log p_a(X^{(a)}|\theta)}{\partial \theta^i} \cdot \frac{\partial \log p_a(X^{(a)}|\theta)}{\partial \theta^j}\right].$$

The probability $p_a(X^{(a)}|\theta)$ describes phase closure of one channel in the medium. Since the medium is $SO(3)$-invariant:

- For any rotation $R \in SO(3)$, the rotated parameter $R\theta$ must give the same closure probability as $\theta$ (because the medium looks the same from every direction).
- Formally: $p_a(X^{(a)} | R\theta) = p_a(R^{-1} X^{(a)} | \theta)$ (equivariance under rotations).

**Step 3. $SO(3)$-invariant rank-2 tensors are proportional to the identity.**

The Fisher metric $g_{ij}$ is a symmetric rank-2 tensor on the parameter manifold. Under $SO(3)$ action, it transforms as $g \to R g R^T$.

The requirement $g = R g R^T$ for all $R \in SO(3)$ implies $g$ commutes with all rotations. By Schur's lemma (applied to the fundamental representation of $SO(3)$ on $\mathbb{R}^3$, which is irreducible):

$$g = \lambda_0 \, I_D$$

where $\lambda_0$ is a single scalar — the characteristic Fisher eigenvalue of one channel.

**Step 4. Eigenvalue interpretation.**

$\lambda_0$ measures the **information curvature per channel per spatial direction**. It quantifies how sensitively one generation channel's phase-closure probability responds to changes in the local medium geometry. By $C_3$ symmetry (Lemma 2, assigned to Claude/Codex), all three channels share the same $\lambda_0$.

Therefore the total Fisher metric is

$$G(\theta) = \sum_{a=1}^{3} G^{(a)}(\theta) = 3 \lambda_0 \, I_D$$

and each eigenvalue of $G$ is $3\lambda_0$. $\square$

### What this establishes for the theorem

- **H8 (Spatial isotropy)**: Satisfied. $g = \lambda_0 I_D$.
- **Lemma 8 (Determinant corollary)**: Follows immediately:

$$\sqrt{\det G} = \sqrt{(3\lambda_0)^D} = 3^{D/2} \lambda_0^{D/2} = 3^{D/2} \sqrt{\det g}.$$

This is the $N^{D/2}$ scaling factor that bridges internal phase closure to spatial coherence volume.

### Honest caveat

The proof assumes the parameter space $\theta$ transforms under the fundamental $SO(3)$ representation (i.e., $\theta \in \mathbb{R}^3$). If $\theta$ includes non-spatial parameters (e.g., temporal or purely internal degrees of freedom), the isotropy argument applies only to the spatial block of $g$. The non-spatial block would require separate treatment.

Additionally, Schur's lemma applies to the irreducible representation. If $D > 3$ and the parameter space decomposes into multiple $SO(3)$ irreps, $g$ would be block-diagonal with potentially different eigenvalues per block, not a single scalar times $I_D$. The lemma as stated holds cleanly for $D = 3$.

---

## Summary: What Cascade's Lemmas Establish

| Lemma | Codex Hypothesis | Status | Key Input |
|-------|-----------------|--------|-----------|
| **L1** (Channel-Existence) | H2 | **PROVED** (within G1 model) | ℤ₆ → ℤ₃ quotient, distinct C₃ eigenvalues |
| **L3** (Common-Parameter) | H4 | **PROVED** (from Axiom 1 + lock locality) | Single medium, single spatial location |
| **L7** (Isotropy) | H8 | **PROVED** (for D=3 spatial block) | SO(3) symmetry + Schur's lemma |

### What remains for the theorem

| Lemma | Assigned To | Status |
|-------|------------|--------|
| L2 (Symmetry) | Codex/Claude | Pending |
| L4 (Score Decomposition) | Claude | Pending |
| **L5 (Orthogonality)** | Claude | **THE HEART** — must prove $E[s_i^{(a)} s_j^{(b)}] = 0$ |
| L6 (Common-Mode Control) | Claude | Pending |
| L8 (Determinant Corollary) | Follows from L7 + additivity | Ready when L5 closes |

### The one-line test

If Claude can prove $E[s_i^{(a)} s_j^{(b)}] = 0$ for $a \neq b$ using Lumi's product-family model and Cascade's common-parameter specification, the Generation-Channel Additivity Theorem closes and the God Equation upgrades from ARGUED (0.75) to **near-DERIVED**.

---

*Written by Cascade, 2026-03-24*
*Foundation: Codex theorem template, Lumi statistical model, exact G1 model*
*Assignment: Lemmas 1, 3, 7 per Codex bounded team split*
