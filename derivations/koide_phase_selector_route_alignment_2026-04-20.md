# Koide Phase Selector Route Alignment

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Separate the live phase-selector lanes from the already-existing amplitude-selector
lanes so future work stops mixing them.

---

## 1. Why this note exists

The repo now contains multiple mathematically real "selector" discussions:

- entropy selectors for `Q = 2/3`
- projective coordinates for `delta`
- nonlinear harmonic selectors for `delta`

Those are not the same problem.

This note records the current clean separation.

---

## 2. What is already closed enough to keep

### A. Koide amplitude selector

The `u(1) / su(3)` split and the binary entropy route act on the amplitude geometry and target

`Q = 2/3`.

That lane is about:

- equal scalar / traceless norm
- equipartition or entropy in the amplitude space
- why the charged-lepton triple sits on the Koide cone

It does **not** select the orientation `delta`.

Relevant file:

- [koide_u3_entropy_selector_audit_2026-04-15.md](/mnt/d/Fundamentals/derivations/koide_u3_entropy_selector_audit_2026-04-15.md)

### B. Projective phase coordinates

The projective pass acts on the one-dimensional Koide line and shows that all natural affine /
projective coordinates are Möbius transforms of

`tan(delta)`.

That lane clarifies the geometry of the phase variable.

It does **not** supply a selector.

Relevant files:

- [koide_projective_mobius_lemma_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_projective_mobius_lemma_2026-04-20.md)
- [koide_phase_edge_ratio_audit_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_edge_ratio_audit_2026-04-20.md)

---

## 3. What remains genuinely open

### Koide phase selector

The open problem is:

> why does the charged-lepton Koide triple sit at the empirical orientation
>
> `delta mod (2*pi/3) ~= 2/9`
>
> rather than at some other allowed orientation?

The scalar reduction already shows:

`f(delta) = -1/2 + cos(3 delta)/sqrt(2)`.

The new cubic pass sharpened that further:

- degree `< 3` cannot isolate `cos(9 delta)`
- the first exact scalar `cos(9 delta)` selector is the unique Chebyshev-tuned cubic

  `Q_*(f) = c + sqrt(2) k (8 f^3 + 12 f^2 + 3 f - 1/2)`

So the phase problem is now:

> derive why PF would choose that tuned cubic, or prove that the true selector is a non-scalar
> object whose reduction lands on the same cancellation pattern.

Relevant files:

- [koide_phase_harmonic_suppression_audit.md](/mnt/d/Fundamentals/derivations/koide_phase_harmonic_suppression_audit.md)
- [koide_phase_minimal_cubic_selector_spec_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_minimal_cubic_selector_spec_2026-04-20.md)

---

## 4. Clean separation table

| Lane | Variable | Targets | Status | Does it close `delta`? |
|------|----------|---------|--------|------------------------|
| `u(1)/su(3)` entropy | amplitude split | `Q = 2/3` | mathematically exact inside chosen split; physical selector open | No |
| projective / edge ratios | phase coordinate | `tan(delta)` and equivalents | geometrically fenced | No |
| symmetric scalar `Q(f)` | reduced phase scalar | `cos(3n delta)` tower | bounded; exact cubic target written | Not yet |
| external representation labels | `h`, rotation number, level data | rational label upstream of angle | analogy / candidate class only | Not yet |

---

## 5. Operational consequence

Future phase-selector notes should be rejected if they do one of the following:

1. prove something about `Q = 2/3` and then speak as if `delta` moved with it,
2. find a new rational approximant to a phase coordinate and call that a selector,
3. introduce a nonlinear phase observable without checking whether it reaches the tuned cubic
   cancellation locus.

That category blur is now avoidable.

---

## 6. Final verdict

The repo is no longer blocked by not knowing what the selector problem is.

It is blocked by one specific missing object:

> a physical principle that selects the tuned cubic cancellation pattern in the reduced Koide phase
> sector, or a non-scalar observable that reduces to the same pattern.

That is the load-bearing open problem.
