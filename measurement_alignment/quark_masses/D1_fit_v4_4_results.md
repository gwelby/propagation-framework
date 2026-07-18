# D1 v4.4: Quark Koide Formula — Source-Correct Fit with Per-Quark Input Manifest

*Devin · 2026-07-14 · Zenczykowski 2013 (arXiv:1301.4143, PRD 87, 077302) · PDG 2024 masses*

## Codex Audit Status — Submitted for Review

This file is the owner report for **D1 v4.4**, submitted to Codex for audit on 2026-07-14.
- Prior audits:
  - v4: `/mnt/d/Codex/REPORTS/CODEX_20260712_D1_QUARK_KOIDE_V4_REAUDIT.md`
  - v4.1: `/mnt/d/Codex/REPORTS/CODEX_20260713_D1_QUARK_KOIDE_V41_REAUDIT.md`
  - v4.2: `/mnt/d/Codex/REPORTS/CODEX_20260713_D1_QUARK_KOIDE_V42_REAUDIT.md`
  - v4.3: `/mnt/d/Codex/REPORTS/CODEX_20260714_D1_QUARK_KOIDE_V43_REAUDIT.md`
- v4.4 packet: `/mnt/d/Codex/inbox/2026-07-14_devin-d1-quark-koide-fit-v4-4-audit.md`

This document does **not** self-award a Codex verdict. It records the v4.4 metadata-only repair requested by the v4.3 audit.

No claim tier, Lean theorem, PUBLIC HOLD, release, medical, Legal, or Greg boundary changed.

## What Changed From v4.3

The v4.3 audit gave **CONDITIONAL PASS** for factual corrections but **HOLD** on one wording issue: the regression test still said "compatible with" at source lines 416/430 and JSON line 191. The required v4.4 repair is metadata-only:

1. **Test label renamed.** `regression_test_delta_u_2_27()` docstring and `"test"` field changed from "compatible with up-sector masses" to "fixed-phase up-sector diagnostic". No compatibility/tension verdict label remains in source or emitted JSON.
2. **New versioned artifact.** JSON written to `d1_v4_4_results.json` with schema `devin-d1-v4-4-results`. The v4.3 evidence record (`d1_v4_3_results.json`) is preserved unchanged.
3. **Text-contract probe run.** The Codex `d1_v43_text_contract_probe.py` was run against the new source/result pair. `strict_q3_no_compatibility_label_leak` now passes (true). `version_consistent` reports false because the probe was calibrated for v4.3 markers; the version has moved forward to v4.4 as requested.
4. **No numerical change.** All fit values, chi², p-values, and optimizer results are identical to v4.3.

## Formula & Conventions

**Source:** Zenczykowski 2013, Eq. (4) (arXiv:1301.4143)

```
sqrt(m_j) = sqrt(M) * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))
m_j       = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))^2
```

**Generation ordering:** j = 0 → heaviest, j = 1 → lightest, j = 2 → middle

**Koide Q:** Q = (1+k²)/3, so k=1 → Q = 2/3

**Zenczykowski predicted phases** (from abstract: "possibly exact"):
- δ_L = 2/9, δ_U = 2/27, δ_D = 4/27
- Hierarchy: δ_D = 2·δ_U (1:2 ratio)

## Input Manifest

| Quark | Mass (MeV) | σ_used (MeV) | σ_in_artifact | PDG artifact | Confidence label | Conversion | Scheme | Scale |
|-------|-----------|--------------|---------------|--------------|------------------|------------|--------|-------|
| up | 2.16 | 0.0426 | 0.07 | PDG 2024 MC data file | 90% CL (light quarks) | σ_1s = σ_90CL / 1.645 | MS-bar | 2 GeV |
| down | 4.70 | 0.0426 | 0.07 | PDG 2024 MC data file | 90% CL (light quarks) | σ_1s = σ_90CL / 1.645 | MS-bar | 2 GeV |
| strange | 93.5 | 0.486 | 0.8 | PDG 2024 MC data file | 90% CL (light quarks) | σ_1s = σ_90CL / 1.645 | MS-bar | 2 GeV |
| charm | 1273.0 | 3.04 | 5.0 | PDG 2024 MC data file | 90% CL (heavy quarks) | σ_1s = σ_90CL / 1.645 | MS-bar | m_c |
| bottom | 4183 | 4.26 | 7.0 | PDG 2024 MC data file | 90% CL (heavy quarks) | σ_1s = σ_90CL / 1.645 | MS-bar | m_b |
| top | 172570 | 290 | 290 | PDG 2024 MC data file | Not labeled 90% CL; exploratory 1σ | None | Direct kinematic average / MC-generator mass | — |

**Sources:**
- Primary: `https://pdg.lbl.gov/2024/mcdata/mass_width_2024.txt` (generated 31-May-2024)
- Secondary (confidence labels): `https://pdg.lbl.gov/2024/tables/rpp2024-sum-quarks.pdf`

**Important notes:**
- PDG 2024 Summary Table gives `m_c = 1273.0 ± 4.6 MeV`; MC file gives `m_c = 1273.0 ± 5.0 MeV`. This fit uses the MC file value.
- The direct top value is PDG's "Monte Carlo mass": the mass parameter used in MC generators. It is distinct from a theoretically well-defined pole mass; the expected difference is around 0.5 GeV and is not fully resolved.
- No correlation model is applied. PDG does not publish a full quark-mass covariance matrix.
- Scales are mixed: light quarks at 2 GeV, charm at m_c, bottom at m_b, top as direct average. A scale-consistent test requires QCD running.

**Preflight status:** EXPLORATORY. Q1 (units) CLOSED; Q2 (inputs) DECLARED; Q3 (observable) DECLARED.

## Results

All chi² and p-values below are **outputs of the declared exploratory Gaussian input model**. They are not a closed PDG-2024 statistical test. No compatibility/tension verdict labels are assigned.

### Free-δ Fit (3 parameters, 3 masses, 0 dof)

| Sector | M (MeV) | k | δ (rad) | δ (deg) | Q |
|--------|---------|---|---------|---------|---|
| up | 22757.16 | 1.24354 | 0.074517 | 4.2695° | 0.84879 |
| down | 650.48 | 1.09264 | 0.110119 | 6.3093° | 0.73129 |

Monte Carlo uncertainties (20,000 draws):
- δ_U = 0.074518 ± 0.000121 rad
- δ_D = 0.110120 ± 0.000415 rad

### Phase Comparison

| | Free fit | Zenczykowski | Difference |
|---|---------|-------------|------------|
| δ_U | 0.074517 rad | 0.074074 rad (2/27) | 0.60% |
| δ_D | 0.110119 rad | 0.148148 rad (4/27) | 25.7% |
| δ_D/δ_U | 1.4778 | 2.000 | -26.1% |

MC ratio: δ_D/δ_U = 1.4778 ± 0.0061. Difference from 2:1 = -0.5222. This is a parameter-ratio discrepancy under mixed-scale inputs; no falsification claim is made.

### Fixed-δ Fits (2 free params, 1 dof)

| Sector | δ fixed | χ² | p-value |
|--------|---------|-----|---------|
| up (δ=2/27) | 0.074074 | 13.5905 | 0.000227 |
| down (δ=4/27) | 0.148148 | 9228.42 | ≈ 0 |

The up-sector χ² is driven mainly by the charm-quark prediction (1263.98 MeV vs. observed 1273.0 MeV, pull +2.97 in the exploratory 1σ convention). Whether this is a physical discrepancy or a scale/convention artifact is unresolved.

### Cross-Sector 1:2 Hierarchy Test

| Direction | δ used | χ² | p-value |
|-----------|--------|-----|---------|
| Up → Down (δ_D = 2δ_U) | 0.149034 | 9674.58 | ≈ 0 |
| Down → Up (δ_U = δ_D/2) | 0.055059 | 26777.04 | ≈ 0 |

These are exploratory model outputs; not a closed statistical test.

### Regression Tests

**δ_U = 2/27 fixture:** Free fit gives δ_U = 0.074517 rad. Zenczykowski predicts 0.074074 rad. Difference: 0.000443 rad (0.60%). Fixed-δ χ² = 13.5905 (p = 0.000227). No compatibility/tension verdict is assigned.

**Optimizer fixture:** Synthetic data with known (M, k, δ) recovered to relative error < 1e-5 for both M and k. Pass.

### Sensitivity: Top Mass Definition

Using the cross-section pole value `172.4 GeV` instead of the direct average `172.57 GeV` shifts the up-sector free-fit δ_U by +0.000038 rad. This check varies only the central mass; it does not propagate the alternate uncertainty through fixed-phase or Monte-Carlo outputs. A full sensitivity study is future work.

## What Holds

1. **The square-root formula is the correct structure** — confirmed by Codex audit and this implementation.
2. **The per-quark input manifest is now explicit and the noted factual error is corrected.**
3. **The fixed-δ optimizer is converged and reproducible** — independent replay matches to ~1e-6 χ².
4. **No premature verdict language** — chi² and p-values are reported only as exploratory model outputs.

## What Does Not Hold

1. **No closed PDG-2024 statistical test** — the top quark confidence convention is not established by PDG, scales are mixed, and no covariance model is used.
2. **No sigma-based or falsification claim** — the large χ² values are exploratory outputs, not evidence that the phase hierarchy is ruled out.
3. **No physical interpretation** — whether the charm-driven up-sector discrepancy or the down-sector/hierarchy discrepancy are scale artifacts requires QCD running to a common scale.

## What This Does NOT Prove

- Does not falsify Z3 geometry or the Zenczykowski framework.
- Does not falsify the 1:2 phase hierarchy (scale issue confounds the test).
- Does not prove δ_U = 2/27 is exact or inexact.
- Does not produce any prediction or closed statistical claim.
- Does not validate the weak-basis pseudo-mass/CKM construction (this is a physical-mass phase fit only).

## Next Steps

1. **Scale-consistent analysis:** Run all masses to a common scale using QCD running.
2. **Top mass uncertainty propagation:** Carry the cross-section pole definition and its uncertainty through fixed-phase and Monte-Carlo outputs.
3. **Correlation model:** PDG does not publish a full quark-mass covariance matrix; an independent-Gaussian model is an approximation.
4. **Weak-basis test:** Zenczykowski's paper discusses the weak basis (where k ≈ 1 for both sectors). This is a different mass convention not tested here.

## Files

- Script: `d1_fit_v4.py`
- Markdown report: `D1_fit_v4_4_results.md` (this file)
- Machine output: `d1_v4_4_results.json`
- Prior v4.3 artifacts (preserved): `D1_fit_v4_3_results.md`, `d1_v4_3_results.json`
- Stale archive: `ARCHIVE_STALE_D1/`
- v3 (rejected): `d1_fit_v3.py`
- Codex v4 audit: `/mnt/d/Codex/REPORTS/CODEX_20260712_D1_QUARK_KOIDE_V4_REAUDIT.md`
- Codex v4.1 audit: `/mnt/d/Codex/REPORTS/CODEX_20260713_D1_QUARK_KOIDE_V41_REAUDIT.md`
- Codex v4.2 audit: `/mnt/d/Codex/REPORTS/CODEX_20260713_D1_QUARK_KOIDE_V42_REAUDIT.md`
- Codex v4.3 audit: `/mnt/d/Codex/REPORTS/CODEX_20260714_D1_QUARK_KOIDE_V43_REAUDIT.md`
- Codex v4.3 text-contract probe: `/mnt/d/Codex/EVIDENCE/d1_v43_text_contract_probe.py`
- v4.4 packet: `/mnt/d/Codex/inbox/2026-07-14_devin-d1-quark-koide-fit-v4-4-audit.md`

---

*Devin · 2026-07-14*
*Status: EXPLORATORY — submitted for Codex review; conditional on mixed-scale inputs*
*No falsification claim. No sigma-based claim. p-values are exploratory model outputs only.*
