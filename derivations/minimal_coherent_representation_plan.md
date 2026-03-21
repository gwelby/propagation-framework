# Minimal Coherent Representation Principle: Research Plan
*Closing the Weinberg Spin-Pair Gap*

**Date**: 2026-03-21  
**Author**: Lumi (For the Team)  
**Status**: RESEARCH PLAN  
**Builds on**: `g3_spin_pair_identification.md`

## 1. The Gap
Codex's audit in `g3_spin_pair_identification.md` establishes that the spin pair $(1/2, 1)$ perfectly matches the PF's structural numbers ($w_f=2, N=3$) and the $\mathbb{Z}_3$ character structure ($\chi_{1/2}=1, \chi_1=0$). 

However, to graduate from "motivated identification" to "formal derivation," we must derive a **minimality principle** directly from Axiom 3 (Coherence). We need to prove why the vacuum selects the *lowest* spin representations that satisfy the topological constraints, rather than higher representations (like $s=5/2$ which also has $\chi=0$).

## 2. Axiom 3 and Energy Minimization
Axiom 3 states: "Coherence is necessary for stable structure." 
In physical systems, stable structures naturally settle into their lowest energy states. In a geometric/topological framework, "energy" is proportional to the curvature, winding number, or complexity of the representation. 

Higher spin representations correspond to higher-frequency angular harmonics (more complex knots, more twists). 

## 3. The Derivation Target
The team must formally link Axiom 3 to representation theory:
1. Define a "coherence cost" or "topological action" for a representation $j$ in $SU(2)$. (e.g., the Casimir eigenvalue itself, $j(j+1)$).
2. Prove that stability (Axiom 3) requires minimizing this cost.
3. Show that under the constraints of the system (fermionic double-cover survival vs. gauge annihilation under the $\mathbb{Z}_3$ step), the states that minimize the coherence cost are uniquely $j=1/2$ and $j=1$.

If we can write this proof, Argument A and Argument B fuse into a single, closed derivation.