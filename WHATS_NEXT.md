# What's Next: Rigor-First Closure Order

**Date**: 2026-04-12 (updated after v0.3 paper pass + two-attack strategy session)
**Context**: Paper v0.3 is done. Neutrino non-universality integrated as positive scope result. God Equation Path B Families A/B/edge-flux are closed no-gos. The attack plan below supersedes the April 1 priority order.

---

## ⚡ 2026-04-12 — TWO HIGHEST-LEVERAGE ATTACKS

### Attack 1: δ=2/9 Casimir Selector (Codex + Lumi)
**The question**: Does the Casimir polynomial sector produce x* = 2/9 as a natural fixed point — independently of the Weinberg angle derivation?
**Why it matters**: δ\_Koide = 0.22222963 rad (|δ − 2/9| = 7.4×10⁻⁶, confirmed April 2). sin²θ\_W = 0.22310 = 2/9 + O(α). RG: sin²θ\_W runs to δ at μ ≈ 98 GeV. If a single PF derivation produces x* = 2/9 and separately accounts for both quantities, that's two independent precision measurements unified from one equation. Either the framework is right in a deep way, or a remarkable numerical coincidence is exposed.
**Assigned to**: Codex (Casimir algebra — does any spin assignment or resonance condition in the polynomial produce 2/9 as a fixed point?), Lumi (physics check — does the RG argument hold, and what would a PF-native selector corollary look like?)
**Task**: T-022 (new)
**Done when**: Casimir polynomial scan returns either (a) a spin assignment producing 2/9 ± 0.001 with a geometric interpretation, or (b) a clean ruled-out result with why no such assignment exists.

### Attack 2: EEG TEST 1 Pre-registration + Run (Greg + Lumi)
**The question**: Does Critical Slowing Down (EEG variance increase >50%) precede genuine insight events in ≥7/10 sessions?
**Why it matters**: This is the only test generating new data the framework doesn't have yet. A positive result is the first cross-scale validation. A negative result falsifies the biological claim while leaving the particle physics results intact. Binary. Pre-registerable. Executable this week.
**Assigned to**: Greg (run the Muse sessions, button-press at insight), Lumi (write the pre-registration spec before any session runs — state the exact threshold and falsification criterion in `protocols/muse_insight_protocol.md` before touching the headset)
**Task**: T-020 (existing — see pre-registration note below)
**Done when**: Pre-registration doc exists with date stamp, then ≥10 sessions collected and analyzed.

**Rule**: Pre-register before running. Write the expected outcome in `protocols/muse_insight_protocol.md` before the first session. If the result disagrees, the pre-registered prediction stands.

---

**Date**: 2026-04-01 (original — see below for April 1 priority order, still valid for the theorem stack)
**Context**: Public-facing docs are much closer to the live truth board. The next milestone should harden theorem structure, not widen the claim surface.
**Question**: What is the shortest honest path from the current repo to a smaller number of stronger claims?

---

## 2026-04-01 Finding — Path A Ticket Is Stale

`chiral_projection_z3.py` was audited and corrected today. The script's interpretation block had claimed `β ≈ 0` and `T_L³ IS diagonal`. Both were wrong.

What chiral projection actually does:
- Kills the k=2 **eigenmode** entirely (sets its eigenvalue to zero)
- Does **not** eliminate the S̄² term from position space: `|β/α| = 1.0` (measured)
- T_L³ in the full 3D position space has **nonzero off-diagonals** — Gap B no-go still applies

What IS true: within the projected {k=0, k=1} 2D subspace, T_L³ is diagonal in the Fourier eigenbasis. That is a weaker result — 3-step periodicity within the left-handed sector, not full H_prod closure.

**Consequence for Path A ticket**:
The ticket `God_Equation_Path_A` asks to derive `b=0` from chiral coupling. That target is not what chiral projection produces. The ticket must be reframed before any derivation work proceeds, or it will repeat the interpretation error the script just corrected.

**New named gap** (not in any ticket yet):
Prove that Fourier-basis closure in the projected 2D sector implies position-space probability factorization for H_prod. This is a separate proof obligation that Path A did not previously identify.

---

## Current Call

The shortest path is not:

- more domains
- more numerology
- more outreach-first hype

The shortest path is:

- fewer unnamed moves
- cleaner theorem boundaries
- bounded closure work on the actual load-bearing bridges

That gives the following work order.

---

## Priority Order

### 1. Finish truth-sync and keep one status grammar

Keep `CLAIMS.md` as the only formal scoreboard.
Any planning, explainer, manuscript, or Explorer copy should map back to it cleanly.

This is not cosmetic.
It prevents the repo from manufacturing fake progress through language drift.

### 2. Write the Axiom 3 selector note

The framework still has a threshold principle more clearly than it has a general ordering principle.

The next bounded target is:

- `derivations/axiom3_selector_note_2026-04-01.md`

Done condition:

- one selector object or one bounded selector corollary is stated clearly enough to survive hostile audit
- or the attempted selector is killed cleanly

### 3. Close T1 physical realization

The `SU(2)` lift is no longer the weak point.
The live missing theorem is why Axiom 3 forces physical population of the available weight-2 branch.

Working card:

- `derivations/generation_closure_cards_2026-04-01.md`

Done condition:

- the T1 card no longer depends on an unnamed selector move or the external `A_NR` hypothesis

### 4. Close T2 denominator theorem

The local `2x2` Fermi-point lemma is useful but still conditional.
`M = 3` will not close until the PF-native bridge is stronger than the Volovik analogy.

Working card:

- `derivations/generation_closure_cards_2026-04-01.md`

Done condition:

- either the Fermi-point route becomes PF-native and audit-ready
- or it is ruled out and replaced with a cleaner PF-native denominator route

### 5. Reopen G3 only on the exact remaining bridge

No more broad God Equation storytelling.
No more treating a good number as closure.

**Path A status (reframed 2026-04-01, ticket updated)**:
- Old target: derive `b=0` from chiral ℤ₃ coupling — DEAD
- Correct target: two obligations H-A (is {k=0,k=1} sector forced by Lagrangian?) and H-B (does
  Fourier-sector closure imply position-space H_prod factorization?)
- Path A ticket now states these correctly. See `God_Equation_Path_A_—_Derive_b=0_...md`

**Path B status (Families A and B narrowed hard, 2026-04-01)**:
- Family A (direct closure-time channel intensities): STRONG RESTRICTED NO-GO CANDIDATE
  - `Cov(X^(0), X^(1)) = (441/2048)σ⁴ > 0`; survives broader iid exchange-symmetric ensemble class
  - See `derivations/god_eq_path_b_family_a_intensity_theorem_2026-04-01.md` and `..._audit_...md`
- Family B:
  - the two tested quadratic time-integrated readouts fail strongly under the isotropic real Gaussian probe
  - the natural antisymmetric edge-flux current is now an **exact no-go** because `J^(0)+J^(1)+J^(2)=0` identically, so nontrivial factorization is impossible
  - the Family A whitening covariance does **not** rescue the tested B1/B2 observables
  - See `derivations/god_eq_path_b_family_b_integrated_currents_2026-04-01.md`, `..._audit_...md`, and `derivations/god_eq_path_b_edge_flux_current_no_go_2026-04-01.md`
- Vacuum direction:
  - the free linearized `ℤ₃` vacuum points away from the Family A escape covariance
  - stronger PF/energy/entropy closure language is not signed off yet
  - See `derivations/god_eq_pf_vacuum_ensemble_analysis_2026-04-01.md` and `..._audit_...md`
- Family C (quadratic closure functionals of the operator): still open and is now the last natural quadratic Path B candidate
- Nonquadratic one-medium observables: still open in principle, but now need a genuinely new probability model rather than another current-style rephrasing

Working card:

- `derivations/g3_closure_card_2026-04-01.md`

Done condition:

- Path A is either reframed with the corrected target, or ruled out and replaced
- one exact closure object
- one explicit probability model
- one proof or falsification of `H_prod`

### 6. Only then do pre-registered empirical risk and external review

IBM, EEG, and outside physicist feedback are still important.
They are just downstream of the theorem stack being stated tightly enough to be worth attacking.

The right order is:

- theorem target first
- prediction statement second
- hostile outside critique third

**Pre-registration rule (added 2026-04-01)**:
State the expected numerical result *before* running the sandbox script. The chiral script bug happened because the conclusion was written into the interpretation block first, and the computation was treated as confirmation. If the script had been pre-registered as "we expect |β/α| ≈ 0, and if |β/α| = 1 then Path A is challenged" — the wrong interpretation would never have survived.

For any new sandbox script: write the prediction in a comment at the top of the file before running it. If the result disagrees, update the prediction section to record the finding honestly before touching the interpretation.

**Sandbox hygiene (added 2026-04-01, partially completed)**:
The specific path-contaminating scripts named in the earlier pass have now been cleaned to use `Path(__file__).resolve().parent`. Keep the rule, but do not treat that old list as still-open work. Before the next empirical push, do one quick repo-wide audit for any remaining hardcoded output paths and keep the pre-registration discipline at the top of each new script.

---

## Working Documents For This Pass

- `CLAIMS.md`
- `ACTIVE_ISSUES.md`
- `derivations/axiom3_selector_note_2026-04-01.md`
- `derivations/generation_closure_cards_2026-04-01.md`
- `derivations/g3_closure_card_2026-04-01.md`

These are the current bounded planning documents for the next serious theorem work.

---

## What Not To Do Next

Do not do these out of order:

- do not let the IBM chirality result be described as a proof of `H_prod`
- do not promote T1 or T2 because the algebra after the missing bridge looks beautiful
- do not reopen Koide phase or alpha derivation as if they are upstream of the selector and generation stack
- do not let the public layer outrun the exact-status layer again
- **Path A ticket is now reframed** (2026-04-01) — the stale `b=0` target is removed; obligations H-A and H-B are the live targets
- do not mistake "the computation ran and gave a number" for "the script is testing what it claims to test" — perihelion_precession.py ran for months returning None; the chiral script ran and printed the wrong interpretation for months. Running ≠ verified.

---

## Strongest Honest Summary

The framework gets closer to a finished theory by getting smaller, not bigger.

Right now that means:

1. one status grammar
2. one selector note
3. one T1 closure card
4. one T2 closure card
5. one G3 closure card — **with Path A reframed first**

If those harden, the rest of the repo reorganizes around them.
If they fail, the framework still becomes more honest and therefore more valuable.

**On testing**: the project currently has more derivation tickets than it has clean, correctly-tested, non-contaminating verification scripts. The next empirical push (EEG TEST 1) is the right external test. Before that, the sandbox needs pre-registration discipline and path cleanup. Derivation progress and testing progress are separate tracks — do not let one substitute for the other.
