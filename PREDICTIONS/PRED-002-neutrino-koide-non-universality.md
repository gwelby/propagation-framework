# PRED-002 — Neutrino Koide Universality (PF predicts NO)

> **STATUS: OPEN candidate.** PF has a pre-registered position: neutrino masses do NOT satisfy the Koide relation Q=2/3 because neutrinos lack electromagnetic coupling, which PF identifies as the mechanism that locks the charged-lepton amplitude geometry. This is a falsifiable disagreement with Brannen/Rivero/ZiP-type rivals that extend Koide to neutrinos.

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
rivals_say:     Brannen/Rivero predict Q_ν ≈ 2/3 (normal ordering, m_3 ≈ 0.05 eV) via
                sign-flipped preon/Clifford phase mechanism. ZiP also extends Koide to
                neutrinos with a similar mechanism. This makes the disagreement clean.
falsifier:      DUNE/Hyper-K measure Q_ν within 1% of 2/3 (i.e., |Q_ν - 2/3| < 0.0067)
                under either mass ordering.
```

## Why this is a real prediction

1. **PF has a mechanism claim**: Koide Q=2/3 is tied to electromagnetic coupling locking the amplitude geometry (`definitions/coherence.md`, `CLAIMS.md`).
2. **Neutrinos lack that mechanism**: They have no electric charge, so the locking mechanism is absent.
3. **Current data already supports PF**: PF's 2026-04-02 scan found Q_NO = 0.5496 (17.5% from 2/3) and Q_IO = 0.4790 (28.2% from 2/3) under current mass-squared-difference data. This is not a near-miss; it is a strong deviation.
4. **Rivals explicitly disagree**: Brannen/Rivero predict neutrino Koide works with a sign-flip phase. This makes the test discriminating.

## Why this is not PRED-001

PRED-001 asks for the value of δ_CP from a PF-native phase selector. That machine does not exist; all selector routes failed. PRED-002 does not require a phase selector. It only requires PF's existing interpretation of Koide's EM-sector specificity, which is already documented and partially argued.

## What must happen before locking

- [ ] Codex hostile audit of the prediction wording and error bar.
- [ ] Greg approval to commit the block.
- [ ] Verify the `rivals_say` entries against Brannen/Rivero/ZiP source documents.
- [ ] Confirm the current Q_ν computation is reproducible from `neutrino_koide_scan.py`.

## Existing evidence

- `neutrino_koide_scan.py`
- `LOCAL_TEST_RESULTS_20260402.md`
- `papers/FALSIFICATION_PAPER_DRAFT.md` v0.3 TEST 2
- `CLAIMS.md` — Neutrino Koide non-universality row (EMPIRICAL 0.95)

---
*Append-only resolution log below.*
