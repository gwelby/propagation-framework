# Phase 1 Explorer Hardening Audit
*Codex audit note*
*Date: 2026-05-06*
*Scope: `sandbox/explorer` Phase 1 shell after AntiGravity workspace build*

---

## Verdict

**PASS WITH CONCERNS.**

The new Explorer shell now loads all five primary workspaces without browser runtime failures:

- `observatory`
- `proof-atlas`
- `definition-lattice`
- `no-go-museum`
- `experiment-bench`

The implementation is usable as a Phase 1 research instrument shell, but the Proof Atlas remains a shallow claim/axiom graph until the full derivation-step object graph is built.

---

## Fixes Applied

| Area | Finding | Fix |
|------|---------|-----|
| Core orchestration | `core.js` targeted old DOM IDs and old `[data-nav]` selectors | Rewired to `panelStage`, `appDrawer`, `drawerBody`, `workspaceSidebar`, and `[data-route]` |
| Command bar | `index.html` and `core.js` both mounted the command bar | Centralized mounting in `core.js` using `cbControls` |
| Drawer state | Drawer opened visually but did not keep ARIA state coherent | Added `aria-hidden`, `aria-expanded`, title/eyebrow/body updates |
| Proof Atlas | Panel passed structured claim objects into legacy graph code | Added graph-result adapter in `proof-atlas.js` |
| Derivation graph | Graph was not responsive and details bypassed the unified drawer | Added resize handling and delegated details to `PFExplorer.focusResult()` |
| Experiment Bench | Panel expected legacy `summary`, `formula`, `falsifier` fields | Mapped to `story`, `math`, and `audit.falsifier` |
| Definition Lattice | Cyclic definition dependencies caused infinite recursion | Added cycle guard in dependency-depth calculation |
| Source encoding | New shell contained mojibake in labels, buttons, and comments | Replaced bad characters with ASCII-safe labels and comments |
| Styling | New workspace classes were partially unstyled | Added CSS coverage for Observatory, Proof Atlas, Experiment Bench, and sidebar metrics |
| Local references | HTML asset/script references needed verification | Verified 33 local refs, 0 missing |

---

## Verification

```bash
node --check sandbox/explorer/data.claims.js
node --check sandbox/explorer/command-bar.js
node --check sandbox/explorer/core.js
node --check sandbox/explorer/derivation-graph.js
node --check sandbox/explorer/panels/observatory.js
node --check sandbox/explorer/panels/proof-atlas.js
node --check sandbox/explorer/panels/definition-lattice.js
node --check sandbox/explorer/panels/no-go-museum.js
node --check sandbox/explorer/panels/experiment-bench.js
```

All syntax checks passed.

```bash
google-chrome --headless=new --dump-dom http://127.0.0.1:18184/index.html#observatory
google-chrome --headless=new --dump-dom http://127.0.0.1:18184/index.html#proof-atlas
google-chrome --headless=new --dump-dom http://127.0.0.1:18184/index.html#definition-lattice
google-chrome --headless=new --dump-dom http://127.0.0.1:18184/index.html#no-go-museum
google-chrome --headless=new --dump-dom http://127.0.0.1:18184/index.html#experiment-bench
```

All five routes passed headless browser smoke testing.

---

## Remaining Concerns

| ID | Concern | Required Next Work |
|----|---------|--------------------|
| EX-01 | Proof Atlas edges are temporary axiom anchors, not audited derivation-step edges | Build the shared object graph: definitions, claims, derivations, no-go routes, experiments, sources |
| EX-02 | MathJax is lazy-loaded from CDN | Vendor MathJax locally if the Explorer must run fully offline |
| EX-03 | `implementation_plan.md` was referenced in the handoff but is not present | Either add it or stop referencing it in status updates |
| EX-04 | Several older standalone pages remain in the workspace | Decide whether they become drill-down views or are deprecated after the unified shell stabilizes |
| EX-05 | Browser smoke proves route load, not full UX quality | Next pass should test search, scale filtering, status filtering, mode switching, and mobile layout |

---

## Acceptance Boundary

This pass makes the Phase 1 Explorer shell operational. It does not certify the visual design as world-class and does not certify Proof Atlas semantics beyond "runtime-safe and truth-status bounded."
