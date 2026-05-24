"""Release guard for public-facing Propagation Framework claims.

This check is intentionally narrow: it catches the stale overclaims that have
already been identified in sprint briefs and public-claim audits. It does not
try to prove the papers are correct; it blocks known bad release language.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PUBLIC_FILES = [
    ROOT / "README.md",
    ROOT / "papers" / "PUBLISHABLE_CORE_DRAFT.md",
    ROOT / "papers" / "FALSIFICATION_PAPER_DRAFT.md",
    ROOT / "sandbox" / "explorer" / "data.claims.js",
    ROOT / "sandbox" / "explorer" / "derivation.html",
    ROOT / "sandbox" / "explorer" / "playground.html",
]


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    message: str


RULES = [
    Rule(
        "t1_not_derived_098",
        re.compile(r"Topological Weights[\s\S]{0,120}(?:Derived|DERIVED)[\s\S]{0,40}0\.98", re.IGNORECASE),
        "T1/topological weights must not be public as DERIVED 0.98; use PARTIAL DERIVATION 0.85.",
    ),
    Rule(
        "t3_not_derived_098",
        re.compile(r"(?:Three Generations|Number of Generations|N=3)[\s\S]{0,160}(?:Derived|DERIVED)[\s\S]{0,40}0\.98", re.IGNORECASE),
        "Three Generations must not be public as DERIVED 0.98; use CONDITIONAL 0.85.",
    ),
    Rule(
        "sleep_not_derived_092",
        re.compile(r"(?:8h Sleep|8-hour sleep|sleep constant)[\s\S]{0,120}(?:Derived|DERIVED)[\s\S]{0,40}0\.92", re.IGNORECASE),
        "8h sleep constant must not be public as DERIVED 0.92; use ARGUED 0.72.",
    ),
    Rule(
        "god_equation_not_04_percent",
        re.compile(r"(?:God Equation|lambda_c|λ_c)[\s\S]{0,260}0\.4\\?%", re.IGNORECASE),
        "God Equation public error must be 1.48%, not stale 0.4%.",
    ),
    Rule(
        "no_physics_solved",
        re.compile(r"\b(?:physics solved|solved physics|everything derived|God Equation proved)\b", re.IGNORECASE),
        "Release copy must not claim physics solved or God Equation proved.",
    ),
    Rule(
        "koide_not_reciprocal_normalized",
        re.compile(r"Q\s*=\s*\(Σ√mᵢ\)\²\s*/\s*\(3·Σmᵢ\)\s*=\s*2/3", re.IGNORECASE),
        "Public Koide Q must use Q = Σmᵢ/(Σ√mᵢ)^2, not the reciprocal-normalized convention.",
    ),
    Rule(
        "generations_not_unqualified_derived",
        re.compile(r"framework derives the\s+(?:<em>)?three generations", re.IGNORECASE),
        "Three Generations public copy must be conditional on T1/T2 bridges.",
    ),
]


def scan_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    for rule in RULES:
        match = rule.pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            failures.append(f"{path.relative_to(ROOT)}:{line}: {rule.name}: {rule.message}")
    return failures


def main() -> int:
    failures: list[str] = []
    for path in PUBLIC_FILES:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT)}: missing public release file")
            continue
        failures.extend(scan_file(path))

    if failures:
        print("PUBLIC CLAIM GUARD: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PUBLIC CLAIM GUARD: PASS")
    print(f"Scanned {len(PUBLIC_FILES)} release-facing files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
