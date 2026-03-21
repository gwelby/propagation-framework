# Koide Selection Audit — What Exactly Must Be Explained?

**Date**: 2026-03-21  
**Author**: Codex  
**Task**: Sharpen issue #2 — "Why does the vacuum choose \(Q=2/3\)?"  
**Status**: EXACT STRUCTURAL RESULTS + ROUTE AUDIT  
**Builds on**: `koide_geometric_equivalence.md`  

---

## 1. The Selection Problem

For charged-lepton amplitudes

\[
x_i = \sqrt{m_i}, \qquad e_1 = x_1+x_2+x_3,
\]

the Koide quantity is

\[
Q = \frac{x_1^2+x_2^2+x_3^2}{(x_1+x_2+x_3)^2}.
\]

The geometric equivalence

\[
Q = \frac{2}{3}
\iff
\frac{R}{A} = \sqrt{2}
\iff
\theta = 45^\circ
\iff
\frac{e_2}{e_1^2} = \frac{1}{6}
\]

is already established in `koide_geometric_equivalence.md`.

The remaining question is a **selection** question:

> Why should the physical charged-lepton vector land at the specific value \(Q=2/3\), instead of
> any other allowed value?

This note isolates what is exact, what is false, and what remains genuinely open.

---

## 2. Normalize the Problem

Define normalized amplitudes

\[
p_i = \frac{x_i}{e_1},
\qquad
p_i > 0,
\qquad
\sum_{i=1}^3 p_i = 1.
\]

Then the Koide quantity becomes

\[
Q = \sum_{i=1}^3 p_i^2.
\]

So \(Q\) is simply the squared Euclidean norm of a point on the probability simplex.

Also,

\[
e_2 = x_1x_2+x_1x_3+x_2x_3
     = \frac{e_1^2 - (x_1^2+x_2^2+x_3^2)}{2},
\]

hence

\[
\frac{e_2}{e_1^2} = \frac{1-Q}{2}.
\]

Therefore

\[
Q=\frac{2}{3}
\iff
\frac{e_2}{e_1^2} = \frac{1}{6}.
\]

---

## 3. Exact Range of \(Q\)

Since \(p_1+p_2+p_3=1\) and \(p_i>0\),

\[
\frac{1}{3} \le \sum_i p_i^2 < 1.
\]

The lower bound is the democratic point

\[
p_1=p_2=p_3=\frac{1}{3}
\quad\Rightarrow\quad
Q=\frac{1}{3}.
\]

The upper bound is approached when one amplitude dominates and the other two go to zero:

\[
(p_1,p_2,p_3)\to(1,0,0)
\quad\Rightarrow\quad
Q\to 1.
\]

So the physically allowed interval is

\[
\boxed{\frac{1}{3} \le Q < 1.}
\]

The Koide value

\[
Q=\frac{2}{3}
\]

is exactly the arithmetic midpoint of this interval.

That midpoint fact is exact, but by itself it is not yet a physical selection theorem.

---

## 4. Exact Equipartition Theorem in the \(u(3)\) Split

From `koide_geometric_equivalence.md`, let

\[
X=\mathrm{diag}(x_1,x_2,x_3) = \frac{e_1}{3}I + H,
\qquad
\mathrm{Tr}\,H=0.
\]

Then

\[
Q = \frac{1}{3} + \frac{\mathrm{Tr}\,H^2}{e_1^2}.
\]

The scalar part has squared Frobenius norm

\[
\left\|\frac{e_1}{3}I\right\|_F^2 = \frac{e_1^2}{3},
\]

and the traceless part has squared Frobenius norm

\[
\|H\|_F^2 = \mathrm{Tr}\,H^2 = e_1^2\!\left(Q-\frac{1}{3}\right).
\]

So their ratio is

\[
\rho := \frac{\|H\|_F^2}{\|(e_1/3)I\|_F^2}
      = \frac{e_1^2(Q-1/3)}{e_1^2/3}
      = 3Q-1.
\]

Therefore:

\[
\boxed{Q=\frac{2}{3} \iff \rho = 1.}
\]

In words:

> The Koide point is exactly the point at which the scalar \(u(1)\) component and traceless
> \(su(3)\) component of the diagonal amplitude matrix carry equal squared Frobenius norm.

This is the strongest exact structural statement currently available.

---

## 5. What Naive Entropy Does — and Does Not — Select

A common instinct is to interpret the normalized amplitudes \(p_i\) as a probability
distribution and ask whether \(Q=2/3\) is the maximum-entropy point.

For Shannon entropy

\[
S(p) = -\sum_{i=1}^3 p_i \log p_i,
\]

the maximum occurs at the democratic point

\[
p_1=p_2=p_3=\frac{1}{3}.
\]

At that point:

\[
Q = \sum_i p_i^2 = 3\left(\frac{1}{3}\right)^2 = \frac{1}{3},
\qquad
\frac{e_2}{e_1^2} = \frac{1}{3}.
\]

So:

\[
\boxed{\text{maximum generation entropy selects } Q=\frac{1}{3}, \text{ not } \frac{2}{3}.}
\]

This means any "maximum entropy" explanation of Koide must refer to a different entropy notion,
for example an entropy over the **sector split** \(u(1)\oplus su(3)\), not over the three
generation amplitudes themselves.

That distinction is essential.

---

## 6. What This Does to the Three Candidate Routes

### Route A — Maximum Entropy

Still possible in principle, but only in a refined form.

What fails:

- naive entropy over the generation weights \(p_i\)

What remains possible:

- an entropy or equipartition principle over the scalar/traceless sector split

### Route B — Cubic / Spectral Orbit

Still viable.

The exact structural content is now clearer:

- \(Q=2/3\) is the equal-norm point in the \(u(3)\) decomposition
- equivalently, it is the midpoint spectral stratum in the allowed \(Q\)-interval

What remains open is why gauge or orbit selection would force that stratum.

### Route C — Pairwise Coherence

Still open, but constrained.

If one imposes only full democratic symmetry \(x_1=x_2=x_3\), the result is

\[
Q=\frac{1}{3},
\]

not \(2/3\). So route C requires an additional nontrivial constraint beyond simple equal-pair
symmetry.

---

## 7. Exact Output of This Audit

What is now exact:

1. \(Q\) is a simplex norm: \(Q=\sum p_i^2\)
2. \(Q\) lives in the interval \([1/3,1)\)
3. \(Q=2/3\) is the midpoint of that interval
4. \(Q=2/3\) is exactly the equal-norm point of the scalar/traceless \(u(3)\) decomposition
5. naive Shannon entropy over generations selects \(Q=1/3\), not \(2/3\)

What remains open:

- why the physical lepton vector should prefer the equal-norm point over the democratic point or
  any other allowed point

That is the real content of issue #2.

---

## 8. Best Current Statement of the Problem

The Koide selection problem is now narrow enough to phrase cleanly:

> Find a first-principles selection rule that picks the equal-norm point
>
> \[
> \|u(1)\text{-part}\|_F^2 = \|su(3)\text{-part}\|_F^2
> \]
>
> of the charged-lepton amplitude matrix.

That is the strongest honest frontier statement currently available.

---

*This note does not solve the Koide selection problem. It removes one false route, strengthens the
exact structure, and sharpens what any successful derivation must actually explain.*
