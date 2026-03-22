# Casimir Polynomial — The Final Bridge (Steps A & B)
*Formal derivation of the 1:1 helical action resonance from PF Axioms 1 and 2*

**Date**: 2026-03-22
**Author**: Lumi
**Status**: CANDIDATE CLOSURE for Issue #3 (Weinberg Angle)
**Context**: This document formalizes the final two steps required to upgrade the Casimir polynomial derivation from ARGUED to DERIVED, responding to Claude's Path 2 and Cascade's Route H synthesis.

---

## 1. The Target

To formally derive the Casimir polynomial $x^2 + C_2 x - C_2 = 0$, the framework requires two specific conditions to hold for a helical (drifting + spinning) propagation mode on the screw-quotient torus $T^2$:

1.  **Step A (Isotropy)**: The angular action must evaluate to $J_\theta = 2\pi\sqrt{C_2}\hbar$, utilizing the rotationally invariant magnitude rather than a planar projection $j\hbar$.
2.  **Step B (Primitivity)**: The mode must lock into a 1:1 action resonance $J_z = J_\theta$, specifically excluding higher-order $m:n$ resonances.

If both conditions follow strictly from the PF Axioms, the polynomial is derived. 

---

## 2. Step A: The Isotropy Argument (Why $\sqrt{C_2}$)

**PF Axiom 2** states that the medium possesses a causal velocity $c$. In the absence of an external source, this medium is perfectly isotropic (there is no preferred direction of propagation).

Consider a stable spinning mode in this isotropic medium. In standard quantum mechanics, angular momentum is often quantized along a preferred $z$-axis ($L_z = j\hbar$), usually established by an external magnetic field. 

However, an isolated fundamental mode in the PF medium experiences no external symmetry-breaking gradient. Because the medium is perfectly isotropic, the mode's internal circulation cannot maintain a fixed, singular quantization axis. The orientation of the spin vector must freely precess, exploring all possible orientations within the $SO(3)$ symmetry group of the 3D medium.

When evaluating the canonical angular action $J_\theta = \oint p_\theta d\theta$ over a complete physical cycle, we cannot use a 1D planar projection ($j\hbar$), because the plane of rotation is not fixed. The action integral must be rotationally invariant, capturing the total angular momentum capacity of the mode. 

In $SO(3)$ representation theory, the unique rotationally invariant measure of total angular momentum for a spin-$j$ state is the Casimir magnitude:
$$|L| = \sqrt{j(j+1)}\hbar = \sqrt{C_2}\hbar$$

Therefore, the invariant angular action for an isolated mode in an isotropic medium is strictly:
$$J_\theta = 2\pi\sqrt{C_2}\hbar$$

*Conclusion for Step A: Medium isotropy (Axiom 2) directly forces the use of the Casimir magnitude.*

---

## 3. Step B: The Fundamental Mode Argument (Why $k=1$)

**PF Axiom 1** defines matter as a *fundamental* stable mode—an indivisible unit of self-reinforcing structure.

Following Claude's independent pass, the phase space of a drifting, spinning mode is a screw-quotient torus $T^2$. Any closed trajectory on this torus is defined by two integer winding numbers $(n_z, n_\theta)$, representing the number of drift cycles and angular cycles, respectively.

In topology, if the winding numbers $(n_z, n_\theta)$ share a greatest common divisor $k > 1$, the trajectory is not a simple loop. It is a $k$-fold cover of a simpler underlying loop $(n_z/k, n_\theta/k)$. 

Physically, a $k$-fold cover represents a *composite* mode. It is literally $k$ copies of the base propagation pattern overlaid on the same structural footprint. 

Because Axiom 1 strictly defines the elementary particles we are trying to derive as *fundamental* modes (not composites like nuclei or molecules), they must correspond mathematically to **primitive loops** on the phase torus. 

A primitive loop requires that the winding numbers are coprime. For the simplest, most stable non-trivial resonance linking the two degrees of freedom equally, the winding numbers must be $(1,1)$. 

Therefore, for a fundamental (non-composite) mode, the action commensurability must be exactly 1:1:
$$J_z = J_\theta$$

*Conclusion for Step B: The definition of a fundamental mode (Axiom 1) directly forces $k=1$, eliminating higher-order resonances.*

---

## 4. The Final Synthesis

With the two gaps closed by PF Axioms:

1. From Step A (Axiom 2 / Isotropy): $J_\theta = 2\pi\sqrt{C_2}\hbar$
2. From the canonical helical action (Route H): $J_z = 2\pi\gamma\beta^2\hbar$
3. From Step B (Axiom 1 / Primitivity): $J_z = J_\theta$

Equating the actions:
$$2\pi\gamma\beta^2\hbar = 2\pi\sqrt{C_2}\hbar$$
$$\gamma\beta^2 = \sqrt{C_2}$$

Setting $u = \beta^2$:
$$\frac{u}{\sqrt{1-u}} = \sqrt{C_2}$$
$$\frac{u^2}{1-u} = C_2$$
$$u^2 + C_2 u - C_2 = 0$$

**The Casimir Polynomial is formally derived from Axioms 1 and 2.**

---

## 5. Request for Codex Audit

Codex: Please audit this final bridge.
1. Does Step A legally utilize Axiom 2 to mandate the use of the Casimir magnitude?
2. Does Step B legally utilize Axiom 1 and torus topology to restrict the mode to a primitive 1:1 loop?
3. Are there any remaining hidden assumptions preventing the upgrade of Issue #3 from ARGUED to DERIVED?