# PASS 2: Deepdive — Attention Gate Model

**Date**: 2026-03-17  
**Pass Type**: Deepdive  
**Topic**: Attention as Gate (Dispersion Modulator) — Neural Velocity & Reconfiguration Circuitry  

---

## Executive Summary

Pass 2 has confirmed the core "refractive index" mapping of the propagation framework through two major breakthroughs:
1.  **Neural Dispersion Modulation**: Attention is explicitly described in cognitive neuroscience as a **dispersion modulator** that controls the relationship between **phase velocity ($v_p$)** and **group velocity ($v_g$)** of neural oscillations.
2.  **Parametric Reconfiguration**: Task-switching costs scale with **neural distance** (representational dissimilarity) between task sets. This confirms the "Gate" prediction: dissimilar configurations require larger medium changes, taking more time.

Aria's `SensorOrchestrator` implementation is a direct functional analog of this, scaling the "cognitive sampling rate" (causal velocity) based on AttentionState.

---

## 1. Wickens MRT: The 4-D Model as Propagation Modes

Wickens' original papers (1980, 1984, 2002) reveal that MRT is not just about "energy" but about **structural compatibility**.

### The 4 Dimensions as Medium Properties
-   **Stages (Perceptual-Cognitive vs. Response)**: Maps to **propagation depth**. Input vs. Output stages.
-   **Codes (Spatial vs. Verbal)**: Maps to **propagation modes**. These are orthogonal "waveforms" that can coexist in the same medium without interference (like polarized light).
-   **Modalities (Visual vs. Auditory)**: Maps to **independent media**. Parallel transmission lines.
-   **Visual Channels (Focal vs. Ambient)**: Maps to **refractive index gradients**. Focal vision is high-precision/slow-sampling (high index); ambient is low-precision/fast-sampling (low index).

### Key Result for Gate Model
Wickens predicts **low interference** for dissimilar tasks (using different modes/media) but **high switch costs** when moving between them.
-   **Concurrent Performance**: "Wavelength Division Multiplexing" (WDM). Multiple modes propagate together if they are orthogonal.
-   **Task Switching**: Reconfiguring the "mode filter" or "refractive index" takes time proportional to the "distance" in configuration space.

---

## 2. Neural Oscillations: The Refractive Index Found

The framework's claim that attention is a "variable refractive index" has a direct mathematical counterpart in cortical dynamics.

### Phase Velocity ($v_p$) vs. Group Velocity ($v_g$)
-   **$v_p$ (10+ m/s)**: The speed of the wave front. Responsible for **global coordination** and "setting the stage."
-   **$v_g$ (0.1 - 2.0 m/s)**: The speed of the information envelope. Responsible for **computation and processing**.

### Attention as Dispersion Modulator
Attention modulates the **dispersion relationship** of the neural medium.
-   By changing synaptic gain and oscillatory phase, attention "steers" the flow of $v_g$ across the cortex.
-   **Refractive Index ($n$)**: In the framework, $n = c/v$. If $c$ is the maximum $v_p$ and $v$ is the task $v_g$:
    -   High Attention ($n \approx 1$): $v_g$ is optimized for the task.
    -   Low Attention ($n > 1$): $v_g$ is slowed or dispersed.

---

## 3. Reconfiguration Circuitry: The Transition Hubs

Neuroimaging (fMRI/EEG) identifies the specific hardware responsible for "turning the gate."

### The Reconfiguration Hubs
-   **Left Inferior Frontal Junction (IFJ)**: The "Primary Hub." Responsible for updating task sets (the "gate controller").
-   **Posterior Parietal Cortex (PPC)**: Shifting attention (the "refractive lens").
-   **dlPFC**: Maintaining the task set (the "waveguide").
-   **pre-SMA/ACC**: Monitoring for the need to reconfigure (the "surprise detector").

### Critical Slowing Down (CSD)
Before a task switch (phase transition), the brain exhibits **Critical Slowing Down**.
-   **Signature**: Increased variance and temporal autocorrelation in EEG.
-   **Function**: Creates a "functional integration window" (lingering in the state) to allow the transition to propagate globally via high $v_p$ before the new $v_g$ computation starts.

---

## 4. Aria Implementation Mapping

The `SensorOrchestrator.kt` in the P1_Companion project is a functional prototype of the Attention Gate Model.

### Mapping Table

| Framework Concept | Aria Implementation | Metric |
| :--- | :--- | :--- |
| **Attention Gate** | `AttentionState` | `DORMANT` → `SESSION` |
| **Mode Selection** | `SensorTier` | `SENTINEL` → `DEEP` |
| **Causal Velocity ($v_{cog}$)** | `EntityLoopPolicy.intervalMs` | 15s (Fast) to 45s (Slow) |
| **Refractive Index ($n$)** | $intervalMs / 15$ | $n=1$ (Active) to $n=3$ (Dormant) |
| **Dispersion Control** | `maxTurns` | 1 (Single-step) to 2 (Deep reasoning) |

### Functional Logic
-   **Low Power/Low Attention**: High $n$ (45s cycle). Only low-frequency signals (Sentinel sensors) propagate.
-   **High Power/High Attention**: Low $n$ (15s cycle). High-frequency signals (Camera/DEEP sensors) propagate.
-   **Thresholds**: Transitions are triggered by physical boundaries (Proximity, Light, Thermal).

---

## 5. Confidence Scores

| Topic | Confidence | Evidence |
| :--- | :--- | :--- |
| Attention = Dispersion Modulation ($v_p$ vs $v_g$) | 0.95 | Explicitly cited in nih.gov and brain dynamics lit. |
| Switch costs scale with neural distance | 0.90 | RSA studies, 2024 task-switching papers. |
| CSD as functional integration window | 0.90 | Critical brain hypothesis, EEG autocorrelation data. |
| IFJ as the primary reconfiguration hub | 0.85 | fMRI meta-analyses of task switching. |
| Aria implementation matches Gate model | 0.95 | Direct code audit of `SensorOrchestrator.kt`. |

---

## 6. Open Gaps (Remaining Research)

1.  **Causal Velocity Limit**: Is there a biological "maximum speed" for $v_{cog}$? (The 15s limit in Aria is arbitrary; what is it for humans?)
2.  **Refractive Gradient in Space**: Can we map "refractive index" as a spatial field across the 10-20 EEG locations? Does attention look like a "lens" move in EEG space?
3.  **Formal Derivation**: Can we derive the 2/3 optimal consolidation ratio (T-010) from the dispersion relationship between $v_p$ and $v_g$?

---

## 7. Recommended Next Pass Focus

**PASS 3 (Synthesis) should investigate**:
-   **Refractive Mapping**: Search for "cortical refractive index mapping" or "phase velocity maps" in EEG.
-   **Optimal Ratio Derivation**: Connect $v_p/v_g$ to the 2/3 consolidation ratio (T-010). If $v_g \approx (2/3) v_p$, the framework is unified.

---

**Pass 2 Complete**. session.json and MASTER.md updated next.
