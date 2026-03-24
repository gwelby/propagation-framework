# Issue #5: Koide Phase δ₀ — Why 2/9?

**Created**: 2026-03-21  
**Priority**: HIGH (4.5σ empirical signal)  
**Status**: OPEN — gap identified, mechanism partially understood  
**Related**: Issue #2 (Koide amplitude), G3 (internal phase bridge)

---

## The Empirical Fact

**Charged lepton Koide phase**:
```
δ₀ = 2.3166 rad
δ₀ mod (2π/3) = 0.222230 rad
2/9 = 0.222222... rad

Residual: 7.4 × 10⁻⁶ rad = 33 ppm
Significance: 4.3σ (specific to 2/9), 3.1σ (with look-elsewhere)
```

**Source**: `http://lxbifi11.bifi.unizar.es:8080/3/results/koide_phases.md`

---

## The Mechanism (Rivero 2026)

**Three-instanton superpotential**:
```
W_3 = c₃ (det M)³ / Λ¹⁸
```

**Generates effective potential**:
```
V_eff(δ) ∝ [f(δ)]⁶ × (harmonic sum)

where f(δ) = -1/2 + cos(3δ)/√2
```

**Fourier expansion of [f(δ)]⁶**:

| Harmonic | Amplitude | Relative |
|----------|-----------|----------|
| cos(3δ) | 0.2554 | 1.000 |
| cos(6δ) | 0.1758 | 0.688 |
| **cos(9δ)** | **0.0879** | **0.344** |
| cos(12δ) | 0.0219 | 0.086 |
| cos(15δ) | 0.0022 | 0.008 |
| cos(18δ) | 0.00005 | 0.0002 |

**The gap**: cos(9δ) is **NOT dominant** — only 34% of cos(3δ) amplitude.

**Why it still matters**: Z₉ discrete symmetry (from 3 instantons × 3 generations) breaks U(1) phase to Z₉. The potential has **9 minima** at:
```
δ = 2/9 + 2kπ/3,  k = 0,1,2
```

**The open question**: What eliminates cos(3δ) and cos(6δ) to make cos(9δ) the leading term?

---

## Propagation Framework Connection

### What PF Has

From `koide_geometric_equivalence.md`:
- ✅ Derives **Q = 2/3** from energy equipartition ⟨z²⟩ = z₀²
- ✅ Derives **three generations** from SO(3) topology
- ✅ Derives **Z₃ symmetry** (120° phase steps in internal walk)

### What PF Lacks

- ❌ **No phase δ₀ derivation** — the Koide phase is not mentioned
- ❌ **No instanton mechanism** — PF has no non-perturbative dynamics
- ❌ **No Z₉ symmetry** — only Z₃ from generation cycle

---

## The Bridge Question (Codex Audit)

From `koide_phase_rivero_bridge_audit.md`:

**PF Z₃ cycle forces any reduced phase potential into the cos(3nδ) harmonic tower.**

| Harmonic | PF Origin | Rivero Mechanism | Status |
|----------|-----------|------------------|--------|
| cos(3δ) | Z₃ cycle (n=1) | One-instanton | ⚠️ Must be suppressed |
| cos(6δ) | Z₃ cycle (n=2) | Two-instanton | ⚠️ Must be suppressed |
| cos(9δ) | Z₃ cycle (n=3) | Three-instanton | ✅ Observed (33 ppm) |

**The theorem**: PF coherence might eliminate n=1, n=2 harmonics, leaving cos(9δ) as first surviving term.

**What needs proof**: Show that PF Axiom 3 (coherence necessary for stable structure) suppresses lower harmonics.

---

## Numerical Verification Tasks

### Task 1: Verify cos(9δ) Suppression Ratios

**Script**: `sandbox/cos9delta_verification.py`

**Compute**:
1. Fourier coefficients of [f(δ)]⁶ exactly (sympy)
2. Verify amplitudes match Rivero's values
3. Compute suppression ratios: cos(9δ)/cos(3δ), cos(9δ)/cos(6δ)

**Expected**:
- cos(9δ)/cos(3δ) ≈ 0.344
- cos(9δ)/cos(6δ) ≈ 0.500

### Task 2: Test Z₉ Minima Count

**Script**: `sandbox/z9_minima_count.py`

**Compute**:
1. Full V_eff(δ) = [f(δ)]⁶ × Σ_k 1/g_k(δ)²
2. Count local minima in [0, 2π)
3. Verify 9 minima (Z₉ symmetry)

**Expected**: 9 minima at δ ≈ 2/9 + 2kπ/3

### Task 3: Coherence Suppression Model

**Script**: `sandbox/coherence_suppression.py`

**Hypothesis**: PF coherence factor C(n) suppresses lower harmonics:
```
C(n) = exp(-n²/σ²)  or  C(n) = 1/n^p
```

**Test**: Can C(n) with reasonable σ or p suppress cos(3δ), cos(6δ) while keeping cos(9δ)?

---

## What Would Close This Issue

### Derivation Route (High Risk)

Show that PF axioms imply:
1. Z₃ cycle → cos(3nδ) harmonic tower ✅ (Codex proved)
2. Coherence Axiom 3 → suppresses n=1, n=2 ⚠️ (open)
3. Three-instanton dynamics → n=3 survives ✅ (Rivero has mechanism)

**Result**: δ₀ = 2/9 is the unique minimum of the leading surviving harmonic.

### Empirical Route (Medium Risk)

Verify:
1. All fermion triples have phases in one Z₃ fundamental domain ✅ (partial)
2. Lepton phase is closest to rational with small denominator ✅ (33 ppm)
3. Z₉ symmetry is unique subgroup compatible with PF ⚠️ (open)

**Result**: δ₀ = 2/9 is empirically selected, mechanism pending.

---

## Falsification Criteria

This issue is falsified if:

1. **δ₀ shifts with m_τ measurement** — If m_τ moves by >2σ and δ₀ mod 2π/3 moves away from 2/9 by >100 ppm, the coincidence fails.

2. **Other triples show random phases** — If quark triples have phases uniformly distributed in [0, 2π/3), not clustered near rational values, the Z₉ symmetry is accidental.

3. **Coherence model fails to suppress** — If no reasonable coherence factor C(n) can suppress cos(3δ), cos(6δ) while keeping cos(9δ), the mechanism is wrong.

---

## Related Issues

| Issue | Connection |
|-------|------------|
| **#2 (Koide amplitude)** | Amplitude Q=2/3 is derived; phase δ₀ is the missing half |
| **#3 (Weinberg angle)** | Independent — run in parallel |
| **G3 (α bridge)** | Wilson loop phase was wrong tool (SU(2) traces are real) |

---

## Research Plan

| Step | Task | Agent | Output |
|------|------|-------|--------|
| 1 | Verify cos(9δ) amplitudes | Qwen | `cos9delta_verification.py` |
| 2 | Count Z₉ minima | Qwen | `z9_minima_count.py` |
| 3 | Test coherence suppression | Qwen | `coherence_suppression.py` |
| 4 | Derive n=1, n=2 suppression | Codex | `coherence_harmonic_suppression.md` |
| 5 | Update CLAIMS.md | All | Koide phase entry |

---

## Resources

- **Rivero server**: `http://lxbifi11.bifi.unizar.es:8080/3/`
- **cos(9δ) derivation**: `calculations/cos9delta_derivation.py`
- **Koide phases**: `results/koide_phases.md`
- **Three-instanton**: `calculations/three_instanton_seiberg.py`
- **Assembly round 19**: `results/assembly_round19.md`

---

*Issue created: 2026-03-21*  
*Empirical status: 33 ppm (4.3σ)*  
*Mechanism: Z₉ symmetry from three-instanton dynamics*  
*PF gap: Coherence suppression of n=1, n=2 harmonics*
