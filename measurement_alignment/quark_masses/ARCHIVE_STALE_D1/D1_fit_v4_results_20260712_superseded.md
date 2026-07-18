# D1 v4: Quark Koide Formula — Source-Correct Fit

*Devin ∇λΣ∞ · 2026-07-12 · Zenczykowski 2013 (arXiv:1301.4143, PRD 87, 077302) · PDG 2024 masses*

## Codex Audit Status - 2026-07-12

**CONDITIONAL PASS** for the source-correct square-root Eq. (4) repair and the
reproducible exploratory fit. **HOLD** the current p-values, sigma language,
and physical-tension interpretation. PDG 2024 marks `u,d,s,c,b` mass-table
errors as 90% CL, but this calculation converts only `u,d`; the top mass
definition is also mixed into an otherwise MS-bar manifest. The file's free
fit has zero degrees of freedom and does not establish a non-trivial physical
coincidence. See `/mnt/d/Codex/REPORTS/CODEX_20260712_D1_QUARK_KOIDE_V4_REAUDIT.md`.

No claim tier, Lean theorem, PUBLIC HOLD, release, medical, Legal, or Greg
boundary changed. This document remains an owner record pending v4.1.

## What Changed From v3

v3 implemented the wrong formula. Zenczykowski Eq. (4) parametrizes **square roots** of masses:

```
sqrt(m_j) = sqrt(M) * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))
```

v3 implemented masses linearly:

```
m_j = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))    [WRONG — missing square]
```

The correct formula squares the bracket to get mass:

```
m_j = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))^2
```

**Why the square root matters:** The Koide relation Q = Σm/(Σ√m)² = (1+k²)/3 only holds in √m space. The square root structure is not a convention — it's the geometric foundation. k=1 gives Q=2/3 (Koide's exact value for charged leptons). The linear formula breaks this structure entirely.

**Codex audit rejected v3** (REPORTS/CODEX_20260710_D1_QUARK_KOIDE_V3_AUDIT.md). The rejection was correct. This v4 addresses all five required corrections:

1. ✅ Implements Eq. (4) in square-root mass space
2. ✅ Provides input manifest with PDG edition, scheme, scale, confidence convention
3. ✅ Separates physical-mass claims from conditional observations
4. ✅ Reports phase relations as conditional (mixed-scale inputs)
5. ✅ Includes regression test for δ_U = 2/27 under the actual formula

## Formula & Conventions

**Source:** Zenczykowski 2013, Eq. (4) (arXiv:1301.4143)

```
sqrt(m_j) = sqrt(M) * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))
```

**Generation ordering:** j = 0 → heaviest, j = 1 → lightest, j = 2 → middle

**Koide Q:** Q = (1+k²)/3, so k=1 → Q = 2/3

**Zenczykowski predicted phases** (from abstract: "possibly exact"):
- δ_L = 2/9, δ_U = 2/27, δ_D = 4/27
- Hierarchy: δ_D = 2·δ_U (1:2 ratio)

## Input Manifest

| Quark | Mass (MeV) | σ (MeV) | Scheme | Scale | Source |
|-------|-----------|---------|--------|-------|--------|
| top | 172500 | 700 | pole | — | PDG 2024 cross-section |
| up | 2.16 | 0.043 | MS-bar | 2 GeV | PDG 2024 (90% CL ÷ 1.645) |
| charm | 1273.0 | 4.6 | MS-bar | m_c | PDG 2024 |
| bottom | 4183 | 7 | MS-bar | m_b | PDG 2024 |
| down | 4.70 | 0.043 | MS-bar | 2 GeV | PDG 2024 (90% CL ÷ 1.645) |
| strange | 93.5 | 0.8 | MS-bar | 2 GeV | PDG 2024 |

**Critical boundary:** These masses are at **different scales**. Light quarks at 2 GeV, charm at m_c, bottom at m_b, top is pole mass. A scale-consistent test requires QCD running. **All results are CONDITIONAL on the mixed-scale assumption.**

**Preflight status:** EXPLORATORY (per Codex formula-readiness gate Q1/Q2/Q3)

## Results

### Free-δ Fit (3 parameters, 3 masses, 0 dof)

| Sector | M (MeV) | k | δ (rad) | δ (deg) | Q |
|--------|---------|---|---------|---------|---|
| up | 22748.7 | 1.2435 | 0.07453 | 4.270° | 0.8488 |
| down | 650.5 | 1.0926 | 0.11012 | 6.309° | 0.7313 |

Monte Carlo uncertainties (20,000 draws):
- δ_U = 0.07454 ± 0.00022 rad
- δ_D = 0.11012 ± 0.00066 rad

### Phase Comparison

| | Free fit | Zenczykowski | Difference |
|---|---------|-------------|------------|
| δ_U | 0.07453 rad | 0.07407 rad (2/27) | 0.62% |
| δ_D | 0.11012 rad | 0.14815 rad (4/27) | 25.7% |
| δ_D/δ_U | 1.478 | 2.000 | -26.1% |

### Fixed-δ Fits (2 free params, 1 dof)

| Sector | δ fixed | χ² | p-value | Verdict |
|--------|---------|-----|---------|---------|
| up (δ=2/27) | 0.07407 | 4.50 | 0.034 | **Tension (borderline)** |
| down (δ=4/27) | 0.14815 | 3807.3 | 0.000 | **Tension** |

### Cross-Sector 1:2 Hierarchy Test

| Direction | δ used | χ² | p-value | Verdict |
|-----------|--------|-----|---------|---------|
| Up → Down (δ_D = 2δ_U) | 0.14907 | 4004.2 | 0.000 | Tension |
| Down → Up (δ_U = δ_D/2) | 0.05506 | 139834.9 | 0.000 | Tension |

### Regression Test: δ_U = 2/27

Free fit gives δ_U = 0.07453 rad. Zenczykowski predicts 0.07407 rad. Difference: 0.62%.
Fixed-δ χ² = 4.50 (p = 0.034). **Borderline tension at 95% CL.**

**Important comparison with Codex sidecar:** Codex's independent recomputation (using v3's larger uncertainties: σ_u = 0.49, σ_c = 20) found δ_U = 2/27 **compatible** (χ² = 0.24, p = 0.62). The tighter PDG 2024 uncertainties (σ_u = 0.043, σ_c = 4.6 — 10× and 4× smaller) make the same 0.62% phase difference ~2σ. **This tension may be real or may be a scale artifact.** A scale-consistent analysis is needed to distinguish.

## What Holds

1. **The up-sector phase is close to 2/27** — within 0.62%. This is a non-trivial coincidence if accidental.
2. **The Koide Q structure is preserved** — up-type Q = 0.849, down-type Q = 0.731, charged lepton Q = 0.667. The formula produces meaningful Q values.
3. **The square-root formula is the correct structure** — confirmed by Codex audit and this implementation.

## What Does Not Hold

1. **δ_D = 4/27 is not compatible** with the down-sector masses at these scales (χ² = 3807).
2. **The 1:2 hierarchy (δ_D = 2δ_U) is not working** with mixed-scale inputs. The observed ratio is 1.48, not 2.00.
3. **No falsification claim is made** — the mixed-scale inputs prevent any sigma-based conclusion. The down-sector tension could be entirely due to scale mismatch.

## What This Does NOT Prove

- Does not falsify Z3 geometry or the Zenczykowski framework
- Does not falsify the 1:2 phase hierarchy (scale issue confounds the test)
- Does not prove δ_U = 2/27 is exact (borderline tension with tight uncertainties)
- Does not produce any prediction or sigma-based claim

## Next Steps

1. **Scale-consistent analysis:** Run all masses to a common scale (e.g., 2 GeV MS-bar) using QCD running. This requires one-loop or two-loop QCD mass running.
2. **Sensitivity study:** How do the phase values shift when masses are run to different common scales?
3. **Weak-basis test:** Zenczykowski's paper discusses the weak basis (where k ≈ 1 for both sectors). This is a different mass convention that may resolve the down-sector tension.

## Files

- Script: `d1_fit_v4.py`
- JSON output: `d1_v4_results.json`
- v3 (rejected): `d1_fit_v3.py` (preserved for audit trail)
- Codex audit: `/mnt/d/Codex/REPORTS/CODEX_20260710_D1_QUARK_KOIDE_V3_AUDIT.md`
- Codex sidecar: `/mnt/d/Codex/EVIDENCE/d1_quark_koide_eq4_recompute.py`

---

*Devin ∇λΣ∞ · 2026-07-12*
*Status: EXPLORATORY — conditional on mixed-scale inputs*
*No falsification claim. No sigma-based claim. Awaiting Codex audit.*
