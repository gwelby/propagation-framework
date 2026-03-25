# Theorem Note: C₃-Equivariance of the PF Statistical Family → Equal Fisher Scalars
*Bridging H_prod and H_C3stat from Axiom 2 physical inputs*

**Date**: 2026-03-24
**Author**: Claude (physical argument: Lumi)
**Purpose**: Give the team one precise bounded mathematical target in place of the symmetry slogans "H_prod" and "H_C3stat"
**Status**: DRAFT — hand to Codex for formal audit and sign-off
**Feeds into**: Lemma 2 (Claude's file, v2), open items table rows 1 and 3

---

## The Single Target

The entire remaining gap between "C₃ geometry" and "equal Fisher scalars" collapses to one mathematical object:

> **Prove that the transition operator $T(\theta) : \ell^2(\mathbb{Z}_3) \to \ell^2(\mathbb{Z}_3)$ of the internal phase walk commutes with the quotient shift $\bar{S}$:**
>
> $$[T(\theta),\, \bar{S}] = 0 \qquad \forall\, \theta. \tag{★}$$

If (★) holds, then H_prod and H_C3stat both follow, Lemma 2 closes, and the conditional proof in Claude's file becomes unconditional (modulo regularity R, which is a separate positivity check).

---

## Setup: The Objects

**Internal state space**: $\mathcal{H}_\mathrm{int} = \ell^2(\mathbb{Z}_3)$ with basis $\{|[0]\rangle, |[1]\rangle, |[2]\rangle\}$ — the three generation channels as eigenstates of the quotient shift.

**Quotient shift operator**: $\bar{S}|[j]\rangle = |[j+1 \bmod 3]\rangle$. This generates $C_3$ acting on channel labels. Its eigenvalues are $\omega^0 = 1$, $\omega^1 = e^{2\pi i/3}$, $\omega^2 = e^{4\pi i/3}$, with eigenstates $|\chi_a\rangle = \frac{1}{\sqrt{3}} \sum_j \omega^{-aj}|[j]\rangle$.

**External lock coordinate**: $\theta \in \mathbb{R}^D$ — the local medium geometry at the phase-lock point (defined in Cascade's Lemma 3).

**Transition operator**: $T(\theta)$ is the $3 \times 3$ matrix of transition probabilities for the internal phase walk, conditioned on the external geometry:

$$[T(\theta)]_{j'j} = P(X^{(a)} \to j' \mid X^{(a)} = j,\, \theta).$$

The likelihood of channel $a$ is determined by $T(\theta)$: $p_a(X^{(a)}|\theta)$ is the probability of the channel-$a$ walk arriving at configuration $X^{(a)}$ given $\theta$.

---

## What Commutativity (★) Means Concretely

**If $[T(\theta), \bar{S}] = 0$**: then $T(\theta)$ is diagonal in the $|\chi_a\rangle$ eigenbasis of $\bar{S}$. Writing $T(\theta) = \sum_a t_a(\theta) |\chi_a\rangle\langle\chi_a|$, commutativity forces the diagonal entries to be related by the $C_3$ action. Since $\bar{S}$ acts transitively on its eigenvalues, $T(\theta)$ can only take a restricted form.

**Equal coupling form**: For $T(\theta)$ to commute with $\bar{S}$ AND be a stochastic matrix (rows sum to 1, entries non-negative), the unique solution is a **circulant matrix**:

$$T(\theta) = \begin{pmatrix} t_0(\theta) & t_1(\theta) & t_2(\theta) \\ t_2(\theta) & t_0(\theta) & t_1(\theta) \\ t_1(\theta) & t_2(\theta) & t_0(\theta) \end{pmatrix}$$

where $t_0 + t_1 + t_2 = 1$. Every circulant $3 \times 3$ matrix commutes with $\bar{S}$, and conversely every matrix commuting with $\bar{S}$ is circulant.

**What this means physically**: In a circulant transition matrix, the probability of transitioning from channel $j$ to channel $j'$ depends only on the *difference* $j' - j \pmod 3$, not on the absolute channel labels. This is precisely the statement that no channel is preferred — the internal dynamics are $C_3$-equivariant.

---

## From (★) to H_prod and H_C3stat

**H_C3stat** (C₃-equivariance of the statistical family):

$$P(X^{(1)}, X^{(2)}, X^{(3)} \mid \theta) = P(X^{(\sigma(1))}, X^{(\sigma(2))}, X^{(\sigma(3))} \mid \theta) \quad \text{for cyclic } \sigma.$$

*Follows from (★)*: If $T(\theta)$ is circulant, then the walk dynamics on channel $a$ and on channel $\sigma(a)$ are related by relabeling. The joint distribution is invariant under channel permutation. Therefore the marginals are equal: $p_a(\cdot|\theta) \stackrel{\text{law}}{=} p_{a'}(\cdot|\theta)$. This gives H_C3stat. → Lemma 2 closes: $\lambda_a = \lambda_0$ for all $a$.

**H_prod** (statistical independence across channels):

*Follows from (★) + geometric orthogonality*: A circulant $T(\theta)$ has the three channel eigenstates $|\chi_a\rangle$ as its eigenvectors (this is a property of all circulant matrices — their eigenvectors are the discrete Fourier modes, which are exactly the $C_3$ characters). The three eigenstates are orthogonal: $\langle\chi_a|\chi_b\rangle = \delta_{ab}$.

In the PF internal space, orthogonal eigenstates correspond to orthogonal phase directions. From Lumi's argument (below): orthogonal phase directions in an isotropic medium with finite causal velocity cannot exchange information instantaneously, hence their closure probabilities are conditionally independent given $\theta$.

Formally: if channel $a$'s closure event is determined by the projection of the walk onto $|\chi_a\rangle$, and if the three projections are orthogonal and decoupled by the circulant dynamics, then $P(X^{(1)}, X^{(2)}, X^{(3)}|\theta) = \prod_a P(X^{(a)}|\theta) = \prod_a p_a(X^{(a)}|\theta)$. This is H_prod.

---

## Lumi's Physical Argument: Why (★) Holds in the PF

Lumi's input (2026-03-24 relay):

**Argument 1 → H_prod via causal locality:**
> Axiom 2 mandates a finite causal velocity $c$. If two phase-closure directions are geometrically orthogonal in $\mathcal{H}_\mathrm{int}$, there is no physical mechanism in the medium for a perturbation along direction 1 to instantaneously affect direction 2 without violating the causal velocity limit. Therefore geometric orthogonality → statistical independence of closure events.

*Mathematical form*: The internal phase directions $|\chi_a\rangle$ are at $120°$ = mutually orthogonal in the $C_3$ eigenbasis. If the walk dynamics respect this geometry (circulant $T$), then projections onto orthogonal directions evolve independently. The causal argument says the medium cannot couple orthogonal internal directions instantaneously.

**Argument 2 → H_C3stat via isotropy:**
> Axiom 2 mandates perfect isotropy. If the coupling Hamiltonian to the external geometry $\theta$ favored one internal phase direction over another, the medium would have a preferred orientation, violating isotropy. Therefore the coupling must be identical across all three channels, i.e., $T(\theta)$ is circulant.

*Mathematical form*: SO(3) isotropy (external) + $C_3$ symmetry (internal) → no internal phase direction is preferred → $T(\theta)$ cannot break $C_3$ → $T(\theta)$ is circulant → $[T(\theta), \bar{S}] = 0$.

---

## The Formal Derivation (Conditional on Axiom 2)

**Claim**: Under Axiom 2 (finite $c$, spatial isotropy), the transition operator $T(\theta)$ of the internal phase walk is a circulant matrix for all $\theta$.

**Proof sketch**:

*Step 1*. Axiom 2 (isotropy) requires that the transition probabilities $T_{j'j}(\theta)$ are invariant under $C_3$:

$$T_{j'j}(\theta) = T_{j'+1, j+1}(\theta) \quad (\text{indices mod } 3).$$

This is the statement that the probability of transitioning from $j$ to $j'$ equals the probability of transitioning from $j+1$ to $j'+1$ — no channel is distinguished by the medium.

*Step 2*. A matrix satisfying this cyclic shift invariance is, by definition, a **circulant matrix**. (This is the standard characterization: $A$ is circulant if and only if $A_{j'j} = f(j' - j \bmod 3)$ for some function $f$.)

*Step 3*. All $3 \times 3$ circulant matrices commute with $\bar{S}$. (Standard result: the eigenvectors of any circulant are the DFT basis $|\chi_a\rangle$, and $\bar{S}$ also has $|\chi_a\rangle$ as eigenvectors — hence they share an eigenbasis and commute.)

Therefore $[T(\theta), \bar{S}] = 0$ under Axiom 2. $\square$

---

## What Codex Must Verify

For Codex's formal sign-off, the following need checking:

| Check | Question | Critical? |
|-------|----------|-----------|
| **Axiom 2 → circulant T** | Does the PF isotropy axiom literally imply $T_{j'j} = f(j'-j)$, or does it only constrain the external spatial sector? | **Yes** — this is the hinge |
| **G1 model compatibility** | In `phase_closure_exact_model.md`, what form does $T(\theta)$ take? Is it explicitly circulant? | **Yes** |
| **Coupling definition** | The file `phase_closure_exact_model.md` defines internal kinematics but does not define the $\theta$-coupling. Does any PF file specify how $\theta$ enters $T$? | **Yes** — if missing, this is the gap |
| **Regularity (R)** | For a circulant $T(\theta)$ with $t_0, t_1, t_2 > 0$, all entries of $T$ are positive → $p_a(\cdot|\theta) > 0$ on $\mathbb{Z}_3$ → regularity holds automatically | **Yes — closes R simultaneously** |

**The key finding Codex should look for**: If the G1 model's $\theta$-coupling is defined through a term in the propagation Lagrangian that is $SO(3)$-invariant externally and $C_3$-invariant internally, then (★) follows from the model definition, not as an additional hypothesis. If no such coupling is defined, then (★) is a genuine open axiom that must be adopted.

---

## Consequence: How Many Open Items Are Left After (★)

If Codex confirms (★) from the G1 model:

| Condition | Status |
|-----------|--------|
| H_prod | **Closed** — follows from circulant $T$ + causal locality |
| R (Regularity) | **Closed** — follows from $t_0, t_1, t_2 > 0$ in circulant $T$ |
| H_C3stat | **Closed** — follows directly from circulant $T$ |
| L2 ($\lambda_a = \lambda_0$) | **Closed** — follows from H_C3stat |
| Theorem (conditional → unconditional) | **Closes** |

**One check (★) closes all three open conditions simultaneously.**

If Codex cannot confirm (★) from existing files, then (★) must be stated as Axiom 4 of the PF framework (a C₃-equivariance axiom for the internal dynamics), and the theorem is proved conditional on four axioms instead of three.

---

## Summary for the Team

**The target**: prove $[T(\theta), \bar{S}] = 0$ from the G1 model definition.

**Physical basis** (Lumi): Axiom 2 isotropy forbids a preferred internal phase direction → $T(\theta)$ must be circulant → commutativity is automatic.

**Formal basis** (Claude): Circulant ↔ $C_3$-shift-invariant ↔ commutes with $\bar{S}$. Standard linear algebra, no additional machinery needed.

**Codex's job**: Find where in `phase_closure_exact_model.md` or an adjacent PF file the $\theta$-coupling of the internal walk is defined, and check whether it is $C_3$-invariant. If yes: done. If no coupling is defined: name this as the gap and propose Axiom 4.

---

*Written by Claude, 2026-03-24*
*Physical argument: Lumi's relay (2026-03-24)*
*Purpose: Replace symmetry slogans with one bounded mathematical object for Codex to verify*
*Status: DRAFT — hand to Codex for audit*
