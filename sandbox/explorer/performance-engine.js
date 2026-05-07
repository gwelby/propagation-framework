/**
 * PerformanceEngine — World-Class Performance Optimization for PF Explorer
 * 
 * Target: 60fps on iPhone 12 (3yo), 45fps on iPhone X (5yo)
 * Memory: <200MB, Initial Load: <3s, No frame drops during transitions
 * 
 * Features:
 *   - Device-based quality tiers (high/medium/low)
 *   - Level-of-Detail (LOD) system with distance/scale-based switching
 *   - InstancedMesh for repeated objects (stars, cells, atoms, etc.)
 *   - Frustum culling with bounding sphere caching
 *   - Web Worker pool for physics and pathfinding
 *   - Memory management with object pooling and proper disposal
 *   - Texture atlasing to reduce draw calls
 *   - Shader LOD (simpler shaders on mobile)
 *   - Adaptive frame rate with time scaling
 */
(function () {
  'use strict';

  // ═══════════════════════════════════════════════════════════════════════
  // DEVICE DETECTION & QUALITY TIER
  // ═══════════════════════════════════════════════════════════════════════

  const DeviceProfile = {
    tier: 'high', // 'high' | 'medium' | 'low' | 'minimal'
    maxFPS: 60,
    targetFPS: 60,
    maxParticles: 10000,
    maxInstances: 10000,
    enableShadows: true,
    enableBloom: true,
    enablePostFX: true,
    shaderQuality: 'full', // 'full' | 'medium' | 'low'
    pixelRatio: 2,
    maxDrawCalls: 100,
    geometryDetail: 1.0, // multiplier for geometry segments
    cullDistance: 1000,
    lodDistance: [10, 30, 100], // distances for LOD switching
    workerCount: 4,
    touch: false,
    memoryLimit: 200 * 1024 * 1024, // 200MB
    cpuCores: 4,
    gpuTier: 'high',
    isMobile: false,
    isLowPower: false
  };

  function detectDevice() {
    const ua = navigator.userAgent;
    const mobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua);
    const ios = /iPhone|iPad|iPod/i.test(ua);
    const android = /Android/i.test(ua);
    const touch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    // CPU cores detection
    const cores = navigator.hardwareConcurrency || 4;
    
    // GPU detection via canvas
    let gpuTier = 'medium';
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (gl) {
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) {
          const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
          const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
          
          // Detect low-power GPUs
          const lowPowerGPUs = /Mali-4|Mali-3|Adreno 3|Adreno 4|PowerVR|Intel.*HD.*Graphics.*4/i;
          const highPowerGPUs = /Apple.*M[12]|Apple.*A1[456789]|Adreno [6789]|Mali-G|Mali-T8/i;
          
          if (lowPowerGPUs.test(renderer)) gpuTier = 'low';
          else if (highPowerGPUs.test(renderer)) gpuTier = 'high';
          else gpuTier = 'medium';
        }
        
        // Test shader complexity support
        const maxVertexUniforms = gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS);
        if (maxVertexUniforms < 128) gpuTier = 'low';
        else if (maxVertexUniforms > 256) gpuTier = Math.max(gpuTier === 'high' ? 'high' : 'medium', gpuTier);
      }
    } catch (e) {
      gpuTier = 'low';
    }

    // iPhone model detection
    let iphoneModel = null;
    if (ios) {
      const match = ua.match(/iPhone.*OS (\d+)[_\d]* like/);
      const version = match ? parseInt(match[1]) : 0;
      
      // Rough model inference from screen size + pixel ratio
      const screenPixels = window.screen.width * window.screen.height * window.devicePixelRatio;
      if (screenPixels > 2000000) iphoneModel = 'modern'; // iPhone X+
      else iphoneModel = 'legacy'; // iPhone 8 and earlier
    }

    // Determine quality tier
    let tier = 'high';
    if (mobile) {
      DeviceProfile.isMobile = true;
      if (ios && iphoneModel === 'legacy') tier = 'low';
      else if (gpuTier === 'low') tier = 'low';
      else if (gpuTier === 'medium') tier = 'medium';
      else if (cores <= 4) tier = 'medium';
      
      // iPhone X and earlier get low tier
      if (ua.includes('iPhone')) {
        const match = ua.match(/iPhone\d+,\d+/);
        if (match) {
          const model = parseInt(match[0].replace('iPhone', '').split(',')[0]);
          if (model <= 10) tier = 'low'; // iPhone X or earlier
        }
      }
    }

    // Apply tier settings
    DeviceProfile.tier = tier;
    DeviceProfile.touch = touch;
    DeviceProfile.cpuCores = cores;
    DeviceProfile.gpuTier = gpuTier;
    DeviceProfile.isLowPower = tier === 'low';

    switch (tier) {
      case 'high':
        DeviceProfile.maxFPS = 60;
        DeviceProfile.targetFPS = 60;
        DeviceProfile.maxParticles = 10000;
        DeviceProfile.maxInstances = 10000;
        DeviceProfile.enableShadows = true;
        DeviceProfile.enableBloom = true;
        DeviceProfile.shaderQuality = 'full';
        DeviceProfile.pixelRatio = Math.min(window.devicePixelRatio, 2);
        DeviceProfile.geometryDetail = 1.0;
        DeviceProfile.workerCount = Math.min(cores, 4);
        DeviceProfile.lodDistance = [15, 40, 120];
        break;
        
      case 'medium':
        DeviceProfile.maxFPS = 60;
        DeviceProfile.targetFPS = 45;
        DeviceProfile.maxParticles = 5000;
        DeviceProfile.maxInstances = 5000;
        DeviceProfile.enableShadows = false;
        DeviceProfile.enableBloom = false;
        DeviceProfile.shaderQuality = 'medium';
        DeviceProfile.pixelRatio = Math.min(window.devicePixelRatio, 1.5);
        DeviceProfile.geometryDetail = 0.6;
        DeviceProfile.workerCount = Math.min(cores, 2);
        DeviceProfile.lodDistance = [10, 25, 60];
        break;
        
      case 'low':
        DeviceProfile.maxFPS = 30;
        DeviceProfile.targetFPS = 30;
        DeviceProfile.maxParticles = 2000;
        DeviceProfile.maxInstances = 2000;
        DeviceProfile.enableShadows = false;
        DeviceProfile.enableBloom = false;
        DeviceProfile.shaderQuality = 'low';
        DeviceProfile.pixelRatio = 1;
        DeviceProfile.geometryDetail = 0.4;
        DeviceProfile.workerCount = 1;
        DeviceProfile.lodDistance = [8, 20, 40];
        break;
        
      case 'minimal':
        DeviceProfile.maxFPS = 30;
        DeviceProfile.targetFPS = 24;
        DeviceProfile.maxParticles = 500;
        DeviceProfile.maxInstances = 1000;
        DeviceProfile.enableShadows = false;
        DeviceProfile.enableBloom = false;
        DeviceProfile.shaderQuality = 'low';
        DeviceProfile.pixelRatio = 1;
        DeviceProfile.geometryDetail = 0.25;
        DeviceProfile.workerCount = 1;
        DeviceProfile.lodDistance = [5, 15, 30];
        break;
    }

    // Log detection results
    console.log('[PerformanceEngine] Device detected:', {
      tier: tier,
      mobile: mobile,
      gpu: gpuTier,
      cores: cores,
      pixelRatio: DeviceProfile.pixelRatio
    });

    return DeviceProfile;
  }

  // ═══════════════════════════════════════════════════════════════════════
  // LEVEL-OF-DETAIL (LOD) SYSTEM
  // ═══════════════════════════════════════════════════════════════════════

  const LODSystem = {
    levels: {
      cosmic:    { geometryDetail: 0.1,  particleCount: 500,   shaderComplexity: 'low'    },
      galactic:  { geometryDetail: 0.15, particleCount: 800,   shaderComplexity: 'low'    },
      stellar:   { geometryDetail: 0.2,  particleCount: 1000,  shaderComplexity: 'medium' },
      planetary: { geometryDetail: 0.25, particleCount: 1200,  shaderComplexity: 'medium' },
      human:     { geometryDetail: 0.3,  particleCount: 1500,  shaderComplexity: 'medium' },
      neural:    { geometryDetail: 0.35, particleCount: 1000,  shaderComplexity: 'medium' },
      cellular:  { geometryDetail: 0.4,  particleCount: 800,   shaderComplexity: 'medium' },
      virus:     { geometryDetail: 0.5,  particleCount: 600,   shaderComplexity: 'medium' },
      molecular: { geometryDetail: 0.6,  particleCount: 500,   shaderComplexity: 'full'   },
      atomic:    { geometryDetail: 0.8,  particleCount: 400,   shaderComplexity: 'full'   },
      nuclear:   { geometryDetail: 0.9,  particleCount: 300,   shaderComplexity: 'full'   },
      proton:    { geometryDetail: 1.0,  particleCount: 200,   shaderComplexity: 'full'   },
      matter:    { geometryDetail: 1.0,  particleCount: 200,   shaderComplexity: 'full'   },
      gut:       { geometryDetail: 0.8,  particleCount: 300,   shaderComplexity: 'medium' },
      planck:    { geometryDetail: 0.5,  particleCount: 200,   shaderComplexity: 'low'    }
    },

    // Get LOD settings for a scale, adjusted by device tier
    getSettings(scaleId) {
      const base = this.levels[scaleId] || { geometryDetail: 0.5, particleCount: 500, shaderComplexity: 'medium' };
      const tier = DeviceProfile.tier;
      
      const multipliers = {
        high: { geometry: 1.0, particles: 1.0 },
        medium: { geometry: 0.8, particles: 0.6 },
        low: { geometry: 0.5, particles: 0.3 },
        minimal: { geometry: 0.3, particles: 0.15 }
      };
      
      const mult = multipliers[tier] || multipliers.medium;
      
      return {
        geometryDetail: Math.min(base.geometryDetail * DeviceProfile.geometryDetail * mult.geometry, 1.0),
        particleCount: Math.floor(base.particleCount * mult.particles),
        shaderComplexity: tier === 'low' ? 'low' : base.shaderComplexity,
        maxInstances: DeviceProfile.maxInstances
      };
    },

    // Calculate geometry segments based on detail level
    getSegments(baseSegments, detail) {
      return Math.max(3, Math.floor(baseSegments * detail));
    },

    // Get sphere geometry with LOD
    getSphereGeometry(radius, segments, detail) {
      const adjusted = this.getSegments(segments, detail);
      return new THREE.SphereGeometry(radius, adjusted, adjusted);
    },

    // Get cylinder geometry with LOD
    getCylinderGeometry(radiusTop, radiusBottom, height, segments, detail) {
      const adjusted = Math.max(3, Math.floor(segments * detail));
      return new THREE.CylinderGeometry(radiusTop, radiusBottom, height, adjusted);
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // INSTANCED MESH SYSTEM
  // ═══════════════════════════════════════════════════════════════════════

  const InstancingSystem = {
    pools: {},
    
    // Configuration for instancing by object type
    config: {
      stars: { use: true, maxCount: 10000, geometry: 'icosahedron', size: 1 },
      cells: { use: true, maxCount: 5000, geometry: 'sphere', size: 1 },
      atoms: { use: true, maxCount: 2000, geometry: 'sphere', size: 0.5 },
      particles: { use: true, maxCount: 8000, geometry: 'plane', size: 0.1 },
      quarks: { use: true, maxCount: 500, geometry: 'sphere', size: 0.35 },
      vesicles: { use: true, maxCount: 1000, geometry: 'sphere', size: 0.25 },
      mitochondria: { use: true, maxCount: 200, geometry: 'capsule', size: 1 }
    },

    // Create or get an instanced mesh pool
    getPool(type, material, maxCount = null) {
      const config = this.config[type];
      if (!config) return null;
      
      const count = maxCount || Math.min(config.maxCount, DeviceProfile.maxInstances);
      const poolKey = `${type}_${material.uuid || material.id || Math.random()}`;
      
      if (this.pools[poolKey]) {
        return this.pools[poolKey];
      }

      // Create geometry based on type
      let geometry;
      const detail = DeviceProfile.geometryDetail;
      
      switch (config.geometry) {
        case 'icosahedron':
          geometry = new THREE.IcosahedronGeometry(config.size, Math.floor(detail));
          break;
        case 'sphere':
          const segments = LODSystem.getSegments(8, detail);
          geometry = new THREE.SphereGeometry(config.size, segments, segments);
          break;
        case 'capsule':
          geometry = new THREE.CapsuleGeometry(config.size * 0.35, config.size * 1.2, 
            Math.max(4, Math.floor(8 * detail)), 
            Math.max(8, Math.floor(16 * detail)));
          break;
        case 'plane':
          geometry = new THREE.PlaneGeometry(config.size, config.size);
          break;
        default:
          geometry = new THREE.SphereGeometry(config.size, 8, 8);
      }

      const instancedMesh = new THREE.InstancedMesh(geometry, material, count);
      instancedMesh.count = 0; // Start with 0 visible
      instancedMesh.userData = { 
        maxCount: count,
        currentIndex: 0,
        positions: [],
        matrices: []
      };

      this.pools[poolKey] = instancedMesh;
      return instancedMesh;
    },

    // Add an instance to the pool
    addInstance(pool, position, scale = 1, rotation = null) {
      if (!pool || pool.count >= pool.userData.maxCount) return false;
      
      const index = pool.count;
      const matrix = new THREE.Matrix4();
      const dummy = new THREE.Object3D();
      
      dummy.position.copy(position);
      dummy.scale.setScalar(scale);
      if (rotation) {
        dummy.rotation.copy(rotation);
      }
      dummy.updateMatrix();
      
      pool.setMatrixAt(index, dummy.matrix);
      pool.count++;
      
      // Store for updates
      pool.userData.positions[index] = position.clone();
      pool.userData.matrices[index] = dummy.matrix.clone();
      
      pool.instanceMatrix.needsUpdate = true;
      return true;
    },

    // Update instance at index
    updateInstance(pool, index, position, scale = 1, rotation = null) {
      if (!pool || index >= pool.count) return false;
      
      const dummy = new THREE.Object3D();
      dummy.position.copy(position);
      dummy.scale.setScalar(scale);
      if (rotation) dummy.rotation.copy(rotation);
      dummy.updateMatrix();
      
      pool.setMatrixAt(index, dummy.matrix);
      pool.instanceMatrix.needsUpdate = true;
      return true;
    },

    // Clear all instances
    clearPool(pool) {
      if (!pool) return;
      pool.count = 0;
      pool.userData.currentIndex = 0;
      pool.userData.positions = [];
      pool.userData.matrices = [];
    },

    // Dispose a pool
    disposePool(pool) {
      if (!pool) return;
      if (pool.geometry) pool.geometry.dispose();
      this.clearPool(pool);
    },

    // Clean up all pools
    disposeAll() {
      Object.values(this.pools).forEach(pool => this.disposePool(pool));
      this.pools = {};
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // FRUSTUM CULLING & OCCLUSION SYSTEM
  // ═══════════════════════════════════════════════════════════════════════

  const CullingSystem = {
    frustum: new THREE.Frustum(),
    projScreenMatrix: new THREE.Matrix4(),
    boundingSphere: new THREE.Sphere(),
    culledCount: 0,
    totalCount: 0,
    
    enabled: true,
    cacheMatrices: true,
    
    // Update frustum from camera
    update(camera) {
      if (!this.enabled || !camera) return;
      
      camera.updateMatrixWorld();
      this.projScreenMatrix.multiplyMatrices(
        camera.projectionMatrix,
        camera.matrixWorldInverse
      );
      this.frustum.setFromProjectionMatrix(this.projScreenMatrix);
    },

    // Check if object is in frustum
    isVisible(object) {
      if (!this.enabled) return true;
      
      this.totalCount++;
      
      // Get world position
      const position = new THREE.Vector3();
      object.getWorldPosition(position);
      
      // Calculate bounding sphere
      let radius = object.userData.boundingRadius;
      if (!radius && object.geometry) {
        if (!object.geometry.boundingSphere) {
          object.geometry.computeBoundingSphere();
        }
        radius = object.geometry.boundingSphere.radius;
        // Account for scale
        const scale = object.scale.length();
        radius *= scale;
        object.userData.boundingRadius = radius;
      }
      radius = radius || 1;
      
      this.boundingSphere.set(position, radius);
      
      const visible = this.frustum.intersectsSphere(this.boundingSphere);
      if (!visible) this.culledCount++;
      
      return visible;
    },

    // Batch visibility check for instanced meshes
    updateInstancedVisibility(mesh, camera) {
      if (!this.enabled || !mesh || !mesh.isInstancedMesh) return;
      
      this.update(camera);
      
      const dummy = new THREE.Object3D();
      const matrix = new THREE.Matrix4();
      const position = new THREE.Vector3();
      
      let visibleCount = 0;
      
      for (let i = 0; i < mesh.count; i++) {
        mesh.getMatrixAt(i, matrix);
        position.setFromMatrixPosition(matrix);
        
        // Quick distance check first
        const distSq = position.distanceToSquared(camera.position);
        if (distSq > DeviceProfile.cullDistance * DeviceProfile.cullDistance) {
          continue; // Too far, skip
        }
        
        this.boundingSphere.set(position, 1); // Assume unit radius
        if (this.frustum.intersectsSphere(this.boundingSphere)) {
          visibleCount++;
        }
      }
      
      return visibleCount;
    },

    // Get culling stats
    getStats() {
      const stats = {
        culled: this.culledCount,
        total: this.totalCount,
        ratio: this.totalCount > 0 ? (this.culledCount / this.totalCount * 100).toFixed(1) + '%' : '0%'
      };
      // Reset counters
      this.culledCount = 0;
      this.totalCount = 0;
      return stats;
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // WEB WORKER SYSTEM
  // ═══════════════════════════════════════════════════════════════════════

  const WorkerSystem = {
    workers: [],
    taskQueue: [],
    taskId: 0,
    pendingTasks: new Map(),

    async init() {
      if (DeviceProfile.workerCount <= 0) return;
      
      // Workers will be created on demand for specific tasks
      console.log('[PerformanceEngine] Worker system initialized, max workers:', DeviceProfile.workerCount);
    },

    // Execute task in worker
    async execute(workerScript, data, timeout = 5000) {
      return new Promise((resolve, reject) => {
        if (!window.Worker) {
          // Fallback to main thread
          resolve(this.fallbackExecute(data));
          return;
        }

        const taskId = ++this.taskId;
        const worker = new Worker(workerScript);
        
        const timeoutId = setTimeout(() => {
          worker.terminate();
          this.pendingTasks.delete(taskId);
          reject(new Error('Worker timeout'));
        }, timeout);

        worker.onmessage = (e) => {
          clearTimeout(timeoutId);
          worker.terminate();
          this.pendingTasks.delete(taskId);
          resolve(e.data);
        };

        worker.onerror = (err) => {
          clearTimeout(timeoutId);
          worker.terminate();
          this.pendingTasks.delete(taskId);
          reject(err);
        };

        this.pendingTasks.set(taskId, { worker, timeoutId });
        worker.postMessage({ taskId, data });
      });
    },

    // Fallback execution on main thread
    fallbackExecute(data) {
      // Simple fallback for physics calculations
      if (data.type === 'physics') {
        // Basic physics update
        return { result: data.positions.map(p => ({ x: p.x, y: p.y, z: p.z })) };
      }
      if (data.type === 'pathfinding') {
        return { path: [] };
      }
      return data;
    },

    // Batch process particles in worker
    async batchProcessParticles(particles, dt, type = 'update') {
      if (particles.length < 100 || DeviceProfile.workerCount <= 1) {
        // Process on main thread for small batches
        return particles.map(p => ({
          x: p.x + (p.vx || 0) * dt,
          y: p.y + (p.vy || 0) * dt,
          z: p.z + (p.vz || 0) * dt
        }));
      }

      try {
        return await this.execute('workers/physics-worker.js', {
          type: 'particles',
          particles: particles,
          dt: dt
        });
      } catch (e) {
        // Fallback
        return particles.map(p => ({
          x: p.x + (p.vx || 0) * dt,
          y: p.y + (p.vy || 0) * dt,
          z: p.z + (p.vz || 0) * dt
        }));
      }
    },

    // Pathfinding in worker
    async findPath(start, end, obstacles) {
      if (DeviceProfile.workerCount <= 1) {
        // Simple direct path
        return [start, end];
      }

      try {
        return await this.execute('workers/path-worker.js', {
          type: 'pathfind',
          start: start,
          end: end,
          obstacles: obstacles
        });
      } catch (e) {
        return [start, end];
      }
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // MEMORY MANAGEMENT SYSTEM
  // ═══════════════════════════════════════════════════════════════════════

  const MemoryManager = {
    pools: new Map(),
    trackedObjects: new Set(),
    disposalQueue: [],
    lastGC: performance.now(),
    gcInterval: 10000, // GC every 10 seconds
    
    // Track an object for disposal
    track(object, type = 'unknown') {
      if (!object) return;
      object.userData = object.userData || {};
      object.userData._trackedType = type;
      object.userData._trackedAt = performance.now();
      this.trackedObjects.add(object);
    },

    // Untrack an object
    untrack(object) {
      this.trackedObjects.delete(object);
    },

    // Queue object for disposal
    queueDisposal(object) {
      if (!object) return;
      this.disposalQueue.push(object);
      this.untrack(object);
    },

    // Process disposal queue
    processDisposalQueue(maxPerFrame = 10) {
      const toDispose = this.disposalQueue.splice(0, maxPerFrame);
      
      toDispose.forEach(obj => {
        this.disposeObject(obj);
      });
      
      return this.disposalQueue.length;
    },

    // Dispose a single object properly
    disposeObject(obj) {
      if (!obj) return;
      
      try {
        // Remove from parent
        if (obj.parent) {
          obj.parent.remove(obj);
        }
        
        // Dispose geometry
        if (obj.geometry) {
          obj.geometry.dispose();
          obj.geometry = null;
        }
        
        // Dispose material(s)
        if (obj.material) {
          if (Array.isArray(obj.material)) {
            obj.material.forEach(m => {
              this.disposeMaterial(m);
            });
          } else {
            this.disposeMaterial(obj.material);
          }
          obj.material = null;
        }
        
        // Dispose textures in userData
        if (obj.userData) {
          Object.values(obj.userData).forEach(val => {
            if (val && val.isTexture) {
              val.dispose();
            }
          });
        }
        
        // Recursively dispose children
        if (obj.children) {
          [...obj.children].forEach(child => this.disposeObject(child));
        }
      } catch (e) {
        console.warn('[MemoryManager] Disposal error:', e);
      }
    },

    // Dispose material and its textures
    disposeMaterial(material) {
      if (!material) return;
      
      // Dispose textures
      ['map', 'normalMap', 'specularMap', 'alphaMap', 'emissiveMap', 
       'roughnessMap', 'metalnessMap', 'displacementMap'].forEach(prop => {
        if (material[prop]) {
          material[prop].dispose();
          material[prop] = null;
        }
      });
      
      material.dispose();
    },

    // Run garbage collection hints
    maybeGC() {
      const now = performance.now();
      if (now - this.lastGC > this.gcInterval) {
        // Hint to JS engine
        if (window.gc) {
          try { window.gc(); } catch (e) {}
        }
        this.lastGC = now;
      }
    },

    // Get memory stats (approximate)
    getStats() {
      const stats = {
        trackedObjects: this.trackedObjects.size,
        disposalQueue: this.disposalQueue.length,
        memoryUsed: 0
      };
      
      if (performance.memory) {
        stats.jsHeapSize = performance.memory.usedJSHeapSize;
        stats.jsHeapLimit = performance.memory.jsHeapSizeLimit;
        stats.jsHeapPercent = (stats.jsHeapSize / stats.jsHeapLimit * 100).toFixed(1) + '%';
      }
      
      return stats;
    },

    // Clean up everything
    disposeAll() {
      this.trackedObjects.forEach(obj => this.disposeObject(obj));
      this.trackedObjects.clear();
      this.disposalQueue.forEach(obj => this.disposeObject(obj));
      this.disposalQueue = [];
      InstancingSystem.disposeAll();
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // TEXTURE ATLAS SYSTEM
  // ═══════════════════════════════════════════════════════════════════════

  const TextureAtlas = {
    atlases: {},
    canvas: null,
    ctx: null,

    // Create a texture atlas from multiple sources
    createAtlas(name, sources, size = 1024) {
      if (this.atlases[name]) return this.atlases[name];
      
      this.canvas = this.canvas || document.createElement('canvas');
      this.canvas.width = size;
      this.canvas.height = size;
      this.ctx = this.ctx || this.canvas.getContext('2d');
      this.ctx.clearRect(0, 0, size, size);
      
      const atlas = {
        texture: new THREE.CanvasTexture(this.canvas),
        regions: {},
        nextX: 0,
        nextY: 0,
        rowHeight: 0,
        size: size
      };
      
      // Pack regions (simple shelf packing)
      sources.forEach((source, i) => {
        const w = source.width || 128;
        const h = source.height || 128;
        
        if (this.nextX + w > size) {
          this.nextX = 0;
          this.nextY += this.rowHeight;
          this.rowHeight = 0;
        }
        
        if (this.nextY + h > size) {
          console.warn('[TextureAtlas] Atlas full, skipping remaining');
          return;
        }
        
        // Draw to atlas
        if (source.draw) {
          source.draw(this.ctx, this.nextX, this.nextY, w, h);
        } else if (source.color) {
          this.ctx.fillStyle = source.color;
          this.ctx.fillRect(this.nextX, this.nextY, w, h);
        }
        
        // Store UV coordinates
        atlas.regions[source.name] = {
          u0: this.nextX / size,
          v0: 1 - (this.nextY + h) / size,
          u1: (this.nextX + w) / size,
          v1: 1 - this.nextY / size,
          width: w,
          height: h
        };
        
        this.nextX += w;
        this.rowHeight = Math.max(this.rowHeight, h);
      });
      
      atlas.texture.needsUpdate = true;
      this.atlases[name] = atlas;
      
      return atlas;
    },

    // Get UVs for a named region
    getUVs(atlasName, regionName) {
      const atlas = this.atlases[atlasName];
      if (!atlas) return null;
      return atlas.regions[regionName];
    },

    // Get texture for an atlas
    getTexture(atlasName) {
      const atlas = this.atlases[atlasName];
      return atlas ? atlas.texture : null;
    },

    // Dispose an atlas
    disposeAtlas(name) {
      if (this.atlases[name]) {
        this.atlases[name].texture.dispose();
        delete this.atlases[name];
      }
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // ADAPTIVE RENDERING
  // ═══════════════════════════════════════════════════════════════════════

  const AdaptiveRendering = {
    frameTimeHistory: [],
    historySize: 30,
    lastFrameTime: 0,
    adaptiveEnabled: true,
    currentScale: 1.0,
    targetFrameTime: 1000 / 60, // 60fps
    
    // Record frame time
    recordFrame(timestamp) {
      if (this.lastFrameTime > 0) {
        const frameTime = timestamp - this.lastFrameTime;
        this.frameTimeHistory.push(frameTime);
        
        if (this.frameTimeHistory.length > this.historySize) {
          this.frameTimeHistory.shift();
        }
      }
      this.lastFrameTime = timestamp;
    },

    // Get average frame time
    getAverageFrameTime() {
      if (this.frameTimeHistory.length === 0) return this.targetFrameTime;
      const sum = this.frameTimeHistory.reduce((a, b) => a + b, 0);
      return sum / this.frameTimeHistory.length;
    },

    // Get current FPS
    getFPS() {
      return Math.round(1000 / this.getAverageFrameTime());
    },

    // Adjust quality based on performance
    adjustQuality() {
      if (!this.adaptiveEnabled) return;
      
      const avgFrameTime = this.getAverageFrameTime();
      const ratio = avgFrameTime / this.targetFrameTime;
      
      // If consistently slow, reduce quality
      if (ratio > 1.3 && this.frameTimeHistory.length >= this.historySize) {
        this.currentScale = Math.max(0.5, this.currentScale * 0.95);
        this.applyQualityScale();
      }
      // If fast, slowly increase quality
      else if (ratio < 0.8 && this.currentScale < 1.0) {
        this.currentScale = Math.min(1.0, this.currentScale * 1.02);
        this.applyQualityScale();
      }
    },

    // Apply current quality scale
    applyQualityScale() {
      // This would adjust renderer settings
      const renderer = window.ScaleEngine ? window.ScaleEngine.getRenderer() : null;
      if (renderer && renderer.setPixelRatio) {
        const baseRatio = DeviceProfile.pixelRatio;
        renderer.setPixelRatio(baseRatio * this.currentScale);
      }
    },

    // Get skip frame recommendation (for very slow frames)
    shouldSkipFrame() {
      const avg = this.getAverageFrameTime();
      return avg > this.targetFrameTime * 2;
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // SCENE OPTIMIZATION HELPERS
  // ═══════════════════════════════════════════════════════════════════════

  const SceneOptimizer = {
    // Optimize a standard scene by converting repeated objects to instancing
    optimizeScene(scene, options = {}) {
      const groups = new Map();
      
      // Group similar meshes
      scene.traverse(obj => {
        if (obj.isMesh && !obj.userData.skipInstancing) {
          const key = `${obj.geometry.uuid}_${obj.material.uuid}`;
          if (!groups.has(key)) {
            groups.set(key, []);
          }
          groups.get(key).push(obj);
        }
      });
      
      // Convert groups with multiple objects to instanced meshes
      groups.forEach((objects, key) => {
        if (objects.length >= (options.minCount || 5)) {
          this.convertToInstanced(scene, objects);
        }
      });
    },

    // Convert array of meshes to single instanced mesh
    convertToInstanced(scene, objects) {
      if (objects.length === 0) return;
      
      const template = objects[0];
      const geometry = template.geometry;
      const material = template.material;
      
      const instancedMesh = new THREE.InstancedMesh(geometry, material, objects.length);
      
      const dummy = new THREE.Object3D();
      objects.forEach((obj, i) => {
        dummy.position.copy(obj.position);
        dummy.rotation.copy(obj.rotation);
        dummy.scale.copy(obj.scale);
        dummy.updateMatrix();
        instancedMesh.setMatrixAt(i, dummy.matrix);
        
        // Remove original
        if (obj.parent) obj.parent.remove(obj);
        MemoryManager.queueDisposal(obj);
      });
      
      instancedMesh.instanceMatrix.needsUpdate = true;
      scene.add(instancedMesh);
      MemoryManager.track(instancedMesh, 'instanced');
      
      return instancedMesh;
    },

    // Batch update materials
    batchMaterialUpdate(materials, property, value) {
      materials.forEach(mat => {
        if (mat[property] !== undefined) {
          mat[property] = value;
        }
      });
    },

    // Set up automatic LOD switching for an object
    setupLOD(object, lodLevels) {
      object.userData.lodLevels = lodLevels;
      object.userData.currentLOD = -1;
      
      return {
        update: (camera) => {
          const distance = object.position.distanceTo(camera.position);
          let targetLOD = 0;
          
          for (let i = 0; i < DeviceProfile.lodDistance.length; i++) {
            if (distance > DeviceProfile.lodDistance[i]) {
              targetLOD = i + 1;
            }
          }
          
          if (targetLOD !== object.userData.currentLOD) {
            object.userData.currentLOD = targetLOD;
            const level = lodLevels[Math.min(targetLOD, lodLevels.length - 1)];
            if (level) {
              this.applyLODLevel(object, level);
            }
          }
        }
      };
    },

    applyLODLevel(object, level) {
      if (level.visible !== undefined) {
        object.visible = level.visible;
      }
      if (level.material && object.material) {
        // Swap material
        const oldMat = object.material;
        object.material = level.material;
        // Don't dispose oldMat here - it might be shared
      }
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // PERFORMANCE MONITORING
  // ═══════════════════════════════════════════════════════════════════════

  const PerformanceMonitor = {
    metrics: {
      fps: 0,
      frameTime: 0,
      drawCalls: 0,
      triangles: 0,
      geometries: 0,
      textures: 0,
      memory: 0
    },
    
    lastLog: 0,
    logInterval: 5000,
    
    // Update metrics from renderer info
    update(renderer) {
      if (!renderer) return;
      
      const info = renderer.info;
      this.metrics.drawCalls = info.render.calls;
      this.metrics.triangles = info.render.triangles;
      this.metrics.geometries = info.memory.geometries;
      this.metrics.textures = info.memory.textures;
      
      this.metrics.fps = AdaptiveRendering.getFPS();
      this.metrics.frameTime = AdaptiveRendering.getAverageFrameTime().toFixed(2);
      
      if (performance.memory) {
        this.metrics.memory = (performance.memory.usedJSHeapSize / 1048576).toFixed(1) + ' MB';
      }
    },

    // Log performance periodically
    maybeLog() {
      const now = performance.now();
      if (now - this.lastLog > this.logInterval) {
        console.log('[PerformanceMonitor]', {
          fps: this.metrics.fps,
          frameTime: this.metrics.frameTime + 'ms',
          drawCalls: this.metrics.drawCalls,
          triangles: this.metrics.triangles.toLocaleString(),
          memory: this.metrics.memory
        });
        
        const cullStats = CullingSystem.getStats();
        if (cullStats.total > 0) {
          console.log('[Culling]', cullStats.ratio + ' culled');
        }
        
        this.lastLog = now;
      }
    },

    // Get all metrics
    getMetrics() {
      return { ...this.metrics };
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // PUBLIC API
  // ═══════════════════════════════════════════════════════════════════════

  window.PerformanceEngine = {
    // Device detection
    DeviceProfile: DeviceProfile,
    detectDevice: detectDevice,
    
    // LOD
    LOD: LODSystem,
    getLODSettings: (scaleId) => LODSystem.getSettings(scaleId),
    
    // Instancing
    Instancing: InstancingSystem,
    getInstancedPool: (type, material, count) => InstancingSystem.getPool(type, material, count),
    addInstance: (pool, pos, scale, rot) => InstancingSystem.addInstance(pool, pos, scale, rot),
    
    // Culling
    Culling: CullingSystem,
    updateFrustum: (camera) => CullingSystem.update(camera),
    isVisible: (obj) => CullingSystem.isVisible(obj),
    
    // Workers
    Workers: WorkerSystem,
    executeInWorker: (script, data, timeout) => WorkerSystem.execute(script, data, timeout),
    
    // Memory
    Memory: MemoryManager,
    trackObject: (obj, type) => MemoryManager.track(obj, type),
    queueDisposal: (obj) => MemoryManager.queueDisposal(obj),
    processDisposal: (max) => MemoryManager.processDisposalQueue(max),
    disposeAll: () => MemoryManager.disposeAll(),
    
    // Texture Atlas
    Atlas: TextureAtlas,
    createAtlas: (name, sources, size) => TextureAtlas.createAtlas(name, sources, size),
    
    // Adaptive Rendering
    Adaptive: AdaptiveRendering,
    recordFrame: (ts) => AdaptiveRendering.recordFrame(ts),
    adjustQuality: () => AdaptiveRendering.adjustQuality(),
    getFPS: () => AdaptiveRendering.getFPS(),
    
    // Scene optimization
    Optimizer: SceneOptimizer,
    optimizeScene: (scene, opts) => SceneOptimizer.optimizeScene(scene, opts),
    
    // Monitoring
    Monitor: PerformanceMonitor,
    updateMetrics: (renderer) => PerformanceMonitor.update(renderer),
    maybeLog: () => PerformanceMonitor.maybeLog(),
    getMetrics: () => PerformanceMonitor.getMetrics(),
    
    // Initialization
    init() {
      detectDevice();
      WorkerSystem.init();
      
      // Add frame recording to core loop if available
      if (window.PFExplorer && window.PFExplorer.loop) {
        const originalLoop = window.PFExplorer.loop;
        window.PFExplorer.loop = function(timestamp) {
          AdaptiveRendering.recordFrame(timestamp);
          PerformanceMonitor.update(
            window.ScaleEngine ? window.ScaleEngine.getRenderer() : null
          );
          PerformanceMonitor.maybeLog();
          MemoryManager.processDisposalQueue(5);
          MemoryManager.maybeGC();
          
          // Adaptive quality adjustment every 60 frames
          if (Math.floor(timestamp / 16) % 60 === 0) {
            AdaptiveRendering.adjustQuality();
          }
          
          return originalLoop.call(this, timestamp);
        };
      }
      
      console.log('[PerformanceEngine] Initialized for ' + DeviceProfile.tier + ' tier device');
      return this;
    }
  };

  // Auto-initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      window.PerformanceEngine.init();
    });
  } else {
    // Already loaded
    setTimeout(() => window.PerformanceEngine.init(), 0);
  }

})();
