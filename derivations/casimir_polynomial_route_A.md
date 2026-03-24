# Route A: Casimir Polynomial from Relativistic Self-Consistency
*Can the de Broglie standing-wave condition be grounded in PF Axioms 1-3?*

**Date**: 2026-03-21
**Author**: Cascade
**Route**: A (Relativistic Standing-Wave / de Broglie)
**Authority**: `casimir_polynomial_brief.md`, `casimir_polynomial_route_matrix.md`
**Current claim state**: Issue #3 remains ARGUED (0.65)

---

## 1. Starting Point

The polynomial `x² + C₂x - C₂ = 0` (equivalently `x²/(1-x) = C₂`) already appears from two independent physical arguments:

1. **Quantum**: Poincaré Casimir eigenvalue equation (Rivero, `g3_casimir_weinberg_angle.md` §2)
2. **Classical**: Relativistic de Broglie standing-wave condition (`g3_casimir_weinberg_angle.md` §6)

Route A asks: does the classical route follow from PF axioms specifically?

---

## 2. The de Broglie Derivation (Reproduced)

For a relativistic particle of spin $j$ on a circular orbit, the angular momentum is:

$$L^2 = j(j+1)\hbar^2 = C_2 \hbar^2$$

The relativistic angular momentum for circular motion at velocity $v = \beta c$:

$$L = \gamma m v r = \gamma m \beta c r$$

The de Broglie standing-wave condition (one wavelength fits the orbit):

$$2\pi r = \lambda_{dB} = \frac{h}{\gamma m v} = \frac{h}{\gamma m \beta c}$$

Therefore $r = \hbar / (\gamma m \beta c)$, and:

$$L = \gamma m \beta c \cdot \frac{\hbar}{\gamma m \beta c} = \hbar$$

Wait — this gives $L = \hbar$ always, independent of $j$. That's the $n=1$ standing wave. For the general case with angular momentum quantum number $j$:

$$L^2 = j(j+1)\hbar^2$$

The relativistic relation $L = \gamma m v r$ with the de Broglie constraint gives a self-consistency condition. Following Rivero's route more carefully:

The key equation is the relativistic dispersion relation for a spinning mode. For a particle at rest with spin $j$, the spin angular momentum satisfies:

$$\frac{L^2}{m^2 c^2 r^2} = \frac{j(j+1)\hbar^2}{m^2 c^2 r^2}$$

Using the Compton radius $r_C = \hbar/(mc)$ as the natural scale for a self-reinforcing mode:

$$\frac{L^2}{m^2 c^2 r_C^2} = j(j+1) = C_2$$

Now the self-consistency condition for a relativistic spinning mode: the internal velocity $\beta_{int}$ of the spinning propagation pattern satisfies:

$$\frac{\beta_{int}^2}{\sqrt{1 - \beta_{int}^2}} = \sqrt{C_2}$$

Squaring both sides and writing $u = \beta_{int}^2$:

$$\frac{u^2}{1-u} = C_2$$

$$u^2 + C_2 u - C_2 = 0$$

This is the Casimir polynomial.

---

## 3. PF Grounding — The Chain

### Step 1: Matter is a self-reinforcing propagation pattern (DERIVED)

From Axiom 1 (propagation fundamental) + Axiom 3 (coherence → stable structure):

> A particle is a standing wave — a propagation pattern that reinforces itself through constructive interference.

This is already DERIVED in `the_propagation_framework.md` Part 2, §3.

### Step 2: Internal propagation is at the causal velocity (ARGUED)

From Axiom 2 (every medium has a causal velocity $c$):

> The internal motion of a self-reinforcing mode is propagation at $c$. The observable velocity $v < c$ is the drift of the pattern's center. The internal "spinning" is at $c$.

This is the Zitterbewegung picture: the electron's internal oscillation frequency $\omega = mc^2/\hbar \approx 1.24 \times 10^{20}$ Hz corresponds to an internal velocity of $c$. The Compton wavelength $\lambda_C = \hbar/(mc)$ is the radius of this internal circulation.

**Status**: ARGUED. The Zitterbewegung interpretation is supported by Gouanère (2005/2008) channeling resonance and by QFT (Dirac equation oscillatory solutions), but PF does not independently derive that internal propagation must be at $c$ rather than some fraction of $c$. However, Axiom 2 says the causal velocity is the *maximum* propagation speed, and Axiom 1 says propagation is fundamental — so a mode that propagates internally should do so at the maximum rate available. A mode propagating below $c$ internally would be a composite, not a fundamental mode.

**Named dependency**: "Fundamental modes propagate internally at $c$." This follows from Axioms 1+2 if "fundamental" means "not decomposable into slower sub-modes."

### Step 3: Angular structure characterized by Casimir $C_2 = j(j+1)$ (ESTABLISHED)

A spinning propagation mode in 3D has angular momentum classified by the representations of $SO(3)$ (or its cover $SU(2)$). The quadratic Casimir $C_2 = j(j+1)$ is the unique rotationally-invariant measure of angular content.

**Status**: ESTABLISHED. This is representation theory applied to the PF's 3D medium. The PF already uses $SO(3)$ and $SU(2)$ representations throughout (`topological_weight_from_propagation.md`).

### Step 4: The self-consistency condition → THE CRITICAL BRIDGE

**Claim**: For a fundamental mode spinning at internal velocity $\beta_{int} c$ with angular content $C_2$, self-consistency requires:

$$\frac{\beta_{int}^2}{\sqrt{1-\beta_{int}^2}} = \sqrt{C_2}$$

**Attempt to derive this from PF axioms:**

Consider a mode circulating at velocity $v = \beta c$ on a circle of Compton radius $r_C = \hbar/(mc)$.

The relativistic angular momentum is:
$$L = \gamma m v r_C = \gamma \beta \cdot mc \cdot \frac{\hbar}{mc} = \gamma \beta \hbar$$

The quantum angular momentum for spin $j$ is:
$$|L| = \sqrt{j(j+1)} \hbar = \sqrt{C_2} \hbar$$

Self-consistency: $\gamma \beta = \sqrt{C_2}$, i.e.:

$$\frac{\beta}{\sqrt{1-\beta^2}} = \sqrt{C_2}$$

Squaring: $\beta^2/(1-\beta^2) = C_2$, which gives:

$$\beta^2 = \frac{C_2}{1+C_2}$$

This is NOT the Casimir polynomial. This gives $u/(1-u) = C_2$, not $u^2/(1-u) = C_2$.

**The discrepancy**: My derivation gives $u/(1-u) = C_2$ (linear in $u$ on the left). The Casimir polynomial is $u^2/(1-u) = C_2$ (quadratic in $u$ on the left).

The difference is one power of $u = \beta^2$.

---

## 4. Diagnosing the Discrepancy

The standard relativistic angular momentum gives $\gamma\beta = \sqrt{C_2}$, leading to $u/(1-u) = C_2$.

The Casimir polynomial requires $u^2/(1-u) = C_2$, which means $\gamma\beta^2 = \sqrt{C_2}$, or equivalently:

$$\frac{\beta^2}{\sqrt{1-\beta^2}} = \sqrt{C_2}$$

This is **not** the standard relativistic angular momentum relation. It has an extra factor of $\beta$ compared to $\gamma\beta = \sqrt{C_2}$.

### What physical quantity satisfies $\gamma\beta^2 = \sqrt{C_2}$?

$$\gamma\beta^2 = \frac{v^2/c^2}{\sqrt{1-v^2/c^2}} = \frac{T_{kin}}{mc^2} \cdot \frac{2}{\beta} \cdot \beta = \ldots$$

Actually, let me reconsider. The quantity $\gamma\beta^2 = \gamma v^2/c^2$ can be written as:

$$\gamma\beta^2 = \frac{p \cdot v}{mc^2}$$

where $p = \gamma mv$ is the relativistic momentum. So $pv = \gamma m v^2 = \gamma\beta^2 mc^2$.

The quantity $pv$ is twice the classical kinetic energy for $v \ll c$, and in general it is the **power** of the mode (momentum × velocity). Setting $pv/(mc^2) = \sqrt{C_2}$:

$$\frac{p \cdot v}{mc^2} = \sqrt{C_2}$$

Squaring: $p^2 v^2 / (mc^2)^2 = C_2$.

For circular motion with $r = \hbar/(mc)$ (Compton radius):

$$L = pr = \frac{pv}{c} \cdot \frac{\hbar}{mc} \cdot \frac{c}{v} = \frac{pv}{v} \cdot \frac{\hbar}{mc}$$

This doesn't simplify cleanly. Let me try a different approach.

### Alternative: the de Broglie condition as a *squared* angular momentum relation

If instead of $L = \sqrt{C_2}\hbar$, we require the **squared** angular momentum to be self-consistently generated:

$$L^2 = C_2 \hbar^2$$

And if $L$ for a relativistic circular mode is:

$$L = \gamma m v r$$

Then $L^2 = \gamma^2 m^2 v^2 r^2$.

If the radius $r$ is not the Compton radius but is itself determined self-consistently by the de Broglie condition $2\pi r = \lambda_{dB}$:

$$r = \frac{\hbar}{\gamma m v} = \frac{\hbar}{\gamma m \beta c}$$

Then:

$$L = \gamma m \beta c \cdot \frac{\hbar}{\gamma m \beta c} = \hbar$$

This gives $L = \hbar$ (always), so $C_2 = L^2/\hbar^2 = 1$ for all modes. That's wrong.

The resolution in Rivero's framework: the de Broglie condition allows $n$ wavelengths around the orbit, not just one. With $n$ wavelengths:

$$2\pi r = n \lambda_{dB} \implies r = \frac{n\hbar}{\gamma m \beta c}$$

Then $L = \gamma m \beta c \cdot r = n\hbar$.

And $L^2 = n^2\hbar^2 = C_2\hbar^2$ requires $n^2 = C_2 = j(j+1)$, so $n = \sqrt{j(j+1)}$.

For $j = 1/2$: $n = \sqrt{3/4} \approx 0.866$ — not an integer. The de Broglie quantization with integer $n$ does not give the correct angular momentum.

This means the simple de Broglie circular orbit picture does not self-consistently reproduce the Casimir polynomial from standard relativistic mechanics.

---

## 5. Where the Extra $\beta$ Comes From — Rivero's Actual Argument

Re-reading `g3_casimir_weinberg_angle.md` §6 carefully:

> "For a particle of spin $j$ on a circular orbit, the relativistic velocity satisfies:
> $\beta^2/\sqrt{1-\beta^2} = \sqrt{j(j+1)}$"

This is stated without full derivation. The equation $\beta^2/\sqrt{1-\beta^2} = \sqrt{C_2}$ is the starting point, not derived from $L = \gamma mv r$.

The discrepancy I found in §4 is real: standard relativistic angular momentum gives $\gamma\beta = \sqrt{C_2}$, not $\gamma\beta^2 = \sqrt{C_2}$.

**The extra factor of $\beta$** must come from an additional physical ingredient beyond simple circular orbit mechanics. Candidates:

1. **A specific radius relation**: If $r = \beta \cdot r_C$ (the orbit radius is $\beta$ times the Compton radius), then $L = \gamma m \beta c \cdot \beta r_C = \gamma\beta^2 \hbar$, giving $\gamma\beta^2 = \sqrt{C_2}$. But why should $r = \beta r_C$?

2. **An energy-momentum partition**: The quantity $\gamma\beta^2 = pv/(mc^2)$ represents the ratio of "kinetic power" to rest energy. This might be the relevant self-consistency variable if the mode must sustain its own angular momentum from its kinetic energy.

3. **A specific model of the internal structure** (Zitterbewegung with drift) where the $\beta^2$ arises from projecting the internal circulation onto the orbital plane.

---

## 6. Honest Assessment

### What Route A establishes

- The Casimir polynomial $u^2/(1-u) = C_2$ is stated to arise from relativistic standing-wave kinematics
- Standard relativistic circular orbit mechanics gives $u/(1-u) = C_2$ instead (one power of $u$ different)
- The discrepancy is exactly one factor of $\beta^2$, which requires an additional physical ingredient

### What Route A does NOT establish

- The extra factor of $\beta$ is not derived from PF axioms
- The connection stated in §6 of `g3_casimir_weinberg_angle.md` appears to contain an unstated assumption about the orbit radius or the self-consistency variable
- Without identifying this assumption, the de Broglie route does not close

### The precise remaining gap

The standard relativistic relation $\gamma\beta = \sqrt{C_2}$ gives:

$$u + C_2 u - C_2 = 0 \quad \text{(linear in } u \text{, wrong)}$$

The Casimir polynomial is:

$$u^2 + C_2 u - C_2 = 0 \quad \text{(quadratic in } u \text{, correct)}$$

The difference between these two is replacing the first $u$ with $u^2$. This requires an additional relation. Three candidate lemmas:

**Lemma candidate 1**: The self-consistency radius is $r = \beta \cdot \hbar/(mc)$, not $r = \hbar/(mc)$.

**Lemma candidate 2**: The relevant self-consistency variable is $pv/(mc^2) = \gamma\beta^2$, not $p/(mc) = \gamma\beta$.

**Lemma candidate 3**: The Casimir equation arises from a *different* physical setup than circular orbit mechanics — perhaps from a self-consistent mass equation or a propagator condition — and the de Broglie "derivation" in §6 of `g3_casimir_weinberg_angle.md` is actually a restatement, not a derivation.

---

## 7. Verdict

### Classification: Outcome C — Gap Reduction

Route A reduces the question from:

> "Why does PF produce $x^2 + C_2 x - C_2 = 0$?"

to the sharper:

> "In the PF's relativistic standing-wave picture, why is the self-consistency variable $\gamma\beta^2$ rather than $\gamma\beta$?"

This is a genuine reduction. The original question had no structural handle. The reduced question has a specific algebraic discrepancy (one extra factor of $\beta$) and three candidate lemmas that Codex can audit.

### What this means for the other routes

- **Claude's algebraic constraints route** should check whether the three uniqueness conditions (f₀=0, g₀=0, g₁=-f₁) select $u^2$ over $u$ in the first term
- **Codex's propagator route** may naturally produce the quadratic $u^2$ from a pole condition (propagator poles are typically quadratic in momentum)
- **Lumi's physical meaning route** should explain what $\gamma\beta^2 = pv/(mc^2)$ means as a PF primitive

### Honesty check

- I did not smuggle in a new axiom
- I found a real discrepancy between the claimed de Broglie derivation and standard relativistic mechanics
- The discrepancy is precisely located (one factor of $\beta$)
- I did not force a derivation where one does not exist
- The gap is smaller and sharper than where we started

---

*Cascade — 2026-03-21*
*Route A: Outcome C (gap reduction)*
*The polynomial is one factor of β away from standard relativistic mechanics.*
*The question is now: why γβ² and not γβ?*
