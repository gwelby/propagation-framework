# PREDICTIONS/ — The Forward-Prediction Ledger
*Created 2026-06-18. This is the structure that guides the family from postdiction to truth. Born from the demotion audit + the `framework-toward-true` sweep (5 maps → synthesis → 3 adversarial cooling lenses). Read `../UNDENIABLE_ROADMAP.md` first.*

## Why this exists (the diagnosis)
The family kept drifting back to overclaiming **not from dishonesty but from structure.** The scoreboard was `CLAIMS.md` — a count of "how many known constants did we derive." That metric **has no wrong answer**: you can always find another combination, and every promotion looks like progress. Postdiction of things we already know cannot falsify you, so it drifts toward overclaim forever. Exhortation ("be honest") failed because it never changed the scoreboard.

**This ledger changes the scoreboard.** From *"how many constants did we match?"* (unfalsifiable) to *"what did we commit to BEFORE the experiment, and did it land?"* (failure is possible → success means something). A framework that can be wrong and isn't is undeniable. A framework that can't be wrong is just elegant.

`CLAIMS.md` is hereby **supporting evidence**, not the claim. The claim is what's in this ledger.

## The hard truth this ledger must hold (2026-06-18)
**PF cannot make a discriminating forward prediction today.** Verified by the sweep:
- δ = 2/9 (the Koide phase) is a **postdiction** (read off data; every PF-native selector route — T-021, T-022, 4 audit lanes — FAILED) **and DEGENERATE** (rivals ZiP/Brannen/Rivero also land on ~2/9). Committing it would not count and would not distinguish PF.
- Every other candidate (neutrino ordering, Σmν, δ_CP, 3-generations, dark matter) fails the test **"can PF compute a number today?"** — No.
- So the first ledger entry is not a prediction. It is the **one machine to build** (a PF-native phase selector), logged honestly as **BLOCKED**, so the family cannot mistake an aspiration for a commitment.

That negative result IS the deliverable. The honest map of where the framework actually stands is worth more than a fake number.

## Entry schema (commitment block = git-timestamp-LOCKED, never edited)
```
id:             PRED-NNN
status:         OPEN | BLOCKED | RESOLVED-HIT | RESOLVED-MISS | DEGENERATE | WITHDRAWN
committed:      <git commit timestamp — the lock; you cannot pre-date>
committed_by:   <agent> @ <commit SHA>
claim:          a NUMBER or functional-form + the parameter to be fixed (vague claims REJECTED)
error_bar:      explicit (e.g. "<3σ vs PDG best-fit")
conditional_on: EVERY unresolved premise named (Postulate D; EM-sector-specificity; …)
resolution:     a REAL planned measurement + date window (must be able to resolve)
sm_says:        "silent" | a specific SM value
rivals_say:     each named rival's number — OR a time-boxed task to find them (NOT "assumed different")
falsifier:      the exact observation that kills it
--- (everything below this line is append-only resolution log) ---
```

## Anti-gaming rules (from the cooling pass — these are what make it stick)
1. **Number-or-form, never prose.** "PF predicts normal ordering" with no error bar is REJECTED. A claim must be falsifiable by a measurement.
2. **The git timestamp is the lock.** Like clinical-trial pre-registration — you cannot back-date a commitment. The commitment block is never edited; resolution only appends.
3. **`conditional_on` is mandatory at the point of maximum temptation.** Every inherited premise (Postulate D especially) must be named at the prediction site, or it doesn't land.
4. **`rivals_say` empty → DEGENERATE-risk flag.** If you haven't found what rivals predict, it's a time-boxed task, not an assumption. If all rivals give the same number → **DEGENERATE** (lands but doesn't distinguish PF → does not count toward undeniability).
5. **BLOCKED ≠ OPEN.** A prediction contingent on machinery that doesn't exist is BLOCKED, never OPEN. The family must not mistake "we could predict this IF we build X" for "we predict this."
6. **Clock-enforced, or it dies like the claim-guard.** A periodic check (Pi/cron) surfaces OPEN entries nearing their resolution window and BLOCKED entries with their blocker — so the ledger cannot be quietly forgotten. *Resolution is enforced by a clock the family does not control.* This is the single property that keeps it from becoming another orphaned file.

## Status today
- `PRED-001` — δ_CP via a PF-native phase selector — **BLOCKED** (the machine doesn't exist; 4 derivation routes failed). Status report: `/mnt/d/Fundamentals/predictions/PRED-001-H8-Z3-STATUS-20260626.md`.
- `PRED-002` — Neutrino Koide non-universality — **OPEN candidate / Codex HOLD on commitment**. The 2026-07-24 audit finds that the cited DUNE/Hyper-K route does not measure the individual absolute masses needed for `Q_nu`; the prediction needs an evidence-backed absolute-mass transfer contract, uncertainty propagation, verified rivals, and one canonical reproducible packet before re-audit or Greg lock. Report: `/mnt/d/Codex/REPORTS/CODEX_20260724_PRED_002_NEUTRINO_KOIDE_COMMITMENT_AUDIT.md`.
- The day a PRED entry goes OPEN with a real number, a named experiment, and rivals_say filled in differing — that is the day PF stops being numerology and becomes physics.

---

## PRED-002 Absolute-Mass Transfer Contract (DRAFT — for Codex re-audit)

*Drafted 2026-08-03 by Devin (∇λΣ∞). This section addresses Codex HOLD items 1–2
of the 2026-07-24 audit (evidence-backed absolute-mass channel + transfer
contract with uncertainty propagation). It does NOT change PRED-002 status from
HOLD. Status change requires a new Codex audit. See
`/mnt/d/Codex/REPORTS/CODEX_20260724_PRED_002_NEUTRINO_KOIDE_COMMITMENT_AUDIT.md`.*

### A. Experiments that provide m_lightest

PRED-002's observable is the neutrino Koide quality parameter
`Q_ν = (m₁ + m₂ + m₃) / (√m₁ + √m₂ + √m₃)²`. Computing `Q_ν` requires the
three individual absolute masses, which are NOT directly measured by any single
experiment. They are reconstructed from (i) oscillation mass-squared differences
Δm²₂₁, Δm²₃₁ (measured by long-baseline/reactor experiments) and (ii) a single
absolute-mass anchor `m_lightest`. The three experimental channels that constrain
`m_lightest` are:

| Channel | Observable measured | How m_lightest is extracted | Current sensitivity | Projected sensitivity |
|---------|-------------------|-----------------------------|---------------------|-----------------------|
| **KATRIN** (direct β decay) | `m_β = √(Σᵢ |U_ei|² mᵢ²)` (effective electron-neutrino mass) | Invert via ordering + Δm² to bound m_lightest | m_β < 0.45 eV (90% CL, 2024) | m_β ~ 0.2 eV (final); next-gen ~0.04 eV |
| **Cosmology** (CMB-S4, DESI, Euclid) | `Σmν = m₁ + m₂ + m₃` | Combined with Δm² + ordering → m_lightest | Σmν < 0.12 eV (Planck 2018); CMB-S4 target σ(Σmν) ~ 0.04 eV | Σmν < 0.06 eV (2σ, CMB-S4 ~2030) |
| **0νββ** (nEXO, LEGEND-1000) | `m_ββ = |Σᵢ U²_ei mᵢ|` (effective Majorana mass) | Invert via ordering + Δm² + Majorana phase to bound m_lightest | m_ββ < 0.08–0.18 eV (current, isotope-dependent) | m_ββ ~ 0.01–0.02 eV (nEXO/LEGEND-1000, ~2032) |

**Key honesty point (from Codex audit):** None of these channels measures
`m_lightest` directly. Each measures a different effective mass combination.
`m_lightest` is inferred by combining the measured observable with oscillation
Δm² values and a mass-ordering assumption. The inference is model-dependent
(ordering choice, Majorana phase for 0νββ, cosmological priors for Σmν). The
transfer contract below makes this explicit.

**Resolution window:** The earliest channel capable of constraining m_lightest
at the precision needed to test Q_ν meaningfully is CMB-S4 (Σmν sensitivity
~0.04 eV, data ~2028–2030). KATRIN's final sensitivity (~0.2 eV on m_β) is
insufficient to distinguish the Q_ν band from 2/3 at the |Q_ν − 2/3| ≥ 0.033
level, because at m_lightest ≲ 0.05 eV the Q_ν values (Q_NO ≈ 0.55, Q_IO ≈ 0.48)
are already far from 2/3 and the question is whether m_lightest could be large
enough to push Q_ν toward 2/3. The critical regime is m_lightest ≲ 0.1 eV, where
CMB-S4 and 0νββ are the discriminating channels.

### B. Uncertainty model: oscillation Δm² → absolute masses

Given `m_lightest` (from any channel above) and the oscillation mass-squared
differences (from NuFIT 6.0 or successor), the individual masses are:

**Normal ordering (NO):** m₁ = m_lightest is the lightest state.
```
m₁ = m_lightest
m₂ = √(m_lightest² + Δm²₂₁)
m₃ = √(m_lightest² + Δm²₃₁)
```

**Inverted ordering (IO):** m₃ = m_lightest is the lightest state.
```
m₃ = m_lightest
m₁ = √(m_lightest² + |Δm²₃₁|)
m₂ = √(m_lightest² + |Δm²₃₁| + Δm²₂₁)
```

**Uncertainty propagation (Gaussian, first-order):**

The Koide parameter is `Q_ν = Σmᵢ / (Σ√mᵢ)²`. Its uncertainty has two
independent sources:

1. **Oscillation inputs** (Δm²₂₁, Δm²₃₁): Propagated via the Jacobian
   `∂Q_ν/∂(Δm²_ij)`. At m_lightest → 0 (the current-favored regime), Q_ν is
   dominated by the ratio Δm²₂₁/Δm²₃₁ and is insensitive to the absolute scale.
   The NuFIT 6.0 uncertainties are σ(Δm²₂₁) ≈ 0.20×10⁻⁵ eV²,
   σ(Δm²₃₁) ≈ 0.034×10⁻³ eV². At m_lightest = 0.0001 eV these yield
   σ(Q_ν) ≈ 0.002 (NO) and σ(Q_ν) ≈ 0.003 (IO) — well below the 0.033 band.

2. **m_lightest** (from KATRIN/CMB-S4/0νββ): This is the dominant uncertainty
   source. Q_ν varies with m_lightest: at m_lightest → 0, Q_NO ≈ 0.550 and
   Q_IO ≈ 0.479; as m_lightest increases, both drift toward 2/3 (Q_NO crosses
   2/3 near m_lightest ≈ 0.035 eV for NO, Q_IO approaches but does not reach 2/3
   within the Σmν < 0.12 eV bound). The m_lightest uncertainty from CMB-S4
   (σ(Σmν) ~ 0.04 eV → σ(m_lightest) ~ 0.013 eV) maps to σ(Q_ν) ~ 0.02–0.04
   depending on ordering and central value. **This is the uncertainty that
   determines whether the |Q_ν − 2/3| ≥ 0.033 band is resolvable.**

**Null model (SM-silent baseline):** The Standard Model has no prediction for
the neutrino mass pattern or Q_ν. The null hypothesis is that Q_ν takes whatever
value the measured masses give — there is no SM value to test against. The
prediction is PF-specific: PF claims Q_ν ≠ 2/3 because the EM-locking mechanism
that enforces Koide in the charged sector is absent for neutrinos.

**Current scan values (reproduced from `sandbox/neutrino_koide_scan.py`):**

| Ordering | m_lightest (eV) | Q_ν | |Q_ν − 2/3| |
|----------|----------------|-----|------------|
| NO | 0.0001 (scan floor) | 0.549622134 | 0.1170 |
| IO | 0.0001 (scan floor) | 0.479016 | 0.1877 |

**Caveat (from Codex audit item 4):** These values are computed at the scan
floor `m_lightest = 0.0001 eV`, which is a boundary value, not a measurement.
The transfer contract must separate the current scan result (a postdiction under
an unmeasured-mass assumption) from any future experimental commitment. The
lightest-mass prior must be stated explicitly in the locked commitment.

### C. Rival check: UGP mass-squared ratio vs PF Q_ν

**UGP predicts** Δm²₂₁/Δm²₃₁ = 0.0294 (parameter-free, from GF(7) arithmetic).
NuFIT 6.0 gives 0.02951 ± 0.00098, so UGP lands at 0.11σ — a strong postdiction
or near-postdiction.

**PF does NOT predict the mass-squared ratio.** PF takes Δm²₂₁ and Δm²₃₁ as
measured inputs (from NuFIT/PDG), not as derived quantities. The PF scan uses
PDG 2024 values (Δm²₂₁ = 7.53×10⁻⁵, Δm²₃₁ = 2.453×10⁻³), giving a ratio of
0.03070 — which is 1.21σ from NuFIT 6.0. This is an input-data choice, not a PF
prediction.

**PF's observable is different:** PF predicts Q_ν ≠ 2/3 (Koide non-universality
in the neutrino sector). UGP predicts the mass-squared ratio. These are
**different observables** — they are not a direct head-to-head. Both could be
correct simultaneously. The transfer contract notes this explicitly to avoid
false discrimination claims.

**What PF would need to compete with UGP on the ratio:** A PF-native derivation
of Δm²₂₁/Δm²₃₁ from the propagation axioms. This does not currently exist. If
built, it would be a separate prediction (PRED-003 candidate), not a repair of
PRED-002. The mass-squared ratio is an INPUT to PRED-002's Q_ν calculation, not
its output.

**Implication for the transfer contract:** The locked commitment must specify
which Δm² values are used (NuFIT 6.0 recommended over PDG 2024 for consistency
with UGP's comparison baseline) and must note that these are measured inputs,
not PF predictions. If UGP's predicted ratio (0.0294) is used instead of NuFIT
6.0 (0.02951), the Q_ν values shift by < 0.002 — negligible compared to the
0.033 band. The rival check is therefore: UGP competes on the ratio; PF competes
on Q_ν; they are orthogonal.

### D. Pre-registration hash template

Before any new experimental data (CMB-S4, nEXO, LEGEND-1000, or KATRIN final)
is public, the prediction must be committed to a SHA-256 hash and timestamped.
The hash locks the commitment block, the transfer contract, the Δm² input
values, and the reproduction script.

**Template:**
```
PRED-002 PRE-REGISTRATION HASH
================================
committed_at:   <ISO 8601 UTC timestamp>
committed_by:   <agent> @ <git commit SHA>
locked_fields:
  claim:        |Q_ν - 2/3| ≥ 0.033 for both NO and IO
  error_bar:    σ(Q_ν) from m_lightest uncertainty (channel-specific)
  Δm²_inputs:   NuFIT 6.0 (or named successor)
  ordering:      both NO and IO tested independently
  transfer:      this contract (Section B)
  rivals:        Brannen/Rivero/ZiP (Q_ν ≈ 2/3) — primary-source verified
                UGP (Δm²₂₁/Δm²₃₁ = 0.0294) — orthogonal observable, noted
  falsifier:    |Q_ν - 2/3| < 0.0067 under either ordering
  script:        sandbox/neutrino_koide_scan.py @ <git blob SHA>
hash:           SHA-256(<all locked_fields concatenated>)
```

**Procedure (mirrors UGP's α_s pre-registration):**
1. Concatenate all `locked_fields` values into a single string.
2. Compute `SHA-256(string)`.
3. Commit the hash to git with the timestamp.
4. Publish the hash (not the full content) before the resolving experiment
   releases data.
5. After data is public, reveal the full content and verify the hash matches.

**This hash is NOT yet computed.** It will be computed when the commitment block
is finalized and Codex re-audit passes. The template above is the structure that
will be filled.

### Remaining HOLD items (not addressed by this contract)

This transfer contract addresses Codex audit items 1–2 (absolute-mass channel +
transfer contract). The following items remain OPEN before re-audit:

- [ ] **Item 3:** Commit a single numeric condition the named channel can
      actually resolve, with uncertainty source cited. (The |Q_ν − 2/3| ≥ 0.033
      band must be checked against CMB-S4's σ(m_lightest) to confirm
      resolvability.)
- [ ] **Item 4:** Make the lightest-mass assumption explicit and separate the
      current scan result from the future commitment. (Partially addressed in
      Section B caveat; needs formal separation in the locked block.)
- [ ] **Item 5:** Verify `rivals_say` against primary sources (Brannen/Rivero/
      ZiP). The UGP rival check (Section C) is verified from
      `competitor_comparison_2026-08-02.md`; Brannen/Rivero/ZiP need
      primary-source verification.
- [ ] **Item 6:** Restore one canonical packet path and a minimal
      dependency-checked reproducibility command. (`neutrino_koide_scan.py`
      currently fails without matplotlib; a stdlib-only reproduction path is
      needed.)

---

## PRED-002 Resolution Log — 2026-08-07 (Repair Status)

**Date:** 2026-08-07
**Agent:** Devin ∇λΣ∞
**Re:** PRED-002 repair per Codex re-audit `CODEX_20260807_PRED_002_REPAIR_REAUDIT.md`

### Items addressed

| Re-audit item | Status | Action |
|---|---|---|
| PRED002-R4 (Q_NO consistency) | **FIXED** | Q_NO standardized to 0.549622134 (the independently recomputed scan value) in all surfaces: `pre_registrations/20260806T190015Z_neutrino_koide_Q_NO.json` (expected_value updated from 0.549622 to 0.549622134), `README.md` scan table, `PRED-002-neutrino-koide-non-universality.md`, and repair packet. The 0.549627 MC-mean inconsistency is resolved. |
| PRED002-R5 (flatness unreproducible) | **FIXED** | Residual-flatness claim WITHDRAWN — "referenced code not supplied" note added to repair packet (`Codex/inbox/2026-08-07-deepseek-pred002-repair-packet.md` §2) and to `PRED-002-neutrino-koide-non-universality.md` resolution log. Same withdrawal treatment as PRED-003 (PRED003-04). |
| PRED002-R6 (resolution-log append) | **FIXED** | This entry. Appended 2026-08-07 to `PREDICTIONS/README.md` recording the PRED-002 repair status. |
| PRED002-R7 (git lock on Lean file) | **FIXED** | `Fundamentals/lean/PfLean/KoideUnlocked.lean` git-added and committed with this change set. |

### Pre-registration hash

The pre-registration hash template (Section D above) remains NOT yet computed. The hash will be computed when the commitment block is finalized and Codex re-audit passes. The R7 git lock on `KoideUnlocked.lean` is a necessary prerequisite; the hash computation itself awaits full Codex PASS.

### PRED-003 sigma denominator clarification (Finding 7)

Both pre-registration JSON records (`20260806T190015Z_neutrino_koide_Q_NO.json`, `20260806T190020Z_neutrino_koide_Q_IO.json`) now include a `sigma_denominator` field explicitly stating the denominator used for the σ estimate: `full_window_spread (0.045 eV = 2 × half-spread ±0.023 eV)` for NO and `full_window_spread (0.028 eV = 2 × half-spread ±0.014 eV)` for IO. Notes updated to state unambiguously that the σ is computed against the full window spread, NOT the uncertainty field (half-spread). The IO notes copy-paste error (stated ±0.023 instead of ±0.014) is also corrected.

### Status after repair

PRED-002 remains **OPEN candidate / Codex HOLD on commitment**. These repairs address packaging defects R4–R7 from the 2026-08-07 re-audit. The substantive HOLD items ( Items 3–6 from the 2026-07-24 audit) remain OPEN. Re-audit required before Greg lock.
