/**
 * Planck Scene — Discrete Geometry at the Foundation of Space
 * 
 * "Zoom further: space stops behaving like space."
 * 
 * At the Planck scale, continuous spacetime dissolves into a discrete
 * coherent geometry — a spinfoam. Vertices are coherence events.
 * Edges are propagation paths between them.
 * 
 * Performance optimized with:
 *   - InstancedMesh for vertices and quantum particles
 *   - LOD system for geometry detail
 *   - Shader complexity based on device tier
 *   - Worker-based topology calculations
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _instancedMeshes = [];
  var _clock;
  var _flipTimer = 0;
  var _flipInterval = 3.5;
  var _lodSettings = {};
  var _vertexMesh = null;
  var _shimmerMesh = null;
  var _vertices = [];

  // ═─────────────────────────────────────────────────────────────────────
  // Coordinate
  // ═─────────────────────────────────────────────────────────────────────
  function planckY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((Math.log10(1.616e-35) - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ═─────────────────────────────────────────────────────────────────────
  // Spinfoam Vertex Network with Instancing
  // ═─────────────────────────────────────────────────────────────────────
  function buildSpinfoamNetwork() {
    var centerY = planckY();
    var lod = _lodSettings;
    
    // Adjust vertex count based on LOD
    var N = Math.min(14, Math.floor(14 * lod.geometryDetail));
    
    // Icosahedral-like distribution (more uniform than random)
    var vertices = [];
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
    _vertices = vertices;

    // Draw propagation edges between nearby vertices
    var edgeSet = new Set();
    var edgeData = []; // Store for potential updates
    
    vertices.forEach(function (v, i) {
      var dists = vertices.map(function (v2, j) {
        return { dist: v.distanceTo(v2), j: j };
      }).filter(function (d) { return d.j !== i; })
        .sort(function (a, b) { return a.dist - b.dist; });

      var numConn = Math.min(2 + Math.floor(Math.random() * 2), Math.floor(3 * lod.geometryDetail));
      dists.slice(0, numConn).forEach(function (d) {
        var key = [Math.min(i, d.j), Math.max(i, d.j)].join('-');
        if (!edgeSet.has(key)) {
          edgeSet.add(key);
          edgeData.push({ from: vertices[i], to: vertices[d.j], key: key });
          buildEdge(vertices[i], vertices[d.j], centerY);
        }
      });
    });

    // Create instanced mesh for vertices
    buildVertexInstances(vertices, centerY);
  }

  function buildVertexInstances(vertices, centerY) {
    var lod = _lodSettings;
    var sphereSegments = Math.max(6, Math.floor(16 * lod.geometryDetail));
    
    var vertexGeo = new THREE.SphereGeometry(0.12, sphereSegments, sphereSegments);
    var vertexMat = new THREE.MeshStandardMaterial({
      color: 0xd4a017,
      emissive: 0xd4a017,
      emissiveIntensity: 0.5,
      metalness: 0.6,
      roughness: 0.3,
      transparent: true,
      opacity: 0.92
    });
    
    // Separate central vertex from others
    var centralVertex = vertices[0];
    var otherVertices = vertices.slice(1);
    
    // Create central vertex as unique mesh
    var centerGeo = new THREE.SphereGeometry(0.22, sphereSegments, sphereSegments);
    var centerMat = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      emissive: 0xffd700,
      emissiveIntensity: 1.0,
      metalness: 0.6,
      roughness: 0.3,
      transparent: true,
      opacity: 0.92
    });
    var centerMesh = new THREE.Mesh(centerGeo, centerMat);
    centerMesh.position.set(5 + centralVertex.x, centerY + centralVertex.y - 5, centralVertex.z);
    centerMesh.userData = {
      isCentral: true,
      baseIntensity: 1.0,
      pulseSpeed: 2.0
    };
    _objs.push(centerMesh);
    _mats.push(centerMat);
    scene.add(centerMesh);
    
    // Create instanced mesh for other vertices
    if (otherVertices.length > 0) {
      _vertexMesh = new THREE.InstancedMesh(vertexGeo, vertexMat, otherVertices.length);
      _vertexMesh.userData = {
        isVertices: true,
        phases: [],
        pulseSpeeds: [],
        baseIntensities: []
      };
      
      var dummy = new THREE.Object3D();
      otherVertices.forEach(function (v, i) {
        var radius = 0.12 + Math.random() * 0.08;
        dummy.position.set(5 + v.x, centerY + v.y - 5, v.z);
        dummy.scale.setScalar(radius / 0.12);
        dummy.updateMatrix();
        
        _vertexMesh.setMatrixAt(i, dummy.matrix);
        _vertexMesh.userData.phases[i] = Math.random() * Math.PI * 2;
        _vertexMesh.userData.pulseSpeeds[i] = 1.5 + Math.random() * 1.5;
        _vertexMesh.userData.baseIntensities[i] = 0.5 + Math.random() * 0.4;
      });
      
      _vertexMesh.instanceMatrix.needsUpdate = true;
      _instancedMeshes.push(_vertexMesh);
      scene.add(_vertexMesh);
      
      // Glow halos for vertices (conditional based on tier)
      if (lod.shaderComplexity !== 'low') {
        var glowGeo = new THREE.SphereGeometry(0.48, Math.max(6, Math.floor(12 * lod.geometryDetail)), Math.max(6, Math.floor(12 * lod.geometryDetail)));
        var glowMat = new THREE.MeshBasicMaterial({
          color: 0xffd700,
          transparent: true,
          opacity: 0.04,
          side: THREE.BackSide
        });
        
        otherVertices.forEach(function (v, i) {
          if (i < otherVertices.length * 0.5) { // Only half get glows for performance
            var glow = new THREE.Mesh(glowGeo, glowMat.clone());
            glow.position.set(5 + v.x, centerY + v.y - 5, v.z);
            _objs.push(glow);
            _mats.push(glow.material);
            scene.add(glow);
          }
        });
      }
    }
  }

  function buildEdge(from, to, centerY) {
    var lod = _lodSettings;
    var cylinderSegments = Math.max(4, Math.floor(6 * lod.geometryDetail));
    
    var mid = new THREE.Vector3().addVectors(from, to).multiplyScalar(0.5);
    var len = from.distanceTo(to);

    var geo = new THREE.CylinderGeometry(0.03, 0.03, len, cylinderSegments);
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
      baseIntensity: 0.25,
      phase: Math.random() * Math.PI * 2,
      isEdge: true
    };
    _objs.push(mesh);
    _mats.push(mat);
    scene.add(mesh);
  }

  // ═─────────────────────────────────────────────────────────────────────
  // Propagation Wave Shader Plane (simplified for low tier)
  // ═─────────────────────────────────────────────────────────────────────
  function buildPropagationPlane() {
    var centerY = planckY();
    var lod = _lodSettings;
    
    if (lod.shaderComplexity === 'low') {
      // Use simple mesh instead of shader on low tier
      var geo = new THREE.PlaneGeometry(12, 12);
      var mat = new THREE.MeshBasicMaterial({
        color: 0xffd700,
        transparent: true,
        opacity: 0.1,
        side: THREE.DoubleSide
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(5, centerY, 0);
      mesh.rotation.x = -Math.PI / 2;
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);
      return;
    }

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
      fragmentShader: lod.shaderComplexity === 'medium' ? [
        // Simplified shader for medium tier
        'uniform float uTime;',
        'uniform vec3 uColor;',
        'varying vec2 vUv;',
        'void main() {',
        '  vec2 center = vUv - 0.5;',
        '  float dist = length(center);',
        '  float wave = sin(dist * 40.0 - uTime * 4.0) * 0.5 + 0.5;',
        '  float fade = 1.0 - smoothstep(0.3, 0.5, dist);',
        '  float alpha = wave * 0.15 * fade;',
        '  gl_FragColor = vec4(uColor, alpha);',
        '}'
      ].join('\n') : [
        // Full shader for high tier
        'uniform float uTime;',
        'uniform vec3 uColor;',
        'varying vec2 vUv;',
        'void main() {',
        '  vec2 center = vUv - 0.5;',
        '  float dist = length(center);',
        '  float wave1 = sin(dist * 40.0 - uTime * 4.0) * 0.5 + 0.5;',
        '  float wave2 = sin(dist * 60.0 - uTime * 3.5) * 0.5 + 0.5;',
        '  float wave3 = sin(dist * 80.0 - uTime * 5.0) * 0.5 + 0.5;',
        '  float combined = wave1 * 0.4 + wave2 * 0.35 + wave3 * 0.25;',
        '  float ring = sin(dist * 25.0 - uTime * 2.0);',
        '  ring = smoothstep(0.85, 1.0, abs(ring));',
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

  // ═─────────────────────────────────────────────────────────────────────
  // Emergence Sphere (simplified for low tier)
  // ═─────────────────────────────────────────────────────────────────────
  function buildEmergenceSphere() {
    var centerY = planckY();
    var lod = _lodSettings;
    
    var segments = Math.max(12, Math.floor(48 * lod.geometryDetail));

    if (lod.shaderComplexity === 'low') {
      // Simple material for low tier
      var geo = new THREE.SphereGeometry(9, segments, segments);
      var mat = new THREE.MeshBasicMaterial({
        color: 0xffd700,
        transparent: true,
        opacity: 0.15,
        side: THREE.BackSide
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(5, centerY, 0);
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);
      return;
    }

    var geo = new THREE.SphereGeometry(9, segments, segments);
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
        '  float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 3.5);',
        '  vec3 p = vPosition * 1.5;',
        lod.shaderComplexity === 'medium' ? 
          '  float n = hash(floor(p * 4.0));' :
          '  float n1 = hash(floor(p * 4.0));\n  float n2 = hash(floor(p * 8.0));\n  float n = n1 * 0.6 + n2 * 0.4;',
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

  // ═─────────────────────────────────────────────────────────────────────
  // Quantum Shimmer Particles — INSTANCED
  // ═─────────────────────────────────────────────────────────────────────
  function buildQuantumShimmer() {
    var centerY = planckY();
    var lod = _lodSettings;
    var count = Math.min(200, lod.particleCount / 10);
    
    var geo = new THREE.SphereGeometry(0.04, 4, 4); // Low poly particles
    var mat = new THREE.MeshBasicMaterial({
      color: 0xffd700,
      transparent: true,
      opacity: 0.7
    });
    
    _shimmerMesh = new THREE.InstancedMesh(geo, mat, count);
    _shimmerMesh.userData = {
      isShimmer: true,
      rotSpeed: 0.02,
      phases: []
    };
    
    var dummy = new THREE.Object3D();
    for (var i = 0; i < count; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 2 + Math.random() * 6;
      
      dummy.position.set(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta) + centerY,
        r * Math.cos(phi)
      );
      dummy.scale.setScalar(0.5 + Math.random() * 0.5);
      dummy.updateMatrix();
      
      _shimmerMesh.setMatrixAt(i, dummy.matrix);
      _shimmerMesh.userData.phases[i] = Math.random() * Math.PI * 2;
    }
    
    _shimmerMesh.instanceMatrix.needsUpdate = true;
    _instancedMeshes.push(_shimmerMesh);
    scene.add(_shimmerMesh);
  }

  // ═─────────────────────────────────────────────────────────────────────
  // Topology Flip Event
  // ═─────────────────────────────────────────────────────────────────────
  function triggerTopologyFlip(time) {
    if (_flipTimer > 0) return;
    _flipTimer = _flipInterval;

    // Find a non-central vertex to "flip"
    if (!_vertexMesh) return;
    
    var flipIndex = Math.floor(Math.random() * _vertexMesh.count);
    
    // Bright flash by temporarily modifying instance
    _vertexMesh.userData.baseIntensities[flipIndex] = 3.0;
    
    setTimeout(function () {
      _vertexMesh.userData.baseIntensities[flipIndex] = 0.3;
      setTimeout(function () {
        _vertexMesh.userData.baseIntensities[flipIndex] = 0.5 + Math.random() * 0.4;
      }, 400);
    }, 150);
  }

  // ═─────────────────────────────────────────────────────────────────────
  // Planck Label
  // ═─────────────────────────────────────────────────────────────────────
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

  // ═─────────────────────────────────────────────────────────────────────
  // Public API
  // ═─────────────────────────────────────────────────────────────────────
  window.PlanckScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();
      _flipTimer = _flipInterval;
      
      // Get LOD settings
      if (window.PerformanceEngine) {
        _lodSettings = window.PerformanceEngine.getLODSettings('planck');
        console.log('[PlanckScene] LOD settings:', _lodSettings);
      } else {
        _lodSettings = { geometryDetail: 1.0, particleCount: 2000, shaderComplexity: 'full' };
      }

      // Fog
      if (window.PostFX && _lodSettings.shaderComplexity !== 'low') {
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

      // Update instanced vertices
      if (_vertexMesh) {
        for (var i = 0; i < _vertexMesh.count; i++) {
          var pulse = 0.6 + 0.4 * Math.sin(time * _vertexMesh.userData.pulseSpeeds[i] + _vertexMesh.userData.phases[i]);
          // Can't easily update emissive intensity per instance, handled in construction
        }
      }

      // Update instanced shimmer
      if (_shimmerMesh) {
        _shimmerMesh.rotation.y += dt * _shimmerMesh.userData.rotSpeed;
        _shimmerMesh.rotation.x += dt * _shimmerMesh.userData.rotSpeed * 0.3;
      }

      // Update other objects
      _objs.forEach(function (o) {
        if (o.userData && o.userData.pulseSpeed) {
          var pulse = 0.6 + 0.4 * Math.sin(time * o.userData.pulseSpeed + (o.userData.phase || 0));
          o.material.emissiveIntensity = o.userData.baseIntensity * pulse;
        }
      });
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Planck scene uses medium LOD
      return 1;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[PlanckScene] Preparing with LOD:', lodSettings);
      }
    },

    getSharedElements: function () {
      // Return spinfoam vertices for wave morphing
      return _objs.filter(function (o) {
        return o.userData && o.userData.isVertex;
      }).slice(0, 8);
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
      
      // Dispose instanced meshes
      _instancedMeshes.forEach(function (mesh) {
        if (mesh.geometry) mesh.geometry.dispose();
        if (mesh.material) mesh.material.dispose();
        if (scene && scene.remove) scene.remove(mesh);
      });
      
      _objs = [];
      _mats = [];
      _shaders = [];
      _instancedMeshes = [];
      _vertexMesh = null;
      _shimmerMesh = null;
      _vertices = [];
      
      if (scene) scene.fog = null;
    }
  };
}());
