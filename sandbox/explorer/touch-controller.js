/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * TOUCH CONTROLLER — Native Mobile Experience for Propagation Framework Explorer
 * 
 * Pinch-to-zoom, swipe navigation, gyroscope, haptics, thumb-zone layout
 * Makes the web app feel like a native mobile application
 * ═══════════════════════════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════════
  const TouchController = {
    // Gesture settings
    gestures: {
      pinchZoom: { 
        enabled: true, 
        scale: 'log',
        threshold: 0.1,
        sensitivity: 1.5
      },
      swipe: { 
        enabled: true, 
        threshold: 50,
        velocityThreshold: 0.5
      },
      pan: { 
        enabled: true, 
        twoFinger: true,
        friction: 0.9
      },
      tap: { 
        enabled: true, 
        doubleTapZoom: true,
        tapDelay: 300,
        doubleTapDelay: 300
      }
    },
    
    // Haptic feedback patterns
    haptics: {
      scaleTransition: { 
        type: 'light', 
        duration: 10,
        pattern: [10]
      },
      buttonPress: { 
        type: 'medium', 
        duration: 20,
        pattern: [20]
      },
      boundary: { 
        type: 'heavy', 
        duration: 30,
        pattern: [30, 50, 30]
      },
      completion: {
        type: 'success',
        duration: 100,
        pattern: [20, 30, 20, 30, 50]
      },
      error: {
        type: 'error',
        duration: 50,
        pattern: [50, 30, 50]
      }
    },
    
    // Device orientation settings
    deviceOrientation: {
      enabled: true,
      sensitivity: 0.5,
      deadzone: 5, // degrees
      smoothing: 0.15,
      maxTilt: 45
    },

    // Mobile scene adjustments per scale
    mobileAdjustments: {
      human: { cameraDistance: 0.7, particleCount: 0.5, fov: 60 },
      cellular: { cameraDistance: 0.8, particleCount: 0.6, fov: 55 },
      molecular: { cameraDistance: 0.75, particleCount: 0.5, fov: 55 },
      atomic: { cameraDistance: 0.8, particleCount: 0.4, fov: 50 },
      subatomic: { cameraDistance: 0.85, particleCount: 0.3, fov: 50 },
      planck: { cameraDistance: 0.9, particleCount: 0.25, fov: 45 },
      planetary: { cameraDistance: 0.7, particleCount: 0.5, fov: 60 },
      stellar: { cameraDistance: 0.75, particleCount: 0.6, fov: 55 },
      galactic: { cameraDistance: 0.8, particleCount: 0.5, fov: 55 },
      cosmic: { cameraDistance: 0.85, particleCount: 0.4, fov: 50 }
    },

    // State tracking
    state: {
      isTouch: false,
      isPinching: false,
      isSwiping: false,
      isPanning: false,
      touchCount: 0,
      lastScale: 1,
      initialPinchDistance: 0,
      currentScaleIndex: 0,
      orientationEnabled: false,
      orientationAlpha: 0,
      orientationBeta: 0,
      orientationGamma: 0,
      smoothedAlpha: 0,
      smoothedBeta: 0,
      smoothedGamma: 0,
      touchStartTime: 0,
      lastTapTime: 0,
      hasTriggeredHaptic: false,
      scalesVisited: new Set(),
      allScalesSeen: false
    },

    // Scale definitions for pinch navigation
    scales: [
      { id: 'human', name: 'Human Scale', exponent: 0, size: '10⁰ m' },
      { id: 'cellular', name: 'Cellular', exponent: -5, size: '10⁻⁵ m' },
      { id: 'molecular', name: 'Molecular', exponent: -9, size: '10⁻⁹ m' },
      { id: 'atomic', name: 'Atomic', exponent: -10, size: '10⁻¹⁰ m' },
      { id: 'subatomic', name: 'Subatomic', exponent: -15, size: '10⁻¹⁵ m' },
      { id: 'planck', name: 'Planck', exponent: -35, size: '10⁻³⁵ m' },
      { id: 'planetary', name: 'Planetary', exponent: 7, size: '10⁷ m' },
      { id: 'stellar', name: 'Stellar', exponent: 9, size: '10⁹ m' },
      { id: 'galactic', name: 'Galactic', exponent: 21, size: '10²¹ m' },
      { id: 'cosmic', name: 'Cosmic', exponent: 26, size: '10²⁶ m' }
    ]
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // UTILITY FUNCTIONS
  // ═══════════════════════════════════════════════════════════════════════════
  
  const Utils = {
    // Detect touch device
    isTouchDevice: () => {
      return (('ontouchstart' in window) || 
              (navigator.maxTouchPoints > 1) ||
              (window.matchMedia('(pointer: coarse)').matches));
    },

    // Detect iOS
    isIOS: () => {
      return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    },

    // Detect Android
    isAndroid: () => {
      return /Android/.test(navigator.userAgent);
    },

    // Clamp value between min and max
    clamp: (value, min, max) => Math.min(max, Math.max(min, value)),

    // Linear interpolation
    lerp: (start, end, t) => start + (end - start) * t,

    // Get distance between two touch points
    getTouchDistance: (touch1, touch2) => {
      const dx = touch2.clientX - touch1.clientX;
      const dy = touch2.clientY - touch1.clientY;
      return Math.sqrt(dx * dx + dy * dy);
    },

    // Get center point between two touches
    getTouchCenter: (touch1, touch2) => ({
      x: (touch1.clientX + touch2.clientX) / 2,
      y: (touch1.clientY + touch2.clientY) / 2
    }),

    // Throttle function execution
    throttle: (func, limit) => {
      let inThrottle;
      return function(...args) {
        if (!inThrottle) {
          func.apply(this, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    },

    // Debounce function execution
    debounce: (func, wait) => {
      let timeout;
      return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
      };
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // HAPTIC FEEDBACK SYSTEM
  // ═══════════════════════════════════════════════════════════════════════════
  
  const Haptics = {
    // Check if vibration is supported
    isSupported: () => {
      return 'vibrate' in navigator;
    },

    // Trigger haptic feedback
    trigger: (type) => {
      if (!Haptics.isSupported()) return false;
      
      const pattern = TouchController.haptics[type];
      if (!pattern) return false;

      try {
        // Use pattern if available, otherwise fall back to duration
        if (pattern.pattern && Array.isArray(pattern.pattern)) {
          navigator.vibrate(pattern.pattern);
        } else {
          navigator.vibrate(pattern.duration);
        }
        return true;
      } catch (e) {
        console.warn('Haptic feedback failed:', e);
        return false;
      }
    },

    // Scale transition haptic
    scaleTransition: () => Haptics.trigger('scaleTransition'),

    // Button press haptic
    buttonPress: () => Haptics.trigger('buttonPress'),

    // Boundary haptic (can't go further)
    boundary: () => Haptics.trigger('boundary'),

    // Completion haptic (all scales seen)
    completion: () => Haptics.trigger('completion'),

    // Error haptic
    error: () => Haptics.trigger('error')
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // VISUAL FEEDBACK SYSTEM
  // ═══════════════════════════════════════════════════════════════════════════
  
  const VisualFeedback = {
    // Create ripple effect on touch
    createRipple: (x, y, container = document.body) => {
      const ripple = document.createElement('div');
      ripple.className = 'touch-ripple';
      ripple.style.cssText = `
        position: fixed;
        left: ${x - 25}px;
        top: ${y - 25}px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 229, 255, 0.4) 0%, transparent 70%);
        pointer-events: none;
        z-index: 9999;
        transform: scale(0);
        animation: touchRipple 0.6s ease-out forwards;
      `;
      container.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    },

    // Show scale indicator during pinch
    showScaleIndicator: (scaleName, scaleSize) => {
      let indicator = document.getElementById('touchScaleIndicator');
      if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'touchScaleIndicator';
        indicator.className = 'touch-scale-indicator';
        document.body.appendChild(indicator);
      }

      indicator.innerHTML = `
        <div class="scale-name">${scaleName}</div>
        <div class="scale-size">${scaleSize}</div>
      `;
      indicator.classList.add('visible');

      // Hide after delay
      clearTimeout(indicator.hideTimeout);
      indicator.hideTimeout = setTimeout(() => {
        indicator.classList.remove('visible');
      }, 1500);
    },

    // Show gesture hint
    showGestureHint: (gesture) => {
      const hints = {
        pinch: 'Pinch to zoom between scales',
        swipe: 'Swipe to navigate',
        pan: 'Two-finger drag to pan',
        doubleTap: 'Double-tap to zoom in',
        gyro: 'Tilt device to look around'
      };

      let hint = document.getElementById('touchGestureHint');
      if (!hint) {
        hint = document.createElement('div');
        hint.id = 'touchGestureHint';
        hint.className = 'touch-gesture-hint';
        document.body.appendChild(hint);
      }

      hint.textContent = hints[gesture] || gesture;
      hint.classList.add('visible');

      clearTimeout(hint.hideTimeout);
      hint.hideTimeout = setTimeout(() => {
        hint.classList.remove('visible');
      }, 2000);
    },

    // Show thumb zone overlay (for first-time users)
    showThumbZones: () => {
      if (localStorage.getItem('pf_thumbzones_shown')) return;

      const toast = document.createElement('div');
      toast.className = 'premium-toast';
      toast.innerHTML = `
        <div class="toast-content">
          <span class="toast-icon">✨</span>
          <p>Optimized for touch controls</p>
        </div>
        <button class="toast-dismiss">Got it</button>
      `;
      document.body.appendChild(toast);

      toast.querySelector('.toast-dismiss').addEventListener('click', () => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
        localStorage.setItem('pf_thumbzones_shown', '1');
      });

      setTimeout(() => {
        if (document.body.contains(toast)) {
          toast.classList.add('hiding');
          setTimeout(() => toast.remove(), 300);
          localStorage.setItem('pf_thumbzones_shown', '1');
        }
      }, 5000);
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // GESTURE HANDLERS
  // ═══════════════════════════════════════════════════════════════════════════
  
  const GestureHandlers = {
    // Touch tracking
    touches: new Map(),
    gestureStartTime: 0,
    startDistance: 0,
    startScale: 1,
    currentScale: 1,

    // Initialize gesture handling
    init: () => {
      const overlay = document.getElementById('zoomSequenceOverlay');
      const stage = document.getElementById('zsStage');
      const target = stage || overlay || document.body;

      // Touch start
      target.addEventListener('touchstart', GestureHandlers.onTouchStart, { passive: true });
      
      // Touch move
      target.addEventListener('touchmove', GestureHandlers.onTouchMove, { passive: false });
      
      // Touch end
      target.addEventListener('touchend', GestureHandlers.onTouchEnd, { passive: true });
      target.addEventListener('touchcancel', GestureHandlers.onTouchEnd, { passive: true });

      // Prevent default touch behaviors that interfere
      document.addEventListener('touchmove', (e) => {
        if (TouchController.state.isPinching || TouchController.state.isPanning) {
          e.preventDefault();
        }
      }, { passive: false });
    },

    onTouchStart: (e) => {
      TouchController.state.touchStartTime = Date.now();
      TouchController.state.touchCount = e.touches.length;

      // Track all touches
      for (let i = 0; i < e.touches.length; i++) {
        const touch = e.touches[i];
        GestureHandlers.touches.set(touch.identifier, {
          startX: touch.clientX,
          startY: touch.clientY,
          currentX: touch.clientX,
          currentY: touch.clientY,
          startTime: Date.now()
        });
      }

      // Pinch start (two fingers)
      if (e.touches.length === 2 && TouchController.gestures.pinchZoom.enabled) {
        TouchController.state.isPinching = true;
        GestureHandlers.startDistance = Utils.getTouchDistance(e.touches[0], e.touches[1]);
        GestureHandlers.startScale = TouchController.state.lastScale;
        GestureHandlers.gestureStartTime = Date.now();
        
        // Prevent page zoom
        e.preventDefault();
      }

      // Pan start (two fingers, different from pinch)
      if (e.touches.length === 2 && TouchController.gestures.pan.enabled && TouchController.gestures.pan.twoFinger) {
        const center = Utils.getTouchCenter(e.touches[0], e.touches[1]);
        GestureHandlers.panStartX = center.x;
        GestureHandlers.panStartY = center.y;
      }

      // Single touch for swipe detection
      if (e.touches.length === 1) {
        GestureHandlers.swipeStartX = e.touches[0].clientX;
        GestureHandlers.swipeStartY = e.touches[0].clientY;
      }
    },

    onTouchMove: (e) => {
      // Update touch positions
      for (let i = 0; i < e.touches.length; i++) {
        const touch = e.touches[i];
        const tracked = GestureHandlers.touches.get(touch.identifier);
        if (tracked) {
          tracked.currentX = touch.clientX;
          tracked.currentY = touch.clientY;
        }
      }

      // Handle pinch zoom
      if (TouchController.state.isPinching && e.touches.length === 2) {
        e.preventDefault();
        
        const currentDistance = Utils.getTouchDistance(e.touches[0], e.touches[1]);
        const scaleRatio = currentDistance / GestureHandlers.startDistance;
        GestureHandlers.currentScale = GestureHandlers.startScale * scaleRatio;

        // Map scale to scale index
        const scaleDelta = Math.log2(scaleRatio) * TouchController.gestures.pinchZoom.sensitivity;
        const newScaleIndex = Utils.clamp(
          TouchController.state.currentScaleIndex + Math.round(scaleDelta),
          0,
          TouchController.scales.length - 1
        );

        // Show scale indicator during pinch
        const targetScale = TouchController.scales[newScaleIndex];
        if (targetScale) {
          VisualFeedback.showScaleIndicator(targetScale.name, targetScale.size);
        }
      }

      // Handle two-finger pan
      if (e.touches.length === 2 && TouchController.state.isPanning) {
        const center = Utils.getTouchCenter(e.touches[0], e.touches[1]);
        const deltaX = center.x - GestureHandlers.panStartX;
        const deltaY = center.y - GestureHandlers.panStartY;
        
        // Apply pan to camera/viewer if available
        if (window.PFExplorer && window.PFExplorer.applyPan) {
          window.PFExplorer.applyPan(deltaX * 0.01, deltaY * 0.01);
        }
      }
    },

    onTouchEnd: (e) => {
      const touchDuration = Date.now() - TouchController.state.touchStartTime;
      
      // Clean up ended touches
      for (let i = 0; i < e.changedTouches.length; i++) {
        GestureHandlers.touches.delete(e.changedTouches[i].identifier);
      }

      // Handle pinch end
      if (TouchController.state.isPinching && e.touches.length < 2) {
        TouchController.state.isPinching = false;
        
        const currentDistance = GestureHandlers.startDistance * (GestureHandlers.currentScale / GestureHandlers.startScale);
        const scaleRatio = currentDistance / GestureHandlers.startDistance;
        const scaleDelta = Math.log2(scaleRatio) * TouchController.gestures.pinchZoom.sensitivity;
        
        // Apply scale change if significant
        if (Math.abs(scaleDelta) >= TouchController.gestures.pinchZoom.threshold / 100) {
          const direction = scaleDelta > 0 ? -1 : 1; // Pinch in = zoom in (smaller scales)
          GestureHandlers.changeScale(direction);
        }

        TouchController.state.lastScale = 1;
        GestureHandlers.currentScale = 1;
      }

      // Detect swipe
      if (e.changedTouches.length === 1 && TouchController.gestures.swipe.enabled) {
        const touch = e.changedTouches[0];
        const tracked = GestureHandlers.touches.get(touch.identifier);
        
        if (tracked) {
          const deltaX = touch.clientX - tracked.startX;
          const deltaY = touch.clientY - tracked.startY;
          const velocity = Math.sqrt(deltaX * deltaX + deltaY * deltaY) / touchDuration;

          // Check if swipe meets threshold
          if (Math.abs(deltaY) > TouchController.gestures.swipe.threshold && 
              Math.abs(deltaY) > Math.abs(deltaX)) {
            // Vertical swipe - change scale
            const direction = deltaY < 0 ? 1 : -1; // Swipe up = zoom out (larger scales)
            GestureHandlers.changeScale(direction);
            Haptics.scaleTransition();
          } else if (Math.abs(deltaX) > TouchController.gestures.swipe.threshold && 
                     velocity > TouchController.gestures.swipe.velocityThreshold) {
            // Horizontal swipe - could navigate derivation nodes
            GestureHandlers.handleHorizontalSwipe(deltaX > 0 ? 'right' : 'left');
          }
        }
      }

      // Detect tap/double-tap
      if (e.changedTouches.length === 1 && touchDuration < TouchController.gestures.tap.tapDelay) {
        const now = Date.now();
        const timeSinceLastTap = now - TouchController.state.lastTapTime;
        
        if (timeSinceLastTap < TouchController.gestures.tap.doubleTapDelay && 
            TouchController.gestures.tap.doubleTapZoom) {
          // Double tap - zoom in
          GestureHandlers.changeScale(-1);
          Haptics.buttonPress();
        }
        
        TouchController.state.lastTapTime = now;
      }

      // Reset state
      if (e.touches.length === 0) {
        TouchController.state.isPanning = false;
        TouchController.state.touchCount = 0;
      }
    },

    // Change scale level
    changeScale: (direction) => {
      const newIndex = Utils.clamp(
        TouchController.state.currentScaleIndex + direction,
        0,
        TouchController.scales.length - 1
      );

      if (newIndex !== TouchController.state.currentScaleIndex) {
        TouchController.state.currentScaleIndex = newIndex;
        const scale = TouchController.scales[newIndex];
        
        // Track visited scales
        TouchController.state.scalesVisited.add(scale.id);
        
        // Check if all scales seen
        if (TouchController.state.scalesVisited.size >= TouchController.scales.length && 
            !TouchController.state.allScalesSeen) {
          TouchController.state.allScalesSeen = true;
          Haptics.completion();
          VisualFeedback.showGestureHint('All scales explored!');
        } else {
          Haptics.scaleTransition();
        }

        // Visual feedback
        VisualFeedback.showScaleIndicator(scale.name, scale.size);

        // Trigger zoom sequence advance if overlay is active
        const overlay = document.getElementById('zoomSequenceOverlay');
        if (overlay && overlay.style.display !== 'none') {
          // Simulate click to advance zoom sequence
          const event = new Event('click');
          overlay.dispatchEvent(event);
        }

        // Apply mobile adjustments
        GestureHandlers.applyMobileAdjustments(scale.id);
      } else {
        // At boundary
        Haptics.boundary();
      }
    },

    // Handle horizontal swipe
    handleHorizontalSwipe: (direction) => {
      // Navigate derivation nodes or panels
      if (window.PFExplorer && window.PFExplorer.navigate) {
        const routes = ['hub', 'foundations', 'refraction', 'generations', 'koide', 
                       'weinberg', 'koide-weinberg-bridge', 'god-equation', 'bohr'];
        const currentRoute = window.PFExplorer.state.route;
        const currentIndex = routes.indexOf(currentRoute);
        
        if (currentIndex !== -1) {
          const newIndex = direction === 'left' 
            ? Math.min(currentIndex + 1, routes.length - 1)
            : Math.max(currentIndex - 1, 0);
          
          if (newIndex !== currentIndex) {
            window.PFExplorer.navigate(routes[newIndex]);
          }
        }
      }
    },

    // Apply mobile scene adjustments
    applyMobileAdjustments: (scaleId) => {
      const adjustments = TouchController.mobileAdjustments[scaleId];
      if (!adjustments || !window.THREE) return;

      // Find and adjust Three.js camera if exists
      const canvases = document.querySelectorAll('canvas');
      canvases.forEach(canvas => {
        if (canvas.__threejs_camera) {
          const camera = canvas.__threejs_camera;
          if (adjustments.fov) {
            camera.fov = adjustments.fov;
            camera.updateProjectionMatrix();
          }
        }
      });

      // Dispatch event for panels to handle
      window.dispatchEvent(new CustomEvent('mobileScaleChange', {
        detail: { scale: scaleId, adjustments }
      }));
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // DEVICE ORIENTATION HANDLER
  // ═══════════════════════════════════════════════════════════════════════════
  
  const OrientationHandler = {
    init: () => {
      if (!window.DeviceOrientationEvent) {
        console.log('Device orientation not supported');
        return;
      }

      // Request permission on iOS 13+
      if (typeof DeviceOrientationEvent.requestPermission === 'function') {
        // Create toggle button for orientation
        OrientationHandler.createToggleButton();
      } else {
        // Auto-enable on non-iOS devices
        OrientationHandler.enable();
      }

      window.addEventListener('deviceorientation', OrientationHandler.onOrientationChange);
    },

    createToggleButton: () => {
      const container = document.createElement('div');
      container.className = 'orientation-toggle-container';
      container.innerHTML = `
        <button id="orientationToggle" class="orientation-toggle" aria-label="Enable gyroscope">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
          </svg>
          <span>Gyroscope</span>
        </button>
      `;
      document.body.appendChild(container);

      const btn = document.getElementById('orientationToggle');
      btn.addEventListener('click', async () => {
        try {
          const permission = await DeviceOrientationEvent.requestPermission();
          if (permission === 'granted') {
            OrientationHandler.enable();
            btn.classList.add('active');
            btn.querySelector('span').textContent = 'Gyro On';
            Haptics.buttonPress();
          }
        } catch (e) {
          console.error('Orientation permission denied:', e);
        }
      });
    },

    enable: () => {
      TouchController.state.orientationEnabled = true;
      document.body.classList.add('orientation-enabled');
    },

    disable: () => {
      TouchController.state.orientationEnabled = false;
      document.body.classList.remove('orientation-enabled');
    },

    onOrientationChange: (e) => {
      if (!TouchController.state.orientationEnabled) return;
      if (!e.alpha && !e.beta && !e.gamma) return;

      const { sensitivity, deadzone, smoothing } = TouchController.deviceOrientation;

      // Store raw values
      TouchController.state.orientationAlpha = e.alpha || 0;
      TouchController.state.orientationBeta = e.beta || 0;
      TouchController.state.orientationGamma = e.gamma || 0;

      // Apply deadzone
      const applyDeadzone = (value) => {
        if (Math.abs(value) < deadzone) return 0;
        return value > 0 ? value - deadzone : value + deadzone;
      };

      const beta = applyDeadzone(TouchController.state.orientationBeta);
      const gamma = applyDeadzone(TouchController.state.orientationGamma);

      // Smooth values
      TouchController.state.smoothedBeta = Utils.lerp(
        TouchController.state.smoothedBeta, 
        beta, 
        smoothing
      );
      TouchController.state.smoothedGamma = Utils.lerp(
        TouchController.state.smoothedGamma, 
        gamma, 
        smoothing
      );

      // Apply to Three.js camera if available
      if (window.PFExplorer && window.PFExplorer.applyOrientation) {
        window.PFExplorer.applyOrientation(
          TouchController.state.smoothedBeta * sensitivity * 0.01,
          TouchController.state.smoothedGamma * sensitivity * 0.01
        );
      }

      // Dispatch custom event
      window.dispatchEvent(new CustomEvent('deviceorientationchange', {
        detail: {
          alpha: TouchController.state.orientationAlpha,
          beta: TouchController.state.smoothedBeta,
          gamma: TouchController.state.smoothedGamma
        }
      }));
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // LONG PRESS / CONTEXT MENU
  // ═══════════════════════════════════════════════════════════════════════════
  
  const LongPressHandler = {
    longPressDelay: 500,
    longPressTimer: null,

    init: () => {
      document.addEventListener('touchstart', LongPressHandler.onTouchStart, { passive: true });
      document.addEventListener('touchend', LongPressHandler.onTouchEnd, { passive: true });
      document.addEventListener('touchmove', LongPressHandler.onTouchMove, { passive: true });
    },

    onTouchStart: (e) => {
      // Only on result cards and interactive elements
      const target = e.target.closest('[data-result-id], .result-card, .scale-card');
      if (!target) return;

      LongPressHandler.longPressTimer = setTimeout(() => {
        LongPressHandler.showContextMenu(e, target);
        Haptics.buttonPress();
      }, LongPressHandler.longPressDelay);
    },

    onTouchEnd: () => {
      if (LongPressHandler.longPressTimer) {
        clearTimeout(LongPressHandler.longPressTimer);
        LongPressHandler.longPressTimer = null;
      }
    },

    onTouchMove: () => {
      if (LongPressHandler.longPressTimer) {
        clearTimeout(LongPressHandler.longPressTimer);
        LongPressHandler.longPressTimer = null;
      }
    },

    showContextMenu: (e, target) => {
      // Prevent default context menu
      e.preventDefault();

      const resultId = target.dataset.resultId;
      const existingMenu = document.querySelector('.touch-context-menu');
      if (existingMenu) existingMenu.remove();

      const menu = document.createElement('div');
      menu.className = 'touch-context-menu';
      menu.style.cssText = `
        position: fixed;
        left: ${e.touches[0].clientX}px;
        top: ${e.touches[0].clientY}px;
        transform: translate(-50%, -100%);
        z-index: 10000;
      `;

      menu.innerHTML = `
        <div class="context-menu-item" data-action="details">View Details</div>
        <div class="context-menu-item" data-action="share">Share</div>
        <div class="context-menu-item" data-action="evidence">Show Evidence</div>
      `;

      document.body.appendChild(menu);

      // Handle menu item clicks
      menu.addEventListener('click', (clickE) => {
        const action = clickE.target.dataset.action;
        if (action === 'details' && resultId) {
          if (window.PFExplorer) {
            window.PFExplorer.focusResult(resultId, { open: true });
          }
        } else if (action === 'evidence') {
          if (window.PFExplorer) {
            window.PFExplorer.toggleDrawer(true);
          }
        }
        menu.remove();
      });

      // Remove on outside click
      setTimeout(() => {
        document.addEventListener('click', function removeMenu() {
          menu.remove();
          document.removeEventListener('click', removeMenu);
        });
      }, 10);
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // BOTTOM SHEET FOR DETAILS
  // ═══════════════════════════════════════════════════════════════════════════
  
  const BottomSheet = {
    init: () => {
      // Convert drawer to bottom sheet on mobile
      if (window.matchMedia('(max-width: 768px)').matches) {
        BottomSheet.setup();
      }

      // Listen for resize
      window.addEventListener('resize', Utils.debounce(() => {
        if (window.matchMedia('(max-width: 768px)').matches) {
          BottomSheet.setup();
        } else {
          BottomSheet.teardown();
        }
      }, 250));
    },

    setup: () => {
      const drawer = document.getElementById('appDrawer');
      if (!drawer || drawer.classList.contains('bottom-sheet')) return;

      drawer.classList.add('bottom-sheet');
      
      // Add drag handle
      const handle = document.createElement('div');
      handle.className = 'bottom-sheet-handle';
      handle.innerHTML = '<div class="handle-bar"></div>';
      drawer.insertBefore(handle, drawer.firstChild);

      // Add swipe to dismiss
      let startY = 0;
      let currentY = 0;

      handle.addEventListener('touchstart', (e) => {
        startY = e.touches[0].clientY;
        drawer.classList.add('dragging');
      }, { passive: true });

      handle.addEventListener('touchmove', (e) => {
        currentY = e.touches[0].clientY;
        const delta = currentY - startY;
        if (delta > 0) {
          drawer.style.transform = `translateY(${delta}px)`;
        }
      }, { passive: true });

      handle.addEventListener('touchend', () => {
        drawer.classList.remove('dragging');
        const delta = currentY - startY;
        
        if (delta > 100) {
          // Close sheet
          if (window.PFExplorer) {
            window.PFExplorer.toggleDrawer(false);
          }
        } else {
          // Snap back
          drawer.style.transform = '';
        }
        
        drawer.style.transform = '';
      }, { passive: true });
    },

    teardown: () => {
      const drawer = document.getElementById('appDrawer');
      if (!drawer) return;

      drawer.classList.remove('bottom-sheet');
      const handle = drawer.querySelector('.bottom-sheet-handle');
      if (handle) handle.remove();
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // MAIN INITIALIZATION
  // ═══════════════════════════════════════════════════════════════════════════
  
  const TouchControllerMain = {
    init: () => {
      // Only initialize on touch devices
      if (!Utils.isTouchDevice()) {
        document.body.classList.add('no-touch');
        return;
      }

      document.body.classList.add('touch-device');
      TouchController.state.isTouch = true;

      // Initialize all modules
      GestureHandlers.init();
      OrientationHandler.init();
      LongPressHandler.init();
      BottomSheet.init();

      // Add button haptics
      TouchControllerMain.addButtonHaptics();

      // Show thumb zones hint for first-time users
      if (!localStorage.getItem('pf_thumbzones_shown')) {
        setTimeout(() => {
          VisualFeedback.showThumbZones();
        }, 2000);
      }

      // Expose API globally
      window.TouchController = TouchController;
      window.TouchHaptics = Haptics;
      window.TouchVisualFeedback = VisualFeedback;

      console.log('Touch Controller initialized');
    },

    addButtonHaptics: () => {
      const buttons = document.querySelectorAll('button, .btn, .route-button, .chip-button');
      
      buttons.forEach(btn => {
        btn.addEventListener('touchstart', () => {
          Haptics.buttonPress();
          VisualFeedback.createRipple(
            btn.getBoundingClientRect().left + btn.offsetWidth / 2,
            btn.getBoundingClientRect().top + btn.offsetHeight / 2
          );
        }, { passive: true });
      });
    }
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', TouchControllerMain.init);
  } else {
    TouchControllerMain.init();
  }

  // Expose configuration for external access
  window.TouchControllerConfig = TouchController;

})();
