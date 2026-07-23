// Derivation Graph 3D — Three.js Force-Directed Graph
// In offline mode the 3D bundle may be absent; degrade to 2D-only honestly.
(function() {
  'use strict';

  let graph3DInstance = null;
  let is3DActive = false;
  let currentCategory = 'all';

  const COLORS = {
    DERIVED: '#44ff88',
    CONDITIONAL: '#ffaa00',
    'PARTIAL DERIVATION': '#00cfff',
    ARGUED: '#ff6b6b',
    EMPIRICAL: '#ffdd55',
    INTUITION: '#ff92d2',
    UNSYNCED: '#d9a2ff',
    axiom: '#9b59b6',
    background: '#07111c'
  };

  function getNodeColor(d) {
    if (d.type === 'axiom') return COLORS.axiom;
    return COLORS[d.status] || '#666';
  }

  function getNodeRadius(d) {
    if (d.type === 'axiom') return 12;
    return 5 + (d.confidence || 0) * 8;
  }

  function showUnavailableMessage(container) {
    container.innerHTML =
      '<div class="note-box" style="margin:24px;text-align:left">' +
        '<strong>3D graph unavailable</strong>' +
        '<p>This offline build keeps the audited 2D derivation graph fully local. The optional 3D force-graph bundle is not vendored here.</p>' +
      '</div>';
  }

  function buildGraphData(category) {
    const results = window.PFTruth ? window.PFTruth.getAuditedResults() : [];
    const nodes = [];
    const links = [];
    const nodeMap = new Map();

    // Axiom nodes
    const axioms = [
      { id: 'axiom1', title: 'Axiom 1: Propagation', shortTitle: 'A1: Propagation', type: 'axiom', status: 'axiom', confidence: 1.0, description: 'Everything that exists propagates.' },
      { id: 'axiom2', title: 'Axiom 2: Finite Causal Velocity', shortTitle: 'A2: Finite c', type: 'axiom', status: 'axiom', confidence: 1.0, description: 'No causal influence propagates faster than c.' },
      { id: 'axiom3', title: 'Axiom 3: Coherence', shortTitle: 'A3: Coherence', type: 'axiom', status: 'axiom', confidence: 1.0, description: 'Stable structure requires self-reinforcing propagation.' },
      { id: 'axiom3b', title: 'Axiom 3b: Minimal Winding', shortTitle: 'A3b: Min Winding', type: 'axiom', status: 'axiom', confidence: 1.0, description: 'Minimal winding principle for coherent modes.' }
    ];

    axioms.forEach(a => {
      nodes.push(a);
      nodeMap.set(a.id, a);
    });

    // Result nodes — filter by category
    const filteredResults = category === 'all'
      ? results
      : results.filter(r => r.category === category);

    filteredResults.forEach(result => {
      const node = {
        id: result.id,
        title: result.title,
        shortTitle: result.shortTitle || result.title,
        type: 'result',
        status: result.status,
        confidence: result.confidence || 0,
        description: result.summary,
        formula: result.formula,
        sources: result.sources,
        derivation: result.derivation || [],
        category: result.category,
        authorityClaimIds: result.authorityClaimIds || [],
        isStandardMath: result.isStandardMath || false,
        badge: result.badge || result.status
      };
      nodes.push(node);
      nodeMap.set(result.id, node);
    });

    // Links — only for visible nodes
    filteredResults.forEach(result => {
      if (result.derivation) {
        result.derivation.forEach(dep => {
          if (nodeMap.has(dep)) {
            links.push({
              source: dep,
              target: result.id,
              type: result.status
            });
          }
        });
      }
    });

    return { nodes, links };
  }

  function init3DGraph(category) {
    const container = document.getElementById('graph3D');
    if (!container) return;

    if (typeof ForceGraph3D !== 'function') {
      showUnavailableMessage(container);
      is3DActive = false;
      return;
    }

    // Destroy existing instance
    if (graph3DInstance) {
      container.innerHTML = '';
      graph3DInstance = null;
    }

    const graphData = buildGraphData(category);

    graph3DInstance = ForceGraph3D()(container)
      .graphData(graphData)
      .backgroundColor(COLORS.background)
      .nodeLabel(d => d.shortTitle || d.title)
      .nodeColor(getNodeColor)
      .nodeVal(getNodeRadius)
      .nodeResolution(16)
      .nodeOpacity(0.85)
      .linkColor(d => COLORS[d.type] || '#666')
      .linkOpacity(0.3)
      .linkWidth(1.5)
      .linkDirectionalParticles(2)
      .linkDirectionalParticleWidth(2)
      .linkDirectionalParticleSpeed(0.008)
      .linkDirectionalParticleColor(d => COLORS[d.type] || '#666')
      .onNodeClick(node => {
        // Fly to node
        const distance = 60;
        const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);
        graph3DInstance.cameraPosition(
          { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
          node,
          1500
        );
        // Show detail panel
        showNodeDetail(node);
      })
      .onNodeHover((node, prevNode) => {
        container.style.cursor = node ? 'pointer' : 'default';
        if (node) {
          // Highlight connected
          highlightConnected(node);
        } else {
          resetHighlight();
        }
      })
      .dagMode('td')
      .dagLevelDistance(80)
      .d3VelocityDecay(0.15)
      .cooldownTicks(120)
      .warmupTicks(60)
      .showNavInfo(true);

    // Add bloom post-processing
    try {
      const bloomPass = new THREE.UnrealBloomPass(
        new THREE.Vector2(container.clientWidth, container.clientHeight),
        0.6,   // strength
        0.4,   // radius
        0.85   // threshold
      );
      graph3DInstance.postProcessingComposer().addPass(bloomPass);
    } catch(e) {
      console.log('Bloom post-processing not available:', e);
    }

    is3DActive = true;
  }

  function highlightConnected(node) {
    if (!graph3DInstance) return;
    const connectedIds = new Set([node.id]);
    const graphData = graph3DInstance.graphData();
    
    graphData.links.forEach(l => {
      const srcId = typeof l.source === 'object' ? l.source.id : l.source;
      const tgtId = typeof l.target === 'object' ? l.target.id : l.target;
      if (srcId === node.id) connectedIds.add(tgtId);
      if (tgtId === node.id) connectedIds.add(srcId);
    });

    graph3DInstance
      .nodeVisibility(d => connectedIds.has(d.id))
      .linkVisibility(d => {
        const srcId = typeof d.source === 'object' ? d.source.id : d.source;
        const tgtId = typeof d.target === 'object' ? d.target.id : d.target;
        return connectedIds.has(srcId) && connectedIds.has(tgtId);
      });
  }

  function resetHighlight() {
    if (!graph3DInstance) return;
    graph3DInstance.nodeVisibility(true).linkVisibility(true);
  }

  function showNodeDetail(nodeData) {
    const panel = document.getElementById('detailPanel');
    const title = document.getElementById('detailTitle');
    const content = document.getElementById('detailContent');
    
    if (!panel || !title || !content) return;
    
    title.textContent = nodeData.title;
    
    let html = '';
    
    html += '<div class="detail-section">';
    html += '<h4>Type</h4>';
    html += '<p>' + (nodeData.type === 'axiom' ? 'Fundamental Axiom' : 'Derived Result') + '</p>';
    html += '</div>';
    
    if (nodeData.description) {
      html += '<div class="detail-section">';
      html += '<h4>Description</h4>';
      html += '<p>' + escapeHtml(nodeData.description) + '</p>';
      html += '</div>';
    }
    
    if (nodeData.formula) {
      html += '<div class="detail-section">';
      html += '<h4>Key Formula</h4>';
      html += '<div class="detail-formula">' + escapeHtml(nodeData.formula) + '</div>';
      html += '</div>';
    }
    
    if (nodeData.type !== 'axiom') {
      // V5.5: Resolve displayed status/confidence from the authoritative claim.
      var claimId = (nodeData.authorityClaimIds && nodeData.authorityClaimIds.length > 0)
        ? nodeData.authorityClaimIds[0]
        : nodeData.id;
      var claim = (window.PFTruth && window.PFTruth.getClaim) ? window.PFTruth.getClaim(claimId) : null;
      var displayStatus = nodeData.status;
      var displayConfidence = nodeData.confidence;
      var bindingAttr = '';
      if (claim) {
        displayStatus = (claim.isStandardMath && claim.badge)
          ? claim.badge.replace(/\s+\d+(\.\d+)?\s*%?.*$/, '')
          : claim.status;
        displayConfidence = claim.confidence;
        bindingAttr = ' data-claim-id="' + claimId + '"';
      } else {
        bindingAttr = ' data-status-reason="unmapped-result"';
      }
      var confText = (displayConfidence !== null && displayConfidence !== undefined)
        ? ' (' + displayConfidence.toFixed(2) + ')'
        : '';
      html += '<div class="detail-section">';
      html += '<h4>Status</h4>';
      html += '<span class="detail-confidence"' + bindingAttr + '>' + displayStatus + confText + '</span>';
      html += '</div>';
    }
    
    if (nodeData.derivation && nodeData.derivation.length > 0) {
      html += '<div class="detail-section">';
      html += '<h4>Derivation Path</h4>';
      html += '<ul class="derivation-steps">';
      nodeData.derivation.forEach(function(step) {
        const stepNode = window.PFTruth ? window.PFTruth.getResult(step) : null;
        if (stepNode) {
          html += '<li>' + escapeHtml(stepNode.title) + '</li>';
        } else {
          html += '<li>' + escapeHtml(step) + '</li>';
        }
      });
      html += '</ul></div>';
    }
    
    if (nodeData.sources) {
      html += '<div class="detail-section">';
      html += '<h4>Sources</h4>';
      if (Array.isArray(nodeData.sources)) {
        nodeData.sources.forEach(function(source) {
          if (typeof source === 'string') {
            html += '<p><a href="../../' + source + '" target="_blank">' + escapeHtml(source) + '</a></p>';
          } else if (source && source.href) {
            html += '<p><a href="' + source.href + '" target="_blank">' + escapeHtml(source.label || source.href) + '</a></p>';
          }
        });
      }
      html += '</div>';
    }
    
    content.innerHTML = html;
    panel.classList.add('active');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // Public API
  window.DerivationGraph3D = {
    init: function(category) {
      init3DGraph(category || 'all');
    },
    destroy: function() {
      if (graph3DInstance) {
        const container = document.getElementById('graph3D');
        if (container) container.innerHTML = '';
        graph3DInstance = null;
        is3DActive = false;
      }
    },
    isActive: function() {
      return is3DActive;
    },
    setCategory: function(category) {
      currentCategory = category;
      if (is3DActive) {
        init3DGraph(category);
      }
    }
  };

  // Auto-init mode toggle
  document.addEventListener('DOMContentLoaded', function() {
    var mode2D = document.getElementById('mode2D');
    var mode3D = document.getElementById('mode3D');
    var svgContainer = document.getElementById('derivationGraph');
    var container3D = document.getElementById('graph3D');
    var categoryFilter = document.getElementById('categoryFilter');

    if (mode2D && mode3D) {
      if (typeof ForceGraph3D !== 'function') {
        mode3D.disabled = true;
        mode3D.title = '3D graph unavailable in this offline build';
        mode3D.setAttribute('aria-disabled', 'true');
      }

      mode2D.addEventListener('click', function() {
        mode2D.classList.add('is-active');
        mode2D.setAttribute('aria-selected', 'true');
        mode3D.classList.remove('is-active');
        mode3D.setAttribute('aria-selected', 'false');
        if (svgContainer) svgContainer.style.display = 'block';
        if (container3D) container3D.style.display = 'none';
        DerivationGraph3D.destroy();
      });

      mode3D.addEventListener('click', function() {
        if (mode3D.disabled) {
          return;
        }
        mode3D.classList.add('is-active');
        mode3D.setAttribute('aria-selected', 'true');
        mode2D.classList.remove('is-active');
        mode2D.setAttribute('aria-selected', 'false');
        if (svgContainer) svgContainer.style.display = 'none';
        if (container3D) container3D.style.display = 'block';
        DerivationGraph3D.init(currentCategory);
      });
    }

    if (categoryFilter) {
      categoryFilter.addEventListener('change', function() {
        currentCategory = categoryFilter.value;
        if (is3DActive) {
          DerivationGraph3D.setCategory(currentCategory);
        }
      });
    }
  });
})();
