/**
 * Spatial Audio Engine for Propagation Framework Explorer
 * 
 * World-class soundscape using Tone.js
 * - Scale-reactive drones with distinct sonic signatures
 * - Smooth 500ms crossfades between scales
 * - Interaction sounds (click, whoosh, pop)
 * - Spatial positioning and reverb per scale
 * - Respects prefers-reduced-motion
 * - Mute state persists in localStorage
 * 
 * @version 1.0.0
 */

(function () {
  'use strict';

  // ═══════════════════════════════════════════════════════════════════════
  // SCALE AUDIO DEFINITIONS
  // ═══════════════════════════════════════════════════════════════════════

  const ScaleAudio = {
    // Each scale has a unique sonic signature
    human: {
      baseFreq: 432,
      overtone: [1, 1.5, 2],
      drone: 'solid',
      waveform: 'sine',
      stereoWidth: 0.3,
      reverbDecay: 1.5,
      reverbPreDelay: 0.02,
      description: 'Grounded, warm, earthly'
    },
    cellular: {
      baseFreq: 528,
      overtone: [1, 2, 3],
      drone: 'pulse',
      waveform: 'triangle',
      stereoWidth: 0.4,
      reverbDecay: 2.0,
      reverbPreDelay: 0.03,
      description: 'Living, breathing, organic'
    },
    molecular: {
      baseFreq: 594,
      overtone: [1, 1.618, 2.618], // Golden ratio harmonics
      drone: 'vibrate',
      waveform: 'sawtooth',
      stereoWidth: 0.5,
      reverbDecay: 2.5,
      reverbPreDelay:0.04,
      description: 'Resonant, structural, bonding'
    },
    atomic: {
      baseFreq: 672,
      overtone: [1, 2, 4, 8],
      drone: 'flutter',
      waveform: 'square',
      stereoWidth: 0.6,
      reverbDecay: 3.0,
      reverbPreDelay: 0.05,
      description: 'Energetic, orbital, quantum'
    },
    nuclear: {
      baseFreq: 720,
      overtone: [1, 1.2, 1.44],
      drone: 'confined',
      waveform: 'sine',
      stereoWidth: 0.4,
      reverbDecay: 1.8,
      reverbPreDelay: 0.02,
      description: 'Intense, bound, powerful'
    },
    compton: {
      baseFreq: 768,
      overtone: [1, 2, 3, 5],
      drone: 'standing',
      waveform: 'sine',
      stereoWidth: 0.5,
      reverbDecay: 4.0,
      reverbPreDelay: 0.08,
      description: 'Wave-like, matter as pattern'
    },
    gut: {
      baseFreq: 864,
      overtone: [1, 1.333, 2], // Perfect fourth
      drone: 'unified',
      waveform: 'triangle',
      stereoWidth: 0.7,
      reverbDecay: 5.0,
      reverbPreDelay: 0.1,
      description: 'Unified, force-merging'
    },
    planetary: {
      baseFreq: 216,
      overtone: [1, 2, 4],
      drone: 'orbit',
      waveform: 'sine',
      stereoWidth: 0.8,
      reverbDecay: 6.0,
      reverbPreDelay: 0.15,
      description: 'Vast, orbital, gravitational'
    },
    galactic: {
      baseFreq: 144,
      overtone: [1, 1.5, 2.5],
      drone: 'spiral',
      waveform: 'sine',
      stereoWidth: 0.9,
      reverbDecay: 8.0,
      reverbPreDelay: 0.2,
      description: 'Spiral, density waves, majestic'
    },
    cosmic: {
      baseFreq: 108,
      overtone: [1, 2, 3],
      drone: 'void',
      waveform: 'sine',
      stereoWidth: 1.0,
      reverbDecay: 10.0,
      reverbPreDelay: 0.3,
      description: 'Infinite, cosmic web, eternal'
    },
    planck: {
      baseFreq: 1728,
      overtone: [1, 2, 4, 8],
      drone: 'foam',
      waveform: 'sawtooth',
      stereoWidth: 0.2,
      reverbDecay: 1.2,
      reverbPreDelay: 0.01,
      description: 'Discrete, bubbling, primordial'
    }
  };

  // Map scene types to scale definitions
  const sceneTypeToScale = {
    'solid': 'human',
    'cells': 'cellular',
    'molecules': 'molecular',
    'atom': 'atomic',
    'standingWave': 'compton',
    'quantumFoam': 'planck',
    'planets': 'planetary',
    'galaxy': 'galactic',
    'cosmic': 'cosmic'
  };

  // ═══════════════════════════════════════════════════════════════════════
  // AUDIO ENGINE STATE
  // ═══════════════════════════════════════════════════════════════════════

  const AudioEngine = {
    // Core Tone.js objects
    ctx: null,
    masterGain: null,
    reverb: null,
    limiter: null,
    
    // Drone oscillators
    primaryOsc: null,
    overtoneOscs: [],
    currentScale: null,
    isInitialized: false,
    isMuted: false,
    isPlaying: false,
    
    // Interaction synths
    clickSynth: null,
    whooshSynth: null,
    popSynth: null,
    
    // Crossfade timing
    transitionTime: 0.5, // 500ms
    
    // User preference
    reducedMotion: false,

    // ═════════════════════════════════════════════════════════════════════
    // INITIALIZATION
    // ═════════════════════════════════════════════════════════════════════

    init: function () {
      if (this.isInitialized) return true;
      
      // Check for reduced motion preference
      this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (this.reducedMotion) {
        console.log('[AudioEngine] Reduced motion detected - audio disabled');
        return false;
      }

      // Check for existing mute preference
      try {
        const savedMute = localStorage.getItem('pf_audio_muted');
        if (savedMute !== null) {
          this.isMuted = savedMute === 'true';
        }
      } catch (e) {
        // localStorage not available
      }

      // Tone.js must be loaded
      if (typeof Tone === 'undefined') {
        console.warn('[AudioEngine] Tone.js not loaded');
        return false;
      }

      try {
        this._createAudioGraph();
        this._createInteractionSounds();
        this.isInitialized = true;
        console.log('[AudioEngine] Initialized successfully');
        return true;
      } catch (e) {
        console.error('[AudioEngine] Initialization failed:', e);
        return false;
      }
    },

    _createAudioGraph: function () {
      // Master limiter for safety
      this.limiter = new Tone.Limiter(-6).toDestination();
      
      // Master gain with mute capability
      this.masterGain = new Tone.Gain(this.isMuted ? 0 : 0.7).connect(this.limiter);
      
      // High-quality reverb
      this.reverb = new Tone.Reverb({
        decay: 2,
        preDelay: 0.05,
        wet: 0.4
      }).connect(this.masterGain);
      
      // Stereo widening via spatializer
      this.stereoWidener = new Tone.StereoWidener(0.5).connect(this.reverb);
      
      // Drone output path
      this.droneGain = new Tone.Gain(0).connect(this.stereoWidener);
      
      // Filter for smoothing
      this.droneFilter = new Tone.Filter(800, 'lowpass', -12).connect(this.droneGain);
    },

    _createInteractionSounds: function () {
      // Satisfying click - short sine burst
      this.clickSynth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: 'sine' },
        envelope: {
          attack: 0.001,
          decay: 0.08,
          sustain: 0,
          release: 0.05
        },
        volume: -12
      }).connect(this.masterGain);

      // Whoosh - filtered noise sweep
      this.whooshNoise = new Tone.Noise('pink').start();
      this.whooshFilter = new Tone.Filter(200, 'lowpass').connect(this.masterGain);
      this.whooshGain = new Tone.Gain(0).connect(this.whooshFilter);
      this.whooshNoise.connect(this.whooshGain);
      
      // Pop - quick membrane sound
      this.popSynth = new Tone.MembraneSynth({
        pitchDecay: 0.02,
        octaves: 3,
        oscillator: { type: 'sine' },
        envelope: {
          attack: 0.001,
          decay: 0.1,
          sustain: 0,
          release: 0.05
        },
        volume: -10
      }).connect(this.masterGain);
    },

    // ═════════════════════════════════════════════════════════════════════
    // USER INTERACTION START (browser autoplay policy)
    // ═════════════════════════════════════════════════════════════════════

    startOnUserInteraction: function () {
      if (!this.isInitialized) {
        this.init();
      }
      
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      
      if (Tone.context.state === 'suspended') {
        Tone.start();
      }
      
      this.isPlaying = true;
    },

    // ═════════════════════════════════════════════════════════════════════
    // SCALE TRANSITIONS
    // ═════════════════════════════════════════════════════════════════════

    transitionTo: function (sceneTypeOrScale) {
      if (!this.isInitialized || this.isMuted || this.reducedMotion) return;
      if (!this.isPlaying) return;

      const scaleName = sceneTypeToScale[sceneTypeOrScale] || sceneTypeOrScale;
      const scaleDef = ScaleAudio[scaleName];
      
      if (!scaleDef) {
        console.warn('[AudioEngine] Unknown scale:', scaleName);
        return;
      }

      if (this.currentScale === scaleName) return;
      this.currentScale = scaleName;

      // Update reverb for this scale
      this._updateReverb(scaleDef);
      
      // Update stereo width
      if (this.stereoWidener) {
        this.stereoWidener.width.rampTo(scaleDef.stereoWidth, this.transitionTime);
      }

      // Create new drone with crossfade
      this._crossfadeToScale(scaleDef);
    },

    _updateReverb: function (scaleDef) {
      if (!this.reverb) return;
      
      // Smoothly update reverb parameters
      this.reverb.decay = scaleDef.reverbDecay;
      this.reverb.preDelay = scaleDef.reverbPreDelay;
      
      // Adjust wet/dry based on scale character
      const wetAmount = scaleDef.reverbDecay > 5 ? 0.6 : 0.4;
      this.reverb.wet.rampTo(wetAmount, this.transitionTime);
    },

    _crossfadeToScale: function (scaleDef) {
      const now = Tone.now();
      
      // Fade out current drone
      if (this.droneGain) {
        this.droneGain.gain.rampTo(0, this.transitionTime, now);
      }

      // Clean up old oscillators after fade
      const oldOscs = [this.primaryOsc, ...this.overtoneOscs];
      setTimeout(() => {
        oldOscs.forEach(osc => {
          if (osc) {
            osc.stop();
            osc.dispose();
          }
        });
      }, this.transitionTime * 1000 + 50);

      // Create new primary oscillator
      this.primaryOsc = new Tone.Oscillator({
        frequency: scaleDef.baseFreq,
        type: scaleDef.waveform,
        volume: -18
      }).connect(this.droneFilter);

      // Add subtle FM for richness on certain scales
      if (scaleDef.drone === 'vibrate' || scaleDef.drone === 'flutter') {
        const fmOsc = new Tone.Oscillator(scaleDef.baseFreq * 0.01, 'sine').start();
        const fmGain = new Tone.Gain(scaleDef.baseFreq * 0.1).connect(this.primaryOsc.frequency);
        fmOsc.connect(fmGain);
        this.primaryOsc.fmOsc = fmOsc;
        this.primaryOsc.fmGain = fmGain;
      }

      this.primaryOsc.start(now + this.transitionTime * 0.3);

      // Create overtone oscillators
      this.overtoneOscs = [];
      scaleDef.overtone.forEach((ratio, i) => {
        const overtoneVol = -24 - (i * 3); // Decreasing volume for higher harmonics
        const osc = new Tone.Oscillator({
          frequency: scaleDef.baseFreq * ratio,
          type: scaleDef.waveform,
          volume: overtoneVol
        }).connect(this.droneFilter);
        
        // Detune slightly for beating effect
        osc.detune.value = (Math.random() - 0.5) * 10;
        
        osc.start(now + this.transitionTime * 0.3 + (i * 0.05));
        this.overtoneOscs.push(osc);
      });

      // Fade in new drone
      setTimeout(() => {
        if (this.droneGain) {
          this.droneGain.gain.rampTo(1, this.transitionTime * 0.5);
        }
      }, this.transitionTime * 300);
    },

    // ═════════════════════════════════════════════════════════════════════
    // INTERACTION SOUNDS
    // ═════════════════════════════════════════════════════════════════════

    playInteraction: function (type) {
      if (!this.isInitialized || this.isMuted || this.reducedMotion) return;
      if (!this.isPlaying) return;

      switch (type) {
        case 'click':
        case 'advance':
          this._playClick();
          break;
        case 'whoosh':
        case 'zoom':
          this._playWhoosh();
          break;
        case 'pop':
        case 'button':
          this._playPop();
          break;
        case 'explore':
          this._playExplore();
          break;
        default:
          console.warn('[AudioEngine] Unknown interaction type:', type);
      }
    },

    _playClick: function () {
      if (!this.clickSynth) return;
      
      // Pleasant high-pitched confirmation
      const note = ['C6', 'E6', 'G6'][Math.floor(Math.random() * 3)];
      this.clickSynth.triggerAttackRelease(note, '16n');
    },

    _playWhoosh: function () {
      if (!this.whooshGain || !this.whooshFilter) return;
      
      const now = Tone.now();
      
      // Filter sweep from low to high
      this.whooshFilter.frequency.setValueAtTime(200, now);
      this.whooshFilter.frequency.exponentialRampToValueAtTime(4000, now + 0.3);
      
      // Amplitude envelope
      this.whooshGain.gain.cancelScheduledValues(now);
      this.whooshGain.gain.setValueAtTime(0, now);
      this.whooshGain.gain.linearRampToValueAtTime(0.3, now + 0.1);
      this.whooshGain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
    },

    _playPop: function () {
      if (!this.popSynth) return;
      this.popSynth.triggerAttackRelease('C4', '32n');
    },

    _playExplore: function () {
      if (!this.clickSynth) return;
      
      // Majestic chord for final explore
      this.clickSynth.triggerAttackRelease(['C4', 'E4', 'G4', 'C5'], '8n');
    },

    // ═════════════════════════════════════════════════════════════════════
    // MUTE CONTROL
    // ═════════════════════════════════════════════════════════════════════

    toggleMute: function () {
      this.isMuted = !this.isMuted;
      
      if (this.masterGain) {
        this.masterGain.gain.rampTo(this.isMuted ? 0 : 0.7, 0.1);
      }
      
      // Save preference
      try {
        localStorage.setItem('pf_audio_muted', this.isMuted.toString());
      } catch (e) {
        // localStorage not available
      }
      
      this._updateMuteButton();
      return this.isMuted;
    },

    setMute: function (muted) {
      this.isMuted = muted;
      
      if (this.masterGain) {
        this.masterGain.gain.rampTo(this.isMuted ? 0 : 0.7, 0.1);
      }
      
      try {
        localStorage.setItem('pf_audio_muted', this.isMuted.toString());
      } catch (e) {}
      
      this._updateMuteButton();
    },

    // ═════════════════════════════════════════════════════════════════════
    // UI INTEGRATION
    // ═════════════════════════════════════════════════════════════════════

    createMuteButton: function (container) {
      if (!container) {
        container = document.getElementById('zoomSequenceOverlay');
      }
      if (!container) return;

      // Check if button already exists
      if (document.getElementById('pf-audio-mute-btn')) return;

      const btn = document.createElement('button');
      btn.id = 'pf-audio-mute-btn';
      btn.className = 'pf-audio-mute-btn';
      btn.setAttribute('type', 'button');
      btn.setAttribute('aria-label', this.isMuted ? 'Unmute audio' : 'Mute audio');
      btn.innerHTML = this.isMuted ? '🔇' : '🔊';
      
      // Position in top-right
      btn.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10001;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(10,10,26,0.8);
        backdrop-filter: blur(10px);
        color: #fff;
        font-size: 20px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        opacity: 1;
        pointer-events: auto;
      `;

      btn.addEventListener('mouseenter', () => {
        btn.style.background = 'rgba(20,20,46,0.95)';
        btn.style.transform = 'scale(1.1)';
      });

      btn.addEventListener('mouseleave', () => {
        btn.style.background = 'rgba(10,10,26,0.8)';
        btn.style.transform = 'scale(1)';
      });

      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const muted = this.toggleMute();
        btn.innerHTML = muted ? '🔇' : '🔊';
        btn.setAttribute('aria-label', muted ? 'Unmute audio' : 'Mute audio');
      });

      container.appendChild(btn);
      this.muteButton = btn;
    },

    _updateMuteButton: function () {
      if (!this.muteButton) return;
      this.muteButton.innerHTML = this.isMuted ? '🔇' : '🔊';
      this.muteButton.setAttribute('aria-label', this.isMuted ? 'Unmute audio' : 'Mute audio');
    },

    showMuteButton: function () {
      if (this.muteButton) {
        this.muteButton.style.opacity = '1';
        this.muteButton.style.pointerEvents = 'auto';
      }
    },

    hideMuteButton: function () {
      if (this.muteButton) {
        this.muteButton.style.opacity = '0';
        this.muteButton.style.pointerEvents = 'none';
      }
    },

    // ═════════════════════════════════════════════════════════════════════
    // CLEANUP
    // ═════════════════════════════════════════════════════════════════════

    dispose: function () {
      this.isPlaying = false;
      
      // Stop and dispose oscillators
      [this.primaryOsc, ...this.overtoneOscs].forEach(osc => {
        if (osc) {
          osc.stop();
          osc.dispose();
        }
      });
      
      // Dispose synths
      if (this.clickSynth) this.clickSynth.dispose();
      if (this.popSynth) this.popSynth.dispose();
      if (this.whooshNoise) this.whooshNoise.dispose();
      
      // Remove mute button
      if (this.muteButton && this.muteButton.parentNode) {
        this.muteButton.parentNode.removeChild(this.muteButton);
      }
      
      this.isInitialized = false;
      console.log('[AudioEngine] Disposed');
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // EXPOSE TO WINDOW
  // ═══════════════════════════════════════════════════════════════════════

  window.AudioEngine = AudioEngine;
  window.ScaleAudio = ScaleAudio;

  // Auto-initialize on DOM ready if Tone.js is available
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      if (typeof Tone !== 'undefined') {
        // Wait for first user interaction to start audio (browser policy)
        const initOnInteraction = () => {
          AudioEngine.startOnUserInteraction();
          AudioEngine.createMuteButton();
          document.removeEventListener('click', initOnInteraction);
          document.removeEventListener('keydown', initOnInteraction);
          document.removeEventListener('touchstart', initOnInteraction);
        };
        document.addEventListener('click', initOnInteraction, { once: true });
        document.addEventListener('keydown', initOnInteraction, { once: true });
        document.addEventListener('touchstart', initOnInteraction, { once: true });
      }
    });
  }

})();
