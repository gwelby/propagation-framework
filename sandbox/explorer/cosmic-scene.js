/**
 * Cosmic Scene — Large-Scale Structure of the Universe
 * 
 * "Zoom out: the universe draws the same logic at the largest scale."
 * 
 * The cosmic web is the universe's standing wave pattern —
 * filaments are nodes of coherent propagation frozen at cosmic scale.
 * Galaxy clusters are coherence maxima at filament intersections.
 * Voids are destructive interference zones.
 * 
 * Visual layers:
 *   1. Cosmic web filaments  — glowing filamentary network (shader-driven)
 *   2. Galaxy cluster nodes  — bright point sources at filament intersections
 *   3. Void sphere           — outer boundary, destructive interference zone
 *   4. CMB glow haze         — volumetric remnant radiation
 *   5. Star field background — distant field emission
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;

  // ── Coordinate ────────────────────────────────────────────────────────────
  // Cosmis scale: log10(1e26) → y ≈ 99.7 on the 100-unit beam
  function cosmicY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((26 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Cosmic Web Filament Network ──────────────────────────────────────────
  // Procedurally generated filament tree using recursive branching
  function buildFilamentNetwork() {
    var centerY = cosmicY();
    var filaments = [];
    var nodes = [];

    // Node positions — filament intersections (galaxy cluster locations)
    var nodePositions = [
      [0, 0, 0],
      [7, 3, 2], [-5, 3, 4], [2, -4, 3],
      [10, 5, -1], [-8, 4, -3], [3, -6, 5],
      [-3, 6, -2], [6, -2, 6], [-5, -3, 3],
      [12, 6, 3], [-10, 5, -4], [4, 8, -1]
    ];

    // Connections — which nodes are linked by filaments
    var connections = [
      [0, 1], [0, 2], [0, 3],
      [1, 4], [2, 5], [3, 6],
      [0, 7], [0, 8], [0, 9],
      [7, 10], [5, 11], [6, 12]
    ];

    // Draw filaments as glowing cylinders
    connections.forEach(function (conn) {
      var from = nodePositions[conn[0]];
      var to = nodePositions[conn[1]];
      var fv = new THREE.Vector3(from[0], from[1], from[2]);
      var tv = new THREE.Vector3(to[0], to[1], to[2]);
      var mid = new THREE.Vector3().addVectors(fv, tv).multiplyScalar(0.5);
      var len = fv.distanceTo(tv);

      var geo = new THREE.CylinderGeometry(0.12, 0.12, len, 8);
      var mat = new THREE.MeshStandardMaterial({
        color: 0x7c5cbf,
        emissive: 0x7c5cbf,
        emissiveIntensity: 0.22,
        metalness: 0.7,
        roughness: 0.3,
        transparent: true,
        opacity: 0.7
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(5 + mid.x, centerY + mid.y - 5, mid.z);
      mesh.lookAt(5 + tv.x, centerY + tv.y - 5, tv.z);
      mesh.rotateX(Math.PI / 2);
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);

      // Add smaller side filaments branching off
      addBranchFilaments(mesh.position, tv.clone().sub(fv), centerY);
    });

    // Draw galaxy cluster nodes at filament intersections
    nodePositions.forEach(function (p, i) {
      var isCenter = i === 0;
      var radius = isCenter ? 0.6 : 0.35 + Math.random() * 0.2;
      var geo = new THREE.SphereGeometry(radius, 16, 16);
      var mat = new THREE.MeshStandardMaterial({
        color: isCenter ? 0xffdd55 : 0xd63031,
        emissive: isCenter ? 0xffdd55 : 0xd63031,
        emissiveIntensity: isCenter ? 0.9 : 0.6,
        metalness: 0.3,
        roughness: 0.4,
        transparent: true,
        opacity: isCenter ? 0.95 : 0.85
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(5 + p[0], centerY + p[1] - 5, p[2]);
      mesh.userData = {
        isCenter: isCenter,
        baseIntensity: mat.emissiveIntensity,
        phase: Math.random() * Math.PI * 2,
        orbitAngle: Math.random() * Math.PI * 2,
        orbitRadius: 0.3 + Math.random() * 0.4,
        orbitSpeed: (Math.random() - 0.5) * 0.3
      };
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);

      // Glow sprite around each cluster
      if (!isCenter) {
        var glowGeo = new THREE.SphereGeometry(radius * 2.5, 12, 12);
        var glowMat = new THREE.MeshBasicMaterial({
          color: 0xd63031,
          transparent: true,
          opacity: 0.06,
          side: THREE.BackSide
        });
        var glow = new THREE.Mesh(glowGeo, glowMat);
        glow.position.copy(mesh.position);
        _objs.push(glow);
        _mats.push(glowMat);
        scene.add(glow);
      }
    });
  }

  // Branch filaments from parent filament midpoint
  function addBranchFilaments(from, direction, centerY) {
    var numBranches = 1 + Math.floor(Math.random() * 2);
    for (var b = 0; b < numBranches; b++) {
      var perp = new THREE.Vector3(
        (Math.random() - 0.5) * 2,
        (Math.random() - 0.5) * 2,
        (Math.random() - 0.5) * 2
      ).normalize();
      if (perp.dot(direction) > 0.9) {
        perp = new THREE.Vector3(1, 0, 0);
      }
      var len = 1.5 + Math.random() * 2;
      var end = from.clone().add(perp.multiplyScalar(len));

      var geo = new THREE.CylinderGeometry(0.04, 0.04, len, 6);
      var mat = new THREE.MeshStandardMaterial({
        color: 0x7c5cbf,
        emissive: 0x7c5cbf,
        emissiveIntensity: 0.12,
        transparent: true,
        opacity: 0.4
      });
      var mesh = new THREE.Mesh(geo, mat);
      var mid = new THREE.Vector3().addVectors(from, end).multiplyScalar(0.5);
      mesh.position.copy(mid);
      mesh.lookAt(end);
      mesh.rotateX(Math.PI / 2);
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);
    }
  }

  // ── Void Sphere — outer boundary ─────────────────────────────────────────
  function buildVoidSphere() {
    var centerY = cosmicY();

    // Multiple nested void shells for depth
    [24, 20, 16].forEach(function (r, i) {
      var opacity = 0.04 + i * 0.02;
      var geo = new THREE.SphereGeometry(r, 48, 48);
      var mat = new THREE.MeshBasicMaterial({
        color: 0x020408,
        side: THREE.BackSide,
        transparent: true,
        opacity: opacity
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(5, centerY, 0);
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);
    });

    // Void boundary glow ring
    var ringGeo = new THREE.TorusGeometry(18, 0.15, 8, 64);
    var ringMat = new THREE.MeshBasicMaterial({
      color: 0x7c5cbf,
      transparent: true,
      opacity: 0.08
    });
    var ring = new THREE.Mesh(ringGeo, ringMat);
    ring.position.set(5, centerY, 0);
    ring.rotation.x = Math.PI / 2;
    _objs.push(ring);
    _mats.push(ringMat);
    scene.add(ring);
  }

  // ── CMB Haze — volumetric glow ─────────────────────────────────────────
  function buildCMBHaze() {
    var centerY = cosmicY();

    var geo = new THREE.SphereGeometry(14, 32, 32);
    var mat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uColor: { value: new THREE.Color(0x7c5cbf) }
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
        'uniform vec3 uColor;',
        'varying vec3 vNormal;',
        'varying vec3 vPosition;',

        'float hash(vec3 p) {',
        '  return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453);',
        '}',

        'void main() {',
        '  // Fresnel glow at edges',
        '  float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.8);',

        '  // Animated noise for CMB anisotropy',
        '  vec3 p = vPosition * 0.12 + uTime * 0.03;',
        '  float n = hash(floor(p * 8.0)) * 0.5 + hash(floor(p * 16.0)) * 0.3;',

        '  float alpha = fresnel * 0.18 + n * 0.04;',
        '  gl_FragColor = vec4(uColor * (0.5 + n * 0.5), alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.BackSide,
      depthWrite: false
    });
    var mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(5, centerY, 0);
    _objs.push(mesh);
    _shaders.push(mat);
    scene.add(mesh);
  }

  // ── Background Star Field ────────────────────────────────────────────────
  function buildStarField() {
    var count = 800;
    var positions = new Float32Array(count * 3);
    for (var i = 0; i < count; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 20 + Math.random() * 12;
      positions[i * 3]     = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
    }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var mat = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.12,
      transparent: true,
      opacity: 0.6,
      sizeAttenuation: true
    });
    var stars = new THREE.Points(geo, mat);
    stars.position.set(5, cosmicY(), 0);
    stars.userData.rotSpeed = 0.003;
    _objs.push(stars);
    _mats.push(mat);
    scene.add(stars);
  }

  // ── Cosmic Scale Label ────────────────────────────────────────────────────
  function buildLabel() {
    if (!window.ScaleEngine) return;
    var canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 96;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 512, 96);
    ctx.font = 'bold 32px DM Sans, sans-serif';
    ctx.fillStyle = '#d63031';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Cosmic Scale — 10²⁶ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, cosmicY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.CosmicScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();

      // Volumetric medium fog — space is not empty
      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.008 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.008);
      }

      buildVoidSphere();
      buildCMBHaze();
      buildFilamentNetwork();
      buildStarField();
      buildLabel();

      // Camera setup
      camera.position.set(5, cosmicY(), 28);
      camera.lookAt(5, cosmicY(), 0);
    },

    update: function (dt, time) {
      // Shader uniforms
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      // Galaxy node pulsing
      _objs.forEach(function (o) {
        if (o.userData && o.userData.baseIntensity !== undefined && !o.userData.isCenter) {
          var pulse = 0.55 + 0.35 * Math.sin(time * 1.2 + o.userData.phase);
          o.material.emissiveIntensity = o.userData.baseIntensity * pulse;
        }
        // Slow star field rotation
        if (o.userData && o.userData.rotSpeed) {
          o.rotation.y += dt * o.userData.rotSpeed;
        }
        // Galaxy orbit
        if (o.userData && o.userData.orbitSpeed && !o.userData.isCenter) {
          o.userData.orbitAngle += dt * o.userData.orbitSpeed;
          var r = o.userData.orbitRadius;
          o.position.x += Math.cos(o.userData.orbitAngle) * 0.001;
          o.position.z += Math.sin(o.userData.orbitAngle) * 0.001;
        }
        // Filament shimmer
        if (o.geometry && o.geometry.type === 'CylinderGeometry' && o.geometry.parameters) {
          var lp = o.position.x * 0.1;
          o.material.emissiveIntensity = 0.15 + 0.08 * Math.sin(time * 0.4 + lp);
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
