/**
 * PhiFlow Bridge — Receives live PhiFlow OSC events via WebSocket
 * and drives the Propagation Framework Explorer.
 *
 * When a PhiFlow program runs with --osc, it broadcasts events:
 *   /phi/start              — program begins
 *   /phi/intention/push     — intention scope entered (name, depth)
 *   /phi/intention/pop      — intention scope exited (name, depth)
 *   /phi/witness            — witness checkpoint (coherence, time, intention)
 *   /phi/resonate           — value broadcast (intention, value)
 *   /phi/coherence          — coherence score
 *   /phi/end                — program ended (final_coherence)
 *
 * The bridge maps these to explorer actions:
 *   intention push → navigate to journey section + audio scale transition
 *   resonate       → pulse audio + visual feedback
 *   witness        → play bell + flash overlay
 *   coherence      → adjust global lighting/filter
 *   end            → show completion state
 *
 * Usage (in journey_live.html):
 *   <script src="phi-bridge.js"></script>
 *
 * The bridge auto-connects to ws://localhost:18528 (or ?host= param).
 * It exposes window.PhiBridge with:
 *   connect()           — start WebSocket connection
 *   disconnect()        — close connection
 *   onEvent(callback)   — register for raw events
 *   status              — current connection status
 *
 * @version 1.0.0
 */

(function () {
  'use strict';

  // ═════════════════════════════════════════════════════════════════
  //  INTENTION → JOURNEY SECTION MAP
  // ═════════════════════════════════════════════════════════════════

  // Each PhiFlow intention name maps to a journey section + audio scale
  var INTENTION_MAP = {
    'opening': {
      section: 'opening',
      scale: 'human',         // 432 Hz — grounded, where we start
      label: 'Opening: Three Axioms'
    },
    'act1_unlearning': {
      section: 'act1',
      scale: 'human',         // 432 Hz — human intuition being dismantled
      label: 'Act I: The Great Unlearning'
    },
    'act2_coherence': {
      section: 'act2',
      scale: 'cellular',      // 528 Hz — creation, life emerges
      label: 'Act II: The Symphony of Coherence'
    },
    'act3_anchor': {
      section: 'act3',
      scale: 'nuclear',       // 720 Hz — vision gate, cross-scale
      label: 'Act III: The Geometric Anchor'
    },
    'act4_scoreboard': {
      section: 'act4',
      scale: 'compton',       // 768 Hz — unity, full picture
      label: 'Act IV: The Full Scoreboard'
    },
    'epilogue_falsification': {
      section: 'epilogue',
      scale: 'cosmic',        // 108 Hz — the void, where truth lives
      label: 'Epilogue: What Would Kill This'
    }
  };

  // ═════════════════════════════════════════════════════════════════
  //  RESONATE → MEANING MAP
  // ═════════════════════════════════════════════════════════════════

  // Resonate values that carry semantic meaning (strings)
  var RESONANCE_MEANINGS = {
    'axiom1': 'Everything propagates through a structured medium',
    'axiom2': 'Propagation is local — no action at a distance',
    'axiom3': 'Stable structures are self-reinforcing closed loops',
    'gravity_is_refraction': 'Gravity is bent propagation, not a pull',
    'matter_is_pattern': 'Matter is a standing wave, not solid stuff',
    'n3_topological_lock': 'N=3 is a topological lock, not arbitrary',
    'tune_the_medium': 'When waves align, structure emerges',
    'phase_closure': 'Only integer orbits close — this is quantization',
    'coherence_is_the_law': 'Coherence is the law. Stability is the exception.',
    'god_equation': 'One equation crosses 17 orders of magnitude',
    'the_keyhole': 'We found the keyhole. We are learning to turn the key.',
    'the_scoreboard': '22 audited claims. 3 derived. 4 conditional. Honest.',
    'three_vs_nineteen': '3 axioms vs 19+ parameters vs 10^500 landscapes',
    'six_ways_to_kill': 'Six ways to kill this framework. Each a falsifier.',
    'honesty_is_the_only_currency': 'Honesty is the only currency. The duck watches.'
  };

  // ═════════════════════════════════════════════════════════════════
  //  BRIDGE STATE
  // ═════════════════════════════════════════════════════════════════

  var ws = null;
  var connected = false;
  var currentIntention = null;
  var eventListeners = [];
  var wsPort = 18528;
  var reconnectTimer = null;

  // Get host from URL param
  var urlParams = new URLSearchParams(location.search);
  var hostParam = urlParams.get('host') || 'localhost';

  // ═════════════════════════════════════════════════════════════════
  //  UI OVERLAY
  // ═════════════════════════════════════════════════════════════════

  function createOverlay() {
    var existing = document.getElementById('phi-bridge-overlay');
    if (existing) return;

    var overlay = document.createElement('div');
    overlay.id = 'phi-bridge-overlay';
    overlay.style.cssText = [
      'position: fixed',
      'top: 10px',
      'right: 10px',
      'z-index: 9999',
      'background: rgba(0,0,0,0.85)',
      'border: 1px solid rgba(68,136,255,0.4)',
      'border-radius: 10px',
      'padding: 14px 18px',
      'font-family: Georgia, serif',
      'font-size: 13px',
      'color: #fff',
      'max-width: 340px',
      'pointer-events: none',
      'transition: opacity 0.3s'
    ].join(';');

    overlay.innerHTML =
      '<div style="color:#4af; font-size:14px; margin-bottom:6px; letter-spacing:1px;">' +
        'PhiFlow Live Bridge' +
      '</div>' +
      '<div id="phi-bridge-status" style="color:#fa0; font-size:12px;">' +
        'Connecting to ws://' + hostParam + ':' + wsPort + '...' +
      '</div>' +
      '<div id="phi-bridge-intention" style="color:#4af; font-size:13px; margin-top:6px; min-height:18px;"></div>' +
      '<div id="phi-bridge-resonance" style="color:#4f4; font-size:12px; margin-top:4px; min-height:16px; font-style:italic;"></div>' +
      '<div id="phi-bridge-coherence" style="color:#fa0; font-size:12px; margin-top:4px;">Coherence: —</div>';

    document.body.appendChild(overlay);
  }

  function updateStatus(text, color) {
    var el = document.getElementById('phi-bridge-status');
    if (el) {
      el.textContent = text;
      el.style.color = color || '#fa0';
    }
  }

  function updateIntention(text) {
    var el = document.getElementById('phi-bridge-intention');
    if (el) el.textContent = text || '';
  }

  function updateResonance(text) {
    var el = document.getElementById('phi-bridge-resonance');
    if (el) el.textContent = text || '';
  }

  function updateCoherence(val) {
    var el = document.getElementById('phi-bridge-coherence');
    if (el) el.textContent = 'Coherence: ' + (val !== null ? val.toFixed(4) : '—');
  }

  // ═════════════════════════════════════════════════════════════════
  //  WITNESS FLASH OVERLAY
  // ═════════════════════════════════════════════════════════════════

  function witnessFlash(coherence) {
    var flash = document.createElement('div');
    var hue = 40 + coherence * 200;  // amber → blue-green at high coherence
    flash.style.cssText = [
      'position: fixed',
      'top: 0', 'left: 0', 'width: 100%', 'height: 100%',
      'z-index: 9998',
      'background: radial-gradient(circle at center, hsla(' + hue + ',80%,60%,0.15) 0%, transparent 70%)',
      'pointer-events: none',
      'transition: opacity 1.5s',
      'opacity: 1'
    ].join(';');
    document.body.appendChild(flash);

    // Fade out
    setTimeout(function () {
      flash.style.opacity = '0';
    }, 50);
    setTimeout(function () {
      if (flash.parentNode) flash.parentNode.removeChild(flash);
    }, 1600);
  }

  // ═════════════════════════════════════════════════════════════════
  //  JOURNEY NAVIGATION
  // ═════════════════════════════════════════════════════════════════

  function navigateToSection(sectionId) {
    // Strategy 1: If journey.js exposed goToSection globally, use it
    if (typeof window.goToSection === 'function') {
      window.goToSection(sectionId);
      return;
    }

    // Strategy 2: Simulate clicking the "next-act" button to advance
    // This uses journey.js's own navigation (including animation triggers)
    var sections = ['opening', 'act1', 'act2', 'act3', 'act4', 'epilogue'];
    var currentIdx = sections.indexOf(window._phiCurrentSection || 'opening');
    var targetIdx = sections.indexOf(sectionId);

    if (targetIdx > currentIdx) {
      // Click "next" buttons until we reach the target
      function advanceOnce() {
        var current = window._phiCurrentSection || 'opening';
        if (current === sectionId) return; // arrived

        var activeSection = document.getElementById('journey-' + current);
        if (!activeSection) return;

        var nextBtn = activeSection.querySelector('.next-act');
        if (nextBtn) {
          nextBtn.click();
          // Wait for the transition, then check again
          setTimeout(advanceOnce, 300);
        }
      }
      advanceOnce();
      return;
    }

    // Strategy 3: Direct DOM manipulation fallback
    var currentEl = document.querySelector('.journey-section.active');
    if (currentEl) currentEl.classList.remove('active');

    var nextEl = document.getElementById('journey-' + sectionId);
    if (nextEl) {
      nextEl.classList.add('active');
      window._phiCurrentSection = sectionId;
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ═════════════════════════════════════════════════════════════════
  //  AUDIO ENGINE INTEGRATION
  // ═════════════════════════════════════════════════════════════════

  function transitionAudio(scaleName) {
    if (typeof window.AudioEngine !== 'undefined' && window.AudioEngine.transitionTo) {
      window.AudioEngine.transitionTo(scaleName);
    }
  }

  function playInteractionSound(type) {
    if (typeof window.AudioEngine !== 'undefined' && window.AudioEngine.interact) {
      window.AudioEngine.interact(type);
    }
  }

  // ═════════════════════════════════════════════════════════════════
  //  EVENT HANDLING
  // ═════════════════════════════════════════════════════════════════

  function handleOscMessage(address, args) {
    // Notify raw event listeners
    eventListeners.forEach(function (cb) {
      try { cb(address, args); } catch (e) { console.error('[PhiBridge] Event listener error:', e); }
    });

    if (address === '/phi/start') {
      updateStatus('▶ PhiFlow program running', '#4f4');
      playInteractionSound('whoosh');
    }

    else if (address === '/phi/end') {
      var finalCoherence = args[0] || 0;
      updateStatus('■ Program ended — coherence ' + finalCoherence.toFixed(4), '#fa0');
      updateIntention('Journey complete');
      updateResonance('');
      playInteractionSound('explore');
    }

    else if (address === '/phi/intention/push') {
      var name = args[0];
      var depth = args[1];
      currentIntention = name;

      var mapping = INTENTION_MAP[name];
      if (mapping) {
        // Navigate to the journey section
        navigateToSection(mapping.section);

        // Transition audio to the matching scale
        transitionAudio(mapping.scale);

        // Update overlay
        updateIntention('▶ ' + mapping.label);
        updateResonance('');

        // Play transition sound
        playInteractionSound('whoosh');
      } else {
        updateIntention('→ ' + name + ' (depth ' + depth + ')');
      }
    }

    else if (address === '/phi/intention/pop') {
      var popName = args[0];
      if (popName === currentIntention) {
        currentIntention = null;
      }
    }

    else if (address === '/phi/resonate') {
      var intention = args[0];
      var value = args[1];

      // Check if value is a sacred frequency (number)
      if (typeof value === 'number' && value > 50 && value < 2000) {
        // Sacred frequency broadcast — the scale is changing
        updateResonance('🌊 ' + value.toFixed(1) + ' Hz');
      } else if (typeof value === 'string') {
        // Semantic resonance — look up the meaning
        var meaning = RESONANCE_MEANINGS[value];
        if (meaning) {
          updateResonance('🌊 ' + meaning);
        } else {
          updateResonance('🌊 ' + value);
        }
      }

      // Pulse the audio
      playInteractionSound('pop');
    }

    else if (address === '/phi/witness') {
      var coherence = args[0] || 0;
      var time = args[1];
      var witnessIntention = args[2];

      // Visual flash
      witnessFlash(coherence);

      // Audio bell
      playInteractionSound('click');

      // Update coherence display
      updateCoherence(coherence);
    }

    else if (address === '/phi/coherence') {
      var coh = args[0] || 0;
      updateCoherence(coh);

      // Could adjust global lighting here if the explorer exposes it
    }
  }

  // ═════════════════════════════════════════════════════════════════
  //  WEBSOCKET CONNECTION
  // ═════════════════════════════════════════════════════════════════

  function connect() {
    createOverlay();

    var wsUrl = 'ws://' + hostParam + ':' + wsPort;
    updateStatus('Connecting to ' + wsUrl + '...', '#fa0');

    try {
      ws = new WebSocket(wsUrl);
    } catch (e) {
      updateStatus('Cannot connect: ' + e.message, '#f44');
      scheduleReconnect();
      return;
    }

    ws.onopen = function () {
      connected = true;
      updateStatus('✅ Connected — waiting for PhiFlow...', '#4f4');
      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
        reconnectTimer = null;
      }
    };

    ws.onmessage = function (evt) {
      try {
        var msg = JSON.parse(evt.data);
        handleOscMessage(msg.address, msg.args);
      } catch (e) {
        console.error('[PhiBridge] Parse error:', e);
      }
    };

    ws.onclose = function () {
      connected = false;
      updateStatus('Disconnected — retrying in 3s...', '#fa0');
      scheduleReconnect();
    };

    ws.onerror = function () {
      if (ws) ws.close();
    };
  }

  function scheduleReconnect() {
    if (reconnectTimer) clearTimeout(reconnectTimer);
    reconnectTimer = setTimeout(function () {
      connect();
    }, 3000);
  }

  // ═════════════════════════════════════════════════════════════════
  //  FACILITATOR CUE SENDING (Ceremony Engine)
  // ═════════════════════════════════════════════════════════════════

  function sendOsc(address, args) {
    if (!ws || !connected) {
      console.warn('[PhiBridge] Not connected, cannot send:', address, args);
      return false;
    }
    try {
      ws.send(JSON.stringify({ address: address, args: args || [] }));
      return true;
    } catch (e) {
      console.error('[PhiBridge] Send error:', e);
      return false;
    }
  }

  function sendCue(channel, value) {
    return sendOsc('/ceremony/cue', [channel, value]);
  }

  function sendAdvance() {
    return sendOsc('/ceremony/advance', []);
  }

  function sendCoherence(value) {
    // value should be a number 0.0–1.0
    var num = parseFloat(value);
    if (isNaN(num)) num = 0.5;
    return sendOsc('/ceremony/coherence', [num]);
  }

  function disconnect() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    if (ws) {
      ws.onclose = null;
      ws.close();
      ws = null;
    }
    connected = false;
    updateStatus('Disconnected', '#888');
  }

  // ═════════════════════════════════════════════════════════════════
  //  PUBLIC API
  // ═════════════════════════════════════════════════════════════════

  window.PhiBridge = {
    connect: connect,
    disconnect: disconnect,
    onEvent: function (cb) { eventListeners.push(cb); },
    sendOsc: sendOsc,
    sendCue: sendCue,
    sendAdvance: sendAdvance,
    sendCoherence: sendCoherence,
    get status() { return connected ? 'connected' : 'disconnected'; },
    get currentIntention() { return currentIntention; },
    intentionMap: INTENTION_MAP,
    resonanceMeanings: RESONANCE_MEANINGS
  };

  // Auto-connect on load if we're in journey_live mode
  if (document.body && document.body.classList.contains('phi-live-mode')) {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', connect);
    } else {
      connect();
    }
  }

})();
