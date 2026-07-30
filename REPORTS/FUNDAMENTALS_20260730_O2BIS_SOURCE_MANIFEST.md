# O2bis Source Manifest — Repair Against Codex HOLD

**Commit:** see the git revision that contains this file (`git rev-parse --verify HEAD`)  
**Ledger:** `clg_8d642db3f9d24a616f312922` (prior), `clg_de85188d6be71e28aa854159` (re-audit)  
**Date:** 2026-07-30  
**Agent:** Devin ∇λΣ∞

---

## Candidate source files (frozen in this commit)

| File | SHA-256 | Role |
|------|---------|------|
| `derivations/o2bis_analytic_kickstart_2026-07-29.md` | `992100fa34ccb5c407a6d2d8bfe47563542fdff1d2e3f5eebe859db76c8a4974` | Repair notes and claim tiers |
| `sandbox/o2bis_fast_regression.py` | `6041a2e0fc4b5dee776f353a98217bb94d74c9e193d4d932a96988a572816354` | Fast, exact, fail-closed regression gate (< 2 s) |
| `sandbox/o2bis_independent_verification.py` | `949086d653141e55607153024370f22a004b247104a3e1da3e5dcdef5c3f2f26` | Seeded MC integration/statistical check (~30 s fast, ~60 s full) |
| `sandbox/o2bis_cptp_completions.py` | `97d8a52b4c6a436a956bbd13b3f403c85d9d68ccccc2fee50b4d886380bf071a` | Fixed-orientation CPTP sweep + a-dependent counterexample |
| `sandbox/o2bis_instrument_probe.py` | `a9d2280bd5b7020e2f61d78896728aba72e6f8652e4c6253f48eae32dec23bd3` | Exact white-noise instrument (DeepSeek copy, byte-identical) |
| `sandbox/o2bis_cptp_channel.py` | `fdf92c7afe03292e64c43dc0d7e4c25ff265db09f1d4b1b48aca22d0b2c23ca5` | Exact Q→Q CPTP no-selection control (DeepSeek copy, byte-identical) |
| `CLAIMS.md` | `6a30ff19558f201a90c49a7df2dfee2b8fc5f36126e40963a1292cfcc2b4e985` | Live scoreboard row (paths corrected) |

## Known external files (not in this repo, exact hashes recorded)

| File | SHA-256 | Source |
|------|---------|--------|
| `/mnt/d/DeepSeek/sandbox/o2bis_instrument_probe.py` | `a9d2280bd5b7020e2f61d78896728aba72e6f8652e4c6253f48eae32dec23bd3` | DeepSeek workspace (mirrored above) |
| `/mnt/d/DeepSeek/sandbox/o2bis_cptp_channel.py` | `fdf92c7afe03292e64c43dc0d7e4c25ff265db09f1d4b1b48aca22d0b2c23ca5` | DeepSeek workspace (mirrored above) |
| `REPORTS/FUNDAMENTALS_20260730_O2BIS_CORRELATION_FUNCTIONAL_REPAIR.md` | `9c9e653b267f775a1b7124accafa34dd27c93748e1e20bedeb05aeeb1ba884bd` | Original repair report (superseded by V2) |
| `REPORTS/FUNDAMENTALS_20260730_O2BIS_CORRELATION_FUNCTIONAL_REPAIR_V2.md` | `59f126a906d888fb15de9f7c7b659d0d9866746cb4d1166c7f0e5f7aa5d046f1` | O2R-01..O2R-05 response and verification commands |
| `REPORTS/FUNDAMENTALS_20260730_O2BIS_SOURCE_MANIFEST.md` | `326abee8f96be384e866b4f0e32d5b9f025bce70e917133c0434d63bc6de14fc` | This manifest (self-referential; hash is pre-computed) |
| `REPORTS/CODEX_20260730_O2BIS_CORRELATION_FUNCTIONAL_0D85A8A_REAUDIT.md` | (frozen by Codex) | Codex hostile re-audit |

---

## Regression commands and expected outcomes

1. **Primary fast gate (exact, fail-closed):**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py
   ```
   Expected: `REGRESSION RESULT: N passed, 0 failed`, exit 0, wall time < 2 s.

2. **Negative control (proves gate is fail-closed):**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py --negative
   ```
   Expected: exactly one deliberate `FAIL`, exit 1.

3. **Seeded MC integration check (slower, not the fast gate):**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast
   ```
   Expected: `EXIT STATUS: 0 failure(s)`, exit 0; wall time ~30 s on this hardware.

4. **Negative control for the MC script:**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast --negative
   ```
   Expected: `EXIT STATUS: 20 failure(s)` (G formula doubled), exit 20.

5. **CPTP completions and exact instrument/channel:**
   ```bash
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_instrument_probe.py
   python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_channel.py
   ```
   Expected: prints exact tables, no assertions failed.

---

## Audit-item mapping

| Codex O2R | Repair in this commit |
|---|---|
| **O2R-01** regression fixture not fail-closed | New `o2bis_fast_regression.py` accumulates checks and exits non-zero on any failure; `--negative` deliberately corrupts one formula and proves the gate fails. `o2bis_independent_verification.py` also now increments `FAILURES` and exits with the count. |
| **O2R-02** competing-null exponent sign | `o2bis_independent_verification.py` now uses one convention everywhere: `decoh = C2 * (1-a)**m_fit`, with `m_fit` negative, and recomputes the displayed `R²` in log space. |
| **O2R-03** fixed-orientation conclusion asserted from examples | `o2bis_cptp_completions.py` and the derivation now list the tested constructions explicitly and label the class-wide statement as sampled evidence, not a theorem; no un-derived `admissible` claim. |
| **O2R-04** malformed row and source provenance | `CLAIMS.md` row uses absolute resolving paths, removes `admissible` language, and references the manifest. DeepSeek instrument/CPTP scripts are copied into `Fundamentals/sandbox/` so the next commit is self-contained. |
| **O2R-05** false bounded-runtime claim | `o2bis_fast_regression.py` is purely exact, runs in ~1.3 s. The MC script docstring no longer claims `< 5 s`; it is clearly labelled a statistical integration check. |

---

## Non-claims

- No claim that a physical selection principle forces `a=0`.
- No claim that the quantum instrument selects `a=0`.
- No claim that the `G(a)` power law is a transfer theorem.
- No claim that `τ_c` is derived from Axioms 1-3.
- No claim that the tested fixed-orientation constructions exhaust or prove the full class.
- No PUBLIC HOLD, release, outreach, or Greg boundary moves.

---

*Devin ∇λΣ∞ — 2026-07-30*
