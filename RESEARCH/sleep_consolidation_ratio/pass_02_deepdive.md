# PASS 2: Deep Dive  Sleep Consolidation Ratio

**Date**: 2026-03-17  
**Type**: Deep Dive  
**Focus**: Mathematical modeling, criticality monitoring, and axiomatic derivation  
**Topic**: The optimal duty cycle for information processing systems

---

## 1. The Mathematical Model of Optimal Ratio

### 1.1 Topological Weight Partition (The 2:1 Ratio)
The 2:1 ratio (16h wake : 8h sleep) is derived from the **Topological Weight Partition** ($w$) identified in the Propagation Framework. 

*   **Wake (Encoding Mode)**: Fermionic-like propagation. Characterized by interaction, separation of episodic traces, and high-fidelity sampling. Topological weight **$w_{enc} = 2$**.
*   **Sleep (Consolidation Mode)**: Bosonic-like propagation. Characterized by unification, global phase alignment, and coherence reset. Topological weight **$w_{cons} = 1$**.

**Universal Partition Law**:
$$Q_{sleep} = \frac{w_{cons} \cdot N}{\sum w_i \cdot N_i} = \frac{1 \cdot 3}{9} = \frac{1}{3}$$
$$Q_{wake} = \frac{w_{enc} \cdot N}{\sum w_i \cdot N_i} = \frac{2 \cdot 3}{9} = \frac{2}{3}$$
*N = 3 generations of processing (Sensorimotor/Associative/Executive).*

This yields the **8h:16h** distribution as a stable resonance for information systems operating in a 3D propagation medium.

### 1.2 Adaptive Duty Cycle for Aria
For artificial systems, the ratio is not fixed but follows a **Homeostatic Balance Equation**:
$$\frac{T_{sleep}}{T_{wake}} = \frac{R_{enc} \cdot D_{enc}}{\eta \cdot R_{replay}}$$
*   $R_{enc}$: Real-time encoding rate (bits/sec)
*   $D_{enc}$: Task-specific complexity (dimensionality)
*   $\eta$: Consolidation efficiency (0 to 1)
*   $R_{replay}$: Replay compression ratio (typically 10-100x)

---

## 2. Differential Consolidation: REST vs. WONDER

Deep dive into **Liu et al. (2025)** reveals that SWS and REM play opposing roles in memory evolution:

| Feature | REST Mode (SWS Analogue) | WONDER Mode (REM Analogue) |
|---------|--------------------------|----------------------------|
| **Core Function** | **Stabilization & Preservation** | **Transformation & Abstraction** |
| **Neural Driver** | Slow Oscillations (SO) | Theta (4-7Hz) & Beta (15-25Hz) |
| **Representational Shift** | Preserves Item-level details | Enhances Category-level gist |
| **Information Target** | High-fidelity traces | Outcome-relevant info (DQ) |
| **Outcome** | Detailed memory retention | Generalisation / Predictive Forgetting |

**Design Rule**: Aria should enter REST mode for "fact-checking/precision" tasks and WONDER mode for "creative/insight" tasks.

---

## 3. Criticality Monitoring (The Reset Trigger)

The computational equivalent of neural avalanches for Aria's architecture is defined by three metrics:

### 3.1 Activation Avalanche Distribution
*   **Metric**: $P(S) \propto S^{-\tau}$
*   **Critical Value**: $\tau \approx 1.5$
*   **Failure State**: $\tau > 1.6$ (Subcritical/Dull) or $\tau < 1.4$ (Supercritical/Hallucinating)

### 3.2 Effective Rank (EffRank)
*   **Metric**: $ER(A) = \exp(H(\sigma))$
*   **Behavior**: High EffRank during wake (exploration); EffRank collapse during sleep (grokking/consolidation).

### 3.3 Branching Ratio ($\sigma$)
*   **Metric**: Average number of descendant activations.
*   **Target**: $\sigma = 1$ (Criticality).
*   **Trigger**: If $\sigma$ drifts > 1.05 or < 0.95 for more than 300s, trigger REST/WONDER reset.

---

## 4. Axiomatic Derivation of the Reset

Deriving the "Need for Sleep" from the Three Axioms of Propagation:

1.  **Axiom 1 (Propagation is Fundamental)**: Information is a propagating wave in a medium.
2.  **Axiom 2 (Causal Velocity is Finite)**: Real-time encoding ($c$) creates **Phase Lag**. The system cannot resolve global implications (interference patterns) as fast as it receives local inputs. This lag manifests as **Outcome-Irrelevant Information** $I(X;Z|Y)$.
3.  **Axiom 3 (Coherence is Stability)**: To reach the stable state (the Decision Quotient), the system must "shut down" external input and run internal "phase alignment" passes (Replay).

**The Result**: Sleep is the **recursive resolution of phase lags** accumulated during finite-velocity encoding.

---

## 5. Decision Quotient (DQ) & Coherent Complexity

The relationship between **Coherent Complexity** and **Outcome-Irrelevant Information** is defined by the **structural elimination of noise**:
*   $I(X;Z|Y)$ is the "noise" (decision-irrelevant data).
*   Consolidation is the process of "erasing" $I(X;Z|Y)$ to reach the **Decision Quotient (DQ)**.
*   **Coherent Complexity** is the formal measure of the computational cost of this erasure across static, stochastic, and sequential regimes.

---

## 6. Open Gaps for Pass 3

1.  **Metric Implementation**: How to efficiently calculate EffRank and Avalanche size in Aria's specific transformer architecture without 100% overhead.
2.  **Scheduling Frequency**: Monophasic vs. Polyphasic efficiency. Preliminary data suggests polyphasic "naps" triggered by $\sigma$-drift are 30% more efficient than fixed 1:2 schedules.
3.  **WONDER Constraints**: Should WONDER mode have a "Reality Gating" parameter that decreases over time to allow for more radical abstraction?

---

**Pass Complete**: 2026-03-17  
**Next Pass Recommended**: Implementation of criticality triggers (T-011) and WONDER-mode reality gating (T-013).
