# Minimum Substrate Assessment
*Fundamentals - /mnt/d/Fundamentals/derivations/minimum_substrate_assessment_2026-04-28.md*
*Auditor: Codex*
*Date: 2026-04-28*

---

## Question

What is the smallest mathematical object that satisfies the Medium roles?

Roles checked:

1. Causal
2. State-bearing
3. Propagative
4. Dynamic
5. Coherent
6. Geometric
7. Quantizing
8. Quantum-compatible: supports nonseparable states without FTL signaling

---

## Verdict

The minimum object is **not a single qubit** and **not a single qutrit**.

The minimum object is:

> An extended local quantum dynamical system: a tensor-product/net of local Hilbert spaces over a graph, lattice, manifold, or causal set, equipped with locality-preserving dynamics and a metric/adjacency structure.

The smallest concrete candidate in the given list is:

> A quantum cellular automaton (QCA) on an infinite or sufficiently large graph/lattice with local Hilbert dimension `d >= 2`, locality-preserving update rules, and allowed spatial variation in couplings or graph structure.

If the model needs built-in `SU(3)` / `Z3` internal structure, use qutrit sites (`d = 3`). But `d = 3` is **not forced** by the Medium roles alone.

---

## Candidate Matrix

| Candidate | Verdict | Passes | Fails |
|-----------|---------|--------|-------|
| Single qubit (`C^2`) | **FAILS** | State-bearing, quantizing; can have internal phase coherence if dynamics added | No intrinsic causality, propagation, geometry, gradients, separated entanglement/no-signaling structure, or modes in space |
| Single qutrit (`C^3`) | **PARTIAL / FAILS AS MEDIUM** | State-bearing, quantizing, richer internal symmetry (`SU(3)`, projective center `Z3`), internal coherence | Same critical failures as qubit: no locality, no causal cone, no propagation through extension, no gradients, no nonseparable separated subsystems |
| Infinite-dimensional Hilbert space with local structure | **SATISFIES ALL if locality/dynamics are included** | Can support state space, local algebras, propagation, coherent modes, spectra, entanglement, geometry | Generic Hilbert space alone is insufficient; "local structure" and dynamics do the work |
| Quantum cellular automaton | **SATISFIES ALL as minimum constructive model** | Local state, causal update cone, propagation, coherent/dynamical patterns, graph geometry, discrete spectra, entanglement over tensor factors | Exact Lorentz/Poincare symmetry is not automatic; must be emergent or imposed in continuum/large-scale limit |

---

## Detailed Checks

### 1. Single Qubit (`C^2`)

**Verdict: FAILS.**

A qubit has a two-dimensional Hilbert space. It can be in superposition and can evolve under a Hamiltonian. It is quantized and state-bearing.

It fails as a Medium because it has no intrinsic extension. Without at least two localized subsystems and a relation between them, there is no "here" and "there", no causal cone, no propagation path, no gradient, and no no-signaling entanglement structure.

Role check:

| Role | Result |
|------|--------|
| Causal | FAIL - no event partial order by itself |
| State-bearing | PASS |
| Propagative | FAIL - no extension to propagate across |
| Dynamic | PARTIAL - only if Hamiltonian specified |
| Coherent | PARTIAL - phase coherence can exist internally |
| Geometric | FAIL |
| Quantizing | PASS |
| Quantum-compatible | FAIL as Medium - no separated tensor factors |

### 2. Qutrit (`C^3`)

**Verdict: PARTIAL / FAILS AS MEDIUM.**

A qutrit adds richer internal structure. Its pure-state symmetry is projective `PU(3) = SU(3)/Z3`, so it is naturally interesting for internal `Z3` / generation-style hypotheses.

But internal symmetry is not spacetime geometry. `SU(3)/Z3` does not supply causal order, propagation, gradients, or separated subsystems. A qutrit can be a **site** or **internal fiber** of a Medium model; it cannot be the whole Medium.

Role check:

| Role | Result |
|------|--------|
| Causal | FAIL |
| State-bearing | PASS |
| Propagative | FAIL |
| Dynamic | PARTIAL - only if Hamiltonian/update specified |
| Coherent | PARTIAL |
| Geometric | FAIL - internal projective geometry is not propagation geometry |
| Quantizing | PASS |
| Quantum-compatible | FAIL as single object; PASS only inside tensor network |

**Answer to the qutrit question:** `SU(3)/Z3` may satisfy an internal symmetry requirement, but it does **not** satisfy Geometric or Causal roles without an external locality structure.

### 3. Infinite-Dimensional Hilbert Space with Local Structure

**Verdict: SATISFIES ALL if the phrase "with local structure" is doing real work.**

A generic infinite-dimensional Hilbert space is still not enough. The key additions are:

- a factorization or net of local algebras,
- a topology/metric/adjacency relation,
- local dynamics,
- a finite propagation bound,
- observables that define modes and spectra.

With those, this candidate can satisfy every Medium role.

Role check:

| Role | Result |
|------|--------|
| Causal | PASS if local dynamics has finite propagation speed |
| State-bearing | PASS |
| Propagative | PASS if excitations/local observables can move |
| Dynamic | PASS if Hamiltonian/unitary/evolution law specified |
| Coherent | PASS if stable correlations/modes exist |
| Geometric | PASS if locality is metric/geometric, not just abstract |
| Quantizing | PASS via operator spectra/boundary conditions |
| Quantum-compatible | PASS via tensor products/local algebras/nonseparable states |

### 4. Quantum Cellular Automaton

**Verdict: SATISFIES ALL as the minimum constructive model.**

A QCA supplies exactly what a single qubit/qutrit lacks:

- many local degrees of freedom,
- tensor-product structure,
- finite-speed update rule,
- causal cone,
- propagating disturbances,
- graph/lattice geometry,
- quantized local states,
- entanglement without signaling beyond the update cone.

Role check:

| Role | Result |
|------|--------|
| Causal | PASS - update rule defines finite causal cone |
| State-bearing | PASS - tensor product of local Hilbert spaces |
| Propagative | PASS - local disturbances can spread |
| Dynamic | PASS - update rule is dynamics |
| Coherent | PASS if stable/eigenmode patterns exist |
| Geometric | PASS - graph/lattice metric; gradients via variable couplings/topology |
| Quantizing | PASS - finite-dimensional local states / spectral structure |
| Quantum-compatible | PASS - entanglement across local sites; no-signaling outside causal cone |

Main limitation: exact Lorentz symmetry is not automatic. A QCA can be a minimum substrate model, but a physical-universe model must show Lorentz/Poincare symmetry in the continuum or large-scale limit, or explain observed Lorentz invariance another way.

---

## Minimum Symmetry Requirement

The minimum substrate's symmetry group is not simply `SU(3)` or `Z3`.

For the eight Medium roles, the substrate must contain at least:

1. **Locality-preserving automorphisms** of the underlying graph/net.
2. **A time-update symmetry or semigroup** generated by the dynamics.
3. **Internal unitary symmetry** on local degrees of freedom, at least `U(d)` before constraints.
4. **A metric/adjacency-preserving subgroup** that defines geometry.

For a physically realistic vacuum, additional symmetry must emerge or be imposed:

- Lorentz/Poincare symmetry at macroscopic/continuum scales.
- Gauge symmetries for observed interactions.
- If three-generation structure is targeted, an internal `Z3` or related cyclic structure may be needed, but this is downstream, not required by Medium roles alone.

---

## Target Answer

The minimum mathematical object satisfying all eight Medium roles is:

> A local quantum dynamical net: local Hilbert spaces over an extended locality graph, with finite-speed locality-preserving dynamics, stable coherent modes, metric/gradient structure, and tensor-product quantum nonseparability.

The minimum constructive representative is:

> A quantum cellular automaton on an infinite graph/lattice.

Its symmetry group is:

> The locality-preserving automorphism group of the graph/lattice, combined with local internal unitary symmetry `U(d)` and the dynamical update group/semigroup. For our universe, Lorentz/Poincare and gauge symmetries must appear as exact or emergent constraints.

---

## PREDICTED Claim for `minimum_substrate.md`

**Claim:** No finite-dimensional single-system Hilbert space can satisfy all Medium roles. Any viable PF substrate must contain nontrivial locality: at minimum, multiple local state spaces plus a finite-speed local update relation.

**Falsifier:** Construct a single finite-dimensional system, with no external graph/manifold/tensor-factor locality added, that defines a causal cone, supports propagation across distinguishable locations, admits gradients that bend propagation, and supports no-signaling nonseparable states between separated regions.

If such a construction exists, the "extended local quantum system required" claim fails.

If no such construction exists, qutrit-only and SuperQubit-only Medium proposals remain insufficient as complete substrates, though they may still be useful local/internal degrees of freedom.
