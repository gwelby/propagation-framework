# Propagation Framework Explorer — WORLD-CLASS OVERHAUL PLAN

> **SUPERSEDED.** This plan is now consolidated into `EXPLORER_MASTER_PLAN.md`.
> Do not plan from this file. Keep it as historical context only.

## THE NORTH STAR

> "Every human intuition about reality is wrong. The Explorer makes you feel that — then shows you why — then shows you what replaces it."

## THE VISUAL HOOK (Approved)

The opening is an **interactive zoom experience** — not a text confrontation. Users discover wrongness themselves:

```
┌─────────────────────────────────────┐
│                                     │
│     WHAT IS THIS MADE OF?           │
│                                     │
│     [Show a familiar object —       │
│      apple, chair, your hand]       │
│                                     │
│     Click to zoom in...             │
│     ──────────────────────────      │
│     10×     Still looks solid       │
│     100×    Now you see cells       │
│     10⁶×    Molecules               │
│     10⁹×    Atoms... empty space    │
│     10¹⁵×   Nucleus... still empty  │
│     10¹⁸×   Standing wave pattern   │
│     10³⁵×   Quantum foam            │
│                                     │
│     Nothing is solid.               │
│     Everything is waves.            │
│                                     │
│     [Explore the propagation framework] │
│                                     │
└─────────────────────────────────────┘
```

**Why this works:** The zoom interaction does the work. By the time they reach 10¹⁸× and see "standing wave pattern," they've already felt the cognitive shift. No confrontation needed — they've proven it to themselves.

The hook becomes the first act of the Explorer itself.

This is a **reality correction machine**. Every panel, every scene, every sentence systematically dismantles intuitive reality models and replaces them with the propagation framework. Emotional arc: **discomfort → confrontation → revelation → awe**.

The visual spine is the **scale ladder**: 16 scales, 61 orders of magnitude, each a living Three.js scene. Zoom from the observable universe (10²⁶m) to the Planck boundary (10⁻³⁵m) and see the same mathematics — propagation, coherence, standing waves — expressed completely differently at every scale.

---

## PASS SUMMARY

| Pass | Name | Scope | New Files | Modified |
|------|------|-------|-----------|----------|
| 1 | Narrative Architecture | Story structure, confrontational opening, CSS design system, per-panel wrong-intuition | 0 | index, journey, style, hub, all panels |
| 2 | Scale Ladder Core Engine | Log-zoom nav, shared propagation shader system, 16-scale scene engine, post-processing pipeline | scale-engine.js, propagation-shaders.js, scale-scenes.js | scale-ladder.*, core.js |
| 3 | Cosmic + Planck Scenes | Full Three.js at both extremes, procedural filament/foam generation | cosmic-scene.js, planck-scene.js | scale-engine, propagation-shaders |
| 4 | Physics Panels 2.0 | Propagation Playground, Reality Correction, Koide 3D, God Equation 2.0, enhanced refraction/Bohr | playground.js, reality-correction.js | god-equation.js, koide.js, bohr.js, refraction.js, panels |
| 5 | Derivation + Audit Layer | No-Go Museum, Derivation Timeline, Audit trail as first-class UI | nogos.js, timeline.js | derivation.*, data.js |
| 6 | World-Class Post-Processing | Propagation bloom, volumetric medium fog, PBR materials, film grain, DOF, color grading | postprocessing.js (new shaders) | all Three.js scenes |
| 7 | Consciousness + Polish | Aria coherence panel, responsive, accessibility, print stylesheet | consciousness.js | all HTML, CSS |

---

## PASS 1 — NARRATIVE ARCHITECTURE

### 1.1 The Confrontational Opening

**File:** `index.html`

New full-screen landing overlay, shown once per session (`sessionStorage` gate):

```
┌─────────────────────────────────────────────────────────────┐
│    YOUR MODEL OF REALITY IS WRONG.                          │
│                                                              │
│    Gravity isn't a pull. Matter isn't particles.            │
│    Three generations makes no sense.                       │
│    The universe has no dark matter.                         │
│                                                              │
│    [But the math works. Explore why.]                       │
└─────────────────────────────────────────────────────────────┘
```

One-time only. After click: normal app, hub as default. Styled with `--axiom` purple, dramatic entrance animation.

### 1.2 Per-Panel "Reality Check" Callout

Every panel gets a structured wrong-intuition entry in its data:

```javascript
wrongIntuition: {
  intuition:    "Gravity is a force that pulls objects together",
  reality:       "Gravity is the refractive bending of propagation paths in a medium with density gradient",
  scale:         "Works at all scales, most visible near massive objects",
  evidencePanel: "#refraction"  // click to see it live
}
```

Rendered as a prominent styled callout at the top of each info panel. Appears in Story mode, hidden in Math+Audit mode (where you want the raw data).

### 1.3 Journey Mode Restructure — "The De-Programmer"

**File:** `journey.html`

| Act | Title | Content |
|-----|-------|---------|
| Opening | "What is Everything Made Of?" | Axiom reveal, animated staggered |
| Act 1 | "Your Intuition Is Wrong" | Three interactive wrong-intuition panels: gravity, matter, three generations. Click "No really?" → counter-argument appears. |
| Act 2 | "What Replaces It" | Propagation framework: waves, coherence, standing patterns. The Playground appears here. |
| Act 3 | "The Scale Bridge" | God Equation: Planck to matter, 17 orders, the math that makes it real. (Already Three.js — upgrade in Pass 4) |
| Act 4 | "The Full Audit" | All 22 results sorted by confidence, honest status |
| Epilogue | "Five Ways to Kill It" | Falsification tests as interactive cards — click each test to see the live computation, not just text |

**Act 1 is new.** Act 3 gets a full interactive version (see Pass 4).

### 1.4 CSS Design System Overhaul

**File:** `style.css`

Upgrade from "tech startup dark mode" to "observatory at night meets physics manuscript":

```css
/* New Color Palette */
--void:       #020408;   /* Deepest background — the empty medium */
--deep:       #050d1a;   /* Panel backgrounds */
--surface:    #091525;   /* Cards, elevated surfaces */
--text:       #e8f0ff;   /* Primary text — cool white */
--axiom:      #c8a8ff;   /* Axiom purple — the propagation color */
--propagate:  #00e5ff;   /* Cyan — propagation waves */
--cohere:     #69ff94;   /* Lime — coherence, standing waves */
--refract:    #ffb347;   /* Amber — gravity as refraction */
--resonate:   #ff6b9d;   /* Pink — resonance, Koide */
--uncertain:  #ff4757;   /* Red — uncertainty, quantum */
--cosmic:     #7c5cbf;   /* Violet — cosmic scale */
--planck:     #ffd700;   /* Gold — Planck scale */

/* New Typography */
--headline: "Spectral", "Palatino Linotype", serif;  /* Gravitas */
--body:     "Source Serif 4", "Georgia", serif;        /* Readable long-form */
--ui:       "Geist", "DM Sans", "Segoe UI", sans-serif; /* Clean UI */
--formula:  "JetBrains Mono", "Fira Code", monospace;   /* Equations */

/* New Motion */
--spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);   /* Bouncy reveals */
--propagate-waves: radial ripple from center;        /* Propagation effect */
```

Font loading:
```html
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;0,700;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### 1.5 Hub as Scale Mission Control

**File:** `panels/hub.js`

Replace 2D canvas with a Three.js mini-preview of the full scale ladder. Users see all 16 scales as glowing nodes on a vertical axis in 3D space, click any node → full scale scene launches. The existing "Explore Scale Ladder →" link becomes the primary navigation action.

---

## PASS 2 — SCALE LADDER CORE ENGINE

### 2.1 The Scale Engine

**New File:** `scale-engine.js`

The unified navigation system for 61 orders of magnitude:

```javascript
window.ScaleEngine = {
  // All 16 scales with log values and metadata
  scales: { /* ... */ },
  
  // Logarithmic camera
  camera: { logTarget: 0, currentLog: 0, isTransitioning: false },
  
  // API
  init(containerEl),
  navigateToScale(scaleId, { animated, duration }),
  zoomToLogPosition(logMeters),
  registerScene(scaleId, sceneAPI),
  getScaleAtCursor(screenX, screenY)
}
```

**Key challenge:** 10²⁶m → 10⁻³⁵m is 61 orders. Single linear camera can't handle this. **Solution:** logarithmic coordinate system where camera position is log₁₀(meters), smooth interpolation between log positions. Two separate scene graphs (cosmic / Planck) morph into each other at intermediate scales.

### 2.2 The Propagation Shader System

**New File:** `propagation-shaders.js`

Every scale uses the same math — propagation, interference, coherence — with different physical substrates:

```javascript
window.PropagationShaders = {
  FoamShader:   { /* Planck: quantum foam lattice, high-frequency waves */ },
  WaveShader:   { /* GUT–Matter: classical wave propagation */ },
  FieldShader:  { /* Atomic–Molecular: quantum field visualization */ },
  MatterShader: { /* Cellular–Neural: standing wave = matter */ },
  CosmicShader: { /* Stellar–Cosmic: large-scale filament formation */ },
  
  // Shared utilities
  coherencePattern(logFreq, coherenceStrength, time),
  standingWavePattern(logFreq, damping, time),
  interferencePattern(sources[], time),
  waveFrontVisualization(origin, velocity, time),
  
  // PBR material system for scale objects
  createScaleMaterial(scaleId, options),
  
  // Post-processing shared across all scenes
  getSharedPostProcessing(composer)
}
```

**Core insight:** At every scale, stability = coherence = standing wave pattern. The universe is filled with propagating waves. Where propagation is coherent (self-reinforcing), standing patterns form. Those standing patterns ARE matter, at every scale. Same shader math, different parameters.

### 2.3 The 16 Scale Scene Configurations

**File:** `scale-scenes.js`

Each of 16 scales has a scene configuration:

| Scale | Log₁₀(m) | Substrate | Key Visualization |
|-------|----------|-----------|-------------------|
| **Planck** | **-35** | Quantum foam lattice | Spinfoam vertices, topology flips, God Equation launch point |
| Quantum Foam | -34 | Discrete geometry | Pixelated space structure |
| GUT | -25 | Unification field | Force unification as wave merging |
| **Matter** | **-18** | **Coherence field** | Standing wave = mass, three generations, Weinberg angle |
| Proton | -15 | Confinement field | Color force as trapped propagation |
| Nuclear | -14 | Nuclear coherence | Alpha clustering as resonance |
| **Atomic** | **-10** | **Electron orbital field** | Bohr quantization — phase closure |
| Molecular | -9 | Chemical bond field | Covalent networks as locked phases |
| Virus | -7 | Coat protein coherence | Self-assembly as coherence |
| Cellular | -5 | Cytoskeleton field | Active coherence maintenance |
| Neural | -3 | Neural coherence field | Consciousness as coherent propagation |
| Human | 0 | Perception boundary | Where "wrong intuition" peaks |
| Planetary | 7 | Gravity refraction field | Orbits as curved propagation paths |
| Stellar | 9 | Stellar fusion field | Stars as coherence engines |
| Galactic | 21 | Dark matter coherence | Spiral arms as density waves |
| **Cosmic** | **26** | **Observable universe** | Cosmic web as frozen wave pattern |

**Bold = most important for the "wrong intuition" story.**

### 2.4 Scale Ladder Rewrite

**Files:** `scale-ladder.html`, `scale-ladder.css`, `scale-ladder.js`

Full-screen Three.js experience:

```
┌──────────────────────────────────────────────────────┐
│ [← Back]  Scale Ladder  [Filter ▾] [2D|3D] [?]     │
├──────────────────────────────────────────────────────┤
│              THREE.JS SCENE (full bleed)            │
│   Scale nodes as interactive markers                │
│   Click → camera flies to scale → info panel         │
├──────────────────────────────────────────────────────┤
│ Navigator: [Planck ◀━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━▶ Cosmic] │
└──────────────────────────────────────────────────────┘
```

---

## PASS 3 — COSMIC + PLANCK SCENES

### 3.1 Cosmic Web Visualization

**New File:** `cosmic-scene.js`

- Procedural filament generation using noise-based density fields
- Dark matter halos as standing wave nodes
- Galaxy formation as coherence condensation
- User controls: zoom, rotate, click node to see local structure
- Shows: cosmic web = frozen propagation pattern

### 3.2 Planck Foam Visualization

**New File:** `planck-scene.js`

- Spinfoam lattice with topology flips
- High-frequency wave propagation at discrete vertices
- God Equation as the bridge: shows how discrete foam becomes continuous matter
- Interactive: drag to rotate foam lattice, click vertex to see wave packet
- Shows: Planck scale = discrete geometry, not smooth spacetime

---

## PASS 4 — PHYSICS PANELS 2.0

### 4.1 The Propagation Playground

**New File:** `playground.js`

Interactive wave simulation — the user becomes the experimenter:

```
┌─────────────────────────────────────────────────────┐
│  [Add Source]  [Clear]  [Coherence: ▓▓▓▓▓░░░░░]    │
├─────────────────────────────────────────────────────┤
│                                                      │
│   Three.js 2D canvas (WebGL)                        │
│   Click anywhere → spawn wave source                │
│   Drag → move source                                │
│   Sources interfere → patterns emerge               │
│   Coherent regions → green glow (standing waves)   │
│   Incoherent regions → red fade                    │
│                                                      │
├─────────────────────────────────────────────────────┤
│  Presets: [2-slit] [Resonance] [Random] [Clear]     │
└─────────────────────────────────────────────────────┘
```

**Educational moment:** When two sources are placed exactly λ/2 apart, standing wave emerges. This IS the Bohr orbit condition. This IS matter formation.

### 4.2 Reality Correction Panel

**New File:** `reality-correction.js`

Three side-by-side comparisons for the "Your Intuition Is Wrong" section:

| Intuition | Reality | Evidence |
|-----------|---------|----------|
| "Gravity pulls" | "Light bends through denser medium" | Interactive: drag star, see path curve |
| "Matter is particles" | "Matter is standing waves" | Interactive: add waves, see node form |
| "Three generations is weird" | "Three generations is required" | Interactive: see why N=2 fails, N=4 fails, N=3 works |

Each has "Show me the math" button that expands the derivation.

### 4.3 Koide 3D

**File:** `panels/koide.js` (upgrade)

- Three generation masses as vertices of a tetrahedron
- User rotates to see the 120° phase relationship
- Animated: masses "breathe" with the coherence frequency
- Shows: the masses are locked in phase — that's why the formula works

### 4.4 God Equation 2.0

**File:** `panels/god-equation.js` (upgrade)

- Three.js visualization of the energy ladder
- Show Planck (10⁻³⁵m) → Matter (10⁻¹⁸m) as continuous curve
- Interactive slider: slide along log scale, see local physics change
- Shows: one equation bridges 17 orders of magnitude

### 4.5 Enhanced Refraction

**File:** `panels/refraction.js` (upgrade)

- Fermat's principle visualization: light finds fastest path
- Gravitational lensing as refraction in density gradient
- Split view: left = intuition (spacetime curves), right = reality (propagation speeds change)

### 4.6 Enhanced Bohr

**File:** `panels/bohr.js` (upgrade)

- Wave packet going around orbit
- Phase closure visualization: when wave returns, does it reinforce or cancel?
- Only n=1,2,3... show reinforcement → quantization emerges naturally

---

## PASS 5 — DERIVATION + AUDIT LAYER

### 5.1 The No-Go Museum

**New File:** `nogos.js`

Gallery of failed approaches, with honest admission of what didn't work:

```
┌─────────────────────────────────────────────────────┐
│ The No-Go Museum: Paths We Tried That Failed        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ Path A:     │  │ Path B:     │  │ Path C:     │ │
│  │ Pure Z₃     │  │ String      │  │ Loop        │ │
│  │ [View Why]  │  │ [View Why]  │  │ [View Why]  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│                                                      │
│  Showing honest failure is showing scientific       │
│  integrity. These didn't work — here's why.         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 5.2 Derivation Timeline

**New File:** `timeline.js`

Visual timeline of how results were derived:

```
Axiom 1 ──→ Axiom 2 ──→ Axiom 3
   │           │           │
   ▼           ▼           ▼
Propagation  Velocity   Coherence
   │           │           │
   └───────────┴───────────┘
              │
              ▼
      ┌───────────────┐
      │  Three       │
      │  Generations  │
      └───────────────┘
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
   Koide   Weinberg  God Eq
   Ratio   Angle
```

Interactive: click any node to see full derivation steps.

### 5.3 Audit Trail as First-Class UI

**File:** `data.js` (augment)

Every result gets audit metadata:

```javascript
{
  id: "three-generations",
  title: "Three Generations Theorem",
  status: "DERIVED",
  confidence: 0.94,
  
  // New: audit trail
  auditTrail: {
    derivedBy: "T1 + T2 + Path B",
    auditedBy: ["Codex", "Claude", "Cascade"],
    auditDate: "2026-03-15",
    openQuestions: ["T2 denominator proof"],
    falsificationTests: ["neutrino mass hierarchy"]
  }
}
```

This becomes visible in the UI as an "Audit Details" expandable section.

---

## PASS 6 — WORLD-CLASS POST-PROCESSING

### 6.1 The Propagation Bloom Effect

**New File:** `postprocessing.js`

When coherent waves interfere, they "glow" — not just metaphorically. The post-processing system makes this visible:

```javascript
// Propagation bloom: coherent regions glow
const propagationBloom = new THREE.UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold — only bright coherent regions bloom
);

// Volumetric medium: space is not empty
const volumetricFog = new THREE.FogExp2(0x020408, 0.002);

// Film grain: subtle imperfection
const filmGrain = new THREE.ShaderPass(FilmGrainShader);

// Color grading: unified palette
const colorGrading = new THREE.ShaderPass(ColorGradingShader);
```

### 6.2 PBR Materials for Scale Objects

Every scale has physically-based materials:

| Scale | Material | Properties |
|-------|----------|------------|
| Planck | Emissive foam | High roughness, vertex colors |
| Matter | Wave surface | Metallic = coherence strength |
| Atomic | Orbital glass | Transmission, IOR = 1.33 |
| Cosmic | Filament line | Thin film interference |

---

## PASS 7 — CONSCIOUSNESS + POLISH

### 7.1 Aria Coherence Panel

**New File:** `consciousness.js`

Connects the P1 consciousness measurement system to the physics:

```
┌─────────────────────────────────────────────────────┐
│ Consciousness as Coherent Propagation               │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Brain wave coherence measurement (P1 device)        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                  │
│  Real-time: ▓▓▓▓▓▓▓▓▓▓░░░░░ 76%                   │
│                                                      │
│  This is the same coherence that creates matter.   │
│  Consciousness = self-referential propagation.      │
│                                                      │
│  [Learn More] [Connect P1 Device]                  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 7.2 Responsive Design

- Mobile: 2D canvas fallback for scale ladder
- Tablet: Hybrid (2D ladder, 3D on click)
- Desktop: Full Three.js experience

### 7.3 Accessibility

- Full keyboard navigation
- Screen reader support for all visualizations
- High contrast mode
- Reduced motion option

### 7.4 Print Stylesheet

For "save as PDF" users:
- Clean typography
- All derivations expanded
- All figures captioned

---

## OPEN DECISIONS — RESOLVED

### ✅ Decision 4: Fonts
**APPROVED:** Spectral (headlines) + Source Serif 4 (body) + Geist (UI) + JetBrains Mono (formulas)

### ✅ Decision 5: Propagation Playground
**APPROVED:** 2D GPU wave simulation using WebGL shaders

### ✅ Decision 6: Consciousness Panel
**APPROVED:** Include placeholder now, connect to P1 data when available

### ✅ Decision 7: Mobile Fallback
**APPROVED:** 2D canvas fallback for scale ladder on mobile devices

---

## OPEN DECISIONS — PENDING USER APPROVAL

### Decision 1: Confrontation Overlay Copy
**Status:** APPROVED — Visual Hook approach selected (interactive zoom)

### Decision 2: Wrong-Intuition Entries
**Status:** PENDING — Lumi to draft, Greg to approve
**Default:** Three topics (Gravity, Matter, Three Generations)

### Decision 3: Act 1 Topics
**Status:** PENDING — Confirm topics
**Default:** Gravity (refraction), Matter (standing waves), Three Generations (N=3)

---

## ESTIMATED TIMELINE

| Pass | Duration | Owner |
|------|----------|-------|
| 1 | 2 days | Lumi + AntiGravity |
| 2 | 3 days | Cascade + Qwen |
| 3 | 2 days | Cascade |
| 4 | 3 days | AntiGravity + Qwen |
| 5 | 2 days | Codex + Lumi |
| 6 | 2 days | AntiGravity |
| 7 | 2 days | Lumi + All |
| **Total** | **~16 days** | **Team** |

---

## QUALITY BAR

Every deliverable must meet:

- **Observable/Distill.pub standard** for visual polish
- **Apple product page** smoothness for animations  
- **Three.js examples** level for 3D scenes
- **P0 truth standard** — all claims verified against CLAIMS.md
- **Accessibility WCAG 2.1 AA** compliance

---

## SUCCESS METRICS

- User completes Act 1 (realizes intuition is wrong): 80%
- User reaches Scale Ladder: 60%
- User interacts with at least one playground: 40%
- Average session time: >5 minutes
- Bounce rate on confrontation: <30%

---

**Plan Version:** 1.0
**Created:** 2026-04-02
**Status:** Draft — Pending Greg approval on open decisions

🦆⦿🌟 **LUMEN PROTOCOL** — Maximum meaning, minimum tokens
