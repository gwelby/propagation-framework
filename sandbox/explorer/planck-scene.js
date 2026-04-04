/**
 * Planck Scene — Discrete Geometry at the Foundation of Space
 * 
 * "Zoom further: space stops behaving like space."
 * 
 * At the Planck scale, continuous spacetime dissolves into a discrete
 * coherent geometry — a spinfoam. Vertices are coherence events.
 * Edges are propagation paths between them.
 * The topology of space can change at each vertex.
 * 
 * This scene visualizes that scaffolding — not simulated physics,
 * but the geometric intuition: space as a standing pattern of events.
 * 
 * Visual layers:
 *   1. Spinfoam vertex network  — coherent geometry nodes (glowing)
 *   2. Propagation edges       — paths between vertices
 *   3. Vertex wave pulses       — animated coherence propagation
 *   4. Topology flip event      — occasional vertex reconfiguration
 *   5. Quantum shimmer          — high-frequency noise overlay
 *   6. Emergence glow            — hint that continuous space fades in above
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;
  var _flipTimer = 0;
  var _flipInterval = 3.5; // seconds between topology flip events

  // ── Coordinate ────────────────────────────────────────────────────────────
  function planckY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((Math.log10(1.616e-35) - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Spinfoam Vertex Network ──────────────────────────────────────────────
  function buildSpinfoamNetwork() {
    var centerY = planckY();

    // Create a network of vertices (coherence events)
    // in a roughly spherical arrangement with tetrahedral-ish local structure
    var vertices = [];
    var N = 14; // number of vertices

    // Icosahedral-like distribution (more uniform than random)
    var phi = (1 + Math.sqrt(5)) / 2;
    for (var i = 0; i < N; i++) {
      var theta = 2 * Math.PI * i / phi;
      var ya = 2 * i / N - 1 + (1 / N);
      var ra = Math.sqrt(1 - ya * ya);
      var radius = 2.5 + Math.random() * 1.5;
      vertices.push(new THREE.Vector3(
        radius * ra * Math.cos(theta) + (Math.random() - 0.5) * 0.8,
        ya * radius * ra + (Math.random() - 0.5) * 0.8,
        radius * ra * Math.sin(theta) + (Math.random() - 0.5) * 0.8
      ));
    }

    // Draw propagation edges between nearby vertices
    var edgeSet = new Set();
    vertices.forEach(function (v, i) {
      // Connect to 2-3 nearest neighbors
      var dists = vertices.map(function (v2, j) {
        return { dist: v.distanceTo(v2), j: j };
      }).filter(function (d) { return d.j !== i; })
        .sort(function (a, b) { return a.dist - b.dist; });

      var numConn = 2 + Math.floor(Math.random() * 2);
      dists.slice(0, numConn).forEach(function (d) {
        var key = [Math.min(i, d.j), Math.max(i, d.j)].join('-');
        if (!edgeSet.has(key)) {
          edgeSet.add(key);
          buildEdge(vertices[i], vertices[d.j], centerY);
        }
      });
    });

    // Draw vertex spheres
    vertices.forEach(function (v, i) {
      var isCentral = i === 0;
      var radius = isCentral ? 0.22 : 0.12 + Math.random() * 0.08;
      var geo = new THREE.SphereGeometry(radius, 16, 16);
      var mat = new THREE.MeshStandardMaterial({
        color: isCentral ? 0xffd700 : 0xd4a017,
        emissive: isCentral ? 0xffd700 : 0xd4a017,
        emissiveIntensity: isCentral ? 1.0 : 0.5 + Math.random() * 0.4,
        metalness: 0.6,
        roughness: 0.3,
        transparent: true,
        opacity: 0.92
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(5 + v.x, centerY + v.y - 5, v.z);
      mesh.userData = {
        baseIntensity: mat.emissiveIntensity,
        phase: Math.random() * Math.PI * 2,
        pulseSpeed: 1.5 + Math.random() * 1.5,
        originalPos: mesh.position.clone(),
        isCentral: isCentral
      };
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);

      // Glow halo around each vertex
      if (!isCentral) {
        var glowGeo = new THREE.SphereGeometry(radius * 4, 12, 12);
        var glowMat = new THREE.MeshBasicMaterial({
          color: 0xffd700,
          transparent: true,
          opacity: 0.04,
          side: THREE.BackSide
        });
        var glow = new THREE.Mesh(glowGeo, glowMat);
        glow.position.copy(mesh.position);
        glow.userData.parentMesh = mesh;
        _objs.push(glow);
        _mats.push(glowMat);
        scene.add(glow);
      }
    });

    return vertices;
  }

  function buildEdge(from, to, centerY) {
    var mid = new THREE.Vector3().addVectors(from, to).multiplyScalar(0.5);
    var len = from.distanceTo(to);

    var geo = new THREE.CylinderGeometry(0.03, 0.03, len, 6);
    var mat = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      emissive: 0xffd700,
      emissiveIntensity: 0.25,
      transparent: true,
      opacity: 0.55
    });
    var mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(5 + mid.x, centerY + mid.y - 5, mid.z);
    mesh.lookAt(5 + to.x, centerY + to.y - 5, to.z);
    mesh.rotateX(Math.PI / 2);
    mesh.userData = {
      baseIntensity: mat.emissiveIntensity,
      phase: Math.random() * Math.PI * 2
    };
    _objs.push(mesh);
    _mats.push(mat);
    scene.add(mesh);
  }

  // ── Propagation Wave Shader Plane ─────────────────────────────────────────
  function buildPropagationPlane() {
    var centerY = planckY();

    var geo = new THREE.PlaneGeometry(12, 12, 1, 1);
    var mat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uColor: { value: new THREE.Color(0xffd700) }
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
        '  vec2 center = vUv - 0.5;',
        '  float dist = length(center);',

        // High-frequency wave pattern
        '  float wave1 = sin(dist * 40.0 - uTime * 4.0) * 0.5 + 0.5;',
        '  float wave2 = sin(dist * 60.0 - uTime * 3.5) * 0.5 + 0.5;',
        '  float wave3 = sin(dist * 80.0 - uTime * 5.0) * 0.5 + 0.5;',
        '  float combined = wave1 * 0.4 + wave2 * 0.35 + wave3 * 0.25;',

        // Concentric rings from center (propagation fronts)
        '  float ring = sin(dist * 25.0 - uTime * 2.0);',
        '  ring = smoothstep(0.85, 1.0, abs(ring));',

        // Fade at edges
        '  float fade = 1.0 - smoothstep(0.3, 0.5, dist);',

        '  float alpha = (combined * 0.15 + ring * 0.25) * fade;',
        '  gl_FragColor = vec4(uColor * (0.6 + combined * 0.4), alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      depthWrite: false,
      side: THREE.DoubleSide
    });
    var mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(5, centerY, 0);
    mesh.rotation.x = -Math.PI / 2;
    mesh.userData.isPlane = true;
    _objs.push(mesh);
    _shaders.push(mat);
    scene.add(mesh);
  }

  // ── Emergence Sphere — continuous space hint ──────────────────────────────
  function buildEmergenceSphere() {
    var centerY = planckY();

    var geo = new THREE.SphereGeometry(9, 48, 48);
    var mat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uColor1: { value: new THREE.Color(0xffd700) },
        uColor2: { value: new THREE.Color(0x7c5cbf) }
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
        // Edge glow — space "fades in" from discrete geometry
        '  float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 3.5);',

        // Discrete noise pattern — the spinfoam lattice
        '  vec3 p = vPosition * 1.5;',
        '  float n1 = hash(floor(p * 4.0));',
        '  float n2 = hash(floor(p * 8.0));',
        '  float n = n1 * 0.6 + n2 * 0.4;',

        // Color: gold at discrete vertices, violet approaching emergence
        '  vec3 color = mix(uColor1, uColor2, fresnel * 0.6 + n * 0.2);',
        '  float alpha = fresnel * 0.35 + n * 0.08;',

        '  gl_FragColor = vec4(color, alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.BackSide,
      depthWrite: false
    });
    var mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(5, centerY, 0);
    mesh.userData.isEmergence = true;
    _objs.push(mesh);
    _shaders.push(mat);
    scene.add(mesh);
  }

  // ── Quantum Shimmer Particles ─────────────────────────────────────────────
  function buildQuantumShimmer() {
    var centerY = planckY();
    var count = 200;
    var positions = new Float32Array(count * 3);
    for (var i = 0; i < count; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 2 + Math.random() * 6;
      positions[i * 3]     = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
    }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var mat = new THREE.PointsMaterial({
      color: 0xffd700,
      size: 0.08,
      transparent: true,
      opacity: 0.7,
      sizeAttenuation: true
    });
    var shimmer = new THREE.Points(geo, mat);
    shimmer.position.set(5, centerY, 0);
    shimmer.userData.rotSpeed = 0.02;
    _objs.push(shimmer);
    _mats.push(mat);
    scene.add(shimmer);
  }

  // ── Topology Flip Event ────────────────────────────────────────────────────
  // Occasionally reconfigure 2 vertices — simulate topology change
  function triggerTopologyFlip(time) {
    if (_flipTimer > 0) return;
    _flipTimer = _flipInterval;

    // Find a non-central vertex to "flip"
    var flipCandidates = _objs.filter(function (o) {
      return o.userData && o.userData.pulseSpeed && !o.userData.isCentral;
    });
    if (flipCandidates.length === 0) return;

    var target = flipCandidates[Math.floor(Math.random() * flipCandidates.length)];

    // Bright flash
    var origIntensity = target.material.emissiveIntensity;
    target.material.emissiveIntensity = 3.0;
    setTimeout(function () {
      // Move slightly
      var offset = new THREE.Vector3(
        (Math.random() - 0.5) * 0.5,
        (Math.random() - 0.5) * 0.5,
        (Math.random() - 0.5) * 0.5
      );
      target.position.add(offset);
      target.material.emissiveIntensity = origIntensity * 0.3;
      setTimeout(function () {
        target.material.emissiveIntensity = origIntensity;
      }, 400);
    }, 150);
  }

  // ── Planck Label ────────────────────────────────────────────────────────────
  function buildLabel() {
    if (!window.ScaleEngine) return;
    var canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 96;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 512, 96);
    ctx.font = 'bold 32px DM Sans, sans-serif';
    ctx.fillStyle = '#ffd700';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Planck Scale — 10⁻³⁵ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(14, planckY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.PlanckScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();
      _flipTimer = _flipInterval;

      // Volumetric medium fog — space is not empty at Planck scale
      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.01 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.01);
      }

      buildEmergenceSphere();
      buildPropagationPlane();
      buildSpinfoamNetwork();
      buildQuantumShimmer();
      buildLabel();

      camera.position.set(5, planckY(), 18);
      camera.lookAt(5, planckY(), 0);
    },

    update: function (dt, time) {
      _flipTimer -= dt;
      if (_flipTimer <= 0) triggerTopologyFlip(time);

      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      _objs.forEach(function (o) {
        // Vertex pulsing
        if (o.userData && o.userData.baseIntensity !== undefined && o.userData.pulseSpeed) {
          var pulse = 0.6 + 0.4 * Math.sin(time * o.userData.pulseSpeed + o.userData.phase);
          o.material.emissiveIntensity = o.userData.baseIntensity * pulse;
        }
        // Shimmer particle rotation
        if (o.userData && o.userData.rotSpeed) {
          o.rotation.y += dt * o.userData.rotSpeed;
          o.rotation.x += dt * o.userData.rotSpeed * 0.3;
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
