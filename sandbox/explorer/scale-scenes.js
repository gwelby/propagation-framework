/**
 * Scale Scenes — Per-scale Three.js Scene Configurations
 * 
 * Each scale registers a scene object with the ScaleEngine.
 * The engine activates/deactivates scenes as the user navigates.
 * 
 * Scene object shape:
 *   {
 *     activate(scene, camera) — called when this scale becomes active
 *     deactivate()            — called when leaving this scale
 *     update(dt, time)        — called each frame (optional)
 *     dispose()               — cleanup (optional)
 *   }
 * 
 * Scale visual taxonomy:
 *   Planck (-35)     → FieldDensity (quantum foam, discrete geometry)
 *   GUT (-25)        → WaveField (force unification as merging waves)
 *   Matter (-18)     → HelixRibbon (standing wave = mass)
 *   Atomic (-10)     → WaveField (Bohr orbits as phase closure)
 *   Molecular (-9)    → WaveField (covalent bonds as locked phases)
 *   Cellular (-5)    → FieldDensity (active coherence maintenance)
 *   Neural (-3)      → WaveField (neural coherence oscillations)
 *   Cosmic (+26)     → FieldDensity (cosmic web as frozen pattern)
 */

(function () {
  'use strict';

  var _scene, _camera;
  var _activeObjects = [];
  var _activeMaterials = [];

  function track(mesh, mat) {
    _activeObjects.push(mesh);
    if (mat) _activeMaterials.push(mat);
  }

  function clearScene() {
    _activeObjects.forEach(function (o) {
      if (o.geometry) o.geometry.dispose();
      if (o.material) {
        if (Array.isArray(o.material)) {
          o.material.forEach(function (m) { m.dispose(); });
        } else {
          o.material.dispose();
        }
        }
      _scene.remove(o);
    });
    _activeObjects = [];
    _activeMaterials = [];
  }

  // ── Scale Scene Definitions ──────────────────────────────────────────────

  var scenes = {

    planck: window.PlanckScene || null,

    'quantum-foam': {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var count = 120;
        for (var i = 0; i < count; i++) {
          var r = 3 + Math.random() * 7;
          var theta = Math.random() * Math.PI * 2;
          var phi = Math.acos(2 * Math.random() - 1);
          var geo = new THREE.SphereGeometry(0.15 + Math.random() * 0.25, 12, 12);
          var mat = new THREE.MeshStandardMaterial({
            color: 0xd4a017,
            emissive: 0xd4a017,
            emissiveIntensity: 0.4 + Math.random() * 0.4,
            transparent: true,
            opacity: 0.6 + Math.random() * 0.3
          });
          var mesh = new THREE.Mesh(geo, mat);
          mesh.position.set(
            r * Math.sin(phi) * Math.cos(theta),
            metersToY(1e-33) + (Math.random() - 0.5) * 6,
            r * Math.sin(phi) * Math.sin(theta)
          );
          mesh.userData.baseIntensity = mat.emissiveIntensity;
          mesh.userData.phase = Math.random() * Math.PI * 2;
          track(mesh, mat);
          scene.add(mesh);
        }
        addScaleLabel(scene, 'Quantum Foam — 10⁻³³ m', new THREE.Vector3(8, metersToY(1e-33), 0), 0xd4a017);
      },

      update: function (dt, time) {
        _activeObjects.forEach(function (o) {
          if (o.userData.baseIntensity !== undefined) {
            o.material.emissiveIntensity = o.userData.baseIntensity * (0.6 + 0.4 * Math.sin(time * 2 + o.userData.phase));
          }
        });
      },

      getSharedElements: function () {
        return _activeObjects.slice(0, 8);
      },

      getLODLevel: function () {
        return 1;
      },

      prepare: function (lodSettings) {
        if (lodSettings) {
          console.log('[QuantumFoamScene] Preparing with LOD:', lodSettings);
        }
      },

      deactivate: clearScene,
      dispose: clearScene
    },

    proton: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var pos = new THREE.Vector3(5, metersToY(1e-15), 0);

        // Central proton glow
        var coreGeo = new THREE.SphereGeometry(1.2, 32, 32);
        var coreMat = new THREE.MeshStandardMaterial({
          color: 0x00b4d8,
          emissive: 0x00b4d8,
          emissiveIntensity: 0.6,
          transparent: true,
          opacity: 0.8
        });
        var core = new THREE.Mesh(coreGeo, coreMat);
        core.position.copy(pos);
        track(core, coreMat);
        scene.add(core);

        // Three quarks (up, up, down) in triangular arrangement
        var quarkColors = [0xff6b6b, 0x69ff94, 0x4488ff];
        var quarkPositions = [
          new THREE.Vector3(0, 1.8, 0),
          new THREE.Vector3(1.56, -0.9, 0),
          new THREE.Vector3(-1.56, -0.9, 1.2)
        ];
        quarkPositions.forEach(function (offset, i) {
          var qGeo = new THREE.SphereGeometry(0.35, 24, 24);
          var qMat = new THREE.MeshStandardMaterial({
            color: quarkColors[i],
            emissive: quarkColors[i],
            emissiveIntensity: 0.7
          });
          var quark = new THREE.Mesh(qGeo, qMat);
          quark.position.copy(pos).add(offset);
          quark.userData.baseOffset = offset.clone();
          quark.userData.phase = i * Math.PI * 2 / 3;
          track(quark, qMat);
          scene.add(quark);

          // Gluon field line to center
          var lineGeo = new THREE.CylinderGeometry(0.03, 0.03, offset.length(), 8);
          var lineMat = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            transparent: true,
            opacity: 0.4
          });
          var line = new THREE.Mesh(lineGeo, lineMat);
          line.position.copy(pos).add(offset.clone().multiplyScalar(0.5));
          line.lookAt(pos.clone().add(offset));
          line.rotateX(Math.PI / 2);
          line.userData.quarkIndex = i;
          track(line, lineMat);
          scene.add(line);
        });

        // Confinement field shell
        var shellGeo = new THREE.SphereGeometry(2.5, 48, 48);
        var shellMat = window.PropagationShaders.createFieldDensityMaterial({
          density: 0.5,
          coherence: 0.8,
          fieldColor: 0x00b4d8,
          cohColor: 0x00e5ff,
          bgColor: 0x020408
        });
        var shell = new THREE.Mesh(shellGeo, shellMat);
        shell.position.copy(pos);
        track(shell, shellMat);
        scene.add(shell);

        addScaleLabel(scene, 'Proton Scale — 10⁻¹⁵ m', pos, 0x00b4d8);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
        // Orbit quarks around center
        _activeObjects.forEach(function (o) {
          if (o.userData.baseOffset) {
            var speed = 2.0;
            var angle = time * speed + o.userData.phase;
            var radius = 1.5;
            o.position.x = _activeObjects[0].position.x + Math.cos(angle) * radius;
            o.position.z = _activeObjects[0].position.z + Math.sin(angle) * radius;
          }
        });
      },

      getSharedElements: function () {
        return _activeObjects.slice(0, 4);
      },

      getLODLevel: function () {
        return 0;
      },

      prepare: function (lodSettings) {
        if (lodSettings) {
          console.log('[ProtonScene] Preparing with LOD:', lodSettings);
        }
      },

      deactivate: clearScene,
      dispose: clearScene
    },

    gut: window.GUTScene || null,

    matter: window.ComptonScene || null,

    atomic: window.AtomicScene || null,

    molecular: window.MolecularScene || null,

    virus: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        // Icosahedral virus shell
        var geo = new THREE.IcosahedronGeometry(4, 1);
        var mat = new THREE.MeshStandardMaterial({
          color: 0x69ff94,
          emissive: 0x69ff94,
          emissiveIntensity: 0.3,
          metalness: 0.6,
          roughness: 0.35,
          wireframe: false
        });
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(5, metersToY(1e-7), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Surface spikes
        var spikeCount = 20;
        for (var i = 0; i < spikeCount; i++) {
          var theta = Math.random() * Math.PI * 2;
          var phi = Math.acos(2 * Math.random() - 1);
          var x = Math.sin(phi) * Math.cos(theta);
          var y = Math.sin(phi) * Math.sin(theta);
          var z = Math.cos(phi);
          var spikeGeo = new THREE.CylinderGeometry(0.04, 0.1, 1.2, 6);
          var spikeMat = new THREE.MeshStandardMaterial({
            color: 0x69ff94,
            emissive: 0x80ed99,
            emissiveIntensity: 0.4,
            transparent: true,
            opacity: 0.8
          });
          var spike = new THREE.Mesh(spikeGeo, spikeMat);
          spike.position.set(
            mesh.position.x + x * 4.5,
            mesh.position.y + y * 4.5,
            mesh.position.z + z * 4.5
          );
          spike.lookAt(new THREE.Vector3(
            mesh.position.x + x * 10,
            mesh.position.y + y * 10,
            mesh.position.z + z * 10
          ));
          spike.userData.rotSpeed = (Math.random() - 0.5) * 0.5;
          track(spike, spikeMat);
          scene.add(spike);
        }
        addScaleLabel(scene, 'Virus Scale — 10⁻⁷ m', mesh.position, 0x69ff94);
      },

      update: function (dt, time) {
        _activeObjects.forEach(function (o) {
          if (o.userData.rotSpeed) {
            o.rotation.x += dt * o.userData.rotSpeed;
            o.rotation.y += dt * o.userData.rotSpeed * 0.7;
          } else if (o.geometry && o.geometry.type === 'IcosahedronGeometry') {
            o.rotation.y += dt * 0.08;
          }
        });
      },

      getSharedElements: function () {
        return _activeObjects.slice(0, 5);
      },

      getLODLevel: function () {
        return 1;
      },

      prepare: function (lodSettings) {
        if (lodSettings) {
          console.log('[VirusScene] Preparing with LOD:', lodSettings);
        }
      },

      deactivate: clearScene,
      dispose: clearScene
    },

    cellular: window.CellularScene || null,

    neural: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var mat = window.PropagationShaders.createWaveFieldMaterial({
          scale: 0.4,
          decay: 0.2,
          color1: 0xffdd55,
          color2: 0xffb347,
          bgColor: 0x020408
        });
        var geo = new THREE.PlaneGeometry(20, 14);
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(6, metersToY(1e-2), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Neural node network
        var nodePositions = [
          [-4, 2], [-2, -1], [0, 3], [2, 1], [4, -2],
          [-3, -3], [1, -3], [3, 3]
        ];
        nodePositions.forEach(function (p) {
          var nodeGeo = new THREE.SphereGeometry(0.3, 12, 12);
          var nodeMat = new THREE.MeshStandardMaterial({
            color: 0xffdd55,
            emissive: 0xffdd55,
            emissiveIntensity: 0.6,
            transparent: true,
            opacity: 0.85
          });
          var node = new THREE.Mesh(nodeGeo, nodeMat);
          node.position.set(mesh.position.x + p[0], mesh.position.y + p[1], 0.5);
          node.userData.phase = Math.random() * Math.PI * 2;
          track(node, nodeMat);
          scene.add(node);
        });
        addScaleLabel(scene, 'Neural Scale — 10⁻² m', mesh.position, 0xffdd55);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
        _activeObjects.forEach(function (o) {
          if (o.userData.phase !== undefined) {
            var pulse = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(time * 3 + o.userData.phase));
            o.material.emissiveIntensity = pulse;
          }
        });
      },

      getSharedElements: function () {
        return _activeObjects.slice(0, 6);
      },

      getLODLevel: function () {
        return 1;
      },

      prepare: function (lodSettings) {
        if (lodSettings) {
          console.log('[NeuralScene] Preparing with LOD:', lodSettings);
        }
      },

      deactivate: clearScene,
      dispose: clearScene
    },

    human: window.HumanScene || null,

    planetary: window.PlanetaryScene || null,

    stellar: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var geo = new THREE.SphereGeometry(6, 48, 48);
        var mat = new THREE.MeshStandardMaterial({
          color: 0xff6b6b,
          emissive: 0xff6b6b,
          emissiveIntensity: 0.8,
          metalness: 0.2,
          roughness: 0.4
        });
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(5, metersToY(1e9), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Corona glow
        var coronaGeo = new THREE.SphereGeometry(7.5, 32, 32);
        var coronaMat = new THREE.MeshBasicMaterial({
          color: 0xff6b6b,
          transparent: true,
          opacity: 0.06,
          side: THREE.BackSide
        });
        var corona = new THREE.Mesh(coronaGeo, coronaMat);
        corona.position.copy(mesh.position);
        track(corona, coronaMat);
        scene.add(corona);

        addScaleLabel(scene, 'Stellar Scale — 10⁹ m', mesh.position, 0xff6b6b);
      },

      update: function (dt, time) {
        if (_activeObjects[0]) {
          _activeObjects[0].material.emissiveIntensity = 0.7 + 0.15 * Math.sin(time * 1.5);
        }
      },

      getSharedElements: function () {
        return _activeObjects.slice(0, 2);
      },

      getLODLevel: function () {
        return 2;
      },

      prepare: function (lodSettings) {
        if (lodSettings) {
          console.log('[StellarScene] Preparing with LOD:', lodSettings);
        }
      },

      deactivate: clearScene,
      dispose: clearScene
    },

    galactic: window.GalacticScene || null,

    nuclear: window.NuclearScene || null,

    cosmic: window.CosmicScene || null,
  };

  // Scales with no custom scene use the default node only
  var noCustomScene = [];

  // ── Helpers ────────────────────────────────────────────────────────────────

  function metersToY(meters) {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    var LOG_RANGE = LOG_MAX - LOG_MIN;
    var BEAM_LENGTH = 100;
    var logM = Math.log10(meters);
    return ((logM - LOG_MIN) / LOG_RANGE) * BEAM_LENGTH;
  }

  function addScaleLabel(scene, text, position, color) {
    if (!window.ScaleEngine) return;
    var canvas = document.createElement('canvas');
    canvas.width = 480;
    canvas.height = 80;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 480, 80);
    var hex = '#' + color.toString(16).padStart(6, '0');
    ctx.font = 'bold 28px DM Sans, sans-serif';
    ctx.fillStyle = hex;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 8, 40);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(position.x + position.y * 0.05 + 6, position.y, position.z + 3);
    sprite.scale.set(18, 3.5, 1);
    scene.add(sprite);
  }

  // ── Registration ──────────────────────────────────────────────────────────

  function registerScenes() {
    if (!window.ScaleEngine) {
      console.warn('[scale-scenes] ScaleEngine not found — skipping registration');
      return;
    }
    Object.keys(scenes).forEach(function (scaleId) {
      window.ScaleEngine.registerScene(scaleId, scenes[scaleId]);
    });
    console.log('[scale-scenes] Registered', Object.keys(scenes).length, 'custom scale scenes');
  }

  // Auto-register when ScaleEngine is ready
  if (window.ScaleEngine) {
    registerScenes();
  } else {
    window.addEventListener('DOMContentLoaded', function () {
      setTimeout(registerScenes, 100);
    });
  }
}());
