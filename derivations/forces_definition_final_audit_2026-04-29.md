# Forces Definition Final Audit
*Fundamentals - `/mnt/d/Fundamentals/derivations/forces_definition_final_audit_2026-04-29.md`*
*Target: `/mnt/d/Fundamentals/definitions/forces.md`*
*Auditor: Codex*
*Date: 2026-04-29*

---

## Verdict

**PASS.**

`definitions/forces.md` is now safe for canonical status.

The canonical definition is standard-first and bounded:

> A force is an interaction that changes a mode's momentum, trajectory, phase, internal quantum numbers, or field configuration.

The file no longer treats "all forces are Medium gradients" as a completed theorem. It states that gravity is encoded by spacetime geometry, gauge forces are encoded by gauge fields, and the PF interpretation of these structures as Medium properties remains a research program unless a force-specific derivation is supplied.

---

## Corrections Applied During Final Audit

Six precision leaks were fixed before PASS:

| ID | Issue | Correction |
|----|-------|------------|
| R-01 | Geodesic equation used proper time for both massive and massless particles. | Replaced with affine parameter `λ`; proper time applies only to timelike geodesics. |
| R-02 | Optical metric was written as a scalar refractive index for all static/stationary cases. | Restricted scalar `n_opt` to static isotropic cases; stationary frame-dragging cases require Randers/Finsler optical geometry. |
| R-03 | Massive-particle Jacobi/Maupertuis formula was too broad. | Marked as Newtonian-limit schematic; canonical massive-particle statement is timelike geodesic of `g_{μν}`. |
| R-04 | PF gravity language said modes minimize proper time. | Replaced with timelike modes extremize proper time; null modes follow affine null geodesics. |
| R-05 | Causal-velocity relationship implied force mediators simply "travel" at `≤ c`. | Rewritten: controllable field changes respect causal velocity; virtual exchange is not a signal. |
| R-06 | Unification section still sounded like all four mappings were established Medium facts. | Rewritten as PF research hypothesis with incomplete exact correspondences. |

---

## Answers to Pre-Dispatch Questions

### Q1 - Is gravity-as-refraction correctly restricted?

**Yes.**

The file restricts the established Fermat/optical-geometry statement to null geodesics in static/stationary domains, with the scalar refractive-index form limited to static isotropic cases. It explicitly separates massive timelike geodesics from optical Fermat paths and marks the massive-particle extension as requiring a separate Jacobi/Maupertuis-type construction.

This closes F-02 and protects F-03.

### Q2 - Is the weak force correctly described?

**Yes.**

The file now starts from the Standard Model account: W/Z exchange, V-A structure, CKM mixing, Higgs mechanism for W/Z masses, and beta decay as `d -> u + W-` followed by `W- -> e- + anti-nu_e`.

The old Higgs-boundary crossing account is gone. PF "mode conversion" is labeled OPEN and explicitly lacks a derivation of V-A structure, parity violation, CKM structure, or CP violation.

This closes F-06.

### Q3 - Is strong force as "extreme refraction" demoted enough?

**Yes.**

The file presents QCD first: SU(3), running coupling, asymptotic freedom, flux tubes, and confinement. The PF "extreme refraction" language is explicitly labeled as an analogy until a mapping from Wilson loops/running coupling to a refractive-index functional exists.

This closes F-05.

### Q4 - Is causal velocity protected?

**Yes.**

The file states that local Lorentz-invariant `c` does not vary in GR. Any varying propagation language is coordinate propagation speed / optical metric language only. The relationship table also distinguishes controllable field changes from virtual exchange.

This closes F-03.

---

## Finding Closure

| ID | Prior severity | Prior finding | Final audit result |
|----|----------------|---------------|--------------------|
| F-01 | Critical | Definition treated all forces as Medium gradients. | **CLOSED.** Standard structures come first; PF gradient framing is a research program. |
| F-02 | Critical | Gravity-as-refraction exceeded audited domain. | **CLOSED.** Restricted to null optical geometry; massive paths separated. |
| F-03 | Critical | Causal-velocity language conflicted with canonical `causal_velocity.md`. | **CLOSED.** Local `c` is invariant; coordinate propagation speed/optical metric language only. |
| F-04 | High | EM phase-gradient account was incomplete. | **CLOSED.** Gauge-covariant derivative and Lorentz force are primary; PF interpretation secondary. |
| F-05 | High | Strong as extreme refraction was treated as derivation. | **CLOSED.** Marked analogy/OPEN pending Wilson-loop/running-coupling mapping. |
| F-06 | Critical | Weak as Higgs-boundary conversion was invalid. | **CLOSED.** Replaced with W/Z exchange, V-A, CKM, Higgs mass mechanism; PF mode conversion remains OPEN. |
| F-07 | Medium | Gravity hierarchy explanation was qualitative. | **CLOSED.** Not claimed as resolved in canonical definition. |
| F-08 | Medium | Falsifiers mismatched weak flavor change. | **CLOSED.** Flavor change is now stated as expected SM behavior, not a falsifier. |

---

## Residual Boundaries

The following are not defects, but must remain bounded:

- `forces.md` does not unify the four forces.
- `forces.md` does not provide a quantum gravity theory.
- `forces.md` does not derive QCD confinement from PF axioms.
- `forces.md` does not derive weak V-A structure, CKM mixing, or CP violation from PF axioms.
- `forces.md` does not prove that all gauge fields are Medium gradients.
- The gravity/refraction theorem is canonical only in the restricted optical-geometry domain described in the file.

---

## Final Status

`definitions/forces.md`: **CANONICAL v1.0**.

With this pass, Phase 2 definitions are complete:

- `time.md`
- `mode.md`
- `energy.md`
- `matter.md`
- `forces.md`
