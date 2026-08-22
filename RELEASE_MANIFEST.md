# Fundamentals — Release Manifest

## Canonical surface
- **Source:** `PROPAGATION_MANUSCRIPT_PROD.md` — SHA-256: `f2711d043470f34404b3675aed086fe2f35c78a41188a21b4a1cc402238c3291`
- **HTML:** `book.html` — SHA-256: `22ec736f2ac54f95c448cef2b49838567e80ebfd7979157fe35b048145428ac0`
- **HTML Print:** `book.print.html` — SHA-256: `309fc7b820fa17690667b02b24ac3d153ed269444ec52519a424fb1c752436ff`
- **PDF:** `BOOK_PROPAGATION_FRAMEWORK.pdf` — SHA-256: `b140bedd1db9e2debc5c2fde2a29af260987e2977fdc02e36bf213a587cd2bce`

## Release gates
| Gate | Status | Owner |
|---|---|---|
| Content build | ✅ PASS (49/49 entries; one coherent build from frozen source) | AntiGravity |
| Claim audit | ⛔ HOLD — Codex v8 re-audit pending | Codex |
| Forbidden phrases | ⛔ HOLD — pending v8 re-audit after source corrections | Devin / Codex |
| Legal | ⏳ PENDING | Legal |
| Greg approval | ⏳ PENDING | Greg |

## v7 Required return status (CODEX_20260822_V7_REAUDIT)
1. **Source phrase corrections** — ✅ DONE. "Verified numerical error" → "Computed relative difference"; "verified by local NumPy" → "computed locally with NumPy"; "no fitting parameters" removed; "verified 2026-04-16" → "computed 2026-04-16"; "Mathematical proof (Fountas, 2026)" → "Formal result within the model of Fountas et al. (2026)".
2. **One coherent rebuild** — ✅ DONE. All four surfaces rebuilt from one frozen source (PROPAGATION_MANUSCRIPT_PROD.md, 2026-08-22). No stale artifacts.
3. **Artifact-coherence check** — ✅ DONE. `artifact_coherence_check.py` verifies: eigenvalue signs agree across all surfaces (0 corrupted, 0 excluded sections, load-bearing tokens coherent).
4. **Health scanner fix** — ✅ DONE. `health_scanner_v2.py` uses whitespace-normalized rendered text across all surfaces. 0 medical_outcome, 0 personal_seizure_outcome, 0 frequency_intervention, 0 excluded_section. 42 neural_intervention (EEG in consciousness research — flagged for Codex/Greg review, not medical).
5. **Unicode minus fix** — ✅ DONE. Root cause: `manuscript_preprocessor.py` line 41 listed `−` (U+2212) as a "risky unicode" character. Removed from bad_chars list. All surfaces now preserve `−1/8` eigenvalues.
6. **Manifest truth** — ✅ DONE. Content build = ✅ PASS only after coherent build. Claim audit = HOLD. Forbidden phrases = HOLD.
7. **Legal and Greg separate** — ⏳ PENDING. Not inferred from build or scan results.

## Boundaries
No public or buyer-facing release is permitted. The current artifact hashes
identify the v8 build; they do not certify its medical safety or release readiness.

Governing verdict:
`/mnt/d/Codex/REPORTS/CODEX_20260822_FUNDAMENTALS_V7_RELEASE_CA7FD99_REAUDIT.md`.
Required route: Codex v8 re-audit of corrected source → Legal → Greg.
