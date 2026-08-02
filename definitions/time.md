# Time
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md` Derived Quantity 1*
*Dependencies: `observer.md` CANONICAL v1.0; `state.md` CANONICAL v1.0; `causal_velocity.md` CANONICAL v1.0*
*Audits: `derivations/time_definition_audit_2026-04-29.md`; `derivations/time_pre_dispatch_audit_2026-04-29.md`; `derivations/time_definition_final_audit_2026-04-29.md`*

---

## The Definition

**Time is the ordering and metric of state changes along physical histories.**

Proper time is the invariant duration measured by an ideal clock along a timelike worldline. Coordinate time is a convention for labeling events within a chosen reference frame or foliation. The Propagation Framework interprets both as records of propagation-compatible state change within the Medium, but this interpretation must reproduce SR/GR clock comparisons and must not introduce a preferred frame.

Plain language (not the formal definition):

> Time is what the record of change looks like from along a path.

*Observer* is used operationally in this file to mean a physical clock or record-bearing subsystem following a worldline. The canonical observer definition is `definitions/observer.md`.

---

## On Circularity

*Added 2026-07-29 from DeepSeek literature depth pass (`inbox/2026-07-29-deepseek-time-literature-depth-pass.md`)*

The definition "time is the ordering and metric of state changes along physical histories" faces a classical objection: does "change" presuppose a temporal ordering, making the definition circular?

### Historical precedent: Leibniz vs. Clarke (1715-1716)

This is not a new objection. It is exactly the Leibniz-Clarke debate:

- **Leibniz (relationalist):** Time is the "order of successions" — a derived relation between events, not a container.
- **Clarke (absolutist, Newtonian):** "Succession" already implies temporal order, so Leibniz's definition is circular.

Leibniz's reply: succession is a logical-ordinal relationship, not a temporal-flow relationship. Two events can be ordered (one before the other) without "time" existing independently — the ordering IS the temporal structure.

### Three modern escape routes

1. **Configuration-space (Barbour):** Define "change" as "different points in configuration space." A history is a curve through configuration space. No temporal ordering primitive is needed — the ordering falls out of the curve parameter. Cost: requires a global configuration space and a distinguished measure.

2. **Thermodynamic emergence (Rovelli):** At the fundamental level (Wheeler-DeWitt), there is no time variable. Time emerges from coarse-graining of quantum gravitational degrees of freedom. The arrow requires a low-entropy boundary condition (Past Hypothesis). **This is the closest relative to the PF approach** — both treat time as derived from state-change records.

3. **Operational:** Time is whatever clocks measure. The SI second is 9,192,631,770 hyperfine transitions of Cs-133. Circularity is sidestepped by grounding in a specific physical process. Cost: can't explain why different clocks agree or address the arrow of time.

### Assessment for the PF definition

The PF definition is closest to the Leibniz-Rovelli lineage. The potential circularity is **real but manageable:**

1. **The "metric" component helps.** The definition includes both ordering AND metric. "Metric" implies a measure of separation between state changes — an extra primitive that the Leibniz formulation lacked.

2. **"State change" can be defined without temporal ordering** if states are defined in configuration space. The PF Medium has states {S₁, S₂, ...}. The "change" from Sᵢ to Sⱼ is the difference, not the temporal ordering. The ordering is then the causal-propagation structure of the Medium (Barbour escape).

3. **The honest vulnerability:** If PF "propagation" itself assumes time (propagation takes time), then the definition is circular at a deeper level. This is equivalent to the Wheeler-DeWitt problem: in a fundamentally timeless theory, what selects the foliation? **This remains open.** The PF must be able to define propagation without presupposing time.

### What this subsection does NOT claim

- Does NOT claim the circularity is resolved. The deep vulnerability (propagation presupposing time) is flagged, not closed.
- Does NOT change the canonical status of the definition. The definition is operationally useful regardless of whether the circularity is fully resolved.
- Does NOT add a new axiom or postulate. The configuration-space approach is a reading of existing PF structure, not a new assumption.

---

## Formal Structure

### Proper Time

In flat spacetime (SR), the proper time accumulated along a timelike worldline between events A and B is:

```text
dτ² = dt² - (1/c²)(dx² + dy² + dz²)

τ_AB = ∫_A^B dτ
```

In curved spacetime (GR), the proper time is:

```text
dτ² = -g_μν dx^μ dx^ν / c²
```

for timelike intervals (`g_μν dx^μ dx^ν < 0` in the (-+++) signature).

Proper time is path-dependent. Two clocks following different worldlines between the same two events accumulate different proper times. This is not a deformation of time; it is a direct consequence of the Lorentz/metric structure.

**PF interpretation:** Proper time counts propagation-compatible state changes along a timelike path through the Medium. A calibrated physical clock is an operational proxy for `dτ` only after specifying the transition frequency, environmental corrections, and relation to the invariant interval. The raw state-change count `∫ dN(s)` is not a definition of proper time; it is a measurement model that must be validated against SR/GR clock comparisons.

### Coordinate Time

Coordinate time `t` is a labeling convention for events across a chosen foliation or reference frame. It is useful for bookkeeping but has no more fundamental status than any other coordinate choice. Under a Lorentz boost, coordinate time mixes with the spatial coordinate.

The SI second is defined by 9,192,631,770 hyperfine transitions of cesium-133 at rest in zero field. This fixes the unit, not the concept. The second is an operational realization of `dτ` for a specific clock at rest in weak gravity.

### Path-Dependence (Time Dilation)

Different timelike worldlines between the same events can have different accumulated proper times:

```text
τ_clock_1 ≠ τ_clock_2   (if worldlines differ)
```

The standard SR formula for a clock moving at constant velocity `v` relative to a coordinate frame:

```text
dτ = dt √(1 - v²/c²)
```

**PF interpretation:** Different worldlines sample the Medium's causal-dynamical structure along geometrically different paths. This is not motion relative to a preferred Medium rest frame. The PF account must reduce exactly to the SR/GR clock-comparison formulas; any preferred-frame language is unsafe unless a physical symmetry-breaking mechanism is identified and testable.

### Null Worldlines

The proper time along an ideal null worldline is zero:

```text
g_μν dx^μ dx^ν = 0   →   dτ = 0
```

This is the precise statement. Massless excitations (photons in vacuum) follow null worldlines. Zero proper time is a geometric property of the path. It is not a statement about experience or observation by the excitation. No massive clock-bearing subsystem follows a null worldline.

---

## Time's Arrow

The arrow of time — the observed asymmetry between past and future — requires:

1. a low-entropy boundary condition (e.g., early universe),
2. an entropy functional or coarse-graining scheme,
3. dynamics that make high-entropy macrostates overwhelmingly typical under that measure.

The time-reversal symmetry of fundamental dynamics (up to CPT and weak-force effects) means the arrow is not built into the microscopic equations. It arises from the boundary condition and the coarse-graining.

**PF interpretation (hypothesis, not canonical derivation):** For localized disturbances in an extended Medium, outward propagation from a compact source distributes state changes over a growing surface. Under suitable coarse-graining and with a low-entropy boundary condition, this geometric expansion is consistent with entropy increase. Whether PF can derive the thermodynamic arrow from propagation geometry alone — without assuming a low-entropy initial condition — is an open question. The second law is not derived here.

---

## Time and Quantum Mechanics

In standard nonrelativistic quantum mechanics, time appears as an external parameter, not a universal self-adjoint operator. Pauli's theorem constrains self-adjoint time operators for systems with semi-bounded Hamiltonians. Specific time observables exist in restricted settings (arrival-time, time-of-flight, clock POVMs) and require separate measurement models.

**PF interpretation:** The PF treats time as a derived relational property — the record of state-change ordering along a worldline — rather than a universal parameter external to the system. This is compatible with the standard QM treatment as a parameter; it does not require a universal time operator.

---

## Open Questions and Speculative PF Interpretations

### Present as Local Causal Frontier (speculative)

The intuition that "the present is the propagation wavefront" — the frontier boundary between states already reached and states not yet reached — works cleanly for a single observer's worldline: their local causal past is the region their past light cone has already intersected.

This cannot be a global canonical definition. Relativity of simultaneity means different inertial observers define different global present slices. Generic curved spacetimes may not admit a unique global foliation.

Any extension requires specifying which observer's wavefront, or choosing a foliation, or restricting to a specific cosmological model. Until then: local intuition, not global definition.

| Question | Status |
|----------|--------|
| Can PF derive the thermodynamic arrow from propagation geometry without assuming a low-entropy initial condition? | OPEN |
| Does the "local causal frontier" concept for a worldline recover standard SR/GR proper time when made precise? | OPEN |
| Does the PF local-causal-frontier picture extend cleanly to quantum field theory? | OPEN |
| Is the Big Bang a boundary condition of propagation rather than a "beginning of time"? | OPEN — speculative; needs model |
| Are there multiple propagation fields with multiple arrows of time? | OPEN — speculative |

---

## What Time Is NOT

- Not a universal external container in which events exist. Events are state changes; time is their ordering along a path.
- Not a substance or medium. The Medium is the substrate; time is a derived relational property of paths through it.
- Not reversible for embedded clock-bearing subsystems under thermodynamic coarse-graining, even though fundamental dynamics are time-symmetric.
- Not a global universal present slice — simultaneity is frame-dependent in SR and generic GR spacetimes.
- Not a preferred-frame property — the PF account must not imply a preferred Medium rest frame.
- Not a universal quantum observable — it is a parameter in standard QM; clock observables are separate restricted models.
- Not phenomenological "experience" at the level of this physical definition. Clock readings are physical registrations.

---

## Measurement Discipline

Every time claim must specify:

1. **Type:** proper time (path integral of `dτ`), coordinate time (frame/foliation label), or ordering relation (before/after without metric).
2. **Clock model:** which physical process realizes the time unit (e.g., cesium hyperfine, optical lattice, GPS).
3. **Worldline or reference frame:** which path or foliation anchors the time label.
4. **Metric / effective geometry:** flat SR, curved GR, effective medium approximation, or cosmological metric.
5. **Regime:** SR, GR, thermodynamic, quantum, cosmological, or PF interpretation/analogy.
6. **Calibration and uncertainty:** systematic effects (gravitational redshift, velocity, environment) and measurement precision.
7. **Arrow:** whether the claim involves a direction of time; if so, which entropy functional, boundary condition, and coarse-graining scheme.

"Time stops for photons" is a statement about zero proper time along a null worldline (Type 1). It is not a statement about coordinate time, which is undefined along a null path.

---

## Falsification Conditions

A time definition fails if:

1. **SR reduction fails:** the definition must reduce to `dτ² = dt² - (1/c²)|dx|²` for inertial observers in flat spacetime.
2. **GR reduction fails:** must reduce to `dτ² = -g_μν dx^μ dx^ν / c²` for timelike worldlines in curved spacetime.
3. **Clock comparison fails:** the operational clock proxy must agree with SR/GR proper-time predictions to the precision of existing tests (airborne clocks, GPS satellites, muon lifetime in beams).
4. **Arrow claim is unfalsifiable:** any PF thermodynamic-arrow claim must specify entropy functional, boundary condition, and coarse-graining, or it is not a falsifiable result.
5. **Preferred frame introduced:** any PF realization that requires a preferred Medium rest frame fails unless the preferred-frame effect is identified, testable, and bounded against current Lorentz-invariance experiments.
