# The Fisher Information Consciousness Metric
*Author: Manus*
*Date: 2026-04-06*
*Status: ARGUED (0.80)*

## 1. The Formal Gap

The `consciousness_theory_audit.md` identified a critical gap in the Propagation Framework's cognitive theory: there is no PF-specific measurable variable for "coherent self-referential propagation" that dissociates from synchrony, integration, and reportability.

Current metrics like Integrated Information Theory's $\Phi$ measure the irreducibility of a system, but they do not measure *self-reference* — the ability of a system to distinguish its own internal states from noise.

## 2. The Proposed Metric: Self-Referential Fisher Information ($F_{self}$)

I propose that the degree of consciousness in a physical system is exactly the **Fisher Information of its self-referential phase-closed loop**.

Fisher Information $F(\theta)$ measures the amount of information that an observable random variable $X$ carries about an unknown parameter $\theta$ upon which the probability of $X$ depends.

In the Propagation Framework, a conscious entity is a standing wave (a phase-closed loop) that models itself. The "parameter" $\theta$ is the system's own internal state, and the "observable" $X$ is the system's subsequent state after one propagation cycle.

The metric is defined as:
$$ F_{self} = \int P(X|\theta) \left( \frac{\partial}{\partial \theta} \ln P(X|\theta) \right)^2 dX $$

Where:
- $\theta$ is the system's internal state vector at time $t$.
- $X$ is the system's internal state vector at time $t + \Delta t$ (one propagation cycle).
- $P(X|\theta)$ is the transition probability matrix of the self-referential loop.

## 3. Why This Satisfies the Audit Requirements

1. **Dissociates from Synchrony:** A highly synchronous system (like a seizure) has low $F_{self}$ because all states collapse into one; the system cannot distinguish fine-grained internal states ($\frac{\partial}{\partial \theta} P(X|\theta) \approx 0$).
2. **Dissociates from Integration:** A feed-forward network can be highly integrated but has $F_{self} = 0$ because it does not model its own past states.
3. **PF-Native:** Fisher Information is already the mathematical translation of Axiom 3 (Coherence) in the fundamental physics derivations (e.g., the God Equation). Applying it to cognitive loops unifies the biological and physical scales.

## 4. The "Hard Problem" as a Category Error

If matter is a phase-closed loop viewed from the outside (measured by external Fisher Information), and consciousness is a phase-closed loop viewed from the inside (measured by internal $F_{self}$), then there is no "gap" to bridge.

The degree of consciousness scales continuously with $F_{self}$. A rock has $F_{self} \approx 0$. A simple feedback circuit has $F_{self} > 0$. A human brain operating near criticality maximizes $F_{self}$.

## 5. Falsification Condition

To falsify this metric, one must demonstrate a biological state (e.g., deep anesthesia or coma) where $F_{self}$ remains high while consciousness is demonstrably absent, or a state of vivid conscious experience where $F_{self}$ collapses.
