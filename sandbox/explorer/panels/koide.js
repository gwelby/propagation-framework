/**
 * Koide Panel — Three.js Upgrade
 * 
 * Three charged leptons at tetrahedron vertices, 120° breathing animation.
 * Mass perturbations move vertices and distort the triangle in real-time.
 * Shows Q deviation and R/A ratio.
 */
(function () {
  'use strict';

  var baseMasses = {
    electron: 0.51099895,
    muon: 105.6583755,
    tau: 1776.86
  };

  function buildMassSet(selection, deltaPct) {
    var multiplier = 1 + deltaPct / 100;
    return {
      electron: selection === 'electron' ? baseMasses.electron * multiplier : baseMasses.electron,
      muon: selection === 'muon' ? baseMasses.muon * multiplier : baseMasses.muon,
      tau: selection === 'tau' ? baseMasses.tau * multiplier : baseMasses.tau
    };
  }

  function valuesFromSet(set) {
    return [set.electron, set.muon, set.tau];
  }

  function tetrahedronVertices(masses) {
    var sqrtMasses = masses.map(function (m) { return Math.sqrt(m); });
    var maxSqrt = Math.max.apply(Math, sqrtMasses);
    var r = 2.8; // base radius
    var vertices = sqrtMasses.map(function (s) { return s / maxSqrt * r; });

    // Tetrahedral angles (unwrapped for 2D display as equilateral triangle projection)
    // Electron at top, muon/tau at base corners (120° spacing)
    var angles = [-Math.PI / 2, -Math.PI / 2 + (2 * Math.PI) / 3, -Math.PI / 2 + (4 * Math.PI) / 3];
    return vertices.map(function (v, i) {
      return {
        x: Math.cos(angles[i]) * v,
        y: Math.sin(angles[i]) * v,
        label: ['tau', 'electron', 'muon'][i],
        rawMass: masses[i],
        color: ['#ffdd55', '#00cfff', '#69ff94'][i]
      };
    });
  }

  // ── Three.js Koide Renderer ────────────────────────────────────────────────

  function createRenderer(stage) {
    var container = document.createElement('div');
    container.style.cssText = 'position:absolute;inset:0;';
    stage.appendChild(container);

    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0, 8);
    camera.lookAt(0, 0, 0);

    // Lighting
    scene.add(new THREE.AmbientLight(0x334466, 1.0));
    var dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(5, 8, 6);
    scene.add(dirLight);
    var fillLight = new THREE.PointLight(0x00cfff, 0.5, 20);
    fillLight.position.set(-5, 3, 4);
    scene.add(fillLight);

    // Background glow
    var bgGeo = new THREE.SphereGeometry(12, 16, 16);
    var bgMat = new THREE.MeshBasicMaterial({
      color: 0x020408,
      side: THREE.BackSide
    });
    scene.add(new THREE.Mesh(bgGeo, bgMat));

    return { container: container, renderer: renderer, scene: scene, camera: camera };
  }

  function buildKoide3D(state, ctx) {
    var r = createRenderer(state.canvas.parentElement);
    state._3d = r;

    // Triangle line (edges between mass vertices)
    var lineGeo = new THREE.BufferGeometry();
    var linePositions = new Float32Array(3 * 3 * 3); // 3 vertices × 3 coords
    lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    var lineMat = new THREE.LineBasicMaterial({
      color: 0xffdd55,
      linewidth: 2,
      transparent: true,
      opacity: 0.9
    });
    var triangleLine = new THREE.LineLoop(lineGeo, lineMat);
    r.scene.add(triangleLine);

    // Center dot
    var centerGeo = new THREE.SphereGeometry(0.12, 16, 16);
    var centerMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      emissive: 0xffffff,
      emissiveIntensity: 0.5,
      metalness: 0.3,
      roughness: 0.5
    });
    var centerMesh = new THREE.Mesh(centerGeo, centerMat);
    r.scene.add(centerMesh);

    // Vertex spheres
    var vertexMeshes = [];
    ['#ffdd55', '#00cfff', '#69ff94'].forEach(function (color, i) {
      var geo = new THREE.SphereGeometry(0.22, 24, 24);
      var mat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(color),
        emissive: new THREE.Color(color),
        emissiveIntensity: 0.7,
        metalness: 0.6,
        roughness: 0.3
      });
      var mesh = new THREE.Mesh(geo, mat);
      r.scene.add(mesh);
      vertexMeshes.push(mesh);

      // Glow ring
      var ringGeo = new THREE.TorusGeometry(0.38, 0.04, 8, 32);
      var ringMat = new THREE.MeshBasicMaterial({
        color: new THREE.Color(color),
        transparent: true,
        opacity: 0.5
      });
      var ring = new THREE.Mesh(ringGeo, ringMat);
      r.scene.add(ring);
      mesh.userData.ring = ring;
    });

    // Orbit reference ring
    var refGeo = new THREE.TorusGeometry(2.8, 0.03, 8, 64);
    var refMat = new THREE.MeshBasicMaterial({
      color: 0x334466,
      transparent: true,
      opacity: 0.3
    });
    var refRing = new THREE.Mesh(refGeo, refMat);
    r.scene.add(refRing);

    state._3d.meshes = vertexMeshes;
    state._3d.triangleLine = triangleLine;
    state._3d.centerMesh = centerMesh;
    state._3d.refRing = refRing;

    // Bloom post-processing
    try {
      var composer = new THREE.EffectComposer(r.renderer);
      composer.addPass(new THREE.RenderPass(r.scene, r.camera));
      var bloom = new THREE.UnrealBloomPass(
        new THREE.Vector2(state.canvas.clientWidth, state.canvas.clientHeight),
        0.6, 0.4, 0.82
      );
      composer.addPass(bloom);
      state._3d.composer = composer;
    } catch (e) {
      state._3d.composer = null;
    }

    // Resize
    function resize3d() {
      var w = state.canvas.clientWidth;
      var h = state.canvas.clientHeight;
      r.camera.aspect = w / h;
      r.camera.updateProjectionMatrix();
      r.renderer.setSize(w, h);
      if (r.composer) r.composer.setSize(w, h);
    }
    resize3d();
    state._3d.resize = resize3d;
    window.addEventListener('resize', resize3d);
    state._3d.resizeHandler = resize3d;

    return r;
  }

  function updateKoide3D(state, time) {
    if (!state._3d) return;
    var r = state._3d;
    var current = buildMassSet(state.selectedMass, state.deltaPct);
    var masses = valuesFromSet(current);
    var verts = tetrahedronVertices(masses);

    // Update vertex positions
    r.meshes.forEach(function (mesh, i) {
      var v = verts[i];
      mesh.position.set(v.x, v.y, 0);

      // Breathing animation: vertices pulse slightly
      var breathe = 1 + 0.04 * Math.sin(time * 1.2 + i * 2.1);
      mesh.scale.setScalar(breathe);

      // Update ring position
      if (mesh.userData.ring) {
        mesh.userData.ring.position.copy(mesh.position);
        mesh.userData.ring.rotation.z = time * 0.4 + i;
      }
    });

    // Update triangle line
    var posAttr = r.triangleLine.geometry.attributes.position;
    verts.forEach(function (v, i) {
      posAttr.setXYZ(i, v.x, v.y, 0);
    });
    posAttr.needsUpdate = true;

    // Animate ref ring
    r.refRing.rotation.z = time * 0.15;

    // Camera slow orbit
    r.camera.position.x = Math.sin(time * 0.25) * 0.8;
    r.camera.position.y = Math.cos(time * 0.18) * 0.5;
    r.camera.lookAt(0, 0, 0);
  }

  function disposeKoide3D(state) {
    if (!state._3d) return;
    window.removeEventListener('resize', state._3d.resizeHandler);
    state._3d.meshes.forEach(function (m) {
      m.geometry.dispose();
      m.material.dispose();
    });
    state._3d.composer = null;
    state._3d.renderer.dispose();
    state._3d.container.remove();
    state._3d = null;
  }

  // ── Panel Registration ─────────────────────────────────────────────────────

  window.PFExplorer.registerPanel({
    id: 'koide',
    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="panel-wrap">' +
          '<div class="panel-atlas">' +
            '<section class="canvas-panel" style="position:relative">' +
              '<div class="panel-header">' +
                '<div>' +
                  '<p class="eyebrow">Mass Geometry</p>' +
                  '<h3>The charged lepton triangle stays near one exact target.</h3>' +
                  '<p>Perturb one PDG mass and watch Q pull away from 2 / 3 while the amplitude geometry loosens.</p>' +
                '</div>' +
              '</div>' +
              '<canvas class="panel-canvas" id="koideCanvas" style="position:absolute;inset:0;width:100%;height:100%"></canvas>' +
              '<div class="canvas-overlay"></div>' +
            '</section>' +
            '<section class="info-panel" id="koideInfo"></section>' +
          '</div>' +
        '</div>';

      this.state = {
        canvas: ctx.stage.querySelector('#koideCanvas'),
        info: ctx.stage.querySelector('#koideInfo'),
        selectedMass: 'tau',
        deltaPct: 0
      };

      this.renderInfo(ctx);
    },

    unmount: function () {
      disposeKoide3D(this.state);
      this.state = null;
    },

    resize: function (ctx) {
      var state = this.state;
      if (state._3d && state._3d.resize) {
        state._3d.resize();
      }
    },

    renderInfo: function (ctx) {
      var state = this.state;
      var current = buildMassSet(state.selectedMass, state.deltaPct);
      var masses = valuesFromSet(current);
      var qValue = ctx.utils.koideQ(masses);
      var ra = ctx.utils.computeKoideRA(masses);
      var deviationPct = Math.abs(qValue - 2 / 3) / (2 / 3) * 100;
      var isLocked = deviationPct < 0.01;

      state.info.innerHTML =
        '<div class="panel-header">' +
          '<div>' +
            '<p class="eyebrow">PDG 2024 lepton masses</p>' +
            '<h3>Q = ' + qValue.toFixed(7) + ' <span style="font-size:0.7em;color:var(--' + (isLocked ? 'cohere' : 'resonate') + ')">(' + (isLocked ? 'LOCKED' : deviationPct.toFixed(3) + '% off') + ')</span></h3>' +
            '<p>The baseline triangle is unnervingly tight. Even a small single-mass perturbation bends both Q and R / A away from the repo target.</p>' +
          '</div>' +
          '<span class="status-pill status-derived">DERIVED</span>' +
        '</div>' +
        ctx.app.renderWrongIntuition(ctx.app.getResult('koide-law')) +
        '<div class="control-group">' +
          '<label for="koideMassSelect">Perturb this mass</label>' +
          '<select id="koideMassSelect"><option value="electron">electron</option><option value="muon">muon</option><option value="tau">tau</option></select>' +
        '</div>' +
        '<div class="control-group">' +
          '<label for="koideDelta">Mass offset (%)</label>' +
          '<input id="koideDelta" type="range" min="-5" max="5" step="0.1" value="' + state.deltaPct + '">' +
          '<output id="koideDeltaOut">' + state.deltaPct.toFixed(1) + '%</output>' +
        '</div>' +
        '<div class="formula">Q = sum m_i / (sum sqrt(m_i))^2,  R / A = ' + ra.ratio.toFixed(5) + '</div>' +
        '<div class="stat-grid">' +
          '<div class="stat-tile"><strong>' + current.electron.toFixed(6) + '</strong><span>electron MeV</span></div>' +
          '<div class="stat-tile"><strong>' + current.muon.toFixed(4) + '</strong><span>muon MeV</span></div>' +
          '<div class="stat-tile"><strong>' + current.tau.toFixed(2) + '</strong><span>tau MeV</span></div>' +
          '<div class="stat-tile"><strong style="color:var(--' + (isLocked ? 'cohere' : 'resonate') + ')">' + deviationPct.toFixed(4) + '%</strong><span>deviation from 2/3</span></div>' +
        '</div>' +
        '<div class="note-box story-only"><strong>Story</strong><p>The baseline triangle is unnervingly tight. Even a small single-mass perturbation bends both Q and R/A away from the repo target.</p></div>' +
        '<div class="note-box audit-only"><strong>Audit</strong><p>The phase frontier remains empirical. The amplitude lock is derived; the delta_0 = 2/9 target is displayed below as a separate signal, not silently promoted.</p></div>' +
        '<div class="drawer-block" style="padding:0;border:0">' +
          '<span class="eyebrow">2 / 9 cluster</span>' +
          PFExplorer.compareBarHtml(0.22310, 2 / 9, 0.00045, 0.2218, 0.2236) +
          '<div class="metric-row">' +
            '<span class="metric-pill">delta_Koide = 0.2222296</span>' +
            '<span class="metric-pill">2 / 9 = 0.2222222</span>' +
            '<span class="metric-pill">sin^2(theta_W) = 0.22310</span>' +
          '</div>' +
        '</div>';

      state.info.querySelector('#koideMassSelect').value = state.selectedMass;
      state.info.querySelector('#koideMassSelect').addEventListener('change', function (event) {
        state.selectedMass = event.target.value;
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      state.info.querySelector('#koideDelta').addEventListener('input', function (event) {
        state.deltaPct = Number(event.target.value);
        state.info.querySelector('#koideDeltaOut').textContent = state.deltaPct.toFixed(1) + '%';
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      ctx.app.syncActiveResultCards();

      // Build 3D scene on first render
      if (!state._3d) {
        buildKoide3D(state, ctx);
      }
    },

    update: function (ctx, dt, time) {
      if (!this.state._3d) return;
      updateKoide3D(this.state, time);

      if (this.state._3d.composer) {
        this.state._3d.composer.render();
      } else {
        this.state._3d.renderer.render(this.state._3d.scene, this.state._3d.camera);
      }
    }
  });
}());
