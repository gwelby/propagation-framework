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

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
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
      this.dom.mobileNavToggle = document.getElementById("mobileNavToggle");
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

      this.bindKeyboardNav();
      this.bindHighContrastToggle();
    },

    bindKeyboardNav: function () {
      var self = this;
      var NAV_KEYS = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Home", "End"];
      var routeButtons;

      function getRouteButtons() {
        return Array.from(self.dom.routeNav.querySelectorAll(".route-button"));
      }

      document.addEventListener("keydown", function (e) {
        var routeId = self.state.route;
        if (!routeId) return;

        // Arrow key navigation in route nav
        if (e.target === self.dom.routeNav || e.target.closest(".route-nav")) {
          if (NAV_KEYS.indexOf(e.key) === -1) return;
          e.preventDefault();
          routeButtons = getRouteButtons();
          var currentIndex = routeButtons.findIndex(function (btn) {
            return btn.getAttribute("data-route") === routeId;
          });
          var nextIndex;
          if (e.key === "ArrowRight" || e.key === "ArrowDown") {
            nextIndex = (currentIndex + 1) % routeButtons.length;
          } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
            nextIndex = (currentIndex - 1 + routeButtons.length) % routeButtons.length;
          } else if (e.key === "Home") {
            nextIndex = 0;
          } else if (e.key === "End") {
            nextIndex = routeButtons.length - 1;
          }
          if (nextIndex !== undefined && routeButtons[nextIndex]) {
            routeButtons[nextIndex].focus();
            self.navigate(routeButtons[nextIndex].getAttribute("data-route"));
          }
          return;
        }

        // Escape closes drawer or mobile nav
        if (e.key === "Escape") {
          if (self.state.drawerOpen) {
            self.toggleDrawer(false);
            self.dom.drawerClose.focus();
          }
          if (document.body.classList.contains("nav-open")) {
            document.body.classList.remove("nav-open");
            self.dom.mobileNavToggle && self.dom.mobileNavToggle.setAttribute("aria-expanded", "false");
          }
        }

        // Ctrl+/ opens keyboard shortcuts help (future enhancement)
        if (e.key === "/" && e.ctrlKey) {
          e.preventDefault();
        }
      });

      // Route buttons: focus management
      routeButtons = getRouteButtons();
      routeButtons.forEach(function (btn) {
        btn.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            self.navigate(btn.getAttribute("data-route"));
          }
        });
      });
    },

    bindHighContrastToggle: function () {
      var self = this;
      var btn = document.getElementById("highContrastToggle");
      if (!btn) return;
      btn.addEventListener("click", function () {
        document.body.classList.toggle("high-contrast");
        var isHC = document.body.classList.contains("high-contrast");
        btn.setAttribute("aria-pressed", String(isHC));
        btn.textContent = isHC ? "Standard Contrast" : "High Contrast";
        try {
          localStorage.setItem("pf_high_contrast", isHC ? "1" : "0");
        } catch (e) {}
      });
      // Restore preference
      try {
        if (localStorage.getItem("pf_high_contrast") === "1") {
          document.body.classList.add("high-contrast");
          btn.setAttribute("aria-pressed", "true");
          btn.textContent = "Standard Contrast";
        }
      } catch (e) {}
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
      this.dom.headChipC.textContent = routeId === "dashboard" ? "CLAIMS + UNDERSTAND" : "browser native";
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
      if (this.state.drawerOpen) {
        this.dom.drawerClose.focus();
        this.announceToScreenReader("Evidence drawer opened");
      } else {
        this.announceToScreenReader("Evidence drawer closed");
      }
    },

    announceToScreenReader: function (message) {
      var announcer = document.getElementById("srAnnouncer");
      if (!announcer) return;
      announcer.textContent = "";
      setTimeout(function () {
        announcer.textContent = message;
      }, 50);
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

    statusToClass: function (status) {
      return statusClassMap[status] || statusClassMap.OPEN;
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

    renderWrongIntuition: function (result) {
      if (!result || !result.wrongIntuition) return "";
      var wi = result.wrongIntuition;
      var evidenceAttr = wi.evidencePanel ? ' data-evidence="' + wi.evidencePanel + '"' : '';
      return (
        '<div class="wrong-intuition-callout story-only"' + evidenceAttr + '>' +
          '<div class="wi-header">' +
            '<span class="wi-badge">Your intuition</span>' +
          '</div>' +
          '<p class="wi-intuition">' + escapeHtml(wi.intuition) + '</p>' +
          '<div class="wi-divider">' +
            '<span class="wi-arrow">↓</span>' +
          '</div>' +
          '<p class="wi-reality-label">But actually:</p>' +
          '<p class="wi-reality">' + escapeHtml(wi.reality) + '</p>' +
        '</div>'
      );
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
    PFExplorer.initZoomSequence();
  });

  /* ═══════════════════════════════════════════════════════════════
     9-BEAT ZOOM SEQUENCE — Pass 1: Narrative Architecture
     "Your Intuition About Reality Is Wrong"
     ═══════════════════════════════════════════════════════════════ */
  PFExplorer.initZoomSequence = function () {
    var overlay = document.getElementById("zoomSequenceOverlay");
    var fallback = document.getElementById("zsFallback");
    var stage = document.getElementById("zsStage");
    var headlineEl = document.getElementById("zsHeadline");
    var beatTextEl = document.getElementById("zsBeatText");
    var scaleValueEl = document.getElementById("zsScaleValue");
    var progressFill = document.getElementById("zsProgressFill");
    var beatNumEl = document.getElementById("zsBeatNum");
    var skipBtn = document.getElementById("zsSkipBtn");
    var fallbackBtn = document.getElementById("zsFallbackBtn");
    var directionEl = document.getElementById("zsDirection");

    if (!overlay) return;

    // 9-beat sequence data — the narrative spine
    var beats = [
      {
        scale: "10⁰",
        scaleLog: 0,
        headline: "Your Intuition About Reality Is Wrong.",
        text: "At your scale, reality looks solid.",
        direction: "in"
      },
      {
        scale: "10⁻⁵",
        scaleLog: -5,
        headline: "Cellular",
        text: "Zoom in: solidity becomes living structure.",
        direction: "in"
      },
      {
        scale: "10⁻⁹",
        scaleLog: -9,
        headline: "Molecular",
        text: "Zoom in: structure becomes bond, vibration, and pattern.",
        direction: "in"
      },
      {
        scale: "10⁻¹⁰",
        scaleLog: -10,
        headline: "Atomic",
        text: "Zoom in: atoms are mostly field.",
        direction: "in"
      },
      {
        scale: "10⁻¹⁸",
        scaleLog: -18,
        headline: "Matter",
        text: "Zoom further: matter resolves into standing pattern.",
        direction: "in"
      },
      {
        scale: "10⁻³⁵",
        scaleLog: -35,
        headline: "Planck",
        text: "Zoom further: space stops behaving like space.",
        direction: "in"
      },
      {
        scale: "10⁷",
        scaleLog: 7,
        headline: "Planetary",
        text: "Zoom out: worlds move through curved propagation.",
        direction: "out"
      },
      {
        scale: "10²¹",
        scaleLog: 21,
        headline: "Galactic",
        text: "Zoom out: galaxies settle into density-wave structure.",
        direction: "out"
      },
      {
        scale: "10²⁶",
        scaleLog: 26,
        headline: "Cosmic",
        text: "The universe draws the same logic at the largest scale.",
        direction: "out"
      }
    ];

    var currentBeat = 0;
    var isRunning = false;
    var beatDuration = 3500; // ms per beat (8-10s total sequence)
    var transitionDuration = 400; // ms for text transitions

    // Check sessionStorage for "seen" flag
    var hasSeenSequence = false;
    try {
      hasSeenSequence = sessionStorage.getItem("pf_zoom_sequence_seen") === "1";
    } catch (e) {}

    // Exit handler — navigate to wave visualization, the proof IS the experience
    function exitSequence() {
      if (!isRunning) return;
      isRunning = false;
      overlay.classList.add("zs-exiting");
      setTimeout(function () {
        // Mark as seen
        try {
          sessionStorage.setItem("pf_zoom_sequence_seen", "1");
        } catch (e) {}
        // Navigate to scale ladder with waves active — words → propagation
        window.location.href = "scale-ladder.html?mode=propagation&autostart=1";
      }, 500);
    }

    // Render a beat
    function renderBeat(index) {
      var beat = beats[index];
      if (!beat) return;

      // Exit animation on current content
      headlineEl.classList.add("zs-exit");
      beatTextEl.classList.add("zs-exit");

      setTimeout(function () {
        // Update content
        headlineEl.textContent = beat.headline;
        beatTextEl.textContent = beat.text;
        scaleValueEl.textContent = beat.scale;
        beatNumEl.textContent = String(index + 1);

        // Update progress
        var progress = ((index + 1) / beats.length) * 100;
        progressFill.style.width = String(progress) + "%";

        // Update direction indicator
        if (beat.direction === "out") {
          directionEl.classList.add("zs-zoom-out");
          directionEl.querySelector(".zs-dir-label").textContent = "Zooming Out";
          directionEl.querySelector(".zs-dir-arrow").textContent = "↑";
        } else {
          directionEl.classList.remove("zs-zoom-out");
          directionEl.querySelector(".zs-dir-label").textContent = "Zooming In";
          directionEl.querySelector(".zs-dir-arrow").textContent = "↓";
        }

        // Enter animation
        headlineEl.classList.remove("zs-exit");
        beatTextEl.classList.remove("zs-exit");
      }, transitionDuration);
    }

    // Advance to next beat
    function nextBeat() {
      if (!isRunning) return;
      currentBeat++;
      if (currentBeat >= beats.length) {
        // Final beat complete — show closing text then exit
        setTimeout(function () {
          headlineEl.textContent = "Different scales. Same propagation.";
          beatTextEl.textContent = "Three axioms. Twenty-two audited claims.";
          progressFill.style.width = "100%";
          setTimeout(exitSequence, 2500);
        }, beatDuration);
        return;
      }
      renderBeat(currentBeat);
      setTimeout(nextBeat, beatDuration);
    }

    // Start sequence
    function startSequence() {
      if (hasSeenSequence) {
        // Skip if already seen this session
        overlay.style.display = "none";
        return;
      }
      isRunning = true;
      fallback.style.display = "none";
      stage.style.display = "flex";
      renderBeat(0);
      setTimeout(nextBeat, beatDuration);
    }

    // Skip handler
    if (skipBtn) {
      skipBtn.addEventListener("click", exitSequence);
    }

    // Fallback handler (for no-JS or accessibility)
    if (fallbackBtn) {
      fallbackBtn.addEventListener("click", function () {
        exitSequence();
      });
    }

    // Keyboard: Escape skips, Space advances
    overlay.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        e.preventDefault();
        exitSequence();
      } else if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        if (currentBeat < beats.length - 1) {
          // Advance immediately
          currentBeat++;
          renderBeat(currentBeat);
        } else {
          exitSequence();
        }
      }
    });

    // Start after a brief delay for page load
    setTimeout(startSequence, 300);
  };
}());
