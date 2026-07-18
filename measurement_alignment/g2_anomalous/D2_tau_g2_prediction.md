# D2: Tau Anomalous Magnetic Moment Prediction
*Devin · 2026-07-10 · PF coherence-ceiling framework · PDG 2024*

## Formula & Conventions

The task specifies the PF prediction:

```
δa_τ = w_max / (m_τ / λ_c · (ħc)⁻¹)
```

This evaluates to:

```
δa_τ = w_max · λ_c · ħc / m_τ
```

In **natural units** (ħc = 1, length measured in MeV⁻¹):

```
λ_c^natural = λ_c^SI / (ħc) = 1.157×10⁻¹⁸ m / 1.97327×10⁻¹³ MeV·m
δa_τ = w_max · λ_c^natural / m_τ
```


## Input Parameters

| Parameter | Value | Uncertainty | Source |
|---|---|---|---|
| m_τ | 1776.86 MeV | ±0.12 MeV | PDG 2024 |
| λ_c | 1.157×10⁻¹⁸ m | ±1.700e-20 m | CLAIMS.md, ARGUED 0.60 |
| ħc | 1.97327×10⁻¹³ MeV·m | — | defined |
| w_max | 2.0 | ±1.0 | PF manuscript: Z₂ spin structure winding |
| a_τ^SM | 1177.21×10⁻⁶ | ±0.05×10⁻⁶ | Standard Model QED |

Natural-unit λ_c = 5.863364e-06 MeV⁻¹
Implied ceiling mass m_t = ħc/λ_c = 170550.6 MeV = 170.55 GeV

## 1. What λ_c Is in PF (Targeted Search)

I searched the canonical PF documents for a physical definition of λ_c in MeV:

- `/mnt/d/Fundamentals/derivations/lambda_c_from_axioms.md` (the God Equation derivation)
- `/mnt/d/Fundamentals/definitions/coherence.md` (canonical coherence definition)
- `/mnt/d/Fundamentals/PROPAGATION_MANUSCRIPT.md` (MAX-1 and surrounding context)

### Finding

**λ_c is identified with the top quark Compton wavelength:** λ_c = ħc/m_t ≈ 1.14 × 10⁻¹⁸ m, corresponding to m_t ≈ 173 GeV.
Using the CLAIMS.md value λ_c = 1.157 × 10⁻¹⁸ m gives m_t = ħc/λ_c ≈ 170.55 GeV.

This identification is **calibrated / empirical**, not derived from PF axioms. The `lambda_c_from_axioms.md` document explicitly states:

> λ_c ≈ 1.14 × 10⁻¹⁸ m (matter coherence scale) is currently calibrated to the top quark mass, not derived from axioms.

The `definitions/coherence.md` file lists the open question:

> Can 'coherence ceiling' be defined as a precise functional rather than a phrase? | OPEN

### Consequence for D2

- λ_c is pinned as the top Compton wavelength, but **the formula that uses it is not dimensionally closed**. See Section 5.
- The literal-formula numerics are ~6.6 × 10⁻⁹; the ceiling-mass numerics are ~1.17 × 10⁻⁵. These differ by a factor of m_τ and **both are unit-stripped outputs, not dimensionally valid predictions of a dimensionless anomalous magnetic moment.

## 2. PF Prediction (Formula As Written)

**δa_τ = 6.600 × 10^-9**

Monte Carlo uncertainty (m_τ, λ_c, w_max): **3.11 × 10^-9** (68% interval)
68% interval: [3.57 × 10^-9, 9.92 × 10^-9]

Relative to SM: δa_τ / a_τ^SM = 5.61e-06
Relative to SM uncertainty: δa_τ / σ_SM = 0.13σ

## 3. Alternative Interpretation (Coherence Ceiling Mass)

The PF manuscript prose says the correction is 'proportional to the topological winding number divided by the coherence ceiling mass.' If the coherence ceiling mass is m_t = ħc/λ_c, the formula would be:

```
δa_τ = w_max / m_t
```

**δa_τ^alt = 1.173 × 10^-5**

This is 9.96e-03 of the SM value and 234.5σ of the SM uncertainty.

## 4. Comparison with Belle II Sensitivity

Belle II feasibility target (PF manuscript): **σ(a_τ) ≈ 1e-05**

### Formula-as-written prediction
- PF δa_τ = 6.600 × 10^-9
- Belle II σ = 1e-05
- PF signal / Belle II precision = 6.60e-04
- **Conclusion:** Belle II at 10⁻⁵ would measure a_τ consistent with pure QED; the PF correction is ~1515× below the projected precision.
- Sensitivity needed for 2σ detection: **σ(a_τ) < 3.30 × 10^-9**

### Alternative ceiling-mass interpretation
- PF δa_τ^alt = 1.173 × 10^-5
- PF signal / Belle II precision = 1.17
- **Conclusion:** Belle II at 10⁻⁵ could detect or constrain this correction.

## 5. Dimensional Analysis

An anomalous magnetic moment `a = (g-2)/2` is **dimensionless**. The PF formula must produce a dimensionless number. It does not, under either reading.

In natural units (ħc = 1), λ_c has dimensions of inverse mass. The formula as written is:

```
δa_τ = w_max / (m_τ / λ_c)
```

Since λ_c ~ 1/m_t, this becomes:

```
δa_τ ~ w_max / (m_τ · m_t)
```

If `w_max` is a pure winding number (dimensionless), the right-hand side has dimensions **mass⁻²**, not dimensionless. The reported number 6.6 × 10⁻⁹ is what remains after stripping the units.

The ceiling-mass reading `δa_τ = w_max / m_t` has dimensions **mass⁻¹**, still not dimensionless. The reported number 1.17 × 10⁻⁵ is likewise unit-stripped.

**Conclusion:** PF has not yet dimensionally closed lepton g-2. Neither reading of the stated formula yields a dimensionless prediction. The two numbers are not competing interpretations of a valid formula; they are two different ways of mishandling the same dimensional gap.

## 6. Assessment

**What the calculation shows:**
- Evaluating the given formula literally with w_max = 2 gives a tiny number: **6.60 × 10^-9**.
- Evaluating the ceiling-mass reading gives a larger number: **1.17 × 10^-5**.
- **Neither is a valid prediction of a dimensionless anomalous magnetic moment.** See Section 5.

**What the λ_c search found:**
- λ_c is canonically identified with the top quark Compton wavelength (~1.14 × 10⁻¹⁸ m).
- This identification is **calibrated/empirical**, not derived from PF axioms (`lambda_c_from_axioms.md` is explicit about this).
- The 'coherence ceiling' is not yet a precise functional in `definitions/coherence.md`; it is listed as OPEN.

**Honest ambiguity:**
- The formula as written is dimensionally inconsistent. A dimensionless `a_τ` cannot equal `w_max / (mass²)` or `w_max / mass` unless `w_max` carries compensating units that the PF manuscript does not specify.
- The ceiling-mass reading gives ~1.2 × 10⁻⁵, which sits near Belle II's projected 10⁻⁵ reach. This coincidence is not a successful prediction; it is the signature of a free factor-of-m_τ ambiguity landing near an experimental threshold.
- The '234σ of SM theory uncertainty' framing is misleading: it is 234 × the tiny SM theory uncertainty (~5×10⁻⁸), not 234σ of detectability. At Belle II's actual precision (~10⁻⁵), a 1.17 × 10⁻⁵ effect is a ~1σ hint, not a slam dunk.

**What this does not prove:**
- It does not prove or disprove the PF coherence-ceiling mechanism. It shows that the current formula for lepton g-2 is not dimensionally closed and therefore not yet a prediction.
- It does not resolve the gap; that requires a field-theoretic derivation of how the coherence ceiling contributes to the lepton magnetic moment.

**Next step for PF:**
- Derive a dimensionally closed formula for lepton g-2 from the PF Lagrangian or coherence functional, or admit the gap openly in the PREMISE_LEDGER.
- Do not present the 6.6 × 10⁻⁹ or 1.17 × 10⁻⁵ numbers as predictions until the dimensional scaffolding is fixed.
- TASK-051/052 (muon/electron g-2) will hit the same undefined formula and should not be started.

## 7. Method Notes

- Natural-unit conversion: λ_c(MeV⁻¹) = λ_c(m) / (ħc in MeV·m).
- Uncertainty propagation: 50,000 Monte Carlo samples perturbing m_τ, λ_c, and w_max within their stated uncertainties.
- Source script: `d2_tau_g2.py` in this directory.
