#!/usr/bin/env python3
"""
health_scanner_v2.py — Fail-closed whitespace-normalized health-content scanner.

Scans all release surfaces (manuscript, regular HTML, print HTML, PDF)
using whitespace-normalized rendered text. This catches HTML-wrapped
phrases that the old line-by-line scanner missed.

FAIL-CLOSED DESIGN (per Codex v8 required return #3):
  - Requires exactly 4 named, nonempty surfaces (manuscript, book.html,
    book.print.html, PDF). Missing, empty, or extraction-failed → FAIL.
  - Requires pdftotext exit 0 for PDF extraction. Any extraction error
    or empty result → FAIL.
  - Prints surface hashes for audit binding.
  - Exit 1 on any health cue finding OR any surface integrity failure.
  - Exit 0 only on 0 findings across all 4 surfaces.

Usage:
    python3.12 health_scanner_v2.py <build_dir> [--expected-hashes <json_file>]

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


# --- Health cue patterns --------------------------------------------------

HEALTH_CUES = {
    "medical_outcome": [
        r"zero\s+seizure",
        r"seizure[-\s]free",
        r"pain\s+relief",
        r"remission",
        r"cures?\s+(?:for|of)\s+(?:seizures?|diseases?|epilepsy)",
        r"eliminates?\s+seizures?",
        r"seizure\s+elimination",
    ],
    "neural_intervention": [
        r"neural\s+entrainment",
        r"brainwave\s+entrainment",
        r"neurofeedback",
        r"EEG\s+(?:phase|entrainment|intervention)",
    ],
    "frequency_intervention": [
        r"40\s*Hz\s+(?:sensory|audio|therapy|treatment|entrainment|intervention)",
        r"432\s*Hz\s+(?:therapy|treatment|healing|repair)",
        r"acoustic\s+entrainment",
        r"vibration\s+stabilization",
        r"sound\s+waves\s+refract\s+through\s+tissue",
    ],
    "personal_seizure_outcome": [
        r"Greg\s+(?:observed|reported|experienced)\s+.*seizure",
        r"zero\s+seizure\s+events?",
    ],
    "excluded_section": [
        r"frequency_human_resonance",
        r"subjective\s+pain\s+relief",
        r"strongly\s+assist\s+medium\s+stabilization",
    ],
}


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

    Fail-closed: caller must check exit_code and treat non-zero as failure.
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


# --- Scanning --------------------------------------------------------------

def scan_surface(text: str) -> dict:
    results = {}
    for category, patterns in HEALTH_CUES.items():
        matches = []
        for pattern in patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 40)
                context = text[start:end]
                matches.append({
                    "pattern": pattern,
                    "match": m.group(),
                    "context": context,
                })
        results[category] = matches
    return results


# --- Main ------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: health_scanner_v2.py <build_dir> [--expected-hashes <json_file>]")
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
    print("HEALTH SCANNER v2 (fail-closed, whitespace-normalized)")
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

    # --- Phase 2: Scan all surfaces ----------------------------------------
    print("--- Phase 2: Health cue scan ---")
    all_results = {}
    total_findings = 0

    for name, text in surfaces.items():
        scan = scan_surface(text)
        all_results[name] = scan

        surface_total = sum(len(v) for v in scan.values())
        total_findings += surface_total

        print(f"\n  --- {name} ---")
        if surface_total == 0:
            print("    ✅ CLEAN — 0 health cues found")
        else:
            for category, matches in scan.items():
                if matches:
                    print(f"    ❌ {category}: {len(matches)} matches")
                    for m in matches[:3]:
                        print(f"       pattern: {m['pattern']}")
                        print(f"       match:   {m['match']}")
                        print(f"       context: ...{m['context']}...")
                    if len(matches) > 3:
                        print(f"       ... and {len(matches) - 3} more")

    print()

    # --- Phase 3: Surface hashes -------------------------------------------
    print("--- Phase 3: Surface hashes (for audit binding) ---")
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
    if total_findings == 0 and not hash_failures:
        print("VERDICT: PASS — 0 health cues across all 4 surfaces")
        if expected_hashes:
            print("  • All surface hashes match expected values (STRICT mode)")
        sys.exit(0)
    elif hash_failures and total_findings == 0:
        print(f"VERDICT: FAIL — {len(hash_failures)} hash mismatch(es) (STRICT mode)")
        for f in hash_failures:
            print(f"  • {f}")
        sys.exit(1)
    else:
        print(f"VERDICT: FAIL — {total_findings} health cues found across {len(surfaces)} surfaces")
        if hash_failures:
            print(f"  AND {len(hash_failures)} hash mismatch(es)")
            for f in hash_failures:
                print(f"  • {f}")
        # Per-surface breakdown
        for name, scan in all_results.items():
            surface_total = sum(len(v) for v in scan.values())
            if surface_total > 0:
                cats = ", ".join(f"{k}: {len(v)}" for k, v in scan.items() if v)
                print(f"  • {name}: {surface_total} ({cats})")
        sys.exit(1)


if __name__ == "__main__":
    main()
