# Proposed `CLAIMS.md` Diff — Ready to Review

**Date:** 2026-06-16
**Author:** Claude (Opus 4.8) — **PROPOSED, NOT APPLIED.** Demotions are the board's call (Codex's role). This is a precise find/replace patch so the change is one reviewed commit, not a rewrite.
**Basis:** `audit/PROPOSED_CLAIMS_HONEST.md` + the five audit notes. Every change moves a grade *down to where the source file already sits* — no new physics.

Apply order: header block first, then the five rows. Each block is exact `FIND` → `REPLACE`.

---

## EDIT 1 — Header status line (CLAIMS.md:4)

**FIND:**
> **God Equation upgraded to DERIVED (with Postulate D) on 2026-05-31; Codex reconciliation sign-off recorded 2026-06-06**: primitive Z₃ no-self-loop selector forces U = M/2 uniquely; eigenvalues {1, −1/8, −1/8} exact. Seven approaches converged; Greg approved Postulate D.

**REPLACE:**
> **God Equation: CONDITIONAL (with Postulate D).** The Z₃ selector U = M/2 follows *only* once a=0 is adopted as Postulate D (not derived from Axioms 1-3). The "seven approaches converged" support was found overstated on 2026-06-16 (`audit/POSTULATE_D_PROBE_AUDIT.md`): ≥3 of the 7 cannot discriminate a=0, and the eigenvalue match is target-loaded. The "decisive 52.7× decoherence" is an endpoint artifact whose own script self-rates CONDITIONAL 0.88 (`audit/DECOHERENCE_PROBE_AUDIT.md`).

---

## EDIT 2 — Weinberg Angle row (CLAIMS.md:52)

**FIND (status + confidence cells):**
> **Weinberg Angle (sin²θ_W)** | **DERIVED** | … | 0.90 |

**REPLACE:**
> **Weinberg Angle (sin²θ_W)** | **ARGUED** | [unchanged evidence text] **Audit 2026-06-16:** derivation file self-rates ARGUED 0.65; the value matches the on-shell scheme and misses MS̄(M_Z)=0.23122 by 0.008; trials factor ≈0.46 (`audit/LOOK_ELSEWHERE_RESULTS.md`). Provenance: de Vries 2004 / Rivero. | 0.65 |

---

## EDIT 3 — God Equation row (CLAIMS.md:57)

**FIND (status + confidence cells):**
> **λ_c from l_P (The God Equation)** | **DERIVED (with Postulate D)** | … | 0.90 |

**REPLACE:**
> **λ_c from l_P (The God Equation)** | **CONDITIONAL** | [keep evidence text, but add] **Audit 2026-06-16:** "no fitting parameters" is not accurate — the exponent N^{D/2}=N^{1.5} is the exact-fit value (1.4997); the framework's own heat-kernel derivation gives N^1 (off by 10¹⁷). `lambda_c_from_axioms.md` self-rates the core hypothesis 0.05, overall 0.75, with the N^{D/2} bridge "not yet proven." Floor rule: confidence ≤ min(parents) = min(N=3 @0.85, D=3 @0.60, Postulate D, bridge) ⇒ ≤0.60. | 0.60 |

---

## EDIT 4 — Koide Law row (CLAIMS.md:43)

**FIND (status cell):**
> **Koide Law for Charged Leptons (Q = 2/3)** | **DERIVED** |

**REPLACE:**
> **Koide Law for Charged Leptons (Q = 2/3)** | **EXACT IDENTITY (geometry) + OPEN (physical selection)** |

…and append to the evidence cell:
> **Audit 2026-06-16:** the 0.95 covers the algebraic identity `Q=2/3 ⟺ equal U(1)/SU(3) norm` only. `koide_geometric_equivalence.md` §4 states the physical selection of the equal-norm point is "Not Yet Derived" (3 conjectural routes). Provenance: Koide 1981, Foot 1994.

(Confidence: keep 0.95 *for the identity*; add OPEN for the selection.)

---

## EDIT 5 — Fine Structure Constant α row (CLAIMS.md:53)

**FIND (status + confidence cells):**
> **Fine Structure Constant α** | **ARGUED** | … | 0.35 (as derivation); 0.60 (as structural identification) |

**REPLACE:**
> **Fine Structure Constant α** | **OPEN** | `alpha_from_pf.md` concludes "FAILED — no derivation of 1/137.036 achieved." The `(1−x₁)·x_{3/2}²·(1−x₂)/π = 1/137.119` hit (0.06%) is a Casimir-root scan result the source file itself classifies as numerology; trials factor (`audit/LOOK_ELSEWHERE_RESULTS.md`) ≈0.46. Removed as a confidence-bearing claim. | OPEN |

---

## EDIT 6 — Lean wording (everywhere "machine-verified DERIVED" appears)

**FIND:** `machine-verified DERIVED claim` / `machine-certified` (in physics-claim context)
**REPLACE:** `algebraic content machine-checked in Lean 4`

Rationale: every Lean theorem (`WeinbergAngle`, `KoideGeometry`, `ThreeGenerations`, `GravityOptics`, `TopologicalWeights`) proves an algebraic identity or a standard group-theory fact, not the physical identification that carries the claim. True and still valuable — just not "verified physics."

---

## EDIT 7 — Add a Provenance line under the title

**ADD after the "Audit Agent" line:**
> **Provenance:** The core numerical relations predate this framework — Koide (1981), Foot (1994, `foot_1994.pdf` in repo), de Vries (Physics Forums 2004), Rivero (2005–6). PF reinterprets and extends them; it did not discover them.

---

## Net effect on the headline count

| Before | After |
|---|---|
| 4 DERIVED + God Equation DERIVED | 2 DERIVED (gravity optics, topo-kernel — both correct but imported) · 1 EXACT IDENTITY (Koide) · 1 EMPIRICAL anchor (δ≈2/9) · God Eq & Weinberg → CONDITIONAL/ARGUED · α → OPEN |

This is the scoreboard a hostile physicist cannot dismantle, because every cell now matches the file beneath it. **Reviewer (Codex): accept / amend / reject each edit with reasons.**
