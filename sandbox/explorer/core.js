/**
 * core.js — The Propagation Framework Explorer Orchestrator
 * Central singleton for SPA state, panel lifecycle, and evidence drawer hydration.
 *
 * Requirements:
 * - Register panels via PFExplorer.registerPanel()
 * - Unified navigation via navigate(routeId)
 * - Strict adherence to Codex truth-audit gates
 * - MathJax lazy-loading coordination via CommandBar
 */

(function () {
  'use strict';

  var dom = {};
  var panels = {};
  var currentPanel = null;
  var state = {
    mode: 'story',
    currentRoute: null,
    heat: 0,
    scaleMeters: 1.7, // Default human scale
    selectedItem: null, // { type: 'claim'|'def', data: {...} }
    filters: {}
  };

  var lastTime = 0;
  var isLooping = false;

  // Internal singleton construction
  var PF = {
    version: '2.1.0-Hardened',
    
    init: function () {
      console.log('PFExplorer: Initializing Observatory...');

      // Ensure data is synced if using truth-utils
      if (window.PFTruth && typeof window.PFTruth.syncLegacyData === 'function') {
        window.PFTruth.syncLegacyData();
      }
      
      // Cache core DOM elements
      dom.stage = document.getElementById('panelStage') || document.getElementById('workspaceStage');
      dom.drawer = document.getElementById('appDrawer');
      dom.drawerContent = document.getElementById('drawerBody');
      dom.drawerTitle = document.getElementById('drawerTitle');
      dom.drawerEyebrow = document.getElementById('drawerEyebrow');
      dom.drawerToggle = document.getElementById('drawerToggle');
      dom.panelTitle = document.getElementById('panelTitle');
      dom.sidebar = document.getElementById('workspaceSidebar');
      dom.nav = document.getElementById('wsNav');
      dom.commandBar = document.getElementById('commandBar');
      dom.commandBarControls = document.getElementById('cbControls');
      dom.metrics = document.getElementById('wsMetrics');
      dom.modeToggle = document.getElementById('modeToggle');
      dom.heatSlider = document.getElementById('heatSlider');

      if (!dom.stage) {
        console.error('PFExplorer: Essential stage DOM missing.');
        return;
      }

      // Initialize CommandBar
      if (window.CommandBar && dom.commandBarControls && !dom.commandBarControls.hasChildNodes()) {
        CommandBar.mount(dom.commandBarControls);
        state.filters = CommandBar.getFilters();
        state.mode = CommandBar.getMode();
      }
      
      if (dom.modeToggle) {
        dom.modeToggle.addEventListener('click', PF.toggleMode);
      }
      
      if (dom.heatSlider) {
        dom.heatSlider.addEventListener('input', function(e) {
          state.heat = parseFloat(e.target.value);
          document.dispatchEvent(new CustomEvent('pf:heatChange', { detail: { heat: state.heat } }));
        });
      }

      // Sidebar/Nav delegation
      if (dom.nav || dom.sidebar) {
        (dom.nav || dom.sidebar).addEventListener('click', function (e) {
          var btn = e.target.closest('[data-route]');
          if (btn) {
            PF.navigate(btn.getAttribute('data-route'));
          }
        });
      }

      // Drawer close
      var closeBtn = document.getElementById('drawerClose') || (dom.drawer ? dom.drawer.querySelector('.drawer-close') : null);
      if (closeBtn) closeBtn.addEventListener('click', PF.closeDrawer);
      if (dom.drawerToggle) {
        dom.drawerToggle.addEventListener('click', function () {
          if (dom.drawer.getAttribute('aria-hidden') === 'false') PF.closeDrawer();
          else PF.openDrawer();
        });
      }

      PF.renderSidebarMetrics();

      // Initial route
      var initial = window.location.hash.substring(1) || 'observatory';
      PF.navigate(initial);

      // Start loop
      PF.startLoop();
      
      // Global Resize
      window.addEventListener('resize', function () {
        var ctx = PF.getContext();
        if (currentPanel && typeof currentPanel.resize === 'function') {
          currentPanel.resize(ctx);
        }
      });

      // CommandBar Listeners
      document.addEventListener('pf:filtersChange', function (e) {
        state.filters = e.detail.filters;
        if (currentPanel && typeof currentPanel.onFiltersChange === 'function') {
          currentPanel.onFiltersChange(PF.getContext());
        }
      });

      document.addEventListener('pf:scaleChange', function (e) {
        state.scaleMeters = e.detail.anchor.meters;
        if (currentPanel && typeof currentPanel.onScaleChange === 'function') {
          currentPanel.onScaleChange(PF.getContext());
        }
      });
    },

    registerPanel: function (config) {
      if (!config.id) return;
      panels[config.id] = config;
      console.log('PFExplorer: Registered panel ->', config.id);
    },

    navigate: function (routeId) {
      if (!panels[routeId]) {
        console.warn('PFExplorer: Route not found ->', routeId);
        routeId = 'observatory';
      }

      var panel = panels[routeId];
      if (currentPanel && typeof currentPanel.unmount === 'function') {
        currentPanel.unmount(PF.getContext());
      }

      currentPanel = panel;
      state.currentRoute = routeId;
      window.location.hash = routeId;

      if (dom.panelTitle) dom.panelTitle.textContent = panel.title || routeId;
      
      // Update Sidebar state
      if (dom.sidebar) {
        Array.prototype.forEach.call(dom.sidebar.querySelectorAll('[data-route]'), function (btn) {
          var active = btn.getAttribute('data-route') === routeId;
          btn.classList.toggle('is-active', active);
          btn.setAttribute('aria-selected', String(active));
        });
      }

      // Mount
      dom.stage.innerHTML = '';
      var ctx = PF.getContext();
      panel.mount(ctx);

      if (typeof panel.resize === 'function') panel.resize(ctx);
      if (typeof panel.onModeChange === 'function') panel.onModeChange(ctx);

      console.log('PFExplorer: Navigated to ->', routeId);
    },

    toggleMode: function () {
      var modes = ['story', 'audit', 'math'];
      var idx = (modes.indexOf(state.mode) + 1) % modes.length;
      PF.setMode(modes[idx]);
    },

    setMode: function(mode) {
      state.mode = mode;
      if (dom.modeToggle) dom.modeToggle.textContent = state.mode.toUpperCase() + ' MODE';
      
      var ctx = PF.getContext();
      if (currentPanel && typeof currentPanel.onModeChange === 'function') {
        currentPanel.onModeChange(ctx);
      }
      
      if (state.mode === 'math' && window.CommandBar) {
        CommandBar.triggerTypeset();
      }
      
      if (state.selectedItem) PF.renderDrawer();
    },

    // ── Drawer / Evidence ───────────────────────────────────────────────────

    openDrawer: function () {
      if (!dom.drawer) return;
      dom.drawer.classList.add('is-open');
      dom.drawer.setAttribute('aria-hidden', 'false');
      if (dom.drawerToggle) dom.drawerToggle.setAttribute('aria-expanded', 'true');
    },

    closeDrawer: function () {
      if (!dom.drawer) return;
      dom.drawer.classList.remove('is-open');
      dom.drawer.setAttribute('aria-hidden', 'true');
      if (dom.drawerToggle) dom.drawerToggle.setAttribute('aria-expanded', 'false');
    },

    focusResult: function (id, options) {
      var item = PF.getResult(id);
      if (!item) return;
      state.selectedItem = { type: 'claim', data: item };
      PF.renderDrawer();
      if (options && options.open) PF.openDrawer();
    },

    focusDefinition: function (id, options) {
      var item = (window.PFClaimsData && window.PFClaimsData.DEFINITIONS || []).find(function(d){ return d.id === id; });
      if (!item) return;
      state.selectedItem = { type: 'def', data: item };
      PF.renderDrawer();
      if (options && options.open) PF.openDrawer();
    },

    renderDrawer: function () {
      var item = state.selectedItem;
      if (!item || !dom.drawerContent) return;

      var d = item.data;
      var html = '';
      if (dom.drawerTitle) dom.drawerTitle.textContent = d.title || 'Evidence';
      if (dom.drawerEyebrow) dom.drawerEyebrow.textContent = item.type === 'def' ? 'Canonical Definition' : 'Claim Evidence';

      if (item.type === 'claim') {
        var status = d.status || { label: 'UNAVAILABLE', color: 'gray' };
        var isNoGo = !!d.failedAt;
        var claimId = d.id || '';

        html = [
          '<div class="drawer-item">',
            '<header class="drawer-header">',
              '<span class="status-pill" style="--cc:var(--col-' + status.color + ')" data-claim-id="' + claimId + '">' + status.label + '</span>',
              '<h2>' + d.title + '</h2>',
            '</header>',
            '<div class="drawer-body">',
              '<section class="drawer-section story-only">',
                '<h3>Narrative</h3>',
                '<p>' + (d.story || 'No narrative description available.') + '</p>',
                d.oneLiner ? '<p class="drawer-quote">"' + d.oneLiner + '"</p>' : '',
              '</section>',
              '<section class="drawer-section audit-only">',
                '<h3>Hostile Audit</h3>',
                isNoGo ? [
                  '<div class="audit-block audit-block--nogo">',
                    '<p><strong>Failed at:</strong> ' + d.failedAt + '</p>',
                    '<p><strong>Failed assumption:</strong> ' + d.failedAssumption + '</p>',
                    '<p><strong>Lesson:</strong> ' + d.lesson + '</p>',
                  '</div>'
                ].join('') : [
                  '<div class="audit-block">',
                    '<p><strong>Claim:</strong> ' + (d.audit.claim || '') + '</p>',
                    '<p><strong>Standard Boundary:</strong> ' + (d.audit.standardBoundary || '') + '</p>',
                    '<p><strong>Derived Part:</strong> ' + (d.audit.derivedPart || '') + '</p>',
                    '<p class="obs-open-bridge"><strong>Open Bridge:</strong> ' + (d.audit.openBridge || 'None') + '</p>',
                    '<p class="drawer-falsifier"><strong>Falsifier:</strong> ' + (d.audit.falsifier || 'None') + '</p>',
                  '</div>'
                ].join(''),
              '</section>',
              '<section class="drawer-section math-only">',
                '<h3>Derivation</h3>',
                '<div class="drawer-formula">$$' + (d.math || '') + '$$</div>',
                d.confidence ? '<p class="drawer-meta">Confidence: ' + (d.confidence * 100).toFixed(1) + '%</p>' : '',
              '</section>',
              '<section class="drawer-section">',
                '<h3>Evidence Sources</h3>',
                '<ul class="drawer-sources">',
                  (d.sources || []).map(function(s) {
                    var label = s.split('/').pop();
                    if (/\.md$/i.test(s) && window.SourceViewer) {
                      return '<li><button class="obs-source-pill obs-source-pill--link" ' +
                        'onclick="SourceViewer.open(\'' + s.replace(/\\/g,'\\\\').replace(/'/g,"\\'") + '\')">' +
                        label + ' ↗</button></li>';
                    }
                    return '<li><span class="obs-source-pill">' + label + '</span></li>';
                  }).join(''),
                '</ul>',
              '</section>',
            '</div>',
          '</div>'
        ].join('');
      } else if (item.type === 'def') {
        html = [
          '<div class="drawer-item">',
            '<header class="drawer-header">',
              '<span class="status-pill" style="--cc:var(--col-white)">' + (d.auditLine || d.status || 'UNAVAILABLE') + '</span>',
              '<h2>' + d.title + '</h2>',
            '</header>',
            '<div class="drawer-body">',
              '<section class="drawer-section">',
                '<h3>Definition</h3>',
                '<p class="drawer-quote">"' + d.oneLiner + '"</p>',
                '<h4>Conceptual Context</h4>',
                '<p>' + d.storyLine + '</p>',
              '</section>',
              '<section class="drawer-section audit-only">',
                '<h3>Audit Boundary</h3>',
                '<p>' + d.auditLine + '</p>',
                '<p class="drawer-falsifier"><strong>Not this:</strong> ' + d.notThis + '</p>',
              '</section>',
              '<section class="drawer-section">',
                '<h3>Dependencies</h3>',
                '<div class="obs-pc-sources">',
                  (d.dependencies || []).map(function(dep) {
                    return '<button class="obs-source-pill" onclick="PFExplorer.focusDefinition(\''+dep+'\')">' + dep + '</button>';
                  }).join(''),
                '</div>',
              '</section>',
              '<section class="drawer-section">',
                '<h3>Canonical File</h3>',
                window.SourceViewer
                  ? '<button class="obs-source-pill obs-source-pill--link" onclick="SourceViewer.open(\'' +
                    d.file.replace(/'/g,"\\'") + '\')">' + d.file + ' ↗</button>'
                  : '<span class="obs-source-pill">' + d.file + '</span>',
              '</section>',
            '</div>',
          '</div>'
        ].join('');
      }

      dom.drawerContent.innerHTML = html;
      if (state.mode === 'math' && window.CommandBar) CommandBar.triggerTypeset();
    },

    // ── UI Helpers ──────────────────────────────────────────────────────────

    renderWrongIntuition: function (wi) {
      if (!wi) return '';
      return [
        '<div class="wrong-intuition-callout">',
          '<div class="wi-box wi-intuition">',
            '<span class="wi-label">Your intuition says:</span>',
            '<p class="wi-text">' + (wi.intuition || 'Standard Model assumption.') + '</p>',
          '</div>',
          '<div class="wi-arrow" aria-hidden="true">&#8595;</div>',
          '<div class="wi-box wi-reality">',
            '<span class="wi-label">Reality says:</span>',
            '<p class="wi-text">' + (wi.reality || 'Derived structural result.') + '</p>',
            wi.detail ? '<p class="wi-detail">' + wi.detail + '</p>' : '',
          '</div>',
        '</div>'
      ].join('');
    },

    compareBarHtml: function (val, ref, err, min, max) {
      var range = max - min;
      var valPct = Math.min(100, Math.max(0, ((val - min) / range) * 100));
      var refPct = Math.min(100, Math.max(0, ((ref - min) / range) * 100));
      var errText = typeof err === 'number' ? err.toFixed(2) + 'σ Error' : (err || '');
      
      return [
        '<div class="compare-bar-container">',
          '<div class="compare-bar-meta">',
            '<span class="compare-bar-label">Prediction Accuracy</span>',
            '<span class="compare-bar-err">' + errText + '</span>',
          '</div>',
          '<div class="compare-bar-track">',
            '<div class="compare-bar-ref" style="left: ' + refPct + '%"></div>',
            '<div class="compare-bar-val" style="left: ' + valPct + '%"></div>',
          '</div>',
          '<div class="compare-bar-range">',
            '<span>' + min.toFixed(4) + '</span>',
            '<span>' + max.toFixed(4) + '</span>',
          '</div>',
        '</div>'
      ].join('');
    },

    renderSidebarMetrics: function () {
      if (!dom.metrics) return;
      var data = window.PFClaimsData || {};
      var claims = data.CLAIMS || [];
      var derived = claims.filter(function (c) { return c.status && c.status.label === 'DERIVED'; }).length;
      var conditional = claims.filter(function (c) { return c.status && (c.status.label === 'CONDITIONAL' || c.status.label === 'PARTIAL'); }).length;
      dom.metrics.innerHTML = [
        '<div class="ws-metric-row"><strong>' + derived + '</strong><span>Derived</span></div>',
        '<div class="ws-metric-row"><strong>' + conditional + '</strong><span>Conditional</span></div>',
        '<div class="ws-metric-row"><strong>' + ((data.DEFINITIONS || []).length) + '</strong><span>Definitions</span></div>'
      ].join('');
    },

    syncActiveResultCards: function () {
      // Stub for panel-specific updates
    },

    // Data accessors backed by window.PFExplorerData (curated snapshot).
    getAuditedResults: function () {
      var src = window.PFExplorerData || { results: [] };
      return (src.results || []).filter(function (r) { return !r.unsynced; });
    },

    getLinkedPanelIdsForScale: function (scale) {
      if (!scale || !scale.resultIds) return [];
      var src = window.PFExplorerData || { panelMeta: [] };
      var resultIds = scale.resultIds;
      var linked = {};
      (src.panelMeta || []).forEach(function (p) {
        (p.linkedResultIds || []).forEach(function (rid) {
          if (resultIds.indexOf(rid) >= 0) linked[p.id] = true;
        });
      });
      return Object.keys(linked);
    },

    statusToClass: function (status) {
      if (window.PFTruth && typeof window.PFTruth.statusToClass === 'function') {
        return window.PFTruth.statusToClass(status);
      }
      if (status && typeof status === 'object' && status.label) {
        return window.PFTruth && window.PFTruth.statusToClass
          ? window.PFTruth.statusToClass(status.label)
          : 'status-open';
      }
      return 'status-open';
    },

    createResultCard: function (result, options) {
      options = options || {};
      var card = document.createElement('div');
      if (!result) {
        card.className = 'result-card';
        card.textContent = '—';
        return card;
      }
      var statusStr = (result.status && result.status.label) ? result.status.label : (result.status || 'UNAVAILABLE');
      var statusClass = PF.statusToClass(statusStr);
      card.className = 'result-card ' + statusClass;
      if (result.id) card.setAttribute('data-result-id', result.id);
      var confidence = (typeof result.confidence === 'number')
        ? Math.round(result.confidence * 100) + '%' : 'n/a';
      var parts = [
        '<div class="result-card-head">',
          '<div class="result-card-title">', (result.title || ''), '</div>',
          '<div class="result-card-status ', statusClass.replace(/^status-/, ''), '">', statusStr, '</div>',
        '</div>'
      ];
      if (result.formula) parts.push('<div class="result-card-formula">', result.formula, '</div>');
      parts.push('<div class="result-card-confidence">Confidence: ', confidence, '</div>');
      if (options.showInlineFalsifier && result.falsifier) {
        parts.push('<div class="result-card-falsifier"><strong>Falsifier:</strong> ', result.falsifier, '</div>');
      }
      if (result.summary) parts.push('<div class="result-card-summary">', result.summary, '</div>');
      card.innerHTML = parts.join('');
      if (options.wholeCardFocus && result.id) {
        card.addEventListener('click', function () {
          if (typeof PF.focusResult === 'function') PF.focusResult(result.id, { open: true });
        });
      }
      return card;
    },

    // ── Utils / Logic ───────────────────────────────────────────────────────

    getResult: function (id) {
      if (!window.PFClaimsData) return null;
      var all = [].concat(window.PFClaimsData.CLAIMS || [], window.PFClaimsData.NOGOS || []);
      return all.find(function(c) { return c.id === id; });
    },

    getContext: function () {
      return {
        stage: dom.stage,
        state: state,
        app: PF,
        utils: PF.utils,
        data: window.PFExplorerData || { results: [], scales: [], panelMeta: [], definitions: [] }
      };
    },

    startLoop: function () {
      if (isLooping) return;
      isLooping = true;
      requestAnimationFrame(loop);
    },

    stopLoop: function () {
      isLooping = false;
    },

    utils: {
      casimirRoot: function (j) {
        var c2 = j * (j + 1);
        return (-c2 + Math.sqrt(c2 * c2 + 4 * c2)) / 2;
      },
      formatScientific: function (value, digits) {
        if (value === null || value === undefined || isNaN(value)) return 'n/a';
        var d = (typeof digits === 'number') ? digits : 3;
        return Number(value).toExponential(d);
      },
      koideQ: function (masses) {
        var sumSqrt = masses.reduce(function (a, b) { return a + Math.sqrt(b); }, 0);
        var sumM = masses.reduce(function (a, b) { return a + b; }, 0);
        return sumM / Math.pow(sumSqrt, 2);
      },
      computeKoideRA: function (masses) {
        var sqrtMasses = masses.map(Math.sqrt);
        var r = Math.sqrt(sqrtMasses.reduce(function(a,b){return a+b*b;},0)/3);
        var a = sqrtMasses.reduce(function(a,b){return a+b;},0)/3;
        return { r: r, a: a, ratio: r/a };
      },
      qOfN: function (n) {
        return (2 * n) / (2 * n + 3);
      }
    }
  };

  function loop(timestamp) {
    if (!isLooping) return;
    
    var dt = lastTime ? (timestamp - lastTime) / 1000 : 0.016;
    lastTime = timestamp;

    if (currentPanel && typeof currentPanel.update === 'function') {
      try {
        currentPanel.update(PF.getContext(), dt, timestamp);
      } catch (e) {
        console.error('PFExplorer: Panel update error ->', e);
      }
    }

    requestAnimationFrame(loop);
  }

  // Export
  PF.state = state;
  window.PFExplorer = PF;

  // Final Bootstrap
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    PF.init();
  } else {
    document.addEventListener('DOMContentLoaded', PF.init);
  }

}());
