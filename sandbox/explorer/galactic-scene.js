/**
 * Galactic Scene — Galaxy Filaments and Large-Scale Structure
 *
 * "The cosmos draws the same logic at every scale."
 *
 * At the galactic scale (10²¹ m), we witness the cosmic web's local
 * manifestation — galaxy clusters strung along filaments of dark matter,
 * with vast voids between. This is coherence at the largest scales:
 * structure frozen from primordial fluctuations, shaped by the
 * same propagation principles that govern quantum fields.
 *
 * Visual layers:
 *   1. Filament network       — glowing dark matter strands
 *   2. Galaxy clusters        — bright nodes at filament intersections
 *   3. Dark matter halos      — extended gravitational influence
 *   4. Void regions           — low-density cosmic bubbles
 *   5. Satellite galaxies     — smaller gravitationally-bound systems
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;

  // ── Coordinate ────────────────────────────────────────────────────────────
  function galacticY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((21 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Filament Network ─────────────────────────────────────────────────────
  function buildFilamentNetwork() {
    var centerY = galacticY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    // Main filament trunk — the backbone of the Local Supercluster
    var mainFilamentCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-8, 0, -6),
      new THREE.Vector3(-4, 2, -3),
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(4, -1, 3),
      new THREE.Vector3(8, 1, 6)
    ]);

    var mainGeo = new THREE.TubeGeometry(mainFilamentCurve, 64, 0.35, 12, false);
    var mainMat = new THREE.MeshStandardMaterial({
      color: 0x7c5cbf,
      emissive: 0x7c5cbf,
      emissiveIntensity: 0.35,
      metalness: 0.6,
      roughness: 0.35,
      transparent: true,
      opacity: 0.75
    });
    var mainFilament = new THREE.Mesh(mainGeo, mainMat);
    mainFilament.position.copy(centerPos);
    _objs.push(mainFilament);
    _mats.push(mainMat);
    scene.add(mainFilament);

    // Branch filaments
    var branches = [
      { start: new THREE.Vector3(-2, 1, -1), end: new THREE.Vector3(-6, 4, 2), thickness: 0.2 },
      { start: new THREE.Vector3(2, -0.5, 1), end: new THREE.Vector3(6, -3, -2), thickness: 0.18 },
      { start: new THREE.Vector3(0, 0.5, 0), end: new THREE.Vector3(-3, -2, 4), thickness: 0.15 }
    ];

    branches.forEach(function (branch) {
      var curve = new THREE.CatmullRomCurve3([
        branch.start,
        new THREE.Vector3(
          (branch.start.x + branch.end.x) / 2 + (Math.random() - 0.5),
          (branch.start.y + branch.end.y) / 2 + (Math.random() - 0.5) * 2,
          (branch.start.z + branch.end.z) / 2 + (Math.random() - 0.5)
        ),
        branch.end
      ]);

      var geo = new THREE.TubeGeometry(curve, 32, branch.thickness, 8, false);
      var mat = new THREE.MeshStandardMaterial({
        color: 0x7c5cbf,
        emissive: 0x7c5cbf,
        emissiveIntensity: 0.25,
        transparent: true,
        opacity: 0.6
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.copy(centerPos);
      mesh.userData.phase = Math.random() * Math.PI * 2;
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);
    });
  }

  // ── Galaxy Clusters ───────────────────────────────────────────────────────
  function buildGalaxyClusters() {
    var centerY = galacticY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    var clusters = [
      { pos: new THREE.Vector3(0, 0, 0), size: 1.2, color: 0xffdd55, name: 'central' },
      { pos: new THREE.Vector3(-5, 2.5, -3), size: 0.8, color: 0xd63031, name: 'virgo-like' },
      { pos: new THREE.Vector3(4, -1, 2), size: 0.9, color: 0xd63031, name: 'fornax-like' },
      { pos: new THREE.Vector3(-2, -2, 4), size: 0.6, color: 0x7c5cbf, name: 'satellite' },
      { pos: new THREE.Vector3(6, 1, -2), size: 0.5, color: 0x7c5cbf, name: 'satellite' }
    ];

    clusters.forEach(function (cluster) {
      // Core cluster sphere
      var coreGeo = new THREE.SphereGeometry(cluster.size, 32, 32);
      var coreMat = new THREE.MeshStandardMaterial({
        color: cluster.color,
        emissive: cluster.color,
        emissiveIntensity: cluster.name === 'central' ? 0.9 : 0.6,
        metalness: 0.4,
        roughness: 0.4,
        transparent: true,
        opacity: 0.85
      });
      var core = new THREE.Mesh(coreGeo, coreMat);
      core.position.copy(centerPos).add(cluster.pos);
      core.userData = {
        baseIntensity: coreMat.emissiveIntensity,
        phase: Math.random() * Math.PI * 2,
        pulseSpeed: 0.8 + Math.random() * 0.6,
        isCentral: cluster.name === 'central'
      };
      _objs.push(core);
      _mats.push(coreMat);
      scene.add(core);

      // Dark matter halo — extended gravitational influence
      var haloGeo = new THREE.SphereGeometry(cluster.size * 4, 24, 24);
      var haloMat = new THREE.MeshBasicMaterial({
        color: 0x7c5cbf,
        transparent: true,
        opacity: 0.04,
        side: THREE.BackSide
      });
      var halo = new THREE.Mesh(haloGeo, haloMat);
      halo.position.copy(core.position);
      _objs.push(halo);
      _mats.push(haloMat);
      scene.add(halo);

      // Galaxy swarm particles around cluster
      var particleCount = cluster.name === 'central' ? 150 : 80;
      var positions = new Float32Array(particleCount * 3);
      for (var i = 0; i < particleCount; i++) {
        var theta = Math.random() * Math.PI * 2;
        var phi = Math.acos(2 * Math.random() - 1);
        var r = cluster.size * (1.5 + Math.random() * 2.5);
        positions[i * 3] = cluster.pos.x + r * Math.sin(phi) * Math.cos(theta);
        positions[i * 3 + 1] = cluster.pos.y + r * Math.sin(phi) * Math.sin(theta) * 0.3;
        positions[i * 3 + 2] = cluster.pos.z + r * Math.cos(phi);
      }
      var pGeo = new THREE.BufferGeometry();
      pGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      var pMat = new THREE.PointsMaterial({
        color: cluster.color,
        size: cluster.name === 'central' ? 0.15 : 0.1,
        transparent: true,
        opacity: 0.7
      });
      var particles = new THREE.Points(pGeo, pMat);
      particles.position.copy(centerPos);
      particles.userData.rotSpeed = (Math.random() - 0.5) * 0.1;
      _objs.push(particles);
      _mats.push(pMat);
      scene.add(particles);
    });
  }

  // ── Void Bubbles ──────────────────────────────────────────────────────────
  function buildVoids() {
    var centerY = galacticY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    // Large void regions — areas of low matter density
    var voids = [
      { pos: new THREE.Vector3(12, 3, 5), radius: 5 },
      { pos: new THREE.Vector3(-10, -4, -6), radius: 4.5 }
    ];

    voids.forEach(function (v) {
      var voidGeo = new THREE.SphereGeometry(v.radius, 32, 32);
      var voidMat = new THREE.MeshBasicMaterial({
        color: 0x020408,
        transparent: true,
        opacity: 0.3,
        side: THREE.BackSide
      });
      var voidMesh = new THREE.Mesh(voidGeo, voidMat);
      voidMesh.position.copy(centerPos).add(v.pos);
      _objs.push(voidMesh);
      _mats.push(voidMat);
      scene.add(voidMesh);
    });
  }

  // ── Field Density Shell ───────────────────────────────────────────────────
  function buildFieldShell() {
    var centerY = galacticY();

    if (window.PropagationShaders) {
      var shellGeo = new THREE.SphereGeometry(16, 48, 48);
      var shellMat = window.PropagationShaders.createFieldDensityMaterial({
        density: 0.35,
        coherence: 0.65,
        fieldColor: 0x7c5cbf,
        cohColor: 0xffdd55,
        bgColor: 0x020408
      });
      var shell = new THREE.Mesh(shellGeo, shellMat);
      shell.position.set(5, centerY, 0);
      _objs.push(shell);
      _shaders.push(shellMat);
      scene.add(shell);
    }
  }

  // ── Distant Galaxy Field ─────────────────────────────────────────────────
  function buildDistantField() {
    var centerY = galacticY();
    var count = 600;
    var positions = new Float32Array(count * 3);

    for (var i = 0; i < count; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 18 + Math.random() * 10;
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
    }

    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var mat = new THREE.PointsMaterial({
      color: 0x7c5cbf,
      size: 0.08,
      transparent: true,
      opacity: 0.5,
      sizeAttenuation: true
    });
    var field = new THREE.Points(geo, mat);
    field.position.set(5, centerY, 0);
    field.userData.rotSpeed = 0.008;
    _objs.push(field);
    _mats.push(mat);
    scene.add(field);
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
    ctx.fillStyle = '#7c5cbf';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Galactic Scale — 10²¹ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, galacticY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.GalacticScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();

      // Volumetric medium fog
      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.006 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.006);
      }

      buildFilamentNetwork();
      buildGalaxyClusters();
      buildVoids();
      buildFieldShell();
      buildDistantField();
      buildLabel();

      // Camera setup
      camera.position.set(5, galacticY(), 35);
      camera.lookAt(5, galacticY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, galacticY(), 35),
        target: new THREE.Vector3(5, galacticY(), 0),
        fov: 48
      };
    },

    getSharedElements: function () {
      // Return filaments and clusters for wave morphing
      return _objs.filter(function (o) {
        return o.geometry && (
          o.geometry.type === 'TubeGeometry' ||
          o.geometry.type === 'SphereGeometry'
        );
      }).slice(0, 6);
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Galactic scene uses low LOD due to many particles
      return 2;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[GalacticScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      // Update shader uniforms
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      // Animate clusters
      _objs.forEach(function (o) {
        if (o.userData && o.userData.baseIntensity !== undefined && !o.userData.isCentral) {
          var pulse = 0.6 + 0.4 * Math.sin(time * o.userData.pulseSpeed + o.userData.phase);
          o.material.emissiveIntensity = o.userData.baseIntensity * pulse;
        }
        if (o.userData && o.userData.rotSpeed) {
          o.rotation.y += dt * o.userData.rotSpeed;
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
