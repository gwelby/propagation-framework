# Koide Phase: Tolerance and Proxy-Potential Audit

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Run the bounded next pass Claude asked for:

1. quantify how much coefficient drift around the Chebyshev cubic locus is needed before a scalar
   cubic selector can place a minimum near the empirical charged-lepton phase,
2. audit the historical proxy potential

   `V_proxy(delta) = f(delta)^6 * sum_k 1 / g_k(delta)^2`

   against the repo's old "9 minima" expectation.

**Companion files**:
- [koide_phase_minimal_cubic_selector_spec_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_minimal_cubic_selector_spec_2026-04-20.md)
- [koide_phase_character_normal_form_audit_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_character_normal_form_audit_2026-04-20.md)
- [koide_phase_harmonic_suppression_audit.md](/mnt/d/Fundamentals/derivations/koide_phase_harmonic_suppression_audit.md)
- [koide_phase_tolerance_scan.py](/mnt/d/Fundamentals/sandbox/koide_phase_tolerance_scan.py)

---

## 1. Short answer

The tolerance pass does **not** rescue the current selector story.

It sharpens two separations:

1. the exact Chebyshev cubic lane is a **harmonic-purity** result, not a `delta = 2/9` selector,
2. the historical proxy potential does **not** place its minima near the empirical Koide phase.

More concretely:

- the exact Chebyshev point `(b,c,d) = (3,12,8)` puts its minima at

  `delta = pi/9, pi/3, 5pi/9 (mod 2pi/3)`,

  not near the empirical

  `delta_emp = 0.222229631490`,

- making `delta_emp` a minimum inside the scalar cubic family requires a substantial deformation of
  the coefficient direction, including a **sign flip** of the linear term,
- the historical proxy potential

  `f(delta)^6 * sum_k 1 / g_k(delta)^2`

  has **6 minima** on `[0, 2pi)`, not 9, and the closest one sits

  `0.039575 rad`

  away from `delta_emp`, which is about `153` times the current `m_tau`-induced phase uncertainty.

So the honest state after this pass is:

> the cubic Chebyshev locus does not by itself select the empirical Koide phase, and the old
> historical proxy potential is not the selector either.

---

## 2. Setup

The reduced scalar from the earlier audits is

`f(delta) = -1/2 + cos(3 delta)/sqrt(2)`.

The exact harmonic-purity note proved that the unique cubic family whose reduction is pure
`cos(9 delta)` is

`V_(b,c,d)(delta) = b f + c f^2 + d f^3`

with coefficient direction

`(b,c,d) propto (3,12,8)`.

The empirical phase anchor remains

`delta_emp = 0.222229631490`,

with

`|delta_emp - 2/9| = 7.409267777786e-06`.

For this phase,

`f_emp = f(delta_emp) = 0.055696492022`.

---

## 3. Exact condition for hitting the empirical phase

For an interior stationary point of the cubic family, one must have

`V'(delta) = f'(delta) * (b + 2 c f + 3 d f^2) = 0`.

Away from the trivial `sin(3 delta) = 0` points, the condition at `delta_emp` is therefore

`b + 2 f_emp c + 3 f_emp^2 d = 0`.

This is a codimension-1 plane in coefficient space.

Numerically, at the Chebyshev point `(3,12,8)`:

- plane residual = `4.411166189889`
- Euclidean distance to the target-critical plane = `4.383863020284`
- relative distance in normalized coefficient space = `0.297596013091`

The nearest point on that plane is

`(-1.35672885, 11.51469097, 7.95945498)`,

or, after normalizing by `d`,

`(-0.170455, 1.446668, 1)`.

### Consequence

To even make `delta_emp` an interior critical point, the cubic family must move a long way from the
Chebyshev direction and flip the sign of the linear term.

That is already a strong warning that the harmonic-purity locus and the empirical phase-selector
lane are not the same thing.

---

## 4. What the exact Chebyshev cubic actually minimizes

At the Chebyshev point `(3,12,8)`, the stationary points in the reduced fundamental domain are

`0, pi/9, 2pi/9, pi/3, 4pi/9, 5pi/9, 2pi/3`

numerically

`0, 0.349065850399, 0.698131700798, 1.047197551197, 1.396263401595, 1.745329251994, 2.094395102393`.

The minima occur at

`pi/9, pi/3, 5pi/9 (mod 2pi/3)`,

all of them far from `delta_emp = 0.222229631490`.

So the key mismatch is exact and structural:

> the unique scalar cubic that isolates the `9 delta` harmonic does not select the empirical Koide
> phase.

This is not a small numerical miss. It is the wrong selector geometry.

---

## 5. How much drift is needed before a cubic can hit the empirical phase

Holding `d = 8` fixed and scanning a local rectangle around the Chebyshev point:

- `b in [3-6, 3+6]`
- `c in [12-12, 12+12]`

the best minima near `delta_emp` occur around:

- `(-1.35, 11.45, 8)` giving

  `delta_min = 0.222226652057`

  with error `2.98e-06`,

- `(-1.45, 12.35, 8)` giving

  `delta_min = 0.222233912767`

  with error `4.28e-06`,

- `(-1.30, 11.00, 8)` giving

  `delta_min = 0.222222624404`

  with error `7.01e-06`.

### What survives this scan

Yes, there are cubic coefficient sets that place a minimum near the empirical phase.

### What does **not** survive

Those coefficient sets are **not** close to the Chebyshev ratio in the physically relevant sense:

- the linear coefficient changes sign,
- the needed direction is roughly the target-critical plane direction above,
- this is not a "small tolerance around `(3,12,8)`" story.

So the tolerance pass answers Claude's question cleanly:

> the empirical phase is not protected by a wide basin around the Chebyshev cubic. Reaching it
> requires moving to a different selector direction.

That is physics-bad for the scalar-Chebyshev rescue idea.

---

## 6. Historical proxy-potential audit

The old issue file carried the historical candidate proxy

`V_proxy(delta) = f(delta)^6 * sum_k 1 / g_k(delta)^2`.

The new bounded scan over `[0, 2pi)` finds:

- number of minima = `6`
- minima at approximately
  - `0.261804623787`
  - `1.832600950582`
  - `2.356194490192`
  - `3.926990816987`
  - `4.450584356598`
  - `6.021380683393`

The closest minimum to the empirical Koide phase is

`0.261804623787`,

with gap

`|delta_min - delta_emp| = 0.039574992297`.

This is:

- `153.39` times the current `m_tau`-propagated phase uncertainty,
- `5341.28` times the tiny empirical gap `|delta_emp - 2/9|`.

The numerical derivative at `delta_emp` is also nonzero:

- `V_proxy'(delta_emp) = -1.661121057177e-03`

So `delta_emp` is not even approximately stationary for this proxy.

### Consequence

The historical sentence

> "the potential has 9 minima"

does not survive audit for this proxy.

The audited statement is:

> this proxy potential has 6 minima and misses the empirical Koide phase badly.

---

## 7. Honest board-level conclusion

This pass closes two soft lanes:

### Closed soft lane A

"Maybe the exact Chebyshev cubic already gives the empirical selector up to a tolerant coefficient
region."

No. The Chebyshev cubic is a harmonic-purity object. Its minima are not near `delta_emp`, and the
coefficient directions that do hit `delta_emp` are materially different.

### Closed soft lane B

"Maybe the old `f^6 sum 1/g_k^2` proxy already has the advertised 9-minimum structure near
`delta = 2/9`."

No. The proxy has 6 minima, and the nearest one is far from the empirical anchor.

---

## 8. Strongest honest verdict

The tolerance pass is an honest negative for the current scalar-selector rescue attempts.

The repo can now say, more sharply than before:

> PF derives the Koide amplitude geometry and the allowed `cos(3 n delta)` harmonic class.
> The exact scalar Chebyshev cubic isolates the `9 delta` harmonic but does not select the
> empirical charged-lepton phase. The historical proxy potential `f^6 sum 1/g_k^2` also fails to
> select the empirical phase and in fact has 6 minima on `[0, 2pi)`, not 9. Therefore no audited
> scalar selector currently closes `delta ~= 2/9`.

That is the right place to stop.
