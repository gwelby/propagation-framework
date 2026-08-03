# Wave Report: AUDIT-003 — First Cross-Workspace Audit (Money-Research)

**Wave ID:** AUDIT-003
**Date:** 2026-08-01
**Agent:** Devin (Cognition AI)
**Status:** GREEN — all proofs compile, full project builds clean

---

## What was built

`PfLean/MoneyResearchAudit.lean` (~590 lines) — the first cross-workspace application of the AuditProtocol.

### The port

26 claims from `Money-Research/CLAIMS/claims.ndjson` were ported to Lean `ClaimEntry` values:

| Tier mapping | Count | Description |
|-------------|-------|-------------|
| TIER 1 → EMPIRICAL | 14 | Verified historical/economic facts (mr001-013, mr016) |
| TIER 2 → ARGUED | 5 | Plausible, sourced reasoning (mr014, mr015, mr020-022) |
| TIER 3 → INTUITION | 3 | Conceptual, not validated (mr017, mr018, mr023) |
| UNVERIFIED → OPEN | 4 | Unsupported by evidence (mr019, mr024-026) |
| **Total** | **26** | |

Each claim includes:
- The claim text (in the evidence string, prefixed with "Source: ...")
- The source attribution
- A falsifier — the specific evidence that would disprove the claim
- Empty dependencies (all claims are independent)

### The audit certificate

**`moneyResearch_passes_full_audit`** — all 9 structural checks pass:

| Check | What it verifies | Result |
|-------|-----------------|--------|
| TierConsistency | Confidence in tier's range | PASS (by construction) |
| DependenciesResolved | All deps name real entries | PASS (vacuous — all deps empty) |
| UniqueEntryNames | No duplicate names | PASS (26 distinct IDs) |
| FalsifierNonEmpty | Every claim has falsifier | PASS (26/26) |
| EvidenceNonEmpty | Every claim has evidence | PASS (26/26) |
| StatusGateConsistency | No OK→HOLD/NOGO deps | PASS (all OK, vacuous) |
| NoSelfDependency | No entry deps on itself | PASS (vacuous) |
| NoCyclicDependencies | No 2-cycles | PASS (vacuous) |
| Acyclic | No cycles of any length | PASS (no edges in graph) |

### Tier distribution (machine-verified)

- `moneyResearch_empirical_count` = 14
- `moneyResearch_argued_count` = 5
- `moneyResearch_intuition_count` = 3
- `moneyResearch_open_count` = 4
- `moneyResearch_tier_counts_sum` = 26

---

## What the certificate says vs. doesn't say

**Says:**
- All 26 claims have non-empty falsifiers (they're testable)
- All 26 claims have non-empty evidence strings (they're sourced)
- All 26 names are unique (no confusion)
- All tiers are in their confidence ranges
- The dependency graph is acyclic (trivially — all independent)

**Does NOT say:**
- That the evidence strings semantically support the claims
- That the sources say what we attribute to them
- That the tier assignments are correct (e.g., that "Barter is rare" is truly EMPIRICAL)
- That the falsifiers are actually testable in practice

The semantic audit was done manually in `Money-Research/AUDIT_2026-08-01.md`. The Lean audit certifies the structure; the manual audit certified the semantics. Both were needed, and both passed.

---

## The honest limitation

These are empirical/historical claims, not mathematical theorems. The `P : Prop` for each entry is `True` (trivially proven), and the actual claim content lives in the evidence string. The Lean audit checks STRUCTURAL honesty — it does NOT check SEMANTIC honesty.

This is stated directly in the .lean file's doc comment (lines 7-12), not just in the report. The limitation is baked into the artifact.

---

## Build verification

```
lake build PfLean.MoneyResearchAudit  → GREEN (384s)
lake build                             → GREEN (16534 jobs, full project)
```

---

## Lines of code (cumulative across all waves)

| File | Lines | Theorems | Negative fixtures |
|------|-------|----------|-------------------|
| AuditProtocol.lean | ~780 | 7 | 5 |
| AuditRegistry.lean | ~470 | 17 | 0 |
| MoneyResearchAudit.lean | ~590 | 15 | 0 |
| **Total** | **~1,840** | **39** | **5** |

---

## Why this matters

This is the first time the AuditProtocol has been applied to a different workspace's claims. The protocol was designed for PF claims, but it's workspace-agnostic — any claim system that uses the ClaimLedger structure can be audited.

The Money-Research claims are fundamentally different from PF claims:
- PF claims are mathematical (proofs, theorems, group theory)
- Money-Research claims are empirical (history, economics, cryptography)

The audit doesn't care about the domain. It checks the structure. This is the same principle as a financial audit — the auditor doesn't need to understand the business, they need to verify the books are consistent.

---

## What the audit caught (and didn't catch)

The Money-Research claims were already manually audited on 2026-08-01. The manual audit found:
- 4 UNVERIFIED claims that were correctly flagged as unsupported
- 3 TIER 3 claims that were correctly flagged as conceptual
- No structural issues

The Lean audit confirms the manual audit's structural findings. It didn't catch anything new because the manual audit already fixed the structure. But now the structure is machine-verified — if someone adds a new claim with an empty falsifier or a circular dependency, the Lean audit will catch it.

---

## Next waves

**Wave 4: Port Gambling claims and formalize the 9-step Prediction Audit Protocol.**
The gambling workspace has its own audit protocol (the `prediction-audit` skill). Formalizing it as a Lean specialization of the AuditProtocol would give gambling predictions the same structural audit certificate.

**Wave 5: Soundness bridge.**
Connect each computable check to its propositional form: `runAudit_allPassed_implies_auditPasses`. The tier consistency direction is proven; the remaining directions require unfolding the computable check functions.

**Wave 6: Cross-workspace audit registry.**
A single Lean module that runs the audit on all workspaces (PF, Money-Research, Gambling) and produces a unified certificate. This would be the family-level audit artifact.
