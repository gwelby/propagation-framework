/**
 * Bohr Panel — Enhanced with Wave Packet Phase Closure + Spectral Diagram
 * 
 * Shows the standing wave condition: ∮ n ds = 2πk
 * Wave packets propagate around the orbit. At integer k, they interfere
 * constructively and close perfectly. At non-integer k, they drift and fade.
 * 
 * NEW: Spectral Line Diagram
 * - Energy level diagram with E_k = -1/(4k²) levels
 * - Transition arrows showing photon emission/absorption
 * - Lyman, Balmer, Paschen series visualization
 * - Interactive: click level to view orbit, click transition for photon animation
 * 
 * The visualization shows:
 *   1. The orbit as a phase closure ring
 *   2. Animated wave packets at configurable k
 *   3. Standing wave nodes (where amplitude = 0) highlighted in magenta
 *   4. "LOCKED" indicator when k is integer ± tolerance
 *   5. Spectral energy diagram with transition series
 */
(function () {
  'use strict';

  function nearestInteger(value) {
    return Math.round(value);
  }

  // ── SPECTRAL DIAGRAM UTILITIES ────────────────────────────────────────────

  function calculateEnergyLevel(k) {
    // E_k = -1/(4k²) from the circular-eikonal Coulomb model
    return -1 / (4 * k * k);
  }

  function calculateRadius(k) {
    // r_k = 2k² from the circular-eikonal Coulomb model
    return 2 * k * k;
  }

  function wavelengthForTransition(kUpper, kLower) {
    // 1/λ = R_H * (1/n_lower² - 1/n_upper²)
    // Using k directly: ΔE = E_upper - E_lower = -1/(4k_upper²) - (-1/(4k_lower²))
    // Photon energy = -ΔE (emission)
    var eUpper = calculateEnergyLevel(kUpper);
    var eLower = calculateEnergyLevel(kLower);
    var deltaE = eLower - eUpper; // positive for emission (lower is more negative)
    if (deltaE <= 0) return null;
    // λ ∝ 1/ΔE (in atomic units)
    return 1 / deltaE;
  }

  function getSeriesName(kLower) {
    // n = 2k is the closure quantum number
    var n = 2 * kLower;
    switch (n) {
      case 2: return 'Lyman';
      case 4: return 'Balmer';
      case 6: return 'Paschen';
      case 8: return 'Brackett';
      default: return 'n=' + n;
    }
  }

  function getSeriesColor(kLower) {
    var n = 2 * kLower;
    switch (n) {
      case 2: return '#00cfff'; // Cyan - Lyman (UV)
      case 4: return '#44ff88'; // Green - Balmer (Visible)
      case 6: return '#ffdd55'; // Gold - Paschen (IR)
      case 8: return '#ff6b8a'; // Pink - Brackett (Far IR)
      default: return '#cccccc';
    }
  }

  // ── 3D BOHR VISUALIZATION ─────────────────────────────────────────────────

  function buildBohr3D(state) {
    var container = document.createElement('div');
    container.style.cssText = 'position:absolute;inset:0;';
    state.canvas.parentElement.appendChild(container);

    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    } catch (e) {
      console.warn("WebGL not supported, running in fallback mode:", e);
      container.innerHTML = '';
      var fallbackDiv = document.createElement('div');
      fallbackDiv.className = 'webgl-fallback';
      fallbackDiv.style.cssText = 'display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; min-height: 250px; border: 1px dashed rgba(232, 240, 255, 0.2); border-radius: 8px; background: rgba(9, 21, 37, 0.2); color: rgba(232, 240, 255, 0.8); text-align: center; padding: 20px; box-sizing: border-box;';
      fallbackDiv.innerHTML = '<h4 style="margin: 0 0 8px 0; color: #00cfff;">WebGL Not Supported</h4><p style="margin: 0; font-size: 12px; color: var(--muted); max-width: 280px; line-height: 1.4;">Standing wave phase-closure modes are calculated and plotted below in the spectral diagrams.</p>';
      container.appendChild(fallbackDiv);
      return {
        container: container,
        renderer: null,
        scene: null,
        camera: null,
        composer: null,
        _isFallback: true
      };
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    var w = state.canvas.parentElement.clientWidth || 640;
    var h = state.canvas.parentElement.clientHeight || 400;
    renderer.setSize(w, h, false);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.3;
    container.appendChild(renderer.domElement);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100);
    camera.position.set(0, 3, 12);
    camera.lookAt(0, 0, 0);

    scene.add(new THREE.AmbientLight(0x223355, 1.0));
    var dir = new THREE.DirectionalLight(0xffffff, 1.1);
    dir.position.set(5, 10, 8);
    scene.add(dir);

    // Nucleus (central charge)
    var nucleusGroup = new THREE.Group();
    var nucleusGeo = new THREE.SphereGeometry(0.8, 32, 32);
    var nucleusMat = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      emissive: 0xffaa00,
      emissiveIntensity: 0.8,
      metalness: 0.4,
      roughness: 0.3
    });
    var nucleus = new THREE.Mesh(nucleusGeo, nucleusMat);
    nucleusGroup.add(nucleus);
    
    // Add point light to nucleus
    var nucLight = new THREE.PointLight(0xffdd55, 2.0, 15);
    nucleusGroup.add(nucLight);
    
    // Add glow sprite to nucleus
    var canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;
    var ctx2d = canvas.getContext('2d');
    var grad = ctx2d.createRadialGradient(64, 64, 0, 64, 64, 64);
    grad.addColorStop(0, 'rgba(255, 200, 50, 1)');
    grad.addColorStop(0.2, 'rgba(255, 150, 0, 0.5)');
    grad.addColorStop(1, 'rgba(255, 100, 0, 0)');
    ctx2d.fillStyle = grad;
    ctx2d.fillRect(0, 0, 128, 128);
    var tex = new THREE.CanvasTexture(canvas);
    var spriteMat = new THREE.SpriteMaterial({ map: tex, color: 0xffffff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false });
    var glowSprite = new THREE.Sprite(spriteMat);
    glowSprite.scale.set(4, 4, 1);
    nucleusGroup.add(glowSprite);

    scene.add(nucleusGroup);

    // Orbit ring (the standing wave boundary)
    var orbitGeo = new THREE.TorusGeometry(4.5, 0.04, 8, 128);
    var orbitMat = new THREE.MeshStandardMaterial({
      color: 0x00cfff,
      emissive: 0x00cfff,
      emissiveIntensity: 0.2,
      transparent: true,
      opacity: 0.5
    });
    var orbitRing = new THREE.Mesh(orbitGeo, orbitMat);
    scene.add(orbitRing);

    // Wave packet ring (the animated traveling wave)
    var waveGeo = new THREE.TorusGeometry(4.5, 0.18, 12, 128);
    var waveMat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uK: { value: state.kLike },
        uColor: { value: new THREE.Color(0x00cfff) }
      },
      vertexShader: [
        'varying vec2 vUv;',
        'void main() {',
        '  vUv = uv;',
        '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform float uTime;',
        'uniform float uK;',
        'uniform vec3 uColor;',
        'varying vec2 vUv;',
        'void main() {',
        '  float angle = vUv.x * 2.0 * 3.14159265;',
        '  float phase = uK * angle - uTime * 2.5;',
        '  float wave = sin(phase) * 0.5 + 0.5;',
        '  // Node detection: where wave amplitude ≈ 0',
        '  float node = smoothstep(0.12, 0.0, abs(sin(phase)));',
        '  vec3 waveColor = mix(uColor, vec3(1.0, 0.2, 0.6), node * 0.8);',
        '  float alpha = 0.5 + 0.5 * wave;',
        '  gl_FragColor = vec4(waveColor, alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    var waveRing = new THREE.Mesh(waveGeo, waveMat);
    scene.add(waveRing);

    // Reference orbit rings (k=1,2,3,4 ghosts)
    [1, 2, 3, 4].forEach(function (k) {
      var refGeo = new THREE.TorusGeometry(4.5 * k / state.kLike, 0.03, 8, 64);
      var isNearest = k === nearestInteger(state.kLike);
      var refMat = new THREE.MeshStandardMaterial({
        color: isNearest ? 0x00cfff : 0x334466,
        emissive: isNearest ? 0x0088aa : 0x000000,
        transparent: true,
        opacity: isNearest ? 0.6 : 0.15
      });
      var refRing = new THREE.Mesh(refGeo, refMat);
      scene.add(refRing);
    });

    // Node markers (magenta dots at standing wave nodes)
    var nodeGroup = new THREE.Group();
    scene.add(nodeGroup);
    var nodeGeo = new THREE.SphereGeometry(0.12, 12, 12);
    var nodeMat = new THREE.MeshBasicMaterial({ color: 0xff6b8a });
    for (var n = 0; n < 16; n++) {
      var node = new THREE.Mesh(nodeGeo, nodeMat);
      nodeGroup.add(node);
    }

    // Bloom
    try {
      var composer = new THREE.EffectComposer(renderer);
      composer.setSize(w, h);
      composer.addPass(new THREE.RenderPass(scene, camera));
      var bloom = new THREE.UnrealBloomPass(
        new THREE.Vector2(w, h),
        2.0, 0.4, 0.82
      );
      composer.addPass(bloom);
      return { container: container, renderer: renderer, scene: scene, camera: camera, composer: composer,
        nucleus: nucleus, orbitRing: orbitRing, waveRing: waveRing, nodeGroup: nodeGroup };
    } catch (e) {
      return { container: container, renderer: renderer, scene: scene, camera: camera, composer: null,
        nucleus: nucleus, orbitRing: orbitRing, waveRing: waveRing, nodeGroup: nodeGroup };
    }
  }

  function updateBohr3D(r, state, time) {
    if (!r) return;

    var k = state.kLike;
    var nearest = nearestInteger(k);
    var stable = Math.abs(k - nearest) < 0.02;
    var orbitR = 4.5;

    // Update wave shader
    if (r.waveRing.material.uniforms) {
      r.waveRing.material.uniforms.uTime.value = time;
      r.waveRing.material.uniforms.uK.value = k;

      // Color: stable = cyan, unstable = orange-red
      var targetColor = stable ? new THREE.Color(0x00e5ff) : new THREE.Color(0xff7040);
      r.waveRing.material.uniforms.uColor.value.lerp(targetColor, 0.05);
    }

    // Orbit ring glow
    r.orbitRing.material.emissiveIntensity = stable ? 0.4 : 0.1;
    r.orbitRing.material.opacity = stable ? 0.7 : 0.3;

    // Nucleus pulse
    r.nucleus.material.emissiveIntensity = 0.5 + 0.2 * Math.sin(time * 2.0);

    // Node positions
    var nodeCount = Math.round(2 * k);
    r.nodeGroup.children.forEach(function (node, i) {
      if (i < nodeCount) {
        var angle = (i / nodeCount) * Math.PI * 2;
        node.position.set(
          orbitR * Math.cos(angle),
          orbitR * Math.sin(angle),
          0
        );
        node.visible = true;
      } else {
        node.visible = false;
      }
    });

    // Wave ring rotation (electron going around)
    r.waveRing.rotation.z = time * (stable ? 1.0 : 0.6);
    r.orbitRing.rotation.z = time * 0.05;

    // Camera gentle orbit
    r.camera.position.x = Math.sin(time * 0.2) * 2;
    r.camera.position.y = 3 + Math.cos(time * 0.15) * 0.5;
    r.camera.lookAt(0, 0, 0);

    if (r.composer) {
      r.composer.render();
    } else {
      r.renderer.render(r.scene, r.camera);
    }
  }

  function disposeBohr3D(r) {
    if (!r) return;
    window.removeEventListener('resize', r._resizeHandler);
    if (r._isFallback) {
      r.container.remove();
      return;
    }
    // Dispose every geometry/material reachable from the scene graph. This
    // covers the named meshes (nucleus, orbit ring, wave ring, node group)
    // AND the reference orbit rings added in the [1,2,3,4].forEach loop,
    // which a hand-written list previously missed.
    r.scene.traverse(function (obj) {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) obj.material.forEach(function (m) { m.dispose(); });
        else obj.material.dispose();
      }
    });
    if (r.composer && r.composer.dispose) r.composer.dispose();
    r.renderer.dispose();
    r.container.remove();
  }

  // ── SPECTRAL DIAGRAM ──────────────────────────────────────────────────────

  function createSpectralDiagram(state) {
    var container = document.createElement('div');
    container.id = 'spectralDiagram';
    container.className = 'spectral-diagram';
    container.style.cssText = 'width:100%;height:280px;background:#0a0a1a;border:1px solid #1a1a2e;border-radius:8px;position:relative;overflow:hidden;';

    // SVG for energy levels and transitions
    var svgNS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');
    svg.setAttribute('viewBox', '0 0 600 280');
    svg.style.cssText = 'position:absolute;top:0;left:0;';

    // Define gradients and filters
    var defs = document.createElementNS(svgNS, 'defs');
    defs.innerHTML = [
      '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">',
      '<feGaussianBlur stdDeviation="2" result="coloredBlur"/>',
      '<feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>',
      '</filter>',
      '<linearGradient id="photonGradient" x1="0%" y1="0%" x2="100%" y2="0%">',
      '<stop offset="0%" stop-color="#00cfff" stop-opacity="1"/>',
      '<stop offset="50%" stop-color="#ffdd55" stop-opacity="0.8"/>',
      '<stop offset="100%" stop-color="#00cfff" stop-opacity="1"/>',
      '</linearGradient>'
    ].join('');
    svg.appendChild(defs);

    // Title
    var title = document.createElementNS(svgNS, 'text');
    title.setAttribute('x', '300');
    title.setAttribute('y', '20');
    title.setAttribute('text-anchor', 'middle');
    title.setAttribute('fill', '#cccccc');
    title.setAttribute('font-size', '12');
    title.setAttribute('font-weight', 'bold');
    title.textContent = 'Energy Level Diagram — E_k = -1/(4k²)';
    svg.appendChild(title);

    // Energy axis label
    var yLabel = document.createElementNS(svgNS, 'text');
    yLabel.setAttribute('x', '15');
    yLabel.setAttribute('y', '140');
    yLabel.setAttribute('text-anchor', 'middle');
    yLabel.setAttribute('fill', '#666');
    yLabel.setAttribute('font-size', '10');
    yLabel.setAttribute('transform', 'rotate(-90, 15, 140)');
    yLabel.textContent = 'Energy (atomic units)';
    svg.appendChild(yLabel);

    // Draw energy levels (k = 1 to 6)
    var maxK = 6;
    var minEnergy = calculateEnergyLevel(1); // -0.25
    var maxEnergy = 0.05; // Just above zero
    var energyRange = maxEnergy - minEnergy;
    var levelX = 120;
    var levelWidth = 120;

    for (var k = 1; k <= maxK; k++) {
      var energy = calculateEnergyLevel(k);
      var y = 240 - ((energy - minEnergy) / energyRange) * 200;
      var n = 2 * k; // closure quantum number
      var color = getSeriesColor(k);

      // Energy level line
      var line = document.createElementNS(svgNS, 'line');
      line.setAttribute('x1', levelX);
      line.setAttribute('y1', y);
      line.setAttribute('x2', levelX + levelWidth);
      line.setAttribute('y2', y);
      line.setAttribute('stroke', color);
      line.setAttribute('stroke-width', k === nearestInteger(state.kLike) ? '3' : '2');
      line.setAttribute('filter', 'url(#glow)');
      line.setAttribute('class', 'energy-level');
      line.setAttribute('data-k', k);
      line.style.cursor = 'pointer';
      line.style.transition = 'all 0.3s';
      svg.appendChild(line);

      // Level label (k and n)
      var label = document.createElementNS(svgNS, 'text');
      label.setAttribute('x', levelX - 10);
      label.setAttribute('y', y + 4);
      label.setAttribute('text-anchor', 'end');
      label.setAttribute('fill', color);
      label.setAttribute('font-size', '11');
      label.setAttribute('font-weight', 'bold');
      label.textContent = 'k=' + k + ' (n=' + n + ')';
      svg.appendChild(label);

      // Energy value
      var eLabel = document.createElementNS(svgNS, 'text');
      eLabel.setAttribute('x', levelX + levelWidth + 10);
      eLabel.setAttribute('y', y + 4);
      eLabel.setAttribute('fill', '#888');
      eLabel.setAttribute('font-size', '9');
      eLabel.textContent = energy.toFixed(4);
      svg.appendChild(eLabel);

      // Radius annotation
      var rLabel = document.createElementNS(svgNS, 'text');
      rLabel.setAttribute('x', levelX + levelWidth + 60);
      rLabel.setAttribute('y', y + 4);
      rLabel.setAttribute('fill', '#666');
      rLabel.setAttribute('font-size', '8');
      rLabel.textContent = 'r=' + calculateRadius(k).toFixed(1);
      svg.appendChild(rLabel);
    }

    // Draw zero energy line (ionization threshold)
    var zeroY = 240 - ((0 - minEnergy) / energyRange) * 200;
    var zeroLine = document.createElementNS(svgNS, 'line');
    zeroLine.setAttribute('x1', levelX - 20);
    zeroLine.setAttribute('y1', zeroY);
    zeroLine.setAttribute('x2', levelX + levelWidth + 100);
    zeroLine.setAttribute('y2', zeroY);
    zeroLine.setAttribute('stroke', '#444');
    zeroLine.setAttribute('stroke-width', '1');
    zeroLine.setAttribute('stroke-dasharray', '4,2');
    svg.appendChild(zeroLine);

    var zeroLabel = document.createElementNS(svgNS, 'text');
    zeroLabel.setAttribute('x', levelX + levelWidth + 105);
    zeroLabel.setAttribute('y', zeroY + 3);
    zeroLabel.setAttribute('fill', '#666');
    zeroLabel.setAttribute('font-size', '9');
    zeroLabel.textContent = 'E=0 (ionization)';
    svg.appendChild(zeroLabel);

    // Draw transition series (Lyman: n→1, Balmer: n→2, Paschen: n→3)
    var transitionGroup = document.createElementNS(svgNS, 'g');
    transitionGroup.id = 'transitions';

    function drawTransition(kUpper, kLower, xOffset, opacity) {
      var eUpper = calculateEnergyLevel(kUpper);
      var eLower = calculateEnergyLevel(kLower);
      var yUpper = 240 - ((eUpper - minEnergy) / energyRange) * 200;
      var yLower = 240 - ((eLower - minEnergy) / energyRange) * 200;
      var x = levelX + levelWidth + xOffset;
      var color = getSeriesColor(kLower);
      var seriesName = getSeriesName(kLower);

      // Transition arrow (wavy line for photon)
      var arrow = document.createElementNS(svgNS, 'path');
      var midY = (yUpper + yLower) / 2;
      var waveAmp = 3;
      var path = 'M' + x + ',' + yUpper + ' Q' + (x + waveAmp) + ',' + (yUpper + (yLower - yUpper) * 0.25) + ' ' + x + ',' + midY + ' Q' + (x - waveAmp) + ',' + (yUpper + (yLower - yUpper) * 0.75) + ' ' + x + ',' + yLower;
      arrow.setAttribute('d', path);
      arrow.setAttribute('stroke', color);
      arrow.setAttribute('stroke-width', '2');
      arrow.setAttribute('fill', 'none');
      arrow.setAttribute('opacity', opacity);
      arrow.setAttribute('marker-end', 'url(#arrowhead)');
      arrow.setAttribute('class', 'transition-arrow');
      arrow.setAttribute('data-from', kUpper);
      arrow.setAttribute('data-to', kLower);
      arrow.style.cursor = 'pointer';
      transitionGroup.appendChild(arrow);

      // Photon wavelength annotation
      var lambda = wavelengthForTransition(kUpper, kLower);
      if (lambda) {
        var lambdaLabel = document.createElementNS(svgNS, 'text');
        lambdaLabel.setAttribute('x', x + 10);
        lambdaLabel.setAttribute('y', midY);
        lambdaLabel.setAttribute('fill', color);
        lambdaLabel.setAttribute('font-size', '8');
        lambdaLabel.setAttribute('opacity', opacity);
        lambdaLabel.textContent = 'λ~' + lambda.toFixed(1);
        transitionGroup.appendChild(lambdaLabel);
      }
    }

    // Draw series
    // Lyman series (transitions to k=1, n=2)
    for (var ku = 2; ku <= 5; ku++) {
      drawTransition(ku, 1, 40 + (ku - 2) * 25, state.showAllSeries ? 0.8 : 0.15);
    }

    // Balmer series (transitions to k=2, n=4) 
    if (state.showAllSeries || state.activeSeries === 'balmer') {
      for (var ku = 3; ku <= 6; ku++) {
        drawTransition(ku, 2, 140 + (ku - 3) * 25, state.showAllSeries ? 0.6 : 0.8);
      }
    }

    // Paschen series (transitions to k=3, n=6)
    if (state.showAllSeries || state.activeSeries === 'paschen') {
      for (var ku = 4; ku <= 6; ku++) {
        drawTransition(ku, 3, 220 + (ku - 4) * 20, state.showAllSeries ? 0.5 : 0.8);
      }
    }

    svg.appendChild(transitionGroup);

    // Series legend
    var legendY = 50;
    var series = [
      { name: 'Lyman (n→2)', color: '#00cfff', desc: 'UV' },
      { name: 'Balmer (n→4)', color: '#44ff88', desc: 'Visible' },
      { name: 'Paschen (n→6)', color: '#ffdd55', desc: 'IR' }
    ];
    series.forEach(function(s, i) {
      var ly = legendY + i * 18;
      var rect = document.createElementNS(svgNS, 'rect');
      rect.setAttribute('x', '480');
      rect.setAttribute('y', ly - 6);
      rect.setAttribute('width', '12');
      rect.setAttribute('height', '12');
      rect.setAttribute('fill', s.color);
      rect.setAttribute('rx', '2');
      svg.appendChild(rect);

      var text = document.createElementNS(svgNS, 'text');
      text.setAttribute('x', '498');
      text.setAttribute('y', ly + 3);
      text.setAttribute('fill', '#aaa');
      text.setAttribute('font-size', '9');
      text.textContent = s.name + ' ' + s.desc;
      svg.appendChild(text);
    });

    // Photon animation circle (hidden initially)
    var photon = document.createElementNS(svgNS, 'circle');
    photon.id = 'photon';
    photon.setAttribute('r', '5');
    photon.setAttribute('fill', 'url(#photonGradient)');
    photon.setAttribute('filter', 'url(#glow)');
    photon.setAttribute('opacity', '0');
    svg.appendChild(photon);

    container.appendChild(svg);

    // Click handlers for energy levels
    container.querySelectorAll('.energy-level').forEach(function(line) {
      line.addEventListener('click', function() {
        var k = parseInt(line.getAttribute('data-k'));
        state.kLike = k;
        state.spectralLevelClicked = k;
        PFExplorer.state.activePanel.renderInfo(PFExplorer.state.activePanel.ctx);
      });
      line.addEventListener('mouseenter', function() {
        line.setAttribute('stroke-width', '4');
      });
      line.addEventListener('mouseleave', function() {
        var k = parseInt(line.getAttribute('data-k'));
        line.setAttribute('stroke-width', k === nearestInteger(state.kLike) ? '3' : '2');
      });
    });

    // Click handlers for transitions
    container.querySelectorAll('.transition-arrow').forEach(function(arrow) {
      arrow.addEventListener('click', function() {
        var kFrom = parseInt(arrow.getAttribute('data-from'));
        var kTo = parseInt(arrow.getAttribute('data-to'));
        animatePhotonEmission(container, kFrom, kTo, minEnergy, energyRange);
      });
    });

    return container;
  }

  function animatePhotonEmission(container, kFrom, kTo, minEnergy, energyRange) {
    var photon = container.querySelector('#photon');
    var eFrom = calculateEnergyLevel(kFrom);
    var eTo = calculateEnergyLevel(kTo);
    var levelX = 120;
    var levelWidth = 120;

    var yFrom = 240 - ((eFrom - minEnergy) / energyRange) * 200;
    var yTo = 240 - ((eTo - minEnergy) / energyRange) * 200;
    var x = levelX + levelWidth + 40;

    // Simple animation using requestAnimationFrame
    var startTime = performance.now();
    var duration = 1000;

    photon.setAttribute('opacity', '1');

    function step(now) {
      var elapsed = now - startTime;
      var progress = Math.min(elapsed / duration, 1);
      var y = yFrom + (yTo - yFrom) * progress;

      photon.setAttribute('cx', x);
      photon.setAttribute('cy', y);

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        // Fade out
        setTimeout(function() {
          photon.setAttribute('opacity', '0');
        }, 200);
      }
    }

    requestAnimationFrame(step);
  }

  function updateSpectralDiagram(state) {
    var container = document.getElementById('spectralDiagram');
    if (!container) return;

    // Update highlight based on current k
    var lines = container.querySelectorAll('.energy-level');
    lines.forEach(function(line) {
      var k = parseInt(line.getAttribute('data-k'));
      line.setAttribute('stroke-width', k === nearestInteger(state.kLike) ? '3' : '2');
    });
  }

  // ── PANEL REGISTRATION ────────────────────────────────────────────────────

  window.PFExplorer.registerPanel({
    id: 'bohr',
    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="panel-wrap">' +
          '<div class="panel-atlas">' +
            '<section class="canvas-panel" style="position:relative">' +
              '<div class="panel-header">' +
                '<div>' +
                  '<p class="eyebrow"><span style="color:#ffaa33; font-family:serif; margin-right:8px;">ψ</span> Phase Closure Orbit</p>' +
                  '<h3><span style="color:#44ff88; font-family:serif; margin-right:8px;">◈</span> Only integer winding survives. Everything else fades.</h3>' +
                  '<p>The slider moves through continuous k-like radii. Stable orbits glow at integer winding numbers, representing the fundamental standing wave condition.</p>' +
                  '<p class="interaction-cue"><strong>Interaction:</strong> Drag the slider to vary the orbit radius. Observe how only integer winding numbers (k) survive phase closure.</p>' +
                '</div>' +
              '</div>' +
              '<canvas class="panel-canvas" id="bohrCanvas" style="position:absolute;inset:0;width:100%;height:100%"></canvas>' +
              '<div class="canvas-overlay"></div>' +
            '</section>' +
            '<section class="info-panel" id="bohrInfo"></section>' +
          '</div>' +
        '</div>';

      this.state = {
        canvas: ctx.stage.querySelector('#bohrCanvas'),
        info: ctx.stage.querySelector('#bohrInfo'),
        kLike: 1,
        phase: 0,
        showAllSeries: false,
        activeSeries: 'balmer',
        spectralLevelClicked: null,
        ctx: ctx
      };

      this.renderInfo(ctx);
    },

    unmount: function () {
      disposeBohr3D(this.state._3d);
      this.state = null;
    },

    resize: function (ctx) {
      var state = this.state;
      if (!state || !state._3d || state._3d._isFallback) return;
      var r = state._3d;
      var w = state.canvas.parentElement.clientWidth;
      var h = state.canvas.parentElement.clientHeight;
      if (w < 2 || h < 2) return;  // DOM not laid out yet; skip cleanly.
      r.camera.aspect = w / h;
      r.camera.updateProjectionMatrix();
      r.renderer.setSize(w, h, false);
      if (r.composer) r.composer.setSize(w, h);
    },

    renderInfo: function (ctx) {
      var state = this.state;
      var nearest = nearestInteger(state.kLike);
      var radius = 2 * state.kLike * state.kLike;
      var energy = -1 / (4 * state.kLike * state.kLike);
      var phaseValue = 2 * Math.PI * state.kLike;
      var mismatch = Math.abs(state.kLike - nearest);
      var errorPct = nearest === state.kLike ? 0 : Math.abs(phaseValue - 2 * Math.PI * nearest) / (2 * Math.PI * nearest) * 100;
      var stable = mismatch < 0.02;
      var statusColor = stable ? 'var(--cohere)' : 'var(--resonate)';

      // Build spectral diagram section
      var spectralSection = '<div class="spectral-section" style="margin:16px 0;padding:12px;background:#0f0f1a;border:1px solid #1a1a2e;border-radius:8px;">';
      spectralSection += '<h4 style="margin:0 0 12px 0;color:#cccccc;font-size:13px;">Bohr-like Spectrum: 1/k² Energy Levels</h4>';
      spectralSection += '<div id="spectralContainer"></div>';
      spectralSection += '<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">';
      spectralSection += '<button type="button" class="chip-button" id="toggleSeries">' + (state.showAllSeries ? 'Show Active Only' : 'Show All Series') + '</button>';
      spectralSection += '<button type="button" class="chip-button" data-series="balmer">Balmer (Visible)</button>';
      spectralSection += '<button type="button" class="chip-button" data-series="paschen">Paschen (IR)</button>';
      spectralSection += '</div>';
      spectralSection += '<p style="margin:10px 0 0 0;color:#888;font-size:10px;line-height:1.4;">';
      spectralSection += '<strong>Click</strong> an energy level to view that orbit. <strong>Click</strong> a transition arrow to animate photon emission. ';
      spectralSection += 'The circular-eikonal model yields r_k = 2k² and E_k = -1/(4k²), a Bohr-like 1/k² spectrum.';
      spectralSection += '</p></div>';

      state.info.innerHTML =
        '<div class="panel-header">' +
          '<div>' +
            '<p class="eyebrow">Integer winding</p>' +
            '<h3 style="color:' + statusColor + '">k = ' + state.kLike.toFixed(2) + (stable ? ' — LOCKED' : '') + '</h3>' +
            '<p>The panel uses exact repo formulas so integer k reproduces zero closure error rather than approximating it numerically.</p>' +
          '</div>' +
          (function() {
            var claim = window.PFTruth && window.PFTruth.getClaim ? window.PFTruth.getClaim('bohr-spectrum') : null;
            var badge = claim ? (claim.badge || claim.status) : 'UNAVAILABLE';
            var cls = claim ? (claim.statusClass || 'status-derived') : 'status-derived';
            return '<span class="status-pill ' + cls + '">' + badge + '</span>';
          })() +
        '</div>' +
        ctx.app.renderWrongIntuition(ctx.app.getResult('bohr-quantization')) +
        '<div class="control-group">' +
          '<label for="bohrK">Continuous winding k</label>' +
          '<input id="bohrK" class="premium-slider" type="range" min="0.8" max="4.2" step="0.01" value="' + state.kLike + '">' +
          '<output id="bohrKOut">k = ' + state.kLike.toFixed(2) + '</output>' +
        '</div>' +
        '<div class="metric-row">' +
          '<button class="chip-button" type="button" data-k="1">k = 1</button>' +
          '<button class="chip-button" type="button" data-k="2">k = 2</button>' +
          '<button class="chip-button" type="button" data-k="3">k = 3</button>' +
          '<button class="chip-button" type="button" data-k="4">k = 4</button>' +
        '</div>' +
        spectralSection +
        '<div class="formula">r_k = 2k^2,  E_k = -1/(4k^2),  integral n ds = 2pi k</div>' +
        '<div class="stat-grid">' +
          '<div class="stat-tile"><strong>' + radius.toFixed(3) + '</strong><span>radius</span></div>' +
          '<div class="stat-tile"><strong>' + energy.toFixed(5) + '</strong><span>energy</span></div>' +
          '<div class="stat-tile"><strong>' + (mismatch < 1e-8 ? '0.0000%' : errorPct.toFixed(3) + '%') + '</strong><span>closure error</span></div>' +
          '<div class="stat-tile"><strong style="color:' + statusColor + '">' + (stable ? 'STABLE' : 'DRIFTING') + '</strong><span>orbit status</span></div>' +
        '</div>' +
        '<div class="note-box story-only"><strong>Story</strong><p>' + (stable
          ? 'The orbit is phase-locked because the wave closes on itself after exactly k circuits. This is why atoms have discrete energy levels — they are standing wave conditions, not orbiting particles.'
          : 'The orbit misses perfect closure. After each circuit the phase has drifted slightly, so the pattern disperses over time. No stable atom at this k.') + '</p></div>' +
        '<div class="note-box audit-only"><strong>Audit</strong><p>Current repo status is conditional, not derived from Axiom 3 alone. At integer k the panel reports exact formula-level closure inside the named model layer. The Bohr-like spectrum emerges from the circular-eikonal Coulomb model with phase closure.</p></div>';

      // Add event listeners
      state.info.querySelector('#bohrK').addEventListener('input', function (e) {
        state.kLike = Number(e.target.value);
        updateSpectralDiagram(state);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });

      Array.prototype.forEach.call(state.info.querySelectorAll('[data-k]'), function (btn) {
        btn.addEventListener('click', function () {
          state.kLike = Number(btn.getAttribute('data-k'));
          updateSpectralDiagram(state);
          PFExplorer.state.activePanel.renderInfo(ctx);
        });
      });

      // Series toggle
      var toggleBtn = state.info.querySelector('#toggleSeries');
      if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
          state.showAllSeries = !state.showAllSeries;
          PFExplorer.state.activePanel.renderInfo(ctx);
        });
      }

      // Series selector buttons
      Array.prototype.forEach.call(state.info.querySelectorAll('[data-series]'), function (btn) {
        btn.addEventListener('click', function () {
          state.activeSeries = btn.getAttribute('data-series');
          state.showAllSeries = false;
          PFExplorer.state.activePanel.renderInfo(ctx);
        });
      });

      // Initialize 3D if needed
      if (!state._3d) {
        state._3d = buildBohr3D(state);
        var self = this;
        state._3d._resizeHandler = function () { self.resize(ctx); };
        window.addEventListener('resize', state._3d._resizeHandler);
        // Snap the renderer to the current panel size on first mount. The
        // initial size baked into buildBohr3D is just a safety floor; the
        // real dimensions only become available after the DOM lays out.
        self.resize(ctx);
      }

      // Create and inject spectral diagram
      var spectralContainer = state.info.querySelector('#spectralContainer');
      if (spectralContainer) {
        var diagram = createSpectralDiagram(state);
        spectralContainer.appendChild(diagram);
      }
    },

    update: function (ctx, dt, time) {
      if (!this.state._3d || this.state._3d._isFallback) return;
      updateBohr3D(this.state._3d, this.state, time);
    }
  });
}());
