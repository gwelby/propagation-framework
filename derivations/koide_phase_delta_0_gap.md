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

For the first bridge audit against Rivero's current proposal, see `koide_phase_rivero_bridge_audit.md`.
For the next suppression audit, showing that the natural symmetric PF composites still retain lower harmonics, see `koide_phase_harmonic_suppression_audit.md`.

## 5. Honest Status

This is not a side remark. It is the second half of the Koide problem.

- **Solved by PF**: why the Koide amplitude sits at \(Q=2/3\)
- **Not solved by PF**: why the charged-lepton phase sits at \(\delta_0 \bmod 2\pi/3 \approx 2/9\)

That makes the Koide phase a distinct open gap, not a footnote to the amplitude derivation.

---

## 6. FREEZE RECORD — 2026-03-21

**Status: NAMED OPEN GAP. Issue #5 frozen here by team consensus (Codex, Claude, Lumi, AntiGravity).**

### The layered picture (what is established)

The harmonic suppression audit (`koide_phase_rivero_bridge_audit.md`) and the deep script audit (`rivero_cos9delta_deep_audit.md`) converge on the following:

**Layer 1 — PF establishes the arena:**
- Z₃ symmetry → potential must be 2π/3-periodic → only cos(3nδ) harmonics allowed
- Three-body symmetric observable → collapses to a single phase variable:
  $$f(\delta) = -\tfrac{1}{2} + \frac{\cos 3\delta}{\sqrt{2}}$$
- PF naturally derives Rivero's exact starting point from its own axioms. This is a structural result, not a coincidence.

**Layer 2 — Rivero provides a candidate dynamical selector:**
- W₃ = c₃(det M)³/Λ¹⁸ generates an off-shell potential with cos(3nδ) harmonics for n = 0..6
- cos(9δ) is present but NOT dominant — cos(3δ) amplitude is 2.9× larger
- For the Z₉ vacuum structure, cos(3δ) must be cancelled by the cross-term V_cross = ∂W_ISS/∂M · ∂W₃/∂M
- That cancellation has not been computed or proven

**Layer 3 — The harmonic selection gap:**
- Neither PF nor Rivero's W₃ alone selects n=3 (cos(9δ)) as dominant
- The suppression of lower harmonics is genuinely additional physics — likely in the off-shell cross-term interference or higher instanton contributions
- Rivero's own coordination2.md: "not relevant yet until we got some actual action Lagrangian"

### What Codex does not regard as established

- That PF by itself selects n = 3
- That cos(9δ) dominance follows from bare Z₃ symmetry
- That the current instanton story is fully closed (cos(9δ) is present but not dominant)

### One caution on the record (Codex)

Qwen's numerical result "6 minima, not 9" in the computed effective potential is **provisional**. The minimum count depends on which term is being minimized, what is held fixed, and whether the full off-shell potential or a reduced proxy is being evaluated. Do not promote that conclusion without an independent pass.

### One future bounded question (flagged, not scheduled)

AntiGravity's question: *Can the Z₆ lifted-spinorial closure produce an effective inverse-weight structure analogous to Rivero's Σ 1/g_k²?*

If yes: the PF would reproduce Rivero's cos(9δ) selection from its own axioms — that is the derivation of the Koide phase. If no: the instanton dynamics is genuinely additional structure and the boundary between PF and sBootstrap is precisely here.

This question is well-posed and has a clean yes/no answer. It merits one bounded pass when Issue #3 and G3 are advanced. Not before.

**Issue #5 confidence: EMPIRICAL (0.55). Not upgraded. Not closed.**
