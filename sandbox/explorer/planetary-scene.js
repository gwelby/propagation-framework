/**
 * Planetary Scene — Solar System with Curved Light Paths
 *
 * "Gravity is not a force. It is the geometry of propagation."
 *
 * At the planetary scale (10⁷ m), we see the playground of curved spacetime.
 * Light follows geodesics — not straight lines — through the gravitational
 * wells of massive bodies. This is Fermat's principle applied to the medium
 * of spacetime itself.
 *
 * Visual layers:
 *   1. Central star           — the gravitational anchor
 *   2. Planetary orbits       — curved paths in the gravitational field
 *   3. Light ray geodesics    — bent paths showing gravitational lensing
 *   4. Gravitational well     — the depression in the fabric
 *   5. Lagrange points        — stability nodes in the field
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;
  var _orbitNodes = [];

  // ── Coordinate ────────────────────────────────────────────────────────────
  function planetaryY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((7 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Central Star ───────────────────────────────────────────────────────────
  function buildCentralStar() {
    var centerY = planetaryY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    // Star core
    var coreGeo = new THREE.SphereGeometry(1.8, 48, 48);
    var coreMat = new THREE.MeshStandardMaterial({
      color: 0xff9f43,
      emissive: 0xff9f43,
      emissiveIntensity: 1.2,
      metalness: 0.2,
      roughness: 0.4
    });
    var core = new THREE.Mesh(coreGeo, coreMat);
    core.position.copy(centerPos);
    _objs.push(core);
    _mats.push(coreMat);
    scene.add(core);

    // Corona glow
    var coronaGeo = new THREE.SphereGeometry(2.4, 32, 32);
    var coronaMat = new THREE.MeshBasicMaterial({
      color: 0xff9f43,
      transparent: true,
      opacity: 0.12,
      side: THREE.BackSide
    });
    var corona = new THREE.Mesh(coronaGeo, coronaMat);
    corona.position.copy(centerPos);
    _objs.push(corona);
    _mats.push(coronaMat);
    scene.add(corona);

    // Solar wind particles
    var windCount = 300;
    var positions = new Float32Array(windCount * 3);
    for (var i = 0; i < windCount; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 2.5 + Math.random() * 3;
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
    }
    var windGeo = new THREE.BufferGeometry();
    windGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var windMat = new THREE.PointsMaterial({
      color: 0xffdd55,
      size: 0.08,
      transparent: true,
      opacity: 0.6
    });
    var wind = new THREE.Points(windGeo, windMat);
    wind.position.copy(centerPos);
    wind.userData.rotSpeed = 0.05;
    _objs.push(wind);
    _mats.push(windMat);
    scene.add(wind);
  }

  // ── Planetary Orbits ───────────────────────────────────────────────────────
  function buildPlanetarySystem() {
    var centerY = planetaryY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    var planets = [
      { radius: 4.5, size: 0.25, color: 0x88aabb, speed: 1.5 },
      { radius: 6.5, size: 0.4, color: 0xcc8866, speed: 1.0 },
      { radius: 9, size: 0.42, color: 0x66aaff, speed: 0.7 },
      { radius: 12, size: 0.35, color: 0xdd8866, speed: 0.5 },
      { radius: 16, size: 0.9, color: 0xd4a574, speed: 0.3 }
    ];

    planets.forEach(function (p, i) {
      // Orbit path ring
      var orbitGeo = new THREE.TorusGeometry(p.radius, 0.03, 6, 64);
      var orbitMat = new THREE.MeshBasicMaterial({
        color: 0xff9f43,
        transparent: true,
        opacity: 0.2
      });
      var orbit = new THREE.Mesh(orbitGeo, orbitMat);
      orbit.position.copy(centerPos);
      orbit.rotation.x = Math.PI / 2 + (i - 2) * 0.1;
      _objs.push(orbit);
      _mats.push(orbitMat);
      scene.add(orbit);

      // Planet sphere
      var planetGeo = new THREE.SphereGeometry(p.size, 24, 24);
      var planetMat = new THREE.MeshStandardMaterial({
        color: p.color,
        emissive: p.color,
        emissiveIntensity: 0.15,
        metalness: 0.3,
        roughness: 0.6
      });
      var planet = new THREE.Mesh(planetGeo, planetMat);
      var angle = Math.random() * Math.PI * 2;
      planet.position.copy(centerPos).add(new THREE.Vector3(
        Math.cos(angle) * p.radius,
        (Math.random() - 0.5) * 0.5,
        Math.sin(angle) * p.radius
      ));
      planet.userData = {
        orbitRadius: p.radius,
        orbitSpeed: p.speed * 0.1,
        orbitAngle: angle,
        centerPos: centerPos.clone()
      };
      _objs.push(planet);
      _mats.push(planetMat);
      scene.add(planet);
      _orbitNodes.push(planet);

      // Gravitational influence halo
      var haloGeo = new THREE.SphereGeometry(p.size * 2, 16, 16);
      var haloMat = new THREE.MeshBasicMaterial({
        color: p.color,
        transparent: true,
        opacity: 0.06,
        side: THREE.BackSide
      });
      var halo = new THREE.Mesh(haloGeo, haloMat);
      halo.position.copy(planet.position);
      halo.userData.planetRef = planet;
      _objs.push(halo);
      _mats.push(haloMat);
      scene.add(halo);
    });
  }

  // ── Curved Light Geodesics ────────────────────────────────────────────────
  function buildLightGeodesics() {
    var centerY = planetaryY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    // Create bent light paths showing gravitational lensing
    var rayCount = 5;
    for (var r = 0; r < rayCount; r++) {
      var offset = (r - 2) * 3;
      var points = [];
      var segments = 40;
      for (var i = 0; i <= segments; i++) {
        var t = i / segments;
        var x = -15 + t * 30;
        // Parabolic bend toward central mass
        var distFromCenter = Math.abs(x);
        var bend = 3 * Math.exp(-distFromCenter * 0.3);
        var y = offset + (offset > 0 ? -bend : bend) * (1 - t * 0.5);
        var z = Math.sin(t * Math.PI) * 0.5;
        points.push(new THREE.Vector3(x, y, z));
      }

      var curve = new THREE.CatmullRomCurve3(points);
      var geo = new THREE.TubeGeometry(curve, 32, 0.04, 6, false);
      var mat = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.4 - Math.abs(offset) * 0.05
      });
      var ray = new THREE.Mesh(geo, mat);
      ray.position.copy(centerPos);
      ray.userData.phase = r * Math.PI / 3;
      _objs.push(ray);
      _mats.push(mat);
      scene.add(ray);

      // Animated photon particles along the ray
      var photonGeo = new THREE.SphereGeometry(0.08, 8, 8);
      var photonMat = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        emissiveIntensity: 0.8
      });
      var photon = new THREE.Mesh(photonGeo, photonMat);
      photon.position.copy(centerPos).add(points[0]);
      photon.userData = {
        curve: curve,
        t: 0,
        speed: 0.3 + r * 0.05,
        centerPos: centerPos.clone()
      };
      _objs.push(photon);
      _mats.push(photonMat);
      scene.add(photon);
    }
  }

  // ── Gravitational Well Visualization ──────────────────────────────────────
  function buildGravitationalWell() {
    var centerY = planetaryY();

    // Create a depression mesh showing spacetime curvature
    var wellGeo = new THREE.PlaneGeometry(30, 30, 48, 48);
    var positions = wellGeo.attributes.position.array;
    for (var i = 0; i < positions.length; i += 3) {
      var x = positions[i];
      var z = positions[i + 1];
      var dist = Math.sqrt(x * x + z * z);
      // Gravitational potential well shape
      var depth = -4 * Math.exp(-dist * 0.25);
      positions[i + 2] = depth;
    }
    wellGeo.computeVertexNormals();

    var wellMat = new THREE.MeshStandardMaterial({
      color: 0xff9f43,
      emissive: 0xff9f43,
      emissiveIntensity: 0.1,
      transparent: true,
      opacity: 0.15,
      wireframe: true,
      side: THREE.DoubleSide
    });
    var well = new THREE.Mesh(wellGeo, wellMat);
    well.position.set(5, centerY - 6, 0);
    well.rotation.x = -Math.PI / 2;
    _objs.push(well);
    _mats.push(wellMat);
    scene.add(well);
  }

  // ── Lagrange Points ────────────────────────────────────────────────────────
  function buildLagrangePoints() {
    var centerY = planetaryY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    // L4 and L5 points (60 degrees ahead/behind in orbit)
    var l4Pos = new THREE.Vector3(
      centerPos.x + Math.cos(Math.PI / 3) * 9,
      centerPos.y + 0.5,
      centerPos.z + Math.sin(Math.PI / 3) * 9
    );
    var l5Pos = new THREE.Vector3(
      centerPos.x + Math.cos(-Math.PI / 3) * 9,
      centerPos.y - 0.5,
      centerPos.z + Math.sin(-Math.PI / 3) * 9
    );

    [l4Pos, l5Pos].forEach(function (pos, i) {
      var lGeo = new THREE.SphereGeometry(0.15, 12, 12);
      var lMat = new THREE.MeshBasicMaterial({
        color: 0x69ff94,
        transparent: true,
        opacity: 0.7
      });
      var lPoint = new THREE.Mesh(lGeo, lMat);
      lPoint.position.copy(pos);
      lPoint.userData = {
        baseIntensity: 0.7,
        phase: i * Math.PI,
        isLagrange: true
      };
      _objs.push(lPoint);
      _mats.push(lMat);
      scene.add(lPoint);

      // Stability ring
      var ringGeo = new THREE.RingGeometry(0.3, 0.4, 16);
      var ringMat = new THREE.MeshBasicMaterial({
        color: 0x69ff94,
        transparent: true,
        opacity: 0.25,
        side: THREE.DoubleSide
      });
      var ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.copy(pos);
      ring.rotation.x = Math.PI / 2;
      _objs.push(ring);
      _mats.push(ringMat);
      scene.add(ring);
    });
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
    ctx.fillStyle = '#ff9f43';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Planetary Scale — 10⁷ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, planetaryY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.PlanetaryScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();
      _orbitNodes = [];

      // Volumetric medium fog
      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.007 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.007);
      }

      buildCentralStar();
      buildPlanetarySystem();
      buildLightGeodesics();
      buildGravitationalWell();
      buildLagrangePoints();
      buildLabel();

      // Camera setup
      camera.position.set(5, planetaryY(), 40);
      camera.lookAt(5, planetaryY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, planetaryY(), 40),
        target: new THREE.Vector3(5, planetaryY(), 0),
        fov: 50
      };
    },

    getSharedElements: function () {
      // Return light geodesics (curved paths) for wave morphing
      return _objs.filter(function (o) {
        return o.userData && (
          o.userData.curve ||
          o.userData.isLagrange
        );
      });
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Planetary scene uses medium LOD
      return 1;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[PlanetaryScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      // Update shader uniforms
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      // Animate planets in orbit
      _objs.forEach(function (o) {
        if (o.userData && o.userData.orbitRadius) {
          o.userData.orbitAngle += dt * o.userData.orbitSpeed;
          var r = o.userData.orbitRadius;
          o.position.x = o.userData.centerPos.x + Math.cos(o.userData.orbitAngle) * r;
          o.position.z = o.userData.centerPos.z + Math.sin(o.userData.orbitAngle) * r;
        }
        // Update halos to follow planets
        if (o.userData && o.userData.planetRef) {
          o.position.copy(o.userData.planetRef.position);
        }
        // Animate solar wind
        if (o.userData && o.userData.rotSpeed && !o.userData.orbitRadius) {
          o.rotation.y += dt * o.userData.rotSpeed;
        }
        // Animate photons along geodesics
        if (o.userData && o.userData.curve) {
          o.userData.t += dt * o.userData.speed;
          if (o.userData.t > 1) o.userData.t = 0;
          var point = o.userData.curve.getPoint(o.userData.t);
          o.position.copy(o.userData.centerPos).add(point);
        }
        // Pulse Lagrange points
        if (o.userData && o.userData.isLagrange) {
          o.material.opacity = 0.4 + 0.3 * Math.sin(time * 2 + o.userData.phase);
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
      _orbitNodes = [];
      if (scene) scene.fog = null;
    }
  };
}());
