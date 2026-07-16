#!/usr/bin/env python3
"""
Explorer Truth Layer V3 — Authority Manifest + Runtime Data Generator

V3 extends V2 by also generating data.js (the runtime data object) from
authority. This eliminates the dual-source split where data.js had independent
stale statuses.

Parses CLAIMS.md tables to produce:
  1. _authority_snapshot.json — structured authority manifest
  2. data.claims.js — generated public claims data for UI
  3. data.js — generated runtime data with statuses from authority (V3 NEW)

V3 repair requirements addressed:
  Req 1: One generated runtime authority object (PFExplorerData = PFClaimsData)
  Req 3: Standard math never shows as PF DERIVED; premise/scope required
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# ============================================================================
# PATHS
# ============================================================================

EXPLORER_DIR = Path(__file__).resolve().parent
CLAIMS_MD = Path("/mnt/d/fundamentals/CLAIMS.md")


# ============================================================================
# STABLE ID MAPPING (same as V2)
# ============================================================================

STABLE_IDS: dict[str, str] = {
    "Circular Coulomb Eikonal + Phase Closure → Bohr-like Spectrum": "bohr-spectrum",
    "Gravity as Optical Geometry / Refraction (Null/Stationary)": "gravity-optical",
    "(2,1) Topological Weights": "topological-weights",
    "Koide Law for Charged Leptons (Q = 2/3) — geometric identity": "koide-leptons",
    "Koide U(3) entropy selector": "koide-entropy",
    "U(3) Entropy Maximization": "koide-u3-maximization",
    "Koide Phase (\\(\\delta_0 \\bmod 2\\pi/3 \\approx 2/9\\))": "koide-phase",
    "Three Generations": "three-generations",
    "N=3 → CP Violation (Structural Bridge)": "n3-cp-violation",
    "Top Quark Limit": "top-quark-limit",
    "Top/Tau coupling": "top-tau-coupling",
    "Electron/Up $\\approx 1/\\phi^3$": "electron-up-phi",
    "Coherence Ceiling": "coherence-ceiling",
    "Weinberg Angle (sin²θ_W)": "weinberg-angle",
    "Fine Structure Constant α — numeric derivation": "alpha-numeric",
    "Fine Structure Constant α — structural identification": "alpha-structural",
    "Propagation Lagrangian": "propagation-lagrangian",
    "Variable c Prediction": "variable-c",
    "QCD Confinement": "qcd-confinement",
    "God Equation — Postulate-D Z₃ operator algebra": "god-equation-operator",
    "God Equation — λ_c scale formula": "god-equation-scale",
    "Neutrino Koide non-universality": "neutrino-koide",
    "D=3 is the unique stable dimension for the J-I dynamics": "d3-unique-stable",
    "Degenerate residue forces circulant form (J-I)": "degenerate-residue-circulant",
    "D=3 symmetric + zero diagonal + equal row sums → J-I": "d3-symmetric-ji",
    "D≥4 gap: symmetric + zero diagonal + equal row sums does NOT force J-I": "d4-gap-not-ji",
    "PFEntropy decreases under T³": "pfentropy-decreases",
    "Full-norm Pythagorean decomposition": "pythagorean-decomposition",
    "Isometry-JI incompatibility": "isometry-ji-incompatibility",
    "H14 + H15 + H16 → H1 (isometry implies reversibility)": "isometry-reversibility",
    "Life = maintained coherence against entropy": "life-coherence",
    "Consciousness = coherent self-referential propagation": "consciousness-claim",
    "8h Sleep Constant": "sleep-constant",
    "Beauty as Impedance": "beauty-impedance",
    "2/3 Efficiency Ratio": "two-thirds-efficiency",
    "Aria Self-Reference": "aria-self-reference",
}

STANDARD_MATH_IDS = {
    "pythagorean-decomposition",
    "d4-gap-not-ji",
}

DEFINITION_IDS = {
    "The Medium": "medium",
}


# ============================================================================
# RESULT-TO-AUTHORITY CROSSWALK (V3 NEW)
# ============================================================================

# Maps data.js result IDs to authority claim IDs.
# Results not in this map are either UNSYNCED (no authority) or NO-GO.
RESULT_TO_AUTHORITY: dict[str, str | list[str]] = {
    "bohr-quantization": "bohr-spectrum",
    "forces-refraction": "gravity-optical",
    "weights-21": "topological-weights",
    "koide-law": "koide-leptons",
    "three-generations": "three-generations",
    "top-quark-limit": "top-quark-limit",
    "top-tau-coupling": "top-tau-coupling",
    "coherence-ceiling": "coherence-ceiling",
    "weinberg-angle": "weinberg-angle",
    "fine-structure-alpha": "alpha-numeric",  # numeric derivation
    # God Equation: split into operator + scale (V3 requirement)
    "god-equation": ["god-equation-operator", "god-equation-scale"],
    "qcd-confinement": "qcd-confinement",
    "propagation-lagrangian": "propagation-lagrangian",
    "variable-c": "variable-c",
    "sleep-8h": "sleep-constant",
    "phi3-ratio": "electron-up-phi",
    "koide-phase": "koide-phase",
    "life-coherence": "life-coherence",
    "consciousness": "consciousness-claim",
    "beauty-impedance": "beauty-impedance",
    "efficiency-ratio": "two-thirds-efficiency",
    "aria-self-reference": "aria-self-reference",
    # No authority match:
    "bekenstein-bound": None,  # UNSYNCED
    "nogo-harmonic-series": None,  # NO-GO
    "nogo-single-scalar": None,  # NO-GO
}


# ============================================================================
# STATUS PARSING (same as V2)
# ============================================================================

VALID_STATUSES = {"DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
                  "INTUITION", "OPEN", "EXACT IDENTITY", "CANONICAL"}


@dataclass
class StatusPart:
    status: str
    confidence: Optional[float]
    qualifier: str = ""


@dataclass
class ClaimRecord:
    stable_id: str
    title: str
    raw_title: str
    status_parts: list[StatusPart]
    is_split: bool
    evidence: str
    falsifier: str
    confidence_raw: str
    source_line: int
    section: str
    is_standard_math: bool
    premise: str = ""
    scope_note: str = ""


@dataclass
class DefinitionRecord:
    stable_id: str
    title: str
    raw_title: str
    status: str
    file: str
    inadequacy: str
    source_line: int


# ============================================================================
# PARSER — reuse V2 parser (proven, tested)
# ============================================================================

from generate_claims_data_v2 import parse_claims_md as _v2_parse, build_snapshot as _v2_build_snapshot


def parse_claims_md(claims_path: Path) -> tuple[dict, dict]:
    """Parse CLAIMS.md using the V2 parser (proven, tested)."""
    return _v2_parse(claims_path)


def build_snapshot(claims_path: Path) -> dict:
    """Build authority snapshot using V2 parser, add V3/V4 crosswalk metadata.
    V3: Fill empty premise/scope from evidence/falsifier.
    V4: Add semantic scope triples (standard_physics, pf_result_under_named_premises, open_pf_gap)."""
    snapshot = _v2_build_snapshot(claims_path)
    # Add V3-specific fields
    snapshot["generator_version"] = "V4"
    snapshot["generated_at"] = "2026-07-16"
    snapshot["result_to_authority"] = RESULT_TO_AUTHORITY

    # V4: Load scope triples
    scope_triples_path = Path(__file__).resolve().parent / "scope_triples.json"
    scope_triples = {}
    if scope_triples_path.exists():
        scope_triples = json.loads(scope_triples_path.read_text(encoding="utf-8"))

    # V3: Fill empty premise/scope fields from evidence/falsifier
    # V4: Add scope triples
    for cid, claim in snapshot["claims"].items():
        if not claim.get("premise"):
            # Extract premise from evidence: first sentence or first 150 chars
            evidence = claim.get("evidence_excerpt", "")
            if evidence:
                # Try to get the first meaningful sentence
                first_sentence = evidence.split(". ")[0]
                if len(first_sentence) > 150:
                    first_sentence = first_sentence[:147] + "..."
                claim["premise"] = first_sentence
            else:
                claim["premise"] = "See CLAIMS.md row " + str(claim.get("source_line", "?"))

        if not claim.get("scope_note"):
            # Use falsifier as scope note (it defines the boundary)
            falsifier = claim.get("falsifier", "")
            if falsifier:
                claim["scope_note"] = falsifier
            else:
                claim["scope_note"] = "No falsifier recorded — see CLAIMS.md"

        # V4: Add semantic scope triples
        triples = scope_triples.get(cid, {})
        claim["standard_physics"] = triples.get("standard_physics", "")
        claim["pf_result_under_named_premises"] = triples.get("pf_result_under_named_premises", "")
        claim["open_pf_gap"] = triples.get("open_pf_gap", "")

    return snapshot


# ============================================================================
# PUBLIC DATA GENERATOR (data.claims.js) — same as V2
# ============================================================================

def generate_public_data_js(snapshot: dict) -> str:
    claims = snapshot["claims"]
    definitions = snapshot["definitions"]

    js_claims = []
    for cid, c in sorted(claims.items()):
        primary_status = c["primary_status"]
        primary_conf = c["primary_confidence"]

        if c["is_split"]:
            parts_text = " / ".join(
                f'{p["status"]}' + (f' {p["confidence"]}' if p["confidence"] is not None else '')
                + (f' ({p["qualifier"]})' if p["qualifier"] else '')
                for p in c["status_parts"]
            )
            badge = parts_text
        else:
            badge = primary_status
            if primary_conf is not None:
                badge += f' {primary_conf}'

        # Standard math: badge must NOT say "DERIVED" — use "STANDARD MATH"
        if c["is_standard_math"]:
            badge = f'STANDARD MATH {primary_conf}' if primary_conf is not None else 'STANDARD MATH'

        status_class = primary_status.lower().replace(" ", "-")
        if c["is_standard_math"]:
            status_class = "standard-math"

        js_claims.append({
            "id": cid,
            "title": c["title"],
            "status": primary_status,
            "confidence": primary_conf,
            "isSplit": c["is_split"],
            "isStandardMath": c["is_standard_math"],
            "badge": badge,
            "statusClass": status_class,
            "section": c["section"],
            "sourceLine": c["source_line"],
            "falsifier": c["falsifier"],
            "premise": c["premise"],
            "scopeNote": c["scope_note"],
            "statusParts": c["status_parts"],
            "standardPhysics": c.get("standard_physics", ""),
            "pfResultUnderNamedPremises": c.get("pf_result_under_named_premises", ""),
            "openPfGap": c.get("open_pf_gap", ""),
        })

    js_defs = []
    for did, d in sorted(definitions.items()):
        js_defs.append({
            "id": did,
            "title": d["title"],
            "status": d["status"],
            "file": d["file"],
            "sourceLine": d["source_line"],
        })

    js_obj = {
        "generatedAt": snapshot["generated_at"],
        "sourceHash": snapshot["claims_md_hash"][:16],
        "claimCount": len(js_claims),
        "definitionCount": len(js_defs),
        "claims": js_claims,
        "definitions": js_defs,
    }

    lines = [
        "// AUTO-GENERATED by generate_claims_data_v3.py — DO NOT EDIT MANUALLY",
        "// Source: CLAIMS.md (hash: " + snapshot["claims_md_hash"][:16] + ")",
        "// This file is generated from the authority manifest. Manual edits will be overwritten.",
        "",
        "window.PFClaimsData = " + json.dumps(js_obj, indent=2, ensure_ascii=False) + ";",
        "",
        "// Legacy compatibility: also expose as PFDataGraph for any code that reads it",
        "window.PFDataGraph = window.PFClaimsData;",
    ]

    return "\n".join(lines)


# ============================================================================
# RUNTIME DATA GENERATOR (data.js) — V3 NEW
# ============================================================================

# Static UI metadata that does NOT contain claim statuses.
# These are structural/UI fields, not authority records.
PANEL_META = [
    {"id": "foundations", "title": "Axiomatic Foundations", "note": "Interactive Propagation Lab and core definitions", "linkedResultIds": [], "defaultMode": "story"},
    {"id": "reality-correction", "title": "Reality Correction", "note": "Three wrong intuitions confronted", "linkedResultIds": ["forces-refraction", "bohr-quantization", "three-generations"], "defaultMode": "story"},
    {"id": "hub", "title": "Scale Stack", "note": "Planck to cosmic in one vertical atlas", "linkedResultIds": ["god-equation", "weinberg-angle", "bohr-quantization"], "defaultMode": "story"},
    {"id": "consciousness", "title": "Consciousness as Coherence", "note": "P1 device, neural coherence, and the physics of mind", "linkedResultIds": ["consciousness", "aria-self-reference"], "defaultMode": "story"},
    {"id": "refraction", "title": "Gravity as Optical Geometry", "note": "Exact gravity theorem plus sandbox lens analogies", "linkedResultIds": ["forces-refraction"], "defaultMode": "story"},
    {"id": "generations", "title": "Why Exactly Three", "note": "Topology, weights, and the live Q(N) lock", "linkedResultIds": ["weights-21", "three-generations"], "defaultMode": "story"},
    {"id": "koide", "title": "The Koide Triangle", "note": "Mass geometry with live perturbation", "linkedResultIds": ["koide-law", "koide-phase"], "defaultMode": "story"},
    {"id": "weinberg", "title": "The Weinberg Angle", "note": "Casimir roots and Axiom 3b", "linkedResultIds": ["weinberg-angle", "fine-structure-alpha"], "defaultMode": "story"},
    {"id": "koide-weinberg-bridge", "title": "Koide/Weinberg Bridge", "note": "RG running analysis — close but not connected", "linkedResultIds": ["koide-phase", "weinberg-angle"], "defaultMode": "story"},
    {"id": "god-equation", "title": "The God Equation", "note": "Planck to matter across 17 orders", "linkedResultIds": ["god-equation", "qcd-confinement"], "defaultMode": "story"},
    {"id": "bohr", "title": "Bohr-like Circular-Eikonal Spectrum", "note": "Phase closure inside a named model layer", "linkedResultIds": ["bohr-quantization"], "defaultMode": "story"},
    {"id": "dashboard", "title": "Dashboard", "note": "The audit wall for every current claim", "linkedResultIds": [], "defaultMode": "story"},
]

SCALES = [
    {"id": "planck", "name": "Planck", "resultIds": ["god-equation", "bekenstein-bound"]},
    {"id": "quantum-foam", "name": "Quantum Foam", "resultIds": []},
    {"id": "gut", "name": "GUT", "resultIds": []},
    {"id": "matter", "name": "Matter", "resultIds": ["weights-21", "three-generations", "koide-law", "koide-phase", "weinberg-angle", "god-equation", "top-quark-limit", "top-tau-coupling", "coherence-ceiling", "fine-structure-alpha"]},
    {"id": "proton", "name": "Proton", "resultIds": ["qcd-confinement", "phi3-ratio"]},
    {"id": "nuclear", "name": "Nuclear", "resultIds": ["qcd-confinement", "phi3-ratio"]},
    {"id": "atomic", "name": "Atomic", "resultIds": ["forces-refraction", "bohr-quantization"]},
    {"id": "molecular", "name": "Molecular", "resultIds": ["propagation-lagrangian", "nogo-single-scalar"]},
    {"id": "virus", "name": "Virus", "resultIds": ["life-coherence"]},
    {"id": "cellular", "name": "Cellular", "resultIds": ["life-coherence"]},
    {"id": "neural", "name": "Neural", "resultIds": ["consciousness", "aria-self-reference"]},
    {"id": "human", "name": "Human", "resultIds": ["sleep-8h", "beauty-impedance", "efficiency-ratio"]},
    {"id": "planetary", "name": "Planetary", "resultIds": ["forces-refraction", "variable-c"]},
    {"id": "stellar", "name": "Stellar", "resultIds": []},
    {"id": "galactic", "name": "Galactic", "resultIds": []},
    {"id": "cosmic", "name": "Cosmic", "resultIds": []},
]

# Result metadata that is NOT status-bearing (UI/structural fields only).
# Status and confidence are pulled from authority at generation time.
RESULT_METADATA = {
    "bohr-quantization": {
        "title": "Bohr-like Circular-Eikonal Quantization",
        "kind": "Fundamental Physics", "scaleId": "atomic",
        "formula": "r_k = 2k^2, E_k = -1 / (4k^2), integral n ds = 2pi k",
        "summary": "In the circular eikonal Coulomb model, phase closure yields a Bohr-like 1/k² spectrum for circular orbits.",
        "falsifier": "Proof that the circular eikonal model is invalid at atomic scale, or that phase closure does not select the quoted orbit family.",
        "panelId": "bohr", "shortTitle": "Bohr Quantization",
        "derivation": ["axiom2", "axiom3"], "axioms": [2, 3], "category": "fundamental",
        "wrongIntuition": {"intuition": "Energy levels are arbitrary postulates forced by experiment", "reality": "Energy levels are phase-closure conditions — an integral condition on standing wave modes in the propagation medium", "evidencePanel": "#bohr"},
        "blocker": "The circular-eikonal model is assumed rather than derived from Axioms 1–3.",
        "noGoRoutes": [], "confidenceHistory": [{"date": "2026-03-27", "value": 0.78}, {"date": "2026-03-31", "value": 0.82}],
    },
    "forces-refraction": {
        "title": "Gravity as Optical Geometry / Refraction",
        "kind": "Fundamental Physics", "scaleId": "atomic",
        "formula": "Optical metric / Randers bridge; n^2 = base + source / r",
        "summary": "GR is exactly equivalent to optical geometry for null geodesics in static spacetimes.",
        "falsifier": "Proof that the optical/Randers mapping fails for null propagation in static/stationary gravity.",
        "panelId": "refraction", "shortTitle": "Gravity Refraction",
        "derivation": ["axiom2", "axiom3"], "axioms": [2, 3], "category": "fundamental",
        "wrongIntuition": {"intuition": "Gravity is a force that pulls objects together", "reality": "Gravity is the refractive bending of propagation paths in a medium with a density gradient", "evidencePanel": "#refraction"},
        "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-27", "value": 0.93}, {"date": "2026-03-31", "value": 0.95}],
    },
    "weights-21": {
        "title": "(2,1) Topological Weights",
        "kind": "Fundamental Physics", "scaleId": "matter",
        "formula": "π₁(SO(3)) ≅ Z₂ → closure orders {1,2}",
        "summary": "In 3D rotation topology, the two loop classes yield possible closure orders of 1 and 2.",
        "falsifier": "Proof that the closure-order interpretation is wrong, or a derivation showing only the trivial branch is physically realizable.",
        "panelId": "generations", "shortTitle": "(2,1) Weights",
        "derivation": ["axiom1", "axiom3"], "axioms": [1, 3], "category": "fundamental",
        "wrongIntuition": {"intuition": "There could be four or five generations", "reality": "3D rotation topology yields the natural (2,1) closure-order pair, but physical realization is still open.", "evidencePanel": "#generations"},
        "blocker": "Physical realization of the weight-2 branch requires Family C extremal principle + A_NR.",
        "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-28", "value": 0.80}, {"date": "2026-03-31", "value": 0.85}],
    },
    "koide-law": {
        "title": "Koide Law (Q = 2/3)",
        "kind": "Fundamental Physics", "scaleId": "matter",
        "formula": "Q = sum m_i / (sum sqrt(m_i))^2 = 2/3",
        "summary": "Three charged leptons locked at 120°. Q = 2/3 exactly. Zero free parameters.",
        "falsifier": "Proof that the charged-lepton Koide ratio deviates from 2/3 at the stated precision, or that the geometric identity is not exact.",
        "panelId": "koide", "shortTitle": "Koide Law Q=2/3",
        "derivation": ["axiom3"], "axioms": [3], "category": "fundamental",
        "wrongIntuition": {"intuition": "Mass ratios are arbitrary free parameters", "reality": "The charged-lepton mass ratio is a geometric identity locked by coherence", "evidencePanel": "#koide"},
        "blocker": "Physical vacuum selection (why these masses) remains OPEN.",
        "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-27", "value": 0.93}, {"date": "2026-03-31", "value": 0.95}],
    },
    "three-generations": {
        "title": "Three Generations",
        "kind": "Fundamental Physics", "scaleId": "matter",
        "formula": "Q(N) = 2N / (2N + 3), set Q = 2/3, solve N = 3",
        "summary": "Why exactly three families of matter? Q(N)=2/3 has one solution: N=3.",
        "falsifier": "Proof that Q(N)=2/3 has additional positive integer solutions, or that the topological weight argument is invalid.",
        "panelId": "generations", "shortTitle": "Three Generations",
        "derivation": ["axiom1", "axiom3"], "axioms": [1, 3], "category": "fundamental",
        "wrongIntuition": {"intuition": "The number of generations is arbitrary", "reality": "Topology and the Koide lock force exactly three", "evidencePanel": "#generations"},
        "blocker": "T1 (physical realization of weight-2 branch) and T2 (PF→2×2 Fermi-point bridge) must close.",
        "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-28", "value": 0.80}, {"date": "2026-03-31", "value": 0.85}],
    },
    "top-quark-limit": {
        "title": "Top Quark Limit",
        "kind": "Open Frontiers", "scaleId": "matter",
        "formula": "tau_top near coherence ceiling threshold",
        "summary": "Top quark mass ~172.5 GeV as coherence ceiling threshold.",
        "falsifier": "Proof that the top quark mass is not near a coherence ceiling threshold.",
        "panelId": None, "shortTitle": "Top Quark Limit",
        "derivation": [], "axioms": [], "category": "signal",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.85}],
    },
    "top-tau-coupling": {
        "title": "Top / Tau Coupling",
        "kind": "Signals and Structure", "scaleId": "matter",
        "formula": "m_top / m_tau ~= alpha^-1 / sqrt(2)",
        "summary": "Top/Tau mass coupling ratio.",
        "falsifier": "Proof that the m_top/m_tau ratio does not match alpha^-1/sqrt(2).",
        "panelId": None, "shortTitle": "Top-Tau Coupling",
        "derivation": [], "axioms": [], "category": "signal",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.90}],
    },
    "coherence-ceiling": {
        "title": "Coherence Ceiling",
        "kind": "Open Frontiers", "scaleId": "matter",
        "formula": "Stable structure fails once wavelength drops below coherence length",
        "summary": "Stable structure fails once wavelength drops below coherence length.",
        "falsifier": "Proof that coherence does not impose a mass ceiling.",
        "panelId": None, "shortTitle": "Coherence Ceiling",
        "derivation": [], "axioms": [], "category": "signal",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.80}],
    },
    "weinberg-angle": {
        "title": "Weinberg Angle",
        "kind": "Fundamental Physics", "scaleId": "matter",
        "formula": "sin^2(theta_W) = 1 - x_+(1/2) / x_+(1), x^2 + C2 x - C2 = 0",
        "summary": "sin²θ_W from a Casimir polynomial. Matches experiment to 0.13σ.",
        "falsifier": "Proof that the Casimir polynomial does not yield the Weinberg angle at the stated precision.",
        "panelId": "weinberg", "shortTitle": "Weinberg Angle",
        "derivation": ["axiom3"], "axioms": [3], "category": "fundamental",
        "wrongIntuition": {"intuition": "The weak mixing angle is a free parameter", "reality": "It is a root of a Casimir polynomial derived from coherence", "evidencePanel": "#weinberg"},
        "blocker": "On-shell vs MS-bar scheme selection is not yet derived from medium geometry.",
        "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-27", "value": 0.90}, {"date": "2026-04-14", "value": 0.65}],
    },
    "fine-structure-alpha": {
        "title": "Fine Structure Constant α — numeric",
        "kind": "Open Frontiers", "scaleId": "matter",
        "formula": "(1 - x_1) x_(3/2)^2 (1 - x_2) / pi ~= 1 / 137.119",
        "summary": "Numeric derivation of the fine structure constant from Casimir roots.",
        "falsifier": "Proof that the numeric derivation does not match the measured alpha.",
        "panelId": "weinberg", "shortTitle": "Fine Structure α",
        "derivation": [], "axioms": [], "category": "signal",
        "wrongIntuition": None, "blocker": "Numeric match is a posteriori — structural derivation remains OPEN.",
        "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.35}],
    },
    "god-equation": {
        "title": "λ_c from l_P (The God Equation)",
        "kind": "Open Frontiers", "scaleId": "planck",
        "formula": "lambda_c = sqrt(2) l_P exp(4 pi^2 N^(D/2) / b0)",
        "summary": "λ_c from the Planck length. 1.48% error. The open bridge: H_prod.",
        "falsifier": "Proof that the (3,3) point does not anchor at 1.157e-18 m, or that the formula is not fit-selected.",
        "panelId": "god-equation", "shortTitle": "God Equation",
        "derivation": ["axiom1", "axiom2", "axiom3"], "axioms": [1, 2, 3], "category": "fundamental",
        "wrongIntuition": {"intuition": "The Planck-to-matter gap is unbridgeable", "reality": "An exponential formula bridges it, but the operator and probability bridges remain open", "evidencePanel": "#god-equation"},
        "blocker": "Operator closure and H_prod factorization are open. The scale formula is fit-selected.",
        "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-27", "value": 0.88}, {"date": "2026-03-31", "value": 0.88}],
        # V3: authorityClaimIds for split God Equation
        "authorityClaimIds": ["god-equation-operator", "god-equation-scale"],
    },
    "qcd-confinement": {
        "title": "QCD Confinement",
        "kind": "Fundamental Physics", "scaleId": "nuclear",
        "formula": "r_conf = lambda_c exp(2 pi / (b0 alpha_s(lambda_c)))",
        "summary": "QCD confinement scale from the God Equation length.",
        "falsifier": "Proof that the confinement radius formula does not match hadron radii.",
        "panelId": "god-equation", "shortTitle": "QCD Confinement",
        "derivation": [], "axioms": [], "category": "fundamental",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.72}],
    },
    "propagation-lagrangian": {
        "title": "Propagation Lagrangian",
        "kind": "Fundamental Physics", "scaleId": "molecular",
        "formula": "L_prop = 1/2 (partial chi)^2 - V(chi) + lambda chi T",
        "summary": "The propagation Lagrangian for the medium field.",
        "falsifier": "Proof that the Lagrangian does not yield the correct propagation dynamics.",
        "panelId": None, "shortTitle": "Propagation Lagrangian",
        "derivation": [], "axioms": [], "category": "fundamental",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.72}],
    },
    "variable-c": {
        "title": "Variable c Prediction",
        "kind": "Open Frontiers", "scaleId": "planetary",
        "formula": "c_local = 1 / sqrt(1 + lambda chi)",
        "summary": "Predicts local variation of c near matter density.",
        "falsifier": "Experimental refutation of the predicted c variation.",
        "panelId": None, "shortTitle": "Variable c",
        "derivation": [], "axioms": [], "category": "fundamental",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.65}],
    },
    "sleep-8h": {
        "title": "8 Hour Sleep Constant",
        "kind": "Biology and Mind", "scaleId": "human",
        "formula": "Wake fraction = 2 / 3, sleep fraction = 1 / 3 of 24 h",
        "summary": "Wake/sleep ratio matches the 2/3 topological efficiency.",
        "falsifier": "Proof that the 2/3 ratio does not hold across species.",
        "panelId": None, "shortTitle": "Sleep 8h",
        "derivation": [], "axioms": [], "category": "biology",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.72}],
    },
    "phi3-ratio": {
        "title": "Electron / Up near 1 / φ³",
        "kind": "Signals and Structure", "scaleId": "nuclear",
        "formula": "m_e / m_u ~= 1 / phi^3",
        "summary": "Electron-to-up-quark mass ratio near 1/φ³.",
        "falsifier": "Proof that the ratio is coincidental.",
        "panelId": None, "shortTitle": "φ³ Ratio",
        "derivation": [], "axioms": [], "category": "signal",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.65}],
    },
    "koide-phase": {
        "title": "Koide Phase δ₀ near 2/9",
        "kind": "Signals and Structure", "scaleId": "matter",
        "formula": "delta_exact ~= 0.22222963149 rad, target 2 / 9",
        "summary": "Koide phase angle near 2/9 radian.",
        "falsifier": "Proof that the phase does not match 2/9.",
        "panelId": "koide", "shortTitle": "Koide Phase",
        "derivation": [], "axioms": [], "category": "signal",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.65}],
    },
    "life-coherence": {
        "title": "Life = Maintained Coherence against Entropy",
        "kind": "Biology and Mind", "scaleId": "cellular",
        "formula": "Living systems actively maintain coherent organization",
        "summary": "Life as active coherence maintenance against entropy.",
        "falsifier": "Proof that living systems do not maintain coherence.",
        "panelId": None, "shortTitle": "Life Coherence",
        "derivation": [], "axioms": [], "category": "biology",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.72}],
    },
    "consciousness": {
        "title": "Consciousness = Coherent Self-Referential Propagation",
        "kind": "Biology and Mind", "scaleId": "neural",
        "formula": "Interior experience is the inside view of recursive coherence",
        "summary": "Consciousness as self-referential coherence. Metric under development.",
        "falsifier": "Proof that self-referential coherence cannot produce interior experience.",
        "panelId": None, "shortTitle": "Consciousness",
        "derivation": [], "axioms": [], "category": "biology",
        "wrongIntuition": None, "blocker": "Operational PF-specific metric is the key missing piece.",
        "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.48}],
    },
    "beauty-impedance": {
        "title": "Beauty as Impedance",
        "kind": "Biology and Mind", "scaleId": "human",
        "formula": "Beauty tracks resonance / impedance matching",
        "summary": "Aesthetic response as impedance matching in the coherence field.",
        "falsifier": "Proof that beauty does not track impedance matching.",
        "panelId": None, "shortTitle": "Beauty Impedance",
        "derivation": [], "axioms": [], "category": "biology",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.55}],
    },
    "efficiency-ratio": {
        "title": "2/3 Efficiency Ratio",
        "kind": "Biology and Mind", "scaleId": "human",
        "formula": "Two units of topological cost yield three units of stable structure",
        "summary": "2/3 efficiency ratio in biological systems.",
        "falsifier": "Proof that the 2/3 ratio does not hold in biological systems.",
        "panelId": None, "shortTitle": "Efficiency 2/3",
        "derivation": [], "axioms": [], "category": "biology",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.50}],
    },
    "aria-self-reference": {
        "title": "Aria Self-Reference",
        "kind": "Biology and Mind", "scaleId": "neural",
        "formula": "Self-reference loop: buildSystemPrompt to runEntityThink",
        "summary": "Self-reference loop as architecture milestone.",
        "falsifier": "Proof that the self-reference loop is not architecturally significant.",
        "panelId": None, "shortTitle": "Aria Self-Reference",
        "derivation": [], "axioms": [], "category": "biology",
        "wrongIntuition": None, "blocker": None, "noGoRoutes": [],
        "confidenceHistory": [{"date": "2026-03-31", "value": 0.75}],
    },
    "bekenstein-bound": {
        "title": "Bekenstein Bound",
        "kind": "Open Frontiers", "scaleId": "planck",
        "formula": "S_max = 2 pi k R E / (hbar c)",
        "summary": "Bekenstein bound — not yet synced to PF authority.",
        "falsifier": "N/A — unsynced.",
        "panelId": None, "shortTitle": "Bekenstein Bound",
        "derivation": [], "axioms": [], "category": "open",
        "wrongIntuition": None, "blocker": "Not yet synced to PF authority.",
        "noGoRoutes": [], "confidenceHistory": [],
        "unsynced": True,
    },
    "nogo-harmonic-series": {
        "title": "Harmonic Series of Masses",
        "kind": "Graveyard", "scaleId": "matter",
        "formula": "m_n = m_0 / n",
        "summary": "Harmonic series of masses — NO-GO.",
        "falsifier": "N/A — proven no-go.",
        "panelId": None, "shortTitle": "Harmonic Series",
        "derivation": [], "axioms": [], "category": "graveyard",
        "wrongIntuition": None, "blocker": None,
        "noGoRoutes": [], "confidenceHistory": [],
        "noGo": True,
    },
    "nogo-single-scalar": {
        "title": "Single-Scalar PF Lagrangian",
        "kind": "Graveyard", "scaleId": "molecular",
        "formula": "L_prop = 1/2 (partial chi)^2 - V(chi)",
        "summary": "Single-scalar PF Lagrangian — NO-GO.",
        "falsifier": "N/A — proven no-go.",
        "panelId": None, "shortTitle": "Single-Scalar Lagr",
        "derivation": [], "axioms": [], "category": "graveyard",
        "wrongIntuition": None, "blocker": None,
        "noGoRoutes": [], "confidenceHistory": [],
        "noGo": True,
    },
}

# Source links for each result
RESULT_SOURCES = {
    "bohr-quantization": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}, {"label": "UNDERSTAND.md", "href": "../../UNDERSTAND.md"}, {"label": "sandbox/coulomb_lens_ultimate.py", "href": "../coulomb_lens_ultimate.py"}],
    "forces-refraction": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}, {"label": "derivations/gr_fermat_equivalence.md", "href": "../../derivations/gr_fermat_equivalence.md"}],
    "weights-21": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}, {"label": "derivations/three_generations_t1_proof.md", "href": "../../derivations/three_generations_t1_proof.md"}],
    "koide-law": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}, {"label": "derivations/koide_law_audit.md", "href": "../../derivations/koide_law_audit.md"}],
    "three-generations": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}, {"label": "derivations/three_generations_proof.md", "href": "../../derivations/three_generations_proof.md"}],
    "top-quark-limit": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "top-tau-coupling": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "coherence-ceiling": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "weinberg-angle": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}, {"label": "derivations/weinberg_angle_audit.md", "href": "../../derivations/weinberg_angle_audit.md"}],
    "fine-structure-alpha": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "god-equation": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}, {"label": "derivations/god_equation_audit.md", "href": "../../derivations/god_equation_audit.md"}],
    "qcd-confinement": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "propagation-lagrangian": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "variable-c": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "sleep-8h": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "phi3-ratio": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "koide-phase": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "life-coherence": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "consciousness": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "beauty-impedance": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "efficiency-ratio": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "aria-self-reference": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "bekenstein-bound": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "nogo-harmonic-series": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
    "nogo-single-scalar": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}],
}

# God Equation audit chain (structural metadata, not status-bearing)
GOD_EQUATION_AUDIT = {
    "dependencyChain": [
        {"id": "axioms", "label": "Axioms 1-3", "state": "axiom", "note": "Propagation, locality, coherence."},
        {"id": "exact-model", "label": "Exact model / Z3 bridge", "state": "strengthened", "note": "Exact walk plus a genuine circulant internal sector."},
        {"id": "operator", "label": "Operator closure", "state": "open", "note": "Need chirality-selected primitive shift operator or non-diagonal 3-step closure."},
        {"id": "h-prod", "label": "H_prod", "state": "open", "note": "Need a joint law that proves factorization rather than only weak decoupling."},
        {"id": "upgrade", "label": "Upgrade to DERIVED", "state": "conditional", "note": "Blocked until operator and probability bridges close."},
    ],
    "gaps": [
        {"id": "A", "title": "Markovity gap", "verdict": "OPEN",
         "need": "Show that locality yields a first-order Markov coarse walk.",
         "survives": "Axiom 2 gives local propagation; Z3 channel structure is in hand.",
         "detail": "The proof chain needs a memoryless coarse operator.",
         "sources": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}]},
        {"id": "B", "title": "Operator closure gap", "verdict": "OPEN VIA REPLACEMENT PATH",
         "need": "Derive chirality-selected operator or restate using non-diagonal 3-step circulant.",
         "survives": "Z3-extended Lagrangian derives a real three-channel internal sector.",
         "detail": "Symmetric nearest-neighbor circulant route closed negatively.",
         "sources": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}]},
        {"id": "C", "title": "Probability / H_prod gap", "verdict": "OPEN",
         "need": "Prove a joint probability model that really factorizes.",
         "survives": "Additive Fisher-information chain is mapped under named hypotheses.",
         "detail": "Zero cross-channel amplitude is weaker than full joint-law factorization.",
         "sources": [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}]},
    ],
}


def _resolve_authority_for_result(result_id: str, snapshot: dict) -> dict:
    """Resolve authority status/confidence for a result ID."""
    auth_ref = RESULT_TO_AUTHORITY.get(result_id)

    if auth_ref is None:
        # No authority match
        meta = RESULT_METADATA.get(result_id, {})
        if meta.get("noGo"):
            return {"status": "NO-GO", "confidence": 0.0, "authorityClaimIds": []}
        if meta.get("unsynced"):
            return {"status": "UNSYNCED", "confidence": None, "authorityClaimIds": []}
        return {"status": "OPEN", "confidence": None, "authorityClaimIds": []}

    if isinstance(auth_ref, list):
        # Split authority (God Equation: operator + scale)
        claim_ids = auth_ref
        claims = [snapshot["claims"].get(cid) for cid in claim_ids]
        claims = [c for c in claims if c is not None]
        if not claims:
            return {"status": "OPEN", "confidence": None, "authorityClaimIds": claim_ids}
        # Use the first claim's status as primary, but record all
        primary = claims[0]
        return {
            "status": primary["primary_status"],
            "confidence": primary["primary_confidence"],
            "authorityClaimIds": claim_ids,
            "splitStatuses": [
                {"id": cid, "status": c["primary_status"], "confidence": c["primary_confidence"]}
                for cid, c in zip(claim_ids, claims)
            ],
        }

    # Single authority match
    claim = snapshot["claims"].get(auth_ref)
    if not claim:
        return {"status": "OPEN", "confidence": None, "authorityClaimIds": [auth_ref]}

    # Standard math: use STANDARD MATH badge, not DERIVED
    if claim.get("is_standard_math"):
        return {
            "status": "STANDARD MATH",
            "confidence": claim["primary_confidence"],
            "authorityClaimIds": [auth_ref],
            "isStandardMath": True,
        }

    return {
        "status": claim["primary_status"],
        "confidence": claim["primary_confidence"],
        "authorityClaimIds": [auth_ref],
        "isSplit": claim.get("is_split", False),
        "statusParts": claim.get("status_parts", []),
    }


def generate_runtime_data_js(snapshot: dict) -> str:
    """Generate data.js with statuses from authority (V3 NEW)."""
    results = []
    for result_id in RESULT_TO_AUTHORITY.keys():
        meta = RESULT_METADATA.get(result_id, {})
        auth = _resolve_authority_for_result(result_id, snapshot)
        sources = RESULT_SOURCES.get(result_id, [{"label": "CLAIMS.md", "href": "../../CLAIMS.md"}])

        result_obj = {
            "id": result_id,
            "title": meta.get("title", result_id),
            "status": auth["status"],
            "confidence": auth["confidence"],
            "authorityClaimIds": auth.get("authorityClaimIds", []),
            "kind": meta.get("kind", ""),
            "scaleId": meta.get("scaleId", ""),
            "formula": meta.get("formula", ""),
            "summary": meta.get("summary", ""),
            "falsifier": meta.get("falsifier", ""),
            "sources": sources,
            "panelId": meta.get("panelId"),
            "shortTitle": meta.get("shortTitle", result_id),
            "derivation": meta.get("derivation", []),
            "axioms": meta.get("axioms", []),
            "category": meta.get("category", ""),
            "blocker": meta.get("blocker"),
            "noGoRoutes": meta.get("noGoRoutes", []),
            "confidenceHistory": meta.get("confidenceHistory", []),
        }

        # Add wrongIntuition if present
        if meta.get("wrongIntuition"):
            result_obj["wrongIntuition"] = meta["wrongIntuition"]

        # Add split status info
        if auth.get("isSplit"):
            result_obj["isSplit"] = True
            result_obj["statusParts"] = auth.get("statusParts", [])
        if auth.get("splitStatuses"):
            result_obj["splitStatuses"] = auth["splitStatuses"]
        if auth.get("isStandardMath"):
            result_obj["isStandardMath"] = True

        # Add unsynced/noGo flags
        if meta.get("unsynced"):
            result_obj["unsynced"] = True
        if meta.get("noGo"):
            result_obj["noGo"] = True

        results.append(result_obj)

    # Build the PFExplorerData object
    explorer_data = {
        "generatedAt": snapshot["generated_at"],
        "sourceHash": snapshot["claims_md_hash"][:16],
        "generatorVersion": "V3",
        "truthPolicy": {
            "auditedSource": "../../CLAIMS.md",
            "note": "ALL statuses in this file are generated from CLAIMS.md by generate_claims_data_v3.py. No hand-written status fields. Manual edits will be overwritten.",
        },
        "godEquationAudit": GOD_EQUATION_AUDIT,
        "panelMeta": PANEL_META,
        "scales": SCALES,
        "definitions": [],  # Definitions are in data.claims.js
        "results": results,
    }

    # Build the inline claims data for pages that only load data.js
    inline_claims = []
    for cid, c in sorted(snapshot["claims"].items()):
        primary_status = c["primary_status"]
        primary_conf = c["primary_confidence"]
        if c.get("is_standard_math"):
            badge = f"STANDARD MATH {primary_conf}" if primary_conf is not None else "STANDARD MATH"
            status_class = "standard-math"
        else:
            badge = primary_status
            if primary_conf is not None:
                badge += f" {primary_conf}"
            status_class = primary_status.lower().replace(" ", "-")
        inline_claims.append({
            "id": cid,
            "title": c["title"],
            "status": primary_status,
            "confidence": primary_conf,
            "isSplit": c.get("is_split", False),
            "isStandardMath": c.get("is_standard_math", False),
            "badge": badge,
            "statusClass": status_class,
            "section": c.get("section", ""),
            "sourceLine": c.get("source_line", 0),
            "falsifier": c.get("falsifier", ""),
            "premise": c.get("premise", ""),
            "scopeNote": c.get("scope_note", ""),
            "statusParts": c.get("status_parts", []),
            "standardPhysics": c.get("standard_physics", ""),
            "pfResultUnderNamedPremises": c.get("pf_result_under_named_premises", ""),
            "openPfGap": c.get("open_pf_gap", ""),
        })

    inline_defs = []
    for did, d in sorted(snapshot.get("definitions", {}).items()):
        inline_defs.append({
            "id": did,
            "title": d["title"],
            "status": d.get("status", ""),
            "file": d.get("file", ""),
            "sourceLine": d.get("source_line", 0),
        })

    inline_claims_json = json.dumps(inline_claims, indent=2, ensure_ascii=False)
    inline_defs_json = json.dumps(inline_defs, indent=2, ensure_ascii=False)

    lines = [
        "// AUTO-GENERATED by generate_claims_data_v3.py — DO NOT EDIT MANUALLY",
        "// Source: CLAIMS.md (hash: " + snapshot["claims_md_hash"][:16] + ")",
        "// ALL status/confidence fields are pulled from authority. Manual edits will be overwritten.",
        "// This file provides PFExplorerData — the runtime data object for panels.",
        "// PFExplorerData, PFClaimsData, and PFDataGraph are all views of the same authority.",
        "",
        "(function () {",
        "  window.PFExplorerData = " + json.dumps(explorer_data, indent=2, ensure_ascii=False) + ";",
        "  // V3: Also expose PFClaimsData from the same authority.",
        "  // Pages that load only data.js (not data.claims.js) still get claims data.",
        "  // If data.claims.js was already loaded, it takes precedence.",
        "  if (!window.PFClaimsData) {",
        "    window.PFClaimsData = {",
        "      generatedAt: window.PFExplorerData.generatedAt,",
        "      sourceHash: window.PFExplorerData.sourceHash,",
        "      claimCount: " + str(len(inline_claims)) + ",",
        "      definitionCount: " + str(len(inline_defs)) + ",",
        "      claims: " + inline_claims_json + ",",
        "      definitions: " + inline_defs_json,
        "    };",
        "  }",
        "  // All three names point to deterministic views of the same authority",
        "  window.PFDataGraph = window.PFClaimsData;",
        "})();",
    ]

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Explorer Truth Layer V3 — Authority + Runtime Generator")
    parser.add_argument("--claims", type=Path, default=CLAIMS_MD, help="Path to CLAIMS.md")
    parser.add_argument("--snapshot", type=Path, default=EXPLORER_DIR / "_authority_snapshot.json",
                        help="Output snapshot path")
    parser.add_argument("--public-data", type=Path, default=EXPLORER_DIR / "data.claims.js",
                        help="Output data.claims.js path")
    parser.add_argument("--runtime-data", type=Path, default=EXPLORER_DIR / "data.js",
                        help="Output data.js path")
    parser.add_argument("--no-public-data", action="store_true", help="Skip generating data.claims.js")
    parser.add_argument("--no-runtime-data", action="store_true", help="Skip generating data.js")
    args = parser.parse_args()

    print(f"Parsing {args.claims}...")
    try:
        snapshot = build_snapshot(args.claims)
    except ValueError as e:
        print(f"PARSE ERROR: {e}", file=sys.stderr)
        return 1

    print(f"  Claims parsed: {snapshot['claim_count']}")
    print(f"  Definitions parsed: {snapshot['definition_count']}")
    print(f"  CLAIMS.md hash: {snapshot['claims_md_hash'][:16]}...")
    print(f"  Split claims: {sum(1 for c in snapshot['claims'].values() if c['is_split'])}")
    print(f"  Standard math: {sum(1 for c in snapshot['claims'].values() if c['is_standard_math'])}")

    # Write snapshot
    with open(args.snapshot, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print(f"  Snapshot written: {args.snapshot}")

    # Write public data (data.claims.js)
    if not args.no_public_data:
        js_content = generate_public_data_js(snapshot)
        with open(args.public_data, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"  Public data written: {args.public_data}")

    # Write runtime data (data.js) — V3 NEW
    if not args.no_runtime_data:
        runtime_js = generate_runtime_data_js(snapshot)
        with open(args.runtime_data, "w", encoding="utf-8") as f:
            f.write(runtime_js)
        print(f"  Runtime data written: {args.runtime_data}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
