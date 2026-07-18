#!/usr/bin/env python3.12
"""
Claim Boundary Check — "No accommodation language. DERIVED, OPEN, or HONEST NEGATIVE."
=====================================
Rejects PF claims that use decoration instead of derivation. Run before any claim
enters CLAIMS.md or before publishing a claim outside the family.

Usage:
    python3.12 claim_boundary_check.py "The PF accommodates thermodynamics."
    python3.12 claim_boundary_check.py --file /mnt/d/fundamentals/CLAIMS.md
    python3.12 claim_boundary_check.py --stdin

Gate: PASS / REJECT
Author: Hermes · 2026-07-01
"""

import argparse
import re
import sys
from pathlib import Path

# ── Banned accommodation phrases ──
# These are decoration. They feel like a claim but prove nothing.
# If any appear in a PF claim, REJECT — no derivation exists.
BANNED = [
    r"\baccommodates?\b",
    r"\bis consistent with\b",
    r"\bnaturally extends? to\b",
    r"\bshould emerge\b",
    r"\bis built to handle\b",
    r"\bis compatible with\b",
    r"\bsupports\b",
    r"\baligns? with\b",
    r"\bis.*-adjacent\b",
    r"\bis.*-addressable\b",
    r"\bwould follow from\b",
    r"\bcould be derived\b",
    r"\bsuggests\b",
    r"\bimplies\b",
    r"\bpoints to\b",
    r"\blays the groundwork for\b",
    r"\bopens the door to\b",
    r"\bpaves the way for\b",
    r"\bsets the stage for\b",
    r"\bprovides a foundation for\b",
]

# ── Required vocabulary ──
# If a claim is making a physics statement, one of these should appear
# (or it should be marked OPEN)
REQUIRED_TERMS = [
    "DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
    "INTUITION", "OPEN", "HONEST NEGATIVE", "WITHDRAWN",
]


def check_claim(text: str, source: str = "stdin") -> tuple[bool, list[str]]:
    """Check a claim for banned accommodation language.
    
    Returns (passed, violations) where passed=True means the claim is clean
    and violations lists what was found if not.
    """
    violations = []
    lowered = text.lower()

    for pattern in BANNED:
        matches = re.findall(pattern, lowered)
        for match in matches:
            violations.append(f"'{match}' — banned accommodation language")

    # Check if claim has a confidence tier or is marked OPEN
    has_tier = any(term.lower() in lowered for term in REQUIRED_TERMS)

    return len(violations) == 0, violations, has_tier


def main():
    parser = argparse.ArgumentParser(
        description="Claim Boundary Check — reject accommodation language in PF claims"
    )
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument("text", nargs="?", help="Claim text to check")
    source_group.add_argument("--file", help="Path to file containing claims")
    source_group.add_argument("--stdin", action="store_true", help="Read claim from stdin")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"REJECT: File not found: {args.file}")
            sys.exit(1)
        text = path.read_text(encoding="utf-8", errors="replace")
        source = args.file
    elif args.stdin:
        text = sys.stdin.read()
        source = "stdin"
    elif args.text:
        text = args.text
        source = "argument"
    else:
        parser.print_help()
        sys.exit(1)

    passed, violations, has_tier = check_claim(text, source)

    if not passed:
        print(f"REJECT — {len(violations)} banned phrase(s) in {source}:")
        for v in list(dict.fromkeys(violations)):  # dedupe
            print(f"  • {v}")
        print()
        print("Accommodation language proves nothing. Rewrite using only:")
        print("  DERIVED | CONDITIONAL | ARGUED | EMPIRICAL | INTUITION | OPEN | HONEST NEGATIVE | WITHDRAWN")
        print()
        print("If no derivation from PF axioms exists, the claim is OPEN.")
        sys.exit(1)

    if not has_tier:
        print(f"PASS with warning — no confidence tier detected in {source}")
        print("Add one: DERIVED | CONDITIONAL | ARGUED | EMPIRICAL | INTUITION | OPEN")
        sys.exit(0)

    print(f"PASS — {source} is clean")
    sys.exit(0)


if __name__ == "__main__":
    main()
