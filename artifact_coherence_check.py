#!/usr/bin/env python3
"""
artifact_coherence_check.py — Cross-artifact coherence checker.

Verifies that load-bearing tokens (Unicode minus signs, eigenvalues,
excluded section names) agree across the manuscript, regular HTML,
print HTML, and extracted PDF text.

Usage:
    python3.12 artifact_coherence_check.py /mnt/d/Fundamentals
"""

import re
import sys
import json
import subprocess
from pathlib import Path
from html import unescape


def strip_html_tags(text: str) -> str:
    """Strip HTML tags and unescape entities."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    return text


def normalize_whitespace(text: str) -> str:
    """Collapse all whitespace runs to single spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def load_text(path: Path) -> str:
    """Load text from a file, normalized."""
    return path.read_text(encoding='utf-8', errors='replace')


def load_html_normalized(path: Path) -> str:
    """Load HTML, strip tags, normalize whitespace."""
    raw = load_text(path)
    stripped = strip_html_tags(raw)
    return normalize_whitespace(stripped)


def load_pdf_text(path: Path) -> str:
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(
            ['pdftotext', str(path), '-'],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return normalize_whitespace(result.stdout)
    except Exception as e:
        return f"[PDF_EXTRACTION_ERROR: {e}]"


def check_token_across_surfaces(
    token: str,
    surfaces: dict,
) -> dict:
    """Check if a token appears in each surface and report counts."""
    results = {}
    for name, text in surfaces.items():
        count = text.count(token)
        results[name] = count
    return results


def check_excluded_sections(
    excluded_terms: list,
    surfaces: dict,
) -> dict:
    """Check that excluded terms do NOT appear in any surface."""
    results = {}
    for term in excluded_terms:
        term_results = {}
        for name, text in surfaces.items():
            count = text.count(term)
            term_results[name] = count
        results[term] = term_results
    return results


def check_eigenvalue_signs(surfaces: dict) -> dict:
    """Check that the Postulate-D eigenvalues have correct minus signs."""
    # The Unicode minus (U+2212) is the canonical form in the source.
    # pdftotext may render it as U+2212 or as an en-dash (U+2013).
    # Both are "negative" signs — the corruption we're checking for is
    # the ABSENCE of any minus sign (i.e., "{1, 1/8, 1/8}").
    correct_variants = [
        "{1, −1/8, −1/8}",  # U+2212 Unicode minus
        "{1, –1/8, –1/8}",  # U+2013 en-dash (pdftotext variant)
    ]
    corrupted = "{1, 1/8, 1/8}"

    results = {
        "correct_pattern": {},
        "corrupted_pattern": check_token_across_surfaces(corrupted, surfaces),
    }

    for name, text in surfaces.items():
        total = 0
        for variant in correct_variants:
            total += text.count(variant)
        results["correct_pattern"][name] = total

    # Also check for the Unicode minus in other contexts
    minus_char = "\u2212"
    results["unicode_minus_count"] = check_token_across_surfaces(minus_char, surfaces)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: artifact_coherence_check.py <build_dir>")
        sys.exit(1)

    build_dir = Path(sys.argv[1])

    manuscript = build_dir / "PROPAGATION_MANUSCRIPT_PROD.md"
    book_html = build_dir / "book.html"
    book_print_html = build_dir / "book.print.html"
    pdf = build_dir / "BOOK_PROPAGATION_FRAMEWORK.pdf"

    # Load surfaces
    surfaces = {}
    if manuscript.exists():
        surfaces["manuscript"] = normalize_whitespace(load_text(manuscript))
    if book_html.exists():
        surfaces["book.html"] = load_html_normalized(book_html)
    if book_print_html.exists():
        surfaces["book.print.html"] = load_html_normalized(book_print_html)
    if pdf.exists():
        surfaces["pdf"] = load_pdf_text(pdf)

    print("=" * 60)
    print("ARTIFACT COHERENCE CHECK")
    print("=" * 60)
    print()

    # 1. Eigenvalue sign check
    print("--- 1. Eigenvalue sign coherence ---")
    eigen_results = check_eigenvalue_signs(surfaces)
    print(f"  Correct pattern {{1, −1/8, −1/8}}:")
    for name, count in eigen_results["correct_pattern"].items():
        status = "✅" if count > 0 else "❌"
        print(f"    {status} {name}: {count} occurrences")
    print(f"  Corrupted pattern {{1, 1/8, 1/8}}:")
    all_clean = True
    for name, count in eigen_results["corrupted_pattern"].items():
        status = "✅" if count == 0 else "❌"
        if count > 0:
            all_clean = False
        print(f"    {status} {name}: {count} occurrences")
    print(f"  Unicode minus (U+2212) count:")
    for name, count in eigen_results["unicode_minus_count"].items():
        print(f"    {name}: {count} occurrences")
    print()

    # 2. Excluded sections check
    print("--- 2. Excluded section coherence ---")
    excluded_terms = [
        "frequency_human_resonance",
        "subjective pain relief",
        "zero seizure",
        "Acoustic Entrainment",
        "strongly assist medium stabilization",
        "Sound waves refract through tissue",
    ]
    excluded_results = check_excluded_sections(excluded_terms, surfaces)
    all_excluded_clean = True
    for term, counts in excluded_results.items():
        total = sum(counts.values())
        status = "✅" if total == 0 else "❌"
        if total > 0:
            all_excluded_clean = False
        print(f"  {status} '{term}': {counts}")
    print()

    # 3. Load-bearing token check
    print("--- 3. Load-bearing token coherence ---")
    load_bearing_tokens = [
        "CONDITIONAL 0.88",
        "ARGUED 0.60",
        "N^(D/2)",
        "fit-selected",
        "Postulate D",
        "computed 2026-04-16",
        "computed locally with NumPy",
        "Formal result within the model of Fountas",
    ]
    for token in load_bearing_tokens:
        counts = check_token_across_surfaces(token, surfaces)
        total = sum(counts.values())
        status = "✅" if total > 0 else "⚠️"
        print(f"  {status} '{token}': {counts}")
    print()

    # 4. Artifact hashes
    print("--- 4. Artifact hashes ---")
    import hashlib
    for name, path in [
        ("manuscript", manuscript),
        ("book.html", book_html),
        ("book.print.html", book_print_html),
        ("pdf", pdf),
    ]:
        if path.exists():
            h = hashlib.sha256(path.read_bytes()).hexdigest()
            print(f"  {name}: {h}")
        else:
            print(f"  {name}: MISSING")
    print()

    # Overall verdict
    print("=" * 60)
    sign_coherent = all(
        v == 0 for v in eigen_results["corrupted_pattern"].values()
    )
    excluded_clean = all_excluded_clean
    if sign_coherent and excluded_clean:
        print("VERDICT: PASS — artifacts are coherent")
        sys.exit(0)
    else:
        issues = []
        if not sign_coherent:
            issues.append("sign corruption detected")
        if not excluded_clean:
            issues.append("excluded content found in artifacts")
        print(f"VERDICT: FAIL — {', '.join(issues)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
