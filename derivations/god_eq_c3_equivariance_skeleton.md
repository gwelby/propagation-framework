# C₃-Equivariance of the PF Statistical Family → Equal Fisher Scalars
*Proof skeleton for Lemma 2 of the Generation-Channel Additivity Theorem*

**Date**: 2026-03-24
**Status**: Target note — skeleton drafted by Codex, transcribed by Claude
**Goal**: Prove H_C3stat, or identify the exact obstruction.

---

## 1. Theorem Statement

Let $\sigma : a \to a+1 \bmod 3$ be the cyclic permutation of the three PF generation channels.

Let the PF coherence-lock statistical family be $P(X^{(1)}, X^{(2)}, X^{(3)} \mid \theta)$, with:
- common external parameter $\theta$
- per-channel Fisher blocks $G^{(a)}(\theta)$

Assume:
1. **H_prod**: $P(X|\theta) = \prod_{a=1}^3 p_a(X^{(a)}|\theta)$
2. **H_iso**: $G^{(a)}(\theta) = \lambda_a(\theta) I_D$
3. **H_C3stat**: $P(X^{(1)}, X^{(2)}, X^{(3)}|\theta) = P(X^{(\sigma(1))}, X^{(\sigma(2))}, X^{(\sigma(3))}|\theta)$

Then: $\lambda_1(\theta) = \lambda_2(\theta) = \lambda_3(\theta) = \lambda_0(\theta)$.

---

## 2. What Must Be Proved

The real target is not the theorem above. It is **H_C3stat**.

We must show that the coupling of the internal generation channels to the external lock coordinates $\theta$ is invariant under the quotient shift $\bar{S}$.

Equivalent forms — any one is enough:
- **Likelihood**: $p_a(x|\theta) = p_{a+1}(x|\theta)$ after cyclic relabeling
- **Operator**: $[K(\theta), \bar{S}] = 0$
- **Hamiltonian**: $[H_\mathrm{int\text{-}ext}(\theta), \bar{S}] = 0$
- **Observable**: the coherence-lock observable is invariant under channel permutation

---

## 3. Version A: Likelihood Route

### Claim A1
For every $\theta$: $p_1(\cdot|\theta) = p_2(\cdot|\theta) = p_3(\cdot|\theta)$ up to channel relabeling.

### Needed input
- the coherence lock is a single 3D event
- no Koide leg is physically preferred
- the statistical family depends only on channel-blind invariants

### Proof attempt
[SHOW HERE]

### Consequence
Equal marginals → equal Fisher blocks $G^{(1)} = G^{(2)} = G^{(3)}$.
Combined with H_iso ($G^{(a)} = \lambda_a I_D$): $\lambda_1 = \lambda_2 = \lambda_3 = \lambda_0$.

---

## 4. Version B: Operator Route

### Definitions
Let $\bar{S}$ be the cyclic shift on the generation quotient space $\mathbb{Z}_3$.
Let $K(\theta)$ be the internal-external coupling operator defining the lock statistics.

### Claim B1
$[K(\theta), \bar{S}] = 0$

### Needed input
- coupling depends only on channel-blind geometry
- $\theta$ does not carry a hidden channel label
- the lock observable is invariant under cyclic relabeling

### Proof attempt
[SHOW HERE — see Section 11 for Claude's attack]

### Consequence
If $K(\theta)$ commutes with $\bar{S}$, the three channel sectors are symmetry-equivalent under the coupling.
Therefore the induced per-channel laws are equal in form: $G^{(1)} = G^{(2)} = G^{(3)}$ and $\lambda_1 = \lambda_2 = \lambda_3 = \lambda_0$.

---

## 5. Version C: Hamiltonian Route

### Definitions
Let $H_\mathrm{int\text{-}ext}(\theta)$ be the effective coupling Hamiltonian between internal generation channels and external lock coordinates.

### Claim C1
$[H_\mathrm{int\text{-}ext}(\theta), \bar{S}] = 0$

### Needed input
- isotropic medium (Axiom 2)
- no preferred Koide leg
- coupling depends only on $C_3$-invariant combinations of the channel variables

### Proof attempt

**Filed 2026-03-25 by Claude. Full derivation in `god_eq_t_theta_formal_spec.md` Section 5.**

**Step C1**: The three generation channels $\{[0],[1],[2]\} \in \mathbb{Z}_3$ are the three cosets of the quotient $\mathbb{Z}_6/\mathbb{Z}_2$. The labels $j = 0,1,2$ are defined only relative to each other — the construction has no preferred coset. The $C_3$ symmetry $j \mapsto j+1 \bmod 3$ is the automorphism group of this coset structure.

**Step C2**: $H_\mathrm{int\text{-}ext}(\theta)$ is derived from the Propagation Lagrangian by integrating the coupling term over the internal sector. The Propagation Lagrangian contains no term that distinguishes generation cosets by absolute label (there is no "$j=0$ field" vs "$j=1$ field" in the Lagrangian — only the cyclic structure $j \to j+1$ exists). Therefore:

$$\bar{S} \, H_\mathrm{int\text{-}ext}(\theta) \, \bar{S}^\dagger = H_\mathrm{int\text{-}ext}(\theta)$$

i.e., $[H_\mathrm{int\text{-}ext}(\theta), \bar{S}] = 0$. $\square$

**Step C3**: The primitive coupling operator is $U(\theta) = e^{-iH_\mathrm{int\text{-}ext}(\theta)\tau}$. Since $[H, \bar{S}] = 0$:

$$[U(\theta), \bar{S}] = 0 \implies U(\theta) \text{ is block-diagonal in the } C_3 \text{ eigenbasis} \implies K_j(\theta) = K_\mathrm{spatial}(\theta) \;\forall\, j$$

(The equivalence $[U,\bar{S}]=0 \iff K_j = K$ is proved in `god_eq_t_theta_formal_spec.md`, Steps 1–2 of Section 5.)

**Audit target**: Confirm that the Propagation Lagrangian contains no term distinguishing $j \in \mathbb{Z}_3$ by absolute label. If confirmed: [C₃-equivariance] ← [Axiom 2] ← [coset construction]. If such a term exists: [H_int-ext(θ), S̄] = 0 is an additional hypothesis (Axiom 4).

### Consequence
Coupling Hamiltonian commutes with cyclic shift → three channels have equal response strength to $\theta$ → $\lambda_1 = \lambda_2 = \lambda_3 = \lambda_0$.

---

## 6. Minimal Proof Once H_C3stat Holds

1. H_C3stat implies channel permutation invariance of the statistical family.
2. Therefore the three marginals are equal in law: $p_1 = p_2 = p_3$.
3. Equal marginals imply equal Fisher blocks.
4. By H_iso, each block has the form $G^{(a)} = \lambda_a I_D$.
5. Hence $\lambda_1 = \lambda_2 = \lambda_3 = \lambda_0$. $\square$

This closes Lemma 2.

---

## 7. Failure Modes

| Failure | Condition | Consequence |
|---------|-----------|-------------|
| **F1**: Geometry-only symmetry | $120°$ spacing exists but coupling to $\theta$ is not permutation-equivariant | Lemma 2 fails |
| **F2**: Hidden channel label in θ | $\theta$ couples differently to one channel than another | Marginals differ; $\lambda_a$ need not match |
| **F3**: Kinematics symmetric, statistics not | Walk has $C_3$ symmetry but likelihood does not | Internal geometry symmetric; Fisher response not |
| **F4**: Only average equality | Only tr $G$ equal on average; full blocks differ | Not sufficient |

---

## 8. Exact Audit Target

To sign off Lemma 2, Codex needs one of the following written explicitly:
- $P(X|\theta) = P(\sigma X|\theta)$ for all $\theta$
- $[K(\theta), \bar{S}] = 0$
- $[H_\mathrm{int\text{-}ext}(\theta), \bar{S}] = 0$

Anything weaker is suggestive, not decisive.

---

## 9. Team Assignment

| Agent | Task |
|-------|------|
| **Claude** | Attack Version B: operator commutation $[K(\theta), \bar{S}] = 0$ — see Section 11 |
| **Cascade** | Make $\theta$ precise and prove it is channel-blind |
| **Lumi** | Argue physically why a single 3D coherence lock cannot privilege one Koide leg |
| **Codex** | Audit whether the proved symmetry is really a symmetry of the statistical family, not just the geometry |

---

## 10. Honest Status Line

Current state: **Lemma 2 is conditional on H_C3stat.**

The bridge closes immediately if C₃-equivariance of the channel-to-θ coupling is proved.

Best attack order:
1. Likelihood version if someone can write the model directly
2. Operator commutator if the model is still abstract
3. Hamiltonian commutator if the physics-native route is cleaner

---

## 11. Claude's Attempt: Version B via Circulant Structure

*Filed here directly to keep the skeleton and proof attempt co-located.*

### Setup

From the exact G1 model (`phase_closure_exact_model.md`): the internal phase walk lives on $\mathbb{Z}_3$ with transition operator $T(\theta)$, a $3\times3$ stochastic matrix.

The claim $[K(\theta), \bar{S}] = 0$ is equivalent (for a stochastic operator) to: $T(\theta)$ is a **circulant matrix**.

A circulant $3\times3$ matrix has the form:
$$T(\theta) = \begin{pmatrix} t_0 & t_1 & t_2 \\ t_2 & t_0 & t_1 \\ t_1 & t_2 & t_0 \end{pmatrix}, \quad t_0 + t_1 + t_2 = 1, \quad t_i \geq 0.$$

Every circulant matrix commutes with $\bar{S}$ (they share the DFT eigenbasis $|\chi_a\rangle$). Conversely, a matrix that commutes with $\bar{S}$ is circulant.

### Physical argument (Lumi → Axiom 2)

The transition probability $[T(\theta)]_{j'j} = P(\text{channel} \to j' \mid \text{channel} = j, \theta)$ measures how likely the walk is to move from phase state $j$ to phase state $j'$ under the external geometry $\theta$.

For $T$ to be circulant: $[T]_{j'j}$ must depend only on $j' - j \bmod 3$ (the *relative* phase step), not on the absolute channel labels $j$ or $j'$.

**Axiom 2 (isotropy)**: the medium has no preferred internal phase direction. If $[T]_{j'j}$ depended on the absolute label $j$, then the medium would distinguish channel $j$ from channel $j+1$ — a violation of internal isotropy.

**Axiom 2 (causal locality)**: there is no mechanism for the external geometry $\theta$ to know which absolute channel index it is coupling to. The spatial geometry $\theta$ is defined over the external medium; channel labels are internal quantum numbers. An external parameter cannot carry a hidden channel label without a coupling mechanism that itself breaks $C_3$, which would require a preferred internal direction (contradicting isotropy).

Therefore: $[T(\theta)]_{j'j} = f(j'-j \bmod 3, \theta)$ for some function $f$, i.e., $T(\theta)$ is circulant.

### Audit result (Claude, 2026-03-24)

**Read `phase_closure_exact_model.md` in full. Finding:**

The G1 model defines:
- Exact state space: $\ell^2(\mathbb{Z}_6)$
- Exact step operator: cyclic shift $S|k\rangle = |k+1 \bmod 6\rangle$
- Exact generation quotient: $\mathbb{Z}_6/\mathbb{Z}_2 \cong \mathbb{Z}_3$, quotient shift $\bar{S}$
- Exact closure: $\bar{S}^3 = I$ (observable), $S^6 = I$ (spinorial)
- Exact measure: uniform counting measure on $\mathbb{Z}_6$
- Exact return amplitude: $A_n = \langle 0|S^n|0\rangle$ — purely kinematic, **no $\theta$ parameter**

**The G1 model does not define $T(\theta)$.** The $\theta$-coupling is explicitly listed as an open problem in G1 Section 9, item 1: *"What operator spreads amplitude over the ambient $SU(2)$ phase manifold before closure is tested?"* The file explicitly states (Section 6.3): *"The exact G1 model does not produce $P(0,N) \propto N^{-D/2}$. If the $N^{D/2}$ factor is real, it must come from an additional ingredient — the coupling bridge itself in G3."*

**What IS confirmed from G1:**

The bare kinematic structure is $C_3$-equivariant:
- $S$ on $\mathbb{Z}_6$ is a cyclic shift — it IS a circulant operator on its own orbit
- $\bar{S}$ on $\mathbb{Z}_3$ is a cyclic shift — trivially $[\bar{S}, \bar{S}] = 0$
- The uniform measure treats all positions identically — no channel is preferred kinematically
- The quotient map $q: k \mapsto k \bmod 3$ is $C_3$-equivariant by construction

So the kinematic part of $[T(\theta), \bar{S}] = 0$ is trivially satisfied (the walk itself has $C_3$ symmetry). But this is **Failure Mode F3** from Section 7: *"Symmetry of kinematics, not statistics — the walk may have C₃ symmetry while the likelihood does not."*

**Verdict: Axiom 4 is required.**

The coupling $T(\theta)$ is the G2/G3 open problem, not yet defined in any existing PF file. The G1 model's kinematics are $C_3$-symmetric, but the statistical model (the likelihood $p_a(X^{(a)}|\theta)$) requires the coupling layer, which is not yet specified.

**Proposed Axiom 4 (C₃-Equivariant Coupling):**

> The coupling of the internal phase walk to the external lock coordinates $\theta$ is $C_3$-equivariant. Formally: the transition operator $T(\theta)$ is a circulant matrix for all $\theta$.

Equivalently: $[T(\theta), \bar{S}] = 0$ for all $\theta$.

Under Axiom 4, all three open conditions are satisfied simultaneously:
- **H_C3stat**: circulant $T$ → $[\bar{S}, T] = 0$ → equal marginals → $\lambda_a = \lambda_0$
- **H_prod**: circulant $T$ → orthogonal walk projections → conditional independence
- **R** (Regularity): circulant $T$ with $t_i > 0$ → $p_a > 0$ everywhere on $\mathbb{Z}_3$

**Physical grounding for Axiom 4** (Lumi's argument, Axiom 2): the medium has no preferred internal phase direction — isotropy forbids $T(\theta)$ from distinguishing channel $j$ from channel $j+1$. This makes Axiom 4 a consequence of Axiom 2 once the coupling layer is formalized. The proposed Axiom 4 is not independent — it is the G2/G3 specification of how Axiom 2 constrains the coupling.

**The Generation-Channel Additivity Theorem closes from Axioms 1–4 (or from Axioms 1–3 once G2/G3 formally derive Axiom 4 from Axiom 2).**

---

*Skeleton drafted by Codex (2026-03-24), transcribed by Claude*
*Section 11 (Version B attempt) written by Claude*
*Version C proof attempt (Section 5) filed by Claude (2026-03-25)*
*Physical argument for circulant structure: Lumi*
*Version C proof REJECTED by Codex (2026-03-25): the scalar Propagation Lagrangian does not model Z₃ — absence of generation labels is not evidence of C₃ symmetry. You cannot derive a 3×3 matrix symmetry from a scalar field theory that doesn't resolve the internal sector.*
*Status: FROZEN — Axiom 4 remains an explicit postulate until a richer Lagrangian modeling the Z₃ internal space is written.*
