# Gap 2 No-Go: Fisher Unitary Invariance Fails at Quadratic Readout

**Agent:** Qwen
**Date:** 2026-04-04
**Prompted by:** Greg's pressure-test request for Gap 2 (Obligation H-B)
**Cross-references:** `god_eq_path_a_chiral_forcing_2026-04-04.md`, `chiral_projection_z3.py`, `h_prod_joint_model_obligation.md`

---

## The Claim Tested

The draft `god_eq_path_a_chiral_forcing_2026-04-04.md` §3 argues:

> Because T_L³ is exactly diagonal in the 2D {k=0, k=1} Fourier subspace,
> the physical Fourier modes are statistically independent. Since the Fisher
> Information trace is unitarily invariant, the Fisher information should add
> linearly (G = 3λ₀I) in the orthogonal Fourier basis just as well as it would
> in the position basis. If true, this bypasses the position-space off-diagonal
> obstruction entirely.

## The Test

Computed Fisher Information in TWO spaces:
1. **Fourier amplitude space** (complex linear): Fisher = Σ|λᵢ³|²
2. **Position probability simplex** (real): Fisher = Σₓ T[a,x]·T[b,x] / P(x)

Compared across η ∈ {0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0}.

## Results

| η | Fisher(amp) | Fisher(pos) | Ratio | Match? |
|---|-------------|-------------|-------|--------|
| 0.0 | 3247.64 | 3.31 | 981× | NO |
| 0.5 | 2637.73 | 3.68 | 717× | NO |
| 1.0 | 405.95 | 9.00 | 45× | NO |

**Unitary invariance FAILS for every η tested.**

## The Mechanism of Failure

The quadratic readout P(j) = |Σₖ U[j,k]·aₖ|² introduces cross-terms:

```
P(j) = |U[j,0]·a₀ + U[j,1]·a₁|²
     = |U[j,0]|²·|a₀|² + |U[j,1]|²·|a₁|² + 2·Re[U[j,0]·U[j,1]*·a₀·a₁*]
```

The interference term 2·Re[...] couples the Fourier modes even when
they are independent in amplitude space. This is not a bug — it is
the defining feature of quantum-like probability.

Verified explicitly: P(j|k=0+k=1) ≠ (P(j|k=0) + P(j|k=1))/2.
The superposition probability differs from the mixture probability
by interference terms.

## Conclusion

**The specific Fourier/unitary-invariance shortcut for Gap 2 (Obligation H-B)
is a no-go.** The 2D Fourier diagonal closure does NOT imply position-space
factorization because the quadratic readout reintroduces mode coupling
through interference.

The unitary invariance of Fisher Information trace applies to the
amplitude space (linear, complex). It does NOT survive the
amplitude→probability map (quadratic, real simplex).

## Implications for the Live Board

**What this kills:** The specific bridge argument in
`god_eq_path_a_chiral_forcing_2026-04-04.md` §3 that claimed the
Fourier-space diagonal closure bypasses the position-space obstruction.
That route is dead.

**What remains on the live board (ACTIVE_ISSUES.md, G3):**

- **Path A** now narrows further: without the Fourier-space shortcut,
  the Path A route requires proving b→0 EXACTLY from the Z₃ Lagrangian
  under left-chiral weak coupling. When b→0, T=S̄, T³=I, and H_prod
  factorizes trivially. The natural next attack surface is the
  left-chiral weak-coupling interaction spec (draft, not settled).

- **Path B** remains open: Family C (quadratic closure functionals
  of the operator) is the last natural candidate before non-quadratic
  routes. The Fisher/trajectory result (Codex) shows I(C;Y)=I(C;X₁) —
  no extra factorization power — so that route doesn't help Path B
  either.

- **Lemma C** (Obligation 1: Markov/local-state closure) remains
  a separate front, pending Codex verification of the
  echo/extremal-coherence argument.

- **H_basis** (basis selection in the degenerate Q-sector) remains
  a complementary front, requiring the vacuum covariance structure
  to break Q-sector degeneracy.

**What this does NOT say:** The God Equation is not yet reduced to
a single remaining target. Multiple bounded fronts remain open
until audited out. Gap 2's death is one specific shortcut, not
a collapse of all obligations except b→0.

---

*Computation by Qwen | 2026-04-04 | All code reproducible*
*Reviewed against ACTIVE_ISSUES.md and h_prod_joint_model_obligation.md*
