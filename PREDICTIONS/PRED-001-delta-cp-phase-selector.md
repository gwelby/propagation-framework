# PRED-001 — PMNS leptonic CP phase δ_CP (via a PF-native phase selector)

> **STATUS: BLOCKED.** This is NOT a live prediction. It is the one machine the framework must build to *become able* to make a discriminating forward prediction. Logged here so the family aims at it and cannot mistake the aspiration for a commitment.

## Commitment block — *cannot be filled until the blocker clears (do not edit above the line once it can)*
```
id:             PRED-001
status:         BLOCKED
committed:      — (not yet; BLOCKED entries carry no lock until they go OPEN)
committed_by:   Claude @ (scaffold) 2026-06-18
claim:          [BLOCKED] a specific value for the PMNS leptonic CP phase δ_CP,
                output by a PF-native phase selector — NOT YET COMPUTABLE
error_bar:      [BLOCKED]
conditional_on: Postulate D (explicit premise, NOT derived; 4 derivation routes failed) ·
                Koide EM-sector-specificity (argued, not derived) ·
                a neutrino-sector extension PF has NO warrant for (its only neutrino
                result is that Koide FAILS for neutrinos, Q_NO≈0.55)
resolution:     DUNE + Hyper-Kamiokande, δ_CP at multi-σ, ~2029–2033 (feasible window)
sm_says:        SILENT — the SM treats δ_CP as a free input (this is the strong leg)
rivals_say:     UNVERIFIED — time-boxed task: do ZiP / Brannen / Rivero commit a δ_CP
                number? Real risk: they are charged-lepton constructions that may be
                SILENT on δ_CP (→ PF wouldn't distinguish from rivals, only from SM),
                OR extend via the same Koide-geometry phase (→ same number → DEGENERATE).
                MUST be checked before this can count as discriminating.
falsifier:      DUNE/HK measured δ_CP outside the selector's predicted band
```

## The blocker (why this is BLOCKED, stated plainly)
PF has **no machinery to compute δ_CP today.** The prerequisite is a **PF-native phase selector** — a derivation, from Axioms 1-3 (or an explicitly-named minimal added premise), of *why* the Koide phase δ takes the value it does. That selector:
- has been attempted and **FAILED four times** (T-021 RG audit, T-022 Casimir selector, the 2026-04-20 scalar/character lanes, the 2026-05-20 information-theoretic route — all NO-GO / target-loaded, per CLAIMS.md);
- would, *if* it derived δ=2/9, only **recover a postdiction** (δ=2/9 is degenerate across rivals) — but its *mechanism* might then output a forward δ_CP, which is the actual payoff.

So this is a **research bet, not a prediction**: PF would be staking its one shot at undeniability on a number it cannot compute, via a mechanism it has failed four times to derive, against rivals whose competing δ_CP values nobody has confirmed exist. Logging it BLOCKED keeps that honest.

## What would move this OPEN (the only path found)
1. Build the phase selector (DeepSeek/Codex frontier — the real physics).
2. Confirm it recovers δ=2/9 from the axioms (postdiction validation of the mechanism).
3. Run the mechanism forward to a δ_CP number + error bar.
4. Complete `rivals_say` (the time-boxed task) — confirm rivals differ or are silent.
5. THEN, and only then, commit the block with a git timestamp and flip to OPEN.

Until step 5, this stays BLOCKED. That is the honest state of the art on 2026-06-18.



## Current unblocking work plan (2026-06-25)

See also: `/mnt/d/Fundamentals/predictions/PRED-001-H8-Z3-STATUS-20260626.md` for the full H8/Z3 integration status report.

The phase selector remains the single machine PF must build to make a discriminating prediction. The closed routes (T-021, T-022, scalar/character, information-theoretic) are documented in `CLAIMS.md`. The active frontier is the H8/H_isometry/recurrence route in Lean (`PfLean.Axioms.lean`), which may constrain the structure of recurrence/stability enough to narrow the phase space.

### Next steps
1. **Complete the H8 circularity fix** — `Hypothesis_Coherence` now asserts recurrence + Lyapunov stability (non-circular). Finish the Lean equivalence proof and documentation corrections.
2. **Test the compact-recurrent-orbit conjecture** — Prove or disprove that H8 + H_isometry + H3 + H5 yields a compact recurrent orbit (Claude's quasi-periodic caveat: exact periodicity needs rationality; recurrence is the honest intermediate step).
3. **Bridge recurrence to degenerate_residue_forces_circulant** — If compact recurrence is proven, test whether it forces the J-I symmetry at D=3 through the eigenvalue structure.
4. **Map the phase selector** — If the above bridge closes, derive whether the recurrence frequency / rationality condition selects the Koide phase δ=2/9.
5. **Audit before prediction** — Codex hostile audit of any proposed phase selector; only then can PRED-001 flip from BLOCKED to OPEN.

### Owner
- DeepSeek owns the dependency-graph/phase-selector mathematics.
- Claude owns the Lean/H8/circularity documentation.
- Codex owns hostile audit.
- Devin (this instance) bridges findings into state files.

---
*(append-only resolution log below)*

## Resolution Log

### 2026-06-30 — PRED-001a falsified sub-pattern recorded

PRED-001 remains BLOCKED. A proposed sub-pattern, PRED-001a, is FALSIFIED by existing PMNS first-column data and must not be treated as a live prediction or as an unblocking result.

The rejected sub-pattern was mu/tau symmetry in the PMNS first column:
`|U_mu1|^2 = |U_tau1|^2 = 1/6`, corresponding to `[2/3, 1/6, 1/6]`.

Claude's archived 2026-06-22 note records measured central values `[0.678, 0.081, 0.241]`; mu1 and tau1 differ by roughly 3x. The close scalar `Q` value was a summary-statistic trap, not a valid prediction.

References:
- `/mnt/d/DeepSeek/inbox/ARCHIVE/2026-06-26/2026-06-22-claude-PRED001a-falsified-not-prediction.md`
- `/mnt/d/DeepSeek/REPORTS/DEEPSEEK_20260626_CROSS_SURFACE_TRUTH_TABLE.md`
- `/mnt/d/Codex/REPORTS/CODEX_20260630_CLAIMS_EXISTING_ROW_UPDATES_AUDIT.md`
