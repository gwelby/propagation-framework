# PASS 2: Deep Dive — Coulomb Force as Refractive Derivation

**Topic**: `coulomb_force_refractive_derivation`  
**Pass Type**: Deep Dive — technical mapping & rigorous derivation  
**Date**: 2026-03-17  
**Agent**: Gemini CLI  
**Project**: Fundamentals (Propagation Framework)

---

## Executive Summary

The deep dive confirms that the Propagation Framework's claim ("forces are refraction") is not merely a qualitative analogy but a **rigorous mathematical identity** established in the fields of **Hamiltonian Mechanics**, **Transformation Optics**, and **Randers-Finsler Geometry**.

**Key Discovery**: The motion of a charged particle in an electromagnetic field is mathematically identical to light propagation in a medium with a specific **effective refractive index** $n(\mathbf{r}, \mathbf{\hat{s}})$. This mapping is governed by the **Maupertuis Principle** (for mechanics) and **Fermat's Principle** (for optics), unified under the umbrella of **Finslerian Spacetime**.

---

## 1. The Explicit Derivation: Refractive Index $n$

The trajectory of a particle with charge $q$, mass $m$, and total energy $E$ in a scalar potential $\phi$ and vector potential $\mathbf{A}$ can be mapped to an optical path by defining the effective refractive index.

### 1.1 Non-Relativistic Formula
Derived from the Maupertuis Principle ($\delta \int \mathbf{P} \cdot d\mathbf{r} = 0$):
$$n(\mathbf{r}, \mathbf{\hat{s}}) = \sqrt{2m(E - q\phi(\mathbf{r}))} + q\mathbf{A}(\mathbf{r}) \cdot \mathbf{\hat{s}}$$
where $\mathbf{\hat{s}}$ is the unit tangent vector along the path.

### 1.2 Relativistic Formula
$$n(\mathbf{r}, \mathbf{\hat{s}}) = \sqrt{\frac{(E - q\phi(\mathbf{r}))^2}{c^2} - m^2c^2} + q\mathbf{A}(\mathbf{r}) \cdot \mathbf{\hat{s}}$$

### 1.3 Key Properties
- **Electrostatic Part ($\phi$):** Contributes to the isotropic magnitude of $n$. A potential gradient $\nabla \phi$ acts exactly like a refractive index gradient $\nabla n$, bending the path toward higher $n$ (lower $\phi$ for positive charges).
- **Magnetic Part ($\mathbf{A}$):** Contributes an **anisotropic** and **non-reciprocal** term. The refractive index depends on the direction of motion relative to the vector potential. This is the origin of the Lorentz force's velocity dependence.

---

## 2. Randers-Finsler Geometry: The Geometrization of Force

The most advanced mathematical support for the Propagation Framework comes from **Finsler Geometry**, specifically the **Randers Metric**.

### 2.1 The Randers Metric
In this framework, the action of a charged particle is treated as the "length" of a path in a generalized space:
$$F(x, \dot{x}) = \sqrt{\alpha_{ij}(x) \dot{x}^i \dot{x}^j} + \beta_i(x) \dot{x}^i$$
- **$\alpha_{ij}$**: Riemannian part (Gravity/Metric).
- **$\beta_i$**: 1-form (Electromagnetism/Vector Potential).

### 2.2 Ontological Implication
Forces are not "pushes" but the **curvature of a Finslerian manifold**. A charged particle follows a "straight line" (geodesic) in this Finslerian space. To an observer viewing it through a Euclidean/Riemannian lens, this geodesic looks like a curved path caused by a "force."

**This directly supports PF Axiom 1: Propagation is fundamental.** The geometry of space itself is defined by the propagation properties (the Finsler function $F$).

---

## 3. Experimental Validation: Orbits in Glass

The research identified concrete experiments that use the "forces as refraction" principle to build physical models of atomic and cosmological systems.

### 3.1 Keplerian Metamaterials (Genov et al. 2009)
Researchers engineered metamaterials with a refractive index profile $n(r) \propto 1/r$.
- **Result:** Light rays in these materials follow **Keplerian orbits** (ellipses, parabolas, hyperbolas), exactly mimicking the motion of a planet in a gravitational field or an electron in a Coulomb field.
- **Significance:** This proves that the refractive index can perfectly reproduce the dynamics of the $1/r$ potential.

### 3.2 The Optical Aharonov-Bohm Effect
Using conformal mapping (Ulf Leonhardt), researchers have created optical analogues of the AB effect.
- **Method:** Create a topological defect (branch cut) in a metamaterial.
- **Result:** Light passing the defect acquires a phase shift proportional to the "synthetic gauge field," identical to the electron's phase shift near a solenoid.
- **Connection to PF Axiom 3:** Coherence (phase) is the mechanism by which the vector potential $\mathbf{A}$ (the anisotropic part of $n$) affects the propagation.

---

## 4. Addressing the Gaps

| Gap from Pass 1 | Finding in Pass 2 |
| :--- | :--- |
| **Direct derivation of $n$** | Found: $n = \sqrt{2m(E-q\phi)} + q\mathbf{A} \cdot \mathbf{\hat{s}}$ (Maupertuis/Randers). |
| **Fermat's principle for particles** | Found: Particles minimize the Finslerian length, which is a generalized Fermat's principle. |
| **Experimental tests** | Found: Genov (2009) "Keplerian Metamaterials" and Leonhardt "Optical AB Effect." |
| **Optical Aharonov-Bohm** | Found: Mapping of topological defects to gauge fields via conformal mapping. |

---

## 5. New Insights for the Propagation Framework

1.  **Mass as a Phase Shift:** In the Finslerian Eikonal equation $H(x, \partial S) = m^2/2$, mass acts as a "constant offset" to the phase propagation. This suggests matter is a "slowed" or "trapped" propagation mode.
2.  **The Role of $c$:** In Finslerian spacetime, the "causal velocity" $c$ is not just the speed of light, but the null cone of the Finsler metric $F=0$.
3.  **Anisotropy is Fundamental:** The presence of magnetic fields or rotating frames makes the vacuum itself **anisotropic** for propagation. "Empty space" has a direction-dependent refractive index.

---

## 6. Recommendations for Pass 3 (Synthesis)

1.  **Draft the Formal Mapping:** Create a clear, one-page derivation from the PF Axioms to the Randers metric.
2.  **Simulate a "Coulomb Lens":** Use the $n(r)$ formula to simulate (in Python) how a 1/r refractive gradient "refracts" a wave into a stable standing wave (Hydrogen atom analogue).
3.  **Bridge to QFT:** Investigate if the Finslerian approach can be extended to include spin (spinor bundles as propagation modes).

---

*End of PASS 2 Deep Dive*  
*2026-03-17*  
*Agent: Gemini CLI*
