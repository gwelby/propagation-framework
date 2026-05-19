# Coupling
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 — passed Codex final audit 2026-04-30*
*The dynamical relation by which two Medium subsystems can influence each other's evolution. Measurement, decoherence, and force are specialized cases.*
*Source: load-bearing term audit across canonical definitions; `measurement.md`; `decoherence.md`; `forces.md`; `field.md`*
*Audit: `derivations/coupling_definition_final_audit_2026-04-30.md`*
*Dependencies: `medium.md` CANONICAL v1.0; `field.md` CANONICAL v1.0; `state.md` CANONICAL v1.0; `mode.md` CANONICAL v1.0; `coherence.md` CANONICAL v1.0; `information.md` CANONICAL v1.0; `causal_velocity.md` CANONICAL v1.0; `minimum_substrate.md` CANONICAL v1.0; `propagation.md` CANONICAL v1.0*
*Related definitions: `decoherence.md`, `measurement.md`, `forces.md`, `observer.md` CANONICAL v1.0*

---

## Definition

**Coupling is a dynamical dependence between two or more Medium subsystems: the evolution of one subsystem depends on the state, field, or boundary condition of another through a specified interaction structure.**

A coupling claim requires:

1. **Two (or more) subsystems** — distinguishable boundaries in the Medium (`state.md`, `minimum_substrate.md`)
2. **A shared Medium interaction** — an overlap or connection through the Medium's degrees of freedom that makes one system's evolution dependent on another's (`medium.md`, `field.md`)
3. **Observable dependence or possible correlation generation** — under at least some allowed preparations, the joint dynamics can change subsystem states, generate correlations, exchange conserved quantities, or alter transition probabilities (`state.md`, `information.md`)

**In PF terms:** Coupling is what happens when two mode structures or field configurations interact through the Medium such that distinguishable change in one system can alter the evolution of the other. The common observable result is a correlated, entangled, or otherwise conditionally dependent joint state, but a specific initial state may be an eigenstate, dark state, or symmetry-protected state that shows no new correlation in that trial.

**Coupling is the primitive interaction relation.** Measurement, decoherence, and force-like effects are specialized cases of coupling with additional conditions. No additional conditions are required for coupling itself: coupling may occur without a stable record, without uncontrolled environmental phase loss, and without momentum transfer.

**Canonical reference:** `measurement.md` defines measurement as coupling + amplification + stabilization. `decoherence.md` defines decoherence as coupling to uncontrolled environmental degrees of freedom. `forces.md` defines force as an interaction that changes a mode's momentum, trajectory, phase, internal quantum numbers, or field configuration. All three use coupling or interaction structure as their common substrate.

---

## The Sub-Typing Hierarchy

Coupling is the primitive interaction relation. Measurement, decoherence, and force-like effects are distinguished by what the coupling does beyond dynamical dependence:

| Sub-type | Additional condition | PF definition |
|----------|---------------------|---------------|
| **Thermodynamic coupling (Regime 1)** | Interaction occurs but no stable accessible record survives; correlations rapidly thermalize or disperse | `measurement.md` Regime 1 |
| **Force / force-like interaction** | Coupling or metric/gauge interaction changes mode momentum, trajectory, phase, internal quantum numbers, or field configuration | `forces.md` |
| **Decoherence** | Coupling to uncontrolled environmental degrees of freedom makes phase relations inaccessible to the reduced system | `decoherence.md` |
| **Measurement** | Coupling + amplification + stabilization → stable accessible record correlated with the measured system | `measurement.md` Regimes 2–4 |

The hierarchy is not exhaustive — there are other specific coupling types (e.g., entanglement generation without decoherence, coherent state transfer). The point is that every more specific process presupposes coupling; coupling presupposes none of them.

---

## Coupling Strength and Type

Every coupling is characterized by two independent properties:

**Strength:** the magnitude of the interaction. In quantum settings, characterized by coupling constants or dimensionless strengths (e.g., electromagnetic `e` or `α`, Yukawa coupling constants for matter-Higgs interactions), matrix elements `⟨i,j|H_int|k,l⟩`, transition rates, cross sections, or interaction Hamiltonian norm in a specified model. Stronger coupling usually generates correlations, transitions, or relaxation faster in the stated regime, but no universal rate formula is canonical.

**Type:** the structure of the interaction term, which determines:
- Which observable or degree of freedom is affected or can become correlated (the effective pointer basis when the coupling is measurement-like)
- Whether coupling is coherent (preserves or generates basis-relative phase structure in the relevant subsystem description) or incoherent (averages over uncontrolled environmental phases)
- Whether coupling is closed-system/unitary (total Hamiltonian Hermitian; total energy conserved when time-translation symmetry holds) or open-system/dissipative (effective dynamics such as Lindblad terms, relaxation, or energy flow to an environment)

No universal formula for coupling strength is canonical here. Any quantitative coupling claim must name the interaction structure, subsystem boundaries, relevant observables, and approximation scheme in use.

---

## Causal Constraints on Coupling

Controllable influence through coupling is bounded by causal velocity (`causal_velocity.md`):

- A new local coupling influence between separated subsystems requires causal contact — controllable influence propagates through the Medium at ≤ causal velocity
- Quantum entanglement generated by past coupling does not constitute a new coupling channel; measuring one entangled subsystem does not couple it again to the other
- No-signaling: correlations generated by coupling do not transmit controllable information faster than the causal velocity. Correlation and controllable influence are distinct (`information.md`)

---

## Coupling Is Not

- **Not correlation alone.** Correlation is a common result of coupling. Two systems may be correlated because they were coupled in the past. A static correlated state is not itself a coupling event — it is evidence of one.
- **Not measurement.** Coupling is part of a measurement only when the correlation is amplified and stabilized into an accessible record. Most coupling in the universe (thermal collisions, ambient field interactions) produces no stable record.
- **Not decoherence.** Coupling to a controlled system can preserve or increase coherence. Decoherence specifically requires coupling to uncontrolled environmental degrees of freedom. Not every coupling destroys phase relations.
- **Not force.** Force-like coupling changes mode momentum, trajectory, phase, internal quantum numbers, or field configuration. Coupling that generates entanglement between subsystems without changing trajectories (e.g., quantum gate operations, entanglement distribution) is coupling without force.
- **Not instantaneous.** New controllable influence through coupling propagates through the Medium at ≤ causal velocity. There is no instantaneous coupling signal between spatially separated subsystems.
- **Not controllable FTL signaling.** Coupling generates correlations. Correlations alone do not transmit controllable information faster than the causal velocity (`causal_velocity.md`, `information.md`).

---

## Measurement Discipline

Every coupling claim must specify:

1. **Subsystem boundaries:** which two or more systems are coupled, and what is treated as environment?
2. **Interaction structure:** Hamiltonian term, Lagrangian term, gauge coupling, boundary condition, field overlap, scattering channel, or effective update rule.
3. **Coupled observables or degrees of freedom:** which state variables, fields, modes, charges, or records are affected?
4. **Strength/rate measure:** coupling constant, matrix element, transition rate, cross section, interaction norm, relaxation rate, or qualitative-only claim.
5. **Regime:** closed/unitary, open/dissipative, perturbative, nonperturbative, thermal, measurement, decoherence, force-like, or PF interpretation.
6. **Causal domain:** whether the systems are locally interacting now, share a past coupling history, or are spacelike separated with only pre-existing correlations.
7. **Outcome claimed:** correlation generation, entanglement, mode mixing, momentum/energy exchange, decoherence, stable record, or no observable effect for a protected/dark state.

Status boundaries:

| Claim | Status | Basis |
|-------|--------|-------|
| Coupling is dynamical dependence through a specified interaction structure | PF operational definition | Framework definition; consistent with standard physics |
| Coupling can be characterized by interaction Hamiltonians, Lagrangian terms, gauge couplings, boundary conditions, scattering channels, or update rules | Established | Standard quantum mechanics, QFT, classical field theory, and effective models |
| No universal coupling strength or rate formula — must name the interaction structure, boundaries, and approximation | PF constraint | System/model-specific; any quantitative claim must specify these |
| Measurement, decoherence, and force-like interactions are specialized cases of coupling/interaction structure with additional conditions | PF taxonomy | Follows from measurement.md, decoherence.md, forces.md canonical definitions |
| Controllable influence through coupling is bounded by causal velocity | Established (PF consistent) | No-signaling theorem; `causal_velocity.md` canonical |
| Coupling can generate correlations; correlations ≠ controllable information transfer | Established | `information.md` canonical; no-signaling theorems |

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `medium.md` | Coupling occurs through the Medium; the Medium's degrees of freedom carry and mediate coupling interactions |
| `field.md` | Fields provide distributed degrees of freedom through which coupling can be represented as overlap, exchange, boundary dependence, or interaction terms |
| `state.md` | Coupling can generate correlations between subsystem states; whether the post-interaction joint state factorizes depends on preparation, dynamics, and measurement context |
| `mode.md` | Coupling between modes creates superpositions, entanglement, and mode mixing |
| `coherence.md` | Coherent coupling can preserve or generate basis-relative coherence; incoherent/environmental coupling can degrade accessible coherence |
| `decoherence.md` | Decoherence is coupling to uncontrolled environmental degrees of freedom — a specialized coupling case with effective loss of accessible phase relations |
| `measurement.md` | Measurement is coupling + amplification + stabilization — a sub-type of coupling that creates a stable record |
| `forces.md` | Force-like interactions use coupling or metric/gauge interaction structure to change mode momentum, trajectory, phase, quantum numbers, or field configuration |
| `information.md` | Coupling can create correlations; correlations are the physical basis of information; coupling does not by itself constitute controllable information transfer |
| `observer.md` | Observer types are distinguished by what kind of coupling they engage in: Type 1 (thermodynamic coupling), Type 2 (measurement coupling), Type 3 (relay coupling), Type 4 (self-referential coupling loop) |
| `causal_velocity.md` | Controllable influence through coupling propagates at ≤ causal velocity; pre-existing correlations do not constitute a new signal channel |
| `minimum_substrate.md` | A PF substrate must support subsystem boundaries and local coupling through tensor-product structure with no-signaling |
| `propagation.md` | Propagation is movement of distinguishable change through the Medium; coupling is when that propagating change makes the evolution of a second subsystem dependent on the first |

---

## Falsification Conditions

1. **A claimed coupling creates no dynamical dependence under any allowed preparation:** If changing subsystem A never changes subsystem B's evolution, transition probabilities, conserved-quantity exchange, or correlations in the stated regime, then the claimed coupling is physically empty.

2. **Measurement without prior coupling:** If a stable record correlated with a measured system can be created without any interaction between the measuring and measured systems, the sub-typing hierarchy (measurement as specific coupling) collapses.

3. **Reduced-system decoherence without environmental coupling:** If a system undergoes genuine decoherence into an inaccessible environment without any coupling to environmental degrees of freedom — no shared Hamiltonian, no field overlap, no Medium connection, no coarse-grained degrees of freedom — the decoherence sub-type definition is wrong. Reversible unitary dephasing in a closed system does not count as decoherence for this falsifier.

4. **Controllable FTL influence via coupling:** If two systems can be coupled such that controllable information is transmitted faster than the causal velocity of their shared Medium, the PF causal structure of coupling is wrong.

---

## Open Questions

| Question | Status |
|----------|--------|
| Is there a PF minimum operationally resolvable coupling strength below which no correlation can be detected in finite time? | OPEN — experimental sensitivity and quantum discreteness must not be conflated |
| Can two subsystems be permanently decoupled in the PF — no shared Medium degrees of freedom, no shared field, no causal contact? | OPEN — related to causal isolation and cosmological horizon structure |
| Does the sub-typing hierarchy (force/decoherence/measurement as coupling sub-types) hold at quantum gravity scales? | OPEN — requires background-independent formulation |
| Is the coupling-vs-correlation distinction a fundamental PF distinction or a coarse-graining artifact of the observer's time resolution? | OPEN — may be scale-dependent |
