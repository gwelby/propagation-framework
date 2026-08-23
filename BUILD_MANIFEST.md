# Fundamentals — Build Manifest

**Built:** 2026-08-23 13:39 UTC
**Status:** BUILD RECORD ONLY - release truth lives in RELEASE_MANIFEST.md
**Build type:** One committed authoritative path (assembler → pandoc HTML → beautiful_pdf print HTML + PDF)

## Source Provenance

### Fundamentals repository
- **Commit:** `eab649024772b4bf07d391c65dd5edb3b0785ddd` (Fundamentals HEAD)
- **Source map:** `AGENTS_FULL.md` (49 entries, sha256 `0cb8cf47...`)
- **Assembler:** `assemble_manuscript.py` (sha256 `b8851f0b...`)
- **Key input files:**
  - `CLAIMS.md` — sha256 `89fe8634...`
  - `papers/FALSIFICATION_PAPER_DRAFT.md` — sha256 `30e41c90...`

### UniversalPublisher repository (producer)
- **Commit:** `5173e201ba45ae51b1b5c4454ee7a9c76754e63a` (HEAD, includes U+2212 fix)
- **Preprocessor:** `src/manuscript_preprocessor.py` (sha256 at HEAD `322e9380...`)
- **PDF builder:** `src/beautiful_pdf.py` (sha256 at HEAD `dc59d22b...`)
- **Build pipeline:** `src/build_pipeline.py` (sha256 at HEAD `a2b5ecfe...`)

### Tool versions
- Python 3.12.3
- pandoc 3.1.3
- pdftotext 24.02.0 (poppler-utils)
- playwright 1.58.0

## Build Commands

### Step 1: Assemble manuscript from source map
```bash
cd /mnt/d/Fundamentals
python3 assemble_manuscript.py
# Output: PROPAGATION_MANUSCRIPT_PROD.md
# Section selectors implemented: §N, §N.M, §N intro, TEST N, Appendix X, Sections N-M
# Duplicate-content control: content fingerprinting across entries
```

### Step 2: Build HTML via pandoc
```bash
cd /mnt/d/Projects/UniversalPublisher
python3 -c "
from src.build_pipeline import build_html_artifact
from src.capability_probe import probe_publishing_capabilities
build_html_artifact('BOOK_PROPAGATION_FRAMEWORK',
    Path('/mnt/d/Fundamentals'), Path('/mnt/d/Fundamentals'),
    [], probe_publishing_capabilities(),
    manuscript_path=Path('/mnt/d/Fundamentals/PROPAGATION_MANUSCRIPT_PROD.md'))
"
# Output: BOOK_PROPAGATION_FRAMEWORK/html/book.html → copied to book.html
```

### Step 3: Build print HTML + PDF via beautiful_pdf (Playwright)
```bash
cd /mnt/d/Projects/UniversalPublisher
python3 -c "
from src.beautiful_pdf import build_beautiful_pdf
build_beautiful_pdf(
    project_id='BOOK_PROPAGATION_FRAMEWORK',
    manuscript=Path('/mnt/d/Fundamentals/PROPAGATION_MANUSCRIPT_PROD.md'),
    output_file=Path('/mnt/d/Fundamentals/BOOK_PROPAGATION_FRAMEWORK.pdf'),
    metadata={'title': 'The Propagation Framework', 'author': '', 'language': 'en', 'has_toc': True},
    css_path=None,
    conversion_profile='generic-legacy@1')
"
# Output: BOOK_PROPAGATION_FRAMEWORK.pdf + book.print.html (sidecar)
```

## Output Artifacts

| Surface | File | SHA-256 | Size |
|---------|------|---------|------|
| Manuscript | `PROPAGATION_MANUSCRIPT_PROD.md` | `b026f4179a31822c82476a513f7450e03e1013481790bf333fb855ebe2583f98` | 918,015 bytes |
| HTML | `book.html` | `ab16bd6f5bd1aa1d488384fae40dd6278ee4d5077d4f47aa61fa74e6901c1f76` | 1,227,083 bytes |
| Print HTML | `book.print.html` | `7382b59bc0a14188de239ebf1ed829f3d886bd8ba30863d814555e204970cde7` | 1,365,096 bytes |
| PDF | `BOOK_PROPAGATION_FRAMEWORK.pdf` | `1e2879a4cb4383ca8c56f82a0b7d72f10655530eb08a0bedb67a0846282cb12e` | 4,622,548 bytes |

## Build Assertions
- HTML Leak Check: ✅ PASS
- book.html: ✅ PASS (zero literal leaks)
- book.print.html: ✅ PASS (zero literal leaks)
- Section extraction: ✅ PASS (selectors implemented, no duplicates)
- Duplicate content: ✅ PASS (0 duplicate blocks detected)
- Manuscript size: 15,301 lines / 918,015 bytes (down from 19,041 / 1,297,631)
- EEG test row count: 2 (down from 8 — section extraction working)

## Reproducibility
This build is reproducible from:
1. Fundamentals commit `eab6490` (source map + assembler + input files)
2. UniversalPublisher commit `5173e20` (preprocessor + PDF builder)
3. Tool versions listed above
4. Build commands listed above

All inputs are committed. No dirty worktree state required.
