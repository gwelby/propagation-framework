# Claude Source Audit — Entropy Chain & Periodic-Orbit Closure

**By:** Claude · 2026-07-15 · Qwen-lane independent verification (Greg-requested)
**Scope:** Source-level audit of `lean/PfLean/Entropy.lean` + periodic-orbit refs in `lean/PfLean/Axioms.lean`, triggered by the Jul 12–15 Lean surge commits.
**Verdict tag:** PLAUSIBLE — **source-confirmed, NOT compiler-confirmed** (see Limit).
**Boundary:** documentation only. No `CLAIMS.md`, PRED, PUBLIC HOLD, tier, or Lean-source change.

---

## Headline
The surge is **real and self-policing** — the named theorems exist and `Entropy.lean` carries **no live `sorry`**. But the load-bearing spectral results are **CONDITIONAL, not DERIVED**: they take entropy-decrease as a *hypothesis* and thread it through. "Sorry-free" is being conflated with "unconditionally proven." Cite accordingly.

## Findings

**F1 — `Entropy.lean` has zero live `sorry`/`admit`.**
A precise grep for `sorry`/`admit` as *tactic terms* (excluding backticked prose) returns only line 16 (a header comment). The `sorry` at **line 484** is **stale docstring prose** describing the heavy general-eigenvalue route they chose *not* to take; the real proof (`residueOperator_contraction`) sits immediately below it. Not a live gap.

**F2 — The spectral-constraint theorems are CONDITIONAL by construction.**
`residueOperator_contraction` (L507), `entropy_decrease_constrains_residue` (L526), `entropy_decrease_constrains_residue_eigenvalue` (L942), `realEigenvalue_is_complexEigenvalue` (L1027) all take
```
(h_entropy_decrease : ∀ s, PFEntropy (fun i => ∑ j, M i j * s j) ≤ PFEntropy s)
```
as a **hypothesis**. The proof of `residueOperator_contraction` is 2 lines — apply the hypothesis, rewrite by `PFEntropy_Q`. So the theorem proves *"IF entropy decreases for all states, THEN the residue operator is a contraction."* The physical content (entropy actually decreases under the dynamics) is **assumed, not derived**, at the general-matrix level. → **CONDITIONAL.**

**F3 — For the specific `T3` operator, entropy decrease IS unconditional.**
`PFEntropy_T3_decreases` (L293) and `full_norm_T3_strictly_decreases` (L371) carry no such hypothesis. **Open seam:** is `h_entropy_decrease` discharged for the *physical* operator, or do the general spectral theorems remain hanging on the hypothesis? That is the one question any citation must not paper over.

**F4 — Self-policing (genuinely good).**
`non_symmetric_cooling_counterexample` (L445) and `counterexample_positive_eigenvalue` (L1217) **prove the tempting strong claim FALSE**: even with entropy decrease, a non-symmetric matrix can have a positive residue eigenvalue. They formalized a disproof of their own shortcut (commit `2ad8b7a`). This is the discipline working as intended.

**F5 — Periodic-orbit / Edge-28 is NOT closed.**
`Axioms.lean` states it itself: L540 "PARTIAL (sorry)", **L1014 "The dependency closure contains `sorryAx`"**, L1028/L1192/L2242 the live gap. μ=±2 (T=1,2) proven and the odd-dim route avoids the spectral theorem, but general `|μ|<2` is a **live `sorry`** gated on Mathlib's Stone's theorem. The Jul 12–15 orbit commits *advanced* it; "periodic orbit theorem proven" would overclaim. Its `#print axioms` **would** show `sorryAx`. (Codex is auditing the adjacent proof-design return under thread `fundamentals-isometry-periodic-20260715` as of this writing — this corroborates that lane.)

## Limit (honest)
This is a **source read**, not a build. `lake build` / `#print axioms` was not run (the NTFS/OOM build problem — the lane's own priority #1). I can see there is no live `sorry` in `Entropy.lean` and the proof bodies are simple enough to read, but a source audit cannot catch a type error only the compiler would surface. **The decisive `#print axioms` on the entropy closure is still owed** and unblocks when the build is fixed.

## Recommendation (tiers)
- **Entropy spectral bound:** cite as **CONDITIONAL** — sorry-free; entropy-decrease is a hypothesis at the general level; strong (Re(λ)≤0) form disproven for the non-symmetric case. **Not** "entropy proof closed / DERIVED."
- **Periodic orbit:** cite as **PARTIAL** — μ=±2 proven; general case `sorryAx` in closure. **Not** "proven."
- Owed to upgrade PLAUSIBLE→CONFIRMED on F1: a clean `#print axioms` once the build runs.

## Replay (for Codex)
```
cd /mnt/d/Fundamentals
grep -nE '(^|[^`\w])sorry([^`\w]|$)|(^|[^`\w])admit([^`\w]|$)' lean/PfLean/Entropy.lean   # → only L16 (comment)
sed -n '507,536p' lean/PfLean/Entropy.lean    # residueOperator_contraction: h_entropy_decrease is a hypothesis
sed -n '540p;1010,1028p' lean/PfLean/Axioms.lean   # periodic-orbit PARTIAL + sorryAx note
```
