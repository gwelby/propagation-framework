# H_prod: The Exact Proof Obligation (2026-04-04)

**Author**: Claude Sonnet 4.6
**Status**: OPEN — route map, not a proof
**Purpose**: State the exact remaining obligation for H_prod, given the audit trail through Wave 5–6.
**Truth sources**: `h_prod_markovian_walk_proof.md`, `god_eq_h_prod_model_routes_audit_2026-04-01.md`,
  `god_eq_path_b_family_c_counterexample_search_2026-04-02.md`, `ACTIVE_ISSUES.md`

---

## 1. What the Route Audits Have Established

### Dead routes (killed exactly)

| Route | Killed by | File |
|-------|-----------|------|
| DFT orthogonality → H_prod | Diagonal T ≠ independent joint law | `h_prod_markovian_walk_proof.md §5` |
| T_sym³ diagonal → factorization | T_sym³ is NOT diagonal (off-diag = 3/8) | `god_eq_gap_B_nearest_neighbor_no_go.md` |
| One-hot X^(j) on T_sym | P(X^(0)=1,X^(1)=1,X^(2)=1)=0 while product>0 | Routes audit §5 |
| Family C canonical (quadratic) | Real symmetric circulant algebra is 2-dimensional | `god_eq_path_b_family_c_counterexample_search_2026-04-02.md` |
| Fisher/trajectory beats first-step | I(C;Y)=I(C;X₁) — no extra leverage | `fisher_3step_degeneracy_proof.md` |

### What is NOT dead

- **H_prod itself** — the statement that there exists a joint probability model on
  one three-channel medium such that the channel closure events factorize.
- **Noncanonical basis-fixed Family C** — requires H_basis derivation (why a specific
  basis inside the degenerate Q-sector is selected).
- **Path A (extra directional coupling → b→0)** — if an added weak-coupling structure
  forces b→0 (pure forward shift T=S̄), then T³=I exactly, and the one-hot factorization
  trivially holds. But the 2026-04-05 `\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3` audit says
  the bare G1 kinematics do not force any canonical chirality-direction lock.

---

## 2. The Three Exact Proof Obligations

From `h_prod_markovian_walk_proof.md §7`:

### Obligation 1 — Full local state with first-order evolution

> Define the full local state of the medium and derive that its evolution is
> first-order in time (Markov) from the PF axioms.

**Current gap**: Finite causal speed (Axiom 2) gives locality but not first-order
memorylessness of the coarse walk state. A local system can still carry memory
through hidden variables.

**What would close it**: Either show the walk state is a minimal sufficient statistic
for future evolution (no hidden variables), or show Axiom 3 extremal coherence forces
the minimal state — the echo argument direction from Lemma C candidate.

### Obligation 2 — Primitive operator derivation

> Either derive the primitive transition operator used in the closure argument from
> the ℤ₃-extended Lagrangian, OR rewrite the theorem directly from the actual
> circulant operator derived from the EOM.

**Current gap**: The clean closure proof requires T³ = K³·I (pure-shift family).
The Z₃ EOM gives T_sym = (1/2)(S̄ + S̄²), which does NOT cube to a diagonal matrix.

**What would close it**: Either Path A closes b→0 from the CP/chiral argument,
giving T=S̄ and T³=I, OR show that the physical observable (closure event) can be
defined on the projected {k=0,k=1} sector where closure IS diagonal.

### Obligation 3 — Explicit joint probability model + factorization proof

> Define a joint probability law P(X^(0), X^(1), X^(2)) on ONE three-channel medium
> (not three independent experiments) and prove it factorizes.

**Current gap**: Two interpretations remain:

- **Interpretation A** (three independent experiments): product factorization holds
  by construction but changes the meaning of N=3 in the God Equation.
- **Interpretation B** (one coupled medium): the minimal one-hot model fails immediately
  (P(all three return) = 0 for T_sym). Any replacement observable must be defined
  explicitly.

**What would close it**: A precise probability space assignment — σ-algebra,
measure, and observable definitions — such that channel events X^(j) are provably
independent events in that space, derived from T and the PF axioms alone.

---

## 3. Which Obligation is Closest to Closed

### Obligation 2 is closest, via Path A

If CP violation forces b→0 (pure shift T=S̄):
- T³ = S̄³ = I (exact diagonal, all entries = 1)
- One-hot return probability = 1 for every channel
- P(X^(j)=1)=1 for all j, trivially independent

The formal Path A target is now narrower: **derive an added weak-coupling structure that
drives b/a → 0 in the IR.** This can no longer be stated as "bare left-chiral G1
kinematics force the pure shift."

Current status: `chiral_projection_z3.py` shows P_L kills the k=2 eigenmode but does
NOT eliminate S̄² from the position-space matrix (|β/α|=1 after projection). The
2026-04-05 audit `path_a_z6_z3_chirality_intertwiner_audit_2026-04-05.md` then proves
that the bare `\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3` kinematics do not force any
canonical lock between quotient direction and spacetime chirality.
Two remaining gaps:
1. Derive a genuine generation-directional weak-coupling term or locking mechanism beyond bare G1
2. If such a term exists, prove it really yields the position-space factorization needed for `H_prod`

### Obligation 1 has a candidate path (Lemma C)

The echo/Lemma C argument (Kilo.ai, 2026-03-29):
> Unpopulated available mode = coherence leak = unstable by Axiom 3 extremal principle
> → medium MUST populate all available rotational branches.

If confirmed (pending Codex formal verification), this would close the Markov step:
the full local state is the minimal state that populates all coherent modes, and
its evolution is first-order by the extremal coherence principle.

### Obligation 3 remains open with no active route

No surviving proposal defines a joint probability model on one medium that factorizes.
The surviving candidates would require either Path A closure (trivial factorization at T=S̄)
or a genuinely new observable definition.

---

## 4. The Sharpest Next Target

Given the audit state:

**Target A (highest leverage)**: Derive an explicit weak-coupling extension that
produces a real generation-directional asymmetry b/a → 0 in the IR. This is the
surviving Path A target and would simultaneously close Obligation 2.

**Target B (parallel)**: Confirm Lemma C formally (Codex verification of the
echo/extremal-coherence argument). This closes Obligation 1 and enables a Markov
walk probability model.

**Target C (complementary)**: Derive H_basis — why a specific basis inside the
degenerate Q-sector is physically selected. This is the noncanonical Family C sliver.
Requires the vacuum covariance structure (positive off-diagonals on stable branch)
to break the Q-sector degeneracy.

**NOT the next target**: Any further investigation of Family C canonical (no-go is
pinned), or Family A/B intensity routes (killed by earlier audits), or Fisher/trajectory
quadratic probes (I(C;Y)=I(C;X₁) — no extra power).

---

## 5. Empirical Probe

`sandbox/pf_toy_world_model.py` now includes `probe_h_prod()` and `run_h_prod_survey()`
which compute:
- Whether T³ is diagonal for each walk configuration
- KL divergence between joint distribution and product distribution
- Mutual information I(channel; 3-step outcome)

These mirror the four parameter sets from `fisher_3step_numerical.md`.
Key finding: T_sym³ is not diagonal (off-diag fraction ≈ 0.72), confirming the
one-hot factorization fails for the physical symmetric closure operator.
The diagonal condition holds only for T = pure shift (b/a=0, the Path A target).

---

## 6. Summary of Status

```
H_prod: OPEN (God Equation CONDITIONAL 0.88)

Proof obligations:
  [1] Full local state + first-order evolution   ← Lemma C candidate (Codex pending)
  [2] Primitive operator = pure shift T=S̄       ← Path A target (chiral b→0)
  [3] Explicit joint model + factorization proof ← depends on [1] and [2]

Live routes:
  - Path A: CP violation → b/a→0 in IR (chiral ℤ₃ Lagrangian)
  - Lemma C: extremal coherence forces full mode population → Markov
  - H_basis: vacuum Q-sector degeneracy breaking (noncanonical Family C sliver)

Dead routes (exact no-gos):
  - Family C canonical (2D real symmetric circulant algebra, C₃-invariant)
  - Fisher/trajectory absolute-label (I(C;Y)=I(C;X₁))
  - T_sym diagonal argument (T_sym³ is not diagonal)
  - DFT orthogonality → factorization
```

---

*This file: route map + exact obligations. Not a proof attempt.*
*Next proof attempt should target Path A (Obligation 2) or Lemma C (Obligation 1).*
