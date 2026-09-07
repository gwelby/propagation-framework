# AGENTS.md

## What this workspace is
This repository documents the Propagation Framework: a first-principles physics research framework built around the claim that propagation is fundamental. It treats space as a physical medium through which information propagates, rather than an empty mathematical void.

## Mission
Derive the structure of physical reality from three axioms (propagation is fundamental, causal velocity exists, coherence is necessary for stable structure).

## Tech Stack
- Python (core verification, simulation, and graph generation scripts)
- Pytest (unit and integration tests)
- Markdown (core documentation, derivation records, and live status scoreboards)

## Truth Order
1. `AGENTS.md` - Workspace rules and truth order
2. `CLAIMS.md` - Live scoreboard of claim statuses
3. `ACTIVE_ISSUES.md` - (if exists) Active obligations and blockers
4. `the_propagation_framework.md` - Canonical axioms and derived quantities
5. Code / Tests - Ground truth for derivations and simulations
6. Docs / Specs - Explanatory materials

*(Note: When in conflict, `sandbox_results.md` > `CLAIMS.md` > `the_propagation_framework.md` applies to derivation status.)*

## Key Commands
- Test suite: `python -m pytest tests/`
- Run God Equation verification: `python RESEARCH/god_equation_verification.py`
- Run Koide Triangle visualization: `python visualizations/koide_triangle.py`
- Demo Refractive Gravity: `python sandbox/refractive_gravity_demo.py`

## Boundaries
- **No inventing:** Do not state a result is "DERIVED" if it is only "ARGUED". Refer to `CLAIMS.md` for strict live statuses.
- **Do not merge PRs:** Leave them for review.
- **No reaching out:** Do not attempt to reach any service on 172.28.x.x or localhost.
- **Stay in scope:** Make minimal, targeted changes. Do not refactor unrelated code or fix unrelated test failures unless explicitly asked.

## Identity Reminder
Agents are agents, and the project is the project. This is a collaborative workspace between human vision and AI derivations, audits, and formalizations. Maintain absolute transparency about what is verified vs. what is a conditional or empirical fit.
