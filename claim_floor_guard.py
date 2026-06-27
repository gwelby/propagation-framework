#!/usr/bin/env python3.12
"""
Dependency floor-rule guard for Fundamentals claims.

Reads CLAIMS.md + a dependency metadata file, checks that no claim's
confidence/status exceeds its weakest unresolved parent.

Usage:
    python3 claim_floor_guard.py [--json]
    python3 claim_floor_guard.py --build-status  # Report PfLean build status

Exit codes:
    0 = all claims respect floor rules
    1 = floor rule violations found
    2 = metadata or parsing error
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


CLAIMS_PATH = Path("/mnt/d/Fundamentals/CLAIMS.md")
DEPENDENCIES_PATH = Path("/mnt/d/Fundamentals/claim_dependencies.json")
LEAN_ROOT = Path("/mnt/d/Fundamentals/lean")


@dataclass
class Claim:
    name: str
    status: str
    confidence: float
    depends_on: list[str]
    lean_module: str | None
    notes: str


def parse_confidence(status_str: str) -> float:
    """Extract numeric confidence from status string like '0.95' or '0.88'."""
    nums = re.findall(r"0\.\d+|1\.00?", status_str)
    if nums:
        return float(nums[-1])
    return 0.0


def extract_claims_table(claims_text: str) -> list[dict[str, str]]:
    """Parse the Fundamental Physics claims table from CLAIMS.md."""
    rows = []
    in_table = False
    lines = claims_text.splitlines()

    for i, line in enumerate(lines):
        # Look for the start of the claims table
        if "### 1. Fundamental Physics" in line:
            in_table = True
            continue
        if in_table and line.startswith("### ") and "1. Fundamental Physics" not in line:
            # Next section
            break
        if not in_table:
            continue

        # Table row: | Claim | Status | Evidence | What Falsifies It | Confidence |
        if line.startswith("|") and "Claim" not in line and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 5:
                rows.append({
                    "claim": cells[0],
                    "status": cells[1],
                    "evidence": cells[2] if len(cells) > 2 else "",
                    "falsifies": cells[3] if len(cells) > 3 else "",
                    "confidence": cells[4] if len(cells) > 4 else "",
                })

    return rows


def load_dependencies() -> dict[str, Any]:
    """Load or create default claim dependencies."""
    if DEPENDENCIES_PATH.exists():
        return json.loads(DEPENDENCIES_PATH.read_text())

    # Default fixtures as specified by Codex
    defaults = {
        "claims": {
            "God Equation — Postulate-D Z₃ operator algebra": {
                "depends_on": ["Postulate D (Primitive Z₃ no-self-loop selector)"],
                "lean_module": None,
                "max_confidence": 0.88,
            },
            "Weinberg Angle (sin²θ_W)": {
                "depends_on": ["Axiom 3b (Minimal Winding Principle)", "Casimir polynomial derivation"],
                "lean_module": "PfLean.WeinbergAngle",
                "max_confidence": 0.65,
            },
            "(2,1) Topological Weights": {
                "depends_on": ["SU(2) double cover homomorphism"],
                "lean_module": "PfLean.TopologicalWeights",
                "max_confidence": 0.95,
            },
            "Koide Law for Charged Leptons (Q = 2/3)": {
                "depends_on": ["Equal-amplitude premise (U(1)_em coupling)"],
                "lean_module": "PfLean.KoideGeometry",
                "max_confidence": 0.95,
            },
            "Gravity as Optical Geometry / Refraction": {
                "depends_on": ["Null geodesics in static/stationary spacetimes"],
                "lean_module": "PfLean.GravityOptics",
                "max_confidence": 0.95,
            },
            "Three Generations": {
                "depends_on": [
                    "(2,1) Topological Weights physical realization",
                    "M = 3 denominator theorem"
                ],
                "lean_module": "PfLean.ThreeGenerations",
                "max_confidence": 0.85,
            },
            "SO(2) Rotation Group Structure": {
                "depends_on": [],
                "lean_module": "PfLean.SO2Rotation",
                "max_confidence": 1.0,
            },
            "SO(3) Double Cover": {
                "depends_on": [],
                "lean_module": "PfLean.SO3DoubleCover",
                "max_confidence": 1.0,
            },
        },
        "_meta": {
            "description": "Dependency metadata for Fundamentals claims floor-rule guard.",
            "rule": "A claim's effective confidence cannot exceed the minimum confidence of its unresolved dependencies.",
            "created": "2026-06-17",
        }
    }
    DEPENDENCIES_PATH.write_text(json.dumps(defaults, indent=2))
    return defaults


def check_floor_rules(claims: list[dict], deps: dict) -> list[dict]:
    """Check that no claim exceeds its dependency floor."""
    violations = []
    claim_map = {c["claim"]: c for c in claims}

    for claim_name, meta in deps.get("claims", {}).items():
        claim = claim_map.get(claim_name)
        if not claim:
            continue

        conf = parse_confidence(claim["confidence"])
        depends_on = meta.get("depends_on", [])
        max_allowed = meta.get("max_confidence", 1.0)

        # Check declared max_confidence
        if conf > max_allowed + 0.001:
            violations.append({
                "claim": claim_name,
                "type": "exceeds_declared_max",
                "actual_confidence": conf,
                "max_allowed": max_allowed,
                "detail": f"Claim confidence {conf} exceeds declared max {max_allowed}",
            })

        # Check dependency floors
        for dep_name in depends_on:
            dep_claim = claim_map.get(dep_name)
            if not dep_claim:
                # Dependency not in scoreboard — treat as unresolved
                violations.append({
                    "claim": claim_name,
                    "type": "unresolved_dependency",
                    "dependency": dep_name,
                    "detail": f"Dependency '{dep_name}' not found in CLAIMS.md — treated as OPEN (floor=0.0)",
                })
                continue

            dep_conf = parse_confidence(dep_claim["confidence"])
            dep_status = dep_claim["status"].upper()

            # If dependency is not DERIVED/EXACT/CONDITIONAL, it caps the child
            if "DERIVED" not in dep_status and "EXACT" not in dep_status and "CONDITIONAL" not in dep_status:
                if conf > dep_conf + 0.001:
                    violations.append({
                        "claim": claim_name,
                        "type": "floor_violation",
                        "dependency": dep_name,
                        "actual_confidence": conf,
                        "dependency_confidence": dep_conf,
                        "dependency_status": dep_status,
                        "detail": f"Confidence {conf} exceeds dependency floor {dep_conf} ({dep_status})",
                    })
            elif conf > dep_conf + 0.001:
                # Even if dependency is solid, child can't exceed it
                violations.append({
                    "claim": claim_name,
                    "type": "floor_violation",
                    "dependency": dep_name,
                    "actual_confidence": conf,
                    "dependency_confidence": dep_conf,
                    "dependency_status": dep_status,
                    "detail": f"Confidence {conf} exceeds dependency confidence {dep_conf}",
                })

    return violations


def check_lean_build_status() -> dict[str, Any]:
    """Check which PfLean modules have .olean files."""
    build_dir = LEAN_ROOT / ".lake/build/lib/lean/PfLean"
    modules = {
        "WeinbergAngle": "PfLean.WeinbergAngle",
        "KoideGeometry": "PfLean.KoideGeometry",
        "GravityOptics": "PfLean.GravityOptics",
        "TopologicalWeights": "PfLean.TopologicalWeights",
        "ThreeGenerations": "PfLean.ThreeGenerations",
        "SO2Rotation": "PfLean.SO2Rotation",
        "SO3DoubleCover": "PfLean.SO3DoubleCover",
        "CollatzSyracuse": "PfLean.CollatzSyracuse",
        "ShorBound": "PfLean.ShorBound",
        "U3Decomposition": "PfLean.U3Decomposition",
        "Basic": "PfLean.Basic",
        "CasimirPolynomial": "PfLean.CasimirPolynomial",
        "CrossModuleBridge": "PfLean.CrossModuleBridge",
        "PFCore": "PfLean.PFCore",
        "ProcessOntology": "PfLean.ProcessOntology",
    }

    status = {}
    for name, module in modules.items():
        olean = build_dir / f"{name}.olean"
        status[module] = {
            "olean_exists": olean.exists(),
            "olean_path": str(olean) if olean.exists() else None,
            "olean_timestamp": olean.stat().st_mtime if olean.exists() else None,
        }

    return status


def run_build_check(module: str) -> dict[str, Any]:
    """Run lake build for a specific module and capture output."""
    try:
        proc = subprocess.run(
            ["lake", "build", module],
            cwd=str(LEAN_ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "module": module,
            "exit_code": proc.returncode,
            "stdout_tail": "\n".join(proc.stdout.splitlines()[-10:]),
            "stderr_tail": "\n".join(proc.stderr.splitlines()[-10:]),
        }
    except Exception as e:
        return {
            "module": module,
            "exit_code": -1,
            "error": str(e),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--build-status", action="store_true", help="Report PfLean build status only")
    parser.add_argument("--build-module", help="Run lake build for a specific module")
    args = parser.parse_args()

    if args.build_module:
        result = run_build_check(args.build_module)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Module: {result['module']}")
            print(f"Exit code: {result['exit_code']}")
            if result.get("stdout_tail"):
                print("STDOUT tail:")
                print(result["stdout_tail"])
            if result.get("stderr_tail"):
                print("STDERR tail:")
                print(result["stderr_tail"])
            if result.get("error"):
                print(f"ERROR: {result['error']}")
        return 0 if result.get("exit_code") == 0 else 1

    if args.build_status:
        status = check_lean_build_status()
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print("=== PfLean Build Status ===")
            for module, info in status.items():
                icon = "✅" if info["olean_exists"] else "❌"
                print(f"  {icon} {module}")
                if info["olean_exists"]:
                    print(f"     olean: {info['olean_path']}")
        return 0

    # Main floor-rule check
    if not CLAIMS_PATH.exists():
        print(f"ERROR: {CLAIMS_PATH} not found", file=sys.stderr)
        return 2

    claims_text = CLAIMS_PATH.read_text(errors="replace")
    claims = extract_claims_table(claims_text)
    deps = load_dependencies()

    violations = check_floor_rules(claims, deps)
    lean_status = check_lean_build_status()

    result = {
        "status": "PASS" if not violations else "FAIL",
        "claims_parsed": len(claims),
        "violations_count": len(violations),
        "violations": violations,
        "lean_build_status": lean_status,
        "dependencies_file": str(DEPENDENCIES_PATH),
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"=== Claim Floor-Rule Guard ===")
        print(f"Claims parsed: {len(claims)}")
        print(f"Violations: {len(violations)}")
        if violations:
            print("\n--- Violations ---")
            for v in violations:
                print(f"  ❌ {v['claim']}")
                print(f"     Type: {v['type']}")
                print(f"     Detail: {v['detail']}")
        else:
            print("\n✅ All claims respect floor rules.")

        print("\n=== Lean Build Status ===")
        for module, info in lean_status.items():
            icon = "✅" if info["olean_exists"] else "❌"
            print(f"  {icon} {module}")

    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
