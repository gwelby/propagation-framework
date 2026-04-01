/**
 * truth-utils.js
 * Shared helper for narrative pages that read audited PF truth from data.js.
 */
(function () {
  "use strict";

  var STATUS_ORDER = {
    "DERIVED": 0,
    "CONDITIONAL": 1,
    "PARTIAL DERIVATION": 2,
    "ARGUED": 3,
    "EMPIRICAL": 4,
    "INTUITION": 5,
    "OPEN": 6,
    "UNSYNCED": 7
  };

  var STATUS_CLASS_MAP = {
    "DERIVED": "status-derived",
    "CONDITIONAL": "status-conditional",
    "PARTIAL DERIVATION": "status-partial",
    "ARGUED": "status-argued",
    "EMPIRICAL": "status-empirical",
    "INTUITION": "status-intuition",
    "OPEN": "status-open",
    "UNSYNCED": "status-unsynced"
  };

  function getResults() {
    return window.PFExplorerData && Array.isArray(window.PFExplorerData.results)
      ? window.PFExplorerData.results
      : [];
  }

  function getAuditedResults() {
    return getResults().filter(function (result) {
      return !result.unsynced && result.status !== "UNSYNCED";
    });
  }

  function getCountsByStatus() {
    return getAuditedResults().reduce(function (counts, result) {
      counts.total += 1;
      counts[result.status] = (counts[result.status] || 0) + 1;
      return counts;
    }, { total: 0 });
  }

  function getResult(id) {
    return getResults().find(function (result) {
      return result.id === id;
    });
  }

  function statusToClass(status) {
    return STATUS_CLASS_MAP[status] || "status-open";
  }

  function sortResultsForNarrative(results) {
    return results.slice().sort(function (a, b) {
      var tierA = STATUS_ORDER[a.status] !== undefined ? STATUS_ORDER[a.status] : 99;
      var tierB = STATUS_ORDER[b.status] !== undefined ? STATUS_ORDER[b.status] : 99;

      if (tierA !== tierB) {
        return tierA - tierB;
      }

      return (b.confidence || 0) - (a.confidence || 0);
    });
  }

  var api = {
    getAuditedResults: getAuditedResults,
    getCountsByStatus: getCountsByStatus,
    getResult: getResult,
    statusToClass: statusToClass,
    sortResultsForNarrative: sortResultsForNarrative,

    // Compatibility aliases for any existing narrative code.
    getResults: getResults,
    getCounts: getCountsByStatus,
    sortResults: sortResultsForNarrative
  };

  window.PFTruth = api;
  window.PFExplorerTruth = api;
})();
