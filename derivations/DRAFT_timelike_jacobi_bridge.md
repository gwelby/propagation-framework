# DRAFT — Timelike Extension of Gravity-as-Refraction (the Jacobi/Maupertuis Bridge)

> ⚠ **STATUS: UNAUDITED DRAFT — not a result, not a tier.** Authored by Claude (Opus 4.8) 2026-06-09 for CYCLE-PF-TIMELIKE. This is the *target and the gap*, written down precisely so DeepSeek can GROUND the physics and Codex can AUDIT. Nothing here promotes any `CLAIMS.md` row. The one genuinely-new claim (the PF standing-wave mechanism, §4) is explicitly marked OPEN.
> **Extends:** `derivations/gr_fermat_equivalence.md` (Codex, 2026-03-20) — its §9 *is* this document's starting gap.
> **Discharges (if it survives audit):** the manuscript's own stated obligation, `PROPAGATION_MANUSCRIPT_PROD.md:31764` — "the framework must formally derive how the phase-closure of that standing wave generates the Jacobi/Maupertuis effective metric from the underlying null optical metric."

---

## 0. What is and isn't being claimed

The light story is **done** (DERIVED 0.95): null geodesics in a static/stationary spacetime are geodesics of the optical metric `ĥ_ij = V⁻²h_ij` (gr_fermat_equivalence §4). The matter story is **ARGUED ~0.70**: "planets bend like light" is asserted by analogy, and `PERIHELION_VERIFICATION.md` is honestly flagged as a weak-field toy, not a theorem.

This draft attacks exactly that gap in three moves:
- **§1–2 (GR side, textbook):** there already exists a rigorous energy-dependent optical metric for *massive* particles — the Jacobi/Maupertuis metric. This is not PF; it is classical mechanics + GR. Solid ground.
- **§3 (the unification check):** that massive metric reduces to the null optical metric as m→0, and to Newtonian falling in the slow/weak limit. One object, two known limits.
- **§4 (the PF-specific bridge — THE OPEN PIECE):** why a PF "matter = coherent standing wave" mode should *have* that energy-dependent index. This is the only part that is PF's to earn, and it is the part the manuscript flagged.

**Honest headline:** the GR-side math (§1–3) is strong enough to lift "matter bends by refraction" from *analogy* to *derived-modulo-the-PF-mechanism*. The remaining work (§4) is narrower and sharper than "derive gravity for matter" — it is "show the PF medium's dispersion relation reproduces the Jacobi conformal factor."

---

## 1. The Maupertuis principle (non-relativistic, textbook)

A particle of energy `E` in potential `Φ(x)` extremizes the abbreviated (Maupertuis) action
`δ ∫ p · dx = 0`, with `|p| = √(2m(E − mΦ))`. This is *identical in form* to Fermat's `δ∫ n dl = 0` with an **energy-dependent index**

```
n_E(x) = √( 2m ( E − mΦ(x) ) ).
```

So even before relativity, "a massive particle is a ray in a medium" is exact — the only difference from light is that the index depends on the particle's energy. (This is the `n = √[2m(E−qφ)]` already cited at `PROPAGATION_MANUSCRIPT_PROD.md:13223`.) Rays of `n_E` bend toward higher `n_E`, i.e. toward deeper potential — gravity as refraction, for matter, in flat-space mechanics.

## 2. The relativistic/GR Jacobi metric (static spacetimes — established, Gibbons-type)

For a static metric `ds² = −V(x)²c²dt² + h_ij dx^i dx^j`, a **timelike** geodesic of a particle with conserved energy `E` and mass `m` projects onto a spatial geodesic of the **Jacobi-Maupertuis metric**

```
J_ij(x; E) = ( E² − m²c⁴ V(x)² ) / ( c² V(x)² ) · h_ij(x).        … (J)
```

This is a *theorem* of static-spacetime mechanics (Gibbons, "The Jacobi metric for timelike geodesics in static spacetimes," 2015, and Gibbons–Warnick): the massive particle's spatial path is literally a geodesic of `J_ij`. `J_ij` is conformal to the spatial metric `h_ij`, with an **energy-dependent conformal factor** — i.e. an effective optical metric with an energy-dependent index. This is the rigorous matter-analog of §4-light.

**Define** the timelike effective index by factoring the conformal factor against flat space in the conformally-flat weak field:

```
n_E(x)²  ∝  ( E² − m²c⁴V(x)² ) / ( c²V(x)² ).
```

## 3. The two limits (the part that must hold exactly — ALGEBRAIC gate)

**(a) Massless / ultrarelativistic limit `E ≫ mc²`:** drop `m²c⁴V²` against `E²`:

```
J_ij → ( E² / c²V² ) h_ij  ∝  V⁻² h_ij  =  ĥ_ij.        [the null optical metric, gr_fermat §4]
```

The Jacobi metric's `m→0` limit **is** the derived null optical metric. Light is not a separate claim — it is the high-energy boundary of the same object. *This is the unification, and it is a clean algebraic check.*

**(b) Weak-field, slow-motion limit `E ≈ mc² + ½mv²`, `Φ/c² ≪ 1`:** expand `V² = 1 + 2Φ/c²`. To leading order the geodesics of `J_ij` reduce to `d²x^i/dt² = −∂_iΦ` — **Newtonian falling**. (This recovers gr_fermat §2's slow-timelike limit, now *from the optical object itself* rather than separately.)

**(c) Perihelion (the regime Codex separated in the Masters cycle):** Mercury's precession must come out of the geodesic equation of `J_ij` for `Φ = −GM/r` at order `(GM/rc²)` — *without borrowing the null index*. This is the decisive ALGEBRAIC-gate test: if `J_ij` is the right object, perihelion is a massive/timelike Jacobi geodesic, exactly as Codex insisted it should be classified (weak-field massive support, not a null-theorem result).

> **Gate criteria (for the sandbox, before Codex sees it):**
> 1. `m→0` limit of (J) equals `V⁻²h_ij` symbolically. [pass/fail]
> 2. Slow/weak limit of (J)-geodesics equals `ẍ = −∇Φ`. ✔/✗
> 3. (J)-geodesic for `Φ=−GM/r` yields Mercury's `6πGM/c²a(1−e²)` per orbit, derived from (J), not imported. ✔/✗
> Pass all three → the GR-side object is verified and matter-refraction is derived **down to the PF mechanism**.

## 4. The PF-specific bridge — **OPEN** (this is the only piece PF must earn)

Everything above is GR + classical mechanics. It establishes that *if* a massive PF mode follows timelike geodesics of the static metric, it refracts with index (J). PF's own obligation (manuscript 31764) is to derive **why a PF "matter = coherent standing wave" has exactly that energy-dependent index** — i.e. to generate (J) from the medium's dispersion relation, not postulate it.

**Proposed mechanism (candidate, OPEN — for DeepSeek to attempt, Codex to break):**
A PF massive mode is a standing wave in the medium (de Broglie). In a medium with position-dependent causal velocity `c(x)` (the same `V(x)` that gives the null index), a standing wave has a **dispersion relation** `ω² = c(x)²k² + (mc²/ℏ)²` — a frequency-dependent (hence energy-dependent) phase velocity. The eikonal/WKB limit of a wave with this dispersion extremizes an arrival-phase functional whose index is **automatically energy-dependent** and, in the `m→0` branch, collapses to the null index. The claim to test:

```
   eikonal index of the PF standing-wave dispersion   ?=   Jacobi index n_E of (J).
```

If equal → the energy-dependence isn't postulated, it's *forced* by the standing-wave nature of matter in the PF medium, and the manuscript's obligation is discharged. **This equality is unproven and is the whole cycle.** Do not state it as holding.

**Why this is the honest formulation:** it replaces the vague "matter bends like light" with a single sharp, falsifiable algebraic equality between two independently-defined indices. It can fail — and if it fails, we learn the PF standing-wave picture does *not* reproduce GR matter dynamics, which scopes the framework. Either outcome is a real result.

---

## 5. Proposed tiering IF this survives GROUND + AUDIT (Codex decides, not me)
| Sub-claim | Now | If §3 gates pass | If §4 equality also proven |
|---|---|---|---|
| Matter bends by refraction (mechanism-agnostic, GR Jacobi object) | ARGUED 0.70 | **DERIVED-modulo-PF-mechanism ~0.85** | — |
| PF standing-wave forces the Jacobi index (the manuscript's obligation) | not on ledger | OPEN | **DERIVED → "gravity is refraction" whole, light+matter** |
| All forces are refraction | OPEN | OPEN (unchanged) | OPEN (unchanged) |

## 6. Pipeline
1. **DeepSeek (GROUND):** verify (J) against the Gibbons references; run §3 gates (a)(b)(c) symbolically/numerically; attempt the §4 eikonal-index equality.
2. **Sandbox/ALGEBRAIC gate:** the three checks in §3, as hard pass/fail.
3. **Codex (AUDIT):** only after gates pass. Hostile questions to expect: is (J) the correct sign/convention for attractive gravity? does the `m→0` limit *uniformly* converge to the null metric or only pointwise? is the standing-wave dispersion (§4) PF-derived or imported from textbook de Broglie (if imported, §4 is not a PF result)?

---
*Lineage: gr_fermat_equivalence.md (null, DERIVED) → this draft (timelike target + PF gap, UNAUDITED). The light result is the m→0 face of one object; the open work is showing PF's medium puts matter on the other face. — Claude, CYCLE-PF-TIMELIKE DRAFT*
