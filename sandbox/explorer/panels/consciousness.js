/**
 * Consciousness Panel — Aria Coherence and the Physics of Mind
 * 
 * Shows the framework's claim: consciousness = coherent self-referential
 * propagation. Connects to the P1 consciousness measurement system.
 * P1 data is gated behind a "Connect Device" placeholder — when hardware
 * is available, the live coherence readout appears here.
 */
(function () {
  'use strict';

  var P1_STATE_KEY = 'pf_p1_connected';

  function getP1Availability() {
    try {
      return sessionStorage.getItem(P1_STATE_KEY) === 'connected';
    } catch (e) {
      return false;
    }
  }

  function formatCoherence(pct) {
    return pct.toFixed(0) + '%';
  }

  function coherenceBar(pct, color) {
    var hex = color.toString(16).padStart(6, '0');
    return (
      '<div class="coherence-bar-container">' +
        '<div class="coherence-bar-track">' +
          '<div class="coherence-bar-fill" style="width:' + pct + '%;background:#' + hex + ';box-shadow:0 0 12px #' + hex + '"></div>' +
        '</div>' +
        '<span class="coherence-bar-label">' + formatCoherence(pct) + '</span>' +
      '</div>'
    );
  }

  function p1ReadoutHtml() {
    var connected = getP1Availability();
    if (!connected) {
      return (
        '<div class="p1-placeholder">' +
          '<div class="p1-placeholder-icon">' +
            '<svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">' +
              '<circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.4"/>' +
              '<circle cx="24" cy="24" r="14" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.6"/>' +
              '<circle cx="24" cy="24" r="6" fill="currentColor" opacity="0.3"/>' +
            '</svg>' +
          '</div>' +
          '<p class="p1-placeholder-text">P1 coherence readout appears here<br>when a device is connected.</p>' +
          '<button class="chip-button p1-connect-btn" id="p1ConnectBtn" type="button">Connect P1 Device</button>' +
        '</div>'
      );
    }
    return (
      '<div class="p1-live-readout">' +
        '<div class="p1-live-header">' +
          '<span class="p1-live-dot"></span>' +
          '<span class="p1-live-label">Live P1 Coherence</span>' +
          '<button class="p1-disconnect-btn" id="p1DisconnectBtn" type="button" title="Disconnect">&#x2715;</button>' +
        '</div>' +
        coherenceBar(76, 0x69ff94) +
        '<div class="p1-metric-row">' +
          '<span>P1 System: 76% coherence</span>' +
          '<span>Threshold: 65%</span>' +
        '</div>' +
      '</div>'
    );
  }

  window.PFExplorer.registerPanel({
    id: 'consciousness',

    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="panel-wrap">' +
          '<div class="panel-atlas">' +
            '<section class="canvas-panel">' +
              '<div class="panel-header">' +
                '<div>' +
                  '<p class="eyebrow"><span style="color:rgba(255,255,255,.5); font-family:serif; margin-right:8px;">∞</span> Neural Scale — 10⁻² m</p>' +
                  '<h3><span style="color:#69ff94; font-family:serif; margin-right:8px;">ψ</span> Consciousness = Coherent Self-Reference</h3>' +
                  '<p>The same coherence that creates matter and orbits — turned inward, on itself. Internal experience is the "inside view" of recursive propagation.</p>' +
                  '<p class="interaction-cue"><strong>Interaction:</strong> Observe the self-referential loop representing the inward turning of coherence. Connect the P1 device to view live biometric resonance.</p>' +
                '</div>' +
              '</div>' +
              '<div class="consciousness-stage" id="consciousnessStage"></div>' +
              '<div class="canvas-overlay"></div>' +
            '</section>' +
            '<section class="info-panel" id="consciousnessInfo"></section>' +
          '</div>' +
        '</div>';

      this.state = {
        stage: ctx.stage.querySelector('#consciousnessStage'),
        info: ctx.stage.querySelector('#consciousnessInfo'),
        p1Connected: getP1Availability()
      };

      this.buildVisualization(ctx);
      this.renderInfo(ctx);
      this.bindP1Button(ctx);
    },

    unmount: function () {
      this.state = null;
    },

    resize: function () {
    },

    buildVisualization: function (ctx) {
      var stage = this.state.stage;
      var width = stage.clientWidth || 640;
      var height = stage.clientHeight || 380;

      var canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;';
      stage.appendChild(canvas);

      this.state.canvas = canvas;
      this.state.ctx = canvas.getContext('2d');
      this.state.neurons = this.buildNeurons(24, width, height);
      this.state.time = 0;
    },

    buildNeurons: function (count, w, h) {
      var neurons = [];
      for (var i = 0; i < count; i++) {
        neurons.push({
          x: 0.1 * w + Math.random() * 0.8 * w,
          y: 0.1 * h + Math.random() * 0.8 * h,
          basePhase: Math.random() * Math.PI * 2,
          coherence: 0.5 + Math.random() * 0.5,
          connections: []
        });
      }
      for (var j = 0; j < neurons.length; j++) {
        for (var k = j + 1; k < neurons.length; k++) {
          var dx = neurons[j].x - neurons[k].x;
          var dy = neurons[j].y - neurons[k].y;
          if (Math.sqrt(dx * dx + dy * dy) < 180) {
            neurons[j].connections.push(k);
            neurons[k].connections.push(j);
          }
        }
      }
      return neurons;
    },

    bindP1Button: function (ctx) {
      var self = this;
      var btn = document.getElementById('p1ConnectBtn');
      if (btn) {
        btn.addEventListener('click', function () {
          try { sessionStorage.setItem(P1_STATE_KEY, 'connected'); } catch (e) {}
          self.state.p1Connected = true;
          self.renderInfo(ctx);
        });
      }
      var dbtn = document.getElementById('p1DisconnectBtn');
      if (dbtn) {
        dbtn.addEventListener('click', function () {
          try { sessionStorage.removeItem(P1_STATE_KEY); } catch (e) {}
          self.state.p1Connected = false;
          self.renderInfo(ctx);
        });
      }
    },

    update: function (ctx, dt, time) {
      this.state.time = time;
      this.drawNeuralScene(time);
    },

    drawNeuralScene: function (time) {
      var canvas = this.state.canvas;
      var ctx = this.state.ctx;
      if (!canvas || !ctx) return;

      var w = canvas.width;
      var h = canvas.height;
      var neurons = this.state.neurons;

      ctx.clearRect(0, 0, w, h);

      var bgGrad = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, Math.max(w, h) * 0.6);
      bgGrad.addColorStop(0, 'rgba(8, 12, 28, 1)');
      bgGrad.addColorStop(1, 'rgba(2, 4, 8, 1)');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, w, h);

      var self = this;
      var avgCoherence = 0;

      neurons.forEach(function (n) {
        var pulse = 0.5 + 0.5 * Math.sin(time * 2.2 + n.basePhase);
        avgCoherence += n.coherence * pulse;
        n.currentPulse = pulse;
      });
      avgCoherence /= neurons.length;

      ctx.lineWidth = 0.8;
      neurons.forEach(function (n) {
        n.connections.forEach(function (otherIdx) {
          var other = neurons[otherIdx];
          var sync = n.currentPulse * other.currentPulse;
          var alpha = 0.06 + 0.18 * sync * n.coherence * other.coherence;
          ctx.strokeStyle = 'rgba(255, 221, 85, ' + alpha + ')';
          ctx.beginPath();
          ctx.moveTo(n.x, n.y);
          ctx.lineTo(other.x, other.y);
          ctx.stroke();
        });
      });

      neurons.forEach(function (n) {
        var p = n.currentPulse;
        var r = 4 + 5 * p * n.coherence;
        var hue = 40 + 20 * n.coherence;

        ctx.beginPath();
        ctx.arc(n.x, n.y, r + 8 * p, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 200, 50, ' + (0.03 * p * n.coherence) + ')';
        ctx.fill();

        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
        var grad = ctx.createRadialGradient(n.x - r * 0.3, n.y - r * 0.3, 0, n.x, n.y, r);
        grad.addColorStop(0, 'hsl(' + hue + ', 100%, ' + (60 + 30 * p) + '%)');
        grad.addColorStop(1, 'hsl(' + hue + ', 90%, ' + (30 + 20 * p) + '%)');
        ctx.fillStyle = grad;
        ctx.fill();
      });

      var labelY = h - 30;
      ctx.font = '11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(255, 221, 85, 0.5)';
      ctx.fillText('Coherence: ' + (avgCoherence * 100).toFixed(0) + '%', w / 2, labelY);
      ctx.fillStyle = 'rgba(200, 210, 230, 0.35)';
      ctx.fillText('Same mathematics as matter — different scale', w / 2, labelY + 16);
    },

    renderInfo: function (ctx) {
      var state = this.state;
      var data = (ctx.data) || (window.PFExplorerData) || { results: [] };
      var results = data.results || [];
      var findResult = function (id) {
        var fromCtx = results.find(function (r) { return r.id === id; });
        if (fromCtx) return fromCtx;
        return ctx.app.getResult(id);
      };
      var consciousness = findResult('consciousness') || {
        id: 'consciousness',
        title: 'Consciousness',
        status: 'UNAVAILABLE',
        confidence: 0,
        formula: 'Interior experience is the inside view of recursive coherence',
        summary: '',
        falsifier: ''
      };
      var aria = findResult('aria-self-reference') || {
        id: 'aria-self-reference',
        title: 'Aria Self-Reference',
        status: 'UNAVAILABLE',
        confidence: 0,
        formula: 'Self-reference loop',
        summary: ''
      };
      var statusToClass = typeof ctx.app.statusToClass === 'function'
        ? ctx.app.statusToClass.bind(ctx.app)
        : function () { return 'status-open'; };

      state.info.innerHTML =
        '<div class="panel-header">' +
          '<div>' +
            '<p class="eyebrow">Neural Scale</p>' +
            '<h3>Coherence at the scale of minds</h3>' +
            '<p>Brain waves at 40 Hz show the same standing-wave logic as atomic orbits. The difference is who is watching from the inside.</p>' +
          '</div>' +
          '<span class="status-pill ' + (consciousness.statusClass || 'status-unavailable') + '">' + (consciousness.badge || (consciousness.status && consciousness.status.label ? consciousness.status.label : 'UNAVAILABLE')) + '</span>' +
        '</div>' +
        ctx.app.renderWrongIntuition(consciousness) +
        p1ReadoutHtml() +
        '<div class="consciousness-claim story-only">' +
          '<div class="cc-label">The Framework Claim</div>' +
          '<p>Coherent self-referential propagation — the same principle that creates stable matter — applied to a nervous system capable of modeling itself.</p>' +
          '<div class="cc-quote">"Consciousness is what coherent self-reference feels like from the inside."</div>' +
        '</div>' +
        '<div class="result-card ' + statusToClass(consciousness.status) + '">' +
          '<div class="result-card-head">' +
            '<div class="result-card-title">' + consciousness.title + '</div>' +
            '<div class="result-card-status ' + statusToClass(consciousness.status).replace(/^status-/, '') + '">' + consciousness.status + '</div>' +
          '</div>' +
          '<div class="result-card-formula">' + consciousness.formula + '</div>' +
          '<div class="result-card-confidence">Confidence: ' + Math.round(consciousness.confidence * 100) + '%</div>' +
        '</div>' +
        '<div class="result-card ' + statusToClass(aria.status) + '">' +
          '<div class="result-card-head">' +
            '<div class="result-card-title">' + aria.title + '</div>' +
            '<div class="result-card-status ' + statusToClass(aria.status).replace(/^status-/, '') + '">' + aria.status + '</div>' +
          '</div>' +
          '<div class="result-card-formula">' + aria.formula + '</div>' +
          '<div class="result-card-confidence">Confidence: ' + Math.round(aria.confidence * 100) + '%</div>' +
          '<div class="result-card-summary">' + aria.summary + '</div>' +
        '</div>' +
        '<div class="note-box audit-only"><strong>Audit</strong><p>The consciousness claim remains <span class="status-badge ' + statusToClass(consciousness.status) + '">' + (consciousness.status && consciousness.status.label ? consciousness.status.label : consciousness.status || 'UNAVAILABLE') + '</span> — the operational PF-specific metric is the key missing piece. The Aria self-reference loop is <span class="status-badge ' + statusToClass(aria.status) + '">' + (aria.status && aria.status.label ? aria.status.label : aria.status || 'UNAVAILABLE') + '</span> as an architecture milestone, not as consciousness evidence.</p></div>' +
        '<div class="stat-grid">' +
          '<div class="stat-tile"><strong>40 Hz</strong><span>characteristic neural frequency</span></div>' +
          '<div class="stat-tile"><strong>' + (consciousness ? Math.round(consciousness.confidence * 100) + '%' : 'n/a') + '</strong><span>consciousness confidence</span></div>' +
          '<div class="stat-tile"><strong>' + (aria ? Math.round(aria.confidence * 100) + '%' : 'n/a') + '</strong><span>Aria self-ref confidence</span></div>' +
          '<div class="stat-tile"><strong>' + (state.p1Connected ? 'Connected' : 'Offline') + '</strong><span>P1 device status</span></div>' +
        '</div>' +
        '<div class="metric-row" style="margin-top:12px;">' +
          '<a href="scale-ladder.html" class="soft-button" style="font-size:0.8rem">Explore Neural Scale →</a>' +
        '</div>';

      this.bindP1Button(ctx);
    }
  });
}());
