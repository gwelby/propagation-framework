/**
 * Scale Scenes — Per-scale Three.js Scene Configurations
 * 
 * Each scale registers a scene object with the ScaleEngine.
 * The engine activates/deactivates scenes as the user navigates.
 * 
 * Scene object shape:
 *   {
 *     activate(scene, camera) — called when this scale becomes active
 *     deactivate()            — called when leaving this scale
 *     update(dt, time)        — called each frame (optional)
 *     dispose()               — cleanup (optional)
 *   }
 * 
 * Scale visual taxonomy:
 *   Planck (-35)     → FieldDensity (quantum foam, discrete geometry)
 *   GUT (-25)        → WaveField (force unification as merging waves)
 *   Matter (-18)     → HelixRibbon (standing wave = mass)
 *   Atomic (-10)     → WaveField (Bohr orbits as phase closure)
 *   Molecular (-9)    → WaveField (covalent bonds as locked phases)
 *   Cellular (-5)    → FieldDensity (active coherence maintenance)
 *   Neural (-3)      → WaveField (neural coherence oscillations)
 *   Cosmic (+26)     → FieldDensity (cosmic web as frozen pattern)
 */

(function () {
  'use strict';

  var _scene, _camera;
  var _activeObjects = [];
  var _activeMaterials = [];

  function track(mesh, mat) {
    _activeObjects.push(mesh);
    if (mat) _activeMaterials.push(mat);
  }

  function clearScene() {
    _activeObjects.forEach(function (o) {
      if (o.geometry) o.geometry.dispose();
      if (o.material) {
        if (Array.isArray(o.material)) {
          o.material.forEach(function (m) { m.dispose(); });
        } else {
          o.material.dispose();
        }
        }
      _scene.remove(o);
    });
    _activeObjects = [];
    _activeMaterials = [];
  }

  // ── Scale Scene Definitions ──────────────────────────────────────────────

  var scenes = {

    planck: window.PlanckScene || null,

    'quantum-foam': {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var count = 120;
        for (var i = 0; i < count; i++) {
          var r = 3 + Math.random() * 7;
          var theta = Math.random() * Math.PI * 2;
          var phi = Math.acos(2 * Math.random() - 1);
          var geo = new THREE.SphereGeometry(0.15 + Math.random() * 0.25, 12, 12);
          var mat = new THREE.MeshStandardMaterial({
            color: 0xd4a017,
            emissive: 0xd4a017,
            emissiveIntensity: 0.4 + Math.random() * 0.4,
            transparent: true,
            opacity: 0.6 + Math.random() * 0.3
          });
          var mesh = new THREE.Mesh(geo, mat);
          mesh.position.set(
            r * Math.sin(phi) * Math.cos(theta),
            metersToY(1e-33) + (Math.random() - 0.5) * 6,
            r * Math.sin(phi) * Math.sin(theta)
          );
          mesh.userData.baseIntensity = mat.emissiveIntensity;
          mesh.userData.phase = Math.random() * Math.PI * 2;
          track(mesh, mat);
          scene.add(mesh);
        }
        addScaleLabel(scene, 'Quantum Foam — 10⁻³³ m', new THREE.Vector3(8, metersToY(1e-33), 0), 0xd4a017);
      },

      update: function (dt, time) {
        _activeObjects.forEach(function (o) {
          if (o.userData.baseIntensity !== undefined) {
            o.material.emissiveIntensity = o.userData.baseIntensity * (0.6 + 0.4 * Math.sin(time * 2 + o.userData.phase));
          }
        });
      },

      deactivate: clearScene
    },

    gut: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var mat = window.PropagationShaders.createWaveFieldMaterial({
          scale: 0.8,
          decay: 0.4,
          color1: 0x9b59b6,
          color2: 0x7b2cbf,
          bgColor: 0x020408
        });
        var geo = new THREE.PlaneGeometry(18, 12);
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(6, metersToY(1e-25), 0);
        track(mesh, mat);
        scene.add(mesh);
        addScaleLabel(scene, 'GUT Scale — 10⁻²⁵ m', mesh.position, 0x9b59b6);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
      },

      deactivate: clearScene
    },

    matter: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;

        // Central helix — standing wave = mass
        var helixGeo = window.PropagationShaders.createHelixRibbonGeometry(1.8, 8, 3, 0.12);
        var helixMat = new THREE.MeshStandardMaterial({
          color: 0x00e5ff,
          emissive: 0x00e5ff,
          emissiveIntensity: 0.55,
          metalness: 0.7,
          roughness: 0.25,
          transparent: true,
          opacity: 0.9
        });
        var helix = new THREE.Mesh(helixGeo, helixMat);
        helix.position.set(5, metersToY(1.145e-18) - 2, 0);
        track(helix, helixMat);
        scene.add(helix);

        // Coherence shell
        var shellGeo = new THREE.SphereGeometry(2.8, 48, 48);
        var shellMat = window.PropagationShaders.createFieldDensityMaterial({
          density: 0.4,
          coherence: 0.75,
          fieldColor: 0x00e5ff,
          cohColor: 0x69ff94,
          bgColor: 0x020408
        });
        var shell = new THREE.Mesh(shellGeo, shellMat);
        shell.position.copy(helix.position);
        track(shell, shellMat);
        scene.add(shell);

        // Orbital electron indicator
        var orbGeo = new THREE.TorusGeometry(3.6, 0.06, 8, 64);
        var orbMat = new THREE.MeshStandardMaterial({
          color: 0x00e5ff,
          emissive: 0x00e5ff,
          emissiveIntensity: 0.3,
          transparent: true,
          opacity: 0.4
        });
        var orb = new THREE.Mesh(orbGeo, orbMat);
        orb.position.copy(helix.position);
        orb.rotation.x = Math.PI / 4;
        track(orb, orbMat);
        scene.add(orb);

        addScaleLabel(scene, 'Matter Scale — 10⁻¹⁸ m', helix.position, 0x00e5ff);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
        _activeObjects.forEach(function (o) {
          if (o.geometry && o.geometry.type === 'TorusGeometry') {
            o.rotation.z += dt * 0.3;
          }
          if (o.geometry && o.geometry.type === 'TubeGeometry') {
            o.rotation.y += dt * 0.15;
          }
        });
      },

      deactivate: clearScene
    },

    atomic: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var mat = window.PropagationShaders.createWaveFieldMaterial({
          scale: 1.2,
          decay: 0.35,
          color1: 0x0077b6,
          color2: 0x00e5ff,
          bgColor: 0x020408
        });
        var geo = new THREE.PlaneGeometry(20, 14);
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(6, metersToY(1e-10), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Bohr orbit rings
        var radii = [3, 5, 7];
        radii.forEach(function (r, i) {
          var orbGeo = new THREE.TorusGeometry(r, 0.07, 8, 64);
          var orbMat = new THREE.MeshStandardMaterial({
            color: 0x0077b6,
            emissive: 0x0077b6,
            emissiveIntensity: 0.25,
            transparent: true,
            opacity: 0.4 - i * 0.1
          });
          var orb = new THREE.Mesh(orbGeo, orbMat);
          orb.position.set(mesh.position.x, mesh.position.y, mesh.position.z);
          orb.rotation.x = Math.PI / 2 + (i - 1) * 0.3;
          track(orb, orbMat);
          scene.add(orb);
        });
        addScaleLabel(scene, 'Atomic Scale — 10⁻¹⁰ m', mesh.position, 0x0077b6);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
        _activeObjects.forEach(function (o) {
          if (o.geometry && o.geometry.type === 'TorusGeometry') {
            o.rotation.z += dt * (0.2 + o.geometry.parameters.tube * 0.02);
          }
        });
      },

      deactivate: clearScene
    },

    molecular: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var mat = window.PropagationShaders.createWaveFieldMaterial({
          scale: 0.9,
          decay: 0.28,
          color1: 0x48cae4,
          color2: 0x69ff94,
          bgColor: 0x020408
        });
        var geo = new THREE.PlaneGeometry(18, 12);
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(6, metersToY(1e-9), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Bond lines between nodes
        var nodes = [
          new THREE.Vector3(-3, 0, 0),
          new THREE.Vector3(0, 2, 0),
          new THREE.Vector3(3, 0, 0),
          new THREE.Vector3(0, -2, 0)
        ];
        for (var i = 0; i < nodes.length; i++) {
          var next = nodes[(i + 1) % nodes.length];
          var mid = new THREE.Vector3().addVectors(nodes[i], next).multiplyScalar(0.5);
          var bondGeo = new THREE.CylinderGeometry(0.05, 0.05, nodes[i].distanceTo(next), 8);
          var bondMat = new THREE.MeshStandardMaterial({
            color: 0x48cae4,
            emissive: 0x48cae4,
            emissiveIntensity: 0.3,
            transparent: true,
            opacity: 0.6
          });
          var bond = new THREE.Mesh(bondGeo, bondMat);
          bond.position.copy(mesh.position).add(mid);
          bond.lookAt(mesh.position.clone().add(nodes[i]).add(nodes[(i + 1) % 4]));
          bond.rotateX(Math.PI / 2);
          track(bond, bondMat);
          scene.add(bond);

          // Node spheres
          var nodeGeo = new THREE.SphereGeometry(0.3, 16, 16);
          var nodeMat = new THREE.MeshStandardMaterial({
            color: 0x69ff94,
            emissive: 0x69ff94,
            emissiveIntensity: 0.5
          });
          var node = new THREE.Mesh(nodeGeo, nodeMat);
          node.position.copy(mesh.position).add(nodes[i]);
          track(node, nodeMat);
          scene.add(node);
        }
        addScaleLabel(scene, 'Molecular Scale — 10⁻⁹ m', mesh.position, 0x48cae4);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
      },

      deactivate: clearScene
    },

    virus: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        // Icosahedral virus shell
        var geo = new THREE.IcosahedronGeometry(4, 1);
        var mat = new THREE.MeshStandardMaterial({
          color: 0x69ff94,
          emissive: 0x69ff94,
          emissiveIntensity: 0.3,
          metalness: 0.6,
          roughness: 0.35,
          wireframe: false
        });
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(5, metersToY(1e-7), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Surface spikes
        var spikeCount = 20;
        for (var i = 0; i < spikeCount; i++) {
          var theta = Math.random() * Math.PI * 2;
          var phi = Math.acos(2 * Math.random() - 1);
          var x = Math.sin(phi) * Math.cos(theta);
          var y = Math.sin(phi) * Math.sin(theta);
          var z = Math.cos(phi);
          var spikeGeo = new THREE.CylinderGeometry(0.04, 0.1, 1.2, 6);
          var spikeMat = new THREE.MeshStandardMaterial({
            color: 0x69ff94,
            emissive: 0x80ed99,
            emissiveIntensity: 0.4,
            transparent: true,
            opacity: 0.8
          });
          var spike = new THREE.Mesh(spikeGeo, spikeMat);
          spike.position.set(
            mesh.position.x + x * 4.5,
            mesh.position.y + y * 4.5,
            mesh.position.z + z * 4.5
          );
          spike.lookAt(new THREE.Vector3(
            mesh.position.x + x * 10,
            mesh.position.y + y * 10,
            mesh.position.z + z * 10
          ));
          spike.userData.rotSpeed = (Math.random() - 0.5) * 0.5;
          track(spike, spikeMat);
          scene.add(spike);
        }
        addScaleLabel(scene, 'Virus Scale — 10⁻⁷ m', mesh.position, 0x69ff94);
      },

      update: function (dt, time) {
        _activeObjects.forEach(function (o) {
          if (o.userData.rotSpeed) {
            o.rotation.x += dt * o.userData.rotSpeed;
            o.rotation.y += dt * o.userData.rotSpeed * 0.7;
          } else if (o.geometry && o.geometry.type === 'IcosahedronGeometry') {
            o.rotation.y += dt * 0.08;
          }
        });
      },

      deactivate: clearScene
    },

    cellular: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var geo = new THREE.SphereGeometry(6, 48, 48);
        var mat = window.PropagationShaders.createFieldDensityMaterial({
          density: 0.55,
          coherence: 0.7,
          fieldColor: 0x80ed99,
          cohColor: 0x69ff94,
          bgColor: 0x020408
        });
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(5, metersToY(1e-5), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Cytoskeleton filaments
        for (var f = 0; f < 8; f++) {
          var curve = new THREE.CatmullRomCurve3([
            mesh.position.clone(),
            new THREE.Vector3(
              mesh.position.x + (Math.random() - 0.5) * 8,
              mesh.position.y + (Math.random() - 0.5) * 8,
              mesh.position.z + (Math.random() - 0.5) * 8
            )
          ]);
          var filGeo = new THREE.TubeGeometry(curve, 20, 0.08, 8, false);
          var filMat = new THREE.MeshStandardMaterial({
            color: 0x80ed99,
            emissive: 0x80ed99,
            emissiveIntensity: 0.3,
            transparent: true,
            opacity: 0.6
          });
          var fil = new THREE.Mesh(filGeo, filMat);
          track(fil, filMat);
          scene.add(fil);
        }
        addScaleLabel(scene, 'Cellular Scale — 10⁻⁵ m', mesh.position, 0x80ed99);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
        if (_activeObjects[0]) {
          _activeObjects[0].rotation.y += dt * 0.06;
        }
      },

      deactivate: clearScene
    },

    neural: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var mat = window.PropagationShaders.createWaveFieldMaterial({
          scale: 0.4,
          decay: 0.2,
          color1: 0xffdd55,
          color2: 0xffb347,
          bgColor: 0x020408
        });
        var geo = new THREE.PlaneGeometry(20, 14);
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(6, metersToY(1e-2), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Neural node network
        var nodePositions = [
          [-4, 2], [-2, -1], [0, 3], [2, 1], [4, -2],
          [-3, -3], [1, -3], [3, 3]
        ];
        nodePositions.forEach(function (p) {
          var nodeGeo = new THREE.SphereGeometry(0.3, 12, 12);
          var nodeMat = new THREE.MeshStandardMaterial({
            color: 0xffdd55,
            emissive: 0xffdd55,
            emissiveIntensity: 0.6,
            transparent: true,
            opacity: 0.85
          });
          var node = new THREE.Mesh(nodeGeo, nodeMat);
          node.position.set(mesh.position.x + p[0], mesh.position.y + p[1], 0.5);
          node.userData.phase = Math.random() * Math.PI * 2;
          track(node, nodeMat);
          scene.add(node);
        });
        addScaleLabel(scene, 'Neural Scale — 10⁻² m', mesh.position, 0xffdd55);
      },

      update: function (dt, time) {
        _activeMaterials.forEach(function (m) {
          if (m.uniforms && m.uniforms.uTime) m.uniforms.uTime.value = time;
        });
        _activeObjects.forEach(function (o) {
          if (o.userData.phase !== undefined) {
            var pulse = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(time * 3 + o.userData.phase));
            o.material.emissiveIntensity = pulse;
          }
        });
      },

      deactivate: clearScene
    },

    human: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        // Simple human silhouette (torso approximation)
        var torsoGeo = new THREE.CapsuleGeometry(1.2, 3, 8, 16);
        var torsoMat = new THREE.MeshStandardMaterial({
          color: 0xffb347,
          emissive: 0xffb347,
          emissiveIntensity: 0.15,
          metalness: 0.3,
          roughness: 0.6,
          transparent: true,
          opacity: 0.8
        });
        var torso = new THREE.Mesh(torsoGeo, torsoMat);
        torso.position.set(5, metersToY(1), 0);
        track(torso, torsoMat);
        scene.add(torso);

        // Head
        var headGeo = new THREE.SphereGeometry(0.9, 24, 24);
        var head = new THREE.Mesh(headGeo, torsoMat);
        head.position.set(5, metersToY(1) + 2.8, 0);
        track(head, torsoMat);
        scene.add(head);

        // Torus for 2/3 ratio symbol
        var ratioGeo = new THREE.TorusGeometry(0.5, 0.08, 8, 32);
        var ratioMat = new THREE.MeshStandardMaterial({
          color: 0xffb347,
          emissive: 0xffb347,
          emissiveIntensity: 0.5,
          transparent: true,
          opacity: 0.7
        });
        var ratio = new THREE.Mesh(ratioGeo, ratioMat);
        ratio.position.set(8, metersToY(1), 0);
        track(ratio, ratioMat);
        scene.add(ratio);

        addScaleLabel(scene, 'Human Scale — 10⁰ m', torso.position, 0xffb347);
      },

      update: function (dt, time) {
        _activeObjects.forEach(function (o) {
          if (o.geometry && o.geometry.type === 'TorusGeometry') {
            o.rotation.x += dt * 0.4;
            o.rotation.y += dt * 0.3;
          }
        });
      },

      deactivate: clearScene
    },

    planetary: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        // Planet sphere
        var geo = new THREE.SphereGeometry(5, 48, 48);
        var mat = new THREE.MeshStandardMaterial({
          color: 0xff9f43,
          emissive: 0xff9f43,
          emissiveIntensity: 0.2,
          metalness: 0.4,
          roughness: 0.55
        });
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(5, metersToY(1e11), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Atmosphere glow
        var atmGeo = new THREE.SphereGeometry(5.6, 48, 48);
        var atmMat = new THREE.MeshBasicMaterial({
          color: 0xff9f43,
          transparent: true,
          opacity: 0.08,
          side: THREE.BackSide
        });
        var atm = new THREE.Mesh(atmGeo, atmMat);
        atm.position.copy(mesh.position);
        track(atm, atmMat);
        scene.add(atm);

        // Orbit path
        var orbGeo = new THREE.TorusGeometry(9, 0.06, 8, 64);
        var orbMat = new THREE.MeshStandardMaterial({
          color: 0xff9f43,
          emissive: 0xff9f43,
          emissiveIntensity: 0.2,
          transparent: true,
          opacity: 0.3
        });
        var orb = new THREE.Mesh(orbGeo, orbMat);
        orb.position.copy(mesh.position);
        orb.rotation.x = Math.PI / 3;
        track(orb, orbMat);
        scene.add(orb);

      addScaleLabel(scene, 'Planetary Scale — 10⁷ m', mesh.position, 0xff9f43);
      },

      update: function (dt, time) {
        if (_activeObjects[0]) _activeObjects[0].rotation.y += dt * 0.05;
        if (_activeObjects[1]) _activeObjects[1].rotation.z += dt * 0.02;
      },

      deactivate: clearScene
    },

    stellar: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;
        var geo = new THREE.SphereGeometry(6, 48, 48);
        var mat = new THREE.MeshStandardMaterial({
          color: 0xff6b6b,
          emissive: 0xff6b6b,
          emissiveIntensity: 0.8,
          metalness: 0.2,
          roughness: 0.4
        });
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(5, metersToY(1e9), 0);
        track(mesh, mat);
        scene.add(mesh);

        // Corona glow
        var coronaGeo = new THREE.SphereGeometry(7.5, 32, 32);
        var coronaMat = new THREE.MeshBasicMaterial({
          color: 0xff6b6b,
          transparent: true,
          opacity: 0.06,
          side: THREE.BackSide
        });
        var corona = new THREE.Mesh(coronaGeo, coronaMat);
        corona.position.copy(mesh.position);
        track(corona, coronaMat);
        scene.add(corona);

        addScaleLabel(scene, 'Stellar Scale — 10⁹ m', mesh.position, 0xff6b6b);
      },

      update: function (dt, time) {
        if (_activeObjects[0]) {
          _activeObjects[0].material.emissiveIntensity = 0.7 + 0.15 * Math.sin(time * 1.5);
        }
      },

      deactivate: clearScene
    },

    galactic: {
      activate: function (scene, camera) {
        _scene = scene;
        _camera = camera;

        // Spiral galaxy (simplified)
        var spiralArms = 2;
        var armCount = 200;
        var positions = new Float32Array(armCount * 3);
        for (var a = 0; a < spiralArms; a++) {
          var offset = (a / spiralArms) * Math.PI * 2;
          for (var i = 0; i < armCount / spiralArms; i++) {
            var t = i / (armCount / spiralArms);
            var r = 1 + t * 10;
            var angle = offset + t * Math.PI * 2.5;
            var idx = (a * armCount / spiralArms + i) * 3;
            positions[idx] = r * Math.cos(angle);
            positions[idx + 1] = (Math.random() - 0.5) * 0.8;
            positions[idx + 2] = r * Math.sin(angle);
          }
        }
        var pGeo = new THREE.BufferGeometry();
        pGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        var pMat = new THREE.PointsMaterial({
          color: 0x7c5cbf,
          size: 0.25,
          transparent: true,
          opacity: 0.8
        });
        var galaxy = new THREE.Points(pGeo, pMat);
        galaxy.position.set(5, metersToY(1e21), 0);
        galaxy.userData.rotSpeed = 0.04;
        track(galaxy, pMat);
        scene.add(galaxy);

        // Central bulge
        var bulgeGeo = new THREE.SphereGeometry(1.5, 24, 24);
        var bulgeMat = new THREE.MeshStandardMaterial({
          color: 0xffdd55,
          emissive: 0xffdd55,
          emissiveIntensity: 0.6,
          transparent: true,
          opacity: 0.7
        });
        var bulge = new THREE.Mesh(bulgeGeo, bulgeMat);
        bulge.position.copy(galaxy.position);
        track(bulge, bulgeMat);
        scene.add(bulge);

        addScaleLabel(scene, 'Galactic Scale — 10²¹ m', galaxy.position, 0x7c5cbf);
      },

      update: function (dt, time) {
        _activeObjects.forEach(function (o) {
          if (o.userData.rotSpeed) {
            o.rotation.y += dt * o.userData.rotSpeed;
          }
        });
      },

      deactivate: clearScene
    },

    cosmic: window.CosmicScene || null,
  };

  // Scales with no custom scene use the default node only
  var noCustomScene = ['proton', 'nuclear'];

  // ── Helpers ────────────────────────────────────────────────────────────────

  function metersToY(meters) {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    var LOG_RANGE = LOG_MAX - LOG_MIN;
    var BEAM_LENGTH = 100;
    var logM = Math.log10(meters);
    return ((logM - LOG_MIN) / LOG_RANGE) * BEAM_LENGTH;
  }

  function addScaleLabel(scene, text, position, color) {
    if (!window.ScaleEngine) return;
    var canvas = document.createElement('canvas');
    canvas.width = 480;
    canvas.height = 80;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 480, 80);
    var hex = '#' + color.toString(16).padStart(6, '0');
    ctx.font = 'bold 28px DM Sans, sans-serif';
    ctx.fillStyle = hex;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 8, 40);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(position.x + position.y * 0.05 + 6, position.y, position.z + 3);
    sprite.scale.set(18, 3.5, 1);
    scene.add(sprite);
  }

  // ── Registration ──────────────────────────────────────────────────────────

  function registerScenes() {
    if (!window.ScaleEngine) {
      console.warn('[scale-scenes] ScaleEngine not found — skipping registration');
      return;
    }
    Object.keys(scenes).forEach(function (scaleId) {
      window.ScaleEngine.registerScene(scaleId, scenes[scaleId]);
    });
    console.log('[scale-scenes] Registered', Object.keys(scenes).length, 'custom scale scenes');
  }

  // Auto-register when ScaleEngine is ready
  if (window.ScaleEngine) {
    registerScenes();
  } else {
    window.addEventListener('DOMContentLoaded', function () {
      setTimeout(registerScenes, 100);
    });
  }
}());
