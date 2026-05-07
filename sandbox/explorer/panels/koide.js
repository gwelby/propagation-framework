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

  function createRenderer(stage, canvas) {
    var container = document.createElement('div');
    container.style.cssText = 'position:absolute;inset:0;pointer-events:none;';
    canvas.parentElement.appendChild(container);

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

  function buildKoide3D(panelState, ctx) {
    var r = createRenderer(ctx.stage, panelState.canvas);
    panelState._3d = r;

    // Triangle line (edges between mass vertices)
    var lineGeo = new THREE.BufferGeometry();
    var linePositions = new Float32Array(3 * 3 * 3); 
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

    panelState._3d.meshes = vertexMeshes;
    panelState._3d.triangleLine = triangleLine;
    panelState._3d.centerMesh = centerMesh;
    panelState._3d.refRing = refRing;

    // Bloom post-processing
    if (window.THREE && window.THREE.EffectComposer) {
      try {
        var composer = new THREE.EffectComposer(r.renderer);
        composer.addPass(new THREE.RenderPass(r.scene, r.camera));
        var bloom = new THREE.UnrealBloomPass(
          new THREE.Vector2(panelState.canvas.clientWidth, panelState.canvas.clientHeight),
          0.6, 0.4, 0.82
        );
        composer.addPass(bloom);
        panelState._3d.composer = composer;
      } catch (e) {
        panelState._3d.composer = null;
      }
    }

    return r;
  }

  function updateKoide3D(panelState, time) {
    if (!panelState._3d) return;
    var r = panelState._3d;
    var current = buildMassSet(panelState.selectedMass, panelState.deltaPct);
    var masses = valuesFromSet(current);
    var verts = tetrahedronVertices(masses);

    // Update vertex positions
    r.meshes.forEach(function (mesh, i) {
      var v = verts[i];
      mesh.position.set(v.x, v.y, 0);

      // Breathing animation
      var breathe = 1 + 0.04 * Math.sin(time * 1.2 + i * 2.1);
      mesh.scale.setScalar(breathe);

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

    r.refRing.rotation.z = time * 0.15;

    // Camera slow orbit
    r.camera.position.x = Math.sin(time * 0.25) * 0.8;
    r.camera.position.y = Math.cos(time * 0.18) * 0.5;
    r.camera.lookAt(0, 0, 0);
  }

  function disposeKoide3D(panelState) {
    if (!panelState || !panelState._3d) return;
    var r = panelState._3d;
    if (r.meshes) {
      r.meshes.forEach(function (m) {
        m.geometry.dispose();
        m.material.dispose();
      });
    }
    if (r.renderer) r.renderer.dispose();
    if (r.container) r.container.remove();
    panelState._3d = null;
  }

  // ── Panel Registration ─────────────────────────────────────────────────────

  window.PFExplorer.registerPanel({
    id: 'koide',
    title: 'Koide Mass Geometry',
    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="panel-wrap">' +
          '<div class="panel-atlas">' +
            '<section class="canvas-panel" style="position:relative">' +
              '<div class="panel-header">' +
                '<div>' +
                  '<p class="eyebrow">Mass Geometry</p>' +
                  '<h3>The charged lepton triangle stays near one exact target.</h3>' +
                  '<p>Perturb one PDG mass and watch Q pull away from 2/3 while the amplitude geometry loosens.</p>' +
                '</div>' +
              '</div>' +
              '<canvas class="panel-canvas" id="koideCanvas" style="position:absolute;inset:0;width:100%;height:100%"></canvas>' +
              '<div class="canvas-overlay"></div>' +
            '</section>' +
            '<section class="info-panel" id="koideInfo"></section>' +
          '</div>' +
        '</div>';

      this.panelState = {
        canvas: ctx.stage.querySelector('#koideCanvas'),
        info: ctx.stage.querySelector('#koideInfo'),
        selectedMass: 'tau',
        deltaPct: 0
      };

      this.renderInfo(ctx);
    },

    unmount: function (ctx) {
      disposeKoide3D(this.panelState);
      this.panelState = null;
    },

    resize: function (ctx) {
      var ps = this.panelState;
      if (!ps || !ps._3d) return;
      var r = ps._3d;
      var w = ps.canvas.clientWidth;
      var h = ps.canvas.clientHeight;
      r.camera.aspect = w / h;
      r.camera.updateProjectionMatrix();
      r.renderer.setSize(w, h);
      if (r.composer) r.composer.setSize(w, h);
    },

    renderInfo: function (ctx) {
      var self = this;
      var ps = this.panelState;
      var current = buildMassSet(ps.selectedMass, ps.deltaPct);
      var masses = valuesFromSet(current);
      var qValue = ctx.utils.koideQ(masses);
      var ra = ctx.utils.computeKoideRA(masses);
      var deviationPct = Math.abs(qValue - 2 / 3) / (2 / 3) * 100;
      var isLocked = deviationPct < 0.01;

      ps.info.innerHTML =
        '<div class="panel-header">' +
          '<div>' +
            '<p class="eyebrow">PDG 2024 lepton masses</p>' +
            '<h3>Q = ' + qValue.toFixed(7) + ' <span style="font-size:0.7em;color:var(--' + (isLocked ? 'cohere' : 'resonate') + ')">(' + (isLocked ? 'LOCKED' : deviationPct.toFixed(3) + '% off') + ')</span></h3>' +
            '<p>The baseline triangle is unnervingly tight. Even a small perturbation bends both Q and R/A away from the target.</p>' +
          '</div>' +
          '<span class="status-pill status-derived">DERIVED</span>' +
        '</div>' +
        ctx.app.renderWrongIntuition(ctx.app.getResult('koide-law')) +
        '<div class="control-group">' +
          '<label for="koideMassSelect">Perturb this mass</label>' +
          '<select id="koideMassSelect" class="premium-select">' +
            '<option value="electron">electron</option>' +
            '<option value="muon">muon</option>' +
            '<option value="tau">tau</option>' +
          '</select>' +
        '</div>' +
        '<div class="control-group">' +
          '<label for="koideDelta">Mass offset (%)</label>' +
          '<input id="koideDelta" class="premium-slider" type="range" min="-5" max="5" step="0.1" value="' + ps.deltaPct + '">' +
          '<output id="koideDeltaOut">' + ps.deltaPct.toFixed(1) + '%</output>' +
        '</div>' +
        '<div class="formula">Q = sum m_i / (sum sqrt(m_i))^2,  R/A = ' + ra.ratio.toFixed(5) + '</div>' +
        '<div class="stat-grid">' +
          '<div class="stat-tile"><strong>' + current.electron.toFixed(6) + '</strong><span>electron MeV</span></div>' +
          '<div class="stat-tile"><strong>' + current.muon.toFixed(4) + '</strong><span>muon MeV</span></div>' +
          '<div class="stat-tile"><strong>' + current.tau.toFixed(2) + '</strong><span>tau MeV</span></div>' +
          '<div class="stat-tile"><strong style="color:var(--' + (isLocked ? 'cohere' : 'resonate') + ')">' + deviationPct.toFixed(4) + '%</strong><span>deviation from 2/3</span></div>' +
        '</div>' +
        '<div class="drawer-block" style="padding:16px 0;border:0">' +
          '<span class="eyebrow">2/9 cluster</span>' +
          ctx.app.compareBarHtml(0.22310, 2 / 9, 0.00045, 0.2218, 0.2236) +
          '<div class="metric-row" style="margin-top:12px">' +
            '<span class="metric-pill">delta_Koide = 0.2222296</span>' +
            '<span class="metric-pill">2/9 = 0.2222222</span>' +
            '<span class="metric-pill">sin^2(theta_W) = 0.22310</span>' +
          '</div>' +
        '</div>';

      ps.info.querySelector('#koideMassSelect').value = ps.selectedMass;
      ps.info.querySelector('#koideMassSelect').addEventListener('change', function (e) {
        ps.selectedMass = e.target.value;
        self.renderInfo(ctx);
      });
      ps.info.querySelector('#koideDelta').addEventListener('input', function (e) {
        ps.deltaPct = Number(e.target.value);
        ps.info.querySelector('#koideDeltaOut').textContent = ps.deltaPct.toFixed(1) + '%';
        self.renderInfo(ctx);
      });

      if (!ps._3d) {
        buildKoide3D(ps, ctx);
        this.resize(ctx);
      }
    },

    update: function (ctx, dt, time) {
      if (!this.panelState || !this.panelState._3d) return;
      updateKoide3D(this.panelState, time);

      var r = this.panelState._3d;
      if (r.composer) {
        r.composer.render();
      } else {
        r.renderer.render(r.scene, r.camera);
      }
    }
  });
}());
