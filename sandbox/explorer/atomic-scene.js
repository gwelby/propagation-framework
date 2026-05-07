/**
 * Atomic Scene — Electron Orbitals as Probability Clouds
 *
 * "The electron is not a particle that orbits. It is a standing wave
 *  that closes on itself at specific phases."
 *
 * At the atomic scale (10⁻¹⁰ m), the Bohr model breaks down and
 * quantum mechanics takes over. Electrons exist as probability
 * distributions — coherent patterns in the electron field.
 * Each orbital is a stationary state: a standing wave around the nucleus.
 *
 * Visual layers:
 *   1. Nucleus                    — the central proton (small but massive)
 *   2. 1s orbital                 — spherical probability cloud
 *   3. 2p orbitals                — dumbbell p-orbitals
 *   4. Electron probability shells — concentric probability zones
 *   5. Orbital transitions        — animated electron jumps
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;

  // ── Coordinate ────────────────────────────────────────────────────────────
  function atomicY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((-10 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Nucleus ───────────────────────────────────────────────────────────────
  function buildNucleus() {
    var centerY = atomicY();
    var centerPos = new THREE.Vector3(5, atomicY(), 0);

    // Proton sphere
    var protonGeo = new THREE.SphereGeometry(0.4, 32, 32);
    var protonMat = new THREE.MeshStandardMaterial({
      color: 0x0077b6,
      emissive: 0x0077b6,
      emissiveIntensity: 0.8,
      metalness: 0.3,
      roughness: 0.4
    });
    var proton = new THREE.Mesh(protonGeo, protonMat);
    proton.position.copy(centerPos);
    _objs.push(proton);
    _mats.push(protonMat);
    scene.add(proton);

    // Nuclear glow
    var glowGeo = new THREE.SphereGeometry(0.8, 24, 24);
    var glowMat = new THREE.MeshBasicMaterial({
      color: 0x0077b6,
      transparent: true,
      opacity: 0.15,
      side: THREE.BackSide
    });
    var glow = new THREE.Mesh(glowGeo, glowMat);
    glow.position.copy(centerPos);
    _objs.push(glow);
    _mats.push(glowMat);
    scene.add(glow);
  }

  // ── 1s Orbital — Spherical probability cloud ──────────────────────────────
  function build1sOrbital() {
    var centerY = atomicY();
    var centerPos = new THREE.Vector3(5, atomicY(), 0);

    // Create probability density using multiple concentric shells
    var shells = [1.5, 2.2, 2.8];
    shells.forEach(function (radius, i) {
      var shellGeo = new THREE.SphereGeometry(radius, 32, 32);
      var shellMat = new THREE.MeshBasicMaterial({
        color: 0x48cae4,
        transparent: true,
        opacity: 0.08 - i * 0.02,
        side: THREE.BackSide
      });
      var shell = new THREE.Mesh(shellGeo, shellMat);
      shell.position.copy(centerPos);
      shell.userData = { isOrbital: true, shell: i };
      _objs.push(shell);
      _mats.push(shellMat);
      scene.add(shell);
    });

    // Probability dots — electron position samples
    var dotCount = 400;
    var positions = new Float32Array(dotCount * 3);
    for (var i = 0; i < dotCount; i++) {
      // Random point in spherical distribution (1s has peak at Bohr radius)
      var u = Math.random();
      var r = -2.5 * Math.log(1 - u * 0.95); // Exponential distribution
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);

      positions[i * 3] = centerPos.x + r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = centerPos.y + r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
    }

    var dotsGeo = new THREE.BufferGeometry();
    dotsGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var dotsMat = new THREE.PointsMaterial({
      color: 0x69ff94,
      size: 0.06,
      transparent: true,
      opacity: 0.5
    });
    var dots = new THREE.Points(dotsGeo, dotsMat);
    dots.userData = { isProbabilityDots: true };
    _objs.push(dots);
    _mats.push(dotsMat);
    scene.add(dots);
  }

  // ── 2p Orbitals — Dumbbell probability clouds ───────────────────────────────
  function build2pOrbitals() {
    var centerY = atomicY();
    var centerPos = new THREE.Vector3(5, atomicY(), 0);

    // Three p-orbitals oriented along x, y, z axes
    var orientations = [
      { axis: new THREE.Vector3(1, 0, 0), color: 0xdd88ff },
      { axis: new THREE.Vector3(0, 1, 0), color: 0xff88dd },
      { axis: new THREE.Vector3(0, 0, 1), color: 0x88ddff }
    ];

    orientations.forEach(function (orient, i) {
      // Create dumbbell shape using two spheres
      var sphereGeo = new THREE.SphereGeometry(0.8, 24, 24);
      var sphereMat = new THREE.MeshBasicMaterial({
        color: orient.color,
        transparent: true,
        opacity: 0.12
      });

      var lobe1 = new THREE.Mesh(sphereGeo, sphereMat);
      lobe1.position.copy(centerPos).add(orient.axis.clone().multiplyScalar(1.8));
      _objs.push(lobe1);
      scene.add(lobe1);

      var lobe2 = new THREE.Mesh(sphereGeo, sphereMat);
      lobe2.position.copy(centerPos).add(orient.axis.clone().multiplyScalar(-1.8));
      _objs.push(lobe2);
      scene.add(lobe2);

      // Connecting bridge
      var bridgeGeo = new THREE.CylinderGeometry(0.3, 0.3, 3.6, 12);
      var bridgeMat = new THREE.MeshBasicMaterial({
        color: orient.color,
        transparent: true,
        opacity: 0.08
      });
      var bridge = new THREE.Mesh(bridgeGeo, bridgeMat);
      bridge.position.copy(centerPos);
      bridge.lookAt(centerPos.clone().add(orient.axis));
      bridge.rotateX(Math.PI / 2);
      bridge.userData = { isPOrbital: true, index: i };
      _objs.push(bridge);
      _mats.push(bridgeMat);
      scene.add(bridge);

      _mats.push(sphereMat);
    });
  }

  // ── Bohr Orbit Rings (historical reference) ───────────────────────────────
  function buildBohrRings() {
    var centerY = atomicY();
    var centerPos = new THREE.Vector3(5, atomicY(), 0);

    var radii = [3, 5, 7];
    radii.forEach(function (r, i) {
      var ringGeo = new THREE.TorusGeometry(r, 0.04, 6, 64);
      var ringMat = new THREE.MeshStandardMaterial({
        color: 0x0077b6,
        emissive: 0x0077b6,
        emissiveIntensity: 0.15,
        transparent: true,
        opacity: 0.25 - i * 0.05
      });
      var ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.copy(centerPos);
      ring.rotation.x = Math.PI / 2 + (i - 1) * 0.3;
      ring.userData = { isBohrRing: true, index: i };
      _objs.push(ring);
      _mats.push(ringMat);
      scene.add(ring);
    });
  }

  // ── Wave Field Background ─────────────────────────────────────────────────
  function buildWaveField() {
    var centerY = atomicY();

    if (window.PropagationShaders) {
      var fieldGeo = new THREE.PlaneGeometry(20, 14);
      var fieldMat = window.PropagationShaders.createWaveFieldMaterial({
        scale: 1.2,
        decay: 0.35,
        color1: 0x0077b6,
        color2: 0x00e5ff,
        bgColor: 0x020408
      });
      var field = new THREE.Mesh(fieldGeo, fieldMat);
      field.position.set(6, centerY, -4);
      _objs.push(field);
      _shaders.push(fieldMat);
      scene.add(field);
    }
  }

  // ── Electron Jump Visualization ───────────────────────────────────────────
  function buildElectronJump() {
    var centerY = atomicY();
    var centerPos = new THREE.Vector3(5, atomicY(), 0);

    // Electron particle that jumps between orbits
    var electronGeo = new THREE.SphereGeometry(0.15, 16, 16);
    var electronMat = new THREE.MeshStandardMaterial({
      color: 0x69ff94,
      emissive: 0x69ff94,
      emissiveIntensity: 1.0
    });
    var electron = new THREE.Mesh(electronGeo, electronMat);
    electron.position.copy(centerPos);
    electron.userData = {
      isElectron: true,
      orbitRadius: 3,
      orbitAngle: 0,
      targetRadius: 3
    };
    _objs.push(electron);
    _mats.push(electronMat);
    scene.add(electron);

    // Photon emission cone (appears during jumps)
    var photonGeo = new THREE.ConeGeometry(0.3, 1.5, 16, 1, true);
    var photonMat = new THREE.MeshBasicMaterial({
      color: 0xffff88,
      transparent: true,
      opacity: 0,
      side: THREE.DoubleSide
    });
    var photon = new THREE.Mesh(photonGeo, photonMat);
    photon.position.copy(centerPos);
    photon.rotation.x = -Math.PI / 2;
    photon.userData = { isPhoton: true, life: 0 };
    _objs.push(photon);
    _mats.push(photonMat);
    scene.add(photon);
  }

  // ── Energy Level Indicator ───────────────────────────────────────────────
  function buildEnergyLevels() {
    var centerY = atomicY();
    var centerPos = new THREE.Vector3(5, atomicY(), 0);

    // Horizontal lines showing energy levels
    var levels = [0, 2.5, 5];
    levels.forEach(function (y, i) {
      var lineGeo = new THREE.CylinderGeometry(0.02, 0.02, 4, 8);
      var lineMat = new THREE.MeshBasicMaterial({
        color: 0x0077b6,
        transparent: true,
        opacity: 0.3 - i * 0.08
      });
      var line = new THREE.Mesh(lineGeo, lineMat);
      line.position.copy(centerPos).add(new THREE.Vector3(6, y * 0.3 - 1, 0));
      line.rotation.z = Math.PI / 2;
      _objs.push(line);
      _mats.push(lineMat);
      scene.add(line);
    });
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
    ctx.fillStyle = '#0077b6';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Atomic Scale — 10⁻¹⁰ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, atomicY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.AtomicScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();

      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.02 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.02);
      }

      buildNucleus();
      build1sOrbital();
      build2pOrbitals();
      buildBohrRings();
      buildWaveField();
      buildElectronJump();
      buildEnergyLevels();
      buildLabel();

      camera.position.set(5, atomicY(), 20);
      camera.lookAt(5, atomicY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, atomicY(), 20),
        target: new THREE.Vector3(5, atomicY(), 0),
        fov: 55
      };
    },

    getSharedElements: function () {
      // Return Bohr rings and orbitals for wave morphing
      return _objs.filter(function (o) {
        return o.userData && (
          o.userData.isBohrRing ||
          o.userData.isOrbital
        );
      });
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Atomic scene uses high LOD for orbital detail
      return 0;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[AtomicScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      _objs.forEach(function (o) {
        // Rotate Bohr rings slowly
        if (o.userData && o.userData.isBohrRing) {
          o.rotation.z += dt * (0.1 + o.userData.index * 0.05);
        }
        // Pulsate orbitals
        if (o.userData && o.userData.isOrbital) {
          var pulse = 1 + 0.05 * Math.sin(time * 2 + o.userData.shell);
          o.scale.setScalar(pulse);
        }
        // Animate electron
        if (o.userData && o.userData.isElectron) {
          o.userData.orbitAngle += dt * 1.5;
          var r = o.userData.orbitRadius;
          o.position.x = 5 + Math.cos(o.userData.orbitAngle) * r;
          o.position.z = Math.sin(o.userData.orbitAngle) * r;
          o.position.y = atomicY() + Math.sin(time * 0.5) * 0.5;

          // Random jump to different orbit
          if (Math.random() < 0.005) {
            var orbits = [3, 5, 7];
            o.userData.orbitRadius = orbits[Math.floor(Math.random() * orbits.length)];
          }
        }
        // Animate photon emission
        if (o.userData && o.userData.isPhoton) {
          if (o.userData.life > 0) {
            o.userData.life -= dt;
            o.material.opacity = Math.max(0, o.userData.life);
            o.position.z += dt * 5;
          } else if (Math.random() < 0.01) {
            o.userData.life = 0.5;
            o.material.opacity = 0.6;
            o.position.set(5, atomicY(), 0);
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
