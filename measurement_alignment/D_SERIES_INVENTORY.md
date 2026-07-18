# D-Series Quantitative Task Inventory
*Per Codex 2026-07-15 formula-readiness gate repair, requirement #5*

| Task | Status | Validator wired? | Q3 decision type | Notes |
|------|--------|-------------------|-------------------|-------|
| D1 (quark Koide fit) | EXPLORATORY | YES — `d1_fit_v4.py:run_preflight()` calls `d_series_validator.validate_preflight()` | computational_diagnostic | Mixed renormalization scales prevent READY. Output is fitted-model values, not predictions. |
| D2 (lepton Koide) | BLOCKED | N/A — dimensionally blocked, no quantitative run | none | Dimensionally blocked; no quantitative output. |
| D3 (CKM angle scan) | EXPLORATORY | YES — `d3_ckm_scan_v3_1.py` uses `initial_pair` selector and post-hoc labels per 2026-07-15 repair | computational_diagnostic | Post-hoc reproducible sensitivity run. No sigma, no falsification, no pre-registration claim. |
| D4+ | Not started | Will require validator | TBD | Future tasks must invoke `validate_preflight()` before any quantitative run. |

## Verification

Each D-series task that produces quantitative output must:
1. Import `d_series_validator` from `measurement_alignment/`
2. Call `validate_preflight()` with Q1/Q2/Q3 statuses and Q3 decision type
3. Include the validator result in its JSON output
4. Use only allowed language per the validator's `allowed_language` field
5. Avoid all terms in the validator's `disallowed_language` list

Tasks that are BLOCKED or non-quantitative are exempt from the validator requirement but must state this explicitly.
