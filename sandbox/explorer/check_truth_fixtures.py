#!/usr/bin/env python3
"""Negative fixtures for the Explorer truth layer.

Each fixture tests a specific known overclaim pattern that was identified
in the Codex 2026-07-15 audit. The fixture provides a FAIL case (the overclaim)
and a PASS case (the corrected version).

These fixtures are run by check_truth_drift.py as part of the release gate.
They ensure that the drift gate would catch regressions if any of the known
overclaims were reintroduced.

Usage:
    python3 check_truth_fixtures.py

Exit code 0 = all fixtures pass (drift gate catches the overclaims)
Exit code 1 = one or more fixtures fail (drift gate has a blind spot)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent


# ─── Fixture definitions ─────────────────────────────────────────────────────
# Each fixture has:
# - id: the known overclaim case
# - fail_text: text that SHOULD trigger the forbidden pattern
# - pass_text: corrected text that should NOT trigger the pattern
# - pattern: the regex to test

FIXTURES = [
    {
        "id": "weinberg-as-derived",
        "description": "Weinberg angle must not appear as DERIVED or with confidence ≥ 0.90",
        "fail_text": 'id: "weinberg-angle", status: STATUS.DERIVED, confidence: 0.90',
        "pass_text": 'id: "weinberg-angle", status: STATUS.ARGUED, confidence: 0.65',
        "pattern": r'weinberg.*?status.*?DERIVED|weinberg.*?confidence.*?0\.9[0-9]',
    },
    {
        "id": "stale-0.4-percent",
        "description": "The stale 0.4% error must not appear (correct value is 1.48%)",
        "fail_text": "The (3,3) point is anchored at 1.145e-18 m and 0.4% error.",
        "pass_text": "The (3,3) point is anchored at 1.157e-18 m and 1.48% error.",
        "pattern": r'0\.4%\s*error|0\.4\s*percent',
    },
    {
        "id": "codex-audit-passed",
        "description": "'Codex audit passed' is false — current verdict is HOLD",
        "fail_text": "CLAIMS.md -> data.claims.js -> UI. Codex audit passed. Status badges are data.",
        "pass_text": "CLAIMS.md -> data.claims.js -> UI. Status badges are data-driven. Public release HOLD pending Codex re-audit.",
        "pattern": r'[Cc]odex\s+audit\s+passed',
    },
    {
        "id": "dark-matter-explained",
        "description": "Dark matter must not be claimed as 'explained' — no matching claim row",
        "fail_text": "Spiral arms as standing density waves. Dark matter explained entirely via refractive geometry.",
        "pass_text": "Spiral arms as standing density waves. Galactic rotation in the refractive medium framework — dark matter interpretation remains open.",
        "pattern": r'[Dd]ark\s+matter\s+(explained|solved|derived)',
    },
    {
        "id": "reality-derives-from-three-axioms",
        "description": "Axioms define vocabulary, not all results derived",
        "fail_text": "Interactive visualization of how reality derives from three axioms",
        "pass_text": "Interactive visualization of the Propagation Framework — claims, derivations, and open questions",
        "pattern": r'reality\s+derives?\s+from\s+three\s+axioms|everything\s+else\s+derived',
    },
    {
        "id": "seven-approaches-converged",
        "description": "'Seven approaches converged' language was WITHDRAWN",
        "fail_text": "Seven approaches converged and 52.7× decisive evidence.",
        "pass_text": "The previously claimed convergence language has been withdrawn per Codex audit.",
        "pattern": r'seven\s+approaches\s+converged|52\.7[x×]',
    },
    {
        "id": "god-equation-verified-on-silicon",
        "description": "IBM hardware did NOT measure −1/8 eigenvalue on silicon",
        "fail_text": "The God Equation was verified on silicon by IBM Quantum hardware.",
        "pass_text": "IBM Quantum hardware provided calibration support but did not measure the eigenvalue on silicon.",
        "pattern": r'[Gg]od\s+[Ee]quation\s+\w*\s*verified\s+on\s+silicon|verified.*?silicon.*?eigenvalue',
    },
    {
        "id": "koide-physical-selection-complete",
        "description": "Koide physical vacuum selection is OPEN, not completed",
        "fail_text": "Koide's physical vacuum selection has been derived and proven.",
        "pass_text": "Koide's physical vacuum selection remains an open question.",
        "pattern": r'[Kk]oide.*?(physical\s+selection|vacuum\s+selection).*?(derived|proved|closed|complete)',
    },
    {
        "id": "consciousness-promoted",
        "description": "Consciousness is INTUITION 0.48, must not be promoted",
        "fail_text": 'id: "consciousness-claim", status: STATUS.DERIVED, confidence: 0.75',
        "pass_text": 'id: "consciousness-claim", status: STATUS.INTUITION, confidence: 0.48',
        "pattern": r'consciousness.*?status.*?(DERIVED|CONDITIONAL|EMPIRICAL)|consciousness.*?confidence.*?0\.[5-9]',
    },
    {
        "id": "bohr-spectrum-underclaimed",
        "description": "Bohr spectrum was upgraded to DERIVED 0.90 after Kepler degeneracy proof",
        "fail_text": 'id: "bohr-spectrum", status: STATUS.CONDITIONAL, confidence: 0.82',
        "pass_text": 'id: "bohr-spectrum", status: STATUS.DERIVED, confidence: 0.90',
        "pattern": r'bohr.*?status.*?CONDITIONAL|bohr.*?confidence.*?0\.8[0-2]',
    },
]


def run_fixtures() -> int:
    failures = 0

    print("=== Explorer Truth Drift Negative Fixtures ===")
    print()

    for fixture in FIXTURES:
        fid = fixture["id"]
        desc = fixture["description"]
        pattern = fixture["pattern"]
        fail_text = fixture["fail_text"]
        pass_text = fixture["pass_text"]

        # Test 1: fail_text MUST trigger the pattern
        fail_matches = re.findall(pattern, fail_text, re.IGNORECASE)
        if not fail_matches:
            print(f"  FAIL: {fid}")
            print(f"    The drift gate would NOT catch the known overclaim:")
            print(f"    Pattern: {pattern}")
            print(f"    Text:    {fail_text}")
            failures += 1
        else:
            # Test 2: pass_text must NOT trigger the pattern
            pass_matches = re.findall(pattern, pass_text, re.IGNORECASE)
            if pass_matches:
                print(f"  FAIL: {fid}")
                print(f"    The drift gate would FALSE-POSITIVE on the corrected text:")
                print(f"    Pattern: {pattern}")
                print(f"    Text:    {pass_text}")
                failures += 1
            else:
                print(f"  PASS: {fid} — {desc}")

    print()
    print("=== Summary ===")
    if failures == 0:
        print(f"PASS: All {len(FIXTURES)} negative fixtures verified.")
        print("The drift gate correctly catches all known overclaim patterns.")
        return 0
    else:
        print(f"FAIL: {failures}/{len(FIXTURES)} fixtures failed.")
        print("The drift gate has blind spots that need fixing.")
        return 1


if __name__ == "__main__":
    sys.exit(run_fixtures())
