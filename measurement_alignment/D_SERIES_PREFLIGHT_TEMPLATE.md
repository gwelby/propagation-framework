# D-Series Task Preflight Template
*Per Codex formula-readiness gate (2026-07-12)*

Every new D-series quantitative task must include this preflight before numerical
runs. Status must be declared **before** reading results.

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
before the run?

| Field | Required record |
|-------|----------------|
| Q3 status | `CLOSED` / `OPEN` / `BLOCKED` |
| Observable | State the quantity being computed |
| Control / null | State the control or null comparison |
| Decision threshold | State the pass/fail rule **before** reading the result |
| Pre-registration | State the plan hash or receipt path (if pre-registered) |

## Overall Status

| Status | Meaning |
|--------|---------|
| `READY` | Can be called a prediction within its model |
| `EXPLORATORY` | May run sensitivity/diagnostic work; cannot produce prediction, sigma, or public language |
| `BLOCKED` | The requested quantitative run is invalid until the missing item is closed |

**Rule:** Overall status is `READY` only if all three checks are `CLOSED`.
Otherwise it is `EXPLORATORY` (if all are at least `OPEN`) or `BLOCKED`.

## Example: D1 v4 Preflight

See `quark_masses/d1_fit_v4.py` `run_preflight()` for a working implementation.
Current status: `EXPLORATORY` (Q1 CLOSED, Q2 DECLARED, Q3 DECLARED — not READY
because mixed renormalization scales prevent a closed unit system).
