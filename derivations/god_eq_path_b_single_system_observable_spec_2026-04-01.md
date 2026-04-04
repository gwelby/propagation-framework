# God Equation Path B: Single-System Observable Spec (2026-04-01)
*Bounded theorem target for the next honest `H_prod` attempt on one three-channel medium*

**Status**: Working spec, not a proof  
**Purpose**: Define what a physically acceptable single-system Path B probability model must look
like before anyone can claim `H_prod` from the actual non-diagonal closure object.  
**Truth sources**: `CLAIMS.md`, `ACTIVE_ISSUES.md`,
`god_eq_h_prod_model_routes_audit_2026-04-01.md`,
`god_eq_h_prod_closed_proof_audit_2026-04-01.md`, `g3_closure_card_2026-04-01.md`,
`h_prod_markovian_walk_proof.md`, `g3_product_walk_no_go.md`,
`z3_extended_propagation_lagrangian.md`

---

## 1. Why This File Exists

Path B is now the more literal God Equation route:

- keep the actual non-diagonal closure object
- keep one medium with three internal channels
- write an explicit joint probability law there
- prove or refute `H_prod` there

The 2026-04-01 route audit already killed the most naive single-system reading:

- if one 3-step closure trial ends in one final channel label `Y in {0,1,2}`
- and `X^(r) = 1[Y = r]`
- then the indicators are mutually exclusive, so factorization fails immediately

That is useful, but not enough.

This file names the next honest target:

> define observables on one three-channel medium that are not one-hot by construction, are
> physically tied to the actual `kappa`-coupled closure object, and are strong enough to make
> `H_prod` a real theorem target rather than a replicated-experiment artifact.

---

## 2. Exact Target

We need a probability space `(Omega, P_theta)` for one medium at fixed external parameter `theta`
and three measurable observables

`X^(0), X^(1), X^(2) : Omega -> S`

such that:

1. the observables are all defined on the **same** trial of the **same** system
2. the observables are channel-resolved in a physically meaningful way
3. the induced joint law is not built in by replication or separate preparation
4. `H_prod`

   `P_theta(X^(0), X^(1), X^(2)) = prod_j p_j(X^(j) | theta)`

   is a substantive claim, not a tautology

If the microstate collapses to a single categorical label per trial, Path B fails immediately.

So any viable one-system Path B model must expose **simultaneous channel information** at closure,
not just a single final-channel choice.

---

## 3. Admissibility Tests

A candidate Path B observable family is admissible only if it passes all five tests:

### Test A — One-system support

All three observables must be defined on one probability space for one medium.

Disallow:

- "channel 0 trial", "channel 1 trial", "channel 2 trial" as separate experiments
- product measures introduced by hand from replicated preparations

### Test B — Non-one-hot support

The support cannot force a relation like

`X^(0) + X^(1) + X^(2) = const`

that makes independence impossible before the dynamics are even examined.

### Test C — Physical readout

The observables must be tied to actual field or closure variables of the `Z_3` medium:

- channel amplitudes
- channel intensities
- channel currents
- closure functionals of the actual `kappa`-coupled operator

not just a convenient abstract randomization.

### Test D — Actual-operator dependence

The law must be computed from the actual non-diagonal closure object or the actual linearized EOM,
not from the dead pure-shift shortcut.

### Test E — Independence strength

Zero covariance, zero off-diagonal amplitude, or orthogonality is not enough.

The target is full joint-law factorization.

---

## 4. Immediate No-Go Family

### Family 1 — Final-channel one-hot indicators

Let one closure trial produce one final channel label

`Y in {0,1,2}`

and define

`X^(r) = 1[Y = r]`.

Then automatically

`X^(0) + X^(1) + X^(2) = 1`

on every trial.

Under the normalized symmetric closure object

`T_sym^3 = (1/4) I + (3/8) Sbar + (3/8) Sbar^2`

the marginals are nontrivial, for example from start channel `0`:

- `P(Y=0) = 1/4`
- `P(Y=1) = 3/8`
- `P(Y=2) = 3/8`

but

`P(X^(0)=1, X^(1)=1, X^(2)=1) = 0`

while the product of marginals is

`(1/4)(3/8)(3/8) = 9/256 > 0`.

So this family is permanently excluded as a Path B closure route.

### Family 2 — Replicated per-start return indicators

Define one return indicator per separately prepared start channel.

That is mathematically clean, but it is no longer a one-system theorem.

It may remain a useful auxiliary experiment model, but it does **not** close `H_prod` for one
three-channel medium.

---

## 5. Candidate Observable Families Still Worth Testing

These are not sign-offs. They are only the remaining admissible families.

### Family A — Closure-time channel intensities

Candidate form:

`X^(r) = F_r(|chi_0|^2, |chi_1|^2, |chi_2|^2)`

at the closure scale.

What changed on 2026-04-01:

- the natural normalized subfamily is now a restricted no-go:
  `god_eq_path_b_intensity_fraction_no_go_2026-04-01.md`
- if `X^(r)` is the normalized channel fraction at closure, then
  `X^(0) + X^(1) + X^(2) = 1` almost surely, so factorization forces degeneracy

What is still missing:

- whether a non-normalized intensity readout is physically justified
- a measurement map from raw field amplitudes to probabilities
- proof that the resulting joint law is the right God Equation observable

### Family B — Integrated channel currents over the closure window

Candidate form:

`X^(r) = G_r(J_r(t))` integrated over the 3-step closure period.

Why this survives initial screening:

- it uses dynamical information rather than only final labels
- it can encode simultaneous channel activity

What is still missing:

- an explicit path-space or trajectory law for the `kappa`-coupled system
- proof that these currents are the right closure observables for `H_prod`

### Family C — Quadratic closure functionals of the actual operator

Candidate form:

`X^(r) = H_r(T^3, psi_0)`

with `T^3` the actual non-diagonal closure object.

Why this survives initial screening:

- it is built directly from the real closure operator
- it avoids pretending the operator is diagonal

What is still missing:

- a concrete map from operator-valued closure to classical observables on one probability space
- proof that the joint law is not just a rephrased covariance statement

---

## 6. Families That Do Not Count As Closure

The following may still be useful side calculations, but they do **not** close Path B:

- Fourier-mode occupation alone
  - useful for Path A, but not enough unless it is bridged back to one-medium channel observables
- covariance-level support
  - weaker than factorization
- entropy reduction alone
  - evidence for selection, not proof of independence
- IBM identity-preservation data alone
  - evidence for chirality selection, not proof of `H_prod`

---

## 7. Minimal Work Program

Any new Path B derivation should follow this order:

1. **Choose one admissible observable family only**
   Do not mix replicated trials with one-system observables.

2. **Define the microstate at closure**
   What exactly is random on one trial of one medium?

3. **Define the readout map**
   How do `chi`, `T^3`, or the path variables produce `X^(0), X^(1), X^(2)`?

4. **Check support constraints first**
   If the support already forces dependence, stop.

5. **Compute the joint law under the actual `kappa`-coupled dynamics**
   Not under the pure-shift shortcut.

6. **Only then test factorization**
   If factorization fails generically, Path B should be downgraded further or killed.

---

## 8. Upgrade / Kill Criteria

### Path B upgrades only if

- the observables live on one medium and one probability space
- they are not one-hot or support-constrained by definition
- the law is derived from the actual `kappa`-coupled closure object
- factorization survives there

### Path B dies if

- every admissible one-system observable family inherits a support constraint that blocks
  independence
- only replicated experiments factorize
- the required measurement law is ad hoc rather than forced by the model

---

## Strongest Honest Current Statement

The next real Path B question is no longer:

> can we say "independence" loudly enough to make the God Equation close?

It is:

> what observables can one medium actually carry at closure, and does their joint law factorize
> under the actual non-diagonal `kappa`-coupled dynamics?

Until that is answered, `H_prod` stays open.
