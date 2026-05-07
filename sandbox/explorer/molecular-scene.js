/**
 * Molecular Scene — Molecular Bonds and Vibrational Modes
 *
 * "A molecule is a locked phase relationship between atomic orbitals."
 *
 * At the molecular scale (10⁻⁹ m), electron wavefunctions from different
 * atoms overlap and lock into coherent relationships — chemical bonds.
 * These bonds vibrate, rotate, and bend with quantized energies,
 * carrying the propagation signatures of their constituent atoms.
 *
 * Visual layers:
 *   1. Molecular structure       — atoms as spheres, bonds as cylinders
 *   2. Vibrational modes         — animated bond stretching/bending
 *   3. Electron cloud overlap    — the shared electron density
 *   4. Van der Waals envelope    — the molecule's outer boundary
 *   5. Rotational motion         — the molecule tumbling in space
 */
(function () {
  'use strict';

  var scene, camera, renderer;
  var _objs = [];
  var _mats = [];
  var _shaders = [];
  var _clock;
  var _moleculeGroup;

  // ── Coordinate ────────────────────────────────────────────────────────────
  function molecularY() {
    var LOG_MIN = Math.log10(1.616e-35);
    var LOG_MAX = 26;
    return ((-9 - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100;
  }

  // ── Water Molecule (H2O) ──────────────────────────────────────────────────
  function buildWaterMolecule() {
    var centerY = molecularY();
    var centerPos = new THREE.Vector3(5, molecularY(), 0);

    _moleculeGroup = new THREE.Group();
    _moleculeGroup.position.copy(centerPos);

    // Oxygen atom (larger, red)
    var oxygenGeo = new THREE.SphereGeometry(1, 32, 32);
    var oxygenMat = new THREE.MeshStandardMaterial({
      color: 0xff4444,
      emissive: 0xff4444,
      emissiveIntensity: 0.35,
      metalness: 0.3,
      roughness: 0.4
    });
    var oxygen = new THREE.Mesh(oxygenGeo, oxygenMat);
    oxygen.userData = { isAtom: true, element: 'O' };
    _moleculeGroup.add(oxygen);

    // Hydrogen atoms
    var hydrogenGeo = new THREE.SphereGeometry(0.5, 24, 24);
    var hydrogenMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      emissive: 0xffffff,
      emissiveIntensity: 0.25,
      metalness: 0.1,
      roughness: 0.3
    });

    // H1 — at 104.5° angle, ~0.96 Å distance
    var h1 = new THREE.Mesh(hydrogenGeo, hydrogenMat);
    h1.position.set(
      Math.cos(Math.PI / 6) * 2,
      Math.sin(Math.PI / 6) * 2,
      0
    );
    h1.userData = { isAtom: true, element: 'H', bondIndex: 0 };
    _moleculeGroup.add(h1);

    // H2
    var h2 = new THREE.Mesh(hydrogenGeo, hydrogenMat);
    h2.position.set(
      Math.cos(-Math.PI / 6) * 2,
      Math.sin(-Math.PI / 6) * 2,
      0
    );
    h2.userData = { isAtom: true, element: 'H', bondIndex: 1 };
    _moleculeGroup.add(h2);

    // Bonds — cylinders connecting atoms
    var bondMat = new THREE.MeshStandardMaterial({
      color: 0x88ccff,
      emissive: 0x88ccff,
      emissiveIntensity: 0.3,
      metalness: 0.5,
      roughness: 0.3
    });

    // Bond 1 (O-H1)
    var bond1Geo = new THREE.CylinderGeometry(0.12, 0.12, 2, 12);
    var bond1 = new THREE.Mesh(bond1Geo, bondMat);
    bond1.position.copy(h1.position).multiplyScalar(0.5);
    bond1.lookAt(h1.position);
    bond1.rotateX(Math.PI / 2);
    bond1.userData = { isBond: true, atomA: oxygen, atomB: h1, bondIndex: 0 };
    _moleculeGroup.add(bond1);

    // Bond 2 (O-H2)
    var bond2Geo = new THREE.CylinderGeometry(0.12, 0.12, 2, 12);
    var bond2 = new THREE.Mesh(bond2Geo, bondMat);
    bond2.position.copy(h2.position).multiplyScalar(0.5);
    bond2.lookAt(h2.position);
    bond2.rotateX(Math.PI / 2);
    bond2.userData = { isBond: true, atomA: oxygen, atomB: h2, bondIndex: 1 };
    _moleculeGroup.add(bond2);

    // Electron cloud — shared orbital representation
    var cloudGeo = new THREE.SphereGeometry(2.2, 32, 32);
    var cloudMat = new THREE.MeshBasicMaterial({
      color: 0x88ccff,
      transparent: true,
      opacity: 0.08,
      side: THREE.BackSide
    });
    var cloud = new THREE.Mesh(cloudGeo, cloudMat);
    cloud.scale.set(1, 0.7, 1);
    cloud.userData = { isElectronCloud: true };
    _moleculeGroup.add(cloud);

    // Lone pair lobes (oxygen's unshared electrons)
    var lobeGeo = new THREE.SphereGeometry(0.4, 16, 16);
    var lobeMat = new THREE.MeshBasicMaterial({
      color: 0x88ccff,
      transparent: true,
      opacity: 0.3
    });

    var lobe1 = new THREE.Mesh(lobeGeo, lobeMat);
    lobe1.position.set(0, 1.5, 1);
    _moleculeGroup.add(lobe1);

    var lobe2 = new THREE.Mesh(lobeGeo, lobeMat);
    lobe2.position.set(0, 1.5, -1);
    _moleculeGroup.add(lobe2);

    _objs.push(_moleculeGroup);
    scene.add(_moleculeGroup);

    // Track materials for disposal
    _mats.push(oxygenMat, hydrogenMat, bondMat, cloudMat, lobeMat);
  }

  // ── Wave Field Background ─────────────────────────────────────────────────
  function buildWaveField() {
    var centerY = molecularY();

    if (window.PropagationShaders) {
      var fieldGeo = new THREE.PlaneGeometry(20, 14);
      var fieldMat = window.PropagationShaders.createWaveFieldMaterial({
        scale: 0.9,
        decay: 0.28,
        color1: 0x48cae4,
        color2: 0x69ff94,
        bgColor: 0x020408
      });
      var field = new THREE.Mesh(fieldGeo, fieldMat);
      field.position.set(6, centerY, -3);
      _objs.push(field);
      _shaders.push(fieldMat);
      scene.add(field);
    }
  }

  // ── Vibrational Mode Visualization ───────────────────────────────────────
  function buildVibrationIndicators() {
    var centerY = molecularY();
    var centerPos = new THREE.Vector3(5, centerY, 0);

    // Symmetric stretch indicator
    var stretchGeo = new THREE.RingGeometry(3.5, 3.8, 32);
    var stretchMat = new THREE.MeshBasicMaterial({
      color: 0x69ff94,
      transparent: true,
      opacity: 0.2,
      side: THREE.DoubleSide
    });
    var stretch = new THREE.Mesh(stretchGeo, stretchMat);
    stretch.position.copy(centerPos);
    stretch.rotation.x = Math.PI / 2;
    stretch.userData = { isVibration: true, mode: 'stretch', phase: 0 };
    _objs.push(stretch);
    _mats.push(stretchMat);
    scene.add(stretch);

    // Bending mode indicator
    var bendGeo = new THREE.RingGeometry(2.8, 3.1, 32);
    var bendMat = new THREE.MeshBasicMaterial({
      color: 0xffdd55,
      transparent: true,
      opacity: 0.15,
      side: THREE.DoubleSide
    });
    var bend = new THREE.Mesh(bendGeo, bendMat);
    bend.position.copy(centerPos);
    bend.rotation.x = Math.PI / 2;
    bend.rotation.y = Math.PI / 4;
    bend.userData = { isVibration: true, mode: 'bend', phase: Math.PI / 2 };
    _objs.push(bend);
    _mats.push(bendMat);
    scene.add(bend);
  }

  // ── Surrounding Molecules (atmosphere) ─────────────────────────────────
  function buildMolecularAtmosphere() {
    var centerY = molecularY();
    var count = 50;

    for (var i = 0; i < count; i++) {
      var smallGeo = new THREE.SphereGeometry(0.15, 8, 8);
      var smallMat = new THREE.MeshBasicMaterial({
        color: Math.random() > 0.5 ? 0x88ccff : 0xffffff,
        transparent: true,
        opacity: 0.3
      });
      var small = new THREE.Mesh(smallGeo, smallMat);

      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 8 + Math.random() * 6;
      small.position.set(
        5 + r * Math.sin(phi) * Math.cos(theta),
        centerY + r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      );

      small.userData = {
        isAmbient: true,
        drift: new THREE.Vector3(
          (Math.random() - 0.5) * 0.1,
          (Math.random() - 0.5) * 0.1,
          (Math.random() - 0.5) * 0.1
        )
      };
      _objs.push(small);
      _mats.push(smallMat);
      scene.add(small);
    }
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
    ctx.fillStyle = '#48cae4';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Molecular Scale — 10⁻⁹ m', 12, 48);
    var tex = new THREE.CanvasTexture(canvas);
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(16, molecularY(), 3);
    sprite.scale.set(20, 4, 1);
    scene.add(sprite);
    _objs.push(sprite);
    _mats.push(mat);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.MolecularScene = {
    activate: function (s, c) {
      scene = s;
      camera = c;
      _clock = new THREE.Clock();
      _moleculeGroup = null;

      if (window.PostFX) {
        window.PostFX.addFog(scene, { color: 0x020408, density: 0.015 });
      } else {
        scene.fog = new THREE.FogExp2(0x020408, 0.015);
      }

      buildWaterMolecule();
      buildWaveField();
      buildVibrationIndicators();
      buildMolecularAtmosphere();
      buildLabel();

      camera.position.set(5, molecularY(), 18);
      camera.lookAt(5, molecularY(), 0);
    },

    getCameraPosition: function () {
      return {
        position: new THREE.Vector3(5, molecularY(), 18),
        target: new THREE.Vector3(5, molecularY(), 0),
        fov: 48
      };
    },

    getSharedElements: function () {
      // Return molecular bonds for vibration morphing
      return _objs.filter(function (o) {
        return o.userData && o.userData.isBond;
      });
    },

    /**
     * Get LOD level for this scene (0 = highest detail)
     * Used by PerformanceEngine for adaptive quality
     */
    getLODLevel: function () {
      // Molecular scene uses medium-high LOD
      return 1;
    },

    /**
     * Prepare scene with LOD settings before activation
     */
    prepare: function (lodSettings) {
      if (lodSettings) {
        console.log('[MolecularScene] Preparing with LOD:', lodSettings);
      }
    },

    update: function (dt, time) {
      _shaders.forEach(function (m) {
        if (m.uniforms && m.uniforms.uTime) {
          m.uniforms.uTime.value = time;
        }
      });

      // Rotate entire molecule
      if (_moleculeGroup) {
        _moleculeGroup.rotation.y += dt * 0.3;
        _moleculeGroup.rotation.z = Math.sin(time * 0.5) * 0.1;
      }

      // Vibrational modes
      _objs.forEach(function (o) {
        if (o.userData && o.userData.isVibration) {
          if (o.userData.mode === 'stretch') {
            var stretch = 1 + 0.1 * Math.sin(time * 8 + o.userData.phase);
            o.scale.set(stretch, stretch, 1);
          } else if (o.userData.mode === 'bend') {
            var bend = 1 + 0.08 * Math.sin(time * 6 + o.userData.phase);
            o.scale.set(1, bend, 1);
          }
        }
        if (o.userData && o.userData.isAmbient) {
          o.position.add(o.userData.drift);
          // Wrap around boundary
          if (o.position.distanceTo(new THREE.Vector3(5, molecularY(), 0)) > 18) {
            o.position.sub(o.userData.drift.clone().multiplyScalar(100));
          }
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
      _moleculeGroup = null;
      if (scene) scene.fog = null;
    }
  };
}());
