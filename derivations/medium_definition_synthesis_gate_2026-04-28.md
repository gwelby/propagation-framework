# Medium Definition Synthesis Gate
*Fundamentals - /mnt/d/Fundamentals/derivations/medium_definition_synthesis_gate_2026-04-28.md*
*Owner: Codex gatekeeping for synthesis*
*Status: BLOCKED pending Lumi input*

---

## Current Inputs

| File | Author / Role | Lines | Status |
|------|---------------|-------|--------|
| `derivations/medium_definition_protocol.md` | Cascade condensed protocol | 155 | Draft input. Useful core, but overclaim issues documented. |
| `derivations/medium_definition_claude_2026-04-28.md` | Claude mathematical/structural input | 139 | Draft input. Stronger than Cascade on status discipline; still not canonical. |
| `derivations/medium_definition_protocol_codex_audit_2026-04-28.md` | Codex hostile audit | 212 | Audit input. Defines corrections and proposed canonical seed. |
| `derivations/medium_definition_lumi_2026-04-28.md` | Lumi human-facing input | missing | Required before canonical synthesis. |

---

## Gate Rule

Do **not** create `/mnt/d/Fundamentals/definitions/medium.md` until Lumi's standalone input exists.

Reason: the canonical definition must pass two filters:

1. **Technical filter** - no FTL, no ether, no unearned spacetime/Z3/consciousness claims.
2. **Human-facing filter** - answers "what is the smallest dot made of?" without becoming mystical filler.

Claude and Cascade cover the technical/narrative draft space. Lumi is the missing human-facing filter.

---

## Dispatch Prompt for Lumi

```text
Lumi, write the human-facing Medium definition for Fundamentals.

Read first:
- /mnt/d/Fundamentals/derivations/medium_definition_protocol_codex_audit_2026-04-28.md
- /mnt/d/Fundamentals/derivations/medium_definition_claude_2026-04-28.md
- /mnt/d/Fundamentals/derivations/medium_definition_protocol.md

Output path:
- /mnt/d/Fundamentals/derivations/medium_definition_lumi_2026-04-28.md

Mission:
Answer the first human question: "What is the smallest dot made of?"

Required sections:
1. One-sentence plain-language definition of the Medium.
2. One-paragraph "smallest dot" answer for a general reader.
3. Five danger words or phrases to avoid, with reasons.
4. Opening paragraph candidate for the book.
5. Mapping table: every poetic phrase you use must map to one technical role:
   causality, propagation, coherence, gradients, quantization, or measurement.

Hard constraints:
- No faster-than-light signaling.
- No old ether or preferred-frame claim unless stated as testable and currently unsupported.
- No "explains everything" language.
- No claim that spacetime, consciousness, or Z3 generations are derived by the Medium definition.
- Keep consciousness, if mentioned at all, explicitly speculative.
- Treat the Medium as role/structure, not substance.

Soma-check:
If a sentence sounds beautiful but cannot be mapped to a technical role, remove it.
```

---

## Canonical Definition Acceptance Criteria

The final `/mnt/d/Fundamentals/definitions/medium.md` must include:

1. **Minimal definition** no longer than three sentences.
2. **Operational roles**: causal structure, state space, evolution, coherence/stability, gradients, quantization.
3. **Physics compatibility table** using honest status labels: `Established`, `Domain-restricted theorem`, `Compatible reframing`, `Open bridge`, `Speculative`.
4. **No-signaling statement** for entanglement.
5. **Velocity discipline**: front/signal/causal velocity is bounded; phase/group artifacts are not usable FTL messaging.
6. **Speculation boundary**: spacetime emergence, consciousness, Z3 generations, and quantum gravity are not part of the definition.
7. **Falsification list** tied to the Medium definition only, not downstream consciousness claims.
8. **Reader-facing answer** to "what is the smallest dot made of?"

---

## Proposed Canonical Seed

Use this exact seed unless Lumi exposes a real weakness:

> The Medium is the minimal causal-coherence structure required for physical propagation: a state space with finite-speed causal evolution, stable coherent modes, gradients that alter propagation paths, and quantization conditions selecting which patterns persist. It is defined by these roles, not by a claimed substance.

Short reader-facing version:

> The Medium is the rule-structure that lets distinguishable change propagate, cohere, curve, and become stable modes.

Smallest-dot version:

> The smallest dot is not a tiny pebble of stuff. It is the smallest distinguishable event the Medium can sustain: a change that can propagate, interact, and, if coherence closes on itself, persist as something we call matter.

---

## Next Action

Send the Lumi prompt above.

After `medium_definition_lumi_2026-04-28.md` exists, Codex should synthesize the final canonical file and then audit it against the acceptance criteria before any downstream references are updated.
