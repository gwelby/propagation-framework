# Decoherence
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 — passed Codex final audit 2026-04-30*
*How coherent mode structures degrade through interaction with the Medium environment.*
*Audit: `derivations/decoherence_definition_final_audit_2026-04-30.md`*
*Related definitions: `coupling.md` CANONICAL v1.0; `coherence.md`; `measurement.md`; `information.md`*

---

## Definition

**Decoherence** is the Medium-environment-mediated loss of stable phase relationships between the modes of a coherent structure. It is not the absence of propagation — it is the degradation of coherent propagation into incoherent propagation.

Decoherence occurs when a coherent mode structure interacts with environmental degrees of freedom that are not part of the mode structure itself. The interaction correlates or entangles the system's phase/state variables with environmental variables, making the original coherent relations inaccessible to the reduced system. The irreversibility is effective: in principle a closed unitary system can contain the correlations, but recovering them requires control of the environmental degrees of freedom.

**In PF terms:** Decoherence is the increase in environmental coupling of a coherent mode, where the environment is the set of Medium degrees of freedom not captured in the mode's own coherent structure.

**Formal characterization (schematic):**
- In quantum settings, decoherence appears as suppression of off-diagonal density-matrix terms in an environment-selected pointer basis.
- In open-system models, the decoherence rate depends on the system-environment coupling, environmental spectral density, temperature, and coarse-graining assumptions.
- When `Γ_decoherence × t >> 1` in a specified model, coherent phase relations are effectively unavailable to the reduced system.

No universal scalar formula for `Γ_decoherence` is canonical here. Any quantitative claim must name the model, coupling, environment, basis, and approximation.

**Canonical reference:** `coherence.md` layers 1–3 describe coherence as a spectrum. Decoherence is the process by which a mode structure transitions from higher coherence (layers 2–3) toward lower coherence (layer 1) through environmental interaction.

---

## The Decoherence Mechanism

Decoherence is not mysterious. It is the expected behavior of coherent systems in a Medium that has more degrees of freedom than the coherent structure can control.

The process:

1. **Mode structure initializes** — coherent phase relationships exist between modes (layer 2 coherence)
2. **Environmental coupling occurs** — the coherent structure interacts with surrounding Medium degrees of freedom
3. **Phase entanglement propagates** — the phases of the coherent modes become entangled with environmental phases
4. **Effective irreversible dispersion** — the environmental variables are not controlled by the mode structure, so the original phase relationships cannot be restored without access to the environment or active correction
5. **Coherence collapses to layer 1** — the mode structure still propagates, but without stable phase relationships

This is the standard quantum-decoherence pattern and the PF template for coherence loss in broader systems. Biological systems subject to thermal and physiological noise show analogous loss of organized correlations, but biological noise should not be read as literal quantum decoherence unless a quantum model is specified.

---

## Decoherence Timescales

Decoherence is characterized by a timescale `τ_decoherence`, but there is no universal value. It depends on:

| Factor | Why it matters |
|--------|----------------|
| System-environment coupling | Stronger coupling usually shortens coherence lifetime |
| Environmental spectral density | Determines which system frequencies are efficiently decohered |
| Temperature / occupation | Hotter or more populated environments usually add more uncontrolled degrees of freedom |
| Basis / observable | Decoherence is basis-relative; pointer states are selected by the interaction |
| Active error correction or feedback | Stabilization mechanisms can preserve usable coherence longer than passive dynamics |

The longer the decoherence timescale relative to the mode lifetime or record-readout time, the more stable the coherent structure or record.

**PF significance:** Biological systems that maintain organized dynamics, such as neural phase-locking or gamma-band coordination, do so through active stabilization and feedback. This is a structural coherence-maintenance claim, not a claim that macroscopic brain dynamics are protected quantum coherent states.

---

## Decoherence and Noise

**Noise** and **decoherence** are related but not identical:

- **Decoherence** is the mechanism — entanglement of mode phases with uncontrolled environmental degrees of freedom, causing irreversible dispersion of phase correlations
- **Noise** is the observable manifestation — the random fluctuations that appear in a signal when phase relationships have been dispersed

In quantum coherent systems, the observable signature of decoherence in a phase-sensitive measurement is an increased noise floor in the off-diagonal density matrix elements. Broadly, noise in physical signals arises from multiple sources — thermal fluctuations, shot noise, quantization noise, 1/f noise — not all of which are decoherence signatures. The PF narrow claim: decoherence manifests as noise in phase-sensitive observables of coherent systems. This does not generalize to all noise sources.

**Canonical reference:** `medium.md` role 8 (Noise injection) identifies the Medium as a source of environmental decoherence. The ambient Medium degrees of freedom are not in a controlled coherent state, so they inject decoherence into any coherent structure they interact with.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `coupling.md` | Decoherence is the specialized case of coupling to uncontrolled environmental degrees of freedom |
| `coherence.md` | Decoherence is the degradation pathway from layer 3 → layer 2 → layer 1 coherence |
| `medium.md` | The Medium provides the environmental degrees of freedom that drive decoherence (role 8: Noise injection) |
| `mode.md` | Stable modes persist when their coherence lifetime exceeds their decoherence timescale |
| `observer.md` | Type 2 observers require coherence/record persistence long enough to form records; Type 3 observers require the correlation to survive propagation; Type 4 claims require self-correlation to survive long enough to affect future response |
| `information.md` | Decoherence disperses distinguishability from the local system into the environment; information is not globally destroyed in a closed description, but the original local record may become inaccessible |
| `consciousness_metric_program.md` | L_self maintenance is coherence-maintenance against decoherence; the metric program tests whether self-model loops can sustain coherence below decoherence thresholds |

---

## Falsification Conditions

1. **Model-specific decoherence does not occur:** If a coherent mode structure in a specified environment shows no loss of the predicted coherence under the stated coupling, basis, and approximation, that decoherence model is wrong.

2. **Uncontrolled macroscopic decoherence is generically reversible:** If dispersed phase relationships in an uncontrolled macroscopic environment routinely recover without environmental control, recurrence engineering, echo protocols, or active correction, the effective-irreversibility account is wrong.

3. **Noise is uncorrelated with environmental coupling:** If changing environmental coupling has no effect on the relevant noise floor or coherence lifetime in a controlled model, the PF noise/decoherence link needs revision.

---

## Open Questions

| Question | Status |
|----------|--------|
| Is there a fundamental decoherence rate for the vacuum Medium itself (quantum vacuum fluctuations)? | OPEN — related to vacuum energy and cosmological constant |
| Can biological coherence-maintenance mechanisms (e.g., neural phase coordination) sustain organized correlations against physiological noise? | OPEN — relevant to consciousness_metric_program.md |
| Does the PF imply a fundamental limit to coherence lifetime, or can arbitrarily long coherence be sustained with sufficient active maintenance? | OPEN — may have implications for quantum computing and consciousness |
| Does the Minimum Substrate require decoherence for quantization (quantization as decoherence-selection)? | Speculative — not yet in canonical scope |
