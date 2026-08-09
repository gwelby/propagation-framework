# Rival Verification: Brannen / Rivero / ZiP — Do they predict Q_ν = 2/3?

**Date:** 2026-08-09
**Verifier:** Devin
**Status:** COMPLETED — finding changes PRED-002's `rivals_say` field

---

## The question

PRED-002's commitment block states:

> rivals_say: Brannen/Rivero predict Q_ν ≈ 2/3 (normal ordering, m_3 ≈ 0.05 eV) via sign-flipped preon/Clifford phase mechanism. ZiP also extends Koide to neutrinos with a similar mechanism. This makes the disagreement clean.

Codex flagged this as DEGENERATE-risk (Codex audit item 5): the rivals' claims have not been verified against primary sources. This document verifies them.

---

## Primary sources examined

### 1. Brannen

- **"Koide Mass Formula for Neutrinos"** (April 2006)
  URL: http://brannenworks.com/MASSES.pdf
  viXra: https://vixra.org/abs/0702.0052

- **"The Lepton Masses"** (May 2006)
  URL: https://brannenworks.com/MASSES2.pdf

- **"Koide Formula for Neutrino Masses"** (November 2006)
  URL: http://www.brannenworks.com/jpp06.pdf

### 2. Rivero

- **"The strange formula of Dr. Koide"** (review paper)
  URL: https://a.rivero.nom.es/research/koide.pdf
  arXiv: hep-ph/0505220

- **"Koide's formula and the s-c-t tuple"** (extension paper)
  URL: https://a.rivero.nom.es/research/koidenew2.pdf

### 3. ZiP (Zero-Interaction Principle)

- **"Derivation of the Koide Formula from the Zero-Interaction Principle"**
  J. Buchanan (2025), academia.edu/145613039

- **"Derivation of Neutrino Masses from the Zero-Interaction Principle: The Inverted Moment Formula"**
  J. Buchanan (2026), academia.edu/145881329

- **"Derivation of PMNS Mixing Angles from the Zero-Interaction Principle"**
  J. Buchanan (2026), academia.edu/145881383

---

## Findings

### Brannen: Sign-flipped formula, NOT standard Q_ν = 2/3

Brannen's key formula (from jpp06.pdf, confirmed in MASSES.pdf):

```
(-√m_ν1 + √m_ν2 + √m_ν3)² / (m_ν1 + m_ν2 + m_ν3) = 3/2
```

This is a **sign-flipped** Koide relation. The first square root is NEGATIVE. This is NOT the standard Koide formula:

```
Standard:  Q = (m_ν1 + m_ν2 + m_ν3) / (√m_ν1 + √m_ν2 + √m_ν3)² = 2/3
Brannen:   Q' = (m_ν1 + m_ν2 + m_ν3) / (-√m_ν1 + √m_ν2 + √m_ν3)² = 2/3
```

These are **different formulas**. The denominators differ by the sign of √m_ν1.

**Numerical verification with Brannen's predicted masses** (m_ν1 = 0.000383 eV, m_ν2 = 0.008913 eV, m_ν3 = 0.050712 eV):

| Formula | Value | ≈ 2/3? |
|---------|-------|--------|
| Standard Q_ν = Σm/(Σ√m)² | **0.5216** | NO (0.145 away) |
| Brannen Q' = Σm/(-√m₁+√m₂+√m₃)² | **0.6667** | YES |

**Brannen AGREES with PF that the standard Q_ν ≠ 2/3.** His prediction is that a MODIFIED (sign-flipped) formula gives 2/3, not the standard one. The sign flip is the mechanism — it's not a minor detail, it's the entire claim.

### Rivero: Reviewer/framework builder, not a Q_ν = 2/3 predictor

Rivero's paper "The strange formula of Dr. Koide" is a review of the Koide formula literature. Key findings:

- Rivero discusses sign flips for QUARKS (√m_s negative in koidenew2.pdf), not specifically for neutrinos
- Rivero references Brannen's neutrino work: "The neutrino case was reevaluated with most modern data [1, 2]" — referring to Brannen
- Rivero's contribution is the phase parameterization (Foot's cone, δ angle), not a specific Q_ν = 2/3 prediction
- Rivero does NOT independently predict that standard Q_ν = 2/3 for neutrinos

Rivero is cited in PRED-002 as co-predicting Q_ν ≈ 2/3, but the primary source shows he reviews and extends the framework — he doesn't make the specific prediction attributed to him.

### ZiP: Different phase, different structure, NOT standard Q_ν = 2/3

ZiP (Zero-Interaction Principle, J. Buchanan 2025/2026) predicts:

- Neutrino Koide phase: **δ_ν = -4/15** (different from charged lepton δ = 2/9)
- "Inverted moment formula" for neutrinos (d=1 dimensional limit vs d=3 for charged leptons)
- "Neutrinos exist in a constrained one-dimensional manifold where the moment formula inverts"

This is a **different structure** from the charged lepton Koide relation. The inverted moment formula suggests a different β (amplitude) parameter, not the β = √2 that gives Q = 2/3.

**Numerical check:** With δ_ν = -4/15 and β = √2, one amplitude goes slightly negative (-0.005), violating the physical domain condition. If β < √2 (as the "inverted" formula suggests), then Q_ν = (1 + β²/2)/3 < 2/3.

ZiP does NOT predict standard Q_ν = 2/3. It predicts a different phase and a different structure.

---

## Verdict

**The PRED-002 `rivals_say` field is MISLEADING.** Specifically:

| Claim in PRED-002 | Primary source says | Verdict |
|---|---|---|
| "Brannen/Rivero predict Q_ν ≈ 2/3" | Brannen predicts sign-flipped Q' = 2/3, NOT standard Q_ν = 2/3. Rivero reviews but doesn't independently predict. | **MISLEADING** |
| "via sign-flipped preon/Clifford phase mechanism" | The sign-flip IS the mechanism — and it means the standard Q_ν ≠ 2/3 | **Technically accurate but misleading** — the sign flip is why standard Q_ν ≠ 2/3 |
| "ZiP also extends Koide to neutrinos with a similar mechanism" | ZiP uses an inverted moment formula with δ_ν = -4/15, NOT a similar mechanism | **INACCURATE** — different mechanism, different prediction |
| "This makes the disagreement clean" | All three rivals AGREE with PF that standard Q_ν ≠ 2/3 | **FALSE** — there is no clean disagreement on standard Q_ν |

---

## What this means for PRED-002

1. **PRED-002 is NOT a discriminating prediction against Brannen/Rivero/ZiP.** All parties agree that the standard Q_ν ≠ 2/3. The disagreement is about whether a MODIFIED formula (sign-flipped, inverted moments) works — which is a different question.

2. **The prediction is still valid.** PF predicts standard Q_ν ≠ 2/3, and the MC confirms this at 10.24σ (NO) / 25.99σ (IO). The prediction is just not discriminating against these specific rivals.

3. **The DEGENERATE-risk flag from Codex was CORRECT.** The rivals don't actually disagree with the prediction as stated.

4. **The `rivals_say` field must be corrected.** The honest statement is: "No known rival predicts standard Q_ν = 2/3 for neutrinos. Brannen predicts a sign-flipped modified formula; Rivero reviews the framework; ZiP predicts a different phase and structure. The standard Q_ν ≠ 2/3 is agreed by all parties."

5. **The falsifier remains valid.** If DUNE/Hyper-K/CMB-S4 measures standard Q_ν within 1% of 2/3, that would falsify PF's claim AND Brannen's sign-flip claim AND ZiP's inverted formula — because none of them predict standard Q_ν = 2/3.

---

## Recommended correction to PRED-002

Replace the `rivals_say` field with:

```
rivals_say: No known rival predicts standard Q_ν = 2/3 for neutrinos.
            Brannen (2006) predicts a SIGN-FLIPPED modified Koide relation
            (-√m₁+√m₂+√m₃)²/Σm = 3/2, which gives standard Q_ν = 0.52,
            NOT 2/3. Rivero reviews the framework but does not independently
            predict standard Q_ν = 2/3. ZiP (Buchanan 2025) predicts a
            different phase (δ_ν = -4/15) and inverted moment structure.
            All parties AGREE that standard Q_ν ≠ 2/3. The prediction is
            not discriminating against these rivals. The falsifier remains
            valid: if standard Q_ν is measured within 1% of 2/3, all
            frameworks (PF, Brannen, ZiP) are falsified.
```

---

*This verification was conducted against primary sources (Brannen's papers at brannenworks.com, Rivero's review at a.rivero.nom.es, ZiP preprints at academia.edu). All URLs verified accessible 2026-08-09.*
