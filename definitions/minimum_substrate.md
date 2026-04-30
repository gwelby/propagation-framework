# Minimum Substrate
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: Codex assessment `minimum_substrate_assessment_2026-04-28.md`; PF Medium roles; `medium.md`, `mode.md`, `propagation.md`, `causal_velocity.md`*
*Audit: `derivations/minimum_substrate_final_audit_2026-04-29.md`*
*Dependencies: `medium.md` CANONICAL v1.0; `mode.md` CANONICAL v1.0; `propagation.md` CANONICAL v1.0; `causal_velocity.md` CANONICAL v1.0; `coherence.md` CANONICAL v1.0; `gradient.md` CANONICAL v1.0; `observer.md` CANONICAL v1.0; `information.md` CANONICAL v1.0*
*Deferrals: `consciousness.md` (P5 — substrate sufficient for physical observers, not sufficient for consciousness); Lorentz/Poincare emergence (continuum limit — not yet derived)*

---

## The Question

What is the minimum local quantum dynamical structure that can serve as the PF substrate — the Medium — such that all canonical definitions (mode, propagation, gradient, observer, causal velocity) are well-defined on it?

This is not asking what the universe IS made of. It is asking: what mathematical structure is minimally sufficient, as a role-specification, to support PF structure?

---

## The Core Claim

**A single finite-dimensional Hilbert space — qubit, qutrit, or any isolated system with no external locality structure — cannot serve as the PF Medium.**

Every canonical PF definition requires at least two distinguishable spatial regions connected by a finite-speed update relation. A single isolated Hilbert space has no "here" and "there," no causal cone, no propagation path, and no way to define gradient or nonseparable entanglement between separated regions.

The minimum sufficient role-specification is:

> A local quantum dynamical net: local Hilbert spaces over an extended graph/lattice/manifold/causal set, with finite-speed locality-preserving dynamics, stable coherent mode structures, metric/adjacency geometry, and tensor-product quantum nonseparability.

The concrete minimal constructive representative used here is:

> A quantum cellular automaton (QCA) on an infinite or sufficiently large graph with local Hilbert dimension `d ≥ 2` and locality-preserving update rules.

---

## Why a Single Qubit Fails as PF Medium

A qubit (`C²`) is state-bearing and can support internal coherence. It can be in a superposition and evolve unitarily. It is quantized.

It fails every other Medium role:

| Medium Role | Qubit verdict |
|-------------|---------------|
| Causal | FAIL — no event partial order without external clock or update rule |
| State-bearing | PASS |
| Propagative | FAIL — no space to propagate through |
| Dynamic | PARTIAL — only with externally supplied Hamiltonian |
| Coherent | PARTIAL — internal phase coherence exists |
| Geometric | FAIL — no metric, no adjacency, no "here" |
| Quantizing | PASS |
| Quantum-compatible | FAIL as Medium — no separated tensor factors for no-signaling entanglement |

A qubit can be a local site inside a Medium model. It cannot be the Medium itself.

---

## Why a Single Qutrit Fails as PF Medium

A qutrit (`C³`) has richer internal structure — its pure-state symmetry is projective `PU(3) = SU(3)/Z₃`, which is naturally interesting for internal `Z₃` / three-generation hypotheses. This is noted in `mode.md` and remains OPEN.

But internal symmetry is not spacetime geometry. `SU(3)/Z₃` does not supply causal order, propagation paths, gradients, or separated subsystems. A qutrit can be a **site** or **internal fiber** of a Medium model; it cannot be the whole Medium.

The verdict is identical to the qubit:

| Medium Role | Qutrit verdict |
|-------------|---------------|
| Causal | FAIL |
| State-bearing | PASS |
| Propagative | FAIL |
| Dynamic | PARTIAL |
| Coherent | PARTIAL |
| Geometric | FAIL — internal projective geometry is not propagation geometry |
| Quantizing | PASS |
| Quantum-compatible | FAIL as single object; PASS only inside tensor network |

A qutrit may be the **minimum local dimension** for a PF that requires `SU(3)` internal symmetry (three generations, `Z₃` charge structure). This is an OPEN PF interpretation, not a canonical requirement.

---

## The Minimum Sufficient Role-Specification

The PF Medium must satisfy all roles from `medium.md`. A mathematical structure that meets them is a local quantum dynamical net:

**1. Local Hilbert spaces:** The total state space is a tensor product `⊗_i H_i` over sites `i`. Each `H_i` has finite dimension `d ≥ 2`. This provides separated subsystems capable of no-signaling entanglement.

**2. Finite-speed update rule:** The dynamics is a locality-preserving map — a quantum cellular automaton rule, a nearest-neighbor Hamiltonian, or equivalent. Every site update is confined to a finite causal cone. This bounds propagation speed and gives causal velocity a meaning.

**3. Metric/adjacency structure:** The underlying graph/lattice/manifold provides a metric or adjacency relation. This defines what "distance," "gradient," and "nearest neighbor" mean. It enables the mode localization that `mode.md` requires.

**4. Stable coherent modes:** Local interactions and boundary conditions produce eigenvalue spectra and normalizable mode structures. Without stable modes, `mode.md` and `energy.md` are undefined.

**5. Coherence over relevant scales:** The update rule must permit coherence to persist long enough for the relevant experiment — enough for `coherence.md` and `observer.md` to be applicable.

**6. Quantum nonseparability without FTL:** The tensor-product structure allows entangled states between separated regions. The locality-preserving dynamics prevents signaling outside the causal cone.

---

## Local Dimension: `d ≥ 2` Is Locally Sufficient, `d = 3` Is Not Required

The minimum nontrivial local Hilbert dimension is `d ≥ 2` (qubit). A model with local dimension `d ≥ 2` is locally sufficient only when it also satisfies the structural requirements above: extended locality, finite-speed dynamics, metric/adjacency structure, stable modes, coherence over relevant scales, and no-signaling quantum nonseparability.

`d = 3` (qutrit) is **not forced** by the Medium roles alone. It becomes relevant only if the PF makes specific internal symmetry claims (e.g., `SU(3)` structure for three generations). Those are OPEN claims, not canonical requirements.

This distinction matters:

- **Locally sufficient:** `d ≥ 2` is enough local state capacity for a QCA/graph candidate, provided the graph, update rule, metric/adjacency, and stable-mode requirements are also present.
- **Not sufficient alone:** `d ≥ 2` by itself does not satisfy the Medium roles; the structure (locality + update + metric) does the work.
- **Necessary only for nontrivial finite local quantum sites:** `d = 1` is trivial and cannot host local alternatives. More general substrates using local algebras, infinite-dimensional local systems, causal sets, or continuum fields must be audited separately.
- **Not reducible:** A single site of any dimension, with no external graph, cannot satisfy the Medium roles regardless of `d`.

---

## The SuperQubit / Qutrit Debate (PF Context)

The SuperQubit model (embedding `SU(2|1)` or extended superalgebra structure) and the qutrit-first approach (`d = 3` for `Z₃` internal symmetry) are legitimate **model-building choices**, not derived PF requirements.

The canonical definition does not determine:
- Whether the local fiber is a qubit or qutrit.
- Whether the internal symmetry group is `SU(2)`, `SU(3)`, or something larger.
- Whether there are additional hidden dimensions or internal moduli.

These are **model selection questions** downstream of the canonical substrate definition. The canonical definition only states: extended locality, finite-speed update, metric structure, tensor-product quantum mechanics.

---

## What the Minimum Substrate Is NOT

- Not a description of what the universe is actually made of. The file answers: what class of mathematical structure is minimally sufficient to support PF definitions? Whether the physical universe employs a QCA, a causal set, a spin network, or a continuum field theory on top of this is a separate empirical question.
- Not a single qubit or qutrit. A single finite-dimensional Hilbert space — regardless of dimension — cannot supply causal structure, propagation paths, or separated observer stations. Local fibers can be qubits or qutrits; the complete substrate requires the extended graph/network structure.
- Not a claim that the PF derivations are complete. The canonical substrate defines the minimum structural requirements; it does not derive the specific QCA dynamics, the specific local fiber dimension, or the specific continuum limit that reproduces the Standard Model.
- Not a constraint on local fiber internal symmetry. The canonical definition only specifies nontrivial local state capacity plus extended locality. Whether the fiber is `SU(2)`, `SU(3)`, or `SU(2|1)` is a downstream model choice, not a canonical requirement.
- Not a resolution of the hierarchy problem, the cosmological constant problem, or quantum gravity. Those open questions in physics apply to any candidate substrate description; the canonical definition is silent on them.

---

## Measurement Discipline

Every minimum-substrate claim must specify:

1. **Which Medium roles are tested:** the core claim is that all eight roles from `medium.md` are satisfied. Claims about partial role satisfaction must name which roles are in scope.
2. **Local fiber dimension:** is the claim about a specific `d` (qubit: `d = 2`, qutrit: `d = 3`) or the class `d ≥ 2`? Distinguish local nontriviality from whole-substrate sufficiency.
3. **Graph/lattice topology:** finite, infinite, periodic, aperiodic? Causal set, regular lattice, random graph? The topology affects which mode structures are stable and which propagation paths exist.
4. **Update rule class:** is the dynamics a unitary QCA, a Lindbladian open-system QCA, a nearest-neighbor Hamiltonian, or a causal-set dynamics? Each has different coherence and decoherence properties.
5. **Scale:** at what spatial and temporal scale is the substrate description valid? Does the claim apply at Planck scale, at Standard Model scale, or only in the continuum limit?
6. **Standard physics vs. PF interpretation:** the local quantum net structure is consistent with algebraic quantum field theory (Haag-Kastler locality) and with known QCA constructions (Dirac/Weyl QCA); the claim that this is the PF Medium is a PF interpretation, not a derived result from existing physics.
7. **Sufficient vs. necessary:** the canonical definition establishes sufficient role-criteria and a minimal constructive representative. Claims about uniqueness or necessity require additional arguments (e.g., proving no simpler structure supports the Medium roles).

---

## Falsification Conditions

A minimum-substrate claim fails if:

1. **A single isolated system with no external locality structure satisfies all canonical PF definitions:** Construct a single `d`-dimensional Hilbert space — no graph, no update rule, no metric — that supports `mode.md` localized modes, `propagation.md` causal-front propagation, `gradient.md` spatial variation, and `observer.md` separated Type 2/3 observers. If this succeeds, the "extended locality required" claim fails.
2. **The substrate predicts signals that exceed `c`:** The update rule must bound all controllable propagation at or below causal velocity. If superluminal signaling is possible within the substrate dynamics, the causal velocity definition is violated.
3. **The substrate cannot support entangled separated observers:** If Type 2/3 observers at spacelike separation cannot be in nonseparable states without FTL signaling, the quantum compatibility requirement fails.
4. **The PF-required substrate cannot recover Lorentz symmetry in the continuum limit:** The substrate is discrete (QCA/graph) by default. If no locality-preserving QCA construction with the PF's required Medium properties can recover Lorentz invariance (exact or emergent) in the continuum/large-scale limit, then the substrate cannot represent a relativistic universe. Note: existing Dirac/Weyl QCA constructions do recover Lorentz invariance in the continuum limit for specific update rules; this falsifier applies to whether such a construction satisfies all PF Medium roles simultaneously. This is OPEN — no combined derivation yet.
5. **The local state capacity claim fails:** The claim that nontrivial local quantum sites with `d ≥ 2` can serve as local fibers is falsified if every substrate satisfying the PF roles requires larger local dimension or additional local algebraic structure. The file does not claim `d ≥ 2` alone is sufficient without the graph/update/metric structure.

---

## Open Questions

| Question | Status |
|----------|--------|
| Is `d = 3` (qutrit) required for three-generation SM structure? | OPEN — consistent with some PF interpretations; not canonical |
| Does the minimum substrate require `SU(3)` internal symmetry? | OPEN — mode.md notes the `Z₃` connection; not a canonical claim |
| Can a QCA satisfying all PF Medium roles recover Lorentz/Poincaré symmetry in the continuum limit? | OPEN — no combined derivation yet; individual Dirac/Weyl QCAs recover Lorentz invariance but have not been audited for all Medium roles |
| Is a generic QCA enough, or does the PF require a specific QCA (e.g., Dirac-type, Hadron-type)? | OPEN — specific models not yet canonical |
| Are there lower-dimensional topological substrates (e.g., spin networks, causal sets) that satisfy all Medium roles with less structure? | OPEN — topological approaches are candidates but have not been audited |

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `medium.md` | The substrate is a candidate mathematical instantiation of the Medium roles: local state space, finite-speed causal evolution, coherent modes, gradients/geometry, quantization, and quantum compatibility |
| `mode.md` | Mode localization requires the graph/lattice metric structure of the substrate; modes are defined on local Hilbert spaces |
| `propagation.md` | Propagation requires the finite-speed update rule and graph adjacency of the substrate |
| `causal_velocity.md` | Causal velocity is the speed of the update rule's causal cone on the substrate |
| `coherence.md` | Coherence over relevant spatial and temporal scales requires the substrate's update and interaction structure |
| `observer.md` | Type 2/3 observers with separated records require the substrate's tensor-product structure for no-signaling entanglement |
| `information.md` | Information distinguishability requires the substrate's local state spaces and measurement basis structure |
