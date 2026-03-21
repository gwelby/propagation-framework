# Koide Phase: PF ↔ Rivero Bridge Audit
*What the Propagation Framework naturally gives, and what Rivero's \(\cos(9\delta)\) mechanism adds*

**Date**: 2026-03-21  
**Author**: Codex  
**Status**: AUDIT COMPLETE — PF naturally gives \(2\pi/3\) periodicity and a \(\cos(3n\delta)\) tower; it does not yet single out \(\cos(9\delta)\)  
**Builds on**: `koide_phase_delta_0_gap.md`, `koide_geometric_equivalence.md`, `phase_closure_exact_model.md`, Rivero's `paper_koide.tex`, and `cos9delta_derivation.py`

---

## 1. The Question

Rivero's current work adds a missing ingredient to the Koide problem:

- PF already explains the **amplitude condition** \(Q = 2/3\)
- Rivero is arguing for a dynamical selection of the **phase** \(\delta_0\)

The sharp question is:

> does the existing PF internal phase / holonomy structure naturally lead to Rivero's
> \(\cos(9\delta)\) phase-selection mechanism?

This note answers that as narrowly and honestly as possible.

---

## 2. What Rivero Actually Has

From `paper_koide.tex`, any exact Koide triple can be parameterized as

\[
\sqrt{m_k}=\sqrt{M_0}\left(1+\sqrt{2}\cos\left(\frac{2\pi k}{3}+\delta_0\right)\right),
\qquad k=0,1,2.
\]

So:

- \(Q = 2/3\) fixes the amplitude ratio \(\sqrt{2}\)
- \(\delta_0\) determines where the triple sits on the Koide cone

Rivero then reports the charged-lepton empirical fact

\[
\delta_0 \bmod \frac{2\pi}{3} \approx \frac{2}{9}
\]

to 33 ppm.

The script `cos9delta_derivation.py` derives a specific dynamical route:

1. define
   \[
   f(\delta)=\prod_{k=1}^3 \left(1+\sqrt{2}\cos\left(\delta+\frac{2\pi k}{3}\right)\right)
   \]
2. this simplifies exactly to
   \[
   f(\delta)=-\frac12+\frac{\cos(3\delta)}{\sqrt{2}}
   \]
3. a specific superpotential / instanton term then uses powers of \(f\), in particular \(f^6\)
4. the Fourier expansion of \(f^6\) contains harmonics \(\cos(3n\delta)\) up to \(n=6\), including
   \(\cos(9\delta)\)

One important honesty point from Rivero's own script:

> \(\cos(9\delta)\) is **present but not dominant**. Lower harmonics such as \(\cos(3\delta)\) are
> larger unless additional cancellations occur.

So even on Rivero's side, the exact statement is more subtle than “the phase potential is simply
\(\cos(9\delta)\).”

---

## 3. What PF Already Gives Exactly

From `phase_closure_exact_model.md`, the observable generation sector is the quotient orbit

\[
\mathbb Z_6 / \mathbb Z_2 \cong \mathbb Z_3.
\]

That means the observable phase structure is intrinsically 3-cyclic:

\[
0 \to 1 \to 2 \to 0.
\]

So any generation-symmetric scalar phase function on the reduced Koide angle must respect

\[
V(\delta + 2\pi/3)=V(\delta).
\]

This is the exact PF bridge.

### Theorem 1

Any sufficiently regular reduced phase potential compatible with the PF three-generation cycle has
a Fourier expansion of the form

\[
V(\delta)=a_0+\sum_{n\ge 1}\Bigl(a_n\cos(3n\delta)+b_n\sin(3n\delta)\Bigr).
\]

If the phase-selection rule is also reflection-symmetric, \(V(\delta)=V(-\delta)\), then the
sine terms vanish and

\[
V(\delta)=a_0+\sum_{n\ge 1} a_n\cos(3n\delta).
\]

This is exact.

So PF does give a nontrivial structural result:

> Rivero's \(\cos(9\delta)\) is not alien to PF. It lives inside the exact PF-allowed
> \(\cos(3n\delta)\) harmonic tower.

---

## 4. What PF Does Not Yet Give

PF does **not** currently derive which harmonic in that tower should dominate.

That is the missing step.

The internal \(Z_3\) cycle explains why the reduced phase is naturally \(2\pi/3\)-periodic.
It does **not** explain why the preferred potential should single out

\[
n=3 \quad \Longrightarrow \quad \cos(9\delta)
\]

rather than

- \(\cos(3\delta)\)
- \(\cos(6\delta)\)
- a generic combination of \(\cos(3n\delta)\)

### Theorem 2

The existing PF kinematics determine the **periodicity class** of the phase potential, but not the
dominant harmonic.

Equivalently:

- PF currently explains the symmetry constraint
- Rivero's mechanism adds a specific dynamical selection rule

This is the cleanest statement of complementarity between the two programs.

---

## 5. Where the Number 9 Could Come From

There is one suggestive structural hint, but it is not yet a derivation.

Rivero's route combines:

1. the **threefold Koide orbit**
2. a **nonlinear determinant/product structure**
3. a further **power / instanton order**

That is qualitatively the sort of mechanism needed to move from bare \(Z_3\) periodicity to a
higher harmonic such as \(3 \times 3 = 9\).

But PF does not yet contain the analogue of:

- the determinant-based composite observable
- the instanton order
- the cancellation of lower \(\cos(3\delta)\) and \(\cos(6\delta)\) terms

So the current PF status is:

> compatible with \(9\delta\), not predictive of \(9\delta\).

---

## 6. Strongest Honest Bridge Statement

The best bridge statement the repo can currently support is:

> PF predicts that any reduced Koide phase potential must live in the \(2\pi/3\)-periodic Fourier
> tower \(\cos(3n\delta)\). Rivero's \(\cos(9\delta)\) mechanism is therefore structurally
> compatible with PF, but PF does not yet derive the \(n=3\) selection.

That is a real result. It is stronger than “interesting coincidence,” but weaker than “PF derives
Rivero's phase law.”

---

## 7. What Would Actually Close the Gap

There are three realistic ways forward.

### 7.1 Derive a PF composite phase observable

Find a natural PF observable built from the three-step internal phase cycle whose effective action is
cubic or otherwise nonlinear enough to generate a distinguished \(n=3\) harmonic in the
\(\cos(3n\delta)\) tower.

### 7.2 Derive cancellation of lower harmonics

Show that PF coherence or topological constraints eliminate \(\cos(3\delta)\) and
\(\cos(6\delta)\), leaving \(\cos(9\delta)\) as the first surviving term.

### 7.3 Admit new dynamics

Conclude that Axioms 1-3 fix the Koide amplitude but not the phase, and that phase selection needs
an additional dynamical ingredient of exactly the sort Rivero is modeling.

---

## 8. Final Verdict

| Question | Answer |
|----------|--------|
| Does PF naturally allow a \(2\pi/3\)-periodic phase potential? | **Yes** |
| Does that imply a \(\cos(3n\delta)\) Fourier tower? | **Yes** |
| Does PF currently single out \(n=3\), i.e. \(\cos(9\delta)\)? | **No** |
| Is Rivero's mechanism compatible with PF? | **Yes** |
| Is it currently derived by PF? | **No** |

**Net outcome**:

- PF and Rivero are talking about the same missing half of Koide
- PF supplies the symmetry class
- Rivero supplies a candidate dynamics
- the bridge between them is still open

---

*Written by Codex, 2026-03-21*  
*Purpose: separate exact PF phase symmetry from Rivero's stronger dynamical \(\cos(9\delta)\) claim*
