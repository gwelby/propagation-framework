/**
 * GUT Scene — Grand Unification Force Field Visualization
 *
 * "At the GUT scale, the forces merge. Electromagnetic, weak, strong —
 *  they become a single unified field. X and Y bosons mediate everything."
 *
 * At the GUT scale (10⁻²⁵ m), the three fundamental forces of the Standard
 * Model (electromagnetic, weak, strong) are believed to unify into a single
 * grand unified force. This is the realm of X and Y bosons, proton decay,
 * and the ultimate symmetry of nature.
 *
 * Visual layers:
 *   1. Unified force field      — single field showing force unity
 *   2. X-Y boson vertices        — the unified force carriers
 *   3. Symmetry breaking shell   — where unity splits into multiplicity
 *   4. Force merger visualization — three streams becoming one
 *   5. Leptoquark field          — where quarks and leptons become one
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;

  // ── Coordinate ────────────────────────────────────────────────────────────
  function gutY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((-25 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Unified Force Field ─────────────────────────────────────────────────
  function buildUnifiedField() {
    var centerY = gutY();

    // Main wave field using shader if available
    if (window.PropagationShaders) {
      var fieldGeo = new THREE.PlaneGeometry(22, 16);
      var fieldMat = window.PropagationShaders.createWaveFieldMaterial({
        scale: 0.8,
        decay: 0.4,
        color1: 0x9b59b6,  // Violet
        color2: 0x7b2cbf,  // Purple
        bgColor: 0x020408
      });
      var field = new THREE.Mesh(fieldGeo, fieldMat);
      field.position.set(6, gutY(), -2);
      _objs.push(field);
      _shaders.push(fieldMat);
      scene.add(field);
    }

    // Unified field shell
    var shellGeo = new THREE.SphereGeometry(6, 48, 48);
    var shellMat = new THREE.MeshBasicMaterial({
      color: 0x9b59b6,
      transparent: true,
      opacity: 0.08,
      side: THREE.BackSide
    });
    var shell = new THREE.Mesh(shellGeo, shellMat);
    shell.position.set(5, gutY(), 0);
    _objs.push(shell);
    _mats.push(shellMat);
    scene.add(shell);
  }

  // ── X and Y Boson Vertices ───────────────────────────────────────────────
  function buildXYBosons() {
    var centerY = gutY();
    var centerPos = new THREE.Vector3(5, gutY(), 0);

    // X and Y bosons are the unified force carriers
    var bosonData = [
      { type: 'X', color: 0xff6b6b, pos: new THREE.Vector3(0, 2, 0) },
      { type: 'X', color: 0xff6b6b, pos: new THREE.Vector3(1.5, -1.5, 1.2) },
      { type: 'Y', color: 0x69ff94, pos: new THREE.Vector3(-1.5, -1.5, 1.2) },
      { type: 'Y', color: 0x69ff94, pos: new THREE.Vector3(0, 0.5, -2) }
    ];

    bosonData.forEach(function (data, i) {
      var bosonGeo = new THREE.SphereGeometry(0.6, 24, 24);
      var bosonMat = new THREE.MeshStandardMaterial({
        color: data.color,
        emissive: data.color,
        emissiveIntensity: 0.8,
        metalness: 0.4,
        roughness: 0.3
      });
      var boson = new THREE.Mesh(bosonGeo, bosonMat);
      boson.position.copy(centerPos).add(data.pos);
      boson.userData = {
        isBoson: true,
        type: data.type,
        phase: i * Math.PI / 2,
        basePos: data.pos.clone()
      };
      _objs.push(boson);
      _mats.push(bosonMat);
      scene.add(boson);

      // Boson glow
      var glowGeo = new THREE.SphereGeometry(1.2, 16, 16);
      var glowMat = new THREE.MeshBasicMaterial({
        color: data.color,
        transparent: true,
        opacity: 0.15,
        side: THREE.BackSide
      });
      var glow = new THREE.Mesh(glowGeo, glowMat);
      glow.position.copy(boson.position);
      _objs.push(glow);
      _mats.push(glowMat);
      scene.add(glow);
    });

    // Connect bosons with unified field lines
    for (var i = 0; i < bosonData.length; i++) {
      for (var j = i + 1; j < bosonData.length; j++) {
        var lineGeo = new THREE.CylinderGeometry(0.05, 0.05, 1, 8);
        var lineMat = new THREE.MeshBasicMaterial({
          color: 0x9b59b6,
          transparent: true,
          opacity: 0.3
        });
        var line = new THREE.Mesh(lineGeo, lineMat);
        var pos1 = bosonData[i].pos;
        var pos2 = bosonData[j].pos;
        var mid = new THREE.Vector3().addVectors(pos1, pos2).multiplyScalar(0.5);
        line.position.copy(centerPos).add(mid);
        line.lookAt(centerPos.clone().add(pos2));
        line.rotateX(Math.PI / 2);
        line.scale.y = pos1.distanceTo(pos2);
        _objs.push(line);
        _mats.push(lineMat);
        scene.add(line);
      }
    }
  }

  // ── Symmetry Breaking Visualization ─────────────────────────────────────
  function buildSymmetryBreaking() {
    var centerY = gutY();
    var centerPos = new THREE.Vector3(5, gutY(), 0);

    // The symmetry breaking shell — where unity diverges
    var breakGeo = new THREE.SphereGeometry(8, 48, 48);
    var breakMat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uColor1: { value: new THREE.Color(0x9b59b6) },
        uColor2: { value: new THREE.Color(0x7b2cbf) }
      },
      vertexShader: [
        'varying vec3 vNormal;',
        'varying vec3 vPosition;',
        'void main() {',
        '  vNormal = normalize(normalMatrix * normal);',
        '  vPosition = position;',
        '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform float uTime;',
        'uniform vec3 uColor1;',
        'uniform vec3 uColor2;',
        'varying vec3 vNormal;',
        'varying vec3 vPosition;',

        'float hash(vec3 p) {',
        '  return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453);',
        '}',

        'void main() {',
        // Fresnel for edge glow
        '  float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.5);',

        // Noise pattern representing field fluctuations
        '  vec3 p = vPosition * 0.5 + uTime * 0.1;',
        '  float n1 = hash(floor(p * 4.0));',
        '  float n2 = hash(floor(p * 8.0));',
        '  float noise = n1 * 0.6 + n2 * 0.4;',

        // Mix colors based on field intensity
        '  vec3 color = mix(uColor1, uColor2, fresnel * 0.7 + noise * 0.3);',
        '  float alpha = fresnel * 0.25 + noise * 0.1;',

        '  gl_FragColor = vec4(color, alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.BackSide,
      depthWrite: false
    });
    var breakShell = new THREE.Mesh(breakGeo, breakMat);
    breakShell.position.copy(centerPos);
    _objs.push(breakShell);
    _shaders.push(breakMat);
    scene.add(breakShell);
  }

  // ── Force Merger Streams ────────────────────────────────────────────────
  // Three streams (EM, weak, strong) merging into one
  function buildForceMerger() {
    var centerY = gutY();
    var centerPos = new THREE.Vector3(5, gutY(), 0);

    var forces = [
      { name: 'EM', color: 0xffff88, start: new THREE.Vector3(-6, 3, 0) },
      { name: 'Weak', color: 0xff88ff, start: new THREE.Vector3(-6, 0, 4) },
      { name: 'Strong', color: 0x88ffff, start: new THREE.Vector3(-6, -3, -2) }
    ];

    forces.forEach(function (force, i) {
      // Curved stream merging at center
      var curve = new THREE.CatmullRomCurve3([
        force.start,
        new THREE.Vector3(
          force.start.x * 0.5 + (Math.random() - 0.5),
          force.start.y * 0.5 + (Math.random() - 0.5),
          force.start.z * 0.5
        ),
        new THREE.Vector3(0, 0, 0)
      ]);

      var streamGeo = new THREE.TubeGeometry(curve, 32, 0.2, 12, false);
      var streamMat = new THREE.MeshStandardMaterial({
        color: force.color,
        emissive: force.color,
        emissiveIntensity: 0.4,
        transparent: true,
        opacity: 0.6
      });
      var stream = new THREE.Mesh(streamGeo, streamMat);
      stream.position.copy(centerPos);
      stream.userData = {
        isForceStream: true,
        force: force.name,
        phase: i * Math.PI * 2 / 3
      };
      _objs.push(stream);
      _mats.push(streamMat);
      scene.add(stream);

      // Flowing particles in stream
      for (var p = 0; p < 8; p++) {
        var particleGeo = new THREE.SphereGeometry(0.1, 8, 8);
        var particleMat = new THREE.MeshBasicMaterial({
          color: force.color,
          transparent: true,
          opacity: 0.8
        });
        var particle = new THREE.Mesh(particleGeo, particleMat);
        particle.position.copy(centerPos);
        particle.userData = {
          isFlowParticle: true,
          curve: curve,
          t: p / 8,
          speed: 0.2 + Math.random() * 0.1
        };
        _objs.push(particle);
        _mats.push(particleMat);
        scene.add(particle);
      }
    });
  }

  // ── Leptoquark Field ───────────────────────────────────────────────────────
  // The field where quarks and leptons become unified
  function buildLeptoquarkField() {
    var centerY = gutY();
    var centerPos = new THREE.Vector3(5, gutY(), 0);

    // Lattice of leptoquark vertices
    var latticeSize = 3;
    for (var x = -latticeSize; x <= latticeSize; x++) {
      for (var y = -latticeSize; y <= latticeSize; y++) {
        for (var z = -latticeSize; z <= latticeSize; z++) {
          if (Math.abs(x) + Math.abs(y) + Math.abs(z) > 4) continue;

          var vertexGeo = new THREE.SphereGeometry(0.12, 8, 8);
          var vertexMat = new THREE.MeshBasicMaterial({
            color: 0x9b59b6,
            transparent: true,
            opacity: 0.4
          });
          var vertex = new THREE.Mesh(vertexGeo, vertexMat);
          vertex.position.copy(centerPos).add(new THREE.Vector3(x * 1.2, y * 1.2, z * 1.2));
          vertex.userData = {
            isLeptoquark: true,
            gridPos: new THREE.Vector3(x, y, z),
            phase: Math.random() * Math.PI * 2
          };
          _objs.push(vertex);
          _mats.push(vertexMat);
          scene.add(vertex);
        }
      }
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
    ctx.fillStyle = '#9b59b6';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('GUT Scale — 10⁻²⁵ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, gutY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.GUTScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();

      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.025 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.025);
      }

      buildUnifiedField();
      buildXYBosons();
      buildSymmetryBreaking();
      buildForceMerger();
      buildLeptoquarkField();
      buildLabel();

      camera.position.set(5, gutY(), 25);
      camera.lookAt(5, gutY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, gutY(), 25),
        target: new THREE.Vector3(5, gutY(), 0),
        fov: 55
      };
    },

    getSharedElements: function () {
      // Return bosons and force field elements for wave morphing
      return _objs.filter(function (o) {
        return o.userData && (
          o.userData.isBoson ||
          o.userData.isLeptoquark
        );
      }).slice(0, 6);
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // GUT scene uses medium LOD
      return 1;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[GUTScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      _objs.forEach(function (o) {
        // Animate bosons
        if (o.userData && o.userData.isBoson) {
          var pulse = 0.7 + 0.3 * Math.sin(time * 3 + o.userData.phase);
          o.material.emissiveIntensity = pulse;
          // Orbit slightly
          var angle = time * 0.2 + o.userData.phase;
          o.position.x = 5 + Math.cos(angle) * 0.3 + o.userData.basePos.x;
          o.position.z = Math.sin(angle) * 0.3 + o.userData.basePos.z;
        }
        // Animate force stream particles
        if (o.userData && o.userData.isFlowParticle) {
          o.userData.t += dt * o.userData.speed;
          if (o.userData.t > 1) o.userData.t = 0;
          var point = o.userData.curve.getPoint(o.userData.t);
          o.position.set(5 + point.x, gutY() + point.y, point.z);
          o.material.opacity = 0.3 + 0.5 * Math.sin(o.userData.t * Math.PI);
        }
        // Animate leptoquark lattice
        if (o.userData && o.userData.isLeptoquark) {
          var intensity = 0.3 + 0.3 * Math.sin(time * 2 + o.userData.phase);
          o.material.opacity = intensity;
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
