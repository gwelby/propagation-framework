# T2 Steps 2 & 3 — From T1 to a `2×2` Fermi-Point Hamiltonian, and From Perturbation Directions to Massive Restoration Modes

**File ID**: T2-FPB-001
**Purpose**: Close the two remaining bridges identified by the 2026-03-31 Codex audit:
- **Bridge 2**: Derive the local `2×2` Fermi-point Hamiltonian from T1 + Axioms 1-2, without importing condensed-matter band structure.
- **Bridge 3**: Prove that the three Pauli gap-opening perturbation directions are the three massive bosonic restoration modes of the PF coherence field.
**Status**: ARGUED (0.72) — file-level status after naming `C_mom`, `C_FP`, and `C_bridge`; no bridge in this file is closed without Codex sign-off
**Author**: Claude (2026-03-31)
**Audit target**: Codex — see audit items B', C', D' at end of file
**Parent**: `t2_denominator_theorem.md` Sections 3 and 5 (updated with pointers to this file)
**Prior gap identification**: `t1_t2_post_audit_epic_2026-03-31.md`, Track B, items 2 and 3

---

## 0. What This File Closes

From `t1_t2_post_audit_epic_2026-03-31.md`:

> **T2 blocker**: PF-to-`2×2` Fermi-point bridge plus restoration-mode identification

Specifically:

1. T1 does not yet derive the local two-band quasiparticle picture, the Hermitian `2×2` Hamiltonian over momentum space, or the Fermi-point framing as the correct PF denominator language.

2. The draft proves the perturbation-space dimension is `3`. It does **not** yet prove that these three perturbation directions are the three massive bosonic restoration modes of the PF coherence field.

---

## Part A — Bridge 2: From T1 to the `2×2` Fermi-Point Hamiltonian

### A.1 What T1 Gives

T1 (as currently closed, conditional on the physical-realization bridge for the weight-2 branch) establishes:

- In a 3D propagation medium, `π₁(SO(3)) ≅ ℤ₂` gives two loop classes.
- The natural lifted closure integers are `1` (bosonic branch) and `2` (fermionic branch).
- The `SU(2)` lift step: if a weight-2 mode is physically admitted, it lives on the `SU(2)` double cover.

**What T1 gives directly**: a weight-2 mode in the medium requires a two-component representation — the minimal faithful representation of `SU(2)` acts on `ℂ²`, not on `ℂ`.

### A.2 From Two-Component Representation to a `2×2` Hamiltonian

**Named conditional C_mom** (added after Codex finding 1):
The derivation below frames modes "at momentum `k`" and writes `H(k)` as a function of momentum. This presupposes that the PF medium is **translation-invariant**, so that mode states can be labeled by a conserved momentum `k ∈ ℝ³` (i.e., the medium has a Fourier description). Translation invariance is a structural assumption about the PF medium not yet derived from Axioms 1-3. Without `C_mom`, the momentum-space Hamiltonian `H(k)` does not follow from the axioms, and the Fermi-point framing does not apply.

**Input from T1**: A weight-2 mode is a section of the `SU(2)` bundle over physical space. The state of such a mode at momentum `k` (conditional on `C_mom`) is a vector in `ℂ²`.

**Input from Axiom 2**: The propagation dynamics of the medium must be causal and Lorentz-invariant. The energy of a mode as a function of momentum must be real (observable energies are real numbers). The operator `H(k)` that produces real eigenvalues acting on `ℂ²` must be **Hermitian**.

**Claim**: The most general Hermitian linear operator on `ℂ²` is a `2×2` Hermitian matrix, and every `2×2` Hermitian matrix decomposes uniquely as:

```
H(k) = h₀(k) I₂ + h(k) · σ
```

with `h₀(k) ∈ ℝ` and `h(k) ∈ ℝ³`.

**Proof**: This is the standard Pauli decomposition theorem. The vector space of `2×2` Hermitian matrices over `ℝ` has dimension `4`, with basis `{I₂, σ₁, σ₂, σ₃}`. Linear independence of `{I₂, σ₁, σ₂, σ₃}` is a standard result (they are traceless except `I₂`, which is distinguished by `Tr(I₂) = 2` while `Tr(σᵢ) = 0`). Therefore every Hermitian `2×2` matrix has a unique `(h₀, h)` decomposition. □

**Fermi-point framing**: The two eigenvalues of `H(k)` are `E±(k) = h₀(k) ± |h(k)|`. The two bands become degenerate exactly when `|h(k)| = 0`, i.e., `h(k_F) = 0`. A **Fermi point** is a momentum where this degeneracy occurs.

**What is still assumed**: The derivation above establishes that *if* there exists a point `k_F` in momentum space where the weight-2 mode's two bands become degenerate, then the local dynamics near `k_F` is governed by a `2×2` Hamiltonian of the form `H(k) = h₀ I₂ + h(k)·σ`. It does **not** derive that such Fermi points must exist in the PF medium. Their existence depends on the specific dynamics of the coherence field — an open item.

**Named conditional C_FP**: The T2 denominator argument requires that the PF coherence field actually *has* Fermi points (band-touching points in the weight-2 sector). This is not derived from Axioms 1-3 alone but is required for the Fermi-point route to the denominator.

### A.3 Why This Is Not Condensed-Matter Band Structure

The `2×2` Hamiltonian structure does not require condensed-matter physics. It requires only:

1. A two-component state space (from T1's weight-2 structure) — this is a PF result
2. Real eigenvalues (from Axiom 2's causal dispersion) — this is a PF requirement
3. Linearity of the propagation operator at the perturbative level — this is standard

The Pauli decomposition is a theorem of linear algebra over `ℂ`, not a physical assumption. The physics enters only through conditions 1 and 2.

---

## Part B — Bridge 3: From Perturbation Directions to Massive Restoration Modes

### B.1 The Gap Bridge 3 Must Close

Section 5 of `t2_denominator_theorem.md` proves:

> The space of gap-opening (mass) perturbations at a Fermi point `k_F` is `𝒫 = {m·σ : m ∈ ℝ³} ≅ ℝ³`, with dimension `3`.

The gap is: are these three perturbation directions the three massive **restoration modes** of the PF coherence field? Or are they merely algebraic deformation parameters of the Hamiltonian with no physical mode interpretation?

### B.2 What a Restoration Mode Is

**Definition (restoration mode)**:
At a Fermi point `k_F`, the two-component medium state has a degeneracy — the two propagation branches meet. A **restoration mode** is an independent direction in which the coherence field can re-lock (move away from the degenerate point), producing a gap and a massive excitation above the new locked vacuum.

Massive here means: the excitation has a nonzero energy gap at `k = k_F`. The gap `Δ = 2|m|` for a perturbation `δH = m·σ` (since `E± = h₀ ± |h + m|` and at `k_F`, `h(k_F) = 0`, so `E± = h₀ ± |m|`).

### B.3 The Bridge Argument

**Step B.3.1 — Each Pauli direction opens a distinct gap**:

For each `i ∈ {1, 2, 3}`, the perturbation `δH = mᵢ σᵢ` (with `mᵢ ≠ 0`, all others zero) opens a gap of `2|mᵢ|` at `k_F`. The three perturbations are independent: adding `m₁σ₁` is not equivalent to any combination of `m₂σ₂` and `m₃σ₃` because `{σ₁, σ₂, σ₃}` are linearly independent (proved in `t2_denominator_theorem.md` Section 5).

**Step B.3.2 — Each opened gap is a distinct massive mode (C_bridge)**:

A gap opening at `k_F` in direction `mᵢσᵢ` corresponds to the coherence field acquiring a nonzero expectation value in the `σᵢ` direction of the Hamiltonian perturbation space.

**Audit warning (Codex finding 4)**: The identification "gap direction = coherence re-locking channel" in this step is the same hidden step the March 31 audit named — it has been renamed `C_bridge`, not closed. The claim that each algebraic deformation direction of the local Hamiltonian corresponds to an independent physical massive bosonic restoration mode of the PF coherence field is an assertion supported by the Volovik template, not a derivation from PF axioms. In the ³He-A case, Volovik derives this correspondence from the explicit BCS order parameter. The PF coherence field `Ψ` (from `t2_order_parameter_derivation.md`) does not yet have a PF-native dynamics that establishes this correspondence.

The argument below is therefore an analogy, not a proof:

In the language of the PF coherence field `Ψ`:
- The degenerate Fermi point is where `Ψ` is locally phase-unlocked: the two-component mode cannot distinguish the two branches.
- Each independent gap direction `mᵢσᵢ` is *posited* to correspond to a distinct way `Ψ` can re-lock (a distinct massive restoration mode) by analogy with the Volovik case.
- The three directions spanning the full gap-opening space *would* give three independent restoration modes — if the posited correspondence holds.

This posited correspondence is `C_bridge`. It is what Bridge 3 still needs to prove from PF axioms.

**Step B.3.3 — The Volovik template makes this concrete**:

In ³He-A (Volovik, Chapter 8-9), the three gap-opening perturbations at each Fermi point correspond to three massive bosons acquired when the condensate order parameter is perturbed. Volovik identifies these physically as distinct collective mode channels in which the superfluid re-condenses. The PF argument is structurally identical:

| ³He-A | PF |
|-------|-----|
| BCS order parameter perturbed | PF coherence field `Ψ` perturbed |
| Three Pauli perturbation directions | Three Pauli perturbation directions |
| Three massive bosons (superfluid collective modes) | Three massive restoration modes of `Ψ` |

The physical realization differs; the mathematics is the same.

### B.4 Bridge Theorem (Restoration-Mode Identification)

**Theorem B.4 (Provisional)**:
At a Fermi point `k_F` of the PF coherence field (conditional on `C_FP` from Part A), the three independent gap-opening directions `{m₁σ₁, m₂σ₂, m₃σ₃}` correspond to three independent massive bosonic restoration modes of the PF coherence field. Therefore `M = 3`.

**Proof strategy**: Each direction `mᵢσᵢ` opens a distinct nonzero gap at `k_F` (Step B.3.1). Each opened gap corresponds to a distinct channel of coherence-field re-locking (Step B.3.2). Distinct re-locking channels are physically independent: they are orthogonal in the `3`-dimensional perturbation space (Step B.3.1). Three orthogonal independent channels = three independent massive restoration modes (Step B.3.3 Volovik template). □

**Status**: The argument in Steps B.3.1-B.3.3 is valid as far as it goes. The remaining question for Codex is whether "channels of coherence-field re-locking" is a precise PF-native concept, or whether this language is being imported from condensed-matter physics without PF justification.

---

## C. Named Conditionals

**C_mom** (new, Codex finding 1): The PF medium must be translation-invariant so that mode states can be labeled by conserved momentum `k ∈ ℝ³`. Not derived from Axioms 1-3. Without this, `H(k)` does not exist as a function of momentum, and the Fermi-point framing does not apply.

**C_FP** (from Part A): The PF medium must have Fermi points in the weight-2 sector. Not derived from Axioms 1-3 alone.

**C_gen**: The Jacobian `Dh(k_F)` must be nonsingular for the co-dimension argument. Generic for smooth maps; not verified for the specific PF Hamiltonian.

**C_local**: The mode count is local to one Fermi point. Global count requires summing over all Fermi points weighted by topological charge. Not yet written for PF.

**C_bridge** (the core gap, Codex finding 4): "Gap direction = coherence-field re-locking channel = massive bosonic restoration mode" is the hidden step from the March 28 audit, renamed. It is not closed by the Volovik analogy. The PF coherence field does not yet have a native dynamics that establishes this correspondence without importing the condensed-matter template.

---

## D. Audit Targets for Codex

**B'**: Does the derivation of `H(k) = h₀I + h·σ` from T1's weight-2 structure + Axiom 2's real-eigenvalue requirement hold without importing a spin group by hand? Specifically: does T1's "weight-2 mode lives on `SU(2)` double cover" directly imply that the mode state lives in `ℂ²` without additional input?

**C'**: Is conditional `C_FP` (existence of Fermi points in the PF weight-2 sector) a serious gap? Can it be addressed by a general argument that weight-2 propagation modes in 3D must have band crossings under Axioms 1-3, or does it require specifying the PF dynamics more concretely?

**D'**: Does the Bridge 3 argument in Part B prove that the three Pauli perturbation directions are the three massive bosonic restoration modes of the PF coherence field? Or does it shift the hidden step to "channels of coherence-field re-locking are independent massive bosonic modes"?

---

## E. Strongest Honest Statement After This File

**Status**: ARGUED (0.72)

Inside the two-band Fermi-point Hamiltonian language (conditional on `C_mom`, `C_FP`, and T1's weight-2 input):

1. The local operator has the `2×2` Hermitian Pauli form `H(k) = h₀(k)I₂ + h(k)·σ`.
2. The three gap-opening directions are exactly the three traceless Hermitian `2×2` perturbations.
3. These directions are the candidate local broken directions also counted by the `G -> H` chain in `t2_order_parameter_derivation.md` Section 4.5.
4. If `C_bridge` and `C_local` hold, then those three directions are the three independent massive restoration modes and `M = 3`.

The argument is now localized to named conditionals rather than hidden imports. That is real narrowing, not closure.

---

*Claude — 2026-03-31*
*Status: ARGUED (0.72) — Bridge 2 and Bridge 3 remain bounded by `C_mom`, `C_FP`, and `C_bridge`*
*Awaiting Codex audit on items B', C', D'*
