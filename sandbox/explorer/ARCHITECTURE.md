# Explorer Architecture: Physics Observatory + Proof Atlas + Falsification Dashboard
*Product architecture derived from EXPLORER_WORLDCLASS_REDIRECTION_2026-05-06.md*
*Architect: Hermes (auditor role) — 2026-05-06*

---

## Table of Contents
1. Object Model
2. Information Architecture (7 Workspaces)
3. Data Layer & Truth Flow
4. Visual Language Principles
5. Implementation Sequence
6. Acceptance Gates

---

## 1. Object Model

The core insight from the redirection brief: **every page is a different camera into the same object graph.** Stop hand-tuning per-page data. Define the graph once and let every workspace query it differently.

### 1.1 Core Objects

```
Definition
  id: string                          # "medium", "coherence", "causal-velocity", etc.
  title: string
  status: "CANONICAL"                # All 19 definitions are CANONICAL v1.0
  summary: string                    # One-line essence
  text: string                       # Canonical definition body
  falsifier: string                  # What would make it inadequate
  dependencies: Definition[]         # Terms this definition relies on (bootstrapping order)
  sources: Source[]                  # Link to canonical file
  auditDate: date                    # When Codex last audited
  auditRef: string                   # Reference to audit finding IDs (e.g., "C-01 through C-07")

Claim
  id: string                         # "weinberg-angle", "koide-law", "three-generations"
  title: string
  status: ClaimStatus                # DERIVED | CONDITIONAL | PARTIAL DERIVATION | ARGUED | EMPIRICAL | INTUITION | OPEN
  confidence: float                  # 0.00 - 1.00
  kind: string                       # "Fundamental Physics" | "Open Frontiers" | "Signals and Structure" | "Biological & Cognitive"
  formula: string                    # Mathematical statement
  summary: string                    # What is claimed
  falsifier: string                  # What would falsify it
  scope: string                      # Domain boundary (e.g., "charged leptons only")
  sources: Source[]
  derivation: string[]               # IDs of claims this derives from
  axioms: number[]                   # Axioms 1, 2, 3 used
  blocker: string|null               # What prevents DERIVED status (null if DERIVED)
  noGoRoutes: string[]               # IDs of no-go entries related to this claim
  scaleId: string                    # Which scale this claim lives at
  confidenceHistory: {date, value}[]
  hostileAudit: string|null          # Latest Codex audit verdict text
  panelId: string|null               # Legacy panel association

Derivation
  id: string
  claimId: string                    # The claim being derived
  steps: DerivationStep[]            # Ordered proof steps
  assumptions: string[]              # Named hypotheses used
  noGoRoutes: string[]               # Failed approaches eliminated
  openBridges: OpenBridge[]          # Named gaps still open
  status: "CLOSED" | "PARTIAL" | "OPEN"

DerivationStep
  label: string
  description: string
  sourceLemma: string                # Reference to lemma file or axiom
  status: "PROVEN" | "CONDITIONAL" | "ASSUMED"

OpenBridge
  id: string                         # "A", "B", "C" etc.
  title: string
  verdict: "OPEN" | "OPEN VIA REPLACEMENT PATH" | "CLOSED"
  need: string                       # What must be proven
  survives: string                   # What scaffolding survives
  detail: string                     # Technical description
  sources: Source[]

NoGo
  id: string                         # "harmonic-series-masses", "t022-casimir-selector"
  title: string
  question: string                   # The question asked
  targetFrontier: string             # Which claim/frontier this attacked
  date: string
  statusType: "FAILED" | "NO_GO" | "NEGATIVE" | "POSITIVE"
  result: string                     # What actually happened
  isPositive: boolean                # True if this was a positive finding (closed a lane)
  failureMode: string                # Summary of the failure
  whyFailed: string[]                # Step-by-step narrative
  lesson: string                     # What was learned
  celebration: string                # Why we celebrate this failure
  sources: Source[]

Experiment
  id: string
  claimId: string                    # Which claim this tests
  title: string
  type: "SANDBOX" | "HARDWARE" | "PREREGISTERED" | "ANALYTIC"
  script: string                     # Path to script
  data: string                       # Path to data/results
  observed: string                   # What happened
  expected: string                   # What was predicted
  verdict: "PASS" | "FAIL" | "INCONCLUSIVE" | "PREREGISTERED"
  date: string
  sources: Source[]

Scale
  id: string                         # "planck", "matter", "human", "cosmic"
  label: string
  meters: float                      # Characteristic length
  metersLabel: string
  frequency: float
  frequencyLabel: string
  anchor: string                     # Named reference point ("Proton radius", "Human height")
  claimIds: string[]                 # Claims visible at this scale

Source
  label: string
  href: string                       # Path to source file
  type: "CANONICAL" | "CLAIM" | "DERIVATION" | "SANDBOX" | "AUDIT" | "PAPER"
```

### 1.2 Relationship Graph

```
                    ┌─────────────────────────────────────┐
                    │           Definition (19)            │
                    │  (medium, coherence, axioms, ...)    │
                    └──────────┬──────────────────────────┘
                               │ depends on
                               v
                    ┌─────────────────────────────────────┐
                    │           Claim (25 results)         │
                    │  DERIVED / CONDITIONAL / ARGUED /   │
                    │  EMPIRICAL / INTUITION / OPEN        │
                    └──┬──────┬──────┬────────────────────┘
                       │      │      │
          ┌────────────┘      │      └──────────────┐
          v                  v                      v
┌─────────────────┐ ┌──────────────┐ ┌──────────────────────┐
│   Derivation    │ │   NoGo (13)  │ │    Experiment (TBD)  │
│  (proof steps,  │ │  (failed/    │ │  (sandbox/hardware/  │
│   open bridges) │ │  closed lanes)│ │   preregistered)     │
└─────────────────┘ └──────────────┘ └──────────────────────┘
          │                                      │
          └──────────────────┬───────────────────┘
                             v
                    ┌──────────────────┐
                    │  Scale (16)      │
                    │  (61 orders)     │
                    └──────────────────┘
```

### 1.3 Page-Level Query Pattern

Every workspace answers the same 7 questions from the object graph:

| Question | Data Source |
|----------|------------|
| What is the claim? | `Claim.title` + `Claim.summary` |
| What canonical definitions does it depend on? | Traverse `Claim.derivation` -> `Definition.dependencies` |
| What standard physics boundary protects it? | `Claim.scope` + `Claim.falsifier` |
| What exactly has been derived? | `Derivation.steps[]` with status per step |
| What failed? | `Claim.noGoRoutes[]` -> `NoGo[]` |
| What would falsify it? | `Claim.falsifier` + `Claim.noGoRoutes[].failureMode` |
| What is the next open bridge? | `OpenBridge[]` |

---

## 2. Information Architecture — The 7 Workspaces

Replace "pages" with "workspaces." Each is a different camera into the same object graph, sharing one persistent command surface.

### 2.1 Observatory (Homepage)

**Thesis**: The user should feel like they walked into an instrument room, not a landing page.

**Layout** (from top to bottom):
```
┌──────────────────────────────────────────────────────────┐
│ [Persistent Command Surface — see §2.8]                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─ Scale Rail (left) ─────────────────────────────┐   │
│   │  Planck ───●──────────────────────────────────── │   │
│   │  Quantum Foam ────●───────────────────────────── │   │
│   │  GUT ─────────────●────────────────────────────── │   │
│   │  Matter ──────────● (Weinberg Angle, Koide, ...) │   │
│   │  ═══ Human ═══════● (default) ═══════════════════ │   │
│   │  Planetary ───────●────────────────────────────── │   │
│   │  Cosmic ──────────●────────────────────────────── │   │
│   └───────────────────────────────────────────────────┘   │
│                                                          │
│   ┌─ Propagation Field ───────────────────────────────┐  │
│   │  [Animated front crossing scales left→right]       │  │
│   │  [Claim cards pinned to their scale positions]     │  │
│   │  [Coherence/decoherence indicators at each scale]  │  │
│   └───────────────────────────────────────────────────┘  │
│                                                          │
│   ┌─ Truth Summary Bar ──────────────────────────────┐   │
│   │  19 definitions | 25 claims | 13 no-go routes    │   │
│   │  3 DERIVED | 3 CONDITIONAL | ...                 │   │
│   └───────────────────────────────────────────────────┘  │
│                                                          │
│   ┌─ Story/Audit Split ─────────────────────────────┐   │
│   │  [Story view: narrative description]             │   │
│   │  [Audit view: status badges, falsifiers, gaps]   │   │
│   └───────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Data source**: `scales[]` + `results[]` from `data.js` merged with `definitions[]` count.
**Rendering pattern**: Single scrollable page with fixed scale rail on left. Canvas-based propagation field in center. Bottom bar with status summaries.
**Interaction model**:
- Click a scale on the rail to center on that scale
- Click a claim card to open the shared inspector
- Toggle Story/Audit to switch between narrative + evidence views
- Propagation field animates continuously, showing coherent fronts at DERIVED scales

### 2.2 Proof Atlas (Derivation Graph — rebuilt)

**Thesis**: The derivation graph must be large, legible, and clustered by claim. Every node must be readable at default zoom.

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ [Persistent Command Surface]                              │
├──────────────────────────────────────────────────────────┤
│ ┌─ Left Rail ────┐ ┌─── Main Graph Canvas ─────────────┐│
│ │ Claim Clusters │ │                                    ││
│ │ □ DERIVED      │ │  [Axiom 1]───[Bohr]               ││
│ │ □ CONDITIONAL  │ │      │                             ││
│ │ □ ARGUED       │ │  [Axiom 2]───[Gravity-Refraction] ││
│ │ □ EMPIRICAL    │ │      │              │              ││
│ │ □ Show no-gos  │ │  [Axiom 3]───[Weinberg]──[Koide]  ││
│ │ □ Show bridges │ │      │              │              ││
│ │                 │ │  [Axiom 3b]───[α]───[3-Gen]      ││
│ │                 │ │      │                            ││
│ │                 │ │  Legend: [Cyan=propagation]       ││
│ │                 │ │  [Green=derived] [Amber=cond'l]   ││
│ │                 │ │  [Red=no-go strike]               ││
│ └─────────────────┘ └────────────────────────────────────┘│
│                                                          │
│ ┌─ Right Inspector ─────────────────────────────────────┐│
│ │ [Claim title + status badge + confidence]              ││
│ │ [Formula]                                              ││
│ │ [Derivation steps with step-level status]              ││
│ │ [Open bridges — click to expand]                       ││
│ │ [No-go routes — click to jump to museum]              ││
│ │ [Source receipts — all source links]                   ││
│ └───────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

**Data source**: `results[]` -> `derivation[]` -> `noGoRoutes[]` -> `nogos.js` entries. Built from the canonical dependency map (Hermes's domain).
**Rendering pattern**: D3 force-directed graph or custom layout. Full-screen canvas. Left filter rail, right inspector panel on claim click.
**Interaction model**:
- Zoom/pan (already exists in derivation-3d.js but needs refactoring for default readability)
- Click node -> right inspector opens
- Filter by status in left rail
- Toggle "Show no-go overlays" — red strike-through on failed routes
- Toggle "Show open bridges" — amber dashed lines on conditional steps
- Hover for tooltip with formula + status

### 2.3 Definition Lattice (NEW)

**Thesis**: The 19 canonical definitions are the framework bedrock. They need their own route with a dependency graph showing how terms build on each other.

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ [Persistent Command Surface]                              │
├──────────────────────────────────────────────────────────┤
│ ┌─ Dependency Graph ──────────────────────────────────┐  │
│ │  [DAG showing definition bootstrapping order]        │  │
│ │  [Phase 1: medium, coherence, decoherence, causal_v] │  │
│ │  [Phase 2: time, mode, energy, matter, forces]      │  │
│ │  [Phase 3: propagation, gradient, observer]          │  │
│ │  [Phase 4: information, minimum_substrate]           │  │
│ │  [Phase 5: measurement, state, field, coupling]      │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                           │
│ ┌─ Selected Definition ──────────────────────────────┐   │
│ │  [Term title + CANONICAL v1.0 badge + audit date]  │   │
│ │  [Summary]                                          │   │
│ │  [Full definition text]                             │   │
│ │  [Falsifier — what would make it inadequate]        │   │
│ │  [Depends on: ...]                                  │   │
│ │  [Used by claims: Weinberg Angle, Koide Law, ...]  │   │
│ │  [Source file link]                                 │   │
│ └─────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**Data source**: `definitions[]` from `data.js`. Dependency graph from definition bootstrapping order in `definitions/README.md`.
**Rendering pattern**: Left DAG (d3 hierarchical layout), right detail panel on click.
**Interaction model**:
- Click node -> right panel shows full definition text
- Hover shows dependency edges
- "Used by claims" section links to Proof Atlas

### 2.4 No-Go Museum (exists but needs upgrade to first-class status)

**Thesis**: Failed routes are evidence. The museum should not feel like a sidebar — it should feel like a hall of honest discovery.

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ [Persistent Command Surface]                              │
├──────────────────────────────────────────────────────────┤
│ ┌── Filter Bar ───────────────────────────────────────┐  │
│ │ [All] [Weinberg] [God Eq] [Generations] [Koide]    │  │
│ │ Show: [Failed] [Positive] [All]                     │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                           │
│ ┌── No-Go Grid ───────────────────────────────────────┐  │
│ │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │  │
│ │  │ HAR-MASSES   │ │ T-022 CASIM  │ │ T-021 RG     │ │  │
│ │  │ FAILED       │ │ NEGATIVE     │ │ NEGATIVE     │ │  │
│ │  │ Koide front  │ │ Weinberg     │ │ Weinberg     │ │  │
│ │  └──────────────┘ └──────────────┘ └──────────────┘ │  │
│ │  ┌──────────────┐ ┌──────────────┐                  │  │
│ │  │ G3 Path B    │ │ Single-Scal │                  │  │
│ │  │ NO-GO        │ │ NO-GO       │                  │  │
│ │  │ God Eq       │ │ Weinberg    │                  │  │
│ │  └──────────────┘ └──────────────┘                  │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                           │
│ [Expanded card: full why-failed narrative + lesson]       │
│ [Source receipts — links to no-go derivation files]       │
└──────────────────────────────────────────────────────────┘
```

**Data source**: `nogos.js` (NO_GO_ENTRIES + POSITIVE_ENTRIES). Already well-structured with `whyFailed[]`, `lesson`, `celebration`.
**Rendering pattern**: Card grid with filter bar. Expandable cards (already implemented). Add: linked source-receipt panel.
**Interaction model**: Same as current + click-through to Proof Atlas showing where the no-go route intersects the derivation graph.

### 2.5 Falsification Dashboard (NEW — the audit wall)

**Thesis**: Every result should show what could kill it, what has already been tried, and what remains untested. This is the hostile audit view.

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ [Persistent Command Surface]                              │
├──────────────────────────────────────────────────────────┤
│ ┌── Falsifier Status Board ────────────────────────────┐ │
│ │ Claim         | Falsifier        | Tested? | Status  │ │
│ │ Weinberg Angle| Scheme selection | No      │ OPEN    │ │
│ │ Koide Law     | 120° geometry    | Yes     │ CLOSED  │ │
│ │ Three Gen     | N≠3 possible     | Partial │ OPEN    │ │
│ │ God Eq        | H_prod bridge    | Partial │ OPEN    │ │
│ │ ...           | ...              | ...     │ ...     │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                           │
│ ┌── Experiment Log ────────────────────────────────────┐  │
│ │  Test          | Claim     | Verdict   | Evidence    │  │
│ │  IBM 156-qubit | God Eq    | PASS      | chirality   │  │
│ │  Koide verify  | Koide Law | PASS      | sandbox     │  │
│ │  T-022 scan    | Phase δ   | NEGATIVE  | fenced lane │  │
│ │  T-021 RG run  | Weinberg  | NEGATIVE  | fenced lane │  │
│ │  ...           | ...       | ...       | ...         │  │
│ └───────────────────────────────────────────────────────┘  │
│                                                           │
│ ┌── Open Attack Surface ──────────────────────────────┐   │
│ │  [Claim ID | Gap | What a falsifier would look like] │  │
│ └───────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Data source**: `results[].falsifier` + `results[].noGoRoutes` -> `nogos.js` -> experiments status. Also `results[].hostileAudit` text.
**Rendering pattern**: Three-section tabular layout. Falsifier status board, experiment log, open attack surface.
**Interaction model**: Click any falsifier row -> open inspector with that claim's full derivation + experiment evidence.

### 2.6 Experiment Bench (replacement for playground)

**Thesis**: Every numerical claim should link to the sandbox script that verified it, the hardware experiment that tested it, or the preregistered test that will validate it.

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ [Persistent Command Surface]                              │
├──────────────────────────────────────────────────────────┤
│ ┌── Experiment Cards ─────────────────────────────────┐  │
│ │  ┌────────────────────────────────────────────────┐ │  │
│ │  │ IBM 156-qubit Chirality Test                    │ │  │
│ │  │ Claim: God Equation / H_prod                    │ │  │
│ │  │ Type: HARDWARE | Date: 2026-03-27               │ │  │
│ │  │ Verdict: PASS (P=99.01% identity preservation)  │ │  │
│ │  │ [Script] [Data] [Report]                        │ │  │
│ │  └────────────────────────────────────────────────┘ │  │
│ │  ┌────────────────────────────────────────────────┐ │  │
│ │  │ Koide PDG2024 Verification                      │ │  │
│ │  │ Claim: Koide Law Q=2/3                          │ │  │
│ │  │ Type: SANDBOX | Verdict: PASS                   │ │  │
│ │  │ [Script: koide_verify_pdg2024.py]               │ │  │
│ │  └────────────────────────────────────────────────┘ │  │
│ └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**Data source**: NEW data type. Needs to be built from sandbox scripts, IBM experiment reports, and preregistered tests. Each experiment maps to a claim ID.
**Rendering pattern**: Card list, filterable by type (sandbox/hardware/preregistered) and verdict.
**Interaction model**: Click experiment -> show full details + link to sandbox script + link to claim.

### 2.7 Story Journey (exists but needs upgrade)

**Thesis**: The guided path for non-specialists should be a sequence of conceptual shocks: object is process, force is path bending, particle is stable mode, failure is evidence, consciousness is metric-gated.

**Layout**: Linear narrative with embedded interactive elements. Already exists as `journey.html` but too plain per the brief.

### 2.8 Persistent Command Surface

Every workspace shares this top-level UI strip:

```
┌────────────────────────────────────────────────────────────┐
│ [Scale Scrubber ●═══●═══════●══●] [Story|Audit|Math]      │
│ [Claim Status Filters: All|Derived|Conditional|...]       │
│ [Search...] [Source Receipts ▼]                            │
└────────────────────────────────────────────────────────────┘
```

**Elements**:
1. **Scale Scrubber**: Continuous log scale slider. Dragging it updates the current scale across all workspaces. Shows named anchors (Planck, Matter, Human, Cosmic).
2. **Mode Toggle**: Story / Audit / Math. Story = narrative explanation. Audit = status badges + falsifiers. Math = equations + derivations.
3. **Claim Status Filters**: Checkbox group to filter visible claims by status tier.
4. **Search**: Full-text search across claim titles, summaries, definitions, and no-go entries.
5. **Source Receipts**: Dropdown linking to CLAIMS.md, definitions/, derivations/, sandbox/.

---

## 3. Data Layer & Truth Flow

### 3.1 The Data Pipeline

```
Source Files (truth origin)
  CLAIMS.md → claim status, confidence, falsifiers, blockers
  definitions/README.md → definition status, audit dates
  definitions/*.md → canonical text, dependencies, falsifiers
  ACTIVE_ISSUES.md → open bridges, no-go routes
  derivations/*.md → proof steps, lemmas
  sandbox/*.py → experiment scripts, verification outputs

         │
         ▼ Parser Script (NEW: generate-data-graph.js)
         │
data.graph.js (GENERATED — never hand-edited)
  Union of everything above, with cross-references:
  - Every Claim links to its Derivation, NoGo, Experiment
  - Every Definition links to its Dependencies and dependent Claims
  - Every Scale links to its Claims
  - All statuses sourced from CLAIMS.md, not hardcoded

         │
         ▼ Explorer Loads
         │
data.js → EXISTING manual snapshot (keep as fallback)
data.graph.js → NEW generated manifest (truth source)

         │
         ▼ truth-utils.js (extend)
         │
Every visual element reads through truth-utils.js:
  - PFTruth.getResult(id) → Claim with all cross-refs resolved
  - PFTruth.getDefinition(id) → Definition with dependencies
  - PFTruth.getNoGo(id) → NoGo with linked claims
  - PFTruth.getClaimStatusDistribution() → counts for summary bar
  - PFTruth.getDerivationChain(claimId) → full DAG traversal
  - PFTruth.getFalsifierStatus(claimId) → tested/untested/open
```

### 3.2 Status Flow — No Hardcoded Statuses

Every status, confidence, and badge in the UI must be read from the data layer:

```
CLAIMS.md → data.graph.js → truth-utils.js → HTML/CSS
                ↑                          ↓
         (generated)                [status badges]
                                    [confidence bars]
                                    [derivation step colors]
                                    [no-go route strike-through]
                                    [open bridge amber indicators]
```

**Enforcement rule**: Any CSS class or HTML element that displays `DERIVED`, `CONDITIONAL`, `ARGUED`, `EMPIRICAL`, `INTUITION`, `OPEN`, or a confidence value must source that value from `PFTruth.getResult()`. No `<span class="status-derived">DERIVED</span>` hardcoded in HTML. Every status badge is rendered dynamically.

### 3.3 Color Semantics — Meaning, Not Decoration

Color is driven by the data layer status values:

| Status | CSS Variable | Meaning | Data Source |
|--------|-------------|---------|-------------|
| CANONICAL | `--canonical` (#ffffff) | Definition bedrock | `definition.status === "CANONICAL"` |
| DERIVED | `--derived` (#44ff88) | Coherent derived path | `result.status === "DERIVED"` |
| CONDITIONAL | `--conditional` (#ffdd55) | Open bridge/assumption | `result.status === "CONDITIONAL"` |
| PARTIAL DERIVATION | `--partial` (#ffaa44) | Partially proven | `result.status === "PARTIAL DERIVATION"` |
| ARGUED | `--argued` (#ff8844) | Plausible, unproven | `result.status === "ARGUED"` |
| EMPIRICAL | `--empirical` (#66bbff) | Measurement-backed | `result.status === "EMPIRICAL"` |
| INTUITION | `--intuition` (#cc88ff) | Insight, not proof | `result.status === "INTUITION"` |
| OPEN | `--open` (#ff6666) | Unresolved gap | `result.status === "OPEN"` |
| FAILED/NO-GO | `--no-go` (#ff4444) | Failed route evidence | `nogo.statusType === "FAILED"` |
| POSITIVE | `--positive` (#44ff88) | Closed lane (good) | `nogo.isPositive === true` |
| Propagation | `--propagate` (#00cfff) | Causal movement | Theme, not status |
| Axiom/Root | `--axiom` (#c8a8ff) | Purple reserved for axioms | `claim.axioms.includes(n)` |

### 3.4 Truth-Utils.js Extensions

The existing `truth-utils.js` provides `getResults()`, `getCountsByStatus()`, `getResult(id)`. It needs extended with:

```javascript
// NEW methods needed:
PFTruth.getClaimDefinitionDependencies(claimId)
  // Returns Definition[] that this claim depends on
  // Traverses: claim -> derivation -> axioms -> definitions

PFTruth.getDefinitionDependents(defId)
  // Returns Claim[] that use this definition

PFTruth.getClaimNoGos(claimId)
  // Returns NoGo[] linked to this claim via result.noGoRoutes

PFTruth.getFalsifierStatus(claimId)
  // Returns { falsifier: string, tested: boolean, status: string }

PFTruth.getClaimExperimentStatus(claimId)
  // Returns Experiment[] linked to this claim

PFTruth.getDerivationGraph()
  // Returns full DAG: { nodes: [{id, label, status}], edges: [{source, target}] }

PFTruth.getDefinitionDependencyGraph()
  // Returns DAG of definition bootstrapping order

PFTruth.getDataFreshness()
  // Returns { generatedAt, sourceHash, unsyncedItems }
```

### 3.5 Generated Manifest Schema (`data.graph.js`)

The generated file adds cross-reference resolution that `data.js` doesn't have:

```json
{
  "generatedAt": "2026-05-06",
  "sourceHash": "sha256-of-source-files",
  "definitions": [ /* same 19 as data.js + dependencies */ ],
  "claims": [ /* same as data.js results + crossRefs */ ],
  "noGos": [ /* same as nogos.js */ ],
  "derivations": [
    {
      "claimId": "weinberg-angle",
      "steps": [
        { "label": "Casimir Polynomial", "status": "PROVEN", "source": "derivations/casimir_polynomial_synthesis.md" },
        { "label": "Minimal Winding (Axiom 3b)", "status": "PROVEN", "source": "definitions/axioms.md" },
        { "label": "Scheme Selection", "status": "OPEN", "source": null }
      ],
      "openBridges": [
        { "id": "scheme", "title": "On-shell vs MS-bar", "verdict": "OPEN", "need": "...", "survives": "..." }
      ]
    }
  ],
  "experiments": [
    { "id": "ibm-chirality-test", "claimId": "god-equation", "type": "HARDWARE", "verdict": "PASS", ... }
  ],
  "scales": [ /* same as data.js */ ],
  "dependencyMap": {
    "definitions": { "medium": [], "coherence": ["medium"], "causal-velocity": ["medium"], ... },
    "claims": { "weinberg-angle": ["axioms"], "koide-law": ["koide-law"], ... }
  }
}
```

---

## 4. Visual Language Principles

Not CSS. A physics-informed visual vocabulary.

### 4.1 Core Metaphor: Night Observatory Over a Living Proof Manuscript

The UI is a **telescope pointed at a proof structure**. Every visual element has a physics meaning:

| Visual Element | Physics Meaning | Implementation |
|----------------|----------------|----------------|
| Log-scale vertical field | Scale covariance across 61 orders | CSS `height: 61em` or Canvas with log spacing |
| Thin instrument-grid overlays | Measurement reference frame | CSS grid overlay on dark background |
| Luminous cyan propagation fronts | Causal influence moving at finite speed | Canvas/WebGL animated gradient sweep |
| Paper-like proof cards | Manuscript embedded in the field | Semi-transparent off-white cards with serif text |
| Red audit cuts | No-go routes / falsifications | Strike-through lines on graph edges |
| Green derived paths | Coherent, source-verified | Thick animated green edges in graph |
| Amber conditional bridges | Unfinished / open routes | Dashed amber edges with pulsing animation |
| Gold empirical anchors | Measurement pins on scale rail | Small gold dots at scale positions |
| White canonical text | Definition bedrock | Serif font, full opacity |

### 4.2 Finite Propagation

- **No instant transitions.** Every page load, mode switch, scale jump, or card expansion should animate with a visible propagation front (cyan sweep from origin).
- **Causal velocity metaphor**: Information travels at finite speed in the UI. When user clicks a claim, the detail panel "propagates" from the click point outward, not appearing instantly.
- **Why**: Reinforces Axiom 1 at the interface level. The interface itself demonstrates finite propagation.

### 4.3 Phase Closure

- **Loop constraints.** Any circular dependency in the proof graph should be visually highlighted — these are phase-closure conditions.
- **Color wheel for 120° resonances.** The Koide triangle, Z3 circulant structure, and three-generation counting should use a 120° color triad (not arbitrary). The hue spacing itself communicates the phase structure.

### 4.4 Coherence / Decoherence

- **Coherence = stable pattern persistence.** Green paths that remain stable when zoomed/panned.
- **Decoherence = information leakage.** Red paths that fade or fragment when user changes scale/view. No-go routes that become visible only when drilling into a claim.
- **Information loss over distance.** Cards further from the current focal claim should render with less detail (decoration decoherence), not just smaller.

### 4.5 Optical Gravity

- **Path bending under gradients.** In the scale ladder, the vertical rail should visually bend or compress near dense claim clusters (Matter scale has 10 claims — it should visually "warp" relative to sparse scales).
- **Refractive index = density of proof.** Regions with many derivations should appear denser/brighter. Empty scales should appear evacuated.

### 4.6 Scale Covariance

- **The interface transforms under scale changes.** Dragging the scale scrubber should not just zoom — the claim cards, definition terms, and no-go markers should reposition, regroup, and re-label based on which scale cluster is in focus.
- **No fixed resolution.** At Planck scale, space itself looks different (quantum foam animation). At Human scale, familiar objects appear.
- **Smallest dot is a verb.** At the smallest visible scale, the dot should pulse/evolve — nothing is static at any scale.

### 4.7 Proof Obligations

- **Visual debt indicators.** Claims with open bridges should show an "unfinished" visual treatment: dashed borders, amber glow, or a partial-fill progress ring showing what fraction of the derivation chain is closed.
- **Accumulating proof.** When a claim moves from CONDITIONAL to DERIVED, a visual "lock" animation should play — the dashed border becomes solid, amber becomes green.

### 4.8 Hostile Audit

- **The audit view is not a skin — it is a different data density mode.** Switching to Audit mode should reveal: falsifier text, no-go strike-throughs on the graph, source links, confidence history sparklines, and Codex audit verdicts.
- **Audit mode should feel like reading a referee report over the manuscript.** Denser typography, more data per pixel, black ink on white paper aesthetic (or white ink on dark).
- **Red audit cuts should be visually uncomfortable.** They should interrupt the smooth story flow. The user should feel the friction of a failed route.

### 4.9 Typography

| Context | Font | Size | Style |
|---------|------|------|-------|
| Theorem titles, claim names, definitions | Strong serif (Playfair Display, EB Garamond) | 1.2-1.8rem | Bold, leading 1.3 |
| Controls, metadata, scale labels | Compact technical sans (Inter, SF Mono) | 0.75-0.9rem | Regular, letter-spaced |
| Equations, scripts, audit excerpts | Mono (JetBrains Mono, Fira Code) | 0.8-1.0rem | Regular |
| Narrative body | Light serif or humanist sans | 0.95-1.1rem | Regular, leading 1.6 |

### 4.10 Layout Principles

| Principle | Rule |
|-----------|------|
| No center box | Content lives on a full-width field, not in a centered column |
| No floating cards without context | Every card is anchored to a scale, a derivation step, or a proof path |
| No empty space that says nothing | Empty space = decoherence/absence. If a scale has no claims, label it "evacuated" |
| No decorative glow | All glow/color is semantically tied to status, propagation, or coherence |
| No animation from zero | Counters start at their actual value, not from 0 (avoid current comparison.html bug) |

---

## 5. Implementation Sequence

Per the brief: "no more isolated panels or cosmetic polish." The first build must prove the instrument concept.

### Phase 0 — Truth Surface Hardening (technical prerequisite)

**Owner**: Codex + Hermes

**Deliverables**:
1. `generate-data-graph.js` — Parses CLAIMS.md + definitions/README.md + nogos.js -> `data.graph.js` manifest
2. `data.graph.js` — Generated manifest with cross-ref resolution (definitions->claims, claims->no-gos, claims->experiments)
3. Extended `truth-utils.js` — All methods from §3.4
4. Data validation script — Ensures every claim's status matches CLAIMS.md, no orphan claims, no dead links
5. Smoke test script — Automated route verification for all workspaces

**Acceptance**:
- `data.graph.js` passes validation against CLAIMS.md and definitions/
- No orphan claim (every claim has a derivation chain back to axioms)
- Every canonical definition has its falsifier
- CI can regenerate `data.graph.js` and verify it

### Phase 1 — Observatory Shell (minimum viable instrument)

**Owner**: AntiGravity (implementation) + Claude (copy)

**Deliverables**:
1. **New homepage/observatory** with:
   - Scale rail (left) showing all 16 scales with claim counts
   - Propagation field (center) with animated cyan front
   - Truth summary bar (bottom) showing live counts from data layer
   - Story/Audit split
2. **Persistent command surface** — shared across all workspaces:
   - Scale scrubber
   - Story/Audit/Math toggle
   - Claim status filter checkboxes
   - Search (basic text search across claims + definitions)
3. **Shared inspector panel** — right-hand panel that opens on any claim click:
   - Shows claim title, status badge, confidence
   - Shows formula, scope, falsifier
   - Shows source links
   - Works the same way from any workspace

**Acceptance**:
- 5-second first-screen test: new viewer understands "reality is propagation through a structured Medium"
- All status badges read from data layer (no hardcoded statuses)
- Scale rail shows correct claim counts per scale

### Phase 2 — Proof Atlas + No-Go Integration

**Owner**: AntiGravity (graph rebuild) + Hermes (dependency graph)

**Deliverables**:
1. **Rebuilt derivation graph**:
   - Full-screen D3/Canvas layout with left filter rail + right inspector
   - Node labels readable at default zoom (minimum 10px font)
   - Clustered by claim with color-coded status borders
   - Legend does not overlap controls
2. **No-go overlays on graph**:
   - Red strike-through on edges that have been closed by no-go routes
   - Click no-go to jump to museum entry
3. **Open bridge visualization**:
   - Amber dashed edges for conditional/derivation steps
   - Pulse animation on open bridges
4. **Source receipts panel**:
   - Every node shows its source files
   - Click to open CLAIMS.md, derivation file, or sandbox script

**Acceptance**:
- Physicist can identify DERIVED vs CONDITIONAL within 30 seconds
- Every graph edge has a source link
- No-go routes are as visible as successes

### Phase 3 — Definition Lattice + Falsification Dashboard

**Owner**: AntiGravity (implementation) + Claude (copy)

**Deliverables**:
1. **Definition Lattice** (new route):
   - DAG of 19 definitions with bootstrapping order
   - Click any definition for full text, falsifier, dependencies, dependent claims
2. **Falsification Dashboard** (new route):
   - All claims in table view with falsifier status
   - Experiment log
   - Open attack surface

**Acceptance**:
- Every canonical term links to its definition file
- Every falsifier is visible and sourced
- Every claim links to its experiment evidence (or shows "no experiment yet")

### Phase 4 — Scale Instrument + Experiment Bench

**Owner**: AntiGravity (scale rebuild) + Codex (experiment data)

**Deliverables**:
1. **Rebuilt Scale Ladder**:
   - Default to Human scale with visible body/cell/atom/cosmic context
   - Scale ticks with named anchors
   - Associated claims visible on scale rail
   - "Smallest dot is a verb" animation at Planck scale
2. **Experiment Bench** (new route):
   - Cards for each sandbox script, hardware experiment, preregistered test
   - Links to claim it tests
   - Verdict badges

**Acceptance**:
- 61 orders of magnitude feel navigable
- Every sandbox script is linked to a claim

### Phase 5 — Story + Publish

**Owner**: Lumi (journey) + Claude (copy) + AntiGravity (presentation)

**Deliverables**:
1. Redesigned guided journey (5 conceptual shocks)
2. Presentation mode
3. Screenshots/social assets at 1440px, 1024px, mobile
4. Accessibility pass
5. Performance budget (load < 3s on 4G, 60fps animations)

---

## 6. Acceptance Gates (from the Redirection Brief)

The Explorer is not "world-class" until all are true:

| # | Gate | How to Verify | Owner |
|---|------|--------------|-------|
| 1 | **First screen test**: within 5 seconds, a new viewer understands the claim | Fresh user test; record verbal explanation | Claude + AntiGravity |
| 2 | **Physicist test**: within 30 seconds, DERIVED vs CONDITIONAL is obvious | Colleague review; timed identification | Codex |
| 3 | **Truth test**: every visible status is sourced from data layer | Script: grep for hardcoded statuses in HTML/JS | Hermes |
| 4 | **Instrument test**: every major control changes understanding | Before/after: user cannot explain PF → can explain PF after using scrubber | Lumi |
| 5 | **Scale test**: 61 orders feel navigable | User can find "Matter scale" and name a claim there in <10s | AntiGravity |
| 6 | **Failure test**: no-go routes are as visible as successes | Screenshot audit — no-go routes not hidden | Codex |
| 7 | **Mobile test**: usable on a phone | Lighthouse mobile audit > 70 | AntiGravity |
| 8 | **Screenshot test**: every route has a composed above-the-fold | Screenshots at 1440px saved in `screenshots/` | AntiGravity |

---

## Appendix A: File Map

| File | Purpose | Status |
|------|---------|--------|
| `data.js` | Current manual data snapshot | EXISTS — keep as fallback |
| `data.graph.js` | NEW generated manifest from source files | DOES NOT EXIST — Phase 0 |
| `generate-data-graph.js` | NEW parser from CLAIMS.md + definitions/ + nogos.js | DOES NOT EXIST — Phase 0 |
| `truth-utils.js` | Data access layer for all views | EXISTS — extend in Phase 0 |
| `core.js` | Current app shell logic | EXISTS — refactor for shared command surface |
| `index.html` | Homepage/observatory | EXISTS — rebuild as observatory in Phase 1 |
| `derivation.html` + `derivation-3d.js` | Current derivation graph | EXISTS — rebuild in Phase 2 |
| `scale-ladder.html` + `scale-ladder.js` | Current scale view | EXISTS — rebuild in Phase 4 |
| `nogos.html` + `nogos.js` | No-go museum | EXISTS — upgrade in Phase 2 |
| `journey.html` + `journey.js` | Guided story | EXISTS — redesign in Phase 5 |
| `comparison.html` | Framework comparison | EXISTS — fold into Falsification Dashboard (Phase 3) |
| `playground.html` + `playground.js` | Propagation lab | EXISTS — convert to Experiment Bench (Phase 4) |
| `panels/` | Individual claim panels | EXISTS — refactor data reads through truth-utils.js |
| `definitions-lattice.html` | NEW definition DAG route | DOES NOT EXIST — Phase 3 |
| `falsification.html` | NEW audit dashboard | DOES NOT EXIST — Phase 3 |
| `experiments.html` | NEW experiment bench | DOES NOT EXIST — Phase 4 |
| `style.css` | Current styles | EXISTS — refactor for new visual language |

## Appendix B: Agent Handoff Summary

| Agent | What They Own | First Action |
|-------|--------------|--------------|
| **Codex** | Truth validation, acceptance gates, `data.graph.js` schema | Define `generate-data-graph.js` schema + write data validation script |
| **AntiGravity** | Shell/visual implementation, all 7 workspaces | Build observatory homepage with scale rail + propagation field (Phase 1) |
| **Claude** | Technical copy for Story/Audit/Math modes, definition descriptions | Write route-level narrative + compress each claim into 7-question format |
| **Hermes** | Dependency graph, source link verification, truth sync | Build canonical dependency map + identify missing source links |
| **Lumi** | Guided journey narrative | Redesign journey as 5 conceptual shocks |
| **Pi/Devin** | Crystal search (future, not blocking) | Do nothing until Phase 5 — static Explorer must stand alone |
