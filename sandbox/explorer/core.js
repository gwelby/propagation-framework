(function () {
  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function round(value, digits) {
    var factor = Math.pow(10, digits || 0);
    return Math.round(value * factor) / factor;
  }

  function formatConfidence(value) {
    if (typeof value !== "number") {
      return "Unsynced";
    }
    return value.toFixed(2);
  }

  function formatScientific(value, digits) {
    if (!isFinite(value) || value === 0) {
      return String(value);
    }
    var exp = value.toExponential(digits == null ? 2 : digits).split("e");
    return exp[0] + "e" + exp[1].replace("+", "");
  }

  function formatPercent(value, digits) {
    return round(value * 100, digits == null ? 2 : digits).toFixed(digits == null ? 2 : digits) + "%";
  }

  function createElement(tag, className, html) {
    var node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (html != null) {
      node.innerHTML = html;
    }
    return node;
  }

  function uniqueKinds(results) {
    var seen = {};
    var out = [];
    results.forEach(function (result) {
      if (!seen[result.kind]) {
        seen[result.kind] = true;
        out.push(result.kind);
      }
    });
    return out;
  }

  var statusClassMap = {
    DERIVED: "status-derived",
    CONDITIONAL: "status-conditional",
    "PARTIAL DERIVATION": "status-partial",
    ARGUED: "status-argued",
    EMPIRICAL: "status-empirical",
    INTUITION: "status-intuition",
    OPEN: "status-open",
    UNSYNCED: "status-unsynced"
  };

  var PFExplorer = {
    data: window.PFExplorerData,
    panels: {},
    dom: {},
    state: {
      route: "hub",
      mode: "story",
      activePanel: null,
      activePanelCtx: null,
      focusedResultId: null,
      drawerOpen: false,
      layoutMode: null,
      frameHandle: 0,
      lastFrame: 0
    },
    utils: {
      clamp: clamp,
      lerp: lerp,
      round: round,
      formatConfidence: formatConfidence,
      formatScientific: formatScientific,
      formatPercent: formatPercent,
      casimirRoot: function (spin) {
        var c2 = spin * (spin + 1);
        return (-c2 + Math.sqrt(c2 * c2 + 4 * c2)) / 2;
      },
      qOfN: function (n) {
        return (2 * n) / (2 * n + 3);
      },
      koideQ: function (masses) {
        var sqrtSum = masses.reduce(function (acc, value) {
          return acc + Math.sqrt(value);
        }, 0);
        var massSum = masses.reduce(function (acc, value) {
          return acc + value;
        }, 0);
        return massSum / (sqrtSum * sqrtSum);
      },
      computeKoideRA: function (masses) {
        var roots = masses.map(function (value) {
          return Math.sqrt(value);
        });
        var a = roots.reduce(function (acc, value) {
          return acc + value;
        }, 0) / roots.length;
        var variance = roots.reduce(function (acc, value) {
          return acc + Math.pow(value - a, 2);
        }, 0);
        var r = Math.sqrt((2 / 3) * variance);
        return {
          A: a,
          R: r,
          ratio: r / a
        };
      }
    },

    registerPanel: function (definition) {
      this.panels[definition.id] = definition;
    },

    boot: function () {
      this.cacheDom();
      this.applyDrawerState();
      this.renderMetrics();
      this.renderNav();
      this.bindGlobalEvents();
      this.resolveRoute();
      this.focusResult("god-equation", { open: this.state.drawerOpen });
      this.loop(performance.now());
    },

    cacheDom: function () {
      this.dom.body = document.body;
      this.dom.routeNav = document.getElementById("routeNav");
      this.dom.metricStack = document.getElementById("metricStack");
      this.dom.panelStage = document.getElementById("panelStage");
      this.dom.panelTitle = document.getElementById("panelTitle");
      this.dom.panelEyebrow = document.getElementById("panelEyebrow");
      this.dom.drawerTitle = document.getElementById("drawerTitle");
      this.dom.drawerEyebrow = document.getElementById("drawerEyebrow");
      this.dom.drawerBody = document.getElementById("drawerBody");
      this.dom.drawer = document.getElementById("appDrawer");
      this.dom.modeToggle = document.getElementById("modeToggle");
      this.dom.drawerToggle = document.getElementById("drawerToggle");
      this.dom.drawerClose = document.getElementById("drawerClose");
      this.dom.headChipA = document.getElementById("headChipA");
      this.dom.headChipB = document.getElementById("headChipB");
      this.dom.headChipC = document.getElementById("headChipC");
    },

    bindGlobalEvents: function () {
      var self = this;

      window.addEventListener("hashchange", function () {
        self.resolveRoute();
      });

      window.addEventListener("resize", function () {
        self.applyDrawerState();
        if (self.state.activePanel && typeof self.state.activePanel.resize === "function") {
          self.state.activePanel.resize(self.state.activePanelCtx);
        }
      });

      this.dom.modeToggle.addEventListener("click", function (event) {
        var button = event.target.closest("[data-mode]");
        if (!button) {
          return;
        }
        self.setMode(button.getAttribute("data-mode"));
      });

      this.dom.drawerToggle.addEventListener("click", function () {
        self.toggleDrawer();
      });

      this.dom.drawerClose.addEventListener("click", function () {
        self.toggleDrawer(false);
      });
    },

    resolveRoute: function () {
      var nextRoute = (window.location.hash || "#hub").replace(/^#/, "");
      if (!this.panels[nextRoute]) {
        nextRoute = "hub";
        window.location.hash = "#hub";
      }
      this.mountRoute(nextRoute);
    },

    renderNav: function () {
      var self = this;
      this.dom.routeNav.innerHTML = "";
      this.data.panelMeta.forEach(function (panel) {
        var button = createElement(
          "button",
          "route-button" + (panel.id === self.state.route ? " is-active" : ""),
          "<span class=\"route-name\">" + panel.title + "</span><span class=\"route-note\">" + panel.note + "</span>"
        );
        button.type = "button";
        button.setAttribute("data-route", panel.id);
        button.addEventListener("click", function () {
          self.navigate(panel.id);
        });
        self.dom.routeNav.appendChild(button);
      });
    },

    renderMetrics: function () {
      var audited = this.getAuditedResults();
      var counts = {};
      audited.forEach(function (result) {
        counts[result.status] = (counts[result.status] || 0) + 1;
      });

      this.dom.metricStack.innerHTML = "";
      var cards = [
        { value: 3, label: "Axioms" },
        { value: counts.DERIVED || 0, label: "Derived" },
        { value: audited.length, label: "Audited results" },
        { value: counts.CONDITIONAL || 0, label: "Conditional" },
        { value: counts.EMPIRICAL || 0, label: "Empirical" },
        { value: (counts["PARTIAL DERIVATION"] || 0) + (counts.ARGUED || 0) + (counts.INTUITION || 0), label: "Frontier items" }
      ];

      cards.forEach(function (card) {
        var node = createElement("div", "metric-card");
        node.innerHTML = "<strong>" + card.value + "</strong><span>" + card.label + "</span>";
        PFExplorer.dom.metricStack.appendChild(node);
      });
    },

    navigate: function (routeId) {
      window.location.hash = "#" + routeId;
    },

    mountRoute: function (routeId) {
      var panel = this.panels[routeId];
      var meta = this.getPanelMeta(routeId);
      var defaultResult = meta && meta.linkedResultIds.length ? meta.linkedResultIds[0] : null;

      if (this.state.activePanel && typeof this.state.activePanel.unmount === "function") {
        this.state.activePanel.unmount(this.state.activePanelCtx);
      }

      this.state.route = routeId;
      this.state.activePanel = panel;
      this.dom.panelStage.innerHTML = "";
      this.dom.panelTitle.textContent = meta ? meta.title : panel.title || routeId;
      this.dom.panelEyebrow.textContent = meta ? meta.note : "Propagation Framework Explorer";
      this.dom.headChipA.textContent = routeId === "dashboard" ? "audit wall" : "live computation";
      this.dom.headChipB.textContent = routeId === "hub" ? "scale atlas" : "shared evidence drawer";
      this.dom.headChipC.textContent = routeId === "dashboard" ? "CLAIMS + UNDERSTAND" : "file:// ready";
      this.renderNav();

      this.state.activePanelCtx = {
        app: this,
        data: this.data,
        stage: this.dom.panelStage,
        meta: meta,
        utils: this.utils
      };

      panel.mount(this.state.activePanelCtx);
      if (typeof panel.resize === "function") {
        panel.resize(this.state.activePanelCtx);
      }

      if (defaultResult) {
        this.focusResult(defaultResult, { open: this.state.drawerOpen });
      } else if (routeId === "dashboard") {
        this.focusResult("god-equation", { open: this.state.drawerOpen });
      }
    },

    setMode: function (mode) {
      this.state.mode = mode === "audit" ? "audit" : "story";
      this.dom.body.classList.toggle("mode-story", this.state.mode === "story");
      this.dom.body.classList.toggle("mode-audit", this.state.mode === "audit");
      Array.prototype.forEach.call(this.dom.modeToggle.querySelectorAll("[data-mode]"), function (button) {
        button.classList.toggle("is-active", button.getAttribute("data-mode") === PFExplorer.state.mode);
      });
      if (this.state.activePanel && typeof this.state.activePanel.onModeChange === "function") {
        this.state.activePanel.onModeChange(this.state.activePanelCtx);
      }
      this.renderDrawer();
    },

    toggleDrawer: function (forceOpen) {
      if (typeof forceOpen === "boolean") {
        this.state.drawerOpen = forceOpen;
      } else {
        this.state.drawerOpen = !this.state.drawerOpen;
      }
      this.applyDrawerState();
    },

    applyDrawerState: function () {
      var nextLayout = window.innerWidth > 1180 ? "wide" : (window.innerWidth > 960 ? "overlay" : "narrow");
      if (this.state.layoutMode !== nextLayout) {
        if (nextLayout === "wide") {
          this.state.drawerOpen = true;
        } else if (this.state.layoutMode == null || this.state.layoutMode === "wide") {
          this.state.drawerOpen = false;
        }
        this.state.layoutMode = nextLayout;
      }
      this.dom.body.classList.toggle("drawer-collapsed", !this.state.drawerOpen);
      this.dom.body.classList.toggle("drawer-overlay", nextLayout !== "wide");
      this.dom.body.classList.toggle("drawer-wide", nextLayout === "wide");
    },

    getAuditedResults: function () {
      return this.data.results.filter(function (result) {
        return !result.unsynced;
      });
    },

    getResult: function (resultId) {
      return this.data.results.find(function (result) {
        return result.id === resultId;
      });
    },

    getScale: function (scaleId) {
      return this.data.scales.find(function (scale) {
        return scale.id === scaleId;
      });
    },

    getPanelMeta: function (panelId) {
      return this.data.panelMeta.find(function (panel) {
        return panel.id === panelId;
      });
    },

    getResultPanelId: function (result) {
      if (result.panelId) {
        return result.panelId;
      }
      var match = this.data.panelMeta.find(function (panel) {
        return panel.linkedResultIds.indexOf(result.id) >= 0;
      });
      return match ? match.id : null;
    },

    getLinkedPanelIdsForScale: function (scale) {
      var panelIds = {};
      if (!scale) {
        return [];
      }
      scale.resultIds.forEach(function (resultId) {
        var result = PFExplorer.getResult(resultId);
        var panelId = result ? PFExplorer.getResultPanelId(result) : null;
        if (panelId) {
          panelIds[panelId] = true;
        }
      });
      return Object.keys(panelIds);
    },

    focusResult: function (resultId, options) {
      var result = this.getResult(resultId);
      if (!result) {
        return;
      }
      this.state.focusedResultId = result.id;
      if (!options || options.open !== false) {
        this.state.drawerOpen = true;
        this.applyDrawerState();
      }
      this.renderDrawer();
      this.syncActiveResultCards();
    },

    syncActiveResultCards: function () {
      var activeId = this.state.focusedResultId;
      Array.prototype.forEach.call(document.querySelectorAll("[data-result-id]"), function (node) {
        node.classList.toggle("is-active", node.getAttribute("data-result-id") === activeId);
      });
    },

    renderDrawer: function () {
      var result = this.getResult(this.state.focusedResultId);
      if (!result) {
        this.dom.drawerTitle.textContent = "Select a result";
        this.dom.drawerBody.innerHTML = "";
        return;
      }

      var scale = this.getScale(result.scaleId);
      var panelId = this.getResultPanelId(result);
      this.dom.drawerTitle.textContent = result.title;
      this.dom.drawerEyebrow.textContent = result.unsynced ? "Evidence - Unsynced" : "Evidence - Audited";

      var body = [];
      body.push(
        "<div class=\"drawer-block\">" +
          "<div class=\"result-card-head\">" +
            "<div>" +
              "<h4>" + result.title + "</h4>" +
              "<p>" + result.summary + "</p>" +
            "</div>" +
            "<span class=\"status-pill " + statusClassMap[result.status] + "\">" + result.status + "</span>" +
          "</div>" +
        "</div>"
      );

      body.push(
        "<div class=\"drawer-block\">" +
          "<div class=\"drawer-grid\">" +
            "<div class=\"drawer-metric\"><strong>" + (scale ? scale.label : "Unplaced") + "</strong><span>Scale placement</span></div>" +
            "<div class=\"drawer-metric\"><strong>" + formatConfidence(result.confidence) + "</strong><span>Confidence</span></div>" +
          "</div>" +
          (result.unsynced ? "<p class=\"unsynced-note\">This item is visible because UNDERSTAND.md mentions it, but it is excluded from audited totals until CLAIMS.md carries a synchronized entry.</p>" : "") +
        "</div>"
      );

      body.push(
        "<div class=\"drawer-block\">" +
          "<span class=\"eyebrow\">Core Formula</span>" +
          "<div class=\"formula\">" + result.formula + "</div>" +
        "</div>"
      );

      if (this.state.mode === "audit") {
        body.push(
          "<div class=\"drawer-block\">" +
            "<span class=\"eyebrow\">What Falsifies It</span>" +
            "<p>" + result.falsifier + "</p>" +
          "</div>"
        );
      }

      body.push(
        "<div class=\"drawer-block\">" +
          "<span class=\"eyebrow\">Sources</span>" +
          "<div class=\"source-list\">" +
            result.sources.map(function (source) {
              return "<a href=\"" + source.href + "\" target=\"_blank\" rel=\"noreferrer\">" + source.label + "</a>";
            }).join("") +
          "</div>" +
          (panelId ? "<div class=\"result-actions\" style=\"margin-top:12px\"><button class=\"soft-button\" type=\"button\" data-open-panel=\"" + panelId + "\">Open linked panel</button></div>" : "") +
        "</div>"
      );

      this.dom.drawerBody.innerHTML = body.join("");

      Array.prototype.forEach.call(this.dom.drawerBody.querySelectorAll("[data-open-panel]"), function (button) {
        button.addEventListener("click", function () {
          PFExplorer.navigate(button.getAttribute("data-open-panel"));
        });
      });
    },

    createResultCard: function (result, options) {
      options = options || {};
      var card = createElement("article", "result-card");
      var panelId = this.getResultPanelId(result);
      var confidenceWidth = typeof result.confidence === "number" ? clamp(result.confidence, 0, 1) * 100 : 0;
      var shouldInlineAudit = options.showInlineFalsifier || options.showInlineSources;
      var auditId = "";
      var inlineAuditHtml = "";
      var auditDetailsHtml = "<p>" + result.formula + "</p>";

      if (!shouldInlineAudit) {
        auditDetailsHtml += "<p style=\"margin-top:8px\">" + result.falsifier + "</p>";
      } else {
        this._inlineAuditSerial = (this._inlineAuditSerial || 0) + 1;
        auditId = "inline-audit-" + this._inlineAuditSerial;
        inlineAuditHtml =
          "<div class=\"inline-audit\">" +
            "<button class=\"soft-button inline-audit-toggle\" type=\"button\" data-inline-audit-toggle=\"" + auditId + "\" aria-expanded=\"" + (options.auditExpanded ? "true" : "false") + "\">" +
              (options.auditExpanded ? "Hide" : "Show") + " audit details" +
            "</button>" +
            "<div class=\"inline-audit-body\" id=\"" + auditId + "\"" + (options.auditExpanded ? "" : " hidden") + ">" +
              (options.showInlineFalsifier ?
                "<div class=\"mini-audit-block\">" +
                  "<span class=\"eyebrow\">What Would Falsify It</span>" +
                  "<p>" + result.falsifier + "</p>" +
                "</div>" : "") +
              (options.showInlineSources ?
                "<div class=\"mini-audit-block\">" +
                  "<span class=\"eyebrow\">Sources</span>" +
                  "<div class=\"source-list\">" +
                    result.sources.map(function (source) {
                      return "<a href=\"" + source.href + "\" target=\"_blank\" rel=\"noreferrer\">" + source.label + "</a>";
                    }).join("") +
                  "</div>" +
                "</div>" : "") +
            "</div>" +
          "</div>";
      }

      card.setAttribute("data-result-id", result.id);
      card.innerHTML =
        "<div class=\"result-card-head\">" +
          "<div>" +
            "<h4>" + result.title + "</h4>" +
            "<p>" + result.summary + "</p>" +
          "</div>" +
          "<span class=\"status-pill " + statusClassMap[result.status] + "\">" + result.status + "</span>" +
        "</div>" +
        "<div class=\"confidence-bar\"><span style=\"width:" + confidenceWidth + "%\"></span></div>" +
        "<div class=\"metric-row\">" +
          "<span class=\"metric-pill\">" + this.getScale(result.scaleId).label + "</span>" +
          "<span class=\"metric-pill\">" + formatConfidence(result.confidence) + "</span>" +
          (result.unsynced ? "<span class=\"metric-pill unsynced-note\">Unsynced</span>" : "") +
        "</div>" +
        "<div class=\"story-only note-box\"><strong>Story</strong><p>" + result.summary + "</p></div>" +
        "<div class=\"audit-only note-box\"><strong>Audit</strong>" + auditDetailsHtml + "</div>" +
        inlineAuditHtml +
        "<div class=\"result-actions\">" +
          "<button class=\"soft-button\" type=\"button\" data-focus-result=\"" + result.id + "\">Evidence</button>" +
          (panelId && options.hidePanelButton !== true ? "<button class=\"soft-button\" type=\"button\" data-open-panel=\"" + panelId + "\">Open panel</button>" : "") +
        "</div>";

      Array.prototype.forEach.call(card.querySelectorAll("[data-focus-result]"), function (button) {
        button.addEventListener("click", function () {
          PFExplorer.focusResult(button.getAttribute("data-focus-result"), { open: true });
        });
      });

      Array.prototype.forEach.call(card.querySelectorAll("[data-open-panel]"), function (button) {
        button.addEventListener("click", function () {
          PFExplorer.navigate(button.getAttribute("data-open-panel"));
        });
      });

      Array.prototype.forEach.call(card.querySelectorAll("[data-inline-audit-toggle]"), function (button) {
        button.addEventListener("click", function () {
          var target = card.querySelector("#" + button.getAttribute("data-inline-audit-toggle"));
          var nextExpanded = target.hasAttribute("hidden");
          if (nextExpanded) {
            target.removeAttribute("hidden");
          } else {
            target.setAttribute("hidden", "hidden");
          }
          button.setAttribute("aria-expanded", nextExpanded ? "true" : "false");
          button.textContent = (nextExpanded ? "Hide" : "Show") + " audit details";
        });
      });

      if (options.wholeCardFocus) {
        card.addEventListener("click", function (event) {
          if (event.target.closest("button, a, input, select, textarea, label")) {
            return;
          }
          PFExplorer.focusResult(result.id, { open: true });
        });
      }

      return card;
    },

    compareBarHtml: function (prediction, reference, error, min, max) {
      var left = function (value) {
        return clamp((value - min) / (max - min), 0, 1) * 100;
      };
      var bandMin = left(reference - error);
      var bandMax = left(reference + error);
      return (
        "<div class=\"comparison-track\">" +
          "<span class=\"comparison-band\" style=\"left:" + bandMin + "%; width:" + (bandMax - bandMin) + "%\"></span>" +
          "<span class=\"comparison-point prediction\" style=\"left:" + left(prediction) + "%\"></span>" +
          "<span class=\"comparison-point reference\" style=\"left:" + left(reference) + "%\"></span>" +
        "</div>"
      );
    },

    loop: function (timestamp) {
      var self = this;
      var dt = Math.min((timestamp - this.state.lastFrame) / 1000, 0.05) || 0.016;
      this.state.lastFrame = timestamp;

      if (this.state.activePanel && typeof this.state.activePanel.update === "function") {
        this.state.activePanel.update(this.state.activePanelCtx, dt, timestamp / 1000);
      }

      this.state.frameHandle = window.requestAnimationFrame(function (nextTimestamp) {
        self.loop(nextTimestamp);
      });
    }
  };

  PFExplorer.data.kinds = uniqueKinds(PFExplorer.data.results);

  window.PFExplorer = PFExplorer;

  document.addEventListener("DOMContentLoaded", function () {
    PFExplorer.boot();
  });
}());
