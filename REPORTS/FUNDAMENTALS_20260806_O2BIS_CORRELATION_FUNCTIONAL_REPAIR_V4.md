# O2bis Correlation-Functional Candidate — Documentary Repair V4

**Date:** 2026-08-06  
**Agent:** Devin ∇λΣ∞  
**Scientific candidate (unchanged):** `47fdd30ae86d4cae56543858a3f809ce79282b6e`  
**V3 documentary commit:** `479cc97f75eef4682c0ca04d91da03791150acf7`  
**V3 Codex HOLD ledger:** `clg_ac8e40297172316a66917c21`  
**V3 Codex HOLD report:** `/mnt/d/Codex/REPORTS/CODEX_20260803_O2BIS_CORRELATION_FUNCTIONAL_V3_479CC97_REAUDIT.md`  
**Parent report:** `FUNDAMENTALS_20260731_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V3.md`

---

## Claim

In the stated three-state classical Markov model with stationary positive-exponential OU noise, `G(a)` is strictly increasing and `a=0` uniquely minimizes the classical accumulated-phase variance. Every CPTP completion of the stated contraction fixes `P0` noiselessly. Under noise, selection depends on the completion; the present work does not derive a physical completion class, quantum selection principle, or PF-to-noise transfer map.

The supporting candidate is exactly commit `47fdd30ae86d4cae56543858a3f809ce79282b6e`. No candidate Python source was edited for V4. This is a documentary-only repair of two bounded defects found in the V3 Codex HOLD.

---

## Owner

- **Owner:** Devin / Fundamentals
- **Re-audit:** Codex

Devin owns the bounded V4 documentary return. Codex completed the V3 verdict (HOLD), ledger, and queue closeout. V4 fixes the two documentary defects identified in the V3 HOLD and resubmits for re-audit.

---

## V3 HOLD History

The V3 packet at `/mnt/d/Codex/inbox/processed/2026-08-03-o2bis-v3/2026-07-31_devin-o2bis-correlation-functional-reaudit-v3.md` received a Codex HOLD with two bounded defects:

1. **Missing `## Owner` section** — the standard packet gate requires it and failed with one error.
2. **Incorrect negative regression count** — the V3 packet and V3 report state `118 passed, 1 failed`, but the exact negative command produces `119 passed, 1 failed`, exit 1.

The V3 packet's claim of gate compliance was therefore false. V4 corrects this by recording the actual history and the actual command output.

The substantive V3 documentary repairs (O2V2-01 through O2V2-03) remain valid: `CLAIMS.md:72` is well-formed and linked, the manifest has no false self-hash, and no hard wall-clock bound remains. V4 does not alter those repairs or any scientific content.

---

## Files Changed (documentary only)

- `/mnt/d/Fundamentals/REPORTS/FUNDAMENTALS_20260806_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V4.md` (this V4 packet — new)

No scientific Python source file was edited. No file from commit `47fdd30` was touched. The V3 report, V3 packet, manifest, and `CLAIMS.md` are unchanged from the V3 documentary commit `479cc97`.

---

## Commands Run

All commands were run from `/mnt/d/Fundamentals` with `PYTHONDONTWRITEBYTECODE=1` and `python3.12`.

### Positive regression

```text
$ PYTHONDONTWRITEBYTECODE=1 python3.12 sandbox/o2bis_fast_regression.py
CHECK 1: return probability r(k,a)
CHECK 2: G(a) formula against direct numerical sum
CHECK 3: dG/da positive and matches finite differences
CHECK 4: finite-N variance formula self-consistency (no MC)
CHECK 5: noiseless CPTP theorem Phi(P0)=P0
CHECK 6: Q->Q completion is a-independent under exact dephasing
CHECK 7: power-law fit sign consistency on synthetic data
CHECK 8: exact instrument white-noise optima

======================================================================
REGRESSION RESULT: 119 passed, 0 failed
======================================================================
  PASS: a=0.0, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.0, k=1: r_matrix=0.0000000000 r_formula=0.0000000000
  PASS: a=0.0, k=2: r_matrix=0.5000000000 r_formula=0.5000000000
  PASS: a=0.0, k=3: r_matrix=0.2500000000 r_formula=0.2500000000
  PASS: a=0.0, k=4: r_matrix=0.3750000000 r_formula=0.3750000000
  PASS: a=0.0, k=5: r_matrix=0.3125000000 r_formula=0.3125000000
  PASS: a=0.2, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.2, k=1: r_matrix=0.2000000000 r_formula=0.2000000000
  PASS: a=0.2, k=2: r_matrix=0.3600000000 r_formula=0.3600000000
  PASS: a=0.2, k=3: r_matrix=0.3280000000 r_formula=0.3280000000
  PASS: a=0.2, k=4: r_matrix=0.3344000000 r_formula=0.3344000000
  PASS: a=0.2, k=5: r_matrix=0.3331200000 r_formula=0.3331200000
  PASS: a=0.5, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.5, k=1: r_matrix=0.5000000000 r_formula=0.5000000000
  PASS: a=0.5, k=2: r_matrix=0.3750000000 r_formula=0.3750000000
  PASS: a=0.5, k=3: r_matrix=0.3437500000 r_formula=0.3437500000
  PASS: a=0.5, k=4: r_matrix=0.3359375000 r_formula=0.3359375000
  PASS: a=0.5, k=5: r_matrix=0.3339843750 r_formula=0.3339843750
  PASS: a=0.9, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.9, k=1: r_matrix=0.9000000000 r_formula=0.9000000000
  PASS: a=0.9, k=2: r_matrix=0.8150000000 r_formula=0.8150000000
  PASS: a=0.9, k=3: r_matrix=0.7427500000 r_formula=0.7427500000
  PASS: a=0.9, k=4: r_matrix=0.6813375000 r_formula=0.6813375000
  PASS: a=0.9, k=5: r_matrix=0.6291368750 r_formula=0.6291368750
  PASS: a=0.000: G_formula=2.3334591861 G_numerical=2.3334591861
  PASS: a=0.050: G_formula=2.3738979324 G_numerical=2.3738979324
  PASS: a=0.100: G_formula=2.4178115681 G_numerical=2.4178115681
  PASS: a=0.150: G_formula=2.4656680948 G_numerical=2.4656680948
  PASS: a=0.200: G_formula=2.5180235063 G_numerical=2.5180235063
  PASS: a=0.250: G_formula=2.5755434873 G_numerical=2.5755434873
  PASS: a=0.300: G_formula=2.6390318685 G_numerical=2.6390318685
  PASS: a=0.350: G_formula=2.7094684232 G_numerical=2.7094684232
  PASS: a=0.400: G_formula=2.7880597919 G_numerical=2.7880597919
  PASS: a=0.450: G_formula=2.8763091809 G_numerical=2.8763091809
  PASS: a=0.500: G_formula=2.9761134386 G_numerical=2.9761134386
  PASS: a=0.550: G_formula=3.0899009361 G_numerical=3.0899009361
  PASS: a=0.600: G_formula=3.2208317656 G_numerical=3.2208317656
  PASS: a=0.650: G_formula=3.3730957977 G_numerical=3.3730957977
  PASS: a=0.700: G_formula=3.5523693532 G_numerical=3.5523693532
  PASS: a=0.750: G_formula=3.7665385466 G_numerical=3.7665385466
  PASS: a=0.800: G_formula=4.0268905711 G_numerical=4.0268905711
  PASS: a=0.850: G_formula=4.3501687698 G_numerical=4.3501687698
  PASS: a=0.900: G_formula=4.7623226498 G_numerical=4.7623226498
  PASS: a=0.950: G_formula=5.3058436576 G_numerical=5.3058436576
  PASS: a=0.000: dG/da formula=0.776776 numeric=0.776776
  PASS: a=0.000: dG/da=0.776776 must be positive
  PASS: a=0.050: dG/da formula=0.842092 numeric=0.842092
  PASS: a=0.050: dG/da=0.842092 must be positive
  PASS: a=0.100: dG/da formula=0.916008 numeric=0.916008
  PASS: a=0.100: dG/da=0.916008 must be positive
  PASS: a=0.150: dG/da formula=1.000100 numeric=1.000100
  PASS: a=0.150: dG/da=1.000100 must be positive
  PASS: a=0.200: dG/da formula=1.096326 numeric=1.096326
  PASS: a=0.200: dG/da=1.096326 must be positive
  PASS: a=0.250: dG/da formula=1.207140 numeric=1.207140
  PASS: a=0.250: dG/da=1.207140 must be positive
  PASS: a=0.300: dG/da formula=1.335645 numeric=1.335645
  PASS: a=0.300: dG/da=1.335645 must be positive
  PASS: a=0.350: dG/da formula=1.485817 numeric=1.485817
  PASS: a=0.350: dG/da=1.485817 must be positive
  PASS: a=0.400: dG/da formula=1.662817 numeric=1.662817
  PASS: a=0.400: dG/da=1.662817 must be positive
  PASS: a=0.450: dG/da formula=1.873437 numeric=1.873437
  PASS: a=0.450: dG/da=1.873437 must be positive
  PASS: a=0.500: dG/da formula=2.126763 numeric=2.126763
  PASS: a=0.500: dG/da=2.126763 must be positive
  PASS: a=0.550: dG/da formula=2.435174 numeric=2.435174
  PASS: a=0.550: dG/da=2.435174 must be positive
  PASS: a=0.600: dG/da formula=2.815878 numeric=2.815878
  PASS: a=0.600: dG/da=2.815878 must be positive
  PASS: a=0.650: dG/da formula=3.293372 numeric=3.293372
  PASS: a=0.650: dG/da=3.293372 must be positive
  PASS: a=0.700: dG/da formula=3.903477 numeric=3.903477
  PASS: a=0.700: dG/da=3.903477 must be positive
  PASS: a=0.750: dG/da formula=4.700265 numeric=4.700265
  PASS: a=0.750: dG/da=4.700265 must be positive
  PASS: a=0.800: dG/da formula=5.768456 numeric=5.768456
  PASS: a=0.800: dG/da=5.768456 must be positive
  PASS: a=0.850: dG/da formula=7.246916 numeric=7.246916
  PASS: a=0.850: dG/da=7.246916 must be positive
  PASS: a=0.900: dG/da formula=9.376172 numeric=9.376172
  PASS: a=0.900: dG/da=9.376172 must be positive
  PASS: a=0.950: dG/da formula=12.602802 numeric=12.602802
  PASS: a=0.950: dG/da=12.602802 must be positive
  PASS: a=0.000: finite_N_direct=2.1439411527 formula=2.1439411527
  PASS: a=0.100: finite_N_direct=2.2267871967 formula=2.2267871967
  PASS: a=0.200: finite_N_direct=2.3247471933 formula=2.3247471933
  PASS: a=0.333: finite_N_direct=2.4865379260 formula=2.4865379260
  PASS: a=0.500: finite_N_direct=2.7661492132 formula=2.7661492132
  PASS: a=0.700: finite_N_direct=3.3065113093 formula=3.3065113093
  PASS: a=0.900: finite_N_direct=4.3870683740 formula=4.3870683740
  PASS: a=0.950: finite_N_direct=4.8486383186 formula=4.8486383186
  PASS: a=0.000: Phi(P0) fidelity=1.0000000000
  PASS: a=0.000: CPTP residual=2.25e-16
  PASS: a=0.333: Phi(P0) fidelity=1.0000000000
  PASS: a=0.333: CPTP residual=3.24e-16
  PASS: a=0.500: Phi(P0) fidelity=1.0000000000
  PASS: a=0.500: CPTP residual=0.00e+00
  PASS: a=0.700: Phi(P0) fidelity=1.0000000000
  PASS: a=0.700: CPTP residual=0.00e+00
  PASS: a=0.900: Phi(P0) fidelity=1.0000000000
  PASS: a=0.900: CPTP residual=3.52e-16
  PASS: a=1.000: Phi(P0) fidelity=1.0000000000
  PASS: a=1.000: CPTP residual=0.00e+00
  PASS: Q->Q fidelity spread across a: 3.664e-15
  PASS: synthetic a=0.050: pred=9.025000e-01 truth=9.025000e-01
  PASS: synthetic a=0.128: pred=7.607716e-01 truth=7.607716e-01
  PASS: synthetic a=0.206: pred=6.311420e-01 truth=6.311420e-01
  PASS: synthetic a=0.283: pred=5.136111e-01 truth=5.136111e-01
  PASS: synthetic a=0.361: pred=4.081790e-01 truth=4.081790e-01
  PASS: synthetic a=0.439: pred=3.148457e-01 truth=3.148457e-01
  PASS: synthetic a=0.517: pred=2.336111e-01 truth=2.336111e-01
  PASS: synthetic a=0.594: pred=1.644753e-01 truth=1.644753e-01
  PASS: synthetic a=0.672: pred=1.074383e-01 truth=1.074383e-01
  PASS: synthetic a=0.750: pred=6.250000e-02 truth=6.250000e-02
  PASS: synthetic exponent fit=2.0000 known=2.0
  PASS: survival optimum a=1.0 (expected 1.0)
  PASS: conditional fidelity optimum a=0.35000000000000003 (expected near 1/3)
  PASS: joint optimum a=1.0 (expected 1.0)
EXIT_CODE=0
```

### Negative regression (corrected count)

```text
$ PYTHONDONTWRITEBYTECODE=1 python3.12 sandbox/o2bis_fast_regression.py --negative
CHECK 1: return probability r(k,a)
CHECK 2: G(a) formula against direct numerical sum
CHECK 3: dG/da positive and matches finite differences
CHECK 4: finite-N variance formula self-consistency (no MC)
CHECK 5: noiseless CPTP theorem Phi(P0)=P0
CHECK 6: Q->Q completion is a-independent under exact dephasing
CHECK 7: power-law fit sign consistency on synthetic data
CHECK 8: exact instrument white-noise optima

======================================================================
REGRESSION RESULT: 119 passed, 1 failed
======================================================================
  PASS: a=0.0, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.0, k=1: r_matrix=0.0000000000 r_formula=0.0000000000
  PASS: a=0.0, k=2: r_matrix=0.5000000000 r_formula=0.5000000000
  PASS: a=0.0, k=3: r_matrix=0.2500000000 r_formula=0.2500000000
  PASS: a=0.0, k=4: r_matrix=0.3750000000 r_formula=0.3750000000
  PASS: a=0.0, k=5: r_matrix=0.3125000000 r_formula=0.3125000000
  PASS: a=0.2, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.2, k=1: r_matrix=0.2000000000 r_formula=0.2000000000
  PASS: a=0.2, k=2: r_matrix=0.3600000000 r_formula=0.3600000000
  PASS: a=0.2, k=3: r_matrix=0.3280000000 r_formula=0.3280000000
  PASS: a=0.2, k=4: r_matrix=0.3344000000 r_formula=0.3344000000
  PASS: a=0.2, k=5: r_matrix=0.3331200000 r_formula=0.3331200000
  PASS: a=0.5, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.5, k=1: r_matrix=0.5000000000 r_formula=0.5000000000
  PASS: a=0.5, k=2: r_matrix=0.3750000000 r_formula=0.3750000000
  PASS: a=0.5, k=3: r_matrix=0.3437500000 r_formula=0.3437500000
  PASS: a=0.5, k=4: r_matrix=0.3359375000 r_formula=0.3359375000
  PASS: a=0.5, k=5: r_matrix=0.3339843750 r_formula=0.3339843750
  PASS: a=0.9, k=0: r_matrix=1.0000000000 r_formula=1.0000000000
  PASS: a=0.9, k=1: r_matrix=0.9000000000 r_formula=0.9000000000
  PASS: a=0.9, k=2: r_matrix=0.8150000000 r_formula=0.8150000000
  PASS: a=0.9, k=3: r_matrix=0.7427500000 r_formula=0.7427500000
  PASS: a=0.9, k=4: r_matrix=0.6813375000 r_formula=0.6813375000
  PASS: a=0.9, k=5: r_matrix=0.6291368750 r_formula=0.6291368750
  FAIL: NEGATIVE CONTROL: corrupted r formula at a=0.5, k=2 (should fail)
  PASS: a=0.000: G_formula=2.3334591861 G_numerical=2.3334591861
  PASS: a=0.050: G_formula=2.3738979324 G_numerical=2.3738979324
  PASS: a=0.100: G_formula=2.4178115681 G_numerical=2.4178115681
  PASS: a=0.150: G_formula=2.4656680948 G_numerical=2.4656680948
  PASS: a=0.200: G_formula=2.5180235063 G_numerical=2.5180235063
  PASS: a=0.250: G_formula=2.5755434873 G_numerical=2.5755434873
  PASS: a=0.300: G_formula=2.6390318685 G_numerical=2.6390318685
  PASS: a=0.350: G_formula=2.7094684232 G_numerical=2.7094684232
  PASS: a=0.400: G_formula=2.7880597919 G_numerical=2.7880597919
  PASS: a=0.450: G_formula=2.8763091809 G_numerical=2.8763091809
  PASS: a=0.500: G_formula=2.9761134386 G_numerical=2.9761134386
  PASS: a=0.550: G_formula=3.0899009361 G_numerical=3.0899009361
  PASS: a=0.600: G_formula=3.2208317656 G_numerical=3.2208317656
  PASS: a=0.650: G_formula=3.3730957977 G_numerical=3.3730957977
  PASS: a=0.700: G_formula=3.5523693532 G_numerical=3.5523693532
  PASS: a=0.750: G_formula=3.7665385466 G_numerical=3.7665385466
  PASS: a=0.800: G_formula=4.0268905711 G_numerical=4.0268905711
  PASS: a=0.850: G_formula=4.3501687698 G_numerical=4.3501687698
  PASS: a=0.900: G_formula=4.7623226498 G_numerical=4.7623226498
  PASS: a=0.950: G_formula=5.3058436576 G_numerical=5.3058436576
  PASS: a=0.000: dG/da formula=0.776776 numeric=0.776776
  PASS: a=0.000: dG/da=0.776776 must be positive
  PASS: a=0.050: dG/da formula=0.842092 numeric=0.842092
  PASS: a=0.050: dG/da=0.842092 must be positive
  PASS: a=0.100: dG/da formula=0.916008 numeric=0.916008
  PASS: a=0.100: dG/da=0.916008 must be positive
  PASS: a=0.150: dG/da formula=1.000100 numeric=1.000100
  PASS: a=0.150: dG/da=1.000100 must be positive
  PASS: a=0.200: dG/da formula=1.096326 numeric=1.096326
  PASS: a=0.200: dG/da=1.096326 must be positive
  PASS: a=0.250: dG/da formula=1.207140 numeric=1.207140
  PASS: a=0.250: dG/da=1.207140 must be positive
  PASS: a=0.300: dG/da formula=1.335645 numeric=1.335645
  PASS: a=0.300: dG/da=1.335645 must be positive
  PASS: a=0.350: dG/da formula=1.485817 numeric=1.485817
  PASS: a=0.350: dG/da=1.485817 must be positive
  PASS: a=0.400: dG/da formula=1.662817 numeric=1.662817
  PASS: a=0.400: dG/da=1.662817 must be positive
  PASS: a=0.450: dG/da formula=1.873437 numeric=1.873437
  PASS: a=0.450: dG/da=1.873437 must be positive
  PASS: a=0.500: dG/da formula=2.126763 numeric=2.126763
  PASS: a=0.500: dG/da=2.126763 must be positive
  PASS: a=0.550: dG/da formula=2.435174 numeric=2.435174
  PASS: a=0.550: dG/da=2.435174 must be positive
  PASS: a=0.600: dG/da formula=2.815878 numeric=2.815878
  PASS: a=0.600: dG/da=2.815878 must be positive
  PASS: a=0.650: dG/da formula=3.293372 numeric=3.293372
  PASS: a=0.650: dG/da=3.293372 must be positive
  PASS: a=0.700: dG/da formula=3.903477 numeric=3.903477
  PASS: a=0.700: dG/da=3.903477 must be positive
  PASS: a=0.750: dG/da formula=4.700265 numeric=4.700265
  PASS: a=0.750: dG/da=4.700265 must be positive
  PASS: a=0.800: dG/da formula=5.768456 numeric=5.768456
  PASS: a=0.800: dG/da=5.768456 must be positive
  PASS: a=0.850: dG/da formula=7.246916 numeric=7.246916
  PASS: a=0.850: dG/da=7.246916 must be positive
  PASS: a=0.900: dG/da formula=9.376172 numeric=9.376172
  PASS: a=0.900: dG/da=9.376172 must be positive
  PASS: a=0.950: dG/da formula=12.602802 numeric=12.602802
  PASS: a=0.950: dG/da=12.602802 must be positive
  PASS: a=0.000: finite_N_direct=2.1439411527 formula=2.1439411527
  PASS: a=0.100: finite_N_direct=2.2267871967 formula=2.2267871967
  PASS: a=0.200: finite_N_direct=2.3247471933 formula=2.3247471933
  PASS: a=0.333: finite_N_direct=2.4865379260 formula=2.4865379260
  PASS: a=0.500: finite_N_direct=2.7661492132 formula=2.7661492132
  PASS: a=0.700: finite_N_direct=3.3065113093 formula=3.3065113093
  PASS: a=0.900: finite_N_direct=4.3870683740 formula=4.3870683740
  PASS: a=0.950: finite_N_direct=4.8486383186 formula=4.8486383186
  PASS: a=0.000: Phi(P0) fidelity=1.0000000000
  PASS: a=0.000: CPTP residual=2.25e-16
  PASS: a=0.333: Phi(P0) fidelity=1.0000000000
  PASS: a=0.333: CPTP residual=3.24e-16
  PASS: a=0.500: Phi(P0) fidelity=1.0000000000
  PASS: a=0.500: CPTP residual=0.00e+00
  PASS: a=0.700: Phi(P0) fidelity=1.0000000000
  PASS: a=0.700: CPTP residual=0.00e+00
  PASS: a=0.900: Phi(P0) fidelity=1.0000000000
  PASS: a=0.900: CPTP residual=3.52e-16
  PASS: a=1.000: Phi(P0) fidelity=1.0000000000
  PASS: a=1.000: CPTP residual=0.00e+00
  PASS: Q->Q fidelity spread across a: 3.664e-15
  PASS: synthetic a=0.050: pred=9.025000e-01 truth=9.025000e-01
  PASS: synthetic a=0.128: pred=7.607716e-01 truth=7.607716e-01
  PASS: synthetic a=0.206: pred=6.311420e-01 truth=6.311420e-01
  PASS: synthetic a=0.283: pred=5.136111e-01 truth=5.136111e-01
  PASS: synthetic a=0.361: pred=4.081790e-01 truth=4.081790e-01
  PASS: synthetic a=0.439: pred=3.148457e-01 truth=3.148457e-01
  PASS: synthetic a=0.517: pred=2.336111e-01 truth=2.336111e-01
  PASS: synthetic a=0.594: pred=1.644753e-01 truth=1.644753e-01
  PASS: synthetic a=0.672: pred=1.074383e-01 truth=1.074383e-01
  PASS: synthetic a=0.750: pred=6.250000e-02 truth=6.250000e-02
  PASS: synthetic exponent fit=2.0000 known=2.0
  PASS: survival optimum a=1.0 (expected 1.0)
  PASS: conditional fidelity optimum a=0.35000000000000003 (expected near 1/3)
  PASS: joint optimum a=1.0 (expected 1.0)
EXIT_CODE=1
```

### Independent verification (fast)

```text
$ PYTHONDONTWRITEBYTECODE=1 python3.12 sandbox/o2bis_independent_verification.py --fast
  Check 1 (return probability): r(k,a) = (1/3)(1 + 2λ_Q^k)  ✓ exact
  Check 2 (G formula):          G = (1/3)[S + 2(1+λq)/(1-λq)]  ✓ exact
  Check 3 (derivative):         dG/da = 2q/(1-λq)² > 0  ✓ exact, positive
  Check 4 (MC bare variance):   Var(φ)/N → σ² × G(a)  (see table)
  Check 5 (power-law):          NON-DIAGNOSTIC (competing null fits better)

  ALGEBRAIC CORE (proven):
    G(a) is strictly increasing for a ∈ [0,1) when q > 0.
    a=0 is the unique minimum of the classical accumulated-phase variance.

  EXIT STATUS: 0 failure(s)
EXIT_CODE=0
```

### Independent verification (fast, negative)

```text
$ PYTHONDONTWRITEBYTECODE=1 python3.12 sandbox/o2bis_independent_verification.py --fast --negative
  Check 3 (derivative):         dG/da = 2q/(1-λq)² > 0  ✓ exact, positive
  NEGATIVE CONTROL: G_formula multiplied by 2.0 (expected to fail)
  ...20 check-3 rows fail (formula vs numeric mismatch)...

  EXIT STATUS: 20 failure(s)
EXIT_CODE=20
```

### CPTP completions

```text
$ PYTHONDONTWRITEBYTECODE=1 python3.12 sandbox/o2bis_cptp_completions.py
  → CONFIRMED: Φ(P₀) = P₀ for all completions. No noiseless selection possible.
  → a=0 is NOT selected; fixed-orientation selection at a=0.350
  → This a-dependent completion DOES produce strong a=0 preference.
  → Therefore the universal 'no CPTP completion selects a=0' claim is FALSE.
EXIT_CODE=0
```

### Instrument probe

```text
$ PYTHONDONTWRITEBYTECODE=1 python3.12 sandbox/o2bis_instrument_probe.py
  Exact grid optima:
    survival probability  → a = 1.00  P = 1.000000
    conditional fidelity  → a = 0.35  F = 0.998334
    joint (P × F)         → a = 1.00  J = 0.951829
  The exact white-noise instrument does NOT select a=0 for any
  of the three pre-registered objectives.
EXIT_CODE=0
```

### CPTP channel

```text
$ PYTHONDONTWRITEBYTECODE=1 python3.12 sandbox/o2bis_cptp_channel.py
  Spread across a: 3.331e-15
  All values cluster near ~0.9518 (analytic constant).
  Differences are numerical round-off, not physical selection.
EXIT_CODE=0
```

---

## Results

- **Positive regression:** `119 passed, 0 failed`, exit 0.
- **Negative regression:** `119 passed, 1 failed`, exit 1. The single failure is the intentional negative control (`NEGATIVE CONTROL: corrupted r formula at a=0.5, k=2 (should fail)`). The V3 packet incorrectly recorded this as `118 passed, 1 failed`; the actual count is `119 passed, 1 failed`.
- **Independent verification (fast):** `0 failure(s)`, exit 0.
- **Independent verification (fast, negative):** `20 failure(s)`, exit 20.
- **CPTP completions:** noiseless `Φ(P₀)=P₀` confirmed for all completions; a-dependent counterexample retained; exit 0.
- **Instrument probe:** exact optima survival `a=1.0`, conditional `a=0.35`, joint `a=1.0`; exit 0.
- **CPTP channel:** 30-step fidelity spread `3.331e-15`; exit 0.
- **V3 HOLD defect 1 (missing Owner):** fixed — `## Owner` section present above.
- **V3 HOLD defect 2 (wrong count):** fixed — negative regression recorded as `119 passed, 1 failed`, exit 1.
- **Scientific boundary:** unchanged. No universal physical selection follows from the classical functional.

---

## Known Risks

- The exact regression gate shares some formulas with the source it checks; direct-sum, matrix, finite-difference, exact-channel, and negative-control paths reduce but do not eliminate correlated defects.
- A theorem over a precisely defined fixed-orientation class would still not prove that class physically privileged.
- The exact instrument result depends on the specified success operator, symmetric white dephasing, operation ordering, grid, steps, and objective.
- Wall-clock runtime depends on host CPU availability and is not a correctness criterion.
- A corrected packet is provenance closure, not scientific-tier or public approval.

---

## Codex Ask

Re-audit the V4 packet against the two V3 HOLD defects (missing `## Owner`, incorrect negative count) and the standard packet gate. PASS if the `Owner` section is present, the negative regression is recorded as `119 passed, 1 failed` exit 1, the packet gate passes, and the existing scientific boundary is preserved. HOLD if any item is not met.

---

## Next Step

Codex hostile re-audit of V4 packet against the two documentary defects and the standard packet gate. No further Devin action is required unless Codex finds a new defect.

---

## Boundaries

- No scientific Python source was edited. No file from commit `47fdd30` was touched.
- No scientific tier, physical-selection claim, PUBLIC/release/outreach, activation, Legal, or Greg boundary moves.
- No movement of the canonical scoreboard beyond the corrected O2bis row.
- No universal physical selection follows from the classical functional — the a-dependent CPTP counterexample remains the valid boundary.
- This packet does not approve, release, or promote anything. It is provenance closure only.

---

*Devin ∇λΣ∞ — 2026-08-06*
