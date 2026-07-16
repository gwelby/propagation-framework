(function() {
  'use strict';
  
  // Derivation Graph Engine — World-Class Implementation
  class DerivationGraph {
    constructor(container, data) {
      this.container = container;
      this.data = data;
      this.nodes = [];
      this.edges = [];
      this.simulation = null;
      this.svg = null;
      this.width = 800;
      this.height = 600;
      this.cssColors = {}; // Cache for CSS variable colors
      
      this.init();
    }

    measure() {
      const rect = this.container.getBoundingClientRect();
      this.width = Math.max(720, Math.floor(rect.width || 800));
      this.height = Math.max(520, Math.floor(rect.height || 600));
    }
    
    // Get color from CSS variables
    getCSSColor(varName) {
      if (!this.cssColors[varName]) {
        const style = getComputedStyle(document.documentElement);
        this.cssColors[varName] = style.getPropertyValue(varName).trim() || '#999';
      }
      return this.cssColors[varName];
    }
    
    init() {
      // Check D3 dependency
      if (typeof d3 === 'undefined') {
        console.error('DerivationGraph: D3.js is required but not loaded');
        this.container.innerHTML = '<div class="graph-error"><p>⚠️ Derivation graph requires D3.js library.</p><p>Please ensure D3 is loaded before initializing the graph.</p></div>';
        return;
      }
      
      // Clear container
      this.container.innerHTML = '';

      this.measure();
      
      // Create SVG
      this.svg = d3.select(this.container)
        .append('svg')
        .attr('width', this.width)
        .attr('height', this.height)
        .attr('viewBox', `0 0 ${this.width} ${this.height}`)
        .attr('preserveAspectRatio', 'xMidYMid meet');
      
      // Create zoom behavior
      const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', (event) => {
          this.g.attr('transform', event.transform);
        });
      
      this.svg.call(zoom);
      
      // Create main group
      this.g = this.svg.append('g');
      
      // Process data
      this.processData();
      
      // Create force simulation
      this.createSimulation();
      
      // Render
      this.render();
    }
    
    processData() {
      // Source from the audited PFClaimsData if available, else fallback to constructor data
      var pfc = window.PFClaimsData || {};
      var allClaims = pfc.CLAIMS || (this.data && this.data.results) || [];
      var allNogos  = pfc.NOGOS  || [];

      // Create nodes from claims
      this.nodes = allClaims.map(result => ({
        id: result.id,
        title: result.title,
        status: result.status && result.status.label ? result.status.label : (result.status || 'UNKNOWN'),
        confidence: result.confidence,
        type: this.getNodeType(result),
        radius: this.getNodeRadius(result),
        isNogo: false,
      }));

      // Add axiom nodes
      const axioms = [
        { id: 'axiom1', title: 'Axiom 1: Propagation', type: 'axiom' },
        { id: 'axiom2', title: 'Axiom 2: Finite Velocity', type: 'axiom' },
        { id: 'axiom3', title: 'Axiom 3: Coherence', type: 'axiom' }
      ];

      axioms.forEach(axiom => {
        if (!this.nodes.find(n => n.id === axiom.id)) {
          this.nodes.push({
            id: axiom.id,
            title: axiom.title,
            type: 'axiom',
            radius: 30,
            status: 'AXIOM',
            isNogo: false,
          });
        }
      });

      // Add NO-GO route nodes as shattered evidence nodes
      allNogos.forEach(nogo => {
        this.nodes.push({
          id: nogo.id,
          title: nogo.title,
          _nodeType: 'NO-GO',  // structural type, not a claim status
          type: 'nogo',
          radius: 18,
          isNogo: true,
          nogoTarget: nogo.target,
          lesson: nogo.lesson,
        });
      });

      // Create edges
      this.edges = [];
      allClaims.forEach(result => {
        const axiomSources = ['axiom1', 'axiom3'];
        const text = `${result.id} ${result.title} ${result.story || ''}`.toLowerCase();
        if (/causal|gravity|variable c|light|bohr|coulomb|propagation/.test(text)) {
          axiomSources.push('axiom2');
        }
        axiomSources.forEach(source => {
          this.edges.push({
            source,
            target: result.id,
            type: this.getEdgeType(result.status && result.status.label ? result.status.label : result.status)
          });
        });
      });

      // Add NO-GO edges: from target claim toward the no-go node (failed route)
      allNogos.forEach(nogo => {
        if (nogo.target) {
          this.edges.push({
            source: nogo.target,
            target: nogo.id,
            type: 'nogo',
          });
        }
      });
    }
    
    getNodeType(result) {
      if (result.type === 'nogo') return 'nogo';
      var statusLabel = result.status && result.status.label ? result.status.label : result.status;
      if (statusLabel === 'AXIOM') return 'axiom';
      if (result.formula && result.derivation) return 'theorem';
      return 'result';
    }
    
    getNodeRadius(result) {
      if (result.type === 'nogo') return 16;
      const baseRadius = 20;
      if (result.confidence > 0.9) return baseRadius + 10;
      if (result.confidence > 0.7) return baseRadius + 5;
      return baseRadius;
    }
    
    getEdgeType(status) {
      var lbl = status && status.label ? status.label : status;
      if (lbl === 'DERIVED') return 'derives';
      if (lbl === 'CONDITIONAL') return 'conditional';
      if (lbl === 'NO-GO') return 'nogo';
      return 'depends';
    }
    
    createSimulation() {
      this.simulation = d3.forceSimulation(this.nodes)
        .force('link', d3.forceLink(this.edges).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(this.width / 2, this.height / 2))
        .force('collision', d3.forceCollide().radius(d => d.radius + 5));
    }
    
    render() {
      // Create links
      const link = this.g.append('g')
        .selectAll('line')
        .data(this.edges)
        .enter().append('line')
        .attr('class', d => `link link-${d.type}`)
        .attr('stroke', d => this.getEdgeColor(d.type))
        .attr('stroke-width', d => d.type === 'nogo' ? 1.5 : 2)
        .attr('stroke-dasharray', d => {
          if (d.type === 'nogo') return '4,4';
          if (d.type === 'conditional') return '5,5';
          return 'none';
        })
        .attr('opacity', d => d.type === 'nogo' ? 0.5 : 1);
      
      // Create node groups
      const node = this.g.append('g')
        .selectAll('g')
        .data(this.nodes)
        .enter().append('g')
        .attr('class', 'node')
        .call(this.drag());
      
      // Add node shapes
      node.append('path')
        .attr('d', d => this.getNodeShape(d))
        .attr('fill', d => this.getNodeColor(d))
        .attr('stroke', d => d.isNogo ? '#ff4455' : '#fff')
        .attr('stroke-width', d => d.isNogo ? 2.5 : 2)
        .attr('stroke-dasharray', d => d.isNogo ? '4,2' : 'none')
        .attr('opacity', d => d.isNogo ? 0.7 : 1)
        .style('cursor', 'pointer')
        .on('click', (event, d) => this.showDetails(d));

      // NO-GO cross mark (×) for failed route nodes
      node.filter(d => d.isNogo)
        .append('text')
        .text('×')
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('font-size', '16px')
        .attr('font-weight', '900')
        .attr('fill', '#ff4455')
        .style('pointer-events', 'none');
      
      // Add labels (skip for NO-GO nodes — the X mark is sufficient)
      node.filter(d => !d.isNogo)
        .append('text')
        .text(d => d.title.length > 20 ? d.title.substring(0, 20) + '...' : d.title)
        .attr('text-anchor', 'middle')
        .attr('dy', '.35em')
        .attr('font-size', '12px')
        .attr('fill', '#fff')
        .style('pointer-events', 'none');

      // NO-GO label below node
      node.filter(d => d.isNogo)
        .append('text')
        .text(d => d.title.length > 16 ? d.title.substring(0, 16) + '…' : d.title)
        .attr('text-anchor', 'middle')
        .attr('dy', d => d.radius + 14)
        .attr('font-size', '9px')
        .attr('fill', '#ff4455')
        .attr('opacity', 0.8)
        .style('pointer-events', 'none');
      
      // Update positions on tick
      this.simulation.on('tick', () => {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);
        
        node.attr('transform', d => `translate(${d.x},${d.y})`);
      });
    }
    
    getNodeShape(d) {
      // D3 v7 API: symbol().type().size()()
      const size = d.radius * d.radius * 4; // Area, not radius

      if (d.type === 'nogo') {
        // Shattered / X shape for NO-GO routes — use a custom path
        const s = d.radius * 0.85;
        return `M${-s},${-s} L${s},${s} M${s},${-s} L${-s},${s}`;
      }
      if (d.type === 'axiom') {
        return d3.symbol().type(d3.symbolTriangle).size(size)();
      } else if (d.type === 'theorem') {
        return d3.symbol().type(d3.symbolDiamond).size(size)();
      } else {
        return d3.symbol().type(d3.symbolCircle).size(size)();
      }
    }
    
    getNodeColor(d) {
      if (d.type === 'nogo') return 'rgba(255,68,85,0.12)'; // Shattered red — mostly transparent, border carries the weight
      // Use CSS variables for consistent design system
      if (d.type === 'axiom') return this.getCSSColor('--planck');
      switch(d.status) {
        case 'DERIVED': return this.getCSSColor('--cohere');
        case 'CONDITIONAL': return this.getCSSColor('--planck');
        case 'PARTIAL DERIVATION': return this.getCSSColor('--refract');
        case 'ARGUED': return this.getCSSColor('--refract');
        case 'EMPIRICAL': return this.getCSSColor('--propagate');
        default: return this.getCSSColor('--muted');
      }
    }
    
    getEdgeColor(type) {
      switch(type) {
        case 'derives': return this.getCSSColor('--cohere');
        case 'conditional': return this.getCSSColor('--planck');
        case 'nogo': return '#ff4455';
        default: return this.getCSSColor('--line-strong');
      }
    }
    
    drag() {
      return d3.drag()
        .on('start', (event, d) => {
          if (!event.active) this.simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', (event, d) => {
          if (!event.active) this.simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        });
    }
    
    showDetails(node) {
      // Try claim first, then no-go, then fallback to graph modal
      var pfc = window.PFClaimsData || {};
      var result = (pfc.CLAIMS || []).find(r => r.id === node.id) ||
                   (pfc.NOGOS  || []).find(r => r.id === node.id) ||
                   (this.data && this.data.results && this.data.results.find(r => r.id === node.id));

      if (window.PFExplorer && typeof window.PFExplorer.focusResult === 'function' && result) {
        window.PFExplorer.focusResult(result.id, { open: true });
        return;
      }
      
      // Create or update detail modal
      let modal = document.getElementById('graph-detail-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'graph-detail-modal';
        modal.className = 'graph-modal';
        document.body.appendChild(modal);
      }
      
      modal.innerHTML = `
        <div class="graph-modal-content">
          <button class="graph-modal-close">&times;</button>
          <h3>${result.title}</h3>
          <p class="status-badge status-${result.status.toLowerCase()}">${result.status}</p>
          ${result.confidence ? `<p>Confidence: ${(result.confidence * 100).toFixed(1)}%</p>` : ''}
          ${result.formula ? `<p class="formula">${result.formula}</p>` : ''}
          ${result.summary ? `<p>${result.summary}</p>` : ''}
          ${result.falsifier ? `<div class="falsifier"><strong>Falsifier:</strong> ${result.falsifier}</div>` : ''}
        </div>
      `;
      
      modal.className = 'graph-modal is-visible';
      
      // Close modal handlers
      modal.querySelector('.graph-modal-close').onclick = () => {
        modal.classList.remove('is-visible');
      };
      modal.onclick = (e) => {
        if (e.target === modal) {
          modal.classList.remove('is-visible');
        }
      };
      
      // Close on Escape key
      const escHandler = (e) => {
        if (e.key === 'Escape') {
          modal.classList.remove('is-visible');
          document.removeEventListener('keydown', escHandler);
        }
      };
      document.addEventListener('keydown', escHandler);
    }
    
    destroy() {
      if (this.simulation) {
        this.simulation.stop();
      }
      this.container.innerHTML = '';
    }

    resize() {
      if (!this.svg || !this.simulation) return;
      this.measure();
      this.svg
        .attr('width', this.width)
        .attr('height', this.height)
        .attr('viewBox', `0 0 ${this.width} ${this.height}`);
      this.simulation
        .force('center', d3.forceCenter(this.width / 2, this.height / 2))
        .alpha(0.25)
        .restart();
    }
  }
  
  // Expose to global
  window.DerivationGraph = DerivationGraph;
})();
