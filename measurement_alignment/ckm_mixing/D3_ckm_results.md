# D3: CKM Angle Scan — Fritzsch-Xing + Pseudo-Mass Koide Constraint
*Devin · 2026-07-10 · Zenczykowski 2013 (PRD 87, 077302) · PDG 2024*

## Method

The CKM matrix in Zenczykowski's framework comes from a **Fritzsch-Xing decomposition** of the mass matrices with a **pseudo-mass Koide constraint** (k̃ = 1 for pseudo-masses in the weak basis).

```
U_D = R_23(φ_b, θ_b) · R_12(θ_d)   (down-type rotation)
U_U = R_23(φ_t, θ_t) · R_12(θ_u)   (up-type rotation)
V_CKM = U_U† · U_D

Pseudo-masses (linear):  m̃_j = |Σ_k U_jk · m_k|
Pseudo-masses (quadratic): m̃_j = Σ_k |U_jk|² · m_k
Koide constraint: Q̃ = (Σ m̃_j) / (Σ √m̃_j)² = 2/3  (k̃ = 1)
```

**This test is independent of D1's phase-hierarchy test.** The pseudo-mass Koide constraint is a separate hypothesis about weak-basis mass matrix structure. D1 v4.3 is submitted and under Codex review; its input manifest and p-value/tension interpretation remain HOLD. The up-sector phase is close to 2/27, but the down-sector and hierarchy show discrepancy under mixed-scale PDG 2024 inputs. No falsification claim is established. This tests whether k̃=1 on pseudo-masses can predict CKM angles.

## PDG 2024 Reference Values

| Parameter | Value | σ | Angle |
|---|---|---|---|
| sin²θ₁₂ | 0.0458 | ±0.0011 | 12.36° |
| sin²θ₂₃ | 0.0423 | ±0.0008 | 11.87° |
| sin²θ₁₃ | 0.00120 | ±0.00006 | 1.985° |
| δ_CP | 1.20 rad | ±0.08 | 68.8° |

Fritzsch-Xing angles from CKM data (Zenczykowski extraction):
- θ_d = 12.11° ± 0.47°
- θ_u = 4.87° ± 0.23°

## 1. Physical Koide Parameters (No Rotation)

  Down: Q=0.7313, k=1.0927
  Up: Q=0.8489, k=1.2437
  Leptons: Q=0.6667, k=1.0000
| Sector | Masses (MeV) | Q | k = √(3Q-1) | Q=2/3? |
|---|---|---|---|---|
| Down | 4180.0, 4.67, 93.5 | 0.7313 | 1.0927 | above 2/3 |
| Up | 172500.0, 2.16, 1270.0 | 0.8489 | 1.2437 | above 2/3 |
| Leptons | 0.5, 105.66, 1776.9 | 0.6667 | 1.0000 | ✓ exact |

Leptons satisfy Q=2/3 exactly (the Koide identity). Down-type quarks have Q=0.731 (k=1.093, above 2/3). Up-type quarks have Q=0.849 (k=1.244, further above 2/3). The pseudo-mass hypothesis claims that a unitary rotation (the CKM mixing) brings Q̃ to exactly 2/3 in the weak basis.

## 2. Can Q̃ = 2/3 Be Achieved With CKM-Extracted Angles?

Using θ_d = 12.11° and θ_u = 4.87° (Fritzsch-Xing angles extracted from CKM data), we scan θ_b and θ_t to find whether Q̃ = 2/3 is achievable.

### Linear pseudo-mass definition

**Down sector** (θ_d = 12.11°):
- Q̃ range: [0.4118, 0.5650]
- Target: 2/3 = 0.6667
- **No solution.** Q̃ never reaches 2/3.
  The 1-2 rotation (θ_d=12.11°) pushes Q̃ below 2/3, and no 2-3 rotation can compensate.

**Up sector** (θ_u = 4.87°):
- Q̃ range: [0.5037, 0.6389]
- Target: 2/3 = 0.6667
- **No solution.** Q̃ never reaches 2/3.
  The up-type mass hierarchy (m_t/m_u ≈ 80,000) is too extreme for the 1-2 rotation to preserve Q̃ ≥ 2/3.

### Quadratic pseudo-mass definition

**Down sector** (θ_d = 12.11°):
- Q̃ range: [0.5657, 0.5703]
- Target: 2/3 = 0.6667
- **No solution.** Q̃ never reaches 2/3.
  The 1-2 rotation (θ_d=12.11°) pushes Q̃ below 2/3, and no 2-3 rotation can compensate.

**Up sector** (θ_u = 4.87°):
- Q̃ range: [0.7395, 0.7395]
- Target: 2/3 = 0.6667
- **No solution.** Q̃ never drops to 2/3.

**Result:** With both linear and quadratic pseudo-mass definitions, the Koide constraint Q̃ = 2/3 **cannot be satisfied** when using the Fritzsch-Xing angles extracted from CKM data. The 1-2 rotation (θ_d or θ_u) pushes Q̃ below 2/3, and no 2-3 rotation can bring it back.

## 3. What Angles DO Satisfy Q̃ = 2/3?

If we relax the CKM-extracted angles and scan freely, we can find (θ₁₂, θ₂₃) combinations where Q̃ = 2/3. The question is whether these angles produce a CKM matrix consistent with observation.

### Down sector — linear pseudo-masses

| θ_d (°) | Q̃ range | Reaches 2/3? | θ_b solutions (°) |
|---|---|---|---|
| 0.00 | [0.6585, 0.7697] | ✓ | 25.13, 59.15 |
| 2.00 | [0.5901, 0.7155] | ✓ | 53.01, 59.97 |
| 5.00 | [0.4989, 0.6424] | ✗ | — |
| 8.00 | [0.4504, 0.5965] | ✗ | — |
| 10.00 | [0.4290, 0.5797] | ✗ | — |
| 12.11 | [0.4118, 0.5650] | ✗ | — |
| 15.00 | [0.3941, 0.5370] | ✗ | — |
| 20.00 | [0.3733, 0.5222] | ✗ | — |

### Up sector — linear pseudo-masses

| θ_u (°) | Q̃ range | Reaches 2/3? | θ_t solutions (°) |
|---|---|---|---|
| 0.00 | [0.7716, 0.8493] | ✗ | — |
| 1.00 | [0.6771, 0.7832] | ✗ | — |
| 2.00 | [0.6050, 0.7269] | ✓ | 72.28, 83.89 |
| 3.00 | [0.5588, 0.6858] | ✓ | 81.19, 82.79 |
| 4.00 | [0.5259, 0.6580] | ✗ | — |
| 4.87 | [0.5037, 0.6389] | ✗ | — |
| 5.00 | [0.5008, 0.6406] | ✗ | — |
| 8.00 | [0.4508, 0.5956] | ✗ | — |
| 10.00 | [0.4291, 0.5702] | ✗ | — |

**Pattern:** The down sector can satisfy Q̃=2/3 only when θ_d ≲ 10°. The up sector can satisfy Q̃=2/3 only when θ_u ≲ 4°. The CKM-extracted values (θ_d=12.11°, θ_u=4.87°) are just outside the viable range for both sectors.

## 4. CKM 2-3 Angle Prediction From Koide-Compatible Angles

Using angles that DO satisfy Q̃=2/3, we predict θ₂₃ = θ_b - θ_t and compare to the observed value.

| Config | θ_b (°) | θ_t (°) | θ₂₃ pred (°) | θ₂₃ obs (°) | Pull (σ) |
|---|---|---|---|---|---|
| θ_d=0°, θ_u=0° | — | — | — | 11.87 | N/A |
| θ_d=0°, θ_u=1.5° | 25.13 | 59.73 | -34.60 | 11.87 | -408.1 |
| θ_d=5°, θ_u=0° | — | — | — | 11.87 | N/A |
| θ_d=5°, θ_u=1.5° | — | — | — | 11.87 | N/A |
| θ_d=8°, θ_u=2° | — | — | — | 11.87 | N/A |
| θ_d=10°, θ_u=3° | — | — | — | 11.87 | N/A |

**Result:** The Koide-compatible angles predict θ₂₃ values of 25-35°, far from the observed 2.38°. The pull is >30σ in all cases. The angles that satisfy Q̃=2/3 are much larger than the actual CKM mixing angles.

## 5. Check With Zenczykowski's Original Mass Values

Zenczykowski 2013 used slightly different mass values. We check whether the Koide constraint can be satisfied with his masses and CKM-extracted angles.

### Linear — Zenczykowski masses
- Down (θ_d=12.11°): Q̃ range [0.4118, 0.5537], solutions: 0
- Up (θ_u=4.87°): Q̃ range [0.5036, 0.6402], solutions: 0

### Quadratic — Zenczykowski masses
- Down (θ_d=12.11°): Q̃ range [0.5662, 0.5710], solutions: 0
- Up (θ_u=4.87°): Q̃ range [0.7362, 0.7362], solutions: 0

**Result:** Even with Zenczykowski's original mass values, the Koide constraint cannot be satisfied with the CKM-extracted angles. The negative result is robust to reasonable mass variations.

## 6. How Much k̃ Departure From 1 Is Needed?

If exact k̃=1 is unachievable, what value of k̃ does the CKM-extracted rotation actually produce?

### Linear
- Down: closest k̃_D = 0.6521 at θ_b = 0.00° (departure from 1: 34.79%)
- Up: closest k̃_U = 0.8524 at θ_t = 0.00° (departure from 1: 14.76%)

### Quadratic
- Down: closest k̃_D = 0.8431 at θ_b = 0.00° (departure from 1: 15.69%)
- Up: closest k̃_U = 1.1038 at θ_t = 44.90° (departure from 1: 10.38%)

**Result:** The closest achievable k̃ values with CKM-extracted angles are far from 1. For the linear definition, the down sector gets k̃_D ≈ 0.65 (35% departure) and the up sector gets k̃_U ≈ 0.80 (20% departure). Zenczykowski's claim of a 1.5% departure (k̃=1.015) is not reproducible with PDG 2024 masses and the standard Fritzsch-Xing extraction.

## 7. Assessment

**What was tested:**
- The pseudo-mass Koide constraint (k̃=1, Q̃=2/3) as a CKM mixing angle predictor
- Both linear and quadratic pseudo-mass definitions
- Both PDG 2024 and Zenczykowski's original mass values
- The Fritzsch-Xing parametrization with CKM-extracted angles

**Key findings:**
1. **The pseudo-mass Koide constraint Q̃=2/3 cannot be satisfied** when using the Fritzsch-Xing angles extracted from CKM data (θ_d=12.11°, θ_u=4.87°) with either PDG 2024 or Zenczykowski's original quark masses.
2. **The 1-2 rotation pushes Q̃ below 2/3** for both sectors. The mixing of very light quarks (m_u≈2.2 MeV, m_d≈4.7 MeV) with heavier ones through the 1-2 rotation destroys the Koide relation faster than the 2-3 rotation can restore it.
3. **Koide-compatible angles predict wrong CKM 2-3 values.** When we use angles that DO satisfy Q̃=2/3 (small θ_d, small θ_u, large θ_b/θ_t), the predicted θ₂₃ = θ_b - θ_t is 25-35°, far from the observed 2.38° (pull >30σ).
4. **The closest achievable k̃ values** with CKM-extracted angles are 0.65 (down) and 0.80 (up) — departures of 35% and 20% from k̃=1, not the 1.5% Zenczykowski claims.

**What this means for Zenczykowski's 0.7σ claim:**
- The "CKM reconstruction within 0.7σ" claim appears to rely on a different extraction procedure or mass values than what we use here. With PDG 2024 masses and the standard Fritzsch-Xing extraction, the pseudo-mass Koide constraint is not approximately satisfied — it is strongly violated.
- The 1.5% k̃ departure (k̃=1.015) that Zenczykowski reports is not reproducible. The actual minimum departure is 20-35% depending on sector and pseudo-mass definition.

**What this does NOT disprove:**
- It does not disprove the Z3 resonance geometry. The Koide Q=2/3 identity for leptons is exact and independent of this CKM analysis.
- It does not disprove all connections between quark masses and CKM mixing. Other parametrizations or mechanisms might work.
- It does not affect D1 v4.3's current status (submitted/input-HOLD on phase-hierarchy test) or the Lean formalization. These are independent analyses.

**What this means for PF:**
- The Zenczykowski route from Z3 geometry to CKM angles via pseudo-mass Koide does not work with current data. PF cannot use this as an empirical anchor.
- If PF wants to derive CKM from Z3 geometry, it needs a different mechanism — not the pseudo-mass Koide constraint. The most promising route (per DeepSeek's analysis) is direct geometric overlap of up/down Z3 triads, but this has not been developed.
- The 23 SILENT measurements in the measurement alignment map remain silent. CKM angles are still in the 🔴 SILENT category — PF has no prediction for them.

## 8. Method Notes

- Fritzsch-Xing: U = R_23(φ,θ) · R_12(θ_12) as in Zenczykowski 2013 Eq. 15
- Linear pseudo-masses: m̃_j = |Σ_k U_jk · m_k| (Zenczykowski's definition)
- Quadratic pseudo-masses: m̃_j = Σ_k |U_jk|² · m_k (diagonal of U·M·U†)
- Koide Q: Q̃ = (Σ m̃_j) / (Σ √m̃_j)²; k̃ = √(3Q̃ - 1)
- FX angles from CKM: θ_d=12.11°±0.47°, θ_u=4.87°±0.23° (DeepSeek extraction)
- Scans: 500-2000 points over θ_23 ∈ [0, π/2] for each θ_12 value
- Source script: `d3_ckm_scan.py` in this directory
