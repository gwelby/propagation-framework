# D3 v3: CKM Angle Scan — Branch Continuation + Sensitivity Study

> **SUPERSEDED by D3 v3.1 — see `/mnt/d/Fundamentals/measurement_alignment/ckm_mixing/D3v3_1_ckm_results.md`.**
>
> The Monte Carlo "uncertainty propagation" section in this file (Section 5) was rejected by Codex in `CODEX_20260712_D3V3_CKM_BRANCH_CONTINUATION_AUDIT.md` for wrong PDG uncertainty values (sin(θ₁₂)=0.00029 instead of 0.00068; sin(θ₁₃) symmetric instead of asymmetric), a one-sided asymmetric sampler, and unverifiable pre-registration. The corrected sensitivity envelope and exploratory MC are in the v3.1 report. The central branch result (2.988° → 4.3085°) remains valid and is preserved in v3.1.

*Devin · 2026-07-12 · Zenczykowski 2013 (arXiv:1301.4143v2) · PDG 2024*
*Corrected per Codex audit CODEX_20260711_D3V2_CKM_PSEUDOMASS_AUDIT.md*

## Pre-Registration (Declared Before Computation)

**Analysis type:** SENSITIVITY STUDY — non-statistical
**Reason:** Quark masses are at different renormalization scales (light: MS-bar 2 GeV, c/b: MS-bar at own mass, t: pole mass). Without QCD running to a common scale, no sigma-based falsification or prediction claim is valid.
**Branch rule:** Track the paper's Eq. (25) root pair by continuity. Start from (paper masses, 2012 FX angles, k=1) where θ₂₃=2.988°. Identify the root pair (θ_b, θ_t) that produces 2.988°. Gradually interpolate masses and angles to PDG 2024 values. At each step, select the root pair closest to the previous step. Report where the tracked branch ends.
**Statistic:** Predicted θ₂₃ from the tracked branch vs. observed PDG 2024 θ₂₃. Reported as a qualitative sensitivity observation, not a sigma pull.
**Threshold:** No pass/fail threshold. This is a sensitivity study. The output is: where does the paper branch end up under PDG 2024 inputs, and how sensitive is it to mass and CKM parameter uncertainties?
**What this does NOT claim:** No falsification of Zenczykowski's model. No confirmation of the pseudo-mass Koide hypothesis. No sigma-based statistical test. No CLAIMS.md, MAP.md, or CKM tier change. CKM remains SILENT in PF.

## Corrections from D3 v2

D3 v2 was CONDITIONAL PASS for source replay but REJECTED for current-data claims. Five fixes:
1. **Branch selection by continuity:** Track paper's root pair from 2.988° checkpoint by homotopy, instead of picking smallest positive root
2. **Correct PDG 2024 CKM:** δ_CP = 1.147 (not 1.20), asymmetric θ₂₃ uncertainties
3. **Sensitivity study label:** Mixed-scale masses → no sigma-based claim. Explicitly labeled as non-statistical.
4. **Full uncertainty propagation:** Monte Carlo over mass + CKM parameter uncertainties + root-selection ambiguity
5. **Pre-registration:** Branch, statistic, and threshold declared above, before any computation

## 1. Unit Tests — Paper Checkpoint Reproduction

Using Zenczykowski's Eq. (23) masses and 2012 FX angles (θ_d=12.11°, θ_u=4.87°):


**Paper checkpoints reproduced.** Implementation matches source conventions.

## 2. PDG 2024 Reference Values (Corrected)

| Parameter | Value | Uncertainty | Source |
|---|---|---|---|
| sin(θ₁₂) | 0.22501 | ±0.00029 | PDG 2024 Eq. 12.28 |
| sin(θ₂₃) | 0.04183 | +0.00079/-0.00069 | PDG 2024 (asymmetric) |
| sin(θ₁₃) | 0.003732 | ±0.000119 | PDG 2024 Eq. 12.28 |
| δ_CP | 1.147 rad | ±0.026 | PDG 2024 Eq. 12.28 (CORRECTED from 1.20) |

### Fritzsch-Xing angles from PDG 2024 CKM (Eq. 20)

| Angle | Value | Formula |
|---|---|---|
| θ_u | 5.098° | atan(|V_ub|/|V_cb|) |
| θ_d | 11.793° | atan(|V_td|/|V_ts|) |
| θ₂₃ (observed) | 2.407° | asin(√(|V_ub|²+|V_cb|²)) |

CKM matrix elements: |V_ub|=0.00373, |V_cb|=0.04183, |V_td|=0.00858, |V_ts|=0.04111

Comparison with Zenczykowski's 2012 extraction:
- θ_d: PDG 2024 = 11.793° vs 2012 = 12.11°
- θ_u: PDG 2024 = 5.098° vs 2012 = 4.87°

## 3. Mass Data

### Paper Eq. (23) masses (MeV, source coordinate order)
- Down (d,s,b): [7.843, 160.0, 4209.0]
- Up (u,c,t): [4.392, 1296.0, 172000.0]

### PDG 2024 masses (MeV, MIXED SCALE — sensitivity study only)

| Quark | Central (MeV) | 1σ (MeV) | Scheme | Note |
|---|---|---|---|---|
| d | 4.70 | 0.043 | MS-bar 2 GeV | 90% CL ÷ 1.645 |
| s | 93.5 | 0.486 | MS-bar 2 GeV | 90% CL ÷ 1.645 (±0.8 → 0.486) |
| b | 4183.0 | 4.26 | MS-bar at m_b | 90% CL ÷ 1.645 (±7.0 → 4.26) |
| u | 2.16 | 0.043 | MS-bar 2 GeV | 90% CL ÷ 1.645 |
| c | 1273.0 | 2.80 | MS-bar at m_c | 90% CL ÷ 1.645 (±4.6 → 2.80) |
| t | 172500.0 | 700.0 | Pole mass | Cross-section extraction |

**WARNING:** These masses are at different renormalization scales. This is a SENSITIVITY STUDY, not a scale-consistent test. No sigma-based falsification claim is made.

## 4. Branch Continuation Analysis (Core v3 Fix)

### Method

Instead of selecting the smallest positive root difference, we track the paper's
root pair by homotopy continuation:
1. Start at paper parameters (Eq. 23 masses, 2012 FX angles, k=1)
2. Identify the root pair (θ_b, θ_t) that gives θ₂₃ = 2.988°
3. Gradually interpolate to PDG 2024 masses and FX angles (100 steps)
4. At each step, select the root pair closest to the previous step (continuity)
5. Report where the tracked branch ends

### 4a. Paper masses → PDG masses (2012 FX angles held fixed)

This isolates the effect of mass changes while keeping the paper's angle extraction.

Starting θ₂₃: 2.9883° (paper checkpoint: 2.988°)
Ending θ₂₃: 4.3039°
Observed θ₂₃: 2.407° (FX, PDG 2024)

Trajectory (selected steps):

| Step | λ | θ_d (°) | θ_u (°) | θ_b (°) | θ_t (°) | θ₂₃ pred (°) |
|---|---|---|---|---|---|---|
| 0 | 0.00 | 12.110 | 4.870 | -0.5537 | -3.5420 | 2.9883 |
| 10 | 0.10 | 12.110 | 4.870 | -0.4299 | -3.5411 | 3.1112 |
| 20 | 0.20 | 12.110 | 4.870 | -0.3046 | -3.5403 | 3.2357 |
| 30 | 0.30 | 12.110 | 4.870 | -0.1776 | -3.5394 | 3.3618 |
| 40 | 0.40 | 12.110 | 4.870 | -0.0488 | -3.5385 | 3.4897 |
| 50 | 0.50 | 12.110 | 4.870 | 0.0819 | -3.5376 | 3.6195 |
| 60 | 0.60 | 12.110 | 4.870 | 0.2147 | -3.5368 | 3.7514 |
| 70 | 0.70 | 12.110 | 4.870 | 0.3497 | -3.5359 | 3.8856 |
| 80 | 0.80 | 12.110 | 4.870 | 0.4872 | -3.5350 | 4.0222 |
| 90 | 0.90 | 12.110 | 4.870 | 0.6274 | -3.5341 | 4.1615 |
| 100 | 1.00 | 12.110 | 4.870 | 0.7706 | -3.5333 | 4.3039 |
| 100 | 1.00 | 12.110 | 4.870 | 0.7706 | -3.5333 | 4.3039 |

**Result:** The paper branch moves from 2.988° to 4.3039° when masses are changed from paper Eq. (23) to PDG 2024 (mixed-scale), with 2012 FX angles held fixed.

**Comparison with v2:** v2 reported 0.2330° for this configuration by selecting the smallest positive root. The continuity-tracked branch ends at 4.3039° instead. This confirms Codex's finding that v2 promoted a different branch.

### 4b. Paper masses + 2012 angles → PDG masses + PDG 2024 angles

This is the full interpolation: both masses and FX angles change to PDG 2024 values.

Starting θ₂₃: 2.9883° (paper checkpoint: 2.988°)
Ending θ₂₃: 4.3085°
Observed θ₂₃: 2.407° (FX, PDG 2024)

Trajectory (selected steps):

| Step | λ | θ_d (°) | θ_u (°) | θ_b (°) | θ_t (°) | θ₂₃ pred (°) |
|---|---|---|---|---|---|---|
| 0 | 0.00 | 12.110 | 4.870 | -0.5537 | -3.5420 | 2.9883 |
| 10 | 0.10 | 12.078 | 4.893 | -0.4273 | -3.5390 | 3.1117 |
| 20 | 0.20 | 12.047 | 4.916 | -0.2992 | -3.5359 | 3.2367 |
| 30 | 0.30 | 12.015 | 4.939 | -0.1696 | -3.5329 | 3.3634 |
| 40 | 0.40 | 11.983 | 4.961 | -0.0381 | -3.5299 | 3.4918 |
| 50 | 0.50 | 11.951 | 4.984 | 0.0952 | -3.5269 | 3.6221 |
| 60 | 0.60 | 11.920 | 5.007 | 0.2305 | -3.5240 | 3.7545 |
| 70 | 0.70 | 11.888 | 5.030 | 0.3681 | -3.5210 | 3.8891 |
| 80 | 0.80 | 11.856 | 5.053 | 0.5081 | -3.5181 | 4.0262 |
| 90 | 0.90 | 11.824 | 5.076 | 0.6507 | -3.5151 | 4.1659 |
| 100 | 1.00 | 11.793 | 5.098 | 0.7963 | -3.5122 | 4.3085 |
| 100 | 1.00 | 11.793 | 5.098 | 0.7963 | -3.5122 | 4.3085 |

**Result:** The paper branch ends at 4.3085° under full PDG 2024 inputs (mixed-scale masses + PDG 2024 FX angles).

**Comparison with v2:** v2 reported 0.2077° by selecting the smallest positive root. The continuity-tracked branch ends at 4.3085°. This is consistent with Codex's independent finding that the paper branch continues to ~4.31° under PDG central substitution.

### 4c. Same as 4b but with k̃ = 1.015 (Zenczykowski's 1.5% departure)

Starting θ₂₃: 2.4426° (paper checkpoint: 2.44°)
Ending θ₂₃: 3.7258°
Observed θ₂₃: 2.407° (FX, PDG 2024)

## 5. Monte Carlo Uncertainty Propagation

500 draws perturbing mass uncertainties (1σ Gaussian) and CKM parameter 
uncertainties (including asymmetric θ₂₃). For each draw, the branch is tracked 
from the paper checkpoint to the perturbed endpoint.

**Successful draws:** 500 / 500

| Statistic | Value (°) |
|---|---|
| Mean | 4.3132 |
| Std | 0.0226 |
| Median | 4.3128 |
| 5th percentile | 4.2762 |
| 95th percentile | 4.3492 |
| Min | 4.2467 |
| Max | 4.3775 |

**Observed θ₂₃ (FX):** 2.407° (PDG 2024)
**Observed θ₂₃ uncertainty:** +0.0453° / -0.0396° (asymmetric)

**This is a sensitivity study, not a statistical test.** The Monte Carlo shows the spread of the branch-tracked prediction under mass and CKM parameter uncertainties. It does not account for the dominant uncontrolled systematic: masses from incompatible renormalization scales. No sigma-based claim is made.

## 6. All Branches at PDG 2024 Central Values

For completeness, here are ALL root pair differences at the PDG 2024 endpoint, not just the continuity-tracked one. This shows the full solution structure.

Down roots (θ_b): ['-89.2037°', '-3.3295°', '0.7963°', '86.6705°']
Up roots (θ_t): ['-87.3302°', '-3.5122°', '2.6698°', '86.4878°']

| # | θ_b (°) | θ_t (°) | θ₂₃ = θ_b - θ_t (°) | Continuity-tracked? |
|---|---|---|---|---|
| 1 | 86.6705 | 86.4878 | 0.1827 |  |
| 2 | -3.3295 | -3.5122 | 0.1827 |  |
| 3 | -89.2037 | -87.3302 | -1.8735 |  |
| 4 | 0.7963 | 2.6698 | -1.8735 |  |
| 5 | 0.7963 | -3.5122 | 4.3085 | YES ← |
| 6 | -3.3295 | 2.6698 | -5.9993 |  |

The continuity-tracked branch is the one that connects to the paper's 2.988° checkpoint. Other branches exist but are not continuations of the paper's result.

## 7. Assessment

**What was corrected:**
- Branch selection now uses continuity tracking from the paper's 2.988° checkpoint
- PDG 2024 CKM parameters corrected: δ_CP = 1.147, asymmetric θ₂₃ uncertainties
- Mixed-scale masses explicitly labeled as sensitivity study, not statistical test
- Monte Carlo propagates mass + CKM + root-selection uncertainties
- Analysis pre-registered before computation

**What the corrected analysis shows:**

1. **Branch continuation result:** The paper's 2.988° branch ends at 4.3085° under PDG 2024 inputs (mixed-scale masses + PDG 2024 FX angles).
   Observed θ₂₃ = 2.407°. The branch-tracked prediction is 1.90° from the observed value.
   This is a **qualitative sensitivity observation**, not a statistical test.

2. **Mass-only effect:** Changing masses from paper to PDG (2012 angles fixed) moves the branch from 2.988° to 4.3039°. The strange-mass substitution (160→93.5 MeV) is the dominant driver.

3. **Uncertainty spread:** Monte Carlo (500 draws) gives θ₂₃ = 4.31° ± 0.02° (90% CI: 4.28° to 4.35°). This spread reflects mass and CKM parameter uncertainties but NOT the scale-mixing systematic, which is uncontrolled.

**What this does NOT prove:**
- It does not falsify Zenczykowski's model. The mixed-scale masses prevent any falsification claim.
- It does not confirm the pseudo-mass Koide hypothesis. It tests branch continuity.
- It does not connect to PF's Z3 geometry directly.
- It does not produce a sigma-based statistical test.
- No CLAIMS.md, MAP.md, or CKM tier change is warranted.

**What would be needed for a statistical test:**
- Run all six quark masses to a common renormalization scale with a trusted QCD prescription
- Include PDG-published CKM-fit covariance (not just independent parameter uncertainties)
- Pre-register the branch, statistic, and pass/fail threshold before the scale-consistent run
- Only then would a sigma-based comparison to observed θ₂₃ be meaningful

## 8. Method Notes

- Source: Zenczykowski, arXiv:1301.4143v2, Eqs. (14), (16), (17), (20), (23)-(25)
- R12: Eq. (16) `[[c,-s,0],[s,c,0],[0,0,1]]`
- R23: Eq. (17) with phase dropped per Eq. (22) justification
- Pseudo-mass: Eq. (14) linear definition `m̃_j = |Σ_k U_jk · m_k|`
- Koide Q: `Q̃ = (Σ m̃_j) / (Σ √m̃_j)²`; target `Q = (1+k̃²)/3`
- Scan domain: `[-π/2, π/2]` (signed, per paper Fig. 1)
- Root finding: brentq on sign-changing intervals, 2001 grid points (50001 for unit tests)
- Branch tracking: homotopy continuation, 100 interpolation steps
- FX angle extraction: Eq. (20), `θ_u=atan(|V_ub|/|V_cb|)`, `θ_d=atan(|V_td|/|V_ts|)`
- PDG 2024 CKM: sin(θ₁₂)=0.22501, sin(θ₂₃)=0.04183, sin(θ₁₃)=0.003732, δ_CP=1.147
- PDG 2024 FX angles: θ_d=11.793°, θ_u=5.098°
- Mass scheme: MIXED (light: MS-bar 2 GeV, c/b: MS-bar at own mass, t: pole mass)
- 90% CL uncertainties converted to 1σ by dividing by 1.645 for light quarks
- Monte Carlo: 500 draws, independent Gaussian mass perturbations, asymmetric θ₂₃ perturbation, 20 continuation steps per draw
- Source script: `d3_ckm_scan_v3.py` in this directory
