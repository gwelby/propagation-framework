# Look-Elsewhere Stress Test — The Weinberg "Unique Among 582" Claim

**Date:** 2026-06-16
**Auditor:** Claude (Opus 4.8)
**Scripts:** `weinberg_lookelsewhere_scan.py`, `weinberg_trials_factor.py` (in this folder; reproducible, stdlib only)
**Pre-registered prediction (written before running):** the spin/functional menu will yield many sub-percent hits on famous constants; the (½,1) sin²θ_W hit will be one of several once the functional form is also free.

---

## What the repo claims

`g3_casimir_weinberg_angle.md`:
> "A systematic scan of 582 polynomial alternatives … confirms uniqueness: **no other equation of this class reproduces sin²θ_W to sub-percent accuracy at (s₁,s₂)=(½,1).**"

This is presented as evidence that the match is "real (0.13–0.4σ is not a coincidence given the uniqueness proof)."

## The problem with that as evidence

"Unique among 582 *polynomials*, at the *fixed* spin pair (½,1), with the *fixed* functional `1−x(½)/x(1)`, against the *single* target sin²θ_W" holds the four other choices fixed and varies only one. The honest question is: **how dense is the space of sub-percent hits when the other hand-fixed choices are allowed to vary the way they were, in fact, chosen?**

---

## Experiment 1 — fixed polynomial, vary spin pair + functional

Holding their exact polynomial `x² + C₂x − C₂ = 0`, scanning 12 half-integer spins (66 pairs) × 7 simple functional forms = **462 combinations**, against 8 famous O(0.1–1) constants at 0.5% relative tolerance:

- **14 sub-percent hits** appeared, including:
  - Cabibbo angle sin²θ_C — **0.19% off** at s=(2.5,4)
  - δ_Koide = 2/9 — 0.40% off (same (½,1) value, 0.22310)
  - sin²θ_W on-shell — 0.12% off at **(½,1)** *and* 0.33% off at **(1,3.5)**

So even with the polynomial and functional fixed to their choices, **(½,1) is not the only sub-percent sin²θ_W hit** — there is a second at (1,3.5).

**Fairness credit (a genuine point for the framework):** (½,1) *is* the **best** sin²θ_W hit, clearly ahead of the runner-up:

| spin pair | `1 − x(a)/x(b)` | error vs on-shell |
|---|---|---|
| **(½,1)** ← repo | 0.22310 | **0.12%** |
| (1,3.5) | 0.22410 | 0.33% |
| (1,4) | 0.23301 | 4.32% |

The (½,1) match is not noise. It is the standout. But "standout of a dense menu" and "unique prediction at 0.13σ" are very different evidential claims.

---

## Experiment 2 — the trials factor (the number that matters)

Cleanest metric: of all values reachable by {spin pair × simple functional} on the fixed polynomial, what fraction of a *random* target constant in [0.05, 0.70] lands within 0.5% of one of them?

- Reachable distinct values in [0,1]: **264**
- Monte Carlo (200k random targets): **P(random target gets a sub-percent hit) = 0.46**

> **Roughly 1 in 2.2 arbitrary constants in this band is "derivable" to sub-percent by this machinery, by chance.**

That 0.46 is a **lower bound** on the trials factor, because it still holds the polynomial, the scheme, and the target fixed. The actual search that produced the headline also varied:
- the polynomial (582 alternatives — explicitly),
- the scheme (on-shell vs MS̄ — the value matches on-shell and misses MS̄ by 0.008),
- the target (the repo reports hits on sin²θ_W, δ_Koide, α, top/tau, electron/up, …).

Multiply those out and the effective number of independent "tries" is in the hundreds to thousands. A 0.12% coincidence against that denominator is **expected**, not surprising.

---

## Honest conclusion

1. The (½,1) sin²θ_W match is the **best** hit and sits at the most physically-motivated spin pair — that deserves credit and is not dismissed.
2. But the search space is **dense with sub-percent hits** (46% coverage), so the *existence* of a good hit carries little evidential weight on its own.
3. The "0.13σ" framing treats a best-of-many-choices result as a single pre-registered prediction. **It must be reported with a trials factor.** A defensible honest statement is: *"sin²θ_W ≈ 0.22310 is the best of a dense menu of Casimir-root functionals, matching the on-shell value to 0.12%, with an effective trials factor of order 10²–10³."* That is interesting numerology worth chasing — it is not a 0.13σ derivation.

## Constructive proposal for the group

Adopt a standing rule: **every numerical-coincidence claim ships with its menu-coverage number.** The two scripts here compute it in seconds for any target. A claim whose menu coverage is >10% at the claimed tolerance should be labeled `COINCIDENCE (uncorrected)`, never `DERIVED`. This turns the repo's own scanning discipline into an honesty instrument instead of a coincidence factory.
