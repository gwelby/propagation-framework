// Scale Ladder — Three.js 3D Navigation from Planck to Cosmic
// Visualizes the full propagation scale: 61 orders of magnitude
(function() {
  'use strict';

  // State
  let scene, camera, renderer, controls, composer;
  let scaleNodes = [];
  let labels = [];
  let showLabels = true;
  let clock;

  // Scale data (from data.js)
  const SCALES = [
    { id: 'planck', label: 'Planck', meters: 1.616e-35, color: 0x9b59b6 },
    { id: 'quantum-foam', label: 'Quantum Foam', meters: 1e-33, color: 0x8e44ad },
    { id: 'gut', label: 'GUT', meters: 1e-25, color: 0x7b2cbf },
    { id: 'matter', label: 'Matter', meters: 1.145e-18, color: 0x00cfff },
    { id: 'proton', label: 'Proton', meters: 1e-15, color: 0x00b4d8 },
    { id: 'nuclear', label: 'Nuclear', meters: 9e-16, color: 0x0096c7 },
    { id: 'atomic', label: 'Atomic', meters: 1e-10, color: 0x0077b6 },
    { id: 'molecular', label: 'Molecular', meters: 1e-9, color: 0x48cae4 },
    { id: 'virus', label: 'Virus', meters: 1e-7, color: 0x44ff88 },
    { id: 'cellular', label: 'Cellular', meters: 1e-5, color: 0x80ed99 },
    { id: 'neural', label: 'Neural', meters: 1e-2, color: 0xffdd55 },
    { id: 'human', label: 'Human', meters: 1, color: 0xffb347 },
    { id: 'planetary', label: 'Planetary', meters: 1e11, color: 0xff9f43 },
    { id: 'stellar', label: 'Stellar', meters: 1e9, color: 0xff6b6b },
    { id: 'galactic', label: 'Galactic', meters: 1e21, color: 0xff4757 },
    { id: 'cosmic', label: 'Cosmic', meters: 1e26, color: 0xd63031 }
  ];

  // Logarithmic scale: map meters to 3D position
  // Planck = 0, Cosmic = 100 (in a scaled view)
  function metersToPosition(meters, maxY) {
    const minLog = Math.log10(1.616e-35);
    const maxLog = 26; // 10^26
    const logMeters = Math.log10(meters);
    const t = (logMeters - minLog) / (maxLog - minLog);
    return t * maxY;
  }

  function init() {
    const container = document.getElementById('scaleScene');
    if (!container) {
      console.error('Scale scene container not found');
      return;
    }

    clock = new THREE.Clock();

    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x07111c);
    scene.fog = new THREE.FogExp2(0x07111c, 0.008);

    // Camera
    camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 40, 60);
    camera.lookAt(0, 40, 0);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;
    container.appendChild(renderer.domElement);

    // Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 20;
    controls.maxDistance = 200;
    controls.target.set(0, 40, 0);

    // Post-processing
    try {
      composer = new THREE.EffectComposer(renderer);
      const renderPass = new THREE.RenderPass(scene, camera);
      composer.addPass(renderPass);

      const bloomPass = new THREE.UnrealBloomPass(
        new THREE.Vector2(container.clientWidth, container.clientHeight),
        0.6, 0.4, 0.85
      );
      composer.addPass(bloomPass);
    } catch(e) {
      composer = null;
    }

    // Lighting
    setupLighting();

    // Create scale nodes
    createScaleNodes();

    // Create central beam
    createCentralBeam();

    // Create particle background
    createParticles();

    // Events
    setupEvents();

    // Start animation loop
    animate();
  }

  function setupLighting() {
    const ambient = new THREE.AmbientLight(0x222244, 0.6);
    scene.add(ambient);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 50, 20);
    scene.add(dirLight);

    const fillLight = new THREE.PointLight(0x00cfff, 0.4, 200);
    fillLight.position.set(-30, 30, -20);
    scene.add(fillLight);

    const rimLight = new THREE.PointLight(0xffdd55, 0.3, 200);
    rimLight.position.set(30, 60, 30);
    scene.add(rimLight);
  }

  function createScaleNodes() {
    const maxY = 100;

    SCALES.forEach((scale, index) => {
      const y = metersToPosition(scale.meters, maxY);
      
      // Node sphere
      const radius = index === 0 || index === SCALES.length - 1 ? 2.5 : 1.8;
      const geometry = new THREE.SphereGeometry(radius, 32, 32);
      const material = new THREE.MeshStandardMaterial({
        color: scale.color,
        emissive: scale.color,
        emissiveIntensity: 0.3,
        metalness: 0.4,
        roughness: 0.6
      });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set(0, y, 0);
      sphere.userData = { scale: scale, index: index };
      scene.add(sphere);
      scaleNodes.push(sphere);

      // Glow ring around node
      const ringGeometry = new THREE.RingGeometry(radius + 0.3, radius + 0.6, 32);
      const ringMaterial = new THREE.MeshBasicMaterial({
        color: scale.color,
        transparent: true,
        opacity: 0.3,
        side: THREE.DoubleSide
      });
      const ring = new THREE.Mesh(ringGeometry, ringMaterial);
      ring.position.copy(sphere.position);
      ring.rotation.x = Math.PI / 2;
      scene.add(ring);

      // Label (canvas-based for crisp text)
      if (showLabels) {
        const label = createLabel(scale.label, scale.color);
        label.position.set(radius + 3, y, 0);
        scene.add(label);
        labels.push(label);
      }
    });
  }

  function createLabel(text, color) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = 256;
    canvas.height = 64;

    context.fillStyle = 'transparent';
    context.fillRect(0, 0, canvas.width, canvas.height);

    context.font = 'bold 28px Trebuchet MS, sans-serif';
    context.fillStyle = '#' + color.toString(16).padStart(6, '0');
    context.textAlign = 'left';
    context.textBaseline = 'middle';
    context.fillText(text, 10, 32);

    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      opacity: 0.9
    });
    const sprite = new THREE.Sprite(material);
    sprite.scale.set(12, 3, 1);

    return sprite;
  }

  function createCentralBeam() {
    // Main beam
    const beamGeometry = new THREE.CylinderGeometry(0.15, 0.15, 105, 16);
    const beamMaterial = new THREE.MeshStandardMaterial({
      color: 0x00cfff,
      emissive: 0x00cfff,
      emissiveIntensity: 0.1,
      metalness: 0.8,
      roughness: 0.2,
      transparent: true,
      opacity: 0.4
    });
    const beam = new THREE.Mesh(beamGeometry, beamMaterial);
    beam.position.set(0, 50, 0);
    scene.add(beam);

    // Tick marks along beam
    for (let i = 0; i <= 10; i++) {
      const y = i * 10;
      const tickGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.5, 8);
      const tickMaterial = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        emissiveIntensity: 0.2,
        transparent: true,
        opacity: 0.5
      });
      const tick = new THREE.Mesh(tickGeometry, tickMaterial);
      tick.position.set(0, y, 0);
      scene.add(tick);
    }
  }

  function createParticles() {
    const particleCount = 500;
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 150;
      positions[i * 3 + 1] = Math.random() * 110;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 150;
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.3,
      transparent: true,
      opacity: 0.4
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);
  }

  function showScaleInfo(scale) {
    const panel = document.getElementById('scaleInfoPanel');
    const nameEl = document.getElementById('scaleName');
    const contentEl = document.getElementById('scaleInfoContent');

    if (!panel || !nameEl || !contentEl) return;

    // Find results for this scale
    const results = window.PFExplorerData ? 
      window.PFExplorerData.results.filter(r => r.scaleId === scale.id) : [];

    nameEl.textContent = scale.label + ' Scale';

    let html = `
      <div class="scale-meters">${scale.meters.toExponential(3)} m</div>
      <p>${getScaleDescription(scale.id)}</p>
    `;

    if (results.length > 0) {
      html += '<h4>PF Results</h4><div class="scale-result-list">';
      results.forEach(r => {
        html += `
          <div class="scale-result-item" data-result="${r.id}">
            <div class="result-title">${r.shortTitle || r.title}</div>
            <span class="result-status ${r.status}">${r.status}</span>
          </div>
        `;
      });
      html += '</div>';
    } else {
      html += '<p><em>No mapped results yet at this scale.</em></p>';
    }

    contentEl.innerHTML = html;
    panel.classList.add('active');

    // Bind result clicks
    contentEl.querySelectorAll('.scale-result-item').forEach(item => {
      item.addEventListener('click', () => {
        const resultId = item.dataset.result;
        window.location.href = `index.html?result=${resultId}`;
      });
    });
  }

  function getScaleDescription(scaleId) {
    const descriptions = {
      'planck': 'The geometry boundary. Where spacetime itself emerges from coherent propagation. The God Equation launches from here.',
      'quantum-foam': 'Virtual fluctuations at the Planck scale. The medium\'s baseline noise.',
      'gut': 'Grand Unification scale. Where the three gauge forces merge in standard physics.',
      'matter': 'The densest cluster. Topology, Koide, Weinberg angle, and the hierarchy lock together.',
      'proton': 'Quarks and gluons. QCD confinement and the φ³ mass ratio signal.',
      'nuclear': 'Nuclear structure. Amplified matter-scale coherence.',
      'atomic': 'Where gravity becomes refraction. Bohr quantization and the Coulomb lens become visual.',
      'molecular': 'The propagation Lagrangian appears. Variable-c prediction at large scales.',
      'virus': 'Self-replicating propagation patterns. The bridge between physics and biology.',
      'cellular': 'Active coherence maintenance. Life enters as a coherence phenomenon.',
      'neural': 'Consciousness metrics. Self-reference becomes architecture.',
      'human': 'Topology into daily structure. Beauty, efficiency, the compressed 2/3 intuition.',
      'planetary': 'Refractive gravity. Large-scale propagation with the same lens law.',
      'stellar': 'Stellar nucleosynthesis. Where heavy elements form.',
      'galactic': 'Galactic rotation curves. Dark matter as coherence at cosmic scale.',
      'cosmic': 'CMB and large-scale structure. The universe as a propagating pattern.'
    };
    return descriptions[scaleId] || 'Explore this scale in the Propagation Framework.';
  }

  function navigateToScale(index) {
    const scale = SCALES[index];
    if (!scale) return;

    // Animate camera to focus on this scale
    const y = metersToPosition(scale.meters, 100);
    const targetY = y;

    // Smooth camera movement
    const startY = camera.position.y;
    const duration = 1000;
    const startTime = Date.now();

    function animateCamera() {
      const elapsed = Date.now() - startTime;
      const t = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);

      camera.position.y = startY + (targetY - startY) * eased;
      controls.target.y = targetY;

      if (t < 1) {
        requestAnimationFrame(animateCamera);
      }
    }

    animateCamera();
    showScaleInfo(scale);

    // Highlight the selected node
    scaleNodes.forEach((node, i) => {
      const scale_data = node.userData.scale;
      const material = node.material;
      if (i === index) {
        material.emissiveIntensity = 0.8;
        material.scale.setScalar(1.3);
      } else {
        material.emissiveIntensity = 0.3;
        material.scale.setScalar(1);
      }
    });
  }

  function animate() {
    requestAnimationFrame(animate);

    const time = clock.getElapsedTime();

    // Animate scale nodes (subtle pulse)
    scaleNodes.forEach((node, i) => {
      const pulse = 1 + Math.sin(time * 2 + i * 0.5) * 0.05;
      if (node.material.emissiveIntensity > 0.5) {
        node.material.emissiveIntensity = 0.5 + Math.sin(time * 3 + i) * 0.3;
      }
    });

    controls.update();

    if (composer) {
      composer.render();
    } else {
      renderer.render(scene, camera);
    }
  }

  function setupEvents() {
    // Resize
    window.addEventListener('resize', () => {
      const container = document.getElementById('scaleScene');
      if (!container) return;

      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
      if (composer) {
        composer.setSize(container.clientWidth, container.clientHeight);
      }
    });

    // Click on nodes
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    renderer.domElement.addEventListener('click', (event) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scaleNodes);

      if (intersects.length > 0) {
        const scale = intersects[0].object.userData.scale;
        const index = intersects[0].object.userData.index;
        navigateToScale(index);
      }
    });

    // Hover effect
    renderer.domElement.addEventListener('mousemove', (event) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scaleNodes);

      renderer.domElement.style.cursor = intersects.length > 0 ? 'pointer' : 'grab';
    });

    // Back button
    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        window.location.href = 'index.html';
      });
    }

    // Reset camera
    const resetBtn = document.getElementById('resetCamera');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        camera.position.set(0, 40, 60);
        controls.target.set(0, 40, 0);
      });
    }

    // Toggle labels
    const toggleLabelsBtn = document.getElementById('toggleLabels');
    if (toggleLabelsBtn) {
      toggleLabelsBtn.addEventListener('click', () => {
        showLabels = !showLabels;
        labels.forEach(label => {
          label.visible = showLabels;
        });
        toggleLabelsBtn.classList.toggle('is-active', showLabels);
      });
    }

    // Scale navigation slider
    const scaleNavSlider = document.getElementById('scaleNavSlider');
    if (scaleNavSlider) {
      scaleNavSlider.addEventListener('input', (e) => {
        const index = parseInt(e.target.value);
        navigateToScale(index);
      });
    }

    // Close info panel
    const closeInfoBtn = document.getElementById('closeInfo');
    if (closeInfoBtn) {
      closeInfoBtn.addEventListener('click', () => {
        const panel = document.getElementById('scaleInfoPanel');
        if (panel) panel.classList.remove('active');
      });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        window.location.href = 'index.html';
      }
      if (e.key === 'l' || e.key === 'L') {
        toggleLabelsBtn.click();
      }
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
