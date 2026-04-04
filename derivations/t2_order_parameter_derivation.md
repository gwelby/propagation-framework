# T2 Step 1 — PF Order Parameter: From Axioms 1-3 to the Coherence Field

**File ID**: T2-OP-001
**Purpose**: Promote the PF coherence field from a model ansatz (as it stood in the initial T2 draft) to a theorem derived from Axioms 1-3 alone.
**Status**: ARGUED (0.72) — Gap OP-1a and Gap OP-2 keep the order-parameter bridge bounded; the single-component claim remains argued, not proved.
**Author**: Claude (2026-03-31)
**Audit target**: Codex — see audit items A'1 through A'4 at end of file
**Parent**: `t2_denominator_theorem.md` Section 2 (replaced with pointer to this file)

---

## 0. What This File Closes

The 2026-03-31 Codex audit of `t2_denominator_theorem.md` found:

> The coherence field `Ψ : ℝ³ × ℝ → ℂ` with `|Ψ_vac| = ρ₀ > 0` is a model ansatz, not a theorem from Axioms 1-3 alone.

This file derives the coherence field from Axioms 1-3, or at minimum promotes it from a bare ansatz to a bounded conditional claim with named assumptions.

---

## 1. Starting from Axiom 1: What the Medium Must Carry

**Axiom 1** (Propagation is Fundamental): Everything that exists propagates. The medium is not empty space but a field capable of carrying a signal.

For the medium to carry a signal, it must have a **state** at each point that can vary in time and space — otherwise it cannot carry anything. The minimal such state is a map:

```
σ : ℝ³ × ℝ → S
```

where `S` is the state space of the medium at a single point.

What must `S` contain? At minimum:
- **An amplitude** encoding signal strength (a non-negative real number)
- **A phase** encoding the propagation direction in the medium's cycle

This is the minimal signal-carrying state. We do not assert `S` is larger without additional input.

---

## 2. Axiom 2 Forces Complex Structure

**Axiom 2** (Finite Causal Velocity): Every medium has a maximum signal speed `c`. No causal influence propagates faster.

Axiom 2 establishes a finite maximum signal speed `c`. It does not specify a particular dispersion relation — `ω² = c²|k|²` (massless relativistic) is one possible form; other dispersive media with finite speed also satisfy Axiom 2. What Axiom 2 does force is that wave solutions of the medium must have a well-defined phase: at each point the medium state can advance or lag, and this phase is a degree of freedom independent of amplitude.

**Claim**: The medium state requires a two-parameter local description (amplitude + phase). The natural minimal algebraic packaging of these two parameters is a complex number.

**Argument**:

A propagating wave mode at momentum `k` has a linearized perturbation of the form:

```
δσ(x, t) = A cos(k·x − ωt + φ)
```

This requires two real parameters per mode: amplitude `A` and phase `φ`. The complex number `ψ = A e^{iφ}` packages both in a single algebraic object, making superposition and phase arithmetic natural.

A strictly real-valued state space `S = ℝ` can encode amplitude but cannot directly represent the phase degree of freedom without doubling the state space — which is precisely what `ℂ = ℝ²` with complex multiplication does. Two-component real vectors `(A, φ)` ∈ ℝ² would also work algebraically; `ℂ` is the standard packaging with the additional structure of complex multiplication.

**Gap OP-1a** (named): Axiom 2 motivates `ℂ` as the natural minimal encoding, but does not uniquely force `ℂ` over `ℝ²` as the state space. Both are two-dimensional over `ℝ`. The choice of `ℂ` (with its multiplicative structure) is natural for wave physics but is argued, not proved from Axiom 2 alone.

**Conclusion**: The medium state field is:

```
Ψ : ℝ³ × ℝ → ℂ
```

where `ℂ` is the natural minimal packaging. **Note**: This argument does not rule out higher-dimensional `S = ℂⁿ` for `n > 1`. That is addressed in Section 4. □

---

## 3. Axiom 3 Forces a Nonzero Coherent Vacuum

**Axiom 3** (Coherence): Stable structure requires self-reinforcing, coherent propagation. Incoherent modes disperse.

Apply Axiom 3 to the uniform state `Ψ = const`:

- If `Ψ_vac = ρ₀ e^{iφ_0}` with `ρ₀ > 0`: the medium carries a uniform coherent amplitude. By Axiom 3, this self-reinforcing coherent state is stable.
- If `|Ψ_vac| = 0`: the mean field is zero. A zero-mean-field state can still support propagating perturbations — Axiom 1 is not violated. However, a zero mean field has no coherent amplitude to self-reinforce: Axiom 3 requires self-reinforcing propagation for stable structure, and a state with `ρ₀ = 0` has no mean coherence to reinforce.

**Gap OP-2** (named): The argument above is weaker than claimed in the original draft. A medium with `ρ₀ = 0` can carry signal through perturbations even if the mean field is zero (standard field theory in the symmetric/unbroken phase). Axiom 3 as currently stated ("stable structure requires self-reinforcing, coherent propagation; incoherent modes disperse") must be interpreted as requiring a nonzero coherent mean field, not merely the existence of perturbations, for `ρ₀ = 0` to be forbidden. This interpretation is natural but is an argued reading of Axiom 3, not a clean logical consequence.

**Conclusion (conditional on Gap OP-2 reading)**:

```
|Ψ_vac| = ρ₀ > 0
```

Under the interpretation that Axiom 3 selects states with nonzero coherent mean field, the PF vacuum is nonzero. Phase `φ_0` is undetermined (U(1) degree of freedom in the vacuum). □

---

## 4. Minimality: Why a Single Complex Scalar Rather Than `ℂⁿ`

The argument in Sections 2-3 shows `Ψ : ℝ³ × ℝ → ℂ` is the minimal complex field consistent with Axioms 1-3. Sections 2-3 do not rule out `Ψ : ℝ³ × ℝ → ℂⁿ` for `n > 1`.

**Minimality argument**:

T2's role is to derive the denominator `M` — the count of massive restoration modes at a Fermi point. This count is a property of the **local** gap-opening structure, which is controlled by the local Hamiltonian perturbation space (as derived in `t2_fermi_point_bridge.md`, Steps 2-3). The local perturbation space dimension depends on the **weight-2 (two-component) structure** forced by T1, not on the number of independent complex components in the global order parameter.

Therefore: for the purpose of T2's denominator count, the single complex scalar `Ψ` is sufficient. A multi-component order parameter would require T1 to specify additional structure — if T1 forces weight-2 at the single-mode level, then the local Hamiltonian at a Fermi point has the `2×2` structure that controls the denominator, regardless of whether the global order parameter has one or more complex components.

**Named conditional**: If the PF coherence field turns out to require `n > 1` complex components for reasons not yet derived (e.g., from the full three-axiom structure plus T1), this file's conclusion may be a lower bound rather than an exact characterization. That would be a scope extension of T2, not a refutation.

---

## 4.5 PF Symmetry-Breaking Chain

This subsection records the formal `G -> H` chain required by the T2 ticket. It does not upgrade the file beyond `ARGUED (0.72)`: the group-theoretic count still depends on T1's local weight-2 input and on `C_bridge` from `t2_fermi_point_bridge.md`.

**Pre-locking local data**:
Sections 2-3 argue for a nonzero complex coherence amplitude. If T1's weight-2 branch is locally realized, the unlocked local state is naturally written as a nonzero two-component complex vector

```
q ∈ ℂ² \ {0}.
```

The natural linear symmetry acting on this local data is

```
G = U(2).
```

This is the largest unitary group preserving the Hermitian norm on the two-component complex state.

**Post-locking residual symmetry**:
Coherence locking selects a definite local ray `[q_0]` in `ℂ²`. The subgroup preserving the locked ray up to overall phase is

```
H = U(1).
```

So the post-locking state keeps only the residual global phase freedom.

**Broken-generator count**:
The real dimensions are

```
dim_R U(2) = 4,   dim_R U(1) = 1,
```

hence

```
dim_R(G/H) = 4 - 1 = 3.
```

**Pauli realization**:
At the locked state, the tangent directions orthogonal to the residual `U(1)` phase are represented by the traceless Hermitian generators

```
{σ₁, σ₂, σ₃}.
```

So the broken directions are the same three real directions that appear in the local `2×2` Hamiltonian perturbation space.

**Lemma 4.5.1 (Conditional symmetry count)**:
If the PF weight-2 sector admits the local `2×2` Hamiltonian description of `t2_fermi_point_bridge.md` Part A, then the broken directions of `G/H` are three-dimensional and match the Pauli perturbation space.

**Corollary 4.5.2 (Conditional route to `M = 3`)**:
If, in addition, `C_bridge` holds — i.e. each broken Pauli direction is an independent massive restoration mode of the PF coherence field — then

```
M = dim_R(G/H) = 3.
```

This is the PF analogue of the Volovik-style symmetry-breaking count. It is a real narrowing of the T2 target, not a closure of Bridge 3. □

---

## 5. The Derived PF Order Parameter

**Theorem (PF Coherence Field, bounded form)**:
Axioms 1-3 argue that the PF medium is described, at minimum, by a complex-valued coherence field

```
Ψ : ℝ³ × ℝ → ℂ
```

with the following bounded claims:

- Complex structure ARGUED by Axiom 2 (Gap OP-1a: `ℂ` is natural packaging, not uniquely forced over `ℝ²`): ARGUED (0.72)
- Nonzero vacuum ARGUED by Axiom 3 (Gap OP-2: zero-mean-field can support perturbations; requires specific Axiom 3 reading): ARGUED (0.72)
- Single-component minimality ARGUED (0.72), Gap OP-1a named in companion
- Phase `φ_0` is undetermined at the uniform level (`U(1)` residual phase freedom)

For the purpose of the T2 denominator count, the local weight-2 structure from T1 is the controlling input; the global single-component order parameter remains argued rather than proved.

**Status of this theorem**: ARGUED (0.72)

---

## 6. The Remaining Gap (Named for Codex)

The surviving order-parameter gap is:

> **Remaining global-component gap**: Sections 2-5 argue for a complex coherence field with nonzero coherent mean amplitude, but Axioms 1-3 do not uniquely force the global component count to be one. The T2 denominator count uses T1's local weight-2 structure and the local `2×2` Hamiltonian language; it does not yet prove that the full PF order parameter cannot be `ℂⁿ` for `n > 1`.

This gap does not block the local T2 denominator argument directly, because the denominator count is local (it uses the Fermi-point Hamiltonian, not the full global order-parameter manifold). It remains named here for completeness and Codex verification.

---

## Audit Targets for Codex

**A'1**: Does the Axiom 2 argument in Section 2 (complex structure from wave dispersion) hold without importing quantum mechanics or a spin group? The claim is purely about the phase degree of freedom in classical wave solutions.

**A'2**: Does the Axiom 3 argument in Section 3 (nonzero vacuum) hold from the Coherence axiom as stated in `the_propagation_framework.md`? Does it require a stronger form of Axiom 3 than currently written?

**A'3**: Is the minimality argument in Section 4 correct — specifically the claim that T1's local weight-2 structure makes the single-component global order parameter sufficient for the denominator count?

**A'4**: Does the derived PF coherence field in Section 5 match the existing `axiom3_coherence_functional_spec.md` and `theory_of_propagation.md`? Does it import structure from those files, or is it independently derived here?

---

*Claude — 2026-03-31*
*Status: ARGUED (0.72) — promotes the PF order parameter from bare ansatz to bounded derivation*
*Awaiting Codex audit before this file upgrades T2's OP-bridge status*
