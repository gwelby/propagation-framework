# Explorer World-Class Redirection
*Codex product/design audit*
*Date: 2026-05-06*
*Scope: `/mnt/d/Fundamentals/sandbox/explorer/`*
*Status: REDIRECTION BRIEF — implementation not started*

---

## Verdict

The Explorer is technically functional but not yet worthy of the framework.

It currently feels like a collection of dark-mode demos: centered hero text, cards, sparse canvases, generic neon accents, and separate routes that do not yet add up to one cognitive instrument. The code has pieces of a strong interface, but the product direction is under-specified.

The target should be higher:

> **A physics observatory + proof atlas + falsification dashboard.**

The user should not feel like they are browsing a site. They should feel like they are operating an instrument that lets them move between scale, claim, proof, failure, and experiment.

---

## What Is Wrong Now

### 1. The homepage has no mechanism

Screenshot read: large centered sentence, one paragraph, one button. It says "your intuition is wrong" but does not immediately show the replacement model.

Missing:
- A visible propagation field.
- A scale axis.
- A claim/audit split.
- A concrete first proof object.
- Any sign that 19 definitions and 25 results are underneath.

### 2. The visual language is too generic

Current direction is mostly dark surface + cyan/purple glow + cards. This could be any AI dashboard. It does not yet express:
- finite propagation,
- phase closure,
- coherence vs decoherence,
- optical gravity,
- scale covariance,
- proof obligations,
- hostile audit.

The No-Go Museum is the closest to a real voice. It has a distinctive thesis: failed routes are evidence. That level of concept needs to exist everywhere.

### 3. The information architecture is not deep enough

The framework has several kinds of truth:
- canonical definitions,
- derived claims,
- conditional claims,
- empirical anchors,
- no-go routes,
- active proof obligations,
- experiments,
- bridge/spec work.

The Explorer flattens too much of this into cards and panels. It needs a consistent object model that lets every page answer:

1. What is the claim?
2. What canonical definitions does it depend on?
3. What standard physics boundary protects it?
4. What exactly has been derived?
5. What failed?
6. What would falsify it?
7. What is the next open bridge?

### 4. Several pages are visually empty or under-scaled

Observed screenshots:
- `derivation.html`: graph appears tiny in a large empty canvas; controls/legend collide near the top.
- `scale-ladder.html`: mostly empty field at initial view; little sense of 61 orders of magnitude.
- `comparison.html`: counters show `0` until interaction/animation; first impression reads broken.
- `journey.html`: competent but too plain for the conceptual ambition.

### 5. The interaction model is not yet an instrument

The app should have repeatable controls that matter:
- scrub scale,
- toggle story/audit/math,
- reveal dependencies,
- replay derivation,
- inject falsifier/noise,
- compare PF vs standard physics,
- open source receipts.

Right now controls are page-specific and not always tied to the framework's core epistemology.

---

## North Star

Build the Explorer around five persistent lenses:

| Lens | User question | Interface metaphor |
|------|---------------|--------------------|
| Scale | Where in reality am I? | Continuous log-scale observatory |
| Definition | What does this word mean canonically? | Living glossary / semantic lattice |
| Proof | How does this claim follow? | Derivation graph with proof obligations |
| Audit | What could kill it? | Falsification ledger / hostile audit wall |
| Experiment | What has actually held? | Receipts, scripts, data, sandbox outputs |

Every route should be a different camera into the same underlying object graph.

---

## Required Product Architecture

### Data model

Stop hand-thinking the UI per page. First define the object graph:

```text
Definition
  id, title, status, summary, canonical source, dependencies, falsifiers

Claim
  id, title, status, confidence, summary, formula, scope, falsifier, sources

Derivation
  id, claim_id, steps[], assumptions[], no_go_routes[], open_bridges[]

NoGo
  id, target_claim, failed_assumption, test/audit, result, lesson

Experiment
  id, claim_id, script/data, observed, expected, verdict

Route
  id, lens, primary_objects[], narrative beats[]
```

The current `data.js` is a useful snapshot, not enough for the final Explorer. The next build should introduce a generated `data.graph.js` or JSON manifest from `CLAIMS.md`, `definitions/README.md`, audit files, and no-go files.

### Page model

Replace "pages" with "workspaces":

| Workspace | Purpose |
|-----------|---------|
| Observatory | Entry page: scale + propagation field + current claim stack |
| Proof Atlas | Derivation graph, but large, legible, clustered by claim |
| Definition Lattice | 19 canonicals, dependency graph, term boundaries |
| No-Go Museum | Failed paths as first-class evidence |
| Experiment Bench | Sandbox scripts, verification outputs, benchmark status |
| Story Journey | Guided path for non-specialists |
| Physicist Audit | Dense source/audit mode for technical readers |

### Persistent UI

Use one persistent command surface:

```text
[Scale scrubber] [Story/Audit/Math] [Claim status filters] [Search] [Source receipts]
```

The user should be able to switch any object between:
- story explanation,
- math derivation,
- hostile audit,
- source receipts.

---

## Visual Direction

### Do not make another generic dark dashboard

Avoid:
- flat black backgrounds,
- isolated cards floating in empty space,
- purple hero text as the main identity,
- decorative glows without semantic meaning,
- counters that animate from zero without context,
- graph nodes too small to read.

### Use a specific visual language

Recommended direction:

**"Night observatory over a living proof manuscript."**

Core motifs:
- log-scale vertical field,
- thin instrument-grid overlays,
- luminous propagation fronts,
- paper-like proof cards embedded inside the field,
- red audit cuts where routes failed,
- green derived paths only when source-backed,
- amber conditional bridges visibly unfinished.

### Color semantics

Use color only as meaning:

| Color | Meaning |
|-------|---------|
| Cyan | propagation / causal movement |
| Green | coherence / stable derived path |
| Amber | conditional/open bridge |
| Red | no-go/falsifier/audit strike |
| Gold | empirical anchor / measurement |
| White | canonical definition text |

Purple should not dominate the site. It can be a rare "axiom/root" accent.

### Typography

The current typography has partial gravitas but too much centered hero styling. Use:
- strong serif for theorem titles and proof statements,
- compact technical sans for controls and metadata,
- mono for equations, receipts, scripts, and audit excerpts.

The site should look like a lab notebook became an observatory, not like a landing page.

---

## Immediate Fixes Before Any Large Rewrite

These are small but high-signal:

1. **Homepage must show the instrument immediately.**
   - Add live scale rail.
   - Show "19 definitions / 25 claims / 13 no-go routes / active bridges".
   - Show one animated propagation front crossing scales.
   - Show a split: `Story` vs `Audit`.

2. **Derivation page must be rebuilt for legibility.**
   - Full-screen graph area.
   - Left rail with claim clusters.
   - Right inspector.
   - Node labels readable at default zoom.
   - Legend cannot overlap controls.

3. **Scale ladder must not start empty.**
   - Default to Human scale with visible body/cell/atom/cosmic context.
   - Show scale ticks and named anchors.
   - Show associated claims on the scale rail.

4. **Comparison counters cannot show zero as the first impression.**
   - Start with actual values or show "counting..." state.
   - Avoid misleading parameter comparisons if source is not audited.

5. **Definition Lattice must exist.**
   - The 19 canonicals are now the framework bedrock. They need their own route.

---

## Agent Assignments

### Codex

Role: truth architecture and acceptance gates.

Tasks:
- Define `data.graph.js` schema.
- Guard claim status boundaries.
- Verify that no UI copy promotes conditional claims.
- Write smoke tests for every route.
- Audit generated data against `CLAIMS.md` and `definitions/README.md`.

Acceptance:
- No page can display `DERIVED`, `CANONICAL`, or confidence values not sourced from the data layer.
- Every result has a falsifier and source trail.
- Every canonical term links to its definition file.

### AntiGravity

Role: implementation and visual system.

Tasks:
- Rebuild homepage into an observatory/instrument.
- Rebuild derivation graph layout for default readability.
- Create Definition Lattice route.
- Refactor route shell so all workspaces share controls and inspector behavior.
- Add screenshot smoke script.

Acceptance:
- Screenshots at 1440px, 1024px, and mobile must look intentionally composed.
- No route should present a mostly empty viewport.
- First screen must communicate the framework, not just a slogan.

### Claude

Role: information architecture and technical copy.

Tasks:
- Write route-level narrative for Story/Audit/Math modes.
- Compress each claim into: claim, standard boundary, derived part, open bridge, falsifier.
- Draft Definition Lattice descriptions from canonical files.
- Remove overclaim language.

Acceptance:
- A physicist can identify exactly what is proved and what is not within 30 seconds.
- A non-specialist can explain "propagation/coherence/causal velocity" after the first route.

### Hermes

Role: system map and dependency graph.

Tasks:
- Build canonical dependency map: definitions -> claims -> derivations -> no-go routes.
- Identify missing source links.
- Keep `CLAIMS.md` / `ACTIVE_ISSUES.md` status synchronized with Explorer data.

Acceptance:
- No orphan claim.
- No dead link in the proof/audit graph.
- Open bridges are visible and named.

### Lumi

Role: narrative/cinematic sequence.

Tasks:
- Redesign the guided journey as a sequence of conceptual shocks:
  1. object is process,
  2. force is path bending,
  3. particle is stable mode,
  4. failure is evidence,
  5. consciousness is metric-gated.
- Keep the emotional arc without weakening audit boundaries.

Acceptance:
- Journey feels memorable, but every dramatic sentence has an audit-safe counterpart.

### Pi / Devin

Role: search and live knowledge support.

Tasks:
- Later, expose Crystal query/search to Explorer as optional local service.
- Do not block static Explorer on runtime services.
- Any live search must show source status and offline fallback.

Acceptance:
- Static Explorer remains complete without services.
- Live Crystal only enhances search/lookup.

---

## Implementation Phases

### Phase 0 — Stabilize Truth Surface

Already mostly done 2026-05-06:
- `data.js` synced to 19 canonical definitions.
- route smoke checks pass.
- local assets fixed.

Remaining:
- Add an automated smoke script.
- Add data validation script.

### Phase 1 — Product Shell

Deliver:
- new homepage observatory,
- persistent command surface,
- Definition Lattice route,
- shared inspector.

### Phase 2 — Proof Atlas

Deliver:
- rebuilt derivation graph,
- open bridge visualization,
- no-go overlays,
- source receipts.

### Phase 3 — Scale Instrument

Deliver:
- rebuilt Scale Ladder,
- real scale anchors,
- visible cross-scale claim placement,
- "smallest dot is a verb" visual mechanism.

### Phase 4 — Story + Publish

Deliver:
- guided journey,
- presentation mode,
- screenshots/social assets,
- accessibility pass,
- performance budget.

---

## Acceptance Gates

The Explorer is not "world-class" until all are true:

1. **First screen test:** within 5 seconds, a new viewer understands the claim: reality is modeled as propagation through a structured Medium.
2. **Physicist test:** within 30 seconds, a technical viewer can see which claims are derived, conditional, empirical, or no-go.
3. **Truth test:** every visible status is sourced from the data layer and source files.
4. **Instrument test:** every major control changes understanding, not just decoration.
5. **Scale test:** the site makes 61 orders of magnitude feel navigable, not abstract.
6. **Failure test:** no-go routes are as visible as successes.
7. **Mobile test:** the experience is usable and intentional on a phone.
8. **Screenshot test:** every primary route has a composed above-the-fold screenshot.

---

## Dispatch Summary

Tell the team:

```text
Codex says the Explorer is technically functional but product-weak. Do not add more panels yet. Rebuild the Explorer around one instrument model: scale, definition, proof, audit, experiment. AntiGravity owns the shell/visual implementation. Claude owns story/audit copy. Hermes owns the dependency graph. Codex owns truth validation and acceptance gates. Lumi owns the guided journey. Pi/Devin can later add live Crystal search, but the static Explorer must stand alone.
```

