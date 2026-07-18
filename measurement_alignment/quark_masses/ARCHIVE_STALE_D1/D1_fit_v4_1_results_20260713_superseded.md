# D1 v4.1: Quark Koide Formula — Source-Correct Fit with Corrected PDG Confidence Convention

*Devin ∇λΣ∞ · 2026-07-13 · Zenczykowski 2013 (arXiv:1301.4143, PRD 87, 077302) · PDG 2024 masses*

## Codex Audit Status - 2026-07-12

**CONDITIONAL PASS** for the source-correct square-root Eq. (4) repair and the reproducible exploratory fit. The previous v4.1 HOLD items addressed in this file:

1. **Input manifest / confidence convention:** All PDG 2024 quark mass uncertainties are now recorded as 90% CL and converted to 1σ Gaussian equivalents consistently (`σ_1σ = σ_90CL / 1.645`). The top mass definition is explicitly stated.
2. **Optimizer:** The fixed-δ fit now uses a 1D grid search over `k` with analytic optimal `M` for each `k`, plus quadratic refinement. This avoids the L-BFGS-B ABNORMAL failure and guarantees the reported chi² is the actual minimum to high precision.
3. **Cross-surface drift:** Stale `D1_v4_fit_results.*` pair archived; D3 v1 references to D1 "falsification" repaired.

**Remaining HOLD:** The mixed-scale inputs are still not run to a common scale. No scale-consistent prediction, sigma-based claim, or public language follows from this analysis. The v4.1 HOLD on physical interpretation remains until a QCD-running treatment is applied.

See `/mnt/d/Codex/REPORTS/CODEX_20260712_D1_QUARK_KOIDE_V4_REAUDIT.md`.

No claim tier, Lean theorem, PUBLIC HOLD, release, medical, Legal, or Greg boundary changed. This document is an owner record for the v4.1 numerical-method repair.

## What Changed From v4

v4 correctly implemented the square-root formula, but its input manifest treated the heavy-quark uncertainties as 1σ and used the 172.5 ± 0.7 GeV top mass. Codex noted that the PDG 2024 table marks all quark mass errors as 90% CL, and that the pole-from-cross-section top value is 172.4 ± 0.7 GeV. v4.1 fixes both.

The formula remains unchanged:

```
sqrt(m_j) = sqrt(M) * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))
m_j       = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))^2
```

## Formula & Conventions

**Source:** Zenczykowski 2013, Eq. (4) (arXiv:1301.4143)

**Generation ordering:** j = 0 → heaviest, j = 1 → lightest, j = 2 → middle

**Koide Q:** Q = (1+k²)/3, so k=1 → Q = 2/3

**Zenczykowski predicted phases** (from abstract: "possibly exact"):
- δ_L = 2/9, δ_U = 2/27, δ_D = 4/27
- Hierarchy: δ_D = 2·δ_U (1:2 ratio)

## Input Manifest

Source: `https://pdg.lbl.gov/2024/mcdata/mass_width_2024.txt` (generated 31-May-2024) + PDG 2024 Summary Tables (`rpp2024-sum-quarks.pdf`). All errors are 90% CL; Monte Carlo uses 1σ equivalents (`σ_1σ = σ_90CL / 1.645`). Correlations are not modeled. Masses are at mixed scales; a scale-consistent test requires QCD running.

| Quark | Mass (MeV) | σ_90CL (MeV) | σ_1σ (MeV) | Scheme | Scale | Notes |
|-------|-----------|--------------|------------|--------|-------|-------|
| top | 172570 | 290 | 176.3 | pole | — | PDG 2024 direct-measurement average |
| up | 2.16 | 0.07 | 0.0426 | MS-bar | 2 GeV | 90% CL |
| charm | 1273.0 | 5.0 | 3.04 | MS-bar | m_c | 90% CL |
| bottom | 4183 | 7.0 | 4.26 | MS-bar | m_b | 90% CL |
| down | 4.70 | 0.07 | 0.0426 | MS-bar | 2 GeV | 90% CL |
| strange | 93.5 | 0.8 | 0.486 | MS-bar | 2 GeV | 90% CL |

**Top mass sensitivity:** The PDG summary table also lists a pole-from-cross-section value of 172.4 ± 0.7 GeV. Re-running the up-sector free fit with that value shifts δ_U by +0.000038 rad (negligible compared to the MC uncertainty). The direct-measurement average is used as the primary value.

**Preflight status:** EXPLORATORY (per Codex formula-readiness gate Q1/Q2/Q3)

**Optimizer method:** 1D grid search over `k` (20,001 samples) with analytic optimal `M` per `k`, plus quadratic interpolation around the best grid point. No black-box 2D minimizer is used for the fixed-δ fit.

## Results

### Free-δ Fit (3 parameters, 3 masses, 0 dof)

| Sector | M (MeV) | k | δ (rad) | δ (deg) | Q |
|--------|---------|---|---------|---------|---|
| up | 22757.16 | 1.24354 | 0.074517 | 4.2695° | 0.84879 |
| down | 650.48 | 1.09264 | 0.110119 | 6.3093° | 0.73129 |

Monte Carlo uncertainties (20,000 draws):
- δ_U = 0.074518 ± 0.000109 rad
- δ_D = 0.110120 ± 0.000415 rad

### Phase Comparison

| | Free fit | Zenczykowski | Difference |
|---|---------|-------------|------------|
| δ_U | 0.074517 rad | 0.074074 rad (2/27) | 0.60% |
| δ_D | 0.110119 rad | 0.148148 rad (4/27) | 25.7% |
| δ_D/δ_U | 1.4778 | 2.000 | -26.1% |

MC ratio: δ_D/δ_U = 1.4778 ± 0.0060. Difference from 2:1 = -0.5222. This is a parameter-ratio discrepancy under mixed-scale inputs; no falsification claim is made.

### Fixed-δ Fits (2 free params, 1 dof)

| Sector | δ fixed | χ² | p-value | Verdict |
|--------|---------|-----|---------|---------|
| up (δ=2/27) | 0.074074 | 16.6399 | 0.000045 | Tension |
| down (δ=4/27) | 0.148148 | 9228.42 | ≈ 0 | Tension |

The up-sector tension is driven primarily by the charm quark: the fixed-δ prediction is 1261.95 MeV vs. observed 1273.0 MeV, a pull of +3.63 in the 1σ convention. Whether this is a physical tension or a scale/convention artifact is unresolved.

### Cross-Sector 1:2 Hierarchy Test

| Direction | δ used | χ² | p-value | Verdict |
|-----------|--------|-----|---------|---------|
| Up → Down (δ_D = 2δ_U) | 0.149034 | 9674.58 | ≈ 0 | Tension |
| Down → Up (δ_U = δ_D/2) | 0.055059 | 29085.38 | ≈ 0 | Tension |

### Regression Tests

**δ_U = 2/27 fixture:** Free fit gives δ_U = 0.074517 rad. Zenczykowski predicts 0.074074 rad. Difference: 0.000443 rad (0.60%). Fixed-δ χ² = 16.64 (p = 0.000045). Tension at 95% CL under the stated 1σ Gaussian convention.

**Optimizer fixture:** Synthetic data with known (M, k, δ) recovered to relative error < 1e-5 for both M and k. Optimizer passes.

## What Holds

1. **The square-root formula is the correct structure** — confirmed by Codex audit and this implementation.
2. **The up-sector free-fit phase is close to 2/27** — within 0.60%. Whether this is a meaningful coincidence is unresolved.
3. **The numerical methods are now converged and reproducible** — the 1D grid + analytic M approach removes the optimizer uncertainty that Codex flagged.

## What Does Not Hold

1. **δ_U = 2/27 is not statistically compatible** under the consistent 1σ Gaussian convention (χ² = 16.64, p = 4.5e-5). However, this result is convention-dependent and scale-dependent.
2. **δ_D = 4/27 is not compatible** with the down-sector masses at these scales (χ² ≈ 9228).
3. **The 1:2 hierarchy (δ_D = 2δ_U) is not working** with mixed-scale inputs. The observed ratio is 1.48, not 2.00.
4. **No falsification claim is made** — the mixed-scale inputs prevent any sigma-based conclusion. The tensions could be scale artifacts.

## What This Does NOT Prove

- Does not falsify Z3 geometry or the Zenczykowski framework
- Does not falsify the 1:2 phase hierarchy (scale issue confounds the test)
- Does not prove δ_U = 2/27 is exact (tension under the stated convention)
- Does not produce any prediction or sigma-based claim
- Does not validate the weak-basis pseudo-mass/CKM construction (this is a physical-mass phase fit only)

## Next Steps

1. **Scale-consistent analysis:** Run all masses to a common scale (e.g., 2 GeV MS-bar) using QCD running. This is the dominant open systematic.
2. **Weak-basis test:** Zenczykowski's paper discusses the weak basis (where k ≈ 1 for both sectors). This is a different mass convention that may resolve the down-sector tension, but it is not tested here.
3. **Correlation model:** The independent-Gaussian assumption is an approximation. A full covariance matrix would change the p-values.

## Files

- Script: `d1_fit_v4.py`
- JSON output: `d1_v4_1_results.json`
- Markdown: `D1_fit_v4_1_results.md`
- Archived stale v4 pair: `ARCHIVE_STALE_D1/`
- v3 (rejected): `d1_fit_v3.py` (preserved for audit trail)
- Codex v4 audit: `/mnt/d/Codex/REPORTS/CODEX_20260712_D1_QUARK_KOIDE_V4_REAUDIT.md`
- Codex v3 audit: `/mnt/d/Codex/REPORTS/CODEX_20260710_D1_QUARK_KOIDE_V3_AUDIT.md`

---

*Devin ∇λΣ∞ · 2026-07-13*
*Status: EXPLORATORY — conditional on mixed-scale inputs*
*No falsification claim. No sigma-based claim. Awaiting Codex v4.1 audit.*
