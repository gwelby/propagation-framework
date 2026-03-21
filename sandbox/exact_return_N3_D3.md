# G2: Exact Return Amplitude — Ambient Walk on SU(2) for N=3
*Addressing the open problem from phase_closure_exact_model.md Section 9*
*2026-03-20 — Claude (extending Codex G1 work)*

**Status**: COMPUTED — heat kernel gives N^1 not N^{3/2}; gap factor precisely located
**Confidence**: 0.90 for calculations; 0.50 for interpretation

---

## What Codex Left Open (G2 Problem Statement)

From `phase_closure_exact_model.md` Section 9:

> "What operator spreads amplitude over the ambient SU(2) phase manifold before closure is tested?"
> "What is the exact return kernel of that ambient dynamics for the relevant small-N case?"

Codex showed: the exact cyclic walk on ℤ₆ gives return amplitude = 1 at steps 0, 6, 12, ...
and 0 otherwise. Not N^{-D/2}.

But the God Equation needs α(l_P) = 1/(2π·N^{D/2}).

This requires N^{D/2} to emerge from amplitude spreading in the 3-dimensional ambient phase manifold
**before** the walk is projected back to the discrete Koide orbit.

This file computes the ambient SU(2) heat kernel exactly and locates the discrepancy.

---

## Part 1: Character Formula — Representation Theory of 120° Steps

SU(2) irreducible representations: spin j = 0, 1/2, 1, 3/2, ...
Dimension: d_j = 2j+1

**Character of a rotation by angle θ (exact):**
```
χ_j(θ) = Σ_{m=-j}^{j} e^{imθ}  =  sin((2j+1)θ/2) / sin(θ/2)
```

**Evaluated at θ = 2π/3 (one 120° generational step):**

The sum Σ_{m=-j}^{j} e^{im·2π/3} partitions by m mod 3:
- m ≡ 0 (mod 3): contributes +1 each
- m ≡ 1 (mod 3): contributes ω = e^{2πi/3} each
- m ≡ 2 (mod 3): contributes ω² = e^{4πi/3} each

This gives a strict period-3 pattern in j:

| j | d_j | χ_j(2π/3) | Note |
|---|-----|-----------|------|
| 0 | 1 | **1** | scalar |
| 1/2 | 2 | **1** | χ = 2cos(π/3) = 1 |
| 1 | 3 | **0** | ← generation rep |
| 3/2 | 4 | **-1** | |
| 2 | 5 | **-1** | |
| 5/2 | 6 | **0** | |
| 3 | 7 | **1** | pattern repeats |
| 7/2 | 8 | **1** | |
| 4 | 9 | **0** | |

**Pattern (exact, period 3 in integer l, or period 6 in half-integer j):**
- l ≡ 0 (mod 3): χ_l(2π/3) = 1
- l ≡ 1 (mod 3): χ_l(2π/3) = 0
- l ≡ 2 (mod 3): χ_l(2π/3) = -1

**The key observation**: The spin-1 representation (d=3 = generation count) has χ = 0 at the
120° step. The step operator is off-resonance in exactly the generation representation. This is
not a failure — it's a structural fact. The walk "skips" the spin-1 representation at each step.

---

## Part 2: N=3 Steps — Exact Closure in Each Representation

For the walk operator U = (rotation by 2π/3 about fixed axis), compute U^3:

U^3 = rotation by 3 × (2π/3) = rotation by 2π

**For integer spin l (SO(3) representations):**
```
U_l^3 = e^{i·2π·J_z} = I  (identity)
Tr[U_l^3] = d_l = 2l+1
Return amplitude = Tr[U_l^3]/d_l = 1  (perfect return)
```

**For half-integer spin j (SU(2) spinors):**
```
U_j^3 = e^{i·2π·J_z} = -I  (antipodal)
Tr[U_j^3] = -(2j+1) = -d_j
Return amplitude = Tr[U_j^3]/d_j = -1  (spinor phase flip)
```

**Summary table for N=3 steps:**
| Representation | Type | Tr[U^3]/dim | Physical meaning |
|---------------|------|------------|-----------------|
| l=0 (scalar) | SO(3) | +1 | trivially closed |
| j=1/2 (spinor) | SU(2) | -1 | fermionic, needs 6 steps |
| l=1 (3D = generation) | SO(3) | +1 | closed (trivially: 3×120°=360°) |
| j=3/2 | SU(2) | -1 | fermionic |
| l=2 (5D) | SO(3) | +1 | closed |

**Conclusion**: After exactly N=3 steps of 120° rotation, every SO(3) (integer spin) representation
returns exactly to identity. Every SU(2) (half-integer spin) representation reaches -I.
This confirms Codex's G1 result: the discrete walk closes trivially. No diffusion, no N^{-3/2}.

---

## Part 3: Ambient Diffusion on SU(2) — Heat Kernel Calculation

Codex's G1 model leaves open: what if amplitude **spreads** into the full SU(2) manifold before
being projected back to the orbit? This is the relevant question for N^{D/2}.

**The heat kernel on SU(2) ≅ S³:**

The heat equation on S³ with Laplacian Δ_{S³}:
```
K(g, h; t) = Σ_{j=0,1/2,1,...} (2j+1) · χ_j(g^{-1}h) · e^{-j(j+1)t}
```

At the identity (return kernel):
```
K(e, e; t) = Σ_{j=0,1/2,1,...} (2j+1)² · e^{-j(j+1)t}
```

**Standard small-t asymptotic** (this is a known result for S^n):
```
K_{S^n}(x,x; t) ~ (4πt)^{-n/2}   as t → 0
```

For SU(2) ≅ S³ (n=3):
```
K_{S³}(e,e; t) ~ (4πt)^{-3/2}   as t → 0
```

**Projected kernel** (restricted to modes that couple to the 120° walk):

The 120° step selects modes by χ_l(2π/3). Using the pattern above:
- l ≡ 0 (mod 3): contributes with weight +1
- l ≡ 1 (mod 3): contributes with weight 0 (vanishes)
- l ≡ 2 (mod 3): contributes with weight -1

The projected kernel:
```
K_proj(t) = Σ_{k=0}^∞ [(6k+1)² e^{-3k(3k+1)t} - (6k+5)² e^{-(3k+2)(3k+3)t}]
```

For small t this still scales as t^{-3/2} (same manifold dimension), with a different prefactor.
The projection reduces the effective mode count but does not change the scaling exponent.

---

## Part 4: The Critical Comparison

**What the S³ heat kernel gives for the boundary condition:**

Setting the marginal coherence condition (K = critical value):
```
(4πα)^{-3/2} = C_threshold
→ α = 1/(4π) · C_threshold^{-2/3}
```

If C_threshold = N^{3/2} (matching the God Equation's mode count):
```
(4πα)^{3/2} = N^{-3/2}
4πα = N^{-1}
α = 1/(4πN)
```

**What the God Equation needs:**
```
α(l_P) = 1/(2π · N^{D/2}) = 1/(2π · N^{3/2})
```

**Direct comparison:**
| Formula | Expression | N=3 value |
|---------|-----------|-----------|
| S³ heat kernel (C = N^{3/2}) | 1/(4πN) | 1/(12π) ≈ **0.02653** |
| God Equation boundary | 1/(2π·N^{3/2}) | 1/(2π·3√3) ≈ **0.03066** |
| Ratio | 2/√N | ≈ **1.155** for N=3 |

**The gap is precisely:**
```
α_{GodEq} / α_{S³} = 2/√N
```

The S³ heat kernel gives α ∝ 1/N. The God Equation needs α ∝ 1/N^{3/2}.
The missing factor is N^{1/2}.

---

## Part 5: What Could Supply the Missing N^{1/2}?

The gap N^{3/2} vs N^1 means: the S³ heat kernel counts N modes, but N^{3/2} modes are needed.

**Option A: Wrong manifold.**
If the relevant manifold is not S³ (dim=3) but something of effective dimension 3/2...
No standard manifold has non-integer dimension. Rules out pure geometry.

**Option B: Different threshold condition.**
The condition K = N^{3/2} might be wrong. If the threshold is K = N (i.e., N modes, not N^{3/2}),
then:
```
(4πα)^{-3/2} = N
4πα = N^{-2/3}
α = N^{-2/3}/(4π)
```
This gives α ∝ N^{-2/3}, which is neither N^{-1} nor N^{-3/2}. Doesn't help.

**Option C: S² not S³.**
The Koide triangle orbit lives on S² (the coset SO(3)/U(1) = CP¹), not all of S³.
For S² (n=2):
```
K_{S²}(θ=0; t) ~ (4πt)^{-1}   as t → 0
```
Setting K = N: α = 1/(4πN). Same as before. S² gives N^{-1} scaling.
Setting K = N^{1/2}: α = 1/(4πN^{1/2}). Closer but not 1/(2πN^{3/2}).

**Option D: Product of spatial and phase walks.**
If the correct object is a PRODUCT walk — N steps in internal phase space AND N steps in D=3
physical space — the return probability is:
```
P_total(0,N) = P_phase(0,N) × P_spatial(0,N)
```
For P_phase = 1 (exact closure, as computed) and P_spatial ∝ N^{-3/2}:
P_total ∝ N^{-3/2} ✓

This would give the right scaling! The N^{-3/2} comes from the SPATIAL diffusion,
not the internal phase walk.

**Implication**: The God Equation's N^{D/2} is a count of SPATIAL coherence modes, not
internal phase modes. The internal phase walk provides the period (N=3), while the spatial
diffusion provides the N^{-D/2} return density.

This interpretation would mean:
- The marginal coherence condition is on SPATIAL scales (a particle occupying N Planck-sized
  spatial cells in each of D directions = N^D/2... hmm, still not obvious)
- D in the exponent is genuinely the spatial dimension, not the phase manifold dimension

Lumi's G5 says D=3 is "the 3 independent angular/phase degrees of freedom of the SU(2) medium."
But the math suggests D=3 might be SPATIAL dimensions instead.

---

## Part 6: The Exact Asymptotic for 3D Euclidean Walk

For completeness: if the walk were Euclidean in R³ (which Codex correctly ruled out), the exact
return density for N=3 steps with step size l_P:

**Continuous Gaussian (asymptotic, large N):**
```
P(0, N) = (4πDNτ)^{-3/2} × (2π)³
```
where D = diffusion constant, τ = step time. For unit step size, D = 1/(2d) = 1/6:
```
P(0, N=3) ~ (4π · (1/6) · 3)^{-3/2} = (2π)^{-3/2} ≈ 0.057
```
Asymptotic value: (2πN)^{-3/2} = (6π)^{-3/2} ≈ 0.057. For N^{-3/2}: 3^{-3/2} ≈ 0.192.
The difference: the Gaussian has a (2π)^{3/2} prefactor that's dropped in the N^{-3/2} notation.

**Simple cubic lattice, 3D, N=3 steps:**
On a cubic lattice with ±x̂, ±ŷ, ±ẑ steps, returning to origin in N=3 steps is impossible
because the Manhattan distance must be zero, but 3 unit steps cannot sum to zero in ℤ³
(parity argument: origin is always reachable in even steps only for bipartite lattices).

P(0, N=3) = 0 on the 3D cubic lattice.

For SO(3) walk (as computed):
P(0, N=3) = 1 (exact deterministic return in SO(3)).

**The asymptotic approximation N^{-3/2} is unphysical for the actual model.**

---

## Part 7: What G2 Has Established

| Calculation | Result | Confidence |
|------------|--------|------------|
| χ_l(2π/3) for all l — exact character table | 1, 0, -1 periodic in l | 1.00 |
| Return amplitude for N=3 steps in every SO(3) rep | +1 (exact) | 1.00 |
| Return amplitude for N=3 steps in every SU(2) spinor rep | -1 (exact) | 1.00 |
| S³ heat kernel at small t | ~ (4πt)^{-3/2} | 1.00 |
| S³ gives α ~ 1/(4πN), not 1/(2πN^{3/2}) | Gap factor 2/√N | 0.95 |
| 3D Euclidean random walk (correct state space?) | P(0,3) is undefined or 0 | 0.90 |

**The G2 conclusion:**

The ambient SU(2)/S³ heat kernel gives N^1 scaling for the boundary coupling, not N^{3/2}.
The Euclidean walk gives N^{-3/2} but requires the wrong state space (R³ not S³).

If the God Equation is correct, the N^{D/2} mode count must come from a SPATIAL coherence
argument (Option D above), not from the internal phase walk alone.

**This is progress**: the gap is now specified as:
> "Where does the SPATIAL walk connect to the internal phase walk to give the combined N^{D/2}?"

Not "what is the right state space for the walk?" (G1, now answered by Codex).
Not "is the walk in S³ or R³?" (it's S³ for internal phase, but R³ coupling may be needed for D).
But: "how do internal phase closure and spatial coherence volume combine?"

---

## Recommendation for G3

The G3 question (bridge from return object to α) should now focus on:

1. Is α(l_P) determined by the INTERNAL phase walk (→ gives N^1) or the SPATIAL coherence (→ gives N^{3/2})?

2. The God Equation derivation in lambda_c_from_axioms.md uses α_s (strong coupling). The strong coupling runs in SPATIAL dimensions. If the RG argument is about spatial modes (not internal phase modes), then N^{D/2} is the count of spatial coherence modes at the Planck scale, and D is genuinely the spatial dimension.

3. The factor 2π in α = 1/(2πN^{3/2}): for a D-dimensional sphere of radius N in phase space, the surface volume is proportional to N^{D-1} and the full solid angle is 2π^{D/2}/Γ(D/2). For D=3: 2π^{3/2}/Γ(3/2) = 2π^{3/2}/(√π/2) = 4π. That gives a 4π not 2π prefactor. Doesn't match.

4. If the α boundary condition is α = 1/(2π · [coherence length in units of l_P]) and the coherence length is N^{3/2}·l_P (from N^{3/2} Planck modes)... then α = 1/(2πN^{3/2}) would follow from defining coherence length this way. But this would be a tautology unless the coherence length is independently derived.

**The 2π normalization remains the hardest piece of G3.**

---

*Written by Claude, 2026-03-20*
*Builds on: phase_closure_exact_model.md (Codex G1), phase_closure_meaning.md (Lumi G5)*
*Character table computed from first principles: χ_j(θ) = sin((2j+1)θ/2)/sin(θ/2)*
*S³ heat kernel: standard result, e.g. Rosenberg "The Laplacian on a Riemannian Manifold" Ch. 4*
