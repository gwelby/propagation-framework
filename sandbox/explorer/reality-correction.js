/**
 * Reality Correction Panel — Three Wrong-Intuition Comparisons
 *
 * Shows three core PF confrontations:
 * 1. Gravity pull vs. light bending (refraction)
 * 2. Matter particles vs. standing waves
 * 3. Generation count: N=2 fails, N=4 fails, N=3 works
 *
 * Each comparison: wrong intuition struck through → reality in green
 * → interactive element → link to live panel
 *
 * Dual-context: works in Explorer shell (panel registration) AND
 * standalone Journey mode (PFRealityVisuals export).
 */
(function () {
  'use strict';

  // ═══════════════════════════════════════════════════════════════
  // UTILITIES
  // ═══════════════════════════════════════════════════════════════

  function getCanvasBox(canvas, fallbackHeight) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var cssWidth = canvas.clientWidth || parseFloat(canvas.getAttribute('width')) || 300;
    var cssHeight = canvas.clientHeight || parseFloat(canvas.getAttribute('height')) || fallbackHeight || 120;
    canvas.width = Math.max(1, Math.round(cssWidth * dpr));
    canvas.height = Math.max(1, Math.round(cssHeight * dpr));
    return { dpr: dpr, width: cssWidth, height: cssHeight };
  }

  function lerp(a, b, t) { return a + (b - a) * t; }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  function easeInOut(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  // ═══════════════════════════════════════════════════════════════
  // 1. GRAVITY REFRACTION — Animated light rays through density gradient
  // ═══════════════════════════════════════════════════════════════

  var _gravityAnimState = null;

  function drawGravityRefraction(canvas, opts) {
    if (!canvas) return;
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var box = getCanvasBox(canvas, 140);
    var cw = box.width, ch = box.height;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(box.dpr, box.dpr);
    ctx.clearRect(0, 0, cw, ch);

    var cx = cw / 2, cy = ch / 2;
    var time = opts.time || 0;
    var showWrong = opts.showWrong !== false;

    // ── Density gradient (medium gets denser toward massive object) ──
    var starX = cx, starY = cy + ch * 0.15;
    var grad = ctx.createRadialGradient(starX, starY, 0, starX, starY, cw * 0.6);
    grad.addColorStop(0, 'rgba(0, 48, 96, 0.30)');
    grad.addColorStop(0.4, 'rgba(0, 32, 64, 0.12)');
    grad.addColorStop(1, 'rgba(0, 16, 32, 0.0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, cw, ch);

    // ── Refractive index contour lines (concentric rings) ──
    for (var ring = 1; ring <= 4; ring++) {
      var ringR = ring * cw * 0.12;
      ctx.beginPath();
      ctx.arc(starX, starY, ringR, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(0, 207, 255, ' + (0.08 - ring * 0.015) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // ── Massive object (star) ──
    var starR = Math.min(16, cw * 0.04);
    var starGrad = ctx.createRadialGradient(starX, starY, 0, starX, starY, starR * 3);
    starGrad.addColorStop(0, 'rgba(255, 215, 0, 0.8)');
    starGrad.addColorStop(0.3, 'rgba(255, 179, 71, 0.25)');
    starGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = starGrad;
    ctx.beginPath();
    ctx.arc(starX, starY, starR * 3, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(starX, starY, starR, 0, Math.PI * 2);
    ctx.fillStyle = '#ffd700';
    ctx.fill();
    ctx.shadowColor = '#ffd700';
    ctx.shadowBlur = 8;
    ctx.fill();
    ctx.shadowBlur = 0;

    // ── Animated light rays (multiple parallel rays bending) ──
    var numRays = 5;
    var raySpacing = ch * 0.06;
    var rayStartX = cw * 0.05;

    for (var ri = 0; ri < numRays; ri++) {
      var impactParam = (ri - (numRays - 1) / 2) * raySpacing;
      var rayStartY = starY + impactParam;
      var bendAmount = 1.0 / (1.0 + Math.abs(impactParam) / (starR * 2));
      var rayAlpha = 0.3 + 0.7 * bendAmount;

      // Incoming ray (straight)
      var hitX = starX - starR * 1.5;
      var hitY = rayStartY;

      ctx.beginPath();
      ctx.moveTo(rayStartX, rayStartY);
      ctx.lineTo(hitX, hitY);
      ctx.strokeStyle = 'rgba(255, 221, 85, ' + rayAlpha + ')';
      ctx.lineWidth = 1.5 + bendAmount;
      ctx.stroke();

      // Refracted ray (bent toward mass)
      var bendAngle = bendAmount * 0.35;
      var rayLen = cw * 0.45;
      var endX = hitX + rayLen;
      var endY = hitY + rayLen * Math.sin(bendAngle) * (impactParam >= 0 ? 1 : -1);

      // Curved path through medium
      ctx.beginPath();
      ctx.moveTo(hitX, hitY);
      var cpX = (hitX + endX) / 2;
      var cpY = (hitY + endY) / 2 + bendAmount * ch * 0.04 * (impactParam >= 0 ? 1 : -1);
      ctx.quadraticCurveTo(cpX, cpY, endX, endY);
      ctx.strokeStyle = 'rgba(0, 207, 255, ' + rayAlpha + ')';
      ctx.lineWidth = 1.5 + bendAmount;
      ctx.stroke();

      // Animated photon dot along the ray
      var photonT = ((time * 0.3 + ri * 0.2) % 1.0);
      var photonX, photonY;
      if (photonT < 0.4) {
        var t = photonT / 0.4;
        photonX = lerp(rayStartX, hitX, t);
        photonY = lerp(rayStartY, hitY, t);
      } else {
        var t = (photonT - 0.4) / 0.6;
        var mt = 1 - t;
        photonX = mt * mt * hitX + 2 * mt * t * cpX + t * t * endX;
        photonY = mt * mt * hitY + 2 * mt * t * cpY + t * t * endY;
      }
      ctx.beginPath();
      ctx.arc(photonX, photonY, 2 + bendAmount, 0, Math.PI * 2);
      ctx.fillStyle = bendAmount > 0.5 ? 'rgba(0, 207, 255, 0.9)' : 'rgba(255, 221, 85, 0.7)';
      ctx.fill();
    }

    // ── Normal line at closest approach ──
    ctx.beginPath();
    ctx.setLineDash([3, 3]);
    ctx.moveTo(starX, starY - ch * 0.35);
    ctx.lineTo(starX, starY + ch * 0.35);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.10)';
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.setLineDash([]);

    // ── Labels ──
    ctx.font = '10px "DM Sans", sans-serif';
    ctx.textAlign = 'left';

    // "vacuum" label
    ctx.fillStyle = 'rgba(139, 163, 189, 0.5)';
    ctx.fillText('vacuum (n ≈ 1)', 8, 14);

    // "medium" label
    ctx.fillText('medium (n > 1 near mass)', 8, ch - 8);

    // ── Wrong intuition label ──
    if (showWrong) {
      ctx.fillStyle = 'rgba(255, 71, 87, 0.55)';
      ctx.font = '9px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('✗ "gravity pulls" — no, propagation bends', cw * 0.5, ch - 22);
    }
  }

  // ── Gravity animation loop (for standalone Journey mode) ──

  function startGravityAnimation(canvas) {
    if (!canvas) return;
    if (_gravityAnimState && _gravityAnimState.canvas === canvas) return;
    stopGravityAnimation();
    _gravityAnimState = { canvas: canvas, running: true };
    var startTime = performance.now();
    function frame() {
      if (!_gravityAnimState || !_gravityAnimState.running) return;
      var t = (performance.now() - startTime) / 1000;
      drawGravityRefraction(canvas, { time: t });
      _gravityAnimState.frameId = requestAnimationFrame(frame);
    }
    _gravityAnimState.frameId = requestAnimationFrame(frame);
  }

  function stopGravityAnimation() {
    if (_gravityAnimState && _gravityAnimState.frameId) {
      cancelAnimationFrame(_gravityAnimState.frameId);
    }
    _gravityAnimState = null;
  }

  // ═══════════════════════════════════════════════════════════════
  // 2. PARTICLE vs STANDING WAVE — Animated with envelope + nodes
  // ═══════════════════════════════════════════════════════════════

  function drawParticleVsWave(canvas, opts) {
    if (!canvas) return;
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var box = getCanvasBox(canvas, 120);
    var cw = box.width, ch = box.height;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(box.dpr, box.dpr);
    ctx.clearRect(0, 0, cw, ch);

    var t = opts.time !== undefined ? opts.time : (performance.now() / 1000);
    var midY = ch * 0.50;
    var amp = ch * 0.22;
    var numWaves = 4; // number of half-wavelengths

    // ── Envelope (dashed boundary) ──
    ctx.beginPath();
    for (var xi = 0; xi <= cw; xi += 1) {
      var xEnv = xi / cw * Math.PI * numWaves;
      var yEnv = midY - Math.sin(xEnv) * amp;
      if (xi === 0) ctx.moveTo(xi, yEnv);
      else ctx.lineTo(xi, yEnv);
    }
    ctx.strokeStyle = 'rgba(105, 255, 148, 0.15)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.stroke();
    ctx.setLineDash([]);

    // Bottom envelope
    ctx.beginPath();
    for (var xi = 0; xi <= cw; xi += 1) {
      var xEnv = xi / cw * Math.PI * numWaves;
      var yEnv = midY + Math.sin(xEnv) * amp;
      if (xi === 0) ctx.moveTo(xi, yEnv);
      else ctx.lineTo(xi, yEnv);
    }
    ctx.strokeStyle = 'rgba(105, 255, 148, 0.15)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.stroke();
    ctx.setLineDash([]);

    // ── Standing wave: sin(kx) * cos(ωt) ──
    ctx.beginPath();
    for (var xi = 0; xi <= cw; xi += 1) {
      var x = xi / cw * Math.PI * numWaves;
      var y = midY - Math.sin(x) * Math.cos(t * 1.5) * amp;
      if (xi === 0) ctx.moveTo(xi, y);
      else ctx.lineTo(xi, y);
    }
    ctx.strokeStyle = 'rgba(105, 255, 148, 0.9)';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = 'rgba(105, 255, 148, 0.4)';
    ctx.shadowBlur = 6;
    ctx.stroke();
    ctx.shadowBlur = 0;

    // ── Node markers (fixed points where wave always crosses zero) ──
    for (var n = 0; n <= numWaves; n++) {
      var nx = (n / numWaves) * cw;
      // Pulsing node glow
      var nodeGlow = 0.5 + 0.5 * Math.sin(t * 2 + n);
      ctx.beginPath();
      ctx.arc(nx, midY, 3 + nodeGlow * 2, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(105, 255, 148, ' + (0.4 + nodeGlow * 0.3) + ')';
      ctx.fill();
    }

    // ── Wavelength marker ──
    var lambdaStart = 0;
    var lambdaEnd = (2 / numWaves) * cw;
    ctx.beginPath();
    ctx.moveTo(lambdaStart, midY + amp + 14);
    ctx.lineTo(lambdaEnd, midY + amp + 14);
    ctx.strokeStyle = 'rgba(255, 221, 85, 0.5)';
    ctx.lineWidth = 1;
    ctx.stroke();
    // Arrow heads
    ctx.beginPath();
    ctx.moveTo(lambdaStart, midY + amp + 11);
    ctx.lineTo(lambdaStart, midY + amp + 17);
    ctx.moveTo(lambdaEnd, midY + amp + 11);
    ctx.lineTo(lambdaEnd, midY + amp + 17);
    ctx.stroke();
    ctx.fillStyle = 'rgba(255, 221, 85, 0.6)';
    ctx.font = '9px "DM Sans", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('λ', (lambdaStart + lambdaEnd) / 2, midY + amp + 26);

    // ── Labels ──
    ctx.fillStyle = '#69ff94';
    ctx.font = 'bold 10px "DM Sans", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('standing wave — stable nodes at λ/2', cw / 2, 14);

    ctx.fillStyle = 'rgba(139, 163, 189, 0.7)';
    ctx.font = '9px "DM Sans", sans-serif';
    ctx.fillText('This is what matter IS: self-reinforcing propagation', cw / 2, ch - 6);

    // ── Particle ghost (faint, struck through) ──
    var ghostX = cw * 0.28;
    var ghostY = midY - amp * 0.5;
    ctx.globalAlpha = 0.15 + 0.05 * Math.sin(t * 0.8);
    ctx.beginPath();
    ctx.arc(ghostX, ghostY, 7, 0, Math.PI * 2);
    ctx.fillStyle = '#ff6b9d';
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(ghostX - 10, ghostY - 10);
    ctx.lineTo(ghostX + 10, ghostY + 10);
    ctx.strokeStyle = '#ff4757';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.globalAlpha = 1;

    ctx.fillStyle = 'rgba(255, 107, 157, 0.4)';
    ctx.font = '8px "DM Sans", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('"particle"', ghostX, ghostY + 20);
  }

  // ═══════════════════════════════════════════════════════════════
  // 3. GENERATION TOPOLOGY — Animated with transitions
  // ═══════════════════════════════════════════════════════════════

  var _topologyAnimState = null;

  function drawTopologyDiagram(canvas, n, selected, opts) {
    if (!canvas) return;
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var box = getCanvasBox(canvas, 140);
    var cw = box.width, ch = box.height;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(box.dpr, box.dpr);
    ctx.clearRect(0, 0, cw, ch);

    var cx = cw / 2, cy = ch / 2;
    var r = Math.min(cw, ch) * 0.28;
    var time = opts.time || 0;
    var transitionT = opts.transitionT !== undefined ? opts.transitionT : 1; // 0→1 animation progress
    var prevN = opts.prevN !== undefined ? opts.prevN : n;

    // Smooth transition between N values
    var currentN = transitionT >= 1 ? n : (transitionT <= 0 ? prevN : n);
    var easedT = easeInOut(clamp(transitionT, 0, 1));

    // ── Background glow ──
    var glowColor;
    if (n === 3) glowColor = 'rgba(105, 255, 148, 0.04)';
    else if (n === 2) glowColor = 'rgba(0, 207, 255, 0.03)';
    else if (n === 4) glowColor = 'rgba(255, 107, 157, 0.03)';
    else glowColor = 'rgba(200, 168, 255, 0.03)';

    ctx.beginPath();
    ctx.arc(cx, cy, r * 2, 0, Math.PI * 2);
    ctx.fillStyle = glowColor;
    ctx.fill();

    // ── N=1: Trivial ──
    if (currentN === 1) {
      var pulse = 0.8 + 0.2 * Math.sin(time * 2);
      ctx.beginPath();
      ctx.arc(cx, cy, 8 * pulse, 0, Math.PI * 2);
      ctx.fillStyle = '#c8a8ff';
      ctx.shadowColor = '#c8a8ff';
      ctx.shadowBlur = 10;
      ctx.fill();
      ctx.shadowBlur = 0;

      ctx.fillStyle = '#8ba3bd';
      ctx.font = '11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=1: trivial — no structure', cx, cy + 24);
      ctx.fillStyle = 'rgba(255, 71, 87, 0.5)';
      ctx.fillText('Cannot produce 3 generations', cx, cy + 38);
      return;
    }

    // ── N=2: ℤ₂ — Only two classes ──
    if (currentN === 2) {
      var a0 = -Math.PI / 2;
      var a1 = Math.PI / 2;
      var p0x = cx + r * Math.cos(a0), p0y = cy + r * Math.sin(a0);
      var p1x = cx + r * Math.cos(a1), p1y = cy + r * Math.sin(a1);

      // Connection line (pulsing)
      var linePulse = 0.5 + 0.3 * Math.sin(time * 1.5);
      ctx.beginPath();
      ctx.moveTo(p0x, p0y);
      ctx.lineTo(p1x, p1y);
      ctx.strokeStyle = 'rgba(0, 207, 255, ' + linePulse + ')';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Vertices
      [p0x, p1x].forEach(function (px, i) {
        var py = [p0y, p1y][i];
        var isActive = selected === i || selected === 2;
        ctx.beginPath();
        ctx.arc(px, py, isActive ? 10 : 8, 0, Math.PI * 2);
        ctx.fillStyle = isActive ? '#00e5ff' : '#334466';
        ctx.fill();
        if (isActive) {
          ctx.strokeStyle = '#00e5ff';
          ctx.lineWidth = 1.5;
          ctx.shadowColor = '#00e5ff';
          ctx.shadowBlur = 8;
          ctx.stroke();
          ctx.shadowBlur = 0;
        }
      });

      // Labels
      ctx.fillStyle = '#8ba3bd';
      ctx.font = '11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=2: ℤ₂ topology only', cx, cy + 24);
      ctx.fillStyle = '#ff6b9d';
      ctx.font = 'bold 10px "DM Sans", sans-serif';
      ctx.fillText('✗ Only 2 channels — cannot form Koide triangle', cx, cy + 40);
      return;
    }

    // ── N=3: LOCKED — Three generations at 120° ──
    if (currentN === 3) {
      var angles = [-Math.PI / 2, -Math.PI / 2 + 2 * Math.PI / 3, -Math.PI / 2 + 4 * Math.PI / 3];
      var pts = angles.map(function (a) {
        return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) };
      });

      // Triangle fill (subtle)
      ctx.beginPath();
      ctx.moveTo(pts[0].x, pts[0].y);
      ctx.lineTo(pts[1].x, pts[1].y);
      ctx.lineTo(pts[2].x, pts[2].y);
      ctx.closePath();
      ctx.fillStyle = 'rgba(105, 255, 148, 0.04)';
      ctx.fill();

      // Triangle edges (glowing)
      var edgePulse = 0.6 + 0.2 * Math.sin(time * 1.2);
      ctx.strokeStyle = 'rgba(105, 255, 148, ' + edgePulse + ')';
      ctx.lineWidth = 2;
      ctx.shadowColor = 'rgba(105, 255, 148, 0.3)';
      ctx.shadowBlur = 6;
      ctx.stroke();
      ctx.shadowBlur = 0;

      // 120° angle arc
      ctx.beginPath();
      ctx.arc(pts[0].x, pts[0].y, 16, Math.PI * 0.17, Math.PI * 0.83);
      ctx.strokeStyle = 'rgba(255, 221, 85, 0.4)';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = 'rgba(255, 221, 85, 0.5)';
      ctx.font = '8px "DM Sans", sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('120°', pts[0].x + 18, pts[0].y + 3);

      // Vertices with labels
      var labels = ['e', 'μ', 'τ'];
      var masses = ['0.511 MeV', '105.7 MeV', '1776.8 MeV'];
      pts.forEach(function (p, i) {
        var isActive = selected === 3 || selected === i;
        var nodeR = isActive ? 11 : 8;
        var nodePulse = isActive ? (0.9 + 0.1 * Math.sin(time * 2 + i)) : 0.7;

        ctx.beginPath();
        ctx.arc(p.x, p.y, nodeR * nodePulse, 0, Math.PI * 2);
        ctx.fillStyle = isActive ? '#69ff94' : '#2a4a2a';
        ctx.fill();
        if (isActive) {
          ctx.strokeStyle = '#69ff94';
          ctx.lineWidth = 1.5;
          ctx.shadowColor = '#69ff94';
          ctx.shadowBlur = 10;
          ctx.stroke();
          ctx.shadowBlur = 0;
        }

        // Label inside node
        ctx.fillStyle = isActive ? '#020408' : '#4a6a4a';
        ctx.font = 'bold 9px "DM Sans", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(labels[i], p.x, p.y);

        // Mass label outside
        ctx.fillStyle = 'rgba(139, 163, 189, 0.6)';
        ctx.font = '8px "DM Sans", sans-serif';
        ctx.textBaseline = 'alphabetic';
        var labelAngle = angles[i];
        var labelR = r + 18;
        ctx.fillText(masses[i], cx + labelR * Math.cos(labelAngle), cy + labelR * Math.sin(labelAngle) + 3);
      });

      // Status label
      ctx.fillStyle = '#69ff94';
      ctx.font = 'bold 11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=3: LOCKED ✓', cx, cy + r + 28);
      ctx.fillStyle = 'rgba(139, 163, 189, 0.7)';
      ctx.font = '9px "DM Sans", sans-serif';
      ctx.fillText('Koide Q = 2/3 — matches experiment', cx, cy + r + 42);
      return;
    }

    // ── N=4: Destabilizes — Too many channels ──
    if (currentN === 4) {
      // Four vertices in asymmetric arrangement
      var tetraAngles = [
        -Math.PI / 2,
        -Math.PI / 2 + 2 * Math.PI / 3,
        -Math.PI / 2 + 4 * Math.PI / 3,
        Math.PI / 6
      ];
      var tetraR = r * 0.85;
      var tetraPts = tetraAngles.map(function (a, i) {
        var offset = (i === 3) ? -r * 0.08 : 0;
        return { x: cx + tetraR * Math.cos(a), y: cy + tetraR * Math.sin(a) + offset };
      });

      // All edges (complete graph K₄)
      for (var i = 0; i < 4; i++) {
        for (var j = i + 1; j < 4; j++) {
          ctx.beginPath();
          ctx.moveTo(tetraPts[i].x, tetraPts[i].y);
          ctx.lineTo(tetraPts[j].x, tetraPts[j].y);
          ctx.strokeStyle = 'rgba(255, 107, 157, 0.25)';
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }

      // Vertices
      tetraPts.forEach(function (p, i) {
        var jitter = 0.5 * Math.sin(time * 3 + i * 1.7);
        ctx.beginPath();
        ctx.arc(p.x + jitter, p.y + jitter * 0.5, 7, 0, Math.PI * 2);
        ctx.fillStyle = '#ff6b9d';
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 107, 157, 0.4)';
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      // Labels
      ctx.fillStyle = '#ff6b9d';
      ctx.font = 'bold 11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=4: destabilizes ✗', cx, cy + r + 28);
      ctx.fillStyle = 'rgba(139, 163, 189, 0.7)';
      ctx.font = '9px "DM Sans", sans-serif';
      ctx.fillText('Too many channels — coherence breaks', cx, cy + r + 42);
      return;
    }
  }

  // ── Topology animation loop (for standalone Journey mode) ──

  function startTopologyAnimation(canvas, n, selected) {
    if (!canvas) return;
    if (_topologyAnimState && _topologyAnimState.canvas === canvas) return;
    stopTopologyAnimation();
    _topologyAnimState = { canvas: canvas, n: n, selected: selected, running: true };
    var startTime = performance.now();
    function frame() {
      if (!_topologyAnimState || !_topologyAnimState.running) return;
      var t = (performance.now() - startTime) / 1000;
      drawTopologyDiagram(canvas, _topologyAnimState.n, _topologyAnimState.selected, { time: t });
      _topologyAnimState.frameId = requestAnimationFrame(frame);
    }
    _topologyAnimState.frameId = requestAnimationFrame(frame);
  }

  function stopTopologyAnimation() {
    if (_topologyAnimState && _topologyAnimState.frameId) {
      cancelAnimationFrame(_topologyAnimState.frameId);
    }
    _topologyAnimState = null;
  }

  // ═══════════════════════════════════════════════════════════════
  // PUBLIC API — PFRealityVisuals
  // ═══════════════════════════════════════════════════════════════

  window.PFRealityVisuals = {
    drawTopologyDiagram: drawTopologyDiagram,
    drawGravityRefraction: drawGravityRefraction,
    drawParticleVsWave: drawParticleVsWave,
    startGravityAnimation: startGravityAnimation,
    stopGravityAnimation: stopGravityAnimation,
    startTopologyAnimation: startTopologyAnimation,
    stopTopologyAnimation: stopTopologyAnimation
  };

  // ═══════════════════════════════════════════════════════════════
  // PANEL REGISTRATION (Explorer shell only)
  // ═══════════════════════════════════════════════════════════════

  if (window.PFExplorer && typeof window.PFExplorer.registerPanel === 'function') {
    window.PFExplorer.registerPanel({
      id: 'reality-correction',
      mount: function (ctx) {
        ctx.stage.innerHTML =
          '<div class="panel-wrap">' +
            '<div class="panel-atlas">' +
              '<section class="canvas-panel">' +
                '<div class="panel-header">' +
                  '<div>' +
                    '<p class="eyebrow">Three Confrontations</p>' +
                    '<h3>Your intuition about reality is wrong in three predictable ways.</h3>' +
                    '<p>Each section: the wrong model → the replacement → the live evidence.</p>' +
                  '</div>' +
                '</div>' +
                '<div class="reality-card-grid" id="realityCardGrid"></div>' +
                '<div class="canvas-overlay"></div>' +
              '</section>' +
              '<section class="info-panel" id="realityInfo"></section>' +
            '</div>' +
          '</div>';

        this.state = {
          grid: ctx.stage.querySelector('#realityCardGrid'),
          info: ctx.stage.querySelector('#realityInfo'),
          selectedN: 3,
          animTime: 0
        };

        this.renderCards(ctx);
        this.renderInfo(ctx);
      },

      unmount: function () {
        stopGravityAnimation();
        stopTopologyAnimation();
        this.state = null;
      },

      resize: function () {
        // Canvas elements are CSS-size-driven (no JS resize needed)
      },

      renderCards: function (ctx) {
        var self = this;
        var state = this.state;

        var cards = [
          {
            id: 'gravity',
            eyebrow: 'Intuition 1',
            title: 'Gravity is a pull',
            wrong: 'Gravity is a force that attracts masses',
            right: 'Gravity is the refractive bending of propagation paths in a medium with density gradient',
            visual: 'gravity',
            linkId: 'refraction',
            linkLabel: 'Try the refraction sandbox'
          },
          {
            id: 'matter',
            eyebrow: 'Intuition 2',
            title: 'Matter is particles',
            wrong: 'Matter is made of solid, fundamental particles',
            right: 'Matter is a stable self-reinforcing interference pattern — a standing wave in the fabric',
            visual: 'matter',
            linkId: 'playground',
            linkLabel: 'Spawn waves in the playground'
          },
          {
            id: 'generations',
            eyebrow: 'Intuition 3',
            title: 'Three generations is arbitrary',
            wrong: 'There happen to be three generations; it could be any number',
            right: 'The current topology-plus-Koide story points to N=3, but the full generation lock is still conditional on the unresolved bridge theorems.',
            visual: 'generations',
            linkId: 'generations',
            linkLabel: 'See the full generation analysis'
          }
        ];

        state.grid.innerHTML = cards.map(function (card) {
          return (
            '<article class="reality-card" data-card="' + card.id + '">' +
              '<div class="reality-card-header">' +
                '<span class="eyebrow">' + card.eyebrow + '</span>' +
                '<h4 class="reality-card-title">' + card.title + '</h4>' +
              '</div>' +
              '<div class="wrong-panel">' +
                '<div class="wrong-badge">WRONG</div>' +
                '<p class="wrong-text">' + card.wrong + '</p>' +
              '</div>' +
              '<div class="right-panel">' +
                '<div class="right-badge">REALITY</div>' +
                '<p class="right-text">' + card.right + '</p>' +
              '</div>' +
              '<div class="reality-visual-wrap">' +
                (card.visual === 'gravity'
                  ? '<canvas class="reality-visual" id="rvGravity" height="140"></canvas>'
                  : card.visual === 'matter'
                  ? '<canvas class="reality-visual" id="rvMatter" height="120"></canvas>'
                  : '<div class="gen-topology-wrap">' +
                      '<canvas class="reality-visual" id="rvGen" height="140"></canvas>' +
                      '<div class="gen-n-selector" id="genNSelector">' +
                        [1, 2, 3, 4].map(function (n) {
                          return '<button class="gen-n-btn' + (n === 3 ? ' active' : '') + '" data-n="' + n + '">N=' + n + '</button>';
                        }).join('') +
                      '</div>' +
                    '</div>'
                ) +
              '</div>' +
              '<div class="reality-card-actions">' +
                (card.linkId === 'playground'
                  ? '<a href="playground.html" class="soft-button" target="_blank">' + card.linkLabel + ' →</a>'
                  : '<button class="soft-button" type="button" data-open-panel="' + card.linkId + '">' + card.linkLabel + ' →</button>'
                ) +
              '</div>' +
            '</article>'
          );
        }).join('');

        // Draw initial visuals
        drawGravityRefraction(document.getElementById('rvGravity'));
        drawParticleVsWave(document.getElementById('rvMatter'));
        drawTopologyDiagram(document.getElementById('rvGen'), 3, 3);

        // Generation N selector
        state.grid.querySelectorAll('.gen-n-btn').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var n = Number(btn.getAttribute('data-n'));
            state.selectedN = n;
            state.grid.querySelectorAll('.gen-n-btn').forEach(function (b) {
              b.classList.toggle('active', b.getAttribute('data-n') === String(n));
            });
            drawTopologyDiagram(document.getElementById('rvGen'), n, n);
          });
        });

        // Panel navigation buttons
        state.grid.querySelectorAll('[data-open-panel]').forEach(function (btn) {
          btn.addEventListener('click', function () {
            PFExplorer.navigate(btn.getAttribute('data-open-panel'));
          });
        });
      },

      renderInfo: function (ctx) {
        var state = this.state;
        state.info.innerHTML =
          '<div class="panel-header">' +
            '<div>' +
              '<p class="eyebrow">Framework principle</p>' +
              '<h3>Wrong intuition is structurally predictable.</h3>' +
              '<p>Human intuitions evolved for middle scales. They fail at quantum scales, cosmic scales, and anywhere propagation dominates over particle semantics.</p>' +
            '</div>' +
            '<span class="status-pill status-derived">FRAMEWORK</span>' +
          '</div>' +
          '<div class="note-box story-only">' +
            '<strong>How to use this panel</strong>' +
            '<p>Each card shows a wrong intuition, the propagation replacement, and a live visualization. Click through to the linked panel to interact with the full evidence.</p>' +
          '</div>' +
          '<div class="formula">Three axioms. Everything else is derived.</div>' +
          '<div class="stat-grid">' +
            '<div class="stat-tile"><strong>3</strong><span>Core axioms</span></div>' +
            '<div class="stat-tile"><strong>22</strong><span>Audited results</span></div>' +
            '<div class="stat-tile"><strong>3</strong><span>Wrong intuitions confronted</span></div>' +
            '<div class="stat-tile"><strong>1</strong><span>Unified mechanism</span></div>' +
          '</div>' +
          '<div class="note-box audit-only">' +
            '<strong>Audit note</strong>' +
            '<p>These confrontations are honest about their status. Gravity-as-refraction is DERIVED. Standing-wave-matter is a conceptual framework (CONDITIONAL). Generation lock is PARTIAL DERIVATION pending T1 and T2 closure.</p>' +
          '</div>';
      },

      update: function (ctx, dt, time) {
        var state = this.state;
        if (!state || !state.grid) return;
        state.animTime = time;

        // Animate gravity refraction
        var gravityCanvas = state.grid.querySelector('#rvGravity');
        if (gravityCanvas) {
          drawGravityRefraction(gravityCanvas, { time: time });
        }

        // Animate matter wave
        var matterCanvas = state.grid.querySelector('#rvMatter');
        if (matterCanvas) {
          drawParticleVsWave(matterCanvas, { time: time });
        }

        // Animate topology (static per N, but pulse nodes)
        var genCanvas = state.grid.querySelector('#rvGen');
        if (genCanvas) {
          drawTopologyDiagram(genCanvas, state.selectedN, state.selectedN, { time: time });
        }
      }
    });
  }
}());
