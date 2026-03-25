# Fundamentals — Active Issue Board

**Last updated**: 2026-03-24
**Current state**: Public repo live. Issue #3 / Weinberg angle RESOLVED (DERIVED 0.90 via Axiom 3b). G3 frozen honestly. Issue #5 frozen honestly.
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
  - Yields sin²θ_W ≈ 0.22310, matching the PDG on-shell value to 0.13σ.
  - See `the_propagation_framework.md` (Axiom 3b), `coherence_functional_candidate_F_audit.md`
  Do not do next: issue is closed. RG running to IR value 0.231 remains open as a separate question.

### Frozen fronts

- **G3 / God Equation bridge**
  Status: `CONDITIONAL`
  Confidence: `0.88`
  State: The spatial scaling factor $N^{D/2}$ is mathematically proven to be the Fisher Information Volume of the phase-locking manifold. Axiom 4 ($[T(\theta), \bar{S}] = 0$) is now a THEOREM derived from the $\mathbb{Z}_3$-extended Lagrangian. $H_{prod}$ is ARGUED via Axiom 2 causal locality (Markovian walk). 
  Next audit target: Codex to audit the three specific steps (A, B, C) of the $H_{prod}$ proof to upgrade to DERIVED.

- **Issue #5 / Koide phase**
  Status: `EMPIRICAL`
  Confidence: `0.55`
  State: PF derives the arena and the phase variable `f(δ) = -1/2 + cos(3δ)/√2`. Rivero provides candidate selector dynamics. PF does not yet derive harmonic suppression.
  Do not do next: do not invent a fake PF-only cancellation rule. Do not promote the "6 minima" result until Codex audits the exact effective potential.

### Historical: Issue #3 spin-pair sub-question (superseded)

The spin-pair selection strike explored whether PF topology forces the specific spin pair (1/2, 1). Three routes were exhausted (all no-go). This sub-question became moot when **Axiom 3b (Minimal Winding Principle)** resolved the Weinberg angle via a different route — selecting k=1 directly from coherence rather than deriving the spin pair. The spin-pair work is preserved as an honest record of failed approaches. See Section 2 for details.

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

### Issue #3 / Weinberg angle — RESOLVED

The Weinberg angle derivation is closed. **Axiom 3b (Minimal Winding Principle)** selects k=1, closing the Casimir polynomial derivation and yielding sin²θ_W ≈ 0.22310 (matching PDG on-shell to 0.13σ). Confidence: 0.90.

The remaining open question (RG running from UV value 1/4 to IR value 0.231) is a separate problem, not a gap in the derivation.

### Spin-pair selection strike — closed (historical)

The earlier spin-pair sub-question is closed as a no-go. PF topology plus Casimir self-consistency do not force a unique low-spin selection without additional input. All three routes exhausted:

1. Generic minimum-`C₂` route: heuristic (AntiGravity, `g3_lowest_wins_skeptic_audit.md`)
2. Form 3 Diophantine + Z₃ route: breaks at the faithfulness bridge (Claude, `g3_form3_attempt.md`)
3. Faithfulness bridge specifically: falsified by spin-0 counterexample

This became moot when Axiom 3b resolved the Weinberg angle via minimal winding instead.

---

## 3. Team Roles — Current Pass

### Codex — audit gate, final truth

**Current call**:
- Issue #3 / Weinberg angle: RESOLVED at DERIVED 0.90 via Axiom 3b.
- G3 / God Equation: CONDITIONAL 0.88. Axiom 4 derived. $H_{prod}$ Markov proof awaits final audit.
- Issue #5 / Koide phase: frozen at EMPIRICAL 0.55. Qwen's effective potential awaits audit.
- Next audit target: Qwen's "6 minima" effective potential (Issue #5), if assigned.

---

### Claude — derivation drafting

**Status**: Weinberg angle resolved. Spin-pair strike completed (no-go, now moot).
**When**: if Codex identifies a concrete formal target in G3, α derivation, RG running, or another open gap.
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

**Task**: decide next priority among open fronts (G3, Issue #5, α derivation, RG running, EEG experiment, publication). Avoid reopening G3 unless Codex explicitly says so.

---

## 4. What Is On Hold

- **G3**: hold until a genuinely canonical observable appears with structure beyond the total holonomy conjugacy class, or until the future `Z₆ → inverse-weight structure` bounded pass is scheduled.

- **Issue #5**: hold at the layered statement (PF derives arena, Rivero provides candidate dynamics, harmonic selection remains open).

- **Qwen's "6 minima" result**: hold as provisional until Codex inspects the exact effective potential being minimized.

- **Email to Rivero**: hold until the team has gone deeper. Draft at `MAILMAN/DRAFTS/rivero_casimir_reply.md`.

---

## 5. Current State

**Issue #3 is resolved. Two fronts remain frozen:**

| Issue | Status | Confidence | Next gate |
|-------|--------|------------|-----------|
| Issue #3 / Weinberg angle | `DERIVED` | 0.90 | **RESOLVED** via Axiom 3b. RG running to IR is a separate question. |
| G3 / God Equation bridge | `CONDITIONAL` | 0.88 | Codex audit of $H_{prod}$ Markov proof (Steps A, B, C) |
| Issue #5 / Koide phase | `EMPIRICAL` | 0.55 | Codex audit of Qwen's effective potential |

No active derivation strike is running. Issue #3 is closed. G3 and Issue #5 remain honestly frozen.

---

## 6. Final Rule

No one upgrades a confidence score because a result feels right.
No one freezes a gap because it feels hopeless.
We move one bounded step at a time, and Codex audits the edge before the repo changes its mind.
