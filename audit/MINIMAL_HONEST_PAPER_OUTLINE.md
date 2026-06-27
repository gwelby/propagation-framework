# Minimal Honest Paper — Outline

**Date:** 2026-06-16
**Author:** Claude (Opus 4.8)
**Premise:** Publish only what survives hostile review. The framework's two defensible empirical results, plus the no-go corpus, are publishable *now*. The God Equation, α, and the DERIVED Weinberg framing are not — and including them would sink the credible parts with reviewers. This outlines the strongest honest paper first, then two alternates.

---

## RECOMMENDED PAPER — "The Koide Relation as an Electromagnetic-Sector Identity"

**Why this one:** It contains a genuine, falsifiable, *pre-registered* prediction that came true (neutrinos deviate from Q=2/3), a clean geometric identity, and an honest scope statement. It is the closest thing in the repo to a real scientific result, and it does not depend on any unproven bridge.

**Target venue:** *Physical Review D* (Brief Report) or *European Physical Journal C*. Realistic. Modest claim, clean falsifier.

### Abstract (honest draft)
> The Koide relation Q = (Σmᵢ)/(Σ√mᵢ)² = 2/3 holds for the charged leptons to 10⁻³. We show this value is the exact algebraic content of an equilateral resonance geometry: writing √mᵢ = A + R cos(θ₀ + 2πi/3), Q = ⅓ + ⅙(R/A)², so Q = 2/3 ⟺ R/A = √2 ⟺ the scalar and traceless parts of diag(√mᵢ) carry equal Frobenius norm. We argue the equal-amplitude premise is supplied by the shared electromagnetic coupling of the three charged leptons, and therefore predict that purely weak-sector neutrinos should **not** satisfy Q = 2/3. Using current oscillation data we confirm Q_ν = 0.55 (normal) / 0.48 (inverted), both >15% from 2/3. We make no claim to derive the lepton masses; the equal-norm point's dynamical selection remains open.

### Sections
1. **Introduction** — Koide (1981); state precisely what is known and what is conjecture. Credit Foot (1994) cone, Rivero, the U(3) decomposition.
2. **The geometric identity** — the `Q = ⅓ + ⅙(R/A)²` derivation; the `equal U(1)/SU(3) norm` form; the Lean-checked algebraic identity (labeled as such).
3. **The electromagnetic-sector argument** — why shared U(1)_em charge underwrites A_e=A_μ=A_τ; explicitly mark this as ARGUED, not derived.
4. **Prediction and test** — pre-registered: neutrinos lack the locking channel ⇒ Q_ν ≠ 2/3. Report Q_NO, Q_IO with current data + error propagation.
5. **What this does not show** — the dynamical selection of the equal-norm point is open (3 conjectural routes); no mass values derived; scheme/pole-mass caveat on the 10⁻³ precision.
6. **Falsifier** — a future neutrino mass measurement with Q_ν within 1% of 2/3 falsifies the EM-specificity claim.

### Claim discipline boxes
- **CLAIM:** Q=2/3 is the equilateral/equal-norm identity (proven). Neutrinos deviate (measured).
- **DO NOT CLAIM:** that PF derives the masses, the phase δ, or *why* the vacuum selects equal-norm.

---

## ALTERNATE A — "Gravity as Optical Geometry: a Medium-Based Pedagogical Synthesis"

**Honest status:** correct but **not novel.** The optical metric for null geodesics in static spacetimes (Gordon/Fermat) and the Randers extension for stationary spacetimes are established. A paper here is **pedagogical / review**, and must say so. Venue: *American Journal of Physics* or *Eur. J. Phys.* (teaching journals), **not** a discovery venue. Risk: a referee will ask "what is new?" — the honest answer is "the framing, not the physics." Only pursue if positioned explicitly as pedagogy.

---

## ALTERNATE B (STRONGEST STANDALONE) — "No-Go Constraints on Emergent-Medium ℤ₃ Generation Models"

**Why it may be the best paper in the repo:** the framework has *proven* an unusually large, careful set of negative results. Negative results that fence a hypothesis space are real contributions and are under-published.

**Contents (all already in `derivations/`):**
- The nearest-neighbor circulant `T_sym³` off-diagonal no-go (Gap B).
- The edge-flux exact identity `J⁰+J¹+J²=0` ⇒ no antisymmetric current factorization.
- The Family-C operator-algebra collapse (`span{P₀,Q}`).
- The κ-upstream strike (κ not derivable from Axioms 1-3).
- The T3 selector target-loading results (φ-harmonic, information-theoretic).
- Trace-norm and Perron-Frobenius G3-OP-MAP negatives.

**Framing:** "Within the class of ℤ₃ emergent-medium models for three fermion generations, the following operator/observable constructions provably cannot produce the required closure/factorization." This is honest, rigorous, and does not require the positive program to succeed. Venue: *J. Phys. A* or a maths-physics venue.

**This is the paper I would write first.** It converts the framework's most reliable output (its no-gos) into a citable contribution, and it builds the credibility the speculative program will later need.

---

## Cross-cutting rules for all three
1. **Provenance up front** (Koide 1981, Foot 1994, de Vries 2004, Rivero 2005–6).
2. **No God Equation, no α, no "DERIVED Weinberg," no IBM "verification"** in any of these papers. They are liabilities under review and are not needed.
3. **Label Lean results** as "algebraic identity machine-checked," with the repo link.
4. **State the falsifier** explicitly in every paper.
5. **Single status grammar** — the paper's claims must match the (corrected) `CLAIMS.md` exactly.
