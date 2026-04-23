# T-021 RG Audit for the Koide/Weinberg Crossing

**Date**: 2026-04-13  
**Status**: `NO-GO / convention audit complete`  
**Scope**: bounded Standard Model convention check first; PF interpretation second  
**Companion helper**: `sandbox/weinberg_rg_crossing_check.py`

**Primary sources used for conventions and external inputs**

1. PDG 2025 gauge-boson listings: `M_W = 80.3692 +- 0.0133 GeV`, `M_Z = 91.1880 +- 0.0020 GeV`  
   https://pdg.lbl.gov/2025/tables/rpp2025-sum-gauge-higgs-bosons.pdf
2. PDG 2025 electroweak review, Table 10.5: `sin^2(theta_eff^ell) = 0.23154 +- 0.00006`, `s_hat_Z^2 = 0.23122 +- 0.00006`  
   https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf
3. Standard Model gauge beta-functions used in the helper's one-loop running check: A. V. Bednyakov, A. F. Pikelner, V. N. Velizhanin, *JHEP* **01** (2013) 017  
   https://doi.org/10.1007/JHEP01(2013)017

---

## 1. Exact claim under audit

The repo had been using a generic sentence of the form:

> RG: `sin^2(theta_W)` runs to `delta` at `mu ~= 98 GeV`.

That sentence is too loose to be defensible without a convention audit, because three different quantities were being collapsed into one label:

1. the direct on-shell pole-mass ratio `1 - M_W^2 / M_Z^2`,
2. the running `MS-bar` weak angle `s_hat^2(mu)`,
3. the effective leptonic angle `sin^2(theta_eff^ell)` extracted from Z-pole asymmetries.

The bounded T-021 question is therefore:

**Does any legitimate Standard Model definition of the weak mixing angle cross `delta ~= 2/9`, and specifically does any audited convention support the sentence `mu ~= 98 GeV`?**

The internal PF value

`sin^2(theta_W)_PF = 0.223101322300866`

is included for comparison only. It is not itself a Standard Model RG definition.

---

## 2. Standard Model convention audit and crossing calculation

### 2.1 Definitions that must be kept separate

| Quantity | Meaning | Value used here | Can run with `mu`? |
|---|---|---:|---|
| `delta_target` | Rational target | `2/9 = 0.222222222222` | no |
| `delta_exact` | Koide phase anchor from repo scan | `0.222229631490` | no |
| `sin^2(theta_W)_PF` | Repo Casimir value | `0.223101322300866` | no |
| `1 - M_W^2 / M_Z^2` | direct pole-mass on-shell ratio | `0.223209492843` using current PDG 2025 pole masses | no |
| `sin^2(theta_eff^ell)` | effective leptonic angle | `0.23154 +- 0.00006` | no, not as a generic RG trajectory |
| `s_hat_Z^2` | `MS-bar` weak angle at `M_Z` | `0.23122 +- 0.00006` | yes |

Two immediate consequences already narrow the claim sharply:

1. `1 - M_W^2 / M_Z^2` is a fixed pole-mass ratio. Calling it "RG running" is a category error.
2. `sin^2(theta_eff^ell)` is a Z-pole extracted observable. It is also not the thing that "runs to 98 GeV."

The only legitimate running convention in this audit is therefore `s_hat^2(mu)` in the `MS-bar` scheme.

### 2.2 Direct pole-mass comparison

Using the current PDG 2025 particle listings:

- `M_W = 80.3692 GeV`
- `M_Z = 91.1880 GeV`

gives

`sin^2(theta_W)^os, direct = 1 - M_W^2 / M_Z^2 = 0.223209492843`.

This is close to the repo Casimir value `0.223101322301`, but it does not run.

For continuity with older repo files, if one keeps the older anchor `M_Z = 91.1876 GeV`, the same fixed ratio becomes

`1 - M_W^2 / M_Z^2 = 0.223202677950`.

That numerical shift is only `6.8e-06`, and it does not change the verdict below.

### 2.3 Running `MS-bar` angle

The PDG electroweak review gives

- `s_hat_Z^2 = 0.23122 +- 0.00006`,
- `sin^2(theta_eff^ell) = 0.23154 +- 0.00006`,
- `alpha_hat^(5)(M_Z)^-1 = 127.930 +- 0.008`.

Using the standard one-loop SM gauge running above `M_Z` with the conventional coefficients

- `b1 = 41/10`,
- `b2 = -19/6`,

the helper script evaluates the `MS-bar` angle as follows:

| `mu` | `s_hat^2(mu)` | relative to `2/9` |
|---:|---:|---|
| `M_W = 80.3692 GeV` | `0.230589619` | above `2/9` |
| `M_Z = 91.1880 GeV` | `0.231220000` | above `2/9` |
| `98 GeV` | `0.231579930` | above `2/9` by `9.36e-03` |
| `100 GeV` | `0.231680904` | above `2/9` |
| `172.61 GeV` | `0.234416236` | above `2/9` |
| `1 TeV` | `0.243312660` | above `2/9` |
| `10 TeV` | `0.255194114` | above `2/9` |

The same helper gives

`d s_hat^2 / d ln(mu) at 98 GeV = +0.004997604`,

so the running direction above `M_Z` is upward, not toward `2/9`.

The PDG review also states that the scale dependence of `s_hat^2(mu)` reaches its minimum near `mu = M_W`, below which one switches to an effective-field-theory treatment with thresholds. That matters because the one-loop helper already gives

`s_hat^2(M_W) = 0.230589619 > 2/9`.

So the standard `MS-bar` trajectory is already above `2/9` at its electroweak minimum in this bounded pass.

### 2.4 Sensitivity to current PDG inputs

Varying `s_hat_Z^2` and `alpha_hat^(5)(M_Z)^-1` across the PDG quoted `1 sigma` corners gives

- `s_hat^2(98 GeV) in [0.231519888, 0.231639972]`,
- `s_hat^2(172.61 GeV) in [0.234355860, 0.234476611]`,
- `s_hat^2(1 TeV) in [0.243251233, 0.243374087]`.

These variations are tiny compared with the gap to `2/9`.

### 2.5 Standard Model verdict

The sentence

> `sin^2(theta_W)` runs to `delta` at `mu ~= 98 GeV`

does **not** survive the convention audit.

What survives is narrower:

1. the direct on-shell pole-mass ratio is a fixed quantity, not RG flow;
2. the effective leptonic angle is a Z-pole observable, not a generic running definition;
3. the standard `MS-bar` running angle `s_hat^2(mu)` stays well above `2/9` in the electroweak region audited here and is already above `2/9` at its electroweak minimum.

Therefore **no legitimate Standard Model definition audited in this pass supports a crossing at `mu ~= 98 GeV`.**

---

## 3. PF interpretation: what survives, what fails, and what remains open

### What survives

The empirical cluster is still real:

- `delta_exact = 0.222229631490`,
- `2/9 = 0.222222222222`,
- `sin^2(theta_W)_PF = 0.223101322301`,
- direct pole-mass on-shell ratio `= 0.223209492843`.

Those numbers are close. That remains a legitimate empirical observation.

### What fails

Two proposed upgrade routes are now honest negatives:

1. **T-022 Casimir selector**: the Casimir polynomial sector did not produce `2/9` as a natural fixed point. The only near-hit was the already-known Weinberg pair itself.
2. **T-021 RG rescue**: no audited Standard Model convention supports the generic repo sentence that `sin^2(theta_W)` runs to `delta` at `mu ~= 98 GeV`.

This means the shared-origin story is **not** currently supported by either the Casimir algebra scan or the Standard Model RG check.

### What remains open

The live question is now narrower and more honest:

**Can PF produce a selector for `delta = 2/9` by some mechanism other than the already-tested Casimir polynomial scan and the now-rejected generic RG-crossing sentence?**

Possible remaining directions are:

- a genuinely PF-native selector outside the present Casimir polynomial sector,
- a convention-specific electroweak statement with explicit source-backed definitions,
- or an honest demotion of the shared-origin thesis if no selector appears.

**Allowed repo conclusion after T-021**: Koide phase remains `EMPIRICAL`; the empirical anchor survives, but the `mu ~= 98 GeV` RG claim does not.
