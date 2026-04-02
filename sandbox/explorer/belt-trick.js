// Dirac Belt Trick — Three.js Ribbon Visualization
// Demonstrates π₁(SO(3)) = ℤ₂: 360° = twisted, 720° = untwisted
(function() {
  'use strict';

  // State
  let scene, camera, renderer, controls, composer;
  let ribbon, ribbonGeometry, ribbonMaterial;
  let rotationObject, rotationGroup;
  let currentAngle = 0;
  let targetAngle = 0;
  let isPlaying = false;
  let animationSpeed = 1;
  let loopClass = 'trivial';
  let clock;

  // Configuration
  const CONFIG = {
    ribbonWidth: 0.8,
    ribbonLength: 6,
    ribbonSegments: 120,
    ribbonWidthSegments: 12,
    rotationSpeed: 0.5,
    bgColor: 0x07111c,
    ribbonColor1: 0x00cfff,
    ribbonColor2: 0x44ff88,
    ribbonEmissive: 0x003344,
    objectColor: 0xffdd55,
    bloomStrength: 0.8,
    bloomRadius: 0.4,
    bloomThreshold: 0.7
  };

  function init() {
    const container = document.getElementById('beltScene');
    if (!container) {
      console.error('Belt scene container not found');
      return;
    }

    clock = new THREE.Clock();

    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(CONFIG.bgColor);
    scene.fog = new THREE.FogExp2(CONFIG.bgColor, 0.04);

    // Camera
    camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 3, 8);
    camera.lookAt(0, 0, 0);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.minDistance = 4;
    controls.maxDistance = 20;
    controls.target.set(0, 0, 0);

    // Post-processing (bloom)
    try {
      composer = new THREE.EffectComposer(renderer);
      const renderPass = new THREE.RenderPass(scene, camera);
      composer.addPass(renderPass);

      const bloomPass = new THREE.UnrealBloomPass(
        new THREE.Vector2(container.clientWidth, container.clientHeight),
        CONFIG.bloomStrength,
        CONFIG.bloomRadius,
        CONFIG.bloomThreshold
      );
      composer.addPass(bloomPass);
    } catch(e) {
      console.log('Bloom not available, using standard renderer');
      composer = null;
    }

    // Lighting
    setupLighting();

    // Ribbon geometry
    createRibbon();

    // Rotation object (cube at end of ribbon)
    createRotationObject();

    // Grid helper (subtle)
    const gridHelper = new THREE.GridHelper(20, 40, 0x111122, 0x0a0a15);
    gridHelper.position.y = -2;
    scene.add(gridHelper);

    // Events
    setupEvents();

    // Start animation loop
    animate();
  }

  function setupLighting() {
    const ambient = new THREE.AmbientLight(0x222244, 0.5);
    scene.add(ambient);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
    dirLight.position.set(5, 8, 5);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    scene.add(dirLight);

    const fillLight = new THREE.PointLight(0x00cfff, 0.6, 20);
    fillLight.position.set(-5, 3, -3);
    scene.add(fillLight);

    const rimLight = new THREE.PointLight(0xffdd55, 0.4, 20);
    rimLight.position.set(3, -2, 5);
    scene.add(rimLight);

    const accentLight = new THREE.PointLight(0x44ff88, 0.3, 15);
    accentLight.position.set(0, 5, -5);
    scene.add(accentLight);
  }

  function createRibbon() {
    ribbonGeometry = new THREE.PlaneGeometry(
      CONFIG.ribbonWidth,
      CONFIG.ribbonLength,
      CONFIG.ribbonWidthSegments,
      CONFIG.ribbonSegments
    );

    ribbonMaterial = new THREE.MeshStandardMaterial({
      color: CONFIG.ribbonColor1,
      emissive: CONFIG.ribbonEmissive,
      metalness: 0.3,
      roughness: 0.6,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.9
    });

    ribbon = new THREE.Mesh(ribbonGeometry, ribbonMaterial);
    ribbon.castShadow = true;
    ribbon.receiveShadow = true;
    ribbon.rotation.x = Math.PI / 2;
    ribbon.position.set(0, 0, -CONFIG.ribbonLength / 2);
    scene.add(ribbon);

    // Edge wireframe for visual clarity
    const edgesGeometry = new THREE.EdgesGeometry(ribbonGeometry);
    const edgesMaterial = new THREE.LineBasicMaterial({
      color: CONFIG.ribbonColor2,
      transparent: true,
      opacity: 0.15
    });
    const edges = new THREE.LineSegments(edgesGeometry, edgesMaterial);
    edges.rotation.x = Math.PI / 2;
    edges.position.copy(ribbon.position);
    scene.add(edges);
  }

  function createRotationObject() {
    rotationGroup = new THREE.Group();

    const cubeGeometry = new THREE.BoxGeometry(0.6, 0.6, 0.6);
    const cubeMaterial = new THREE.MeshStandardMaterial({
      color: CONFIG.objectColor,
      emissive: 0x443300,
      metalness: 0.5,
      roughness: 0.4
    });
    rotationObject = new THREE.Mesh(cubeGeometry, cubeMaterial);
    rotationObject.castShadow = true;
    rotationGroup.add(rotationObject);

    // Visible axes
    const axisLength = 0.5;
    const xAxisGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-axisLength, 0, 0),
      new THREE.Vector3(axisLength, 0, 0)
    ]);
    rotationGroup.add(new THREE.Line(xAxisGeo, new THREE.LineBasicMaterial({ color: 0xff4444 })));

    const yAxisGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, -axisLength, 0),
      new THREE.Vector3(0, axisLength, 0)
    ]);
    rotationGroup.add(new THREE.Line(yAxisGeo, new THREE.LineBasicMaterial({ color: 0x44ff44 })));

    const zAxisGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, -axisLength),
      new THREE.Vector3(0, 0, axisLength)
    ]);
    rotationGroup.add(new THREE.Line(zAxisGeo, new THREE.LineBasicMaterial({ color: 0x4444ff })));

    rotationGroup.position.set(0, 0, -CONFIG.ribbonLength);
    scene.add(rotationGroup);

    // Ring around rotation axis
    const ringGeometry = new THREE.TorusGeometry(0.5, 0.02, 8, 32);
    const ringMaterial = new THREE.MeshStandardMaterial({
      color: 0x00cfff,
      emissive: 0x003344,
      metalness: 0.8,
      roughness: 0.2
    });
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.rotation.x = Math.PI / 2;
    rotationGroup.add(ring);
  }

  function updateRibbonTwist(angle) {
    if (!ribbonGeometry) return;

    const positions = ribbonGeometry.attributes.position;
    const vertexCount = positions.count;

    for (let i = 0; i < vertexCount; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);
      const z = positions.getZ(i);

      // Progress along ribbon length (0 to 1)
      const t = (y + CONFIG.ribbonLength / 2) / CONFIG.ribbonLength;
      
      // Twist angle varies linearly: 0 at fixed end, full angle at rotating end
      const localTwist = angle * t * (Math.PI / 180);

      // Apply twist rotation around Y axis
      const cosT = Math.cos(localTwist);
      const sinT = Math.sin(localTwist);

      positions.setX(i, x * cosT - z * sinT);
      positions.setZ(i, x * sinT + z * cosT);
    }

    positions.needsUpdate = true;
    ribbonGeometry.computeVertexNormals();
  }

  function updateStateDisplay(angle) {
    const angleDisplay = document.getElementById('angleDisplay');
    const stateDisplay = document.getElementById('stateDisplay');
    const statusIndicator = document.getElementById('statusIndicator');

    if (angleDisplay) {
      angleDisplay.textContent = angle.toFixed(1) + '°';
    }

    if (stateDisplay) {
      const stateValue = stateDisplay.querySelector('.state-value');
      const normalizedAngle = angle % 720;
      
      if (Math.abs(normalizedAngle) < 5 || Math.abs(normalizedAngle - 720) < 5) {
        stateValue.textContent = 'Identity';
        stateValue.style.color = '#44ff88';
      } else if (Math.abs(normalizedAngle - 360) < 5) {
        stateValue.textContent = 'Twisted (360°)';
        stateValue.style.color = '#ffaa00';
      } else if (normalizedAngle > 0 && normalizedAngle < 360) {
        stateValue.textContent = 'Twisting...';
        stateValue.style.color = '#ff6b6b';
      } else if (normalizedAngle > 360 && normalizedAngle < 720) {
        stateValue.textContent = 'Untwisting...';
        stateValue.style.color = '#00cfff';
      } else {
        stateValue.textContent = 'Intermediate';
        stateValue.style.color = '#ffaa00';
      }
    }

    if (statusIndicator) {
      const statusText = statusIndicator.querySelector('.status-text');
      const normalizedAngle = angle % 720;
      
      if (Math.abs(normalizedAngle) < 5 || Math.abs(normalizedAngle - 720) < 5) {
        statusText.textContent = '✓ System returned to original configuration';
        statusIndicator.style.borderColor = 'rgba(68, 255, 136, 0.4)';
        statusIndicator.style.background = 'rgba(68, 255, 136, 0.1)';
      } else if (Math.abs(normalizedAngle - 360) < 5) {
        statusText.textContent = '⚠ Twisted state — cannot untwist without further rotation';
        statusIndicator.style.borderColor = 'rgba(255, 170, 0, 0.4)';
        statusIndicator.style.background = 'rgba(255, 170, 0, 0.1)';
      } else {
        statusText.textContent = 'Rotating...';
        statusIndicator.style.borderColor = 'rgba(0, 207, 255, 0.4)';
        statusIndicator.style.background = 'rgba(0, 207, 255, 0.1)';
      }
    }
  }

  function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();

    if (isPlaying || Math.abs(currentAngle - targetAngle) > 0.1) {
      const diff = targetAngle - currentAngle;
      const step = CONFIG.rotationSpeed * animationSpeed * 60 * delta;
      
      if (Math.abs(diff) > step) {
        currentAngle += Math.sign(diff) * step;
      } else {
        currentAngle = targetAngle;
        if (Math.abs(targetAngle % 360) < 1) {
          isPlaying = false;
        }
      }

      updateRibbonTwist(currentAngle);

      if (rotationObject) {
        rotationObject.rotation.y = currentAngle * (Math.PI / 180);
      }
      if (rotationGroup) {
        rotationGroup.rotation.y = currentAngle * (Math.PI / 180);
      }

      updateStateDisplay(currentAngle);
      
      const rotationSlider = document.getElementById('rotationSlider');
      const rotationValue = document.getElementById('rotationValue');
      if (rotationSlider) rotationSlider.value = currentAngle % 720;
      if (rotationValue) rotationValue.textContent = Math.round(currentAngle % 720) + '°';
    }

    controls.update();

    if (composer) {
      composer.render();
    } else {
      renderer.render(scene, camera);
    }
  }

  function setupEvents() {
    window.addEventListener('resize', () => {
      const container = document.getElementById('beltScene');
      if (!container) return;
      
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
      if (composer) {
        composer.setSize(container.clientWidth, container.clientHeight);
      }
    });

    const playBtn = document.getElementById('playBtn');
    const playIcon = document.getElementById('playIcon');
    if (playBtn) {
      playBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (playIcon) {
          playIcon.textContent = isPlaying ? '⏸' : '▶';
        }
        if (isPlaying && targetAngle === currentAngle) {
          targetAngle += 360;
        }
      });
    }

    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        currentAngle = 0;
        targetAngle = 0;
        isPlaying = false;
        updateRibbonTwist(0);
        if (rotationObject) rotationObject.rotation.y = 0;
        if (rotationGroup) rotationGroup.rotation.y = 0;
        updateStateDisplay(0);
        const rotationSlider = document.getElementById('rotationSlider');
        const rotationValue = document.getElementById('rotationValue');
        if (rotationSlider) rotationSlider.value = 0;
        if (rotationValue) rotationValue.textContent = '0°';
        if (playIcon) playIcon.textContent = '▶';
      });
    }

    const rotationSlider = document.getElementById('rotationSlider');
    if (rotationSlider) {
      rotationSlider.addEventListener('input', (e) => {
        targetAngle = parseFloat(e.target.value);
        currentAngle = targetAngle;
        updateRibbonTwist(currentAngle);
        updateStateDisplay(currentAngle);
        const rotationValue = document.getElementById('rotationValue');
        if (rotationValue) rotationValue.textContent = Math.round(currentAngle) + '°';
      });
    }

    const speedSlider = document.getElementById('speedSlider');
    if (speedSlider) {
      speedSlider.addEventListener('input', (e) => {
        animationSpeed = parseFloat(e.target.value);
        const speedValue = document.getElementById('speedValue');
        if (speedValue) speedValue.textContent = animationSpeed.toFixed(1) + 'x';
      });
    }

    const rotate360 = document.getElementById('rotate360');
    if (rotate360) {
      rotate360.addEventListener('click', () => {
        targetAngle += 360;
        isPlaying = true;
        if (playIcon) playIcon.textContent = '⏸';
      });
    }

    const rotate720 = document.getElementById('rotate720');
    if (rotate720) {
      rotate720.addEventListener('click', () => {
        targetAngle += 720;
        isPlaying = true;
        if (playIcon) playIcon.textContent = '⏸';
      });
    }

    document.querySelectorAll('input[name="loopClass"]').forEach(radio => {
      radio.addEventListener('change', (e) => {
        loopClass = e.target.value;
      });
    });

    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        window.location.href = 'index.html';
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === ' ') {
        e.preventDefault();
        if (playBtn) playBtn.click();
      }
      if (e.key === 'r') {
        if (resetBtn) resetBtn.click();
      }
      if (e.key === 'Escape') {
        window.location.href = 'index.html';
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
