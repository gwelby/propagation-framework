# Measurement
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 — passed Codex final audit 2026-04-30*
*What constitutes a measurement in PF terms, and how it relates to the observer taxonomy.*
*Audit: `derivations/measurement_definition_final_audit_2026-04-30.md`*
*Related definitions: `coupling.md` CANONICAL v1.0; `observer.md`; `information.md`; `decoherence.md`*

---

## Definition

**Measurement** is the process by which a propagation event becomes a record — a physical state change in a measuring system that is correlated with the measured system and remains causally accessible to downstream observers after the original coupling event.

A measurement has three structural components:

1. **Coupling:** The measured system and the measuring system interact via the Medium, such that the state of the measuring system becomes correlated with the state of the measured system
2. **Amplification:** The measuring system's state change propagates beyond the immediate coupling region — it is accessible to other parts of the measuring system and to other observers
3. **Stabilization:** The record persists under decoherence — the correlation survives the measuring system's decoherence processes and remains accessible after the coupling is severed

**In PF terms:** Measurement is the creation of a Type 2 observer record (from `observer.md`) — a physical state change in a second system that is causally downstream of the measured system and remains accessible.

**Canonical reference:** `observer.md` defines Type 2 as "Recording: a system that makes records of its observations." The record is the physical footprint of a measurement. This file defines what makes a specific interaction a measurement rather than just a coupling.

---

## Measurement Regimes

The PF recognizes measurement regimes corresponding to the observer taxonomy:

**Regime 1 — Thermodynamic coupling (Type 1):**
Two systems interact via the Medium. States are correlated. No record is made. The coupling is transient and the correlation is not stabilized. This is just propagation — indistinguishable from noise in a thermal system.

*Example: Two molecules collide and exchange energy. Their states are correlated after the collision. No record exists.*

**Regime 2 — Recorded observation (Type 2):**
The measuring system stabilizes the correlation as a physical record that persists under decoherence. The record is accessible to other observers.

*Example: A photon hits a detector and creates a persistent photoproduct. The photoproduct is a record that persists and can be read by other observers.*

**Regime 3 — Relayed or propagated record (Type 3):**
The measuring system preserves the correlation in an outgoing signal, cascade, or readout channel. The record does not merely stay local; it propagates to another observer.

*Example: A detector triggers a readout electronics chain. The original interaction is converted into a durable downstream signal.*

**Regime 4 — Self-referential measurement (Type 4 — PF interpretation, OPEN):**
The record feeds back into the measuring system's own future state. The measurement loop is closed within the system itself.

*Example: A neural system senses its own activity and the sensing modifies subsequent activity. The record is internal and self-influencing.*

---

## The Measurement Problem in PF Terms

The standard measurement problem: in quantum mechanics, unitary evolution preserves superpositions, while actual measurements yield definite outcomes. How do definite outcomes and Born-rule probabilities arise from the quantum formalism?

The PF framing: the observer is a Medium subsystem, not an external metaphysical ingredient. Measurement is a Medium process: the record is a physical state change in the recording Medium.

What decoherence explains: why measurement outcomes appear definite, why interference disappears, why records persist — the stable, accessible, decohered records that different observers agree on.

What decoherence does not explain by itself: which specific outcome occurs (outcome selection), or why the Born rule gives the specific probabilities it does. Decoherence helps select a pointer basis and suppress interference. It does not by itself select which pointer state occurs. The Born rule is a separate open problem.

---

## Shannon Measurement vs. Von Neumann Measurement

Two distinct concepts that must be separated:

**Shannon measurement (classical/Type 2):**
A record is created. For `N` equally probable alternatives, the maximum Shannon information content of the record is `log₂(N)` bits; for unequal probabilities it is `H(X) = −Σ p(x) log₂ p(x)`. The record is basis/context-dependent — the outcome distribution depends on which observable was measured. This is what `information.md` calls information as distinguishability.

**Von Neumann measurement (quantum/Type 2 in quantum Medium):**
The density matrix of the measured system becomes correlated or entangled with the state of the measuring system. The measuring system's record is created. The von Neumann entropy `S(ρ)` of the measured system — its mixedness — may increase, decrease, or remain unchanged depending on the measurement type and conditioning:
- **Ideal nonselective projective measurement:** `S(ρ)` increases or stays the same because coherences are discarded when outcomes are not conditioned on
- **Selective/QND measurement:** S(ρ) can decrease — the system is projected onto a pure state conditioned on the outcome
- **Projective measurement:** S(ρ) increases for the mixture, but the conditional post-selected state may be pure

The key point: the record is created in the measuring system regardless of whether the measured system's entropy increases, decreases, or stays the same. Von Neumann entropy change and record creation are related but not identical.

**Key distinction:**
- Shannon: measures the information content of the record
- Von Neumann: measures mixedness of the quantum state; decoherence is one physical process that can increase mixedness in a reduced description

The record is Type 2. In decoherence accounts, record creation correlates the measured system with the measuring system and suppresses off-diagonal terms in the relevant pointer basis. This explains stable classical-looking records and loss of interference, but not the Born rule or unique-outcome selection by itself.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `coupling.md` | Measurement is coupling plus amplification and stabilization into an accessible record |
| `observer.md` | Measurement is the process that creates a Type 2 record; Type 3 propagates records; Type 4 self-referential measurement remains PF interpretation |
| `information.md` | Shannon measurement creates distinguishable records; von Neumann entropy measures quantum mixedness and must not be conflated with mutual information |
| `coherence.md` | Quantum measurement suppresses coherences relative to a pointer basis in decoherence accounts; stable records require structural coherence over readout timescales |
| `decoherence.md` | Stable macroscopic records usually require decoherence into an environment-selected pointer basis; decoherence does not by itself solve outcome selection |
| `propagation.md` | Measurement is a propagation event with amplification and stabilization |
| `causal_velocity.md` | Record creation and record propagation are bounded by the relevant causal/front velocity |

---

## Falsification Conditions

1. **A claimed Type 2 measurement creates no stable record:** If a measuring system couples to a measured system but the correlation does not persist long enough to be accessed in the stated regime, it is Type 1 coupling, not Type 2 measurement.

2. **Record creation is independent of correlation:** If a supposed record carries no recoverable correlation with the measured system or event, it is not a measurement record under this definition.

3. **Controllable FTL measurement:** If a measurement outcome can be transmitted faster than causal velocity, the PF causal structure of measurement is wrong. Records cannot propagate faster than causal velocity.

4. **Type 4 measurement without a self-model mechanism:** If a system is claimed to make self-referential records but no mechanism links the record to its own future state dynamics, the Type 4 characterization is incomplete.

---

## Open Questions

| Question | Status |
|----------|--------|
| Can the PF derive the Born rule (probabilities of measurement outcomes) from Medium axioms? | OPEN — related to the God Equation |
| Is quantum measurement fundamentally different from classical measurement, or is classical record creation the macroscopic/decohered limit of quantum measurement? | OPEN — PF favors continuity, not derived |
| Does a Type 4 self-measurement loop constitute consciousness, or is it necessary but not sufficient? | Deferred to `consciousness.md` |
| What is the minimum decoherence rate for a system to create stable records? | OPEN — relevant to neural systems and quantum computing |
