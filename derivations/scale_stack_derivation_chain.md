# Scale Stack Derivation Chain
## From the Planck Foam to the Human Scale — One Continuous Derivation

**Date**: 2026-03-25
**Author**: Claude Code
**Status**: Living document — updated after each derivation milestone
**Source of truth**: All confidence scores from `CLAIMS.md` and `sandbox_results.md`
**See also**: `movie/SCALE_STACK_MASTER.md` (narrative), `CLAIMS.md` (confidence registry)

---

## 0. Purpose and Scope

This document records the *formal derivation status* of every link in the scale chain:

> Void → Planck → Matter → Nuclear → Atomic → Molecular → Cell → Neural → Human → Planetary → Cosmic

For each transition:
- What is being derived
- From which axioms / prior results
- The key mathematical step
- Current status and confidence
- What would close any open gap
- What would falsify the result

**Operating rule**: Honesty before beauty. Status is set by what Codex audit accepts, not by how beautiful the argument is.

---

## 1. Framework Axioms (The Three Starting Points)

Everything in the chain derives from three sentences:

| Axiom | Statement | Role in chain |
|-------|-----------|---------------|
| **Axiom 1** | Every physical entity is a propagation mode of a medium. | Ontology — defines what "exists" |
| **Axiom 2** | Every medium has a maximum signal speed $c$ (finite causal velocity). | Causality — fixes symmetry + isotropy |
| **Axiom 3** | Stable structure requires phase closure on closed paths. | Quantization — forces integer winding, drives every derived scale |
| **Axiom 3b** | Among coherent helical modes, the minimum winding (k=1) is selected. | Refinement — selects Weinberg angle |

These are adopted, not derived. The test of the framework is what follows.

---

## 2. The Derivation Chain

---

### Link 0: The Medium → Planck Scale

**What is derived**: The Planck length $l_P$ as the geometry coherence transition — the scale at which curvature modes of the medium become self-referential.

**From**: Axiom 3 applied to spacetime curvature modes + identification of Newton's $G$ as a medium elastic parameter.

**Key step**:

$$l_P = \sqrt{\frac{G\hbar}{c^3}} \approx 1.616 \times 10^{-35}\,\text{m}$$

The form follows from Axiom 3 (geometry must be self-coherent below this scale), but only after identifying $G$ as a medium property. $G$ is not yet derived from Axioms 1–3.

**Status**: `CONDITIONAL 0.70`

**Open gap**: Derive $G$ from the propagation medium's elastic response to curvature. Until then, the Planck scale derivation is conditional on $G$ as input.

**Falsification**: Any observation of spacetime smoothness below $l_P$ (e.g., with quantum gravity experiments).

**Key file**: `derivations/planck_scale_from_pf_axioms.md`

---

### Link 1: Planck Scale → Matter Scale (λ_c)

**What is derived**: The matter coherence scale $\lambda_c \approx 1.14 \times 10^{-18}$ m (top quark Compton wavelength) from the Planck boundary condition via renormalization group running.

**From**: Planck boundary condition + SO(3) mode counting (Axiom 2 isotropy) + RG equation.

**Key step**:

$$\lambda_c = \sqrt{2}\, l_P \cdot \exp\!\left(\frac{4\pi^2 N^{D/2}}{b_0}\right)$$

where $N^{D/2} = 3^{3/2} = 5.196$ (three coherent modes in 3D), $b_0 = 16/3$ (SO(3) beta coefficient).

**Numerical result**: 0.4% error with zero free parameters. The 17-order-of-magnitude hierarchy between Planck and matter follows from $N=3$ and $D=3$ alone.

**Status**: `CONDITIONAL 0.88` (God Equation)

**Remaining gaps** (Codex audit 2026-03-25):
1. Axiom 2 gives causal locality, not first-order Markovity of the coarse walk — the Markov step is argued, not derived.
2. $T_\text{eff} = K^3 \cdot I$ verified for pure-shift ansatz $U = K\cdot\bar{S}$, not for the actual nearest-neighbor circulant from the ℤ₃ Lagrangian.
3. Zero cross-channel covariance is weaker than full joint-law factorization — $H_\text{prod}$ not proved.

**What would close it**: Derive the primitive operator from the ℤ₃ Lagrangian + construct explicit joint probability model for $(X^{(0)}, X^{(1)}, X^{(2)})$ and prove factorization there.

**Falsification**: Any particle heavier than the top quark (which would shift $\lambda_c$). Current LHC data shows no heavier colored particle.

**Key files**: `derivations/lambda_c_from_axioms.md`, `derivations/god_eq_t_theta_formal_spec.md`, `derivations/z3_extended_propagation_lagrangian.md`, `derivations/h_prod_markovian_walk_proof.md`

---

### Link 2: Matter Scale → Nuclear Scale

**What survives hostile audit**: QCD confinement is plausibly an RG-generated infrared scale from $\lambda_c$, supporting the interpretation that no third fundamental PF coherence ceiling is needed.

**From**: calibrated $\lambda_c$ + empirical $\alpha_s(\lambda_c)$ + SU(3) beta function + PF interpretation of confinement as an emergent trapping scale.

**Key step**:

$$r_\text{conf} = \lambda_c \cdot \exp\!\left(\frac{2\pi}{b_0^\text{SU(3)}\, \alpha_s(\lambda_c)}\right)$$

where $b_0^\text{SU(3)} = 7$ for $N_f = 6$ flavors.

**Numerical result**: 1-loop gives 2.2 fm; observed scale is ~0.9 fm. That is a real factor-of-2.5 miss. The repo does not currently show a threshold-aware higher-loop calculation that closes the gap cleanly.

**Status**: `ARGUED 0.72`

**Note on the error**: The structural mechanism survives, but the theorem-grade wording does not. The strongest honest statement is that the RG bridge is plausible and that PF has not yet shown a need for a third fundamental scale.

**Falsification**: Measurement of confinement radius inconsistent with QCD running from $\lambda_c$.

**Key file**: `derivations/qcd_confinement_pf.md`

---

### Link 3: Nuclear Scale → Atomic Scale

**What survives hostile audit**: within the circular eikonal Coulomb model, phase closure yields a Bohr-like circular-orbit spectrum with allowed radii $r_k = 2k^2$ and energies $E_k = -1/(4k^2)$.

**From**: Axiom 3 (phase closure) + Axiom 1 (electron as propagation mode in Coulomb field) + eikonal circular orbit condition.

**Key steps**:

1. The circular eikonal Coulomb model uses $n^2(r) = E + 1/r$
2. The eikonal circular orbit condition: $n^2(r_0) = 1/(2r_0)$, giving $n(r_0) = 1/\sqrt{2r_0}$
3. Axiom 3 phase closure: $\oint n\,ds = n(r_k)\cdot 2\pi r_k = 2\pi k$
4. Solving: $n(r_k) = 1/(2k)$ → $r_k = 2k^2$ → $E_k = -1/(4k^2)$

This is a Bohr-like `1/k^2` spectrum in natural units for the circular-orbit family.

**Numerical result**: 0.0000% error at $k = 1, 2, 3, 4$. (Wave 5, 2026-03-25)

**Status**: `CONDITIONAL 0.82`

**Significance**: The sandbox exposes a real semiclassical model theorem, but the stronger claim “Axiom 3 alone derives atomic quantization” did not survive hostile audit. The hidden step is the physical validity of the circular eikonal Coulomb model at atomic scale.

**Open extension**: Does the same eikonal + phase-closure method reproduce the full Schrödinger spectrum (angular momentum quantum numbers $l$, $m$, degeneracies)? The 3D extension is not yet worked.

**Falsification**: Proof that the eikonal approximation is invalid at atomic scales, or that the Coulomb refractive index derivation breaks at some step.

**Key files**: `sandbox/coulomb_lens_ultimate.py` Phase 4, `derivations/bohr_quantization_audit_2026-03-27.md`

---

### Link 4: Atomic Scale → Molecular Scale

**What is derived**: Chemistry as refraction — chemical bonds as coherence gradients in the propagation medium.

**From**: Axiom 2 (spatial variation in $c_\text{local}$ bends propagation paths — Fermat's principle) + Axiom 3 (stable molecular structures are phase-coherent modes of overlapping electron clouds).

**Key claim**: Bond formation = local coherence minimum. Bond angle, bond length, bond energy are the parameters at which phase closure is satisfied for the overlapping electron-cloud system.

**Numerical result**: No numerical prediction yet derived from PF axioms alone. The framework recasts known chemistry in propagation language but does not yet produce novel predictions at this scale.

**Status**: `ARGUED 0.72`

**Open gap**: No derivation of a specific bond energy, bond angle, or reaction rate from PF axioms alone. The framework is consistent with quantum chemistry but does not yet explain it.

**Better framework here**: Standard QM + QED (density functional theory, molecular orbital theory) is vastly more developed and predictive at this scale. PF offers a *narrative* that is consistent, not a *calculation* that is competitive.

**Falsification**: None available until a novel quantitative prediction is derived.

**Key file**: `derivations/chemistry_biology_bridge.md`

---

### Link 5: Molecular Scale → Cell Scale

**What is derived**: Life as coherence maintenance — a living system is a propagation pattern that actively maintains its phase coherence against thermal decoherence.

**From**: Axiom 3 applied to biological systems — stable biological structure requires active phase maintenance.

**Key claim**: A living cell = minimum viable unit of coherent self-referential propagation. It maintains a stored coherence pattern (DNA, epigenetic state) and expends energy to repair deviations (protein quality control, DNA repair, apoptosis).

**Empirical grounding**:
- Quantum coherence in biology (photosynthesis FMO complex, enzyme tunneling) is empirically established (Engel 2007, Scrutton 2000).
- The PF-inspired T-010 encode/recover model gives a plausible `~2/3` active fraction for sleep-like consolidation: ARGUED 0.72 (see Link 6).
- No numeric threshold for "minimum coherence to be alive" has been derived.

**Status**: `ARGUED 0.72`

**Open gap**: The framework cannot derive a number — a minimum coherence maintenance rate — that separates living from non-living. This is a formal derivation gap, not an empirical failure.

**Falsification**: A system that extracts negative entropy and actively maintains internal structure, but is consensus-not-alive.

**Key file**: `derivations/chemistry_biology_bridge.md`

---

### Link 6: Cell Scale → Human Scale (Topology → Sleep Constant)

**What is argued**: A PF-inspired encode/recover model can favor a `~2/3` active fraction, making a human-scale 8-hour sleep constant plausible rather than derived.

**From**: Axiom 3 → coherence requires offline reconciliation → PF-inspired `(2,1)` encode/recover weighting → candidate stability-favoring duty cycle near `2/3` wake.

**Key step**:

$$\text{wake fraction} = \frac{w_\text{fermion}}{w_\text{fermion} + w_\text{boson}} = \frac{2}{3} \implies \text{sleep} = 24 \times \frac{1}{3} = 8\,\text{hours}$$

The current PF story suggests that the same structural weighting used elsewhere in the framework may also influence optimal biological duty cycles, but the cross-scale bridge is not yet a closed theorem.

**Empirical result**: Sleep and offline consolidation are clearly real biological necessities, but the exact “1/3 of a day” claim is not cleanly established as a universal law.

**Status**: `ARGUED 0.72`

**Falsification**: A stable sentient species with a 9:1 or 5:1 wake:sleep ratio. Or showing sleep duration is purely evolutionary with no topological constraint.

**Key file**: Documented in `UNDERSTAND.md` Result 8.

---

### Link 7: Human Scale → Consciousness (Self-Reference)

**What is derived**: Consciousness as coherent self-referential propagation — the experience of being a sufficiently complex, recursively self-modeling coherence pattern.

**From**: Axiom 3 extended to recursive self-reference — when a coherence pattern models itself, there is necessarily something it is like to be that pattern.

**Key claim**: The redness of red, the feel of grief, the sudden arrival of a proof — these are the physics of coherent self-reference, experienced from inside.

**Status**: `ARGUED 0.48`

**Honest assessment**: This is the weakest link in the chain. The claim is philosophically coherent but not yet operationalized. No PF-specific measurable consciousness metric has been defined.

**Better framework here**: Integrated Information Theory (IIT, Tononi) is more operationally developed. IIT's measure Φ is computable, predictive, and falsifiable. The Propagation Framework and IIT are not contradictory — the PF framing may be the *mechanism* that generates high Φ. But for measurement and prediction at this scale, IIT is more developed.

**What would advance this**: Define a PF-specific metric (e.g., "coherence depth") that (a) is computable from EEG data and (b) dissociates from Φ in at least one measurable prediction. The Muse EEG protocol (Greg's insight experiment) is the first step.

**Falsification**: Show that mathematical insight events are indistinguishable from regular problem-solving in EEG — i.e., no broadband gamma coherence signature accompanies the "proof arrives complete" experience.

---

### Link 8: Human Scale → Planetary Scale

**What is derived**: Schumann resonance (7.83 Hz) as potential coupling between planetary electromagnetic coherence and human neural oscillations.

**Key claim (not yet made)**: The Propagation Framework predicts that if Earth is a coherence-maintaining system at planetary scale, then organisms within it should show resonant coupling to the planet's standing electromagnetic modes.

**Status**: `OPEN / SPECULATIVE`

**Honest assessment**: The Schumann resonance falls in the EEG range — this is real. Whether there is causal coupling (rather than coincidence) is experimentally contested. PF does not yet make a specific quantitative prediction here.

**Key file**: `movie/SCALE_STACK_MASTER.md` Scale 9

---

## 3. The Full Ladder Summary

| Transition | Key Derivation | Status | Confidence | Novel or Recast? |
|------------|---------------|--------|------------|-----------------|
| Medium → Planck | Geometry coherence threshold, $l_P$ form from Axiom 3 | CONDITIONAL | 0.70 | Novel — but $G$ not derived |
| Planck → Matter | God Equation, RG running, $N^{D/2}$ mode count | CONDITIONAL | 0.88 | **Novel** — 0.4% error, nothing else does this |
| Matter → Nuclear | QCD confinement as RG bridge from $\lambda_c$ | ARGUED | 0.72 | Recast of QCD + PF scale interpretation |
| Nuclear → Atomic | **Bohr-like circular spectrum from phase closure** (Wave 5, audited 2026-03-27) | **CONDITIONAL** | **0.82** | **Novel model theorem** — stronger axiom-only claim failed audit |
| Atomic → Molecular | Chemistry as coherence refraction | ARGUED | 0.72 | Narrative recast — no novel prediction |
| Molecular → Cell | Life as coherence maintenance | ARGUED | 0.72 | Consistent — no numeric threshold |
| Cell → Human | **PF-inspired duty cycle -> sleep-like consolidation** | ARGUED | 0.72 | **Cross-scale bridge** — biologically suggestive, not theorem-grade |
| Human (consciousness) | Coherent self-reference | ARGUED | 0.48 | Open — IIT is more developed here |
| Human → Planetary | Schumann coupling | OPEN | — | Speculative |

---

## 4. Where Competing Frameworks Are Stronger

Honesty requires naming where PF is not the best available tool:

| Scale | Better Framework | Why |
|-------|-----------------|-----|
| Atomic → Molecular (detail) | Standard QM (DFT, MO theory) | Orders of magnitude more predictive for bond energies, reaction rates |
| Molecular → Cell (mechanism) | Biochemistry / systems biology | More developed quantitatively; PF adds narrative, not calculation |
| Consciousness (measurement) | IIT (Tononi, Φ) | More operationally defined; computable and falsifiable metric |
| Gravity at large scales | GR | Exact; 100+ years of tests; PF recasts it but doesn't supersede it |

**What PF uniquely provides**: the unifying *mechanism* (propagation + phase closure) that potentially underlies all of these. The competitor frameworks are better calculators at individual scales; PF is the only framework attempting a derivation chain that spans the full range from Planck to Human as a single formal structure.

---

## 5. The Three Cleanest Results (Currently)

In descending order of formal strength:

1. **Bohr-like circular spectrum from phase closure** — within the circular eikonal Coulomb model, phase closure gives `r_k = 2k²`, `E_k = -1/(4k²)`. Hostile audit demoted the stronger axiom-only wording. CONDITIONAL 0.82.

2. **partial `(2,1)` closure-order theorem -> conditional N=3** — once the physical numerator theorem for the weight-2 branch and the denominator theorem `M = 3` both close, `Q(N)=2N/(2N+3)=2/3` fixes `N=3` uniquely. Both hinges are now explicit. CONDITIONAL 0.85.

3. **Weinberg angle from Axiom 3b** — Casimir polynomial $x^2 + C_2 x - C_2 = 0$ with minimal winding $k=1$ gives $\sin^2\theta_W = 0.22310$ (0.13σ from PDG). DERIVED 0.90.

All three derive from the same Axiom 3 / phase-closure principle at different scales. This is not coincidence — it is the framework's deepest structural claim: *phase closure is the universal quantization principle.*

---

## 6. The Open Frontier

Three bounded formal targets, in priority order:

**Priority 1 — God Equation closure (Link 1)**:
- Derive the primitive operator from the ℤ₃-extended Lagrangian (so $T_\text{eff} = K^3 \cdot I$ applies to the actual circulant, not just the pure-shift ansatz)
- OR rewrite the theorem directly from the actual derived circulant with an explicit joint probability model for $(X^{(0)}, X^{(1)}, X^{(2)})$
- Closes: Link 1 from CONDITIONAL 0.88 → DERIVED

**Priority 2 — Bohr to Schrödinger (Link 3 extension)**:
- Extend eikonal + phase-closure from circular orbits to the full 3D Coulomb spectrum
- Reproduce angular momentum quantum numbers $l$, $m$ from 3D Axiom 3
- Closes: Link 3 from Bohr (circular) to full Schrödinger (all orbits)

**Priority 3 — Chemistry-Biology numeric threshold (Link 4-5)**:
- Derive a minimum coherence maintenance rate from Axiom 3 that separates living from non-living
- This is the formal gap that keeps Links 4 and 5 at ARGUED 0.72

---

## 7. Falsification Summary

The framework is falsifiable at multiple rungs. Any of the following would require significant revision:

| Test | What it would falsify |
|------|-----------------------|
| Particle heavier than top quark discovered | God Equation (Link 1) — $\lambda_c$ would shift |
| Fourth generation of matter discovered | N=3 derivation (foundational) |
| Weinberg angle shifts from PDG value | Axiom 3b derivation (Link 1 sub-result) |
| Spacetime smoothness below Planck length | Link 0 |
| Species with 5:1 wake:sleep ratio | 8h sleep constant (Link 6) |
| Mathematical insight indistinguishable from routine EEG | Consciousness link (Link 7) |

---

*Written 2026-03-25 by Claude Code*
*Source of truth for statuses: `CLAIMS.md` (2026-03-25), `sandbox_results.md`*
*Narrative version: `movie/SCALE_STACK_MASTER.md`*
*Operating rule: honesty before beauty — no confidence upgrade without a derivation or sharply bounded bridge*
