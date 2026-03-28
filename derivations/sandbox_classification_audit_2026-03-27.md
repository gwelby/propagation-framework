# Sandbox Classification Audit — 2026-03-27

**Audit ID**: HA-20260327-004  
**Auditor**: Codex  
**Scope**: `/mnt/d/fundamentals/sandbox/`  
**Purpose**: classify sandbox artifacts by evidentiary role so the repo stops blurring regressions, empirical signals, toy models, stress tests, calculators, and illustrations.

---

## 1. Audit Method

- Read the live sandbox board: [sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md)
- Sampled high-impact scripts directly:
  - [casimir_verification.py](/mnt/d/fundamentals/sandbox/casimir_verification.py)
  - [propagation.py](/mnt/d/fundamentals/sandbox/propagation.py)
  - [z3_coupling_scan.py](/mnt/d/fundamentals/sandbox/z3_coupling_scan.py)
  - [refractive_gravity_quantitative.py](/mnt/d/fundamentals/sandbox/refractive_gravity_quantitative.py)
  - [perihelion_precession_simple.py](/mnt/d/fundamentals/sandbox/perihelion_precession_simple.py)
  - [shapiro_delay.py](/mnt/d/fundamentals/sandbox/shapiro_delay.py)
  - [alpha_casimir_hunt.py](/mnt/d/fundamentals/sandbox/alpha_casimir_hunt.py)
  - [z3_extended_lagrangian.py](/mnt/d/fundamentals/sandbox/z3_extended_lagrangian.py)
  - [ibm_quantum_h_prod_test.py](/mnt/d/fundamentals/sandbox/ibm_quantum_h_prod_test.py)
  - [ibm_quantum_result_audit.py](/mnt/d/fundamentals/sandbox/ibm_quantum_result_audit.py)
  - [top_tau_coupling_explorer.py](/mnt/d/fundamentals/sandbox/top_tau_coupling_explorer.py)
  - [koide_verify_pdg2024.py](/mnt/d/fundamentals/sandbox/koide_verify_pdg2024.py)
- Attempted WARP ingest first per workspace rule; it failed because WARP memory is offline in this environment.

---

## 2. Classification Rules

### A. Regression / Verification
Checks that a specified model reproduces a known target. Strong evidence for implementation correctness, but not a derivation by itself.

### B. Empirical Signal / Lead
Finds a nontrivial numerical pattern in data or constants. Worth follow-up, but does not by itself explain the mechanism.

### C. Stress Test / No-Go
Attempts to break a proposed bridge or distinguish two candidate mechanisms. High hostile-audit value.

### D. Toy-Model Support
Shows a mechanism inside a simplified model. Useful for plausibility and target-sharpening, but not theorem closure.

### E. Calculator / Illustration
Evaluates assumed formulas or visualizes them. Useful pedagogy; low evidentiary weight.

---

## 3. Core Verdict

The sandbox is valuable, but mixed.

What is strong:
- it contains real **stress tests** and **no-go probes** on the God Equation front
- it contains real **regression checks** on gravity-as-refraction
- it contains real **empirical leads** worth explaining

What is risky:
- some scripts are still easy to misread as theorem closures when they are only calculators or toy models
- the sandbox has duplicate summary surfaces (`/sandbox/sandbox_results.md` and root `/sandbox_results.md`), which invites drift
- several older script docstrings still speak in pre-audit language

So the sandbox is now good enough to support the framework, but not yet clean enough to act as a truth source without human interpretation.

---

## 4. High-Impact Classification Table

| Artifact | Class | Honest use |
|---------|-------|------------|
| [refractive_gravity_quantitative.py](/mnt/d/fundamentals/sandbox/refractive_gravity_quantitative.py) | **A. Regression / Verification** | Checks that the chosen refractive/geodesic model reproduces light deflection. Strong model verification, not axiomatic derivation. |
| [perihelion_precession_simple.py](/mnt/d/fundamentals/sandbox/perihelion_precession_simple.py) | **A. Regression / Verification** | Verifies the chosen refractive model reproduces the GR weak-field precession formula. |
| [shapiro_delay.py](/mnt/d/fundamentals/sandbox/shapiro_delay.py) | **A. Regression / Verification** | Verifies Shapiro delay in the refractive picture once the refractive law is assumed. |
| [z3_coupling_scan.py](/mnt/d/fundamentals/sandbox/z3_coupling_scan.py) | **C. Stress Test / No-Go** | Exactly the right style of executable hostile audit for the God Equation bridge. |
| [chiral_vs_symmetric_entropy.py](/mnt/d/fundamentals/sandbox/chiral_vs_symmetric_entropy.py) | **C. Stress Test / No-Go** | Sharp executable comparison of chirality versus mixing. Illustrates the Gap B no-go cleanly. |
| [ibm_quantum_h_prod_test.py](/mnt/d/fundamentals/sandbox/ibm_quantum_h_prod_test.py) | **C. Stress Test / Hardware no-go tool** | Honest after cleanup: hardware comparison tool, not proof. |
| [ibm_quantum_result_audit.py](/mnt/d/fundamentals/sandbox/ibm_quantum_result_audit.py) | **C. Audit Tool** | Post-run classifier for IBM results. Useful infrastructure, not evidence by itself. |
| [top_tau_coupling_explorer.py](/mnt/d/fundamentals/sandbox/top_tau_coupling_explorer.py) | **B. Empirical Signal / Lead** | Strong anomaly scan with significance estimates. Still a lead until a mechanism closes. |
| [alpha_casimir_hunt.py](/mnt/d/fundamentals/sandbox/alpha_casimir_hunt.py) | **B. Empirical Signal / Lead** | Pattern hunt across algebraic combinations. Can motivate a target; cannot close a derivation. |
| [koide_verify_pdg2024.py](/mnt/d/fundamentals/sandbox/koide_verify_pdg2024.py) | **B. Empirical Verification** | Confirms Koide numerically from masses. Good factual anchor; not explanatory. |
| [analyze_real_eeg.py](/mnt/d/fundamentals/sandbox/analyze_real_eeg.py) / [eeg_csd_analysis.py](/mnt/d/fundamentals/sandbox/eeg_csd_analysis.py) | **B. Empirical Signal / Lead** | Potentially high value because they engage real data. Need consistent reporting. |
| [z3_extended_lagrangian.py](/mnt/d/fundamentals/sandbox/z3_extended_lagrangian.py) | **D. Toy-Model Support** | Useful toy confirmation of orbit-averaged isotropy structure. Does not close R3 for the full PF. |
| [casimir_verification.py](/mnt/d/fundamentals/sandbox/casimir_verification.py) | **E. Calculator / Illustration** | Numerically evaluates assumed formulas. Not evidence for derivation status. |
| [propagation.py](/mnt/d/fundamentals/sandbox/propagation.py) | **E. Calculator / Demo API** | Encodes current formulas and status claims. Useful as demo surface; dangerous if mistaken for evidence. |

---

## 5. Findings

### Finding 1
[z3_coupling_scan.py](/mnt/d/fundamentals/sandbox/z3_coupling_scan.py) is the current sandbox gold standard.

Why:
- it names the open theorem questions explicitly
- it tries to break them
- it distinguishes equal marginals, `H_prod`, regularity, and isotropy instead of collapsing them

This is the model future theory-sandbox work should follow.

### Finding 2
[propagation.py](/mnt/d/fundamentals/sandbox/propagation.py) is a calculator/demo surface, not an evidentiary artifact.

Why:
- it returns headline quantities directly
- it still prints language like “Derived” in a presentation layer
- it does not test or falsify anything

This file is useful, but it should never be cited as support for claim upgrades.

### Finding 3
The gravity-as-refraction scripts are strong **regression** artifacts, not derivations.

This matters because they are still among the best sandbox assets in the repo, but their honest role is:
- once the refractive model is specified, these scripts show it reproduces key GR tests
- they do not by themselves prove “forces are refraction” from the axioms alone

### Finding 4
[z3_extended_lagrangian.py](/mnt/d/fundamentals/sandbox/z3_extended_lagrangian.py) should be cited as toy-model support only.

The script itself says “toy model” in the header. The strongest honest statement is:
- it demonstrates orbit-averaged Fisher isotropy in a Gaussian `C3` toy model
- it does not close the full PF coupling/isotropy theorem

### Finding 5
Empirical pattern hunters are present and useful, but they need guardrails.

The following should stay in the repo:
- [alpha_casimir_hunt.py](/mnt/d/fundamentals/sandbox/alpha_casimir_hunt.py)
- [top_tau_coupling_explorer.py](/mnt/d/fundamentals/sandbox/top_tau_coupling_explorer.py)
- [koide_phase_scan.py](/mnt/d/fundamentals/sandbox/koide_phase_scan.py)

But they should always be read as:
- pattern discovery / anomaly ranking
- not theorem closure

---

## 6. Changes Recommended

### Immediate
1. Keep [sandbox/sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md) as the canonical sandbox truth log.
2. Add classification labels to new sandbox entries by default.
3. Do not let calculator/demo scripts print claim-grade words like `DERIVED` without a visible audit warning.

### Near-term cleanup
1. Relabel [propagation.py](/mnt/d/fundamentals/sandbox/propagation.py) as demo/API and strip evidentiary language from its console output.
2. Add a short class banner to older high-impact scripts:
   - regression
   - empirical lead
   - toy model
   - stress test
3. Consolidate or clearly separate the root [sandbox_results.md](/mnt/d/fundamentals/sandbox_results.md) from [sandbox/sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md).

### Structural
1. Future sandbox scripts should declare one of the five classes in the docstring.
2. Claim upgrades should require:
   - a derivation/audit source
   - plus sandbox evidence when relevant
   - never sandbox evidence alone

---

## 7. Final Status

The sandbox is now strong enough to support honest hostile audit, but only if its artifacts are classified correctly.

My current ranking:
- **Best evidence scripts**: [z3_coupling_scan.py](/mnt/d/fundamentals/sandbox/z3_coupling_scan.py), [refractive_gravity_quantitative.py](/mnt/d/fundamentals/sandbox/refractive_gravity_quantitative.py), [perihelion_precession_simple.py](/mnt/d/fundamentals/sandbox/perihelion_precession_simple.py), [shapiro_delay.py](/mnt/d/fundamentals/sandbox/shapiro_delay.py)
- **Best no-go / stress scripts**: [chiral_vs_symmetric_entropy.py](/mnt/d/fundamentals/sandbox/chiral_vs_symmetric_entropy.py), [ibm_quantum_h_prod_test.py](/mnt/d/fundamentals/sandbox/ibm_quantum_h_prod_test.py)
- **Most dangerous if misread**: [propagation.py](/mnt/d/fundamentals/sandbox/propagation.py), [casimir_verification.py](/mnt/d/fundamentals/sandbox/casimir_verification.py)

**Audit verdict**: sandbox classification pass completed. The sandbox is a net asset, but its pedagogy layer still needs guardrails.
