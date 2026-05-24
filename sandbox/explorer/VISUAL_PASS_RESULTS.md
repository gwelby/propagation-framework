# PFExplorer Visual Pass Results

This file is the append-only log of visual-pass runs over the PFExplorer panels. Each row records one panel check against a specific commit. A clean row must exist here for every panel before pushing to `gh-pages`.

The rules governing this log come from the bugfix spec at `.kiro\specs\explorer-panel-render-health\requirements.md`, Requirement 8 (live render verification before release) and Requirement 10 (no silent deployments). In short:

- A passing static audit alone is not sufficient for release.
- Do not push to `gh-pages` without appending a clean row here for every panel touched or for the full panel set when a deploy is claimed.
- A `FAIL` row MUST NOT be followed by a deploy. Fix the underlying panel first, then record a `PASS` row from a subsequent run.

## How to generate entries

1. Start the local static server:

   ```
   python sandbox\explorer\serve.py
   ```

2. In a separate shell, run the visual pass:

   ```
   python sandbox\explorer\visual_pass.py
   ```

   The tool loads each panel in headless Chromium, waits for first paint, and samples a 200x200 pixel block at canvas center. A panel passes if at least one sampled pixel differs from the page background by more than 5 in any channel (see Req 1.4).

3. For each panel, append one row to the table below with:

   - `Commit`: short SHA from `git rev-parse --short HEAD`
   - `Date`: ISO date (YYYY-MM-DD) of the run
   - `Panel`: panel filename without extension (e.g. `god-equation`, `bohr`, `hub`)
   - `Result`: `PASS`, `FAIL`, or `SKIP` (see Legend)
   - `Note`: short free-text note; for `FAIL` describe the symptom, for `SKIP` explain why the panel was excluded

Do not edit or delete existing rows. The log is append-only so the audit trail stays intact.

## Results

| Commit | Date | Panel | Result | Note |
| ------ | ---- | ----- | ------ | ---- |
| c52c79e (pre-fix) | 2026-05-06 | observatory | PASS | 40000 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | hub | PASS | 15358 non-bg pixels (after adding script tag + data.js + core.js shims) |
| c52c79e (pre-fix) | 2026-05-06 | foundations | PASS | 39930 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | god-equation | PASS | 303 non-bg pixels (after guarded ctx.data + formatScientific shim) |
| c52c79e (pre-fix) | 2026-05-06 | koide | PASS | 40000 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | weinberg | PASS | 173 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | refraction | PASS | 40000 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | bohr | PASS | 2353 non-bg pixels (after renderer setSize + this.resize wiring) |
| c52c79e (pre-fix) | 2026-05-06 | generations | PASS | 11400 non-bg pixels (after this.resize wiring) |
| c52c79e (pre-fix) | 2026-05-06 | consciousness | PASS | 39850 non-bg pixels (after guarded data-layer + stub fallbacks) |
| c52c79e (pre-fix) | 2026-05-06 | koide-weinberg-bridge | PASS | 2319 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | dashboard | PASS | 31106 non-bg pixels (after adding script tag + data.js + core.js shims) |
| c52c79e (pre-fix) | 2026-05-06 | proof-atlas | PASS | 40000 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | experiment-bench | PASS | 40000 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | no-go-museum | PASS | 40000 non-bg pixels |
| c52c79e (pre-fix) | 2026-05-06 | definition-lattice | PASS | 40000 non-bg pixels (after removing stray IIFE tail) |
| c52c79e (pre-fix) | 2026-05-06 | scale-ladder-panel | PASS | 40000 non-bg pixels |

_Run log: `python sandbox\explorer\visual_pass.py --screenshots sandbox\explorer\_visual_pass_screens` at 1920x1080 via headless Chromium. Background colour (10, 10, 26). Exit 0, 17/17 panel(s) clean. Screenshots captured in `sandbox/explorer/_visual_pass_screens/`. The "c52c79e (pre-fix)" column annotates that the fixes for this spec were applied on top of commit c52c79e and have not yet been re-committed; the next release commit will re-run this sequence and append a fresh block below._

| ff68d29 | 2026-05-06 | observatory | PASS | live: 40000 non-bg pixels |
| ff68d29 | 2026-05-06 | hub | PASS | live: 15358 non-bg pixels |
| ff68d29 | 2026-05-06 | foundations | PASS | live: 39989 non-bg pixels |
| ff68d29 | 2026-05-06 | god-equation | PASS | live: 4291 non-bg pixels |
| ff68d29 | 2026-05-06 | koide | PASS | live: 40000 non-bg pixels |
| ff68d29 | 2026-05-06 | weinberg | PASS | live: 173 non-bg pixels |
| ff68d29 | 2026-05-06 | refraction | PASS | live: 40000 non-bg pixels |
| ff68d29 | 2026-05-06 | bohr | PASS | live: 2353 non-bg pixels |
| ff68d29 | 2026-05-06 | generations | PASS | live: 11400 non-bg pixels |
| ff68d29 | 2026-05-06 | consciousness | PASS | live: 39791 non-bg pixels |
| ff68d29 | 2026-05-06 | koide-weinberg-bridge | PASS | live: 2319 non-bg pixels |
| ff68d29 | 2026-05-06 | dashboard | PASS | live: 31106 non-bg pixels |
| ff68d29 | 2026-05-06 | proof-atlas | PASS | live: 40000 non-bg pixels |
| ff68d29 | 2026-05-06 | experiment-bench | PASS | live: 40000 non-bg pixels |
| ff68d29 | 2026-05-06 | no-go-museum | PASS | live: 40000 non-bg pixels |
| ff68d29 | 2026-05-06 | definition-lattice | PASS | live: 40000 non-bg pixels |
| ff68d29 | 2026-05-06 | scale-ladder-panel | PASS | live: 40000 non-bg pixels |

_Live deploy verification: `python sandbox\explorer\visual_pass.py --server https://gwelby.github.io/PFExplorer/` at 1920x1080 via headless Chromium after gh-pages CDN refresh. Exit 0, 17/17 panel(s) clean. This satisfies Requirement 10 (no silent deployments) — the live URL is verified, not just the build pipeline._

## Legend

- `PASS` — Requirement 1.4 satisfied: at least one non-background pixel present in the 200x200 centre sample of the panel canvas within 500 ms of mount.
- `FAIL` — Panel rendered blank, renderer errored, or every sampled pixel was within 5 of the page background. Do NOT ship a build that produced this row; fix the panel and record a later `PASS` first.
- `SKIP` — Panel was intentionally skipped for this run (e.g. no WebGL available in the environment, panel temporarily disabled). The `Note` column MUST explain the reason; a `SKIP` row does not satisfy the release gate for that panel.
