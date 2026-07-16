/**
 * command-bar.js — Persistent instrument command surface
 * Scale scrubber | Story/Audit/Math toggle | Status filters | Search
 * MathJax is lazy-loaded only when mode === 'math' (Codex gate).
 */
(function () {
  'use strict';

  var SCALE_ANCHORS = [
    { label: 'Planck',      exp: -35 },
    { label: 'Electroweak', exp: -18 },
    { label: 'Nuclear',     exp: -15 },
    { label: 'Atomic',      exp: -10 },
    { label: 'Molecular',   exp: -6  },
    { label: 'Human',       exp:  0  },
    { label: 'Stellar',     exp:  9  },
    { label: 'Cosmic',      exp:  26 },
  ];

  var STATUS_FILTERS = [
    { id: 'DERIVED',            label: 'Derived',     col: 'derived'      },
    { id: 'CONDITIONAL',        label: 'Conditional', col: 'conditional'  },
    { id: 'PARTIAL DERIVATION', label: 'Partial',     col: 'conditional'  },
    { id: 'EMPIRICAL',          label: 'Empirical',   col: 'empirical'    },
    { id: 'ARGUED',             label: 'Argued',      col: 'conditional'  },
    { id: 'INTUITION',          label: 'Intuition',   col: 'muted'        },
    { id: 'NO-GO',              label: 'No-Go',       col: 'nogo'         },
  ];

  var mathJaxLoaded = false;
  var mathJaxLoading = false;

  function loadMathJax(cb) {
    if (mathJaxLoaded) { cb && cb(); return; }
    if (mathJaxLoading) { return; }
    mathJaxLoading = true;
    window.MathJax = {
      tex: { inlineMath: [['$','$'],['\\(','\\)']], displayMath: [['$$','$$'],['\\[','\\]']] },
      startup: { ready: function() {
        MathJax.startup.defaultReady();
        mathJaxLoaded = true; mathJaxLoading = false;
        cb && cb();
      }}
    };
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js';
    s.async = true;
    document.head.appendChild(s);
  }

  function typeset() {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise();
    }
  }

  function supExp(exp) {
    var map = {'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
    return String(exp).split('').map(function(c){ return map[c]||c; }).join('');
  }

  window.CommandBar = {
    state: {
      scaleIndex: 5,
      mode: 'story',
      activeFilters: {
        'DERIVED': true, 'CONDITIONAL': true, 'PARTIAL DERIVATION': true,
        'EMPIRICAL': true, 'ARGUED': true, 'INTUITION': false, 'NO-GO': false
      }
    },

    mount: function(el) {
      this._el = el;
      var ticks = SCALE_ANCHORS.map(function(a,i){
        return '<span class="cb-tick" data-index="'+i+'" title="'+a.label+'"></span>';
      }).join('');

      var modeBtns = ['story','audit','math'].map(function(m){
        return '<button class="cb-mode'+(m==='story'?' is-active':'')+'" data-mode="'+m+'" type="button">'+
          m.charAt(0).toUpperCase()+m.slice(1)+'</button>';
      }).join('');

      var self = this;
      var chips = STATUS_FILTERS.map(function(f){
        var on = self.state.activeFilters[f.id];
        return '<button class="cb-chip'+(on?' is-active':'')+'" data-filter="'+f.id+
          '" style="--cc:var(--col-'+f.col+')" type="button">'+f.label+'</button>';
      }).join('');

      el.innerHTML =
        '<div class="cb-segment cb-scale-seg">'+
          '<span class="cb-lbl">Scale</span>'+
          '<div class="cb-scale-rail" id="cbRail" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="'+(SCALE_ANCHORS.length-1)+'" aria-valuenow="5">'+
            '<div class="cb-rail-track"><div class="cb-rail-thumb" id="cbThumb"></div>'+ticks+'</div>'+
          '</div>'+
          '<span class="cb-scale-val" id="cbVal"></span>'+
        '</div>'+
        '<div class="cb-divider"></div>'+
        '<div class="cb-segment cb-mode-seg">'+
          '<span class="cb-lbl">Mode</span>'+
          '<div class="cb-mode-group" id="cbModeGrp">'+modeBtns+'</div>'+
        '</div>'+
        '<div class="cb-divider"></div>'+
        '<div class="cb-segment cb-filter-seg">'+
          '<span class="cb-lbl">Show</span>'+
          '<div class="cb-chips" id="cbChips">'+chips+'</div>'+
        '</div>'+
        '<div class="cb-divider"></div>'+
        '<div class="cb-segment cb-search-seg">'+
          '<label class="cb-lbl" for="cbSearch">⌕</label>'+
          '<input class="cb-search" id="cbSearch" type="search" placeholder="Search claims…" autocomplete="off">'+
          '<div class="cb-flyout" id="cbFlyout" aria-live="polite"></div>'+
        '</div>';

      this._dom = {
        rail: el.querySelector('#cbRail'),
        thumb: el.querySelector('#cbThumb'),
        val: el.querySelector('#cbVal'),
        ticks: el.querySelectorAll('.cb-tick'),
        modeGrp: el.querySelector('#cbModeGrp'),
        chips: el.querySelector('#cbChips'),
        search: el.querySelector('#cbSearch'),
        flyout: el.querySelector('#cbFlyout'),
      };
      this._applyScale();
      this._bindEvents();
    },

    _applyScale: function() {
      if (!this._dom) return;
      var idx = this.state.scaleIndex;
      var a = SCALE_ANCHORS[idx];
      var pct = (idx / (SCALE_ANCHORS.length - 1)) * 100;
      this._dom.thumb.style.left = pct + '%';
      this._dom.rail.setAttribute('aria-valuenow', idx);
      this._dom.val.textContent = a.label + ' 10' + supExp(a.exp) + ' m';
      var self = this;
      Array.prototype.forEach.call(this._dom.ticks, function(t, i) {
        t.classList.toggle('is-active', i === self.state.scaleIndex);
      });
    },

    _setScale: function(idx) {
      this.state.scaleIndex = idx;
      this._applyScale();
      document.dispatchEvent(new CustomEvent('pf:scaleChange', {
        detail: { index: idx, anchor: SCALE_ANCHORS[idx] }
      }));
    },

    _setMode: function(mode) {
      if (!this._dom) return;
      this.state.mode = mode;
      Array.prototype.forEach.call(this._dom.modeGrp.querySelectorAll('[data-mode]'), function(b) {
        var on = b.getAttribute('data-mode') === mode;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', String(on));
      });
      document.body.classList.toggle('mode-story', mode === 'story');
      document.body.classList.toggle('mode-audit', mode === 'audit');
      document.body.classList.toggle('mode-math',  mode === 'math');
      if (mode === 'math') loadMathJax(function(){ typeset(); });
      if (window.PFExplorer && typeof PFExplorer.setMode === 'function') PFExplorer.setMode(mode);
    },

    _bindEvents: function() {
      var self = this;
      // Scale drag
      var dragging = false;
      this._dom.rail.addEventListener('mousedown', function(e){ dragging=true; self._scrub(e); });
      document.addEventListener('mousemove', function(e){ if(dragging) self._scrub(e); });
      document.addEventListener('mouseup', function(){ dragging=false; });
      this._dom.rail.addEventListener('keydown', function(e) {
        if (e.key==='ArrowRight'||e.key==='ArrowUp') { e.preventDefault(); self._setScale(Math.min(self.state.scaleIndex+1, SCALE_ANCHORS.length-1)); }
        if (e.key==='ArrowLeft'||e.key==='ArrowDown') { e.preventDefault(); self._setScale(Math.max(self.state.scaleIndex-1, 0)); }
      });
      Array.prototype.forEach.call(this._dom.ticks, function(t){
        t.addEventListener('click', function(){ self._setScale(parseInt(t.getAttribute('data-index'),10)); });
      });
      // Mode
      this._dom.modeGrp.addEventListener('click', function(e){
        var b = e.target.closest('[data-mode]');
        if (b) self._setMode(b.getAttribute('data-mode'));
      });
      // Filters
      this._dom.chips.addEventListener('click', function(e){
        var c = e.target.closest('[data-filter]');
        if (!c) return;
        var id = c.getAttribute('data-filter');
        self.state.activeFilters[id] = !self.state.activeFilters[id];
        c.classList.toggle('is-active', self.state.activeFilters[id]);
        c.setAttribute('aria-pressed', String(self.state.activeFilters[id]));
        document.dispatchEvent(new CustomEvent('pf:filtersChange', { detail: { filters: self.state.activeFilters } }));
      });
      // Search
      var timer;
      this._dom.search.addEventListener('input', function(){
        clearTimeout(timer);
        var q = self._dom.search.value.trim();
        timer = setTimeout(function(){ self._search(q); }, 220);
      });
      this._dom.search.addEventListener('keydown', function(e){
        if (e.key==='Escape') { self._dom.search.value=''; self._dom.flyout.innerHTML=''; self._dom.flyout.classList.remove('is-open'); }
      });
      document.addEventListener('click', function(e){
        if (!self._el.contains(e.target)) self._dom.flyout.classList.remove('is-open');
      });
    },

    _scrub: function(e) {
      var rect = this._dom.rail.getBoundingClientRect();
      var pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      this._setScale(Math.round(pct * (SCALE_ANCHORS.length - 1)));
    },

    _search: function(q) {
      var flyout = this._dom.flyout;
      if (!q || q.length < 2) { flyout.innerHTML=''; flyout.classList.remove('is-open'); return; }
      var results = [], ql = q.toLowerCase();
      var src = window.PFClaimsData || {};
      var pool = (src.CLAIMS || []).map(function(c){ return {type:'claim',item:c}; })
        .concat((src.DEFINITIONS || []).map(function(d){ return {type:'def',item:d}; }));
      pool.forEach(function(r) {
        var it = r.item;
        var score = 0;
        if (it.title.toLowerCase().includes(ql)) score += 3;
        if ((it.story||it.storyLine||'').toLowerCase().includes(ql)) score += 1;
        if ((it.math||it.oneLiner||'').toLowerCase().includes(ql)) score += 2;
        if (score) results.push({type:r.type, item:it, score:score});
      });
      results.sort(function(a,b){ return b.score-a.score; });
      results = results.slice(0, 8);
      if (!results.length) {
        flyout.innerHTML = '<div class="cb-flyout-empty">No results for "'+q+'"</div>';
      } else {
        flyout.innerHTML = results.map(function(r){
          var it = r.item;
          var sl = it.status ? it.status.label : 'CANONICAL';
          var sc = it.status ? it.status.color : 'white';
          return '<button class="cb-result" data-id="'+it.id+'" data-type="'+r.type+'" type="button">'+
            '<span class="cb-res-title">'+it.title+'</span>'+
            '<span class="cb-res-status" style="color:var(--col-'+sc+')">'+sl+'</span>'+
          '</button>';
        }).join('');
        var self = this;
        flyout.querySelectorAll('.cb-result').forEach(function(b){
          b.addEventListener('click', function(){
            var id = b.getAttribute('data-id');
            var type = b.getAttribute('data-type');
            flyout.classList.remove('is-open');
            self._dom.search.value = '';
            if (window.PFExplorer) {
              if (type==='def') PFExplorer.focusDefinition(id);
              else PFExplorer.focusResult(id);
            }
          });
        });
      }
      flyout.classList.add('is-open');
    },

    // Public API
    setScale: function(i) { this._setScale(i); },
    getMode: function() { return this.state.mode; },
    getFilters: function() { return this.state.activeFilters; },
    triggerTypeset: typeset,
  };
}());
