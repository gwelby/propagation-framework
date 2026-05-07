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
                'Target: <button class="ng-parent-link" data-result-id="'+ng.target+'" type="button">'+parentTitle+'</button>',
                ' — currently <span class="ng-parent-status">'+parentStatus+'</span>',
              '</div>',
            '</div>',
            '<span class="ng-date">Failed ' + (ng.failedAt || '—') + '</span>',
          '</div>',
          '<div class="ng-assumption">',
            '<span class="ng-lbl">Failed assumption</span>',
            '<div class="ng-assumption-text">' + (ng.failedAssumption || '—') + '</div>',
          '</div>',
          '<div class="ng-lesson">',
            '<span class="ng-lbl">Lesson</span>',
            '<p>' + (ng.lesson || '—') + '</p>',
          '</div>',
          '<div class="ng-codex-stamp">',
            '<span class="ng-codex-eye" aria-hidden="true">👁</span>',
            '<span>Codex audit — route closed</span>',
          '</div>',
        '</article>',
      ].join('');
    }).join('');

    return [
      '<div class="ng-shell">',
        '<div class="ng-header">',
          '<div class="ng-header-text">',
            '<h2 class="ng-headline">No-Go Museum</h2>',
            '<p class="ng-subhead">Every failed route is kept as evidence. Knowing what doesn\'t work is as important as knowing what does. These are not embarrassments — they are the audit trail.</p>',
          '</div>',
          '<div class="ng-count-badge">',
            '<strong>' + nogos.length + '</strong>',
            '<span>closed routes</span>',
          '</div>',
        '</div>',

        '<div class="ng-policy-block">',
          '<span class="ng-policy-icon" aria-hidden="true">⚖</span>',
          '<div>',
            '<strong>Truth Policy</strong>',
            '<p>A route is admitted to the No-Go Museum only when an explicit mathematical, empirical, or logical closure has been documented and audited by Codex. "Doesn\'t feel right" is not a no-go. "J⁽⁰⁾+J⁽¹⁾+J⁽²⁾=0 identically" is.</p>',
          '</div>',
        '</div>',

        '<div class="ng-grid" id="ngGrid">',
          cards,
        '</div>',

        '<div class="ng-open-section">',
          '<h3 class="ng-open-title">Still Open</h3>',
          '<p class="ng-open-desc">Routes that have not been closed. These are active research fronts, not no-gos. The distinction matters.</p>',
          '<ul class="ng-open-list">',
            '<li>T1 physical realization non-redundancy theorem — Family C routes still open</li>',
            '<li>T2 denominator theorem — full PF→local 2×2 bridge not yet built</li>',
            '<li>God Equation H_prod statistical independence — Path A and Family C still active</li>',
            '<li>Koide phase δ=2/9 selector — all five audited routes honest negatives; selector still missing</li>',
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
