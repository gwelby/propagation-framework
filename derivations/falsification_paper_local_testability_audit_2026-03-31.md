# Falsification Paper — Local Testability Audit (2026-03-31)

**Scope**: Compare `papers/FALSIFICATION_PAPER_DRAFT.md` against `CLAIMS.md`, `sandbox/sandbox_results.md`, and the sandbox scripts that are runnable in the current local environment.

**Method**: Run the local scripts that map most directly to the paper's five falsification tests and nearby high-visibility claims. Record what actually runs, what fails on missing dependencies, and where the paper outruns the current local evidence.

---

## Executive Verdict

The paper is directionally useful but not yet honest enough about **what is locally testable now**.

Three main issues showed up:

1. The paper had been overstating the current status of the generation / fourth-generation chain relative to `CLAIMS.md`.
2. TEST 2 (Neutrino Koide) had gone stale: the local scan and `CLAIMS.md` both say neutrinos do **not** satisfy Koide.
3. Only part of the test suite is self-testable from this machine today. Some paths run locally, some are blocked by missing Python packages, and several depend on external experiments by design.

---

## Paper-Level Findings

### Finding 1 — Abstract had overstated T3/C1 and local testability

Before the patch in this pass, [papers/FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md#L15) said:

- the number of generations is uniquely fixed at three
- fourth-generation exclusion follows from the same axioms
- three of the five tests can be done within twelve months

That was too strong relative to [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md#L33), where:

- `Three Generations` is **CONDITIONAL 0.85**
- `4th generation forbidden` is **ARGUED 0.85**

And relative to the local environment:

- only TEST 1 and TEST 2 have meaningful partial local executability
- TEST 3, TEST 4, and TEST 5 remain external-program tests

This was corrected in the paper patch for this audit pass.

### Finding 2 — TEST 2 was contradicted by local sandbox and claim matrix

Before the patch in this pass, [papers/FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md#L223) said:

> Computed: `Q_nu ~= 0.667`

That was false under the current local scripts and current board state.

Local results:

- `python3 sandbox/koide_verify_pdg2024.py`
  - Brannen point: `Q_nu = 0.522473`
- `python3 sandbox/neutrino_koide_scan.py`
  - Normal ordering best point: `Q = 0.549622`
  - Inverted ordering best point: `Q = 0.479016`

These agree with [sandbox/sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md#L357) and [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md#L69): neutrinos do **not** satisfy Koide.

This was corrected in the paper patch for this audit pass.

### Finding 3 — TEST 5 had outrun the exact gravity claim

At [papers/FALSIFICATION_PAPER_DRAFT.md](/mnt/d/fundamentals/papers/FALSIFICATION_PAPER_DRAFT.md#L270), TEST 5 treats frequency-dependent gravitational-wave dispersion as a framework prediction under `Claim F1`.

But [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md#L29) is narrower:

- exact optical / Randers mapping for null propagation in static / stationary gravity
- sandbox gravity scripts are regression / verification of the weak-field model
- broader beyond-GR claims are not what the exact row proves

So TEST 5 should be framed as a **future extension target**, not as a closed consequence of the currently derived gravity theorem.

This was corrected in the paper patch for this audit pass.

---

## What We Can Actually Test Ourselves

| Test | Local status | What we can do now | What remains external |
| :--- | :--- | :--- | :--- |
| TEST 1 — EEG phase transition | **Untested — simulator only** | Run synthetic / proxy scripts locally | Real-data validation requires EEG hardware and dataset access; no multi-subject study conducted |
| TEST 2 — Neutrino Koide | **Self-testable now from public mass-squared data** | Recompute `Q_nu` from current oscillation inputs; local result is already negative for universality | JUNO can tighten the error bars |
| TEST 3 — Fourth generation exclusion | **Not self-testable locally** | Restate the framework's logical prediction only | Requires collider discovery / null searches |
| TEST 4 — Tau g-2 | **Not self-testable locally** | No quantitative local `delta a_tau` prediction is closed yet | Requires Belle II or equivalent |
| TEST 5 — GW dispersion | **Not self-testable locally** | We can compare against existing constraints only | Requires LIGO/LISA-class data and a quantitative PF prediction |

---

## Local Script Sweep

### Runnable and informative

- `koide_verify_pdg2024.py`
  - charged-lepton Koide confirmed to `<0.001%`
  - neutrino Brannen point is **not** near `2/3`
- `neutrino_koide_scan.py`
  - universality fails under current oscillation inputs
- `koide_phase_scan.py`
  - `delta_exact` is extremely close to `2/9`
- `casimir_verification.py`
  - formula evaluation matches the quoted on-shell value, but the script itself correctly labels this as a **sanity check**, not theorem closure
- `refractive_gravity_quantitative.py`
  - weak-field light deflection regression is acceptable
- `shapiro_delay.py`
  - weak-field Shapiro regression is very strong
- `perihelion_precession_simple.py`
  - Mercury-like regime is acceptable (`~4.5%` error), but broader cases are far worse
- `sleep_coherence_net.py`
  - supports a plausible `~2/3` active fraction model, not theorem closure
- `top_tau_coupling_explorer.py`
  - strong numerical support for the `top/tau` ratio, but not a closed mechanism
- `mass_formula_audit.py`
  - repeats the `top/tau` numerical signal and a Greulich building-block near-hit
- `phi_vs_delay.py`
  - discriminates correctly in a synthetic two-run setup; honest caveat says the biological test still requires real EEG lag data
- `eeg_csd_simulator.py`
  - renders the expected template figure only; no empirical result
- `gen2_audit.py`, `gen3_audit.py`
  - numerical pattern-hunt scripts, not theorem closure
- `ibm_quantum_h_prod_test.py`
  - useful local no-go comparison for the symmetric walk; hardware portion is offline without Qiskit / IBM runtime

### Blocked by local environment

- `eeg_csd_analysis.py`
  - fails: `ModuleNotFoundError: No module named 'mne'`
- `analyze_real_eeg.py`
  - fails: `ModuleNotFoundError: No module named 'pandas'`
- `ibm_quantum_chiral_test.py`
  - fails: `ModuleNotFoundError: No module named 'qiskit'`

### Internally inconsistent / needs cleanup

- `chiral_projection_z3.py`
  - computed values still show `|beta/alpha| = 1` and nonzero off-diagonals in `T_L^3`, while the printed interpretation says `beta ~= 0` and diagonal closure
- `perihelion_precession.py`
  - did not produce the advertised quantitative values in the local run (`None` outputs in the printed table)

---

## Path Contamination / Reproducibility Note

Several scripts wrote output files to literal Windows-style filenames in the repository root during WSL execution, e.g.:

- `D:\Fundamentals\sandbox\sandbox_results.md`
- `d:\Fundamentals\sandbox\refractive_verification.png`

This does not invalidate the mathematical results, but it **does** contaminate the local audit trail and should be fixed before any clean reproducibility claim is made.

---

## Paper Changes Applied In This Pass

1. The abstract now matches `CLAIMS.md`:
   - T3 is conditional
   - C1 is argued
   - only TEST 1 / TEST 2 are partially locally executable right now

2. TEST 2 now reflects the actual local result:
   - current public-data scan is already a negative result for universality
   - JUNO is a refinement / sharpening step, not the first computation

3. TEST 5 is now marked as an extension target beyond the current exact gravity theorem.

4. The falsification section now contains a compact "what we can test ourselves now" table.

---

## Bottom Line

The paper is strongest when it behaves like the sandbox:

- exact where exact
- conditional where conditional
- negative where negative
- blocked where blocked

That is the standard the repo is now capable of meeting.
