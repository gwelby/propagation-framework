/**
 * panels/proof-atlas.js
 * Unified Proof Atlas panel wrapping DerivationGraph engine.
 */
(function () {
  'use strict';

  function toGraphResult(claim) {
    return {
      id: claim.id,
      title: claim.title,
      status: claim.status && claim.status.label ? claim.status.label : 'UNKNOWN',
      confidence: claim.confidence,
      formula: claim.math || '',
      summary: claim.story || (claim.audit && claim.audit.claim) || '',
      falsifier: (claim.audit && claim.audit.falsifier) || '',
      sources: claim.sources || []
    };
  }

  function graphData() {
    return {
      results: ((window.PFClaimsData || {}).CLAIMS || []).map(toGraphResult)
    };
  }

  PFExplorer.registerPanel({
    id: 'proof-atlas',
    title: 'Proof Atlas',

    mount: function (ctx) {
      ctx.stage.innerHTML = [
        '<div class="atlas-shell">',
          '<div class="atlas-header">',
            '<div class="atlas-header-text">',
              '<h2 class="atlas-headline"><span style="color:#ffdd55; font-family:serif; margin-right:8px;">◈</span> Proof Atlas</h2>',
              '<p class="atlas-subhead">A topological map of the framework\'s logical dependency graph. Axioms <em>(∇)</em> form the root, conditional proofs <em>(λ)</em> bridge the gap, and physical results <em>(Σ)</em> sit at the leaves. Distance represents derivation depth.</p>',
              '<p class="interaction-cue"><strong>Interaction:</strong> Drag to pan. Scroll to zoom. Click any node to open the Evidence Drawer for its full derivation and falsification criteria.</p>',
            '</div>',
            '<div class="atlas-controls" id="atlasControls">',
              '<button class="atlas-reset-btn" id="resetAtlas">Reset View</button>',
            '</div>',
          '</div>',
          '<div class="atlas-graph-container" id="atlasGraph"></div>',
          '<div class="atlas-legend">',
            '<div class="legend-item"><span class="legend-shape shape-tri"></span> <strong>Axiom</strong> (Foundation)</div>',
            '<div class="legend-item"><span class="legend-shape shape-dia"></span> <strong>Theorem</strong> (Mathematical Bridge)</div>',
            '<div class="legend-item"><span class="legend-shape shape-circ"></span> <strong>Result</strong> (Physical Match)</div>',
          '</div>',
        '</div>'
      ].join('');

      this.state = {
        container: ctx.stage.querySelector('#atlasGraph'),
        graph: null
      };

      if (window.DerivationGraph) {
        this.state.graph = new window.DerivationGraph(this.state.container, graphData());
      } else {
        this.state.container.innerHTML = '<div class="error-box">DerivationGraph engine not found.</div>';
      }

      const resetBtn = ctx.stage.querySelector('#resetAtlas');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          if (this.state.graph) {
            this.state.graph.destroy();
            this.state.graph = new window.DerivationGraph(this.state.container, graphData());
          }
        });
      }
    },

    unmount: function () {
      if (this.state && this.state.graph) {
        this.state.graph.destroy();
      }
      this.state = null;
    },

    resize: function () {
      if (this.state && this.state.graph) {
        this.state.graph.resize();
      }
    }
  });

}());
