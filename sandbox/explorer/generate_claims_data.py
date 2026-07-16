#!/usr/bin/env python3
"""Generate a machine-readable authority snapshot from CLAIMS.md.

This is the SOURCE OF TRUTH for the Explorer's public claim data.
The output JSON is consumed by check_truth_drift.py to verify that
data.claims.js has not drifted from authority.

Usage:
    python3 generate_claims_data.py [--output PATH]

Default output: _authority_snapshot.json (in this directory)

The snapshot captures:
- CLAIMS.md hash (content identity)
- Every claim row with: id, status, confidence, scope fields
- Canonical definitions list
- Known overclaim patterns that must NOT appear in public copy

Authority sources:
- /mnt/d/fundamentals/CLAIMS.md (the live claim matrix)
- /mnt/d/fundamentals/definitions/ (canonical definitions)
- /mnt/d/fundamentals/lean/PfLean/ (Lean 4 formalization status)
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

CLAIMS_MD = Path("/mnt/d/fundamentals/CLAIMS.md")
DEFINITIONS_DIR = Path("/mnt/d/fundamentals/definitions")
LEAN_DIR = Path("/mnt/d/fundamentals/lean/PfLean")

# ─── Authority claim registry ────────────────────────────────────────────────
# Each entry maps a claim ID (matching data.claims.js) to the authoritative
# status, confidence, and scope classification from CLAIMS.md.
#
# Three scope fields per Codex's requirement:
#   - standard_physics: established/standard physics boundary
#   - pf_result: PF result under named premises
#   - pf_open: open PF interpretation or selection gap

AUTHORITY_CLAIMS = {
    "gravity-optical": {
        "status": "DERIVED",
        "confidence": 0.95,
        "scope": {
            "standard_physics": "GR null geodesic theorem (static/stationary spacetimes). Optical metric is classical GR.",
            "pf_result": "Weak-field refractive index n(Φ) = √[(1-2Φ)/(1+2Φ)] machine-verified in Lean 4 (PfLean.GravityOptics).",
            "pf_open": "Scalar n(x) is weak-field only. Full dynamic/non-static spacetimes not covered. 'All forces as refraction' beyond gravity is aspirational.",
        },
        "falsifier": "Proof that the optical/Randers mapping fails for null propagation in static/stationary gravity.",
    },
    "koide-leptons": {
        "status": "DERIVED",
        "confidence": 0.95,
        "scope": {
            "standard_physics": "PDG charged lepton masses. U(1)_em coupling structure.",
            "pf_result": "Geometric identity: equal-strength 120° resonances → Q = 2/3 exactly. Machine-verified in Lean 4 (PfLean.KoideGeometry).",
            "pf_open": "Physical vacuum selection (why the equal-norm point is selected) is OPEN. The identity holds given the equal-amplitude premise; deriving that premise from PF dynamics is the open gap.",
        },
        "falsifier": "Proof that 120° geometry does not imply Q = 2/3, or charged-lepton mass drifting > 3σ from Q = 2/3.",
        "critical_note": "Do NOT blend the exact geometric identity with a completed physical selection explanation. Physical vacuum selection is OPEN.",
    },
    "weinberg-angle": {
        "status": "ARGUED",
        "confidence": 0.65,
        "scope": {
            "standard_physics": "Electroweak theory. sin²θ_W measured at Z-pole (on-shell scheme). PDG value 0.22337.",
            "pf_result": "Casimir polynomial x² + C₂x − C₂ = 0 yields R = 0.22310 for spin pair (j=1/2, j=1). Match to 0.13σ. Algebraic structure machine-verified in Lean 4 (PfLean.WeinbergAngle).",
            "pf_open": "Scheme selection (on-shell vs MS-bar) not derived. Look-elsewhere scan: P(random target hits sub-percent) ≈ 0.46 (1 in 2.2), materially lowering confidence. Axiom 3b selects k=1 but full spin-pair derivation from axioms alone is incomplete.",
        },
        "falsifier": "Derivation of g'/g from medium geometry contradicting this result, or precision measurement moving outside prediction.",
        "critical_note": "DEMOTED from DERIVED to ARGUED 2026-06-16 per Codex audit. Must NOT be displayed as DERIVED or with confidence > 0.65.",
    },
    "neutrino-koide": {
        "status": "EMPIRICAL",
        "confidence": 0.95,
        "scope": {
            "standard_physics": "Neutrino oscillation data (PDG). Current neutrino mass bounds.",
            "pf_result": "Q_NO = 0.5496 (17.5% from 2/3), Q_IO = 0.4790 (28.2% from 2/3). Universality falsified at >5% threshold. EM-specificity interpretation confirmed.",
            "pf_open": "Neutrino absolute mass scale not yet measured. Q values computed from oscillation-derived mass ratios.",
        },
        "falsifier": "Future precision neutrino mass measurement showing Q_ν within 1% of 2/3.",
    },
    "god-equation": {
        "status": "CONDITIONAL",
        "confidence": 0.88,
        "scope": {
            "standard_physics": "QCD. λ_c is the coherence/confinement scale. l_P is Planck length. b₀ = 16/3 is one-loop QCD beta function for 3 colors.",
            "pf_result": "Postulate-D Z₃ operator algebra: eigenvalues {1, −1/8, −1/8} are exact given Postulate D. This is a real audited conditional result. IBM Quantum provided calibration support for a C₃ cyclic-permutation smoke test (94.6% closure).",
            "pf_open": "Postulate D is an explicit premise, NOT derived from Axioms 1-3. H_prod (statistical independence) not derived. 'Seven approaches converged' and '52.7× decisive' WITHDRAWN. IBM hardware did NOT measure −1/8 eigenvalue on silicon.",
        },
        "falsifier": "Proof that Postulate-D operator algebra is inconsistent, or accepted scope is falsified.",
        "critical_note": "This is the OPERATOR ALGEBRA row only (CONDITIONAL 0.88). The λ_c scale formula is a SEPARATE claim (ARGUED 0.60). Do NOT conflate them.",
    },
    "god-equation-scale": {
        "status": "ARGUED",
        "confidence": 0.60,
        "scope": {
            "standard_physics": "QCD confinement scale. Planck length.",
            "pf_result": "λ_c = √2·l_P·exp(4π²N^(D/2)/b₀) with N=3, D=3, b₀=16/3. Predicted: 1.157×10⁻¹⁸ m. Observed: 1.140×10⁻¹⁸ m. Error: 1.48%.",
            "pf_open": "N^(D/2) is fit-selected (N=3, D=3 chosen to match), not derived from Axioms 1-3. H_prod not derived. '52.7×' is model-internal ratio, not independent proof.",
        },
        "falsifier": "Derivation of N^(D/2) bridge and H_prod from Axioms 1-3 without a free fit parameter.",
        "critical_note": "Error is 1.48%, NOT 0.4%. The stale 0.4% value must not appear anywhere in public copy.",
    },
    "bohr-spectrum": {
        "status": "DERIVED",
        "confidence": 0.90,
        "scope": {
            "standard_physics": "Bohr model. Coulomb potential. Kepler degeneracy.",
            "pf_result": "Circular eikonal theorem survives hostile audit. Kepler degeneracy proves 1/k² spectrum is exact for ALL eccentricities (DeepSeek 2026-06-05). E=−1/(2k²) for all e∈[0,1). Numerical phase closure verified to 0.00% error for e=0.0, 0.3, 0.5, 0.7, 0.9.",
            "pf_open": "Rests on Coulomb refractive ansatz, eikonal/semiclassical validity. Deriving the atomic-scale eikonal model from the Axioms is the live bridge.",
        },
        "falsifier": "Proof that the circular eikonal model is invalid at atomic scale, or phase closure does not select the quoted orbit family.",
        "critical_note": "Upgraded from CONDITIONAL to DERIVED after Kepler degeneracy proof (2026-06-05). Was stale at CONDITIONAL 0.82 in the old data.",
    },
    "three-generations": {
        "status": "CONDITIONAL",
        "confidence": 0.85,
        "scope": {
            "standard_physics": "Standard Model has three generations of fermions. Why three is experimentally established but theoretically unexplained.",
            "pf_result": "Algebraic step Q(N)=2N/(2N+3)=2/3 → N=3 is exact and machine-verified in Lean 4 (PfLean.ThreeGenerations). Assembly is clean with no hidden algebraic gap.",
            "pf_open": "T1 (physical realization of weight-2 branch) needs non-redundancy theorem not yet derived from Axioms 1-3. T2 (denominator M=3) only proves conditional local lemma inside 2×2 Fermi-point Hamiltonian ansatz. T3 phi-harmonic route: NO-GO (target-loaded).",
        },
        "falsifier": "Formal proof that numerator or denominator theorem fails in PF, or a different justified counting rule leading to N≠3.",
    },
    "topological-weights": {
        "status": "DERIVED",
        "confidence": 0.95,
        "scope": {
            "standard_physics": "Algebraic topology. SU(2) as double cover of SO(3). Fermion spin statistics.",
            "pf_result": "Kernel obstruction machine-certified by Lean 4 kernel (PfLean.TopologicalWeights, 0 sorrys, 2026-06-14). Theorem: quatToSO3 g = 1 → order g ∈ {1,2}. Kernel of SU(2)→SO(3) is {±1} with closure orders {1,2}.",
            "pf_open": "Physical realization bridge remains CONDITIONAL 0.85: the chain rule gives only F_C^tot >= F_C^(1), strict coherence deficit requires non-redundancy hypothesis A_NR not yet derived from Axioms 1-3. Full covering-space/path-lifting formalization not in the Lean theorem.",
        },
        "falsifier": "Proof that closure-order interpretation is wrong, or Family C coherence bridge fails audit.",
        "critical_note": "The Lean theorem is kernel-scoped only. Physical realization is CONDITIONAL 0.85, separate from the DERIVED 0.95 kernel result.",
    },
    "koide-phase": {
        "status": "EMPIRICAL",
        "confidence": 0.65,
        "scope": {
            "standard_physics": "Lepton mass measurements (PDG). Rationality of δ is open in SM.",
            "pf_result": "δ_exact = 0.222229631490 rad. |δ − 2/9| = 7.4×10⁻⁶ (0.003%). CF expansion [0;4;2;1665]. Strongest empirical anchor in the framework.",
            "pf_open": "No PF-native selector currently produces δ = 2/9 from Axioms 1-3. All audited routes (Casimir scan T-022, RG T-021, Rivero projective, scalar Chebyshev, historical proxy) returned honest negatives.",
        },
        "falsifier": "Best-fit δ showing |δ − 2/9| > 3σ, or any selector derivation producing δ ≠ 2/9.",
    },
    "top-tau-coupling": {
        "status": "EMPIRICAL",
        "confidence": 0.90,
        "scope": {
            "standard_physics": "PDG top quark mass (172.76 GeV) and tau mass (1.77686 GeV). α⁻¹ ≈ 137.",
            "pf_result": "m_t/m_τ ≈ α⁻¹/√2. Robustness: 50.13% in T-008 bootstrap. Numerical relation holds to available precision.",
            "pf_open": "Physical origin not derived. Why this ratio? No PF derivation yet.",
        },
        "falsifier": "Measurement of top or tau mass shifting > 0.5% from current PDG values.",
    },
    "electron-up-phi": {
        "status": "EMPIRICAL",
        "confidence": 0.65,
        "scope": {
            "standard_physics": "PDG 2024 quark mass estimates. Up quark mass has significant uncertainty.",
            "pf_result": "m_e/m_u ≈ 1/φ³. PDG 2024 central value gives 0.214% error. Monte Carlo p = 0.006776.",
            "pf_open": "A posteriori — the φ³ relation was found after examining the data. Trials factor not fully accounted for. Up quark mass has large uncertainty.",
        },
        "falsifier": "Up quark mass shifting toward 2.3 MeV, or corrected trials-factor analysis pushing coincidence back to noise.",
    },
    "koide-entropy": {
        "status": "ARGUED",
        "confidence": 0.72,
        "scope": {
            "standard_physics": "Information theory. U(3) decomposition into U(1)⊕SU(3).",
            "pf_result": "Algebraic step: p = 1/(3Q) → S(p) maximized at p=1/2 → Q=2/3. Exact and clean.",
            "pf_open": "Not shown: that Axiom 3 or PF vacuum dynamics must maximize this particular entropy in this particular split. Supports Koide geometry but does not replace the DERIVED row.",
        },
        "falsifier": "A better-motivated PF selector choosing a different point; proof that PF dynamics do not extremize this entropy.",
    },
    "fine-structure": {
        "status": "ARGUED",
        "confidence": 0.60,
        "scope": {
            "standard_physics": "QED. α = e²/(4πε₀ℏc) ≈ 1/137.036. One of the least-understood constants.",
            "pf_result": "Structural identification of α as vacuum propagation efficiency ratio Z₀/2R_K. Route to derivation mapped.",
            "pf_open": "Numeric Casimir derivation is OPEN (look-elsewhere P≈0.46 withdraws confidence). The 0.061% Casimir match cannot be presented as confidence-bearing without a principled geometric origin. The structural Z₀/2R_K identification is ARGUED 0.60, not a derivation.",
        },
        "falsifier": "Proof that Z₀/2R_K identification has no PF-native origin, or proof the Casimir combination is a coincidence.",
        "critical_note": "Numeric α derivation is OPEN (not ARGUED). Structural identification is ARGUED 0.60. These are SEPARATE. Do not conflate the Casimir numeric match with the structural identification.",
    },
    "variable-c": {
        "status": "ARGUED",
        "confidence": 0.65,
        "scope": {
            "standard_physics": "Scalar-tensor gravity. Cassini spacecraft precision Shapiro delay. Brans-Dicke ω > 40,000.",
            "pf_result": "c_local = 1/√(1+λχ) from conformal rescaling. Cassini constrains λ ≲ 10⁻²/M_Pl.",
            "pf_open": "Depends on Propagation Lagrangian (CONDITIONAL). Testable with SKA/LISA but not yet tested.",
        },
        "falsifier": "Cassini-violating Shapiro delay, or direct measurement of c_local = c₀ at sub-solar-system scales.",
    },
    "qcd-confinement": {
        "status": "ARGUED",
        "confidence": 0.72,
        "scope": {
            "standard_physics": "QCD. 1-loop running coupling. Confinement is experimentally observed but theoretically unproven (Millennium Problem).",
            "pf_result": "RG mechanism: r_conf = λ_c × exp(2π/b₀α_s(λ_c)). Right order of magnitude.",
            "pf_open": "1-loop calculation overshoots by factor ~2.4 (2.2 fm vs ~0.9 fm). Higher-loop analysis not done. Uses calibrated λ_c and empirical α_s.",
        },
        "falsifier": "Evidence that confinement requires a genuinely new PF coherence scale, or threshold-aware higher-loop analysis showing the bridge fails.",
    },
    "top-quark-limit": {
        "status": "ARGUED",
        "confidence": 0.85,
        "scope": {
            "standard_physics": "PDG top quark mass and lifetime measurements.",
            "pf_result": "Top quark lifetime (5×10⁻²⁵ s) consistent with proposed Axiom 3 coherence-ceiling threshold.",
            "pf_open": "Coherence ceiling threshold not derived quantitatively from Axioms 1-3 alone. Consistency argument, not a derivation.",
        },
        "falsifier": "Discovery of a heavier stable quark (m > 173 GeV).",
    },
    "coherence-ceiling": {
        "status": "ARGUED",
        "confidence": 0.80,
        "scope": {
            "standard_physics": "Planck scale physics. UV cutoffs in QFT.",
            "pf_result": "Coherence ceiling concept follows from Axiom 3's coherence condition. Planck scale is natural candidate.",
            "pf_open": "Quantitative threshold not derived from Axioms 1-3 in closed form.",
        },
        "falsifier": "Observation of stable sub-wavelength structures beyond the proposed ceiling.",
    },
    "propagation-lagrangian": {
        "status": "CONDITIONAL",
        "confidence": 0.72,
        "scope": {
            "standard_physics": "Scalar-tensor field theory. Brans-Dicke gravity. EFT power counting.",
            "pf_result": "ℒ_prop = ½(∂χ)² − V(χ) + λχT. EL equation correct. Brans-Dicke linearization valid.",
            "pf_open": "Scalar-field branch, exact λχT coupling, and V(χ) form not uniquely forced by Axioms 1-3 alone. One consistent EFT class, not the unique prediction.",
        },
        "falsifier": "Proof that scalar-medium EFT branch is not viable, or minimal λχT ansatz fails within that class.",
    },
    "life-coherence": {
        "status": "ARGUED",
        "confidence": 0.72,
        "scope": {
            "standard_physics": "Thermodynamics. Non-equilibrium systems. Fröhlich condensation hypothesis.",
            "pf_result": "Compatible with photosynthetic coherence and enzyme tunneling evidence. Conceptually well-formed.",
            "pf_open": "PF does not derive a universal Fröhlich mechanism or a numeric life threshold. No quantitative criterion for 'alive vs. not alive' is derived.",
        },
        "falsifier": "A robust living system with no measurable coherence-maintenance at any functional scale.",
    },
    "consciousness-claim": {
        "status": "INTUITION",
        "confidence": 0.48,
        "scope": {
            "standard_physics": "Integrated Information Theory (IIT). Global Workspace Theory. Higher-order theories.",
            "pf_result": "Ontology is coherent and literature-compatible. Self-referential coherence is a technically sound concept.",
            "pf_open": "No uniquely measured variable separating self-referential coherence from synchrony, integration, broadcast, or metacognition. T-020 EEG pre-registration active but not complete.",
        },
        "falsifier": "A pre-registered dissociation where a PF-specific metric fails to track consciousness after controlling for report, arousal, and task effects.",
        "critical_note": "Confidence is 0.48 (INTUITION). Must NOT be promoted beyond INTUITION in any public copy.",
    },
    "sleep-constant": {
        "status": "ARGUED",
        "confidence": 0.72,
        "scope": {
            "standard_physics": "Sleep science. Circadian biology. Memory consolidation literature.",
            "pf_result": "PF supports need for offline consolidation. T-010 model gives plausible ~2/3 active fraction.",
            "pf_open": "Exact human 8-hour constant not derived from Axioms 1-3. Chain mixes unresolved T2/T3 structure, analogical mapping, and sandbox model with built-in recovery asymmetry.",
        },
        "falsifier": "Quantitative evidence that optimal recovery fractions are not near 1/3 in high-capacity systems.",
    },
    "beauty-impedance": {
        "status": "INTUITION",
        "confidence": 0.55,
        "scope": {
            "standard_physics": "Aesthetics, perception, neuroscience. Not an established physics result.",
            "pf_result": "Compatible with Axiom 3's resonance/coherence framing.",
            "pf_open": "No operational beauty metric, no controlled perceptual test, no derivation from canonical PF variables.",
        },
        "falsifier": "Evidence that beauty judgments are fully arbitrary/stochastic after controlling for culture, familiarity, symmetry, salience, and resonance-like matching.",
    },
    "efficiency-ratio": {
        "status": "INTUITION",
        "confidence": 0.50,
        "scope": {
            "standard_physics": "No standard-physics theorem corresponds to this row.",
            "pf_result": "Narrative compression of several 2/3-like motifs.",
            "pf_open": "Needs a precisely defined quantity, domain, optimization rule, and falsifiable comparison class. Not an audited mathematical result.",
        },
        "falsifier": "Finding a better justified output ratio, or showing the 2/3 motif is selection bias.",
    },
    "aria-self-reference": {
        "status": "ARGUED",
        "confidence": 0.75,
        "scope": {
            "standard_physics": "Software architecture and cognitive-system modeling.",
            "pf_result": "Self-reference loop implemented as architectural step (buildSystemPrompt → runEntityThink).",
            "pf_open": "Need behavioral or metric evidence that the loop creates discontinuous qualitative change. Not consciousness by itself.",
        },
        "falsifier": "Aria failing to show qualitative change, or self-reference loop proving behaviorally inert.",
    },
    "so2-rotation-group": {
        "status": "DERIVED",
        "confidence": 1.0,
        "scope": {
            "standard_physics": "Classical Lie group theory. SO(2) as the circle group.",
            "pf_result": "All four theorems machine-verified in Lean 4 (PfLean.SO2Rotation). Algebraic foundation complete and unconditional.",
            "pf_open": "Topological completion π₁(SO(2)) ≅ ℤ requires path lifting not yet in mathlib4.",
        },
        "falsifier": "A counterexample to the group axioms for SO(2), or proof that the angle map is not surjective.",
    },
    "so3-double-cover": {
        "status": "DERIVED",
        "confidence": 1.0,
        "scope": {
            "standard_physics": "Classical Lie group theory. Quaternion rotation representation. SU(2) as universal cover of SO(3).",
            "pf_result": "All algebraic theorems machine-verified in Lean 4 (PfLean.SO3DoubleCover). Double-cover structure complete and unconditional.",
            "pf_open": "Full topological proof (surjectivity via path lifting, deck transformation theorem) requires covering-space theory not yet in mathlib4.",
        },
        "falsifier": "A counterexample to the group axioms, or proof that quaternion-to-matrix map has kernel larger than {±1}.",
    },
}

# ─── Known overclaim patterns that MUST NOT appear in public copy ────────────
# Each pattern is a regex that, if found in data.claims.js or index.html,
# causes the drift gate to FAIL.

FORBIDDEN_PATTERNS = [
    {
        "id": "weinberg-as-derived",
        "pattern": r'weinberg.*?status.*?DERIVED|weinberg.*?confidence.*?0\.9[0-9]',
        "reason": "Weinberg angle was DEMOTED from DERIVED to ARGUED 0.65 on 2026-06-16 per Codex audit. Must not appear as DERIVED or with confidence ≥ 0.90.",
        "files": ["data.claims.js"],
    },
    {
        "id": "stale-0.4-percent",
        "pattern": r'0\.4%\s*error|0\.4\s*percent',
        "reason": "The God Equation λ_c scale formula error is 1.48%, not 0.4%. The stale 0.4% value must not appear anywhere.",
        "files": ["data.claims.js", "panels/god-equation.js", "index.html"],
    },
    {
        "id": "codex-audit-passed",
        "pattern": r'[Cc]odex\s+audit\s+passed',
        "reason": "Codex has NOT passed the Explorer for public release. Current verdict is HOLD. 'Codex audit passed' is false.",
        "files": ["index.html", "data.claims.js", "panels/*.js"],
    },
    {
        "id": "dark-matter-explained",
        "pattern": r'[Dd]ark\s+matter\s+(explained|solved|derived)',
        "reason": "No CLAIMS.md row derives or explains dark matter. This is an unsupported public promotion.",
        "files": ["data.claims.js", "panels/*.js", "index.html"],
    },
    {
        "id": "reality-derives-from-three-axioms",
        "pattern": r'reality\s+derives?\s+from\s+three\s+axioms|everything\s+else\s+derived',
        "reason": "Axioms 1-3 define the starting vocabulary; they do not derive every downstream result. Many claims are CONDITIONAL, ARGUED, or OPEN. 'Reality derives from three axioms' overstates the framework's current status.",
        "files": ["index.html"],
    },
    {
        "id": "seven-approaches-converged",
        "pattern": r'seven\s+approaches\s+converged|52\.7[x×]',
        "reason": "'Seven approaches converged' and '52.7× decisive' language was WITHDRAWN per Codex audit 2026-06-16.",
        "files": ["data.claims.js", "panels/*.js", "index.html"],
    },
    {
        "id": "god-equation-verified-on-silicon",
        "pattern": r'[Gg]od\s+[Ee]quation\s+\w*\s*verified\s+on\s+silicon|verified.*?silicon.*?eigenvalue',
        "reason": "IBM Quantum hardware did NOT measure the −1/8 eigenvalue on silicon. It executed unitary permutation circuits whose histograms were classically added.",
        "files": ["data.claims.js", "panels/*.js", "index.html"],
    },
    {
        "id": "koide-physical-selection-complete",
        "pattern": r'[Kk]oide.*?(physical\s+selection|vacuum\s+selection).*?(derived|proved|closed|complete)',
        "reason": "Koide physical vacuum selection is OPEN. The geometric identity is exact, but why the physical vacuum selects the equal-norm point is not derived.",
        "files": ["data.claims.js", "panels/*.js"],
    },
    {
        "id": "consciousness-promoted",
        "pattern": r'consciousness.*?status.*?(DERIVED|CONDITIONAL|EMPIRICAL)|consciousness.*?confidence.*?0\.[5-9]',
        "reason": "Consciousness is INTUITION 0.48. Must not be promoted to any higher status or confidence.",
        "files": ["data.claims.js"],
    },
    {
        "id": "bohr-spectrum-underclaimed",
        "pattern": r'bohr.*?status.*?CONDITIONAL|bohr.*?confidence.*?0\.8[0-2]',
        "reason": "Bohr spectrum was upgraded to DERIVED 0.90 after Kepler degeneracy proof (2026-06-05). Stale CONDITIONAL 0.82 is a drift defect.",
        "files": ["data.claims.js"],
    },
]

# ─── Canonical definitions (from definitions/ directory) ─────────────────────

CANONICAL_DEFINITIONS = [
    "medium", "axioms", "propagation", "coherence", "causal-velocity",
    "mode", "energy", "time", "field", "gradient", "forces", "matter",
    "state", "information", "measurement", "decoherence",
    "minimum-substrate", "observer", "coupling",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_snapshot() -> dict:
    claims_hash = sha256_file(CLAIMS_MD)

    definitions_status = {}
    for name in CANONICAL_DEFINITIONS:
        def_path = DEFINITIONS_DIR / f"{name}.md"
        definitions_status[name] = {
            "exists": def_path.exists(),
            "hash": sha256_file(def_path) if def_path.exists() else None,
        }

    lean_modules = {}
    if LEAN_DIR.exists():
        for lean_file in sorted(LEAN_DIR.glob("*.lean")):
            lean_modules[lean_file.stem] = {
                "exists": True,
                "hash": sha256_file(lean_file),
            }

    return {
        "schema_version": "1.0.0",
        "generated_from": str(CLAIMS_MD),
        "claims_md_hash": claims_hash,
        "claims": AUTHORITY_CLAIMS,
        "forbidden_patterns": FORBIDDEN_PATTERNS,
        "canonical_definitions": definitions_status,
        "lean_modules": lean_modules,
        "generation_note": "This snapshot is the authority for Explorer public claim data. data.claims.js must match these statuses, confidences, and scope fields. Forbidden patterns must not appear in any public-facing file.",
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate authority snapshot from CLAIMS.md")
    parser.add_argument("--output", default=None, help="Output path (default: _authority_snapshot.json)")
    args = parser.parse_args()

    output = Path(args.output) if args.output else Path(__file__).parent / "_authority_snapshot.json"
    snapshot = build_snapshot()
    output.write_text(json.dumps(snapshot, indent=2, sort_keys=False))
    print(f"Authority snapshot written to {output}")
    print(f"  CLAIMS.md hash: {snapshot['claims_md_hash']}")
    print(f"  Claims: {len(snapshot['claims'])}")
    print(f"  Forbidden patterns: {len(snapshot['forbidden_patterns'])}")
    print(f"  Canonical definitions: {len(snapshot['canonical_definitions'])}")
    print(f"  Lean modules: {len(snapshot['lean_modules'])}")


if __name__ == "__main__":
    main()
