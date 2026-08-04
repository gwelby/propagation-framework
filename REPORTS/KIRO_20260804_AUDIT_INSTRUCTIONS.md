# Kiro GPT-5.6 Sol Audit Instructions

Greg — to run the third parallel audit using Kiro with GPT-5.6 Sol:

## Setup

1. Open Kiro IDE
2. Select model: **GPT-5.6 Sol** (or whatever the strongest available model is)
3. Open the workspace: `/mnt/d/Fundamentals`

## Audit Prompt

Copy-paste this into Kiro:

```
You are the third independent auditor for a Lean 4 formalization project.
A Codex audit found HOLD issues. Repairs were applied. DeepSeek and Devin
have also audited. You are the tiebreaker.

Read these files:
- /mnt/d/Fundamentals/lean/PfLean/BekensteinBound.lean
- /mnt/d/Fundamentals/lean/PfLean/ChainRule.lean
- /mnt/d/Fundamentals/CLAIMS.md (rows 73-86 only)
- /mnt/d/Codex/REPORTS/CODEX_20260804_FUNDAMENTALS_BEKENSTEIN_CHAINRULE_AUDIT.md (the original audit)

For each of the 14 CLAIMS.md rows (lines 73-86), assess:
1. Is the tier (DERIVED/ARGUED/OPEN) honest?
2. Is the confidence score appropriate?
3. Does the Lean theorem actually prove what the row claims?
4. Are there hidden assumptions?

Specifically check:
- Does bekenstein_bound_algebraic derive the bound, or assume hS as input?
- Is bekenstein_saturation_def vacuous (rfl)?
- Do the parameter instantiation theorems prove M.causal_velocity IS vacuum c?
- Does ChainRule.lean derive Hawking temperature from PF axioms, or from imported GR?
- Is "G NOT derivable" a formal no-go theorem or just a survey of failed routes?

Build verification:
cd /mnt/d/Fundamentals/lean && lake build PfLean

Provide your verdict:
- PASS / HOLD / FAIL for each of the 14 rows
- Overall verdict
- Any remaining overclaims
- Whether the 11 Codex repairs were correctly applied

Write your report to: /mnt/d/Fundamentals/REPORTS/KIRO_20260804_BEKENSTEIN_REAUDIT.md
```

## Why Three Auditors?

Codex credits are exhausted until Aug 6. We need trusted redundancy:
- **Codex** (GPT-5.6 Sol): original audit, HOLD verdict — the gold standard
- **DeepSeek v4-pro**: independent reasoning engine, different model family
- **Devin** (GLM-5.2): self-audit, build verification, claim-by-claim review
- **Kiro GPT-5.6 Sol**: same model family as Codex, can run the same protocol

If 3 of 4 agree, we have convergence. If they disagree, we know there's
something worth looking at more carefully.

## Status

- [x] Codex: HOLD (original audit, 11 repairs demanded)
- [x] Devin: PASS (self-audit, all 14 rows honestly tiered)
- [ ] DeepSeek: running (codewhale exec, v4-pro)
- [ ] Kiro: waiting for Greg to run manually
