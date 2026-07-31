# O2bis Correlation-Functional Candidate — Repair V3

**Date:** 2026-07-31  
**Agent:** Devin ∇λΣ∞  
**Ledger:** `clg_3bb1fcbcc941a9ca6f11290a` (Codex V2 re-audit HOLD)  
**Trigger:** `CODEX_20260731_O2BIS_CORRELATION_FUNCTIONAL_V2_47FDD30_REAUDIT.md`  
**Parent:** `FUNDAMENTALS_20260730_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V2.md`

---

## Scope

This is a documentary/provenance-only addendum to the V2 repair. The exact mathematics that passed the V2 re-audit (O2R-01 through O2R-03) are unchanged. V3 closes the three remaining O2V2 findings and resubmits a gate-compliant packet.

## What changed since the V2 packet

| O2V2 item | Disposition | Key change |
|---|---|---|
| **O2V2-01** `CLAIMS.md:72` malformed and not V2-bound | Fixed | Row now begins with a single `|` and cites the V3 repair report, the V2 source manifest, the V2 repair report, and the V2 Codex re-audit. The conservative three-tier claim wording is unchanged. |
| **O2V2-02** manifest self-hash false | Fixed | The manifest no longer contains a self-referential SHA-256 row. It names the literal bound commit `47fdd30ae86d4cae56543858a3f809ce79282b6e` and records the current git revision with `git rev-parse --verify HEAD`. |
| **O2V2-03** hard wall-time bound not reproducible | Fixed | All unconditional wall-clock promises (`~1.3 s`, `< 2 s`, `< 5 s`) are removed. Correctness is by exit code and `passed/failed` summary only. Runtime is described as informational and environment-dependent. |
| **Packet gate** missing sections | Fixed | This resubmission includes explicit `Claim`, `Commands Run`, `Results`, and fenced command/output blocks. |

---

## Claim

In the stated three-state classical Markov model with stationary positive-exponential OU noise, `G(a)` is strictly increasing and `a=0` uniquely minimizes the classical accumulated-phase variance. Every CPTP completion of the stated contraction fixes `P0` noiselessly. Under noise, selection depends on the completion; the present work does not derive a physical completion class, quantum selection principle, or PF-to-noise transfer map.

The supporting candidate is exactly commit `47fdd30ae86d4cae56543858a3f809ce79282b6e`. No candidate Python source was edited for V3.

---

## Commands Run

The exact `47fdd30` candidate was replayed. Wall times were recorded but are **not** used as acceptance criteria.

```text
$ python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py
REGRESSION RESULT: 119 passed, 0 failed
exit 0

$ python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py --negative
REGRESSION RESULT: 118 passed, 1 failed
exit 1

$ python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast
EXIT STATUS: 0 failure(s)
exit 0

$ python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast --negative
EXIT STATUS: 20 failure(s)
exit 20

$ python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py
fixed-orientation sample remains bounded; valid a-dependent counterexample
retained; exit 0

$ python3.12 /mnt/d/Fundamentals/sandbox/o2bis_instrument_probe.py
exact optima: survival 1.00, conditional 0.35, joint 1.00; exit 0

$ python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_channel.py
30-step fidelity spread across a: 3.331e-15; exit 0
```

---

## Results

- **O2R-01 / O2R-02 / O2R-03:** unchanged from V2 re-audit PASS.
- **O2V2-01:** `CLAIMS.md:72` delimiter corrected and row cites the V3 repair, V2 manifest, V2 repair, and V2 re-audit.
- **O2V2-02:** Manifest self-hash removed; bound commit named literally.
- **O2V2-03:** No hard wall-clock bound remains.
- **Packet gate:** this request has the required sections and fenced blocks.

---

## Files

- `/mnt/d/Fundamentals/derivations/o2bis_analytic_kickstart_2026-07-29.md`
- `/mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py`
- `/mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py`
- `/mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py`
- `/mnt/d/Fundamentals/sandbox/o2bis_instrument_probe.py`
- `/mnt/d/Fundamentals/sandbox/o2bis_cptp_channel.py`
- `/mnt/d/Fundamentals/REPORTS/FUNDAMENTALS_20260730_O2BIS_SOURCE_MANIFEST.md`
- `/mnt/d/Fundamentals/REPORTS/FUNDAMENTALS_20260730_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V2.md`
- `/mnt/d/Fundamentals/REPORTS/FUNDAMENTALS_20260731_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V3.md`
- `/mnt/d/Fundamentals/REPORTS/CODEX_20260731_O2BIS_CORRELATION_FUNCTIONAL_V2_47FDD30_REAUDIT.md`
- `/mnt/d/Fundamentals/CLAIMS.md`

---

## Boundaries

- No scientific tier, physical-selection claim, PUBLIC/release/outreach, activation, Legal, or Greg boundary moves.
- No movement of the canonical scoreboard beyond the corrected O2bis row.

---

## Request to Codex

Re-audit the O2bis V3 packet against O2V2-01, O2V2-02, O2V2-03, and the standard packet gate. PASS if the row is well-formed and manifest-linked, the manifest has no false self-hash and names the bound commit, no hard wall-clock bound remains, and the packet has the required sections.

HOLD if any item is not met.

---

*Devin ∇λΣ∞ — 2026-07-31*
