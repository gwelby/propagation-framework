# T2 — Denominator Theorem: Prove M=3 from PF axioms alone (co-dimension route)



## What This Is

**Frontier**: Three Generations denominator — `PARTIAL DERIVATION 0.85`
**Blocking**: Three Generations (Ticket 3), God Equation
**Source audit**: `file:derivations/three_generations_t2_audit_2026-03-28.md`

The algebra `Q(N) = 2N/(2N+3) = 2/3 → N=3` is exact once `M=3` is granted. The denominator `3` is supported by three converging arguments (co-dimension, `SO(3)` generator count, broken-symmetry language) — but convergence is not a theorem. One closed proof is needed.

---

## The Exact Gap (from Codex audit)

The cleanest route identified is the **formal co-dimension theorem**:

> Prove within PF that: `number of independent massive restoration modes = co-dim(point defect)`

The first arrow (point defect in 3D → co-dimension 3) is trivial geometry. The second arrow is the nontrivial theorem: why does co-dimension equal the number of massive bosonic restoration modes?

**What is NOT allowed** (documented no-gos from the audit):
- Importing the observed electroweak triplet `(W+, W-, Z)` as the denominator proof
- Treating co-dimension, Lie-group dimension, and massive gauge-boson count as automatically identical
- Invoking Goldstone/Higgs language without an explicit broken-symmetry setup and order parameter

---

## The Volovik Bridge (Qwen's finding)

From `file:AGENTS.md` (RESEARCH wave findings):

> Volovik's *Universe in a Helium Droplet* confirmed the co-dimension argument for M=3 in superfluid ³He — the same argument the framework needs for T2.

The task is to translate Volovik's ³He co-dimension theorem into PF language — replacing the superfluid order parameter with the PF coherence field, and showing the counting is identical.

---

## Proof Obligations

Write a formal derivation file `derivations/t2_denominator_theorem.md` that:

1. **Defines the PF order parameter** — what is the field that undergoes phase locking? Name it explicitly. This is the step the Goldstone route was missing.
2. **States the symmetry group before locking and the unbroken subgroup after** — without importing the Standard Model answer.
3. **Proves the co-dimension theorem**: in a 3D PF medium, a point-defect in the coherence field has co-dimension 3, and this equals the number of independent massive restoration modes. Cite Volovik's ³He result as a structural template, but prove the PF version from PF axioms.
4. **States the theorem cleanly**: "The denominator in `Q(N) = 2N/(2N+M)` is `M=3`, derived from the co-dimension of a point defect in the 3D PF coherence field."

---

## Acceptance Criteria

- [ ] The PF order parameter is explicitly defined (not borrowed from the Standard Model)
- [ ] The co-dimension → restoration-mode count step is proved, not asserted
- [ ] The Volovik ³He analogy is used as a template, not as the proof itself
- [ ] Codex audits the file and either signs off or names the remaining hidden step
- [ ] If signed off: `CLAIMS.md` updates T2 from `PARTIAL DERIVATION 0.85` → `DERIVED 0.90`

**Assigned to**: Claude (draft, using Volovik as template) → Codex (audit)
**Do not promote** without Codex sign-off.

