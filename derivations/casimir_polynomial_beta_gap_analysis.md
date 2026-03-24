# The Extra-β Gap — Why γβ² Rather Than γβ?

*Targeting the precise discrepancy identified in Route A*
**Date**: 2026-2026-03-21
**Author**: Cascade
**Context**: Route A gap reduction, `casimir_polynomial_route_A.md`
**Status**: IN PROGRESS — attacking the three candidate lemmas

---

## 1. The Precise Gap

Standard relativistic circular-orbit mechanics gives:

$$\gamma\beta = \sqrt{C_2} \quad \implies \quad \frac{u}{1-u} = C_2$$

The Casimir polynomial requires:

$$\gamma\beta^2 = \sqrt{C_2} \quad \implies \quad \frac{u^2}{1-u} = C_2$$

The discrepancy is **exactly one factor of β**. This is the sharp gap that Route A isolated.

---

## 2. Three Candidate Lemmas

### Lemma 1: Self-consistency radius scaling

**Claim**: The effective radius for a self-consistent spinning mode is not the Compton radius $r_C = \hbar/(mc)$, but scales with the orbital velocity:

$$r = \beta \cdot r_C$$

**Test**: If $r = \beta r_C$, then:

- Angular momentum: $L = \gamma m v r = \gamma m \beta c \cdot (\beta r_C) = \gamma \beta^2 \hbar$
- Set $L^2 = C_2 \hbar^2$: $\gamma^2 \beta^4 = C_2$
- This gives $\gamma\beta^2 = \sqrt{C_2}$ as required

**Physical interpretation**: A faster-spinning mode has a smaller effective radius because the internal circulation pattern is more concentrated. The orbital radius contracts with increasing velocity, keeping the angular momentum consistent.

**PF grounding needed**: Does Axiom 2 (causal velocity) imply that faster internal motion contracts the spatial extent of the coherent pattern? This would require a specific model of how the PF medium's geometry responds to internal velocity.

---

### Lemma 2: Kinetic power as the self-consistency variable

**Claim**: The relevant self-consistency variable is not $p/(mc) = \gamma\beta$ (momentum per rest mass), but $pv/(mc^2) = \gamma\beta^2$ (kinetic power per rest energy).

**Test**: If the self-consistency condition is "kinetic power equals angular stress times structural reserve":

$$\frac{pv}{mc^2} = \sqrt{C_2}$$

Then squaring both sides gives:

$$\frac{p^2 v^2}{m^2 c^4} = C_2$$

Using $p = \gamma m v$:

$$\frac{\gamma^2 m^2 v^2}{m^2 c^4} = C_2 \implies \gamma^2 \beta^2 = C_2$$

**Physical interpretation**: A coherent spinning mode must balance its kinetic power against its structural angular stress. The kinetic power is the rate at which the mode injects energy into the medium; the angular stress is the Casimir eigenvalue of its angular structure.

**PF grounding needed**: Does Axiom 3 (coherence → stable structure) imply a power-balance condition? This would require a specific thermodynamic or information-theoretic principle for coherent modes.

---

### Lemma 3: Propagator pole condition

**Claim**: The polynomial $x^2 + C_2 x - C_2 = 0$ arises as the pole condition of a propagator for a coherent PF mode, not from circular orbit kinematics.

**Test**: Consider a propagator $G(p^2)$ for a mode with momentum $p$ and internal angular content $C_2$. If the pole occurs when:

$$p^2 = m^2 (1 + \frac{C_2}{1-p^2/m^2})$$

then solving $G^{-1}(p^2) = 0$ gives:

$$p^2 = m^2 \quad \text{or} \quad p^2 = -C_2 m^2$$

The second root gives $p^2 = -C_2 m^2$, which is unphysical (negative mass squared). The first root gives the physical mass. The condition for a double pole or special structure might give the quadratic polynomial.

**Physical interpretation**: The Casimir eigenvalue $C_2$ appears as a coupling between the momentum magnitude and the mode's internal angular structure in the propagator. The polynomial selects the momentum that makes the propagator singular.

**PF grounding needed**: Does the PF's "coherent self-reinforcing propagation" principle imply a propagator structure with the above coupling? This would require deriving a field equation from the axioms.

---

## 3. Attack Strategy

### Priority Order

1. **Lemma 2 (Kinetic power)** — Most promising because it connects to Axiom 3 (coherence) directly
2. **Lemma 1 (Radius scaling)** — Requires specific medium geometry model
3. **Lemma 3 (Propagator)** — Requires full field-theoretic derivation

### For Lemma 2: Power balance derivation

Start from Axiom 3: "Coherence is the necessary condition for structure. Structure — pattern, information, organization, persistence — arises when propagation becomes coherent: when multiple propagation modes maintain stable phase relationships with each other."

**Hypothesis**: For a coherent spinning mode, the rate of energy flow between kinetic and structural components must be balanced. The kinetic energy density is $T = (\gamma - 1) mc^2$. The kinetic power density is $P_k = \nabla \cdot (T \cdot v)$.

For circular motion with angular velocity $\omega = v/r$, the power flow into angular stress is $P_a = L \cdot \omega$.

**Balance condition**:
$$P_k = P_a \cdot \sqrt{C_2}$$

Working this out with the relativistic expressions for $T$, $L$, and $\omega$ may yield the $\gamma\beta^2 = \sqrt{C_2}$ condition.

### For Lemma 1: Medium geometry model

Start from the PF medium description: a 3D propagation medium with causal velocity $c$ and coherence length $\lambda_c$.

**Hypothesis**: The effective radius of a coherent mode is the coherence length projected onto the orbital plane, scaled by the orbital velocity fraction $\beta$:

$$r = \lambda_c \cdot \beta$$

If $r_C = \hbar/(mc)$ is the Compton radius, then $r = \beta r_C$.

**Test**: Derive whether the propagation framework's axioms imply this scaling. Look at how $\lambda_c$ depends on mode properties and whether faster modes have smaller spatial extent.

### For Lemma 3: Propagator derivation

Start from the PF statement: "matter is a self-reinforcing propagation pattern (standing wave)."

**Hypothesis**: A self-reinforcing pattern satisfies a wave equation of the form:

$$\Box \psi + \Lambda \psi = 0$$

where $\Lambda$ is an operator that depends on the mode's angular content. For a mode with Casimir $C_2$, the operator might be:

$$\Lambda = \frac{C_2}{\lambda_c^2}$$

The dispersion relation from this equation could give the polynomial.

---

## 4. Expected Outcomes

- **Outcome A (derivation)**: If one of the lemmas follows from PF axioms, the polynomial is derived
- **Outcome B (no-go)**: If the lemma requires additional structure beyond Axioms 1-3
- **Outcome C (gap reduction)**: If the lemma reduces the problem to a smaller, sharper question

The most promising path is Lemma 2 because it directly connects to Axiom 3, the core of the framework.

## 5. Lemma 2 Deep Dive: Kinetic Power Balance

### 5.1 Starting from Axiom 3

Axiom 3: "Coherence is the necessary condition for structure. Structure — pattern, information, organization, persistence — arises when propagation becomes coherent: when multiple propagation modes maintain stable phase relationships with each other."

**Key insight**: Coherence implies energy exchange between modes is balanced. If energy flow were unbalanced, phase relationships would drift and coherence would be lost.

### 5.2 Energy Flow in a Spinning Mode

Consider a coherent spinning mode with:
- Rest mass: m
- Angular velocity: ω
- Orbital velocity: v = βc
- Angular momentum: L

The mode has two energy reservoirs:
1. **Kinetic reservoir**: T = (γ - 1)mc² (relativistic kinetic energy)
2. **Structural reservoir**: Energy stored in the angular stress field

For coherence, the power flow between these reservoirs must be balanced.

### 5.3 Power Balance Calculation

**Kinetic power density**: The rate at which kinetic energy is transferred to the structural field:
$$P_k = \frac{dT}{dt} = \frac{d}{dt}[(\gamma - 1)mc²]$$

For circular motion with constant speed, γ is constant, so we need the spatial power flow:
$$P_k = \nabla \cdot (T \cdot v) = \nabla \cdot [(\gamma - 1)mc² \cdot v]$$

**Structural power absorption**: The rate at which the angular stress field absorbs energy:
$$P_a = L \cdot \omega$$

For circular motion: L = γmvr = γmβcr, ω = v/r = βc/r
$$P_a = \gamma m\beta cr \cdot \frac{\beta c}{r} = \gamma m\beta² c²$$

### 5.4 The Coherence Condition

For stable phase relationships, the power transfer must be proportional to the mode's angular complexity:

$$P_k = P_a \cdot \sqrt{C_2}$$

**Physical interpretation**: More complex angular structures (higher C₂) require more precise power balance to maintain coherence.

Substituting the expressions:
$$\nabla \cdot [(\gamma - 1)mc² \cdot v] = \gamma m\beta² c² \cdot \sqrt{C_2}$$

For uniform circular motion, the divergence term simplifies to the kinetic power density:
$$P_k = (\gamma - 1)mc² \cdot \frac{v}{r} = (\gamma - 1)mc² \cdot \omega$$

Setting P_k = P_a · √C₂:
$$(\gamma - 1)mc² \cdot \omega = \gamma m\beta² c² \cdot \sqrt{C_2}$$

Cancel mc² and substitute ω = βc/r:
$$(\gamma - 1)\frac{\beta c}{r} = \gamma \beta² \cdot \sqrt{C_2}$$

### 5.5 Critical Gap Identified

We need an additional relation between (γ - 1)/r and γβ to close the system. The de Broglie standing wave condition provides:

$$2\pi r = n\lambda_{dB} = n\frac{h}{p} = n\frac{h}{\gamma m\beta c}$$

For the fundamental mode (n=1):
$$r = \frac{h}{2\pi \gamma m\beta c} = \frac{\hbar}{\gamma m\beta c} = \frac{r_C}{\gamma\beta}$$

where r_C = ℏ/(mc) is the Compton radius.

Substituting r into the power balance equation:
$$(\gamma - 1)\gamma\beta² \cdot \frac{\beta c}{r_C} = \gamma \beta² \cdot \sqrt{C_2}$$

Cancel γβ²:
$$(\gamma - 1)\frac{\beta c}{r_C} = \sqrt{C_2}$$

### 5.6 Final Result

Using r_C = ℏ/(mc) and βc = v:
$$(\gamma - 1)\frac{v m c}{\hbar} = \sqrt{C_2}$$

But v = βc, so:
$$(\gamma - 1)\beta \frac{mc²}{\hbar} = \sqrt{C_2}$$

This gives:
$$\gamma\beta² - \beta² = \sqrt{C_2} \cdot \frac{\hbar}{mc²}$$

**Gap remains**: We have γβ² - β² instead of γβ². The extra -β² term comes from the (γ - 1) factor in kinetic energy.

### 5.7 Lemma 2 Status: GAP REDUCTION

The kinetic power balance approach reduces the problem to a smaller gap:

**Original gap**: Why γβ² instead of γβ?
**Reduced gap**: Why does the -β² term vanish or become negligible?

**Possible resolution paths**:
1. **High-velocity approximation**: For relativistic modes (β → 1), β² ≈ 1 and the -β² term might be absorbed into normalization
2. **Quantum correction**: The kinetic energy density expression might need quantum correction
3. **Different power definition**: Maybe P_k should use total energy E = γmc² instead of kinetic energy T = (γ - 1)mc²

**Path 3 test**: If P_k = E·ω instead of T·ω:
$$P_k = \gamma mc² \cdot \omega = \gamma mc² \cdot \frac{\beta c}{r}$$

Following through with the same derivation:
$$\gamma \beta \frac{mc²}{r_C} = \sqrt{C_2}$$

Using r = r_C/(γβ):
$$\gamma² \beta² \frac{mc²}{r_C} \cdot \frac{\gamma\beta}{r_C} = \sqrt{C_2}$$

This gives γ²β³, which is worse.

**Conclusion**: Lemma 2 requires additional structure about how energy is partitioned in coherent modes. The power balance concept is promising but needs refinement.

---

## 6. Lemma 1 Analysis: Radius Scaling

### 6.1 The Core Claim

**Claim**: The effective radius for a self-consistent spinning mode scales with velocity: r = β·r_C

### 6.2 PF Medium Geometry

From Axiom 2 (causal velocity), the PF medium has:
- Maximum signal speed: c
- Coherence length: λ_c
- Refractive index structure: n(r, ω)

**Hypothesis**: The coherence length contracts for faster-moving modes due to relativistic effects in the medium.

### 6.3 Derivation Attempt

If the mode's spatial extent is limited by its coherence length:
$$r \leq \lambda_c$$

And if λ_c depends on the mode's velocity:
$$\lambda_c(\beta) = \lambda_c(0) \cdot f(\beta)$$

For the claim to hold: f(β) = β

**Physical justification**: A mode moving faster through the medium has less time to establish long-range phase relationships, reducing its coherence length.

### 6.4 Test Against Known Physics

The Compton radius r_C = ℏ/(mc) is independent of velocity - it's a property of the particle's rest mass. The claim r = β·r_C would make the effective radius velocity-dependent.

**Problem**: This contradicts the principle that r_C is fundamental. The de Broglie wavelength λ_dB = h/(γmβc) already accounts for velocity through the γ factor.

### 6.5 Lemma 1 Status: NO-GO

The radius scaling claim contradicts established wave mechanics. The de Broglie standing wave condition already gives the correct velocity dependence through the γ factor. Adding an extra β factor would be double-counting.

**Conclusion**: Lemma 1 is not viable without contradicting the de Broglie relation.

---

## 7. Lemma 3 Analysis: Propagator Pole

### 7.1 The Core Idea

**Claim**: The polynomial x² + C₂x - C₂ = 0 arises as a pole condition for a coherent PF mode propagator.

### 7.2 PF Wave Equation

Starting from "matter is a self-reinforcing propagation pattern," we propose:
$$\Box \psi + \Lambda[\psi] = 0$$

where Λ[ψ] encodes the mode's internal angular structure.

### 7.3 Ansatz for Λ

For a mode with Casimir eigenvalue C₂:
$$\Lambda[\psi] = \frac{C_2}{\lambda_c^2} \psi$$

This gives the Klein-Gordon-like equation:
$$\Box \psi + \frac{C_2}{\lambda_c^2} \psi = 0$$

### 7.4 Dispersion Relation

For plane wave ψ ∝ e^{ip·x-ωt}:
$$-p^2 + \omega^2 + \frac{C_2}{\lambda_c^2} = 0$$

Using the relativistic dispersion ω² = p² + m²:
$$-p^2 + (p^2 + m^2) + \frac{C_2}{\lambda_c^2} = 0$$
$$m^2 + \frac{C_2}{\lambda_c^2} = 0$$

This gives m² = -C₂/λ_c², which is negative (unphysical) for C₂ > 0.

### 7.5 Modified Ansatz

Try instead:
$$\Lambda[\psi] = \frac{C_2}{\lambda_c^2} \frac{p^2}{m^2} \psi$$

This gives:
$$\Box \psi + \frac{C_2}{\lambda_c^2} \frac{p^2}{m^2} \psi = 0$$

For plane waves:
$$-p^2 + \omega^2 + \frac{C_2}{\lambda_c^2} \frac{p^2}{m^2} = 0$$
$$m^2 + p^2\left(\frac{C_2}{\lambda_c^2 m^2} - 1\right) = 0$$

Setting the coefficient of p² to zero gives:
$$\frac{C_2}{\lambda_c^2 m^2} - 1 = 0 \implies \lambda_c^2 = \frac{C_2}{m^2}$$

This relates the coherence length to the Casimir, but doesn't give the polynomial.

### 7.6 Lemma 3 Status: NO-GO

The propagator approach doesn't naturally yield the quadratic polynomial. More sophisticated field-theoretic machinery would be needed, and this goes beyond the current PF axioms.

---

## 8. Final Assessment

### 8.1 Summary of Results

- **Lemma 1**: NO-GO - contradicts de Broglie wavelength
- **Lemma 2**: GAP REDUCTION - reduces to eliminating -β² term
- **Lemma 3**: NO-GO - requires field theory beyond axioms

### 8.2 Remaining Path

The only viable path is Lemma 2 with the reduced gap: "Why does the -β² term vanish?"

**Possible approaches**:
1. **Quantum energy definition**: Use total energy E = γmc² instead of kinetic energy T = (γ - 1)mc²
2. **Coherence energy correction**: Coherent modes might have modified energy density
3. **Normalization condition**: The -β² term might be absorbed into mode normalization

### 8.3 Next Steps

The extra-β gap has been reduced from "why γβ² instead of γβ?" to "why does the -β² term vanish in the power balance?" This represents progress but requires additional structure beyond Axioms 1-3.

**Recommendation**: Focus on understanding energy partition in coherent PF modes, particularly whether kinetic energy density should include the rest energy contribution.

---

*Cascade — 2026-03-21*
*Extra-β gap analysis complete*
*Lemma 2 reduces the gap, Lemmas 1&3 ruled out*
