# Forces
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md` Derived Quantity 4*
*Audit: `derivations/forces_definition_final_audit_2026-04-29.md`; prior audit: `forces_as_refraction_audit_2026-03-27.md`; prior pre-dispatch packet superseded: `derivations/forces_pre_dispatch_audit_2026-04-29.md`*
*Dependencies: `field.md` CANONICAL v1.0; `mode.md` CANONICAL v1.0; `energy.md` CANONICAL v1.0; `matter.md` CANONICAL v1.0; `causal_velocity.md` CANONICAL v1.0*
*Related definitions: `coupling.md`, `gradient.md`, `information.md` CANONICAL v1.0*

---

## The Definition

**A force is an interaction that changes a mode's momentum, trajectory, phase, internal quantum numbers, or field configuration.**

In standard physics, forces are encoded by two structures:
1. **Spacetime geometry** (gravity): geodesic deviation from curved spacetime metric.
2. **Gauge fields** (EM, strong, weak): minimal coupling via gauge-covariant derivatives.

The Propagation Framework interprets these structures as gradients or properties of the Medium. Each force requires a separate domain-specific derivation; the program of framing all forces as Medium-property gradients is the PF research program, not a single canonical claim.

Plain language (not the formal definition):

> Forces are what the Medium's structure does to modes moving through it.

---

## Force-by-Force Account

### Gravity

**Standard account:** A massive object curves the spacetime metric. All other modes — massive and massless — follow geodesics of the curved metric. The geodesic equation is:

```text
d²x^μ/dλ² + Γ^μ_{νρ} (dx^ν/dλ)(dx^ρ/dλ) = 0
```

where `Γ^μ_{νρ}` are the Christoffel symbols of the metric `g_{μν}` and `λ` is an affine parameter. For timelike geodesics, `λ` may be chosen as proper time `τ`; for null geodesics, proper time is zero and an affine parameter must be used. This is the standard result of general relativity.

**Optical/Fermat connection (established, restricted domain):**

For **null geodesics** (`g_{μν} dx^μ dx^ν = 0`) in **static or stationary spacetimes**, the geodesic equation can be expressed as a Fermat-type variational principle applied to the optical geometry:

```text
δ ∫ n_opt(x) ds = 0
```

In static isotropic cases this can be written using a scalar effective optical refractive index `n_opt(x) = c / v_coord(x)`. In stationary cases with frame-dragging, the optical geometry is generally Randers/Finsler rather than a scalar refractive index. This is an established result in GR for light paths, but it is domain-restricted.

**Massive particle geodesics (separate construction):**

For timelike geodesics, optical Fermat's principle does not directly apply. Jacobi/Maupertuis-type variational constructions exist only under additional restrictions such as fixed energy and stationary/static backgrounds. In the Newtonian limit, the spatial path can be written schematically as:

```text
δ ∫ √(2m(E − V_grav)) ds = 0
```

but this is not the optical metric and is not the general GR timelike-geodesic law. The reliable canonical statement is: massive particles follow timelike geodesics of `g_{μν}`; their spatial path can sometimes be reformulated by a separate Jacobi/Maupertuis construction. These two cases must not be conflated.

**Causal-velocity note:** The fundamental causal velocity `c` is the local Lorentz-invariant constant and does not vary in GR. What varies is the coordinate propagation speed (the effective coordinate speed of light determined by the metric). See `causal_velocity.md` for the full taxonomy. Any "varying propagation speed" language in this file refers to coordinate propagation speed, not the local causal velocity.

**PF interpretation (labeled):** Gravity is the Medium's causal structure having nonuniform geometry. Timelike modes extremize proper time along geodesics; null modes follow affine null geodesics, with a Fermat/optical-geometry reformulation available in the restricted static/stationary domain above. The extension to all spacetimes and all force regimes is the PF research program.

**Confirmed predictions (GR, not PF-specific):**

| Effect | Prediction | Measured |
|--------|-----------|---------|
| Light bending | 1.75 arcsec per solar radius | Confirmed 1919; refined continuously |
| Gravitational redshift | Δf/f = ΔΦ/c² | Confirmed (Pound-Rebka 1959, GPS) |
| Shapiro delay | Variable travel time | Confirmed (Cassini, 0.003%) |
| Gravitational time dilation | `dτ = dt √(1 − 2GM/rc²)` | Confirmed (atomic clocks at different altitudes) |

---

### Electromagnetism

**Standard account:** A charged matter mode couples minimally to the U(1) gauge field `A_μ`. The gauge-covariant derivative is:

```text
D_μ = ∂_μ − iqA_μ/ℏ
```

where `q` is the electric charge. The Lorentz force law follows from the non-commutation of `D_μ` in an electromagnetic potential:

```text
F = q(E + v × B)
```

This is fully derived in standard QED and classical EM; it requires no PF interpretation.

**PF interpretation (labeled):** The PF frames the U(1) gauge field as a Medium property. A charged mode's coupling to this field is its response to that structured Medium. This is consistent with the standard gauge-theory account but adds no new physics until the PF specifies what Medium property corresponds to `A_μ` and how it is generated.

---

### Strong Force (QCD)

**Standard account:** Quarks carry color charge and couple to the SU(3) color gauge field (gluons). The running coupling `α_s(Q²)` increases at low momentum transfer (large distance), producing confinement: the energy stored in a color flux tube grows linearly with separation, and quark-antiquark pair production occurs before free quarks can be separated.

At short distances (high Q²), `α_s` is small — asymptotic freedom — allowing perturbative QCD. At confinement distances (~1 fm), the coupling is order unity and perturbation theory fails.

**PF interpretation (labeled, OPEN):** The PF frames strong-force confinement as "extreme refraction" — an effective medium whose refractive index grows without bound at the confinement scale. This is a consistent analogy with the QCD running coupling behavior. It is not a derivation: no mapping from QCD Wilson loops or the running coupling to a PF refractive-index functional has been provided. Until such a mapping exists, this remains a PF analogy.

---

### Weak Force

**Standard account:** The weak force is mediated by W⁺, W⁻, and Z gauge bosons, which are massive due to the Higgs mechanism. Weak interactions are left-handed (V−A structure) and are the only Standard Model interactions that change quark or lepton flavor.

Beta decay example (neutron → proton + electron + antineutrino):

```text
n → p + e⁻ + ν̄_e
```

At the quark level:

```text
d → u + W⁻   followed by   W⁻ → e⁻ + ν̄_e
```

The W boson is a virtual propagator; the interaction vertex is governed by the weak coupling constant `g_W` and the CKM mixing matrix. The Higgs field provides the W and Z masses through spontaneous symmetry breaking; it does not change value during individual decay events.

**PF interpretation (labeled, OPEN):** The PF frames weak interactions as mode conversion — the down-quark mode transitions to an up-quark mode with emission of the W carrier, which converts to lepton modes. This is consistent with the flavor-changing structure of weak interactions. It is not a derivation: the PF has not reproduced the V−A interaction, parity violation, CKM structure, or CP violation from PF axioms. The weak force remains the least-mapped force in the framework.

---

### Force Taxonomy

| Force | Standard encoding | PF interpretation | PF status |
|-------|-----------------|-------------------|-----------|
| Gravity | Spacetime metric `g_{μν}` | Medium causal structure geometry | Established for null geodesics in restricted optical-geometry domain; massive paths use timelike geodesic/Jacobi treatment |
| Electromagnetism | U(1) gauge field `A_μ` | Medium U(1) structure coupling | PF label for standard gauge theory |
| Strong | SU(3) QCD running coupling | "Extreme refraction" analogy | PF analogy; formal mapping OPEN |
| Weak | W/Z boson exchange, V−A | Mode conversion interpretation | PF interpretation; formal derivation OPEN |

---

## Unification Program

The PF does not yet have a single master force equation. Its research program is to test whether a single Medium can be specified whose structural properties reproduce the four observed force effects.

| Unification approach | What it proposes |
|---------------------|-----------------|
| String theory | 10/11D spacetime with compactified geometry |
| Loop quantum gravity | Spin foam as discrete causal structure |
| Grand Unified Theories | Simple non-Abelian group containing `SU(3)×SU(2)×U(1)` |
| PF (current hypothesis) | Force effects as Medium structural properties; exact correspondences remain incomplete |

This is a research agenda framing, not a canonical derivation. Moving it from the canonical definition body to the framework manuscript is recommended.

---

## What Forces Are NOT

- Not action at a distance across empty space. Standard physics encodes force effects through local metric or gauge field structures; PF interprets these as Medium structures.
- Not a substance. Forces are descriptions of how modes change when they interact with field or metric structure.
- Not incompatible with quantum mechanics. QFT treats three of the four forces as quantum gauge theories; quantum gravity remains open.
- Not consciousness. No force has awareness, intention, or experience.
- Not information. Force interactions transfer energy and momentum; they do not inherently constitute meaningful information.

---

## Measurement Discipline

Every force claim must specify:

1. **Force type:** gravity, EM, strong, weak, or effective/composite (van der Waals, Casimir, nuclear).
2. **Mathematical structure:** spacetime metric (gravity), gauge group and potential (EM: U(1); strong: SU(3); weak: SU(2)×U(1)), or effective coupling.
3. **Affected modes:** gravity acts on all modes; EM acts on electrically charged modes; strong acts on color-charged modes (quarks, gluons); weak acts on all SM fermions and W/Z/Higgs.
4. **Energy/distance scale:** the regime in which the description is valid (QED, perturbative QCD, confinement scale, GR, Newtonian limit).
5. **Coupling constant(s):** G (gravity), α ≈ 1/137 (EM), α_s (strong, scale-dependent), G_F (weak).
6. **Whether the claim is established physics or PF interpretation:** gravity-as-optical-metric for null geodesics is established; strong-as-extreme-refraction and weak-as-mode-conversion are PF interpretations.
7. **Whether massive-particle gravity or massless-particle gravity is claimed:** the Fermat/optical-metric construction applies to null geodesics; massive particle paths require the full geodesic/Jacobi variational account.

---

## Open Questions

| Question | Status |
|----------|--------|
| Does the PF gravity-as-refraction extend canonically to massive particles beyond the qualitative level? | OPEN — Jacobi/Maupertuis construction needed; not equivalent to optical Fermat |
| Does the PF provide a formal mapping from QCD confinement to an effective refractive-index functional? | OPEN — "extreme refraction" is analogy until Wilson-loop/running-coupling mapping exists |
| Does the PF derive V−A structure, parity violation, CKM mixing, or CP violation from axioms? | OPEN — weak force is the least-mapped force in the framework |
| What is the minimum substrate (QCA) causal structure that reproduces all four force types? | OPEN — see `derivations/minimum_substrate_assessment_2026-04-28.md` |
| Does quantum gravity have a clean PF Medium interpretation? | OPEN — remains the hardest unification target |

---

## Falsification Conditions

A forces definition fails if:

1. **Light does not bend at 1.75 arcsec per solar radius** (to current precision): GR geodesics and the null optical-metric equivalence are falsified.
2. **Gravitational redshift is not measured** at the predicted rate: time dilation in the metric is falsified.
3. **Free quarks are observed in isolation:** QCD color confinement is falsified; the strong-force account needs revision.
4. **The Lorentz force law fails** for charged modes in tested EM fields: the U(1) gauge account fails.
5. **Beta decay is observed to violate energy-momentum conservation:** the W exchange account is falsified. Note: flavor change in beta decay (d → u) is the *expected* Standard Model behavior; it is not a falsifier.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `mode.md` | Forces change mode trajectories, momenta, or internal quantum numbers |
| `matter.md` | Matter modes are the primary carriers on which forces act |
| `energy.md` | Force interactions transfer energy (Hamiltonian terms); Noether symmetries connect force-field symmetries to conservation laws |
| `field.md` | Standard force descriptions use metric structure, gauge fields, and interaction terms; field observability/gauge caveats are controlled there |
| `coupling.md` | Force-like interactions are specialized coupling/interaction structures when they change a mode's momentum, trajectory, phase, quantum numbers, or field configuration |
| `medium.md` | Forces are Medium structural properties; gravity = metric structure; gauge forces = gauge field structure |
| `causal_velocity.md` | Controllable changes in force fields respect causal velocity; on-shell massless mediators propagate at `c`, massive mediators below `c`, and virtual exchange is not a signal |
| `coherence.md` | Stable bound states (force-bound matter modes) require structural coherence |
| `time.md` | Gravitational time dilation connects spacetime curvature (gravity) to proper-time differences |
