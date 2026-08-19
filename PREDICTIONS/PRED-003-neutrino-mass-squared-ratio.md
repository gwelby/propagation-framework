# PRED-003 — PF-Native Derivation of the Neutrino Mass-Squared Ratio

**Status:** NOT YET BUILT / SCOPING — no locked number, no pre-registration hash  
**Date:** 2026-08-18  
**Agent:** Devin ∇λΣ∞  
**Authority tier:** advisory — this file is a route map, not a truth claim  
**Public hold:** yes — Fundamentals PUBLIC HOLD remains in effect until Codex recheck clears

---

## 1. Why this is the kill shot

The `UNDENIABLE_ROADMAP.md` defines the kill shot as *one quantity where*:

| Criterion | PRED-003 status |
|---|---|
| (a) The Standard Model is silent | **YES** — SM has no neutrino mass-pattern prediction |
| (b) PF makes a specific number | **NO** — no PF-native derivation exists yet |
| (c) A named rival predicts a *different* number | **YES** — UGP predicts 0.0294 from GF(7) arithmetic |
| (d) Feasible within ~10 years | **YES** — the ratio is already measured (NuFIT 6.0) |

PRED-002 (Q_ν ≠ 2/3) fails criterion (c): all primary rivals (Brannen, Rivero, ZiP) agree that standard Q_ν ≠ 2/3. It is a valid forward prediction but **not discriminating**. PRED-003 is the only live candidate that would let PF compete head-to-head with UGP on a *different* number. <ref_snippet file="/mnt/d/Fundamentals/UNDENIABLE_ROADMAP.md" lines="30-34" />

---

## 2. The target observable

**Quantity:**  
```
r_ν = Δm²₂₁ / Δm²₃₁
```

- **Δm²₂₁** — solar mass-squared splitting (measured by reactor/long-baseline experiments)
- **Δm²₃₁** — atmospheric mass-squared splitting (measured by atmospheric/long-baseline experiments)

**Measured value (NuFIT 6.0, normal ordering):**
- Δm²₂₁ = 7.49 × 10⁻⁵ eV²
- Δm²₃₁ = 2.534 × 10⁻³ eV²
- **r_ν = 0.02951 ± 0.00098**
- Source: http://www.nu-fit.org/?q=node%2F294

**UGP prediction:**  
- r_ν = 0.0294 (parameter-free, from GF(7) cellular-automaton arithmetic)
- Agreement with NuFIT 6.0: ~0.16σ
- UGP does **not** predict Q_ν; PF does **not** predict r_ν. The two observables are orthogonal. <ref_snippet file="/mnt/d/Fundamentals/PREDICTIONS/README.md" lines="173-203" />

**PF current behavior:**  
PF takes Δm²₂₁ and Δm²₃₁ as measured inputs. They are used in `neutrino_koide_scan.py` and `pred002_mc_stdlib.py` to compute Q_ν. The ratio is an **input**, not an **output** of any PF derivation. <ref_snippet file="/mnt/d/Fundamentals/PREDICTIONS/README.md" lines="179-195" />

---

## 3. Transfer contract (per MEDIUM_TRANSFER_LAYER)

Before this can be called a derived prediction, every field below must be filled. Fields marked `???` are open and block promotion.

| Field | Current state |
|---|---|
| **Name** | PRED-003: neutrino mass-squared ratio from PF propagation axioms |
| **Source domain** | PF axioms (Axioms 1–3), Postulate D, Z₃ circulant algebra, D=3/N=3 selection |
| **Source structure** | God Equation spectrum {1, −1/8, −1/8}; Koide P₀/Q decomposition; Circulant3 residue eigenvalues; equal-weight coupling |
| **Source dynamics** | T³ residue contraction; stability selection of D=3; N=3 unique residue spectrum |
| **Target domain** | Neutrino flavor/mass physics |
| **Target observable** | r_ν = Δm²₂₁ / Δm²₃₁ |
| **Expected output structure** | A single positive real number, with a falsifiable uncertainty band, independent of measured Δm² inputs |
| **Medium** | The propagation Medium; the mechanism by which PF mass eigenstates acquire their values |
| **Coupling map** | ??? — no named map from abstract PF eigenvalues to eV-scale mass-squared differences |
| **Coarse-graining / measurement map** | ??? — no map from PF residue modes to SM neutrino mass eigenstates |
| **Entropy / cost functional** | ??? — no named cost that selects one splitting over another |
| **Resolution / observer limits** | ??? — no named observer or finite-resolution channel |
| **Null model** | The mass-squared differences are free Lagrangian parameters (the SM view), not determined by propagation geometry |
| **Survival metric** | A PF-native derivation yields a number consistent with NuFIT 6.0 within its uncertainty |
| **Residual / noise metric** | The prediction's uncertainty must come from PF structural choices, not from m_lightest or oscillation experiments |
| **Falsifier** | A derived r_ν that deviates from NuFIT 6.0 by >3σ, or no derivation at all |
| **Evidence files** | This scoping document, `competitor_comparison_2026-08-02.md`, `PREDICTIONS/README.md` §C |
| **Lean status** | No theorem connects PF axioms to Δm². `Circulant3Spectrum.lean` explicitly disclaims any mass/Koide/PRED-003 transfer. |
| **Simulation status** | No PF-native numerical derivation of r_ν exists. |
| **Hardware / empirical status** | None. The target is already measured by oscillation experiments; PF has no independent measurement proposal. |
| **Claim tier** | **SCOPING / HYPOTHESIS** — not DERIVED, not CONDITIONAL, not a locked prediction |

---

## 4. Candidate routes and their blockers

### Route A — God Equation eigenvalue → mass ratio

**What PF has:**  
`GodEquationSpectrum.lean` proves that N = 3 is the unique cycle whose full residue spectrum is {−1/8, −1/8}. Given Postulate D, the three-step closure operator T³ has eigenvalues {1, −1/8, −1/8}. `ArbitraryD.lean` and `GodEquationGap.lean` show D = 3 is the unique stable dimension for the J−I operator.

**Blocker:**  
The eigenvalues {1, −1/8} are dimensionless algebraic numbers. There is no transfer contract that maps them to eV² mass-squared differences. The λ_c scale formula `√2·l_P·exp(4π²N^(D/2)/b₀)` uses N = 3, D = 3 fit-selected to match the top Compton wavelength; `GodEquationGap.lean` labels this **fit-selected, not derived**. <ref_snippet file="/mnt/d/Fundamentals/lean/PfLean/GodEquationGap.lean" lines="21-35" />

### Route B — Koide ansatz → mass ratio

**What PF has:**  
`KoideGeometry.lean` proves Q = 2/3 from the standard Koide formula. `KoideSelection.lean` shows the P₀/Q decomposition and the Z₃ cosine identity that makes it work.

**Blocker:**  
The Koide ansatz itself is not derived from Axioms 1–3. Even if it were, Q_ν is a *different* observable from r_ν. Moving from Q_ν to r_ν requires additional assumptions about the absolute scale, the phase δ, and the mass ordering. PRED-003 is a separate prediction, not a repair of PRED-002. <ref_snippet file="/mnt/d/Fundamentals/lean/PfLean/KoideSelection.lean" lines="63-79" />

### Route C — Circulant3Spectrum residue → mass ratio

**What PF has:**  
`Circulant3Spectrum.lean` proves the closed-form spectrum of real D=3 circulants, the eigenrelation, and negative controls. The symmetric member (b = c) uniquely minimizes the contraction factor.

**Blocker:**  
The file header explicitly states: *"No physical interpretation, no arrow of time, no mass identification, no Koide/PRED-003 transfer."* The parameters `b` and `c` are free real numbers; nothing fixes them to physical neutrino masses. <ref_snippet file="/mnt/d/Fundamentals/lean/PfLean/Circulant3Spectrum.lean" lines="1-19" />

### Route D — D=3 / N=3 uniqueness → mass ratio

**What PF has:**  
`Z3FromBareMedium.lean` and `GodEquationSelection.lean` sharpen why D = 3 and N = 3 are selected structurally.

**Blocker:**  
Selection of 3 spatial dimensions and 3 generations does not determine the *splitting* between mass eigenstates. The number of modes is not the same as their eigenvalues. This route gives cardinality, not mass ratios.

### Route E — UGP-style arithmetic route

**What the rival does:**  
UGP derives 0.0294 from GF(7) arithmetic. PF does not have an equivalent finite-field or cellular-automaton substrate.

**PF blocker:**  
PF's substrate is propagation geometry, not finite-field arithmetic. Copying UGP's route would not be a PF-native derivation. A PF number must come from Axioms 1–3 + named posits, not from an imported rival ansatz.

---

## 5. Missing pieces (no-go until closed)

1. **Mass scale bridge** — How does PF produce an eV-scale number? `PREMISE_LEDGER.md` Entry 004 notes that λ_c is calibrated to the top Compton wavelength, not derived from Axioms 1–3. A neutrino mass-squared difference in eV² requires a scale. <ref_snippet file="/mnt/d/Fundamentals/PREMISE_LEDGER.md" lines="103-122" />

2. **Flavor/PMNS bridge** — How do PF residue modes map to the three SM neutrino mass eigenstates? There is no named identification of PF's Z₃ channels with ν_e, ν_μ, ν_τ or with mass eigenstates m₁, m₂, m₃.

3. **Mass-squared-difference generator** — What PF mechanism produces two distinct positive numbers Δm²₂₁ and Δm²₃₁? The God Equation gives one residue eigenvalue −1/8 (twofold degenerate). It does not naturally produce two different splittings.

4. **Ordering/phase independence** — The ratio r_ν is independent of the absolute scale, but a derivation must still produce both numerator and denominator from a common source. The phase δ in the Koide ansatz (and the PMNS CP phase) is currently an open degree of freedom.

5. **Dimensional closure** — Any mass formula must be dimensionally closed. `PREMISE_LEDGER.md` Entry 001 (lepton g-2) shows that PF has previously produced dimensionally inconsistent formulas. A PRED-003 derivation must be checked for dimensional closure from the start.

---

## 6. Concrete next step: a bounded probe

Do **not** start by guessing a number. Start by building the smallest possible transfer model and trying to falsify it.

### Step 1 — Choose one candidate route

The best starting point is **Route C** (Circulant3Spectrum), because:
- It has the most recent Codex-audited Lean formalization.
- It has explicit free parameters `b` and `c` whose ratio could be interpreted as a mass ratio.
- The file already disclaims physical transfer, so a failed probe is an honest no-go.

### Step 2 — Write a toy map

Hypothesis (to be tested, not asserted):
```
Δm²₂₁ / Δm²₃₁  ⇌  f(b, c)  for some function f on the circulant parameters
```
Candidate: the squared-modulus ratio of residue eigenvalues, or the contraction-factor ratio. The simplest is:
```
r_PF(b, c) = |λ₁(b, c)|² / |λ_uniform|²
```
At the symmetric point b = c = 1/2 this gives |λ|² = 1/4, so the ratio to the uniform eigenvalue 1 is 1/4 — not 0.0294. The probe will almost certainly fail; that is the point.

### Step 3 — Run the probe

Create a Python or Lean probe that:
1. Picks a one-parameter slice of the Circulant3 family.
2. Computes the resulting r_PF.
3. Compares it to 0.02951.
4. Varies the interpretation (squared modulus, real part, imaginary part, contraction factor, etc.).

Expected result: **no natural interpretation of the free circulant parameters reproduces 0.02951 without additional structure.** Document the no-go.

### Step 4 — If the probe fails, report what is missing

The output of the probe is not a number. It is a list of missing transfer-contract fields (scale bridge, flavor bridge, mass-squared-difference generator, etc.). This scoping document is then updated with the no-go evidence.

### Step 5 — If the probe succeeds, escalate immediately

If any interpretation yields 0.02951 with a clean derivation, do the following **before** calling it a prediction:
1. Write the explicit transfer contract.
2. Make the derivation Lean-verifiable or at least reproducible.
3. Send it to Codex hostile audit.
4. Pre-register a SHA-256 commitment with a named resolution window.

### 6.1 Route C probe — initial no-go (2026-08-18)

A toy Python probe was run on the normalized slice `b + c = 1` of the D=3 circulant family: `sandbox/pred003_circulant3_probe.py`.

**Method:**
- Residue eigenvalue: `λ = b·ω + c·ω²`, `|λ|² = (b+c)²/4 + 3(b-c)²/4`
- Uniform eigenvalue: `u = b + c = 1`
- Tested four naive interpretations of the ratio `r_ν`:
  1. `r1 = |λ|² / u` — residue contraction factor over uniform mode.
  2. `r2 = Im(λ)² / Re(λ)²` — squared imaginary-to-real ratio.
  3. `r3 = (b-c)² / (b+c)²` — normalized asymmetry squared.
  4. `r4 = (b-c) / (b+c)` — normalized asymmetry.

**Key results (target r_ν = 0.02951 ± 0.00098):**

| Candidate | Best-fit (b, c) | r_PF | Distance from target |
|---|---|---|---|
| r1 = |λ|² / u | (0.5000, 0.5000) — the H17 symmetric point | 0.25000 | 224.99σ |
| r2 = Im² / Re² | (0.4500, 0.5500) — off-symmetry, ad hoc | 0.03000 | 0.50σ |
| r3 = (b-c)² / (b+c)² | (0.4000, 0.6000) — off-symmetry, ad hoc | 0.04000 | 10.70σ |
| r4 = (b-c) / (b+c) | (0.5000, 0.5000) — symmetric, zero asymmetry | 0.00000 | 30.11σ |

**Interpretation:**
- The *natural* selected point `b = c = 1/2` (H17 symmetry) gives `r1 = 0.25` — **225σ away** from the measured ratio. This is the no-go for the simplest eigenvalue-ratio interpretation.
- Candidates r2 and r3 *can* be tuned to land near 0.0295, but only by choosing an arbitrary off-symmetry `b ≠ c`. No PF axiom or theorem selects that value. The match is a fit, not a derivation.
- Candidate r4 cannot even be tuned to a positive value at the symmetric point; it would require an additional sign convention with no PF source.

**Conclusion:**  
Route C does not survive a first-contact probe. The residue eigenvalue algebra is internally consistent, but it does not naturally output the measured mass-squared ratio. The missing pieces identified in §5 (mass-scale bridge, flavor/PMNS bridge, mass-squared-difference generator, ordering/phase selector, dimensional closure) remain open.

This is a **toy no-go**, not a formal impossibility theorem. A real no-go would require a Lean theorem showing that no PF-derived, dimensionally closed map from the circulant family to the neutrino mass-squared ratio can reproduce 0.02951. That is beyond this scoping session.

---

## 7. What this is not

- **This is not a locked prediction.** No pre-registration hash has been computed. The file is a scoping and route-map document.
- **This is not a claim that PF can derive r_ν.** It is an honest map of the open gaps.
- **This is not a repair of PRED-002.** The mass-squared ratio is an *input* to PRED-002's Q_ν calculation, not its output. PRED-002 and PRED-003 are separate predictions.
- **This is not outreach material.** PUBLIC HOLD on Fundamentals remains in effect.

---

## 8. References

| File | Role |
|---|---|
| `UNDENIABLE_ROADMAP.md` | Kill-shot criteria and strategic context |
| `WHATS_NEXT.md` | PRED-003 named as highest-value open target |
| `PREDICTIONS/README.md` | UGP rival check, transfer-contract template, PRED-002 context |
| `derivations/competitor_comparison_2026-08-02.md` | UGP 0.0294 source and head-to-head comparison |
| `lean/PfLean/Circulant3Spectrum.lean` | Codex-audited D=3 circulant algebra, explicit no-transfer disclaimer |
| `lean/PfLean/GodEquationGap.lean` | Honest gaps: Postulate D, N^(D/2) fit-selection, H_prod |
| `lean/PfLean/KoideSelection.lean` | Koide ansatz, P₀/Q decomposition, equal-weight coupling |
| `lean/PfLean/Axioms.lean` / `Axiom1ToH12.lean` | What is and is not derived from Axioms 1–3 |
| `PREMISE_LEDGER.md` | Cross-cutting premise gaps, including mass scale and dimensional closure |
| `MEDIUM_TRANSFER_LAYER.md` | Cross-domain bridge protocol used for this scoping contract |
| `sandbox/pred003_circulant3_probe.py` | Toy Route C sweep (2026-08-18); not a derivation or a locked prediction |
| `PREDICTIONS/PRED-003-route-A-probe.md` | Route A no-go: God Equation eigenvalue / scale bridge |
| `PREDICTIONS/PRED-003-route-B-probe.md` | Route B conditional/fit: Koide ansatz probe |
| `PREDICTIONS/PRED-003-route-D-probe.md` | Route D no-go: D=3/N=3 selection and splitting degeneracy |
| `PREDICTIONS/PRED-003-ugp-reverse.md` | Route U: UGP GF(7) 0.02936 derivation reverse-engineer |
| `Spivack 2026 (Zenodo 10.5281/zenodo.20170120 / 20682687)` | Primary UGP source on the neutrino mass-squared ratio |
| `sandbox/pred003_route_A_toy.py` | Toy God Equation scale-bridge calculation |
| `sandbox/pred003_route_B_toy.py` | Toy Koide (β,δ) grid scan |
| `lean/PfLean/Z3FromBareMedium.lean` | D=3 uniqueness and circulant degeneracy |
| `lean/PfLean/GodEquationSelection.lean` | N=3 selection among cycles |
| `lean/PfLean/KoideUnlocked.lean` | Generalized `Q(β)` and falsified `β ↔ −1/8` cross-links |
| `derivations/god_eq_q_sector_basis_selection_2026-04-02.md` | Q-sector degeneracy protection (C₃ invariance) |
| `derivations/selection_boundary_synthesis_2026-05-08.md` | Degeneracy-breaking vacuum selector (candidate only) |

---

## 9. Multi-angle probe results and cross-route discussion (2026-08-18)

Four subagents were dispatched in parallel to probe the candidate PRED-003 routes (Blackboard thread `pred003-multi-angle`). A fifth, the UGP reverse-engineer, is still running. This section is the cross-route discussion: what each route found, how they talk to each other, and where they converge.

### Verdict summary

| Route | Question | Verdict | Key file |
|---|---|---|---|
| C — Circulant3Spectrum | Does any natural eigenvalue-ratio interpretation of the D=3 circulant free parameters yield `r_ν`? | **NO-GO** | §6.1 and `sandbox/pred003_circulant3_probe.py` |
| A — God Equation scale bridge | Can the exact spectrum `{1, −1/8, −1/8}` plus a single PF-derived scale produce `r_ν`? | **NO-GO** | `PREDICTIONS/PRED-003-route-A-probe.md` |
| B — Koide ansatz | Does the Koide ansatz, with PF anchors `δ = 2/9` or `β = √2`, derive `r_ν`? | **CONDITIONAL / FIT** | `PREDICTIONS/PRED-003-route-B-probe.md` |
| D — D=3 / N=3 selection | Does the uniqueness of 3 dimensions and 3 generations determine the mass-squared splitting? | **NO-GO** | `PREDICTIONS/PRED-003-route-D-probe.md` |
| U — UGP reverse | How does UGP get `0.0294` from GF(7), and can PF either reproduce or structurally refute it? | **REPORT / CONDITIONAL** | `PREDICTIONS/PRED-003-ugp-reverse.md` |

### Cross-route discussion

The four completed routes converge on one structural fact: **PF has the right number of modes (three) and the right degenerate residue eigenvalue (`−1/8`), but it has no mechanism to split that degeneracy, no eV-scale bridge, and no map to the SM neutrino mass eigenstates.** Each route illuminates the same missing pieces from a different direction.

**Route C — Circulant3Spectrum**  
The free circulant parameters `b, c` have a natural selected point at `b = c = 1/2` (H17 symmetry). That point gives a residue contraction `r_PF = |λ|² / uniform = 0.25`, which is **225σ** away from the measured `0.02951`. Other functions of `(b, c)` can be tuned to hit the target, but only by choosing an arbitrary off-symmetry `(b, c)`. No PF axiom selects that choice.

**Route A — God Equation scale bridge**  
The exact spectrum `{1, −1/8, −1/8}` is a beautiful algebraic result, but a single scale `s` cannot serve both splittings:
- If `m_i² = s·|e_i|`, the two residue modes are degenerate, so `Δm²₂₁ = 0`.
- If we try to map the residue to one splitting at a time, the solar scale is `s_solar ≈ 6 × 10⁻⁴ eV²` and the atmospheric scale is `s_atm ≈ 2 × 10⁻² eV²`. They differ by `r_ν` itself — the same eigenvalue cannot be the source of both.
- The PF `λ_c` formula is anchored to the top-quark Compton wavelength (`~170 GeV`). The neutrino scale is `~10⁻² eV`. The required suppression is `10²⁴–10²⁵`, or roughly **26–27 powers of `1/8`** — not a small, PF-derived number.

**Route D — D=3 / N=3 selection**  
This is the *formal* reason behind Route A's numerical failure. `Z3FromBareMedium.lean` and `GodEquationSelection.lean` prove that D=3 and N=3 are unique, but the theorems fix **cardinality and degeneracy**, not mass-squared values. The Q-sector degeneracy `μ₁² = μ₂² = m² + κ` is protected by C₃ symmetry (`god_eq_q_sector_basis_selection_2026-04-02.md`, lines 175–187). A toy traceless perturbation of the 2D residue block needs magnitude `ρ ≈ 0.0588` — about **47% of the residue magnitude `1/8`** — to reproduce `r_ν`. The D=3/N=3 algebra does not select `ρ`, and the orientation of the perturbation is also undetermined.

**Route B — Koide ansatz**  
Route B is structurally different. The Koide ansatz has enough freedom (`β, δ, m̄`) that it can **fit** the measured ratio in thousands of places (2146 grid points within 3σ). But none of the PF anchors land there:
- Charged-lepton anchor `β = √2`, `δ = 2/9` → `r = 0.003535` (26.5σ off).
- Measured neutrino `Q_NO = 0.55` with `δ = 2/9` → `r = 0.009494` (20.4σ off).
- Best fit on the `δ = 2/9` line requires `β ≈ 0.799` (`Q ≈ 0.44`), which no PF principle predicts.
- Full-grid best fit `β ≈ 1.154`, `δ ≈ 0.398 rad` gives the target, but is selected by neither `Q = 2/3` nor `δ = 2/9`.

**The common root cause: the mass-squared-difference generator is missing.**  
All four routes need the same new object — a PF-native rule that:
1. lifts the twofold `−1/8` residue degeneracy into two distinct mass-squared values;
2. supplies an eV-scale absolute magnitude independent of the top-Compton `λ_c`;
3. identifies the resulting modes with `m₁, m₂, m₃` in the correct PMNS/ordering convention.

Route C shows the circulant parameters cannot be this object. Route A shows the God Equation eigenvalues cannot be, because the scale is wrong and the residue is degenerate. Route D proves the degeneracy is protected by symmetry and that any splitting requires a new, un-named perturbation. Route B shows that even if a splitting formula is *assumed*, PF has no selector that fixes the point.

### UGP comparison — result

Route U inspected the primary UGP source: Nova Spivack, *Predicting the Neutrino Mass-Squared Ratio from the Braid Atlas Topological Invariants and the QCD Colour Rank* (2026), Zenodo `10.5281/zenodo.20170120` / `10.5281/zenodo.20682687`. The exact arithmetic is:

```
r_UGP = (11^{58/9} − 5^{58/9}) / (19^{58/9} − 5^{58/9}) = 0.029357… ≈ 0.02936
```

with right-handed-neutrino Braid-Atlas b-values `{5, 11, 19}` and power-law exponent `29/9 = N_c + θ_Koide = 3 + 2/9`. The number was independently verified in Python.

**How UGP gets `29/9`:** it claims three structural decompositions of the integer `29`:
```
29 = N_c³ + s = 4 N_c² − δ = dim(45_SU(5)) − dim(16_SO(10))
```
where `s = 2` (strand count), `δ = 7` (mirror offset), and `45 − 16 = 29` (GUT representation defect), with `N_c = 3` and Froggatt–Nielsen texture `(q₁, q₂) = (3, 2)` selected by MDL. Then `29/9 = N_c + 2/9`.

**Can PF reproduce it?** No — not without importing UGP's substrate. PF has no Braid-Atlas b-values, no `GF(7)`/GTE cascade, no power-law on a generation index, no Froggatt–Nielsen texture, no SO(10) representation input, and no seesaw `M_R` cancellation.

**Can PF refute it?** No — PF has no competing PF-native number. The only honest statement is that `0.02936` does not follow from Axioms 1–3 + Postulate D.

**Implication for PRED-003:** UGP's number is a **valid, internally consistent, arithmetically checkable prediction within the UGP substrate**. For PF it is an **external benchmark**. PRED-003 remains unbuilt.

---

## 10. What remains after the multi-angle sweep

PRED-003 remains **NOT YET BUILT**. The transfer contract in §3 is still mostly `???`. The multi-angle sweep has turned those question marks into **evidenced no-go / conditional statements** for five routes:

1. **The `−1/8` residue degeneracy is a real, symmetry-protected obstacle.** It is not an accident; it is the Z₃ signature of N=3.
2. **The `λ_c` / top-Compton scale is the wrong scale for neutrinos.** The neutrino mass scale is `10²⁴–10²⁵` times smaller.
3. **The Koide ansatz can fit, but not derive, `r_ν`.** The measured ratio is one point in a large `{(β, δ, m̄)}` family; no PF principle selects it.
4. **Routes C and D are structurally linked.** Route C is the free-parameter failure; Route D is the formal symmetry reason behind it.
5. **UGP's `0.02936` is a valid rival benchmark but not derivable in PF.** It comes from a Braid-Atlas / `GF(7)` / GUT-representation substrate that PF does not have. PF cannot reproduce or refute it on PF grounds.
6. **All five routes need the same new object.** A real PRED-003 derivation requires a **mass-squared-difference generator**, a **flavor/PMNS bridge**, a **dimensional/scale closure**, and a **degeneracy-breaking rule**. None exists today.

**Honest next step:** The sweep is complete enough to show that *more route variations are unlikely to help*. The next productive move is to design **one candidate object** that closes all four gaps at once, or to prove that no object derivable from Axioms 1–3 + Postulate D can do so.

---

## 11. Sign-off gate (PRED-003 → OPEN)

Before this becomes an OPEN prediction with a locked number, all of the following must hold:

- [ ] A PF-native derivation of r_ν exists (Lean theorem or explicit, reproducible Python/algorithm).
- [ ] The `conditional_on` field names every premise: Postulate D, H7/H12/H17/H18, stability, and any new premise introduced.
- [ ] `rivals_say` is filled with UGP 0.0294 and any other named rival's prediction, with primary-source verification.
- [ ] `sm_says` is "silent" with explicit justification.
- [ ] A falsifier and a named resolution window / experiment are specified.
- [ ] The prediction is pre-registered with a SHA-256 hash and committed to git.
- [ ] Codex hostile audit passes.
- [ ] The file is reviewed by a second agent or by Greg.

Until all gates are met, PRED-003 remains **NOT YET BUILT**.
