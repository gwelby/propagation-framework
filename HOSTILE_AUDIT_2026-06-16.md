# Hostile Audit — Fundamentals / The Propagation Framework

**Date:** 2026-06-16
**Auditor:** Claude (Opus 4.8), commissioned as hostile external reviewer
**Scope:** Foundations (axioms, Medium), the five DERIVED rows in `CLAIMS.md`, the Lean 4 "machine-verified" claims, and the α / numerical-coincidence cluster.
**Method:** Read the scoreboard, then read the derivation files *underneath* it, then recompute the load-bearing numbers independently, then compare source files to scoreboard.
**Stance:** Adversarial by request. Findings are stated bluntly. A "What is genuinely good" section at the end gives the framework its due — read it; the criticism is not the whole story.

**Companion working files (in `audit/`):** `LOOK_ELSEWHERE_RESULTS.md` (+ scripts — the trials-factor experiment), `DEPENDENCY_DAG.md` (floor-rule ledger), `POSTULATE_D_PROBE_AUDIT.md` (+ script — the "seven approaches" recount), `FINDINGS_LOG.md` (running positive/negative notes for the group). All numbers in those files are independently reproducible from stdlib/numpy.

---

## 0. One-line verdict

**This is a well-run numerical-coincidence program presented as a rigorous derivation program.** The internal audit *culture* is genuinely excellent — among the most honest "theory of everything" repos in existence. But the headline `DERIVED` claims are, without exception, pre-existing numerical coincidences (Koide 1981; de Vries 2004 / Rivero; Foot 1994; the optical metric) that are restated as algebraic identities, machine-checked *as algebra*, and then promoted to "derived physics" by inserting exactly the premise each one needs. **The scoreboard says materially more than the files beneath it.**

---

## 1. The central structural finding: identity-laundering

Every `DERIVED` row follows the same five-step pipeline:

1. **Take a known empirical relation** (Koide `Q=2/3`; de Vries/Rivero Weinberg ratio; optical metric for null geodesics; the `(2,1)` double-cover).
2. **Rewrite it as an algebraic identity** ("`Q=2/3 ⟺ R/A=√2`", "`R = (√19−3)(√19−√3)/16`", "`Q(N)=2/3 ⟺ N=3`").
3. **Machine-check the identity in Lean.** The Lean kernel confirms the *algebra* — which a calculator also confirms.
4. **Print "machine-verified DERIVED claim."**
5. **The actual physics premise** — *why* the masses are equilateral, *why* spins `(½,1)`, *why* `R` should equal `sin²θ_W`, *why* the vacuum selects the equal-norm point, *why* `a=0` — **is left underived and openly flagged as OPEN in the source file.**

The Lean theatre is the load-bearing rhetorical move, so state it plainly:

> **Lean is verifying arithmetic, not physics.** `WeinbergAngle.lean` proves `1 − x₊(½)/x₊(1) = (√19−3)(√19−√3)/16 ≈ 0.22310`. True — and empty of physics. `ThreeGenerations.lean` proves `2N/(2N+3)=2/3 ↔ N=3`, which is middle-school algebra. `KoideGeometry.lean` proves the `Q=2/3 ⟺ R=½` identity. In **every** case the Lean file certifies the step that was never in doubt and is silent on the step that carries the entire claim. "Lean-certified DERIVED" conflates the two.

This single pattern accounts for 5 of the 5 DERIVED rows. It is the core of the audit.

---

## 2. Independently recomputed numbers

All recomputed from scratch (Python, standard constants). Arithmetic in the repo is **correct**; the issue is never arithmetic — it is what the arithmetic is claimed to mean.

| Claim | Repo value | Recomputed | Verdict on the *number* |
|---|---|---|---|
| Weinberg `R = 1 − x₊(½)/x₊(1)` | 0.22310 | **0.223101** ✓ | Correct. But matches **on-shell** (0.22337); misses **MS̄(M_Z)** (0.23122) by 0.008 — many σ. Scheme-shopped. |
| God Eq `λ_c`, exponent `N^(D/2)=N^1.5` | 1.157×10⁻¹⁸ m, 1.48% | **1.157×10⁻¹⁸, 1.48%** ✓ | The exponent that hits the target *exactly* is **1.4997**. The repo's own honest derivation says the heat kernel gives `N^1`, which yields **1.0×10⁻²⁵ m (off by 10¹⁷)**. |
| α "zero-free-parameter" Casimir hit | 1/137.119 | **1/137.119** ✓ | Real `1/α=137.036`. A hand-picked product of three Casimir roots (j=1,3/2,2) over π. Numerology. |
| Koide `Q` (charged leptons) | 2/3 to 0.0009% | identity confirmed | Genuine coincidence (Koide 1981). Here it is *parameterized*, not derived. |

**The God Equation line is the decisive one.** "No fitting parameters" is false: a power sitting *inside an exponential of ~38* is set to precisely the value that lands the answer, and that value (`1.5`) **contradicts the only derivation the repo has for it** (`N^1`). One tuned exponent inside `exp()` can hit any scale in the universe; it hit this one.

---

## 3. Confidence inflation: source file vs. scoreboard

This is the most serious governance problem. `WHATS_NEXT.md` mandates "one status grammar." The repo violates it against itself. Confidence is *manufactured* in the gap between the derivation file and `CLAIMS.md`.

| Claim | Source-file confidence | `CLAIMS.md` | Inflation |
|---|---|---|---|
| **God Equation (λ_c)** | `lambda_c_from_axioms.md` line 409: **"confidence in the hypothesis as stated … 0.05"**; line 137 "0.75 ARGUED"; line 89 "bridge … **not yet proven**" | **DERIVED 0.90** | **up to 18×** |
| **Weinberg angle** | `g3_casimir_weinberg_angle.md` line 268: **"ARGUED (0.65)"** | **DERIVED 0.90** | ~1.4× + status jump |
| **N=3 (used *inside* the God Eq)** | God-Eq file cites it at **0.985**; CLAIMS scores it **CONDITIONAL 0.85** | — | God Eq imports a number at 0.985 that the repo itself rates 0.85 CONDITIONAL |
| **D=3 (used inside God Eq)** | God-Eq file line 224: **0.60** ("knot stability argument") | — | a 0.60 input feeding a 0.90 output |

**Logical floor violated:** a derived result cannot be more certain than its least-certain premise. The God Equation takes `N=3` (CONDITIONAL 0.85), `D=3` (0.60), an unproven `N^{D/2}` bridge, a `√2` "interpretation," **and** Postulate D — and is published at **0.90**. That is arithmetically impossible as a confidence; it is a marketing number.

---

## 4. Per-claim verdicts

### 4.1 Weinberg angle — **overstated: ARGUED, not DERIVED**
- Provenance: H. de Vries (Physics Forums, 2004), Rivero (2005–6). Not original here.
- The polynomial `x²+C₂x−C₂=0` is pinned by **three hand-chosen constraints** (`f₀=0, g₀=0, g₁=−f₁`) plus an implicit `f₁=1`, plus the spin pair `(½,1)`, plus the functional `R=1−x(½)/x(1)`, plus the identification `R≡sin²θ_W`, plus the on-shell scheme. That is **≥6 choices**.
- "Unique among 582 alternatives" is a **look-elsewhere scan conditioned on the answer** ("…that reproduces sin²θ_W … at `(½,1)`"). Searching 582 expressions for a sub-percent hit on a famous constant and keeping the hit is the mechanism that *manufactures* coincidences, not evidence against coincidence. No trials-factor correction anywhere.
- The scheme gap is admitted, then ignored in the grade.

### 4.2 God Equation (λ_c from l_P) — **overstated: ARGUED/CONDITIONAL at best**
- "No free parameters" is false (§2). The `N^{D/2}` bridge is "not yet proven" *in the same file*. Core hypothesis self-rated **0.05**.
- "DERIVED (with Postulate D)" — `G3_CLOSURE_20260531.md` is candid: `a=0` was **"not derived from Axioms 1-3 alone"**, so it was **"admitted as explicit postulate."** Acceptance criterion: **"Greg: Cannot see a reason for No."** That is argument from incredulity. "Seven approaches converged" and "decoherence probe 52.7×" are *motivation*, not proof.
- The IBM quantum-hardware run (98.1% fidelity) verifies that a chiral ℤ₃ medium preserves a label — a real result — but the repo's own rule ("do not let the IBM chirality result be described as a proof of H_prod") is being bent by the public "G3: CLOSED" framing.

### 4.3 Koide `Q=2/3` — **DERIVED label is a category error; it is an EXACT IDENTITY + an OPEN selection problem**
- The math is correct and clean: `√mₙ = A + R cos(θ₀+2πn/3)` ⟹ `Q = ⅓ + ⅙(R/A)²`, so `Q=2/3 ⟺ R/A=√2 ⟺ 45° Foot cone ⟺ equal U(1)/SU(3) Frobenius norm`. All true.
- But this is a **restatement of the premise**, not a derivation of the masses. Section 4 of `koide_geometric_equivalence.md` admits the selection — *why the vacuum sits at the equal-norm point* — is **"Not Yet Derived"**, with three conjectural routes (A/B/C), one of which (C) carries an explicit caution that the naive symmetry argument gives `1/3`, not `1/6`.
- Caveat the repo under-states: `Q=2/3` to 0.0009% uses **pole masses**; `Q` drifts with mass scheme/running. The precision is partly a scheme artifact, not a pure law.
- Honest grade: **EXACT IDENTITY (geometry) + OPEN (physical selection)**. Not DERIVED.

### 4.4 (2,1) Topological Weights — **kernel theorem is real and standard; physics is CONDITIONAL and shaky**
- `topological_availability` (`quatToSO3 g = 1 → closureOrder g ∈ {1,2}`) is **genuinely proven, 0 sorrys** (verified — the lone "sorry" grep hit is inside a comment). Credit where due.
- But it is **textbook group theory**: the kernel of SU(2)→SO(3) is {±1}. It proves nothing PF-specific.
- The file is honest that physical realization is **CONDITIONAL 0.85** on an undischarged hypothesis `A_NR`. Worse: the pressure test `spin_pair_classification.py` shows **j=1 (boson) is ANNIHILATED**, contradicting the "j=1 survives" narrative the weight-count story rests on.
- Note for the record: this same flagship file previously contained a **mathematically false theorem** (claiming *all* unit quaternions have order ≤2) that stood until 2026-06-14. Honest to fix; sobering that it shipped.

### 4.5 Gravity as optical geometry — **legitimate, but not new and not a PF result**
- `weakFieldIndex Φ = √[(1−2Φ)/(1+2Φ)]` and the null-geodesic/Randers story are **correct, standard physics** (the optical metric for static/stationary spacetimes is textbook; Gordon, Fermat). DERIVED 0.95 is defensible *as physics*.
- But it is a **known equivalence imported into PF**, not derived from Axioms 1–3. Presenting it as a framework achievement inflates the framework's novelty. The Lean file verifies properties of a known formula.

### 4.6 α (fine structure constant) — **the most honest file in the repo; the scoreboard ignores it**
- `alpha_from_pf.md` concludes **"FAILED … No derivation of 1/137.036 has been achieved,"** and explicitly tags Eddington-style fits as numerology. Exemplary.
- Yet `CLAIMS.md` keeps a *different* result alive at **0.60**: `(1−x₁)·x_{3/2}²·(1−x₂)/π = 1/137.119`, found by `alpha_casimir_hunt.py`. The careful file says fail; the scoreboard banks the scan hit. **Resolve this contradiction in favor of the honest file.**

---

## 5. Foundations are non-predictive

The three axioms (propagation is fundamental; every medium has a causal velocity; coherence is necessary for structure) and the Medium (defined "by roles, not substance," and declared "compatible with SR/GR/QM/QFT") **constrain no number.** They are a *reinterpretation layer* over existing physics, not a generative one. Every actual number enters through an *added* selector — Axiom 3b, Postulate D, the chosen spins, `f₁=1`, the on-shell scheme, `N^{D/2}`. The axioms are doing zero quantitative work; the selectors are doing all of it, and the selectors are chosen to fit.

---

## 6. What is MISSING

1. **One novel, quantitative, falsifiable prediction that differs from the Standard Model and has been tested and confirmed.** There are none. Every DERIVED row is a postdiction of an already-measured number. The one genuinely new prediction (variable `c`) is constrained by Cassini to be indistinguishable from null; the one new data test (EEG critical-slowing-down, T-020) is **unrun**.
2. **A trials-factor / look-elsewhere correction.** The repo runs scans ("582 alternatives", "Casimir hunt", Monte-Carlo p-values) but never penalizes for the size of the search. This is the single biggest methodological hole — it is the machine that produces the coincidences being celebrated.
3. **Provenance up front.** Koide (1981), Foot (1994 — `foot_1994.pdf` is *in the repo*), de Vries/Rivero (2004–6) authored the interesting relations. The framework wraps them. Say so in the abstract, not the footnotes.
4. **Derivation of even one selector** (`N=3`, `b₀=16/3`, the spins, Postulate D, Axiom 3b, the scheme) from the axioms. Until one exists, "derived from Axioms 1–3" is unsupported for all of physics-section §1.
5. **A dependency audit.** `DERIVED` results import `CONDITIONAL` inputs (God Eq ← N=3). Build a DAG; no node may be graded above its weakest parent.
6. **External physicist review.** Rivero is the *source* of the numerology, not an independent referee. No adversarial mainstream critique has been solicited.
7. **For the biological/consciousness rows:** the one variable `consciousness_theory_audit.md` itself names as required — a PF-specific metric that dissociates from synchrony/integration/reportability — does not exist. Until it does, those rows are INTUITION at most.
8. **A single source of truth for "current state."** `STATE.md` (physics), `RESUME.md` (Lean compile errors, different author), and `REMEMBER.md` (UI/UX pass) describe three different projects. Pick one.

---

## 7. What is genuinely good (and should be preserved)

- **The audit culture is real and rare.** Honest negatives, NO-GO logs, "running ≠ verified," pre-registration discipline, the Duck's "How do you know?", target-loaded-selector rejections. Most *derivation* files are more honest than the *scoreboard*. This is the opposite of crank behavior and is worth protecting.
- **Several no-go results are genuine intellectual output**: the edge-flux `J⁽⁰⁾+J⁽¹⁾+J⁽²⁾=0` identity, the Family-C operator-algebra collapse, the κ-upstream strike. These are real (negative) theorems.
- **The neutrino Koide non-universality result** is handled exactly right: a confirmed *scope-delimiter*, not over-sold.
- **The gravity-optics module** is correct physics.
- **Postulate D is at least labeled** as a postulate rather than silently smuggled — the fix is to carry that honesty up to `CLAIMS.md` and the public docs.

The framework's problem is not dishonesty in the trenches. It is **honest trenches feeding a dishonest scoreboard.**

---

## 8. Recommendations (priority order)

1. **Demote to match the source files.** God Equation → ARGUED/CONDITIONAL; Weinberg → ARGUED; Koide → EXACT IDENTITY + OPEN selection; α → OPEN (delete the 0.60 scan hit). This is a one-session edit to `CLAIMS.md` and it ends the credibility risk.
2. **Relabel all Lean claims** "algebraic identity machine-checked" — true, still valuable, and no longer overstated as "verified physics."
3. **Fix or retract "no free parameters"** on the God Equation. Either derive `N^{D/2}` honestly or call the formula a fit.
4. **Add a trials-factor column** to every numerical-coincidence row, or move them to a clearly-labeled "Noted Coincidences (uncorrected)" appendix.
5. **Build the dependency DAG** and enforce the floor rule (no node above its weakest parent).
6. **Run T-020 (EEG).** A framework with this much machinery and zero confirmed novel predictions needs *data*, not more derivation files. Pre-register first (the repo already knows this).
7. **Collapse the three "current state" files into one.**

---

## 9. The falsification challenge (offered in good faith)

If the framework wants to convert a skeptic, the path is short and it is not more algebra:

> **State one number the Standard Model does not already give, derive it from Axioms 1–3 with no selector chosen after seeing the target, pre-register it, and measure it.**

Until that exists, the honest one-sentence status of Fundamentals is:

**"A coherent reinterpretation of known physics that has rediscovered several known numerical coincidences and proved, in Lean, that they are arithmetically what they are — with the physical derivations of all of them still open."**

That is a real and defensible thing to be. It is just not what `CLAIMS.md` currently says it is.

---
*Audit performed 2026-06-16. Numbers recomputed independently. Findings are reproducible from the cited files. — Claude (Opus 4.8), hostile reviewer.*
