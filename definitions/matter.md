# Matter
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md` Derived Quantity 3*
*Audit: `derivations/matter_definition_final_audit_2026-04-29.md`; prior pre-dispatch packet superseded: `derivations/matter_pre_dispatch_audit_2026-04-29.md`*
*Dependencies: `mode.md` CANONICAL v1.0; `energy.md` CANONICAL v1.0*
*Related definitions: `forces.md`, `information.md` CANONICAL v1.0*

---

## The Definition

**Matter is stable or quasi-stable excitation structure of matter fields: quarks, leptons, and composite states built from them.**

The Propagation Framework interprets such excitations as self-maintaining modes of the Medium. Localized standing waves and bound states are important examples of matter modes, but free particles and propagating wave packets also count as matter. The scope of this definition is *matter fields* in the Standard Model sense: fermionic quarks and leptons, plus composite states made from them. Gauge bosons (photon, W, Z, gluon) and the Higgs boson have energy and may have rest mass, but they are not matter fields in this definition.

Plain language (not the formal definition):

> Matter is the quark-and-lepton side of the particle spectrum, including the stable structures built from it.

**PF interpretation (labeled, not canonical derivation):** The PF frames matter modes as self-maintaining excitations whose energy eigenvalues and quantum numbers are stable under the Medium's dynamics. The mechanism by which the Medium selects exactly the observed matter field content is not yet derived from PF axioms; it is an open problem.

---

## Scope: Matter Fields vs. Force Carriers

This file covers matter fields. Force carriers are treated separately in `definitions/forces.md`.

| Category | Examples | Rest mass | Status in this definition |
|----------|----------|-----------|---------------------------|
| **Quarks** | u, d, s, c, b, t | Yes | Matter fields; carry baryon number 1/3 and color |
| **Charged leptons** | e, μ, τ | Yes | Matter fields; carry lepton number and electric charge |
| **Neutrinos** | ν_e, ν_μ, ν_τ | Yes (small) | Matter fields; carry lepton number |
| **Composite matter** | proton, neutron, atoms | Yes | Bound states built from quarks/leptons |
| **Gauge bosons** | γ, W, Z, g | W/Z: yes; γ, g: no | Force carriers; see `forces.md` |
| **Higgs boson** | H | Yes | Scalar excitation; not a matter field in this definition |

**Why the distinction matters:** Calling the photon "stable matter" (as a prior draft did) conflates matter fields with force carriers. A photon has no rest mass and no baryon or lepton number; it is a gauge boson. W/Z bosons and the Higgs have rest mass, but rest mass alone is not sufficient for "matter" under this definition. This definition uses "matter" in the physics sense: fermions and their composites.

---

## Formal Structure

### Matter Modes as Field Excitations

A matter particle is a stable or quasi-stable one-particle excitation of a matter field. In quantum field theory:

```text
particle:     a†(k,s) |0⟩   — creation operator for particle with momentum k, spin s
antiparticle: b†(k,s) |0⟩   — creation operator for antiparticle (charge conjugate)
```

where the vacuum `|0⟩` is the ground state of the matter field. The two creation operators are distinct; the antiparticle is not produced by negating the particle state.

For a free Dirac fermion, the field decomposes as:

```text
ψ(x) = Σ_{k,s} [ u(k,s) a(k,s) e^{-ikx} + v(k,s) b†(k,s) e^{+ikx} ]
```

where `u(k,s)` and `v(k,s)` are the positive- and negative-energy spinors. The antiparticle creation operator `b†(k,s)` appears with the negative-energy spinor, not as a sign-flip of `a†(k,s)`.

### Free Particles and Wave Packets

A free electron is described by a wave packet in momentum space:

```text
|ψ⟩ = ∫ dk φ(k) a†(k,s) |0⟩
```

This is a propagating excitation, not a localized standing wave. It carries the electron's rest mass `m_e` and quantum numbers (charge, spin, lepton number), and it satisfies the relativistic dispersion relation `E² = (pc)² + (m_e c²)²`. A free electron is matter even though it is not a standing wave.

### Bound States and Standing Waves

When matter modes interact and confine, bound states form. A hydrogen atom is a bound state of a proton and an electron; a proton is a bound state of three quarks. In the rest frame of a bound state, the dominant spatial mode structure can be approximated as a standing wave:

```text
Ψ(x, t) ≈ φ(x) e^{-iEt/ℏ}
```

where `φ(x)` is the spatially localized wavefunction and `E` is the total Hamiltonian eigenvalue (including binding energy — see `energy.md`).

Bound states weigh less than the naive sum of their constituents because the binding energy is negative:

```text
M_bound c² = Σ m_i c² + E_binding   (E_binding < 0 for stable bound states)
```

This is handled through the Hamiltonian in `energy.md`, not through the matter definition itself.

### Stability Classes

| Class | Description | Example |
|-------|-------------|---------|
| **Stable** | No kinematically allowed decay channel within current experimental bounds | Electron, proton (> 10³⁴ yr), neutrinos (cosmological bounds) |
| **Quasi-stable** | Decays via weak interaction on macroscopic timescale | Neutron (880 s free), muon (2.2 μs), pion (26 ns) |
| **Unstable / Resonance** | Decays on strong/EM timescale; finite decay width | Top quark (5×10⁻²⁵ s), Δ baryon |

Stability is determined by whether a decay mode exists that is kinematically allowed and satisfies the relevant conservation laws and selection rules (energy-momentum, electric charge, baryon/lepton number where applicable, and compatibility with CPT).

---

## Properties

### Wave-Particle Description

A matter particle is a quantum field excitation. The apparent duality between "particle" and "wave" descriptions arises because:

- **Particle description:** the excitation has definite quantum numbers (mass, charge, spin) and is detected at a point.
- **Wave description:** the excitation is a superposition of momentum modes; it exhibits diffraction and interference.

**PF framework position:** These are two descriptions of the same quantum field excitation, not two ontologically different things. When a detector localizes the excitation, the interaction is local field coupling. The PF does not claim to have resolved the quantum measurement problem; it adopts a decoherence/relational position in which measurement is local field interaction, not a fundamental collapse mechanism. This is one position in an open foundational debate.

### Solidity

When two matter modes overlap, their mutual interaction determines whether they can coexist spatially:

- **Fermions (Pauli exclusion):** The spin-statistics theorem requires that fermionic wavefunctions are antisymmetric under exchange of identical particles. No two identical fermions can occupy the same quantum state. This follows from the anticommutation relations of fermionic creation operators in relativistic QFT; it is not derived from mode alignment in the PF.

- **Like-charge particles (electromagnetic repulsion):** Charged modes experience repulsive gauge field interactions when their charge distributions overlap.

- **Short-range nuclear repulsion:** At sub-femtometer distances, color and quark-exchange effects provide strong repulsive cores.

**PF interpretation (labeled):** The PF frames solidity as the result of overlapping mode configurations being forced into locally inconsistent field states. The Pauli mechanism (antisymmetry) and the electromagnetic/strong repulsion mechanisms are distinct and should not be collapsed into a single "waves pushing apart" picture without specifying which mechanism applies.

### Antimatter

Matter fields have charge-conjugate excitations. For charged Dirac matter fields, the antiparticle carries opposite charge quantum numbers (opposite electric charge, opposite baryon or lepton number) and the same mass. For neutral fields, the charge-conjugate state may be distinct or identical depending on whether the field is Dirac or Majorana; the neutrino case remains experimentally open.

Charge conjugation `C` maps a particle state to its antiparticle state. In the Standard Model, `C` is a symmetry of strong and EM interactions but is violated by weak interactions (C-violation). The combined `CPT` symmetry is a theorem of local relativistic quantum field theory.

**Annihilation:** When a particle and antiparticle annihilate, their combined state transitions to gauge boson radiation. For electron-positron annihilation:

```text
e⁻ + e⁺ → γ + γ
```

Total energy, momentum, and all conserved quantum numbers are preserved. The PF interpretation: two charge-conjugate matter modes convert to propagating gauge boson modes; the matter field occupation number decreases by one for each, and the photon field occupation number increases.

**PF interpretation (open):** Whether the charge-conjugation structure of antimatter follows from PF axioms or must be imported from the Standard Model is an open question.

### Charge

Electric charge is the coupling of a matter mode to the U(1) electromagnetic gauge field. Charge is quantized in the observed spectrum: quarks carry charge ±e/3 or ±2e/3; leptons carry charge ±e or 0.

U(1) gauge symmetry alone permits any real charge value; it does not by itself enforce integer or fractional multiples of `e`. The observed quantization pattern (with specific fractions for quarks) requires additional structure:

- Anomaly cancellation in the Standard Model constrains charge assignments across generations.
- Grand Unified Theories (GUT) can derive charge quantization from embedding `U(1)` in a simple non-Abelian group.
- PF derivation of the specific charge assignments is not yet achieved.

---

## What Matter Is NOT

- Not only localized standing waves. Free particles and propagating wave packets are also matter.
- Not synonymous with "particle." Force carriers (photon, W, Z, gluons) are particles but not matter fields in the sense used here.
- Not classical substance. The "hardness" of matter is a consequence of quantum exclusion and interaction, not an intrinsic property of classical stuff.
- Not made of classical pieces. A quark is a field excitation in a confined color state, not a classical sphere inside a proton.
- Not consciousness. Matter modes may be part of conscious systems, but no matter mode by itself carries awareness or experience.
- Not information. Matter modes carry structure that can encode information, but "matter" and "information" are distinct concepts.

---

## Measurement Discipline

Every matter claim must specify:

1. **Particle type:** which matter-field excitation (quark flavor, lepton flavor, composite matter state, or beyond-SM matter candidate). If the excitation is a gauge boson or Higgs boson, this file is not the controlling definition.
2. **State:** free particle (wave packet), bound state (composite), or resonance (unstable mode with decay width).
3. **Rest mass and quantum numbers:** mass in MeV/c² or GeV/c²; charge; baryon number; lepton number; color; spin.
4. **Stability class:** stable, quasi-stable (with measured lifetime or decay width), or unstable.
5. **Regime:** nonrelativistic (wave function / Schrödinger), relativistic (Dirac / QFT), strong-field, or effective theory.
6. **Whether charge quantization is used:** if so, note that the specific assignments are empirical and not yet derived from PF axioms.
7. **Whether the claim involves antimatter:** if so, use charge-conjugation language, not sign-flip language.

---

## Open Questions

| Question | Status |
|----------|--------|
| Why does the vacuum support exactly this matter field content (quarks, leptons)? | OPEN — the central PF derivation problem |
| Why three generations of quarks and leptons? | OPEN — may be topological degeneracy; no formal derivation |
| Does PF derive charge quantization and the specific fractional charges of quarks? | OPEN — requires additional structure beyond U(1) gauge invariance |
| Does the charge-conjugation structure of antimatter follow from PF axioms? | OPEN |
| Is there a dark matter mode — a stable matter excitation beyond the Standard Model? | OPEN |
| Does PF account for the baryon asymmetry of the universe? | OPEN — CP violation in SM exists; cosmological asymmetry generation is an active research area |

---

## Falsification Conditions

A matter definition fails if:

1. **Free electrons cease to exhibit quantum interference:** if the wave-packet / field-excitation account fails at any tested scale, the definition needs revision.
2. **Discrete mass values for particle species break down:** if matter fields are found to have continuous rest-mass values where standard QFT predicts discrete particle species, the mode account fails.
3. **Pauli exclusion is violated for identical fermions:** the antisymmetry postulate and spin-statistics theorem are among the best-tested results in physics; any confirmed violation would require revision of the fermionic matter account.
4. **Matter-antimatter pair annihilation fails to conserve energy and quantum numbers:** all measured annihilation events conserve total energy-momentum and all Standard Model charges; violation would falsify both the matter definition and QFT charge conservation.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `mode.md` | Matter particles are stable or quasi-stable quantum modes of matter fields |
| `energy.md` | Rest energy of matter is `mc²`; bound-state energy includes interaction/binding terms |
| `coherence.md` | Stable matter modes require structural coherence under evolution |
| `causal_velocity.md` | Matter-mode front/signal velocities respect causal velocity; massive particle velocities are strictly below `c`; phase/group velocities require taxonomy |
| `forces.md` | Forces determine how matter modes interact and bind; deferred pending `forces.md` audit |
| `time.md` | Matter modes have proper time along their worldlines; time dilation applies to all matter |
