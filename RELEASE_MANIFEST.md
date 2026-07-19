# Fundamentals — Release Manifest

## Canonical surface
- **Source:** `PROPAGATION_MANUSCRIPT_PROD.md` — SHA-256: `98d660ff69852fd10d179e14e8963c71e27fa0a1d9177f8773f803ed8b68b368`
- **HTML:** `book.html` — SHA-256: `94fa5f2311362d30a86e384f68f93f9888289b1f9523414d6cac871d58f93b71`
- **HTML Print:** `book.print.html` — SHA-256: `045cafa3d18259cc38e916c528f4a7627c7989daf4516a1f3a70135d6f7ff673`
- **PDF:** `BOOK_PROPAGATION_FRAMEWORK.pdf` — SHA-256: `9b86e7cc2bc46759b35aa0541aa4ffe361c252e37e7ac76729619649925145b3`

## Release gates
| Gate | Status | Owner |
|---|---|---|
| Content build | PASS (49/49 intended entries) | AntiGravity |
| Claim audit | HOLD — Codex v6 re-audit (2026-07-14) | Codex |
| Legal | ⏳ PENDING | Legal |
| Greg approval | ⏳ PENDING | Greg |

## Boundaries
No public or buyer-facing release is permitted. The current artifact hashes
identify the v7 build; they do not certify its medical safety or release readiness.

Governing verdict:
`/mnt/d/Codex/REPORTS/CODEX_20260714_FUNDAMENTALS_V6_MEDICAL_RELEASE_REAUDIT.md`.
Required route: bound the source map, exclude or qualify Appendix E through
the required human review, rebuild all artifacts, rerun claim/health/visual
gates, then obtain separate Codex, Legal, and Greg decisions.
