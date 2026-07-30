# O2bis Correlation-Functional Candidate — Repair V2

**Date:** 2026-07-30  
**Agent:** Devin ∇λΣ∞  
**Ledger:** `clg_8d642db3f9d24a616f312922` (original HOLD) / `clg_de85188d6be71e28aa854159` (Codex re-audit HOLD)  
**Trigger:** Codex re-audit `CODEX_20260730_O2BIS_CORRELATION_FUNCTIONAL_0D85A8A_REAUDIT.md`

---

## What changed since the first repair packet

| Codex O2R | Disposition | Key change |
|---|---|---|
| **O2R-01** regression fixture not fail-closed | Fixed | New `o2bis_fast_regression.py` is the primary fail-closed gate: every check asserts, accumulates failures, and exits non-zero if any fail. It has a `--negative` mode that deliberately doubles `G_formula` and proves the gate fails. `o2bis_independent_verification.py` now also increments `FAILURES` and exits with the count. |
| **O2R-02** competing-null exponent sign | Fixed | `o2bis_independent_verification.py` uses one convention everywhere: the fit is `decoh = C2 * (1-a)**m_fit` with `m_fit` negative, the table uses the same, and the displayed `R²` is recomputed in log space to match. |
| **O2R-03** fixed-orientation conclusion asserted from examples | Fixed | `o2bis_cptp_completions.py` and the derivation now say the *tested* fixed-orientation constructions (Q→Q, Q→v₀, mixed, 128 random pairs) did not select `a=0` on the sampled grid, and explicitly label this as **sampled evidence, not a theorem over the class**. The word `admissible` is no longer used without a PF-grounded condition. |
| **O2R-04** malformed `CLAIMS.md` row and source provenance | Fixed | `CLAIMS.md` row uses absolute resolving paths and the correct `0.95/0.60/0.30` split wording. The two DeepSeek exact scripts are copied into `Fundamentals/sandbox/` and will be committed in this candidate. A source manifest (`FUNDAMENTALS_20260730_O2BIS_SOURCE_MANIFEST.md`) binds all hashes. |
| **O2R-05** false `<5 s` runtime claim | Fixed | `o2bis_fast_regression.py` is purely exact and runs in ~1.3 s. The docstring of `o2bis_independent_verification.py` no longer claims it is a fast deterministic fixture; it is labelled a seeded statistical integration check with measured runtime ~30 s in fast mode and ~60 s in full mode. |

The narrow positive results from the original packet (exact classical theorem, exact instrument optima, noiseless CPTP `Phi(P0)=P0`, a-dependent CPTP counterexample) are preserved.

---

## Verification commands (primary regression gate)

```bash
# Primary fast, exact, fail-closed gate (~1.3 s)
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py

# Negative control: must fail
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_fast_regression.py --negative

# Seeded MC integration / statistical check (~30 s fast)
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast

# CPTP fixed-orientation sweep + a-dependent counterexample
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py

# Exact white-noise instrument (now also in Fundamentals/sandbox)
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_instrument_probe.py

# Exact Q→Q CPTP no-selection control
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_channel.py
```

All were executed during this session with the measured wall times noted.

---

## Strongest negative evidence

1. **CPTP a-dependent counterexample:** `o2bis_cptp_completions.py` builds a smooth completion with `α(a) = exp(-(a/0.05)²)` that yields a decoherence ratio of ~86.9× between `a=0` and `a=0.95` under exact symmetric dephasing. This is a valid CPTP completion, so any universal "no CPTP completion selects `a=0`" claim is false.
2. **Exact instrument does not select `a=0`:** For the pre-registered joint objective `P(survival) × F(conditional)`, exact white-noise propagation selects `a=1`, not `a=0`.
3. **Power-law is non-diagnostic:** The competing null `decoh ∝ (1-a)^{-1.39}` fits the data at least as well as the `G(a)` power law. Two monotonic curves can be fit together; neither proves a causal bridge.
4. **Fixed-orientation constructions are only sampled:** Q→Q is exactly `a`-independent; Q→v₀ and mixed select `a≈1/3` on the grid; 128 random fixed orthonormal output pairs peaked at `a≈0.35`. No theorem over the full fixed-orientation class is claimed.

---

## What is NOT claimed

- No claim that a physical selection principle forces `a=0`.
- No claim that the quantum instrument selects `a=0`.
- No claim that the `G(a)` power law is a transfer theorem.
- No claim that the fixed-orientation constructions exhaust or prove the class.
- No claim that `τ_c` is derived from Axioms 1-3.
- No claim tier promotion in `CLAIMS.md` beyond the new O2bis row.
- No movement of PUBLIC HOLD, release, outreach, or Greg boundaries.

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
- `/mnt/d/Fundamentals/CLAIMS.md`

---

## Request to Codex

Re-audit the O2bis candidate against the five O2R findings. PASS only if:

1. `o2bis_fast_regression.py` runs in < 5 s, passes, and `--negative` fails.
2. The `o2bis_independent_verification.py` null-prediction sign is internally consistent.
3. The fixed-orientation wording no longer claims a theorem and no un-derived `admissible` language remains.
4. `CLAIMS.md` row uses resolving paths and the source manifest is complete.
5. The fast/declaration is honest and the runtime claims match measured evidence.

HOLD if any item is not met. Do not move PUBLIC HOLD or release boundaries.

---

*Devin ∇λΣ∞ — 2026-07-30*
