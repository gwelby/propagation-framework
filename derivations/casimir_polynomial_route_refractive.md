# Casimir Polynomial — Route: Refractive Stress / Virial Balance
*Can the polynomial arise from a PF balance law between drift and angular refractive stress?*

**Date**: 2026-03-21
**Author**: Codex
**Route**: Refractive / virial balance
**Outcome**: C (gap reduction) — refractive dynamics explains why a balance law is natural, but not why the specific polynomial is forced
**Builds on**: `gr_fermat_equivalence.md`, `RESEARCH/coulomb_force_refractive_derivation/MASTER.md`, `topological_weight_from_propagation.md`, `casimir_polynomial_brief.md`

---

## 1. Target

Test whether the PF statement

> forces are refraction

can be pushed far enough to derive the Casimir polynomial

\[
x^2 + C_2x - C_2 = 0
\]

as a drift-versus-structure balance law for a stable coherent mode.

---

## 2. What Refraction Naturally Gives

From the Coulomb/refraction research and the GR/Fermat equivalence note, PF already has a rigorous geometric fact:

- propagation in a medium with gradients is governed by a Fermat/Maupertuis variational principle
- orbital bending can be written as propagation in an effective refractive geometry
- central potentials become central refractive profiles

For a central refractive problem, the effective radial balance always has the form

\[
p_r^2 + \frac{L^2}{r^2} = p^2(r),
\]

or in optical language:

\[
\text{radial part} + \text{angular barrier} = \text{available propagation budget}.
\]

This is the first key Route E result:

\[
\boxed{
\text{PF refraction naturally produces a kinematic/structural balance law}
}
\]

where the angular part enters through \(L^2\), hence through a Casimir-like quantity.

---

## 3. Where `C₂` Enters Naturally

In a 3D rotational medium, coherent angular structure is labeled by

\[
C_2 = j(j+1).
\]

So Route E naturally interprets the structural barrier as

\[
\frac{C_2}{r^2}
\]

up to the appropriate normalization scale.

This is good news:

- Route B showed PF needs an internal angular sector
- Route E shows refractive orbital balance is a natural place for such a sector to act

So refraction makes the appearance of \(C_2\) in a balance equation physically natural.

---

## 4. Why The Polynomial Still Does Not Follow

The generic refractive/virial balance gives a relation of the type

\[
K(x) + S(C_2) = \text{total budget}
\]

or, after normalization,

\[
F(x) = G(C_2).
\]

But it does **not** by itself force

\[
\frac{x^2}{1-x} = C_2.
\]

The problem is the same sharp issue found elsewhere:

- refraction explains why there should be a competition between drift and angular structure
- it does not explain why the drift contribution enters as \(x^2\) rather than \(x\), \(x/(1-x)\), or another function

The refractive route gives the existence of a balance law.
It does not uniquely fix the specific nonlinear form of that law.

---

## 5. Virial Reading

The strongest PF reading of this route is:

- \(x\) measures the fraction of propagation capacity committed to drift
- \(1-x\) measures the structural reserve needed to keep the mode closed
- \(C_2\) measures angular complexity / angular stress

Then the polynomial

\[
x^2 = C_2(1-x)
\]

reads as:

> the self-reinforcing drift capacity squared equals the angular stress times the remaining structural reserve

This is physically legible in PF language.

But again, this is an interpretation of the polynomial, not a derivation of it.

---

## 6. What Route E Adds That Is Real

Route E contributes two clean structural gains.

### Gain 1

It independently supports the idea that the polynomial should be read as a **balance law**, not merely as a numerical fit.

### Gain 2

It gives a PF-native reason why an angular Casimir should enter the balance: in a refractive central problem, angular structure acts as a barrier / stress term.

This means the Casimir is not being imported arbitrarily. The refractive picture gives it a natural seat in the dynamics.

---

## 7. The Remaining Gap

Route E reduces to one precise unresolved step:

> What principle of refractive coherence turns the generic drift-versus-structure balance into the specific nonlinear law
> `x²/(1-x) = C₂`?

There are two likely possibilities:

1. it is the same relativistic squaring step as Route A in different language
2. it is the same cross-sector coupling structure as Route G written as an effective stress balance

So Route E does not open a third deep gap.
It likely maps onto one of the two already identified ones.

---

## 8. Honest Verdict

Route E does not derive the Casimir polynomial.

But it does establish that:

- a PF refractive medium naturally leads to a drift/structure balance law
- the angular Casimir naturally belongs in the structural side of that balance
- the unresolved content is the same one seen elsewhere: what fixes the exact nonlinear form?

So this route ends as:

\[
\boxed{
\text{Outcome C: refractive balance supports the interpretation, but not the specific polynomial}
}
\]

The best synthesis reading is:

\[
\boxed{
\text{Route E strengthens the physical meaning of the polynomial more than its derivation status}
}
\]
