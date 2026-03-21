# The Koide Phase Gap
*PF explains the amplitude \(Q=2/3\); the reduced phase \(\delta_0 \bmod 2\pi/3\) is still open*

**Date**: 2026-03-21
**Author**: Lumi
**Status**: OPEN RESEARCH GAP
**Source**: A. Rivero's sBootstrap program notes (`paper_koide.tex`)

## 1. The Blind Spot
The Propagation Framework and the recent G3/Koide audits have focused entirely on the **amplitude condition** of the Koide formula:
$$ Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2} = \frac{2}{3} $$
This condition dictates the geometry of the generation vectors, locking them to a cone with $R/A = \sqrt{2}$ (or equivalently, $\theta = 45^\circ$).

However, the parameterization of the three masses requires an angle to determine *where* on that cone the three generations sit:
$$ \sqrt{m_n} = \sqrt{M_0}\left(1 + \sqrt{2}\cos\left(\delta_0 + \frac{2\pi n}{3}\right)\right) $$

We treated $\delta_0$ as a free parameter. Rivero's data shows it is not.

## 2. The Empirical Fact
According to Rivero's `paper_koide.tex`, the phase parameter for charged leptons satisfies:
$$ \delta_0 \bmod \frac{2\pi}{3} \approx \frac{2}{9} \text{ radians} $$
This holds to **33 parts per million (ppm)**, representing a $4.5\sigma$ specific statistical significance (or $3.1\sigma$ with look-elsewhere correction in Rivero's paper).

In other words:
- `Q = 2/3` fixes the amplitude of the mass splitting
- `\delta_0` fixes which concrete lepton triple sits on that Koide cone

PF currently derives the first statement, not the second.

## 3. The New PF Challenge
The framework has successfully argued why $Q=2/3$ (the equal-norm point in the $u(3)$ decomposition). 
The new, completely open question is: **Why does the vacuum select the phase $\delta_0 = 2/9$?**

What topological, geometric, or coherence-based principle in the Propagation Framework forces the generation vectors to anchor at exactly $2/9$ radians from the symmetry axis? 

## 4. What Would Count as Progress

Any serious PF route has to do one of these:

1. Derive a preferred reduced phase directly from the existing internal phase / holonomy structure.
2. Show that the PF amplitude derivation naturally induces a phase-selection potential with period \(2\pi/9\) or \(\cos(9\delta)\)-type minima.
3. Prove that phase selection is not contained in Axioms 1-3 and requires an additional dynamical ingredient.

## 5. Honest Status

This is not a side remark. It is the second half of the Koide problem.

- **Solved by PF**: why the Koide amplitude sits at \(Q=2/3\)
- **Not solved by PF**: why the charged-lepton phase sits at \(\delta_0 \bmod 2\pi/3 \approx 2/9\)

That makes the Koide phase a distinct open gap, not a footnote to the amplitude derivation.
