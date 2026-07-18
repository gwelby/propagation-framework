# D1 v4: Quark Koide Formula — Source-Correct Square-Root Fit
*Devin · 2026-07-11 · Zenczykowski 2013 (PRD 87, 077302) · PDG 2024 masses*

## Codex Status - 2026-07-12

**SUPERSEDED / DO NOT CITE AS CURRENT D1 TRUTH.** A newer D1 v4 source and
result pair exists under `d1_fit_v4.py`, `D1_fit_v4_results.md`, and
`d1_v4_results.json`; the two v4 result pairs use different inputs and report
different numbers. The newer pair is itself **HOLD** for PDG confidence-
convention, optimizer, scale, and physical-interpretation repairs. Governing
report: `/mnt/d/Codex/REPORTS/CODEX_20260712_D1_QUARK_KOIDE_V4_REAUDIT.md`.

## Summary

This report corrects the D1 v3 error identified by Codex (2026-07-10): Zenczykowski's Eq. (4) parametrizes **square roots** of quark masses, not masses linearly. All fits below use the source-correct formula.

**Key result:** With the correct formula and the mixed-scale PDG 2024 central values:
- The up-type fixed phase `δ_U = 2/27` is **compatible** with the data (χ² = 0.242, p = 0.623).
- The down-type fixed phase `δ_D = 4/27` is **strongly rejected** (χ² = 248.43, p = 5.72e-56).
- The claimed `δ_D = 2·δ_U` hierarchy is **tensioned**: MC δ_D/δ_U = 1.481 ± 0.027 vs. predicted 2.000; pull = -17.27σ.

**Boundary:** These are numeric tests of a published phenomenological formula, not PF first-principles derivations. The inputs are mixed-scale PDG 2024 values, not run to a common scale. No `CLAIMS.md` tier change or public boundary is warranted from this analysis alone.

## Input Manifest

| Quantity | Value |
|---|---|
| PDG edition | 2024 |
| Source | https://pdg.lbl.gov/2024/tables/rpp2024-sum-quarks.pdf |
| Confidence convention | 1-sigma uncertainties as reported by PDG 2024 |
| Correlation assumptions | Uncertainties treated as uncorrelated. This is an approximation; PDG does not publish a full quark-mass covariance matrix. |
| Scale convention | Mixed-scale PDG 2024 central values. The formula is evaluated at the reported scales, not run to a common scale. A fully scale-consistent treatment would require running masses and is beyond the scope of this numeric test. |

### Masses used (MeV)

| Quark | Central | Sigma | Scheme |
|---|---|---|---|
| up | 2.16 | 0.49 | MS-bar at 2 GeV |
| down | 4.67 | 0.48 | MS-bar at 2 GeV |
| charm | 1270.0 | 20.0 | MS-bar at m_c |
| strange | 93.5 | 0.8 | MS-bar at 2 GeV |
| bottom | 4180.0 | 20.0 | MS-bar at m_b |
| top | 172500.0 | 700.0 | Pole mass (PDG average) |

### Ordering convention

```
j=0 -> heaviest (top, bottom)
j=1 -> lightest (up, down)
j=2 -> middle   (charm, strange)
```

## Formula

Zenczykowski 2013 Eq. (4), source-correct:

```
sqrt(m_j) = sqrt(M) * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))
```

Equivalently:

```
m_j = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))**2
```

## Free Fits

### Up-type

| Parameter | Value |
|---|---|
| sqrt(M) [MeV^(1/2)] | 150.813 |
| M [MeV] | 22744.455 |
| k | 1.243677 |
| delta [rad] | 0.074437 |
| delta / (2*pi) | 0.011847 |

| Quantity | Mean | Std |
|---|---|---|
| sqrt(M) | 150.811 | 0.303 |
| k | 1.243720 | 0.001417 |
| delta [rad] | 0.074463 | 0.000742 |

| Quark | Observed [MeV] | Predicted [MeV] | Residual [MeV] |
|---|---|---|---|
| top | 172500.000 | 172500.000 | 0.000 |
| up | 2.160 | 2.160 | 0.000 |
| charm | 1270.000 | 1270.000 | 0.000 |

### Down-type

| Parameter | Value |
|---|---|
| sqrt(M) [MeV^(1/2)] | 25.494 |
| M [MeV] | 649.969 |
| k | 1.092720 |
| delta [rad] | 0.110256 |
| delta / (2*pi) | 0.017548 |

| Quantity | Mean | Std |
|---|---|---|
| sqrt(M) | 25.494 | 0.065 |
| k | 1.092801 | 0.003022 |
| delta [rad] | 0.110303 | 0.001674 |

| Quark | Observed [MeV] | Predicted [MeV] | Residual [MeV] |
|---|---|---|---|
| bottom | 4180.000 | 4180.000 | 0.000 |
| down | 4.670 | 4.670 | 0.000 |
| strange | 93.500 | 93.500 | 0.000 |

## Fixed-Phase Fits

### Regression test: up-type at δ_U = 2/27

This is the test Codex required: under the actual Eq. (4), does the up sector tolerate the claimed `δ_U = 2/27`?

| Quantity | Value |
|---|---|
| Fixed delta | 0.074074 rad (= 2/27) |
| sqrt(M) | 150.815 MeV^(1/2) |
| k | 1.244033 |
| chi2 | 0.2417 |
| dof | 1 |
| p-value | 0.6230 |

| Quark | Observed [MeV] | Predicted [MeV] | Sigma [MeV] | Pull |
|---|---|---|---|---|
| top | 172500.000 | 172573.060 | 700.000 | -0.104 |
| up | 2.160 | 2.270 | 0.490 | -0.225 |
| charm | 1270.000 | 1261.511 | 20.000 | 0.424 |

**Result:** The up sector is compatible with `δ_U = 2/27` (p = 0.623). This directly contradicts the D1 v3 claim that both fixed phases were ruled out.

### Down-type at δ_D = 4/27

| Quantity | Value |
|---|---|
| Fixed delta | 0.148148 rad (= 4/27) |
| sqrt(M) | 24.573 MeV^(1/2) |
| k | 1.136180 |
| chi2 | 248.426 |
| dof | 1 |
| p-value | 5.72e-56 |

| Quark | Observed [MeV] | Predicted [MeV] | Sigma [MeV] | Pull |
|---|---|---|---|---|
| bottom | 4180.000 | 4047.906 | 20.000 | 6.605 |
| down | 4.670 | 0.000 | 0.480 | 9.729 |
| strange | 93.500 | 101.896 | 0.800 | -10.495 |

**Result:** The down sector strongly rejects `δ_D = 4/27` (p = 5.72e-56). The main driver is the bottom-quark prediction being far below the observed value.

## Cross-Sector Hierarchy Test

Zenczykowski's paper claims `δ_D = 2·δ_U`. We test this by using the free-fit `δ_U` to predict `δ_D`, and vice versa.

### Up-type δ predicts down-type masses

| Quantity | Value |
|---|---|
| Predicted delta | 0.148875 rad |
| sqrt(M) | 24.553 MeV^(1/2) |
| k | 1.135143 |
| chi2 | 273.892 |
| p-value | 1.61e-61 |

| Quark | Observed [MeV] | Predicted [MeV] | Sigma [MeV] | Pull |
|---|---|---|---|---|
| bottom | 4180.000 | 4036.452 | 20.000 | 7.177 |
| down | 4.670 | 0.000 | 0.480 | 9.729 |
| strange | 93.500 | 102.541 | 0.800 | -11.301 |

### Down-type δ predicts up-type masses

| Quantity | Value |
|---|---|
| Predicted delta | 0.055128 rad |
| sqrt(M) | 149.543 MeV^(1/2) |
| k | 1.272633 |
| chi2 | 645.094 |
| p-value | 2.61e-142 |

| Quark | Observed [MeV] | Predicted [MeV] | Sigma [MeV] | Pull |
|---|---|---|---|---|
| top | 172500.000 | 174957.463 | 700.000 | -3.511 |
| up | 2.160 | 5.441 | 0.490 | -6.695 |
| charm | 1270.000 | 785.050 | 20.000 | 24.248 |

### Hierarchy summary

| Quantity | Value |
|---|---|
| δ_U [rad] | 0.074437 ± 0.000742 |
| δ_D [rad] | 0.110256 ± 0.001674 |
| δ_D / δ_U (free) | 1.4812 |
| δ_D / δ_U (MC mean) | 1.4813 ± 0.0269 |
| Predicted by 1:2 hierarchy | 2.000 |
| δ_D - 2·δ_U (MC) | -0.038622 ± 0.002237 |
| Pull against 1:2 | -17.27 σ |

**Result:** The `δ_D = 2·δ_U` hierarchy is tensioned at 17.3σ under the mixed-scale PDG uncertainty model. Because the inputs are not run to a common scale and correlations are ignored, this tension should be treated as **conditional**, not a broad physical falsification.

## Claim Separation

### What this analysis tests
- Whether the Zenczykowski 2013 Eq. (4), evaluated with mixed-scale PDG 2024 central values, can reproduce quark masses.
- Whether the specific phase values `δ_U = 2/27` and `δ_D = 4/27` are compatible with those masses.
- Whether the claimed `δ_D = 2·δ_U` hierarchy holds.

### What this analysis does NOT test
- Any PF first-principles derivation of quark masses.
- The validity of Zenczykowski's weak-basis or pseudo-mass constructions.
- A scale-consistent running-mass treatment; the inputs are at different renormalization scales.
- Any claim about CKM mixing angles or CP violation.

### What would strengthen or weaken the result
- **Strengthen:** Run all six quark masses to a common scale with a trusted QCD running prescription and repeat.
- **Strengthen:** Include PDG-published correlations or a full covariance matrix.
- **Weaken:** Show that the mixed-scale treatment is the sole source of the down-sector tension.

## Comparison with D1 v3

| Issue | D1 v3 | D1 v4 (this report) |
|---|---|---|
| Formula used | `m_j = M * (...)` linear | `sqrt(m_j) = sqrt(M) * (...)` source-correct |
| Up fixed phase `δ_U = 2/27` | claimed ruled out | compatible (p = 0.623) |
| Down fixed phase `δ_D = 4/27` | claimed ruled out | strongly rejected (p ≈ 6e-56) |
| 1:2 hierarchy | claimed 19.4σ falsification | tensioned at ~17σ, but conditional on mixed-scale inputs |

## Evidence & Artifacts

- Source script: `d1_fit_v4.py`
- Output: `D1_v4_fit_results.md`
- Codex v3 rejection: `/mnt/d/Codex/REPORTS/CODEX_20260710_D1_QUARK_KOIDE_V3_AUDIT.md`
- Codex v3 resubmission requirements: `/mnt/d/Devin/inbox/2026-07-10-codex-d1-v3-reject-resubmission.md`
- Codex independent Eq. (4) recomputation: `/mnt/d/Codex/EVIDENCE/d1_quark_koide_eq4_recompute.py`

## Boundary

- Numeric test of a published phenomenological model, not a PF first-principles derivation.
- No `lean/PfLean/*` theorem, `CLAIMS.md` tier, PUBLIC HOLD, release, medical, Legal, or Greg boundary changed.
- Awaiting Codex audit of this v4 packet before any catalog or claim update.

## Next

- Submit this v4 packet to Codex for audit.
- If Codex accepts the source convention and input boundary, consider a scale-consistent rerun as a follow-up study.
