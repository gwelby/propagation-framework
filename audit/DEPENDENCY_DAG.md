# Dependency DAG & Floor-Rule Audit

**Date:** 2026-06-16
**Auditor:** Claude (Opus 4.8)
**Rule under test (the "floor rule"):** *a derived result cannot be graded more confident than its least-confident premise.* Confidence(claim) ≤ min over parents of Confidence(parent). Any `DERIVED` node with an `OPEN` / `POSTULATED` / `CONDITIONAL` parent is a **floor violation**.

Parent confidences are taken from the framework's own files (`CLAIMS.md`, `axioms.md`, the derivation files). Where a file and `CLAIMS.md` disagree, both are shown.

---

## The DAG (physics section)

```
AXIOMS 1-3  (non-quantitative; constrain no number)
   │
   ├── Axiom 3b "Minimal Winding"  [OPEN: "Does 3b follow from Axiom 3? OPEN" — axioms.md]
   │        │
   │        └──> WEINBERG ANGLE  ......................... CLAIMS: DERIVED 0.90
   │                 parents:
   │                   • Casimir polynomial choice ......... ARGUED (3 hand-picked constraints + f1=1)
   │                   • spin pair (1/2, 1) ................. CHOSEN (best of a dense menu; see look-elsewhere)
   │                   • R ≡ sin2_W identification .......... ASSUMED
   │                   • scheme = on-shell ................. OPEN (misses MS-bar by 0.008)
   │                   • Axiom 3b .......................... OPEN
   │                 source file g3_casimir_weinberg_angle.md self-rates: ARGUED 0.65
   │                 HONEST CEILING = min(parents) ≈ 0.65 (ARGUED), not 0.90
   │
   ├── Three Generations  ............................... CLAIMS: CONDITIONAL 0.85
   │        parents:
   │          • T1 numerator (physical (2,1) weight) ...... CONDITIONAL 0.85, needs A_NR [OPEN]
   │          • T2 denominator (M=3) .................... NOT CLOSED ("does not close M=3 from PF axioms alone")
   │        (correctly graded CONDITIONAL — this node is honest)
   │        │
   │        └──(used as an INPUT, at "0.985", inside)──┐
   │                                                   │
   ├── D = 3  [confidence 0.60, "knot stability argument" — lambda_c file]   │
   │                                                   │
   ├── Postulate D  [POSTULATED 2026-05-31; "not derived from Axioms 1-3 alone" — G3_CLOSURE] │
   │                                                   │
   ├── N^{D/2} spatial-closure bridge  [NOT PROVEN — lambda_c file line 89] │
   │                                                   ▼
   └────────────────────────────────────> GOD EQUATION (λ_c)  ... CLAIMS: DERIVED 0.90
                  parents & self-ratings (all from lambda_c_from_axioms.md):
                    • core hypothesis "as stated" ........ 0.05   ← the killer
                    • overall ............................ 0.75 ARGUED
                    • N=3 input .......................... cited 0.985, but CLAIMS rates it 0.85 CONDITIONAL
                    • D=3 input .......................... 0.60
                    • N^{D/2} bridge ..................... NOT PROVEN
                    • Postulate D ........................ POSTULATED
                  HONEST CEILING = min(parents) ≈ 0.05–0.60, NOT 0.90


KOIDE Q = 2/3  ......................................... CLAIMS: DERIVED 0.95
   parents:
     • parameterization sqrt(m_n)=A+R cos(...) .......... EXACT IDENTITY (true)
     • equal-amplitude premise (A_e=A_mu=A_tau) ......... ARGUED (from shared EM coupling)
     • vacuum selects equal-norm point .................. OPEN ("Not Yet Derived" — section 4, all 3 routes conjectural)
   HONEST CEILING = EXACT IDENTITY (geometry) + OPEN (physical selection); the 0.95 covers only the identity


(2,1) TOPOLOGICAL WEIGHTS — kernel obstruction ........ CLAIMS: DERIVED 0.95
   parent: SU(2)->SO(3) double cover, kernel {+-1} ...... TEXTBOOK MATH (true, 0 sorrys verified)
   HONEST: solid parent — but it is standard group theory, not PF-specific.
(2,1) TOPOLOGICAL WEIGHTS — physical realization ...... CLAIMS: CONDITIONAL 0.85
   parent: A_NR non-redundancy hypothesis .............. OPEN
   (correctly graded CONDITIONAL — honest)


GRAVITY AS OPTICAL GEOMETRY ........................... CLAIMS: DERIVED 0.95
   parent: optical/Randers metric for null geodesics ... TEXTBOOK PHYSICS (true)
   HONEST: solid — but imported, not derived from Axioms 1-3.
```

---

## Floor-rule violation ledger

| DERIVED claim | Weakest parent | Parent status | Published | Honest ceiling | Violation? |
|---|---|---|---|---|---|
| **God Equation λ_c** | core hypothesis / N^{D/2} bridge | **0.05 / NOT PROVEN** | 0.90 | **≤ 0.60** | **YES — severe (up to 18×)** |
| **Weinberg angle** | Axiom 3b + scheme | **OPEN** | 0.90 | **≤ 0.65** | **YES** |
| **Koide Q=2/3** | vacuum selection | **OPEN** | 0.95 | identity only | **YES (label)** |
| Topological kernel | double cover | TEXTBOOK | 0.95 | 0.95 | no (but not novel) |
| Topological physical | A_NR | OPEN | 0.85 (COND) | 0.85 | no (honest) |
| Gravity optics | optical metric | TEXTBOOK | 0.95 | 0.95 | no (but not novel) |
| Three Generations | T2 (M=3) | NOT CLOSED | 0.85 (COND) | 0.85 | no (honest) |

**Pattern:** the two nodes with *solid* parents (gravity optics, topological kernel) are **textbook results imported into PF** — true but not novel. The two nodes graded honestly (three generations, topological physical) are the **CONDITIONAL** ones. Every node that is *both* graded `DERIVED` *and* claims novelty (God Equation, Weinberg, Koide-selection) **violates the floor rule.**

This is not a coincidence — it is the signature of the identity-laundering pipeline: novelty and `DERIVED` status are inversely correlated with parent solidity.

---

## Concrete recommendation: automate this

Add a `depends_on:` field to every row in `CLAIMS.md` and a CI check that recomputes `min(parent confidence)` and flags any row published above its floor. ~30 lines of Python. This would have caught the God Equation 0.90 the day it was written. The repo already has the discipline (`public_claim_guard.py`); extend it to enforce the floor.
