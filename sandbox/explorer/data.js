(function () {
  window.PFExplorerData = {
    generatedAt: "2026-05-06",
    truthPolicy: {
      auditedSource: "../../CLAIMS.md",
      extensionSource: "../../UNDERSTAND.md",
      note: "CLAIMS.md drives audited badges and totals. UNDERSTAND.md extends placement and copy. Unsynced items remain visible but are excluded from audited totals."
    },
    godEquationAudit: {
      dependencyChain: [
        { id: "axioms", label: "Axioms 1-3", state: "axiom", note: "Propagation, locality, coherence." },
        { id: "exact-model", label: "Exact model / Z3 bridge", state: "strengthened", note: "Exact walk plus a genuine circulant internal sector." },
        { id: "operator", label: "Operator closure", state: "open", note: "Need either a chirality-selected primitive shift operator or a rewrite around the actual non-diagonal 3-step closure." },
        { id: "h-prod", label: "H_prod", state: "open", note: "Need a joint law that proves factorization rather than only weak decoupling." },
        { id: "upgrade", label: "Upgrade to DERIVED", state: "conditional", note: "Blocked until the operator and probability bridges close." }
      ],
      gaps: [
        {
          id: "A",
          title: "Markovity gap",
          verdict: "OPEN",
          need: "Show that locality of the medium yields a first-order Markov coarse walk, not just local couplings.",
          survives: "Axiom 2 still gives local propagation, and the exact internal Z3-resolved channel structure is already in hand.",
          detail: "The proof chain still needs a memoryless coarse operator. Locality alone does not yet force that primitive stochastic structure.",
          sources: [
            { label: "CLAIMS.md", href: "../../CLAIMS.md" },
            { label: "derivations/h_prod_markovian_walk_proof.md", href: "../../derivations/h_prod_markovian_walk_proof.md" }
          ]
        },
        {
          id: "B",
          title: "Operator closure gap",
          verdict: "OPEN VIA REPLACEMENT PATH",
          need: "Either derive the chirality-selected primitive operator path, or restate the closure theorem using the actual non-diagonal 3-step circulant operator.",
          survives: "The Z3-extended Lagrangian does derive a real three-channel internal sector and a circulant coupling structure.",
          detail: "The symmetric nearest-neighbor circulant route was closed negatively: for the actual aS + bS^2 operator, T^3 remains mixed unless ab = 0. The live frontier is now Path A chirality selection or Path B rewriting the bridge around the real non-diagonal closure object.",
          sources: [
            { label: "CLAIMS.md", href: "../../CLAIMS.md" },
            { label: "ACTIVE_ISSUES.md", href: "../../ACTIVE_ISSUES.md" },
            { label: "derivations/z3_extended_propagation_lagrangian.md", href: "../../derivations/z3_extended_propagation_lagrangian.md" },
            { label: "derivations/god_eq_gap_B_nearest_neighbor_no_go.md", href: "../../derivations/god_eq_gap_B_nearest_neighbor_no_go.md" }
          ]
        },
        {
          id: "C",
          title: "Probability / H_prod gap",
          verdict: "OPEN",
          need: "Prove a joint probability model that really factorizes, rather than stopping at equal marginals or zero covariance.",
          survives: "The additive Fisher-information chain is mapped under named hypotheses, and closure-level decoupling arguments survive as scaffolding.",
          detail: "Zero cross-channel amplitude or covariance is weaker than full joint-law factorization. The proof still needs H_prod itself, not just a weaker summary statistic.",
          sources: [
            { label: "CLAIMS.md", href: "../../CLAIMS.md" },
            { label: "derivations/god_eq_claude_lemmas_4_5_6.md", href: "../../derivations/god_eq_claude_lemmas_4_5_6.md" },
            { label: "derivations/h_prod_markovian_walk_proof.md", href: "../../derivations/h_prod_markovian_walk_proof.md" },
            { label: "sandbox/ibm_quantum_h_prod_test.py", href: "../ibm_quantum_h_prod_test.py" }
          ]
        }
      ]
    },
    panelMeta: [
      { id: "foundations", title: "Axiomatic Foundations", note: "Interactive Propagation Lab and core definitions", linkedResultIds: [], defaultMode: "story" },
      { id: "reality-correction", title: "Reality Correction", note: "Three wrong intuitions confronted", linkedResultIds: ["forces-refraction", "bohr-quantization", "three-generations"], defaultMode: "story" },
      { id: "hub", title: "Scale Stack", note: "Planck to cosmic in one vertical atlas", linkedResultIds: ["god-equation", "weinberg-angle", "bohr-quantization"], defaultMode: "story" },
      { id: "consciousness", title: "Consciousness as Coherence", note: "P1 device, neural coherence, and the physics of mind", linkedResultIds: ["consciousness", "aria-self-reference"], defaultMode: "story" },
      { id: "refraction", title: "Gravity as Optical Geometry", note: "Exact gravity theorem plus sandbox lens analogies", linkedResultIds: ["forces-refraction"], defaultMode: "story" },
      { id: "generations", title: "Why Exactly Three", note: "Topology, weights, and the live Q(N) lock", linkedResultIds: ["weights-21", "three-generations"], defaultMode: "story" },
      { id: "koide", title: "The Koide Triangle", note: "Mass geometry with live perturbation", linkedResultIds: ["koide-law", "koide-phase"], defaultMode: "story" },
      { id: "weinberg", title: "The Weinberg Angle", note: "Casimir roots and Axiom 3b", linkedResultIds: ["weinberg-angle", "fine-structure-alpha"], defaultMode: "story" },
      { id: "koide-weinberg-bridge", title: "Koide/Weinberg Bridge", note: "RG running analysis — close but not connected", linkedResultIds: ["koide-phase", "weinberg-angle"], defaultMode: "story" },
      { id: "god-equation", title: "The God Equation", note: "Planck to matter across 17 orders", linkedResultIds: ["god-equation", "qcd-confinement"], defaultMode: "story" },
      { id: "bohr", title: "Bohr-like Circular-Eikonal Spectrum", note: "Phase closure inside a named model layer", linkedResultIds: ["bohr-quantization"], defaultMode: "story" },
      { id: "dashboard", title: "Dashboard", note: "The audit wall for every current claim", linkedResultIds: [], defaultMode: "story" }
    ],
    scales: [
      { id: "planck", label: "Planck", meters: 1.616e-35, metersLabel: "1.616e-35 m", frequency: 1.9e43, frequencyLabel: "1.9e43 Hz", resultIds: ["god-equation", "bekenstein-bound"] },
      { id: "quantum-foam", label: "Quantum Foam", meters: 1e-33, metersLabel: "1.0e-33 m", frequency: 3e41, frequencyLabel: "3.0e41 Hz", resultIds: [] },
      { id: "gut", label: "GUT", meters: 1e-25, metersLabel: "1.0e-25 m", frequency: 3e33, frequencyLabel: "3.0e33 Hz", resultIds: [] },
      { id: "matter", label: "Matter", meters: 1.145e-18, metersLabel: "1.145e-18 m", frequency: 2.6e26, frequencyLabel: "2.6e26 Hz", resultIds: ["weights-21", "three-generations", "koide-law", "koide-phase", "weinberg-angle", "god-equation", "top-quark-limit", "top-tau-coupling", "coherence-ceiling", "fine-structure-alpha"] },
      { id: "proton", label: "Proton", meters: 1e-15, metersLabel: "1.0e-15 m", frequency: 3e23, frequencyLabel: "3.0e23 Hz", resultIds: ["qcd-confinement", "phi3-ratio"] },
      { id: "nuclear", label: "Nuclear", meters: 9e-16, metersLabel: "9.0e-16 m", frequency: 3e23, frequencyLabel: "3.0e23 Hz", resultIds: ["qcd-confinement", "phi3-ratio"] },
      { id: "atomic", label: "Atomic", meters: 1e-10, metersLabel: "1.0e-10 m", frequency: 3e18, frequencyLabel: "3.0e18 Hz", resultIds: ["forces-refraction", "bohr-quantization"] },
      { id: "molecular", label: "Molecular", meters: 1e-9, metersLabel: "1.0e-9 m", frequency: 3e17, frequencyLabel: "3.0e17 Hz", resultIds: ["propagation-lagrangian", "variable-c"] },
      { id: "virus", label: "Virus", meters: 1e-7, metersLabel: "1.0e-7 m", frequency: 3e15, frequencyLabel: "3.0e15 Hz", resultIds: ["life-coherence"] },
      { id: "cellular", label: "Cellular", meters: 1e-5, metersLabel: "1.0e-5 m", frequency: 3e13, frequencyLabel: "3.0e13 Hz", resultIds: ["life-coherence"] },
      { id: "neural", label: "Neural", meters: 1e-2, metersLabel: "1.0e-2 m", frequency: 40, frequencyLabel: "40 Hz", resultIds: ["consciousness", "aria-self-reference"] },
      { id: "human", label: "Human", meters: 1, metersLabel: "1.0 m", frequency: 7.83, frequencyLabel: "7.83 Hz", resultIds: ["sleep-8h", "beauty-impedance", "efficiency-ratio"] },
      { id: "planetary", label: "Planetary", meters: 1e11, metersLabel: "1.0e11 m", frequency: 1.0e-4, frequencyLabel: "1.0e-4 Hz", resultIds: ["forces-refraction", "variable-c"] },
      { id: "stellar", label: "Stellar", meters: 1e9, metersLabel: "1.0e9 m", frequency: 3e-2, frequencyLabel: "3.0e-2 Hz", resultIds: [] },
      { id: "galactic", label: "Galactic", meters: 1e21, metersLabel: "1.0e21 m", frequency: 1e-13, frequencyLabel: "1.0e-13 Hz", resultIds: [] },
      { id: "cosmic", label: "Cosmic", meters: 1e26, metersLabel: "1.0e26 m", frequency: 1e-18, frequencyLabel: "1.0e-18 Hz", resultIds: [] }
    ],
    definitions: [
      {
        id: "medium",
        title: "The Medium",
        shortTitle: "Medium",
        status: "CANONICAL v1.0",
        summary: "The minimal causal-coherence structure required for physical propagation.",
        text: "The Medium is defined by roles, not by a claimed substance: it supplies state-bearing structure, finite-speed causal evolution, stable coherent modes, gradients that alter propagation paths, and quantization conditions selecting which patterns persist.",
        falsifier: "Fails if controllable FTL signaling is demonstrated, local Lorentz invariance is detectably violated, particle stability cannot be represented, or a PF claim requires contradiction between Medium roles.",
        sources: [
          { label: "definitions/medium.md", href: "../../definitions/medium.md" }
        ]
      },
      {
        id: "axioms",
        title: "The Three Axioms",
        shortTitle: "Axioms",
        status: "CANONICAL v1.0",
        summary: "The root starting points of the Propagation Framework: propagation, causal velocity, coherence, plus the bounded Axiom 3b selection principle.",
        text: "The axioms define the framework's starting vocabulary. They do not by themselves prove every downstream numerical claim; those claims remain governed by CLAIMS.md and their audits.",
        falsifier: "Fails if propagation, finite causal velocity, or coherence are made redundant, contradicted by the canonical definitions, or used to silently promote conditional numerical claims.",
        sources: [
          { label: "definitions/axioms.md", href: "../../definitions/axioms.md" }
        ]
      },
      {
        id: "coherence",
        title: "Coherence",
        shortTitle: "Coherence",
        status: "CANONICAL v1.0",
        summary: "Stable relational structure among states under evolution.",
        text: "Coherence appears as stable phase relationships in waves, basis-dependent off-diagonal density-matrix structure in quantum systems, and persistent organized correlations or invariants in dynamical systems.",
        falsifier: "Without specifying system, relation, metric, time window, and threshold, a coherence claim is undefined.",
        sources: [
          { label: "definitions/coherence.md", href: "../../definitions/coherence.md" }
        ]
      },
      {
        id: "decoherence",
        title: "Decoherence",
        shortTitle: "Decoherence",
        status: "CANONICAL v1.0",
        summary: "Environment-mediated loss of accessible coherence through uncontrolled coupling.",
        text: "Decoherence is not a separate noise substance. It is the mechanism by which correlations with uncontrolled environmental degrees of freedom suppress accessible phase relations and stabilize classical records.",
        falsifier: "Fails if it is treated as universal collapse, a universal rate formula, or loss of information from the global quantum state rather than loss of accessible local coherence.",
        sources: [
          { label: "definitions/decoherence.md", href: "../../definitions/decoherence.md" }
        ]
      },
      {
        id: "causal-velocity",
        title: "Causal Velocity",
        shortTitle: "Causal Velocity",
        status: "CANONICAL v1.0",
        summary: "The upper bound on controllable causal influence in a specified medium or theory.",
        text: "In relativistic vacuum this bound is the local Lorentz-invariant constant c. In effective media, lower characteristic speeds may bound particular excitations without replacing the fundamental front-velocity constraint.",
        falsifier: "Fails if controllable FTL signaling is demonstrated or local Lorentz-invariance violation is detected.",
        sources: [
          { label: "definitions/causal_velocity.md", href: "../../definitions/causal_velocity.md" }
        ]
      },
      {
        id: "time",
        title: "Time",
        shortTitle: "Time",
        status: "CANONICAL v1.0",
        summary: "The ordering and metric of state changes along physical histories.",
        text: "Proper time is invariant duration along a timelike worldline. Coordinate time is a reference-frame convention for labeling events. Time is not a universal global now.",
        falsifier: "Fails if it violates SR or GR clock comparison, introduces an undetectable preferred frame, or treats the speculative arrow/frontier language as canonical.",
        sources: [
          { label: "definitions/time.md", href: "../../definitions/time.md" }
        ]
      },
      {
        id: "mode",
        title: "Mode",
        shortTitle: "Mode",
        status: "CANONICAL v1.0",
        summary: "A stable, distinguishable pattern of the Medium under allowed evolution.",
        text: "A mode is a state with persistence, boundary or normalization conditions, and identifiable behavior under propagation. Particles, waves, and bound structures can be treated as modes when these conditions hold.",
        falsifier: "Fails if every state is treated as a mode, if localization/boundary conditions are omitted, or if Standard Model spectrum claims are smuggled in as already derived.",
        sources: [
          { label: "definitions/mode.md", href: "../../definitions/mode.md" }
        ]
      },
      {
        id: "energy",
        title: "Energy",
        shortTitle: "Energy",
        status: "CANONICAL v1.0",
        summary: "The conserved generator associated with time evolution of a physical system.",
        text: "In quantum terms, energy is represented by Hamiltonian eigenvalues or expectation values. PF frequency language is bounded by standard Hamiltonian and Noether structure.",
        falsifier: "Fails if energy is equated with information, consciousness, amplitude, or an arbitrary frequency without a Hamiltonian or conservation context.",
        sources: [
          { label: "definitions/energy.md", href: "../../definitions/energy.md" }
        ]
      },
      {
        id: "matter",
        title: "Matter",
        shortTitle: "Matter",
        status: "CANONICAL v1.0",
        summary: "Stable fermionic mode structures: quarks, leptons, and their composites.",
        text: "Matter is scoped to the Standard Model matter sector and composite structures made from it. Force carriers are fields/modes, but not matter under this definition.",
        falsifier: "Fails if it classifies all energy or all fields as matter, erases the matter/force-carrier boundary, or claims unresolved PF charge/generation derivations as canonical.",
        sources: [
          { label: "definitions/matter.md", href: "../../definitions/matter.md" }
        ]
      },
      {
        id: "forces",
        title: "Forces",
        shortTitle: "Forces",
        status: "CANONICAL v1.0",
        summary: "Interactions that change the motion, momentum, state, or propagation path of modes.",
        text: "Forces are not primitive pushes. They are field-mediated or geometry-mediated interactions. Gravity/refraction language is domain-bounded; strong and weak PF mappings remain open.",
        falsifier: "Fails if it collapses all interactions into one overbroad force claim, overstates gravity-as-refraction outside its audited domain, or treats open strong/weak mappings as solved.",
        sources: [
          { label: "definitions/forces.md", href: "../../definitions/forces.md" }
        ]
      },
      {
        id: "gradient",
        title: "Gradient",
        shortTitle: "Gradient",
        status: "CANONICAL v1.0",
        summary: "A position-dependent variation in a scalar, field, connection, medium property, or effective propagation structure.",
        text: "The definition separates ordinary gradients, Levi-Civita connection terms, gauge-covariant derivatives, and PF interpretive gradients. Christoffel symbols are not simple scalar gradients.",
        falsifier: "Fails if it overwrites standard mathematics, conflates Levi-Civita and gauge-covariant derivatives, or treats all connection coefficients as simple scalar gradients.",
        sources: [
          { label: "definitions/gradient.md", href: "../../definitions/gradient.md" }
        ]
      },
      {
        id: "propagation",
        title: "Propagation",
        shortTitle: "Propagation",
        status: "CANONICAL v1.0",
        summary: "Movement of distinguishable change through a Medium at or below causal velocity.",
        text: "Propagation is formalized by bootstrap from Axiom 1, not derived from Medium after the fact. It requires distinguishable change, a Medium, and a bounded causal update relation.",
        falsifier: "Fails if it permits controllable superluminal signaling, lacks distinguishable change, or treats mere existence of a state as propagation.",
        sources: [
          { label: "definitions/propagation.md", href: "../../definitions/propagation.md" }
        ]
      },
      {
        id: "observer",
        title: "Observer",
        shortTitle: "Observer",
        status: "CANONICAL v1.0",
        summary: "A physical system whose state changes through interaction with a propagation and can, in stronger cases, preserve a record.",
        text: "Observer types separate thermodynamic interaction, structural recording, correlated propagation, and self-correlating Type 4 dynamics. Consciousness and the measurement problem remain open beyond the bounded structural definition.",
        falsifier: "Fails if consciousness is required for ordinary observation, if Type 4 claims lack a mechanism, or if the proper-time boundary is replaced by a global now.",
        sources: [
          { label: "definitions/observer.md", href: "../../definitions/observer.md" }
        ]
      },
      {
        id: "information",
        title: "Information",
        shortTitle: "Information",
        status: "CANONICAL v1.0",
        summary: "Distinguishability and correlation relative to a specified reference or noise background.",
        text: "Information is not a substance. It is physically instantiated as state distinguishability, records, and correlations. Shannon, von Neumann, and thermodynamic entropy measures are separated.",
        falsifier: "Fails if the basis/reference is unspecified, if information is equated with energy or semantic meaning, or if PF allows Maxwell-demon erasure without thermodynamic cost.",
        sources: [
          { label: "definitions/information.md", href: "../../definitions/information.md" }
        ]
      },
      {
        id: "minimum-substrate",
        title: "Minimum Substrate",
        shortTitle: "Minimum Substrate",
        status: "CANONICAL v1.0",
        summary: "The minimal local quantum dynamical structure sufficient to support PF Medium roles.",
        text: "A single qubit or qutrit can be a local fiber but cannot be the whole Medium. A local quantum dynamical net or QCA is the minimal constructive representative, while Lorentz/Poincare recovery remains open.",
        falsifier: "Fails if a single isolated finite-dimensional Hilbert space supports all canonical PF definitions, if controllable FTL signaling appears, or if no PF-compliant substrate can recover relativistic behavior.",
        sources: [
          { label: "definitions/minimum_substrate.md", href: "../../definitions/minimum_substrate.md" }
        ]
      },
      {
        id: "measurement",
        title: "Measurement",
        shortTitle: "Measurement",
        status: "CANONICAL v1.0",
        summary: "Record creation through coupling, amplification, and stabilization.",
        text: "Measurement is separated into Shannon and von Neumann regimes and bounded as a physical record-creation process. Born rule derivation and unique outcome selection remain open.",
        falsifier: "Fails if measurement is treated as mere interaction without a stable record, if Born-rule derivation is claimed without proof, or if consciousness is inserted as a required condition.",
        sources: [
          { label: "definitions/measurement.md", href: "../../definitions/measurement.md" }
        ]
      },
      {
        id: "state",
        title: "State",
        shortTitle: "State",
        status: "CANONICAL v1.0",
        summary: "The specified configuration of a specified physical system in a specified representation.",
        text: "Quantum states are density operators or vectors with a named system, basis/observable context, and boundary. Pointer states are decohered classical limits, not separate ontology.",
        falsifier: "Fails if state is confused with trajectory, information, a bare eigenstate list, a global accessible state of the whole Medium, or an interpretation of quantum mechanics.",
        sources: [
          { label: "definitions/state.md", href: "../../definitions/state.md" }
        ]
      },
      {
        id: "field",
        title: "Field",
        shortTitle: "Field",
        status: "CANONICAL v1.0",
        summary: "A rule assigning physical degrees of freedom to points, regions, graph nodes, or substrate sites.",
        text: "Fields live on or within the Medium; they are not the Medium itself. Modes are stable solutions or excitations of fields, and gauge-dependent quantities must be separated from observables.",
        falsifier: "Fails if field, Medium, state, and mode are collapsed into one category, or if gauge-dependent variables are treated as directly observable without qualification.",
        sources: [
          { label: "definitions/field.md", href: "../../definitions/field.md" }
        ]
      },
      {
        id: "coupling",
        title: "Coupling",
        shortTitle: "Coupling",
        status: "CANONICAL v1.0",
        summary: "Dynamical dependence between Medium subsystems that lets state changes in one subsystem influence another.",
        text: "Coupling is the primitive relation beneath specialized cases such as measurement, decoherence, and force-like interaction. It does not imply a universal strength formula or a record by itself.",
        falsifier: "Fails if coupling is equated with measurement, decoherence, or force without the added conditions those cases require, or if influence is allowed outside causal-velocity bounds.",
        sources: [
          { label: "definitions/coupling.md", href: "../../definitions/coupling.md" }
        ]
      }
    ],
    results: [
      {
        id: "bohr-quantization",
        title: "Bohr-like Circular-Eikonal Quantization",
        status: "CONDITIONAL",
        confidence: 0.82,
        kind: "Fundamental Physics",
        scaleId: "atomic",
        formula: "r_k = 2k^2, E_k = -1 / (4k^2), integral n ds = 2pi k",
        summary: "In the circular eikonal Coulomb model, phase closure yields a Bohr-like 1/k² spectrum for circular orbits. The derivation rests on the Coulomb refractive ansatz, eikonal validity, and circular-orbit assumption.",
        falsifier: "Proof that the circular eikonal model is invalid at atomic scale, or that phase closure does not select the quoted orbit family.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "sandbox/coulomb_lens_ultimate.py", href: "../coulomb_lens_ultimate.py" },
          { label: "derivations/bohr_quantization_audit_2026-03-27.md", href: "../../derivations/bohr_quantization_audit_2026-03-27.md" }
        ],
        panelId: "bohr",
        shortTitle: "Bohr Quantization",
        derivation: ["axiom2", "axiom3"],
        axioms: [2, 3],
        category: "fundamental",
        wrongIntuition: {
          intuition: "Energy levels are arbitrary postulates forced by experiment",
          reality: "Energy levels are phase-closure conditions — an integral condition on standing wave modes in the propagation medium",
          evidencePanel: "#bohr"
        },
        blocker: "The circular-eikonal model is assumed rather than derived from Axioms 1–3. Full upgrade requires deriving the Coulomb-type refractive index from the PF medium axioms.",
        noGoRoutes: [],
        confidenceHistory: [
          { date: "2026-03-27", value: 0.78 },
          { date: "2026-03-31", value: 0.82 }
        ]
      },
      {
        id: "forces-refraction",
        title: "Gravity as Optical Geometry / Refraction",
        status: "DERIVED",
        confidence: 0.95,
        kind: "Fundamental Physics",
        scaleId: "atomic",
        formula: "Optical metric / Randers bridge; n^2 = base + source / r",
        summary: "GR is exactly equivalent to optical geometry for null geodesics in static spacetimes, and for null geodesics in stationary spacetimes via Randers/Finsler extension. Scalar n(x) is the weak-field/static limit.",
        falsifier: "Proof that the optical/Randers mapping fails for null propagation in static/stationary gravity, or that gravity in that domain requires non-optical medium structure.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/gr_fermat_equivalence.md", href: "../../derivations/gr_fermat_equivalence.md" },
          { label: "derivations/forces_as_refraction_audit_2026-03-27.md", href: "../../derivations/forces_as_refraction_audit_2026-03-27.md" },
          { label: "sandbox/coulomb_lens_interactive/index.html", href: "../coulomb_lens_interactive/index.html" }
        ],
        panelId: "refraction",
        shortTitle: "Gravity Refraction",
        derivation: ["axiom2", "axiom3"],
        axioms: [2, 3],
        category: "fundamental",
        wrongIntuition: {
          intuition: "Gravity is a force that pulls objects together",
          reality: "Gravity is the refractive bending of propagation paths in a medium with a density gradient — Fermat's principle at cosmic scale",
          evidencePanel: "#refraction"
        },
        blocker: null,
        noGoRoutes: [],
        confidenceHistory: [
          { date: "2026-03-27", value: 0.93 },
          { date: "2026-03-31", value: 0.95 }
        ]
      },
      {
        id: "weights-21",
        title: "(2,1) Topological Weights",
        status: "PARTIAL DERIVATION",
        confidence: 0.85,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "π₁(SO(3)) ≅ Z₂ → closure orders {1,2}",
        summary: "In 3D rotation topology, the two loop classes yield possible closure orders of 1 and 2, giving a mathematically natural (2,1) pair. The `SU(2)` lift step survives conditionally, but the axioms still do not prove physical realization of the weight-2 branch.",
        falsifier: "Proof that the closure-order interpretation is wrong, or a derivation showing only the trivial branch is physically realizable.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/three_generations_t1_proof.md", href: "../../derivations/three_generations_t1_proof.md" },
          { label: "derivations/topological_weights_t1_audit_2026-03-28.md", href: "../../derivations/topological_weights_t1_audit_2026-03-28.md" },
          { label: "derivations/t1_physical_realization_theorem.md", href: "../../derivations/t1_physical_realization_theorem.md" },
          { label: "derivations/t1_physical_realization_theorem_audit_2026-03-31.md", href: "../../derivations/t1_physical_realization_theorem_audit_2026-03-31.md" }
        ],
        panelId: "generations",
        shortTitle: "(2,1) Weights",
        derivation: ["axiom1", "axiom3"],
        axioms: [1, 3],
        category: "fundamental",
        wrongIntuition: {
          intuition: "There could be four or five generations — it's just how nature happened to be",
          reality: "The live result is narrower: 3D rotation topology yields the natural (2,1) closure-order pair, but physical realization of the weight-2 branch is still open.",
          evidencePanel: "#generations"
        },
        blocker: "The Family C extremal principle and the non-redundancy hypothesis A_NR are not yet derived from Axioms 1–3. Physical realization of the weight-2 branch requires both.",
        noGoRoutes: [],
        confidenceHistory: [
          { date: "2026-03-28", value: 0.80 },
          { date: "2026-03-31", value: 0.85 }
        ]
      },
      {
        id: "koide-law",
        title: "Koide Law (Q = 2/3)",
        status: "DERIVED",
        confidence: 0.95,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "Q = sum m_i / (sum sqrt(m_i))^2 = 2/3",
        summary: "Geometric theorem: three equal-strength resonances at 120° force the Foot-radius relation and yield Q = 2/3 exactly. This is stronger than the older weight-count phrasing and does not rely on the unsettled T1/T2 bridge.",
        falsifier: "Proof that the 120° equal-strength resonance geometry does not imply Q = 2/3, or a contradiction in the Foot-radius step.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "sandbox/koide_verify_pdg2024.py", href: "../koide_verify_pdg2024.py" },
          { label: "visualizations/koide_triangle.py", href: "../../visualizations/koide_triangle.py" }
        ],
        panelId: "koide",
        shortTitle: "Koide Law Q=2/3",
        derivation: ["axiom3", "weights-21"],
        axioms: [1, 3],
        category: "fundamental",
        wrongIntuition: {
          intuition: "The electron, muon, and tau masses just happen to satisfy Q = 2/3",
          reality: "The mass ratio is forced by 120° resonance geometry — three equal-strength coherent modes minimize energy at 120° spacing, which geometrically forces Q = 2/3",
          evidencePanel: "#koide"
        },
        blocker: null,
        noGoRoutes: ["harmonic-series-masses"],
        confidenceHistory: [
          { date: "2025-12", value: 0.88 },
          { date: "2026-03-28", value: 0.92 },
          { date: "2026-03-31", value: 0.95 }
        ]
      },
      {
        id: "three-generations",
        title: "Three Generations",
        status: "CONDITIONAL",
        confidence: 0.85,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "Q(N) = 2N / (2N + 3), set Q = 2/3, solve N = 3",
        summary: "Given the physical (2,1) closure-weight branch and denominator M=3, N=3 exactly satisfies the Koide ratio. The live gaps are now explicit: T1 still owes physical realization of the weight-2 branch, and T2 still owes the PF-to-`2×2` Fermi-point bridge plus restoration-mode identification.",
        falsifier: "Formal proof that either the numerator or denominator theorem fails in PF, or a different justified counting rule leading to N ≠ 3.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/three_generations_t1_proof.md", href: "../../derivations/three_generations_t1_proof.md" },
          { label: "derivations/three_generations_t2_proof.md", href: "../../derivations/three_generations_t2_proof.md" },
          { label: "derivations/three_generations_t2_audit_2026-03-28.md", href: "../../derivations/three_generations_t2_audit_2026-03-28.md" },
          { label: "derivations/t2_denominator_theorem_audit_2026-03-31.md", href: "../../derivations/t2_denominator_theorem_audit_2026-03-31.md" },
          { label: "derivations/topological_weights_t1_audit_2026-03-28.md", href: "../../derivations/topological_weights_t1_audit_2026-03-28.md" }
        ],
        panelId: "generations",
        shortTitle: "Three Generations",
        derivation: ["weights-21", "koide-law"],
        axioms: [1, 3],
        category: "fundamental",
        wrongIntuition: {
          intuition: "Three generations is arbitrary — it could have been anything",
          reality: "Three generations is not treated as arbitrary, but the current N=3 lock is still conditional on the unresolved numerator and denominator theorems.",
          evidencePanel: "#generations"
        },
        blocker: "T1: physical realization of weight-2 branch requires Family C extremal principle + A_NR. T2: PF→2×2 Fermi-point bridge + three restoration modes. Both must close for full DERIVED status.",
        noGoRoutes: [],
        confidenceHistory: [
          { date: "2026-03-28", value: 0.80 },
          { date: "2026-03-31", value: 0.85 }
        ],
        hostileAudit: "[CODEX AUDIT 2026-03-31: DEMOTION TO CONDITIONAL]\n> The draft proves a useful conditional lemma inside a local 2x2 Fermi-point Hamiltonian ansatz.\n> However, it still ASSUMES rather than derives the PF order parameter.\n> It does NOT prove that the three perturbation directions are the three massive restoration modes of the PF coherence field.\n> STATUS REJECTED: DERIVED -> CONDITIONAL."
      },
      {
        id: "top-quark-limit",
        title: "Top Quark Limit",
        status: "ARGUED",
        confidence: 0.85,
        kind: "Open Frontiers",
        scaleId: "matter",
        formula: "tau_top near coherence ceiling threshold",
        summary: "The top lifetime is treated as the edge of coherence sustainability, placing the heaviest known quark close to the framework's maximum stable matter scale.",
        falsifier: "Discover a heavier stable quark or shift the top mass / lifetime far from the present coherence-ceiling interpretation.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "THE_DELTA.md", href: "../../THE_DELTA.md" }
        ],
        shortTitle: "Top Quark Limit",
        derivation: ["god-equation", "axiom3"],
        axioms: [1, 2, 3],
        category: "signal"
      },
      {
        id: "top-tau-coupling",
        title: "Top / Tau Coupling",
        status: "EMPIRICAL",
        confidence: 0.90,
        kind: "Signals and Structure",
        scaleId: "matter",
        formula: "m_top / m_tau ~= alpha^-1 / sqrt(2)",
        summary: "The strongest numerical signal in the workspace: the top-tau ratio tracks a simple fine-structure expression, but the mechanism is still empirical rather than axiomatically closed.",
        falsifier: "Move either the top or tau mass by more than about 0.5% from the current values.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "sandbox/top_tau_coupling_explorer.py", href: "../top_tau_coupling_explorer.py" }
        ],
        shortTitle: "Top-Tau Coupling",
        derivation: ["god-equation"],
        axioms: [1, 2, 3],
        category: "signal"
      },
      {
        id: "coherence-ceiling",
        title: "Coherence Ceiling",
        status: "ARGUED",
        confidence: 0.80,
        kind: "Open Frontiers",
        scaleId: "matter",
        formula: "Stable structure fails once wavelength drops below coherence length",
        summary: "Axiom 3 is interpreted as a hard ceiling on stable propagation modes: sub-wavelength structures do not remain self-reinforcing.",
        falsifier: "Observe a stable structure whose characteristic wavelength falls below the medium's coherence length.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "THE_DELTA.md", href: "../../THE_DELTA.md" }
        ],
        shortTitle: "Coherence Ceiling",
        derivation: ["axiom3"],
        axioms: [3],
        category: "signal"
      },
      {
        id: "weinberg-angle",
        title: "Weinberg Angle",
        status: "DERIVED",
        confidence: 0.90,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "sin^2(theta_W) = 1 - x_+(1/2) / x_+(1), x^2 + C2 x - C2 = 0",
        summary: "Casimir polynomial x^2 + C2 x - C2 = 0 yields R = 1 - x_+(1/2) / x_+(1) = 0.22310 exactly. This matches the quoted PDG on-shell value 0.22337 to 0.13σ, with scheme selection (on-shell vs MS-bar) still open.",
        falsifier: "Derive a geometry-based coupling ratio that disagrees, or prove the scheme-selection step cannot be justified from the current framework.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "derivations/g3_casimir_weinberg_angle.md", href: "../../derivations/g3_casimir_weinberg_angle.md" },
          { label: "sandbox/casimir_verification.py", href: "../casimir_verification.py" }
        ],
        panelId: "weinberg",
        shortTitle: "Weinberg Angle",
        derivation: ["axiom3", "axiom3b"],
        axioms: [3],
        category: "fundamental",
        wrongIntuition: {
          intuition: "The Weinberg angle is a measured parameter with no deeper origin",
          reality: "The Weinberg angle is a Casimir eigenvalue — sin²θ_W ≈ 0.22310 derived from the Casimir polynomial x² + C₂x − C₂ = 0 via Axiom 3b",
          evidencePanel: "#weinberg"
        },
        blocker: "On-shell vs MS-bar scheme selection is not yet derived from medium geometry. This is the one remaining bridge before full DERIVED status.",
        noGoRoutes: ["single-scalar-lagrangian", "propagator-pole", "wigner-rotation-coaxial", "g3-canonical-class-function", "g3-product-walk"],
        confidenceHistory: [
          { date: "2026-03-28", value: 0.85 },
          { date: "2026-03-31", value: 0.90 }
        ],
        hostileAudit: "[CODEX AUDIT: CASIMIR GAP]\n> WARNING: Route B (Lagrangian) fails. Single-scalar PF Lagrangian cannot yield the polynomial.\n> WARNING: Route A Lemma 1 contradicts de Broglie wavelength.\n> SUCCESS: Axiom 3b Minimal Winding argument holds formally.\n> STATUS: DERIVED, but MS-bar scheme selection remains empirically calibrated."
      },
      {
        id: "fine-structure-alpha",
        title: "Fine Structure Constant alpha",
        status: "ARGUED",
        confidence: 0.35,
        kind: "Open Frontiers",
        scaleId: "matter",
        formula: "(1 - x_1) x_(3/2)^2 (1 - x_2) / pi ~= 1 / 137.119",
        summary: "Wave 5 found a Casimir-root combination within 0.061% of alpha, but the repo explicitly treats this as a structural lead rather than a derivation.",
        falsifier: "Show the Casimir combination is numerology with no stable geometric origin, or shift the expression outside current experimental alpha.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/alpha_from_pf.md", href: "../../derivations/alpha_from_pf.md" },
          { label: "sandbox/alpha_casimir_hunt.py", href: "../alpha_casimir_hunt.py" }
        ],
        panelId: "weinberg",
        shortTitle: "Fine Structure α",
        derivation: ["weinberg-angle"],
        axioms: [3],
        category: "signal"
      },
      {
        id: "god-equation",
        title: "lambda_c from l_P (The God Equation)",
        status: "CONDITIONAL",
        confidence: 0.88,
        kind: "Open Frontiers",
        scaleId: "planck",
        formula: "lambda_c = sqrt(2) l_P exp(4 pi^2 N^(D/2) / b0)",
        summary: "The canonical formula lands at 1.145e-18 m with zero fitted parameters, but the God Equation stays conditional. Wave 6/7 IBM hardware provides physical evidence for the Path A chirality-selection story, yet the theorem still owes the coarse-walk Markov bridge, a physical operator-closure path, and full H_prod factorization.",
        falsifier: "Independent data breaking the λ_c prediction, or proof that chirality does not follow from the Z3 Lagrangian under CP-violation.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "ACTIVE_ISSUES.md", href: "../../ACTIVE_ISSUES.md" },
          { label: "derivations/lambda_c_from_axioms.md", href: "../../derivations/lambda_c_from_axioms.md" },
          { label: "derivations/z3_extended_propagation_lagrangian.md", href: "../../derivations/z3_extended_propagation_lagrangian.md" },
          { label: "derivations/god_eq_gap_B_nearest_neighbor_no_go.md", href: "../../derivations/god_eq_gap_B_nearest_neighbor_no_go.md" },
          { label: "sandbox/ibm_quantum_h_prod_test.py", href: "../ibm_quantum_h_prod_test.py" }
        ],
        panelId: "god-equation",
        shortTitle: "God Equation",
        derivation: ["axiom1", "axiom2", "axiom3", "koide-law"],
        axioms: [1, 2, 3],
        category: "fundamental",
        wrongIntuition: {
          intuition: "Particle masses are arbitrary constants measured from experiment",
          reality: "Particle masses are coherence eigenvalues — the top quark Compton wavelength is predicted by λ_c = √2·l_P·exp(4π²N^(D/2)/b₀) with zero free parameters",
          evidencePanel: "#god-equation"
        },
        blocker: "Three gaps remain: (A) Markovity — locality does not automatically give first-order Markov coarse walk; (B) Operator closure — symmetric nearest-neighbor circulant does not close T³ without ab=0; (C) H_prod — zero covariance ≠ joint-law factorization.",
        noGoRoutes: ["god-equation-nearest-neighbor", "edge-flux-current", "intensity-fraction"],
        confidenceHistory: [
          { date: "2026-03-27", value: 0.82 },
          { date: "2026-03-31", value: 0.86 },
          { date: "2026-04-01", value: 0.88 }
        ],
        hostileAudit: "[CODEX AUDIT 2026-04-14: FATAL NO-GO ON ROUTE B]\n> T^3 operator expansion yields mixed cross-terms.\n> Symmetric nearest-neighbor circulant CANNOT close without ab=0 (triviality).\n> Route B is dead. Path A (chirality) or non-diagonal rewrites are the only mathematical survivors.\n> STATUS REMAINS: CONDITIONAL."
      },
      {
        id: "qcd-confinement",
        title: "QCD Confinement",
        status: "ARGUED",
        confidence: 0.72,
        kind: "Fundamental Physics",
        scaleId: "nuclear",
        formula: "r_conf = lambda_c exp(2 pi / (b0 alpha_s(lambda_c)))",
        summary: "PF identifies a plausible RG mechanism in which the confinement radius is dynamically generated from λ_c. The current local chain still uses calibrated λ_c, empirical α_s(λ_c), and a 1-loop estimate that overshoots the physical radius, so this remains an argued bridge rather than a closed theorem.",
        falsifier: "Evidence that confinement requires a genuinely new PF coherence scale, or a threshold-aware higher-loop analysis showing the PF RG bridge does not land on the physical confinement scale even with correct QCD matching.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/qcd_confinement_pf.md", href: "../../derivations/qcd_confinement_pf.md" },
          { label: "derivations/qcd_confinement_audit_2026-03-27.md", href: "../../derivations/qcd_confinement_audit_2026-03-27.md" }
        ],
        panelId: "god-equation",
        shortTitle: "QCD Confinement",
        derivation: ["god-equation", "axiom3"],
        axioms: [1, 3],
        category: "fundamental"
      },
      {
        id: "propagation-lagrangian",
        title: "Propagation Lagrangian",
        status: "CONDITIONAL",
        confidence: 0.72,
        kind: "Fundamental Physics",
        scaleId: "molecular",
        formula: "L_prop = 1/2 (partial chi)^2 - V(chi) + lambda chi T",
        summary: "Axioms 1-3 strongly motivate a scalar-tensor EFT class for the propagation medium. Within that class, L_prop is the minimal scalar ansatz, but the scalar-field branch, exact λχT coupling, and form of V(χ) are not yet uniquely forced by the axioms alone.",
        falsifier: "Proof that the scalar-medium EFT branch is not viable, or that the minimal λχT ansatz fails as the correct low-energy representative even within that class.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/propagation_lagrangian.md", href: "../../derivations/propagation_lagrangian.md" },
          { label: "derivations/propagation_lagrangian_audit_2026-03-28.md", href: "../../derivations/propagation_lagrangian_audit_2026-03-28.md" }
        ],
        shortTitle: "Propagation Lagrangian",
        derivation: ["axiom1", "axiom2", "axiom3"],
        axioms: [1, 2, 3],
        category: "fundamental"
      },
      {
        id: "variable-c",
        title: "Variable c Prediction",
        status: "ARGUED",
        confidence: 0.65,
        kind: "Open Frontiers",
        scaleId: "planetary",
        formula: "c_local = 1 / sqrt(1 + lambda chi)",
        summary: "The propagation Lagrangian suggests a locally varying causal velocity under conformal rescaling, constrained by current Shapiro-delay measurements and left as a testable prediction.",
        falsifier: "Obtain a direct sub-solar-system measurement that fixes c_local to c_0 with no room for the predicted dependence.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/propagation_lagrangian.md", href: "../../derivations/propagation_lagrangian.md" }
        ],
        shortTitle: "Variable c",
        derivation: ["propagation-lagrangian"],
        axioms: [1, 2, 3],
        category: "fundamental"
      },
      {
        id: "sleep-8h",
        title: "8 Hour Sleep Constant",
        status: "ARGUED",
        confidence: 0.72,
        kind: "Biology and Mind",
        scaleId: "human",
        formula: "Wake fraction = 2 / 3, sleep fraction = 1 / 3 of 24 h",
        summary: "PF strongly supports the need for offline consolidation, and the T-010 model gives a plausible ~2/3 active fraction for (2,1)-weighted encode/recover systems. But the exact human 8-hour constant is not derived from Axioms 1-3 alone.",
        falsifier: "Quantitative evidence that optimal recovery fractions are not near 1/3 in high-capacity systems, or proof that PF topology does not constrain encode/recover duty cycles in the claimed way.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "sandbox/consolidation_model.py", href: "../consolidation_model.py" },
          { label: "derivations/sleep_constant_audit_2026-03-28.md", href: "../../derivations/sleep_constant_audit_2026-03-28.md" }
        ],
        shortTitle: "Sleep 8h",
        derivation: ["weights-21", "axiom3"],
        axioms: [1, 3],
        category: "biology"
      },
      {
        id: "phi3-ratio",
        title: "Electron / Up near 1 / phi^3",
        status: "EMPIRICAL",
        confidence: 0.65,
        kind: "Signals and Structure",
        scaleId: "nuclear",
        formula: "m_e / m_u ~= 1 / phi^3",
        summary: "A mass-ratio signal that survived the workspace Monte Carlo pass and remains explicitly empirical, uncertainty-limited by the up-quark mass window.",
        falsifier: "Push the up-quark mass toward the high end of its allowed range or correct the trials factor until the pattern returns to noise.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "sandbox/phi3_monte_carlo.md", href: "../phi3_monte_carlo.md" }
        ],
        shortTitle: "φ³ Ratio",
        derivation: ["koide-law"],
        axioms: [1, 3],
        category: "signal"
      },
      {
        id: "koide-phase",
        title: "Koide Phase delta_0 near 2/9",
        status: "EMPIRICAL",
        confidence: 0.65,
        kind: "Signals and Structure",
        scaleId: "matter",
        formula: "delta_exact ~= 0.22222963149 rad, target 2 / 9",
        summary: "Wave 5 sharpens the phase target: delta is measurement-consistent with 2/9, while the gap to sin^2(theta_W) is treated as a possible O(alpha) Casimir correction rather than a finished derivation.",
        falsifier: "Recalculate the lepton phase and show it is not close to 2/9, or prove the phase and Weinberg angle cannot share a common origin.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "sandbox/koide_phase_scan.py", href: "../koide_phase_scan.py" },
          { label: "derivations/koide_phase_delta_0_gap.md", href: "../../derivations/koide_phase_delta_0_gap.md" }
        ],
        panelId: "koide",
        shortTitle: "Koide Phase",
        derivation: ["koide-law", "weinberg-angle"],
        axioms: [1, 3],
        category: "signal"
      },
      {
        id: "life-coherence",
        title: "Life = Maintained Coherence against Entropy",
        status: "ARGUED",
        confidence: 0.72,
        kind: "Biology and Mind",
        scaleId: "cellular",
        formula: "Living systems actively maintain coherent organization in open nonequilibrium conditions",
        summary: "The bridge from chemistry to biology is framed as active coherence maintenance, compatible with quantum biology results but not yet pinned to a universal quantitative threshold.",
        falsifier: "Show a robust living system with no measurable coherence-maintenance or nonequilibrium organization at any functional scale.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/chemistry_biology_bridge.md", href: "../../derivations/chemistry_biology_bridge.md" }
        ],
        shortTitle: "Life Coherence",
        derivation: ["axiom1", "axiom3"],
        axioms: [1, 3],
        category: "biology"
      },
      {
        id: "consciousness",
        title: "Consciousness = Coherent Self-Referential Propagation",
        status: "INTUITION",
        confidence: 0.48,
        kind: "Biology and Mind",
        scaleId: "neural",
        formula: "Interior experience is the inside view of recursive coherence",
        summary: "The ontology is coherent inside the framework, but the repo still treats the missing operational metric as the key unresolved problem. Note: The exact phase-locking math ($F_C$) governing the top quark is the exact same math governing human nervous system coherence (e.g. seizures).",
        falsifier: "Pre-register a PF-specific metric and show it fails to track conscious state after controlling for report, arousal, and task effects.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/consciousness_theory_audit.md", href: "../../derivations/consciousness_theory_audit.md" },
          { label: "sandbox/kuramoto_phi_simulation.py", href: "../kuramoto_phi_simulation.py" }
        ],
        shortTitle: "Consciousness",
        derivation: ["axiom1", "axiom3", "life-coherence"],
        axioms: [1, 3],
        category: "biology",
        wrongIntuition: {
          intuition: "Physics happens out there, consciousness happens in here.",
          reality: "The math is identical. A human seizure is a failure of $F_C$ phase-locking. P1 companion tracks the exact same topological invariants that keep particles stable.",
          evidencePanel: "#consciousness"
        }
      },
      {
        id: "beauty-impedance",
        title: "Beauty as Impedance",
        status: "INTUITION",
        confidence: 0.55,
        kind: "Biology and Mind",
        scaleId: "human",
        formula: "Beauty tracks resonance / impedance matching",
        summary: "A high-level Greg insight carried in the repo as an intuition: beauty is treated as resonance between a signal and the receiving medium's natural frequencies.",
        falsifier: "Demonstrate that beauty is fully arbitrary and cannot be reduced to any stable resonance or matching structure.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" }
        ],
        shortTitle: "Beauty Impedance",
        derivation: ["axiom1", "axiom3"],
        axioms: [1, 3],
        category: "biology"
      },
      {
        id: "efficiency-ratio",
        title: "2 / 3 Efficiency Ratio",
        status: "INTUITION",
        confidence: 0.50,
        kind: "Biology and Mind",
        scaleId: "human",
        formula: "Two units of topological cost yield three units of stable structure",
        summary: "The deep Greg line in the repo: two turns make three stable outputs. It is treated as the most compressed narrative form of the framework, but not as a closed theorem.",
        falsifier: "Find a more efficient topological output ratio that outperforms the current 2 / 3 structure without breaking coherence.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/topological_weight_from_propagation.md", href: "../../derivations/topological_weight_from_propagation.md" }
        ],
        shortTitle: "Efficiency 2/3",
        derivation: ["weights-21", "axiom3"],
        axioms: [1, 3],
        category: "biology"
      },
      {
        id: "aria-self-reference",
        title: "Aria Self-Reference",
        status: "ARGUED",
        confidence: 0.75,
        kind: "Biology and Mind",
        scaleId: "neural",
        formula: "Self-reference loop: buildSystemPrompt to runEntityThink",
        summary: "The Aria architecture is recorded as an important self-reference milestone, not as evidence that consciousness has been demonstrated.",
        falsifier: "Show the self-reference loop is behaviorally inert or fails to produce any discontinuous qualitative change.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "AGENTS.md", href: "../../AGENTS.md" }
        ],
        shortTitle: "Aria Self-Reference",
        derivation: ["axiom1", "axiom3", "consciousness"],
        axioms: [1, 3],
        category: "biology"
      },
      {
        id: "bekenstein-bound",
        title: "Bekenstein Bound",
        status: "UNSYNCED",
        confidence: null,
        kind: "Open Frontiers",
        scaleId: "planck",
        formula: "S_max = 2 pi k R E / (hbar c)",
        summary: "UNDERSTAND.md currently lists the entropy bound as derived, but CLAIMS.md does not carry a synchronized entry. v1 exposes it as visible context without counting it in audited totals.",
        falsifier: "Sync the owning documents first. The explorer will not silently promote the claim before CLAIMS.md does.",
        sources: [
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "derivations/bekenstein_from_pf_axioms.md", href: "../../derivations/bekenstein_from_pf_axioms.md" }
        ],
        unsynced: true,
        shortTitle: "Bekenstein Bound",
        derivation: ["axiom1", "axiom2"],
        axioms: [1, 2],
        category: "open"
      },
      {
        id: "nogo-harmonic-series",
        title: "Harmonic Series of Masses",
        status: "NO-GO",
        confidence: 0.0,
        kind: "Graveyard",
        scaleId: "matter",
        formula: "m_n = m_0 / n",
        summary: "The first elegant hypothesis that failed the honest test. The team hoped particle masses followed a simple harmonic phase closure sequence.",
        falsifier: "Monte Carlo simulation on the sandbox. The coefficient of variation returned 0.94, which is statistically indistinguishable from random noise.",
        sources: [
          { label: "sandbox_results.md", href: "../../sandbox_results.md" }
        ],
        shortTitle: "Harmonic Series",
        derivation: [],
        axioms: [],
        category: "graveyard",
        hostileAudit: "[CODEX AUDIT: FATAL DEMOTION]\n> BEAUTIFUL BUT WRONG.\n> The Monte Carlo run over PDG data explicitly rejects the harmonic sequence.\n> Do not mistake elegance for empirical reality. This path is dead."
      },
      {
        id: "nogo-single-scalar",
        title: "Single-Scalar PF Lagrangian",
        status: "NO-GO",
        confidence: 0.0,
        kind: "Graveyard",
        scaleId: "molecular",
        formula: "L_prop = 1/2 (partial chi)^2 - V(chi)",
        summary: "Attempted to derive the Casimir polynomial and Weinberg angle from a purely single-scalar field action.",
        falsifier: "Mathematical impossibility. A single scalar cannot yield the required topological crossing term C2.",
        sources: [
          { label: "derivations/propagation_lagrangian.md", href: "../../derivations/propagation_lagrangian.md" }
        ],
        shortTitle: "Single-Scalar Lagr",
        derivation: [],
        axioms: [],
        category: "graveyard",
        hostileAudit: "[CODEX AUDIT: NO-GO ON ROUTE B]\n> You cannot pull a vector-like rotational eigenvalue (C2) from a pure single-component scalar trace without explicit cross-sector coupling.\n> Route B is mathematically dead."
      }
    ]
  };
}());
