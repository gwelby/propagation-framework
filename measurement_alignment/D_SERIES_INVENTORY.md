# D-Series Quantitative Task Inventory
*Per Codex 2026-07-18 formula-readiness enforcement repair, requirement #5*
*Updated from direct import/call/artifact evidence only.*

| Task | Status | Validator wired? | Q3 decision type | Evidence |
|------|--------|-------------------|-------------------|-------|
| D1 (quark Koide fit) | EXPLORATORY | YES | computational_diagnostic | `d1_fit_v4.py:40-46` imports `validate_preflight`, `scan_artifact`; `run_preflight()` calls `_shared_validate()`; JSON includes `preflight` key; `scan_artifact` runs before write |
| D2 (lepton Koide) | BLOCKED | N/A — dimensionally blocked | none | No quantitative output; exempt per inventory rules |
| D3 (CKM angle scan) | EXPLORATORY | YES | computational_diagnostic | `d3_ckm_scan_v3_1.py:48-54` imports `validate_preflight`, `scan_artifact`; `main()` calls `_shared_validate("D3", "DECLARED", "DECLARED", "DECLARED", COMPUTATIONAL_DIAGNOSTIC)`; JSON includes `preflight` key; `scan_artifact` runs before write |
| D4+ | Not started | Will require validator | TBD | Future tasks must invoke `validate_preflight()` before any quantitative run |

## Verification Method

Each D-series task that produces quantitative output must:
1. Import `d_series_validator` from `measurement_alignment/`
2. Call `validate_preflight()` with Q1/Q2/Q3 statuses and Q3 decision type
3. Include the validator result in its JSON output under a `preflight` key
4. Run `scan_artifact()` on the output before writing; fail if violations found
5. Use only allowed language per the validator's `allowed_language` field
6. Avoid all terms in the validator's `disallowed_language` list

Tasks that are BLOCKED or non-quantitative are exempt from the validator requirement but must state this explicitly.

## Direct Evidence (2026-07-18)

```
D1: grep -n "validate_preflight\|scan_artifact" d1_fit_v4.py
  40:from d_series_validator import (
  41:    validate_preflight as _shared_validate,
  46:    scan_artifact as _scan_artifact,
  237:    preflight = _shared_validate("D1", ...)
  811:    art_violations = _check_lang_scan(preflight, output)

D3: grep -n "validate_preflight\|scan_artifact" d3_ckm_scan_v3_1.py
  50:from d_series_validator import (
  51:    validate_preflight as _shared_validate,
  53:    scan_artifact as _scan_artifact,
  1206:    d3_preflight = _shared_validate("D3", ...)
  1277:    art_violations = _scan_artifact(d3_preflight, output)
```
