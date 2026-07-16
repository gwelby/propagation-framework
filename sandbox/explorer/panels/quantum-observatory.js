/**
 * panels/quantum-observatory.js
 * Quantum Substrate & Noise Spectroscopy Observatory Panel.
 * Visualizes Shor period-finding boundary, QFT phase-destruction, and dephasing limits.
 */
(function () {
  'use strict';

  // CSS Embedded Stylesheet for the Quantum Observatory
  const CSS_STYLES = `
    .q-obs-container {
      display: grid;
      grid-template-columns: 340px 1fr 360px;
      gap: var(--spacing-2);
      height: 100%;
      min-height: calc(100vh - 120px);
      padding: var(--spacing-2);
      box-sizing: border-box;
      background: radial-gradient(circle at 50% 50%, #080816 0%, #03030c 100%);
      font-family: var(--ui);
      color: var(--text);
    }
    
    .q-obs-card {
      background: rgba(9, 21, 37, 0.45);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(232, 240, 255, 0.08);
      border-radius: 12px;
      padding: var(--spacing-2);
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
      transition: border-color var(--transition-base), box-shadow var(--transition-base);
    }
    
    .q-obs-card:hover {
      border-color: rgba(0, 229, 255, 0.25);
      box-shadow: 0 15px 50px rgba(0, 229, 255, 0.08);
    }
    
    .q-obs-controls {
      overflow-y: auto;
    }
    
    .q-obs-header {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      margin-bottom: var(--spacing-2);
    }
    
    .q-obs-icon {
      font-size: 2.2rem;
      background: linear-gradient(135deg, var(--planck), var(--propagate));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 2px 8px rgba(0, 229, 255, 0.4));
      animation: spin 12s linear infinite;
    }
    
    @keyframes spin {
      100% { transform: rotate(360deg); }
    }
    
    .q-obs-headline {
      font-family: var(--headline);
      font-size: var(--font-size-xl);
      margin: 0;
      letter-spacing: -0.02em;
    }
    
    .q-obs-subhead {
      font-size: var(--font-size-xs);
      color: var(--muted);
      margin: 2px 0 0 0;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .q-obs-divider {
      height: 1px;
      background: linear-gradient(90deg, rgba(232, 240, 255, 0.15) 0%, rgba(232, 240, 255, 0.0) 100%);
      margin: var(--spacing-2) 0;
    }
    
    .q-control-group {
      margin-bottom: var(--spacing-2);
    }
    
    .q-label {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: var(--font-size-sm);
      margin-bottom: 6px;
      font-weight: 500;
    }
    
    .q-val-display {
      font-family: var(--formula);
      color: var(--propagate);
      text-shadow: 0 0 8px rgba(0, 229, 255, 0.4);
    }
    
    .q-slider {
      -webkit-appearance: none;
      width: 100%;
      height: 6px;
      border-radius: 3px;
      background: rgba(232, 240, 255, 0.1);
      outline: none;
      margin: 8px 0;
    }
    
    .q-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--planck);
      cursor: pointer;
      box-shadow: 0 0 10px var(--planck);
      transition: transform var(--transition-fast);
    }
    
    .q-slider::-webkit-slider-thumb:hover {
      transform: scale(1.2);
    }
    
    .q-hint {
      display: block;
      font-size: 11px;
      color: var(--muted);
      line-height: 1.3;
    }
    
    .q-select {
      width: 100%;
      background: var(--surface);
      color: var(--text);
      border: 1px solid rgba(232, 240, 255, 0.15);
      border-radius: 6px;
      padding: var(--spacing-1);
      font-family: var(--ui);
      font-size: var(--font-size-sm);
      outline: none;
      cursor: pointer;
    }
    
    .q-toggle-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }
    
    .q-toggle-label {
      font-size: var(--font-size-sm);
      font-weight: 500;
    }
    
    .q-toggle {
      width: 40px;
      height: 20px;
      -webkit-appearance: none;
      background: rgba(232, 240, 255, 0.15);
      border-radius: 10px;
      position: relative;
      outline: none;
      cursor: pointer;
      transition: background var(--transition-base);
    }
    
    .q-toggle:checked {
      background: var(--cohere);
    }
    
    .q-toggle::before {
      content: '';
      position: absolute;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--text);
      top: 2px;
      left: 2px;
      transition: left var(--transition-base);
    }
    
    .q-toggle:checked::before {
      left: 22px;
    }
    
    .q-btn-entrain {
      background: linear-gradient(135deg, rgba(0, 229, 255, 0.2) 0%, rgba(105, 255, 148, 0.2) 100%);
      border: 1px solid var(--propagate);
      color: var(--text);
      border-radius: 8px;
      padding: var(--spacing-2);
      font-family: var(--ui);
      font-size: var(--font-size-sm);
      font-weight: 600;
      cursor: pointer;
      transition: background var(--transition-base), box-shadow var(--transition-base);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .q-btn-entrain:hover {
      background: linear-gradient(135deg, rgba(0, 229, 255, 0.35) 0%, rgba(105, 255, 148, 0.35) 100%);
      box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
    }
    
    .q-btn-entrain.is-active {
      background: linear-gradient(135deg, rgba(255, 107, 157, 0.3) 0%, rgba(255, 179, 71, 0.3) 100%);
      border-color: var(--resonate);
      box-shadow: 0 0 15px rgba(255, 107, 157, 0.4);
    }
    
    .q-obs-stage {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-2);
      height: 100%;
    }
    
    .q-obs-webgl {
      flex: 1;
      position: relative;
      min-height: 380px;
    }
    
    .q-obs-card-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--muted);
      margin-bottom: var(--spacing-1);
      font-weight: 600;
    }
    
    .q-obs-row {
      display: grid;
      grid-template-columns: 240px 1fr;
      gap: var(--spacing-2);
      height: 240px;
    }
    
    .q-obs-qft {
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .q-obs-metrics {
      justify-content: space-between;
    }
    
    .q-metric-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: var(--spacing-1) var(--spacing-2);
      background: rgba(232, 240, 255, 0.03);
      border-radius: 6px;
      border: 1px solid rgba(232, 240, 255, 0.05);
    }
    
    .q-m-lbl {
      font-size: var(--font-size-sm);
      color: var(--muted);
    }
    
    .q-m-val {
      font-family: var(--formula);
      font-size: var(--font-size-base);
      font-weight: 600;
    }
    
    .q-obs-audit {
      overflow-y: auto;
    }
    
    .q-tier-box {
      background: rgba(232, 240, 255, 0.03);
      border: 1px solid rgba(232, 240, 255, 0.06);
      border-radius: 8px;
      padding: var(--spacing-2);
      margin-bottom: var(--spacing-2);
      transition: background var(--transition-base), border-color var(--transition-base);
    }
    
    .q-tier-box:hover {
      background: rgba(232, 240, 255, 0.06);
      border-color: rgba(232, 240, 255, 0.15);
    }
    
    .q-tier-title {
      font-family: var(--headline);
      font-size: var(--font-size-lg);
      margin-bottom: var(--spacing-1);
    }
    
    #tierMeasured .q-tier-title { color: var(--propagate); }
    #tierModel .q-tier-title { color: var(--cohere); }
    #tierStory .q-tier-title { color: var(--planck); }
    
    .q-tier-desc {
      font-size: var(--font-size-sm);
      color: var(--muted);
      margin: 0 0 10px 0;
      line-height: 1.4;
    }
    
    .q-tier-evidence {
      font-family: var(--ui);
      font-size: 11px;
      background: rgba(0, 0, 0, 0.2);
      padding: var(--spacing-1);
      border-radius: 4px;
      line-height: 1.5;
    }
    
    /* Coherence Zone colors */
    .zone-aligned { color: var(--planck); text-shadow: 0 0 8px rgba(255, 215, 0, 0.4); }
    .zone-stable { color: var(--blue); text-shadow: 0 0 8px rgba(92, 164, 255, 0.4); }
    .zone-healing { color: var(--refract); text-shadow: 0 0 8px rgba(255, 179, 71, 0.4); }
    .zone-critical { color: var(--red); text-shadow: 0 0 8px rgba(255, 71, 87, 0.4); }
    
    /* Responsive overrides for 4K / Widescreen */
    @media (max-width: 1450px) {
      .q-obs-container {
        grid-template-columns: 1fr;
        overflow-y: auto;
      }
      .q-obs-controls, .q-obs-audit {
        max-height: 400px;
      }
    }
  `;

  // Hardware probe points to plot as 3D spheres
  const PROBE_POINTS = [
    { name: 'Fez 540 CX (Null)', cx: 540, t2: 188, conf: 0.45, color: 0xff4757, desc: 'Fez PQC absence run. False-positive period 8 due to readout noise on bit 4.' },
    { name: 'Kingston 540 CX (Null)', cx: 540, t2: 187, conf: 0.35, color: 0xffa502, desc: 'Kingston PQC absence run. False-positive period 5.' },
    { name: 'Fez 33K CX (Null)', cx: 33000, t2: 188, conf: 0.05, color: 0x2ed573, desc: 'Fez PQC absence run (high depth). Correctly rejects noise (period 15).' },
    { name: 'Kingston Shor (540 CX)', cx: 540, t2: 187, conf: 0.85, color: 0x1e90ff, desc: 'Kingston Shor v1 run. Period 4 successfully extracted.' }
  ];

  // Tone.js Soundscape State
  let audioCtxActive = false;
  let synth = null;
  let noise = null;
  let noiseFilter = null;

  function initAudio() {
    if (synth) return;
    
    // Create phi-harmonic polyphonic synthesizer
    synth = new Tone.PolySynth(Tone.Synth, {
      oscillator: { type: 'sine' },
      envelope: {
        attack: 0.1,
        decay: 0.2,
        sustain: 0.6,
        release: 0.8
      }
    }).toDestination();
    
    // Create Pink noise generator to model the hardware noise floor
    noise = new Tone.Noise('pink');
    noiseFilter = new Tone.Filter(800, 'lowpass').toDestination();
    noise.connect(noiseFilter);
    noise.volume.value = -Infinity; // Start completely silent
    noise.start();
  }

  function updateAudio(coherence, period) {
    if (!synth || !audioCtxActive) return;

    // Adjust noise floor level based on dephasing
    if (coherence < 0.382) {
      // Critical Yield: loud noise, detuned synth
      noise.volume.rampTo(-18, 0.3);
      noiseFilter.frequency.rampTo(1200, 0.3);
    } else if (coherence < 0.618) {
      // Healing Zone: soft background noise
      noise.volume.rampTo(-28, 0.3);
      noiseFilter.frequency.rampTo(600, 0.3);
    } else {
      // Stable/Aligned: completely silent noise floor
      noise.volume.rampTo(-Infinity, 0.5);
    }

    // Dynamic carrier chords based on period
    // Map extracted period to phi-harmonic intervals
    let frequencies = [432, 540, 648]; // Default period 4 (perfect major triad)
    if (period === 8) {
      frequencies = [432, 864, 1296]; // Octave + Octave-fifth
    } else if (period === 5) {
      frequencies = [432, 518.4, 648]; // Minor-like intervals
    } else if (period === 15 || period === 'None') {
      frequencies = [382, 496, 618]; // Dispersed/detuned
    }

    // Add vibrato/detune if dephasing is high
    synth.set({
      detune: coherence < 0.618 ? (0.618 - coherence) * -200 : 0
    });

    // Trigger chord
    synth.triggerAttackRelease(frequencies, '8n');
  }

  function stopAudio() {
    if (synth) {
      synth.releaseAll();
    }
    if (noise) {
      noise.volume.rampTo(-Infinity, 0.3);
    }
  }

  PFExplorer.registerPanel({
    id: 'quantum-observatory',
    title: 'Quantum Substrate Observatory',

    mount: function (ctx) {
      var self = this;
      // Inject CSS Styles
      const styleEl = document.createElement('style');
      styleEl.textContent = CSS_STYLES;
      ctx.stage.appendChild(styleEl);

      // Inject HTML Layout
      const shell = document.createElement('div');
      shell.className = 'q-obs-container';
      shell.innerHTML = `
        <!-- Left Side: Controls -->
        <div class="q-obs-card q-obs-controls">
          <div class="q-obs-header">
            <span class="q-obs-icon">⚛</span>
            <div>
              <h2 class="q-obs-headline">Quantum Substrate</h2>
              <p class="q-obs-subhead">Shor Probe & Noise Spectroscopy</p>
            </div>
          </div>
          <div class="q-obs-divider"></div>
          
          <div class="q-control-group">
            <label class="q-label">
              <span>CX Gate Count</span>
              <span class="q-val-display" id="cxVal">540</span>
            </label>
            <input type="range" class="q-slider" id="cxSlider" min="100" max="33000" step="100" value="540">
            <span class="q-hint">Target circuit size (N=15: 540; N=21: ~33K)</span>
          </div>

          <div class="q-control-group">
            <label class="q-label">
              <span>Coherence Time (T₂ Ratio)</span>
              <span class="q-val-display" id="t2Val">188 μs</span>
            </label>
            <input type="range" class="q-slider" id="t2Slider" min="10" max="500" step="5" value="188">
            <span class="q-hint">Qubit dephasing limit (decay scale)</span>
          </div>

          <div class="q-control-group">
            <label class="q-label">
              <span>Gate Duration</span>
              <span class="q-val-display" id="gateVal">80 ns</span>
            </label>
            <input type="range" class="q-slider" id="gateSlider" min="10" max="300" step="10" value="80">
            <span class="q-hint">CZ gate pulse duration on hardware</span>
          </div>

          <div class="q-control-group">
            <label class="q-label">
              <span>Extraction Method</span>
            </label>
            <select class="q-select" id="extractorSelect">
              <option value="top-vote" selected>Top-Vote (Honest Extractor)</option>
              <option value="kl-div">KL Divergence (Structural Extractor)</option>
              <option value="combined">Combined Extractor (Convergence)</option>
            </select>
          </div>

          <div class="q-control-group">
            <div class="q-toggle-row">
              <span class="q-toggle-label">ZNE Twirling</span>
              <input type="checkbox" class="q-toggle" id="twirlingToggle">
            </div>
            <span class="q-hint">Stochasticizes errors but dephases peak relations</span>
          </div>

          <div class="q-control-group">
            <div class="q-toggle-row">
              <span class="q-toggle-label">Power-of-2 Pruning</span>
              <input type="checkbox" class="q-toggle" id="pruningToggle" checked>
            </div>
            <span class="q-hint">Optimizes control gates when period divides register size</span>
          </div>

          <div class="q-obs-divider"></div>
          <button class="q-btn-entrain" id="audioToggle">Activate Entrainment (432 Hz)</button>
        </div>

        <!-- Center Stage: 3D Visualization + QFT Circle -->
        <div class="q-obs-stage">
          <div class="q-obs-card q-obs-webgl" id="webglContainer">
            <div class="q-obs-card-label">NOISE SPECTROSCOPY BOUNDARY (3D)</div>
            <!-- WebGL element mounted here -->
          </div>
          
          <div class="q-obs-row">
            <!-- QFT Phase Circle -->
            <div class="q-obs-card q-obs-qft">
              <div class="q-obs-card-label">8-QUBIT QFT PHASE RELATIONSHIPS</div>
              <canvas id="qftCanvas" width="180" height="180"></canvas>
            </div>
            
            <!-- Live Metrics -->
            <div class="q-obs-card q-obs-metrics">
              <div class="q-obs-card-label">REAL-TIME SPECTROSCOPY</div>
              <div class="q-metric-item">
                <span class="q-m-lbl">Current Zone:</span>
                <span class="q-m-val" id="coherenceZone">Stable (0.68)</span>
              </div>
              <div class="q-metric-item">
                <span class="q-m-lbl">Estimated Period:</span>
                <span class="q-m-val" id="extractedPeriod">4 (True)</span>
              </div>
              <div class="q-metric-item">
                <span class="q-m-lbl">Entropy Index:</span>
                <span class="q-m-val" id="entropyIndex">0.24 bits</span>
              </div>
              <div class="q-metric-item">
                <span class="q-m-lbl">Gate Count Redux:</span>
                <span class="q-m-val" id="gateRedux">50% (Pruned)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Three-Tier Audits -->
        <div class="q-obs-card q-obs-audit">
          <div class="q-obs-card-label">THREE-TIER SPECTROSCOPY LEDGER</div>
          
          <div class="q-tier-box" id="tierMeasured">
            <div class="q-tier-title">MEASURED (Physical Reality)</div>
            <p class="q-tier-desc">Raw counting register distributions from hardware runs.</p>
            <div class="q-tier-evidence" id="measuredEvidence">
              Loading measured audit...
            </div>
          </div>

          <div class="q-tier-box" id="tierModel">
            <div class="q-tier-title">MODEL (Dephasing Physics)</div>
            <p class="q-tier-desc">T2 decay projection: <span class="formula">S = exp(-t_idle / T2)</span>.</p>
            <div class="q-tier-evidence">
              <strong>Decay projection:</strong> <span id="decayProj">93.8% (Survives)</span>
            </div>
          </div>

          <div class="q-tier-box" id="tierStory">
            <div class="q-tier-title">STORY (Human Framework)</div>
            <p class="q-tier-desc">Claims database statements and confidence ratings.</p>
            <div class="q-tier-evidence">
              <strong>Claim C-054:</strong> Fez bit 4 readout noise (Score: 0.85)<br>
              <strong>Claim C-037:</strong> Pruning on power-of-2 (Score: 0.90)
            </div>
          </div>
        </div>
      `;
      ctx.stage.appendChild(shell);

      // Cache DOM references inside panelState
      const panelState = {
        cxSlider: shell.querySelector('#cxSlider'),
        t2Slider: shell.querySelector('#t2Slider'),
        gateSlider: shell.querySelector('#gateSlider'),
        extractorSelect: shell.querySelector('#extractorSelect'),
        twirlingToggle: shell.querySelector('#twirlingToggle'),
        pruningToggle: shell.querySelector('#pruningToggle'),
        
        cxVal: shell.querySelector('#cxVal'),
        t2Val: shell.querySelector('#t2Val'),
        gateVal: shell.querySelector('#gateVal'),
        
        coherenceZone: shell.querySelector('#coherenceZone'),
        extractedPeriod: shell.querySelector('#extractedPeriod'),
        entropyIndex: shell.querySelector('#entropyIndex'),
        gateRedux: shell.querySelector('#gateRedux'),
        
        decayProj: shell.querySelector('#decayProj'),
        measuredEvidence: shell.querySelector('#measuredEvidence'),
        
        audioToggle: shell.querySelector('#audioToggle'),
        qftCanvas: shell.querySelector('#qftCanvas'),
        webglContainer: shell.querySelector('#webglContainer'),
        
        _3d: null,
        _animationFrame: null,
        _isAudioRunning: false
      };

      this.state = panelState;

      // Initialize WebGL Scene
      initWebGL(panelState);

      // Bind Listeners
      const update = () => {
        recalculatePhysics(panelState);
      };
      
      panelState.cxSlider.addEventListener('input', (e) => {
        panelState.cxVal.textContent = e.target.value;
        update();
      });
      
      panelState.t2Slider.addEventListener('input', (e) => {
        panelState.t2Val.textContent = e.target.value + ' μs';
        update();
      });
      
      panelState.gateSlider.addEventListener('input', (e) => {
        panelState.gateVal.textContent = e.target.value + ' ns';
        update();
      });

      panelState.extractorSelect.addEventListener('change', update);
      panelState.twirlingToggle.addEventListener('change', update);
      panelState.pruningToggle.addEventListener('change', update);

      // Audio Toggle click handler
      panelState.audioToggle.addEventListener('click', () => {
        if (!panelState._isAudioRunning) {
          // Initialize Tone.js and resume context
          initAudio();
          Tone.start();
          audioCtxActive = true;
          panelState._isAudioRunning = true;
          panelState.audioToggle.textContent = 'Mute Entrainment';
          panelState.audioToggle.classList.add('is-active');
          recalculatePhysics(panelState); // Trigger immediate sound play
        } else {
          stopAudio();
          audioCtxActive = false;
          panelState._isAudioRunning = false;
          panelState.audioToggle.textContent = 'Activate Entrainment (432 Hz)';
          panelState.audioToggle.classList.remove('is-active');
        }
      });

      // Initial calculation
      recalculatePhysics(panelState);

      // Start animation loop
      animate(panelState);

      // Trigger initial resize sync
      self.resize();
    },

    unmount: function () {
      if (this.state) {
        // Stop audio
        stopAudio();
        this.state._isAudioRunning = false;

        // Cancel animation frame
        if (this.state._animationFrame) {
          cancelAnimationFrame(this.state._animationFrame);
        }

        // Clean up WebGL
        if (this.state._3d) {
          const r = this.state._3d;
          r.renderer.dispose();
          r.container.innerHTML = '';
        }
      }
      this.state = null;
    },

    resize: function () {
      if (this.state && this.state._3d) {
        const r = this.state._3d;
        const w = r.container.clientWidth;
        const h = r.container.clientHeight;
        r.camera.aspect = w / h;
        r.camera.updateProjectionMatrix();
        r.renderer.setSize(w, h);
      }
    }
  });

  // ── Physics Recalculations ──────────────────────────────────────────────────
  
  function recalculatePhysics(panelState) {
    const cx = parseInt(panelState.cxSlider.value, 10);
    const t2 = parseInt(panelState.t2Slider.value, 10);
    const gateNs = parseInt(panelState.gateSlider.value, 10);
    const extractor = panelState.extractorSelect.value;
    const twirling = panelState.twirlingToggle.checked;
    const pruning = panelState.pruningToggle.checked;

    // Pruning reduces active CX counts by 50% for power-of-2 target simulation
    const redux = pruning ? 0.5 : 0.0;
    const effectiveCx = cx * (1 - redux);
    
    // Calculate idle time in microseconds
    // (Assuming a simple linear depth mapping: depth = effectiveCx * 3.5)
    const depth = effectiveCx * 3.5;
    const tIdleUs = (depth * gateNs) / 1000;

    // Dephasing decay factor: S = exp(-t_idle / T2)
    const decay = Math.exp(-tIdleUs / t2);
    panelState.decayProj.textContent = (decay * 100).toFixed(1) + '%';
    
    if (decay > 0.8) {
      panelState.decayProj.className = 'zone-aligned';
    } else if (decay > 0.6) {
      panelState.decayProj.className = 'zone-stable';
    } else if (decay > 0.38) {
      panelState.decayProj.className = 'zone-healing';
    } else {
      panelState.decayProj.className = 'zone-critical';
    }

    // Determine Coherence Zone
    let zone = '';
    let zoneClass = '';
    if (decay >= 0.844) {
      zone = 'Aligned';
      zoneClass = 'zone-aligned';
    } else if (decay >= 0.618) {
      zone = 'Stable';
      zoneClass = 'zone-stable';
    } else if (decay >= 0.382) {
      zone = 'Healing';
      zoneClass = 'zone-healing';
    } else {
      zone = 'Critical Yield';
      zoneClass = 'zone-critical';
    }
    panelState.coherenceZone.innerHTML = `<span class="${zoneClass}">${zone} (${decay.toFixed(2)})</span>`;

    // Map extracted period based on method and dephasing limits
    let extracted = '4 (True)';
    let entropy = (0.05 + (1 - decay) * 1.5).toFixed(2); // Entropy rises as coherence decays

    if (extractor === 'top-vote') {
      // Top-vote has high recall but low precision: it invents periods from noise
      if (decay < 0.382) {
        // Under high noise, it invents period 5 or 8 from noise (false positive)
        extracted = cx < 10000 ? '8 (False Pos)' : '5 (False Pos)';
      } else {
        extracted = '4 (True)';
      }
    } else if (extractor === 'kl-div') {
      // KL divergence has high precision but low recall: rejects when noise is high
      if (decay < 0.618) {
        extracted = 'None (Rejected)';
        entropy = (1.5 + (1 - decay) * 2.0).toFixed(2);
      } else {
        extracted = '4 (True)';
      }
    } else {
      // Combined: cross-checks period divisibility, robust
      if (decay < 0.382) {
        extracted = 'None (No consensus)';
      } else {
        extracted = '4 (True)';
      }
    }

    panelState.extractedPeriod.textContent = extracted;
    panelState.entropyIndex.textContent = entropy + ' bits';
    panelState.gateRedux.textContent = pruning ? '50% (Pruned)' : '0% (Standard)';

    // Update Audited Measured Box description dynamically based on slider
    let measuredText = '';
    if (cx <= 1000) {
      measuredText = `<strong>Kingston Shor v1 (540 CX):</strong> Period 4 extracted successfully.<br>
                      <strong>Fez 540 CX (Null):</strong> False-pos period 8 (readout error on bit 4).`;
    } else {
      measuredText = `<strong>Fez 33K CX (Null):</strong> Correctly rejects noise (returns no period).<br>
                      <strong>Kingston LWE (33K CX):</strong> Decay restricts phase recovery.`;
    }
    panelState.measuredEvidence.innerHTML = measuredText;

    // Trigger Synth audio update
    if (panelState._isAudioRunning) {
      const numericPeriod = extracted.includes('4') ? 4 : (extracted.includes('8') ? 8 : (extracted.includes('5') ? 5 : 'None'));
      updateAudio(decay, numericPeriod);
    }

    // Update WebGL Mesh deformity
    if (panelState._3d && panelState._3d.boundaryMesh) {
      const mesh = panelState._3d.boundaryMesh;
      const positions = mesh.geometry.attributes.position.array;
      const widthSegments = 20;
      const heightSegments = 20;

      for (let i = 0; i <= widthSegments; i++) {
        // x represents CX Gate count (scaled 0 to 33000)
        const xVal = (i / widthSegments) * 33000;
        const eCx = xVal * (1 - redux);
        const dep = eCx * 3.5;
        const tId = (dep * gateNs) / 1000;

        for (let j = 0; j <= heightSegments; j++) {
          // y represents T2 coherence time (scaled 10 to 500)
          const yVal = 10 + (j / heightSegments) * 490;
          
          // Calculated boundary dephasing
          const dec = Math.exp(-tId / yVal);
          
          const index = (i * (heightSegments + 1) + j) * 3;
          // Set Z height relative to dephasing confidence
          positions[index + 2] = dec * 2.0 - 1.0; 
        }
      }
      mesh.geometry.attributes.position.needsUpdate = true;
      mesh.geometry.computeVertexNormals();
    }
  }

  // ── WebGL Engine Initializer ──────────────────────────────────────────────

  function initWebGL(panelState) {
    const container = panelState.webglContainer;
    
    // Create Renderer
    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    } catch (e) {
      console.warn("WebGL not supported, running in fallback mode:", e);
      container.innerHTML = '';
      const fallbackDiv = document.createElement('div');
      fallbackDiv.className = 'webgl-fallback';
      fallbackDiv.style.cssText = 'display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; min-height: 250px; border: 1px dashed rgba(232, 240, 255, 0.2); border-radius: 8px; background: rgba(9, 21, 37, 0.2); color: rgba(232, 240, 255, 0.8); text-align: center; padding: 20px; box-sizing: border-box;';
      fallbackDiv.innerHTML = `
        <h4 style="margin: 0 0 8px 0; color: #00cfff; font-family: var(--headline);">WebGL Not Supported</h4>
        <p style="margin: 0; font-size: 12px; color: var(--muted); max-width: 280px; line-height: 1.4;">
          Coherence surface dephasing boundaries are calculated and monitored below in the QFT phase simulator and telemetry cards.
        </p>
      `;
      container.appendChild(fallbackDiv);
      panelState._3d = null;
      return;
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const w = container.clientWidth || 600;
    const h = container.clientHeight || 380;
    renderer.setSize(w, h);

    const scene = new THREE.Scene();
    
    // Camera
    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    camera.position.set(3, 3, 4.5);
    camera.lookAt(0, 0, 0);

    // OrbitControls
    let controls = null;
    if (window.THREE && window.THREE.OrbitControls) {
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.maxPolarAngle = Math.PI / 2 - 0.05; // Prevent camera going below floor
    }

    // Lighting
    scene.add(new THREE.AmbientLight(0x0f172a, 1.5));
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.8);
    dirLight.position.set(5, 10, 3);
    scene.add(dirLight);

    const fillLight = new THREE.PointLight(0x00cfff, 1.0, 10);
    fillLight.position.set(-3, 2, 2);
    scene.add(fillLight);

    // ── Build Grid Mesh Surface ──────────────────────────────────────────────
    const widthSegments = 20;
    const heightSegments = 20;
    const geometry = new THREE.PlaneGeometry(3, 3, widthSegments, heightSegments);
    
    // Custom material showing dephasing height colored zones
    const material = new THREE.MeshStandardMaterial({
      color: 0x00cfff,
      wireframe: true,
      transparent: true,
      opacity: 0.6,
      side: THREE.DoubleSide
    });

    const boundaryMesh = new THREE.Mesh(geometry, material);
    boundaryMesh.rotation.x = -Math.PI / 2; // Flat on floor
    boundaryMesh.position.y = -0.5;
    scene.add(boundaryMesh);

    // Draw coordinate axes lines
    const lineMat = new THREE.LineBasicMaterial({ color: 0x475569 });
    
    // X Axis (CX Gate Count)
    const xGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-1.5, -0.5, 1.5),
      new THREE.Vector3(1.8, -0.5, 1.5)
    ]);
    scene.add(new THREE.Line(xGeo, lineMat));

    // Y Axis (T2 Coherence)
    const yGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-1.5, -0.5, 1.5),
      new THREE.Vector3(-1.5, -0.5, -1.8)
    ]);
    scene.add(new THREE.Line(yGeo, lineMat));

    // Z Axis (Confidence / Coherence)
    const zGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-1.5, -0.5, 1.5),
      new THREE.Vector3(-1.5, 1.5, 1.5)
    ]);
    scene.add(new THREE.Line(zGeo, lineMat));

    // Plot Probe Points as glowing Spheres
    const spheres = [];
    PROBE_POINTS.forEach(pt => {
      const sphereGeo = new THREE.SphereGeometry(0.08, 16, 16);
      const sphereMat = new THREE.MeshStandardMaterial({
        color: pt.color,
        emissive: pt.color,
        emissiveIntensity: 0.8,
        roughness: 0.2
      });
      const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
      
      // Scale coordinates to fit WebGL boundaries (-1.5 to 1.5)
      const xPos = -1.5 + (pt.cx / 33000) * 3;
      const yPos = -0.5 + pt.conf * 2;
      const zPos = 1.5 - ((pt.t2 - 10) / 490) * 3;
      
      sphereMesh.position.set(xPos, yPos, zPos);
      scene.add(sphereMesh);
      spheres.push(sphereMesh);
    });

    panelState._3d = {
      container: container,
      renderer: renderer,
      scene: scene,
      camera: camera,
      controls: controls,
      boundaryMesh: boundaryMesh,
      spheres: spheres
    };
  }

  // ── Animation Loop ────────────────────────────────────────────────────────

  function animate(panelState) {
    function loop(time) {
      panelState._animationFrame = requestAnimationFrame(loop);

      const r = panelState._3d;
      if (r) {
        if (r.controls) {
          r.controls.update();
        }

        // Rotate boundary mesh slightly over time for dynamic view
        if (r.boundaryMesh) {
          // Slow rotation pulse
          const s = 1 + Math.sin(time / 2000) * 0.05;
          r.boundaryMesh.scale.set(s, s, 1);
        }

        // Pulse probe points glow
        if (r.spheres) {
          r.spheres.forEach(mesh => {
            mesh.material.emissiveIntensity = 0.6 + Math.sin(time / 300) * 0.4;
          });
        }

        r.renderer.render(r.scene, r.camera);
      }

      // Render the 2D QFT phase circles
      drawQFTCanvas(panelState, time);
    }
    panelState._animationFrame = requestAnimationFrame(loop);
  }

  // ── QFT Canvas Drawing ──────────────────────────────────────────────────────

  function drawQFTCanvas(panelState, time) {
    const canvas = panelState.qftCanvas;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    // Physics inputs
    const t2 = parseInt(panelState.t2Slider.value, 10);
    const cx = parseInt(panelState.cxSlider.value, 10);
    const gateNs = parseInt(panelState.gateSlider.value, 10);
    const twirling = panelState.twirlingToggle.checked;
    const pruning = panelState.pruningToggle.checked;

    const depth = cx * 3.5 * (pruning ? 0.5 : 1.0);
    const tIdleUs = (depth * gateNs) / 1000;
    const decay = Math.exp(-tIdleUs / t2); // coherence ratio

    const numQubits = 8;
    const center = { x: w / 2, y: h / 2 };
    const ringRadius = 60;

    // Draw central QFT connections (entanglement links)
    ctx.beginPath();
    ctx.strokeStyle = `rgba(0, 229, 255, ${decay * 0.15})`;
    ctx.lineWidth = 1;
    for (let i = 0; i < numQubits; i++) {
      const angleI = (i / numQubits) * Math.PI * 2;
      const xI = center.x + Math.cos(angleI) * ringRadius;
      const yI = center.y + Math.sin(angleI) * ringRadius;

      for (let j = i + 1; j < numQubits; j++) {
        const angleJ = (j / numQubits) * Math.PI * 2;
        const xJ = center.x + Math.cos(angleJ) * ringRadius;
        const yJ = center.y + Math.sin(angleJ) * ringRadius;

        ctx.moveTo(xI, yI);
        ctx.lineTo(xJ, yJ);
      }
    }
    ctx.stroke();

    // Draw individual qubit phase vectors
    for (let i = 0; i < numQubits; i++) {
      const angle = (i / numQubits) * Math.PI * 2;
      const qx = center.x + Math.cos(angle) * ringRadius;
      const qy = center.y + Math.sin(angle) * ringRadius;

      // Qubit base ring
      ctx.beginPath();
      ctx.arc(qx, qy, 14, 0, Math.PI * 2);
      ctx.fillStyle = '#091525';
      ctx.fill();
      ctx.strokeStyle = `rgba(232, 240, 255, ${0.1 + decay * 0.5})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Qubit index label
      ctx.fillStyle = 'rgba(232, 240, 255, 0.4)';
      ctx.font = '9px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`q${i}`, qx, qy + 20);

      // Phase Arrow direction calculation
      // Perfect coherence: all qubits in-phase or structured mod 4
      let phaseAngle = (time / 1000) * (i + 1) * 0.5; // base rotation
      
      if (!pruning) {
        // Unpruned: mismatch creates phase error offsets
        phaseAngle += i * 0.8;
      }

      // Add dephasing noise (phase dispersion)
      if (decay < 0.8) {
        const dispersionStrength = (1 - decay) * 2;
        // Map noise to random-walk phase perturbations
        phaseAngle += Math.sin(time / 200 + i) * dispersionStrength;
      }

      // ZNE twirling adds high frequency phase jitter (stochasticizes phase)
      if (twirling) {
        phaseAngle += Math.sin(time * 5 + i * 2) * 0.6;
      }

      const arrowLen = 10;
      const ax = qx + Math.cos(phaseAngle) * arrowLen;
      const ay = qy + Math.sin(phaseAngle) * arrowLen;

      // Draw Phase Arrow
      ctx.beginPath();
      ctx.moveTo(qx, qy);
      ctx.lineTo(ax, ay);
      
      // Determine arrow color based on coherence
      let arrowColor = '#00cfff'; // cyan
      if (decay < 0.382) {
        arrowColor = '#ff4757'; // red
      } else if (decay < 0.618) {
        arrowColor = '#ffa502'; // amber
      }
      
      ctx.strokeStyle = arrowColor;
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Arrow head
      ctx.fillStyle = arrowColor;
      ctx.beginPath();
      ctx.arc(ax, ay, 2, 0, Math.PI * 2);
      ctx.fill();
    }
  }

}());
