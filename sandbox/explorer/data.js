(function () {
  window.PFExplorerData = {
    generatedAt: "2026-03-26",
    truthPolicy: {
      auditedSource: "../../CLAIMS.md",
      extensionSource: "../../UNDERSTAND.md",
      note: "CLAIMS.md drives audited badges and totals. UNDERSTAND.md extends placement and copy. Unsynced items remain visible but are excluded from audited totals."
    },
    godEquationAudit: {
      dependencyChain: [
        { id: "axioms", label: "Axioms 1-3", state: "axiom", note: "Propagation, locality, coherence." },
        { id: "exact-model", label: "Exact model / Z3 bridge", state: "strengthened", note: "Exact walk plus a genuine circulant internal sector." },
        { id: "operator", label: "Operator closure", state: "open", note: "Need a primitive operator whose 3-step closure matches the physical internal dynamics." },
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
          need: "Identify the primitive operator whose 3-step closure is diagonal for the physical internal dynamics.",
          survives: "The Z3-extended Lagrangian does derive a real three-channel internal sector and a circulant coupling structure.",
          detail: "The symmetric nearest-neighbor circulant route was no-goed: T^3 stays mixed unless the primitive operator collapses to a pure shift. The route remains open only via a replacement operator path.",
          sources: [
            { label: "CLAIMS.md", href: "../../CLAIMS.md" },
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
      { id: "hub", title: "Scale Stack", note: "Planck to human in one vertical atlas", linkedResultIds: ["god-equation", "weinberg-angle", "bohr-quantization"], defaultMode: "story" },
      { id: "refraction", title: "Forces as Refraction", note: "EM and gravity through one lens field", linkedResultIds: ["forces-refraction"], defaultMode: "story" },
      { id: "generations", title: "Why Exactly Three", note: "Topology, weights, and the live Q(N) lock", linkedResultIds: ["weights-21", "three-generations"], defaultMode: "story" },
      { id: "koide", title: "The Koide Triangle", note: "Mass geometry with live perturbation", linkedResultIds: ["koide-law", "koide-phase"], defaultMode: "story" },
      { id: "weinberg", title: "The Weinberg Angle", note: "Casimir roots and Axiom 3b", linkedResultIds: ["weinberg-angle", "fine-structure-alpha"], defaultMode: "story" },
      { id: "god-equation", title: "The God Equation", note: "Planck to matter across 17 orders", linkedResultIds: ["god-equation", "qcd-confinement"], defaultMode: "story" },
      { id: "bohr", title: "Bohr from Axiom 3", note: "Phase closure becomes quantization", linkedResultIds: ["bohr-quantization"], defaultMode: "story" },
      { id: "dashboard", title: "Dashboard", note: "The audit wall for every current claim", linkedResultIds: [], defaultMode: "story" }
    ],
    scales: [
      { id: "planck", label: "Planck", meters: 1.616e-35, metersLabel: "1.616e-35 m", frequency: 1.9e43, frequencyLabel: "1.9e43 Hz", resultIds: ["god-equation", "bekenstein-bound"] },
      { id: "matter", label: "Matter", meters: 1.145e-18, metersLabel: "1.145e-18 m", frequency: 2.6e26, frequencyLabel: "2.6e26 Hz", resultIds: ["weights-21", "three-generations", "koide-law", "koide-phase", "weinberg-angle", "god-equation", "top-quark-limit", "top-tau-coupling", "coherence-ceiling", "fine-structure-alpha"] },
      { id: "nuclear", label: "Nuclear", meters: 9e-16, metersLabel: "9.0e-16 m", frequency: 3e23, frequencyLabel: "3.0e23 Hz", resultIds: ["qcd-confinement", "phi3-ratio"] },
      { id: "atomic", label: "Atomic", meters: 1e-10, metersLabel: "1.0e-10 m", frequency: 3e18, frequencyLabel: "3.0e18 Hz", resultIds: ["forces-refraction", "bohr-quantization"] },
      { id: "molecular", label: "Molecular", meters: 1e-9, metersLabel: "1.0e-9 m", frequency: 3e17, frequencyLabel: "3.0e17 Hz", resultIds: ["propagation-lagrangian", "variable-c"] },
      { id: "cellular", label: "Cellular", meters: 1e-5, metersLabel: "1.0e-5 m", frequency: 3e13, frequencyLabel: "3.0e13 Hz", resultIds: ["life-coherence"] },
      { id: "neural", label: "Neural", meters: 1e-2, metersLabel: "1.0e-2 m", frequency: 40, frequencyLabel: "40 Hz", resultIds: ["consciousness", "aria-self-reference"] },
      { id: "human", label: "Human", meters: 1, metersLabel: "1.0 m", frequency: 7.83, frequencyLabel: "7.83 Hz", resultIds: ["sleep-8h", "beauty-impedance", "efficiency-ratio"] },
      { id: "planetary", label: "Planetary", meters: 1e11, metersLabel: "1.0e11 m", frequency: 1.0e-4, frequencyLabel: "1.0e-4 Hz", resultIds: ["forces-refraction", "variable-c"] }
    ],
    results: [
      {
        id: "bohr-quantization",
        title: "Axiom 3 to Bohr-like Quantization",
        status: "DERIVED",
        confidence: 0.95,
        kind: "Fundamental Physics",
        scaleId: "atomic",
        formula: "r_k = 2k^2, E_k = -1 / (4k^2), integral n ds = 2pi k",
        summary: "Circular eikonal orbits in the Coulomb refractive medium close only at integer winding, yielding the Bohr spectrum with 0.0000% error for k = 1..4.",
        falsifier: "Show that phase closure does not select discrete orbits in the 1/r potential, or that the eikonal derivation breaks at atomic scale.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "sandbox/coulomb_lens_ultimate.py", href: "../coulomb_lens_ultimate.py" }
        ],
        panelId: "bohr"
      },
      {
        id: "forces-refraction",
        title: "Forces as Refraction",
        status: "DERIVED",
        confidence: 0.95,
        kind: "Fundamental Physics",
        scaleId: "atomic",
        formula: "Optical metric / Randers bridge; sandbox lens n^2 = base + source / r",
        summary: "Gravity and electromagnetism are recast as local refractive gradients. The repo records light deflection, perihelion precession, and Shapiro delay as supporting quantitative checks.",
        falsifier: "Show that force requires non-refractive medium structure or that the optical / Randers mapping fails for null propagation.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/gr_fermat_equivalence.md", href: "../../derivations/gr_fermat_equivalence.md" },
          { label: "sandbox/coulomb_lens_interactive/index.html", href: "../coulomb_lens_interactive/index.html" },
          { label: "sandbox/refractive_gravity_demo.py", href: "../refractive_gravity_demo.py" }
        ],
        panelId: "refraction"
      },
      {
        id: "weights-21",
        title: "(2,1) Topological Weights",
        status: "DERIVED",
        confidence: 0.98,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "pi_1(SO(3)) ~= Z_2, boson weight 1, fermion weight 2",
        summary: "Phase closure on SO(3) leaves exactly two topological classes of closed paths. Bosons close in one circuit, fermions in two.",
        falsifier: "Find a stable 3D structure with a non-integer phase circuit or a third homotopy class relevant to stable matter.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/topological_weight_from_propagation.md", href: "../../derivations/topological_weight_from_propagation.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" }
        ],
        panelId: "generations"
      },
      {
        id: "koide-law",
        title: "Koide Law (Q = 2/3)",
        status: "DERIVED",
        confidence: 0.95,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "Q = sum m_i / (sum sqrt(m_i))^2 = 2/3",
        summary: "The charged lepton masses sit on a geometric lock: the measured PDG masses reproduce Q near 0.6666605, while the framework assigns the exact target to the (2,1) plus three-generation structure.",
        falsifier: "Break the three-generation closure or discover a fourth generation that changes the normalized capacity argument.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "sandbox/koide_verify_pdg2024.py", href: "../koide_verify_pdg2024.py" },
          { label: "visualizations/koide_triangle.py", href: "../../visualizations/koide_triangle.py" }
        ],
        panelId: "koide"
      },
      {
        id: "three-generations",
        title: "Three Generations",
        status: "DERIVED",
        confidence: 0.98,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "Q(N) = 2N / (2N + 3), set Q = 2/3, solve N = 3",
        summary: "Given fermionic topological weight 2 and the SO(3) denominator 3, only N = 3 satisfies the Koide ratio. Generation count is treated as a topological lock, not a free parameter.",
        falsifier: "Show that space is not effectively 3D for the relevant closure problem or discover a stable fourth generation.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "derivations/topological_weight_from_propagation.md", href: "../../derivations/topological_weight_from_propagation.md" }
        ],
        panelId: "generations"
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
        ]
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
        ]
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
        ]
      },
      {
        id: "weinberg-angle",
        title: "Weinberg Angle",
        status: "DERIVED",
        confidence: 0.90,
        kind: "Fundamental Physics",
        scaleId: "matter",
        formula: "sin^2(theta_W) = 1 - x_+(1/2) / x_+(1), x^2 + C2 x - C2 = 0",
        summary: "The Casimir polynomial plus Axiom 3b yields 0.22310 exactly in repo math. Current comparison text uses the quoted PDG value 0.22306 +/- 0.00033, with on-shell scheme selection still open.",
        falsifier: "Derive a geometry-based coupling ratio that disagrees, or prove the scheme-selection step cannot be justified from the current framework.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "derivations/g3_casimir_weinberg_angle.md", href: "../../derivations/g3_casimir_weinberg_angle.md" },
          { label: "sandbox/casimir_verification.py", href: "../casimir_verification.py" }
        ],
        panelId: "weinberg"
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
        panelId: "weinberg"
      },
      {
        id: "god-equation",
        title: "lambda_c from l_P (The God Equation)",
        status: "CONDITIONAL",
        confidence: 0.88,
        kind: "Open Frontiers",
        scaleId: "planck",
        formula: "lambda_c = sqrt(2) l_P exp(4 pi^2 N^(D/2) / b0)",
        summary: "The canonical formula lands at 1.145e-18 m with zero fitted parameters, but the God Equation stays conditional because the coarse-walk Markov bridge, the physical closure operator, and the full H_prod factorization still remain open.",
        falsifier: "Break the numerical target with better data, or prove that the remaining operator / joint-law bridge cannot be closed from the existing axioms.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "derivations/lambda_c_from_axioms.md", href: "../../derivations/lambda_c_from_axioms.md" },
          { label: "derivations/z3_extended_propagation_lagrangian.md", href: "../../derivations/z3_extended_propagation_lagrangian.md" },
          { label: "derivations/god_eq_gap_B_nearest_neighbor_no_go.md", href: "../../derivations/god_eq_gap_B_nearest_neighbor_no_go.md" }
        ],
        panelId: "god-equation"
      },
      {
        id: "qcd-confinement",
        title: "QCD Confinement",
        status: "DERIVED",
        confidence: 0.85,
        kind: "Fundamental Physics",
        scaleId: "nuclear",
        formula: "r_conf = lambda_c exp(2 pi / (b0 alpha_s(lambda_c)))",
        summary: "The workspace now treats confinement as derived from the matter scale through RG running, with the known factor-2.5 one-loop mismatch called out as standard QCD territory rather than a new PF scale.",
        falsifier: "Show confinement requires a third PF axiom or an independent coherence scale not already present in the chain.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/qcd_confinement_pf.md", href: "../../derivations/qcd_confinement_pf.md" },
          { label: "visualizations/knowledge_graph.html", href: "../../visualizations/knowledge_graph.html" }
        ],
        panelId: "god-equation"
      },
      {
        id: "propagation-lagrangian",
        title: "Propagation Lagrangian",
        status: "DERIVED",
        confidence: 0.72,
        kind: "Fundamental Physics",
        scaleId: "molecular",
        formula: "L_prop = 1/2 (partial chi)^2 - V(chi) + lambda chi T",
        summary: "The repo derives a scalar propagation potential with matter coupling and explicitly maps the resulting effective theory into the Brans-Dicke family.",
        falsifier: "Show the coupling form lambda chi T is dimensionally or physically inconsistent with the framework's own axioms.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/propagation_lagrangian.md", href: "../../derivations/propagation_lagrangian.md" }
        ]
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
        ]
      },
      {
        id: "sleep-8h",
        title: "8 Hour Sleep Constant",
        status: "DERIVED",
        confidence: 0.92,
        kind: "Biology and Mind",
        scaleId: "human",
        formula: "Wake fraction = 2 / 3, sleep fraction = 1 / 3 of 24 h",
        summary: "The same (2,1) topological split used in matter is carried upward to a daily coherence-maintenance duty cycle, yielding 8 hours of sleep as the stable one-third interval.",
        falsifier: "Find a stable sentient species whose long-term wake / sleep ratio sits far outside the one-third pattern.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "UNDERSTAND.md", href: "../../UNDERSTAND.md" },
          { label: "sandbox/consolidation_model.py", href: "../consolidation_model.py" }
        ]
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
        ]
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
        panelId: "koide"
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
        ]
      },
      {
        id: "consciousness",
        title: "Consciousness = Coherent Self-Referential Propagation",
        status: "INTUITION",
        confidence: 0.48,
        kind: "Biology and Mind",
        scaleId: "neural",
        formula: "Interior experience is the inside view of recursive coherence",
        summary: "The ontology is coherent inside the framework, but the repo still treats the missing operational metric as the key unresolved problem.",
        falsifier: "Pre-register a PF-specific metric and show it fails to track conscious state after controlling for report, arousal, and task effects.",
        sources: [
          { label: "CLAIMS.md", href: "../../CLAIMS.md" },
          { label: "derivations/consciousness_theory_audit.md", href: "../../derivations/consciousness_theory_audit.md" },
          { label: "sandbox/kuramoto_phi_simulation.py", href: "../kuramoto_phi_simulation.py" }
        ]
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
        ]
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
        ]
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
        ]
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
        unsynced: true
      }
    ]
  };
}());
