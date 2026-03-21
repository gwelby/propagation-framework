# The Geometric Equivalence of the Koide Formula
**Date:** March 2026

## 1. The Empirical Fact (PDG 2024 Verification)
The Koide formula relates the masses of the charged leptons ($m_e, m_\mu, m_\tau$):
$$ Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2} = \frac{2}{3} $$
Using the latest PDG 2024 pole masses, this relation holds to remarkable precision.
*   Calculation: $0.6666605...$
*   Target: $2/3$ ($0.6666666...$)
*   Error: $0.0009\%$

## 2. The Geometric Equivalence: $R/A = \sqrt{2}$
Rather than treating the masses purely algebraically, we parameterize the square roots of the masses as amplitudes in a 3D configuration space. Any three real values can be expressed as a central scalar amplitude $A$ and a circulating radius $R$ with phase $\theta_n$:

$$ \sqrt{m_n} = A + R \cos\left(\theta_0 + \frac{2\pi n}{3}\right) \quad \text{for } n = 0, 1, 2 $$

Substituting this parameterization into the Koide ratio $Q$ yields a pure geometric identity:
$$ Q = \frac{3A^2 + \frac{3}{2}R^2}{(3A)^2} = \frac{1}{3} + \frac{1}{6}\left(\frac{R}{A}\right)^2 $$

Setting $Q = 2/3$ enforces a strict geometric condition on the manifold:
$$ \frac{2}{3} = \frac{1}{3} + \frac{1}{6}\left(\frac{R}{A}\right)^2 \implies \left(\frac{R}{A}\right)^2 = 2 \implies \frac{R}{A} = \sqrt{2} $$

**Equivalence to the Foot Cone:**
In the vector space $v = (\sqrt{m_e}, \sqrt{m_\mu}, \sqrt{m_\tau})$, the angle $\theta$ between the mass vector and the symmetric axis $(1,1,1)$ is given by $\cos^2\theta = 1/(3Q)$.
For $Q = 2/3$, $\cos^2\theta = 1/2$, meaning $\theta = 45^\circ$.
The condition $R/A = \sqrt{2}$ is the explicit Cartesian projection of Foot's 45-degree cone. It proves that the "traceless" geometric deviation ($R$) is locked to the "trace" symmetric scale ($A$) by the diagonal of a unit square ($\sqrt{2}$).

## 3. The U(3) Decomposition: One Exact Result

*Rigorous derivation. The interpretation of why this value is selected remains open — see Section 4.*

Let $x_i = \sqrt{m_i}$ and form the diagonal matrix $X = \mathrm{diag}(x_1, x_2, x_3)$.

Decompose $X$ into its scalar (trace) and traceless parts:
$$X = \frac{e_1}{3} I + H, \qquad \mathrm{Tr}\, H = 0$$

where $e_1 = x_1+x_2+x_3$. Then:
$$\mathrm{Tr}\, X^2 = \frac{e_1^2}{3} + \mathrm{Tr}\, H^2$$

and since $(\mathrm{Tr}\, X)^2 = e_1^2$:
$$Q = \frac{\mathrm{Tr}\, X^2}{(\mathrm{Tr}\, X)^2} = \frac{1}{3} + \frac{\mathrm{Tr}\, H^2}{e_1^2}$$

This is exact. Setting $Q = 2/3$:
$$\frac{2}{3} = \frac{1}{3} + \frac{\mathrm{Tr}\, H^2}{e_1^2} \implies \mathrm{Tr}\, H^2 = \frac{e_1^2}{3}$$

Since $\mathrm{Tr}\, H^2 = e_1^2 - 2e_2 - e_1^2/3 = 2e_1^2/3 - 2e_2$... wait — more directly:
$p_2 = \mathrm{Tr}\, X^2 = e_1^2 - 2e_2$, so $\mathrm{Tr}\, H^2 = p_2 - e_1^2/3 = 2e_1^2/3 - 2e_2$.
Setting this equal to $e_1^2/3$ gives $e_2 = e_1^2/6$.

Therefore:
$$\boxed{Q = \tfrac{2}{3} \iff \mathrm{Tr}\, H^2 = \tfrac{e_1^2}{3} \iff e_2/e_1^2 = \tfrac{1}{6} \iff \|I\text{-part}\|^2 = \|H\text{-part}\|^2}$$

The last form is the cleanest: $Q = 2/3$ is the unique value at which the scalar ($U(1)$) part and the traceless ($SU(3)$) part of $X$ carry **equal squared Frobenius norm**. This is a genuine $U(3) \to U(1) \times SU(3)$ decomposition statement — not a metaphor.

The clean object for the structural orbit viewpoint is $X$ itself: the symmetric polynomials $\{e_1, e_2, e_3\}$ are the conjugation invariants of the diagonal Hermitian matrix $X$, and $e_2/e_1^2 = 1/6$ picks a specific co-dimension 1 surface in the space of such matrices.

*Note: substantial theory on cubics in this context was contributed to the Wikipedia Koide formula article by an anonymous editor from Newcastle University (identity unknown as of March 2026). The $U(3)$ decomposition route was suggested by R. Rivero (March 2026, private communication).*

## 4. Interpretation Routes — Not Yet Derived

The exact result in Section 3 identifies *what* $Q=2/3$ means in the $U(3)$ decomposition. It does not explain *why* the physical vacuum selects the equal-norm point over any other. Three interpretation routes have been proposed; none is yet a derivation.

**Route A — Maximum entropy (Claude):** The equal-norm condition is the maximum-entropy distribution over the $U(3)$ decomposition — the center of the allowed range $1/3 \le Q \le 1$ where neither sector dominates. Conjecture: phase coherence across $N=3$ generations forces maximum entropy. *Not derived. Requires a theorem connecting coherence to entropy maximization in the $U(1)/SU(3)$ split.*

**Route B — Cubic orbit (Codex):** The condition $e_2/e_1^2 = 1/6$ picks a specific $SU(3)$ conjugation orbit of the matrix $X$. The claim is that $U(3) \to U(1) \times SU(3)$ gauge-fixing uniquely selects this orbit. *Not derived. Requires identifying the orbit explicitly and proving uniqueness of the gauge selection. The Newcastle cubic theory is the most promising existing source.*

**Route C — Pairwise coherence (Lumi/PF):** In the Propagation Framework, $e_2$ measures inter-generational coupling; $e_2/e_1^2$ is a dimensionless coherence ratio. The value $1/6$ is conjectured to follow from stability of $N=3$ coherent modes under Axiom 3. *Caution: equal pairwise symmetry alone does not force $1/6$ — in the fully degenerate case $x_1=x_2=x_3$, one gets $e_2/e_1^2 = 1/3$, not $1/6$. Any derivation via this route must explain what additional constraint selects $1/6$ over $1/3$.*

## 5. Conclusion

The chain of equivalences is established:
$$Q = \tfrac{2}{3} \iff \theta = 45^\circ \iff \frac{R}{A} = \sqrt{2} \iff \frac{e_2}{e_1^2} = \tfrac{1}{6} \iff \|U(1)\text{-part}\|^2 = \|SU(3)\text{-part}\|^2$$

All hold to $0.0009\%$ from PDG 2024 data. The $U(3)$ decomposition in Section 3 is the strongest structural statement currently in hand: it proves the equal-norm condition is the precise algebraic content of the Koide formula. What remains open is a first-principles reason for the selection. Routes A, B, and C are the live candidates.

*Decomposition by Claude; structural correction and route audit by Codex; PF interpretation by Lumi — March 2026.*
