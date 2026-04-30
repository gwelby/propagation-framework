# Causal Velocity Definition Final Audit
*Fundamentals - `/mnt/d/Fundamentals/derivations/causal_velocity_definition_final_audit_2026-04-29.md`*
*Target: `/mnt/d/Fundamentals/definitions/causal_velocity.md`*
*Auditor: Codex*
*Date: 2026-04-29*

---

## Verdict

**PASS.**

`definitions/causal_velocity.md` can be marked `CANONICAL v1.0`.

The rewrite closes the prior HOLD findings from `coherence_causal_velocity_audit_2026-04-28.md` by separating:

- fundamental/local causal velocity,
- front velocity,
- signal / information velocity,
- group velocity,
- phase velocity,
- effective propagation speed.

This is the key correction. The previous draft treated material speeds in glass, water, copper, neural axons, and sound as if they were all "causal velocities". The canonical rewrite now treats those as effective speeds of excitations while preserving the local front-velocity / no-FTL constraint.

---

## Finding Closure Table

| Prior finding | Status | Audit result |
|---------------|--------|--------------|
| V-01: core definition survives | **CLOSED / KEPT** | The seed definition survives in tightened form: causal velocity is the upper bound on controllable causal influence in a specified medium or theory. |
| V-02: "most important single number" rhetoric | **CLOSED** | The rhetoric is removed from the definition and appears only as a negated overclaim. |
| V-03: energy-scale claim unjustified | **CLOSED** | The file now says causal velocity constrains wavelength/frequency/dispersion but does not by itself set energy scale. |
| V-04: "maximum efficiency" undefined | **CLOSED** | Replaced with standard null-cone language for massless excitations. |
| V-05: material-media table conflates speeds | **CLOSED** | The table is now explicitly "Effective Propagation Speeds in Media"; front velocity remains bounded by `c`. |
| V-06: propagation ratio conflict | **CLOSED** | The file separates `n_phase = c / v_phase` from `r_eff = v_signal / c`. |
| V-07: threshold overgeneralization | **CLOSED** | Neural/cognitive threshold language is now labeled PF analogy / applied hypothesis, not canonical causal-velocity definition. |
| V-08: falsification condition imprecise | **CLOSED** | Falsification now targets controllable FTL signaling or local Lorentz-invariance violation, with a GR coordinate-speed caveat. |

---

## Acceptance Criteria

### 1. No material-media causal-speed conflation

**PASS.**

Glass, water, copper, axons, and sound are no longer assigned new fundamental causal velocities. They are presented as effective propagation speeds for specific excitations.

### 2. Front, signal, group, and phase velocities are separated

**PASS.**

The final patch split signal / information velocity from group velocity. This matters because group velocity can be anomalous and should not be treated as identical to controllable information speed.

### 3. No unsupported energy-scale claim

**PASS.**

The file now states that causal velocity enters wavelength/frequency/dispersion relations but does not set energy scale without other parameters such as `h`, mass, and couplings.

### 4. Relativity boundary is safe

**PASS.**

The definition uses local Lorentz-invariant `c`, null cones for massless excitations, and a GR caveat that coordinate speeds are not local causal violations.

### 5. Applied PF analogies are labeled

**PASS.**

Neural criticality and cognitive-bandwidth claims are explicitly not canonical causal-velocity results.

---

## Remaining Constraints

This PASS does **not** upgrade any downstream claim by itself.

The following remain open:

- derivation of the numerical vacuum `c` from PF axioms,
- formal causal-velocity treatment for a discrete/QCA minimum substrate,
- tested mapping from neural/cognitive thresholds to any causal-velocity analogue,
- cleanup of downstream framework prose flagged in `semantic_consistency_scan_2026-04-28.md`.

---

## Downstream Rule

Any future use of "causal velocity" must state whether it means:

- fundamental/local causal velocity,
- front velocity,
- signal / information velocity,
- group velocity,
- phase velocity,
- effective propagation speed.

If a claim cannot identify the layer, it should not be upgraded.

---

## Final Status

`definitions/causal_velocity.md`: **CANONICAL v1.0**.
