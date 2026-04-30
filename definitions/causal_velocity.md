# Causal Velocity
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Audits: `derivations/coherence_causal_velocity_audit_2026-04-28.md`; `derivations/causal_velocity_definition_final_audit_2026-04-29.md`*

---

## The Definition

**Causal velocity is the upper bound on controllable causal influence in a specified medium or theory.**

In relativistic vacuum, this bound is the local Lorentz-invariant constant `c`. In effective media, lower characteristic speeds may bound particular excitations without replacing the fundamental front-velocity constraint of the underlying theory.

Short form:

> Causal velocity is the speed limit of cause and effect in a given physical context.

---

## Distinct Velocity Concepts

These must not be conflated:

| Concept | Symbol | Definition | Can exceed c? |
|---------|--------|------------|---------------|
| **Fundamental causal velocity** | `c` | The local Lorentz-invariant upper bound on controllable influence in vacuum | No |
| **Front velocity** | `v_front` | The leading edge of any causal disturbance in a medium; the first possible carrier of new influence | Never exceeds `c` |
| **Signal / information velocity** | `v_signal` | Speed of a controllable message or information-carrying excitation | Never exceeds `v_front` |
| **Group velocity** | `v_group` | Wave-packet envelope speed, usually `dω/dk` | Can appear `> c` or negative in anomalous dispersion; not automatically a signal speed |
| **Phase velocity** | `v_phase` | Speed of a wave's phase surface | Can exceed `c` (carries no information) |
| **Effective propagation speed** | `v_eff` | Characteristic speed of excitations in an effective medium (not a causal bound on the underlying theory) | Usually below `c` for material excitations; apparent superluminal quantities must be classified as phase/group, not signal/front |

Any causal-velocity claim must name which concept it is using.

---

## The Vacuum Instance

In vacuum, the causal velocity is:

**c = 299,792,458 m/s** (exact, by SI definition since 1983)

This is not "the speed of light in particular." It is the fundamental causal velocity of the vacuum. Massless excitations (photons, gravitons in linearized GR) propagate on null cones — they travel at `c` because they have no rest mass and the null cone is the causal boundary. Massive particles always travel at `v < c`.

> Massless excitations propagate on null cones in vacuum. The null cone is defined by `c`, not by light.

The vacuum causal velocity is also what relates wavelength, frequency, and dispersion for modes propagating in vacuum: `λν = c`, from which dispersion relations follow. It does not by itself set an energy scale; that requires additional parameters (Planck's constant, mass, coupling).

---

## Effective Propagation Speeds in Media

The following are **effective propagation speeds** — speeds of particular excitations in particular materials. They are not the causal velocity of the underlying theory; the front velocity of any disturbance in these media still cannot exceed `c`.

| Medium | Effective propagation speed | Note |
|--------|----------------------------|-------|
| Vacuum | `c = 299,792,458 m/s` | Fundamental causal velocity; also the front velocity |
| Glass (optical) | `v_phase ≈ c/1.5` | Phase velocity of light; front velocity still `c` |
| Water | `v_phase ≈ c/1.33` | Phase velocity of light in water |
| Copper wire (electrical) | `v_signal ≈ 0.6c–0.7c` | EM signal propagation; velocity factor of the line |
| Myelinated neural axon | `v_signal ≈ 100 m/s` | Action potential conduction velocity |
| Unmyelinated neural axon | `v_signal ≈ 1 m/s` | Action potential conduction velocity |
| Sound in air | `v_sound ≈ 343 m/s` | Compression wave; governed by acoustic physics |

**The invariant:** the fundamental causal velocity `c` applies to all these media at the level of the underlying field theory. The listed speeds are effective excitation speeds within an approximate description. Cherenkov radiation occurs when a charged particle exceeds the *phase* velocity of light in a medium (`c/n`) — not the vacuum `c` — which is why it is physically allowed.

---

## Velocity Ratios

**Phase refractive index** (optics):

```text
n_phase = c / v_phase
```

When `n_phase > 1`, the phase velocity is subluminal. When `n_phase < 1` (anomalous dispersion), the phase velocity is superluminal — this does not permit signaling.

**Effective propagation ratio** (general media):

```text
r_eff = v_signal / c
```

This is the ratio of a signal's actual speed to the vacuum causal bound. `r_eff = 1` means the signal saturates the vacuum causal bound, as massless vacuum excitations do. In material or effective media, `r_eff` only reports how the excitation speed compares to `c`; it does not define a new fundamental causal bound. `r_eff << 1` means the medium strongly shapes the signal.

Do not use `n` for both ratios simultaneously, as they differ by inversion and measure different physical quantities.

---

## What Causal Velocity Does

| Role | Meaning |
|------|---------|
| Defines causal structure | Partitions events into "can influence" and "cannot influence" — the light cone structure |
| Bounds controllable information transfer | No message carrying new information travels faster than `v_front ≤ c` |
| Constrains dispersion relations | Relates wavelength, frequency, and group/phase velocity for modes in that medium |
| Marks causal boundary | In theories where the bound is approached or saturated, causal-horizon or threshold behavior can appear; this is not a universal phase-transition rule |

---

## Phase Transitions Near Propagation Thresholds

When an excitation's speed crosses a relevant effective threshold in its medium, qualitative effects can occur:

| System | Threshold | Effect |
|--------|-----------|--------|
| Optical medium | Charged particle exceeds `v_phase = c/n` | Cherenkov radiation — coherent shockwave |
| Plasma | Signal approaches plasma frequency cutoff | Reflection; no propagation below cutoff |

**PF analogies (not canonical causal-velocity claims):**  
The Propagation Framework hypothesizes that neural criticality and cognitive-bandwidth saturation may function as *analogues* of causal-velocity thresholds in their respective effective theories — meaning qualitative reorganization occurs as activity rates approach medium-specific limits. These are applied hypotheses in the PF biological and cognitive layers, not consequences of the present definition. They should not be cited as established causal-velocity results.

---

## Velocity Discipline

Not all apparently fast phenomena violate the causal velocity:

| Phenomenon | Faster than `c`? | Explanation |
|-----------|-----------------|-------------|
| Phase velocity in medium | Sometimes `> c` | Carries no information; front velocity is causal |
| Group velocity in anomalous dispersion | Can appear `> c` | Signal/front velocity does not exceed `c` |
| Quantum tunneling time | Apparently fast | No controlled information transferred |
| Entanglement correlations | Non-local but not FTL | Pre-existing coherence structure; no new causal signal |
| Cherenkov radiation | Particle `> c/n`, not `> c` | Exceeds medium phase velocity, not vacuum `c` |

**The invariant:** *controllable causal influence* — the ability to send a chosen message — never exceeds the front velocity, which never exceeds `c`.

---

## What Causal Velocity Is NOT

- Not "the speed of light" specifically — `c` is the vacuum causal velocity; it is defined independently of light
- Not the effective signal speed in all media — material media have lower effective propagation speeds that are not the causal velocity of the underlying theory
- Not a limit on phase velocity — phase velocity can be superluminal without violating causality
- Not the same as group velocity — group velocity can behave anomalously in dispersive media
- Not "the most important single number" in isolation — causal structure, state space, dynamics, and coherence/stability conditions are all required to characterize a medium

---

## Relation to Medium Definition

The causal velocity is what gives the Medium causal structure (property 1 in `definitions/medium.md`):

> The Medium defines a partial order on events — what can influence what — with light cones defined by the fundamental causal velocity.

Without a finite causal velocity, there is no light-cone structure, no distinction between past and future light cones, and no causal physics.

---

## Axiom 2 Boundary

**Axiom 2:** Every medium has a finite causal velocity.

Canonical interpretation:

> The upper bound on controllable causal influence in any PF medium is finite. Signals, modes, and excitations in that medium cannot carry new information faster than this bound.

What this definition establishes:

- Every medium has a finite causal velocity (fundamental bound).
- Effective excitations in that medium may propagate at lower characteristic speeds.
- Front velocity ≤ fundamental causal velocity at all times.

What this definition does **not** establish:

- the exact causal velocity of non-relativistic effective media (a derived or measured quantity),
- a derivation of `c` from the PF axioms (it is taken as the vacuum constant),
- whether discrete or analogue substrates have different causal velocity structures (open),
- whether the PF minimum substrate modifies the causal velocity at sub-Planck scales (open).

---

## Falsification

The causal-velocity concept fails if:

1. **Controllable FTL signaling is demonstrated** — the fundamental front-velocity constraint is broken.
2. **Local Lorentz-invariance violation is detected** — a preferred-frame effect inconsistent with current experimental bounds.

Note: In general relativity, coordinate speeds can exceed `c` in curved or expanding spacetimes. This does not violate the causal velocity concept. The relevant constraint is local Lorentz invariance — no locally inertial observer measures a controllable superluminal signal.

---

## Open Questions

| Question | Status |
|----------|--------|
| Does the PF minimum substrate (QCA) introduce a lattice-scale correction to `c`? | OPEN |
| Is there a PF derivation of the vacuum `c` value from the axioms? | OPEN |
| Do effective media in the PF have formally defined causal velocities at each scale? | OPEN |
| Can the neural/cognitive threshold analogy be made precise enough to test? | OPEN — PF applied hypothesis |
