(function () {
  window.PFExplorer.registerPanel({
    id: "foundations",
    mount: function (ctx) {
      var stage = ctx.stage;
      stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<section class=\"hero-panel\">" +
            "<div class=\"hero-copy\">" +
              "<p class=\"eyebrow\">Axiomatic Foundations Lab</p>" +
              "<h3>The fundamental primitives of reality.</h3>" +
              "<p>Select an entry concept to visualize its mechanics. The Explorer data layer now carries all 19 canonical definitions; this panel highlights the original four foundation concepts.</p>" +
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
        animFrame: null,
        visuals: {} // store threejs groups
      };

      this.init3D(ctx);
      this.bindEvents(ctx);
      this.renderDetails(ctx);
      this.updateVisuals();
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

      var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(w, h);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      this.state.container.appendChild(renderer.domElement);

      var ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);
      var dirLight = new THREE.DirectionalLight(0xffffff, 1);
      dirLight.position.set(5, 5, 5);
      scene.add(dirLight);

      this.state.scene = scene;
      this.state.camera = camera;
      this.state.renderer = renderer;

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
      var foamMat = new THREE.PointsMaterial({ color: 0x8800ff, size: 0.1, transparent: true, opacity: 0.5 });
      var foam = new THREE.Points(foamGeo, foamMat);
      mediumGroup.add(foam);
      this.state.visuals.medium = mediumGroup;
      scene.add(mediumGroup);

      // Group for Causal Velocity
      var velocityGroup = new THREE.Group();
      var coneGeo = new THREE.ConeGeometry(5, 10, 32, 1, true);
      var coneMat = new THREE.MeshBasicMaterial({ color: 0x00e5ff, transparent: true, opacity: 0.3, wireframe: true });
      var topCone = new THREE.Mesh(coneGeo, coneMat);
      topCone.position.y = 5;
      var botCone = new THREE.Mesh(coneGeo, coneMat);
      botCone.position.y = -5;
      botCone.rotation.x = Math.PI;
      velocityGroup.add(topCone);
      velocityGroup.add(botCone);
      var pointGeo = new THREE.SphereGeometry(0.2, 16, 16);
      var pointMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      var originPoint = new THREE.Mesh(pointGeo, pointMat);
      velocityGroup.add(originPoint);
      this.state.visuals["causal-velocity"] = velocityGroup;
      scene.add(velocityGroup);

      // Group for Coherence
      var coherenceGroup = new THREE.Group();
      var ringCount = 5;
      for (var i=1; i<=ringCount; i++) {
        var rGeo = new THREE.RingGeometry(i*1.5, i*1.5+0.1, 64);
        var rMat = new THREE.MeshBasicMaterial({ color: 0x69ff94, transparent: true, opacity: 1 - (i/ringCount)*0.8, side: THREE.DoubleSide });
        var r = new THREE.Mesh(rGeo, rMat);
        coherenceGroup.add(r);
      }
      this.state.visuals.coherence = coherenceGroup;
      scene.add(coherenceGroup);

      // Group for Time
      var timeGroup = new THREE.Group();
      var spiralGeo = new THREE.BufferGeometry();
      var spiralPos = new Float32Array(500 * 3);
      for (let i=0; i<500; i++) {
        var t = i / 10;
        spiralPos[i*3] = Math.cos(t) * (t*0.2);
        spiralPos[i*3+1] = t * 0.3 - 8;
        spiralPos[i*3+2] = Math.sin(t) * (t*0.2);
      }
      spiralGeo.setAttribute('position', new THREE.BufferAttribute(spiralPos, 3));
      var spiralMat = new THREE.LineBasicMaterial({ color: 0xffd700, transparent: true, opacity: 0.8 });
      var spiral = new THREE.Line(spiralGeo, spiralMat);
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
      if (!this.state || !this.state.scene) return;
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
            var tint = heat > 0.5 ? 0xff4455 : 0x00e5ff;
            child.material.color.setHex(tint);
            child.material.opacity = Math.max(0.05, 0.3 - heatSq * 0.25);
            // Wireframe shatters into noise at collapse
            child.material.wireframe = heat > 0.7;
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

      this.state.renderer.render(this.state.scene, this.state.camera);
    },

    unmount: function () {
      if (this.state && this.state.animFrame) {
          cancelAnimationFrame(this.state.animFrame);
      }
      this.state = null;
    },

    resize: function () {
      if (!this.state || !this.state.camera) return;
      var w = this.state.container.clientWidth;
      var h = this.state.container.clientHeight;
      this.state.camera.aspect = w / h;
      this.state.camera.updateProjectionMatrix();
      this.state.renderer.setSize(w, h);
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
          '<span class="status-pill status-derived">CANONICAL</span>',
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
