# Mode
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md`; used 34× in framework*
*Audit: `derivations/mode_definition_final_audit_2026-04-29.md`; prior pre-dispatch packet superseded: `derivations/mode_pre_dispatch_audit_2026-04-29.md`*
*Related definitions: `field.md`, `energy.md`, `forces.md`, `information.md` CANONICAL v1.0; Standard Model spectrum derivation remains OPEN*

---

## The Definition

**A mode is an admissible pattern of a field or Medium state under a specified evolution law.**

In linear regimes, modes are eigenfunctions or generalized eigenfunctions of the propagation operator. In interacting regimes, "mode" may denote stable or quasi-stable excitations, resonances, or effective degrees of freedom. Not all modes are discrete; not all modes are stable.

Plain language (not the formal definition):

> A mode is what the Medium can do repeatedly: a self-consistent pattern that the field equations permit.

**PF interpretation (labeled, not canonical derivation):** Stable and quasi-stable quantum modes are what physicists call particles. The Standard Model spectrum is not yet derived from PF axioms; it is reframed here as a mode-selection problem.

---

## Formal Structure

### Linear Modes

For a linear propagation operator `L`, a normal mode is an eigenfunction:

```text
L φ_n = λ_n φ_n
```

where `φ_n(x)` is the spatial mode profile and `λ_n` is the eigenvalue (related to mode frequency via the dispersion relation).

The general solution for a linear field is a superposition:

```text
Ψ(x, t) = Σ_n a_n φ_n(x) e^(-iω_n t)
```

where `ω_n` is the mode frequency and `a_n` is the amplitude coefficient.

### Continuum Modes

For fields on an infinite domain without boundary conditions, the mode spectrum is continuous. A free massive particle is described by wave packets in continuous momentum-frequency modes:

```text
Ψ(x, t) = ∫ dk a(k) φ_k(x) e^(-iω(k) t)
```

Continuous modes do not imply discrete particles. Discreteness arises from boundary conditions, topological constraints, or interaction-induced binding.

### Discrete Modes

When a field is subject to boundary conditions, topological constraints, or self-consistent nonlinear confinement, the spectrum of admissible modes becomes discrete. A violin string supports harmonics at integer multiples of the fundamental; the Medium supports modes at frequencies selected by its geometry, topology, and coupling constants.

Discreteness is a consequence of constraints, not a universal property of all modes.

### Interacting Regimes

In nonlinear or interacting systems, "mode" generalizes to:

- **Quasi-particle**: effective excitation in a many-body or field-theoretic context (e.g., phonon, plasmon).
- **Resonance**: unstable excitation with a finite decay width.
- **Stable bound state**: two or more field excitations whose combined configuration is self-reinforcing.

Mode interactions introduce couplings between amplitude coefficients `a_n`; the superposition principle holds only approximately in the interacting case.

### Mode Stability

| Stability class | Description | Example |
|-----------------|-------------|---------|
| **Stable** | No kinematically allowed decay channel; mode persists indefinitely within current experimental bounds | Electron, photon |
| **Quasi-stable** | Long-lived; slow decay channel exists | Neutron (10 min free half-life), muon (2.2 μs) |
| **Unstable / Resonance** | Decays on dynamical timescale; finite decay width | Excited hadrons, W/Z bosons |

Stability is determined by whether an allowed decay channel exists that satisfies all relevant conservation laws and kinematic constraints. It is not a universal property of being a mode.

---

## Mode Frequency

The mode frequency `ω` is determined by the Medium's dispersion relation:

```text
ω = ω(k; m, g, boundary conditions, topology)
```

Parameters include: wave vector `k`, mass parameter `m`, coupling constants `g`, boundary conditions, and topological winding number. Changing any parameter changes the mode spectrum.

For massive excitations in vacuum (Lorentz-invariant dispersion):

```text
ω² = (ck)² + (mc²/ℏ)²
```

This is the relativistic dispersion relation. The rest-frame frequency is `ω_0 = mc²/ℏ`.

**Note:** The formal relation between mode frequency and energy is defined in `definitions/energy.md`. Mode frequency `ω` is used here as the mechanical oscillation rate of the field configuration.

---

## PF Interpretation: Particles as Modes

The Propagation Framework interprets the observed particle spectrum as the set of stable and quasi-stable modes the Medium supports.

This is a reframing, not a derivation:

- The Standard Model's particle content — quarks, leptons, gauge bosons, Higgs — is the observed mode spectrum.
- The PF asks: what properties of the Medium select exactly these modes and not others?
- A drumhead supports specific vibrational modes because of its geometry, tension, and boundary conditions. The PF hypothesis: the vacuum supports specific particle modes for analogous reasons — its causal structure, topology, and coupling constants.

**Status of this interpretation:** The SM gauge structure `SU(3) × SU(2) × U(1)`, the specific particle representations, and the charge assignments are not yet derived from PF axioms. This is the central open derivation problem.

---

## Antimatter

In quantum field theory, every field supporting a complex representation admits two types of excitations: particles and their charge conjugates (antiparticles). The antiparticle of a mode carries opposite charge quantum numbers and is related to the particle by the charge conjugation operation C of the relevant field theory.

For a charged scalar field, the particle and antiparticle one-particle states are generated by distinct creation operators:

```text
particle:     a†(k)|0>
antiparticle: b†(k)|0>
```

where `b†(k)` creates the charge-conjugate excitation. This is not a global minus sign or a simple phase flip of `a†(k)`. For spinor fields, the relation involves the Dirac charge-conjugation matrix.

When a particle and antiparticle meet, the interaction converts the bound-state configuration into propagating radiation. Total energy and all conserved quantum numbers are preserved.

**PF interpretation (open):** The PF would like to derive the particle/antiparticle structure from the Medium's field equations and symmetry requirements. Whether the charge-conjugation operation follows from PF axioms, or whether it must be imported from the Standard Model, is an open question. The naive `-φ` sign-flip picture is incorrect; the full structure requires the charge-conjugation representation of the field.

---

## What a Mode Is NOT

- Not necessarily a particle. Many modes — continuum radiation modes, thermal fluctuations, phonons in condensed matter — are not identified with individual particles.
- Not necessarily discrete. Free fields on infinite domains have continuous mode spectra.
- Not necessarily stable. Unstable modes (resonances) are modes; they decay.
- Not necessarily quantized in the energy-level sense. Quantization depends on boundary conditions and field-theoretic structure, not on being a mode.
- Not consciousness. A mode may be part of a conscious system, but no mode by itself carries awareness or experience.
- Not a force. Modes are field configurations; forces are interactions that change those configurations (see canonical `definitions/forces.md` and `definitions/coupling.md`).

---

## Measurement Discipline

Every mode claim must specify:

1. **Mode type:** normal mode (linear eigenfunction), continuum mode (plane wave / wave packet), quasi-particle, resonance, or bound state.
2. **Domain:** boundary conditions, spatial extent, and symmetry class (periodic, box, infinite-volume, topological).
3. **Frequency or dispersion:** the mode frequency `ω(k)` or dispersion relation; distinguish rest-frame frequency from propagating frequency.
4. **Stability class:** stable, quasi-stable (with decay width or lifetime), or unstable (resonance).
5. **Quantum numbers:** if claiming particle-mode correspondence, specify charge, spin, color, isospin, and mass.
6. **Regime:** classical field, quantum field (free), interacting QFT, effective theory, or PF interpretation.
7. **Whether the claim is standard physics or PF interpretation:** the mode decomposition is standard; particle-as-mode and generation-as-degeneracy are PF interpretation.

---

## Open Questions

| Question | Status |
|----------|--------|
| Does the PF derive the SM gauge structure `SU(3) × SU(2) × U(1)` from Medium axioms? | OPEN — central unsolved problem |
| What selects exactly three generations? | OPEN — may be topological degeneracy; no formal derivation exists |
| Does the charge-conjugation structure of antiparticles follow from PF axioms, or must it be imported from QFT? | OPEN |
| Are there stable modes beyond the Standard Model (dark sector)? | OPEN — dark matter candidates |
| Does the minimum substrate (QCA) constrain which modes are admissible? | OPEN — see `derivations/minimum_substrate_assessment_2026-04-28.md` |

---

## Falsification Conditions

A mode definition fails if:

1. **Wave phenomena disappear** at scales where quantum interference is currently observed — the discrete mode spectrum must produce diffraction and interference at all tested scales.
2. **Continuous spectra appear where only discrete modes are expected** — atomic spectral lines are discrete; any confirmation of a continuous spectrum where the mode account predicts discrete lines would require revision.
3. **The PF particle-as-mode interpretation implies a prediction that fails** — if the framework predicts a mode that does not exist, or forbids a particle that does, the selection principle fails.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `medium.md` | Modes are admissible patterns of the Medium's field states under its evolution law |
| `field.md` | A field is the distributed degree of freedom whose admissible patterns are modes |
| `coherence.md` | Stable modes require stable relational structure under evolution (structural/dynamical coherence) |
| `causal_velocity.md` | Mode front and signal velocities respect causal velocity; phase and group velocities require the velocity taxonomy in `causal_velocity.md` |
| `energy.md` | For stationary quantum modes, `energy.md` gives the formal `E = ℏω` relation and its Hamiltonian limits |
| `matter.md` | Matter is stable or quasi-stable excitation structure of matter fields; PF frames matter as stable mode structure |
| `forces.md` | Forces change mode momentum, trajectory, phase, internal quantum numbers, or field configuration |
| `information.md` | Information is distinguishability/correlation of mode configurations relative to an alphabet, reference, or record |
