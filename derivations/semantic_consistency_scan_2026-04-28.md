# Semantic Consistency Scan: Coherence and Causal Velocity
*Fundamentals - /mnt/d/Fundamentals/derivations/semantic_consistency_scan_2026-04-28.md*
*Auditor: Codex*
*Date: 2026-04-28*
*Targets: `CLAIMS.md`, `the_propagation_framework.md`, `theory_of_propagation.md`*

---

## Scope Note

`definitions/medium.md` is canonical v1.0.

At initial scan time, `definitions/coherence.md` and `definitions/causal_velocity.md` were **HOLD** after Codex audit. As of the 2026-04-29 addenda, both are **CANONICAL v1.0**. This scan uses the corrected audit boundaries:

- **Coherence** must distinguish phase coherence, quantum coherence, and structural/dynamical coherence.
- **Causal velocity** must distinguish fundamental/front causal velocity from effective propagation, phase, and group velocities.

Report-only. No target files were modified.

---

## Findings

| ID | File:Line | Quoted Text | Finding | Proposed Fix |
|----|-----------|-------------|---------|--------------|
| S-01 | `the_propagation_framework.md:41` | "In all other media, the causal velocity is lower." | Conflates fundamental causal/front velocity with effective propagation speed in materials. | "In effective media, specific excitations often propagate below vacuum `c`; front/signal causality remains bounded by the relevant causal structure." |
| S-02 | `the_propagation_framework.md:43` | "The causal velocity is the most important single number..." | Rhetorical overclaim; Task 1 flagged same issue in `causal_velocity.md`. | "Causal velocity is a central parameter..." |
| S-03 | `the_propagation_framework.md:47` | "The energy scale of the system..." | Causal velocity alone does not set energy scale; `E=hf` is set by frequency and `h`, with velocity entering dispersion/wavelength relations. | "The dispersion relation connecting frequency, wavelength, and propagation speed." |
| S-04 | `the_propagation_framework.md:48` | "Where phase transitions occur (at the approach to the causal velocity)" | Overgeneralized. Cherenkov is phase-velocity threshold; neural/cognitive transitions are criticality analogies, not causal-velocity approach. | "Some threshold effects, including Cherenkov-like cases in effective media; other phase transitions require separate criticality models." |
| S-05 | `the_propagation_framework.md:54` | "coherent: when multiple propagation modes maintain stable phase relationships" | Too narrow for structural stability and quantum coherence. | "coherent: when relevant states maintain stable relational structure under evolution; in wave systems this often appears as phase stability." |
| S-06 | `the_propagation_framework.md:63` | "Every structure in the universe... coherence exceeds the background" | Overbroad. Requires domain-specific coherence metric; atoms, brains, and crystals do not share one simple phase-coherence scalar. | "PF hypothesis: stable structures require a domain-specific coherence/stability condition above background noise." |
| S-07 | `the_propagation_framework.md:95` | "At the causal velocity... an observer's sampling path..." | "Observer traveling at `c`" is not physically valid for massive observers; photon proper time wording should be relativistic, not medium ontology. | "For null propagation, proper time along the null path is zero; no massive embedded observer travels at `c`." |
| S-08 | `the_propagation_framework.md:125` | "Temperature is the average frequency of incoherent propagation modes" | Too direct. Temperature is statistical energy distribution; "average incoherent frequency" is an interpretation needing model assumptions. | "Temperature measures statistical energy distribution of incoherent/thermal modes." |
| S-09 | `the_propagation_framework.md:147` | "Solidity is a coherence effect." | Too broad; solidity involves Pauli exclusion, electromagnetic interactions, and material structure. | "Solidity can be interpreted as an interaction/stability effect of overlapping quantum/electromagnetic patterns; not solely coherence." |
| S-10 | `the_propagation_framework.md:171` | "gradient in the local causal velocity" | GR locally preserves `c`; gravity-as-optics uses optical metric/effective coordinate propagation, not literal local causal-speed reduction. | "gradient in the optical metric / effective propagation conditions." |
| S-11 | `the_propagation_framework.md:173` | "slower local causal velocity" | Same as S-10; unsafe as local GR statement. | "slower coordinate/effective propagation in the optical metric." |
| S-12 | `the_propagation_framework.md:211` | "information capacity of a Medium equals its coherence capacity" | Too strong. Shannon capacity depends bandwidth and SNR; coherence is relevant but not identical. | "PF interprets channel capacity as constrained by supported modes, bandwidth, noise, and coherence." |
| S-13 | `the_propagation_framework.md:213` | "measurement... coherent with the measuring device" | Interpretive and phase-specific; measurement/decoherence is not always simple phase synchronization. | Mark as PF interpretation; avoid presenting as resolved measurement problem. |
| S-14 | `the_propagation_framework.md:215` | "Quantum entanglement is shared coherence" | Mostly consistent, but should be phrased in Hilbert-space/nonseparable-state terms to avoid hidden-signal interpretation. | "Entanglement is nonseparable quantum-state structure; PF reads this as shared coherence, with no FTL information." |
| S-15 | `the_propagation_framework.md:239` | "coherence... parts must maintain stable phase relationships" | Too narrow for consciousness claim; needs integrated/self-referential dynamics, not just phase stability. | "stable integrated relational structure; phase stability may be one measurable proxy." |
| S-16 | `the_propagation_framework.md:254` | "full coherence without any consciousness would weaken..." | Invalid as written. Lasers/crystals/superconductors/BECs are coherent without consciousness. | "High coherence alone is not sufficient; falsifier must target a PF-specific self-referential/integrative coherence metric." |
| S-17 | `the_propagation_framework.md:264-268` | Multiple rows marked "Established — literally..." | Overstates broad PF reinterpretations. Medium audit requires `Compatible reframing`, `Domain-restricted theorem`, or `Open bridge`. | Re-label SR/GR/QM/thermo/EM rows with status discipline. |
| S-18 | `the_propagation_framework.md:278` | "propagation ratio: actual signal speed / causal velocity..." | Depends on held causal-velocity definition; cognitive "causal velocity" needs an operational estimator. | "effective propagation ratio, with domain-specific estimator." |
| S-19 | `the_propagation_framework.md:279` | "threshold at causal velocity -> qualitative change" | Neural criticality is not causal-velocity approach. | "threshold/criticality behavior; not necessarily approach to causal velocity." |
| S-20 | `the_propagation_framework.md:296` | "Every increase in coherence will be accompanied by some change in conscious experience." | Too broad; nonconscious coherent systems are counterexamples unless restricted to self-referential cognitive systems. | "Within conscious systems, changes in a PF-specific self-referential coherence metric should track conscious-state changes." |
| S-21 | `theory_of_propagation.md:29` | Lists sound, copper, fiber, social networks as speed limits. | Effective speeds are mixed with fundamental causal/front velocity. | Add explicit "effective propagation speed for that excitation/domain" language. |
| S-22 | `theory_of_propagation.md:35` | "In everything else, it is something slower." | Same conflation: material effective speeds may be slower, but fundamental front causality still obeys local relativistic constraints. | Split "fundamental causal velocity" and "effective signal velocity." |
| S-23 | `theory_of_propagation.md:55` | "propagation ratio is not a metaphor... measurable in every domain" | Too broad for social/cognitive domains without agreed measurement protocol. | "A proposed measurable proxy in each domain; direct in physics/engineering, open in cognitive/social systems." |
| S-24 | `theory_of_propagation.md:77` | "Coherence... determines more... than any other single variable." | Rhetorical overclaim; the canonical coherence definition does not support ranking coherence above all other variables. | "Coherence is a central variable..." |
| S-25 | `theory_of_propagation.md:85` | "A theory... phase-locked..." | Metaphorical use of coherence without technical mapping. | Either mark as analogy or replace with "internally consistent / mutually constraining." |
| S-26 | `theory_of_propagation.md:87` | "coherence is what turns propagation into information" | Too strong; information also requires encoding, distinguishability, channel, receiver/noise model. | "coherence can make stable distinguishable structure available to a receiver." |
| S-27 | `theory_of_propagation.md:89` | "loss of coherence is the universal failure mode" | Equivocates between decoherence, desynchronization, signal degradation, and cognitive confusion. | "A recurring failure mode across domains, with domain-specific metrics." |
| S-28 | `theory_of_propagation.md:97` | "When a signal approaches the causal velocity..." | Overgeneralized threshold claim. | "Some systems have thresholds tied to effective propagation limits; others are criticality/instability thresholds." |
| S-29 | `theory_of_propagation.md:99` | "charged particle reaches the phase velocity..." | Correct physics, but it follows a causal-velocity paragraph; clarify phase velocity is not causal velocity. | Add: "This is a phase-velocity threshold, not a violation of causal/front velocity." |
| S-30 | `theory_of_propagation.md:105` | "transitions are governed by proximity to causal velocity" | Too broad. | "transitions are often governed by proximity to a threshold: critical point, instability boundary, or effective velocity condition." |
| S-31 | `theory_of_propagation.md:115-119` | Five-principle list uses causal velocity and coherence broadly. | Needs same split: effective propagation speed; coherence as phase/quantum/structural variants. | Update list after definitions are fixed. |
| S-32 | `theory_of_propagation.md:135` | "critical point of the cortical network — the causal velocity..." | False equivalence. Critical point is not causal velocity. | "critical point of cortical dynamics; structurally analogous to threshold behavior, not identical to causal velocity." |
| S-33 | `CLAIMS.md:48` | "Top Quark Limit... coherence ceiling threshold" | "Coherence ceiling" remains undefined/held. | Define the coherence ceiling functional or keep as ARGUED with explicit missing metric. |
| S-34 | `CLAIMS.md:51` | "Coherence Ceiling... coherence length" | Needs canonical coherence definition before this claim can be stable. | Reference a specific coherence length/threshold model and falsifier. |
| S-35 | `CLAIMS.md:52` | "minimal coherent representation principle" | Uses coherence in a selection principle without linking to the exact canonical layer or named PF functional. | Cite the Axiom 3b derivation and specify whether "coherent" means structural/dynamical stability, phase relation, or representation minimality. |

---

## Phase 2 Readiness Assessment

| Term | Readiness | Reason |
|------|-----------|--------|
| **Time** | **PARTIAL** | Has a dedicated section and clear narrative, but several claims ("block universe", observer at `c`) need relativistic cleanup. |
| **Energy** | **PARTIAL** | Has substantial text, but "energy is frequency" and conservation-by-frequency require careful status boundaries. |
| **Matter** | **PARTIAL** | Has a dedicated section and good Medium/mode framing, but "particle zoo = harmonic series" must remain interpretive until derived. |
| **Mode** | **NOT READY** | Heavily used but no dedicated definition section. Prompt notes 34 uses; exact singular/plural target-file scan found 29. This needs its own `definitions/mode.md`. |
| **Forces** | **PARTIAL** | Most framework text is already written here, especially gravity/refraction, but only gravity-as-optical-geometry has a DERIVED domain-restricted claim. EM/strong/weak refraction language is broader than audited proof. |

**Most framework text already written:** Forces. `the_propagation_framework.md` has the longest dedicated treatment (`Derived Quantity 4`, lines 161-197) and the clearest table mapping force families to Medium gradients.

**Clearest falsification path:** Forces, specifically gravity-as-optical-geometry, because it already has a domain-restricted DERIVED row and explicit optical/Randers mapping that can be checked.

**Ranked Phase 2 order:**

1. **Forces** - strongest existing text and clearest audit/falsification path via the gravity subset.
2. **Mode** - most urgent vocabulary gap; many uses and no dedicated definition.
3. **Energy** - central but risky; needs precise boundary between "energy as frequency" and standard Hamiltonian/QFT usage.
4. **Matter** - dependent on mode/coherence definitions; should follow `mode.md`.
5. **Time** - conceptually important but most ontology-heavy; leave until causal-velocity language is fixed.

---

## Claims Status Re-audit

Read target: `CLAIMS.md`.

Question: now that `Medium` is canonical and `coherence` / `causal_velocity` have been audited, do existing claim statuses change?

### Summary

No major claim upgrades.

The canonical Medium, coherence, and causal-velocity definitions improve vocabulary discipline, but they do not close any mathematical bridge. The final coherence definition does not define the coherence ceiling, a particle-spectrum selector, or a PF consciousness metric. The final causal-velocity definition separates local causal velocity, front velocity, signal velocity, group velocity, phase velocity, and effective propagation speed. Therefore any claim depending on "coherence ceiling", "minimal coherent representation", or "local causal velocity gradient" should not upgrade until those specific bridges pass.

### Claim Verdicts

| Claim | CLAIMS.md Line | Uses | Verdict | Reason |
|-------|----------------|------|---------|--------|
| The Medium | 30 | coherence + causal + state + dynamics | **UNCHANGED** | Correctly marked as definition/ontology, not physics result. Canonical v1.0 status remains appropriate. |
| Gravity as Optical Geometry / Refraction | 41 | causal/effective propagation geometry | **UNCHANGED** | Claim row is already narrow and domain-restricted to optical/Randers mapping. The broader `the_propagation_framework.md` language needs cleanup, but CLAIMS status remains DERIVED 0.95. |
| (2,1) Topological Weights | 42 | "strict coherence deficit", Family C coherence bridge | **UNCHANGED** | Canonical Medium does not derive `A_NR`, `kappa`, or the physical-realization bridge. No upgrade. |
| Koide U(3) Entropy Selector | 44 | PF coherence dynamics | **UNCHANGED** | The row already says the PF physical selector is not derived. New definitions do not supply the missing selector. |
| Three Generations | 47 | coherence field / massive restoration modes | **UNCHANGED** | Definitions do not close T1 or T2. Status remains CONDITIONAL 0.85. |
| Top Quark Limit | 48 | coherence ceiling threshold | **RECONSIDER** | The canonical coherence definition does not define a "coherence ceiling". Claim should remain no stronger than ARGUED and likely needs a specific threshold functional before 0.85 is defensible. |
| Coherence Ceiling | 51 | coherence length / threshold | **RECONSIDER** | Directly depends on an undefined ceiling functional. Needs its own definition or downgrade. |
| Weinberg Angle | 52 | Axiom 3b; minimal coherent representation | **UNCHANGED** | Medium definition helps vocabulary but does not alter the accepted Casimir/Axiom 3b chain. Caveat: "minimal coherent representation principle" should specify whether coherence means structural/dynamical stability, minimal winding, or phase relation. |
| Propagation Lagrangian | 54 | propagation medium | **UNCHANGED** | Uses Medium as scalar-tensor EFT substrate. Canonical Medium definition is compatible but does not force the scalar branch. |
| Variable c Prediction | 55 | causal velocity / local propagation speed | **RECONSIDER** | This now needs the causal-velocity split: local Lorentz `c`, effective propagation speed, coordinate speed, and scalar-medium rescaling must be distinguished. |
| QCD Confinement | 56 | coherence scale / `lambda_c` | **UNCHANGED** | Current row is already cautious. Definitions do not close RG/matching chain. |
| God Equation | 57 | H_prod, one-medium closure, coherence/identity preservation | **UNCHANGED** | Canonical Medium does not close H_prod, Path A/B, or factorization. Status remains CONDITIONAL 0.88. |
| Life = maintained coherence against entropy | 65 | biological coherence | **UNCHANGED** | Claim already states ARGUED and requires measurable coherence-maintenance / nonequilibrium organization. Needs domain metric, but no status change. |
| Consciousness = coherent self-referential propagation | 66 | self-referential coherence | **UNCHANGED** | Medium audit explicitly keeps consciousness outside the Medium definition. CLAIMS row already has low INTUITION 0.48 and names missing metric. No upgrade; no additional downgrade required. |

### Focus Claims Required by Prompt

#### Weinberg Angle - Verdict: UNCHANGED

The DERIVED 0.90 label rests on the Casimir polynomial plus Axiom 3b/minimal winding, not on the canonical `coherence.md` definition. The new definitions do not strengthen the derivation, because they do not supply the exact coherence functional selecting k=1. They also do not weaken it, because the claim already treats Axiom 3b as an adopted corollary.

Required cleanup: replace or cite "minimal coherent representation principle" with the exact Axiom 3b/minimal winding statement.

#### God Equation - Verdict: UNCHANGED

The canonical Medium and coherence definitions are compatible with a one-medium internal/external closure story, but they do not prove H_prod or select the physical probability model. They also do not resolve Family C or nonquadratic observables.

No upgrade. No downgrade beyond the existing CONDITIONAL 0.88.

#### Consciousness - Verdict: UNCHANGED

The new vocabulary makes the consciousness claim more constrained, not more proven. Coherence alone is explicitly not sufficient. The row already says the missing step is a PF-specific measurable variable separating self-referential coherence from synchrony, integration, broadcast, or metacognition.

Status remains INTUITION 0.48.

#### Gravity as Optical Geometry - Verdict: UNCHANGED

The claim row is already appropriately narrow: null geodesics in static/stationary gravity via optical/Randers geometry. However, downstream prose should avoid "slower local causal velocity" and use "optical metric / effective propagation conditions" instead.

Status remains DERIVED 0.95.

### Net Status Changes Recommended

No immediate edits to `CLAIMS.md`.

Recommended future work after the 2026-04-29 addenda:

1. Create a dedicated `definitions/mode.md` before revising Matter/Energy claims.
2. Revisit `Top Quark Limit`, `Coherence Ceiling`, and `Variable c Prediction` with the canonical coherence and causal-velocity boundaries.
3. Clean up downstream prose in `the_propagation_framework.md` and `theory_of_propagation.md` using the findings above.

---

## Addendum: Coherence Definition Passed

Date: 2026-04-29

`definitions/coherence.md` has been rewritten and passed final Codex audit in `derivations/coherence_definition_final_audit_2026-04-29.md`.

Status update:

| File | Status |
|------|--------|
| `definitions/coherence.md` | **CANONICAL v1.0** |
| `definitions/causal_velocity.md` | **HOLD at this addendum; later passed on 2026-04-29** |

This does not automatically upgrade any claim in `CLAIMS.md`. It only supplies a safer vocabulary gate.

Downstream implication:

- Uses of "coherence" should now specify phase, quantum, structural/dynamical, self-referential, or a named PF functional.
- `Top Quark Limit`, `Coherence Ceiling`, and `Variable c Prediction` still need rework before status upgrades.
- The next definition blocker at this point was `definitions/causal_velocity.md`; it later passed final audit on 2026-04-29.

---

## Addendum: Causal Velocity Definition Passed

Date: 2026-04-29

`definitions/causal_velocity.md` has been rewritten and passed final Codex audit in `derivations/causal_velocity_definition_final_audit_2026-04-29.md`.

Status update:

| File | Status |
|------|--------|
| `definitions/coherence.md` | **CANONICAL v1.0** |
| `definitions/causal_velocity.md` | **CANONICAL v1.0** |

This does not automatically upgrade any claim in `CLAIMS.md`. It supplies safer velocity vocabulary:

- fundamental/local causal velocity,
- front velocity,
- signal / information velocity,
- group velocity,
- phase velocity,
- effective propagation speed.

Downstream implication:

- `Variable c Prediction` remains **RECONSIDER** until it distinguishes local Lorentz `c`, optical/effective coordinate propagation, scalar-medium rescaling, and any actual Lorentz-violation claim.
- Gravity/refraction prose should use "optical metric" or "effective coordinate propagation conditions", not "slower local causal velocity".
- Neural/cognitive threshold claims should remain analogies or applied hypotheses until operational estimators exist.
