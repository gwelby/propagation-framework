/**
 * No-Go Museum — nogos.js
 *
 * Gallery of documented failed approaches in the Propagation Framework.
 * Each entry: the approach, the specific failure mode, and the lesson.
 * 
 * Enhanced with rich exhibits, status badges, and visual celebration of honest negatives.
 */
(function () {
  'use strict';

  // ── Status Types ─────────────────────────────────────────────────────────────
  var STATUS = {
    FAILED: { label: 'FAILED', color: '#ff4444', icon: '✕' },
    NO_GO: { label: 'NO-GO', color: '#ff6b6b', icon: '⊘' },
    NEGATIVE: { label: 'NEGATIVE', color: '#ff8c42', icon: '−' },
    POSITIVE: { label: 'Closed Positively', color: '#44ff88', icon: '✓' }
  };

  // ── NO-GO Entries ─────────────────────────────────────────────────────────────
  var NO_GO_ENTRIES = [
    {
      id: 'harmonic-series-masses',
      title: 'Harmonic Series Claim',
      question: 'Do masses follow harmonic ratios?',
      targetFrontier: 'koide',
      date: '2025-12',
      statusType: 'FAILED',
      result: 'CV = 0.94 (essentially random)',
      isPositive: false,
      failureMode: 'Monte Carlo: Coefficient of Variation = 0.94. The harmonic series in particle masses is essentially random noise.',
      whyFailed: [
        'Test: harmonic series A·(1 + 1/2 + 1/3 + ...) was proposed as a description of the mass spectrum.',
        'Monte Carlo over random mass assignments showed CV ≈ 0.94 — indistinguishable from noise.',
        'The apparent pattern was a post-hoc narrative, not a genuine signal.',
        'This was the first honest failure of the sandbox — documented, not buried.'
      ],
      lesson: 'Beauty ≠ proof. Numerical pattern-matching without a derivation chain is not physics. The sandbox showed this clearly, and the framework updated.',
      celebration: 'First documented failure. Established the honesty protocol.',
      sources: [
        { label: 'sandbox_results.md', href: '../../sandbox_results.md' },
        { label: 'CLAIMS.md — NO-GO entry', href: '../../CLAIMS.md' }
      ]
    },
    {
      id: 't022-casimir-selector',
      title: 'T-022 Casimir Selector',
      question: 'Does 2/9 emerge from bounded Casimir?',
      targetFrontier: 'weinberg',
      date: '2026-04',
      statusType: 'NEGATIVE',
      result: 'No physical spin assignment produces x* = 2/9',
      isPositive: false,
      failureMode: 'Comprehensive scan of bounded Casimir configurations: no physically valid spin assignment produces the target selector value of 2/9.',
      whyFailed: [
        'The bounded Casimir lemma was proposed as a route to the phase selector δ = 2/9.',
        'Scan over j ∈ {0, 1/2, 1, 3/2, 2} with standard C₂ eigenvalues failed to produce x* = 2/9.',
        'No combination of (j₁, j₂) physical spin assignments yielded the target value.',
        'The T-022 route is closed as an honest negative — it fenced the lane definitively.'
      ],
      lesson: 'Honest negative, fenced the lane. The Casimir route to 2/9 is closed. Framework must seek alternative selectors or reconsider the phase structure.',
      celebration: 'Honest negative that prevented wasted effort. The lane is fenced.',
      sources: [
        { label: 'ACTIVE_ISSUES.md — T-022', href: '../../ACTIVE_ISSUES.md' },
        { label: 'casimir_polynomial_synthesis.md', href: '../../derivations/casimir_polynomial_synthesis.md' }
      ]
    },
    {
      id: 't021-rg-crossing',
      title: 'T-021 RG Crossing',
      question: 'Does sin²θ_W run to δ at 98 GeV?',
      targetFrontier: 'weinberg',
      date: '2026-04',
      statusType: 'NEGATIVE',
      result: 'Standard Model conventions don\'t support this',
      isPositive: false,
      failureMode: 'Standard Model running conventions and renormalization schemes do not support the claim that sin²θ_W runs to δ = 2/9 at 98 GeV.',
      whyFailed: [
        'Proposed: The Weinberg angle runs to the phase selector δ = 2/9 at a specific energy scale (~98 GeV).',
        'Audit of SM renormalization schemes (MS-bar, on-shell, etc.) showed no such crossing.',
        'The energy scale 98 GeV has no special significance in running electroweak parameters.',
        'Precision matters — the SM conventions are well-tested and do not accommodate this hypothesis.'
      ],
      lesson: 'Precision matters. Well-tested theoretical frameworks cannot be overridden by numerological coincidence. The RG crossing hypothesis is closed.',
      celebration: 'Precision audit protected framework from false correlation.',
      sources: [
        { label: 'ACTIVE_ISSUES.md — T-021', href: '../../ACTIVE_ISSUES.md' },
        { label: 'CLAIMS.md', href: '../../CLAIMS.md' }
      ]
    },
    {
      id: 'g3-path-b-families-ab',
      title: 'G3 Path B — Families A/B',
      question: 'Can closure functionals rescue Path B?',
      targetFrontier: 'god-equation',
      date: '2026-04',
      statusType: 'NO_GO',
      result: 'All closure functionals attempted failed',
      isPositive: false,
      failureMode: 'Path B Families A and B: attempted closure functionals for nearest-neighbor circulant and edge-flux current variants all failed.',
      whyFailed: [
        'Family A (nearest-neighbor circulant): T³ remains mixed unless ab = 0. The symmetric model does not close.',
        'Family B (edge-flux current): circulant edge flux does not produce first-order Markov coarse-grained walk.',
        'Family B variant (intensity fraction): ratio formulation insufficient for three-channel factorization.',
        'The gaps are structural, not numerical — no parameter adjustment can rescue these forms.'
      ],
      lesson: 'Document the dead ends. Three-channel structure requires full aS† + bS†² form, not simplified variants. Only Family C remains viable.',
      celebration: 'Systematic exploration eliminated false paths, narrowing to the viable route.',
      sources: [
        { label: 'god_eq_gap_B_nearest_neighbor_no_go.md', href: '../../derivations/god_eq_gap_B_nearest_neighbor_no_go.md' },
        { label: 'god_eq_path_b_edge_flux_current_no_go_2026-04-01.md', href: '../../derivations/god_eq_path_b_edge_flux_current_no_go_2026-04-01.md' },
        { label: 'god_eq_path_b_intensity_fraction_no_go_2026-04-01.md', href: '../../derivations/god_eq_path_b_intensity_fraction_no_go_2026-04-01.md' }
      ]
    },
    {
      id: 'single-scalar-lagrangian',
      title: 'Single-Scalar Lagrangian → Casimir Polynomial',
      targetFrontier: 'weinberg',
      date: '2026-03',
      statusType: 'NO_GO',
      result: 'Angular sector required, not derivable',
      isPositive: false,
      failureMode: 'The Lagrangian is affine in the spectral variable. The Casimir eigenvalue C₂ never enters without an angular sector structure.',
      whyFailed: [
        'A single scalar field Φ(x) with canonical kinetic term produces an action S = ∫ d⁴x (½∂²Φ + V(Φ)).',
        'The Casimir operator eigenvalue C₂ = j(j+1) requires an internal SU(2) or angular degree of freedom to appear in the action.',
        'Without an angular sector, the Casimir term is invisible — it cannot be varied to produce the polynomial.',
        'This is not a numerical subtlety; it is a structural omission.'
      ],
      lesson: 'A scalar field alone cannot produce the Casimir polynomial. The angular sector is not a detail — it is load-bearing.',
      celebration: 'Clarified that angular structure is fundamental, not decorative.',
      sources: [
        { label: 'casimir_polynomial_route_lagrangian.md', href: '../../derivations/casimir_polynomial_route_lagrangian.md' },
        { label: 'CLAIMS.md — NO-GO entry', href: '../../CLAIMS.md' }
      ]
    },
    {
      id: 'propagator-pole',
      title: 'Propagator Pole → Casimir Polynomial',
      targetFrontier: 'weinberg',
      date: '2026-03',
      statusType: 'NO_GO',
      result: 'Requires QFT not in axioms',
      isPositive: false,
      failureMode: 'Route A Lemma 3 requires a quantum field theory framework that Axioms 1–3 do not yet supply.',
      whyFailed: [
        'The propagator pole method routes through a full QFT: computing ⟨0|Tφ(x)φ(0)|0⟩ and reading off residues.',
        'Axioms 1–3 are classical-ish propagation statements. They do not contain the quantization postulate.',
        'Formally postulating QFT structure would smuggle in an assumption that was never derived.',
        'The gap is not resolvable by more clever algebra — it is a pre-quantum vs. quantum boundary.'
      ],
      lesson: 'The propagation axioms do not yet contain quantum field theory. QFT must be derived, not assumed, as the framework\'s own literature has repeatedly shown.',
      celebration: 'Protected axiomatic integrity from smuggled assumptions.',
      sources: [
        { label: 'CLAIMS.md — NO-GO entry', href: '../../CLAIMS.md' }
      ]
    },
    {
      id: 'radius-scaling-debroglie',
      title: 'Radius Scaling r = βr_C in de Broglie Orbit',
      targetFrontier: 'generations',
      date: '2026-03',
      statusType: 'NO_GO',
      result: 'Extra-β discrepancy: γβ vs γβ²',
      isPositive: false,
      failureMode: 'Within the de Broglie orbit framing, r = βr_C contradicts the de Broglie wavelength constraint inside the orbit: λ = 2πr/γβ².',
      whyFailed: [
        'If r = βr_C, then λ = 2πβr_C / (γβ²) = (2πr_C) / (γβ).',
        'This does not equal the required 2πr_C (the nominal orbit circumference).',
        'The extra β in the denominator means the phase accumulation per orbit is wrong.',
        'The route was correctly closed by the Route A Lemma 1 objection: radius scaling contradicts de Broglie wavelength within the orbit framing.'
      ],
      lesson: 'The extra-β discrepancy (γβ vs γβ²) is not a numerical fix. It is a structural mismatch between two different geometric constraints.',
      celebration: 'Precise gap identification turned failure into attack surface.',
      sources: [
        { label: 'CLAIMS.md — NO-GO entry', href: '../../CLAIMS.md' },
        { label: 'Route A analysis — extra-β discrepancy', href: '../../derivations/casimir_polynomial_synthesis.md' }
      ]
    },
    {
      id: 'wigner-rotation-coaxial',
      title: 'Wigner Rotation via Coaxial Helical Geometry',
      targetFrontier: 'weinberg',
      date: '2026-03',
      statusType: 'NO_GO',
      result: 'Trivial W = 1 (Abelian algebra)',
      isPositive: false,
      failureMode: 'Path 3: Coaxial helical motion gives trivial W = 1. The Wigner rotation is identity, not a mixing.',
      whyFailed: [
        'In the coaxial geometry, the rotation about the propagation axis is commutative.',
        'Successive non-relativistic rotations about the same axis add linearly, not via the Bessel function composition.',
        'W₁(φ₁)W₂(φ₂) = exp(iφ₁J_z)exp(iφ₂J_z) = exp(i(φ₁+φ₂)J_z) = W(φ₁+φ₂).',
        'No Bessel function mixing = no W > 1 = the helix does not select higher spin states.'
      ],
      lesson: 'The helical geometry is physically correct for propagation but the rotation algebra for coaxial axes is Abelian. Wigner rotation non-trivialness requires non-collinear boost axes.',
      celebration: 'Algebraic precision identified why geometric intuition failed.',
      sources: [
        { label: 'casimir_polynomial_path2_poincare.md', href: '../../derivations/casimir_polynomial_path2_poincare.md' },
        { label: 'CLAIMS.md — NO-GO entry', href: '../../CLAIMS.md' }
      ]
    },
    {
      id: 'g3-canonical-class-function',
      title: 'g3 — Canonical Class Function Route',
      targetFrontier: 'weinberg',
      date: '2026-03',
      statusType: 'NO_GO',
      result: 'Constant value — no selectivity',
      isPositive: false,
      failureMode: 'The canonical class function g₃ produces a constant value for all configurations. No selectivity between k = 1 and k ≠ 1.',
      whyFailed: [
        'The class function g₃ = Tr(U^k) evaluated on the circulant internal sector gives: g₃(k) = 2cos(2πk/3) + 1.',
        'This is independent of the external spin j. The Casimir eigenvalue C₂ never enters.',
        'The route needs a function that distinguishes k = 1 (bijective, minimal coherence) from k ≠ 1.',
        'A constant function cannot provide that distinction.'
      ],
      lesson: 'The internal sector trace is not the right place to look for selectivity. The external geometry (winding number, helicity structure) must interact with the internal state.',
      celebration: 'Redirected search from internal to external geometric selectors.',
      sources: [
        { label: 'g3_canonical_class_function_no_go.md', href: '../../derivations/g3_canonical_class_function_no_go.md' },
        { label: 'CLAIMS.md — NO-GO entry', href: '../../CLAIMS.md' }
      ]
    },
    {
      id: 'g3-product-walk',
      title: 'g3 — Product Walk Route',
      targetFrontier: 'weinberg',
      date: '2026-03',
      statusType: 'NO_GO',
      result: 'Fails at N = 3 without new assumptions',
      isPositive: false,
      failureMode: 'The product walk formula for g₃ fails at three generations without additional assumptions.',
      whyFailed: [
        'The product formula: g₃(n,m) = f(n)g(m) + f(n)g(m) · O(λ) does not close at N = 3.',
        'At N = 3, the product walk gives the wrong phase factor unless additional coupling assumptions are introduced.',
        'Those additional assumptions are not derivable from Axioms 1–3 alone — they require new structure.',
        'This is not a matter of parameter fitting. The form itself fails at the physical generation count.'
      ],
      lesson: 'Three-generation kinematics cannot be reached by small corrections to two-generation kinematics. The N = 3 case requires its own derivation.',
      celebration: 'Established that three-generation physics is irreducible to two-generation approximations.',
      sources: [
        { label: 'g3_product_walk_no_go.md', href: '../../derivations/g3_product_walk_no_go.md' },
        { label: 'CLAIMS.md — NO-GO entry', href: '../../CLAIMS.md' }
      ]
    },
    {
      id: 'god-equation-nearest-neighbor',
      title: 'Nearest-Neighbor Circulant (God Equation Path B)',
      targetFrontier: 'god-equation',
      date: '2026-04',
      statusType: 'NO_GO',
      result: 'T³ remains mixed',
      isPositive: false,
      failureMode: 'Path B nearest-neighbor circulant: T³ remains mixed unless ab = 0. The symmetric nearest-neighbor model does not close.',
      whyFailed: [
        'The Lagrangian L = aS†S + bS†²S² + h.c. with nearest-neighbor circulant structure was explored.',
        'T³ = (aS† + bS†²)(aS + bS²)³ = ab²(...) + ... does not reduce to pure S³ or S†³.',
        'Mixed terms persist unless ab = 0 (pure single-term case, not genuinely three-channel).',
        'This is a precise algebraic failure, not a numerical gap.'
      ],
      lesson: 'The genuine three-channel circulant structure requires the full aS† + bS†² form, not a simplified nearest-neighbor variant. Path B as originally posed does not close.',
      celebration: 'Algebraic precision eliminated a simplified but insufficient route.',
      sources: [
        { label: 'god_eq_gap_B_nearest_neighbor_no_go.md', href: '../../derivations/god_eq_gap_B_nearest_neighbor_no_go.md' },
        { label: 'ACTIVE_ISSUES.md', href: '../../ACTIVE_ISSUES.md' }
      ]
    },
    {
      id: 'edge-flux-current',
      title: 'Edge Flux Current (God Equation Path B variant)',
      targetFrontier: 'god-equation',
      date: '2026-04',
      statusType: 'NO_GO',
      result: 'Not first-order Markovian',
      isPositive: false,
      failureMode: 'Edge flux current path: the circulant edge flux does not produce a first-order Markov coarse-grained walk.',
      whyFailed: [
        'The edge flux current approach attempts to derive a Markov chain from the circulant structure.',
        'The gap is that locality of the medium does not automatically yield first-order Markovian dynamics.',
        'The proof chain needs a memoryless coarse operator that has not been derived from Axioms 1–3.',
        'This is a genuine open gap, not a closed NO-GO — but the specific edge flux approach was closed.'
      ],
      lesson: 'Local propagation does not imply Markov propagation. The memoryless coarse operator must itself be derived, not assumed.',
      celebration: 'Distinguished locality from Markovianity — subtle but crucial.',
      sources: [
        { label: 'god_eq_path_b_edge_flux_current_no_go_2026-04-01.md', href: '../../derivations/god_eq_path_b_edge_flux_current_no_go_2026-04-01.md' }
      ]
    },
    {
      id: 'intensity-fraction',
      title: 'Intensity Fraction (God Equation Path B variant)',
      targetFrontier: 'god-equation',
      date: '2026-04',
      statusType: 'NO_GO',
      result: 'Insufficient for full factorization',
      isPositive: false,
      failureMode: 'Intensity fraction route: the ratio formulation does not capture the three-channel factorization required.',
      whyFailed: [
        'The intensity fraction I = P_k / ΣP_i approach was explored as an alternative to direct amplitude.',
        'For a genuine three-channel factorization H_prod, the fraction carries less information than the full joint law.',
        'The intensity fraction route was pursued as a weaker proxy — closed as not sufficient for full closure.'
      ],
      lesson: 'Factorization of marginals is weaker than full joint-law factorization. The God Equation needs H_prod itself, not a summary statistic.',
      celebration: 'Protected the God Equation from weakened proxy formulations.',
      sources: [
        { label: 'god_eq_path_b_intensity_fraction_no_go_2026-04-01.md', href: '../../derivations/god_eq_path_b_intensity_fraction_no_go_2026-04-01.md' }
      ]
    }
  ];

  // ── Positive closures (routes that found something instead) ──────────────────
  var POSITIVE_ENTRIES = [
    {
      id: 'z3-circulant-structure',
      title: 'ℤ₃ / Circulant Internal Sector (Wave 5/6)',
      question: 'Does ℤ₃ structure strengthen the framework?',
      targetFrontier: 'weinberg',
      date: '2026-03',
      statusType: 'POSITIVE',
      result: 'Survived hostile audit, now leading candidate',
      isPositive: true,
      failureMode: 'Not a failure — a positive finding that emerged from the Wigner rotation route.',
      whyFailed: [
        'Wave 5/6 of the Casimir multi-route attack found that ℤ₃ structure with genuine three-channel circulant coupling strengthens the overall case.',
        'The internal sector must be circulant (three equivalent channels) for the Casimir operator to have the right eigenvalue structure.',
        'This is not a closed route — it is a reinforced route. The ℤ₃ structure survived hostile audit.'
      ],
      lesson: 'The ℤ₃/circulant structure is now the leading candidate for the internal sector. IBM chirality evidence (Path A) further supports it.',
      celebration: 'Structure survived audit — confidence gained through opposition.',
      sources: [
        { label: 'CLAIMS.md — ℤ₃ evidence', href: '../../CLAIMS.md' },
        { label: 'ACTIVE_ISSUES.md', href: '../../ACTIVE_ISSUES.md' }
      ]
    },
    {
      id: 'extra-beta-debroglie',
      title: 'Extra-β Discrepancy (Route A — de Broglie route)',
      question: 'Why does Route A fail?',
      targetFrontier: 'generations',
      date: '2026-03',
      statusType: 'POSITIVE',
      result: 'Precise gap identified: γβ vs γβ²',
      isPositive: true,
      failureMode: 'Not a failure — the extra-β gap (γβ vs γβ²) was precisely identified and became an attack surface.',
      whyFailed: [
        'Route A (de Broglie orbit): the drift advance per revolution is N_dB = γβ² de Broglie wavelengths.',
        'The Casimir polynomial predicts γβ. The discrepancy is exactly one factor of β.',
        'This precise naming transformed a vague "it doesn\'t work" into a specific gap.',
        'Three candidate lemmas followed from this identification.'
      ],
      lesson: 'The de Broglie route is missing exactly one β. That gap is now a target for Lemma 2, Lemma 4, or the locking-radius route.',
      celebration: 'Vague failure transformed into precise attack surface.',
      sources: [
        { label: 'casimir_polynomial_synthesis.md', href: '../../derivations/casimir_polynomial_synthesis.md' }
      ]
    }
  ];

  // ── All entries ───────────────────────────────────────────────────────────────
  var ALL_ENTRIES = [].concat(NO_GO_ENTRIES, POSITIVE_ENTRIES);

  // ── Frontier labels ────────────────────────────────────────────────────────────
  var FRONTIER_LABELS = {
    'weinberg': 'Weinberg Angle',
    'god-equation': 'God Equation',
    'generations': 'Generation Count',
    'koide': 'Koide / Mass',
    'mass-harmony': 'Mass Harmony',
    'topology': 'Topology'
  };

  // ── Current expanded card ─────────────────────────────────────────────────────
  var expandedCardId = null;

  // ── Render gallery ────────────────────────────────────────────────────────────
  function renderGallery(filter) {
    var gallery = document.getElementById('nogosGallery');
    if (!gallery) return;

    var filtered = filter === 'all'
      ? ALL_ENTRIES
      : ALL_ENTRIES.filter(function (e) { return e.targetFrontier === filter; });

    // Filter buttons
    document.querySelectorAll('.filter-chip').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-filter') === filter);
    });

    gallery.innerHTML = filtered.map(function (entry, idx) {
      var status = STATUS[entry.statusType] || STATUS.NO_GO;
      var isExpanded = expandedCardId === entry.id;
      
      return (
        '<article class="nogo-card' + (entry.isPositive ? ' positive' : '') + (isExpanded ? ' expanded' : '') + '" data-id="' + entry.id + '" style="animation-delay:' + (idx * 60) + 'ms">' +
          '<div class="nogo-card-header">' +
            '<span class="nogo-card-badge" style="--badge-color:' + status.color + '">' +
              '<span class="badge-icon">' + status.icon + '</span>' +
              '<span class="badge-label">' + status.label + '</span>' +
            '</span>' +
            '<span class="nogo-card-date">' + entry.date + '</span>' +
          '</div>' +
          '<h3 class="nogo-card-title">' + entry.title + '</h3>' +
          (entry.question ? '<p class="nogo-card-question">"' + entry.question + '"</p>' : '') +
          '<span class="nogo-card-target">' + (FRONTIER_LABELS[entry.targetFrontier] || entry.targetFrontier) + '</span>' +
          '<p class="nogo-card-failure">' + entry.failureMode + '</p>' +
          (entry.result ? '<div class="nogo-card-result"><span class="result-label">Result:</span> ' + entry.result + '</div>' : '') +
          '<div class="nogo-card-footer">' +
            '<span class="nogo-card-lesson">' + entry.lesson.substring(0, 100) + '…</span>' +
            '<button class="nogo-card-expand" type="button">' + (isExpanded ? 'Collapse ↑' : 'Details →') + '</button>' +
          '</div>' +
          (isExpanded ? renderExpandedContent(entry, status) : '') +
        '</article>'
      );
    }).join('');

    // Card interactions
    gallery.querySelectorAll('.nogo-card').forEach(function (card) {
      var expandBtn = card.querySelector('.nogo-card-expand');
      if (expandBtn) {
        expandBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          toggleCard(card.getAttribute('data-id'));
        });
      }
      card.addEventListener('click', function () {
        showDetail(card.getAttribute('data-id'));
      });
    });

    // Update stats
    var noGoCount = filtered.filter(function (e) { return !e.isPositive; }).length;
    var positiveCount = filtered.filter(function (e) { return e.isPositive; }).length;
    document.getElementById('nogoTotal').textContent = noGoCount;
    document.getElementById('nogoPositive').textContent = positiveCount;
  }

  // ── Render expanded card content ────────────────────────────────────────────
  function renderExpandedContent(entry, status) {
    return (
      '<div class="nogo-card-expanded" onclick="event.stopPropagation()">' +
        '<div class="expanded-section">' +
          '<h4><span class="section-icon">🔍</span> Why It Failed</h4>' +
          '<ul class="why-failed-list">' + entry.whyFailed.map(function (w) { return '<li>' + w + '</li>'; }).join('') + '</ul>' +
        '</div>' +
        '<div class="expanded-section">' +
          '<h4><span class="section-icon">💡</span> The Lesson</h4>' +
          '<p class="lesson-text">' + entry.lesson + '</p>' +
        '</div>' +
        (entry.celebration ? '<div class="expanded-section celebration">' +
          '<h4><span class="section-icon">🎉</span> Why We Celebrate This</h4>' +
          '<p class="celebration-text">' + entry.celebration + '</p>' +
        '</div>' : '') +
        '<div class="expanded-section sources">' +
          '<h4><span class="section-icon">📚</span> Sources</h4>' +
          '<div class="source-links">' +
            entry.sources.map(function (s) {
              return '<a href="' + s.href + '" target="_blank" rel="noreferrer" class="source-link">' + s.label + ' ↗</a>';
            }).join('') +
          '</div>' +
        '</div>' +
      '</div>'
    );
  }

  // ── Toggle card expansion ────────────────────────────────────────────────────
  function toggleCard(id) {
    if (expandedCardId === id) {
      expandedCardId = null;
    } else {
      expandedCardId = id;
    }
    // Re-render to show/hide expanded content
    var activeFilter = document.querySelector('.filter-chip.active');
    renderGallery(activeFilter ? activeFilter.getAttribute('data-filter') : 'all');
  }

  // ── Detail overlay ────────────────────────────────────────────────────────────
  function showDetail(id) {
    var entry = ALL_ENTRIES.find(function (e) { return e.id === id; });
    if (!entry) return;

    var status = STATUS[entry.statusType] || STATUS.NO_GO;
    var overlay = document.getElementById('nogoDetailOverlay');
    var card = document.getElementById('nogoDetailCard');
    var tag = document.getElementById('nogoDetailTag');
    var title = document.getElementById('nogoDetailTitle');
    var question = document.getElementById('nogoDetailQuestion');
    var result = document.getElementById('nogoDetailResult');
    var body = document.getElementById('nogoDetailBody');
    var celebration = document.getElementById('nogoDetailCelebration');
    var sources = document.getElementById('nogoDetailSources');

    tag.textContent = status.label;
    tag.style.background = status.color;
    card.classList.toggle('is-positive', !!entry.isPositive);
    card.style.setProperty('--status-color', status.color);
    title.textContent = entry.title;
    
    if (question) question.textContent = entry.question ? '"' + entry.question + '"' : '';
    if (result) result.innerHTML = entry.result ? '<strong>Result:</strong> ' + entry.result : '';

    body.innerHTML =
      '<div class="nogo-detail-section">' +
        '<h4><span class="section-icon">🎯</span> The Approach</h4>' +
        '<p>Targeting <strong>' + (FRONTIER_LABELS[entry.targetFrontier] || entry.targetFrontier) + '</strong> — ' + entry.failureMode + '</p>' +
      '</div>' +
      '<div class="nogo-detail-section">' +
        '<h4><span class="section-icon">🔍</span> Why It Failed</h4>' +
        '<ul class="detail-why-failed">' + entry.whyFailed.map(function (w) { return '<li>' + w + '</li>'; }).join('') + '</ul>' +
      '</div>' +
      '<div class="nogo-detail-section lesson-section">' +
        '<h4><span class="section-icon">💡</span> The Lesson</h4>' +
        '<p class="lesson-highlight">' + entry.lesson + '</p>' +
      '</div>';

    if (celebration) {
      if (entry.celebration) {
        celebration.innerHTML =
          '<h4><span class="section-icon">🎉</span> Why We Celebrate This</h4>' +
          '<p class="celebration-highlight">' + entry.celebration + '</p>';
        celebration.style.display = 'block';
      } else {
        celebration.style.display = 'none';
      }
    }

    if (sources) {
      sources.innerHTML =
        '<h4><span class="section-icon">📚</span> Source Documents</h4>' +
        '<div class="source-grid">' +
        entry.sources.map(function (s) {
          return '<a href="' + s.href + '" target="_blank" rel="noreferrer" class="source-card">' +
            '<span class="source-icon">📄</span>' +
            '<span class="source-label">' + s.label + '</span>' +
            '<span class="source-arrow">↗</span>' +
          '</a>';
        }).join('') +
        '</div>';
    }

    overlay.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
  }

  function hideDetail() {
    var overlay = document.getElementById('nogoDetailOverlay');
    overlay.setAttribute('hidden', 'hidden');
    document.body.style.overflow = '';
  }

  // ── Init ──────────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    renderGallery('all');

    // Filter chips
    var filterToggle = document.getElementById('filterToggle');
    if (filterToggle) {
      filterToggle.addEventListener('click', function () {
        var bar = document.getElementById('filterBar');
        bar.hasAttribute('hidden') ? bar.removeAttribute('hidden') : bar.setAttribute('hidden', 'hidden');
      });
    }

    document.querySelectorAll('.filter-chip').forEach(function (btn) {
      btn.addEventListener('click', function () {
        expandedCardId = null; // Reset expanded state on filter change
        renderGallery(btn.getAttribute('data-filter'));
      });
    });

    // Detail overlay close
    var detailClose = document.getElementById('nogoDetailClose');
    if (detailClose) {
      detailClose.addEventListener('click', hideDetail);
    }

    var detailOverlay = document.getElementById('nogoDetailOverlay');
    if (detailOverlay) {
      detailOverlay.addEventListener('click', function (e) {
        if (e.target === this) hideDetail();
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') hideDetail();
    });
  });
}());
