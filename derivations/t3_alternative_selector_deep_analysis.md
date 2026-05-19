# T3 Alternative Selector — Deep Analysis

**Date**: 2026-04-23  
**Status**: ANALYSIS — no closure claimed  
**Purpose**: Map what has been tried, identify genuinely new angles for N=3 selection

---

## Executive Summary

The T3 problem is: **why exactly 3 generations?** The algebraic lock `Q(N) = 2N/(2N+3) = 2/3 → N=3` is exact, but imports `(2,1)` weights and `M=3` from unresolved T1/T2 theorems. Any PF-native selector must:

1. Select N=3 uniquely among positive integers
2. Derive from Axioms 1-3 without importing T1/T2 structure
3. Survive the target-leakage test (no bonus for Q=2/3)
4. Provide falsification condition

---

## Part 1: What Has Been Tried and Failed

### 1.1 φ-Harmonic Route (FAILED — Target Leakage)

**Attempt**: Use φ-harmonic coherence maximization to select N=3

**Why it failed**: Codex audit 2026-04-22 showed the scoring function gave N=3 a unique exact-match bonus because Q(3)=2/3. Without that bonus, N=4 wins.

**Key lesson**: The selector gave points for matching the known answer. Circular.

**Files**: `t3_phi_harmonic_closure.md`, `t3_phi_harmonic_closure_codex_audit_2026-04-22.md`

---

### 1.2 Casimir Polynomial Route (FAILED — No δ=2/9)

**Attempt**: T-022 searched for PF-native selector via Casimir polynomial algebra

**Why it failed**: Algebra scan complete — no physical spin assignment in bounded Casimir sector produced x*≈2/9.

**Key lesson**: The Casimir-only sector is too narrow to capture the Koide phase.

**Files**: `casimir_polynomial_synthesis.md`, ACTIVE_ISSUES.md T-022 entry

---

### 1.3 RG Crossing Route (FAILED — Convention Audit)

**Attempt**: T-021 explored whether sin²θ_W runs to δ at μ≈98 GeV

**Why it failed**: No audited Standard Model convention supports this sentence. Direct on-shell ratio is fixed; MS-bar running stays above 2/9.

**Key lesson**: The crossing claim doesn't survive physics convention audit.

**Files**: ACTIVE_ISSUES.md T-021 entry

---

### 1.4 Family C Functional / Mutual Information (STALLED — A_NR Gap)

**Attempt**: Use F_C = I(Φ_int; Φ_ext) as selector, with extremal principle

**Current status**: Proves F_C^tot ≥ F_C^(1), but strict F_C^tot > F_C^(1) requires extra non-redundancy assumption A_NR not derived from Axioms 1-3.

**Gap**: Why does PF force population of available weight-2 branch?

**Files**: `t1_physical_realization_theorem.md`, `axiom3_coherence_functional_spec.md`

---

### 1.5 Cubic Scalar Selector for Koide Phase (SHARPENED — Not N=3)

**Attempt**: Find minimal polynomial selector for δ=2/9 in reduced variable f(δ)

**Current status**: Codex proved minimal exact selector is unique Chebyshev-tuned cubic: Q*(f) = c + √2 k(8f³ + 12f² + 3f - 1/2). This selects cos(9δ), not δ=2/9 specifically.

**Gap**: Why would PF choose that cubic coefficient ratio B:C:D = 3:12:8?

**Files**: `koide_phase_minimal_cubic_selector_spec_2026-04-20.md`

**Note**: This is about PHASE orientation (δ), not GENERATION count (N). Different problem.

---

### 1.6 Walk-Step / Random Walk (INTEGRATED — Not Independent)

**Attempt**: Derive N=3 from generation_as_walk_steps

**Current status**: CLOSED/INTEGRATED. The insight: generations ARE the steps, not separate variables. This is a physical definition in PF, not a mathematical selector theorem.

**Files**: `generation_as_walk_steps.md`

---

## Part 2: What Survives as Honest Foundation

### 2.1 Axiom 3b / Minimal Winding (CLOSED)

**Result**: Selects k=1 in bounded helical family for Weinberg angle

**Why it works**: Genuine extremal principle — lower winding = more coherent = higher F_C score

**Key**: Does not import target answer; selects based on coherence property alone

**Relevance to T3**: Pattern to emulate, but helical family is different from generation-candidate family

---

### 2.2 (2,1) Weights from π₁(SO(3)) = ℤ₂ (CONDITIONAL)

**Result**: Topological weights 2 (fermion) and 1 (boson) follow from 3D topology + phase closure requirement

**Status**: DERIVED 0.90 — but assumes 3D space (M=3 input)

**Gap**: This derives the weights, not why both branches are populated, and imports 3D

**Files**: `topological_weight_from_propagation.md`

---

### 2.3 The Algebraic Lock (CONDITIONAL)

**Result**: If (2,1) and M=3, then Q(N) = 2N/(2N+3) = 2/3 → N=3 uniquely

**Status**: Exact, but conditional on T1/T2

---

## Part 3: Genuinely New Angles to Explore

### 3.1 Information-Theoretic Threshold (UNATTEMPTED)

**Hypothesis**: N=3 is the minimum where coherent information capacity exceeds decoherence rate

**Approach**: 
- Define information capacity C(N) for N-generation system
- Define decoherence rate D(N) from Axiom 3
- Find where C(N) > D(N) uniquely at N=3

**Why different**: Doesn't use Q(N) formula or Q=2/3 target; uses threshold crossing

**Test**: Would N=4 also satisfy C(4) > D(4)? Must show N=3 is unique threshold.

---

### 3.2 Symmetry Breaking Dimension Count (UNATTEMPTED)

**Hypothesis**: The dimension of broken generators dim(G/H) = 3 is forced by minimal coherent structure

**Approach**:
- Start from T1's local ℂ² state space (if T1 closes)
- Natural symmetry G = U(2), residual H = U(1)
- dim(G/H) = 4 - 1 = 3 massive modes
- This M=3 is automatic, not imported

**Why different**: Derives M=3 from representation theory, not from 3D space assumption

**Catch**: Still needs T1 to close first, and assumes U(2) is natural

---

### 3.3 Circulant Closure Self-Consistency (PARTIAL — G3 Connection)

**Hypothesis**: The three-generation circulant structure T = aI + bS̄ + bS̄² has unique algebraic properties at N=3

**Known**: T³ = (a³+b³)I + 3a²bS̄ + 3ab²S̄²

**New angle**: 
- For what N is the circulant algebra closed under cubic power?
- N=3: S̄³ = I, so powers cycle
- N≠3: S̄^N = I, but the cubic doesn't close naturally

**Test**: Does N=3 have unique algebraic closure properties vs N=2,4,5...?

**Files**: `god_eq_path_b_family_c_...` series

---

### 3.4 Coherence Length / Harmonic Cutoff (ATTEMPTED — Needs Sharpening)

**Hypothesis**: Three is minimum for circulation; fourth harmonic would exceed coherence length

**Current status**: Argued in `topological_weight_from_propagation.md` Section 8.3, but not theorem-grade.

**Sharpening needed**:
- Quantify coherence length λ_c from Axiom 3
- Show fourth generation wavelength < λ_c
- Make it a strict inequality, not hand-waving

**Why different**: Uses propagation physics, not algebraic lock

---

### 3.5 Fermi Point Codimension (CONDITIONAL — T2 Route)

**Hypothesis**: In 3D momentum space, generic band-touching point has codimension = 3

**Status**: Proven conditional on local 2×2 Hamiltonian structure

**Gap**: Why must PF have Fermi points? Why must gap-opening perturbations be restoration modes?

**Files**: `t2_denominator_theorem.md`, `t2_fermi_point_bridge.md`

---

## Part 4: Deeper Constraints from Failed Attempts

### 4.1 The Target Leakage Constraint

Any valid selector must pass: if you remove knowledge of the empirical answer, does the selector still pick N=3?

**φ-harmonic failed**: Removed Q=2/3 bonus → N=4 wins

**Implication**: Cannot use Koide ratio, mass values, or SM particle content as input

### 4.2 The Dimension Import Constraint

T2 must derive M=3, not assume 3D space.

**Failed**: All routes assuming 3D space as input

**Implication**: Any route using "3D space" is circular for T2

### 4.3 The Population vs Availability Constraint

T1 gap: why must PF populate available weight-2 branch?

**Failed**: Arguments that "available → must be populated" without extra structure

**Implication**: Need strict coherence deficit proof, not availability argument

---

## Part 5: Sharpest Honest Statement Today

The strongest claim PF can make about T3 without target leakage:

> If stable PF modes must realize both closure classes (2,1) and if PF propagation in 3D supports exactly 3 independent massive restoration modes, then N=3 follows uniquely from Q=2/3.

What remains genuinely open:
1. Why PF populates the weight-2 branch (T1)
2. Why M=3 from native PF structure (T2)  
3. Any PF-native selector that picks N=3 without importing (2,1) or M=3

---

## Part 6: Recommended Next Steps

### Immediate: Sharpen Gaps

1. **Information-theoretic threshold**: Write C(N) vs D(N) model, test for N=2,3,4
2. **Circulant algebra**: Test whether N=3 has unique closure properties under cubic power
3. **Coherence length**: Quantify λ_c from Axiom 3, bound fourth generation

### Medium: Attack T1/T2 Directly

1. **T1**: Close A_NR gap — prove non-redundant information contribution from weight-2 branch
2. **T2**: Close C_mom and C_FP — derive momentum-space structure and Fermi point existence

### Avoid

- Any selector importing Q=2/3, (2,1), or M=3 as bonus
- Assuming 3D space when deriving M=3
- "Available → populated" arguments without strict proof

---

**Status**: ANALYSIS COMPLETE  
**Next**: Implement one sharpened attack path
