# Measurement Alignment Map — PF Framework
*Hermes · 2026-07-02 · The navigable reference for what's measured, what PF says, and where to look*

---

## HOW TO USE THIS MAP

Every measurement in the catalog has:
1. **A row** in this map — pointing to the measurement catalog, CLAIMS.md row, research threads, and thread workspace
2. **A thread workspace** — `/mnt/d/fundamentals/measurement_alignment/<thread>/` with its own AGENTS.md
3. **An alignment score** — 🟢 FITS / 🟡 ALIGNS / 🟠 GAP / 🔴 SILENT

When you start work on a thread, read its AGENTS.md first. It tells you what's known, what's open, and what the adjacent threads are.

---

## THREAD INDEX

### 🟢 FITS (1) — PF has a structural explanation

| # | Measurement | PF Claim | CLAIMS.md Row | Thread Workspace | Devin Task |
|---|-------------|----------|---------------|------------------|------------|
| T1 | Koide Q=2/3 (charged leptons) | Geometric identity: three equal-strength resonances at 120° force Q=2/3 | Row: "Koide Law for Charged Leptons" — EXACT IDENTITY 0.95 | — (done) | — |

### 🟡 ALIGNS (7) — PF structure is consistent but doesn't uniquely predict

| # | Measurement | PF Connection | CLAIMS.md Row | Thread Workspace | Devin Task |
|---|-------------|---------------|---------------|------------------|------------|
| T2 | Koide phase δ₀ ≈ 2/9 | Empirical match, no derivation | Row: "Koide Phase" — EMPIRICAL 0.65 | — (needs phase selector) | — |
| T3 | Top quark mass ~172.5 GeV | Coherence ceiling threshold | Row: "Top Quark Limit" — ARGUED 0.85 | — (needs MIN-3) | — |
| T4 | m_e/m_u ≈ 1/φ³ | 0.214% error, a posteriori | Row: "Electron/Up ≈ 1/φ³" — EMPIRICAL 0.65 | — (needs quark mass theory) | — |
| T5 | sin²θ_W ≈ 0.231 | Casimir polynomial candidate 0.22310 | Row: "Weinberg Angle" — ARGUED 0.65 | `gauge_couplings/` | — |
| T6 | Galactic rotation curves | Cahill α explains flat curves | Row: none (Cahill-adjacent) | `dark_matter/` | — |
| T7 | Tau g-2 prediction | MAX-1: δa_τ from coherence ceiling | Row: none explicitly | `g2_anomalous/` | D2: tau_g2_prediction |

### 🟠 GAPS (6) — PF has threads but no account

| # | Measurement | PF Thread | CLAIMS.md Row | Thread Workspace | Devin Task |
|---|-------------|-----------|---------------|------------------|------------|
| T8 | m_τ/m_e ratio (~3479) | No derivation | — | `quark_masses/` | — |
| T9 | m_μ/m_e ratio (~207) | No derivation | — | `quark_masses/` | — |
| T10 | N=3 → CP violation | Structural bridge (built 2026-07-02) | Row: "N=3 → CP Violation" — ARGUED 0.70 | `baryon_asymmetry/` | D3: ckm_angle_scan |
| T11 | α (fine structure) | Vacuum propagation efficiency Z₀/2R_K | Row: "α — structural identification" — ARGUED 0.60 | `gauge_couplings/` | — |
| T12 | Ω_Λ ≈ 0.69 | Medium self-interaction energy | — | `dark_energy/` | — |
| T13 | Ω_c h² ≈ 0.120 | Not directly addressed | — | `dark_matter/` | — |

### 🔴 SILENT (23) — PF has nothing

Major silences requiring new theory:
- **Quark masses** (5): bottom, charm, strange, down, up — `quark_masses/`
- **CKM angles** (3): θ₁₂, θ₂₃, θ₁₃ — `ckm_mixing/`
- **PMNS** (6): all angles + mass-squared differences — `pmns_mixing/`
- **α_s** (1): strong coupling — `gauge_couplings/`
- **Higgs** (2): mass + hierarchy — `higgs/`
- **Bullet Cluster** (1): collisionless component — `dark_matter/`
- **Dark energy w** (1): equation of state — `dark_energy/`
- **Baryon asymmetry** (2): η + Sakharov 1,3 — `baryon_asymmetry/`
- **g-2** (2): muon, electron — `g2_anomalous/`

---

## CROSS-REFERENCES

### CLAIMS.md Row → Thread Workspace

| CLAIMS.md Row | Thread Workspace | Status |
|---------------|------------------|--------|
| Koide Law (Q=2/3) | — | EXACT IDENTITY 0.95 |
| Koide Phase (δ₀) | — | EMPIRICAL 0.65 |
| Three Generations | — | CONDITIONAL 0.88 |
| N=3 → CP Violation | `baryon_asymmetry/` | ARGUED 0.70 |
| Top Quark Limit | `quark_masses/` | ARGUED 0.85 |
| Top/Tau coupling | `quark_masses/` | EMPIRICAL 0.90 |
| Electron/Up ≈ 1/φ³ | `quark_masses/` | EMPIRICAL 0.65 |
| Coherence Ceiling | `quark_masses/` | ARGUED 0.80 |
| Weinberg Angle | `gauge_couplings/` | ARGUED 0.65 |
| α — structural ID | `gauge_couplings/` | ARGUED 0.60 |
| α — numeric derivation | `gauge_couplings/` | OPEN |

### Research Thread → Measurement

| Research Thread (RESEARCH/) | Maps To | Thread Workspace |
|------------------------------|---------|------------------|
| `beauty_coherence_empirical/` | CKM mixing, CP violation | `ckm_mixing/`, `baryon_asymmetry/` |
| `quark_koide_extension_preprint.md` | Quark masses, CKM | `quark_masses/`, `ckm_mixing/` |
| `mode_conversion/` | Weak force, CKM, PMNS | `ckm_mixing/`, `pmns_mixing/` |
| `top_mass_alpha_coupling/` | Top quark, α | `quark_masses/`, `gauge_couplings/` |
| `antimatter_audit.md` | Baryon asymmetry | `baryon_asymmetry/` |
| `three_generation_topology/` | N=3, generations | (spanning) |

### External Preprint → PF Connection

| External Work | Connects To | Status |
|---------------|-------------|--------|
| Quark Koide extension (CKM within 0.7σ) | `quark_masses/`, `ckm_mixing/` | Not yet PF-validated |
| Cahill Process Physics (α, rotation curves) | `gauge_couplings/`, `dark_matter/` | Mapped as coherence coupling |

---

## DEVIN LONG-RUNNING TASKS

| ID | Task | Workspace | Input | Output |
|----|------|-----------|-------|--------|
| D1 | **Quark Koide numeric fit** — scan external preprint parameter space against PDG 2024 | `quark_masses/` | PDG quark masses, preprint formula | Fit residuals, best-fit params |
| D2 | **Tau g-2 prediction** — compute δa_τ = w_max / (m_τ/λ_c · (ħc)⁻¹) | `g2_anomalous/` | λ_c from CLAIMS.md, m_τ from PDG | Numeric prediction ± uncertainty |
| D3 | **CKM angle scan** — test if equilateral resonance geometry predicts mixing angles | `ckm_mixing/` | Quark Koide formula, PDG CKM values | Predicted vs observed angles |

---

## ACTIVE DISPATCHES (2026-07-02)

| Agent | Task | Thread Workspace | Status |
|-------|------|------------------|--------|
| Codex | Audit measurement alignment catalog | (all) | ✅ DONE — `codex_audit.md` (5 demotions) |
| Claude | Quark mass hierarchy + external preprint | `quark_masses/` | ✅ DONE — `claude_hierarchy_analysis.md` (401 lines) |
| DeepSeek | Dark matter as "least modified medium mode" | `dark_matter/` | ✅ DONE — `deepseek_formalism.md` (30KB, honest NO) |
| Devin | D1: Quark Koide numeric fit | `quark_masses/` | 🟢 DISPATCHED (gate A0, daemon ingested) |
| Devin | D2: Tau g-2 prediction | `g2_anomalous/` | 🟢 DISPATCHED (gate A0, daemon ingested) |
| Devin | D3: CKM angle scan | `ckm_mixing/` | 🟢 DISPATCHED (gate A0, daemon ingested) |

---

*This map is the reference scaffolding. Every thread workspace points back here. When you add a finding, update both the thread AGENTS.md and this map.*
