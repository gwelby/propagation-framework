# CP Violation & Matter/Antimatter Asymmetry — PF Gap Analysis
*Hermes · 2026-07-02 · Research target: what would PF need to explain baryogenesis?*

---

## The Problem

The universe is made of matter. Antimatter is almost entirely absent. The Standard Model cannot explain this — its CP violation is too weak by ~10 orders of magnitude to produce the observed asymmetry. Any fundamental theory must account for it.

**The PF currently does not.** This document maps exactly what's missing.

---

## The Sakharov Conditions (1967)

For baryogenesis to occur, three conditions must be met simultaneously:

| # | Condition | Standard Model Status | PF Status |
|---|-----------|----------------------|-----------|
| 1 | **Baryon number violation** | Non-perturbative (sphalerons) above electroweak scale | ❌ Not addressed |
| 2 | **C and CP violation** | CKM phase in weak interactions — too small by ~10⁻¹⁰ | ⚠️ Threads exist, not derived |
| 3 | **Departure from thermal equilibrium** | Electroweak phase transition (not strongly first-order in SM) | ❌ Not addressed |

---

## What PF Has — Threads Worth Pulling

### Thread 1: N=3 → CP phase → matter survival
*Source: `/mnt/d/fundamentals/RESEARCH/beauty_coherence_empirical/pass_03_synthesis.md` line 23*

> "A minimum of 3 generations is required to support a complex phase in the mixing matrix (CKM/PMNS). This phase allows for CP violation, which is a prerequisite for a matter-dominated universe."

**What this means for PF:** If PF derives N=3 as the unique stable generation count (which it partially does via Z₃/J-I), then it also establishes the *minimum* condition for CP violation. Three generations are necessary for a complex CKM phase. PF has the "why 3" — it doesn't yet have the "why the phase has this value."

**Status:** ARGUED. Not in CLAIMS.md. The connection from N=3 → CP phase exists conceptually but hasn't been formalized.

**What would close it:** Derive the CKM phase magnitude from the same Z₃ structure that forces D=3. Or show that the phase is a free parameter constrained by the medium, with a specific prediction for its value.

### Thread 2: Antimatter as phase-opposite
*Source: `/mnt/d/fundamentals/derivations/matter_pre_dispatch_audit_2026-04-29.md` line 24-25*

> "The file defines antiparticles simply as an opposite phase: Ψ_anti = -Ψ_particle."

**Problem flagged by audit:** "Is defining antimatter purely as a 180° phase shift sufficient to reproduce annihilation physics, or does it violate CPT by oversimplifying Dirac spinor structure?"

**What this means for PF:** The PF's antimatter definition is elegantly simple — opposite phase. But it may be too simple. Full CPT requires charge conjugation + parity inversion + time reversal. A phase flip alone may not capture the full physics of annihilation, CP violation, or the matter/antimatter asymmetry.

**Status:** OPEN. The audit question is unresolved.

**What would close it:** Show that the phase-opposite definition reproduces at minimum the annihilation cross-section and the CPT theorem's consequences. Or replace it with a PF-native definition that captures the full spinor structure.

### Thread 3: Weak force as least-mapped
*Source: `/mnt/d/fundamentals/definitions/forces.md` line 122, 182*

> "PF interpretation (labeled, OPEN): The PF frames weak interactions as mode conversion... It is not a derivation: the PF has not reproduced the V−A interaction, parity violation, CKM structure, or CP violation from PF axioms. The weak force remains the least-mapped force in the framework."

**What this means for PF:** This is the honest baseline. The weak force — where CP violation lives in the Standard Model — is the least-developed part of PF. Mode conversion is a promising frame (down-quark mode → up-quark mode with W emission), but it's a metaphor, not a derivation.

**Status:** OPEN. Explicitly labeled as such in the canonical forces definition.

**What would close it:** Derive V-A structure from PF mode-conversion dynamics. Then derive CKM mixing from mode-coupling in the medium. Then derive the CP-violating phase. Each step is a sub-problem.

### Thread 4: External CKM reconstruction
*Source: `/mnt/d/fundamentals/RESEARCH/koide_generalization/pass_01_survey.md` lines 55, 201*

> "CKM reconstruction: All deviations within 0.7σ of PDG 2024 values." — from a 2025 preprint on quark Koide extension.

**What this means for PF:** Someone else has shown that a Koide-like formula for down-type quarks yields CKM values within 0.7σ. This is external work, not PF-derived. But it suggests the Koide geometry — which PF DOES derive for charged leptons — might extend to quarks and to mixing.

**Status:** External preprint. Not PF-validated. Not in CLAIMS.md.

**What would close it:** Reproduce the external result using PF methods. If PF's equilateral resonance geometry extends to quark mass matrices, CKM mixing may be derivable from the same structure.

---

## The Sakharov Conditions — PF Scorecard

| Condition | PF Has | Missing | Difficulty |
|-----------|--------|---------|------------|
| **Baryon number violation** | Nothing | Entire mechanism. Sphalerons? New physics? PF-native process? | HIGH — requires new physics beyond SM |
| **C and CP violation** | Threads (N=3→phase, mode conversion, external CKM) | Derivation of CP phase magnitude from PF axioms | MEDIUM — threads exist, need formalization |
| **Thermal non-equilibrium** | Nothing | Electroweak phase transition or alternative PF mechanism | HIGH — requires cosmology/phase transition physics |

---

## What's Actionable Now (No Hardware Required)

### Immediate — research consolidation
1. **Pull the beauty_coherence_empirical thread into CLAIMS.md.** The N=3 → CP phase → matter survival chain exists in RESEARCH/ but hasn't been promoted. Add as ARGUED with explicit falsification conditions.
2. **Answer the audit question on antimatter.** Can a 180° phase flip reproduce annihilation + CPT? Yes/no/partial → update matter.md.
3. **Catalog the external CKM preprint.** What's the formula? What are its assumptions? Can PF derive the same thing?

### This week — formalize the gap
4. **Write the CP violation research question** as a formal CLAIM with falsification condition: "PF predicts that the CP-violating phase in the CKM matrix is [value] because [mechanism]." Until the value and mechanism exist, the claim is OPEN.
5. **Define the three Sakharov conditions in PF language.** What would "baryon number violation" look like in a medium-propagation framework? What would "departure from equilibrium" mean when the medium IS the vacuum?

### Next month — connect to existing strengths
6. **Leverage N=3.** PF's strongest card is the generation count. The beauty_coherence thread already connects N=3 to CP phase existence. Formalize this: "Three generations are necessary for a complex CKM phase. PF derives N=3. Therefore PF predicts CP violation is possible." That's not the same as deriving the phase magnitude, but it's a genuine PF prediction: a 2-generation universe cannot have CP violation in mixing.
7. **Leverage the Koide geometry.** If the equilateral resonance that forces Q=2/3 for charged leptons extends to quark mass matrices, CKM mixing may fall out of the same structure.

---

## The Honest Bottom Line

CP violation is the single largest gap in the PF's particle physics coverage. The framework has:
- ✅ A geometric explanation for charged lepton masses (Koide Q=2/3)
- ✅ A candidate explanation for why there are 3 generations (Z₃ stability)
- ❌ No account of why matter survived antimatter
- ❌ No account of the weak force's structure (V-A, CKM, CP phase)
- ⚠️ Threads connecting N=3 to CP phase existence — but not to CP phase magnitude

The path forward exists. It runs through the weak force (mode conversion → V-A → CKM → CP phase) and through the N=3 structure (generations → complex phase → CP violation possible → baryogenesis). But the threads need to be pulled from RESEARCH/ into CLAIMS.md, formalized, and connected.

---

*This document is a research target, not a claim. All statements labeled PF are the framework's own language; all gaps are honest.*
