# Coherence
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Audits: `derivations/coherence_causal_velocity_audit_2026-04-28.md`; `derivations/coherence_definition_final_audit_2026-04-29.md`*

---

## The Definition

**Coherence is stable relational structure among states under evolution.**

In wave systems, coherence appears as stable phase relationships. In quantum systems, it appears as basis-dependent off-diagonal density-matrix structure. In dynamical systems, it appears as persistent organized correlations, modes, or invariants under time evolution.

Short form:

> Coherence is what lets a pattern remain distinguishable as it changes.

Coherence is not one universal scalar. It is a role that must be measured with a domain-specific metric.

---

## Why This Definition Is Layered

The Propagation Framework uses "coherence" across optics, quantum theory, stable particles, biology, cognition, and consciousness. Those uses are related, but not identical.

| Layer | Meaning | Typical mathematical object | Example |
|-------|---------|-----------------------------|---------|
| **Phase / wave coherence** | Stable phase relation between oscillatory modes | First-order coherence function, phase-locking value, cross-spectrum | Laser light, interferometry, synchronized oscillators |
| **Quantum coherence** | Superposition structure relative to a specified basis | Off-diagonal density-matrix terms, resource-theory coherence measures | Qubit superposition, superconducting phase, BEC order parameter |
| **Structural / dynamical coherence** | Persistence of organized correlations or modes under evolution | Eigenmodes, attractors, solitons, conserved/invariant structures | Stable particle modes, vortices, robust biological organization |
| **Self-referential coherence** | A speculative extension where a system maintains an integrated model of its own state/process | Not yet formalized for PF | Candidate consciousness metric; not canonical physics |

Do not substitute one layer for another without naming the bridge. A laser, an atom, an organism, and a conscious brain are not coherent in the same technical sense.

---

## Formal Examples

### Phase / Wave Coherence

For two oscillatory fields or modes, phase coherence means their relative phase remains stable over the relevant time/window:

```text
Delta phi(t) = phi_1(t) - phi_2(t)
```

The relationship is coherent when `Delta phi(t)` is constant or bounded within the tolerance of the measurement.

A common normalized optical coherence function is:

```text
gamma(x, y) = <E*(x) E(y)> / sqrt(<|E(x)|^2> <|E(y)|^2>)
```

This is a wave/optics measure. It is not automatically the right measure for particles, organisms, or consciousness.

### Quantum Coherence

For a quantum state `rho`, coherence is basis-dependent off-diagonal structure:

```text
rho = sum_ij rho_ij |i><j|
```

The off-diagonal terms `rho_ij` for `i != j` represent coherence relative to the chosen basis. A statement about quantum coherence must name or justify the relevant basis and measure.

Decoherence is the suppression of these off-diagonal terms relative to an environment-selected pointer basis. It converts a coherent quantum description into an effectively classical probability description for that context.

### Structural / Dynamical Coherence

A structure is dynamically coherent when its internal relations persist under the system's evolution rule. This can mean:

- an eigenmode persists under a linear operator,
- a soliton maintains shape while propagating,
- a bound state remains stable under perturbation,
- an attractor preserves organized behavior despite noise,
- a biological system maintains functional organization through energy throughput.

This is not necessarily phase coherence. It is stability of relational organization under dynamics.

---

## Axiom 3 Boundary

**Axiom 3:** Stable structure requires coherent propagation. Incoherent modes disperse.

Canonical interpretation:

> A PF structure persists only if it satisfies the relevant domain-specific coherence/stability condition under the Medium's dynamics.

What this definition establishes:

- Coherence is required for persistent structure.
- The relevant coherence metric depends on the domain.
- Phase coherence, quantum coherence, and dynamical coherence must not be conflated.

What this definition does **not** establish:

- the exact particle-spectrum coherence functional,
- a universal numerical threshold,
- the `Z3` generation selector,
- the "coherence ceiling",
- consciousness.

Those remain separate derivation targets.

---

## What Coherence Can Explain

| Phenomenon | Correct coherence role | Status |
|------------|------------------------|--------|
| Laser light | Strong phase coherence across emitted photons | Established optics |
| Superconductivity | Macroscopic quantum phase coherence of the condensate | Established condensed matter |
| Bose-Einstein condensate | Macroscopic occupation of a single quantum state | Established condensed matter |
| Stable particle modes | PF interprets persistence as dynamical coherence/stability under field evolution | PF interpretation; exact selector open |
| Atoms and molecules | Stable quantum bound-state structure | Established physics; not simply "high phase coherence" |
| Biological organization | Maintained non-equilibrium dynamical organization | PF-compatible; needs domain metric |
| EEG synchrony / gamma | Phase-locking or spectral coherence among neural signals | Measurable neuroscience; not consciousness by itself |
| Consciousness | Candidate self-referential/integrative coherence metric | Speculative; separate claim |

---

## Measurement Discipline

Every coherence claim must specify:

1. **System:** what states or modes are being compared.
2. **Relation:** phase, density-matrix basis, correlation, mutual information, stability, invariant, or other structure.
3. **Metric:** the actual estimator or functional.
4. **Window:** time scale, frequency band, spatial scale, or perturbation class.
5. **Threshold:** if a threshold is claimed, how it is derived or measured.

Without these five items, "coherence" is vocabulary, not a result.

### P1 / Applied Biofeedback Note

P1 may use applied coherence proxies such as EEG phase-locking, cross-frequency coupling, HRV coherence, or synchronization against a reference signal.

Those measurements belong in P1 protocol files, not in the canonical physics definition, unless the estimator, windowing, controls, and validation are explicitly specified.

No live P1 value is part of this definition.

---

## What Coherence Is NOT

- Not vague agreement, harmony, beauty, or positive feeling.
- Not amplitude or intensity; a weak signal can be coherent and a strong signal can be incoherent.
- Not one universal number from 0 to 1 across all domains.
- Not synonymous with stability; stability can be incoherent, dissipative, or externally maintained.
- Not synonymous with consciousness; lasers, crystals, superconductors, and BECs are coherent without being conscious.
- Not sufficient for consciousness. Any consciousness claim also needs self-reference, integration, report/control criteria, and a falsifiable measurement protocol.

---

## Open Questions

| Question | Status |
|----------|--------|
| What exact PF coherence functional selects stable particle modes? | OPEN |
| Does Axiom 3 imply a non-redundancy principle for both `Z2` closure classes? | OPEN |
| Does `Z3` symmetry determine a generation coherence/stability threshold? | PREDICTED / not derived |
| Can "coherence ceiling" be defined as a precise functional rather than a phrase? | OPEN |
| What PF-specific metric separates self-referential coherence from synchrony, integration, broadcast, or metacognition? | OPEN - see `CLAIMS.md` consciousness row |

---

## Downstream Rule

When downstream files use "coherence", they must specify which layer they mean:

- `phase coherence`,
- `quantum coherence`,
- `structural/dynamical coherence`,
- `self-referential coherence` (speculative),
- or a named PF coherence functional.

If a claim cannot identify the layer, it should not be upgraded.
