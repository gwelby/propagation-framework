# PASS 2: Technical Deep Dive — Photonic Coherence Computing

**Date**: 2026-03-16  
**Pass Type**: Deep Dive (technical gaps & formal theorems)  
**Researcher**: Gemini CLI  
**Topic**: photonic_coherence_computing  

---

## Executive Summary

This pass resolved the technical gaps regarding formal theorems, scaling laws, and the specific mechanism of partial coherence. We found that **coherence is a dual-edged sword** in photonic computing: while it enables complex-valued universality (Reck/Clements theorems), it imposes a "coherence price" in reservoir computing and tensor processing due to phase-noise-induced interference. The breakthrough finding is that **partial coherence** is an intentional engineering choice to suppress phase noise and enable high-density parallelization (MAC operations) through intensity-based summation.

---

## 1. Formal Coherence-Computation Theorems

We identified the foundational mathematical proofs that provide the "computational universality" for coherent optical systems.

### The Reck (1994) and Clements (2016) Theorems
*   **The Claim**: Any arbitrary $N \times N$ unitary matrix (linear transformation) can be decomposed into a physical mesh of beam splitters and phase shifters.
*   **Mechanism**: These theorems provide the exact recipe for configuring a Mach-Zehnder Interferometer (MZI) mesh to perform any complex-valued matrix multiplication.
*   **Significance for Propagation Framework**: This confirms that **coherent propagation through a structured medium is mathematically equivalent to universal linear computation**. The structure (mesh) defines the computation, and coherence allows the "result" to emerge from the interference of wavefronts.

---

## 2. The Mechanism of Partial Coherence (Nature 2024)

The study "Partial coherence enhances parallelized photonic computing" (Dong et al., *Nature* 2024) provides a critical nuance to the "more coherence = better" assumption.

### Why "Less" is "More" for Parallelization
*   **Problem with Full Coherence**: In high-density multiplexing (tensor cores), coherent signals interfere constructively/destructively, causing "interference-induced noise." This scrambles the calculation when summing many parallel channels into one detector.
*   **Solution: Partial Coherence**: By using light with a broader optical bandwidth (e.g., ASE light), the system "averages out" the random phase fluctuations.
*   **Intensity-Based Summation**: In the partially coherent regime, the photodetector performs a **linear sum of intensities** rather than a square of the sum of electric fields. This enables robust **Multiply-Accumulate (MAC)** operations across $N$ parallel channels without phase-related errors.
*   **Outcome**: $N$-fold enhancement in parallelism and 92%+ accuracy in classification tasks (MNIST/Gait) without the need for extreme thermal/phase stabilization.

---

## 3. Photonic Reservoir Computing (RC) Scaling Laws

The relationship between coherence length ($L_c$) and computational capacity in RC is non-monotonic.

### The "Price of Coherence" in Reservoirs
*   **Coherent Regime ($L_c \gg$ path differences)**: Computation relies on complex field interference. This is fast but sensitive to noise. The "state space" can become crowded, leading to **reduced memory capacity** (MC).
*   **Incoherent Regime ($L_c \ll$ path differences)**: Nodes couple via intensities. Studies show this configuration often has **larger memory capacity** and lower error rates for spatiotemporal tasks.
*   **Scaling Law**: Coherent RC often scales **sub-linearly with $N$** (number of nodes) due to phase constraints and correlations. Incoherent/Partially coherent RC scales **more linearly with $N$**, providing a more robust, high-dimensional state space.

---

## 4. Coherence Budgeting & Thresholds

We found that "coherence budget" is an engineering reality, often partitioned under specific technical terms.

### Key Metrics in Photonic Chip Design
*   **Phase Noise Budget**: The maximum allowable phase fluctuation for a target Bit Error Rate (BER). It is consumed by laser linewidth, non-linear phase noise (NLPN), and thermal gradients.
*   **Phase Coherence Length ($L_{coh}$)**: A critical **Process Design Kit (PDK)** parameter (e.g., ~4.17 mm for silicon strip waveguides).
*   **The Threshold**: If the physical path length of an on-chip interferometer exceeds $L_{coh}$, the **Phase Noise Budget is exhausted** by fabrication non-uniformity alone, rendering coherent computation (phase-sensitive) impossible without massive active compensation.
*   **Coherent Gain**: Coherent detection provides a ~10-15 dB sensitivity boost (shot-noise limited), which acts as a "buffer" for the link budget, allowing for longer reaches or more complex on-chip processing.

---

## 5. Synthesis with Propagation Framework Claims

| Framework Claim | Research Evidence (Pass 2) | Status |
| :--- | :--- | :--- |
| **Coherence is the master variable** | Coherence determines whether a system is phase-sensitive (universal) or intensity-based (parallelized). | **Strongly Supported** |
| **Coherence Length scales capacity** | True, but non-monotonic. High coherence scales "Unitary Depth"; Partial coherence scales "Tensor Width (Parallelism)." | **Refined** |
| **Sharp Computational Threshold** | Threshold exists at $L_{coh}$. Beyond $L_{coh}$, phase-sensitive computation "disperses" into noise (Axiom 3). | **Supported (Empirical)** |
| **Coherence Budgeting** | Formally managed as "Phase Noise Budget" and $L_{coh}$ limits in PDKs. | **Confirmed (Engineering)** |

---

## 6. Updated Open Gaps

1.  **Non-Linearity Thresholds**: How does the introduction of non-linearity (optical or electronic) change the coherence scaling laws?
2.  **Quantum-to-Classical Coherence Boundary**: At what point does a "coherent photonic processor" transition into a "photonic quantum computer" in terms of noise thresholds?
3.  **Active vs. Passive Compensation Costs**: What is the energy cost of maintaining coherence (thermal tuning/DSP) vs. the computational gain?

---

**Pass Complete**: 2026-03-16  
**Confidence Levels**: See session.json  
**Next Pass**: Non-linearity thresholds + energy-coherence trade-offs
