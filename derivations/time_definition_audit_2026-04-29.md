# Time Definition Audit
*Fundamentals - `/mnt/d/Fundamentals/derivations/time_definition_audit_2026-04-29.md`*
*Target: `/mnt/d/Fundamentals/definitions/time.md`*
*Auditor: Codex*
*Date: 2026-04-29*

---

## Verdict

**HOLD.**

`definitions/time.md` is not ready for canonical status.

The draft has a useful seed: time should be treated operationally through ordered state changes, clock readings, and path-dependent proper time rather than as a universal external container. But it currently overclaims in three places:

- it defines proper time as an uncalibrated count of state changes,
- it treats the thermodynamic arrow as derived from `r^2` wavefront growth,
- it presents "present = wavefront" as if it survives relativity.

Those are not wording issues. They are physics-boundary issues.

---

## Finding Summary

| ID | Severity | Finding | Required correction |
|----|----------|---------|---------------------|
| T-01 | Medium | Undefined `observer` dependency and experience language | Use operational clock/worldline language; defer `observer` to `definitions/observer.md`. |
| T-02 | Critical | Proper time is not just `∫ dN(s)` | Define proper time by invariant interval / calibrated clock readings; state-change counts are an operational proxy only after calibration. |
| T-03 | Critical | Time dilation explanation risks preferred-frame "sampling path" language | Require equivalence to SR/GR proper-time formulae; avoid implying a preferred Medium rest frame. |
| T-04 | Critical | Arrow of time is not derived from `r^2` wavefront growth | Mark as PF interpretation or hypothesis unless low-entropy boundary conditions, coarse-graining, and entropy measure are specified. |
| T-05 | Critical | "Present = wavefront" is not canonical | Relativity of simultaneity blocks a universal present wavefront. Move to speculative/open section. |
| T-06 | Medium | Photon/time wording remains unsafe | Say null worldlines have zero proper time; do not assign experience or observer status to photons. |
| T-07 | Medium | Quantum time/operator claim is too broad | Say standard QM treats time as a parameter; do not claim time is never an observable without caveats. |
| T-08 | Medium | Measurement discipline is incomplete | Add clock model, frame/convention, metric/interval, regime, calibration, and uncertainty. |
| T-09 | Medium | Falsification criteria are not well-formed | Replace preferred-rest and broad-arrow criteria with SR/GR reduction, clock-comparison tests, and thermodynamic-arrow assumptions. |

---

## Detailed Findings

### T-01 - Undefined `observer` dependency and experience language

**Severity: Medium**

The definition says:

> Time is the sequential record of state changes experienced by an observer embedded in a propagation Medium.

`observer` is not canonical yet (`definitions/observer.md` does not exist), and "experienced" pulls the definition toward consciousness/phenomenology before the framework has earned that bridge.

This is especially risky because `definitions/coherence.md` explicitly prevents consciousness from being smuggled into foundational definitions.

**Required correction:**

Use clock/worldline/indexing language:

```text
Time is the ordering and metric of state changes along a physical history or worldline.
```

Then add:

```text
Observer is used operationally here to mean a physical clock or record-bearing subsystem. A canonical observer definition is deferred to definitions/observer.md.
```

---

### T-02 - Proper time is not just state-change count

**Severity: Critical**

The draft defines:

```text
τ[observer] = ∫_path dN(s)
```

where `dN(s)` is a count of distinguishable state changes.

This does not yet reproduce relativistic proper time. Proper time is the invariant time measured by an ideal clock along a timelike worldline. In flat spacetime:

```text
dτ² = dt² - (1/c²) d\vec{x}²
```

up to sign convention, and in GR:

```text
dτ² = -g_{\mu\nu} dx^\mu dx^\nu / c²
```

for timelike intervals.

A count of state changes can operationalize clock time only after specifying the clock, transition frequency, calibration, environmental corrections, and relation to the metric interval.

**Required correction:**

Make `∫ dN(s)` an operational clock proxy, not the formal definition.

---

### T-03 - Time dilation explanation risks preferred-frame language

**Severity: Critical**

The draft says observers moving relative to each other "sample different cross-sections of the wavefront" and that time dilation comes from different sampling paths through a "common field".

This can be read as a preferred propagation-field frame. `definitions/medium.md` explicitly requires Lorentz compatibility and no preferred frame unless physically broken and testable.

Time dilation is already formalized by the path-dependent invariant interval. Any PF interpretation must reduce exactly to SR/GR clock-comparison results.

**Required correction:**

State the standard reduction first:

```text
Different timelike worldlines between events can have different accumulated proper time.
```

Then add PF interpretation only as an interpretation:

```text
PF interprets this as different histories through the Medium's causal-dynamical structure, not as motion against a preferred rest frame.
```

---

### T-04 - Arrow of time is over-derived

**Severity: Critical**

The draft says:

> This is the second law of thermodynamics, derived from the Medium's geometry.

The `r^2` surface-growth argument is not a derivation of the second law. The thermodynamic arrow requires at least:

- a low-entropy boundary condition,
- a coarse-graining or entropy functional,
- dynamics that make high-entropy macrostates overwhelmingly typical,
- an explanation of why the retrodictive direction is not treated symmetrically.

Spherical wavefront growth is relevant intuition, but not a second-law proof.

**Required correction:**

Demote to:

```text
PF hypothesis / interpretation: for localized disturbances in extended media, outward propagation supplies one geometric mechanism that can align with entropy increase under suitable coarse-graining and boundary conditions.
```

---

### T-05 - "Present = wavefront" is not canonical

**Severity: Critical**

The draft says:

> The past is the region already traversed by the propagation wavefront. The future is the region not yet reached. The present is the current wavefront.

This is not compatible with relativity as a canonical global definition. In SR and GR, simultaneity is observer/frame dependent, and generic curved spacetimes may not admit a unique global present slice.

It may be useful as a PF metaphor for a local causal frontier or for a specific cosmological model, but it cannot be the canonical definition of time.

**Required correction:**

Move this to Open Questions / Speculative PF Interpretation and state:

```text
The canonical definition does not assert a universal present wavefront.
```

---

### T-06 - Photon/time wording remains unsafe

**Severity: Medium**

The draft improves the old "observer traveling at c" error by saying no massive embedded observer travels at causal velocity. But it still says:

> This is structurally why photons do not experience time.

Photons do not have a rest frame, and "experience" is not defined.

**Required correction:**

Use:

```text
The proper time along an ideal null worldline is zero. This does not mean photons are observers or have experience.
```

---

### T-07 - Quantum time/operator claim is too broad

**Severity: Medium**

The draft says:

> Time is a relational property of the observer-Medium interface, not a system observable.

In standard nonrelativistic quantum mechanics, time is usually an external parameter, not an operator like position. But there are time observables in restricted senses, including arrival-time and clock POVM treatments. The draft overstates.

**Required correction:**

Use:

```text
In standard quantum mechanics, time usually appears as an external parameter rather than a universal self-adjoint operator. Specific time observables require separate clock or measurement models.
```

---

### T-08 - Measurement discipline is incomplete

**Severity: Medium**

The draft lists only:

1. proper vs coordinate time,
2. reference observer/clock,
3. resolution.

That is not enough for canonical status.

**Required correction:**

Every time claim should specify:

- proper time, coordinate time, or ordering relation,
- clock model / physical transition,
- worldline or reference frame,
- metric or effective geometry,
- regime: SR, GR, thermodynamic, quantum, cosmological, or PF analogy,
- calibration and uncertainty,
- whether arrow/directionality is part of the claim.

---

### T-09 - Falsification criteria are not well-formed

**Severity: Medium**

The first falsifier says:

> A clock at rest in the Medium records zero proper time while the Medium has active propagation...

"At rest in the Medium" is unsafe because the canonical Medium definition avoids preferred-frame ether language.

The third falsifier says the arrow must be derived from propagation geometry. But the draft does not supply such a derivation, so this currently falsifies the draft's overclaim rather than the concept of time.

**Required correction:**

Use criteria such as:

- canonical time definition must reduce to SR proper-time clock comparisons,
- must reduce locally to GR proper time in curved spacetime,
- must distinguish coordinate time from proper time in all claims,
- any thermodynamic-arrow claim must specify entropy functional, boundary condition, and coarse-graining,
- any PF "present/wavefront" claim must be model-specific and not contradict relativity of simultaneity.

---

## Minimal Rewrite Target

A safer canonical seed would be:

> Time is the ordering and metric of state changes along physical histories. Proper time is the invariant duration measured by an ideal clock along a timelike worldline. Coordinate time is a convention for labeling events within a chosen reference frame or foliation. PF interprets both as records of propagation-compatible state change within the Medium, but this interpretation must reproduce SR/GR clock comparisons and must not introduce a preferred frame.

This seed is less poetic, but it is compatible with the canonical Medium and causal-velocity definitions.

---

## Required Fix Order

1. Replace the top definition with the minimal rewrite target.
2. Move "time is what change looks like from inside the Medium" to a Plain-Language section.
3. Add observer deferral language.
4. Replace `τ = ∫ dN(s)` with SR/GR proper-time formulae plus a calibrated-clock proxy note.
5. Demote the `r^2` arrow argument to PF interpretation / hypothesis.
6. Move "present = wavefront" to Open Questions and explicitly reject a universal present.
7. Replace photon-experience language with null-worldline proper-time language.
8. Replace the QM operator row with a standard-QM parameter caveat.
9. Expand measurement discipline and falsification criteria.

---

## Final Status

`definitions/time.md`: **HOLD**.

Do not mark canonical until a revised draft passes these findings.
