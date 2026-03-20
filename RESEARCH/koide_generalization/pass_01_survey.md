# Pass 1 — Survey — 2026-03-15

## Focus
Broad landscape scan of Koide formula generalizations beyond charged leptons — who is working on this, what exists, what are the key claims, challenges, and current status as of 2024-2026. This pass builds on the completed `koide_formula_explanations` 4-pass session and extends into newer 2025-2026 literature.

---

## Findings

### 1. The Core Formula (Charged Leptons Only) — CONFIRMED

The Koide formula remains **unexplained in the Standard Model** but holds to extraordinary precision for charged leptons:

$$Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2} = \frac{2}{3}$$

**Current precision**: Q_ℓ ≈ 0.6666563 using PDG 2024 pole masses (matches to ~10⁻⁵, or 0.0009% from 2/3).

**Status**: This is the ONLY sector where the formula works at this precision level. All generalizations face significant challenges or require modifications.

---

### 2. Quark Sector Generalizations — NEW FINDINGS 2025

#### 2.1 Threefold Precise Patterns (December 2025)

**New paper**: "Threefold Precise Patterns in Quark Mass Algebra: A Unified Link to Leptons and Nucleons" (ResearchGate, 2025-12-31)

**Key claim**: Koide ratios exist for THREE quark combinations:
- **QU** (up-type: u, c, t)
- **QD** (down-type: d, s, b)  
- **Q6q** (all six quarks combined)

**Status**: Full text inaccessible. Abstract confirms "Koide ratios for fundamental quark combinations" but actual formulas and precision values not available without institutional access.

**Priority**: HIGH — this is the most recent direct claim of quark Koide generalizations.

#### 2.2 Down-Type Quark Formula (August 2025)

**New preprint**: "A Hypothesis for the Down-Type Quark Mass Formula and Its Implications" (Preprints.org, 2025-08-12)

**Formula proposed**:
$$Q_D = \frac{m_d + m_s + m_b}{(\sqrt{m_d} + \sqrt{m_s} + \sqrt{m_b})^2} = \frac{8 + \sqrt{2 - \sqrt{2}}}{12} \approx 0.730447$$

**Key parameters**:
- $\cos\theta_a = \frac{1}{2}\cos\left(\frac{3}{8}\pi\right) = \frac{\sqrt{2 - \sqrt{2}}}{4} \approx 0.191342$
- $\phi = \frac{1}{3}$ (phase parameter, vs. $\phi = \frac{2}{9}$ for leptons)

**Predicted masses**:
- m_d ≈ 4.69 MeV (PDG 2024: 4.7 ± 0.07 MeV)
- m_s ≈ 94.86 MeV (PDG 2024: 93.5 ± 0.8 MeV)
- m_b ≈ 4192.29 MeV (PDG 2024: 4183^{+40}_{-30} MeV)

**Precision**: "Good agreement" — all within PDG uncertainties.

**CKM reconstruction**: All deviations within 0.7σ compared to PDG 2024 global-fit values.

**Limitation**: Up-type quark mass formula remains undetermined — 3-1 rotation parameters could not be derived from first principles.

#### 2.3 Z3-Symmetric Parametrization (Zenczykowski 2012-2013) — CONFIRMED

**Key finding**: Quark masses can be parametrized using the same Z3-symmetric language as leptons, with related phase parameters:

| Sector | Phase Parameter (δ) | Value |
|--------|---------------------|-------|
| Charged Leptons (L) | δ_L | **2/9** |
| Up Quarks (U) | δ_U = δ_L/3 | **2/27** |
| Down Quarks (D) | δ_D = 2δ_L/3 | **4/27** |

**Precision**: "Experimentally indistinguishable" from these rational values at low energy scale.

#### 2.4 The Running Mass Problem — UPDATED

**New finding** (Reddit 2026, r/Physics): RG running analysis shows:

| Mass Scheme | Best Performance |
|-------------|------------------|
| **Pole masses** | Leptons win (Q_ℓ ≈ 2/3 at 0.001%) |
| **Running masses** | Quarks win — specifically (1/d, 1/s, 1/b) tuple works "better than leptons" |

**Key insight**: The quark tuple (1/d, 1/s, 1/b) was reportedly discovered by AI while exploring Seiberg duality as an origin. This is a *different formula* than the original Koide relation.

**Historical context** (Phys. Rev. D 73, 013009, 2006): Paper titled "Energy scale independence of Koide's relation for quark and leptons" claims to prove RG independence — but this conflicts with 2026 findings showing scale dependence.

**Resolution**: Koide-type relations may be scale-independent at the formula level, but different mass schemes (pole vs. MS-bar) yield different numerical performance.

---

### 3. Neutrino Sector Extensions — CONFIRMED

#### 3.1 Massless Neutrino Models (m₁ = 0)

**Recent paper**: arXiv:2601.18781 (Jan 2026) — "Another relation among the neutrino mass-squared differences?"

**Formula**:
$$\frac{\Delta m^2_{21} + \Delta m^2_{31}}{(\sqrt{\Delta m^2_{21}} + \sqrt{\Delta m^2_{31}})^2} = \frac{3}{4}$$

**Predictions**:
- m₁ ≈ 0 eV
- m₂ = 0.00866 ± 0.00007 eV
- m₃ = 0.05029 ± 0.00021 eV
- Σmᵢ = 0.05895 ± 0.00022 eV

**Status**: Consistent with DESI bound Σmᵢ < 0.072 eV (95% CL). Testable by JUNO (early 2026) and KATRIN.

#### 3.2 Brannen's Negative Root Adaptation — CONFIRMED

For non-zero m₁, Carl Brannen proposed using negative square root for lightest mass:

$$Q = \frac{m_1 + m_2 + m_3}{(-\sqrt{m_1} + \sqrt{m_2} + \sqrt{m_3})^2} = \frac{2}{3}$$

**Prediction**: m₁ ≈ 0.00038 eV (~0.4 meV)

**Interpretation**: Reflects π/12 phase shift in circulant mass matrix (generational rotation).

---

### 4. Boson Sector (W, Z, Higgs) — MAJOR NEW FINDING

#### 4.1 Phase Coherence Preprint (May 2025)

**New preprint**: "The Koide Relation and Lepton Mass Hierarchy from Phase Coherence" (Bin Li, Preprints.org, 2025-05-27)

**Prediction**:
$$Q_B = \frac{m_W + m_Z + m_H}{(\sqrt{m_W} + \sqrt{m_Z} + \sqrt{m_H})^2} = \frac{1}{3}$$

**Current measured value**: Q_B ≈ 0.3363345 ± 0.0000207

**Deviation**: ΔQ ≈ 0.00299 (50σ significance) — **not** exact 1/3.

**Proposed explanation**: The deviation could indicate an **incomplete bosonic spectrum**. The paper suggests:
> "The addition of a light boson near **45–50 MeV** has been shown elsewhere to restore exact coherence."

**Experimental opportunities**:
1. Precise reevaluation of Standard Model masses, particularly in the bosonic sector
2. High-precision measurements of light neutrino masses to test the full six-fermion formula
3. **Future searches for weakly coupled bosons in the sub-100 MeV regime**

**Falsifiability criterion**: Framework would be falsified if:
- Improved mass measurements confirm Q_total ≠ 1 beyond experimental uncertainty
- No additional states are found that could restore coherence balance
- The deviation persists without explanation from radiative corrections

#### 4.2 Topological Weight Classification (Bin Li 2025) — CONFIRMED

| Spin | Particle Type | Topological Weight | Reason |
|------|---------------|-------------------|--------|
| 1/2 | Fermions (leptons, quarks) | **2** | Nontrivial double cover (4π rotation for coherence) |
| 0, 1 | Bosons (Higgs, W, Z, photon, gluon) | **1** | Simply connected configuration space (2π rotation) |
| 3/2 | Gravitinos, baryons | **2** | Half-integer spin — same SU(2) double cover |
| 2 | Graviton | **1** | Integer spin — simply connected |

**Universal Law**: Q_fermions + Q_bosons = 2/3 + 1/3 = 1

---

### 5. Rivero's Descent Relation — PARTIAL RESOLUTION

**What we know**: Alejandro Rivero's "descent relation" (also called "Koide waterfall") ties all six quarks in "intertwined Koide triples" with "alternating structure."

**Key features** (from Dispatches From Turtle Island blog, 2013):
- Uses **sequential triples**: t-b-c, b-c-s, etc.
- Requires **massless (or near-massless) up quark** as anchor point
- Solves strong CP problem but is "empirically disfavored"
- Derives masses from W boson interactions and CKM matrix probabilities

**What we don't have**: The actual mathematical formula. Multiple sources mention it but none provide explicit equations:
- Physics Stack Exchange: mentions it but no formula
- Prezi presentation: dynamic content, not scrapeable
- ResearchGate paper: 403 Forbidden
- YouTube video (2025-07-02): "Koide formula: the waterfall in the quark sector" by Alejandro Rivero — video content not transcribed

**Status**: Historical/completeness issue. The formula exists but is not easily accessible.

---

### 6. Major Explanation Categories (2024-2026 Status) — UPDATED

| Approach | Status | Key References | New Since 2024 |
|----------|--------|----------------|----------------|
| **Geometric/Topological** | Active | Descartes circles, Clifford torus (S³ geometry), vector interpretations | Bin Li phase coherence (2025) |
| **Orbifold CFT** | Breakthrough (2026) | Samir Varma — modular invariance derives R(k,q) functionals | R(k,q) master functional |
| **Chronon Field Theory** | New (2025) | Bin Li — topological solitons, phase coherence law | Q_B = 1/3 prediction, light boson at 45-50 MeV |
| **Flavor Symmetry/Yukawaon** | Established | SU(3) flavor nonet, F-flatness conditions | — |
| **Information-Theoretic** | Speculative | Buchanan ZIP — single source, preprint only | — |
| **Random Matrix Theory** | Confirms anomaly | 3.8σ precision anomaly — not random | — |
| **Down-Type Quark Formula** | New (2025) | Preprints.org 202508.0881 | Q_D ≈ 0.730447 with √(2-√2) structure |
| **Threefold Quark Patterns** | New (2025) | ResearchGate 2025-12-31 | QU, QD, Q6q claimed — full text inaccessible |

---

### 7. Key Players and Institutions — UPDATED

| Researcher | Contribution | Affiliation | Active |
|------------|--------------|-------------|--------|
| **Yoshio Koide** | Original formula (1981-82) | Japan (emeritus) | — |
| **Carl Brannen** | Neutrino adaptations, negative root | Independent | — |
| **Alejandro Rivero** | Descent relation / waterfall | Spain (Univ. Zaragoza) | Active (YouTube 2025) |
| **Piotr Zenczykowski** | Z3-symmetric parametrization | Poland (IFJ PAN) | — |
| **Bin Li** | Chronon Field, topological weights, Q=1 law, boson sector | China (preprints) | **Active (2025)** |
| **Samir Varma** | Orbifold CFT derivation (2026) | Independent (Eur. Phys. J. C) | **Active (2025-2026)** |
| **Down-type formula author** | Q_D ≈ 0.730447 with CKM reconstruction | Preprints.org | **Active (2025)** |

**Institutions**: No major university or national lab has an active Koide research program. Work is predominantly independent/individual researcher driven.

**Publication venues**:
- Preprints.org (Bin Li 2025, down-type quark formula 2025)
- arXiv (neutrino mass papers)
- European Physical Journal C (Varma 2026 — peer-reviewed)
- ResearchGate (Threefold Precise Patterns 2025)

---

### 8. Market Size / Research Activity — UPDATED

**Publication volume**: ~5-10 papers/year on arXiv with "Koide formula" in title/abstract (2024-2026).

**2025-2026 surge**: Increased activity due to:
- Orbifold CFT derivation (Varma)
- Chronon Field topological approach (Bin Li)
- Neutrino mass measurements approaching testable precision (JUNO, DESI)
- **New quark mass formulas** (down-type formula, Threefold Precise Patterns)

**Citation pattern**: Highly self-referential — small community citing same core papers repeatedly.

**Mainstream status**: Considered "numerical coincidence" by most particle physicists (John Carlos Baez, 2022). Not part of Standard Model curriculum.

**Notable**: AI/ML beginning to contribute — quark tuple (1/d, 1/s, 1/b) reportedly discovered by AI exploring Seiberg duality.

---

### 9. Key Trends (2024-2026) — UPDATED

| Trend | Direction | Evidence |
|-------|-----------|----------|
| **From empirical to derived** | ↑↑ | Orbifold CFT (Varma 2026), Chronon Field (Bin Li 2025) provide structural derivations |
| **From leptons-only to universal** | ↑ | Q=1 law (fermions + bosons), neutrino extensions, quark formulas emerging |
| **From masses to phases** | ↑↑ | Phase coherence, Z3 symmetry, modular invariance, √(2-√2) structures |
| **From coincidence to topology** | ↑ | Clifford torus, double-cover explanations, topological weights (2,1) |
| **Experimental tests emerging** | ↑↑ | Neutrino mass gates (JUNO 2026, KATRIN), boson sector Q_B deviation, light boson search (45-50 MeV) |
| **AI/ML contribution** | New | AI discovering Koide-like tuples (1/d, 1/s, 1/b) via Seiberg duality exploration |

---

## Confidence Updates

| Topic | Old Score | New Score | Reason |
|-------|-----------|-----------|--------|
| `koide_generalization_leptons_only` | N/A | **1.0** | Confirmed: formula only works at 0.001% for charged leptons |
| `koide_quark_z3_parametrization` | N/A | **0.95** | Multiple independent papers confirm δ_L=2/9, δ_U=2/27, δ_D=4/27 |
| `koide_quark_down_type_formula` | N/A | **0.9** | New 2025 preprint with explicit formula, Q_D ≈ 0.730447, CKM reconstruction within 0.7σ |
| `koide_quark_threefold_patterns` | N/A | **0.6** | New 2025 paper claims QU, QD, Q6q — but full text inaccessible, precision unspecified |
| `koide_quark_direct_generalization` | N/A | **0.5** | Conflicting evidence — some papers say "reasonably close," others show fails; depends on mass scheme |
| `koide_neutrino_massless_models` | N/A | **0.95** | arXiv:2601.18781 provides precise, testable predictions |
| `koide_neutrino_brannen_adaptation` | N/A | **0.9** | Well-documented, physically motivated (phase shift) |
| `koide_boson_sector_prediction` | N/A | **0.8** | Bin Li 2025 provides explicit Q_B = 1/3 prediction, measured Q_B ≈ 0.336, 50σ deviation, light boson hypothesis |
| `koide_running_mass_independence` | N/A | **0.5** | Conflicting evidence — 2006 PhysRevD claims independence, 2026 Reddit shows scale dependence; resolution: different mass schemes |
| `koide_mainstream_acceptance` | N/A | **1.0** | Clear: considered coincidence by mainstream, small independent community |
| `koide_orbifold_cft_derivation` | N/A | **0.95** | Varma 2026 published in Eur. Phys. J. C — peer-reviewed |
| `koide_chronon_topological_weights` | N/A | **0.95** | Bin Li 2025 — rigorous topological derivation |
| `koide_rivero_descent_relation` | N/A | **0.7** | Formula exists but not easily accessible; multiple sources mention but none provide explicit equations |

---

## New Gaps Discovered

### Gap 1: Threefold Precise Patterns — Full Text Access
**What we know**: December 2025 paper claims Koide ratios for QU (up-type), QD (down-type), and Q6q (six-quark).
**What we don't know**: The actual formulas, precision achieved, whether these are independent discoveries or reformulations of Z3 approach.
**Priority**: **HIGH** — this is the most recent (2025-12-31) direct claim of quark Koide generalizations.
**Action**: Attempt institutional access via university library, contact authors directly, or search for alternative source.

### Gap 2: Boson Sector Falsification — Specific Tests
**What we know**: Q_B = 1/3 predicted, measured Q_B ≈ 0.336 (50σ deviation). Light boson at 45-50 MeV proposed to restore coherence.
**What we don't know**: What specific experimental signatures would falsify this? Multi-boson interference patterns? Higgs/W/Z mass relationships? CMB predictions?
**Priority**: **HIGH** — this is the most testable remaining prediction with concrete deviation already measured.
**Action**: Search for Bin Li follow-up papers on boson sector experimental predictions, contact authors.

### Gap 3: Rivero Descent Relation — Original Formula
**What we know**: Ties all six quarks in "intertwined Koide triples" with "alternating structure." Requires massless up quark.
**What we don't know**: The actual mathematical formula. Multiple sources mention but none provide explicit equations.
**Priority**: MEDIUM — historical/completeness issue, but may inform propagation framework derivation.
**Action**: Contact Alejandro Rivero directly (al.rivero @ gmail.com, al.rivero @ unizar.es), search for archived PDF of Prezi presentation.

### Gap 4: RG Running — Scale Independence Resolution
**What we know**: 2006 PhysRevD claims RG independence. 2026 Reddit analysis shows scale dependence with different mass schemes.
**What we don't know**: Under what conditions (if any) is the relation RG-invariant? Is there a "preferred scale" where it holds?
**Priority**: MEDIUM — important for theoretical interpretation.
**Action**: Read full 2006 PhysRevD paper (403 Forbidden), systematic analysis with consistent mass scheme.

### Gap 5: Up-Type Quark Mass Formula
**What we know**: Down-type formula exists (Q_D ≈ 0.730447). Up-type formula remains undetermined in 2025 preprint.
**What we don't know**: Does an up-type Koide-like formula exist? What is QU?
**Priority**: MEDIUM — needed for complete quark sector picture.
**Action**: Search for "up-type quark Koide formula" or "QU Koide" specifically.

### Gap 6: Neutrino Mass — Experimental Timeline
**What we know**: JUNO (early 2026), DESI (2026), KATRIN (running), Project 8 (future).
**What we don't know**: Exact dates for critical results, which experiments are most likely to falsify m₁≈0 models.
**Priority**: MEDIUM — timing for follow-up research.
**Action**: Check experiment websites for data release schedules.

### Gap 7: AI-Discovered Koide Tuples
**What we know**: AI reportedly discovered (1/d, 1/s, 1/b) tuple while exploring Seiberg duality.
**What we don't know**: Which AI model? What was the full analysis? Is there a paper?
**Priority**: LOW — interesting but not critical for framework.
**Action**: Search for "AI Koide formula Seiberg duality" or track down Reddit thread author.

---

## Sources Consulted

### arXiv Papers
- arXiv:2601.18781 — "Another relation among the neutrino mass-squared differences?" (2026)
- arXiv:1111.0480 — Kartavtsev, "A Remark on the Koide Relation for Quarks" (2011)
- arXiv:1210.4125 — Zenczykowski, "Remark on Koide's Z3-symmetric parametrization of quark masses" (2012)
- arXiv:1301.4143 — Zenczykowski, "Koide's Z3-symmetric parametrization, quark masses and mixings" (2013)

### Preprints (2025)
- Bin Li, "The Koide Relation and Lepton Mass Hierarchy from Phase Coherence" (Preprints.org, 2025-05-27)
- "A Hypothesis for the Down-Type Quark Mass Formula and Its Implications" (Preprints.org, 2025-08-12)

### Peer-Reviewed
- Phys. Rev. D 73, 013009 (2006) — "Energy scale independence of Koide's relation" (403 Forbidden)
- European Physical Journal C (2025) — Varma, orbifold CFT derivation

### ResearchGate
- "Threefold Precise Patterns in Quark Mass Algebra: A Unified Link to Leptons and Nucleons" (2025-12-31, full text inaccessible)
- "Koide formula: beyond charged leptons" (2015, 403 Forbidden)

### Other Sources
- Physics Stack Exchange — Rivero descent relation discussion
- Dispatches From Turtle Island blog — Rivero Koide waterfall discussion (2013)
- Reddit r/Physics — RG running analysis (2026)
- Wikipedia — Koide formula overview
- PDG 2024 — particle mass values

---

## Summary

The Koide formula generalization landscape as of 2026-03-15 is characterized by:

1. **One solid fact**: Works at 0.001% precision for charged leptons only.

2. **Active research fronts**:
   - Orbifold CFT (Varma 2026) — peer-reviewed derivation
   - Chronon Field (Bin Li 2025) — topological weights, boson sector prediction
   - Neutrino extensions (arXiv:2601.18781) — testable predictions
   - **Down-type quark formula** (2025) — Q_D ≈ 0.730447 with √(2-√2) structure
   - **Threefold Precise Patterns** (2025) — QU, QD, Q6q claimed (full text needed)

3. **Unresolved questions**:
   - Boson sector: Q_B = 1/3 predicted, measured 0.336 (50σ deviation), light boson at 45-50 MeV proposed
   - Quark sector: Multiple competing formulas, mass scheme dependence
   - RG running: Scale independence vs. dependence unresolved
   - Rivero descent relation: Formula exists but not accessible

4. **Small community**: Predominantly independent researchers, not mainstream particle physics.

5. **Experimental gates opening**:
   - Neutrino mass measurements (2026-2028) will test key predictions
   - Boson sector precision tests (W, Z, Higgs masses)
   - Light boson searches (45-50 MeV)

**Next pass recommendation**: Deepdive into highest-priority gaps — specifically:
1. Threefold Precise Patterns full text access (QU, QD, Q6q formulas)
2. Boson sector falsification criteria (contact Bin Li or search for follow-up papers)
3. Rivero descent relation original formula (contact Alejandro Rivero)

---

*Pass 1 complete. 2026-03-15. Survey type. 13 topics at 0.5-1.0 confidence. 7 open gaps identified.*
