# PREDICTION LEDGER — STATUS (auto-generated; do not hand-edit)
*Generated 2026-08-14 15:13 UTC by `System/tools/prediction_ledger_check.py`.*
*Reads BOTH narrative `PRED-*.md` entries and hash-committed `pre_registrations/*.json` records. Read-only over the JSON: hashes bind them.*

**Forward predictions OPEN: 2** · self-tests: 2 · unclassified: 0 · md-entries: 2 (OPEN 0 / candidate 1 / blocked 1)

> ✅ 2 hash-committed forward prediction(s) on file. The framework can be wrong — which is the point.
>
> **Read this narrowly.** A hash-committed pre-registration is a commitment by its
> *author* at a *timestamp*. It is NOT an audit clearance and NOT a family lock.
> Governance status (Codex audit verdict, Greg lock) lives in `CLAIMS.md`, the
> narrative `PRED-*.md` entry, and `/mnt/d/Codex/REPORTS/`. A record can be validly
> hash-committed and simultaneously under an audit HOLD — check before citing.

---

## Forward predictions (OPEN — these can fail)

### neutrino_koide_Q_NO
- expected: `0.549622134` · committed 2026-08-07 by Devin ∇λΣ∞ @ f3be9adf8c7f582f9e6d8658509578cfaa880aae
- record: `pre_registrations/20260806T190015Z_neutrino_koide_Q_NO.json` · hash `a78a91284f55…`
- classified FORWARD because: resolution names a future/ongoing experiment

### neutrino_koide_Q_IO
- expected: `0.479016` · committed 2026-08-07 by Devin ∇λΣ∞ @ f3be9adf8c7f582f9e6d8658509578cfaa880aae
- record: `pre_registrations/20260806T190020Z_neutrino_koide_Q_IO.json` · hash `c04df84a8d82…`
- classified FORWARD because: resolution names a future/ongoing experiment

## Self-tests (postdictions — cannot fail forward)

- **koide_Q_charged_leptons** — expected `0.6666666666666666` · `20260803T125022Z_koide_Q_charged_leptons.json` · notes declare a self-test
- **koide_Q_charged_leptons** — expected `0.6666666666666666` · `20260807T022735Z_koide_Q_charged_leptons.json` · notes declare a self-test

## Narrative ledger entries (`PRED-*.md`)

### [BLOCKED] PRED-001-delta-cp-phase-selector
- status line: BLOCKED
- claim: [BLOCKED] a specific value for the PMNS leptonic CP phase δ_CP, output by a PF-native phase selector — NOT YET COMPUTABLE
- resolution: DUNE + Hyper-Kamiokande, δ_CP at multi-σ, ~2029–2033 (feasible window)
- ⛳ blocker: PF has **no machinery to compute δ_CP today.** The prerequisite is a **PF-native phase selector** — a derivation, from Axioms 1-3 (or an explicitly-named minimal added premise), of *why* the Koide pha

### [CANDIDATE] PRED-002-neutrino-koide-non-universality
- status line: OPEN candidate (not yet git-locked)
- ⓘ not locked — does not count as a forward prediction until it is
- claim: The PMNS lepton-sector Koide quality parameter Q_ν remains at least 0.033 away from the charged-lepton value Q_e = 2/3 as neutrino mass precision improves. Specifically: |Q_ν - 2/3| ≥ 0.033 for both normal and inverted orderings. (0.033 = 4
- resolution: CMB-S4 + DESI BAO measurement of Σm_ν (σ = 15 meV, Abazajian et al. 2016). Transfer contract: Σm_ν + oscillation data (Δm²₂₁, Δm²₃₁) + ordering → m_lightest → individual masses → Q_ν. If Σm_ν < 58 meV

## Companion reports (not ledger entries)

- `PRED-001-H8-Z3-STATUS-20260626` — PRED-001 H8/Z3 Integration Status Report

---

## ⚠ Integrity flags

- ~~`20260806T190015Z_neutrino_koide_Q_NO.json`: claims PRED-003 in notes~~ **RESOLVED 2026-08-16:** notes field corrected from "PRED-003" to "PRED-002". Content hash recomputed. PRED-003 is reserved for the Δm² ratio derivation (not yet built).
- ~~`20260806T190020Z_neutrino_koide_Q_IO.json`: claims PRED-003 in notes~~ **RESOLVED 2026-08-16:** same correction as above.

---

## What this surface is for

The scoreboard that matters: what did we commit to BEFORE the measurement, and did it land?
The scoreboard that doesn't: how many known constants we matched after the fact.

*Ledger dir: `/mnt/d/Fundamentals/PREDICTIONS` · protocol: `PREDICTIONS/README.md` · mirror written to `/mnt/d/Pi/REPORTS/prediction_ledger_STATUS.md`.*