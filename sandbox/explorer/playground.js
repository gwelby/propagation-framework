/**
 * Propagation Playground — WebGL Wave Interference Lab
 *
 * Fragment-shader-based 2D wave simulation.
 * Click to spawn sources. Watch interference patterns form.
 * Coherent regions (constructive interference) glow green.
 *
 * Educational moment: λ/2 spacing → standing wave → Bohr orbit → matter.
 */
(function () {
  'use strict';

  // ── Shader sources ────────────────────────────────────────────────────────────

  var VERT_SHADER = [
    'attribute vec2 a_position;',
    'void main() {',
    '  gl_Position = vec4(a_position, 0.0, 1.0);',
    '}'
  ].join('\n');

  var FRAG_SHADER = [
    'precision highp float;',

    'uniform vec2  u_resolution;',
    'uniform float u_time;',
    'uniform float u_wavelength;',   // pixels per wavelength
    'uniform float u_speed;',         // propagation speed multiplier
    'uniform float u_amplitude;',     // global amplitude scale
    'uniform float u_decay;',         // spatial decay rate

    'uniform int   u_numSources;',
    'uniform vec2  u_sources[16];',   // source positions (pixels)
    'uniform float u_phases[16];',    // source phases

    'varying vec2 v_uv;',

    'const float PI     = 3.14159265359;',
    'const float TWO_PI = 6.28318530718;',

    '  // Wave contribution from one source',
    'float waveContrib(vec2 fragCoord, vec2 center, float phase) {',
    '  float dist = length(fragCoord - center);',
    '  if (dist < 0.5) return 0.0;',
    '  float k = TWO_PI / u_wavelength;',
    '  float omega = u_speed * k;',
    '  float theta = k * dist - omega * u_time + phase;',
    '  return sin(theta) * exp(-u_decay * dist);',
    '}',

    'void main() {',
    '  vec2 uv = gl_FragCoord.xy;',

    '  // Sum all wave contributions',
    '  float total = 0.0;',
    '  float maxAmp = 0.0;',
    '  for (int i = 0; i < 16; i++) {',
    '    if (i >= u_numSources) break;',
    '    float w = waveContrib(uv, u_sources[i], u_phases[i]);',
    '    total += w;',
    '    maxAmp += abs(w);',  // theoretical max if all in phase
    '  }',
    '',

    '  // Coherence: if no sources, gray background',
    '  if (u_numSources == 0) {',
    '    gl_FragColor = vec4(0.04, 0.07, 0.12, 1.0);',
    '    return;',
    '  }',
    '',

    '  // Normalized amplitude (0..1)',
    '  float normAmp = clamp(abs(total) / max(maxAmp, 0.001), 0.0, 1.0);',

    '  // Standing wave detection: if two sources, measure node clarity',
    '  float standingness = 0.0;',
    '  if (u_numSources == 2) {',
    '    vec2 d = u_sources[1] - u_sources[0];',
    '    float sep = length(d);',
    '    // Node clarity: high when separation ≈ n * λ/2',
    '    float halfLambda = u_wavelength * 0.5;',
    '    float targetSep = floor(sep / halfLambda + 0.5) * halfLambda;',
    '    float error = abs(sep - targetSep) / halfLambda;',
    '    standingness = exp(-error * error * 8.0);',
    '  }',

    '  // Color mapping',
    '  // Background: deep void',
    '  vec3 bgColor = vec3(0.015, 0.025, 0.05);',

    '  // Constructive interference → bright',
    '  vec3 brightColor = vec3(0.0, 0.72, 1.0);',  // cyan
    '  // Destructive interference → dark blue',
    '  vec3 darkColor   = vec3(0.02, 0.06, 0.18);',

    '  float signedWave = total / max(maxAmp, 0.001);',
    '  float intensity;',
    '  vec3 waveColor;',

    '  if (signedWave >= 0.0) {',
    '    intensity = signedWave;',
    '    waveColor = mix(bgColor, brightColor, intensity);',
    '  } else {',
    '    intensity = -signedWave;',
    '    waveColor = mix(bgColor, darkColor, intensity);',
    '  }',

    '  // Coherence regions glow lime-green on top of wave pattern',
    '  // High coherence = constructive interference from ≥2 sources',
    '  float coherenceStrength = 0.0;',
    '  if (u_numSources >= 2) {',
    '    coherenceStrength = pow(normAmp, 2.0) * standingness;',
    '  }',
    '  vec3 cohereColor = vec3(0.41, 1.0, 0.58); // lime',
    '  waveColor = mix(waveColor, cohereColor, coherenceStrength * 0.7);',

    '  // Add subtle glow bloom at peaks',
    '  float glow = pow(normAmp, 3.5) * 0.4;',
    '  waveColor += cohereColor * glow * (1.0 - coherenceStrength);',

    '  // Standing wave node lines (very thin dark bands at zero crossings)',
    '  if (u_numSources >= 2 && standingness > 0.5) {',
    '    // Detect node proximity: where total is zero',
    '    float nodeProx = exp(-abs(total) * 6.0);',
    '    vec3 nodeColor = vec3(0.01, 0.02, 0.06);',
    '    waveColor = mix(waveColor, nodeColor, nodeProx * 0.6 * standingness);',
    '  }',
    '',
    '  gl_FragColor = vec4(waveColor, 1.0);',
    '}'
  ].join('\n');

  // ── WebGL setup ───────────────────────────────────────────────────────────────

  var canvas = document.getElementById('playgroundCanvas');
  var gl = canvas.getContext('webgl', { antialias: false, alpha: false });

  if (!gl) {
    canvas.style.display = 'none';
    document.body.innerHTML += '<div style="position:fixed;inset:0;display:flex;align-items:center;justify-content:center;color:var(--text);font-family:var(--ui);text-align:center;padding:40px;"><div><h2 style="color:var(--uncertain)">WebGL not available</h2><p>This playground requires WebGL. Try a different browser.</p></div></div>';
    return;
  }

  function compileShader(type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      console.error('Shader compile error:', gl.getShaderInfoLog(sh));
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  var vert = compileShader(gl.VERTEX_SHADER, VERT_SHADER);
  var frag = compileShader(gl.FRAGMENT_SHADER, FRAG_SHADER);
  if (!vert || !frag) {
    return;
  }
  var program = gl.createProgram();
  gl.attachShader(program, vert);
  gl.attachShader(program, frag);
  gl.linkProgram(program);

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error('Program link error:', gl.getProgramInfoLog(program));
    return;
  }

  gl.useProgram(program);

  // Fullscreen quad
  var quadBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, quadBuf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1,  1, -1,  -1, 1,
    -1,  1,  1, -1,   1, 1
  ]), gl.STATIC_DRAW);

  var posLoc = gl.getAttribLocation(program, 'a_position');
  gl.enableVertexAttribArray(posLoc);
  gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

  // Uniform locations
  var U = {
    resolution:   gl.getUniformLocation(program, 'u_resolution'),
    time:         gl.getUniformLocation(program, 'u_time'),
    wavelength:   gl.getUniformLocation(program, 'u_wavelength'),
    speed:        gl.getUniformLocation(program, 'u_speed'),
    amplitude:    gl.getUniformLocation(program, 'u_amplitude'),
    decay:        gl.getUniformLocation(program, 'u_decay'),
    numSources:   gl.getUniformLocation(program, 'u_numSources'),
    sources:      gl.getUniformLocation(program, 'u_sources[0]'),
    phases:       gl.getUniformLocation(program, 'u_phases[0]')
  };

  // ── State ────────────────────────────────────────────────────────────────────

  var sources = [];
  var draggingIndex = -1;
  var time = 0;
  var lastTime = performance.now();

  var params = {
    wavelength: 60,
    speed: 1.5,
    amplitude: 1.0,
    decay: 0.008
  };

  var standingWaveMode = false;

  // ── Resize ────────────────────────────────────────────────────────────────────

  function resize() {
    var dpr = Math.min(window.devicePixelRatio, 2);
    canvas.width  = window.innerWidth  * dpr;
    canvas.height = window.innerHeight * dpr;
    canvas.style.width  = window.innerWidth  + 'px';
    canvas.style.height = window.innerHeight + 'px';
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  window.addEventListener('resize', resize);
  resize();

  // ── Shader uniform updates ────────────────────────────────────────────────────

  function uploadSources() {
    gl.uniform1i(U.numSources, sources.length);

    var posData = new Float32Array(16 * 2);
    var phaseData = new Float32Array(16);
    sources.forEach(function (s, i) {
      posData[i * 2]     = s.x * window.devicePixelRatio;
      posData[i * 2 + 1] = (window.innerHeight - s.y) * window.devicePixelRatio; // flip Y
      phaseData[i] = s.phase;
    });
    gl.uniform2fv(U.sources, posData);
    gl.uniform1fv(U.phases, phaseData);
  }

  function uploadParams() {
    gl.uniform1f(U.wavelength, params.wavelength);
    gl.uniform1f(U.speed,      params.speed);
    gl.uniform1f(U.amplitude,  params.amplitude);
    gl.uniform1f(U.decay,      params.decay);
  }

  // ── Source management ─────────────────────────────────────────────────────────

  function addSource(x, y, phase) {
    if (sources.length >= 16) return;
    sources.push({ x: x, y: y, phase: phase !== undefined ? phase : Math.random() * Math.PI * 2 });
    updateStats();
  }

  function removeNearest(x, y) {
    if (!sources.length) return;
    var best = Infinity, bestIdx = -1;
    sources.forEach(function (s, i) {
      var d = Math.hypot(s.x - x, s.y - y);
      if (d < best) { best = d; bestIdx = i; }
    });
    if (bestIdx >= 0) {
      sources.splice(bestIdx, 1);
      updateStats();
    }
  }

  function addStandingWavePair(x, y) {
    // Place two sources separated by ~1 wavelength
    var sep = params.wavelength;
    addSource(x - sep / 2, y, 0);
    if (sources.length < 16) {
      addSource(x + sep / 2, y, 0);
    }
  }

  // ── Stats / UI ───────────────────────────────────────────────────────────────

  function updateStats() {
    document.getElementById('statSources').textContent = sources.length;
    document.getElementById('sourceBadgeCount').textContent = sources.length;

    var badge = document.getElementById('sourceBadge');
    if (sources.length > 0) {
      badge.removeAttribute('hidden');
    } else {
      badge.setAttribute('hidden', 'hidden');
    }

    if (sources.length >= 2) {
      var s0 = sources[0], s1 = sources[1];
      var sep = Math.hypot(s1.x - s0.x, s1.y - s0.y);
      var halfLam = params.wavelength / 2;
      var targetNodes = Math.round(sep / halfLam);
      document.getElementById('statNodes').textContent = targetNodes;

      var nearestHalfLam = targetNodes * halfLam;
      var error = Math.abs(sep - nearestHalfLam) / halfLam;
      var coherencePct = Math.round(Math.max(0, (1 - error) * 100));
      document.getElementById('statCoherence').textContent = coherencePct + '%';

      var pill = document.getElementById('coherencePill');
      if (coherencePct >= 80) {
        pill.style.color = 'var(--cohere)';
      } else if (coherencePct >= 50) {
        pill.style.color = 'var(--refract)';
      } else {
        pill.style.color = 'var(--muted)';
      }
    } else {
      document.getElementById('statNodes').textContent = '—';
      document.getElementById('statCoherence').textContent = '—';
    }
  }

  // ── Controls wiring ───────────────────────────────────────────────────────────

  document.getElementById('pgWavelength').addEventListener('input', function (e) {
    params.wavelength = Number(e.target.value);
    document.getElementById('pgWavelengthOut').textContent = params.wavelength + ' px';
    updateStats();
  });

  document.getElementById('pgSpeed').addEventListener('input', function (e) {
    params.speed = Number(e.target.value);
    document.getElementById('pgSpeedOut').textContent = params.speed.toFixed(1);
  });

  document.getElementById('pgAmplitude').addEventListener('input', function (e) {
    params.amplitude = Number(e.target.value);
    document.getElementById('pgAmplitudeOut').textContent = params.amplitude.toFixed(2);
  });

  document.getElementById('pgDecay').addEventListener('input', function (e) {
    params.decay = Number(e.target.value);
    document.getElementById('pgDecayOut').textContent = params.decay.toFixed(3);
  });

  document.getElementById('hudReset').addEventListener('click', function () {
    sources.length = 0;
    updateStats();
  });

  document.getElementById('hudStandingWave').addEventListener('click', function () {
    standingWaveMode = !standingWaveMode;
    this.classList.toggle('active', standingWaveMode);
    this.style.borderColor = standingWaveMode ? 'var(--cohere)' : '';
    this.style.color = standingWaveMode ? 'var(--cohere)' : '';
  });

  document.getElementById('hudGuide').addEventListener('click', function () {
    document.getElementById('playgroundGuide').removeAttribute('hidden');
  });

  document.getElementById('guideClose').addEventListener('click', function () {
    document.getElementById('playgroundGuide').setAttribute('hidden', 'hidden');
  });

  document.getElementById('startPlaying').addEventListener('click', function () {
    document.body.classList.add('playing');
  });

  // ── Mouse interactions ────────────────────────────────────────────────────────

  function screenToCanvas(clientX, clientY) {
    return { x: clientX, y: clientY };
  }

  function findNearestSource(x, y) {
    var best = Infinity, bestIdx = -1;
    sources.forEach(function (s, i) {
      var d = Math.hypot(s.x - x, s.y - y);
      if (d < best) { best = d; bestIdx = i; }
    });
    return best < 30 ? bestIdx : -1;
  }

  canvas.addEventListener('click', function (e) {
    var pos = screenToCanvas(e.clientX, e.clientY);
    var idx = findNearestSource(pos.x, pos.y);
    if (idx >= 0) return; // don't double-fire with drag-end

    if (standingWaveMode) {
      addStandingWavePair(pos.x, pos.y);
    } else {
      addSource(pos.x, pos.y);
    }
  });

  canvas.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    var pos = screenToCanvas(e.clientX, e.clientY);
    removeNearest(pos.x, pos.y);
  });

  canvas.addEventListener('dblclick', function (e) {
    var pos = screenToCanvas(e.clientX, e.clientY);
    addStandingWavePair(pos.x, pos.y);
  });

  canvas.addEventListener('pointerdown', function (e) {
    if (e.button !== 0) return;
    var pos = screenToCanvas(e.clientX, e.clientY);
    draggingIndex = findNearestSource(pos.x, pos.y);
  });

  canvas.addEventListener('pointermove', function (e) {
    if (draggingIndex < 0) return;
    var pos = screenToCanvas(e.clientX, e.clientY);
    sources[draggingIndex].x = pos.x;
    sources[draggingIndex].y = pos.y;
    updateStats();
  });

  canvas.addEventListener('pointerup', function (e) {
    draggingIndex = -1;
  });

  canvas.addEventListener('pointerleave', function () {
    draggingIndex = -1;
  });

  // ── Wrong intuition callout logic ───────────────────────────────────────────

  var wrongCallouts = [
    {
      wrong: 'Matter is solid particles.',
      right: 'Matter is a stable self-reinforcing standing wave pattern.'
    },
    {
      wrong: 'Gravity is a force that pulls objects together.',
      right: 'Gravity is the refractive bending of propagation paths in a medium with density gradient.'
    },
    {
      wrong: 'Three generations of particles is arbitrary.',
      right: 'The current topology-plus-Koide story points to N=3, but the full generation lock is still conditional on unresolved bridge theorems.'
    }
  ];
  var calloutIndex = 0;

  function updateWrongCallout() {
    if (sources.length >= 2) {
      calloutIndex = 2; // generation topology
    } else if (sources.length === 1) {
      calloutIndex = sources.length === 1 ? 1 : 0;
    } else {
      calloutIndex = 0;
    }
    var c = wrongCallouts[calloutIndex];
    document.getElementById('wrongCalloutText').textContent = c.wrong;
    document.getElementById('rightCalloutText').textContent = c.right;
  }

  // ── Render loop ───────────────────────────────────────────────────────────────

  function render(timestamp) {
    var dt = Math.min((timestamp - lastTime) / 1000, 0.05);
    lastTime = timestamp;
    time += dt;

    gl.uniform1f(U.time, time);
    gl.uniform2f(U.resolution, canvas.width, canvas.height);
    uploadParams();
    uploadSources();

    gl.drawArrays(gl.TRIANGLES, 0, 6);

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);

  // ── Init ─────────────────────────────────────────────────────────────────────

  updateStats();
})();
