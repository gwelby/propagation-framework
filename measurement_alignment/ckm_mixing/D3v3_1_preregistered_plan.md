# D3 v3.1 Pre-Registered Analysis Plan

> **Seal:** Generated before any computation. SHA-256 and timestamp recorded below.  
> **Purpose:** Satisfy Codex pre-registration requirement for D3 v3.1 repair.  
> **Prior audit:** `/mnt/d/Codex/REPORTS/CODEX_20260712_D3V3_CKM_BRANCH_CONTINUATION_AUDIT.md`

## What This Plan Declares (Before Running)

### 1. Central Branch Result (Accepted from v3)

Under the submitted source equations (Zenczykowski 2013, arXiv:1301.4143v2), the paper's Eq. (25) branch moves from:
- **Start:** `2.988277°` (paper checkpoint, k=1, paper masses, 2012 FX angles)
- **End:** `4.308496°` (PDG 2024 mixed-scale central values)

This is a **fixed-path sensitivity result**, not a current-data test, not a physical-model verdict, and not a PF prediction. CKM remains SILENT in PF.

### 2. Uncertainty Model (To Be Used in v3.1)

All uncertainties are from **PDG 2024 Eq. (12.28)** directly:

| Parameter | Central | Uncertainty | Type |
|---|---|---|---|
| sin(θ₁₂) | 0.22501 | ±0.00068 | Symmetric |
| sin(θ₂₃) | 0.04183 | +0.00079 / −0.00069 | Asymmetric |
| sin(θ₁₃) | 0.003732 | +0.000090 / −0.000085 | Asymmetric |
| δ_CP | 1.147 | ±0.026 | Symmetric |

Mass uncertainties (1σ from 90% CL by ÷1.645, per Codex D1 v4 reaudit):
- d: 4.70 ± 0.043 MeV
- s: 93.5 ± 0.486 MeV
- b: 4183.0 ± 4.26 MeV
- u: 2.16 ± 0.043 MeV
- c: 1273.0 ± 2.80 MeV
- t: 172500.0 ± 700 MeV

### 3. Branch Rule

The **only** branch considered is the one continuous from the paper's Eq. (25) checkpoint. At each interpolation step, select the root pair with the smallest Euclidean distance to the previous step's pair. No other branches are sampled or weighted. This is a **continuation rule**, not a distribution over branch ambiguity.

### 4. What Will Be Computed

A. **Plus/minus sensitivity envelope:** For each input with asymmetric uncertainty, compute the endpoint at (+σ, −σ) separately, holding other inputs at central values. This produces a non-statistical envelope, not a confidence interval.

B. **Small Monte Carlo sample (optional):** A small number of draws (e.g. 100) using a proper two-sided asymmetric sampler, with the sole purpose of verifying the envelope is not grossly misleading. Results will be labeled as **exploratory sensitivity checks**, not uncertainty propagation.

C. **Exact-value regression tests:** The script will assert that the PDG 2024 central values reproduce the known 4.308496° endpoint and the paper checkpoints.

### 5. What Will NOT Be Claimed

- No sigma-based statistical test.
- No falsification or confirmation of Zenczykowski's model.
- No full uncertainty propagation or root-selection ambiguity propagation.
- No CLAIMS.md, MAP.md, or CKM tier change.
- CKM remains SILENT in PF.

### 6. Pass / Fail Threshold

There is no pass/fail threshold. This is a sensitivity study. The outputs are:
- The central fixed-path endpoint: 4.308496°
- A plus/minus sensitivity envelope around that endpoint
- A note that a statistical test requires scale-consistent masses and CKM covariance

---

**Seal:** SHA-256 `4fffaefa984b4d6325689f1a487926c6b109b5f315de697ac45c32850eb73cfb`  
**Timestamp:** 2026-07-13T04:36:24Z  
**Git hash-object:** `57eafcadf2fb809ac86905227b9c7e22dcf1fc82`

> **Audit addendum (2026-07-13):** This plan is reproducible sensitivity work, **not** externally pre-registered. The SHA-256 and git blob above are the actual values of this plan file on disk. Prior claims of `ac0b...ffa3` and `cddf...e508` did not match the actual file and have been corrected. A future v3.2 pre-registered run must use a plan + source hash in a detached, committed/tagged or otherwise immutable receipt **before** execution.

*Plan recorded before computation; not externally pre-registered.*
