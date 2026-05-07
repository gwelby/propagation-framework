# World-Class Explorer — Implementation Brief
*The single source of truth for rebuilding the Propagation Framework Explorer into a cognitive instrument.*
*Date: 2026-05-05*
*Status: ACTIVE — Phase 1 (Observatory Shell) ready for execution*

---

## 0. The Vision (One Sentence)

The user should not feel like they are browsing a site. They should feel like they are operating an instrument that lets them move between scale, claim, proof, failure, and experiment.

---

## 1. Truth Architecture (Codex owns this)

### 1.1 Data Graph Schema

Replace hand-coded UI per page with a generated object graph. Source of truth: `CLAIMS.md`, `definitions/README.md`, `ACTIVE_ISSUES.md`, audit files, no-go files.

```javascript
// data.graph.js — generated, not hand-written
window.PFGraph = {
  definitions: [
    {
      id: 'def-medium',
      title: 'The Medium',
      status: 'CANONICAL',
      summary: 'The minimal causal-coherence structure required for propagation.',
      canonicalSource: 'definitions/medium.md',
      dependencies: [],
      falsifiers: ['Any propagation model that requires a pre-existing background spacetime'],
      claimsDependent: ['claim-gr-refraction', 'claim-bohr']
    }
  ],

  claims: [
    {
      id: 'claim-koide-q',
      title: 'Koide Q = 2/3 as Geometric Identity',
      status: 'DERIVED',
      confidence: 0.95,
      summary: 'For three equal-strength resonance modes in a propagation medium, the mass ratio is fixed by geometry.',
      formula: 'Q(N) = 2N/(2N+3) → Q(3) = 2/3',
      scope: 'Charged-lepton sector only. Neutrinos predicted to deviate.',
      falsifier: 'Q deviates by >0.1% from 2/3 for charged leptons.',
      sources: ['derivations/koide_geometric_identity.md'],
      derivation: ['axiom3', 'axiom3b'],
      noGoRoutes: [],
      openBridges: ['phase-selector-delta-2-9']
    }
  ],

  derivations: [
    {
      id: 'deriv-koide-q',
      claimId: 'claim-koide-q',
      steps: [
        { id: 's1', title: 'Resonance Modes', dependsOn: ['axiom3'] },
        { id: 's2', title: 'Mass as Resistance', dependsOn: ['def-matter'] },
        { id: 's3', title: 'Geometric Sum Rule', dependsOn: ['s1', 's2'] },
        { id: 's4', title: 'Generation Count', dependsOn: ['s3'] }
      ],
      assumptions: ['Three equal-strength modes', 'N=3 from topology (CONDITIONAL)'],
      noGoRoutes: [
        { route: 'harmonic-series', result: 'FAILED', cv: 0.94 }
      ],
      openBridges: ['phase-selector-delta-2-9']
    }
  ],

  noGos: [
    {
      id: 'nogo-harmonic',
      targetClaim: 'claim-particle-masses',
      failedAssumption: 'Particle masses follow harmonic ratios',
      test: 'Monte Carlo simulation',
      result: 'FAILED — CV = 0.94 (essentially random)',
      lesson: 'The framework that survived contact with data is the only framework worth keeping.'
    }
  ],

  experiments: [
    {
      id: 'exp-eeq-t020',
      claimId: 'claim-consciousness',
      script: 'protocols/muse_insight_protocol.md',
      observed: null,
      expected: '≥7/10 insight events with >50% EEG variance increase',
      verdict: 'PRE-REGISTERED'
    }
  ]
};
```

### 1.2 Truth Validation Rules (hard constraints)

1. No page can display `DERIVED`, `CANONICAL`, or confidence values not sourced from `data.graph.js`.
2. Every result must have a falsifier and source trail.
3. Every canonical term must link to its definition file.
4. No conditional claim can read as derived in any UI copy.
5. No empirical signal can read as a theorem.

### 1.3 Smoke Tests

- Screenshots at 1440px, 1024px, and mobile must look intentionally composed.
- No route should present a mostly empty viewport.
- First screen must communicate the framework, not just a slogan.
- All counters must show real values, never zero on first load.

---

## 2. Observatory Homepage (AntiGravity owns this)

### 2.1 What Replaces the Hero

Current: large centered sentence "Everything is propagation", one paragraph, one button.

New: a live instrument surface.

```
┌─────────────────────────────────────────────────────────────┐
│  [Scale: ──────────────────●──────────────────]  [Story|Audit|Math]  🔍  🔊  📋 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    ┌─ Scale Rail (vertical, log)                            │
│    │                                                        │
│    │  ● Cosmic  (1e26 m)    ←──── propagation front       │
│    │  ● Galactic (1e21 m)                                  │
│    │  ● Stellar  (1e9 m)                                   │
│    │  ● Planetary (1e7 m)                                  │
│    │  ● Human    (1 m)  ←──── YOU ARE HERE                │
│    │  ● Neural   (1e-2 m)                                   │
│    │  ● Cellular (1e-5 m)                                  │
│    │  ● Atomic   (1e-10 m)                                  │
│    │  ● Nuclear  (1e-15 m)                                 │
│    │  ● Proton   (1e-15 m)                                  │
│    │  ● Matter   (1e-18 m)                                  │
│    │  ● GUT      (1e-25 m)                                  │
│    │  ● Quantum Foam (1e-33 m)                              │
│    │  ● Planck   (1e-35 m)                                  │
│    │  ● Axiomatic Root                                      │
│    └─                                                        │
│                                                             │
│    ┌─ Live Claim Stack ─────────────────────────┐          │
│    │  19 Canonical Definitions                  │          │
│    │  25 Claims (3 DERIVED / 5 CONDITIONAL / ...)│          │
│    │  13 No-Go Routes (documented failures)     │          │
│    │  6 Active Bridges (open problems)           │          │
│    └──────────────────────────────────────────────┘          │
│                                                             │
│    ┌─ Featured Proof: Koide Resonance Q = 2/3 ──┐          │
│    │  Measured: 0.666659  Theory: 0.666667      │          │
│    │  Status: DERIVED  Confidence: 0.95           │          │
│    │  [View Derivation] [View Audit]             │          │
│    └──────────────────────────────────────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 The Propagation Wave

A persistent animated element: a luminous cyan wave front that propagates down the scale rail. When it reaches a scale, that scale briefly illuminates and plays its sonic signature (from the existing audio engine). This is not decoration. It communicates Axiom 1 visually: everything propagates.

### 2.3 Color Semantics (strict)

| Color | Meaning | Use |
|-------|---------|-----|
| Cyan (#00cfff) | Propagation / causal movement | Wave fronts, causal links |
| Green (#44ff88) | Coherence / stable derived path | DERIVED claims, closed proofs |
| Amber (#ffdd55) | Conditional / open bridge | CONDITIONAL claims, unfinished steps |
| Red (#ff5577) | No-go / falsifier / audit strike | Failed routes, falsifiers |
| Gold (#ffd700) | Empirical anchor / measurement | Experimental results |
| White (#e8f0ff) | Canonical definition text | Definitions, theorems |
| Purple (#c8a8ff) | Axiom / root (rare) | The three axioms only |

Purple must not dominate. It is a rare accent.

### 2.4 Typography System

Already partially implemented. Use:
- **Spectral** (serif) — theorem titles, proof statements, block quotes
- **Geist / DM Sans** (sans) — controls, metadata, labels
- **JetBrains Mono** — equations, receipts, scripts, audit excerpts

The site should look like a lab notebook became an observatory.

---

## 3. Persistent Command Surface (AntiGravity owns this)

One toolbar, visible on every workspace:

```
[≡ Sidebar]  PF Explorer  [Scale: ───────●───────]  [Story | Audit | Math]  [🔍 Search]  [🔊 Audio]  [📋 Source]
```

**Story mode:** Narrative explanation, accessible to non-specialists. "What if the universe is just propagation?"

**Audit mode:** Hostile review. "Here is what survives the audit. Here is the precise hidden step. Here is what would close it."

**Math mode:** Equations, derivations, proof boxes. LaTeX-rendered via MathJax or KaTeX.

The toggle must persist across workspaces and be reflected in the URL (`?mode=audit`).

---

## 4. Workspaces (AntiGravity owns shell, Claude owns copy, Lumi owns narrative)

### 4.1 Observatory (entry)
- Scale rail + claim stack + featured proof
- Default mode: Story

### 4.2 Proof Atlas (replaces derivation.html)
- Full-screen force-directed graph
- Left rail: claim clusters by category (Forces, Generations, Koide, etc.)
- Center: interactive graph with readable labels
- Right inspector: claim details, derivation steps, open bridges, no-go overlays
- Filter by status: DERIVED, CONDITIONAL, ARGUED, EMPIRICAL, OPEN

### 4.3 Definition Lattice (new)
- 19 canonical definitions as a semantic graph
- Click a term → canonical source, dependents, falsifiers
- Search across all definitions

### 4.4 No-Go Museum (new — the most distinctive voice)
- Failed routes are first-class evidence
- Each no-go is a full card: what was tried, why it failed, what was learned
- Historical parallels: steady-state cosmology, phlogiston, etc.
- Tagline: "The framework that survived contact with data is the only framework worth keeping."

### 4.5 Experiment Bench (new)
- Sandbox scripts, verification outputs, benchmark status
- Live error metrics (deflection, perihelion, Shapiro)
- Heatmap of quantitative verification
- Downloadable data

### 4.6 Scale Ladder (replaces scale-ladder.html)
- Must not start empty — default to Human with context
- 16 scales from Planck (-35) to Cosmic (+26)
- Camera flights between scales (transition engine already exists)
- Per-scale 3D scene (scene files already exist: atomic, cellular, cosmic, etc.)
- Audio crossfade between scale signatures (audio engine already exists)
- Claims tagged to their scale magnitude

### 4.7 Story Journey (existing journey.html, rebuilt as default entry for non-specialists)
- 8-minute guided experience
- Opening → Act I (Bohr) → Act II (Generations) → Act III (God Equation) → Act IV (Scoreboard) → Epilogue (Falsification)
- Every dramatic sentence backed by `data.graph.js`

---

## 5. Audio Integration (AntiGravity wires existing audio-engine.js)

The audio engine already defines sonic signatures for each scale. Wire it to:
- Scale ladder transitions (crossfade between scales)
- Claim status changes (green chime for DERIVED, amber tone for CONDITIONAL, red strike for no-go)
- Propagation wave passing a scale node
- Hover on derivation graph nodes

Mute state persists in localStorage. Respect `prefers-reduced-motion`.

---

## 6. Performance Budget (AntiGravity owns)

Already partially implemented in `performance-engine.js`.

| Metric | Target |
|--------|--------|
| First paint | < 1.5s |
| Interactive | < 3s |
| FPS | 60fps desktop, 45fps mobile |
| Memory | < 200MB |
| Bundle size | < 500KB initial, lazy-load scenes |
| Mobile | Usable and intentional |

Use existing quality tiers: high / medium / low / minimal.
Use existing LOD system, InstancedMesh, frustum culling, Web Workers.

---

## 7. Accessibility (AntiGravity owns)

Already partially implemented. Maintain:
- ARIA labels on all controls
- Screen reader announcements for scale changes and claim navigation
- Keyboard navigation for all workspaces
- `prefers-reduced-motion` disables camera flights and particle effects
- High contrast mode support

---

## 8. Agent Task Assignments

| Agent | Task | Deliverable | Acceptance |
|-------|------|-------------|------------|
| **AntiGravity** | Observatory shell, persistent command surface, Definition Lattice, No-Go Museum, rebuilt Scale Ladder, Proof Atlas layout | Working HTML/JS/CSS for all workspaces | Screenshots at 1440/1024/mobile look composed. No empty viewports. |
| **Claude** | Copy for Story/Audit/Math modes, claim compression (claim/boundary/derived/failed/falsifier/bridge), Definition Lattice descriptions | Text content in `content/` or inline in workspace files | Physicist can identify proved vs not-proved in 30s. Non-specialist can explain propagation after first route. |
| **Codex** | `data.graph.js` schema, truth validation script, smoke tests, acceptance gates | `data.graph.js`, `validate-truth.js`, `smoke-test.js` | No DERIVED label without source. Every falsifier present. All screenshots pass. |
| **Lumi** | Rebuilt journey narrative, presentation mode, cinematic arc | `journey.html` v2, `present.js` | Journey feels memorable. Every dramatic sentence has audit-safe counterpart. |
| **Qwen** | Literature connections for each claim, historical no-go parallels | Research notes integrated into Audit mode | Each claim has closest standard-physics parallel named. Each no-go has historical parallel. |
| **Hermes** | Dependency graph maintenance, CLAIMS.md sync | Automated sync script | No orphan claim. No dead link. Open bridges visible and named. |
| **Greg (you)** | Visual direction approval, priority decisions, final sign-off | Decisions logged in `DECISIONS.md` | — |

---

## 9. Implementation Order

### Phase 0 — Stabilize (this week)
- [ ] Codex: Generate `data.graph.js` from existing sources
- [ ] Codex: Write `validate-truth.js` script
- [ ] AntiGravity: Rebuild homepage as Observatory (scale rail + claim stack)
- [ ] AntiGravity: Persistent command surface (Story/Audit/Math toggle)

### Phase 1 — Proof Atlas (next week)
- [ ] AntiGravity: Rebuild derivation graph for legibility
- [ ] Claude: Write Audit-mode copy for all claims
- [ ] AntiGravity: Left rail claim clusters + right inspector

### Phase 2 — Scale & Definition (week after)
- [ ] AntiGravity: Rebuild Scale Ladder with real content
- [ ] AntiGravity: Wire transition engine + audio engine to scale changes
- [ ] AntiGravity: Build Definition Lattice route
- [ ] Claude: Write Definition Lattice descriptions

### Phase 3 — No-Go Museum & Experiment Bench (following week)
- [ ] AntiGravity: Build No-Go Museum
- [ ] AntiGravity: Build Experiment Bench with live metrics
- [ ] Qwen: Research historical no-go parallels
- [ ] Lumi: Final honesty pass on all narrative

### Phase 4 — Polish & Ship (final week)
- [ ] Lumi: Presentation mode
- [ ] AntiGravity: Performance budget pass
- [ ] Codex: Full smoke test suite
- [ ] AntiGravity: Accessibility pass
- [ ] All: Screenshot/social assets

---

## 10. Acceptance Gates (All must pass)

1. **First screen test:** Within 5 seconds, a new viewer understands: reality is modeled as propagation through a structured Medium.
2. **Physicist test:** Within 30 seconds, a technical viewer can see which claims are derived, conditional, empirical, or no-go.
3. **Truth test:** Every visible status is sourced from `data.graph.js` and source files.
4. **Instrument test:** Every major control changes understanding, not just decoration.
5. **Scale test:** The site makes 61 orders of magnitude feel navigable, not abstract.
6. **Failure test:** No-go routes are as visible as successes.
7. **Mobile test:** The experience is usable and intentional on a phone.
8. **Screenshot test:** Every primary route has a composed above-the-fold screenshot.
9. **Audio test:** Scale transitions have smooth sonic crossfades.
10. **Performance test:** 60fps on iPhone 12, 45fps on iPhone X.

---

## 11. Files Already Built (Do Not Rebuild)

These exist and are excellent. Wire them into the new shell:
- `audio-engine.js` — Spatial audio with Tone.js, 16 scale signatures
- `performance-engine.js` — Device tiering, LOD, InstancedMesh, culling, workers
- `transition-engine.js` — Camera flights, motion blur, crossfade between scales
- `scale-engine.js` — 16-scale logarithmic ladder, Three.js scenes
- `derivation-3d.js` — Three.js force-directed graph (degrades to 2D honestly)
- `touch-controller.js` — Mobile touch support
- `service-worker.js` — PWA offline support
- `journey.html` / `journey.js` / `journey.css` — Narrative experience
- `comparison.html` / `comparison.js` / `comparison.css` — Framework comparison
- All `*-scene.js` files — Per-scale 3D scenes

---

*This brief is the contract. Each agent picks up their section and executes. Codex validates. Greg approves. The Explorer becomes an instrument.*
