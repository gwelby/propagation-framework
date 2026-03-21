# G1: Exact Phase-Closure Model
*Integrating G4 and G5 into one explicit state-space specification*

**Date**: 2026-03-20  
**Author**: Codex  
**Task**: Specify the exact model for phase closure: state space, step operator, measure, and the meaning of closure.  
**Status**: MODEL SPECIFIED — supports the God Equation program, but does not by itself derive the \(N^{D/2}\) boundary scaling  
**Current claim status**: Consistent with `CLAIMS.md`, which keeps the God Equation at **ARGUED (0.75)**  
**Verification basis**: Read back against `generation_as_walk_steps.md`, `phase_closure_meaning.md`, `g1_model_specification_brief.md`, `phase_closure_volume_proof.md`, and `lambda_c_from_axioms.md`

---

## 1. Design Constraints

The exact model has to respect four facts already established elsewhere in the framework:

1. The walk is **not** a particle diffusing in Euclidean \(R^3\).
2. A "step" is a **discrete internal phase shift**, not a spatial translation.
3. The three generations are **not** an extra label attached to the walk. They are the three discrete phase positions of the walk itself.
4. Fermionic closure is lifted to the double cover: the observable 3-step phase cycle and the full spinorial closure are related, but not identical.

This file chooses one exact model and states it explicitly.

---

## 2. Model Choice

**Chosen model**: a **discrete quantum walk on the lifted internal phase orbit**.

This is the smallest exact model that integrates both:

- **G4**: generations are the phase steps
- **G5**: closure is an internal \(SU(2)\)/\(SO(3)\) topological event, not spatial return to the Euclidean origin

The model is intentionally minimal. It fixes the kinematics exactly, while leaving the God Equation's scaling and coupling bridge to later steps.

---

## 3. Exact State Space

### 3.1 Ambient Geometry

The ambient internal phase geometry is the spinorial rotation manifold:

\[
SU(2) \cong S^3
\]

with observable orientations obtained after quotienting by the center:

\[
SO(3) \cong SU(2) / \{\pm I\}.
\]

### 3.2 The Lifted Phase Orbit

Choose a fixed unit axis \(\hat n\) and the \(120^\circ\) phase-step element

\[
g = \exp\!\left(-\,i \frac{\pi}{3}\,\hat n \cdot \sigma\right) \in SU(2),
\]

so that in the observable \(SO(3)\) picture this is a \(2\pi/3\) rotation.

Its powers generate a six-point lifted orbit:

\[
\widetilde{\Omega} = \{I, g, g^2, g^3, g^4, g^5\},
\]

with

\[
g^3 = -I, \qquad g^6 = I.
\]

So the exact microscopic phase orbit is a \(\mathbb Z_6\) cycle.

### 3.3 Hilbert Space

The exact walk Hilbert space is

\[
\mathcal H = \ell^2(\widetilde{\Omega}) \cong \ell^2(\mathbb Z_6),
\]

with orthonormal basis states

\[
\{|k\rangle : k \in \mathbb Z_6\}.
\]

### 3.4 The Generation Quotient

Physical generations are not six distinct states. They are the three observable phase positions obtained by quotienting the lifted orbit by the central \(\mathbb Z_2\) deck transformation:

\[
q : \mathbb Z_6 \to \mathbb Z_3, \qquad q(k)=k \bmod 3.
\]

So the generation orbit is

\[
\Omega = \mathbb Z_6 / \mathbb Z_2 \cong \mathbb Z_3.
\]

This is the exact G4 integration:

\[
N_{\text{gen}} = |\Omega| = 3.
\]

The three generations are the three quotient nodes of the lifted phase orbit. They are not an external parameter.

---

## 4. Exact Step Operator

Define the one-step unitary shift operator

\[
S|k\rangle = |k+1 \bmod 6\rangle.
\]

This is one discrete \(120^\circ\) internal phase shift.

On the generation quotient, it induces

\[
\bar S |j\rangle = |j+1 \bmod 3\rangle.
\]

Therefore:

- one step = one generational transition
- three quotient steps traverse the full generation orbit
- six lifted steps traverse the full spinorial orbit

This removes the earlier ambiguity in `generation_as_walk_steps.md`. The model does **not** set walk length equal to generation count by hand. It defines generations as the quotient orbit of the walk.

---

## 5. What "Closure" Means in This Model

Define the deck-transformation operator

\[
J|k\rangle = |k+3 \bmod 6\rangle.
\]

Then

\[
S^3 = J, \qquad J^2 = I, \qquad S^6 = I.
\]

This yields two distinct closure notions.

### 5.1 Observable Generational Closure

On the quotient orbit \(\Omega \cong \mathbb Z_3\),

\[
\bar S^3 = I.
\]

So three steps complete the observable Koide triangle:

\[
0 \to 1 \to 2 \to 0.
\]

This is the closure relevant to the statement "there are three generations."

### 5.2 Spinorial Closure

On the lifted \(SU(2)\) orbit,

\[
S^3 = J \neq I, \qquad S^6 = I.
\]

So after three steps the walk has completed the observable cycle but has moved to the opposite spinor sheet; only after six steps does it return to the exact lifted identity state.

This matches the PF picture:

- **3-step closure** for the generational/orbital cycle
- **6-step closure** for the exact lifted spinorial cycle

The \(\mathbb Z_2\) structure is not extra. It is the exact topological content of the fermionic double cover.

---

## 6. Exact Measure and Return Object

### 6.1 Measure

For the exact discrete model, the natural measure is the normalized counting measure on \(\mathbb Z_6\):

\[
\mu(k) = \frac{1}{6}.
\]

If the model is later extended back into the ambient manifold \(SU(2)\), the corresponding continuum measure is Haar measure. But the exact G1 model itself is discrete.

### 6.2 Exact Return Amplitude

For the bare shift walk, the exact return amplitude to the lifted identity is

\[
A_n = \langle 0|S^n|0\rangle
=
\begin{cases}
1, & n \equiv 0 \pmod{6}, \\
0, & \text{otherwise}.
\end{cases}
\]

The exact return amplitude to the observable generation origin is

\[
\bar A_n = \langle [0]|\bar S^n|[0]\rangle
=
\begin{cases}
1, & n \equiv 0 \pmod{3}, \\
0, & \text{otherwise}.
\end{cases}
\]

This is exact, not asymptotic.

### 6.3 Honest Consequence

The exact G1 model does **not** produce

\[
P(0,N) \propto N^{-D/2}.
\]

Instead, it produces periodic closure:

- exact period 3 on the generation quotient
- exact period 6 on the lifted spinor orbit

So the earlier diffusion-style \(N^{-D/2}\) scaling is **not** the exact return object of the minimal generational walk.

If the \(N^{D/2}\) factor is real, it must come from an additional ingredient:

- amplitude spreading on the ambient \(SU(2)\) manifold before projection back to the orbit, or
- a different coarse-grained return kernel than the bare cyclic shift, or
- the coupling bridge itself in G3 rather than the exact walk kinematics in G1

That is a useful result, not a failure. It separates the exact kinematics from the still-open scaling claim.

---

## 7. Where \(D=3\) Enters

In this exact model, \(D=3\) does **not** mean Euclidean translation in \(x,y,z\).

It enters through the ambient internal geometry:

\[
\dim SU(2) = 3, \qquad \dim \mathfrak{su}(2) = 3.
\]

So the correct statement is:

- the exact walk is on a discrete orbit extracted from the 3-dimensional internal rotation manifold
- the bare orbit fixes the generation-step structure exactly
- the \(D=3\) exponent, if it survives, must come from how amplitude spreads in that ambient 3-dimensional phase geometry, not from the discrete orbit alone

This is the precise place where G2 and G3 begin.

---

## 8. What G1 Resolves

This file resolves the G1 specification problem at the kinematic level.

It now gives:

- an exact state space: \(\ell^2(\mathbb Z_6)\)
- an exact generation quotient: \(\mathbb Z_6/\mathbb Z_2 \cong \mathbb Z_3\)
- an exact step operator: the cyclic shift \(S\)
- an exact notion of closure: \(S^3\) for observable generational closure, \(S^6\) for lifted spinorial closure
- an exact measure: counting measure on the finite orbit
- an exact return object for the bare walk

It also integrates G4 exactly:

\[
N_{\text{gen}} = 3
\]

because the generation count is the size of the quotient orbit, not because a symbol was relabeled.

---

## 9. What Remains Open

This model does **not** yet close the God Equation.

The remaining open problems are now narrower:

1. What operator spreads amplitude over the ambient \(SU(2)\) phase manifold before closure is tested?
2. What is the exact return kernel of that ambient dynamics for the relevant small-\(N\) case?
3. How does that return object map to \(\alpha_{SO(3)}(l_P)\)?
4. Where does the \(2\pi\) normalization come from exactly?
5. Is the God Equation's \(N\) tied to the 3-step quotient closure, the 6-step lifted closure, or a coarse-grained quantity built from both?

Those are G2 and G3 problems. G1 is now specified.

---

## 10. Final Status

**Honest outcome**:

- The exact model now exists.
- The generation-step identity is no longer a free-floating assumption.
- The minimal exact walk does **not** itself generate the \(N^{-D/2}\) return law.

So the correct current status is:

- **G1**: specified
- **G4**: integrated into G1
- **God Equation**: still **ARGUED**

That is a stronger position than before, because the open structure is now more precise.

