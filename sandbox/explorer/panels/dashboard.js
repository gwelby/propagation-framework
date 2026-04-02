(function () {
  function sortResults(a, b) {
    var aScore = typeof a.confidence === "number" ? a.confidence : -1;
    var bScore = typeof b.confidence === "number" ? b.confidence : -1;
    return bScore - aScore;
  }

  function matchesQuery(result, query) {
    if (!query) {
      return true;
    }
    var haystack = [
      result.title,
      result.formula,
      result.summary,
      result.falsifier
    ].join(" ").toLowerCase();
    return haystack.indexOf(query) >= 0;
  }

  function createFilterChip(label, status, isActive, count) {
    var chip = document.createElement("button");
    chip.className = "chip-button" + (isActive ? " is-active" : "");
    chip.type = "button";
    chip.setAttribute("data-filter", status);
    chip.innerHTML = label + " <span class=\"chip-count\">" + count + "</span>";
    return chip;
  }

  window.PFExplorer.registerPanel({
    id: "dashboard",
    mount: function (ctx) {
      var audited = ctx.app.getAuditedResults();
      var counts = {};
      audited.forEach(function (result) {
        counts[result.status] = (counts[result.status] || 0) + 1;
      });

      ctx.stage.innerHTML =
        "<div class=\"panel-wrap\">" +
          "<section class=\"hero-panel\">" +
            "<div class=\"hero-copy\">" +
              "<p class=\"eyebrow\">The Audit Wall</p>" +
              "<p class=\"hero-number\">" + audited.length + "</p>" +
              "<h3>A single registry for what is derived, what is conditional, and what is still only a signal.</h3>" +
              "<p class=\"story-only\">The explorer does not flatten the framework into one tone. Strong results stay strong, open frontiers stay open, and unsynced material is labeled before it can drift into the audited total.</p>" +
              "<p class=\"audit-only\">CLAIMS.md drives every audited row below. UNDERSTAND.md only extends coverage and copy. One current unsynced item is shown separately at the bottom.</p>" +
            "</div>" +
            "<div class=\"stat-grid\">" +
              "<div class=\"stat-tile\"><strong>" + (counts.DERIVED || 0) + "</strong><span>derived</span></div>" +
              "<div class=\"stat-tile\"><strong>" + (counts.CONDITIONAL || 0) + "</strong><span>conditional</span></div>" +
              "<div class=\"stat-tile\"><strong>" + (counts["PARTIAL DERIVATION"] || 0) + "</strong><span>partial derivation</span></div>" +
              "<div class=\"stat-tile\"><strong>" + (counts.ARGUED || 0) + "</strong><span>argued</span></div>" +
              "<div class=\"stat-tile\"><strong>" + (counts.EMPIRICAL || 0) + "</strong><span>empirical</span></div>" +
              "<div class=\"stat-tile\"><strong>" + (counts.INTUITION || 0) + "</strong><span>intuition</span></div>" +
              "<div class=\"stat-tile\"><strong>1</strong><span>unsynced item</span></div>" +
            "</div>" +
          "</section>" +
          "<div class=\"view-toggle\">" +
            "<button class=\"view-toggle-btn is-active\" data-view=\"list\">List View</button>" +
            "<button class=\"view-toggle-btn\" data-view=\"graph\">Derivation Graph</button>" +
            '<a href="derivation.html" class="view-toggle-btn" style="text-decoration:none;padding:8px 16px;border-radius:6px;background:rgba(255,255,255,0.06);color:var(--ui);">View Full Page →</a>' +
          "</div>" +
          "<div class=\"controls-row\" id=\"dashboardFilters\"></div>" +
          "<div class=\"controls-row\" id=\"dashboardSearchRow\">" +
            "<input type=\"text\" id=\"dashboardSearch\" placeholder=\"Search claims, formulas, falsifiers...\" class=\"search-input\">" +
          "</div>" +
          "<div class=\"group-list\" id=\"dashboardGroups\"></div>" +
          "<div class=\"graph-container\" id=\"derivationGraph\" style=\"display: none;\"></div>" +
        "</div>";

      this.state = {
        activeFilter: "all",
        searchQuery: "",
        currentView: "list",
        graph: null
      };

      this.renderFilters(ctx, counts);
      this.renderResults(ctx);
      this.bindEvents(ctx);
    },

    unmount: function () {
      if (this.state.graph) {
        this.state.graph.destroy();
      }
      this.state = null;
    },

    resize: function () {
      if (this.state.graph && this.state.currentView === "graph") {
        // Resize graph if needed
        const container = document.getElementById("derivationGraph");
        if (container) {
          container.style.height = Math.max(400, window.innerHeight - 400) + "px";
        }
      }
    },

    renderFilters: function (ctx, counts) {
      var filtersRoot = ctx.stage.querySelector("#dashboardFilters");
      var self = this;
      var filterConfig = [
        { label: "All", status: "all", count: ctx.app.getAuditedResults().length },
        { label: "Derived", status: "DERIVED", count: counts.DERIVED || 0 },
        { label: "Conditional", status: "CONDITIONAL", count: counts.CONDITIONAL || 0 },
        { label: "Partial", status: "PARTIAL DERIVATION", count: counts["PARTIAL DERIVATION"] || 0 },
        { label: "Argued", status: "ARGUED", count: counts.ARGUED || 0 },
        { label: "Empirical", status: "EMPIRICAL", count: counts.EMPIRICAL || 0 },
        { label: "Intuition", status: "INTUITION", count: counts.INTUITION || 0 }
      ];

      filtersRoot.innerHTML = "";

      filterConfig.forEach(function (config) {
        var chip = createFilterChip(config.label, config.status, self.state.activeFilter === config.status, config.count);
        chip.addEventListener("click", function () {
          self.state.activeFilter = config.status;
          self.renderFilters(ctx, counts);
          self.renderResults(ctx);
        });
        filtersRoot.appendChild(chip);
      });
    },

    renderResults: function (ctx) {
      var self = this;
      var groupsRoot = ctx.stage.querySelector("#dashboardGroups");
      if (!groupsRoot) {
        groupsRoot = document.createElement("div");
        groupsRoot.id = "dashboardGroups";
        groupsRoot.className = "group-list";
        ctx.stage.appendChild(groupsRoot);
      }

      var filteredResults = ctx.data.results.filter(function (result) {
        if (result.unsynced) return false;
        if (self.state.activeFilter !== "all" && result.status !== self.state.activeFilter) {
          return false;
        }
        return matchesQuery(result, self.state.searchQuery.toLowerCase());
      });

      groupsRoot.innerHTML = "";

      if (filteredResults.length === 0) {
        groupsRoot.innerHTML = "<p class=\"note-box\" style=\"text-align:center;padding:40px\">No results match your filters.</p>";
        return;
      }

      var grouped = {};
      filteredResults.forEach(function (result) {
        if (!grouped[result.kind]) {
          grouped[result.kind] = [];
        }
        grouped[result.kind].push(result);
      });

      Object.keys(grouped).forEach(function (kind) {
        var block = document.createElement("section");
        block.className = "group-block";
        block.innerHTML =
          "<div class=\"group-heading\"><h4>" + kind + "</h4><span class=\"metric-pill\">" +
            grouped[kind].length +
            " results</span></div>" +
          "<div class=\"result-strip\"></div>";
        var strip = block.querySelector(".result-strip");
        grouped[kind].sort(sortResults).forEach(function (result) {
          strip.appendChild(ctx.app.createResultCard(result, {
            wholeCardFocus: true,
            showInlineFalsifier: true,
            showInlineSources: true
          }));
        });
        groupsRoot.appendChild(block);
      });

      var unsynced = ctx.data.results.filter(function (result) {
        return result.unsynced && matchesQuery(result, self.state.searchQuery.toLowerCase());
      });
      if (unsynced.length) {
        var unsyncedBlock = document.createElement("section");
        unsyncedBlock.className = "group-block";
        unsyncedBlock.innerHTML =
          "<div class=\"group-heading\"><h4>Unsynced Context</h4><span class=\"metric-pill unsynced-note\">Excluded from totals</span></div>" +
          "<div class=\"result-strip\"></div>";
        var unsyncedStrip = unsyncedBlock.querySelector(".result-strip");
        unsynced.forEach(function (result) {
          unsyncedStrip.appendChild(ctx.app.createResultCard(result, {
            wholeCardFocus: true,
            hidePanelButton: true,
            showInlineFalsifier: true,
            showInlineSources: true
          }));
        });
        groupsRoot.appendChild(unsyncedBlock);
      }

      ctx.app.syncActiveResultCards();
    },

    bindEvents: function (ctx) {
      var self = this;
      var searchInput = ctx.stage.querySelector("#dashboardSearch");
      if (searchInput) {
        searchInput.addEventListener("input", function (event) {
          self.state.searchQuery = event.target.value;
          self.renderResults(ctx);
        });
      }
      
      // View toggle buttons
      var viewButtons = ctx.stage.querySelectorAll(".view-toggle-btn");
      viewButtons.forEach(function(btn) {
        btn.addEventListener("click", function() {
          viewButtons.forEach(b => b.classList.remove("is-active"));
          btn.classList.add("is-active");
          
          var view = btn.getAttribute("data-view");
          self.switchView(ctx, view);
        });
      });
    },
    
    switchView: function(ctx, view) {
      this.state.currentView = view;
      var listContainer = ctx.stage.querySelector("#dashboardGroups");
      var graphContainer = ctx.stage.querySelector("#derivationGraph");
      
      if (view === "graph") {
        listContainer.style.display = "none";
        graphContainer.style.display = "block";
        this.initGraph(ctx);
      } else {
        listContainer.style.display = "block";
        graphContainer.style.display = "none";
        if (this.state.graph) {
          this.state.graph.destroy();
          this.state.graph = null;
        }
      }
    },
    
    initGraph: function(ctx) {
      if (this.state.graph) {
        this.state.graph.destroy();
      }
      
      // Load D3 if not already loaded
      if (typeof d3 === "undefined") {
        var script = document.createElement("script");
        script.src = "https://d3js.org/d3.v7.min.js";
        script.onload = () => {
          this.createGraph(ctx);
        };
        document.head.appendChild(script);
      } else {
        this.createGraph(ctx);
      }
    },
    
    createGraph: function(ctx) {
      var container = document.getElementById("derivationGraph");
      if (!container || !window.DerivationGraph) return;
      
      // Set height
      container.style.height = Math.max(400, window.innerHeight - 400) + "px";
      
      // Create graph
      this.state.graph = new window.DerivationGraph(container, ctx.data);
    },

    update: function () {}
  });
}());
