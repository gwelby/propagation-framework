# Hostile re-audit of `PfLean/NullClassProofs.lean` — 2026-08-20

**Auditor:** Devin
**Code commit audited:** `530699f` (Class I, bridge, and Class II CI closed; wording corrected to "no project-specific axioms").
**Protocol amendment commit:** `877d4e6` (Route E preregistration locked to `530699f`).
**Status:** PASS — no project-specific axioms, zero `sorry`s, every premise-removal probe broke the proof as expected.

---

## 1. Static checks

- `grep '\b(sorry|admit|axiom)\b'` on `lean/PfLean/NullClassProofs.lean`: only matches are in comments explaining what was removed and what is NOT formalized. No source `sorry`, `admit`, or `axiom` remains.
- `lake build PfLean.NullClassProofs`: **8248/8248 jobs green**.
- Full `lake build`: **16572/16572 jobs green**.

## 2. Axiom inventory (`#print axioms`)

All five main theorems depend on exactly the standard Lean 4 foundation axioms and nothing else:

| Theorem | Axioms |
|---------|--------|
| `class_I_conditional_independence` | `propext`, `Classical.choice`, `Quot.sound` |
| `condIndep_sup_of_condIndep_left` | `propext`, `Classical.choice`, `Quot.sound` |
| `condIndepFun_comp_left` | `propext`, `Classical.choice`, `Quot.sound` |
| `indepFun_implies_condIndepFun` (bridge lemma) | `propext`, `Classical.choice`, `Quot.sound` |
| `class_II_conditional_independence` | `propext`, `Classical.choice`, `Quot.sound` |

There are **no project-specific axioms** in `NullClassProofs.lean`.

## 3. Premise-removal probes

For each probe, the script `lean/scripts/premise_probe.py` temporarily removes one hypothesis from the theorem statement, runs `lake build PfLean.NullClassProofs`, and restores the file. A successful build would mean the theorem is overclaiming (the premise is not needed). All probes **broke the build**, confirming the premises are load-bearing.

| Probe | Removed hypothesis | Result | Failure mode |
|-------|--------------------|--------|--------------|
| `class_I_remove_hf` | `hf : Measurable f` | BROKEN (expected) | `Unknown identifier 'hf.comp'` at line 97 |
| `class_I_remove_hM` | `hM : M = f ∘ E` | BROKEN (expected) | `Unknown identifier 'hM'` at line 96 (used by `subst`) |
| `class_I_remove_hX_meas` | `hX_meas : Measurable X` | BROKEN (expected) | `Unknown identifier 'hX_meas'` at line 97 (used by `condIndepFun_of_measurable_left`) |
| `class_II_remove_hfuture_indep` | `hfuture_indep : IndepFun (E', noise) (X, E, M) μ` | BROKEN (expected) | `Unknown identifier 'hfuture_indep.comp'` at line 478 |

The proof bodies fail immediately when a premise is removed, so the theorems are not overclaiming on these axes.

## 4. Known limit

The **only** unformalized step remains the information-theoretic bridge `CI ⟹ I(M; X | E) = 0`. It is NOT stated as an axiom and NOT proven. Formalizing it requires a Lean definition of conditional mutual information and is explicitly marked as future work.

## 5. Honest boundaries

- This module does **not** prove anything about consciousness, EEG, wPLI, or real data.
- It does **not** prove `MI = 0`.
- It uses only standard Lean foundation axioms; the phrase "no project-specific axioms" is accurate.
- `common_driver_confound` remains a known limit (unobserved driver).
- PUBLIC HOLD remains in effect.

---

**Verdict:** `NullClassProofs.lean` at `530699f` passes a hostile re-audit for hidden `sorry`s, hidden axioms, and premise necessity.
