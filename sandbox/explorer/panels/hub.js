(function () {
  var scaleNotes = {
    planck: "The ladder starts at the geometry boundary: Planck-scale coherence, the God Equation launch point, and the unsynced Bekenstein context.",
    matter: "Matter scale is the densest cluster in the explorer. This is where topology, Koide, the Weinberg angle, and the hierarchy lock together.",
    nuclear: "Nuclear structure is treated as amplified matter-scale coherence: confinement and empirical mass-ratio signals live here.",
    atomic: "At atomic scale the framework turns into direct sandbox motion: refraction fields and Bohr quantization become visual and numeric at once.",
    molecular: "The molecular rung is where the effective field story appears: the propagation Lagrangian and the variable-c prediction sit here.",
    cellular: "Life enters as active coherence maintenance, still argued and not overstated.",
    neural: "The neural rung marks the interior frontier: consciousness metrics remain open, while self-reference becomes architecture.",
    human: "Human scale turns topology into daily structure, aesthetics, and the compressed 2/3 intuition.",
    planetary: "Planetary scale keeps the same lens law alive: refractive gravity and large-scale propagation remain part of one atlas."
  };

  function nodeRadius(index) {
    return 10 + index * 1.4;
  }

  function wrapResultCount(scale) {
    return scale.resultIds.length + " mapped results";
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
              "<p class=\"eyebrow\">Scale Stack Navigator</p>" +
              "<p class=\"hero-number\">" + ctx.data.scales.length + "</p>" +
              "<h3>One axiom spine, from Planck boundary to human-scale coherence.</h3>" +
              "<p>Every current result is placed on the same vertical ladder. Click any node to see which claims live there, then jump directly into the deep panels that compute them.</p>" +
              '<p><a href="scale-ladder.html" class="soft-button" style="display:inline-block;margin-top:8px;text-decoration:none">Explore Scale Ladder →</a></p>' +
            "</div>" +
            "<div class=\"stat-grid\">" +
              "<div class=\"stat-tile\"><strong>" + (ctx.data.panelMeta.length - 1) + "</strong><span>deep panels with live browser math</span></div>" +
              "<div class=\"stat-tile\"><strong>" + ctx.data.results.length + "</strong><span>results visible in the curated snapshot</span></div>" +
              "<div class=\"stat-tile\"><strong>" + auditedCount + "</strong><span>audited results from CLAIMS.md</span></div>" +
              "<div class=\"stat-tile\"><strong>" + unsyncedCount + "</strong><span>unsynced items kept visible without promotion</span></div>" +
            "</div>" +
          "</section>" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<canvas class=\"panel-canvas\" id=\"hubCanvas\"></canvas>" +
              "<div class=\"canvas-overlay\"></div>" +
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
        canvas: stage.querySelector("#hubCanvas"),
        details: stage.querySelector("#hubDetails"),
        selectedScaleId: this.state && this.state.selectedScaleId ? this.state.selectedScaleId : "matter",
        hoveredScaleId: null,
        stars: Array.from({ length: 90 }).map(function (_, index) {
          return {
            x: (Math.sin(index * 19.2) * 0.5 + 0.5),
            y: (Math.cos(index * 11.7) * 0.5 + 0.5),
            size: 1 + (index % 3)
          };
        }),
        layout: []
      };

      this.state.canvas.addEventListener("click", this.handleClick.bind(this, ctx));
      this.state.canvas.addEventListener("pointermove", this.handlePointerMove.bind(this, ctx));
      this.state.canvas.addEventListener("pointerleave", this.handlePointerLeave.bind(this));
      this.renderDetails(ctx);
    },

    unmount: function () {
      this.state = null;
    },

    resize: function () {
      var canvas = this.state.canvas;
      canvas.width = canvas.clientWidth * window.devicePixelRatio;
      canvas.height = canvas.clientHeight * window.devicePixelRatio;
    },

    handlePointerMove: function (ctx, event) {
      var rect = this.state.canvas.getBoundingClientRect();
      var x = (event.clientX - rect.left) * window.devicePixelRatio;
      var y = (event.clientY - rect.top) * window.devicePixelRatio;
      var hovered = null;
      this.state.layout.forEach(function (node) {
        var distance = Math.hypot(node.x - x, node.y - y);
        if (distance < node.radius + 10 * window.devicePixelRatio) {
          hovered = node.scale.id;
        }
      });
      if (hovered !== this.state.hoveredScaleId) {
        this.state.hoveredScaleId = hovered;
        this.state.canvas.style.cursor = hovered ? "pointer" : "default";
      }
    },

    handlePointerLeave: function () {
      this.state.hoveredScaleId = null;
      this.state.canvas.style.cursor = "default";
    },

    handleClick: function (ctx, event) {
      var rect = this.state.canvas.getBoundingClientRect();
      var x = (event.clientX - rect.left) * window.devicePixelRatio;
      var y = (event.clientY - rect.top) * window.devicePixelRatio;
      var closest = null;
      this.state.layout.forEach(function (node) {
        var distance = Math.hypot(node.x - x, node.y - y);
        if (!closest || distance < closest.distance) {
          closest = { node: node, distance: distance };
        }
      });
      if (closest && closest.distance < 42 * window.devicePixelRatio) {
        this.state.selectedScaleId = closest.node.scale.id;
        this.renderDetails(ctx);
      }
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

      detail.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">" + scale.label + " scale</p>" +
            "<h3>" + scale.metersLabel + "</h3>" +
            "<p>" + scaleNotes[scale.id] + "</p>" +
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
      scale.resultIds.forEach(function (resultId) {
        var result = ctx.app.getResult(resultId);
        if (result) {
          grid.appendChild(ctx.app.createResultCard(result, { wholeCardFocus: true }));
        }
      });
      ctx.app.syncActiveResultCards();

      // Bind navigation buttons
      Array.prototype.forEach.call(detail.querySelectorAll("[data-navigate]"), function (button) {
        button.addEventListener("click", function () {
          PFExplorer.navigate(button.getAttribute("data-navigate"));
        });
      });
    },

    update: function (ctx, dt, time) {
      var canvas = this.state.canvas;
      var width = canvas.width;
      var height = canvas.height;
      var pixelRatio = window.devicePixelRatio;
      var draw = canvas.getContext("2d");
      var beamX = width * 0.3;
      var topY = height * 0.12;
      var bottomY = height * 0.88;
      var scales = ctx.data.scales;

      draw.clearRect(0, 0, width, height);
      draw.save();
      draw.scale(pixelRatio, pixelRatio);
      draw.clearRect(0, 0, width / pixelRatio, height / pixelRatio);
      draw.restore();

      this.state.layout = [];

      // Draw background stars
      draw.fillStyle = "rgba(255,255,255,0.06)";
      this.state.stars.forEach(function (star, index) {
        var twinkle = 0.35 + 0.35 * Math.sin(time * 0.7 + index);
        draw.fillStyle = "rgba(255,255,255," + twinkle.toFixed(3) + ")";
        draw.beginPath();
        draw.arc(star.x * width, star.y * height, star.size * pixelRatio * 0.6, 0, Math.PI * 2);
        draw.fill();
      });

      // Draw central beam
      var beamGradient = draw.createLinearGradient(beamX, topY, beamX, bottomY);
      beamGradient.addColorStop(0, "rgba(0,207,255,0.05)");
      beamGradient.addColorStop(0.5, "rgba(0,207,255,0.42)");
      beamGradient.addColorStop(1, "rgba(255,221,85,0.08)");
      draw.strokeStyle = beamGradient;
      draw.lineWidth = 16 * pixelRatio;
      draw.beginPath();
      draw.moveTo(beamX, topY);
      draw.lineTo(beamX, bottomY);
      draw.stroke();

      draw.strokeStyle = "rgba(255,255,255,0.08)";
      draw.lineWidth = 1 * pixelRatio;
      draw.beginPath();
      draw.moveTo(beamX, topY);
      draw.lineTo(beamX, bottomY);
      draw.stroke();

      var selectedScale = ctx.data.scales.find(function (s) { return s.id === this.state.selectedScaleId; }, this);
      var linkedPanelIds = selectedScale ? ctx.app.getLinkedPanelIdsForScale(selectedScale) : [];

      scales.forEach(function (scale, index) {
        var t = index / (scales.length - 1);
        var y = ctx.utils.lerp(topY, bottomY, t);
        var pulse = 0.5 + 0.5 * Math.sin(time * 1.6 + index * 0.7);
        var isSelected = scale.id === this.state.selectedScaleId;
        var isHovered = scale.id === this.state.hoveredScaleId;
        var scaleLinkedPanels = ctx.app.getLinkedPanelIdsForScale(scale);
        var isLinked = scaleLinkedPanels.length > 0;
        var radius = nodeRadius(index + 1) * pixelRatio;
        var threadX = beamX + (isSelected ? width * 0.21 : width * 0.14) + Math.sin(time + index) * pixelRatio * 7;

        // Draw connection thread to panel nav
        if (isSelected && linkedPanelIds.length > 0) {
          draw.strokeStyle = "rgba(255,221,85,0.35)";
          draw.lineWidth = 2 * pixelRatio;
          draw.setLineDash([8 * pixelRatio, 6 * pixelRatio]);
          draw.beginPath();
          draw.moveTo(beamX + radius, y);
          draw.lineTo(beamX + width * 0.35, y);
          draw.stroke();
          draw.setLineDash([]);
        }

        // Draw scale node
        draw.fillStyle = isSelected ? "rgba(0,207,255,0.16)" : (isHovered ? "rgba(0,207,255,0.08)" : "rgba(255,255,255,0.06)");
        draw.beginPath();
        draw.arc(beamX, y, radius + 10 * pixelRatio * pulse * 0.35, 0, Math.PI * 2);
        draw.fill();

        draw.fillStyle = isSelected ? "#00cfff" : (isHovered ? "#88ddff" : "rgba(255,255,255,0.86)");
        draw.beginPath();
        draw.arc(beamX, y, radius, 0, Math.PI * 2);
        draw.fill();

        // Draw link indicator dot for scales with linked panels
        if (isLinked && !isSelected) {
          draw.fillStyle = "rgba(255,221,85,0.9)";
          draw.beginPath();
          draw.arc(beamX + radius * 1.6, y, 4 * pixelRatio, 0, Math.PI * 2);
          draw.fill();
        }

        draw.fillStyle = isSelected ? "#ffffff" : "rgba(237,246,255,0.75)";
        draw.font = (14 * pixelRatio) + "px Trebuchet MS";
        draw.fillText(scale.label.toUpperCase(), threadX + 12 * pixelRatio, y - 6 * pixelRatio);
        draw.fillStyle = "rgba(154,178,199,0.88)";
        draw.font = (11 * pixelRatio) + "px Trebuchet MS";
        draw.fillText(scale.metersLabel + " / " + scale.frequencyLabel, threadX + 12 * pixelRatio, y + 12 * pixelRatio);

        this.state.layout.push({ scale: scale, x: beamX, y: y, radius: radius });
      }, this);

      draw.restore();
    }
  });
}());
