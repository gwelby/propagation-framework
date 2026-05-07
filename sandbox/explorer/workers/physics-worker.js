/**
 * Physics Worker — Off-Main-Thread Physics Calculations
 * 
 * Handles:
 *   - Particle system updates (positions, velocities, collisions)
 *   - Force field calculations
 *   - Collision detection for large numbers of objects
 *   - Wave propagation simulation
 *   - Coherence field computation
 * 
 * Communicates via postMessage with main thread.
 */

(function() {
  'use strict';

  // Physics constants
  const PHYSICS = {
    EPSILON: 1e-10,
    MAX_FORCE: 1000,
    DAMPING: 0.99,
    TIME_STEP_MAX: 0.05
  };

  // Vector3 operations (minimal implementation for worker)
  const Vec3 = {
    add: (a, b) => ({ x: a.x + b.x, y: a.y + b.y, z: a.z + b.z }),
    sub: (a, b) => ({ x: a.x - b.x, y: a.y - b.y, z: a.z - b.z }),
    mul: (a, s) => ({ x: a.x * s, y: a.y * s, z: a.z * s }),
    dot: (a, b) => a.x * b.x + a.y * b.y + a.z * b.z,
    length: (a) => Math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z),
    normalize: (a) => {
      const len = Math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
      if (len < PHYSICS.EPSILON) return { x: 0, y: 0, z: 0 };
      return { x: a.x / len, y: a.y / len, z: a.z / len };
    },
    distance: (a, b) => {
      const dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z;
      return Math.sqrt(dx * dx + dy * dy + dz * dz);
    },
    distanceSq: (a, b) => {
      const dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z;
      return dx * dx + dy * dy + dz * dz;
    }
  };

  // Particle system processor
  function updateParticles(particles, dt, forces) {
    const count = particles.length;
    const results = new Array(count);
    
    // Limit dt for stability
    const timeStep = Math.min(dt, PHYSICS.TIME_STEP_MAX);
    
    for (let i = 0; i < count; i++) {
      const p = particles[i];
      
      // Start with current state
      let newPos = { x: p.x, y: p.y, z: p.z };
      let newVel = { 
        x: p.vx || 0, 
        y: p.vy || 0, 
        z: p.vz || 0 
      };
      
      // Apply forces
      if (forces) {
        let force = { x: 0, y: 0, z: 0 };
        
        // Gravity
        if (forces.gravity) {
          force.y -= forces.gravity;
        }
        
        // Attraction/repulsion fields
        if (forces.fields) {
          forces.fields.forEach(field => {
            const toField = Vec3.sub(field.position, newPos);
            const distSq = toField.x * toField.x + toField.y * toField.y + toField.z * toField.z;
            const dist = Math.sqrt(distSq) + PHYSICS.EPSILON;
            
            if (dist < field.radius) {
              const strength = field.strength / (distSq + PHYSICS.EPSILON);
              const dir = Vec3.mul(toField, 1 / dist);
              const f = Vec3.mul(dir, strength);
              force = Vec3.add(force, f);
            }
          });
        }
        
        // Apply force to velocity (F = ma, assume m=1)
        const acc = Vec3.mul(force, timeStep);
        newVel = Vec3.add(newVel, acc);
      }
      
      // Apply damping
      newVel = Vec3.mul(newVel, PHYSICS.DAMPING);
      
      // Update position
      const velStep = Vec3.mul(newVel, timeStep);
      newPos = Vec3.add(newPos, velStep);
      
      // Boundary constraints
      if (forces && forces.bounds) {
        const b = forces.bounds;
        if (newPos.x < b.minX) { newPos.x = b.minX; newVel.x *= -0.5; }
        if (newPos.x > b.maxX) { newPos.x = b.maxX; newVel.x *= -0.5; }
        if (newPos.y < b.minY) { newPos.y = b.minY; newVel.y *= -0.5; }
        if (newPos.y > b.maxY) { newPos.y = b.maxY; newVel.y *= -0.5; }
        if (newPos.z < b.minZ) { newPos.z = b.minZ; newVel.z *= -0.5; }
        if (newPos.z > b.maxZ) { newPos.z = b.maxZ; newVel.z *= -0.5; }
      }
      
      results[i] = {
        x: newPos.x,
        y: newPos.y,
        z: newPos.z,
        vx: newVel.x,
        vy: newVel.y,
        vz: newVel.z,
        id: p.id
      };
    }
    
    return results;
  }

  // Wave propagation simulation (for field visualization)
  function propagateWaves(grid, dt, speed, damping) {
    const width = grid.width;
    const height = grid.height;
    const current = grid.values;
    const previous = grid.prevValues || [...current];
    const result = new Float32Array(width * height);
    
    const c2 = (speed * dt) * (speed * dt);
    
    for (let y = 1; y < height - 1; y++) {
      for (let x = 1; x < width - 1; x++) {
        const idx = y * width + x;
        
        // Discrete 2D wave equation
        const neighbors = 
          current[idx - 1] + current[idx + 1] + 
          current[idx - width] + current[idx + width];
        
        result[idx] = 2 * current[idx] - previous[idx] + 
                      c2 * (neighbors - 4 * current[idx]);
        result[idx] *= damping;
      }
    }
    
    // Copy edges
    for (let x = 0; x < width; x++) {
      result[x] = current[x];
      result[(height - 1) * width + x] = current[(height - 1) * width + x];
    }
    for (let y = 0; y < height; y++) {
      result[y * width] = current[y * width];
      result[y * width + width - 1] = current[y * width + width - 1];
    }
    
    return {
      values: result,
      prevValues: current,
      width: width,
      height: height
    };
  }

  // Coherence field computation
  function computeCoherenceField(particles, resolution = 64, radius = 10) {
    const field = new Float32Array(resolution * resolution);
    const cellSize = (radius * 2) / resolution;
    
    for (let py = 0; py < resolution; py++) {
      for (let px = 0; px < resolution; px++) {
        const worldX = (px - resolution / 2) * cellSize;
        const worldZ = (py - resolution / 2) * cellSize;
        
        let coherence = 0;
        
        // Sum phase-aligned contributions from nearby particles
        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          const dx = p.x - worldX;
          const dz = p.z - worldZ;
          const distSq = dx * dx + dz * dz;
          
          if (distSq < radius * radius) {
            const phase = p.phase || 0;
            const amplitude = Math.exp(-distSq / (2 * radius));
            coherence += Math.cos(phase) * amplitude;
          }
        }
        
        field[py * resolution + px] = coherence / particles.length;
      }
    }
    
    return field;
  }

  // Collision detection (broad phase + narrow phase)
  function detectCollisions(objects, radius = 1.0) {
    const collisions = [];
    const count = objects.length;
    const radiusSq = radius * radius;
    
    // Simple O(n^2) for small counts, spatial hash for larger
    if (count < 100) {
      for (let i = 0; i < count; i++) {
        for (let j = i + 1; j < count; j++) {
          const a = objects[i];
          const b = objects[j];
          const distSq = Vec3.distanceSq(a, b);
          
          if (distSq < radiusSq) {
            collisions.push({
              a: i,
              b: j,
              distance: Math.sqrt(distSq),
              penetration: radius - Math.sqrt(distSq)
            });
          }
        }
      }
    } else {
      // Spatial hash for larger systems
      const cellSize = radius * 2;
      const grid = new Map();
      
      // Insert into grid
      for (let i = 0; i < count; i++) {
        const o = objects[i];
        const cellX = Math.floor(o.x / cellSize);
        const cellY = Math.floor(o.y / cellSize);
        const cellZ = Math.floor(o.z / cellSize);
        const key = `${cellX},${cellY},${cellZ}`;
        
        if (!grid.has(key)) grid.set(key, []);
        grid.get(key).push(i);
      }
      
      // Check neighboring cells
      for (let i = 0; i < count; i++) {
        const o = objects[i];
        const cellX = Math.floor(o.x / cellSize);
        const cellY = Math.floor(o.y / cellSize);
        const cellZ = Math.floor(o.z / cellSize);
        
        for (let dx = -1; dx <= 1; dx++) {
          for (let dy = -1; dy <= 1; dy++) {
            for (let dz = -1; dz <= 1; dz++) {
              const key = `${cellX + dx},${cellY + dy},${cellZ + dz}`;
              const cell = grid.get(key);
              if (!cell) continue;
              
              for (let j = 0; j < cell.length; j++) {
                const otherIdx = cell[j];
                if (otherIdx <= i) continue;
                
                const distSq = Vec3.distanceSq(o, objects[otherIdx]);
                if (distSq < radiusSq) {
                  collisions.push({
                    a: i,
                    b: otherIdx,
                    distance: Math.sqrt(distSq),
                    penetration: radius - Math.sqrt(distSq)
                  });
                }
              }
            }
          }
        }
      }
    }
    
    return collisions;
  }

  // Handle messages from main thread
  self.onmessage = function(e) {
    const { taskId, data } = e.data;
    let result;
    
    try {
      switch (data.type) {
        case 'particles':
          result = updateParticles(
            data.particles,
            data.dt || 0.016,
            data.forces || null
          );
          break;
          
        case 'waves':
          result = propagateWaves(
            data.grid,
            data.dt || 0.016,
            data.speed || 1.0,
            data.damping || 0.99
          );
          break;
          
        case 'coherence':
          result = computeCoherenceField(
            data.particles,
            data.resolution || 64,
            data.radius || 10
          );
          break;
          
        case 'collisions':
          result = detectCollisions(
            data.objects,
            data.radius || 1.0
          );
          break;
          
        case 'orbit':
          // Simple orbital mechanics
          result = data.objects.map(obj => {
            const center = data.center || { x: 0, y: 0, z: 0 };
            const toCenter = Vec3.sub(center, obj);
            const dist = Vec3.length(toCenter);
            const force = data.G * obj.mass * data.centerMass / (dist * dist + PHYSICS.EPSILON);
            const dir = Vec3.normalize(toCenter);
            const acc = Vec3.mul(dir, force / obj.mass);
            
            const newVel = Vec3.add(
              { x: obj.vx || 0, y: obj.vy || 0, z: obj.vz || 0 },
              Vec3.mul(acc, data.dt || 0.016)
            );
            const newPos = Vec3.add(obj, Vec3.mul(newVel, data.dt || 0.016));
            
            return {
              x: newPos.x, y: newPos.y, z: newPos.z,
              vx: newVel.x, vy: newVel.y, vz: newVel.z
            };
          });
          break;
          
        default:
          result = { error: 'Unknown physics task type: ' + data.type };
      }
    } catch (err) {
      result = { error: err.message, stack: err.stack };
    }
    
    self.postMessage({ taskId, result });
  };

  // Signal ready
  self.postMessage({ type: 'ready', version: '1.0.0' });
})();
