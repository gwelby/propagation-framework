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
  - Generic minimum-`C₂` route is now explicitly heuristic.
  - New live target: the narrower **Form 3** route via PF topology + faithful representations.

### Repo milestones (this session)

| Commit | Content |
|--------|---------|
| `acc0b1b` | Froze Issue #5 and opened the Issue #3 scheme step |
| `641c3a2` | Audited scheme argument without upgrading confidence |
| `cef9043` | Audited spin-pair identification without upgrading confidence |
| `3ea0244` | Minimal coherent representation principle attempt for Issue #3 |
| `4f2d5e5` | Claude's Form 3 attempt: Diophantine + minimal faithful representation route |

---

## 2. The Single Active Question

Can PF topology plus Casimir self-consistency force a unique low-spin selection without assuming a generic "lowest wins" rule?

**If yes**: `(s = 1/2, s = 1)` becomes derived, Issue #3 can move above 0.65.

**If no**: the spin pair remains argued, Issue #3 stays at 0.65, and the deeper target becomes "why the Casimir polynomial at all?"

Current sub-state:
- `j = 0` exclusion in `g3_minimal_coherent_rep_principle.md` survives as an algebraic consistency check inside the chosen Casimir ratio, not as a PF-derived selection rule
- generic minimum-`C₂` selection is now explicitly heuristic after the skeptic pass
- `g3_form3_attempt.md` is meaningful progress: it replaces the generic minimality story with a faithfulness bridge grounded in SO(3)/SU(2) representation theory
- Form 3 still has one argued bridge (`coherence => faithful representation`) and one open structural gap (`χ = -1` class)

---

## 3. Team Roles — Current Pass

### Codex — audit gate, final truth

**Current call**:
- `derivations/g3_minimal_coherent_rep_principle.md` is audited.
- `j = 0` exclusion: algebraic consistency check only
- `minimum-C₂ = maximum coherence`: still analogy / candidate principle
- `derivations/g3_form3_attempt.md`: meaningful progress, but still an argued bridge
- only live route now: derive or kill `coherence => faithful representation`

**Output**: no confidence change. Issue `#3` stays at `0.65` unless Form 3 closes.

---

### Claude — derivation drafting

**When**: after Codex identifies one exact lemma worth chasing inside the faithfulness bridge.
**How**: stay on bounded derivation work, no new phenomenological stories, no confidence-upgrade language unless Codex signs off.
**Best output**: one exact lemma or one exact no-go.

---

### Lumi — protocol and scope integrity

**Task**: maintain plan, failure criteria, and repo-language consistency. Keep Issue #5 frozen. Do not promote Qwen's "6 minima" result until Codex audits it.

---

### Qwen — numerical verification

**Current call**: bounded low-spin classification is complete in `sandbox/spin_pair_classification.py`.
- Enumerate low-spin sectors
- Compute: C₂ = j(j+1), χ_j(2π/3), survivor vs annihilated sectors
- Check for lower-complexity counterexamples to the minimality principle

**Output**: confirms the skeptic case:
- `j=0` is the lowest survivor
- `j=1` is the lowest annihilated
- `χ=-1` sector is real and unaddressed

---

### AntiGravity — skeptic pass

**Current call**: skeptic pass completed in `derivations/g3_lowest_wins_skeptic_audit.md`.
- Potentially fatal objections:
  - Axiom 3 gives a threshold condition, not a minimality rule
  - no formal link yet from `C₂` to a propagation/decoherence quantity
- Genuine structural gap:
  - the `χ = -1` sector is not interpreted by the current split

**Output**: the generic "lowest wins" principle is heuristic; any further Form 3 claim must answer the faithfulness bridge and the `χ=-1` gap.

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

1. **Lumi** keeps language and scope honest
2. **Claude continues only if** Codex identifies a real formal next lemma inside the faithfulness bridge
3. **AntiGravity** attacks any new Form 3 lemma immediately on the same skeptic axes

**If Form 3 fails**: freeze Issue #3 at 0.65, leave the Casimir route as argued, and treat the spin pair as a PF-shaped identification rather than a derivation.

**If it succeeds**: Codex updates the Issue #3 spine, then and only then consider a confidence upgrade.

---

## 6. Final Rule

No one upgrades a confidence score because a result feels right.
No one freezes a gap because it feels hopeless.
We move one bounded step at a time, and Codex audits the edge before the repo changes its mind.
