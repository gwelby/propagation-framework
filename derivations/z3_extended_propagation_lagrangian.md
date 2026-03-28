# ℤ₃-Extended Propagation Lagrangian
*Exploratory derivation of a circulant T(θ) candidate for the God Equation coupling layer*

**Date**: 2026-03-25
**Author**: Claude Code
**Status**: EXPLORATORY DERIVATION NOTE — historical candidate, superseded by later hostile audits
**Role**: records a proposed ℤ₃-resolved coupling layer; does not by itself close God Equation Gap 1
**Feeds into**: `god_eq_t_theta_formal_spec.md` (R1), `god_eq_c3_equivariance_skeleton.md` (Version C)

---

## 0. Executive Summary

**The problem (Codex's exact verdict, 2026-03-25):**

> *"The current Propagation Lagrangian is a scalar theory that doesn't model ℤ₃ at all. Absence of generation labels is not evidence of C₃ symmetry. You cannot derive a 3×3 matrix symmetry from a scalar field theory that doesn't resolve the internal sector."*

**This file's response:**

1. Extend the scalar Propagation Lagrangian to three generation-labelled fields, one per ℤ₃ coset, using the G1 model as justification for exactly three channels.
2. Show the extension is C₃-invariant by construction (Axiom 2 forbids preferred channels).
3. Derive the coupling matrix T(θ) from the equations of motion and show it is circulant.
4. Conclude [T(θ), S̄] = 0 from circulant structure (not from hand-waving).
5. Offer a concrete candidate route toward R1 / H_C3stat and expose the remaining gaps around H_prod and Fisher closure.

**What this closes vs what remains:**

| Condition | Before this file | After this file |
|-----------|-----------------|-----------------|
| R1 — [T(θ), S̄] = 0 | POSTULATE / target | **ARGUED candidate** from the proposed ℤ₃-invariant Lagrangian |
| H_C3stat — equal marginals | OPEN (depends on R1) | **ARGUED candidate** if the coupling identification is accepted |
| H_prod — statistical independence | OPEN | **OPEN** |
| God Equation Gap 1 | OPEN | **NOT CLOSED** by this file alone |
| God Equation Gap 2 (H_prod full) | — | Still open |

---

## 1. The Problem in Detail

The scalar Propagation Lagrangian (`propagation_lagrangian.md`) is:

$$\mathcal{L}_\text{prop} = \frac{1}{2}\eta^{ab}(\partial_a\chi)(\partial_b\chi) - V(\chi) + \lambda\chi T$$

Here χ is a **single** scalar field — the local propagation potential. It has no generation index. When we ask "does the coupling of the internal generation walk to θ satisfy [T(θ), S̄] = 0?", the scalar Lagrangian cannot answer: it doesn't have a ℤ₃-resolved structure to resolve.

Codex's point is therefore exact: the derivation in `god_eq_c3_equivariance_skeleton.md` Section 11 (and Version C) shows the **kinematic** ℤ₃ walk (the G1 model) is C₃-symmetric, but the coupling to θ requires the coupling Lagrangian to resolve the three channels. A scalar theory couples all three channels identically by **silence** — but absence of a distinction is not the same as a derived symmetry.

**What Codex wants:** A Lagrangian that explicitly contains three generation fields and from which the C₃ invariance of T(θ) emerges as a theorem, not as a hypothesis.

---

## 2. Setup: Three Generation Fields from the G1 Model

**From the G1 exact model** (`phase_closure_exact_model.md`):

- The generation walk lives on ℤ₆ (spinorial), with observable quotient ℤ₃ = ℤ₆/ℤ₂.
- The three observable generation channels are the cosets [0], [1], [2] of the quotient map q: k ↦ k mod 3.
- The cyclic shift S̄: [j] ↦ [j+1 mod 3] generates the C₃ action on the generation sector.
- These three channels are **ontologically distinct propagation modes** — the electron/muon/tau correspond to different phase winding numbers on the coset structure.

**Minimal extension principle**: Each distinct propagation mode identified by G1 must have its own propagation potential field in the Lagrangian. The scalar χ represents the generation-blind propagation potential. The ℤ₃-extended Lagrangian assigns one potential per generation channel:

$$\chi_j : \mathcal{M} \to \mathbb{R}, \quad j \in \{0, 1, 2\} = \mathbb{Z}_3$$

where χ_j(x) is the local propagation potential **as experienced by generation channel j**.

**This is not a new hypothesis.** It is the direct application of Axiom 1 (all phenomena are propagation events; each distinct mode has its own field) to the three-mode structure established by G1.

---

## 3. The ℤ₃-Extended Propagation Lagrangian

### 3.1 Construction

The ℤ₃-extended Propagation Lagrangian is:

$$\boxed{
\mathcal{L}_{\mathbb{Z}_3} = \sum_{j \in \mathbb{Z}_3} \left[\frac{1}{2}\eta^{ab}(\partial_a\chi_j)(\partial_b\chi_j) - V(\chi_j)\right] - \kappa\sum_{j \in \mathbb{Z}_3} \chi_j\chi_{j+1 \bmod 3} + \frac{\lambda}{3}\left(\sum_{j \in \mathbb{Z}_3} \chi_j\right) T
}$$

The four terms are:
1. **Kinetic terms**: one kinetic term per channel, identical form
2. **Potential terms**: identical self-potential V(χ_j) for each channel
3. **Inter-channel coupling**: −κ χ_j χ_{j+1} summed cyclically over ℤ₃
4. **Coupling to matter**: λ times the ℤ₃-centroid (the generation-averaged field) times the stress-energy T

The parameter κ is the inter-channel coupling constant. The factor 1/3 in the matter coupling ensures normalization consistency with the scalar theory.

### 3.2 Reduction to Scalar Theory

In the generation-symmetric vacuum: χ₀ = χ₁ = χ₂ = χ.

$$\mathcal{L}_{\mathbb{Z}_3}\Big|_{\chi_j = \chi} = 3\cdot\frac{1}{2}(\partial\chi)^2 - 3V(\chi) - 3\kappa\chi^2 + \lambda\chi T$$

Rescaling: ℒ_eff = ½(∂χ)² − V_eff(χ) + (λ/3)χT where V_eff absorbs the κχ² term.

This matches the scalar Propagation Lagrangian (up to the coupling renormalization by 1/3, which is absorbed into λ). **All existing predictions of the scalar theory are preserved in the symmetric vacuum.**

### 3.3 C₃ Invariance — Explicit Proof

The C₃ group action on the fields is the permutation representation:

$$\sigma^* : \chi_j(x) \mapsto \chi_{j+1 \bmod 3}(x), \quad \forall j \in \mathbb{Z}_3$$

**Claim**: $\mathcal{L}_{\mathbb{Z}_3}[\sigma^*\chi_j] = \mathcal{L}_{\mathbb{Z}_3}[\chi_j]$ for all field configurations.

**Proof**: Apply $\sigma^*$ to each term.

**Term 1** (kinetic): $\sum_j ½(\partial\chi_{j+1})^2 = \sum_j ½(\partial\chi_j)^2$ (reindex $j \to j-1 \bmod 3$). ✓

**Term 2** (potential): $\sum_j V(\chi_{j+1}) = \sum_j V(\chi_j)$ (same reindex). ✓

**Term 3** (inter-channel): $\sum_j \chi_{j+1}\chi_{j+2} = \sum_j \chi_j\chi_{j+1}$ (reindex $j \to j-1$). ✓

**Term 4** (matter coupling): $\frac{\lambda}{3}\sum_j \chi_{j+1} \cdot T = \frac{\lambda}{3}\sum_j \chi_j \cdot T$. ✓

Therefore $\mathcal{L}_{\mathbb{Z}_3}$ is invariant under the C₃ permutation action. **QED.**

**The C₃ symmetry is manifest in the Lagrangian** — it is a structural property of the construction, not an assumption about the coupling.

---

## 4. Equations of Motion and the Coupling Matrix T(θ)

### 4.1 Equations of Motion

Varying $\mathcal{L}_{\mathbb{Z}_3}$ with respect to χ_j:

$$\Box\chi_j + V'(\chi_j) = \frac{\lambda}{3}T + \kappa(\chi_{j-1} + \chi_{j+1 \bmod 3})$$

In the linearized regime (small perturbations δχ_j around a homogeneous background χ̄):

$$\Box(\delta\chi_j) + V''(\bar\chi)\,\delta\chi_j = \kappa\left(\delta\chi_{j-1} + \delta\chi_{j+1}\right) + \frac{\lambda}{3}\delta T$$

### 4.2 The Coupling Matrix

Writing the internal dynamics as a matrix equation in the generation sector $\mathbf{f} = (\delta\chi_0, \delta\chi_1, \delta\chi_2)^T$:

$$(\Box + m^2)\mathbf{f} = \kappa\,M\mathbf{f} + \text{source}$$

where $m^2 = V''(\bar\chi)$ and the coupling matrix is:

$$M = \begin{pmatrix} 0 & 1 & 1 \\ 1 & 0 & 1 \\ 1 & 1 & 0 \end{pmatrix} = S̄ + S̄^{-1}$$

**M is explicitly circulant**: each row is a cyclic shift of the previous. This is immediate from the nearest-neighbor sum $\delta\chi_{j-1} + \delta\chi_{j+1}$.

For the general circulant structure (not just nearest-neighbor), the most general C₃-invariant Lagrangian with arbitrary coupling constants t₀, t₁, t₂ gives:

$$T(\theta) = \begin{pmatrix} t_0 & t_1 & t_2 \\ t_2 & t_0 & t_1 \\ t_1 & t_2 & t_0 \end{pmatrix}$$

This is the **general 3×3 circulant matrix** — the unique form consistent with C₃ invariance of the Lagrangian. The values $t_0, t_1, t_2 \geq 0$ with $t_0 + t_1 + t_2 = 1$ (stochastic normalization) parametrize the dynamics; they are not determined by the Lagrangian symmetry alone but require matching to the mass spectrum.

### 4.3 The Circulant is T(θ)

The transition operator T(θ) of the generation walk — the object that appears in `god_eq_t_theta_formal_spec.md` — is identified with the normalized coupling matrix derived from the equations of motion:

$$T(\theta) = \text{Normalize}(M(\theta)) \quad \text{where} \quad M(\theta) = [m_{j'j}(\theta)]$$

and $m_{j'j}(\theta) = \kappa(\theta)(S̄_{j'j} + S̄^{-1}_{j'j})$ encodes the local coupling strength via $\kappa(\theta)$.

**Key claim**: Under the ℤ₃-extended Lagrangian, T(θ) is circulant for **all** local geometries θ. The circulant form is not a function of θ — it is locked in by the Lagrangian's C₃ symmetry.

---

## 5. Candidate Route to R1 from Circulant Structure

**Candidate theorem (R1 route)**: Under $\mathcal{L}_{\mathbb{Z}_3}$, the channel coupling kernels may satisfy $K_j(\theta) = K_\text{spatial}(\theta)$ for all j ∈ ℤ₃ and all θ, provided the identification between the EOM coupling matrix and the primitive walk kernels is valid.

**Proof**: The coupling matrix T(θ) is circulant (Section 4.2). A circulant matrix $[t_0, t_1, t_2]$ satisfies $T_{j'j} = t_{j'-j \bmod 3}$ — depending only on the relative shift, not on absolute channel labels. In the primitive coupling operator $U(\theta) = \sum_j |j+1\rangle\langle j| \otimes K_j(\theta)$, the kernel $K_j(\theta)$ is determined by the $j$-th row of T(θ). Since all rows of a circulant are cyclic shifts of each other, the kernel $K_j(\theta)$ is the same function of θ for all j. Formally:

$$T_{j'j}(\theta) = t_{j'-j\bmod 3}(\theta) \implies K_j(\theta) = \sum_{j'} T_{j'j}(\theta)|j'\rangle = K_\text{spatial}(\theta) \;\forall\, j$$

where $K_\text{spatial}(\theta)$ is the common channel kernel defined by the first column of T(θ).

**Audit caution**: later hostile audit did not accept this as a completed proof. The step from a circulant EOM coupling matrix to channel-identical primitive kernels is a modeling identification that still needs justification in the exact walk/statistical construction.

**Candidate corollary**: $U(\theta) = \bar{S} \otimes K_\text{spatial}(\theta)$ — the primitive coupling factorizes as claimed in `god_eq_t_theta_formal_spec.md` Section 3, if the identification above is accepted.

---

## 6. Candidate Route from R1 to H_C3stat

**Candidate theorem (H_C3stat route)**: Under $\mathcal{L}_{\mathbb{Z}_3}$, the statistical family of the generation walk is C₃-invariant:

$$P(X^{(0)}, X^{(1)}, X^{(2)} | \theta) = P(X^{(\sigma(0))}, X^{(\sigma(1))}, X^{(\sigma(2))} | \theta)$$

for all cyclic permutations σ.

**Proof**: From R1, the per-channel marginal distributions are all equal:

$$p_j(x|\theta) = \sum_{x'} T_{jx'}(\theta)\,\rho(x') = \sum_{x'} T_\text{spatial}(x-x';\theta)\,\rho(x') = p_0(x|\theta) \;\forall\, j$$

(using the circulant form $T_{jx'} = t_{j-x' \bmod 3}$). Equal marginal laws imply equal Fisher information blocks $G^{(j)}(\theta)$. Under H_iso (each block isotropic by Axiom 2), $\lambda_j(\theta) = \lambda_0(\theta)$ for all j. Equal scalar Fisher entries imply the joint distribution is permutation-invariant. **QED.**

**Candidate consequence**: Lemma 2 of the Generation-Channel Additivity Theorem would close if the statistical-family identification and isotropic Fisher block assumptions are accepted:

$$G(\theta) = 3\lambda_0(\theta)\,I_D \implies \sqrt{\det G} = 3^{D/2}\sqrt{\det g} = N^{D/2}\sqrt{\det g} \quad \checkmark$$

---

## 7. Closure-Level Decoupling Does Not Yet Prove H_prod

**H_prod** (statistical independence): $P(X^{(0)}, X^{(1)}, X^{(2)} | \theta) = \prod_{j} p_j(X^{(j)}|\theta)$

This is the condition that requires the most care.

**What does NOT work** (Codex's prior rejection): orthogonal DFT eigenvectors of T ≠ statistical independence of the channel observables. The DFT modes diagonalize the dynamics, but the physical observables are the generation labels j ∈ {0,1,2}, not the DFT modes.

**The closure-level argument**:

From `god_eq_t_theta_formal_spec.md` Section 4.2, under R1:

$$T_\text{eff}(\theta) = K_\text{closure}(\theta) \cdot I_{\mathbb{Z}_3}$$

This says: **after one full generation cycle (3 steps), the return amplitude is the same in all channels, and there are no off-diagonal correlations between channels.**

Formally: the 3-step return matrix in the generation sector is proportional to the identity. This means:

$$\langle j | T_\text{eff}(\theta) | j'\rangle = K_\text{closure}(\theta)\,\delta_{j,j'}$$

The off-diagonal elements are exactly zero. This is the statement that after one complete cycle, the generation channels are **dynamically decoupled**. For the Fisher information calculation (which integrates over one complete closure cycle), the per-channel contributions are independent.

**What this would give, at most**: closure-level decoupling of the effective return matrix. That is weaker than full `H_prod`, and later hostile audit did not accept it as sufficient to conclude Fisher additivity:

$$G(\theta) = \sum_{j=0}^{2} G^{(j)}(\theta) = 3\lambda_0(\theta)\,I_D \quad \checkmark$$

**What remains for a complete H_prod proof**:
A full probabilistic argument showing that the closure-level decoupling implies factorization of the joint distribution, not just of the Fisher information. This requires specifying the noise model for the channel observables, which is not yet defined in the PF. This is a well-posed open subproblem (it is the "statistical independence" gap identified by Codex), and it does block unconditional God Equation closure.

---

## 8. Summary: What the ℤ₃-Extended Lagrangian Proposes

Starting from Axioms 1–3 plus the G1 model (N=3 generation channels from ℤ₆/ℤ₂ quotient):

**Chain of derivation:**

```
Axiom 1 + G1 model
    → Three generation fields χ_j, j ∈ ℤ₃
         |
Axiom 2 (no preferred internal direction)
    → Lagrangian must be C₃-invariant
         |
Minimal C₃-invariant extension
    → ℒ_{ℤ₃} (Section 3.1)
         |
Equations of motion of ℒ_{ℤ₃}
    → T(θ) is circulant (Section 4)
         |
Circulant T(θ)
    → R1: K_j(θ) = K_spatial(θ) for all j   (Section 5)
         |
R1 + Axiom 2 isotropy
    → H_C3stat: equal channel marginals       (Section 6)
         |
H_C3stat + candidate T_eff structure
    → closure-level decoupling proposal       (Section 7)
         |
Full H_prod + Fisher additivity + isotropy
    → still open
         |
    → God Equation remains CONDITIONAL on later board
```

**Audit status**: this file is best read as a candidate route toward a derived coupling principle. Later hostile audit did not accept Axiom 4 as eliminated by this note alone.

---

## 9. Two Remaining Open Subproblems

### 9.1 H_prod Full Proof (God Equation Gap 2)

The closure-level argument in Section 7 gives, at best, a candidate decoupling statement for one full return cycle. A complete proof requires:

1. Define the noise model: what is the probability distribution of the observable $X^{(j)}$ given channel j is in state $|j'\rangle$ after one closure step?
2. Show the joint noise across channels is uncorrelated.
3. This likely requires showing that the ℤ₃-extended Lagrangian produces independent channel-by-channel phase fluctuations at closure.

**Route under consideration**: a Markovian or other explicit noise model may provide the needed factorization, but hostile audit did not accept "Axiom 2 => coarse first-order Markovity" as proved. Any future closure must supply that probabilistic step directly.

**Status**: ARGUED. Not yet a formal proof.

### 9.2 Values of (t₀, t₁, t₂)

The circulant form of T(θ) is derived; the specific values of the circulant entries $(t_0, t_1, t_2)$ are not. They parametrize the dynamics within the C₃-symmetric manifold and must be matched to observation (mass spectrum, mixing angles).

The constraint $t_0 + t_1 + t_2 = 1$ (stochastic normalization) leaves 2 free parameters. The additional constraint from the God Equation derivation (equal marginals → $t_0 = t_1 = t_2 = 1/3$ in the maximally symmetric case?) would close these. This needs investigation.

**Status**: OPEN. This does not by itself settle the God Equation because the bridge also depends on `H_prod` and the Fisher/isotropy closure steps.

---

## 10. Codex Audit Targets

| Claim | Check | Critical? |
|-------|-------|-----------|
| **G1 → three fields** | Is it valid to assign one field per G1 coset? Is this Axiom 1 or additional structure? | Yes |
| **C₃ invariance of ℒ_{ℤ₃}** | Are all four terms invariant under σ*? (Section 3.3 proof complete) | Yes |
| **EOM → circulant M** | Is the nearest-neighbor sum $\delta\chi_{j-1} + \delta\chi_{j+1}$ the only C₃-invariant coupling? Or are there higher-range terms? | Yes |
| **M(θ) circulant → T(θ) circulant** | Is the identification T(θ) = Normalize(M(θ)) justified? | Yes |
| **R1 from circulant** | Is the proof in Section 5 correct? | Yes |
| **H_C3stat from R1** | Is equal marginals derivation in Section 6 correct? | Yes |
| **H_prod at closure** | Is closure-level decoupling sufficient for Fisher additivity? | **No — hostile audit later rejected this** |
| **Axiom 4 eliminated** | Can the C₃ equivariance argument stand without Axiom 4? | **HINGE** |
| **Scalar Lagrangian limit** | Does ℒ_{ℤ₃} reduce correctly to ℒ_prop in symmetric vacuum? | Yes |

**The hinge question for the audit**: Is the derivation chain "Axiom 2 (no preferred direction) → Lagrangian must be C₃-invariant → T(θ) circulant → R1" a logical derivation or does it require an additional postulate at the step "Lagrangian must be C₃-invariant"?

**Answer on record**: The Lagrangian *could* break C₃ if there were a preferred generation label in the physics. The G1 model establishes that there is no such preferred label — the cosets are defined only relative to each other. Axiom 2 (isotropy) reinforces this: the medium cannot distinguish [0] from [1] from [2] by internal direction. Therefore the Lagrangian must be C₃-invariant. This is the same logic by which Lorentz invariance forces the scalar kinetic term to be $\eta^{ab}\partial_a\chi\partial_b\chi$ rather than $g^{ab}_{jk}\partial_a\chi_j\partial_b\chi_k$ with an arbitrary anisotropic metric.

---

## 11. Relation to Previous Failed Attempts

| Attempt | Why It Failed | How This File Fixes It |
|---------|--------------|----------------------|
| Version A (likelihood route) | Required the statistical model before the Lagrangian | Lagrangian comes first |
| Version B (operator commutator) | Showed kinematic C₃ but not statistical C₃ | ℒ_{ℤ₃} gives statistical model directly via EOM |
| Version C (Hamiltonian route) | Argued $[H, S̄] = 0$ from coset isotropy, but Codex said: "scalar field has no ℤ₃ to be symmetric over" | Three-field Lagrangian explicitly resolves ℤ₃ — C₃ symmetry is manifest, not inferred |

The scalar Lagrangian had the right *argument* (internal isotropy forbids preferred channels) but the wrong *object* (a single scalar field cannot carry the three-channel structure). The ℤ₃-extended Lagrangian gives the correct object, and the argument carries through.

---

*Written 2026-03-25 by Claude Code*
*Directly addresses Codex's 2026-03-25 audit rejection of God Equation R1*
*Status at time of writing: exploratory derivation note*
*Current read: historical candidate route; see later God Equation freeze audits for authoritative status*
