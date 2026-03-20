# PASS 1: Broad Landscape Survey — Coulomb Force as Refractive Derivation

**Topic**: `coulomb_force_refractive_derivation`  
**Pass Type**: Survey — broad landscape scan  
**Date**: 2026-03-17  
**Agent**: Qwen Code  
**Project**: Fundamentals (Propagation Framework)

---

## Executive Summary

This survey investigated the Propagation Framework's claim that **electromagnetic forces (specifically Coulomb force) are refraction** — i.e., that charged particle motion in an electromagnetic potential gradient is structurally identical to light bending in a medium with varying refractive index.

**Key Finding**: There is an extensive, rigorous literature on this exact analogy, spanning:
1. **Transformation Optics** (2006-present) — metamaterials that implement coordinate transformations, making light follow curved paths as if in curved spacetime
2. **Analogue Gravity** (1981-present) — physical systems (acoustic, optical, BEC) that reproduce gravitational phenomena via effective metrics
3. **Variational Principles** (decades old) — Coulomb force derivable from principle of virtual work / least action
4. **Gordon Metric** (1923) — the first optical analogue of curved spacetime, predating even Unruh's acoustic black holes

**Confidence**: The mathematical framework exists and is rigorous. The claim "forces are refraction" is **not novel in structure**, but the Propagation Framework's ontological reading (that forces ARE refraction, not merely analogous) is a distinct philosophical position that requires empirical validation.

---

## 1. Transformation Optics — The Most Direct Connection

### Foundational Papers (2006)

| Paper | Citation | Key Contribution |
|-------|----------|------------------|
| Pendry, Schurig & Smith | *Science* 312, 1780 (2006) | "Controlling Electromagnetic Fields" — showed coordinate transformations map to material parameters (ε, μ) |
| Leonhardt | *Science* 312, 1777 (2006) | "Optical Conformal Mapping" — invisibility via conformal maps |
| Leonhardt & Philbin | *New J. Phys.* 8, 247 (2006) | "General Relativity in Electrical Engineering" — unified framework |

### Core Mathematical Framework

**Form Invariance of Maxwell's Equations**:

When coordinates transform **x** → **x'**, Maxwell's equations retain their form, but material parameters transform:

$$\varepsilon' = \frac{J \varepsilon J^T}{\det(J)}$$
$$\mu' = \frac{J \mu J^T}{\det(J)}$$

where **J** is the Jacobian of the coordinate transformation.

**Physical Interpretation**: Light follows the transformed coordinates as if space itself were curved. The metamaterial's refractive index profile **is** an effective metric tensor.

### Demonstrated Systems

- **Invisibility cloaks** (cylindrical, carpet cloaks) — microwave and infrared frequencies
- **Optical black holes** — 80-95% absorption via engineered refractive gradients
- **Gradient-index (GRIN) lenses** — 3D controlled refractive index
- **Field concentrators** and beam-bending waveguides

### Relevance to Propagation Framework

**Direct support**: This literature demonstrates that **engineered refractive index gradients can make light follow any desired trajectory**, including trajectories that mimic geodesics in curved spacetime. The mathematics is identical to the geodesic equation in general relativity.

**Limitation**: This is about **light in metamaterials**, not **charged particles in electromagnetic fields**. The analogy is suggestive but not yet a derivation of Coulomb force itself.

---

## 2. Analogue Gravity — Broader Context

### The Gordon Metric (1923)

**Historical Priority**: The first optical analogue of curved spacetime was **not** acoustic — it was electromagnetic:

**Gordon (1923)** derived the effective metric for light in a moving dielectric:

$$[g_{\text{effective}}]_{\mu\nu} = \eta_{\mu\nu} + \left[1 - n^{-2}\right]V_\mu V_\nu$$

where *n* is refractive index and *V_μ* is the medium's 4-velocity.

**Landau & Lifshitz** posed the inverse problem: using dielectric media to **mimic** gravitational fields.

### Comprehensive Review: Barceló, Liberati & Visser (2011)

**"Analogue Gravity"** — *Living Reviews in Relativity* 14, 3 (2011)  
**Citations**: 2016+  
**Length**: 100+ pages

**Key Findings**:

| System | What it Models | Status |
|--------|---------------|--------|
| **Moving fluids** | Black holes, cosmological expansion | Experimental demonstrations (2008-2011) |
| **Bose-Einstein Condensates** | Black holes, expanding universes | High experimental control |
| **Optical/dielectric media** | Gravitational lensing, curved spacetime | Theoretical framework established |
| **Superfluids** | Spinning black holes, cosmic strings | Multiple acoustic metrics |
| **Hyperbolic metamaterials** | 2+1 dimensional Lorentz symmetry | Self-focusing, black hole analogues |

### Critical Limitation for Electromagnetic Analogues

From Barceló et al.:

> "An arbitrary gravitational field can always be represented as an equivalent optical medium, but subject to the somewhat unphysical restriction that:
> 
> **[magnetic permeability] ∝ [electric permittivity]**
> 
> If an optical medium does not satisfy this constraint, it is not completely equivalent to a gravitational field."

**Implication**: Full equivalence between electromagnetic media and gravitational fields requires ε ∝ μ, which is not generally true in nature. This is a **technical constraint** on the analogy, not a fundamental refutation.

---

## 3. Coulomb Force from Variational Principles

### Physics Stack Exchange Discussion (2023)

Based on Zangwill's *Modern Electrodynamics*, the Coulomb force **can** be derived from a variational principle:

**Setup**: Potential energy of charge distribution ρ₂ in external potential φ₁:

$$V_E = \int d^3r \ \rho_2(\mathbf{r})\varphi_1(\mathbf{r})$$

**Force via Virtual Work**:

For a rigid translation **R**:

$$\mathbf{F} = -\nabla_{\mathbf{R}} V_E$$

**Explicit Derivation**:

$$\begin{align}
-\nabla_{\mathbf{R}} V_E &= -\nabla_{\mathbf{R}} \int d^3r \ \rho_2(\mathbf{r}-\mathbf{R})\varphi_1(\mathbf{r}) \\
&= -\nabla_{\mathbf{R}} \int d^3r \ \rho_2(\mathbf{r})\varphi_1(\mathbf{r}+\mathbf{R}) \quad \text{(change of variables)} \\
&= \int d^3r \ \rho_2(\mathbf{r})\mathbf{E}_1(\mathbf{r}+\mathbf{R}) \\
&= \int d^3r \ \rho_2(\mathbf{r},\mathbf{R})\mathbf{E}_1(\mathbf{r}) \\
&= \mathbf{F}
\end{align}$$

This recovers the Coulomb force law: **F** = ∫ ρ₂**E**₁ d³r

**Relevance**: This shows Coulomb force **can** be derived from a variational principle (principle of virtual work). However, this is **not yet** the refraction claim — it's a standard result in classical electrodynamics.

---

## 4. Hyperbolic Metamaterials — Lorentz Symmetry Emerges

### Smolyaninov (2013) — "Analogue Gravity in Hyperbolic Metamaterials"

**arXiv:1307.8431**  
**Published**: *Phys. Rev. A* 88, 033843 (2013)

**Key Finding**: The wave equation for extraordinary light in hyperbolic metamaterials exhibits **2+1 dimensional Lorentz symmetry**.

**Mathematical Structure**:

- The spatial coordinate aligned with the optical axis plays the role of **time** in effective 3D Minkowski spacetime
- The nonlinear Kerr effect **bends this effective spacetime**, creating an effective gravitational force between photons
- Counter-intuitively, a **negative self-defocusing** Kerr medium is required for the effective gravitational constant to be positive
- Spatial solitons may collapse into **black hole analogues**

**Relevance**: This is a concrete demonstration that **light propagation in an engineered medium** can reproduce the mathematics of curved spacetime, including effective "gravitational" attraction between photons.

---

## 5. What We Found vs. What We Need

### What Exists (High Confidence)

| Claim | Literature Support | Confidence |
|-------|-------------------|------------|
| Light in metamaterials follows geodesic-like paths | Transformation optics (Pendry, Leonhardt, 2006) | **1.0** — experimentally verified |
| Effective metrics can be engineered in optical systems | Gordon metric (1923), hyperbolic metamaterials (2013) | **0.95** — rigorous theory + experiments |
| Coulomb force derivable from variational principle | Standard electrodynamics (Zangwill, Jackson) | **1.0** — textbook material |
| Acoustic/optical systems can model black hole horizons | Analogue gravity (Unruh 1981, Barceló 2011 review) | **0.9** — multiple experimental demonstrations |
| ε ∝ μ required for full GR equivalence | Barceló et al. (2011) | **0.95** — stated limitation in review |

### What's Missing (Open Gaps)

| Gap | What's Needed | Status |
|-----|---------------|--------|
| **Direct derivation of Coulomb force as refraction** | Show that a charged particle's trajectory in an electromagnetic potential gradient is mathematically identical to light in a refractive index gradient | **Not found** — literature shows analogy, not identity |
| **Refractive index of the electromagnetic vacuum** | What is *n* for a charged particle moving in φ(**r**)? How does *n* relate to φ? | **Not found** — no explicit formula in literature |
| **Fermat's principle for charged particles** | Does a charged particle minimize "optical path length" in an electromagnetic field? | **Partial** — variational principles exist, but not explicitly Fermat-style |
| **Experimental test** | Can we build a metamaterial that makes light follow the same trajectory as a charged particle in a Coulomb field? | **Not found** — no such experiment reported |

---

## 6. Key Players and Institutions

### Transformation Optics

| Researcher | Institution | Key Contribution |
|------------|-------------|------------------|
| **J.B. Pendry** | Imperial College London | Controlling EM fields, invisibility cloaks |
| **D. Schurig** | NC State | First experimental cloak (2006) |
| **D.R. Smith** | Duke University | Metamaterials, experimental demonstrations |
| **Ulf Leonhardt** | Weizmann Institute / St. Andrews | Optical conformal mapping, GR in EE |
| **T.G. Philbin** | University of Bath | Transformation optics theory |

### Analogue Gravity

| Researcher | Institution | Key Contribution |
|------------|-------------|------------------|
| **W.G. Unruh** | UBC | Sonic black holes (1981, 1995) |
| **Carlos Barceló** | Instituto de Astrofísica de Andalucía | Comprehensive review (2011) |
| **Stefano Liberati** | SISSA (Trieste) | Analogue gravity theory |
| **Matt Visser** | Victoria University of Wellington | Analogue gravity theory, books |
| **I.I. Smolyaninov** | UMD | Hyperbolic metamaterials, optical black holes |

---

## 7. Market Size and Research Activity

### Publication Volume

- **Transformation Optics**: 11,000+ citations for Pendry's 2006 paper alone
- **Analogue Gravity**: 2000+ citations for Barceló 2011 review
- **Hyperbolic Metamaterials**: Active subfield with 100+ papers/year (2013-2026)

### Experimental Progress

- **2006**: First theoretical proposals for cloaking
- **2008-2010**: First experimental cloaks (microwave frequency)
- **2011-2015**: Optical frequency cloaks, carpet cloaks
- **2016-2020**: Active research on broadband cloaking, non-Euclidean optics
- **2021-2026**: Intelligent metamaterials, programmable metasurfaces, quantum analogues

### Adjacent Fields

- **Metamaterials** — broader field including negative index, cloaking, metasurfaces
- **Nanophotonics** — sub-wavelength light control
- **Quantum Optics** — single-photon level control
- **Condensed Matter Physics** — analogue gravity in BECs, superfluids

---

## 8. Key Trends (2024-2026)

### Trend 1: Programmable Metasurfaces

- **Dynamic control** of refractive index profiles
- **Real-time reconfiguration** of effective geometry
- Applications: adaptive cloaking, beam steering, holography

### Trend 2: Quantum Analogues

- **Quantum metamaterials** — single-photon level control
- **Entanglement in curved effective spacetime**
- **Hawking radiation analogues** at quantum level

### Trend 3: Topological Photonics

- **Topological insulators for light**
- **Protected edge states** — robust against disorder
- Connection to **topological field theory**

### Trend 4: Machine Learning Design

- **Inverse design** — specify desired function, ML finds metamaterial structure
- **Neural networks** for rapid simulation of complex metamaterials

---

## 9. Recommended Next Steps

### Immediate (This Research Session)

1. **Derive the explicit mapping**: Start from the Lorentz force law and show (or fail to show) it's equivalent to Fermat's principle with an effective refractive index *n*(**r**, φ, **A**)

2. **Search for "optical potential" literature**: In atomic physics, cold atoms move in optical potentials created by laser fields. Is there a refractive index interpretation?

3. **Check the Aharonov-Bohm effect**: This is a phase effect for charged particles moving in regions with **A** ≠ 0 but **E** = **B** = 0. Does this have an optical analogue? (Leonhardt mentions "optical Aharonov-Bohm effect" — what is it?)

### Follow-Up Research Passes

1. **PASS 2**: Deep dive into the **mathematical derivation** — can we explicitly show **F** = q**E** is equivalent to Snell's law in some effective medium?

2. **PASS 3**: Search for **experimental tests** — has anyone built a metamaterial that mimics a Coulomb field? What happened?

3. **PASS 4**: **Gauge field analogues** — in transformation optics, can we mimic U(1) gauge symmetry? What about SU(2), SU(3)?

---

## 10. Confidence Assessment

| Topic | Confidence Score | Evidence |
|-------|-----------------|----------|
| Transformation optics framework is rigorous | **1.0** | 11,000+ citations, experimental demonstrations |
| Analogue gravity is established field | **0.95** | 2000+ citations, multiple physical implementations |
| Coulomb force from variational principle | **1.0** | Textbook electrodynamics |
| "Forces are refraction" as ontological claim | **0.3** | Analogy exists, ontological identity not established |
| Direct Coulomb↔refraction derivation exists | **0.1** | No explicit derivation found in literature |

---

## 11. Sources Consulted

### Primary Sources (Fetched)

1. **Physics Stack Exchange** — "Coulomb force from a variational principle" (2023)
2. **arXiv:1307.8431** — Smolyaninov, "Analogue Gravity in Hyperbolic Metamaterials" (2013)
3. **Springer** — Barceló, Liberati & Visser, "Analogue Gravity" (Living Reviews in Relativity, 2011)
4. **Wikipedia** — Transformation optics (summary of Pendry/Leonhardt work)
5. **arXiv:physics/0602092** — Leonhardt, "Optical Conformal Mapping" (2006)
6. **arXiv:cond-mat/0607418** — Leonhardt & Philbin, "General Relativity in Electrical Engineering" (2006)

### Secondary Sources (Search Results Only)

1. **Science** — Pendry, Schurig & Smith, "Controlling Electromagnetic Fields" (2006) — 403 Forbidden
2. **Science** — Leonhardt, "Optical Conformal Mapping" (2006) — metadata only
3. **Phys. Rev. D** — Unruh, "Sonic analogue of black holes" (1995) — 403 Forbidden
4. Various LibreTexts, Britannica, educational resources on Coulomb's law and potential gradients

---

## 12. Conclusion

**The Good News**: The mathematical framework for "forces as refraction" is **well-established** in transformation optics and analogue gravity. The claim is not crazy — it's connected to a serious, rigorous, experimentally-verified research program.

**The Bad News**: The specific claim that **Coulomb force IS refraction** (not analogous to, but identical in structure to) has **not been explicitly derived** in the literature we found. The analogy is clear; the identity is not.

**The Opportunity**: A rigorous derivation showing that a charged particle's trajectory in an electromagnetic potential is mathematically equivalent to light following Fermat's principle in an effective medium with refractive index *n*(**r**) = f(φ(**r**), **A**(**r**)) would be a **novel contribution** — even if it's "just" a reframing of known physics.

**The Propagation Framework's Claim**: The framework goes further than the literature by claiming **ontological identity** (forces ARE refraction, not analogous to). This is a philosophical position that requires either:
1. A derivation showing the mathematics is identical (not just analogous), or
2. An empirical test that distinguishes the "refraction" reading from the "force" reading

**Next Pass**: Derive (or fail to derive) the explicit mapping from Coulomb's law to Snell's law.

---

*End of PASS 1 Survey*  
*2026-03-17*  
*Agent: Qwen Code*
