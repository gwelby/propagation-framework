/**
 * Compton Scene — Standing Wave Patterns (Matter as Waves)
 *
 * "Matter is not made of particles. It is made of standing waves
 *  in the propagation medium. Mass is frequency."
 *
 * At the Compton scale (10⁻¹⁸ m), the wave nature of matter becomes
 * undeniable. The Compton wavelength λ = h/mc defines the spatial
 * scale of quantum interference for a particle of mass m.
 * This is where matter reveals itself as coherent propagation.
 *
 * Visual layers:
 *   1. Standing wave helix      — the matter wave locked in phase
 *   2. Propagation fronts       — wave crests moving through medium
 *   3. Phase closure ring       — where the wave meets itself
 *   4. Compton wavelength ring  — λ_c = h/mc visualization
 *   5. Rest mass energy field   — E = mc² as coherence intensity
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;

  // ── Coordinate ────────────────────────────────────────────────────────────
  function comptonY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((-18 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Standing Wave Helix ───────────────────────────────────────────────────
  function buildStandingWaveHelix() {
    var centerY = comptonY();
    var centerPos = new THREE.Vector3(5, comptonY(), 0);

    // Create a helical standing wave using TubeGeometry
    var turns = 6;
    var radius = 1.5;
    var pitch = 0.8;
    var points = [];
    var segments = 120;

    for (var i = 0; i <= segments; i++) {
      var t = i / segments;
      var angle = t * turns * Math.PI * 2;
      var x = radius * Math.cos(angle);
      var y = (t - 0.5) * turns * pitch;
      var z = radius * Math.sin(angle);
      points.push(new THREE.Vector3(x, y, z));
    }

    var curve = new THREE.CatmullRomCurve3(points);
    var helixGeo = new THREE.TubeGeometry(curve, segments, 0.15, 12, false);
    var helixMat = new THREE.MeshStandardMaterial({
      color: 0x00e5ff,
      emissive: 0x00e5ff,
      emissiveIntensity: 0.6,
      metalness: 0.7,
      roughness: 0.25,
      transparent: true,
      opacity: 0.9
    });
    var helix = new THREE.Mesh(helixGeo, helixMat);
    helix.position.copy(centerPos);
    helix.userData = { isHelix: true, phase: 0 };
    _objs.push(helix);
    _mats.push(helixMat);
    scene.add(helix);

    // Counter-rotating helix (standing wave has two components)
    var helix2 = helix.clone();
    helix2.rotation.y = Math.PI;
    helix2.userData = { isHelix: true, phase: Math.PI };
    _objs.push(helix2);
    scene.add(helix2);
  }

  // ── Propagation Wave Fronts ─────────────────────────────────────────────
  function buildWaveFronts() {
    var centerY = comptonY();
    var centerPos = new THREE.Vector3(5, comptonY(), 0);

    // Concentric wave rings emanating from the standing wave
    for (var i = 0; i < 5; i++) {
      var ringGeo = new THREE.RingGeometry(
        2.5 + i * 0.8,
        2.5 + i * 0.8 + 0.15,
        64
      );
      var ringMat = new THREE.MeshBasicMaterial({
        color: 0x69ff94,
        transparent: true,
        opacity: 0.15 - i * 0.025,
        side: THREE.DoubleSide
      });
      var ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.copy(centerPos);
      ring.rotation.x = Math.PI / 2;
      ring.userData = {
        isWaveFront: true,
        index: i,
        baseRadius: 2.5 + i * 0.8,
        phase: i * Math.PI / 3
      };
      _objs.push(ring);
      _mats.push(ringMat);
      scene.add(ring);
    }
  }

  // ── Phase Closure Visualization ─────────────────────────────────────────
  function buildPhaseClosure() {
    var centerY = comptonY();
    var centerPos = new THREE.Vector3(5, comptonY(), 0);

    // The phase closure happens where the wave meets itself
    var closureGeo = new THREE.TorusGeometry(2.2, 0.06, 8, 64);
    var closureMat = new THREE.MeshStandardMaterial({
      color: 0xffdd55,
      emissive: 0xffdd55,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.6
    });
    var closure = new THREE.Mesh(closureGeo, closureMat);
    closure.position.copy(centerPos);
    closure.rotation.x = Math.PI / 2;
    closure.userData = { isClosure: true };
    _objs.push(closure);
    _mats.push(closureMat);
    scene.add(closure);

    // Phase indicator dots
    for (var i = 0; i < 12; i++) {
      var dotGeo = new THREE.SphereGeometry(0.08, 8, 8);
      var dotMat = new THREE.MeshBasicMaterial({
        color: 0xffdd55,
        transparent: true,
        opacity: 0.7
      });
      var dot = new THREE.Mesh(dotGeo, dotMat);
      var angle = (i / 12) * Math.PI * 2;
      dot.position.set(
        centerPos.x + Math.cos(angle) * 2.2,
        centerPos.y,
        Math.sin(angle) * 2.2
      );
      dot.userData = {
        isPhaseDot: true,
        angle: angle,
        index: i
      };
      _objs.push(dot);
      _mats.push(dotMat);
      scene.add(dot);
    }
  }

  // ── Compton Wavelength Ring ─────────────────────────────────────────────
  function buildComptonRing() {
    var centerY = comptonY();
    var centerPos = new THREE.Vector3(5, comptonY(), 0);

    // λ_c = h/mc — the fundamental length scale
    var ringGeo = new THREE.TorusGeometry(3.8, 0.08, 12, 96);
    var ringMat = new THREE.MeshStandardMaterial({
      color: 0x00b4d8,
      emissive: 0x00b4d8,
      emissiveIntensity: 0.4,
      transparent: true,
      opacity: 0.5
    });
    var ring = new THREE.Mesh(ringGeo, ringMat);
    ring.position.copy(centerPos);
    ring.rotation.x = Math.PI / 2;
    ring.userData = { isComptonRing: true };
    _objs.push(ring);
    _mats.push(ringMat);
    scene.add(ring);

    // Wave number indicator
    var waveNumGeo = new THREE.CylinderGeometry(0.04, 0.04, 3.8, 8);
    var waveNumMat = new THREE.MeshBasicMaterial({
      color: 0x00e5ff,
      transparent: true,
      opacity: 0.3
    });
    var waveNum = new THREE.Mesh(waveNumGeo, waveNumMat);
    waveNum.position.copy(centerPos);
    waveNum.rotation.z = Math.PI / 2;
    _objs.push(waveNum);
    _mats.push(waveNumMat);
    scene.add(waveNum);
  }

  // ── Rest Mass Energy Field ───────────────────────────────────────────────
  function buildEnergyField() {
    var centerY = comptonY();

    if (window.PropagationShaders) {
      var fieldGeo = new THREE.SphereGeometry(5, 48, 48);
      var fieldMat = window.PropagationShaders.createFieldDensityMaterial({
        density: 0.45,
        coherence: 0.75,
        fieldColor: 0x00e5ff,
        cohColor: 0x69ff94,
        bgColor: 0x020408
      });
      var field = new THREE.Mesh(fieldGeo, fieldMat);
      field.position.set(5, centerY, 0);
      field.userData = { isEnergyField: true };
      _objs.push(field);
      _shaders.push(fieldMat);
      scene.add(field);
    } else {
      // Fallback without shaders
      var fallbackGeo = new THREE.SphereGeometry(5, 32, 32);
      var fallbackMat = new THREE.MeshBasicMaterial({
        color: 0x00e5ff,
        transparent: true,
        opacity: 0.1,
        side: THREE.BackSide
      });
      var fallback = new THREE.Mesh(fallbackGeo, fallbackMat);
      fallback.position.set(5, centerY, 0);
      _objs.push(fallback);
      _mats.push(fallbackMat);
      scene.add(fallback);
    }
  }

  // ── Standing Wave Shader Plane ──────────────────────────────────────────
  function buildWaveShaderPlane() {
    var centerY = comptonY();

    var geo = new THREE.PlaneGeometry(14, 14);
    var mat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
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
        'uniform vec3 uColor;',
        'varying vec2 vUv;',

        'void main() {',
        '  vec2 p = vUv - 0.5;',
        '  float r = length(p);',
        '  float theta = atan(p.y, p.x);',

        // Standing wave: sin(kr) * cos(ωt) with angular modulation
        '  float standing = sin(r * 15.0) * cos(uTime * 2.0);',
        '  float angular = sin(theta * 3.0 + uTime * 0.5);',
        '  float wave = standing * angular * 0.5 + 0.5;',

        // Radial fade
        '  float fade = 1.0 - smoothstep(0.3, 0.5, r);',

        '  float alpha = wave * fade * 0.3;',
        '  gl_FragColor = vec4(uColor * (0.5 + wave * 0.5), alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      depthWrite: false,
      side: THREE.DoubleSide
    });
    var mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(5, centerY, 0);
    mesh.rotation.x = -Math.PI / 2;
    _objs.push(mesh);
    _shaders.push(mat);
    scene.add(mesh);
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
    ctx.fillStyle = '#00e5ff';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Compton Scale — 10⁻¹⁸ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, comptonY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.ComptonScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();

      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.02 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.02);
      }

      buildStandingWaveHelix();
      buildWaveFronts();
      buildPhaseClosure();
      buildComptonRing();
      buildEnergyField();
      buildWaveShaderPlane();
      buildLabel();

      camera.position.set(5, comptonY(), 20);
      camera.lookAt(5, comptonY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, comptonY(), 20),
        target: new THREE.Vector3(5, comptonY(), 0),
        fov: 60
      };
    },

    getSharedElements: function () {
      // Return standing wave helix and wave fronts for morphing
      return _objs.filter(function (o) {
        return o.userData && (
          o.userData.isHelix ||
          o.userData.isWaveFront ||
          o.userData.isComptonRing
        );
      });
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Compton scene uses high LOD for wave detail
      return 0;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[ComptonScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      _objs.forEach(function (o) {
        // Rotate helices
        if (o.userData && o.userData.isHelix) {
          o.rotation.y += dt * 0.3 * (o.userData.phase > 0 ? -1 : 1);
        }
        // Expand wave fronts
        if (o.userData && o.userData.isWaveFront) {
          var expansion = 1 + 0.15 * Math.sin(time * 2 + o.userData.phase);
          var newRadius = o.userData.baseRadius * expansion;
          o.geometry.dispose();
          o.geometry = new THREE.RingGeometry(
            newRadius - 0.15,
            newRadius,
            64
          );
        }
        // Rotate closure ring
        if (o.userData && o.userData.isClosure) {
          o.rotation.z += dt * 0.2;
        }
        // Rotate Compton ring
        if (o.userData && o.userData.isComptonRing) {
          o.rotation.x = Math.PI / 2 + Math.sin(time * 0.3) * 0.2;
        }
        // Animate phase dots
        if (o.userData && o.userData.isPhaseDot) {
          var pulse = 0.5 + 0.5 * Math.sin(time * 4 + o.userData.index * 0.5);
          o.material.opacity = 0.3 + pulse * 0.5;
          var angle = o.userData.angle + time * 0.1;
          o.position.x = 5 + Math.cos(angle) * 2.2;
          o.position.z = Math.sin(angle) * 2.2;
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
