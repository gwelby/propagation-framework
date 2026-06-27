# Casimir Axiom 3 — Lemma 2 Energy Partition Exploration
*Bounded target: Can any of the three candidate resolutions close the extra-β gap?*

**Date**: 2026-06-16
**Author**: Devin ∇λΣ∞
**Scope**: Route A Lemma 2 (kinetic power balance) — systematic exploration of the three candidate resolutions identified in `casimir_polynomial_synthesis.md`
**Authority**: `casimir_polynomial_route_A.md`, `casimir_polynomial_synthesis.md`
**Status**: EXPLORATION — not a claim closure

---

## 1. The Extra-β Gap (Restated)

Standard relativistic circular orbit mechanics at Compton radius $r_C = \hbar/(mc)$:

$$L = \gamma m v r_C = \gamma\beta \hbar$$

Matching to quantum angular momentum $|L| = \sqrt{j(j+1)}\hbar = \sqrt{C_2}\hbar$:

$$\gamma\beta = \sqrt{C_2} \implies \frac{\beta^2}{1-\beta^2} = C_2 \implies \frac{u}{1-u} = C_2$$

where $u = \beta^2$.

The **Casimir polynomial** requires:

$$\gamma\beta^2 = \sqrt{C_2} \implies \frac{\beta^4}{1-\beta^2} = C_2 \implies \frac{u^2}{1-u} = C_2$$

The discrepancy is exactly one factor of $\beta$ (equivalently, $u$ vs $u^2$ in the numerator).

Route A's **Lemma 2** reformulates this as: the self-consistency condition involves the **kinetic power** $pv = \gamma\beta^2 mc^2$ rather than momentum $p = \gamma\beta mc$. The power balance equation contains a $-\beta^2$ term that must vanish for the polynomial to close.

This document systematically tests the three candidate resolutions.

---

## 2. Candidate Resolution 1: High-Velocity Approximation ($\beta \to 1$)

### Claim
For $\beta \approx 1$, the extra factor of $\beta$ is approximately 1, so $\gamma\beta \approx \gamma\beta^2 \approx \gamma$. The linear and quadratic forms become indistinguishable.

### Test
For the physical root of the Casimir polynomial with $C_2 = 3/4$ (spin-$\tfrac{1}{2}$):

$$\frac{u^2}{1-u} = \frac{3}{4} \implies u^2 + \frac{3}{4}u - \frac{3}{4} = 0$$

Positive root:
$$u = \frac{-3/4 + \sqrt{9/16 + 3}}{2} = \frac{-0.75 + \sqrt{2.8125}}{2} = \frac{-0.75 + 1.677}{2} = 0.4635$$

So $\beta = \sqrt{u} = \sqrt{0.4635} = 0.681$.

At $\beta = 0.681$:
- $\gamma = 1/\sqrt{1 - 0.4635} = 1/\sqrt{0.5365} = 1/0.732 = 1.366$
- $\gamma\beta = 1.366 \times 0.681 = 0.930$
- $\gamma\beta^2 = 1.366 \times 0.4635 = 0.634$
- $\sqrt{C_2} = \sqrt{0.75} = 0.866$

Now compare:
- Linear prediction: $\gamma\beta = 0.930$ vs target $\sqrt{C_2} = 0.866$ → **error: +7.4%**
- Quadratic prediction: $\gamma\beta^2 = 0.634$ vs target $\sqrt{C_2} = 0.866$ → **error: -26.8%**

Wait — the quadratic prediction gives $0.634 \neq 0.866$. Let me recalculate.

Actually, if $\gamma\beta^2 = \sqrt{C_2}$ is the defining relation, then by construction it holds. Let me verify:

$\gamma\beta^2 = 1.366 \times 0.4635 = 0.634$

But $\sqrt{C_2} = 0.866$. These are not equal!

There must be an error. Let me recalculate from the polynomial.

If $u^2/(1-u) = C_2$, then $u^2 = C_2(1-u)$, so $u^2 + C_2 u - C_2 = 0$.

For $C_2 = 3/4$: $u^2 + 0.75u - 0.75 = 0$.

Roots: $u = \frac{-0.75 \pm \sqrt{0.5625 + 3}}{2} = \frac{-0.75 \pm \sqrt{3.5625}}{2} = \frac{-0.75 \pm 1.888}{2}$

Positive root: $u = (-0.75 + 1.888)/2 = 1.138/2 = 0.569$

Then $\beta = \sqrt{0.569} = 0.754$.

$\gamma = 1/\sqrt{1 - 0.569} = 1/\sqrt{0.431} = 1/0.656 = 1.524$

$\gamma\beta^2 = 1.524 \times 0.569 = 0.867 \approx \sqrt{0.75} = 0.866$ ✓

$\gamma\beta = 1.524 \times 0.754 = 1.149$

Now compare at $\beta = 0.754$:
- The extra-β factor: $\beta = 0.754$ — this is **not** close to 1.
- $\gamma\beta = 1.149$ would predict $\sqrt{C_2} = 1.149$ (error +32.7%)
- $\gamma\beta^2 = 0.867$ correctly predicts $\sqrt{C_2} = 0.866$ (error <0.1%)

### Verdict for Resolution 1

**NO-GO** — $\beta = 0.754$ is not in the high-velocity regime where $\beta \approx 1$. The extra factor of $\beta = 0.754$ is significant (25% difference from 1). The polynomial root is at an intermediate velocity where the $\beta$ factor cannot be approximated away.

For $C_2 = 2$ (spin-1): $u = (-2 + \sqrt{4+8})/2 = (-2 + 3.464)/2 = 0.732$, $\beta = 0.856$. Here $\beta$ is closer to 1, but still $\beta = 0.856 \neq 1$.

For $C_2 = 6$ (spin-2): $u = (-6 + \sqrt{36+24})/2 = (-6 + 7.746)/2 = 0.873$, $\beta = 0.935$. Here $\beta \approx 0.935$ is closer to 1, but still a 6.5% correction.

The high-velocity approximation works progressively better for higher spin, but it is never exact, and for the physically relevant case $j = 1/2$ (the fermion case), it fails by 25%.

---

## 3. Candidate Resolution 2: Quantum Correction to Energy Density

### Claim
The $-\beta^2$ term in the power balance might be canceled by a quantum correction to the energy density of the self-reinforcing mode.

### Setup
For a relativistic quantum particle in a circular orbit, the energy-momentum tensor has quantum fluctuations. The expectation value of the energy density in a coherent state includes quantum corrections:

$$\langle T_{00} \rangle = \frac{E}{V} + \delta T_{00}^{\text{(quantum)}}$$

For a mode of frequency $\omega$ in a volume $V$, the zero-point energy correction is $\hbar\omega/2V$.

For the Zitterbewegung internal motion: $\omega = mc^2/\hbar$, so:

$$\frac{\hbar\omega}{2V} = \frac{mc^2}{2V}$$

If the mode occupies a spherical volume of radius $r_C = \hbar/(mc)$:

$$V = \frac{4\pi}{3} r_C^3 = \frac{4\pi}{3} \frac{\hbar^3}{m^3c^3}$$

The zero-point energy density:

$$\delta T_{00} = \frac{mc^2}{2} \cdot \frac{3m^3c^3}{4\pi\hbar^3} = \frac{3m^4c^5}{8\pi\hbar^3}$$

Compare to the classical energy density:

$$T_{00}^{\text{(classical)}} = \frac{\gamma mc^2}{V} = \frac{3\gamma m^4c^5}{4\pi\hbar^3}$$

The ratio:

$$\frac{\delta T_{00}}{T_{00}^{\text{(classical)}}} = \frac{3/8}{3\gamma/4} = \frac{1}{2\gamma}$$

For $\gamma = 1.524$ (the spin-$\tfrac{1}{2}$ root): this ratio is $1/(2 \times 1.524) = 0.328$.

So the quantum correction is about 33% of the classical energy density — significant, but does it introduce a $+\beta^2$ term?

### Analysis
The quantum correction to the energy density is proportional to $mc^2/V$, which is independent of $\beta$. It does not have the right velocity dependence to cancel a $-\beta^2$ term.

For the cancellation to work, we would need a quantum correction proportional to $\beta^2$ (or $u = \beta^2$). But the zero-point energy of the internal mode is determined by its rest mass, not by its orbital velocity.

### Alternative: de Broglie phase quantization
If the quantum correction comes from requiring an integer number of de Broglie wavelengths around the orbit, the condition is:

$$2\pi r = n\lambda_{dB} = n\frac{h}{\gamma mv}$$

This gives $r = n\hbar/(\gamma m\beta c)$, so:

$$L = \gamma m\beta c \cdot r = n\hbar$$

For $n = 1$: $L = \hbar$, so $C_2 = 1$, which is wrong for $j = 1/2$.

For $n = \sqrt{C_2}$: not an integer. The de Broglie quantization with integer $n$ does not reproduce the correct angular momentum.

### Verdict for Resolution 2

**NO-GO** — The quantum corrections considered (zero-point energy, de Broglie quantization) do not introduce a velocity-dependent term with the correct $\beta^2$ dependence to cancel the $-\beta^2$ term in the power balance. The zero-point energy is independent of $\beta$, and de Broglie quantization with integer $n$ gives the wrong angular momentum.

---

## 4. Candidate Resolution 3: Different Energy Partition (Total vs Kinetic Energy)

### Claim
The power balance should use **total energy** $E = \gamma mc^2$ rather than **kinetic energy** $K = (\gamma - 1)mc^2$ in the self-consistency condition.

### Setup
The standard power balance for a circular orbit uses kinetic energy. But for a self-reinforcing propagation pattern (Axiom 1 + Axiom 3), the total energy (including rest energy) might be the relevant quantity because the mode's persistence involves sustaining its entire energy content, not just the kinetic part.

If the self-consistency condition involves total energy:

$$\frac{E \cdot v}{mc^2 \cdot c} = \frac{\gamma\beta mc^2}{mc^2} = \gamma\beta$$

This just returns the standard result — no extra $\beta$.

But if the condition involves the **energy flux** or **power delivered by the total energy in circulation**:

For a mode circulating at velocity $v$ on a circle of radius $r_C$:
- Circulation frequency: $\omega = v/r_C = \beta c / r_C = \beta mc^2/\hbar$
- The total energy circulates with this frequency.
- The "power" associated with this circulation is $E \cdot \omega / (2\pi)$ (energy per cycle).

For one complete cycle:
$$\text{Energy per cycle} = E = \gamma mc^2$$

This doesn't introduce $\beta^2$.

### Alternative: Kinetic power from relativistic force
The relativistic centripetal force for circular motion:

$$F = \frac{\gamma mv^2}{r} = \frac{\gamma\beta^2 mc^2}{r}$$

The power delivered by this force is:

$$P = F \cdot v = \frac{\gamma\beta^3 mc^3}{r} = \gamma\beta^3 \frac{m^2c^4}{\hbar}$$

(using $r = r_C = \hbar/(mc)$).

The self-consistency condition $P / P_0 = \sqrt{C_2}$ with $P_0 = mc^2 \cdot c/r_C = m^2c^4/\hbar$ gives:

$$\gamma\beta^3 = \sqrt{C_2}$$

This has $\beta^3$ — one power too many!

### Alternative: Angular momentum flux
The angular momentum flux (torque) is:

$$\tau = F \cdot r = \gamma\beta^2 mc^2$$

Dividing by $mc^2$:

$$\frac{\tau}{mc^2} = \gamma\beta^2$$

This is exactly the desired quantity!

### Interpretation
If the self-consistency condition is that the **torque** (angular momentum flux) generated by the internal circulation equals the quantum angular momentum content, then:

$$\frac{\tau}{mc^2} = \sqrt{C_2} \implies \gamma\beta^2 = \sqrt{C_2}$$

The torque is $\tau = F \cdot r = \gamma mv^2 = \gamma\beta^2 mc^2$.

For the standard angular momentum $L = \gamma mvr = \gamma\beta\hbar$, the torque is $\tau = L \cdot \omega = \gamma\beta\hbar \cdot (\beta c/r_C) = \gamma\beta^2 mc^2$.

So the torque naturally has the extra factor of $\beta$ compared to angular momentum.

### But is this derived from PF axioms?

The torque argument shows that $\gamma\beta^2$ arises naturally if the self-consistency condition involves torque rather than angular momentum. But PF Axioms 1-3 do not explicitly mention torque.

However, Axiom 3 says "coherent propagation persists." For a rotating mode to persist, it must continually generate angular momentum against dissipation. The rate of angular momentum generation is torque. So torque is the natural PF quantity for sustained rotation.

### Verdict for Resolution 3

**PARTIAL GAP REDUCTION** — Using torque (angular momentum flux) instead of angular momentum gives the correct extra factor of $\beta$. This is physically natural: Axiom 3 is about persistence, which is a rate (torque), not a static quantity (angular momentum).

However, this is still a **reformulation**, not a full derivation from Axioms 1-3. The PF axioms do not explicitly state that the self-consistency variable must be torque rather than angular momentum.

What would make this a DERIVED result:
- A theorem from Axioms 1-3 that the self-consistency condition for a sustained coherent rotation must involve the generation rate (torque) rather than the static quantity (angular momentum).

---

## 5. Cross-Route Synthesis

| Resolution | Result | Notes |
|---|---|---|
| 1. High-velocity approx | **NO-GO** | $\beta = 0.754$ for $j=1/2$; approximation fails by 25% |
| 2. Quantum correction | **NO-GO** | Zero-point energy is $\beta$-independent; de Broglie quantization gives wrong $C_2$ |
| 3. Energy partition (torque) | **PARTIAL** | Using torque $\tau = F \cdot r$ naturally gives $\gamma\beta^2$; physically motivated by Axiom 3 (persistence = rate) |

The torque reformulation (Resolution 3) is the strongest result. It parallels Route H's finding that the drift phase advance per internal cycle $N_{dB} = \gamma\beta^2$ is the cleanest helical reformulation of the extra-$\beta$ gap.

---

## 6. The Remaining Gap

Resolution 3 reduces the extra-$\beta$ gap to a sharper question:

> **Can Axioms 1-3 be shown to require that the self-consistency condition for a sustained coherent rotation uses the angular momentum generation rate (torque) rather than the static angular momentum?**

This is equivalent to asking: in the PF, is the fundamental dynamical variable for persistent structure a **rate** (power, torque, current) or a **state** (energy, angular momentum, charge)?

Axiom 3 says "coherent propagation persists" — this is a **process** statement, not a **state** statement. Therefore, the PF naturally privileges rates over states for self-consistency conditions.

This suggests a PF-native argument for the extra-$\beta$ factor, but it is not yet a formal derivation.

---

## 7. Honest Assessment

### What this exploration establishes
- All three candidate resolutions have been systematically tested.
- Resolution 3 (torque/energy partition) is the only one that naturally produces the extra-$\beta$ factor.
- The torque argument has a clear physical motivation from Axiom 3 (persistence as a process).

### What this exploration does NOT establish
- A formal derivation from Axioms 1-3 that the self-consistency variable must be torque.
- A mathematical theorem closing the extra-$\beta$ gap.
- An independent derivation of the Casimir polynomial without Axiom 3b.

### The precise remaining gap
> Can the statement "coherent propagation persists" (Axiom 3) be sharpened into a quantitative principle that selects torque-based self-consistency over angular-momentum-based self-consistency for rotating modes?

---

*Devin ∇λΣ∞ — 2026-06-16*
*Route A Lemma 2: Three candidate resolutions tested; Resolution 3 (torque) is the strongest partial result.*