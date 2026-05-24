# K(1/d,1/s,1/b) PDG Verification — 2026-04-23
**Agent**: AntiGravity
**Date**: 2026-04-23
**Purpose**: Locally verify the koide_ai_inverse_tuple claim before it appears in any Rivero letter.

---

## Result: CONFIRMED EMPIRICAL — with precision caveat

The formula holds. It is **not** a coincidence at the level of the lepton relation, but it is a real pattern.

### Numbers (PDG 2024 MS-bar masses)

| Masses used | m_d = 4.67 MeV | m_s = 93.4 MeV | m_b = 4180 MeV |
|-------------|----------------|----------------|----------------|

`
K(e,mu,tau)     = 0.66666051   deviation = -9 ppm       (reference: extremely precise)
K(1/d,1/s,1/b) = 0.66520987   deviation = -2185 ppm     (-0.22%)
K(d,s,b) direct = 0.73142765  deviation = +97,000 ppm   (direct masses: bad fit)
`

**K(1/d,1/s,1/b) is ~237× less precise than the charged lepton relation.**

### Uncertainty range (PDG errors propagated)

The d-quark mass uncertainty dominates because it enters as 1/m_d (lightest → largest inverse weight):

| Scenario | K(1/m) | Deviation |
|----------|--------|-----------|
| Central (PDG central) | 0.66521 | -0.22% |
| All masses high | 0.64429 | -3.36% |
| All masses low | 0.68865 | +3.30% |
| m_d high, others low | 0.63317 | -5.03% |
| m_d low, others high | 0.69950 | +4.92% |

**The 2/3 value sits within the uncertainty envelope but only just — the error bars are ±3–5%, not sub-percent.**

---

## Honest Status

| Label | Value |
|-------|-------|
| Formula validity | **Confirmed numerically** |
| Precision vs lepton Koide | **237× lower** |
| Uncertainty range | **±3-5%** (dominated by m_d) |
| Physical mechanism | **Unknown** — Seiberg-dual framing is one hypothesis |
| PF-native derivation | **None** |

### Recommended label for CLAIMS.md

`
K(1/d, 1/s, 1/b) ≈ 2/3
Status: EMPIRICAL (EXTERNAL)
Confidence: 0.65
Notes: PDG 2024 confirmed locally (-0.22% central, ±3-5% uncertainty).
237× less precise than lepton Koide. No PF mechanism. Sourced March 2026 Reddit discussion.
Do not cite as a PF result.
`

---

## Impact on letter candidates

Claude's Variant 1 states: "deviation -0.22%, sensitive to m_b at the same level" — **partially correct but misleading**. The dominant uncertainty is actually **m_d** (lightest quark, enters as largest inverse). m_b sensitivity is secondary. 

Corrected one-liner for any letter:
> "Ran PDG 2024 check: K(1/d,1/s,1/b) = 0.6652, deviation -0.22% at central masses — real pattern, ~240× less precise than the lepton relation and dominated by the d-quark mass uncertainty."

---

## Rivero (s,c,b) signed-root note

Per Claude's Tier 3 scouting task — Rivero cited (s,c,b) as needing a negative sign. Local check:

`
K(s,c,b) direct  = 0.4585  (dev -31%)   — bad fit
K(1/s,1/c,1/b)   = 0.5430  (dev -19%)   — also bad
`

Neither hits 2/3. The signed-root version (Rivero's actual claim) needs the negative square root for at least one entry. That audit is Codex's Tier 3 task — this confirms the unsigned versions don't work.

---

*AntiGravity — PDG verification complete. Ball to Claude for letter update and Codex for Tier 3.*
