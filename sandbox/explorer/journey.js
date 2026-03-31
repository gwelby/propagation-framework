/**
 * Journey Mode — The 5-Minute Narrative Experience
 * Propagation Framework Explorer
 * 
 * A guided journey through the framework's strongest results
 */

(function() {
  'use strict';

  // State
  let currentSection = 'opening';
  const sections = ['opening', 'act1', 'act2', 'act3', 'act4', 'epilogue'];

  // Canvas contexts
  let bohrCtx, generationsCtx, godEqCtx;

  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initOpening();
    initAct1();
    initAct2();
    initAct3();
    initAct4();
    initEpilogue();
    updateProgress();
  });

  // Navigation
  function initNavigation() {
    // Next buttons
    document.querySelectorAll('.next-act').forEach(btn => {
      btn.addEventListener('click', () => {
        const currentIndex = sections.indexOf(currentSection);
        if (currentIndex < sections.length - 1) {
          goToSection(sections[currentIndex + 1]);
        }
      });
    });

    // Progress steps
    document.querySelectorAll('.progress-step').forEach(step => {
      step.addEventListener('click', () => {
        const section = step.dataset.step;
        goToSection(section);
      });
    });
  }

  function goToSection(sectionId) {
    // Hide current
    document.getElementById(`journey-${currentSection}`).classList.remove('active');
    
    // Show new
    currentSection = sectionId;
    document.getElementById(`journey-${sectionId}`).classList.add('active');
    
    // Update progress
    updateProgress();
    
    // Initialize section-specific logic
    if (sectionId === 'act1') initBohrAnimation();
    if (sectionId === 'act2') initGenerationsAnimation();
    if (sectionId === 'act3') initGodEquationAnimation();
    if (sectionId === 'act4') populateResults();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function updateProgress() {
    const currentIndex = sections.indexOf(currentSection);
    document.querySelectorAll('.progress-step').forEach((step, index) => {
      step.classList.remove('active', 'completed');
      if (index === currentIndex) {
        step.classList.add('active');
      } else if (index < currentIndex) {
        step.classList.add('completed');
      }
    });
  }

  // Opening Sequence
  function initOpening() {
    const beginBtn = document.getElementById('begin-journey');
    beginBtn.addEventListener('click', () => {
      goToSection('act1');
    });

    // Animate axiom cards
    setTimeout(() => {
      document.querySelectorAll('.axiom-card').forEach((card, i) => {
        setTimeout(() => {
          card.classList.add('revealed');
        }, i * 400);
      });
    }, 500);
  }

  // Act I: Bohr Quantization
  function initAct1() {
    const canvas = document.getElementById('bohr-canvas');
    bohrCtx = canvas.getContext('2d');
    resizeCanvas(canvas);
  }

  function initBohrAnimation() {
    const canvas = document.getElementById('bohr-canvas');
    if (!canvas) return;
    
    resizeCanvas(canvas);
    
    let electron = { x: 0, y: 0, phase: 0, orbit: 1 };
    let orbits = [];
    let animationId;

    // Create allowed orbits
    for (let k = 1; k <= 4; k++) {
      orbits.push({
        k: k,
        radius: 2 * k * k,
        energy: -1 / (4 * k * k),
        phase: 0
      });
    }

    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left - canvas.width / 2) * 2;
      const y = (e.clientY - rect.top - canvas.height / 2) * 2;
      
      const dist = Math.sqrt(x * x + y * y);
      const closestOrbit = orbits.reduce((prev, curr) => {
        return Math.abs(dist - curr.radius) < Math.abs(dist - prev.radius) ? curr : prev;
      });
      
      electron = {
        x: x / dist * closestOrbit.radius,
        y: y / dist * closestOrbit.radius,
        phase: 0,
        orbit: closestOrbit.k,
        targetOrbit: closestOrbit
      };
    });

    function animate() {
      const ctx = bohrCtx;
      const w = canvas.width;
      const h = canvas.height;
      
      // Clear
      ctx.fillStyle = '#0f0f1f';
      ctx.fillRect(0, 0, w, h);
      
      // Draw nucleus
      ctx.beginPath();
      ctx.arc(w / 2, h / 2, 8, 0, Math.PI * 2);
      ctx.fillStyle = '#ff5555';
      ctx.fill();
      ctx.shadowColor = '#ff5555';
      ctx.shadowBlur = 20;
      ctx.fill();
      ctx.shadowBlur = 0;
      
      // Draw orbits
      orbits.forEach(orbit => {
        const screenRadius = Math.min(w, h) * 0.15 * orbit.k;
        
        // Check if electron is on this orbit
        const isActive = electron.targetOrbit && electron.targetOrbit.k === orbit.k;
        
        ctx.beginPath();
        ctx.arc(w / 2, h / 2, screenRadius, 0, Math.PI * 2);
        ctx.strokeStyle = isActive ? '#44ff88' : '#333';
        ctx.lineWidth = isActive ? 3 : 1;
        ctx.stroke();
        
        // Draw phase indicator
        if (isActive) {
          orbit.phase += 0.05;
          const phaseX = w / 2 + Math.cos(orbit.phase) * screenRadius;
          const phaseY = h / 2 + Math.sin(orbit.phase) * screenRadius;
          
          ctx.beginPath();
          ctx.arc(phaseX, phaseY, 6, 0, Math.PI * 2);
          ctx.fillStyle = '#00cfff';
          ctx.fill();
          
          // Phase trail
          ctx.beginPath();
          ctx.arc(w / 2, h / 2, screenRadius, orbit.phase - 0.5, orbit.phase);
          ctx.strokeStyle = 'rgba(0, 207, 255, 0.3)';
          ctx.lineWidth = 8;
          ctx.stroke();
        }
      });
      
      // Draw electron
      if (electron.targetOrbit) {
        const orbit = electron.targetOrbit;
        const screenRadius = Math.min(w, h) * 0.15 * orbit.k;
        electron.phase += 0.08;
        electron.x = Math.cos(electron.phase) * screenRadius;
        electron.y = Math.sin(electron.phase) * screenRadius;
        
        ctx.beginPath();
        ctx.arc(w / 2 + electron.x, h / 2 + electron.y, 8, 0, Math.PI * 2);
        ctx.fillStyle = '#00cfff';
        ctx.fill();
        ctx.shadowColor = '#00cfff';
        ctx.shadowBlur = 15;
        ctx.fill();
        ctx.shadowBlur = 0;
      }
      
      // Draw allowed energies
      ctx.fillStyle = '#888';
      ctx.font = '12px monospace';
      ctx.textAlign = 'right';
      orbits.forEach((orbit, i) => {
        const y = h - 30 - i * 25;
        ctx.fillText(`k=${orbit.k}: E = ${orbit.energy.toFixed(4)}`, w - 20, y);
        
        // Energy level line
        ctx.beginPath();
        ctx.moveTo(w - 150, y - 8);
        ctx.lineTo(w - 20, y - 8);
        ctx.strokeStyle = orbit.k === electron.targetOrbit?.k ? '#44ff88' : '#444';
        ctx.lineWidth = 2;
        ctx.stroke();
      });
      
      animationId = requestAnimationFrame(animate);
    }

    animate();

    // Store animation ID for cleanup
    canvas._animationId = animationId;
  }

  // Act II: Three Generations
  function initAct2() {
    const canvas = document.getElementById('generations-canvas');
    generationsCtx = canvas.getContext('2d');
    resizeCanvas(canvas);
    
    // N slider
    const nSlider = document.getElementById('n-slider');
    const nValue = document.getElementById('n-value');
    const qResult = document.getElementById('q-result');
    const lockIndicator = document.getElementById('lock-indicator');
    
    function updateGenerations() {
      const N = parseInt(nSlider.value);
      nValue.textContent = N;
      
      const Q = (2 * N) / (2 * N + 3);
      const isLock = N === 3;
      
      qResult.textContent = `Q(${N}) = ${2*N}/${2*N+3} = ${Q.toFixed(6)} ${isLock ? '= 2/3' : ''}`;
      lockIndicator.style.display = isLock ? 'block' : 'none';
      lockIndicator.textContent = isLock ? '✓ Exact match to nature' : '';
      
      drawGenerations(N);
    }
    
    nSlider.addEventListener('input', updateGenerations);
    updateGenerations();
  }

  function initGenerationsAnimation() {
    const canvas = document.getElementById('generations-canvas');
    if (!canvas) return;
    resizeCanvas(canvas);
    
    let rotation = 0;
    let isDragging = false;
    let lastX = 0;
    
    canvas.addEventListener('mousedown', (e) => {
      isDragging = true;
      lastX = e.clientX;
    });
    
    canvas.addEventListener('mousemove', (e) => {
      if (isDragging) {
        rotation += (e.clientX - lastX) * 0.02;
        lastX = e.clientX;
      }
    });
    
    canvas.addEventListener('mouseup', () => isDragging = false);
    canvas.addEventListener('mouseleave', () => isDragging = false);
    
    function drawGenerations(N) {
      const ctx = generationsCtx;
      const w = canvas.width;
      const h = canvas.height;
      
      ctx.fillStyle = '#0f0f1f';
      ctx.fillRect(0, 0, w, h);
      
      const cx = w / 2;
      const cy = h / 2;
      const radius = Math.min(w, h) * 0.25;
      
      // Draw SO(3) visualization
      // Belt trick / Dirac string
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(rotation);
      
      // Draw the three generation points at 120°
      for (let i = 0; i < 3; i++) {
        const angle = (i * 2 * Math.PI / 3) + rotation;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;
        
        // Draw connection to center
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(x, y);
        ctx.strokeStyle = i < N ? '#00cfff' : '#333';
        ctx.lineWidth = i < N ? 3 : 1;
        ctx.stroke();
        
        // Draw generation point
        ctx.beginPath();
        ctx.arc(x, y, i < N ? 12 : 8, 0, Math.PI * 2);
        ctx.fillStyle = i < N ? '#00cfff' : '#333';
        ctx.fill();
        
        if (i < N) {
          ctx.shadowColor = '#00cfff';
          ctx.shadowBlur = 15;
          ctx.fill();
          ctx.shadowBlur = 0;
        }
        
        // Label
        ctx.fillStyle = i < N ? '#fff' : '#666';
        ctx.font = '14px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(i < N ? ['e', 'μ', 'τ'][i] : '?', x * 1.2, y * 1.2);
      }
      
      // Draw 120° arcs
      for (let i = 0; i < 3; i++) {
        const startAngle = (i * 2 * Math.PI / 3);
        const endAngle = ((i + 1) * 2 * Math.PI / 3);
        
        ctx.beginPath();
        ctx.arc(0, 0, radius * 0.5, startAngle, endAngle);
        ctx.strokeStyle = '#44ff88';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.stroke();
        ctx.setLineDash([]);
      }
      
      // Draw π₁(SO(3)) visualization
      ctx.fillStyle = '#888';
      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('π₁(SO(3)) ≅ ℤ₂', 0, -radius - 30);
      ctx.fillText('Two loop classes: contractible & non-contractible', 0, -radius - 10);
      
      ctx.restore();
      
      // Draw Q(N) calculation
      ctx.fillStyle = '#888';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('Topological constraint: 3D rotations have exactly 2 kinds of closed paths', 20, h - 40);
      ctx.fillText('This forces the (2,1) weight partition → Q(N) = 2N/(2N+3)', 20, h - 20);
    }
    
    // Initial draw
    const N = parseInt(document.getElementById('n-slider').value);
    drawGenerations(N);
    
    // Animation loop
    function animate() {
      if (!isDragging) {
        rotation += 0.005;
      }
      const nSlider = document.getElementById('n-slider');
      if (nSlider) {
        const N = parseInt(nSlider.value);
        drawGenerations(N);
      }
      requestAnimationFrame(animate);
    }
    animate();
  }

  // Act III: God Equation
  function initAct3() {
    const canvas = document.getElementById('god-equation-canvas');
    godEqCtx = canvas.getContext('2d');
    resizeCanvas(canvas);
    
    // Sliders
    const nSlider = document.getElementById('n-slider-ge');
    const nValue = document.getElementById('n-value-ge');
    const dSlider = document.getElementById('d-slider');
    const dValue = document.getElementById('d-value');
    const geResult = document.getElementById('ge-result');
    const geObserved = document.getElementById('ge-observed');
    const geError = document.getElementById('ge-error');
    
    function updateGodEquation() {
      const N = parseInt(nSlider.value);
      const D = parseInt(dSlider.value);
      
      nValue.textContent = N;
      dValue.textContent = D;
      
      // God Equation: λ_c = √2 · l_P · exp(4π² N^(D/2) / b₀)
      const l_P = 1.616e-35;
      const b0 = 16/3;
      const exponent = (4 * Math.PI * Math.PI * Math.pow(N, D/2)) / b0;
      const lambda_c = Math.sqrt(2) * l_P * Math.exp(exponent);
      
      const observed = 1.14e-18;
      const error = Math.abs(lambda_c - observed) / observed * 100;
      
      geResult.textContent = `Predicted: ${lambda_c.toExponential(3)} m`;
      geObserved.textContent = `Observed: ${observed.toExponential(3)} m`;
      
      if (N === 3 && D === 3) {
        geError.textContent = `Error: ${error.toFixed(1)}% • Zero fitted parameters`;
        geError.style.color = '#44ff88';
      } else {
        geError.textContent = `Error: ${error.toFixed(1)}% • Not the physical point`;
        geError.style.color = error < 10 ? '#ffdd55' : '#ff5555';
      }
      
      drawGodEquation(N, D, lambda_c);
    }
    
    nSlider.addEventListener('input', updateGodEquation);
    dSlider.addEventListener('input', updateGodEquation);
    updateGodEquation();
  }

  function initGodEquationAnimation() {
    const canvas = document.getElementById('god-equation-canvas');
    if (!canvas) return;
    resizeCanvas(canvas);
    
    function drawGodEquation(N, D, lambda_c) {
      const ctx = godEqCtx;
      const w = canvas.width;
      const h = canvas.height;
      
      ctx.fillStyle = '#0f0f1f';
      ctx.fillRect(0, 0, w, h);
      
      // Draw logarithmic scale
      const scales = [
        { label: 'Planck', value: -35, y: h - 60 },
        { label: 'Matter', value: -18, y: h - 120 },
        { label: 'Atomic', value: -10, y: h - 180 },
        { label: 'Human', value: 0, y: h - 240 }
      ];
      
      const minY = -40;
      const maxY = 5;
      const scaleY = (h - 100) / (maxY - minY);
      
      // Draw scale lines
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(80, 50);
      ctx.lineTo(80, h - 50);
      ctx.stroke();
      
      // Draw markers
      scales.forEach(scale => {
        const y = h - 50 - (scale.value - minY) * scaleY;
        
        ctx.beginPath();
        ctx.moveTo(70, y);
        ctx.lineTo(80, y);
        ctx.strokeStyle = '#666';
        ctx.stroke();
        
        ctx.fillStyle = '#888';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText(`10^${scale.value} m`, 65, y + 4);
        
        ctx.fillStyle = '#666';
        ctx.fillText(scale.label, 65, y - 8);
      });
      
      // Draw predicted point
      const logLambda = Math.log10(lambda_c);
      const predY = h - 50 - (logLambda - minY) * scaleY;
      
      ctx.beginPath();
      ctx.arc(150, predY, 8, 0, Math.PI * 2);
      ctx.fillStyle = N === 3 && D === 3 ? '#44ff88' : '#ff5555';
      ctx.fill();
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = 15;
      ctx.fill();
      ctx.shadowBlur = 0;
      
      ctx.fillStyle = '#fff';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`Prediction (N=${N}, D=${D})`, 165, predY + 4);
      
      // Draw observed point
      const logObserved = Math.log10(1.14e-18);
      const obsY = h - 50 - (logObserved - minY) * scaleY;
      
      ctx.beginPath();
      ctx.arc(250, obsY, 8, 0, Math.PI * 2);
      ctx.fillStyle = '#00cfff';
      ctx.fill();
      
      ctx.fillStyle = '#fff';
      ctx.fillText('Observed (matter scale)', 265, obsY + 4);
      
      // Draw connection line
      ctx.beginPath();
      ctx.moveTo(150, predY);
      ctx.lineTo(250, obsY);
      ctx.strokeStyle = N === 3 && D === 3 ? '#44ff88' : '#ff5555';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.stroke();
      ctx.setLineDash([]);
      
      // Draw equation
      ctx.fillStyle = '#888';
      ctx.font = '11px monospace';
      ctx.textAlign = 'left';
      ctx.fillText('λ_c = √2 · l_P · exp(4π² N^(D/2) / b₀)', 20, 30);
      ctx.fillText(`b₀ = 16/3 (QCD beta function)`, 20, 50);
      
      // Highlight the physical point
      if (N === 3 && D === 3) {
        ctx.fillStyle = 'rgba(68, 255, 136, 0.1)';
        ctx.fillRect(0, obsY - 30, w, 60);
        
        ctx.fillStyle = '#44ff88';
        ctx.font = 'bold 14px sans-serif';
        ctx.fillText('✓ Only (N=3, D=3) lands in the habitable window', 20, obsY + 80);
      }
    }
    
    // Initial draw
    const nSlider = document.getElementById('n-slider-ge');
    const dSlider = document.getElementById('d-slider');
    if (nSlider && dSlider) {
      const N = parseInt(nSlider.value);
      const D = parseInt(dSlider.value);
      const l_P = 1.616e-35;
      const b0 = 16/3;
      const lambda_c = Math.sqrt(2) * l_P * Math.exp((4 * Math.PI * Math.PI * Math.pow(N, D/2)) / b0);
      drawGodEquation(N, D, lambda_c);
    }
  }

  // Act IV: Scoreboard
  function initAct4() {
    // Populated by populateResults()
  }

  function populateResults() {
    const container = document.getElementById('results-cards-container');
    if (!container) return;
    
    const data = window.PFExplorerData;
    if (!data) return;
    
    container.innerHTML = '';
    
    data.results.forEach(result => {
      if (result.unsynced) return; // Skip unsynced
      
      const card = document.createElement('div');
      card.className = `result-card status-${result.status.toLowerCase().replace(' ', '-')}`;
      
      const statusClass = result.status.toLowerCase().replace(' ', '-');
      
      card.innerHTML = `
        <div class="result-card-title">${result.title}</div>
        <div class="result-card-status ${statusClass}">${result.status}</div>
        <div class="result-card-formula">${result.formula}</div>
        <div class="result-card-confidence">Confidence: ${(result.confidence * 100).toFixed(0)}%</div>
      `;
      
      container.appendChild(card);
    });
  }

  // Epilogue
  function initEpilogue() {
    const restartBtn = document.getElementById('restart-journey');
    const exploreBtn = document.getElementById('explore-more');
    
    restartBtn.addEventListener('click', () => {
      goToSection('opening');
    });
    
    exploreBtn.addEventListener('click', () => {
      window.location.href = 'index.html';
    });
  }

  // Utilities
  function resizeCanvas(canvas) {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = Math.min(500, rect.width * 0.6);
  }

  window.addEventListener('resize', () => {
    if (currentSection === 'act1') {
      const canvas = document.getElementById('bohr-canvas');
      if (canvas) resizeCanvas(canvas);
    }
    if (currentSection === 'act2') {
      const canvas = document.getElementById('generations-canvas');
      if (canvas) resizeCanvas(canvas);
    }
    if (currentSection === 'act3') {
      const canvas = document.getElementById('god-equation-canvas');
      if (canvas) resizeCanvas(canvas);
    }
  });

})();
