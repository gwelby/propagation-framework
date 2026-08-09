# PRED-002 — Neutrino Koide Universality (PF predicts NO)

> **STATUS: OPEN candidate / Codex HOLD on commitment (2026-07-24).** PF has a pre-registered position: neutrino masses do NOT satisfy the Koide relation Q=2/3 because neutrinos lack electromagnetic coupling, which PF identifies as the mechanism that locks the charged-lepton amplitude geometry. This is a falsifiable disagreement with Brannen/Rivero/ZiP-type rivals that extend Koide to neutrinos.
>
> **Codex HOLD (2026-07-24):** the cited DUNE/Hyper-K route does not measure the individual absolute masses needed for `Q_nu`. A revised absolute-mass transfer contract, uncertainty model, primary-source rival check, and canonical reproducible packet are required before re-audit or Greg lock. Report: `/mnt/d/Codex/REPORTS/CODEX_20260724_PRED_002_NEUTRINO_KOIDE_COMMITMENT_AUDIT.md`.

## Commitment block — *ready to lock once Greg/Codex approve the wording and error bar*
```
id:             PRED-002
status:         OPEN candidate (not yet git-locked)
committed:      — (awaiting Greg/Codex approval of exact wording)
committed_by:   Devin ∇λΣ∞ (Kimi K2.7) 2026-06-25
claim:          The PMNS lepton-sector Koide quality parameter Q_ν remains ≥5% away from
                the charged-lepton value Q_e = 2/3 as neutrino mass precision improves.
                Specifically: |Q_ν - 2/3| ≥ 0.033 for both normal and inverted orderings.
error_bar:      ±0.01 on Q_ν at DUNE/Hyper-K precision (target 2029–2033).
conditional_on:  Koide Q=2/3 is an electromagnetic-sector identity (ARGUED 0.70, not yet
                derived from Axioms 1-3); charged-lepton EM coupling locks the amplitude
                geometry; neutrinos interact only weakly and therefore lack this locking
                mechanism.
resolution:      DUNE + Hyper-Kamiokande precision measurement of absolute neutrino masses
                and the resulting Q_ν value. Window: 2029–2033.
sm_says:        SILENT — the SM has no prediction for the neutrino mass pattern or Q_ν.
rivals_say:     No known rival predicts standard Q_ν = 2/3 for neutrinos.
                Brannen (2006) predicts a SIGN-FLIPPED modified Koide relation
                (-√m₁+√m₂+√m₃)²/Σm = 3/2, which gives standard Q_ν = 0.52,
                NOT 2/3. Rivero reviews the framework but does not independently
                predict standard Q_ν = 2/3. ZiP (Buchanan 2025) predicts a
                different phase (δ_ν = -4/15) and inverted moment structure.
                All parties AGREE that standard Q_ν ≠ 2/3. The prediction is
                not discriminating against these rivals. The falsifier remains
                valid: if standard Q_ν is measured within 1% of 2/3, all
                frameworks (PF, Brannen, ZiP) are falsified.
                Primary sources: brannenworks.com/MASSES.pdf (2006),
                a.rivero.nom.es/research/koide.pdf, academia.edu/145881329.
                Full verification: PREDICTIONS/rival_verification_2026-08-09.md.
falsifier:      DUNE/Hyper-K measure Q_ν within 1% of 2/3 (i.e., |Q_ν - 2/3| < 0.0067)
                under either mass ordering.
```

## Why this is a real prediction

1. **PF has a mechanism claim**: Koide Q=2/3 is tied to electromagnetic coupling locking the amplitude geometry (`definitions/coherence.md`, `CLAIMS.md`).
2. **Neutrinos lack that mechanism**: They have no electric charge, so the locking mechanism is absent.
3. **Current data already supports PF**: PF's 2026-04-02 scan found Q_NO = 0.5496 (17.5% from 2/3) and Q_IO = 0.4790 (28.2% from 2/3) under current mass-squared-difference data. This is not a near-miss; it is a strong deviation.
4. **Rivals AGREE with PF on standard Q_ν**: Brannen's sign-flipped formula gives standard Q_ν = 0.52 (not 2/3). Rivero reviews but doesn't predict standard Q_ν = 2/3. ZiP predicts a different phase. The prediction is NOT discriminating against these rivals — all agree standard Q_ν ≠ 2/3. The falsifier (Q_ν within 1% of 2/3) would falsify ALL frameworks simultaneously. See `rival_verification_2026-08-09.md` for primary-source verification.

## Why this is not PRED-001

PRED-001 asks for the value of δ_CP from a PF-native phase selector. That machine does not exist; all selector routes failed. PRED-002 does not require a phase selector. It only requires PF's existing interpretation of Koide's EM-sector specificity, which is already documented and partially argued.

## What must happen before locking

- [ ] Codex hostile audit of the prediction wording and error bar.
- [ ] Greg approval to commit the block.
- [x] Verify the `rivals_say` entries against Brannen/Rivero/ZiP source documents. **DONE 2026-08-09** — rivals do NOT predict standard Q_ν = 2/3. See `rival_verification_2026-08-09.md`. `rivals_say` field corrected.
- [x] Confirm the current Q_ν computation is reproducible from `neutrino_koide_scan.py`. **DONE 2026-08-09** — MC run with 50K samples confirms Q_NO = 0.5458, Q_IO = 0.4754. See `pred002_mc_results.json`.

## Existing evidence

- `neutrino_koide_scan.py`
- `LOCAL_TEST_RESULTS_20260402.md`
- `papers/FALSIFICATION_PAPER_DRAFT.md` v0.3 TEST 2
- `CLAIMS.md` — Neutrino Koide non-universality row (EMPIRICAL 0.95)

---
*Append-only resolution log below.*

- **2026-08-07 (Claude):** Cross-reference — the 2026-08-06 "PRED-003" registrations
  (`pre_registrations/20260806T19001*Z_neutrino_koide_Q_*.json`, DeepSeek) commit THIS
  prediction's observable/mechanism in sharpened point-value form and are best read as
  candidate repair material for this HOLD, not a new PRED. Codex audited them at HOLD
  (`/mnt/d/Codex/REPORTS/CODEX_20260806_PRED003_NEUTRINO_KOIDE_PRE_REGISTRATION_AUDIT.md`);
  Claude's additive cross-audit (PRED-002 identity, Q(β) positivity domain, Σmν genericity,
  ledger divergence): `inbox/2026-08-07-claude-pred003-cross-audit-supplement.md`. HOLD unchanged.

- **2026-08-07 (DeepSeek):** Repair packet delivered (v2). Uncertainty corrected to window spread (Q_NO = 0.549622134 ± 0.023, Q_IO = 0.479016 ± 0.014; honest 2.6σ/6.7σ vs 2/3; canonical Q_NO = 0.549622134 — standardized everywhere, previous 0.549627 MC-mean inconsistency resolved). Transfer contract: m_lightest ∈ [1e-5, 3e-4] eV, argmin degeneracy admitted. Residual-flatness claim WITHDRAWN — referenced code not supplied (Codex re-audit PRED002-R5), same withdrawal as PRED-003. Mechanism evidence: KoideUnlocked.lean (build green, 0 sorries). Codex re-audit HOLD — residual flatness withdrawn, Q_NO reconciled, resolution log appended, KoideUnlocked.lean git-locked. Packet: `inbox/2026-08-07-deepseek-pred002-repair-packet.md`. HOLD unchanged.
