# QWEN — Exact Free Linearized ℤ₃ Vacuum Propagator for G3

## Your Job

Derive the exact free linearized vacuum two-point function for the `\mathbb{Z}_3` internal sector
used in the God Equation Path B discussion.

Write:

- `derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md`

This is a bounded math note, not a philosophy note.

---

## Why This Matters

The current Path B picture includes this pressure statement:

> the free linearized vacuum points away from the Family A whitening covariance

That is useful, but still too compressed.

We need the exact derivation on disk.

The question is:

> for the linearized `\mathbb{Z}_3` coupled sector, what covariance does the natural free vacuum
> actually induce in the channel basis, and how does that compare to the mathematical escape
> covariance used in the Family A discussion?

---

## Read First

- `CLAIMS.md`
- `ACTIVE_ISSUES.md`
- `WHATS_NEXT.md`
- `derivations/god_eq_pf_vacuum_ensemble_analysis_2026-04-01.md`
- `derivations/god_eq_pf_vacuum_ensemble_analysis_audit_2026-04-01.md`
- `derivations/god_eq_path_b_family_a_intensity_audit_2026-04-01.md`
- `z3_extended_propagation_lagrangian.md`

---

## Exact Deliverable

Your note must include:

1. **The linearized coupled EOM**
   Write the channel-space operator explicitly.

2. **Normal-mode diagonalization**
   Derive the eigenmodes and eigenvalues of the `\mathbb{Z}_3` coupling matrix.

3. **Mode frequencies**
   Show the exact frequency structure, e.g. the `k=0` and `k=1,2` split, with all sign
   conventions stated.

4. **Equal-time vacuum covariance**
   Derive the covariance in the normal-mode basis, then transform it back to the channel basis.

5. **Sign structure**
   State explicitly whether the off-diagonal channel correlations are:
   - zero
   - positive
   - negative

6. **Comparison with the Family A escape covariance**
   Compare the natural vacuum covariance with the whitening covariance used in the Family A
   discussion.
   Do not just say "different" — compare the sign pattern and structure.

7. **Regime analysis**
   State what happens when:
   - `\kappa -> 0`
   - `\kappa` is small relative to `m`
   - `\kappa` approaches the stability edge

8. **Exact honest conclusion**
   End with one of:
   - "the free linearized vacuum points away from the Family A escape covariance"
   - "the free linearized vacuum can approach it in a specific regime"
   - or another exact statement if the math forces it

---

## Non-Goals

Do not do any of these:

- do not claim PF fully forbids every escape ensemble
- do not invoke entropy/coherence/energy-selection language unless derived in the note
- do not edit `CLAIMS.md`, `ACTIVE_ISSUES.md`, or `WHATS_NEXT.md`
- do not broaden from the free linearized vacuum to full nonlinear PF unless the bridge is explicit

---

## Acceptance Criteria

- [ ] Exact channel-space covariance matrix written
- [ ] Sign pattern of off-diagonals stated explicitly
- [ ] Comparison to the Family A whitening covariance is explicit
- [ ] Limiting regimes are stated cleanly
- [ ] Final claim is narrower than or equal to what the math supports

---

## Why This Helps Codex

If this note is clean, Codex can answer a very specific question:

> does the natural free vacuum support the existing Path B no-gos, or is there a mathematically
> natural escape ensemble still in play?

That is the only question this note needs to answer.
