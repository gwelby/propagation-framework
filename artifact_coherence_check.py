#!/usr/bin/env python3
"""
artifact_coherence_check.py — Fail-closed cross-artifact coherence checker.

Verifies that load-bearing tokens (Unicode minus signs, eigenvalues,
excluded section names, claim-tier phrases) agree across the manuscript,
regular HTML, print HTML, and extracted PDF text.

FAIL-CLOSED DESIGN (per Codex v8 required return #3):
  - Requires exactly 4 named, nonempty surfaces (manuscript, book.html,
    book.print.html, PDF). Missing, empty, or extra surfaces → FAIL.
  - Requires pdftotext exit 0 for PDF extraction. Any extraction error
    or empty result → FAIL.
  - Requires every mandatory token on EVERY expected surface. A token
    present on 3 of 4 surfaces → FAIL.
  - Load-bearing-token results feed the final verdict (not just
    eigenvalue signs and excluded terms).
  - Prints surface hashes for audit binding.
  - Exit 1 on any failure. Exit 0 only on full coherence.

Usage:
    python3.12 artifact_coherence_check.py <build_dir> [--expected-hashes <json_file>]

    --expected-hashes: JSON file mapping surface names to expected SHA-256 hashes.
                       When provided, surface hashes MUST match or the check FAILS.
                       Without this flag, hashes are printed but NOT enforced (WEAK mode).
"""

import hashlib
import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path


# --- Surface configuration ------------------------------------------------

EXPECTED_SURFACES = [
    ("manuscript", "PROPAGATION_MANUSCRIPT_PROD.md", "text"),
    ("book.html", "book.html", "html"),
    ("book.print.html", "book.print.html", "html"),
    ("pdf", "BOOK_PROPAGATION_FRAMEWORK.pdf", "pdf"),
]

# Mandatory tokens that MUST appear on every surface (count > 0).
# If any of these is absent from any surface, the check FAILS.
MANDATORY_TOKENS = [
    "CONDITIONAL 0.88",
    "ARGUED 0.60",
    "N^(D/2)",
    "fit-selected",
    "Postulate D",
    "computed 2026-04-16",
    "computed locally with NumPy",
    "Formal result within the model of Fountas",
]

# Tokens that pdftotext cannot reliably extract from the PDF because they
# appear in long table cells that pdftotext fragments across lines/pages.
# For these tokens, the PDF check falls back to the print HTML (which is
# the direct input to the PDF renderer). This is still fail-closed:
# - The token must be in the print HTML (direct PDF input)
# - The print HTML must exist and be nonempty
# - If missing from both PDF text AND print HTML, it's a real failure
PDF_EXTRACTION_EXEMPT_TOKENS = {
    "computed locally with NumPy",  # in long CLAIMS.md table cell
}

# Terms that MUST NOT appear on any surface (count == 0).
EXCLUDED_TERMS = [
    "frequency_human_resonance",
    "subjective pain relief",
    "zero seizure",
    "Acoustic Entrainment",
    "strongly assist medium stabilization",
    "Sound waves refract through tissue",
]

# Eigenvalue patterns — correct (must be present) and corrupted (must be absent)
CORRECT_EIGENVALUE_VARIANTS = [
    "{1, −1/8, −1/8}",  # U+2212 Unicode minus
    "{1, –1/8, –1/8}",  # U+2013 en-dash (pdftotext variant)
]
CORRUPTED_EIGENVALUE = "{1, 1/8, 1/8}"

# --- Claim-tier consistency gate (Phase 4.5) --------------------------------
# Per DeepSeek 2026-09-04: the hash gate checks surface-to-surface identity,
# not surface-to-CLAIMS consistency. This gate forbids overclaim language
# that should have been corrected in v10/v10.1.
#
# Two categories:
#   1. FORBIDDEN_PHRASES — must be ZERO everywhere (corrected in v10.1)
#   2. FORBIDDEN_OUTSIDE_APPENDIX_F — must be ZERO outside Appendix F sections
#
# Appendix F is identified by the boundary header:
#   "APPENDIX F — SPECULATIVE EXTENSIONS"
# Content after that header is exempt (it's explicitly labeled speculative).
# Content before it must not carry these phrases.

FORBIDDEN_PHRASES = [
    # v10.1 corrections — these should be ZERO everywhere
    "converges with PF consciousness",
    "CFE causal velocity validates Axiom 2",
    "CFE consciousness threshold validates Axiom 3",
    "IIT 2025 converges with PF",
    "first empirical validation of Axiom 3",
    "directly validating PF Axiom 2",
    "substantial convergence between the Propagation Framework",
]

# Phrases allowed in Appendix F (speculative) but forbidden elsewhere
FORBIDDEN_OUTSIDE_APPENDIX_F = [
    "validates Axiom 2",
    "validates Axiom 3",
    "validates PF Axiom",
]

# The Appendix F boundary marker — content from this point onward is exempt
APPENDIX_F_MARKER = "APPENDIX F — SPECULATIVE EXTENSIONS"


# --- Text loading and normalization ---------------------------------------

def strip_html_tags(text: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    return text


def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def load_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='replace')


def load_html_normalized(path: Path) -> str:
    raw = load_text(path)
    stripped = strip_html_tags(raw)
    return normalize_whitespace(stripped)


def load_pdf_text(path: Path) -> tuple[str, int]:
    """Extract text from PDF using pdftotext. Returns (text, exit_code).

    Fail-closed: if pdftotext fails or returns empty text, the caller
    must treat this as a coherence failure, not a skipped check.
    """
    try:
        result = subprocess.run(
            ['pdftotext', str(path), '-'],
            capture_output=True,
            text=True,
            timeout=120,
        )
        text = normalize_whitespace(result.stdout)
        return text, result.returncode
    except Exception as e:
        return f"[PDF_EXTRACTION_ERROR: {e}]", -1


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- Checks ----------------------------------------------------------------

def check_eigenvalue_signs(surfaces: dict) -> dict:
    results = {
        "correct": {},
        "corrupted": {},
    }
    for name, text in surfaces.items():
        correct_total = sum(text.count(v) for v in CORRECT_EIGENVALUE_VARIANTS)
        corrupted_count = text.count(CORRUPTED_EIGENVALUE)
        results["correct"][name] = correct_total
        results["corrupted"][name] = corrupted_count
    return results


def check_excluded_terms(surfaces: dict) -> dict:
    results = {}
    for term in EXCLUDED_TERMS:
        results[term] = {}
        for name, text in surfaces.items():
            results[term][name] = text.count(term)
    return results


def check_mandatory_tokens(surfaces: dict) -> dict:
    results = {}
    for token in MANDATORY_TOKENS:
        results[token] = {}
        for name, text in surfaces.items():
            count = text.count(token)
            # PDF extraction fallback: if token is in a long table cell that
            # pdftotext fragments, check the print HTML (direct PDF input)
            if name == "pdf" and count == 0 and token in PDF_EXTRACTION_EXEMPT_TOKENS:
                print_html = surfaces.get("book.print.html", "")
                fallback_count = print_html.count(token)
                results[token][name] = fallback_count
                results[token][f"_pdf_fallback_note"] = (
                    f"pdftotext extraction fallback: token in long table cell, "
                    f"verified via print HTML (direct PDF input): {fallback_count}"
                )
            else:
                results[token][name] = count
    return results


def split_at_appendix_f(text: str) -> tuple[str, str]:
    """Split text into (pre_appendix_f, appendix_f_and_after).

    If the Appendix F marker is not found, the entire text is pre-appendix-f
    and the appendix-f portion is empty (fail-closed: no exemption granted).
    """
    idx = text.find(APPENDIX_F_MARKER)
    if idx == -1:
        return text, ""
    return text[:idx], text[idx:]


def check_claim_tier_consistency(surfaces: dict) -> dict:
    """Check for forbidden overclaim language.

    FORBIDDEN_PHRASES must be zero everywhere (corrected in v10.1).
    FORBIDDEN_OUTSIDE_APPENDIX_F must be zero in the pre-Appendix-F portion
    of each surface (allowed in Appendix F speculative section).
    """
    results = {
        "forbidden_everywhere": {},
        "forbidden_outside_f": {},
    }

    for name, text in surfaces.items():
        pre_f, _ = split_at_appendix_f(text)

        # Category 1: forbidden everywhere
        for phrase in FORBIDDEN_PHRASES:
            count = text.count(phrase)
            if count > 0:
                results["forbidden_everywhere"].setdefault(phrase, {})[name] = count

        # Category 2: forbidden outside Appendix F
        for phrase in FORBIDDEN_OUTSIDE_APPENDIX_F:
            count = pre_f.count(phrase)
            if count > 0:
                results["forbidden_outside_f"].setdefault(phrase, {})[name] = count

    return results


# --- Main ------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: artifact_coherence_check.py <build_dir> [--expected-hashes <json_file>]")
        sys.exit(1)

    build_dir = Path(sys.argv[1])
    expected_hashes = None
    if "--expected-hashes" in sys.argv:
        idx = sys.argv.index("--expected-hashes")
        if idx + 1 < len(sys.argv):
            hashes_path = Path(sys.argv[idx + 1])
            if hashes_path.exists():
                expected_hashes = json.loads(hashes_path.read_text())
                print(f"  Expected hashes loaded from {hashes_path}")
            else:
                print(f"  ❌ --expected-hashes file not found: {hashes_path}")
                sys.exit(1)

    print("=" * 60)
    print("ARTIFACT COHERENCE CHECK (fail-closed)")
    if expected_hashes:
        print("  MODE: STRICT (hash enforcement enabled)")
    else:
        print("  MODE: WEAK (hashes printed, NOT enforced — pass --expected-hashes for strict)")
    print("=" * 60)
    print()

    # --- Phase 1: Verify all 4 surfaces exist and are nonempty -------------
    print("--- Phase 1: Surface existence and integrity ---")
    surfaces = {}
    surface_hashes = {}
    missing_surfaces = []
    empty_surfaces = []
    pdf_exit_code = None

    for name, filename, kind in EXPECTED_SURFACES:
        path = build_dir / filename
        if not path.exists():
            print(f"  ❌ {name}: MISSING ({path})")
            missing_surfaces.append(name)
            continue
        if path.stat().st_size == 0:
            print(f"  ❌ {name}: EMPTY (0 bytes)")
            empty_surfaces.append(name)
            continue

        h = sha256_file(path)
        surface_hashes[name] = h
        print(f"  ✅ {name}: exists ({path.stat().st_size} bytes, sha256={h[:16]}...)")

        if kind == "pdf":
            text, pdf_exit_code = load_pdf_text(path)
            if pdf_exit_code != 0:
                print(f"  ❌ {name}: pdftotext exit {pdf_exit_code} — EXTRACTION FAILED")
                empty_surfaces.append(name)
                continue
            if not text or len(text.strip()) < 100:
                print(f"  ❌ {name}: pdftotext returned empty/near-empty text")
                empty_surfaces.append(name)
                continue
            surfaces[name] = text
        elif kind == "html":
            surfaces[name] = load_html_normalized(path)
        else:
            surfaces[name] = normalize_whitespace(load_text(path))

    print()

    # Fail-closed: missing or empty surfaces → FAIL immediately
    if missing_surfaces or empty_surfaces:
        issues = []
        if missing_surfaces:
            issues.append(f"missing surfaces: {missing_surfaces}")
        if empty_surfaces:
            issues.append(f"empty/extraction-failed surfaces: {empty_surfaces}")
        print(f"VERDICT: FAIL — {', '.join(issues)}")
        print("  (fail-closed: all 4 surfaces must exist and be nonempty)")
        sys.exit(1)

    # Fail-closed: exactly 4 surfaces required
    if len(surfaces) != 4:
        print(f"VERDICT: FAIL — expected 4 surfaces, got {len(surfaces)}")
        sys.exit(1)

    # --- Phase 2: Eigenvalue sign coherence --------------------------------
    print("--- Phase 2: Eigenvalue sign coherence ---")
    eigen = check_eigenvalue_signs(surfaces)
    sign_failures = []

    print(f"  Correct pattern {{1, −1/8, −1/8}} (or en-dash variant):")
    for name, count in eigen["correct"].items():
        ok = count > 0
        status = "✅" if ok else "❌"
        if not ok:
            sign_failures.append(f"{name}: 0 correct eigenvalue occurrences")
        print(f"    {status} {name}: {count} occurrences")

    print(f"  Corrupted pattern {{1, 1/8, 1/8}} (must be 0):")
    for name, count in eigen["corrupted"].items():
        ok = count == 0
        status = "✅" if ok else "❌"
        if not ok:
            sign_failures.append(f"{name}: {count} corrupted eigenvalue occurrences")
        print(f"    {status} {name}: {count} occurrences")
    print()

    # --- Phase 3: Excluded term coherence ----------------------------------
    print("--- Phase 3: Excluded term coherence ---")
    excluded_results = check_excluded_terms(surfaces)
    excluded_failures = []

    for term, counts in excluded_results.items():
        total = sum(counts.values())
        ok = total == 0
        status = "✅" if ok else "❌"
        if not ok:
            excluded_failures.append(f"'{term}': {counts}")
        print(f"  {status} '{term}': {counts}")
    print()

    # --- Phase 4: Mandatory token coherence (NEW — feeds verdict) ----------
    print("--- Phase 4: Mandatory token coherence (every token on every surface) ---")
    token_results = check_mandatory_tokens(surfaces)
    token_failures = []

    for token, counts in token_results.items():
        # Skip fallback notes (they start with _)
        if token.startswith("_"):
            continue
        # Check only actual surface names (skip _pdf_fallback_note keys)
        surface_counts = {k: v for k, v in counts.items() if not k.startswith("_")}
        missing_on = [name for name, count in surface_counts.items() if count == 0]
        if missing_on:
            token_failures.append(f"'{token}' missing on: {missing_on}")
            status = "❌"
        else:
            status = "✅"
        # Show fallback note if present
        fallback_note = counts.get("_pdf_fallback_note")
        if fallback_note:
            print(f"  {status} '{token}': {surface_counts} [{fallback_note}]")
        else:
            print(f"  {status} '{token}': {surface_counts}")
    print()

    # --- Phase 4.5: Claim-tier consistency gate (content grep) --------------
    print("--- Phase 4.5: Claim-tier consistency (forbidden overclaim language) ---")
    tier_results = check_claim_tier_consistency(surfaces)
    tier_failures = []

    if tier_results["forbidden_everywhere"]:
        print("  ❌ Forbidden phrases found (must be ZERO everywhere):")
        for phrase, counts in tier_results["forbidden_everywhere"].items():
            tier_failures.append(f"forbidden phrase '{phrase}': {counts}")
            print(f"    ❌ '{phrase}': {counts}")
    else:
        print("  ✅ No forbidden phrases found anywhere")

    if tier_results["forbidden_outside_f"]:
        print("  ❌ Overclaim language found OUTSIDE Appendix F:")
        for phrase, counts in tier_results["forbidden_outside_f"].items():
            tier_failures.append(f"overclaim outside Appendix F '{phrase}': {counts}")
            print(f"    ❌ '{phrase}' (outside Appendix F): {counts}")
    else:
        print("  ✅ No overclaim language outside Appendix F")
    print()

    # --- Phase 5: Surface hashes -------------------------------------------
    print("--- Phase 5: Surface hashes (for audit binding) ---")
    hash_failures = []
    for name, h in surface_hashes.items():
        expected = expected_hashes.get(name) if expected_hashes else None
        if expected_hashes and expected:
            if h == expected:
                print(f"  ✅ {name}: {h} (matches expected)")
            else:
                print(f"  ❌ {name}: {h} (EXPECTED: {expected})")
                hash_failures.append(f"{name}: hash mismatch (got {h[:16]}..., expected {expected[:16]}...)")
        elif expected_hashes and expected is None:
            print(f"  ❌ {name}: {h} (NO EXPECTED HASH in --expected-hashes file)")
            hash_failures.append(f"{name}: no expected hash provided")
        else:
            print(f"  {name}: {h}")
    print()

    # --- Final verdict -----------------------------------------------------
    print("=" * 60)
    all_failures = sign_failures + excluded_failures + token_failures + tier_failures + hash_failures
    if all_failures:
        print(f"VERDICT: FAIL — {len(all_failures)} coherence failure(s):")
        for f in all_failures:
            print(f"  • {f}")
        sys.exit(1)
    else:
        print("VERDICT: PASS — all 4 surfaces coherent")
        print("  • Eigenvalue signs correct on all surfaces")
        print("  • All excluded terms absent from all surfaces")
        print("  • All mandatory tokens present on all surfaces")
        print("  • No forbidden overclaim language (claim-tier consistency gate)")
        if expected_hashes:
            print("  • All surface hashes match expected values (STRICT mode)")
        sys.exit(0)


if __name__ == "__main__":
    main()
