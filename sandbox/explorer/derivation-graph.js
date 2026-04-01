(function() {
  'use strict';
  
  // Derivation Graph Engine
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
      
      this.init();
    }
    
    init() {
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
      if (d.type === 'axiom') {
        return d3.symbolTriangle(d.radius * 2);
      } else if (d.type === 'theorem') {
        return d3.symbolDiamond(d.radius * 2);
      } else {
        return d3.symbolCircle(d.radius);
      }
    }
    
    getNodeColor(d) {
      if (d.type === 'axiom') return '#ffdd55';
      switch(d.status) {
        case 'DERIVED': return '#44ff88';
        case 'CONDITIONAL': return '#ffdd55';
        case 'PARTIAL DERIVATION': return '#ffb24d';
        case 'ARGUED': return '#ff9955';
        case 'EMPIRICAL': return '#00cfff';
        default: return '#999';
      }
    }
    
    getEdgeColor(type) {
      switch(type) {
        case 'derives': return '#44ff88';
        case 'conditional': return '#ffdd55';
        default: return '#666';
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
      
      modal.style.display = 'flex';
      
      // Close modal handlers
      modal.querySelector('.graph-modal-close').onclick = () => {
        modal.style.display = 'none';
      };
      modal.onclick = (e) => {
        if (e.target === modal) {
          modal.style.display = 'none';
        }
      };
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
