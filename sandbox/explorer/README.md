# Propagation Framework Explorer

Static interactive atlas for the current Propagation Framework sandbox.

## What Ships

- `sandbox/explorer/index.html` opens directly in a browser with no build step.
- `sandbox/explorer/journey.html` — **NEW**: 8-minute guided narrative experience
- `CLAIMS.md` drives audited badges and totals.
- `UNDERSTAND.md` extends placement and explanatory copy.
- Story mode gives the visual argument first.
- Math + Audit mode exposes formulas, source trails, falsifiers, and conditional gaps.

Current curated snapshot:

- `23` visible results
- `22` audited results
- `1` unsynced item kept visible but excluded from totals
- `7` deep computation panels plus the dashboard
- **NEW**: Journey Mode with 4 acts + epilogue

## Routes

### Reference Explorer (index.html)

- `#hub` Scale Stack navigator
- `#refraction` Gravity as Optical Geometry
- `#generations` Why Exactly Three
- `#koide` The Koide Triangle
- `#weinberg` The Weinberg Angle
- `#god-equation` The God Equation
- `#bohr` Bohr-like Circular-Eikonal Spectrum
- `#dashboard` Audit wall

### Journey Mode (journey.html)

A guided 8-minute narrative experience:

- **Opening**: Three axioms appear — "What if the universe is just... propagation?"
- **Act I**: Circular-eikonal Bohr-like spectrum (interactive electron placement)
- **Act II**: Conditional N=3 lock with the live Q(N) algebra
- **Act III**: God Equation audit snapshot (N,D sliders around the conditional physical point)
- **Act IV**: Full scoreboard + framework comparison table
- **Epilogue**: Falsification wall (6 ways to kill the framework)

**Best for**: First-time visitors, presentations, sharing with physicists

### Framework Comparison (comparison.html) — NEW

Side-by-side comparison of physics frameworks:
- Interactive parameter counter (PF: 3, SM: 19, String: 10^500)
- Head-to-head table (10 metrics)
- Falsifiability matrix (how to kill each framework)
- Scale coverage visualizer (repo scope view across scales)
- The Delta: 6 key PF differences

**Best for**: Context for physicists, "why should I care" question

### Derivation Chains (derivation.html) — NEW

Interactive visualization of how results derive from axioms:
- Click-to-explore node graph (axioms → intermediate → results)
- Color-coded by confidence level (DERIVED, CONDITIONAL, etc.)
- Detail panel with formulas and derivation paths
- Zoom/pan controls for exploring the full graph
- Statistics dashboard (total nodes, average confidence, longest chain)

**Best for**: Understanding the logical structure, verifying derivation paths

## Wave 2 Additions

- Dashboard filter chips are stable and re-render in place.
- Dashboard cards now support inline expandable audit sections for falsifiers and sources.
- Hub panel routing uses the runtime result-to-panel mapping, not local inference.
- Hub pointer behavior is normalized for desktop and touch-capable browsers.
- The God Equation panel now includes:
  - dependency chain view
  - explicit gap cards for A, B, and C
  - toy visuals for locality vs Markovity and covariance vs factorization
- Narrow layouts default the evidence drawer to collapsed overlay behavior.

## Architecture

```text
sandbox/explorer/
├── index.html          ← Reference explorer (8 panels + dashboard)
├── journey.html        ← 8-minute narrative experience
├── comparison.html     ← Framework comparison (PF vs SM vs String)
├── derivation.html     ← NEW: Interactive derivation chain visualizer
├── style.css           ← Dark theme with glowing accents
├── core.js             ← Math utilities, rendering helpers
├── data.js             ← Results from CLAIMS.md
├── journey.css         ← Journey-specific styles
├── journey.js          ← Journey narrative flow + animations
├── comparison.css      ← Comparison-specific styles
├── comparison.js       ← Comparison interactive logic
├── derivation.css      ← NEW: Derivation visualizer styles
├── derivation.js       ← NEW: Interactive graph logic
├── panels/
│   ├── hub.js
│   ├── refraction.js
│   ├── generations.js
│   ├── koide.js
│   ├── weinberg.js
│   ├── god-equation.js
│   ├── bohr.js
│   └── dashboard.js
└── README.md
```

## Truth Policy

- `sandbox/sandbox_results.md` remains the top truth source for what actually held or failed.
- `CLAIMS.md` defines explorer audit status.
- `data.js` is the Explorer truth layer derived from `CLAIMS.md`; Journey and Comparison must source PF claims from it rather than hardcoding stronger copy.
- `UNDERSTAND.md` may extend explanation, but it does not silently promote claims.
- Unsynced items are visible context, not audited claims.

## Key Behavior

### Story vs Audit

- Story mode favors intuition, geometry, and scale placement.
- Math + Audit mode surfaces formulas, falsifiers, source links, and gap explanations.

### Evidence Drawer

- Wide layouts keep the drawer visible.
- Narrow layouts default the drawer closed.
- On narrow layouts the drawer opens as an overlay, not a permanent third column.

### Dashboard

- Search covers title, formula, summary, and falsifier text.
- Status filters combine with search.
- Unsynced items remain in a separate section and do not affect audited totals.

### God Equation

The panel intentionally keeps the current repo verdict:

- numerical anchor at `(N=3, D=3)` is shown from the current claim snapshot
- status remains `CONDITIONAL`
- the missing bridges are made explicit rather than hidden:
  - Gap A: locality to first-order Markov coarse walk
  - Gap B: operator closure / primitive 3-step dynamics
  - Gap C: full `H_prod` factorization

## Verification

Recommended manual check:

1. Open `sandbox/explorer/index.html` directly in Chrome or Edge.
2. Visit all routes.
3. Toggle Story / Math + Audit.
4. On `#dashboard`, change filters repeatedly and verify the chip row stays at 7 controls, including `Partial`.
5. On `#god-equation`, confirm the three gap cards and dependency chain appear in audit mode.
6. On a narrow viewport, confirm the drawer starts collapsed and opens as an overlay.

Recommended syntax check:

```powershell
node --check core.js
node --check data.js
node --check panels\dashboard.js
node --check panels\hub.js
node --check panels\god-equation.js
```

Automated browser smoke tests can use a temporary local loopback server. The app itself is still designed to work from `file://`.

## Planned, Not Yet Shipped

- Belt trick / Dirac string visualization in the Generations panel
- Refraction error metrics and heatmap overlays
- Koide / Weinberg running-link visual
- Bohr spectral-line diagram
- richer keyboard accessibility

## Scope Guard

This explorer is a curated static snapshot. It does not parse markdown at runtime, does not upgrade claims, and does not replace the underlying derivation files or sandbox scripts.
