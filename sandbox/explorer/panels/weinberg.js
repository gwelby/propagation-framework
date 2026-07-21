(function () {
  window.PFExplorer.registerPanel({
    id: "weinberg",
    mount: function (ctx) {
      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<div class=\"panel-header\">" +
                "<div>" +
                  "<p class=\"eyebrow\"><span style=\"color:#44ff88; font-family:serif; margin-right:8px;\">θ</span> Casimir Polynomial</p>" +
                  "<h3><span style=\"color:#00cfff; font-family:serif; margin-right:8px;\">∇</span> Positive roots for j = 1/2 and j = 1 generate the mixing angle.</h3>" +
                  "<p>The Casimir ratio selects the physical electroweak mixing angle sin²θ_W. The same browser panel shows the raw polynomial, the chosen roots, and the ratio used in the repo derivation.</p>" +
                  "<p class=\"interaction-cue\"><strong>Interaction:</strong> Follow the roots and the mixing angle derivation. Review the explicit scheme caveat in the Evidence Drawer.</p>" +
                "</div>" +
              "</div>" +
              "<canvas class=\"panel-canvas\" id=\"weinbergCanvas\"></canvas>" +
              "<div class=\"canvas-overlay\"></div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"weinbergInfo\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        canvas: ctx.stage.querySelector("#weinbergCanvas"),
        info: ctx.stage.querySelector("#weinbergInfo")
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
      var xHalf = ctx.utils.casimirRoot(0.5);
      var xOne = ctx.utils.casimirRoot(1);
      var prediction = 1 - xHalf / xOne;
      var reference = 0.22337;
      var sigma = 0.13;
      var error = Math.abs(prediction - reference) / sigma;
      var weinbergResult = ctx.app.getResult('weinberg-angle') || {};
      this.state.info.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">Axiom 3b</p>" +
            "<h3>sin^2(theta_W) = " + prediction.toFixed(5) + "</h3>" +
            "<p>Minimal winding selects the primitive branch. The panel keeps the scheme caveat visible instead of pretending the derivation is more complete than the repo says.</p>" +
          "</div>" +
          "<span class=\"status-pill " + (weinbergResult.statusClass || 'status-unavailable') + "\" data-claim-id=\"weinberg-angle\">" + (weinbergResult.badge || (weinbergResult.status && weinbergResult.status.label ? weinbergResult.status.label : 'UNAVAILABLE')) + "</span>" +
        "</div>" +
        ctx.app.renderWrongIntuition(ctx.app.getResult('weinberg-angle')) +
        "<div class=\"formula\">x^2 + C2 x - C2 = 0, then 1 - x_+(1/2) / x_+(1)</div>" +
        ctx.app.compareBarHtml(prediction, reference, error, 0.2222, 0.2238) +
        "<div class=\"metric-row\">" +
          "<span class=\"metric-pill\">prediction = " + prediction.toFixed(5) + "</span>" +
          "<span class=\"metric-pill\">quoted PDG on-shell = 0.22337</span>" +
          "<span class=\"metric-pill\">match = " + sigma.toFixed(2) + " sigma in CLAIMS.md</span>" +
        "</div>" +
        "<div class=\"note-box story-only\"><strong>Story</strong><p>The ratio is small, but the structure is sharp: two positive roots, one subtraction, one electroweak angle.</p></div>" +
        "<div class=\"note-box audit-only\"><strong>Audit</strong><p>The Casimir ratio gives 0.22310 exactly, matched to the quoted on-shell PDG value at 0.13σ. Scheme selection (on-shell vs MS-bar) remains open. See the authority record for current status.</p></div>" +
        "<div class=\"stat-grid\">" +
          "<div class=\"stat-tile\"><strong>" + xHalf.toFixed(6) + "</strong><span>x_+(1/2)</span></div>" +
          "<div class=\"stat-tile\"><strong>" + xOne.toFixed(6) + "</strong><span>x_+(1)</span></div>" +
          "<div class=\"stat-tile\"><strong>k = 1</strong><span>minimal winding branch</span></div>" +
          "<div class=\"stat-tile\"><strong>on-shell</strong><span>comparison scheme in current repo copy</span></div>" +
        "</div>";
      ctx.app.syncActiveResultCards();
    },

    update: function (ctx) {
      var pixelRatio = window.devicePixelRatio;
      var draw = this.state.canvas.getContext("2d");
      var width = this.state.canvas.width / pixelRatio;
      var height = this.state.canvas.height / pixelRatio;
      var padding = { left: width * 0.1, right: width * 0.08, top: height * 0.16, bottom: height * 0.16 };
      var plotW = width - padding.left - padding.right;
      var plotH = height - padding.top - padding.bottom;
      var xHalf = ctx.utils.casimirRoot(0.5);
      var xOne = ctx.utils.casimirRoot(1);

      function mapX(x) {
        return padding.left + x * plotW;
      }

      function mapY(y) {
        return padding.top + (1 - (y + 2.2) / 3.2) * plotH;
      }

      draw.save();
      draw.scale(pixelRatio, pixelRatio);
      draw.clearRect(0, 0, width, height);
      draw.strokeStyle = "rgba(255,255,255,0.08)";
      draw.lineWidth = 1;
      draw.beginPath();
      draw.moveTo(padding.left, mapY(0));
      draw.lineTo(width - padding.right, mapY(0));
      draw.moveTo(padding.left, padding.top);
      draw.lineTo(padding.left, height - padding.bottom);
      draw.stroke();

      [["rgba(0,207,255,0.95)", 0.75, xHalf], ["rgba(255,221,85,0.92)", 2, xOne]].forEach(function (entry) {
        var color = entry[0];
        var c2 = entry[1];
        var root = entry[2];
        draw.beginPath();
        for (var i = 0; i <= 160; i += 1) {
          var x = i / 160;
          var y = x * x + c2 * x - c2;
          if (i === 0) {
            draw.moveTo(mapX(x), mapY(y));
          } else {
            draw.lineTo(mapX(x), mapY(y));
          }
        }
        draw.strokeStyle = color;
        draw.lineWidth = 2.4;
        draw.stroke();
        draw.fillStyle = color;
        draw.beginPath();
        draw.arc(mapX(root), mapY(0), 7, 0, Math.PI * 2);
        draw.fill();
      });

      draw.fillStyle = "rgba(255,255,255,0.92)";
      draw.font = "13px Trebuchet MS";
      draw.fillText("j = 1/2", mapX(xHalf) - 24, mapY(0) - 16);
      draw.fillText("j = 1", mapX(xOne) - 10, mapY(0) - 16);
      draw.fillText("x", width - padding.right - 10, mapY(0) - 10);
      draw.fillText("P(x)", padding.left + 8, padding.top + 12);
      draw.restore();
    }
  });
}());
