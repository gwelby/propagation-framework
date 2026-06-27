/**
 * truth-utils.js
 * 
 * Shared helper for narrative pages and the explorer shell.
 * Provides a unified API to the PF Data Graph.
 * 
 * Acts as a bridge between the raw data.graph.js manifest and the UI panels.
 */

(function () {
  "use strict";

  // Status mapping for CSS classes and ordering
  const STATUS_ORDER = {
    "DERIVED": 0,
    "CONDITIONAL": 1,
    "PARTIAL DERIVATION": 2,
    "ARGUED": 3,
    "EMPIRICAL": 4,
    "INTUITION": 5,
    "OPEN": 6,
    "UNSYNCED": 7
  };

  const STATUS_CLASS_MAP = {
    "DERIVED": "status-derived",
    "CONDITIONAL": "status-conditional",
    "PARTIAL DERIVATION": "status-partial",
    "ARGUED": "status-argued",
    "EMPIRICAL": "status-empirical",
    "INTUITION": "status-intuition",
    "OPEN": "status-open",
    "UNSYNCED": "status-unsynced",
    "CANONICAL v1.0": "status-canonical"
  };

  /**
   * Core Accessors
   */

  function getData() {
    return window.PFDataGraph || {
      generatedAt: "legacy-fallback",
      definitions: [],
      claims: [],
      noGos: [],
      scales: [],
      experiments: []
    };
  }

  function getDefinitions() {
    return getData().definitions || [];
  }

  function getClaims() {
    return getData().claims || [];
  }

  function getNoGos() {
    return getData().noGos || [];
  }

  function getDefinition(id) {
    return getDefinitions().find(d => d.id === id);
  }

  function getClaim(id) {
    return getClaims().find(c => c.id === id);
  }

  /**
   * Formatting & Styling
   */

  function statusToClass(status) {
    return STATUS_CLASS_MAP[status] || "status-open";
  }

  function getColor(tokenName) {
    if (typeof window !== 'undefined' && window.getComputedStyle) {
      var rgbStr = window.getComputedStyle(document.documentElement).getPropertyValue('--' + tokenName + '-rgb');
      if (rgbStr) {
        var parts = rgbStr.split(',').map(function(s) { return parseInt(s.trim(), 10); });
        if (parts.length >= 3 && !isNaN(parts[0])) {
          return (parts[0] << 16) | (parts[1] << 8) | parts[2];
        }
      }
    }
    const fallbacks = {
      'propagate': 0x00cfff, 'planck': 0xffdd55, 'cohere': 0x44ff88,
      'refract': 0xff9955, 'axiom': 0xc8a8ff, 'cosmic': 0x7c5cbf,
      'uncertain': 0xff4757, 'resonate': 0xff6b9d, 'surface': 0x091525,
      'deep': 0x050d1a, 'void': 0x020408
    };
    return fallbacks[tokenName] || 0xffffff;
  }

  /**
  /**
   * Compatibility Layer for Legacy Panels (window.PFClaimsData)
   */
  function syncLegacyData() {
    var data = getData();
    var STATUS = {
      DERIVED: { label: "DERIVED", color: "green", ring: true },
      CONDITIONAL: { label: "CONDITIONAL", color: "amber", ring: true },
      ARGUED: { label: "ARGUED", color: "amber", ring: false },
      EMPIRICAL: { label: "EMPIRICAL", color: "gold", ring: false },
      INTUITION: { label: "INTUITION", color: "gray", ring: false },
      CANONICAL: { label: "CANONICAL", color: "white", ring: true },
      NOGO: { label: "NO-GO", color: "red", ring: false },
      OPEN: { label: "OPEN", color: "gray", ring: false },
      UNSYNCED: { label: "UNSYNCED", color: "gray", ring: false }
    };

    window.PFClaimsData = {
      STATUS: STATUS,
      DEFINITIONS: (data.definitions || []).map(function (d) {
        return {
          id: d.id,
          title: d.title,
          file: d.file,
          oneLiner: d.oneLiner || d.summary || "",
          storyLine: d.storyLine || d.summary || "",
          auditLine: d.status || "CANONICAL v1.0",
          notThis: "See " + (d.file || d.id),
          dependencies: d.dependencies || []
        };
      }),
      CLAIMS: (data.claims || []).map(function (c) {
        var legacyStatus = STATUS[c.status] || STATUS.OPEN;
        return {
          id: c.id,
          title: c.title,
          status: legacyStatus,
          confidence: c.confidence,
          falsifier: c.falsifier,
          evidence: c.evidence,
          audit: {
            claim: c.title,
            falsifier: c.falsifier
          },
          story: c.summary,
          math: c.formula,
          scaleId: c.scaleId
        };
      }),
      NOGOS: (data.noGos || []).map(function (n) {
        // Map frontier labels to stable claim IDs
        var targetId = n.target || n.targetFrontier;
        if (targetId === 'koide') targetId = 'koide-leptons';
        if (targetId === 'weinberg') targetId = 'weinberg-angle';
        if (targetId === 'generations') targetId = 'three-generations';

        return {
          id: n.id,
          title: n.title,
          target: targetId || "koide-leptons",
          failedAt: n.date || n.failedAt || "—",
          failedAssumption: n.failureMode || n.failedAssumption || "—",
          lesson: n.lesson || "—",
          whyFailed: n.whyFailed || [],
          statusType: n.statusType || "FAILED"
        };
      }),
      SCALE_ANCHORS: data.scales || []
    };
  }

  var api = {
    getData: getData,
    getDefinitions: getDefinitions,
    getClaims: getClaims,
    getNoGos: getNoGos,
    getDefinition: getDefinition,
    getClaim: getClaim,
    statusToClass: statusToClass,
    getColor: getColor,
    syncLegacyData: syncLegacyData
  };

  window.PFTruth = api;
  window.PFExplorerTruth = api;

  // Auto-sync if data is present, but respect existing PFClaimsData from data.claims.js
  if (window.PFClaimsData && window.PFClaimsData.CLAIMS && window.PFClaimsData.CLAIMS.length > 0) {
    // data.claims.js already loaded — do not overwrite with legacy graph data
  } else if (window.PFDataGraph) {
    syncLegacyData();
  } else {
    // Polling fallback
    var attempts = 0;
    var poller = setInterval(function() {
      attempts++;
      if (window.PFClaimsData && window.PFClaimsData.CLAIMS && window.PFClaimsData.CLAIMS.length > 0) {
        clearInterval(poller);  // data.claims.js loaded — respect it
        return;
      }
      if (window.PFDataGraph) {
        syncLegacyData();
        clearInterval(poller);
        if (window.PFExplorer && typeof window.PFExplorer.renderSidebarMetrics === 'function') {
          window.PFExplorer.renderSidebarMetrics();
        }
      }
      if (attempts > 20) clearInterval(poller);
    }, 100);
  }
})();

