# Codex Audit: Coherence and Causal Velocity Definitions
*Fundamentals - /mnt/d/Fundamentals/derivations/coherence_causal_velocity_audit_2026-04-28.md*
*Auditor: Codex*
*Targets: `/mnt/d/Fundamentals/definitions/coherence.md`; `/mnt/d/Fundamentals/definitions/causal_velocity.md`*
*Date: 2026-04-28*

---

## Verdict Summary

| File | Verdict | Reason |
|------|---------|--------|
| `definitions/coherence.md` | **HOLD** | Useful seed, but it conflates phase coherence, structural stability, biological organization, and P1 metrics under one definition. |
| `definitions/causal_velocity.md` | **HOLD** | Strong core definition, but it conflates causal/front velocity with effective signal, phase, and group velocities in material media. |

Do not mark either file canonical until the findings below are resolved.

---

## Shared Gate

Both files were pre-labeled `CANONICAL v1.0` before Codex audit. That repeats the same failure mode the Medium definition audit corrected.

**Finding S-01 - Premature canonical status**

**Severity: High**

Both files say canonical while also saying Codex audit is pending. A file cannot be canonical and pending audit at the same time.

**Required correction:** status must be `HOLD - pending Codex finding closure` until a follow-up audit passes.

---

## Audit: `definitions/coherence.md`

### C-01 - Definition is useful but too narrow for all later uses

**Severity: High**

Line 10 defines coherence as "the degree to which multiple propagation modes maintain stable phase relationships with each other." This is valid for optical/wave coherence, but too narrow for all uses in the framework.

The file later applies coherence to particles, atoms, organisms, EEG, and consciousness. Those domains require at least three distinct notions:

1. **Phase coherence** - stable phase relationships.
2. **Quantum coherence** - basis-dependent off-diagonal density-matrix structure.
3. **Structural/dynamical coherence** - persistence of a stable pattern under evolution.

These may be related, but they are not identical.

**Verdict:** HOLD until the definition explicitly separates these levels.

### C-02 - "High coherence" examples overreach

**Severity: High**

Lines 28, 53, and 57 use atoms, molecules, organisms, and biological structures as direct examples of "high coherence." This risks equivocation.

Atoms and molecules can be stable structures without being high phase-coherence objects in the same sense as lasers or superconductors. Organisms are sustained non-equilibrium systems, but calling them "high coherence" requires a defined biological coherence metric.

**Required correction:** separate "stable mode" from "phase coherence" and state which metric applies in each domain.

### C-03 - Axiom 3 threshold claim is stated as more closed than current truth allows

**Severity: Medium**

Line 31 says the particle spectrum is the set of modes that cross the coherence threshold. This matches PF intent, but the exact threshold functional remains an open frontier in `AGENTS.md` and `ACTIVE_ISSUES.md`.

**Required correction:** mark this as PF claim/open formalization, not canonical definition.

### C-04 - Quantum coherence statement omits basis dependence

**Severity: Medium**

Line 45 says quantum coherence is "the off-diagonal element" of density matrix `rho`. More precisely, coherence is basis-dependent off-diagonal structure in a density matrix, not one element and not an absolute basis-free scalar unless a measure and preferred basis are specified.

**Required correction:** define the basis and measure, or state this as an example rather than the definition.

### C-05 - P1 measurement section is not appropriate in a canonical definition

**Severity: High**

Lines 62-70 embed a live P1 biofeedback value (`76%`) and interpret it as phase stability "76% of the time." This may be meaningful inside the P1 project, but it is not suitable for a foundational physics definition unless the measurement pipeline, estimator, windowing, reference signal, and validation are specified.

**Required correction:** move P1-specific material to a separate application note. The canonical definition may say "P1 attempts to measure an applied coherence proxy" but should not bake in a live value.

### C-06 - EEG gamma/insight line is too strong

**Severity: Medium**

Line 58 calls EEG gamma burst at insight "the Medium's threshold effect visible in brain." That is interpretive and too direct. It may be an analogy or applied hypothesis, not canonical definition.

**Required correction:** mark as "PF application hypothesis" or remove from definition.

### C-07 - Consciousness caution is good and should remain

**Severity: Pass**

Line 92 correctly says coherence is not synonymous with consciousness and is not sufficient. This aligns with the final Medium audit.

---

## Required Fix for Coherence

Use this structure:

1. Minimal definition:
   `Coherence is stable relational structure among states under evolution. In wave systems this is phase stability; in quantum systems it is basis-dependent off-diagonal structure; in dynamical systems it is persistence of organized correlations.`

2. Separate sections:
   - Optical/phase coherence.
   - Quantum coherence.
   - Dynamical/structural coherence.
   - PF Axiom 3 coherence threshold as open formal target.

3. Move P1 metrics and consciousness discussion to application/speculation sections.

---

## Audit: `definitions/causal_velocity.md`

### V-01 - Core definition survives

**Severity: Pass**

Line 10 is strong:

> The causal velocity of a medium is the maximum speed at which a controllable causal influence can propagate through it.

This should remain the canonical seed.

### V-02 - "Most important single number" is rhetoric, not definition

**Severity: Low**

Line 12 says causal velocity is the most important single number characterizing any propagation medium. This may be true in PF narrative terms, but it is not needed in the definition and may overstate relative to state space, dynamics, symmetry, and coherence.

**Required correction:** remove or rephrase as "a central parameter."

### V-03 - Energy-scale claim is not justified

**Severity: High**

Line 26 says causal velocity "sets the energy scale" through `E = hf` and `lambda nu = v_causal`. This is not generally correct. `E = hf` ties energy to frequency through Planck's constant; velocity enters dispersion relations and wavelength/frequency relations, but causal velocity alone does not set an energy scale.

**Required correction:** change to "relates wavelength, frequency, and dispersion for modes in that medium" unless a specific derivation is supplied.

### V-04 - "Light travels at c because photons are massless" is acceptable; "maximum efficiency" is not

**Severity: Medium**

Line 37 says photons travel at `c` because they are massless. That is acceptable in standard relativistic language. "They couple to the Medium at maximum efficiency" is undefined and should be removed.

**Required correction:** use: "Massless excitations propagate on null cones in vacuum."

### V-05 - Material-media table conflates causal velocity with effective signal/phase/group speeds

**Severity: Critical**

Lines 43-55 list glass, water, copper, neural axons, and sound as having their own causal velocities. This needs much sharper language.

There are at least three levels:

1. **Fundamental causal/front velocity** - no controllable influence outruns this.
2. **Effective signal velocity in a medium** - speed of a pulse or excitation in an effective theory.
3. **Phase/group velocity** - can differ from signal/front velocity and can be superluminal or subluminal without allowing FTL messaging.

Saying "glass causal velocity ~c/1.5" is unsafe unless "causal velocity" is explicitly defined as an effective medium signal speed, not fundamental front velocity. The file later says front velocity remains causal, so the current wording is internally unstable.

**Required correction:** split `fundamental causal velocity` from `effective propagation velocity`. Use "effective propagation speed" for glass/water/copper unless front velocity is explicitly meant.

### V-06 - Propagation ratio formula conflicts with the definition

**Severity: High**

Lines 61-65 define `n = v_causal / v_signal`. This is fine as an abstract ratio, but the examples use optical refractive index where standard `n = c / v_phase`, not necessarily causal/front velocity divided by signal velocity.

**Required correction:** define separate ratios:

- `n_phase = c / v_phase` for optical phase index.
- `r_eff = v_signal / v_causal` for effective propagation ratio.

Avoid reusing `n` for both.

### V-07 - Threshold claims overgeneralize causal velocity

**Severity: Medium**

Lines 79-89 say neural/cognitive transitions occur when signals approach causal velocity. This is not established. Neural criticality and cognitive bandwidth are plausible analogies, but they are not the same as a signal reaching a causal velocity bound.

**Required correction:** mark neural/cognitive examples as PF analogies or applied hypotheses, not canonical causal-velocity definition.

### V-08 - Falsification condition about vacuum causal velocity varying needs precision

**Severity: Medium**

Line 132 says the concept fails if vacuum causal velocity varies. In GR, coordinate speeds can vary while local Lorentz invariance remains intact. The falsifier should be a local Lorentz-invariance violation or controllable superluminal signaling, not any coordinate-dependent variation.

**Required correction:** use: "local Lorentz-invariance violation or preferred-frame effect inconsistent with current bounds."

---

## Required Fix for Causal Velocity

Use this structure:

1. Minimal definition:
   `Causal velocity is the upper bound on controllable causal influence in a specified effective medium or theory. In relativistic vacuum this is local c; in effective media, lower characteristic speeds may bound particular excitations without replacing the fundamental front-velocity constraint.`

2. Separate:
   - Fundamental/local causal velocity.
   - Effective propagation speeds.
   - Phase/group velocities.
   - Front/signal velocity.

3. Remove unsupported "sets energy scale" and "maximum efficiency" language.

---

## Medium Role Independence Check

The final Medium definition lists operational roles: causal, state-bearing, propagative, dynamic, coherent, geometric, quantizing, quantum-compatible, Lorentz-compatible, measurable.

These roles are **not all primitive**, but they are not fully redundant either. The correct structure is:

| Role | Independent? | Reason |
|------|--------------|--------|
| Causal | Yes | A partial/causal order can exist without specifying state contents. |
| State-bearing | Yes | A state space can exist without causal propagation. |
| Dynamic | Yes | Evolution rules are not implied by a state space alone. |
| Propagative | Partly dependent | Requires state + dynamics + some locality/transport structure, but adds actual disturbance transport. |
| Coherent | Partly dependent | Requires states + dynamics, but adds stable relational persistence. |
| Geometric | No as primitive; yes as additional structure | Causal + propagative does not automatically imply differentiable geometry; discrete graphs and automata are counterexamples. Geometry is extra structure or an emergent property. |
| Quantizing | No as primitive; yes as constraint | Discrete spectra do not follow from propagation alone; they require boundary/operator/coherence conditions. |
| Quantum-compatible | Independent from mere quantizing | A classical discrete system can quantize without Hilbert-space nonseparability. |
| Lorentz-compatible | Constraint, not primitive role | It specializes the causal/geometric structure for relativistic domains. |
| Measurable | Epistemic gate, not ontological role | It governs scientific admissibility, not what the Medium is. |

**Conclusion:** The Medium definition should not call all roles independent primitives. The minimal core is:

1. state-bearing,
2. dynamic,
3. causal/local,
4. propagation-capable,
5. coherence/stability-capable.

Geometry, quantization, and quantum compatibility are additional constraints required for our universe, not logically forced by the bare concept of a medium.

This does **not** invalidate `definitions/medium.md`, because that file defines the Medium of physical reality, not an abstract medium in the weakest possible sense. But downstream writers must not claim all roles are independent axioms.

---

## Task 1 Final Verdict

| Target | Verdict |
|--------|---------|
| `definitions/coherence.md` | **HOLD** |
| `definitions/causal_velocity.md` | **HOLD** |
| Medium role independence | **PARTIAL** - roles are operationally useful but not all independent primitives. |

No status upgrade is authorized.
