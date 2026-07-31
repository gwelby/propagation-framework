# O2bis Source Manifest — Repair Against Codex HOLD

**Candidate commit bound by this manifest:** `47fdd30ae86d4cae56543858a3f809ce79282b6e`  
**Current git revision of this file:** use `git rev-parse --verify HEAD`  
**Ledger:** `clg_8d642db3f9d24a616f312922` (prior), `clg_de85188d6be71e28aa854159` (re-audit), `clg_3bb1fcbcc941a9ca6f11290a` (V2 re-audit)  
**Date:** 2026-07-30  
**Agent:** Devin ∇λΣ∞

---

## Candidate source files (frozen in commit 47fdd30)

| File | SHA-256 | Role |
|------|---------|------|
| `derivations/o2bis_analytic_kickstart_2026-07-29.md` | `992100fa34ccb5c407a6d2d8bfe47563542fdff1d2e3f5eebe859db76c8a4974` | Repair notes and claim tiers |
| `sandbox/o2bis_fast_regression.py` | `6041a2e0fc4b5dee776f353a98217bb94d74c9e193d4d932a96988a572816354` | Fast, exact, fail-closed regression gate |
| `sandbox/o2bis_independent_verification.py` | `949086d653141e55607153024370f22a004b247104a3e1da3e5dcdef5c3f2f26` | Seeded MC integration/statistical check |
| `sandbox/o2bis_cptp_completions.py` | `97d8a52b4c6a436a956bbd13b3f403c85d9d68ccccc2fee50b4d886380bf071a` | Fixed-orientation CPTP sweep + a-dependent counterexample |
| `sandbox/o2bis_instrument_probe.py` | `a9d2280bd5b7020e2f61d78896728aba72e6f8652e4c6253f48eae32dec23bd3` | Exact white-noise instrument (DeepSeek copy, byte-identical) |
| `sandbox/o2bis_cptp_channel.py` | `fdf92c7afe03292e64c43dc0d7e4c25ff265db09f1d4b1b48aca22d0b2c23ca5` | Exact Q→Q CPTP no-selection control (DeepSeek copy, byte-identical) |
| `CLAIMS.md` | `8b0f88772bcf283eae5c147c447241a32e607ba50bd42b7fd6a4a494d52589ac` | Live scoreboard row (delimiter and V2/V3 links corrected) |

## Known external files and audits (hashes recorded)

| File | SHA-256 | Source |
|------|---------|--------|
| `/mnt/d/DeepSeek/sandbox/o2bis_instrument_probe.py` | `a9d2280bd5b7020e2f61d78896728aba72e6f8652e4c6253f48eae32dec23bd3` | DeepSeek workspace (mirrored above) |
| `/mnt/d/DeepSeek/sandbox/o2bis_cptp_channel.py` | `fdf92c7afe03292e64c43dc0d7e4c25ff265db09f1d4b1b48aca22d0b2c23ca5` | DeepSeek workspace (mirrored above) |
| `REPORTS/FUNDAMENTALS_20260730_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V2.md` | `59f126a906d888fb15de9f7c7b659d0d9866746cb4d1166c7f0e5f7aa5d046f1` | V2 O2R-01..O2R-05 response and verification commands |
| `REPORTS/FUNDAMENTALS_20260731_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V3.md` | `68d14c7dc392433f6c7f1f7f8d533da8a3202e7516692acaf3545c69bb7fb7c3` | V3 addendum to V2 re-audit O2V2-01..O2V2-03 and packet gate |
| `REPORTS/CODEX_20260731_O2BIS_CORRELATION_FUNCTIONAL_V2_47FDD30_REAUDIT.md` | `ed0afe22c1661635574fdce621aec03a5a400211a2bfdfd6055142a542d2f0e7` | Codex V2 hostile re-audit |
| `Codex/inbox/2026-07-30_devin-o2bis-correlation-functional-reaudit-v2.md` | `c76a47f8722796f1ddd0727e1b26d22c8d2595c71e56c11bc5a416f304a23587` | V2 re-audit request |
| `Codex/inbox/2026-07-31_devin-o2bis-correlation-functional-reaudit-v3.md` | `79d7bac415e6de1d7e5611f81a9ee0879218a984ec4bb879b255b33a8f92f97a` | V3 gate-compliant re-audit request |

---

## Regression commands and expected outcomes

1. **Primary fast gate (exact, fail-closed):**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py
   ```
   Expected: `REGRESSION RESULT: N passed, 0 failed` and exit 0. Wall time is informational and depends on CPU availability.

2. **Negative control (proves gate is fail-closed):**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py --negative
   ```
   Expected: exactly one deliberate `FAIL` and exit 1.

3. **Seeded MC integration check (not the fast gate):**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast
   ```
   Expected: `EXIT STATUS: 0 failure(s)` and exit 0. Wall time is informational and depends on CPU availability.

4. **Negative control for the MC script:**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast --negative
   ```
   Expected: `EXIT STATUS: N failure(s)` with N > 0 and exit N.

5. **CPTP completions and exact instrument/channel:**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_instrument_probe.py
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_channel.py
   ```
   Expected: prints exact tables and exits 0.

---

## Runtime note

The exact gate is deterministic and contains no Monte Carlo. Its wall-clock time is environment-dependent and is not used as an acceptance criterion. Correctness is determined solely by exit code and the `passed/failed` summary. The seeded MC integration script is a separate, slower statistical check.

---

## Audit-item mapping

| Codex O2R / O2V2 | Repair in this manifest |
|---|---|
| **O2R-01** regression fixture not fail-closed | `o2bis_fast_regression.py` accumulates checks and exits non-zero on any failure; `--negative` deliberately corrupts one formula and proves the gate fails. `o2bis_independent_verification.py` also exits with its `FAILURES` count. |
| **O2R-02** competing-null exponent sign | `o2bis_independent_verification.py` uses `C2*(1-a)**m_fit` consistently and recomputes `R²` in log space. |
| **O2R-03** fixed-orientation conclusion over-claimed | `o2bis_cptp_completions.py` and the derivation list tested constructions and label the class-wide statement as sampled evidence. |
| **O2R-04 / O2V2-01** `CLAIMS.md` row and provenance | Row now starts with a single `|`, cites the V2 repair report, this manifest, and the V2 Codex re-audit. The manifest names the bound commit and records all hashes. |
| **O2R-05 / O2V2-03** runtime honesty | No hard wall-clock acceptance bound; exact gate correctness is by exit code only. |
| **O2V2-02** manifest self-hash | Self-hash row removed; the bound commit is named literally and the current revision can be read from git. |

---

## Non-claims

- No claim that a physical selection principle forces `a=0`.
- No claim that the quantum instrument selects `a=0`.
- No claim that the `G(a)` power law is a transfer theorem.
- No claim that `τ_c` is derived from Axioms 1-3.
- No claim that the tested fixed-orientation constructions exhaust or prove the full class.
- No movement of PUBLIC HOLD, release, outreach, or Greg boundaries.

---

*Devin ∇λΣ∞ — 2026-07-30*
