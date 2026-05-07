/**
 * Human Scene — Solid-Looking Macro Objects at the Everyday Scale
 *
 * "At the human scale, coherence appears as solidity."
 *
 * At 10⁰ meters — the scale of everyday objects — quantum uncertainty
 * averages out into the solid, persistent forms we experience. A chair.
 * A human hand. These are not 'real' in an absolute sense; they are
 * stable coherence patterns at our observation scale.
 *
 * Visual layers:
 *   1. Human figure silhouette — the observer at the center
 *   2. Chair — a macro object demonstrating persistent form
 *   3. Table surface — the stage for human-scale interaction
 *   4. Light and shadow — demonstrating how we see solid objects
 *   5. The 2/3 ratio symbol — the Koide relation, visible at this scale
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;

  // ── Coordinate ────────────────────────────────────────────────────────────
  function humanY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((0 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Human Figure ──────────────────────────────────────────────────────────
  function buildHumanFigure() {
    var centerY = humanY();
    var basePos = new THREE.Vector3(5, centerY, 0);

    // Material for human form — warm, solid-looking
    var skinMat = new THREE.MeshStandardMaterial({
      color: 0xffb347,
      emissive: 0xffb347,
      emissiveIntensity: 0.1,
      metalness: 0.1,
      roughness: 0.7
    });

    // Torso — capsule shape
    var torsoGeo = new THREE.CapsuleGeometry(0.9, 2.2, 8, 16);
    var torso = new THREE.Mesh(torsoGeo, skinMat);
    torso.position.copy(basePos).add(new THREE.Vector3(0, 1.6, 0));
    _objs.push(torso);
    _mats.push(skinMat);
    scene.add(torso);

    // Head
    var headGeo = new THREE.SphereGeometry(0.7, 24, 24);
    var head = new THREE.Mesh(headGeo, skinMat);
    head.position.copy(basePos).add(new THREE.Vector3(0, 3.8, 0));
    _objs.push(head);
    scene.add(head);

    // Shoulders/arms hint (simplified)
    var shoulderGeo = new THREE.CapsuleGeometry(0.4, 1.5, 6, 12);

    var leftArm = new THREE.Mesh(shoulderGeo, skinMat);
    leftArm.position.copy(basePos).add(new THREE.Vector3(-1.2, 2.5, 0));
    leftArm.rotation.z = Math.PI / 6;
    _objs.push(leftArm);
    scene.add(leftArm);

    var rightArm = new THREE.Mesh(shoulderGeo, skinMat);
    rightArm.position.copy(basePos).add(new THREE.Vector3(1.2, 2.5, 0));
    rightArm.rotation.z = -Math.PI / 6;
    _objs.push(rightArm);
    scene.add(rightArm);

    // Shadow plane beneath figure
    var shadowGeo = new THREE.CircleGeometry(1.8, 32);
    var shadowMat = new THREE.MeshBasicMaterial({
      color: 0x000000,
      transparent: true,
      opacity: 0.2
    });
    var shadow = new THREE.Mesh(shadowGeo, shadowMat);
    shadow.position.copy(basePos).add(new THREE.Vector3(0, 0.05, 0));
    shadow.rotation.x = -Math.PI / 2;
    _objs.push(shadow);
    _mats.push(shadowMat);
    scene.add(shadow);
  }

  // ── Chair Object ───────────────────────────────────────────────────────────
  function buildChair() {
    var centerY = humanY();
    var chairPos = new THREE.Vector3(5 - 3, centerY, 1.5);

    var woodMat = new THREE.MeshStandardMaterial({
      color: 0x8b4513,
      emissive: 0x5c2d0d,
      emissiveIntensity: 0.05,
      metalness: 0.1,
      roughness: 0.8
    });

    // Seat
    var seatGeo = new THREE.BoxGeometry(1.4, 0.15, 1.4);
    var seat = new THREE.Mesh(seatGeo, woodMat);
    seat.position.copy(chairPos).add(new THREE.Vector3(0, 1.2, 0));
    _objs.push(seat);
    _mats.push(woodMat);
    scene.add(seat);

    // Backrest
    var backGeo = new THREE.BoxGeometry(1.4, 1.5, 0.12);
    var back = new THREE.Mesh(backGeo, woodMat);
    back.position.copy(chairPos).add(new THREE.Vector3(0, 2.0, -0.65));
    back.rotation.x = -0.1;
    _objs.push(back);
    scene.add(back);

    // Legs
    var legGeo = new THREE.CylinderGeometry(0.08, 0.06, 1.2, 8);
    var legPositions = [
      { x: -0.6, z: -0.6 },
      { x: 0.6, z: -0.6 },
      { x: -0.6, z: 0.6 },
      { x: 0.6, z: 0.6 }
    ];

    legPositions.forEach(function (pos) {
      var leg = new THREE.Mesh(legGeo, woodMat);
      leg.position.copy(chairPos).add(new THREE.Vector3(pos.x, 0.6, pos.z));
      _objs.push(leg);
      scene.add(leg);
    });
  }

  // ── Table Surface ──────────────────────────────────────────────────────────
  function buildTable() {
    var centerY = humanY();
    var tablePos = new THREE.Vector3(5 + 2.5, centerY, -1);

    // Table top
    var topMat = new THREE.MeshStandardMaterial({
      color: 0x4a4a4a,
      emissive: 0x2a2a2a,
      emissiveIntensity: 0.08,
      metalness: 0.6,
      roughness: 0.4
    });

    var topGeo = new THREE.BoxGeometry(2.5, 0.1, 1.8);
    var top = new THREE.Mesh(topGeo, topMat);
    top.position.copy(tablePos).add(new THREE.Vector3(0, 1.5, 0));
    _objs.push(top);
    _mats.push(topMat);
    scene.add(top);

    // Table legs
    var tableLegGeo = new THREE.CylinderGeometry(0.1, 0.08, 1.5, 8);
    var legOffsets = [
      { x: -1, z: -0.7 },
      { x: 1, z: -0.7 },
      { x: -1, z: 0.7 },
      { x: 1, z: 0.7 }
    ];

    legOffsets.forEach(function (offset) {
      var leg = new THREE.Mesh(tableLegGeo, topMat);
      leg.position.copy(tablePos).add(new THREE.Vector3(offset.x, 0.75, offset.z));
      _objs.push(leg);
      scene.add(leg);
    });

    // Objects on table — a sphere and cube representing macro objects
    var sphereGeo = new THREE.SphereGeometry(0.25, 24, 24);
    var sphereMat = new THREE.MeshStandardMaterial({
      color: 0x4488ff,
      metalness: 0.5,
      roughness: 0.3
    });
    var sphere = new THREE.Mesh(sphereGeo, sphereMat);
    sphere.position.copy(tablePos).add(new THREE.Vector3(-0.5, 1.85, 0.3));
    _objs.push(sphere);
    _mats.push(sphereMat);
    scene.add(sphere);

    var cubeGeo = new THREE.BoxGeometry(0.35, 0.35, 0.35);
    var cubeMat = new THREE.MeshStandardMaterial({
      color: 0xff4444,
      metalness: 0.3,
      roughness: 0.5
    });
    var cube = new THREE.Mesh(cubeGeo, cubeMat);
    cube.position.copy(tablePos).add(new THREE.Vector3(0.3, 1.85, -0.2));
    cube.rotation.y = Math.PI / 8;
    _objs.push(cube);
    _mats.push(cubeMat);
    scene.add(cube);
  }

  // ── Floor Plane ────────────────────────────────────────────────────────────
  function buildFloor() {
    var centerY = humanY();

    var floorGeo = new THREE.PlaneGeometry(20, 16);
    var floorMat = new THREE.MeshStandardMaterial({
      color: 0x1a1a2e,
      roughness: 0.9
    });
    var floor = new THREE.Mesh(floorGeo, floorMat);
    floor.position.set(5, centerY, 0);
    floor.rotation.x = -Math.PI / 2;
    _objs.push(floor);
    _mats.push(floorMat);
    scene.add(floor);

    // Floor grid for scale reference
    var gridHelper = new THREE.GridHelper(20, 20, 0x444466, 0x2a2a3e);
    gridHelper.position.set(5, centerY + 0.01, 0);
    _objs.push(gridHelper);
    scene.add(gridHelper);
  }

  // ── The 2/3 Ratio Symbol ─────────────────────────────────────────────────
  // The Koide relation appears at human scale as proportion
  function buildRatioSymbol() {
    var centerY = humanY();
    var symbolPos = new THREE.Vector3(8.5, centerY + 2.5, 1);

    // Two interlocking rings representing the 2/3 ratio
    var ringGeo = new THREE.TorusGeometry(0.4, 0.06, 8, 32);
    var ringMat = new THREE.MeshStandardMaterial({
      color: 0xffb347,
      emissive: 0xffb347,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.8
    });

    var ring1 = new THREE.Mesh(ringGeo, ringMat);
    ring1.position.copy(symbolPos);
    ring1.rotation.x = Math.PI / 4;
    _objs.push(ring1);
    _mats.push(ringMat);
    scene.add(ring1);

    var ring2 = new THREE.Mesh(ringGeo, ringMat);
    ring2.position.copy(symbolPos);
    ring2.rotation.y = Math.PI / 4;
    _objs.push(ring2);
    scene.add(ring2);

    // Store for animation
    ring1.userData = { isRatioRing: true, speed: 0.5 };
    ring2.userData = { isRatioRing: true, speed: -0.3 };
  }

  // ── Ambient Particles ──────────────────────────────────────────────────────
  // Dust motes visible in light beams — a human-scale phenomenon
  function buildDustParticles() {
    var centerY = humanY();
    var count = 200;
    var positions = new Float32Array(count * 3);

    for (var i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 12;
      positions[i * 3 + 1] = Math.random() * 5;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 8;
    }

    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var mat = new THREE.PointsMaterial({
      color: 0xffdd88,
      size: 0.03,
      transparent: true,
      opacity: 0.4,
      sizeAttenuation: true
    });
    var dust = new THREE.Points(geo, mat);
    dust.position.set(5, centerY, 0);
    dust.userData = { isDust: true, drift: 0.1 };
    _objs.push(dust);
    _mats.push(mat);
    scene.add(dust);
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
    ctx.fillStyle = '#ffb347';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Human Scale — 10⁰ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, humanY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.HumanScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();

      // Softer fog for interior scene
      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x0a0a14, density: 0.015 });
      } else {
        scene.fog = new THREE.FogExp2(0x0a0a14, 0.015);
      }

      buildFloor();
      buildHumanFigure();
      buildChair();
      buildTable();
      buildRatioSymbol();
      buildDustParticles();
      buildLabel();

      // Camera setup
      camera.position.set(5, humanY() + 3, 15);
      camera.lookAt(5, humanY() + 2, 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, humanY() + 3, 15),
        target: new THREE.Vector3(5, humanY() + 2, 0),
        fov: 48
      };
    },

    getSharedElements: function () {
      // Return chair edge meshes for propagation wave morphing
      return _objs.filter(function (o) {
        return o.geometry && (
          o.geometry.type === 'BoxGeometry' ||
          o.geometry.type === 'CylinderGeometry'
        );
      }).slice(0, 4); // First 4 structural elements
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Human scene uses medium LOD
      return 1;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      // Apply LOD settings if provided
      if (lodSettings) {
        console.log('[HumanScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      // Update shader uniforms
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      // Animate ratio rings
      _objs.forEach(function (o) {
        if (o.userData && o.userData.isRatioRing) {
          o.rotation.x += dt * o.userData.speed;
          o.rotation.y += dt * o.userData.speed * 0.7;
        }
        // Slowly drift dust particles
        if (o.userData && o.userData.isDust) {
          o.rotation.y += dt * o.userData.drift * 0.1;
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
