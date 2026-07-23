# Explorer Master Plan

This is the single canonical plan for the Propagation Framework Explorer. It consolidates the prior planning documents (`EXPLORER_OVERHAUL_PLAN.md`, `GRAND_PLAN.md`, `PLAN_OVERHAUL.md`) and adds the **truth-layer / runtime-proof roadmap** that those plans did not cover.

## North Star

> "Every human intuition about reality is wrong. The Explorer makes you feel that — then shows you why — then shows you what replaces it."

The Explorer is a **reality-correction machine**: a browser experience that dismantles intuitive models of reality and replaces them with the propagation framework, while keeping every claim's true epistemic status visible.

## What the Explorer Is

- A set of HTML/JS panels (`index.html`, `journey.html`, `scale-ladder.html`, `comparison.html`, etc.) that visualize PF claims.
- A claim-status rendering layer that reads generated authority (`data.claims.js` / `PFClaimsData`) and displays badges/pills with exact status and confidence.
- A runtime-proof gate (`check_runtime_proof_v5.py`) that verifies every rendered status state is bound to an authority claim ID and matches generated authority.
- A public-facing surface subject to the **PUBLIC HOLD** until Codex clears the current audits.

## Legacy Plans (Superseded)

The following files are historical context and are no longer authoritative:

- `EXPLORER_OVERHAUL_PLAN.md` — original 7-pass visual/narrative overhaul.
- `GRAND_PLAN.md` — original 2.0 vision and Journey Mode.
- `PLAN_OVERHAUL.md` — early duplicate of the overhaul plan.

All future Explorer planning should use this file (`EXPLORER_MASTER_PLAN.md`) only.

## Roadmap

### Phase A — Truth Layer & Runtime Proof (ACTIVE)

The runtime proof is the gate that keeps the Explorer honest. No visual/narrative pass is release-ready unless the truth layer can prove every rendered claim-status state is authority-bound.

| Version | Status | What It Does | Next |
|---------|--------|--------------|------|
| **V5.1** | ✅ PASS | Authority-bound DOM verification, `PFClaimsData` / `PFExplorerData` unity, quarantine 404s, source hygiene. | — |
| **V5.2** | ❌ REJECT | Candidate-owned server, dynamic free port, `statusInventory` (9 entries on `index.html`), God Equation primary pill bound to `god-equation-operator`, scale badge bound to `god-equation-scale`. Rejected because inventory covers only `index.html` and generic pill collection precedes per-entry activation. | V5.3 |
| **V5.3** | ❌ REJECT | Complete inventory across every `servedRoutes` entry with `hasStatusContent: true` (30 entries); per-entry activation and inspection; bind every authority-bearing rendered status element with `data-claim-id`; copied-candidate negative fixtures with named failures. | Re-audited 2026-07-22: registry did not cover Journey `.result-card-status` (36) or Experiment Bench `.eb-status-pill` (36); generic scan did not include those selectors and inherited `data-claim-id` from parent cards. |
| **V5.4** | ❌ REJECT | Mechanical status-class scan covering `.status-pill`, `.status-badge`, `[data-status-note]`, `.result-card-status`, `.eb-status-pill`, `.result-status`; panel-walk activation for `index.html`; direct `data-claim-id` on every status-bearing element; dynamic inventory entries; copied-candidate fixtures for unbound Journey result-card and Experiment Bench pill. Rejected because `derivation.html` was falsely classified `hasStatusContent: false`, main D3 graph detail status had no claim binding, and timeline node/detail status used stale node confidence instead of the mapped authority. | V5.5 |
| **V5.5** | 🔧 IN PROGRESS | Authority-bound status for `derivation.html`: main D3 graph detail bound to `authorityClaimIds`, timeline node/detail bound via `NODE_TO_AUTHORITY` to current claim status/confidence, unmapped/intermediate nodes tagged `data-status-reason`, runtime proof exercises `#timelineToggle` and node selection, copied-candidate fixtures for main-graph unbinding, timeline unbinding, and Bohr confidence mismatch. | Awaiting Codex re-audit |

### Phase B — Visual & Narrative Experience

Based on `EXPLORER_OVERHAUL_PLAN.md` / `GRAND_PLAN.md` / `PLAN_OVERHAUL.md`.

| Pass | Name | Status | Scope |
|------|------|--------|-------|
| 1 | Narrative Architecture | 📋 | Confrontational opening / visual zoom hook, per-panel `wrongIntuition`, Journey mode restructure, CSS design system, hub as scale mission control. |
| 2 | Scale Ladder Core Engine | 📋 | Log-zoom navigation, shared propagation shader system, 16-scale scene engine, post-processing pipeline. |
| 3 | Cosmic + Planck Scenes | 📋 | Full Three.js at largest and smallest scales, procedural filament/foam generation. |
| 4 | Physics Panels 2.0 | 📋 | Propagation Playground, Reality Correction, Koide 3D, God Equation 2.0, enhanced refraction/Bohr. |
| 5 | Derivation + Audit Layer | 📋 | No-Go Museum, Derivation Timeline, audit trail as first-class UI. |
| 6 | World-Class Post-Processing | ✅ COMPLETE | `postprocessing.js` pipeline, fog, PBR materials, DOF/Bokeh, color grading. |
| 7 | Consciousness + Polish | ✅ COMPLETE | `consciousness.js`, `print.css`, responsive, prefers-reduced-motion, high-contrast mode, keyboard navigation, ARIA live regions. |

**Phase B depends on Phase A.** No new claim-bearing visual pass ships until the runtime proof can cover its rendered states.

## Active Repair Contracts (Explorer)

1. **V5.4 Dynamic Status Inventory Repair** — `/mnt/d/Codex/REPORTS/CODEX_20260722_EXPLORER_V5_3_COMPLETE_STATUS_INVENTORY_REAUDIT.md`
   - Mechanically scan all status-bearing DOM classes: `.status-pill`, `.status-badge`, `[data-status-note]`, `.result-card-status`, `.eb-status-pill`, `.result-status`.
   - Activate each real panel and compare every rendered authority-bearing item.
   - Direct `data-claim-id` on every status-bearing element (no parent inheritance).
   - Copied-candidate negative fixtures: unbound Journey result-card status and unbound Experiment Bench status pill.

## Cross-Dependencies

- `CLAIMS.md` is the authority for all status text/confidence.
- `data.claims.js` and `data.js` are generated from `CLAIMS.md`; never manually edited.
- `measurement_alignment/` (D1/D3) supplies current-data inputs; its language-enforcement scanner pattern is analogous to the Explorer's claim-binding scanner.
- `lean/PfLean/` provides machine-checked theorems that feed into `CLAIMS.md` statuses; any new formal result that changes a claim status must be reflected in the Explorer's authority data and re-proven by the runtime proof.
- `tools/publish_pf.sh` is the only allowed path to the public `pf` remote, per the 2026-07-21 history scrub.

## Current Blockers

- **PUBLIC HOLD** on Fundamentals claim surfaces until Codex recheck clears.

## Next Step

Await Codex re-audit of the V5.4 return packet.

## Boundaries

- No `CLAIMS.md` edits.
- No generated-authority tier changes, scientific promotion/demotion, or public/release action.
- No `git push pf` directly; use `tools/publish_pf.sh --push`.
