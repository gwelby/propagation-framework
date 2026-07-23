/**
 * truth-utils.js — V2
 *
 * Shared helper for narrative pages and the explorer shell.
 * Provides a unified API to the generated claims data.
 *
 * V2: The dual-source split (PFDataGraph vs PFClaimsData) has been eliminated.
 * data.claims.js is the single generated source. data.graph.js is a thin alias.
 * This file adapts the generated format to what panels expect.
 */

(function () {
  "use strict";

  // Status mapping for CSS classes and ordering
  var STATUS_ORDER = {
    "DERIVED": 0,
    "EXACT IDENTITY": 0,
    "CONDITIONAL": 1,
    "ARGUED": 3,
    "EMPIRICAL": 4,
    "INTUITION": 5,
    "OPEN": 6,
    "CANONICAL": 0,
    "STANDARD MATH": 0,
    "UNSYNCED": 7
  };

  var STATUS_CLASS_MAP = {
    "DERIVED": "status-derived",
    "EXACT IDENTITY": "status-derived",
    "CONDITIONAL": "status-conditional",
    "ARGUED": "status-argued",
    "EMPIRICAL": "status-empirical",
    "INTUITION": "status-intuition",
    "OPEN": "status-open",
    "CANONICAL": "status-canonical",
    "STANDARD MATH": "status-standard-math",
    "UNSYNCED": "status-unsynced"
  };

  // Status objects for legacy panel compatibility
  var STATUS = {
    DERIVED: { label: "DERIVED", color: "green", ring: true },
    "EXACT IDENTITY": { label: "EXACT IDENTITY", color: "green", ring: true },
    CONDITIONAL: { label: "CONDITIONAL", color: "amber", ring: true },
    ARGUED: { label: "ARGUED", color: "amber", ring: false },
    EMPIRICAL: { label: "EMPIRICAL", color: "gold", ring: false },
    INTUITION: { label: "INTUITION", color: "gray", ring: false },
    CANONICAL: { label: "CANONICAL", color: "white", ring: true },
    "STANDARD MATH": { label: "STANDARD MATH", color: "blue", ring: true },
    NOGO: { label: "NO-GO", color: "red", ring: false },
    OPEN: { label: "OPEN", color: "gray", ring: false },
    UNSYNCED: { label: "UNSYNCED", color: "gray", ring: false }
  };

  /**
   * Core Accessors — read from the generated PFClaimsData
   */
  function getData() {
    return window.PFClaimsData || window.PFDataGraph || {
      generatedAt: "missing",
      claims: [],
      definitions: []
    };
  }

  function getDefinitions() {
    var data = getData();
    // V2 format: data.definitions (array of objects with id, title, status, file)
    // Legacy format: data.DEFINITIONS
    return data.definitions || data.DEFINITIONS || [];
  }

  function getClaims() {
    var data = getData();
    // V2 format: data.claims (array of objects with id, title, status, confidence)
    // Legacy format: data.CLAIMS
    return data.claims || data.CLAIMS || [];
  }

  function getNoGos() {
    var data = getData();
    return data.noGos || data.NOGOS || [];
  }

  function getDefinition(id) {
    return getDefinitions().find(function (d) { return d.id === id; });
  }

  function getClaim(id) {
    return getClaims().find(function (c) { return c.id === id; });
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
        var parts = rgbStr.split(',').map(function (s) { return parseInt(s.trim(), 10); });
        if (parts.length >= 3 && !isNaN(parts[0])) {
          return (parts[0] << 16) | (parts[1] << 8) | parts[2];
        }
      }
    }
    var fallbacks = {
      'propagate': 0x00cfff, 'planck': 0xffdd55, 'cohere': 0x44ff88,
      'refract': 0xff9955, 'axiom': 0xc8a8ff, 'cosmic': 0x7c5cbf,
      'uncertain': 0xff4757, 'resonate': 0xff6b9d, 'surface': 0x091525,
      'deep': 0x050d1a, 'void': 0x020408
    };
    return fallbacks[tokenName] || 0xffffff;
  }

  /**
   * V3 Legacy Compatibility Layer
   * Adapts generated format to what panels expect (DEFINITIONS, CLAIMS, STATUS)
   * Also syncs PFExplorerData results to use authority statuses from PFClaimsData.
   * PFExplorerData, PFClaimsData, and PFDataGraph are all views of one authority.
   */
  function syncLegacyData() {
    var data = getData();
    var claims = getClaims();
    var defs = getDefinitions();

    // Build legacy DEFINITIONS array
    var legacyDefs = defs.map(function (d) {
      return {
        id: d.id,
        title: d.title,
        file: d.file || "",
        oneLiner: d.oneLiner || d.summary || "",
        storyLine: d.storyLine || d.summary || "",
        auditLine: d.status || d.auditLine || "CANONICAL v1.0",
        notThis: d.notThis || ("See " + (d.file || d.id)),
        dependencies: d.dependencies || []
      };
    });

    // Build legacy CLAIMS array
    var legacyClaims = claims.map(function (c) {
      var statusStr = c.status || "UNAVAILABLE";
      var legacyStatus = STATUS[statusStr] || STATUS.OPEN;
      if (c.isSplit && c.badge) {
        legacyStatus = { label: c.badge, color: "amber", ring: true };
      }
      if (c.isStandardMath) {
        legacyStatus = STATUS["STANDARD MATH"];
      }
      return {
        id: c.id,
        title: c.title,
        status: legacyStatus,
        confidence: c.confidence,
        isSplit: c.isSplit || false,
        isStandardMath: c.isStandardMath || false,
        badge: c.badge || statusStr,
        statusClass: c.statusClass || statusToClass(statusStr),
        falsifier: c.falsifier || "",
        premise: c.premise || "",
        scopeNote: c.scopeNote || "",
        sourceLine: c.sourceLine || 0,
        audit: {
          claim: c.title,
          falsifier: c.falsifier || "",
          standardBoundary: c.premise || "",
          openBridge: c.scopeNote || ""
        },
        story: c.story || c.summary || c.evidence || "",
        math: c.math || c.formula || "",
        sources: c.sources || [],
        citations: c.citations || []
      };
    });

    // Set the legacy format on PFClaimsData for panels that read it
    window.PFClaimsData = window.PFClaimsData || {};
    window.PFClaimsData.STATUS = STATUS;
    window.PFClaimsData.DEFINITIONS = legacyDefs;
    window.PFClaimsData.CLAIMS = legacyClaims;
    window.PFClaimsData.NOGOS = getNoGos();
    window.PFClaimsData.SCALE_ANCHORS = data.scales || data.SCALE_ANCHORS || [];

    // V3: Sync PFExplorerData results to use authority statuses
    // PFExplorerData is generated by data.js (V3) with statuses from authority.
    // If PFExplorerData exists, verify its results match authority.
    if (window.PFExplorerData && window.PFExplorerData.results) {
      var authClaims = {};
      claims.forEach(function (c) { authClaims[c.id] = c; });
      // Crosswalk: result ID → authority claim ID
      var crosswalk = data.result_to_authority || {};
      window.PFExplorerData.results.forEach(function (r) {
        var authIds = r.authorityClaimIds || [];
        if (authIds.length > 0) {
          var primaryAuth = authClaims[authIds[0]];
          if (primaryAuth) {
            r.status = primaryAuth.status;
            r.confidence = primaryAuth.confidence;
            r.badge = primaryAuth.badge || primaryAuth.status;
            r.statusClass = primaryAuth.statusClass || statusToClass(primaryAuth.status);
            r.isSplit = primaryAuth.isSplit || false;
            r.isStandardMath = primaryAuth.isStandardMath || false;
          }
        }
      });
    }

    // All three names point to deterministic views of the same authority
    window.PFDataGraph = window.PFClaimsData;
    // PFExplorerData stays as generated (data.js), but its statuses are synced above
  }

  // V4: Add getCountsByStatus and getAuditedResults to the PFTruth API
  function getCountsByStatus() {
    var claims = getClaims();
    var counts = {};
    claims.forEach(function (c) {
      var s = c.status || c.primary_status || 'UNKNOWN';
      counts[s] = (counts[s] || 0) + 1;
    });
    return counts;
  }

  function getAuditedResults() {
    // V5.5: Prefer the curated PFExplorerData.results snapshot; it carries
    // authorityClaimIds, derivation links, summaries, and source metadata.
    if (window.PFExplorerData && window.PFExplorerData.results) {
      return window.PFExplorerData.results;
    }
    var data = getData();
    if (data && data.results) {
      return data.results;
    }
    // Fallback: derive from claims
    var claims = getClaims();
    return claims.map(function (c) {
      return {
        id: c.id,
        title: c.title,
        status: c.status || c.primary_status,
        confidence: c.confidence,
        section: c.section,
        isStandardMath: c.isStandardMath || false,
        badge: c.badge || (c.status || c.primary_status || ""),
        authorityClaimIds: [c.id]
      };
    });
  }

  function getResult(id) {
    var results = getAuditedResults();
    return results.find(function (r) { return r.id === id; }) || null;
  }

  function sortResultsForNarrative(results) {
    // Sort results by confidence descending for narrative display
    return results.slice().sort(function (a, b) {
      var ca = a.confidence || 0;
      var cb = b.confidence || 0;
      return cb - ca;
    });
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
    syncLegacyData: syncLegacyData,
    STATUS: STATUS,
    getCountsByStatus: getCountsByStatus,
    getAuditedResults: getAuditedResults,
    getResult: getResult,
    sortResultsForNarrative: sortResultsForNarrative
  };

  window.PFTruth = api;
  window.PFExplorerTruth = api;

  // Auto-sync: adapt generated data to legacy panel format
  // This runs after data.graph.js (stub) but before data.claims.js (generated)
  // We poll for data.claims.js to load, then sync
  function trySync() {
    if (window.PFClaimsData && window.PFClaimsData.claims && window.PFClaimsData.claims.length > 0) {
      syncLegacyData();
      if (window.PFExplorer && typeof window.PFExplorer.renderSidebarMetrics === 'function') {
        window.PFExplorer.renderSidebarMetrics();
      }
      return true;
    }
    return false;
  }

  if (!trySync()) {
    var attempts = 0;
    var poller = setInterval(function () {
      attempts++;
      if (trySync() || attempts > 20) {
        clearInterval(poller);
      }
    }, 50);
  }
})();
