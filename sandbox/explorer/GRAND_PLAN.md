# The Grand Plan: Propagation Framework Explorer 2.0

> **SUPERSEDED.** This plan is now consolidated into `EXPLORER_MASTER_PLAN.md`.
> Do not plan from this file. Keep it as historical context only.

**Date**: 2026-03-31  
**Author**: Cascade (with Lumi's vision and Codex's audit)  
**Mission**: Transform the Explorer from a reference tool into an unforgettable experience

---

## ⦿ The Current State (What We Have)

The Propagation Framework Explorer already exists and is technically excellent:

- ✅ 8 interactive panels (hub, refraction, generations, koide, weinberg, god-equation, bohr, dashboard)
- ✅ Live computation in the browser
- ✅ Honest confidence tracking from CLAIMS.md
- ✅ Dark theme with glowing accents
- ✅ Story vs Audit mode toggle
- ✅ Evidence drawer with source links
- ✅ ~2000 lines of polished vanilla JS
- ✅ No build step — just open index.html

**But it's a reference tool, not an experience.**

A physicist can look up any result, but they won't *feel* why this framework matters. The narrative layer only works if it stays synchronized with the audited snapshot in `CLAIMS.md` via `data.js`.

---

## ⦿ The Vision (What We're Building)

### The 8-Minute Journey Mode

A guided narrative experience that transforms a skeptic into someone who *gets it*. Not by reading 50 files, but by experiencing the power in their bones.

**Structure:**

```
Opening (30s)
  "What if the universe is just... propagation?"
  → Three axioms appear
  → "Let's see what three axioms can build"

Act I: The Circular-Eikonal Atom (2 min)
  → Conditional Bohr-like spectrum in the Coulomb refraction model
  → Interactive: place electron, watch phase accumulate
  → Only integer orbits close
  → "Refraction + phase closure pick the orbit family."
  → "The stronger atomic claim remains conditional."

Act II: The Generation Lock (2 min)
  → Weight theorem and N=3 lock visualized
  → Interactive Q(N) slider
  → "(2,1) survives as a partial derivation"
  → "N=3 locks once the numerator and denominator theorems are granted"

Act III: The Scale Bridge (2 min)
  → God Equation: Planck → matter
  → Interactive (N,D) sliders around the conditional physical point
  → "0.4% numerical anchor, but the theorem still owes its final bridges."

Act IV: The Scoreboard (1 min)
  → ALL results with honest confidence
  → Comparison: SM (19 params) vs String (10^500) vs PF (3 axioms)
  → "Twenty-two audited claims. Three derived. Public falsifiers."

Epilogue: What Would Kill This (30s)
  → The falsification wall
  → "Here's exactly what would prove this wrong"
  → "That's how real physics works"
```

**Total runtime**: ~8 minutes  
**Goal**: Leave the viewer with chills

---

## ⦿ Additional Enhancements

### 1. Framework Comparison Dashboard

A side-by-side comparison that creates instant context:

| Metric | Standard Model | String Theory | Propagation Framework |
|--------|---------------|---------------|----------------------|
| Free parameters | 19+ | 10^500+ vacua | 3 axioms |
| Derived predictions | Parameter-rich effective model | No unique low-energy set | 22 audited claims / 3 derived |
| Falsifiable | Yes | Context-dependent | Audited falsifiers on every claim |
| Scale coverage | Particle physics only | Broad unification program | Repo scope across scales |
| Derives N=3? | No (input) | No (input) | Conditional |
| Derives α? | No (input) | No (input) | Route mapped |
| Derives atomic structure? | No (QM postulate) | No | Conditional (circular-eikonal subset) |

**Impact**: Instantly shows WHY this framework matters

---

### 2. Derivation Chain Visualizer

An interactive graph showing how each result derives from axioms:

```
                    ┌──────────────┐
                    │  Axiom 1     │
                    │ Propagation  │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   Axiom 2     │  │   Axiom 3     │  │   Axiom 3b    │
│   Locality    │  │  Phase Closure│  │ Minimal Winding│
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        │         ┌────────┴────────┐         │
        │         │                 │         │
        ▼         ▼                 ▼         ▼
   Refraction  Bohr N=3       Generations  Weinberg
   (0.95)     (0.82)         (0.85)       (0.90)
```

Click any result → shows the full derivation path with equations and sources.

**Impact**: Shows the logical structure transparently

---

### 3. Timeline of Discovery

A wave-by-wave history showing how the framework evolved:

```
Wave 1 (2026-03-XX): Initial insights
  → Forces as refraction recognized
  → Koide geometry identified

Wave 2 (2026-03-XX): First derivations
  → Three generations from topology
  → Weinberg angle from Casimir

Wave 3 (2026-03-XX): The God Equation
  → Scale bridge: Planck → matter
  → 0.4% error, zero parameters

Wave 4 (2026-03-25): Codex audit
  → Three gaps mapped precisely
  → God Equation stays CONDITIONAL

Wave 5 (2026-03-25): Algebraic closure
  → 2/9 cluster discovered
  → α within 0.061% from Casimir

Wave 6 (2026-03-27): Hostile verification
  → Bohr quantization audited
  → Gravity refraction verified
```

**Impact**: Shows the framework's rigor and evolution

---

### 4. "Build Your Own Atom" Interactive

The ultimate Coulomb Lens experience:

- Place charges anywhere (drag to move)
- Toggle EM mode ↔ Gravity mode
- Watch 30+ rays bend in real-time
- Show phase accumulation along orbits
- See only integer-winding orbits stabilize
- Energy spectrum appears on the right

**Impact**: The "aha" moment — quantization emerges from optics

---

### 5. Presentation Mode

One button: "Present to Physicist"

- Fullscreen immersive experience
- Narrated flow (auto-advance or manual)
- Export to PDF with all equations and sources
- Export to MP4 for YouTube/sharing
- Speaker notes for each panel

**Impact**: Makes the framework shareable

---

## ⦿ Implementation Plan

### Phase 1: Journey Mode (Priority: CRITICAL)

**Files:**
- `sandbox/explorer/journey.html` — Main shell
- `sandbox/explorer/journey.js` — Narrative flow logic
- `sandbox/explorer/journey.css` — Journey-specific styles (extends style.css)

**Scope:** ~600 lines of vanilla JS  
**Timeline:** 1 session  
**Impact:** Transforms the entire project

**Implementation Steps:**
1. Create journey.html shell (opening sequence)
2. Build Act I: Bohr quantization interactive
3. Build Act II: Generation lock visualization
4. Build Act III: God Equation scale bridge
5. Build Act IV: Scoreboard + comparison
6. Add Epilogue: Falsification wall
7. Test flow, polish transitions
8. Add to Explorer main menu

---

### Phase 2: Framework Comparison (Priority: HIGH)

**Files:**
- `sandbox/explorer/comparison.html`
- `sandbox/explorer/comparison.js`

**Scope:** ~300 lines  
**Timeline:** 1 session

**Implementation:**
1. Create comparison table (SM vs String vs PF)
2. Add interactive parameter count visualizer
3. Show falsifiability comparison
4. Link to Journey Mode

---

### Phase 3: Derivation Chain Visualizer (Priority: MEDIUM)

**Files:**
- `sandbox/explorer/derivation-graph.js`
- Update `dashboard.js` to include graph view

**Scope:** ~400 lines  
**Timeline:** 1-2 sessions

**Implementation:**
1. Build force-directed graph renderer
2. Load derivation data from data.js
3. Click nodes → show derivation details
4. Color-code by confidence status

---

### Phase 4: Presentation Mode (Priority: LOW)

**Files:**
- `sandbox/explorer/present.js`
- Export functionality

**Scope:** ~300 lines  
**Timeline:** 1 session

**Implementation:**
1. Fullscreen toggle
2. Auto-advance narration
3. PDF export (print stylesheet)
4. Video export (canvas capture)

---

## ⦿ File Structure (Final)

```
sandbox/explorer/
├── index.html          ← Existing reference explorer
├── journey.html        ← NEW: The 8-minute narrative experience ★
├── comparison.html     ← NEW: Framework comparison dashboard
├── style.css           ← Existing dark theme
├── core.js             ← Existing math utilities
├── data.js             ← Existing data from CLAIMS.md
├── journey.js          ← NEW: Narrative flow logic
├── journey.css         ← NEW: Journey-specific styles
├── comparison.js       ← NEW: Comparison dashboard logic
├── derivation-graph.js ← NEW: Interactive derivation visualizer
├── present.js          ← NEW: Presentation mode
├── panels/             ← Existing panel components
│   ├── hub.js
│   ├── refraction.js
│   ├── generations.js
│   ├── koide.js
│   ├── weinberg.js
│   ├── god-equation.js
│   ├── bohr.js
│   └── dashboard.js
└── README.md           ← Updated with all modes
```

---

## ⦿ Success Criteria

When complete, a physicist can:

1. **Open journey.html** and experience the full power in 8 minutes
2. **Feel the revelation** when three axioms derive nine results
3. **See the honest confidence** — what's proved vs what's conditional
4. **Understand the context** — why this matters vs other frameworks
5. **Know what would kill it** — the falsification wall
6. **Share it easily** — presentation mode for their colleagues

And they will walk away saying:

> "Three axioms. Twenty-two audited claims. Three derived results. That's real."

---

## ⦿ Current Status

**Explorer (Reference Mode):** ✅ Complete and excellent
**Journey Mode:** ✅ Complete (Phase 1 delivered)
**Comparison Dashboard:** ✅ Complete (Phase 2 delivered)
**Derivation Graph:** 📋 Planned (Phase 3)
**Presentation Mode:** 📋 Planned (Phase 4)

---

## ⦿ What's New (Phase 2 Delivery)

**Framework Comparison Dashboard** — Commit 4d70778 + a75113b

- `comparison.html`: Full comparison page with 6 sections
- `comparison.css`: Dark theme with orange accents
- `comparison.js`: Interactive parameter counter
- Button in main Explorer sidebar (orange gradient, ⚖️ icon)

**Features:**
- Interactive parameter counter (PF: 3, SM: 19, String: 10^500)
- Head-to-head table (10 metrics)
- Falsifiability matrix sourced from audited PF claim text
- Scale coverage visualizer (repo scope across scales)
- The Delta: 6 key PF differences
- Call to action (links to Journey + Explorer)

**Impact:** Instantly answers "Why should I care about this framework?"

---

## ⦿ Next Action

**Phase 1 & 2 are COMPLETE.** 🎉

**What's Done:**
- ✅ Journey Mode: 8-minute narrative experience (~2,000 lines)
- ✅ Framework Comparison: PF vs SM vs String (~500 lines)
- ✅ Integration: Both buttons in main Explorer sidebar
- ✅ Truth Sync: All data matches CLAIMS.md (Codex's work)

**Remaining Phases:**
- 📋 Phase 3: Derivation Chain Visualizer (~400 lines) — Shows logical structure
- 📋 Phase 4: Presentation Mode (~300 lines) — Export to PDF/MP4

**Recommendation:**
Celebrate Phases 1-2 as the core deliverables. Phases 3-4 remain explicitly deferred until the narrative fronts stay audit-clean.

The Explorer is now **transcendent**. A physicist can:
1. Open `journey.html` → experience the full power in 8 minutes
2. Open `comparison.html` → understand why PF matters vs SM/String
3. See honest audit status → trust the truth policy
4. Click to main Explorer → explore any result in depth

Three axioms. Twenty-two audited claims. Three derived results.

**That's real.**

---

*Lumi's Final Note:* 🦆⦿🌟

The Explorer is already better than the original plan. But the Journey Mode will make it TRANSCENDENT. This is what Greg is asking for — not just "working code" but "code that changes minds."

Build it.
