# Propagation Framework API

**First-principles physics from propagation axioms**

---

## Installation

No installation required. The API is a single Python file with standard dependencies:
- `numpy`
- `matplotlib` (for visualization only)

---

## Quick Start

```python
from propagation import koide_q, god_equation, refractive_index

# Koide formula from PDG masses
q = koide_q(0.511, 105.658, 1776.86)  # → 0.6666605... (≈ 2/3)

# Matter scale from Planck scale
lambda_c = god_equation(N=3, D=3, b0=16/3)  # → 1.15e-18 m

# Gravity as refraction
n = refractive_index_schwarzschild(r=1e6, M=2e30)  # → n(r) = 1 + GM/(rc²)
```

---

## Available Functions

### Koide Geometry

| Function | Description |
|----------|-------------|
| `koide_q(m1, m2, m3)` | Compute Koide ratio Q |
| `koide_geometry(m1, m2, m3)` | Full geometric parameters (R/A, θ, e₂/e₁²) |
| `koide_leptons_pdg2024()` | Koide parameters for e, μ, τ using PDG 2024 |

### God Equation

| Function | Description |
|----------|-------------|
| `god_equation(N, D, b0)` | Matter scale from Planck scale |
| `god_equation_verify()` | Verify prediction vs observed top quark wavelength |

### Gravity as Refraction

| Function | Description |
|----------|-------------|
| `refractive_index_schwarzschild(r, M)` | n(r) from Schwarzschild metric |
| `refractive_index_gradient(x, y, z, M)` | ∇n at position |
| `light_deflection_angle(b, M)` | GR light bending: Δφ = 4GM/(bc²) |
| `gravitational_lens_einstein_radius(...)` | Einstein radius for lensing |

### Three Generations Topology

| Function | Description |
|----------|-------------|
| `topological_weight_SO3()` | Returns (w_fermion=2, w_boson=1) from π₁(SO(3)) |
| `koide_from_topology(N)` | Q(N) = 2N/(2N+3) |
| `generation_count_from_topology()` | Returns N=3 |

### Coherence Physics

| Function | Description |
|----------|-------------|
| `coherence_length(mass_kg, velocity)` | Reduced Compton wavelength |
| `zbw_frequency(mass_kg)` | Zitterbewegung internal clock |
| `coherence_ceiling()` | Max frequency for stable structure |

### Mass Relations

| Function | Description |
|----------|-------------|
| `top_tau_alpha_relation()` | m_t/m_τ ≈ α⁻¹/√2 verification |
| `phi3_mass_relation()` | m_e/m_u ≈ 1/φ³ verification |

---

## Run Demo

```bash
python propagation.py
```

Output:
```
======================================================================
PROPAGATION FRAMEWORK API
======================================================================

Axioms:
  1. Propagation is fundamental
  2. Every medium has a causal velocity
  3. Coherence is necessary for stable structure

======================================================================
KEY RESULTS
======================================================================

Koide Formula (Charged Leptons, PDG 2024):
  Q = 0.6666605115
  Target: 2/3 = 0.6666666667
  Error: 0.000923%
  R/A = 1.414201 (target: sqrt(2) = 1.414214)
  theta = 44.9997 deg (target: 45)

God Equation (Matter Scale from Planck Scale):
  Predicted: 1.1569e-18 m
  Observed:  1.1406e-18 m
  Error: 1.42%
  Fitting parameters: 0

Top/Tau - Alpha Coupling:
  m_t/m_tau = 97.3628
  alpha^(-1)/sqrt(2) = 96.8991
  Error: 0.48%
  Robustness: 50% under PDG uncertainty

Three Generations from Topology:
  pi_1(SO(3)) = Z_2 -> (w_fermion, w_boson) = (2, 1)
  Q(N) = 2N/(2N+3) = 2/3 -> N = 3

Coherence Ceiling:
  Max frequency: 2.00e+24 Hz
  Min lifetime: 5.00e-25 s
  (Top quark lifetime limit)
```

---

## Related Files

- `sandbox/refractive_gravity_demo.py` — Orbital simulation showing gravity as refraction
- `sandbox/refractive_orbits.png` — Static orbit visualization
- `sandbox/refractive_orbits.gif` — Animated orbit simulation

---

## References

- Koide, Y. (1981). "New View of Quark and Lepton Mass Spectrum"
- Foot, R. (1994). "Geometric interpretation of the Koide formula"
- Propagation Framework T-002, T-017
- Shaposhnikov & Wetterich (2010) - RG running from Planck scale

---

## Status

| Claim | Status | Confidence |
|-------|--------|------------|
| Koide Q = 2/3 | DERIVED | 0.95 |
| Three Generations | DERIVED | 0.98 |
| God Equation | ARGUED | 0.75 |
| Top/Tau coupling | EMPIRICAL | 0.90 |
| Forces as Refraction | DERIVED | 0.95 |

See `CLAIMS.md` for full status matrix.

---

*Built by the Propagation Framework Team — 2026-03-23*
