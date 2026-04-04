# God Equation — Exact Free Linearized `\mathbb{Z}_3` Vacuum Propagator (2026-04-01)
*Bounded exact note for the channel-basis vacuum covariance on the actual `\mathbb{Z}_3` linearized sector*

**Status**: Exact math note, bounded to the free linearized sector  
**Purpose**: Derive the equal-time vacuum covariance exactly and state what it does and does not say
about the Family A escape covariance.  
**Truth sources**:
- `CLAIMS.md`
- `ACTIVE_ISSUES.md`
- `WHATS_NEXT.md`
- `derivations/g3_closure_card_2026-04-01.md`
- `derivations/z3_extended_propagation_lagrangian.md`
- `derivations/god_eq_pf_vacuum_ensemble_analysis_2026-04-01.md`
- `derivations/god_eq_pf_vacuum_ensemble_analysis_audit_2026-04-01.md`
- `derivations/god_eq_path_b_family_a_intensity_audit_2026-04-01.md`

---

## 0. Assumptions and Scope

This note is deliberately narrow.

It assumes only:

1. the **free linearized** internal `\mathbb{Z}_3` sector from
   `z3_extended_propagation_lagrangian.md`
2. the channel-space equation of motion

   `(\Box + m^2)\,\delta\chi_j = \kappa(\delta\chi_{j-1} + \delta\chi_{j+1})`

3. the stable branch

   `m^2 > 2\kappa > 0`

4. the standard equal-time free-vacuum covariance for each normal mode

   `\nu_k(|p|) = 1/(2\omega_k(|p|))`

This note does **not** claim:

- that the full nonlinear PF vacuum is proved to equal this free vacuum
- that every physically admissible ensemble is therefore fixed
- that the Family A escape hatch is physically closed in full generality

It only derives the exact free linearized vacuum covariance and compares its sign structure with the
known Family A escape covariance.

---

## 1. Why This File Exists

The earlier PF/vacuum ensemble note contained one useful core result and several stronger claims
that were not signed off.

What survived audit was narrower:

> the natural free equal-time vacuum of the linearized `\mathbb{Z}_3` sector points away from the
> Family A escape covariance rather than toward it.

This file isolates exactly that surviving statement.

---

## 2. Channel-Space Linearized Dynamics

From `z3_extended_propagation_lagrangian.md`, the linearized internal equations of motion are

`(\Box + m^2)\,\delta\chi_j = \kappa(\delta\chi_{j-1} + \delta\chi_{j+1})`

with channel labels taken mod `3`.

Write the channel vector as

`f = (\delta\chi_0,\delta\chi_1,\delta\chi_2)^T`.

Then

`(\Box + m^2) f = \kappa M f`

with

`M = \bar S + \bar S^2`

and

` \bar S = [[0,0,1],[1,0,0],[0,1,0]],   \bar S^2 = [[0,1,0],[0,0,1],[1,0,0]] `.

So explicitly

`M = [[0,1,1],[1,0,1],[1,1,0]]`.

This is the same `\mathbb{Z}_3` coupling matrix that underlies the actual symmetric closure route.

---

## 3. Exact Normal-Mode Diagonalization

Use the discrete Fourier transform matrix

`F = (1/sqrt(3)) [[1,1,1],[1,\omega,\omega^2],[1,\omega^2,\omega]]`

with

`\omega = e^{2\pi i/3}`.

Then

`F^\dagger M F = diag(2,-1,-1)`.

So the channel coupling eigenvalues are

- `\lambda_0 = 2`
- `\lambda_1 = \lambda_2 = -1`

If the Fourier-mode amplitudes are `\tilde\chi_k`, then each mode satisfies

`(\Box + \mu_k^2)\tilde\chi_k = 0`

with exact effective masses

- `\mu_0^2 = m^2 - 2\kappa`
- `\mu_1^2 = \mu_2^2 = m^2 + \kappa`

On the stable branch `m^2 > 2\kappa > 0`, all three mode masses are positive.

---

## 4. Equal-Time Free Vacuum Covariance

For fixed spatial momentum magnitude `|p|`, define

- `\omega_0(|p|) = sqrt(|p|^2 + m^2 - 2\kappa)`
- `\omega_1(|p|) = sqrt(|p|^2 + m^2 + \kappa)`

and therefore

- `\nu_0(|p|) = 1/(2\omega_0(|p|))`
- `\nu_1(|p|) = 1/(2\omega_1(|p|))`

with `\nu_2 = \nu_1`.

In the normal-mode basis the equal-time free vacuum covariance is

`diag(\nu_0,\nu_1,\nu_1)`.

Transforming back to the channel basis gives

` \Sigma_vac(|p|) = F diag(\nu_0,\nu_1,\nu_1) F^\dagger `.

Carrying out the multiplication yields the exact `C_3`-circulant matrix

` \Sigma_vac = [[(\nu_0+2\nu_1)/3, (\nu_0-\nu_1)/3, (\nu_0-\nu_1)/3],
                [(\nu_0-\nu_1)/3, (\nu_0+2\nu_1)/3, (\nu_0-\nu_1)/3],
                [(\nu_0-\nu_1)/3, (\nu_0-\nu_1)/3, (\nu_0+2\nu_1)/3]] `.

So:

- diagonal entry: `d = (\nu_0 + 2\nu_1)/3`
- off-diagonal entry: `o = (\nu_0 - \nu_1)/3`

This is the exact free equal-time channel covariance on the linearized `\mathbb{Z}_3` sector.

---

## 5. Stable-Branch Sign Structure

On the stable branch:

`m^2 - 2\kappa < m^2 + \kappa`

so for every fixed `|p| >= 0`,

`\omega_0(|p|) < \omega_1(|p|)`.

Since `x -> 1/(2x)` is strictly decreasing for `x > 0`, this implies

` \nu_0(|p|) > \nu_1(|p|) `.

Therefore the channel-basis off-diagonal entry satisfies

` o = (\nu_0 - \nu_1)/3 > 0 `.

So the exact free linearized vacuum covariance has:

- positive diagonal entries
- positive off-diagonal entries
- full `C_3` symmetry

This is the central surviving result.

---

## 6. Comparison with the Family A Escape Covariance

The Family A intensity audit identified the whitening covariance

` \Sigma_escape = (A A^T)^{-1},   A = T_sym^3 `

with sign pattern

` \Sigma_escape \propto [[43,-21,-21],[-21,43,-21],[-21,-21,43]] `.

So:

- `\Sigma_vac` has **positive** off-diagonal entries
- `\Sigma_escape` has **negative** off-diagonal entries

Hence the free linearized vacuum points in the opposite sign direction from the Family A escape
covariance.

This supports the narrower audited statement:

> the obvious free linearized vacuum does not naturally select the Family A escape covariance.

It does **not** by itself prove that every physically admissible PF ensemble is excluded from the
escape class.

---

## 7. Regime Analysis

### 7.1 Decoupled limit `\kappa -> 0`

Let

`\Omega(|p|) = sqrt(|p|^2 + m^2)`.

Then as `\kappa -> 0`,

- `\omega_0 -> \Omega`
- `\omega_1 -> \Omega`
- `\nu_0 -> 1/(2\Omega)`
- `\nu_1 -> 1/(2\Omega)`

and therefore

` \Sigma_vac(|p|) -> (1/(2\Omega(|p|))) I `.

So the channels become decoupled and isotropic in the channel basis in the zero-coupling limit.

### 7.2 Small-coupling expansion

For fixed `|p|`, let `\Omega = sqrt(|p|^2 + m^2)`.

To first order in `\kappa`,

- `\nu_0 = 1/(2\Omega) + \kappa/(2\Omega^3) + O(\kappa^2)`
- `\nu_1 = 1/(2\Omega) - \kappa/(4\Omega^3) + O(\kappa^2)`

Therefore

- `d = (\nu_0 + 2\nu_1)/3 = 1/(2\Omega) + O(\kappa^2)`
- `o = (\nu_0 - \nu_1)/3 = \kappa/(4\Omega^3) + O(\kappa^2)`

So the leading correction is purely off-diagonal:

` \Sigma_vac(|p|) = (1/(2\Omega)) I + (\kappa/(4\Omega^3)) M + O(\kappa^2) `.

This makes the positive-correlation direction explicit.

### 7.3 Stability edge `\kappa -> m^2/2`

At zero spatial momentum,

`\omega_0(0) = sqrt(m^2 - 2\kappa)`,

so as `\kappa -> m^2/2` from below,

`\nu_0(0) = 1/(2 sqrt(m^2 - 2\kappa)) -> \infty`.

This is the expected soft-mode divergence of the `k=0` channel at the stability edge.

For fixed nonzero `|p|`, the same limit gives

`\omega_0(|p|) -> |p|`,

so the divergence is specifically an infrared / zero-momentum effect rather than a uniform
pointwise blow-up at every fixed `|p|`.

For that reason, conclusions in this note are restricted to the stable interior

`m^2 > 2\kappa > 0`.

---

## 8. What This Note Does and Does Not Settle

### Settled here

1. the exact normal-mode spectrum of the free linearized `\mathbb{Z}_3` channel operator
2. the exact channel-basis free equal-time covariance
3. the sign of the off-diagonal channel correlations on the stable branch
4. the fact that this sign points away from the Family A escape covariance

### Not settled here

1. whether the physically relevant PF ensemble is exactly this free vacuum
2. whether interactions or preparation effects could generate a different admissible ensemble
3. whether a broader escape class remains available for Path B or Family C
4. any closure of `H_prod`

So this note is a pressure result, not a final ensemble theorem.

---

## 9. Strongest Honest Current Statement

For the free linearized `\mathbb{Z}_3` sector on the stable branch,

` \Sigma_vac(|p|) = [[(\nu_0+2\nu_1)/3, (\nu_0-\nu_1)/3, (\nu_0-\nu_1)/3], ...] `

with

` \nu_0 > \nu_1 `,

so the natural equal-time channel covariance has **positive** off-diagonal entries.

Since the Family A escape covariance has **negative** off-diagonal entries, the free linearized
vacuum points away from that escape structure rather than toward it.

That is the exact result worth keeping.
