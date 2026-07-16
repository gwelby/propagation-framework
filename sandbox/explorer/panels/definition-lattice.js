/**
 * panels/definition-lattice.js — Definition Lattice Workspace
 * 19 canonical definitions. Dependency graph. Term inspector.
 *
 * Codex acceptance gates:
 * - axioms.md appears in the lattice
 * - consciousness.md does NOT appear as canonical (it is INTUITION in CLAIMS, not DEFINITIONS)
 * - All 19 definitions are CANONICAL v1.0
 */
(function () {
  'use strict';

  var WORKSPACE_ID = 'definition-lattice';

  // Bootstrap order for display — nodes that others depend on come first
  var BOOTSTRAP_ORDER = [
    'medium', 'axioms', 'propagation', 'causal-velocity', 'coherence',
    'mode', 'time', 'energy', 'field', 'gradient',
    'forces', 'matter', 'state', 'information', 'measurement',
    'decoherence', 'minimum-substrate', 'observer', 'coupling'
  ];

  function getDependencyEdges(defs) {
    var edges = [];
    var defMap = {};
    defs.forEach(function(d){ defMap[d.id] = d; });
    defs.forEach(function(d) {
      (d.dependencies || []).forEach(function(dep) {
        if (defMap[dep]) edges.push({ from: dep, to: d.id });
      });
    });
    return edges;
  }

  function buildLatticeHTML(defs) {
    // Sort by bootstrap order
    var ordered = BOOTSTRAP_ORDER.map(function(id) {
      return defs.find(function(d){ return d.id === id; });
    }).filter(Boolean);

    // Any defs not in the order list
    defs.forEach(function(d) {
      if (!BOOTSTRAP_ORDER.includes(d.id)) ordered.push(d);
    });

    var listHTML = ordered.map(function(def, idx) {
      var deps = (def.dependencies || []);
      var depHTML = deps.length
        ? '<div class="dl-def-deps">Requires Coherence: ' + deps.map(function(d){
            return '<button class="dl-dep-link" data-focus-def="'+d+'" type="button">'+d+'</button>';
          }).join(', ') + '</div>'
        : '<div class="dl-def-deps dl-def-deps--root">Axiomatic Root — Propagation starts here</div>';

      return [
        '<article class="dl-def-card" data-def-id="' + def.id + '" tabindex="0">',
          '<div class="dl-vibe-icon" aria-hidden="true">≋</div>',
          '<div class="dl-def-head">',
            '<div class="dl-def-num">' + String(idx + 1).padStart(2, '0') + '</div>',
            '<div class="dl-def-meta">',
              '<h4 class="dl-def-title">' + def.title + '</h4>',
              '<span class="dl-def-status">' + (def.auditLine || 'CANONICAL v1.0') + '</span>',
            '</div>',
          '</div>',
          '<p class="dl-def-oneliner">' + def.oneLiner + '</p>',
          depHTML,
          '<div class="dl-def-views">',
            '<div class="dl-def-story story-only">' + 
              '<span class="dl-narrative-cue">Insight:</span> ' + def.storyLine + 
            '</div>',
            '<div class="dl-def-audit audit-only">',
              '<div class="dl-audit-row"><span class="dl-lbl">Audit Boundary:</span><span>' + def.auditLine + '</span></div>',
              '<div class="dl-audit-row dl-not-this"><span class="dl-lbl">Conceptual Trap:</span><span>' + def.notThis + '</span></div>',
            '</div>',
            '<div class="dl-def-math math-only">',
              '<span class="dl-file-ref">📄 Evidence: ' + (def.file || '') + '</span>',
            '</div>',
          '</div>',
        '</article>',
      ].join('');
    }).join('');

    // Dependency graph — SVG
    var svgHTML = buildDependencyGraph(ordered);

    return [
      '<div class="dl-shell">',
        '<div class="dl-sidebar">',
          '<div class="dl-sidebar-head">',
            '<h3 class="dl-sidebar-title"><span style="color:#00cfff; font-family:serif; margin-right:8px;">≋</span> The Vocabulary of Reality</h3>',
            '<p class="dl-sidebar-sub">Before we can see what reality *is*, we must define the medium it propagates through. These ' + ordered.length + ' primitives are the only permitted words in the framework. No magic. No exceptions.</p>',
          '</div>',
          '<div class="dl-def-list" id="dlDefList">',
            listHTML,
          '</div>',
        '</div>',
        '<div class="dl-graph-pane">',
          '<div class="dl-graph-head">',
            '<h3 class="dl-graph-title">Lattice of Coherence</h3>',
            '<p class="dl-graph-sub">Each node is a concept. Each line is a prerequisite. Watch how reality builds itself from the Medium up.</p>',
            '<p class="interaction-cue"><strong>Interaction:</strong> Click any node to navigate to its details in the sidebar and observe its dependency resonance.</p>',
          '</div>',
          '<div class="dl-graph-canvas-wrap">',
            '<div class="dl-graph-overlay">PHASE TRANSITION IN PROGRESS</div>',
            svgHTML,
          '</div>',
          '<div class="dl-inspector" id="dlInspector">',
            '<div class="dl-inspector-empty">',
              '<div class="dl-vibe-pulse" aria-hidden="true">≋</div>',
              '<span>Select a definition to observe its resonance</span>',
            '</div>',
          '</div>',
        '</div>',
      '</div>',
    ].join('');
  }

  function buildDependencyGraph(defs) {
    // Simple static SVG layout — positions based on dependency depth
    var defMap = {};
    defs.forEach(function(d){ defMap[d.id] = d; });

    // Compute depth (longest path from a root)
    var depth = {};
    var visiting = {};
    function getDepth(id) {
      if (depth[id] != null) return depth[id];
      if (visiting[id]) return 0;
      var def = defMap[id];
      if (!def || !def.dependencies || !def.dependencies.length) {
        depth[id] = 0; return 0;
      }
      visiting[id] = true;
      var maxD = def.dependencies.reduce(function(mx, dep) {
        if (!defMap[dep]) return mx;
        return Math.max(mx, getDepth(dep) + 1);
      }, 0);
      visiting[id] = false;
      depth[id] = maxD;
      return maxD;
    }
    defs.forEach(function(d){ getDepth(d.id); });

    var maxDepth = Math.max.apply(null, defs.map(function(d){ return depth[d.id] || 0; }));

    // Group by depth
    var levels = {};
    defs.forEach(function(d) {
      var lv = depth[d.id] || 0;
      if (!levels[lv]) levels[lv] = [];
      levels[lv].push(d);
    });

    var W = 760; var H = 420;
    var padding = 40;
    var levelCount = maxDepth + 1;

    // Node positions
    var positions = {};
    for (var lv = 0; lv <= maxDepth; lv++) {
      var nodes = levels[lv] || [];
      nodes.forEach(function(d, i) {
        var x = padding + (lv / Math.max(levelCount - 1, 1)) * (W - padding * 2);
        var yStep = (H - padding * 2) / Math.max(nodes.length, 1);
        var y = padding + yStep * i + yStep / 2;
        positions[d.id] = { x: x, y: y };
      });
    }

    // SVG edges
    var edges = getDependencyEdges(defs);
    var edgeSVG = edges.map(function(e) {
      var from = positions[e.from]; var to = positions[e.to];
      if (!from || !to) return '';
      var mx = (from.x + to.x) / 2;
      return '<path d="M'+from.x+','+from.y+' C'+mx+','+from.y+' '+mx+','+to.y+' '+to.x+','+to.y+'"' +
             ' stroke="rgba(0,207,255,0.25)" stroke-width="1" fill="none" marker-end="url(#arr)"/>';
    }).join('');

    // SVG nodes
    var nodeSVG = defs.map(function(d) {
      var pos = positions[d.id];
      if (!pos) return '';
      var isRoot = !d.dependencies || !d.dependencies.length;
      var r = isRoot ? 8 : 6;
      var col = isRoot ? '#9966ff' : '#00cfff';
      var label = d.title.length > 12 ? d.title.substring(0, 11) + '…' : d.title;
      return '<g class="dl-node" data-def-id="' + d.id + '" style="cursor:pointer">'+
               '<circle cx="'+pos.x+'" cy="'+pos.y+'" r="'+r+'" fill="'+col+'" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>'+
               '<text x="'+pos.x+'" y="'+(pos.y - r - 4)+'" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.7)" font-family="inherit">'+label+'</text>'+
             '</g>';
    }).join('');

    return [
      '<svg class="dl-graph-svg" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">',
        '<defs>',
          '<marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">',
            '<path d="M0,0 L0,6 L6,3 z" fill="rgba(0,207,255,0.4)"/>',
          '</marker>',
        '</defs>',
        edgeSVG,
        nodeSVG,
      '</svg>',
    ].join('');
  }

  function renderInspector(def) {
    var inspector = document.getElementById('dlInspector');
    if (!inspector) return;
    var deps = (def.dependencies || []);
    var depLinks = deps.length
      ? deps.map(function(d) {
          return '<button class="dl-dep-link" data-focus-def="'+d+'" type="button">'+d+'</button>';
        }).join(', ')
      : '<em>None — root primitive</em>';

    inspector.innerHTML = [
      '<div class="dl-ins-head">',
        '<div>',
          '<span class="dl-ins-eyebrow">Canonical Definition</span>',
          '<h4 class="dl-ins-title">' + def.title + '</h4>',
          '<p class="dl-ins-file">' + (def.file || '') + '</p>',
        '</div>',
        '<span class="dl-ins-badge">CANONICAL v1.0</span>',
      '</div>',
      '<p class="dl-ins-oneliner">' + def.oneLiner + '</p>',
      '<div class="dl-ins-section story-only">',
        '<span class="dl-ins-lbl">Story</span>',
        '<p>' + def.storyLine + '</p>',
      '</div>',
      '<div class="dl-ins-section audit-only">',
        '<span class="dl-ins-lbl">Audit</span>',
        '<p>' + def.auditLine + '</p>',
        '<div class="dl-ins-not-this">',
          '<span class="dl-ins-lbl">Not this:</span>',
          '<p>' + def.notThis + '</p>',
        '</div>',
      '</div>',
      '<div class="dl-ins-section">',
        '<span class="dl-ins-lbl">Depends on</span>',
        '<div class="dl-ins-deps">' + depLinks + '</div>',
      '</div>',
    ].join('');

    // Wire dep links inside inspector
    Array.prototype.forEach.call(inspector.querySelectorAll('[data-focus-def]'), function(btn) {
      btn.addEventListener('click', function() {
        var id = btn.getAttribute('data-focus-def');
        var defs = (window.PFClaimsData || {}).DEFINITIONS || [];
        var target = defs.find(function(d){ return d.id === id; });
        if (target) {
          renderInspector(target);
          // Scroll the card into view
          var card = document.querySelector('[data-def-id="'+id+'"]');
          if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    });
  }

  PFExplorer.registerPanel({
    id: WORKSPACE_ID,
    title: 'Definition Lattice',

    mount: function (ctx) {
      var data = window.PFClaimsData || {};
      var defs = data.DEFINITIONS || [];

      if (!defs.length) {
        ctx.stage.innerHTML = '<div class="dl-empty"><p>Definition data not loaded. Ensure data.claims.js is included before definition-lattice.js.</p></div>';
        return;
      }

      ctx.stage.innerHTML = buildLatticeHTML(defs);

      var self = this;

      // Card click → inspector + active state
      Array.prototype.forEach.call(ctx.stage.querySelectorAll('.dl-def-card'), function(card) {
        card.addEventListener('click', function(e) {
          if (e.target.closest('[data-focus-def]')) return;
          var id = card.getAttribute('data-def-id');
          var def = defs.find(function(d){ return d.id === id; });
          if (!def) return;
          Array.prototype.forEach.call(ctx.stage.querySelectorAll('.dl-def-card'), function(c) {
            c.classList.remove('is-active');
          });
          card.classList.add('is-active');
          renderInspector(def);
          // Also notify drawer
          if (window.PFExplorer) PFExplorer.focusDefinition(id, { open: false });
        });
        card.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); card.click(); }
        });
      });

      // Dependency link clicks inside cards
      Array.prototype.forEach.call(ctx.stage.querySelectorAll('[data-focus-def]'), function(btn) {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          var id = btn.getAttribute('data-focus-def');
          var targetCard = ctx.stage.querySelector('[data-def-id="'+id+'"]');
          if (targetCard) {
            targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            targetCard.click();
          }
        });
      });

      // SVG node clicks
      Array.prototype.forEach.call(ctx.stage.querySelectorAll('.dl-node'), function(node) {
        node.addEventListener('click', function() {
          var id = node.getAttribute('data-def-id');
          var targetCard = ctx.stage.querySelector('[data-def-id="'+id+'"]');
          if (targetCard) {
            targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            targetCard.click();
          }
        });
      });
    },

    unmount: function () {},
    resize: function () {},
  });

}());
