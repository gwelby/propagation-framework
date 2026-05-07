/**
 * Nuclear Scene — Nucleons and Quark Confinement
 *
 * "The nucleus is a bag of quarks held together by the strong force.
 *  Quarks cannot be isolated — they are confined by the very
 *  nature of the strong field."
 *
 * At the nuclear scale (10⁻¹⁵ m), protons and neutrons cluster together,
 * bound by the residual strong force. Inside each nucleon, quarks are
 * confined by gluon exchange — the force actually strengthens with distance.
 *
 * Visual layers:
 *   1. Proton-neutron cluster     — the nucleus as a whole
 *   2. Individual nucleons       — protons (red) and neutrons (blue)
 *   3. Quark structure           — three quarks per nucleon
 *   4. Gluon field lines         — the strong force binding
 *   5. Confinement shell         — the bag model boundary
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;
  var _nucleons = [];

  // ── Coordinate ────────────────────────────────────────────────────────────
  function nuclearY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((-15 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Nucleus — Cluster of Nucleons ────────────────────────────────────────
  function buildNucleus() {
    var centerY = nuclearY();
    var centerPos = new THREE.Vector3(5, nuclearY(), 0);

    // Alpha particle: 2 protons, 2 neutrons
    var nucleonData = [
      { type: 'proton', offset: new THREE.Vector3(0.8, 0.5, 0.3), color: 0xff6b6b },
      { type: 'proton', offset: new THREE.Vector3(-0.6, -0.7, 0.5), color: 0xff6b6b },
      { type: 'neutron', offset: new THREE.Vector3(-0.7, 0.6, -0.4), color: 0x4488ff },
      { type: 'neutron', offset: new THREE.Vector3(0.5, -0.5, -0.6), color: 0x4488ff }
    ];

    nucleonData.forEach(function (data, i) {
      var nucleon = buildNucleon(data.type, data.color, i);
      nucleon.position.copy(centerPos).add(data.offset);
      nucleon.userData.baseOffset = data.offset.clone();
      nucleon.userData.index = i;
      _nucleons.push(nucleon);
      scene.add(nucleon);
    });

    // Nuclear binding field — the residual strong force between nucleons
    var bindingGeo = new THREE.SphereGeometry(2.5, 32, 32);
    var bindingMat = new THREE.MeshBasicMaterial({
      color: 0x0096c7,
      transparent: true,
      opacity: 0.08,
      side: THREE.BackSide
    });
    var binding = new THREE.Mesh(bindingGeo, bindingMat);
    binding.position.copy(centerPos);
    _objs.push(binding);
    _mats.push(bindingMat);
    scene.add(binding);
  }

  // ── Individual Nucleon (Proton or Neutron) ────────────────────────────────
  function buildNucleon(type, color, index) {
    var group = new THREE.Group();

    // Nucleon shell (the "bag")
    var shellGeo = new THREE.SphereGeometry(1, 32, 32);
    var shellMat = new THREE.MeshStandardMaterial({
      color: color,
      emissive: color,
      emissiveIntensity: 0.4,
      transparent: true,
      opacity: 0.6,
      metalness: 0.3,
      roughness: 0.4
    });
    var shell = new THREE.Mesh(shellGeo, shellMat);
    group.add(shell);
    _objs.push(shell);
    _mats.push(shellMat);

    // Three quarks inside
    var quarkColors = type === 'proton'
      ? [0xff0000, 0x00ff00, 0x0000ff] // u u d (red, green, blue)
      : [0xff0000, 0x0000ff, 0x00ff00]; // u d d

    quarkColors.forEach(function (qc, q) {
      var quarkGeo = new THREE.SphereGeometry(0.25, 16, 16);
      var quarkMat = new THREE.MeshStandardMaterial({
        color: qc,
        emissive: qc,
        emissiveIntensity: 0.6
      });
      var quark = new THREE.Mesh(quarkGeo, quarkMat);
      // Quarks orbit inside nucleon
      var angle = (q / 3) * Math.PI * 2 + index;
      quark.position.set(
        Math.cos(angle) * 0.5,
        Math.sin(angle) * 0.4,
        (Math.random() - 0.5) * 0.3
      );
      quark.userData = {
        isQuark: true,
        orbitAngle: angle,
        orbitSpeed: 2 + q * 0.5,
        orbitRadius: 0.5
      };
      group.add(quark);
      _objs.push(quark);
      _mats.push(quarkMat);
    });

    // Gluon glow around quarks
    var gluonGeo = new THREE.SphereGeometry(0.6, 16, 16);
    var gluonMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.1,
      side: THREE.BackSide
    });
    var gluon = new THREE.Mesh(gluonGeo, gluonMat);
    group.add(gluon);
    _objs.push(gluon);
    _mats.push(gluonMat);

    return group;
  }

  // ── Gluon Field Lines ─────────────────────────────────────────────────────
  function buildGluonField() {
    var centerY = nuclearY();
    var centerPos = new THREE.Vector3(5, nuclearY(), 0);

    // Field lines connecting nucleons
    var connections = [[0, 1], [0, 2], [1, 3], [2, 3], [0, 3], [1, 2]];

    connections.forEach(function (conn, i) {
      var lineGeo = new THREE.CylinderGeometry(0.04, 0.04, 1, 8);
      var lineMat = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.2
      });
      var line = new THREE.Mesh(lineGeo, lineMat);
      line.position.copy(centerPos);
      line.userData = {
        isGluonLine: true,
        connIndex: i,
        nucleonA: conn[0],
        nucleonB: conn[1],
        phase: Math.random() * Math.PI * 2
      };
      _objs.push(line);
      _mats.push(lineMat);
      scene.add(line);
    });
  }

  // ── Confinement Visualization ──────────────────────────────────────────────
  function buildConfinement() {
    var centerY = nuclearY();
    var centerPos = new THREE.Vector3(5, nuclearY(), 0);

    // Use FieldDensity shader if available
    if (window.PropagationShaders) {
      var confineGeo = new THREE.SphereGeometry(3.5, 48, 48);
      var confineMat = window.PropagationShaders.createFieldDensityMaterial({
        density: 0.6,
        coherence: 0.8,
        fieldColor: 0x0096c7,
        cohColor: 0x00e5ff,
        bgColor: 0x020408
      });
      var confine = new THREE.Mesh(confineGeo, confineMat);
      confine.position.copy(centerPos);
      _objs.push(confine);
      _shaders.push(confineMat);
      scene.add(confine);
    }
  }

  // ── Virtual Pion Cloud ────────────────────────────────────────────────────
  // The residual strong force is mediated by virtual pions
  function buildPionCloud() {
    var centerY = nuclearY();
    var centerPos = new THREE.Vector3(5, nuclearY(), 0);

    var pionCount = 30;
    for (var i = 0; i < pionCount; i++) {
      var pionGeo = new THREE.SphereGeometry(0.1, 8, 8);
      var pionMat = new THREE.MeshBasicMaterial({
        color: 0x99ff99,
        transparent: true,
        opacity: 0.4
      });
      var pion = new THREE.Mesh(pionGeo, pionMat);

      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 3 + Math.random() * 2;
      pion.position.set(
        centerPos.x + r * Math.sin(phi) * Math.cos(theta),
        centerPos.y + r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      );

      pion.userData = {
        isPion: true,
        life: Math.random() * 2,
        maxLife: 1 + Math.random()
      };
      _objs.push(pion);
      _mats.push(pionMat);
      scene.add(pion);
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
    ctx.fillStyle = '#0096c7';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Nuclear Scale — 10⁻¹⁵ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, nuclearY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.NuclearScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();
      _nucleons = [];

      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.025 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.025);
      }

      buildNucleus();
      buildGluonField();
      buildConfinement();
      buildPionCloud();
      buildLabel();

      camera.position.set(5, nuclearY(), 15);
      camera.lookAt(5, nuclearY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, nuclearY(), 15),
        target: new THREE.Vector3(5, nuclearY(), 0),
        fov: 55
      };
    },

    getSharedElements: function () {
      // Return nucleons and gluon lines for wave morphing
      return _objs.filter(function (o) {
        return o.userData && (
          o.userData.isGluonLine ||
          o.userData.isNucleon
        );
      });
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Nuclear scene uses medium LOD
      return 1;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[NuclearScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      // Update nucleon positions
      _nucleons.forEach(function (nucleon, i) {
        var floatX = Math.sin(time * 0.5 + i) * 0.1;
        var floatY = Math.cos(time * 0.7 + i * 1.3) * 0.1;
        var floatZ = Math.sin(time * 0.3 + i * 0.7) * 0.1;
        nucleon.position.x = 5 + nucleon.userData.baseOffset.x + floatX;
        nucleon.position.y = nuclearY() + nucleon.userData.baseOffset.y + floatY;
        nucleon.position.z = nucleon.userData.baseOffset.z + floatZ;

        // Rotate quarks inside nucleon
        nucleon.children.forEach(function (child) {
          if (child.userData && child.userData.isQuark) {
            child.userData.orbitAngle += dt * child.userData.orbitSpeed;
            child.position.x = Math.cos(child.userData.orbitAngle) * child.userData.orbitRadius;
            child.position.y = Math.sin(child.userData.orbitAngle) * child.userData.orbitRadius * 0.8;
          }
        });
      });

      // Update gluon field lines
      _objs.forEach(function (o) {
        if (o.userData && o.userData.isGluonLine) {
          var na = _nucleons[o.userData.nucleonA];
          var nb = _nucleons[o.userData.nucleonB];
          if (na && nb) {
            var mid = new THREE.Vector3().addVectors(na.position, nb.position).multiplyScalar(0.5);
            var dist = na.position.distanceTo(nb.position);
            o.position.copy(mid);
            o.lookAt(nb.position);
            o.rotateX(Math.PI / 2);
            o.scale.y = dist;
            // Pulsate opacity
            o.material.opacity = 0.15 + 0.1 * Math.sin(time * 3 + o.userData.phase);
          }
        }
        // Animate pions
        if (o.userData && o.userData.isPion) {
          o.userData.life -= dt;
          o.material.opacity = Math.max(0, o.userData.life / o.userData.maxLife * 0.4);
          if (o.userData.life <= 0) {
            // Respawn
            o.userData.life = o.userData.maxLife;
            var theta = Math.random() * Math.PI * 2;
            var phi = Math.acos(2 * Math.random() - 1);
            var r = 3 + Math.random() * 2;
            o.position.set(
              5 + r * Math.sin(phi) * Math.cos(theta),
              nuclearY() + r * Math.sin(phi) * Math.sin(theta),
              r * Math.cos(phi)
            );
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
      _nucleons = [];
      _objs = [];
      _mats = [];
      _shaders = [];
      if (scene) scene.fog = null;
    }
  };
}());
