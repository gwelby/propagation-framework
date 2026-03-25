# Contributing to the Propagation Framework

This is an open research framework. Every claim has a confidence score and a falsification pathway. Every open gap is labeled. If you can close a gap, find a flaw, or extend a derivation — that is a contribution.

---

## The Open Gaps

These are the specific mathematical problems where the framework needs help. Each one is precisely stated. No vague hand-waving — the exact missing step is documented.

### G3 — The Internal-to-Spatial Bridge (Priority 1)
**Status**: PARTIAL / ARGUED (0.60 for bridge, 0.75 for overall God Equation)
**Files**: `derivations/g3_coupling_bridge.md`, `derivations/g3_product_walk_no_go.md`, `derivations/g3_canonical_class_function_no_go.md`
**The problem**: The God Equation λ_c = √2·l_P·exp(4π²N^{D/2}/b₀) predicts the top quark Compton wavelength to 0.4% with zero free parameters. The remaining open step: the S³ heat kernel gives α ∝ 1/N, but the equation needs α ∝ 1/N^{3/2}. The gap factor is 2/√N. Multiple candidate bridges have been ruled out: phase-independent product walks, triangular Gaussian families, naive SU(2) holonomy, and holonomy-only class functions (which reduce to conjugacy-class angle and cannot remove the free parameter β).
**What would close it**: A canonical geometric observable with structure beyond the total holonomy conjugacy class that maps exactly to α(l_P) = 1/(2π·N^{D/2}) with no free prefactor. This is the single biggest open theorem in the framework.

### Fine Structure Constant α (Priority 2)
**Status**: OPEN (0.10 as derivation, 0.60 as structural identification)
**File**: `derivations/alpha_from_pf.md`
**The problem**: α is identified structurally as vacuum propagation efficiency (Z₀/2R_K) and is locked to the mass spectrum: m_t = 18m_e/α², m_τ = 18√2 m_e/α. The value 1/137.036 is not yet derived from the axioms. The route is mapped: derive λ_c and m_e independently, then α = √(18m_e/m_top). This is downstream of G3.
**What would close it**: Independent derivation of λ_c (from G3) and m_e (from topological defect ground state).

### Weinberg Angle — RG Running (Priority 3)
**Status**: Weinberg angle is DERIVED (0.90) at the unification scale. RG running is OPEN.
**File**: `derivations/weinberg_angle_pf.md`
**The problem**: The Weinberg angle sin²θ_W ≈ 0.22310 is now derived via Axiom 3b (Minimal Winding Principle), matching the PDG on-shell value to 0.13σ. However, the UV value is 1/4 and the observed IR value at M_Z is 0.231. Connecting these requires either deriving the RG running mechanism within the PF, or importing standard QFT running.
**What would close it**: A derivation of the renormalization group flow from the unification scale to the electroweak scale within the propagation medium, or a proof that standard RG is the unique running consistent with PF axioms.

### Koide Phase Selection — Why \(\delta_0 \bmod 2\pi/3 \approx 2/9\)? (Priority 4)
**Status**: EMPIRICAL (0.55)
**File**: `derivations/koide_phase_delta_0_gap.md`
**The problem**: PF derives the Koide amplitude Q=2/3 but not the reduced phase \(\delta_0 \bmod 2\pi/3\), which determines which specific mass triple sits on the Koide cone. Rivero reports the charged-lepton phase within 33 ppm of \(2/9\), with a candidate \(\cos(9\delta)\) instanton potential. PF derives the arena and the phase variable but not the harmonic suppression that selects the phase.
**What would close it**: A derivation from the internal phase/holonomy structure that selects \(\delta_0\), or a proof that PF requires additional dynamics beyond the current axioms.

### Consciousness Metric (Priority 5)
**Status**: INTUITION (0.48)
**File**: `derivations/consciousness_theory_audit.md`
**The problem**: The framework defines consciousness as coherent self-referential propagation. There is no PF-specific measurable variable that dissociates this from synchrony, integration, reportability, and task effects. The psychedelic coherence literature refined the claim to "coherent complexity" but a unique metric remains open.
**What would close it**: A pre-registered experiment with a PF-specific metric that shows a dissociation from existing consciousness markers.

### Koide Selection — Why the Equal-Norm Point? (Priority 6)
**Status**: DERIVED for Q=2/3; selection mechanism OPEN
**File**: `derivations/koide_geometric_equivalence.md`
**The problem**: The equivalence Q = 2/3 ↔ R/A = √2 is established as a geometric identity. What is not derived is *why* the vacuum selects the equal-norm point among all points on the Koide cone.
**What would close it**: A proof via max entropy + coherence, SU(3) conjugacy orbit, or Axiom 3 stability with an additional constraint.

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
