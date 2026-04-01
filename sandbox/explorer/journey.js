/**
 * Journey Mode — The 8-Minute Narrative Experience
 * Propagation Framework Explorer
 */
(function () {
  "use strict";

  var currentSection = "opening";
  var sections = ["opening", "act1", "act2", "act3", "act4", "epilogue"];
  var truth = window.PFExplorerTruth || window.PFTruth;

  var bohrCtx = null;
  var generationsCtx = null;
  var godEqCtx = null;

  var bohrState = {
    started: false,
    electron: null,
    orbits: [],
    wavePackets: [],
    phaseAccumulation: 0,
    showPhaseClosure: true
  };

  var generationsState = {
    started: false,
    rotation: 0,
    isDragging: false,
    lastX: 0,
    currentN: 3
  };

  var godEquationState = {
    started: false,
    currentN: 3,
    currentD: 3,
    currentLambda: 1.145e-18,
    animationTime: 0,
    rgCurve: [],
    isAnimating: false
  };

  var falsificationIds = [
    "koide-law",
    "weinberg-angle",
    "god-equation",
    "forces-refraction",
    "bohr-quantization",
    "three-generations"
  ];

  var falsificationMeta = {
    "koide-law": { icon: "🔬", title: "Break the Koide relation" },
    "weinberg-angle": { icon: "🔭", title: "Break the Weinberg angle" },
    "god-equation": { icon: "🌌", title: "Break the God Equation" },
    "forces-refraction": { icon: "💫", title: "Break the optical force map" },
    "bohr-quantization": { icon: "⚛️", title: "Break the circular-eikonal Bohr sector" },
    "three-generations": { icon: "🧬", title: "Break the N = 3 lock" }
  };

  document.addEventListener("DOMContentLoaded", function () {
    initNavigation();
    initOpening();
    initAct1();
    initAct2();
    initAct3();
    initAct4();
    initEpilogue();
    updateProgress();
  });

  function getTruth() {
    return truth || window.PFExplorerTruth || window.PFTruth;
  }

  function initNavigation() {
    document.querySelectorAll(".next-act").forEach(function (button) {
      button.addEventListener("click", function () {
        var currentIndex = sections.indexOf(currentSection);
        if (currentIndex < sections.length - 1) {
          goToSection(sections[currentIndex + 1]);
        }
      });
    });

    document.querySelectorAll(".progress-step").forEach(function (step) {
      step.addEventListener("click", function () {
        goToSection(step.dataset.step);
      });
    });
  }

  function goToSection(sectionId) {
    var currentNode = document.getElementById("journey-" + currentSection);
    var nextNode = document.getElementById("journey-" + sectionId);

    if (currentNode) {
      currentNode.classList.remove("active");
    }
    if (nextNode) {
      nextNode.classList.add("active");
    }

    currentSection = sectionId;
    updateProgress();

    if (sectionId === "act1") {
      ensureBohrAnimation();
    }
    if (sectionId === "act2") {
      ensureGenerationsAnimation();
      renderGenerationsScene(generationsState.currentN);
    }
    if (sectionId === "act3") {
      ensureGodEquationAnimation();
      refreshGodEquation();
    }
    if (sectionId === "act4") {
      populateAct4();
    }
    if (sectionId === "epilogue") {
      populateFalsificationCards();
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function updateProgress() {
    var currentIndex = sections.indexOf(currentSection);
    document.querySelectorAll(".progress-step").forEach(function (step, index) {
      step.classList.remove("active", "completed");
      if (index === currentIndex) {
        step.classList.add("active");
      } else if (index < currentIndex) {
        step.classList.add("completed");
      }
    });
  }

  function initOpening() {
    var beginButton = document.getElementById("begin-journey");
    if (beginButton) {
      beginButton.addEventListener("click", function () {
        goToSection("act1");
      });
    }

    setTimeout(function () {
      document.querySelectorAll(".axiom-card").forEach(function (card, index) {
        setTimeout(function () {
          card.classList.add("revealed");
        }, index * 400);
      });
    }, 500);
  }

  function initAct1() {
    var canvas = document.getElementById("bohr-canvas");
    if (!canvas) {
      return;
    }

    bohrCtx = canvas.getContext("2d");
    bohrState.orbits = buildBohrOrbits();
    bohrState.electron = {
      phase: 0,
      targetOrbit: bohrState.orbits[0]
    };
  }

  function buildBohrOrbits() {
    var orbits = [];
    // Include both integer and non-integer orbits to show phase closure
    for (var k = 1; k <= 4; k += 0.5) {
      orbits.push({
        k: k,
        radius: 2 * k * k,
        energy: -1 / (4 * k * k),
        phase: 0,
        isInteger: k === Math.floor(k)
      });
    }
    return orbits;
  }

  function ensureBohrAnimation() {
    var canvas = document.getElementById("bohr-canvas");
    if (!canvas || bohrState.started) {
      if (canvas) {
        resizeCanvas(canvas);
      }
      return;
    }

    resizeCanvas(canvas);
    bohrState.started = true;

    canvas.addEventListener("click", function (event) {
      var rect = canvas.getBoundingClientRect();
      var localX = event.clientX - rect.left - canvas.width / 2;
      var localY = event.clientY - rect.top - canvas.height / 2;
      var dist = Math.max(1, Math.sqrt(localX * localX + localY * localY));
      var scale = bohrOrbitScreenScale(canvas);

      var closestOrbit = bohrState.orbits.reduce(function (best, orbit) {
        return Math.abs(dist - orbit.radius * scale) < Math.abs(dist - best.radius * scale)
          ? orbit
          : best;
      }, bohrState.orbits[0]);

      bohrState.electron = {
        phase: 0,
        targetOrbit: closestOrbit
      };
    });

    requestAnimationFrame(animateBohr);
  }

  function bohrOrbitScreenScale(canvas) {
    return Math.min(canvas.width, canvas.height) * 0.08;
  }

  function animateBohr() {
    var canvas = document.getElementById("bohr-canvas");
    if (!canvas || !bohrCtx) {
      return;
    }

    var ctx = bohrCtx;
    var w = canvas.width;
    var h = canvas.height;
    var cx = w / 2;
    var cy = h / 2;
    var scale = bohrOrbitScreenScale(canvas);

    // Clear canvas with fade effect
    ctx.fillStyle = "rgba(15, 15, 31, 0.95)";
    ctx.fillRect(0, 0, w, h);

    // Draw nucleus with pulsing effect
    const nucleusPulse = Math.sin(Date.now() * 0.002) * 2 + 8;
    ctx.beginPath();
    ctx.arc(cx, cy, nucleusPulse, 0, Math.PI * 2);
    ctx.fillStyle = "#ff5555";
    ctx.shadowColor = "#ff5555";
    ctx.shadowBlur = 18 + Math.sin(Date.now() * 0.003) * 5;
    ctx.fill();
    ctx.shadowBlur = 0;

    // Draw nucleus glow layers
    for (let i = 3; i > 0; i--) {
      ctx.beginPath();
      ctx.arc(cx, cy, nucleusPulse + i * 5, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 85, 85, ${0.1 / i})`;
      ctx.fill();
    }

    // Draw orbits and wave packets
    bohrState.orbits.forEach(function (orbit) {
      var screenRadius = orbit.radius * scale;
      var isActive = bohrState.electron && bohrState.electron.targetOrbit.k === orbit.k;
      var isInteger = orbit.k === Math.floor(orbit.k);

      // Draw orbit path
      ctx.beginPath();
      ctx.arc(cx, cy, screenRadius, 0, Math.PI * 2);
      ctx.strokeStyle = isActive ? "#44ff88" : "#333";
      ctx.lineWidth = isActive ? 3 : 1;
      ctx.stroke();

      // Draw wave packet if active
      if (isActive && bohrState.showPhaseClosure) {
        // Create wave packet visualization
        var wavePoints = 100;
        var wavelength = (2 * Math.PI * screenRadius) / (orbit.k * 4);
        
        ctx.beginPath();
        for (var i = 0; i <= wavePoints; i++) {
          var angle = (i / wavePoints) * Math.PI * 2;
          var waveX = cx + Math.cos(angle) * screenRadius;
          var waveY = cy + Math.sin(angle) * screenRadius;
          
          // Wave amplitude based on phase closure
          var phase = (angle * orbit.k) + orbit.phase;
          var amplitude = isInteger ? 15 : 5;
          var waveOffset = Math.sin(phase) * amplitude;
          
          waveX += Math.cos(angle) * waveOffset;
          waveY += Math.sin(angle) * waveOffset;
          
          if (i === 0) {
            ctx.moveTo(waveX, waveY);
          } else {
            ctx.lineTo(waveX, waveY);
          }
        }
        
        ctx.closePath();
        ctx.strokeStyle = isInteger ? "rgba(68, 255, 136, 0.6)" : "rgba(255, 170, 0, 0.3)";
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Fill wave for integer orbits (constructive interference)
        if (isInteger) {
          ctx.fillStyle = "rgba(68, 255, 136, 0.1)";
          ctx.fill();
        }

        // Update phase for animation
        orbit.phase += 0.05;
        
        // Draw phase accumulation indicator
        var phaseClosure = (orbit.phase % (2 * Math.PI)) / (2 * Math.PI);
        ctx.beginPath();
        ctx.arc(cx, cy, 5, 0, phaseClosure * Math.PI * 2);
        ctx.strokeStyle = "#00cfff";
        ctx.lineWidth = 3;
        ctx.stroke();
      }
    });

    // Draw electron as wave packet
    if (bohrState.electron && bohrState.electron.targetOrbit) {
      var activeOrbit = bohrState.electron.targetOrbit;
      var radius = activeOrbit.radius * scale;
      bohrState.electron.phase += 0.08;
      var ex = cx + Math.cos(bohrState.electron.phase) * radius;
      var ey = cy + Math.sin(bohrState.electron.phase) * radius;

      // Electron trail effect
      for (let i = 5; i > 0; i--) {
        const trailPhase = bohrState.electron.phase - i * 0.1;
        const trailX = cx + Math.cos(trailPhase) * radius;
        const trailY = cy + Math.sin(trailPhase) * radius;
        
        ctx.beginPath();
        ctx.arc(trailX, trailY, 4 - i * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 207, 255, ${0.1 * (6 - i) / 6})`;
        ctx.fill();
      }

      // Electron wave packet with gradient
      var gradient = ctx.createRadialGradient(ex, ey, 0, ex, ey, 20);
      gradient.addColorStop(0, "rgba(255, 255, 255, 1)");
      gradient.addColorStop(0.2, "rgba(0, 207, 255, 1)");
      gradient.addColorStop(0.5, "rgba(0, 207, 255, 0.5)");
      gradient.addColorStop(1, "rgba(0, 207, 255, 0)");
      
      ctx.beginPath();
      ctx.arc(ex, ey, 20, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
      
      // Core particle with glow
      ctx.beginPath();
      ctx.arc(ex, ey, 6, 0, Math.PI * 2);
      ctx.fillStyle = "#ffffff";
      ctx.shadowColor = "#00cfff";
      ctx.shadowBlur = 20;
      ctx.fill();
      ctx.shadowBlur = 0;
      
      // Wave function visualization
      ctx.strokeStyle = "rgba(0, 207, 255, 0.3)";
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.arc(ex, ey, 25, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Draw energy level diagram
    ctx.fillStyle = "#888";
    ctx.font = "12px monospace";
    ctx.textAlign = "right";
    bohrState.orbits.forEach(function (orbit, index) {
      var y = h - 30 - index * 25;
      var isInteger = orbit.k === Math.floor(orbit.k);
      var isActive = bohrState.electron && bohrState.electron.targetOrbit.k === orbit.k;
      
      // Energy level line
      ctx.beginPath();
      ctx.moveTo(w - 150, y - 8);
      ctx.lineTo(w - 20, y - 8);
      ctx.strokeStyle = isActive ? "#44ff88" : isInteger ? "#666" : "#444";
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Energy text
      ctx.fillStyle = isActive ? "#44ff88" : isInteger ? "#aaa" : "#666";
      ctx.fillText("k=" + orbit.k + ": E = " + orbit.energy.toFixed(4), w - 160, y);
      
      // Phase closure indicator
      if (isActive && isInteger) {
        ctx.fillStyle = "#44ff88";
        ctx.fillText("✓ Phase closure", w - 160, y + 15);
      } else if (isActive && !isInteger) {
        ctx.fillStyle = "#ffaa00";
        ctx.fillText("✗ No closure", w - 160, y + 15);
      }
    });

    // Phase accumulation display
    if (bohrState.electron && bohrState.electron.targetOrbit) {
      var activeOrbit = bohrState.electron.targetOrbit;
      var phase = (bohrState.electron.phase * activeOrbit.k) % (2 * Math.PI);
      var closurePercent = (phase / (2 * Math.PI)) * 100;
      
      ctx.fillStyle = "#00cfff";
      ctx.font = "14px monospace";
      ctx.textAlign = "left";
      ctx.fillText("Phase Accumulation: " + closurePercent.toFixed(1) + "%", 20, 30);
      
      // Phase bar
      ctx.fillStyle = "#333";
      ctx.fillRect(20, 40, 200, 10);
      ctx.fillStyle = "#00cfff";
      ctx.fillRect(20, 40, (closurePercent / 100) * 200, 10);
      
      // Axiom 3 display
      ctx.fillStyle = "#888";
      ctx.font = "12px monospace";
      ctx.fillText("∮ n·ds = 2πk (Axiom 3)", 20, 70);
    }

    requestAnimationFrame(animateBohr);
  }

  function initAct2() {
    var canvas = document.getElementById("generations-canvas");
    var slider = document.getElementById("n-slider");
    if (!canvas || !slider) {
      return;
    }

    generationsCtx = canvas.getContext("2d");
    generationsState.currentN = parseInt(slider.value, 10);

    slider.addEventListener("input", function () {
      generationsState.currentN = parseInt(slider.value, 10);
      refreshGenerationsText();
      if (currentSection === "act2") {
        renderGenerationsScene(generationsState.currentN);
      }
    });

    refreshGenerationsText();
  }

  function ensureGenerationsAnimation() {
    var canvas = document.getElementById("generations-canvas");
    if (!canvas) {
      return;
    }

    resizeCanvas(canvas);
    if (generationsState.started) {
      return;
    }

    generationsState.started = true;

    canvas.addEventListener("mousedown", function (event) {
      generationsState.isDragging = true;
      generationsState.lastX = event.clientX;
    });

    canvas.addEventListener("mousemove", function (event) {
      if (!generationsState.isDragging) {
        return;
      }
      generationsState.rotation += (event.clientX - generationsState.lastX) * 0.02;
      generationsState.lastX = event.clientX;
    });

    ["mouseup", "mouseleave"].forEach(function (type) {
      canvas.addEventListener(type, function () {
        generationsState.isDragging = false;
      });
    });

    requestAnimationFrame(animateGenerations);
  }

  function refreshGenerationsText() {
    var nValue = document.getElementById("n-value");
    var qResult = document.getElementById("q-result");
    var lockIndicator = document.getElementById("lock-indicator");
    var N = generationsState.currentN;
    var qValue = (2 * N) / (2 * N + 3);

    if (nValue) {
      nValue.textContent = N;
    }

    if (qResult) {
      qResult.textContent = "Q(" + N + ") = " + (2 * N) + "/" + (2 * N + 3) + " = " + qValue.toFixed(6);
    }

    if (lockIndicator) {
      if (N === 3) {
        lockIndicator.style.display = "block";
        lockIndicator.textContent = "Conditional lock once T1 and T2 are granted";
      } else {
        lockIndicator.style.display = "block";
        lockIndicator.textContent = "Misses the audited Koide target";
      }
    }
  }

  function animateGenerations() {
    if (currentSection === "act2" || generationsState.started) {
      if (!generationsState.isDragging) {
        generationsState.rotation += 0.005;
      }
      renderGenerationsScene(generationsState.currentN);
    }

    requestAnimationFrame(animateGenerations);
  }

  function renderGenerationsScene(N) {
    var canvas = document.getElementById("generations-canvas");
    if (!canvas || !generationsCtx) {
      return;
    }

    var ctx = generationsCtx;
    var w = canvas.width;
    var h = canvas.height;
    var cx = w / 2;
    var cy = h / 2;
    var radius = Math.min(w, h) * 0.25;

    ctx.fillStyle = "#0f0f1f";
    ctx.fillRect(0, 0, w, h);

    ctx.save();
    ctx.translate(cx, cy);

    for (var i = 0; i < 3; i += 1) {
      var angle = i * 2 * Math.PI / 3 + generationsState.rotation;
      var x = Math.cos(angle) * radius;
      var y = Math.sin(angle) * radius;
      var active = i < Math.min(N, 3);

      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(x, y);
      ctx.strokeStyle = active ? "#00cfff" : "#333";
      ctx.lineWidth = active ? 3 : 1;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(x, y, active ? 12 : 8, 0, Math.PI * 2);
      ctx.fillStyle = active ? "#00cfff" : "#444";
      if (active) {
        ctx.shadowColor = "#00cfff";
        ctx.shadowBlur = 15;
      }
      ctx.fill();
      ctx.shadowBlur = 0;

      ctx.fillStyle = active ? "#fff" : "#666";
      ctx.font = "14px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(active ? ["e", "μ", "τ"][i] : "?", x * 1.2, y * 1.2);
    }

    for (var arcIndex = 0; arcIndex < 3; arcIndex += 1) {
      var startAngle = arcIndex * 2 * Math.PI / 3;
      var endAngle = (arcIndex + 1) * 2 * Math.PI / 3;

      ctx.beginPath();
      ctx.arc(0, 0, radius * 0.5, startAngle, endAngle);
      ctx.strokeStyle = "#44ff88";
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    ctx.fillStyle = "#888";
    ctx.font = "12px monospace";
    ctx.textAlign = "center";
    ctx.fillText("π₁(SO(3)) ≅ ℤ₂", 0, -radius - 30);
    ctx.fillText("(2,1) closure orders: partial theorem, not full physical realization", 0, -radius - 10);
    ctx.restore();

    ctx.fillStyle = "#888";
    ctx.font = "12px sans-serif";
    ctx.textAlign = "left";
    ctx.fillText("Q(N) = 2N / (2N + 3) hits 2/3 only at N = 3.", 20, h - 40);
    ctx.fillText("That algebraic lock becomes physical only when the numerator and denominator theorems close.", 20, h - 20);
  }

  function initAct3() {
    var canvas = document.getElementById("god-equation-canvas");
    var nSlider = document.getElementById("n-slider-ge");
    var dSlider = document.getElementById("d-slider");
    if (!canvas || !nSlider || !dSlider) {
      return;
    }

    godEqCtx = canvas.getContext("2d");
    godEquationState.currentN = parseInt(nSlider.value, 10);
    godEquationState.currentD = parseInt(dSlider.value, 10);

    nSlider.addEventListener("input", function () {
      godEquationState.currentN = parseInt(nSlider.value, 10);
      refreshGodEquation();
    });

    dSlider.addEventListener("input", function () {
      godEquationState.currentD = parseInt(dSlider.value, 10);
      refreshGodEquation();
    });
  }

  function ensureGodEquationAnimation() {
    var canvas = document.getElementById("god-equation-canvas");
    if (!canvas) {
      return;
    }

    resizeCanvas(canvas);
    godEquationState.started = true;
  }

  function refreshGodEquation() {
    var nValue = document.getElementById("n-value-ge");
    var dValue = document.getElementById("d-value");
    var geResult = document.getElementById("ge-result");
    var geObserved = document.getElementById("ge-observed");
    var geError = document.getElementById("ge-error");
    var N = godEquationState.currentN;
    var D = godEquationState.currentD;
    var lP = 1.616e-35;
    var b0 = 16 / 3;
    var exponent = (4 * Math.PI * Math.PI * Math.pow(N, D / 2)) / b0;
    var lambdaC = Math.sqrt(2) * lP * Math.exp(exponent);
    var observed = 1.14e-18;
    var error = Math.abs(lambdaC - observed) / observed * 100;

    godEquationState.currentLambda = lambdaC;
    
    // Reset animation when values change
    godEquationState.animationTime = 0;
    godEquationState.rgCurve = [];

    if (nValue) {
      nValue.textContent = N;
    }
    if (dValue) {
      dValue.textContent = D;
    }
    if (geResult) {
      geResult.textContent = "Predicted: " + lambdaC.toExponential(3) + " m";
    }
    if (geObserved) {
      geObserved.textContent = "Observed: " + observed.toExponential(3) + " m";
    }
    if (geError) {
      if (N === 3 && D === 3) {
        geError.textContent = "Status: CONDITIONAL 0.88 • numerical anchor error " + error.toFixed(1) + "%";
        geError.style.color = "#44ff88";
      } else {
        geError.textContent = "Status: CONDITIONAL • off the physical point";
        geError.style.color = "#ffdd55";
      }
    }

    renderGodEquation(N, D, lambdaC);
  }

  function renderGodEquation(N, D, lambdaC) {
    var canvas = document.getElementById("god-equation-canvas");
    if (!canvas || !godEqCtx) {
      return;
    }

    var ctx = godEqCtx;
    var w = canvas.width;
    var h = canvas.height;
    var minLog = -40;
    var maxLog = 5;
    var scaleY = (h - 100) / (maxLog - minLog);
    var scales = [
      { label: "Planck", value: -35 },
      { label: "GUT", value: -25 },
      { label: "Matter", value: -18 },
      { label: "Atomic", value: -10 },
      { label: "Human", value: 0 }
    ];

    // Clear canvas with fade effect
    ctx.fillStyle = "rgba(15, 15, 31, 0.95)";
    ctx.fillRect(0, 0, w, h);

    // Draw grid
    ctx.strokeStyle = "#222";
    ctx.lineWidth = 1;
    for (let i = minLog; i <= maxLog; i += 5) {
      const y = h - 50 - (i - minLog) * scaleY;
      ctx.beginPath();
      ctx.moveTo(80, y);
      ctx.lineTo(w - 20, y);
      ctx.stroke();
    }

    // Draw axis
    ctx.strokeStyle = "#444";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(80, 50);
    ctx.lineTo(80, h - 50);
    ctx.stroke();

    // Draw scale labels
    scales.forEach(function (scale) {
      var y = h - 50 - (scale.value - minLog) * scaleY;

      ctx.beginPath();
      ctx.moveTo(70, y);
      ctx.lineTo(80, y);
      ctx.strokeStyle = "#666";
      ctx.stroke();

      ctx.fillStyle = "#888";
      ctx.font = "12px sans-serif";
      ctx.textAlign = "right";
      ctx.fillText("10^" + scale.value + " m", 65, y + 4);
      ctx.fillText(scale.label, 65, y - 8);
    });

    // Calculate and draw RG running curve
    if (!godEquationState.isAnimating) {
      godEquationState.isAnimating = true;
      animateRGCurve();
    }

    // Draw the RG curve
    drawRGCurve(ctx, w, h, minLog, scaleY);

    // Calculate positions
    var predictedY = h - 50 - (Math.log10(lambdaC) - minLog) * scaleY;
    var observedY = h - 50 - (Math.log10(1.14e-18) - minLog) * scaleY;
    var activeColor = N === 3 && D === 3 ? "#44ff88" : "#ff5555";

    // Draw predicted point with glow
    const glowSize = 15 + Math.sin(godEquationState.animationTime * 0.003) * 5;
    const gradient = ctx.createRadialGradient(150, predictedY, 0, 150, predictedY, glowSize);
    gradient.addColorStop(0, activeColor);
    gradient.addColorStop(0.5, activeColor + "80");
    gradient.addColorStop(1, "transparent");
    
    ctx.beginPath();
    ctx.arc(150, predictedY, glowSize, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(150, predictedY, 8, 0, Math.PI * 2);
    ctx.fillStyle = activeColor;
    ctx.shadowColor = activeColor;
    ctx.shadowBlur = 15;
    ctx.fill();
    ctx.shadowBlur = 0;

    // Draw observed point with pulsing effect
    const pulseSize = 8 + Math.sin(godEquationState.animationTime * 0.005) * 2;
    ctx.beginPath();
    ctx.arc(250, observedY, pulseSize, 0, Math.PI * 2);
    ctx.fillStyle = "#00cfff";
    ctx.shadowColor = "#00cfff";
    ctx.shadowBlur = 10;
    ctx.fill();
    ctx.shadowBlur = 0;

    // Draw connection line with animation
    const dashOffset = (godEquationState.animationTime / 20) % 10;
    ctx.setLineDash([5, 5]);
    ctx.lineDashOffset = -dashOffset;
    ctx.beginPath();
    ctx.moveTo(150, predictedY);
    ctx.lineTo(250, observedY);
    ctx.strokeStyle = activeColor;
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.setLineDash([]);

    // Labels
    ctx.fillStyle = "#fff";
    ctx.font = "11px sans-serif";
    ctx.textAlign = "left";
    ctx.fillText("Prediction (N=" + N + ", D=" + D + ")", 165, predictedY + 4);
    ctx.fillText("Observed matter scale", 265, observedY + 4);

    // Formula
    ctx.fillStyle = "#888";
    ctx.font = "11px monospace";
    ctx.fillText("λ_c = √2 · l_P · exp(4π² N^(D/2) / b₀)", 20, 30);
    
    // Highlight physical window
    if (N === 3 && D === 3) {
      // Draw habitable window
      ctx.fillStyle = "rgba(68, 255, 136, 0.05)";
      ctx.fillRect(0, observedY - 40, w, 80);
      
      ctx.strokeStyle = "rgba(68, 255, 136, 0.3)";
      ctx.lineWidth = 2;
      ctx.strokeRect(0, observedY - 40, w, 80);
      
      ctx.fillStyle = "#44ff88";
      ctx.font = "bold 14px sans-serif";
      ctx.fillText("✓ Physical Point: Only (3,3) lands in habitable window", 20, observedY + 80);
      
      // Error indicator
      const error = Math.abs(lambdaC - 1.14e-18) / 1.14e-18 * 100;
      ctx.fillStyle = "#ffdd55";
      ctx.font = "12px sans-serif";
      ctx.fillText("Numerical anchor error: " + error.toFixed(1) + "%", 20, observedY + 100);
    } else {
      ctx.fillStyle = "#ffaa00";
      ctx.font = "bold 14px sans-serif";
      ctx.fillText("✗ Outside physical window", 20, observedY + 80);
    }

    // Continue animation
    godEquationState.animationTime++;
    if (godEquationState.isAnimating) {
      requestAnimationFrame(() => renderGodEquation(N, D, lambdaC));
    }
  }

  function drawRGCurve(ctx, w, h, minLog, scaleY) {
    if (godEquationState.rgCurve.length === 0) {
      // Initialize RG curve points
      for (let mu = -35; mu <= 5; mu += 0.5) {
        const energy = Math.pow(10, mu);
        // Simplified RG running: α(μ) = α₀ / (1 - (α₀/2π) * ln(μ/μ₀))
        const alpha0 = 1/137;
        const mu0 = 1.14e-18;
        const alpha = alpha0 / (1 - (alpha0 / (2 * Math.PI)) * Math.log(energy / mu0));
        godEquationState.rgCurve.push({ mu, alpha });
      }
    }

    // Draw the curve
    ctx.strokeStyle = "rgba(0, 207, 255, 0.6)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    godEquationState.rgCurve.forEach((point, i) => {
      const x = 100 + (i / godEquationState.rgCurve.length) * (w - 120);
      const y = h - 50 - (Math.log10(point.alpha * 1e-10) - minLog) * scaleY;
      
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    
    ctx.stroke();

    // Draw moving point on curve
    const progress = (godEquationState.animationTime % 200) / 200;
    const index = Math.floor(progress * (godEquationState.rgCurve.length - 1));
    const point = godEquationState.rgCurve[index];
    const x = 100 + (index / godEquationState.rgCurve.length) * (w - 120);
    const y = h - 50 - (Math.log10(point.alpha * 1e-10) - minLog) * scaleY;
    
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fillStyle = "#00cfff";
    ctx.shadowColor = "#00cfff";
    ctx.shadowBlur = 10;
    ctx.fill();
    ctx.shadowBlur = 0;
  }

  function animateRGCurve() {
    // This function can be expanded to add more complex RG flow animations
    // For now, the animation is handled in renderGodEquation
  }

  function initAct4() {
    populateAct4();
  }

  function populateAct4() {
    populateJourneyComparisonTable();
    populateResults();
    populateBigNumbers();
  }

  function populateJourneyComparisonTable() {
    var api = getTruth();
    if (!api) {
      return;
    }

    var counts = api.getCountsByStatus();
    var audited = api.getAuditedResults();
    var falsifiableCount = audited.filter(function (result) {
      return result.falsifier;
    }).length;

    setText("journey-pf-free", "3 axioms");
    setText("journey-pf-derived", counts.total + " audited claims • " + (counts.DERIVED || 0) + " derived");
    setText("journey-pf-falsifiable", "Yes (" + falsifiableCount + " audited falsifiers)");
  }

  function populateResults() {
    var api = getTruth();
    var container = document.getElementById("results-cards-container");
    if (!api || !container) {
      return;
    }

    container.innerHTML = "";

    api.sortResultsForNarrative(api.getAuditedResults()).forEach(function (result) {
      var card = document.createElement("div");
      var statusClass = api.statusToClass(result.status);
      var badgeClass = statusClass.replace(/^status-/, "");

      card.className = "result-card " + statusClass;
      card.innerHTML = [
        '<div class="result-card-title">' + escapeHtml(result.title) + "</div>",
        '<div class="result-card-status ' + badgeClass + '">' + escapeHtml(result.status) + "</div>",
        '<div class="result-card-formula">' + escapeHtml(result.formula) + "</div>",
        '<div class="result-card-confidence">Confidence: ' + Math.round((result.confidence || 0) * 100) + "%</div>"
      ].join("");

      container.appendChild(card);
    });
  }

  function populateBigNumbers() {
    var api = getTruth();
    if (!api) {
      return;
    }

    var counts = api.getCountsByStatus();
    setText("journey-count-total", counts.total);
    setText("journey-count-derived", counts.DERIVED || 0);
    setText("journey-count-conditional", counts.CONDITIONAL || 0);
  }

  function initEpilogue() {
    var restartButton = document.getElementById("restart-journey");
    var exploreButton = document.getElementById("explore-more");

    if (restartButton) {
      restartButton.addEventListener("click", function () {
        goToSection("opening");
      });
    }

    if (exploreButton) {
      exploreButton.addEventListener("click", function () {
        window.location.href = "index.html";
      });
    }

    populateFalsificationCards();
  }

  function populateFalsificationCards() {
    var api = getTruth();
    var container = document.getElementById("journey-falsification-cards");
    if (!api || !container) {
      return;
    }

    container.innerHTML = "";

    falsificationIds.forEach(function (id) {
      var result = api.getResult(id);
      if (!result) {
        return;
      }

      var meta = falsificationMeta[id] || { icon: "•", title: result.title };
      var card = document.createElement("div");
      card.className = "falsify-card";
      card.innerHTML = [
        '<div class="falsify-icon">' + meta.icon + "</div>",
        '<div class="falsify-title">' + escapeHtml(meta.title) + "</div>",
        '<div class="falsify-detail">' + escapeHtml(result.falsifier || "See audited claim entry.") + "</div>"
      ].join("");
      container.appendChild(card);
    });
  }

  function resizeCanvas(canvas) {
    if (!canvas || !canvas.parentElement) {
      return;
    }

    var rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = Math.max(320, Math.floor(rect.width));
    canvas.height = Math.min(500, Math.max(260, Math.floor(rect.width * 0.6)));
  }

  function setText(id, value) {
    var node = document.getElementById(id);
    if (node) {
      node.textContent = value;
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  window.addEventListener("resize", function () {
    if (currentSection === "act1") {
      ensureBohrAnimation();
    }
    if (currentSection === "act2") {
      ensureGenerationsAnimation();
      renderGenerationsScene(generationsState.currentN);
    }
    if (currentSection === "act3") {
      ensureGodEquationAnimation();
      renderGodEquation(
        godEquationState.currentN,
        godEquationState.currentD,
        godEquationState.currentLambda
      );
    }
  });
})();
