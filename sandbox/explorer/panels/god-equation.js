(function () {
  var LP = 1.616e-35;
  var OBSERVED = 1.14e-18;
  var CLAIM_ANCHOR = 1.145e-18;
  var CLAIM_N = 3;
  var CLAIM_D = 3;

  function b0ForN(n) {
    return (22 - 2 * n) / 3;
  }

  function exponentFor(n, d) {
    var b0 = b0ForN(n);
    if (b0 <= 0) {
      return null;
    }
    return (4 * Math.PI * Math.PI * Math.pow(n, d / 2)) / b0;
  }

  function lambdaFor(n, d) {
    var exponent = exponentFor(n, d);
    var anchorExponent = exponentFor(CLAIM_N, CLAIM_D);
    if (exponent == null || anchorExponent == null) {
      return null;
    }
    // Anchor the live slider math to the audited CLAIMS.md snapshot, then move by the RG exponent.
    return CLAIM_ANCHOR * Math.exp(exponent - anchorExponent);
  }

  function sourceListHtml(sources) {
    return (
      "<div class=\"source-list\">" +
        sources.map(function (source) {
          return "<a href=\"" + source.href + "\" target=\"_blank\" rel=\"noreferrer\">" + source.label + "</a>";
        }).join("") +
      "</div>"
    );
  }

  function dependencyChainHtml(chain) {
    return (
      "<div class=\"audit-chain\">" +
        chain.map(function (step, index) {
          return (
            (index ? "<span class=\"audit-chain-arrow\">&#8594;</span>" : "") +
            "<div class=\"audit-chain-step is-" + step.state + "\">" +
              "<strong>" + step.label + "</strong>" +
              "<span>" + step.note + "</span>" +
            "</div>"
          );
        }).join("") +
      "</div>"
    );
  }

  function channelToyHtml() {
    return (
      "<section class=\"toy-visual\">" +
        "<div>" +
          "<p class=\"eyebrow\">Gap A</p>" +
          "<h4>Locality is not yet Markovity</h4>" +
          "<p>Nearest-neighbor couplings show local propagation. The missing step is the memoryless coarse operator that turns that locality into a first-order walk.</p>" +
        "</div>" +
        "<div class=\"channel-track\">" +
          "<div class=\"channel-row\">" +
            "<span class=\"channel-label\">Local medium</span>" +
            "<span class=\"channel-node is-cyan\"></span><span class=\"channel-link\"></span><span class=\"channel-node is-cyan\"></span><span class=\"channel-link\"></span><span class=\"channel-node is-cyan\"></span>" +
          "</div>" +
          "<div class=\"channel-row channel-row-weak\">" +
            "<span class=\"channel-label\">Need for proof</span>" +
            "<span class=\"channel-node is-gold\"></span><span class=\"channel-link is-dashed\"></span><span class=\"channel-node is-gold\"></span><span class=\"channel-link is-dashed\"></span><span class=\"channel-node is-gold\"></span>" +
          "</div>" +
        "</div>" +
        "<div class=\"toy-caption\">Top row: already-local channels. Bottom row: the still-unproved one-step transition law.</div>" +
      "</section>"
    );
  }

  function factorizationToyHtml() {
    return (
      "<section class=\"toy-visual\">" +
        "<div>" +
          "<p class=\"eyebrow\">Gap C</p>" +
          "<h4>Zero covariance is weaker than factorization</h4>" +
          "<p>A clean covariance signal can still hide structure in the joint law. The proof target is the full H_prod factorization, not only a weaker decoupling statistic.</p>" +
        "</div>" +
        "<div class=\"factor-compare\">" +
          "<div class=\"factor-panel\">" +
            "<span class=\"factor-label\">Zero covariance</span>" +
            "<div class=\"factor-grid\">" +
              "<span class=\"factor-cell level-mid\"></span><span class=\"factor-cell level-low\"></span><span class=\"factor-cell level-mid\"></span>" +
              "<span class=\"factor-cell level-low\"></span><span class=\"factor-cell level-high\"></span><span class=\"factor-cell level-low\"></span>" +
              "<span class=\"factor-cell level-mid\"></span><span class=\"factor-cell level-low\"></span><span class=\"factor-cell level-mid\"></span>" +
            "</div>" +
          "</div>" +
          "<div class=\"factor-panel\">" +
            "<span class=\"factor-label\">Factorized H_prod</span>" +
            "<div class=\"factor-grid\">" +
              "<span class=\"factor-cell level-low\"></span><span class=\"factor-cell level-mid\"></span><span class=\"factor-cell level-high\"></span>" +
              "<span class=\"factor-cell level-low\"></span><span class=\"factor-cell level-mid\"></span><span class=\"factor-cell level-high\"></span>" +
              "<span class=\"factor-cell level-low\"></span><span class=\"factor-cell level-mid\"></span><span class=\"factor-cell level-high\"></span>" +
            "</div>" +
          "</div>" +
        "</div>" +
        "<div class=\"toy-caption\">Balanced noise can mimic decoupling. The right-hand structure is stronger: the full joint law splits into channel products.</div>" +
      "</section>"
    );
  }

  function gapCardsHtml(gaps) {
    return (
      "<div class=\"audit-gap-grid\">" +
        gaps.map(function (gap) {
          return (
            "<article class=\"audit-gap-card\">" +
              "<div class=\"gap-card-head\">" +
                "<div class=\"gap-heading\">" +
                  "<span class=\"gap-letter\">" + gap.id + "</span>" +
                  "<div>" +
                    "<h4>" + gap.title + "</h4>" +
                    "<p>" + gap.need + "</p>" +
                  "</div>" +
                "</div>" +
                "<span class=\"gap-verdict\">" + gap.verdict + "</span>" +
              "</div>" +
              "<div class=\"mini-audit-block\">" +
                "<span class=\"eyebrow\">What survives</span>" +
                "<p>" + gap.survives + "</p>" +
              "</div>" +
              "<div class=\"mini-audit-block\">" +
                "<span class=\"eyebrow\">Why it remains open</span>" +
                "<p>" + gap.detail + "</p>" +
              "</div>" +
              "<div class=\"mini-audit-block\">" +
                "<span class=\"eyebrow\">Source trail</span>" +
                sourceListHtml(gap.sources) +
              "</div>" +
            "</article>"
          );
        }).join("") +
      "</div>"
    );
  }

  window.PFExplorer.registerPanel({
    id: "god-equation",
    mount: function (ctx) {
      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<div class=\"panel-atlas\">" +
            "<section class=\"canvas-panel\">" +
              "<div class=\"panel-header\">" +
                "<div>" +
                  "<p class=\"eyebrow\">Planck to Matter</p>" +
                  "<h3>The hierarchy is rendered as one exponential climb, not a loose metaphor.</h3>" +
                  "<p>Move N and D and the ladder either lands near the matter window or misses it by orders of magnitude.</p>" +
                "</div>" +
              "</div>" +
              "<canvas class=\"panel-canvas\" id=\"godCanvas\"></canvas>" +
              "<div class=\"canvas-overlay\"></div>" +
            "</section>" +
            "<section class=\"info-panel\" id=\"godInfo\"></section>" +
          "</div>" +
        "</div>";

      this.state = {
        canvas: ctx.stage.querySelector("#godCanvas"),
        info: ctx.stage.querySelector("#godInfo"),
        nValue: 3,
        dValue: 3
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
      var b0 = b0ForN(state.nValue);
      var prediction = lambdaFor(state.nValue, state.dValue);
      var errorPct = prediction ? Math.abs(prediction - OBSERVED) / OBSERVED * 100 : null;
      var audit = ctx.data.godEquationAudit || { dependencyChain: [], gaps: [] };

      state.info.innerHTML =
        "<div class=\"panel-header\">" +
          "<div>" +
            "<p class=\"eyebrow\">Current frontier</p>" +
            "<h3>" + (prediction ? ctx.utils.formatScientific(prediction, 3) + " m" : "no asymptotic branch") + "</h3>" +
            "<p>The current repo keeps the formula and the numerical target, but the operator and probability bridge remain explicitly open.</p>" +
          "</div>" +
          "<span class=\"status-pill status-conditional\">CONDITIONAL</span>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"godN\">Generations N</label>" +
          "<input id=\"godN\" type=\"range\" min=\"1\" max=\"5\" step=\"1\" value=\"" + state.nValue + "\">" +
          "<output id=\"godNOut\">N = " + state.nValue + "</output>" +
        "</div>" +
        "<div class=\"control-group\">" +
          "<label for=\"godD\">Spatial dimensions D</label>" +
          "<input id=\"godD\" type=\"range\" min=\"1\" max=\"5\" step=\"1\" value=\"" + state.dValue + "\">" +
          "<output id=\"godDOut\">D = " + state.dValue + "</output>" +
        "</div>" +
        "<div class=\"formula\">lambda_c = sqrt(2) l_P exp(4 pi^2 N^(D/2) / b0), b0 = (22 - 2N) / 3</div>" +
        "<div class=\"stat-grid\">" +
          "<div class=\"stat-tile\"><strong>" + b0.toFixed(3) + "</strong><span>b0(N)</span></div>" +
          "<div class=\"stat-tile\"><strong>" + (prediction ? errorPct.toFixed(1) + "%" : "n/a") + "</strong><span>error vs 1.14e-18 m</span></div>" +
          "<div class=\"stat-tile\"><strong>" + ctx.utils.formatScientific(LP, 2) + "</strong><span>Planck boundary</span></div>" +
          "<div class=\"stat-tile\"><strong>" + ctx.utils.formatScientific(OBSERVED, 2) + "</strong><span>observed matter scale</span></div>" +
        "</div>" +
        "<div class=\"note-box story-only\"><strong>Story</strong><p>N = 3 and D = 3 are the intended landing site. Moving either one shifts the exponential enough that the matter window becomes visibly special.</p></div>" +
        "<div class=\"note-box audit-only\"><strong>Why CONDITIONAL stays CONDITIONAL</strong><p>The `(3,3)` point remains anchored to the current CLAIMS.md snapshot at 1.145e-18 m and 0.4% error. What stays open is not the arithmetic display but the bridge from the exact internal model to the operator closure and full H_prod probability statement.</p></div>" +
        "<section class=\"audit-stack audit-only\">" +
          "<div class=\"audit-section\">" +
            "<span class=\"eyebrow\">Dependency chain</span>" +
            "<p>This is the current proof spine: what is already secured, what strengthened, and where the upgrade still blocks.</p>" +
            dependencyChainHtml(audit.dependencyChain) +
          "</div>" +
          "<div class=\"two-column audit-toy-grid\">" +
            channelToyHtml() +
            factorizationToyHtml() +
          "</div>" +
          gapCardsHtml(audit.gaps) +
        "</section>";

      state.info.querySelector("#godN").addEventListener("input", function (event) {
        state.nValue = Number(event.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
      state.info.querySelector("#godD").addEventListener("input", function (event) {
        state.dValue = Number(event.target.value);
        PFExplorer.state.activePanel.renderInfo(ctx);
      });
    },

    update: function (ctx) {
      var state = this.state;
      var prediction = lambdaFor(state.nValue, state.dValue);
      var pixelRatio = window.devicePixelRatio;
      var draw = state.canvas.getContext("2d");
      var width = state.canvas.width / pixelRatio;
      var height = state.canvas.height / pixelRatio;
      var topY = height * 0.14;
      var bottomY = height * 0.88;
      var axisX = width * 0.42;
      var minLog = -35;
      var maxLog = -17;

      function yForValue(value) {
        var exponent = Math.log10(value);
        var t = (exponent - minLog) / (maxLog - minLog);
        return bottomY - t * (bottomY - topY);
      }

      draw.save();
      draw.scale(pixelRatio, pixelRatio);
      draw.clearRect(0, 0, width, height);

      draw.strokeStyle = "rgba(255,255,255,0.10)";
      draw.lineWidth = 10;
      draw.beginPath();
      draw.moveTo(axisX, topY);
      draw.lineTo(axisX, bottomY);
      draw.stroke();

      draw.strokeStyle = "rgba(255,255,255,0.12)";
      draw.lineWidth = 1;
      [-35, -30, -25, -20, -18].forEach(function (tick) {
        var y = yForValue(Math.pow(10, tick));
        draw.beginPath();
        draw.moveTo(axisX - 18, y);
        draw.lineTo(axisX + 18, y);
        draw.stroke();
        draw.fillStyle = "rgba(154,178,199,0.88)";
        draw.font = "12px Trebuchet MS";
        draw.fillText("1e" + tick, axisX + 26, y + 4);
      });

      var bandY = yForValue(OBSERVED);
      draw.fillStyle = "rgba(68,255,136,0.16)";
      draw.fillRect(axisX - 80, bandY - 14, 160, 28);
      draw.fillStyle = "rgba(68,255,136,0.96)";
      draw.fillText("observed matter window", axisX + 92, bandY + 4);

      var planckY = yForValue(LP);
      draw.fillStyle = "rgba(255,221,85,0.95)";
      draw.beginPath();
      draw.arc(axisX, planckY, 8, 0, Math.PI * 2);
      draw.fill();
      draw.fillText("l_P", axisX - 28, planckY + 5);

      if (prediction) {
        var predictedY = yForValue(prediction);
        draw.strokeStyle = "rgba(0,207,255,0.86)";
        draw.lineWidth = 3;
        draw.beginPath();
        draw.moveTo(axisX, planckY);
        draw.lineTo(axisX, predictedY);
        draw.stroke();
        draw.fillStyle = "rgba(0,207,255,0.98)";
        draw.beginPath();
        draw.arc(axisX, predictedY, state.nValue === 3 && state.dValue === 3 ? 12 : 9, 0, Math.PI * 2);
        draw.fill();
        draw.fillText(state.nValue === 3 && state.dValue === 3 ? "claim anchor (3,3)" : "predicted lambda_c", axisX - 128, predictedY - 12);
      }

      draw.restore();
    }
  });
}());
