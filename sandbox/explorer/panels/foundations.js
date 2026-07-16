(function () {
  window.PFExplorer.registerPanel({
    id: "foundations",
    mount: function (ctx) {
      var stage = ctx.stage;
      stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<section class=\"hero-panel\">" +
            "<div class=\"hero-copy\">" +
              "<p class=\"eyebrow\"><span style=\"color:#00cfff; font-family:serif; margin-right:8px;\">∇</span> Axiomatic Foundations Lab</p>" +
              "<h3>The fundamental primitives of reality.</h3>" +
              "<p>Select an entry concept to visualize its mechanics. These primitives are the only permitted words in the framework. No magic. No exceptions.</p>" +
              "<p class=\"interaction-cue\"><strong>Interaction:</strong> Select an axiom to switch views. Drag the Falsification slider to inject thermal noise and test structural collapse.</p>" +
            "</div>" +
            "<div class=\"stat-grid\">" +
              "<div class=\"stat-tile axiomatic-btn is-active\" data-axiom=\"medium\" style=\"cursor:pointer;\"><strong>1</strong><span>The Medium</span></div>" +
              "<div class=\"stat-tile axiomatic-btn\" data-axiom=\"causal-velocity\" style=\"cursor:pointer;\"><strong>2</strong><span>Causal Velocity</span></div>" +
              "<div class=\"stat-tile axiomatic-btn\" data-axiom=\"coherence\" style=\"cursor:pointer;\"><strong>3</strong><span>Coherence</span></div>" +
              "<div class=\"stat-tile axiomatic-btn\" data-axiom=\"time\" style=\"cursor:pointer;\"><strong>4</strong><span>Time</span></div>" +
            "</div>" +
          "</section>" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\" style=\"position:relative; overflow:hidden;\">" +
              "<div id=\"axiom3DContainer\" style=\"width:100%; height:100%; position:absolute; inset:0;\"></div>" +
              "<div class=\"canvas-overlay\" style=\"pointer-events:none;\"></div>" +
              "<div class=\"falsification-controls\" style=\"position:absolute; bottom:20px; left:20px; right:20px; background:rgba(0,0,0,0.85); padding:16px; border:1px solid rgba(255,71,87,0.4); border-radius:8px; z-index:100; backdrop-filter:blur(4px);\">" +
                "<div style=\"display:flex; justify-content:space-between; margin-bottom:8px;\">" +
                  "<span style=\"color:var(--uncertain); font-weight:600; font-size:11px; letter-spacing:0.05em; text-transform:uppercase;\">Falsification Testing: System Heat</span>" +
                  "<span id=\"heatValueLabel\" style=\"color:var(--text); font-size:12px; font-family:var(--formula);\">0.00 K</span>" +
                "</div>" +
                "<input type=\"range\" id=\"heatSlider\" min=\"0\" max=\"1\" step=\"0.01\" value=\"0\" class=\"premium-slider\" style=\"background:rgba(255,71,87,0.2);\">" +
                "<div style=\"color:var(--muted); font-size:11px; margin-top:8px;\">Inject thermal noise to observe structural collapse. PF predicts that beyond critical heat, coherent structures dissipate.</div>" +
              "</div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"axiomDetails\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        container: stage.querySelector("#axiom3DContainer"),
        details: stage.querySelector("#axiomDetails"),
        heatSlider: stage.querySelector("#heatSlider"),
        heatValueLabel: stage.querySelector("#heatValueLabel"),
        selectedAxiomId: "medium",
        heat: 0,
        scene: null,
        camera: null,
        renderer: null,
        composer: null,
        animFrame: null,
        visuals: {} // store threejs groups
      };

      this.init3D(ctx);
      this.bindEvents(ctx);
      this.renderDetails(ctx);
      this.updateVisuals();

      // Wire the window resize listener to the canonical resize() method
      // and then snap once so the first frame already matches the laid-out
      // DOM instead of init3D's default-size fallback.
      var self = this;
      this.state._resizeHandler = function () { self.resize(ctx); };
      window.addEventListener('resize', this.state._resizeHandler);
      self.resize(ctx);
    },

    bindEvents: function(ctx) {
      var self = this;
      var buttons = ctx.stage.querySelectorAll(".axiomatic-btn");
      Array.prototype.forEach.call(buttons, function(btn) {
        btn.addEventListener("click", function() {
          Array.prototype.forEach.call(buttons, function(b) { b.classList.remove("is-active"); });
          btn.classList.add("is-active");
          self.state.selectedAxiomId = btn.getAttribute("data-axiom");
          self.renderDetails(ctx);
          self.updateVisuals();
        });
      });

      if (this.state.heatSlider) {
        this.state.heatSlider.addEventListener("input", function(e) {
          self.state.heat = parseFloat(e.target.value);
          var h = self.state.heat;
          // Dynamic label: 0-0.3 = Stable, 0.3-0.6 = Critical, 0.6+ = Collapse
          var label = h < 0.3 ? 'Stable' : h < 0.6 ? 'Critical ⚠' : 'COLLAPSE ✗';
          var tempStr = (h * 100).toFixed(2) + ' K  —  ' + label;
          if (self.state.heatValueLabel) {
            self.state.heatValueLabel.textContent = tempStr;
            self.state.heatValueLabel.style.color = h < 0.3 ? 'var(--text)' : h < 0.6 ? '#ffaa33' : '#ff4455';
          }
        });
      }
    },

    init3D: function(ctx) {
      if (!window.THREE) return;
      var w = this.state.container.clientWidth || 400;
      var h = this.state.container.clientHeight || 600;

      var scene = new THREE.Scene();
      scene.background = new THREE.Color(0x020408);

      var camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
      camera.position.set(0, 0, 20);

      var renderer;
      try {
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      } catch (e) {
        console.warn("WebGL not supported, running in fallback mode:", e);
        this.state.container.innerHTML = '';
        var fallbackDiv = document.createElement('div');
        fallbackDiv.className = 'webgl-fallback';
        fallbackDiv.style.cssText = 'display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; min-height: 250px; border: 1px dashed rgba(232, 240, 255, 0.2); border-radius: 8px; background: rgba(9, 21, 37, 0.2); color: rgba(232, 240, 255, 0.8); text-align: center; padding: 20px; box-sizing: border-box;';
        fallbackDiv.innerHTML = '<h4 style="margin: 0 0 8px 0; color: #00cfff;">WebGL Not Supported</h4><p style="margin: 0; font-size: 12px; color: var(--muted); max-width: 280px; line-height: 1.4;">Foundational Axioms and mathematical structures are calculated and plotted below in the definitions panel.</p>';
        this.state.container.appendChild(fallbackDiv);
        this.state._isFallback = true;
        return;
      }
      renderer.setSize(w, h);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.2;
      this.state.container.appendChild(renderer.domElement);

      var composer = null;
      try {
        composer = new THREE.EffectComposer(renderer);
        composer.addPass(new THREE.RenderPass(scene, camera));
        var bloom = new THREE.UnrealBloomPass(new THREE.Vector2(w, h), 1.5, 0.4, 0.85);
        composer.addPass(bloom);
      } catch(e) {}

      var ambientLight = new THREE.AmbientLight(0x222244, 1.0);
      scene.add(ambientLight);
      var dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
      dirLight.position.set(5, 5, 5);
      scene.add(dirLight);

      this.state.scene = scene;
      this.state.camera = camera;
      this.state.renderer = renderer;
      this.state.composer = composer;

      // Group for The Medium
      var mediumGroup = new THREE.Group();
      var foamGeo = new THREE.BufferGeometry();
      var foamPos = new Float32Array(3000 * 3);
      for (let i=0; i<3000; i++) {
        foamPos[i*3] = (Math.random()-0.5)*30;
        foamPos[i*3+1] = (Math.random()-0.5)*30;
        foamPos[i*3+2] = (Math.random()-0.5)*10;
      }
      foamGeo.setAttribute('position', new THREE.BufferAttribute(foamPos, 3));
      var foamMat = new THREE.PointsMaterial({ 
        color: 0x8800ff, 
        size: 0.15, 
        transparent: true, 
        opacity: 0.8,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });
      var foam = new THREE.Points(foamGeo, foamMat);
      mediumGroup.add(foam);
      this.state.visuals.medium = mediumGroup;
      scene.add(mediumGroup);

      // Group for Causal Velocity
      var velocityGroup = new THREE.Group();
      var coneGeo = new THREE.ConeGeometry(5, 10, 32, 1, true);
      var coneMatTop = new THREE.MeshBasicMaterial({ color: 0x00cfff, transparent: true, opacity: 0.2, wireframe: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false });
      var coneMatBot = new THREE.MeshBasicMaterial({ color: 0xff00ff, transparent: true, opacity: 0.2, wireframe: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false });
      
      var topCone = new THREE.Mesh(coneGeo, coneMatTop);
      topCone.position.y = 5;
      var botCone = new THREE.Mesh(coneGeo, coneMatBot);
      botCone.position.y = -5;
      botCone.rotation.x = Math.PI;
      
      var topConeWire = new THREE.Mesh(coneGeo, new THREE.MeshBasicMaterial({ color: 0x00cfff, wireframe: true, transparent: true, opacity: 0.15 }));
      topCone.add(topConeWire);
      var botConeWire = new THREE.Mesh(coneGeo, new THREE.MeshBasicMaterial({ color: 0xff00ff, wireframe: true, transparent: true, opacity: 0.15 }));
      botCone.add(botConeWire);

      velocityGroup.add(topCone);
      velocityGroup.add(botCone);
      
      var coreGeo = new THREE.CylinderGeometry(0.05, 0.05, 20, 8);
      var coreMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 });
      var coreBeam = new THREE.Mesh(coreGeo, coreMat);
      velocityGroup.add(coreBeam);

      var pointGeo = new THREE.SphereGeometry(0.3, 32, 32);
      var pointMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      var originPoint = new THREE.Mesh(pointGeo, pointMat);
      velocityGroup.add(originPoint);
      this.state.visuals["causal-velocity"] = velocityGroup;
      scene.add(velocityGroup);

      // Group for Coherence
      var coherenceGroup = new THREE.Group();
      var ringCount = 6;
      for (var i=1; i<=ringCount; i++) {
        var rGeo = new THREE.TorusGeometry(i*1.5, 0.1, 16, 100);
        var rMat = new THREE.MeshStandardMaterial({ 
          color: 0x69ff94, 
          emissive: 0x228844,
          transparent: true, 
          opacity: 1 - (i/ringCount)*0.7, 
          roughness: 0.2,
          metalness: 0.8
        });
        var r = new THREE.Mesh(rGeo, rMat);
        coherenceGroup.add(r);
      }
      this.state.visuals.coherence = coherenceGroup;
      scene.add(coherenceGroup);

      // Group for Time
      var timeGroup = new THREE.Group();
      var spiralPoints = [];
      for (let i=0; i<300; i++) {
        var t = i / 10;
        spiralPoints.push(new THREE.Vector3(
          Math.cos(t) * (t*0.2),
          t * 0.3 - 5,
          Math.sin(t) * (t*0.2)
        ));
      }
      var curve = new THREE.CatmullRomCurve3(spiralPoints);
      var tubeGeo = new THREE.TubeGeometry(curve, 300, 0.15, 8, false);
      var tubeMat = new THREE.MeshStandardMaterial({ 
        color: 0xffaa00, 
        emissive: 0xff5500,
        emissiveIntensity: 0.5,
        transparent: true, 
        opacity: 0.9,
        roughness: 0.2,
        metalness: 0.8
      });
      var spiral = new THREE.Mesh(tubeGeo, tubeMat);
      timeGroup.add(spiral);
      this.state.visuals.time = timeGroup;
      scene.add(timeGroup);

      this.animate();
    },

    updateVisuals: function() {
      if (!this.state.scene) return;
      var active = this.state.selectedAxiomId;
      Object.keys(this.state.visuals).forEach(function(key) {
        this.state.visuals[key].visible = (key === active);
      }, this);
    },

    animate: function() {
      if (!this.state || !this.state.scene || this.state._isFallback) return;
      this.state.animFrame = requestAnimationFrame(this.animate.bind(this));
      var time = Date.now() * 0.001;
      var heat = this.state.heat || 0;
      // Collapse is non-linear — quadratic response so the instrument "feels" like a phase transition
      var heatSq = heat * heat;
      var isCollapsed = heat > 0.85;

      // --- Medium: quantum foam ---
      if (this.state.visuals.medium && this.state.visuals.medium.visible) {
        this.state.visuals.medium.rotation.y = time * 0.1 * (1 + heat * 2);
        var pts = this.state.visuals.medium.children[0];
        var mPos = pts.geometry.attributes.position.array;
        for (var i = 0; i < mPos.length; i += 3) {
          var baseWave = Math.sin(time * 2 + mPos[i] * 0.3) * 0.015;
          // At high heat: large random kicks that scatter particles far from origin
          var chaos = (Math.random() - 0.5) * heatSq * 4.5;
          mPos[i]   += baseWave + chaos;
          mPos[i+1] += baseWave + chaos * 0.8;
          mPos[i+2] += (Math.random() - 0.5) * heatSq * 2.0;
          // At collapse, drift particles toward screen edges (dissipation)
          if (isCollapsed) {
            mPos[i]   *= 1.0012;
            mPos[i+1] *= 1.0012;
          }
        }
        pts.geometry.attributes.position.needsUpdate = true;
        // Opacity degrades with heat
        pts.material.opacity = Math.max(0.05, 0.5 - heatSq * 0.45);
      }

      // --- Causal Velocity: light-cone ---
      if (this.state.visuals['causal-velocity'] && this.state.visuals['causal-velocity'].visible) {
        var cv = this.state.visuals['causal-velocity'];
        cv.rotation.y = time * 0.5;
        // Shake intensity scales with heat^2
        var shakeAmp = heatSq * 1.8;
        cv.position.set(
          (Math.random() - 0.5) * shakeAmp,
          (Math.random() - 0.5) * shakeAmp * 0.5,
          0
        );
        // At high heat, cone materials go red then transparent (coherence lost)
        cv.children.forEach(function(child) {
          if (child.material) {
            var tint = heat > 0.5 ? 0xff4455 : (child.position.y > 0 ? 0x00cfff : 0xff00ff);
            if (child.material.color) {
              child.material.color.setHex(tint);
            }
            if (child.material.wireframe !== undefined) {
              child.material.opacity = Math.max(0.05, 0.3 - heatSq * 0.25);
              child.material.wireframe = child.material.wireframe || (heat > 0.7);
            }
          }
        });
        cv.rotation.z = isCollapsed ? Math.random() * Math.PI : 0;
      }

      // --- Coherence: concentric rings ---
      if (this.state.visuals.coherence && this.state.visuals.coherence.visible) {
        var cg = this.state.visuals.coherence;
        cg.rotation.x = Math.PI / 2 - 0.2;
        cg.children.forEach(function(ring, idx) {
          // Base pulsation
          var pulse = 1 + Math.sin(time * 3 - idx) * 0.05;
          // At low heat: rings breathe coherently
          // At high heat: rings decohere — each vibrates independently and chaotically
          var decohere = (Math.random() - 0.5) * heatSq * 2.5;
          var scale = pulse + decohere;
          ring.scale.set(scale, scale, 1);
          // Phase destruction: rings drift off-axis
          ring.position.x = (Math.random() - 0.5) * heatSq * 3;
          ring.position.y = (Math.random() - 0.5) * heatSq * 3;
          // Opacity collapses — coherence literally fades out
          ring.material.opacity = Math.max(0.02, (1 - (idx / 5) * 0.8) - heatSq * 0.9);
          // Color shifts to red at high heat (energy without structure)
          if (heat > 0.5) {
            ring.material.color.setRGB(
              Math.min(1, 0.4 + heat),
              Math.max(0, 1 - heat * 1.2),
              Math.max(0, 0.6 - heat)
            );
          }
        });
      }

      // --- Time: Cauchy spiral ---
      if (this.state.visuals.time && this.state.visuals.time.visible) {
        var tg = this.state.visuals.time;
        tg.rotation.y = time * (1 + heatSq * 3);
        // Spiral fractures: random axis tilt at high heat
        tg.rotation.x = heatSq * (Math.random() - 0.5) * 1.2;
        tg.rotation.z = heatSq * (Math.random() - 0.5) * 0.8;
        // At collapse, spiral loses its structure and looks like random noise
        var line = tg.children[0];
        if (line && line.material) {
          line.material.opacity = Math.max(0.05, 0.8 - heatSq * 0.75);
        }
      }

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
      if (!this.state || !this.state.camera || this.state._isFallback) return;
      var w = this.state.container.clientWidth;
      var h = this.state.container.clientHeight;
      if (w < 2 || h < 2) return;  // DOM not laid out yet; skip cleanly.
      this.state.camera.aspect = w / h;
      this.state.camera.updateProjectionMatrix();
      this.state.renderer.setSize(w, h, false);
      if (this.state.composer) {
        this.state.composer.setSize(w, h);
      }
    },

    renderDetails: function(ctx) {
      var defId = this.state.selectedAxiomId;
      var data = window.PFClaimsData || {};
      var def = (data.DEFINITIONS || []).find(function(d) { return d.id === defId; });

      if (!def) {
        this.state.details.innerHTML = '<div class="panel-header"><p>Select an axiom.</p></div>';
        return;
      }

      var auditSection = '';
      if (ctx.state.mode === 'audit') {
        auditSection = [
          '<div class="audit-only note-box" style="margin-top:16px; display:block;">',
            '<strong>Audit Boundary</strong>',
            '<p>' + (def.auditLine || '') + '</p>',
            def.notThis ? '<p class="drawer-falsifier"><strong>Not this:</strong> ' + def.notThis + '</p>' : '',
          '</div>',
        ].join('');
      }

      // Wrong intuition callout for select definitions
      var wiSection = '';
      if (def.id === 'medium') {
        wiSection = window.PFExplorer.renderWrongIntuition({
          intuition: 'Space is empty — a passive backdrop that things move through.',
          reality: 'The Medium is the active substrate of reality. It propagates, constrains, and shapes everything. \u201cEmpty space\u201d is not empty — it is the Medium at rest.',
          detail: 'All three Axioms are properties of the Medium. Remove the Medium and the framework has nothing to act on.',
        });
      } else if (def.id === 'coherence') {
        wiSection = window.PFExplorer.renderWrongIntuition({
          intuition: 'Coherence is a single thing you either have or don\u2019t — like being organized.',
          reality: 'Coherence has at least four technically distinct layers (phase, quantum, structural, self-referential). A laser and a living cell are not coherent in the same sense.',
          detail: def.notThis || '',
        });
      }

      this.state.details.innerHTML = [
        '<div class="panel-header">',
          '<div>',
            '<p class="eyebrow">Canonical Definition</p>',
            '<h3>' + def.title + '</h3>',
            '<p class="drawer-quote">\u201c' + (def.oneLiner || '') + '\u201d</p>',
          '</div>',
          '<span class="status-pill status-derived">' + (def.auditLine || 'CANONICAL') + '</span>',
        '</div>',
        '<div style="padding:0 var(--spacing-4)">',
          '<p>' + (def.storyLine || '') + '</p>',
          wiSection,
          auditSection,
          def.dependencies && def.dependencies.length ? [
            '<div class="obs-pc-sources" style="margin-top:16px;">',
              '<span style="font-size:11px; color:var(--muted); margin-right:8px;">Dependencies:</span>',
              def.dependencies.map(function(dep) {
                return '<button class="obs-source-pill" onclick="PFExplorer.focusDefinition(\'' + dep + '\')">'
                  + dep + '</button>';
              }).join(''),
            '</div>',
          ].join('') : '',
        '</div>',
      ].join('');

      if (ctx.state.mode === 'math' && window.CommandBar) {
        CommandBar.triggerTypeset();
      }
    },

    update: function (ctx, dt, time) {
      // Logic moved to Three.js animate loop
    }
  });
}());
