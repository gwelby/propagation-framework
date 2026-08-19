# PRED-003 Route B — Koide ansatz → neutrino mass-squared ratio probe

**Status:** CONDITIONAL (currently a fit / no-go as a PF-native derivation)  
**Date:** 2026-08-18  
**Agent:** Devin ∇λΣ∞  
**Authority tier:** advisory — angle-specific probe, does not upgrade `PRED-003-neutrino-mass-squared-ratio.md`  
**Public hold:** yes — Fundamentals PUBLIC HOLD remains in effect

---

## Question

Can the Koide ansatz

```
√m_k = √m̄ · (1 + β·cos(δ + 2πk/3)),   k = 0, 1, 2
```

produce the two distinct measured squared-mass splittings

```
Δm²₂₁ = 7.49 × 10⁻⁵ eV²
Δm²₃₁ = 2.534 × 10⁻³ eV²
```

and therefore their ratio

```
r_ν = Δm²₂₁ / Δm²₃₁ = 0.02951 ± 0.00098    (NuFIT 6.0, normal ordering)
```

without importing new, unjustified structure?  Specifically, does any
**known PF principle** — the charged-lepton `Q = 2/3` condition (`β = √2`) or
the Koide phase `δ = 2/9` — select a point in `(β, δ, m̄)`-space that gives the
measured ratio?

---

## What PF has

### 1. The Koide `Q = 2/3` identity

`KoideGeometry.lean` defines the reciprocal Koide ratio

```
Q = (a² + b² + c²) / (a + b + c)²
```

and proves `Q = 2/3 ↔ a² + b² + c² = 4(ab + bc + ca)` when `a, b, c > 0`
<ref_snippet file="/mnt/d/Fundamentals/lean/PfLean/KoideGeometry.lean" lines="71-92,104-125"/>.
This is the exact charged-lepton identity, but it is a **constraint on three
numbers**, not a generator of the two splittings.

### 2. The P₀/Q decomposition

`KoideSelection.lean` proves the Z₃ cosine identity

```
cos(δ) + cos(δ + 2π/3) + cos(δ + 4π/3) = 0
```

and shows that the ansatz splits as

```
(√m_0, √m_1, √m_2) = √m̄·(1,1,1) + √m̄·β·(cos δ, cos(δ+2π/3), cos(δ+4π/3))
                    = P₀ + Q
```

where `P₀` is the uniform mode and `Q` is the residue
<ref_snippet file="/mnt/d/Fundamentals/lean/PfLean/KoideSelection.lean" lines="114-148,184-212"/>.
This is the same P₀/Q structure that appears in the God Equation, but the
mapping to neutrino mass eigenstates is not formalized.

### 3. The generalized `Q(β)` identity

`KoideUnlocked.lean` proves that for the generalized ansatz

```
Q(β) = (1 + β²/2) / 3
```

for all `β, δ` (algebraic) and, with the domain condition
`1 + β·cos(δ + 2πk/3) ≥ 0`, for physical masses
<ref_snippet file="/mnt/d/Fundamentals/lean/PfLean/KoideUnlocked.lean" lines="176-210,233-253"/>.
Setting `β = √2` recovers the charged-lepton value `Q = 2/3`.

### 4. Falsified cross-links

`KoideUnlocked.lean` also records five hypotheses that tried to connect the
amplitude `β` to the God Equation contraction `−1/8` or to the Casimir root; all
were numerically falsified
<ref_snippet file="/mnt/d/Fundamentals/lean/PfLean/KoideUnlocked.lean" lines="295-324"/>.
So `−1/8` does **not** currently select a neutrino `β`.

### 5. The `δ = 2/9` anchor

The Koide phase `δ ≈ 2/9` is PF's strongest empirical anchor for the charged
leptons, but `PREDICTIONS/README.md` records it as a **postdiction** and notes
that every PF-native selector route for `δ` has failed
<ref_snippet file="/mnt/d/Fundamentals/PREDICTIONS/README.md" lines="11-14"/>.

---

## Missing bridge

A PF-native derivation of `r_ν` from the Koide ansatz would need to close all of
the following gaps.

| Missing piece | Why it blocks Route B |
|---|---|
| **Ansatz not derived from Axioms 1–3** | The form `√m_k = √m̄(1 + β·cos(...))` is assumed, not obtained from the propagation axioms. The `P₀/Q` decomposition is proven, but the ansatz itself is a selection. |
| **Free phase `δ`** | The `δ = 2/9` anchor is postdicted; there is no PF theorem that fixes the neutrino phase. The ansatz can reproduce `r_ν` for many different `δ` by tuning `β`. |
| **Free amplitude `β`** | `Q(β) = (1 + β²/2)/3` is algebraic, not predictive. The charged-lepton value `β = √2` gives a ratio far from `r_ν`. A neutrino `β` must be supplied from outside. |
| **No two-splitting generator** | `Q` is a single quality parameter. It does not, by itself, emit two distinct positive numbers `Δm²₂₁` and `Δm²₃₁`. The two splittings require both the pattern (`β, δ`) and an ordering. |
| **No flavor / PMNS bridge** | No theorem identifies the ansatz branches `k = 0, 1, 2` with `m₁, m₂, m₃` or with flavor states `ν_e, ν_μ, ν_τ`. Sorting the branches is an extra assumption. |
| **Mass scale `m̄`** | The ratio `r_ν` is independent of `m̄`, but the two actual `Δm²` values are not. PF has no derivation of the eV-scale `m̄`; it must be fit to one measured splitting. |
| **Normal vs. inverted ordering** | The ansatz gives a set of three positive amplitudes, but does not select normal ordering (NO) or inverted ordering (IO). That choice is an extra premise. |

`PRED-003-neutrino-mass-squared-ratio.md` already identifies these as the
Route-B blockers <ref_snippet file="/mnt/d/Fundamentals/PREDICTIONS/PRED-003-neutrino-mass-squared-ratio.md" lines="92-98"/>.

---

## Toy probe

### Setup

Python file: `sandbox/pred003_route_B_toy.py`.

The toy uses the standard Koide ansatz exactly as written in
`KoideSelection.lean`:

```
√m_k = √m̄ · (1 + β·cos(δ + 2πk/3)),   k = 0, 1, 2
```

with the physical-mass requirement
`1 + β·cos(δ + 2πk/3) ≥ 0` (the `DomainOk` condition of `KoideUnlocked.lean`).
The physical masses are `m_k = m̄·(1 + β·cos(...))²`.  The script sorts the three
masses into ascending order (`m₁ < m₂ < m₃`, normal ordering), computes

```
Δm²₂₁ = m₂² − m₁²
Δm²₃₁ = m₃² − m₁²
r = Δm²₂₁ / Δm²₃₁
```

and compares with NuFIT 6.0.

The absolute scale `m̄` is fixed by requiring the solar splitting to match
`7.49 × 10⁻⁵ eV²`, which also lets the script report the implied `Σmν`.

The script tests three kinds of "selected" points:

1. **PF/empirical anchors** at `δ = 2/9` with `β = √2` (charged-lepton `Q=2/3`),
   `β` from measured `Q_NO = 0.55`, and `β` from measured `Q_IO = 0.48`.
2. **Best fit on a line of constant `β`**: vary `δ` at `β = √2`, `Q_NO`, and
   `Q_IO` to see whether any phase reproduces `r_ν`.
3. **Best fit on a line of constant `δ`**: vary `β` at `δ = 2/9` to see
   whether the PF phase alone can hit `r_ν`.
4. **Full `(β, δ)` grid scan** to find the best unprincipled fit and the size
   of the `r ≈ r_ν` region.

### Results

Run output (`python3 sandbox/pred003_route_B_toy.py`):

```text
==============================================================================
PRED-003 Route B toy probe — Koide ansatz → neutrino mass-squared ratio
Target r_ν = 0.02951 ± 0.00098
==============================================================================

--- 1. Specific PF / empirical anchors -------------------------------
  charged-lepton anchor: β=√2, δ=2/9                 β=1.41421  δ=0.222222  Q=0.66667  r=0.003535  |r−r_ν|=0.02597 (26.5σ)
  measured Q_NO=0.55 with δ=2/9                      β=1.14018  δ=0.222222  Q=0.55000  r=0.009494  |r−r_ν|=0.02002 (20.4σ)
  measured Q_IO=0.479 with δ=2/9                     β=0.93488  δ=0.222222  Q=0.47900  r=0.019081  |r−r_ν|=0.01043 (10.6σ)

--- 2. Best fit on the charged-lepton Q=2/3 line (β=√2) --------------
  Best δ for r_ν at β=√2: δ = 1.832596 rad (5.2500·(π/9))
  r = 0.005155, distance = 0.02436 (24.9σ)
  Compare with PF phase anchor δ = 2/9 = 0.222222 rad.

--- 2a. Best-fit phase for the measured neutrino Q values ------------
  Measured Q_NO=0.55 (β=1.14018):
    Best δ for r_ν: δ = 0.392699 rad (1.1250·(π/9))   (= π/8)
    r = 0.029521, distance = 0.00001 (0.0σ)
    Distance from PF phase anchor δ=2/9: 0.170477 rad (76.7%)
  Measured Q_IO=0.479 (β=0.93488):
    Best δ for r_ν: δ = 0.296985 rad (0.8508·(π/9))
    r = 0.029511, distance = 0.00000 (0.0σ)
    Distance from PF phase anchor δ=2/9: 0.074763 rad (33.6%)

--- 3. Best fit on the PF phase line (δ = 2/9) -----------------------
  Best β for r_ν at δ=2/9: β = 0.799280
  Q(β) = 0.43981
  r = 0.029501, distance = 0.00001 (0.0σ)
  Compare with charged-lepton Q=2/3 anchor β=√2=1.414214.

--- 4. Full (β,δ) grid scan ------------------------------------------
  Best-fit grid point: β=1.15388, δ=0.397935 rad, r=0.029512
  Distance from target: 0.00000 (0.00σ)
  Q at this point: 0.55524
  Scale m̄ = 0.011829 eV (chosen to match Δm²₂₁)
  Implied masses (eV): m1=0.000077, m2=0.008655, m3=0.050378
  Implied Δm²₂₁ = 7.490000e-05 eV², Δm²₃₁ = 2.537950e-03 eV²
  Implied Σmν = 0.059110 eV
  Points within 3σ of target: 2146

--- 5. Inverted ordering (IO) sanity check ---------------------------
  Best IO point: β=1.15388, δ=0.397935 rad, r_IO=0.029512, distance=0.00000 (0.0σ)

==============================================================================
Interpretation:
- The ratio r_ν is a continuous function of (β,δ). A match can always be
  obtained by fitting one of these two free parameters once the other is fixed.
- The PF-known fixed points (δ=2/9, β=√2) do not reproduce r_ν.
- Therefore the Koide ansatz, as PF currently has it, does not DERIVE the
  neutrino mass-squared ratio; it can only FIT it with an additional selector
  for β or δ that PF does not possess.
==============================================================================
```

### Summary table

| Test point | β | δ (rad) | Q | `r_PF` | `|r_PF − r_ν|` |
|---|---:|---:|---:|---:|---:|
| Charged-lepton anchor (`β=√2`, `δ=2/9`) | 1.41421 | 0.222222 | 0.66667 | 0.003535 | 26.5σ |
| Measured `Q_NO=0.55`, `δ=2/9` | 1.14018 | 0.222222 | 0.55000 | 0.009494 | 20.4σ |
| Measured `Q_IO=0.479`, `δ=2/9` | 0.93488 | 0.222222 | 0.47900 | 0.019081 | 10.6σ |
| Best `δ` at `β=√2` | 1.41421 | 1.832596 | 0.66667 | 0.005155 | 24.9σ |
| Best `δ` at measured `Q_NO=0.55` | 1.14018 | 0.392699 (π/8) | 0.55000 | 0.029521 | 0.0σ |
| Best `δ` at measured `Q_IO=0.479` | 0.93488 | 0.296985 | 0.47900 | 0.029511 | 0.0σ |
| Best `β` at `δ=2/9` | 0.79928 | 0.222222 | 0.43981 | 0.029501 | 0.0σ |
| Full-grid best fit | 1.15388 | 0.397935 | 0.55524 | 0.029512 | 0.0σ |

### Interpretation of the toy

- **The Koide ansatz can fit `r_ν`, but cannot derive it.**  The full
  `(β, δ)` grid contains thousands of points within 3σ of the target; `r_ν` is
  a one-parameter family of fits, not a unique output.

- **The charged-lepton anchor fails.**  `β = √2` (the `Q = 2/3` condition) with
  any physical `δ` cannot get closer than ~25σ to the measured ratio.  Even the
  best `δ` on the `β = √2` line is at `δ ≈ 1.83` rad, nowhere near the PF phase
  `δ = 2/9`.

- **The PF phase `δ = 2/9` fails unless `β` is fitted.**  At `δ = 2/9` the
  target is hit only by setting `β ≈ 0.799` (`Q ≈ 0.44`).  No PF theorem or
  measurement predicts this `β`.

- **The measured neutrino `Q` values also fail with `δ = 2/9`.**  If `Q_NO =
  0.55` is taken as input, the ansatz needs `δ ≈ π/8` (0.393 rad), not `2/9`,
  to reproduce `r_ν`.  If `Q_IO = 0.479` is taken, the required `δ` is
  `0.297` rad.  In both cases the phase must be adjusted by hand.

- **The full best fit is unprincipled.**  The grid best point
  `(β ≈ 1.154, δ ≈ 0.398 rad, Q ≈ 0.555, m̄ ≈ 0.0118 eV)` gives a sensible
  neutrino spectrum, but it is selected by neither the charged-lepton `Q = 2/3`
  condition nor the Koide `δ = 2/9` anchor.  It is a fit to the data, not a
  derivation from PF premises.

- **The absolute scale `m̄` is an extra fit.**  Once `β` and `δ` are chosen to
  match the ratio, `m̄` is simply adjusted to match `Δm²₂₁`.  This is the same
  circularity that blocks any PF-native scale bridge.

---

## Honest conclusion

**CONDITIONAL** — the Koide ansatz can reproduce the measured
`r_ν = 0.02951`, but only under the premise stated below.  With the PF premises
that currently exist, the route is a **fit, not a derivation**, and is therefore
**blocked as a PF-native prediction**.

The key result is not that the Koide ansatz is mathematically incompatible with
the neutrino data; the opposite is true — it is *too* compatible, because it has
enough free parameters to hit the target in many places.  What is missing is a
PF-native selector that picks the neutrino point.

### Exact premise that would need to be added

For Route B to become a PF-native derivation of `r_ν`, the following premise
(or an equivalent one with the same content) would have to be introduced and
independently justified:

> **Postulate K (neutrino Koide bridge).**  The three neutrino masses are given
> by the Koide ansatz `√m_k = √m̄(1 + β·cos(δ + 2πk/3))`, and **all** of the
> following are supplied by PF:
>
> 1. a derivation of the ansatz form, or at least of the equal `2π/3` phase
>    spacing and the cosine modulation, from Axioms 1–3 or an explicit named
>    premise;
> 2. a PF-derived rule that fixes the neutrino amplitude `β_ν` (or equivalently
>    `Q_ν`) and the neutrino phase `δ_ν` independently of the charged-lepton
>    values `β = √2`, `δ = 2/9`;
> 3. a PF-derived rule that maps the three ansatz branches to the ordered
>    neutrino mass eigenstates `m₁, m₂, m₃`, including the normal/inverted
>    ordering choice;
> 4. a PF-derived absolute scale `m̄` (or a proof that the scale is fixed by the
>    propagation medium), or else an explicit admission that the absolute scale
>    is taken from one measured splitting.

Until Postulate K (or a premise of equivalent content) is independently
derived or audited, Route B remains a **fit**, not a **PF-native derivation** of
the neutrino mass-squared ratio.

---

## References

| File | Role |
|---|---|
| `lean/PfLean/KoideGeometry.lean` lines 71–92, 104–125 | `Q = 2/3` identity and `Q ↔ R` bridge |
| `lean/PfLean/KoideSelection.lean` lines 114–148, 184–212 | Z₃ cosine identity, `P₀/Q` decomposition, ansatz mass vector |
| `lean/PfLean/KoideUnlocked.lean` lines 176–210, 233–253 | Generalized `Q(β) = (1+β²/2)/3` and domain restriction |
| `lean/PfLean/KoideUnlocked.lean` lines 295–324 | Falsified `β ↔ −1/8` / Casimir cross-link hypotheses |
| `PREDICTIONS/README.md` lines 11–14 | `δ = 2/9` is a postdiction, PF phase selector routes failed |
| `PRED-003-neutrino-mass-squared-ratio.md` lines 92–98 | Route B blocker statement |
| `sandbox/pred003_route_B_toy.py` | Toy numerical probe (this route) |

---

## Sign-off

- This is a **toy probe**, not a formal no-go theorem.
- No prediction is locked; no pre-registration hash has been computed.
- `PRED-003-neutrino-mass-squared-ratio.md` and the workspace state files
  (`RESUME.md`, `STATE.md`, `CHANGELOG.md`, `REMEMBER.md`) were **not edited**.
