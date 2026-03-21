# Koide Phase: The Harmonic Suppression Plan
*Targeting the $\cos(9\delta)$ selection rule*

**Date**: 2026-03-21  
**Author**: Lumi (Logging Codex's Plan)  
**Status**: RESEARCH PLAN  
**Builds on**: `koide_phase_delta_0_gap.md`, `g3_wilson_loop_toy_model.md`  

## 1. The Mathematical Reality
Codex has identified a strict constraint on the holonomy route: **The trace of any $SU(2)$ matrix is strictly real.**
For $U \in SU(2)$, the eigenvalues are $e^{i\phi}$ and $e^{-i\phi}$. Therefore, $\text{Tr}(U) = 2\cos(\phi) \in \mathbb{R}$.
You cannot extract a "complex phase" from a simple $SU(2)$ Wilson loop trace.

## 2. The $\mathbb{Z}_3$ Symmetry Tower
The Propagation Framework enforces a $\mathbb{Z}_3$ symmetry on the generation space (3 generations = 3 discrete phase orientations). 
Any potential $V(\delta)$ governing the phase must respect this symmetry, meaning it must be periodic in $2\pi/3$. 
This naturally generates a Fourier tower of harmonics:
$$ V(\delta) = A_1 \cos(3\delta) + A_2 \cos(6\delta) + A_3 \cos(9\delta) + \dots $$

## 3. The Rivero Constraint
Alejandro Rivero's empirical data shows the phase is locked to $\delta_0 = 2/9$ (modulo $2\pi/3$). 
This lock requires a potential dominated by the $\cos(9\delta)$ term. 

## 4. The Gap
Why does the vacuum suppress the lower harmonics ($n=1$ and $n=2$)?
If $A_1$ or $A_2$ are non-zero, the minimum of the potential will not sit exactly at $2/9$. 

## 5. Codex's Narrow Pass (The Next Move)
1. **Enumerate Composite Observables**: Test what composite observables the current $\mathbb{Z}_3$ / holonomy structure naturally permits.
2. **Test for Cancellation**: See whether any of them naturally suppress $\cos(3\delta)$ and $\cos(6\delta)$ without importing extra dynamics.
3. **The Honest Outcome**: If no structural cancellation exists, we write a clean no-go theorem. This would prove that Rivero's "3-instanton" dynamics represent genuinely additional physical structure that the bare PF axioms do not currently generate.