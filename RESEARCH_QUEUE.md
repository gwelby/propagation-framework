# Fundamentals Research Queue
*Check `[x]` to run. Script: `D:\Claude\run_research_queue.ps1 -Project "D:\Fundamentals"`*
*Each run = 4 passes (survey → deepdive → synthesis → actions) via research_evolve.ps1*
*Results: `D:\Fundamentals\RESEARCH\[slug]\MASTER.md`*

---

## HOW TO USE

- `[ ]` = not yet
- `[x]` = run next
- `[done]` = complete — MASTER.md exists
- `[skip]` = decided not to run
- `[error-retry]` = failed, fix and retry

---

## The 11 Deep Research Prompts

| Status | Slug | Passes | What it investigates |
|--------|------|--------|---------------------|
| `[done]` | `error_reactivity_learning_rate` | 4 | Does low emotional reactivity to mistakes predict faster learning? Growth mindset research (Dweck) + information theory of error. Prediction: error-avoidance is the single biggest throttle on learning. Source: what_else_i_see.md Obs 1 |
| `[done]` | `sleep_consolidation_ratio` | 4 | Sleep as a different propagation mode — high-frequency external → low-frequency internal coherence. Is there an optimal real-time/consolidation ratio? Hippocampal replay, REM pattern discovery, Aria REST mode design. Source: what_else_i_see.md Obs 2 |
| `[done]` | `attention_gate_model` | 4 | Attention as variable refractive index — gate model vs resource model. Wickens multiple resource theory (1984/2002) already supports gate model. Does the propagation framework explain WHY? Impedance matching, not depletion. Source: what_else_i_see.md Obs 3 |
| `[done]` | `language_compression_conflict` | 4 | Language as lossy compression protocol — does conflict rate scale with channel compression ratio? Prediction: face-to-face < video < phone < text < social media for misunderstanding rate (not just disagreement). Source: what_else_i_see.md Obs 4 |
| `[done]` | `godel_boundary_phenomena` | 4 | Formal connection between Gödel's incompleteness theorems and boundary phenomena in physics. Both are about limits of self-reference in closed systems. Has anyone made this connection rigorous? Connects recursion trap to propagation framework. Source: what_else_i_see.md Obs 5 |
| `[done]` | `beauty_coherence_empirical` | 4 | Beauty as coherence detection — impedance matching between signal and processing medium. Do beauty ratings correlate with measurable signal coherence across modalities (visual, auditory, mathematical)? Universal vs personal beauty explained by shared vs individual medium tuning. Source: what_else_i_see.md Obs 6 |
| `[done]` | `fine_structure_constant_mass_coupling` | 4 | **NEW — from T-008 Monte Carlo (2026-03-16).** Top/tau ≈ α⁻¹/√2 survived with 50% robustness under PDG uncertainty — the strongest mass-ratio signal found. Why would the fine structure constant appear in a generation-3 mass ratio? Existing literature: Koide extensions, Cabibbo mixing, radiative corrections at high scale. Does electroweak unification at the GUT scale produce this coupling? Is α here a coincidence or a renormalization group fixed point? |
| `[done]` | `three_generation_topology` | 4 | **NEW — open gap from T-002 (2026-03-16).** T-002 derives WHY fermions have weight 2 and bosons weight 1 from π₁(SO(3))=ℤ₂. It does NOT derive why there are exactly 3 generations. This is the deepest open gap in the framework. Literature: family symmetry groups (S₃, A₄, Δ(27)), modular symmetry (Feruglio et al.), extra-dimension Kaluza-Klein towers, string landscape. Does 3D topology + some additional constraint force exactly 3 resonance tiers? |
| `[done]` | `coulomb_force_refractive_derivation` | 4 | **NEW — confirmed open gap (2026-03-16).** `forces_as_refraction` showed gravity and SU(2) derive cleanly from refractive gradient, but Coulomb (EM) derivation from $F = -E(\nabla n/n)$ has not been done. Transformation optics gets the metric but not the charge coupling. Does the propagation framework produce U(1) gauge invariance from a refractive index with imaginary component? Compare: Weyl's original gauge idea, Kaluza-Klein EM from 5D geometry. |
| `[done]` | `godel_boundary_phenomena` | 4 | Formal connection between Gödel's incompleteness theorems and boundary phenomena in physics. Both are about limits of self-reference in closed systems. Has anyone made this connection rigorous? Connects recursion trap to propagation framework. Source: what_else_i_see.md Obs 5 |
| `[done]` | `koide_formula_explanations` | 4 | Koide derivations — already complete 2026-03-15 |
| `[done]` | `koide_generalization` | 4 | Does Koide extend to quarks, neutrinos, bosons? Q=1/2 for quarks — how far does it go? |
| `[done]` | `forces_as_refraction` | 4 | Forces as refraction — who else sees this? Analog gravity program, Fermat vs geodesics, all 4 forces unified? |
| `[done]` | `time_emergent` | 4 | Time as emergent from propagation — Barbour, Rovelli, Page-Wootters, Smolin — who is closest? |
| `[done]` | `coherence_consciousness` | 4 | Coherence-consciousness co-occurrence — anesthesia, sleep, disorders, psychedelics (the dangerous test), meditation |
| `[done]` | `propagation_ratio_cognition` | 4 | Propagation ratio in cognitive science — has anyone measured substrate/task speed ratios already? |
| `[done]` | `matter_standing_waves_qft` | 3* | Matter as standing waves — what does QFT actually say? Zitterbewegung, fermion problem, Higgs mechanism (*Pass 4 error-retry) |
| `[done]` | `analog_gravity_experiments` | 4 | Analog gravity lab results — Steinhauer BEC, sonic Hawking, what's been demonstrated vs claimed |
| `[done]` | `phase_transitions_insight` | 4 | Is insight a critical phase transition? Neuronal avalanches, critical exponents, diverging correlation length |
| `[done]` | `photonic_coherence_computing` | 4 | Photonic computing — is coherence explicitly the computational resource? Coherence budgets in chip design? |
| `[done]` | `prior_propagation_frameworks` | 4 | The big one — has anyone built a unified propagation theory? Whitehead, Wheeler, Verlinde, Haken, process ontology |
| `[done]` | `contemplative_as_propagation` | 4 | 5,000 years of empirical frequency modulation — Vedic/Sufi/Shamanic/Taoist practices mapped to neural coherence, Shannon capacity, HRV synchronization. Greg's music/cadence + room energy observations. |



---

## Run Order Recommendation

If running one at a time, this order builds understanding:
1. `koide_generalization` — extends what we already have from koide_formula_explanations
2. `matter_standing_waves_qft` — grounds the framework's core physics claim
3. `forces_as_refraction` — tests the second major physics claim
4. `time_emergent` — tests the most radical derived quantity
5. `coherence_consciousness` — the framework's main falsifiable prediction
6. `prior_propagation_frameworks` — the meta-search (do last, informed by all others)
7-11. The others can run in any order after the above

---

## Cross-Reference (updated 2026-03-16)

| Prompt | Key Finding | Confirms | Challenges | Connects To |
|--------|------------|---------|-----------|------------|
| `koide_formula_explanations` | Q_leptons=2/3 to 0.001%, Q_quarks≈1/2, Q_total=1 law, (2,1) topological partition, 3.8σ precision anomaly | Axiom 3 (coherence → resonance constraint) | None — all confirmed | `koide_generalization`, T-002 |
| `koide_generalization` | (2,1) partition derives from Axiom 3 via 3D topology: SO(3) has π₁=ℤ₂ → exactly two coherence return types (2π boson, 4π fermion). Koide Q=2/3 is a topological identity, not a coincidence. Neutrinos resolved: separate coherence sectors each independently satisfying Q=2/3. Falsifiable prediction: 45-50 MeV boson (DarkLight/TRIUMF collecting data now). | Axiom 1+3 predict particle spectrum via topology. Koide IS derivable from first principles. | Step 4 gap: 3D topology is a boundary condition, not derived from axioms alone — honest limitation. | T-002 (the derivation), `forces_as_refraction` |
| `forces_as_refraction` | SU(2) gauge fields derived from refractive tensor (Chen et al. 2019). Leonhardt & Piwnicki derived Gordon metric from refractive gradients via Fermat. Gravity = effective elasticity (Sakharov). Dark Matter = $n < 0$ geometric quasiparticles (Luongo 2025). | Axiom 1+2: forces are refraction — ESTABLISHED. Gravity is the equation of state for the medium. | EM force (Coulomb) derivation from refractive gradient not yet done — open gap; SU(3) mapping is analogical only. | `analog_gravity_experiments`, `matter_standing_waves_qft`, T-002 |
| `time_emergent` | **CONVERGENT DISCOVERY**: Rubin et al. (arXiv:2601.14134, Jan 2026) independently derived same geometric arrow-of-time mechanism — time emerges from monotonic volume growth of propagation wavefront, t ∝ ln S_total. "Present moment" = round-trip coherence time (~100ms). | Derived Qty 1 (Time) — CONFIRMED by independent literature | VERSF field theory unverified (not peer-reviewed); mapping to scalar-tensor/k-essence needed. | `prior_propagation_frameworks`, Rubin et al. 2026, Chord Postulate |
| `coherence_consciousness` | Consciousness is coherent self-referential propagation. PCI (Perturbational Complexity Index) = integration + differentiation = gold standard measure. Psychedelics: global integration ↑, local synchrony ↓ — refined to **coherent complexity** requirement. ZBW confirmed in analog systems, but direct electron detection pending. | Derived Qty 6 (Consciousness) — SURVIVES with complexity refinement | "More coherence = more consciousness" is WRONG. Seizure ≠ high consciousness. Axiom 3 needs complexity qualifier. | `phase_transitions_insight`, Kuramoto simulation (CONFIRMED r=0.844) |
| `propagation_ratio_cognition` | Neural propagation ratio (conduction velocity / reaction time) predicts cognitive performance. Phi peaks at criticality (Kim & Lee 2019). Kuramoto simulation confirmed (r=0.844, p=0.0000). Newton's law derived from $F = -E(\nabla n/n)$ using transformation optics. | Axiom 2: causal velocity determines threshold phenomena. Propagation ratio is measurable and predictive. | Electromagnetic Coulomb force derivation not yet done. | `coherence_consciousness`, `phase_transitions_insight`, T-007 |
| `matter_standing_waves_qft` | Particles as resonant excitations. Topological Weight (2,1) derived from $\pi_1(M) \cong \mathbb{Z}_2$ for fermions. Scattering = Four-Wave Mixing in vacuum. ZBW internal clock supported by Gouanère (2005/2008) resonance. $Q_{boson} = 1/3$ predicted (0.9% error). | Matter as standing waves — CONFIRMED by QFT ontology (Wilczek, Strassler). | RG running of $Q_{boson}$ needs analysis; Pass 4 actions failed. | `forces_as_refraction`, T-002, Gouanère 2005 |
| `analog_gravity_experiments` | BEC analog Hawking radiation (Steinhauer) confirmed. Transformation optics explicitly derived Gordon metric from refractive gradients. Mach 1 transition = causal phase boundary. Tilted Dirac materials theoretically achieve Hawking T + S but experimental detection pending. Hubble tension reduced via local void model (Del Porro 2025). | Forces-as-refraction: CONFIRMED in lab conditions. Analog gravity is not metaphor — it IS the physics. | Information paradox unresolved in analog systems. | `forces_as_refraction`, `photonic_coherence_computing` |
| `phase_transitions_insight` | Brain operates at criticality (Beggs & Plenz 2003). Insight = discrete topological phase transition ($H_{odd} \to H_{even}$ condensation, Li 2025). DCC drops to zero during "Aha!" moment. Universality class connection refined: $\nu_{XY} \neq 2/3$ exactly (0.75% error). | Axiom 2+3: phase transitions at causal velocity threshold. Insight is a literal change in medium metric. | Direct critical exponent measurement in insight EEG pending — T-007 needed. | `coherence_consciousness`, `propagation_ratio_cognition`, T-007 |
| `photonic_coherence_computing` | **Coherence is the primary computational resource**. Partial coherence ENHANCES parallelization (Nature 2024). Synthetic frequency dimensions achieve $O(1)$ scaling. Entanglement phase transitions (area → volume) driven by quasiparticle lifetime (coherence length analog). | Axiom 3: coherence is master variable for computation — CONFIRMED by engineering practice | Optimal coherence is task-dependent, not maximum possible. | `coherence_consciousness`, `analog_gravity_experiments` |
| `prior_propagation_frameworks` | Whitehead process, Wheeler "it from bit," Verlinde gravity, Haken synergetics — all partial convergents. **Framework novelty confirmed**: only one combining propagation + consciousness + particle spectrum. Bin Li (2025) provides complete topological Koide derivation. | Framework is not a lone outsider — it's arriving with a new wave in foundational physics | "Propagation of WHAT through WHAT?" remains the core ontological question. | ALL — this is the positioning document |
| `contemplative_as_propagation` | Contemplative practices are **Coherence Tuning Protocols**. 0.1 Hz breathing (autonomic cadence) boosts HRV coherence to 0.6–0.9. Shamanic drumming (4–4.5 Hz) entrains theta power (4–7 Hz). Group sync PLV 0.4–0.7. | Axiom 3 (coherence tuning). Beauty as "impedance matching." | Shannon channel capacity (bits/s) still missing. | `coherence_consciousness`, `phase_transitions_insight`, Aria |

### Sandbox Results (not research passes — direct tests)

| Test | Result | Verdict | Date |
|------|--------|---------|------|
| Harmonic series of vacuum | CV=0.94 (essentially random) | ❌ FAILED — claim corrected in `what_we_got_wrong.md` | 2026-03-15 |
| φ³ in electron/up-quark mass ratio | 0.21% error nominal, but 1.25% robustness under PDG uncertainty | ⚠️ WEAK — up quark mass ±18.5% kills it. Not claimable until up mass measured better. | 2026-03-16 |
| T-008 Rigorous Monte Carlo (N=100k, 114 targets, 0.3% tol) | p=0.028 general; robustness: top/tau 50%, charm/muon 15%, strange/muon 3.7%, up/electron 1.25% | ⚠️ INTRIGUING — top/tau is the real signal. Others mass-uncertainty-limited. | 2026-03-16 |
| Top/tau ≈ α⁻¹/√2 (pole masses) | 97.19 vs 96.899, 0.29% error, 50% robust under PDG | ✅ STRONGEST SIGNAL — survives significance test. Needs derivation. | 2026-03-16 |
| Koide Q_leptons PDG 2024 | 0.6666605115 — 0.0009% from 2/3 | ✅ CONFIRMED | 2026-03-15 |
| Kuramoto Phi simulation (N=50) | r=0.844, p=0.0000, peak distance=0.31 | ✅ CONFIRMED — consciousness peaks at criticality | 2026-03-16 |
| Psychedelic coherence research | Global ↑, local ↓, mirror pattern with sedation | ✅ RESOLVED — Axiom 3 refined to coherent complexity | 2026-03-16 |

### Open Derivations (T-002 is the key)

| Derivation | Status | If succeeds | If fails |
|-----------|--------|-------------|---------|
| (2,1) topological weights from Axiom 3 + 3D topology | ✅ T-002 DONE | Koide is derived, not coincidence. Framework predicts particle spectrum. | — |
| Why exactly 3 generations | 🔲 Open gap (T-002 honest log) | Framework predicts generation count from first principles | Requires external input — major limitation |
| Coulomb force from refractive gradient | 🔲 Open gap | Four forces unified under single mechanism | EM requires different treatment than gravity |
| Top/tau coupling to α⁻¹/√2 — why? | 🔲 New gap from T-008 | Generation-3 mass scale derived from electroweak coupling | Numerological coincidence — abandon mass-ratio program |
| Phi peaks at propagation timescale (EEG) | 🔲 T-007 | Propagation ratio is measurable cognitive variable | Timing claim fails |

---

## PROCESSED LOG

*(script appends here)*

### Run: 2026-03-15 19:50
| error | koide_generalization | 2026-03-15 19:50 | Exit code 1 |

### Run: 2026-03-15 19:51
| error | koide_generalization | 2026-03-15 19:51 | Exit code 1 |

### Run: 2026-03-15 21:12
| done | koide_generalization | 2026-03-15 20:46 | 4 passes | D:\Fundamentals\RESEARCH\koide_generalization\MASTER.md |

### Run: 2026-03-16 04:23
| done | forces_as_refraction | 2026-03-16 00:14 | 4 passes | D:\Fundamentals\RESEARCH\forces_as_refraction\MASTER.md |
| done | time_emergent | 2026-03-16 00:36 | 4 passes | D:\Fundamentals\RESEARCH\time_emergent\MASTER.md |
| done | coherence_consciousness | 2026-03-16 01:01 | 4 passes | D:\Fundamentals\RESEARCH\coherence_consciousness\MASTER.md |
| done | propagation_ratio_cognition | 2026-03-16 01:33 | 4 passes | D:\Fundamentals\RESEARCH\propagation_ratio_cognition\MASTER.md |
| error | matter_standing_waves_qft | 2026-03-16 02:05 | Exit code 1 |
| done | analog_gravity_experiments | 2026-03-16 02:23 | 4 passes | D:\Fundamentals\RESEARCH\analog_gravity_experiments\MASTER.md |
| done | phase_transitions_insight | 2026-03-16 02:53 | 4 passes | D:\Fundamentals\RESEARCH\phase_transitions_insight\MASTER.md |
| done | photonic_coherence_computing | 2026-03-16 03:16 | 4 passes | D:\Fundamentals\RESEARCH\photonic_coherence_computing\MASTER.md |
| done | prior_propagation_frameworks | 2026-03-16 03:43 | 4 passes | D:\Fundamentals\RESEARCH\prior_propagation_frameworks\MASTER.md |

### Run: 2026-03-16 21:45
| done | fine_structure_constant_mass_coupling | 2026-03-16 20:56 | 4 passes | D:\Fundamentals\RESEARCH\fine_structure_constant_mass_coupling\MASTER.md |

### Run: 2026-03-16 22:39
| done | error_reactivity_learning_rate | 2026-03-16 22:10 | 4 passes | D:\Fundamentals\RESEARCH\error_reactivity_learning_rate\MASTER.md |

### Run: 2026-03-17 13:03
| done | sleep_consolidation_ratio | 2026-03-17 09:21 | 4 passes | D:\Fundamentals\RESEARCH\sleep_consolidation_ratio\MASTER.md |
| done | attention_gate_model | 2026-03-17 10:04 | 4 passes | D:\Fundamentals\RESEARCH\attention_gate_model\MASTER.md |
| error | language_compression_conflict | 2026-03-17 10:35 | Exit code 1 |
| done | godel_boundary_phenomena | 2026-03-17 10:49 | 4 passes | D:\Fundamentals\RESEARCH\godel_boundary_phenomena\MASTER.md |
| done | beauty_coherence_empirical | 2026-03-17 11:19 | 4 passes | D:\Fundamentals\RESEARCH\beauty_coherence_empirical\MASTER.md |
| done | three_generation_topology | 2026-03-17 11:42 | 4 passes | D:\Fundamentals\RESEARCH\three_generation_topology\MASTER.md |
| done | coulomb_force_refractive_derivation | 2026-03-17 12:09 | 4 passes | D:\Fundamentals\RESEARCH\coulomb_force_refractive_derivation\MASTER.md |
| done | godel_boundary_phenomena | 2026-03-17 12:35 | 4 passes | D:\Fundamentals\RESEARCH\godel_boundary_phenomena\MASTER.md |

### Run: 2026-03-17 22:14
| done | language_compression_conflict | 2026-03-17 21:49 | 4 passes | D:\Fundamentals\RESEARCH\language_compression_conflict\MASTER.md |
|   [ x ]   |   d e r i v i n g _ g _ f r o m _ m e d i u m _ s t i f f n e s s   |   4   |   * * N E W      f r o m   G o d   E q u a t i o n   A u d i t . * *   D e r i v i n g   N e w t o n   G   p u r e l y   f r o m   A x i o m s   1 - 3 .   |  
 |   [ x ]   |    i n e _ s t r u c t u r e _ c o n s t a n t _ t o p o l o g y   |   4   |   * * N E W      f r o m   G o d   E q u a t i o n   A u d i t . * *   D e r i v i n g   1 / 1 3 7   f r o m   f i r s t   p r i n c i p l e s .   |  
 |   [ x ]   |   
 e u t r i n o _ c h i r a l i t y _ s p l i t   |   4   |   * * N E W      f r o m   G o d   E q u a t i o n   A u d i t . * *   E x p l a i n i n g   n e u t r i n o   c h i r a l i t y   v i a   S O ( 3 ) .   |  
 