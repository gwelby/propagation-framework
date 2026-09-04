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

---

## 7. WAVE 5 UPDATE — 2026-03-25

**Algebraic precision check: δ_Koide vs sin²θ_W vs 2/9**

Executed inline Python check using PDG 2024 values: m_τ = 1776.86 ± 0.12 MeV; sin²θ_W (on-shell) = 0.22337; sin²θ_W (Casimir-derived) = 0.22310.

### Definitive numerical results

```
sin²θ_W (Casimir)   = 0.223101322300866
δ_Koide (PDG)       = 0.222229631490000
2/9                 = 0.222222222222222

gap A:  sin²θ_W − 2/9     = +8.791 × 10⁻⁴
gap B:  sin²θ_W − δ_Koide = +8.717 × 10⁻⁴
gap C:  δ_Koide − 2/9     = +7.409 × 10⁻⁶

δ_uncertainty (from m_τ ± 0.12 MeV) = 8.35 × 10⁻⁶ rad  [corrected 2026-09-04: was 2.58×10⁻⁴, a stale value 30.9× too large]
|δ_exact − 2/9|                      = 7.41 × 10⁻⁶ rad
ratio gap/uncertainty                = 0.89  [corrected: was 0.029, derived from stale uncertainty]
```

### Three conclusions

**1. δ_Koide IS 2/9 within measurement uncertainty.**
The gap of 7.4×10⁻⁶ is 0.89× the m_τ measurement uncertainty. Any future precision m_τ measurement within current uncertainty is fully consistent with δ_exact = 2/9 exactly. **Note (2026-09-04)**: the previous "0.029σ" was based on a stale uncertainty value 30.9× too large. The correct value is 0.89σ — still consistent, but much closer to the 1σ edge than previously stated. See Claude's Monte-Carlo verification (N=200k) and the τ-mass pre-registration trigger in CLAIMS.md.

**2. sin²θ_W ≠ 2/9 algebraically — definitively.**
The Casimir polynomial gives sin²θ_W = 1 − x₊(1/2)/x₊(1) = (−5 + 8√3 − √57)/(8(√3−1)).
Test: is this equal to 2/9?
```
56√3 − 9√57 = 29 ?
LHS = 29.046335306420374
RHS = 29.000000000000000
```
The LHS misses RHS by 4.63×10⁻², a structural gap, not numerical error.
**sin²θ_W (Casimir) = 2/9 is FALSE — algebraically distinct.**

**3. sin²θ_W ≠ δ_Koide exactly (0.4% gap is real).**
Gap B = 8.72×10⁻⁴. This is ~3.4× the m_τ uncertainty. If they were equal, it would require the Casimir polynomial to conspire with the PDG mass triple. They are related but not identical.

### Candidate gap expression

From alpha_casimir_hunt.py scan:
```
gap B ≈ α · (1 − x(1.5)) · x(1.5)²   at 0.317% error
```
where x(j) are Casimir polynomial roots. This uses only j ∈ {1/2, 1, 3/2} — the same roots that appear in the Weinberg angle derivation. No geometric mechanism identified yet.

### RG interpretation (audited 2026-04-13)

The earlier sentence

`sin²θ_W runs to δ_Koide at μ ≈ 97.9 GeV`

does **not** survive the T-021 convention audit.

- The direct on-shell quantity `1 - M_W^2/M_Z^2` is a fixed pole-mass ratio, not an RG trajectory.
- The effective leptonic angle `sin^2(theta_eff^ell)` is a Z-pole extracted observable, not a generic running definition.
- The legitimate running quantity in this pass is the `MS-bar` angle `s_hat^2(mu)`. Using current PDG inputs and a bounded one-loop SM helper gives `s_hat^2(98 GeV) = 0.231579930`, not `2/9`, and the PDG review places the electroweak minimum near `μ = M_W`, still above `2/9`.

So the RG bridge is removed. Any remaining Koide/Weinberg connection must be PF-native or explicitly convention-specific.

### Updated interpretation of Issue #5

The layered picture from Section 6 survives intact, but now with sharper distinctions:

- **δ_Koide = 2/9 is a measurement-consistent hypothesis** (not falsified, 0.89σ away — corrected 2026-09-04 from stale 0.029σ).
- **sin²θ_W ≠ 2/9** — these are two genuinely distinct quantities sharing a 0.4% proximity.
- **The proximity sin²θ_W ≈ δ_Koide ≈ 2/9** is triple: the Casimir-derived Weinberg angle, the Koide phase, and the simple fraction 2/9 all cluster within 0.4%. Whether this is a single derivation target or three separate coincidences is the key open question.

The most economical live interpretation is now narrower:

- `δ_Koide = 2/9` remains a measurement-consistent empirical anchor.
- `sin²θ_W(Casimir) = 0.22310` remains a nearby derived quantity.
- T-022 and T-021 both failed as selector bridges, so the shared-origin thesis is still open, not established.

**This remains the sharpest honest formal target for Issue #5, but not an upgraded derivation.**

**Issue #5 updated confidence: EMPIRICAL (0.60). sin²θ_W ≠ 2/9 confirmed algebraically. δ_Koide = 2/9 survives. Generic RG-crossing language removed on audit.**
