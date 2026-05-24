# The Propagation Framework: Audited Results and Open Frontiers
**Draft Status:** Publishable Core v3 — credibility-first release candidate  
**Date:** 2026-05-22  
**Authority:** Public claims in this draft defer to `CLAIMS.md`.

## Abstract

The Propagation Framework (PF) is a first-principles research program built from three commitments: propagation is fundamental, causal influence has a finite velocity, and stable structure requires coherence. The framework is not presented as complete. Its claims are tracked by explicit status: `DERIVED`, `PARTIAL DERIVATION`, `CONDITIONAL`, `ARGUED`, `EMPIRICAL`, or `INTUITION`.

The current strongest results are: charged-lepton Koide geometry as a derived geometric identity; null/static-stationary gravity as optical/Randers geometry; and the Weinberg angle from the Casimir polynomial plus Axiom 3b. The framework also records important positive constraints: neutrino masses do not satisfy charged-lepton Koide, which supports the interpretation that Koide is electromagnetic-sector specific. The major open frontiers remain the God Equation bridge, the Three Generations theorem stack, the Koide phase selector, and alpha.

## 1. The Three Axioms

1. **Propagation is Fundamental:** physical entities are modeled as stable propagation modes in a medium.
2. **Finite Causal Velocity:** the medium has a maximum causal signal speed.
3. **Coherence:** stable structures require closed, self-reinforcing propagation.

The canonical statements are maintained in `the_propagation_framework.md` and the canonical definition stack under `definitions/`.

## 2. Topological Weights and Fermion/Boson Partitioning
**Status:** PARTIAL DERIVATION  
**Confidence:** 0.85

In three dimensions, `π₁(SO(3)) ≅ Z₂` gives a clean two-class closure-order structure. The surviving exact mathematical content is that lifted closure orders naturally produce `(2,1)` as closure integers.

What is not closed: the physical-realization bridge. The current T1 audit says the `SU(2)` lift step survives as a conditional covering-space result, but strict physical population of the weight-2 branch still depends on the non-redundancy hypothesis `A_NR`, which has not been derived from Axioms 1-3.

## 3. The Number of Generations
**Status:** CONDITIONAL  
**Confidence:** 0.85

The algebraic assembly is exact once its prerequisites are granted:

$$Q(N) = \frac{2N}{2N+3}, \qquad Q(N)=\frac{2}{3} \Rightarrow N=3.$$

This does not yet make `N=3` a closed PF theorem. The numerator theorem depends on the T1 physical-realization bridge, and the denominator theorem `M=3` depends on T2 bridges including `C_mom`, `C_FP`, and `C_bridge`. The 2026-04-22 phi-harmonic closure route and the 2026-05-20 information-theoretic selector route both returned NO-GO / target-loaded audits.

## 4. Charged-Lepton Koide Geometry
**Status:** DERIVED  
**Confidence:** 0.95

The charged-lepton Koide quantity is:

$$Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2}.$$

For charged leptons, `Q ≈ 2/3`. In amplitude space, this is equivalent to the Foot cone / radius condition:

$$Q = \frac{2}{3} \iff \frac{R}{A} = \sqrt{2} \iff \theta = 45^\circ.$$

The U(3) scalar/traceless decomposition sharpens the algebra: `Q=2/3` is the equal-norm point between the scalar `u(1)` part and traceless `su(3)` part of the diagonal amplitude matrix. The open problem is not the equivalence; it is the deeper physical selector explaining why the charged-lepton sector lands on this point.

### 4.1 Neutrino Koide Non-Universality
**Status:** EMPIRICAL  
**Confidence:** 0.95

Current neutrino data do not satisfy `Q=2/3` under either mass ordering:

- Normal ordering: `Q_NO ≈ 0.550`
- Inverted ordering: `Q_IO ≈ 0.479`

This is a positive scope-delimiting result. PF currently treats charged-lepton Koide as an electromagnetic-sector identity. Purely weak-sector neutrinos lack the electromagnetic locking channel and are expected to deviate.

## 5. Gravity as Optical Geometry
**Status:** DERIVED  
**Confidence:** 0.95

The exact theorem is domain-restricted: null propagation in static gravity is optical geometry, and the stationary extension is Randers/Finsler geometry. The familiar scalar refractive-index model is the weak-field/static limit. This result should not be broadened into “all forces are refraction” without force-specific derivations.

## 6. Weinberg Angle
**Status:** DERIVED  
**Confidence:** 0.90

The Casimir polynomial

$$x^2 + C_2x - C_2 = 0$$

together with Axiom 3b (Minimal Winding Principle) yields:

$$\sin^2\theta_W \approx 0.22310.$$

This matches the PDG on-shell value to about `0.13σ`. The remaining open question is scheme/running: PF does not yet derive the observed effective running convention internally.

## 7. Biological Coherence and the 8h Sleep Constant
**Status:** ARGUED  
**Confidence:** 0.72

PF supports offline consolidation as a coherence-maintenance requirement, and the `(2,1)` encode/recover ratio gives a plausible `2/3` active and `1/3` recovery split. The exact human eight-hour constant is not derived from Axioms 1-3 alone.

## 8. Open Frontiers

1. **God Equation / matter scale:** CONDITIONAL 0.88. The verified error is `1.48%`. The active frontier is `G3-OP-MAP`: deriving or falsifying a PF-native oscillator-to-closure map. May 2026 audits closed trace-norm projection and Perron-Frobenius collapse as conditional negatives.
2. **Koide phase δ₀ ≈ 2/9:** EMPIRICAL. The numerical anchor is strong: `|δ - 2/9| = 7.4×10⁻⁶`, but all known selector lanes are fenced or negative. A PF-native selector is still open.
3. **Fine structure constant α:** ARGUED / structural. A `0.061%` Casimir expression exists, but the derivation is not closed.
4. **Consciousness metric:** INTUITION. PF language is suggestive, but no uniquely derived measurable exists.

## 9. Release Rule

This paper is release-safe only while every public claim maps back to `CLAIMS.md`. If `CLAIMS.md` and this paper conflict, `CLAIMS.md` wins.

## Conclusion

PF is strongest when it publishes both its wins and its failures. The credible public posture is not a declaration of completion. It is: a first-principles framework with several audited derived results, named open proof obligations, and falsifiable empirical frontiers.
