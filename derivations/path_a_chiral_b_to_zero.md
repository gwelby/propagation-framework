# Path A: Chiral b→0 Proof Attempt — Sub-targets 1 and 2
*Bounded formal derivation attempt for H_prod via left-chiral ℤ₃ coupling*

**Author**: Codex (derivation) + Claude Sonnet 4.6 (transcription)
**Date**: 2026-04-04
**Status**: BOTH SUB-TARGETS FAIL TO CLOSE — exact obligations named
**Reads**: `sandbox/chiral_projection_z3.py`, `derivations/h_prod_joint_model_obligation.md`
**Truth sources**: `CLAIMS.md`, `ACTIVE_ISSUES.md` (READ ONLY — not edited here)

---

## 0. Summary

| Sub-target | Verdict | Blocker |
|---|---|---|
| 1. Lagrangian forces b→0 via P_L | **DOES NOT CLOSE** | No generation-selective coupling in ℤ₃ Lagrangian |
| 2. Fourier 2D closure → position-space H_prod | **DOES NOT CLOSE** | Position projectors not diagonal in Fourier basis |

Neither sub-target is blocked by a shallow gap. Both require new physics input not currently derivable from the three PF axioms plus the existing ℤ₃-extended Lagrangian.

---

## 1. Setup: What Path A Requires

The goal is to reduce the generation-walk transition operator from

```
T = α·S̄ + β·S̄²    (general circulant, |β/α| = 1 for T_sym)
```

to the pure forward shift

```
T = S̄              (b/a → 0, i.e. β = 0)
```

because `S̄³ = I` (exact), which gives diagonal T³ and trivially satisfies H_prod.

The two proposed routes were:

1. **Lagrangian forcing**: Prove that left-chiral weak coupling on the ℤ₃ Lagrangian
   physically forces `P_L` onto the {k=0, k=1} Fourier sector, eliminating the
   k=2 backward mode and driving β → 0 in position space.

2. **Fourier-to-position bridge**: Even if P_L cannot be formally forced, the projected
   operator T_L has eigenvalues {1, -1/2, 0} and T_L³ is diagonal in the {k=0,k=1}
   Fourier basis. Does this imply position-space factorization for H_prod?

---

## 2. Sub-target 1: Lagrangian Forcing of b→0

### 2.1 The ℤ₃-extended Lagrangian

The relevant Lagrangian (from `z3_extended_propagation_lagrangian.md`) couples three
scalar fields `χⱼ` (j = 0,1,2) via nearest-neighbor circulant coupling:

```
L = Σⱼ [ (1/2)(∂_μ χⱼ)² - (m²/2)χⱼ² - (κ/2)(χⱼ χⱼ₊₁ + χⱼ χⱼ₋₁) ] + interaction terms
```

The free linearized EOM produces the symmetric coupling matrix:

```
M = S̄ + S̄⁻¹  =  S̄ + S̄²
```

so `T_sym = (1/2)M = (1/2)(S̄ + S̄²)` with `t₀=0, t₁=t₂=1/2`.

**Key observation**: This Lagrangian is C₃-symmetric and generation-blind. The coupling
`κ(χⱼ χⱼ₊₁ + χⱼ χⱼ₋₁)` weights forward (S̄) and backward (S̄²) hops identically.

### 2.2 The Chiral Coupling Attempt

The Standard Model weak interaction is left-chiral: only left-handed fermion doublets
couple to SU(2)_L. In the generation-walk picture, this would couple the walk only to
the forward (k=1, phase +2π/3) mode, not the backward (k=2, phase -2π/3) mode.

From `sandbox/chiral_projection_z3.py`, the left-chiral projector is:

```
P_L = P₀ + P₁ = projector onto {k=0 static, k=1 forward} sector
```

**Critical result from the script**: After applying P_L, in position space:

```
T_L = P_L · T_sym · P_L

Fourier decomposition of T_L:
  α = forward S̄ coefficient = 5/12 + i√3/12
  β = backward S̄² coefficient = 5/12 - i√3/12
  |β/α| = 1.000
```

The projector kills the k=2 **eigenmode** but does NOT eliminate the S̄² component
from the position-space matrix. The backward coupling magnitude equals the forward
coupling magnitude in position space after projection.

### 2.3 Why the Lagrangian Cannot Force b→0

The minimal weak source term that would need to be added is generation-selective:

```
L_weak = g_L · W_μ · J_L^μ
```

where `J_L^μ` is the left-handed generation current. For this to force `P_L` onto the
walk and drive β → 0, the current would need to couple selectively to the k=1 mode
(forward propagating) and not the k=2 mode (backward propagating).

**The obstruction**: The weak coupling in the Standard Model acts on generation doublets
`(ν_e, e⁻)`, `(ν_μ, μ⁻)`, `(ν_τ, τ⁻)`. This is not the same as coupling to Fourier
modes of the generation walk. The k=1 and k=2 modes are eigenstates of the S̄ operator
on the ℤ₃ channel space — they are generation-symmetric superpositions, not the
individual generation fermions.

A term that couples to generation j selectively would be of the form:

```
L_select = g_j · χⱼ · W_μ · ψⱼ
```

This is NOT derivable from the current ℤ₃ Lagrangian. It requires an additional
**generation-selective coupling** that distinguishes between channels at the Lagrangian
level. Such a coupling is not implied by Axioms 1–3.

**Verdict on Sub-target 1**: The ℤ₃ Lagrangian with left-chiral weak coupling does NOT
force b/a → 0. The existing coupling is generation-symmetric (C₃-invariant), and the
chiral projector preserves |β/α| = 1 in position space.

**What would close it**: A generation-selective coupling term in the Lagrangian that
distinguishes k=1 (forward) from k=2 (backward) propagation at the level of the action.
This would be a new physical input beyond Axioms 1–3 and the current ℤ₃ structure.

---

## 3. Sub-target 2: Fourier Closure → Position-Space H_prod

### 3.1 What the Projected Sector Gives

From `chiral_projection_z3.py`, the projected operator T_L has:

```
Eigenvalues:  λ₀ = 1  (k=0 sector),  λ₁ = -1/2  (k=1 sector),  λ₂ = 0  (k=2 killed)
```

Therefore:

```
T_L³ eigenvalues:  λ₀³ = 1,  λ₁³ = -1/8,  λ₂³ = 0
```

In the {k=0, k=1} 2D Fourier subspace, T_L³ is diagonal:

```
T_L³|₂D = diag(1, -1/8)   in Fourier eigenbasis
```

### 3.2 Why This Does Not Imply Position-Space H_prod

The position-space channel indicators are:

```
X^(j) = 1 if walk returns to channel j after 3 steps
```

In position space, the basis states are `|0⟩, |1⟩, |2⟩` (the three generation channels).

The Fourier eigenstates are:

```
|k=0⟩ = (1/√3)(|0⟩ + |1⟩ + |2⟩)
|k=1⟩ = (1/√3)(|0⟩ + ω|1⟩ + ω²|2⟩)
|k=2⟩ = (1/√3)(|0⟩ + ω²|1⟩ + ω⁴|2⟩)
```

**The obstruction**: The position projectors `|j⟩⟨j|` are NOT diagonal in the Fourier
basis. Specifically:

```
⟨k=0| j⟩⟨j| |k=0⟩ = 1/3  for all j
⟨k=1| j⟩⟨j| |k=1⟩ = 1/3  for all j
```

So a diagonal T_L³ in the Fourier eigenbasis does NOT imply diagonal matrix elements
`[T_L³]_{jj'}` in the position basis. In fact, from `chiral_projection_z3.py`:

```
T_L³ in full 3D position space:
  diag(T_L³) = 7/24 ≈ 0.2917  (non-trivial, not 1)
  off-diagonal entries ≠ 0
```

So T_L³ is NOT diagonal in position space, and the one-hot closure factorization fails.

### 3.3 The Minimal H_prod Test

Under the one-hot model where X^(j) = 1 iff walk starting in channel j returns to j:

```
P(X^(j) = 1) = [T_L³]_{jj} = 7/24

Product of marginals: P(X^(0)=1) · P(X^(1)=1) · P(X^(2)=1)
                    = (7/24)³ = 343/13824 ≈ 0.0248

P(X^(0)=1, X^(1)=1, X^(2)=1)  [joint, independent starts] 
                    = (7/24)³ ≈ 0.0248    (independent by construction)

But [T_L³]_{jj} = 7/24 ≠ 1, so return probability < 1 for every channel.
The observable is non-trivial but factorization holds only under independent starts.
```

For the single-medium reading: the joint event "all three channels return simultaneously"
requires a joint probability model on one medium. That model is not defined here, and
the Fourier-basis closure structure does not determine it.

**Verdict on Sub-target 2**: Diagonal Fourier-sector closure does NOT propagate to
position-space H_prod. The position projectors are mixtures of Fourier modes, so
diagonal structure in the Fourier basis does not imply diagonal T³ in position space.

---

## 4. The Two Exact Remaining Obligations

### Obligation A — Generation-selective Lagrangian coupling

> Derive a generation-selective weak coupling term in the ℤ₃ Lagrangian that
> couples selectively to the k=1 (forward) Fourier mode and not the k=2 (backward)
> mode, driving β/α → 0 in the IR.

**Status**: Not derivable from Axioms 1–3 + current ℤ₃ Lagrangian.
Requires new physical content identifying *why* the weak interaction distinguishes
forward from backward generation propagation at the Lagrangian level.

**Possible source**: CP violation. If the weak CP phase forces asymmetry between
forward (k=1) and backward (k=2) couplings, this could source the required
generation-selective term. But the formal derivation from CP violation to β/α → 0
is not yet written.

### Obligation B — Fourier-to-position H_prod bridge

> Prove that diagonal T³ in the {k=0, k=1} Fourier sector implies
> P(X^(0), X^(1), X^(2)) = ∏ P(X^(j)) for position-space channel indicators.

**Status**: False for the current projected operator. Fourier diagonal ≠ position diagonal.

**Possible source**: Define the closure observable differently — not in terms of
position-space channel return, but in terms of Fourier-sector occupation. Under such
a definition, factorization would hold by the diagonal structure. But then the
connection to the God Equation's H_prod (which is a statement about generation channel
independence, not Fourier mode independence) must be established separately.

---

## 5. What Path A Needs to Proceed

Path A is not dead. But it requires at least one of:

1. **CP violation drives β/α → 0**: Jarlskog J ≠ 0 is known from experiment. If CP
   violation in the weak sector produces an asymmetric coupling in the ℤ₃ Lagrangian
   that selectively suppresses backward (k=2) mode coupling in the IR, then b/a → 0
   is sourced by observed physics. This is the most promising concrete route.

2. **Alternative closure observable**: Redefine the generation-channel observable in
   terms of Fourier sectors rather than position-space labels. Prove the redefinition
   is physically equivalent to the God Equation's H_prod statement.

3. **A_NR / A_Sel input**: From `t1_non_redundancy_lemma.md`, the non-redundancy axiom
   (A_NR) or selection axiom (A_Sel) might force the medium to populate only forward
   propagating modes. If A_NR selects the forward branch (k=1) as the coherent stable
   mode, then the backward branch (k=2) is unstable and β → 0 naturally.

---

## 6. Honest Status

```
Path A chiral b→0 route:  CONDITIONAL — requires Obligation A or B

Obligation A (generation-selective Lagrangian):
  Most promising source: CP violation (J≠0) → β/α → 0
  Current derivation: NOT WRITTEN
  
Obligation B (Fourier → position H_prod bridge):
  Current status: FALSE for the natural one-hot model
  Possible rescue: redefine observable in Fourier sector basis
  Connection to God Equation H_prod: not yet established

H_prod remains OPEN.
God Equation remains CONDITIONAL 0.88.
```

---

*Derivation by Codex (2026-04-04). Transcribed by Claude Sonnet 4.6.*
*Filesystem write access was unavailable in the Codex sandbox — file written via Claude.*
*No changes to ACTIVE_ISSUES.md or CLAIMS.md.*
