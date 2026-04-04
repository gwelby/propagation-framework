This ticket is now a **historical stale draft**.

After the 2026-04-01 chiral audit, its dependency on "Ticket 4 gives `b=0` and diagonal `T^3`" is
no longer valid. Use instead:

- `CLAIMS.md`
- `ACTIVE_ISSUES.md`
- `Plan_v1___Handoff__Ticket__God_Equation_H_prod_—_Write_the_explicit_joint_probability_model_and_prove_factorization.md`
- `derivations/god_eq_h_prod_model_routes_audit_2026-04-01.md`
- `derivations/god_eq_path_b_single_system_observable_spec_2026-04-01.md`

Do **not** treat the completion status or dependency structure below as current truth.

# God Equation H_prod — Write the explicit joint probability model and prove factorization



## What This Is

**Frontier**: God Equation `λ_c` — `CONDITIONAL 0.88`
**This ticket**: The final probability bridge — H_prod
**Depends on**: Historical pre-2026-04-01 Path A framing only; now superseded by the audited Path A /
Path B split
**Source**: `file:derivations/h_prod_markovian_walk_proof.md`,
`file:derivations/god_eq_gap_B_nearest_neighbor_no_go.md`

Even with diagonal 3-step closure (from Ticket 4), H_prod is not yet proved. The Codex audit identified three remaining obligations that zero covariance / diagonal closure does not satisfy:

---

## The Three Remaining Proof Obligations (from Codex audit)

From `file:derivations/h_prod_markovian_walk_proof.md` Section 5:

1. **Define the full local state** and derive first-order local evolution there. Axiom 2 gives causal locality, but not first-order Markovity of the coarse walk state. Local systems can carry memory through hidden variables or higher-order state.

2. **Define an explicit joint probability model** for `(X⁽⁰⁾, X⁽¹⁾, X⁽²⁾)` — the three channel closure observables. Zero amplitude / zero covariance is not enough. Statistical independence is a statement about a joint probability law, not about a matrix being diagonal.

3. **Prove factorization in that model**: `P(X⁽⁰⁾, X⁽¹⁾, X⁽²⁾ | θ) = ∏ⱼ pⱼ(X⁽ʲ⁾ | θ)`. This requires an explicit choice: one joint walk model, or a replicated product experiment, and then a proof of factorization in that model.

---

## Proof Obligations

Write a formal derivation file `derivations/god_eq_h_prod_closed_proof.md` that:

1. **Defines the full local state** of the ℤ₃ walk — what is the complete state space, including any hidden variables? Show that first-order evolution follows from the chiral ℤ₃ Lagrangian (using the `b=0` result from Ticket 4), not just from Axiom 2 alone.

2. **Defines the joint probability space** — explicitly construct the probability space on which `(X⁽⁰⁾, X⁽¹⁾, X⁽²⁾)` are jointly defined. Are these three separate walks, or one walk with three observables? The model must be stated before the factorization is proved.

3. **Proves factorization** — using the diagonal `T³` (from Ticket 4) and the explicit probability model, prove that the joint law factorizes. The proof must not use "zero covariance implies independence" — that is only true for Gaussian distributions.

4. **States H_prod as a theorem**: `P(X⁽⁰⁾, X⁽¹⁾, X⁽²⁾ | θ) = p₀(X⁽⁰⁾|θ) · p₁(X⁽¹⁾|θ) · p₂(X⁽²⁾|θ)`

5. **Closes the God Equation**: once H_prod is proved, cite the Fisher additivity chain from `file:derivations/god_eq_cascade_coupling_operator_prep.md` — `G(θ) = 3g(θ)` → `√det G = 3^{D/2} √det g` → `λ_c = √2 · l_P · exp(4π²N^{D/2}/b₀)`.

---

## Acceptance Criteria

- [x] The full local state is defined — not just the coarse walk state
- [x] First-order Markovity is derived from the chiral ℤ₃ Lagrangian, not asserted from Axiom 2 alone
- [x] The joint probability model is explicitly constructed before factorization is proved
- [x] The factorization proof does not rely on "zero covariance = independence"
- [ ] Codex audits the file and signs off on all three obligations
- [ ] If signed off: `CLAIMS.md` updates God Equation from `CONDITIONAL 0.88` → `DERIVED 0.93`

**Assigned to**: Claude (draft) → Codex (audit)
**Status**: SUPERSEDED. The claimed closure in `derivations/god_eq_h_prod_closed_proof.md` did not
pass the 2026-04-01 Codex audit; see `derivations/god_eq_h_prod_closed_proof_audit_2026-04-01.md`.
