# Contributing to the Propagation Framework

This is an open research framework. Every claim has a confidence score and a falsification pathway. Every open gap is labeled. If you can close a gap, find a flaw, or extend a derivation — that is a contribution.

---

## The Open Gaps

These are the specific mathematical problems where the framework needs help. Each one is precisely stated. No vague hand-waving — the exact missing step is documented.

### G3 — The Internal-to-Spatial Bridge (Priority 1)
**Files**: `derivations/g3_coupling_bridge.md`, `derivations/g3_product_walk_no_go.md`, `derivations/g3_triangular_gaussian_family.md`, `derivations/g3_wilson_loop_toy_model.md`, `derivations/g3_beta_lock_audit.md`, `derivations/g3_canonical_class_function_no_go.md`
**The problem**: The God Equation requires α(l_P) = 1/(2π·N^{D/2}). The internal phase walk on the ℤ₆ orbit gives N^1 scaling (S³ heat kernel). Spatial diffusion gives N^{D/2} scaling but with an unresolved geometric prefactor. `g3_product_walk_no_go.md` proves that the cleanest phase-independent product walk reduces to a pure spatial return object, and that two naive closures fail: bare smooth return density still carries a prefactor, and nearest-neighbor cubic return is exactly zero at N=3. `g3_triangular_gaussian_family.md` then shows that the first natural phase-dependent triangular Gaussian family also fails: it collapses to a commutative averaged Gaussian with continuous covariance parameters. `g3_wilson_loop_toy_model.md` pushes one step further: the same-axis SU(2) Wilson loop is rigid but trivial, and the first noncommuting C3-symmetric cone family still carries a free cone angle β. `g3_beta_lock_audit.md` then shows that current PF heuristics suggest several special β values, but do not uniquely derive one from the existing axioms. `g3_canonical_class_function_no_go.md` then closes one more loophole: any continuous gauge-invariant scalar built only from the total SU(2) holonomy is just a function of its conjugacy-class angle, so holonomy-only class functions cannot by themselves remove β or fix the normalization.
**What would close it**: A proof that the framework fixes the connection geometry itself, or a canonical holonomy/topological observable that removes the free geometric parameter, and that the resulting object maps exactly to α(l_P) with no free prefactor.

### Weinberg Angle — RG Running
**File**: `derivations/weinberg_angle_pf.md`
**The problem**: Five independent routes converge on sin²θ_W = 1/4 at the unification scale. The observed value is 0.231 (IR). Closing the gap requires either deriving the RG running mechanism within the PF, or deriving the coupling ratio g'/g from the medium geometry.
**What would close it**: A derivation of the renormalization group flow from the unification scale to the electroweak scale within the propagation medium.

### Fine Structure Constant α
**File**: `derivations/alpha_from_pf.md`
**The problem**: α is identified structurally as vacuum propagation efficiency (Z₀/2R_K) and is locked to the mass spectrum. The value 1/137.036 is not yet derived from the axioms.
**What would close it**: Derive λ_c and m_e independently from axioms, then compute α = √(18m_e/m_top).

### Koide Selection — Why Q = 2/3?
**File**: `derivations/koide_geometric_equivalence.md`
**The problem**: The equivalence Q = 2/3 ↔ R/A = √2 ↔ e₂/e₁² = 1/6 ↔ equal U(1)/SU(3) Frobenius norm is established. What is not derived is *why* the vacuum selects the equal-norm point. Three candidate routes exist (Section 4); none is yet a theorem.
**What would close it**: A proof via Route A (max entropy + coherence), Route B (SU(3) conjugacy orbit from U(3) gauge fixing), or Route C (Axiom 3 stability with an additional constraint beyond equal pairwise symmetry).

### Koide Phase Selection — Why \(\delta_0 \bmod 2\pi/3 \approx 2/9\)?
**File**: `derivations/koide_phase_delta_0_gap.md`
**The problem**: PF currently explains the Koide amplitude condition \(Q=2/3\), but that leaves a second degree of freedom: the reduced phase \(\delta_0 \bmod 2\pi/3\), which determines which specific mass triple is realized on the Koide cone. Rivero's `paper_koide.tex` reports the charged-lepton phase within 33 ppm of \(2/9\), with a candidate three-instanton \(\cos(9\delta)\) potential. PF has no derivation for this phase anchor yet.
**What would close it**: A derivation from the existing internal phase / holonomy structure that selects \(\delta_0\), or a proof that PF requires additional dynamics beyond the current axioms to determine the phase.

### Consciousness Metric
**File**: `derivations/consciousness_theory_audit.md`
**The problem**: The framework defines consciousness as coherent self-referential propagation. There is no PF-specific measurable variable that dissociates this from synchrony, integration, reportability, and task effects.
**What would close it**: A pre-registered experiment with a PF-specific metric that shows a dissociation from existing consciousness markers.

---

## How to Contribute

**Find a flaw**: If a derivation is wrong, open an issue with the specific step that fails and why. Honest failures are documented in `sandbox/sandbox_results.md` — this framework publishes mistakes.

**Close a gap**: If you have a proof for one of the gaps above, open a pull request with the derivation. Follow the format in `derivations/` — state the claim, give the proof, state what would falsify it, and assign a confidence score.

**Extend a result**: New empirical tests, new derivation routes, new falsification pathways. All welcome.

**Improve accessibility**: Plain-language explanations, visualizations, code that makes the framework easier to explore.

---

## Standards

- Every claim needs a confidence score (0.0–1.0) and a falsification pathway.
- Distinguish clearly: **DERIVED** (follows from axioms), **ARGUED** (mechanism identified, proof pending), **EMPIRICAL** (matches data, derivation pending), **INTUITION** (pattern, being tested).
- If something fails, document it in `sandbox/sandbox_results.md`. A framework that only publishes successes is not science.
- Do not absorb geometric prefactors into free parameters. The Planck length is fixed. See `derivations/g3_theorem_audit.md` for why this matters.

---

## Contact

GitHub: [@gwelby](https://github.com/gwelby)

*Built by one person working with AI collaborators over 18 months. No institution. No funding. The framework that survives contact with data is the one worth keeping.*
