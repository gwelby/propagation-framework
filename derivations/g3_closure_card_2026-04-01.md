# G3 Closure Card (2026-04-01)
*Shortest honest map from the current God Equation status to either closure or failure*

**Status**: Planning / closure map  
**Purpose**: Keep the God Equation front bounded to its actual remaining proof obligations.  
**Truth sources**: `CLAIMS.md`, `ACTIVE_ISSUES.md`, `derivations/lambda_c_from_axioms.md`, `derivations/god_equation_gap_status.md`, `derivations/god_eq_gap_B_nearest_neighbor_no_go.md`

---

## Claim

PF derives

`lambda_c = sqrt(2) l_P exp(4 pi^2 N^(D/2) / b_0)`

from its own internal generation structure and coherence dynamics.

---

## Live Status

`CONDITIONAL 0.88`

The numerical lock is strong.
The theorem is not closed.

---

## What Survives

- the numerical prediction for `lambda_c` remains strong
- the `Z_3`-extended Lagrangian gives a genuine three-channel internal sector
- the circulant coupling structure is real
- the symmetric nearest-neighbor closure shortcut has now been cleanly falsified rather than left vague
- the chiral-vs-symmetric hardware result is meaningful evidence for identity preservation

These are real supports.
None of them, by themselves, prove `H_prod`.

---

## Exact Missing Bridges

The live owner docs now localize the front to three connected gaps:

1. **Markov / primitive-operator gap**
   Axiom 2 gives causal locality, but not first-order Markovity of the coarse walk state.

2. **Actual closure-object gap**
   The symmetric nearest-neighbor story does not give

   `T_eff = K^3 · I`

   except in the pure-shift ansatz.
   That shortcut is dead for the actual symmetric operator.

3. **Probability / factorization gap**
   Zero cross-channel covariance or amplitude is weaker than full joint-law factorization.
   So `H_prod` is still not proved.

The historical coherence-volume and product-walk language still matters as part of the longer derivation story, but the live freeze point is now sharper than that:

> write the actual closure operator and the actual probability model, then prove factorization or fail.

---

## Why It Matters

This is the load-bearing scale bridge in the repo.
If it closes honestly, the framework gains a real theorem-level hierarchy result.
If it fails, the framework still benefits because one of its most tempting overreach zones becomes permanently bounded.

---

## Shortest Route To Closure

Choose one path only.
Do not mix them.

### Path A. Chirality selection

Do not aim this route at `b = 0` anymore.

The audited `chiral_projection_z3.py` result is weaker and more specific:

- the projected left-handed sector kills the `k = 2` Fourier eigenmode
- it does **not** eliminate the `\bar{S}^2` term in position space
- `|beta/alpha| = 1`, so the projected operator is not a pure shift

So the live Path A question is:

> if the `Z_3` Lagrangian really forces the projected `{k=0,k=1}` sector, does closure in that 2D Fourier sector imply the position-space probability factorization required for `H_prod`?

In current shorthand:

- derive whether the physics really forces the projected `{k=0,k=1}` sector
- if yes, write the exact closure object in that sector
- then prove or refute the bridge from Fourier-basis closure to position-space factorization for `H_prod`

### Path B. Actual non-diagonal closure

Accept the real closure object instead of trying to diagonalize it away.

Then:

- write the explicit probability law on that actual walk
- define factorization on the real closure object rather than the dead shortcut
- prove or refute `H_prod` there

Current narrowing:

- the normalized intensity-fraction reading is already a restricted no-go
- the direct raw local intensity reading is now a strong restricted no-go candidate under a broad
  iid exchange-symmetric ensemble class
- the tested integrated readouts fail strongly, and the natural antisymmetric edge-flux current is
  now an exact no-go because its three channel observables satisfy `J^(0)+J^(1)+J^(2)=0`
- so the clean surviving subroutes are now Family C quadratic closure functionals or genuinely new
  nonquadratic one-medium observables

---

## Shortest Route To Failure

- prove that the `Z_3` Lagrangian does not force the projected `{k=0,k=1}` sector, so Path A cannot start
- or show that Fourier-basis closure in the projected sector does not imply the position-space factorization that `H_prod` needs
- or show that for the actual closure operator the required joint-law factorization fails generically
- or show that any proof of `H_prod` would need assumptions stronger than the `Z_3` Lagrangian plus Axioms 1-3

Any one of those would kill the current closure route honestly.

---

## Do Not Say Yet

- "the IBM result closes the God Equation"
- "`H_prod` is proved"
- "Axiom 2 implies Markovity"
- "the number is too good for the bridge to be wrong"

---

## Boundary Conditions For New Work

New G3 work should be admitted only if it does one of these:

- sharpens the primitive closure operator
- sharpens the explicit probability model
- proves or falsifies factorization on the actual closure object

New G3 work should be deferred if it only does one of these:

- adds more broad numerics
- retells the historical product-walk story without reducing a proof obligation
- treats covariance-level support as independence-level closure

---

## Strongest Honest Summary

The God Equation front is no longer waiting for "more intuition."
It is waiting for one exact thing:

> a real closure operator plus a real probability model strong enough to prove `H_prod`, or strong enough to show that the current route fails.

That is the closure card.
