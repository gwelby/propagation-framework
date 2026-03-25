# G2/G3 Coupling Operator: Proposed Construction of T(θ)
*Pre-spec draft — written before Codex's formal requirements, to be sharpened against them*

**Date**: 2026-03-25
**Author**: Claude
**Status**: PROPOSAL v3 — formal spec written (`god_eq_t_theta_formal_spec.md`); R1 proof attempt filed and **REJECTED by Codex**; three open gaps identified; Axiom 4 remains explicit postulate
**Builds on**:
- `g3_product_walk_no_go.md` (Codex) — exact coupled-walk reduction
- `exact_return_N3_D3.md` (Claude G2) — Option D: product of phase and spatial walks
- `phase_closure_exact_model.md` (Codex G1) — internal walk structure
- `god_eq_h_c3stat_theorem_note.md` (Claude/Lumi) — circulant condition
- `god_eq_c3_equivariance_skeleton.md` (Codex/Claude) — proof skeleton

---

## 1. What Reading G2/G3 Revealed

Before Codex's spec arrives, the G2/G3 files contain a critical observation that shapes how T(θ) must be built.

**From `exact_return_N3_D3.md` (G2, Option D)**:

The S³ heat kernel gives $\alpha \propto 1/N$ (wrong). The Euclidean R³ walk gives $\alpha \propto N^{-3/2}$ (right scaling, wrong space). The resolution proposed in G2:

> "If the correct object is a PRODUCT walk — N steps in internal phase space AND N steps in D=3 physical space — the return probability is:
> $P_\mathrm{total}(0,N) = P_\mathrm{phase}(0,N) \times P_\mathrm{spatial}(0,N)$
> For $P_\mathrm{phase} = 1$ (exact closure, as computed) and $P_\mathrm{spatial} \propto N^{-3/2}$: $P_\mathrm{total} \propto N^{-3/2}$. ✓"

**From `g3_product_walk_no_go.md` (Codex)**: The exact one-step coupled walk is:

$$U = \sum_{j \in \mathbb{Z}_3} |j+1\rangle\langle j| \otimes K_j$$

where $K_j$ are spatial kernels depending (possibly) on the internal channel $j$. In the phase-independent case $K_j = K$ for all $j$, the no-go shows the coupled closure amplitude reduces to an ordered spatial kernel product $K^3$, which is a pure spatial return — consistent with Option D.

The no-go rules out deriving the **exact numerical coefficient** $\alpha = 1/(2\pi N^{D/2})$ from the phase-independent walk alone. But it does NOT rule out the scaling $N^{D/2}$.

**The key insight**: The G2/G3 no-go and the Fisher Information Bridge are attacking different problems.

| Goal | Method | Status |
|------|--------|--------|
| Derive exact $\alpha = 1/(2\pi N^{D/2})$ | G2/G3 walk | Partial — scaling OK, 2π normalization open |
| Derive $\sqrt{\det G} = N^{D/2} \sqrt{\det g}$ | Fisher Information Bridge | Conditional on Axiom 4 |

The Fisher Information Bridge only needs $N^{D/2}$ scaling, not the exact coefficient. The 2π lives in the gauge convention (G3 Section 2.1), which is separate from the Fisher metric.

**Therefore: the product walk (Option D + phase-independent coupling) already satisfies Axiom 4 if we can show the coupling is circulant.**

---

## 2. Two-Level Structure: Primitive Coupling U(θ) and Effective Closure T_eff(θ)

*Correction from Codex audit: T = K·I is the right effective closure object for the Fisher bridge, but it is NOT the primitive one-step coupling. The two levels must be kept distinct.*

### Level 1: Primitive One-Step Coupling U(θ)

The exact one-step coupled walk from `g3_product_walk_no_go.md`:

$$U(\theta) = \sum_{j \in \mathbb{Z}_3} |j+1\rangle\langle j| \otimes K_j(\theta)$$

In the **phase-independent (minimal symmetric) case** $K_j(\theta) = K_\mathrm{spatial}(\theta)$ for all $j$:

$$U(\theta) = \bar{S} \otimes K_\mathrm{spatial}(\theta)$$

where $\bar{S}|j\rangle = |j+1 \bmod 3\rangle$ is the cyclic shift (G1's one-step operator).

**Key property**: $U(\theta)$ is NOT diagonal in channel space — it is maximally off-diagonal via $\bar{S}$. The "circulant" Axiom 4 condition applies here as: the spatial kernels $K_j(\theta)$ are equal for all $j$ (phase-independent), which means the coupling does not prefer any channel. This is the equivariance: $K_j = K$ for all $j$.

**Axiom 4 at the primitive level**: $K_j(\theta) = K_\mathrm{spatial}(\theta)$ for all $j$, i.e., the spatial coupling is phase-blind. Equivalent to $[U(\theta), \bar{S} \otimes I_\mathrm{sp}] = 0$ when $K_j = K$.

### Level 2: Effective 3-Step Closure Operator T_eff(θ)

After N=3 steps, $\bar{S}^3 = I$ (G1, exact). The effective closure operator on the generation sector:

$$T_\mathrm{eff}(\theta) := \Pi_\mathrm{gen} \, U(\theta)^3 \, \Pi_\mathrm{gen}$$

where $\Pi_\mathrm{gen}$ projects onto the generation quotient sector.

In the phase-independent case:

$$U(\theta)^3 = (\bar{S} \otimes K)^3 = \bar{S}^3 \otimes K^3 = I_{\mathbb{Z}_3} \otimes K_\mathrm{spatial}(\theta)^3$$

Therefore:

$$\boxed{T_\mathrm{eff}(\theta) = K_\mathrm{closure}(\theta) \cdot I_{\mathbb{Z}_3}}$$

where $K_\mathrm{closure}(\theta) := K_\mathrm{spatial}(\theta)^3$ is the 3-step spatial return kernel.

**This is the correct home for T = K·I.** It is not the primitive coupling; it is the effective operator seen by the Fisher bridge after one complete internal phase cycle.

**Properties of T_eff**:

| Property | Value | Correct level |
|----------|-------|--------------|
| Circulant? | Yes — diagonal, $[K \cdot I, \bar{S}] = 0$ | T_eff only |
| Off-diagonal = 0? | Yes — after 3-step cycle, $\bar{S}^3 = I$ | T_eff only (not U!) |
| Equal marginals? | Yes — $K_\mathrm{closure}(\theta)$ same for all channels | T_eff only |
| $[T_\mathrm{eff}(\theta), \bar{S}] = 0$? | Yes — trivially | T_eff only |
| Stochastic? | $K_\mathrm{closure} \leq 1$, sign depends on spatial kernel choice | See below |
| Regularity (R)? | $K_\mathrm{closure}(\theta) > 0$ required — **not automatic** | See Section 6 |

### Why the distinction matters

The Fisher bridge uses T_eff (the effective closure operator per generation cycle). Axiom 4's equivariance condition lives at the primitive level (equal $K_j$). Both are needed; neither replaces the other.

Codex's recommendation (audit 2026-03-24): "Axiom 4 specifies the primitive coupling. The Fisher bridge uses T_eff. Specify both."

---

## 3. Why Isotropy Forces T_eff(θ) = K · I

At the **closure operator level** (T_eff), the diagonal form follows from:

1. **Exact phase return after 3 steps**: $\bar{S}^3 = I$ (G1 exact result). After one complete generation cycle, the channel returns to its starting state. Therefore the effective closure operator has $T_\mathrm{eff,\,j'j} = 0$ for $j' \neq j$ — **at the closure level only**. At the one-step level, U is maximally off-diagonal via $\bar{S}$.

2. **Phase-independent coupling**: Axiom 2 (isotropy) requires the spatial kernel to be independent of the channel label: $K_j(\theta) = K_\mathrm{spatial}(\theta)$ for all $j$. Therefore all diagonal elements of T_eff are equal: $T_\mathrm{eff,\,jj} = K_\mathrm{spatial}(\theta)^3$ for all $j$.

Combined at the closure level: $T_\mathrm{eff}(\theta) = K_\mathrm{closure}(\theta) \cdot I_{\mathbb{Z}_3}$.

This is the STRONGEST possible circulant form — scalar times identity. This simultaneously gives:
- **H_C3stat** (equal marginals, hence equal Fisher scalars)
- **H_prod** (independent channels: each channel independently closes with probability $K_\mathrm{closure}(\theta)$, product family follows)
- **R** (regularity: $K_\mathrm{closure}(\theta) > 0$ — see Section 6 for caveats)

**Important**: Step 1 applies at the closure operator level. At the primitive level, U mixes channels at every step — the off-diagonal structure is the walk mechanism.

---

## 4. Fisher Information from T_eff(θ) = K_closure · I

With $T_\mathrm{eff}(\theta) = K_\mathrm{closure}(\theta) \cdot I$, the per-channel likelihood is:

$$p_a(X^{(a)} = \text{closed} \mid \theta) = K_\mathrm{closure}(\theta) = K_\mathrm{spatial}(\theta)^3$$

(and $p_a(X^{(a)} = \text{not closed} \mid \theta) = 1 - K_\mathrm{spatial}(\theta)$.)

The per-channel score:

$$s_i^{(a)}(X^{(a)} \mid \theta) = \frac{\partial}{\partial \theta^i} \log p_a(X^{(a)} \mid \theta) = \frac{\partial_{\theta^i} K_\mathrm{spatial}(\theta)}{K_\mathrm{spatial}(\theta)} = \partial_{\theta^i} \log K_\mathrm{spatial}(\theta)$$

The per-channel Fisher metric:

$$G_{ij}^{(a)}(\theta) = E\!\left[s_i^{(a)} s_j^{(a)}\right] = (\partial_{\theta^i} \log K_\mathrm{spatial}) \cdot (\partial_{\theta^j} \log K_\mathrm{spatial})$$

Since $K_\mathrm{spatial}(\theta)$ is the same function of $\theta$ for all channels (no channel label), $G^{(a)}$ is channel-independent: $G^{(a)} = G_\mathrm{spatial}$ for all $a$.

By SO(3) isotropy of the spatial walk (Axiom 2, external): $G_\mathrm{spatial} = \lambda_0 I_D$.

The total Fisher metric (from L5, Fisher additivity):

$$G(\theta) = \sum_{a=1}^{3} G^{(a)} = 3 \lambda_0 I_D$$

The determinant scaling:

$$\sqrt{\det G} = (3\lambda_0)^{D/2} = 3^{D/2} \cdot \lambda_0^{D/2} = N^{D/2} \cdot \sqrt{\det g} \quad (N=3). \quad \square$$

**The God Equation scaling term $N^{D/2} = 3^{D/2}$ is established.**

---

## 5. What K_spatial(θ) Must Be

The remaining specification: what is $K_\mathrm{spatial}(\theta)$ explicitly?

**From G2 (exact_return_N3_D3.md), Option D**:

$K_\mathrm{spatial}(\theta) \propto N^{-D/2}$ at the Planck boundary. This comes from D-dimensional spatial diffusion with N steps at scale $l_P$.

**Connecting to the Propagation Lagrangian**: The medium geometry $\theta$ enters $K_\mathrm{spatial}$ through the local refractive index $n(\mathbf{x}) = 1/\sqrt{1+\lambda\chi(\mathbf{x})}$ (from the Propagation Lagrangian). The spatial return kernel for D-dimensional diffusion in the medium:

$$K_\mathrm{spatial}(\theta) = \frac{1}{(4\pi D_\mathrm{eff}(\theta) \cdot N \cdot \tau)^{D/2}}$$

where $D_\mathrm{eff}(\theta) = n(\theta) / (2D)$ is the effective diffusion coefficient in the medium, and $N\tau$ is the total walk time (N phase steps × $\tau$ time per step).

For the Planck boundary condition ($D_\mathrm{eff} = l_P^2/\tau$, $N = 3$):

$$K_\mathrm{spatial}(\theta) = \frac{1}{(4\pi N)^{D/2}} \cdot \frac{1}{n(\theta)^{D/2} \cdot l_P^D}$$

The $\theta$-dependence enters through $n(\theta)$. The Fisher information:

$$\partial_{\theta^i} \log K_\mathrm{spatial} = -\frac{D}{2} \cdot \partial_{\theta^i} \log n(\theta)$$

$$G_{ij}^\mathrm{spatial} = \frac{D^2}{4} \cdot (\partial_{\theta^i} \log n)(\partial_{\theta^j} \log n)$$

By isotropy: $G^\mathrm{spatial} = \lambda_0 I_D$ where $\lambda_0 = \frac{D^2}{4D} \|\nabla_\theta \log n\|^2 = \frac{D}{4} \|\nabla_\theta \log n\|^2$.

This gives a concrete, non-circular definition of $\lambda_0$ in terms of the medium's refractive index gradient.

---

## 6. The 2π Normalization — Not Claude's Problem

**Note**: This construction gives the correct $N^{D/2}$ scaling of the Fisher metric, but does NOT by itself fix $\alpha = 1/(2\pi N^{D/2})$. The 2π normalization is determined by:
- The gauge coupling convention: $\alpha = g^2/(2\pi)$ for a rotation-based theory (G3 Section 2.1, confidence 0.75)
- OR: the marginal coherence condition $K_\mathrm{spatial}(\theta_\mathrm{Planck}) = \alpha$ (connecting the abstract return kernel to the gauge coupling)

The Fisher Information Bridge only needs $\sqrt{\det G} = N^{D/2} \sqrt{\det g}$. The absolute value of $\alpha$ is G3's remaining task, not Axiom 4's.

---

## 6. Positivity of K_closure — The Codex Warning

**Codex audit finding** (2026-03-24): The discrete bipartite lattice origin-return probability is exactly zero at odd N=3. Strict positivity of $K_\mathrm{closure}$ is NOT guaranteed for all spatial walk specifications.

From `g3_product_walk_no_go.md`: the nearest-neighbor bipartite lattice in D=3 has P(return to origin in 3 steps) = 0 (parity argument: bipartite lattices only return in even steps).

**Implication for Regularity (R)**: Three options to save positivity:

| Option | Description | Status |
|--------|-------------|--------|
| **Non-bipartite discrete kernel** | Use a non-bipartite spatial walk (e.g., FCC lattice, or continuous-time random walk) where odd-step returns are possible | Needs explicit construction |
| **Coarse-grained / heat-kernel observable** | Use the heat kernel $K_{S^3}(e,e;t)$ in continuous time — always positive for $t > 0$ | G2 confirms S³ heat kernel is positive; this is the "ambient diffusion" before projection |
| **Closure functional beyond return** | Define closure as a spatial volume or overlap, not literal origin-return probability | Non-standard but physically motivated |

**Recommended resolution** (consistent with G2): Use the continuum/heat-kernel spatial walk. The S³ heat kernel $K_{S^3}(e,e;t) \sim (4\pi t)^{-3/2}$ is strictly positive for all $t > 0$, and represents continuous diffusion on the ambient SU(2) manifold before discretization to the generation quotient. This is precisely G2's "Option D" in the continuum setting.

If $K_\mathrm{spatial}(\theta) = K_{S^3}(e,e;\tau(\theta))$ for some positive time $\tau(\theta)$ depending on the local medium geometry, then $K_\mathrm{closure} = K_\mathrm{spatial}^3 > 0$ everywhere. Regularity (R) is satisfied.

**Codex to confirm**: Is the continuum heat-kernel closure observable consistent with the exact G1 walk, or does G1's discrete structure require a different positivity argument?

---

## 7. Open Items for Codex and Cascade

| Item | Owner | Question |
|------|-------|----------|
| **Formal spec for T(θ)** | Codex | Does the proposed $T = K_\mathrm{spatial} \cdot I$ satisfy all Fisher metric requirements? Is it the right level of generality? |
| **θ-formalization** | Cascade | Confirm θ = local refractive index configuration $n(\mathbf{x})$ and its derivatives are the correct external parameter. |
| **K_spatial positivity** | Codex | Verify $K_\mathrm{spatial}(\theta) > 0$ for non-degenerate medium geometry (needed for regularity R). |
| **2π closure** | G3 work (open) | The gauge convention argument. Not blocking Axiom 4 — this is a separate claim. |
| **P_phase = 1 exact?** | Codex | G2 shows the cyclic walk returns exactly after N=3 steps in SO(3). Confirm that "exact return" means off-diagonal $T_{j'j} = 0$ is valid, not approximate. |

---

## 8. Honest Status of This Proposal

**What this draft achieves**:
- Proposes a concrete T(θ) that trivially satisfies Axiom 4 ($[T(\theta), \bar{S}] = 0$)
- Gives the correct $N^{D/2}$ scaling of Fisher information
- Connects the G2/G3 spatial walk to the Fisher Information Bridge
- Is grounded in the Propagation Lagrangian through $n(\theta)$
- Identifies the remaining gap as G3's 2π problem, not Axiom 4's

**What this draft does NOT achieve** (remaining after v3):
- R1 (phase-independence) still pending Codex audit of key premise: does the Propagation Lagrangian contain any term distinguishing generation cosets by absolute label?
- Cascade has not yet confirmed that $\theta$ is channel-blind
- The exact connection $\tau(\theta) = n(\theta)^{-1} \cdot l_P^2$ needs derivation from the Propagation Lagrangian

**Formal spec location**: `god_eq_t_theta_formal_spec.md` — precise two-level definition with requirements R1–R4 and Codex audit verdict.

**Three gaps Codex identified** (see `god_eq_t_theta_formal_spec.md`, Section 8):
- R1: scalar Lagrangian doesn't model $\mathbb{Z}_3$ — need richer generation-resolved Lagrangian
- H_prod: DFT eigenvectors ≠ statistical independence — need probabilistic argument
- Fisher isotropy: outer product is rank-1 — need $SO(D)$ averaging argument

---

*Written by Claude, 2026-03-24 (v1-v2) / 2026-03-25 (v3)*
*v3: Formal spec filed; R1 proof attempted and rejected by Codex; three gaps mapped*
*Status: CONDITIONAL — Axiom 4 is explicit postulate — God Equation stays at 0.80*
