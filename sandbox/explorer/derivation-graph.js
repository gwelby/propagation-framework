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
      
      // Create SVG
      this.svg = d3.select(this.container)
        .append('svg')
        .attr('width', this.width)
        .attr('height', this.height);
      
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
      // Create nodes from results
      this.nodes = this.data.results.map(result => ({
        id: result.id,
        title: result.title,
        status: result.status,
        confidence: result.confidence,
        type: this.getNodeType(result),
        radius: this.getNodeRadius(result)
      }));
      
      // Create edges from sources
      this.edges = [];
      this.data.results.forEach(result => {
        if (result.sources) {
          result.sources.forEach(source => {
            const sourceId = typeof source === 'string' ? source : source.href || source;
            const sourceResult = this.data.results.find(r => 
              r.id === sourceId || 
              r.sources?.some(s => 
                typeof s === 'string' ? s === sourceId : s.href === sourceId
              )
            );
            
            if (sourceResult) {
              this.edges.push({
                source: sourceResult.id,
                target: result.id,
                type: this.getEdgeType(result.status)
              });
            }
          });
        }
      });
      
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
            status: 'AXIOM'
          });
        }
      });
    }
    
    getNodeType(result) {
      if (result.status === 'AXIOM') return 'axiom';
      if (result.formula && result.derivation) return 'theorem';
      return 'result';
    }
    
    getNodeRadius(result) {
      const baseRadius = 20;
      if (result.confidence > 0.9) return baseRadius + 10;
      if (result.confidence > 0.7) return baseRadius + 5;
      return baseRadius;
    }
    
    getEdgeType(status) {
      if (status === 'DERIVED') return 'derives';
      if (status === 'CONDITIONAL') return 'conditional';
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
        .attr('stroke-width', 2)
        .attr('stroke-dasharray', d => d.type === 'conditional' ? '5,5' : 'none');
      
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
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .style('cursor', 'pointer')
        .on('click', (event, d) => this.showDetails(d));
      
      // Add labels
      node.append('text')
        .text(d => d.title.length > 20 ? d.title.substring(0, 20) + '...' : d.title)
        .attr('text-anchor', 'middle')
        .attr('dy', '.35em')
        .attr('font-size', '12px')
        .attr('fill', '#fff')
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
      
      if (d.type === 'axiom') {
        return d3.symbol().type(d3.symbolTriangle).size(size)();
      } else if (d.type === 'theorem') {
        return d3.symbol().type(d3.symbolDiamond).size(size)();
      } else {
        return d3.symbol().type(d3.symbolCircle).size(size)();
      }
    }
    
    getNodeColor(d) {
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
      const result = this.data.results.find(r => r.id === node.id);
      if (!result) return;
      
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
  }
  
  // Expose to global
  window.DerivationGraph = DerivationGraph;
})();
