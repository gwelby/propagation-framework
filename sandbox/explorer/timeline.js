/**
 * Derivation Timeline — Visual Chronology of the Propagation Framework
 *
 * Shows: Axioms → intermediate results → current frontier
 * Confidence at discovery vs. current
 * The derivation path as the primary visual, not just chronological time
 * 
 * Enhanced with complete derivation chains and interactive features.
 */
(function () {
  'use strict';

  // ── Status Configuration ───────────────────────────────────────────────────────
  var STATUS_CONFIG = {
    axiom: { color: '#9b59b6', label: 'AXIOM', bg: 'rgba(155, 89, 182, 0.15)' },
    DERIVED: { color: '#44ff88', label: 'DERIVED', bg: 'rgba(68, 255, 136, 0.15)' },
    CONDITIONAL: { color: '#ffaa00', label: 'CONDITIONAL', bg: 'rgba(255, 170, 0, 0.15)' },
    'PARTIAL DERIVATION': { color: '#00cfff', label: 'PARTIAL', bg: 'rgba(0, 207, 255, 0.15)' },
    ARGUED: { color: '#ff6b6b', label: 'ARGUED', bg: 'rgba(255, 107, 107, 0.15)' },
    EMPIRICAL: { color: '#ffdd55', label: 'EMPIRICAL', bg: 'rgba(255, 221, 85, 0.15)' },
    INTUITION: { color: '#ff92d2', label: 'INTUITION', bg: 'rgba(255, 146, 210, 0.15)' },
    UNSYNCED: { color: '#d9a2ff', label: 'UNSYNCED', bg: 'rgba(217, 162, 255, 0.15)' }
  };

  // ── Timeline node data ────────────────────────────────────────────────────────
  // Ordered by derivation chain: axioms first, then dependencies
  // Confidence: [discovery, current] — shows how confidence evolved

  var TIMELINE_NODES = [
    // ── AXIOMS ──────────────────────────────────────────────────────────────────
    {
      id: 'axiom1',
      label: 'Axiom 1',
      shortLabel: 'Prop.',
      title: 'Propagation is Fundamental',
      formula: '∃x: Propagates(x) ↔ Exists(x)',
      status: 'axiom',
      confidence: [1.0, 1.0],
      type: 'axiom',
      date: 'Foundation',
      description: 'Everything that exists propagates. The Medium is the minimal causal-coherence structure required for propagation.',
      chain: 'all',
      dependents: ['bohr-quantization', 'forces-refraction', 'koide-law', 'three-generations', 'weights-21', 'god-equation']
    },
    {
      id: 'axiom2',
      label: 'Axiom 2',
      shortLabel: 'c',
      title: 'Finite Causal Velocity',
      formula: '∀M, ∀x ∈ M: |v_causal(x)| ≤ c_M',
      status: 'axiom',
      confidence: [1.0, 1.0],
      type: 'axiom',
      date: 'Foundation',
      description: 'Every Medium has a finite upper bound on controllable causal influence.',
      chain: 'all',
      dependents: ['bohr-quantization', 'forces-refraction', 'god-equation', 'top-quark-limit', 'life-coherence']
    },
    {
      id: 'axiom3',
      label: 'Axiom 3',
      shortLabel: 'Coh.',
      title: 'Coherence',
      formula: 'Stable ↔ Coherent(Propagation)',
      status: 'axiom',
      confidence: [1.0, 1.0],
      type: 'axiom',
      date: 'Foundation',
      description: 'Stable structure requires coherent propagation. Incoherent modes disperse.',
      chain: 'all',
      dependents: ['koide-law', 'weights-21', 'three-generations', 'forces-refraction', 'bohr-quantization', 'god-equation', 'weinberg-angle']
    },
    {
      id: 'axiom3b',
      label: 'Axiom 3b',
      shortLabel: 'Min Wind.',
      title: 'Minimal Winding Principle',
      formula: 'W_min = 1 ⇒ Selection',
      status: 'axiom',
      confidence: [0.9, 0.92],
      type: 'axiom',
      date: 'March 2026',
      description: 'Minimal winding number in propagation geometry selects preferred states.',
      chain: 'weinberg',
      dependents: ['weinberg-angle', 'casimir-poly']
    },

    // ── WEINBERG ANGLE CHAIN ───────────────────────────────────────────────────
    {
      id: 'casimir-poly',
      label: 'Casimir Polynomial',
      shortLabel: 'C₂(x)',
      title: 'Casimir Eigenvalue Polynomial',
      formula: 'x_±(j) = [1 ± √(1 + 8j(j+1))]/4',
      status: 'DERIVED',
      confidence: [0.85, 0.90],
      type: 'result',
      date: 'March 2026',
      description: 'From bounded Casimir operators with angular sector structure.',
      chain: 'weinberg',
      parents: ['axiom3b'],
      dependents: ['weinberg-angle']
    },
    {
      id: 'weinberg-angle',
      label: 'Weinberg θ',
      shortLabel: 'Wθ',
      title: 'Weinberg Angle',
      formula: 'sin²θ_W = x_+(1/2)/x_+(1) = 0.22310',
      status: 'DERIVED',
      confidence: [0.85, 0.90],
      type: 'result',
      date: 'March 2026',
      description: 'Electroweak mixing angle derived from minimal winding and Casimir structure.',
      chain: 'weinberg',
      parents: ['axiom3b', 'casimir-poly'],
      dependents: ['fine-structure-alpha']
    },

    // ── KOIDE CHAIN ─────────────────────────────────────────────────────────────
    {
      id: 'three-resonances',
      label: '3 Resonances',
      shortLabel: 'N=3',
      title: 'Three Resonance Condition',
      formula: 'N = 3 required for stability',
      status: 'CONDITIONAL',
      confidence: [0.78, 0.85],
      type: 'result',
      date: 'March 2026',
      description: 'Three-generation kinematics from (2,1) weight closure.',
      chain: 'koide',
      parents: ['weights-21'],
      dependents: ['koide-law']
    },
    {
      id: '120-geometry',
      label: '120° Geometry',
      shortLabel: '120°',
      title: 'Phase Geometry',
      formula: 'φ = 2π/3 = 120°',
      status: 'DERIVED',
      confidence: [0.90, 0.95],
      type: 'result',
      date: 'March 2026',
      description: 'Phase angle from three-fold symmetry of generation structure.',
      chain: 'koide',
      parents: ['three-resonances'],
      dependents: ['foot-radius']
    },
    {
      id: 'foot-radius',
      label: 'Foot Radius',
      shortLabel: 'r_f',
      title: 'Koide Foot Radius',
      formula: 'r_f = (m₁ + m₂ + m₃) / (√m₁ + √m₂ + √m₃)²',
      status: 'DERIVED',
      confidence: [0.88, 0.93],
      type: 'result',
      date: 'March 2026',
      description: 'Geometric mean structure linking three masses.',
      chain: 'koide',
      parents: ['120-geometry'],
      dependents: ['koide-q']
    },
    {
      id: 'koide-q',
      label: 'Koide Q=2/3',
      shortLabel: 'Koide',
      title: 'Koide Mass Relation',
      formula: 'Q = (Σm_i)² / (3Σm_i²) = 2/3',
      status: 'DERIVED',
      confidence: [0.90, 0.95],
      type: 'result',
      date: 'March 2026',
      description: 'Mass ratio prediction verified to high precision across charged leptons.',
      chain: 'koide',
      parents: ['foot-radius', 'weights-21'],
      dependents: ['koide-phase', 'fine-structure-alpha']
    },

    // ── THREE GENERATIONS CHAIN ───────────────────────────────────────────────
    {
      id: 'weights-21',
      label: '(2,1) Weights',
      shortLabel: '(2,1)',
      title: 'Topological Closure Orders',
      formula: 'w = (2,1) → SU(2) × U(1)',
      status: 'PARTIAL DERIVATION',
      confidence: [0.80, 0.85],
      type: 'result',
      date: 'March 2026',
      description: 'Topological weights from coherence closure conditions.',
      chain: 'generations',
      parents: ['axiom3'],
      dependents: ['three-resonances', 'koide-law', 'generation-formula']
    },
    {
      id: 'generation-formula',
      label: 'Q(N) Formula',
      shortLabel: 'Q(N)',
      title: 'Generation Count Formula',
      formula: 'Q(N) = 2N/(2N+3)',
      status: 'DERIVED',
      confidence: [0.85, 0.90],
      type: 'result',
      date: 'March 2026',
      description: 'General formula for mass ratio as function of generation count.',
      chain: 'generations',
      parents: ['weights-21'],
      dependents: ['three-generations']
    },
    {
      id: 'three-generations',
      label: 'N = 3',
      shortLabel: 'Gen',
      title: 'Three Generations Required',
      formula: 'Q(3) = 6/9 = 2/3 ✓',
      status: 'CONDITIONAL',
      confidence: [0.78, 0.85],
      type: 'result',
      date: 'March 2026',
      description: 'Three generations required to match observed Koide ratio.',
      chain: 'generations',
      parents: ['generation-formula', 'koide-q'],
      dependents: []
    },

    // ── GOD EQUATION CHAIN ─────────────────────────────────────────────────────
    {
      id: 'z3-extension',
      label: 'ℤ₃ Extension',
      shortLabel: 'ℤ₃',
      title: 'ℤ₃ Circulant Extension',
      formula: 'S³ = 1, [S, S†] = circulant',
      status: 'CONDITIONAL',
      confidence: [0.82, 0.88],
      type: 'result',
      date: 'March 2026',
      description: 'Three-fold symmetric extension of propagation algebra.',
      chain: 'god-equation',
      parents: ['axiom3'],
      dependents: ['circulant-coupling']
    },
    {
      id: 'circulant-coupling',
      label: 'Circulant H',
      shortLabel: 'H_circ',
      title: 'Circulant Coupling Operator',
      formula: 'H_prod = aS† + bS†² + h.c.',
      status: 'CONDITIONAL',
      confidence: [0.80, 0.85],
      type: 'result',
      date: 'March 2026',
      description: 'Product operator for three-channel circulant dynamics.',
      chain: 'god-equation',
      parents: ['z3-extension'],
      dependents: ['lambda-c']
    },
    {
      id: 'lambda-c',
      label: 'λ_c',
      shortLabel: 'λc',
      title: 'God Equation (Planck → Matter)',
      formula: 'λ_c = √(ℏG/c³) · f(ℤ₃)',
      status: 'CONDITIONAL',
      confidence: [0.82, 0.88],
      type: 'result',
      date: 'March 2026',
      description: 'Characteristic length connecting Planck scale to matter emergence.',
      chain: 'god-equation',
      parents: ['circulant-coupling'],
      dependents: ['top-quark-limit', 'top-tau-coupling']
    },

    // ── OTHER RESULTS ───────────────────────────────────────────────────────────
    {
      id: 'forces-refraction',
      label: 'Gravity Refraction',
      shortLabel: 'Grav.',
      title: 'Gravity as Refraction',
      formula: 'F_g = −∇n_eff(r)',
      status: 'DERIVED',
      confidence: [0.92, 0.95],
      type: 'result',
      date: 'March 2026',
      description: 'Gravitational force emerges from refractive index gradient in Medium.',
      chain: 'all',
      parents: ['axiom1', 'axiom2'],
      dependents: []
    },
    {
      id: 'bohr-quantization',
      label: 'Bohr Phase',
      shortLabel: 'Bohr',
      title: 'Bohr-like Phase Closure',
      formula: '∮p·dq = nℏ',
      status: 'CONDITIONAL',
      confidence: [0.72, 0.78],
      type: 'result',
      date: 'March 2026',
      description: 'Quantization from phase coherence around closed orbits.',
      chain: 'all',
      parents: ['axiom1', 'axiom2'],
      dependents: []
    },
    {
      id: 'fine-structure-alpha',
      label: 'α',
      shortLabel: 'α',
      title: 'Fine Structure Constant',
      formula: 'α = e²/(4πε₀ℏc) ≈ 1/137',
      status: 'ARGUED',
      confidence: [0.55, 0.60],
      type: 'result',
      date: 'Open Frontier',
      description: 'All 5 routes fail — needs new input beyond Axioms 1-3.',
      chain: 'all',
      parents: ['weinberg-angle', 'koide-q'],
      dependents: []
    },
    {
      id: 'top-quark-limit',
      label: 'Top Limit',
      shortLabel: 'm_t',
      title: 'Top Quark Mass Bound',
      formula: 'm_t < λ_c · threshold',
      status: 'CONDITIONAL',
      confidence: [0.70, 0.75],
      type: 'result',
      date: 'March 2026',
      description: 'Upper bound on top quark mass from God Equation scale.',
      chain: 'god-equation',
      parents: ['lambda-c'],
      dependents: []
    },
    {
      id: 'koide-phase',
      label: 'Koide Phase',
      shortLabel: 'δ',
      title: 'Koide Phase Selector',
      formula: 'δ = 2/9 (T-021/T-022 NEGATIVE)',
      status: 'ARGUED',
      confidence: [0.45, 0.50],
      type: 'result',
      date: 'TOP PRIORITY',
      description: 'Phase selector for Koide relation — T-021/T-022 closed, alternative routes needed.',
      chain: 'koide',
      parents: ['koide-q'],
      dependents: []
    }
  ];

  // ── Derivation Chains ──────────────────────────────────────────────────────────
  var DERIVATION_CHAINS = {
    'weinberg': {
      name: 'Weinberg Angle',
      description: 'From Minimal Winding to electroweak mixing angle',
      nodes: ['axiom3b', 'casimir-poly', 'weinberg-angle']
    },
    'koide': {
      name: 'Koide Relation',
      description: 'Three resonances to Q = 2/3 mass formula',
      nodes: ['weights-21', 'three-resonances', '120-geometry', 'foot-radius', 'koide-q']
    },
    'generations': {
      name: 'Three Generations',
      description: 'Topological closure to generation count',
      nodes: ['weights-21', 'generation-formula', 'three-generations']
    },
    'god-equation': {
      name: 'God Equation',
      description: 'ℤ₃ extension to Planck-matter bridge',
      nodes: ['z3-extension', 'circulant-coupling', 'lambda-c']
    },
    'all': {
      name: 'All Chains',
      description: 'Complete derivation graph',
      nodes: null // Show all
    }
  };

  // ── Current filter state ─────────────────────────────────────────────────────
  var currentFilter = 'all';
  var selectedNodeId = null;

  // ── Build chain graph ─────────────────────────────────────────────────────────
  function buildChainLayout(filterChain) {
    var nodes = TIMELINE_NODES;
    if (filterChain && filterChain !== 'all') {
      var chain = DERIVATION_CHAINS[filterChain];
      if (chain && chain.nodes) {
        // Include axioms that are dependencies
        var chainIds = new Set(chain.nodes);
        var includeIds = new Set(chainIds);
        nodes.forEach(function(n) {
          if (chainIds.has(n.id)) {
            if (n.parents) n.parents.forEach(function(p) { includeIds.add(p); });
            if (n.dependents) n.dependents.forEach(function(d) { includeIds.add(d); });
          }
        });
        nodes = nodes.filter(function(n) { return includeIds.has(n.id); });
      }
    }

    var levels = [];
    var maxDepth = 4;

    function getLevel(id) {
      var node = nodes.find(function (n) { return n.id === id; });
      if (!node) return 0;
      if (node._level !== undefined) return node._level;

      if (node.type === 'axiom') {
        node._level = 0;
      } else if (!node.dependents || node.dependents.length === 0) {
        node._level = maxDepth;
      } else {
        var childLevels = node.dependents.map(getLevel);
        node._level = Math.max.apply(Math, childLevels) + 1;
      }
      return node._level;
    }

    nodes.forEach(function (n) { getLevel(n.id); });

    var byLevel = {};
    nodes.forEach(function (n) {
      var l = Math.min(n._level, maxDepth);
      if (!byLevel[l]) byLevel[l] = [];
      byLevel[l].push(n);
    });

    Object.keys(byLevel).forEach(function (level) {
      var levelNodes = byLevel[level];
      levelNodes.forEach(function (n, i) {
        n._x = parseInt(level);
        n._y = i;
        n._totalInLevel = levelNodes.length;
      });
    });

    return { nodes: nodes, byLevel: byLevel, maxDepth: maxDepth };
  }

  // ── Render Timeline ───────────────────────────────────────────────────────────
  function renderTimeline(container, filterChain) {
    container.innerHTML = '';
    var layout = buildChainLayout(filterChain);
    var nodes = layout.nodes;
    var byLevel = layout.byLevel;
    var maxDepth = layout.maxDepth;

    var numLevels = Object.keys(byLevel).length || 4;
    var nodeHeight = 88;
    var levelGap = 40;
    var axiomGap = 20;
    var padding = { x: 40, y: 60 };

    var maxPerLevel = Math.max.apply(Math, Object.keys(byLevel).map(function (l) { 
      return byLevel[l] ? byLevel[l].length : 1; 
    }));

    var svgWidth  = (numLevels * 280) + padding.x * 2;
    var svgHeight = Math.max((maxPerLevel * (nodeHeight + axiomGap)) + padding.y * 2, 500);

    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', svgHeight);
    svg.setAttribute('viewBox', '0 0 ' + svgWidth + ' ' + svgHeight);
    svg.style.display = 'block';
    svg.classList.add('timeline-svg');

    // Defs
    var defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');

    // Glow filter
    var glowFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
    glowFilter.setAttribute('id', 'tl-glow');
    glowFilter.innerHTML =
      '<feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>' +
      '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>';
    defs.appendChild(glowFilter);

    // Gradients for each status
    Object.keys(STATUS_CONFIG).forEach(function(status) {
      var grad = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
      grad.setAttribute('id', 'grad-' + status.replace(/\s+/g, '-'));
      grad.setAttribute('x1', '0%');
      grad.setAttribute('y1', '0%');
      grad.setAttribute('x2', '100%');
      grad.setAttribute('y2', '100%');
      var color = STATUS_CONFIG[status].color;
      grad.innerHTML = '<stop offset="0%" stop-color="' + color + '" stop-opacity="0.3"/>' +
        '<stop offset="100%" stop-color="' + color + '" stop-opacity="0.1"/>';
      defs.appendChild(grad);
    });

    // Arrow markers
    ['derived', 'conditional', 'argued', 'partial', 'empirical', 'axiom'].forEach(function (type) {
      var marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
      marker.setAttribute('id', 'arrow-' + type);
      marker.setAttribute('markerWidth', '10');
      marker.setAttribute('markerHeight', '10');
      marker.setAttribute('refX', '8');
      marker.setAttribute('refY', '4');
      marker.setAttribute('orient', 'auto');
      var colors = {
        derived: '#44ff88',
        conditional: '#ffaa00',
        argued: '#ff6b6b',
        partial: '#00cfff',
        empirical: '#ffdd55',
        axiom: '#9b59b6'
      };
      marker.innerHTML = '<path d="M0,0 L0,8 L10,4 z" fill="' + colors[type] + '" opacity="0.8"/>';
      defs.appendChild(marker);
    });

    svg.appendChild(defs);

    var g = document.createElementNS('http://www.w3.org/2000/svg', 'g');

    // Draw links
    var linkGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    linkGroup.setAttribute('class', 'tl-links');

    nodes.forEach(function (node) {
      if (!node.dependents) return;
      var nodeX = padding.x + node._x * 280 + 140;
      var nodeY = padding.y + node._y * (nodeHeight + axiomGap) + nodeHeight / 2;

      node.dependents.forEach(function (depId) {
        var dep = nodes.find(function (n) { return n.id === depId; });
        if (!dep) return;

        var depX = padding.x + dep._x * 280 + 140;
        var depY = padding.y + dep._y * (nodeHeight + axiomGap) + nodeHeight / 2;

        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        var color = STATUS_CONFIG[node.status] ? STATUS_CONFIG[node.status].color : '#666';
        var mtype = node.status === 'DERIVED' ? 'derived'
          : node.status === 'CONDITIONAL' ? 'conditional'
          : node.status === 'PARTIAL DERIVATION' ? 'partial'
          : node.status === 'ARGUED' ? 'argued'
          : node.status === 'axiom' ? 'axiom'
          : 'empirical';
        var d = 'M' + (nodeX + 50) + ',' + nodeY
          + ' C' + (nodeX + 130) + ',' + nodeY
          + ' ' + (depX - 130) + ',' + depY
          + ' ' + (depX - 50) + ',' + depY;
        path.setAttribute('d', d);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', color);
        path.setAttribute('stroke-width', '2');
        path.setAttribute('stroke-opacity', '0.5');
        path.setAttribute('marker-end', 'url(#arrow-' + mtype + ')');
        path.classList.add('chain-link');
        linkGroup.appendChild(path);
      });
    });
    g.appendChild(linkGroup);

    // Draw nodes
    var nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    nodeGroup.setAttribute('class', 'tl-nodes');

    nodes.forEach(function (node) {
      var x = padding.x + node._x * 280;
      var y = padding.y + node._y * (nodeHeight + axiomGap);
      var config = STATUS_CONFIG[node.status] || { color: '#666', bg: 'rgba(100,100,100,0.1)' };
      var isAxiom = node.type === 'axiom';
      var isSelected = selectedNodeId === node.id;

      // Node group
      var nodeG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      nodeG.setAttribute('class', 'timeline-node' + (isSelected ? ' selected' : ''));
      nodeG.setAttribute('data-id', node.id);
      nodeG.style.cursor = 'pointer';

      // Background rect with gradient
      var rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', x);
      rect.setAttribute('y', y);
      rect.setAttribute('width', '280');
      rect.setAttribute('height', String(nodeHeight));
      rect.setAttribute('rx', '16');
      rect.setAttribute('fill', 'url(#grad-' + node.status.replace(/\s+/g, '-') + ')');
      rect.setAttribute('stroke', config.color);
      rect.setAttribute('stroke-width', isSelected ? '3' : (isAxiom ? '2' : '1.5'));
      rect.setAttribute('stroke-opacity', isSelected ? '1' : (isAxiom ? '0.9' : '0.7'));
      rect.setAttribute('class', 'node-rect');
      nodeG.appendChild(rect);

      // Status indicator dot
      var dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('cx', x + 20);
      dot.setAttribute('cy', y + 20);
      dot.setAttribute('r', '6');
      dot.setAttribute('fill', config.color);
      nodeG.appendChild(dot);

      // Status label
      var statusLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      statusLabel.setAttribute('x', x + 34);
      statusLabel.setAttribute('y', y + 24);
      statusLabel.setAttribute('fill', config.color);
      statusLabel.setAttribute('font-family', 'JetBrains Mono, monospace');
      statusLabel.setAttribute('font-size', '9');
      statusLabel.setAttribute('font-weight', '600');
      statusLabel.textContent = config.label;
      nodeG.appendChild(statusLabel);

      // Node label
      var label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', x + 20);
      label.setAttribute('y', y + 45);
      label.setAttribute('fill', '#e8f0ff');
      label.setAttribute('font-family', 'Spectral, Georgia, serif');
      label.setAttribute('font-size', '14');
      label.setAttribute('font-weight', '600');
      label.textContent = node.label;
      nodeG.appendChild(label);

      // Formula (if fits)
      if (node.formula) {
        var formula = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        formula.setAttribute('x', x + 20);
        formula.setAttribute('y', y + 64);
        formula.setAttribute('fill', '#8ba3bd');
        formula.setAttribute('font-family', 'JetBrains Mono, monospace');
        formula.setAttribute('font-size', '10');
        formula.textContent = node.formula.substring(0, 35);
        nodeG.appendChild(formula);
      }

      // Confidence badge
      var confBadge = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      var confRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      confRect.setAttribute('x', x + 200);
      confRect.setAttribute('y', y + 12);
      confRect.setAttribute('width', '68');
      confRect.setAttribute('height', '36');
      confRect.setAttribute('rx', '8');
      confRect.setAttribute('fill', 'rgba(0,0,0,0.3)');
      confRect.setAttribute('stroke', 'rgba(255,255,255,0.08)');
      confRect.setAttribute('stroke-width', '1');
      confBadge.appendChild(confRect);

      var confLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      confLabel.setAttribute('x', x + 234);
      confLabel.setAttribute('y', y + 24);
      confLabel.setAttribute('text-anchor', 'middle');
      confLabel.setAttribute('fill', '#8ba3bd');
      confLabel.setAttribute('font-family', 'JetBrains Mono, monospace');
      confLabel.setAttribute('font-size', '8');
      confLabel.textContent = 'CONF';
      confBadge.appendChild(confLabel);

      var confValue = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      confValue.setAttribute('x', x + 234);
      confValue.setAttribute('y', y + 42);
      confValue.setAttribute('text-anchor', 'middle');
      confValue.setAttribute('fill', config.color);
      confValue.setAttribute('font-family', 'JetBrains Mono, monospace');
      confValue.setAttribute('font-size', '14');
      confValue.setAttribute('font-weight', '600');
      confValue.textContent = node.confidence[1].toFixed(2);
      confBadge.appendChild(confValue);

      nodeG.appendChild(confBadge);

      // Click interaction
      nodeG.addEventListener('click', function () {
        selectNode(node);
      });

      nodeGroup.appendChild(nodeG);
    });

    g.appendChild(nodeGroup);
    svg.appendChild(g);

    // Column labels
    var labelY = svgHeight - 20;
    var colLabels = ['AXIOMS', 'INTERMEDIATE', 'RESULTS', 'FRONTIER'];
    colLabels.forEach(function(label, i) {
      if (byLevel[i]) {
        var colLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        colLabel.setAttribute('x', padding.x + i * 280 + 140);
        colLabel.setAttribute('y', labelY);
        colLabel.setAttribute('text-anchor', 'middle');
        colLabel.setAttribute('fill', 'rgba(139, 163, 189, 0.5)');
        colLabel.setAttribute('font-family', 'DM Sans, sans-serif');
        colLabel.setAttribute('font-size', '10');
        colLabel.setAttribute('letter-spacing', '2');
        colLabel.setAttribute('font-weight', '600');
        colLabel.textContent = label;
        svg.appendChild(colLabel);
      }
    });

    container.appendChild(svg);
  }

  // ── Node Selection ───────────────────────────────────────────────────────────
  function selectNode(node) {
    selectedNodeId = node.id;
    
    // Re-render to update selection visual
    var container = document.getElementById('timelineContainer');
    if (container) {
      renderTimeline(container, currentFilter);
    }

    // Show detail panel
    showNodeDetail(node);
  }

  // ── Show Node Detail ─────────────────────────────────────────────────────────
  function showNodeDetail(node) {
    var panel = document.getElementById('nodeDetailPanel');
    if (!panel) return;

    var config = STATUS_CONFIG[node.status] || { color: '#666', label: 'UNKNOWN' };
    var delta = node.confidence[1] - node.confidence[0];
    var deltaStr = delta !== 0
      ? '<span class="confidence-delta" style="color:' + (delta > 0 ? '#69ff94' : '#ff6b6b') + '">' + (delta > 0 ? '+' : '') + delta.toFixed(2) + '</span>'
      : '';

    var parentsHtml = node.parents 
      ? node.parents.map(function(p) {
          var pnode = TIMELINE_NODES.find(function(n) { return n.id === p; });
          return pnode ? '<span class="detail-tag" data-id="' + p + '">' + pnode.label + '</span>' : '';
        }).join(' → ')
      : 'None (Axiom)';

    var childrenHtml = node.dependents && node.dependents.length > 0
      ? node.dependents.map(function(d) {
          var dnode = TIMELINE_NODES.find(function(n) { return n.id === d; });
          return dnode ? '<span class="detail-tag" data-id="' + d + '">' + dnode.label + '</span>' : '';
        }).join(', ')
      : 'None (Frontier)';

    var chainName = node.chain && DERIVATION_CHAINS[node.chain] 
      ? DERIVATION_CHAINS[node.chain].name 
      : 'General';

    panel.innerHTML =
      '<div class="detail-header" style="border-left-color:' + config.color + '">' +
        '<div class="detail-status" style="color:' + config.color + '">' + config.label + '</div>' +
        '<h3>' + node.title + '</h3>' +
        '<div class="detail-formula">' + (node.formula || '') + '</div>' +
      '</div>' +
      '<div class="detail-body">' +
        '<p class="detail-description">' + node.description + '</p>' +
        '<div class="detail-confidence">' +
          '<span class="conf-label">Confidence:</span>' +
          '<span class="conf-value" style="color:' + config.color + '">' + node.confidence[1].toFixed(2) + '</span>' +
          deltaStr +
        '</div>' +
        '<div class="detail-meta">' +
          '<div><strong>Date:</strong> ' + node.date + '</div>' +
          '<div><strong>Chain:</strong> ' + chainName + '</div>' +
        '</div>' +
        '<div class="detail-connections">' +
          '<div class="detail-parents"><strong>From:</strong> ' + parentsHtml + '</div>' +
          '<div class="detail-children"><strong>To:</strong> ' + childrenHtml + '</div>' +
        '</div>' +
      '</div>';

    panel.classList.add('active');

    // Add click handlers for tags
    panel.querySelectorAll('.detail-tag').forEach(function(tag) {
      tag.addEventListener('click', function() {
        var id = this.getAttribute('data-id');
        var n = TIMELINE_NODES.find(function(node) { return node.id === id; });
        if (n) selectNode(n);
      });
    });
  }

  // ── Filter Buttons ───────────────────────────────────────────────────────────
  function renderFilterButtons() {
    var container = document.getElementById('chainFilterButtons');
    if (!container) return;

    Object.keys(DERIVATION_CHAINS).forEach(function(chainId) {
      var chain = DERIVATION_CHAINS[chainId];
      var btn = document.createElement('button');
      btn.className = 'chain-filter-btn' + (chainId === currentFilter ? ' active' : '');
      btn.textContent = chain.name;
      btn.title = chain.description;
      btn.addEventListener('click', function() {
        currentFilter = chainId;
        updateFilterButtons();
        var timelineContainer = document.getElementById('timelineContainer');
        if (timelineContainer) {
          renderTimeline(timelineContainer, currentFilter);
        }
      });
      container.appendChild(btn);
    });
  }

  function updateFilterButtons() {
    var container = document.getElementById('chainFilterButtons');
    if (!container) return;

    container.querySelectorAll('.chain-filter-btn').forEach(function(btn, idx) {
      var chainId = Object.keys(DERIVATION_CHAINS)[idx];
      btn.classList.toggle('active', chainId === currentFilter);
    });
  }

  // ── Inject CSS ─────────────────────────────────────────────────────────────────
  function injectTimelineCSS() {
    if (document.getElementById('tl-enhanced-styles')) return;
    
    var style = document.createElement('style');
    style.id = 'tl-enhanced-styles';
    style.textContent =
      '.timeline-scroll-container { overflow-x: auto; padding: 20px 0; }' +
      '.timeline-svg { min-width: 100%; }' +
      '.timeline-node { transition: all 0.3s ease; }' +
      '.timeline-node:hover .node-rect { stroke-opacity: 1; filter: url(#tl-glow); }' +
      '.timeline-node.selected .node-rect { stroke-width: 3px; }' +
      '.chain-link { transition: stroke-opacity 0.3s; }' +
      '.chain-link:hover { stroke-opacity: 0.8; stroke-width: 3; }' +
      '.chain-filter-container { display: flex; gap: 10px; flex-wrap: wrap; padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); }' +
      '.chain-filter-btn { padding: 8px 16px; border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; background: rgba(0,0,0,0.3); color: #8ba3bd; font-family: "DM Sans", sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; }' +
      '.chain-filter-btn:hover { border-color: rgba(255,255,255,0.4); color: #e8f0ff; }' +
      '.chain-filter-btn.active { background: rgba(68, 255, 136, 0.2); border-color: #44ff88; color: #44ff88; }' +
      '#nodeDetailPanel { position: fixed; right: 20px; top: 100px; width: 320px; background: rgba(5, 13, 26, 0.98); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 20px; backdrop-filter: blur(12px); transform: translateX(400px); transition: transform 0.3s ease; z-index: 100; }' +
      '#nodeDetailPanel.active { transform: translateX(0); }' +
      '.detail-header { border-left: 4px solid; padding-left: 15px; margin-bottom: 20px; }' +
      '.detail-header h3 { margin: 5px 0; font-family: var(--headline); color: #e8f0ff; }' +
      '.detail-status { font-family: "JetBrains Mono", monospace; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }' +
      '.detail-formula { font-family: "JetBrains Mono", monospace; font-size: 12px; color: #8ba3bd; margin-top: 8px; }' +
      '.detail-description { color: #b8c5d6; line-height: 1.6; margin-bottom: 15px; }' +
      '.detail-confidence { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 8px; }' +
      '.conf-label { color: #8ba3bd; font-size: 12px; }' +
      '.conf-value { font-family: "JetBrains Mono", monospace; font-size: 18px; font-weight: 600; }' +
      '.confidence-delta { font-family: "JetBrains Mono", monospace; font-size: 12px; }' +
      '.detail-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; font-size: 12px; color: #8ba3bd; }' +
      '.detail-connections { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px; }' +
      '.detail-connections > div { margin-bottom: 8px; font-size: 12px; }' +
      '.detail-tag { display: inline-block; padding: 3px 8px; background: rgba(0, 207, 255, 0.15); border: 1px solid rgba(0, 207, 255, 0.3); border-radius: 4px; font-family: "JetBrains Mono", monospace; font-size: 10px; color: #00cfff; cursor: pointer; margin: 2px; transition: all 0.2s; }' +
      '.detail-tag:hover { background: rgba(0, 207, 255, 0.3); }';
    document.head.appendChild(style);
  }

  // ── Public API ──────────────────────────────────────────────────────────────────
  window.DerivationTimeline = {
    init: function (containerId) {
      injectTimelineCSS();
      renderFilterButtons();
      
      var container = document.getElementById(containerId);
      if (!container) return;
      
      // Create detail panel if not exists
      if (!document.getElementById('nodeDetailPanel')) {
        var panel = document.createElement('div');
        panel.id = 'nodeDetailPanel';
        document.body.appendChild(panel);
      }
      
      renderTimeline(container, currentFilter);
    },
    filter: function(chainId) {
      currentFilter = chainId;
      updateFilterButtons();
      var container = document.getElementById('timelineContainer');
      if (container) {
        renderTimeline(container, currentFilter);
      }
    }
  };
}());
