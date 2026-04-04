/**
 * God Equation Panel — Three.js Upgrade
 * 
 * Shows the exponential ladder from Planck to Matter.
 * Three.js visualization: exponential N^(D/2) surface with (3,3) anchor highlighted.
 * Log-scale slider for N (generations) and D (spatial dimensions).
 */
(function () {
  'use strict';

  var LP = 1.616e-35;
  var OBSERVED = 1.14e-18;
  var CLAIM_ANCHOR = 1.145e-18;

  function b0ForN(n) {
    return (22 - 2 * n) / 3;
  }

  function exponentFor(n, d) {
    var b0 = b0ForN(n);
    if (b0 <= 0) return null;
    return (4 * Math.PI * Math.PI * Math.pow(n, d / 2)) / b0;
  }

  function lambdaFor(n, d) {
    var exp = exponentFor(n, d);
    var anchorExp = exponentFor(3, 3);
    if (exp == null || anchorExp == null) return null;
    return CLAIM_ANCHOR * Math.exp(exp - anchorExp);
  }

  function sourceListHtml(sources) {
    return (
      '<div class="source-list">' +
        sources.map(function (s) {
          return '<a href="' + s.href + '" target="_blank" rel="noreferrer">' + s.label + '</a>';
        }).join('') +
      '</div>'
    );
  }

  function dependencyChainHtml(chain) {
    return (
      '<div class="audit-chain">' +
        chain.map(function (step, i) {
          return (
            (i ? '<span class="audit-chain-arrow">&#8594;</span>' : '') +
            '<div class="audit-chain-step is-' + step.state + '">' +
              '<strong>' + step.label + '</strong>' +
              '<span>' + step.note + '</span>' +
            '</div>'
          );
        }).join('') +
      '</div>'
    );
  }

  function gapCardsHtml(gaps) {
    return (
      '<div class="audit-gap-grid">' +
        gaps.map(function (gap) {
          return (
            '<article class="audit-gap-card">' +
              '<div class="gap-card-head">' +
                '<div class="gap-heading">' +
                  '<span class="gap-letter">' + gap.id + '</span>' +
                  '<div><h4>' + gap.title + '</h4><p>' + gap.need + '</p></div>' +
                '</div>' +
                '<span class="gap-verdict">' + gap.verdict + '</span>' +
              '</div>' +
              '<div class="mini-audit-block">' +
                '<span class="eyebrow">What survives</span>' +
                '<p>' + gap.survives + '</p>' +
              '</div>' +
              '<div class="mini-audit-block">' +
                '<span class="eyebrow">Why it remains open</span>' +
                '<p>' + gap.detail + '</p>' +
              '</div>' +
              '<div class="mini-audit-block">' +
                '<span class="eyebrow">Source trail</span>' +
                sourceListHtml(gap.sources) +
              '</div>' +
            '</article>'
          );
        }).join('') +
      '</div>'
    );
  }

  // ── Three.js God Equation Renderer ─────────────────────────────────────────

  function createRenderer3D(stage) {
    var container = document.createElement('div');
    container.style.cssText = 'position:absolute;inset:0;';
    stage.appendChild(container);

    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(40, 1, 0.1, 1000);
    camera.position.set(0, 8, 20);
    camera.lookAt(0, 0, 0);

    scene.add(new THREE.AmbientLight(0x223355, 0.8));
    var dir = new THREE.DirectionalLight(0xffffff, 1.0);
    dir.position.set(5, 15, 10);
    scene.add(dir);
    var fill = new THREE.PointLight(0x00cfff, 0.4, 50);
    fill.position.set(-8, 5, 5);
    scene.add(fill);

    // Exponential surface: λ(N,D) = exp(N^(D/2))
    // We'll show it as a 3D parametric surface
    var geometry = new THREE.BufferGeometry();
    var nSegments = 40, dSegments = 40;
    var positions = [];
    var colors = [];

    function computeHeight(n, d) {
      var exp = exponentFor(Math.round(n), Math.round(d));
      if (exp == null) return 0;
      // Normalize: range from 0 (Planck) to 1 (observed matter)
      var anchorExp = exponentFor(3, 3);
      if (anchorExp == null) return 0;
      var delta = exp - anchorExp;
      return Math.exp(delta * 0.3); // scale factor for visibility
    }

    for (var i = 0; i <= nSegments; i++) {
      for (var j = 0; j <= dSegments; j++) {
        var n = 1 + (i / nSegments) * 4;  // N from 1 to 5
        var d = 1 + (j / dSegments) * 4;  // D from 1 to 5
        var h = computeHeight(n, d);
        var x = (n - 1) / 4 * 10 - 5; // map to -5..5
        var z = (d - 1) / 4 * 10 - 5;
        var y = h * 4; // height scale

        positions.push(x, y, z);

        // Color: near (3,3) = cyan/green, far = violet
        var distTo33 = Math.sqrt((n - 3) ** 2 + (d - 3) ** 2);
        var t = Math.min(1, distTo33 / 4);
        var r = Math.floor(0 + 100 * t);
        var g = Math.floor(229 - 100 * t);
        var b = 255;
        colors.push(r / 255, g / 255, b / 255);
      }
    }

    var indices = [];
    for (var ii = 0; ii < nSegments; ii++) {
      for (var jj = 0; jj < dSegments; jj++) {
        var a = ii * (dSegments + 1) + jj;
        var b = a + 1;
        var c = a + (dSegments + 1);
        var d = c + 1;
        indices.push(a, c, b, b, c, d);
      }
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();

    var material = new THREE.MeshStandardMaterial({
      vertexColors: true,
      metalness: 0.5,
      roughness: 0.4,
      side: THREE.DoubleSide
    });
    var surface = new THREE.Mesh(geometry, material);
    scene.add(surface);

    // Anchor point at (3,3) — the God Equation landing
    var anchorGeo = new THREE.SphereGeometry(0.4, 24, 24);
    var anchorMat = new THREE.MeshStandardMaterial({
      color: 0x00e5ff,
      emissive: 0x00e5ff,
      emissiveIntensity: 1.0,
      metalness: 0.3,
      roughness: 0.2
    });
    var anchorMesh = new THREE.Mesh(anchorGeo, anchorMat);
    scene.add(anchorMesh);

    // Anchor glow ring
    var anchorRingGeo = new THREE.TorusGeometry(0.8, 0.06, 8, 32);
    var anchorRingMat = new THREE.MeshBasicMaterial({
      color: 0x00e5ff,
      transparent: true,
      opacity: 0.6
    });
    var anchorRing = new THREE.Mesh(anchorRingGeo, anchorRingMat);
    scene.add(anchorRing);

    // Particle dots along the exp curve
    var particleCount = 300;
    var pPositions = new Float32Array(particleCount * 3);
    for (var p = 0; p < particleCount; p++) {
      var pn = 1 + Math.random() * 4;
      var pd = 1 + Math.random() * 4;
      var ph = computeHeight(pn, pd) * 4;
      pPositions[p * 3] = (pn - 1) / 4 * 10 - 5;
      pPositions[p * 3 + 1] = ph;
      pPositions[p * 3 + 2] = (pd - 1) / 4 * 10 - 5;
    }
    var pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute('position', new THREE.BufferAttribute(pPositions, 3));
    var pMat = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.08,
      transparent: true,
      opacity: 0.4
    });
    var particles = new THREE.Points(pGeo, pMat);
    scene.add(particles);

    // Axes
    function addAxis(from, to, color) {
      var axGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3().fromArray(from),
        new THREE.Vector3().fromArray(to)
      ]);
      var axMat = new THREE.LineBasicMaterial({ color: color, transparent: true, opacity: 0.4 });
      scene.add(new THREE.Line(axGeo, axMat));
    }
    addAxis([-5, -0.5, -5], [5, -0.5, -5], 0x444466); // N axis
    addAxis([-5, -0.5, -5], [-5, 6, -5], 0x444466);   // D axis

    // Bloom
    try {
      var composer = new THREE.EffectComposer(renderer);
      composer.addPass(new THREE.RenderPass(scene, camera));
      var bloom = new THREE.UnrealBloomPass(
        new THREE.Vector2(container.clientWidth || 640, container.clientHeight || 400),
        0.5, 0.35, 0.82
      );
      composer.addPass(bloom);
      return { container: container, renderer: renderer, scene: scene, camera: camera, composer: composer,
        surface: surface, anchorMesh: anchorMesh, anchorRing: anchorRing, particles: particles };
    } catch (e) {
      return { container: container, renderer: renderer, scene: scene, camera: camera, composer: null,
        surface: surface, anchorMesh: anchorMesh, anchorRing: anchorRing, particles: particles };
    }
  }

  function updateGod3D(r, state, time) {
    if (!r) return;

    var n = state.nValue;
    var d = state.dValue;
    var pred = lambdaFor(n, d);

    // Current point on surface
    var x = (n - 1) / 4 * 10 - 5;
    var z = (d - 1) / 4 * 10 - 5;
    var anchorExp = exponentFor(3, 3);
    var delta = (pred != null && anchorExp != null) ? pred / CLAIM_ANCHOR : 1;
    var y = Math.log(delta) * 2 + 0.5;

    r.anchorMesh.position.set(x, Math.max(0.1, y), z);
    r.anchorRing.position.copy(r.anchorMesh.position);
    r.anchorRing.rotation.x = time * 0.8;
    r.anchorRing.rotation.y = time * 0.5;

    // Glow pulse
    r.anchorMesh.material.emissiveIntensity = 0.7 + 0.3 * Math.sin(time * 2.5);

    // Surface color update based on current (N,D)
    var isClaimPoint = (n === 3 && d === 3);
    if (isClaimPoint) {
      r.surface.material.emissive = new THREE.Color(0x00e5ff);
      r.surface.material.emissiveIntensity = 0.15 + 0.1 * Math.sin(time);
    } else {
      r.surface.material.emissive = new THREE.Color(0x000000);
      r.surface.material.emissiveIntensity = 0;
    }

    // Camera slow orbit
    r.camera.position.x = Math.sin(time * 0.2) * 4;
    r.camera.position.y = 8 + Math.cos(time * 0.15) * 2;
    r.camera.lookAt(0, 2, 0);

    if (r.composer) {
      r.composer.render();
    } else {
      r.renderer.render(r.scene, r.camera);
    }
  }

  function disposeGod3D(r) {
    if (!r) return;
    window.removeEventListener('resize', r._resizeHandler);
    r.surface.geometry.dispose();
    r.surface.material.dispose();
    r.anchorMesh.geometry.dispose();
    r.anchorMesh.material.dispose();
    r.anchorRing.geometry.dispose();
    r.anchorRing.material.dispose();
    r.particles.geometry.dispose();
    r.particles.material.dispose();
    if (r.composer) r.renderer.dispose();
    r.container.remove();
  }

  // ── Panel Registration ───────────────────────────────────────────────────

  window.PFExplorer.registerPanel({
    id: 'god-equation',
    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="panel-wrap">' +
          '<div class="panel-atlas">' +
            '<section class="canvas-panel" style="position:relative">' +
              '<div class="panel-header">' +
                '<div>' +
                  '<p class="eyebrow">Planck to Matter</p>' +
                  '<h3>The hierarchy is one exponential climb, not a loose metaphor.</h3>' +
                  '<p>Move N and D and the ladder either lands near the matter window or misses it by orders of magnitude.</p>' +
                '</div>' +
              '</div>' +
              '<canvas class="panel-canvas" id="godCanvas" style="position:absolute;inset:0;width:100%;height:100%"></canvas>' +
              '<div class="canvas-overlay"></div>' +
            '</section>' +
            '<section class="info-panel" id="godInfo"></section>' +
          '</div>' +
        '</div>';

      this.state = {
        canvas: ctx.stage.querySelector('#godCanvas'),
        info: ctx.stage.querySelector('#godInfo'),
        nValue: 3,
        dValue: 3
      };

      this.renderInfo(ctx);
    },

    unmount: function () {
      disposeGod3D(this.state._3d);
      this.state = null;
    },

    resize: function (ctx) {
      var state = this.state;
      if (state._3d) {
        var w = state.canvas.clientWidth;
        var h = state.canvas.clientHeight;
        state._3d.camera.aspect = w / h;
        state._3d.camera.updateProjectionMatrix();
        state._3d.renderer.setSize(w, h);
        if (state._3d.composer) state._3d.composer.setSize(w, h);
      }
    },

    renderInfo: function (ctx) {
      var state = this.state;
      var b0 = b0ForN(state.nValue);
      var prediction = lambdaFor(state.nValue, state.dValue);
      var errorPct = prediction ? Math.abs(prediction - OBSERVED) / OBSERVED * 100 : null;
      var audit = ctx.data.godEquationAudit || { dependencyChain: [], gaps: [] };
      var isClaimPoint = (state.nValue === 3 && state.dValue === 3);

      state.info.innerHTML =
        '<div class="panel-header">' +
          '<div>' +
            '<p class="eyebrow">Current frontier</p>' +
            '<h3>' + (prediction ? ctx.utils.formatScientific(prediction, 3) + ' m' : 'no asymptotic branch') + '</h3>' +
            '<p>The formula and numerical target are anchored. The operator and probability bridge remain explicitly open.</p>' +
          '</div>' +
          '<span class="status-pill status-conditional">CONDITIONAL</span>' +
        '</div>' +
        ctx.app.renderWrongIntuition(ctx.app.getResult('god-equation')) +
        '<div class="control-group">' +
          '<label for="godN">Generations N</label>' +
          '<input id="godN" type="range" min="1" max="5" step="1" value="' + state.nValue + '">' +
          '<output id="godNOut">N = ' + state.nValue + (state.nValue === 3 ? ' ← PF target' : '') + '</output>' +
        '</div>' +
        '<div class="control-group">' +
          '<label for="godD">Spatial dimensions D</label>' +
          '<input id="godD" type="range" min="1" max="5" step="1" value="' + state.dValue + '">' +
          '<output id="godDOut">D = ' + state.dValue + (state.dValue === 3 ? ' ← physical' : '') + '</output>' +
        '</div>' +
        '<div class="formula">lambda_c = sqrt(2) l_P exp(4 pi^2 N^(D/2) / b0),  b0 = (22 - 2N) / 3</div>' +
        '<div class="stat-grid">' +
          '<div class="stat-tile"><strong>' + b0.toFixed(3) + '</strong><span>b0(N)</span></div>' +
          '<div class="stat-tile"><strong>' + (errorPct !== null ? errorPct.toFixed(1) + '%' : 'n/a') + '</strong><span>error vs 1.14e-18 m</span></div>' +
          '<div class="stat-tile"><strong>' + ctx.utils.formatScientific(LP, 2) + '</strong><span>Planck l_P</span></div>' +
          '<div class="stat-tile"><strong>' + (isClaimPoint ? '✓ CLAIM (3,3)' : 'other point') + '</strong><span>formula position</span></div>' +
        '</div>' +
        '<div class="note-box story-only"><strong>Story</strong><p>N = 3 and D = 3 are the intended landing site. Moving either shifts the exponential enough that the matter window becomes visibly special.</p></div>' +
        '<div class="note-box audit-only"><strong>Why CONDITIONAL stays CONDITIONAL</strong><p>The (3,3) point is anchored at 1.145e-18 m and 0.4% error. What stays open is the bridge from the exact internal model to operator closure and H_prod factorization.</p></div>' +
        '<section class="audit-stack audit-only">' +
          '<div class="audit-section">' +
            '<span class="eyebrow">Dependency chain</span>' +
            dependencyChainHtml(audit.dependencyChain) +
          '</div>' +
          gapCardsHtml(audit.gaps) +
        '</section>';

      state.info.querySelector('#godN').addEventListener('input', function (e) {
        state.nValue = Number(e.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      state.info.querySelector('#godD').addEventListener('input', function (e) {
        state.dValue = Number(e.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });

      if (!state._3d) {
        state._3d = createRenderer3D(state.canvas.parentElement);
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
      updateGod3D(this.state._3d, this.state, time);
    }
  });
}());
