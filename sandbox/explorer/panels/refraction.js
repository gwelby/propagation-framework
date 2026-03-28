(function () {
  function createDefaultSources(mode) {
    if (mode === "gravity") {
      return [
        { x: -1.2, y: 0.0, strength: 1.45 },
        { x: 2.4, y: -1.1, strength: 0.75 }
      ];
    }
    return [
      { x: -2.2, y: 0.0, strength: 1.1 },
      { x: 1.6, y: 0.0, strength: -0.75 }
    ];
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  window.PFExplorer.registerPanel({
    id: "refraction",
    mount: function (ctx) {
      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<div class=\"panel-header\">" +
                "<div>" +
                  "<p class=\"eyebrow\">Refraction Sandbox</p>" +
                  "<h3>EM and gravity share one local bending story.</h3>" +
                  "<p>Drag sources, add attractors or repellers, and watch eikonal rays and Newton-style probes bend through the same field.</p>" +
                "</div>" +
              "</div>" +
              "<div class=\"controls-row\" id=\"refractionControls\"></div>" +
              "<canvas class=\"panel-canvas\" id=\"refractionCanvas\"></canvas>" +
              "<div class=\"canvas-overlay\"></div>" +
              "<div class=\"canvas-legend\">" +
                "<div class=\"legend-item\"><span class=\"legend-swatch\" style=\"background:var(--cyan)\"></span>eikonal rays</div>" +
                "<div class=\"legend-item\"><span class=\"legend-swatch\" style=\"background:var(--gold)\"></span>Newton overlay</div>" +
                "<div class=\"legend-item\"><span class=\"legend-swatch\" style=\"background:var(--lime)\"></span>source markers</div>" +
              "</div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"refractionInfo\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        canvas: ctx.stage.querySelector("#refractionCanvas"),
        controls: ctx.stage.querySelector("#refractionControls"),
        info: ctx.stage.querySelector("#refractionInfo"),
        mode: "em",
        rayCount: 18,
        energy: 0.78,
        addMode: "attract",
        sources: createDefaultSources("em"),
        draggingIndex: -1,
        dirtyField: true,
        fieldCanvas: document.createElement("canvas"),
        compareOverlay: true,
        world: { minX: -7, maxX: 7, minY: -4.5, maxY: 4.5 }
      };

      this.renderControls(ctx);
      this.renderInfo(ctx);
      this.bindCanvasEvents(ctx);
    },

    unmount: function () {
      this.state = null;
    },

    resize: function () {
      var pixelRatio = window.devicePixelRatio;
      var canvas = this.state.canvas;
      canvas.width = canvas.clientWidth * pixelRatio;
      canvas.height = canvas.clientHeight * pixelRatio;
      this.state.fieldCanvas.width = Math.max(120, Math.floor(canvas.clientWidth / 3));
      this.state.fieldCanvas.height = Math.max(70, Math.floor(canvas.clientHeight / 3));
      this.state.dirtyField = true;
    },

    renderControls: function (ctx) {
      var state = this.state;
      state.controls.innerHTML =
        "<div class=\"control-group\">" +
          "<label for=\"refMode\">Field</label>" +
          "<select id=\"refMode\"><option value=\"em\">EM lens</option><option value=\"gravity\">Gravity lens</option></select>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"refRayCount\">Rays</label>" +
          "<input id=\"refRayCount\" type=\"range\" min=\"8\" max=\"40\" step=\"1\" value=\"" + state.rayCount + "\">" +
          "<output id=\"refRayCountOut\">" + state.rayCount + "</output>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"refEnergy\">Field gain</label>" +
          "<input id=\"refEnergy\" type=\"range\" min=\"0.45\" max=\"1.4\" step=\"0.01\" value=\"" + state.energy + "\">" +
          "<output id=\"refEnergyOut\">" + state.energy.toFixed(2) + "</output>" +
        "</div>" +
        "<button class=\"chip-button\" id=\"refAddAttract\" type=\"button\">Add attractor</button>" +
        "<button class=\"chip-button\" id=\"refAddRepel\" type=\"button\">Add repeller</button>" +
        "<button class=\"chip-button\" id=\"refToggleCompare\" type=\"button\">Overlay on</button>" +
        "<button class=\"chip-button\" id=\"refReset\" type=\"button\">Reset field</button>";

      state.controls.querySelector("#refMode").value = state.mode;

      state.controls.querySelector("#refMode").addEventListener("change", function (event) {
        state.mode = event.target.value;
        state.sources = createDefaultSources(state.mode);
        state.addMode = state.mode === "gravity" ? "attract" : state.addMode;
        state.dirtyField = true;
        PFExplorer.focusResult("forces-refraction", { open: false });
        PFExplorer.state.activePanel.renderInfo(ctx);
      });

      state.controls.querySelector("#refRayCount").addEventListener("input", function (event) {
        state.rayCount = Number(event.target.value);
        state.controls.querySelector("#refRayCountOut").textContent = String(state.rayCount);
      });

      state.controls.querySelector("#refEnergy").addEventListener("input", function (event) {
        state.energy = Number(event.target.value);
        state.controls.querySelector("#refEnergyOut").textContent = state.energy.toFixed(2);
        state.dirtyField = true;
        PFExplorer.state.activePanel.renderInfo(ctx);
      });

      state.controls.querySelector("#refAddAttract").addEventListener("click", function () {
        state.addMode = "attract";
      });

      state.controls.querySelector("#refAddRepel").addEventListener("click", function () {
        state.addMode = "repel";
      });

      state.controls.querySelector("#refToggleCompare").addEventListener("click", function (event) {
        state.compareOverlay = !state.compareOverlay;
        event.target.textContent = state.compareOverlay ? "Overlay on" : "Overlay off";
      });

      state.controls.querySelector("#refReset").addEventListener("click", function () {
        state.sources = createDefaultSources(state.mode);
        state.dirtyField = true;
      });
    },

    renderInfo: function () {
      var state = this.state;
      var result = PFExplorer.getResult("forces-refraction");
      var formula = state.mode === "gravity"
        ? "sandbox lens: n^2 = 1 + gain * sum(M / r)"
        : "sandbox lens: n^2 = gain + sum(q / r)";
      var bridge = state.mode === "gravity"
        ? "Story bridge: the same local refractive gradient that bends EM rays can be re-used at planetary scale."
        : "Story bridge: opposite signs turn the same local lens law from attraction into repulsion.";

      state.info.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">" + (state.mode === "gravity" ? "Gravity mode" : "EM mode") + "</p>" +
            "<h3>" + (state.mode === "gravity" ? "Mass bends the medium." : "Charge bends the medium.") + "</h3>" +
            "<p>" + bridge + "</p>" +
          "</div>" +
          "<span class=\"status-pill status-derived\">" + result.status + "</span>" +
        "</div>" +
        "<div class=\"formula\">" + formula + "</div>" +
        "<div class=\"note-box story-only\"><strong>How to use it</strong><p>Click empty space to place a new source. Drag an existing source to reshape the field. Negative sources only apply in EM mode.</p></div>" +
        "<div class=\"note-box audit-only\"><strong>Audit note</strong><p>Repo truth still lives in the optical metric and Randers / Finsler bridge. This panel is a normalized sandbox, not a scheme-derivation for the full stationary metric.</p></div>" +
        "<div class=\"stat-grid\">" +
          "<div class=\"stat-tile\"><strong>" + state.sources.length + "</strong><span>active sources</span></div>" +
          "<div class=\"stat-tile\"><strong>" + state.rayCount + "</strong><span>eikonal rays</span></div>" +
          "<div class=\"stat-tile\"><strong>" + state.energy.toFixed(2) + "</strong><span>field gain</span></div>" +
          "<div class=\"stat-tile\"><strong>" + (state.compareOverlay ? "on" : "off") + "</strong><span>Newton overlay</span></div>" +
        "</div>";
    },

    bindCanvasEvents: function (ctx) {
      var canvas = this.state.canvas;
      var self = this;
      canvas.addEventListener("pointerdown", function (event) {
        var point = self.screenToWorld(event);
        self.state.draggingIndex = self.findSourceIndex(point.x, point.y);
        if (self.state.draggingIndex < 0) {
          var strength = self.state.mode === "gravity" ? 0.9 : (self.state.addMode === "repel" ? -0.8 : 0.9);
          self.state.sources.push({ x: point.x, y: point.y, strength: strength });
          self.state.dirtyField = true;
        }
        self.renderInfo(ctx);
      });

      canvas.addEventListener("pointermove", function (event) {
        if (self.state.draggingIndex < 0) {
          return;
        }
        var point = self.screenToWorld(event);
        self.state.sources[self.state.draggingIndex].x = clamp(point.x, self.state.world.minX + 0.2, self.state.world.maxX - 0.2);
        self.state.sources[self.state.draggingIndex].y = clamp(point.y, self.state.world.minY + 0.2, self.state.world.maxY - 0.2);
        self.state.dirtyField = true;
      });

      function stopDrag() {
        self.state.draggingIndex = -1;
      }

      canvas.addEventListener("pointerup", stopDrag);
      canvas.addEventListener("pointerleave", stopDrag);
    },

    worldToScreen: function (x, y) {
      var state = this.state;
      var pixelRatio = window.devicePixelRatio;
      var canvas = state.canvas;
      var sx = ((x - state.world.minX) / (state.world.maxX - state.world.minX)) * canvas.width;
      var sy = ((state.world.maxY - y) / (state.world.maxY - state.world.minY)) * canvas.height;
      return { x: sx / pixelRatio, y: sy / pixelRatio };
    },

    screenToWorld: function (event) {
      var rect = this.state.canvas.getBoundingClientRect();
      var nx = (event.clientX - rect.left) / rect.width;
      var ny = (event.clientY - rect.top) / rect.height;
      return {
        x: this.state.world.minX + nx * (this.state.world.maxX - this.state.world.minX),
        y: this.state.world.maxY - ny * (this.state.world.maxY - this.state.world.minY)
      };
    },

    findSourceIndex: function (x, y) {
      var index = -1;
      var best = Infinity;
      this.state.sources.forEach(function (source, sourceIndex) {
        var distance = Math.hypot(source.x - x, source.y - y);
        if (distance < best) {
          best = distance;
          index = sourceIndex;
        }
      });
      return best < 0.45 ? index : -1;
    },

    potentialAt: function (x, y) {
      return this.state.sources.reduce(function (sum, source) {
        var distance = Math.max(0.22, Math.hypot(x - source.x, y - source.y));
        return sum + source.strength / distance;
      }, 0);
    },

    n2At: function (x, y) {
      var potential = this.potentialAt(x, y);
      if (this.state.mode === "gravity") {
        return Math.max(0.08, 1 + this.state.energy * 0.82 * potential);
      }
      return Math.max(0.08, this.state.energy + potential);
    },

    gradAt: function (x, y) {
      var epsilon = 0.035;
      var gx = (this.n2At(x + epsilon, y) - this.n2At(x - epsilon, y)) / (2 * epsilon);
      var gy = (this.n2At(x, y + epsilon) - this.n2At(x, y - epsilon)) / (2 * epsilon);
      return { x: gx, y: gy };
    },

    integrateEikonal: function (x0, y0, theta) {
      var dt = 0.04;
      var path = [];
      var x = x0;
      var y = y0;
      var n = Math.sqrt(this.n2At(x, y));
      var px = n * Math.cos(theta);
      var py = n * Math.sin(theta);
      var i;

      for (i = 0; i < 340; i += 1) {
        n = Math.sqrt(this.n2At(x, y));
        var grad = this.gradAt(x, y);
        path.push({ x: x, y: y });
        x += (px / n) * dt;
        y += (py / n) * dt;
        px += grad.x * 0.18 * dt;
        py += grad.y * 0.18 * dt;

        if (x > this.state.world.maxX || y > this.state.world.maxY || x < this.state.world.minX || y < this.state.world.minY) {
          break;
        }
      }
      return path;
    },

    integrateNewton: function (x0, y0, theta) {
      var dt = 0.032;
      var speed = this.state.mode === "gravity" ? 1.45 : 1.18;
      var x = x0;
      var y = y0;
      var vx = speed * Math.cos(theta);
      var vy = speed * Math.sin(theta);
      var path = [];
      var step;

      for (step = 0; step < 340; step += 1) {
        path.push({ x: x, y: y });
        var ax = 0;
        var ay = 0;
        this.state.sources.forEach(function (source) {
          var dx = x - source.x;
          var dy = y - source.y;
          var r3 = Math.pow(Math.max(0.25, Math.hypot(dx, dy)), 3);
          ax += (-source.strength * dx) / r3;
          ay += (-source.strength * dy) / r3;
        });
        vx += ax * dt * 0.42;
        vy += ay * dt * 0.42;
        x += vx * dt;
        y += vy * dt;
        if (x > this.state.world.maxX || y > this.state.world.maxY || x < this.state.world.minX || y < this.state.world.minY) {
          break;
        }
      }
      return path;
    },

    renderField: function () {
      var state = this.state;
      var canvas = state.fieldCanvas;
      var draw = canvas.getContext("2d");
      var width = canvas.width;
      var height = canvas.height;
      var x;
      var y;

      for (y = 0; y < height; y += 1) {
        for (x = 0; x < width; x += 1) {
          var wx = state.world.minX + (x / width) * (state.world.maxX - state.world.minX);
          var wy = state.world.maxY - (y / height) * (state.world.maxY - state.world.minY);
          var potential = this.potentialAt(wx, wy);
          var tint = clamp(0.5 + potential * 0.18, 0, 1);
          var red = Math.floor(18 + 90 * (1 - tint));
          var green = Math.floor(30 + 105 * tint);
          var blue = Math.floor(56 + 150 * tint);
          draw.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
          draw.fillRect(x, y, 1, 1);
        }
      }
      state.dirtyField = false;
    },

    drawPath: function (draw, path, strokeStyle, lineWidth) {
      if (!path.length) {
        return;
      }
      draw.beginPath();
      path.forEach(function (point, index) {
        var screen = this.worldToScreen(point.x, point.y);
        if (index === 0) {
          draw.moveTo(screen.x, screen.y);
        } else {
          draw.lineTo(screen.x, screen.y);
        }
      }, this);
      draw.strokeStyle = strokeStyle;
      draw.lineWidth = lineWidth;
      draw.stroke();
    },

    update: function (ctx) {
      var state = this.state;
      var pixelRatio = window.devicePixelRatio;
      var draw = state.canvas.getContext("2d");
      var width = state.canvas.width / pixelRatio;
      var height = state.canvas.height / pixelRatio;
      var i;

      if (state.dirtyField) {
        this.renderField();
      }

      draw.save();
      draw.scale(pixelRatio, pixelRatio);
      draw.clearRect(0, 0, width, height);
      draw.drawImage(state.fieldCanvas, 0, 0, width, height);

      draw.strokeStyle = "rgba(255,255,255,0.05)";
      draw.lineWidth = 1;
      for (i = 1; i < 6; i += 1) {
        var xLine = (width / 6) * i;
        draw.beginPath();
        draw.moveTo(xLine, 0);
        draw.lineTo(xLine, height);
        draw.stroke();
      }

      for (i = 0; i < state.rayCount; i += 1) {
        var offset = -3.4 + (6.8 * i) / Math.max(1, state.rayCount - 1);
        var eikonal = this.integrateEikonal(state.world.minX + 0.25, offset, 0);
        this.drawPath(draw, eikonal, "rgba(0,207,255,0.84)", 1.35);
      }

      if (state.compareOverlay) {
        var compareRays = [-1.7, 0, 1.7];
        compareRays.forEach(function (offset) {
          var eikonal = this.integrateEikonal(state.world.minX + 0.25, offset, 0);
          var newton = this.integrateNewton(state.world.minX + 0.25, offset, 0);
          this.drawPath(draw, eikonal, "rgba(255,221,85,0.22)", 2.1);
          this.drawPath(draw, newton, "rgba(255,221,85,0.9)", 1);
        }, this);
      }

      state.sources.forEach(function (source) {
        var screen = this.worldToScreen(source.x, source.y);
        var radius = state.mode === "gravity" ? 9 : 8 + Math.abs(source.strength) * 3;
        draw.fillStyle = source.strength >= 0 ? "rgba(68,255,136,0.94)" : "rgba(255,102,115,0.96)";
        draw.beginPath();
        draw.arc(screen.x, screen.y, radius, 0, Math.PI * 2);
        draw.fill();
        draw.strokeStyle = "rgba(255,255,255,0.9)";
        draw.lineWidth = 1.4;
        draw.stroke();
        draw.fillStyle = "#07111c";
        draw.font = "11px Trebuchet MS";
        draw.fillText(source.strength >= 0 ? "+" : "-", screen.x - 3, screen.y + 4);
      }, this);

      draw.restore();
    }
  });
}());
