# Codex Audit — `data.claims.js`
*Date: 2026-05-06*
*Scope: `/mnt/d/Fundamentals/sandbox/explorer/data.claims.js` vs `/mnt/d/Fundamentals/CLAIMS.md` and `/mnt/d/Fundamentals/definitions/README.md`*

## Verdict

**MODIFY APPLIED — now acceptable as the Explorer copy/data layer seed.**

The file had the correct architecture: story/audit/math separation, status-driven color, definition copy, no-go routes, and scale anchors. It was not yet safe to wire directly because it promoted one noncanonical file and omitted several live CLAIMS rows.

## Findings

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| DCL-01 | Critical | `consciousness.md` was listed in the canonical definition lattice and `axioms.md` was missing. This contradicted `definitions/README.md`: 19 canonical definitions exclude consciousness and include axioms. | Replaced the consciousness definition entry with `axioms.md`; `DEFINITIONS.length` remains 19. Consciousness remains only as an INTUITION claim. |
| DCL-02 | High | Not every live CLAIMS.md scoreboard row was represented. `Beauty as Impedance`, `2/3 Efficiency Ratio`, and `Aria Self-Reference` were missing. | Added all three with exact statuses/confidences from CLAIMS.md. |
| DCL-03 | Medium | `STATUS.PARTIAL` displayed as `PARTIAL`, but CLAIMS.md says `PARTIAL DERIVATION`. | Changed label to `PARTIAL DERIVATION`. |
| DCL-04 | Medium | Several definition copy blocks compressed too aggressively and risked overclaiming: forces as geometry, field as Medium state, time as emergent, measurement as solved/inherited, coupling as just strength. | Rewritten to match canonical definitions more tightly. |
| DCL-05 | Medium | God Equation `derivedPart` said "the equation structure is derived", which was too strong while `H_prod` remains open. | Rewritten: IBM result strengthens chiral-sector model but does not prove `H_prod`, statistical independence, or full `λ_c` derivation. |
| DCL-06 | Low | IDs diverged from existing Explorer hyphen convention for `causal-velocity` and `minimum-substrate`. | Normalized IDs and dependencies to the existing convention. |

## Acceptance Check

Current imported counts:

```text
DEFINITIONS: 19
CLAIMS: 24
NOGOS: 6
DERIVED claims: gravity-optical, koide-leptons, weinberg-angle
```

The 24 CLAIMS rows match the live scoreboard after excluding the stale duplicate `U(3) Entropy Maximization` row and the separate `Hermes One-Shot Trigger Mechanism` appendix entry. `Bekenstein Bound` remains intentionally outside this file because it is UNSYNCED and not present as a CLAIMS.md scoreboard row.

## Remaining Integration Constraints

- Do not treat `data.claims.js` as the only truth source. It is an Explorer presentation layer derived from CLAIMS.md and canonical definitions.
- Keep existing deep links working when replacing the flat 12-panel nav.
- If AntiGravity adds a Definition Lattice, it must read `axioms` as canonical and `consciousness` as noncanonical/candidate.
- If Bekenstein is surfaced, it must be marked `UNSYNCED`, not `DERIVED`, until CLAIMS.md is updated.
