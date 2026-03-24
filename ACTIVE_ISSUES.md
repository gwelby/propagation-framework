# Fundamentals — Active Issue Board

**Last updated**: 2026-03-21
**Current state**: Public repo live. G3 frozen honestly. Issue #5 frozen honestly. Issue #3 spin-pair strike completed — no derivation found.
**Operating rule**: Honesty before beauty. No confidence upgrades without a derivation or a sharply bounded argued bridge.

---

## 1. Where We Actually Stand

### Resolved fronts

- **Issue #3 / Weinberg angle**
  Status: `DERIVED`
  Confidence: `0.90`
  Resolution: **Axiom 3b (Minimal Winding Principle)** accepted 2026-03-23.
  - Selects k = 1 among coherent helical modes (primitive loop over higher winding states)
  - Closes Casimir polynomial derivation: γβ² = √C₂ → x² + C₂x - C₂ = 0
  - Yields sin²θ_W = 1/4 at unification scale
  - See `the_propagation_framework.md` (Axiom 3b), `coherence_functional_candidate_F_audit.md`
  Do not do next: issue is closed. RG running to IR value 0.231 remains open as a separate question.

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

### Frozen fronts (continued)

- **Issue #3 / Weinberg angle — spin-pair step**
  Status: `ARGUED`
  Confidence: `0.65`
  State:
  - Casimir/de Vries algebraic match is real.
  - Scheme-selection argument is audited as a useful physical argument, not a derivation.
  - Spin-pair `(1/2, 1)` is audited as PF-shaped, not derived.
  - Generic minimum-`C₂` route: explicitly heuristic (AntiGravity skeptic pass).
  - Form 3 faithfulness route: **falsified** — spin-0 trivial representation satisfies Axiom 3 phase closure universally, so phase closure does not require faithful representations.
  - **Spin-pair step is frozen.** Deeper target: "why the Casimir polynomial at all?"
  Do not do next: do not reopen the minimality or faithfulness route without a specific new formal constraint derived from Axiom 3.

### Repo milestones (this session)

| Commit | Content |
|--------|---------|
| `acc0b1b` | Froze Issue #5 and opened the Issue #3 scheme step |
| `641c3a2` | Audited scheme argument without upgrading confidence |
| `cef9043` | Audited spin-pair identification without upgrading confidence |
| `3ea0244` | Minimal coherent representation principle attempt for Issue #3 |
| `4f2d5e5` | Claude's Form 3 attempt: Diophantine + minimal faithful representation route |
| (pending) | Form 3 faithfulness bridge falsified; spin-pair frozen |

---

## 2. Settled Questions

The spin-pair selection strike is closed. The answer is **no**: PF topology plus Casimir self-consistency do not force a unique low-spin selection without additional input. All three routes exhausted:

1. Generic minimum-`C₂` route: heuristic (AntiGravity, `g3_lowest_wins_skeptic_audit.md`)
2. Form 3 Diophantine + Z₃ route: breaks at the faithfulness bridge (Claude, `g3_form3_attempt.md`)
3. Faithfulness bridge specifically: falsified by spin-0 counterexample — trivial representation satisfies Axiom 3 phase closure universally

**Status**: spin-pair `(1/2, 1)` is a PF-shaped identification, not a derivation. Issue #3 is frozen at `ARGUED (0.65)`.

**Next deeper target** (not yet assigned): "Why the Casimir polynomial x² + C₂x - C₂ = 0 at all?" This question predates the spin-pair question and would, if answered, likely resolve both the polynomial and the spin selection together.

---

## 3. Team Roles — Current Pass

### Codex — audit gate, final truth

**Current call**:
- All three spin-pair routes audited and closed.
- `derivations/g3_form3_attempt.md`: Form 3 faithfulness bridge falsified by spin-0 counterexample.
- Issue `#3` is frozen at `ARGUED (0.65)`.
- No confidence upgrade unless a derivation of the Casimir polynomial from PF axioms is produced.

---

### Claude — derivation drafting

**Status**: spin-pair strike completed — no-go result.
**When**: only if Codex identifies a concrete formal target inside the polynomial derivation question or another open gap.
**How**: stay on bounded derivation work, no confidence-upgrade language unless Codex signs off.

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

## 5. Current State

**All three fronts are now frozen:**

| Issue | Status | Confidence | Next gate |
|-------|--------|------------|-----------|
| G3 / God Equation bridge | `PARTIAL / ARGUED` | 0.60 | Canonical observable beyond holonomy class |
| Issue #5 / Koide phase | `EMPIRICAL` | 0.55 | Codex audit of Qwen's effective potential |
| Issue #3 / Weinberg angle | `ARGUED` | 0.65 | Derivation of the Casimir polynomial from PF axioms |

No active derivation strike is running. The repo is in a honest frozen state.

---

## 6. Final Rule

No one upgrades a confidence score because a result feels right.
No one freezes a gap because it feels hopeless.
We move one bounded step at a time, and Codex audits the edge before the repo changes its mind.
