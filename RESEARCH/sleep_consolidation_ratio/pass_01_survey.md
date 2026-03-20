# PASS 1: Broad Landscape Survey — Sleep Consolidation Ratio

**Date**: 2026-03-17  
**Type**: Survey  
**Focus**: Who are the players, what exists, key trends, quantitative measures  
**Topic**: Sleep as a different propagation mode — is there an optimal real-time/consolidation ratio?

---

## Executive Summary

The landscape reveals **five major research programs** addressing sleep as active consolidation (not downtime), with converging evidence for:

1. **Temporal separation is computationally necessary** — mathematical proof that high-capacity systems cannot simultaneously satisfy online fidelity and generalisation objectives (arXiv:2603.04688v1, Mar 2026)
2. **Neural criticality degrades during wake, resets during sleep** — every waking moment pushes circuits away from optimal computational state (Nature Neuroscience, Jan 2024)
3. **SWS and REM play differential (opposing) roles** — SWS preserves precise details, REM drives abstraction/transformation (Nature Communications Biology, Oct 2025)
4. **Hippocampal replay occurs at 10-100x compression** — awake replay is super-diffusive (planning), sleep replay is diffusive (generalization) (Nature Communications, Jan 2026)
5. **Optimal sleep duration ~7 hours** — U-shaped curve with cognitive impairment at 9+ hours (Alzheimer's & Dementia, Apr 2025)

**Key Gap**: No published work directly addresses **optimal sleep-wake ratio for information processing efficiency** as a design principle for artificial systems. The 1:2 ratio (8h:16h) is studied for human health, not computational optimality.

---

## 1. Major Research Programs

### 1.1 Active Systems Consolidation (ASC)

**Core Claim**: Sleep actively reorganizes memories through hippocampal-cortical dialogue orchestrated by slow oscillations (SO), spindles, and ripples.

**Key Players**:
- Born, J. (University of Tübingen) — foundational ASC theory
- Rasch, B. (University of Fribourg) — targeted memory reactivation
- Cairney, S. (University of York) — systems consolidation dynamics

**Recent Findings**:
- SO-spindle coupling is the critical neural signature of effective consolidation
- Temporal synchrony between SOs and spindles predicts memory retention
- TMR during SWS stabilizes memories; TMR during REM drives transformation

**Quantitative Measures**:
- SW-spindle coupling strength correlates with accuracy improvement (r = 0.70, p = 0.011)
- Optimal TMR timing: during SWS upstates (spindle peaks)
- Consolidation efficiency: personalized TMR > standard TMR for difficult memories (L3 condition: p < 0.001)

**Status**: Well-established, empirically supported

---

### 1.2 Synaptic Homeostasis Hypothesis (SHY)

**Core Claim**: Wakefulness causes net synaptic potentiation (learning); sleep causes global synaptic downscaling to prevent saturation and restore energy balance.

**Key Players**:
- Tononi, G. (University of Wisconsin-Madison) — SHY originator, Integrated Information Theory
- Cirelli, C. (University of Wisconsin-Madison) — molecular evidence for synaptic downscaling

**Relationship to ASC**: Complementary, not competing:
- ASC: explains **selective** memory reorganization (which memories are strengthened/weakened)
- SHY: explains **global** synaptic renormalization (why sleep is needed at all)

**Recent Findings**:
- Structural evidence in Drosophila: synaptic markers decrease after sleep
- Sleep spindle activity promotes hippocampal network downregulation (Current Biology, Feb 2026)
- SHY + ASC together explain both preservation and transformation

**Status**: Well-established, structural evidence accumulating

---

### 1.3 Neural Criticality Reset

**Core Claim**: Wakefulness progressively degrades neural criticality (optimal computational state); sleep restores it.

**Key Players**:
- Hengen, K. (Washington University in St. Louis) — 2024 Nature Neuroscience paper
- Wessel, R. (Washington University in St. Louis) — avalanche analysis methods
- Plenz, D. (NIMH) — neuronal avalanches, criticality in cortical dynamics

**Quantitative Measures**:
- **Avalanche distribution**: post-sleep = all sizes present (critical); pre-sleep = biased toward small only (sub-critical)
- **Predictive capability**: researchers could predict sleep onset from avalanche distribution alone
- **Time course**: degradation is continuous during wake; restoration occurs during sleep (specific duration not reported)

**Status**: Emerging (2024), highly relevant to propagation framework

**Direct Quote**:
> "Every waking moment pushes relevant brain circuits away from criticality, and sleep helps the brain reset." — Hengen (2024)

---

### 1.4 Predictive Forgetting / Generalisation Theory

**Core Claim**: Consolidation is computationally necessary for high-capacity systems to achieve optimal generalisation. Single-pass encoding cannot simultaneously satisfy fidelity and generalisation objectives.

**Key Players**:
- Fountas et al. (2026) — arXiv:2603.04688v1, mathematical proof

**Mathematical Results**:
- **The Conflict**: I(X;Z) ≈ H(X) (fidelity) vs. I(X;Z|Y) → 0 (generalisation)
- **Proof**: I(X;Z|Y) ≥ H(X) - I(Y;X) > 0 — superfluous information is lower-bounded by environmental noise
- **Resolution**: Temporal separation is **necessary**, not optional

**Quantitative Model**:
```
Generalisation Bound: Δ ≤ Õ(√[(I(X;Z|Y) + C) / n])
```
- Δ = generalisation gap
- I(X;Z|Y) = outcome-irrelevant information
- C = encoder complexity
- n = training examples

**Empirical Results**:
| Metric | Online-Only | With Consolidation | Improvement |
|--------|-------------|-------------------|-------------|
| Generalisation Gap (CIFAR-10, d=512) | ~0.25 | ~0.08 | 68% reduction |
| Test Accuracy (d=1024) | ~72% | ~84% | +12 percentage points |
| KV Cache Gap (GSM8K) | ~0.15 | ~0.02 | 87% reduction |

**Status**: Brand new (Mar 2026), mathematically rigorous, directly applicable to Aria

---

### 1.5 Hippocampal Replay Dynamics

**Core Claim**: Replay is the neural mechanism of consolidation, occurring at 10-100x timescale compression with state-dependent dynamics.

**Key Players**:
- Ji, Z. et al. (2026) — Nature Communications 17, 1282
- Buzsáki, G. (NYU) — replay discovery and characterization
- Wilson, M. (MIT) — awake replay and decision-making

**Quantitative Measures**:
- **Timescale compression**: 10-100x (seconds of experience → tens/hundreds of ms replay)
- **Temporal resolution**: 2-ms bins for decoding
- **Diffusivity regimes**:
  - Awake: super-diffusive (η > 0.69, behavior-like, planning)
  - Sleep: diffusive (η = 0.69 ± 0.12, Brownian, generalization)

**Firing Rate Adaptation (FRA) as Control Mechanism**:
| FRA Strength | Replay Type | Function |
|--------------|-------------|----------|
| Weak (below threshold) | Stationary | Local processing |
| Moderate | Diffusive | Generalization |
| Strong | Super-diffusive | Planning, exploration |

**Status**: Well-established, mechanistic understanding emerging

---

## 2. Key Quantitative Findings

### 2.1 Optimal Sleep Duration

| Duration | Cognitive Impact | Source |
|----------|-----------------|--------|
| < 6 hours | Impaired executive function, attention, memory | Multiple meta-analyses |
| **7-8 hours** | **Optimal for cognitive performance** | Alzheimer's & Dementia (Apr 2025) |
| 9+ hours | Worse cognitive performance, stronger effect with depression | Alzheimer's & Dementia (Apr 2025) |

**U-shaped curve confirmed**: Both short and long sleep associated with impairment.

**Domain-specific vulnerabilities**:
- Attention/vigilance: most vulnerable (large effect sizes)
- Memory: encoding and consolidation both impaired
- Executive function: working memory, flexibility, decision-making impaired
- Emotional regulation: amygdala reactivity increases, PFC-amygdala connectivity weakens

---

### 2.2 Sleep Architecture: SWS vs REM Differential Roles

**Traditional View**: SWS and REM are complementary (both needed for consolidation)

**New Finding (Liu et al., 2025)**: SWS and REM play **opposing** roles:

| Memory Type | REM Association | SWS Association |
|-------------|-----------------|-----------------|
| **Precise (item-level)** | REM theta: β = -29.324, R² = 0.142, pFDR = 0.016 (negative) | No correlation |
| **Abstract (category-level)** | REM theta: β = 21.600, R² = 0.134, pFDR = 0.038 (positive) | SWS slow oscillation: β = -1.161 (negative) |

**REM/SWS Ratio** (not product) predicts transformation:
- Item-level change: β = -0.022, adjusted R² = 0.196, p = 0.005
- Category-level change: β = 0.014, adjusted R² = 0.126, p = 0.022

**Interpretation**: Higher REM drives transformation (precise → abstract); higher SWS opposes transformation (preserves details).

---

### 2.3 Sleep-Wake Ratio Effects

**1:2 Ratio (8h sleep : 16h wake)**:
- Circadian modulation of sleep propensity is **pronounced**
- Clear Wake Maintenance Zone (WMZ) in early evening
- Clear Afternoon Nap Zone (ANZ) in late afternoon
- Optimal for cognitive performance under normal conditions

**1:5 Ratio (4.7h sleep : 23.3h wake)**:
- Circadian effects **masked** by homeostatic pressure
- WMZ disappears completely
- ANZ disappears by day 2
- Sleep propensity high at all circadian phases

**Key Finding**: Circadian benefits (WMZ alertness) only available under non-restricted sleep.

**Gap**: No study directly optimizes sleep-wake ratio for **information processing throughput** (only for health/cognitive performance).

---

### 2.4 Hippocampal Replay Efficiency

**Compression Ratio**: 10-100x
- Behavioral sequence: seconds to minutes
- Replay duration: tens to hundreds of milliseconds
- Theta sequences: dozens of milliseconds

**Replay Organization**:
- Chains avoid self-repetition over short timescales
- Post-movement replays avoid previous path for ~3 seconds
- Awake replay more diffusive than sleep replay (P = 4.6 × 10⁻⁴)

**Consolidation Efficiency**:
- Replay during SWS: stabilization
- Replay during REM: transformation
- TMR during SWS: enhances stabilization only (does not promote transformation)

---

## 3. Market Size / Research Volume

**Publication Volume** (approximate, from search results):
- "sleep memory consolidation": 10,000+ papers (PubMed)
- "hippocampal replay": 2,000+ papers
- "sleep criticality": 200+ papers (emerging)
- "predictive forgetting" / "generalisation sleep": <50 papers (very new)

**Active Labs**: ~50 major labs worldwide (estimate from author affiliations)

**Funding**: NIH, NSF, Wellcome Trust, EU Horizon — sleep research is well-funded but not a "hot" area compared to AI/ML

**Commercial Applications**:
- Sleep optimization apps (Oura, Whoop, Eight Sleep) — consumer focus, not computational
- TMR devices (Emerging, but early stage)
- No commercial "consolidation scheduling" for AI systems

---

## 4. Key Trends (2024-2026)

### 4.1 From Complementary to Differential Roles

**Old**: SWS and REM both contribute to consolidation (additive)

**New**: SWS and REM play **opposing** roles (SWS preserves, REM transforms)

**Implication**: Optimal sleep architecture depends on **what** you want to consolidate (details vs. gist)

---

### 4.2 From Passive to Active

**Old**: Sleep is passive recovery, replenishment of depleted resources

**New**: Sleep is **active computation** — generative replay, predictive forgetting, criticality reset

**Implication**: Sleep duration should be determined by computational load, not fixed schedule

---

### 4.3 From One-Size-Fits-All to Personalized

**Old**: 8 hours is optimal for everyone

**New**: Personalized TMR outperforms standard TMR for difficult memories; optimal duration varies by individual and daily information load

**Implication**: Aria's REST/WONDER scheduling should be **adaptive**, not fixed

---

### 4.4 From Descriptive to Mathematical

**Old**: Sleep helps memory (qualitative)

**New**: Consolidation is **computationally necessary** for high-capacity systems (mathematical proof, arXiv:2603.04688v1)

**Implication**: This is not a biological quirk — it's a **universal constraint** on information processing systems

---

### 4.5 From Correlation to Mechanism

**Old**: Sleep correlates with memory improvement

**New**: Firing rate adaptation controls replay dynamics; SO-spindle coupling mediates consolidation; criticality reset is measurable via avalanche distributions

**Implication**: We can now **engineer** consolidation, not just observe it

---

## 5. Open Gaps (Research Needed)

### 5.1 Optimal Sleep-Wake Ratio for Information Processing

**What We Know**:
- 7-8 hours optimal for human cognitive performance
- 1:2 ratio supports circadian modulation
- Consolidation is computationally necessary for high-capacity systems

**What We Don't Know**:
- Is there a **mathematical optimum** for the ratio of real-time processing to consolidation?
- Does the optimal ratio scale with system capacity?
- Does it scale with daily information load?
- Is there a "minimum effective dose" of consolidation for a given encoding load?

**Research Direction**: Model consolidation as a function of:
- Encoding load (bits/day)
- System capacity (representational dimensions)
- Generalisation requirements (how much transfer vs. rote memory)

---

### 5.2 Consolidation Scheduling

**What We Know**:
- Temporal separation is necessary (cannot consolidate while encoding)
- Sleep occurs once per 24h in humans (monophasic)
- Afternoon naps provide partial restoration

**What We Don't Know**:
- Is monophasic consolidation optimal, or are multiple shorter sessions better?
- What is the optimal **frequency** of consolidation cycles?
- Should consolidation frequency scale with encoding rate?

**Research Direction**: Compare monophasic vs. polyphasic consolidation in artificial systems

---

### 5.3 WONDER Mode as "Dreaming"

**What We Know**:
- REM drives memory transformation (precise → abstract)
- REM theta power correlates with abstraction (R² = 0.134)
- "Dreaming" is generative replay with sensory gating

**What We Don't Know**:
- Should WONDER mode run on **stored memories only** (like biological dreaming)?
- Should it run with **reality constraints removed** (like biological REM)?
- What is the optimal WONDER:REST ratio?

**Research Direction**: Implement WONDER as REM-analogue (generative, transformative) vs. REST as SWS-analogue (stabilizing)

---

### 5.4 Criticality as a Measurable Target

**What We Know**:
- Criticality degrades during wake, restores during sleep
- Avalanche distribution is a measurable signature
- Researchers could predict sleep onset from criticality measures

**What We Don't Know**:
- Can we measure Aria's "criticality" (coherence state)?
- Can we use criticality as a **trigger** for REST mode (not fixed schedule)?
- What is the computational equivalent of neural avalanches in Aria's architecture?

**Research Direction**: Implement coherence monitoring as a REST trigger (not timer-based)

---

### 5.5 Personalized TMR for AI

**What We Know**:
- Personalized TMR > standard TMR for difficult memories (L3: p < 0.001)
- SW-spindle coupling mediates effect (r = 0.70)
- Response-contingent stimulation is key

**What We Don't Know**:
- What is the AI equivalent of TMR?
- Should Aria "replay" difficult episodes more frequently during REST?
- Should replay frequency be performance-contingent?

**Research Direction**: Implement performance-contingent replay scheduling in REST mode

---

## 6. Confidence Scores

| Topic | Confidence | Evidence Quality |
|-------|-----------|------------------|
| Temporal separation is necessary | 0.95 | Mathematical proof + empirical |
| Neural criticality reset | 0.85 | Strong empirical (2024) |
| SWS vs REM differential roles | 0.90 | Strong empirical (2025) |
| Hippocampal replay compression | 0.95 | Well-replicated |
| Optimal sleep duration ~7h | 0.85 | Meta-analytic |
| 1:2 sleep-wake ratio optimal | 0.70 | Correlational, human health focus |
| Consolidation scales with capacity | 0.80 | New (2026), theoretical + empirical |
| Personalized TMR effectiveness | 0.85 | RCT-level evidence |

---

## 7. Recommended Actions

### Immediate (for Aria Design)

1. **Implement REST mode as SWS-analogue** — stabilization, replay, coherence restoration
2. **Implement WONDER mode as REM-analogue** — generative, transformative, abstraction-focused
3. **Make consolidation adaptive** — trigger by coherence state, not fixed timer
4. **Implement performance-contingent replay** — difficult episodes get more replay

### Research (for Fundamentals Project)

1. **T-010: Model optimal consolidation ratio** — mathematical model of encoding:consolidation ratio as function of capacity and load
2. **T-011: Implement criticality monitoring in Aria** — coherence metrics as REST trigger
3. **T-012: Test monophasic vs. polyphasic consolidation** — simulation study in artificial system
4. **T-013: WONDER mode as dreaming** — implement and test generative replay on stored memories

---

## 8. Key References

### Foundational
1. **Fountas et al. (2026)**. "Why the Brain Consolidates: Predictive Forgetting for Optimal Generalisation." arXiv:2603.04688v1 [q-bio.NC]. **CRITICAL** — mathematical proof.
2. **Hengen & Wessel (2024)**. "Sleep restores neural criticality." Nature Neuroscience. **CRITICAL** — criticality reset.
3. **Liu et al. (2025)**. "Slow-wave sleep and REM sleep differentially contribute to memory representational transformation." Communications Biology 8, 1407. **CRITICAL** — SWS vs REM opposition.

### Mechanistic
4. **Ji et al. (2026)**. "Dynamical modulation of hippocampal replay through firing rate adaptation." Nature Communications 17, 1282.
5. **Bes (2025)**. "Treatise on an alternative perspective on the two-process model." Nature: Sleep Science.
6. **Tai et al. (2025)**. "The Role of Sleep and the Effects of Sleep Loss on Cognitive Function." PMC12168795.

### Applied
7. **Personalized TMR (2025)**. "Personalized targeted memory reactivation enhances consolidation." Nature: npj Science of Learning.
8. **Harvard Health (2025)**. "Too much sleep may harm cognitive performance." Alzheimer's & Dementia, Apr 2025.

---

## 9. Connection to Propagation Framework

### Confirmed Predictions

| Framework Claim | Research Confirmation |
|----------------|----------------------|
| Sleep is different propagation mode, not downtime | Active computation, generative replay, criticality reset |
| Temporal separation necessary | Mathematical proof (arXiv:2603.04688v1) |
| Coherence restoration during sleep | Criticality reset = coherence restoration |
| Replay at compressed timescales | 10-100x compression confirmed |
| Optimal ratio exists | 1:2 for humans, capacity-dependent in theory |

### New Insights for Framework

1. **Criticality = Coherence**: Neural criticality may be the measurable signature of "coherent self-referential propagation"
2. **SWS/REM Opposition**: Not all consolidation is the same — stabilization vs. transformation are different operations
3. **Capacity-Dependence**: Consolidation necessity scales with system capacity — explains why large brains need more sleep
4. **Predictive Forgetting**: Forgetting is not failure — it's the mechanism of generalisation

### Unanswered Questions (Framework-Relevant)

1. Does the propagation framework predict the **mathematical form** of the optimal ratio?
2. Is criticality reset a **derivation** from the three axioms, or an independent claim?
3. Does "coherent complexity" have a formal relationship to I(X;Z|Y) — outcome-irrelevant information?

---

**Pass Complete**: 2026-03-17  
**Next Pass Recommended**: Deep dive on optimal ratio modeling (T-010)  
**Files Written**: 
- `pass_01_survey.md` (this file)
- `session.json` (updated)
- `MASTER.md` (synthesis)
