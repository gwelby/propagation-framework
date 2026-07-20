# D-Series Quantitative Task Inventory
*Per Codex 2026-07-20 formula-readiness scanner repair contract, requirement #5*
*Updated from direct import/call/artifact evidence only.*

| Task | Status | Validator wired? | Q3 decision type | Evidence |
|------|--------|-------------------|-------------------|-------|
| D1 (quark Koide fit) | EXPLORATORY | YES | computational_diagnostic | `d1_fit_v4.py:41-46` imports `validate_preflight`, `scan_artifact`; `d1_fit_v4.py:50-52` wraps `scan_artifact` in `_check_lang_scan`; `d1_fit_v4.py:255` records validator in `preflight`; `d1_fit_v4.py:817` calls `_scan_artifact` before write; `d1_v4_4_results.json` contains `preflight` key and scanner passed |
| D2 (lepton Koide) | BLOCKED | N/A — dimensionally blocked | none | No quantitative output; exempt per inventory rules |
| D3 (CKM angle scan) | EXPLORATORY | YES | computational_diagnostic | `d3_ckm_scan_v3_1.py:51-53` imports `validate_preflight`, `scan_artifact`; `d3_ckm_scan_v3_1.py:1277` calls `_scan_artifact` before write; `d3_v3_1_results.json` contains `preflight` key and scanner passed |
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

## Direct Evidence (2026-07-20)

```
D1: grep -n "validate_preflight\|scan_artifact" quark_masses/d1_fit_v4.py
  41:    validate_preflight as _shared_validate,
  46:    scan_artifact as _scan_artifact,
  50:def _check_lang_scan(preflight_result, artifact_dict):
  52:    return _scan_artifact(preflight_result, artifact_dict)
 255:    preflight["validator"] = "d_series_validator.validate_preflight"
 817:    art_violations = _scan_artifact(preflight_vr, output)

D3: grep -n "validate_preflight\|scan_artifact" ckm_mixing/d3_ckm_scan_v3_1.py
  51:    validate_preflight as _shared_validate,
  53:    scan_artifact as _scan_artifact,
1277:    art_violations = _scan_artifact(d3_preflight, output)
```

## Scanner Repair Evidence (2026-07-20)

- `d_series_validator.py` self-tests include 10 fixtures: status reduction, language checks, clean/dirty artifact scans, contrast-sentence negation-boundary tests, and direct-negation boundary tests.
- `test_d_writer_fixtures.py` performs copied-candidate writer traps for D1 and D3: it injects a contrast sentence into a temp copy of each writer, asserts each exits nonzero, and asserts the original `d1_v4_4_results.json` / `d3_v3_1_results.json` are unchanged.
- D1 and D3 were re-run after the scanner repair; both wrote fresh JSON with `Language scan: PASS`.
