# T2 — Denominator Theorem: M = 3 from PF Axioms (Co-Dimension Route)

**File ID**: T2-DENOM-001
**Claim**: Candidate co-dimension route for the denominator `M` in `Q(N) = 2N / (2N + M)`: relate `M = 3` to the co-dimension of a propagation-medium Fermi point in 3D momentum space.
**Status**: AUDITED DRAFT — no sign-off on T2 closure; the surviving result is a conditional 2×2 Fermi-point lemma, while T2 remains `PARTIAL DERIVATION 0.85`
**Depends on**: T1 (the `(2,1)` topological weight partition), PF Axiom 3 (Coherence), and the PF premise that physical space has dimension `d = 3`.
**Author**: Claude (draft, 2026-03-31)
**Auditor**: Codex (`t2_denominator_theorem_audit_2026-03-31.md`)
**Prior audit that defines this gap**: `three_generations_t2_audit_2026-03-28.md` (HA-20260328-008)
**Follow-up bridge note**: `t2_coherence_tensor_bridge.md` (2026-04-01) replaces the scalar order-parameter ansatz with a conditional three-component coherence tensor, but does not change T2 status
**v2 companion files (2026-03-31)**:
- `t2_order_parameter_derivation.md` — promotes PF coherence field from ansatz to ARGUED derivation from Axioms 1-3
- `t2_fermi_point_bridge.md` — derives `2×2` Hamiltonian from T1+Axiom 2 (Bridge 2) and argues restoration-mode identification (Bridge 3)

---

## 0. What This File Is For

The Codex audit of 2026-03-28 identified one clean gap in the T2 argument:

> The second arrow in `co-dim(point defect) = 3 → three independent massive modes = M` is not proved.

This file attempts to close that gap using the co-dimension route (Option A of the audit's required closure).

It does **not** invoke the electroweak triplet `(W+, W-, Z)` by name.
It does **not** assume a gauge symmetry group.
It does **not** smuggle the Standard Model answer through Goldstone-Higgs language without explicitly defining a PF order parameter.

---

## 1. Inputs and Allowed Premises

**Allowed**:
- PF Axiom 1: propagation is fundamental; physical space is the medium carrying modes
- PF Axiom 2: finite causal velocity; relativistic dispersion relations hold
- PF Axiom 3: coherent modes survive; incoherent modes disperse
- T1 result: stable propagation modes in the medium carry topological weight partition `(2, 1)` — two-component spinorial structure for fermions, one-component for bosons
- Empirical premise: physical momentum space is 3-dimensional (`ℝ³`)
- Standard linear algebra over `ℝ` and `ℂ`

**Not allowed**:
- The observed electroweak triplet as a counting input
- Gauge group assumptions not derived from PF
- Goldstone counting without explicit PF order parameter and symmetry-breaking derivation
- Volovik's ³He result as the proof itself (it is used as a structural template only)

---

## 2. The PF Order Parameter

*This section previously defined the coherence field as a bare ansatz. The ansatz has been promoted to an argued derivation in a companion file.*

**See**: `t2_order_parameter_derivation.md` for the full argument from Axioms 1-3.

**Summary** (for self-containedness of this file):

From Axiom 1 (propagation requires a state-carrying medium), Axiom 2 (wave solutions require complex phase structure), and Axiom 3 (stable structure requires nonzero coherent vacuum), the PF medium carries:

```
Ψ : ℝ³ × ℝ → ℂ,   |Ψ_vac| = ρ₀ > 0
```

- Complex structure is forced by Axiom 2 (real fields cannot encode phase): ARGUED (0.85)
- Nonzero vacuum is forced by Axiom 3 (zero vacuum fails to carry a signal, violating Axiom 1): ARGUED (0.85)
- Single-component minimality for the T2 denominator count: ARGUED (0.80) — conditional on T1's local weight-2 structure being sufficient (see `t2_order_parameter_derivation.md` Section 4)

**Named gap**: `t2_order_parameter_derivation.md` carries Gap OP-1 — Axioms 1-3 do not uniquely rule out `Ψ : ℝ³ × ℝ → ℂⁿ` for `n > 1`; the single-component claim rests on the minimality argument (Section 4 of that file). `t2_coherence_tensor_bridge.md` explores whether a three-component order parameter is forced by T1 — status: does not change T2 status as of 2026-04-01.

No gauge group is assumed. The field `Ψ` carries propagation phase only.

---

## 3. The 2×2 Effective Hamiltonian (from T1)

*The derivation of the `2×2` structure from T1 + Axiom 2 has been moved to a companion file.*

**See**: `t2_fermi_point_bridge.md` Part A for the full derivation (Bridge 2).

**Summary** (for self-containedness):

T1 establishes that weight-2 modes live on the `SU(2)` double cover → state space is `ℂ²`. Axiom 2 requires real eigenvalues → the propagation operator must be Hermitian. Every Hermitian operator on `ℂ²` is a `2×2` Hermitian matrix. By the Pauli decomposition theorem (standard linear algebra, not a physical import):

```
H(k) = h₀(k) · I₂ + h(k) · σ,   h₀ ∈ ℝ,   h = (h₁, h₂, h₃) ∈ ℝ³
```

This form is exhaustive and unique. No condensed-matter band structure is assumed.

**Eigenvalues**: `E±(k) = h₀(k) ± |h(k)|`

**Fermi point**: a momentum `k_F` where `h(k_F) = 0` — two bands become degenerate.

**Named conditional** (`C_FP`): This framing requires the PF medium to have Fermi points in the weight-2 sector. Existence of such points is not derived from Axioms 1-3 alone; it depends on the specific PF dynamics (see `t2_fermi_point_bridge.md` Section A.2).

---

## 4. Co-Dimension of the Fermi Point

**Theorem 4.1 (Co-Dimension of Fermi Points)**:
For a generic smooth map `h : ℝ³ → ℝ³`, the preimage `h⁻¹(0)` consists of isolated points. The co-dimension of these points in momentum space is `3`.

**Proof**:

The condition `h(k_F) = 0` is a system of `3` scalar equations:

```
h₁(k_F) = 0
h₂(k_F) = 0
h₃(k_F) = 0
```

in `3` unknowns `(k_1, k_2, k_3) ∈ ℝ³`.

By the implicit function theorem: if the Jacobian `Dh(k_F)` is nonsingular at a solution `k_F`, then `k_F` is an isolated solution. Generically (for an open dense set of maps `h`), the Jacobian is nonsingular at solutions.

- `3` constraints, `3` variables, generically nonsingular Jacobian → solutions are isolated points
- Co-dimension = number of independent constraints = `3`

In contrast, if momentum space had dimension `d = 2`, we would have `2` unknowns for `3` constraints: generically no solutions (no Fermi points at all). If `d = 4`, we would have `4` unknowns for `3` constraints: generically 1-dimensional curves of solutions (co-dimension 3, but embedded in 4D).

**The key fact used here is `d = 3`** — the premise that physical momentum space is 3-dimensional. □

**Note on genericity**: The Jacobian singularity condition is non-generic (measure zero in function space). For the specific `h(k)` arising from a given PF propagation medium, one should verify that `Dh(k_F)` is nonsingular. This is a remaining audit target.

---

## 5. Mass Space: From Co-Dimension to Restoration Modes

This is the step the 2026-03-28 audit identified as unproved. We close it here.

**Setup**:
A Fermi point `k_F` is where two bands become degenerate: `E₊(k_F) = E₋(k_F)`. At this point the propagation Hamiltonian becomes proportional to the identity:

```
H(k_F) = h₀(k_F) · I₂
```

A **perturbation** to the Hamiltonian — any small modification allowed by the propagation medium — can open a gap at `k_F`. We ask: how many independent perturbations exist that move us away from the gapless point?

**Definition (mass perturbation)**:
A mass perturbation at `k_F` is a Hermitian `2×2` perturbation `δH` that opens a gap at `k_F`. That is, `δH` must break the band degeneracy:

```
δH ≠ α I₂   for any scalar α
```

because `α I₂` shifts both eigenvalues equally and leaves the degeneracy intact.

The mass perturbations are therefore the **traceless** Hermitian `2×2` matrices:

```
δH = m · σ   where m = (m₁, m₂, m₃) ∈ ℝ³
```

**Theorem 5.1 (Mass Space Dimension)**:
The space of mass perturbations at a Fermi point is

```
𝒫 = { m·σ : m ∈ ℝ³ } ≅ ℝ³
```

which is `3`-dimensional.

**Proof**:
The Pauli matrices `{σ₁, σ₂, σ₃}` are linearly independent over `ℝ` — a standard result in linear algebra. Therefore `{σ₁, σ₂, σ₃}` form a basis for the real vector space of traceless Hermitian `2×2` matrices. This space has dimension `3`. □

**Bridge Theorem 5.2 (Restoration-Mode Identification, ARGUED 0.73)**:
There are exactly `3` independent directions in which a mass perturbation can open a gap at the Fermi point. Each such direction corresponds to one independent massive bosonic restoration mode of the PF coherence field.

**See**: `t2_fermi_point_bridge.md` Part B for the full argument (Bridge 3).

**Argument summary**: Each Pauli direction `mᵢσᵢ` opens a distinct gap (proved in Theorem 5.1 by linear independence). Each opened gap is a distinct channel of coherence-field re-locking — a distinct way the phase-unlocked state at `k_F` can restore coherence. Distinct re-locking channels are orthogonal in the `3`-dimensional perturbation space. Three orthogonal independent channels = three independent massive restoration modes. The Volovik ³He-A template confirms this identification in a physically realized system with identical mathematical structure.

**Named conditionals**: conditional on `C_FP` (Fermi points exist in the PF medium) and `C_bridge` (distinct re-locking channels are independent massive bosonic modes — the core Bridge 3 assertion, ARGUED not proved from PF axioms alone). See `t2_fermi_point_bridge.md` Section C.

**v1 audit note**: The 2026-03-31 Codex audit did **not** accept this correspondence as proved from PF axioms alone. Bridge 3 in the companion file addresses this by naming the conditional (`C_bridge`) explicitly and providing the Volovik-template argument for it. Codex re-audit pending.

---

## 6. The Connection Between the Two Results

The co-dimension result (Section 4) and the mass space result (Section 5) are two sides of the same structure:

| Side | Object | Dimension |
|------|--------|-----------|
| Momentum space | co-dimension of Fermi point | 3 |
| Hamiltonian space | dimension of mass perturbation space | 3 |

Both equal `3` because both count the same underlying object: the number of real parameters in the vector `h(k)`.

More precisely: `h : ℝ³ → ℝ³` maps `3`-dimensional momentum space to `3`-dimensional "field space" `ℝ³`. The co-dimension counts the dimension of the target (`3` constraints). The mass space counts the dimension of the source used to parameterize perturbations (`3` independent directions `m ∈ ℝ³`).

Inside the assumed `2×2` Hamiltonian language, this coincidence is not accidental: both counts come from the three real components of `h`. The missing PF theorem is the bridge from this Hamiltonian count to the count of massive restoration modes of the coherence field.

---

## 7. The Volovik ³He Analogy (Template, Not Proof)

Volovik's *Universe in a Helium Droplet* (2003), Chapter 8, uses the identical mathematical structure for the A-phase of superfluid ³He.

The ³He-A order parameter is a `2×2` matrix with:
- Fermi points at `k = ±k_F ẑ`
- Effective Hamiltonian `H(k) = v_F(k_z ∓ k_F)σ₃ + v_⊥(k_x σ₁ + k_y σ₂)`
- `h(k) = (v_⊥ k_x, v_⊥ k_y, v_F(k_z ∓ k_F))`
- Three components → Fermi points have co-dimension 3 in 3D
- Three independent mass perturbations: `(m₁σ₁, m₂σ₂, m₃σ₃)`

Volovik shows these three modes correspond to the three massive bosons acquired when the ³He-A order parameter is perturbed.

**Role here**: The ³He-A example demonstrates that the abstract argument in Sections 4–6 is physically realized in a real condensed-matter system. It is a structural template — confirmation that the mathematics is not vacuous — not a substitute for the PF-internal derivation.

**What differs**: In ³He-A, the order parameter is a specific `2×2` matrix with a known BCS-type form. In PF, the order parameter is the coherence field `Ψ` (Section 2) combined with the T1-forced 2-component spinorial structure. The mathematics of co-dimension and mass space is identical; the physical interpretation differs.

---

## 8. Explicit Derivation Chain (v2 — with bridge companions)

```
Axiom 1 + Axiom 2 + Axiom 3
    ↓
PF coherence field Ψ : ℝ³ × ℝ → ℂ, |Ψ_vac| = ρ₀ > 0
[ARGUED 0.80 — see t2_order_parameter_derivation.md; Gap OP-1 named]
    ↓
T1: closure order 2 → SU(2) double cover → state space ℂ²
[PARTIAL DERIVATION 0.85 — physical-realization bridge still open]
    ↓
Axiom 2: real energies → Hermitian propagation operator
    ↓
2×2 Hermitian Hamiltonian: H(k) = h₀(k)I + h(k)·σ  (Pauli decomposition, Section 3)
[DERIVED inside the 2-component assumption, conditional C_FP]
    ↓
Fermi point: h(k_F) = 0  [conditional C_FP: existence of such points not derived]
    ↓
Premise: d = 3  [explicit input — not derived from PF axioms]
    ↓
Co-dimension theorem: 3 equations in 3 unknowns → isolated Fermi points  (Section 4)
[DERIVED — standard implicit function theorem, conditional C_gen]
    ↓
Mass space: span{σ₁,σ₂,σ₃} ≅ ℝ³, dim = 3  (Section 5, Theorem 5.1)
[DERIVED — standard linear algebra]
    ↓
Bridge 3: each perturbation direction = one massive restoration mode
[ARGUED 0.73 — conditional C_bridge; see t2_fermi_point_bridge.md Part B]
    ↓
M = 3  (Bridge Theorem 5.2)
[CONDITIONAL on C_FP + C_gen + C_bridge + T1 + d=3]
```

---

## 9. Conditional Dependencies (v2 — updated)

**C1 — T1 holds** (`PARTIAL DERIVATION 0.85`): The `(2,1)` topological weight partition must be secure, including the physical-realization bridge for the weight-2 branch. The physical-realization bridge is the live T1 gap (see `t1_t2_post_audit_epic_2026-03-31.md`).

**C2 — Physical space is 3-dimensional**: `d = 3` is an explicit input. PF does not derive it from Axioms 1-3. Named as such throughout.

**C3 / C_gen — Genericity of Jacobian**: The implicit function theorem argument requires `Dh(k_F)` to be nonsingular. Non-generic condition. Unverified for the specific PF Hamiltonian.

**C4 — Single Fermi point topology** (unchanged): Argument is local to one Fermi point. Global mode count requires summing over all Fermi points, weighted by topological charge (Volovik's "monopoles in momentum space"). Not yet written for PF.

**C_FP — Fermi points exist**: The PF weight-2 sector must have band-touching points in momentum space. Not derived from Axioms 1-3. Added in v2 as a named conditional (see `t2_fermi_point_bridge.md` Part A).

**C_bridge — Restoration-mode identification**: Each gap-opening perturbation direction is an independent massive bosonic restoration mode of the PF coherence field. This is the core Bridge 3 assertion. ARGUED (0.73) via the Volovik template. The live Bridge 3 gap (see `t2_fermi_point_bridge.md` Part B, Section D).

**Upgraded from v1**: The PF order parameter is no longer a bare ansatz — it is an ARGUED derivation (0.80) in `t2_order_parameter_derivation.md`. This removes one of the three "not closed" items from the v1 audit, replacing it with a named bounded gap (OP-1).

---

## 10. What This Closes and What It Does Not (v2 — updated after bridge additions)

### What survives from v1 audit (unchanged):
- the exact linear-algebra fact that every `2×2` Hermitian matrix has the form `h₀I + h·σ`
- the conditional lemma: for a generic map `h : ℝ³ → ℝ³`, a band-touching point has co-dimension `3` and the gap-opening perturbation space is `3`-dimensional

### New in v2 — what the companion files add:
- **`t2_order_parameter_derivation.md`**: PF coherence field promoted from bare ansatz to ARGUED (0.80) derivation from Axioms 1-3. Gap OP-1 named (single-component minimality rests on T1 local structure argument).
- **`t2_fermi_point_bridge.md` Part A**: `2×2` Hamiltonian structure derived from T1's `ℂ²` state space + Axiom 2's real-energy requirement, without importing condensed-matter band structure. Conditional `C_FP` named explicitly.
- **`t2_fermi_point_bridge.md` Part B**: Restoration-mode identification argued (0.73) via the Volovik template. Conditional `C_bridge` named explicitly.

### Still not closed after v2:
- T1 physical-realization bridge (this file takes T1 as input)
- `C_FP`: Fermi points must exist in the PF weight-2 sector — not derived
- `C_bridge`: each gap-opening direction is a massive bosonic restoration mode — ARGUED, not proved from PF axioms alone
- `d = 3` derivation from PF axioms
- global topology of multiple Fermi points
- `C_gen`: Jacobian nonsingularity at specific PF Fermi points

### Progress map (v1 → v2):

| Gap | v1 status | v2 status |
|-----|-----------|-----------|
| PF order parameter | bare ansatz | ARGUED 0.80, Gap OP-1 named |
| `2×2` Hamiltonian from T1 | imported | derived conditional on C_FP |
| restoration-mode identification | unaddressed | ARGUED 0.73, C_bridge named |
| T1 physical-realization | PARTIAL DERIVATION | unchanged |
| `d = 3` | input, unnamed | input, named explicitly |
| Fermi point existence | unnamed | C_FP named |
| Jacobian genericity | unnamed | C_gen named |

### CLAIMS.md status:
T2 remains `PARTIAL DERIVATION 0.85` until Codex audits the v2 companion files. If Codex signs off on all three bridges (OP derivation, `2×2` Hamiltonian, restoration-mode identification), T2 may upgrade to `CONDITIONAL 0.88` (conditional on T1, `d=3`, `C_FP`, `C_gen`, `C_bridge`, and `C_local`). Do not promote without Codex sign-off.

---

## 11. Codex Audit Target

The following are the specific points Codex should verify:

**Audit item A**: Is the PF order parameter definition in Section 2 consistent with the existing `theory_of_propagation.md` and `axiom3_coherence_functional_spec.md`? Does it import anything beyond Axioms 1-3?

**Audit item B**: Is the derivation of `H(k) = h₀I + h·σ` from T1 clean? The claim is that weight-2 (spinorial) structure + Axiom 2 (dispersion relations) forces a `2×2` Hermitian Hamiltonian. Does this step hold without importing a spin group by hand?

**Audit item C**: Is the implicit function theorem application in Section 4 formally correct? Specifically: is the genericity assumption on `Dh(k_F)` defensible in the PF context, or is there a reason the PF Hamiltonian is non-generic (e.g., has extra symmetry that forces `Dh` to be singular)?

**Audit item D**: Does Corollary 5.2 actually close the gap named in HA-20260328-008? The audit asked for proof that "co-dim(point defect) = number of massive bosonic restoration modes." Is the argument in Sections 4-6 a proof of that, or does it shift the hidden step somewhere else?

**Audit item E**: Does the `d = 3` premise need to be named in `CLAIMS.md` as an explicit input to T2? Or can it be absorbed into the "physical momentum space" framing without generating a new open front?

---

## 12. Codex Audit Result (v1 — 2026-03-31)

See `derivations/t2_denominator_theorem_audit_2026-03-31.md`.

Short version:
- the co-dimension and mass-space lemmas survive **inside** the assumed `2×2` Fermi-point Hamiltonian language
- the PF order-parameter and Hamiltonian bridge do **not** yet follow from the PF axioms alone
- Corollary 5.2 does **not** yet prove that these three perturbation directions are the three massive bosonic restoration modes of the PF coherence field
- therefore T2 remains `PARTIAL DERIVATION 0.85`

---

## 13. Codex Audit Targets (v2 — for companion files)

*These items are for Codex's re-audit of the v2 bridge companion files. They supersede the v1 audit items A-E.*

**Audit item A'** (`t2_order_parameter_derivation.md`):
- A'1: Does the Axiom 2 argument (complex structure from wave dispersion) hold without importing quantum mechanics or a spin group? The claim is purely about the phase degree of freedom in classical wave solutions.
- A'2: Does the Axiom 3 argument (nonzero vacuum) hold from the Coherence axiom as stated in `the_propagation_framework.md`?
- A'3: Is the Section 4 minimality argument correct — specifically that T1's local weight-2 structure makes the single-component global order parameter sufficient for the denominator count?
- A'4: Does the derived PF coherence field match `axiom3_coherence_functional_spec.md` and `theory_of_propagation.md` without importing their structure?

**Audit item B'** (`t2_fermi_point_bridge.md` Part A):
Does the derivation of `H(k) = h₀I + h·σ` from T1's `ℂ²` state space + Axiom 2's real-energy requirement hold without importing a spin group by hand? Specifically: does T1's "weight-2 mode lives on `SU(2)` double cover" directly imply that the mode state lives in `ℂ²` without additional input?

**Audit item C'** (`t2_fermi_point_bridge.md` Part A, conditional C_FP):
Is `C_FP` (existence of Fermi points in the PF weight-2 sector) a serious gap that should be elevated to the main claims board? Can it be addressed by a general argument that weight-2 propagation modes in 3D must have band crossings under Axioms 1-3, or does it require specifying the PF dynamics more concretely?

**Audit item D'** (`t2_fermi_point_bridge.md` Part B, Bridge 3):
Does the Bridge 3 argument prove that the three Pauli perturbation directions are the three massive bosonic restoration modes of the PF coherence field? Or does it shift the hidden step to "channels of coherence-field re-locking are independent massive bosonic modes" (conditional `C_bridge`) — in which case `C_bridge` should be named as a new formal gap on the claims board?

**Audit item E'** (cross-cutting):
Does the `d = 3` dependence remain explicit and correctly named throughout v2? Does it need to be added as a named row on the `CLAIMS.md` board as a PF input assumption, or can it remain as an implicit premise of the Fermi-point route?

---

*Claude (v2 additions) — 2026-03-31*
*v1 Codex audit received 2026-03-31. No status upgrade. v2 companion files submitted for Codex re-audit.*
