# Energy
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md` Derived Quantity 2*
*Audit: `derivations/energy_definition_final_audit_2026-04-29.md`; prior pre-dispatch packet superseded: `derivations/energy_pre_dispatch_audit_2026-04-29.md`*
*Dependencies: `mode.md` CANONICAL v1.0*
*Related definitions: `matter.md`, `information.md` CANONICAL v1.0*

---

## The Definition

**Energy is the generator of time evolution and, when time-translation symmetry is present, the corresponding conserved Noether quantity.**

In Noether's theorem, every continuous symmetry of the action corresponds to a conserved quantity. When the action is invariant under time translation `t → t + ε`, the corresponding conserved quantity is energy. If the system has explicit time dependence or no global time-translation symmetry, energy can still be represented locally or relative to a Hamiltonian, but global conservation is not guaranteed.

In quantum theory, energy is represented by the Hamiltonian operator `H`. The total energy of a system is the expectation value `⟨H⟩`, or the eigenvalue `E` for an energy eigenstate `H|E⟩ = E|E⟩`.

Plain language (not the formal definition):

> Energy is the conserved quantity that tells you how a system's phase evolves in time.

**PF interpretation (labeled, not canonical definition):** The PF interprets energy as mode frequency — for a stationary quantum mode with angular frequency `ω`, the energy eigenvalue satisfies `E = ℏω`. Total energy in interacting systems includes all Hamiltonian contributions (rest, kinetic, field, interaction, binding, vacuum); calling all energy "frequency" requires that the full Hamiltonian frequency is meant, not just the free-field or rest-mass term.

---

## Formal Structure

### Noether / Hamiltonian Energy

For a classical field theory with action `S[φ]` on a fixed background with a chosen time coordinate, time-translation invariance gives a conserved Noether current. In flat spacetime, the time component integrated over space is the Hamiltonian:

```text
H = ∫ T^{00} d³x
```

where `T^{μν}` is the energy-momentum tensor. `H` is conserved when the Lagrangian has no explicit time dependence and the background admits the relevant time-translation symmetry. In generic curved spacetime, global energy conservation requires additional structure such as a timelike Killing vector.

In quantum mechanics, `H` is the generator of time evolution:

```text
iℏ ∂|ψ⟩/∂t = H|ψ⟩
```

Energy eigenstates evolve as:

```text
|E, t⟩ = e^{-iEt/ℏ} |E, 0⟩
```

The phase frequency of this evolution is:

```text
ω = E / ℏ
```

This is the safe, standard statement: the angular frequency of an energy eigenstate's phase evolution equals `E/ℏ`. The SI has fixed the numerical value of `ℏ` exactly since 2019, but the physical content — that energy eigenstates precess at frequency `E/ℏ` — is a structural fact of quantum mechanics, not merely a unit choice.

### Mode-Frequency Correspondence

For a free quantum mode with dispersion relation `ω(k)`:

```text
E = ℏω(k)
```

This holds for:
- A photon: `ω = ck`, so `E = ℏck = hf`
- A free massive particle: `ω² = (ck)² + (mc²/ℏ)²`, so `E² = (pc)² + (mc²)²`
- A quantum harmonic oscillator: `E_n = ℏω(n + ½)` for mode number `n`

**Important:** This correspondence holds for stationary modes and energy eigenstates in free-field or non-interacting limits. In interacting systems, the Hamiltonian includes additional terms, and the total energy is not simply ℏω for any single free-field frequency.

### Binding Energy and Interaction Energy

The total rest energy of a composite bound system is not the naive sum of constituent rest energies:

```text
M_bound c² = Σ m_i c² + E_interaction
```

where `E_interaction` includes potential energy contributions (typically negative for bound states). For atomic hydrogen:

```text
M_H c² = m_p c² + m_e c² − 13.6 eV
```

The binding energy (−13.6 eV) lowers the total invariant mass. In the PF mode picture, the total frequency of a bound system corresponds to the total Hamiltonian eigenvalue, including all interaction terms.

### Energy Conservation

By Noether's theorem, energy is conserved in any isolated system whose dynamics have time-translation symmetry. This applies to:
- Free fields
- Interacting fields (conservation holds for the full Hamiltonian, including interaction terms)
- Bound states (the binding energy is part of the total)

The PF mode-frequency restatement: for a closed system with time-translation-invariant dynamics, total Hamiltonian frequency is conserved under mode conversion. This is the Noether result, not an additional claim.

---

## Properties

### Quantization

Energy levels are discrete when boundary conditions or interaction terms restrict the available mode spectrum. A particle in a box, a hydrogen atom, or a quantum harmonic oscillator has discrete energy eigenvalues because the Schrödinger equation with boundary conditions selects a discrete eigenspectrum.

Free particles on an infinite domain have continuous energy spectra.

Discreteness is a property of the mode spectrum under constraints, not of energy itself.

### Rest Mass and Compton Frequency

For a particle of rest mass `m`, the rest-frame energy eigenvalue is:

```text
E_rest = mc²
```

The corresponding angular frequency of phase evolution is:

```text
ω_Compton = mc²/ℏ
```

This is the Compton frequency — the phase precession rate of the particle's rest-frame quantum state. It is not a mechanical oscillation frequency of the particle itself; it is the rate at which the wavefunction phase advances in the rest frame.

For a proton: `ω_Compton ≈ 1.43 × 10²⁴ rad/s`
For an electron: `ω_Compton ≈ 7.76 × 10²⁰ rad/s`

These are measurable (Compton scattering sets the wavelength scale) and consistent with mass measurements.

### Zero-Point Energy

The ground state of a quantum oscillator has energy `ℏω/2`, not zero. Relative zero-point effects are measurable:

- Casimir effect: zero-point fluctuations of the electromagnetic field produce a force between conducting plates.
- Lamb shift: zero-point fluctuations of the QED vacuum shift atomic energy levels.

Zero-point energy is the irreducible minimum energy of a quantum oscillator relative to its Hamiltonian. Observable effects depend on differences, boundary conditions, or couplings; the absolute vacuum-energy value is subject to renormalization and is tied to the cosmological-constant problem.

**Open:** The sum of zero-point energies over all vacuum modes diverges (the cosmological constant problem). The PF does not resolve this; it is an open problem. The measured cosmological constant is 120 orders of magnitude smaller than the naive sum, and PF does not yet derive this.

### Temperature

**Statistical mechanics (canonical definition):** Temperature is defined by:

```text
1/T = (∂S/∂E)_{V,N}
```

where `S` is thermodynamic entropy and the derivative is taken at constant volume and particle number. In equilibrium, temperature governs the Boltzmann distribution of energy occupation:

```text
P(E) ∝ e^{-E/k_B T}
```

**PF interpretation (reframe, not definition):** Temperature can be restated as the characteristic energy scale of thermal fluctuations, `k_B T`, which corresponds to a characteristic mode frequency `ω_T = k_B T / ℏ`. A hotter system populates higher-frequency modes more strongly. This is a consistent PF reframe of the Planck distribution; it does not replace the statistical definition.

---

## What Energy Is NOT

- Not a substance or fluid. Energy is a conserved quantity and can have flux in field theory, but it is not a material stuff that flows.
- Not "converted" to or from mass in nuclear reactions. Rest energy `mc²` is the Hamiltonian eigenvalue in the rest frame; nuclear reactions redistribute it among products and radiation.
- Not a universal synonym for mode frequency. The mode-frequency correspondence holds for free-field energy eigenstates; interacting and bound systems require the full Hamiltonian.
- Not a measure of consciousness or information in itself.
- Not dimensionless. The identification of energy with frequency requires the constant `ℏ`, which carries units J·s. The analogy to a simple unit conversion (like km to m) is instructive but imprecise; `ℏ` is not a pure conversion factor.

---

## Measurement Discipline

Every energy claim must specify:

1. **Type:** total energy `E`, rest energy `mc²`, kinetic energy `E - mc²`, potential energy, binding energy, or free energy.
2. **System:** whether the energy is for a single mode, a multi-particle system, or a field configuration.
3. **Hamiltonian:** which terms are included (free-field, interaction, binding, vacuum/zero-point).
4. **Reference frame:** rest frame, lab frame, or center-of-mass frame.
5. **Regime:** nonrelativistic (`E ≈ mc² + p²/2m`), relativistic (`E² = p²c² + m²c⁴`), quantum (`E = ℏω` for energy eigenstates), thermal (`k_B T` scale), or cosmological.
6. **Conservation scope:** isolated system, open system exchanging with a bath, or approximate (where symmetry is only approximate).
7. **Whether frequency language is used:** if energy is restated as frequency, specify that the full Hamiltonian frequency is meant and include binding/interaction terms.

---

## What This Resolves

| Problem | Resolution | Status |
|---------|-----------|--------|
| Why energy is conserved | Time-translation symmetry of the action (Noether's theorem) | Standard physics |
| Why energy is discrete for bound systems | Boundary conditions / interaction terms select discrete Hamiltonian eigenvalues | Standard physics |
| Why photon energy is `E = hf` | For a free massless mode, `E = ℏω = hf` — mode-frequency correspondence in free field | Standard physics; PF restates as frequency interpretation |
| Why `E = mc²` | Rest energy is the Hamiltonian eigenvalue in the rest frame; `ω_Compton = mc²/ℏ` | Standard physics |
| Why bound states weigh less | Binding energy lowers total Hamiltonian eigenvalue (negative potential contributions) | Standard physics |
| Why zero-point energy exists | Ground state has minimum non-zero Hamiltonian eigenvalue | Standard physics; cosmological-constant magnitude remains OPEN |

---

## Open Questions

| Question | Status |
|----------|--------|
| Does PF derive the vacuum energy / cosmological constant magnitude? | OPEN — zero-point frequencies sum to divergent result; measured Λ is 120 orders smaller |
| Does PF give a derivation of `ℏ` from Medium properties? | OPEN — `ℏ` is currently taken as a given constant, not derived |
| Is the mode-frequency correspondence exact in the interacting PF Medium, or is it an approximation? | OPEN — holds exactly for free-field modes; PF must specify the full Hamiltonian |
| Does `ΔEΔt ≥ ℏ/2` follow from mode decomposition in PF? | INTUITION — the time-energy uncertainty relation follows from Fourier conjugacy of time and frequency |

---

## Falsification Conditions

An energy definition fails if:

1. **Noether / time-translation symmetry fails:** any confirmed violation of energy conservation in an isolated system with time-translation-invariant dynamics would require revision.
2. **Energy eigenstates do not precess at `ω = E/ℏ`:** spectroscopic measurements and quantum time-evolution tests would contradict the Hamiltonian account.
3. **Binding energy accounting fails:** if bound-system invariant masses could not be described by the full Hamiltonian including interaction terms, the mode-frequency restatement would fail.
4. **Zero-point effects vanish where quantum field theory predicts them:** absence of Casimir or Lamb-shift effects would falsify the included quantum ground-state claims, not the Noether definition itself.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `mode.md` | For a stationary quantum mode with frequency `ω`, the energy eigenvalue is `E = ℏω` |
| `coherence.md` | Stable modes (which carry well-defined energy eigenvalues) require structural coherence under evolution |
| `causal_velocity.md` | Relativistic dispersion uses the invariant speed `c`; mode front/signal velocities respect causal-velocity limits |
| `time.md` | Energy is the generator of time translations; relation to proper time depends on the chosen frame or worldline |
| `matter.md` | Rest energy of a matter mode is `mc²`; matter is scoped to quarks, leptons, and composites |
| `information.md` | Energy is a Hamiltonian scalar or expectation value; information is a relational distinguishability/correlation measure |
