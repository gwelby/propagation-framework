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

    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    container.appendChild(renderer.domElement);

    // Post-processing
    var composer = null;
    try {
      composer = new THREE.EffectComposer(renderer);
      composer.addPass(new THREE.RenderPass(scene, camera));
      var bloom = new THREE.UnrealBloomPass(new THREE.Vector2(width, height), BELT_CONFIG.bloomStrength, BELT_CONFIG.bloomRadius, BELT_CONFIG.bloomThreshold);
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
    var ribbonMat = new THREE.MeshStandardMaterial({
      color: BELT_CONFIG.ribbonColor1,
      emissive: BELT_CONFIG.ribbonEmissive,
      metalness: 0.3,
      roughness: 0.6,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.9
    });
    var ribbon = new THREE.Mesh(ribbonGeo, ribbonMat);
    ribbon.rotation.x = Math.PI / 2;
    ribbon.position.set(0, 0, -BELT_CONFIG.ribbonLength / 2);
    scene.add(ribbon);

    // Cube group
    var rotationGroup = new THREE.Group();
    var cubeGeo = new THREE.BoxGeometry(0.5, 0.5, 0.5);
    var cubeMat = new THREE.MeshStandardMaterial({ color: BELT_CONFIG.objectColor, metalness: 0.5 });
    var cube = new THREE.Mesh(cubeGeo, cubeMat);
    rotationGroup.add(cube);
    rotationGroup.position.set(0, 0, -BELT_CONFIG.ribbonLength);
    scene.add(rotationGroup);

    // Fixed origin
    var fixedGeo = new THREE.BoxGeometry(0.5, 0.5, 0.5);
    var fixedMat = new THREE.MeshStandardMaterial({ color: 0x888888 });
    var fixedCube = new THREE.Mesh(fixedGeo, fixedMat);
    scene.add(fixedCube);

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
                  "<p class=\"eyebrow\">π₁(SO(3)) = ℤ₂</p>" +
                  "<h3>The Belt Trick: Why 720° = Identity</h3>" +
                  "<p>Spin-1/2 particles require 4π rotation to return to original state. This underlies the (2,1) weight ratio.</p>" +
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
    },

    unmount: function () {
      disposeBelt3D(this.panelState);
      this.panelState = null;
    },

    resize: function (ctx) {
      var ps = this.panelState;
      if (!ps || !ps._3d) return;
      var r = ps._3d;
      var w = ps.beltContainer.clientWidth;
      var h = ps.beltContainer.clientHeight;
      r.camera.aspect = w / h;
      r.camera.updateProjectionMatrix();
      r.renderer.setSize(w, h);
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
          "<span class=\"status-pill status-conditional\">CONDITIONAL</span>" +
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
      if (!this.panelState || !this.panelState._3d) return;
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
