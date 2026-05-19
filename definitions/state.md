# State
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 — passed Codex final audit 2026-04-30*
*What a state is in PF terms, and how quantum state and classical pointer state relate to the canonical coherence/decoherence/measurement stack.*
*Source: load-bearing term audit across canonical definitions; `mode.md`; `measurement.md`; `decoherence.md`; `information.md`*
*Audit: `derivations/state_definition_final_audit_2026-04-30.md`*
*Dependencies: `medium.md` CANONICAL v1.0; `mode.md` CANONICAL v1.0; `coherence.md` CANONICAL v1.0; `decoherence.md` CANONICAL v1.0; `measurement.md` CANONICAL v1.0; `information.md` CANONICAL v1.0; `observer.md` CANONICAL v1.0; `minimum_substrate.md` CANONICAL v1.0; `energy.md` CANONICAL v1.0; `time.md` CANONICAL v1.0; `causal_velocity.md` CANONICAL v1.0*

---

## Definition

**A state is a complete specification of a system's relevant degrees of freedom sufficient to determine its measurement predictions under a specified evolution law and measurement context.**

In PF terms: a state is the operational configuration assigned to a system at a moment — the set of mode occupancies, phase relationships, and correlations that determines how it propagates, couples to other systems, and creates records.

Three aspects of a state must always be named:

1. **The system** — which Medium degrees of freedom are being described; where is the boundary?
2. **The representation** — which formalism encodes those degrees of freedom (wavefunction, density operator, field configuration, classical phase-space point)
3. **The basis or context** — relative to which observable or pointer basis the state is specified; a density operator is basis-independent, but its matrix representation and measurement probabilities require a specified observable context

A state is not self-defining. "The state of X" must specify all three or it is incomplete.

**Canonical reference:** `mode.md` defines a mode as "an admissible pattern of a field or Medium state under a specified evolution law." A mode is a specific kind of state — one that is an eigenpattern of the evolution operator. A general state may be a superposition of modes, a statistical mixture of modes, or both.

---

## Two Regimes: Quantum State and Classical Pointer State

The PF recognizes two operational state regimes, grounded in `coherence.md` and `decoherence.md`:

### Quantum state (general quantum regime)

The system is described by a density operator `ρ` (or pure-state wavefunction `|ψ⟩ = Σᵢ cᵢ|i⟩` as a special case). Off-diagonal elements `ρᵢⱼ` for `i≠j` in a specified basis are coherences in the sense of `coherence.md` layer 2. A quantum state can be pure or mixed, can be a superposition relative to one basis and diagonal relative to another, can be entangled with other systems, and its observable properties depend on which observable is measured.

- A pure state `ρ = |ψ⟩⟨ψ|` has minimal mixedness, `S(ρ) = 0`; its coherence is basis-relative, not identical to purity
- A mixed state `ρ = Σᵢ pᵢ |i⟩⟨i|` (with respect to some basis) is a statistical mixture; it may or may not reflect decoherence depending on the basis and preparation history
- Von Neumann entropy `S(ρ) = −Tr(ρ log ρ)` measures the mixedness of the state, not its information content in isolation (see `information.md` and `measurement.md`)

### Classical pointer state (decohered regime)

The system's off-diagonal coherences in the environment-selected pointer basis have been suppressed by decoherence (`decoherence.md`). The resulting state behaves as if it is a definite, stable configuration — a record or a classically readable outcome. Classical pointer states are:

- The stable physical records that Type 2 observers create (`measurement.md`: coupling + amplification + stabilization)
- Robust under environmental coupling (the pointer basis is selected by the system-environment interaction)
- Describable to good approximation by classical probability distributions over the pointer basis

The transition from quantum state to classical pointer state is the process described in `decoherence.md`. It is not a sharp threshold — it depends on the decoherence timescale, the pointer basis, and the degree of environmental entanglement. The classical pointer state is the decohered limit of a quantum state, not a separate ontological category.

---

## State and Mode

Related but distinct:

| Concept | What it is |
|---------|-----------|
| Mode | An admissible state pattern that is an eigenfunction of the evolution operator; a stable propagation pattern (`mode.md`) |
| State | The general configuration of the system's degrees of freedom — can be a single mode, a superposition of modes, a statistical mixture, or any combination |

A single-mode state is a special case of a state. A general quantum state may be a superposition of modes, a mixed state over modes, an entangled state across subsystems, or a thermal state weighted by Boltzmann factors. Every mode is a state; not every state is a mode.

---

## State and Information

A state carries information only relative to a reference (`information.md`):

- A known pure state has zero von Neumann entropy and carries no surprise for an observer who already knows the preparation; relative to a receiver uncertain among `N` possible preparations, identifying that state can carry up to `log₂(N)` bits
- The distinguishability between two states is the physical basis of information
- Measuring a state creates a record correlated with that state (`measurement.md`); the information in the record is the mutual information between the state and the record, not the state itself

The physical state itself is not identical to information. It is a configuration. Information arises when one state is distinguishable from another against a reference distribution or prior.

---

## State Is Not

- **Not a trajectory.** A state specifies a configuration at a moment (or a density operator over a time window). Trajectories are sequences of states under an evolution law. Equating a state with its history is a category error.
- **Not a bare eigenstate list.** A density operator `ρ` is a basis-independent mathematical object — its eigenvalues, trace, and von Neumann entropy are basis-invariant. But the matrix elements `ρᵢⱼ`, the diagonal form, and the probabilities for outcomes of a specified observable depend on the chosen basis or measurement context. A state claim that specifies only "ρ" without naming the relevant observable context is incomplete.
- **Not information.** A state is a configuration; information is distinguishability between configurations. A state in a known, recorded configuration carries zero additional Shannon information to an observer who already holds the record.
- **Not a classical phase-space point.** Classical mechanics describes states as points `(q, p)` in phase space. Quantum states are density operators — richer objects that include superposition and entanglement. The classical picture is the decohered pointer-state limit, not the fundamental description.
- **Not global.** A state is always a state of a specified system with a specified boundary. There is no globally accessible state of the whole Medium — observer access is always local (see `observer.md`, `minimum_substrate.md`, `causal_velocity.md`).
- **Not an interpretation commitment.** "State" in this file means an operational description that determines predictions for measurements. Which interpretation of quantum mechanics (Copenhagen, Many-Worlds, relational, etc.) is correct remains open. The PF uses the operational reading and does not select an interpretation.

---

## Measurement Discipline

Every state claim must specify:

1. **System boundary:** what subsystem is being described, and which degrees of freedom are excluded as environment?
2. **Representation:** wavefunction, density operator, field configuration, classical phase-space distribution, or pointer-state distribution.
3. **Basis or observable context:** which basis, pointer basis, or observable defines the relevant probabilities and coherences?
4. **Evolution law:** which Hamiltonian, update rule, field equation, or effective dynamics evolves the state?
5. **Preparation and mixedness:** pure state, mixed state, thermal state, reduced state, or classical distribution; include `S(ρ)` when mixedness matters.
6. **Access level:** local subsystem state, reduced density operator, observer record, or hypothetical global state; do not imply globally accessible state unless justified.
7. **Status of the claim:** standard quantum/classical physics, PF operational vocabulary, or open interpretation.

Status boundaries:

| Claim | Status | Basis |
|-------|--------|-------|
| A state is an operational specification of degrees of freedom sufficient for evolution and measurement predictions | PF operational definition | Framework definition; consistent with standard physics |
| Pure state `ρ = |ψ⟩⟨ψ|`; mixed state `ρ = Σᵢ pᵢ |i⟩⟨i|` in a specified basis | Established | Standard quantum mechanics |
| Von Neumann entropy `S(ρ) = −Tr(ρ log ρ)` measures mixedness | Established | Standard quantum mechanics; used in `measurement.md` |
| Decoherence suppresses off-diagonal terms in a pointer basis selected by system-environment coupling | Established | Standard decoherence theory |
| Classical pointer state is the decohered limit of quantum state — not a separate ontological category | PF interpretation — consistent with decoherence theory | `decoherence.md` canonical |
| Quantum interpretation (ontological reading of `ρ`) | OPEN — interpretational | Copenhagen / Many-Worlds / relational QM — PF does not select |

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `medium.md` | The Medium is state-bearing: it provides the degrees of freedom whose configurations are described by states |
| `field.md` | A field state is a configuration of distributed field degrees of freedom |
| `mode.md` | A mode is a specific kind of state — an eigenpattern of the evolution law; a general state is a superposition or mixture of modes |
| `coherence.md` | Coherence is basis/context-relative structure in a state: phase relation, off-diagonal density-matrix terms, or persistent correlation depending on regime |
| `decoherence.md` | Decoherence suppresses off-diagonal terms in the pointer basis and makes records effectively classical; the transition is continuous, not a sharp collapse |
| `measurement.md` | Measurement creates a record correlated with a state; the record is itself a pointer state; measurement reads a state property into the measuring system |
| `information.md` | Information is distinguishability between states relative to a reference; a state is not itself information |
| `observer.md` | Different observer types can access different state properties; Type 1 thermodynamic coupling does not create a stable record; Type 2+ observers create records of state properties |
| `minimum_substrate.md` | A PF substrate must support tensor-product state spaces ℋ = ℋ₁ ⊗ ℋ₂ ⊗ … with local degrees of freedom; a single isolated Hilbert space cannot serve as the whole Medium |
| `energy.md` | Energy is represented by the Hamiltonian operator `H`; `iℏ ∂|ψ⟩/∂t = H|ψ⟩`, and energy values are expectation values `⟨H⟩` or eigenvalues for energy eigenstates |
| `time.md` | A state is a configuration at a moment; time is the ordering relation on state changes along physical histories |
| `causal_velocity.md` | Physical changes and controllable information about states propagate at ≤ causal velocity |

---

## Falsification Conditions

1. **A state specification that makes no observable predictions:** If a proposed state description yields no predictions about any measurement outcome in any context, it is not a state in the operational PF sense — it is notation without physical content.

2. **Basis-independent coherence is claimed:** If a definition claims that off-diagonal coherence is an absolute property independent of basis, it fails. Coherence must be specified relative to a basis, observable, pointer structure, or decomposition into subsystems.

3. **A thermodynamically stabilized pointer state spontaneously recovers accessible quantum coherences under ambient conditions:** If a macroscopic record (decohered into environment, thermally stabilized) spontaneously reverts to an observable quantum superposition without controlled intervention, the PF decoherence account of state transitions is wrong.

4. **A globally accessible state of the whole Medium:** If an observer can operationally access the complete state of the entire Medium — all degrees of freedom and all correlations — the PF's locality structure is wrong (`causal_velocity.md`, `minimum_substrate.md`).

---

## Open Questions

| Question | Status |
|----------|--------|
| Which interpretation of quantum mechanics gives the correct ontological reading of the density operator? | OPEN — interpretational; PF uses operational reading |
| Is the quantum-to-classical transition exactly the decohered pointer-state limit, or is an additional ingredient required? | OPEN — related to the measurement problem; decoherence is necessary but Born rule outcome selection remains open |
| Can a state of the whole Medium (global state) be consistently defined in the PF? | OPEN — requires quantum gravity or background-independent formulation |
| What is the minimum number of degrees of freedom for a system to have a well-defined state distinguishable from background? | OPEN — related to `minimum_substrate.md` |
