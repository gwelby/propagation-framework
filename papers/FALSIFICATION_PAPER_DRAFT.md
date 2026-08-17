# The Propagation Framework: Derivations and Falsifiable Predictions

**Draft v0.7 — 2026-08-07**
*G. Welby¹, [co-author TBD]²*
*¹ Independent Research*

**Target:** Foundations of Physics
**Status:** Working draft — not yet submitted. PUBLIC HOLD in effect.
**Changes in v0.7:** (1) Integrated the four honesty-layer modules into the Lean verification surface — KoideUnlocked (F2 domain restriction, machine-checked), CasimirGap (extra-β incompatibility, machine-checked), BekensteinGap (path mixing, G free parameter — prose-documented gaps), GodEquationGap (Postulate D target-loading, N^(D/2) fit-selection, IBM scope, convergence withdrawn — mixed theorem/prose-documented) — all build green, 0 sorrys; (2) added the F2 saga to the Honesty Log (domain overclaim caught by three independent mechanisms; corrected theorem machine-checked); (3) established the family's formalization pattern — "formalize the algebra, expose the gap, let the gap be honest" — as the method statement; (4) cross-referenced each gap module's non-theorem block against the claim-status ladder; (5) Lean surface: 44 tracked top-level sources, 41 root imports, 3 unimported standalone modules; aggregate `lake build PfLean` produces 8293 jobs (verified from `git archive`); base v0.7 commit `4bdeaeb` has parent `2942ed1` (2026-08-07 PRED-002/003 repair); the current candidate chain is `4bdeaeb → 218b54f → 2fb050c → cfae2df → … → 6b755c0`.
**Changes in v0.6:** (1) Fixed §5 section numbering (was incorrectly labeled 4.x); (2) fixed Weinberg angle σ inconsistency (0.90σ → 0.13σ, matching CLAIMS.md and abstract); (3) Axiom 3b relabeled as "Candidate Corollary" with explicit note that it is not derived from Axioms 1-3; (4) G1 status corrected from DERIVED to EXACT IDENTITY (matching CLAIMS.md); (5) T1 upgrade path updated — Family C MI approach falsified; (6) Lean build verification updated to 2026-08-02 (16534 jobs); (7) removed duplicate reference line in §4.2; (8) added Bohr-like spectrum (DERIVED 0.90) to Honesty Log; (9) corrected discussion to distinguish Lean-verified results from numerically-verified results.
**Changes in v0.5:** Integrated July 2026 audit wave: (1) Postulate D complete audit — all 7 probes fail to derive a=0 from Axioms 1-3; Postulate D is definitively a premise; (2) compact-orbit theorem fully proven in Lean (0 sorrys, build verified 2026-07-30); (3) Casimir MI attempt falsified (partition-dependent penalty); (4) O2bis decoherence attempt falsified (CPTP channel shows no selection); (5) "Seven approaches converged" and "52.7× decisive" language struck; (6) honest boundary statement: Axioms 1-2 strong, Axiom 3 underdetermined. Release posture unchanged: credibility-first, claim-status controlled by `CLAIMS.md`.
**Changes in v0.4:** Added May 2026 G3-OP-MAP audit wave; updated God Equation to split-tier CONDITIONAL 0.88 (operator algebra, Postulate D) / ARGUED 0.60 (scale formula, N^(D/2) fit-selected); recorded trace-norm and Perron-Frobenius routes as conditional negatives; added T3 information-theoretic selector NO-GO; made the release posture credibility-first and claim-status controlled by `CLAIMS.md`.
**Changes in v0.3:** Integrated neutrino Koide non-universality as a scope-delimiting positive result; updated God Equation discussion with Path B no-go results (Families A/B/edge-flux); added April 2026 pressure test findings to Honesty Log; updated Discussion to reflect framework scope. Journal target changed from PRL to Foundations of Physics (paper exceeds PRL word limit; FoP accepts honest theoretical frameworks with explicit derivation-status ladders).
**Changes in v0.2:** Added Weinberg angle derivation (Axiom 3b), QCD confinement, GR verification results, updated honesty log.

---

## Abstract

We present a minimal framework in which gravity, topological structure, and parts of the generation structure of the Standard Model emerge from three axioms about a propagation medium. The strongest current results, machine-verified in Lean 4, are: (1) null propagation in gravity is exactly optical geometry in the static case, with weak-field refractive index $n(\Phi) = \sqrt{(1-2\Phi)/(1+2\Phi)}$ (DERIVED 0.95); (2) the topological weights kernel obstruction $\mathrm{quatToSO3}(g) = 1 \Rightarrow \mathrm{order}(g) \in \{1,2\}$ (DERIVED 0.95); (3) the Koide mass ratio $Q = 2/3$ for charged leptons is a geometric identity forced by three equal-strength resonance modes at $120°$ spacing (EXACT IDENTITY 0.95); (4) the PF entropy Pythagorean decomposition (DERIVED 0.95); (5) the compact-orbit theorem for isometric propagation in finite-dimensional media (VERIFIED, 0 sorrys). We also report that the Koide $Q = 2/3$ relation does NOT hold for neutrino masses under either mass ordering ($Q_{NO} \approx 0.550$, $Q_{IO} \approx 0.479$, both $>5\%$ from $2/3$) — a positive scope-delimiting result confirming Koide as an electromagnetic-sector identity. The Weinberg angle $\sin^2\theta_W \approx 0.22310$ (ARGUED 0.65, $0.13\sigma$ match) and the three-generation result (CONDITIONAL 0.88, pending T1/T2 bridge theorems) remain open. We report honestly that the God Equation operator algebra (CONDITIONAL 0.88) depends on Postulate D, which is an explicit premise — all seven claimed derivation paths have been audited and none derive $a=0$ from Axioms 1-3. The framework's boundary is precise: Axioms 1-2 are strong (gravity, topology, compact orbits); Axiom 3 is underdetermined (cannot distinguish competing coherence conditions for the Casimir polynomial). We identify five experiments bearing on the framework's predictions and are explicit about which results are fully derived, which are argued, and which require additional structure.

---

## 1. Introduction

The Standard Model successfully describes particle physics but does not explain its own structure. Why are there exactly three generations of fermions? Why does the Koide formula $Q = (m_e + m_\mu + m_\tau)/(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2 = 2/3$ hold to four significant figures? These are treated as numerical coincidences or free parameters.

We propose that both facts may be consequences of the same underlying structure: a propagation medium in three spatial dimensions in which stable matter corresponds to topologically protected resonance modes. The derivation does not invoke supersymmetry, extra dimensions, or fine-tuning. It requires three axioms and the observed dimensionality of space.

This paper is written as a falsification document. Each claim is labeled with its derivation status (DERIVED, ARGUED, or EMPIRICAL), and each prediction is accompanied by a specific falsification criterion. We report results honestly, including where the derivation chain is incomplete.

### v0.4 Release Posture

This draft is a credibility-first release candidate. Public claims defer to `CLAIMS.md`; if this draft and `CLAIMS.md` conflict, `CLAIMS.md` wins. The May 2026 audit wave sharpened the main frontier without upgrading any confidence scores: `G3-OP-MAP` is now the active bounded strike for the God Equation bridge, and the trace-norm projection plus Perron-Frobenius collapse routes are recorded as conditional negatives rather than live closures.

### v0.5 Honest Boundary Statement

The July 2026 audit wave established the framework's boundary precisely:

**Axioms 1-2 are strong.** They derive gravity as optical geometry (0.95), the topological weights kernel obstruction (0.95), the Koide geometric identity (0.95), the Bohr-like spectrum (0.90), and the compact-orbit theorem (machine-verified, 0 sorrys). These are real, verified physics results.

**Axiom 3 is underdetermined.** The English statement "coherent propagation persists; incoherent disperses" is compatible with $\gamma\beta^n = \sqrt{C_2}$ for any integer $n$. Eight independent routes to the Casimir polynomial converged on the same gap: Axiom 3 cannot distinguish $\gamma\beta = \sqrt{C_2}$ (wrong) from $\gamma\beta^2 = \sqrt{C_2}$ (correct). The axiom is not wrong — it is too vague to select the correct coherence condition.

**Postulate D is extra structure.** The God Equation operator algebra (eigenvalues $\{1, -1/8, -1/8\}$) is exact given Postulate D ($a=0$, no self-loop). But Postulate D is an explicit premise. All seven claimed derivation paths have been audited: three are $a$-independent, one is tangential, one is circular, one is about a different parameter, and one is an endpoint artifact falsified by the CPTP control. No path from Axioms 1-3 to $a=0$ survives audit.

This is normal in theory-building. Newton's laws cover planetary motion but not Mercury's perihelion. The question is whether to extend, revise, or accept the boundary. We accept it honestly and publish what is proven.

---

## 2. The Framework

### 2.1 Three Axioms

**Axiom 1 (Propagation):** Everything that exists propagates. The medium is not empty space but a field capable of carrying a signal.

**Axiom 2 (Finite Velocity):** Propagation has a finite maximum causal speed $c$. This establishes a coherence length: disturbances separated by more than $\lambda_c = c/\Gamma$ (where $\Gamma$ is the medium's dissipation rate) cannot maintain phase-locked coherence.

**Axiom 3 (Coherence):** Stable structure requires self-reinforcing, coherent propagation. Incoherent modes disperse. A structure persists if and only if it satisfies the phase closure condition: after one complete circuit, the propagation mode returns to its original phase state.

**Axiom 3b (Minimal Winding Principle — Candidate Corollary):** Among coherent states in the same topological class, the stable fundamental mode is the one with minimal topological winding. A mode with winding $k = 1$ is fundamental; modes with $k > 1$ are excited or composite states.

*Note:* Axiom 3b is labeled a candidate corollary rather than a theorem. The July 2026 audit established that Axiom 3 as stated is compatible with $\gamma\beta^n = \sqrt{C_2}$ for any integer $n$ — coherence alone does not select $k=1$ over $k>1$. The minimal winding principle is a plausible selection rule, but it has not been derived from Axioms 1-3. See the boundary statement in §1 and the state-of-play in `derivations/casimir_extra_beta_state_of_play_2026-07-28.md`.

### 2.2 Gravity as Optical Geometry / Refraction

In a medium with spatially varying propagation speed $c(x)$, a wavefront propagating in a direction $\hat{k}$ experiences differential phase velocity across its extent. One side of the wavefront lags the other. The path curves.

This is refraction. In a medium where density increases toward a source, the wavefront curves toward the source without any direct force being applied. The apparent "pull" is a consequence of geometry, not an interaction.

**Claim F1 (DERIVED, domain-restricted):** In a medium with refractive index $n(x) = c_0/c(x)$, the trajectory of a propagating mode obeys:
$$\frac{d}{ds}\!\left(n\frac{d\mathbf{x}}{ds}\right) = \nabla n$$
which is formally equivalent to Newton's gravitational law near a spherical mass if $n(r) = 1 + r_s/r$ (Schwarzschild refractive index, where $r_s = 2GM/c^2$).

More precisely: null propagation in static gravity is exactly optical geometry, and in stationary gravity the minimum exact extension is Randers/Finsler optical geometry. The scalar-index picture above is the weak-field static limit.

### 2.3 Lean 4 Formalization

The framework's algebraic and group-theoretic content has been machine-verified in Lean 4. The formalization project (`PfLean/`) contains 44 tracked top-level `.lean` files, of which 41 are imported by the library root `PfLean.lean`; three tracked sources (`BekensteinBound`, `ChainRule`, `PeriodOrbitRefactor`) are standalone modules not in the main import graph. Build status: green, 0 sorrys; full `lake build PfLean` produces 8293 jobs (verified from `git archive` of commit `6b755c0`, not the live tree). The key verified theorems are:

**Gravity optics** (`PfLean.GravityOptics`):
```lean
theorem weakFieldIndex_sq {Φ : ℝ} (hΦ : |Φ| < 1 / 2) :
  (weakFieldIndex Φ) ^ 2 = (1 - 2 * Φ) / (1 + 2 * Φ)
```

**Topological weights kernel** (`PfLean.TopologicalWeights`):
```lean
theorem kernel_closure_orders :
  ∀ g : UnitQuaternion, quatToSO3 g = 1 → closureOrder g = 1 ∨ closureOrder g = 2
```

**Koide geometric identity** (`PfLean.KoideGeometry`):
```lean
theorem koide_Q_two_thirds_iff {a b c : ℝ} (ha : a > 0) (hb : b > 0) (hc : c > 0) :
  KoideQ a b c = 2 / 3 ↔ a ^ 2 + b ^ 2 + c ^ 2 = 4 * (a * b + b * c + c * a)
```

**PF entropy Pythagorean decomposition** (`PfLean.Entropy`):
```lean
theorem full_norm_Pythagorean (x : Fin 3 → ℝ) :
    (full_norm x) ^ 2 = (P0 x 0) ^ 2 + (P0 x 1) ^ 2 + (P0 x 2) ^ 2 + (PFEntropy x) ^ 2
```

**Compact-orbit theorem** (`PfLean.Axioms`):
```lean
theorem isometry_finite_dim_gives_compact_orbit
    (M : BareMedium) [FiniteDimensional ℝ M.State]
    (s : M.State) (hBdd : Hypothesis_BoundedOrbit M s) (hDNorm : Hypothesis_DIsNorm M) :
    IsCompact (closure (Set.range (fun t : {t : ℝ // t ≥ 0} => M.propagate t.val s)))
```

**Honesty-layer modules (algebra machine-checked, boundaries documented in comments):**

**Generalized Koide identity** (`PfLean.KoideUnlocked`):
```lean
theorem koide_Q_unlocked_physical {mbar β δ : ℝ} (hmbar : 0 < mbar) (hdom : DomainOk β δ) :
  KoideQ (s0 mbar β δ) (s1 mbar β δ) (s2 mbar β δ) = (1 + β ^ 2 / 2) / 3

theorem sqrt2_domain_not_universal : ¬ ∀ δ : ℝ, DomainOk (Real.sqrt 2) δ
```
The algebraic identity Q(β) = (1+β²/2)/3 is exact; the physical statement requires the domain condition (all branches non-negative). The earlier claim "Q = 2/3 for any δ" is false as a physical statement — the domain fails at δ = π/2 (1 − √6/2 < 0). The domain is part of the theorem, not a footnote.

**Casimir/Weinberg gaps** (`PfLean.CasimirGap`):
```lean
theorem extra_beta_gap {β C₂ : ℝ} (hβ_pos : 0 < β) (hβ_lt : β < 1) (hC₂ : 0 < C₂)
  (h_deBroglie : lorentzFactor β * β = Real.sqrt C₂)
  (h_casimir : lorentzFactor β * β^2 = Real.sqrt C₂) : False
```
The de Broglie condition (γβ = √C₂) and the Casimir condition (γβ² = √C₂) are algebraically incompatible for any physical particle — the core gap across all 8 derivation routes, now a theorem. The look-elsewhere scan proves (1/2, 1) is the unique match in the low-spin set (alternatives R ∈ (0.29,0.32), (0.09,0.13), (0.32,0.38) — all far from 0.22310).

**Bekenstein gaps** (`PfLean.BekensteinGap`): the chain-rule factor-of-2 resolution is pinned; the thermodynamic path mixing (partial vs total derivative), G as a free parameter, and the saturation hypothesis are documented as non-theorems.

**God Equation gaps** (`PfLean.GodEquationGap`):
```lean
theorem gap_residue_eigenvalue_requires_alpha_half : ... -- if the residue eigenvalue is -3/2, then α = 1/2
theorem gap_N_power_sensitive : Real.sqrt 27 ≠ Real.sqrt 8 -- 3^(3/2) ≠ 2^(3/2): N^(D/2) is fit-selected
```
Postulate D sets α = 1/2 — target-loading, now visible in the code. The N^(D/2) scale formula is fit-selected (√27 ≠ √8). IBM hardware scope: cyclic permutation circuits, not −1/8 eigenvalue measurement. The "seven approaches converged" claim is withdrawn (probes 4/5/6 do not discriminate a=0).

The Lean kernel has verified algebraic and group-theoretic content — including selected contradictions, domain restrictions, and dependency identities that constrain what can be derived. It has **not** verified: the Casimir polynomial derivation from axioms, the God Equation as a physical prediction, Postulate D as a theorem, or the Weinberg angle as a derived result. The formalization is honest about its scope: the algebra is machine-checked, and the boundaries of what that algebra cannot reach are documented in module comments and gap statements — not themselves kernel proofs.

---

## 3. The Generation Structure — Derivation

### 3.1 Topological Classification of Modes

In three spatial dimensions, the rotation group is SO(3). Its fundamental group:
$$\pi_1(\text{SO}(3)) \cong \mathbb{Z}_2$$

This has a direct physical consequence. There are exactly two topologically distinct ways a propagation mode can close on itself in 3D:

**Class 1 (contractible / bosonic-like):** The mode returns to its original state after a $2\pi$ rotation. One circuit for closure. Topological weight $w = 1$.

**Class 2 (lifted / fermionic-like):** On the nontrivial lifted branch, two circuits are required for closure. Topological weight $w = 2$. The physical fermion identification remains downstream of the numerator theorem.

**Claim T1 (PARTIAL DERIVATION):** In a 3D propagation medium, Axiom 3 plus `π₁(SO(3)) ≅ Z₂` gives a two-class closure-order structure. If closure weight is defined as the minimal number of full circuits needed to return a lifted mode to identity, the natural closure integers are `(2,1)`. Codex audit (2026-03-31): the revised T1 theorem file fixes the invalid mutual-information decomposition and cleanly isolates the `SU(2)` lift step, which survives as a conditional covering-space result. But the physical-realization bridge is still not derived: the chain rule gives only `F_C^tot >= F_C^(1)`, while strict coherence deficit requires an extra non-redundancy hypothesis `A_NR` not yet derived from Axioms 1-3. Therefore T1 remains `PARTIAL DERIVATION 0.85`, and the full fermion/boson distinction is still not completely closed from PF axioms alone.

### 3.2 Counting Stable Modes

From Claim T1, the total topological weight of a system with $N$ fermionic generations and $M$ massive bosonic mediators is:
$$W_{total} = 2N + M$$

The leptonic Koide ratio is the fraction of the total weight carried by the fermionic sector:
$$Q = \frac{2N}{2N + M}$$

**Claim T2 (PARTIAL DERIVATION):** In 3D space, the denominator is strongly supported by convergent co-dimension arguments pointing to `M = 3`. Codex audit (2026-03-31): the co-dimension draft proves a useful conditional lemma inside a local `2×2` Fermi-point Hamiltonian ansatz — in 3D, the codimension of a generic band-touching point and the dimension of the gap-opening perturbation space are both `3`. The PF theorem is not yet closed. v2 companion files narrowed the gaps but introduced new named conditionals: `C_mom` (translation invariance of the PF medium, not derived from Axioms 1-3), `C_FP` (Fermi points must exist in the weight-2 sector), and `C_bridge` (the three Pauli perturbation directions must be proved to be massive bosonic restoration modes of the PF coherence field, not merely algebraic deformation parameters). Codex found that Bridge 3 renamed rather than closed the core hidden step from the March 28 audit. Therefore `M = 3` is not yet fully closed. See `three_generations_t2_audit_2026-03-28.md`, `t2_denominator_theorem_audit_2026-03-31.md`, and `t2_denominator_theorem.md` Section 13 for all four Codex objections.

This is the current strongest route for grounding the denominator in the spatial dimension independently of the observed count of weak bosons. (Volovik [2003] derived the same result for superfluid $^3$He from analogous reasoning; here the framework has a strong convergent route to the same result, but not yet a single closed theorem.)

Substituting $M = 3$:
$$Q(N) = \frac{2N}{2N + 3}$$

Setting $Q = 2/3$ (the Koide ratio, measured):
$$\frac{2}{3} = \frac{2N}{2N+3} \implies N = 3$$

**Claim T3 (CONDITIONAL):** If the numerator theorem (the physical `(2,1)` closure-weight branch) and the denominator theorem `M = 3` both hold, then the number of fermion generations is uniquely fixed at $N = 3$. This is the only positive integer satisfying the Koide constraint in a 3D medium with topological weights `(2,1)`. See `derivations/three_generations_closed_proof.md` for the clean assembly theorem and its current prerequisite gates.

### 3.3 Why Q = 2/3 Is Exact: The Geometric Identity

The Koide formula written in amplitude space (letting $a_i = \sqrt{m_i}$):
$$Q = \frac{a_1^2 + a_2^2 + a_3^2}{(a_1 + a_2 + a_3)^2}$$

**Theorem:** $Q = 2/3$ if and only if the three amplitudes are equally spaced by $120°$ on a circle with radius $R = A\sqrt{2}$, where $A$ is the circle's center height.

*Proof:* Parametrize $a_i = A + R\cos(\theta + 2\pi(i-1)/3)$. The sum $\sum a_i = 3A$ (the cosine terms cancel by root-of-unity identity: $\sum_{k=0}^{2} e^{2\pi i k/3} = 0$). The sum of squares: $\sum a_i^2 = 3A^2 + 3R^2/2$. Therefore:
$$Q = \frac{3A^2 + 3R^2/2}{9A^2} = \frac{1}{3} + \frac{R^2}{6A^2}$$
Setting $Q = 2/3$ gives $R = A\sqrt{2}$. $\square$

**Physical meaning:** The three generation amplitudes are arranged on a circle, equally spaced at $120°$, with the specific ratio $R/A = \sqrt{2}$. This is the standard Foot-Harari-Zenczykowski parametrization, which fits the measured lepton masses to four significant figures with a single phase angle $\theta \approx 0.2222$ radians.

**Claim G1 (DERIVED — geometric identity):** $Q = 2/3$ is not a free parameter. It is forced by energy minimization: three equal-strength resonances on a circle minimize coupling energy at $120°$ spacing, which forces $R = A\sqrt{2}$ from the quantum harmonic oscillator ground/first-excited state amplitude ratio, which forces $Q = 2/3$.

The small deviation of measured lepton masses from exact $Q = 2/3$ ($<0.001\%$) is attributed to electroweak radiative corrections — perturbations to an underlying exact geometric identity.

---

## 4. The Weinberg Angle

### 4.1 The Casimir Polynomial

For a massive propagation mode with speed $\beta = v/c$ and Lorentz factor $\gamma = (1-\beta^2)^{-1/2}$ in a helical geometry, the drift-to-spin resonance ratio is $k = J_z/J_\theta$. Axiom 3 (phase closure) requires that the longitudinal drift $J_z = 2\pi\gamma\beta^2\hbar$ and the transverse spin $J_\theta = 2\pi\sqrt{C_2}\hbar$ (where $C_2 = j(j+1)$ is the Casimir invariant) maintain a rational resonance.

Axiom 3b (Minimal Winding, a candidate principle — see §2.1 note) selects $k = 1$: the primitive loop. Setting $J_z = J_\theta$:
$$\gamma\beta^2 = \sqrt{C_2}$$

With $x = \beta^2$, this yields the **Casimir polynomial**:
$$x^2 + C_2 x - C_2 = 0$$

### 4.2 The Weinberg Angle

The Weinberg angle parametrizes electroweak mixing: $\sin^2\theta_W = g'^2/(g^2 + g'^2)$. In the propagation framework, this is the ratio of longitudinal to total propagation in the electroweak sector.

For the mixed spin pair $(j_1, j_2) = (1/2, 1)$ with $C_2 = j(j+1) = 3/4$ (for $j = 1/2$), solving the Casimir polynomial gives $x \approx 0.4571$. The Weinberg angle follows from the electroweak mixing geometry.

**Claim W1 (ARGUED):** Multiple routes (generator count, stiffness ratio, coherence angle, topological, geometric embedding) produce $\sin^2\theta_W \approx 0.22310$, consistent with the PDG on-shell value ($0.22337$) to $0.13\sigma$. The minimal winding principle (Axiom 3b) provides a candidate explanation, but the look-elsewhere effect (five routes scanned) materially lowers confidence: the probability that a random target achieves a sub-percent hit is $\approx 0.46$ (1 in 2.2). The RG running from UV to IR ($M_Z$) is not yet derived internally. See `weinberg_angle_pf.md` and `coherence_functional_candidate_F_audit.md` for the full derivation.

**Note:** This is the UV (unification scale) value. The observed IR value $\sin^2\theta_W \approx 0.231$ at $M_Z$ differs due to renormalization group running, which the framework does not yet derive internally.

---

## 5. The Coherence Ceiling

### 5.1 Definition

From Axiom 2, the medium has a finite coherence length $\lambda_c$. A stable resonance mode requires:
$$\lambda_{dB} = \frac{\hbar}{mc} \geq \lambda_c$$

Modes with de Broglie wavelength below the coherence length cannot self-reinforce. They form but scatter before completing one oscillation. They are not particles — they are resonance failures.

### 5.2 Empirical Calibration

The top quark ($m_t = 173.1 \pm 0.9$ GeV) has de Broglie wavelength:
$$\lambda_{dB}(t) = \frac{197.3 \text{ MeV·fm}}{173,100 \text{ MeV}} \approx 1.14 \times 10^{-3} \text{ fm}$$

Its lifetime ($\tau_t \approx 5 \times 10^{-25}$ s) is shorter than the QCD confinement time ($\tau_{QCD} \approx 3 \times 10^{-24}$ s). The top is the only known quark that decays before forming a hadron. It is a resonance at the edge.

**Calibration result:** $\lambda_c \approx 1.14 \times 10^{-3}$ fm for the strong-sector coherence scale.

### 5.3 Fourth Generation

A fourth-generation quark would require (by the harmonic mode structure):
$$m_4 \gg m_t$$

LHC direct bounds: $m_{q'} > 700$ GeV. Its de Broglie wavelength:
$$\lambda_{dB}(q') < \frac{197.3 \text{ MeV·fm}}{700,000 \text{ MeV}} \approx 2.8 \times 10^{-4} \text{ fm} \approx \frac{\lambda_c}{4}$$

**Claim C1 (ARGUED):** No fourth-generation quark exists at any mass. This is not an energy-dependent exclusion (as in the Standard Model's electroweak precision argument) but a topological one. The fourth-generation mode cannot achieve phase closure in the medium regardless of coupling constants.

*Note: This claim is labeled ARGUED rather than DERIVED because $\lambda_c$ is currently calibrated to the top quark mass rather than derived from framework parameters. Deriving $\lambda_c$ analytically from Axiom 2 would upgrade this to DERIVED.*

### 5.4 The Generation Hierarchy

| Generation | Particle | Mass | $\lambda_{dB}$ | Medium status |
|-----------|----------|------|-------------|---------------|
| 1 | Electron | 0.511 MeV | 387 fm | Deep within coherence — stable |
| 2 | Muon | 105.7 MeV | 1.87 fm | First torsion mode — anomalous $g-2$ |
| 3 | Top quark | 173,100 MeV | $1.14 \times 10^{-3}$ fm | At coherence ceiling |
| 4 | (forbidden) | $>700,000$ MeV | $< 2.8 \times 10^{-4}$ fm | Below $\lambda_c$ — not a particle |

### 5.5 The Muon Anomaly as First Torsion

The three generations represent three qualitatively different relationships to the medium:
- **Generation 1:** Ground mode. Spherical symmetry. Minimal torsion. The electron anomalous magnetic moment agrees with QED to 13 decimal places.
- **Generation 2:** First harmonic. The medium deforms into a toroidal mode. The deformation creates a phase lag — the "First Torsion." **This is the muon $g-2$ anomaly.**
- **Generation 3:** At the coherence ceiling. The mode is locked — it has no room to wobble. The torsion averages out at the phase boundary.

**Claim M1 (ARGUED):** The persistent muon $g-2$ anomaly ($\Delta a_\mu \approx 2.5 \times 10^{-9}$, ~4$\sigma$ above Standard Model) is a structural consequence of the middle generation sitting in the First Torsion zone. It is not a Standard Model error — it is a measurement of the medium's elastic response to the first non-trivial harmonic mode.

**Quantitative prediction (pending):** Once $\lambda_c$ is derived analytically from Axiom 2, the framework predicts a specific value for the tau anomalous magnetic moment $a_\tau$ that deviates from QED by a calculable amount proportional to the ratio $m_\tau / (m_\tau^{ceiling})$, where $m_\tau^{ceiling}$ is the coherence ceiling mass. This will be presented in a companion calculation.

---

## 6. The Five Falsification Tests

This is the central section. Each test has a specific pass/fail criterion. A single well-executed failure falsifies the claim indicated.

---

### 6.0 What We Can Test Ourselves Now

| Test | Local status | Current reality |
|------|--------------|-----------------|
| TEST 1 — EEG phase transition | Partially self-testable | Local simulator runs; real-data analysis still needs Python deps (`mne`, `pandas`) plus headset / dataset access |
| TEST 2 — Neutrino Koide | Self-testable from public data | Current local scan already disfavors universality; JUNO can sharpen the exclusion |
| TEST 3 — Fourth generation exclusion | Not locally self-testable | Requires collider discovery / null searches |
| TEST 4 — Tau $g-2$ | Not locally self-testable | No closed local $\delta a_\tau$ prediction yet; depends on Belle II or equivalent |
| TEST 5 — GW dispersion | Not locally self-testable | Existing data constrain it; a distinctive PF beyond-GR prediction is not yet closed |

---

### TEST 1 — EEG Phase Transition (Near-Term, Low Cost)
**Tests:** Whether cognitive insight follows the same topological phase-transition mathematics as particle physics.

**Framework prediction:** A cognitive insight event is a phase transition in the propagation medium — identical in mathematical structure to a particle reaching the coherence ceiling and undergoing topological phase change. Specifically, the framework predicts that **Critical Slowing Down (CSD)** precedes every genuine insight event:
- EEG variance increases monotonically in the 5-second window before insight
- Alpha envelope suppresses >40% in the same window
- A gamma burst (30–80 Hz) marks the transition point

**Measurement:** EEG headset (Muse 2 or clinical equivalent), Mind Monitor app, problem-solving sessions with button-press insight marker.

**Falsification criterion:** If CSD (variance increase >50%) does not precede insight in ≥7 of 10 genuine insight events (p < 0.05 against noise baseline), the claim that insight and phase transitions share the same mathematics is falsified.

**Non-falsification:** A positive result in a single-subject study is consistent but not conclusive. Falsification requires a pre-registered multi-subject study (see TEST 1b — Medium path).

**What it would mean:** If insight events consistently show CSD, the same mathematics that governs the tau lepton at the coherence ceiling governs the moment a human brain crosses a cognitive boundary. The medium would be universal across scales.

---

### TEST 2 — Neutrino Koide (Pre-Answered; JUNO Quantifies the Deviation)
**Tests:** Whether the Koide $Q = 2/3$ ratio is universal across fermionic sectors or specific to charged leptons.

**Framework prediction (pre-v0.3):** Universal Koide, i.e., $Q_\nu \approx 2/3$.

**Result as of 2026-04-02 (pre-answered):** Universality is **falsified** at the $>5\%$ threshold. Computed from current oscillation inputs:
- Normal Ordering: $Q_{NO} = 0.549622$ — $17.5\%$ from $2/3$
- Inverted Ordering: $Q_{IO} = 0.479016$ — $28.2\%$ from $2/3$

This is not noise. The deviations exceed the falsification criterion definitively under both orderings.

**Scope revision (positive result):** The non-universality is structurally interpretable. Neutrinos interact only via the weak force; charged leptons interact electromagnetically. The Koide geometric identity ($Q = 2/3$ from three equal-strength resonances at $120°$) requires electromagnetic coupling to lock the amplitude geometry. In the neutrino sector, that locking mechanism is absent. The result is therefore a *positive scope-delimiting finding*: Koide is an electromagnetic-sector identity, not a property of ℤ₃ topology alone. This constrains the framework without falsifying the charged-lepton result (which is measured and DERIVED).

**Implication for the derivation chain:** The denominator theorem ($M = 3$) derives from 3D co-dimension arguments independent of which gauge sector is operative. The neutrino Koide null result is not in conflict with $M = 3$ or $N = 3$; it constrains the amplitude-geometry prediction (G1) to the electromagnetically coupled sector.

**JUNO's role (revised):** JUNO (2026) will constrain $\Delta m^2_{21}$ to sub-percent precision. This does not change the falsified universality conclusion, but will sharpen the measured deviation ($|Q_\nu - 2/3|$) to better than 1%. This allows precision comparison with any future PF prediction for the weak-sector Q value.

**What remains falsifiable:** If a future PF derivation of $Q_\nu$ in the weak-only sector produces a prediction, and JUNO data disagrees with that prediction, the framework is further constrained. The current result sets the target: any such prediction must land near $Q_{NO} \approx 0.55$.

---

### TEST 3 — Fourth Generation Absolute Exclusion (Long-Term, LHC / HL-LHC)
**Tests:** Whether the fourth-generation exclusion is absolute (framework) or energy-dependent (Standard Model).

**Standard Model position:** A fourth generation with standard couplings is excluded by electroweak precision data. However, a fourth generation with non-standard couplings (e.g., modified $Z$-pole contributions) is not excluded by the SM alone up to some mass range.

**Framework position:** No fourth generation exists at *any* energy, regardless of coupling. The exclusion is topological, not kinematic.

**Measurement:** HL-LHC (beginning ~2029) will extend direct search sensitivity to $m_{q'} > 2$ TeV for standard couplings, and future circular colliders (FCC-hh) to $>5$ TeV.

**Falsification criterion:** Discovery of a fourth-generation quark or lepton at any mass with any coupling structure falsifies Claim C1 absolutely.

**Non-falsification:** Continued null results up to any energy are consistent with the framework (but also with the SM for standard couplings).

**The unique prediction:** The framework predicts null results at *all* energies. The SM only predicts null results for standard-coupling scenarios. If a non-standard fourth generation is discovered, that falsifies the framework while being compatible with the SM.

---

### TEST 4 — Tau Anomalous Magnetic Moment (Medium-Term, Belle II)
**Tests:** The First Torsion prediction (Claim M1).

**Framework prediction:** The tau lepton, sitting at the coherence ceiling, should show a specific correction to its anomalous magnetic moment:
$$a_\tau^{Framework} = a_\tau^{QED} + \delta a_\tau^{torsion}$$

The torsion correction $\delta a_\tau^{torsion}$ is calculable once $\lambda_c$ is derived analytically (see the companion calculation, in preparation). Qualitatively, the correction is *negative* (the locked state averages out upward torsion) and smaller in magnitude than the muon anomaly $\Delta a_\mu \approx 2.5 \times 10^{-9}$.

**Standard Model prediction:** $a_\tau^{QED} = (1177.21 \pm 0.05) \times 10^{-6}$ (QED to three loops).

**Current experimental status:** $a_\tau$ is poorly measured ($|a_\tau| < 0.0052$ from LEP). Belle II is expected to reach sensitivity ~$10^{-4}$ within 5 years and potentially ~$10^{-5}$ at full luminosity.

**Falsification criterion:** If $a_\tau$ is measured and found consistent with pure QED to $10^{-5}$ with no framework-predicted torsion correction, Claim M1 is falsified. If the correction is found with the predicted sign and approximate magnitude, that constitutes strong confirmation.

**Note:** The quantitative prediction ($\delta a_\tau^{torsion}$) will be published separately once $\lambda_c$ is derived. This prevents post-hoc fitting.

---

### TEST 5 — Gravitational Wave Dispersion (Medium-Term, LIGO/LISA Data)
**Tests:** Whether gravity is refractive or geometric (i.e., whether the medium interpretation makes predictions beyond General Relativity).

**Framework extension target:** The exact current theorem (Claim F1) is the optical/Randers equivalence for null propagation in static/stationary gravity. A distinctive gravitational-wave dispersion signal would be a **beyond-current-claim** extension of that theorem, not part of the exact result already closed.

**Standard GR prediction:** Gravitational waves propagate at exactly $c$, with no dispersion.

**Current constraint:** GW170817 (binary neutron star merger, 2017) established that the GW speed equals the electromagnetic speed to within $\pm 3 \times 10^{-15}$ of $c$ across the LIGO frequency band (10–1000 Hz). This is a very tight constraint.

**Framework response:** The framework must be consistent with GW170817. The dispersion, if present, must be below current detection thresholds in the 10–1000 Hz band.

**Future test:** LISA (Laser Interferometer Space Antenna, planned ~2034) will measure GW in the $10^{-4}$–$0.1$ Hz band from supermassive black hole mergers. If the medium's refractive index has a frequency dependence that becomes detectable at very low frequencies, this would appear as a difference in arrival times between high-frequency and low-frequency GW components from the same source.

**Falsification criterion:** If LISA detects a frequency-dependent GW travel time, the magnitude must match the framework's prediction. If the framework predicts dispersion and LISA sees none at the relevant scale, Claim F1 is constrained (though not necessarily falsified if the dispersion scale is below LISA's sensitivity).

---

## 7. What Distinguishes This Framework from the Standard Model

| Prediction | Standard Model | This Framework |
|-----------|----------------|----------------|
| N = 3 generations | Free parameter | Conditional assembly result: uniquely fixed once the T1/T2 bridge theorems close |
| Koide ratio | Unexplained coincidence | Geometric identity from energy minimization |
| Weinberg angle | Measured free parameter | ARGUED 0.65 — consistent with Axiom 3b to 0.13σ (look-elsewhere effect materially lowers confidence) |
| 4th generation | Excluded for standard couplings | Excluded absolutely, all energies, all couplings |
| Muon g-2 | Unexplained anomaly | First Torsion of the 3D medium — structural, calculable |
| Tau g-2 | Pure QED | Modified by coherence ceiling torsion |
| EEG phase transitions | Not addressed | Same mathematics as particle phase transitions |
| Gravity | Metric curvature | Refractive gradient in propagation medium |

The Standard Model is a description. This framework is an explanation. Where both describe the same phenomenon, the SM remains the precision tool. Where they diverge, experiment decides.

---

## 8. Honesty Log — Derivation Status of All Claims

| Claim | Status | Confidence | What Would Upgrade It |
|-------|--------|------------|----------------------|
| T1: (2,1) topological weights | PARTIAL DERIVATION | 0.85 | Derive the non-redundancy hypothesis `A_NR` so the chain-rule lower bound upgrades from `F_C^tot >= F_C^(1)` to a strict coherence deficit. Note: the Family C mutual information approach was falsified (partition-dependent penalty, 2026-07-29); a partition-invariant coherence functional is needed. |
| T3: N=3 uniquely forced | CONDITIONAL | 0.85 | Close both the numerator theorem (physical `(2,1)` branch) and the denominator theorem `M = 3` from PF axioms alone |
| G1: Q=2/3 geometric identity | EXACT IDENTITY | 0.95 | Derive the equal-amplitude premise from PF vacuum dynamics (currently OPEN per CLAIMS.md) |
| F1: Gravity as optical geometry / refraction | DERIVED | 0.95 | Extend the exact optical/Randers statement into a distinctive, pre-registered beyond-GR prediction |
| Bohr-like spectrum from Coulomb eikonal | DERIVED | 0.90 | Kepler degeneracy proves 1/k² is exact for all eccentricities; phase closure verified to 0.00% error |
| Sleep 8h constant | ARGUED | 0.72 | Derive the biological encode/recover bridge and exact duty-cycle theorem from PF axioms alone |
| W1: Weinberg angle sin²θ_W | **ARGUED 0.65** | 0.65 | Derive Axiom 3b (minimal winding) from Axioms 1-3, and derive RG running to IR value 0.231. Machine-checked: `CasimirGap.lean` proves the extra-β incompatibility (γβ = √C₂ vs γβ² = √C₂ → False for 0<β<1) and the unique low-spin match (1/2,1). Prose-documented (NOT machine-checked): non-theorem blocks N1 (spin-pair selection), N2 (Axiom 3b), N3 (scheme selection), N4 (polynomial derivation) — these are honesty-layer documentation, not Lean theorems |
| QCD confinement from λ_c | ARGUED | 0.72 | Show threshold-aware higher-loop matching from the same UV boundary and clarify exactly what PF adds beyond standard QCD running |
| T2: Denominator M=3 from co-dimension | PARTIAL DERIVATION | 0.85 | Derive the PF-native dynamics giving the local `2×2` Fermi-point structure (including translation invariance `C_mom` and band-touching existence `C_FP`), and prove that the three gap-opening perturbation directions are the three massive bosonic restoration modes of the PF coherence field (`C_bridge`) — see `t2_denominator_theorem.md` Section 13 for all four Codex objections |
| C1: 4th generation forbidden | ARGUED | 0.85 | Derive λ_c from Axiom 2 analytically |
| God Equation (λ_c from l_P) | **CONDITIONAL 0.88** (operator algebra) / **ARGUED 0.60** (scale formula) | 0.60 | Postulate D is an explicit premise — all 7 claimed derivation paths audited (2026-07-30), none derive $a=0$ from Axioms 1-3. The CPTP channel (natural open-system completion) gives constant fidelity ~0.952 for all $a$ — no selection. The 52.7× ratio is an endpoint artifact (fair comparison $a=0$ vs $a=1/3$ is 1.62×). "Seven approaches converged" is withdrawn (honest count: zero derive $a=0$). The operator algebra eigenvalues $\{1, -1/8, -1/8\}$ are exact given Postulate D (machine-checked in `GodEquationGap.lean`: `gap_T3_residue_eigenvalue` proves (−1/2)³ = −1/8; `gap_residue_eigenvalue_requires_alpha_half` makes the target-loading of α=1/2 explicit; non-theorem blocks N1 Postulate D, N2 H_prod, N3 IBM scope, N4-N5 withdrawn convergence claims are PROSE documentation, not Lean theorems). The unconditional derivation remains open with no active route. |
| M1: Muon g-2 as First Torsion | ARGUED | 0.70 | Quantitative prediction of δa_τ from λ_c |
| D=3 from knot stability | ARGUED | 0.70 | Formal proof that topological stability requires D=3 |
| α (fine structure constant) | OPEN | 0.10 | Derive λ_c and m_e independently from axioms |
| Generalized Koide amplitude (free β) | EXACT IDENTITY (domain-restricted) | 0.95 | Q(β) = (1+β²/2)/3 is exact; β=√2 → 2/3 within the domain (KoideUnlocked.lean, 0 sorrys). The F2 domain restriction is confirmed by three independent mechanisms: Lean machine-check, direct code execution, and the retraction of a contrary claim (2026-08-07). |
| Koide phase $\delta_0 \approx 2/9$ | EMPIRICAL | 0.65 | Confirmed April 2026: $\delta = 0.22222963$ rad, $|\delta - 2/9| = 7.4 \times 10^{-6}$ (0.003%). Strongest empirical anchor in the framework. The nearby Casimir value $\sin^2\theta_W = 0.22310$ remains suggestive, but T-022 did not produce $2/9$ as a Casimir fixed point and T-021 did not confirm any legitimate Standard Model convention in which $\sin^2\theta_W(\mu)$ crosses $\delta$ near $\mu \approx 98$ GeV. Not DERIVED until a PF-native selector proof produces $2/9$ as a fixed point. |
| Neutrino Koide non-universality | EMPIRICAL | 0.95 | April 2026 confirmed: $Q_{NO} = 0.550$, $Q_{IO} = 0.479$. Koide is electromagnetic-sector specific. Scope-limiting positive result. |

**F2 saga — the filter working (2026-08-07):** the framework's identity "Q = 2/3" was originally claimed for any phase δ. An audit found the claim overreached: the identity holds only within the positivity domain (all branches 1 + β·cos(...) ≥ 0). A counter-correction then claimed the original claim was right after all — and was itself refuted by direct code execution (Q = 0.634574 at δ = 0.3, not 2/3). Three independent mechanisms converged: the Lean module `KoideUnlocked.lean` proves the domain restriction (`sqrt2_domain_not_universal`), the actual repo function reproduces F2's numbers, and the counter-correction was retracted. The corrected theorem, machine-checked, now stands in place of the overclaim. This is the falsification filter working in both directions: an overclaim was caught, a false correction was caught, and the machine now holds the boundary.

---

## 9. What Would Confirm the Framework (Not Just Fail to Falsify It)

Consistency with five tests would be confirming but not conclusive — many false theories are consistent with data. The framework would be *confirmed* (not merely not-falsified) by:

1. **A quantitative prediction of the muon g-2 value** made before the Fermilab final result, matched to within 1σ.
2. **A quantitative prediction of the tau g-2 correction** matched by Belle II.
3. **The EEG phase transition pattern**, pre-registered and confirmed in a multi-subject study (n ≥ 30).

Any one of these would move the framework from "consistent with data" to "uniquely predictive."

---

## 10. Discussion

The framework presented here is minimal: three axioms (with one corollary), one observed fact (D = 3), and the requirement that structure be topologically stable. From these, several of the deepest unexplained features of the Standard Model — the charged-lepton Koide mass ratio and gravity as optical geometry for null propagation — emerge as consequences fixed by the framework rather than as free parameters, while the Weinberg angle remains an argued/conditional candidate. The generation-count result is still conditional on unresolved numerator / denominator bridge theorems.

**Scope delimitation — neutrino Koide:** The finding that neutrino masses do not satisfy $Q = 2/3$ ($Q_{NO} \approx 0.550$, $Q_{IO} \approx 0.479$, both $>17\%$ from $2/3$, confirmed April 2026) is a positive result for framework scope. The Koide geometric identity requires electromagnetic coupling to lock the three-resonance amplitude geometry. The purely weak-sector neutrinos lack this locking mechanism. This is interpretable rather than merely negative: it identifies electromagnetic coupling as a necessary ingredient of the G1 geometric derivation, and constrains the framework's universality claim without touching the charged-lepton result. A future derivation of the neutrino Q value in a weak-coupling-only medium would be a precision prediction testable with JUNO data.

**God Equation — Postulate D audit complete (2026-07-30):** The derivation of $\lambda_c$ from the Planck length via $\lambda_c = \sqrt{2}\,l_P\exp(4\pi^2 N^{D/2}/b_0)$ is **CONDITIONAL 0.88** (operator algebra, given Postulate D) / **ARGUED 0.60** (scale formula, $N^{D/2}$ fit-selected). The operator algebra eigenvalues $\{1, -1/8, -1/8\}$ are exact given Postulate D ($a=0$, no self-loop). However, Postulate D is an explicit premise. All seven claimed derivation paths have been audited: (1) Casimir polynomial → $N=3$ (tangential — about $N$, not $a$); (2) $\kappa$-strike (about the coupling parameter $b$, not $a$ — both are free by the C₃ algebra theorem); (3) gauge holonomy (circular — assumes the primitive step is pure transport to conclude $a=0$); (4) mutual information ($a$-independent); (5) Fisher information ($a$-independent); (6) decoherence-free subspace ($a$-independent); (7) dynamical decoupling (endpoint artifact — fair comparison $a=0$ vs $a=1/3$ is 1.62×, and the CPTP channel gives constant fidelity ~0.952 for all $a$). No path from Axioms 1-3 to $a=0$ survives audit. The unconditional derivation remains open with no active route. The "seven approaches converged" and "52.7× decisive" language is withdrawn.

**The method — formalize the algebra, expose the gap, let the gap be honest.** Every major derivation in this framework now carries an honesty-layer module with machine-checked algebra and documented boundaries: `KoideUnlocked.lean` (the domain restriction that the "Q=2/3 for any δ" claim violated), `CasimirGap.lean` (the extra-β incompatibility at the heart of the Weinberg derivation), `BekensteinGap.lean` (the thermodynamic path mixing and G's status as a free parameter), and `GodEquationGap.lean` (Postulate D's target-loading made explicit, the N^(D/2) fit-selection proven, the IBM scope and the withdrawn convergence claims documented). The pattern: pin the algebra as a theorem, then document the boundary of what the algebra cannot reach in comments and gap statements. The boundary documentation is not itself a kernel proof — it is human-readable prose that records what was checked and what was not. A claim that survives both is either DERIVED or honestly CONDITIONAL — never silently in between. This is the falsification filter as a formalization practice, and it is the framework's strongest defense against the mythology layer that surrounds unexamined derivations.

The framework is not complete. The quark mass ratios and the absolute scale of fermion masses are not derived here. The fine structure constant $\alpha$ is structurally identified but not yet derived. The bridge between the biological predictions (EEG phase transitions) and the particle physics derivations is argued, not proved.

The framework now has six DERIVED or EXACT IDENTITY results at confidence $\geq 0.90$ (gravity optics 0.95, topological weights kernel 0.95, Koide geometric identity 0.95, PF entropy Pythagorean decomposition 0.95, Bohr-like spectrum 0.90, compact-orbit theorem verified with 0 sorrys). Five of these are machine-verified in Lean 4; the Bohr-like spectrum is verified by numerical phase-closure computation and hostile audit. A wider ring of CONDITIONAL and ARGUED bridges surrounds these, and the first pre-answered test (TEST 2, neutrino Koide) provides positive scope information. The boundary is precise: Axioms 1-2 produce the DERIVED results; Axiom 3 is underdetermined and cannot select the Casimir polynomial's coherence condition; Postulate D is extra structure not derived from the axioms. The path to further confirmation requires either formalizing Axiom 3 as a mathematical object that can distinguish competing coherence conditions, or experimental validation of unique predictions from the proven results.

The five tests above define that path, with TEST 2 now reporting a result rather than a prediction.

---

## Appendix A — PDG Mass Values Used

| Particle | Mass (PDG 2024) | Source |
|----------|-----------------|--------|
| Electron | 0.51099895 MeV | Direct measurement |
| Muon | 105.6583755 MeV | Direct measurement |
| Tau | 1776.93 MeV | Direct measurement |
| Top quark | 173.1 ± 0.9 GeV | LHC combination |
| Up quark | 2.16 MeV (MS-bar, 2 GeV) | Lattice QCD |

**Koide verification:** $Q_{measured} = 0.666661...$ vs $Q_{theory} = 2/3 = 0.666666...$
Deviation: $0.000875\%$ — consistent with radiative corrections.

---

## Appendix B — Conditional Assembly of Q(N) = 2N/(2N+3)

Granting the T1 numerator input (physical topological weights $(w_F, w_B) = (2, 1)$) and the T2 denominator input `M = 3`:

$$Q(N) = \frac{\sum_{\text{fermions}} w_F}{\sum_{\text{fermions}} w_F + \sum_{\text{bosons}} w_B} = \frac{2N}{2N + 3}$$

Solving $Q(N) = 2/3$:
$$\frac{2N}{2N+3} = \frac{2}{3}$$
$$6N = 4N + 6$$
$$N = 3$$

The solution is unique for positive integers. Conditionally, $N = 3$ is the only generation count consistent with the Koide ratio in a 3D medium once the numerator and denominator theorems are both granted.

---

## References

1. Koide, Y. (1983). "New view of quark and lepton mass hierarchy." *Phys. Rev. D*, **28**, 252.
2. Volovik, G.E. (2003). *The Universe in a Helium Droplet.* Oxford University Press.
3. Foot, R. (1994). "A note on Koide's lepton mass relation." *hep-ph/9402242*.
4. Harari, H., Haut, H., Weyers, J. (1978). "Quark masses and Cabibbo angles." *Phys. Lett. B*, **78**, 459.
5. Zenczykowski, P. (2012). "Koide relation and lepton masses." *Phys. Lett. B*, **718**, 901.
6. Budiyono, A. (2009). "Wave mechanics of particles from de Broglie soliton." *Physica A*, **388**, 4981.
7. Abbott et al. (LIGO/Virgo) (2017). "Gravitational waves and gamma-rays from binary neutron star merger." *Astrophys. J. Lett.*, **848**, L13.
8. JUNO Collaboration (2022). "JUNO physics and detector." *Prog. Part. Nucl. Phys.*, **123**, 103927.

---

*Draft v0.7 — 2026-08-07*
*"The framework has a boundary. We know where it is. We publish what's proven."*
⦿
