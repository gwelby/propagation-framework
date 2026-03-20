# MASTER: Koide Formula Explanations
*Last updated: 2026-03-15 — PASS 4 Actions*

## Executive Summary
The **Koide formula** is a 44-year-old empirical relation in particle physics that relates the masses of the three generations of fundamental fermions with an unexplained precision of ~0.001%. Recent theoretical breakthroughs (2025–2026) in **Orbifold Conformal Field Theory** and **Chronon Field Theory** have provided structural derivations based on modular invariance and topological weighting.

### Key Universal Ratios
| Sector | Functional Ratio (Q) | Theoretical Basis | Current Accuracy |
|--------|---------------------|-------------------|------------------|
| **Charged Leptons** | **2/3** | Modular Invariance (k=1, q=1) | 0.0009% (Pole mass) |
| **Quarks** | **1/2** | Orbifold CFT (k=2, q=1/3) | Verified @ MZ (4 decimal places) |
| **Bosons** | **1/3** | Topological Weight 1 (simply connected) | Predicted (Bin Li 2025) |
| **Universal Total** | **1.000** | Universal Phase Coherence Law | Predicted (Q_fermion + Q_boson = 1) |

---

## 1. The Core Formula
Proposed by **Yoshio Koide** in 1981-1982:
$$Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2} = \frac{2}{3}$$
- The value 2/3 lies at the exact center of the mathematically allowed range (1/3 ? Q ? 1 for positive roots).
- It predicted the tau mass to ~1777 MeV/c² before precise experimental confirmation.
- Holds to 0.001% precision using PDG 2024 pole masses.

---

## 2. Major Explanation Categories

### 2.1 Geometric & Topological Approaches
- **Descartes Circle Geometry** (Kocik, 2012): Lepton masses map to squared curvatures (m_i = b_i²) of pairwise intersecting circles. The 2/3 is the cosine of the 48.2° intersection angle.
- **Vector Interpretation**: Three vectors (?m_e, ?m_?, ?m_?) at 60° angles in 3D root-space.
- **Clifford Torus / S³ Geometry**: Claims derivation from "geometry of Clifford torus embedded in S³" as exact topological partition.

### 2.2 Flavor Symmetry & Yukawaon Models
- **Democratic Mass Matrices** (2000s): Start with S3 permutation symmetric matrix; breaking S3 ? S2 ? nothing generates hierarchy.
- **Yukawaon Model** (Liang & Sun, 2021): In SU(3) flavor nonet model, 2/3 emerges from F-flatness conditions. For scalar field potential to have three distinct generations: Tr(F²) = 2/3 (Tr F)².

### 2.3 Orbifold Conformal Field Theory (2026)
**Samir Varma** derived Koide ratios as **modular-covariant functionals** from orbifold CFT consistency:

**Master Functional:**
$$R(k, q) = \frac{\left(\sum_i m_i^{1/k}\right)^{kq}}{\left(\sum_i m_i^{1/(2k)}\right)^{2kq}}$$

| Parameter | Physical Meaning | Lepton Value | Quark Value |
|-----------|------------------|--------------|-------------|
| **k** (twist order) | Degree of twisted sector in orbifold CFT | k=1 (minimal twist) | k=2 (u/d split twist) |
| **q** (charge unit) | Minimal monodromy charge of fermion family | q=1 (electric charge) | q=1/3 (down-quark charge magnitude) |

- **Leptons (R_? = 2/3)**: R(1, 1) reproduces original Koide formula.
- **Quarks (R_q = 1/2)**: R(2, 1/3) ? 0.500 using MS-bar masses.
- **RG Invariance**: R_q(10¹? GeV) = 0.500 ± 0.002 — suggests high-scale orbifold dynamics preserved to low energies.

### 2.4 Chronon Field Theory & Phase Coherence (2025)
**Bin Li** models particles as topological solitons in a temporal flow field.

**Topological Weight Classification:**
| Spin | Particle Type | Topological Weight | Reason |
|------|---------------|-------------------|--------|
| 1/2 | Leptons, quarks | **2** | ??(M) ? ?? — nontrivial double cover (spinor bundle) |
| 0, 1 | Bosons (Higgs, W, Z, gluon, photon) | **1** | Simply connected configuration space |
| 3/2 | ? baryons, ? baryons, gravitino | **2** | Half-integer spin — same SU(2) double cover |
| 2 | Graviton | **1** | Integer spin — simply connected |

**Partition Formula:**
$$Q_{\text{sector}} = \frac{w_{\text{sector}} \cdot N_{\text{sector}}}{\sum_{\text{all sectors}} w_i \cdot N_i}$$

- **Leptons (Q_? = 2/3)**: Weight 2 × 3 generations / (2×3 + 1×3) = 6/9 = 2/3
- **Bosons (Q_B = 1/3)**: Weight 1 × 3 generations / (2×3 + 1×3) = 3/9 = 1/3
- **Universal Law**: Q_total = Q_fermions + Q_bosons = 2/3 + 1/3 = 1

### 2.5 Information-Theoretic Approaches
- **Zero-Interaction Principle** (Buchanan, recent): Masses as eigenvalues of Gaussian Pure Potential States; 2/3 = M? - M? (difference between third and second topological moments).

### 2.6 Random Matrix Theory Analysis
- **Anomalous Precision Study** (2025): Generic hierarchical mass matrix yields ?Q? ? 0.545; charged leptons Q_? = 0.666661 is a 3.8? precision anomaly, suggesting geometrically constrained system.

---

## 3. Neutrino Sector Extensions

### Massless Models (m? = 0)
- arXiv:2601.18781 (Jan 2026): Modified ratio (?m? + ?m?) / (??m? + ??m?)² = 3/4
- Predicts: m? = 0, m? = 0.00866 eV, m? = 0.05029 eV, ?m_i = 0.05895 eV
- Consistent with DESI bound ?m_i < 0.072 eV

### Non-zero Models (m? > 0)
**Carl Brannen's adaptation** uses "negative square root" for lightest mass:
$$Q = \frac{m_1 + m_2 + m_3}{(-\sqrt{m_1} + \sqrt{m_2} + \sqrt{m_3})^2} = \frac{2}{3}$$
- Predicts m? ? 0.00038 eV (~0.4 meV)
- Reflects ?/12 phase shift in circulant mass matrix (generational rotation)

---

## 4. Connection to Propagation Framework

The Koide derivations align directly with **Propagation Framework Axioms**:

| Axiom | Koide Connection |
|-------|------------------|
| **Axiom 1 (Propagation Fundamental)** | Mass as frequency (m = ?). Koide ratio is resonance stability condition for standing-wave patterns in vacuum medium. |
| **Axiom 2 (Causal Velocity)** | 2/3 lies at center of allowed range — stable equilibrium for propagation in 3D medium. |
| **Axiom 3 (Coherence)** | Total Q=1 law is conservation of coherence. Topological weights (2,1) are stress coefficients for coherent self-referential propagation. |

**Key insight**: The (2,1) weight partition may derive from causal structure of propagation medium — fermions require 4? rotation (double cover) for phase coherence, bosons require only 2?.

---

## 5. Experimental Falsification Gates (2026-2028)

### Neutrino Tests
| Experiment | Prediction | Status |
|------------|------------|--------|
| **JUNO (Jiangmen)** | Sub-percent ?m²?? precision; Normal Ordering favored | Early 2026 results expected |
| **DESI (Cosmology)** | ?m_i < 0.064 eV supports m? ? 0 models | 2026 upper limit |
| **KATRIN** | Sensitivity 0.2 eV; detection would falsify hierarchical models | Running |
| **Project 8** | Ultimate test at 40 meV absolute mass scale | Future |

### Boson Sector (Q_B = 1/3)
**Status: No direct experimental tests proposed yet**

Potential avenues:
- Multi-boson production cross-section deviations at coherence thresholds
- Modified Hong-Ou-Mandel interference with coherence-dependent phase locking
- Higgs/W/Z mass relationship predictions
- CMB polarization from early-universe boson coherence

### Spin-3/2 Extensions
- If SUSY discovered: Three generations of gravitinos (spin-3/2) should satisfy Koide-like relation with weight=2
- Baryon decuplet (?, ?*, ?*, ?) follows Gell-Mann–Okubo, not Koide — confinement complicates interpretation

---

## 6. Confidence Matrix

| Topic | Confidence | Source/Status |
|-------|------------|---------------|
| `koide_formula_definition` | 1.0 | Unambiguous, verified across 10+ sources |
| `koide_historical_discovery` | 0.95 | Koide 1982, Letters to Nuovo Cimento |
| `koide_precision_value` | 1.0 | 0.001% using PDG 2024 pole masses |
| `koide_standard_model_status` | 1.0 | Unexplained in SM; masses are free parameters |
| `koide_geometric_interpretations` | 0.9 | Descartes circles, vectors, torus — well-documented |
| `koide_flavor_symmetry_approaches` | 0.95 | Yukawaon F-flatness derivation confirmed |
| `koide_information_theoretic` | 0.8 | Buchanan ZIP — single source, preprint only |
| `koide_phase_coherence` | 1.0 | Bin Li 2025, topological weight derivation |
| `koide_random_matrix_analysis` | 0.85 | 3.8? anomaly, peer-reviewed methodology |
| `koide_neutrino_extensions` | 1.0 | Both m?=0 and m?>0 models mapped |
| `koide_quark_relations` | 1.0 | Varma 2026 Orbifold CFT, R_q=1/2 verified |
| `koide_modular_functional` | 0.95 | Full R(k,q) derivation from modular invariance |
| `koide_boson_experimental_tests` | 0.4 | No direct tests proposed — gap remains |
| `koide_spin_extensions` | 0.7 | Weight classification established; no explicit formula |
| `koide_propagation_connection` | 0.9 | Strong alignment with axioms; derivation pending |

---

## 7. Open Research Gaps

### Priority 1: Boson Sector Falsification
**Gap**: What specific experimental signature would falsify Q_B=1/3?
**Needed**: Concrete predictions for Higgs/W/Z mass relationships or multi-boson interference patterns.
**Action**: Contact Bin Li or search for follow-up papers on boson sector experimental predictions.

### Priority 2: Gravitino/Superpartner Koide Relations
**Gap**: If SUSY is discovered, would three generations of spin-3/2 gravitinos satisfy a Koide-like relation?
**Testable**: Future colliders could measure gravitino masses if SUSY broken at accessible scale.

### Priority 3: Modular Functional Uniqueness
**Gap**: Is R(k,q) the unique modular-covariant functional, or one of a family?
**Needed**: Proof that orbifold constraints fix R(k,q) uniquely, not just as one consistent ansatz.

### Priority 4: Propagation Framework Derivation
**Gap**: Does propagation-as-fundamental predict why topological weights are (2,1)?
**Action**: Derive (2,1) partition from causal structure of propagation medium — does coherence in 3D naturally give this ratio?

---

## 8. Pass History

| Pass | Type | Date | Focus | Key Findings |
|------|------|------|-------|--------------|
| 1 | Survey | 2026-03-15 | Landscape scan | 12 topics at 0.7-0.95 confidence; 5 explanation categories |
| 2 | Deepdive | 2026-03-15 | Original papers, Yukawaon, Chronon status | Koide 1982 composite model; F-flatness derivation; JUNO gates |
| 3 | Synthesis | 2026-03-15 | Orbifold CFT, Q=1 law, m? adaptations | R_q=1/2 from Varma 2026; Brannen negative root |
| 4 | Actions | 2026-03-15 | Boson tests, R(k,q) derivation, spin-3/2 | Full R(k,q) formula; weight=2 for all half-integer spin; no boson tests found |

---

## 9. Recommended Next Actions

### Research (External)
1. **Pass 5**: Deepdive on boson sector falsification — search for Chronon Field experimental predictions beyond general signatures
2. Contact authors (Bin Li, Samir Varma) for follow-up on open questions
3. Search SUSY literature for "gravitino mass relations" or "spin-3/2 Koide"

### Framework (Internal)
1. Derive topological weight (2,1) from propagation axioms
2. Calculate boson mass relationships from Q_B=1/3 constraint
3. Update `sandbox_results.md` with Koide verification using PDG 2024 masses
4. Monte Carlo test: Is ?³ in electron/up-quark ratio significant? (T-001 from TASKS.md)

---

*MASTER.md regenerated. Pass 4 complete. 4 passes total. 4 open gaps remain at 0.4-0.7 confidence.*
