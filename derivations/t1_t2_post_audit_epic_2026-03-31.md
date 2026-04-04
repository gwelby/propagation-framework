# T1 / T2 Post-Audit Epic — Path to Truth Verification

*What still needs to close after the 2026-03-31 bounded theorem audits*

---

## Purpose

This note replaces the older pre-audit epic language for the T1 numerator route and the T2 denominator route.

Both fronts materially improved on 2026-03-31.
Neither front closed.

The right post-audit posture is:

- **T1**: sharpened, still `PARTIAL DERIVATION 0.85`
- **T2**: sharpened, still `PARTIAL DERIVATION 0.85`
- **T3 / Three Generations**: still `CONDITIONAL 0.85`

The value of the March 31 work is not that it proved the numerator or denominator theorems.
The value is that it moved both gaps from vague convergence language to exact missing lemmas.

---

## Current Truth

### T1 — Physical Realization of `(2,1)`

**Board status**: `PARTIAL DERIVATION 0.85`

What is now closed:

1. `π₁(SO(3)) ≅ ℤ₂` gives a two-class closure-order structure.
2. The natural minimal lifted closure integers are `1` and `2`.
3. The `SU(2)` lift step now survives as a **conditional covering-space result**:
   if a genuine weight-2 mode is physically admitted, it lives on the `SU(2)` lift rather than on `SO(3)` alone.

What is still open:

1. **Extremal principle bridge**  
   Why Axiom 3 selects the candidate Family C functional

   `F_C = I(Phi_int; Phi_ext)`

   as the correct selector for stable branch population.

2. **Strict coherence-deficit bridge**  
   The chain rule gives only

   `F_C^tot >= F_C^(1)`.

   The strict step

   `F_C^tot > F_C^(1)`

   still requires the extra non-redundancy hypothesis

   `A_NR: I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0`.

So the live T1 gap is no longer "why `SU(2)`?".
The live T1 gap is:

> why Axiom 3 forces physical population of the available weight-2 branch.

---

### T2 — Denominator Theorem `M = 3`

**Board status**: `PARTIAL DERIVATION 0.85` — unchanged. v2 companion files submitted for Codex re-audit.

What is now closed conditionally (unchanged from v1):

1. If one grants a local two-band Hermitian Hamiltonian

   `H(k) = h_0(k) I_2 + h(k) · sigma`

   then:
   - the degeneracy condition is `h(k_F) = 0`
   - in `k in ℝ^3`, a generic band-touching point is isolated
   - the co-dimension is `3`
   - the gap-opening perturbation space is `span_R{sigma_1, sigma_2, sigma_3}`
   - that space has dimension `3`

2. The Volovik / `³He-A` analogy is used correctly as a structural template rather than as the proof.

**What v2 companion files added (2026-03-31)**:

1. **PF order-parameter bridge** (`t2_order_parameter_derivation.md`)
   The coherence field `Ψ : ℝ³ × ℝ → ℂ` promoted from bare ansatz to **ARGUED (0.72)** derivation from Axioms 1-3. Complex structure forced by Axiom 2 wave kinematics; nonzero vacuum forced by Axiom 3. Gaps OP-1a/OP-2 named. Includes formal G→H symmetry breaking chain (U(2)→U(1)) in Section 4.5. Status: gap is bounded and named, not closed.

2. **PF → `2×2` Fermi-point Hamiltonian bridge** (`t2_fermi_point_bridge.md` Part A)
   Derived from T1's `ℂ²` state space + Axiom 2's real-energy requirement without importing condensed-matter band structure. The Pauli decomposition is a linear algebra theorem, not a physical import. New named conditionals `C_mom` and `C_FP`: the PF medium must admit a momentum-space description, and Fermi points must exist in the PF weight-2 sector. Status: bridge file remains **ARGUED (0.72)**.

3. **Perturbation-space → bosonic restoration-mode bridge** (`t2_fermi_point_bridge.md` Part B)
   Argued (**0.72**) via the Volovik template: the three Pauli directions are the candidate broken directions counted again by the formal G→H chain in `t2_order_parameter_derivation.md` Section 4.5, but `C_bridge` is still the live hidden step that would turn that count into three independent massive restoration modes. Status: bridge argued (0.72), conditional `C_bridge` named.

4. **Explicit `d = 3` input**
   Unchanged. Named explicitly throughout v2. Still an input, not a PF consequence.

**Live T2 gaps after v2**:

The live T2 gap is now more precisely stated than before:

> 1. **`C_FP`**: Prove that the PF weight-2 propagation sector has Fermi points (band-touching points in 3D momentum space), or find a different T2 route that does not require their existence.
> 2. **`C_bridge`**: Prove from PF axioms alone that each of the three gap-opening Pauli directions at a Fermi point is an independent massive bosonic restoration mode of the PF coherence field — without invoking the Volovik condensed-matter template as justification.

These are sharper than the pre-v2 gaps. The unknowns are now localized enough to attack directly.

---

## T3 Depends On Both

**Three Generations** remains:

> once the numerator theorem and denominator theorem are both granted,
> `Q(N) = 2N / (2N + 3) = 2/3`
> gives `N = 3` uniquely.

That algebra is exact.
The two load-bearing blockers are now explicit:

1. **T1 blocker**: Axiom 3 physical-population bridge for the weight-2 branch
2. **T2 blocker**: PF-to-`2×2` Fermi-point bridge plus restoration-mode identification

So T3 is no longer a vague "topology probably gives 3" claim.
It is a clean conditional statement with two named unresolved denominators.

---

## Correct Next Work

### Track A — Close T1 honestly

Do **not** spend time re-litigating the `SU(2)` lift.
That is no longer the weak point.

The exact T1 targets are:

1. Derive why Axiom 3 selects the Family C extremal principle rather than merely permitting it.
2. Derive `A_NR`, or replace it with a stronger PF-native lemma that yields strict coherence deficit without smuggling.
3. Classify whether partially populated branch configurations are forbidden, metastable, or merely lower-scoring.

### Track B — Close T2 honestly

Do **not** claim `M = 3` just because the local Pauli algebra gives three perturbation directions.

The exact T2 targets remain unchanged from the March 31 audit. v2 companion files (`t2_order_parameter_derivation.md`, `t2_fermi_point_bridge.md`) were submitted to narrow these targets; a Codex review found they added useful narrowing but did not close any of the three bridges. Specifically:

- The order-parameter file had three overclaims (corrected in v2.1, Gap OP-1a and Gap OP-2 named; status revised to ARGUED 0.72)
- Bridge 2 still presupposes translation invariance of the PF medium (new named conditional `C_mom`)
- Bridge 3 renamed the core hidden step as `C_bridge` rather than closing it (status revised to ARGUED 0.72)

The targets remain:

1. Derive the PF order parameter from Axioms 1-3 (promoted from bare ansatz but still ARGUED (0.72) with named gaps OP-1a and OP-2); the formal G→H chain in Section 4.5 organizes the count but does not close the theorem.
2. Derive the local `2×2` Hermitian Fermi-point Hamiltonian from T1 + Axioms 1-3, without assuming translation invariance (`C_mom`) or band-touching point existence (`C_FP`).
3. Prove that the three perturbation directions are the three massive bosonic restoration modes of the PF coherence field (`C_bridge`) — the Section 4.5 symmetry count sharpens this target but does not close it.
4. Keep the `d = 3` dependence explicit until PF derives dimensionality.

See `t2_denominator_theorem.md` Section 13 for all four Codex objections, and `three_generations_t2_proof.md` for the strongest honest current T2 statement.

### Track C — Protect T3 from premature promotion

T3 must stay `CONDITIONAL 0.85` until both tracks close.

Do not promote on the basis of:

- convergence language,
- analogy to `³He`,
- Goldstone counting imported from elsewhere,
- or the emotional fact that `N = 3` is central to the framework.

---

## Acceptance Criteria

### T1 upgrade gate

T1 may upgrade only if:

- the Axiom 3 selector is derived rather than merely proposed,
- the strict coherence-deficit step no longer depends on an external `A_NR`,
- and Codex audit signs off on the physical-population bridge.

### T2 upgrade gate

T2 may upgrade only if:

- the PF order parameter is derived or explicitly justified as an adopted corollary,
- the PF-to-`2×2` Fermi-point Hamiltonian bridge is closed,
- the perturbation directions are proved to be the bosonic restoration modes,
- and Codex audit signs off on the theorem rather than only the conditional lemma.

### T3 upgrade gate

T3 may upgrade only if:

- T1 numerator closure is signed off,
- T2 denominator closure is signed off,
- and the owning docs remain synchronized to the narrower theorem language.

---

## Strongest Honest Summary

After the March 31 work, the framework does **not** yet prove either:

- why PF must physically realize the weight-2 branch, or
- why PF must count exactly three massive restoration modes.

But it now knows the exact missing bridges:

- **T1**: extremal principle + strict non-redundancy
- **T2**: PF coherence dynamics -> `2×2` Fermi-point Hamiltonian -> restoration-mode identification

That is real progress.
The unknowns are now localized enough to attack without lying.
