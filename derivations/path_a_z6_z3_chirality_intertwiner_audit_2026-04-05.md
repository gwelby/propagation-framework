# Path A: Formal Audit of the $\mathbb Z_6 \to \mathbb Z_3$ Chirality-Intertwiner Question

**Date**: 2026-04-05  
**Author**: Codex  
**Status**: BOUNDED NO-GO — the bare G1 kinematics do not force chiral-generation locking  
**Scope**: Path A only (`H_prod` primitive-operator route)  
**Builds on**: `phase_closure_exact_model.md`, `product_walk_bridge_model.md`,
`g1_model_specification_brief.md`, `path_a_chiral_b_to_zero.md`,
`path_a_spinor_cp_obstruction_2026-04-04.md`,
`god_eq_chiral_generation_locking_ansatz_2026-04-04.md`

---

## 0. Executive Summary

The exact G1 model fixes:

- the lifted internal orbit \(\ell^2(\mathbb Z_6)\)
- the deck transformation \(J=S^3\)
- the quotient map \(q:\mathbb Z_6 \to \mathbb Z_3\)
- the induced observable shift \(\bar S\)

It does **not** fix:

- any spacetime spinor factor
- any chirality operator \(\gamma_5\), \(P_L\), or \(P_R\)
- any weak-coupling layer tying internal motion to spacetime chirality

The audit question was:

> Can the bare \(\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3\) kinematics force a canonical
> intertwiner between quotient direction \((\bar S \text{ vs } \bar S^2)\) and spacetime
> chirality \((P_L \text{ vs } P_R)\)?

**Answer: No.**

Three independent reasons close the question:

1. The deck transformation is central and acts trivially on the quotient, so the
   \(\mathbb Z_2\) lift data cannot distinguish \(\bar S\) from \(\bar S^2\).
2. The quotient \(\mathbb Z_3\) has no preferred generator: \(\bar S\) and \(\bar S^2\)
   are exchanged by the inversion automorphism, and the bare G1 data does not break that symmetry.
3. There is no nontrivial homomorphism \(\mathbb Z_3 \to \mathbb Z_2\), and G1 contains no
   spacetime spinor representation anyway, so a chirality-direction lock is not present as typed data.

Therefore:

> **Chiral-generation locking is not derivable from the current G1 kinematics alone.**

If Path A is to survive, the lock must come from **additional coupling structure**
outside bare G1, or else be adopted explicitly as a new model postulate.

---

## 1. Exact G1 Data

From `phase_closure_exact_model.md`, the exact internal kinematics are:

\[
\mathcal H_{\mathrm{int}} = \ell^2(\mathbb Z_6),
\qquad
S|k\rangle = |k+1 \bmod 6\rangle,
\qquad
J := S^3.
\]

The deck transformation satisfies:

\[
J^2 = I,
\qquad
S^6 = I,
\qquad
J = S^3.
\]

The observable generation quotient is:

\[
q:\mathbb Z_6 \to \mathbb Z_3,
\qquad
q(k)=k \bmod 3,
\]

with induced observable shift:

\[
\bar S |j\rangle = |j+1 \bmod 3\rangle,
\qquad
\bar S^3 = I.
\]

This is all internal finite-group kinematics. No spacetime spinor sector appears in the model.

---

## 2. Lemma 1: The Deck Transformation Does Not Reverse the Walk

### Claim

The deck transformation \(J=S^3\) does **not** conjugate the lifted forward shift \(S\) to
its inverse \(S^{-1}\). Instead:

\[
JSJ^{-1} = S.
\]

### Proof

Because the group is abelian:

\[
JSJ^{-1} = S^3 S S^{-3} = S.
\]

Equivalently, \(J\) is central in \(\mathbb Z_6\), so it commutes with every group element.

\[
\square
\]

### Consequence

The \(\mathbb Z_2\) lift structure is **not** an orientation-reversing operation on the
internal orbit. It cannot identify "left sheet" with forward motion and "right sheet"
with backward motion. The deck operation preserves the direction of the walk.

---

## 3. Lemma 2: The Deck Transformation Acts Trivially on the Observable Quotient

### Claim

The deck transformation induces the identity map on \(\mathbb Z_3\):

\[
q \circ J = q.
\]

### Proof

For any \(k \in \mathbb Z_6\),

\[
q(Jk) = q(k+3) = k+3 \pmod 3 = k \pmod 3 = q(k).
\]

So the central \(\mathbb Z_2\) action disappears after quotienting.

\[
\square
\]

### Consequence

The observable generation sector remembers the 3-cycle, but it forgets the deck label.
Therefore the \(\mathbb Z_2\) data cannot distinguish the two nontrivial quotient directions
\(\bar S\) and \(\bar S^2\).

This is already enough to block the desired lock:

\[
(\text{deck } \mathbb Z_2) \not\Rightarrow (\bar S \text{ vs } \bar S^2).
\]

---

## 4. Lemma 3: The Observable Quotient Has No Preferred Generator

### Claim

Within the bare quotient data, \(\bar S\) and \(\bar S^2\) are related by the inversion
automorphism of \(\mathbb Z_3\):

\[
\iota(j) = -j \pmod 3,
\qquad
\iota \bar S \iota^{-1} = \bar S^2.
\]

### Proof

Let \(\iota |j\rangle = |-j\rangle\). Then:

\[
\iota \bar S \iota^{-1} |j\rangle
= \iota \bar S |-j\rangle
= \iota |1-j\rangle
= |j-1\rangle
= \bar S^2 |j\rangle.
\]

So \(\bar S\) and \(\bar S^2\) are exchanged by an automorphism of the quotient cycle.

\[
\square
\]

### Consequence

The bare G1 quotient data gives a 3-cycle, but not a canonical orientation on that cycle.
Any claim that the quotient itself singles out \(\bar S\) over \(\bar S^2\) must therefore
introduce structure beyond the quotient kinematics.

---

## 5. Lemma 4: There Is No Nontrivial Group-Theoretic Map from Quotient Direction to Chirality

If chirality is treated as a two-valued sign structure, its algebraic shadow is \(\mathbb Z_2\).

Any attempt to derive a chirality label directly from the observable generation quotient would
require a nontrivial map

\[
f:\mathbb Z_3 \to \mathbb Z_2.
\]

But every group homomorphism \(\mathbb Z_3 \to \mathbb Z_2\) is trivial, because:

\[
f(3 \cdot 1) = 3 f(1) = 0 \quad \text{in } \mathbb Z_2,
\]

and the only element of \(\mathbb Z_2\) with \(3x=0\) is \(x=0\).

So:

\[
\mathrm{Hom}(\mathbb Z_3,\mathbb Z_2) = 0.
\]

### Consequence

The observable quotient cycle carries no intrinsic two-valued chirality tag.
The 3-cycle and a left/right splitting are algebraically different kinds of structure.

This does **not** prove that a larger coupled model can never relate them.
It proves the narrower statement that the relation is not forced by the bare quotient group itself.

---

## 6. Lemma 5: G1 Does Not Even Contain the Target Chirality Operator

The desired locked vertex has the form

\[
V_{\mathrm{lock}} \sim P_L \otimes \bar S + P_R \otimes \bar S^2.
\]

But the G1 model defines only:

- an internal Hilbert space \(\ell^2(\mathbb Z_6)\)
- internal shift operators \(S\) and \(\bar S\)

It does **not** define:

- a spacetime spinor Hilbert space
- a Lorentz or \(\mathrm{Spin}(1,3)\) representation
- \(\gamma_5\), \(P_L\), or \(P_R\)

So the proposed lock is not merely *unproven* in G1. It is not even a well-typed operator in the
G1 model by itself. To write it, one must enlarge the state space to something like

\[
\mathcal H_{\mathrm{spinor}} \otimes \ell^2(\mathbb Z_6)
\]

and specify an interaction law tying the two factors together.

That interaction law is precisely the missing extra structure.

---

## 7. Representation-Theoretic Reading

The regular representation of \(\mathbb Z_6\) decomposes into six one-dimensional characters.
The observable quotient keeps exactly the characters trivial on the deck element \(J=S^3\), namely:

\[
1,\quad \omega,\quad \omega^2
\qquad
(\omega = e^{2\pi i /3}).
\]

These are the three characters of \(\mathbb Z_3\). Both nontrivial quotient directions live in
this same quotient character set.

Crucially:

- the deck element \(J\) acts as \(+1\) on all quotient characters
- so deck parity does not split \(\omega\) from \(\omega^2\)
- the only built-in distinction supplied by the lift is "quotient-visible" vs "quotient-odd",
  not "forward" vs "backward"

So the \(\mathbb Z_6\) lift gives the existence of the 3-cycle, but not an orientation/chirality
pairing on that cycle.

---

## 8. Audit Verdict

The bare \(\mathbb Z_6 \to \mathbb Z_3\) kinematics support:

1. a lifted six-step spinorial orbit
2. an observable three-step quotient orbit
3. exact cyclic closure

They do **not** support:

1. an orientation-reversing deck action
2. a preferred generator of the quotient cycle
3. a canonical map from quotient direction to a two-valued chirality label
4. a spacetime chiral operator at all

Therefore the answer to the audit question is:

> **No canonical chirality-direction intertwiner is forced by the current G1 kinematics.**

The Chiral-Generation Locking Ansatz is therefore **not derivable from bare G1**.

The strongest honest Path A statement is now:

> If a future extended model adds a spinor sector plus an interaction law that ties quotient
> direction to chirality, then a pure-shift closure route may exist.
> But that lock is additional coupling structure, not a theorem of the present
> \(\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3\) kinematics.

---

## 9. What Would Be Needed to Reopen Path A on Existing PF Structure

To rescue Path A without declaring a new postulate, one would need an actual derivation of one of:

1. a canonical lift-to-spinor map in which the deck \(\mathbb Z_2\) is identified with
   spacetime chirality rather than merely spinorial sheet exchange
2. an interaction theorem showing that the only allowed weak vertex consistent with the full
   enlarged model is
   \[
   P_L \otimes \bar S + P_R \otimes \bar S^2
   \]
3. a deeper PF selector principle that dynamically suppresses one quotient direction and thereby
   creates the lock in the effective IR theory

None of those are present in the current G1 data.

---

## 10. Repo-Safe Consequence

This audit does **not** kill Path A completely.

It kills the narrower claim that:

> the bare \(\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3\) kinematics already contain the
> chiral-generation lock.

After this audit, Path A survives only in the following weakened form:

> find or justify an **extra directional coupling structure** that produces
> \(b/a \to 0\) in the IR.

That is a model-extension problem, not a closure theorem from the current axioms plus G1 alone.
