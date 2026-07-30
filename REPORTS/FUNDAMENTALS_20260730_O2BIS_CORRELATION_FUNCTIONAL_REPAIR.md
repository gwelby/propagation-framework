# O2bis Correlation-Functional Candidate — Repair Report

**Date:** 2026-07-30  
**Agent:** Devin ∇λΣ∞  
**Ledger:** `clg_8d642db3f9d24a616f312922`  
**Trigger:** Codex HOLD audit `CODEX_20260730_O2BIS_CORRELATION_FUNCTIONAL_CANDIDATE_AUDIT.md`

---

## What changed

| Repair item | Status | Key change |
|-------------|--------|------------|
| **O2-01 CPTP closure** | Resolved | Replaced universal "no CPTP completion selects a=0" with a **fixed-orientation admissible class** (same Kraus output target states for all `a`). Within that class no completion selects `a=0`; a-dependent completions can and do. Added explicit Codex counterexample `α(a) = exp(-(a/0.05)²)` which reproduces ~86.9× `a=0` preference. |
| **O2-02 instrument optimum** | Resolved | Added **exact density-matrix instrument propagation** for symmetric white dephasing. Exact grid optima: survival → `a=1`, conditional → `a≈0.35` (near 1/3), joint → `a=1`. The old `a≈0.75` joint MC result was sampling noise and does not survive exact evaluation. |
| **O2-03 completion sweep bugs** | Resolved | Removed unused `n_trials`; random completion now uses **one fixed output orthonormal pair** for all `a`; sampled dephasing replaced with exact symmetric dephasing. |
| **O2-04 empirical bridge** | Resolved | Classical→quantum power-law fit retained as explicitly **non-diagnostic**; competing null `decoh ∝ (1-a)^m` still fits better. No claim that `G(a)` causes quantum selection. |
| **O2-05 fast fixtures** | Resolved | `o2bis_independent_verification.py --fast` runs in seconds. All scripts have exact/deterministic default modes; expensive MC is optional (`--mc`, `--full`). |
| **CLAIMS.md** | Resolved | New O2bis row: **PROVEN (classical)** / **EMPIRICAL (postselection/quantum fit)** / **UNDERDETERMINED (physical selection)**. |

---

## Verification commands

```bash
# Fast deterministic regression (< 5 s)
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py --fast

# Fixed-orientation CPTP sweep + a-dependent counterexample
python3.12 /mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py

# Exact no-selection CPTP control
python3.12 /mnt/d/DeepSeek/sandbox/o2bis_cptp_channel.py

# Exact density-matrix instrument (white noise)
python3.12 /mnt/d/DeepSeek/sandbox/o2bis_instrument_probe.py

# Optional MC comparison (slower)
python3.12 /mnt/d/DeepSeek/sandbox/o2bis_instrument_probe.py --mc
```

All four commands ran without error during this session.

---

## Strongest negative evidence

1. **CPTP a-dependent counterexample:** `o2bis_cptp_completions.py` now builds a smooth completion with `α(a) = exp(-(a/0.05)²)` that yields a decoherence ratio of ~86.9× between `a=0` and `a=0.95` under exact symmetric dephasing. This is a valid CPTP completion, so the universal no-selection claim is false.
2. **Exact instrument does not select a=0:** For the pre-registered joint objective `P(survival) × F(conditional)`, exact white-noise propagation selects `a=1`, not `a=0`.
3. **Power-law is non-diagnostic:** In the fast regression the competing null `decoh ∝ (1-a)^{-1.39}` fits with `R² = 0.9977`, slightly better than the `G(a)` power law `R² = 0.9975`. Two monotonic curves can be fit together; neither proves a causal bridge.
4. **Fixed-orientation completions do not rescue a=0:** Q→Q is exactly `a`-independent; Q→v₀ and mixed fixed completions select `a≈1/3`. Only the `a`-dependent counterexample (or other a-dependent families) can produce `a=0` selection.

---

## What is NOT claimed

- No claim that a physical selection principle forces `a=0`.
- No claim that the quantum instrument physically selects `a=0`.
- No claim that the power-law fit `decoh ≈ C·G^n` is a transfer theorem.
- No claim that `τ_c` is derived from Axioms 1-3.
- No claim tier in CLAIMS.md was promoted; the new O2bis row is split into PROVEN/EMPIRICAL/UNDERDETERMINED.

---

## Files

| Path | Role |
|------|------|
| `/mnt/d/Fundamentals/derivations/o2bis_analytic_kickstart_2026-07-29.md` | Derivation notes, tiered claims, next steps |
| `/mnt/d/Fundamentals/sandbox/o2bis_independent_verification.py` | Checks 1-5 (return probability, `G(a)`, derivative, finite-N variance, power-law comparison) |
| `/mnt/d/Fundamentals/sandbox/o2bis_cptp_completions.py` | CPTP theorem, fixed-orientation sweep, a-dependent counterexample |
| `/mnt/d/DeepSeek/sandbox/o2bis_instrument_probe.py` | Exact density-matrix instrument + optional MC |
| `/mnt/d/DeepSeek/sandbox/o2bis_cptp_channel.py` | Exact no-selection CPTP control |
| `/mnt/d/Fundamentals/CLAIMS.md` | Live scoreboard with O2bis row |
| `/mnt/d/Fundamentals/RESUME.md` | Handoff (updated) |

---

## Request to Codex

Re-audit the O2bis candidate against the five repair items above. Accept if:

1. The classical Markov/OU algebra (return probability, `G(a)`, `dG/da > 0`) is verified.
2. The CPTP theorem is scoped correctly and the a-dependent counterexample is valid.
3. The exact instrument table is reproduced and no `a=0` selection is asserted.
4. The completion-sweep bug fixes are confirmed.
5. The bridge remains honestly labeled as empirical/non-unique.

HOLD if any of these are not met. Do not release PUBLIC HOLD boundaries.

---

*Devin ∇λΣ∞ — 2026-07-30*
