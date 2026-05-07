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
 * Performance optimized with:
 *   - InstancedMesh for stars and galaxy clusters
 *   - LOD system for geometry detail based on device tier
 *   - Frustum culling integration
 *   - Proper memory disposal
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _instancedMeshes = [];
  var _clock;
  var _lodSettings = {};
  var _starFieldMesh = null;
  var _galaxyClustersMesh = null;
  var _glowMeshes = [];

  // ═─────────────────────────────────────────────────────────────────────
  // Coordinate
  // ═─────────────────────────────────────────────────────────────────────
  function cosmicY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((26 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ═─────────────────────────────────────────────────────────────────────
  // Performance-Optimized Filament Network
  // ═─────────────────────────────────────────────────────────────────────
  function buildFilamentNetwork() {
    var centerY = cosmicY();
    var lod = _lodSettings;

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

    // Filament geometry detail based on LOD
    var cylinderSegments = Math.max(6, Math.floor(8 * lod.geometryDetail));
    
    // Draw filaments as glowing cylinders (not instanced - each is unique)
    connections.forEach(function (conn) {
      var from = nodePositions[conn[0]];
      var to = nodePositions[conn[1]];
      var fv = new THREE.Vector3(from[0], from[1], from[2]);
      var tv = new THREE.Vector3(to[0], to[1], to[2]);
      var mid = new THREE.Vector3().addVectors(fv, tv).multiplyScalar(0.5);
      var len = fv.distanceTo(tv);

      var geo = new THREE.CylinderGeometry(0.12, 0.12, len, cylinderSegments);
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
      mesh.userData.isFilament = true;
      mesh.userData.baseIntensity = 0.22;
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);

      // Add smaller side filaments branching off
      addBranchFilaments(mesh.position, tv.clone().sub(fv), centerY);
    });

    // Create galaxy clusters using instancing for performance
    buildGalaxyClusters(nodePositions, centerY);
  }

  function buildGalaxyClusters(nodePositions, centerY) {
    var lod = _lodSettings;
    var sphereSegments = Math.max(8, Math.floor(16 * lod.geometryDetail));
    
    // Create instanced mesh for galaxy clusters
    var clusterGeo = new THREE.SphereGeometry(0.35, sphereSegments, sphereSegments);
    var clusterMat = new THREE.MeshStandardMaterial({
      color: 0xd63031,
      emissive: 0xd63031,
      emissiveIntensity: 0.6,
      metalness: 0.3,
      roughness: 0.4,
      transparent: true,
      opacity: 0.85
    });
    
    // Count non-center clusters
    var clusterCount = nodePositions.length - 1;
    _galaxyClustersMesh = new THREE.InstancedMesh(clusterGeo, clusterMat, clusterCount);
    _galaxyClustersMesh.userData.isGalaxyClusters = true;
    _galaxyClustersMesh.userData.phases = [];
    _galaxyClustersMesh.userData.orbitSpeeds = [];
    _galaxyClustersMesh.userData.orbitRadii = [];
    _galaxyClustersMesh.userData.baseIntensities = [];
    
    var dummy = new THREE.Object3D();
    var instanceIdx = 0;
    
    nodePositions.forEach(function (p, i) {
      var isCenter = i === 0;
      if (isCenter) {
        // Center cluster is unique, not instanced
        var centerGeo = new THREE.SphereGeometry(0.6, sphereSegments, sphereSegments);
        var centerMat = new THREE.MeshStandardMaterial({
          color: 0xffdd55,
          emissive: 0xffdd55,
          emissiveIntensity: 0.9,
          metalness: 0.3,
          roughness: 0.4,
          transparent: true,
          opacity: 0.95
        });
        var centerMesh = new THREE.Mesh(centerGeo, centerMat);
        centerMesh.position.set(5 + p[0], centerY + p[1] - 5, p[2]);
        centerMesh.userData = {
          isCenter: true,
          baseIntensity: 0.9
        };
        _objs.push(centerMesh);
        _mats.push(centerMat);
        scene.add(centerMesh);
        return;
      }
      
      // Set up instanced cluster
      dummy.position.set(5 + p[0], centerY + p[1] - 5, p[2]);
      var radius = 0.35 + Math.random() * 0.2;
      dummy.scale.setScalar(radius / 0.35);
      dummy.updateMatrix();
      
      _galaxyClustersMesh.setMatrixAt(instanceIdx, dummy.matrix);
      _galaxyClustersMesh.userData.phases[instanceIdx] = Math.random() * Math.PI * 2;
      _galaxyClustersMesh.userData.orbitSpeeds[instanceIdx] = (Math.random() - 0.5) * 0.3;
      _galaxyClustersMesh.userData.orbitRadii[instanceIdx] = 0.3 + Math.random() * 0.4;
      _galaxyClustersMesh.userData.baseIntensities[instanceIdx] = 0.6;
      
      instanceIdx++;
      
      // Glow sprite around each cluster (only for high/medium tier)
      if (lod.shaderComplexity !== 'low' && instanceIdx <= lod.particleCount / 100) {
        var glowRadius = radius * 2.5;
        var glowSegments = Math.max(8, Math.floor(12 * lod.geometryDetail));
        var glowGeo = new THREE.SphereGeometry(glowRadius, glowSegments, glowSegments);
        var glowMat = new THREE.MeshBasicMaterial({
          color: 0xd63031,
          transparent: true,
          opacity: 0.06,
          side: THREE.BackSide
        });
        var glow = new THREE.Mesh(glowGeo, glowMat);
        glow.position.copy(dummy.position);
        _glowMeshes.push(glow);
        _objs.push(glow);
        _mats.push(glowMat);
        scene.add(glow);
      }
    });
    
    _galaxyClustersMesh.instanceMatrix.needsUpdate = true;
    _galaxyClustersMesh.count = instanceIdx;
    _instancedMeshes.push(_galaxyClustersMesh);
    scene.add(_galaxyClustersMesh);
  }

  // Branch filaments from parent filament midpoint
  function addBranchFilaments(from, direction, centerY) {
    var lod = _lodSettings;
    var numBranches = 1 + Math.floor(Math.random() * 2 * lod.geometryDetail);
    var cylinderSegments = Math.max(5, Math.floor(6 * lod.geometryDetail));
    
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

      var geo = new THREE.CylinderGeometry(0.04, 0.04, len, cylinderSegments);
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
      mesh.userData.isFilament = true;
      mesh.userData.baseIntensity = 0.12;
      _objs.push(mesh);
      _mats.push(mat);
      scene.add(mesh);
    }
  }

  // ═─────────────────────────────────────────────────────────────────────
  // Void Sphere — outer boundary
  // ═─────────────────────────────────────────────────────────────────────
  function buildVoidSphere() {
    var centerY = cosmicY();
    var lod = _lodSettings;

    // Multiple nested void shells with LOD-adjusted segments
    var shells = lod.shaderComplexity === 'low' ? [16] : lod.shaderComplexity === 'medium' ? [16, 20] : [24, 20, 16];
    
    shells.forEach(function (r, i) {
      var opacity = 0.04 + i * 0.02;
      var segments = Math.max(16, Math.floor(48 * lod.geometryDetail / (i + 1)));
      var geo = new THREE.SphereGeometry(r, segments, segments);
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
    var ringSegments = Math.max(16, Math.floor(64 * lod.geometryDetail));
    var ringGeo = new THREE.TorusGeometry(18, 0.15, 8, ringSegments);
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

  // ═─────────────────────────────────────────────────────────────────────
  // CMB Haze — volumetric glow (simplified for low tier)
  // ═─────────────────────────────────────────────────────────────────────
  function buildCMBHaze() {
    var centerY = cosmicY();
    var lod = _lodSettings;
    
    if (lod.shaderComplexity === 'low') {
      // Skip shader-based CMB on low tier
      return;
    }

    var segments = Math.max(12, Math.floor(32 * lod.geometryDetail));
    var geo = new THREE.SphereGeometry(14, segments, segments);
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
        '',
        'float hash(vec3 p) {',
        '  return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453);',
        '}',
        '',
        'void main() {',
        '  float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.8);',
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

  // ═─────────────────────────────────────────────────────────────────────
  // Background Star Field — INSTANCED for performance
  // ═─────────────────────────────────────────────────────────────────────
  function buildStarField() {
    var lod = _lodSettings;
    var count = Math.min(800, lod.particleCount);
    
    // Use InstancedMesh for stars instead of Points
    var starGeo = new THREE.IcosahedronGeometry(0.08, 1);
    var starMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.6
    });
    
    _starFieldMesh = new THREE.InstancedMesh(starGeo, starMat, count);
    _starFieldMesh.userData = {
      isStarField: true,
      rotSpeed: 0.003
    };
    
    var dummy = new THREE.Object3D();
    var centerY = cosmicY();
    
    for (var i = 0; i < count; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 20 + Math.random() * 12;
      
      dummy.position.set(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta) + centerY,
        r * Math.cos(phi)
      );
      dummy.scale.setScalar(0.5 + Math.random() * 0.5);
      dummy.updateMatrix();
      
      _starFieldMesh.setMatrixAt(i, dummy.matrix);
    }
    
    _starFieldMesh.instanceMatrix.needsUpdate = true;
    _instancedMeshes.push(_starFieldMesh);
    scene.add(_starFieldMesh);
  }

  // ═─────────────────────────────────────────────────────────────────────
  // Cosmic Scale Label
  // ═─────────────────────────────────────────────────────────────────────
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

  // ═─────────────────────────────────────────────────────────────────────
  // Public API
  // ═─────────────────────────────────────────────────────────────────────
  window.CosmicScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();
      
      // Get LOD settings from PerformanceEngine
      if (window.PerformanceEngine) {
        _lodSettings = window.PerformanceEngine.getLODSettings('cosmic');
        console.log('[CosmicScene] LOD settings:', _lodSettings);
      } else {
        _lodSettings = { geometryDetail: 1.0, particleCount: 800, shaderComplexity: 'full' };
      }

      // Volumetric medium fog — space is not empty
      if (window.PostFX && _lodSettings.shaderComplexity !== 'low') {
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

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, cosmicY(), 28),
        target: new THREE.Vector3(5, cosmicY(), 0),
        fov: 48
      };
    },

    getSharedElements: function () {
      // Return filaments and nodes for wave morphing
      return _objs.filter(function (o) {
        return o.geometry && (
          o.geometry.type === 'CylinderGeometry' ||
          o.geometry.type === 'SphereGeometry'
        );
      }).slice(0, 8);
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Cosmic scene uses low LOD due to many particles
      return 2;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[CosmicScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      // Shader uniforms
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      // Update instanced galaxy clusters
      if (_galaxyClustersMesh) {
        var dummy = new THREE.Object3D();
        var matrix = new THREE.Matrix4();
        var position = new THREE.Vector3();
        var scale = new THREE.Vector3();
        var quaternion = new THREE.Quaternion();
        
        for (var i = 0; i < _galaxyClustersMesh.count; i++) {
          _galaxyClustersMesh.getMatrixAt(i, matrix);
          position.setFromMatrixPosition(matrix);
          scale.setFromMatrixScale(matrix);
          matrix.decompose(position, quaternion, scale);
          
          var pulse = 0.55 + 0.35 * Math.sin(time * 1.2 + _galaxyClustersMesh.userData.phases[i]);
          var intensity = _galaxyClustersMesh.userData.baseIntensities[i] * pulse;
          
          // Update orbit
          if (_galaxyClustersMesh.userData.orbitSpeeds[i]) {
            var angle = time * _galaxyClustersMesh.userData.orbitSpeeds[i] + _galaxyClustersMesh.userData.phases[i];
            position.x += Math.cos(angle) * 0.001;
            position.z += Math.sin(angle) * 0.001;
          }
          
          dummy.position.copy(position);
          dummy.scale.copy(scale);
          dummy.quaternion.copy(quaternion);
          dummy.updateMatrix();
          _galaxyClustersMesh.setMatrixAt(i, dummy.matrix);
        }
        _galaxyClustersMesh.instanceMatrix.needsUpdate = true;
      }

      // Update other objects
      _objs.forEach(function (o) {
        // Slow star field rotation
        if (o.userData && o.userData.isStarField) {
          o.rotation.y += dt * o.userData.rotSpeed;
        }
        // Filament shimmer
        if (o.userData && o.userData.isFilament && o.material) {
          var lp = o.position.x * 0.1;
          o.material.emissiveIntensity = o.userData.baseIntensity + 0.08 * Math.sin(time * 0.4 + lp);
        }
      });
      
      // Update star field rotation
      if (_starFieldMesh) {
        _starFieldMesh.rotation.y += dt * _starFieldMesh.userData.rotSpeed;
      }
    },

    deactivate: function () {
      // Dispose all regular objects
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
      
      // Clear arrays
      _objs = [];
      _mats = [];
      _shaders = [];
      _instancedMeshes = [];
      _starFieldMesh = null;
      _galaxyClustersMesh = null;
      _glowMeshes = [];
      
      // Clear fog
      if (scene) {
        scene.fog = null;
      }
    }
  };
}());
