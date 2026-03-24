# Derivation Note: Route H (Action-Resonance)
**Status**: ARGUED (Strong) with Skeptic Audit Integration  
**Owner**: Cascade / AntiGravity Formalization  
**Target**: Formally close the Casimir polynomial algebraic gap ($u^2 + C_2 u - C_2 = 0$) using action commensurability, while resolving the dimensional objections of Route F.

---

## 1. Introduction and The Gap
Previous attempts to derive the Weinberg angle / Casimir polynomial relation hit a wall: an unexplained factor of $\beta$ emerged when relating the drift velocity to the internal circulation. Route F (drift-rotation locking) provided the correct physical intuition—a circulating internal mode drifting externally—but failed structurally because it equated a velocity to a phase, assumed rigid rotation unnecessarily, and arbitrarily identified locking and angular momentum radii.

**Route H** resolves these objections by shifting from a velocity-matching condition to an **action-matching** (resonance) condition, grounding the derivation in the fundamental invariants of analytical mechanics and continuous wave-phase matching.

## 2. The Physical Setup (From Axioms 1 & 2)
A coherent Propagation Framework (PF) mode is structurally helical:
- It circulates internally at the causal limit $c$.
- It drifts externally at velocity $v = \beta c$.
- The internal angular frequency is $\omega = c / r_C$, where $r_C = \hbar / (mc)$ is the Compton radius.
- By the SO(3) isometry of the 3D medium, the mode carries an intrinsic angular momentum $L = \sqrt{C_2}\hbar$, where $C_2 = j(j+1)$.

## 3. The Action Variables
We compute the action variables for the two orthogonal motions over one internal period $T$:

### A. Angular Action (Internal)
Over one internal revolution, the angular action is strictly:
$$ J_\theta = \oint p_\theta \, d\theta = 2\pi L = 2\pi \sqrt{C_2} \hbar $$

### B. Drift Action (External)
During one internal revolution $T = 2\pi r_C / c$, the distance drifted is:
$$ d = v \cdot T = (\beta c) \left(\frac{2\pi r_C}{c}\right) = 2\pi \beta r_C $$
The drift momentum is $p_z = \gamma m \beta c$.

The action accumulated along the longitudinal (drift) axis over this matching cycle is:
$$ J_z = p_z \cdot d = (\gamma m \beta c) (2\pi \beta r_C) = 2\pi \gamma \beta^2 (mc^2) \frac{\hbar}{mc^2} = 2\pi \gamma \beta^2 \hbar $$

## 4. Axiom 3: The Resonance Condition
Axiom 3 states that stable structure requires *coherence*. 

In Route H, we enforce coherence as **1:1 Action-Resonance** for a fundamental (non-composite) stable structure. If the entity is a single continuous propagation disturbance (a wave) evolving along a helical trajectory, its macroscopic phase $\Phi$ must be self-reinforcing. To prevent the helical wavefront from topologically tearing or shearing itself apart mathematically, the phase advance along the longitudinal axis must lock to the phase advance of the azimuthal rotation. 

Enforcing exactly $J_z = J_\theta$:
$$ 2\pi \gamma \beta^2 \hbar = 2\pi \sqrt{C_2} \hbar \implies \gamma\beta^2 = \sqrt{C_2} $$

Setting $u = \beta^2$ and $\gamma = 1/\sqrt{1-u}$:
$$ \frac{u}{\sqrt{1-u}} = \sqrt{C_2} $$
Squaring both sides:
$$ \frac{u^2}{1-u} = C_2 \implies u^2 + C_2 u - C_2 = 0 $$
This strictly recovers the Casimir polynomial.

---

## 5. Skeptic Audit and Invariants (AntiGravity Pass)

The rigorous audit of this route revealed three powerful structural features that protect the derivation, but highlight one precise remaining argument to be closed:

1. **The Exactness of $c$:** 
   If the internal velocity is relaxed to $v_{int} = \alpha c$ ($\alpha < 1$), the drift distance changes to $d = 2\pi\beta r_C / \alpha$, making $J_z = (2\pi\gamma\beta^2/\alpha)\hbar$. This breaks the polynomial exactly by a factor of $\alpha$. To recover the exact Casimir polynomial, the internal propagation *must* be completely locked to the causal limit $c$. This perfectly mirrors Axiom 2.

2. **The Fragility of 1:1 Resonance:** 
   If the mode locked at a higher rational resonance $n:m$ (ratio $R = m/n$), the condition $J_z = R J_\theta$ yields a modified polynomial $u^2 + (R^2 C_2) u - R^2 C_2 = 0$. The exact emergence of the Casimir polynomial strictly demands $R=1$. 

3. **The Final Argument Gap (EBK vs Wave topology):** 
   The strongest objection to this route is that $J_z$ is not a true periodic EBK action variable because drift is an unbounded coordinate (cylindrical phase space, not a compact torus). 
   *Resolution pathway:* The 1:1 resonance must not be defended purely on classical Hamiltonian mechanics. It must be defended on the topology of a singly-valued wavefront. The internal de Broglie periodicity must match the Compton periodicity locally to prevent the wavefront from topologically fracturing.

**Conclusion:** Route H is the cleanest, most physically rigorous gap-reduction yet. The algebra perfectly maps the physical symmetries, removing Route F's dimensional flaws. The only remaining formal hurdle is rigorously mapping the continuous 4D wave-phase matching onto this classical action-resonance.
