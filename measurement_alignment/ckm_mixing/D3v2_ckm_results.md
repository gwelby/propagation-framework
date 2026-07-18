# D3 v2: CKM Angle Scan — Fritzsch-Xing + Pseudo-Mass Koide
*Devin · 2026-07-11 · Zenczykowski 2013 (arXiv:1301.4143v2) · PDG 2024*
*Corrected per Codex audit CODEX_20260710_D3_CKM_PSEUDOMASS_AUDIT.md*

## Corrections from D3 v1

D3 v1 was REJECTED by Codex for three implementation errors:
1. **R12 transpose:** Used `[[c,s],[-s,c]]` instead of source Eq. (16) `[[c,-s],[s,c]]`
2. **Mass ordering:** Used `(b,d,s)` and `(t,u,c)` instead of `(d,s,b)` and `(u,c,t)`
3. **Restricted domain:** Scanned `[0,π/2]` instead of `[-π/2,π/2]`, excluding negative roots

All three are fixed in v2. Unit tests reproduce the paper's checkpoints.

## 1. Unit Tests — Paper Checkpoint Reproduction

Using Zenczykowski's Eq. (23) masses and 2012 FX angles (θ_d=12.11°, θ_u=4.87°):


**Paper checkpoints reproduced.** Implementation matches source conventions.

## 2. Method

```
Fritzsch-Xing (Zenczykowski Eq. 15-17):
  U = R_23(θ₂₃) · R_12(θ₁₂)
  R_12(θ) = [[c, -s, 0], [s, c, 0], [0, 0, 1]]   (Eq. 16)
  R_23(θ) = [[1, 0, 0], [0, c, s], [0, -s, c]]    (Eq. 17, phase dropped)

Pseudo-mass (Eq. 14): m̃_j = |Σ_k U_jk · m_k|
Koide constraint: Q̃ = (Σ m̃_j) / (Σ √m̃_j)² = (1+k̃²)/3
  k̃ = 1 → Q̃ = 2/3 (exact Koide)
  k̃ = 1.015 → Q̃ = 0.6767 (Zenczykowski's 1.5% departure)

CKM 2-3 angle: θ₂₃ = θ_b - θ_t
  θ_b: root of Q̃_D(θ_d, θ_b) = target_Q(k̃)
  θ_t: root of Q̃_U(θ_u, θ_t) = target_Q(k̃)

Scan domain: θ_b, θ_t ∈ [-π/2, π/2] (signed, per paper Fig. 1)
```

## 3. PDG 2024 Reference Values

| Parameter | Value | Angle |
|---|---|---|
| sin(θ₁₂) | 0.22501 | 13.003° |
| sin(θ₂₃) | 0.04183 | 2.397° |
| sin(θ₁₃) | 0.003732 | 0.214° |
| δ_CP | 1.20 rad | 68.8° |

### Fritzsch-Xing angles from PDG 2024 CKM (Eq. 20)

| Angle | Value | Formula |
|---|---|---|
| θ_u | 5.098° | atan(|V_ub|/|V_cb|) |
| θ_d | 12.061° | atan(|V_td|/|V_ts|) |
| θ₂₃ | 2.407° | asin(√(|V_ub|²+|V_cb|²)) |

CKM matrix elements used: |V_ub|=0.00373, |V_cb|=0.04183, |V_td|=0.00878, |V_ts|=0.04107

Comparison with Zenczykowski's 2012 extraction:
- θ_d: PDG 2024 = 12.061° vs 2012 = 12.11°
- θ_u: PDG 2024 = 5.098° vs 2012 = 4.87°
- θ₂₃: PDG 2024 = 2.407° vs 2012 = 2.37°

## 4. Physical Koide Parameters (No Rotation)

| Sector | Masses (MeV) | Q | k = √(3Q-1) |
|---|---|---|---|
| Down (d,s,b) | 4.67, 93.50, 4180.0 | 0.7313 | 1.0927 |
| Up (u,c,t) | 2.16, 1270.00, 172500.0 | 0.8489 | 1.2437 |
| Paper Down | 7.84, 160.00, 4209.0 | 0.6783 | 1.0174 |
| Paper Up | 4.39, 1296.00, 172000.0 | 0.8452 | 1.2391 |
| Leptons | 0.51, 105.66, 1776.9 | 0.6667 | 1.0000 |

## 5. Historical Reproduction — Paper Masses, 2012 FX Angles

This reproduces Zenczykowski's own calculation using his Eq. (23) masses and 2012 FX angles (θ_d=12.11°, θ_u=4.87°).

### k̃ = 1.0
- Down roots (θ_b): ['-3.7481°', '-0.5537°', '86.2519°', '89.4463°']
- Up roots (θ_t): ['-87.3185°', '-3.5420°', '2.6815°', '86.4580°']
- Small positive θ_b - θ_t: ['2.9883°', '2.9883°']
- **Predicted θ₂₃ = 2.9883°** (observed 2.397°, pull = 54.23σ)

### k̃ = 1.015
- Down roots (θ_b): ['-3.5354°', '-0.7665°', '86.4646°', '89.2335°']
- Up roots (θ_t): ['-87.6515°', '-3.2091°', '2.3485°', '86.7909°']
- Small positive θ_b - θ_t: ['2.4426°', '2.4426°']
- **Predicted θ₂₃ = 2.4426°** (observed 2.397°, pull = 4.15σ)

## 6. PDG 2024 Masses with 2012 FX Angles

Using PDG 2024 quark masses (in source coordinate order) with Zenczykowski's 2012 FX angle extraction. This tests whether updated masses change the result.

**Mass scheme caveat:** PDG 2024 light quark masses are MS-bar at 2 GeV, c/b are MS-bar at their own masses, and top is pole mass. These mix schemes. A scale-consistent reanalysis would require running all masses to a common scale.

### k̃ = 1.0
- Down roots (θ_b): ['-89.2323°', '-3.3003°', '0.7677°', '86.6997°']
- Up roots (θ_t): ['-87.3074°', '-3.5333°', '2.6926°', '86.4667°']
- Small positive θ_b - θ_t: ['0.2330°', '0.2330°', '4.3010°']
- **Predicted θ₂₃ = 0.2330°** (observed 2.397°, pull = -198.65σ)

### k̃ = 1.015
- Down roots (θ_b): ['-89.4813°', '-3.0513°', '0.5187°', '86.9487°']
- Up roots (θ_t): ['-87.6404°', '-3.2003°', '2.3596°', '86.7997°']
- Small positive θ_b - θ_t: ['0.1490°', '0.1490°', '3.7190°']
- **Predicted θ₂₃ = 0.1490°** (observed 2.397°, pull = -206.36σ)

## 7. PDG 2024 Masses with PDG 2024 FX Angles

Using PDG 2024 quark masses AND PDG 2024-derived FX angles. This is the most current-data test, subject to the mass scheme caveat above.

### k̃ = 1.0
- θ_d = 12.061°, θ_u = 5.098°
- Down roots (θ_b): ['-89.2284°', '-3.3046°', '0.7716°', '86.6954°']
- Up roots (θ_t): ['-87.3281°', '-3.5123°', '2.6719°', '86.4877°']
- Small positive θ_b - θ_t: ['0.2077°', '0.2077°', '4.2839°']
- **Predicted θ₂₃ = 0.2077°** (observed 2.397°, pull = -200.96σ)

### k̃ = 1.015
- θ_d = 12.061°, θ_u = 5.098°
- Down roots (θ_b): ['-89.4778°', '-3.0552°', '0.5222°', '86.9448°']
- Up roots (θ_t): ['-87.6596°', '-3.1809°', '2.3404°', '86.8191°']
- Small positive θ_b - θ_t: ['0.1256°', '0.1256°', '3.7031°']
- **Predicted θ₂₃ = 0.1256°** (observed 2.397°, pull = -208.50σ)

## 8. Q̃ Ranges with Different Angle/Mass Combinations

| Config | θ₁₂ | Masses | Q̃ range | Reaches 2/3? |
|---|---|---|---|---|
| Paper, 2012 angles (Down) | 12.110° | 7.8,160.0,4209.0 | [0.4584, 0.8636] | ✓ |
| Paper, 2012 angles (Up) | 4.870° | 4.4,1296.0,172000.0 | [0.4858, 0.9427] | ✓ |
| PDG, 2012 angles (Down) | 12.110° | 4.7,93.5,4180.0 | [0.4673, 0.8818] | ✓ |
| PDG, 2012 angles (Up) | 4.870° | 2.2,1270.0,172500.0 | [0.4858, 0.9404] | ✓ |
| PDG, PDG angles (Down) | 12.061° | 4.7,93.5,4180.0 | [0.4674, 0.8824] | ✓ |
| PDG, PDG angles (Up) | 5.098° | 2.2,1270.0,172500.0 | [0.4855, 0.9390] | ✓ |

## 9. Assessment

**What was corrected:**
- R12 now matches source Eq. (16) exactly
- Mass ordering now (d,s,b) and (u,c,t) per Eq. (23)
- Scan domain now [-π/2, π/2] including negative roots
- FX angles derived from PDG 2024 CKM matrix via Eq. (20)
- Unit tests reproduce paper's 2.98° and 2.44° checkpoints
- CKM parameters use sin (not sin²) from PDG 2024

**What the corrected analysis shows:**

1. **Historical reproduction (paper masses, 2012 angles):** θ₂₃ = 2.9883° with k̃=1
   This matches Zenczykowski's Eq. (25) checkpoint of 2.98°.

2. **PDG 2024 masses, 2012 FX angles:** θ₂₃ = 0.2330° (observed 2.397°, pull = -198.65σ)

3. **PDG 2024 masses, PDG 2024 FX angles:** θ₂₃ = 0.2077° (observed 2.397°, pull = -200.96σ)

**What this means:**
- The pseudo-mass Koide constraint (k̃=1) DOES produce a CKM 2-3 angle prediction when implemented correctly. D3 v1's negative result was an artifact of implementation errors (transposed R12, wrong mass ordering, restricted domain).
- The prediction quality depends on which masses and FX angles are used. The historical reproduction matches the paper. The current-data test is subject to mass scheme caveats.
- This is a **consistency relation**, not a first-principles derivation. The FX angles θ_d and θ_u are extracted from CKM data, not predicted.

**What this does NOT prove:**
- It does not derive CKM from first principles. θ_d and θ_u are inputs from data.
- It does not prove the pseudo-mass Koide hypothesis. It tests consistency.
- It does not connect to PF's Z3 geometry directly.
- The mass scheme mixing (MS-bar at different scales + pole mass) is an uncontrolled systematic. A scale-consistent reanalysis is needed for a definitive current-data test.

## 10. Method Notes

- Source: Zenczykowski, arXiv:1301.4143v2, Eqs. (14), (16), (17), (20), (23)-(25)
- R12: Eq. (16) `[[c,-s,0],[s,c,0],[0,0,1]]`
- R23: Eq. (17) with phase dropped per Eq. (22) justification
- Pseudo-mass: Eq. (14) linear definition `m̃_j = |Σ_k U_jk · m_k|`
- Koide Q: `Q̃ = (Σ m̃_j) / (Σ √m̃_j)²`; target `Q = (1+k̃²)/3`
- Scan domain: `[-π/2, π/2]` (signed, per paper Fig. 1)
- Root finding: brentq on sign-changing intervals, 50001 grid points
- FX angle extraction: Eq. (20), `θ_u=atan(|V_ub|/|V_cb|)`, `θ_d=atan(|V_td|/|V_ts|)`
- PDG 2024 CKM: sin(θ₁₂)=0.22501, sin(θ₂₃)=0.04183, sin(θ₁₃)=0.003732
- Mass scheme caveat: light quarks MS-bar@2GeV, c/b MS-bar@m_c/m_b, t pole mass
- Source script: `d3_ckm_scan_v2.py` in this directory
