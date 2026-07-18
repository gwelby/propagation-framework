# PF Framework Premise Ledger

> **Purpose:** Cross-cutting ledger of framework-level premise gaps, dimensional problems, and unresolved scaffolding that blocks downstream predictions. This is distinct from the Lean hypothesis ledger (`lean/PREMISE_LEDGER.md`), which tracks formalized axioms H1–H21.
>
> **Scope:** Physics-modeling premises that are not yet derived from Axioms 1–3, the PF Lagrangian, or canonical definitions. Each entry states the gap, why it matters, and what work it blocks.
>
> **Last updated:** 2026-07-11

---

## Entry 001 — Lepton g-2 is not dimensionally closed

**Discovered:** 2026-07-11 (Devin D2 tau g-2 task, Claude review)

**Gap:** The PF formula for the tau anomalous magnetic moment,

```
δa_τ = w_max / (m_τ / λ_c · (ħc)⁻¹)
```

is not dimensionally closed. An anomalous magnetic moment `a = (g-2)/2` is dimensionless. In natural units λ_c ~ 1/m_t, so:

- **Literal reading:** `δa_τ ~ w_max / (m_τ · m_t)` has dimensions **mass⁻²**.
- **Ceiling-mass reading:** `δa_τ ~ w_max / m_t` has dimensions **mass⁻¹**.

Neither yields a dimensionless number. The reported values 6.6 × 10⁻⁹ and 1.17 × 10⁻⁵ are unit-stripped numerics, not predictions. The factor-of-m_τ ambiguity between them is a symptom of the dimensional gap, not a choice between valid interpretations.

**Why it matters:** Lepton g-2 is one of PF's flagship falsification tests (Belle II). A test must start from a dimensionally closed prediction. Without that, the framework cannot claim to predict `a_τ`, `a_μ`, or `a_e`.

**Blocked downstream work:**
- TASK-049 (tau g-2): blocked — non-prediction.
- TASK-051 (muon g-2): should not start — same undefined formula.
- TASK-052 (electron g-2): should not start — same undefined formula.

**What would close it:** A field-theoretic derivation of how the coherence ceiling / PF medium contributes to the lepton magnetic moment, including the correct compensating factors of `ħ` and `c` (or a dimensionless coupling) that make `δa_ℓ` dimensionless.

**Evidence:**
- `/mnt/d/Fundamentals/measurement_alignment/g2_anomalous/D2_tau_g2_prediction.md`
- `/mnt/d/Fundamentals/measurement_alignment/g2_anomalous/d2_tau_g2.py`
- `/mnt/d/Fundamentals/definitions/coherence.md` — "coherence ceiling" listed as OPEN
- `/mnt/d/Fundamentals/derivations/lambda_c_from_axioms.md` — λ_c calibrated to top mass, not derived from axioms

---

## Entry 002 — CKM mixing angles remain 🔴 SILENT in PF

**Discovered:** 2026-07-11 (Devin D3 CKM angle scan; Codex audit 2026-07-11)

**Gap:** PF has no first-principles derivation of the CKM mixing angles or the CP phase. The N=3 → CP-violation bridge (ARGUED 0.70) only shows that CP violation is structurally possible with three generations; it does not predict the phase magnitude δ ≈ 1.2 rad or the angle hierarchy θ₁₃ << θ₂₃ << θ₁₂.

**Why it matters:** CKM is a central test of flavor physics. An external preprint (Zenczykowski 2013) claimed 0.7σ reconstruction from a pseudo-mass Koide constraint. Devin's D3 v2 reproduced the paper's historical checkpoints, but Codex 2026-07-11 rejected the claim that the model is falsified on PDG 2024 data. The v2 code selected newly-positive root differences rather than following the paper's branch rule, used a non-PDG CP phase and a too-small CKM uncertainty, and mixed mass renormalization scales. The accepted result is a qualitative sensitivity observation: the model output is highly dependent on mass inputs, especially `m_s`.

**Blocked downstream work:**
- TASK-050 (CKM angle scan): D3 v2 source conventions pass, but current-data falsification conclusions are rejected. D3 v3 must pre-register a root-selection rule, use a consistent PDG CKM representation/covariance, use a common-scale mass set, and propagate all uncertainties before any sigma language.

**What would close it:** A PF derivation of V-A structure and flavor mixing from the Z₃/mode-conversion framework, or a scale-consistent, branch-respecting phenomenological ansatz that survives current data.

**Evidence:**
- `/mnt/d/Fundamentals/measurement_alignment/ckm_mixing/D3v2_ckm_results.md`
- `/mnt/d/Fundamentals/measurement_alignment/ckm_mixing/d3_ckm_scan_v2.py`
- `/mnt/d/Codex/REPORTS/CODEX_20260710_D3_CKM_PSEUDOMASS_AUDIT.md`
- `/mnt/d/Codex/REPORTS/CODEX_20260711_D3V2_CKM_PSEUDOMASS_AUDIT.md`
- `/mnt/d/Codex/inbox/2026-07-11_devin-d3v2-ckm-angle-scan-audit.md`
- `/mnt/d/Devin/inbox/2026-07-11-codex-d3v2-conditional-pass-v3-requirements.md`

---

## Entry 003 — Alpha impedance relation is not an independent PF derivation

**Discovered:** 2026-07-12 (Claude askability audit; Codex hostile replay)

**Gap:**

```text
alpha = Z0 / (2 R_K)
```

is an exact dependent relationship under the standard electromagnetic and quantum-Hall identities:

```text
Z0 = mu0 c
R_K = h/e^2
mu0 = 2 alpha h/(c e^2)
```

The current PF material gives an interpretation of the ratio, but does not independently derive `Z0`, `R_K`, or their ratio from Axioms 1-3. Measuring the relation therefore cannot distinguish PF from established electrodynamics.

**Why it matters:** A true identity can explain what kind of quantity alpha is without providing a numerical PF prediction. Calling the identity a graded empirical confirmation would turn a dependent equation into evidence for the framework.

**Blocked downstream work:**
- Any numerical alpha derivation or confidence increase based only on restating `Z0/(2 R_K)`.
- Any measurement proposal whose only decision rule is whether the two sides of this dependent relation agree.

**What would close it:** A PF-native, non-circular derivation of `Z0`, `R_K`, or their ratio without importing alpha, e, the measured electron mass, or a target-selected equivalent.

**Evidence:**
- `derivations/alpha_from_pf.md:188-207, 385-430`
- [BIPM Appendix 2](https://www.bipm.org/documents/20126/41489676/SI-App2-ampere.pdf) (relations among `mu0`, `Z0`, `R_K`, and alpha in modern SI)
- `/mnt/d/Codex/REPORTS/CODEX_20260712_FUNDAMENTALS_ASKABILITY_AUDIT.md`

---

## Entry 004 — Lambda-c target is calibrated and its boundary inputs remain argued

**Discovered:** 2026-07-12 (Claude askability audit; Codex hostile replay)

**Gap:** PF currently identifies its matter coherence length `lambda_c` with the top-quark Compton wavelength. The local D2 evidence explicitly calls that identification calibrated/empirical, not derived from Axioms 1-3. The displayed scale formula also depends on an argued Planck-boundary coupling, `N^(D/2)` bridge, and interpretation of the `sqrt(2)` factor.

**Why it matters:** The top mass is independently measured, but PF has not independently shown that its coherence scale is the corresponding Compton wavelength. A percentage difference between the formula and that calibrated label is retrospective internal alignment, not a forward PF prediction.

**Blocked downstream work:**
- Promotion of the current `lambda_c` percentage agreement as independently predictive evidence.
- Downstream numerical claims that treat the top-Compton identification as PF-derived rather than as an admitted empirical input.

**What would close it:** Derive the coherence functional and its physical mapping from Axioms 1-3, independently fix the Planck-boundary inputs, then preregister a comparison to a measured observable not reused to set the scale.

**Evidence:**
- `measurement_alignment/g2_anomalous/D2_tau_g2_prediction.md:49-55, 132-148`
- `derivations/lambda_c_from_axioms.md:42-57, 93-141`
- `CLAIMS.md:61`
- `/mnt/d/Codex/REPORTS/CODEX_20260712_FUNDAMENTALS_ASKABILITY_AUDIT.md`

---

*This ledger is append-only. When a premise gap is closed, add a closure entry with evidence rather than deleting the original entry.*
