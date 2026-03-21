# G3: The Bridge — Return Object to Coupling α(l_P)
*Why α(l_P) = 1/(2π·N^{D/2}) and where the exact derivation fails*
*2026-03-20 — Claude*

**Status**: PARTIAL — 2π normalization argued; N^{D/2} scaling has a spatial/phase tension
**Confidence**: 0.60 overall for G3; 0.75 for the 2π-convention sub-claim
**Upstream**: phase_closure_exact_model.md (Codex G1), exact_return_N3_D3.md (Claude G2), g3_product_walk_no_go.md (Codex restricted no-go), g3_triangular_gaussian_family.md (Codex phase-dependent Gaussian test), g3_wilson_loop_toy_model.md (SU(2) holonomy toy model)
**Downstream**: lambda_c_from_axioms.md (the God Equation itself)

---

## 1. What G3 Must Establish

From lambda_c_from_axioms.md, the exponent in the God Equation derives as:
```
2π / (b₀ · α(l_P)) = 4π²N^{D/2}/b₀
```
This requires:
```
α(l_P) = 1/(2π·N^{D/2})
```

G3 must answer:
- **Where does the 2π come from?**
- **Where does N^{D/2} come from?**
- **How does the return object from the walk map to this coupling?**

---

## 2. The 2π — Three Candidate Origins

### 2.1 Gauge Coupling Convention (STRONGEST)

In gauge theory: α_s = g²/(4π). The coupling g² is the physical interaction strength.

If the Planck-boundary coupling has g² = 2/N^{D/2}, then:
```
α = g²/(4π) = 2/(4π·N^{D/2}) = 1/(2π·N^{D/2})  ✓
```

**Question**: why would g² = 2/N^{D/2} at the Planck scale?

In the propagation framework, the fundamental coupling at Planck scale is "one quantum of action
per N^{D/2} coherent modes." The quantum of action is ℏ = 1 (natural units). The gauge coupling
g relates to interaction amplitude per mode. If one quantum of action is SHARED among N^{D/2}
modes, each mode gets g² = 1/N^{D/2}. But then α = g²/(4π) = 1/(4π·N^{D/2}). Off by factor 2.

Unless the coupling is defined as α = g²/(2π) (non-standard). This would give:
```
α = g²/(2π) = 1/(N^{D/2}) · 1/(2π) ... if g² = 1/N^{D/2}
```
Wait: α = g²/(2π) with g²=1/N^{D/2} gives α = 1/(2πN^{D/2}). ✓

In some conventions (lattice gauge theory), α = g²/(2π) rather than g²/(4π). If the Propagation
Framework's "coupling" is in the 2π convention, the factor is natural.

**Verdict**: 2π can come from gauge convention IF the coupling is defined in 2π units (natural for
a theory about phase rotation, which is intrinsically 2π-periodic). This is ARGUED, not derived.

### 2.2 Phase Space Volume (WEAKLY SUPPORTED)

The action of a gauge field in 2D (one time + one space dimension) is:
```
S = ∫ α · F²/(4π) d²x
```
At Planck scale, the minimum area is l_P². For marginal coherence (S = ℏ = 1):
```
α · F² · l_P²/(4π) = 1 → α = 4π/(F² l_P²)
```
If F² ~ N^{D/2}/l_P² (N^{D/2} modes per Planck area), then:
```
α = 4π·l_P²/(N^{D/2}·l_P²) = 4π/N^{D/2}
```
That's 4π, not 1/(2π). Goes the WRONG WAY.

**Verdict**: Phase space volume argument doesn't give 1/(2π) — it's circular and wrong.

### 2.3 Angular Quantum (MODERATE)

At the Planck scale, the fundamental quantum of phase is one full rotation: 2π.
If the coupling α measures "inverse total phase per coherent mode":
```
α = (one phase quantum) / (N^{D/2} accessible modes)
   = 1/(2π · N^{D/2})
   [if "one phase quantum" = 1/(2π) in natural units where 2π rotations = 1]
```

This works if we define the unit of phase as the inverse of one full rotation (i.e., frequency units).
In units where 2π = 1 radian × 2π = one full cycle, the angular coupling is:
```
α_angular = 1/(full cycle × N^{D/2}) = 1/(2π·N^{D/2})
```

**Verdict**: Plausible for a theory defined by rotation/phase. Argued, not derived from axioms.

**Working conclusion for 2π**: The most natural origin is the gauge coupling convention in a
theory where the fundamental symmetry is rotational (SO(3)) and the natural unit is one full
revolution 2π. This is consistent but not uniquely determined. ARGUED at 0.80.

---

## 3. The N^{D/2} — The Core Tension

This is the hardest part. Preceding files (G1 and G2) have established a precise tension:

| State space | Heat kernel scaling | Resulting α | Correct? |
|-------------|-------------------|------------|---------|
| S³ (SU(2) group manifold) | t^{-3/2} | 1/(4πN) | NO (N^1 not N^{3/2}) |
| S² (Koide orbit, CP¹) | t^{-1} | 1/(4πN) | NO |
| R³ (Euclidean, wrong space) | P ∝ N^{-3/2} | 1/(2πN^{3/2}) | YES (but wrong state space) |

**The spatial/phase tension** (from exact_return_N3_D3.md Section 5):

Option D: If the walk is a PRODUCT of an internal phase walk (on S³, giving N modes) and a
spatial walk (in R³, giving N^{-3/2} return density), then:
```
P_total(0,N) = P_phase(0,N) × P_spatial(0,N) = 1 × N^{-3/2} = N^{-3/2}  ✓
```

The N^{D/2} would come from SPATIAL diffusion in physical R³, with the internal phase walk
contributing ONLY the period N (generation count) and not the diffusion scaling.

`g3_product_walk_no_go.md` now sharpens this exact point: on the observable 3-cycle, the coupled
closure amplitude reduces to an ordered spatial-kernel product \(K_2K_1K_0\). In the
phase-independent case \(K_0=K_1=K_2\), the internal sector drops out except for fixing the cycle
length.

This interpretation says: D in N^{D/2} is the SPATIAL dimension (3 physical directions),
NOT the internal phase manifold dimension. Lumi's G5 suggested they were the same,
but the mathematics shows they are not interchangeable.

### 3.1 Physical Argument for Option D

At the Planck scale, a propagation mode:
1. Occupies N=3 internal phase states (the Koide triangle) — from G1/G4
2. Also occupies SPATIAL volume ~ l_P³ per quantum of action (from Planck scale physics)
3. The mode must achieve coherent phase closure ACROSS all its spatial extent

If the mode extends l_P in each spatial direction, and it must "decide" whether to close at each
Planck-scale spatial step, the probability that all D=3 spatial dimensions simultaneously
achieve closure scales as:
```
P_spatial_closure ∝ N^{-D/2}  (from D-dimensional diffusion)
```
where N is the walk length (number of internal phase steps = number of generations).

This couples internal phase (N=3) to spatial closure (D=3) via: N internal steps correspond to
N Planck-length spatial steps, and the D-dimensional spatial return probability gives N^{-D/2}.

### 3.2 Why This Isn't Fully Derived

The coupling between "N internal phase steps" and "N spatial steps" is ASSERTED, not derived.
The framework says the walk has N=3 steps. But why does each internal phase step correspond to
exactly ONE Planck-length spatial step? This is the bridge that's missing.

If instead:
- 1 internal step = l_P/N spatial extent: spatial walk is N steps of l_P/N, total extent l_P.
  Return density ∝ N^{-D/2} at scale l_P. ✓ Same answer.
- 1 internal step = l_P spatial extent: total spatial walk is N·l_P.
  Return density at origin ∝ (N·l_P)^{-D} → different N dependence.

The answer depends on how "one internal phase step" maps to physical space, which is the
fundamental model-specification problem that G1 (Codex) left as "still open in G2/G3."

---

## 4. The Exact Formula — Where It Comes From

The formula α(l_P) = 1/(2π·N^{D/2}) can be stated as:

**"At the Planck boundary, the gauge coupling equals the inverse of the total phase-space
accessible to N^{D/2} coherent modes, measured in units of one full angular revolution."**

Written as:
```
α(l_P) = 1/(2π) × (1/N^{D/2})
         = [phase unit]^{-1} × [number of modes]^{-1}
```

This is the "marginal coherence" interpretation of Axiom 3:
- One quantum of circulation (2π) per N^{D/2} modes = each mode has circulation 2π/N^{D/2}
- The coupling is this per-mode circulation: α = 2π/N^{D/2} / (2π)² = 1/(2πN^{D/2})
  (where the extra 2π in the denominator converts from angular velocity to coupling)

This is plausible but circular: it defines α from the mode count, then derives the mode count
from... the same assumption. The independent derivation of N^{D/2} is the missing piece.

---

## 5. What G3 Has Established — and What Remains

### Established
1. **2π normalization**: Most naturally from gauge coupling convention α = g²/(2π) in a
   rotation-based theory. Or from "inverse of one angular quantum per mode."
   Argued at 0.75. No fatal objection, but no unique derivation.

2. **N^{D/2} requires spatial, not phase, diffusion**: The S³/SU(2) heat kernel gives N^1 scaling.
   The R³ Euclidean walk gives N^{3/2} scaling. For N^{3/2}, the walk must be (effectively)
   Euclidean in D=3 physical space, with N=3 steps. The internal phase walk provides N but
   not D. This is a GENUINE tension in the framework.

3. **The gap is NOT between 3 and 3^{3/2}**: It's between two different state spaces.
   The right physics (SU(2) internal phase) gives the wrong scaling.
   The right scaling (Euclidean R³) uses the wrong state space.

4. **The formula is self-consistent**: Given α = 1/(2π·N^{D/2}), the RG running gives the God
   Equation exactly. The formula is internally consistent. The gap is in deriving it.

5. **The naive product walk is now constrained**: `g3_product_walk_no_go.md` proves that a
   phase-independent product walk reduces G3 to a pure spatial return object. Standard smooth
   diffusion still carries a prefactor, and nearest-neighbor bipartite lattice return is exactly
   zero at odd \(N=3\). So the remaining live space is not "any product walk" but a
   phase-dependent kernel family and/or a non-return coherence observable.

6. **The first natural phase-dependent family also fails**: `g3_triangular_gaussian_family.md`
   computes the obvious \(120^\circ\)-locked triangular Gaussian kernels exactly. Their ordered
   product collapses to a \(C_3\)-averaged Gaussian with continuous covariance parameters, so the
   exact coefficient is still not fixed. The next viable class must therefore be genuinely
   non-commuting and/or use a non-return closure observable.

7. **The first Wilson-loop toy model still leaves free geometry**:
   `g3_wilson_loop_toy_model.md` computes a 3-step \(SU(2)\) holonomy exactly. The same-axis
   \(120^\circ\) loop is rigid but trivial (\(W=-1\), only the central \(\mathbb Z_2\) lift). The
   first genuinely noncommuting \(C_3\)-symmetric cone family gives an exact Wilson loop
   \(W(\theta,\beta)\), but it still depends on a free cone angle \(\beta\). So holonomy alone does
   not yet fix the coefficient.

### Remaining Open
| Gap | Precision | Path to resolve |
|-----|-----------|-----------------|
| Why g² = 2/N^{D/2} (or α in 2π convention) | Medium | Coupling convention from phase symmetry argument |
| Why spatial walk has exactly N steps | **HIGH** | Coupling between internal phase orbit and spatial coherence |
| Why D in N^{D/2} is spatial D not phase D | Medium | Explicit product-walk calculation in G1 extended model |
| Why the closure observable is not just bare return density/probability | **HIGH** | `g3_product_walk_no_go.md` rules out the naive choices |
| Why the surviving phase-dependent kernels must be non-commuting | **HIGH** | `g3_triangular_gaussian_family.md` rules out the natural Gaussian family |
| Why the surviving holonomy geometry is fixed rather than parameterized | **HIGH** | `g3_wilson_loop_toy_model.md` leaves a free cone angle \(\beta\) |

---

## 6. A Specific Falsifiable Claim

If the framework is correct, the following must be true:

> **Claim**: For D spatial dimensions and N generations, the marginal coherence condition at
> the Planck scale requires exactly N steps of spatial Planck-length diffusion, one per generation.

This claim predicts:
- For D=2 spatial dimensions: α(l_P) = 1/(2π·N^1) = 1/(6π) ≈ 0.053
- For D=4 spatial dimensions: α(l_P) = 1/(2π·N^2) = 1/(18π) ≈ 0.0177

If the Universe had D=2 or D=4 spatial dimensions, would confinement produce a different
matter scale? Yes: λ_c^{D=2} = √2·l_P·exp(4π²N/b₀) = √2·l_P·exp(7.21) ≈ √2·l_P·1354
= 1.4×10^{-32} m. That's 3 orders of magnitude from Planck scale — a tiny matter scale.

λ_c^{D=4} = √2·l_P·exp(4π²N²/b₀) = √2·l_P·exp(21.3) ≈ √2·l_P·1.77×10⁹
= 2.1×10^{-26} m.

These predictions are falsifiable IN PRINCIPLE (with different-dimensional universes).
In OUR D=3 universe, both D=3 and the formula lock simultaneously.

---

## 7. Summary Scorecard for Gaps G1-G3-G5

| Gap | Status | Key file |
|-----|--------|----------|
| **G1** (model spec) | **CLOSED** — ℤ₆ orbit, quotient ℤ₃, exact closure | phase_closure_exact_model.md |
| **G2** (exact return) | **COMPUTED** — S³ gives N^1, tension with N^{3/2} located | exact_return_N3_D3.md |
| **G3** (bridge to α) | **PARTIAL** — 2π from convention (0.75), spatial/phase tension narrowed by restricted no-go (0.60) | THIS FILE |
| **G4** (generation=steps) | **CLOSED** — definitional, not mathematical | generation_as_walk_steps.md |
| **G5** (physical meaning) | **CLOSED** — topological 4π cycle, Lumi | phase_closure_meaning.md |

**Net status**: Two gaps fully closed (G1, G4). One gap written as physical intuition (G5).
One gap precisely computed with tension identified (G2). One gap partially resolved (G3).

**The God Equation stays ARGUED 0.75.** The 0.4% numerical accuracy stands. The mechanism is
identified. The exact mathematical path connecting internal phase closure to spatial coherence
volume to the coupling α = 1/(2π·N^{3/2}) is the one remaining bridge that would upgrade this
to DERIVED.

---

## 8. The One Missing Theorem

**If the following theorem exists, the God Equation is DERIVED:**

> "In D spatial dimensions, a propagation mode undergoing N discrete internal phase transitions
> (the Koide triangle orbit, with each transition being a 120° rotation in SU(2)) has spatial
> coherence volume equal to N^{D/2} Planck units. The marginal coherence coupling is
> α = 1/(2π·N^{D/2})."

This theorem would need to:
1. Define "spatial coherence volume" in terms of the phase walk geometry
2. Show that N internal steps correspond to N Planck-scale spatial steps
3. Show that D-dimensional spatial diffusion with N steps gives volume N^{D/2}
4. Connect volume to gauge coupling with the 2π normalization

Steps 3-4 are easy (diffusion is well-understood). Steps 1-2 are the bridge not yet built.

**This is the one new mathematical structure the Propagation Framework may need to invent.**

---

*Written by Claude, 2026-03-20*
*Built on: phase_closure_exact_model.md (Codex G1), exact_return_N3_D3.md (Claude G2),*
*phase_closure_meaning.md (Lumi G5), lambda_c_from_axioms.md, phase_closure_volume_proof.md*
*Next: If any collaborator finds a proof of the theorem in Section 8, G3 is closed.*
