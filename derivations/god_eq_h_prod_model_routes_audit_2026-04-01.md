# God Equation H_prod Model Routes Audit (2026-04-01)
*Q-A through Q-D on the post-chiral-audit Path A / Path B split*

**Claim under review**: whether the new `H_prod` route split materially advances the God Equation bridge  
**Status**: No sign-off on closure; bounded audit of the two surviving model classes  
**Truth sources**: `CLAIMS.md`, `ACTIVE_ISSUES.md`, `god_eq_h_prod_closed_proof.md`, `god_eq_gap_B_nearest_neighbor_no_go.md`, `z3_extended_propagation_lagrangian.md`, `sandbox/chiral_projection_z3.py`

---

## Verdict

`H_prod` remains open.

What improves:

- the route split is real and worth keeping
- the old fake closure proof is dead
- the remaining questions are now named more precisely

What does **not** improve yet:

- Model A is not killed, but its claimed zero-return obstruction was wrong for the actual projected operator
- Model B does not close, because the replicated product experiment is still not justified as the physical reading of one medium with three coupled channels
- the actual `kappa`-coupled closure object does not show a near-decoupled regime at the 3-step scale

---

## Finding 1 — Q-A only applies to the wrong operator class

The quick algebra proposed for Path A was:

`T = a Sbar + b Sbar^2`, kill the `k=2` eigenmode, infer `b = -a omega`, then conclude `a^3 + b^3 = 0`, hence `[T^3]_{jj} = 0`.

That algebra is internally correct **for that operator class**.

It is **not** the actual operator used in `chiral_projection_z3.py`.

The actual projected operator is

`T_L = P_L T_sym P_L`

with

- `P_L = P_0 + P_1`
- `T_sym = (1/2)(Sbar + Sbar^2)`

so it retains the static `k=0` sector and therefore has an identity component.

Numerically:

- `T_L = c I + a Sbar + b Sbar^2`
- `c = 1/6`
- `a = 5/12 + i sqrt(3)/12`
- `b = 5/12 - i sqrt(3)/12`

Its Fourier eigenvalues are:

- `1`
- `-1/2`
- `0`

Therefore the actual 3-step projected operator has diagonal entries

`[T_L^3]_{jj} = (1 + (-1/2)^3 + 0)/3 = 7/24`

not `0`.

Direct script-consistent computation gives:

- `diag(T_L^3) = 0.291666... = 7/24`

So the “zero return probability” claim is rejected for the actual projected operator.

---

## Finding 2 — Model A is still blocked, but by a basis bridge, not by zero return

The projected-sector route still has no accepted path from Fourier closure to the position-space factorization statement required by `H_prod`.

What survives:

- the projected `{k=0,k=1}` sector is a meaningful reduced sector candidate
- closure in that sector is diagonal in the Fourier description

What does not survive:

- the claim that the natural position-space closure observable is dead because return probability is zero

The real problem is weaker and more exact:

- Fourier-sector closure is not yet the same statement as position-space statistical factorization

Natural candidate observables such as:

- return to channel `j`
- projected-sector occupation
- relative phase
- eigenmode interference
- winding count

all fail one of two tests:

1. they stay native to the Fourier/projected description and do not descend to the position-space `H_prod` claim, or
2. once rewritten in position space, they lose the very diagonal structure that motivated Path A

So Model A remains open, but no natural replacement observable currently closes the bridge.

---

## Finding 3 — Q-C does not sign off on Model B

The replicated product experiment is mathematically legitimate:

- three independent copies of the same closure test do give product-measure factorization

But the physical reading is still unresolved.

There are two incompatible interpretations:

### Interpretation A — one medium, three internal channels

Then the God Equation is about one coupled system.

In that case, the replicated product experiment is not yet the same physical object as the theorem target.

### Interpretation B — three separately prepared experiments

Then product factorization is valid by construction.

But now the factor `N = 3` risks meaning “three replicated trials” rather than “three ontic generation channels in one medium.”

That changes the meaning of the bridge.

So Model B currently proves, at best, an auxiliary experiment theorem.
It does not yet prove that the God Equation’s `H_prod` statement for one three-channel medium has been closed.

---

## Finding 4 — Q-D: `kappa` is not a harmless perturbation at closure scale

The actual linearized EOM is

`(Box + m^2) delta chi_j = kappa (delta chi_{j-1} + delta chi_{j+1}) + (lambda/3) delta T`

so cross-channel coupling enters at first order in the dynamics.

For the normalized symmetric closure operator:

`T_sym = (1/2)(Sbar + Sbar^2)`

one gets

`T_sym^3 = (1/4) I + (3/8) Sbar + (3/8) Sbar^2`

For the unnormalized EOM matrix:

`M = Sbar + Sbar^2`

one gets

`M^3 = 2 I + 3 Sbar + 3 Sbar^2`

So at the 3-step closure scale:

- the off-diagonal terms are not suppressed
- they are the same order as the diagonal term
- in the explicit closure matrices they are larger

Therefore there is no exact decoupling regime visible here.

Any single-system Path B proof of independence must confront this mixing directly.
It cannot demote `kappa` to a subleading correction under the current operator.

---

## Finding 5 — Minimal single-system Path B model fails immediately

There is one very simple single-system reading worth testing.

Let one 3-step closure trial produce a final channel label

`Y in {0,1,2}`

and define the channel indicators on that same trial by

`X^(r) = 1[Y = r]`.

Then automatically

`X^(0) + X^(1) + X^(2) = 1`

on every trial.

So the joint law is supported only on one-hot outcomes, and the three indicators are mutually exclusive.

Under the normalized symmetric closure operator

`T_sym^3 = (1/4) I + (3/8) Sbar + (3/8) Sbar^2`

the per-channel marginals are nontrivial. For a start in channel `0`, for example:

`P(Y=0) = 1/4,  P(Y=1) = 3/8,  P(Y=2) = 3/8`.

Then

`P(X^(0)=1, X^(1)=1, X^(2)=1) = 0`

while the product of marginals is

`(1/4)(3/8)(3/8) = 9/256 > 0`.

So factorization fails immediately on this minimal one-system reading.

This does **not** refute every possible one-system formulation of `H_prod`, because one could define different observables.

But it does show:

- the most naive single-system reading does not work
- one cannot claim that Path B is "almost closed" just because the diagonal fraction is `1/4`

Any surviving single-system Path B route must therefore use a more careful observable definition than one-hot final-channel indicators.

---

## Strongest Honest Current Statement

The route split survives.

The live post-audit state is:

- **Model A**: still a meaningful reduced-sector route, but no accepted bridge from Fourier closure to position-space `H_prod`
- **Model B**: still the more literal route, but the current replicated-product reading is not yet physically justified and the actual single-system closure object shows no near-decoupling at 3 steps

So the God Equation remains:

`CONDITIONAL 0.88`

and the next honest theorem targets are:

1. prove or kill `H-A` / `H-B` for Model A
2. define a genuine single-system probability law for Model B and test factorization there

---

## Minimal Upgrade / Kill Criteria

### Model A upgrades only if

- the projected `{k=0,k=1}` sector is derived from the `Z_3` Lagrangian, and
- a precise map from projected-sector closure to position-space `H_prod` is proved

### Model B upgrades only if

- the probability law is defined on one three-channel medium, not only on replicated experiments, and
- factorization survives the actual `kappa`-coupled closure object

### Either route dies if

- the missing bridge requires adding assumptions stronger than the `Z_3` Lagrangian plus Axioms 1–3

---

*Current truth: no sign-off on `H_prod`; route map sharper, closure still open.*
