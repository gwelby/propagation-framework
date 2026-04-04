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
 *
 * WORLD-CLASS FEATURES:
 * - Continuous wavefront simulation (not ray diagrams)
 * - Web Audio API sound design (gravity drone, wave hum, topology chime)
 * - Interactive mass dragging and wave source placement
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
  function smoothstep(edge0, edge1, x) {
    var t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
    return t * t * (3 - 2 * t);
  }

  // ═══════════════════════════════════════════════════════════════
  // SOUND ENGINE — Web Audio API
  // ═══════════════════════════════════════════════════════════════

  var _audioCtx = null;
  var _audioEnabled = false;
  var _audioNodes = {};

  function ensureAudioContext() {
    if (_audioCtx) return _audioCtx;
    try {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      _audioCtx = new AC();
      return _audioCtx;
    } catch (e) {
      return null;
    }
  }

  function resumeAudio() {
    var ctx = ensureAudioContext();
    if (ctx && ctx.state === 'suspended') {
      ctx.resume();
    }
    _audioEnabled = !!ctx;
    return ctx;
  }

  // Enable audio on first user interaction (browser policy)
  function enableAudioOnInteraction() {
    if (!_audioEnabled) {
      resumeAudio();
    }
  }

  // ── Gravity Drone ──
  // Low-frequency oscillator that deepens near mass

  function startGravityDrone(intensity) {
    if (!_audioEnabled) return;
    stopGravityDrone();
    var ctx = _audioCtx;
    intensity = clamp(intensity || 0.3, 0, 1);

    var osc1 = ctx.createOscillator();
    var osc2 = ctx.createOscillator();
    var gain = ctx.createGain();
    var filter = ctx.createBiquadFilter();

    osc1.type = 'sine';
    osc1.frequency.value = lerp(55, 38, intensity); // A1 → lower
    osc2.type = 'sine';
    osc2.frequency.value = lerp(55.5, 38.3, intensity); // Slight detune for beating

    filter.type = 'lowpass';
    filter.frequency.value = lerp(200, 120, intensity);
    filter.Q.value = 2;

    gain.gain.value = 0;
    gain.gain.linearRampToValueAtTime(0.06 * intensity, ctx.currentTime + 0.5);

    osc1.connect(filter);
    osc2.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc1.start();
    osc2.start();

    _audioNodes.gravityDrone = { osc1: osc1, osc2: osc2, gain: gain, filter: filter };
  }

  function updateGravityDrone(intensity) {
    if (!_audioEnabled || !_audioNodes.gravityDrone) return;
    var ctx = _audioCtx;
    var n = _audioNodes.gravityDrone;
    intensity = clamp(intensity, 0, 1);
    n.osc1.frequency.linearRampToValueAtTime(lerp(55, 38, intensity), ctx.currentTime + 0.1);
    n.osc2.frequency.linearRampToValueAtTime(lerp(55.5, 38.3, intensity), ctx.currentTime + 0.1);
    n.filter.frequency.linearRampToValueAtTime(lerp(200, 120, intensity), ctx.currentTime + 0.1);
    n.gain.gain.linearRampToValueAtTime(0.06 * intensity, ctx.currentTime + 0.1);
  }

  function stopGravityDrone() {
    if (_audioNodes.gravityDrone) {
      var n = _audioNodes.gravityDrone;
      var ctx = _audioCtx;
      n.gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.3);
      setTimeout(function () {
        try { n.osc1.stop(); n.osc2.stop(); } catch (e) {}
      }, 400);
      _audioNodes.gravityDrone = null;
    }
  }

  // ── Standing Wave Hum ──
  // Sine wave at the standing wave frequency

  function startWaveHum(freq, amplitude) {
    if (!_audioEnabled) return;
    stopWaveHum();
    var ctx = _audioCtx;
    freq = freq || 220; // A3
    amplitude = clamp(amplitude || 0.5, 0, 1);

    var osc = ctx.createOscillator();
    var gain = ctx.createGain();
    var filter = ctx.createBiquadFilter();

    osc.type = 'sine';
    osc.frequency.value = freq;

    filter.type = 'lowpass';
    filter.frequency.value = freq * 3;
    filter.Q.value = 1;

    gain.gain.value = 0;
    gain.gain.linearRampToValueAtTime(0.04 * amplitude, ctx.currentTime + 0.3);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);
    osc.start();

    _audioNodes.waveHum = { osc: osc, gain: gain, filter: filter, baseFreq: freq };
  }

  function updateWaveHum(amplitude) {
    if (!_audioEnabled || !_audioNodes.waveHum) return;
    var ctx = _audioCtx;
    var n = _audioNodes.waveHum;
    amplitude = clamp(amplitude, 0, 1);
    n.gain.gain.linearRampToValueAtTime(0.04 * amplitude, ctx.currentTime + 0.05);
  }

  function stopWaveHum() {
    if (_audioNodes.waveHum) {
      var n = _audioNodes.waveHum;
      var ctx = _audioCtx;
      n.gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.2);
      setTimeout(function () { try { n.osc.stop(); } catch (e) {} }, 300);
      _audioNodes.waveHum = null;
    }
  }

  // ── Topology Chime ──
  // Three-note chord when N=3 locks

  function playTopologyChime(n) {
    if (!_audioEnabled) return;
    var ctx = _audioCtx;
    var now = ctx.currentTime;

    // Different chords for different N
    var freqs;
    if (n === 3) {
      // Major triad — locked, harmonious
      freqs = [261.63, 329.63, 392.00]; // C4, E4, G4
    } else if (n === 2) {
      // Dissonant interval — incomplete
      freqs = [261.63, 277.18]; // C4, C#4
    } else if (n === 4) {
      // Chaotic cluster — too many
      freqs = [261.63, 277.18, 293.66, 311.13];
    } else {
      // Single tone — trivial
      freqs = [261.63];
    }

    freqs.forEach(function (freq, i) {
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.value = 0;
      gain.gain.linearRampToValueAtTime(0.03, now + 0.05 + i * 0.02);
      gain.gain.linearRampToValueAtTime(0, now + 1.5);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now + i * 0.02);
      osc.stop(now + 1.6);
    });
  }

  // ── Public Sound API ──

  window.PFSound = {
    enable: enableAudioOnInteraction,
    startGravityDrone: startGravityDrone,
    updateGravityDrone: updateGravityDrone,
    stopGravityDrone: stopGravityDrone,
    startWaveHum: startWaveHum,
    updateWaveHum: updateWaveHum,
    stopWaveHum: stopWaveHum,
    playTopologyChime: playTopologyChime,
    isReady: function () { return _audioEnabled; }
  };

  // ═══════════════════════════════════════════════════════════════
  // 1. GRAVITY WAVEFRONT SIMULATION — Continuous wave propagation
  //    with spatially varying refractive index
  // ═══════════════════════════════════════════════════════════════

  var _gravitySim = null;

  function initGravitySimulation(canvas) {
    if (!canvas) return null;
    var box = getCanvasBox(canvas, 160);
    var w = box.width, h = box.height;

    // Grid resolution (coarser than pixel for performance)
    var cellSize = 3;
    var cols = Math.ceil(w / cellSize);
    var rows = Math.ceil(h / cellSize);

    // Wave state: current and previous frames
    var u = new Float32Array(cols * rows);
    var uPrev = new Float32Array(cols * rows);
    var uNext = new Float32Array(cols * rows);

    // Refractive index field: n(x,y) = 1 + rs / |r - r_mass|
    var nField = new Float32Array(cols * rows);

    // Wave speed field: c(x,y) = c0 / n(x,y)
    var cField = new Float32Array(cols * rows);

    // Image data for rendering
    var imageData = canvas.getContext('2d').createImageData(w, h);

    return {
      canvas: canvas,
      ctx: canvas.getContext('2d'),
      box: box,
      cols: cols,
      rows: rows,
      cellSize: cellSize,
      u: u,
      uPrev: uPrev,
      uNext: uNext,
      nField: nField,
      cField: cField,
      imageData: imageData,
      massX: 0.5,
      massY: 0.5,
      massStrength: 0.4,
      waveFreq: 0.08,
      waveAmp: 0.6,
      damping: 0.998,
      time: 0,
      running: false,
      dragging: false,
      animFrameId: null
    };
  }

  function updateGravityFields(sim) {
    var cols = sim.cols, rows = sim.rows;
    var massCol = sim.massX * cols;
    var massRow = sim.massY * rows;
    var rs = sim.massStrength * Math.min(cols, rows) * 0.3;

    for (var j = 0; j < rows; j++) {
      for (var i = 0; i < cols; i++) {
        var dx = i - massCol;
        var dy = j - massRow;
        var dist = Math.sqrt(dx * dx + dy * dy) + 1; // +1 to avoid singularity
        var nVal = 1 + rs / dist;
        var idx = j * cols + i;
        sim.nField[idx] = nVal;
        sim.cField[idx] = 1 / nVal; // c = c0 / n, c0 = 1
      }
    }
  }

  function stepGravityWave(sim) {
    var cols = sim.cols, rows = sim.rows;
    var u = sim.u, uPrev = sim.uPrev, uNext = sim.uNext;
    var cField = sim.cField;
    var damping = sim.damping;

    for (var j = 1; j < rows - 1; j++) {
      for (var i = 1; i < cols - 1; i++) {
        var idx = j * cols + i;
        var c = cField[idx];

        // 2D wave equation: u_tt = c² * (u_xx + u_yy)
        // Discretized: u_next = 2*u - u_prev + c² * dt² * laplacian
        var laplacian = u[idx - 1] + u[idx + 1] + u[idx - cols] + u[idx + cols] - 4 * u[idx];
        var dt2 = 0.25; // Courant-stable timestep
        uNext[idx] = 2 * u[idx] - uPrev[idx] + c * c * dt2 * laplacian;
        uNext[idx] *= damping;
      }
    }

    // Absorbing boundary conditions (damp edges)
    var edgeDamp = 0.9;
    for (var i = 0; i < cols; i++) {
      uNext[i] *= edgeDamp; // top
      uNext[(rows - 1) * cols + i] *= edgeDamp; // bottom
    }
    for (var j = 0; j < rows; j++) {
      uNext[j * cols] *= edgeDamp; // left
      uNext[j * cols + cols - 1] *= edgeDamp; // right
    }

    // Swap buffers
    var tmp = uPrev;
    sim.uPrev = u;
    sim.u = uNext;
    sim.uNext = tmp;
  }

  function driveGravityWave(sim, time) {
    var cols = sim.cols, rows = sim.rows;
    var u = sim.u;
    var freq = sim.waveFreq;
    var amp = sim.waveAmp;

    // Drive from left edge: continuous plane wave
    var driveCols = 3;
    for (var j = 0; j < rows; j++) {
      for (var di = 0; di < driveCols; di++) {
        var idx = j * cols + di;
        var phase = time * freq * Math.PI * 2;
        // Smooth envelope to avoid sharp edges
        var envelope = smoothstep(0, driveCols, di);
        u[idx] += Math.sin(phase) * amp * envelope * 0.3;
      }
    }
  }

  function renderGravityWave(sim) {
    var w = sim.box.width, h = sim.box.height;
    var cols = sim.cols, rows = sim.rows;
    var cellSize = sim.cellSize;
    var u = sim.u;
    var imageData = sim.imageData;
    var data = imageData.data;

    // Clear
    for (var i = 0; i < data.length; i += 4) {
      data[i] = 2;     // R
      data[i + 1] = 4; // G
      data[i + 2] = 8; // B
      data[i + 3] = 255;
    }

    // Render wave field
    for (var j = 0; j < rows; j++) {
      for (var i = 0; i < cols; i++) {
        var idx = j * cols + i;
        var val = u[idx];

        // Color mapping: positive = cyan, negative = deep blue
        var absVal = Math.abs(val);
        var px = Math.min(i * cellSize, w - 1);
        var py = Math.min(j * cellSize, h - 1);

        var r, g, b;
        if (val > 0) {
          // Cyan wave peaks
          r = Math.floor(absVal * 0);
          g = Math.floor(absVal * 200);
          b = Math.floor(absVal * 255);
        } else {
          // Deep blue troughs
          r = Math.floor(absVal * 10);
          g = Math.floor(absVal * 30);
          b = Math.floor(absVal * 120 + 20);
        }

        // Fill cell (cellSize × cellSize pixels)
        for (var dy = 0; dy < cellSize && py + dy < h; dy++) {
          for (var dx = 0; dx < cellSize && px + dx < w; dx++) {
            var pi = ((py + dy) * w + (px + dx)) * 4;
            data[pi] = Math.min(255, data[pi] + r);
            data[pi + 1] = Math.min(255, data[pi + 1] + g);
            data[pi + 2] = Math.min(255, data[pi + 2] + b);
          }
        }
      }
    }

    // Draw mass indicator
    var massPx = sim.massX * w;
    var massPy = sim.massY * h;
    var massR = Math.min(12, w * 0.03);

    var ctx = sim.ctx;
    ctx.putImageData(imageData, 0, 0);

    // Mass glow
    var grad = ctx.createRadialGradient(massPx, massPy, 0, massPx, massPy, massR * 4);
    grad.addColorStop(0, 'rgba(255, 215, 0, 0.6)');
    grad.addColorStop(0.3, 'rgba(255, 179, 71, 0.15)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(massPx, massPy, massR * 4, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(massPx, massPy, massR, 0, Math.PI * 2);
    ctx.fillStyle = '#ffd700';
    ctx.shadowColor = '#ffd700';
    ctx.shadowBlur = 12;
    ctx.fill();
    ctx.shadowBlur = 0;

    // Labels
    ctx.font = '10px "DM Sans", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillStyle = 'rgba(139, 163, 189, 0.5)';
    ctx.fillText('wavefront →', 8, 14);

    ctx.fillStyle = 'rgba(255, 71, 87, 0.5)';
    ctx.textAlign = 'center';
    ctx.font = '9px "DM Sans", sans-serif';
    ctx.fillText('✗ "gravity pulls" — no, the wave slows down here', w / 2, h - 8);
  }

  function runGravitySimulation(sim) {
    if (!sim || !sim.running) return;
    sim.time += 1;

    driveGravityWave(sim, sim.time);
    stepGravityWave(sim);
    stepGravityWave(sim); // 2 steps per frame for speed
    renderGravityWave(sim);

    // Update sound
    if (_audioEnabled) {
      updateGravityDrone(sim.massStrength);
    }

    sim.animFrameId = requestAnimationFrame(function () {
      runGravitySimulation(sim);
    });
  }

  function startGravitySimulation(canvas) {
    if (!canvas) return;
    stopGravitySimulation();

    var sim = initGravitySimulation(canvas);
    if (!sim) return;

    updateGravityFields(sim);
    sim.running = true;
    _gravitySim = sim;

    // Mouse/touch interaction: drag the mass
    function getPos(e) {
      var rect = canvas.getBoundingClientRect();
      var clientX = e.touches ? e.touches[0].clientX : e.clientX;
      var clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return {
        x: (clientX - rect.left) / rect.width,
        y: (clientY - rect.top) / rect.height
      };
    }

    function onDown(e) {
      e.preventDefault();
      var pos = getPos(e);
      var dx = pos.x - sim.massX;
      var dy = pos.y - sim.massY;
      if (Math.sqrt(dx * dx + dy * dy) < 0.15) {
        sim.dragging = true;
      }
    }

    function onMove(e) {
      if (!sim.dragging) return;
      e.preventDefault();
      var pos = getPos(e);
      sim.massX = clamp(pos.x, 0.1, 0.9);
      sim.massY = clamp(pos.y, 0.1, 0.9);
      updateGravityFields(sim);
    }

    function onUp() {
      sim.dragging = false;
    }

    canvas.addEventListener('mousedown', onDown);
    canvas.addEventListener('mousemove', onMove);
    canvas.addEventListener('mouseup', onUp);
    canvas.addEventListener('touchstart', onDown, { passive: false });
    canvas.addEventListener('touchmove', onMove, { passive: false });
    canvas.addEventListener('touchend', onUp);

    sim._cleanup = function () {
      canvas.removeEventListener('mousedown', onDown);
      canvas.removeEventListener('mousemove', onMove);
      canvas.removeEventListener('mouseup', onUp);
      canvas.removeEventListener('touchstart', onDown);
      canvas.removeEventListener('touchmove', onMove);
      canvas.removeEventListener('touchend', onUp);
    };

    runGravitySimulation(sim);
  }

  function stopGravitySimulation() {
    if (_gravitySim) {
      _gravitySim.running = false;
      if (_gravitySim.animFrameId) cancelAnimationFrame(_gravitySim.animFrameId);
      if (_gravitySim._cleanup) _gravitySim._cleanup();
      _gravitySim = null;
    }
    stopGravityDrone();
  }

  // ═══════════════════════════════════════════════════════════════
  // 2. STANDING WAVE — Two counter-propagating waves forming nodes
  // ═══════════════════════════════════════════════════════════════

  var _waveAnimState = null;

  function drawParticleVsWave(canvas, opts) {
    if (!canvas) return;
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var box = getCanvasBox(canvas, 140);
    var cw = box.width, ch = box.height;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(box.dpr, box.dpr);
    ctx.clearRect(0, 0, cw, ch);

    var t = opts.time !== undefined ? opts.time : (performance.now() / 1000);
    var midY = ch * 0.50;
    var amp = ch * 0.20;
    var numWaves = 4;

    // ── Show the two traveling waves (faint) ──
    var waveAlpha = 0.25;
    for (var dir = -1; dir <= 1; dir += 2) {
      ctx.beginPath();
      for (var xi = 0; xi <= cw; xi += 1) {
        var x = xi / cw * Math.PI * numWaves;
        var y = midY - Math.sin(x - dir * t * 1.5) * amp * 0.5;
        if (xi === 0) ctx.moveTo(xi, y);
        else ctx.lineTo(xi, y);
      }
      ctx.strokeStyle = dir === 1
        ? 'rgba(0, 207, 255, ' + waveAlpha + ')'
        : 'rgba(255, 179, 71, ' + waveAlpha + ')';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    // Labels for traveling waves
    ctx.font = '8px "DM Sans", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillStyle = 'rgba(0, 207, 255, 0.5)';
    ctx.fillText('→ right-moving', 8, 12);
    ctx.fillStyle = 'rgba(255, 179, 71, 0.5)';
    ctx.fillText('← left-moving', 8, 22);

    // ── Envelope (dashed boundary) ──
    ctx.beginPath();
    for (var xi = 0; xi <= cw; xi += 1) {
      var xEnv = xi / cw * Math.PI * numWaves;
      var yEnv = midY - Math.sin(xEnv) * amp;
      if (xi === 0) ctx.moveTo(xi, yEnv);
      else ctx.lineTo(xi, yEnv);
    }
    ctx.strokeStyle = 'rgba(105, 255, 148, 0.12)';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.beginPath();
    for (var xi = 0; xi <= cw; xi += 1) {
      var xEnv = xi / cw * Math.PI * numWaves;
      var yEnv = midY + Math.sin(xEnv) * amp;
      if (xi === 0) ctx.moveTo(xi, yEnv);
      else ctx.lineTo(xi, yEnv);
    }
    ctx.strokeStyle = 'rgba(105, 255, 148, 0.12)';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.stroke();
    ctx.setLineDash([]);

    // ── Standing wave: sin(kx) * cos(ωt) — the SUM of the two ──
    ctx.beginPath();
    for (var xi = 0; xi <= cw; xi += 1) {
      var x = xi / cw * Math.PI * numWaves;
      var y = midY - Math.sin(x) * Math.cos(t * 1.5) * amp;
      if (xi === 0) ctx.moveTo(xi, y);
      else ctx.lineTo(xi, y);
    }
    ctx.strokeStyle = 'rgba(105, 255, 148, 0.95)';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = 'rgba(105, 255, 148, 0.4)';
    ctx.shadowBlur = 8;
    ctx.stroke();
    ctx.shadowBlur = 0;

    // ── Node markers (pulsing) ──
    for (var n = 0; n <= numWaves; n++) {
      var nx = (n / numWaves) * cw;
      var nodeGlow = 0.5 + 0.5 * Math.sin(t * 2 + n);
      ctx.beginPath();
      ctx.arc(nx, midY, 3 + nodeGlow * 2, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(105, 255, 148, ' + (0.4 + nodeGlow * 0.3) + ')';
      ctx.fill();
    }

    // ── λ/2 spacing annotation ──
    var halfLambdaStart = 0;
    var halfLambdaEnd = (1 / numWaves) * cw;
    ctx.beginPath();
    ctx.moveTo(halfLambdaStart, midY + amp + 16);
    ctx.lineTo(halfLambdaEnd, midY + amp + 16);
    ctx.strokeStyle = 'rgba(255, 221, 85, 0.5)';
    ctx.lineWidth = 1;
    ctx.stroke();
    // Tick marks
    ctx.beginPath();
    ctx.moveTo(halfLambdaStart, midY + amp + 13);
    ctx.lineTo(halfLambdaStart, midY + amp + 19);
    ctx.moveTo(halfLambdaEnd, midY + amp + 13);
    ctx.lineTo(halfLambdaEnd, midY + amp + 19);
    ctx.stroke();
    ctx.fillStyle = 'rgba(255, 221, 85, 0.6)';
    ctx.font = '8px "DM Sans", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('λ/2', (halfLambdaStart + halfLambdaEnd) / 2, midY + amp + 28);

    // ── Labels ──
    ctx.fillStyle = '#69ff94';
    ctx.font = 'bold 10px "DM Sans", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('two waves interfere → standing wave forms', cw / 2, ch - 18);

    ctx.fillStyle = 'rgba(139, 163, 189, 0.6)';
    ctx.font = '9px "DM Sans", sans-serif';
    ctx.fillText('Stable nodes at λ/2 — this is what matter IS', cw / 2, ch - 6);

    // ── Particle ghost (faint, struck through) ──
    var ghostX = cw * 0.78;
    var ghostY = midY - amp * 0.6;
    ctx.globalAlpha = 0.12 + 0.04 * Math.sin(t * 0.8);
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

    ctx.fillStyle = 'rgba(255, 107, 157, 0.35)';
    ctx.font = '8px "DM Sans", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('"particle"', ghostX, ghostY + 20);
  }

  function startWaveAnimation(canvas) {
    if (!canvas) return;
    if (_waveAnimState && _waveAnimState.canvas === canvas) return;
    stopWaveAnimation();
    _waveAnimState = { canvas: canvas, running: true };
    var startTime = performance.now();

    // Start sound
    if (_audioEnabled) {
      startWaveHum(220, 0.5);
    }

    function frame() {
      if (!_waveAnimState || !_waveAnimState.running) return;
      var t = (performance.now() - startTime) / 1000;
      drawParticleVsWave(canvas, { time: t });
      _waveAnimState.frameId = requestAnimationFrame(frame);
    }
    _waveAnimState.frameId = requestAnimationFrame(frame);
  }

  function stopWaveAnimation() {
    if (_waveAnimState && _waveAnimState.frameId) {
      cancelAnimationFrame(_waveAnimState.frameId);
    }
    _waveAnimState = null;
    stopWaveHum();
  }

  // ═══════════════════════════════════════════════════════════════
  // 3. GENERATION TOPOLOGY — Interference-based visualization
  // ═══════════════════════════════════════════════════════════════

  var _topologyAnimState = null;

  function drawTopologyDiagram(canvas, n, selected, opts) {
    if (!canvas) return;
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var box = getCanvasBox(canvas, 160);
    var cw = box.width, ch = box.height;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(box.dpr, box.dpr);
    ctx.clearRect(0, 0, cw, ch);

    var cx = cw / 2, cy = ch / 2;
    var r = Math.min(cw, ch) * 0.26;
    var time = opts.time || 0;

    // ── Background glow ──
    var glowColor;
    if (n === 3) glowColor = 'rgba(105, 255, 148, 0.04)';
    else if (n === 2) glowColor = 'rgba(0, 207, 255, 0.03)';
    else if (n === 4) glowColor = 'rgba(255, 107, 157, 0.03)';
    else glowColor = 'rgba(200, 168, 255, 0.03)';

    ctx.beginPath();
    ctx.arc(cx, cy, r * 2.2, 0, Math.PI * 2);
    ctx.fillStyle = glowColor;
    ctx.fill();

    // ── Interference pattern background ──
    // Show what N channels of interference look like
    var imgData = ctx.createImageData(cw, ch);
    var data = imgData.data;
    var numSources = n;
    var sourceAngles = [];
    for (var si = 0; si < numSources; si++) {
      sourceAngles.push(-Math.PI / 2 + si * 2 * Math.PI / numSources);
    }
    var sourceR = r * 0.6;
    var sources = sourceAngles.map(function (a) {
      return { x: cx + sourceR * Math.cos(a), y: cy + sourceR * Math.sin(a) };
    });

    for (var py = 0; py < ch; py++) {
      for (var px = 0; px < cw; px++) {
        var waveSum = 0;
        for (var si = 0; si < sources.length; si++) {
          var dx = px - sources[si].x;
          var dy = py - sources[si].y;
          var dist = Math.sqrt(dx * dx + dy * dy) + 1;
          var k = 0.15;
          waveSum += Math.sin(dist * k - time * 2 + si * Math.PI * 2 / numSources) / Math.sqrt(dist);
        }

        var absVal = Math.abs(waveSum);
        var intensity = clamp(absVal * 0.5, 0, 1);

        var pi = (py * cw + px) * 4;
        if (n === 3) {
          // Green for coherent (N=3)
          data[pi] = Math.floor(intensity * 20);
          data[pi + 1] = Math.floor(intensity * 180 + 20);
          data[pi + 2] = Math.floor(intensity * 80 + 10);
        } else if (n === 4) {
          // Red/pink for chaotic (N=4)
          data[pi] = Math.floor(intensity * 150 + 15);
          data[pi + 1] = Math.floor(intensity * 40 + 10);
          data[pi + 2] = Math.floor(intensity * 60 + 10);
        } else {
          // Blue for incomplete (N=1,2)
          data[pi] = Math.floor(intensity * 30);
          data[pi + 1] = Math.floor(intensity * 80 + 15);
          data[pi + 2] = Math.floor(intensity * 150 + 20);
        }
        data[pi + 3] = Math.floor(intensity * 60);
      }
    }
    ctx.putImageData(imgData, 0, 0);

    // ── Draw channel nodes ──
    var nodeR = r * 1.1;
    var angles = [];
    for (var ni = 0; ni < n; ni++) {
      angles.push(-Math.PI / 2 + ni * 2 * Math.PI / n);
    }
    var pts = angles.map(function (a) {
      return { x: cx + nodeR * Math.cos(a), y: cy + nodeR * Math.sin(a) };
    });

    // Connection lines
    for (var i = 0; i < n; i++) {
      for (var j = i + 1; j < n; j++) {
        ctx.beginPath();
        ctx.moveTo(pts[i].x, pts[i].y);
        ctx.lineTo(pts[j].x, pts[j].y);
        var lineAlpha = n === 3 ? 0.5 : 0.2;
        ctx.strokeStyle = n === 3
          ? 'rgba(105, 255, 148, ' + lineAlpha + ')'
          : n === 4
          ? 'rgba(255, 107, 157, ' + lineAlpha + ')'
          : 'rgba(0, 207, 255, ' + lineAlpha + ')';
        ctx.lineWidth = n === 3 ? 2 : 1;
        ctx.stroke();
      }
    }

    // Nodes
    var labels = ['e', 'μ', 'τ', 'X'];
    pts.forEach(function (p, i) {
      var nodePulse = 0.85 + 0.15 * Math.sin(time * 2 + i);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 9 * nodePulse, 0, Math.PI * 2);
      ctx.fillStyle = n === 3 ? '#69ff94' : n === 4 ? '#ff6b9d' : '#00e5ff';
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = 8;
      ctx.fill();
      ctx.shadowBlur = 0;

      ctx.fillStyle = '#020408';
      ctx.font = 'bold 9px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(labels[i], p.x, p.y);
    });

    // ── Status label ──
    ctx.textBaseline = 'alphabetic';
    if (n === 3) {
      ctx.fillStyle = '#69ff94';
      ctx.font = 'bold 11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=3: LOCKED ✓', cx, cy + nodeR + 22);
      ctx.fillStyle = 'rgba(139, 163, 189, 0.6)';
      ctx.font = '9px "DM Sans", sans-serif';
      ctx.fillText('Koide Q = 2/3 — triangular interference', cx, cy + nodeR + 36);
    } else if (n === 4) {
      ctx.fillStyle = '#ff6b9d';
      ctx.font = 'bold 11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=4: chaotic ✗', cx, cy + nodeR + 22);
      ctx.fillStyle = 'rgba(139, 163, 189, 0.6)';
      ctx.font = '9px "DM Sans", sans-serif';
      ctx.fillText('Interference pattern unstable', cx, cy + nodeR + 36);
    } else if (n === 2) {
      ctx.fillStyle = '#00e5ff';
      ctx.font = 'bold 11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=2: ℤ₂ only', cx, cy + nodeR + 22);
      ctx.fillStyle = 'rgba(139, 163, 189, 0.6)';
      ctx.font = '9px "DM Sans", sans-serif';
      ctx.fillText('Linear interference — no triangle', cx, cy + nodeR + 36);
    } else {
      ctx.fillStyle = '#c8a8ff';
      ctx.font = 'bold 11px "DM Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('N=1: trivial', cx, cy + nodeR + 22);
      ctx.fillStyle = 'rgba(139, 163, 189, 0.6)';
      ctx.font = '9px "DM Sans", sans-serif';
      ctx.fillText('No interference possible', cx, cy + nodeR + 36);
    }
  }

  function startTopologyAnimation(canvas, n, selected) {
    if (!canvas) return;
    if (_topologyAnimState && _topologyAnimState.canvas === canvas) return;
    stopTopologyAnimation();
    _topologyAnimState = { canvas: canvas, n: n, selected: selected, running: true };
    var startTime = performance.now();

    // Play chime
    if (_audioEnabled) {
      playTopologyChime(n);
    }

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
    drawGravityRefraction: function (canvas, opts) {
      // Backward compat: if called without simulation, start one
      if (_gravitySim && _gravitySim.canvas === canvas) return;
      startGravitySimulation(canvas);
    },
    drawParticleVsWave: drawParticleVsWave,
    startGravitySimulation: startGravitySimulation,
    stopGravitySimulation: stopGravitySimulation,
    startWaveAnimation: startWaveAnimation,
    stopWaveAnimation: stopWaveAnimation,
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
        stopGravitySimulation();
        stopWaveAnimation();
        stopTopologyAnimation();
        this.state = null;
      },

      resize: function () {
        // Canvas elements are CSS-size-driven
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
                  ? '<canvas class="reality-visual" id="rvGravity" height="160"></canvas>'
                  : card.visual === 'matter'
                  ? '<canvas class="reality-visual" id="rvMatter" height="140"></canvas>'
                  : '<div class="gen-topology-wrap">' +
                      '<canvas class="reality-visual" id="rvGen" height="160"></canvas>' +
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

        // Start simulations
        startGravitySimulation(document.getElementById('rvGravity'));
        startWaveAnimation(document.getElementById('rvMatter'));
        startTopologyAnimation(document.getElementById('rvGen'), 3, 3);

        // Generation N selector
        state.grid.querySelectorAll('.gen-n-btn').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var n = Number(btn.getAttribute('data-n'));
            state.selectedN = n;
            state.grid.querySelectorAll('.gen-n-btn').forEach(function (b) {
              b.classList.toggle('active', b.getAttribute('data-n') === String(n));
            });
            stopTopologyAnimation();
            startTopologyAnimation(document.getElementById('rvGen'), n, n);
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
      }
    });
  }

  // ── Enable audio on first click anywhere in the page ──
  document.addEventListener('click', function () {
    enableAudioOnInteraction();
  }, { once: true });

  document.addEventListener('touchstart', function () {
    enableAudioOnInteraction();
  }, { once: true });
}());
