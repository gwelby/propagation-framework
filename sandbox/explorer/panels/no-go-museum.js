/**
 * panels/no-go-museum.js — No-Go Museum Workspace
 * Failed routes are first-class evidence.
 * Six audited no-go routes from data.claims.js NOGOS array.
 */
(function () {
  'use strict';

  var WORKSPACE_ID = 'no-go-museum';

  function buildNoGoHTML(nogos, claims) {
    var claimMap = {};
    claims.forEach(function(c){ claimMap[c.id] = c; });

    var cards = nogos.map(function(ng) {
      var parent = claimMap[ng.target] || null;
      var parentTitle = parent ? parent.title : ng.target;
      var parentStatus = parent && parent.status ? parent.status.label : '—';

      return [
        '<article class="ng-card" data-nogo-id="' + ng.id + '">',
          '<div class="ng-card-head">',
            '<div class="ng-skull" aria-hidden="true">✕</div>',
            '<div class="ng-meta">',
              '<h4 class="ng-title">' + ng.title + '</h4>',
              '<div class="ng-parent">',
                'Attacked: <button class="ng-parent-link" data-result-id="'+ng.target+'" type="button">'+parentTitle+'</button>',
                ' — status: <span class="ng-parent-status">'+parentStatus+'</span>',
              '</div>',
            '</div>',
            '<span class="ng-date">Negative Result ' + (ng.failedAt || '—') + '</span>',
          '</div>',
          '<div class="ng-assumption">',
            '<span class="ng-lbl">Intuitive Trap</span>',
            '<div class="ng-assumption-text">"' + (ng.failedAssumption || '—') + '"</div>',
          '</div>',
          '<div class="ng-lesson">',
            '<span class="ng-lbl">The Revelation</span>',
            '<p>' + (ng.lesson || '—') + '</p>',
          '</div>',
          '<div class="ng-codex-stamp">',
            '<span class="ng-codex-eye" aria-hidden="true">⚖</span>',
            '<span>Integrity Audit: Route Honest Negative</span>',
          '</div>',
        '</article>',
      ].join('');
    }).join('');

    return [
      '<div class="ng-shell">',
        '<div class="ng-header">',
          '<div class="ng-header-text">',
            '<h2 class="ng-headline"><span style="color:#ff4455; font-family:serif; margin-right:8px;">✕</span> The Museum of Honest Failures</h2>',
            '<p class="ng-subhead">Every red line here is a victory. In physics, knowing exactly where the wall is proves that the room exists. We celebrate these falsified routes because they protected us from wrong intuitions and forced us toward the structural truth.</p>',
            '<p class="interaction-cue"><strong>Interaction:</strong> Click the "Attacked" target link to view the derivation node that invalidated the route. Review the intuitive trap for each.</p>',
          '</div>',
          '<div class="ng-count-badge">',
            '<strong>' + nogos.length + '</strong>',
            '<span>falsified routes</span>',
          '</div>',
        '</div>',

        '<div class="ng-policy-block">',
          '<span class="ng-policy-icon" aria-hidden="true">🔥</span>',
          '<div>',
            '<strong>The Fire of Falsification</strong>',
            '<p>We do not bury our mistakes. We frame them. A route enters this museum only when it has been mathematically or empirically destroyed. These are the "honest negatives" that force us toward the truth.</p>',
          '</div>',
        '</div>',

        '<div class="ng-grid" id="ngGrid">',
          cards,
        '</div>',

        '<div class="ng-open-section">',
          '<h3 class="ng-open-title">The Next Walls</h3>',
          '<p class="ng-open-desc">These routes are currently under attack. They may survive. They may burn. Either outcome is an advance.</p>',
          '<ul class="ng-open-list">',
            '<li><span class="ng-open-cue">Frontier:</span> T1 physical realization non-redundancy theorem</li>',
            '<li><span class="ng-open-cue">Frontier:</span> T2 denominator theorem (2×2 bridge)</li>',
            '<li><span class="ng-open-cue">Frontier:</span> God Equation H_prod statistical independence</li>',
            '<li><span class="ng-open-cue">Frontier:</span> Koide phase δ=2/9 selector</li>',
          '</ul>',
        '</div>',
      '</div>',
    ].join('');
  }

  PFExplorer.registerPanel({
    id: WORKSPACE_ID,
    title: 'No-Go Museum',

    mount: function (ctx) {
      var data = window.PFClaimsData || {};
      var nogos = data.NOGOS || [];
      var claims = data.CLAIMS || [];

      ctx.stage.innerHTML = buildNoGoHTML(nogos, claims);

      // Wire parent claim links
      Array.prototype.forEach.call(ctx.stage.querySelectorAll('[data-result-id]'), function(btn) {
        btn.addEventListener('click', function() {
          var id = btn.getAttribute('data-result-id');
          PFExplorer.focusResult(id, { open: true });
        });
      });
    },

    unmount: function () {},
    resize: function () {},
  });

}());
