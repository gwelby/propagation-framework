# Stale D1 v4 Results — Superseded

**Why archived:** Multiple incompatible D1 v4 result files existed in the same directory. This archive contains three superseded artifacts:

1. `D1_v4_fit_results_20260711_superseded.*` — the oldest v4 pair from 2026-07-11. It used v3 input uncertainties (e.g., `m_u = 2.16 ± 0.49`) and produced different numbers than the newer pair.
2. `D1_fit_v4_results_20260712_superseded.md` and `d1_v4_results_20260712_superseded.json` — the v4 pair from 2026-07-12. It had the source-correct formula but the wrong confidence convention (treated heavy-quark errors as 1σ when PDG marks them as 90% CL) and the old 2D optimizer that Codex found not converged.
3. `D1_fit_v4_1_results_20260713_superseded.md` and `d1_v4_1_results_20260713_superseded.json` — the v4.1 pair from 2026-07-13. It improved the confidence convention and optimizer but still labeled the direct top uncertainty as 90% CL (PDG does not label it as such) and kept TENSION/COMPATIBLE verdict language.
4. `D1_fit_v4_2_results_20260713_superseded.md` and `d1_v4_2_results_20260713_superseded.json` — the v4.2 pair from 2026-07-13. It fixed the above but contained a factual error in the summary-table charm value (wrote `1270.0 ± 4.6` instead of `1273.0 ± 4.6`) and lacked the explicit `## Codex Ask` packet heading.

**Current canonical pair:**
- `d1_fit_v4.py` (source)
- `D1_fit_v4_3_results.md` (markdown report)
- `d1_v4_3_results.json` (machine-readable output)

**Status:** The current canonical pair addresses the v4.2 text/process repairs. It remains **EXPLORATORY/HOLD** on p-value interpretation because the top quark confidence convention is not closed by PDG and the inputs are at mixed scales. Governing reports: `/mnt/d/Codex/REPORTS/CODEX_20260712_D1_QUARK_KOIDE_V4_REAUDIT.md`, `/mnt/d/Codex/REPORTS/CODEX_20260713_D1_QUARK_KOIDE_V41_REAUDIT.md`, and `/mnt/d/Codex/REPORTS/CODEX_20260713_D1_QUARK_KOIDE_V42_REAUDIT.md`.

HOLD items remaining: scale-consistent QCD running, full top-mass uncertainty propagation, correlation model, weak-basis/pseudo-mass test.

**Do not cite these archived files as current D1 truth.**
