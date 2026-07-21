/**
 * Generations Panel — Three.js Belt Trick
 * 
 * π₁(SO(3)) = ℤ₂ visualization.
 * Topological numerator (2N) vs SO(3) denominator (3).
 */
(function () {
  'use strict';

  var BELT_CONFIG = {
    ribbonWidth: 0.6,
    ribbonLength: 5,
    ribbonSegments: 100,
    ribbonWidthSegments: 10,
    rotationSpeed: 0.8,
    bgColor: 0x07111c,
    ribbonColor1: 0x00cfff,
    ribbonColor2: 0x44ff88,
    ribbonEmissive: 0x003344,
    objectColor: 0xffdd55,
    bloomStrength: 0.6,
    bloomRadius: 0.3,
    bloomThreshold: 0.8
  };

  // ── Three.js Belt Trick Renderer ───────────────────────────────────────────

  function createBelt3D(panelState, ctx) {
    var container = panelState.beltContainer;
    if (!container || typeof THREE === 'undefined') return;

    var width = container.clientWidth;
    var height = container.clientHeight;

    var scene = new THREE.Scene();
    scene.background = new THREE.Color(BELT_CONFIG.bgColor);
    scene.fog = new THREE.FogExp2(BELT_CONFIG.bgColor, 0.06);

    var camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
    camera.position.set(3, 2.5, 6);
    camera.lookAt(0, 0, -2);

    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    } catch (e) {
      console.warn("WebGL not supported, running in fallback mode:", e);
      container.innerHTML = '';
      var fallbackDiv = document.createElement('div');
      fallbackDiv.className = 'webgl-fallback';
      fallbackDiv.style.cssText = 'display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; min-height: 250px; border: 1px dashed rgba(232, 240, 255, 0.2); border-radius: 8px; background: rgba(9, 21, 37, 0.2); color: rgba(232, 240, 255, 0.8); text-align: center; padding: 20px; box-sizing: border-box;';
      fallbackDiv.innerHTML = '<h4 style="margin: 0 0 8px 0; color: #00cfff;">WebGL Not Supported</h4><p style="margin: 0; font-size: 12px; color: var(--muted); max-width: 280px; line-height: 1.4;">SO(3) topology and Dirac belt Dirac-trick models are calculated and displayed below in the interactive controls.</p>';
      container.appendChild(fallbackDiv);
      panelState._3d = {
        _isFallback: true
      };
      return;
    }
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.3;
    container.appendChild(renderer.domElement);

    // Post-processing
    var composer = null;
    try {
      composer = new THREE.EffectComposer(renderer);
      composer.addPass(new THREE.RenderPass(scene, camera));
      var bloom = new THREE.UnrealBloomPass(new THREE.Vector2(width, height), 1.5, 0.4, 0.85);
      composer.addPass(bloom);
    } catch(e) {}

    // Lighting
    scene.add(new THREE.AmbientLight(0x222244, 0.5));
    var dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
    dirLight.position.set(4, 6, 4);
    dirLight.castShadow = true;
    scene.add(dirLight);

    // Ribbon
    var ribbonGeo = new THREE.PlaneGeometry(BELT_CONFIG.ribbonWidth, BELT_CONFIG.ribbonLength, BELT_CONFIG.ribbonWidthSegments, BELT_CONFIG.ribbonSegments);
    var ribbonMat = new THREE.MeshPhysicalMaterial({
      color: 0x00e5ff,
      emissive: 0x004455,
      metalness: 0.2,
      roughness: 0.1,
      clearcoat: 1.0,
      clearcoatRoughness: 0.1,
      transmission: 0.8,
      thickness: 0.2,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.95
    });
    var ribbon = new THREE.Mesh(ribbonGeo, ribbonMat);
    ribbon.rotation.x = Math.PI / 2;
    ribbon.position.set(0, 0, -BELT_CONFIG.ribbonLength / 2);
    scene.add(ribbon);

    // Cube group (now smooth spheres)
    var rotationGroup = new THREE.Group();
    var sphereGeo = new THREE.SphereGeometry(0.4, 32, 32);
    var endMat = new THREE.MeshStandardMaterial({ 
      color: 0xffdd55, 
      emissive: 0xffaa00,
      emissiveIntensity: 0.4,
      metalness: 0.6,
      roughness: 0.2
    });
    var movingSphere = new THREE.Mesh(sphereGeo, endMat);
    rotationGroup.add(movingSphere);
    
    // Add point light to the moving end to cast dynamic shadows
    var movingLight = new THREE.PointLight(0xffdd55, 1.5, 10);
    movingLight.position.set(0, 0, 0);
    rotationGroup.add(movingLight);
    
    rotationGroup.position.set(0, 0, -BELT_CONFIG.ribbonLength);
    scene.add(rotationGroup);

    // Fixed origin
    var fixedSphere = new THREE.Mesh(sphereGeo, endMat);
    scene.add(fixedSphere);

    panelState._3d = {
      scene: scene,
      camera: camera,
      renderer: renderer,
      composer: composer,
      ribbon: ribbon,
      ribbonGeo: ribbonGeo,
      rotationGroup: rotationGroup,
      currentAngle: 0,
      targetAngle: 0,
      isPlaying: false
    };
  }

  function updateBeltRibbon(panelState, angle) {
    var geo = panelState._3d.ribbonGeo;
    var positions = geo.attributes.position;
    for (var i = 0; i < positions.count; i++) {
      var x = positions.getX(i);
      var y = positions.getY(i);
      var z = positions.getZ(i);
      var t = (y + BELT_CONFIG.ribbonLength / 2) / BELT_CONFIG.ribbonLength;
      var twist = angle * t * (Math.PI / 180);
      var cosT = Math.cos(twist);
      var sinT = Math.sin(twist);
      // We twist around Y in the local plane space, then it's rotated to Z
      positions.setX(i, x * cosT - z * sinT);
      positions.setZ(i, x * sinT + z * cosT);
    }
    positions.needsUpdate = true;
    geo.computeVertexNormals();
  }

  function disposeBelt3D(panelState) {
    if (!panelState || !panelState._3d) return;
    var r = panelState._3d;
    if (r._isFallback) {
      panelState._3d = null;
      return;
    }
    if (r.renderer) r.renderer.dispose();
    if (r.ribbonGeo) r.ribbonGeo.dispose();
    panelState._3d = null;
  }

  // ── Panel Registration ─────────────────────────────────────────────────────

  window.PFExplorer.registerPanel({
    id: "generations",
    title: "Generation Counting",
    mount: function (ctx) {
      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<div class=\"panel-header\">" +
                "<div>" +
                  "<p class=\"eyebrow\"><span style=\"color:#ffaa33; font-family:serif; margin-right:8px;\">N³</span> π₁(SO(3)) = ℤ₂</p>" +
                  "<h3><span style=\"color:#00cfff; font-family:serif; margin-right:8px;\">⬡</span> The Belt Trick: Why 720° = Identity</h3>" +
                  "<p>Spin-1/2 particles require 4π rotation to return to their original state. This topological requirement underlies the (2,1) weight ratio found in the derivation of the three generations.</p>" +
                  "<p class=\"interaction-cue\"><strong>Interaction:</strong> Click 'Animate 720°' to untangle the ribbon by rotating it fully twice. Adjust the generation count N below to see the Q(N) shift.</p>" +
                "</div>" +
              "</div>" +
              "<div id=\"beltTrickContainer\" class=\"belt-trick-container\" style=\"height:300px;position:relative\"></div>" +
              "<div class=\"belt-overlay\">" +
                "<div class=\"belt-angle-display\"><span id=\"beltAngleValue\">0°</span></div>" +
              "</div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"generationInfo\"></section>" +
          "</div>" +
        "</div>";

      this.panelState = {
        beltContainer: ctx.stage.querySelector("#beltTrickContainer"),
        info: ctx.stage.querySelector("#generationInfo"),
        nValue: 3,
        phaseAngle: 0
      };

      createBelt3D(this.panelState, ctx);
      this.renderInfo(ctx);

      // Wire the window resize listener to the canonical resize() method
      // and then snap once so the first frame already matches the laid-out
      // DOM instead of createBelt3D's initial-size fallback.
      var self = this;
      this.panelState._resizeHandler = function () { self.resize(ctx); };
      window.addEventListener('resize', this.panelState._resizeHandler);
      self.resize(ctx);
    },

    unmount: function () {
      if (this.panelState && this.panelState._resizeHandler) {
        window.removeEventListener('resize', this.panelState._resizeHandler);
      }
      disposeBelt3D(this.panelState);
      this.panelState = null;
    },

    resize: function (ctx) {
      var ps = this.panelState;
      if (!ps || !ps._3d || ps._3d._isFallback) return;
      var r = ps._3d;
      var w = ps.beltContainer.clientWidth;
      var h = ps.beltContainer.clientHeight;
      if (w < 2 || h < 2) return;  // DOM not laid out yet; skip cleanly.
      r.camera.aspect = w / h;
      r.camera.updateProjectionMatrix();
      r.renderer.setSize(w, h, false);
      if (r.composer) r.composer.setSize(w, h);
    },

    renderInfo: function (ctx) {
      var self = this;
      var ps = this.panelState;
      var qValue = ctx.utils.qOfN(ps.nValue);
      var exact = Math.abs(qValue - 2 / 3) < 1e-9;

      ps.info.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">Generation lock</p>" +
            "<h3>Q(N) = 2N / (2N + 3)</h3>" +
            "<p>Topological numerator (2N) vs SO(3) denominator (3).</p>" +
          "</div>" +
          (function() {
            var claim = window.PFTruth && window.PFTruth.getClaim ? window.PFTruth.getClaim('three-generations') : null;
            var badge = claim ? (claim.badge || claim.status) : 'UNAVAILABLE';
            var cls = claim ? (claim.statusClass || 'status-unavailable') : 'status-unavailable';
            return '<span class="status-pill ' + cls + '" data-claim-id="three-generations">' + badge + '</span>';
          })() +
        "</div>" +
        ctx.app.renderWrongIntuition(ctx.app.getResult('three-generations')) +
        "<div class=\"control-group\">" +
          "<label>Generation count N</label>" +
          "<input id=\"generationRange\" type=\"range\" min=\"1\" max=\"5\" step=\"1\" value=\"" + ps.nValue + "\" class=\"premium-slider\">" +
          "<output>N = " + ps.nValue + "</output>" +
        "</div>" +
        "<div class=\"formula\">Q(N) = 2N / (2N + 3) = " + qValue.toFixed(6) + "</div>" +
        "<div class=\"stat-grid\">" +
          "<div class=\"stat-tile\"><strong>" + (2 * ps.nValue) + "</strong><span>weight</span></div>" +
          "<div class=\"stat-tile\"><strong>3</strong><span>denominator</span></div>" +
          "<div class=\"stat-tile\"><strong>" + qValue.toFixed(4) + "</strong><span>computed Q</span></div>" +
        "</div>" +
        "<div class=\"belt-button-group\" style=\"margin-top:20px\">" +
          "<button id=\"beltPlayBtn\" class=\"soft-button\">Animate 720°</button>" +
          "<button id=\"beltResetBtn\" class=\"soft-button\">Reset</button>" +
        "</div>";

      ps.info.querySelector("#generationRange").addEventListener("input", function (e) {
        ps.nValue = Number(e.target.value);
        self.renderInfo(ctx);
      });

      ps.info.querySelector("#beltPlayBtn").addEventListener("click", function () {
        if (ps._3d) {
          ps._3d.targetAngle += 720;
          ps._3d.isPlaying = true;
        }
      });

      ps.info.querySelector("#beltResetBtn").addEventListener("click", function () {
        if (ps._3d) {
          ps._3d.currentAngle = 0;
          ps._3d.targetAngle = 0;
          ps._3d.isPlaying = false;
        }
      });
    },

    update: function (ctx, dt) {
      if (!this.panelState || !this.panelState._3d || this.panelState._3d._isFallback) return;
      var r = this.panelState._3d;

      if (r.isPlaying || Math.abs(r.currentAngle - r.targetAngle) > 0.1) {
        var diff = r.targetAngle - r.currentAngle;
        var step = 180 * dt; // 180 deg per sec
        if (Math.abs(diff) > step) {
          r.currentAngle += Math.sign(diff) * step;
        } else {
          r.currentAngle = r.targetAngle;
          r.isPlaying = false;
        }
        updateBeltRibbon(this.panelState, r.currentAngle);
        r.rotationGroup.rotation.y = r.currentAngle * (Math.PI / 180);
        
        var angleVal = document.getElementById('beltAngleValue');
        if (angleVal) angleVal.textContent = Math.round(r.currentAngle % 720) + '°';
      }

      if (r.composer) r.composer.render();
      else r.renderer.render(r.scene, r.camera);
    }
  });
}());
