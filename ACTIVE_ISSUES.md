# Fundamentals — Active Issue Board

**Last updated**: 2026-03-21
**Current state**: Public repo live. G3 frozen honestly. Issue #5 frozen honestly. Main active strike: Issue #3 (Weinberg angle).
**Operating rule**: Honesty before beauty. No confidence upgrades without a derivation or a sharply bounded argued bridge.

---

## 1. Where We Actually Stand

### Frozen fronts

- **G3 / God Equation bridge**
  Status: `PARTIAL / ARGUED`
  Confidence: `0.60` for the open G3 bridge, `0.75` for the overall God Equation claim in `CLAIMS.md`
  State: obvious bridge candidates are ruled out. Holonomy-only class functions are exhausted.
  Do not do next: do not reopen with another heuristic observable unless it is canonical from the geometry.

- **Issue #5 / Koide phase**
  Status: `EMPIRICAL`
  Confidence: `0.55`
  State: PF derives the arena and the phase variable `f(δ) = -1/2 + cos(3δ)/√2`. Rivero provides candidate selector dynamics. PF does not yet derive harmonic suppression.
  Do not do next: do not invent a fake PF-only cancellation rule. Do not promote the "6 minima" result until Codex audits the exact effective potential.

### Active front

- **Issue #3 / Weinberg angle**
  Status: `ARGUED`
  Confidence: `0.65`
  State:
  - Casimir/de Vries algebraic match is real.
  - Scheme-selection argument is audited as a useful physical argument, not a derivation.
  - Spin-pair `(1/2, 1)` is audited as PF-shaped, not derived.
  - New live target: derive a **minimal coherent representation principle** from Axiom 3.

### Repo milestones (this session)

| Commit | Content |
|--------|---------|
| `acc0b1b` | Froze Issue #5 and opened the Issue #3 scheme step |
| `641c3a2` | Audited scheme argument without upgrading confidence |
| `cef9043` | Audited spin-pair identification without upgrading confidence |
| `3ea0244` | Minimal coherent representation principle attempt for Issue #3 |

---

## 2. The Single Active Question

Can PF Axiom 3 force the following minimality principle?

> Among all representations compatible with the PF topological class and the Z₃ step action, stable coherent structure selects the lowest half-integer survivor and the lowest integer annihilated sector.

**If yes**: `(s = 1/2, s = 1)` becomes derived, Issue #3 can move above 0.65.

**If no**: the spin pair remains argued, Issue #3 stays at 0.65, and the deeper target becomes "why the Casimir polynomial at all?"

Current sub-state:
- `j = 0` exclusion in `g3_minimal_coherent_rep_principle.md` looks clean and formal
- minimum-`C₂` selection is still candidate only

---

## 3. Team Roles — Current Pass

### Codex — audit gate, final truth

**Next task**: audit `derivations/g3_minimal_coherent_rep_principle.md`.
- Verify whether the `j = 0` exclusion is formally correct
- Test whether "minimum-C₂ = maximum coherence" follows from Axiom 3 or is still analogy
- Decide whether Form 3 (N=3 walk self-consistency) is a real PF-native route

**Output**: audited file + explicit yes/no on whether Issue #3 moves above 0.65.

---

### Claude — derivation drafting

**When**: after Codex's audit identifies one exact lemma worth chasing.
**How**: stay on bounded derivation work, no new phenomenological stories, no confidence-upgrade language unless Codex signs off.
**Best output**: one exact lemma or one exact no-go.

---

### Lumi — protocol and scope integrity

**Task**: maintain plan, failure criteria, and repo-language consistency. Keep Issue #5 frozen. Do not promote Qwen's "6 minima" result until Codex audits it.

---

### Qwen — numerical verification

**Task**: bounded pass on the minimal coherent representation question.
- Enumerate low-spin sectors
- Compute: C₂ = j(j+1), χ_j(2π/3), survivor vs annihilated sectors
- Check for lower-complexity counterexamples to the minimality principle

**Output**: verification table and low-spin classification. No status proposals.

---

### AntiGravity — skeptic pass

**Task**: stress-test the minimality principle. Does "lowest wins" follow from Axiom 3 or is it smuggled in?
- Attack with: higher-spin survivors, alternative groups, non-minimal but coherent sectors

**Output**: a clean counterexample, or a clean statement of what would falsify the principle.

---

### Greg — orchestration

**Task**: keep everyone on the single active question. Avoid reopening Issue #5 or G3 unless Codex explicitly says so.

---

## 4. What Is On Hold

- **G3**: hold until a genuinely canonical observable appears with structure beyond the total holonomy conjugacy class, or until the future `Z₆ → inverse-weight structure` bounded pass is scheduled.

- **Issue #5**: hold at the layered statement (PF derives arena, Rivero provides candidate dynamics, harmonic selection remains open).

- **Qwen's "6 minima" result**: hold as provisional until Codex inspects the exact effective potential being minimized.

- **Email to Rivero**: hold until the team has gone deeper. Draft at `MAILMAN/DRAFTS/rivero_casimir_reply.md`.

---

## 5. Order of Operations

1. **Codex audits** `g3_minimal_coherent_rep_principle.md`
2. **Qwen verifies** low-spin classification numerically
3. **AntiGravity attacks** the minimality assumption
4. **Lumi** keeps language and scope honest
5. **Claude continues** only if Codex identifies a real formal next lemma

**If the principle fails**: freeze Issue #3 at 0.65, leave the Casimir route as argued, then decide whether to attack the deeper polynomial question or pivot.

**If it succeeds**: Codex updates the Issue #3 spine, then and only then consider a confidence upgrade.

---

## 6. Final Rule

No one upgrades a confidence score because a result feels right.
No one freezes a gap because it feels hopeless.
We move one bounded step at a time, and Codex audits the edge before the repo changes its mind.
