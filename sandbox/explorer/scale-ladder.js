/**
 * Scale Ladder — Full-screen Three.js Scale Navigation
 * Uses: ScaleEngine + PropagationShaders + ScaleScenes
 */
(function () {
  'use strict';

  var _engine;
  var _clock;
  var _infoPanel;

  function init() {
    var container = document.getElementById('scaleScene');
    if (!container) {
      console.error('[scale-ladder] #scaleScene not found');
      return;
    }

    _clock = new THREE.Clock();
    _infoPanel = {
      el:     document.getElementById('scaleInfoPanel'),
      nameEl: document.getElementById('scaleName'),
      content: document.getElementById('scaleInfoContent')
    };

    // Boot the engine
    _engine = window.ScaleEngine.init(container);

    // Wire UI
    wireSlider();
    wireControls();
    wireBackButton();
    wireScaleInfoPanel();
    wireKeyboard();
    wireResize();

    // Check for autostart from zoom sequence — words → waves
    var params = new URLSearchParams(window.location.search);
    var autostart = params.get('autostart') === '1';
    var mode = params.get('mode');

    if (autostart) {
      // Coming from zoom sequence — immediately start at Human scale with waves active
      // Use timeout to ensure engine is fully initialized
      setTimeout(function () {
        _engine.navigateToScale('human', { duration: 0, force: true });
        showScaleInfo('human');
        // Trigger wave visualization after brief settle
        setTimeout(function () {
          if (_engine.triggerWaveVisualization) {
            _engine.triggerWaveVisualization('human');
          }
        }, 300);
      }, 100);
    } else {
      // Normal entry — navigate to matter scale
      _engine.navigateToScale('matter', { duration: 1400 });
      showScaleInfo('matter');
    }

    // Start render loop
    animate();
  }

  function animate() {
    requestAnimationFrame(animate);
    var dt = Math.min(_clock.getDelta(), 0.05);
    var time = _clock.elapsedTime;

    _engine.getControls().update();
    _engine.tick(dt, time);

    // Update label visibility based on camera position
    if (_engine.updateLabelVisibility) {
      _engine.updateLabelVisibility(_engine.getCamera().position.y);
    }

    if (_engine.getComposer()) {
      _engine.getComposer().render();
    } else {
      _engine.getRenderer().render(_engine.getScene(), _engine.getCamera());
    }
  }

  function wireSlider() {
    var slider = document.getElementById('scaleNavSlider');
    if (!slider) return;
    slider.addEventListener('input', function () {
      var index = parseInt(slider.value, 10);
      var scales = _engine.getScales();
      if (scales[index]) {
        _engine.navigateToScale(scales[index].id, { duration: 1000 });
        showScaleInfo(scales[index].id);
      }
    });
    // Sync slider to current scale
    _engine.onScaleChange(function (scale, index) {
      slider.value = index;
    });
  }

  function wireControls() {
    var resetBtn = document.getElementById('resetCamera');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        _engine.navigateToScale('matter', { force: true, duration: 1200 });
        showScaleInfo('matter');
      });
    }

    var labelsBtn = document.getElementById('toggleLabels');
    if (labelsBtn) {
      labelsBtn.addEventListener('click', function () {
        var current = labelsBtn.classList.contains('is-active');
        _engine.setLabelsVisible(!current);
        labelsBtn.classList.toggle('is-active', !current);
      });
    }
  }

  function wireBackButton() {
    var btn = document.getElementById('backBtn');
    if (btn) {
      btn.addEventListener('click', function () {
        window.location.href = 'index.html';
      });
    }
  }

  function wireScaleInfoPanel() {
    var renderer = _engine.getRenderer();
    if (!renderer) return;
    var raycaster = new THREE.Raycaster();
    var mouse = new THREE.Vector2();

    renderer.domElement.addEventListener('click', function (event) {
      var rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouse, _engine.getCamera());
      var hits = raycaster.intersectObjects(_engine.getScaleNodes());
      if (hits.length > 0) {
        var scaleId = hits[0].object.userData.scaleId;
        _engine.navigateToScale(scaleId, { duration: 900 });
        showScaleInfo(scaleId);
      }
    });

    renderer.domElement.addEventListener('mousemove', function (event) {
      var rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouse, _engine.getCamera());
      var hits = raycaster.intersectObjects(_engine.getScaleNodes());
      renderer.domElement.style.cursor = hits.length > 0 ? 'pointer' : 'grab';
    });

    var closeBtn = document.getElementById('closeInfo');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        if (_infoPanel.el) _infoPanel.el.classList.remove('active');
      });
    }
  }

  function wireKeyboard() {
    var lastKeyTime = 0;
    var KEY_DEBOUNCE = 250; // ms between key presses

    document.addEventListener('keydown', function (e) {
      if (e.repeat) return; // Prevent rapid jumps when holding down keys

      if (e.key === 'Escape') {
        window.location.href = 'index.html';
        return;
      }
      if (e.key === 'l' || e.key === 'L') {
        document.getElementById('toggleLabels').click();
        return;
      }

      // Arrow key navigation with debounce
      var now = Date.now();
      if (now - lastKeyTime < KEY_DEBOUNCE) return;

      var scales = _engine.getScales();
      var currentIdx = scales.findIndex(function (s) { return s.id === _engine.getCurrentScaleId(); });

      if ((e.key === 'ArrowUp' || e.key === 'ArrowRight') && currentIdx < scales.length - 1) {
        lastKeyTime = now;
        _engine.navigateToScale(scales[currentIdx + 1].id);
        showScaleInfo(scales[currentIdx + 1].id);
      }
      if ((e.key === 'ArrowDown' || e.key === 'ArrowLeft') && currentIdx > 0) {
        lastKeyTime = now;
        _engine.navigateToScale(scales[currentIdx - 1].id);
        showScaleInfo(scales[currentIdx - 1].id);
      }
    });
  }

  function wireResize() {
    window.addEventListener('resize', function () {
      _engine.resize();
    });
  }

  function showScaleInfo(scaleId) {
    if (!_infoPanel.el) return;
    var scale = _engine.getScales().find(function (s) { return s.id === scaleId; });
    if (!scale) return;

    var results = (window.PFExplorerData ?
      window.PFExplorerData.results.filter(function (r) { return r.scaleId === scaleId; }) :
      []);

    if (_infoPanel.nameEl) _infoPanel.nameEl.textContent = scale.label + ' Scale';

    var html = '<div class="scale-meters">' + scale.meters.toExponential(3) + ' m</div>';
    html += '<p>' + getScaleDescription(scaleId) + '</p>';
    html += '<div class="scale-freq">ν = ' + getFrequency(scale.meters).toExponential(2) + ' Hz</div>';

    if (results.length > 0) {
      html += '<h4>PF Results</h4><div class="scale-result-list">';
      results.forEach(function (r) {
        var statusClass = r.status ? r.status.toLowerCase().replace(' ', '-') : '';
        var authorityId = (r.authorityClaimIds && r.authorityClaimIds.length > 0) ? r.authorityClaimIds[0] : r.id;
        html += [
          '<div class="scale-result-item" data-result="' + r.id + '">',
          '<div class="result-title">' + (r.shortTitle || r.title) + '</div>',
          '<span class="result-status ' + statusClass + '" data-claim-id="' + authorityId + '">' + (r.status || 'UNAVAILABLE') + '</span>',
          '</div>'
        ].join('');
      });
      html += '</div>';
    } else {
      html += '<p><em>No mapped PF results at this scale yet.</em></p>';
    }

    if (_infoPanel.content) _infoPanel.content.innerHTML = html;

    // Bind result clicks
    if (_infoPanel.content) {
      _infoPanel.content.querySelectorAll('.scale-result-item').forEach(function (item) {
        item.addEventListener('click', function () {
          window.location.href = 'index.html#' +
            (window.PFExplorerData ?
              window.PFExplorerData.results.find(function (r) { return r.id === item.dataset.result; }).panelId || 'hub' :
              'hub');
        });
      });
    }

    _infoPanel.el.classList.add('active');
  }

  function getScaleDescription(id) {
    var d = {
      planck:      'The geometry boundary. Where spacetime itself emerges from coherent propagation. The God Equation launches from here.',
      'quantum-foam': 'Virtual fluctuations at the Planck boundary. The medium baseline noise.',
      gut:         'Grand Unification scale. Where the three gauge forces begin to merge.',
      matter:      'The densest cluster. Topology, Koide ratio, Weinberg angle, and the hierarchy lock together here.',
      proton:      'Quarks and gluons. QCD confinement and the φ³ mass-ratio signal live here.',
      nuclear:     'Nuclear structure. Amplified matter-scale coherence.',
      atomic:      'Where gravity becomes refraction. Bohr quantization and the Coulomb lens become visual.',
      molecular:   'The propagation Lagrangian appears. Variable-c prediction at large scales.',
      virus:       'Self-replicating propagation patterns. The bridge between physics and biology.',
      cellular:    'Active coherence maintenance. Life enters as a coherence phenomenon.',
      neural:      'Consciousness metrics. Self-reference becomes architecture.',
      human:       'Topology into daily structure. Beauty, efficiency, the compressed 2/3 intuition.',
      planetary:   'Refractive gravity. Large-scale propagation with the same lens law.',
      stellar:    'Stellar nucleosynthesis. Where heavy elements form from coherence condensation.',
      galactic:   'Galactic rotation curves. Dark matter as coherence at cosmic scale.',
      cosmic:     'CMB and large-scale structure. The universe as a frozen propagation pattern.'
    };
    return d[id] || 'Explore this scale in the Propagation Framework.';
  }

  function getFrequency(meters) {
    return 3e8 / meters;
  }

  // Bootstrap
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
