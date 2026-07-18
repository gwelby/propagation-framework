# D-Series Task Preflight Template
*Per Codex formula-readiness gate (2026-07-12, repaired 2026-07-15)*

Every new D-series quantitative task must include this preflight before numerical
runs. Status must be declared **before** reading results.

**Shared validator:** `d_series_validator.py` in this directory provides the
executable status enum, deterministic reducer, and language checker. All D-series
tasks must invoke `validate_preflight()` from this module.

## Q1: Units and Normalization

**Check:** Do units and normalization close in the actual implementation?

| Field | Required record |
|-------|----------------|
| Q1 status | `CLOSED` / `OPEN` / `BLOCKED` |
| Units | State the unit system (e.g., MeV, GeV, natural units) |
| Normalization | State the normalization convention and verify it is dimensionally consistent |
| Evidence | Cite the source line(s) or equation(s) where closure is verified |

## Q2: Inputs and Physical Definitions

**Check:** Do all inputs have physical definitions? Are all calibration, target
selection, and reused observed targets declared?

| Field | Required record |
|-------|----------------|
| Q2 status | `CLOSED` / `OPEN` / `BLOCKED` |
| Input manifest | List each input: value, unit, scheme, scale, source, confidence convention |
| Calibration | Declare any calibration parameters and how they were selected |
| Target selection | If a target value is used, state whether it is independent or a posteriori |
| Reused observed targets | List any observed values reused as inputs |

## Q3: Observable, Control, and Decision Threshold

**Check:** Are the observable, control/null, and decision threshold written
before the run? Is the decision type declared?

| Field | Required record |
|-------|----------------|
| Q3 status | `CLOSED` / `OPEN` / `BLOCKED` |
| Observable | State the quantity being computed |
| Control / null | State the control or null comparison |
| Decision threshold | State the pass/fail rule **before** reading the result |
| Decision type | `computational_diagnostic` / `physical_sigma` / `compatibility_test` / `falsification_test` / `none` |
| Pre-registration | State the plan hash or receipt path (if pre-registered) |

**Decision type distinction (2026-07-15 repair):**
- `computational_diagnostic`: chi^2, p-values are numerical outputs of the declared model. May NOT claim physical sigma, compatibility, or falsification.
- `physical_sigma`: may report sigma-based results (requires READY).
- `compatibility_test`: may claim compatibility/incompatibility (requires READY).
- `falsification_test`: may claim falsification (requires READY).
- `none`: no decision-type language allowed.

## Overall Status

| Status | Meaning |
|--------|---------|
| `READY` | Can produce model predictions, sigma, compatibility, or falsification verdicts (per Q3 decision type) |
| `EXPLORATORY` | May run sensitivity/diagnostic work; cannot produce prediction, physical sigma, compatibility, falsification, or public language |
| `BLOCKED` | The requested quantitative run is invalid until the missing item is closed |
| `UNKNOWN` | One or more Q statuses are undeclared or unparseable; no quantitative output is valid |

**Rule (executable in `d_series_validator.py`):** Overall status is `READY` only if all three checks are `CLOSED`.
`EXPLORATORY` if all are at least `DECLARED` but not all `CLOSED`. `BLOCKED` if any is `OPEN` or `BLOCKED`. `UNKNOWN` if any is undeclared.

## Example: D1 v4 Preflight

See `quark_masses/d1_fit_v4.py` `run_preflight()` for a working implementation.
Wired through `d_series_validator.validate_preflight()`.
Current status: `EXPLORATORY` (Q1 CLOSED, Q2 DECLARED, Q3 DECLARED, decision type `computational_diagnostic` — not READY
because mixed renormalization scales prevent a closed unit system).
