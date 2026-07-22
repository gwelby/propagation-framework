/**
 * Journey Mode — The 8-Minute Narrative Experience
 * Propagation Framework Explorer
 */
(function () {
  "use strict";

  var currentSection = "opening";
  var sections = ["opening", "act1", "act2", "act3", "act4", "epilogue"];
  var truth = window.PFExplorerTruth || window.PFTruth;

  var godEqCtx = null;

  var godEquationState = {
    started: false,
    currentN: 3,
    currentD: 3,
    currentLambda: 1.145e-18,
    animationTime: 0,
    rgCurve: [],
    isAnimating: false,
    scene: null,
    camera: null,
    renderer: null,
    composer: null,
    surfaceMesh: null,
    currentPoint: null,
    currentLine: null,
    gridHelper: null,
    animFrameId: null
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
      ensureAct1Animation();
    } else {
      if (act1State.animFrameId) {
        cancelAnimationFrame(act1State.animFrameId);
        act1State.animFrameId = null;
      }
    }

    if (sectionId === "act3") {
      ensureGodEquationAnimation();
      refreshGodEquation();
    } else {
      if (godEquationState.animFrameId) {
        cancelAnimationFrame(godEquationState.animFrameId);
        godEquationState.animFrameId = null;
      }
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

  var act1State = {
    started: false,
    animFrameId: null,
    selectedN: 3
  };

  function initAct1() {
    if (!window.PFRealityVisuals) return;

    var gravityCanvas = document.getElementById('rvGravityJourney');
    if (gravityCanvas) {
      window.PFRealityVisuals.drawGravityRefraction(gravityCanvas);
    }

    var genCanvas = document.getElementById('rvGenJourney');
    if (genCanvas) {
      window.PFRealityVisuals.drawTopologyDiagram(genCanvas, act1State.selectedN, act1State.selectedN);
      
      var selector = document.getElementById('genNSelectorJourney');
      if (selector) {
        selector.querySelectorAll('.gen-n-btn').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var n = Number(btn.getAttribute('data-n'));
            act1State.selectedN = n;
            selector.querySelectorAll('.gen-n-btn').forEach(function (b) {
              b.classList.toggle('active', b.getAttribute('data-n') === String(n));
            });
            window.PFRealityVisuals.drawTopologyDiagram(genCanvas, n, n);
          });
        });
      }
    }
  }

  function ensureAct1Animation() {
    if (!window.PFRealityVisuals) return;

    var gravityCanvas = document.getElementById('rvGravityJourney');
    if (gravityCanvas) {
      window.PFRealityVisuals.drawGravityRefraction(gravityCanvas);
    }

    var genCanvas = document.getElementById('rvGenJourney');
    if (genCanvas) {
      window.PFRealityVisuals.drawTopologyDiagram(genCanvas, act1State.selectedN, act1State.selectedN);
    }
    
    function animate() {
      var matterCanvas = document.getElementById('rvMatterJourney');
      if (matterCanvas && currentSection === "act1") {
        window.PFRealityVisuals.drawParticleVsWave(matterCanvas);
        act1State.animFrameId = requestAnimationFrame(animate);
      }
    }
    
    if (!act1State.animFrameId && currentSection === "act1") {
      animate();
    }
  }

  function initAct3() {
    var container = document.getElementById("god-equation-container");
    var nSlider = document.getElementById("n-slider-ge");
    var dSlider = document.getElementById("d-slider");
    if (!container || !nSlider || !dSlider) {
      return;
    }

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

    refreshGodEquation();
  }

  function ensureGodEquationAnimation() {
    if (godEquationState.started) return;
    godEquationState.started = true;
  }

  function godEquationComputeLambda(N, D) {
    var lP = 1.616e-35;
    var b0 = 16 / 3;
    var exponent = (4 * Math.PI * Math.PI * Math.pow(N, D / 2)) / b0;
    return Math.sqrt(2) * lP * Math.exp(exponent);
  }

  function godEquationLogRatio(N, D) {
    var lambdaC = godEquationComputeLambda(N, D);
    var observed = 1.14e-18;
    return Math.log10(lambdaC / observed);
  }

  function initGodEquationThreeJS() {
    if (typeof THREE === 'undefined') {
      return;
    }
    var container = document.getElementById("god-equation-container");
    if (!container || godEquationState.scene) return;

    var w = container.clientWidth || 640;
    var h = container.clientHeight || 480;

    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a1a);
    scene.fog = new THREE.FogExp2(0x0a0a1a, 0.015);

    var camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 1000);
    camera.position.set(8, 6, 12);
    camera.lookAt(3.5, 3, 0);

    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // Provide a fallback if EffectComposer isn't properly loaded via CDN/vendor
    var composer;
    if (THREE.EffectComposer && THREE.RenderPass && THREE.UnrealBloomPass) {
        composer = new THREE.EffectComposer(renderer);
        var renderPass = new THREE.RenderPass(scene, camera);
        composer.addPass(renderPass);

        var bloomPass = new THREE.UnrealBloomPass(
          new THREE.Vector2(w, h), 0.8, 0.4, 0.85
        );
        composer.addPass(bloomPass);
        godEquationState.composer = composer;
    }

    // Since OrbitControls might be a property of THREE or global
    var OrbitControls = THREE.OrbitControls || window.OrbitControls;
    var controls;
    if (OrbitControls) {
        controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 5;
        controls.maxDistance = 30;
        controls.target.set(3.5, 3, 0);
        controls.update();
        godEquationState.controls = controls;
    }

    var ambientLight = new THREE.AmbientLight(0x334466, 0.6);
    scene.add(ambientLight);

    var dirLight = new THREE.DirectionalLight(0x88ccff, 1.2);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);

    var fillLight = new THREE.DirectionalLight(0x00cfff, 0.4);
    fillLight.position.set(-5, 3, -5);
    scene.add(fillLight);

    var rimLight = new THREE.DirectionalLight(0xffdd55, 0.3);
    rimLight.position.set(0, -5, 10);
    scene.add(rimLight);

    var gridHelper = new THREE.GridHelper(14, 14, 0x223344, 0x112233);
    gridHelper.position.y = -2;
    scene.add(gridHelper);

    var surfaceMesh = buildGodEquationSurface(scene);

    var currentPoint = new THREE.Mesh(
      new THREE.SphereGeometry(0.18, 24, 24),
      new THREE.MeshStandardMaterial({
        color: 0x44ff88,
        emissive: 0x44ff88,
        emissiveIntensity: 2,
        metalness: 0.3,
        roughness: 0.2
      })
    );
    scene.add(currentPoint);

    var currentLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0, 0)
      ]),
      new THREE.LineBasicMaterial({ color: 0x44ff88, transparent: true, opacity: 0.6 })
    );
    scene.add(currentLine);

    var obsGeometry = new THREE.SphereGeometry(0.12, 16, 16);
    var obsMaterial = new THREE.MeshStandardMaterial({
      color: 0x00cfff,
      emissive: 0x00cfff,
      emissiveIntensity: 1.5,
      metalness: 0.5,
      roughness: 0.1
    });
    var observedPoint = new THREE.Mesh(obsGeometry, obsMaterial);
    observedPoint.position.set(3, 3, godEquationLogRatio(3, 3));
    scene.add(observedPoint);

    godEquationState.scene = scene;
    godEquationState.camera = camera;
    godEquationState.renderer = renderer;
    godEquationState.surfaceMesh = surfaceMesh;
    godEquationState.currentPoint = currentPoint;
    godEquationState.currentLine = currentLine;
    godEquationState.observedPoint = observedPoint;

    container.style.cursor = "grab";

    animateGodEquation();
  }

  function buildGodEquationSurface(scene) {
    var N_min = 1, N_max = 6, N_steps = 30;
    var D_min = 1, D_max = 5, D_steps = 20;

    var positions = [];
    var colors = [];
    var indices = [];
    var colorLow = new THREE.Color(0x004488);
    var colorMid = new THREE.Color(0x00cfff);
    var colorHigh = new THREE.Color(0xff6644);
    var colorPhysical = new THREE.Color(0x44ff88);

    var grid = [];
    for (var di = 0; di <= D_steps; di++) {
      var row = [];
      for (var ni = 0; ni <= N_steps; ni++) {
        var N = N_min + (ni / N_steps) * (N_max - N_min);
        var D = D_min + (di / D_steps) * (D_max - D_min);
        var logRatio = godEquationLogRatio(N, D);
        var t = Math.max(0, Math.min(1, (logRatio + 4) / 8));
        var c = new THREE.Color();
        if (Math.abs(N - 3) < 0.3 && Math.abs(D - 3) < 0.3) {
          c.lerpColors(colorMid, colorPhysical, 0.6);
        } else {
          if (t < 0.5) {
            c.lerpColors(colorLow, colorMid, t * 2);
          } else {
            c.lerpColors(colorMid, colorHigh, (t - 0.5) * 2);
          }
        }
        row.push({ N: ni, D: di, x: N, y: D, z: logRatio, color: c });
      }
      grid.push(row);
    }

    for (var di = 0; di < D_steps; di++) {
      for (var ni = 0; ni < N_steps; ni++) {
        var i = positions.length / 3;
        var p00 = grid[di][ni];
        var p10 = grid[di + 1][ni];
        var p01 = grid[di][ni + 1];
        var p11 = grid[di + 1][ni + 1];

        positions.push(p00.x, p00.y, p00.z);
        positions.push(p10.x, p10.y, p10.z);
        positions.push(p01.x, p01.y, p01.z);
        positions.push(p11.x, p11.y, p11.z);

        colors.push(p00.color.r, p00.color.g, p00.color.b);
        colors.push(p10.color.r, p10.color.g, p10.color.b);
        colors.push(p01.color.r, p01.color.g, p01.color.b);
        colors.push(p11.color.r, p11.color.g, p11.color.b);

        indices.push(i, i + 1, i + 2);
        indices.push(i + 1, i + 3, i + 2);
      }
    }

    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();

    var material = new THREE.MeshStandardMaterial({
      vertexColors: true,
      side: THREE.DoubleSide,
      metalness: 0.2,
      roughness: 0.5,
      transparent: true,
      opacity: 0.85
    });

    var mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    var wireMat = new THREE.MeshBasicMaterial({
      color: 0x00cfff,
      wireframe: true,
      transparent: true,
      opacity: 0.06
    });
    var wireMesh = new THREE.Mesh(geometry.clone(), wireMat);
    wireMesh.material.opacity = 0.04;
    scene.add(wireMesh);

    var axisMat = new THREE.LineBasicMaterial({ color: 0x556677, transparent: true, opacity: 0.5 });
    var axisGeoms = [
      [[N_min, 0, 0], [N_max, 0, 0]],
      [[0, D_min, 0], [0, D_max, 0]],
      [[0, 0, -4], [0, 0, 4]]
    ];
    axisGeoms.forEach(function (pts) {
      var g = new THREE.BufferGeometry().setFromPoints(pts.map(function (p) { return new THREE.Vector3(p[0], p[1], p[2]); }));
      scene.add(new THREE.Line(g, axisMat));
    });

    var labelCanvas = document.createElement("canvas");
    labelCanvas.width = 128;
    labelCanvas.height = 32;
    var labelCtx = labelCanvas.getContext("2d");
    labelCtx.fillStyle = "#aabbcc";
    labelCtx.font = "14px monospace";
    labelCtx.fillText("N (generations)", 0, 20);
    var labelTex = new THREE.CanvasTexture(labelCanvas);
    var spriteMat = new THREE.SpriteMaterial({ map: labelTex, transparent: true });
    var sprite = new THREE.Sprite(spriteMat);
    sprite.position.set(3.5, -0.5, 0);
    sprite.scale.set(3, 0.6, 1);
    scene.add(sprite);

    return mesh;
  }

  function updateGodEquationPoint(N, D, lambdaC) {
    if (!godEquationState.currentPoint) return;
    var logRatio = godEquationLogRatio(N, D);
    var isPhysical = N === 3 && D === 3;
    var pointColor = isPhysical ? 0x44ff88 : 0xff6644;
    godEquationState.currentPoint.position.set(N, D, logRatio);
    godEquationState.currentPoint.material.color.setHex(pointColor);
    godEquationState.currentPoint.material.emissive.setHex(pointColor);
    godEquationState.currentPoint.material.emissiveIntensity = isPhysical ? 2.5 : 1.5;

    var linePoints = [
      new THREE.Vector3(N, D, -3),
      new THREE.Vector3(N, D, logRatio)
    ];
    godEquationState.currentLine.geometry.setFromPoints(linePoints);
    godEquationState.currentLine.material.color.setHex(pointColor);
  }

  function animateGodEquation() {
    if (!godEquationState.scene) return;
    godEquationState.animFrameId = requestAnimationFrame(animateGodEquation);
    if (godEquationState.controls) {
      godEquationState.controls.update();
    }
    if (godEquationState.composer) {
      godEquationState.composer.render();
    } else {
      godEquationState.renderer.render(godEquationState.scene, godEquationState.camera);
    }
  }

  function refreshGodEquation() {
    var nValue = document.getElementById("n-value-ge");
    var dValue = document.getElementById("d-value");
    var geResult = document.getElementById("ge-result");
    var geObserved = document.getElementById("ge-observed");
    var geError = document.getElementById("ge-error");
    var N = godEquationState.currentN;
    var D = godEquationState.currentD;
    var lambdaC = godEquationComputeLambda(N, D);
    var observed = 1.14e-18;
    var error = Math.abs(lambdaC - observed) / observed * 100;

    godEquationState.currentLambda = lambdaC;
    godEquationState.animationTime = 0;

    if (nValue) nValue.textContent = N;
    if (dValue) dValue.textContent = D;
    if (geResult) geResult.textContent = "Predicted: " + lambdaC.toExponential(3) + " m";
    if (geObserved) geObserved.textContent = "Observed: " + observed.toExponential(3) + " m";
    if (geError) {
      // V3: Pull status from generated authority data, not hard-coded
      var truth = window.PFExplorerTruth || window.PFTruth;
      var godOp = truth && truth.getClaim ? truth.getClaim("god-equation-operator") : null;
      var opStatus = godOp ? (godOp.badge || (godOp.status && godOp.status.label ? godOp.status.label : godOp.status) || "UNAVAILABLE") : "UNAVAILABLE";
      geError.setAttribute('data-claim-id', 'god-equation-operator');
      if (N === 3 && D === 3) {
        geError.textContent = "Status: " + opStatus + " • numerical anchor error " + error.toFixed(1) + "%";
        geError.style.color = "#44ff88";
      } else {
        geError.textContent = "Status: " + opStatus + " • off the physical point";
        geError.style.color = "#ffdd55";
      }
    }

    ensureGodEquationAnimation();
    if (!godEquationState.scene) {
      initGodEquationThreeJS();
    } else {
      updateGodEquationPoint(N, D, lambdaC);
    }
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
    // V4: Pull status from authority, not hardcoded
    var threeGen = api.getClaim("three-generations");
    var bohr = api.getClaim("bohr-spectrum");
    setText("journey-pf-generations", threeGen ? threeGen.badge : "UNAVAILABLE", threeGen ? threeGen.id : "");
    setText("journey-pf-atomic", bohr ? bohr.badge : "UNAVAILABLE", bohr ? bohr.id : "");
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
      // V5.4: Standard-math claims display the badge status (e.g. STANDARD MATH)
      // instead of the raw authority status (e.g. CONDITIONAL / DERIVED).
      var displayStatus = result.status;
      if (result.isStandardMath && result.badge) {
        displayStatus = result.badge.replace(/\s+\d+(\.\d+)?\s*%?.*$/, "");
      }
      var statusClass = api.statusToClass(displayStatus);
      var badgeClass = statusClass.replace(/^status-/, "");

      card.className = "result-card " + statusClass;
      card.setAttribute('data-claim-id', result.id);
      card.innerHTML = [
        '<div class="result-card-title">' + escapeHtml(result.title) + "</div>",
        '<div class="result-card-status ' + badgeClass + '" data-claim-id="' + result.id + '">' + escapeHtml(displayStatus) + "</div>",
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

  function setText(id, value, claimId) {
    var node = document.getElementById(id);
    if (node) {
      node.textContent = value;
      if (claimId) {
        node.setAttribute('data-claim-id', claimId);
      }
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

  function resizeGodEquation() {
    var container = document.getElementById("god-equation-container");
    if (!container || !godEquationState.renderer) return;
    var w = container.clientWidth || 640;
    var h = container.clientHeight || 480;
    godEquationState.camera.aspect = w / h;
    godEquationState.camera.updateProjectionMatrix();
    godEquationState.renderer.setSize(w, h);
    if (godEquationState.composer) {
        godEquationState.composer.setSize(w, h);
    }
  }

  window.addEventListener("resize", function () {
    if (currentSection === "act3") {
      ensureGodEquationAnimation();
      resizeGodEquation();
    }
  });
})();
