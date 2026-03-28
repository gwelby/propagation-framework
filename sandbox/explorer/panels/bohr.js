(function () {
  function nearestInteger(value) {
    return Math.round(value);
  }

  window.PFExplorer.registerPanel({
    id: "bohr",
    mount: function (ctx) {
      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<div class=\"panel-header\">" +
                "<div>" +
                  "<p class=\"eyebrow\">Phase Closure Orbit</p>" +
                  "<h3>Only integer winding survives. Everything else fades.</h3>" +
                  "<p>The slider moves through continuous k-like radii. The panel shows how stable orbits glow exactly at integer winding.</p>" +
                "</div>" +
              "</div>" +
              "<canvas class=\"panel-canvas\" id=\"bohrCanvas\"></canvas>" +
              "<div class=\"canvas-overlay\"></div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"bohrInfo\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        canvas: ctx.stage.querySelector("#bohrCanvas"),
        info: ctx.stage.querySelector("#bohrInfo"),
        kLike: 1,
        phase: 0
      };

      this.renderInfo(ctx);
    },

    unmount: function () {
      this.state = null;
    },

    resize: function () {
      var pixelRatio = window.devicePixelRatio;
      this.state.canvas.width = this.state.canvas.clientWidth * pixelRatio;
      this.state.canvas.height = this.state.canvas.clientHeight * pixelRatio;
    },

    renderInfo: function (ctx) {
      var state = this.state;
      var nearest = nearestInteger(state.kLike);
      var radius = 2 * state.kLike * state.kLike;
      var energy = -1 / (4 * state.kLike * state.kLike);
      var phaseValue = 2 * Math.PI * state.kLike;
      var mismatch = Math.abs(state.kLike - nearest);
      var errorPct = nearest === state.kLike ? 0 : Math.abs(phaseValue - 2 * Math.PI * nearest) / (2 * Math.PI * nearest) * 100;
      state.info.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">Integer winding</p>" +
            "<h3>k = " + state.kLike.toFixed(2) + "</h3>" +
            "<p>The panel uses the exact repo formulas so integer k reproduces zero closure error rather than approximating it numerically.</p>" +
          "</div>" +
          "<span class=\"status-pill status-derived\">DERIVED</span>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"bohrK\">Continuous winding k</label>" +
          "<input id=\"bohrK\" type=\"range\" min=\"0.8\" max=\"4.2\" step=\"0.01\" value=\"" + state.kLike + "\">" +
          "<output id=\"bohrKOut\">k = " + state.kLike.toFixed(2) + "</output>" +
        "</div>" +
        "<div class=\"metric-row\">" +
          "<button class=\"chip-button\" type=\"button\" data-k=\"1\">k = 1</button>" +
          "<button class=\"chip-button\" type=\"button\" data-k=\"2\">k = 2</button>" +
          "<button class=\"chip-button\" type=\"button\" data-k=\"3\">k = 3</button>" +
          "<button class=\"chip-button\" type=\"button\" data-k=\"4\">k = 4</button>" +
        "</div>" +
        "<div class=\"formula\">r_k = 2k^2, E_k = -1 / (4k^2), integral n ds = 2pi k</div>" +
        "<div class=\"stat-grid\">" +
          "<div class=\"stat-tile\"><strong>" + radius.toFixed(3) + "</strong><span>radius</span></div>" +
          "<div class=\"stat-tile\"><strong>" + energy.toFixed(5) + "</strong><span>energy</span></div>" +
          "<div class=\"stat-tile\"><strong>" + phaseValue.toFixed(4) + "</strong><span>phase accumulation</span></div>" +
          "<div class=\"stat-tile\"><strong>" + (mismatch < 1e-8 ? "0.0000%" : errorPct.toFixed(3) + "%") + "</strong><span>closure error</span></div>" +
        "</div>" +
        "<div class=\"note-box story-only\"><strong>Story</strong><p>" + (mismatch < 0.015 ? "The orbit is essentially locked. The glow stays bright because the phase closes on itself." : "The orbit misses closure. The panel fades the trajectory because the phase does not come home cleanly.") + "</p></div>" +
        "<div class=\"note-box audit-only\"><strong>Audit</strong><p>At integer k this panel reports exact formula-level closure, not numerical integration error. That keeps the displayed 0.0000% aligned with the repo claim.</p></div>";

      state.info.querySelector("#bohrK").addEventListener("input", function (event) {
        state.kLike = Number(event.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      Array.prototype.forEach.call(state.info.querySelectorAll("[data-k]"), function (button) {
        button.addEventListener("click", function () {
          state.kLike = Number(button.getAttribute("data-k"));
          PFExplorer.state.activePanel.renderInfo(ctx);
        });
      });
    },

    update: function () {
      var state = this.state;
      var pixelRatio = window.devicePixelRatio;
      var draw = state.canvas.getContext("2d");
      var width = state.canvas.width / pixelRatio;
      var height = state.canvas.height / pixelRatio;
      var cx = width * 0.42;
      var cy = height * 0.54;
      var base = Math.min(width, height) * 0.05;
      var orbitRadius = base * (2 * state.kLike * state.kLike);
      var nearest = nearestInteger(state.kLike);
      var stable = Math.abs(state.kLike - nearest) < 0.02;
      var glow = stable ? 1 : Math.max(0.18, 1 - Math.abs(state.kLike - nearest) * 4);
      state.phase += 0.9 * (stable ? 1 : 0.75) / Math.max(1, state.kLike);
      var angle = state.phase;

      draw.save();
      draw.scale(pixelRatio, pixelRatio);
      draw.clearRect(0, 0, width, height);

      [1, 2, 3, 4].forEach(function (k) {
        var ringRadius = base * (2 * k * k);
        draw.strokeStyle = k === nearest ? "rgba(255,221,85,0.34)" : "rgba(255,255,255,0.08)";
        draw.lineWidth = k === nearest ? 2.2 : 1;
        draw.beginPath();
        draw.arc(cx, cy, ringRadius, 0, Math.PI * 2);
        draw.stroke();
      });

      draw.fillStyle = "rgba(255,221,85,0.95)";
      draw.beginPath();
      draw.arc(cx, cy, 10, 0, Math.PI * 2);
      draw.fill();

      draw.strokeStyle = "rgba(0,207,255," + (0.3 + 0.6 * glow).toFixed(3) + ")";
      draw.lineWidth = 3;
      draw.beginPath();
      draw.arc(cx, cy, orbitRadius, 0, Math.PI * 2);
      draw.stroke();

      if (!stable) {
        draw.setLineDash([8, 10]);
        draw.strokeStyle = "rgba(255,102,115,0.65)";
        draw.lineWidth = 2;
        draw.beginPath();
        draw.arc(cx, cy, orbitRadius + 8, 0, Math.PI * 2);
        draw.stroke();
        draw.setLineDash([]);
      }

      var px = cx + Math.cos(angle) * orbitRadius;
      var py = cy + Math.sin(angle) * orbitRadius;
      draw.fillStyle = stable ? "rgba(68,255,136,0.98)" : "rgba(255,102,115,0.95)";
      draw.beginPath();
      draw.arc(px, py, 9, 0, Math.PI * 2);
      draw.fill();

      draw.fillStyle = "rgba(255,255,255,0.9)";
      draw.font = "14px Trebuchet MS";
      draw.fillText("nearest stable k = " + nearest, width * 0.08, height * 0.18);
      draw.fillText(stable ? "phase closes" : "phase leaks", width * 0.08, height * 0.24);

      draw.restore();
    }
  });
}());
