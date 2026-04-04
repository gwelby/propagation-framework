/**
 * Bohr Panel — Enhanced with Wave Packet Phase Closure
 * 
 * Shows the standing wave condition: ∮ n ds = 2πk
 * Wave packets propagate around the orbit. At integer k, they interfere
 * constructively and close perfectly. At non-integer k, they drift and fade.
 * 
 * The visualization shows:
 *   1. The orbit as a phase closure ring
 *   2. Animated wave packets at configurable k
 *   3. Standing wave nodes (where amplitude = 0) highlighted in magenta
 *   4. "LOCKED" indicator when k is integer ± tolerance
 */
(function () {
  'use strict';

  function nearestInteger(value) {
    return Math.round(value);
  }

  function buildBohr3D(state) {
    var container = document.createElement('div');
    container.style.cssText = 'position:absolute;inset:0;';
    state.canvas.parentElement.appendChild(container);

    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.3;
    container.appendChild(renderer.domElement);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
    camera.position.set(0, 3, 12);
    camera.lookAt(0, 0, 0);

    scene.add(new THREE.AmbientLight(0x223355, 1.0));
    var dir = new THREE.DirectionalLight(0xffffff, 1.1);
    dir.position.set(5, 10, 8);
    scene.add(dir);

    // Nucleus (central charge)
    var nucleusGeo = new THREE.SphereGeometry(0.8, 32, 32);
    var nucleusMat = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      emissive: 0xffd700,
      emissiveIntensity: 0.6,
      metalness: 0.4,
      roughness: 0.3
    });
    var nucleus = new THREE.Mesh(nucleusGeo, nucleusMat);
    scene.add(nucleus);

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
        uColor: { value: new THREE.Color(0x00e5ff) }
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
        '  float node = smoothstep(0.08, 0.0, abs(sin(phase)));',
        '  vec3 waveColor = mix(uColor, vec3(1.0, 0.42, 0.71), node * 0.6);',
        '  float alpha = 0.6 + 0.3 * wave;',
        '  gl_FragColor = vec4(waveColor, alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.DoubleSide,
      depthWrite: false
    });
    var waveRing = new THREE.Mesh(waveGeo, waveMat);
    scene.add(waveRing);

    // Reference orbit rings (k=1,2,3,4 ghosts)
    [1, 2, 3, 4].forEach(function (k) {
      var refGeo = new THREE.TorusGeometry(4.5 * k / state.kLike, 0.03, 8, 64);
      var refMat = new THREE.MeshBasicMaterial({
        color: k === nearestInteger(state.kLike) ? 0xffdd55 : 0x334466,
        transparent: true,
        opacity: k === nearestInteger(state.kLike) ? 0.3 : 0.08
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
      composer.addPass(new THREE.RenderPass(scene, camera));
      var bloom = new THREE.UnrealBloomPass(
        new THREE.Vector2(state.canvas.clientWidth || 400, state.canvas.clientHeight || 300),
        0.5, 0.4, 0.82
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
    r.waveRing.geometry.dispose();
    r.waveRing.material.dispose();
    r.orbitRing.geometry.dispose();
    r.orbitRing.material.dispose();
    r.nucleus.geometry.dispose();
    r.nucleus.material.dispose();
    r.nodeGroup.children.forEach(function (n) { n.geometry.dispose(); n.material.dispose(); });
    if (r.composer) r.renderer.dispose();
    r.container.remove();
  }

  // ── Panel Registration ───────────────────────────────────────────────────

  window.PFExplorer.registerPanel({
    id: 'bohr',
    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="panel-wrap">' +
          '<div class="panel-atlas">' +
            '<section class="canvas-panel" style="position:relative">' +
              '<div class="panel-header">' +
                '<div>' +
                  '<p class="eyebrow">Phase Closure Orbit</p>' +
                  '<h3>Only integer winding survives. Everything else fades.</h3>' +
                  '<p>The slider moves through continuous k-like radii. Stable orbits glow at integer winding.</p>' +
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
        phase: 0
      };

      this.renderInfo(ctx);
    },

    unmount: function () {
      disposeBohr3D(this.state._3d);
      this.state = null;
    },

    resize: function (ctx) {
      var state = this.state;
      if (state._3d) {
        var w = state.canvas.clientWidth, h = state.canvas.clientHeight;
        state._3d.camera.aspect = w / h;
        state._3d.camera.updateProjectionMatrix();
        state._3d.renderer.setSize(w, h);
        if (state._3d.composer) state._3d.composer.setSize(w, h);
      }
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

      state.info.innerHTML =
        '<div class="panel-header">' +
          '<div>' +
            '<p class="eyebrow">Integer winding</p>' +
            '<h3 style="color:' + statusColor + '">k = ' + state.kLike.toFixed(2) + (stable ? ' — LOCKED' : '') + '</h3>' +
            '<p>The panel uses exact repo formulas so integer k reproduces zero closure error rather than approximating it numerically.</p>' +
          '</div>' +
          '<span class="status-pill status-conditional">CONDITIONAL</span>' +
        '</div>' +
        ctx.app.renderWrongIntuition(ctx.app.getResult('bohr-quantization')) +
        '<div class="control-group">' +
          '<label for="bohrK">Continuous winding k</label>' +
          '<input id="bohrK" type="range" min="0.8" max="4.2" step="0.01" value="' + state.kLike + '">' +
          '<output id="bohrKOut">k = ' + state.kLike.toFixed(2) + '</output>' +
        '</div>' +
        '<div class="metric-row">' +
          '<button class="chip-button" type="button" data-k="1">k = 1</button>' +
          '<button class="chip-button" type="button" data-k="2">k = 2</button>' +
          '<button class="chip-button" type="button" data-k="3">k = 3</button>' +
          '<button class="chip-button" type="button" data-k="4">k = 4</button>' +
        '</div>' +
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
        '<div class="note-box audit-only"><strong>Audit</strong><p>Current repo status is conditional, not derived from Axiom 3 alone. At integer k the panel reports exact formula-level closure inside the named model layer.</p></div>';

      state.info.querySelector('#bohrK').addEventListener('input', function (e) {
        state.kLike = Number(e.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      Array.prototype.forEach.call(state.info.querySelectorAll('[data-k]'), function (btn) {
        btn.addEventListener('click', function () {
          state.kLike = Number(btn.getAttribute('data-k'));
          PFExplorer.state.activePanel.renderInfo(ctx);
        });
      });

      if (!state._3d) {
        state._3d = buildBohr3D(state);
        var self = this;
        state._3d._resizeHandler = function () {
          var w = state.canvas.clientWidth, h = state.canvas.clientHeight;
          state._3d.camera.aspect = w / h;
          state._3d.camera.updateProjectionMatrix();
          state._3d.renderer.setSize(w, h);
          if (state._3d.composer) state._3d.composer.setSize(w, h);
        };
        window.addEventListener('resize', state._3d._resizeHandler);
      }
    },

    update: function (ctx, dt, time) {
      if (!this.state._3d) return;
      updateBohr3D(this.state._3d, this.state, time);
    }
  });
}());
