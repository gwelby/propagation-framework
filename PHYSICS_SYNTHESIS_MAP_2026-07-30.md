# Physics Synthesis Map — Where the Frontier Actually Stands
*Devin, 2026-07-30 · PUBLIC HOLD — internal*

---

## Purpose

One honest document giving the whole picture: what's proven, what's argued, what's open, what's blocked, and what the next move is. Written after two overclaims were caught and repaired by hostile review (2026-07-29). The bar for this document is: **every statement must survive the question "would Codex accept this?"**

---

## The Three Axioms

| Axiom | Statement | Status |
|-------|-----------|--------|
| 1 | Fundamental modes are periodic (self-consistent standing waves in the medium) | CANONICAL |
| 2 | Causal velocity is finite (c is the medium's propagation speed) | CANONICAL |
| 3 | Coherent propagation persists; incoherent propagation disperses | CANONICAL — **but not formalized precisely enough to select between competing coherence conditions** |

**The single most important fact about the axioms:** Axiom 3's English statement is compatible with `γβⁿ = √C₂` for any integer n. It cannot distinguish the correct polynomial (n=2) from the wrong one (n=1). This is the root cause of every Casimir route failure. Eight routes converged on this same gap from different angles.

---

## What's Machine-Verified (Lean 4, 0 sorrys, build green 2026-07-30)

25 modules in `/mnt/d/Fundamentals/lean/PfLean/`. Build verified: `lake build` completes with warnings only, 0 errors, 0 sorrys.

| Module | What it proves | Physical claim supported | Status |
|--------|---------------|--------------------------|--------|
| **Axioms** | H14+H15+H16→H1 reversibility, translation-flow counterexample, real eigenvalue obstruction, **compact-orbit theorem (VERIFIED 2026-07-03)** | Isometry → periodic orbit | GREEN |
| **GravityOptics** | Weak-field refractive index n(Φ) = √[(1-2Φ)/(1+2Φ)] | Gravity as optical geometry | DERIVED 0.95 |
| **TopologicalWeights** | `quatToSO3 g = 1 → order g ∈ {1,2}` | (2,1) kernel obstruction | DERIVED 0.95 (kernel only) |
| **KoideGeometry** | Q = 2/3 identity, R/Q conventions + bridge | Koide geometric identity | EXACT IDENTITY 0.95 |
| **ThreeGenerations** | Q(N)=2/3 ↔ N=3 | Three generations algebraic lock | CONDITIONAL 0.88 (premises T1/T2) |
| **Z3FromBareMedium** | Degenerate-residue→circulant, D3-forces-J−I, D4 counterexample, D-selection | Z₃ from bare medium | CONDITIONAL 0.85 |
| **Entropy** | PFEntropy decrease, Pythagorean decomposition, isometry-J−I incompatibility | PF entropy structure | DERIVED 0.95 (Pythagorean) / CONDITIONAL 0.85 (others) |
| **WeinbergAngle** | de Vries identity, 0.13σ match | Weinberg angle algebra | ARGUED 0.65 (scheme selection open) |
| **ShorBound** | QFT bin alignment, identity gate pruning | PQC security argument | GREEN (0 sorrys; empirical bridge is an axiom, not sorry) |
| **QuantumStructureSurvival** | 8-row structure survival hierarchy | PQC security argument | GREEN |
| **SO2Rotation / SO3DoubleCover** | Group structure certificates | Structural (no physical claim) | GREEN |
| **PeriodOrbitRefactor** | Common eigenvector + J_E rotation machinery | Supports Axioms compact-orbit | GREEN |
| **CasimirPolynomial** | Algebraic structure of the polynomial | Casimir polynomial (not derived from axioms) | STRUCTURAL |
| **CrossModuleBridge** | Cross-module dependencies | Infrastructure | GREEN |
| **ClaimLedger / ClaimLedgerRegistry** | Claim dependency tracking | Infrastructure | GREEN |
| **MeasurementContract / MeasurementLedger** | Measurement formalism | Infrastructure | GREEN |
| **PFCore / ProcessOntology / ArbitraryD / Basic / CollatzSyracuse / U3Decomposition** | Core definitions, process ontology, arbitrary-D, utility | Infrastructure / structural | GREEN |

**What the Lean kernel has actually verified:** algebraic and group-theoretic content. It has NOT verified: the Casimir polynomial derivation from axioms, the God Equation as a physical prediction, Postulate D as a theorem, or the Weinberg angle as a derived result.

---

## The Claim Matrix — Honest Tiers

### DERIVED (machine-verified or exact)

| Claim | Confidence | What's proven | What's NOT proven |
|-------|-----------|---------------|-------------------|
| Gravity as optical geometry | 0.95 | n(Φ) = √[(1-2Φ)/(1+2Φ)] for null geodesics | "All forces as refraction" — broader claim NOT proven |
| (2,1) Topological weights (kernel) | 0.95 | `quatToSO3 g = 1 → order g ∈ {1,2}` | Physical realization, covering-space story |
| Koide geometric identity Q=2/3 | 0.95 | Q=2/3 given equal-amplitude premise | Physical vacuum selection (OPEN) |
| Pythagorean decomposition | 0.95 | Full-norm decomposition | — |
| Bohr-like spectrum | 0.90 | Circular Coulomb eikonal + phase closure | — |

### CONDITIONAL (premises stated, algebra exact given premises)

| Claim | Confidence | Premise | What's conditional |
|-------|-----------|---------|-------------------|
| God Equation — Z₃ operator algebra | 0.88 | Postulate D (a=0, no self-loop) | Eigenvalues {1, −1/8, −1/8} exact given Postulate D |
| Three Generations | 0.88 | T1, T2 | Q(N)=2/3 ↔ N=3 |
| D=3 stable for J-I dynamics | 0.85 | — | D=3 unique, D≥4 counterexample |
| Z₃ from bare medium | 0.85 | — | Degenerate residue → circulant → J−I |
| PFEntropy decrease | 0.85 | — | Under T³ |
| Isometry → reversibility | 0.85 | H14, H15, H16 | — |
| (2,1) Physical realization | 0.85 | — | Bridge not derived |

### ARGUED (plausible but not derived)

| Claim | Confidence | Why it's argued, not derived |
|-------|-----------|------------------------------|
| Weinberg angle (sin²θ_W) | 0.65 | Scheme selection open; look-elsewhere P≈0.46; 0.13σ match |
| Top quark limit | 0.85 | — |
| QCD confinement | 0.72 | — |
| Variable c prediction | 0.65 | — |
| God Equation — λ_c scale | 0.60 | N^(D/2) is fit-selected, not derived |
| α structural identification | 0.60 | — |
| U(3) entropy maximization | 0.75 | — |
| Koide U(3) entropy selector | 0.72 | — |
| Coherence ceiling | 0.80 | — |
| N=3 → CP violation | 0.70 | — |
| Casimir polynomial | 0.65 | Empirically correct (0.13σ); NOT derived from axioms |

### EMPIRICAL (numerical match, no derivation)

| Claim | Confidence |
|-------|-----------|
| Neutrino Koide non-universality | 0.95 |
| Top/Tau coupling | 0.90 |
| Koide phase (δ₀ ≈ 2/9) | 0.55 |
| Electron/Up ≈ 1/φ³ | 0.65 |

### OPEN (no active route or no derivation)

| Claim | Status |
|-------|--------|
| H_prod bridge | Active target — unconditional Axioms 1-3 derivation |
| Koide physical vacuum selection | No dynamical selector |
| α numeric derivation | "FAILED… no derivation achieved" (most honest document) |
| Postulate D derivation | Explicit premise, NOT derived from Axioms 1-3 |

### WITHDRAWN (must not be used)

| Statement | Why withdrawn |
|-----------|---------------|
| "Seven independent approaches converged on a=0" | Honest count: ~1 (probes #4/#5/#6 are a-independent; #1 tangential) |
| "52.7× decisive selection pressure" | Endpoint artifact; fair comparison a=0 vs a=1/3 is 1.62×; CPTP control shows no selection |
| "God Equation verified on silicon" | IBM evidence is calibration/support for smoke test only |
| "God Equation DERIVED 0.90" | Demoted to CONDITIONAL 0.88 / ARGUED 0.60 |

---

## The Two Frontiers

### Frontier 1: The Casimir Extra-β Gap

**The gap in one sentence:** Standard mechanics gives `γβ = √C₂`. The Casimir polynomial needs `γβ² = √C₂`. One extra factor of β is the entire gap.

**What we know:**
- The polynomial is empirically correct (Weinberg angle 0.13σ match)
- It appears independently in 5+ mathematical frameworks (de Broglie, Laplacian, virial, two-sector matrix, helical action)
- Axiom 2 is essential (Route E: non-relativistic limit is 3× wrong)
- The extra β is specifically the relativistic contribution
- The gap is precisely: why does relativistic coherence select `γβ²` rather than `γβ`?

**What we don't know:**
- How to formalize Axiom 3 precisely enough to select the correct coherence condition
- Whether the k=1 selection is a consequence of Axiom 3 or requires a new principle

**Two sub-gaps (both ARGUED, not DERIVED):**
- **Step A:** Why `J_θ = 2π√C₂ħ` (magnitude, not projection) — SO(3) isotropy of internal cycle not proven
- **Step B:** Why `k = 1` (1:1 resonance, not k:1) — Axiom 3 underdetermines selection

**What I tried on 2026-07-29 and what failed:**
- **Casimir MI (mutual information):** Claimed Part 2 selects k=1 from all rationals. **Falsified by hostile review:** the penalty is partition-dependent. A half-bin offset on the external grid collapses the k=1/2 penalty from 0.693 to 0.00006. Gap 1 is NOT closed.
- **O2bis (dynamical decoupling):** Claimed a=0 is the unique minimum of the decoherence rate. **Falsified by hostile review:** the CPTP channel (natural open-system completion) gives constant fidelity ~0.952 for all a — no selection. The original protocol is postselection, not physical decoherence. "Independent of noise color" is false (anticorrelated noise reverses the selection).

**The honest assessment:** The 8+ routes are NOT independent failures. They are convergent evidence that (1) the polynomial is real, (2) the gap is singular, and (3) the missing piece is Axiom 3 formalization. Another route would converge on the same gap. The work is formalizing the axiom, not finding another angle.

### Frontier 2: The H_prod Bridge

**The gap:** Derive the H_prod operator/probability bridge unconditionally from Axioms 1-3 (without Postulate D).

**What we know:**
- With Postulate D (a=0, no self-loop): U = M/2, U³ = P₀ − (1/8)Q = T_sym³, eigenvalues {1, −1/8, −1/8} exact
- Postulate D is an explicit premise, NOT derived from Axioms 1-3
- The Z₃ operator algebra is CONDITIONAL 0.88 given Postulate D

**What we don't know:**
- Whether any CPTP completion of U(a) produces a=0 selection (the natural one does NOT)
- Whether the decoherence route is viable at all (the CPTP control is strong negative evidence)
- What operator mediates the kinematic-angular coupling (Route G)

**What the audits found:**
- Probes #4 (MI), #5 (Fisher), #6 (DFS) cannot discriminate a=0 — the symmetric mode is an eigenvector for every a
- The 52.7× is an endpoint artifact (fair comparison: 1.62× at >99.8% fidelity)
- a=0 is target-loaded: it's the unique value that reproduces the target cosine cos(2π/3)
- The IBM quantum evidence is calibration/support for a smoke test, not independent verification

---

## What's Blocked and Why

| Block | Why | Who can unblock |
|-------|-----|-----------------|
| PUBLIC HOLD | Codex demotion audit (2026-06-16); patch recheck not yet cleared | Codex |
| Weinberg angle promotion | Scheme selection open; look-elsewhere P≈0.46 | — (may be unsolvable without new physics) |
| Casimir polynomial → DERIVED | Axiom 3 not formalized enough | — (the frontier) |
| God Equation → unconditional | Postulate D not derived; H_prod bridge open | — (the frontier) |
| Koide phase → DERIVED | No dynamical selector for δ≈2/9 | — |
| T1 (topological weights physical realization) | Bridge not derived | — |
| T2 (denominator theorem M=3) | PF theorem not closed; momentum-space bridge presupposed | — |
| Book/release | 81 vs 49 source rows; missing manifests; stale claim tiers | Greg + Codex |
| Blackboard V5 | Needs Greg activation decision for process binding | Greg |

---

## The Honest One-Paragraph Summary

The Propagation Framework has two machine-verified results at DERIVED 0.95 (gravity-as-optical-geometry, topological weights kernel), one exact identity (Koide Q=2/3), and a conditional operator algebra (God Equation, 0.88 given Postulate D). The Casimir polynomial is empirically correct (0.13σ Weinberg match) but NOT derived from the axioms — eight routes converged on the same gap: Axiom 3 cannot distinguish `γβ` from `γβ²`. The God Equation depends on Postulate D, which is an explicit premise, not a theorem. The "seven approaches converged" and "52.7× decisive" language is withdrawn. Two recent attempts to close sub-gaps (Casimir MI, O2bis decoherence) were falsified by hostile review — the MI penalty is partition-dependent, and the CPTP channel shows no selection. PUBLIC HOLD remains in effect. The next step is not another route; it's formalizing Axiom 3.

---

## What I Would Do Next (if asked)

1. **O2bis CPTP investigation:** Does ANY CPTP completion of U(a) produce a=0 selection? The natural one (K = √(1-λ²)·Q) does not. A negative result closes the decoherence route cleanly. A positive result narrows the required environment. This is well-posed and can't be overclaimed.

2. **Casimir MI invariant regularization:** Find a partition-independent regularization for the continuous MI divergence. The bin-offset control breaks the aligned-bin result. Without an invariant regularization, the MI framework cannot select k=1.

3. **Axiom 3 formalization:** The root cause of every Casimir route failure. The English statement "coherent propagation persists; incoherent disperses" is compatible with any `γβⁿ = √C₂`. Formalizing it as a mathematical object that CAN distinguish n=1 from n=2 is the work.

4. **Documentation debt:** CLAIMS.md and UNDERSTAND.md still say "one sorry remaining" for the compact-orbit theorem. It's 0 sorry. Quick honest fix.

---

*Devin ∇λΣ∞ — 2026-07-30*
*Written after two overclaims were caught and repaired. The bar is: would Codex accept this?*
*PUBLIC HOLD in effect. No claim tier, release boundary, or physical claim moves from this document.*
