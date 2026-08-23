# v9 Claim Review List for Greg — EEG / Biological / Contemplative / AI-Self

**Prepared:** 2026-08-23
**Purpose:** Codex v8 required return #5 — prepare EEG/biological/contemplative/AI-self claim review list for Greg approval before v9 re-audit submission.

## Summary

The health scanner v2 (fail-closed) found **40 health cues across 4 surfaces** (10 per surface), all in the `neural_intervention` category. This is down from Codex v8's 168 findings (the reduction is due to section extraction eliminating duplicated content). All 40 cues are the same 10 unique matches replicated across manuscript/HTML/print HTML/PDF.

The 10 unique matches fall into 3 claim categories that require Greg's review.

---

## Category 1: EEG Phase Transition Predictions (6 matches)

**Claim status in CLAIMS.md:** ARGUED / INTUITION (not DERIVED)
**Health scanner category:** neural_intervention

### Match 1: EEG phase transitions (table row)
- **Line:** 70, 6780
- **Context:** `| EEG phase transitions | Not addressed | Same mathematics as particle phase transitions |`
- **Claim:** The framework predicts EEG phase transitions using the same mathematics as particle phase transitions.
- **Status:** ARGUED — not empirically confirmed. The bridge between biological predictions and particle physics is "argued, not proved" (line 125).
- **Greg review question:** Is it safe to publish this as an ARGUED prediction (not a medical claim), or should it be removed/strengthened?

### Match 2: EEG phase transition pattern (preregistration)
- **Line:** 109, 6724
- **Context:** `3. **The EEG phase transition pattern**, pre-registered and confirmed in a multi-subject study (n ≥ 30).`
- **Claim:** The EEG phase transition pattern is pre-registered and needs confirmation in a multi-subject study (n ≥ 30).
- **Status:** This is a PREDICTION/preregistration, not a confirmed result. The n ≥ 30 study has NOT been conducted.
- **Greg review question:** Is the preregistration language clear enough that readers understand this is a prediction, not a result?

### Match 3: TEST 1 — EEG phase transition
- **Line:** 6612
- **Context:** `| TEST 1 — EEG phase transition | Partially self-testable | Local simulator runs; real-data analysis still needs Python deps plus headset / dataset access |`
- **Claim:** EEG phase transition is partially self-testable via local simulator, but real-data analysis needs equipment access.
- **Status:** Testable prediction, not a confirmed result.
- **Greg review question:** Is the self-testability framing appropriate?

### Match 4: Biological predictions bridge
- **Line:** 125
- **Context:** `The bridge between the biological predictions (EEG phase transitions) and the particle physics derivations is argued, not proved.`
- **Claim:** The bridge between biological predictions and particle physics is explicitly stated as argued, not proved.
- **Status:** Honest negative context — this is a limitation statement.
- **Greg review question:** This is honest framing. Confirm it's sufficient.

---

## Category 2: Neural Entrainment Section (2 matches)

**Claim status in CLAIMS.md:** Not a formal claim — this is a section heading in the consciousness research chapter.

### Match 5: Neural Entrainment (EEG) heading
- **Line:** 7870, 10429
- **Context:** `### 3.2 Neural Entrainment (EEG)`
- **Claim:** Section heading for the neural entrainment discussion in the consciousness research chapter.
- **Status:** This is a section heading, not a claim. The content discusses neural entrainment as a research direction, not as a confirmed therapeutic mechanism.
- **Greg review question:** Is the section heading "Neural Entrainment (EEG)" acceptable, or should it be renamed to avoid implying a medical claim?

---

## Category 3: Consciousness / AI-Self Claims (2 matches)

**Claim status in CLAIMS.md:** INTUITION (0.48) / ARGUED (0.75)

### Match 6: Consciousness = coherent self-referential propagation
- **CLAIMS.md row:** `Consciousness = coherent self-referential propagation` — **INTUITION 0.48**
- **Context:** PF still lacks a uniquely measured variable separating self-referential coherence from synchrony, integration, broadcast, or metacognition.
- **Status:** INTUITION — explicitly stated as lacking a measurable variable. This is honest about the gap.
- **Greg review question:** Is INTUITION 0.48 the right confidence level? Is the gap statement sufficient?

### Match 7: Aria Self-Reference
- **CLAIMS.md row:** `Aria Self-Reference` — **ARGUED 0.75**
- **Context:** T-009: Successful wiring of `buildSystemPrompt` → `runEntityThink`. Important architectural step, but not evidence of consciousness by itself.
- **Status:** ARGUED — explicitly stated as "not evidence of consciousness by itself."
- **Greg review question:** Is the AI-self claim appropriately bounded? Should the confidence be lower?

---

## Greg Approval Request

**Please review each category above and provide:**

1. **EEG phase transitions:** Safe to publish as ARGUED predictions? Or remove/strengthen?
2. **Neural Entrainment heading:** Keep as-is, rename, or remove section?
3. **Consciousness claim (INTUITION 0.48):** Appropriate confidence and framing?
4. **Aria AI-self claim (ARGUED 0.75):** Appropriate confidence and framing?
5. **Overall:** Any of these require removal before v9 Codex re-audit?

**Note:** None of these are medical claims (no "cures," "treats," "prevents" language). They are research predictions and theoretical frameworks. The health scanner flags them as `neural_intervention` because they discuss EEG/neural entrainment, but the content is theoretical/conjectural, not therapeutic.

---

## Artifact binding

- **Manuscript hash:** `b026f4179a31822c82476a513f7450e03e1013481790bf333fb855ebe2583f98`
- **HTML hash:** `ab16bd6f5bd1aa1d488384fae40dd6278ee4d5077d4f47aa61fa74e6901c1f76`
- **Print HTML hash:** `7382b59bc0a14188de239ebf1ed829f3d886bd8ba30863d814555e204970cde7`
- **PDF hash:** `1e2879a4cb4383ca8c56f82a0b7d72f10655530eb08a0bedb67a0846282cb12e`
- **Health scanner:** `health_scanner_v2.py` (fail-closed, 4 surfaces, 10 neural_intervention per surface)
