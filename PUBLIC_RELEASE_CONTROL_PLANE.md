# Fundamentals Public Release Control Plane

**Last verified:** 2026-07-15 EDT  
**Owner of release truth:** Codex  
**Human release authority:** Legal + Greg  
**Status:** ACTIVE operating surface

> This is the single routing surface for public release. It does not replace
> scientific truth sources such as `sandbox_results.md`, Lean, `CLAIMS.md`, or
> the canonical definitions. It translates those authorities into separate,
> artifact-specific public gates. Old release plans remain history.

## The Decision

There is no single switch called "make Fundamentals public." The public body
is split into independent release rings. A blocked book must not silently
block a claim-safe art/education site, and a clean website must not be used to
imply that the scientific framework or book is release-cleared.

Each ring moves only when its **exact immutable body** passes its own gates.
Marketing receives only a ring-specific release packet, never a source tree or
a general statement that "Fundamentals is public."

## Current Ring Matrix

| Ring | Public role | Exact current body | Current verdict | Decisive blocker | What Marketing may do now |
|---|---|---|---|---|---|
| A. Phiharmonic Studio | Interactive sound, field, and light experiences | `phiharmonic-public-20260715.tar.gz`, SHA-256 `88b4d1ae86d2d0a0cfa959b850a55bab9d7e7fc16315e8749f58e6a02a9b95c6` | **PACKAGE PASS / LIVE HOLD** | DNS does not resolve; deployment credential gate is `1/17`; exact live body has not been retrieved and rechecked | Draft launch material from the approved Field/Light scope. Do not publish it until a live-body receipt exists. Do not market PF validation or Hau endorsement. |
| B. Research Atlas / Explorer | Interactive map of claims, derivations, gaps, and no-go results at `unifiedfield.net` | Dirty `/mnt/d/fundamentals/sandbox/explorer` candidate on commit `4791633a7767f514f9b2380c3f9a5437e4bf6462`; current worktree contains multiple owner lanes | **HOLD** | V2 parser/generator is real but live `data.js` still creates stale independent `PFExplorerData`; the gate exempts it, misses public entry points/bare labels, and trusts cached snapshot records. Desktop/mobile clipping and uncaught WebGL remain separate blockers; no immutable release identity. | Nothing public-facing. Marketing may study audience/navigation only. |
| C. Quantum Knowledge Base | Definitions, current claim tiers, sources, and open questions | `/mnt/d/Domains/quantumknowledgebase.com` static tree; no current release manifest | **EMERGENCY CONTENT HOLD** | Eyesight private-path page is quarantined and its legacy URL returns 404, but stale `DERIVED` labels, overclaiming home/paper copy, consciousness/EEG claims, broken research links, and no implemented generation gates remain | Nothing. Do not repair by selective copy editing; regenerate from current authorities. |
| D. Fundamentals Book | Long-form publication | Current v6 source/HTML/print/PDF in `/mnt/d/fundamentals` | **EMERGENCY RELEASE HOLD** | Source map parses 81 rows instead of 49; health-intervention material remains; Legal/Greg pending. The prior false Codex-PASS row was corrected to HOLD on 2026-07-15. | Nothing public or buyer-facing. |
| E. Physicist Outreach | Questions and correspondence based on released research | `outreach/` packages | **HOLD** | No claim-bearing public reference body is release-cleared; Greg gate remains | Internal preparation only. Hau posture remains gratitude and questions, never validation or endorsement. |
| F. Marketing Campaigns | Distribution of an approved public body | No current Fundamentals release packet | **WAITING FOR RING PACKET** | Marketing has no exact live URL/body hash/allowed-claims contract | Maintain channels and templates. Do not infer claims from old Marketing files. |

## Direct Verification Snapshot - 2026-07-15

### Live network state

| URL | Direct result | Release meaning |
|---|---|---|
| `https://phiharmonic.org` | DNS resolution failure (`curl` exit `6`) | Verified package is not live. |
| `https://unifiedfield.net` | DNS resolution failure (`curl` exit `6`) | Explorer has no live release body. |
| `https://quantumknowledgebase.com` | HTTP `403` from Cloudflare | A host responds, but the exact public body is not retrievable for audit. |

### Explorer gate state

- **REJECT:** Devin's V2 generated-truth completion claim. The parser and
  deterministic 36-claim artifact are genuine, but `data.js` still drives live
  stale `PFExplorerData` in the shell and standalone pages. The gate exempts
  that source, misses bare hard-coded labels, and can accept a cached forged
  snapshot plus forged public record. V3 is routed; report:
  `/mnt/d/Codex/REPORTS/CODEX_20260715_EXPLORER_GENERATED_TRUTH_LAYER_V2_REAUDIT.md`.
- **REJECT:** Devin's V1 generated-truth completion claim. An empty authority
  source still emits all 27 records; unknown claim, forged source hash, and
  empty scope probes pass. The deployable sidebar/panels retain known stale
  statuses while the submitted gate reports green. Governing re-audit:
  `/mnt/d/Codex/REPORTS/CODEX_20260715_EXPLORER_GENERATED_TRUTH_LAYER_REAUDIT.md`.
- **FAIL:** generated `PFDataGraph` contains 36 claims / 21 definition
  surfaces, while later-loaded manual `PFClaimsData` contains 27 / 19. Only
  14 claim IDs are shared; this is not one deterministic public truth layer.
- **NARROW PASS:** Python gate syntax compiles; all 58 root/panel/worker
  JavaScript files pass `node --check`; the expanded nonblank visual sampler
  paints content for all 18 registered routes at 1440x900.
- **FAIL:** route smoke reaches an uncaught `Error creating WebGL context` on
  `quantum-observatory` in the project's headless acceptance environment.
- **FAIL:** the full-frame responsive gate detects 318 px of desktop body
  clipping. At 390x844 the sidebar consumes 280 px, leaving a 108 px panel
  stage while the body is clipped by about 1304 px. Multiple routes also have
  stage-local overflow.
- **Meaning:** a center-pixel/nonblank pass is retained as useful render
  evidence, but it is not a visual release verdict. Truth copy, graceful
  fallback, framing, overlap, and responsive bounds remain separate gates.

Durable screenshots:
`/mnt/d/Codex/EVIDENCE/fundamentals_release_intake_20260715/`.

### Book and Knowledge Base gate state

- Book source-map replay remains **49 intended / 81 live / 32 excess** and
  includes `derivations/*.md`; exit `1`.
- The mechanical release gate remains **FAIL**: four manifest gates are not
  green. Its forbidden-phrase stage also fails closed because the build
  directory contains more than 200 text files, so the exact release scan body
  is still not bounded.
- The Knowledge Base source still promotes Weinberg to `DERIVED` and presents
  "Three Axioms. Everything Else Derived." The legacy Eyesight page is now
  quarantined from the deploy tree and its exact legacy URL returns 404, but
  the proposed deny/generation gates are not implemented. This remains a
  regenerate lane, not a copy-edit or deployment lane.

## Ring Gates

### A. Phiharmonic Studio

Authority and evidence:

- `/mnt/d/Domains/reports/PHIHARMONIC_REBUILD_20260715.md`
- verified deployment archive and SHA-256 listed in the matrix

Required next sequence:

1. Greg restores the owned DNS/deployment credentials without exposing them in
   a packet or log.
2. Domains deploys the verified archive, not the old consulting site and not
   the Explorer tree.
3. Retrieve the exact apex and `www` bodies over HTTPS.
4. Repeat desktop/mobile screenshots, interactions, console checks, TLS,
   headers, sitemap, and local-link checks against the live body.
5. Write a live release receipt containing URL, deployment time, body/archive
   identity, commands, screenshots, negative evidence, and rollback path.
6. Codex checks that receipt. Greg authorizes launch. Marketing receives the
   approved Field/Light packet.

This ring does **not** lift any Fundamentals claim, book, medical, or outreach
hold.

### B. Research Atlas / Explorer

Current direct blockers:

- The candidate is not an immutable release: it is a dirty `gh-pages` tree.
- V1 was rejected and V2 is also rejected. V2 parses current authority, but it
  does not drive all public status copy and fails open on live legacy data,
  cached-manifest tampering, complete public-tree coverage, and premise/scope.
- `VISUAL_PASS_RESULTS.md` proves a May commit, not the July candidate.
- Story copy currently outruns adjacent audit boundaries. Examples include
  treating space as a physical substrate, energy as frequency, all forces as
  refraction, and the charged-lepton Koide selection story as a completed PF
  explanation. The live authorities do not support those broad promotions.
- A new `quantum-observatory` route is untracked and has no release receipt.
- The existing nonblank visual sampler now covers all 18 routes, but the new
  full-frame gate fails on desktop/mobile clipping and missing WebGL fallbacks.

Required next sequence:

1. Freeze the candidate as a named commit or immutable archive. Preserve
   unrelated existing work; no release from a dirty tree.
2. Generate the claims layer from `CLAIMS.md` and canonical definitions, or
   produce a complete machine-diff proving every hand-curated public claim
   matches them.
3. Separate three labels in every result: **standard physics**, **PF result
   under named premises**, and **open PF interpretation**.
4. Run syntax, static acceptance, negative fixtures, link/source, private-path,
   accessibility, responsive-layout, and panel-health checks.
5. Run a full browser visual pass on every route and panel at desktop and
   mobile. A nonblank center sample is necessary but not sufficient; inspect
   framing, text overlap, controls, errors, and interaction.
6. Create an Explorer release manifest with candidate hash, panel inventory,
   exact test receipts, current claim snapshot hash, screenshots, and known
   exclusions.
7. Codex truth re-audit -> AntiGravity visual sign-off -> Greg deployment
   approval -> exact live-body recheck -> Marketing packet.

### C. Quantum Knowledge Base

The current static tree is not a patch target. It is a generated-product
candidate whose generator/source contract is missing.

Required next sequence:

1. Preserve the completed Eyesight quarantine: it is outside the deployable
   body, but must not be restored without a verified private-path gate and
   Greg approval.
2. Define a compact schema sourced from `CLAIMS.md`, canonical definitions,
   Lean scope, and current Codex verdicts.
3. Generate, rather than hand-maintain, claim badges and open-question rows.
4. Fail the build when a source claim changes without a regenerated page, when
   a public tier is stronger than authority, or when private/local paths occur.
5. Verify citations, links, accessibility, responsive rendering, sitemap,
   robots policy, and exact live retrieval.
6. Codex claim audit -> Greg release approval -> Marketing packet.

### D. Fundamentals Book

Current direct evidence, rerun 2026-07-15:

- Source-map probe: **49 intended / 81 live / 32 excess**, including
  `derivations/*.md`; exit `1`.
- Mechanical release gate: **FAIL**; content/claim, Legal, and Greg gates are
  not green. Its broad forbidden-phrase scan also fails closed at more than
  200 text files, so it does not yet identify one bounded release body.
- The v6 manifest's false Codex-PASS row was corrected to current HOLD truth
  on 2026-07-15; this repair does not clear the underlying release blockers.
- Governing audit:
  `/mnt/d/Codex/REPORTS/CODEX_20260714_FUNDAMENTALS_V6_MEDICAL_RELEASE_REAUDIT.md`.

Required next sequence:

1. Bound `parse_source_map()` from `## FRONT MATTER` to the start of
   `# PART IV — AGENT PROTOCOLS`; fail closed if either marker is absent.
2. Add a focused negative fixture proving Part IV rows and
   `derivations/*.md` cannot enter the publication map.
3. Exclude `frequency_human_resonance/MASTER.md` / Appendix E from the public
   build unless it receives qualified medical and Legal review.
4. Keep the corrected `RELEASE_MANIFEST.md` HOLD rows synchronized with every
   new audit; never infer release status from `BUILD_MANIFEST.md`.
5. Rebuild source, HTML, print HTML, and PDF; retain source-map output, hashes,
   full health/claim/leak scans, representative and adversarial page images,
   and a truthful build manifest.
6. AntiGravity packet -> Codex content/release re-audit -> Legal -> Greg.

### E-F. Outreach and Marketing

Outreach is not the mechanism for validating the theory. It begins with a
released reference body and asks bounded questions. Marketing is not the
mechanism for deciding what is true. It distributes only an already approved
body.

## Marketing Entry Contract

Every ring-specific packet delivered to Marketing must contain all fields
below. A missing field means **NO PUBLISH**.

| Field | Required content |
|---|---|
| Release identity | Product name, immutable archive/commit/body hash, release date |
| Exact public body | Canonical HTTPS URL(s), retrieved after deployment |
| Audience and job | Who it is for and the one useful thing they can do there |
| Allowed claims | Exact sentences or bounded paraphrase rules |
| Forbidden claims | Named promotions, medical implications, endorsements, cross-ring inferences |
| Evidence links | Public citations and internal audit/release receipt |
| Assets | Approved screenshots/audio/video with hashes and alt text |
| Channel scope | Which email/social/press channels are authorized |
| Human gates | Legal status, Greg approval, date, approver identity |
| Rollback owner | Who stops or corrects the campaign if live truth changes |
| Measurement | Visits, completion/interaction, qualified replies; never claim truth by engagement |

Marketing must not receive private paths, raw research trees, stale launch
copy, hidden medical claims, or a generic instruction to "promote
Fundamentals."

## Release Order

1. **Deploy and live-verify Phiharmonic Studio.** This is the closest public
   win and is independent of framework claim clearance.
2. **Truth-lock and visually verify Explorer.** This becomes the inspectable
   research interface at `unifiedfield.net`.
3. **Regenerate the Knowledge Base from authorities.** It becomes the stable
   reference layer behind Explorer.
4. **Repair and re-audit the book.** The book can then cite the two public
   reference surfaces instead of trying to contain the entire workspace.
5. **Open outreach, then Marketing, one approved ring at a time.**

## Definition of Done

A ring is public only when all are true:

- its exact immutable candidate is named;
- truth/content, visual/runtime, security/privacy, and legal/human gates are
  recorded separately;
- local tests and exact live retrieval both pass;
- a release receipt says what passed, what remains excluded, and what the
  release does not approve;
- Codex has not been represented as approving any scope it did not audit;
- Greg has approved the exact body;
- Marketing has a complete entry contract.

Until then, use the verdict in the matrix. Build success, a pretty screenshot,
an agent agreement, or a prior deployment is not release approval.
