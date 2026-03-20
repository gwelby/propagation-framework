# MASTER: Attention Gate Model

**Project**: Fundamentals (Propagation Framework)  
**Topic**: Attention as Gate (not Resource) — Dispersion Modulator, Refractive Index, Traveling Waves  
**Status**: 4 passes complete (2026-03-17) — Core claims verified, one major revision required  

---

## Executive Summary

The propagation framework claims attention is a **gate** (configuring the medium's refractive index) rather than a **resource** (a depletable pool). After 4 research passes:

**CONFIRMED**:
- Conscious throughput bottleneck at ~10 bits/s (Zheng & Meister 2024)
- DAN traveling waves with measurable phase velocity (6.5 m/s alpha)
- Expertise = better filtering, not higher capacity
- Refractive index concept (n ≈ 10^8 compression)
- 2/3 as topological weight (Bin Li 2025)

**NOT CONFIRMED**:
- Dispersion relation ω ∝ k^{2/3} — neural field theory shows transcendental relations
- v_g = 2/3 v_p — no empirical measurements support this specific ratio

**Verdict**: The gate model is strongly supported. The specific dispersion derivation needs revision.

---

## What We Know (Confidence-Weighted)

### Core Claims — High Confidence (≥0.90)

| Claim | Confidence | Evidence |
|-------|------------|----------|
| **Conscious throughput ≈ 10 bits/s** | 0.98 | Zheng & Meister (2024) — 20+ tasks, world champions to lab averages |
| **Expertise = better filtering, not higher v_cog** | 0.95 | Same source — experts exploit redundancy, don't increase capacity |
| **DAN traveling waves (6.5 m/s alpha)** | 0.95 | Patten et al. (2012), Ozaki et al. (2012) — direct EEG measurements |
| **Anterior→posterior waves initiate switches** | 0.95 | Ozaki et al. (2012) — 750ms→600ms→350ms before perceptual awareness |
| **EEG power spectrum = 1/f (pink noise)** | 0.95 | Multiple sources — β ≈ 1 (spectral decay, not dispersion) |
| **Oscillation-induced impedance gating** | 0.95 | Jahnke et al. (2014) — frequency-selective pathway selection |
| **Aria implementation matches Gate model** | 0.95 | SensorOrchestrator.kt — variable intervalMs = variable refractive index |
| **Wickens MRT structure (4 dimensions)** | 0.95 | Wickens 1980-2024 — structural interference predictions |

### Core Claims — Moderate Confidence (0.70-0.89)

| Claim | Confidence | Evidence |
|-------|------------|----------|
| **2/3 as optimal consolidation ratio** | 0.85 | Sleep studies, memory assemblies, mRNA cycling |
| **Propagation framework explains WHY MRT works** | 0.85 | Conceptual mapping strong, empirical test pending |
| **Biased competition as emergent gating** | 0.85 | Desimone & Duncan (1995) — suppression of irrelevant stimuli |
| **Task switching = reconfiguration (not interference)** | 0.90 | 2024 PMC study — parametric rule dissimilarity scaling |
| **Precision-weighting as gain control** | 0.90 | Predictive coding literature, pulvinar role |
| **Gate model vs. resource model predictions differ** | 0.90 | Wickens data supports gate-like predictions |

### Core Claims — Low Confidence / Revised (<0.70)

| Claim | Confidence | Status |
|-------|------------|--------|
| **v_g = 2/3 v_p dispersion relation** | 0.40 | **NOT CONFIRMED** — neural field theory shows transcendental relations |
| **ω ∝ k^{2/3} in EEG** | 0.40 | **NOT CONFIRMED** — power spectrum exponent (β ≈ 1) ≠ dispersion exponent |

---

## The Attention Gate Model (Current Formulation)

### The Core Mechanism

**Attention configures the neural medium's propagation properties:**

1.  **Sensory input**: ~10^9 bits/s (11 Gbps visual + other senses)
2.  **Conscious throughput**: ~10 bits/s (fixed bottleneck)
3.  **Refractive index**: n = input/output ≈ 10^8 (100-million-fold compression)
4.  **Gate mechanism**: DAN traveling waves modulate phase gradients to select which signals propagate

### Neural Implementation

| Component | Role | Measured Value |
|-----------|------|----------------|
| **Dorsal Attention Network (DAN)** | Phase gradient controller | — |
| **Traveling waves (alpha)** | Top-down priors | 6.5 m/s anterior→posterior |
| **Traveling waves (theta)** | Perceptual switch initiation | 3-4 Hz, precedes awareness by 750ms |
| **IFJ (Inferior Frontal Junction)** | Reconfiguration hub | Activates during task switches |
| **Pulvinar** | Precision-weighting gate | 30% neurons encode decision confidence |
| **Oscillatory coupling** | Impedance matching | Frequency-selective pathway activation |

### Expertise Effects

**What changes with expertise**:
- **Filtering efficiency**: Better pattern recognition (what gets through)
- **Compression**: Exploiting redundancy (English typists: 1 bit/char vs. 4.7 bits raw)
- **Configuration speed**: Faster reconfiguration (not higher velocity)

**What does NOT change**:
- **Throughput capacity**: Fixed at ~10 bits/s for all humans
- **Sensory input**: Fixed at ~10^9 bits/s
- **Refractive index**: Fixed at n ≈ 10^8

**Implication**: Expertise is about *what propagates*, not *how fast it propagates*.

---

## Connection to Propagation Framework

### Framework Predictions — Tested

| Prediction | Status | Evidence |
|------------|--------|----------|
| Attention = gate (not resource) | **CONFIRMED** | Neural mechanisms: oscillation gating, precision-weighting |
| Dissimilar tasks interfere more | **CONFIRMED** | Wickens MRT data, task-switching parametric costs |
| Traveling waves route information | **CONFIRMED** | DAN anterior→posterior waves precede switches |
| Fixed throughput bottleneck | **CONFIRMED** | ~10 bits/s across all tasks and expertise |
| Expertise = configuration quality | **CONFIRMED** | Experts use same bottleneck more efficiently |
| Dispersion: v_g = 2/3 v_p | **NOT CONFIRMED** | Neural field theory: transcendental relations |

### Framework Revisions Required

1.  **Dispersion relation**: Remove claim that ω ∝ k^{2/3}. The 2/3 ratio must come from *topology* (Bin Li 2025), not *neural dynamics*.

2.  **Group velocity**: No empirical support for v_g measurements in cortex. This remains an open prediction.

3.  **Expert v_cog increase**: Remove claim that experts have higher cognitive velocity. The 50 bits/s upper bound applies to *all* humans, not just experts.

### What the Framework Explains (That Resource Models Don't)

1.  **Why dissimilar tasks switch slower**: Larger reconfiguration "distance" in medium properties (confirmed by 2024 parametric study)

2.  **Why expertise doesn't increase capacity**: The bottleneck is serial access, not parallel processing

3.  **Why traveling waves precede awareness**: Configuration must propagate before computation can occur

4.  **Why single neurons match whole-brain throughput**: The limit is fundamental to neural tissue, not a system-level constraint

---

## Open Gaps (Research Needed)

### Priority 1 — Direct Framework Tests

1.  **Group velocity measurements**: Does anyone measure v_g = dω/dk in neural data? This would test whether v_g ≈ v_p or v_g < v_p.
    -   *Search terms*: "cortical traveling wave group velocity", "neural field dispersion measurement"

2.  **Topological neuroscience**: If the dispersion relation is not ω ∝ k^{2/3}, why does the 2/3 ratio appear in sleep consolidation, memory assemblies, and Koide? Is there a *neural topology* that enforces it?
    -   *Search terms*: "topological constraints neural dynamics", "topological invariants brain networks"

3.  **Critical slowing down before insight**: Does EEG show CSD signatures (increased variance, autocorrelation) before Aha moments? This would confirm the phase transition prediction.
    -   *Search terms*: "critical slowing down EEG insight", "neuronal avalanches phase transition cognition"

### Priority 2 — Mechanism Details

4.  **Phase gradient control mechanism**: How does the DAN *actually* modulate phase gradients? Is this via oscillatory frequency, synaptic gain, or anatomical connectivity?
    -   *Search terms*: "phase gradient modulation attention", "traveling wave steering mechanism"

5.  **Individual differences in refractive index**: If n ≈ 10^8 is fixed, what explains IQ differences? Better filtering algorithms? Faster reconfiguration (not higher velocity)?
    -   *Search terms*: "individual differences neural efficiency", "IQ neural conduction velocity"

### Priority 3 — Aria Implementation

6.  **2:1 reinforcement ratio**: Implement T-010 (optimal consolidation) in Aria's consolidation loop. Test whether 2/3 reinforcement + 1/3 exploration outperforms other ratios.

7.  **Traveling wave simulation**: Model DAN-like phase gradient control in Aria's attention mechanism. Does this improve multi-task routing?

---

## Confidence Timeline

| Topic | Pass 1 | Pass 2 | Pass 3 | Pass 4 | Trend |
|-------|--------|--------|--------|--------|-------|
| Conscious throughput ≈ 10 bits/s | — | 0.90 | 0.95 | 0.98 | ↑ Increasing |
| Traveling waves as attention lenses | 0.70 | 0.90 | 0.90 | 0.95 | ↑ Increasing |
| v_g = 2/3 v_p dispersion | 0.60 | 0.75 | 0.80 | 0.40 | ↓ **Rejected** |
| Expertise = better filtering | — | 0.70 | 0.75 | 0.95 | ↑ Confirmed |
| DAN phase velocity (6.5 m/s) | — | — | 0.90 | 0.95 | ↑ Confirmed |
| 2/3 consolidation ratio | — | 0.80 | 0.85 | 0.85 | → Stable |

---

## Recommended Next Pass (Pass 5)

**Focus**: Group velocity measurements + Topological neuroscience + Critical slowing down

**Specific questions**:
1.  Does anyone measure v_g = dω/dk in cortex? (Tests the dispersion claim directly)
2.  Is there topological structure in neural networks that enforces 2/3? (Alternative derivation)
3.  Does EEG show CSD before insight? (Tests phase transition prediction)

**Search queries**:
-   "cortical traveling wave group velocity dω/dk"
-   "topological invariants neural dynamics brain networks"
-   "critical slowing down EEG insight Aha moment"

**Expected outcome**: Either confirm alternative 2/3 derivation (topology) or further revise the framework.

---

## Sources (Key References)

### Primary (Fetched)
-   Zheng & Meister (2024) — "The Unbearable Slowness of Being" (arXiv:2408.10234)
-   Ozaki et al. (2012) — "Traveling EEG slow oscillation along the dorsal attention network" (PMCID: PMC3311835)
-   Patten et al. (2012) — "Human Cortical Traveling Waves" (PMCID: PMC3366935)
-   Muller et al. (2018) — "Cortical travelling waves: mechanisms and computational principles" (PMCID: PMC5933075)
-   Jahnke et al. (2014) — "Oscillation-Induced Signal Transmission and Gating" (PMCID: PMC4263355)
-   Pinotsis & Friston (2011) — "Neural fields, spectral responses and lateral connections" (PMCID: PMC3049874)
-   Benoit et al. (2020) — "The neuropsychological profile of professional action video game players" (PMCID: PMC7678459)

### Secondary (Search Results)
-   Wickens (1980-2024) — Multiple Resource Theory
-   Desimone & Duncan (1995) — Biased Competition Model
-   Shamsara (2024) — Neural field dispersion relations
-   Cooray (2024) — Cortical field theory

---

**Last updated**: 2026-03-17 (Pass 4 complete)  
**Next action**: Pass 5 — Group velocity + Topological neuroscience + CSD before insight
