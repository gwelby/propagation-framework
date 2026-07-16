/**
 * Framework Comparison — Interactive Logic
 * Propagation Framework Explorer
 */
(function () {
  "use strict";

  var PARAMS = {
    pf: 3,
    sm: 19,
    st: "10^500"
  };

  var counting = false;
  function getTruth() {
    return window.PFExplorerTruth || window.PFTruth;
  }
  var pfFalsifierIds = [
    "koide-law",
    "weinberg-angle",
    "god-equation",
    "forces-refraction",
    "bohr-quantization",
    "three-generations"
  ];

  document.addEventListener("DOMContentLoaded", function () {
    initParameterCounter();
    populatePFTruth();
    initInteractions();
  });

  function initParameterCounter() {
    var button = document.getElementById("count-params");
    if (!button) {
      return;
    }

    button.addEventListener("click", function () {
      if (counting) {
        return;
      }

      counting = true;
      button.textContent = "Counting...";

      animateCount("pf-count", 0, PARAMS.pf, 1000, "pf", function () {
        animateCount("sm-count", 0, PARAMS.sm, 1400, "sm", function () {
          var stCount = document.getElementById("st-count");
          if (stCount) {
            stCount.textContent = PARAMS.st;
            stCount.classList.add("st", "complete");
          }
          counting = false;
          button.textContent = "Count Again";
        });
      });
    });
  }

  function animateCount(elementId, start, end, duration, className, callback) {
    var element = document.getElementById(elementId);
    if (!element) {
      return;
    }

    element.classList.add(className);
    var range = end - start;
    var startTime = performance.now();

    function update(currentTime) {
      var elapsed = currentTime - startTime;
      var progress = Math.min(elapsed / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 4);
      var current = Math.floor(start + range * eased);

      element.textContent = current.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.classList.add("complete");
        if (callback) {
          callback();
        }
      }
    }

    requestAnimationFrame(update);
  }

  function populatePFTruth() {
    if (!getTruth()) {
      return;
    }

    var counts = getTruth().getCountsByStatus();
    var audited = getTruth().getAuditedResults();
    var falsifiableCount = audited.filter(function (result) {
      return result.falsifier;
    }).length;
    var derivedCount = counts.DERIVED || 0;
    var variableC = getTruth().getResult("variable-c");
    var koidePhase = getTruth().getResult("koide-phase");

    setText("pf-parameter-detail", "3 axioms • " + counts.total + " audited claims • " + derivedCount + " derived");
    setText("pf-free-cell", "3 axioms");
    setText("pf-derived-cell", counts.total + " audited claims • " + derivedCount + " derived");
    setText("pf-falsifiable-cell", "Yes (" + falsifiableCount + " audited falsifiers)");
    // V4: Pull status from authority, not hardcoded
    var threeGen = getTruth().getResult("three-generations");
    var bohr = getTruth().getResult("bohr-spectrum");
    var weinberg = getTruth().getResult("weinberg-angle");
    var godScale = getTruth().getResult("god-equation-scale");
    setText("pf-generations-cell", threeGen ? threeGen.badge : "UNAVAILABLE");
    setText("pf-atomic-cell", bohr ? bohr.badge : "UNAVAILABLE");
    setText("pf-weinberg-cell", weinberg ? weinberg.badge : "UNAVAILABLE");
    setText("pf-scale-cell", godScale ? godScale.badge : "UNAVAILABLE");
    setText(
      "pf-testable-cell",
      buildTestablePredictionLine(variableC, koidePhase)
    );

    populatePFFalsifierCard(falsifiableCount);
  }

  function buildTestablePredictionLine(variableC, koidePhase) {
    var parts = [];

    if (variableC) {
      parts.push("Variable c (" + variableC.status.toLowerCase() + ")");
    } else {
      parts.push("Variable c (argued)");
    }

    if (koidePhase) {
      parts.push("Koide phase (" + koidePhase.status.toLowerCase() + ")");
    } else {
      parts.push("Koide phase (empirical)");
    }

    return parts.join(", ");
  }

  function populatePFFalsifierCard(falsifiableCount) {
    if (!getTruth()) {
      return;
    }

    var list = document.getElementById("pf-falsify-list");
    if (!list) {
      return;
    }

    list.innerHTML = "";
    setText("pf-falsify-count", falsifiableCount + " audited falsifiers in current PF claim set");
    setText("pf-falsify-status", "✅ PF card sourced from audited claim text");

    pfFalsifierIds.forEach(function (id) {
      var result = getTruth().getResult(id);
      if (!result) {
        return;
      }

      var item = document.createElement("li");
      item.textContent = result.title + ": " + result.falsifier;
      list.appendChild(item);
    });
  }

  function initInteractions() {
    document.querySelectorAll(".comparison-table tbody tr").forEach(function (row) {
      row.addEventListener("mouseenter", function () {
        row.querySelectorAll("td").forEach(function (cell) {
          cell.style.background = "rgba(0, 207, 255, 0.08)";
        });
      });

      row.addEventListener("mouseleave", function () {
        row.querySelectorAll("td").forEach(function (cell) {
          cell.style.background = "";
        });
      });
    });

    document.querySelectorAll(".falsify-card").forEach(function (card) {
      card.addEventListener("click", function () {
        card.classList.toggle("expanded");
      });
    });

    document.querySelectorAll(".scale-segment").forEach(function (segment) {
      segment.addEventListener("mouseenter", function () {
        var frameworks = segment.getAttribute("data-frameworks") || segment.getAttribute("data-framework");
        if (frameworks) {
          segment.style.transform = "scale(1.05)";
          segment.style.zIndex = "10";
        }
      });

      segment.addEventListener("mouseleave", function () {
        segment.style.transform = "";
        segment.style.zIndex = "";
      });
    });

    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener("click", function (event) {
        var href = this.getAttribute("href");
        if (href === "#") {
          return;
        }

        event.preventDefault();
        var target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });
        }
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        document.querySelectorAll(".falsify-card.expanded").forEach(function (card) {
          card.classList.remove("expanded");
        });
      }
    });
  }

  function setText(id, value) {
    var node = document.getElementById(id);
    if (node) {
      node.textContent = value;
    }
  }
})();
