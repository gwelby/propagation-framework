# Fisher 3-Step Trajectory Metric Under `C_3`-Symmetric `T`

**Date**: 2026-04-04  
**Author**: Codex  
**Status**: Formal proof note for Agent Brief B  
**Verdict**: **Path B Fisher/trajectory branch is LIVE.**

The dead-route inference is false.
This proves **Option B**, in stronger form than requested: the route is live for every
non-uniform circulant `T`, not only for directed walks with `t_1 != t_2`.

What `C_3` symmetry does force is narrower:

- at the `C_3`-fixed prior `u = (1/3, 1/3, 1/3)`, the classical Fisher matrix on the start-channel simplex is `C_3`-invariant
- equivalently, its restriction to the simplex tangent space is a scalar multiple of the identity

What `C_3` symmetry does **not** force is zero distinguishability.

For every non-uniform circulant stochastic matrix `T = circ(t_0,t_1,t_2)`, the scalar is

`3|lambda_1|^2 = 3(t_0^2+t_1^2+t_2^2 - t_0 t_1 - t_1 t_2 - t_2 t_0) > 0`

so the trajectory family has strictly positive Fisher curvature along channel-contrast directions.
Equivalently, `I(channel; trajectory) > 0` for every non-uniform circulant `T`.

Only the trivial uniform walk `t_0 = t_1 = t_2 = 1/3` kills the route.

Cross-check note: `derivations/fisher_3step_numerical.md` was not present when this note was written.

---

## 1. Setup

Let the hidden start channel be

`C in {0,1,2}`

with prior

`P(C=j) = theta_j`,  `theta in Delta_2`,  `theta_j > 0`,  `sum_j theta_j = 1`.

Let the observed absolute 3-step trajectory be

`Y = (X_1, X_2, X_3) in {0,1,2}^3`.

The dynamics are a row-stochastic circulant matrix

`T = circ(t_0,t_1,t_2)`,  `t_r >= 0`,  `t_0+t_1+t_2 = 1`,

so

`T_{ab} = t_{b-a mod 3}`.

Conditioned on `C=j`,

`p_j(x_1,x_2,x_3) := P(Y=(x_1,x_2,x_3) | C=j) = T_{j x_1} T_{x_1 x_2} T_{x_2 x_3}`.

The observable family indexed by the start-channel prior is

`p_theta(y) = sum_j theta_j p_j(y)`.

The classical Fisher matrix in ambient coordinates `(theta_0,theta_1,theta_2)` is

`g_ab(theta) = sum_y p_theta(y) (partial_{theta_a} log p_theta(y)) (partial_{theta_b} log p_theta(y))`

which, because `p_theta` is linear in `theta`, becomes

`g_ab(theta) = sum_y p_a(y) p_b(y) / p_theta(y)`.

The physically relevant metric is the restriction of `g(theta)` to the simplex tangent space

`T_theta Delta_2 = {v in R^3 : v_0+v_1+v_2 = 0}`.

---

## 2. Honest Disambiguation: `I=0` Requires Identical Conditionals, Not Merely `C_3`-Related Ones

This is the key logical fork.

For any prior with all `theta_j > 0`,

`I(C;Y) = sum_j theta_j D_KL(p_j || p_theta)`.

Therefore

`I(C;Y) = 0`

if and only if

`p_j = p_theta` for every `j` with `theta_j > 0`,

hence if and only if

`p_0 = p_1 = p_2`.

So:

- `C_3`-related conditional laws do **not** imply zero mutual information
- only **identical** conditional laws imply zero mutual information

If the observation space keeps the absolute channel labels, a shifted copy is still a different
distribution and is generally distinguishable.

---

## 3. Exact `C_3` Symmetry of the Conditional Trajectory Laws

Let `sigma(a) = a+1 mod 3`, and let `sigma` act on trajectories componentwise:

`sigma(x_1,x_2,x_3) = (sigma(x_1), sigma(x_2), sigma(x_3))`.

Because `T` is circulant,

`T_{sigma(a), sigma(b)} = T_{ab}`.

Hence

`p_{sigma(j)}(sigma(y)) = p_j(y)`.

So the three conditional laws are indeed cyclic shifts of one another.

But they are not identical unless the rows of `T` are identical, i.e. unless

`t_0 = t_1 = t_2 = 1/3`.

That already shows the dead-route argument from symmetry alone fails.

---

## 4. The 3-Step Trajectory Carries Exactly the Same Start-Channel Information as `X_1`

This is the clean structural simplification.

Write

`q_theta(x_1) := P_theta(X_1 = x_1) = sum_j theta_j T_{j x_1}`.

Then

`p_theta(x_1,x_2,x_3) = q_theta(x_1) T_{x_1 x_2} T_{x_2 x_3}`.

So, conditioned on `X_1`, the later coordinates `(X_2,X_3)` are independent of `C`.
Equivalently,

`C -> X_1 -> (X_2,X_3)`

is a Markov chain.

Therefore

`I(C;Y) = I(C;X_1)`.

So the 3-step trajectory route is neither stronger nor weaker than the one-step absolute-position
route for this parameterization. The channel information is already present in `X_1`, and the full
trajectory retains it.

For the symmetric prior `u = (1/3,1/3,1/3)`, a circulant stochastic matrix is automatically
doubly stochastic, so `X_1` is uniform:

`P_u(X_1 = x) = 1/3`.

Also `X_1 = C + Delta mod 3`, where `Delta` has law `(t_0,t_1,t_2)`.
Hence

`I_u(C;Y) = I_u(C;X_1) = log 3 - H(t_0,t_1,t_2)`.

This is strictly positive for every non-uniform circulant `T`, and zero only for the uniform walk.

So the route is live already at the mutual-information level.

---

## 5. Exact Fisher Matrix Formula

Differentiate `p_theta`:

`partial_{theta_a} p_theta(x_1,x_2,x_3) = T_{a x_1} T_{x_1 x_2} T_{x_2 x_3}`.

Therefore

`partial_{theta_a} log p_theta(x_1,x_2,x_3) = T_{a x_1} / q_theta(x_1)`,

which depends only on `x_1`.

Plugging into the Fisher formula gives

`g_ab(theta) = sum_{x_1,x_2,x_3} p_theta(x_1,x_2,x_3) T_{a x_1} T_{b x_1} / q_theta(x_1)^2`

and summing over `x_2,x_3` yields

`g_ab(theta) = sum_{x=0}^2 T_{a x} T_{b x} / q_theta(x)`.

This is the exact trajectory Fisher matrix.

Two immediate consequences:

1. The theorem as originally phrased is false if read as a statement for all `theta`.
2. At the symmetric prior `u`, the symmetry becomes exact and computable.

### 5.1 Why the global claim `g_00 = g_11 = g_22` is false as stated

Take the deterministic cyclic shift

`T = Sbar = circ(0,1,0)`.

Then each conditional law is a point mass, and the supports are disjoint:

- from `C=0`: `Y=(1,2,0)`
- from `C=1`: `Y=(2,0,1)`
- from `C=2`: `Y=(0,1,2)`

So

`p_theta(Y_j) = theta_j`

on the three support points, which gives

`g(theta) = diag(1/theta_0, 1/theta_1, 1/theta_2)`.

Unless `theta_0 = theta_1 = theta_2`, the diagonal entries are not equal.

Therefore the raw statement

`g_00 = g_11 = g_22 for all theta`

is false.

The correct symmetry statement is the one at the `C_3`-fixed prior `u`.

---

## 6. Fisher Matrix at the Symmetric Prior

At `u = (1/3,1/3,1/3)`,

`q_u(x) = 1/3`

for every `x`, so the exact Fisher matrix becomes

`g_ab(u) = 3 sum_x T_{a x} T_{b x} = 3 (T T^T)_{ab}`.

Since `T` is circulant, `T T^T` is real symmetric circulant. Writing

`s := t_0^2 + t_1^2 + t_2^2`

and

`c := t_0 t_1 + t_1 t_2 + t_2 t_0`,

we get

`g(u) = 3 [[s,c,c],[c,s,c],[c,c,s]]`.

So yes:

`g_00(u) = g_11(u) = g_22(u) = 3s`.

But this is not a no-information statement.

### 6.1 Restriction to the simplex tangent space

On the tangent space `v_0+v_1+v_2=0`, the all-ones matrix vanishes, so

`g(u)|_{T_u Delta_2} = 3(s-c) I`.

Now

`s-c = t_0^2+t_1^2+t_2^2 - t_0 t_1 - t_1 t_2 - t_2 t_0`

and also

`s-c = (1/2)[(t_0-t_1)^2 + (t_1-t_2)^2 + (t_2-t_0)^2]`.

Hence

`g(u)|_{T_u Delta_2} = (3/2)[(t_0-t_1)^2 + (t_1-t_2)^2 + (t_2-t_0)^2] I`.

This is:

- zero only when `t_0=t_1=t_2=1/3`
- strictly positive for every non-uniform circulant `T`

So the metric is **isotropic**, but not **degenerate to zero**.

That is the correct conclusion.

### 6.2 Fourier form

Let

`lambda_0 = 1`,

`lambda_1 = t_0 + t_1 omega + t_2 omega^2`,

`lambda_2 = lambda_1^*`,

with `omega = exp(2 pi i / 3)`.

Then

`T T^T`

has eigenvalues

`1, |lambda_1|^2, |lambda_1|^2`.

Therefore

`g(u)|_{T_u Delta_2} = 3 |lambda_1|^2 I`.

Again, this is positive unless `lambda_1 = 0`, which for a stochastic circulant `T` happens only
for the uniform walk.

---

## 7. Explicit Countermodel Killing the “Symmetry Implies Dead Route” Claim

Take

`T = Sbar = circ(0,1,0)`.

This matrix is fully circulant and `C_3`-symmetric.

Yet the observation is maximally informative:

- if `C=0`, then `Y=(1,2,0)`
- if `C=1`, then `Y=(2,0,1)`
- if `C=2`, then `Y=(0,1,2)`

So the trajectory identifies the start channel exactly.

For the symmetric prior `u`,

`I_u(C;Y) = log 3`

and

`g(u) = 3 I_3`,

so

`g(u)|_{T_u Delta_2} = 3 I`.

This is the opposite of a dead route. It is maximal distinguishability.

The conditionals are `C_3`-related, but they are not identical.
That is enough to keep the Fisher curvature strictly positive.

---

## 8. Final Theorem

**Theorem.**
Let `T = circ(t_0,t_1,t_2)` be a row-stochastic circulant matrix on `Z_3`, let `C` be the start
channel, let `Y=(X_1,X_2,X_3)` be the absolute 3-step trajectory, and let `p_theta` be the
trajectory family induced by the start prior `theta`.

Then:

1. `I(C;Y)=0` if and only if the three conditional laws `p_0,p_1,p_2` are identical.
2. For circulant `T`, the conditional laws are cyclic shifts of one another, but they are
   identical only in the uniform case `t_0=t_1=t_2=1/3`.
3. Hence for every non-uniform circulant `T`, `I_u(C;Y) > 0`.
4. The exact Fisher matrix is

   `g_ab(theta) = sum_x T_{a x} T_{b x} / (sum_j theta_j T_{j x})`.

5. At the symmetric prior `u=(1/3,1/3,1/3)`,

   `g(u) = 3 T T^T`,

   so `g(u)` is symmetric circulant and

   `g(u)|_{T_u Delta_2} = 3|lambda_1|^2 I`.

6. Therefore the trajectory Fisher metric is isotropic on the simplex, but it is nonzero for
   every non-uniform circulant `T`.

**Conclusion.**
`C_3` symmetry does **not** kill the Fisher/trajectory route.
What it kills is anisotropy, not distinguishability.
The branch is live unless the walk is the completely uniform channel-scrambler.

---

## 9. Scope Boundary

This note settles only the stated classical trajectory question for the observable

`Y = (X_1,X_2,X_3)`

with absolute channel labels retained.

It does **not** settle:

- Path A
- full `H_prod`
- nonlinear non-Gaussian PF-vacuum routes
- quantum/Bures Fisher variants

One extra caution:

If one quotients the observation space by the global `C_3` shift and keeps only the relative
shape class of the trajectory, then the three conditionals do collapse. That is a different
observable family than the one in this brief.
