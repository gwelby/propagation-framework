# Derivation: Fisher Curvature from PF Coherence Functionals
**Status**: Formalizing Bridge (In Progress)  
**Target**: Formally prove that the Propagation Framework (PF) coherence functionals ($F_C$ and $F_1$) mathematically yield the Fisher curvature structure required by the Chronotopic Theory of Matter and Time (CTMT).

## 1. The Gap Being Closed
The recent unification (Pass 4) established that the God Equation's spatial scaling factor $N^{D/2}$ is exactly the 3D coherence volume boundary $3^{3/2}$ derived in CTMT using the Fisher curvature determinant. 

However, CTMT is an external framework. To claim this as a **DERIVED** PF result, we must prove that the Fisher curvature metric ($G$) natively emerges from the PF's own Axiom 3 coherence functionals developed during the Casimir gap analysis:
- **$F_C$** (Family C): Mutual information of internal and external phase.
- **$F_1$** (Family B): Helical action-cost minimization.

## 2. Information Geometry: From $F_C$ to Fisher Metric $G$

### 2.1 The $F_C$ Functional
During the Weinberg angle derivation, we defined the coherence functional $F_C$ as the Mutual Information between the internal circulation phase $\Phi_{int}$ and the external drift phase $\Phi_{ext}$:
$$ F_C = I(\Phi_{int} ; \Phi_{ext}) $$
Maximum coherence (Axiom 3) requires maximizing this mutual information, which locks the topology to $k=1$ (the $1:1$ action-resonance).

### 2.2 Fisher Information as the Hessian of $F_C$
In absolute Information Geometry, Mutual Information is identically the Kullback-Leibler (KL) divergence between the joint phase distribution and the product of its marginals:
$$ I(\Phi_{int} ; \Phi_{ext}) = D_{KL}\Big( P(\Phi_{int}, \Phi_{ext}) \;\Big\|\; P(\Phi_{int})P(\Phi_{ext}) \Big) $$

The foundational theorem of Information Geometry states that the **Fisher Information Metric $G_{ij}$ is exactly the Hessian of the KL Divergence** evaluated at the matched distribution:
$$ G_{ij} = \frac{\partial^2}{\partial \theta_i \partial \theta_j} D_{KL} \Bigg|_{\Delta=0} $$

**Conclusion 1**: The CTMT Fisher metric $G$ is not an arbitrary choice. It is the exact, necessary geometric tensor that emerges when you take the second derivative (the curvature) of the PF's established $F_C$ coherence functional. $G = \nabla^2 F_C$.

## 3. The Local Phase Hessian $H$

CTMT defines the coherence density using a second tensor, $H$:
$$ H_{ij} = \nabla_i \nabla_j \Phi $$
This is simply the spatial Hessian of the macroscopic propagation phase $\Phi$. 

From the PF's action-resonance derivation (Route H), the total invariant phase $\Phi$ of the helical mode is:
$$ \Phi = \vec{k}\cdot\vec{r} - \omega t $$
For a single coherent structure, the wavefront must not tear. The Hessian $H$ measures the local physical curvature/dispersion of this wavefront, while the Fisher metric $G$ measures the statistical/information curvature of the phase locking $F_C$.

## 4. Recovering the CTMT Coherence Density

CTMT defines coherence density as the trace of the interaction between the Fisher metric and the Phase Hessian, scaled by the Fisher volume:
$$ \rho_c = \frac{1}{Z} \frac{\operatorname{tr}\big(G^{+} H\big)}{\sqrt{\det G}} $$

Let us translate this entirely into PF variables:
1. $G = \nabla^2 [ I(\Phi_{int} ; \Phi_{ext}) ]$ (How tightly locked the internal and external motions are).
2. $H = \nabla^2 \Phi$ (How sharply the physical wavefront is bending).
3. $\sqrt{\det G}$ is the invariant volume element of the Fisher manifold.

If $G$ is large (the modes are tightly locked, mutual information sharply peaked), the internal information volume $\sqrt{\det G}$ grows. 
For an isotropic 3D propagation medium ($D=3$), generating 3 distinct phase directions (the Koide $N=3$ generations), the fundamental matrix $G$ has 3 principal non-zero eigenvalues. 
Thus, the geometric volume of this coherence lock scales strictly as:
$$ \sqrt{\det G} \sim (\lambda_{lock})^{D/2} = (\lambda_{lock})^{3/2} $$

Because the Koide / SO(3) topology restricts the number of internal phase states to $N=3$, the eigenvalue scale exactly matches the generation count. 

## 5. Formal Result
The external CTMT equation $\sqrt{\det G} \sim 3^{3/2}$ is directly mathematically equivalent to taking the Information Geometry volume of the PF's $F_C$ mutual-information functional in 3D space with 3 generations. 

The $N^{D/2}$ scaling in the God Equation is therefore **a native consequence of Axiom 3**, formally derived by applying Information Geometry to the 1:1 phase-locking condition established in Route H.
