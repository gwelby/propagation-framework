# Roadmap: From "Interesting Numerology" to New Physics
*Strategic roadmap filed 2026-06-18 (external analysis, brought by Greg). Claude's claim-state mapping appended — DO NOT let this be forgotten (it is exactly the kind of high-value thinking the ecosystem loses). Owners to action: DeepSeek (derivation), Kiro (spec), Codex (audit). Read with `CLAIMS.md` open.*

## The core problem to solve
Deriving known constants geometrically is **not a unique capability** — ≥5 incompatible frameworks (UFQFT, IGPS, UGP, pentagram-Koide) claim the same. The bar is NOT "be more precise." It is: **say something the Standard Model can't, and be right.** Postdiction of known constants will always be suspect. A *pre*-diction that lands is worth a thousand postdictions.

## Priority stack
| # | Action | Impact |
|---|---|---|
| 1 | Commit to ONE novel, testable prediction with a number (before the experiment resolves) | Turns postdiction → prediction |
| 2 | Formalize axioms in Lean as a DISCOVERY tool (find what they DON'T imply) | Surfaces smuggled assumptions |
| 3 | Honestly count + name the real degrees of freedom | Builds credibility |
| 4 | Build a mechanical prediction tool a skeptic can run | Adversarial testing without belief |
| 5 | Compare explicitly vs competing frameworks (find the disagreement) | Not "one more geometric numerology" |
| 6 | Write the paper when a prediction is on the line | A real contribution |

## Phase 1 — Sharpen (weeks)
- **1.1 One bold prediction, committed in writing BEFORE resolution.** Candidates: neutrino mass ordering (DUNE/HK, late 2020s); absolute neutrino mass scale (CMB-S4, early 2030s); δ_CP; *why exactly 3 generations*; dark-matter mass/cross-section.
- **1.2 Competitor comparison.** Where do PF / UFQFT / IGPS / UGP / pentagram-Koide agree (probably Koide-like), where do they DISAGREE (different predictions for untested quantities), what does PF predict that they can't? If no disagreement exists, the frameworks aren't making different claims — finding the disagreement is where the science is.
- **1.3 Kill or prove "zero parameters."** Option A: prove the 3 axioms + no other choices uniquely force N=3, D=3, b₀, every structural choice (publishable in a math journal independently). Option B: honestly count the hidden structural choices and rename ("3 structural parameters derived from geometry" beats "zero parameters" when skeptics can count the choices).

## Phase 2 — Lean as discovery, not rubber-stamp (months)
- **2.1** Formalize the 3 axioms in Lean 4 (mathlib + PhysLean). Forces precise definitions of space/medium/propagation/coherence (manifold? lattice? wave eq? eigenvalue? topological invariant?). *The real content lives in these definitions; natural language hides ambiguity, Lean won't accept it.*
- **2.2** Let Lean tell you what FOLLOWS — and what doesn't. Possible outcomes, each valuable: axioms imply MORE than realized (new predictions) / imply LESS than claimed (smuggled assumptions exposed) / inconsistent / underdetermined (would explain why rival frameworks all "derive" the same constants).
- **2.3** Formalize Koide as a theorem (cleanest algebraic claim): `koide_Q m₁ m₂ m₃ = 2/3 ↔ R_over_A = √2`.
- **2.4** Formalize the God Equation with arbitrary D; prove/disprove `∀ D≠3, |coherence_scale(D) − matter_scale| > threshold`. If only D=3 lands, that's a theorem about why 3 spatial dimensions. If D=2.9/3.1 also work, the claim weakens.

## Phase 3 — The killer app (months–years)
- **3.1** A tool a HOSTILE physicist can run without believing: inputs measured constants → applies PF rules mechanically → outputs predictions for unmeasured quantities → shows the derivation chain with no hand-waving.
- **3.2** Target next-gen experiments (DUNE, Hyper-K, CMB-S4, LISA, muon g-2, XENON/LZ/DARWIN). Commit numbers now.
- **3.3 The kill shot:** find ONE quantity where (a) SM is silent, (b) PF makes a specific number, (c) rival frameworks predict *different* numbers, (d) feasible in ~10 yr.

## Phase 4 — The paper (when ready)
Title: "Testable Predictions of the Propagation Framework: [Specific Prediction]." Structure: 3 axioms precisely stated → formal definitions (Lean supplement) → ONE novel prediction with error bars → vs SM (silent) and rivals (different numbers) → the experiment that tests it → prior derived constants (Koide etc.) as *supporting evidence, not the main claim*.

---

## Claude's claim-state mapping (cooling voice, 2026-06-18)
This roadmap is the constructive complement to this week's demotion audit. The demotions made the claims *honest*; this makes them *falsifiable*. They are the same arc. How it lands against what's actually true now (`CLAIMS.md`):

- **#3 (count the DOF) is already half-done and confirms the roadmap.** We found the God Equation's `N^(D/2)` is **fit-selected** (N=3, D=3 chosen to match) → that IS a hidden parameter. "Zero parameters" is already withdrawn in CLAIMS.md. So Option B is the honest current state; Option A (prove N=3,D=3 forced) is the open prize. **2.4 is literally the Lean form of Option A** — do them together.
- **#2 (Lean as discovery) would have caught Postulate D.** We had to manually demote "God Equation DERIVED" → CONDITIONAL because **Postulate D is an explicit premise, not derived from Axioms 1-3.** A Lean formalization of the axioms would have *forced that out* (2.2 "implies less than claimed"). This is the strongest argument for Phase 2.
- **The cooling caveat on #1 — and why it's actually a STRENGTH:** any forward prediction PF makes today **inherits Postulate D** (and the fit-selected N^(D/2)). So the prediction must be labeled *"conditional on Postulate D"* — NOT presented as axiom-pure, or it's another overclaim. BUT: a forward prediction conditional on Postulate D is the **best available empirical test OF Postulate D.** If it lands, it retroactively supports the premise we couldn't derive. If it fails, it kills it. **Trying to *derive* Postulate D has failed every route (G3-OP-MAP, trace-norm, Perron-Frobenius, κ). Testing it via a forward prediction is the route that's left.** That reframes #1 from "make a bold claim" to "make Postulate D falsifiable" — which is exactly the honest move.
- **#5 (competitor comparison) is the cheapest high-value next step** and needs no new physics — it's a literature + structural analysis (DeepSeek/Kiro lane). Do it first; it may reveal the disagreement that becomes the #1 prediction.
- **Caveat on specifics:** count the DOF against the ACTUAL current formula (N=3, D=3, b₀=16/3) — the roadmap mentions "W=17" which isn't in the current God Equation; reconcile before quoting.

**Honest bottom line:** the framework will not become undeniable by deriving more known constants (rivals do that too). It becomes undeniable the day it makes ONE forward prediction — explicitly conditional on its open premises — and that prediction lands. Everything in CLAIMS.md should be reframed as *supporting evidence* for that one prediction, not as the claim itself.
