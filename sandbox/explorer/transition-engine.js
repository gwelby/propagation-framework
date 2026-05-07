/**
 * TransitionEngine — Seamless Scale Transitions for the Propagation Framework
 *
 * "Nothing is solid. Everything is waves."
 *
 * This engine provides smooth, continuous camera flights and shared element
 * morphing between any two scales in the 16-scale logarithmic ladder.
 *
 * Core features:
 *   1. Camera flight paths — 5 motion types for different scale relationships
 *   2. Shared element morphing — The Propagation Wave appears in every scale
 *   3. Crossfade system — 30% overlap between scenes
 *   4. Motion blur — velocity-based blur during fast transitions
 *   5. Easing functions — smooth acceleration/deceleration
 *
 * Usage:
 *   TransitionEngine.init(ScaleEngine);
 *   TransitionEngine.transition('human', 'cellular', { duration: 1500 });
 */
(function () {
  'use strict';

  // ── Dependencies ──────────────────────────────────────────────────────────
  var _scaleEngine = null;
  var _scene = null;
  var _camera = null;
  var _renderer = null;
  var _composer = null;

  // ── Transition State ───────────────────────────────────────────────────────
  var _isTransitioning = false;
  var _transitionStartTime = 0;
  var _transitionDuration = 0;
  var _currentTransition = null;
  var _sceneA = null; // outgoing scene
  var _sceneB = null; // incoming scene
  var _sharedElements = []; // morphing elements
  var _motionBlurPass = null;

  // ── Scale Coordinates (must match scale-engine.js) ─────────────────────────
  var LOG_MIN = -40;
  var LOG_MAX = 26;
  var LOG_RANGE = LOG_MAX - LOG_MIN;
  var BEAM_LENGTH = 100;

  var SCALE_COORDS = {
    'axiomatic-root': { log: -40, y: 0, label: 'Axiomatic Root', color: 0xff0055 },
    'planck': { log: -35, y: metersToY(1.616e-35), label: 'Planck', color: 0xffd700 },
    'quantum-foam': { log: -33, y: metersToY(1e-33), label: 'Quantum Foam', color: 0xd4a017 },
    'gut': { log: -25, y: metersToY(1e-25), label: 'GUT', color: 0x9b59b6 },
    'matter': { log: -18, y: metersToY(1.145e-18), label: 'Matter', color: 0x00e5ff },
    'proton': { log: -15, y: metersToY(1e-15), label: 'Proton', color: 0x00b4d8 },
    'nuclear': { log: -15.05, y: metersToY(9e-16), label: 'Nuclear', color: 0x0096c7 },
    'atomic': { log: -10, y: metersToY(1e-10), label: 'Atomic', color: 0x0077b6 },
    'molecular': { log: -9, y: metersToY(1e-9), label: 'Molecular', color: 0x48cae4 },
    'virus': { log: -7, y: metersToY(1e-7), label: 'Virus', color: 0x69ff94 },
    'cellular': { log: -5, y: metersToY(1e-5), label: 'Cellular', color: 0x80ed99 },
    'neural': { log: -2, y: metersToY(1e-2), label: 'Neural', color: 0xffdd55 },
    'human': { log: 0, y: metersToY(1), label: 'Human', color: 0xffb347 },
    'planetary': { log: 7, y: metersToY(1e7), label: 'Planetary', color: 0xff9f43 },
    'stellar': { log: 9, y: metersToY(1e9), label: 'Stellar', color: 0xff6b6b },
    'galactic': { log: 21, y: metersToY(1e21), label: 'Galactic', color: 0x7c5cbf },
    'cosmic': { log: 26, y: metersToY(1e26), label: 'Cosmic', color: 0xd63031 }
  };

  function metersToY(meters) {
    var logM = Math.log10(meters);
    return ((logM - LOG_MIN) / LOG_RANGE) * BEAM_LENGTH;
  }

  // ── Easing Functions ───────────────────────────────────────────────────────
  var Easing = {
    linear: function (t) { return t; },
    easeInQuad: function (t) { return t * t; },
    easeOutQuad: function (t) { return 1 - (1 - t) * (1 - t); },
    easeInOutQuad: function (t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; },
    easeInCubic: function (t) { return t * t * t; },
    easeOutCubic: function (t) { return 1 - Math.pow(1 - t, 3); },
    easeInOutCubic: function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; },
    easeInOutQuart: function (t) { return t < 0.5 ? 8 * t * t * t * t : 1 - Math.pow(-2 * t + 2, 4) / 2; },
    // Elastic overshoot for "penetrate" transitions
    easeOutElastic: function (t) {
      var c4 = (2 * Math.PI) / 3;
      return t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
    },
    // Exponential for "warp" transitions
    easeInOutExpo: function (t) {
      return t === 0 ? 0 : t === 1 ? 1 : t < 0.5 ? Math.pow(2, 20 * t - 10) / 2 : (2 - Math.pow(2, -20 * t + 10)) / 2;
    }
  };

  // ── Flight Path Definitions ──────────────────────────────────────────────
  // Map of transition keys to flight path configurations
  var FLIGHT_PATHS = {
    // ── Zoom In (microscopic direction) ────────────────────────────────────
    'human→cellular': {
      type: 'zoomIn', duration: 1500, easing: 'easeInOutCubic',
      cameraMove: { fromOffset: [0, 0, 15], toOffset: [0, 0, 3], fovChange: [48, 60] }
    },
    'cellular→molecular': {
      type: 'penetrate', duration: 1800, easing: 'easeOutElastic',
      cameraMove: { fromOffset: [0, 0, 3], toOffset: [0, 0, 8], penetrateDepth: 2 }
    },
    'molecular→atomic': {
      type: 'zoomIn', duration: 1200, easing: 'easeInOutQuad',
      cameraMove: { fromOffset: [0, 0, 18], toOffset: [0, 0, 8], fovChange: [48, 55] }
    },
    'atomic→nuclear': {
      type: 'penetrate', duration: 1400, easing: 'easeOutCubic',
      cameraMove: { fromOffset: [0, 0, 20], toOffset: [0, 0, 6], penetrateDepth: 1.5 }
    },
    'nuclear→matter': {
      type: 'zoomIn', duration: 1300, easing: 'easeInOutCubic',
      cameraMove: { fromOffset: [0, 0, 15], toOffset: [0, 0, 8], fovChange: [50, 65] }
    },
    'matter→proton': {
      type: 'zoomIn', duration: 1100, easing: 'easeInOutQuad',
      cameraMove: { fromOffset: [0, 0, 12], toOffset: [0, 0, 5] }
    },
    'proton→gut': {
      type: 'warp', duration: 900, easing: 'easeInOutExpo',
      cameraMove: { fromOffset: [0, 0, 10], toOffset: [0, 0, 8], motionBlur: 0.8 }
    },
    'gut→quantum-foam': {
      type: 'penetrate', duration: 1000, easing: 'easeOutCubic',
      cameraMove: { fromOffset: [0, 0, 8], toOffset: [0, 0, 6] }
    },
    'quantum-foam→planck': {
      type: 'zoomIn', duration: 1200, easing: 'easeInOutCubic',
      cameraMove: { fromOffset: [0, 0, 10], toOffset: [0, 0, 8], fovChange: [55, 70] }
    },

    // ── Zoom Out (macroscopic direction) ───────────────────────────────────
    'planck→quantum-foam': {
      type: 'zoomOut', duration: 1200, easing: 'easeInOutCubic',
      cameraMove: { fromOffset: [0, 0, 8], toOffset: [0, 0, 10] }
    },
    'cellular→human': {
      type: 'zoomOut', duration: 1400, easing: 'easeInOutQuad',
      cameraMove: { fromOffset: [0, 0, 3], toOffset: [0, 0, 15], fovChange: [60, 48] }
    },
    'molecular→cellular': {
      type: 'zoomOut', duration: 1500, easing: 'easeOutQuad',
      cameraMove: { fromOffset: [0, 0, 8], toOffset: [0, 0, 3] }
    },
    'human→planetary': {
      type: 'orbit', duration: 2000, easing: 'easeInOutCubic',
      cameraMove: { orbitAngle: Math.PI / 2, fromOffset: [0, 0, 15], toOffset: [15, 10, 25] }
    },
    'planetary→stellar': {
      type: 'zoomOut', duration: 1600, easing: 'easeInOutQuad',
      cameraMove: { fromOffset: [0, 0, 40], toOffset: [0, 0, 30] }
    },
    'stellar→galactic': {
      type: 'orbit', duration: 2200, easing: 'easeInOutCubic',
      cameraMove: { orbitAngle: Math.PI, fromOffset: [0, 0, 30], toOffset: [20, 5, 35] }
    },
    'galactic→cosmic': {
      type: 'zoomOut', duration: 1800, easing: 'easeOutQuad',
      cameraMove: { fromOffset: [0, 0, 35], toOffset: [0, 0, 28] }
    },

    // ── Extreme Scale Jumps ────────────────────────────────────────────────
    'planck→axiomatic-root': {
      type: 'warp', duration: 800, easing: 'easeInOutExpo',
      cameraMove: { fromOffset: [0, 0, 8], toOffset: [0, 0, 5], motionBlur: 1.0 }
    },
    'cosmic→axiomatic-root': {
      type: 'warp', duration: 2500, easing: 'easeInOutExpo',
      cameraMove: { fromOffset: [0, 0, 28], toOffset: [0, 0, 5], motionBlur: 0.9 }
    }
  };

  // Generate symmetric reverse transitions
  function generateReversePaths() {
    var paths = Object.keys(FLIGHT_PATHS);
    paths.forEach(function (key) {
      var parts = key.split('→');
      if (parts.length === 2) {
        var reverseKey = parts[1] + '→' + parts[0];
        if (!FLIGHT_PATHS[reverseKey]) {
          var original = FLIGHT_PATHS[key];
          var reverseType = original.type === 'zoomIn' ? 'zoomOut' :
                           original.type === 'zoomOut' ? 'zoomIn' : original.type;
          FLIGHT_PATHS[reverseKey] = {
            type: reverseType,
            duration: original.duration,
            easing: original.easing,
            cameraMove: {
              fromOffset: original.cameraMove.toOffset || original.cameraMove.fromOffset,
              toOffset: original.cameraMove.fromOffset,
              fovChange: original.cameraMove.fovChange ? [original.cameraMove.fovChange[1], original.cameraMove.fovChange[0]] : undefined,
              motionBlur: original.cameraMove.motionBlur
            }
          };
        }
      }
    });
  }
  generateReversePaths();

  // ── Shared Element Definitions ─────────────────────────────────────────────
  // The Propagation Wave — a visual motif that morphs across all scales
  var PROPAGATION_WAVE_DEFS = {
    human: {
      geometry: 'chair_outline', scale: 1.0, color: 0xffb347,
      pulseFreq: 0.5, pulseAmp: 0.1,
      description: 'Chair edge glow — subtle macro coherence'
    },
    cellular: {
      geometry: 'cell_membrane', scale: 0.001, color: 0x80ed99,
      pulseFreq: 2.0, pulseAmp: 0.3,
      description: 'Cell membrane vibration pattern'
    },
    molecular: {
      geometry: 'bond_vibration', scale: 0.0001, color: 0x48cae4,
      pulseFreq: 8.0, pulseAmp: 0.2,
      description: 'Molecular bond vibration'
    },
    atomic: {
      geometry: 'orbital_ring', scale: 0.00001, color: 0x0077b6,
      pulseFreq: 12.0, pulseAmp: 0.15,
      description: 'Electron orbital standing wave'
    },
    nuclear: {
      geometry: 'gluon_field', scale: 0.000001, color: 0x0096c7,
      pulseFreq: 20.0, pulseAmp: 0.25,
      description: 'Gluon field coherence'
    },
    matter: {
      geometry: 'standing_wave', scale: 0.0000001, color: 0x00e5ff,
      pulseFreq: 30.0, pulseAmp: 0.4,
      description: 'Compton wavelength standing pattern'
    },
    proton: {
      geometry: 'quark_confinement', scale: 0.00000001, color: 0x00b4d8,
      pulseFreq: 25.0, pulseAmp: 0.3,
      description: 'Quark confinement wave'
    },
    planck: {
      geometry: 'quantum_foam', scale: 0.00000000001, color: 0xffd700,
      pulseFreq: 50.0, pulseAmp: 0.5,
      description: 'Quantum foam vibration'
    },
    planetary: {
      geometry: 'light_curvature', scale: 10000000, color: 0xff9f43,
      pulseFreq: 0.2, pulseAmp: 0.15,
      description: 'Light path curvature in gravity'
    },
    stellar: {
      geometry: 'stellar_pulse', scale: 1000000000, color: 0xff6b6b,
      pulseFreq: 0.1, pulseAmp: 0.3,
      description: 'Stellar oscillation modes'
    },
    galactic: {
      geometry: 'density_wave', scale: 1000000000000000000000, color: 0x7c5cbf,
      pulseFreq: 0.05, pulseAmp: 0.2,
      description: 'Spiral density wave'
    },
    cosmic: {
      geometry: 'filament_glow', scale: 10000000000000000000000000, color: 0xd63031,
      pulseFreq: 0.02, pulseAmp: 0.25,
      description: 'Cosmic web filament glow'
    }
  };

  // Coherence Field — persistent glow across all scales
  var COHERENCE_FIELD_DEFS = {
    human: { color: 0xffb347, intensity: 0.1, radius: 2.0 },
    cellular: { color: 0x80ed99, intensity: 0.25, radius: 4.5 },
    molecular: { color: 0x48cae4, intensity: 0.3, radius: 2.2 },
    atomic: { color: 0x0077b6, intensity: 0.35, radius: 2.8 },
    nuclear: { color: 0x0096c7, intensity: 0.4, radius: 1.2 },
    matter: { color: 0x00e5ff, intensity: 0.45, radius: 5.0 },
    proton: { color: 0x00b4d8, intensity: 0.5, radius: 0.8 },
    planck: { color: 0xffd700, intensity: 0.6, radius: 2.5 },
    planetary: { color: 0xff9f43, intensity: 0.15, radius: 30.0 },
    stellar: { color: 0xff6b6b, intensity: 0.2, radius: 3.0 },
    galactic: { color: 0x7c5cbf, intensity: 0.25, radius: 16.0 },
    cosmic: { color: 0xd63031, intensity: 0.3, radius: 14.0 }
  };

  // ── Shared Element Class ───────────────────────────────────────────────────
  function SharedPropagationWave(scaleA, scaleB) {
    this.scaleA = scaleA;
    this.scaleB = scaleB;
    this.mesh = null;
    this.transitionProgress = 0;
    this.phase = 0;
  }

  SharedPropagationWave.prototype.create = function (scene, centerY) {
    var defA = PROPAGATION_WAVE_DEFS[this.scaleA] || PROPAGATION_WAVE_DEFS.human;
    var defB = PROPAGATION_WAVE_DEFS[this.scaleB] || PROPAGATION_WAVE_DEFS.human;

    // Create morphing ring geometry
    var geometry = new THREE.RingGeometry(0.5, 0.6, 64);
    var material = new THREE.MeshBasicMaterial({
      color: defA.color,
      transparent: true,
      opacity: 0.4,
      side: THREE.DoubleSide
    });

    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.set(5, centerY, 0);
    this.mesh.userData = {
      isSharedElement: true,
      type: 'propagationWave',
      defA: defA,
      defB: defB
    };

    scene.add(this.mesh);
    return this.mesh;
  };

  SharedPropagationWave.prototype.update = function (dt, time, progress) {
    if (!this.mesh) return;
    this.transitionProgress = progress;
    this.phase += dt;

    var defA = this.mesh.userData.defA;
    var defB = this.mesh.userData.defB;

    // Interpolate properties
    var pulseFreq = defA.pulseFreq + (defB.pulseFreq - defA.pulseFreq) * progress;
    var pulseAmp = defA.pulseAmp + (defB.pulseAmp - defA.pulseAmp) * progress;
    var color = new THREE.Color(defA.color).lerp(new THREE.Color(defB.color), progress);

    // Apply pulsing scale
    var scale = 1 + Math.sin(this.phase * pulseFreq) * pulseAmp * (0.5 + progress * 0.5);
    this.mesh.scale.setScalar(scale);

    // Update color
    this.mesh.material.color.copy(color);

    // Rotate
    this.mesh.rotation.z += dt * 0.5;
  };

  SharedPropagationWave.prototype.dispose = function (scene) {
    if (this.mesh) {
      if (this.mesh.geometry) this.mesh.geometry.dispose();
      if (this.mesh.material) this.mesh.material.dispose();
      if (scene) scene.remove(this.mesh);
      this.mesh = null;
    }
  };

  // ── Coherence Field Class ─────────────────────────────────────────────────
  function SharedCoherenceField(scaleA, scaleB) {
    this.scaleA = scaleA;
    this.scaleB = scaleB;
    this.mesh = null;
    this.transitionProgress = 0;
  }

  SharedCoherenceField.prototype.create = function (scene, centerY) {
    var defA = COHERENCE_FIELD_DEFS[this.scaleA] || COHERENCE_FIELD_DEFS.human;
    var defB = COHERENCE_FIELD_DEFS[this.scaleB] || COHERENCE_FIELD_DEFS.human;

    var geometry = new THREE.SphereGeometry(defA.radius, 32, 32);
    var material = new THREE.MeshBasicMaterial({
      color: defA.color,
      transparent: true,
      opacity: defA.intensity * 0.3,
      side: THREE.BackSide
    });

    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.set(5, centerY, 0);
    this.mesh.userData = {
      isSharedElement: true,
      type: 'coherenceField',
      defA: defA,
      defB: defB
    };

    scene.add(this.mesh);
    return this.mesh;
  };

  SharedCoherenceField.prototype.update = function (dt, time, progress) {
    if (!this.mesh) return;
    this.transitionProgress = progress;

    var defA = this.mesh.userData.defA;
    var defB = this.mesh.userData.defB;

    // Interpolate
    var radius = defA.radius + (defB.radius - defA.radius) * progress;
    var intensity = defA.intensity + (defB.intensity - defA.intensity) * progress;
    var color = new THREE.Color(defA.color).lerp(new THREE.Color(defB.color), progress);

    // Update geometry if radius changed significantly
    if (Math.abs(this.mesh.geometry.parameters.radius - radius) > 0.1) {
      this.mesh.geometry.dispose();
      this.mesh.geometry = new THREE.SphereGeometry(radius, 32, 32);
    }

    this.mesh.material.color.copy(color);
    this.mesh.material.opacity = intensity * 0.3;

    // Slow rotation
    this.mesh.rotation.y += dt * 0.1;
  };

  SharedCoherenceField.prototype.dispose = function (scene) {
    if (this.mesh) {
      if (this.mesh.geometry) this.mesh.geometry.dispose();
      if (this.mesh.material) this.mesh.material.dispose();
      if (scene) scene.remove(this.mesh);
      this.mesh = null;
    }
  };

  // ── Motion Blur Pass ──────────────────────────────────────────────────────
  function createMotionBlurPass(width, height) {
    // Simple motion blur using shader
    var shader = {
      uniforms: {
        tDiffuse: { value: null },
        uVelocity: { value: 0.0 },
        uTime: { value: 0.0 }
      },
      vertexShader: [
        'varying vec2 vUv;',
        'void main() {',
        '  vUv = uv;',
        '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform sampler2D tDiffuse;',
        'uniform float uVelocity;',
        'uniform float uTime;',
        'varying vec2 vUv;',
        '',
        'void main() {',
        '  vec4 color = vec4(0.0);',
        '  float samples = 8.0;',
        '  vec2 direction = vec2(uVelocity * 0.02, 0.0);',
        '  ',
        '  for (float i = 0.0; i < samples; i++) {',
        '    float t = i / (samples - 1.0) - 0.5;',
        '    vec2 offset = direction * t;',
        '    color += texture2D(tDiffuse, vUv + offset);',
        '  }',
        '  ',
        '  gl_FragColor = color / samples;',
        '}'
      ].join('\n')
    };

    var ShaderPassCtor = window.THREE.ShaderPass || window.ShaderPass;
    if (!ShaderPassCtor) return null;

    var pass = new ShaderPassCtor(shader);
    pass.uniforms = shader.uniforms;
    return pass;
  }

  // ── Camera Path Calculation ────────────────────────────────────────────────
  function calculateCameraPath(fromScale, toScale, pathType, progress) {
    var fromY = SCALE_COORDS[fromScale] ? SCALE_COORDS[fromScale].y : 50;
    var toY = SCALE_COORDS[toScale] ? SCALE_COORDS[toScale].y : 50;

    var pathConfig = FLIGHT_PATHS[fromScale + '→' + toScale] || {
      cameraMove: { fromOffset: [0, 0, 15], toOffset: [0, 0, 15] }
    };

    var move = pathConfig.cameraMove;
    var fromOffset = new THREE.Vector3(move.fromOffset[0], move.fromOffset[1], move.fromOffset[2]);
    var toOffset = new THREE.Vector3(move.toOffset[0], move.toOffset[1], move.toOffset[2]);

    var position = new THREE.Vector3();
    var target = new THREE.Vector3(5, 0, 0);

    switch (pathType) {
      case 'zoomIn':
        // Linear Y interpolation, Z moves closer
        position.y = fromY + (toY - fromY) * progress;
        position.x = 5;
        position.z = fromOffset.z + (toOffset.z - fromOffset.z) * progress;
        target.y = position.y;
        break;

      case 'zoomOut':
        // Pull back as we move
        position.y = fromY + (toY - fromY) * progress;
        position.x = 5;
        position.z = fromOffset.z + (toOffset.z - fromOffset.z) * progress;
        target.y = position.y;
        break;

      case 'penetrate':
        // Move through a surface (overshoot then settle)
        var penetratePhase = Math.sin(progress * Math.PI);
        position.y = fromY + (toY - fromY) * progress;
        position.x = 5;
        position.z = fromOffset.z + (toOffset.z - fromOffset.z) * progress;
        position.z -= penetratePhase * (move.penetrateDepth || 1);
        target.y = position.y;
        break;

      case 'orbit':
        // Swing around to new angle
        var orbitProgress = progress * (move.orbitAngle || Math.PI / 2);
        position.y = fromY + (toY - fromY) * progress;
        position.x = 5 + Math.sin(orbitProgress) * 15;
        position.z = fromOffset.z + (toOffset.z - fromOffset.z) * progress + Math.cos(orbitProgress) * 10;
        target.y = position.y;
        target.x = 5;
        break;

      case 'warp':
        // Fast jump with stretch
        var warpStretch = Math.sin(progress * Math.PI) * 0.3;
        position.y = fromY + (toY - fromY) * progress;
        position.x = 5;
        position.z = fromOffset.z + (toOffset.z - fromOffset.z) * progress;
        // Add wobble during warp
        position.x += Math.sin(progress * Math.PI * 4) * warpStretch;
        target.y = position.y;
        break;

      default:
        position.y = fromY + (toY - fromY) * progress;
        position.x = 5;
        position.z = fromOffset.z;
        target.y = position.y;
    }

    return { position: position, target: target };
  }

  // ── Crossfade Management ───────────────────────────────────────────────────
  function startCrossfade(fromScale, toScale) {
    // Deactivate old scene immediately for now, can be enhanced to overlap
    if (_sceneA && _sceneA.deactivate) {
      _sceneA.deactivate();
    }

    // Activate new scene
    if (_sceneB && _sceneB.activate && _scene && _camera) {
      _sceneB.activate(_scene, _camera);
    }
  }

  function updateCrossfade(progress) {
    // Fade opacity of shared elements or entire scenes if using composer
    // Currently simple: scenes swap at 0.3 (30% overlap point)
    if (progress > 0.3 && progress < 0.7) {
      // Both scenes visible during middle 40%
    }
  }

  // ── Main Transition Function ────────────────────────────────────────────────
  function transition(fromScaleId, toScaleId, options) {
    options = options || {};

    if (_isTransitioning) {
      // Queue or force new transition
      if (!options.force) return false;
    }

    var transitionKey = fromScaleId + '→' + toScaleId;
    var pathConfig = FLIGHT_PATHS[transitionKey];

    if (!pathConfig) {
      // Fallback to default zoom
      pathConfig = {
        type: 'zoomIn',
        duration: options.duration || 1500,
        easing: 'easeInOutCubic',
        cameraMove: { fromOffset: [0, 0, 15], toOffset: [0, 0, 15] }
      };
    }

    _isTransitioning = true;
    _transitionStartTime = performance.now();
    _transitionDuration = options.duration || pathConfig.duration;
    _currentTransition = {
      fromScale: fromScaleId,
      toScale: toScaleId,
      config: pathConfig
    };

    // Get scene objects from ScaleEngine registry
    if (_scaleEngine) {
      var registry = _scaleEngine.getSceneRegistry ? _scaleEngine.getSceneRegistry() : {};
      _sceneA = registry[fromScaleId];
      _sceneB = registry[toScaleId];
    }

    // Create shared elements
    _sharedElements = [];
    if (_scene) {
      var centerY = (SCALE_COORDS[fromScaleId].y + SCALE_COORDS[toScaleId].y) / 2;

      var wave = new SharedPropagationWave(fromScaleId, toScaleId);
      wave.create(_scene, centerY);
      _sharedElements.push(wave);

      var field = new SharedCoherenceField(fromScaleId, toScaleId);
      field.create(_scene, centerY);
      _sharedElements.push(field);
    }

    // Setup motion blur if enabled
    if (pathConfig.cameraMove.motionBlur && _composer) {
      if (!_motionBlurPass) {
        var size = _renderer ? _renderer.getSize(new THREE.Vector2()) : { width: 1280, height: 720 };
        _motionBlurPass = createMotionBlurPass(size.width, size.height);
      }
      if (_motionBlurPass) {
        // Insert before final pass
        var passes = _composer.passes;
        passes.splice(passes.length - 1, 0, _motionBlurPass);
      }
    }

    return true;
  }

  // ── Animation Loop Update ──────────────────────────────────────────────────
  function update(dt, time) {
    if (!_isTransitioning) return;

    var elapsed = performance.now() - _transitionStartTime;
    var rawProgress = Math.min(elapsed / _transitionDuration, 1);

    // Apply easing
    var config = _currentTransition.config;
    var easingFn = Easing[config.easing] || Easing.easeInOutCubic;
    var progress = easingFn(rawProgress);

    // Calculate camera path
    var cameraState = calculateCameraPath(
      _currentTransition.fromScale,
      _currentTransition.toScale,
      config.type,
      progress
    );

    // Update camera
    if (_camera) {
      _camera.position.copy(cameraState.position);
      if (_camera.lookAt) {
        _camera.lookAt(cameraState.target);
      }
    }

    // Update shared elements
    _sharedElements.forEach(function (element) {
      element.update(dt, time, progress);
    });

    // Update motion blur
    if (_motionBlurPass && _motionBlurPass.uniforms) {
      var velocity = Math.sin(rawProgress * Math.PI) * (config.cameraMove.motionBlur || 0.5);
      _motionBlurPass.uniforms.uVelocity.value = velocity;
      _motionBlurPass.uniforms.uTime.value = time;
    }

    // Handle crossfade timing (30% overlap)
    if (rawProgress >= 0.3 && rawProgress < 0.31 && _sceneA && _sceneB) {
      startCrossfade(_currentTransition.fromScale, _currentTransition.toScale);
    }
    updateCrossfade(rawProgress);

    // Complete transition
    if (rawProgress >= 1) {
      completeTransition();
    }
  }

  function completeTransition() {
    _isTransitioning = false;

    // Clean up shared elements
    _sharedElements.forEach(function (element) {
      element.dispose(_scene);
    });
    _sharedElements = [];

    // Remove motion blur pass
    if (_motionBlurPass && _composer) {
      var index = _composer.passes.indexOf(_motionBlurPass);
      if (index >= 0) {
        _composer.passes.splice(index, 1);
      }
    }

    // Finalize scene activation
    if (_scaleEngine && _scaleEngine.navigateToScale) {
      _scaleEngine.navigateToScale(_currentTransition.toScale, { duration: 0 });
    }

    _currentTransition = null;
    _sceneA = null;
    _sceneB = null;
  }

  // ── Public API ────────────────────────────────────────────────────────────
  window.TransitionEngine = {
    /**
     * Initialize the transition engine with references to Three.js objects
     */
    init: function (scaleEngine, scene, camera, renderer, composer) {
      _scaleEngine = scaleEngine;
      _scene = scene;
      _camera = camera;
      _renderer = renderer;
      _composer = composer;
      console.log('[TransitionEngine] Initialized');
      return this;
    },

    /**
     * Prepare a scene for activation - sets up LOD and shared elements
     * Called by ScaleEngine before activating a scene
     */
    prepareScene: function (scaleId, lodSettings) {
      // Store LOD settings for this scale
      if (lodSettings) {
        _sceneA = _sceneRegistry && _sceneRegistry[scaleId] || null;
        if (_sceneA && _sceneA.lodSettings !== undefined) {
          _sceneA.lodSettings = lodSettings;
        }
      }
      
      // Notify scene to prepare if method exists
      var api = _scaleEngine && _scaleEngine.getSceneRegistry ? 
                _scaleEngine.getSceneRegistry()[scaleId] : null;
      if (api && api.prepare && typeof api.prepare === 'function') {
        api.prepare(lodSettings);
      }
      
      return true;
    },

    /**
     * Start a transition between two scales
     * @param {string} fromScaleId - Starting scale ID
     * @param {string} toScaleId - Target scale ID
     * @param {object} options - Optional { duration, easing, force }
     * @returns {boolean} Whether transition started successfully
     */
    transition: transition,

    /**
     * Update the transition animation (call in render loop)
     * @param {number} dt - Delta time in seconds
     * @param {number} time - Elapsed time in seconds
     */
    update: update,

    /**
     * Check if a transition is currently in progress
     */
    isTransitioning: function () {
      return _isTransitioning;
    },

    /**
     * Get current transition progress (0-1)
     */
    getProgress: function () {
      if (!_isTransitioning) return 0;
      return Math.min((performance.now() - _transitionStartTime) / _transitionDuration, 1);
    },

    /**
     * Cancel current transition immediately
     */
    cancel: function () {
      if (_isTransitioning) {
        completeTransition();
      }
    },

    /**
     * Get flight path configuration for a transition
     */
    getFlightPath: function (fromScaleId, toScaleId) {
      return FLIGHT_PATHS[fromScaleId + '→' + toScaleId] || null;
    },

    /**
     * Get all available flight paths
     */
    getAllFlightPaths: function () {
      return Object.keys(FLIGHT_PATHS).map(function (key) {
        var parts = key.split('→');
        return {
          from: parts[0],
          to: parts[1],
          config: FLIGHT_PATHS[key]
        };
      });
    },

    /**
     * Get propagation wave definition for a scale
     */
    getPropagationWaveDef: function (scaleId) {
      return PROPAGATION_WAVE_DEFS[scaleId] || null;
    },

    /**
     * Get coherence field definition for a scale
     */
    getCoherenceFieldDef: function (scaleId) {
      return COHERENCE_FIELD_DEFS[scaleId] || null;
    },

    /**
     * Set custom easing function
     */
    setEasing: function (name, fn) {
      Easing[name] = fn;
    },

    /**
     * Preview a transition without executing (returns camera positions)
     */
    previewTransition: function (fromScaleId, toScaleId, samples) {
      samples = samples || 10;
      var path = FLIGHT_PATHS[fromScaleId + '→' + toScaleId];
      if (!path) return null;

      var positions = [];
      for (var i = 0; i <= samples; i++) {
        var progress = i / samples;
        var state = calculateCameraPath(fromScaleId, toScaleId, path.type, progress);
        positions.push({
          progress: progress,
          position: state.position.clone(),
          target: state.target.clone()
        });
      }
      return positions;
    },

    // Expose internal classes for extension
    SharedPropagationWave: SharedPropagationWave,
    SharedCoherenceField: SharedCoherenceField,
    Easing: Easing
  };

}());
