# PRED-003 — Route U: Reverse-engineering the UGP 0.02936 neutrino mass-squared ratio

**Status:** REPORT / CONDITIONAL — this is an angle-specific inspection, not a locked prediction.  
**Date:** 2026-08-18  
**Agent:** Devin ∇λΣ∞  
**Authority tier:** advisory — reverse-engineering and structural comparison only  
**Public hold:** yes — Fundamentals PUBLIC HOLD remains in effect

---

## 1. Question

How does Nova Spivack’s **Universal Generative Principle (UGP)** obtain

```
r_ν = Δm²₂₁ / Δm²₃₁ = 0.02936  (often rounded to 0.0294)
```

from its GF(7)/Braid-Atlas/MDL substrate, and can the **Propagation Framework (PF)** either reproduce it or refute it on structural grounds?

---

## 2. What was examined

| Source | What it is | Why it matters |
|---|---|---|
| `/mnt/d/Fundamentals/PREDICTIONS/PRED-003-neutrino-mass-squared-ratio.md` | PF’s own scoping doc | Defines PRED-003 as the kill-shot candidate and lists the blockers. Lines 42–43 and 116–122 state UGP predicts `0.0294` from `GF(7)` arithmetic and that PF has no equivalent substrate. |
| `/mnt/d/Fundamentals/derivations/competitor_comparison_2026-08-02.md` | Rival-framework comparison | Lines 64–72 record UGP’s `0.0294` vs NuFIT 6.0 `0.02951 ± 0.00098`; lines 95–101 compare UGP’s `N=3` certification to PF’s conditional `Postulate D` status. |
| `/mnt/d/Fundamentals/PREDICTIONS/README.md` §C | Rival check for PRED-002 / PRED-003 | Lines 173–203 state UGP’s prediction is orthogonal to PF’s `Q_ν` claim and that PF does not predict the mass-squared ratio. |
| `/mnt/d/Fundamentals/PHYSICS_CONTEXT.md` §1.3 | God Equation / PF substrate | Describes PF’s propagation-geometry output: eigenvalues `{1, −1/8, −1/8}` from `U³ = P₀ − (1/8)Q`, conditional on `Postulate D`. |
| Local workspace search (`find_file_by_name`, `grep`) | UGP/GF(7) material | No local UGP source documents, Lean code, or saved PDFs were found. Only PF’s second-hand summaries exist. |
| Web search + Zenodo download | Primary UGP source | Located and downloaded Nova Spivack, *Predicting the Neutrino Mass-Squared Ratio from the Braid Atlas Topological Invariants and the QCD Colour Rank* (2026), Zenodo DOI `10.5281/zenodo.20170120` / `10.5281/zenodo.20682687`. The PDF was downloaded to `/tmp/neutrino_masses_from_braid_atlas.pdf` (487 151 bytes) and converted to text for inspection. |

---

## 3. UGP derivation summary — to the best of available evidence

### 3.1 Primary source

The source is a 2026 preprint in the UGP Physics series. The archival DOI is `10.5281/zenodo.20170120`; the June 2026 updated version is `10.5281/zenodo.20682687`. The relevant content is in the extracted text (this session’s copy, `/tmp/neutrino_masses_from_braid_atlas.txt`):

- Abstract, lines 12–28: states the prediction `Δm²₂₁ / Δm²₃₁ = 0.02936`, the inputs `N_c = 3` and b-values `{5, 11, 19}`, and the exponent `29/9`.
- §3.1–3.2, lines 221–273: gives the power-law ansatz and the explicit ratio formula.
- §4, lines 324–413: gives the three decompositions of `29/9` and the Lean theorem names.
- §4.4, lines 501–621: gives the Froggatt–Nielsen texture and the MDL selection of `(q₁, q₂) = (3, 2)`.
- §8.4, lines 986–999: explicitly lists the open question of the full Lagrangian bridge from the Braid Atlas to the SO(10) 126 Yukawa operator.

### 3.2 The exact arithmetic mechanism

UGP postulates a **single-exponent power law** for the light neutrino masses

```
m_ν,g ∝ b_g^α ,    {b₁, b₂, b₃} = {5, 11, 19},    α = 29/9 .
```

(PDF §3.1–3.2, equation (2), lines 242–247; equation (3), lines 256–268.)

Because `m_ν,g² ∝ b_g^{2α} = b_g^{58/9}`, the ratio of mass-squared *differences* is

```
Δm²₂₁ / Δm²₃₁ = (m₂² − m₁²) / (m₃² − m₁²)
              = (11^{58/9} − 5^{58/9}) / (19^{58/9} − 5^{58/9}) .
```

This evaluates to

```
0.0293571526565… ≈ 0.02936 ,
```

which matches the NuFIT 6.0 central value `0.02951 ± 0.00098` at `0.16σ` (`0.52%`).

I verified this arithmetic independently in this session with Python (no UGP code used):

```python
from math import exp, log
b1, b2, b3 = 5, 11, 19
alpha = 29/9
R = (b2**(2*alpha) - b1**(2*alpha)) / (b3**(2*alpha) - b1**(2*alpha))
print(R)  # 0.029357152656529106
```

Normal mass ordering is automatic because `b₁ < b₂ < b₃`.

### 3.3 Where the exponent `29/9` comes from in UGP

The exponent is not a fitted parameter. UGP claims three independent structural decompositions of the integer `29` (PDF §4, equation (5), lines 371–374):

```
29 = N_c³ + s = 4 N_c² − δ = dim(45_{SU(5)}) − dim(16_{SO(10)}) .
```

With `N_c = 3`:

- `s = (N_c² − 1)/4 = 2` is the Braid-Atlas strand count;
- `δ = N_c + (N_c² − 1)/2 = 7` is the charged-lepton “mirror offset”;
- `dim(45_{SU(5)}) − dim(16_{SO(10)}) = 45 − 16 = 29` is the “gauge/matter representation defect” of the PSC-selected GUT group.

Dividing by `N_c² = 9` gives `29/9`. UGP also writes this as

```
29/9 = N_c + θ_Koide,    θ_Koide = (N_c² − 1)/(4 N_c²) = 2/9 .
```

(PDF §4.1, lines 426–431.) The `2/9` is the same Koide phase that UGP derives for charged leptons from `N_c = 3`.

### 3.4 Froggatt–Nielsen texture

UGP identifies a two-flavon `U(1)₁ × U(1)₂` texture on the right-handed neutrino with charges

```
(q₁, q₂) = (N_c, strand) = (3, 2),
```

selected by a Minimum Description Length (MDL) “singleton-atomicity” rule (PDF §4.4, lines 537–620). This texture satisfies

```
q₁ + q₂ / N_c² = 3 + 2/9 = 29/9 .
```

The UGP pipeline claims the following theorems in `ugp-lean` (PDF §4, lines 382–418):

- `nu_seesaw_exponent_eq_Nc_plus_koide_theta`
- `nu_seesaw_exponent_three_decompositions`
- `seesaw_index_is_gauge_matter_defect`
- `fn_texture_gives_seesaw_exponent`
- `seesaw_ratio_independent_of_MR`
- `neutrino_mass_ratio_tight_bound`: `|R − 0.02936| < 0.0001`

### 3.5 Honest limits of this summary

I **do** have the primary-source PDF and I have verified that the stated formula reproduces the number `0.02936` to the precision advertised.

I **do not** have a local copy of `ugp-lean`, I have not run `lake build` on UGP’s code, and I have not independently checked the PSC/MDL selection of the Braid-Atlas b-values `{5, 11, 19}`, the GTE derivation of the right-handed-neutrino triples, or the full Lagrangian bridge from the FN texture to the SO(10) 126 operator. Those are UGP-internal claims; this report treats them as stated premises, not as independently verified facts.

---

## 4. PF comparison — UGP substrate vs. PF substrate

### 4.1 UGP’s substrate

UGP’s derivation is built on:

1. **PSC + three axioms** (locality, symmetry, compression/MDL) that select a unique integer seed and a `GF(7)` / GTE arithmetic cascade.
2. **Braid Atlas** topological invariants (`strand count`, `crossing number`, `b-value`) assigned to each SM fermion from GTE triples.
3. **Right-handed neutrino b-values `{5, 11, 19}`** taken as the primary mass-ladder invariants.
4. **A power-law ansatz** `m_ν,g ∝ b_g^{29/9}`.
5. **SO(10)/SU(5) GUT representation dimensions** (`45 − 16 = 29`) and a **Froggatt–Nielsen texture** `(3, 2)` to explain the exponent.

The output `0.02936` is a **ratio of powers of Braid-Atlas b-values**. The absolute mass scale (`E_D = v_H / 29`, `M_R ~ 2 × 10¹⁶ GeV`, `Σ m_ν ≈ 56 meV`) is a separate, scale-dependent layer.

### 4.2 PF’s substrate

PF’s relevant machinery is:

1. **Axioms 1–3** (Medium, Propagation, Coupling) plus **Postulate D** (`a = 0` in `U(a) = a·I + b·M`).
2. **God Equation** `U³ = P₀ − (1/8) Q` with eigenvalues `{1, −1/8, −1/8}` (`PHYSICS_CONTEXT.md` §1.3, lines 154–170).
3. **Z₃ circulant / `Circulant3Spectrum.lean`** algebra: real `D = 3` circulants with free parameters `b`, `c` and residue eigenvalues `λ = b·ω + c·ω²` (`PRED-003-neutrino-mass-squared-ratio.md` lines 100–106, 161–172, 185–216).
4. **Koide relation `Q = 2/3`** as a 120° equal-strength resonance identity for charged leptons (`PHYSICS_CONTEXT.md` §1.2, lines 95–151).

### 4.3 Does PF have an analogous structure?

| UGP ingredient | PF analogue? | Verdict |
|---|---|---|
| `GF(7)` / GTE integer triples | None. PF has no finite-field or cellular-automaton substrate. | **No** |
| Braid-Atlas `b`-values `{5, 11, 19}` | None. PF has no fermion-by-fermion topological mass-ladder invariant. | **No** |
| Power-law `m_ν,g ∝ b_g^{29/9}` | No structural power law on a generation index. The God Equation gives a single residue eigenvalue `−1/8` (twofold degenerate), not two distinct splittings. | **No** |
| Froggatt–Nielsen texture `(q₁, q₂) = (3, 2)` | No FN machinery in PF. | **No** |
| `SO(10)` GUT representation defect `45 − 16 = 29` | No GUT / representation input in PF. | **No** |
| Koide phase `2/9` | The rational `2/9` appears in PF’s Koide formula, but in PF it is the *phase* δ of the charged-lepton mass triplet, not a power-law exponent derived from `N_c = 3`. (`PRED-003` line 134 notes the phase δ is currently an open degree of freedom.) | Superficial overlap only |
| `N = 3` generations | PF selects `N = 3` via `Q(N) = 2/3 ↔ N = 3` once `Postulate D` and the `(2,1)` branch are granted (`PHYSICS_CONTEXT.md` §1.6, lines 292–298; `competitor_comparison_2026-08-02.md` lines 95–101). UGP selects `N = 3` as a unique PSC survivor over 34 560 candidates. | Different mechanism; both get `N = 3` |

### 4.4 PF’s own attempts (Route C toy probe)

`PRED-003-neutrino-mass-squared-ratio.md` §6.1 (lines 185–216) tested whether the free parameters `b`, `c` of `Circulant3Spectrum.lean` could be interpreted as a neutrino mass-squared ratio. The natural symmetric point `b = c = 1/2` gives `r₁ = 0.25`, which is **225σ** away from the measured `0.02951`. Off-symmetry tunings can hit `0.03`, but no PF axiom selects those values. This is the cleanest PF-native no-go available.

---

## 5. Implication for PRED-003

### 5.1 Is UGP’s number purely arithmetic/fit, or does it have a geometric interpretation?

Within UGP, the number is **not advertised as a fit** to the neutrino data. It is presented as a structural consequence of:

- the Braid-Atlas b-values `{5, 11, 19}` (claimed to be GTE-derived);
- the exponent `29/9` (claimed to be over-determined by `N_c = 3`, the Koide phase, mirror offset `δ = 7`, and GUT representation dimensions);
- the MDL-selected FN texture `(3, 2)`;
- the seesaw formula, with the common `M_R` cancelling from the ratio.

However, from the **PF side**, those premises are **external**: they come from a finite-field/number-theoretic/cellular-automaton substrate that PF does not have. There is **no propagation-geometric interpretation** of the b-values or the power law `b^{29/9}` in PF’s current axioms. The only geometric overlap is the rational `2/9` (PF’s Koide phase vs UGP’s `θ_Koide`), but that is a phase, not a power-law exponent, and it does not generate the observed ratio.

### 5.2 Can PF reproduce it?

**No, not without importing UGP’s substrate.** PF could *postdict* the number by writing

```
m_ν,g ∝ (some generation index)^{29/9},
```

but then PF would have to import the b-values `{5, 11, 19}`, the GTE triples, and the FN texture. That would be a PF-native derivation in name only.

### 5.3 Can PF refute it?

**No, not on structural grounds alone.** PF can say:

- the number does not follow from Axioms 1–3 + Postulate D;
- the natural PF structures (God Equation eigenvalues, `Circulant3Spectrum`) do not output it;
- the b-values and the power law are outside PF’s ontology.

But that is a statement about **PF’s incompleteness relative to UGP**, not a refutation of UGP. To refute UGP would require an independent PF derivation that gives a different number, or a proof that no such number can follow from propagation geometry — neither exists.

---

## 6. Honest conclusion

### 6.1 What we know

- **Primary source located and inspected:** Nova Spivack, *Predicting the Neutrino Mass-Squared Ratio from the Braid Atlas Topological Invariants and the QCD Colour Rank* (2026), Zenodo `10.5281/zenodo.20170120` / `10.5281/zenodo.20682687`.
- **Arithmetic formula identified:** `Δm²₂₁ / Δm²₃₁ = (11^{58/9} − 5^{58/9}) / (19^{58/9} − 5^{58/9})`.
- **Number verified independently:** `0.029357152… ≈ 0.02936`, matching the UGP claim.
- **Mechanism in UGP:** Braid-Atlas b-values `{5,11,19}` + power-law exponent `29/9 = N_c + θ_Koide`, with `N_c = 3` and `θ_Koide = 2/9`; the exponent is over-determined by `29 = N_c³ + s = 4N_c² − δ = 45 − 16`; the FN texture `(q₁,q₂) = (3,2)` is MDL-selected; the common `M_R` cancels in the ratio.

### 6.2 What we do not know

- Whether the UGP premises (PSC, MDL selection of the seed, GTE derivation of `{5,11,19}`, full Lagrangian bridge to SO(10) 126) are correct — they were not independently verified in this session.
- Whether the `ugp-lean` theorems named in the paper actually certify the claimed chain, because the repository was not cloned or built here.

### 6.3 Verdict on PRED-003

**REPORT / CONDITIONAL.**

UGP’s `0.02936` is a **valid, internally consistent, arithmetically checkable prediction** *within the UGP substrate*. PF cannot reproduce it from Axioms 1–3 + Postulate D because PF lacks the Braid-Atlas b-values, the `GF(7)`/GTE cascade, the Froggatt–Nielsen texture, and the GUT representation input. PF also cannot refute it, except by later producing its own PF-native number.

Therefore **PRED-003 remains `NOT YET BUILT`**. The kill-shot gap is unchanged: PF still needs a propagation-geometric mass-squared-difference generator plus a flavor/PMNS bridge plus a dimensional/scale closure. UGP’s number is a rival benchmark, not a PF-derived result.

---

## 7. References

| Ref | Source | Role |
|---|---|---|
| [PRED-003] | `/mnt/d/Fundamentals/PREDICTIONS/PRED-003-neutrino-mass-squared-ratio.md` | PF scoping, Route C toy probe, no-go summary. |
| [Comp] | `/mnt/d/Fundamentals/derivations/competitor_comparison_2026-08-02.md` | UGP 0.0294 vs NuFIT, N=3 comparison. |
| [README-C] | `/mnt/d/Fundamentals/PREDICTIONS/README.md` lines 173–203 | Rival check: UGP ratio is orthogonal to PF `Q_ν`. |
| [PhysCtx] | `/mnt/d/Fundamentals/PHYSICS_CONTEXT.md` §1.2–1.3 | PF’s God Equation, Koide, and Postulate D status. |
| [UGP-P21] | Spivack, *Neutrino Mass-Squared Ratio from the Braid Atlas*, Zenodo `10.5281/zenodo.20170120` / `10.5281/zenodo.20682687` (PDF downloaded this session to `/tmp/neutrino_masses_from_braid_atlas.pdf`) | Primary UGP derivation. |
| [NuFIT6] | Esteban et al., NuFIT 6.0, JHEP 12 (2024) 216, http://www.nu-fit.org/ | Experimental value used by UGP and PF. |

---

*This file is an angle-specific reverse-engineering report. It does not change PRED-003’s status, does not commit a number, and does not upgrade any claim tier. The Fundamentals PUBLIC HOLD remains in effect.*
