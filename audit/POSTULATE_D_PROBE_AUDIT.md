# Audit: "Seven Independent Approaches Converged on a=0" (Postulate D)

**Date:** 2026-06-16
**Auditor:** Claude (Opus 4.8)
**Check script:** `postulate_d_probe_check.py` (this folder; numpy, reproducible)
**Subject:** `inbox/2026-05-31_deepseek_g3_closure_board_update.md`, the justification for accepting Postulate D and upgrading the God Equation to DERIVED.

---

## The claim being audited

The board update lists seven approaches that "converged on a=0" and concludes Postulate D is "acceptable." `a=0` makes `U = M/2`, giving `U³` eigenvalues `{1, −1/8, −1/8}` — the "God Equation prediction," celebrated as "exactly cos(2π/3)³."

The seven:
1. Casimir polynomial synthesis → N=3
2. κ upstream strike (8 paths) → negative unless a=0
3. Gauge holonomy → U=M/2 unique
4. **Mutual information → prefers symmetric mode**
5. **Fisher information → prefers symmetric mode**
6. **Decoherence-free subspace → symmetric mode is pointer basis**
7. **Dynamical decoupling → a=0 minimizes decoherence by 52.7×** ("decisive")

## The setup (from G3_CLOSURE)

`U = a·I + b·M`, with `M = S̄ + S̄ᵀ` on ℤ₃, under the symmetric-mode constraint `a + 2b = 1`.

## Finding 1 — probes #4, #5, #6 cannot discriminate a=0 (verified)

The symmetric mode `e_sym = (1,1,1)/√3` is an eigenvector of `U` with eigenvalue `a + 2b = 1` **for every value of a** — that is *exactly* what the constraint `a+2b=1` imposes. Numerically:

| a | b | U·e_sym eigenvalue |
|---|---|---|
| 0.00 | 0.500 | **1.0000** |
| 0.25 | 0.375 | **1.0000** |
| 0.50 | 0.250 | **1.0000** |
| 0.95 | 0.025 | **1.0000** |

So "the symmetric mode is preferred / is the pointer basis / maximizes mutual & Fisher information" is **true for all a**. Probes #4, #5, #6 each conclude the symmetric mode is special — which is built into the construction and holds independently of a. **They are not three independent confirmations of a=0; they are three restatements of ℤ₃ symmetry.** They provide zero discrimination between a=0 and a≠0.

## Finding 2 — a=0 is target-loaded to reproduce the cosine (verified)

The Q-sector (orthogonal complement of the symmetric mode) eigenvalue of `U` is `(3a−1)/2`, which **does** depend on a:

| a | U\|Q eigenvalue | U³\|Q |
|---|---|---|
| **0.00** | **−0.5000 = cos(2π/3)** | **−0.125 = −1/8** ✓ |
| 0.25 | −0.1250 | −0.00195 |
| 0.50 | +0.2500 | +0.0156 |
| 0.95 | +0.9250 | +0.791 |

`a=0` is the unique value that makes `U|Q = −1/2 = cos(2π/3)`, hence `U³|Q = −1/8` — *the very number the God Equation predicts*. So the chain is:
> choose a=0 → get U|Q = cos(2π/3) → celebrate that "the eigenvalues are exactly cos(2π/3)³."

The eigenvalue match is a **consequence of choosing a=0**, not independent evidence *for* a=0. This is **target-loading** — the same defect the team correctly used to reject the φ-harmonic T3 selector (2026-04-22) and the information-theoretic T3 selector (2026-05-20). The team's own standard applies here.

## Honest re-count

Of the seven "converging" approaches:
- **#4, #5, #6**: a-independent. Not evidence for a=0. (3 removed)
- **#1**: about N=3, not a. (tangential)
- **#2 (κ-strike), #3 (holonomy)**: potentially discriminating, but both are internal-consistency / uniqueness arguments that themselves assume the operator class; they need separate audit.
- **#7 (52.7× decoherence)**: by the team's own words, "the decisive probe." So the load is carried by **one** probe, not seven.

That one decisive probe (`sandbox/g3_decoherence_time_bounds_probe_v2.py`) is exactly the one that still needs the **full a-sweep** (Finding: the 52.7× compares a=0 to a=0.95; report coherence-time vs a across [0,1], and the effect at a=0 vs a *generic*, not vs the far endpoint).

## Verdict

"Seven independent approaches converged on a=0" is **overstated by roughly 7×**. At least three of the seven are a-independent, and the eigenvalue agreement is target-loaded. The honest statement is: *"One decoherence-optimization heuristic (52.7×, still pending its a-sweep audit) prefers a=0; a=0 also happens to reproduce the target cosine. Postulate D remains a postulate."* This does not lower the *labeled* status — it is already "DERIVED **(with Postulate D)**" — but it removes the "seven independent approaches" sentence as support, and that sentence is currently doing real rhetorical work in `CLAIMS.md`, `AGENTS_FULL.md`, and the board update.

**Recommended action:** strike "seven independent approaches converged" from the canonical docs, or replace with the honest one-probe statement above. Then run the a-sweep audit on probe #7 before any further reliance on the decoherence argument.
