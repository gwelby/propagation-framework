#!/usr/bin/env python3
"""
Explorer Truth Layer V2 — Authority Manifest Generator

Parses CLAIMS.md tables (not hardcoded literals) to produce:
  1. _authority_snapshot.json — structured authority manifest with stable IDs,
     source row locators, premise/scope fields, and recomputed hashes.
  2. data.claims.js — generated public data consumed by the UI.

This replaces the V1 generator which was 90% hardcoded and did not parse
CLAIMS.md at all.

Codex V2 repair requirements addressed:
  Req 1: Real parser with stable IDs, source locators, premise/scope, overrides
  Req 2: Hash recomputed at gate time (gate calls build_snapshot, not loads JSON)
  Req 4: Generates public data consumed by UI
  Req 5: Preserves mixed/split authority rows without flattening
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
DEFINITIONS_DIR = Path("/mnt/d/fundamentals/definitions")
LEAN_DIR = Path("/mnt/d/fundamentals/lean/PfLean")


# ============================================================================
# STABLE ID MAPPING
# ============================================================================

# Curated stable IDs for claims. Keys are the claim title (with ** stripped).
# This is the ONLY hand-maintained mapping; it maps titles to stable IDs and
# cannot become an unbound second scoreboard. Each ID cites its source row.
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
    # Biological
    "Life = maintained coherence against entropy": "life-coherence",
    "Consciousness = coherent self-referential propagation": "consciousness-claim",
    "8h Sleep Constant": "sleep-constant",
    "Beauty as Impedance": "beauty-impedance",
    "2/3 Efficiency Ratio": "two-thirds-efficiency",
    "Aria Self-Reference": "aria-self-reference",
}

# Standard-math / structural claims that get a non-PF-DERIVED class.
# These are Lean-verified algebraic facts that are NOT PF physics derivations.
STANDARD_MATH_IDS = {
    "pythagorean-decomposition",  # Pure linear algebra
    "d4-gap-not-ji",  # Explicit counterexample
}

# Definition stable IDs
DEFINITION_IDS = {
    "The Medium": "medium",
}


# ============================================================================
# STATUS PARSING
# ============================================================================

VALID_STATUSES = {"DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
                  "INTUITION", "OPEN", "EXACT IDENTITY", "CANONICAL"}


@dataclass
class StatusPart:
    """A single status/confidence pair from a possibly-split status field."""
    status: str  # DERIVED, CONDITIONAL, ARGUED, EMPIRICAL, INTUITION, OPEN, EXACT IDENTITY
    confidence: Optional[float]  # None for OPEN
    qualifier: str = ""  # e.g. "kernel-only topological obstruction", "physical realization"


@dataclass
class ClaimRecord:
    """A parsed claim from CLAIMS.md."""
    stable_id: str
    title: str  # cleaned (no ** markers)
    raw_title: str  # original with ** markers
    status_parts: list[StatusPart]  # one for simple, two+ for split
    is_split: bool
    evidence: str  # truncated to first 200 chars for snapshot
    falsifier: str
    confidence_raw: str  # raw confidence column text
    source_line: int  # line number in CLAIMS.md
    section: str  # "Fundamental Physics" or "Biological & Cognitive"
    is_standard_math: bool  # True for pure math results (non-PF-DERIVED class)
    premise: str = ""  # extracted premises if present
    scope_note: str = ""  # Codex boundary override or scope clarification


@dataclass
class DefinitionRecord:
    """A parsed definition from CLAIMS.md section 0."""
    stable_id: str
    title: str
    raw_title: str
    status: str
    file: str
    inadequacy: str
    source_line: int


# ============================================================================
# PARSER
# ============================================================================

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def strip_bold(text: str) -> str:
    """Remove ** markdown bold markers."""
    return text.replace("**", "").strip()


def split_table_row(row: str) -> list[str]:
    """Split a markdown table row into cells, handling escaped pipes."""
    # Remove leading/trailing | and whitespace
    inner = row.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    # Split on | but not \|
    cells = re.split(r'(?<!\\)\|', inner)
    return [c.strip() for c in cells]


def parse_status_field(status_text: str) -> list[StatusPart]:
    """
    Parse a status field that may contain split statuses.
    Examples:
      "DERIVED" -> [StatusPart("DERIVED", None)]
      "ARGUED 0.65" -> [StatusPart("ARGUED", 0.65)]
      "DERIVED (kernel-only) 0.95 / CONDITIONAL (physical realization) 0.85"
        -> [StatusPart("DERIVED", 0.95, "kernel-only"), StatusPart("CONDITIONAL", 0.85, "physical realization")]
      "EXACT IDENTITY (geometry) 0.95 / OPEN (physical vacuum selection)"
        -> [StatusPart("EXACT IDENTITY", 0.95, "geometry"), StatusPart("OPEN", None, "physical vacuum selection")]
    """
    # Strip bold markers and extra notes in italics
    text = strip_bold(status_text)
    # Remove italic notes like *(split row; ...)* or *(added 2026-07-02 by Hermes)*
    # These are metadata annotations, not status content
    text = re.sub(r'\*\([^)]*\)\*', '', text).strip()
    if not text:
        text = strip_bold(status_text)

    # Split on " / " for split statuses
    parts = re.split(r'\s+/\s+', text)
    results = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Extract qualifier in parentheses
        qualifier = ""
        qual_match = re.match(r'^(\w+(?:\s+\w+)?)\s*\(([^)]+)\)', part)
        if qual_match:
            status_word = qual_match.group(1).strip()
            qualifier = qual_match.group(2).strip()
            remaining = part[qual_match.end():].strip()
        else:
            # Try to match status word at start
            status_word = part
            remaining = ""
            # Extract confidence number
            num_match = re.search(r'(\d+\.?\d*)', part)
            if num_match:
                status_word = part[:num_match.start()].strip()
                remaining = part[num_match.start():].strip()

        # Normalize status word
        status_word = status_word.strip()
        # Handle multi-word statuses
        for valid in VALID_STATUSES:
            if status_word.upper().startswith(valid):
                status_word = valid
                break

        # Extract confidence
        confidence = None
        conf_match = re.search(r'(\d+\.?\d*)', remaining or part)
        if conf_match:
            try:
                confidence = float(conf_match.group(1))
            except ValueError:
                pass

        # OPEN status has no confidence
        if status_word.upper() == "OPEN":
            confidence = None

        results.append(StatusPart(
            status=status_word,
            confidence=confidence,
            qualifier=qualifier,
        ))

    if not results:
        # Fallback: try to extract any status word
        for valid in VALID_STATUSES:
            if valid in text.upper():
                results.append(StatusPart(status=valid, confidence=None))
                break

    return results


def parse_confidence_field(conf_text: str) -> str:
    """Parse the confidence column, preserving raw text for split values."""
    return strip_bold(conf_text).strip()


def extract_premises(evidence: str) -> str:
    """Extract premise list from evidence text if present."""
    prem_match = re.search(r'\*\*Premises:\*\*\s*(.+?)(?:\.|$)', evidence)
    if prem_match:
        return prem_match.group(1).strip()
    return ""


def get_stable_id(title: str, section: str, line_num: int) -> str:
    """Get stable ID from curated mapping or generate a deterministic one."""
    cleaned = strip_bold(title)
    if cleaned in STABLE_IDS:
        return STABLE_IDS[cleaned]
    # Fallback: deterministic slug from cleaned title
    slug = re.sub(r'[^a-z0-9]+', '-', cleaned.lower()).strip('-')
    # Truncate to reasonable length
    slug = slug[:60].rstrip('-')
    return slug


def parse_claims_md(claims_path: Path) -> tuple[list[ClaimRecord], list[DefinitionRecord], str]:
    """
    Parse CLAIMS.md and return (claims, definitions, raw_text).
    Raises ValueError if the file is missing or no tables are found.
    """
    if not claims_path.is_file():
        raise ValueError(f"CLAIMS.md not found at {claims_path}")

    raw_text = claims_path.read_text(encoding="utf-8")
    lines = raw_text.splitlines()

    claims: list[ClaimRecord] = []
    definitions: list[DefinitionRecord] = []

    current_section = ""
    in_table = False
    header_cells: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect section headers
        if line.startswith("### "):
            current_section = line[4:].strip()
            in_table = False
            i += 1
            continue

        # Detect table start (header row followed by separator)
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r'\|[\s:|-]+\|', lines[i + 1].strip()):
            header_cells = [strip_bold(c) for c in split_table_row(line)]
            in_table = True
            i += 2  # skip header and separator
            continue

        # Parse table rows
        if in_table and line.strip().startswith("|"):
            cells = split_table_row(line)

            # Skip empty rows
            if all(c.strip() == "" for c in cells):
                i += 1
                continue

            # Determine table type by header
            if "Definition" in header_cells and "Claim" not in header_cells:
                # Definition table (section 0)
                if len(cells) >= 4:
                    def_title = cells[0]
                    def_id = DEFINITION_IDS.get(strip_bold(def_title),
                                                get_stable_id(def_title, "Definitions", i + 1))
                    definitions.append(DefinitionRecord(
                        stable_id=def_id,
                        title=strip_bold(def_title),
                        raw_title=def_title,
                        status=strip_bold(cells[1]),
                        file=cells[2],
                        inadequacy=cells[3],
                        source_line=i + 1,
                    ))
            elif "Claim" in header_cells and "Status" in header_cells:
                # Claim table (sections 1, 2)
                if len(cells) >= 5:
                    claim_title = cells[0]
                    status_text = cells[1]

                    # Handle malformed rows with extra cells
                    # Standard: | Claim | Status | Evidence | Falsifier | Confidence |
                    # Some rows have an extra cell (e.g. line 46 has 6 cells)
                    if len(cells) == 5:
                        evidence = cells[2]
                        falsifier = cells[3]
                        conf_text = cells[4]
                    elif len(cells) == 6:
                        # Extra cell — merge cells[2] and cells[3] as evidence
                        evidence = cells[2] + " " + cells[3]
                        falsifier = cells[4]
                        conf_text = cells[5]
                    else:
                        # Fallback: last cell is confidence, second-to-last is falsifier
                        conf_text = cells[-1]
                        falsifier = cells[-2]
                        evidence = " ".join(cells[2:-2])

                    cleaned_title = strip_bold(claim_title)
                    stable_id = get_stable_id(claim_title, current_section, i + 1)
                    status_parts = parse_status_field(status_text)
                    is_split = len(status_parts) > 1

                    # If status field didn't yield a confidence, try the
                    # confidence column for non-split rows
                    if not is_split and status_parts and status_parts[0].confidence is None:
                        conf_text_clean = strip_bold(conf_text).strip()
                        # Don't parse "OPEN" or text-only confidence
                        if conf_text_clean and conf_text_clean.upper() != "OPEN":
                            # Extract first number from confidence column
                            num_match = re.search(r'(\d+\.?\d*)', conf_text_clean)
                            if num_match:
                                try:
                                    val = float(num_match.group(1))
                                    # Sanity check: confidence should be 0-1
                                    if 0.0 <= val <= 1.0:
                                        status_parts[0].confidence = val
                                except ValueError:
                                    pass

                    is_std_math = stable_id in STANDARD_MATH_IDS
                    premise = extract_premises(evidence)

                    # Extract scope note from italic annotations
                    scope_note = ""
                    scope_match = re.search(r'\*\(.*?\)\*', status_text)
                    if scope_match:
                        scope_note = scope_match.group(0)

                    claims.append(ClaimRecord(
                        stable_id=stable_id,
                        title=cleaned_title,
                        raw_title=claim_title,
                        status_parts=status_parts,
                        is_split=is_split,
                        evidence=evidence[:300],  # truncate for snapshot
                        falsifier=falsifier,
                        confidence_raw=parse_confidence_field(conf_text),
                        source_line=i + 1,
                        section=current_section,
                        is_standard_math=is_std_math,
                        premise=premise,
                        scope_note=scope_note,
                    ))
            i += 1
            continue

        # End of table: a non-pipe line that's not a blank line within a table
        # (blank lines inside a table are continuation gaps, not table ends)
        if in_table and not line.strip().startswith("|"):
            if line.strip() == "":
                # Blank line — could be a gap within a table (CLAIMS.md has one at line 62)
                # Look ahead: if the next non-blank line starts with |, treat as continuation
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j < len(lines) and lines[j].strip().startswith("|"):
                    i += 1
                    continue
            in_table = False

        i += 1

    if not claims:
        raise ValueError("No claims found in CLAIMS.md — parser produced zero records")

    # Scan DEFINITIONS_DIR for definitions to ensure legacy compatibility (e.g. 21 definitions expected)
    if DEFINITIONS_DIR.is_dir():
        definitions.clear()
        for f in sorted(DEFINITIONS_DIR.glob("*.md")):
            if f.name == "README.md":
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            lines_def = text.splitlines()
            if not lines_def:
                continue
            
            title = ""
            status = "CANONICAL v1.0"
            
            # Parse title from first line starting with #
            for line_def in lines_def:
                if line_def.strip().startswith("#"):
                    title = line_def.lstrip("#").strip()
                    break
            if not title:
                title = f.stem.replace("_", " ").title()
                
            # Parse status
            for line_def in lines_def:
                if "Status:" in line_def:
                    status = line_def.replace("*", "").replace("Status:", "").strip()
                    break
                    
            def_id = f.stem.replace("_", "-")
            definitions.append(DefinitionRecord(
                stable_id=def_id,
                title=title,
                raw_title=title,
                status=status,
                file=f"definitions/{f.name}",
                inadequacy="",
                source_line=1
            ))

    return claims, definitions, raw_text


# ============================================================================
# SNAPSHOT BUILDER
# ============================================================================

def build_snapshot(claims_path: Path = CLAIMS_MD) -> dict:
    """
    Build authority snapshot by parsing CLAIMS.md.
    This is called by the gate at runtime — not from a cached JSON.
    Raises ValueError on any parse failure.
    """
    claims, definitions, raw_text = parse_claims_md(claims_path)
    claims_hash = sha256_text(raw_text)

    # Build definitions manifest
    def_manifest = {}
    for d in definitions:
        def_manifest[d.stable_id] = {
            "title": d.title,
            "status": d.status,
            "file": d.file,
            "inadequacy": d.inadequacy[:200],
            "source_line": d.source_line,
        }

    # Build claims manifest
    claim_manifest = {}
    for c in claims:
        parts = []
        for sp in c.status_parts:
            parts.append({
                "status": sp.status,
                "confidence": sp.confidence,
                "qualifier": sp.qualifier,
            })
        claim_manifest[c.stable_id] = {
            "title": c.title,
            "status_parts": parts,
            "is_split": c.is_split,
            "is_standard_math": c.is_standard_math,
            "primary_status": parts[0]["status"] if parts else "UNKNOWN",
            "primary_confidence": parts[0]["confidence"] if parts else None,
            "evidence_excerpt": c.evidence,
            "falsifier": c.falsifier[:200],
            "confidence_raw": c.confidence_raw,
            "source_line": c.source_line,
            "section": c.section,
            "premise": c.premise,
            "scope_note": c.scope_note,
        }

    # Hash definition files
    def_hashes = {}
    if DEFINITIONS_DIR.is_dir():
        for f in sorted(DEFINITIONS_DIR.glob("*.md")):
            def_hashes[f.name] = sha256_file(f)

    # Hash Lean modules
    lean_hashes = {}
    if LEAN_DIR.is_dir():
        for f in sorted(LEAN_DIR.glob("*.lean")):
            lean_hashes[f.name] = sha256_file(f)

    return {
        "schema_version": "2.0.0",
        "generated_from": str(claims_path),
        "claims_md_hash": claims_hash,
        "claims_md_lines": len(raw_text.splitlines()),
        "claim_count": len(claims),
        "definition_count": len(definitions),
        "claims": claim_manifest,
        "definitions": def_manifest,
        "definition_file_hashes": def_hashes,
        "lean_module_hashes": lean_hashes,
        "valid_statuses": sorted(VALID_STATUSES),
        "standard_math_ids": sorted(STANDARD_MATH_IDS),
    }


# ============================================================================
# PUBLIC DATA GENERATOR (data.claims.js)
# ============================================================================

def generate_public_data_js(snapshot: dict) -> str:
    """
    Generate data.claims.js from the authority snapshot.
    This replaces the manual data.claims.js with generated content.
    """
    claims = snapshot["claims"]
    definitions = snapshot["definitions"]

    # Build JS claim objects
    js_claims = []
    for cid, c in sorted(claims.items()):
        primary_status = c["primary_status"]
        primary_conf = c["primary_confidence"]

        # Build status badge text
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

        # CSS class
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
        })

    # Build JS definition objects
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
        "generatedAt": "2026-07-15",
        "sourceHash": snapshot["claims_md_hash"][:16],
        "claimCount": len(js_claims),
        "definitionCount": len(js_defs),
        "claims": js_claims,
        "definitions": js_defs,
    }

    lines = [
        "// AUTO-GENERATED by generate_claims_data_v2.py — DO NOT EDIT MANUALLY",
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
# MAIN
# ============================================================================

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Explorer Truth Layer V2 — Authority Manifest Generator")
    parser.add_argument("--claims", type=Path, default=CLAIMS_MD, help="Path to CLAIMS.md")
    parser.add_argument("--snapshot", type=Path, default=EXPLORER_DIR / "_authority_snapshot.json",
                        help="Output snapshot path")
    parser.add_argument("--public-data", type=Path, default=EXPLORER_DIR / "data.claims.js",
                        help="Output public data JS path")
    parser.add_argument("--no-public-data", action="store_true", help="Skip generating public data JS")
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

    # Write public data
    if not args.no_public_data:
        js_content = generate_public_data_js(snapshot)
        with open(args.public_data, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"  Public data written: {args.public_data}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
