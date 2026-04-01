// Dirac Belt Trick Visualization
// CSS 3D Implementation of π₁(SO(3)) = ℤ₂
(function() {
  'use strict';

  // State
  let currentRotation = 0;
  let targetRotation = 0;
  let animationSpeed = 1;
  let isAnimating = false;
  let loopClass = 'trivial';
  let animationFrame = null;

  // DOM Elements
  const belt = document.getElementById('belt');
  const rotationObject = document.getElementById('rotationObject');
  const rotationSlider = document.getElementById('rotationSlider');
  const rotationValue = document.getElementById('rotationValue');
  const speedSlider = document.getElementById('speedSlider');
  const speedValue = document.getElementById('speedValue');
  const playBtn = document.getElementById('playBtn');
  const resetBtn = document.getElementById('resetBtn');
  const rotate360 = document.getElementById('rotate360');
  const rotate720 = document.getElementById('rotate720');
  const statusIndicator = document.getElementById('statusIndicator');
  const statusText = statusIndicator.querySelector('.status-text');

  // Initialize
  function init() {
    setupEventListeners();
    updateDisplay();
  }

  // Setup event listeners
  function setupEventListeners() {
    // Rotation slider
    rotationSlider.addEventListener('input', (e) => {
      targetRotation = parseInt(e.target.value);
      updateRotation();
      updateDisplay();
    });

    // Speed slider
    speedSlider.addEventListener('input', (e) => {
      animationSpeed = parseFloat(e.target.value);
      speedValue.textContent = animationSpeed.toFixed(1) + 'x';
    });

    // Control buttons
    playBtn.addEventListener('click', toggleAnimation);
    resetBtn.addEventListener('click', resetRotation);
    rotate360.addEventListener('click', () => rotateTo(360));
    rotate720.addEventListener('click', () => rotateTo(720));

    // Loop class selector
    document.querySelectorAll('input[name="loopClass"]').forEach(radio => {
      radio.addEventListener('change', (e) => {
        loopClass = e.target.value;
        updateStatus();
      });
    });

    // Back button
    document.getElementById('backBtn').addEventListener('click', () => {
      window.location.href = 'index.html';
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      switch(e.key) {
        case ' ':
          e.preventDefault();
          toggleAnimation();
          break;
        case 'r':
        case 'R':
          resetRotation();
          break;
        case '1':
          rotateTo(360);
          break;
        case '2':
          rotateTo(720);
          break;
      }
    });
  }

  // Update rotation display
  function updateRotation() {
    const rotation = currentRotation % 720;
    const beltRotation = rotation;
    const objectRotation = rotation;

    // Apply rotations
    if (belt) {
      belt.style.transform = `rotateY(${beltRotation}deg)`;
    }
    
    if (rotationObject) {
      rotationObject.style.transform = `translateX(-50%) rotateY(${objectRotation}deg)`;
    }

    // Update belt twist visualization
    updateBeltTwist(rotation);
  }

  // Update belt twist based on rotation
  function updateBeltTwist(rotation) {
    const segments = belt.querySelectorAll('.belt-segment');
    const twistAmount = (rotation / 720) * 360; // Full twist at 720°
    
    segments.forEach((segment, index) => {
      const segmentPosition = index / segments.length;
      const localTwist = twistAmount * segmentPosition;
      
      // Add 3D twist effect with more dramatic transforms
      const twistX = Math.sin(localTwist * Math.PI / 180) * 30;
      const twistZ = Math.cos(localTwist * Math.PI / 180) * 20;
      const rotateY = localTwist;
      
      segment.style.transform = `
        rotateY(${rotateY}deg) 
        translateX(${twistX}px) 
        translateZ(${twistZ}px)
        rotateX(${Math.sin(localTwist * Math.PI / 90) * 15}deg)
      `;
      
      // Dynamic color based on twist intensity
      const intensity = Math.abs(Math.sin(localTwist * Math.PI / 180));
      const hue = 180 + intensity * 60; // Cyan to green
      const lightness = 50 + intensity * 20;
      
      segment.style.background = `linear-gradient(135deg, 
        hsl(${hue}, 70%, ${lightness}%) 0%, 
        hsl(${hue + 30}, 80%, ${lightness + 10}%) 50%, 
        hsl(${hue}, 70%, ${lightness}%) 100%)`;
      
      // Glow effect for twisted segments
      const beforeElement = segment.querySelector('::before') || segment;
      if (intensity > 0.5) {
        segment.style.boxShadow = `
          0 0 ${20 * intensity}px hsla(${hue}, 100%, 50%, ${intensity * 0.5}),
          inset 0 0 ${10 * intensity}px hsla(${hue}, 100%, 50%, ${intensity * 0.3})
        `;
      }
      
      // Add visual markers to show twist
      if (index % 2 === 0) {
        const marker = segment.querySelector('.twist-marker') || 
          (() => {
            const m = document.createElement('div');
            m.className = 'twist-marker';
            m.style.cssText = `
              position: absolute;
              top: 50%;
              left: 50%;
              width: 20px;
              height: 20px;
              margin: -10px 0 0 -10px;
              border: 2px solid #fff;
              border-radius: 50%;
              opacity: 0.8;
            `;
            segment.appendChild(m);
            return m;
          })();
        
        marker.style.transform = `rotate(${localTwist * 2}deg) scale(${1 + intensity * 0.5})`;
        marker.style.borderColor = `hsl(${hue}, 100%, ${70 + intensity * 30}%)`;
      }
    });
    
    // Add overall belt glow when twisted
    if (Math.abs(twistAmount) > 180) {
      belt.style.boxShadow = `0 0 40px hsla(${180 + Math.abs(twistAmount) / 4}, 100%, 50%, 0.5)`;
    } else {
      belt.style.boxShadow = 'none';
    }
  }

  // Animate rotation
  function animate() {
    if (!isAnimating) return;

    const diff = targetRotation - currentRotation;
    
    // Handle wrap-around for smooth animation
    let adjustedDiff = diff;
    if (Math.abs(diff) > 360) {
      if (diff > 0) {
        adjustedDiff = diff - 720;
      } else {
        adjustedDiff = diff + 720;
      }
    }

    // Apply easing
    const step = adjustedDiff * 0.1 * animationSpeed;
    currentRotation += step;

    // Check if animation is complete
    if (Math.abs(step) < 0.1) {
      currentRotation = targetRotation;
      isAnimating = false;
      playBtn.innerHTML = '<span class="icon">▶</span>';
      updateStatus();
    }

    updateRotation();
    updateDisplay();

    if (isAnimating) {
      animationFrame = requestAnimationFrame(animate);
    }
  }

  // Toggle animation
  function toggleAnimation() {
    if (isAnimating) {
      isAnimating = false;
      playBtn.innerHTML = '<span class="icon">▶</span>';
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
    } else {
      isAnimating = true;
      playBtn.innerHTML = '<span class="icon">⏸</span>';
      animate();
    }
  }

  // Rotate to specific angle
  function rotateTo(angle) {
    targetRotation = angle;
    rotationSlider.value = angle;
    
    if (!isAnimating) {
      isAnimating = true;
      playBtn.innerHTML = '<span class="icon">⏸</span>';
      animate();
    }
    
    updateStatus();
  }

  // Reset rotation
  function resetRotation() {
    targetRotation = 0;
    rotationSlider.value = 0;
    currentRotation = 0;
    isAnimating = false;
    playBtn.innerHTML = '<span class="icon">▶</span>';
    
    if (animationFrame) {
      cancelAnimationFrame(animationFrame);
    }
    
    updateRotation();
    updateDisplay();
    updateStatus();
  }

  // Update display values
  function updateDisplay() {
    rotationValue.textContent = Math.round(currentRotation) + '°';
  }

  // Update status indicator
  function updateStatus() {
    const rotation = Math.round(currentRotation) % 720;
    let status = '';
    let statusClass = '';
    
    if (rotation === 0) {
      status = 'Identity state - No rotation applied';
      statusClass = 'identity';
    } else if (rotation === 360) {
      status = 'Non-trivial state - Belt is twisted! Need another 360° to untwist';
      statusClass = 'twisted';
    } else if (rotation === 720) {
      status = 'Identity restored - Belt untwisted after 720° rotation';
      statusClass = 'restored';
    } else if (rotation < 360) {
      status = `Rotating... ${rotation}/360°`;
      statusClass = 'rotating';
    } else {
      status = `Rotating... ${rotation - 360}/360° to complete`;
      statusClass = 'completing';
    }
    
    statusText.textContent = status;
    statusIndicator.className = 'status-indicator ' + statusClass;
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
