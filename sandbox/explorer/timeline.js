/**
 * Derivation Timeline — Visual Chronology of the Propagation Framework
 *
 * Shows: Axioms → intermediate results → current frontier
 * Confidence at discovery vs. current
 * The derivation path as the primary visual, not just chronological time
 */
(function () {
  'use strict';

  // ── Timeline node data ────────────────────────────────────────────────────────
  // Ordered by derivation chain: axioms first, then dependencies
  // Confidence: [discovery, current] — shows how confidence evolved

  var TIMELINE_NODES = [
    {
      id: 'axiom1',
      label: 'Axiom 1',
      shortLabel: 'Prop.',
      title: 'Propagation is Fundamental',
      status: 'axiom',
      confidence: [1.0, 1.0],
      type: 'axiom',
      date: 'Foundation',
      dependents: ['bohr-quantization', 'forces-refraction', 'koide-law', 'three-generations', 'weights-21', 'god-equation']
    },
    {
      id: 'axiom2',
      label: 'Axiom 2',
      shortLabel: 'c',
      title: 'Finite Causal Velocity',
      status: 'axiom',
      confidence: [1.0, 1.0],
      type: 'axiom',
      date: 'Foundation',
      dependents: ['bohr-quantization', 'forces-refraction', 'god-equation', 'top-quark-limit', 'life-coherence']
    },
    {
      id: 'axiom3',
      label: 'Axiom 3',
      shortLabel: 'Coh.',
      title: 'Coherence',
      status: 'axiom',
      confidence: [1.0, 1.0],
      type: 'axiom',
      date: 'Foundation',
      dependents: ['koide-law', 'weights-21', 'three-generations', 'forces-refraction', 'bohr-quantization', 'god-equation', 'weinberg-angle']
    },
    {
      id: 'axiom3b',
      label: 'Axiom 3b',
      shortLabel: 'Min Wind.',
      title: 'Minimal Winding Principle',
      status: 'axiom',
      confidence: [0.9, 0.92],
      type: 'axiom',
      date: 'March 2026',
      dependents: ['weinberg-angle']
    },
    {
      id: 'weights-21',
      label: '(2,1) Weights',
      shortLabel: '(2,1)',
      title: 'Topological Closure Orders',
      status: 'PARTIAL DERIVATION',
      confidence: [0.80, 0.85],
      type: 'result',
      date: 'March 2026',
      dependents: ['koide-law', 'three-generations']
    },
    {
      id: 'koide-law',
      label: 'Koide Q=2/3',
      shortLabel: 'Koide',
      title: 'Koide Mass Relation',
      status: 'DERIVED',
      confidence: [0.90, 0.95],
      type: 'result',
      date: 'March 2026',
      dependents: ['three-generations', 'koide-phase', 'fine-structure-alpha']
    },
    {
      id: 'forces-refraction',
      label: 'Gravity Refraction',
      shortLabel: 'Grav.',
      title: 'Gravity as Refraction',
      status: 'DERIVED',
      confidence: [0.92, 0.95],
      type: 'result',
      date: 'March 2026',
      dependents: []
    },
    {
      id: 'bohr-quantization',
      label: 'Bohr Phase',
      shortLabel: 'Bohr',
      title: 'Bohr-like Phase Closure',
      status: 'CONDITIONAL',
      confidence: [0.72, 0.78],
      type: 'result',
      date: 'March 2026',
      dependents: []
    },
    {
      id: 'weinberg-angle',
      label: 'Weinberg θ',
      shortLabel: 'Wθ',
      title: 'Weinberg Angle',
      status: 'DERIVED',
      confidence: [0.85, 0.90],
      type: 'result',
      date: 'March 2026',
      dependents: ['fine-structure-alpha']
    },
    {
      id: 'three-generations',
      label: 'N = 3',
      shortLabel: 'Gen',
      title: 'Three Generations Required',
      status: 'CONDITIONAL',
      confidence: [0.78, 0.85],
      type: 'result',
      date: 'March 2026',
      dependents: []
    },
    {
      id: 'god-equation',
      label: 'λ_c',
      shortLabel: 'λc',
      title: 'God Equation (Planck → Matter)',
      status: 'CONDITIONAL',
      confidence: [0.82, 0.88],
      type: 'result',
      date: 'March 2026',
      dependents: ['top-quark-limit', 'top-tau-coupling']
    }
  ];

  // Status colors
  var STATUS_COLORS = {
    axiom: '#9b59b6',
    DERIVED: '#44ff88',
    CONDITIONAL: '#ffaa00',
    'PARTIAL DERIVATION': '#00cfff',
    ARGUED: '#ff6b6b',
    EMPIRICAL: '#ffdd55',
    INTUITION: '#ff92d2',
    UNSYNCED: '#d9a2ff'
  };

  // ── Build chain graph ──────────────────────────────────────────────────────────
  // Lay out nodes in derivation order: axioms at top, results below, dependents to the right

  function buildChainLayout() {
    var nodes = TIMELINE_NODES;
    var levels = [];
    var placed = new Set();
    var maxDepth = 4;

    // Assign levels by topological depth
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

    // Group by level
    var byLevel = {};
    nodes.forEach(function (n) {
      var l = Math.min(n._level, maxDepth);
      if (!byLevel[l]) byLevel[l] = [];
      byLevel[l].push(n);
    });

    // Assign x/y
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

  // ── Render ────────────────────────────────────────────────────────────────────

  function renderTimeline(container) {
    var layout = buildChainLayout();
    var nodes = layout.nodes;
    var byLevel = layout.byLevel;
    var maxDepth = layout.maxDepth;

    var numLevels = Object.keys(byLevel).length;
    var nodeHeight = 72;
    var levelGap = 40;
    var axiomGap = 16;
    var padding = { x: 32, y: 48 };

    // Find max nodes per level for sizing
    var maxPerLevel = Math.max.apply(Math, Object.keys(byLevel).map(function (l) { return byLevel[l].length; }));

    var svgWidth  = (numLevels * 260) + padding.x * 2;
    var svgHeight = (maxPerLevel * (nodeHeight + axiomGap)) + padding.y * 2;

    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', svgWidth);
    svg.setAttribute('height', svgHeight);
    svg.setAttribute('viewBox', '0 0 ' + svgWidth + ' ' + svgHeight);
    svg.style.display = 'block';

    // Defs: gradients, arrow markers
    var defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');

    // Glow filter
    var glowFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
    glowFilter.setAttribute('id', 'tl-glow');
    glowFilter.innerHTML =
      '<feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>' +
      '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>';
    defs.appendChild(glowFilter);

    // Arrow marker
    ['derived', 'conditional', 'argued', 'partial', 'empirical'].forEach(function (type) {
      var marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
      marker.setAttribute('id', 'arrow-' + type);
      marker.setAttribute('markerWidth', '8');
      marker.setAttribute('markerHeight', '8');
      marker.setAttribute('refX', '6');
      marker.setAttribute('refY', '3');
      marker.setAttribute('orient', 'auto');
      marker.innerHTML = '<path d="M0,0 L0,6 L8,3 z" fill="' + {
        derived: '#44ff88',
        conditional: '#ffaa00',
        argued: '#ff6b6b',
        partial: '#00cfff',
        empirical: '#ffdd55'
      }[type] + '" opacity="0.7"/>';
      defs.appendChild(marker);
    });

    svg.appendChild(defs);

    var g = document.createElementNS('http://www.w3.org/2000/svg', 'g');

    // Draw links first (behind nodes)
    var linkGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    linkGroup.setAttribute('class', 'tl-links');

    nodes.forEach(function (node) {
      if (!node.dependents) return;
      var nodeX = padding.x + node._x * 260 + 130;
      var nodeY = padding.y + node._y * (nodeHeight + axiomGap) + nodeHeight / 2;

      node.dependents.forEach(function (depId) {
        var dep = nodes.find(function (n) { return n.id === depId; });
        if (!dep) return;

        var depX = padding.x + dep._x * 260 + 130;
        var depY = padding.y + dep._y * (nodeHeight + axiomGap) + nodeHeight / 2;

        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        var color = STATUS_COLORS[node.status] || '#666';
        var mtype = node.status === 'DERIVED' ? 'derived'
          : node.status === 'CONDITIONAL' ? 'conditional'
          : node.status === 'PARTIAL DERIVATION' ? 'partial'
          : node.status === 'ARGUED' ? 'argued'
          : 'empirical';
        var d = 'M' + (nodeX + 40) + ',' + nodeY
          + ' C' + (nodeX + 120) + ',' + nodeY
          + ' ' + (depX - 120) + ',' + depY
          + ' ' + (depX - 40) + ',' + depY;
        path.setAttribute('d', d);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', color);
        path.setAttribute('stroke-width', '1.5');
        path.setAttribute('stroke-opacity', '0.4');
        path.setAttribute('marker-end', 'url(#arrow-' + mtype + ')');
        linkGroup.appendChild(path);
      });
    });
    g.appendChild(linkGroup);

    // Draw nodes
    var nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    nodeGroup.setAttribute('class', 'tl-nodes');

    nodes.forEach(function (node) {
      var x = padding.x + node._x * 260;
      var y = padding.y + node._y * (nodeHeight + axiomGap);
      var color = STATUS_COLORS[node.status] || '#666';
      var isAxiom = node.type === 'axiom';

      // Node background rect
      var rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', x);
      rect.setAttribute('y', y);
      rect.setAttribute('width', '260');
      rect.setAttribute('height', String(nodeHeight));
      rect.setAttribute('rx', '14');
      rect.setAttribute('fill', 'rgba(9, 21, 37, 0.85)');
      rect.setAttribute('stroke', color);
      rect.setAttribute('stroke-width', isAxiom ? '2' : '1.5');
      rect.setAttribute('stroke-opacity', isAxiom ? '0.8' : '0.6');
      rect.style.cursor = 'pointer';
      rect.style.transition = 'stroke-opacity 0.2s';
      nodeGroup.appendChild(rect);

      // Status indicator dot
      var dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('cx', x + 18);
      dot.setAttribute('cy', y + 18);
      dot.setAttribute('r', '5');
      dot.setAttribute('fill', color);
      nodeGroup.appendChild(dot);

      // Label
      var label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', x + 32);
      label.setAttribute('y', y + 22);
      label.setAttribute('fill', '#e8f0ff');
      label.setAttribute('font-family', 'Spectral, Georgia, serif');
      label.setAttribute('font-size', '12');
      label.setAttribute('font-weight', '600');
      label.textContent = node.label;
      nodeGroup.appendChild(label);

      // Short title (truncated)
      var shortTitle = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      shortTitle.setAttribute('x', x + 14);
      shortTitle.setAttribute('y', y + 42);
      shortTitle.setAttribute('fill', '#8ba3bd');
      shortTitle.setAttribute('font-family', 'DM Sans, sans-serif');
      shortTitle.setAttribute('font-size', '9');
      shortTitle.textContent = node.title.substring(0, 38);
      nodeGroup.appendChild(shortTitle);

      // Confidence badge
      var confBadge = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      var confRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      confRect.setAttribute('x', x + 160);
      confRect.setAttribute('y', y + 14);
      confRect.setAttribute('width', '88');
      confRect.setAttribute('height', '44');
      confRect.setAttribute('rx', '8');
      confRect.setAttribute('fill', 'rgba(0,0,0,0.25)');
      confRect.setAttribute('stroke', 'rgba(255,255,255,0.06)');
      confRect.setAttribute('stroke-width', '1');
      confBadge.appendChild(confRect);

      var confLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      confLabel.setAttribute('x', x + 204);
      confLabel.setAttribute('y', y + 26);
      confLabel.setAttribute('text-anchor', 'middle');
      confLabel.setAttribute('fill', '#8ba3bd');
      confLabel.setAttribute('font-family', 'JetBrains Mono, monospace');
      confLabel.setAttribute('font-size', '9');
      confLabel.textContent = 'CONF';
      confBadge.appendChild(confLabel);

      var confValue = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      confValue.setAttribute('x', x + 204);
      confValue.setAttribute('y', y + 50);
      confValue.setAttribute('text-anchor', 'middle');
      confValue.setAttribute('fill', color);
      confValue.setAttribute('font-family', 'JetBrains Mono, monospace');
      confValue.setAttribute('font-size', '14');
      confValue.setAttribute('font-weight', '600');
      confValue.textContent = node.confidence[1].toFixed(2);
      confBadge.appendChild(confValue);

      // Change indicator
      if (node.confidence[1] !== node.confidence[0]) {
        var delta = node.confidence[1] - node.confidence[0];
        var deltaText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        deltaText.setAttribute('x', x + 248);
        deltaText.setAttribute('y', y + 52);
        deltaText.setAttribute('text-anchor', 'end');
        deltaText.setAttribute('font-family', 'JetBrains Mono, monospace');
        deltaText.setAttribute('font-size', '8');
        deltaText.setAttribute('fill', delta > 0 ? '#69ff94' : '#ff6b6b');
        deltaText.textContent = (delta > 0 ? '+' : '') + delta.toFixed(2);
        confBadge.appendChild(deltaText);
      }

      nodeGroup.appendChild(confBadge);

      // Click interaction: show tooltip
      (function (nodeData, nodeRect) {
        nodeRect.addEventListener('click', function () {
          showTimelineTooltip(nodeData);
        });
        nodeRect.style.pointerEvents = 'all';
      })(node, rect);
    });

    g.appendChild(nodeGroup);
    svg.appendChild(g);

    // Horizontal column labels (axiom / results / frontier)
    var labelY = svgHeight - 12;
    [
      { x: padding.x, label: 'AXIOMS' },
      { x: padding.x + 260, label: 'INTERMEDIATE' },
      { x: padding.x + 2 * 260, label: 'RESULTS' },
      { x: padding.x + 3 * 260, label: 'FRONTIER' }
    ].forEach(function (col) {
      var colLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      colLabel.setAttribute('x', col.x + 130);
      colLabel.setAttribute('y', labelY);
      colLabel.setAttribute('text-anchor', 'middle');
      colLabel.setAttribute('fill', 'rgba(139, 163, 189, 0.4)');
      colLabel.setAttribute('font-family', 'DM Sans, sans-serif');
      colLabel.setAttribute('font-size', '9');
      colLabel.setAttribute('letter-spacing', '2');
      colLabel.textContent = col.label;
      svg.appendChild(colLabel);
    });

    container.appendChild(svg);
  }

  // ── Timeline tooltip ──────────────────────────────────────────────────────────

  function showTimelineTooltip(node) {
    var color = STATUS_COLORS[node.status] || '#666';
    var delta = node.confidence[1] - node.confidence[0];
    var deltaStr = delta !== 0
      ? '<span style="color:' + (delta > 0 ? '#69ff94' : '#ff6b6b') + ';font-family:var(--formula);font-size:0.78em"> ' + (delta > 0 ? '+' : '') + delta.toFixed(2) + '</span>'
      : '';

    var html =
      '<div class="tt-header">' +
        '<span class="tt-status-dot" style="background:' + color + '"></span>' +
        '<strong>' + node.title + '</strong>' +
      '</div>' +
      '<div class="tt-meta">' +
        '<span class="tt-status-label" style="color:' + color + '">' + node.status + '</span>' +
        '<span class="tt-date">' + node.date + '</span>' +
      '</div>' +
      '<div class="tt-confidence">' +
        '<span class="tt-conf-label">Confidence:</span>' +
        '<span class="tt-conf-value" style="color:' + color + '">' + node.confidence[1].toFixed(2) + '</span>' +
        deltaStr +
      '</div>';

    // Show a temporary tooltip
    var existing = document.querySelector('.tl-tooltip');
    if (existing) existing.remove();

    var tooltip = document.createElement('div');
    tooltip.className = 'tl-tooltip';
    tooltip.innerHTML = html;
    tooltip.style.cssText =
      'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);' +
      'z-index:100;padding:20px 24px;border-radius:18px;' +
      'border:1px solid var(--line-strong);background:rgba(5,13,26,0.98);' +
      'backdrop-filter:blur(12px);min-width:280px;pointer-events:none;' +
      'animation:tlFadeIn 0.2s ease;box-shadow:0 20px 60px rgba(0,0,0,0.5)';
    document.body.appendChild(tooltip);

    setTimeout(function () {
      if (tooltip.parentNode) tooltip.remove();
    }, 2500);
  }

  // ── CSS for tooltip ──────────────────────────────────────────────────────────

  function injectTimelineCSS() {
    if (document.getElementById('tl-styles')) return;
    var style = document.createElement('style');
    style.id = 'tl-styles';
    style.textContent =
      '@keyframes tlFadeIn { from { opacity: 0; transform: translate(-50%,-50%) scale(0.95); } to { opacity: 1; transform: translate(-50%,-50%) scale(1); } }' +
      '.tl-tooltip .tt-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }' +
      '.tl-tooltip .tt-status-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }' +
      '.tl-tooltip strong { font-family: var(--headline); font-size: 0.95rem; color: var(--text); }' +
      '.tl-tooltip .tt-meta { display: flex; gap: 12px; align-items: center; margin-bottom: 10px; }' +
      '.tl-tooltip .tt-status-label { font-family: var(--ui); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; }' +
      '.tl-tooltip .tt-date { font-family: var(--ui); font-size: 0.72rem; color: var(--muted); }' +
      '.tl-tooltip .tt-confidence { display: flex; align-items: center; gap: 6px; }' +
      '.tl-tooltip .tt-conf-label { font-family: var(--ui); font-size: 0.78rem; color: var(--muted); }' +
      '.tl-tooltip .tt-conf-value { font-family: var(--formula); font-size: 1rem; font-weight: 600; }';
    document.head.appendChild(style);
  }

  // ── Public API ────────────────────────────────────────────────────────────────

  window.DerivationTimeline = {
    init: function (containerId) {
      var container = document.getElementById(containerId);
      if (!container) return;
      injectTimelineCSS();
      renderTimeline(container);
    }
  };
}());
