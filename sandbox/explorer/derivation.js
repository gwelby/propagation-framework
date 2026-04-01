// Derivation Chain Visualizer
// Interactive graph showing how results derive from axioms

(function() {
  // Derivation data structure
  const derivationData = {
    nodes: [
      // Axioms (root nodes)
      {
        id: 'axiom1',
        label: 'Axiom 1',
        title: 'Propagation is Fundamental',
        type: 'axiom',
        x: 200,
        y: 400,
        description: 'Everything that exists propagates through a structured medium.',
        formula: '∃ medium M such that ∀ entities e: e propagates in M'
      },
      {
        id: 'axiom2',
        label: 'Axiom 2',
        title: 'Finite Causal Velocity',
        type: 'axiom',
        x: 200,
        y: 200,
        description: 'Every medium has a maximum signal speed c. No causal influence propagates faster.',
        formula: '∃ c > 0: ∀ signals s: |v_s| ≤ c'
      },
      {
        id: 'axiom3',
        label: 'Axiom 3',
        title: 'Coherence',
        type: 'axiom',
        x: 200,
        y: 600,
        description: 'Stable structure requires self-reinforcing, coherent propagation.',
        formula: 'Stable ⇔ Coherent closed-loop propagation'
      },
      
      // Derived results
      {
        id: 'bohr',
        label: 'Bohr Quantization',
        title: 'Atomic spectra from phase closure',
        type: 'conditional',
        confidence: 0.82,
        x: 500,
        y: 500,
        description: 'Circular eikonal orbits with phase closure yield Bohr-like 1/k² spectrum.',
        formula: 'r_k = 2k², E_k = -1/(4k²)',
        sources: ['bohr_quantization_audit_2026-03-27.md'],
        derivation: ['axiom3', 'circular-eikonal-model', 'phase-closure']
      },
      
      {
        id: 'gravity-refraction',
        label: 'Gravity as Refraction',
        title: 'Optical geometry of spacetime',
        type: 'derived',
        confidence: 0.95,
        x: 500,
        y: 300,
        description: 'Gravity is refractive bending of propagation paths in a medium with density gradient.',
        formula: 'n(r) = 1 + r_s/r → d/ds(n dx/ds) = ∇n',
        sources: ['gr_fermat_equivalence.md'],
        derivation: ['axiom1', 'axiom2', 'optical-metric']
      },
      
      {
        id: 'topological-weights',
        label: 'Topological Weights',
        title: '(2,1) from SO(3) topology',
        type: 'partial',
        confidence: 0.85,
        x: 500,
        y: 700,
        description: 'π₁(SO(3)) = ℤ₂ gives two loop classes with closure orders 1 and 2.',
        formula: 'π₁(SO(3)) → {weight-1, weight-2}',
        sources: ['topological_weights_t1_audit_2026-03-28.md'],
        derivation: ['axiom1', 'so3-topology']
      },
      
      {
        id: 'koide',
        label: 'Koide Q=2/3',
        title: 'Geometric identity from resonance',
        type: 'derived',
        confidence: 0.95,
        x: 800,
        y: 600,
        description: 'Three equal-strength resonances at 120° force Q = 2/3 exactly.',
        formula: 'Q = (m_e + m_μ + m_τ)² / (2(m_e² + m_μ² + m_τ²)) = 2/3',
        sources: ['koide_formula_explanations/MASTER.md'],
        derivation: ['axiom3', 'three-resonances', '120°-geometry']
      },
      
      {
        id: 'three-generations',
        label: 'Three Generations',
        title: 'N=3 from topology + Koide',
        type: 'conditional',
        confidence: 0.85,
        x: 800,
        y: 400,
        description: 'Q(N) = 2N/(2N+3) = 2/3 gives N=3 as unique integer solution.',
        formula: 'Q(N) = 2N/(2N+3), Q=2/3 → N=3',
        sources: ['three_generation_topology/MASTER.md'],
        derivation: ['topological-weights', 'koide', 'q-function']
      },
      
      {
        id: 'weinberg',
        label: 'Weinberg Angle',
        title: 'sin²θ_W from Casimir polynomial',
        type: 'derived',
        confidence: 0.90,
        x: 1100,
        y: 300,
        description: 'Casimir polynomial with Axiom 3b selects k=1, yielding sin²θ_W ≈ 0.22310.',
        formula: 'x² + C₂x - C₂ = 0 → sin²θ_W = 0.22310',
        sources: ['g3_casimir_weinberg_angle.md'],
        derivation: ['axiom3', 'axiom3b', 'casimir-polynomial']
      },
      
      {
        id: 'god-equation',
        label: 'God Equation',
        title: 'λ_c from Planck scale',
        type: 'conditional',
        confidence: 0.88,
        x: 1100,
        y: 500,
        description: 'Predicts top quark Compton wavelength to 0.4% with zero free parameters.',
        formula: 'λ_c = √2·l_P·exp(4π²N^(D/2)/b₀)',
        sources: ['lambda_c_from_axioms.md'],
        derivation: ['axiom1', 'axiom2', 'axiom3', 'z3-structure', 'coherence-volume']
      }
    ],
    
    edges: [
      // Direct dependencies
      { from: 'axiom3', to: 'bohr', type: 'conditional' },
      { from: 'axiom1', to: 'gravity-refraction', type: 'derived' },
      { from: 'axiom2', to: 'gravity-refraction', type: 'derived' },
      { from: 'axiom1', to: 'topological-weights', type: 'partial' },
      { from: 'axiom3', to: 'koide', type: 'derived' },
      { from: 'topological-weights', to: 'three-generations', type: 'conditional' },
      { from: 'koide', to: 'three-generations', type: 'conditional' },
      { from: 'axiom3', to: 'weinberg', type: 'derived' },
      { from: 'axiom1', to: 'god-equation', type: 'conditional' },
      { from: 'axiom2', to: 'god-equation', type: 'conditional' },
      { from: 'axiom3', to: 'god-equation', type: 'conditional' },
      
      // Cross-connections
      { from: 'gravity-refraction', to: 'weinberg', type: 'argued' },
      { from: 'three-generations', to: 'god-equation', type: 'argued' }
    ]
  };

  // State
  let currentZoom = 1;
  let selectedNode = null;
  let svg = null;
  let svgGroup = null;

  // Initialize
  function init() {
    svg = document.getElementById('derivationGraph');
    svgGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    svgGroup.setAttribute('id', 'graphGroup');
    svg.appendChild(svgGroup);
    
    renderGraph();
    updateStatistics();
    setupEventListeners();
  }

  // Render the graph
  function renderGraph() {
    // Clear existing content
    svgGroup.innerHTML = '';
    
    // Apply zoom transform
    svgGroup.setAttribute('transform', `scale(${currentZoom})`);
    
    // Draw edges
    derivationData.edges.forEach(edge => {
      const fromNode = derivationData.nodes.find(n => n.id === edge.from);
      const toNode = derivationData.nodes.find(n => n.id === edge.to);
      
      if (fromNode && toNode) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', fromNode.x);
        line.setAttribute('y1', fromNode.y);
        line.setAttribute('x2', toNode.x);
        line.setAttribute('y2', toNode.y);
        line.setAttribute('class', `edge edge-${edge.type}`);
        line.setAttribute('marker-end', `url(#arrow-${edge.type})`);
        line.setAttribute('data-from', edge.from);
        line.setAttribute('data-to', edge.to);
        
        svgGroup.appendChild(line);
      }
    });
    
    // Draw nodes
    derivationData.nodes.forEach(node => {
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('class', `node node-${node.type}`);
      g.setAttribute('data-id', node.id);
      g.setAttribute('transform', `translate(${node.x}, ${node.y})`);
      
      // Node circle
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('r', node.type === 'axiom' ? '35' : '30');
      g.appendChild(circle);
      
      // Node label
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('class', 'node-text');
      text.setAttribute('dy', '5');
      text.textContent = node.label;
      g.appendChild(text);
      
      // Confidence for non-axioms
      if (node.confidence) {
        const confText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        confText.setAttribute('class', 'confidence-text');
        confText.setAttribute('dy', '45');
        confText.textContent = node.confidence.toFixed(2);
        g.appendChild(confText);
      }
      
      // Click handler
      g.addEventListener('click', () => selectNode(node));
      
      svgGroup.appendChild(g);
    });
  }

  // Select and show node details
  function selectNode(node) {
    selectedNode = node;
    
    const panel = document.getElementById('detailPanel');
    const title = document.getElementById('detailTitle');
    const content = document.getElementById('detailContent');
    
    title.textContent = node.title;
    
    let html = `
      <div class="detail-section">
        <h4>Description</h4>
        <p>${node.description}</p>
      </div>
    `;
    
    if (node.formula) {
      html += `
        <div class="detail-section">
          <h4>Key Formula</h4>
          <div class="detail-formula">${node.formula}</div>
        </div>
      `;
    }
    
    if (node.confidence) {
      const statusClass = `confidence-${node.type}`;
      html += `
        <div class="detail-section">
          <h4>Status</h4>
          <span class="detail-confidence ${statusClass}">
            ${node.type.toUpperCase()} (${node.confidence})
          </span>
        </div>
      `;
    }
    
    if (node.derivation && node.derivation.length > 0) {
      html += `
        <div class="detail-section">
          <h4>Derivation Path</h4>
          <ul class="derivation-steps">
      `;
      
      node.derivation.forEach((step, i) => {
        const stepNode = derivationData.nodes.find(n => n.id === step);
        if (stepNode) {
          html += `<li>${stepNode.title}</li>`;
        }
      });
      
      html += `</ul></div>`;
    }
    
    if (node.sources) {
      html += `
        <div class="detail-section">
          <h4>Sources</h4>
      `;
      node.sources.forEach(source => {
        html += `<p><a href="../../${source}" target="_blank">${source}</a></p>`;
      });
      html += `</div>`;
    }
    
    content.innerHTML = html;
    panel.classList.add('active');
  }

  // Update statistics
  function updateStatistics() {
    const totalNodes = derivationData.nodes.length;
    const derivedCount = derivationData.nodes.filter(n => n.type === 'derived').length;
    const avgConfidence = derivationData.nodes
      .filter(n => n.confidence)
      .reduce((sum, n) => sum + n.confidence, 0) / 
      derivationData.nodes.filter(n => n.confidence).length;
    
    // Find longest derivation chain
    let longestChain = 0;
    derivationData.nodes.forEach(node => {
      if (node.derivation) {
        longestChain = Math.max(longestChain, node.derivation.length);
      }
    });
    
    document.getElementById('totalNodes').textContent = totalNodes;
    document.getElementById('derivedCount').textContent = derivedCount;
    document.getElementById('avgConfidence').textContent = avgConfidence.toFixed(2);
    document.getElementById('longestChain').textContent = longestChain;
  }

  // Setup event listeners
  function setupEventListeners() {
    // Back button
    document.getElementById('backBtn').addEventListener('click', () => {
      window.location.href = 'index.html';
    });
    
    // Close detail panel
    document.getElementById('closeDetail').addEventListener('click', () => {
      document.getElementById('detailPanel').classList.remove('active');
    });
    
    // Zoom controls
    document.getElementById('zoomIn').addEventListener('click', () => {
      currentZoom = Math.min(currentZoom * 1.2, 3);
      renderGraph();
    });
    
    document.getElementById('zoomOut').addEventListener('click', () => {
      currentZoom = Math.max(currentZoom / 1.2, 0.5);
      renderGraph();
    });
    
    document.getElementById('resetView').addEventListener('click', () => {
      currentZoom = 1;
      renderGraph();
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.getElementById('detailPanel').classList.remove('active');
      } else if (e.key === '+' || e.key === '=') {
        currentZoom = Math.min(currentZoom * 1.2, 3);
        renderGraph();
      } else if (e.key === '-' || e.key === '_') {
        currentZoom = Math.max(currentZoom / 1.2, 0.5);
        renderGraph();
      }
    });
  }

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', init);
})();
