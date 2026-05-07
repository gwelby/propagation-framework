/**
 * Cellular Scene — Cell Membranes and Organelles
 *
 * "Life is active coherence maintenance."
 *
 * At the cellular scale (10⁻⁵ m), we see the first level of biological
 * organization. The cell membrane maintains an electrochemical gradient
 * — a coherence boundary between inside and outside. Organelles are
 * specialized compartments where specific chemical propagations occur.
 *
 * Visual layers:
 *   1. Cell membrane            — the lipid bilayer boundary
 *   2. Cytoplasm field        — active medium with cytoskeleton
 *   3. Nucleus                — genetic information core
 *   4. Mitochondria           — energy production organelles
 *   5. Cytoskeleton filaments — structural coherence network
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;

  // ── Coordinate ────────────────────────────────────────────────────────────
  function cellularY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((-5 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Cell Membrane ───────────────────────────────────────────────────────────
  function buildCellMembrane() {
    var centerY = cellularY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    // Main cell body — slightly deformed sphere
    var cellGeo = new THREE.SphereGeometry(4.5, 48, 48);
    var positions = cellGeo.attributes.position.array;
    for (var i = 0; i < positions.length; i += 3) {
      var x = positions[i];
      var y = positions[i + 1];
      var z = positions[i + 2];
      // Add subtle irregularity for organic feel
      var noise = Math.sin(x * 2) * Math.cos(y * 1.5) * Math.sin(z) * 0.15;
      positions[i] = x + x * noise * 0.1;
      positions[i + 1] = y + y * noise * 0.1;
      positions[i + 2] = z + z * noise * 0.1;
    }
    cellGeo.computeVertexNormals();

    var cellMat = window.PropagationShaders
      ? window.PropagationShaders.createFieldDensityMaterial({
          density: 0.5,
          coherence: 0.7,
          fieldColor: 0x80ed99,
          cohColor: 0x69ff94,
          bgColor: 0x020408
        })
      : new THREE.MeshStandardMaterial({
          color: 0x80ed99,
          emissive: 0x80ed99,
          emissiveIntensity: 0.3,
          transparent: true,
          opacity: 0.6,
          side: THREE.DoubleSide
        });

    var cell = new THREE.Mesh(cellGeo, cellMat);
    cell.position.copy(centerPos);
    _objs.push(cell);
    if (cellMat.uniforms) _shaders.push(cellMat);
    else _mats.push(cellMat);
    scene.add(cell);

    // Membrane highlight — the boundary itself
    var membraneGeo = new THREE.SphereGeometry(4.6, 32, 32);
    var membraneMat = new THREE.MeshBasicMaterial({
      color: 0x69ff94,
      transparent: true,
      opacity: 0.15,
      side: THREE.BackSide
    });
    var membrane = new THREE.Mesh(membraneGeo, membraneMat);
    membrane.position.copy(centerPos);
    _objs.push(membrane);
    _mats.push(membraneMat);
    scene.add(membrane);
  }

  // ── Nucleus ────────────────────────────────────────────────────────────────
  function buildNucleus() {
    var centerY = cellularY();
    var centerPos = new THREE.Vector3(5, centerY, 0);
    var nucleusPos = centerPos.clone().add(new THREE.Vector3(-0.5, 0.5, 0));

    // Nuclear envelope
    var nuclearGeo = new THREE.SphereGeometry(1.4, 32, 32);
    var nuclearMat = new THREE.MeshStandardMaterial({
      color: 0x4488aa,
      emissive: 0x4488aa,
      emissiveIntensity: 0.4,
      transparent: true,
      opacity: 0.7
    });
    var nucleus = new THREE.Mesh(nuclearGeo, nuclearMat);
    nucleus.position.copy(nucleusPos);
    _objs.push(nucleus);
    _mats.push(nuclearMat);
    scene.add(nucleus);

    // Chromatin — genetic material inside
    var chromatinGeo = new THREE.SphereGeometry(1.1, 24, 24);
    var chromatinMat = new THREE.MeshStandardMaterial({
      color: 0x6633aa,
      emissive: 0x6633aa,
      emissiveIntensity: 0.25,
      wireframe: true
    });
    var chromatin = new THREE.Mesh(chromatinGeo, chromatinMat);
    chromatin.position.copy(nucleusPos);
    chromatin.userData = { isChromatin: true, rotSpeed: 0.1 };
    _objs.push(chromatin);
    _mats.push(chromatinMat);
    scene.add(chromatin);

    // Nucleolus
    var nucleolusGeo = new THREE.SphereGeometry(0.4, 16, 16);
    var nucleolusMat = new THREE.MeshStandardMaterial({
      color: 0xaa5588,
      emissive: 0xaa5588,
      emissiveIntensity: 0.35
    });
    var nucleolus = new THREE.Mesh(nucleolusGeo, nucleolusMat);
    nucleolus.position.copy(nucleusPos).add(new THREE.Vector3(0.3, 0.2, 0.2));
    _objs.push(nucleolus);
    _mats.push(nucleolusMat);
    scene.add(nucleolus);
  }

  // ── Mitochondria ────────────────────────────────────────────────────────────
  function buildMitochondria() {
    var centerY = cellularY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    var mitochondriaPositions = [
      { pos: new THREE.Vector3(2, -1.5, 1.5), rot: [0.5, 0.3, 0] },
      { pos: new THREE.Vector3(-1.5, 1, 2), rot: [0.3, 0.8, 0.2] },
      { pos: new THREE.Vector3(1.5, 1.5, -1.8), rot: [0.2, 0.5, 0.3] }
    ];

    mitochondriaPositions.forEach(function (m, i) {
      // Elongated capsule shape
      var mitoGeo = new THREE.CapsuleGeometry(0.35, 1.2, 8, 16);
      var mitoMat = new THREE.MeshStandardMaterial({
        color: 0xff6b6b,
        emissive: 0xff6b6b,
        emissiveIntensity: 0.35,
        metalness: 0.3,
        roughness: 0.5
      });
      var mito = new THREE.Mesh(mitoGeo, mitoMat);
      mito.position.copy(centerPos).add(m.pos);
      mito.rotation.set(m.rot[0], m.rot[1], m.rot[2]);
      mito.userData = {
        phase: i * Math.PI * 2 / 3,
        isMitochondrion: true
      };
      _objs.push(mito);
      _mats.push(mitoMat);
      scene.add(mito);

      // Cristae — internal folds (represented as rings)
      for (var c = 0; c < 3; c++) {
        var cristaeGeo = new THREE.TorusGeometry(0.2, 0.04, 6, 16);
        var cristaeMat = new THREE.MeshBasicMaterial({
          color: 0xff9999,
          transparent: true,
          opacity: 0.5
        });
        var cristae = new THREE.Mesh(cristaeGeo, cristaeMat);
        cristae.position.copy(mito.position);
        cristae.rotation.set(m.rot[0], m.rot[1], m.rot[2]);
        cristae.translateY(-0.3 + c * 0.3);
        cristae.rotateY(Math.PI / 2);
        _objs.push(cristae);
        _mats.push(cristaeMat);
        scene.add(cristae);
      }
    });
  }

  // ── Cytoskeleton Filaments ────────────────────────────────────────────────
  function buildCytoskeleton() {
    var centerY = cellularY();
    var centerPos = new THREE.Vector3(5, cellularY(), 0);

    // Create network of filaments
    var filamentCount = 12;
    for (var f = 0; f < filamentCount; f++) {
      // Random start point near nucleus
      var startTheta = Math.random() * Math.PI * 2;
      var startPhi = Math.acos(2 * Math.random() - 1);
      var startR = 1.5;
      var start = new THREE.Vector3(
        centerPos.x - 0.5 + startR * Math.sin(startPhi) * Math.cos(startTheta),
        centerPos.y + 0.5 + startR * Math.sin(startPhi) * Math.sin(startTheta),
        startR * Math.cos(startPhi)
      );

      // End point near membrane
      var endTheta = Math.random() * Math.PI * 2;
      var endPhi = Math.acos(2 * Math.random() - 1);
      var endR = 4;
      var end = new THREE.Vector3(
        centerPos.x + endR * Math.sin(endPhi) * Math.cos(endTheta),
        centerPos.y + endR * Math.sin(endPhi) * Math.sin(endTheta),
        endR * Math.cos(endPhi)
      );

      var curve = new THREE.CatmullRomCurve3([
        start,
        new THREE.Vector3(
          (start.x + end.x) / 2 + (Math.random() - 0.5),
          (start.y + end.y) / 2 + (Math.random() - 0.5),
          (start.z + end.z) / 2 + (Math.random() - 0.5)
        ),
        end
      ]);

      var filGeo = new THREE.TubeGeometry(curve, 16, 0.04, 6, false);
      var filMat = new THREE.MeshStandardMaterial({
        color: 0x80ed99,
        emissive: 0x80ed99,
        emissiveIntensity: 0.3,
        transparent: true,
        opacity: 0.6
      });
      var filament = new THREE.Mesh(filGeo, filMat);
      filament.userData = {
        phase: Math.random() * Math.PI * 2,
        isFilament: true
      };
      _objs.push(filament);
      _mats.push(filMat);
      scene.add(filament);
    }
  }

  // ── Vesicles ───────────────────────────────────────────────────────────────
  function buildVesicles() {
    var centerY = cellularY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    var vesicleCount = 8;
    for (var v = 0; v < vesicleCount; v++) {
      var radius = 0.2 + Math.random() * 0.25;
      var vesGeo = new THREE.SphereGeometry(radius, 16, 16);
      var vesMat = new THREE.MeshStandardMaterial({
        color: 0x99ccff,
        emissive: 0x99ccff,
        emissiveIntensity: 0.25,
        transparent: true,
        opacity: 0.7
      });
      var vesicle = new THREE.Mesh(vesGeo, vesMat);

      // Random position within cell
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 2 + Math.random() * 2;
      vesicle.position.set(
        centerPos.x + r * Math.sin(phi) * Math.cos(theta),
        centerPos.y + r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      );

      vesicle.userData = {
        isVesicle: true,
        drift: new THREE.Vector3(
          (Math.random() - 0.5) * 0.2,
          (Math.random() - 0.5) * 0.2,
          (Math.random() - 0.5) * 0.2
        ),
        phase: Math.random() * Math.PI * 2
      };
      _objs.push(vesicle);
      _mats.push(vesMat);
      scene.add(vesicle);
    }
  }

  // ── Scale Label ────────────────────────────────────────────────────────────
  function buildLabel() {
    if (!window.ScaleEngine) return;
    var canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 96;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 512, 96);
    ctx.font = 'bold 32px DM Sans, sans-serif';
    ctx.fillStyle = '#80ed99';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Cellular Scale — 10⁻⁵ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, cellularY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.CellularScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();

      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.012 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.012);
      }

      buildCellMembrane();
      buildNucleus();
      buildMitochondria();
      buildCytoskeleton();
      buildVesicles();
      buildLabel();

      camera.position.set(5, cellularY(), 20);
      camera.lookAt(5, cellularY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, cellularY(), 20),
        target: new THREE.Vector3(5, cellularY(), 0),
        fov: 50
      };
    },

    getSharedElements: function () {
      // Return cell membrane and key structural elements
      return _objs.filter(function (o) {
        return o.userData && (
          o.userData.isCellMembrane ||
          o.userData.isFilament ||
          o.geometry && o.geometry.type === 'SphereGeometry'
        );
      }).slice(0, 5);
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Cellular scene uses medium-high LOD
      return 1;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[CellularScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      _objs.forEach(function (o) {
        // Rotate chromatin
        if (o.userData && o.userData.isChromatin) {
          o.rotation.y += dt * o.userData.rotSpeed;
          o.rotation.z += dt * o.userData.rotSpeed * 0.3;
        }
        // Pulse mitochondria
        if (o.userData && o.userData.isMitochondrion) {
          var pulse = 0.7 + 0.3 * Math.sin(time * 3 + o.userData.phase);
          o.material.emissiveIntensity = 0.35 * pulse;
        }
        // Pulse filaments
        if (o.userData && o.userData.isFilament) {
          o.material.emissiveIntensity = 0.3 + 0.15 * Math.sin(time * 2 + o.userData.phase);
        }
        // Drift vesicles
        if (o.userData && o.userData.isVesicle) {
          o.position.x += o.userData.drift.x * dt;
          o.position.y += o.userData.drift.y * dt;
          o.position.z += o.userData.drift.z * dt;

          // Boundary check — keep within cell
          var dist = o.position.distanceTo(new THREE.Vector3(5, cellularY(), 0));
          if (dist > 4) {
            o.userData.drift.negate();
          }
        }
      });
    },

    deactivate: function () {
      _objs.forEach(function (o) {
        if (o.geometry) o.geometry.dispose();
        if (o.material) {
          if (Array.isArray(o.material)) {
            o.material.forEach(function (m) { m.dispose(); });
          } else {
            o.material.dispose();
          }
        }
        if (scene && scene.remove) scene.remove(o);
      });
      _objs = [];
      _mats = [];
      _shaders = [];
      if (scene) scene.fog = null;
    }
  };
}());
