# Proposed Honest Scoreboard (for board review)

**Date:** 2026-06-16
**Auditor:** Claude (Opus 4.8)
**Purpose:** Side-by-side of `CLAIMS.md`'s current grades vs. what the *source files* support. This is a proposal, not an edit — the board decides. Every demotion cites the source that already contains the lower grade or the audit that establishes it. **No new physics is asserted here; in every case I am moving the scoreboard down to where the underlying file already sits.**

---

## Physics section (§1) — current vs proposed

| Claim | Current | Proposed | One-line basis (source already says so) |
|---|---|---|---|
| **Gravity as optical geometry** | DERIVED 0.95 | **DERIVED 0.95** ✅ keep | Correct textbook physics (optical/Randers metric). *Add: "imported, not derived from Axioms 1–3 — not novel."* |
| **Koide Q = 2/3 (charged leptons)** | DERIVED 0.95 | **EXACT IDENTITY + OPEN selection** | `koide_geometric_equivalence.md` §4: vacuum selection "Not Yet Derived" (3 conjectural routes). The 0.95 covers the algebraic identity only. |
| **(2,1) Topological Weights — kernel** | DERIVED 0.95 | **DERIVED 0.95** ✅ keep | Genuinely proven (0 sorrys, verified). *Add: "standard SU(2)→SO(3) double cover — not PF-specific."* |
| **(2,1) Topological Weights — physical** | CONDITIONAL 0.85 | **CONDITIONAL 0.85** ✅ keep | Honest; `A_NR` undischarged. |
| **Weinberg angle** | DERIVED 0.90 | **ARGUED 0.65** | `g3_casimir_weinberg_angle.md` self-rates **ARGUED 0.65**; scheme gap open; trials factor ~0.46 (`LOOK_ELSEWHERE_RESULTS.md`). |
| **λ_c / God Equation** | DERIVED (w/ Postulate D) 0.90 | **CONDITIONAL ≤ 0.60 (ARGUED defensible)** | `lambda_c_from_axioms.md`: core hypothesis **0.05**, N^{D/2} bridge "not proven", D=3 at 0.60; decoherence probe self-rates **CONDITIONAL 0.88** and is an endpoint artifact (`DECOHERENCE_PROBE_AUDIT.md`); "seven approaches" recount (`POSTULATE_D_PROBE_AUDIT.md`). Floor rule: ≤ min(parents). |
| **Three Generations** | CONDITIONAL 0.85 | **CONDITIONAL 0.85** ✅ keep | Honest; T2 (M=3) not closed. |
| **Fine structure constant α** | ARGUED 0.35 / 0.60 | **OPEN** (delete scan hit) | `alpha_from_pf.md`: "FAILED… no derivation achieved." The 0.60 is a numerology scan hit the file itself rejects. |
| **Koide phase δ≈2/9** | EMPIRICAL 0.65 | **EMPIRICAL 0.65** ✅ keep | Honest; strongest empirical anchor, no PF-native selector. *Add trials factor.* |
| **Weinberg angle (Lean)** | "machine-verified DERIVED" | **"algebraic identity machine-checked"** | `WeinbergAngle.lean` proves `R=(√19−3)(√19−√3)/16`, i.e. arithmetic, not the physics identification. |
| **Top/Tau, electron/up, top-quark limit** | EMPIRICAL/ARGUED 0.65–0.90 | **COINCIDENCE (uncorrected)** until trials factor computed | Single ratios of measured numbers; no look-elsewhere correction. |

---

## Header-line edits to `CLAIMS.md` (the most-read text)

1. Delete **"God Equation upgraded to DERIVED."** Replace with: *"λ_c formula: CONDITIONAL. Reproduces λ_c to 1.48% but the N^{D/2} exponent is set to the value that fits (the heat-kernel derivation gives N¹); Postulate D is an accepted postulate, not a theorem."*
2. Delete **"Seven approaches converged"** everywhere (`POSTULATE_D_PROBE_AUDIT.md`).
3. Delete **"decisive … selection pressure … 52.7×."** Replace with the script's own verdict (`DECOHERENCE_PROBE_AUDIT.md`).
4. Change every **"machine-verified DERIVED claim"** → **"algebraic content machine-checked in Lean 4."**
5. Add a **"Provenance"** line: Koide (1981), Foot (1994), de Vries (2004), Rivero (2005–6).

---

## What this costs and what it buys

**Costs:** the headline count drops from "4 DERIVED + God Equation" to "2 imported-but-correct DERIVED (gravity, topo-kernel) + 1 exact identity (Koide) + a strong empirical anchor (δ) + a rich no-go corpus."

**Buys:** a scoreboard that a hostile physicist cannot dismantle in ten minutes — which is the only kind worth having. Every demotion here is to a grade the repo's *own files already contain*. This is not the auditor imposing a view; it is the scoreboard catching up to the trenches.
