# Gradient
*Fundamentals canonical definition*
*Status: CANONICAL v1.0 - passed Codex final audit 2026-04-29*
*Source: `the_propagation_framework.md` Force mechanism; `medium.md`*
*Audit: `derivations/gradient_definition_final_audit_2026-04-29.md`*
*Dependencies: `medium.md`, `forces.md`, `propagation.md`, `coherence.md`, `mode.md`, `causal_velocity.md` CANONICAL v1.0*

---

## The Definition

**A gradient is the derivative of a field with respect to position or another specified coordinate, identifying how the field changes across that domain.**

For a scalar field on flat space, the spatial gradient is the vector pointing toward the direction of greatest increase, with magnitude equal to the rate of that increase. In one dimension: `∇f = df/dx`. In three dimensions: `∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)`. The gradient is defined at every point where the scalar field is differentiable.

The plain gradient `∇f` applies to scalar fields on flat spaces. Extensions to curved manifolds (covariant derivative `∇_μ`) and gauge fields (gauge-covariant derivative `D_μ`) are related but structurally different; see the Three Usages section below.

Plain language:

> A gradient is a slope. A gradient field tells you which direction is uphill and how steep it is at each point.

---

## Three Distinct Usages in the Canonical Stack

The word "gradient" appears in three different contexts in the PF canonical definitions. These must be distinguished.

### 1. Mathematical Gradient (∇)

This is the pure calculus operator. It is defined independently of physics:

- `∇f` — gradient of a scalar field `f` (the primary sense in this file)

Related `∇` operations are often discussed together, but they are not gradients:

- `∇·A` — divergence of a vector field `A` (note: `A` here is a vector; distinct from any potential)
- `∇×A` — curl of a vector field `A`

Two distinct extensions apply in different physical contexts:

- **Covariant derivative `∇_μ`** (Riemannian geometry): extends differentiation to curved manifolds using a connection. In GR this is usually the Levi-Civita connection, whose coordinate coefficients are the Christoffel symbols. It is used to define parallel transport, geodesics, and curvature. This is *not* the same as the gauge-covariant derivative.
- **Gauge-covariant derivative `D_μ`** (gauge theory): extends the flat-space partial derivative `∂_μ` to gauge fields, schematically `D_μ = ∂_μ − igA_μ` in natural units. It describes how matter fields transform under an internal gauge symmetry. This is *not* the same as the Levi-Civita covariant derivative.

Both `∇_μ` and `D_μ` are "extensions of gradient" in the sense that they generalize differentiation to richer geometric structures, but they are structurally different and should not be conflated.

This definition is not a PF interpretation. It is the mathematical foundation on which the other two usages are built.

### 2. Physical Gradient — Force as Gradient

In standard physics, several force descriptions use gradient language:

**Conservative forces:** `F_vec = −∇φ` where `φ` is a scalar potential. The force vector points in the direction of decreasing potential energy. (Using `φ` for potential and `F_vec` for force to avoid collision with the field strength tensor `F_{μν}` used below.)

**Gravity in Newtonian limit:** `F_vec = −mg∇Φ` where `Φ` is the gravitational potential.

**Gravity in GR (not a force in the traditional sense):** The Christoffel symbols `Γ^μ_{νρ}` are coordinate coefficients of the Levi-Civita connection derived from the metric `g_{μν}`. They describe how basis vectors change along curves. Massive particles follow timelike geodesics — this is free fall in curved spacetime, not a force in the `F = ma` sense. What is often called "gravitational acceleration" is coordinate acceleration or geodesic deviation arising from spacetime curvature. The PF interpretation frames this as structure in the Medium's causal geometry, not as a simple scalar gradient.

**Gauge forces:** The gauge-covariant derivative `D_μ = ∂_μ − igA_μ` (schematically for U(1)/natural units) extends differentiation to fields with internal gauge symmetry. The field strength `F_{μν}` is obtained from the commutator of covariant derivatives and measures gauge curvature. In non-Abelian theories it includes self-interaction terms, not just ordinary derivatives. This is gradient-like language applied to gauge structure, not a plain `∇f`.

### 3. PF Interpretation — Forces as Medium-Property Gradients

`forces.md` states: *"The Propagation Framework interprets these structures as gradients or properties of the Medium."*

This is a PF interpretation, labeled as such in the canonical forces definition. It is not the canonical definition of force — it is a reframing program. The interpretation is:

- Gravity: PF interpretation of spacetime curvature/connection as nonuniform Medium causal structure
- EM: PF interpretation of the U(1) gauge potential/field strength as Medium gauge structure
- Strong: PF analogy connecting SU(3) color-field confinement to an effective Medium structure; formal mapping remains OPEN
- Weak: PF interpretation of electroweak interactions as mode-conversion structure; derivation of V-A, CKM, and CP violation remains OPEN

The PF does not yet have canonical derivations of all four force types from a single Medium-gradient property. This remains the research program.

---

## Gradient and the Medium

`medium.md` says the Medium provides "gradients that alter propagation paths." This means the Medium's structural properties can vary spatially — those spatial variations are gradients in the Medium's structure.

Propagation through a Medium with structural variation:
- A mode's trajectory, momentum, phase, or internal quantum numbers can change in response to the relevant structure
- The mode does not need to experience a "force" in the Newtonian sense — in gravity it follows the causal structure the metric provides
- For gravity: a mode follows a null or timelike geodesic of the metric (not `F_vec = −∇φ`, except in a Newtonian limit)
- For gauge fields: a mode responds to gauge-covariant structure via minimal coupling

This is the connection between gradient and propagation: variation in the Medium's structure can bend propagation paths or change internal states. For gravity, the mode follows the straightest available path in the metric geometry; for gauge fields, the response is through gauge coupling rather than spacetime straightness.

---

## What Gradient Is NOT

- Not a force itself. A gradient produces a force vector in the `F_vec = −∇φ` sense for conservative potentials. In GR, spacetime curvature produces geodesic deviation without a Newtonian-style force. The distinction matters.
- Not only spatial in generalized usage. The plain `∇` gradient is spatial, while `∂_μ`, `∇_μ`, and `D_μ` are spacetime/geometric generalizations. The domain must be specified.
- Not the same as slope in informal language. The mathematical gradient is a vector field; informal "gradient" may mean only the magnitude, not the direction.
- Not the Christoffel symbol alone. `Γ^μ_{νρ}` are coordinate coefficients of the Levi-Civita connection — they describe how basis vectors change, not a simple `∇f`. Calling this structure a gradient is a PF specialization; the standard physics term is connection.
- Not a guarantee of a force. A gradient in a field does not always produce a force — it depends on what the field is coupled to. A temperature gradient produces heat flow only if there is a coupling to the thermal degrees of freedom.

---

## Measurement Discipline

Every gradient claim must specify:

1. **Gradient type:** plain gradient `∇f` (scalar field, flat space), covariant derivative `∇_μ` (curved manifold/GR), gauge-covariant derivative `D_μ` (gauge field), or PF Medium-structure gradient. Do not conflate these.
2. **Tensor rank/order of the gradient object:** `∇f` produces a rank-1 tensor (vector); `∇_μ A_ν` produces a rank-2 tensor; Christoffel symbols `Γ^μ_{νρ}` are rank-3 connection coefficients, not a gradient of a scalar.
3. **Whether the claim is mathematical, standard physics, or PF interpretation:** `∇f` is mathematical; `F_vec = −∇φ` and Christoffel symbols are standard physics; "forces as Medium-property gradients" is PF interpretation.
4. **Coupling:** the gradient must be coupled to a mode or excitation to produce an observable effect. A gradient in an uncoupled field has no physical effect on that mode.
5. **Regime:** Newtonian (`∇φ`), GR (geodesic deviation via `Γ^μ_{νρ}`), gauge theory (`D_μ`), or PF Medium-structure gradient.
6. **Domain:** static or dynamic field; linear or nonlinear regime; perturbative or non-perturbative; differentiable or distribution-valued.
7. **Spatial vs. spacetime:** plain `∇` is a 3-vector operator; `∂_μ`, `∇_μ`, and `D_μ` are 4-vector operators. A gradient claim must state which.

---

## Gradient and Coherence

A gradient field can change a mode's phase relations during propagation, affecting coherence:

- **Phase gradients from spatial variation:** a spatially varying scalar/effective potential or gauge connection can change a mode's momentum and phase through the appropriate coupling. For gauge fields, the physical effect is expressed through gauge-covariant derivatives and field strengths, not through a gauge-dependent potential alone. If the gradient is spatially uniform over the mode's extent, the phase shift is uniform. If the gradient varies within the mode (e.g., near a sharp potential edge), the phase shift can be non-uniform, degrading spatial coherence.
- **Dephasing from inhomogeneous gradients:** an inhomogeneous gradient across a mode's wavefunction produces position-dependent momentum shifts, causing phase dispersion or wavepacket spreading. This can reduce a specified coherence metric, but it is not automatically environmental decoherence unless an environment or unobserved degrees of freedom are involved.
- **Coherence-preserving propagation through uniform gradients:** a mode propagating through a spatially uniform gradient field undergoes uniform acceleration and phase evolution — coherence is preserved. This is the basis of uniform field physics (uniform electric fields, uniform gravitational fields in the Newtonian limit).

This is a standard physics result (phase evolution in uniform fields) restated in PF coherence language. It is not a PF-specific derivation.

---

## Open Questions

| Question | Status |
|----------|--------|
| Does PF derive all four forces from a single class of Medium-structure gradients? | OPEN — research program; no canonical derivation yet |
| Is the Levi-Civita connection, represented in coordinates by `Γ^μ_{νρ}`, the correct PF proxy for "gradient" in spacetime curvature? | OPEN — PF framing treats connection structure this way; formal mapping not canonical |
| Does PF classify gauge field strength `F_{μν}` as a gradient of the Medium's gauge structure? | OPEN — consistent with the interpretation; not yet canonical |
| Can the PF derive a single unified gradient concept that subsumes `∇_μ` and `D_μ`? | OPEN — the mathematical structures are different; any unification requires additional structure |

---

## Falsification Conditions

A gradient definition fails if:

1. **The gradient operator is undefined** in the relevant domain (non-differentiable field at a point where the gradient is claimed): the definition would need domain restriction.
2. **A claimed physical gradient produces no observable effect** on any test mode in the stated regime: if `∇φ` produces no force vector where `F_vec = −∇φ` is claimed, the physical gradient account fails.
3. **PF Medium-gradient interpretation is inconsistent** with established gauge coupling or geodesic deviation in any tested regime: would require revision of the PF gradient-as-Medium-property program.
4. **A PF derivation conflates `∇_μ` and `D_μ` without an explicit unifying structure:** this would invalidate the claimed unification, not the standard mathematical definitions. Any true unification would need to show the additional geometric structure that makes the relationship precise.

---

## Relationship to Other Definitions

| Definition | Connection |
|------------|-----------|
| `forces.md` | Standard physics encodes forces as spacetime geometry or gauge field structure; PF interprets these as Medium structural gradients where a force-specific mapping exists |
| `medium.md` | The Medium provides structural variation that can alter propagation paths; this is the role gradient language formalizes |
| `causal_velocity.md` | Gradients in effective coordinate propagation conditions do not change local causal velocity; causal velocity still bounds controllable influence |
| `mode.md` | Modes respond to gradients by deviating from their initial trajectory or changing their internal state; the response depends on the mode's coupling |
| `coherence.md` | Coherent mode propagation through a gradient field maintains phase structure; inhomogeneous gradients can degrade coherence; uniform gradients preserve it |
| `propagation.md` | Propagation through a Medium with gradients changes the propagating entity's path or state |
