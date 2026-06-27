# Audit: The "52.7× Decoherence Selection Pressure" (Postulate D's decisive probe)

**Date:** 2026-06-16
**Auditor:** Claude (Opus 4.8)
**Source script (re-run, unmodified):** `D:\DeepSeek\sandbox\g3_decoherence_time_bounds_probe_v2.py`
**What it is cited as:** `CLAIMS.md` and the 2026-05-31 board update call this "the decisive probe," "**not a preference — selection pressure**," and the seventh approach that justified upgrading the God Equation to DERIVED.

I re-ran it unmodified. Here is what it actually shows.

---

## Finding 1 — the 52.7× is a monotone-curve endpoint artifact

The full a-sweep (decoherence vs a):

| a | decoherence | fidelity |
|---|---|---|
| **0.00** | 0.00107 | 99.89% |
| 0.10 | 0.00120 | 99.88% |
| 0.20 | 0.00133 | 99.87% |
| 0.33 | 0.00172 | 99.83% |
| 0.50 | 0.00263 | 99.74% |
| 0.70 | 0.00550 | 99.45% |
| 0.90 | 0.02520 | 97.48% |
| **0.95** | 0.05614 | 94.39% |

The curve is **smooth and monotonic**. There is no peak, no basin, no special feature at a=0 — it is simply the left endpoint of a monotonically increasing function. The headline "52.72×" is computed in the script as `max/min = decoh(0.95)/decoh(0.00)` — i.e. **the worst endpoint divided by the best endpoint.** Pick any monotone curve and the endpoint ratio can be made as large as you like by extending the x-range.

## Finding 2 — the fair comparison is 1.62×, on negligible fidelities

The script's own "fair" comparison (a=0 vs a=1/3, the natural "instant mixing" alternative) gives:

> "Decoherence at a=1/3 is **1.62× HIGHER** than at a=0."

1.62×, not 52.7× — and on decoherence values of 0.0011 vs 0.0017, i.e. **99.89% vs 99.83% fidelity.** Across the entire physically-reasonable range a ∈ [0, 0.5], fidelity stays between 99.7% and 99.9%. There is no meaningful selection of a=0 over a=0.2 or a=1/3. The large ratio exists only because the comparison was extended to a=0.95 — a near-identity, self-loop-dominated operator no one proposed.

## Finding 3 — the mechanism is power iteration, not decoherence

`U(a)=aI+bM` (with a+2b=1) has symmetric-mode eigenvalue 1 and Q-sector eigenvalue (3a−1)/2. The script **renormalizes after every step**, so iterating U is power iteration: it projects onto the dominant eigenvector (the symmetric mode) at a rate set by the spectral gap `1 − |(3a−1)/2|`. That gap is **largest at a=0** (|−1/2|) and shrinks to 0 as a→1 (U→I). So "a=0 best preserves symmetric fidelity" is a **restatement of 'U=M/2 has the biggest spectral gap'** — a fact about the operator's eigenvalues, identical to the target-loading already documented in `POSTULATE_D_PROBE_AUDIT.md`. It is not an independent physical decoherence result. The noise model in the docstring is explicitly built so that a=0's cycling "averages out" noise — the conclusion is in the construction.

## Finding 4 — the script's OWN verdict says CONDITIONAL, not DERIVED

The probe cited as decisive for the DERIVED upgrade ends (lines 253–260) with:

> "However, this is **NOT a derivation from Axioms 1-3**. It requires an additional physical postulate: *'The environment couples to the generation basis with correlation times longer than one propagation step.'* This postulate is physically reasonable but not contained in the existing axioms. **G3 remains CONDITIONAL 0.88.**"

**The board update inverted its own decisive evidence.** The script concludes CONDITIONAL 0.88 and names a *second*, undeclared postulate (long-correlation-time noise) that the decoherence argument silently depends on. So the decoherence route does not even reduce to "Postulate D alone" — it needs Postulate D **plus** an environmental-noise postulate, and still self-rates CONDITIONAL.

---

## Verdict

The "52.7× decoherence selection pressure," described in `CLAIMS.md` as decisive and as "not a preference — selection pressure," is:
1. a monotone-curve **endpoint artifact** (fair comparison: 1.62×, on 99.89% vs 99.83% — physically negligible);
2. a **power-iteration / spectral-gap restatement** of a=0, not independent physics;
3. dependent on a **second undeclared postulate** (long-correlation-time environmental noise);
4. and concluded by its **own script** as **CONDITIONAL 0.88, explicitly "NOT a derivation from Axioms 1-3."**

Combined with `POSTULATE_D_PROBE_AUDIT.md` (three of the seven approaches can't discriminate a=0; the eigenvalue match is target-loaded), the support for "Postulate D is acceptable / G3 is DERIVED" collapses to: *a=0 is the value that reproduces the target cosine, and a model built to favor a=0 favors a=0.*

**Recommended action:**
- Strike "decisive," "selection pressure," and "52.7×" from `CLAIMS.md`, `G3_CLOSURE_20260531.md`, and `AGENTS_FULL.md`. Replace with the script's actual verdict: *"a model with long-correlation-time generation noise mildly prefers a=0 (1.62× vs a=1/3, both >99.8% fidelity); the script self-rates CONDITIONAL 0.88 and notes it is not a derivation from Axioms 1-3."*
- The honest status of G3 / the God Equation, after this and `DEPENDENCY_DAG.md`, is **CONDITIONAL ≤ 0.88 at best, ARGUED more defensibly** — not DERIVED 0.90.

## Note on the IBM "98.1% / 99.01%" result (lighter touch)

`ibm_quantum_chiral_test.py` applies a deterministic Z₃ shift unitary (`ChiralShift`) and measures whether population follows the permutation. The "99.01%" is the **gate fidelity of applying a known permutation** on good hardware (permutations are shallow, low-error). The "symmetric" arm applies a mixing operation and, predictably, spreads. This demonstrates the hardware executes the two circuits as written — it does **not** independently validate any PF claim about physical "generation-identity preservation." `CLAIMS.md` already hedges this correctly ("not, by itself, a proof"); the over-reach is only in the `G3_CLOSURE` framing ("strongest structure of any AI signature tested"). Recommend toning that to "hardware executed the chiral vs symmetric circuits at expected fidelity," and, if it is to count as evidence at all, pre-registering a null (shuffled-data / symmetric-baseline gap with error bars).
