/**
 * Koide/Weinberg Bridge Panel — RG Running Visualization
 * 
 * Shows why the proximity between δ_Koide ≈ 2/9 and sin²θ_W ≈ 0.223
 * is striking but not connected via RG running.
 * 
 * T-021 and T-022 results: negative on both Casimir scan and RG crossing.
 * This is honest physics — the gap remains open.
 */
(function () {
  'use strict';

  // Physical constants
  var KOIDE_PHASE = 0.222229631490; // measured empirical value (rad treated as dimensionless here)
  var TWO_NINTHS = 2 / 9; // 0.222222...
  var WEINBERG_ON_SHELL = 0.22337; // PDG on-shell measured value
  var WEINBERG_MZ_MSBAR = 0.23153; // MS-bar value at M_Z (91.1876 GeV)
  
  // RG running parameters (MS-bar scheme, approximate)
  // sin²θ_W(μ) evolution based on Standard Model RG equations
  var MZ = 91.1876; // Z boson mass in GeV
  var ALPHA_EM_MZ = 1 / 127.9; // fine structure at M_Z
  var ALPHA_1_MZ = 0.0169; // g'^2/(4π) at M_Z
  var ALPHA_2_MZ = 0.0338; // g^2/(4π) at M_Z

  /**
   * Calculate sin²θ_W at scale μ using SM RG (MS-bar scheme)
   * Approximate formula: sin²θ_W(μ) = α_em(μ) / α_2(μ)
   * where α_em = (α_1 α_2) / (α_1 + (5/3)α_2) at low energy
   * 
   * Simplified approximation for visualization purposes:
   * Running is dominated by gauge coupling evolution
   */
  function weinbergRunning(mu) {
    // Logarithmic evolution from M_Z
    var t = Math.log(mu / MZ);
    
    // Approximate beta function contributions
    // b1 = 41/10, b2 = -19/6 for SM (roughly)
    // This gives the characteristic slow rise with energy
    var running = WEINBERG_MZ_MSBAR + 0.006 * t + 0.0005 * t * t;
    
    // At low energy, approach the on-shell value
    if (mu < MZ) {
      var lowFactor = Math.pow(mu / MZ, 0.15);
      running = WEINBERG_ON_SHELL + (WEINBERG_MZ_MSBAR - WEINBERG_ON_SHELL) * (1 - lowFactor);
    }
    
    return running;
  }

  function createCanvasPanel(state, ctx) {
    var container = document.createElement('div');
    container.style.cssText = 'position:absolute;inset:0;overflow:hidden;';
    state.canvas.parentElement.appendChild(container);

    var canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;';
    container.appendChild(canvas);
    state.runningCanvas = canvas;
    state.runningContainer = container;

    // Create tooltip
    var tooltip = document.createElement('div');
    tooltip.className = 'running-tooltip';
    tooltip.style.cssText = 'position:absolute;background:rgba(10,10,26,0.95);border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:10px 14px;font-size:12px;color:#fff;pointer-events:none;opacity:0;transition:opacity 0.15s;z-index:100;box-shadow:0 4px 20px rgba(0,0,0,0.5);';
    container.appendChild(tooltip);
    state.tooltip = tooltip;

    // Hover interaction
    canvas.addEventListener('mousemove', function(e) {
      var rect = canvas.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      handleHover(state, x, y, rect.width, rect.height);
    });

    canvas.addEventListener('mouseleave', function() {
      state.tooltip.style.opacity = '0';
    });

    resizeCanvas(state);
  }

  function resizeCanvas(state) {
    if (!state.runningCanvas) return;
    var dpr = window.devicePixelRatio || 1;
    var rect = state.runningContainer.getBoundingClientRect();
    state.runningCanvas.width = rect.width * dpr;
    state.runningCanvas.height = rect.height * dpr;
    state.canvasWidth = rect.width;
    state.canvasHeight = rect.height;
  }

  function getPlotArea(width, height) {
    var padding = { left: 70, right: 40, top: 50, bottom: 60 };
    return {
      left: padding.left,
      right: width - padding.right,
      top: padding.top,
      bottom: height - padding.bottom,
      width: width - padding.left - padding.right,
      height: height - padding.top - padding.bottom
    };
  }

  function energyScale(mu) {
    // Log scale: 1 GeV to 1000 GeV
    return Math.log10(mu);
  }

  function mapX(mu, plot) {
    var logMu = Math.log10(mu);
    var t = (logMu - 0) / 3; // 1 GeV = 10^0, 1000 GeV = 10^3
    return plot.left + t * plot.width;
  }

  function mapY(value, plot) {
    // Map 0.20 → 0.24 to plot area
    var t = (value - 0.20) / 0.04;
    return plot.bottom - t * plot.height;
  }

  function handleHover(state, x, y, width, height) {
    var plot = getPlotArea(width, height);
    
    // Check if in plot area
    if (x < plot.left || x > plot.right || y < plot.top || y > plot.bottom) {
      state.tooltip.style.opacity = '0';
      return;
    }

    // Calculate energy from x position
    var t = (x - plot.left) / plot.width;
    var logMu = t * 3; // 0 to 3
    var mu = Math.pow(10, logMu);

    // Calculate value from y position
    var valueT = (plot.bottom - y) / plot.height;
    var value = 0.20 + valueT * 0.04;

    // Determine what's closest
    var weinbergVal = weinbergRunning(mu);
    var koideDiff = Math.abs(value - KOIDE_PHASE);
    var twoNinthsDiff = Math.abs(value - TWO_NINTHS);
    var weinbergDiff = Math.abs(value - weinbergVal);

    var closest = 'weinberg';
    var minDiff = weinbergDiff;
    if (koideDiff < minDiff) { closest = 'koide'; minDiff = koideDiff; }
    if (twoNinthsDiff < minDiff) { closest = '2/9'; minDiff = twoNinthsDiff; }

    // Build tooltip content
    var html = '<div style="font-weight:600;margin-bottom:4px;color:#00cfff;">μ = ' + mu.toFixed(1) + ' GeV</div>';
    
    if (closest === 'weinberg') {
      html += '<div>sin²θ_W(μ) = <span style="color:#ffdd55;font-weight:600;">' + weinbergVal.toFixed(5) + '</span></div>';
      html += '<div style="font-size:10px;color:rgba(255,255,255,0.6);margin-top:4px;">MS-bar scheme running</div>';
    } else if (closest === 'koide') {
      html += '<div>δ_Koide = <span style="color:#69ff94;font-weight:600;">' + KOIDE_PHASE.toFixed(9) + '</span></div>';
      html += '<div style="font-size:10px;color:rgba(255,255,255,0.6);margin-top:4px;">Constant (no running)</div>';
    } else {
      html += '<div>2/9 = <span style="color:#ff6688;font-weight:600;">' + TWO_NINTHS.toFixed(9) + '</span></div>';
      html += '<div style="font-size:10px;color:rgba(255,255,255,0.6);margin-top:4px;">Mathematical attractor</div>';
    }

    state.tooltip.innerHTML = html;
    state.tooltip.style.left = Math.min(x + 15, width - 180) + 'px';
    state.tooltip.style.top = Math.max(y - 60, 10) + 'px';
    state.tooltip.style.opacity = '1';
  }

  function drawRunningPlot(state, ctx) {
    if (!state.runningCanvas) return;

    var canvas = state.runningCanvas;
    var dpr = window.devicePixelRatio || 1;
    var draw = canvas.getContext('2d');

    var width = state.canvasWidth;
    var height = state.canvasHeight;
    var plot = getPlotArea(width, height);

    draw.save();
    draw.scale(dpr, dpr);
    draw.clearRect(0, 0, width, height);

    // Background grid
    draw.strokeStyle = 'rgba(255,255,255,0.06)';
    draw.lineWidth = 1;

    // Horizontal grid lines (value)
    for (var val = 0.20; val <= 0.24; val += 0.005) {
      var y = mapY(val, plot);
      draw.beginPath();
      draw.moveTo(plot.left, y);
      draw.lineTo(plot.right, y);
      draw.stroke();
    }

    // Vertical grid lines (energy)
    for (var logE = 0; logE <= 3; logE += 0.5) {
      var x = mapX(Math.pow(10, logE), plot);
      draw.beginPath();
      draw.moveTo(x, plot.top);
      draw.lineTo(x, plot.bottom);
      draw.stroke();
    }

    // Plot area border
    draw.strokeStyle = 'rgba(255,255,255,0.25)';
    draw.lineWidth = 1.5;
    draw.strokeRect(plot.left, plot.top, plot.width, plot.height);

    // Axes labels
    draw.fillStyle = 'rgba(255,255,255,0.7)';
    draw.font = '12px Trebuchet MS, sans-serif';
    draw.textAlign = 'center';

    // X-axis labels (energy)
    var energyLabels = [1, 10, 100, 1000];
    energyLabels.forEach(function(e) {
      var x = mapX(e, plot);
      draw.fillText(e + ' GeV', x, plot.bottom + 20);
    });

    // X-axis title
    draw.fillText('Energy Scale μ (GeV)', plot.left + plot.width / 2, height - 12);

    // Y-axis labels (value)
    draw.textAlign = 'right';
    for (var v = 0.20; v <= 0.24; v += 0.01) {
      var y = mapY(v, plot);
      draw.fillText(v.toFixed(2), plot.left - 10, y + 4);
    }

    // Y-axis title
    draw.save();
    draw.translate(20, plot.top + plot.height / 2);
    draw.rotate(-Math.PI / 2);
    draw.textAlign = 'center';
    draw.fillText('Value', 0, 0);
    draw.restore();

    // Draw 2/9 reference line (dotted, pink/red)
    draw.strokeStyle = '#ff6688';
    draw.lineWidth = 2;
    draw.setLineDash([4, 4]);
    draw.beginPath();
    var y2_9 = mapY(TWO_NINTHS, plot);
    draw.moveTo(plot.left, y2_9);
    draw.lineTo(plot.right, y2_9);
    draw.stroke();
    draw.setLineDash([]);

    // 2/9 label
    draw.fillStyle = '#ff6688';
    draw.font = 'bold 13px Trebuchet MS, sans-serif';
    draw.textAlign = 'left';
    draw.fillText('2/9 = 0.222222...', plot.right + 8, y2_9 + 4);

    // Draw Koide phase line (dashed, green)
    draw.strokeStyle = '#69ff94';
    draw.lineWidth = 2.5;
    draw.setLineDash([8, 4]);
    draw.beginPath();
    var yKoide = mapY(KOIDE_PHASE, plot);
    draw.moveTo(plot.left, yKoide);
    draw.lineTo(plot.right, yKoide);
    draw.stroke();
    draw.setLineDash([]);

    // Koide label
    draw.fillStyle = '#69ff94';
    draw.font = 'bold 13px Trebuchet MS, sans-serif';
    draw.fillText('δ_Koide = 0.2222296...', plot.right + 8, yKoide + 4);

    // Draw Weinberg running curve (solid, yellow)
    draw.strokeStyle = '#ffdd55';
    draw.lineWidth = 3;
    draw.beginPath();
    var steps = 200;
    for (var i = 0; i <= steps; i++) {
      var logMu = 3 * i / steps;
      var mu = Math.pow(10, logMu);
      var sw = weinbergRunning(mu);
      var x = mapX(mu, plot);
      var y = mapY(sw, plot);
      if (i === 0) {
        draw.moveTo(x, y);
      } else {
        draw.lineTo(x, y);
      }
    }
    draw.stroke();

    // Mark key points on Weinberg curve
    var keyEnergies = [1, MZ, 1000];
    keyEnergies.forEach(function(e) {
      var sw = weinbergRunning(e);
      var x = mapX(e, plot);
      var y = mapY(sw, plot);
      
      draw.fillStyle = '#ffdd55';
      draw.beginPath();
      draw.arc(x, y, 5, 0, Math.PI * 2);
      draw.fill();
      
      draw.strokeStyle = '#0a0a1a';
      draw.lineWidth = 2;
      draw.stroke();
    });

    // Weinberg labels
    draw.fillStyle = '#ffdd55';
    draw.font = 'bold 13px Trebuchet MS, sans-serif';
    var yWeinbergMZ = mapY(WEINBERG_MZ_MSBAR, plot);
    draw.fillText('sin²θ_W(μ) MS-bar', plot.right + 8, yWeinbergMZ - 8);

    // Gap annotation
    var yGap = (yKoide + yWeinbergMZ) / 2;
    draw.fillStyle = 'rgba(255,255,255,0.5)';
    draw.font = '11px Trebuchet MS, sans-serif';
    draw.fillText('gap ~0.001', plot.left + plot.width * 0.7, yGap);

    // Draw double-headed arrow showing the gap
    var arrowX = plot.left + plot.width * 0.75;
    draw.strokeStyle = 'rgba(255,255,255,0.4)';
    draw.lineWidth = 1;
    draw.setLineDash([2, 2]);
    draw.beginPath();
    draw.moveTo(arrowX, yKoide);
    draw.lineTo(arrowX, yWeinbergMZ);
    draw.stroke();
    draw.setLineDash([]);

    // Arrow heads
    draw.fillStyle = 'rgba(255,255,255,0.5)';
    draw.beginPath();
    draw.moveTo(arrowX - 3, yKoide + 5);
    draw.lineTo(arrowX, yKoide);
    draw.lineTo(arrowX + 3, yKoide + 5);
    draw.fill();
    
    draw.beginPath();
    draw.moveTo(arrowX - 3, yWeinbergMZ - 5);
    draw.lineTo(arrowX, yWeinbergMZ);
    draw.lineTo(arrowX + 3, yWeinbergMZ - 5);
    draw.fill();

    draw.restore();
  }

  // Panel registration
  window.PFExplorer.registerPanel({
    id: 'koide-weinberg-bridge',
    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="panel-wrap">' +
          '<div class="panel-atlas">' +
            '<section class="canvas-panel" style="position:relative">' +
              '<div class="panel-header">' +
                '<div>' +
                  '<p class="eyebrow"><span style="color:#ff4455; font-family:serif; margin-right:8px;">✕</span> RG Running Analysis</p>' +
                  '<h3><span style="color:#00cfff; font-family:serif; margin-right:8px;">⟁</span> Close but not connected.</h3>' +
                  '<p>The Koide phase δ ≈ 2/9 and Weinberg angle sin²θ_W ≈ 0.223 sit tantalizingly close. T-021 and T-022 investigated whether RG running bridges them — both came back negative.</p>' +
                  '<p class="interaction-cue"><strong>Interaction:</strong> Review the results of T-021 and T-022 below. Notice how the gap remains distinct even at high energy scales.</p>' +
                '</div>' +
              '</div>' +
              '<canvas class="panel-canvas" id="bridgeCanvas" style="position:absolute;inset:0;width:100%;height:100%"></canvas>' +
              '<div class="canvas-overlay"></div>' +
            '</section>' +
            '<section class="info-panel" id="bridgeInfo"></section>' +
          '</div>' +
        '</div>';

      this.state = {
        canvas: ctx.stage.querySelector('#bridgeCanvas'),
        info: ctx.stage.querySelector('#bridgeInfo')
      };

      createCanvasPanel(this.state, ctx);
      this.renderInfo(ctx);
    },

    unmount: function () {
      if (this.state.runningContainer) {
        this.state.runningContainer.remove();
      }
      this.state = null;
    },

    resize: function () {
      resizeCanvas(this.state);
    },

    renderInfo: function (ctx) {
      var state = this.state;
      var gap = WEINBERG_ON_SHELL - KOIDE_PHASE;
      var gapFrom2_9 = KOIDE_PHASE - TWO_NINTHS;
      var phaseResult = ctx.app.getResult('koide-phase') || {};

      state.info.innerHTML =
        '<div class="panel-header">' +
          '<div>' +
            '<p class="eyebrow">T-021 / T-022 Results</p>' +
            '<h3>The proximity is striking, but RG running doesn\'t bridge them.</h3>' +
            '<p>Both investigations returned negative. The gap remains: δ_Koide = 0.22223, sin²θ_W = 0.22337. Close enough to notice, far enough to matter.</p>' +
          '</div>' +
          '<span class="status-pill ' + (phaseResult.statusClass || 'status-empirical') + '">' + (phaseResult.badge || (phaseResult.status && phaseResult.status.label ? phaseResult.status.label : 'EMPIRICAL')) + '</span>' +
        '</div>' +
        '<div class="formula" style="font-size:13px;margin-bottom:16px;">' +
          'δ_Koide = ' + KOIDE_PHASE.toFixed(9) + '<br>' +
          '2/9 = ' + TWO_NINTHS.toFixed(9) + '<br>' +
          'sin²θ_W(on-shell) = ' + WEINBERG_ON_SHELL.toFixed(5) +
        '</div>' +
        PFExplorer.compareBarHtml(KOIDE_PHASE, WEINBERG_ON_SHELL, Math.abs(gap) / 0.00013, 0.221, 0.225) +
        '<div class="metric-row">' +
          '<span class="metric-pill">gap = ' + (gap * 1000).toFixed(2) + '×10⁻³</span>' +
          '<span class="metric-pill">δ − 2/9 = ' + (gapFrom2_9 * 1e6).toFixed(1) + ' ppm</span>' +
        '</div>' +
        '<div class="stat-grid" style="margin-top:16px;">' +
          '<div class="stat-tile"><strong style="color:#69ff94;">' + KOIDE_PHASE.toFixed(7) + '</strong><span>Koide phase (empirical)</span></div>' +
          '<div class="stat-tile"><strong style="color:#ff6688;">' + TWO_NINTHS.toFixed(7) + '</strong><span>2/9 attractor</span></div>' +
          '<div class="stat-tile"><strong style="color:#ffdd55;">' + WEINBERG_ON_SHELL.toFixed(5) + '</strong><span>Weinberg on-shell</span></div>' +
          '<div class="stat-tile"><strong>' + WEINBERG_MZ_MSBAR.toFixed(5) + '</strong><span>Weinberg MS-bar @ M_Z</span></div>' +
        '</div>' +
        '<div class="note-box story-only" style="margin-top:16px;">' +
          '<strong>Story</strong>' +
          '<p>Two numbers, both near 2/9. One from lepton mass geometry, one from electroweak mixing. Close enough to make you wonder. Tested and found not connected by RG running. The universe is not required to give us simple explanations — but it is required to be honest when we check.</p>' +
        '</div>' +
        '<div class="note-box audit-only" style="margin-top:12px;">' +
          '<strong>Audit</strong>' +
          '<p>T-021: RG running audit — negative result. The curves do not cross in the accessible energy range.<br>' +
          'T-022: Casimir scan for phase selector — negative result. No PF-native mechanism found for δ = 2/9.<br>' +
          'Status: The proximity remains an open empirical signal, not a derived connection.</p>' +
        '</div>' +
        '<div style="margin-top:16px;padding:12px;background:rgba(0,207,255,0.08);border-radius:8px;border-left:3px solid #00cfff;">' +
          '<p style="margin:0;font-size:12px;color:rgba(255,255,255,0.8);">' +
            '<strong>Interactive:</strong> Hover over the plot to see exact values at any energy scale. The yellow curve shows MS-bar scheme running — it rises with energy, moving away from the Koide phase, not toward it.' +
          '</p>' +
        '</div>';

      ctx.app.syncActiveResultCards();
    },

    update: function (ctx) {
      drawRunningPlot(this.state, ctx);
    }
  });
}());
