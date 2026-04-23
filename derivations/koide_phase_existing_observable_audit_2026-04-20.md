# Koide Phase: Existing Observable Audit

**Date**: 2026-04-20  
**Author**: Codex  
**Purpose**: Audit the existing PF / Koide three-cycle, trace, and determinant-style observables
already present in the repo against the exact Chebyshev cubic target written in
[koide_phase_minimal_cubic_selector_spec_2026-04-20.md](/mnt/d/Fundamentals/derivations/koide_phase_minimal_cubic_selector_spec_2026-04-20.md).

---

## 1. Audit target

The scalar phase reduction already gives

`f(delta) = -1/2 + cos(3 delta)/sqrt(2)`.

The cubic audit proved that inside this scalar lane the first exact pure `cos(9 delta)` selector is
the unique tuned cubic

`Q_*(f) = c + sqrt(2) k (8 f^3 + 12 f^2 + 3 f - 1/2)`.

So the current audit question is:

> do any of the concrete observables already used or proposed in the repo reduce to that tuned
> cubic, or to an equivalent exact selector class?

---

## 2. Candidate family A — determinant / three-factor product

The exact Koide factor triple is

`g_k(delta) = 1 + sqrt(2) cos(delta + 2*pi*k/3)`.

The determinant-like symmetric product is

`g_0 g_1 g_2 = f(delta)`.

### Result

This is only **linear** in the reduced scalar.

It cannot isolate `cos(9 delta)`.

This is exactly the degree barrier from the cubic note.

### Verdict

Not enough structure.

---

## 3. Candidate family B — powers of the determinant factor

The repo already audited monomials `f^k`, especially the Rivero-relevant cases.

Examples:

- `f^3`
- `f^6`

### Result

These remain generic scalar monomials.

They do generate `cos(9 delta)` content, but they also retain lower harmonics.

The earlier harmonic audit already proved this qualitatively.
The new cubic note sharpens it:

> a generic monomial does not land on the unique Chebyshev cancellation locus.

### Verdict

Already dead as an exact selector family.

---

## 4. Candidate family C — inverse-weight corrected determinant terms

The deep Rivero audit identified two more concrete scalar families:

### C1. Cross-term family

The off-shell cross-term has the structure

`f(delta)^6 * sum_k 1 / g_k(delta)^2`.

Using the exact symmetric identities `e1 = 3`, `e2 = 3/2`, `e3 = f`, this reduces exactly to

`sum_k 1/g_k^2 = -3 (8 f - 3) / (4 f^2)`

and therefore

`f^6 * sum_k 1/g_k^2 = -6 f^5 + (9/4) f^4`.

So the cross-term family is a **quartic/quintic** scalar polynomial in `f`.

### C2. Pure `W_3^2` family

The pure higher term has the structure

`f(delta)^12 * sum_k 1 / g_k(delta)^4`.

Again reducing exactly,

`sum_k 1/g_k^4 = 3 (128 f^2 - 144 f + 27) / (16 f^4)`

and therefore

`f^12 * sum_k 1/g_k^4 = 24 f^10 - 27 f^9 + (81/16) f^8`.

So the pure term is an **eighth/tenth-degree** scalar polynomial in `f`.

### Result

These are real existing observable families, but neither one is the tuned cubic selector.

More importantly, the repo's own deep audit already recorded that they do **not** make `cos(9 delta)`
dominant automatically.

### Verdict

These families do not close the selector. They are concrete, but they are outside the exact cubic
target and still exhibit the lower-harmonic problem.

---

## 5. Candidate family D — trace observables of the diagonal Koide matrix

Let

`G(delta) = diag(g_0(delta), g_1(delta), g_2(delta))`.

Natural trace observables include `Tr G^n`.

Using Newton identities with `e1 = 3`, `e2 = 3/2`, `e3 = f`, the low power sums are:

- `Tr G = 3`
- `Tr G^2 = 6`
- `Tr G^3 = 27/2 + 3 f`
- `Tr G^4 = 63/2 + 12 f`
- `Tr G^5 = 297/4 + (75/2) f`
- `Tr G^6 = 351/2 + 108 f + 3 f^2`

### Result

Low trace powers are either:

- constant,
- linear in `f`,
- or only quadratic at sixth order.

So the obvious trace hierarchy on the diagonal Koide matrix does **not** naturally hit the tuned
cubic selector.

### Verdict

No existing low-order trace observable of the diagonal Koide matrix closes the phase selector.

---

## 6. Candidate family E — the repo's verbal "3-step return amplitude"

The main verbal PF-native proposal appears in
[koide_phase_anchor_pf_derivation.md](/mnt/d/Fundamentals/derivations/koide_phase_anchor_pf_derivation.md):

> if the single-step phase factor is `e^{i delta}`, then the 3-step return amplitude is
> `sum_k e^{i(delta + 2*pi*k/3)}` and a further cubic product would yield `e^{i 9 delta}`.

### Audit result

As written, this is not yet a valid observable derivation.

1. The literal sum

   `sum_{k=0}^2 e^{i(delta + 2*pi*k/3)}`

   vanishes identically, because the three cube roots of unity sum to zero.

2. The later expression in that note,

   `sum_{k=0}^2 e^{i(3 delta + 2*pi*k)} = 3 e^{i 3 delta}`,

   is already a post-reduction object in the `3 delta` sector, not a derived PF observable built
   from the original Koide factors.

3. No canonical operator, matrix, or effective action is written there whose trace or determinant
   actually produces the claimed scalar.

### Verdict

This is a **useful heuristic**, not a surviving theorem object.

It does not count as an existing observable that closes the selector.

---

## 7. Net result

The existing concrete repo observable families now separate cleanly:

| Family | Exact reduced form | Outcome |
|--------|---------------------|---------|
| symmetric product | `f` | too low degree |
| monomials | `f^k` | lower harmonics survive |
| cross-term | `-6 f^5 + (9/4) f^4` | concrete but outside cubic target |
| pure `W_3^2` term | `24 f^10 - 27 f^9 + (81/16) f^8` | concrete but outside cubic target |
| low trace powers `Tr G^n` | constants / linear / quadratic in `f` | no tuned cubic |
| verbal 3-step return amplitude | not a specified theorem object | heuristic only |

---

## 8. Final verdict

**No existing concrete PF / Koide observable in the repo currently reduces to the exact
Chebyshev-tuned cubic selector.**

This is therefore an honest bounded no-go for the current repo state:

> the determinant/product family is real but insufficient,
> the inverse-weight corrected Rivero-style families are real but still miss the selector,
> and the PF-native 3-step trace/product language has not yet been written as a canonical theorem
> object.

So the live search is now narrower:

1. either derive a genuinely new PF-native observable that lands on the tuned cubic,
2. or write a non-scalar matrix / trace object cleanly enough that its scalar reduction can be
   audited against the same target,
3. or admit that the current axioms still do not contain the phase selector.
