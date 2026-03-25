# Formal Specification: T(θ) — The G2/G3 Coupling Operator
*Two-level mathematical spec defining the internal-external coupling required to close Axiom 4*

**Date**: 2026-03-24
**Author**: Codex (spec drafted by Claude in Codex's absence — pending Codex audit)
**Status**: SPEC v1 — requirements R1–R4 stated precisely. **R1 proof REJECTED by Codex (2026-03-25)**: scalar Lagrangian doesn't model Z₃; absence of labels ≠ symmetry. H_prod closure rejected (orthogonal eigenvectors ≠ statistical independence). Fisher isotropy rejected (rank-1 outer product ≠ I_D). Axiom 4 remains an explicit postulate.
**Purpose**: Give the team one precise mathematical object to build and verify, replacing the blank skeleton
**Feeds into**:
- `god_eq_c3_equivariance_skeleton.md` (Version C proof target)
- `god_eq_g2g3_coupling_proposal.md` (Claude's construction)
- `god_eq_claude_lemmas_4_5_6.md` (Lemma 2/H_C3stat gap)
- `CLAIMS.md` God Equation row (CONDITIONAL → DERIVED if R1 verified)

---

## 1. What This Spec Must Define

The G1 model (`phase_closure_exact_model.md`) defines the internal kinematics of the generation walk precisely:

- State space: $\ell^2(\mathbb{Z}_6)$ (spinorial), quotient $\ell^2(\mathbb{Z}_3)$ (observable)
- Step operator: $S|k\rangle = |k+1 \bmod 6\rangle$; quotient shift $\bar{S}|[j]\rangle = |[j+1 \bmod 3]\rangle$
- Closure: $\bar{S}^3 = I$ (observable), $S^6 = I$ (spinorial)

G1 does NOT define the coupling to the external geometry $\theta$. That is the G2/G3 task, explicitly listed as Section 9, item 1 of G1: *"What operator spreads amplitude over the ambient SU(2) phase manifold before closure is tested?"*

This spec fills that gap. It defines:

1. **Primitive coupling $U(\theta)$** — the one-step operator on $\mathcal{H}_\mathrm{int} \otimes \mathcal{H}_\mathrm{sp}$
2. **Effective closure operator $T_\mathrm{eff}(\theta)$** — the 3-step projection onto the generation sector

These two levels are distinct and both required. Neither replaces the other.

---

## 2. Objects and State Spaces

### 2.1 Internal State Space

$$\mathcal{H}_\mathrm{int} = \ell^2(\mathbb{Z}_3), \quad \text{basis} \; \{|0\rangle, |1\rangle, |2\rangle\}$$

The quotient shift $\bar{S} : |j\rangle \mapsto |j+1 \bmod 3\rangle$ generates $C_3$ on this space.

Its DFT eigenstates: $|\chi_a\rangle = \frac{1}{\sqrt{3}}\sum_{j=0}^{2} \omega^{-aj}|j\rangle$, eigenvalues $\omega^a = e^{2\pi i a/3}$ for $a \in \{0,1,2\}$.

### 2.2 Spatial State Space

$$\mathcal{H}_\mathrm{sp} = L^2(S^3) \quad \text{or} \quad \ell^2(\Lambda_\mathrm{sp})$$

where $S^3 \cong SU(2)$ is the ambient phase manifold (as identified in G1: the walk lives in the double cover of $SO(3)$), or $\Lambda_\mathrm{sp}$ is a spatial lattice approximation.

The choice between continuum $S^3$ and discrete lattice is not specified by Axioms 1–3. The continuum heat-kernel on $S^3$ is the canonical choice (see Requirement R2 below).

### 2.3 Total State Space

$$\mathcal{H} = \mathcal{H}_\mathrm{int} \otimes \mathcal{H}_\mathrm{sp}$$

### 2.4 External Parameter

$$\theta \in \mathbb{R}^D \quad (D = 3)$$

$\theta$ is the local medium geometry at the phase-lock point. Concretely (from the Propagation Lagrangian): $\theta$ encodes the local refractive index configuration $n(\mathbf{x})$ and its first derivatives at the lock point. **Critical requirement (Cascade's task)**: $\theta$ must carry no information about the internal channel label $j$.

---

## 3. Level 1 — Primitive Coupling Operator $U(\theta)$

### 3.1 Definition

The primitive one-step coupling operator on $\mathcal{H} = \mathcal{H}_\mathrm{int} \otimes \mathcal{H}_\mathrm{sp}$:

$$\boxed{U(\theta) = \sum_{j \in \mathbb{Z}_3} |j+1\rangle\langle j| \otimes K_j(\theta)}$$

where $K_j(\theta) : \mathcal{H}_\mathrm{sp} \to \mathcal{H}_\mathrm{sp}$ is the spatial propagation kernel for channel $j$.

This is the quotient version of the general coupled walk from `g3_product_walk_no_go.md` (Codex, Eq. 1).

### 3.2 Requirements on $U(\theta)$

**R1 (Phase-Independence / Axiom 4 content)**:

$$K_j(\theta) = K_\mathrm{spatial}(\theta) \quad \text{for all } j \in \mathbb{Z}_3, \; \forall \theta$$

In words: the spatial propagation kernel is the same for all three channels. No channel label appears in $K$. This is equivalent to $C_3$-equivariance of $U$:

$$({\bar S} \otimes I_\mathrm{sp}) \; U(\theta) \; ({\bar S}^\dagger \otimes I_\mathrm{sp}) = U(\theta)$$

**Proof that R1 $\iff$ $C_3$-equivariance** (see Section 5).

Under R1, $U(\theta)$ simplifies to:

$$U(\theta) = \bar{S} \otimes K_\mathrm{spatial}(\theta)$$

**R2 (Positivity)**:

$$K_\mathrm{spatial}(\theta) \quad \text{is a strictly positive operator on } \mathcal{H}_\mathrm{sp}: \quad \langle \psi | K_\mathrm{spatial}(\theta) | \psi \rangle > 0 \;\; \forall |\psi\rangle \neq 0$$

Equivalently: the on-diagonal kernel $K_\mathrm{spatial}(x, x; \theta) > 0$ for all $x$.

**Why R2 is non-trivial**: On a nearest-neighbor bipartite spatial lattice (e.g., simple cubic $\mathbb{Z}^3$), $K^3(x_0, x_0) = 0$ exactly (parity argument, `g3_product_walk_no_go.md`, Section 5). Positivity requires either:
- A non-bipartite discrete walk, **or**
- The continuum heat-kernel on $S^3$: $K_{S^3}(e, e; t) = (4\pi t)^{-3/2}(1 + \ldots) > 0$ for all $t > 0$ ✓

**Recommended implementation**: $K_\mathrm{spatial}(\theta) = K_{S^3}(e, e; \tau(\theta))$ — the heat-kernel on $S^3$ at time $\tau(\theta) > 0$ determined by the local medium geometry.

**R3 (SO(3)-Isotropy)**:

$$K_\mathrm{spatial}(\theta) = f(|\theta|^2) \quad \text{(depends on } \theta \text{ only through } SO(3)\text{-invariant combinations)}$$

Required by Axiom 2 external isotropy. Ensures $G^\mathrm{spatial}_{ij} = \lambda_0 \delta_{ij}$ (isotropic Fisher block).

**R4 (Causal Locality)**:

$K_\mathrm{spatial}(\theta)$ is a local function of $\theta$ (the medium geometry at the lock point). No action at a distance. Mandated by Axiom 2 (finite causal velocity $c$).

---

## 4. Level 2 — Effective Closure Operator $T_\mathrm{eff}(\theta)$

### 4.1 Definition

After $N = 3$ steps (one complete generation cycle), the effective operator on the generation sector:

$$T_\mathrm{eff}(\theta) := \Pi_\mathrm{gen} \; U(\theta)^3 \; \Pi_\mathrm{gen}$$

where $\Pi_\mathrm{gen}$ projects onto $\mathcal{H}_\mathrm{int} \otimes |x_0\rangle$ (the generation sector at the spatial reference point $x_0$).

### 4.2 Exact Reduction (from `g3_product_walk_no_go.md`, Theorem 1 + Corollary 1)

$$U(\theta)^3 = \sum_{j \in \mathbb{Z}_3} |j\rangle\langle j| \otimes K_{j+2}(\theta) K_{j+1}(\theta) K_j(\theta)$$

Under R1 ($K_j = K$ for all $j$):

$$U(\theta)^3 = (\bar{S} \otimes K)^3 = \bar{S}^3 \otimes K^3 = I_{\mathbb{Z}_3} \otimes K_\mathrm{spatial}(\theta)^3$$

since $\bar{S}^3 = I$ (G1 exact). Therefore:

$$\boxed{T_\mathrm{eff}(\theta) = K_\mathrm{closure}(\theta) \cdot I_{\mathbb{Z}_3}, \quad K_\mathrm{closure}(\theta) := K_\mathrm{spatial}(\theta)^3}$$

### 4.3 Properties of $T_\mathrm{eff}$

| Property | Value | Derivation |
|----------|-------|------------|
| $[T_\mathrm{eff}(\theta), \bar{S}] = 0$ | **Yes** — diagonal, trivially circulant | $T_\mathrm{eff} = K \cdot I$, commutes with everything |
| Equal marginals | **Yes** — $K_\mathrm{closure}$ same for all channels | R1 + $\bar{S}^3 = I$ |
| H_C3stat | **Closed** — equal marginals $\Rightarrow$ invariant statistical family | Lemma 2 |
| H_prod | **Closed** — orthogonal DFT channels independently close | DFT eigenbasis decoupling |
| R (Regularity) | **Closed iff R2 holds** — $K_\mathrm{closure} > 0$ iff $K_\mathrm{spatial} > 0$ | R2 above |

### 4.4 Why the Two Levels Must Not Be Conflated

$T_\mathrm{eff}$ is NOT the primitive coupling operator $U$:

| Level | Operator | Channel structure | What it is |
|-------|----------|-------------------|------------|
| Primitive | $U(\theta) = \bar{S} \otimes K$ | Maximally off-diagonal in $\mathcal{H}_\mathrm{int}$ | One-step walk operator |
| Closure | $T_\mathrm{eff}(\theta) = K^3 \cdot I$ | Diagonal in $\mathcal{H}_\mathrm{int}$ | 3-cycle return amplitude |

The off-diagonal structure of $U$ is the walk mechanism. The diagonal structure of $T_\mathrm{eff}$ is the emergence of independent channels after one full phase cycle. Both are exact — neither is an approximation.

---

## 5. Proof of Requirement R1 from Axiom 2

**Claim**: Under Axiom 2 (internal isotropy of the medium), $K_j(\theta) = K_\mathrm{spatial}(\theta)$ for all $j \in \mathbb{Z}_3$.

**Strategy**: Show that $C_3$-equivariance of $U(\theta)$ is equivalent to R1, then derive $C_3$-equivariance from internal isotropy.

**Step 1**: Compute $({\bar S} \otimes I) \; U(\theta) \; ({\bar S}^\dagger \otimes I)$.

$$(\bar{S} \otimes I)\left(\sum_j |j+1\rangle\langle j| \otimes K_j\right)(\bar{S}^\dagger \otimes I)
= \sum_j \bar{S}|j+1\rangle\langle j|\bar{S}^\dagger \otimes K_j
= \sum_j |j+2\rangle\langle j+1| \otimes K_j$$

Substituting $k = j+1$:

$$= \sum_k |k+1\rangle\langle k| \otimes K_{k-1}$$

**Step 2**: For $C_3$-equivariance $({\bar S} \otimes I) U ({\bar S}^\dagger \otimes I) = U$:

$$\sum_k |k+1\rangle\langle k| \otimes K_{k-1} = \sum_k |k+1\rangle\langle k| \otimes K_k$$

Since the $\{|k+1\rangle\langle k|\}_k$ are linearly independent operators on $\mathcal{H}_\mathrm{int}$, matching coefficients:

$$K_{k-1}(\theta) = K_k(\theta) \quad \forall\, k \in \mathbb{Z}_3$$

This is the cyclic condition $K_0 = K_1 = K_2 = K$ — i.e., R1. $\square$

**Step 3**: Derive $C_3$-equivariance of $U(\theta)$ from Axiom 2 (internal isotropy).

The three generation channels $\{[0], [1], [2]\} \in \mathbb{Z}_3$ are the three cosets of the quotient $\mathbb{Z}_6 / \mathbb{Z}_2$. The coset labels $j = 0, 1, 2$ are defined only relative to each other — there is no absolute reference for which coset to call "[0]." The C_3 action $j \mapsto j+1 \bmod 3$ is the symmetry group of this construction.

Formally: the generation quotient is defined as the orbit space of a cyclic group action. The coupling Hamiltonian $H_\mathrm{int\text{-}ext}(\theta)$ is derived from the Propagation Lagrangian by integrating the coupling term over the internal sector. The Propagation Lagrangian contains no term that distinguishes the three generation cosets by absolute label — the only structure it can use is the coset algebraic structure, which is $C_3$-invariant.

Therefore $H_\mathrm{int\text{-}ext}(\theta)$ satisfies:

$$\bar{S} \, H_\mathrm{int\text{-}ext}(\theta) \, \bar{S}^\dagger = H_\mathrm{int\text{-}ext}(\theta)$$

and consequently $U(\theta) = e^{-iH_\mathrm{int\text{-}ext}(\theta)\tau}$ satisfies the same $C_3$-equivariance.

By Steps 1–2, $C_3$-equivariance of $U(\theta)$ is equivalent to R1. $\square$

**The key premise** (audit target for Codex):

> The Propagation Lagrangian contains no term distinguishing absolute generation labels $j \in \mathbb{Z}_3$.

This is exactly Lumi's isotropy argument in physical language: "the medium has no preferred internal phase direction." In mathematical language: the coupling term in the Lagrangian is a function of the coset algebraic structure only, not of the coset labeling.

If Codex accepts this premise from the G1 model + Propagation Lagrangian, then R1 follows from Axiom 2, and Axiom 4 is derived (not postulated).

---

## 6. Explicit Construction: $K_\mathrm{spatial}(\theta)$ via Heat Kernel

**Recommended implementation** (continuum, satisfies R2):

$$K_\mathrm{spatial}(\theta) = K_{S^3}(e, e; \tau(\theta))$$

where $K_{S^3}(x, y; t)$ is the heat kernel on $S^3 \cong SU(2)$:

$$K_{S^3}(e, e; t) = \frac{1}{(4\pi t)^{3/2}}\left(1 + \frac{1}{6}\mathcal{R}\, t + O(t^2)\right) > 0 \quad \forall\, t > 0$$

and $\tau(\theta) = c(\theta) \cdot l_P^2$ where $c(\theta) = n(\theta)^{-1}$ is the local signal speed from the Propagation Lagrangian.

**Properties under this construction**:

| Requirement | Satisfied? | Reason |
|-------------|-----------|--------|
| R1 (phase-independence) | **Yes** — $K$ has no $j$-dependence | Heat kernel is $j$-blind by construction |
| R2 (positivity) | **Yes** — $K_{S^3} > 0$ for all $t > 0$ | Standard result for compact manifold heat kernels |
| R3 (isotropy) | **Yes** — $K_{S^3}(e,e;t)$ depends on $t(\theta)$ only | $SO(3)$ acts isometrically on $S^3$; on-diagonal kernel is scalar |
| R4 (causal locality) | **Yes** — $\tau(\theta)$ is local in $\theta$ | Propagation Lagrangian is local |

**Fisher information from this construction**:

$$G_{ij}^\mathrm{spatial}(\theta) = \frac{\partial \log K}{\partial \theta^i} \cdot \frac{\partial \log K}{\partial \theta^j}
= \frac{D^2}{4} \cdot \frac{\partial \log n(\theta)}{\partial \theta^i} \cdot \frac{\partial \log n(\theta)}{\partial \theta^j}$$

By R3 (isotropy): $G^\mathrm{spatial} = \lambda_0 I_D$ where $\lambda_0 = \frac{D}{4}\|\nabla_\theta \log n\|^2$.

Total Fisher (3 channels, Fisher additivity from L5):

$$G(\theta) = 3\lambda_0 I_D \implies \sqrt{\det G} = 3^{D/2} \sqrt{\det g} = N^{D/2} \sqrt{\det g} \quad \checkmark$$

---

## 7. What Codex Must Audit

| Item | Check | Critical? |
|------|-------|-----------|
| **R1 from Lagrangian** | Does the Propagation Lagrangian contain any term distinguishing generation cosets by label? | **Yes — this is the hinge** |
| **R1 $\iff$ equivariance** | Is Step 2 in Section 5 (linear independence argument) correct? | Yes |
| **R2 for heat kernel** | Is $K_{S^3}(e,e;t) > 0$ for all $t > 0$? | Yes (standard result — Codex to confirm) |
| **R3 → isotropy of Fisher block** | Does scalar $K$ imply $G^\mathrm{spatial} = \lambda_0 I_D$? | Yes |
| **Two-level distinction** | Is the division into primitive $U$ and effective $T_\mathrm{eff}$ correct and internally consistent? | Yes |
| **No-go compatibility** | Does R1 conflict with `g3_product_walk_no_go.md` Section 6? | See below |

**On no-go compatibility**: The no-go (Section 6 of `g3_product_walk_no_go.md`) says a phase-independent walk cannot fix the EXACT coefficient $\alpha = 1/(2\pi N^{D/2})$. This is correct — the Fisher Information Bridge only needs the SCALING $N^{D/2}$, not the exact value of $\alpha$. The no-go blocks the G3 coefficient problem; it does not block the Fisher scaling problem. The two targets are orthogonal.

---

## 8. Status After Codex Audit (2026-03-25)

Codex audited this spec and rejected three claims:

| Condition | Pre-audit claim | Codex verdict |
|-----------|----------------|---------------|
| R1 (phase-independence) | Derived from coset isotropy | **REJECTED** — current Lagrangian is scalar; doesn't model $\mathbb{Z}_3$ at all; absence of labels ≠ $C_3$ symmetry |
| R2 (positivity) | Confirmed via $S^3$ heat kernel | **CONFIRMED** ✓ |
| R3 (spatial isotropy) | Immediate from Axiom 2 | **OPEN** — requires $SO(D)$ averaging argument (outer product is rank-1, not $I_D$) |
| R4 (causal locality) | Immediate from Axiom 2 | **CONFIRMED** ✓ |
| H_C3stat | Closed | **OPEN** — depends on R1 |
| H_prod | Closed via DFT eigenbasis | **REJECTED** — orthogonal eigenvectors ≠ statistical independence |
| R (Regularity) | Closed | Deferred (depends on R1 + R2) |
| Lemma 2 | Closed | **OPEN** — depends on H_C3stat |
| Axiom 4 | Derived (not postulated) | **REJECTED** — must remain explicit postulate |
| God Equation | DERIVED (0.92) | **NOT upgraded** — stays CONDITIONAL (0.80) |

**What survives**: two-level operator split, heat-kernel positivity route, R4.

**Three remaining gaps before upgrade**:

1. **Richer Lagrangian**: The Propagation Lagrangian must be extended to explicitly model the $\mathbb{Z}_3$ internal sector and define $H_\mathrm{int\text{-}ext}(\theta)$ as a generation-resolved operator.

2. **H_prod proof**: A proper probabilistic argument showing $P(X^{(1)}, X^{(2)}, X^{(3)}\mid\theta) = \prod_a p_a(X^{(a)}\mid\theta)$ from the physics, not from eigenspace decomposition.

3. **Fisher isotropy averaging**: Replace the rank-1 outer product with an $SO(D)$-averaged Fisher block, or find a different construction that naturally gives $\lambda_0 I_D$.

---

*Written 2026-03-25 by Claude*
*Codex audit verdict added 2026-03-25*
*Status: SPEC v1 — AUDIT COMPLETE — Axiom 4 is an explicit postulate — God Equation CONDITIONAL (0.80)*
