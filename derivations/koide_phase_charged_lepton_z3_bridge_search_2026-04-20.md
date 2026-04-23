# Koide Phase: Charged-Lepton to Z3 Bridge Search

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Record the bounded search for an existing repo theorem object mapping the charged-lepton
square-root mass triple into the quotient-character basis `1, omega, omega^2` without simply
restarting from the Koide parametrization.

---

## 1. Search target

The question from
[koide_phase_z3_origin_audit_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_z3_origin_audit_2026-04-20.md)
was:

> does the repo already contain a theorem object of the form
>
> `charged-lepton square-root mass triple -> canonical Z_3 character basis`
>
> independent of taking the Koide `120°` parametrization as primitive?

This note records the answer.

---

## 2. What was actually found

The repo does contain:

### A. Abstract internal `Z_3` structure

- `phase_closure_exact_model.md`
- `path_a_z6_z3_chirality_intertwiner_audit_2026-04-05.md`
- multiple `G3` files using quotient characters `1, omega, omega^2`

This gives an abstract quotient character set.

### B. Koide amplitude geometry

- `koide_geometric_equivalence.md`
- `closing_the_gaps.md`

These give:

- three equal-strength resonances
- 120-degree spacing
- equilateral geometry / `Q = 2/3`

### C. The new abstract matrix lane

- [koide_phase_minimal_matrix_trace_spec_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_minimal_matrix_trace_spec_2026-04-20.md)

This gives the minimal abstract `3 x 3` phase matrix and its exact `cos(9 delta)` trace structure.

---

## 3. What was not found

No existing file in the current derivation tree was found that does all three of the following in
one theorem object:

1. starts from the charged-lepton square-root mass triple,
2. derives a canonical `Z_3` character basis or phase matrix,
3. does so **without** importing the Koide `120°` parametrization as an input.

In particular, the search did **not** find:

- an existing charged-lepton phase matrix theorem,
- an explicit regular-representation-to-mass-triple bridge,
- a character-theoretic diagonalization of the charged-lepton mass triple treated as a PF theorem,
- a derivation that the charged-lepton square-root vector is naturally the `Z_3` character orbit
  of a single generator.

---

## 4. Why the existing candidates do not count

### G1 / internal walk files

These derive abstract `Z_3` orbit data, but not the charged-lepton mass realization.

### Koide geometry files

These derive 120-degree spacing once the three-mode Koide geometry is already in play, but do not
independently derive a PF `Z_3` character basis for the charged-lepton triple.

### `g1_model_specification_brief.md`

This file explicitly uses language like "the three 120° nodes of the Koide triangle." That is
heuristic model language, not an upstream bridge independent of Koide input.

So it cannot be counted as the missing theorem object.

---

## 5. Search verdict

**Current bounded result**:

> the repo contains the abstract `Z_3` quotient characters and the Koide threefold geometry, but it
> does not yet contain a theorem object that bridges the charged-lepton square-root mass triple to
> that quotient-character basis independently of the Koide parametrization itself.

That absence is the current frontier.

---

## 6. Consequence

The matrix lane remains:

- mathematically natural,
- structurally aligned with PF's abstract quotient character set,
- but still not upgraded to a PF-native derivation of the charged-lepton phase law.

Until this bridge exists, the honest repo status remains:

`delta ~= 2/9` = empirical anchor  
selector mechanism = open
