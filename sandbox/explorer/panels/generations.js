(function () {
  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  window.PFExplorer.registerPanel({
    id: "generations",
    mount: function (ctx) {
      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<div class=\"panel-header\">" +
                "<div>" +
                  "<p class=\"eyebrow\">Topology in Motion</p>" +
                  "<h3>One loop closes at 2pi. The matter loop needs 4pi.</h3>" +
                  "<p>The left side keeps the visual phase story moving while the right side computes the generation lock live.</p>" +
                "</div>" +
              "</div>" +
              "<canvas class=\"panel-canvas\" id=\"generationCanvas\"></canvas>" +
              "<div class=\"canvas-overlay\"></div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"generationInfo\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        canvas: ctx.stage.querySelector("#generationCanvas"),
        info: ctx.stage.querySelector("#generationInfo"),
        nValue: 3,
        phaseAngle: 0
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
      var qValue = ctx.utils.qOfN(state.nValue);
      var exact = Math.abs(qValue - 2 / 3) < 1e-9;
      state.info.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">Generation lock</p>" +
            "<h3>Q(N) = 2N / (2N + 3)</h3>" +
            "<p>Slide the generation count and watch the topological numerator compete against the SO(3) denominator.</p>" +
          "</div>" +
          "<span class=\"status-pill status-conditional\">CONDITIONAL</span>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"generationRange\">Generation count N</label>" +
          "<input id=\"generationRange\" type=\"range\" min=\"1\" max=\"5\" step=\"1\" value=\"" + state.nValue + "\">" +
          "<output id=\"generationOut\">N = " + state.nValue + "</output>" +
        "</div>" +
        "<div class=\"formula\">Q(N) = 2N / (2N + 3) = " + qValue.toFixed(6) + "</div>" +
        "<div class=\"note-box story-only\"><strong>Story</strong><p>" + (exact ? "Only N = 3 lands exactly on the Koide target once the physical (2,1) branch and the denominator theorem are granted." : "This N does not hit the exact Koide target. The slider makes the uniqueness visible without hiding the fact that the numerator and denominator bridges are still being finished.") + "</p></div>" +
        "<div class=\"note-box audit-only\"><strong>Audit</strong><p>The panel combines two linked but not fully closed claims: the (2,1) topological weights now sit at partial derivation, and the N = 3 generation lock remains conditional on both the physical-realization theorem and the denominator theorem M = 3.</p></div>" +
        "<div class=\"stat-grid\">" +
          "<div class=\"stat-tile\"><strong>" + (2 * state.nValue) + "</strong><span>fermionic weight</span></div>" +
          "<div class=\"stat-tile\"><strong>3</strong><span>SO(3) denominator</span></div>" +
          "<div class=\"stat-tile\"><strong>" + qValue.toFixed(4) + "</strong><span>computed Q(N)</span></div>" +
          "<div class=\"stat-tile\"><strong>" + (exact ? "match" : "miss") + "</strong><span>vs 2 / 3</span></div>" +
        "</div>" +
        "<div class=\"scale-card-grid\" id=\"generationTokens\"></div>";

      var range = state.info.querySelector("#generationRange");
      range.addEventListener("input", function (event) {
        state.nValue = Number(event.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });

      var tokenRoot = state.info.querySelector("#generationTokens");
      var fermionLine = document.createElement("div");
      fermionLine.className = "scale-card";
      fermionLine.innerHTML = "<strong>Topological tokens</strong><p>" +
        Array.from({ length: 2 * state.nValue }).map(function () { return "<span class=\"metric-pill\" style=\"margin-right:6px\">fermion</span>"; }).join("") +
        Array.from({ length: 3 }).map(function () { return "<span class=\"metric-pill\" style=\"margin-right:6px;color:var(--gold)\">boson</span>"; }).join("") +
        "</p>";
      tokenRoot.appendChild(fermionLine);
    },

    update: function (ctx, dt) {
      var state = this.state;
      var pixelRatio = window.devicePixelRatio;
      var draw = state.canvas.getContext("2d");
      var width = state.canvas.width / pixelRatio;
      var height = state.canvas.height / pixelRatio;
      var cx = width * 0.48;
      var cy = height * 0.52;
      var radius = Math.min(width, height) * 0.2;
      var phase = state.phaseAngle += dt * 0.9;

      draw.save();
      draw.scale(pixelRatio, pixelRatio);
      draw.clearRect(0, 0, width, height);

      draw.strokeStyle = "rgba(255,255,255,0.08)";
      draw.lineWidth = 2;
      draw.beginPath();
      draw.arc(cx, cy, radius * 1.55, 0, Math.PI * 2);
      draw.stroke();

      var sweep = phase % (Math.PI * 4);
      var closeness2Pi = 1 - clamp(Math.abs(sweep - Math.PI * 2) / (Math.PI * 2), 0, 1);
      var closeness4Pi = 1 - clamp(Math.abs(sweep - Math.PI * 4) / (Math.PI * 2), 0, 1);

      draw.lineWidth = 18;
      draw.lineCap = "round";
      draw.strokeStyle = "rgba(0,207,255,0.32)";
      draw.beginPath();
      for (var i = 0; i <= 180; i += 1) {
        var t = i / 180;
        var angle = t * Math.PI * 2;
        var twist = Math.sin(angle + sweep / 2) * radius * 0.16;
        var x = cx + Math.cos(angle) * radius;
        var y = cy + Math.sin(angle) * (radius * 0.72) + twist;
        if (i === 0) {
          draw.moveTo(x, y);
        } else {
          draw.lineTo(x, y);
        }
      }
      draw.stroke();

      draw.fillStyle = "rgba(255,255,255,0.88)";
      draw.font = "13px Trebuchet MS";
      draw.fillText("2pi closes the boson loop", width * 0.08, height * 0.18);
      draw.fillStyle = "rgba(0,207,255,0.94)";
      draw.fillText("4pi closes the fermion loop", width * 0.08, height * 0.24);

      draw.fillStyle = "rgba(255,221,85,0.92)";
      draw.beginPath();
      draw.arc(width * 0.16, height * 0.34, 10 + closeness2Pi * 12, 0, Math.PI * 2);
      draw.fill();
      draw.fillStyle = "rgba(68,255,136,0.92)";
      draw.beginPath();
      draw.arc(width * 0.16, height * 0.42, 10 + closeness4Pi * 12, 0, Math.PI * 2);
      draw.fill();

      var qValue = ctx.utils.qOfN(state.nValue);
      var barX = width * 0.72;
      var barY = height * 0.26;
      var barW = width * 0.16;
      var barH = height * 0.48;
      draw.fillStyle = "rgba(255,255,255,0.06)";
      draw.fillRect(barX, barY, barW, barH);
      draw.fillStyle = "rgba(0,207,255,0.8)";
      draw.fillRect(barX, barY + barH * (1 - qValue), barW, barH * qValue);
      draw.strokeStyle = "rgba(255,221,85,0.9)";
      draw.lineWidth = 2;
      draw.beginPath();
      draw.moveTo(barX - 8, barY + barH * (1 - 2 / 3));
      draw.lineTo(barX + barW + 8, barY + barH * (1 - 2 / 3));
      draw.stroke();
      draw.fillStyle = "rgba(255,255,255,0.9)";
      draw.fillText("Q(N)", barX, barY - 10);
      draw.fillText(qValue.toFixed(4), barX, barY + barH + 22);
      draw.fillStyle = "rgba(255,221,85,0.9)";
      draw.fillText("target 2/3", barX - 12, barY + barH * (1 - 2 / 3) - 10);

      draw.restore();
    }
  });
}());
