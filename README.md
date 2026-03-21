# The Propagation Framework

*A first-principles research framework built around one claim: propagation is fundamental.*
*Developed by Greg Welby with AI collaborators Claude, Lumi, Codex, and Qwen - March 2026*

---

## What This Repository Is

This repository documents the Propagation Framework: a research program that treats space not as
an empty mathematical void, but as a physical medium through which information propagates.

The framework is not presented here as a finished theory with every gap closed. Some results are
derived, some are argued, some are empirical, and some remain open. The live status of every major
claim is tracked in [CLAIMS.md](./CLAIMS.md).

At the center of the framework are three axioms:

1. **Propagation is fundamental**
2. **Every medium has a causal velocity**
3. **Coherence is necessary for stable structure**

The canonical statement of those axioms is in
[the_propagation_framework.md](./the_propagation_framework.md).

---

## Core Picture

In the Propagation Framework:

- **Matter** is modeled as a stable, self-reinforcing propagation pattern
- **Energy** is frequency
- **Forces** are path-bending effects of the medium, described refractively
- **Stable structure** exists only where coherence is maintained

This repo asks what follows from those claims mathematically, and what survives contact with real
data.

---

## Current Headline Results

| Result | Status | Confidence |
|--------|--------|------------|
| Forces as refraction for null propagation | DERIVED | 0.95 |
| Three generations of matter | DERIVED | 0.98 |
| Koide geometry: \(Q = 2/3 \iff R/A = \sqrt{2}\) | DERIVED | 0.95 |
| Matter scale from Planck scale | ARGUED | 0.75 |
| Top/tau mass ratio \(\approx \alpha^{-1}/\sqrt{2}\) | EMPIRICAL | 0.90 |

The exact status definitions and falsification pathways are in [CLAIMS.md](./CLAIMS.md).

---

## The God Equation

The framework's strongest open mathematical problem is the derivation of the matter coherence scale
from the Planck scale:

\[
\lambda_c = \sqrt{2} \cdot l_P \cdot \exp\!\left(\frac{4\pi^2 N^{D/2}}{b_0^{SO(3)}}\right).
\]

With \(N=3\), \(D=3\), and \(b_0 = 16/3\):

- **Predicted**: \(1.145 \times 10^{-18}\,\mathrm{m}\)
- **Observed**: \(1.14 \times 10^{-18}\,\mathrm{m}\)
- **Error**: \(0.4\%\)
- **Fitting parameters**: \(0\)
- **Status**: **ARGUED**, not DERIVED

What is closed:

- the kinematic internal phase model
- the exact \(N=3\) generational quotient structure
- the numerical agreement of the final scale

What is still open:

- the bridge from internal phase closure to the required spatial coherence-volume scaling
  \(N^{D/2}\)

See [derivations/lambda_c_from_axioms.md](./derivations/lambda_c_from_axioms.md),
[derivations/g3_coupling_bridge.md](./derivations/g3_coupling_bridge.md), and
[derivations/product_walk_bridge_model.md](./derivations/product_walk_bridge_model.md).

You can run the numerical verification directly:

```bash
python RESEARCH/god_equation_verification.py
```

---

## The Koide Result

The cleanest finished result in the repo is the geometric form of the Koide relation for charged
leptons:

\[
Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2}
= \frac{2}{3}
\iff
\frac{R}{A} = \sqrt{2}
\iff
\theta = 45^\circ.
\]

The geometric equivalence is exact, and the PDG 2024 charged-lepton data verify it to high
precision. The deeper question of why the equal-norm point is selected remains open.

See [derivations/koide_geometric_equivalence.md](./derivations/koide_geometric_equivalence.md).

You can regenerate the triangle directly:

```bash
python visualizations/koide_triangle.py
```

---

## What Failed

This repo keeps failures visible.

- The harmonic-series mass claim failed. See [sandbox_results.md](./sandbox_results.md).
- The corrected \(\phi^3\) electron/up-quark relation is interesting but remains uncertainty-limited
  and a posteriori. See [sandbox/phi3_monte_carlo.md](./sandbox/phi3_monte_carlo.md).

A framework that only publishes successes is not science.

---

## Where To Start

- [EXPLAINER.md](./EXPLAINER.md): plain-English entry point
- [READING_ORDER.md](./READING_ORDER.md): guided path by background level
- [CLAIMS.md](./CLAIMS.md): live confidence matrix
- [CONTRIBUTING.md](./CONTRIBUTING.md): open gaps and how to engage

---

## Repository Map

- [the_propagation_framework.md](./the_propagation_framework.md): canonical axioms and derived quantities
- [theory_of_propagation.md](./theory_of_propagation.md): supporting conceptual framework
- [derivations/](./derivations/): formal derivations and audits
- [sandbox/](./sandbox/): scripts, audits, and numerical experiments
- [visualizations/](./visualizations/): Koide triangle and knowledge graph
- [papers/](./papers/): draft paper material and falsification framing
- [RESEARCH/](./RESEARCH/): literature review passes and research notes

---

## Provenance

This repository was built as a human-AI collaboration. Greg Welby provided the core vision,
problem selection, synthesis, and final judgment. Claude, Lumi, Codex, and Qwen contributed
derivations, audits, counterexamples, literature synthesis, and runnable verification work.

The point of keeping those roles visible is traceability.

---

*This might be wrong. That's the point. The framework that survives contact with data is the one
worth keeping.*
