# CODEX AUDIT — PF Measurement Alignment Catalog
*2026-07-02 · Hostile Auditor: Codex · Method: Duck ("How do you know?")*

---

## EXECUTIVE SUMMARY

**Verdict: Catalog overstates alignment on 5 of 6 ALIGNS rows. All ALIGNS→FITS promotion paths require new physics derivations, not just "formalizing connections already found." The catalog's own structural premise (that ALIGNS means "PF structure is consistent but doesn't uniquely predict") is correct — but 4 rows don't even meet that standard. They are SILENT with decoration.**

| Row | Catalog Score | Codex Score | Overclaim? |
|-----|--------------|-------------|------------|
| Koide δ₀ ≈ 2/9 | 🟡 ALIGNS | 🟡 ALIGNS (honest) | No |
| Top ~172.5 GeV | 🟡 ALIGNS | 🟠 GAP / 🔴 SILENT | **Yes** |
| m_e/m_u ≈ 1/φ³ | 🟡 ALIGNS | 🔴 SILENT | **Yes** |
| sin²θ_W ≈ 0.231 | 🟡 ALIGNS | 🟡 ALIGNS (barely) | Borderline |
| Galactic rotation curves | 🟡 ALIGNS | 🟠 GAP | **Yes** |
| Tau g-2 prediction | 🟡 ALIGNS | 🟠 GAP until λ_c pinned | **Yes** |
| m_τ/m_e, m_μ/m_e | 🟠 GAP | 🟠 GAP (honest) | No |
| CKM δ (CP phase) | 🟠 GAP | 🔴 SILENT | **Yes** |
| α (fine structure) | 🟠 GAP | 🟠 GAP (honest) | No |
| Ω_c h² | 🟠 GAP | 🔴 SILENT (not in table but in summary) | Borderline |
| Ω_Λ | 🟠 GAP | 🟠 GAP (honest) | No |
| N=3→CP (Sakharov 2) | 🟠 GAP | 🟠 GAP (honest but threshold wrong) | No |

**Net: 4 confirmed ALIGNS→SILENT demotions, 1 GAP→SILENT demotion. Catalog's summary scorecard has arithmetic inconsistencies (7 ALIGNS advertised, 6 found; 6 GAPS advertised, 7 found).**

---

## METHOD

Duck method: for every ALIGNS or GAP, ask "How do you know?" If the connection is a reframing without a testable difference from Standard Model, flag as NOT EVIDENCE. Assume ALIGNS = SILENT until proven otherwise. The burden of proof is on the catalog.

**The key test:** "Does PF say something the Standard Model doesn't? Is it specific? Is it falsifiable? If 'PF says X is really Y' but Y makes identical predictions, it's a reframing, not a connection."

---

## ROW-BY-ROW AUDIT

---

### ALIGNS #1: Koide Phase δ₀ ≈ 2/9
**Catalog:** Section 1, Lepton masses. EMPIRICAL 0.65. ALIGNS.

**Verdict: ALIGNS is honest. No overclaim. Promotion blocked by missing phase selector.**

**PF connection stated honestly?** Yes. The catalog says "empirical match, no derivation" and "what PF doesn't say: why the phase is 2/9." CLAIMS.md is explicit: "the formal target remains open." The 2/9 ≈ δ_Koide numerical match is real (0.0033% error, p≈0). The catalog openly admits this is an empirical anchor, not a derivation.

**Confidence appropriate?** EMPIRICAL 0.65 is reasonable. The match exists, but no PF-native selector mechanism exists. Rivero filter, character-normal-form bridge, Chebyshev purity route, and Casimir selector scan all returned honest negatives. CLAIMS.md Section 6 documents these failures.

**What's missing for ALIGNS→FITS?** A PF-native phase selector. The 2/9 must emerge from PF's structure, not just be observed. Until then, stays ALIGNS. Not overclaimed.

**Bug note:** The catalog says "ALIGNS" but the thread workspace (MAP.md T2) is empty — "— (needs phase selector)." This is a genuine research gap, not a decoration.

---

### ALIGNS #2: Top Quark Mass ~172.5 GeV (Coherence Ceiling)
**Catalog:** Section 2, Quark masses. ARGUED 0.85. ALIGNS.

**Verdict: DEMOTED to 🟠 GAP. The coherence ceiling is a PF concept, not a PF prediction. Until λ_c or the ceiling mass is derived, it's a reframing.**

**PF connection stated honestly?** No. The catalog says "PF says: the top quark's short lifetime matches the coherence ceiling threshold — above ~173 GeV, the knot can't hold." But:

1. **"Coherence ceiling" is defined, not derived.** CLAIMS.md scores it ARGUED 0.80: "Max frequency where wavelength < coherence length (Axiom 3)." But Axiom 3 doesn't specify a numeric threshold. The ~173 GeV number is set BY the top quark mass, not derived FROM PF structure. The logic is circular: "the top mass is the coherence ceiling because the coherence ceiling is the top mass."

2. **λ_c is not pinned.** The λ_c scale formula is ARGUED 0.60 with N^(D/2) fit-selected. Without λ_c, the coherence ceiling has no independent numeric value. If λ_c changes, the "ceiling" floats.

3. **This is a reframing, not a connection.** PF says "the top quark decays fast because it's at the coherence ceiling." Standard Model says "the top quark decays fast because it's heavy and has a large phase space." Both agree it decays fast. The PF claim adds no new observable. To be a genuine connection, PF must predict: "a particle at mass X will decay in time Y because of coherence ceiling Z" where X, Y, Z are all derivable independently.

**Confidence appropriate?** ARGUED 0.85 is too high. The catalog itself says "MIN-3 in the roadmap" — meaning the derivation doesn't exist yet. An ARGUED claim that depends on an OPEN sub-problem can't carry 0.85.

**Promotion path (GAP→ALIGNS→FITS):**
- MIN-3: Derive λ_c from Axioms 1-3
- MIN-4: Derive the coherence ceiling threshold from λ_c
- MIN-5: Show this threshold independently matches 172.5 GeV
- Until MIN-3 closes, this stays GAP

**Overclaim flag: YES.** The catalog presents "coherence ceiling explains top mass" as an alignment when the ceiling is defined by the top mass. This is backwards.

---

### ALIGNS #3: m_e/m_u ≈ 1/φ³
**Catalog:** Section 2, Quark masses. EMPIRICAL 0.65. ALIGNS.

**Verdict: DEMOTED to 🔴 SILENT. This is a numerology coincidence flagged as PF-aligned. PF says nothing about this ratio — it's observed, not predicted.**

**PF connection stated honestly?** No. The catalog says "EMPIRICAL 0.65 — a real signal but a posteriori." CLAIMS.md says the same. The problem:

1. **The phrase "a posteriori" is doing all the work.** This is a 0.214% numerical coincidence found AFTER knowing the numbers. It is NOT a prediction. PF did NOT say "if our framework is correct, m_e/m_u should equal 1/φ³." Someone noticed the ratio is close and then... what?

2. **PF has no φ in its framework.** φ (the golden ratio) appears nowhere in Axioms 1-3, the Z₃ circulant, the Koide identity, or the Lean formalization. The ratio is geometric (pentagon/icosahedron) but PF is triadic (Z₃). No structural link exists.

3. **One free parameter.** The up quark mass is the least well-measured quark mass (MS-bar 2.2 ± 0.5 MeV at 2 GeV). A 0.214% "match" on a poorly-known quantity with one free parameter (the exponent 3) is numerology.

4. **What does "ALIGNS" mean here?** If "ALIGNS" means "there's a number that looks like another number," then every SILENT row with a close rational approximation would also be ALIGNS. The standard is being applied selectively.

**Confidence appropriate?** EMPIRICAL 0.65 is too high even for a coincidence claim. At p=0.007 (the catalog's own number, from a Monte Carlo with unclear trial factors), this is suggestive but not settled. With proper look-elsewhere correction, p would be higher.

**Promotion path (SILENT→ALIGNS→FITS):**
- Must show φ emerges from PF structure (not imported as a numerological curiosity)
- Must predict the ratio before measuring it (or explain why this ratio specifically)
- Until φ has a PF-native origin, stays SILENT

**Overclaim flag: YES.** The catalog has 5 quark masses scored SILENT and one coincidence scored ALIGNS. What distinguishes the coincidence? Nothing structural. This is pattern-matching dressed as alignment.

---

### ALIGNS #4: sin²θ_W ≈ 0.231 (Casimir Polynomial)
**Catalog:** Section 5, Gauge couplings. ARGUED 0.65. ALIGNS.

**Verdict: ALIGNS is defensible but borderline. The Casimir candidate is real but look-elsewhere P≈0.46 means this could easily be random.**

**PF connection stated honestly?** Mostly. The catalog notes: "what PF doesn't say: why the three gauge couplings have their specific values, why they nearly unify." CLAIMS.md is explicit: the Weinberg angle was demoted from DERIVED to ARGUED 0.65 after the look-elsewhere scan. The scheme selection and lack of PF-native origin for the Casimir polynomial are acknowledged.

**The real problem:**
1. **P(random target hits sub-percent) ≈ 0.46.** This means there's a ~46% chance a random Casimir target gets a match as good as 0.22310. This is barely above a coin flip. An alignment with 46% random-hit probability is not a confident alignment.

2. **The Casimir polynomial has no PF origin.** The spin pair (j=1/2, j=1) is selected by "minimal coherent representation principle" but the Casimir polynomial x² + C₂x - C₂ = 0 is imported from representation theory, not derived from PF axioms. PF didn't predict the Casimir structure — it's Standard Model group theory.

3. **Scheme selection is open.** On-shell vs MS-bar is not derived. The match is to the on-shell value, but which scheme is "correct" for PF is unknown.

**Confidence appropriate?** ARGUED 0.65 is technically within range, but the 0.46 random-hit probability makes this feel generous. A more honest confidence would be 0.40-0.50.

**Promotion path (ALIGNS→FITS):**
- Derive the Casimir polynomial structure from PF axioms (not import it from SU(2)×U(1))
- Derive scheme selection (why on-shell?)
- Close the look-elsewhere gap by showing the selected spin pair is unique under PF constraints
- Until then, stays ALIGNS (barely)

**Overclaim flag: BORDERLINE.** The catalog itself is honest about failures (T-022 negative, scheme selection open). But calling this ALIGNS with a 46% random-hit background is generous.

---

### ALIGNS #5: Galactic Rotation Curves (Cahill α)
**Catalog:** Section 7, Dark matter. ALIGNS. No CLAIMS.md row.

**Verdict: DEMOTED to 🟠 GAP. Cahill's work is external. PF has not validated it, tested it against counter-evidence, or derived it from PF axioms. Calling it "PF-adjacent" is not the same as PF having an account.**

**PF connection stated honestly?** Partially. The catalog says "Cahill's α (the coherence coupling) produces flat galaxy rotation curves without dark matter. This is a genuine PF-adjacent claim from Cahill's Process Physics, which PF has mapped as the coherence coupling constant." But:

1. **"PF-adjacent" ≠ PF.** Cahill developed Process Physics independently. PF later "mapped" Cahill's α as the coherence coupling constant. Mapping is not derivation. Has PF independently reproduced Cahill's rotation curve result from Axioms 1-3? No.

2. **The Bullet Cluster and CMB are strong counter-evidence.** The catalog itself admits this: "The evidence for particle dark matter (Bullet Cluster, CMB) is the strongest counter-argument. PF needs to engage with this, not handwave it." You can't score something ALIGNS while simultaneously noting that the strongest existing evidence contradicts it. That's not alignment — that's an unresolved contradiction.

3. **MOND-adjacent = known failure mode.** Modified gravity explanations for rotation curves (MOND, TeVeS, etc.) are well-studied and fail on cluster scales. PF's Cahill-α approach is MOND-adjacent but has not demonstrated cluster-scale success. The catalog flags this as a concern but scores ALIGNS anyway.

4. **No falsifiable PF prediction.** What does PF predict for rotation curves that MOND doesn't? What specific test distinguishes "Cahill α via PF medium" from "Cahill α via Process Physics" from "MOND"? If PF makes identical predictions to existing (falsified) theories, it inherits their falsification.

**Confidence appropriate?** No confidence score is even listed (no CLAIMS.md row). The catalog just says ALIGNS with no quantitative confidence. This is an empty score.

**Promotion path (GAP→ALIGNS→FITS):**
- Derive Cahill's rotation curve result from PF Axioms 1-3 without importing Cahill's framework
- Engage with Bullet Cluster and CMB with quantitative predictions
- Show a testable difference from MOND/TeVeS
- Until then: GAP

**Overclaim flag: YES.** The catalog scores as ALIGNS a connection to external work that PF has neither validated against counter-evidence nor derived from its own axioms. The dark_matter thread workspace itself says "α-only explanation must address [Bullet Cluster and CMB] or it's incomplete" — yet the catalog scores it ALIGNS. This is internally inconsistent.

---

### ALIGNS #6: Tau g-2 Prediction
**Catalog:** Section 10, Anomalous magnetic moments. ALIGNS. No CLAIMS.md row explicitly.

**Verdict: DEMOTED to 🟠 GAP. A genuine, falsifiable prediction exists IN PRINCIPLE, but the formula depends on λ_c (ARGUED 0.60) — making the prediction unfalsifiable until λ_c is pinned. A prediction you can't compute yet is a gap, not an alignment.**

**PF connection stated honestly?** Mostly. The catalog says "δa_τ = w_max / (m_τ / λ_c · (ħc)⁻¹). This is a genuine, specific, falsifiable prediction — but it depends on λ_c being pinned down first (MIN-3)." This is honest about the dependency. But:

1. **The prediction is not computable today.** λ_c = 1.157×10⁻¹⁸ m is ARGUED 0.60 with N^(D/2) fit-selected. If λ_c changes, δa_τ changes. Until λ_c is derived from Axioms 1-3, the tau g-2 "prediction" is "X depends on Y, and Y is unknown."

2. **w_max is undefined.** The thread workspace says "Determine what w_max is from PF's coherence ceiling framework." If λ_c isn't pinned AND w_max isn't defined, the "prediction" is a formula with two unknowns. That's not a prediction — it's a template for a prediction.

3. **No uncertainty budget exists.** Even if λ_c were known, the prediction needs propagated uncertainties. Without them, "agreement with Belle II" is undefined.

4. **Belle II can't measure tau g-2 yet at precision.** This makes the prediction a future test, not a current alignment. Scoring ALIGNS for a future test that might eventually exist is premature.

**Confidence appropriate?** No confidence score listed. ARGUED would be too high given λ_c dependency. This is more like OPEN→ARGUED after MIN-3.

**Promotion path (GAP→ALIGNS→FITS):**
- MIN-3: Pin λ_c with uncertainty
- MIN-3b: Define w_max from PF's coherence ceiling
- Compute δa_τ with full uncertainty budget
- Then it becomes ALIGNS (has a prediction) or FITS (prediction confirmed by Belle II)

**Overclaim flag: YES.** The catalog calls this "one of PF's strongest cards" but the prediction depends on two unknowns (λ_c, w_max) and can't be tested by current experiments. It's a promissory note, not a card.

---

### GAP #1: m_τ/m_e ratio (~3479)
**Catalog:** Section 1, Lepton masses. GAP.

**Verdict: GAP is honest. No overclaim. Gap closure requires deriving absolute mass scale.**

**Is the GAP stated honestly?** Yes. "Not derived." PF has Koide Q=2/3 (ratios) but not absolute masses.

**Gap closure requirements:**
- Derive the absolute mass scale of charged leptons
- This likely requires λ_c (MIN-3) plus a mechanism selecting m_e as the ground state
- Alternatively: derive that PF predicts mass ratios but absolute scale is a free parameter

**What's missing:** Everything. PF has the architecture (ratios) but not the scale.

---

### GAP #2: m_μ/m_e ratio (~207)
**Catalog:** Section 1, Lepton masses. GAP.

**Verdict: GAP is honest. Same scale problem as GAP #1.**

Actually, PF DOES have something here: the Koide formula with Q=2/3 and δ₀ gives m_e : m_μ : m_τ ratios if you know the absolute scale. But δ₀ is EMPIRICAL, not derived. So even the mass ratios beyond Q=2/3 are not fully derived.

**Gap closure:** Derive δ₀, then use Koide formula + scale to get m_μ/m_e.

---

### GAP #3: CKM δ (CP Phase) ~69° (1.2 rad)
**Catalog:** Section 3, CKM mixing. GAP.

**Verdict: DEMOTED to 🔴 SILENT. PF says N=3 → CP phase EXISTS but nothing about its VALUE. The catalog scores the phase value as GAP, but PF has NO thread on the phase magnitude. This is SILENT, not GAP.**

**Is the GAP stated honestly?** The catalog says "not derived." But:

1. **GAP implies PF has "threads but no account."** What threads? The catalog mentions "PF's equilateral resonance geometry" as a possible path, but this is pure speculation. No Lean theorem, no derivation attempt, no formalism exists connecting Z₃ to δ ≈ 1.2 rad.

2. **The N=3→CP bridge explicitly disclaims the phase magnitude.** The bridge document says: "This does NOT derive the CP phase magnitude. The CKM phase δ ≈ 1.2 rad (≈ 69°) is measured, not derived. PF has no account of its specific value." If PF explicitly says it has nothing on the value, scoring GAP is too generous.

3. **Distinguish from N=3→CP (Sakharov 2).** The structural bridge (N=3 → CP possible) is ARGUED 0.70 and is a genuine thread. But that's about EXISTENCE, not the VALUE. The CKM δ ≈ 69° row is about the VALUE. PF has no thread on the value. SILENT.

**Gap closure requirements (from SILENT):**
- Must go from Z₃ geometry to a specific CP phase value
- External preprint claims CKM reconstruction within 0.7σ — but this is not PF-validated
- Until PF has ANY thread on phase magnitude, stays SILENT

**Overclaim flag: YES.** Scoring GAP when PF has literally nothing on the specific value and the N=3→CP bridge explicitly disclaims the magnitude. This is a category error — confusing "CP violation possible" with "CP phase ≈ 69°."

---

### GAP #4: α (Fine Structure Constant) 1/137.036
**Catalog:** Section 5, Gauge couplings. GAP.

**Verdict: GAP is honest. The structural identification exists but derivation is OPEN.**

**Is the GAP stated honestly?** Yes. "No derivation." CLAIMS.md: α structural ID is ARGUED 0.60, numeric derivation is OPEN. The catalog notes: "PF reframes the question from 'why this value?' to 'what does this value tell us about the medium?' That's a reframing, not a derivation." This is honest.

**Gap closure requirements:**
- Derive λ_c from Axioms 1-3 (MIN-3)
- Derive m_e from topological defect ground state
- Compute α = √(18m_e/m_top) — but this depends on m_top/m_e being derived too
- The "route to derivation" mapped in alpha_from_pf.md is a multi-step chain, each step blocked

**What's missing:** The chain length is the problem. Each link (λ_c, m_e, m_top) is blocked. α derivation requires closing 3+ open problems.

---

### GAP #5: Ω_c h² = 0.120 (Dark Matter Density)
**Catalog:** Section 7, Dark matter. Listed as "not directly addressed" but scored GAP in some tables, SILENT in others.

**Verdict: This is 🔴 SILENT. The catalog itself says "not directly addressed." PF has no formalism, no model, no prediction for Ω_c h².**

**Catalog inconsistency:** The dark_matter thread workspace says: "🟠 GAP: Ω_c h² = 0.120 not directly addressed." But the catalog summary (line 187) says "0 GAP" for dark matter. The table says "not directly addressed." These contradict each other.

**If GAP:** PF has no threads. "Not directly addressed" = SILENT. Scoring GAP requires at minimum a research thread or formalism.

**Gap closure requirements (from SILENT):**
- Develop PF-native dark matter formalism (particle or modified gravity)
- Engage with Bullet Cluster and CMB
- Predict Ω_c h²

---

### GAP #6: Ω_Λ = 0.69 (Dark Energy)
**Catalog:** Section 8, Dark energy. GAP.

**Verdict: GAP is honest but thin. The "medium self-interaction energy" thread is a one-sentence speculation.**

**Is the GAP stated honestly?** Yes. "What PF says: Nothing directly. But the medium has a natural energy density. If the medium IS the vacuum, its self-interaction energy could manifest as the cosmological constant." The catalog openly admits PF has nothing.

**But is it really a GAP?** "The medium has a natural energy density" is not a thread — it's an observation that every quantum field theory makes (vacuum energy). PF adds nothing beyond "maybe our medium explains it." A genuine GAP thread would require at minimum: what sets the scale? Why ~10⁻¹²⁰ M_Planck?

**Gap closure requirements:**
- Derive Ω_Λ from medium properties (λ_c? energy density?)
- Address coincidence problem (why Ω_Λ ≈ Ω_matter now?)
- Predict w (equation of state)

---

### GAP #7: N=3 → CP Violation (Sakharov Condition 2)
**Catalog:** Section 9, Baryon asymmetry. GAP. ARGUED 0.70.

**Verdict: GAP is correct but the threshold is generous. This is a structural bridge, not a physics account. Scoring GAP rather than SILENT is defensible because a formal bridge document exists — but it addresses EXISTENCE, not SUFFICIENCY. The SM's CP violation is ~10 orders of magnitude too weak.**

**Is the GAP stated honestly?** Yes. "Today's bridge: N=3 generations → CP violation structurally possible. This addresses condition 2 at the level of possibility, not sufficiency. The SM's CP violation is too weak by ~10 orders of magnitude."

**But the catalog could be harsher:**
1. **Possibility ≠ mechanism.** Every 3-generation theory "predicts" CP violation is possible. PF's N=3 derivation adds nothing beyond: "we derive N=3, therefore CP violation is possible." But PF's N=3 derivation is CONDITIONAL 0.88 (rests on Postulate D). If Postulate D is wrong, PF loses both N=3 AND the CP bridge.

2. **The bridge is a syllogism, not a derivation.** "PF derives N=3. CKM with N=3 has a complex phase. Therefore PF predicts CP violation is possible." This is logic, not physics. The heavy lifting is in "PF derives N=3" — the rest is standard group theory.

3. **10 orders of magnitude too weak = the bridge is irrelevant to baryogenesis.** Even if PF is right that N=3 → CP possible, the SM's CP violation can't produce the observed baryon asymmetry. A bridge to insufficient CP violation answers the wrong question.

**Gap closure requirements:**
- Derive CP phase MAGNITUDE from Z₃ structure (not just existence)
- Show the PF-predicted CP violation is sufficient for baryogenesis
- Address Sakharov conditions 1 and 3 (B violation, non-equilibrium)

---

## CATALOG QUALITY ISSUES

### 1. Arithmetic Inconsistencies

The summary scorecard (lines 178-190) has multiple errors:

| Category | Catalog FITS/ALIGNS/GAP/SILENT | Actual from table |
|----------|-------------------------------|-------------------|
| Gauge couplings SILENT | 1 | **2** (α_s + unification) |
| Dark matter GAP | 0 | **1** (Ω_c h² → GAP in table) |
| Dark matter SILENT | 1 | **1** (Bullet Cluster) |
| Baryon asymmetry SILENT | 2 | **3** (η + Sakharov 1,3) |
| **Total ALIGNS** | **7** | **6** (counted from table rows) |
| **Total GAPS** | **6** | **7** (counted from table rows) |

These discrepancies suggest the catalog was written top-down (summary first, then table rows) without reconciliation. The claimed 7 ALIGNS appears to be an overcount — only 6 ALIGNS rows exist in the tables.

### 2. "ALIGNS" Definition Creep

The catalog defines ALIGNS as: "PF's structure is consistent with the measurement but doesn't uniquely predict it." But several ALIGNS rows don't even meet this:

- **m_e/m_u ≈ 1/φ³**: PF's structure has no φ. Not consistent — coincident.
- **Galactic rotation curves**: PF's structure is not consistent with Bullet Cluster (self-admitted). Counter-evidence exists.
- **Tau g-2**: PF's structure hasn't produced a computable prediction yet. Consistency unknown.

A better definition for ALIGNS should require:
1. PF structure → observable connection (not coincidence)
2. Connection is testable (not just a reframing)
3. No known counter-evidence (or counter-evidence addressed)

### 3. Confidence Inflation

Several rows cite confidence from CLAIMS.md but CLAIMS.md's own confidences embed dependencies:

| Row | Catalog Confidence | Actual CLAIMS.md Status | Dependency |
|-----|-------------------|------------------------|------------|
| Top quark | ARGUED 0.85 | ARGUED 0.85 | λ_c not derived |
| m_e/m_u | EMPIRICAL 0.65 | EMPIRICAL 0.65 | A posteriori, φ has no PF origin |
| sin²θ_W | ARGUED 0.65 | ARGUED 0.65 | P(random)≈0.46, scheme selection open |
| Tau g-2 | (unscored) | (no CLAIMS row) | λ_c (ARGUED 0.60) + w_max undefined |

When an ALIGNS depends on an OPEN sub-problem, the ALIGNS confidence should be capped at the sub-problem's confidence. A chain is only as strong as its weakest link.

### 4. The "Path Forward" Is Circular

The catalog's conclusion (line 218) says: "Category 1: Promote ALIGNS to FITS by formalizing the connections already found." This assumes the connections ARE found and just need formalization. Our audit shows most ALIGNS rows need NEW DERIVATIONS, not just formalization. "Formalizing" m_e/m_u ≈ 1/φ³ requires deriving φ from PF axioms — which is a new derivation, not formalization of an existing one.

---

## PROMOTION PATHS (HONEST)

### ALIGNS → FITS

| Row | Current | What It Actually Takes |
|-----|---------|----------------------|
| Koide δ₀ ≈ 2/9 | ALIGNS | PF-native phase selector (new derivation). Multiple attempts failed (Rivero, Chebyshev, Casimir). |
| Top quark ~172.5 GeV | **GAP** (demoted) | MIN-3 (derive λ_c) → MIN-4 (derive ceiling) → MIN-5 (match 172.5). Three open problems. |
| m_e/m_u ≈ 1/φ³ | **SILENT** (demoted) | Derive φ in PF from Z₃ structure (unlikely — φ is pentagonal, PF is triadic). |
| sin²θ_W ≈ 0.231 | ALIGNS | Derive Casimir structure from PF axioms + solve scheme selection + close look-elsewhere. |
| Galactic rotation curves | **GAP** (demoted) | Derive from PF axioms + address Bullet Cluster + address CMB + show PF-specific predictions. |
| Tau g-2 | **GAP** (demoted) | MIN-3 (λ_c) + define w_max + compute prediction with uncertainties. |

### GAP Closure

| Row | What It Takes |
|-----|--------------|
| m_τ/m_e, m_μ/m_e | MIN-3 (λ_c) + absolute mass scale derivation |
| CKM δ ≈ 69° | **Start from scratch.** No PF thread on phase magnitude. |
| α = 1/137.036 | MIN-3 + m_e derivation + m_top derivation (3+ open problems) |
| Ω_c h² = 0.120 | **Start from scratch.** No PF dark matter formalism. |
| Ω_Λ = 0.69 | Medium energy density formalism + scale setting + coincidence |
| N=3→CP (Sakharov 2) | CP phase MAGNITUDE + baryogenesis mechanism + B violation + non-equilibrium |

---

## BOTTOM LINE

**The catalog is a useful scaffolding but overstates PF's measurement coverage.** Of 6 ALIGNS rows, only 2 survive hostile audit (Koide δ₀ and sin²θ_W — and the latter barely). The remaining 4 are SILENT or GAP with PF-aligned decoration.

**The honest scorecard:**

| Category | FITS | ALIGNS | GAP | SILENT |
|----------|------|--------|-----|--------|
| Lepton masses | 1 (Koide Q) | 1 (δ₀) | 2 | 0 |
| Quark masses | 0 | 0 | 1 (top ceiling) | 6 |
| CKM mixing | 0 | 0 | 0 | 5 (incl. δ) |
| PMNS mixing | 0 | 0 | 0 | 6 |
| Gauge couplings | 0 | 1 (sin²θ_W) | 1 (α) | 2 |
| Higgs | 0 | 0 | 0 | 2 |
| Dark matter | 0 | 0 | 1 (Cahill α) | 2 (incl. Ω_c) |
| Dark energy | 0 | 0 | 1 (Ω_Λ) | 1 |
| Baryon asymmetry | 0 | 0 | 1 (N=3→CP) | 3 |
| g-2 | 0 | 0 | 0 | 3 |
| **TOTAL** | **1** | **2** | **7** | **30** |

**1 FITS. 2 ALIGNS. 7 GAPS. 30 SILENT.**

That's the honest picture. The Koide identity remains PF's single genuine FITS. Everything else is work to be done — not alignment achieved.

---

*Codex · Hostile audit complete · The Duck asks: "How do you know?" · The answer, for most of these rows, is: "We don't yet."*
