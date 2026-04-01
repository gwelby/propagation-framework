# T2 Step 1 — PF Order Parameter: From Axioms 1-3 to the Coherence Field

**File ID**: T2-OP-001
**Purpose**: Promote the PF coherence field from a model ansatz (as it stood in the initial T2 draft) to a theorem derived from Axioms 1-3 alone.
**Status**: ARGUED (0.80) — the minimal-scalar claim survives; the single-component claim requires the additional minimality argument in Section 4.
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

Axiom 2 forces wave-like solutions on the medium state. Specifically, linear perturbations of `σ` around a uniform state must satisfy a wave equation with dispersion relation:

```
ω² = c² |k|²
```

This is the relativistic dispersion relation with no preferred frame (Axiom 2 is Lorentz-invariant).

**Claim**: The minimal state space `S` consistent with this dispersion relation is `ℂ`, not `ℝ`.

**Proof**:

Consider a linearized perturbation `δσ` around a uniform medium state. The general real solution to `ω² = c²|k|²` for a single wave mode is:

```
δσ(x, t) = A cos(k·x − ωt + φ)
```

This requires tracking two real parameters per mode: amplitude `A` and phase `φ`. The natural algebraic packaging of `(A, φ)` is a complex number:

```
ψ = A e^{iφ}
```

so that `δσ = Re(ψ e^{i(k·x − ωt)})`.

A real-valued state space `S = ℝ` cannot algebraically encode the phase `φ` without introducing an auxiliary variable — which is precisely what `ℂ` is. The complex structure is therefore not imported; it is forced by the need to parameterize the solution space of the Axiom-2 wave equation with a single algebraic object.

**Conclusion**: The medium state field is:

```
Ψ : ℝ³ × ℝ → ℂ
```

**Note**: This argument shows `ℂ` is natural; it does not yet rule out higher-dimensional `S` (e.g., `S = ℂⁿ` for `n > 1`). That is addressed in Section 4. □

---

## 3. Axiom 3 Forces a Nonzero Coherent Vacuum

**Axiom 3** (Coherence): Stable structure requires self-reinforcing, coherent propagation. Incoherent modes disperse.

Apply Axiom 3 to the uniform state `Ψ = const`:

- If `|Ψ_vac| = 0`: the medium carries no signal. By Axiom 1, this is not a physical medium — it cannot carry anything. Forbidden.
- If `Ψ_vac = ρ₀ e^{iφ_0}` with `ρ₀ > 0`: the medium carries a uniform phase, which is a coherent state. This is the maximal-coherence uniform solution. By Axiom 3, this mode does not disperse; it is stable.

**Conclusion**:

```
|Ψ_vac| = ρ₀ > 0
```

The vacuum of the PF coherence field is nonzero. Phase `φ_0` is arbitrary (no preferred phase — this is the U(1) degree of freedom in the vacuum). □

---

## 4. Minimality: Why a Single Complex Scalar Rather Than `ℂⁿ`

The argument in Sections 2-3 shows `Ψ : ℝ³ × ℝ → ℂ` is the minimal complex field consistent with Axioms 1-3. Sections 2-3 do not rule out `Ψ : ℝ³ × ℝ → ℂⁿ` for `n > 1`.

**Minimality argument**:

T2's role is to derive the denominator `M` — the count of massive restoration modes at a Fermi point. This count is a property of the **local** gap-opening structure, which is controlled by the local Hamiltonian perturbation space (as derived in `t2_fermi_point_bridge.md`, Steps 2-3). The local perturbation space dimension depends on the **weight-2 (two-component) structure** forced by T1, not on the number of independent complex components in the global order parameter.

Therefore: for the purpose of T2's denominator count, the single complex scalar `Ψ` is sufficient. A multi-component order parameter would require T1 to specify additional structure — if T1 forces weight-2 at the single-mode level, then the local Hamiltonian at a Fermi point has the `2×2` structure that controls the denominator, regardless of whether the global order parameter has one or more complex components.

**Named conditional**: If the PF coherence field turns out to require `n > 1` complex components for reasons not yet derived (e.g., from the full three-axiom structure plus T1), this file's conclusion may be a lower bound rather than an exact characterization. That would be a scope extension of T2, not a refutation.

---

## 5. The Derived PF Order Parameter

**Theorem (PF Coherence Field)**:
From Axioms 1-3 alone, the medium carries a complex-valued field

```
Ψ : ℝ³ × ℝ → ℂ
```

with:
- `Ψ` satisfies a wave equation with dispersion `ω² = c²|k|²` at the linear level (Axiom 2)
- The vacuum satisfies `|Ψ_vac| = ρ₀ > 0` (Axiom 3 selects nonzero coherent vacuum)
- Phase `φ_0` is undetermined at the uniform level (residual U(1) symmetry)

For the purpose of the T2 denominator count, this single complex scalar is the sufficient minimal object, given T1's constraint to weight-2 local structure.

**Status of this theorem**: ARGUED (0.80).

- The complex structure follows cleanly from Axiom 2 (Section 2 proof).
- The nonzero vacuum follows cleanly from Axiom 3 (Section 3 proof).
- The single-component minimality claim (Section 4) is argued, not proved: it rests on the claim that T1's local weight-2 structure is sufficient for the denominator count, without requiring a global multi-component order parameter. Codex should verify this.

---

## 6. The Remaining Gap (Named for Codex)

The surviving gap is:

> **Gap OP-1**: The Axioms 1-3 argument establishes that `Ψ : ℝ³ × ℝ → ℂ` with `|Ψ_vac| = ρ₀` is the minimal consistent field. But Axioms 1-3 do not uniquely force a single complex scalar — they rule out real-valued fields and zero vacuum, while leaving open the possibility of a higher-dimensional complex order parameter. For the denominator count, this gap is filled by T1's local weight-2 structure (see `t2_fermi_point_bridge.md`), but the global order parameter determination remains a formal open item.

This gap does not block the T2 denominator argument, because the denominator count is local (it uses the Fermi-point Hamiltonian, not the global order parameter structure). It is named here for completeness and Codex verification.

---

## Audit Targets for Codex

**A'1**: Does the Axiom 2 argument in Section 2 (complex structure from wave dispersion) hold without importing quantum mechanics or a spin group? The claim is purely about the phase degree of freedom in classical wave solutions.

**A'2**: Does the Axiom 3 argument in Section 3 (nonzero vacuum) hold from the Coherence axiom as stated in `the_propagation_framework.md`? Does it require a stronger form of Axiom 3 than currently written?

**A'3**: Is the minimality argument in Section 4 correct — specifically the claim that T1's local weight-2 structure makes the single-component global order parameter sufficient for the denominator count?

**A'4**: Does the derived PF coherence field in Section 5 match the existing `axiom3_coherence_functional_spec.md` and `theory_of_propagation.md`? Does it import structure from those files, or is it independently derived here?

---

*Claude — 2026-03-31*
*Status: ARGUED 0.80 — promotes the PF order parameter from bare ansatz to bounded derivation*
*Awaiting Codex audit before this file upgrades T2's OP-bridge status*
