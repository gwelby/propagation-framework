# Casimir Polynomial — Route: Holonomy / Transfer Matrix
*Is the polynomial the characteristic equation of a PF two-sector transport map?*

**Date**: 2026-03-21
**Author**: Claude
**Route**: Holonomy/monodromy — polynomial as characteristic equation of a 2×2 transfer matrix over a closed PF loop
**Outcome**: B/C (partial no-go with structural finding — not independent of Route A gap)
**Warning**: Route matrix notes risk of repeating G3 holonomy dead ends. Tested carefully.

---

## 1. The Setup

A 2×2 matrix T has characteristic polynomial det(T − xI) = x² − Tr(T)x + det(T) = 0.

For this to equal x² + C₂x − C₂ = 0:

$$\mathrm{Tr}(T) = -C_2, \qquad \det(T) = -C_2.$$

The natural minimal matrix satisfying these is:

$$T = \begin{pmatrix} -C_2 & C_2 \\ 1 & 0 \end{pmatrix}.$$

Check: Tr = −C₂ ✓, det = 0 − C₂ = −C₂ ✓.

This T generates the recurrence: if the state vector is v_n = (x_n, x_{n-1}), then T·v_n = v_{n+1} gives:

$$x_{n+1} = -C_2 x_n + C_2 x_{n-1}.$$

The eigenvalues of T are exactly x₊ and x₋ from the polynomial. The question: **can T be identified with a PF phase-walk transfer map?**

---

## 2. Candidate PF Transfer Map

In the PF's N=3 phase walk, each step advances the internal phase by θ = 2π/3. The transfer matrix for a spin-j mode over one step is U_j(2π/3) — a rotation operator in the spin-j representation.

For j = 1 (the bosonic sector):

$$U_1(2\pi/3) = \begin{pmatrix} e^{2i\pi/3} & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & e^{-2i\pi/3} \end{pmatrix}.$$

This is 3×3 unitary, not 2×2. Its characteristic polynomial is of degree 3, not degree 2.

For j = 1/2 (the fermionic sector):

$$U_{1/2}(2\pi/3) = \begin{pmatrix} e^{i\pi/3} & 0 \\ 0 & e^{-i\pi/3} \end{pmatrix}.$$

Characteristic polynomial: (x − e^{iπ/3})(x − e^{−iπ/3}) = x² − 2cos(π/3)x + 1 = x² − x + 1.

This is NOT x² + C₂x − C₂. The phase walk's single-step transfer matrix gives a different quadratic.

---

## 3. Three-Step Product

The full N=3 cycle gives U_j(2π/3)³ = U_j(2π) = (−1)^{2j}I. For j=1/2: (−I). For j=1: (+I).

The characteristic polynomial of ±I is (x ± 1)² — not the Casimir polynomial. The N=3 holonomy reduces to a scalar (±1) on each spin sector, carrying no Casimir information.

**This is the G3 lesson revisited**: the holonomy of the N=3 walk is a scalar (class function), and class functions don't encode C₂ as a dynamical variable. The Casimir polynomial requires C₂ to appear as a free parameter, which a fixed-angle rotation cannot produce.

---

## 4. Cross-Sector Transfer

Hypothesis: T is not a within-sector rotation but a cross-sector transfer map coupling the kinematic parameter x to the angular content C₂.

If the state is v = (kinematic_fraction, angular_content) = (x, C₂), a linear map T: v_n → v_{n+1} with the recurrence structure gives a sequence of mass/phase iterations. The fixed points of this map are the eigenvalues of T — the self-consistent values x₊ and x₋.

**Does such a map exist in PF?** The PF as currently formulated has no defined cross-sector transfer map between the kinematic and angular sectors. The Lagrangian (`propagation_lagrangian.md`) is a scalar field with no spin/angular structure:

$$\mathcal{L}_\text{prop} = \frac{1}{2}\eta^{ab}(\partial_a \chi)(\partial_b \chi) - V(\chi) + \lambda \chi T.$$

There are no matrices, no multi-component fields, no cross-sector couplings. The transfer matrix T cannot be read off from the current Lagrangian.

---

## 5. The Trace = Determinant Condition

The specific condition Tr(T) = det(T) = −C₂ (which makes the polynomial's sum-of-roots equal its product-of-roots) has a representation-theoretic meaning: the eigenvalues x₊, x₋ satisfy x₊ + x₋ = x₊ · x₋ = −C₂.

From the Vieta formulas: x₊ · x₋ = −C₂ and x₊ + x₋ = −C₂ → x₋ = −C₂ − x₊.

The product: x₊(−C₂ − x₊) = −C₂ → −C₂x₊ − x₊² = −C₂ → x₊² + C₂x₊ − C₂ = 0. Circular — this is just the polynomial again.

The condition Tr = det for a 2×2 matrix means: λ₁ + λ₂ = λ₁λ₂. This factors as λ₂(λ₁ − 1) = −λ₁, giving λ₂ = λ₁/(1 − λ₁) for λ₁ ≠ 1. This is the Möbius map z → z/(1−z) applied to one eigenvalue to get the other. Whether this has PF meaning is unclear.

---

## 6. Outcome

**Route D is a partial no-go.** The PF's phase walk produces holonomies that are scalars on each spin sector — they don't encode C₂ dynamically. A transfer matrix with the right characteristic polynomial can be written down, but it requires cross-sector coupling between the kinematic and angular sectors that doesn't exist in the current PF Lagrangian.

**What this route adds**: It confirms that any derivation of the polynomial from PF requires cross-sector coupling — a kinematic sector and an angular sector interacting. This is structural knowledge, not just failure-mode recording.

**Not independent of Route A**: Grounding the cross-sector coupling requires specifying how angular content C₂ enters the kinematic dynamics — which is the same question as Route A (why β²/√(1−β²) = √C₂).

**One small new thing**: The polynomial's eigenvalues are related by the Möbius map λ₂ = λ₁/(1−λ₁). Whether this has PF-native significance is an open but bounded question.

---

*Written by Claude, 2026-03-21*
*Route: Holonomy / Transfer Matrix*
*Outcome: B/C — not independent of Route A gap; confirms cross-sector coupling is required*
*Issue: #3 (Weinberg angle), Casimir polynomial derivation*
