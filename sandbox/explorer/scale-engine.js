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

  const LOG_MIN = -40;
  const LOG_MAX = 26;
  const LOG_RANGE = LOG_MAX - LOG_MIN;
  const BEAM_LENGTH = 100;

  function getThreeAddon(name) {
    return THREE[name] || window[name];
  }

  const SCALE_DEFAULTS = [
    { id: 'axiomatic-root',label: 'Axiomatic Root', meters: 1e-40, color: 0xff0055, hex: '#ff0055' },
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
  let _mediumLayer;
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

      // Human Anchor Highlight
      if (scale.id === 'human') {
        mat.emissiveIntensity = 0.8;
        const auraGeo = new THREE.SphereGeometry(radius + 1.2, 32, 32);
        const auraMat = new THREE.MeshBasicMaterial({ color: scale.color, transparent: true, opacity: 0.25, blending: THREE.AdditiveBlending });
        const aura = new THREE.Mesh(auraGeo, auraMat);
        mesh.add(aura);
        mesh.userData.isHumanAnchor = true;
      }

      // Graveyard (NO-GO) visual integration — use audited PFClaimsData layer
      var hasNoGo = false;
      (function () {
        var pfc = window.PFClaimsData;
        if (!pfc) return;
        // Check if any SCALE_ANCHOR for this scale has a claim that is NO-GO,
        // OR if any NOGO entry has a target scaleId matching this node.
        var anchors = pfc.SCALE_ANCHORS || [];
        var anchor = anchors.find(function (a) {
          // Match by approximate log₁₀ distance: find anchors near this scale
          return Math.abs(Math.log10(scale.meters) - Math.log10(a.meters)) < 1.5;
        });
        if (anchor && anchor.claims) {
          var claims = pfc.CLAIMS || [];
          var nogos  = pfc.NOGOS  || [];
          // Check if any claim at this anchor is NO-GO status
          anchor.claims.forEach(function (cid) {
            var c = claims.find(function (x) { return x.id === cid; });
            if (c && c.status && c.status.label === 'NO-GO') hasNoGo = true;
          });
          // Also flag if any NO-GO route targets a claim anchored here
          anchor.claims.forEach(function (cid) {
            var n = nogos.find(function (x) { return x.target === cid; });
            if (n) hasNoGo = true; // Amber warning: has at least one failed route
          });
        }
      }());
      if (hasNoGo) {
        mat.wireframe = true;
        mat.color.setHex(0xff4757); // Scar Tissue Red
        mat.emissive.setHex(0xff4757);
        mat.emissiveIntensity = 0.5;
        mat.transparent = true;
        mat.opacity = 0.6;
        mesh.userData.isGraveyard = true;
      }

      mesh.position.set(0, y, 0);
      mesh.userData.scaleId = scale.id;
      mesh.userData.scaleIndex = index;
      mesh.userData.baseScale = scale;
      mesh.userData.radius = radius;
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

    // Medium Layer (Quantum Foam background)
    const foamGeo = new THREE.BufferGeometry();
    const foamCount = 2000;
    const foamPos = new Float32Array(foamCount * 3);
    for (let i = 0; i < foamCount; i++) {
      foamPos[i * 3]     = (Math.random() - 0.5) * 200;
      foamPos[i * 3 + 1] = Math.random() * (BEAM_LENGTH + 20) - 10;
      foamPos[i * 3 + 2] = (Math.random() - 0.5) * 200;
    }
    foamGeo.setAttribute('position', new THREE.BufferAttribute(foamPos, 3));
    const foamMat = new THREE.PointsMaterial({
      color: 0x8800ff,
      size: 0.35,
      transparent: true,
      opacity: 0.15,
      blending: THREE.AdditiveBlending
    });
    _mediumLayer = new THREE.Points(foamGeo, foamMat);
    _mediumLayer.visible = false; // toggled via API
    _scene.add(_mediumLayer);
  }

  function buildLabels() {
    // Rightmost scales that need LEFT-side labels to avoid info panel
    var leftSideIndices = [12, 13, 14, 15]; // planetary, stellar, galactic, cosmic

    SCALE_DEFAULTS.forEach(function (scale, index) {
      const y = metersToY(scale.meters);
      const r = _scaleMeshes[index].userData.radius;

      // Position: right side for most, left side for top scales
      var isLeftSide = leftSideIndices.indexOf(index) >= 0;
      var xOffset = isLeftSide ? -(r + 3) : (r + 3);

      const label = makeLabel(scale.label, scale.hex, isLeftSide);
      label.position.set(xOffset, y, 0);

      // Store original position for reference
      label.userData.baseX = xOffset;
      label.userData.baseY = y;

      _scene.add(label);
      _scaleLabels.push(label);
    });
  }

  function makeLabel(text, colorHex, alignRight) {
    const canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 72;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 320, 72);
    ctx.font = 'bold 26px DM Sans, sans-serif';
    ctx.fillStyle = colorHex;
    // For left-side labels, align right so text extends away from the node
    ctx.textAlign = alignRight ? 'right' : 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, alignRight ? 312 : 8, 36);
    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.92 });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.set(14, 3.2, 1);
    sprite.center.set(alignRight ? 1 : 0, 0.5);
    return sprite;
  }

  // ── Camera / animation ────────────────────────────────────────────────────

  function flyToY(targetY, durationMs, onDone) {
    if (_transitionTimer) cancelAnimationFrame(_transitionTimer);

    // Handle instant jump (duration = 0) without NaN
    if (!durationMs || durationMs <= 0) {
      _camera.position.y = targetY;
      _controls.target.y = targetY;
      _isTransitioning = false;
      if (onDone) onDone();
      return;
    }

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

  // Update label visibility based on camera distance — hide distant labels
  function updateLabelVisibility(cameraY) {
    if (!_showLabels) return;
    const VISIBILITY_RANGE = 12; // Reduced range to prevent overlap
    _scaleLabels.forEach(function (label, i) {
      const labelY = label.position.y;
      const distance = Math.abs(labelY - cameraY);
      // Fade out distant labels
      if (distance < VISIBILITY_RANGE) {
        label.visible = true;
        // Quadratic fade down to 0 for smoother transitions
        const opacity = 1 - Math.pow(distance / VISIBILITY_RANGE, 2);
        label.material.opacity = Math.max(0.0, opacity * 0.92);
      } else {
        label.visible = false;
      }
    });
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

      // Get device performance profile for quality settings
      var perfProfile = window.PerformanceEngine ? window.PerformanceEngine.DeviceProfile : null;
      var pixelRatio = perfProfile ? perfProfile.pixelRatio : Math.min(window.devicePixelRatio, 2);
      var enableBloom = perfProfile ? perfProfile.enableBloom : true;
      var enableShadows = perfProfile ? perfProfile.enableShadows : true;
      var shaderQuality = perfProfile ? perfProfile.shaderQuality : 'full';

      // Adjust fog density based on tier
      var fogDensity = perfProfile && perfProfile.tier === 'low' ? 0.005 : 0.002;
      _scene.fog = new THREE.FogExp2(0x020408, fogDensity);

      _camera = new THREE.PerspectiveCamera(
        48,
        (_container ? _container.clientWidth : window.innerWidth) / (_container ? _container.clientHeight : window.innerHeight),
        0.1, 1000
      );
      _camera.position.set(0, metersToY(1e-18), 55);
      _camera.lookAt(0, metersToY(1e-18), 0);

      _renderer = new THREE.WebGLRenderer({
        antialias: perfProfile ? perfProfile.tier !== 'low' : true,
        alpha: true,
        powerPreference: perfProfile && perfProfile.tier === 'low' ? 'low-power' : 'high-performance'
      });
      _renderer.setPixelRatio(pixelRatio);
      _renderer.setClearColor(0x020408, 1);

      // Tone mapping only on capable devices
      if (shaderQuality !== 'low') {
        _renderer.toneMapping = THREE.ACESFilmicToneMapping;
        _renderer.toneMappingExposure = 1.1;
      } else {
        _renderer.toneMapping = THREE.NoToneMapping;
      }

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

      // Bloom post-processing (conditional based on device tier)
      if (enableBloom && shaderQuality !== 'low') {
        try {
          var EffectComposerCtor = getThreeAddon('EffectComposer');
          var RenderPassCtor = getThreeAddon('RenderPass');
          var UnrealBloomPassCtor = getThreeAddon('UnrealBloomPass');
          if (!EffectComposerCtor || !RenderPassCtor || !UnrealBloomPassCtor) {
            throw new Error('Post-processing addons not available');
          }
          _composer = new EffectComposerCtor(_renderer);
          _composer.addPass(new RenderPassCtor(_scene, _camera));

          // Adjust bloom quality based on tier
          var bloomStrength = shaderQuality === 'medium' ? 0.4 : 0.55;
          var bloomRadius = shaderQuality === 'medium' ? 0.3 : 0.38;
          var bloomThreshold = shaderQuality === 'medium' ? 0.9 : 0.82;

          const bloom = new UnrealBloomPassCtor(
            new THREE.Vector2(
              _container ? _container.clientWidth : 1280,
              _container ? _container.clientHeight : 720
            ),
            bloomStrength, bloomRadius, bloomThreshold
          );
          _composer.addPass(bloom);
        } catch (e) {
          _composer = null;
        }
      } else {
        _composer = null;
      }

      buildSceneGraph();
      buildLabels();

      // Initialize TransitionEngine with our scene/camera/renderer
      if (window.TransitionEngine && window.TransitionEngine.init) {
        window.TransitionEngine.init(
          window.ScaleEngine,
          _scene,
          _camera,
          _renderer,
          _composer
        );
        console.log('[ScaleEngine] TransitionEngine integrated');
      }

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

      // Switch registered scale scene with PerformanceEngine LOD hooks
      if (_sceneRegistry[scaleId] && _sceneRegistry[scaleId].activate) {
        Object.keys(_sceneRegistry).forEach(function (id) {
          if (_sceneRegistry[id] && _sceneRegistry[id].deactivate) {
            _sceneRegistry[id].deactivate();
          }
        });
        
        // Get LOD settings from PerformanceEngine
        var lodSettings = null;
        if (window.PerformanceEngine && window.PerformanceEngine.getLODSettings) {
          lodSettings = window.PerformanceEngine.getLODSettings(scaleId);
        }
        
        // Prepare scene using TransitionEngine if available
        if (window.TransitionEngine && window.TransitionEngine.prepareScene) {
          window.TransitionEngine.prepareScene(scaleId, lodSettings);
        }
        
        // Activate the scene with LOD-aware settings
        _sceneRegistry[scaleId].activate(_scene, _camera, lodSettings);
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
    updateLabelVisibility: updateLabelVisibility,

    isTransitioning: function () {
      return _isTransitioning;
    },

    toggleMediumLayer: function (visible) {
      if (_mediumLayer) {
        _mediumLayer.visible = visible !== undefined ? visible : !_mediumLayer.visible;
      }
    },

    /**
     * Called each frame by the render loop. Drives per-scale scene updates.
     * @param {number} dt  - delta time in seconds
     * @param {number} time - elapsed time in seconds
     */
    tick: function (dt, time) {
      // Update TransitionEngine for smooth camera transitions
      if (window.TransitionEngine && window.TransitionEngine.update) {
        window.TransitionEngine.update(dt, time);
      }

      if (_mediumLayer && _mediumLayer.visible) {
        _mediumLayer.rotation.y += 0.05 * dt;
        var positions = _mediumLayer.geometry.attributes.position.array;
        for (let i = 0; i < positions.length; i += 3) {
          positions[i+1] += Math.sin(time * 2 + positions[i]) * 0.01;
        }
        _mediumLayer.geometry.attributes.position.needsUpdate = true;
      }

      var api = _sceneRegistry[_currentScaleId];
      if (api && typeof api.update === 'function') {
        api.update(dt, time);
      }
    },

    getActiveSceneApi: function () {
      return _sceneRegistry[_currentScaleId] || null;
    },

    getSceneRegistry: function () {
      return _sceneRegistry;
    },

    /**
     * Trigger wave visualization for the current scale — the proof IS the experience.
     * Activates propagation wave demonstration at the selected scale.
     * @param {string} scaleId — optional scale to visualize (defaults to current)
     */
    triggerWaveVisualization: function (scaleId) {
      var targetId = scaleId || _currentScaleId;
      var api = _sceneRegistry[targetId];

      // Pulse the scale node to indicate wave activation
      var nodeMesh = _scaleMeshes.find(function (m) {
        return m.userData && m.userData.scaleId === targetId;
      });

      if (nodeMesh) {
        // Visual pulse — the wave begins here
        var originalScale = nodeMesh.scale.x;
        var pulseDuration = 600;
        var startTime = performance.now();

        function pulse() {
          var elapsed = performance.now() - startTime;
          var progress = Math.min(elapsed / pulseDuration, 1);
          var wave = Math.sin(progress * Math.PI) * 0.3;
          var newScale = originalScale * (1 + wave);
          nodeMesh.scale.set(newScale, newScale, newScale);

          if (progress < 1) {
            requestAnimationFrame(pulse);
          } else {
            nodeMesh.scale.set(originalScale, originalScale, originalScale);
          }
        }
        pulse();
      }

      // Notify the per-scale scene to begin wave mode
      if (api && typeof api.beginWaveMode === 'function') {
        api.beginWaveMode();
      }

      // Dispatch event for external listeners
      try {
        window.dispatchEvent(new CustomEvent('pf:wave-visualization-started', {
          detail: { scaleId: targetId, timestamp: performance.now() }
        }));
      } catch (e) {}
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
