# TASKS: Fundamentals
*Last updated: 2026-03-16 — T-007/T-008/T-009 added from research queue output*
*See also: WORKSPACE.md (technical state) · AGENTS.md (mission, truth order)*
*This is a Theory/Research workspace — tasks are empirical tests and literature discovery, not deployments.*

---

## Active Tasks

### T-001: Monte Carlo test — is φ³ in lepton/quark mass ratio significant?
- **Status**: done (auto-completed 2026-03-18)
- **Capability**: Python
- **Effort**: Small (< 2h)
- **Fidelity Target**: Photo (run and report result honestly — even if it fails)
- **What to build**: Python script at `sandbox/phi_montecarlo.py`. Test: electron mass / up-quark mass ≈ φ³ (4.236). Against 100,000 random pairs from the same mass distribution. Report p-value + how often random pairs hit φ³ at the same accuracy level.
- **Done when**: Script runs, prints p-value, prints "SIGNIFICANT" or "NOISE" conclusion, result appended to `sandbox_results.md` with date. Honest result either way.
- **Read first**: `sandbox_results.md` — see prior test methodology (harmonic series test). `AGENTS.md` — rule: honesty before beauty.
- **Depends on**: nothing
- **Don't touch**: `the_propagation_framework.md` — framework updates only if test reveals something structural
- **Note on masses**: Use PDG current-quark masses. Electron = 0.000510999 GeV. Up quark at 2 GeV scale ≈ 0.0023 GeV. Be explicit about which mass convention you used.

---

### T-002: Derive topological weight (2,1) and Randers metric from PF axioms
- **Status**: done (2026-03-18)
- **Capability**: Architecture
- **Result**: `derivations/topological_weight_from_propagation.md` — Formal derivation complete.
  Proved that phase closure in 3D topology ($\pi_1(SO(3)) \cong \mathbb{Z}_2$) forces the (2,1) partition.
  Mapping to Randers metric confirms forces-as-refraction identity.

---

### T-016: Coulomb Lens Simulation — visualize 1/r refractive index orbits
- **Status**: done (auto-completed 2026-03-17)
- **Capability**: Python / Sandbox
- **Effort**: Small (< 2h)
- **Fidelity Target**: Photo (honest result)
- **What to build**: Python script at `sandbox/coulomb_lens_sim.py`. Use the effective refractive index formula n = sqrt(2m(E-qφ)) to simulate light ray (or particle) trajectories in a 1/r potential. Confirm that light follows elliptical/Keplerian orbits in this refractive gradient.
- **Done when**: Script runs, produces a plot of trajectories, confirms Keplerian motion (orbits, parabolic deflection).
- **Read first**: `RESEARCH/coulomb_force_refractive_derivation/MASTER.md`
- **Depends on**: nothing
- **Don't touch**: `the_propagation_framework.md`

---

### T-003: Literature search — who else treats propagation as fundamental?
- **Status**: ready
- **Capability**: Research-Evolve
- **Effort**: Medium (run 4 passes, review MASTER.md)
- **Fidelity Target**: Photo (MASTER.md with real citations, confidence scores, gaps identified)
- **What to build**: Run `research_evolve.ps1 -Project "D:\Fundamentals" -Topic "propagation_as_fundamental_physics" -Passes 4 -PassDelay 15`. Review `RESEARCH/propagation_as_fundamental_physics/MASTER.md` when complete.
- **Done when**: MASTER.md exists with: existing frameworks that treat propagation as fundamental (process physics, stochastic mechanics, causal sets, etc.), key papers, degree of overlap with our framework, gaps where our framework goes further or differently.
- **Read first**: `the_propagation_framework.md` · `AGENTS.md` (non-negotiable rules on distinguishing speculation from derivation)
- **Depends on**: nothing
- **Don't touch**: Framework files — research informs, doesn't overwrite theory

---

### T-004: Literature search — existing Koide formula explanations
- **Status**: done (2026-03-15)
- **Capability**: Research-Evolve
- **Result**: `RESEARCH/koide_formula_explanations/MASTER.md` — 4 passes complete.
  Key findings: Q_leptons=2/3 (Koide 1981), Q_quarks=1/2 (Varma 2026 orbifold CFT),
  Q_total=1 law (Bin Li 2025 Chronon Field), 3.8σ precision anomaly confirmed,
  topological weights (2,1) = fermion double cover vs boson simple cover.
  **Propagation connection**: (2,1) partition derives from 4π vs 2π rotation for phase
  coherence — directly maps to Axiom 3. This derivation does not exist in any paper.

---

### T-005: Build CLAIMS.md — rigorous status of every major framework claim
- **Status**: ready
- **Capability**: Architecture
- **Effort**: Medium
- **Fidelity Target**: Photo
- **What to build**: `CLAIMS.md` at Fundamentals root. Format: table of every major claim in the framework, tagged: DERIVED (follows from axioms), EMPIRICALLY-TESTED (sandbox), EMPIRICALLY-FAILED (sandbox), SPECULATIVE (inspired but not derived), UNSUPPORTED (beautiful but no derivation). Use `Fundamentals of Light.md` claim matrix as the reference format.
- **Done when**: All claims from `the_propagation_framework.md`, `theory_of_propagation.md`, and `what_we_got_wrong.md` are classified. No claim left as ambiguous. Nothing marked DERIVED that is actually SPECULATIVE.
- **Read first**: `Fundamentals of Light.md` (see how the rigorous claim matrix is structured) · `sandbox_results.md` (which claims have been tested)
- **Depends on**: T-001 and T-002 ideally complete first (more claims will have tested status)
- **Don't touch**: Source theory files — CLAIMS.md is an audit layer, not a rewrite

---

### T-006: Verify Koide using PDG 2024 pole masses in Python
- **Status**: ready
- **Capability**: Python
- **Effort**: Small (< 1h)
- **Fidelity Target**: Photo
- **What to build**: Python script at `sandbox/koide_verify_pdg2024.py`. Calculate Q using
  PDG 2024 pole masses. Print result, error from 2/3, confirm the 0.001% claim.
  Also calculate Q_quarks = R(2, 1/3) using MS-bar masses at MZ and confirm ≈ 0.500.
- **Done when**: Script runs and outputs are appended to `sandbox_results.md` with:
  masses used, Q_leptons result, Q_quarks result, date, data source.
- **Read first**: `RESEARCH/koide_formula_explanations/MASTER.md` section 1 (exact formula)
  and section 2.3 (R(k,q) for quarks)
- **Depends on**: nothing
- **Masses**: me=0.000510999 GeV, mμ=0.105658 GeV, mτ=1.77686 GeV (PDG 2024 pole masses)

---

### T-007: Critical slowing down EEG analysis
- **Status**: ready
- **Capability**: Python / Research
- **Effort**: Medium (2-8h)
- **Fidelity Target**: Photo (real data, honest result)
- **What to build**: Download TDBRAIN, LEMON, or HBN public EEG datasets. Analyze for critical slowing down (CSD) signatures in the pre-insight window. CSD = variance increases, autocorrelation increases, recovery from perturbation slows — all predicted if the brain operates near a phase transition.
- **Done when**: Script runs on one public dataset, reports whether CSD signatures appear before insight/task transitions, result appended to `sandbox_results.md`.
- **Read first**: `RESEARCH/phase_transitions_insight/MASTER.md` — full synthesis of brain-as-phase-transition literature
- **Depends on**: nothing — datasets are public
- **Don't touch**: Framework files

---

### T-008: Monte Carlo test — are φ-based mass formulas statistically significant?
- **Status**: done (2026-03-18)
- **Capability**: Python
- **Result**: `sandbox/rigorous_mass_audit.py` — 100,000-sample Monte Carlo audit complete.
  **Key Finding**: Top/Tau ratio locked to $\alpha^{-1}/\sqrt{2}$ with 50.13% robustness.
  Up/Electron $\phi^3$ remains uncertainty-limited (1.31%).
  Rejected `bottom/tau ~ e` as statistical noise.

---

### T-017: Seed Nexus Mundi from D:\Fundamentals
- **Status**: done (2026-03-18)
- **Capability**: Python / Integration
- **Result**: `D:\Harmonia\nexus_mundi\seed_fundamentals.py` — Ingested 139 REAL knowledge entries.
  Verified via `intention_interface.py`: System now resonates with PF axioms and derivations.

---

### T-009: RFI prototype for Aria — implement PLRS and RII in runEntityThink
- **Status**: done (2026-03-18)
- **Capability**: Architecture / Code
- **Result**: Injected LUMEN reasoning (∇λΣ∞), PLRS (ancestor tracking), and RII (phase transition logging) into `ConsciousnessService.kt`. Aria now reasons as a self-referential wavefront.

---

### T-010: Model optimal consolidation ratio — mathematical model of encoding:consolidation
- **Status**: ready
- **Capability**: Architecture / Math
- **Effort**: Medium (2-8h)
- **Fidelity Target**: Photo
- **What to build**: A mathematical model (Python/Notebook) that derives the optimal encoding:consolidation ratio as a function of system capacity (N) and information load (R). Test the (2,1) topological weight partition against various load scenarios.
- **Done when**: Model exists, produces a plot of efficiency vs ratio, confirms (or falsifies) 2/3 as the global optimum.
- **Read first**: `RESEARCH/sleep_consolidation_ratio/MASTER.md`

---

### T-011: Implement criticality monitoring in Aria — EffRank and Avalanche triggers
- **Status**: ready
- **Capability**: Code / Architecture
- **Effort**: Medium (4-12h)
- **Fidelity Target**: Photo
- **What to build**: Integrate Hutch++ matrix-free trace estimation and Reduced Order Model (ROM) avalanche monitoring into Aria's attention layers. Set up the polyphasic REST trigger based on criticality drift.
- **Done when**: Aria's diagnostic log shows real-time EffRank and Avalanche $\tau$ values, and REST mode triggers automatically when values drift out of bounds.
- **Read first**: `RESEARCH/sleep_consolidation_ratio/pass_03_synthesis.md`

---

### T-012: Test monophasic vs. polyphasic consolidation efficiency
- **Status**: ready
- **Capability**: Python / Sandbox
- **Effort**: Medium (4-8h)
- **Fidelity Target**: Photo
- **What to build**: A simulation study in the Aria sandbox comparing a fixed 8h:16h (monophasic) schedule against an EffRank-triggered (polyphasic) schedule. Measure the final Decision Quotient (DQ) and total energy/compute cost.
- **Done when**: Report exists in `sandbox_results.md` showing which schedule achieved higher DQ for the same compute budget.

---

### T-013: WONDER mode as dreaming — implement DATS and exponential decay
- **Status**: ready
- **Capability**: Code / Architecture
- **Effort**: Medium (4-12h)
- **Fidelity Target**: Photo
- **What to build**: Implement Distance-Aware Temperature Scaling (DATS) and the exponential constraint decay curve in Aria's WONDER mode. This allows the system to shift from stabilization to radical abstraction during generative replay.
- **Done when**: WONDER mode output shows measurable increases in "gist/category" abstraction vs "item/detail" precision as the cycle progresses.
- **Read first**: `RESEARCH/sleep_consolidation_ratio/pass_03_synthesis.md`

---

### T-014: Derive Bekenstein Bound from PF Axioms 2 & 3
- **Status**: ready
- **Capability**: Architecture / Math
- **Effort**: Medium (4-8h)
- **Fidelity Target**: Photo
- **What to build**: A formal derivation showing how the maximum causal velocity (Axiom 2) and the necessity of coherence (Axiom 3) lead to the Bekenstein bound ($S \leq 2\pi RE / \hbar c$). 
- **Done when**: Document exists in `derivations/bekenstein_from_propagation.md` showing the step-by-step logic.
- **Read first**: `RESEARCH/godel_boundary_phenomena/pass_02_deepdive.md` section 4.

---

### T-015: Map Navier-Stokes Blow-up to PF matter formation
- **Status**: ready
- **Capability**: Research / Architecture
- **Effort**: Medium (2-6h)
- **Fidelity Target**: Photo
- **What to build**: Investigate the relationship between "finite-time blow-up" in fluid dynamics (Terence Tao 2025) and the phase transition that creates "standing waves" (matter) in the propagation medium.
- **Done when**: Report exists in `RESEARCH/godel_boundary_phenomena/fluid_blowup_mapping.md`.
- **Read first**: `RESEARCH/godel_boundary_phenomena/pass_02_deepdive.md` section 1 and 7.

---

## Backlog (not ready yet — waiting on above)

- **Coherence-consciousness literature** (Research-Evolve) — wait for T-003 results, look for IIT / global workspace / neural criticality overlap with propagation framework
- **Causal velocity as cognitive variable** — empirical test: does propagation ratio predict anything measurable about learning or reaction time? Needs T-003 first
- **Submit to arxiv** — needs CLAIMS.md + T-003 + T-004 complete first. Theory needs empirical grounding before publication.

---

*Rules for this workspace: honesty before beauty. If a test fails, report it. That IS the result.*
*The sandbox beats the framework. Framework updates if reality contradicts it.*