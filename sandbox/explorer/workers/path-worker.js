/**
 * Path Worker — Off-Main-Thread Pathfinding
 * 
 * Handles:
 *   - A* pathfinding in 3D space
 *   - Navigation mesh simplification
 *   - Obstacle avoidance calculations
 *   - Ray casting for visibility tests
 */

(function() {
  'use strict';

  // Vector operations
  const Vec3 = {
    add: (a, b) => ({ x: a.x + b.x, y: a.y + b.y, z: a.z + b.z }),
    sub: (a, b) => ({ x: a.x - b.x, y: a.y - b.y, z: a.z - b.z }),
    mul: (a, s) => ({ x: a.x * s, y: a.y * s, z: a.z * s }),
    length: (a) => Math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z),
    distance: (a, b) => {
      const dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z;
      return Math.sqrt(dx * dx + dy * dy + dz * dz);
    },
    distanceSq: (a, b) => {
      const dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z;
      return dx * dx + dy * dy + dz * dz;
    },
    normalize: (a) => {
      const len = Math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
      if (len < 1e-10) return { x: 0, y: 0, z: 0 };
      return { x: a.x / len, y: a.y / len, z: a.z / len };
    }
  };

  // A* Node
  class PathNode {
    constructor(position, g = 0, h = 0) {
      this.position = position;
      this.g = g; // Cost from start
      this.h = h; // Heuristic to goal
      this.f = g + h;
      this.parent = null;
      this.visited = false;
      this.closed = false;
    }
  }

  // Simple 3D A* pathfinding
  function findPathAStar(start, end, obstacles, options = {}) {
    const maxIterations = options.maxIterations || 1000;
    const stepSize = options.stepSize || 1.0;
    const obstacleRadius = options.obstacleRadius || 1.5;
    
    // Quick check for direct path
    if (!lineIntersectsObstacles(start, end, obstacles, obstacleRadius)) {
      return [start, end];
    }
    
    // A* search
    const openSet = [];
    const closedSet = [];
    const startNode = new PathNode(start, 0, Vec3.distance(start, end));
    openSet.push(startNode);
    
    let iterations = 0;
    
    while (openSet.length > 0 && iterations < maxIterations) {
      iterations++;
      
      // Find node with lowest f score
      let currentIdx = 0;
      let current = openSet[0];
      for (let i = 1; i < openSet.length; i++) {
        if (openSet[i].f < current.f) {
          current = openSet[i];
          currentIdx = i;
        }
      }
      
      // Check if we reached the goal
      if (Vec3.distance(current.position, end) < stepSize) {
        return reconstructPath(current);
      }
      
      // Move to closed set
      openSet.splice(currentIdx, 1);
      closedSet.push(current);
      current.closed = true;
      
      // Generate neighbors
      const neighbors = generateNeighbors(current.position, stepSize);
      
      for (const neighborPos of neighbors) {
        // Skip if inside obstacle
        if (pointInObstacle(neighborPos, obstacles, obstacleRadius)) {
          continue;
        }
        
        // Skip if already in closed set
        if (closedSet.some(n => Vec3.distance(n.position, neighborPos) < stepSize * 0.5)) {
          continue;
        }
        
        const tentativeG = current.g + Vec3.distance(current.position, neighborPos);
        
        // Check if in open set
        let neighbor = openSet.find(n => 
          Vec3.distance(n.position, neighborPos) < stepSize * 0.5
        );
        
        if (!neighbor) {
          neighbor = new PathNode(
            neighborPos,
            tentativeG,
            Vec3.distance(neighborPos, end)
          );
          neighbor.parent = current;
          openSet.push(neighbor);
        } else if (tentativeG < neighbor.g) {
          neighbor.g = tentativeG;
          neighbor.f = neighbor.g + neighbor.h;
          neighbor.parent = current;
        }
      }
    }
    
    // If no path found, return partial path to closest node
    if (closedSet.length > 0) {
      let closest = closedSet[0];
      let closestDist = Vec3.distance(closest.position, end);
      for (const node of closedSet) {
        const dist = Vec3.distance(node.position, end);
        if (dist < closestDist) {
          closest = node;
          closestDist = dist;
        }
      }
      return reconstructPath(closest);
    }
    
    return [start, end];
  }

  // Generate neighbor positions
  function generateNeighbors(pos, step) {
    const dirs = [
      { x: 1, y: 0, z: 0 }, { x: -1, y: 0, z: 0 },
      { x: 0, y: 1, z: 0 }, { x: 0, y: -1, z: 0 },
      { x: 0, y: 0, z: 1 }, { x: 0, y: 0, z: -1 },
      { x: 0.7, y: 0.7, z: 0 }, { x: 0.7, y: -0.7, z: 0 },
      { x: -0.7, y: 0.7, z: 0 }, { x: -0.7, y: -0.7, z: 0 }
    ];
    
    return dirs.map(d => Vec3.add(pos, Vec3.mul(d, step)));
  }

  // Reconstruct path from end node
  function reconstructPath(endNode) {
    const path = [];
    let current = endNode;
    while (current) {
      path.unshift(current.position);
      current = current.parent;
    }
    return path;
  }

  // Check if point is inside any obstacle
  function pointInObstacle(point, obstacles, radius) {
    const rSq = radius * radius;
    for (const obs of obstacles) {
      if (Vec3.distanceSq(point, obs) < rSq) {
        return true;
      }
    }
    return false;
  }

  // Check if line segment intersects any obstacle
  function lineIntersectsObstacles(start, end, obstacles, radius) {
    const dir = Vec3.sub(end, start);
    const len = Vec3.length(dir);
    const rSq = radius * radius;
    
    if (len < 1e-10) return false;
    
    const normDir = Vec3.mul(dir, 1 / len);
    
    for (const obs of obstacles) {
      // Distance from point to line
      const toStart = Vec3.sub(obs, start);
      const proj = toStart.x * normDir.x + toStart.y * normDir.y + toStart.z * normDir.z;
      const clampedProj = Math.max(0, Math.min(len, proj));
      
      const closest = Vec3.add(start, Vec3.mul(normDir, clampedProj));
      const distSq = Vec3.distanceSq(obs, closest);
      
      if (distSq < rSq) {
        return true;
      }
    }
    
    return false;
  }

  // Simplify path (remove unnecessary points)
  function simplifyPath(path, obstacles, radius) {
    if (path.length <= 2) return path;
    
    const simplified = [path[0]];
    let current = 0;
    
    while (current < path.length - 1) {
      let furthest = current + 1;
      
      // Find furthest point we can see
      for (let i = current + 2; i < path.length; i++) {
        if (!lineIntersectsObstacles(path[current], path[i], obstacles, radius)) {
          furthest = i;
        } else {
          break;
        }
      }
      
      simplified.push(path[furthest]);
      current = furthest;
    }
    
    return simplified;
  }

  // Ray casting for visibility
  function rayCast(origin, direction, obstacles, maxDistance = 100) {
    const hit = {
      hit: false,
      distance: maxDistance,
      point: Vec3.add(origin, Vec3.mul(Vec3.normalize(direction), maxDistance)),
      obstacle: null
    };
    
    const normDir = Vec3.normalize(direction);
    
    for (const obs of obstacles) {
      // Ray-sphere intersection
      const toObs = Vec3.sub(obs, origin);
      const proj = toObs.x * normDir.x + toObs.y * normDir.y + toObs.z * normDir.z;
      
      if (proj < 0 || proj > maxDistance) continue;
      
      const closest = Vec3.add(origin, Vec3.mul(normDir, proj));
      const distSq = Vec3.distanceSq(obs, closest);
      const radiusSq = (obs.radius || 1) * (obs.radius || 1);
      
      if (distSq < radiusSq && proj < hit.distance) {
        hit.hit = true;
        hit.distance = proj;
        hit.point = closest;
        hit.obstacle = obs;
      }
    }
    
    return hit;
  }

  // Handle messages
  self.onmessage = function(e) {
    const { taskId, data } = e.data;
    let result;
    
    try {
      switch (data.type) {
        case 'pathfind':
          result = findPathAStar(
            data.start,
            data.end,
            data.obstacles || [],
            data.options || {}
          );
          break;
          
        case 'simplify':
          result = simplifyPath(
            data.path,
            data.obstacles || [],
            data.obstacleRadius || 1.5
          );
          break;
          
        case 'raycast':
          result = rayCast(
            data.origin,
            data.direction,
            data.obstacles || [],
            data.maxDistance || 100
          );
          break;
          
        case 'visibility':
          // Quick visibility check
          result = !lineIntersectsObstacles(
            data.start,
            data.end,
            data.obstacles || [],
            data.obstacleRadius || 1.5
          );
          break;
          
        default:
          result = { error: 'Unknown pathfinding task: ' + data.type };
      }
    } catch (err) {
      result = { error: err.message, stack: err.stack };
    }
    
    self.postMessage({ taskId, result });
  };

  // Signal ready
  self.postMessage({ type: 'ready', version: '1.0.0' });
})();
