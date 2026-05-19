# Information
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md` Derived Quantity 5; deferred from `mode.md`, `energy.md`, `observer.md`*
*Audit: `derivations/information_definition_final_audit_2026-04-29.md`*
*Dependencies: `mode.md` CANONICAL v1.0; `energy.md` CANONICAL v1.0; `coherence.md` CANONICAL v1.0; `propagation.md` CANONICAL v1.0; `observer.md` CANONICAL v1.0; `medium.md` CANONICAL v1.0; `causal_velocity.md` CANONICAL v1.0*
*Related definitions: `coupling.md` CANONICAL v1.0*
*Deferrals: `consciousness.md` (P5 — candidate; consciousness is not derivable from this definition)*

---

## The Definition

**Information is the measure of distinguishability of a state or state change relative to a specified reference or noise background.**

Information is not a substance. It is not an intrinsic fluid carried by a particle independent of context. It is a relationship between a state and a set of alternatives, or between a signal and the context in which it arrives. Physical systems can encode, store, or transmit information only when their states are correlated with a reference or message ensemble. The same physical event may carry different amounts of information relative to different references.

The canonical definition has four components:

**1. Distinguishability (core):** Information exists when a state or propagation structure can be distinguished from the alternatives available in the context. This is the Shannon sense: for N equally probable alternatives, the maximum information is log₂(N) bits; in general, H = −Σ p log₂ p for distribution p.

**Note on coherence and distinguishability:** The relationship is not simple. Quantum information capacity (the ability to be in a superposition of distinguishable states) requires quantum coherence — off-diagonal density-matrix terms. But classical distinguishability (of pointer states after decoherence) is precisely what *survives* after coherences are suppressed; decoherence establishes stable, distinguishable classical outcomes. The claim "distinguishability requires coherence" is correct for quantum information capacity but incorrect for classical information. Thermalized states lose distinguishability because both the quantum coherences *and* the classical pointer-state correlations are destroyed by coupling to the thermal bath — not because of coherence alone.

**2. Correlation (medium of information):** Information is stored or transmitted as a correlation between two or more structures. The observer's record is a correlation between the incoming propagation and the observer's internal state. Shannon mutual information is a correlation measure. Von Neumann entropy measures quantum mixedness/uncertainty of a density operator; it is not itself a correlation measure unless applied to a subsystem of a larger state.

**3. Reference-dependence (observer-relative):** The information content of a state depends on what it is being distinguished from. A photon arriving at a detector can carry information because the detector's state prior to the arrival provides a reference against which the post-arrival state is distinguishable. Without a specified reference, ensemble, or measurement context, an information claim is undefined — there is only a state description.

**4. Physical instantiation (mode-relative):** Information is physically realized as a mode configuration or mode-structure change in the Medium. A record in a Type 2 observer is a stable mode configuration. A Type 3 correlated propagation is a correlation being relayed by a propagating mode. The Medium provides the causal structure that makes distinguishability physically meaningful.

Plain language:

> Information is the measure of how much one thing tells you about another — when the thing and the alternatives are distinguishable.

---

## Information vs. Energy vs. Matter

This distinction is deferred from `mode.md` and `energy.md`. It must be explicit here.

**Energy** is the conserved quantity associated with time-translation symmetry, represented by the Hamiltonian expectation value or eigenvalue (`energy.md`). It is a scalar. A mode has energy whether or not its state is distinguishable from anything. A photon in a thermal radiation field has nonzero energy set by its frequency, with a characteristic thermal scale of order `k_B T`, but it carries no specific information about its origin if its state is fully thermalized within the ambient radiation field.

**Matter** is a classification of stable mode structures — quarks, leptons, and their composites. A matter mode has energy and may carry information, but matter itself is not information.

**Information** is a property of correlations between states, not a property of a single state. The same mode can carry information (when correlated with a reference) or not carry information (when thermalized relative to all available references).

```
A mode in a known pure state selected from an agreed alphabet:
    energy = ℏω, von Neumann entropy S(ρ) = 0, sender uncertainty = 0
    if the receiver already knows the state: no new information is gained
    if the receiver does not know which of N orthogonal states was prepared:
        measurement can convey up to log₂(N) bits
    (pure state does not mean zero communicable information; it means zero mixed-state entropy)

A mode in a thermal mixed state (fully thermalized):
    energy = set by the occupied frequencies; thermal scale ~ k_B T
    S(ρ) = thermal entropy for the ensemble
    mutual information with a specific source/record ≈ 0 unless an additional correlation exists
    (high entropy means high uncertainty; it does not by itself encode a specific message)

A mode correlated with an observer (Type 2 record):
    energy = ℏω, mutual information I(mode;observer) > 0
    (the observer's state narrows down which mode was received)
```

Entropy and information are related but not identical. Entropy measures uncertainty or mixedness relative to a specified ensemble/state description. Mutual information measures correlation between systems. A pure state has zero von Neumann entropy, but whether it conveys information depends on the message ensemble and receiver's prior knowledge. The examples above use "information" to mean mutual information or communicable distinguishability relative to a reference system, not von Neumann entropy of the mode alone.

The PF does not claim energy and information are equivalent. High-energy thermal radiation can carry large energy and entropy while carrying little mutual information about a specific source. A low-noise coherent optical mode can carry high mutual information if its amplitude, phase, timing, or polarization is modulated against a shared reference.

---

## Shannon Entropy and Von Neumann Entropy in PF Terms

**Shannon entropy `H(X) = −Σ p(x) log₂ p(x)`** measures the expected uncertainty, or average surprisal, of a classical random variable `X` with distribution `p(x)`. For `N` equally probable alternatives, `H(X) = log₂(N)`. In PF terms: given a classical set of distinguishable mode configurations `{x}` with probabilities `{p(x)}`, Shannon entropy gives the average number of bits needed to identify which alternative occurred.

**Von Neumann entropy `S(ρ) = −Tr(ρ log₂ ρ)`** measures the mixedness/uncertainty of a quantum density operator `ρ`. It is basis-independent and equals the Shannon entropy of the eigenvalue spectrum of `ρ`. For a pure state (`ρ² = ρ`), `S(ρ) = 0`. For a thermal density matrix, `S(ρ)` is the quantum statistical entropy of that state.

The mapping between Shannon and Von Neumann is not 1:1. Von Neumann entropy is basis-independent, but measurement-outcome Shannon entropy is basis-dependent: choosing an observable or decoherence-selected pointer basis produces a classical distribution over outcomes. Quantum coherence is basis-dependent because off-diagonal density-matrix terms are basis-dependent; this is distinct from the basis-independence of `S(ρ)`.

**PF interpretation (labeled):** The PF treats density-matrix language as the default physical description when quantum mode structure matters. Von Neumann entropy measures mixedness of that density operator, while Shannon entropy applies to classical outcome distributions after a measurement basis or pointer basis has been specified. This is a PF framing; it is consistent with standard quantum information theory but is not an independently derived PF result.

---

## Information and the Observer

`observer.md` defines four types of observation. Information applies differently to each:

**Type 1 — Thermodynamic:** Any recoverable correlation with the incoming propagation is thermalized. The rock absorbing a photon converts the photon's phase/frequency/arrival-time distinguishability into lattice vibration entropy. The source-record correlation is destroyed. Thermodynamic entropy increases; no stable record is produced.

**Type 2 — Structural recording:** The observer's state change produces a stable record. Information is stored as a correlation between the incoming propagation's properties and the observer's structural state. The record can be queried. The specified correlation is preserved over the relevant timescale.

**Type 3 — Correlated propagation:** The correlation is preserved in the outgoing signal. "Information propagates" means the correlation is relayed by a physical mode. A detector triggering a readout system preserves the specified correlation in the readout channel.

**Type 4 — Self-correlating:** The record feeds back into the observer's own internal dynamics. This is the Type 4 case — the observer's structural/dynamical coherence is modified by the record, and that modification influences subsequent response. This is where the PF connects to memory and learning, with consciousness explicitly deferred to `consciousness.md`. The mechanism is not yet canonical; this is the open Type 4 question.

---

## What Information Is NOT

- Not a substance. Information is a measure of a relationship, not a thing that can be stored in a location or transmitted along a wire. "Information transmitted" is shorthand for "correlation propagated between two structures."
- Not the same as thermodynamic entropy. Thermodynamic entropy is a macroscopic property of ensembles. Von Neumann entropy is a quantum mixedness measure. Shannon entropy and mutual information are classical information-theoretic measures. These quantities are related, but they are not interchangeable and must be named separately.
- Not resolution-independent. The distinguishability of a state depends on the basis or measurement context. A state that is maximally distinguishable in one basis may be maximally mixed in another. This is not a defect — it is the structure of quantum distinguishability.
- Not a solution to the mind-body problem. Self-correlating records may be relevant to memory or learning, but the PF does not claim to derive subjective experience from information.
- Not the same as computation. Computation is a specific class of information transformations — logical operations applied to bit strings. The PF does not claim the universe is a computer or that physics is computation. Information in the PF is physical distinguishability; computation is one possible relationship between distinguishable states.

---

## Measurement Discipline

Every information claim must specify:

1. **Distinguishability basis or state space:** what set of alternatives is being distinguished? Shannon information requires an explicit classical alphabet/distribution. A quantum measurement claim requires an observable or POVM. A von Neumann entropy claim requires a density operator and, if relevant, a subsystem split.
2. **Measure:** surprisal, Shannon entropy `H(X)`, Shannon mutual information `I(X;Y)`, von Neumann entropy `S(ρ)`, entanglement entropy, or thermodynamic entropy? These are distinct measures with different physical meanings.
3. **Observer type (if applicable):** Type 1 (no record), Type 2 (local record), Type 3 (propagating record), Type 4 (self-correlating — PF interpretation only).
4. **Physical medium of the record:** what mode structure carries the correlation? A CCD pixel is a mode; a neural cascade is a mode-structure; a propagating signal is a mode propagating.
5. **Reference frame/context:** information is reference-relative. Is the reference a pre-existing structure (prior state), an ensemble (probability distribution), or an observer's prior state?
6. **Whether the claim is standard physics or PF interpretation:** Shannon and Von Neumann entropy are standard physics. Type 4 self-correlating information is PF interpretation. The PF does not use "semantic information" or "meaning" as technical terms.
7. **Record persistence timescale:** over what timescale must the correlation be maintained? (Connects to `observer.md`'s stability requirement.) Type 1/2/3 classification depends on whether the correlation persists long enough to be queried or relayed in the stated experiment, not on an absolute lifetime threshold. The timescale must be compared to the relevant decoherence, relaxation, and readout times.

---

## Falsification Conditions

A specific information claim fails if:

1. **The claimed correlation is fully thermalized with respect to all available references:** if no recoverable distinguishability exists because the state is in thermal equilibrium with the noise background, the claimed information record does not survive.
2. **The distinguishability basis is not specified:** if no reference distribution or measurement basis is stated, the information claim is undefined.
3. **A Type 4 self-correlating information claim has no proposed mechanism:** the claim that an observer's internal state feeds back into its own dynamics requires a structural mechanism. Without it, the claim is not a canonical PF derivation.
4. **PF information interpretation predicts that thermodynamic Maxwell's demon can operate without an energy cost:** Landauer's principle requires at least `k_B T ln 2` of heat dissipation per bit for logically irreversible erasure into a bath at temperature `T` in the quasistatic limit. If the PF predicts otherwise, the thermodynamics account needs revision.
5. **The PF claims the universe computes, simulates, or processes semantic information as a canonical result:** this would be a scope violation of the canonical definition, which is strictly about distinguishability and correlation, not meaning.

---

## Open Questions

| Question | Status |
|----------|--------|
| Can the PF derive Landauer's principle from mode/coherence/propagation? | OPEN — consistent with thermodynamics but not yet derived from PF canonicals |
| Is Type 4 self-correlating information supported by a structural mechanism? | OPEN — no mechanism proposed |
| Can PF derive the bridge from quantum density-matrix entropy to classical Shannon records? | OPEN — this definition distinguishes the measures but does not derive the decoherence/pointer-basis bridge |
| Can biological memory be described as Type 4 observer state modification within the PF? | OPEN — consistent with PF but not a canonical claim |

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `mode.md` | Information is encoded in distinguishable mode configurations only relative to an alphabet, reference, or correlated record; a mode state alone is not an information measure |
| `energy.md` | A mode has energy regardless of its information content; energy is a Hamiltonian scalar, information is a relational measure; deferred to this file |
| `coherence.md` | Quantum coherence supports quantum information capacity; decoherence can create stable classical pointer records; structural coherence is required for records to persist |
| `coupling.md` | Coupling can create the correlations that make information physically available; correlation alone is not controllable information transfer |
| `observer.md` | Types 1–3 cover standard physical record/correlation handling; Type 4 covers self-correlating records (memory, learning — OPEN) |
| `propagation.md` | Information propagates when a correlated signal travels from one observer to another; an uncorrelated propagation carries no information about the specified reference |
| `medium.md` | The Medium provides the causal structure within which distinguishability is meaningful; information cannot be defined without a causal structure that distinguishes before/after |
| `causal_velocity.md` | Information propagation is bounded by causal velocity; no controllable signal exceeds causal velocity; this sets the speed limit for Type 3 information transfer |
| `gradient.md` | Gradient fields produce state changes that can encode information when the state change remains distinguishable relative to a reference |
