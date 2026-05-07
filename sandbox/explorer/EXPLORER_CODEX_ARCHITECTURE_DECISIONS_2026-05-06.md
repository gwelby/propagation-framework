# Explorer Architecture Decisions
*Codex implementation guidance*
*Date: 2026-05-06*
*Status: DECISION RECORD — handoff to AntiGravity/Claude/Hermes*

## Verdict

AntiGravity's proposed direction is accepted with modifications.

The correct architecture is **one instrument shell over one object graph**. The Explorer should not remain a collection of independent pages with local data hacks.

## Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Nav shape | **Desktop: left rail + top command bar. Mobile: compressed top workspace switcher.** | A top tab strip competes with the command bar and will not scale once search, filters, source receipts, and object inspector exist. A left rail makes the five workspaces feel like instrument modes, not marketing tabs. |
| Math mode | **Use MathJax, lazy-loaded only when Math mode is opened or a route requires equations.** | This is a physics proof atlas. Monospace LaTeX is acceptable as a loading fallback, not as the final math experience. The extra payload is justified if it is lazy-loaded. |
| Proof Atlas location | **Inside the unified `index.html` shell. Keep legacy pages as deep-link redirects/adapters only.** | The command bar, status filters, scale scrubber, and object inspector must be persistent. A separate Proof Atlas repeats the current fragmentation problem. |
| Workspace count | **Use five primary workspaces; expose Story Journey and Falsification Dashboard as modes/sections, not top-level nav.** | Five is the right cognitive load for first use. The omitted lenses are still required, but they should live inside the shell: Story as a presentation mode, Falsification as an Experiment/Audit subview. |
| Existing panels | **Preserve as drill-down views from Proof Atlas and object inspector.** | Do not delete working specialist panels. Demote them from top-level navigation and keep direct deep links working. |
| Data source | **`data.claims.js` is presentation copy, not the truth source.** | CLAIMS.md and canonical definitions remain authoritative. The UI can import generated/patched copy, but status/confidence promotion must never happen in UI code. |

## Required Shell Structure

```text
ExplorerShell
  LeftWorkspaceRail
  PersistentCommandBar
    ScaleScrubber
    StoryAuditMathToggle
    StatusFilters
    Search
    SourceReceiptsButton
  MainWorkspaceCanvas
  RightObjectInspector
```

## Primary Workspaces

| Workspace | What it must show first | Notes |
|-----------|-------------------------|-------|
| Observatory | Log-scale field with claims pinned by scale and status | This replaces the empty hero page. First view must show mechanism, not slogan. |
| Proof Atlas | Large derivation graph with open bridges and no-go cuts visible | Must be legible at initial viewport. No tiny graph in a dead canvas. |
| Definition Lattice | 19 canonical definitions including `axioms`, excluding `consciousness` | Bootstrapping order and dependency edges are the point. |
| No-Go Museum | Failed routes as evidence | Keep this top-level. It is one of the framework's strongest trust signals. |
| Experiment Bench | Sandbox results, audit receipts, falsification dashboard | Must answer: predicted, tested, observed, pass/fail, next experiment. |

## Acceptance Gates

1. First viewport shows at least one live claim, its status, its scale, and one source receipt.
2. `consciousness.md` is never displayed as canonical.
3. `axioms.md` appears in the Definition Lattice.
4. The only green/DERIVED claims are `gravity-optical`, `koide-leptons`, and `weinberg-angle`.
5. God Equation remains `CONDITIONAL 0.88` everywhere.
6. Three Generations remains `CONDITIONAL 0.85` everywhere.
7. Koide Phase remains `EMPIRICAL 0.65` everywhere.
8. Bekenstein Bound, if shown, is `UNSYNCED`, not `DERIVED`.
9. Existing links to old pages continue to work or redirect to the equivalent shell workspace/object.
10. MathJax is lazy-loaded; Story/Audit mode should not pay the MathJax cost.

## Immediate Build Order

1. Create the unified shell and persistent command bar.
2. Wire `data.claims.js` after the Codex audit fixes.
3. Build Observatory first, because it sets the visual thesis.
4. Build Definition Lattice second, because it exposes the 19-definition foundation now missing from the site.
5. Move Proof Atlas into the shell and make the graph readable.
6. Re-home current specialist panels as drill-downs.

## Non-Negotiable Copy Rule

Every claim card must have three views:

```text
Story: what a smart non-specialist should understand.
Audit: claim / standard boundary / derived part / open bridge / falsifier.
Math: formula, assumptions, source receipt.
```

If any claim lacks all three, it is not ready for the world-class shell.
