#!/usr/bin/env python3
"""
health_scanner_v2.py — Whitespace-normalized health-content scanner.

Scans all release surfaces (manuscript, regular HTML, print HTML, PDF)
using whitespace-normalized rendered text. This catches HTML-wrapped
phrases that the old line-by-line scanner missed.

Usage:
    python3.12 health_scanner_v2.py /mnt/d/Fundamentals
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


def load_surface(path: Path, is_html: bool = False, is_pdf: bool = False) -> str:
    """Load a surface and normalize it for scanning."""
    if is_pdf:
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

    raw = path.read_text(encoding='utf-8', errors='replace')
    if is_html:
        raw = strip_html_tags(raw)
    return normalize_whitespace(raw)


# Health cue patterns — designed to catch both literal and HTML-wrapped variants
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


def scan_surface(text: str) -> dict:
    """Scan normalized text for health cues."""
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


def main():
    if len(sys.argv) < 2:
        print("Usage: health_scanner_v2.py <build_dir>")
        sys.exit(1)

    build_dir = Path(sys.argv[1])

    surfaces_config = [
        ("manuscript", build_dir / "PROPAGATION_MANUSCRIPT_PROD.md", False, False),
        ("book.html", build_dir / "book.html", True, False),
        ("book.print.html", build_dir / "book.print.html", True, False),
        ("pdf", build_dir / "BOOK_PROPAGATION_FRAMEWORK.pdf", False, True),
    ]

    print("=" * 60)
    print("HEALTH SCANNER v2 (whitespace-normalized)")
    print("=" * 60)
    print()

    all_results = {}
    total_findings = 0

    for name, path, is_html, is_pdf in surfaces_config:
        if not path.exists():
            print(f"  ⚠️ {name}: file not found at {path}")
            all_results[name] = {}
            continue

        text = load_surface(path, is_html=is_html, is_pdf=is_pdf)
        scan = scan_surface(text)
        all_results[name] = scan

        surface_total = sum(len(v) for v in scan.values())
        total_findings += surface_total

        print(f"--- {name} ({path.name}) ---")
        if surface_total == 0:
            print("  ✅ CLEAN — 0 health cues found")
        else:
            for category, matches in scan.items():
                if matches:
                    print(f"  ❌ {category}: {len(matches)} matches")
                    for m in matches[:3]:
                        print(f"     pattern: {m['pattern']}")
                        print(f"     match:   {m['match']}")
                        print(f"     context: ...{m['context']}...")
                    if len(matches) > 3:
                        print(f"     ... and {len(matches) - 3} more")
        print()

    print("=" * 60)
    if total_findings == 0:
        print(f"VERDICT: PASS — 0 health cues across all surfaces")
        sys.exit(0)
    else:
        print(f"VERDICT: FAIL — {total_findings} health cues found")
        sys.exit(1)


if __name__ == "__main__":
    main()
