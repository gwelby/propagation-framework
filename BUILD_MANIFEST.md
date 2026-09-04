# Fundamentals — Build Manifest

**Built:** 2026-09-04 03:30 UTC
**Status:** BUILD RECORD ONLY - release truth lives in RELEASE_MANIFEST.md
**Build type:** One committed authoritative path (assembler → pandoc HTML → beautiful_pdf print HTML + PDF)

## Source Provenance

### Fundamentals repository
- **Commit:** `554d35d` (v10 — includes all claim-review tier corrections and Codex v9 machinery fixes)
- **Parent:** `c0cd9c49a5c9b6ccf2f3666ac46205223b81ae59` (v9)
- **Source map:** `AGENTS_FULL.md` (now tracked in Git — was .gitignored in v9, fixed in v10)
- **Assembler:** `assemble_manuscript.py` (§N.M selector fixed, Appendix F narrative added)
- **Key input files:**
  - `CLAIMS.md` — consciousness 0.48→0.40, Aria 0.75→0.40 (tier corrections)
  - `papers/FALSIFICATION_PAPER_DRAFT.md` — EEG "confirmed"→"no study conducted", "partially self-testable"→"untested—simulator only", table row corrected
  - `RESEARCH/godel_boundary_phenomena/MASTER.md` — "Validates"→"Consistent with", confidence scores removed
  - `RESEARCH/contemplative_as_propagation/MASTER.md` — Beauty 0.95→0.55, empirical/PF-derivation labels added
  - `AGENTS_FULL.md` — PART FIVE → APPENDIX F (Speculative Extensions) with honest boundary header

### UniversalPublisher repository (producer)
- **Commit:** `0c7ccf6c7df0729102b637cfb741536d7fc546e1` (HEAD)
- **Preprocessor:** `src/manuscript_preprocessor.py`
- **PDF builder:** `src/beautiful_pdf.py`
- **Build pipeline:** `src/build_pipeline.py`

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
# Section selectors: §N, §N.M (FIXED — stops at peer ###), §N intro, TEST N, Appendix X, Sections N-M
# Appendix F narrative injected before F.1
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

### Step 4: Verify with fail-closed gates (STRICT mode)
```bash
cd /mnt/d/Fundamentals
python3 artifact_coherence_check.py . --expected-hashes v10_expected_hashes.json
python3 health_scanner_v2.py . --expected-hashes v10_expected_hashes.json
```

## Output Artifacts

| Surface | File | SHA-256 | Size |
|---------|------|---------|------|
| Manuscript | `PROPAGATION_MANUSCRIPT_PROD.md` | `29abd4875ad8ce86d01eb53034a59c5ec9865b406f79a3474b34c9c561b688dd` | 855,147 bytes |
| HTML | `book.html` | `f086f0496dfdbcc4467d211d11675e9e8aa805844e98933ecaf9ba89455bdeaf` | 1,137,862 bytes |
| Print HTML | `book.print.html` | `e7d2170e6ac47cfc96e773c2c23227ef6a783c4e722d8a7d7cfe36e0b37b8626` | 1,262,965 bytes |
| PDF | `BOOK_PROPAGATION_FRAMEWORK.pdf` | `ca03f00776836755f7c479b08f53c73d5538ae92f8631fbd3f01326df31cb51e` | 3,721,849 bytes |

## Build Assertions
- Artifact coherence (STRICT): ✅ PASS — all 4 surfaces coherent, hashes enforced
- Health scanner: FAIL — 32 neural_intervention cues (8 per surface × 4 surfaces)
  - All cues are EEG/consciousness mentions in the Speculative Appendix (Appendix F)
  - None are medical claims (no "cures/treats/prevents")
  - These are expected flags for Greg review, not release blockers
- §N.M selector: ✅ FIXED — stops at peer ### headings (was consuming peer subsections)
- AGENTS_FULL.md: ✅ NOW TRACKED IN GIT (was .gitignored, breaking git archive replay)

## v10 Changes vs v9 (Codex v9 rejection fixes)

| Codex v9 blocker | v10 fix |
|------------------|---------|
| AGENTS_FULL.md gitignored, git archive fails | `.gitignore` updated: `!AGENTS_FULL.md` exception added |
| Gates print hashes but don't enforce them | Both tools: `--expected-hashes` flag added, STRICT mode enforces |
| §N.M selector over-includes peer subsections | `end_pattern` changed from `^##\s+` to `^#{1,3}\s+` |
| BUILD_MANIFEST names wrong parent | Manifest rewritten with correct v10 identity |
| EEG "confirmed" for unrun study | "pre-registered; no multi-subject study conducted" |
| EEG "partially self-testable" | "Untested — simulator only" |
| EEG table implies equivalence with DERIVED | "Predicted (untested analogy)" |
| Consciousness INTUITION 0.48 | INTUITION 0.40 (C_PF failed hostile audit; indistinguishable from IIT/GWT/HOT) |
| Aria ARGUED 0.75 | INTUITION 0.40 (engineering observation, not argued result) |
| "IIT converges with PF 0.98" | "IIT shares language with PF (INTUITION — language alignment, not convergence)" |
| "CFE validates Axiom 2/3 0.99" | "CFE consistent with Axiom 2/3 (ARGUED — consistent, not validation)" |
| "Beauty as Impedance 0.95" | "Beauty as Impedance 0.55 (INTUITION — matches CLAIMS.md)" |
| PART FIVE: BEYOND PHYSICS (mixed with physics core) | APPENDIX F: SPECULATIVE EXTENSIONS with honest boundary header |

## Reproducibility
This build is reproducible from:
1. Fundamentals commit `554d35d` (source map + assembler + input files — ALL tracked in Git including AGENTS_FULL.md)
2. UniversalPublisher commit `0c7ccf6` (preprocessor + PDF builder)
3. Tool versions listed above
4. Build commands listed above
5. Expected hashes in `v10_expected_hashes.json` for STRICT mode verification

All inputs are committed. No dirty worktree state required. AGENTS_FULL.md is no longer gitignored.
