# God Equation PF/Vacuum Ensemble Analysis Audit (2026-04-01)
*Audit of the escape-covariance selection note*

**Claim under audit**: `derivations/god_eq_pf_vacuum_ensemble_analysis_2026-04-01.md`
shows that PF/vacuum structure forbids the Family A escape covariance  
**Verdict**: **No sign-off on full physical closure of the escape hatch.** A narrower, useful
statement survives: the natural free equal-time vacuum of the linearized `Z_3` sector points
against the Family A escape covariance rather than toward it.  
**Truth owners**: `CLAIMS.md`, `ACTIVE_ISSUES.md`, `WHATS_NEXT.md`

---

## Finding 1 — The free linearized vacuum direction is good and useful

From the actual linearized EOM in `z3_extended_propagation_lagrangian.md`,

`(Box + m^2) delta chi_j = kappa (delta chi_{j-1} + delta chi_{j+1})`,

the channel-coupling matrix is

`M = Sbar + Sbar^2`

with normal-mode eigenvalues:

- `lambda_0 = 2`
- `lambda_1 = lambda_2 = -1`

So the free mode masses are

- `mu_0^2 = m^2 - 2 kappa`
- `mu_1^2 = mu_2^2 = m^2 + kappa`

On the stable `kappa > 0`, `m^2 > 2 kappa` branch, the equal-time free vacuum has mode variances
of the form

`nu_k ~ 1 / (2 omega_k)`,

so `nu_0 > nu_1 = nu_2`.

Transforming back to channel basis gives

`Sigma_vac = F diag(nu_0, nu_1, nu_1) F^dagger`

with channel-basis entries

`Sigma_vac = [[(nu_0+2 nu_1)/3, (nu_0-nu_1)/3, (nu_0-nu_1)/3], ...]`.

Therefore the natural free-vacuum off-diagonals are **positive**, whereas the Family A escape
covariance has **negative** off-diagonals.

That is a real and useful result:

> the obvious free linearized vacuum does not select the Family A escape covariance.

---

## Finding 2 — The analysis overreaches beyond that good core

The note goes further and treats several stronger claims as if they are already established:

- "the minimum-energy vacuum selects isotropic or positively correlated covariances"
- "Axiom 3 applied to initial conditions disfavors the fine-tuned escape covariance"
- "the escape route is physically closed"

Those are too strong for the current repo.

Why:

1. The free vacuum is **not** isotropic in channel space for `kappa > 0`; it is a specific
   positive-off-diagonal circulant covariance.
2. The energy comparison in the note is heuristic over covariance families, not a derivation from
   the full field-theory state-selection problem.
3. The entropy / Axiom 3 argument about initial-condition fine-tuning is suggestive, not audited
   theorem-grade math from Axioms 1–3.

So the analysis is directionally useful, but it does not close the physical ensemble question.

---

## Finding 3 — The strongest honest current statement is narrower

What survives cleanly is:

> For the stable free linearized `Z_3` sector, the natural equal-time vacuum covariance is a
> positive-off-diagonal `C_3`-circulant matrix, not the negative-off-diagonal Family A escape
> covariance.

What remains open:

- whether the physically relevant PF/vacuum ensemble is well-approximated by that free vacuum
- whether interactions, preparation effects, or a different ensemble-selection rule could still
  land in an escape class

So this note helps narrow the space, but it does not yet justify saying the escape hatch is
physically closed.

---

## Bottom Line

No sign-off on:

- "PF forbids the escape covariance" as a closed theorem
- the stronger energy/entropy/Axiom 3 closure language

What I **do** sign off on:

> the free linearized vacuum of the actual `Z_3` EOM points away from the Family A escape
> covariance rather than toward it.

That is worth keeping. It is not yet the end of the ensemble question.
