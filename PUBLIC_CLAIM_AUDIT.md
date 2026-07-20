# PUBLIC CLAIM AUDIT
**Date**: 2026-07-17 · **Auditor**: Hermes · **Source**: `CLAIMS.md` (2026-07-02)  
**Target**: Align all public-facing narrative assets with current claim states.

---

## Claim State Changes Since April 2026

### God Equation — SPLIT
- **Old (pre-June 16):** "God Equation DERIVED" — one row, seven approaches, 52.7x decisive
- **New:** Two separate rows:
  - **Postulate-D Z₃ operator algebra: CONDITIONAL 0.88** — eigenvalues {1, −1/8, −1/8} exact given explicit Postulate D, which is NOT derived from Axioms 1-3
  - **λ_c scale formula: ARGUED 0.60** — N^(D/2) is fit-selected, H_prod not derived, "seven approaches converged" withdrawn
- **Impact on public narrative:** Never say "God Equation verified." Say "The Z₃ algebra closes exactly under an explicit postulate; the scale formula is a candidate, not a derivation."

### Weinberg Angle — DEMOTED
- **Old:** DERIVED
- **New:** ARGUED 0.65 — Casimir algebra is a real candidate, not a proved derivation. Look-elsewhere scan: P(random hit) ≈ 0.46.
- **Impact:** Never say "derived." Say "a candidate explanation with a striking algebraic match."

### Fine Structure Constant α — DEMOTED to OPEN
- **Old:** Numeric derivation claimed (0.061% error)
- **New:** OPEN — Casimir combination withdrawn as confidence-bearing. No derivation from Axioms 1-3 exists.
- **Impact:** Do not claim α is derived. The structural identification (α = Z₀/2R_K) remains ARGUED 0.60.

### CP Violation Bridge — ADDED
- **New:** ARGUED 0.70 — PF's N=3 structural derivation implies CP violation exists (one complex CKM phase). Does NOT derive phase magnitude.
- **Impact:** Can say "If N=3 is structurally required, CP violation must exist." Do not claim magnitude.

### Lean-Verified Results — ADDED (June 29-30)
- D=3 is the unique stable dimension for J-I dynamics: CONDITIONAL 0.85
- Degenerate residue forces J-I circulant: CONDITIONAL 0.85
- D=3 symmetric + zero diagonal + equal row sums → J-I: CONDITIONAL 0.85
- D≥4 gap: same premises do not force J-I: CONDITIONAL (negative) 0.85
- PFEntropy decreases under T³: CONDITIONAL 0.85
- Full-norm Pythagorean decomposition: DERIVED 0.95
- Isometry-JI incompatibility: CONDITIONAL 0.85
- Impact: These are machine-certified by Lean 4 kernel. Can say "Lean-verified" for these specific conditional results. Do not say "the framework is Lean-verified" broadly.

---

## Per-Asset Audit

### 1. `movie/VOICEOVER_SCRIPT.md`
- **God Equation references:** Replace all "derived" with "follows from an explicit postulate"
- **"Now we know why" (Three Generations):** BLOCKED — soften to "The geometry suggests a reason"
- **"Seven approaches converged":** WITHDRAWN — remove entirely
- **Fine Structure Constant:** Remove any "we derived α" language
- **Missing:** Add ε₀/μ₀ bridge — the video audience learns c = 1/√(ε₀μ₀), our framework asks "why those values?"

### 2. `movie/NOTEBOOKLM_BRIDGE_BRIEF.md`
- Update claim tiers to match current CLAIMS.md
- Add ε₀/μ₀ entry point

### 3. `movie/HUMAN_ENTRY_MAP.md`
- Verify all entry points reflect current claim states
- Add "fourth door" pedagogical entry point

### 4. `sandbox/explorer/index.html`
- Opening still reads "YOUR MODEL OF REALITY IS WRONG" — BLOCK, needs humbler tone
- Three Generations → mark CONDITIONAL

---

## Public Language Discipline

| Old Phrase | Replacement |
|-----------|-------------|
| "We derived X" | "The framework predicts X under [condition]" |
| "Now we know why" | "The geometry suggests a reason" |
| "Seven approaches converged" | WITHDRAWN — do not use |
| "God Equation verified" | "Z₃ algebra closes under an explicit postulate" |
| "52.7x decisive" | WITHDRAWN — do not use |
| "The framework proves" | "The framework supports" or "Lean-verified under premises" |

---

*Source: `CLAIMS.md` v0.3 (2026-07-02). This audit reflects the current scoreboard, not April's.*
