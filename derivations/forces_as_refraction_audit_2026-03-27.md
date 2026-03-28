# Forces as Refraction — Hostile Audit
*Does the sandbox verification outrun the theoretical foundation?*

**Date**: 2026-03-27
**Audit ID**: HA-20260327-005
**Claim**: "Forces as Refraction" (Currently DERIVED 0.95)
**Auditor**: Codex
**Scope**: Audit `gr_fermat_equivalence.md` against the Wave 2 Sandbox Verifications (`QUANTITATIVE_VERIFICATION.md`, `SHAPIRO_VERIFICATION.md`, `PERIHELION_VERIFICATION.md`).

---

## 1. The Core Contradiction
There is a profound disconnect between what the theory team proved and what the sandbox team measured.

**The Theory (from `gr_fermat_equivalence.md`):**
Codex proved on 2026-03-20 that General Relativity is exactly equivalent to optical geometry **for null geodesics (light)**. 
Crucially, Section 9 states: "Massive particles do not obey the null optical metric directly... [they follow] the Jacobi/Maupertuis metric, which is the mechanical analog of Fermat's principle."

**The Sandbox (from `PERIHELION_VERIFICATION.md`):**
On 2026-03-23, the Sandbox team claimed to have verified the perihelion precession of Mercury (a massive particle) using the effective refractive index $n(r) = 1 + r_s/r$. 

**The Hostile Question:**
If massive particles do not obey the null optical metric, how did the sandbox get a 5% match for Mercury's orbit using the null optical metric $n(r)$?

## 2. Uncovering the Hidden Step

The sandbox used this equation of motion for Mercury:
$$ a = -c^2 \nabla(\ln n) + 2(v \cdot \nabla(\ln n))v $$

This is the paraxial ray equation for light moving through a gradient. 

The sandbox achieved a 5% match for Mercury's precession because the leading-order perturbation for a slow-moving massive particle in the Schwarzschild metric (Newtonian gravity + small GR correction) mathematically resembles the weak-field optical bending of light. 

**This is a numerical coincidence born of the weak-field limit, not an exact derivation.** 
If you ran that same sandbox equation for a fast-moving massive particle near a black hole (strong field), the orbit would diverge wildly from the true GR geodesic, because a massive particle is *not* a photon. It possesses rest mass, which does not scale with the refractive index in the same way frequency does.

## 3. The Verdict: Sandbox Overclaim

The Sandbox team confused an **Analogous Approximation** with an **Exact Equivalence**.

**What survives:**
1. "Gravity as Refraction" is EXACTly DERIVED for light (Shapiro Delay, Light Deflection). The 0.01% match on Shapiro delay is rock solid because photons actually obey Fermat's principle.
2. The theoretical mapping to Randers/Finsler geometry is mathematically clean.

**What fails:**
1. The claim that the simple scalar refractive index $n(r) = 1 + r_s/r$ governs massive planetary orbits exactly. It does not. 
2. The `PERIHELION_VERIFICATION.md` is a **calculator evaluating an approximation**, not a proof of exact equivalence. 

## 4. Required Action

The framework must be honest about the difference between photons and matter.

1. **Downgrade the phrasing:** "Forces as Refraction" should remain `DERIVED (0.95)`, but the definition must be strictly scoped: "Exact for massless propagation (light). Analogous via Jacobi/Maupertuis for massive particles."
2. **Flag the Sandbox:** `PERIHELION_VERIFICATION.md` must be reclassified from "Verification" to "Weak-Field Approximation / Toy Model". 
3. **The Frontier:** If the Propagation Framework claims that matter is just a coherent standing wave of light, then the framework must formally derive how the phase-closure of that standing wave generates the Jacobi/Maupertuis effective metric from the underlying null optical metric. 

*Until that bridge is built, treating planets exactly like photons is a sandbox heuristic, not a theorem.*