# Field
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 — passed Codex final audit 2026-04-30*
*Source: load-bearing term audit across canonical definitions; `mode.md`; `matter.md`; `forces.md`; `gradient.md`; `medium.md`*
*Audit: `derivations/field_definition_final_audit_2026-04-30.md`*
*Dependencies: `medium.md` CANONICAL v1.0; `state.md` CANONICAL v1.0; `mode.md` CANONICAL v1.0; `coherence.md` CANONICAL v1.0; `energy.md` CANONICAL v1.0; `forces.md` CANONICAL v1.0; `gradient.md` CANONICAL v1.0; `minimum_substrate.md` CANONICAL v1.0*
*Related definitions: `coupling.md` CANONICAL v1.0*

---

## Definition

**A field is an assignment of physical degrees of freedom to points, regions, or sites of a domain, together with rules for how those degrees of freedom transform, evolve, and couple.**

In standard physics, a field may be a scalar, vector, spinor, tensor, gauge connection, or quantum field operator. In PF terms, a field is a way to represent state-bearing structure of the Medium: the local variables whose admissible patterns are modes, whose gradients can affect propagation, and whose excitations can appear as particles.

Plain language:

> A field is a distributed physical variable. A mode is a self-consistent pattern of that variable.

---

## Standard Field Types

| Field type | Mathematical form | Example | Notes |
|------------|-------------------|---------|-------|
| Scalar field | value at each point/site | Higgs field, temperature field | One number or scalar degree of freedom per location |
| Vector/tensor field | vector or tensor at each point/site | electromagnetic field, metric tensor | Carries directional or geometric structure |
| Spinor field | spinor-valued field | electron/Dirac field | Requires spin structure; matter fields are spinor fields in the Standard Model |
| Gauge field | connection on an internal bundle | `A_μ`, gluon field | The potential is gauge-dependent; physical claims require gauge-invariant observables or properly gauge-covariant structures |
| Quantum field | operator-valued distribution or local observable algebra | QED electron/photon fields | Excitations are particles or quasiparticles |
| Effective field | coarse-grained field variable | phonon field, order parameter | Valid only in a stated scale/regime |

The word "field" is therefore not a single mathematical object. Every field claim must specify the field type, domain, transformation law, and regime.

---

## Field, Medium, State, and Mode

The PF uses these terms in a strict hierarchy:

| Term | Role |
|------|------|
| Medium | The rule-structure that permits propagation, coherence, curvature, and stable modes |
| Field | A state-bearing degree of freedom distributed over the Medium or substrate |
| State | A configuration of the relevant degrees of freedom of a system |
| Mode | An admissible pattern of a field or Medium state under an evolution law |

The Medium is not just one field. It may support many fields and may also include the causal, metric, topological, or update-rule structure that lets fields exist and propagate. A field is the variable; a state is a configuration of that variable; a mode is a special stable or admissible configuration.

---

## Classical, Quantum, and Discrete Fields

### Classical field

A classical field assigns ordinary values to a domain:

```text
φ: spacetime region → value space
```

Examples include a scalar potential, fluid velocity field, or classical electromagnetic field. Classical field descriptions are often effective limits of underlying quantum or statistical systems.

### Quantum field

A quantum field is not a classical wave spread through space. In QFT it is represented by operator-valued distributions or by algebras of local observables. In regimes where a particle interpretation applies, particle states are excitations of the field above the vacuum state.

For a field operator `φ(x)`, one-particle states are created schematically by creation operators acting on the vacuum:

```text
|particle⟩ = a†(k)|0⟩
```

This is the sense used by `matter.md`: matter particles are excitations of matter fields.

### Discrete substrate field

In `minimum_substrate.md`, the minimal constructive representative is a local quantum dynamical net or QCA. In such a model, "field" need not mean a continuum function. It can mean a local degree of freedom assigned to graph sites or links, with continuum field behavior emerging only in a long-wavelength limit.

---

## Gauge Fields

Gauge fields require special care. A gauge potential such as `A_μ` is not itself uniquely observable because it changes under gauge transformations. Physical content is expressed through gauge-invariant observables or gauge-covariant structures such as:

- field strength `F_{μν}` in electromagnetism,
- gauge-invariant contractions or Wilson loops/holonomies,
- covariant derivatives `D_μ` as the coupling structure for matter fields,
- scattering amplitudes and conserved currents.

For non-Abelian gauge theory, the field strength is gauge-covariant, not automatically gauge-invariant as a standalone component. Observable claims must specify the invariant or operational quantity being measured.

PF may interpret gauge fields as Medium gauge structure, but that is a labeled interpretation, not a derivation of the Standard Model gauge group. `forces.md` remains controlling for force-specific claims.

---

## What a Field Is NOT

- **Not the Medium itself.** A field is a state-bearing structure within or over the Medium. The Medium also includes causal, metric, topological, and update-rule structure.
- **Not automatically a particle.** Particles are excitations or modes of fields, not fields themselves.
- **Not automatically observable.** Gauge potentials and field coordinates can be representation-dependent. Observable claims must use gauge-invariant or operationally defined quantities.
- **Not necessarily continuous.** Continuum fields are one representation; lattice/QCA/site fields are allowed in substrate models.
- **Not always fundamental.** Many fields are effective or coarse-grained, valid only at specified scales.
- **Not synonymous with force.** Forces describe how modes change under metric/gauge/interaction structure; fields are the structures or variables being coupled.

---

## Measurement Discipline

Every field claim must specify:

1. **Field type:** scalar, vector, tensor, spinor, gauge, quantum, effective, or discrete-site field.
2. **Domain:** continuum spacetime, curved manifold, graph/lattice/QCA, material medium, or abstract state space.
3. **Representation:** classical value, effective wavefunction/wave amplitude, density operator, operator-valued distribution, local observable algebra, connection, or effective order parameter.
4. **Transformation law:** Lorentz/Poincare, gauge group, internal symmetry, coordinate covariance, or lattice symmetry.
5. **Dynamics:** Lagrangian, Hamiltonian, field equation, update rule, or effective equation of motion.
6. **Observable status:** whether the field variable itself is observable or only gauge-invariant/correlation-derived quantities are observable.
7. **Regime and scale:** fundamental, effective, continuum limit, perturbative, nonperturbative, thermal, condensed matter, or PF interpretation.

---

## Open Questions

| Question | Status |
|----------|--------|
| Does PF derive the observed Standard Model field content? | OPEN — central unsolved derivation problem |
| Is the Medium more fundamental than fields, or exactly expressible as a complete field algebra? | OPEN — current definitions use the Medium as rule-structure, not a single field |
| Can continuum fields be derived from a QCA/local-net substrate in a Lorentz-compatible limit? | OPEN — individual Dirac/Weyl QCA results exist; full PF substrate derivation remains open |
| Are gauge fields literally Medium structure or an effective description of deeper Medium dynamics? | OPEN — PF interpretation, not canonical derivation |

---

## Falsification Conditions

A field definition fails if:

1. **The field has no specified domain or degrees of freedom:** a "field" with no assignment over points, regions, sites, or algebraic localization is not a field under this definition.
2. **A gauge-dependent field coordinate is treated as directly observable without gauge fixing or an invariant quantity:** this would contradict standard gauge theory.
3. **A claimed field excitation cannot support the mode behavior assigned to it:** if the stated dynamics does not admit the claimed modes, the field-mode account fails in that regime.
4. **A PF field claim requires superluminal controllable influence:** changes in local observables and controllable signals must obey `causal_velocity.md`; gauge-coordinate artifacts do not count as signals.
5. **A continuum field is claimed fundamental where only an effective long-wavelength limit has been shown:** the claim must be demoted to effective-field status.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `medium.md` | Fields are state-bearing structures of or within the Medium; the Medium is not reducible to one field in this definition |
| `state.md` | A field state is a configuration of field degrees of freedom |
| `mode.md` | A mode is an admissible pattern of a field or Medium state |
| `coupling.md` | Coupling specifies how field degrees of freedom influence each other's evolution |
| `matter.md` | Matter particles are stable or quasi-stable excitations of matter fields |
| `forces.md` | Force effects are encoded through metric structure, gauge fields, and interaction terms |
| `gradient.md` | A gradient is the derivative or covariant variation of a field with respect to a specified coordinate/domain |
| `energy.md` | Field configurations have Hamiltonian/Noether energy when the relevant symmetry and dynamics are specified |
| `coherence.md` | Field modes are stable only when their relevant relational structure remains coherent under evolution |
| `minimum_substrate.md` | A discrete substrate may realize fields as local degrees of freedom on graph/lattice/QCA sites or links |
