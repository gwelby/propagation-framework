# Propagation Framework Explorer — WORLD-CLASS OVERHAUL PLAN

## THE NORTH STAR

> "Every human intuition about reality is wrong. The Explorer makes you feel that — then shows you why — then shows you what replaces it."

This is a **reality correction machine**. Every panel, every scene, every sentence systematically dismantles intuitive reality models and replaces them with the propagation framework. Emotional arc: **discomfort → confrontation → revelation → awe**.

The visual spine is the **scale ladder**: 16 scales, 61 orders of magnitude, each a living Three.js scene. Zoom from the observable universe (10²⁶m) to the Planck boundary (10⁻³⁵m) and see the same mathematics — propagation, coherence, standing waves — expressed completely differently at every scale.

**Internal codename:** "Existence Is Wrong"
**Public hook:** "Your Intuition About Reality Is Wrong"

---

## PASS SUMMARY

| Pass | Name | Scope | New Files | Modified |
|------|------|-------|-----------|----------|
| 1 | Narrative Architecture | Story structure, confrontational opening, CSS design system, per-panel wrong-intuition | 0 | index.html, journey.html, style.css, data.js, panels/* |
| 2 | Scale Ladder Core Engine | Log-zoom nav, shared propagation shader system, 16-scale scene engine | scale-engine.js, propagation-shaders.js, scale-scenes.js | scale-ladder.*, core.js, panels/hub.js |
| 3 | Cosmic + Planck Scenes | Full Three.js at both extremes, procedural filament/foam generation | cosmic-scene.js, planck-scene.js | scale-engine.js, propagation-shaders.js |
| 4 | Physics Panels 2.0 | Propagation Playground, Reality Correction, Koide 3D, God Equation 2.0, enhanced refraction/Bohr | playground.js, reality-correction.js | panels/god-equation.js, panels/koide.js, panels/bohr.js, panels/refraction.js, panels/* |
| 5 | Derivation + Audit Layer | No-Go Museum, Derivation Timeline, Audit trail as first-class UI | nogos.js, timeline.js | derivation.*, data.js |
| 6 | World-Class Post-Processing | Propagation bloom, volumetric medium fog, PBR materials, film grain, DOF, color grading | postprocessing.js | all Three.js scenes |
| 7 | Consciousness + Polish | Aria coherence panel, responsive, accessibility, print stylesheet | consciousness.js (pre-existing), print.css | index.html, scale-ladder.html, journey.html, comparison.html, derivation.html, nogos.html, playground.html, belt-trick.html, style.css, core.js |

*Pass 6 — COMPLETE (2026-04-02): postprocessing.js shared pipeline created, fog added to cosmic/planck scenes, PostFX API available for all scenes.*

*Pass 7 — COMPLETE (2026-04-02): consciousness.js confirmed pre-existing (298 lines, fully functional). New: print.css (~340 lines) — clean black-on-white, all derivations expanded, proper page breaks, A4 printing. Added prefers-reduced-motion support throughout style.css — disables all animations/transitions when OS preference is set. Added high contrast mode (both forced-colors media query and manual .high-contrast toggle with localStorage persistence). Enhanced keyboard navigation: arrow keys in route nav, Escape closes drawer/nav, focus management on drawer open/close, High Contrast toggle button in rail. ARIA live regions added: #srAnnouncer (polite) and #srAnnouncerAssertive in index.html, aria-live="polite" on drawer body, screen reader announcements on drawer toggle. Responsive gap-fill: 480px breakpoint added, consciousness panel mobile canvas sizing, journey.html wrapped in <main id="journey-content"> with skip link and SR announcer, comparison.html main given id and role. print.css linked in all 8 HTML entry points.*

---

## PASS 1 — NARRATIVE ARCHITECTURE

### 1.1 The Confrontational Opening

**File:** `index.html`

New full-screen landing overlay, shown once per session (`sessionStorage` gate).

**Primary entrance: Visual Zoom Hook (Option D)**
The user zooms through scales and discovers wrongness themselves.

**Overlay Sequence — 9 anchor beats:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     10⁰ m — Human                                          │
│     At your scale, reality looks solid.                    │
│                                                             │
│     [Continues to zoom automatically, 8-10s total]         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Beat 1 — Human scale (10⁰ m)
  At your scale, reality looks solid.

Beat 2 — Cellular (10⁻⁵ m)
  Zoom in: solidity becomes living structure.

Beat 3 — Molecular (10⁻⁹ m)
  Zoom in: structure becomes bond, vibration, and pattern.

Beat 4 — Atomic (10⁻¹⁰ m)
  Zoom in: atoms are mostly field.

Beat 5 — Matter (10⁻¹⁸ m)
  Zoom further: matter resolves into standing pattern.

Beat 6 — Planck (10⁻³⁵ m)
  Zoom further: space stops behaving like space.

Beat 7 — Planetary (10⁷ m)
  Zoom out: worlds move through curved propagation.

Beat 8 — Galactic (10²¹ m)
  Zoom out: galaxies settle into density-wave structure.

Beat 9 — Cosmic (10²⁶ m)
  Zoom out: the universe draws the same logic at the largest scale.

Close:
  Different scales. Same propagation.
```

**Fallback text overlay (no WebGL / SEO / accessibility):**
```
┌─────────────────────────────────────────────────────────────┐
│    YOUR INTUITION ABOUT REALITY IS WRONG.                   │
│                                                             │
│    At your scale, matter looks solid.                       │
│    Zoom in: atoms become fields.                            │
│    Zoom further: matter becomes standing pattern.            │
│    Zoom further: space stops behaving like space.           │
│    Zoom out: galaxies trace the same logic.                 │
│                                                             │
│    Different scales. Same propagation.                      │
│                                                             │
│    [Explore what replaces the old model]                   │
└─────────────────────────────────────────────────────────────┘
```

One-time only. After click: normal app, hub as default. Styled with `--axiom` purple, dramatic entrance animation.

### 1.2 Per-Panel "Reality Check" Callout

Every panel gets a structured wrong-intuition entry in its data. **Ship with provisional copy now; refine after shell is live.**

```javascript
wrongIntuition: {
  intuition:    "Gravity is a force that pulls objects together",
  reality:       "Gravity is the refractive bending of propagation paths in a medium with density gradient",
  scale:         "Works at all scales, most visible near massive objects",
  evidencePanel: "#refraction"  // click to see it live
}
```

Rendered as a prominent styled callout at the top of each info panel. Appears in Story mode, hidden in Math+Audit mode (where you want the raw data).

**Provisional copy for flagship panels (ship now, refine later):**

| Panel | Intuition | Reality |
|-------|-----------|----------|
| gravity | Gravity is a pull | Gravity is bent propagation paths — Fermat's principle in a medium |
| matter | Matter is solid particles | Matter is stable self-reinforcing standing wave patterns |
| three-generations | Three generations is arbitrary | Three generations is required by topology — N=2 fails, N=4 destabilizes |

### 1.3 Journey Mode Restructure — "The De-Programmer"

**File:** `journey.html`

| Act | Title | Content |
|-----|-------|---------|
| Opening | "What is Everything Made Of?" | Axiom reveal, animated staggered |
| Act 1 | "Your Intuition Is Wrong" | Three interactive wrong-intuition panels: **gravity is not a pull**, **matter is not particles**, **why exactly three generations**. Click "No really?" → counter-argument appears. |
| Act 2 | "What Replaces It" | Propagation framework: waves, coherence, standing patterns. The Playground appears here. |
| Act 3 | "The Scale Bridge" | God Equation: Planck to matter, 17 orders, the math that makes it real. (Already Three.js — upgrade in Pass 4) |
| Act 4 | "The Full Audit" | All 22 results sorted by confidence, honest status |
| Epilogue | "Five Ways to Kill It" | Falsification tests as interactive cards — click each test to see the live computation, not just text |

**Act 1 topics (confirmed):**
1. Gravity is not a pull
2. Matter is not particles
3. Why exactly three generations?

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
--resonate:    #ff6b9d;   /* Pink — resonance, Koide */
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

**Font loading:**
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

```javascript
window.ScaleEngine = {
  scales: {},
  camera: { logTarget: 0, currentLog: 0, isTransitioning: false },
  init(containerEl),
  navigateToScale(scaleId, { animated, duration }),
  zoomToLogPosition(logMeters),
  registerScene(scaleId, sceneAPI),
  getScaleAtCursor(screenX, screenY)
}
```

**Key challenge:** 10²⁶m → 10⁻³⁵m is 61 orders. **Solution:** logarithmic coordinate system where camera position is `log₁₀(meters)`, smooth interpolation. Two separate scene graphs (cosmic / Planck) morph at intermediate scales.

### 2.2 The Propagation Shader System

**New File:** `propagation-shaders.js`

Every scale uses the same math — propagation, interference, coherence — with different physical substrates.

### 2.3 The 16 Scale Scene Configurations

**File:** `scale-scenes.js`

| Scale | Log₁₀(m) | Substrate | Key Visualization |
|-------|----------|-----------|-------------------|
| **Planck** | **-35** | Quantum foam lattice | Spinfoam vertices, topology flips |
| Quantum Foam | -34 | Discrete geometry | Pixelated space structure |
| GUT | -25 | Unification field | Force unification as wave merging |
| **Matter** | **-18** | **Coherence field** | Standing wave = mass |
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

### 2.4 Scale Ladder Rewrite

**Files:** `scale-ladder.html`, `scale-ladder.css`, `scale-ladder.js`

Full-screen Three.js experience with log-scale navigation slider and scene morphing.

---

## PASS 3 — COSMIC + PLANCK SCENES

### 3.1 Cosmic Web (new: `cosmic-scene.js`)
- Procedural filament generation via wave interference
- Dark matter halos as standing wave nodes
- Galaxy formation as coherence condensation
- Shows: cosmic web = frozen propagation pattern

### 3.2 Planck Foam (new: `planck-scene.js`)
- Spinfoam lattice with topology flips
- High-frequency wave propagation at discrete vertices
- God Equation as the bridge from discrete foam to continuous matter

---

## PASS 4 — PHYSICS PANELS 2.0

### 4.1 Propagation Playground (new: `playground.js`)
WebGL/canvas 2D wave simulation. Click to spawn sources, watch interference patterns form, see coherent regions glow green. Educational moment: λ/2 spacing → standing wave = Bohr orbit = matter.

### 4.2 Reality Correction Panel (new: `reality-correction.js`)
Three interactive comparisons for Act 1:
| Intuition | Reality | Evidence |
|-----------|---------|----------|
| Gravity pulls | Light bends through denser medium | Drag star, see path curve |
| Matter is particles | Matter is standing waves | Add waves, see node form |
| Three generations is weird | Three generations is required | See why N=2 fails, N=4 fails, N=3 works |

### 4.3–4.6 Panel Upgrades
- **Koide 3D** (`panels/koide.js`): Three masses as tetrahedron vertices, 120° phase breathing
- **God Equation 2.0** (`panels/god-equation.js`): Log-scale slider Planck→Matter with RG flow
- **Enhanced Refraction** (`panels/refraction.js`): Fermat's principle + gravitational lensing
- **Enhanced Bohr** (`panels/bohr.js`): Wave packet phase closure visualization

---

## PASS 5 — DERIVATION + AUDIT LAYER

### 5.1 No-Go Museum (new: `nogos.js`)
Gallery of documented failed approaches. Failed routes visible as primary feature, not buried.

### 5.2 Derivation Timeline (new: `timeline.js`)
Visual chronology: Axioms → intermediate results → current frontier. Confidence at discovery vs current.

### 5.3 Audit Trail as First-Class UI
Every result in `data.js` exposes: derivation spine, current status, blockers, falsifiers, no-go routes.

---

## PASS 6 — WORLD-CLASS POST-PROCESSING

### 6.1 Shared Pipeline (new: `postprocessing.js`)
- Propagation bloom (coherent regions glow)
- Volumetric medium fog (space is not empty)
- Depth of Field / Bokeh (lens-style focus, BokehPass)
- Film grain (subtle imperfection)
- Color grading (unified palette)

**Implementation:**
- `postprocessing.js` — shared PostFX pipeline (~490 lines)
  - `PostFX.createComposer(renderer, scene, camera, options)` — unified bloom composer, consistent params (strength: 0.55, radius: 0.38, threshold: 0.82) across all scenes
  - `PostFX.addFog(scene, options)` / `PostFX.removeFog(scene)` — volumetric fog API
  - `PostFX.createColorGradePass()` — combined ACES filmic tone mapping + film grain shader pass
  - `PostFX.patchRenderer()` — for patching existing renderers with full PostFX pipeline
  - `PostFX.createMaterial(preset, options)` — scale-appropriate PBR material helper with 6 presets: coherent, filament, plasma, quantum, neural, virus
  - `PostFX.setDOFFocus(focus)` / `PostFX.setDOFAperture(aperture)` — DOF control API via BokehPass
- `scale-ladder.html` — added `postprocessing.js` + `ShaderPass.js` + `BokehPass.js` CDN to script chain

### 6.2 PBR Materials
Scale-appropriate physically-based materials throughout.

**Implementation:**
- `PostFX.createMaterial()` helper provides consistent MeshStandardMaterial defaults per scale/type
- Fog integrated into `cosmic-scene.js` (density 0.008) and `planck-scene.js` (density 0.010)
- Both scenes clear fog on deactivate()
- DOF available via `createComposer` options (disabled by default, enable with dof: true)
- Existing panels (koide, god-equation, bohr) retain standalone bloom — PostFX available for future migration

---

## PASS 7 — CONSCIOUSNESS + POLISH

### 7.1 Aria Coherence Panel (new: `consciousness.js`)
Connects P1 consciousness measurement to physics. Include now as coherence/structure panel; gate P1 data-heavy claims behind availability.

### 7.2 Responsive Design
- Desktop: Full Three.js
- Tablet: Hybrid (2D ladder, 3D on click)
- Mobile: 2D fallback where performance demands

### 7.3 Accessibility
- Full keyboard navigation
- Screen reader labels for all visualizations
- High contrast mode, reduced motion option

### 7.4 Print Stylesheet
Clean black-on-white, all derivations expanded, proper page breaks.

---

## ALL 7 DECISIONS — RESOLVED

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Confrontation overlay | **Hybrid:** Visual Zoom Hook (Option D) as primary entrance; Variant A text fallback. See Section 1.1 for full overlay sequence and fallback copy. |
| 2 | Act 1 topics | Gravity is not a pull / Matter is not particles / Why exactly three generations? |
| 3 | Fonts | Spectral (headlines) + Source Serif 4 (body) + Geist/DM Sans (UI) + JetBrains Mono (formulas) |
| 4 | Playground | WebGL/canvas wave sim first; CPU fallback only if needed |
| 5 | Consciousness panel | Include now as coherence/structure panel; gate P1 data-heavy claims behind availability |
| 6 | Mobile fallback | 3D where stable; 2D ladder fallback where performance or interaction density demands |
| 7 | wrongIntuition entries | Ship with provisional copy now; refine after shell is live |

---

## SEQUENCING RULES

- Finish Pass 1 before large scene work. Story and system decide what the engine needs, not the reverse.
- Pass 2 is the architectural hinge. Do not start endpoint scenes before the ladder API exists.
- Passes 3 and 4 can overlap only after Pass 2 is stable.
- Pass 5 must truth-sync against repo data, not hand-written presentation text.
- Passes 6 and 7 are polish only after the product structure is already correct.

---

## PASS EXIT CHECKLIST

Each pass is only complete when:
- [ ] Explorer loads cleanly
- [ ] New UI wired into existing navigation
- [ ] Story mode and audit mode both behave intentionally
- [ ] Claim text remains consistent with repo truth
- [ ] Pass result reflected back into this file

---

## QUALITY BAR

Every deliverable must meet:
- **Observable/Distill.pub standard** for visual polish
- **Apple product page** smoothness for animations
- **Three.js examples** level for 3D scenes
- **P0 truth standard** — all claims verified against CLAIMS.md
- **WCAG 2.1 AA** accessibility compliance

---

## SUCCESS METRICS

- User completes Act 1: 80%
- User reaches Scale Ladder: 60%
- User interacts with at least one playground: 40%
- Average session time: >5 minutes
- Bounce rate on confrontation: <30%

---

## CHANGE LOG

| Date | Change |
|------|--------|
| 2026-04-02 | Full plan written with 7-pass structure, acceptance criteria, open decisions |
| 2026-04-02 | All 7 decisions resolved. Visual Zoom Hook (Option D) + Variant A fallback locked as primary entrance. Act 1 topics confirmed. Fonts, playground tech, consciousness panel timing, mobile fallback all set to recommended defaults. wrongIntuition to ship with provisional copy. |
| 2026-04-02 | Pass 6 COMPLETE. postprocessing.js created (createComposer, addFog, createColorGradePass, createMaterial). Fog added to cosmic-scene.js and planck-scene.js. scale-ladder.html updated with postprocessing.js + ShaderPass CDN. PBR material helper available for all scenes. |
| 2026-04-02 | Pass 6 review fix: DOF/Bokeh added to postprocessing.js via BokehPass CDN. BUG FIX: wrongIntuition data existed in data.js but was never rendered — fixed via PFExplorer.renderWrongIntuition() helper in core.js, CSS in style.css, and calls added to all 6 affected panels (bohr, refraction, koide, weinberg, god-equation, generations). |
| 2026-04-02 | Pass 7 COMPLETE. consciousness.js confirmed pre-existing and functional. print.css created (~340 lines) with full A4 print styles, derivation expansion, page breaks. prefers-reduced-motion support added throughout style.css. High contrast mode added (forced-colors + .high-contrast class). Keyboard navigation enhanced: arrow keys in route nav, focus management, Escape handler. ARIA live regions: #srAnnouncer polite/assertive, aria-live on drawer body. 480px responsive breakpoint, consciousness mobile canvas sizing. journey.html and comparison.html accessibility: skip links, main landmark, SR announcer. print.css linked in all 8 HTML entry points. High Contrast toggle button added to app-rail. Core.js: announceToScreenReader(), bindKeyboardNav(), bindHighContrastToggle(), mobileNavToggle cached in cacheDom(). |

---

*Canonical plan file. Other planning docs in this folder are supporting context.*
*Plan version: 2.0 — All decisions resolved. Pass 1 can start immediately.*
