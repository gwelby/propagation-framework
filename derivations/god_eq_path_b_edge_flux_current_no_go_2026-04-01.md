# God Equation Path B — Antisymmetric Edge-Flux Current No-Go (2026-04-01)
*Exact obstruction for the remaining natural current-family observable on the symmetric `\mathbb{Z}_3` closure route*

**Status**: **NO-GO** for this observable family  
**Author**: Codex (2026-04-01)  
**Scope**: actual symmetric closure dynamics `T_sym = (1/2)(\bar{S} + \bar{S}^2)` with
`chi(t_n) = T_sym^n chi(0)`  
**Truth sources**:
- `god_eq_path_b_family_b_integrated_currents_2026-04-01.md`
- `god_eq_path_b_family_b_integrated_currents_audit_2026-04-01.md`
- `god_eq_h_prod_model_routes_audit_2026-04-01.md`

---

## 0. Why This Note Exists

The Family B audit left one genuinely interesting current-style observable open:

`J^(r) = sum_{n=0}^2 [chi_r(t_n) chi_{r+1}(t_{n+1}) - chi_{r+1}(t_n) chi_r(t_{n+1})]`

This is the discrete antisymmetric edge-flux current between channels `r` and `r+1`. It is not a
squared-amplitude observable, so the earlier quadratic no-go did not automatically kill it.

This note closes that remaining current-family candidate exactly.

---

## 1. Setup

Use the actual symmetric step operator:

`T_sym = (1/2)(\bar{S} + \bar{S}^2)`

so that

`chi(t_n) = T_sym^n x`, with `x = chi(0)`.

The 3-step closure operator is

`T_sym^3 = [[1/4, 3/8, 3/8], [3/8, 1/4, 3/8], [3/8, 3/8, 1/4]]`.

For `r in {0,1,2}` define

`J^(r) = sum_{n=0}^2 [chi_r(t_n) chi_{r+1}(t_{n+1}) - chi_{r+1}(t_n) chi_r(t_{n+1})]`

with channel labels taken mod 3.

Because each term is bilinear in `x`, there is a symmetric kernel `K_r` such that

`J^(r) = x^T K_r x`.

Direct expansion gives:

`K_0 = [[ 3/8,    0,    3/16], [   0, -3/8, -3/16], [ 3/16, -3/16,    0]]`

`K_1 = [[   0,  3/16, -3/16], [3/16,  3/8,     0 ], [-3/16,   0,   -3/8]]`

`K_2 = [[-3/8, -3/16,    0 ], [-3/16,   0,   3/16], [   0,  3/16,  3/8]]`

These are exact.

---

## 2. Exact Support Constraint

Summing the three kernels gives

`K_0 + K_1 + K_2 = 0`.

Therefore

`J^(0) + J^(1) + J^(2) = x^T (K_0 + K_1 + K_2) x = 0`

for **every** initial state `x`.

This is stronger than a covariance statement. It is an exact support constraint on the observable
triple.

---

## 3. Consequence For `H_prod`

If `H_prod` is read as a nontrivial factorized one-medium joint law on the three channel
observables `(J^(0), J^(1), J^(2))`, this current family cannot realize it.

Reason:

1. `J^(0) + J^(1) + J^(2) = 0` almost surely.
2. If the three observables were independent and had finite second moments, then
   `Var(J^(0) + J^(1) + J^(2)) = Var(J^(0)) + Var(J^(1)) + Var(J^(2))`.
3. But the left-hand side is `0`, so each variance must be `0`.
4. Hence independence forces degeneracy.

So this observable family admits no nontrivial factorized law.

This is an **exact no-go** for the edge-flux current family. It does not depend on Gaussianity.
It depends only on:

- the actual symmetric `T_sym` dynamics
- the edge-flux definition above
- ordinary finite-moment probabilistic admissibility

---

## 4. Gaussian Probe (Consistency Check)

For centered real Gaussian input with covariance `sigma^2 I`,

`Cov(x^T A x, x^T B x) = 2 sigma^4 Tr(AB)`.

Applying that here gives the exact covariance matrix:

`Cov(J^(r), J^(r)) = 27/32 sigma^4`

`Cov(J^(r), J^(s)) = -27/64 sigma^4`, for `r != s`.

So the Gaussian probe confirms the same structure numerically:

- each current has nonzero variance
- different channel currents are negatively correlated
- the covariance matrix already reflects the exact identity `J^(0) + J^(1) + J^(2) = 0`

But the real obstruction is still the support constraint, not the Gaussian calculation.

---

## 5. What This Does And Does Not Kill

What this kills:

- the most natural remaining antisymmetric current-style observable on Path B

What this does not kill by itself:

- every imaginable nonquadratic Path B observable
- Family C operator-level closure functionals
- any future route that changes the observable family rather than reusing this current

So the honest update is:

> Family B's natural current candidates are now in serious trouble:
> B1 and B2 fail under the isotropic Gaussian probe, and the edge-flux current is an exact
> no-go because its three channel observables satisfy a deterministic sum-zero constraint.

---

## Bottom Line

The antisymmetric edge-flux current does **not** rescue Path B.

It fails more strongly than the earlier quadratic probes:

- not because its covariance has the wrong sign,
- but because the three channel currents are algebraically constrained by
  `J^(0) + J^(1) + J^(2) = 0`.

That makes nontrivial factorization impossible for this observable family.

The clean remaining Path B front is now:

- Family C (quadratic closure functionals of the operator), or
- genuinely new nonquadratic observables with an explicit one-medium probability law.
