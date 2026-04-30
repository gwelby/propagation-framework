# Propagation
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md` Axiom 1*
*Audit: `derivations/propagation_definition_final_audit_2026-04-29.md`*
*Dependencies: `medium.md`, `causal_velocity.md`, `coherence.md`, `mode.md`, `energy.md`, `time.md` CANONICAL v1.0; related downstream terms: `matter.md`, `forces.md` CANONICAL v1.0*

---

## The Definition

**Propagation is the finite-speed causal transmission of a distinguishable state change through the Medium.**

A propagating entity may be a mode, field disturbance, wave packet, signal front, or composite excitation. Its controllable causal influence is bounded by the relevant causal/front velocity, while its phase relations may be preserved or degraded according to the Medium's coherence rules.

Propagation is not the same as motion. Motion is displacement over time. Propagation is the specific kind of causal state-change in which a disturbance travels to future causal points. Not all motion is propagation. Not all propagation is motion in the Newtonian particle sense.

Plain language:

> Propagation is how change gets from one place to another through the Medium's structure — at finite speed, bounded by causal velocity.

---

## Bootstrapping: Propagation as the Completed Primitive

Axiom 1 says propagation is prior to everything. `medium.md` defines the Medium as "the rule-structure that lets distinguishable change propagate." Read naively, these two statements are circular: propagation is defined through the Medium; the Medium is defined through propagation.

The resolution: propagation is the *intuitive primitive* with which the PF axioms begin, not a concept derived from something more basic. The canonical definitions (medium.md, causal_velocity.md, coherence.md, time.md, mode.md, energy.md, matter.md, forces.md) were built in order to *formalize* what propagation means — to replace the informal intuition with precise, auditable concepts.

`propagation.md` completes that program: it uses all those canonical definitions to state precisely what was assumed informally at the start. The canonical definitions do not depend on `propagation.md` — they were written without it. `propagation.md` is the reverse step: the boot-strap closes when the primitive concept is restated using the formal vocabulary built on top of it.

This structure is not unique to the PF. "Computation" in computer science is the intuitive primitive; the Church-Turing thesis makes it precise using formal models (Turing machines, lambda calculus) that were built on top of the intuition. The formalization is not circular — it is the completion of a definitional program.

Unlike the Church-Turing case, the PF did not have a pre-existing formal model of propagation when it began. The propagation primitive was informal from the start. The canonical definitions were constructed to repair that informality. `propagation.md` is therefore the first formalization of the primitive, not the re-derivation of a pre-existing model.

**Practical consequence:** every technical term used in `propagation.md` has a canonical definition that stands independently of this file as formal authority. `propagation.md` uses those terms; it does not redefine them.

---

## Propagation vs. Other Transport Phenomena

| Phenomenon | Causal front? | Coherence preserved? | Example |
|------------|--------------|----------------------|---------|
| **Wave propagation** | Yes — front bounded by causal velocity | Can be coherent or incoherent | Light in vacuum; sound in air |
| **Diffusion** | Effective equation often lacks a sharp front; microscopic carriers remain causal | Usually incoherent | Heat diffusion; dye in water |
| **Drift / advection** | Carrier motion is causal, but not necessarily a propagating disturbance front | Usually incoherent | Leaf in wind; charge drift in wire |
| **Instantaneous influence** | No — violates causal structure | N/A | Action at a distance |

Propagation is the causal, front-bounded transmission of distinguishable state change. Diffusion and drift are transport processes built from underlying causal microscopic dynamics, but they are not propagation claims unless the propagating disturbance, front, signal, or mode is specified.

---

## Causal Velocity and Propagation Speed

Every propagation context has a finite upper bound on controllable causal influence. In relativistic vacuum this bound is `c`; in effective media, lower characteristic speeds may describe particular excitations without replacing the fundamental front-velocity bound. The relevant propagation-speed claim must name the velocity concept:

- **Front/signal velocity:** bounded by the relevant causal/front velocity.
- **Massless vacuum modes** (null propagation): propagate at `c` on null geodesics.
- **Massive modes** (timelike propagation): particle/signal velocity is `v < c`.
- **Phase/group velocities:** require the taxonomy in `causal_velocity.md`; they can behave anomalously without carrying controllable causal influence.

Effective media can have lower excitation speeds (for example light's phase velocity in glass or electrical signal velocity in a cable), but the underlying front velocity remains bounded by `c`. In relativistic vacuum, propagation that saturates the local causal bound follows null worldlines; subluminal matter propagation follows timelike worldlines with finite proper time.

The local Lorentz-invariant `c` does not vary with position in vacuum. What varies is the coordinate propagation speed — the effective speed of light determined by the metric in GR.

---

## Coherence and Propagation

Propagation can be **coherent** (phase relations maintained) or **incoherent** (randomized phase):

- **Coherent propagation:** Relevant phase relations are preserved over the stated regime. A laser beam or a prepared electron wave packet can propagate coherently over finite distances/times. See `coherence.md`.
- **Incoherent propagation:** Phase relations randomize. Thermal radiation from a heated body propagates energy but loses phase structure.

The Medium's coherence rules (from `coherence.md`) determine whether a propagating mode maintains its structure.

---

## Mode and Propagation

A mode is an admissible pattern of a field under an evolution law (`mode.md`). Propagation is one behavior a mode or field disturbance can exhibit: it transmits state change through the Medium, subject to:

- Its **dispersion relation** from `mode.md` and `energy.md`: for a massless mode, `ω = ck` and `E = ℏω = ℏck = pc` (null propagation at `c`); for a massive mode, `ω² = (ck)² + (mc²/ℏ)²`, giving `E² = (pc)² + (mc²)²` (subluminal propagation at `v < c`).
- The **Medium's causal structure**: propagation follows causal paths determined by the metric or state-space structure.
- The **Medium's coherence rules**: whether propagation preserves phase structure.

Propagation does not create the mode. A free mode may propagate as a wave packet; a bound mode may propagate as a composite center-of-mass while its internal degrees of freedom remain confined.

---

## What Propagation Is NOT

- Not the same as motion. Motion is displacement; propagation is causal state transfer.
- Not a substance. Propagation is a property of the Medium's dynamics — not a thing that travels through the Medium.
- Not timeless. Propagation at `c` produces null worldlines (no proper time for null paths); propagation below `c` produces timelike worldlines with proper time.
- Not information alone. Propagation can occur without meaningful information content (e.g., thermal fluctuations).
- Not quantum tunneling. Tunneling appears fast but no controllable causal signal is transferred faster than `c`; the apparent superluminality of tunneling times does not carry new information. See `causal_velocity.md` for the full taxonomy.
- Not diffusion or drift as coarse-grained transport laws. Diffusion and drift are built from underlying causal microscopic motion, but they are not propagation claims unless a front, signal, disturbance, or mode is specified.

---

## Measurement Discipline

Every propagation claim must specify:

1. **What is propagating:** which mode (photon, phonon, electron wave packet, gravitational wave, etc.) or which field disturbance.
2. **Through which medium:** vacuum, material medium (with effective propagation speed), or field-theoretic state space.
3. **Which velocity concept:** phase velocity, group velocity, signal velocity, front velocity, or effective propagation speed. These are distinct — see `causal_velocity.md`.
4. **Coherence state:** coherent propagation (phase-preserving) or incoherent (phase-randomizing). See `coherence.md`.
5. **Boundary conditions:** open (infinite domain), confined (bound state, waveguide), or periodic.
6. **Regime:** vacuum field theory, GR (curved background), effective medium, condensed matter, or PF interpretation.
7. **Whether the claim is established physics or PF interpretation:** dispersion relations from standard QFT are established; the PF Medium framing of propagation is interpretation.

---

## Open Questions

| Question | Status |
|----------|--------|
| Does the PF Medium support propagation in more than 4D? | OPEN — depends on extra-dimension structure |
| Is the Medium's causal structure fundamentally discrete or continuous? | OPEN — PF does not yet specify spacetime quantization |
| Does the PF reproduce the QFT path integral? | OPEN — PF path-integral derivation not yet complete |
| What determines the dimensionality of the Medium's causal structure? | OPEN — topological considerations (k=1 principle) under investigation |

---

## Falsification Conditions

A propagation definition fails if:

1. **Controllable FTL signaling is demonstrated:** would falsify the causal velocity bound. See `causal_velocity.md`.
2. **A propagating disturbance has no definable causal ordering:** would falsify the Medium interpretation without necessarily falsifying standard field theory.
3. **A claimed propagating mode has no consistent evolution or dispersion relation in its stated regime:** would falsify that mode-propagation account.
4. **A coherence-preserving propagation claim fails under specified coherence metrics:** if a claimed coherent mode randomizes while all stated coherence-preservation conditions are met, the coherence account needs revision.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `mode.md` | Modes are one class of propagating structure; dispersion relations constrain their propagation behavior |
| `causal_velocity.md` | Propagation claims must distinguish front, signal, group, phase, and effective velocities; controllable causal influence is bounded |
| `medium.md` | Propagation is a dynamical behavior supported by the Medium's rule-structure |
| `coherence.md` | Coherent propagation preserves mode structure; incoherent propagation randomizes phase |
| `energy.md` | Propagation can transport energy; for energy eigenstates this is the Hamiltonian eigenvalue, while general disturbances require the full Hamiltonian/field content |
| `matter.md` | Matter modes can propagate as free wave packets or as composite bound states with confined internal degrees of freedom |
| `forces.md` | Forces change propagation paths, momenta, phases, or internal quantum numbers; gravity alters geodesic propagation through metric structure |
