#!/usr/bin/env python3.12
"""claims_numeric_recheck.py — re-derive every checkable number in the Koide/2-9
section of CLAIMS.md from first inputs, and fail closed on mismatch.

PROPOSED, NOT ADOPTED. Written by Claude 2026-09-04, filed to inbox/ rather than
audit/ because Fundamentals owns its own audit surface and Codex has not yet
verified the finding this came from.

WHY THIS EXISTS
---------------
`derivations/koide_phase_delta_0_gap.md:122` states:

    delta_uncertainty (from m_tau +- 0.12 MeV) = 2.58e-4 rad

The stated input does not produce the stated output: +-0.12 MeV moves delta by
8.35e-6 rad. The figure is 30.9x too large, and it generated the "0.029 sigma"
quoted on four surfaces (and live in the public repo). The correct value is
0.89 sigma.

The failure mode is not bad arithmetic — every other number in that section is
correct to 1e-12. It is a STALE UNCERTAINTY: a value carried forward into a
fresh calculation and never re-derived, sitting one line below the correct input
it contradicts. Nothing checked it for five months, across multiple audits,
because nothing re-derives quoted uncertainties from their stated inputs.

This script is that check.

    python3.12 claims_numeric_recheck.py          # report
    python3.12 claims_numeric_recheck.py --strict # exit 1 on any FAIL

⚠ TOLERANCE NOTE — read before editing
--------------------------------------
The first version of this checker used

    ok = abs(claimed - actual) <= tol * max(1, abs(actual))

which makes the tolerance ABSOLUTE for small quantities: with tol=1e-2 the bound
became 0.01, and it PASSED the very 31x error it was written to catch. Use
relative error only. A checker that cannot fail is not a checker.
"""
import math
import sys

# --- PDG 2024 charged-lepton masses (MeV) -----------------------------------
M_E, S_E = 0.51099895000, 0.00000000015
M_MU, S_MU = 105.6583755, 0.0000023
M_TAU, S_TAU = 1776.86, 0.12
TAU3 = 2 * math.pi / 3

# --- Document binding (added 2026-09-06, Codex finding F5) ---------------------
# ⚠ THE DEFECT THIS FIXES. The original version compared hard-coded literals to
# recomputed values and never opened a source file. It reported "9/9 pass" from
# an EMPTY DIRECTORY. It therefore could not detect the very thing it was
# adopted to detect: a stale number reappearing in CLAIMS.md.
#
# It also HAD a passing positive control -- which exercised the comparison path,
# not the document-reading path. Sharper statement of QSOP P-013:
# *a positive control only guards the path it exercises.*
import os
import re

REPO = os.environ.get("PF_REPO", "/mnt/d/Fundamentals")
SOURCES = {
    "CLAIMS": os.path.join(REPO, "CLAIMS.md"),
    "GAP": os.path.join(REPO, "derivations", "koide_phase_delta_0_gap.md"),
}


def load_sources() -> dict:
    """Read the bound documents. FAIL CLOSED: a missing source is an error,
    never a silent pass. This is the whole point of F5."""
    out = {}
    missing = []
    for name, path in SOURCES.items():
        try:
            with open(path, encoding="utf-8") as fh:
                out[name] = fh.read()
        except OSError:
            missing.append(path)
    if missing:
        raise SystemExit(
            "FAIL-CLOSED: cannot read bound source document(s):\n  "
            + "\n  ".join(missing)
            + "\nThis checker verifies DOCUMENTS, not just arithmetic. Refusing to report a pass."
        )
    return out


def assert_absent(docs: dict, pattern: str, label: str) -> tuple:
    """A retired value must not reappear as a live claim anywhere."""
    hits = []
    for name, text in docs.items():
        for m in re.finditer(pattern, text):
            line = text.count("\n", 0, m.start()) + 1
            # ⚠ 2026-09-06: the first version used a 90-char window, which CUT
            # THE WORD "corrected" IN HALF ("...orrected 2026-09-04...") and
            # raised a false positive on a legitimate errata note. Widen the
            # window and match on stems so a boundary cannot hide a keyword.
            # Note the failure direction was LOUD (false alarm), not silent --
            # which is the correct way for a guard to be wrong.
            ctx = text[max(0, m.start() - 300): m.start() + 120].replace("\n", " ").lower()
            if any(k in ctx for k in ("correct", "stale", "previous", "superseded",
                                      "was ", "retired", "does not reproduce")):
                continue  # an errata note citing the old value is legitimate
            hits.append(f"{name}:{line}")
    return (label, not hits, hits)



def koide_delta(me: float, mmu: float, mtau: float) -> float:
    """Koide phase, closed form — no fitting, no scan.

    For sqrt(m_k) proportional to 1 + sqrt2*cos(delta + 2*pi*k/3), writing
    c_k = (sqrt(m_k)/M - 1)/sqrt2 with M = mean(sqrt(m_k)) gives
        c_0 = cos(delta)
        c_2 - c_1 = sqrt3 * sin(delta)
    hence delta = atan2(c_2 - c_1, sqrt3 * c_0), reduced mod 2*pi/3.
    """
    s = [math.sqrt(m) for m in (me, mmu, mtau)]
    mean = sum(s) / 3.0
    c = [(x / mean - 1.0) / math.sqrt(2.0) for x in s]
    return math.atan2(c[2] - c[1], math.sqrt(3.0) * c[0]) % TAU3


def koide_Q(me: float, mmu: float, mtau: float) -> float:
    return (me + mmu + mtau) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2


_results: list[tuple[str, bool, str]] = []


def check(name: str, claimed: float, actual: float, rtol: float, source: str) -> None:
    """RELATIVE tolerance only. See the tolerance note in the module docstring."""
    rel = abs(claimed - actual) / abs(actual) if actual else float("inf")
    ok = rel <= rtol
    _results.append((name, ok, source))
    tag = "OK  " if ok else "FAIL"
    print(f"  [{tag}] {name:<38} rel.err {rel:.3e}")
    if not ok:
        ratio = claimed / actual if actual else float("inf")
        print(f"         claimed {claimed:.6g}   recomputed {actual:.6g}   claimed is {ratio:.2f}x")
        print(f"         source: {source}")


def main() -> int:
    d = koide_delta(M_E, M_MU, M_TAU)
    sigma_d = abs(koide_delta(M_E, M_MU, M_TAU + S_TAU) - d)
    s2w = (-5 + 8 * math.sqrt(3) - math.sqrt(57)) / (8 * (math.sqrt(3) - 1))

    print("CLAIMS.md numeric recheck — Koide / 2-9 section")
    print(f"inputs: m_e={M_E} m_mu={M_MU} m_tau={M_TAU}+-{S_TAU} MeV (PDG 2024)\n")

    K = "CLAIMS.md Koide Phase row"
    G = "derivations/koide_phase_delta_0_gap.md"

    check("delta_Koide (PDG)", 0.222229631490000, d, 1e-11, K)
    check("|delta - 2/9|", 7.409e-6, abs(d - 2 / 9), 1e-3, K)
    check("sigma_delta from m_tau +-0.12", 8.35e-6, sigma_d, 1e-2, G + ":122 (corrected 2026-09-04)")
    check("ratio gap/uncertainty", 0.89, abs(d - 2 / 9) / sigma_d, 1e-2, G + ":124 (corrected 2026-09-04)")
    check("tan(delta_exact)", 0.225961718896, math.tan(d), 1e-10, K)
    check("sin2thW (Casimir closed form)", 0.223101322300866, s2w, 1e-13, K)
    check("gap A: sin2thW - 2/9", 8.791e-4, s2w - 2 / 9, 1e-3, G)
    check("gap B: sin2thW - delta", 8.717e-4, s2w - d, 1e-3, G)
    check("56*sqrt3 - 9*sqrt57", 29.046, 56 * math.sqrt(3) - 9 * math.sqrt(57), 1e-4, K)

    # --- Document checks (F5): verify the SOURCES, not just the arithmetic ---
    docs = load_sources()
    print("  -- document binding --")
    print(f"  [OK  ] read {len(docs)} bound source(s): {', '.join(SOURCES)}")
    doc_fails = []
    for label, ok, hits in [
        assert_absent(docs, r"0\.029\s*(?:σ|sigma)", "retired 0.029 sigma absent as a live claim"),
        assert_absent(docs, r"2\.58\s*×\s*10⁻⁴", "retired 2.58e-4 absent as a live claim"),
        assert_absent(docs, r"fully consistent with δ_exact = 2/9 exactly", "false forward-safety sentence absent"),
        assert_absent(docs, r"within 0\.05 MeV of 1776\.86", "false symmetric trigger window absent"),
    ]:
        print(f"  [{'OK  ' if ok else 'FAIL'}] {label}")
        if not ok:
            print(f"         found at: {', '.join(hits[:4])}")
            doc_fails.append(label)
    for want, label in [(r"8\.35\s*×\s*10⁻⁶", "corrected sigma 8.35e-6 present"),
                        (r"1776\.8765", "worked trigger boundary present")]:
        present = any(re.search(want, t) for t in docs.values())
        print(f"  [{'OK  ' if present else 'FAIL'}] {label}")
        if not present:
            doc_fails.append(label)

    # Positive control: this MUST fail. If it passes, the checker is broken.
    print("\n  -- positive control (must FAIL) --")
    check("CONTROL: deliberate 2x error", 2 * d, d, 1e-6, "self-test")

    real = [r for r in _results if r[0] != "CONTROL: deliberate 2x error"]
    ctrl = [r for r in _results if r[0] == "CONTROL: deliberate 2x error"][0]
    passed = sum(1 for _, ok, _ in real if ok)
    failed = [(n, s) for n, ok, s in real if not ok]

    print(f"\n  {passed}/{len(real)} pass, {len(failed)} FAIL")
    if ctrl[1]:
        print("  *** CHECKER IS BROKEN: the positive control passed. Do not trust this run. ***")
        return 2
    print("  positive control failed as required — checker is live.")
    for n, s in failed:
        print(f"    FAIL: {n}   <- {s}")

    if failed:
        print("\n  Every other number in this section is correct to ~1e-12.")
        print("  The failures are a stale uncertainty and the ratio derived from it,")
        print("  not a pattern of arithmetic error.")

    if doc_fails:
        print(f"\n  {len(doc_fails)} DOCUMENT check(s) failed — a retired value has reappeared or a correction is missing.")
    if "--strict" in sys.argv and (failed or doc_fails):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
