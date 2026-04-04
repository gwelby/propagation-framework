# T3 - Three Generations: Close N=3 once T1 and T2 are derived

## What This Is

**Frontier**: Three Generations `N=3` - `CONDITIONAL 0.85`  
**Current state**: blocked by unresolved T1 and T2 theorem gaps  
**Owning sources**:
- `CLAIMS.md`
- `derivations/three_generations_closed_proof.md`
- `derivations/three_generations_t2_audit_2026-03-28.md`
- `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`
- `derivations/t2_denominator_theorem_audit_2026-03-31.md`

This file tracks the T3 assembly work after the March 31 bounded audits.
The algebra is already exact.
The prerequisites are not.

So the current implementation target is:

> write the clean assembly proof now, keep T3 conditional, and avoid any status upgrade language until T1 and T2 actually close.

---

## Current Truth

Today the repo truth order says:

- T1 / numerator route: `PARTIAL DERIVATION 0.85`
- T2 / denominator route: `PARTIAL DERIVATION 0.85`
- T3 / Three Generations: `CONDITIONAL 0.85`

That means this ticket is still blocked as a full theorem-closing pass.
It is **not** blocked as preparatory implementation work.

---

## Implemented In This Pass

1. Added `derivations/three_generations_closed_proof.md` as the exact conditional assembly theorem.
2. Synchronized summary wording so T3 is not described as fully derived while T1 and T2 remain open.
3. Left the claim status unchanged at `CONDITIONAL 0.85`.

---

## Conditional Algebraic Chain

```
T1 (not yet closed): PF must physically realize closure weights (2,1)
    -> numerator of Q(N) = 2N/(2N+M) is 2N

T2 (not yet closed): PF must derive M = 3 from native 3D defect structure
    -> denominator of Q(N) = 2N/(2N+M) is 3

Koide Q = 2/3 (DERIVED 0.95): geometric theorem, independent of T1/T2

Then:
2N/(2N+3) = 2/3 -> 4N+6 = 6N -> N = 3
```

There is no hidden algebraic step beyond those inputs.
The uncertainty is entirely in the T1 and T2 bridges.

---

## Promotion Gate

T3 may upgrade only if:

- T1 receives a Codex audit that upgrades the physical `(2,1)` numerator theorem
- T2 receives a Codex audit that upgrades the denominator theorem `M = 3`
- the assembly file is re-audited to confirm no new hidden step was introduced
- the owning status docs are synchronized in truth order

Until then, the correct wording is:

> Three Generations is a conditional theorem with exact algebra and two named unresolved prerequisite bridges.

---

## Acceptance Criteria

- [x] `derivations/three_generations_closed_proof.md` exists and cites the live T1/T2 audits
- [x] Repo summary language no longer overstates T3 as fully derived
- [ ] T1 is upgraded to DERIVED by Codex audit
- [ ] T2 is upgraded to DERIVED by Codex audit
- [ ] Codex audits the final assembly theorem after the prerequisites close
- [ ] `CLAIMS.md` is promoted only after those prerequisite audits exist
