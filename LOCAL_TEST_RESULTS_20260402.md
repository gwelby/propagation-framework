# Local Falsification Test Results — 2026-04-02

**Truth Order Compliance**: Results sourced from `sandbox_results.md` → `CLAIMS.md` → `ACTIVE_ISSUES.md` → scripts.  
**Purpose**: Actionable test matrix, not synthesis.  
**Agent**: Qwen Code

---

## Test Results Matrix

| Script | Claim Touched | Category | Runnable Now? | Current Result | Impact |
|--------|---------------|----------|---------------|----------------|--------|
| `koide_phase_scan.py` | Koide Phase δ₀ ≈ 2/9 | **Falsifier** | ✅ Yes | δ = 0.222229631490 rad, \|δ - 2/9\| = 7.4×10⁻⁶ (0.0033%) | **SUPPORTS** — strongest empirical anchor |
| `neutrino_koide_scan.py` | Neutrino Koide universality conjecture | **Falsifier** | ✅ Yes | Q_NO = 0.5496, \|Q - 2/3\| = 0.117 (17.5%) | **WEAKENS** — scoped null result for universality |
| `spin_pair_classification.py` | T1 Topological Weights | **Pressure Test** | ✅ Yes | j=0, 0.5 survive; j=1 annihilated | **PRESSURE** — contradicts old shorthand, not direct falsification of live T1 |
| `chiral_projection_z3.py` | God Equation Path A | **Pressure Test** | ✅ Yes | T_chiral³ NOT diagonal; Gap B confirmed | **NEUTRAL** — confirms existing gap, no new falsification |
| `koide_verify_pdg2024.py` | Koide Q = 2/3 (charged leptons) | **Regression** | ✅ Yes | Q = 0.6666605115 (0.000923% from 2/3); Brannen neutrino point Q_ν = 0.522473 | **SUPPORTS** — charged-lepton Koide confirmed; Brannen neutrino extension misses |
| `eeg_csd_simulator.py` | EEG Phase Transition (TEST 1) | **Falsifier** | ✅ Yes | Local template renders `sandbox/insight_phase_transition.png` | **NEUTRAL** — runnable locally, but still synthetic only |
| `analyze_real_eeg.py` | EEG Phase Transition (TEST 1) | **Falsifier** | ❌ Blocked | Requires local data/headset and missing Python deps (`pandas`) | — |
| `chiral_vs_symmetric_entropy.py` | God Equation ℤ₃ structure | **Pressure Test** | ⚠️ Needs run | Not executed this session | — |
| `ibm_quantum_h_prod_test.py` | H_prod factorization | **Falsifier** | ❌ Blocked / external | Local/hardware path requires IBM runtime stack or account access | — |
| `refractive_gravity_quantitative.py` | Gravity as Refraction | **Regression** | ⚠️ Needs run | Not executed — already DERIVED 0.95 | — |
| `shapiro_delay.py` | Gravity as Refraction | **Regression** | ⚠️ Needs run | Not executed — already DERIVED 0.95 | — |
| `perihelion_precession_simple.py` | Gravity as Refraction | **Regression** | ⚠️ Needs run | Not executed — already DERIVED 0.95 | — |

---

## Detailed Results

### 1. Koide Phase δ₀ = 2/9 — SUPPORTS

**Script**: `sandbox/koide_phase_scan.py` (cross-check helper: `verify_koide_exact.py`)  
**Claim**: Koide Phase row in `CLAIMS.md` (EMPIRICAL 0.65)  
**Result**:
```
δ_exact     = 0.222229631490 rad
2/9         = 0.222222222222 rad
|δ - 2/9|   = 7.4093×10⁻⁶ rad (0.0033%)
```
**Impact**: This is the tightest numerical coincidence in the framework. No status change recommended pending selection mechanism derivation.

---

### 2. Neutrino Koide Universality — WEAKENS

**Script**: `sandbox/neutrino_koide_scan.py`  
**Claim**: neutrino Koide universality conjecture discussed in `CLAIMS.md` Duck's Log / falsification paper  
**Result**:
```
Normal Ordering:
  Q_NO = 0.549622
  |Q_NO - 2/3| = 0.117 (17.5% deviation)

Inverted Ordering:
  Q_IO = 0.479016
  |Q_IO - 2/3| = 0.188 (28.2% deviation)
```
**Impact**: Universality falsified at >5% threshold. No dedicated CLAIMS.md row exists to demote; record as scoped null result. Koide Q = 2/3 is charged-lepton specific.

**Action**: Keep this as a scoped null result in `CLAIMS.md` notes / Duck's Log or in `papers/FALSIFICATION_PAPER_DRAFT.md`.

---

### 3. Topological Weights (2,1) — PRESSURE

**Script**: `sandbox/spin_pair_classification.py`  
**Claim**: T1 / `(2,1)` Topological Weights in `CLAIMS.md` (PARTIAL DERIVATION 0.85)  
**Result**:
```
j = 0.0   → χ = +1.0 → SURVIVOR
j = 0.5   → χ = +1.0 → SURVIVOR
j = 1.0   → χ =  0.0 → ANNIHILATED
j = 1.5   → χ = -1.0 → SURVIVOR
```
**Impact**: Contradicts simplified "j=1 survives, j=0.5 annihilated" narrative. The live T1 claim already acknowledges the physical-realization bridge (A_NR) as open, so this is **pressure on old storytelling, not direct falsification**.

**Action**: No status change. Document this only as pressure on the old low-spin narrative if needed.

---

### 4. Chiral Projection Path A — NEUTRAL

**Script**: `sandbox/chiral_projection_z3.py`  
**Claim**: God Equation / Path A route in `CLAIMS.md` and `ACTIVE_ISSUES.md` (CONDITIONAL 0.88)  
**Result**:
```
T_symmetric³ = [[0.25,  0.375, 0.375],
                [0.375, 0.25,  0.375],
                [0.375, 0.375, 0.25 ]]  → NOT DIAGONAL

T_chiral³ = [[0.2917+0j,     0.3542-0.0361j, 0.3542+0.0361j],
             [0.3542+0.0361j, 0.2917+0j,     0.3542-0.0361j],
             [0.3542-0.0361j, 0.3542+0.0361j, 0.2917+0j    ]]  → NOT DIAGONAL
```
**Impact**: Confirms existing Gap B no-go and Path A gap (Fourier-to-position-space bridge). No new falsification.

**Action**: No status change. Gap is already documented on the live board.

---

## What Did NOT Run

| Script | Blocking Factor | Priority |
|--------|-----------------|----------|
| `eeg_csd_analysis.py` | Missing MNE, pandas libraries | High (TEST 1) |
| `analyze_real_eeg.py` | Requires EEG headset or dataset and missing `pandas` | High (TEST 1) |
| `ibm_quantum_h_prod_test.py` | Requires IBM Quantum account access | Medium (H_prod) |
| `koide_verify_pdg2024.py` | Already executed after first draft; row updated above | — |
| `chiral_vs_symmetric_entropy.py` | Not executed — should run | Medium (pressure) |
| Gravity scripts | Already DERIVED 0.95 — low priority | Low |

---

## Recommended CLAIMS.md Edits (Truth-Order Legal)

### 1. Koide Phase Row

**Current**: EMPIRICAL 0.65  
**Proposed**: No change from this report alone. The 0.0033% precision is noted, but selection mechanism remains open.

**Add to Evidence column**:
> "Rerun 2026-04-02: δ = 0.222229631490 rad, |δ - 2/9| = 7.4×10⁻⁶ (0.0033%). Strongest empirical anchor."

---

### 2. Neutrino Koide Note (Duck's Log / falsification-facing docs)

**Current**: Mentions JUNO will refine, current local scan disfavors universality  
**Proposed**: Strengthen language to reflect confirmed falsification

**Add to Duck's Honest Log**:
> "Neutrino Koide universality falsified 2026-04-02: Q_NO = 0.5496 (17.5% from 2/3), Q_IO = 0.4790 (28.2% from 2/3). Koide Q = 2/3 is charged-lepton specific, not universal."

---

### 3. T1 Topological Weights

**Current**: PARTIAL DERIVATION 0.85, physical-realization bridge open  
**Proposed**: No status change. Add pressure note.

**Add to Evidence column**:
> "Pressure test 2026-04-02: spin_pair_classification.py shows j=0, 0.5 survive (χ=+1), j=1 annihilated (χ=0). Simple 'fermion=boson' narrative contradicted; χ=-1 sector uninterpreted. Physical-realization bridge (A_NR) remains the live gap."

---

### 4. God Equation Path A

**Current**: CONDITIONAL 0.88, Path A needs Fourier-to-position-space bridge  
**Proposed**: No change. Confirmed.

**Add to Evidence column**:
> "Pressure test 2026-04-02: chiral_projection_z3.py confirms T_chiral³ NOT diagonal in 3D. Path A gap confirmed."

---

## Next Actions (Priority Order)

1. **Run `koide_verify_pdg2024.py`** — Regression check on Q = 2/3
2. **Run `chiral_vs_symmetric_entropy.py`** — Pressure test on ℤ₃ structure
3. **Install MNE/pandas** — Enable EEG CSD analysis (TEST 1)
4. **Update CLAIMS.md** — Add neutrino null result note, Koide phase precision note
5. **Document χ=-1 sector** — What physical states occupy this branch?

---

*Generated: 2026-04-02*  
*Scripts executed: 6 (including local reruns after first draft cleanup)*  
*Truth-order compliant: Yes*  
*Ready for CLAIMS.md edits: Yes (narrow, evidence-only)*

⦿
