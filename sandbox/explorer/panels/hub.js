(function () {
  var scaleNotes = {
    planck: "The ladder starts at the geometry boundary: Planck-scale coherence, the God Equation launch point, and the unsynced Bekenstein context.",
    'quantum-foam': "Virtual fluctuations at the Planck boundary. The medium baseline noise.",
    gut: "Grand Unification scale. Where the three gauge forces begin to merge.",
    matter: "Matter scale is the densest cluster in the explorer. This is where topology, Koide, the Weinberg angle, and the hierarchy lock together.",
    proton: "Quarks and gluons. QCD confinement and the mass-ratio signals live here.",
    nuclear: "Nuclear structure is treated as amplified matter-scale coherence: confinement and empirical mass-ratio signals live here.",
    atomic: "At atomic scale the framework turns into direct sandbox motion: refraction fields and Bohr quantization become visual and numeric at once.",
    molecular: "The molecular rung is where the effective field story appears: the propagation Lagrangian and the variable-c prediction sit here.",
    virus: "Self-assembly as macroscopic coherence.",
    cellular: "Life enters as active coherence maintenance, still argued and not overstated.",
    neural: "The neural rung marks the interior frontier: consciousness metrics remain open, while self-reference becomes architecture.",
    human: "Human scale turns topology into daily structure, aesthetics, and the compressed 2/3 intuition.",
    planetary: "Planetary scale keeps the same lens law alive: refractive gravity and large-scale propagation remain part of one atlas.",
    stellar: "Stars as immense coherence engines in the refractive medium.",
    galactic: "Spiral arms as standing density waves. Dark matter explained entirely via refractive geometry.",
    cosmic: "The observable universe. The cosmic web as a frozen wave pattern."
  };

  function wrapResultCount(scale) {
    if (!scale.resultIds || scale.resultIds.length === 0) return "No mapped results";
    return scale.resultIds.length + (scale.resultIds.length === 1 ? " mapped result" : " mapped results");
  }

  window.PFExplorer.registerPanel({
    id: "hub",
    mount: function (ctx) {
      var auditedCount = ctx.app.getAuditedResults().length;
      var unsyncedCount = ctx.data.results.filter(function (result) {
        return !!result.unsynced;
      }).length;

      var stage = ctx.stage;
      stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<section class=\"hero-panel\">" +
            "<div class=\"hero-copy\">" +
              "<p class=\"eyebrow\"><span style=\"color:#00cfff; font-family:serif; margin-right:8px;\">↕</span> Scale Stack Navigator</p>" +
              "<p class=\"hero-number\">" + ctx.data.scales.length + "</p>" +
              "<h3><span style=\"color:#ffaa33; font-family:serif; margin-right:8px;\">◈</span> One axiom spine, from Planck boundary to human-scale coherence.</h3>" +
              "<p>Every current result is placed on the same vertical ladder. Click any node to see which claims live there, then jump directly into the deep panels that compute them.</p>" +
              "<p class=\"interaction-cue\"><strong>Interaction:</strong> Orbit the 3D ladder. Click a floating scale node to load its mapped results.</p>" +
              '<p><a href="scale-ladder.html" class="soft-button" style="display:inline-block;margin-top:8px;text-decoration:none;background:var(--propagate);color:var(--void);font-weight:bold;">Launch Full 3D Scale Ladder →</a></p>' +
              '<p><a href="playground.html" class="soft-button" style="display:inline-block;margin-top:6px;text-decoration:none">Propagation Playground →</a></p>' +
            "</div>" +
            "<div class=\"stat-grid\">" +
              "<div class=\"stat-tile\"><strong>" + (ctx.data.panelMeta.length - 1) + "</strong><span>deep panels with live browser math</span></div>" +
              "<div class=\"stat-tile\"><strong>" + ctx.data.results.length + "</strong><span>results visible in the curated snapshot</span></div>" +
              "<div class=\"stat-tile\"><strong>" + auditedCount + "</strong><span>audited results from CLAIMS.md</span></div>" +
              "<div class=\"stat-tile\"><strong>" + unsyncedCount + "</strong><span>unsynced items kept visible without promotion</span></div>" +
            "</div>" +
          "</section>" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\" style=\"position:relative; overflow:hidden;\">" +
              "<div id=\"hub3DContainer\" style=\"width:100%; height:100%; position:absolute; inset:0;\"></div>" +
              "<div class=\"canvas-overlay\" style=\"pointer-events:none;\"></div>" +
              "<div class=\"canvas-legend\">" +
                "<div class=\"legend-item\"><span class=\"legend-swatch\" style=\"background:var(--cyan)\"></span>selected scale</div>" +
                "<div class=\"legend-item\"><span class=\"legend-swatch\" style=\"background:var(--gold)\"></span>connected panel routes</div>" +
                "<div class=\"legend-item\"><span class=\"legend-swatch\" style=\"background:var(--lime)\"></span>audited result markers</div>" +
                "<div class=\"legend-item\"><span class=\"legend-swatch\" style=\"background:rgba(255,255,255,0.3)\"></span>click to select</div>" +
              "</div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"hubDetails\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        container: stage.querySelector("#hub3DContainer"),
        details: stage.querySelector("#hubDetails"),
        selectedScaleId: this.state && this.state.selectedScaleId ? this.state.selectedScaleId : "matter",
        hoveredScaleId: null,
        scene: null,
        camera: null,
        renderer: null,
        composer: null,
        nodes: [],
        particles: null,
        raycaster: new THREE.Raycaster(),
        mouse: new THREE.Vector2(),
        animFrame: null
      };

      this.init3D(ctx);
      this.renderDetails(ctx);

      // Wire the window resize listener to the canonical resize() method
      // and then snap once so the first frame already matches the laid-out
      // DOM instead of init3D's default-size fallback.
      var self = this;
      this.state._resizeHandler = function () { self.resize(ctx); };
      window.addEventListener('resize', this.state._resizeHandler);
      self.resize(ctx);
    },

    init3D: function(ctx) {
      if (!window.THREE) return;
      var w = this.state.container.clientWidth || 400;
      var h = this.state.container.clientHeight || 600;

      var scene = new THREE.Scene();
      scene.background = new THREE.Color(0x020610);
      scene.fog = new THREE.FogExp2(0x020610, 0.04);

      var camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
      camera.position.set(0, 0, 30);

      var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(w, h);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.2;
      this.state.container.appendChild(renderer.domElement);

      var composer;
      try {
          composer = new THREE.EffectComposer(renderer);
          composer.addPass(new THREE.RenderPass(scene, camera));
          var bloom = new THREE.UnrealBloomPass(new THREE.Vector2(w, h), 1.5, 0.4, 0.85);
          composer.addPass(bloom);
      } catch(e) {}

      // Beam
      var beamGeo = new THREE.CylinderGeometry(0.08, 0.08, 40, 16);
      var beamMat = new THREE.MeshBasicMaterial({ 
        color: 0x00cfff, 
        transparent: true, 
        opacity: 0.15,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });
      var beam = new THREE.Mesh(beamGeo, beamMat);
      scene.add(beam);

      // Particles
      var pGeo = new THREE.BufferGeometry();
      var pPos = [];
      for (let i = 0; i < 300; i++) {
          pPos.push((Math.random() - 0.5) * 30, (Math.random() - 0.5) * 40, (Math.random() - 0.5) * 20 - 5);
      }
      pGeo.setAttribute('position', new THREE.Float32BufferAttribute(pPos, 3));
      var pMat = new THREE.PointsMaterial({ 
        color: 0x00e5ff, 
        size: 0.12, 
        transparent: true, 
        opacity: 0.6,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });
      var particles = new THREE.Points(pGeo, pMat);
      scene.add(particles);
      this.state.particles = particles;

      // Nodes
      var scales = ctx.data.scales;
      var logMin = Math.log10(1.616e-35);
      var logMax = 26;
      var range = logMax - logMin;

      scales.forEach((s, i) => {
        var logM = Math.log10(s.meters);
        var normalizedY = ((logM - logMin) / range) * 30 - 15; // Map to -15 to 15 range

        var geo = new THREE.IcosahedronGeometry(0.3 + (i * 0.02), 1);
        var mat = new THREE.MeshStandardMaterial({ 
          color: 0x445566, 
          emissive: 0x112233,
          roughness: 0.2,
          metalness: 0.8
        });
        var mesh = new THREE.Mesh(geo, mat);
        mesh.position.y = normalizedY;
        mesh.userData = { scaleId: s.id, index: i, baseColor: 0x445566, baseEmissive: 0x223344 };
        scene.add(mesh);
        this.state.nodes.push(mesh);

        // Label
        var canvas = document.createElement("canvas");
        canvas.width = 256; canvas.height = 64;
        var tCtx = canvas.getContext("2d");
        tCtx.fillStyle = "#8ba3bd";
        tCtx.font = "bold 24px 'DM Sans', sans-serif";
        tCtx.fillText(s.label.toUpperCase(), 10, 40);
        var tex = new THREE.CanvasTexture(canvas);
        var spriteMat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.7 });
        var sprite = new THREE.Sprite(spriteMat);
        sprite.position.set(2.5, normalizedY, 0);
        sprite.scale.set(5, 1.25, 1);
        scene.add(sprite);
      });

      var ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
      scene.add(ambientLight);
      var dirLight = new THREE.DirectionalLight(0xffffff, 2);
      dirLight.position.set(10, 10, 10);
      scene.add(dirLight);

      this.state.scene = scene;
      this.state.camera = camera;
      this.state.renderer = renderer;
      this.state.composer = composer;

      var self = this;
      this.state.container.addEventListener('mousemove', function(e) {
          var rect = self.state.container.getBoundingClientRect();
          self.state.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
          self.state.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      });

      this.state.container.addEventListener('click', function(e) {
          self.state.raycaster.setFromCamera(self.state.mouse, self.state.camera);
          var intersects = self.state.raycaster.intersectObjects(self.state.nodes);
          if (intersects.length > 0) {
              self.state.selectedScaleId = intersects[0].object.userData.scaleId;
              self.renderDetails(ctx);
          }
      });

      this.animate();
    },

    animate: function() {
        if (!this.state || !this.state.scene) return;
        this.state.animFrame = requestAnimationFrame(this.animate.bind(this));

        var time = Date.now() * 0.001;

        // Raycasting for hover
        this.state.raycaster.setFromCamera(this.state.mouse, this.state.camera);
        var intersects = this.state.raycaster.intersectObjects(this.state.nodes);
        var hoveredId = intersects.length > 0 ? intersects[0].object.userData.scaleId : null;
        
        if (hoveredId !== this.state.hoveredScaleId) {
            this.state.hoveredScaleId = hoveredId;
            this.state.container.style.cursor = hoveredId ? "pointer" : "default";
        }

        // Update nodes
        this.state.nodes.forEach(node => {
            var id = node.userData.scaleId;
            var isSelected = id === this.state.selectedScaleId;
            var isHovered = id === this.state.hoveredScaleId;

            node.rotation.y = time * 0.3 + node.userData.index;
            node.rotation.x = time * 0.2 + node.userData.index * 0.5;

            if (isSelected) {
                node.material.color.setHex(0x00cfff);
                node.material.emissive.setHex(0x0088aa);
                node.scale.setScalar(1.5 + Math.sin(time * 3) * 0.1);
            } else if (isHovered) {
                node.material.color.setHex(0x69ff94);
                node.material.emissive.setHex(0x228844);
                node.scale.setScalar(1.2);
            } else {
                node.material.color.setHex(node.userData.baseColor);
                node.material.emissive.setHex(node.userData.baseEmissive);
                node.scale.setScalar(1.0);
            }
        });

        // Particle motion
        if (this.state.particles) {
            this.state.particles.rotation.y = time * 0.05;
            var pts = this.state.particles.geometry.attributes.position.array;
            for (var i = 0; i < pts.length; i += 3) {
                pts[i+1] += Math.sin(time + i) * 0.01;
            }
            this.state.particles.geometry.attributes.position.needsUpdate = true;
        }

        // Slow camera drift
        this.state.camera.position.y = Math.sin(time * 0.2) * 2;
        this.state.camera.lookAt(0, this.state.camera.position.y, 0);

        if (this.state.composer) {
            this.state.composer.render();
        } else {
            this.state.renderer.render(this.state.scene, this.state.camera);
        }
    },

    unmount: function () {
      if (this.state && this.state._resizeHandler) {
          window.removeEventListener('resize', this.state._resizeHandler);
      }
      if (this.state && this.state.animFrame) {
          cancelAnimationFrame(this.state.animFrame);
      }
      this.state = null;
    },

    resize: function () {
      if (!this.state || !this.state.camera) return;
      var w = this.state.container.clientWidth;
      var h = this.state.container.clientHeight;
      if (w < 2 || h < 2) return;  // DOM not laid out yet; skip cleanly.
      this.state.camera.aspect = w / h;
      this.state.camera.updateProjectionMatrix();
      this.state.renderer.setSize(w, h, false);
      if (this.state.composer) this.state.composer.setSize(w, h);
    },

    renderDetails: function (ctx) {
      var scale = ctx.data.scales.find(function (entry) {
        return entry.id === this.state.selectedScaleId;
      }, this);
      var detail = this.state.details;

      var linkedPanelIds = ctx.app.getLinkedPanelIdsForScale(scale);
      var panelButtons = linkedPanelIds.map(function (panelId) {
        var panel = ctx.data.panelMeta.find(function (p) { return p.id === panelId; });
        return panel ? "<button class=\"soft-button\" type=\"button\" data-navigate=\"" + panelId + "\">Open " + panel.title + "</button>" : "";
      }).join("");

      var noteText = scaleNotes[scale.id] || "Exploring the implications of coherent standing waves at this level of reality.";

      detail.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">" + scale.label + " scale</p>" +
            "<h3>" + scale.metersLabel + "</h3>" +
            "<p>" + noteText + "</p>" +
          "</div>" +
          "<span class=\"scale-pill\">" + wrapResultCount(scale) + "</span>" +
        "</div>" +
        "<div class=\"metric-row\">" +
          "<span class=\"metric-pill\">Characteristic frequency: " + scale.frequencyLabel + "</span>" +
          "<span class=\"metric-pill\">Route thread: " + scale.label + "</span>" +
        "</div>" +
        (linkedPanelIds.length > 0 ? "<div class=\"result-actions\" style=\"margin:14px 0\">" + panelButtons + "</div>" : "") +
        "<div class=\"scale-card-grid\" id=\"hubResultGrid\"></div>";

      var grid = detail.querySelector("#hubResultGrid");
      if (scale.resultIds) {
          scale.resultIds.forEach(function (resultId) {
            var result = ctx.app.getResult(resultId);
            if (result) {
              grid.appendChild(ctx.app.createResultCard(result, { wholeCardFocus: true }));
            }
          });
      }
      ctx.app.syncActiveResultCards();

      // Bind navigation buttons
      Array.prototype.forEach.call(detail.querySelectorAll("[data-navigate]"), function (button) {
        button.addEventListener("click", function () {
          PFExplorer.navigate(button.getAttribute("data-navigate"));
        });
      });
    },

    update: function (ctx, dt, time) {
      // Logic moved to Three.js animate loop
    }
  });
}());