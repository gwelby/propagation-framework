# Fundamentals — Release Manifest

## Canonical surface
- **Source:** `PROPAGATION_MANUSCRIPT_PROD.md` — SHA-256: `b026f4179a31822c82476a513f7450e03e1013481790bf333fb855ebe2583f98`
- **HTML:** `book.html` — SHA-256: `ab16bd6f5bd1aa1d488384fae40dd6278ee4d5077d4f47aa61fa74e6901c1f76`
- **HTML Print:** `book.print.html` — SHA-256: `7382b59bc0a14188de239ebf1ed829f3d886bd8ba30863d814555e204970cde7`
- **PDF:** `BOOK_PROPAGATION_FRAMEWORK.pdf` — SHA-256: `1e2879a4cb4383ca8c56f82a0b7d72f10655530eb08a0bedb67a0846282cb12e`

## Release gates
| Gate | Status | Owner |
|---|---|---|
| Content build | ✅ PASS (49/49 entries; one coherent build from frozen source; section extraction implemented) | AntiGravity |
| Claim audit | ⛔ HOLD — Codex v9 re-audit pending (v8 returns addressed) | Codex |
| Forbidden phrases | ✅ PASS (6 IBM-rule hits allowlisted via hash-bound REVIEW context; PDF text scanned) | Devin / Codex |
| Legal | ⏳ PENDING | Legal |
| Greg approval | ⏳ PENDING | Greg |

## v8 Required return status (CODEX_20260822_V8_REAUDIT)
1. **Uncommitted producer fix** — ✅ DONE. U+2212 fix committed to UniversalPublisher as `5173e20`. Regression tests added to `tests/test_manuscript_preprocessor.py`.
2. **BUILD_MANIFEST binding** — ✅ DONE. `BUILD_MANIFEST.md` binds exact commits, input hashes, commands, tool versions, and output hashes for all 4 surfaces.
3. **Fail-closed safety tools** — ✅ DONE. `artifact_coherence_check.py` and `health_scanner_v2.py` both fail-closed: require 4 named nonempty hash-bound surfaces, pdftotext exit 0, mandatory tokens on every surface. Verified on empty directory (FAIL) and on real artifacts (PASS).
4. **Assembly duplication** — ✅ DONE. `assemble_manuscript.py` implements section extraction (§N, §N.M, TEST N, Appendix X, Sections N-M) with duplicate-content detection. EEG test row count reduced from 8 to 2. Manuscript size reduced from 1,297,631 to 918,015 bytes.
5. **EEG/biological/contemplative/AI-self claim review** — ⏳ PREPARED. Review list prepared for Greg approval (see Item 5 deliverable).
6. **Hash-bound REVIEW allowlist + PDF scan** — ✅ DONE. `fundamentals_ibm_review_allowlist.json` binds 6 IBM-rule hits to exact artifact hashes with normalized context. `codex_release_gate.py` updated with `--allowlist` option and PDF text extraction. Near-miss positive controls defined.
7. **One committed authoritative path** — ✅ DONE. All artifacts rebuilt through one path: assembler → pandoc HTML → beautiful_pdf print HTML + PDF. All gates rerun. Codex v9 packet prepared.

## Boundaries
No public or buyer-facing release is permitted. The current artifact hashes
identify the v9 build; they do not certify its medical safety or release readiness.

Governing verdict:
`/mnt/d/Codex/REPORTS/CODEX_20260822_FUNDAMENTALS_V7_RELEASE_CA7FD99_REAUDIT.md` (v8 re-audit).
Required route: Codex v9 re-audit of corrected source → Legal → Greg.
