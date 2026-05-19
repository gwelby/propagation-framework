/**
 * panels/experiment-bench.js
 * The Audit Wall — Falsification Dashboard and Claims Registry.
 */
(function () {
  'use strict';

  function matchesQuery(claim, query) {
    if (!query) return true;
    const q = query.toLowerCase();
    const haystack = [
      claim.title,
      claim.math,
      claim.story,
      claim.audit && claim.audit.claim,
      claim.audit && claim.audit.derivedPart,
      claim.audit && claim.audit.openBridge,
      claim.audit && claim.audit.falsifier
    ].filter(Boolean).join(' ').toLowerCase();
    return haystack.indexOf(q) >= 0;
  }

  function claimSummary(claim) {
    return claim.story || (claim.audit && claim.audit.claim) || 'No summary available.';
  }

  function claimFormula(claim) {
    return claim.math || '';
  }

  function claimFalsifier(claim) {
    return (claim.audit && claim.audit.falsifier) || '';
  }

  function createFilterChip(label, status, isActive, count) {
    const chip = document.createElement('button');
    chip.className = 'eb-chip' + (isActive ? ' is-active' : '');
    chip.type = 'button';
    chip.setAttribute('data-filter', status);
    chip.innerHTML = label + ' <span class="eb-chip-count">' + count + '</span>';
    return chip;
  }

  PFExplorer.registerPanel({
    id: 'experiment-bench',
    title: 'Experiment Bench',

    mount: function (ctx) {
      const data = window.PFClaimsData || {};
      const claims = data.CLAIMS || [];
      
      const counts = {};
      claims.forEach(c => {
        counts[c.status.label] = (counts[c.status.label] || 0) + 1;
      });

      ctx.stage.innerHTML = [
        '<div class="eb-shell">',
          '<section class="eb-hero">',
            '<div class="eb-hero-text">',
              '<p class="eb-eyebrow"><span style="color:#ffdd55; font-family:serif; margin-right:8px;">⚗</span> The Audit Wall</p>',
              '<h2 class="eb-headline">Registry of Physical Truth</h2>',
              '<p class="eb-subhead">Every claim in the Propagation Framework is audited against empirical data. These are the only audited results. If a claim isn\'t here, it is conjecture. If it is here, its falsification criteria are public and verifiable.</p>',
              '<p class="interaction-cue"><strong>Interaction:</strong> Filter claims by status using the tabs. Click on any claim to open the detailed Evidence Drawer for derivation logs and source references.</p>',
            '</div>',
            '<div class="eb-stats">',
              '<div class="eb-stat-item"><strong>' + (counts['DERIVED'] || 0) + '</strong><span>Derived</span></div>',
              '<div class="eb-stat-item"><strong>' + (counts['CONDITIONAL'] || 0) + '</strong><span>Conditional</span></div>',
              '<div class="eb-stat-item"><strong>' + (counts['ARGUED'] || 0) + '</strong><span>Argued</span></div>',
              '<div class="eb-stat-item"><strong>' + (counts['EMPIRICAL'] || 0) + '</strong><span>Empirical</span></div>',
            '</div>',
          '</section>',

          '<div class="eb-controls">',
            '<div class="eb-filters" id="ebFilters"></div>',
            '<div class="eb-search-wrap">',
              '<input type="text" id="ebSearch" placeholder="Search claims, math, falsifiers..." class="eb-search-input">',
            '</div>',
          '</div>',

          '<div class="eb-grid" id="ebGrid"></div>',
        '</div>'
      ].join('');

      this.state = {
        activeFilter: 'all',
        searchQuery: '',
        claims: claims
      };

      this.renderFilters(ctx);
      this.renderGrid(ctx);
      this.bindEvents(ctx);
    },

    renderFilters: function (ctx) {
      const root = ctx.stage.querySelector('#ebFilters');
      if (!root) return;
      
      const claims = this.state.claims;
      const counts = {};
      claims.forEach(c => {
        counts[c.status.label] = (counts[c.status.label] || 0) + 1;
      });

      const filterConfig = [
        { label: 'All', status: 'all', count: claims.length },
        { label: 'Derived', status: 'DERIVED', count: counts['DERIVED'] || 0 },
        { label: 'Conditional', status: 'CONDITIONAL', count: counts['CONDITIONAL'] || 0 },
        { label: 'Argued', status: 'ARGUED', count: counts['ARGUED'] || 0 },
        { label: 'Empirical', status: 'EMPIRICAL', count: counts['EMPIRICAL'] || 0 }
      ];

      root.innerHTML = '';
      filterConfig.forEach(config => {
        const chip = createFilterChip(config.label, config.status, this.state.activeFilter === config.status, config.count);
        chip.addEventListener('click', () => {
          this.state.activeFilter = config.status;
          this.renderFilters(ctx);
          this.renderGrid(ctx);
        });
        root.appendChild(chip);
      });
    },

    renderGrid: function (ctx) {
      const grid = ctx.stage.querySelector('#ebGrid');
      if (!grid) return;

      const filtered = this.state.claims.filter(c => {
        if (this.state.activeFilter !== 'all' && c.status.label !== this.state.activeFilter) return false;
        return matchesQuery(c, this.state.searchQuery);
      });

      if (filtered.length === 0) {
        grid.innerHTML = '<div class="eb-empty">No audited results match your criteria.</div>';
        return;
      }

      grid.innerHTML = filtered.map(c => {
        const statusClass = 'status-' + c.status.label.toLowerCase().replace(' ', '-');
        return [
          '<article class="eb-card" data-claim-id="' + c.id + '">',
            '<div class="eb-card-head">',
              '<span class="eb-status-pill ' + statusClass + '">' + c.status.label + '</span>',
              '<h4 class="eb-card-title">' + c.title + '</h4>',
            '</div>',
            '<p class="eb-card-summary">' + claimSummary(c) + '</p>',
            claimFormula(c) ? '<div class="eb-card-formula">' + claimFormula(c) + '</div>' : '',
            claimFalsifier(c) ? '<p class="eb-card-falsifier"><strong>Falsifier:</strong> ' + claimFalsifier(c) + '</p>' : '',
            '<div class="eb-card-foot">',
              '<button class="eb-inspect-btn" data-id="' + c.id + '">Inspect Evidence</button>',
            '</div>',
          '</article>'
        ].join('');
      }).join('');

      // Bind inspect buttons
      Array.prototype.forEach.call(grid.querySelectorAll('.eb-inspect-btn'), btn => {
        btn.addEventListener('click', () => {
          const id = btn.getAttribute('data-id');
          PFExplorer.focusResult(id, { open: true });
        });
      });
    },

    bindEvents: function (ctx) {
      const search = ctx.stage.querySelector('#ebSearch');
      if (search) {
        search.addEventListener('input', (e) => {
          this.state.searchQuery = e.target.value;
          this.renderGrid(ctx);
        });
      }
    },

    unmount: function () {
      this.state = null;
    },

    resize: function () {}
  });

}());
