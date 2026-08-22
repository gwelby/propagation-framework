# Fundamentals — Release Manifest

## Canonical surface
- **Source:** `PROPAGATION_MANUSCRIPT_PROD.md` — SHA-256: `98d660ff69852fd10d179e14e8963c71e27fa0a1d9177f8773f803ed8b68b368`
- **HTML:** `book.html` — SHA-256: `94fa5f2311362d30a86e384f68f93f9888289b1f9523414d6cac871d58f93b71`
- **HTML Print:** `book.print.html` — SHA-256: `fb10c3938f82a32f972671d383b8e59abdaf918aad88ff7e9fa3eeaee6103576`
- **PDF:** `BOOK_PROPAGATION_FRAMEWORK.pdf` — SHA-256: `60b77224013fc17032e267ef9dbde4241c4941b6c8328050c8b004801e03202b`

## Release gates
| Gate | Status | Owner |
|---|---|---|
| Content build | PASS (49/49 intended entries; parser boundary verified) | AntiGravity |
| Claim audit | HOLD — Codex v6 re-audit (2026-07-14); v7 re-audit packet pending | Codex |
| Forbidden phrases | FAIL — 22 matches (ibm_q_overclaim: 16, mathematical_proof_public_claim: 6) | Devin |
| Legal | ⏳ PENDING | Legal |
| Greg approval | ⏳ PENDING | Greg |

## v6 Required return status (CODEX_20260714)
1. **Parser boundary fix** — ✅ DONE. `parse_source_map()` stops at `# PART IV — AGENT PROTOCOLS`; 49 entries, no `derivations/*.md`, no `frequency_human_resonance`.
2. **Appendix E exclusion** — ✅ DONE. `frequency_human_resonance` excluded in `resolve_source()`. Health scan: 0 medical_outcome, 0 personal_seizure_outcome matches.
3. **Regenerate artifacts** — ⚠️ PARTIAL. Manuscript and book.html hashes match manifest; book.print.html and PDF were rebuilt but manifest was stale. Manifest now updated with current hashes.
4. **Correct manifest** — ✅ DONE. `Claim audit` says HOLD, not PASS. This row continues to tell the truth.
5. **Gate-shaped packet** — ⏳ PENDING. In progress.
6. **Legal and Greg separate** — ⏳ PENDING. Not inferred from build or scan results.

## Boundaries
No public or buyer-facing release is permitted. The current artifact hashes
identify the v7 build; they do not certify its medical safety or release readiness.

Governing verdict:
`/mnt/d/Codex/REPORTS/CODEX_20260714_FUNDAMENTALS_V6_MEDICAL_RELEASE_REAUDIT.md`.
Required route: bound the source map, exclude or qualify Appendix E through
the required human review, rebuild all artifacts, rerun claim/health/visual
gates, then obtain separate Codex, Legal, and Greg decisions.
