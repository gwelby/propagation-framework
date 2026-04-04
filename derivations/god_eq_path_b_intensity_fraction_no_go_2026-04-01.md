# God Equation Path B — Restricted No-Go for Normalized Intensity Fractions (2026-04-01)
*Why the most natural one-medium intensity readout cannot satisfy nontrivial `H_prod`*

**Date**: 2026-04-01  
**Author**: Codex  
**Task**: Test the first admissible Path B observable family from
`god_eq_path_b_single_system_observable_spec_2026-04-01.md`  
**Status**: RESTRICTED NO-GO — kills the normalized intensity-fraction subfamily, not all Path B
intensity models  
**Builds on**: `god_eq_h_prod_model_routes_audit_2026-04-01.md`,
`god_eq_path_b_single_system_observable_spec_2026-04-01.md`,
`z3_extended_propagation_lagrangian.md`, `god_eq_gap_B_nearest_neighbor_no_go.md`

---

## 1. Why This File Exists

The Path B observable spec kept **closure-time channel intensities** alive as the first serious
one-medium candidate family:

`X^(r) = F_r(|chi_0|^2, |chi_1|^2, |chi_2|^2)`

That family was still too broad.

The most natural physical reading is the normalized fraction carried by each channel at closure:

`X^(r) = I_r / (I_0 + I_1 + I_2)`,  where `I_r >= 0`.

This file checks that exact subfamily.

---

## 2. The Candidate Readout

Let one closure trial of one three-channel medium produce nonnegative channel intensities

`I_0, I_1, I_2 >= 0`.

Define the normalized closure fractions

`X^(r) = I_r / (I_0 + I_1 + I_2)`.

Then automatically:

1. `X^(r) >= 0` for all `r`
2. `X^(0) + X^(1) + X^(2) = 1` almost surely

This is the most natural way to turn simultaneous channel support into a one-system probability
vector.

---

## 3. Main Theorem

### Theorem

Let `X^(0), X^(1), X^(2)` be random variables on one probability space such that

- `X^(r) >= 0`
- `X^(0) + X^(1) + X^(2) = 1` almost surely

If their joint law factorizes:

`P_theta(X^(0), X^(1), X^(2)) = prod_j p_j(X^(j) | theta)`,

then each `X^(r)` is almost surely constant.

So a nontrivial normalized intensity-fraction model cannot satisfy `H_prod`.

### Proof

Because the sum is constant,

`Var_theta(X^(0) + X^(1) + X^(2)) = 0`.

If the joint law factorizes, the three variables are independent. Therefore

`Var_theta(X^(0) + X^(1) + X^(2)) = Var_theta(X^(0)) + Var_theta(X^(1)) + Var_theta(X^(2))`.

So

`Var_theta(X^(0)) + Var_theta(X^(1)) + Var_theta(X^(2)) = 0`.

Each variance is nonnegative, hence each variance must be zero:

`Var_theta(X^(r)) = 0` for all `r`.

Therefore each `X^(r)` is almost surely constant.

`square`

---

## 4. What This Means For Path B

This does **not** prove that all intensity-based Path B models fail.

It proves the narrower and important statement:

> If the one-medium closure observables are the normalized channel fractions, then `H_prod`
> factorization is impossible unless the model is degenerate.

That kills the most natural probability-vector reading of simultaneous channel occupancy.

So the normalized-fraction route does not close `H_prod`.

---

## 5. Concrete Check Against the Actual Closure Object

For the normalized symmetric closure operator from the actual nearest-neighbor circulant route,

`T_sym = (1/2)(Sbar + Sbar^2)`,

the 3-step closure object is

`T_sym^3 = (1/4) I + (3/8) Sbar + (3/8) Sbar^2`.

From a basis start in channel `0`, the closure fractions are

`(1/4, 3/8, 3/8)`.

They already satisfy the shared-total constraint

`1/4 + 3/8 + 3/8 = 1`.

So if one tries to interpret these as the simultaneous one-medium channel probabilities, the only
factorized case would be a degenerate law concentrated at one constant triple.

That is not the nontrivial statistical bridge Path B was trying to produce.

---

## 6. What Survives

The broader intensity family splits into two branches:

### Killed

- normalized closure-time channel fractions

### Still open

- raw, unnormalized channel intensities
- integrated channel currents
- quadratic closure functionals of the actual operator

But any surviving intensity route must now explain why the readout is **not** the normalized
probability vector that the medium naturally presents.

---

## 7. Upgrade / Kill Criteria

### This no-go upgrades to a broader Family A no-go only if

- every physically acceptable intensity readout reduces to normalized fractions or another
  fixed-total representation

### Path B intensity routes survive only if

- they use a non-normalized readout with a justified measurement law
- they live on one medium and one probability space
- they still test factorization on the actual `kappa`-coupled closure object

---

## Strongest Honest Current Statement

The first Path B family did not close.

More precisely:

> the most natural one-medium intensity readout, normalized channel fractions at closure, is a
> restricted no-go for nontrivial `H_prod`.

Path B remains open, but the next honest candidates are now narrower than before.
