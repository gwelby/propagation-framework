/**
 * ScaleEngine — Propagation Framework Scale Ladder Core
 * 
 * Manages the 16-scale logarithmic navigation system.
 * Log₁₀ range: Planck (-35) → Cosmic (+26) = 61 orders of magnitude.
 * 
 * API:
 *   window.ScaleEngine.init(containerEl)         — boot engine, return scene/camera
 *   window.ScaleEngine.navigateToScale(id)      — animated fly-to scale
 *   window.ScaleEngine.getScaleAtCursor(x, y)  — raycasting, returns scale or null
 *   window.ScaleEngine.registerScene(id, api)   — register per-scale Three.js scene
 *   window.ScaleEngine.getLogPosition(scaleId)  — get log₁₀(meters) for a scale
 *   window.ScaleEngine.getScaleNodes()          — access scale node meshes
 *   window.ScaleEngine.getCamera()              — access camera for external use
 *   window.ScaleEngine.onScaleChange(cb)        — subscribe to scale change events
 */
(function () {
  'use strict';

  const LOG_MIN = Math.log10(1.616e-35);
  const LOG_MAX = 26;
  const LOG_RANGE = LOG_MAX - LOG_MIN;
  const BEAM_LENGTH = 100;

  function getThreeAddon(name) {
    return THREE[name] || window[name];
  }

  const SCALE_DEFAULTS = [
    { id: 'planck',      label: 'Planck',      meters: 1.616e-35, color: 0xffd700, hex: '#ffd700' },
    { id: 'quantum-foam',label: 'Quantum Foam', meters: 1e-33,      color: 0xd4a017, hex: '#d4a017' },
    { id: 'gut',         label: 'GUT',          meters: 1e-25,      color: 0x9b59b6, hex: '#9b59b6' },
    { id: 'matter',      label: 'Matter',       meters: 1.145e-18,  color: 0x00e5ff, hex: '#00e5ff' },
    { id: 'proton',      label: 'Proton',        meters: 1e-15,      color: 0x00b4d8, hex: '#00b4d8' },
    { id: 'nuclear',     label: 'Nuclear',       meters: 9e-16,      color: 0x0096c7, hex: '#0096c7' },
    { id: 'atomic',      label: 'Atomic',        meters: 1e-10,      color: 0x0077b6, hex: '#0077b6' },
    { id: 'molecular',   label: 'Molecular',     meters: 1e-9,       color: 0x48cae4, hex: '#48cae4' },
    { id: 'virus',       label: 'Virus',         meters: 1e-7,       color: 0x69ff94, hex: '#69ff94' },
    { id: 'cellular',    label: 'Cellular',      meters: 1e-5,       color: 0x80ed99, hex: '#80ed99' },
    { id: 'neural',      label: 'Neural',        meters: 1e-2,       color: 0xffdd55, hex: '#ffdd55' },
    { id: 'human',       label: 'Human',          meters: 1,          color: 0xffb347, hex: '#ffb347' },
    { id: 'planetary',   label: 'Planetary',     meters: 1e7,        color: 0xff9f43, hex: '#ff9f43' },
    { id: 'stellar',     label: 'Stellar',       meters: 1e9,        color: 0xff6b6b, hex: '#ff6b6b' },
    { id: 'galactic',    label: 'Galactic',      meters: 1e21,       color: 0x7c5cbf, hex: '#7c5cbf' },
    { id: 'cosmic',      label: 'Cosmic',         meters: 1e26,       color: 0xd63031, hex: '#d63031' }
  ];

  let _scene, _camera, _renderer, _composer, _controls;
  let _scaleMeshes = [];
  let _scaleLabels = [];
  let _scaleRingMeshes = [];
  let _centralBeam;
  let _particles;
  let _clock;
  let _container;
  let _currentScaleId = 'matter';
  let _isTransitioning = false;
  let _transitionTimer = null;
  let _sceneRegistry = {};
  let _scaleChangeCallbacks = [];
  let _showLabels = true;
  let _raycaster = new THREE.Raycaster();
  let _mouse = new THREE.Vector2();

  // ── Coordinate conversion ────────────────────────────────────────────────

  function metersToY(meters) {
    const logM = Math.log10(meters);
    return ((logM - LOG_MIN) / LOG_RANGE) * BEAM_LENGTH;
  }

  function yToLogM(y) {
    return (y / BEAM_LENGTH) * LOG_RANGE + LOG_MIN;
  }

  function metersToLog(meters) {
    return Math.log10(meters);
  }

  // ── Scene graph ────────────────────────────────────────────────────────────

  function buildSceneGraph() {
    // Central beam
    const beamGeo = new THREE.CylinderGeometry(0.12, 0.12, BEAM_LENGTH + 6, 16);
    const beamMat = new THREE.MeshStandardMaterial({
      color: 0x00e5ff,
      emissive: 0x00e5ff,
      emissiveIntensity: 0.08,
      metalness: 0.9,
      roughness: 0.15,
      transparent: true,
      opacity: 0.35
    });
    _centralBeam = new THREE.Mesh(beamGeo, beamMat);
    _centralBeam.position.set(0, BEAM_LENGTH / 2, 0);
    _scene.add(_centralBeam);

    // Tick marks
    for (let i = 0; i <= 10; i++) {
      const y = i * 10;
      const tickGeo = new THREE.CylinderGeometry(0.22, 0.22, 0.5, 8);
      const tickMat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        emissiveIntensity: 0.15,
        transparent: true,
        opacity: 0.4
      });
      const tick = new THREE.Mesh(tickGeo, tickMat);
      tick.position.set(0, y, 0);
      _scene.add(tick);
    }

    // Scale nodes
    SCALE_DEFAULTS.forEach(function (scale, index) {
      const y = metersToY(scale.meters);
      const isEndpoint = index === 0 || index === SCALE_DEFAULTS.length - 1;
      const radius = isEndpoint ? 2.2 : 1.6;

      // Main sphere
      const geo = new THREE.SphereGeometry(radius, 32, 32);
      const mat = new THREE.MeshStandardMaterial({
        color: scale.color,
        emissive: scale.color,
        emissiveIntensity: index === 3 ? 0.6 : 0.25,
        metalness: 0.5,
        roughness: 0.5
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(0, y, 0);
      mesh.userData = {
        scaleId: scale.id,
        scaleIndex: index,
        baseScale: scale,
        radius: radius
      };
      _scene.add(mesh);
      _scaleMeshes.push(mesh);

      // Glow ring (horizontal, at node level)
      const ringGeo = new THREE.RingGeometry(radius + 0.4, radius + 0.8, 48);
      const ringMat = new THREE.MeshBasicMaterial({
        color: scale.color,
        transparent: true,
        opacity: 0.22,
        side: THREE.DoubleSide
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.set(0, y, 0);
      ring.rotation.x = Math.PI / 2;
      _scene.add(ring);
      _scaleRingMeshes.push(ring);

      // Vertical connection line from previous node
      if (index > 0) {
        const prevScale = SCALE_DEFAULTS[index - 1];
        const prevY = metersToY(prevScale.meters);
        const lineGeo = new THREE.CylinderGeometry(0.04, 0.04, y - prevY, 8);
        const lineMat = new THREE.MeshStandardMaterial({
          color: scale.color,
          emissive: scale.color,
          emissiveIntensity: 0.04,
          transparent: true,
          opacity: 0.25
        });
        const line = new THREE.Mesh(lineGeo, lineMat);
        line.position.set(0, prevY + (y - prevY) / 2, 0);
        _scene.add(line);
      }
    });

    // Background particles
    const count = 600;
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3]     = (Math.random() - 0.5) * 160;
      pos[i * 3 + 1] = Math.random() * (BEAM_LENGTH + 10);
      pos[i * 3 + 2] = (Math.random() - 0.5) * 160;
    }
    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    const pMat = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.25,
      transparent: true,
      opacity: 0.35
    });
    _particles = new THREE.Points(pGeo, pMat);
    _scene.add(_particles);
  }

  function buildLabels() {
    SCALE_DEFAULTS.forEach(function (scale, index) {
      const y = metersToY(scale.meters);
      const label = makeLabel(scale.label, scale.hex);
      const r = _scaleMeshes[index].userData.radius;
      label.position.set(r + 3, y, 0);
      _scene.add(label);
      _scaleLabels.push(label);
    });
  }

  function makeLabel(text, colorHex) {
    const canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 72;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 320, 72);
    ctx.font = 'bold 26px DM Sans, sans-serif';
    ctx.fillStyle = colorHex;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 8, 36);
    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.92 });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.set(14, 3.2, 1);
    return sprite;
  }

  // ── Camera / animation ────────────────────────────────────────────────────

  function flyToY(targetY, durationMs, onDone) {
    if (_transitionTimer) cancelAnimationFrame(_transitionTimer);
    _isTransitioning = true;
    const startY = _camera.position.y;
    const startTargetY = _controls.target.y;
    const start = performance.now();

    function step(now) {
      const t = Math.min((now - start) / durationMs, 1);
      const ease = 1 - Math.pow(1 - t, 3);
      _camera.position.y = startY + (targetY - startY) * ease;
      _controls.target.y = startTargetY + (targetY - startTargetY) * ease;
      if (t < 1) {
        _transitionTimer = requestAnimationFrame(step);
      } else {
        _isTransitioning = false;
        if (onDone) onDone();
      }
    }
    _transitionTimer = requestAnimationFrame(step);
  }

  function setLabelsVisible(visible) {
    _showLabels = visible;
    _scaleLabels.forEach(function (l) { l.visible = visible; });
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.ScaleEngine = {
    /**
     * Boot the engine. Creates scene, camera, renderer, controls, post-processing.
     * Returns { scene, camera, renderer, controls }.
     */
    init: function (containerEl) {
      _container = containerEl || document.getElementById('scaleScene');

      _clock = new THREE.Clock();
      _scene = new THREE.Scene();
      _scene.background = new THREE.Color(0x020408);
      _scene.fog = new THREE.FogExp2(0x020408, 0.006);

      _camera = new THREE.PerspectiveCamera(
        48,
        (_container ? _container.clientWidth : window.innerWidth) / (_container ? _container.clientHeight : window.innerHeight),
        0.1, 1000
      );
      _camera.position.set(0, metersToY(1e-18), 55);
      _camera.lookAt(0, metersToY(1e-18), 0);

      _renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
      _renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      _renderer.toneMapping = THREE.ACESFilmicToneMapping;
      _renderer.toneMappingExposure = 1.1;
      if (_container) {
        _renderer.setSize(_container.clientWidth, _container.clientHeight);
        _container.appendChild(_renderer.domElement);
      }

      var OrbitControlsCtor = getThreeAddon('OrbitControls');
      if (OrbitControlsCtor) {
        _controls = new OrbitControlsCtor(_camera, _renderer.domElement);
        _controls.enableDamping = true;
        _controls.dampingFactor = 0.05;
        _controls.minDistance = 18;
        _controls.maxDistance = 180;
      } else {
        _controls = {
          enableDamping: false,
          dampingFactor: 0,
          minDistance: 18,
          maxDistance: 180,
          target: new THREE.Vector3(),
          update: function () {
            _camera.lookAt(this.target);
          }
        };
      }
      _controls.target.set(0, metersToY(1e-18), 0);

      // Lighting
      _scene.add(new THREE.AmbientLight(0x223355, 0.7));
      const dir = new THREE.DirectionalLight(0xffffff, 0.9);
      dir.position.set(10, 60, 20);
      _scene.add(dir);
      const fill = new THREE.PointLight(0x00e5ff, 0.4, 220);
      fill.position.set(-30, 40, -20);
      _scene.add(fill);
      const rim = new THREE.PointLight(0xffdd55, 0.25, 200);
      rim.position.set(30, 70, 30);
      _scene.add(rim);

      // Bloom post-processing
      try {
        var EffectComposerCtor = getThreeAddon('EffectComposer');
        var RenderPassCtor = getThreeAddon('RenderPass');
        var UnrealBloomPassCtor = getThreeAddon('UnrealBloomPass');
        if (!EffectComposerCtor || !RenderPassCtor || !UnrealBloomPassCtor) {
          throw new Error('Post-processing addons not available');
        }
        _composer = new EffectComposerCtor(_renderer);
        _composer.addPass(new RenderPassCtor(_scene, _camera));
        const bloom = new UnrealBloomPassCtor(
          new THREE.Vector2(
            _container ? _container.clientWidth : 1280,
            _container ? _container.clientHeight : 720
          ),
          0.55, 0.38, 0.82
        );
        _composer.addPass(bloom);
      } catch (e) {
        _composer = null;
      }

      buildSceneGraph();
      buildLabels();

      return window.ScaleEngine;
    },

    /**
     * Navigate to a scale by id. Triggers camera fly-to, highlights node,
     * fires scale change callbacks.
     */
    navigateToScale: function (scaleId, options) {
      options = options || {};
      const scale = SCALE_DEFAULTS.find(function (s) { return s.id === scaleId; });
      if (!scale) return;
      var targetY = metersToY(scale.meters);
      var index = SCALE_DEFAULTS.indexOf(scale);

      _currentScaleId = scaleId;

      // Highlight
      _scaleMeshes.forEach(function (m, i) {
        var mat = m.material;
        if (i === index) {
          mat.emissiveIntensity = 0.75;
        } else {
          mat.emissiveIntensity = 0.22;
        }
      });

      // Ring pulse on selected
      _scaleRingMeshes.forEach(function (r, i) {
        r.material.opacity = (i === index) ? 0.45 : 0.18;
      });

      // Camera fly-to
      var duration = options.duration !== undefined ? options.duration : 1100;
      if (!_isTransitioning || options.force) {
        flyToY(targetY, duration);
      }

      // Fire callbacks
      _scaleChangeCallbacks.forEach(function (cb) {
        cb(scale, index);
      });

      // Switch registered scale scene
      if (_sceneRegistry[scaleId] && _sceneRegistry[scaleId].activate) {
        Object.keys(_sceneRegistry).forEach(function (id) {
          if (_sceneRegistry[id] && _sceneRegistry[id].deactivate) {
            _sceneRegistry[id].deactivate();
          }
        });
        _sceneRegistry[scaleId].activate(_scene, _camera);
      }
    },

    /**
     * Returns the scale object at screen pixel (x, y). Used for raycasting.
     * Returns null if no scale node is hit.
     */
    getScaleAtCursor: function (screenX, screenY) {
      if (!_renderer || !_camera) return null;
      var rect = _renderer.domElement.getBoundingClientRect();
      _mouse.x = ((screenX - rect.left) / rect.width) * 2 - 1;
      _mouse.y = -((screenY - rect.top) / rect.height) * 2 + 1;
      _raycaster.setFromCamera(_mouse, _camera);
      var hits = _raycaster.intersectObjects(_scaleMeshes);
      if (hits.length > 0) {
        return hits[0].object.userData;
      }
      return null;
    },

    /**
     * Register a per-scale scene object.
     * api: { activate(scene, camera), deactivate() }
     */
    registerScene: function (scaleId, api) {
      _sceneRegistry[scaleId] = api;
    },

    /**
     * Subscribe to scale change events.
     */
    onScaleChange: function (cb) {
      _scaleChangeCallbacks.push(cb);
    },

    getCurrentScaleId: function () {
      return _currentScaleId;
    },

    getLogPosition: function (scaleId) {
      var scale = SCALE_DEFAULTS.find(function (s) { return s.id === scaleId; });
      return scale ? metersToLog(scale.meters) : null;
    },

    getScaleNodes: function () {
      return _scaleMeshes;
    },

    getCamera: function () {
      return _camera;
    },

    getControls: function () {
      return _controls;
    },

    getScene: function () {
      return _scene;
    },

    getRenderer: function () {
      return _renderer;
    },

    getComposer: function () {
      return _composer;
    },

    getScales: function () {
      return SCALE_DEFAULTS;
    },

    setLabelsVisible: setLabelsVisible,

    isTransitioning: function () {
      return _isTransitioning;
    },

    /**
     * Called each frame by the render loop. Drives per-scale scene updates.
     * @param {number} dt  - delta time in seconds
     * @param {number} time - elapsed time in seconds
     */
    tick: function (dt, time) {
      var api = _sceneRegistry[_currentScaleId];
      if (api && typeof api.update === 'function') {
        api.update(dt, time);
      }
    },

    getActiveSceneApi: function () {
      return _sceneRegistry[_currentScaleId] || null;
    },

    resize: function () {
      if (!_container || !_renderer || !_camera) return;
      var w = _container.clientWidth;
      var h = _container.clientHeight;
      _camera.aspect = w / h;
      _camera.updateProjectionMatrix();
      _renderer.setSize(w, h);
      if (_composer) _composer.setSize(w, h);
    }
  };
}());
