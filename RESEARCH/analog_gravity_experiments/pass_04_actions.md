# Analog Gravity Experiments — PASS 4 Actions

**Date**: 2026-03-16  
**Type**: Targeted Gap Closure  
**Researcher**: Qwen Code  
**Topic**: analog_gravity_experiments  
**Framework Connection**: PROMPT 7 from `deep_research_prompts.md`

---

## Executive Summary

PASS 4 targeted three specific open gaps from PASS 3:
1. **Observational signature of 2nd order renormalization** — Partially resolved; the "dispersive vacuum energy" claim appears to be a conflation of two distinct research threads
2. **Soliton stability and mass ratios beyond Koide** — No specific predictions found beyond the 2/3 derivation
3. **Tilted Dirac Hawking radiation detection** — Confirmed: **No actual radiation detected**; only thermodynamic properties (T + S) calculated theoretically

**Key finding**: The Hubble tension resolution via "dispersion" is not the same as the Del Porro local void model. These are **separate mechanisms** that were incorrectly synthesized in PASS 3.

---

## Gap 1: Observational Signature of 2nd Order Renormalization

### What We Found

**The claim requires correction.** PASS 3 synthesized two distinct research threads:

| Thread | Mechanism | Status |
|--------|-----------|--------|
| **Del Porro + Liberati (2025)** | Local KBC void + gravitational redshift | Published in PRD 112, 4 (2025) |
| **Modified Dispersion Relations** | Adiabatic renormalization with MDR | Theoretical (2007-2024) |

### Thread 1: Del Porro Local Void Model (PRD 2025)

**Paper**: "Alleviating the Hubble tension with a local void and transitions of the absolute magnitude"  
**Authors**: Francesco Del Porro, Stefano Liberati, Jacopo Mazza  
**Journal**: Physical Review D 112, 4 (2025)

**Mechanism**: NOT dispersion-based. The model proposes:
1. We reside inside the KBC void (~300 Mpc radius, ~46% underdensity)
2. Gravitational outflows create Doppler redshift
3. Gravitational redshift from potential hill adds further contribution
4. Combined effect inflates local H₀ measurement

**Redshift formula** (Eq. 5):
$$1+z = \frac{1}{a(t)} \times \sqrt{\frac{c+v_{\mathrm{int}}}{c-v_{\mathrm{int}}}} \times \exp\left(\frac{1}{c^{2}}\int g_{\mathrm{void}}\,dr\right)$$

**Observational Signatures** (confirmed):
- H₀(z) decreases from ~73.5 (local) to ~67 km/s/Mpc (z ≳ 0.2)
- BAO anomaly: α_iso < 1 at low z, converging to 1 at high z
- FRBs should give H₀ ≈ 76-77 km/s/Mpc (tentatively confirmed)
- No Hubble tension at z ≳ 0.3 (lensed SN Refsdal: H₀ = 66±4)

**Connection to Propagation Framework**: Indirect. The void model is a **standard GR solution** with inhomogeneous matter distribution, not a modification of propagation fundamentals.

### Thread 2: Modified Dispersion Relations + Renormalization

**Paper**: "Adiabatic renormalization in theories with modified dispersion relations"  
**Authors**: Various (2007-2024 literature)  
**Status**: Theoretical framework, not observationally tested

**Key claim from literature**:
- Modified dispersion relations (MDR) affect the **divergence structure** of vacuum energy
- Standard QFT in curved spacetime: 4th order divergences (k⁴)
- With certain MDR: 4th order divergences may be suppressed, leaving 2nd order (k²)

**What this means**:
- Standard renormalization: Λ_renorm ∝ Λ_bare + c₁k⁴ + c₂k² + ...
- With MDR: Λ_renorm ∝ Λ_bare + c₂'k² + ... (k⁴ term suppressed)

**Observational Signature** (theoretical):
- Scale-dependent modification to Friedmann equations
- Different expansion history H(z)
- Modified structure growth rate fσ₈

**Critical Gap**: **No specific, unique signature identified** that definitively distinguishes 2nd-order from 4th-order renormalization in current data. The Alicki "Thermal Vacuum Model" (arXiv:2602.08522) proposes H(z) ∝ (1+z)^(3/4) vs (1+z)³, but this is **not directly connected to Del Porro's work**.

### Verdict on Gap 1

**Status**: **PARTIALLY RESOLVED — with correction**

| Sub-Question | Answer | Confidence |
|--------------|--------|------------|
| Is there a "2nd order renormalization" mechanism? | Yes, in MDR literature | 0.7 |
| Does Del Porro's work use this mechanism? | **No** — uses local void model | 0.95 |
| What is the observational signature? | H(z) modification (Alicki model) OR void-induced redshift (Del Porro) — these are **different mechanisms** | 0.8 |
| Does this support Propagation Framework? | Indirectly — both involve modified propagation, but neither is a direct test | 0.6 |

---

## Gap 2: Soliton Stability and Mass Ratios Beyond Koide

### What We Found

**Status**: **NO SPECIFIC PREDICTIONS FOUND**

Extensive search for topological soliton models predicting mass ratios beyond the Koide formula (Q = 2/3) yielded:

1. **Koide formula itself** — Relates e, μ, τ masses only
2. **Quark extension** — R(2, 1/3) ≈ 0.500 (Varma 2026, orbifold CFT)
3. **Neutrino predictions** — Various attempts, none confirmed
4. **Topological soliton literature** — General framework exists, but no specific mass ratio predictions beyond Koide

### Key Sources Examined

| Source | Claim | Status |
|--------|-------|--------|
| arXiv:1201.2067 | Topological approach to particle masses | PDF extraction failed; historical paper (2012) |
| ResearchGate discussion (2026-02-05) | "Geometric explanation for particle mass ratios" | No specific predictions extracted |
| Bin Li 2025 "Chronon Field" | Q_total = 1 law | Derived Koide, no further predictions |

### What Would Count as Evidence

For the Propagation Framework's "topological soliton" claim to make **new predictions**, it would need to:

1. Derive specific mass values (not just ratios) from propagation axioms
2. Predict undiscovered particle masses (e.g., right-handed neutrinos, dark matter candidates)
3. Explain why certain mass ratios are constrained while others are not

**Current status**: The (2,1) topological weight derivation explains **why** Q = 2/3, but does not predict **what** the individual masses are.

### Verdict on Gap 2

**Status**: **OPEN — No specific predictions found in literature**

| Sub-Question | Answer | Confidence |
|--------------|--------|------------|
| Does topological soliton model predict masses beyond Koide? | No confirmed predictions found | 0.8 |
| Does Propagation Framework make such predictions? | Not yet derived — this is a **framework extension opportunity** | 0.9 |
| Is this a critical gap for the framework? | Yes — without specific predictions, the claim remains speculative | 0.85 |

---

## Gap 3: Tilted Dirac Hawking Radiation Detection

### What We Found

**Status**: **CONFIRMED — No actual radiation detected**

The "Smart Holes" paper (arXiv:2412.08517v3, published as JHEP07(2025)226) reports:

### What Was Done

| Achievement | Status |
|-------------|--------|
| **Theoretical calculation of Hawking temperature** | ✓ Complete |
| **Theoretical calculation of Bekenstein-Hawking entropy** | ✓ Complete |
| **Demonstration that tilted Dirac materials match both** | ✓ Complete |
| **Experimental detection of Hawking radiation** | ✗ **Not performed** |
| **Experimental measurement of temperature** | ✗ **Not performed** |

### Material Systems Proposed

| Material | Tilt Mechanism | Status |
|----------|----------------|--------|
| 8Pmmn Borophene | Anisotropic next-nearest-neighbor hopping | Synthesized, tilt tunable via B→C substitution |
| Graphene | Strain, electromagnetic fields, chemical functionalization | Well-characterized, no horizon experiments reported |
| 1T'-MoS₂ | Intrinsic tilt | Available, no horizon experiments |
| Topological insulator surfaces | In-plane magnetic field | Tunable, no horizon experiments |
| LC resonator arrays (bosonic) | Symmetry breaking C₆ᵥ → C₂ᵥ | Proposed, not built for analog gravity |

### Predicted Signatures (Not Yet Measured)

The paper predicts:
1. **Entropy peak at ζ ≈ 1** — Measurable via specific heat
2. **Fermi puddle formation** — Detectable via ARPES or tunneling spectroscopy
3. **Linear S–T scaling** — Testable via calorimetry
4. **Fermi bay → puddle transition** — Observable in Fermi surface mapping

**None of these have been experimentally confirmed as of 2026-03-16.**

### Related Detection: Spin Chain Analogue (Not Tilted Dirac)

A separate experiment (arXiv:2602.04593, IIT Bombay) reported:
- **System**: 72-qubit superconducting processor implementing chiral spin chain
- **Detection**: Quantum sensing via Unruh-DeWitt detector analogue
- **Result**: Radiation spectrum with deviations from Planckian form, Poissonian statistics
- **Significance**: Not reported (no σ value)
- **Material**: **Not tilted Dirac** — different platform entirely

### Verdict on Gap 3

**Status**: **RESOLVED — No detection yet, only theoretical prediction**

| Sub-Question | Answer | Confidence |
|--------------|--------|------------|
| Has Hawking radiation been detected in tilted Dirac materials? | **No** | 0.95 |
| Has thermodynamics (T + S) been experimentally confirmed? | **No** — only theoretically calculated | 0.9 |
| Is detection feasible with current technology? | Proposed signatures are measurable, but no experiment reported | 0.7 |
| Does this affect Propagation Framework? | Minimal — framework predicts refraction-as-force, not specific analog gravity outcomes | 0.8 |

---

## Updated Confidence Scores

| Topic | Previous | Updated | Rationale |
|-------|----------|---------|-----------|
| key_players_identified | 0.95 | 0.95 | No change |
| experimental_platforms_mapped | 1.0 | 1.0 | No change |
| what_demonstrated | 1.0 | 0.95 | Clarified: tilted Dirac = theoretical only, not experimental |
| market_size | 0.4 | 0.4 | No change |
| limitations_understood | 0.95 | 1.0 | Now fully understood: detection ≠ prediction |
| framework_connection | 1.0 | 0.95 | Del Porro work is GR-based, not propagation-based |

---

## New Open Gaps

### High Priority

1. **Is there a unified "dispersive vacuum energy" model?** — The literature shows two separate threads (Del Porro void model vs. MDR renormalization). Are these connected, or was PASS 3's synthesis incorrect?

2. **Can Propagation Framework derive specific mass predictions?** — The (2,1) topological weight explains Koide 2/3, but what predicts m_e = 0.511 MeV specifically?

3. **Will tilted Dirac Hawking radiation be detected?** — Proposed experiments (ARPES, calorimetry, tunneling) are feasible. Who is building them?

### Medium Priority

4. **What is the Alicki Thermal Vacuum Model's relationship to dispersion?** — arXiv:2602.08522 proposes H(z) ∝ (1+z)^(3/4). Is this derived from MDR?

5. **Does the spin chain Hawking radiation detection (IIT Bombay) count as validation?** — Different platform, different detection method — does it support the broader "forces as refraction" claim?

---

## Recommended Next Steps

### For Propagation Framework

1. **Correct the synthesis** — Del Porro's Hubble tension work is **not** dispersion-based renormalization. Update PASS 3's claim or find the correct source.

2. **Derive mass predictions** — Extend the (2,1) topological weight derivation to predict absolute mass scales, not just ratios.

3. **Contact tilted Dirac experimentalists** — The JHEP paper authors may have ongoing experiments. Reach out to ask about detection timelines.

### For PASS 5 Research

1. **Trace the "2nd order renormalization" claim to its source** — Which paper specifically claims dispersion reduces Λ renormalization from 4th to 2nd order?

2. **Search for mass prediction models** — Literature on "particle mass prediction" beyond Koide (e.g., Koide-Brannen, sum rules, orbifold CFT)

3. **Identify experimental groups building tilted Dirac analogues** — Who is attempting ARPES or calorimetry measurements on 8Pmmn borophene with tunable tilt?

---

## Sources

### Key Papers (PASS 4)

- Del Porro, Liberati, Mazza (2025). "Alleviating the Hubble tension with a local void and transitions of the absolute magnitude." *PRD 112, 4*.
- Alicki (2026). "Thermal Vacuum Cosmology Explains Hubble Tension." arXiv:2602.08522.
- Torabian (2025). "Analogue black holes with the right temperature and entropy." *JHEP07(2025)226*.
- Jaiswal, Shankaranarayanan et al. (2026). "Emergent Hawking Radiation and Quantum Sensing in a Quenched Chiral Spin Chain." arXiv:2602.04593.
- García-Pablos et al. (2007). "Adiabatic renormalization in theories with modified dispersion relations." arXiv:gr-qc/0703016.

### Corrected Claims

- **Del Porro's Hubble tension work** = Local void model (gravitational redshift), NOT dispersion-based renormalization
- **Tilted Dirac "Smart Holes"** = Theoretical prediction only, NOT experimental detection
- **2nd order renormalization** = MDR literature, NOT directly connected to Del Porro or Hubble tension data

---

**PASS 4 Complete**. Three targeted gaps addressed:
- Gap 1: Partially resolved (synthesis correction needed)
- Gap 2: Open (no specific predictions found)
- Gap 3: Resolved (no detection yet)

Next pass should trace the "2nd order renormalization" claim to its primary source and search for mass prediction models beyond Koide.
