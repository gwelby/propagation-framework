# God Equation Path A: Directional Weak-Coupling Specification
*Formal interaction spec for the surviving extra-coupling version of Path A*

**Date**: 2026-04-06
**Author**: Codex
**Status**: DRAFT FOR AUDIT — model-extension spec, not a derivation
**Purpose**: Replace the stale chiral-only Path A target with the minimal interaction
structure that could actually generate a pure-shift closure route after the
2026-04-05 `\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3` audit.
**Builds on**: `path_a_chiral_b_to_zero.md`,
`path_a_spinor_cp_obstruction_2026-04-04.md`,
`god_eq_chiral_generation_locking_ansatz_2026-04-04.md`,
`path_a_z6_z3_chirality_intertwiner_audit_2026-04-05.md`,
`h_prod_joint_model_obligation.md`

---

## 0. Why This File Exists

The older Path A story was:

> weak chirality might by itself kill the backward branch.

That is no longer the live target.

The repo has now established three bounded facts:

1. `P_L` acting on spinor space alone does **not** change the generation-space ratio
   `|b/a|`; see `path_a_spinor_cp_obstruction_2026-04-04.md`.
2. A pure CP-odd phase deformation also does **not** change `|b/a|`; it changes
   interference, not the magnitude ratio.
3. The bare G1 `\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3` kinematics do **not** force any
   canonical chirality-direction lock; see
   `path_a_z6_z3_chirality_intertwiner_audit_2026-04-05.md`.

So the surviving Path A problem is narrower:

> specify an **extra weak-coupling structure** that can generate a real
> generation-directional asymmetry in the effective `\mathbb Z_3` operator.

This file states that structure as cleanly as possible.

---

## 1. Field Content

Take a spinor-generation field

\[
\Psi(x) \in \mathcal H_{\mathrm{spinor}} \otimes \mathbb C^3,
\]

with generation basis \(\{|0\rangle, |1\rangle, |2\rangle\}\) and quotient shift

\[
\bar S |j\rangle = |j+1 \bmod 3\rangle,
\qquad
\bar S^2 |j\rangle = |j-1 \bmod 3\rangle.
\]

The left/right chiral projectors act on the spinor factor:

\[
P_L = \frac{1-\gamma_5}{2},
\qquad
P_R = \frac{1+\gamma_5}{2}.
\]

The weak interaction remains left-chiral in the Standard Model sense. The extra structure
is **not** "replace `P_L` with `P_L \otimes \bar S` by fiat." The extra structure will live
inside the generation operator multiplying the weak current.

---

## 2. Minimal Directional Weak Vertex

The weakest extension consistent with the existing audits is:

\[
\mathcal L_{\mathrm{int}}
=
g_W\,
\bar\Psi \gamma^\mu W_\mu P_L\,
M_{\mathrm{gen}}(E)\,
\Psi
\;+\;\text{h.c.},
\]

with generation operator

\[
M_{\mathrm{gen}}(E)
=
c(E)\,I
+
\big(g(E)+\delta(E)+ i\varepsilon(E)\big)\bar S
+
\big(g(E)-\delta(E)- i\varepsilon(E)\big)\bar S^2.
\]

Interpretation of the three real functions:

- \(g(E)\): symmetric nearest-neighbor mixing strength
- \(\delta(E)\): **real directional asymmetry** between forward and backward generation shifts
- \(\varepsilon(E)\): CP-odd phase skew
- \(c(E)\): stay amplitude / diagonal generation component

This is the minimal family that contains all currently relevant cases:

- **chiral-only old route**: \(\delta=\varepsilon=0\)
- **pure CP-phase route**: \(\delta=0\), \(\varepsilon \neq 0\)
- **surviving extra-coupling route**: \(\delta \neq 0\)

It is also exactly the form isolated by the executable scan in
`sandbox/path_a_spinor_cp_scan.py`.

---

## 3. Effective `a,b,c` Coefficients

The induced effective generation-transition operator is

\[
T_{\mathrm{eff}}(E)
=
c(E)\,I + a(E)\bar S + b(E)\bar S^2
\]

with

\[
a(E)=g(E)+\delta(E)+i\varepsilon(E),
\qquad
b(E)=g(E)-\delta(E)-i\varepsilon(E).
\]

Therefore

\[
|a(E)|^2 = (g+\delta)^2+\varepsilon^2,
\qquad
|b(E)|^2 = (g-\delta)^2+\varepsilon^2,
\]

so

\[
\left|\frac{b}{a}\right|^2
=
\frac{(g-\delta)^2+\varepsilon^2}{(g+\delta)^2+\varepsilon^2}.
\]

This makes the existing no-gos explicit:

- if \(\delta=0\), then \(|b/a|=1\) even when \(\varepsilon \neq 0\)
- a nonzero \(\varepsilon\) alone cannot suppress the backward magnitude
- real directional asymmetry \(\delta>0\) is the first thing that can move the ratio

So the extra-coupling target is mathematically precise:

> Path A needs a mechanism that produces \(\delta(E)>0\) and drives the ratio above
> toward zero in the relevant IR regime.

---

## 4. The Exact IR Target

The pure-shift route needs more than "backward branch small."

For exact three-step diagonal closure on the one-hot reading, the clean target is

\[
T_{\mathrm{eff}}(E_{\mathrm{IR}}) \propto \bar S.
\]

In coefficient language, the sufficient target is

\[
\lim_{E\to \mathrm{IR}} \left|\frac{b(E)}{a(E)}\right| = 0
\qquad\text{and}\qquad
\lim_{E\to \mathrm{IR}} \left|\frac{c(E)}{a(E)}\right| = 0.
\]

The first condition suppresses the backward branch.
The second suppresses any stay amplitude.

If both hold, then after normalization

\[
T_{\mathrm{eff}} \to \bar S,
\qquad
T_{\mathrm{eff}}^3 \to I,
\]

which is the exact primitive-operator closure Path A wants.

This is stricter than the older `b/a -> 0` shorthand and should be used in future Path A work.

---

## 5. What Could Source `\delta(E)`?

This file does not derive `\delta`. It only isolates the allowed source classes.

Three possibilities remain logically open:

### 5.1 Explicit Directional Weak Coupling

The microscopic weak vertex already distinguishes the two quotient directions:

\[
M_{\mathrm{gen}} = g_{\mathrm{fwd}}(E)\bar S + g_{\mathrm{bwd}}(E)\bar S^2 + c(E)I
\]

with

\[
|g_{\mathrm{bwd}}/g_{\mathrm{fwd}}| \to 0
\quad\text{in the IR.}
\]

This is the most direct surviving Path A route.

### 5.2 CP-Violating Interference Plus Absorptive Splitting

Pure phase skew does not help by itself, but a CP-odd sector could still generate a real
directional split after integrating out additional fields or through loop-level absorptive parts.

In that case:

- \(\varepsilon(E)\) is not enough alone
- but \(\varepsilon(E)\) could participate in producing an effective real \(\delta(E)\)

This is a narrower and more honest CP route than the older "CP phase kills `b`" language.

### 5.3 PF-Native Selector / Stability Mechanism

A PF-native selector could destabilize one directed branch in the effective low-energy theory,
so that the surviving coarse operator has \(\delta(E)>0\) even if the microscopic bare coupling
started symmetric.

This would be the strongest route if derived, but it is the least specified today.

---

## 6. What Must Be Proven Next

Any serious Path A closure attempt now has to prove all of the following:

1. **Typed model extension**:
   define the enlarged state space and the weak vertex that produces
   \(M_{\mathrm{gen}}(E)\).

2. **Directional source theorem**:
   derive a nonzero real \(\delta(E)\), not just a phase \(\varepsilon(E)\).

3. **IR suppression theorem**:
   show that \(b/a \to 0\) and, if needed, \(c/a \to 0\) in the relevant infrared limit.

4. **Closure transfer**:
   show that the resulting effective operator really yields the position-space factorization
   needed for `H_prod`.

Without all four, Path A remains conditional.

---

## 7. What This File Does Not Claim

This file does **not** claim:

- that `\delta(E)` has been derived from Axioms 1-3
- that the `\mathbb Z_6/\mathbb Z_2 \to \mathbb Z_3` kinematics force the directional split
- that `P_L` alone closes Path A
- that `H_prod` is proved

This is a **specification of the surviving attack surface**, not a result upgrade.

---

## 8. Repo-Safe Summary

The current honest Path A interaction story is:

> weak chirality provides the spinor-side selection, but a real **generation-directional
> asymmetry** `\delta(E)` must come from additional coupling structure.

The minimal effective operator to study is

\[
T_{\mathrm{eff}}(E)
=
c(E)I
+
\big(g(E)+\delta(E)+ i\varepsilon(E)\big)\bar S
+
\big(g(E)-\delta(E)- i\varepsilon(E)\big)\bar S^2.
\]

The next successful Path A proof, if one exists, must derive this asymmetry from some explicit
microscopic mechanism rather than from chirality alone.
