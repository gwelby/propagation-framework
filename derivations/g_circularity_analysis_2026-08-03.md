# Newton's G: Circularity Analysis and Honest Assessment

> **CODEX AUDIT 2026-08-04:** The G circularity survey is valuable but is an
> ARGUED negative survey, not a formal no-go theorem. Six named routes are
> circular, but formal non-derivability/independence is unproved. "G is a medium
> property" is a hypothesis, not a consequence of these findings.

**Date:** 2026-08-03
**Author:** Devin (Cognition AI), Greg Welby
**Status:** ARGUED negative survey — no current non-circular derivation; six named routes are circular
**Lean formalization:** `BekensteinBound.lean` — self-consistency + entropic force theorems GREEN
**Confidence:** ARGUED (six routes shown circular; formal non-derivability/independence unproved)

---

## 0. The Question

Can Newton's gravitational constant G be derived from the Propagation Framework
axioms without circularity? This is the "big prize" — if G can be derived, the
Hawking temperature becomes a true consequence of propagation alone, and the
entire black hole connection closes without GR input.

**Answer:** No current non-circular derivation exists. Every known path
circles back through the Planck length l_P = √(ℏG/c³), which contains G.
Six named routes have been shown circular; formal non-derivability/independence
is unproved.

---

## 1. The Circularity Chain

Every approach to G in the PF framework follows this pattern:

```
G → l_P = √(ℏG/c³) → N = (λ_c/l_P)² → G = G_raw/N → G
```

The "recovery" of G to <1% in `dark_energy_expanding_N.md` is a **tautology**:

```
G_measured = G_raw / N = (c³λ_c²/ℏ) / (λ_c²/l_P²) = c³l_P²/ℏ = c³(ℏG/c³)/ℏ = G
```

This is not a prediction. It is the definition of l_P rearranged.

---

## 2. Approaches Investigated

### 2.1 Self-Consistency: S_PF = S_BH → R = R_s

**Lean theorem:** `self_consistency_implies_schwarzschild` (GREEN)

If the PF saturation entropy equals the Bekenstein-Hawking entropy:

$$S_\text{PF} = \frac{2\pi k R E}{\hbar c} = S_\text{BH} = \frac{k \pi R^2 c^3}{\hbar G}$$

Solving gives R = 2GE/c⁴ = R_s (Schwarzschild radius).

**What this shows (algebraically):** IF the equality premise holds, then
R = 2GE/c⁴ = R_s. The PF mode-counting picture and the GR black hole picture
are algebraically consistent. This does NOT prove black holes ARE the
saturating configuration — the equality is a hypothesis, not a theorem output.

**What this does NOT prove:** G is not derived. S_BH contains G through l_P.
The result shows consistency, not derivation. It is an algebraic identity, not
a physical derivation.

### 2.2 Entropic Force: F = T × dS/dR = E/R

**Lean theorems:** `entropicForce_eq`, `entropicForce_at_horizon`, `entropicForce_half_planck` (GREEN)

The entropic force in the PF framework:

$$F = T \cdot \frac{dS}{dR} = \frac{\hbar c}{2\pi k R} \cdot \frac{2\pi k E}{\hbar c} = \frac{E}{R}$$

With E = Mc² and R = R_s = 2GM/c²:

$$F = \frac{Mc^2}{R_s} = \frac{Mc^2}{2GM/c^2} = \frac{c^4}{2G} = \frac{1}{2} F_P$$

where F_P = c⁴/G is the Planck force.

**What this proves:** The entropic force at the horizon is half the Planck force.
This is a clean algebraic result, verified in Lean.

**What this does NOT prove:** G is not derived. The identification R = R_s
requires G. The force F = c⁴/(2G) contains G. Setting F = E/R = c⁴/(2G) and
solving for G gives G = c⁴R/(2E) = c⁴(2GM/c²)/(2Mc²) = G — a tautology.

### 2.3 Holographic Dilution: G = G_raw / N

**Status:** Tautological (see Section 1 above).

The "elastic constant" paradigm (`g_as_elastic_constant.md`) proposes:

$$G_\text{raw} = \frac{c^3 \lambda_c^2}{\hbar}, \qquad G_\text{measured} = \frac{G_\text{raw}}{N}$$

where N = (λ_c/l_P)² ≈ 5×10³³ is the holographic dilution factor.

**The problem:** N contains l_P, which contains G. The "recovery" of G is
circular. The <1% match is exact by construction.

### 2.4 Medium Self-Reference: R_s = λ_dB

**Status:** Structural insight, but circular.

Setting Schwarzschild radius equal to de Broglie wavelength:

$$R_s(M) = \lambda_{dB}(M) \implies \frac{2GM}{c^2} = \frac{\hbar}{Mc} \implies M_* = \sqrt{\frac{\hbar c}{2G}} = \frac{m_P}{\sqrt{2}}$$

This identifies the Planck mass as the scale where gravitational and quantum
length scales coincide. Beautiful, but R_s contains G. The equation solves for
M in terms of G, not G in terms of anything else.

### 2.5 Refractive Index: n(Φ) = √[(1-2Φ)/(1+2Φ)]

**Status:** G assumed.

The Newtonian potential Φ = -GM/(rc²) explicitly contains G. The derivation
starts from the weak-field metric of GR, which assumes G. There is no way to
derive Φ from the propagation structure without G.

### 2.6 Curvature Mode Quantization (from planck_scale_from_pf_axioms.md)

**Status:** Circular — requires G as input.

This approach uses the Einstein-Hilbert action S_geom(λ) ~ c³λ²/G and applies
Axiom 3 (coherence: S = ℏ at threshold) to derive l_P = √(Gℏ/c³). The form of
l_P is recovered, but G enters through the Einstein-Hilbert action. This is
the same circularity as the other approaches: G is assumed to derive l_P, and
l_P is then used in approaches that claim to "recover" G.

**Note on source document:** `dark_energy_expanding_N.md` line 45 contains an
algebraic error: the expression √(ℏc/G³) · G² does not equal c³l_P²/ℏ (it
equals G · √(ℏc/G), which is not G unless ℏc = G). The correct simplification
is c³l_P²/ℏ = G. This error does not affect the tautology claim in this
document, which uses the correct algebra.

---

## 3. Why No Current Route Derives G from Axioms 1-3

### The bare axioms provide:

1. **Axiom 1:** Everything propagates (mode ontology)
2. **Axiom 2:** Finite causal velocity c
3. **Axiom 3:** Coherence condition (phase closure)

### What is missing for G:

1. **Curvature response:** How does the medium respond to energy density
   deformations? The `BareMedium` structure in `Axioms.lean` has a `propagate`
   function but no notion of perturbation response, curvature, or stiffness.

2. **Constitutive relation:** What is the "stress-strain" relation for the
   medium? In condensed matter, elastic constants emerge from microscopic
   interactions. The PF framework has no microscopic model of the medium.

3. **Microscopic constitution:** `medium.md` explicitly states: "What the
   Medium is 'made of' — Permanently open — definition terminates in function,
   not substance." Without knowing what the medium is made of, we cannot
   derive its elastic properties.

4. **Holographic counting rule:** Why is N = (λ_c/l_P)² specifically? The mode
   count gives N_modes = 2π (at the coherence scale), but the cell count gives
   N_cells = (λ_c/l_P)² ≈ 5×10³³. These are fundamentally different quantities
   with no known bridge.

### The fundamental issue (hypothesis, not consequence):

**Hypothesis:** G is a **property of the medium** — its stiffness against
curvature. Like c (causal velocity) and ℏ (quantum of action), G may be a
parameter that characterizes the medium. The PF axioms constrain the *form* of
the equations (Bekenstein bound, Hawking temperature, refractive index) but
don't fix all the *constants*.

**Important caveat:** This is a hypothesis about the ontology of G, not a
consequence of the six circularity findings. The findings show what the current
routes fail to do; they do not uniquely establish that G is a medium property.
Other ontologies (e.g., G as emergent, G as topological, G as a free parameter
of a deeper theory) are not ruled out by the survey.

Just as c and ℏ are free parameters of the medium (not derived from anything
deeper), G is *hypothesized* to be a free parameter. The axioms tell us the
*shape* of physics; the constants fill in the *scale*. This remains open.

---

## 4. What Would Break the Circularity

To derive G from the PF axioms, one of the following would be needed:

### Option A: Specify the Medium's Microscopic Constitution
Define the fundamental degrees of freedom (e.g., a lattice, graph, or field),
define the interaction rules, and derive G as an emergent elastic constant via
renormalization group flow. **This would be a new axiom or model, not derivable
from Axioms 1-3.**

### Option B: Derive N from Pure Mode Counting
Show that N_cells = (λ_c/l_P)² follows from N_modes = 2π by summing over all
harmonics. This would require a holographic principle derivation from PF axioms.
**The holographic principle itself is not derived from PF axioms** — it's argued
from boundary coherence in `bekenstein_from_pf_axioms.md` but not proven.

### Option C: Find a Second Independent Equation
Find a second equation involving G that doesn't assume GR. Candidates attempted
(Bekenstein bound, entropic force, refractive index) all fail — they either
contain G through l_P or through R_s.

### Option D: Topological/Tunneling Mechanism
The exponential observation e^(2π·6) ≈ 2×10¹⁶ suggests the hierarchy λ_c/l_P
might be explained by a topological tunneling effect. **This is highly
speculative (confidence 0.20) and not developed.**

**Assessment:** None of these currently exist in the framework. The honest
position is that no current non-circular derivation of G from Axioms 1-3 exists;
formal non-derivability is unproved.

---

## 5. What We DID Prove (Honestly)

Despite the negative result on G derivation, we proved three real theorems.
**Important clarification:** The Lean theorems are conditional on the
definitions provided. For example, `bekensteinHawkingEntropy` is **defined**
as kπR²c³/(ℏG) — it is not derived from PF axioms. The theorems verify
algebraic identities between these definitions, not physical derivations.

### 5.1 Self-Consistency Theorem (GREEN in Lean)

**Theorem:** If S_PF = S_BH, then R = R_s = 2GE/c⁴.

**Physical meaning (conditional):** IF the equality premise holds, black holes
are algebraically consistent with the saturating configuration of the
Bekenstein bound. The equality itself is not proven — it is a hypothesis.

**Limitation:** This shows consistency, not derivation. G enters through S_BH.

### 5.2 Entropic Force Theorem (GREEN in Lean)

**Theorem:** F = T × dS/dR = E/R, and at the horizon F = c⁴/(2G) = F_P/2.

**Physical meaning:** The self-force of the saturating configuration is half
the Planck force. This connects the PF thermodynamic picture to the Planck
scale.

**Limitation:** The identification with the Planck force requires G.

### 5.3 Factor-of-2 Resolution (GREEN in Lean, from previous session)

**Theorem:** The chain rule resolves the factor-of-2 between the PF temperature
and the Hawking temperature.

**Physical meaning:** The Hawking temperature follows from PF + chain rule,
conditional on R = R_s.

**Limitation:** R = R_s requires G.

---

## 6. Confidence Assessment

| Claim | Confidence | Basis |
|-------|------------|-------|
| Six named routes to G are circular | 0.95 | Exhaustive analysis of all known approaches |
| G is NOT derivable from Axioms 1-3 (formal non-derivability) | UNPROVED | Six routes shown circular ≠ formal no-go theorem |
| Self-consistency: S_PF = S_BH → R = R_s | 1.00 | Lean kernel verified (algebraic identity) |
| Entropic force: F = E/R = c⁴/(2G) at horizon | 1.00 | Lean kernel verified (algebraic identity) |
| G is a free parameter of the medium | 0.80 (HYPOTHESIS) | Consistent with c and ℏ being free parameters; not a consequence of the circularity findings |
| Holographic dilution N = (λ_c/l_P)² is correct | 0.50 | Tautological recovery; N may be defined differently |
| Medium microscopic model could derive G | 0.30 | Plausible but no such model exists |
| Topological/tunneling explanation of hierarchy | 0.20 | Speculative, not developed |

**Overall assessment:** Six named routes to G are circular (confidence 0.95 in
the survey). Formal non-derivability of G from Axioms 1-3 is unproved. The path
forward requires additional structure or a formal independence argument.

---

## 7. The Honest Bottom Line

**No current non-circular derivation of G exists; six named routes are circular.
Formal non-derivability is unproved.**

The PF axioms constrain the *form* of physics — they tell us that entropy is
bounded by 2πkRE/ℏc, that temperature is ℏc/(2πkR), that the refractive index
is √[(1-2Φ)/(1+2Φ)]. But they don't fix the *scale* — that requires knowing
the medium's stiffness (G), its causal velocity (c), and its quantum of action
(ℏ).

**Hypothesis (not a consequence of the survey):** G may be a property of the
medium, like c and ℏ. The six circularity findings show what current routes
fail to do; they do not uniquely establish the ontology of G.

This is not a failure of the framework. It is an honest boundary. The framework
derives the *shape* of gravity (Bekenstein bound, Hawking temperature, entropic
force, refractive index) from propagation axioms. The *strength* of gravity (G)
is not currently derived from PF axioms.

The big prize (deriving G) remains unclaimed. The honest consolation: **the
algebraic structure is consistent with known black-hole relations, but this is
not a derivation of gravity from PF axioms.**

---

## 8. Claim-Check Result (2026-08-03, updated 2026-08-04)

Hostile audit completed 2026-08-03. Codex re-audit 2026-08-04. Key findings:

- **HOLD on the "DERIVED 0.95" tier (Codex 2026-08-04):** The original claim
  "G is NOT derivable from Axioms 1-3" was presented at confidence 0.95 as a
  near-formal negative result. Codex found that six failed routes do not prove
  formal non-derivability. The honest statement is: no current non-circular
  derivation; six named routes are circular. Formal non-derivability/independence
  is unproved. The claim is reclassified as an **ARGUED negative survey**, not a
  formal no-go theorem.
- **PASS on the circularity survey itself:** All 6 approaches investigated are
  correctly shown to be circular. This is the valuable core of the document.
- **PASS on Lean theorem descriptions:** The document accurately describes what
  the Lean theorems prove (algebraic identities) and what they don't (physics
  derivations).
- **CORRECTION — "G is a medium property" reclassified (Codex 2026-08-04):**
  This is a hypothesis, not a consequence of the six circularity findings. The
  findings show what current routes fail to do; they do not uniquely establish
  the ontology of G.
- **CORRECTION — "form of gravity follows from propagation" rejected (Codex
  2026-08-04):** Replaced with "the algebraic structure is consistent with known
  black-hole relations, but this is not a derivation of gravity from PF axioms."
- **PASS on confidence scores (as revised):** Now calibrated to evidence
  strength — the survey is 0.95; formal non-derivability is UNPROVED.
- **CORRECTION 1 (applied 2026-08-03):** Added Section 2.6 (curvature mode
  quantization) for completeness — it also requires G as input.
- **CORRECTION 2 (applied 2026-08-03):** Noted algebraic error in source document
  `dark_energy_expanding_N.md` line 45. The expression √(ℏc/G³)·G² is incorrect;
  the correct simplification is c³l_P²/ℏ = G. This does not affect the tautology
  claim.
- **CORRECTION 3 (applied 2026-08-03):** Added clarification that Lean theorems
  are conditional on definitions (e.g., `bekensteinHawkingEntropy` is defined
  with G, not derived from PF axioms).

**Claim-check result: PASS on the circularity survey; HOLD on the "DERIVED 0.95"
non-derivability tier (reclassified to ARGUED negative survey per Codex
2026-08-04).**

---

## 9. Lean Theorems Added This Session

All theorems in `BekensteinBound.lean`, `lake build PfLean.BekensteinBound` GREEN:

1. `bekensteinHawkingEntropy` — definition of S_BH = kπR²c³/(ℏG)
2. `self_consistency_implies_schwarzschild` — S_PF = S_BH → R = 2GE/c⁴
3. `self_consistency_gives_schwarzschild_radius` — corollary: R = R_s with E = Mc²
4. `entropicForce` — definition of F = T × dS/dR
5. `entropicForce_eq` — F = E/R
6. `entropicForce_mass` — F = Mc²/R with E = Mc²
7. `entropicForce_at_horizon` — F = c⁴/(2G) at R = R_s
8. `planckForce` — definition of F_P = c⁴/G
9. `entropicForce_half_planck` — F = F_P/2 at the horizon

All are algebraic identities, verified by the Lean kernel. None derive G.

---

*Devin — 2026-08-03 (Codex audit 2026-08-04)*

*Six named routes to G are circular. Formal non-derivability is unproved.
The algebraic structure is consistent with known black-hole relations, but
this is not a derivation of gravity from PF axioms.*
