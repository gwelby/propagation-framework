// Derivation Chain Visualizer - D3.js Force-Directed Graph
// Maximum quality implementation with advanced features
(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    width: 1400,
    height: 800,
    nodeRadius: 30,
    axiomRadius: 35,
    linkDistance: 150,
    forceStrength: -1000,
    collisionRadius: 50,
    zoomExtent: [0.1, 4],
    colors: {
      DERIVED: '#44ff88',
      CONDITIONAL: '#ffaa00',
      'PARTIAL DERIVATION': '#00cfff',
      ARGUED: '#ff6b6b',
      EMPIRICAL: '#ffdd55',
      axiom: '#9b59b6',
      link: {
        DERIVED: '#44ff88',
        CONDITIONAL: '#ffaa00',
        ARGUED: '#ff6b6b'
      }
    }
  };

  // State
  let simulation;
  let svg, g, link, node, label;
  let currentZoom = 1;
  let selectedNode = null;
  let currentCategory = 'all';
  let performanceMonitor = {
    frameCount: 0,
    lastTime: performance.now(),
    fps: 60
  };

  // Initialize when DOM and data are ready
  function init() {
    // Check if data is loaded
    if (!window.PFExplorerData || !window.PFTruth) {
      setTimeout(init, 100);
      return;
    }

    setupSVG();
    buildGraph();
    setupInteractions();
    setupPerformanceMonitoring();
    updateStatistics();
  }

  // Setup SVG container
  function setupSVG() {
    const container = d3.select('#derivationGraph');
    
    // Clear existing content
    container.selectAll('*').remove();
    
    // Add definitions for markers and gradients
    const defs = container.append('defs');
    
    // Arrow markers
    ['DERIVED', 'CONDITIONAL', 'ARGUED'].forEach(status => {
      defs.append('marker')
        .attr('id', `arrow-${status.toLowerCase()}`)
        .attr('markerWidth', 10)
        .attr('markerHeight', 10)
        .attr('refX', 9)
        .attr('refY', 3)
        .attr('orient', 'auto')
        .attr('markerUnits', 'strokeWidth')
        .append('path')
        .attr('d', 'M0,0 L0,6 L9,3 z')
        .attr('fill', CONFIG.colors.link[status]);
    });

    // Glow filter
    const glow = defs.append('filter')
      .attr('id', 'glow');
    
    glow.append('feGaussianBlur')
      .attr('stdDeviation', 3)
      .attr('result', 'coloredBlur');
    
    glow.append('feMerge')
      .selectAll('feMergeNode')
      .data(['coloredBlur', 'SourceGraphic'])
      .enter().append('feMergeNode')
      .attr('in', d => d);

    // Gradients for nodes
    Object.entries(CONFIG.colors).forEach(([key, color]) => {
      if (key !== 'link') {
        const gradient = defs.append('radialGradient')
          .attr('id', `gradient-${key.toLowerCase()}`);
        
        gradient.append('stop')
          .attr('offset', '0%')
          .attr('stop-color', color)
          .attr('stop-opacity', 0.8);
        
        gradient.append('stop')
          .attr('offset', '100%')
          .attr('stop-color', color)
          .attr('stop-opacity', 0.3);
      }
    });

    // Main group for zoom/pan
    svg = container.append('g');
    
    // Setup zoom behavior
    const zoom = d3.zoom()
      .scaleExtent(CONFIG.zoomExtent)
      .on('zoom', (event) => {
        currentZoom = event.transform.k;
        svg.attr('transform', event.transform);
        updateLabelVisibility();
      });
    
    container.call(zoom);
    
    // Link group
    link = svg.append('g').attr('class', 'links');
    
    // Node group
    node = svg.append('g').attr('class', 'nodes');
    
    // Label group
    label = svg.append('g').attr('class', 'labels');
  }

  // Build graph from data
  function buildGraph() {
    const allResults = window.PFTruth.getAuditedResults();
    const results = currentCategory === 'all'
      ? allResults
      : allResults.filter(r => r.category === currentCategory);
    
    const nodes = [];
    const links = [];
    const nodeMap = new Map();

    // Create axiom nodes (always show all axioms)
    ['axiom1', 'axiom2', 'axiom3', 'axiom3b'].forEach((id, i) => {
      const axiom = {
        id: id,
        label: `A${i + 1}`,
        title: ['Propagation is Fundamental', 'Finite Causal Velocity', 'Coherence', 'Minimal Winding'][i],
        type: 'axiom',
        status: 'axiom',
        confidence: 1.0,
        x: CONFIG.width * 0.2,
        y: CONFIG.height * (0.15 + i * 0.18)
      };
      nodes.push(axiom);
      nodeMap.set(id, axiom);
    });

    // Create result nodes
    results.forEach(result => {
      const node = {
        id: result.id,
        label: result.shortTitle || result.title,
        title: result.title,
        type: 'result',
        status: result.status,
        confidence: result.confidence || 0,
        description: result.summary,
        formula: result.formula,
        sources: result.sources,
        derivation: result.derivation || [],
        authorityClaimIds: result.authorityClaimIds || [],
        isStandardMath: result.isStandardMath || false,
        badge: result.badge || result.status,
        category: result.category
      };
      nodes.push(node);
      nodeMap.set(result.id, node);
    });

    // V5.5: expose lookup map for runtime proof interactions
    window.__derivationNodes = nodeMap;

    // Create links based on derivations
    results.forEach(result => {
      if (result.derivation) {
        result.derivation.forEach(dep => {
          const source = nodeMap.get(dep);
          if (source) {
            links.push({
              source: dep,
              target: result.id,
              type: result.status.toLowerCase(),
              value: 1
            });
          }
        });
      }
    });

    // Create force simulation
    simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links)
        .id(d => d.id)
        .distance(CONFIG.linkDistance)
        .strength(0.5))
      .force('charge', d3.forceManyBody()
        .strength(CONFIG.forceStrength))
      .force('center', d3.forceCenter(CONFIG.width / 2, CONFIG.height / 2))
      .force('collision', d3.forceCollide()
        .radius(d => d.type === 'axiom' ? CONFIG.axiomRadius * 1.5 : CONFIG.collisionRadius))
      .force('x', d3.forceX(CONFIG.width / 2).strength(0.1))
      .force('y', d3.forceY(CONFIG.height / 2).strength(0.1));

    // Render links
    const linkSelection = link.selectAll('line')
      .data(links)
      .enter().append('line')
      .attr('class', d => `link link-${d.type}`)
      .attr('stroke', d => CONFIG.colors.link[d.type] || '#666')
      .attr('stroke-width', 2)
      .attr('stroke-opacity', 0.6)
      .attr('marker-end', d => `url(#arrow-${d.type})`);

    // Render nodes
    const nodeSelection = node.selectAll('g')
      .data(nodes)
      .enter().append('g')
      .attr('class', 'node')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    // Node circles
    nodeSelection.append('circle')
      .attr('r', d => d.type === 'axiom' ? CONFIG.axiomRadius : CONFIG.nodeRadius)
      .attr('fill', d => `url(#gradient-${d.type === 'axiom' ? 'axiom' : d.status.toLowerCase()})`)
      .attr('stroke', d => CONFIG.colors[d.type === 'axiom' ? 'axiom' : d.status] || '#666')
      .attr('stroke-width', 2);

    // Node icons/symbols
    nodeSelection.append('text')
      .attr('class', 'node-symbol')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', d => d.type === 'axiom' ? '20px' : '16px')
      .attr('fill', 'white')
      .attr('pointer-events', 'none')
      .text(d => {
        if (d.type === 'axiom') return 'A';
        switch(d.status) {
          case 'DERIVED': return '✓';
          case 'CONDITIONAL': return '?';
          case 'PARTIAL DERIVATION': return '◐';
          case 'ARGUED': return '◇';
          case 'EMPIRICAL': return '◈';
          default: return '○';
        }
      });

    // Node labels
    const labelSelection = label.selectAll('text')
      .data(nodes)
      .enter().append('text')
      .attr('class', 'node-label')
      .attr('text-anchor', 'middle')
      .attr('dy', d => (d.type === 'axiom' ? CONFIG.axiomRadius : CONFIG.nodeRadius) + 20)
      .attr('font-size', '12px')
      .attr('fill', '#ccc')
      .attr('pointer-events', 'none')
      .text(d => d.label);

    // Node click handler
    nodeSelection.on('click', (event, d) => {
      selectNode(d);
      event.stopPropagation();
    });

    // Update positions on tick
    simulation.on('tick', () => {
      linkSelection
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      nodeSelection
        .attr('transform', d => `translate(${d.x},${d.y})`);

      labelSelection
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });
  }

  // Setup interactions
  function setupInteractions() {
    // Zoom controls
    d3.select('#zoomIn').on('click', () => {
      const svg = d3.select('#derivationGraph');
      const zoom = d3.zoom().scaleExtent(CONFIG.zoomExtent);
      svg.transition().duration(300).call(zoom.scaleBy, 1.3);
    });

    d3.select('#zoomOut').on('click', () => {
      const svg = d3.select('#derivationGraph');
      const zoom = d3.zoom().scaleExtent(CONFIG.zoomExtent);
      svg.transition().duration(300).call(zoom.scaleBy, 0.7);
    });

    d3.select('#resetView').on('click', () => {
      const svg = d3.select('#derivationGraph');
      const zoom = d3.zoom().scaleExtent(CONFIG.zoomExtent);
      svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
    });

    // Back button
    d3.select('#backBtn').on('click', () => {
      window.location.href = 'index.html';
    });

    // Close detail panel
    d3.select('#closeDetail').on('click', () => {
      d3.select('#detailPanel').classed('active', false);
      selectedNode = null;
    });

    // Category filter
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
      categoryFilter.addEventListener('change', (e) => {
        currentCategory = e.target.value;
        rebuildGraph();
      });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      switch(e.key) {
        case 'Escape':
          d3.select('#detailPanel').classed('active', false);
          selectedNode = null;
          break;
        case '+':
        case '=':
          d3.select('#zoomIn').node().click();
          break;
        case '-':
        case '_':
          d3.select('#zoomOut').node().click();
          break;
        case '0':
          d3.select('#resetView').node().click();
          break;
      }
    });
  }

  // Select and show node details
  function selectNode(nodeData) {
    selectedNode = nodeData;
    
    const panel = d3.select('#detailPanel');
    const title = d3.select('#detailTitle');
    const content = d3.select('#detailContent');
    
    title.text(nodeData.title);
    
    let html = `
      <div class="detail-section">
        <h4>Type</h4>
        <p>${nodeData.type === 'axiom' ? 'Fundamental Axiom' : 'Derived Result'}</p>
      </div>
    `;
    
    if (nodeData.description) {
      html += `
        <div class="detail-section">
          <h4>Description</h4>
          <p>${nodeData.description}</p>
        </div>
      `;
    }
    
    if (nodeData.formula) {
      html += `
        <div class="detail-section">
          <h4>Key Formula</h4>
          <div class="detail-formula">${nodeData.formula}</div>
        </div>
      `;
    }
    
    if (nodeData.type !== 'axiom') {
      // V5.5: Resolve displayed status/confidence from the authoritative claim.
      let claimId = (nodeData.authorityClaimIds && nodeData.authorityClaimIds.length > 0)
        ? nodeData.authorityClaimIds[0]
        : nodeData.id;
      let claim = (window.PFTruth && window.PFTruth.getClaim) ? window.PFTruth.getClaim(claimId) : null;
      let displayStatus = nodeData.status;
      let displayConfidence = nodeData.confidence;
      let bindingAttr = '';
      if (claim) {
        displayStatus = (claim.isStandardMath && claim.badge)
          ? claim.badge.replace(/\s+\d+(\.\d+)?\s*%?.*$/, '')
          : claim.status;
        displayConfidence = claim.confidence;
        bindingAttr = ` data-claim-id="${claimId}"`;
      } else {
        bindingAttr = ' data-status-reason="unmapped-result"';
      }
      const statusClass = `confidence-${(displayStatus || 'unavailable').toLowerCase().replace(/\s+/g, '-')}`;
      const confText = (displayConfidence !== null && displayConfidence !== undefined)
        ? ` (${displayConfidence.toFixed(2)})`
        : '';
      html += `
        <div class="detail-section">
          <h4>Status</h4>
          <span class="detail-confidence ${statusClass}"${bindingAttr}>
            ${displayStatus}${confText}
          </span>
        </div>
      `;
    }
    
    if (nodeData.derivation && nodeData.derivation.length > 0) {
      html += `
        <div class="detail-section">
          <h4>Derivation Path</h4>
          <ul class="derivation-steps">
      `;
      
      nodeData.derivation.forEach(step => {
        const stepNode = window.PFTruth.getResult(step);
        if (stepNode) {
          html += `<li>${stepNode.title}</li>`;
        }
      });
      
      html += `</ul></div>`;
    }
    
    if (nodeData.sources) {
      html += `
        <div class="detail-section">
          <h4>Sources</h4>
      `;
      if (Array.isArray(nodeData.sources)) {
        nodeData.sources.forEach(source => {
          if (typeof source === 'string') {
            html += `<p><a href="../../${source}" target="_blank">${source}</a></p>`;
          } else if (source.href) {
            html += `<p><a href="${source.href}" target="_blank">${source.label || source.href}</a></p>`;
          }
        });
      }
      html += `</div>`;
    }
    
    content.html(html);
    panel.classed('active', true);
  }

  // Update statistics
  function updateStatistics() {
    const results = window.PFTruth.getAuditedResults();
    const counts = window.PFTruth.getCountsByStatus();
    
    d3.select('#totalNodes').text(results.length + 3); // +3 for axioms
    d3.select('#derivedCount').text(counts.DERIVED || 0);
    
    const avgConfidence = results.reduce((sum, r) => sum + (r.confidence || 0), 0) / results.length;
    d3.select('#avgConfidence').text(avgConfidence.toFixed(2));
    
    // Find longest derivation chain
    let longestChain = 0;
    results.forEach(result => {
      if (result.derivation) {
        longestChain = Math.max(longestChain, result.derivation.length);
      }
    });
    d3.select('#longestChain').text(longestChain);
  }

  // Update label visibility based on zoom
  function updateLabelVisibility() {
    const shouldShowLabels = currentZoom > 0.5;
    d3.selectAll('.node-label')
      .style('opacity', shouldShowLabels ? 1 : 0);
  }

  // Drag functions
  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  // Performance monitoring
  function setupPerformanceMonitoring() {
    function updateFPS() {
      performanceMonitor.frameCount++;
      const now = performance.now();
      const delta = now - performanceMonitor.lastTime;
      
      if (delta >= 1000) {
        performanceMonitor.fps = Math.round((performanceMonitor.frameCount * 1000) / delta);
        performanceMonitor.frameCount = 0;
        performanceMonitor.lastTime = now;
        
        // Log FPS for debugging
        if (performanceMonitor.fps < 30) {
          console.warn(`Low FPS detected: ${performanceMonitor.fps}`);
        }
      }
      
      requestAnimationFrame(updateFPS);
    }
    
    requestAnimationFrame(updateFPS);
  }

  // Rebuild graph with current category filter
  function rebuildGraph() {
    if (simulation) {
      simulation.stop();
    }
    setupSVG();
    buildGraph();
    updateStatistics();
  }

  // V5.5: Expose minimal API for the runtime proof to exercise interactions
  window.DerivationRoute = {
    isReady: function() {
      return !!window.__derivationNodes && window.__derivationNodes.size > 0;
    },
    selectNodeById: function(id) {
      if (!window.__derivationNodes) return false;
      var node = window.__derivationNodes.get(id);
      if (node) { selectNode(node); return true; }
      return false;
    },
    getResultNodeIds: function() {
      if (!window.__derivationNodes) return [];
      return Array.from(window.__derivationNodes.keys()).filter(function(k) { return !/^axiom/.test(k); });
    }
  };

  // Initialize when ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
