(function () {
  var baseMasses = {
    electron: 0.51099895,
    muon: 105.6583755,
    tau: 1776.86
  };

  function buildMassSet(selection, deltaPct) {
    var multiplier = 1 + deltaPct / 100;
    return {
      electron: selection === "electron" ? baseMasses.electron * multiplier : baseMasses.electron,
      muon: selection === "muon" ? baseMasses.muon * multiplier : baseMasses.muon,
      tau: selection === "tau" ? baseMasses.tau * multiplier : baseMasses.tau
    };
  }

  function valuesFromSet(set) {
    return [set.electron, set.muon, set.tau];
  }

  window.PFExplorer.registerPanel({
    id: "koide",
    mount: function (ctx) {
      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<div class=\"panel-header\">" +
                "<div>" +
                  "<p class=\"eyebrow\">Mass Geometry</p>" +
                  "<h3>The charged lepton triangle stays near one exact target.</h3>" +
                  "<p>Perturb one PDG mass and watch Q pull away from 2 / 3 while the amplitude geometry loosens.</p>" +
                "</div>" +
              "</div>" +
              "<canvas class=\"panel-canvas\" id=\"koideCanvas\"></canvas>" +
              "<div class=\"canvas-overlay\"></div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"koideInfo\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        canvas: ctx.stage.querySelector("#koideCanvas"),
        info: ctx.stage.querySelector("#koideInfo"),
        selectedMass: "tau",
        deltaPct: 0
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
      var current = buildMassSet(state.selectedMass, state.deltaPct);
      var masses = valuesFromSet(current);
      var qValue = ctx.utils.koideQ(masses);
      var ra = ctx.utils.computeKoideRA(masses);
      var deviationPct = Math.abs(qValue - 2 / 3) / (2 / 3) * 100;
      state.info.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">PDG 2024 lepton masses</p>" +
            "<h3>Q = " + qValue.toFixed(7) + "</h3>" +
            "<p>At the baseline masses, the geometry stays almost locked at 2 / 3. Any perturbation immediately makes the deviation visible.</p>" +
          "</div>" +
          "<span class=\"status-pill status-derived\">DERIVED</span>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"koideMassSelect\">Perturb this mass</label>" +
          "<select id=\"koideMassSelect\"><option value=\"electron\">electron</option><option value=\"muon\">muon</option><option value=\"tau\">tau</option></select>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"koideDelta\">Mass offset (%)</label>" +
          "<input id=\"koideDelta\" type=\"range\" min=\"-5\" max=\"5\" step=\"0.1\" value=\"" + state.deltaPct + "\">" +
          "<output id=\"koideDeltaOut\">" + state.deltaPct.toFixed(1) + "%</output>" +
        "</div>" +
        "<div class=\"formula\">Q = sum m_i / (sum sqrt(m_i))^2, R / A = " + ra.ratio.toFixed(5) + "</div>" +
        "<div class=\"stat-grid\">" +
          "<div class=\"stat-tile\"><strong>" + current.electron.toFixed(6) + "</strong><span>electron MeV</span></div>" +
          "<div class=\"stat-tile\"><strong>" + current.muon.toFixed(4) + "</strong><span>muon MeV</span></div>" +
          "<div class=\"stat-tile\"><strong>" + current.tau.toFixed(2) + "</strong><span>tau MeV</span></div>" +
          "<div class=\"stat-tile\"><strong>" + deviationPct.toFixed(4) + "%</strong><span>deviation from 2 / 3</span></div>" +
        "</div>" +
        "<div class=\"note-box story-only\"><strong>Story</strong><p>The baseline triangle is unnervingly tight. Even a small single-mass perturbation bends both Q and R / A away from the repo target.</p></div>" +
        "<div class=\"note-box audit-only\"><strong>Audit</strong><p>The phase frontier remains empirical. The amplitude lock is derived; the delta_0 = 2 / 9 target is displayed below as a separate signal, not silently promoted.</p></div>" +
        "<div class=\"drawer-block\" style=\"padding:0;border:0\">" +
          "<span class=\"eyebrow\">2 / 9 cluster</span>" +
          PFExplorer.compareBarHtml(0.22310, 2 / 9, 0.00045, 0.2218, 0.2236) +
          "<div class=\"metric-row\">" +
            "<span class=\"metric-pill\">delta_Koide = 0.2222296</span>" +
            "<span class=\"metric-pill\">2 / 9 = 0.2222222</span>" +
            "<span class=\"metric-pill\">sin^2(theta_W) = 0.22310</span>" +
          "</div>" +
        "</div>";

      state.info.querySelector("#koideMassSelect").value = state.selectedMass;
      state.info.querySelector("#koideMassSelect").addEventListener("change", function (event) {
        state.selectedMass = event.target.value;
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      state.info.querySelector("#koideDelta").addEventListener("input", function (event) {
        state.deltaPct = Number(event.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      ctx.app.syncActiveResultCards();
    },

    update: function (ctx) {
      var state = this.state;
      var current = buildMassSet(state.selectedMass, state.deltaPct);
      var masses = valuesFromSet(current);
      var roots = masses.map(function (value) { return Math.sqrt(value); });
      var pixelRatio = window.devicePixelRatio;
      var draw = state.canvas.getContext("2d");
      var width = state.canvas.width / pixelRatio;
      var height = state.canvas.height / pixelRatio;
      var cx = width * 0.46;
      var cy = height * 0.54;
      var outer = Math.min(width, height) * 0.28;
      var maxRoot = Math.max.apply(Math, roots);
      var labels = ["tau", "electron", "muon"];
      var angles = [-Math.PI / 2, -Math.PI / 2 + (2 * Math.PI) / 3, -Math.PI / 2 + (4 * Math.PI) / 3];
      var points = [];
      var i;

      draw.save();
      draw.scale(pixelRatio, pixelRatio);
      draw.clearRect(0, 0, width, height);

      draw.strokeStyle = "rgba(255,255,255,0.10)";
      draw.lineWidth = 2;
      draw.beginPath();
      draw.arc(cx, cy, outer, 0, Math.PI * 2);
      draw.stroke();

      for (i = 0; i < 3; i += 1) {
        var length = outer * (roots[i] / maxRoot);
        var point = {
          x: cx + Math.cos(angles[i]) * length,
          y: cy + Math.sin(angles[i]) * length
        };
        points.push(point);
        draw.strokeStyle = "rgba(0,207,255,0.45)";
        draw.lineWidth = 2.2;
        draw.beginPath();
        draw.moveTo(cx, cy);
        draw.lineTo(point.x, point.y);
        draw.stroke();
      }

      draw.beginPath();
      points.forEach(function (point, index) {
        if (index === 0) {
          draw.moveTo(point.x, point.y);
        } else {
          draw.lineTo(point.x, point.y);
        }
      });
      draw.closePath();
      draw.strokeStyle = "rgba(255,221,85,0.94)";
      draw.lineWidth = 2.4;
      draw.stroke();

      points.forEach(function (point, index) {
        var color = index === 0 ? "#ffdd55" : (index === 1 ? "#00cfff" : "#44ff88");
        draw.fillStyle = color;
        draw.beginPath();
        draw.arc(point.x, point.y, 9, 0, Math.PI * 2);
        draw.fill();
        draw.fillStyle = "rgba(255,255,255,0.92)";
        draw.font = "13px Trebuchet MS";
        draw.fillText(labels[index], point.x + 12, point.y + 4);
      });

      draw.fillStyle = "rgba(255,255,255,0.88)";
      draw.font = "14px Georgia";
      draw.fillText("sqrt(m_i) amplitudes", width * 0.08, height * 0.16);
      draw.fillStyle = "rgba(154,178,199,0.9)";
      draw.font = "12px Trebuchet MS";
      draw.fillText("triangle deforms immediately when one mass leaves the lock", width * 0.08, height * 0.21);

      draw.restore();
    }
  });
}());
