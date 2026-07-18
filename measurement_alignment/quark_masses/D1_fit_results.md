# D1 v3: Quark Koide Formula — Full Parameter Fit & Predictive Power
*Devin · 2026-07-10 · Zenczykowski 2013 (PRD 87, 077302) · PDG 2024 masses*

## Formula & Conventions

We use Zenczykowski's published Eq. (4):

```
m_j = M · (1 + √2 · k · cos(2πj/3 + δ))
```

with generation ordering `j = 0, 1, 2` mapping to heaviest, lightest, middle.
Koide Q in this convention is `Q = (1 + k²)/3`, so `k = 1` gives `Q = 2/3` exactly.

## Input Masses (PDG 2024)

| Sector | Quark | j | Mass (MeV) | σ (MeV) |
|---|---|---|---|---|
| up | u | 1 | 2.16 | 0.49 |
| up | c | 2 | 1270 | 20 |
| up | t | 0 | 172500 | 700 |
| down | d | 1 | 4.67 | 0.48 |
| down | s | 2 | 93.5 | 0.8 |
| down | b | 0 | 4180 | 20 |

## 1. Free-δ Fit (3 parameters, 3 masses)

A 3-parameter model fit to 3 masses has zero degrees of freedom and will reproduce the input exactly if a real solution exists. The interesting output is the best-fit parameters and their uncertainty.

### Up-type

| Quark | j | PDG (MeV) | Fit (MeV) | Residual |
|---|---|---|---|---|
| top | 0 | 172500.000 | 172500.000 | 0 |
| up | 1 | 2.160 | 2.160 | 6.74e-10 |
| charm | 2 | 1270.000 | 1270.000 | -6.83e-10 |

- **M** = 57924.053 ± 234.885 MeV
- **k** = 1.398712 ± 0.000250
- **δ** = 0.006389 ± 0.000105 rad (0.3660°)
- **Q = (1+k²)/3** = 0.985465

### Down-type

| Quark | j | PDG (MeV) | Fit (MeV) | Residual |
|---|---|---|---|---|
| bottom | 0 | 4180.000 | 4180.000 | 0 |
| down | 1 | 4.670 | 4.670 | -1.96e-11 |
| strange | 2 | 93.500 | 93.500 | 2.17e-11 |

- **M** = 1426.057 ± 6.656 MeV
- **k** = 1.365773 ± 0.000503
- **δ** = 0.018621 ± 0.000216 rad (1.0669°)
- **Q = (1+k²)/3** = 0.955112

### δ_U : δ_D Ratio Test

- δ_U = 0.006389 ± 0.000105 rad
- δ_D = 0.018621 ± 0.000216 rad
- Observed δ_D / δ_U = 2.915 ± 0.059
- Zenczykowski prediction (1:2 phase hierarchy): δ_D / δ_U = 2.000
- Pull from 1:2 prediction: **19.41σ**

## 2. Fixed-δ Fit (Zenczykowski's δ = 2/27 for up, 4/27 for down)

This is the actual claim: Zenczykowski asserts the phase hierarchy is exact, with δ_U = 2/27 and δ_D = 4/27. With δ fixed, the model has 2 free parameters (M, k) and 1 degree of freedom.

### Up-type, δ = 0.074074 rad (4.2441°)

| Quark | j | PDG (MeV) | Pred (MeV) | σ (MeV) | Pull |
|---|---|---|---|---|---|
| top | 0 | 172500.000 | 32381.234 | 700.000 | 200.17 |
| up | 1 | 2.160 | 1.393 | 0.490 | 1.57 |
| charm | 2 | 1270.000 | 2662.031 | 20.000 | -69.60 |

- M = 11681.553 MeV, k = 1.256437
- χ² = 44914.724 (dof = 1)
- p-value = 0.000e+00

### Down-type, δ = 0.148148 rad (8.4883°)

| Quark | j | PDG (MeV) | Pred (MeV) | σ (MeV) | Pull |
|---|---|---|---|---|---|
| bottom | 0 | 4180.000 | 831.614 | 20.000 | 167.42 |
| down | 1 | 4.670 | -5.557 | 0.480 | 21.31 |
| strange | 2 | 93.500 | 127.267 | 0.800 | -42.21 |

- M = 317.774 MeV, k = 1.156051
- χ² = 30264.795 (dof = 1)
- p-value = 0.000e+00

## 3. Cross-Sector Predictive Test (1:2 Phase Hierarchy)

The only genuinely predictive claim in the Zenczykowski framework is the phase hierarchy: δ_D = 2δ_U. If true, the up-type masses (3 free parameters) predict the down-type masses after fixing δ_D, leaving only M and k free for the down sector. This test has 1 degree of freedom for the down-type prediction. The reverse prediction (down → up) also has 1 degree of freedom.

### Up-type δ predicts Down-type masses

- Predictor δ_u = 0.006389 rad
- Predicted δ_d = 0.012777 rad (by 1:2 hierarchy)
- Free-fit δ_d = 0.018621 rad
| Quark | j | PDG (MeV) | Predicted (MeV) | σ (MeV) | Pull |
|---|---|---|---|---|---|
| bottom | 0 | 4180.000 | 4350.764 | 20.000 | -8.54 |
| down | 1 | 4.670 | 11.287 | 0.480 | -13.79 |
| strange | 2 | 93.500 | 74.846 | 0.800 | 23.32 |

- M = 1478.966 MeV, k = 1.373145
- χ² = 806.682 (dof = 1)
- p-value = 0.000e+00

### Down-type δ predicts Up-type masses

- Predictor δ_d = 0.018621 rad
- Predicted δ_u = 0.009310 rad (by 1:2 hierarchy)
- Free-fit δ_u = 0.006389 rad
| Quark | j | PDG (MeV) | Predicted (MeV) | σ (MeV) | Pull |
|---|---|---|---|---|---|
| top | 0 | 172500.000 | 165876.511 | 700.000 | 9.46 |
| up | 1 | 2.160 | 1.860 | 0.490 | 0.61 |
| charm | 2 | 1270.000 | 1775.631 | 20.000 | -25.28 |

- M = 55884.667 MeV, k = 1.391783
- χ² = 729.063 (dof = 1)
- p-value = 0.000e+00

## 4. Pole Distance & Fine-Tuning

The lightest quark sits near the zero of the cosine term. The closer it is to the pole `1 + √2·k·cos = 0`, the more fine-tuned the parameters are.

### Up-type
- cos(2π/3 + δ) = -0.505522
- Pole location cos_pole = -1/(√2·k) = -0.505541
- Distance to pole: 1.885174e-05
- Lightest mass: 2.160 MeV

### Down-type
- cos(2π/3 + δ) = -0.516038
- Pole location cos_pole = -1/(√2·k) = -0.517734
- Distance to pole: 1.695456e-03
- Lightest mass: 4.670 MeV

## 5. Assessment

**What the fit proves:**
- The Zenczykowski formula with 3 free parameters (M, k, δ) can exactly reproduce any three positive quark masses that satisfy the geometric positivity constraint. This is expected algebra, not a physical prediction.
- With δ fixed at Zenczykowski's claimed values (2/27 for up, 4/27 for down), the formula is **strongly ruled out** by PDG 2024 masses. The up-type fit predicts top = 32.4 GeV (actual 172.5 GeV, pull 200σ) and charm = 2.66 GeV (actual 1.27 GeV, pull −70σ). The down-type fit predicts bottom = 832 MeV (actual 4.18 GeV, pull 167σ), strange = 127 MeV (actual 93.5 MeV, pull −42σ), and **down = −5.6 MeV** (negative, unphysical).
- The cross-sector prediction test is also ruled out: using the 1:2 hierarchy to predict down-type masses from up-type masses gives χ² = 806.7 (dof = 1, p ≈ 0); the reverse gives χ² = 729.1 (dof = 1, p ≈ 0).

**What the fit does NOT prove:**
- It does not prove that the Z3 resonance geometry is wrong. It shows that the specific phase values δ_U=2/27, δ_D=4/27 are inconsistent with data.
- It does not prove the alternative best-fit δ values are meaningful; 3 parameters fitting 3 data points is a reparameterization, not a derivation.

**The key falsifiable claim:**
- Zenczykowski predicts δ_U : δ_D = 1 : 2. The data give δ_D/δ_U = 2.915 ± 0.059, a **19.4σ** deviation. The 1:2 phase hierarchy is therefore falsified by PDG 2024 quark masses at the level of the parameter values themselves.

**Next step for PF:**
- If PF wants to derive quark masses from Z3 geometry, it must derive δ and k from first principles (e.g., gauge couplings, color factors, coherence ceiling) rather than adopt Zenczykowski's empirical phase hierarchy. The current result removes that empirical anchor.

## 6. Method Notes

- Free-δ parameters solved analytically from the three mass equations; the solution is unique for the assumed heaviest/lightest/middle ordering.
- Parameter uncertainties estimated by Monte Carlo: 20,000 samples perturbing each PDG mass within its quoted σ.
- Fixed-δ fits use Nelder-Mead minimization of χ² with respect to M and k.
- Source script: `d1_fit_v3.py` in this directory.
